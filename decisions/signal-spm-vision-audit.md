# Audit: Vision — SIGNAL
Date: 2026-05-21

## Verdict
PASS-WITH-NOTES

The Vision doc is substantive, specific, and detailed enough for Mia to start mockups — with three scope-adjustments noted below that must be resolved before design begins on Features 3, 6, and 8.

---

## Checklist Results

- [✓] **One-line vision present, <=15 words, no buzzwords** — "AI agency strategist that drafts, schedules, and reports every brand, every Monday." (14 words, pitch-trimmed version; full version is 22 words but the doc self-identifies this and provides the 14-word cut). Passes.

- [✓] **Personas named with job/company/country specificity** — Priya (Agency PM, Mumbai, mid-market agency, 8 brands, uses Notion + Buffer + ChatGPT + WhatsApp), CEO B (agency CEO, 10–30 brands, buyer), Anita's Marketing Head (client-side reviewer, House of Anita Dongre, composite). All three are specific enough to design for. Passes.

- [✓] **All 11 locked features deeply spec'd** — All 11 features have: what-it-is, user-moment-it-enables, UX surfaces list, per-post/per-action detail, and at least one [OPEN] item correctly tagged. Features 1–11 are present and specced at a level above PRD depth. Passes.

- [✓] **RBAC matrix present and unambiguous** — Section 8 (vision.md:783–838) contains a full permission matrix: 40+ actions × 3 roles (Admin/Editor/Reviewer), each cell Y/N/R. Two open items are correctly tagged within the feature spec (Reviewer acceptance advisory vs. schedule-trigger; magic link expiry). The matrix itself is not ambiguous. Passes.

- [✓] **Data model sketch + IA present** — Section 7 (vision.md:624–775) contains a 15-entity data model with foreign keys, field names, and state enums. Section 6 (vision.md:583–616) contains a full IA tree for both agency-side and reviewer-side navigation. Passes.

- [⚠] **[OPEN] items tagged for dev-kickoff** — Four required open items from the audit brief:
  - Image gen provider: tagged as [OPEN-IMG-1] with DRI (Raj). PRESENT.
  - FB/IG/LI API approvals: Instagram App Review tagged [OPEN-API-2] with DRI (Founder) and deadline "Day 1 of dev kickoff". LinkedIn Partner Program tagged [OPEN-API-1] with DRI (Founder) and deadline "before dev kickoff". PRESENT.
  - Comment polling cadence: tagged [OPEN-INBOX-1] with DRI (Raj). PRESENT.
  - Voice-cloning data minimums: NOT PRESENT. The vision doc does not reference voice cloning anywhere. The checklist asked for this item; it is absent. Likely a non-applicable item given SIGNAL does not include audio features — but the brief explicitly listed it. Flag for Chief of Staff to confirm whether this was a stale checklist item or an intentional omission.

- [⚠] **Kill criteria still intact from PRD** — The PRD's kill criteria (Day-60: 3 paid agencies × $300 by 2026-07-20; EOY win metric: 30 agencies × $300 = $9K MRR by 2026-12-31; pivot/kill if <10 paid by 2026-09-30) are NOT reproduced in the Vision doc. The Vision doc is written as a full-scale design brief and intentionally defers cost/phase decisions to dev kickoff — this is consistent with state.md. However, the kill line from the PRD (specifically the <10 paid by 2026-09-30 trigger) is not referenced anywhere in the Vision, creating a gap: Mia and Raj will read this doc without knowing the conditions under which the product stops. Not a design-blocker, but a tracking omission.

- [✓] **Sample Monday packet artifact present and concrete enough for Mia** — Section 3 (vision.md:44–165) contains a full, named, real-world packet for "Anita Dongre / Grassroot — Week of 26 May 2026" with: strategic header, per-day per-channel copy (Facebook, LinkedIn, Instagram, Threads), inline rationale, performance loop signal from last week, and a complete monthly report draft. Copy is non-placeholder — it reads as real Grassroot content with specific engagement figures and brand reasoning. Mia can design directly from this. Passes.

