# KaiSTEM design system — "Soft-Clay Editorial"

The single source of truth for the KaiSTEM redesign. Every page (hub, topic indexes, lessons,
reference cards) reads as one warm, joyful-but-credible thing. Chosen with `/ui-ux-pro-max` and
curated for a **dual audience**: the course is *for a 3.5-year-old*, but the *reader* is the parent,
often reading research-cited content — so the chrome is playful (soft clay) and the reading core is
editorial (real hierarchy, calm measure).

> Direction locked with the owner: **Baloo 2** display + **Nunito** body, **restrained**
> claymorphism, warm cream/ink base + honey-amber hub accent + the three track hues, **light + dark
> + print**.

## Non-negotiables

- **Preserve every existing CSS class/selector** in `assets/styles.css` and `assets/lesson.css`.
  All 15 pages reuse them; renaming breaks pages. Change the *treatment*, not the *contract*.
- **Static, no build.** Load fonts with a single `@import` at the top of each stylesheet (and/or a
  `<link>` in page heads). No JS framework.
- **Light + dark + print**, everywhere. Dark mode is a NEW addition — it did not exist before.
- Respect `prefers-reduced-motion` (already wired in `lesson.css`; add to `styles.css` too).
- Keep the per-track accent overriding mechanism: topic pages and lessons set `--accent` /
  `--accent-deep` inline; the system must theme cleanly off those two variables.

## Fonts (4 families, weights trimmed)

```css
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700&family=Nunito:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Mono:wght@400;700&family=Caveat:wght@500;600&display=swap');
```

| Role | Family | Used for |
|------|--------|----------|
| Display | **Baloo 2** (600/700) | `h1`,`h2`,`h3`, hero titles, `.h2`, loop-card day words, big numbers |
| Body | **Nunito** (400/600/700) | all reading prose, cards, buttons, inputs |
| Label | **Space Mono** (400/700) | kickers, eyebrows, `.badge`, table headers, locators — small, letterspaced, uppercase. Keeps an editorial-precision counterweight to the round display/body. |
| Hand | **Caveat** (500/600) | journal "said" captions ONLY — the one handwriting charm point |

Token mapping (keep the existing names, give them these values):
- `styles.css`: `--font-disp` → Baloo 2 stack; `--font-body` → Nunito stack; `--font-mono` → Space Mono stack; `--font-hand` → Caveat stack.
- `lesson.css`: add `--disp` → Baloo 2 stack; `--serif` → Nunito stack (rename intent, keep the token name to avoid churn); `--mono` → Space Mono; `--hand` → Caveat. Switch `.hero h1`, `.h2`, and `.loop-card .name`/day word to `var(--disp)`.

Baloo 2 stack: `"Baloo 2","Trebuchet MS",system-ui,sans-serif`
Nunito stack: `"Nunito","Segoe UI",system-ui,sans-serif`

## Colour — light theme (refine current)

Warm paper + warm ink. Keep the current light values; they already fit.
```
--paper:      oklch(98.5% 0.008 85)   cream
--paper-2:    oklch(96.4% 0.013 80)   raised surface
--paper-sunk: oklch(95%   0.014 78)   inset well
--ink:        oklch(26%   0.02  60)   text
--ink-soft:   oklch(46%   0.02  60)   secondary text (verify ≥4.5:1 on paper)
--rule:       oklch(88%   0.015 75)   hairline
```
Hub/default accent = honey-amber; per track overridden:
```
--accent (hub honey):   oklch(64% 0.15 72)   --accent-deep: oklch(52% 0.15 70)
Science (warm amber):   --accent: oklch(60% 0.15 45)   --accent-deep: oklch(48% 0.15 45)
Words   (coral):        --accent: oklch(62% 0.18 18)   --accent-deep: oklch(50% 0.18 18)
Visual  (indigo):       --accent: oklch(58% 0.16 295)  --accent-deep: oklch(45% 0.16 296)
```
Tone hues (loop/callout coding) — keep: `--wonder` violet ~285°, `--predict` amber ~72°,
`--test` teal ~205°, `--grow` green ~150°. All used as *accents/borders*, not body text.

**Every accent must clear 4.5:1 as link/heading text on `--paper`.** Where a chosen hue does not,
darken to `--accent-deep` for text and reserve the lighter one for fills/borders. Verify, don't guess.

## Colour — dark theme (NEW)

