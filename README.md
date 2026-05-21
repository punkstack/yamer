# Your AI Org — v3 (Slack + ClickUp)

A real product org running in your Slack workspace.

- **9 agents** with names and personas: Devika (Chief of Staff), Sarah (SPM), Priya (PM), Raj (Backend), Mia (Frontend), Karthik (DevOps), Alex (Innovator), Neha (GTM), Vikram (QA), plus the Auditor.
- **Each agent has its own Slack channel** — drop into `#org-raj-backend` to talk to Raj, `#org-mia-frontend` to talk to Mia. Messages render as that persona, not as a generic bot.
- **War room** at `#org-warroom` — agents drop status here. You watch the org work.
- **DM the bot** to talk to Devika (Chief of Staff). She orchestrates.
- **ClickUp** is the tracker. Every meaningful task lands there with the right DRI tag.
- **Runs locally on your laptop.** Socket Mode means no public URL, no ngrok, no deployment. Just `python main.py`.
- **Claude Max subscription billing** by default. Switches to API only if you tell it to.

---

## Step-by-step setup

### Phase 1 — Slack app (10 min)

**1.** Go to **https://api.slack.com/apps** → click **Create New App** → **From a manifest**.

**2.** Pick your workspace.

**3.** Paste the entire contents of `org_bridge/slack-manifest.yaml`. Review. Click **Create**.

**4.** Once created:
- Sidebar → **Install App** → **Install to <workspace>** → Allow.
- Sidebar → **OAuth & Permissions** → copy the **Bot User OAuth Token** (`xoxb-...`). Save it.
- Sidebar → **Basic Information** → scroll to **App-Level Tokens** → **Generate Token and Scopes** → name it `socket`, add scope `connections:write`, generate. Copy the token (`xapp-...`). Save it.

**5.** Find your Slack IDs:
- Open Slack in browser. Click your name top-left → look at the URL. The `T...` is your **team ID**.
- Click your own avatar → **Profile** → click `⋯` → **Copy member ID**. That's your **founder user ID** (`U...`).

### Phase 2 — ClickUp setup (5 min)

**1.** Open ClickUp → **Settings** → **Apps** → **API** → **Generate** → copy the personal token (`pk_...`).

**2.** Create a Space called `Org`, a List called `Build`.

**3.** On that list, add:
- Statuses: `Backlog → Spec → Building → Review → Done`
- Tags: `spm` `pm` `backend` `frontend` `devops` `innovator` `gtm` `qa` `auditor`

**4.** Get the list ID:
```bash
# Use your pk_... token
curl -H "Authorization: pk_YOUR_TOKEN" https://api.clickup.com/api/v2/team
# Find your team_id in the response. Then:
curl -H "Authorization: pk_YOUR_TOKEN" \
  https://api.clickup.com/api/v2/team/YOUR_TEAM_ID/space?archived=false
# Find the "Org" space_id. Then:
curl -H "Authorization: pk_YOUR_TOKEN" \
  https://api.clickup.com/api/v2/space/YOUR_SPACE_ID/list?archived=false
# Find the "Build" list_id. That single value goes into CLICKUP_LIST_ID.
```

### Phase 3 — Local install (5 min)

**1.** Make sure prerequisites are in place:
```bash
node -v               # 18+ for Claude Code
python3 --version     # 3.11+ for the bridge
git --version
```

**2.** Confirm Claude Code is installed and on subscription:
```bash
npm install -g @anthropic-ai/claude-code
unset ANTHROPIC_API_KEY      # critical — empty means Max billing
claude --version
```

**3.** Drop the org folder in:
```bash
unzip ~/Downloads/my-org-v3.zip -d ~/projects/
cd ~/projects/my-org-v3
chmod +x scripts/worktree.sh
git init && git add . && git commit -m "v3 setup"
```

**4.** Install Python deps for the bridge:
```bash
cd org_bridge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**5.** Configure environment:
```bash
cp .env.example .env
# Open .env in your editor and fill in:
#   SLACK_BOT_TOKEN, SLACK_APP_TOKEN
#   CLICKUP_API_KEY, CLICKUP_LIST_ID
# Leave ANTHROPIC_API_KEY blank (Max subscription)
# Leave CLAUDE_RUNTIME=code
# CHAT_HISTORY_TURNS=6 is a good default (raise for stickier context, lower for less token use)
```

### Phase 4 — First launch

**1.** Start the bridge:
```bash
# from org_bridge/ with venv active
python main.py
```

You'll see:
```
[INFO] org-bridge: Connected as bot Org in workspace <name>
[INFO] org-bridge: Setting up channels...
  + #org-chief (created)
  + #org-sarah-spm (created)
  + #org-priya-pm (created)
  + #org-raj-backend (created)
  + #org-mia-frontend (created)
  + #org-karthik-devops (created)
  + #org-alex-innovator (created)
  + #org-neha-gtm (created)
  + #org-vikram-qa (created)
  + #org-auditor (created)
  + #org-warroom (created)
