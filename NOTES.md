# Notes — working preferences

## Parent's stated preferences (2026-06-23)
- **Project-based**, not one-off activities.
- **~30 min hands-on daily.**
- **Note-keeping** matters — wants a journal/record artifact. Build a journal page into every project.
- **Progressive difficulty** — within a project (day to day) AND across projects.
- Parent will **prepare physical materials in advance** — so every lesson needs a clear,
  shop-ahead prep list.

## Design conventions for this workspace
- Lessons are written **for the parent** (the reader), about running an activity **with Kai**.
- Every project = a multi-day arc, each day a ~30-min session.
- Every project ends with a **Kai-led day** (he picks what to test) — builds ownership.
- Weave **counting** into projects when natural (early math = high leverage).
- Keep the science vocabulary in lessons matched to the Glossary in the Parent Playbook.
- Tone: warm, encouraging, concrete scripts ("say this") over theory.

## Calibration log
- **2026-06-24 (after Project 1):** Kai learned P1 *very well*, but each day finished in ~10 min,
  not 30. Takeaway: lessons were too thin, not his attention. Going forward, build every day in
  **3 layers** (warm-up ~5 / main = several rounds ~15 / extend + "stretch it further" ~10).
  Applied to P4–P5. Offered to retrofit P1–P3. See [learning record 0003](./learning-records/0003-p1-feedback-and-extension.md).

## Parent's stated preferences (2026-07-09)
- Wants the Visual track to be **really visual**.
- **Has AI image generation** (ChatGPT / DALL·E or Gemini) and wants to help build course assets.
  → Write **paste-ready prompt packs** into any lesson that needs imagery.
  → But: AI images **cannot** make valid mental-rotation cards (geometric exactness *is* the task).
    Use them for pattern sets, vocabulary cards, and symmetry/mandala art.
    See [LR 0006](./learning-records/0006-visual-track-and-shichida-evidence.md).
- **Every lesson ships on-screen *and* print-ready.** His words: "in case we can't print in time."
  → `assets/cards.js` renders both faces from one trial definition. Reuse it, don't re-invent it.
- Used the **Shichida method** and found it helpful. Shown the evidence, he chose "keep the
  activities, drop the theory." **He takes honest correction well — do not soften findings.**
- "Feel free to customise CSS per learning stream" → each track may carry its own stylesheet
  (`assets/track-visual.css` is the first).

## Design conventions, Visual track
- Track colour: indigo (`--accent: oklch(58% 0.16 295)`). Science owns warm ~35, Words ~15.
- Loop: **Look → Wonder → Turn → Make → Talk**.
- Card decks mount **outside `#app`**, so the lesson engine's full re-render never clobbers them.
- Deck answer sides follow a **Thue–Morse sequence**, never alternation: a child can beat an
  A/B/A/B key by tracking sides instead of turning shapes.
- Shapes must be **chiral** (no reflection symmetry), or the "flipped" decoy is secretly the correct
  answer and the card teaches nothing. Verify any new shape before shipping it.

## Open questions to revisit
- Pick a parent community (see RESOURCES.md).
- Confirm what materials are already at home vs. need buying.
- Did the 3-layer days actually hit ~30 min for Kai? Re-tune after P4/P5.
- Retrofit P1–P3 with "Stretch it further" layers? (awaiting parent's go)
