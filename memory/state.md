# Org State

product_name: SIGNAL
phase: Stage 3 — Design (Mia dispatched, full-scale clickable mockups)
last_updated: 2026-05-21

## Stages

stage_1_discovery:    done           audit: -
stage_2_options_spec: done           audit: PASS-WITH-NOTES (signal-spm-vision-audit.md, 2026-05-21)
stage_3_design_arch:  in_progress    audit: -    (Mia running — 3 clickable HTML variants, ETA 2026-05-25 to 2026-05-27)
stage_4_build:        not_started    audit: -
stage_5_qa_review:    not_started    audit: -
stage_6_gtm_launch:   not_started    audit: -

## Current focus
Discovery in parallel: spm (3 product cuts + PRD skeleton) and innovator (pressure-test strategist thesis vs. "better Postiz"). Mia (frontend) queued behind Sarah for scale-stress mockups.

## 14-day demo target
*Shifted.* Design phase (full-scale Vision) ~7–10 days → dev kickoff w/ Neha+Raj to slice V0.1 → 14-day build clock on the slice. Real demo ~2026-06-11 to 2026-06-18. Founder acked the slip 2026-05-21.

## Blockers
None — Sarah re-briefed to convert PRD → Product Vision doc (full-scale, 11 features).

## Recent decisions (most recent first)
- 2026-05-21 — *Vision audit: PASS-WITH-NOTES.* All 11 features deeply spec'd, personas concrete, RBAC matrix clean, sample Anita/Grassroot packet ready to design from. Notes: (a) AI Visuals labeled Phase 2 candidate, confirm at dev kickoff; (b) channels = design all 4 (FB/LI/IG/Threads), V0.1 build slice = FB+LI; (c) Notion/Slides import added to intake per founder G3 partial; (d) LinkedIn Partner Program risk → Founder decides at dev kickoff (native vs manual fallback). Grill Me deferrals logged as HIGH but non-blocking per founder.
- 2026-05-21 — *Mia dispatched* — 3 full-scale clickable HTML mockup variants (v1-cockpit / v2-canvas / v3-inbox). Covers all 11 features incl. Notion/Slides import. ETA 2026-05-25 to 2026-05-27.
- 2026-05-21 — *Devika takes the reins.* Founder elected to defer Grill Me G1/G2/G3 on Vision to prototype review. Devika makes all calls between now and clickable prototype. Founder pings = status snapshots (no timer-based heartbeats; Devika is not a persistent process).
- 2026-05-21 — *Vision reframe.* PRD → *Product Vision doc* (full-scale, no V0.1 budget thinking). Design and product get a free hand. Cost/cut decisions deferred to dev kickoff with Neha (GTM) + Raj (backend) in ClickUp. Demo rhythm shifts: design ~7–10 days → dev kickoff → V0.1 slice picked → 14-day build clock starts on the slice. Real demo ~3 weeks out (mid-June), not 2026-06-04.
- 2026-05-21 — *Full-scale Vision (11 features locked for design):* (1) Guided intake 6Q+PDF+free-text, (2) multi-channel gen (FB/LI/IG/+), (3) AI-generated visuals, (4) Monday packet email, (5) web review platform (Accept/Draft/Delete/Edit, per-post + bulk), (6) native scheduling+publishing (no Buffer/Later — disruption stance), (7) multi-brand dashboard, (8) RBAC: Admin/Reviewer/Editor (agency + client review seats), (9) live performance loop into next week's strategy, (10) comments/inbox surface w/ agent-drafted replies, (11) auto-drafted monthly client report.
- 2026-05-21 — *Grill Me debt logged.* Founder declined G1/G2/G3 on original PRD v1. Will re-grill on Vision doc before Mia briefs — non-optional, 2 weeks of design work downstream.
- 2026-05-21 — Framing locked: SIGNAL = *unlock dormant FB/LinkedIn for agencies*, not replace IG. Anita Dongre brand as demo target through CEO B.
- 2026-05-21 — Founder picked *(a) Guided intake* for brand-kit: 6 structured questions (voice, audience, taboo topics, 3 example posts they love, 3 they hate, KPIs) + PDF upload + free-text. Forces signal in; answers double as eval fixtures later. ~1 extra day frontend in V0.1.
- 2026-05-21 — Founder picked *CEO B's agency* as the V0.1 design partner. DRI for relationship: Founder.
- 2026-05-21 — Brand-kit ingestion for V0.1 = *PDF upload + free-text context setting* (founder/agency pastes brand voice, do/don'ts, audience). Output: per-brand agent system prompt. No Notion/Drive integration in V0.1.
- 2026-05-21 — Founder picked Alex's V0.1 unit-of-work: *client-week packet* (calendar + per-post rationale + monthly client report) over Sarah's "5 drafts/channel". Reason: justifies the $300 price; drafts alone don't. DRI to write PRD: Sarah.
- 2026-05-21 — Sarah (spm) picked Approach A (Strategist-First). File: decisions/signal-spm-options.md.
- 2026-05-21 — Alex (innovator) verdict: PIVOT THE WEDGE. Reframe V0.1 unit from "drafts" to "client-week packet (calendar + rationale + monthly client report)". Cut Phase 1 from 14 platforms / 4 mo → 3 platforms / 6 wk on Postiz fork. File: decisions/signal-innovator-pressure-test.md.
- 2026-05-21 — Locked design-for-scale / build-for-small discipline. Mockups handle 50 brands × 20 accounts; code ships 1 brand × 2 channels for V0.1.
- 2026-05-21 — V0.1 = FB + LinkedIn, 1 brand, 1 approval loop. Phase 1 = full 14-platform scheduler (months 1–4 post-demo). Phase 2 (image gen, edit studio, influencer) firewalled until 30 paid agencies.
- 2026-05-21 — Price re-anchored from $599 (aspirational in GTM brief) to $300 (real conditional yes from 3 CEOs). Win metric: 30 agencies × $300 = $9K MRR by EOY 2026.
- 2026-05-21 — Pitch locked: "Per-brand AI strategist + scheduler for marketing agencies. Drafts the week, you approve in one tap. $300/agency."

## Platform Team (org infra — separate from SIGNAL product track)

**Status:** Shipped 2026-05-21 by Raj. Handed off to Arjun.
**DRI going forward:** Arjun (platform)

### Files shipped in this PR
| File | Lines | Status |
|---|---|---|
| `org_bridge/main.py` | +63 lines | heartbeat_loop, ACTIVE_AGENTS, LAST_ARTIFACT, pulse wiring |
| `org_bridge/agents.py` | +70 lines | platform agent registered, write_agent_status, record_artifact helpers |
| `org_bridge/pulse.py` | 164 lines (new) | 10-min transparency ticker, format_pulse, stall detection |
| `org_bridge/slack-manifest.yaml` | +7 lines | #org-pulse and #org-arjun-platform documented |
| `.claude/agents/platform.md` | 95 lines (new) | Arjun persona |
| `decisions/platform-team-charter.md` | 91 lines (new) | Boundary + handoff protocol |

### Verified (locally)
- `python -c "import agents; import pulse"` — exit 0
- `SLACK_BOT_TOKEN=xoxb-fake python -c "import main; import pulse; import agents"` — exit 0
- Pulse formatter dry-run with 3-agent fake status (chief active 15m, platform stalled 75m, backend idle) — output matches spec format. Stall detection fired correctly at 75m > 30m threshold.

### NOT verified (requires live bridge)
- Heartbeat posts to #org-warroom — needs bridge restart
- Pulse posts to #org-pulse — needs bridge restart + #org-pulse channel to exist
- Platform agent routes to #org-arjun-platform — needs Slack manifest reapply + restart

### Restart checklist for founder
1. In Slack app config (api.slack.com) → Your app → Incoming webhooks / App Manifest → paste updated `org_bridge/slack-manifest.yaml` content → Save. (This documents the new channels; the bot creates them programmatically via slack_setup.py on startup.)
2. `cd /home/manojbojja/git/ai/yamer/org_bridge && source .venv/bin/activate && python main.py`
3. Confirm in Slack: new channels `#org-pulse` and `#org-arjun-platform` appear.
4. Wait 10 minutes for first pulse post to `#org-pulse`.
5. Wait 5 minutes for first heartbeat post to `#org-warroom`.
6. To verify stall detection: start an agent run that takes >30 min; the next pulse tick will flag it `⚠ stalled`.

### Env vars added (optional — defaults are sane)
- `HEARTBEAT_ENABLED=false` — disable heartbeat
- `HEARTBEAT_INTERVAL_SECONDS=300` — heartbeat cadence (default 5 min)
- `PULSE_INTERVAL_SECONDS=600` — pulse cadence (default 10 min)
- `STALL_THRESHOLD_SECONDS=1800` — stall detection threshold (default 30 min)
- `QUIET_TICKS_THRESHOLD=3` — consecutive idle ticks before quiet post (default 3)

## Open questions for the founder
- (none — both Mia/Sarah inputs answered 2026-05-21)
