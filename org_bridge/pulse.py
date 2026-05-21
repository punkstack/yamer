"""Pulse — 10-minute transparency ticker for #org-pulse.

Every PULSE_INTERVAL_SEC seconds, reads memory/agent-status.json and posts
a consolidated snapshot to the Slack channel identified by pulse_channel_id.

Design constraints:
- NO LLM call. Deterministic snapshot only. Cost = one chat_postMessage per tick.
- Stall detection: agent active >STALL_THRESHOLD_SEC with no last_artifact_ts update
  since the run started → flagged ⚠ stalled in the post.
- If no agents active for QUIET_TICKS_THRESHOLD consecutive ticks → single quiet post.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("org-bridge.pulse")

PULSE_INTERVAL_SEC     = int(os.getenv("PULSE_INTERVAL_SECONDS", "600"))   # 10 min default
STALL_THRESHOLD_SEC    = int(os.getenv("STALL_THRESHOLD_SECONDS", "1800"))  # 30 min
QUIET_TICKS_THRESHOLD  = int(os.getenv("QUIET_TICKS_THRESHOLD", "3"))


# -------------------------------------------------------------------
# Formatter (pure function — no I/O, fully testable without Slack)
# -------------------------------------------------------------------

def format_pulse(status: dict, now_iso: str | None = None) -> str:
    """Format the pulse message from the agent-status dict.

    Args:
        status: parsed contents of memory/agent-status.json
        now_iso: ISO timestamp string for "now" (injectable for tests)

    Returns:
        Slack-formatted string ready to post.
    """
    if now_iso is None:
        now_iso = datetime.now(timezone.utc).isoformat()

    try:
        now_dt = datetime.fromisoformat(now_iso)
    except ValueError:
        now_dt = datetime.now(timezone.utc)

    active_lines: list[str] = []
    idle_names: list[str] = []

    for agent_key, entry in sorted(status.items()):
        state = entry.get("state", "idle")
        persona = entry.get("persona", agent_key)
        task = entry.get("task") or ""
        start_ts = entry.get("start_ts")
        last_artifact = entry.get("last_artifact") or "none"

        if state in ("active", "stalled"):
            since = "?"
            stalled = False

            if start_ts:
                try:
                    start_dt = datetime.fromisoformat(start_ts)
                    elapsed = (now_dt - start_dt).total_seconds()
                    since = _format_elapsed(int(elapsed))
                    if state != "stalled" and elapsed > STALL_THRESHOLD_SEC:
                        stalled = True
                except ValueError:
                    pass

            stall_marker = " ⚠ stalled" if (state == "stalled" or stalled) else ""
            task_display = f" _Working on:_ {task[:80]}" if task else ""
            active_lines.append(
                f"*{persona} ({agent_key})*{stall_marker} —{task_display}"
                f" · _Since:_ {since}"
                f" · _Last artifact:_ `{last_artifact}`"
            )
        else:
            idle_names.append(persona)

    parts: list[str] = ["*Org Pulse*"]

    if active_lines:
        parts.append("\n".join(active_lines))
    else:
        parts.append("_No active agents._")

    if idle_names:
        parts.append(f"⏸ Idle: {', '.join(idle_names)}")

    return "\n".join(parts)


def _format_elapsed(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins  = minutes % 60
    return f"{hours}h {mins}m"


# -------------------------------------------------------------------
# Pulse coroutine
# -------------------------------------------------------------------

async def pulse_loop(
    pulse_channel_id: str,
    slack_client,
    status_file: Path,
) -> None:
    """Post a transparency snapshot to #org-pulse every PULSE_INTERVAL_SEC seconds.

    Args:
        pulse_channel_id: Slack channel ID for #org-pulse
        slack_client:     the AsyncApp's .client (passed in to keep pulse testable)
        status_file:      path to memory/agent-status.json
    """
    consecutive_quiet = 0

    while True:
        await asyncio.sleep(PULSE_INTERVAL_SEC)
        try:
            if status_file.exists():
                try:
                    raw = status_file.read_text()
                    status: dict = json.loads(raw) if raw.strip() else {}
                except (json.JSONDecodeError, OSError):
                    log.warning("pulse: could not parse %s — skipping tick", status_file)
                    continue
            else:
                status = {}

            # Count active agents for quiet-mode tracking
            active_count = sum(
                1 for e in status.values()
                if e.get("state") in ("active", "stalled")
            )

            if active_count == 0:
                consecutive_quiet += 1
            else:
                consecutive_quiet = 0

            if consecutive_quiet >= QUIET_TICKS_THRESHOLD and active_count == 0:
                # Post single quiet message (only once per quiet run, not every tick)
                if consecutive_quiet == QUIET_TICKS_THRESHOLD:
                    await slack_client.chat_postMessage(
                        channel=pulse_channel_id,
                        text="No active agents.",
                        username="Org Pulse",
                        icon_emoji=":zzz:",
                    )
                log.info("pulse: quiet tick %d — no active agents", consecutive_quiet)
                continue

            text = format_pulse(status)
            await slack_client.chat_postMessage(
                channel=pulse_channel_id,
                text=text,
                username="Org Pulse",
                icon_emoji=":bar_chart:",
            )
            log.info("pulse posted (active=%d)", active_count)

        except Exception:
            log.exception("pulse tick failed")
