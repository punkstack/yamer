# Product Options: signal
Date: 2026-05-21
Author: spm

## Problem (one paragraph, user's voice)

I run a mid-market agency with 15 client brands. My junior strategist costs me $4K/mo, doesn't remember last quarter's brand voice decisions, and uses ChatGPT for drafts and Buffer to schedule — three tools, zero connective tissue. When she quits, I lose institutional knowledge I can't recover. Buffer and Sprout don't think — they post. Marky and Blaze write but they don't learn my clients' actual voice across time, and they can't handle the 10–14 platforms my clients now demand. I'd replace that $4K/mo salary with a $300/mo tool tomorrow — but only if it actually does the strategy, not just the scheduling.

---

## Evidence base

- [AI is squeezing marketing agencies from both sides — Search Engine Land](https://searchengineland.com/ai-squeezing-marketing-agencies-472189): 66% of agency owners worry about talent pipeline; basic content creation is being commoditized. Agencies are being squeezed on both sides — clients want savings passed through, internal margins shrinking. This confirms the wedge: the $300 seat isn't competing with Buffer ($15/mo), it's competing with a junior strategist ($3–6K/mo).
- [Blaze AI Pricing 2026 — SocialRails](https://socialrails.com/blog/blaze-ai-pricing): Blaze's Growth plan (10 accounts) = $85/mo. Their done-for-you "dedicated strategist" tier = $999–5,999/mo. There is a dead zone between $85 and $999 where SIGNAL lives. No competitor owns $300/mo for AI-first, per-brand strategy at scale.
- [Postiz GitHub — gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app): Open-source, 20+ integrations, agency customer groups, approval flows. Self-hostable. This is the Phase 1 scheduler foundation — do not build from scratch.
- [Sprout Social Trustpilot 2026 — Trustpilot](https://www.trustpilot.com/review/sproutsocial.com): Agencies reporting double-billing, forced auto-renewals, per-user pricing that doesn't scale for client-facing work. Confirmed churn signal from the enterprise end — agencies are actively looking for alternatives.

---

## Three approaches

### Approach A — Strategist-First

What it is: Build the per-brand AI strategist agent as the entire V0.1 product. No scheduler. The agent ingests brand kit + post history, drafts the week's posts for FB + LinkedIn, delivers to founder/CEO via Slack or email, gets a one-tap approve or edit. Scheduler is Phase 1 — bolted on via Postiz fork after the strategist proves value.

Scope: ~8 requirements (brand ingestion, LLM prompt chain per brand, post draft UI, Slack/email delivery, approve/edit loop, audit log of decisions, brand voice memory, FB + LinkedIn output format). V0.1 is 3–4 of these.

Timeline: V0.1 in 14 days (2026-06-04). Phase 1 in 4 months post-demo.

Risk profile: Medium — why: The strategist is the hardest part (brand voice quality = the product), but it's also the only part that matters for V0.1. Scheduler commodity risk is deferred. Main risk: if draft quality is mediocre, no amount of polish saves the demo.

Best if: The founder believes the 3 CEOs will react to great drafts before they need to see scheduling. Best if the real demo moment is "holy sh*t it sounds like my client" not "I can post to 14 platforms."

Who it wins: The 3 conditional-yes CEOs who specifically called out "AI marketing plans" and "brand cycles" as requirements. Wins the buyer who is replacing a junior strategist, not replacing Buffer.

Who it loses: Agencies who are already doing strategy fine and just want multi-platform scheduling cheaper than Sprout.

What it kills later: Nothing. Scheduler snaps on via Postiz in Phase 1. This approach preserves all options.

14-day demo feasibility: High. Scope is 1 brand × 2 channels × 5 posts × approve-in-Slack. Solo dev can ship this nights/weekends in 14 days.

Conversion-to-$300 odds: Medium-high. The $300 conditional yes requires the full list (scheduler + analytics + brand cycles). V0.1 doesn't close the deal — it builds the belief that the AI can actually do strategy. That belief is what makes the CEO wait 4 months for Phase 1 to close.

Evidence: Search Engine Land confirms agencies are losing junior staff to AI — a $300/mo AI strategist is a direct replacement thesis. Blaze's $85 offering has no "per-brand memory" or "week drafting" feature — the niche is real.

---

### Approach B — Scheduler-First

What it is: Fork Postiz (open-source, 20+ platforms, approval flows, agency customer groups). Wrap a thin AI layer on top for content suggestions. Position as "smarter Hootsuite at 1/10th the price." Lead with the scheduler, add strategist capabilities iteratively.

Scope: ~15 requirements (Postiz fork, rebrand, agency workspace config, LLM content suggestions per post, approval flow UI, analytics dashboard, 14-platform OAuth chain, rate limit handling, brand grouping, white-label). V0.1 would be a subset — but even a minimal viable scheduler is 4–6 weeks of OAuth plumbing alone.

Timeline: V0.1 in 14 days: NOT feasible. A scheduler demo that actually posts to FB + LinkedIn requires OAuth, token management, error handling. That is not 14 days solo. Realistic V0.1: 6–8 weeks.

Risk profile: High — why: The 14-day demo deadline is a hard kill criterion from the founder. Approach B fails it. Additionally, Postiz already exists. Self-hostable, $0/mo. An agency that knows Postiz exists will ask "why pay $300 for a fork?" Commodity risk from day 1.

Best if: The 3 CEOs' primary pain is platform fragmentation, not strategy quality. If "I already have good drafts, I just can't post to 14 places" is the verbatim pain — this is the right call. Current evidence does not support that.

Who it wins: Agencies who are Hootsuite-heavy and price-sensitive. Not the design-partner ICPs.

Who it loses: The 3 conditional-yes CEOs, who specifically named "AI marketing plans" and "brand cycles" — neither of which a scheduler fork provides.

What it kills later: The strategist moat. If you lead with scheduling, you're Postiz with a markup. Competitors can always undercut on platform count.

14-day demo feasibility: Low. OAuth plumbing for FB + LinkedIn alone takes 3–5 days. Error handling, token refresh, content format per platform — you're at week 3 before anything looks good.

Conversion-to-$300 odds: Low-medium. A scheduler at $300 competes directly with Sprout ($249/seat/mo, well-known brand) and Postiz ($49/mo self-hosted). The price justification falls apart without the strategist moat.

Evidence: [Postiz Review 2026 — aichief.com](https://aichief.com/ai-marketing-tools/postiz/) confirms Postiz already handles 20+ channels, approval flows, agency grouping. Building a worse version of this in 14 days is not viable.

---

### Approach C — Hybrid (Thin Scheduler + Thin Strategist)

What it is: Build both the strategist agent and the scheduler in parallel, neither at full depth. V0.1 ships a basic scheduler (FB + LinkedIn) with AI draft suggestions alongside it. The pitch is "draft + schedule in one tool" from day one.

Scope: ~18 requirements. Scheduler + AI layer is 2 separate complex surfaces that must be coherent in UX. At solo-dev capacity, this is 6–8 weeks minimum.

Timeline: V0.1 in 14 days: NOT feasible. Two surfaces, both shallow, both need OAuth + LLM integration. You'll have neither working well at the demo.

Risk profile: High — why: "Best of both worlds" products at V0.1 are typically best-of-neither. The CEO at the demo sees a scheduler that can't post reliably and drafts that are thin because the brand memory system wasn't the focus. Neither surface impresses. Classic scope trap — the exact anti-pattern the config warns against.

Best if: The founder wants to show a "complete product vision" in the demo. But the demo is a belief-builder, not a feature tour. A complete-but-shallow demo loses to a narrow-but-jaw-dropping one.

Who it wins: No one decisively. Can't beat Postiz on scheduling at V0.1. Can't beat a focused strategist agent either.

Who it loses: The 3 CEOs who want to be impressed by one thing, not shown two half-done things.

What it kills later: Forces 4 months of catch-up on two surfaces instead of doubling down on the winning one.

14-day demo feasibility: Very low.

Conversion-to-$300 odds: Low. The $300 conditional yes requires quality, not breadth. Quality needs focus.

Evidence: Blaze AI's Growth plan at $85/mo already does thin-scheduler + thin-AI. Adding SIGNAL at $300 with the same value prop is a hard sell without a clear differentiated depth. [Blaze AI Review 2026 — SocialRails](https://socialrails.com/blog/blaze-ai-review)

---

## My recommendation

**Approach A — Strategist-First.**

The only approach that hits the 14-day demo deadline, the only one that competes on the axis competitors cannot easily copy (per-brand voice memory + weekly strategy drafts), and the only one that maps cleanly to the verbatim conditional yes from the 3 CEOs. The scheduler is a Phase 1 bolt-on via Postiz fork — it's not a hard problem once the strategist proves value. Cut scope harder than feels comfortable, nail the one demo moment ("holy sh*t it sounds like my client"), and use that belief to buy 4 months to finish the product that closes at $300.

---

## PRD skeleton (Approach A)

### V0.1 acceptance criteria (demo is a YES when)

1. A CEO from one of the 3 design-partner agencies sees 5 draft posts for their client brand — FB format and LinkedIn format — and says "this sounds like them" without editing the brand voice.
2. The CEO can approve or request edits from Slack or email in fewer than 3 taps.
3. The founder can swap to a different brand kit in under 10 minutes (proves the system is brandable, not hardcoded).
4. No draft references a competitor or uses a tone inconsistent with the provided brand kit.
5. Zero manual intervention from the founder between brand-kit ingestion and draft delivery.

These are the only 5 acceptance criteria. If all 5 hit, the demo is a YES. If any one fails, the demo is a NO.

### Phase 1 roadmap (months 1–4 post-demo, to unlock $300)

| Month | Milestone | What it unlocks |
|-------|-----------|----------------|
| M1 | Postiz fork configured for SIGNAL: 14-platform OAuth, agency workspace, brand groups | Scheduling capability — CEOs can see the roadmap demo |
| M1 | Brand-cycle layer: ingest campaign calendars, seasonal triggers, client approval history | Second conditional requirement from CEOs |
| M2 | Scheduler live for 3 design partners: FB, LinkedIn, Instagram, Twitter (4 of 14) | First real posts shipped via SIGNAL |
| M2 | Historical post analysis: import last 90 days per brand, LLM extracts voice + performance signals | Closes the "historical analysis" condition |
| M3 | Analytics dashboard: engagement by brand, post performance vs. drafts, approval cycle time | Closes the "analytics" condition |
| M3 | Remaining 10 platforms: TikTok, Pinterest, YouTube, Reddit, Threads, Mastodon, Bluesky, GMB, WhatsApp, Snapchat | Closes the "14 platforms" condition |
| M4 | Full conditional-yes checklist complete: scheduler + AI plans + brand cycles + historical analysis + analytics | $300 conversion conversation begins |

Note on M3–M4 platform count: OAuth complexity per platform varies significantly. TikTok and YouTube are high-complexity (review processes, rate limits). Prioritize by which platforms the 3 CEOs' client brands are actually on — confirm this in the open questions below.

### Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Draft quality is mediocre — brand voice doesn't land | Medium | Critical | Build brand ingestion first. Test against at least 3 real historical posts from the demo brand before the CEO sees anything. If it fails internal test, reschedule demo — do not show a bad draft. |
| 3 CEOs go cold after V0.1 (don't wait 4 months for Phase 1) | Medium | High | Set expectations before demo: "This is the strategist. Scheduler ships in month 1. Here's the roadmap." Get written commitment to stay in design-partner program. |
| Solo dev bandwidth — nights/weekends, 14-day deadline | High | High | V0.1 is 3 requirements: brand ingestion → LLM draft chain → Slack/email delivery. That is it. Every other idea goes on a parking lot list. Founder must enforce their own scope. |
| Postiz fork complexity in Phase 1 — OAuth per platform adds 1–2 weeks per major platform | Medium | Medium | Start Postiz fork in month 1 in parallel with Phase 1 strategist deepening. Do not wait until month 3. |
| Brand kit format is undefined — PDF? Notion? URL? | High | Medium | Resolve in first open question below. V0.1 can accept a text paste or a Google Doc link. Do not build a file parser for the demo. |

### Open questions for the founder (ranked by what blocks the next 7 days)

1. **Which of the 3 design-partner agencies are we using for V0.1, and what brand?** This is the demo brand. We need their brand kit (even a rough one) and 30 days of post history by day 3 of the 14-day window. If we don't have this by day 3, we can't validate draft quality before the demo. DRI: founder.

2. **What format does the brand kit exist in today?** PDF, Notion doc, Google Drive folder, or "it's in someone's head"? The answer determines the ingestion interface for V0.1. A text paste works for the demo. A file parser does not get built in 14 days. DRI: founder (ask the agency CEO).

3. **Which of the 14 platforms do the 3 CEOs' client brands actually use?** The Phase 1 platform priority list should be driven by their actual client roster, not the full 14. If 80% of their brands are on FB + LinkedIn + Instagram, we ship those 3 first. TikTok OAuth hell comes later. DRI: founder (ask all 3 CEOs in first post-demo call).

4. **Slack approval loop — does the agency CEO have a Slack workspace we can add a bot to, or is email the fallback for V0.1?** This is a 2-day implementation decision. Slack bot is cleaner but requires OAuth setup. Email is ugly but ships in 4 hours. For a demo, email may be the right call — but confirm before building. DRI: founder.

5. **What LLM are we using for the draft chain?** Claude (already on Max plan — zero marginal cost for V0.1), GPT-4o, or Gemini? Claude is the obvious call given the Max subscription. Confirm this is the decision and close it today. DRI: founder.
