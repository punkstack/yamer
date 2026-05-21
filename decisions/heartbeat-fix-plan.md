# Heartbeat Fix Plan
Date: 2026-05-21
Author: Raj (staff-backend)
ClickUp: https://app.clickup.com/t/86d32w3ah
Diagnostic: decisions/transparency-gap-diagnostic.md (Gap 1, Option 1A)

---

## What we are building

A single `asyncio` background coroutine (`heartbeat_loop`) launched in `startup()` in
`org_bridge/main.py`. It wakes every N seconds, computes a status snapshot, and posts it
to `#org-warroom` as a plain `chat_postMessage` call. That is the entire scope.

**Out of scope for this PR:** ClickUp lifecycle (Gap 2), Slack thread closure (Gap 3),
manifest enrichment (Gap 4). Those are separate tickets.

---

## Exact file changes

### `org_bridge/main.py`

**Additions only. No deletions.**

1. Add two new constants near the top of the module (after `WATCH_DIRS` line 51):

   ```python
   HEARTBEAT_ENABLED      = os.getenv("HEARTBEAT_ENABLED", "true").lower() != "false"
   HEARTBEAT_INTERVAL_SEC = int(os.getenv("HEARTBEAT_INTERVAL_SECONDS", "300"))  # 5 min default
   ```

2. Add a module-level set to track in-flight agent runs (line ~53, after the constants above):

   ```python
   ACTIVE_AGENTS: set[str] = set()   # agent.key strings currently inside handle_for_agent
   ```

3. Modify `handle_for_agent` to bracket the agent run with ACTIVE_AGENTS bookkeeping
   (two lines: add at entry, discard in finally):

   - Entry  (after line 108 `react eyes`):  `ACTIVE_AGENTS.add(agent.key)`
   - Finally (wrapping the try/except block): `ACTIVE_AGENTS.discard(agent.key)`

4. Add module-level state for last artifact (line ~55):

   ```python
   LAST_ARTIFACT: dict | None = None   # set by handle_for_agent after each publish
   ```

5. In `handle_for_agent`, after the publish loop (line ~144, inside the `if PUBLISHER:` block),
   on successful publish set:

   ```python
   global LAST_ARTIFACT
   LAST_ARTIFACT = {
       "slug": result.slug,
       "doc_type": result.doc_type,
       "ts": datetime.now(timezone.utc).isoformat(),
       "agent": agent.key,
   }
   ```

6. Add the coroutine after the `_split_for_slack` function (~line 163):

   ```python
   async def heartbeat_loop(warroom_channel_id: str) -> None:
       """Post a status snapshot to #org-warroom every HEARTBEAT_INTERVAL_SEC seconds."""
       import asyncio
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
   ```

7. In `startup()` (after PUBLISHER is initialized, line ~244), add:

   ```python
   if HEARTBEAT_ENABLED and CHANNEL_IDS.get(WARROOM_CHANNEL):
       asyncio.create_task(heartbeat_loop(CHANNEL_IDS[WARROOM_CHANNEL]))
       log.info("Heartbeat active — interval=%ds", HEARTBEAT_INTERVAL_SEC)
   else:
       log.info("Heartbeat disabled (HEARTBEAT_ENABLED=%s)", HEARTBEAT_ENABLED)
   ```

### `org_bridge/main.py` — import addition

Add `from datetime import datetime, timezone` to the import block (line ~17).
`asyncio` is already imported.

### No other files change.

`agents.py` — read-only. We read `agent.key` from the existing `Agent` dataclass field,
no modifications needed.

`publisher.py` — read-only. We consume `result.slug`, `result.doc_type` from the existing
`PublishResult` dataclass, no modifications needed.

`requirements.txt` — no new dependencies. `slack_bolt`, `python-dotenv`, `asyncio`
(stdlib), `httpx` are all already present.

---

## Coroutine signature

```python
async def heartbeat_loop(warroom_channel_id: str) -> None
```

Parameters: only the warroom channel ID (a string, resolved once at startup from
`CHANNEL_IDS`). No other arguments — it reads `ACTIVE_AGENTS` and `LAST_ARTIFACT`
from module-level state.

---

## Status snapshot data model

A heartbeat post carries exactly four fields:

| Field | Source | Type |
|---|---|---|
| `uptime_sec` | `asyncio.get_event_loop().time()` since startup | int |
| `active` | `ACTIVE_AGENTS` module-level set | list[str] (agent keys) |
| `last_artifact` | `LAST_ARTIFACT` module-level dict | dict or None |
| `idle` | `len(ACTIVE_AGENTS) == 0` | derived |

No external reads. No filesystem reads. No `state.md` parsing. No LLM call.
This is intentional — see Design Decision 1 below.

---

## How active-agent state is read

We do NOT read from `state.md`, `agents.py`, or any file. That would require filesystem
I/O inside the heartbeat tick, introduce latency, and create a coupling to file format.

Instead, `ACTIVE_AGENTS: set[str]` is a module-level set maintained by
`handle_for_agent`. Entry: `ACTIVE_AGENTS.add(agent.key)`. Exit (always, via `finally`):
`ACTIVE_AGENTS.discard(agent.key)`. Cost: two lines added to the one function that is
the single bottleneck for all agent work in this bridge. No lock needed — `asyncio` is
single-threaded; the set is accessed only from the event loop.

