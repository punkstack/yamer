# PRD: SIGNAL V0.1
Date: 2026-05-21
Approach picked: A (Strategist-First) — unit of work locked as client-week packet per founder's call 2026-05-21
Author: spm

---

## Pitch

SIGNAL turns one client's week into a ready-to-resell deliverable — calendar, rationale, and report — for $300/mo.

*(15 words)*

---

## Problem

I run a boutique marketing agency with 10–15 client brands. My junior strategist costs $4K/mo, burns out every 14 months, and produces monthly client reports by manually copying numbers into a Google Doc for 2–3 hours per client. When she quits, the voice knowledge for each brand leaves with her. Buffer schedules. ChatGPT drafts. Neither produces the thing I actually sell the client: a strategic deliverable that shows I'm thinking about their brand, not just posting at it. I'd pay $300/mo for a tool that produces that deliverable — but only if it sounds like the client and not like a ChatGPT template.

---

## Who

**Primary user:** Owner-operator CEO of a Bangalore or SEA boutique marketing agency running 3–15 client brands on retainer. Staff of 3–8. Billing each client $1,500–2,500/mo. Personally reviews every piece of content before it goes to the client.

**Current alternative:** Junior strategist ($3–6K/mo) + Buffer/Hootsuite ($50–200/mo) + ChatGPT (ad-hoc) + 2–3 hrs/client/month of manual reporting. Three disconnected tools, no institutional memory, high attrition risk.

**Receipts from 3 CEO conversations:**

> "I'd pay $300/mo if you handle scheduling across the famous 14 platforms + AI marketing plans + brand cycles + historical analysis + analytics."
> — verbatim conditional yes, all 3 CEOs (captured in `.claude/project-config.md`)

Alex's pressure test surfaced the reframe: these CEOs are not buying drafts — they are buying a resellable deliverable. Agencies bill clients $1,500–2,500/mo. The monthly report is the proof-of-value artifact they write to justify that fee. SIGNAL producing the report draft is what makes the $300 vs. $65 (Blaze AI) gap defensible.

---

## Evidence

