# Transparency Gap Diagnostic
Date: 2026-05-21
Author: Raj (staff-backend)
Mode: DIAGNOSTIC ONLY — no code changed

---

## A. HEARTBEAT MECHANISM

**Finding: Zero scheduler code exists anywhere in the bridge. The "heartbeat every 5 min" promise was structurally impossible.**

Search results for scheduler, cron, timer, asyncio.sleep, periodic, interval across all of `org_bridge/` returned zero hits. Here is the entirety of the `main()` entrypoint:

```python
# org_bridge/main.py, lines 247–255
async def main() -> None:
    await startup()
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    log.info("Org Bridge is online. Talk to Devika in #org-chief.")
    await handler.start_async()
```

`handler.start_async()` is a blocking call that parks the event loop waiting for Slack socket events. There is no `asyncio.create_task()`, no background task, no APScheduler, no Celery beat, nothing. The process is purely reactive: it does work only when a Slack message arrives. Devika's admission that she "isn't a persistent daemon" is technically accurate — but the gap is in the bridge code, not in the agent. A real heartbeat would require a background coroutine running alongside the socket handler.

**What it would take:** Add one `asyncio.create_task(heartbeat_loop())` call before `handler.start_async()`, where `heartbeat_loop()` is an `async def` that calls `run_agent(chief, STATUS_PROMPT)` and posts the result to `#org-warroom` every N minutes. This is a 30-line addition. The risk is it burns LLM tokens on a cadence regardless of whether anything changed.

---

## B. CLICKUP INTEGRATION

**Finding: ClickUp tasks are created and updated on artifact publish, but `update_status` and `list_open` from `clickup.py` are dead code — never called from anywhere in the bridge.**

`clickup.py` exposes four functions: `search_tasks`, `create_task`, `update_status`, `list_open`. A codebase-wide grep for callers of `update_status` and `list_open` outside the venv returns zero results. The publisher (`publisher.py`) does NOT import `clickup.py` at all — it hand-rolls its own inline HTTP calls to the ClickUp REST API (lines 238–270 of `publisher.py`). So `clickup.py` is an orphan module.

What the publisher actually does:

```python
# publisher.py, lines 210–270 (_upsert_ticket)
# On every artifact publish:
# 1. GET /list/{list_id}/task — fetch all tasks, find by name match
# 2. If found: PUT /task/{id} — update description only
# 3. If not found: POST /list/{list_id}/task — create with status="Spec"
```

What it does NOT do:
- Never calls `update_status` to advance a ticket (Spec → Building → Done)
- Never marks a ticket closed or Done
- Never calls `list_open` to surface what's pending to the founder
- The `clickup.py::update_status()` function (line 77) exists but has zero call sites in production code

So the answer to "why can't I see discussions closing in ClickUp" is exact: the only status a ticket ever gets is `"Spec"` (set at creation, line 267 of `publisher.py`). It never moves. Completion is not modeled in any code path.

---

## C. SLACK DISCUSSION CLOSING

**Finding: The bridge posts a `white_check_mark` reaction on the triggering message after an agent responds, but no thread close marker, no "discussion closed" message, and no status channel update is ever posted.**

The full post-response sequence in `main.py`:

```python
# org_bridge/main.py, lines 129–146
for piece in _split_for_slack(full):
    await post_as_agent(channel_id, agent, piece)

# Auto-publish any new or changed artifacts
if PUBLISHER:
    post_snapshot = snapshot_dirs(ORG_ROOT, WATCH_DIRS)
    for changed_path in diff_snapshots(pre_snapshot, post_snapshot):
        ...
        result = await PUBLISHER.publish(changed_path, agent)

await react(channel_id, ts, "white_check_mark")
```

The `white_check_mark` reaction is on the founder's original message. It signals the bot processed the request. It does not signal the discussion/work item is complete, closed, or handed off. There is no concept of "closing" a Slack thread in the bridge. There is no message posted to `#org-warroom` saying "task X closed." The `slack-manifest.yaml` does not declare any slash commands, shortcuts, or interactivity that would let a human or agent mark a thread resolved.

The warroom announcement (`publisher.py::_announce`, lines 274–298) fires when an artifact is published — it says "New PRD published" but says nothing about the prior work item being closed.

---

## D. DECISION TRAIL

**Finding: The manifest exists and is actively maintained. The decisions files have dense narrative. However, there is no WHY column in the manifest, no rejected-alternatives log, and no causal chain linking a manifest entry to the conversation that produced it.**

The `.manifest.jsonl` has 7 entries, all from 2026-05-21, all with working GitHub URLs and ClickUp ticket IDs. Each entry is a snapshot of the artifact at publish time:

```json
{"ts": "2026-05-21T06:53:48...", "slug": "signal-innovator-pressure", "type": "test",
 "file": "decisions/signal-innovator-pressure-test.md", "commit": "6759a4d...",
 "github_url": "https://github.com/punkstack/yamer/blob/6759a4d.../...",
 "clickup_ticket_id": "86d32q0mu", "clickup_url": "https://app.clickup.com/t/86d32q0mu"}
```

What is missing from the manifest:
- No `agent` field — you cannot tell which agent wrote the artifact
- No `triggered_by` field — no link to the Slack message or conversation that initiated the work
- No `rationale` field — why this artifact exists, what decision it closed
- No `supersedes` field — when a doc is updated (signal-spm-prd.md appears 3 times across entries 3, 5, 6), there is no indication entry 6 supersedes entries 3 and 5

The `memory/state.md` file is the best decision trail that exists. It has chronological entries with context (e.g., "Founder picked Alex's V0.1 unit-of-work"). A third party could reconstruct the broad arc from `state.md` alone. But `state.md` is a flat narrative file maintained by convention, not by code — there is no code path that forces `state.md` to be updated when an artifact is published. It is updated manually by the Chief agent at session end. If an agent runs between sessions, or if the Chief forgets, `state.md` drifts.

The `decisions/*.md` files themselves do contain rationale inside their content, but that content is not indexed or linked — a third party must open each file and read prose.

---

## E. ROOT CAUSE SYNTHESIS

The systemic failure is a single architecture choice: **the bridge is a pure event-loop reactor with no scheduled work and no lifecycle model for tasks.** Every component assumes work is initiated by a Slack message and completed when the agent responds. There is no concept of a task being "open," "in progress," or "closed" at the bridge level — those states live only inside ClickUp (where they never change from "Spec") and in prose inside `state.md` (where updates depend on the Chief agent remembering to write them). The `clickup.py` module has the right primitives (`update_status`, `list_open`) but they are never wired into any execution path. The heartbeat is impossible not because it is hard to build but because the event loop has no background task slot allocated for it. Every transparency feature was designed at the agent-prompt layer ("Devika will post updates") without any bridge-layer mechanism to enforce or even enable it.

---

## F. RANKED FIX OPTIONS

### Gap 1: Heartbeat (periodic status updates)

**Option 1A — Background coroutine in the bridge (S effort, high impact, low risk)**
Add `asyncio.create_task(heartbeat_loop())` in `main.py::startup()` before the socket handler starts. The coroutine calls `run_agent(chief, HEARTBEAT_PROMPT)` on an interval (e.g., every 30 min, configurable via env). Result is posted to `#org-warroom`. Risk: burns tokens on cadence; if Claude is slow, loop can drift. Mitigation: add a timeout and skip if previous tick is still running.
DRI: Raj (backend).

**Option 1B — External cron job hitting a `/heartbeat` HTTP endpoint (M effort, high impact, medium risk)**
Add a minimal HTTP server (FastAPI, single route) to the bridge. A cron job (crontab, GitHub Actions schedule, Railway cron) POSTs to `/heartbeat` on schedule. Risk: adds an HTTP surface; requires a second process or deployment change. More ops overhead than 1A for the same result.
DRI: Karthik (devops).

**Option 1C — Slack scheduled messages via the API (M effort, low impact, no code risk)**
Use the Slack API `chat.scheduleMessage` to post templated status requests into `#org-chief` on a cadence. This doesn't involve Claude at all — it's a cron-driven Slack message that triggers Devika the same way the founder would. Zero new infrastructure. But the "heartbeat" is only as good as Devika's response to a prompted message — it is not a true daemon.
DRI: Karthik (devops).

**Recommendation:** 1A. It is the minimum viable implementation: 30 lines in one file, no new infrastructure, configurable interval.

---

### Gap 2: ClickUp task lifecycle (open → in-progress → done)

**Option 2A — Call `update_status` in the publisher on artifact type (S effort, high impact, low risk)**
In `publisher.py::_upsert_ticket()`, after creating or updating a ticket, call `update_status(ticket_id, status)` based on `doc_type`: prd/options/arch → "Spec", tasks → "Building", build/qa/audit → "Review", grillme closed → "Done". This re-uses the existing `clickup.py::update_status` function that is currently dead. The publisher already has the ticket_id in scope. Risk: requires ClickUp statuses in the workspace to match exactly — misconfigured status names will throw 400s silently (need error logging).
DRI: Raj (backend).

