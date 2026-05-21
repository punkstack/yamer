# Transparency Channel — Spec

**Ticket:** updates appended to `86d32w30g` (parent transparency-gap) as a new sub-scope.
**DRI:** Raj (staff-backend)
**Status:** Backlog → awaiting founder greenlight on heartbeat-fix-plan first.

## What the founder asked for (verbatim intent)

> "Launch tech to make a new channel which shows transparency — who is working on what, and every 10 mins everyone is gonna send the updates."

## Scope

1. **New Slack channel:** `#org-pulse` (or `#org-transparency` — Raj picks the cleaner name).
   - Purpose: single read-only feed of "who is doing what right now."
   - No human conversation in this channel — bot-only posts.

2. **10-minute pulse cadence:**
   - Every 10 minutes, the bridge posts one consolidated message to `#org-pulse`.
   - Format per active agent:
     ```
     *Sarah (spm)* — _Working on:_ <current task> · _Since:_ <HH:MM> · _Last artifact:_ <file or "none">
     ```
   - If an agent is idle, list it under `⏸ Idle: Sarah, Raj, ...`
   - If no agents active for 3 consecutive ticks, post a single `🌙 Quiet — no active agents.`

3. **Per-agent self-report:**
   - When an agent is dispatched, it MUST write its current task to a state file (e.g. `memory/agent-status.json`) at start and on every meaningful step.
   - The 10-min pulse reads that file. No LLM call in the pulse tick.
   - If an agent has been "active" >30 min with no artifact + no status update → flagged `⚠ stalled` in the pulse.

4. **Closes the loop with heartbeat work:**
   - Heartbeat (already scoped in `decisions/heartbeat-fix-plan.md`) provides the active-agent `set[str]`.
   - This pulse builds on that set + adds the "since" timestamp + "last artifact" lookup from `decisions/.manifest.jsonl`.
   - Reuses the same coroutine scheduler — second `asyncio.create_task` with a 600s interval.

## Constraints (paste into ticket)

- **DO NOT START** until founder greenlights the heartbeat-fix-plan first. Heartbeat is the foundation.
- **No LLM in the pulse tick.** Deterministic snapshot only. Cost = $0.
- **Single DRI:** Raj. No parallel work.
- **Plan before code:** Raj writes a 1-page fix plan to `decisions/transparency-channel-plan.md` and waits for founder sign-off before implementing.
- **Phase 2 follow-up** (already noted): dispatched-but-no-artifact-in-N-min → alert. Roll into this same ticket.

## Effort estimate

- S (small): ~50 lines on top of the heartbeat coroutine. New channel ID in env, new state file write at agent dispatch chokepoint, second scheduler tick.

## Why this matters (bird's-eye)

This is the systemic fix for the silent-fail problem we hit with Mia today. We dispatched her in narrative; nothing actually ran; we had no signal for 30+ min. With `#org-pulse`, that gap is visible in 10 min max.
