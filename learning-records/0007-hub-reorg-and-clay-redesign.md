# 0007 — Hub-of-tracks reorganisation + "Soft-Clay Editorial" redesign

- **Date:** 2026-07-16
- **Status:** active
- **Type:** workspace architecture / design system

## Context

The parent asked to reorganise KaiSTEM the way DatLearn is organised — **separate projects instead
of one combined workspace** — and then redesign every page (direction chosen via a design pass,
approved before build).

## The reorganisation (reverses part of record 0004)

Record 0004 chose the flat `L0001-` / `V0001-` namespace *because* "a subfolder would break the
relative `../assets/` paths." This reorg deliberately reverses that: tracks are now full workspaces
in subfolders, and all asset/cross-links were rewritten for the new depth.

```
KaiSTEM/  (hub: index.html · HUB.md · assets/ · reference/parent-playbook · learning-records 0001,0004,0007)
├── science/   MISSION · RESOURCES · NOTES · index · lessons/0001–0005 · learning-records 0002,0003
├── words/     MISSION · RESOURCES · NOTES · index · lessons/0001–0002 (was L0001–L0002) · LR 0005
└── visual/    MISSION · RESOURCES · NOTES · index · lessons/0001 (was V0001) · reference/evidence · assets/cards.* · LR 0006
```

Split rules that mattered:
- **The shared north star lives once, in `HUB.md`** (per DatLearn). Track `MISSION.md`s state only
  what their track grows and link back — no restating, no drift.
- `RESOURCES.md` split cleanly by track; shared communities/books stayed in HUB.md.
- The Parent Playbook stayed **hub-level** (`reference/`): it is the shared method, unlike DatLearn
  whose topics share no method. This is a deliberate divergence from a "thin hub".
- Learning records went to the track they belong to; 0001/0004 (course-wide) stayed at hub level.
- **URLs changed** (GitHub Pages): old flat `lessons/…` paths are gone. Accepted knowingly.

## The redesign — "Soft-Clay Editorial" (spec: `assets/DESIGN-SYSTEM.md`)

Chosen with `/ui-ux-pro-max`, then curated: the raw recommendation (full Claymorphism, Baloo 2 +
Comic Neue, education-teal) was adjusted because the *reader is the parent* of research-cited
content — Comic Neue dropped for **Nunito**, teal dropped to keep the **load-bearing track hues**,
clay kept **restrained**. Owner approved: Baloo 2 display + Nunito body, restrained clay.

Gaps from the 2026-07-09 audit now closed:
- **Dark mode + theme toggle shipped** (`assets/theme.js`, OS-following with manual override).
- **Track colours are now measured, not eyeballed** — every accent ships light *and* dark values
  with computed WCAG ratios (all text pairs ≥4.5:1 in both themes; table in the foundation report).
- **Track skin scoped**: `visual/assets/track-visual.css` rules are scoped to
  `[data-accent="visual"]` and cannot leak.

## Rules that must not be reverted

- **Never set `--accent` via inline style or `LESSON.theme` again** — inline styles beat
  stylesheets, which silently breaks dark mode. Use `data-accent="science|words|visual"` on `<html>`
  (track colours), or a per-lesson `<style>` block carrying BOTH light and dark values (the pattern
  every lesson now uses). `LESSON.theme` accent entries were removed from all lessons.
- The shared stylesheets' **selector contract is load-bearing**: 0 selectors were renamed in the
  redesign; keep it that way.
- `.day` pins `h3`/`.day-body` to `grid-column: 2`; any single-column card variant must reset the
  children too (the hub's `.day.track` does — 120px-wide card bodies on phones otherwise).

## Open

- Print a journal page from a real printer once, both a lesson and the playbook (print CSS is
  written and reviewed, not yet paper-tested).
- Run the new look past the parent on his actual phone — clay shadows render differently on OLED.