- [ReportsMate 2026](https://www.reportsmate.com/blog/how-to-automate-client-reporting-for-marketing-agencies-in-2026) — agencies spend 2–3 hrs/client on monthly reports at $100–150/hr billable; 20 clients = 40–60 hrs/month of reporting labor, more than one FTE. SIGNAL's report draft removes that labor cost.
- [Blaze AI Review — SaaSGenius 2026](https://www.saasgenius.com/reviews/blaze-ai/) — Blaze autopilot at $46–65/mo already drafts a week of posts. Differentiation at $300 requires a resellable deliverable, not just better post drafts.
- [Search Engine Land — AI squeezing agencies 2025](https://searchengineland.com/ai-squeezing-marketing-agencies-472189) — 66% of agency owners worry about talent pipeline; junior strategist attrition is stated pain, not a hypothesis.
- [Postiz Review 2026 — LifetimeDealTech](https://lifetimedealtech.com/postiz-review-2026/) — Postiz is open-source, MIT-licensed, agentic-ready. Phase 1 scheduler is a Postiz fork. Do not build from scratch.

---

## The Client-Week Packet — Exact Spec

The unit of work is a **client-week packet**, not a set of post drafts. One packet per brand per week. Delivered Monday morning.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLIENT-WEEK PACKET
[Brand Name] — Week of [Mon Date]
Delivered to: [Agency CEO name] via email
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTION 1 — STRATEGIC HEADER
Weekly theme: [1 sentence — what narrative thread ties this week]
Why this week: [2–3 sentences — connects to brand cycle, seasonal
               context, or last week's performance signal if available]
Watch for: [1 sentence — what to flag proactively to the client]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — WEEKLY CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONDAY
  FACEBOOK
  [Post copy — max 280 chars, no more than 2 hashtags]
  Rationale: [1 sentence answering: why this topic / why today / why this hook]

  LINKEDIN
  [Post copy — max 600 chars, professional framing, max 3 hashtags]
  Rationale: [1 sentence answering: why this topic / why today / why this hook]

TUESDAY ... FRIDAY [same structure]

Note: Saturday and Sunday omitted unless brand kit specifies weekend cadence.

Low-confidence posts (where rationale cannot be justified by brand kit
or sample posts) are flagged inline:
  ⚠ LOW CONFIDENCE — [reason]. Recommend human review before approving.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — MONTHLY REPORT DRAFT SKELETON
(week-4 packet only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Brand Name] — Monthly Performance Summary — [Month Year]
Draft prepared by SIGNAL. Agency to review, add real metrics, rebrand, and send.

WHAT WE POSTED
[3–4 sentences summarizing the month's content themes and why]

WHAT PERFORMED
- [Top post 1 — describe, note engagement signal — placeholder in V0.1]
- [Top post 2]
- [Top post 3]

WHAT WE LEARNED
[2–3 sentences — voice observation or platform insight from the month]

NEXT MONTH RECOMMENDATION
[2–3 sentences — what SIGNAL proposes to shift in strategy and why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — APPROVAL ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply "APPROVED" to approve all posts.
Reply with the post day + platform + your note to request an edit.
Reply "REJECT" + reason to reject the full week (treated as brand kit gap).
```

**Per-post rationale rule:** Each rationale sentence answers exactly one of: (a) why this topic — connects to a brand kit pillar or a performance signal; (b) why today — audience timing, campaign cycle, or contextual hook; (c) why this hook — format choice relative to brand voice. One sentence. No padding. If the agent cannot answer, it flags the post as LOW CONFIDENCE.

**Monthly report rule:** It is not a polished client-ready document. It is a structured skeleton the agency PM edits in 30 minutes and sends under their own letterhead. V0.1 uses placeholder performance language (no real analytics yet). Real data is Phase 1.

---

## The One Demo Moment

**The agency CEO reads the week-1 packet for their client brand and says: "I would show this to my client tomorrow."**

Not "this is pretty good for AI." Not "interesting." That specific sentence. It signals simultaneously that the voice is close enough the CEO trusts it, and that the format is client-presentable. Everything in the 14-day build is subordinated to landing that one moment.

Secondary signal: CEO says "this sounds like them" when reading the Monday post aloud without prompting.

---

## MVP (ship by 2026-06-04)

**Must-have — 6 actions the user does:**

1. **Founder pastes the brand kit** (text or Google Doc URL) + 20–30 sample posts from the demo brand's FB and LinkedIn into a minimal setup interface (CLI script or bare intake form — whichever ships faster). Agent extracts: brand name, tone descriptors, messaging pillars, audience definition, off-limits topics.

2. **SIGNAL generates the full client-week packet** — 5 posts × 2 channels + per-post rationale + strategic header — zero manual intervention after brand kit ingestion.

3. **Agency CEO receives the packet** via formatted plain-text email with the approval action block (approve-all / request-edit per post / reject week).

4. **Agency CEO approves the week** by replying "APPROVED." System logs timestamp + confirmation to a local file. No database.

5. **Agency CEO requests an edit** by replying with post day + platform + note. Founder reads the reply and adjusts manually for V0.1. No automated edit processing — the loop exists for the demo, automation is Phase 1.

6. **SIGNAL appends the monthly report draft skeleton** to the week-4 packet. CEO receives it alongside the week's calendar. No real analytics — placeholder language explicitly labeled as such.

**Explicit cuts:**

- No scheduler. No posting to any platform. No OAuth. No API connections. Zero.
- No Slack bot. Email only. Slack OAuth is 2–3 days that do not improve the demo.
- No dashboard or web UI. A minimal intake page or CLI is sufficient.
- No multi-brand. One brand, one agency, hardcoded to the design partner.
- No analytics. Monthly report draft uses placeholder performance language.
- No automated edit processing. CEO's edit requests are handled manually by founder.
- No historical post API pull. Manual paste of 20–30 sample posts.
- No image generation, no edit studio, no influencer layer. Phase 2. Firewalled.
- No client portal. Agency CEO is the only approver in V0.1.
- No CSV import/export.

**Later (Phase 1, months 1–4 post-demo):**

- Postiz fork for FB + LinkedIn + Instagram scheduling (3 platforms first, not 14)
- Structured brand kit editor UI
- Automated edit processing in-product
- Slack bot delivery
- Historical performance API pull + analytics
- Multi-brand support
- Real monthly report with actual engagement data
- Approval workflow in-product (not email-reply)

---

## Success Metric

**One metric. One target. One deadline.**

At least 1 of the 3 conditional-yes CEOs says both sentences in the demo session by 2026-06-04:
- "This sounds like them."
- "I would show this to my client tomorrow."

And commits in writing (email or Slack) before the call ends to stay in the design-partner program through Phase 1.

Target: 1 of 3. Stretch: 2 of 3. If 0 of 3, demo is a fail.

---

## Kill Criteria (day 60 = 2026-07-21)

By 2026-07-21, if any of the following is false, SIGNAL stops or pivots to selling directly to brands:

1. At least 2 of 3 conditional-yes CEOs respond stronger to "produces the client deliverable" framing than to "drafts the week" framing — confirmed by founder's reframe calls by 2026-05-28. DRI: founder.
2. At least 1 CEO says "I would show this to my client" at the V0.1 demo by 2026-06-04. DRI: founder.
3. At least 2 peer CEOs outside the founder's network (cold referrals) validate the $300 price on the reframed pitch by 2026-06-20. Kills the selection-bias risk on 3 CEOs from one network. DRI: founder. [Source: Alex's 30-day kill criteria — `decisions/signal-innovator-pressure-test.md`]

Miss any one → replan. No "let me think about it."

---

## Top 3 Risks

1. **Brand voice quality fails the demo.** Posts sound generic; rationale feels templated; CEO says "it's close but not quite." This is the single highest-risk item — a bad draft demo is worse than a late demo. Mitigation: founder tests the draft chain against at least 3 real historical posts from the demo brand internally before the CEO sees anything. If the internal test fails, reschedule. Do not show a bad packet. DRI: founder.

2. **Brand kit material is not in hand by day 3 (2026-05-24).** Without the demo brand's kit and sample posts, there is no time to validate draft quality before 2026-06-04. Every day of delay in kit receipt compresses the test window. Mitigation: founder asks the design-partner agency CEO today — names the brand, asks for a rough brief and a post export by Friday. DRI: founder.

3. **Solo dev bandwidth overrun kills the deadline.** The 14-day window with a Uber day job is the primary execution constraint, not technical difficulty. Any scope addition outside the 6 must-haves above moves the deadline, and a missed deadline is a kill criterion. Mitigation: the CoS enforces the cut list. Every "what if we also..." goes to a parking lot document, not the sprint. DRI: founder (scope discipline) + CoS (enforcement).

---

## Open Questions for the Founder

**Q1 — Which agency and which client brand is the V0.1 design partner?**
Need brand kit material and 20–30 sample posts by 2026-05-24 (day 3 of the 14-day window). If not resolved today, the 2026-06-04 demo is at risk. Answer before end of day 2026-05-21. DRI: founder.

**Q2 — Brand kit ingestion format for the demo brand.**
Text doc, Google Doc URL, PDF, or "in someone's head"? V0.1 accepts text paste or Google Doc URL. If it is a PDF or verbal, the ingestion session changes: schedule a structured 60-minute call with the agency PM, run the intake live. Do not build a file parser. Answer by 2026-05-22. DRI: founder.

**Q3 — Email or Slack for V0.1 packet delivery?**
Email ships in 4 hours. Slack bot requires OAuth setup (2–3 days). Position: email is the correct call unless the design-partner CEO explicitly expects a Slack bot and has a workspace ready to add a bot to today. Decide by 2026-05-22 — this gates Raj's build scope. DRI: founder.

---

## DRI Table — Next Steps

| Who | What | By when |
|-----|------|---------|
| Founder | Name the V0.1 design-partner agency and client brand | 2026-05-21 EOD |
| Founder | Call all 3 CEOs with "client deliverable" reframe; confirm which framing excites them | 2026-05-28 |
| Founder | Confirm email vs. Slack delivery + confirm Claude on Max plan as the LLM | 2026-05-22 |
| Founder | Get brand kit + 20–30 sample posts from design-partner agency | 2026-05-24 |
| Mia (staff-frontend) | 3 HTML mockups of the client-week packet email + approval UX — design for scale (50 brands × 20 accounts), V0.1 shows 1 brand | After Q1 answered |
| Raj (staff-backend) | 3 arch options for V0.1 backend: brand ingestion → LLM draft chain → email delivery → approval log | After Q2 + Q3 answered |
| CoS | Run Grill Me on this PRD with founder; dispatch auditor | 2026-05-21 |