Add `@media (prefers-color-scheme: dark)` **and** a `:root[data-theme="dark"]` override (for a manual
toggle), both setting the same tokens. Warm dark, never pure black; desaturated, lighter accents.
```
--paper:      oklch(23% 0.018 60)   warm near-black brown
--paper-2:    oklch(27% 0.02  60)   raised
--paper-sunk: oklch(20% 0.018 60)   inset well
--ink:        oklch(93% 0.012 85)   warm off-white
--ink-soft:   oklch(74% 0.02  75)   secondary (verify ≥3:1, aim 4.5:1)
--rule:       oklch(40% 0.02  70)   visible divider in BOTH themes
```
Accents lightened for dark (targets — verify ≥4.5:1 on `--paper` dark):
```
hub honey:  --accent: oklch(80% 0.13 78)   --accent-deep: oklch(86% 0.11 80)
Science:    --accent: oklch(78% 0.13 55)   --accent-deep: oklch(85% 0.11 58)
Words:      --accent: oklch(76% 0.15 20)   --accent-deep: oklch(84% 0.12 22)
Visual:     --accent: oklch(76% 0.13 292)  --accent-deep: oklch(84% 0.11 293)
```
Also lighten `--wonder/--predict/--test/--grow` ~+18–22% L for dark. Test dark contrast
INDEPENDENTLY — do not assume light values transfer.

## Claymorphism — RESTRAINED

Soft, tactile, rounded — not candy. Depth from layered soft shadows + a light inner top highlight, so
surfaces feel like pressed silicone. Reading blocks stay calm; clay is for cards/buttons/chips.

Radii:
```
--radius:      14px    reading blocks, table cells, callouts (unchanged — readable)
--radius-clay: 26px    cards (.box, .day, topic cards, .callout containers)
--radius-pill: 999px   loop chips, badges, mode toggle, FAB
```
Clay elevation (light) — a reusable recipe for raised cards:
```
box-shadow:
  0 1px 2px  oklch(50% 0.06 60 / .10),
  0 10px 24px oklch(52% 0.10 45 / .12),
  inset 0 -3px 6px oklch(48% 0.10 45 / .07),
  inset 0 2px 3px  oklch(100% 0 0 / .75);
```
Clay elevation (dark) — swap the light inner highlight for a subtle one, darken outers:
```
box-shadow:
  0 1px 2px  oklch(0% 0 0 / .35),
  0 12px 26px oklch(0% 0 0 / .40),
  inset 0 -3px 6px oklch(0% 0 0 / .30),
  inset 0 2px 3px  oklch(100% 0 0 / .06);
```
Pressed/active state: reduce outer spread, deepen the bottom inset, `transform: scale(.97)`.
Blobs: keep `lesson.css`'s `.blob` + `@keyframes floatY`; add 2–3 slow-drifting accent blobs to the
**hub hero only** (very low opacity, `filter: blur()`), behind content, `aria-hidden`, disabled under
reduced-motion. Do not scatter blobs across reading pages.

## Motion

- Micro-interactions 150–300ms, `ease-out` enter / `ease-in` exit.
- Press: `transform: scale(.97)` on `:active` for clay buttons/cards/chips; restore on release.
- Hover (pointer devices): lift 2px + slightly stronger shadow; never shift layout of neighbours.
- `@media (prefers-reduced-motion: reduce)`: disable animations + transforms (already in lesson.css;
  replicate in styles.css).

## Accessibility & interaction (must-haves)

- Contrast: body text ≥4.5:1, large text ≥3:1, in BOTH themes. `--rule` visible in both.
- Focus: visible 2–3px focus ring (`:focus-visible`) on every link/button/input, in both themes.
- Touch targets ≥44px for the mode toggle, gear rows, journal buttons, FAB, nav links.
- Don't encode meaning by colour alone (loop steps keep their emoji + name; tone callouts keep labels).
- `cursor: pointer` on all clickables; smooth 150–300ms state transitions.
- Icons: the loop/step emoji are decorative/semantic content, not UI chrome — keep them (they're part
  of the child-facing charm and paired with text). Do NOT introduce emoji as navigation/control icons;
  if a control needs a glyph, use an inline SVG.

## Print (journal pages must print clean)

- White background, black text, hide chrome (`[data-print="hide"]`, coursebar, FAB, mode toggle,
  blobs, nav). Keep the journal grid, gear checklist, and lesson body legible on paper.
- Remove clay shadows in print (`box-shadow:none`), keep borders so cards remain defined.
- `styles.css` should also carry a print block for the reference/journal-bearing doc pages.

## Deliverable checklist (foundation)

- [ ] Fonts imported; tokens remapped; all existing selectors preserved.
- [ ] Light + dark token blocks; manual `[data-theme]` override honoured.
- [ ] Clay recipe applied to `.box`, `.day`, topic cards, `.loop-card`, `.callout`, `.win-box`,
      buttons, `.seg`/mode toggle, `.fab`, `.sheet-card` — restrained, readable.
- [ ] `:focus-visible` rings + press states in both themes.
- [ ] Reduced-motion + print blocks in both stylesheets.
- [ ] Contrast verified for every accent/text pair in both themes (state the values).
