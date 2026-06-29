# Lesson page format (the `LESSON` object)

Every lesson is a thin HTML shell that defines a global `window.LESSON` object and
loads the shared engine. The engine (`assets/lesson.js` + `assets/lesson.css`) renders
a mobile-first interactive page with two modes — **Prep** (the night before) and **Run**
(live, day-by-day) — plus a tappable gear checklist, an interactive science journal that
saves to `localStorage`, a question bank, FAQs, and a "Say this" bottom sheet.

To add a future lesson: copy an existing lesson, change the `LESSON` data, pick a theme, and link
it from `index.html`. No build step. For a **Science** lesson copy `lessons/0001-sink-or-float.html`;
for a **Words** (literacy) lesson copy `lessons/L0001-rhyme-time.html` (it shows the words loop, the
`locatorLabel`/`track` overrides, and a `type:"log"` journal). The engine is track-agnostic — the
journal heading defaults to `"Science journal"` but any lesson overrides it via `journal.title`.

## Shell

```html
<head>
  …Google Fonts (Newsreader, Space Mono, Caveat)…
  <link rel="stylesheet" href="../assets/lesson.css">
</head>
<body>
  <div id="app"></div>
  <script>window.LESSON = { … };</script>
  <script src="../assets/lesson.js"></script>
</body>
```

## Fields

| Field | Purpose |
|-------|---------|
| `storageKey` | Unique per lesson, e.g. `"grow-v1"`. Namespaces localStorage. |
| `childName` | Default `"Kai"`. Anywhere copy contains `{name}` it is substituted. |
| `track` | Optional, e.g. `"science"` / `"words"`. Metadata to label the lesson's track; not required by the engine. |
| `index`, `total` | Locator chip, e.g. `2` / `5`. Renders as `PROJECT NN / NN`. |
| `locatorLabel` | Optional. Overrides the `PROJECT NN / NN` locator text — e.g. `"WORDS · LESSON ONE"` for a non-science track. |
| `locatorHome` | Optional. Overrides the locator's back-link text (default `"All projects"`) — e.g. `"All lessons"`. |
| `defaultMode` | `"prep"` or `"run"` (first visit). |
| `title` | `<title>` text. |
| `theme` | Optional map of CSS variables to override, e.g. `{ "--accent": "oklch(56% .13 150)", "--accent-deep": "oklch(46% .14 150)" }`. Gives each lesson its own colour. |
| `hero` | `{ kicker, titleHTML, subHTML, tags:[{text, lead?}] }`. `titleHTML` may use `.lc`/`.rc`/`.joiner` spans for two-tone titles. |
| `loop` | 5 cards: `{ emoji, name, tone }`. The loop is **track-agnostic** — any tone string works; only the card's top-border colour is tone-specific. Styled tones: science `notice\|wonder\|predict\|test\|talk`, words `listen\|wonder\|play\|make\|share` (`assets/lesson.css`). An unstyled tone just falls back to the neutral default border. Optional `loopLabel` overrides the label above the cards. |
| `prepLabel` / `runLabel` | Optional toggle labels `{ main, sub, emoji }`. |
| `win` | `{ label, html }` — the payoff box. |
| `prep.gear*` | `gearKicker`, `gearTitle`, `gearLead`, and `gear:[{id, strong, rest}]` (tappable checklist; `id` must be unique within the lesson). |
| `prep.deepDive` | `{ kicker, eyebrowTone, title, lead, blocks:[{tone, label, html}] }`. tone ∈ `""|test|predict|grow`. The "important part" callout cards. |
| `prep.safety` | `{ label, html }`. |
| `prep.setup` | `{ kicker, title, steps:[…] }` — numbered list. |
| `arc` | `{ kicker, title, lead }` — heading for the day list (rows come from `days`). |
| `days` | Array of `{ n, stars, lead, title, tag, goal, setup, doText, ask:[…], watch:[{icon,text}], done }`. `tag` shows in the arc + stepper context; `lead` is appended after the stars (e.g. `" · he leads"`). |
| `journal` | See below. |
| `qbank` | `{ kicker, title, intro, items:[{moment, say}] }`. |
| `faq` | `{ kicker, title, items:[{q, a}] }`. |
| `footer` | `{ homeHref, teacherHTML, links:[{href, label}] }`. |

### Journal

Two types:

- **`type: "binary"`** — a guess/result pair with two poles (used by Sink-or-Float).
  ```js
  journal: {
    kicker, title, intro, headerTitle, said,        // `said` is a hand-written caption line
    type: "binary", rows: 5, itemPlaceholder: "what we tested",
    poles: { a: {key:"float", icon:"⬆", label:"float"},
             b: {key:"sink",  icon:"⬇", label:"sink"} },
    countLabel: "🔢 floaters {a} · sinkers {b}"      // {a}/{b} fill with live counts
  }
  ```
  Pole **a** renders in the accent colour, pole **b** in the blue `--test` colour.

- **`type: "log"`** — free-text columns per row (used when the record isn't a binary guess —
  e.g. plant height over days, colour mixes, bugs found).
  ```js
  journal: {
    kicker, title, intro, headerTitle, said,
    type: "log", rows: 5,
    columns: [ {key:"item", placeholder:"what"},
               {key:"saw",  placeholder:"what we saw"} ]
  }
  ```

## Authoring notes

- Rich fields (`*HTML`, `html`, `a`, `q`, `say`, `goal`, `setup`, `doText`, `done`, `text`,
  `watch[].text`, `ask[]`, `said`, `intro`, `lead`) may contain inline `<strong>`, `<em>`,
  `<a>`. These come only from the trusted lesson file. Plain fields (`kicker`, `title`,
  `label`, `moment`, `stars`, `tag`) are escaped.
- Use `{name}` for the child's name so the lesson re-themes for other kids.
- Keep copy mobile-tight: heroes ≤ ~30 chars/line, `ask` lines short enough to read aloud.
- Curly quotes are fine and preferred in display copy.