---

## Reconnect behavior

`heartbeat_loop` is a plain `while True` with `asyncio.sleep`. It does not touch the
socket connection. If the Slack client `chat_postMessage` call fails (e.g., network blip),
the exception is caught and logged, `_running` is reset in `finally`, and the next tick
proceeds normally. There is no retry — a missed heartbeat tick is acceptable.

If the bridge process restarts, `asyncio.create_task(heartbeat_loop(...))` is called
again from `startup()`, resetting the uptime clock and ACTIVE_AGENTS.

---

## Log format

```
2026-05-21 14:51:00 [INFO] org-bridge: heartbeat posted (uptime=300s active=['none'])
2026-05-21 14:56:00 [WARNING] org-bridge: heartbeat: previous tick still running — skipping
2026-05-21 14:56:05 [INFO] org-bridge: heartbeat posted (uptime=605s active=['chief'])
```

---

## How to disable via env var

Set `HEARTBEAT_ENABLED=false` in `.env` or the process environment. The check in
`startup()` is `os.getenv("HEARTBEAT_ENABLED", "true").lower() != "false"`. Any value
that is not the string `"false"` (case-insensitive) leaves the heartbeat on. Default is
on.

To change the interval: `HEARTBEAT_INTERVAL_SECONDS=60` (integer seconds). Default 300.

---

## Test approach

One new file: `org_bridge/tests/test_heartbeat.py`.

Tests are pure `asyncio` unit tests using `pytest-asyncio`. No Slack credentials needed —
the Slack client is mocked.

### Test cases (five, one per TDD micro-task):

1. **`test_heartbeat_posts_to_warroom`**
   Build a mock `app.client` with a recorded `chat_postMessage`. Call `heartbeat_loop`
   with a 0-second interval (patch `HEARTBEAT_INTERVAL_SEC = 0`), let it run one tick,
   cancel the task. Assert `chat_postMessage` called once with the correct channel.

2. **`test_heartbeat_skip_when_running`**
   Patch `_running = True` before the tick by making the mock `chat_postMessage` hang
   (returns a coroutine that never completes). Schedule two ticks. Assert second tick logs
   the "skipping" warning and does NOT call `chat_postMessage` a second time.

3. **`test_heartbeat_disabled_via_env`**
   Patch `HEARTBEAT_ENABLED = False`. Verify `asyncio.create_task` is never called from
   a test-double `startup()`.

4. **`test_active_agents_tracked`**
   Simulate `handle_for_agent` entry and exit. Assert `ACTIVE_AGENTS` contains the key
   during the run and is empty after.

5. **`test_last_artifact_updated_on_publish`**
   Call the publish side-effect code directly (not via full `handle_for_agent`). Assert
   `LAST_ARTIFACT` has the expected slug, doc_type, agent key, and ISO timestamp.

No integration tests that hit Slack or ClickUp. Those require live credentials and belong
in a separate E2E suite outside CI.

---

## Design decisions

### Decision 1: No LLM call in the heartbeat tick

**Option considered:** call `run_agent(chief, HEARTBEAT_PROMPT)` per the diagnostic
Option 1A description.

**Rejected.** Calling `run_agent` on a cadence means every 5 minutes we burn ~$0.01–0.05
in API tokens whether anything changed or not. At 300 ticks/day that is $3–15/day for
a status post the founder may not read. It also introduces a 10–30 second latency per
tick and risks the "no 10-min agent loops" constraint from project config.

**Chosen:** deterministic snapshot from in-process state (`ACTIVE_AGENTS`, `LAST_ARTIFACT`,
uptime). The post is less verbose than an LLM summary but contains the actionable facts:
who is running, what last shipped, how long the bridge has been up. If the founder needs
deeper context they go to the agent's channel.

**Tradeoff accepted:** heartbeat text is plain and mechanical. It is not prose. That is fine
for a status ticker; prose costs money.

### Decision 2: Module-level set instead of reading state.md

**Option considered:** parse `memory/state.md` inside each heartbeat tick to derive
"active agents."

**Rejected.** `state.md` is a manually maintained narrative file (per the diagnostic). Its
format is not machine-parseable at a level of reliability that justifies taking it as the
source of truth for real-time active-agent state. It would also require a file read on
every tick. The set `ACTIVE_AGENTS` is the ground truth because it is mutated by the exact
code path that actually dispatches work.

---

## What I am NOT building in this PR

- ClickUp status lifecycle (Gap 2) — separate ticket
- Slack thread close marker (Gap 3) — separate ticket
- Manifest enrichment with agent/triggered_by fields (Gap 4) — separate ticket
- Any refactor of `agents.py` beyond reading `agent.key` (already a field on the dataclass)
- Retry logic for failed heartbeat ticks
- Rich LLM-generated status summaries

---

## Line count estimate

Changes to `main.py`: ~55 lines added (constants: 3, ACTIVE_AGENTS + LAST_ARTIFACT: 2,
bookkeeping in handle_for_agent: 4, heartbeat_loop coroutine: ~35, startup wiring: 4,
import addition: 1).

New test file: ~120 lines.

Total new code: ~175 lines. No deletions.
