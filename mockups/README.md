# SIGNAL — UI Mockups

Three self-contained clickable HTML files. Open each in Chrome, compare in three tabs. All 11 features are present in every variant. Realistic data throughout — Grassroot / Anita Dongre / Priya / Meera K. No lorem ipsum.

---

## v1-cockpit — Linear/Superhuman keyboard-first dense

**File:** `v1-cockpit/index.html`

**Who it is for:** Priya on her desktop at 9 AM, handling 8 brands with zero slack time. She navigates with J/K/A/D/E keyboard shortcuts. She expects dense information, not whitespace. She has used Linear, Notion, and Superhuman — she knows what a good power tool looks like.

**Design DNA:** Linear sidebar + Superhuman dense list. Dark indigo sidebar for brand navigation. Table-style review grid with channel rows and day columns — every slot visible at once. Bulk toolbar is always present. Keyboard shortcuts shown inline. Nothing hidden behind a hover.

**References:** Linear's issue list density. Superhuman's triage toolbar. Stripe Dashboard's status tables.

**Biggest tradeoff:** The review grid demands screen width — on a 13" laptop at 100% zoom it is tight. Mobile is a card stack fallback, not a first-class experience. The Monday commute check on mobile is deprioritised. This variant bets Priya does her real work at a desk.

---

## v2-canvas — Notion/Figma calm board

**File:** `v2-canvas/index.html`

**Who it is for:** Priya in a considered mindset — Monday morning with a coffee, reviewing strategy before diving into actions. Also the CEO B demo moment: a clean, beautiful board that reads as "premium tool" in 5 seconds of looking.

**Design DNA:** Warm off-white background (#f8f7f4). Rounded cards. Amber/gold accent colour (vs. indigo in v1). Brand chips across the top for switching. Weekly board as the home — 5-day columns, each post is a card. Notion-style contenteditable fields in the report editor.

**References:** Notion's block-based editor feel. Figma's canvas warmth. Linear's card system for the board.

**Biggest tradeoff:** Lower information density means more scrolling. An 8-brand agency PM in full triage mode will find it slower than the cockpit. The board layout works for one brand at a time — the multi-brand view is a separate chips-based switcher, not a single unified table. Also the warmest UI for a demo with CEO B who wants to feel "this is a quality product."

---

## v3-inbox — Superhuman/Front inbox-zero metaphor

**File:** `v3-inbox/index.html`

**Who it is for:** Priya who thinks of her job as triage. She processes her Monday inbox the way she processes email. The Monday packet IS the inbox item. She opens it, triages each post, closes the item. Inbox zero = week scheduled.

**Design DNA:** Three-pane layout: dark left nav (brand/view switcher), middle pane (packet list — one row per brand per week), right pane (detail + actions). Same visual grammar as Superhuman and Front. Dark sidebar creates contrast. The comments inbox follows the same three-pane pattern — so muscle memory transfers from packet review to comment triage.

**References:** Superhuman's three-pane layout and keyboard-first navigation. Front's brand switching model. Linear's dark-sidebar-plus-content pattern.

**Biggest tradeoff:** The three-pane layout requires ~1200px+ width to breathe. On smaller screens the middle pane compresses. Also: users who don't think in "inbox" terms will find the metaphor non-obvious — a brand manager used to Hootsuite or Buffer's calendar view may feel disoriented. This is the most opinionated variant.

---

## My pick: v1-cockpit

Priya is a power user handling 8 brands under time pressure. She is not browsing. She is triaging. The cockpit's density-first grid matches her actual mental model — "what needs my attention, on which channel, for which day" — more directly than a board (v2) or inbox (v3). The keyboard shortcuts shorten the Monday review from 20 minutes to 12. The inline bulk toolbar removes confirmation steps. For the CEO B demo, the dashboard table makes the multi-brand problem feel solved in one glance.

v2-canvas is the better choice if CEO B is the primary demo viewer (warmer, more impressionistic, feels premium). v3-inbox is the right call if we learn that Priya already processes her Monday in an email-like mental model — test this with 2 user interviews before committing.