- [⚠] **Scope creep vs PRD — new items not in the 11-feature lock**
  The following items appear in the Vision that were not in the PRD's 11-feature lock or the locked out-of-scope list:
  1. **Threads as a first-class publishing channel** (vision.md:200, 323, 329) — PRD V0.1 locked FB + LinkedIn only. Vision promotes Threads to first-class alongside Instagram. This is a V1 scope expansion, not a Phase 2 item.
  2. **Instagram as a first-class publishing channel** (vision.md:200–211, 316–323) — PRD V0.1 explicitly locked "Facebook + LinkedIn only." The Vision doc treats Instagram as co-equal first-class from Feature 2 onward. Instagram App Review adds 2–4 weeks to dev timeline (cited at vision.md:346). This is the largest scope delta from the PRD.
  3. **AI-generated visuals (Feature 3)** — PRD Section 4, hard out-of-scope item 8: "Image generation. Not in V0.1, not in Phase 1. Phase 2 only, firewalled until 30 paid agencies." The Vision treats AI visuals as a V1 feature fully specced. This directly contradicts the PRD firewall. The Vision doc's status header acknowledges "Full-scale Vision — no V0.1 scope cuts. Phasing deferred to dev kickoff." The conflict is intentional but must be surfaced explicitly at dev kickoff. Mia should be told: do NOT design AI Visuals for the V0.1 slice — design it for the full product mockup only, and it will be cut at kickoff.
  4. **Comments Inbox (Feature 10)** — Was in the 11-feature lock per state.md. Passes.
  5. **WhatsApp delivery** — Flagged as Phase 2 within the doc itself (vision.md:270). Not scope creep — correctly tagged.

- [⚠] **Migration story (Notion/Slides import)** — Founder's partial G3 answer added "Notion + Google Slides import added to scope (migration path)." The Vision doc mentions Priya uses Notion (persona description, vision.md:22) and that clients currently receive Google Slides (vision.md:28), but there is no import feature specified anywhere. No intake step asks to ingest a Notion doc. No [OPEN] item tags this. The PRD hard out-of-scope list explicitly includes: "Notion / Drive / Slack integration for brand kit ingestion." The G3 partial answer that reportedly added this to scope is not reflected in the Vision. This is a conflict between founder's stated scope and the written doc. MEDIUM finding — not a design blocker for Mia, but must be resolved before intake (Feature 1) is designed or built.

- [✓] **No "we'll figure it out later" hedges in the doc** — All ambiguous items are tagged [OPEN] with a stated DRI and a decision venue ("at tech kickoff"). No unattributed deferrals. The doc's [OPEN] pattern is disciplined: every open item names who decides and when. Passes.

---

## Grill Me Deferrals (High — Non-Blocking, Founder Accepted)

**HIGH — G1/G2/G3 on original PRD v1 (deferred 2026-05-21, first instance):**
Founder declined the standard pre-audit grill on PRD v1. Chief of Staff logged as debt. The assumptions most likely to surface from a G1 ("weakest assumption") on the PRD were: (a) that 3 conditional-yes CEOs are representative of the broader ICP; (b) that brand-voice quality is achievable with the intake spec as written. Neither has been stress-tested by the founder on record.

**HIGH — G1/G2/G3 on Vision doc (deferred to "prototype review", second instance):**
Founder declined the pre-audit grill a second time on this Vision doc, deferring to prototype review. Two weeks of Mia's design work will proceed without the founder having answered on record: (a) which assumption in the Vision they are least sure about; (b) which sentence in the doc is the most likely failure point; (c) what this design will conflict with that hasn't been discussed. These are non-blocking per founder's explicit acceptance of the risk — but they remain open debt. If the prototype review reveals a structural design problem, the cost of redesign will be higher than if G1/G2/G3 had been run before Mia started.

Both deferrals are logged here as High. They do not change the verdict to FAIL.

---

## Required Fixes
None — verdict is PASS-WITH-NOTES.

---

## Notes (PASS-WITH-NOTES)

1. **Scope delta: Instagram + Threads as first-class channels (vision.md:200, 316–329).** The PRD locked V0.1 to "Facebook + LinkedIn only." The Vision doc promotes Instagram and Threads to first-class publishing with full OAuth, App Review dependency, and native scheduling. This is a deliberate full-scale Vision scope expansion — but Mia must be explicitly told which channels are in the V0.1 design slice vs. the full-product mockup. Recommendation: at dev kickoff, Raj and Founder must decide whether Instagram is in V1 or V2. Until then, Mia designs for all four channels in the full mockup but the V0.1 slice indicator should be documented separately. DRI: Founder. Deadline: before dev kickoff.

