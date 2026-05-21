# SIGNAL — Everything Doc (North-Star Vision)
Date: 2026-05-21
Author: spm
Status: REFERENCE ONLY — not a build commitment except V0.1

---

## The North Star

SIGNAL is the first product where a marketing agency gives a brand kit, a Slack channel, and a client's approval, and SIGNAL runs that client as if it were a junior strategist on payroll — producing the posts, the scheduling, and the monthly deliverable the agency bills the client for.

Not a scheduler with AI on top. Not a writing assistant. A strategist agent that produces an agency deliverable the client sees and the agency resells at margin.

The long arc: SIGNAL becomes the operating system for brand marketing — starting with agencies (multi-brand, multi-channel, approval-heavy) and expanding to in-house teams and solo brand operators, all on the same brand-as-workspace primitive. Every feature, every UX decision, every platform integration traces back to one question: does this help an operator produce and prove strategic value for a specific brand?

---

## The Brand-as-Primitive Architecture

Every workspace primitive in SIGNAL is a brand, not a user, not a team, not a channel.

A brand has:
- A Brand Kit (voice, tone, visual guidelines, messaging pillars, audience definition)
- A Platform Account Set (up to 20 accounts per brand across 14 platforms)
- A History (post archive, performance data, campaign calendars, approval decisions)
- An Agent (the per-brand strategist — owns the weekly content cycle for that brand)
- An Approval Chain (agency PM → agency CEO → optional client-side approver)

This is not how Buffer, Hootsuite, or even Postiz are architected. They are channel-first or user-first. SIGNAL is brand-first. That distinction is the structural moat — the data model makes per-brand voice isolation, per-brand performance history, and per-brand agent memory a first-class citizen, not a bolt-on.

Implication for design: every view in SIGNAL (calendar, queue, analytics, approval inbox) is scoped to a brand. The agency-level view is a rollup across brands, not the primary lens. This is the design discipline Mia must hold.

---

## Full Feature Catalog

### Core (required for the $300 to close — Phase 1)

**Brand Workspace**
- Brand kit ingestion (text, Google Doc, PDF, URL)
- Voice profile: tone sliders, messaging pillars, audience persona, off-limits topics
- Per-brand post archive import (CSV or API pull from connected platforms)
- Brand-level performance baseline (last 90 days engagement benchmarks by platform)

**Per-Brand Strategist Agent**
- Weekly content calendar generation: 5–7 posts per active channel per week, with strategic rationale per post ("why this post, why this week")
- Brand-cycle awareness: ingests campaign calendar, seasonal events, client milestones
- Historical performance integration: weights draft decisions against what actually worked
- Competitive context (optional V2): monitors 2–3 named competitors per brand for gap analysis
- Voice consistency guardrails: self-check pass before any draft is sent for approval
- Client-week packet: calendar + rationale document delivered to agency Slack at Monday 9am

**14-Platform Scheduler**
Priority order (by agency client frequency, not platform size):
1. Facebook (Meta Business Suite API)
2. LinkedIn (LinkedIn Marketing API)
3. Instagram (Meta Graph API — shares OAuth with FB)
4. Twitter/X
5. TikTok
6. Pinterest
7. YouTube (video scheduling only, no Shorts in V1)
8. Reddit (brand subreddit posts)
9. Threads (Meta, shares auth)
10. Bluesky
11. Mastodon (federated — low priority)
12. Google Business Profile
13. WhatsApp Business (broadcast messages)
14. Snapchat (low priority — niche brand use)

Note: Facebook, LinkedIn, Instagram share the Meta OAuth surface and should be treated as one integration effort. TikTok and YouTube have separate, higher-friction review processes. Platform priority must be validated against the 3 CEOs' actual client rosters.

**Approval Workflow**
- Draft delivered to Slack (bot) or email with approve / request-edit / reject inline actions
- Edit requests trigger in-app comment thread on the specific post
- Approval state machine: Draft → Agency Review → Client Review (optional) → Approved → Scheduled
- Bulk approval: approve all 5 posts in one tap, or flag individual posts for edit
- Audit log: every approval, rejection, and edit recorded per brand per week

**Analytics**
- Per-brand performance dashboard: engagement, reach, click-through by platform and post
- Post-vs-draft comparison: did the approved version perform better or worse than the AI draft?
- Brand health trend: weekly rollup, 90-day view, exportable PDF for client reports
- Approval cycle time: average hours from draft to approved (operational metric for agencies)

**Client-Week Packet and Monthly Report**
- Weekly: calendar + strategic rationale document (Slack or PDF)
- Monthly: SIGNAL drafts the client-facing performance report (agency rebrand + send)
- Report includes: what was posted, what performed, what the agent recommends for next month
- This is the line item the agency currently bills $1,500–2,500/client/month for. SIGNAL produces the draft. The agency adds their logo and sends it.

