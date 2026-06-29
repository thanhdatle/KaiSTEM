# 0005 — Words W2: syllables ("Word Beats")

- **Date:** 2026-06-29
- **Status:** active
- **Type:** curriculum (Words track)

## Context

Parent said "run the words w2." Built the second Words lesson directly on the approved L0001
template (the multi-track architecture from [0004](./0004-extending-beyond-stem.md) is settled, so
this is content authoring, not re-architecture).

## Decision: W2 = syllables / word-beats

Chosen (parent confirmed, recommended option) over story-telling and first-sounds. Rationale:
it's the **documented next rung of phonological awareness after rhyme** (rhyme → syllables →
first sounds → phonemes), it was already foreshadowed in W1 (Day 1 claps the syllables of his
name), and it keeps the Words track a coherent "ear for sound" ladder.

## The progression (the non-obvious part)

The Words track advances the **grain of the ear**, the way Science advances the *kind of prediction*:

| # | Lesson | The ear for… |
|---|--------|--------------|
| W1 | Rhyme Time | whole words that **sound alike** at the end |
| W2 | Word Beats | the **beats (syllables) inside** a single word |

W2 is *finer* than W1: rhyme compares whole-word endings; syllables segment within one word.

## What shipped

- `lessons/L0002-word-beats.html` — 5-day arc, 3-layer days, Words loop, `type:"log"` journal
  (word → beats), warm tangerine theme (distinct from W1 coral), `locatorLabel: "WORDS · LESSON TWO"`.
- Multi-sensory by design: clap / march / drum / jump the beats (movement cements segmentation).
- **Interleaving:** Day 2 reuses sorting (short vs long); Day 3 reuses science's guess-then-test
  ("guess the beats, then clap to check").
- Same guardrails as W1: joyful-not-graded, **close counts as winning**, stop at 10–15 min,
  never "no, count again."
- Wired into `index.html` (W2 card + nav), `README.md` (Words table), the Parent Playbook glossary
  (beat/syllable, clap-it-out, short/long), and a W1→W2 forward link.

## Open / to confirm next session

- Run W1 then W2 with Kai. Did he start clapping words out unprompted? That's the real signal.
- W3 candidates: **first sounds** ("ball starts with /b/") — the next rung — or a story-telling turn.
- Sourcing: syllable claims rest on Reading Rockets / Zero to Three (already in RESOURCES.md Words tier).