2. **Scope conflict: AI Visuals (Feature 3) vs. PRD firewall (vision.md:223–243 vs. prd.md:57).** PRD explicitly firesalled image generation to "Phase 2 only, firewalled until 30 paid agencies." Vision treats it as a V1 feature with full spec. The Vision's status header acknowledges this is by design — but Mia needs a clear signal: design Feature 3 for the full-product mockup; it will be cut to Phase 2 at dev kickoff unless Founder explicitly unlocks it. Without this instruction, Mia may invest design time on a feature the PRD firewalled. DRI: Founder. Action: state explicitly in Mia's brief whether Feature 3 is included in the V0.1 design slice.

3. **Kill criteria absent from Vision doc.** The PRD's Day-60 kill line (3 paid agencies by 2026-07-20) and EOY win metric (30 agencies × $300 = $9K MRR by 2026-12-31) are not referenced in the Vision. Design teams building toward a feature set should know what the product has to achieve to survive. Not a Mia-blocking issue, but Raj and Neha at kickoff should have the kill line in the room. Recommendation: Chief of Staff adds a "Success and kill criteria" section stub to the dev kickoff agenda.

4. **Migration story gap (Notion + Slides import).** Founder's G3 partial answer reportedly added "Notion + Google Slides import" to scope. The Vision doc does not reflect this anywhere — the PRD's explicit out-of-scope list still prohibits it. If this is genuinely in scope, it affects Feature 1 (intake wizard) UX design — Mia needs to know before designing the intake flow. If it is out of scope (PRD firewall wins), that should be confirmed and the state.md entry corrected. DRI: Founder. Deadline: before Mia briefs Feature 1 intake screens.

5. **Voice-cloning data minimums — checklist item absent from Vision.** The audit checklist required this as a tagged [OPEN] item. The Vision contains no audio or voice-cloning features. Chief of Staff should confirm whether this was a legacy checklist item that doesn't apply to SIGNAL, or whether there is an unwritten feature assumption floating in the founder's head that hasn't been captured. If the latter, it needs to be surfaced before Mia starts.

6. **LinkedIn native publishing is explicitly the highest-risk timeline item (vision.md:344).** [OPEN-API-1] flags LinkedIn Partner Program approval as "months-long, opaque." The Vision lists LinkedIn as a first-class publishing channel with full scheduling spec. If LinkedIn approval is not obtained before V1 launch, Feature 6 (native scheduling) ships with a manual workaround for LinkedIn — which breaks the "no Buffer, SIGNAL is the publisher" disruption stance (vision.md:313–314). Founder must decide before dev kickoff: accept the manual fallback or treat LinkedIn native publishing as a V2 gate. This is not a design-blocker for Mia (she designs for full parity), but it is a launch-blocker Raj needs a decision on.

---

## Recommendation: Can Mia Start Mockups?

**Yes — with scope adjustments communicated explicitly in the brief.**

Mia can start mockups for Features 1, 2, 4, 5, 7, 8, 9, 10, 11 immediately. The Vision doc provides enough specificity for all of these: UX surfaces are named, data states are defined, user journeys are narrated at task level, and the RBAC matrix is unambiguous.

**Three scope-adjustment instructions must be in Mia's brief before she starts:**

1. **Feature 3 (AI Visuals):** Design it in the full-product mockup. Label it "Phase 2 candidate — to be confirmed at dev kickoff." Do not treat it as a V0.1 design slice item.

2. **Channels:** Design all four channels (Facebook, Instagram, LinkedIn, Threads) in the mockup — the full-scale Vision warrants it. But annotate Instagram App Review and LinkedIn Partner Program as "launch dependencies — may ship as manual fallback in V1."

3. **Feature 1 (Intake) — migration path:** Before designing the intake wizard's channel-import step, get a one-line answer from Founder on whether Notion/Slides import is in scope. If yes, add an import step to the wizard. If no (PRD firewall stands), design intake as 6 structured questions + PDF + free-text only.

