# PRD: SIGNAL V0.1
Date: 2026-05-21 (refreshed — guided intake locked)
Approach picked: A (Strategist-First) — unit of work = client-week packet
Author: spm

---

## 1. One-Line Product Statement

SIGNAL turns one client's week into a ready-to-resell deliverable — calendar, rationale, report.

*(15 words)*

---

## 2. The One Demo Moment

CEO B sits down on 2026-06-04. They open one email. It contains a client-week packet for the one client brand we agreed on in V0.1. CEO B reads the Monday Facebook post aloud, pauses, and says one of two things — either "this sounds like them" without being prompted, or "I would show this to my client tomorrow." Those are the only two acceptable demo outcomes. Everything in the 14-day build exists to produce that one moment for that one brand. If the post sounds like a ChatGPT template — flat, generic, hashtag soup — the demo fails regardless of how clean the email looks or how fast the approval loop responds. The voice lands first. Everything else is scaffolding.

*(No verbatim quote from CEO B on file yet — Q1 below unblocks this. Pending exact brand name.)*

---

## 3. V0.1 MVP — 6 Bullets (Build Order)

**1. Guided brand intake — 6 questions + PDF + free-text → per-brand system prompt.**
The founder runs CEO B's contact through the intake form (web form or CLI — whichever ships in 2 hours). The form asks exactly 6 questions (see Section 6). Accepts a PDF upload (brand guidelines, tone doc, or one-pager — whatever the agency has) and a free-text context field. Output: a per-brand system prompt saved to a local file. This is the first thing Raj builds. Nothing else runs without it.

**2. LLM draft chain: system prompt → 5 days × 2 channels → posts + rationales.**
Claude (Max plan — zero marginal API cost) ingests the per-brand system prompt + the 20–30 manually-pasted sample posts and generates the weekly calendar. Output: 5 days × Facebook post + LinkedIn post, each with one-sentence rationale (why this topic / why today / why this hook). Posts flagged LOW CONFIDENCE where the brand kit signal is weak. Zero manual intervention after the brand kit is in.

**3. Strategic header generation.**
Above the calendar: weekly theme (1 sentence), why-this-week context (2–3 sentences connecting to brand cycle or season), watch-for signal (1 sentence). Assembled by the same LLM call as the draft chain. Not a separate UI feature.

**4. Week-4 monthly report draft skeleton.**
On week-4 of each month: the packet appends a structured monthly report skeleton (see Section 5 for exact shape). Placeholder performance language explicitly labeled. No real analytics — V0.1 has none. The agency PM edits in 30 minutes and sends under their letterhead.

**5. Email delivery with approval action block.**
Formatted plain-text email to CEO B's inbox. Approval block at the bottom: "APPROVED" / post-day + platform + note / "REJECT" + reason. Founder monitors the inbox and handles edit requests manually in V0.1. No automated edit processing.

**6. Approval log.**
CEO B's reply triggers a local log entry: timestamp, action type, content. Flat file. No database. This is the audit trail for the demo — proves the loop closed.

---

## 4. Hard Out-of-Scope List

These will be requested. The answer is no for V0.1, every time.

1. **Scheduler / platform posting.** No OAuth. No API connections. No posting to Facebook, LinkedIn, or anywhere else. Zero.
2. **Slack bot delivery.** Email only. Slack OAuth is 2–3 dev days that do not improve the demo moment.
3. **Dashboard or web UI beyond the intake form.** CLI or bare form for intake. No analytics UI. No calendar UI. No approval queue UI.
4. **Multi-brand.** One brand, one agency, hardcoded to CEO B's design-partner brand. Multi-brand is Phase 1.
5. **Multi-agency / multi-tenant.** One agency. One brand. One approval loop. That is the entire system.
6. **Real analytics.** Monthly report uses placeholder performance language. No engagement API pull, no tracking pixel, no reporting dashboard.
7. **Automated edit processing.** Edit requests from CEO B are handled manually by founder. No LLM re-draft triggered by email reply.
8. **Image generation.** Not in V0.1, not in Phase 1. Phase 2 only, firewalled until 30 paid agencies.
9. **Notion / Drive / Slack integration for brand kit ingestion.** Guided intake form and PDF upload only. No third-party integrations.
10. **Historical post API pull.** Manual paste of 20–30 sample posts. No Buffer export, no Facebook Graph API, no LinkedIn content API.
11. **Client portal.** CEO B is the only person with a login-equivalent experience. No client-facing view.
12. **CSV import/export.** Not needed for a 1-brand demo.