[INFO] org-bridge: Ready. 11 channels live.
[INFO] org-bridge: Org Bridge is online. Talk to Devika in #org-chief.
```

**2.** Open Slack. You'll see the new channels in your sidebar. `#org-warroom` will have a kickoff message.

**3.** Go to `#org-chief` and type:
```
hi
```

Devika sees `.claude/project-config.md` is unfilled and opens THE GRILL:

> *"I'm not going to walk you through a form. I'm going to ask you what every senior here would ask in your first 30 minutes. Vague answers get pushed back. Ready?"*

**4.** Answer the 9 grill questions, one at a time. Devika pushes back when you hedge.

**5.** After lockdown, Devika asks: *"innovator first, or jump straight to spm?"* Pick.

---

## Daily flow

Once setup is done, this is your day:

- **Open Slack.** That's it. The bridge runs in the background on your laptop.
- **DM Devika** for orchestration, decisions, status. Or post in `#org-chief`.
- **Drop into specialist channels** to talk directly to that agent — `#org-sarah-spm` to scope, `#org-raj-backend` to debate architecture, `#org-mia-frontend` to ask about a UI choice.
- **Watch `#org-warroom`** for status drops as agents finish work.
- **Check ClickUp** for the kanban view of who's working on what.

### Example session

```
You (DM Devika):       Let's start scoping the invoice chaser.
Devika:                On it. Sending Sarah.
[#org-warroom]         Devika → Sarah: scope invoice-chaser. ETA 8 min.
[#org-sarah-spm]       Sarah: Three approaches incoming. Reading the config...
[#org-sarah-spm]       Sarah: Here are the three options... (posts options doc link)
Devika (DM):           Sarah's back with 3 options. Want to grill her on B before locking?
You:                   Yeah, why didn't she consider mobile-first for option C?
Devika:                Good catch. Sending you both to #org-sarah-spm for that.
```

---

## Folder layout

```
my-org-v3/
├── README.md                          ← this file
├── CLAUDE.md                          ← Devika's brain (Chief of Staff)
├── .claude/
│   ├── project-config.md              ← filled via THE GRILL
│   └── agents/                        ← one .md per agent
│       ├── spm.md          (Sarah)
│       ├── pm.md           (Priya)   ← NEW in v3
│       ├── staff-backend.md (Raj)
│       ├── staff-frontend.md (Mia)
│       ├── devops.md       (Karthik) ← NEW in v3
│       ├── innovator.md    (Alex)
│       ├── gtm.md          (Neha)
│       ├── qa.md           (Vikram)
│       └── auditor.md      (The Auditor)
├── org_bridge/                        ← NEW in v3 — the Slack service
│   ├── main.py                        ← Slack Bolt app
│   ├── agents.py                      ← agent registry + Slack personas
│   ├── claude_loop.py                 ← runs each agent (claude -p)
│   ├── clickup.py                     ← ClickUp REST helper
│   ├── slack_setup.py                 ← auto-creates channels on first run
│   ├── slack-manifest.yaml            ← paste at api.slack.com to create the app
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                           ← (you create this — gitignored)
├── scripts/worktree.sh                ← parallel agent dev helper
├── decisions/                         ← every deliverable lands here (commit to git)
├── mockups/                           ← Mia's 3 HTML files
└── memory/state.md                    ← pipeline dashboard source of truth
```

---

## Two ways to run an agent

### Way 1 — Slack (recommended day-to-day)
The bridge is running. You DM Devika. She delegates. Specialists work in their channels. ClickUp updates automatically.

### Way 2 — Local CLI (when you want focused work without Slack noise)
```bash
cd ~/projects/my-org-v3
claude
```
Same `.claude/agents/` files, same `CLAUDE.md`, same decisions folder. The two modes share the same state via the filesystem — Slack and CLI sessions can interleave.

