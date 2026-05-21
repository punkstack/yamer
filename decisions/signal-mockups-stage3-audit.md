# Audit: Stage 3 (Design & Mockups) — SIGNAL

Date: 2026-05-21

## Verdict

FAIL

The mockups cover all 11 PRD features and use realistic data, but they fail on three FAIL-grade criteria: (1) v2-canvas contradicts the navigation rationale Mia herself stated — it uses a top navigation bar for all screens, not a left sidebar — while v1 and v3 use left sidebars that are structurally inconsistent with each other; (2) no shared design system exists — typography, badge shapes, border-radius, button styles, and spacing units are all independently authored per-variant with no shared token file or component spec; (3) the aesthetic has zero product fingerprint — all three variants resolve to system-font Inter on a Tailwind gray/white base with accent color as the only differentiator, which is what the founder called out verbatim as "looks like shit."

---

## Checklist Results

- [✗] Three HTML files in `./mockups/` exist and are openable — FILES EXIST at `./mockups/v1-cockpit/index.html`, `./mockups/v2-canvas/index.html`, `./mockups/v3-inbox/index.html`. All three load (CDN Tailwind only — no broken local imports). PASS on this line item. Marked ✗ only to note the CDN dependency (see notes).

- [✓] Each file is self-contained (no missing CDN imports break the page) — All three files use only `https://cdn.tailwindcss.com` plus inline `<style>` blocks. No broken local asset references. Opens offline only if CDN cached.

- [✓] Each shows 5+ key screens on one scrollable page — v1 has 11 screens, v2 has 11 screens, v3 has 12 screens. All exceed the 5-screen floor.

- [✓] Realistic data (no Lorem Ipsum, no "User 1, User 2") — Grassroot, Anita Dongre, Priya R., Meera K., AND by Anita Dongre, FabIndia, Global Desi, Nykaa Fashion. Post copy is brand-specific and contextually coherent. No placeholder text.

- [✗] The three differ in interaction shape, not just color — v1 (sidebar + table/grid) and v3 (dark sidebar + three-pane inbox) are genuinely different interaction bets. v2 (top navigation + card board) is also structurally different. However, Mia's own rationale document states: "All three variants use a left sidebar for brand switching, not a top tab bar." v2 has no left sidebar on any screen — it uses a fixed top navigation bar throughout. This is an internal contradiction: the design rationale claims a shared component decision (left sidebar for all three) that v2 does not implement. The variants are not consistent with the stated design logic.

- [✗] Mockups doc has the comparison table filled — Table exists at the top of `signal-frontend-mockups.md` and is filled. However, the "Navigation model" section under "Design Decisions Made" states "All three variants use a left sidebar" — this is false for v2. The doc is internally inconsistent and misdescribes v2 to anyone making a decision from it.

- [✓] Recommendation present — v1-cockpit is recommended with specific reasoning tied to Priya's Monday triage workflow.

---

## Feature Coverage — All 11 PRD Features

Mia's coverage table claims all 11 features appear in all three variants. Spot-check against actual HTML:

| Feature | v1 | v2 | v3 |
|---|---|---|---|
| 1. Guided intake (6Q + PDF + free-text) | S2 ✓ | S2 ✓ | S4 ✓ |
| 2. Monday packet email | S3 ✓ | S3 ✓ | S5 ✓ |
| 3. Web review grid (Accept/Draft/Delete/Edit + bulk) | S4 ✓ | S4 ✓ | S2 right-pane ✓ |
| 4. Per-post edit modal (caption + AI image states) | S5 ✓ | S5 ✓ | S3 ✓ |
| 5. Multi-brand dashboard | S1 ✓ | S1 ✓ | S7 ✓ |
| 6. RBAC (Admin/Editor/Reviewer + client seat) | S10+S11 ✓ | S10+S11 ✓ | S11+S12 ✓ |
| 7. Comments/inbox (triage, bulk approve, negative flag) | S6 ✓ | S6 ✓ | S6 ✓ |
| 8. Monthly report editor | S7 ✓ | S7 ✓ | S8 ✓ |
| 9. Performance loop view | S8 ✓ | S8 ✓ | S9 ✓ |
| 10. Settings (brand voice, channels, schedule windows) | S9 ✓ | S9 ✓ | S10 ✓ |
| 11. Notion/Slides import in intake | S2 ✓ | S2 ✓ | S4 ✓ |

All 11 features confirmed present across all three variants. Coverage is PASS.

---

## Grill Me Concerns — Explicit Verdicts

