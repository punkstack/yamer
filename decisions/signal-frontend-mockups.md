# SIGNAL — Frontend Mockups Design Rationale
Date: 2026-05-21
Author: staff-frontend (Mia)
Status: Ready for founder pick

---

## Three Variants Summary

| Aspect | v1-cockpit | v2-canvas | v3-inbox |
|---|---|---|---|
| Home screen | Dashboard table | Weekly board (cards) | Packet inbox (3-pane) |
| Primary interaction | Table + keyboard shortcuts | Card board + bulk buttons | Inbox triage + approve |
| Information density | High | Medium | High (different shape) |
| Best for user mindset | Power-user triage | Strategic review / demo | Email-native triager |
| Mobile fit | Card fallback | OK | Poor (needs width) |
| Demo-readiness for CEO B | Good | Best | Good |
| Design reference | Linear + Superhuman | Notion + Figma canvas | Superhuman + Front |
| Accent colour | Indigo (#6366f1) | Amber (#d97706) | Violet (#7c3aed) |

---

## Design Decisions Made

### Navigation model

All three variants use a left sidebar for brand switching, not a top tab bar. Rationale: agencies with 8+ brands need persistent navigation that does not push content. A top tab bar at 8 brands is illegible. The sidebar handles 50 brands with a scroll. This matches Linear and Notion's model — proven at scale.

### Review grid structure

Chosen: channels as rows, days as columns. Alternative considered: days as rows, channels as columns. Channels-as-rows is correct because: (1) Priya thinks channel-first in approval ("what does the Instagram line look like this week"), (2) channel icons make rows visually scannable, (3) empty slots (no LinkedIn on Wednesday) are a non-event in a column, not a gap in a row. Reference: Buffer's calendar grid uses the same orientation.

### Monday packet email

Kept as a true email preview — not reimagined as in-app notification. The vision doc is explicit: email is the delivery channel, the web app is the workspace. The email HTML preview in all three variants matches this split. The "Open in SIGNAL" CTA bridges the two without confusion.

### LOW CONFIDENCE badge placement

Every LOW CONFIDENCE post gets a badge in the cell/card and inside the edit modal. It is never hidden, never dismissible until the post is edited or deleted. This enforces the spec: "LOW CONFIDENCE posts are visually differentiated in the review grid — never suppressed." Yellow border on the left of the cell (cockpit) or amber card border (canvas/inbox) makes scanning fast.

### AI image generation states

Three states shown: (1) Generating — spinner + copy of art direction brief, (2) Generated — image placeholder with Regen button, (3) Swapped — upload indicator. The regen counter (0/3) is visible in all edit modals. After 3 regens the post is flagged for human asset creation. This matches the vision spec exactly.

### RBAC demonstration

All three variants show the same RBAC truth in two places: (1) the users table (who has what role on which brands), (2) the permission matrix (what each role can and cannot do). The Reviewer seat (Meera K.) is demonstrated as a separate screen with no sidebar, no navigation, and no access to anything beyond Grassroot's review grid. The advisory-accept distinction is shown via a callout: "Your approval is advisory — the agency PM schedules."

### Comments inbox structure

v1 and v3 use the Superhuman three-pane model for comments. v2 uses a three-column card layout. All three implement the vision spec's triage buckets: gratitude batch (bulk approve with variants), questions (drafted reply + approve), negative (flagged red, no auto-draft, manual write required). The "Approve all 162 gratitude replies" button is the key moment — it demonstrates the AI's value in 1 click.

### Monthly report editor

All three show contenteditable fields for the report sections, with `[AGENCY: insert]` placeholders highlighted in amber. The spec is explicit: SIGNAL never fabricates numbers. The export DOCX button is present on all variants. "Preview letterhead" shows the agency can brand the output before sending.

### Notion/Google Slides import

Shown in the intake wizard (Step 4) across all three variants as a secondary import option alongside PDF. Presented as "paste a URL" — no OAuth, no complex integration UI. This matches the founder's addition to scope. Implementation detail is deferred.

---

## Open Questions Tagged for Dev Kickoff

`[OPEN: dev-kickoff]` **LinkedIn channel display.** LinkedIn Partner Program application is pending. The channel is shown as active in the UI (settings, schedule windows, channel icons). The dev team needs to decide: show LinkedIn as greyed/pending until API access is confirmed, or show it as active and manually gate the publish button. Showing it greyed in the production UI communicates a broken product during CEO B's demo. Showing it active and blocking at publish is more honest. DRI: Founder + Raj. Deadline: before dev kickoff.

`[OPEN: dev-kickoff]` **Mobile layout for review grid.** All three variants show a card-stack mobile fallback for the review grid. The exact breakpoint (e.g., <768px collapse to cards) and the card interaction (swipe-to-accept vs. tap-to-open-modal) are not specified in mockups. DRI: Mia. Resolved in implementation sprint.

`[OPEN: dev-kickoff]` **Reviewer magic link expiry UX.** The client reviewer screens in all three variants do not show an expiry state. If Meera K.'s link expires mid-session, the UI needs a clear "link expired — request a new one" state. Not designed — deferred. DRI: Raj.

`[OPEN: dev-kickoff]` **Notion/Slides import implementation.** The intake wizard shows a "paste a URL" import field for Notion and Google Slides. The actual extraction logic (public Notion API, Google Slides export API, or just scraping the public URL) is not spec'd. DRI: Raj. Do not build until decided.

`[OPEN: dev-kickoff]` **Post preview rendering (platform chrome).** The vision spec raises the question of showing posts as they would appear on Facebook or Instagram (with platform chrome, profile picture, etc.). None of the three mockups implement this — posts are shown as plain text + image. Implementing mock platform UI per channel is valuable for the Reviewer seat (Meera K. is not social-media-native). Scope TBD. DRI: Mia + Raj.

`[OPEN: dev-kickoff]` **Bulk schedule UX confirmation.** All three variants have a "Bulk Schedule" / "Schedule week" button. The confirmation step before 14 posts are queued for publish is not designed. Options: (a) modal confirmation with post count, (b) undo toast after action, (c) no confirmation (trusting the accept step). The vision spec says scheduling requires accepted posts — so the gate is upstream, not at this button. DRI: Mia.

`[OPEN: dev-kickoff]` **Image generation provider placeholder.** All three variants show AI image generation states (generating/generated/swapped). The actual provider (DALL-E 3, Ideogram, Flux) is `[OPEN-IMG-1]` from the vision doc. The UI is provider-agnostic — provider choice does not affect the mockup design. DRI: Raj.

---

## Screens Coverage Check

| Screen | v1-cockpit | v2-canvas | v3-inbox |
|---|---|---|---|
| 1. Guided intake (6Q + PDF + free-text + Notion import) | S2 | S2 | S4 |
| 2. Monday packet email | S3 | S3 | S5 |
| 3. Web review grid (Accept/Draft/Delete/Edit + bulk) | S4 | S4 | S2 (right pane) |
| 4. Per-post edit modal (caption + AI image) | S5 (modal) | S5 (modal) | S3 (modal) |
| 5. Multi-brand dashboard | S1 | S1 | S7 |
| 6. RBAC (Admin/Editor/Reviewer + client seat) | S10 + S11 | S10 + S11 | S11 + S12 |
| 7. Comments/inbox (triage, bulk approve, negative flag) | S6 | S6 | S6 |
| 8. Monthly report editor | S7 | S7 | S8 |
| 9. Performance loop view | S8 | S8 | S9 |
| 10. Settings (brand voice, channels, schedule windows) | S9 | S9 | S10 |
| 11. Notion/Slides import in intake | S2 | S2 | S4 |

All 11 features covered in all three variants.

---

## My Recommendation

**v1-cockpit** for the agency PM (Priya) as primary actor.

The cockpit's table grid is the most direct match for Priya's actual work: she needs to see all 14 posts across 4 channels in one view, take action, and move to the next brand. The canvas board (v2) requires scrolling to see all days; the inbox (v3) requires navigating between panes. Both add friction to a task that is fundamentally about speed.

**Caveat:** If CEO B is sitting next to the founder during the demo, v2-canvas may read better as a "premium product" to a non-daily user. Consider showing v2-canvas to CEO B as the first impression, then switching to v1-cockpit when Priya walks through her Monday routine.

**For founder's review:** Pick A (cockpit), B (canvas), or C (inbox). The pick locks the UX doc for implementation. Any mix ("A's grid but B's colour palette") is a valid note for implementation but does not require re-mocking.