**Option 2B — Add a `close_discussion()` call from `handle_for_agent` after artifact publish (M effort, high impact, medium risk)**
After the publisher loop in `main.py::handle_for_agent()`, check if any published artifact is of a "terminal" type (audit, grillme, build-report) and call `clickup.update_status(ticket_id, "Done")`. Requires passing ticket_id back from `PublishResult` (already in the dataclass). Risk: determining "terminal" artifact type is heuristic — wrong classification closes tickets prematurely.
DRI: Raj (backend).

**Option 2C — Manual close slash command in Slack (M effort, low impact, low risk)**
Add a `/close-task <clickup-id>` slash command to the manifest and wire it in the bridge. Founder manually closes. Solves the symptom but not the root cause — still requires human action after every discussion.
DRI: Karthik (devops).

**Recommendation:** 2A. Wires the already-written `update_status` function into the one code path that runs on every artifact publish. Lowest effort, directly addresses the complaint.

---

### Gap 3: Slack discussion closing marker

**Option 3A — Post a closing message to the agent's channel thread after artifact publish (S effort, medium impact, low risk)**
In `main.py::handle_for_agent()`, after the publisher loop, if at least one artifact was published, post a closing message in the agent's channel (not warroom): `"Discussion closed. Artifact: {doc_type} for {slug}. ClickUp: {ticket_url}"`. Use `thread_ts` to keep it in the triggering thread. Risk: near-zero. One `chat_postMessage` call.
DRI: Raj (backend).

**Option 3B — Add `resolve` reaction to thread (S effort, low impact, low risk)**
After publishing, add a `white_check_mark` + `closed_lock_with_key` reaction sequence to the triggering message. Slightly more visible than the current single checkmark but does not post a message with links.
DRI: Raj (backend).

**Option 3C — Warroom "closed" summary post (S effort, medium impact, low risk)**
Add a second `#org-warroom` post after artifact publishing that explicitly says "Closed: [agent] finished [task]. ClickUp: [link]." Currently the warroom post only says "New artifact published." Separate the "published" signal from the "closed" signal.
DRI: Raj (backend).

**Recommendation:** 3A + 3C together. 3A closes the thread in the agent's channel (where the founder was talking). 3C gives the warroom a clear "discussion closed" event separate from the "artifact created" event. Combined effort is still S.

---

### Gap 4: Decision trail / audit log

**Option 4A — Add `agent` and `triggered_by_ts` fields to the manifest (S effort, high impact, low risk)**
In `publisher.py::_manifest_record()`, add `agent.key` and optionally the Slack `ts` of the triggering message (pass it through from `handle_for_agent`). Then superseded entries are identifiable by slug+type+agent, and the full thread is recoverable via the Slack API using `ts`. No schema migration needed — JSONL is append-only and schema-free.
DRI: Raj (backend).

**Option 4B — Write a `decisions/.decisions-log.md` in human-readable append mode (S effort, medium impact, low risk)**
On every artifact publish, append a structured line to a human-readable log: `2026-05-21T14:51 | signal-spm | vision | Sarah (Senior PM) | Slack ts=1234 | ClickUp 86d32vj9w`. A third party can read this file without parsing JSONL. Risk: slight duplication with manifest, but serves a different audience (human readability vs. machine parsing).
DRI: Raj (backend).

**Option 4C — Enforce `state.md` update via the publisher (M effort, high impact, medium risk)**
After every artifact publish, call `run_agent(chief, STATE_UPDATE_PROMPT)` to force Devika to append the decision to `state.md`. This makes the state update automatic rather than relying on the Chief's memory at session end. Risk: burns extra tokens on every publish; Devika might produce drift if the prompt isn't tight. Also adds latency to every artifact publish.
DRI: Raj (backend).

**Recommendation:** 4A is mandatory and costs 5 lines. 4B is recommended alongside it — it gives the founder a human-readable trail without opening JSONL. 4C is deferrable; the existing state.md discipline is good enough for now if 4A+4B are in place.

---

## Summary Table

| Gap | Recommended Fix | Effort | Impact | Risk | DRI |
|-----|----------------|--------|--------|------|-----|
| Heartbeat | 1A: background coroutine in main.py | S | High | Low | Raj |
| ClickUp lifecycle | 2A: wire update_status in publisher | S | High | Low | Raj |
| Slack close marker | 3A + 3C: thread close msg + warroom close post | S | Medium | Low | Raj |
| Decision trail | 4A + 4B: agent field in manifest + human log | S | High | Low | Raj |

All four recommended fixes are S-effort. Combined, they are a single focused PR. None of them require architectural changes to the bridge — they wire existing code paths that were designed but never connected.

**Founder action required:** Review this report and greenlight which fixes to implement. No code has been changed.
