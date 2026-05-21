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

---

## Scope C — Platform Team (added 2026-05-21 by founder)

> Founder verbatim: *"hire one more uber staff engineer who will be maintaining this virtual org tech update the same ticket and ask raj to handle this."*

**Decision:** stand up a dedicated **Platform Team** inside the virtual org whose sole charter is the bridge / infra / agent substrate itself — separate from product-feature work.

**New role: Arjun — Platform Staff Engineer**
- *Charter:* owns `org_bridge/` end-to-end. Heartbeat, pulse, ClickUp lifecycle, agent dispatch confirmation, decision-manifest schema, observability, cost guards.
- *Reports to:* Devika (Chief of Staff) for prioritization; technical depth equal to Raj.
- *Distinct from Raj:* Raj is product-backend (the things customers buy). Arjun is platform (the things that make the org itself run). No overlap, no two-DRI ambiguity.
- *Persona file:* `.claude/agents/platform.md` (to be created by Raj as part of this ticket — agent prompt, house rules, mandatory loop).
- *Slack channel:* `#org-arjun-platform`.

**Raj's deliverables for this scope (inside the same ticket):**
1. Write `.claude/agents/platform.md` defining Arjun's persona, charter, and mandatory loop. Mirror the structure of `.claude/agents/staff-backend.md`.
2. Update `org_bridge/agents.py` to register `platform` as a known agent with channel routing to `#org-arjun-platform`.
3. Update `org_bridge/slack-manifest.yaml` to add `#org-arjun-platform` (and `#org-pulse`) channels.
4. Update `memory/state.md` org chart section to include Arjun under a new "Platform Team" header.
5. Once Arjun exists, **transfer ownership of the heartbeat + pulse work from Raj to Arjun** — Raj kicks it off, Arjun maintains it. This avoids Raj being both product and platform DRI.

**Why fold into one ticket, not split:** the Platform Team only exists *to maintain this kind of work*. Standing up the team and shipping its first deliverable (heartbeat + pulse) in the same PR is the cleanest demo of the team's purpose. Splitting = 3 tickets that all block each other.

**Constraints (unchanged + new):**
- Plan-before-code applies to the Platform Team setup too. Raj writes a 1-pager: `decisions/platform-team-charter.md` covering Arjun's scope boundary vs Raj, the explicit list of files Arjun owns, and the handoff protocol for heartbeat/pulse.
- Founder signs off on the charter before any code or persona files are written.
- No Phase 3 scope creep ("we should also have Arjun build X") — charter defines the boundary; new asks go to a new ticket.

## Capability-honesty footnote

This spec is written locally in `decisions/`. The ClickUp ticket update itself needs the bridge bot (which has ClickUp API access) to sync. In this Devika session I do not have ClickUp MCP tools loaded, so I cannot directly edit ticket `86d32w30g` from here — the bridge syncs the description from this spec file on next pulse, or Raj/Arjun applies it manually when the platform-team charter is greenlit.