When to use CLI:
- You want to iterate fast on one agent without Slack overhead
- Deep work on `staff-backend` or `staff-frontend` where streaming code into Slack is awkward
- You're offline or your bridge crashed

When to use Slack:
- Strategic / orchestration moves through Devika
- You want the org running in the background while you do other work
- You want async — drop a message, come back when the agent finishes

---

## House rules (the org's culture, enforced everywhere)

1. **Be specific or be silent.** "Users" is not an answer.
2. **Show me the data.** Every claim cites a source or number.
3. **One DRI per decision.** One human or one agent owns it.
4. **Bias to action.** B+ today beats A+ next week.
5. **Disagree and commit.** Once decided, don't reopen without new data.
6. **Demo or kill in 14 days.** Every track has a 14-day target.
7. **No "we'll figure that out later."**
8. **Strong opinions, weakly held.**
9. **Bird's-eye and worm's-eye.** Every update has both.

---

## Troubleshooting

**The bridge starts but Devika doesn't respond in Slack.**
- Check `unset ANTHROPIC_API_KEY` is in effect for the shell running `python main.py`.
- Run `claude /status` separately to confirm subscription billing.
- Tail the bridge logs — agent invocation errors print there.

**Slack says "channel name taken" on startup.**
- Harmless if the channel already exists. The bridge re-uses it.

**ClickUp tasks aren't appearing.**
- Verify `CLICKUP_LIST_ID` is the list ID, not the space or folder ID.
- Test with: `curl -H "Authorization: $CLICKUP_API_KEY" https://api.clickup.com/api/v2/list/$CLICKUP_LIST_ID`

**An agent's reply is empty or has a runtime error tag.**
- Check the agent's `.md` file in `.claude/agents/` exists and is well-formed.
- Run the same agent locally via `claude` and the `/agents` menu to debug in isolation.

**Slack rate limits.**
- Bot sends max ~1 message/sec per channel by default. The bridge respects this. Heavy parallel agent runs may queue briefly.

**Bridge crashed mid-session.**
- Just `python main.py` again. State lives in files (`decisions/`, `memory/`, ClickUp). Nothing in memory is lost.

---

## Cost & rate limits

- **Claude Max 20x ($200/mo)** is the right tier for this fleet. Max 5x will throttle on parallel agent runs.
- **Heavy sessions in the morning IST.** Peak hours (5:30–11:30 PM IST) burn quota ~2x.
- **Watch the Agent SDK credit bucket after June 15, 2026.** `claude -p` (which the bridge uses) draws from a separate monthly credit on subscription plans starting that date.
- **ClickUp + Slack** are both on free tiers for typical usage. Slack free tier limits message history but doesn't limit bot usage.

---

## Known limitations (and what to do about them)

**Chat memory is per-channel, last 6 exchanges.** The bridge keeps a rolling buffer per channel and replays it to the agent every turn. This is what makes the grill work across 9 questions. The buffer lives in process memory — if the bridge restarts mid-conversation, history for that channel resets. Persist by referencing decisions/ files (which agents always read) for anything important.

**Each agent invocation is a fresh process.** `claude -p` runs once per Slack message — the chat buffer above re-injects context, but the agent isn't running a long-lived loop. That keeps token cost low and crash-resilient, but it means agents won't notice file changes mid-turn or hold open connections.

**Slack rate limit per channel is ~1 msg/sec.** The bridge auto-splits long replies but doesn't queue across parallel invocations. If you ping three agents simultaneously, posts may briefly stagger.

**The Auditor has a channel but is gated.** `#org-auditor` exists for transparency — you can read past audits there — but the Auditor agent doesn't take direct instruction from the founder. It's invoked by Devika after stage deliverables, by design.

**ClickUp tasks land via the agent, not the bridge.** When an agent uses its `mcp__clickup` tool inside the `claude -p` runtime, you'll need ClickUp connected as an MCP server in Claude Code (`claude /mcp add ...`) the first time. The personal API key in `.env` is for the bridge's own helpers if you extend `clickup.py` directly.

## When to add more

These are deliberately NOT in v3. Add only when you hit the specific pain:

- **Designer agent** separate from frontend (when you start shipping real designs)
- **Data agent** for analytics, dashboards (when you have users and need to read behavior)
- **Hooks** — deterministic pre-commit / pre-push scripts (when an agent commits a secret)
- **GitHub MCP** alongside ClickUp (when agents need to open PRs)
- **Figma MCP** (when designs come from Figma, not mockups)

Don't add speculatively. The current 9 agents cover MVP through launch.
