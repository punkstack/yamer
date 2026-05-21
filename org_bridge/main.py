"""Org Bridge — Slack <-> Claude agents.

Run with: python main.py

Architecture:
  - Socket Mode (no public URL needed)
  - Each agent owns one Slack channel
  - Messages in #org-<agent>     → that agent receives + replies AS that persona
  - DMs to the bot               → routed to Devika (Chief of Staff)
  - @mentions anywhere           → routed to Devika
  - Per-channel rolling chat memory keeps multi-turn flows (like THE GRILL) coherent
  - Agent replies post via chat_postMessage with username + icon_emoji
    so they render as Sarah, Raj, Mia, etc. — not as a generic "Org bot"
"""

import asyncio
import os
import logging
from pathlib import Path
from collections import deque, defaultdict

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

load_dotenv(Path(__file__).resolve().parent / ".env")

from agents import Agent, ORG, BY_KEY, agent_for_channel, WARROOM_CHANNEL
from claude_loop import run_agent
from slack_setup import setup_channels

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("org-bridge")

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

CHANNEL_IDS: dict[str, str] = {}      # name -> id
CHANNEL_NAMES: dict[str, str] = {}    # id -> name

# Per-channel rolling chat memory. Each entry is (role, text).
# role is "founder" or "agent". Replayed to the agent on every turn so
# multi-turn flows (THE GRILL especially) keep continuity.
HISTORY_TURNS = int(os.getenv("CHAT_HISTORY_TURNS", "6"))
CHAT_LOG: dict[str, deque[tuple[str, str]]] = defaultdict(
    lambda: deque(maxlen=HISTORY_TURNS * 2)
)


# -------------------------------------------------------------------
# Posting as an agent
# -------------------------------------------------------------------

async def post_as_agent(channel_id: str, agent: Agent, text: str, thread_ts: str | None = None) -> None:
    """Post a message in `channel_id` rendered as `agent` (custom username + emoji)."""
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
# Build the prompt for an agent — includes recent chat history
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
# Core: run an agent and stream back to Slack
# -------------------------------------------------------------------

async def handle_for_agent(agent: Agent, channel_id: str, user_id: str, text: str, ts: str) -> None:
    log.info("→ %s | %s | %r", agent.key, user_id, text[:80])
    await react(channel_id, ts, "eyes")

    # Record founder turn BEFORE invoking, so the agent sees its own context
    CHAT_LOG[channel_id].append(("founder", text))
    prompt = build_prompt(channel_id, agent, text)

    chunks: list[str] = []
    try:
        async for chunk in run_agent(agent, prompt):
            chunks.append(chunk)
    except Exception as e:
        log.exception("agent run failed")
        await post_as_agent(channel_id, agent, f"_[I hit an error: {e}]_")
        await react(channel_id, ts, "warning")
        return

    full = "".join(chunks).strip() or "_[no response]_"

    # Record agent turn into history before posting
    CHAT_LOG[channel_id].append(("agent", full))

    for piece in _split_for_slack(full):
        await post_as_agent(channel_id, agent, piece)

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
# Slack event handlers
# -------------------------------------------------------------------

@app.event("message")
async def on_message(event, say):
    # Ignore our own posts (set username override but bot_id is still present)
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

    # Routing:
    #   DM           → Devika (Chief of Staff)
    #   #org-warroom → Devika
    #   #org-<agent> → that agent
    #   other        → ignore (handled by app_mention if needed)
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

    # Strip leading @mention token
    parts = text.split(" ", 1)
    clean = parts[1] if len(parts) > 1 else ""
    if not clean:
        return

    await handle_for_agent(BY_KEY["chief"], channel_id, user_id, clean, ts)


# -------------------------------------------------------------------
# Startup
# -------------------------------------------------------------------

async def startup() -> None:
    auth = await app.client.auth_test()
    log.info("Connected as bot %s in workspace %s", auth["user"], auth["team"])

    log.info("Setting up channels...")
    ids = setup_channels()
    CHANNEL_IDS.update(ids)
    CHANNEL_NAMES.update({v: k for k, v in ids.items()})
    log.info("Ready. %d channels live.", len(CHANNEL_IDS))


async def main() -> None:
    await startup()
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    log.info("Org Bridge is online. Talk to Devika in #org-chief.")
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