---

## 5. Client-Week Packet — Exact Shape

One packet per brand per week. Delivered Monday morning by email. The following is the literal structure of every packet:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLIENT-WEEK PACKET
[Brand Name] — Week of [Mon DD MMM YYYY]
Delivered to: [Agency CEO Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTION 1 — STRATEGIC HEADER
Weekly theme: [1 sentence — the narrative thread tying this week together]
Why this week: [2–3 sentences — connects to brand cycle, seasonal context,
                or last week's performance signal where available]
Watch for: [1 sentence — what to proactively flag to the client]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — WEEKLY CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONDAY
  FACEBOOK
  [Post copy — ≤280 chars, ≤2 hashtags, no emojis unless brand kit specifies]
  Rationale: [1 sentence: why this topic / why today / why this hook]

  LINKEDIN
  [Post copy — ≤600 chars, professional frame, ≤3 hashtags]
  Rationale: [1 sentence: why this topic / why today / why this hook]

TUESDAY — FRIDAY [same structure per day]

Notes:
- Weekend posts omitted unless brand kit specifies weekend cadence.
- LOW CONFIDENCE posts flagged inline:
  ⚠ LOW CONFIDENCE — [reason: brand kit lacks signal on X]. Recommend
    human review before approving this post.
- No post is generated that contradicts a taboo topic from the brand kit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — MONTHLY REPORT DRAFT SKELETON
(week-4 packet only; omitted in weeks 1–3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Brand Name] — Monthly Performance Summary — [Month YYYY]
DRAFT — prepared by SIGNAL. Agency: review, add real metrics, rebrand, send.

WHAT WE POSTED
[3–4 sentences summarizing the month's content themes and strategic rationale]

WHAT PERFORMED
- [Top theme 1 — describe the content pattern; engagement data: placeholder
  in V0.1 — agency to fill with actual numbers before sending to client]
- [Top theme 2]
- [Top theme 3]

WHAT WE LEARNED
[2–3 sentences — voice observation or platform-level insight from the month's posts]

NEXT MONTH RECOMMENDATION
[2–3 sentences — what SIGNAL proposes to shift in strategy and why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — APPROVAL ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply "APPROVED" — approve all posts as-is.
Reply "[Day] [Platform]: [your note]" — request an edit on one post.
Reply "REJECT [reason]" — reject the full week. SIGNAL treats this as a
brand kit gap and will ask the founder to update the intake before
re-generating.
```

**Per-post rationale rule:** Every rationale sentence answers exactly one of: (a) why this topic — anchored to a brand kit pillar or a performance signal from sample posts; (b) why today — audience timing, campaign cycle, or contextual hook; (c) why this hook — format choice relative to brand voice. One sentence. No padding. If the agent cannot answer any of the three, it flags LOW CONFIDENCE and states the gap.

**Concrete example for CEO B's agency (slot to fill once Q1 is answered):**

> MONDAY / FACEBOOK
> "This week we're leaning into behind-the-scenes founder credibility — three of [Brand]'s top 5 posts last month were founder-POV stories, and engagement averaged 2.3x their product posts."
> Rationale: Founder-POV is a proven pillar in the brand kit (#2 messaging pillar); Monday front-loads the week with highest-engagement format while the audience is fresh.

*(The exact brand name is blocked on Q1. The above is the structural model.)*

---

## 6. Guided Intake Spec

**Purpose:** Force signal in. Replace "paste your brand voice" with structured questions that produce consistent, comparable per-brand system prompts. Answers double as eval fixtures — in Phase 1, these become the ground truth for automated brand-voice testing.

**The 6 Questions (verbatim — these ship in V0.1 as-is):**

**Q1. Brand voice in 3–5 words.**
"Describe your client's brand voice in 3–5 adjectives. Examples: 'warm, direct, no-jargon' or 'aspirational, premium, globally-minded'. Do not write a paragraph — force yourself to pick 5 words or fewer."

**Q2. Target audience — one person.**
"Describe the one human who is the target audience for this brand's social content. Include: age range, job or life situation, what they care about, what they scroll past. One paragraph. The more specific, the better the drafts."

**Q3. Taboo topics — explicit no-list.**
"List every topic, tone, or phrase this brand will never use. Examples: competitor names, political topics, slang, profanity, price mentions. Be exhaustive — anything missing here is a risk of appearing in a draft."

**Q4. Three posts they love.**
"Paste 3 posts from this brand (or another brand they admire) that nail the voice. Include the platform, the copy, and one sentence on why this one works."

**Q5. Three posts they hate.**
"Paste 3 posts — from this brand or any brand — that they would be embarrassed to send. Include why each one fails. These negative examples are as important as the positive ones for calibrating the agent."

**Q6. KPIs — what 'performing well' means.**
"What does success look like for this brand's social content? Pick 1–2: engagement rate, follower growth, click-throughs to site, DMs, share/saves, brand sentiment. What number or threshold would make you say 'that post worked'?"

**PDF upload field:** Optional. Accepts any PDF (brand guideline, tone of voice doc, one-pager). Text extracted and appended to the system prompt context. If the PDF is unreadable or image-only, the founder is notified to paste the key content manually. No OCR for V0.1.

**Free-text context field:** Open text box. Label: "Anything else SIGNAL needs to know about this brand that the questions didn't capture." No word limit. Common use: campaign context, recent news, client relationship quirks.

**How the per-brand system prompt is assembled:**

```
BRAND SYSTEM PROMPT — [Brand Name]
Generated: [timestamp]
Source: SIGNAL Guided Intake v0.1

=== VOICE ===
[Q1 answer verbatim]

=== AUDIENCE ===
[Q2 answer verbatim]

=== TABOO ===
[Q3 answer verbatim — rendered as a bulleted list]

=== POSITIVE EXAMPLES ===
[Q4 — each post with platform label and why-it-works note]

=== NEGATIVE EXAMPLES ===
[Q5 — each post with why-it-fails note]

=== SUCCESS DEFINITION ===
[Q6 answer verbatim]

=== SUPPLEMENTARY CONTEXT ===
[PDF extracted text, truncated to 2000 tokens]
[Free-text field verbatim]

=== GENERATION RULES ===
- Facebook: ≤280 chars, ≤2 hashtags.
- LinkedIn: ≤600 chars, professional frame, ≤3 hashtags.
- Every post must be consistent with VOICE above.
- Every post must avoid every item in TABOO above.
- Every post must be written for AUDIENCE above.
- If you cannot justify a post rationale using VOICE, AUDIENCE, or POSITIVE EXAMPLES, flag it LOW CONFIDENCE.
- Do not invent performance data. Use POSITIVE EXAMPLES as the only performance signal in V0.1.
```

**Concrete example output prompt (structural — brand name pending Q1):**

```
=== VOICE ===
Warm, direct, community-first, no-jargon, story-led

=== AUDIENCE ===
28–40-year-old small business owners in Tier 2 Indian cities.
Running a 3–10 person team. Care about practical growth advice
and peer credibility. Scroll past polished corporate content.
Stop for relatable founder stories and actionable tips.

=== TABOO ===
- No competitor brand mentions
- No political or religious topics
- No pricing or discount language
- No engagement-bait questions ("tag a friend who...")
- No stock photo captions

=== POSITIVE EXAMPLES ===
[LinkedIn] "Three years ago I couldn't afford a designer..."
Why it works: Founder vulnerability + specific number + no call-to-action.
Audience responds to the honesty.

=== NEGATIVE EXAMPLES ===
[Facebook] "Exciting news! Big announcement coming soon! Stay tuned!"
Why it fails: Vague, hype-y, no value to the reader. Brand voice is direct;
this is the opposite.

=== SUCCESS DEFINITION ===
Save/share rate on LinkedIn. A post that gets 10+ saves within 24 hours
worked. Engagement rate on Facebook above 3% is good.
```

---

## 7. Demo Success Criteria — Binary

The demo on 2026-06-04 is a PASS or a FAIL. No "pretty good" — that is a FAIL.

**PASS conditions (both must be true):**

1. CEO B reads the week's packet for the demo brand and says — unprompted — either "this sounds like them" or "I would show this to my client tomorrow." One of those two sentences, in their own words. Not prompted by the founder asking "what do you think?"

2. CEO B commits in writing (email reply or Slack message) before leaving the session that they will stay in the design-partner program through Phase 1 (Postiz-fork scheduler, target 2026 Q3).

**FAIL conditions:**

- CEO B says "it's pretty good but I'd need to edit all of these." FAIL.
- CEO B asks "what platforms does this post to?" and is disappointed by the answer. FAIL — failure to set expectations. *Founder must pre-brief CEO B: V0.1 is the strategist, not the scheduler.*
- Any post in the packet references a taboo topic from the brand kit. Hard FAIL — brand kit ingestion is broken.
- Founder had to manually adjust any post before showing it to CEO B. FAIL on zero-intervention requirement.

---

## 8. Day-60 Kill Criteria — Numeric

**Kill date: 2026-07-20**

Stop SIGNAL or pivot to selling directly to brand owners (skip agency layer) if any of these is false by 2026-07-20:

| # | Criterion | Threshold | DRI |
|---|-----------|-----------|-----|
| 1 | Framing validation call | At least 2 of 3 conditional-yes CEOs respond more positively to "SIGNAL produces the client deliverable" framing than to "SIGNAL drafts the week" framing — confirmed before 2026-05-28 | Founder |
| 2 | Demo success | At least 1 CEO says the PASS sentence at the 2026-06-04 demo and commits to Phase 1 design-partner program in writing | Founder |
| 3 | Cold referral validation | At least 2 peer agency CEOs outside the founder's network (cold referrals, not original 3) take a 20-minute call and validate the $300 price on the reframed pitch — confirmed by 2026-06-20 | Founder |
| 4 | Phase 1 paid conversion | At least 3 agencies pay $300/mo by 2026-07-20 (before or coincident with Phase 1 Postiz fork reaching FB + LinkedIn + IG) | Founder |

**Reasoning on threshold 4:** N=3 by day 60 is the minimum to validate that the design-partner pool converts to paid without waiting for the full 30-agency target. 3 paid agencies at $300 = $900 MRR. Not the win metric ($9K MRR by EOY), but proof the unit economics are real and the conditional yes is not vaporware.

If thresholds 1–3 all fail: kill. If threshold 4 fails but 1–3 pass: Phase 1 scope is wrong — re-run options. If threshold 4 passes but 1–3 are mixed: advance with caution and pick up cold-referral validation in Phase 1.

---

## 9. Open Questions for the Founder

Three questions. Each blocks specific build work.

**Q1 — Which brand within CEO B's agency is the V0.1 design-partner brand?**
Need: brand name, industry/vertical, rough brand kit (even a verbal brief), and 20–30 sample FB + LinkedIn posts — by 2026-05-24 (day 3 of the 14-day window). If this arrives after 2026-05-24, the draft-quality test window compresses to fewer than 3 internal test cycles before the demo. The demo date is at risk.
Blocks: Raj's LLM chain (step 2 of build order) and Sarah's eval fixtures.
DRI: Founder. Answer by: 2026-05-21 EOD.

**Q2 — Email or Slack for V0.1 packet delivery?**
Email ships in ~4 hours (SMTP + formatted plain text). Slack bot requires OAuth + bot token setup (2–3 dev days). Recommendation: email for V0.1. Confirm only if CEO B has explicitly asked for a Slack delivery and has a workspace ready to onboard a bot today.
Blocks: Raj's delivery layer (step 3 of build order).
DRI: Founder. Answer by: 2026-05-22.

**Q3 — Does the demo brand's PDF brand guideline exist, and can the agency share it before 2026-05-24?**
If yes: test PDF extraction during brand intake build. If no: intake runs on Q1–Q6 answers + free-text only, which is fine — but we need to know before Raj builds the PDF upload path.
Blocks: PDF handling in guided intake (step 1 of build order).
DRI: Founder (ask CEO B's agency contact). Answer by: 2026-05-22.

---

## 10. DRI Table

| Workstream | DRI | Deadline |
|------------|-----|----------|
| PRD (this document) | Sarah (spm) | Done — 2026-05-21 |
| Intake UX (form design + system prompt assembly) | Mia (staff-frontend) | After Q1 + Q3 answered |
| Packet generation (LLM chain, email delivery, approval log) | Raj (staff-backend) | After Q1 + Q2 answered |
| Design-partner relationship (brand kit, sample posts, demo scheduling) | Founder | 2026-05-24 for kit; 2026-06-04 for demo |
| Eval fixtures (3 internal test packets before CEO B sees anything) | Sarah (spm) | 2026-06-01 — 3 days before demo |
| Reframe calls with all 3 conditional-yes CEOs | Founder | 2026-05-28 |
| Cold referral outreach (2 peer CEOs outside founder's network) | Founder | 2026-06-20 |

---

## Evidence (sources that ground every claim above)

- [Search Engine Land — AI squeezing agencies 2025](https://searchengineland.com/ai-squeezing-marketing-agencies-472189) — 66% of agency owners cite talent pipeline risk; junior strategist attrition is the stated pain, not a hypothesis.
- [Blaze AI Review — SaaSGenius 2026](https://www.saasgenius.com/reviews/blaze-ai/) — Blaze autopilot at $46–65/mo already drafts a week of posts. $300 is defensible only if SIGNAL produces a resellable deliverable (the client report), not just better post drafts.
- [ReportsMate 2026](https://www.reportsmate.com/blog/how-to-automate-client-reporting-for-marketing-agencies-in-2026) — agencies spend 2–3 hrs/client/month on manual reporting at $100–150/hr billable. 20 clients = 40–60 hrs/month. SIGNAL's report draft removes that labor line.
- [Postiz Review 2026 — LifetimeDealTech](https://lifetimedealtech.com/postiz-review-2026/) — open-source, MIT-licensed, agentic-ready. Phase 1 scheduler is a Postiz fork. Do not build from scratch.
- [ANA: In-house agency trend — Marketing Dive](https://www.marketingdive.com/news/in-house-agency-trend-gain-steam-ana/649681/) — 82% of major brands now have in-house agencies (up from 42% in 2008). The agency layer is consolidating to senior-strategy-plus-AI-execution; SIGNAL targets exactly that buyer.

---

## What This PRD Does NOT Relitigate

The following are locked. They are not open for discussion in the build sprint:

- Price: $300/agency/mo. Not $99. Not $599.
- Unit of work: client-week packet (calendar + rationale + monthly report skeleton). Not "5 drafts."
- Channels: Facebook + LinkedIn only. Not Instagram, not TikTok.
- Approval loop: email reply. Not in-product. Not Slack (pending Q2).
- Intake: 6 guided questions + PDF + free-text. Not Notion integration. Not Drive sync.
- Design partner: CEO B's agency. DRI: Founder.
- Phase 2 firewall: image gen, edit studio, influencer — not until 30 paid agencies.
- LLM: Claude on Max plan. Zero marginal API cost. Locked.
