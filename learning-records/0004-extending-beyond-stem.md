# 0004 — Extending beyond STEM: the multi-track course + Words pilot

- **Date:** 2026-06-29
- **Status:** active
- **Type:** curriculum architecture / scope decision

## Context

Parent asked to extend the repo to teach Kai more topics, not just STEM. Process requested:
plan → agree with Codex → execute → Codex review.

## Scope chosen (with the parent)

- **One new domain this pass: Language & Literacy** ("Words"). Not social-emotional / arts / world —
  kept narrow on purpose.
- **The course becomes multi-track**, not "STEM + bolt-ons." A track = a loop + a colour + lessons.
- **Pilot-first:** restructure for two tracks + ship ONE polished literacy lesson, then run it with
  Kai before building more. (Same caution that served records 0002–0003.)

## The non-obvious decision: a literacy-native loop

The engine is built around the science inquiry loop (Notice→Wonder→Predict→Test→Talk). "Predict→test"
is a poor fit for rhyme/story. So **Words gets its own loop:**

> 👂 Listen → 💡 Wonder → 🎭 Play → ✏️ Make → 💬 Share

Same engine, same visual system, same 3-layer days and guardrails — only the loop differs. This keeps
each track honest to how that kind of thinking actually develops, while the *method* (guess/try first,
joy over correctness) stays identical.

## Pilot: Words W1 — "Rhyme Time"

- **Why rhyme:** phonological awareness is among the strongest early predictors of later reading, and
  it's pure play. Animal theme leans on Kai's documented love of animals + songs (record 0001).
- 5-day arc, 3-layer days, `type:"log"` rhyme journal (word → rhymes-with), warm coral theme.
- File: `lessons/L0001-rhyme-time.html` — **`L` namespace, flat folder** (keeps science numbering
  `0001`–`0005` untouched; a subfolder would break the relative `../assets/` paths). Codex concurred.

## Engine changes (minimal, additive)

- `assets/lesson.css`: 4 new loop-tone rules (`listen/play/make/share`). STEM tones untouched.
- `assets/lesson.js`: optional `L.locatorLabel` / `L.locatorHome` so non-science tracks don't read
  "PROJECT 01 / 01". Backward-compatible — the 5 science lessons render byte-identically.

## Codex agreement (2026-06-29)

Codex **agreed** with the plan. Folded-in feedback:
- Corrected a spec claim ("no border color" → new tones fall back to the *neutral default* border;
  `.loop-card` has a default `border-top`).
- Confirmed `L0001-` flat-folder naming over a subfolder.
- Pedagogy guardrails now baked into the lesson: Day 2 is *silly listening play, not a quiz*;
  explicit permission to **stop at 10–15 min**; parent copy avoids reading-prep pressure; a visible
  guardrail states **nonsense & partial rhymes count as winning**.

Spec: `docs/superpowers/specs/2026-06-29-literacy-track-design.md`.

## Open / to confirm next session

- Run W1 with Kai: did he start rhyming *unprompted, away from the activity*? That's the real signal.
- Which pulls harder next — more Words (W2: syllables/sounds, or story-telling) or Science P6?
- Possible later tracks (deferred, YAGNI): social-emotional, creative arts, world & people.
- Re-verify the remaining Words source URLs in RESOURCES.md before quoting exact pages in a lesson.
