# Platform Team Charter
Date: 2026-05-21
Author: Raj (staff-backend)
DRI: Arjun (platform)
Ticket: 86d32w30g (sub-scope C)

---

## Purpose

The Platform Team owns the virtual org's infrastructure — the bridge, the agent substrate,
the observability layer, and the tooling that makes every other team's work visible and
reliable. This is explicitly NOT product-feature work. It is the plumbing that the product
teams depend on.

One DRI: Arjun. No co-ownership with Raj. Raj hands off this ticket's work at merge and
Arjun carries it forward.

---

## Arjun's scope boundary

Arjun owns everything in this list. Raj does not touch these files without a Slack
handoff message from Arjun first.

### Files Arjun owns
| File / Path | Ownership reason |
|---|---|
| `org_bridge/main.py` | Bridge entry point, startup, heartbeat_loop, ACTIVE_AGENTS, LAST_ARTIFACT |
| `org_bridge/agents.py` | Agent registry — adding/removing agents, status-update helpers |
| `org_bridge/claude_loop.py` | Claude runtime dispatch |
| `org_bridge/publisher.py` | Artifact publish pipeline |
| `org_bridge/pulse.py` | 10-min transparency ticker (new, this PR) |
| `org_bridge/slack_setup.py` | Channel provisioning |
| `org_bridge/slack-manifest.yaml` | Slack app manifest |
| `org_bridge/requirements.txt` | Bridge dependencies |
| `org_bridge/.env` | Bridge secrets (never committed) |
| `memory/agent-status.json` | Runtime agent state (written by bridge, read by pulse) |
| `.claude/agents/platform.md` | Arjun's own persona file |

### Files Raj owns (product-backend)
| File / Path | Ownership reason |
|---|---|
| `code/` (any product code) | Product feature implementation |
| `.claude/agents/staff-backend.md` | Raj's persona file |
| `decisions/*-arch*.md` | Architecture decisions for product features |
| `decisions/*-build*.md` | Build reports for product features |
| `decisions/*-tasks*.md` | Task lists for product features |

### Shared read-only (either can read, neither owns alone)
- `decisions/*.md` — decision artifacts written by the agent that ran the session
- `memory/state.md` — org-wide state; Chief of Staff (Devika) is DRI for updates

---

## Handoff protocol

When Raj produces code that lands in Arjun's file-ownership boundary
(e.g., this heartbeat + pulse PR), the handoff is:

1. Raj opens a PR, writes a one-paragraph summary in `#org-warroom`:
   "Handing off heartbeat + pulse to Arjun. Files touched: [list]. Verified: [what].
   Not verified: [what]. Needs bridge restart to confirm live Slack behavior."
2. Arjun reviews. If no concerns within one session, Arjun is DRI going forward.
3. For future bugs or changes to those files: Arjun files the ticket, Arjun writes the
   fix plan, Arjun ships the code. Raj is available for consult, not for DRI.

For urgent production issues (bridge is down): either can patch. First one in writes
a post-incident note to `decisions/incident-<date>.md` within 24h.

---

## What Arjun is NOT responsible for

- Product feature backends (invoice-chaser, signal, etc.) — Raj
- Frontend code — Mia
- CI/CD pipelines, Docker, deploy infrastructure — Karthik (devops)
- Decision audits — The Auditor
- Sprint planning — Priya (pm)

---

## Platform Team backlog (first sprint, inherited from this ticket)

1. Heartbeat coroutine + ACTIVE_AGENTS tracking (shipped in this PR by Raj, handed off)
2. Pulse ticker — `org_bridge/pulse.py`, 10-min cadence, `memory/agent-status.json` source
3. `#org-pulse` + `#org-arjun-platform` channels (manifest + channel setup)
4. ClickUp lifecycle (Gap 2) — separate ticket
5. Slack thread closure marker (Gap 3) — separate ticket
6. Manifest schema enrichment with `agent` + `triggered_by` fields (Gap 4) — separate ticket

---

## Scaling ceiling and blast radius

The bridge is a single Python asyncio process. Blast radius if it goes down: all Slack
agent routing stops. No data loss (decisions/ is git-backed). Recovery: restart the
process. Arjun's job is to keep MTTR under 2 minutes via clean error handling + restart
instructions in `memory/state.md`.

Current ceiling: single-threaded asyncio handles the founder's usage pattern comfortably
(one concurrent agent run at a time, 5–20 messages/hour). No scaling work needed at MVP.
