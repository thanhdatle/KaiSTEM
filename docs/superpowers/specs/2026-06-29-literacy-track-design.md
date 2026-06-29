# Spec: Extending KaiSTEM into a multi-track curiosity course (Literacy track)

- **Date:** 2026-06-29
- **Status:** DONE — built, verified, and APPROVED by Codex (2026-06-29)
- **Author:** Claude (with parent)

## 1. Goal & north star

Grow KaiSTEM from a STEM-only course into a **multi-track home learning course** for Kai (3.5),
without breaking the five existing science lessons or the shared engine. The north star is
unchanged: **spark lifelong curiosity + quality bonding time; joy and wonder over correctness.**

First new track: **Language & Literacy** ("Words"). Scope of *this* pass:
**restructure the repo to be multi-track + ship ONE polished pilot literacy lesson.**

Non-goals (YAGNI): no second non-STEM domain, no full 5-lesson literacy arc, no repo rename,
no build step, no JS framework. Those can follow after we run the pilot with Kai.

## 2. Pedagogical decisions

- **Literacy gets its own 5-move loop** (not the science Notice→Wonder→Predict→Test→Talk):
  **👂 Listen → 💡 Wonder → 🎭 Play → ✏️ Make → 💬 Share.** Same engine, same visual system,
  but the rhythm fits how language is learned (predict→test is a poor fit for rhyme/story).
- **3-layer day retained** (warm-up ~5m → main ~15m → extend ~10m) — proven in record 0003.
- **Pilot topic = rhyme / phonological awareness** ("Rhyme Time", a silly rhyme zoo). Rationale:
  phonological awareness is the strongest evidence-based predictor of later reading, it is pure
  play, and an animal theme leans on Kai's documented love of animals + songs (MISSION.md).
- **Same guardrails**: follow the child's lead, stop on a high note, no "right answers" pressure.
- **Codex pedagogy guardrails (folded in):** (a) Day 2 "rhyme or not?" is framed as *silly listening
  play, never a quiz*; (b) the lesson explicitly gives permission to stop at 10–15 min if joy drops —
  5×30 min on one phonological target can run long; (c) parent-facing copy must not read as
  reading-prep pressure even though the rationale cites evidence; (d) a visible in-lesson guardrail
  states **nonsense and partial rhymes count as winning** (they prove he hears the pattern).

## 3. Architecture

The engine (`assets/lesson.js` + `assets/lesson.css`) is data-driven from a per-lesson
`window.LESSON` object. Verified engine facts that make this low-risk:

- `lesson.js:91` renders each loop card as `loop-card <tone>`; **any tone string works** — only
  CSS styling is tone-specific.
- `lesson.css:94-95` gives `.loop-card` a default `border-top: 3px solid var(--ink-soft)`;
  `:96-100` styles loop tones for `notice/wonder/predict/test/talk` only. New tones fall through
  to the **neutral/default** border (not "no border") → **additive CSS only**, no logic change.
  *(Correction per Codex.)*
- `lesson.js:238` `journal.type === "log"` renders free-text columns. Literacy reuses this.
- `lesson.js:281` journal `<h2>` defaults to "Science journal" but `j.title` overrides it.
- `lesson.js:434` applies `L.theme` CSS-var overrides per lesson → literacy gets its own accent.

### Changes

| # | File | Change | Risk |
|---|------|--------|------|
| A | `assets/lesson.css` | Add loop-tone rules for `listen / play / make / share` (4 rules, ~6 lines). | additive, none |
| A2 | `assets/lesson.js` | `locatorBlock` (`:356-359`) hardcodes `PROJECT NN / NN`. Add optional `L.locatorLabel` override so literacy reads e.g. `WORDS · LESSON ONE` instead of `PROJECT 01 / 01`. Falls back to current text. | additive |
| B | `lessons/L0001-rhyme-time.html` | New pilot literacy lesson (LESSON data + engine include), `track:"words"`, literacy loop, log-journal (word → rhymes-with), warm coral/amber theme, qbank, faq, cited sources. | new file |
| C | `index.html` | Convert to a **track hub**: two sections (🔬 Science / 📖 Words), each with its loop + lessons. Science section lists the existing 5 unchanged. | medium (rework) |
| D | `MISSION.md` | Generalize "STEM identity" → "learner identity"; add a **Tracks** section: each track keeps the same method but has its own loop. | low |
| E | `reference/0001-parent-playbook.html` | Add a "Two tracks, two loops" note + a literacy magic-words / glossary block (one playbook, not fragmented). | low |
| F | `assets/LESSON-SCHEMA.md` | Document `track`, the new loop tones, and that loop/journal are track-agnostic. | docs |
| G | `learning-records/0004-extending-beyond-stem.md` | Record the decision (multi-track, literacy-native loop, pilot-first). | docs |
| H | `README.md` | Reframe one-liner + curriculum table to show two tracks. | low |

