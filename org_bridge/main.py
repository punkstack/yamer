"""Org Bridge — Slack <-> Claude agents, with auto-publishing.

Run with: python main.py

Architecture:
  - Socket Mode (no public URL needed)
  - Each agent owns one Slack channel
  - Messages in #org-<agent>     -> that agent receives + replies AS that persona
  - DMs to the bot               -> routed to Devika (Chief of Staff)
  - @mentions anywhere           -> routed to Devika
  - Per-channel rolling chat memory keeps multi-turn flows (THE GRILL) coherent
  - Agent replies post via chat_postMessage with username + icon_emoji
  - After every agent turn, NEW or CHANGED files in ./decisions/ and ./mockups/
    are auto-published: git commit + push, ClickUp ticket, war-room announcement
"""

import asyncio
import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from collections import deque, defaultdict

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

load_dotenv(Path(__file__).resolve().parent / ".env")

from agents import (
    Agent, ORG, BY_KEY, agent_for_channel,
    WARROOM_CHANNEL, PULSE_CHANNEL, ORG_ROOT,
    write_agent_status, record_artifact,
)
from pulse import pulse_loop
from claude_loop import run_agent
from slack_setup import setup_channels
from publisher import Publisher, snapshot_dirs, diff_snapshots

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("org-bridge")

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

CHANNEL_IDS: dict[str, str] = {}      # name -> id
CHANNEL_NAMES: dict[str, str] = {}    # id -> name

HISTORY_TURNS = int(os.getenv("CHAT_HISTORY_TURNS", "6"))
CHAT_LOG: dict[str, deque[tuple[str, str]]] = defaultdict(
    lambda: deque(maxlen=HISTORY_TURNS * 2)
)

# Directories the publisher watches for new artifacts
WATCH_DIRS = ["decisions", "mockups"]

# Initialized at startup once we have the warroom channel id
PUBLISHER: Publisher | None = None

# -------------------------------------------------------------------
# Heartbeat state — module-level, mutated only by handle_for_agent
# (asyncio is single-threaded; no lock needed)
# -------------------------------------------------------------------

HEARTBEAT_ENABLED      = os.getenv("HEARTBEAT_ENABLED", "true").lower() != "false"
HEARTBEAT_INTERVAL_SEC = int(os.getenv("HEARTBEAT_INTERVAL_SECONDS", "300"))  # 5 min default

ACTIVE_AGENTS: set[str] = set()     # agent.key strings currently inside handle_for_agent
LAST_ARTIFACT: dict | None = None   # set by handle_for_agent after each successful publish


# -------------------------------------------------------------------
# Posting as an agent
# -------------------------------------------------------------------

async def post_as_agent(channel_id: str, agent: Agent, text: str, thread_ts: str | None = None) -> None:
    await app.client.chat_postMessage(
        channel=channel_id,
        text=text,
        username=agent.display_name,
        icon_emoji=agent.icon,
        thread_ts=thread_ts,
    )


async def react(channel_id: str, ts: str, emoji: str) -> None:
    try:
        await app.client.reactions_add(channel=channel_id, timestamp=ts, name=emoji)
    except Exception:
        pass


# -------------------------------------------------------------------
# Prompt building (with chat history replay)
# -------------------------------------------------------------------

def build_prompt(channel_id: str, agent: Agent, latest_user_msg: str) -> str:
    history = CHAT_LOG.get(channel_id)
    parts: list[str] = []

    if history:
        parts.append("Recent conversation in this Slack channel (oldest first):")
        for role, text in history:
            who = "Founder" if role == "founder" else agent.display_name
            parts.append(f"{who}: {text}")
        parts.append("")

    parts.append(f"Founder's latest message:\n{latest_user_msg}")
    parts.append("")
    parts.append(
        "Respond AS your persona, in Slack-flavored markdown "
        "(*bold*, _italic_, `code`). Keep individual messages under ~3000 chars."
    )
    return "\n".join(parts)


# -------------------------------------------------------------------
# Core: run an agent, then auto-publish anything they wrote
# -------------------------------------------------------------------

