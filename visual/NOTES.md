# Notes — Visual track

Working preferences and teaching conventions specific to the Visual track. Shared workspace
conventions live in the hub — see **[[HUB]]** (`../HUB.md`). Evidence backing this track:
[[0006-visual-track-and-shichida-evidence]] and the
[evidence card](reference/0002-visual-thinking-evidence.html).

## Parent's stated preferences (2026-07-09)
- Wants the Visual track to be **really visual**.
- **Has AI image generation** (ChatGPT / DALL·E or Gemini) and wants to help build course assets.
  → Write **paste-ready prompt packs** into any lesson that needs imagery.
  → But: AI images **cannot** make valid mental-rotation cards (geometric exactness *is* the task).
    Use them for pattern sets, vocabulary cards, and symmetry/mandala art.
    See [[0006-visual-track-and-shichida-evidence]].
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
- Did the on-screen deck and print deck stay identical after the last `cards.js` edit? Re-check on
  the next lesson.
- Which materials for V1 are already at home vs. need buying (printer/cardstock, scissors)?
- Pick the next Visual lesson: repeating patterns (per Rittle-Johnson 2020) vs. symmetry art.