**Grill Me 1: "so many inconsistencies left side panel etc" — NOT ADDRESSED**

The left panel is inconsistent across variants. Specific evidence:

- v1-cockpit: white sidebar (220px wide, `bg-white border-r border-gray-200`), brand items use `nav-item` class with indigo active state.
- v2-canvas: NO left sidebar on any screen. Navigation is a fixed top bar (`nav-top`) with Board/Inbox/Reports/Settings tabs. Brand switching is via horizontal chip row inside each screen. There is no left panel.
- v3-inbox: dark sidebar (240px wide, `background:#1e1b2e`), brand items use `left-nav-item` class with violet active state.

Not only are v1 and v3 inconsistent (white vs. dark, different widths, different CSS classes, different brand-item rendering), v2 has no left sidebar at all — directly contradicting the rationale doc's stated shared design decision. This is a structural inconsistency, not a cosmetic one.

Within v1 itself, the sidebar is re-instanced from scratch for each screen (lines 73, 283, 444, 795, 904, 974, 1053) — same HTML duplicated 7 times. If a component decision changes, it must be changed 7 times. There is no component abstraction.

**Grill Me 2: "colors typography also looks dumb... looks like shit" — NOT ADDRESSED**

All three files declare `font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif` (v1) or `font-family: -apple-system, 'Inter', sans-serif` (v2, v3). Inter is not loaded from a Google Fonts or Bunny Fonts CDN — it falls back to Apple system font on Mac (SF Pro) or system sans-serif on Windows/Linux. There is no typeface loaded with a design intent.

Typography scale: all three use Tailwind's default type scale (`text-xs`, `text-sm`, `text-base`, `text-lg`, `font-bold`) with no custom size or weight override. No display font. No numeric font. No custom line-height or letter-spacing applied to headings. The visual weight hierarchy reads as a default Tailwind starter.