async def handle_for_agent(agent: Agent, channel_id: str, user_id: str, text: str, ts: str) -> None:
    global LAST_ARTIFACT

    log.info("-> %s | %s | %r", agent.key, user_id, text[:80])
    await react(channel_id, ts, "eyes")

    ACTIVE_AGENTS.add(agent.key)
    write_agent_status(ORG_ROOT, agent.key, "active", task=text[:120])

    CHAT_LOG[channel_id].append(("founder", text))
    prompt = build_prompt(channel_id, agent, text)

    # Snapshot watched directories so we can detect new/changed artifacts
    pre_snapshot = snapshot_dirs(ORG_ROOT, WATCH_DIRS)

    chunks: list[str] = []
    try:
        async for chunk in run_agent(agent, prompt):
            chunks.append(chunk)
    except Exception as e:
        log.exception("agent run failed")
        await post_as_agent(channel_id, agent, f"_[I hit an error: {e}]_")
        await react(channel_id, ts, "warning")
        return
    finally:
        ACTIVE_AGENTS.discard(agent.key)
        write_agent_status(ORG_ROOT, agent.key, "idle")

    full = "".join(chunks).strip() or "_[no response]_"
    CHAT_LOG[channel_id].append(("agent", full))

    for piece in _split_for_slack(full):
        await post_as_agent(channel_id, agent, piece)

    # Auto-publish any new or changed artifacts
    if PUBLISHER:
        post_snapshot = snapshot_dirs(ORG_ROOT, WATCH_DIRS)
        for changed_path in diff_snapshots(pre_snapshot, post_snapshot):
            try:
                result = await PUBLISHER.publish(changed_path, agent)
                log.info(
                    "published %s as %s-%s (commit=%s, ticket=%s)",
                    changed_path, result.slug, result.doc_type,
                    (result.commit_sha or "-")[:7], result.ticket_id or "-",
                )
                # Update module-level last artifact for heartbeat snapshot
                LAST_ARTIFACT = {
                    "slug": result.slug,
                    "doc_type": result.doc_type,
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "agent": agent.key,
                }
                # Update per-agent artifact record in agent-status.json
                record_artifact(ORG_ROOT, agent.key, result.slug, result.doc_type)
            except Exception:
                log.exception("publish failed for %s", changed_path)

    await react(channel_id, ts, "white_check_mark")


def _split_for_slack(s: str, limit: int = 3500) -> list[str]:
    if len(s) <= limit:
        return [s]
    out: list[str] = []
    buf: list[str] = []
    cur = 0
    for line in s.splitlines(keepends=True):
        if cur + len(line) > limit and buf:
            out.append("".join(buf))
            buf, cur = [], 0
        buf.append(line)
        cur += len(line)
    if buf:
        out.append("".join(buf))
    return out


# -------------------------------------------------------------------
# Heartbeat coroutine
# -------------------------------------------------------------------

async def heartbeat_loop(warroom_channel_id: str) -> None:
    """Post a status snapshot to #org-warroom every HEARTBEAT_INTERVAL_SEC seconds.

    Deterministic — no LLM call. Reads module-level ACTIVE_AGENTS and LAST_ARTIFACT.
    Cost: one chat_postMessage per tick, ~$0.
    """
    _start = asyncio.get_event_loop().time()
    _running = False

    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL_SEC)
        if _running:
            log.warning("heartbeat: previous tick still running — skipping")
            continue
        _running = True
        try:
            uptime_sec = int(asyncio.get_event_loop().time() - _start)
            active = sorted(ACTIVE_AGENTS) or ["none"]
            if LAST_ARTIFACT:
                last = (
                    f"`{LAST_ARTIFACT['slug']}-{LAST_ARTIFACT['doc_type']}`"
                    f" by {LAST_ARTIFACT['agent']} at {LAST_ARTIFACT['ts']}"
                )
            else:
                last = "none yet this session"

            lines = [
                "*Bridge heartbeat*",
                f"Uptime: {uptime_sec // 60}m {uptime_sec % 60}s",
                f"Active agents: {', '.join(active)}",
                f"Last artifact: {last}",
            ]
            await app.client.chat_postMessage(
                channel=warroom_channel_id,
                text="\n".join(lines),
                username="Bridge Monitor",
                icon_emoji=":heartbeat:",
            )
            log.info("heartbeat posted (uptime=%ds active=%s)", uptime_sec, active)
        except Exception:
            log.exception("heartbeat post failed")
        finally:
            _running = False