### Naming scheme (open question for Codex)

Proposed: literacy lessons use an **`L` namespace** — `lessons/L0001-rhyme-time.html` — so science
numbering (`0001`–`0005`) is untouched and tracks are visually grouped in the folder. Alternative
considered: a `lessons/literacy/` subfolder (cleaner grouping, but changes relative asset paths
`../assets/…` → `../../assets/…` and complicates links). **Recommendation: `L` prefix, flat folder.**

## 4. Pilot lesson content outline — "Rhyme Time"

- **Hero:** kicker "KaiSTEM · Words · Lesson One"; two-tone title "Rhyme Time"; sub about hearing
  and making silly rhymes with animals.
- **Loop cards:** Listen/Wonder/Play/Make/Share with the new tones.
- **win:** the payoff — Kai starts *hearing* that words can sound alike (the ear for sound that
  pre-reading rests on).
- **prep.gear:** picture cards or toy animals, a "rhyme basket" of small objects, paper+crayons,
  a favorite rhyming book. Cheap/household.
- **days (5, 3-layer each):**
  1. ★☆☆ Hear the rhyme — read a rhyming book, catch the rhyming pairs (warm-up: clap the beat).
  2. ★★☆ Rhyme or not? — sort pairs that rhyme vs don't (interleaves the science "sort" skill).
  3. ★★★ Silly rhyme zoo — make up nonsense rhymes for animals ("cat → hat → splat").
  4. ★★★ Fill the rhyme — leave the last word of a known rhyme blank, Kai supplies it.
  5. ★★★★ Kai leads — Kai invents a rhyme and "reads" it back; scribe his exact words.
- **journal:** `type:"log"`, columns `word` → `rhymes with`. Title "Rhyme journal".
  localStorage namespaced by `storageKey:"rhyme-v1"`; example row `{word:"cat", "rhymes with":"hat"}`.
- **qbank:** language "magic words" (e.g. "What sounds the same?", "Can you find a word that rhymes
  with __?", "Silly or real — you pick!").
- **faq:** "He makes up nonsense words — is that wrong?" (no — invented rhymes prove he hears the
  pattern), "He can't read, isn't this too early?" (rhyme is ears not eyes), pacing, etc.
- **sources:** NAEYC, Reading Rockets (phonological awareness), Zero to Three. Cited in-lesson.
- **theme:** warm coral/amber accent distinct from the science palette so Words ≠ Science at a glance.

## 5. Process (per parent's request)

1. Write this spec. ✅
2. **Take it to Codex for agreement**; fold in feedback; converge on open questions (naming scheme,
   loop wording, pilot topic).
3. Execute the changes (A–H).
4. **Ask Codex to review** the result.
5. Verify in a browser (320 / 768 / 1440): new lesson renders, new loop tones styled, log-journal
   saves to localStorage, and the 5 science lessons + hub still render unchanged.

## 6. Acceptance criteria

- [x] `index.html` shows two clearly-distinct tracks; all 5 science links + the 1 literacy link work (verified — all hub links resolve).
- [x] `lessons/L0001-rhyme-time.html` parses with the literacy loop (4 new tones styled), a `type:"log"`
      journal, qbank, faq, and cited sources — mobile-first. (Static/Node verification; Playwright visual
      pass deferred — the browser bridge wasn't available in this environment.)
- [x] No regression: the 5 science lessons parse; the `locatorBlock` change is byte-identical without overrides.
- [x] MISSION/README/Playbook/Schema reflect the multi-track framing; learning record 0004 added.
- [x] Codex agreed to the plan and APPROVED the result (after one should-fix round).