Evidence: Marketing agencies spend 2–3 hours per client on monthly reports; at $150/hr billable rate that is $300–450 of labor per client per report. Agencies managing 20 clients spend 40–60 hours/month on reporting alone — more than one FTE. [Source: ReportsMate 2026](https://www.reportsmate.com/blog/how-to-automate-client-reporting-for-marketing-agencies-in-2026)

### Phase 2 — Post 30 Paid Customers (FIREWALLED until hit)

**AI Image Generation**
- Per-brand visual style training (upload 10 approved brand images, train style vector)
- Draft post images alongside draft copy — same approval loop
- Edit studio: crop, resize, overlay text, brand logo placement
- Platform-native size variants auto-generated (1:1 for IG, 16:9 for LinkedIn, 9:16 for Stories)

**Influencer Marketplace**
- Brand-side: discover creators by niche, audience match, engagement rate
- Agency-side: manage creator briefs, content approval, performance tracking in SIGNAL
- This is a separate product surface, not a Phase 1 add-on

**Advanced Competitive Intelligence**
- Real-time competitor post monitoring (public feeds only)
- Gap analysis: topics your brand hasn't covered that competitors are winning on
- Trend signals: rising topics in your brand's niche before they peak

**White-Label / Agency-Branded Portal**
- Client-facing portal with agency logo where clients log in to approve posts
- Removes the "SIGNAL" brand from the client experience entirely
- This is a retention driver for large agencies, not an acquisition driver

---

## Phasing

### V0.1 — 14 days (deadline 2026-06-04)

Purpose: Belief-builder. Prove to 3 CEOs that the AI can produce strategy, not just posts. Not a contract closer.

Scope (non-negotiable, see PRD):
- 1 brand, 1 agency, Facebook + LinkedIn only
- Brand kit ingestion via text paste or Google Doc link
- Strategist agent drafts one client-week packet: 5 posts per channel + strategic rationale document + draft monthly report skeleton
- Delivery via Slack bot or email (founder picks one, does not build both)
- One-tap approve or request-edit
- Zero scheduler. Zero dashboard. Zero multi-brand. Zero analytics.

Demo success: CEO says "this sounds like my client" AND "I would show this to my client." Both sentences. Not one.

### Phase 1 — Months 1–4 Post-Demo (to unlock the $300)

Month 1:
- Postiz fork: configure for SIGNAL — agency workspace, brand grouping, OAuth for FB + LinkedIn + Instagram (3 platforms)
- Approval workflow in product (not just Slack bot)
- Brand kit structured editor (replaces text paste)
- Weekly packet delivery automated (no founder manual trigger)

Month 2:
- Historical post import + LLM performance analysis
- Add Twitter/X + TikTok (4 additional platforms, now 5 total)
- Client-week packet becomes standard output for all brands, not just demo brand
- First paying customer target: 1 of 3 CEOs converts

Month 3:
- Full analytics dashboard (per-brand, per-platform)
- Monthly client report generation (draft + export)
- Brand-cycle calendar ingestion (campaign calendars, seasonal triggers)
- Add Pinterest + YouTube + Reddit (3 more platforms, now 8 total)

Month 4:
- Remaining 6 platforms: Threads, Bluesky, GMB, WhatsApp Business, Mastodon, Snapchat
- Bulk approval UI (approve week for all brands in one session)
- Agency-level rollup dashboard
- Kill-criteria checkpoint: 3 of 3 CEOs converted or replan

### Phase 3 — Vision (post-30 paid)

- AI image generation + edit studio
- Influencer marketplace
- White-label agency portal
- In-house brand team tier (different pricing, different ICP)
- Expand to solo brand operators (self-serve, lower price point)
- API access for enterprise integrations

Nothing in Phase 3 gets scoped until 30 paid agencies are live.

---

## UX and Scale Problems: P-1 for Mia

Mia must design for the full scale before V0.1 code ships. These are not later problems — they are paper problems now.

**Problem 1: Calendar Explosion**
50 brands × 5 posts/week × 14 platforms = 3,500 post slots per week per agency.
The calendar view cannot be a Gantt chart. It must be: brand-scoped by default, with a roll-up toggle that shows the agency the week across all brands in a heat-map or swimlane layout. The brand-level calendar must handle 14 platform rows without becoming unreadable. Mia must solve the visual density problem before she designs a single pixel of V0.1.

**Problem 2: Bulk Operations at Volume**
An agency with 30 brands needs to: change the posting time for all brands on Facebook from 9am to 11am in one operation. Reschedule all posts for a brand because a client is in crisis. Approve all Monday posts for 10 brands in one session.
SIGNAL needs a bulk operations layer that is not a table with checkboxes. Study Linear's command palette and Notion's multi-select for the UX model.

**Problem 3: CSV Import/Export**
Agencies have existing content calendars in Google Sheets. They need to import them. They also need to export SIGNAL's calendar to send to clients.
V0.1 does not need CSV. Phase 1 does. But the data model must support it from day one or the import/export becomes a migration nightmare.

**Problem 4: Approval Queue at Volume**
30 brands × 5 posts each = 150 posts per approval session per week. The agency CEO cannot review 150 posts one by one. The approval UX must support: view by brand, bulk-approve by brand, flag individual posts for edit, and see the strategic rationale without opening each post separately.
This is the highest-risk UX problem in Phase 1. Mia must mock three different patterns for this surface.

**Problem 5: Per-Brand Voice Isolation**
The strategist agent must never bleed voice between brands. A post drafted for Brand A must be provably un-influenced by Brand B's voice profile.
This is an architecture problem (separate prompt contexts, no shared memory across brands) and a UX problem (brand kit editor must make the isolation visible and trustworthy to the agency CEO). Mia's brand kit editor must feel like a vault, not a form.

---

## Open Questions and Assumptions

Every item here is either answered before V0.1 ships or logged as an accepted risk.

**Unresolved — block V0.1:**

1. Which of the 3 design-partner agencies and which specific client brand is the V0.1 demo brand? We need brand kit material and 30 days of post history by day 3 of the 14-day window. If not resolved by 2026-05-24, the 2026-06-04 deadline is at risk. DRI: founder.

2. What format does the demo brand's brand kit exist in? Text, Google Doc, PDF, "in someone's head"? V0.1 accepts text paste or Google Doc link. If the answer is "in someone's head," the brand kit ingestion session must be a structured 60-minute call with the agency PM. Do not build a file parser. DRI: founder.

3. Slack bot or email for V0.1 approval delivery? Slack requires OAuth setup (2–3 days). Email ships in 4 hours. For a 14-day window, the right call is email unless the demo CEO already has a Slack workspace and expects the bot. Decide by 2026-05-22. DRI: founder.

4. LLM for the draft chain: Claude (zero marginal cost on Max plan) vs. GPT-4o vs. Gemini. Claude is the obvious call. Confirm and close. DRI: founder.

**Unresolved — block Phase 1:**

5. Which platforms do the 3 CEOs' client brands actually use? This determines Phase 1 OAuth priority order. Must be answered in the first post-demo call with all 3 CEOs. TikTok and YouTube OAuth review processes take 4–6 weeks — start them immediately if needed. DRI: founder.

6. Does the client-week packet (calendar + rationale + report draft) resonate more with the 3 CEOs than "5 posts per channel"? Alex argues yes. This is the framing pivot. Must be validated before Phase 1 scope is locked. Method: founder calls all 3 CEOs with the reframed pitch before 2026-05-28. DRI: founder.

7. What is the Postiz fork strategy? Self-host vs. managed vs. rebuild on Postiz API? The MIT license makes forking legal. But the fork decision affects Phase 1 architecture. Raj must evaluate before month 1 starts. DRI: staff-backend.

8. Approval chain depth: does the agency want a client-side approver login, or does the agency handle all approvals internally and just send the final calendar to the client? This determines whether Phase 1 needs a client portal or just an export. DRI: founder (ask all 3 CEOs).

**Accepted assumptions (revisit if evidence changes):**

- The $300/mo per-agency price point holds vs. Blaze's $65/mo because SIGNAL produces the monthly client deliverable (a resellable output), not just posts (a content tool). This is the profit-center framing. If 2 of 3 CEOs do not validate this by 2026-05-28, revisit pricing and ICP.
- Mid-market agencies (10–30 brands) are the primary ICP. The in-housing trend (ANA: 82% of major brands in-house as of 2023) affects large enterprise brands, not mid-market agencies serving SMB clients. This assumption holds unless the 3 CEOs report client loss to in-house teams at scale.
- Claude on the Max plan is zero additional COGS for V0.1. This changes in Phase 1 when multi-brand multi-week inference volume increases. COGS estimate of $45/agency/mo must be validated against real Phase 1 inference costs.
- Postiz fork is viable for Phase 1 scheduler. MIT license confirmed. OAuth complexity per platform is the variable — not the fork itself.
- Brand voice quality is achievable on V0.1 with prompt engineering alone. No fine-tuning, no RAG over historical posts. Historical post RAG is Phase 1. If prompt-only quality fails the demo, this assumption must be revisited immediately.

---

## What This Doc Is Not

Nothing in Phase 1, Phase 2, or Phase 3 of this document is a build commitment. This is the map, not the work order. The only build commitment in SIGNAL today is V0.1, scoped in the PRD. All other features exist to inform design decisions (Mia must design for scale) and to answer investor or CEO questions about where this goes. Do not build ahead of the phase gate.

The founder's admitted scope-expansion tendency is the primary execution risk. This doc is not permission to expand. It is permission to think big and build small.

---

## Sources

- [Marketing Agency Benchmarks 2026 — tmetric](https://blog.tmetric.com/marketing-agency-profitability-benchmarks/)
- [How to Automate Client Reporting 2026 — ReportsMate](https://www.reportsmate.com/blog/how-to-automate-client-reporting-for-marketing-agencies-in-2026)
- [Blaze AI Review 2026 — WMappDigital](https://wmappdigital.com/blaze-ai-review/)
- [Blaze AI Pricing — blaze.ai](https://www.blaze.ai/pricing)
- [Postiz Review 2026 — LifetimeDealTech](https://lifetimedealtech.com/postiz-review-2026/)
- [ANA In-House Agency Trend — Marketing Dive](https://www.marketingdive.com/news/in-house-agency-trend-gain-steam-na/649681/)
- [AI Social Media Management Costs 2026 — Apaya](https://apaya.com/blog/ai-social-media-management-costs)
