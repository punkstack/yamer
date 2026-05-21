# PRD: SIGNAL V0.1
Date: 2026-05-21
Approach picked: A — Strategist-First (with Alex's framing pivot applied)
Author: spm

---

## Problem

Agency CEO running 10–30 client brands. Junior strategist costs $4K/mo, doesn't retain brand voice across quarters, uses three disconnected tools (ChatGPT + Buffer + a spreadsheet), and produces a monthly client report that takes 2–3 hours per client to write. When the strategist quits, institutional knowledge walks out. The CEO conditionally committed to $300/mo for a tool that handles AI marketing plans, brand cycles, scheduling across 14 platforms, and historical analysis — but the immediate pain is simpler: nobody on the team produces strategy fast enough or consistently enough. The CEO needs to see that an AI agent can produce a client deliverable they'd actually send — not just a drafted post, but the rationale behind it.

---

## Who

Primary user: the agency CEO or senior account director at a mid-market marketing agency running 10–30 client brands, operating with 3–8 staff. Current alternative: junior strategist ($3–6K/mo) + Buffer/Hootsuite ($50–200/mo) + ChatGPT (ad-hoc) + manual reporting (2–3 hrs/client/month). Confirmed: 3 CEOs in founder's network have given a conditional yes at $300/mo.

---

## The Unit-of-Work Decision: Posts vs. Packets

Alex argued for packets. I previously leaned posts. After reviewing both cases, the call is: **packets**.

A post is a content deliverable. A packet is an agency deliverable. The difference matters for the demo moment and for the $300 price justification.

**A packet is:**
- The week's content calendar for a brand (5 posts × 2 channels = 10 posts with platform-native format)
- One-paragraph strategic rationale per post ("why this post, why this week, what it connects to in the brand's current cycle")
- A one-page draft of the monthly performance summary skeleton (what the agency will rebrand and send to the client)

**Why packets beat posts for V0.1:**
1. The demo moment changes from "look at these drafts" to "look at this thing you'd send to your client." That is a different emotional register. One triggers "nice writing." The other triggers "I could use this tomorrow."
2. The $300 price anchors to the monthly report labor, not to the posts. Agencies spend 2–3 hrs/client at $100–150/hr on reporting — that is $200–450 of billable labor per client per month. SIGNAL producing the report draft at $300/agency/month is a cost compression story the CEO can do arithmetic on.
3. The posts are inside the packet. Building posts-only is not cheaper — you are building the same draft chain. The packet adds a rationale wrapper and a report skeleton, both of which are LLM output, not new product surface.

**The explicit cut this makes:** V0.1 does not demo as a "scheduler with AI." It demos as a "strategist agent that produces the deliverable." The CEO should not be thinking about Buffer during the demo. They should be thinking about their junior strategist.

---

## Evidence

- [ReportsMate 2026](https://www.reportsmate.com/blog/how-to-automate-client-reporting-for-marketing-agencies-in-2026) — agencies spend 2–3 hours per client on monthly reports; 20 clients = 40–60 hours/month of reporting labor, more than one FTE
- [Blaze AI Review 2026 — WMappDigital](https://wmappdigital.com/blaze-ai-review/) — Blaze requires one workspace (one subscription) per client brand; at $65–79/mo per brand, managing 10 brands costs $650–790/mo with no cross-brand learning, no weekly packet, no client report output. SIGNAL's $300/agency is structurally cheaper and produces more.
- [Search Engine Land — AI squeezing agencies](https://searchengineland.com/ai-squeezing-marketing-agencies-472189) — 66% of agency owners worried about talent pipeline; junior strategist attrition is the stated pain
- [Blaze AI Pricing](https://www.blaze.ai/pricing) — $65/mo, no per-brand memory across an agency portfolio, no client report generation. Confirms the gap at $300 is justified if the strategist output quality and reporting land.

---

## MVP — Ship in 14 days (deadline 2026-06-04)

**Must-have:**

1. Brand kit ingestion — accepts text paste or Google Doc URL. Extracts: brand name, tone descriptors, messaging pillars, audience definition, off-limits topics. Stored as a structured JSON profile. No file parser, no PDF upload, no UI form yet — a script or a simple intake page is fine for the demo.

2. Post history ingestion — founder manually pastes 20–30 posts from the demo brand's FB and LinkedIn in the last 30 days into a text file or CSV. The agent reads them before drafting. This is not an API pull. It is a manual file load. Zero OAuth required.

3. Strategist agent draft chain — Claude on Max plan. One chain per brand per week. Output: 5 posts for Facebook (with native format: short caption, link position, hashtag count per FB norms) + 5 posts for LinkedIn (with native format: longer professional framing, no more than 3 hashtags). Each post includes a one-sentence rationale.

4. Client-week packet assembly — takes the 10 draft posts + rationales, formats them into a structured document: weekly calendar view (Mon–Fri), rationale per post, draft monthly report skeleton (3 paragraphs: what we posted, what performed, what we recommend for next month — placeholder data for the demo since there is no real analytics yet).

5. Delivery to approval — packet delivered as a formatted email to the CEO with an approve-all link, a request-edits link, and individual approve/edit per post. No Slack bot for V0.1. Email ships in 4 hours. Slack bot is Phase 1.

6. Approval capture — approve-all records a timestamp and confirmation. Request-edits sends a reply-to-email loop (CEO replies with notes, founder reads and adjusts manually for V0.1). This is not automated edit processing — that is Phase 1. The demo only needs to prove the loop exists, not that it is automated end-to-end.

**Explicit cuts:**

- No scheduler. No posting to any platform. No OAuth. No API connections. Zero.
- No dashboard. No UI beyond the email delivery and a minimal intake page if needed.
- No multi-brand. One brand, one agency, hardcoded to the demo partner.
- No automated edit processing. CEO's edit requests are read by the founder manually.
- No analytics. The monthly report draft uses placeholder performance language.
- No Slack bot. Email only.
- No brand voice training loop. One-shot ingestion from kit + 30 days of posts. Learning over time is Phase 1.
- No client-side portal. The agency CEO is the only approver in V0.1.
- No CSV export. The packet is a formatted email, not a spreadsheet.

**Later (Phase 1, months 1–4):**

- Postiz fork for 14-platform scheduling
- Structured brand kit editor UI
- Automated edit processing
- Slack bot delivery
- Historical performance analytics
- Multi-brand support
- Approval workflow in-product
- Real monthly report with actual data

---

## Success Metric

**The demo is a YES when the CEO says both of these sentences, unprompted:**
1. "This sounds like my client."
2. "I would show this to my client."

One sentence is not enough. Both, in the same demo, from at least 1 of 3 CEOs, by 2026-06-04.

Measurable follow-on: at least 1 of the 3 CEOs commits in writing (email or Slack) to staying in the design-partner program through Phase 1, before the demo session ends.

**Kill signal:** if 0 of 3 CEOs say both sentences after V0.1, the strategist-agent thesis is wrong and we stop or reframe. This is the kill criterion from the project config — it holds.

---

## Top 3 Risks

1. **Draft quality fails the demo.** The brand voice doesn't land — posts sound generic, tone is off, rationale feels templated. This is the single highest-risk item. Mitigation: founder runs 3 internal test cycles against real historical posts from the demo brand before the CEO sees anything. If the internal test fails, the demo is rescheduled — a bad draft demo is worse than a late demo.

2. **The packet framing doesn't resonate — CEOs want to see scheduling first.** Alex called this risk. If the 3 CEOs respond to the "client-week packet" framing with "but can it actually post?" rather than "this is exactly what I need," the framing pivot is wrong and we revert to posts-only with a scheduling roadmap prominent in the deck. Mitigation: founder calls all 3 CEOs with the reframed pitch before 2026-05-28 — confirm which framing excites them before building toward the wrong demo.

3. **Solo dev bandwidth runs out before day 14.** The 14-day window with a day job at Uber is the execution constraint, not the technical difficulty. Mitigation: the cuts above are non-negotiable. If the founder adds one feature outside the must-have list, the deadline moves, and a missed deadline is a kill criterion. Every "what if we also..." question gets logged to a parking lot and answered after the demo.

---

## The 3-CEO Demo Script

This is not a feature tour. It is 3 scenes.

**Scene 1 — "Your client, not a demo brand" (minutes 0–5)**
Founder opens with the brand kit summary on screen: "This is [Brand Name]'s voice profile — I ingested your brief and 30 days of their posts. Here's what the agent understood about them." Reads back 2–3 accurate voice descriptors to the CEO. CEO corrects anything wrong. This moment proves: the agent read the brand, not a generic template.

**Scene 2 — "The week your strategist would have written" (minutes 5–15)**
Founder shares the client-week packet. Does not narrate it — hands it to the CEO and says "read the Monday post and its rationale." Watches the CEO's face. If the CEO says "hm" and starts editing in their head, that is a signal. If the CEO says "this is wrong — they'd never say that," that is also data. Ask: "Would you change the voice, or the strategy?" The answer tells you which axis to improve.

**Scene 3 — "The report you'd send the client" (minutes 15–20)**
Shows the monthly report draft skeleton. "This is what SIGNAL generates at the end of the month. You'd add your logo, fill in the real numbers, and send it. Right now it has placeholder data because we haven't integrated analytics yet — that's month 2. But is this the structure you'd send?" If the CEO says yes, the profit-center framing is validated. If they say "our clients get something totally different," ask them to describe it — that is the product spec for the real Phase 1 report.

Close: "We're onboarding design partners at $300/mo when the scheduler ships in month 1. I'm keeping 3 slots open for the agencies that see this demo. Are you in?" Get a yes or a no in the room. Do not leave with "let me think about it."

---

## Open Questions for the Founder (must be answered before Mia starts mockups)

1. Which agency and which client brand is the V0.1 demo brand? Need brand kit material and 30 posts by 2026-05-24. DRI: founder.

2. Does the demo CEO have a Slack workspace and expect a Slack bot, or is email acceptable? If Slack: add 2 days to build the bot. DRI: founder (ask the CEO today).

3. Will you call all 3 CEOs with the reframed "client deliverable" pitch before 2026-05-28 to validate the packet framing? If 0 of 3 respond stronger to packets, revert to posts-only framing immediately. DRI: founder.

4. Confirmed: Claude on Max plan for the draft chain? No other LLM approved without this decision closed today. DRI: founder.

5. Does the demo brand have 20–30 posts from the last 30 days available in any exportable format (screenshot dump, CSV, copy-paste)? If not, what does "30 days of posts" look like for this brand — are they even posting regularly? If they post 2x per month, the history ingestion step is meaningless. DRI: founder (ask the agency PM).
