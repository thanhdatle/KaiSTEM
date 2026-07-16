# KaiSTEM — how this space works

A personal, multi-track home learning workshop for **Kai (3.5)** — built on the `/teach` method,
organised as a **hub of separate track projects** (the same way [DatLearn] is a hub of topics).

The `teach` method treats one directory as **one** teaching workspace with **one** mission. KaiSTEM
shares a *single north star* across every track, so the hub root holds that shared mission and each
**track** gets its own full workspace in a subfolder — its own loop, colour, sources, and lessons.

## The North Star (shared by every track)

> Spark **lifelong curiosity** and build **quality bonding time**.

Success a year from now is **not** facts memorised. It looks like:

- Kai asking "why?" and "what if?" on his own, unprompted.
- Kai expecting that *his* ideas get tested ("let's try it and see!").
- A folder of filled-in journal pages you both made together.
- Kai seeing himself as "someone who figures things out" — early **learner identity**, across
  science *and* language *and* space, not facts in one subject.

We optimise for **joy and wonder over correctness.** A wrong prediction enthusiastically tested
beats a right answer recited.

## Who is learning (two learners, two layers)

- **Kai (3.5)** — the scientist. He does the exploring, mess-making, and wondering.
- **You (the parent)** — the learner *in this workspace*. Kai can't read HTML lessons, so every
  lesson teaches **you** how to set up and run a hands-on project with Kai: what to prepare, what to
  say, what to look for, and how to capture it.

**Kai right now:** lights up at 🐛 animals & nature, 💧 water/mess/mixing, and 🔢 numbers/books/songs.
Less drawn to building/vehicles (revisit later — interests shift fast). Developmentally he can
predict simple cause-and-effect, sort by one attribute, count small quantities, follow a 2–3 step
activity, and focus ~10–20 min on something genuinely interesting. Abstract explanation does **not**
land yet — *doing* does.

## Layout

```
KaiSTEM/
├── index.html            ← hub home: a card per track
├── HUB.md                ← this file: shared north star + method + guardrails
├── README.md
├── assets/               ← shared design system (reused by ALL tracks; don't fork)
│   ├── styles.css        ← hub & doc pages
│   ├── lesson.css        ← the interactive lesson engine's styles
│   └── lesson.js         ← the interactive lesson engine (Prep/Run, journal, question bank)
├── reference/
│   └── 0001-parent-playbook.html   ← SHARED method: the loop, "magic words", glossary, journal
├── learning-records/     ← hub-level records (course architecture & baseline)
└── <track>/              ← one full teach workspace per track
    ├── index.html        ← the track's landing page (loop + lessons)
    ├── MISSION.md        ← WHY this track exists (points back here for the shared north star)
    ├── RESOURCES.md      ← high-trust sources cited by this track's lessons
    ├── NOTES.md          ← this track's teaching preferences & conventions
    ├── lessons/          ← 0001-*.html, incrementing — the unit of teaching
    ├── reference/        ← track-specific cheat-sheets (e.g. visual's evidence card)
    ├── learning-records/ ← what we've decided & learned in this track
    └── assets/           ← track-specific components (rare; visual's card deck lives here)
```

## The tracks (one course, one method, three loops)

Each track is a domain with its own toddler-sized loop. Same north star, same method, same 3-layer
days and guardrails — the loop is tuned to how that kind of thinking actually develops.

| Track | Loop | What it grows | Accent (hue) |
|-------|------|---------------|--------------|
| 🔬 [Science](science/index.html) | Notice → Wonder → Predict → Test → Talk | inquiry: guess, then find out | warm ~35° |
| 📖 [Words](words/index.html) | Listen → Wonder → Play → Make → Share | language & literacy through play, before letters | coral ~15° |
| 🔄 [Visual](visual/index.html) | Look → Wonder → Turn → Make → Talk | spatial thinking: turning shapes in the mind | indigo ~295° |

**Track colours** must sit far enough apart in hue to read as distinct on the hub grid, and clear
4.5:1 contrast in the eventual light + dark themes. Current hues (Science ~35°, Words ~15°,
Visual ~295°) were chosen by eye against each other; when a dark theme lands they must be
re-measured (see [[kaistem-vs-datlearn-divergences]]: dark-theme contrast was never checked because
there is no dark theme yet).

## How every project runs (the shared method)

- **Format:** project-based. Each project is a multi-day arc, ~**30 min hands-on daily**, built in
  **3 layers** — warm-up (~5) → main, several rounds (~15) → extend / "stretch it further" (~10).
- **Progression:** projects *and* the days within them get **progressively harder** — more steps,
  more variables, more Kai-led decisions. Every project ends on a **Kai-led day** (he picks what to
  test) to build ownership.
- **Materials:** the parent prepares physical materials in advance; every lesson ships a
  shop-ahead prep list.
- **Note-keeping:** Kai keeps a **journal** — a page per project where he draws/marks predictions
  and results. That is the retention + bonding artifact; keep the filled-in pages in a folder.
- **The method itself** — whichever track — is *guess/try first, then find out, and talk about it.*
  The full how-to (the "magic words" question banks, the glossary, how the journal works) lives in
  the shared [Parent Playbook](reference/0001-parent-playbook.html) — read it once, then run the
  first project in any track.

## Guardrails (every track)

- Follow Kai's lead. If he hijacks the project with a better question, **go with his question.**
- Stop while it's still fun. End on a high, not at the meltdown (10–15 min is fine).
- No "right answers" pressure. Predictions are guesses; guesses are great.
- Safety: an adult alongside for all water, small parts, and mixing; nothing he could choke on
  unattended.

## Adding a track

A track = a loop + a colour + lessons. Start narrow (one pilot lesson), run it with Kai, then expand.
Give the new track its own subfolder with the full workspace layout above, split its sources into
`<track>/RESOURCES.md`, and add a card to the hub `index.html` and a row to the table here.

## Evidence & honesty (why this space is trustworthy)

Never trust guesswork. Claims in lessons cite trusted sources (NAEYC, HeadStart.gov, Zero to Three,
Reading Rockets, and the spatial-cognition literature). Where evidence is contested — as with the
Shichida "right-brain" framing behind the Visual track — we say so out loud and keep only what the
research supports. See the visual track's honest audit,
[visual/reference/0002-visual-thinking-evidence.html](visual/reference/0002-visual-thinking-evidence.html).

## Shared communities & further reading (cross-track)

> Not yet selected with the parent. Candidates:
> - **[r/ScienceBasedParenting](https://www.reddit.com/r/ScienceBasedParenting/)** — the culture
>   demands citations and pushes back on marketing claims; the right place to sanity-check the next
>   programme someone recommends.
> - [DREME Family Math (Stanford)](https://familymath.stanford.edu/) /
>   [Erikson Early Math](https://earlymath.erikson.edu/) — research-based activity sources of record.
> - r/toddlers, r/Preschoolers; local library / children's-museum parent programs (in person).
> - Books: *The Scientist in the Crib* (Gopnik et al.); the *Vroom* app/cards (free micro-activities 0–5).

## Viewing

Open `index.html` in a browser (`open index.html` on macOS). Everything is static — no build step,
no server. Published to GitHub Pages.

[DatLearn]: https://github.com/thanhdatle — the reference implementation this hub structure follows.