# -------------------------------------------------------------------
# Slack event handlers
# -------------------------------------------------------------------

@app.event("message")
async def on_message(event, say):
    if event.get("bot_id"):
        return
    if event.get("subtype") in ("message_changed", "message_deleted", "channel_join"):
        return

    user_id = event.get("user")
    channel_id = event.get("channel")
    text = (event.get("text") or "").strip()
    ts = event.get("ts")
    channel_type = event.get("channel_type", "")
    channel_name = CHANNEL_NAMES.get(channel_id, "")

    if not text:
        return

    target: Agent | None = None
    if channel_type == "im":
        target = BY_KEY["chief"]
    elif channel_name == WARROOM_CHANNEL:
        target = BY_KEY["chief"]
    elif channel_name.startswith("org-"):
        target = agent_for_channel(channel_name)

    if target is None:
        return

    await handle_for_agent(target, channel_id, user_id, text, ts)


@app.event("app_mention")
async def on_mention(event, say):
    user_id = event.get("user")
    channel_id = event.get("channel")
    text = (event.get("text") or "").strip()
    ts = event.get("ts")
    parts = text.split(" ", 1)
    clean = parts[1] if len(parts) > 1 else ""
    if not clean:
        return
    await handle_for_agent(BY_KEY["chief"], channel_id, user_id, clean, ts)


# -------------------------------------------------------------------
# Startup
# -------------------------------------------------------------------

async def startup() -> None:
    global PUBLISHER

    auth = await app.client.auth_test()
    log.info("Connected as bot %s in workspace %s", auth["user"], auth["team"])

    log.info("Setting up channels...")
    ids = setup_channels()
    CHANNEL_IDS.update(ids)
    CHANNEL_NAMES.update({v: k for k, v in ids.items()})
    log.info("Ready. %d channels live.", len(CHANNEL_IDS))

    # Initialize the publisher now that we know the war-room channel id
    PUBLISHER = Publisher(
        root=ORG_ROOT,
        slack_client=app.client,
        warroom_channel_id=CHANNEL_IDS.get(WARROOM_CHANNEL),
        clickup_api_key=os.getenv("CLICKUP_API_KEY") or None,
        clickup_list_id=os.getenv("CLICKUP_LIST_ID") or None,
        github_owner=os.getenv("GITHUB_OWNER") or None,
        github_repo=os.getenv("GITHUB_REPO") or None,
        github_token=os.getenv("GITHUB_TOKEN") or None,
        default_branch=os.getenv("GIT_DEFAULT_BRANCH", "main"),
    )
    log.info("Publisher active (clickup=%s github=%s)",
             bool(PUBLISHER.clickup_api_key and PUBLISHER.clickup_list_id),
             bool(PUBLISHER.gh_owner and PUBLISHER.gh_repo))

    if HEARTBEAT_ENABLED and CHANNEL_IDS.get(WARROOM_CHANNEL):
        asyncio.create_task(heartbeat_loop(CHANNEL_IDS[WARROOM_CHANNEL]))
        log.info("Heartbeat active — interval=%ds", HEARTBEAT_INTERVAL_SEC)
    else:
        log.info("Heartbeat disabled (HEARTBEAT_ENABLED=%s)", HEARTBEAT_ENABLED)

    # Launch 10-min transparency pulse — posts to #org-pulse
    pulse_channel_id = CHANNEL_IDS.get(PULSE_CHANNEL)
    if pulse_channel_id:
        status_file = ORG_ROOT / "memory" / "agent-status.json"
        asyncio.create_task(pulse_loop(pulse_channel_id, app.client, status_file))
        log.info("Pulse ticker active — interval=%ds channel=%s", 600, PULSE_CHANNEL)
    else:
        log.warning("Pulse ticker disabled — channel %s not found in CHANNEL_IDS", PULSE_CHANNEL)


async def main() -> None:
    await startup()
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    log.info("Org Bridge is online. Talk to Devika in #org-chief.")
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