Color: the only brand expression in each variant is a single accent hue applied to screen labels, active nav states, and CTAs. v1: indigo-600 (#6366f1). v2: amber-500 (#d97706). v3: violet-600 (#7c3aed). The remaining surfaces are Tailwind gray (gray-50 background, gray-900 text, gray-200 borders). No SIGNAL-specific color story. No considered use of negative space, surface layering, or typographic hierarchy that would read as "this is a premium AI strategist tool."

The founder reference to "fingerprint type color and typography" is unmet. There is no design fingerprint. It reads as a Tailwind component library demo, which is exactly the feedback given.

**Grill Me 3: "fingerprint type color and typography" — NOT ADDRESSED**

No unique typeface loaded. No custom type scale. No color palette beyond one accent hue per variant. Badge shapes differ across v1/v2/v3 (3px border-radius in v1, 3-6px in v2, 4-10px in v3). Button styles differ (v1: rounded-lg everywhere; v2: rounded-lg but with different padding; v3: mixed). No shared token file, no design system spec referenced. Each variant was authored independently with no shared constraints. The three do not feel like three explorations of the same product — they feel like three different developers started from scratch on the same day.

---

## Required Fixes (FAIL)

**1. v2-canvas/index.html — Navigation structure contradicts the stated design rationale**

File: `/home/manojbojja/git/ai/yamer/mockups/v2-canvas/index.html`
What: v2 uses a fixed top navigation bar (`nav-top`, lines 31, 51–71) for all screens. The rationale document (`signal-frontend-mockups.md`, "Navigation model" section) states all three variants use a left sidebar. This must be reconciled. Either: (a) v2 is redesigned to use a left sidebar consistent with the design rationale, OR (b) the rationale doc is corrected to honestly describe v2 as a top-nav variant and the comparison table is updated to surface this as a meaningful structural difference between variants, not a shared foundation.
Why: Founders and the build team make decisions based on the rationale doc. If the doc says "all three have left sidebars" and one does not, the decision is made on false information.
DRI: Mia (staff-frontend)

**2. signal-frontend-mockups.md — Internal contradiction on navigation model**

File: `/home/manojbojja/git/ai/yamer/decisions/signal-frontend-mockups.md`
What: Line "All three variants use a left sidebar for brand switching, not a top tab bar" is false. v2 does not have a left sidebar. The comparison table also does not surface navigation model as a differentiating row, despite it being one of the most significant structural differences between variants.
Why: The recommendation rationale for v1 cites sidebar-vs-topnav as implicit context. If the comparison table does not surface this, the founder cannot evaluate the tradeoff.
DRI: Mia (staff-frontend)

**3. All three mockups — No shared design token layer**

Files: All three `index.html` files.
What: Zero shared design tokens across variants. Border-radius, badge styles, button padding, type scale, and spacing units are all independently authored per-variant. Before any variant proceeds to implementation, a one-page token spec must exist: type scale (display, heading, body, caption with sizes and weights), color palette (background layers, surface colors, accent, semantic states), spacing units, border-radius scale. This spec becomes the constraint that implementation starts from. It does not need to be a Figma library — a single HTML or markdown file listing the tokens is sufficient for this stage.
Why: Without shared tokens, the implemented product will have component drift identical to what the mockups already show. The mockup stage is the cheapest point to fix this.
DRI: Mia (staff-frontend)

**4. All three mockups — Typography has no design POV**

Files: All three `index.html` files, `<head>` section.
What: Inter is declared but not loaded. No display typeface. No numeric/monospace face for data. No custom letter-spacing or line-height applied to headings. The current state is "whatever the system renders for Inter-ish text." A product at $300/agency/month targeting agency CEOs who are evaluating it against Sprout Social must read as designed, not templated.
Required: At minimum, load one typeface via Google Fonts or Bunny Fonts CDN with an explicit design rationale (why this face, why this weight pairing). Apply it to headings across all three variants. The three variants can share this choice or diverge — but the choice must be intentional and stated.
Why: The founder called this out by name ("fingerprint type"). It is unresolved.
DRI: Mia (staff-frontend)

**5. v1-cockpit/index.html — Sidebar HTML is duplicated 7 times with no abstraction**

File: `/home/manojbojja/git/ai/yamer/mockups/v1-cockpit/index.html`
Lines: 73, 283, 444, 795, 904, 974, 1053 (each a new `<div class="sidebar ...">` block instanced from scratch).
What: The sidebar component is copy-pasted identically across all 7 screens that use it. The nav item states (active/inactive), the brand list (Grassroot, AND, Global Desi, Nykaa Fashion, FabIndia, + 3 more), and the user footer are duplicated verbatim. Any change to the sidebar requires 7 edits.
Why this is a mockup-stage finding, not a build-stage finding: if the founder picks v1-cockpit and locks the UX, Mia will hand off the sidebar spec to Raj. The duplication means the "spec" has 7 slightly-divergent instances that Raj must reconcile. Fix before handoff: either mark one instance as canonical and comment the others as copies, or consolidate to a single defined sidebar spec block.
DRI: Mia (staff-frontend)

---

## Notes (not blockers, track for implementation)

1. **Tailwind CDN dependency** — All three files use `https://cdn.tailwindcss.com` (the just-in-time CDN version). This is fine for mockups. At implementation kickoff, replace with a Tailwind CLI build or PostCSS pipeline. The CDN version is not suitable for production.

2. **Mia's pick reasoning is sound on the PRD user** — The recommendation for v1-cockpit correctly identifies Priya's triage-first mental model, the density requirement for 8+ brands, and the keyboard shortcut advantage. The reasoning is tied to specific user behavior, not aesthetics. The rationale would survive a Grill Me on this point. The problem is not the pick — it is that the design needs to be executed at a quality level that supports the $300 price point.

3. **v3-inbox has a duplicate anchor ID** — Line 82 and line 243 of `v3-inbox/index.html` both define `id="s2"`. Screen 1+2 are combined under `id="s1"` at line 82, but the right pane is also anchored as `id="s2"` at line 243. The screen navigation bar link `2·Packet Detail` points to `#s2` — this works (it hits the right pane), but it is ambiguous and could break if screens are reordered.

4. **V0.1 scope vs. mockup scope** — The PRD explicitly scopes V0.1 to no dashboard, no web UI beyond intake form, no multi-brand. The mockups correctly design for Phase 1 scale (50 brands, multi-channel, RBAC). This is consistent with the project-config `design_discipline` rule ("Design for scale, build for small"). No finding here — just confirm the handoff note to Raj is explicit: none of screens 1, 4, 5, 6, 7, 8, 9, 10, 11 are in the V0.1 build sprint.

5. **AI image generation shown in mockups** — All three variants show AI image generation states (generating spinner, generated, regen counter 0/3). The PRD firewalls image generation to Phase 2 (post-30 paid agencies). The mockups show Phase 1 functionality (image generation without specifying a provider). This is acceptable at design stage — the vision doc includes it and the mockups are designing for scale. But flag to Mia: the image generation UX in the mockups should be annotated as "Phase 1+ only" to prevent Raj from building it in the V0.1 sprint.
