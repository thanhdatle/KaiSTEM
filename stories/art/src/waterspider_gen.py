#!/usr/bin/env python3
"""Generates the 13 Water-Spider-Brings-the-Fire flip-book SVGs from shared character parts.

Usage: python3 waterspider_gen.py <output-dir>
Scale rule: on shore pages every animal uses the fixed SIZE table below, so the water spider is
always the smallest and the raven the biggest. Pages set on the lake show the spider alone (closer to us)
at SPIDER_LAKE. Fire colours (FIRE / EMBER / FLAME) appear only where there is fire.
State rule: the raven is pale until page 06, then black; the screech owl gets red eye-rims from 07;
the hooting and horned owls get white eye-rings from 08; the racer snake is pale until 09, then black.
Fixed geometry: island centre x = 560, island top y = 318; the sycamore stands on it.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SIZE = {"raven": .9, "screech": .72, "hooting": .92, "horned": 1.0, "snake": .72, "spider": .47}
SPIDER_LAKE = 1.15
SPIDER, SPIDER_L, STRIPE = "#3A3446", "#544C63", "#E0533D"
BOWL, BOWL_D, BOWL_IN = "#D9AC62", "#A87A3A", "#7A5326"
RAVEN_PALE, RAVEN_PALE_D = "#EEF0F5", "#C6CCD9"
RAVEN_BLK, RAVEN_BLK_D, RAVEN_SHEEN = "#2E3142", "#1E2030", "#5B6A9C"
OWL = {"screech": ("#A3A7AE", "#7D828B", "#D3D6DB"), "hooting": ("#B49877", "#8C7255", "#E2D3BD"),
       "horned": ("#8E6A48", "#694C32", "#D8BE97")}
SNAKE_PALE, SNAKE_PALE_D = "#B7C4AE", "#93A38A"
SNAKE_BLK, SNAKE_BLK_D = "#2B2E3A", "#6A7390"
BARK, BARK_D, BARK_P = "#EEE8DA", "#C9C2AE", "#A7B097"
FIRE, EMBER, FLAME = "#F2652A", "#F25C2A", "#FFC23A"
LAKE, LAKE_L, LAKE_D = "#5B88B5", "#93B9DA", "#456F9C"
SNOW, SNOW_D = "#F4F7FB", "#D6DFEA"
HILL, HILL_D = "#B9C6D6", "#9DAEC4"
ISLE, ISLE_D = "#6E7B5A", "#56613F"
COLD = [(0, "#7189AC"), (1, "#DCE5EF")]
STORM = [(0, "#4C5878"), (1, "#B9C3D3")]
DUSK = [(0, "#2D3A6B"), (.6, "#7E7FB0"), (1, "#E4C9C8")]
WARM = [(0, "#F2B27A"), (.55, "#FBD9A6"), (1, "#FFF1D6")]
IX, IY = 560, 318


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def eye(x: float, y: float, r: float, iris: str = "#fff", pupil: str = INK, mood: str = "open") -> str:
    if mood == "shut":
        return stroke(f"M{x - r} {y} q{r} {r * .8} {2 * r} 0", pupil, max(2.4, r * .38))
    if mood == "blink":
        return (f'<path d="M{x - r} {y} A{r} {r} 0 0 0 {x + r} {y}Z" fill="{iris}"/>'
                f'<circle cx="{x}" cy="{y + r * .35}" r="{r * .42}" fill="{pupil}"/>' + stroke(f"M{x - r} {y} H{x + r}", pupil, max(2.2, r * .3)))
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{iris}"/><circle cx="{x + r * .12}" cy="{y + r * .1}" r="{r * .55}" fill="{pupil}"/>'
            f'<circle cx="{x + r * .32}" cy="{y - r * .2}" r="{r * .2}" fill="#fff"/>')


def puffs(pts: list, col: str = "#fff", op: float = .85) -> str:
    """Little breath / smoke puffs: (x, y, r)."""
    return f'<g fill="{col}" opacity="{op}">' + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>'


def shiver(x: float, y: float, h: float = 30, gap: float = 40) -> str:
    """Zig-zag shiver marks either side of a body, `gap` out from its centre line."""
    return stroke(f"M{x - gap} {y} l-6 {h * .3} l6 {h * .3} l-6 {h * .3} M{x + gap} {y} l6 {h * .3} l-6 {h * .3} l6 {h * .3}", "#fff", 3)


# ---------- characters (each origin is where the feet / belly meet the ground) ----------

def spider(x: float, y: float, s: float = SIZE["spider"], *, ember: bool = False, skate: bool = False, flip: bool = False,
           mood: str = "smile", weave: bool = False, bowl_on: bool = True) -> str:
    """Water Spider: a small round black downy spider with red stripes, big friendly eyes, and a woven bowl on her back."""
    legs, feet, rip = "", "", ""
    fy = 0 if skate else -2
    for sx in (-1, 1):
        for i in range(4):
            hx, hy = sx * 18, -42 + i * 7
            kx, ky = sx * (36 + i * 7), -58 + i * 8
            fx = sx * (40 + i * 12) if skate else sx * (38 + i * 10)
            legs += stroke(f"M{hx} {hy} L{kx} {ky} L{fx} {fy}", SPIDER, 6.5)
            feet += f'<circle cx="{fx}" cy="{fy}" r="3.6" fill="{SPIDER_L}"/>'
            if skate:
                rip += f'<ellipse cx="{fx}" cy="2" rx="9" ry="2.6" fill="none" stroke="#fff" stroke-width="2.2" opacity=".85"/>'
    fuzz = stroke(" ".join(f"M{24 * c:.1f} {-32 + 24 * d:.1f} l{5 * c:.1f} {5 * d:.1f}" for c, d in
                           [(-1, 0), (-.87, .5), (-.87, -.5), (1, 0), (.87, .5), (.87, -.5), (-.5, .87), (.5, .87)]), SPIDER, 3)
    body = (f'<circle cx="0" cy="-32" r="24" fill="{SPIDER}"/>' + fuzz
            + stroke("M-21 -22 Q-25 -34 -19 -46 M21 -22 Q25 -34 19 -46", STRIPE, 4.2) + stroke("M-13 -13 Q0 -8 13 -13", STRIPE, 4.2))
    em = "shut" if mood == "proud" else "open"
    face = (eye(-9, -36, 7.5, mood=em) + eye(9, -36, 7.5, mood=em)
            + stroke("M-15 -44 l-3 -3 M15 -44 l3 -3", "#fff", 2)
            + '<circle cx="-16" cy="-25" r="4" fill="#F2A9B0" opacity=".8"/><circle cx="16" cy="-25" r="4" fill="#F2A9B0" opacity=".8"/>'
            + stroke("M-6 -25 Q0 -19 6 -25", "#F2A9B0", 2.6))
    bowl = (f'<path d="M-26 -74 Q-24 -52 0 -52 Q24 -52 26 -74Z" fill="{BOWL}"/>'
            + stroke("M-16 -72 Q-14 -58 -9 -54 M-5 -73 V-53 M6 -73 V-53 M17 -72 Q14 -58 9 -54", BOWL_D, 2.2)
            + stroke("M-24 -66 Q0 -58 24 -66 M-20 -58 Q0 -52 20 -58", BOWL_D, 2.2)
            + f'<ellipse cx="0" cy="-74" rx="26" ry="6.5" fill="{BOWL_IN}"/>' + stroke("M-26 -74 Q0 -66 26 -74", BOWL_D, 3))
    glow = ""
    if ember:
        glow = f'<ellipse cx="0" cy="-78" rx="22" ry="12" fill="{FLAME}" opacity=".35"/>'
        bowl += (f'<ellipse cx="0" cy="-75" rx="10" ry="5.5" fill="{EMBER}"/><ellipse cx="-2" cy="-76" rx="4" ry="2.4" fill="{FLAME}"/>'
                 f'<path d="M-5 -77 Q-4 -90 1 -96 Q2 -86 6 -77Z" fill="{FLAME}"/>')
    silk = ""
    if weave:
        silk = (stroke("M-30 -80 q-14 -16 -2 -28 q12 -10 18 4 M30 -82 q16 -14 4 -28 q-10 -8 -16 4", "#fff", 2.6)
                + '<g fill="#fff"><circle cx="-36" cy="-106" r="2.4"/><circle cx="40" cy="-110" r="2.4"/><circle cx="0" cy="-98" r="2"/></g>')
    motion = stroke("M-70 -20 h-26 M-74 -34 h-18 M-66 -6 h-30", "#fff", 3) if skate else ""
    big = '<g transform="translate(0 -30) scale(1.25) translate(0 30)">'  # a rounder, chubbier body than the legs alone suggest
    return group(x, y, s, flip, 0, rip + motion + legs + feet + big + glow + body + (bowl if bowl_on else "") + face + silk + "</g>")


def raven(x: float, y: float, s: float = SIZE["raven"], *, black: bool = False, pose: str = "stand", mood: str = "smile",
          flip: bool = False) -> str:
    """Raven, side view facing right. Pale silver-white before the fire, glossy black after."""
    col, dk = (RAVEN_BLK, RAVEN_BLK_D) if black else (RAVEN_PALE, RAVEN_PALE_D)
    iris, pup = ("#fff", INK)
    if pose == "fly":
        wings = (f'<path d="M-20 -70 Q-60 -150 -110 -150 Q-80 -120 -70 -96 Q-50 -84 -10 -66Z" fill="{dk}"/>'
                 f'<path d="M0 -72 Q10 -160 60 -176 Q46 -140 44 -108 Q34 -86 14 -66Z" fill="{col}"/>')
        body = f'<ellipse cx="0" cy="-62" rx="56" ry="24" fill="{col}"/><path d="M-50 -62 L-100 -80 L-104 -60 L-100 -40Z" fill="{col}"/>'
        head = (f'<path d="M40 -58 L46 -44 L52 -54 L58 -42 L62 -56 L68 -46 L70 -64Z" fill="{dk}"/>'  # shaggy throat
                f'<circle cx="54" cy="-74" r="22" fill="{col}"/><path d="M68 -86 Q98 -88 110 -72 Q94 -64 70 -62Z" fill="#3E3E48"/>')
        eyes = eye(60, -80, 6, iris, pup)
        legs = stroke("M-10 -42 l-16 10 M4 -42 l-14 12", "#5A5560", 4)
        return group(x, y, s, flip, 0, wings + legs + body + head + eyes)
    body = (f'<path d="M-44 -46 L-96 -28 L-90 -16 L-100 -6 L-40 -32Z" fill="{dk}"/>'
            f'<ellipse cx="-4" cy="-62" rx="50" ry="34" fill="{col}" transform="rotate(-16 -4 -62)"/>'
            f'<path d="M-36 -64 Q-6 -86 30 -66 Q8 -36 -36 -40Z" fill="{dk}"/>')
    if black:
        body += stroke("M-26 -80 Q0 -94 22 -84", RAVEN_SHEEN, 4)
    head = (f'<circle cx="38" cy="-104" r="26" fill="{col}"/>'  # shaggy raven throat hackles below the beak
            f'<path d="M26 -84 L32 -66 L38 -78 L44 -62 L48 -78 L56 -66 L58 -86 Q44 -80 26 -84Z" fill="{dk}"/>')
    if mood == "cough":
        head += '<path d="M56 -120 Q84 -122 96 -112 L60 -104Z M58 -100 L90 -94 Q74 -88 58 -90Z" fill="#3E3E48"/>'
        eyes = eye(44, -110, 7, iris, "#fff" if black else INK, "shut")
    else:
        head += '<path d="M54 -120 Q86 -122 100 -104 Q90 -100 82 -98 Q70 -94 56 -92Z" fill="#3E3E48"/>'
        eyes = eye(44, -110, 7, iris, pup)
    legs = stroke("M-12 -30 V0 M8 -30 V0 M-12 0 l-10 4 M-12 0 l8 4 M8 0 l-10 4 M8 0 l10 4", "#6A6470", 4)
    return group(x, y, s, flip, 0, legs + body + head + eyes)


def owl(x: float, y: float, kind: str, *, after: bool = False, mood: str = "open") -> str:
    """Front-facing owl. screech = small grey with little ear tufts; hooting = round brown head; horned = big tufts."""
    col, dk, face_c = OWL[kind]
    s = SIZE[kind]
    tufts = ""
    if kind == "screech":
        tufts = f'<path d="M-30 -104 L-24 -126 L-12 -108Z M30 -104 L24 -126 L12 -108Z" fill="{col}"/>'
    elif kind == "horned":
        tufts = f'<path d="M-30 -102 L-30 -140 L-10 -110Z M30 -102 L30 -140 L10 -110Z" fill="{col}"/>'
    body = (f'<path d="M-36 0 Q-46 -62 -32 -94 Q0 -116 32 -94 Q46 -62 36 0 Q0 8 -36 0Z" fill="{col}"/>'
            f'<path d="M-36 -10 Q-50 -50 -34 -70 Q-26 -40 -20 -6Z M36 -10 Q50 -50 34 -70 Q26 -40 20 -6Z" fill="{dk}"/>'
            + stroke(" ".join(f"M{a - 5} {b} l5 5 l5 -5" for a, b in [(-10, -40), (8, -36), (-2, -24), (14, -20), (-16, -18)]), dk, 2.6))
    if kind == "hooting":
        body += stroke("M-26 -52 Q0 -46 26 -52 M-28 -60 Q0 -54 28 -60", dk, 2.4)
    face = f'<ellipse cx="0" cy="-84" rx="31" ry="23" fill="{face_c}"/>'
    rings = ""
    if after and kind == "screech":
        rings = "".join(f'<circle cx="{sx * 13}" cy="-86" r="12.5" fill="none" stroke="#E25A48" stroke-width="3.4"/>' for sx in (-1, 1))
    elif after:
        rings = "".join(f'<circle cx="{sx * 13}" cy="-86" r="15" fill="#fff"/>' for sx in (-1, 1))
    eyes = eye(-13, -86, 10, "#F7D35A", INK, mood) + eye(13, -86, 10, "#F7D35A", INK, mood)
    beak = '<path d="M-5 -76 L5 -76 L0 -64Z" fill="#D9963A"/>'
    feet = stroke("M-14 0 l-5 5 M-14 0 v6 M-14 0 l5 5 M14 0 l-5 5 M14 0 v6 M14 0 l5 5", "#D9963A", 3.4)
    return group(x, y, s, False, 0, feet + tufts + body + face + rings + eyes + beak)


def snake(x: float, y: float, s: float = SIZE["snake"], *, black: bool = False, pose: str = "up", flip: bool = False,
          mood: str = "smile") -> str:
    """The racer: a slim friendly snake. Pale grey-green before the fire, black after."""
    col, ln = (SNAKE_BLK, SNAKE_BLK_D) if black else (SNAKE_PALE, SNAKE_PALE_D)
    if pose == "swim":
        path, hx, hy = "M-110 0 Q-90 -16 -66 -2 Q-40 14 -16 -2 Q8 -18 32 -4 Q48 6 60 -6", 72, -12
    elif pose == "coil":
        path, hx, hy = "M-30 -10 Q-46 -8 -40 -2 Q-36 6 0 6 Q40 6 40 -8 Q40 -22 0 -22 Q-26 -22 -18 -34 Q-6 -44 20 -50 Q34 -56 34 -66", 44, -74
    else:
        path, hx, hy = "M-96 -4 Q-70 -16 -40 -6 Q-6 6 20 -6 Q44 -18 40 -44 Q36 -66 54 -76", 66, -80
    body = stroke(path, col, 15) + stroke(path, ln, 3)
    head = (f'<ellipse cx="{hx}" cy="{hy}" rx="17" ry="12" fill="{col}"/>' + eye(hx + 4, hy - 4, 5, "#fff", INK, "shut" if mood == "shut" else "open")
            + stroke(f"M{hx + 6} {hy + 5} q5 3 9 -1", "#F2A9B0" if black else INK, 2.2))
    return group(x, y, s, flip, 0, body + head)


# ---------- scenery ----------

def thunder(x: float, y: float, s: float = 1) -> str:
    """The Thunders' storm cloud: plain, no face (the Thunders are sacred beings in the story)."""
    inner = ('<g fill="#57627F"><circle cx="-70" cy="10" r="40"/><circle cx="-24" cy="-22" r="52"/><circle cx="36" cy="-10" r="46"/>'
             '<circle cx="84" cy="14" r="34"/><rect x="-104" y="10" width="220" height="40" rx="20"/></g>'
             + '<path d="M-60 -36 Q-24 -70 20 -50" stroke="#7B87A6" stroke-width="8" fill="none" stroke-linecap="round"/>'
             + '<path d="M-96 44 Q-40 30 0 40 Q50 52 110 40 L112 50 H-100Z" fill="#46506B"/>')
    return group(x, y, s, False, 0, inner)


def bolt(d: str) -> str:
    """A zig-zag lightning bolt along path d, with a soft glow."""
    return (f'<g filter="url(#p)">{stroke(d, "#FFF3B0", 22)}</g>'.replace('stroke-width="22"', 'stroke-width="22" opacity=".35"')
            + stroke(d, "#FFF3B0", 9))


def sycamore(x: float = IX, y: float = IY, s: float = 1, *, fire: bool = True, smoke: bool = True, heat: bool = False) -> str:
    """A tall pale hollow sycamore with a broken-off top; the fire burns in a hollow at the bottom."""
    br = stroke("M-18 -118 Q-50 -150 -84 -158 M-62 -152 l-14 -24 M18 -138 Q50 -164 88 -170 M64 -166 l10 -22 M-14 -70 Q-40 -84 -58 -80",
                BARK, 9) + stroke("M-84 -158 l-16 6 M88 -170 l14 8", BARK, 5)
    trunk = (f'<path d="M-30 0 Q-22 -90 -20 -176 L-26 -200 L-12 -190 L-4 -206 L6 -190 L16 -202 L20 -176 Q24 -90 30 0Z" fill="{BARK}"/>'
             f'<path d="M12 -180 Q16 -90 30 0 H14 Q8 -90 4 -180Z" fill="{BARK_D}" opacity=".6"/>'
             f'<g fill="{BARK_P}"><ellipse cx="-10" cy="-150" rx="7" ry="10"/><ellipse cx="8" cy="-110" rx="6" ry="9"/>'
             '<ellipse cx="-12" cy="-84" rx="8" ry="6"/><ellipse cx="14" cy="-60" rx="5" ry="8"/><ellipse cx="-4" cy="-122" rx="4" ry="5"/></g>'
             '<path d="M-15 0 V-26 Q0 -44 15 -26 V0Z" fill="#3A2A22"/>')
    fl = ""
    if fire:
        fl = (f'<circle cx="0" cy="-14" r="34" fill="{FLAME}" opacity=".25"/>'
              f'<path d="M-12 0 Q-14 -18 -4 -30 Q-2 -18 4 -22 Q12 -14 12 0Z" fill="{FIRE}"/>'
              f'<path d="M-6 0 Q-6 -12 0 -18 Q6 -10 6 0Z" fill="{FLAME}"/>')
    sm = puffs([(0, -214, 9), (-8, -232, 12), (6, -254, 15), (-4, -280, 18)], "#8E949E", .75) if smoke else ""
    ht = stroke("M-50 -60 q-6 -10 0 -20 q6 -10 0 -20 M50 -70 q-6 -10 0 -20 q6 -10 0 -20 M-40 -170 q-6 -10 0 -20 M44 -190 q6 -10 0 -20",
                "#FFD9A0", 3) if heat else ""
    return group(x, y, s, False, 0, sm + br + trunk + fl + ht, True)


def island(x: float = IX, y: float = IY) -> str:
    return (f'<ellipse cx="{x}" cy="{y + 6}" rx="130" ry="24" fill="{ISLE}" filter="url(#p)"/>'
            f'<ellipse cx="{x - 50}" cy="{y}" rx="40" ry="8" fill="{SNOW}" opacity=".9"/><ellipse cx="{x + 70}" cy="{y + 4}" rx="30" ry="6" fill="{SNOW}" opacity=".9"/>'
            + stroke(" ".join(f"M{x + d} {y - 2} l-3 -10 M{x + d} {y - 2} l3 -10" for d in (-100, -80, 90, 110)), ISLE_D, 2.6))


def far_hills(top: float = 286) -> str:
    return (f'<path d="M0 {top + 14} Q120 {top - 40} 260 {top} Q380 {top - 30} 520 {top + 4} Q660 {top - 44} 800 {top + 6} V{top + 40} H0Z" fill="{HILL}"/>'
            f'<path d="M0 {top + 26} Q200 {top - 6} 400 {top + 20} T800 {top + 18} V{top + 40} H0Z" fill="{HILL_D}" opacity=".6"/>')


def lake(top: float = 300) -> str:
    rip = " ".join(f"M{a} {b} h{w}" for a, b, w in [(60, 340, 40), (220, 360, 30), (400, 380, 46), (680, 352, 34), (120, 420, 36),
                                                     (320, 440, 30), (520, 410, 40), (700, 440, 30), (240, 500, 44), (600, 500, 36)])
    return (f'<rect y="{top}" width="800" height="{600 - top}" fill="{LAKE}"/>'
            f'<rect y="{top}" width="800" height="10" fill="{LAKE_L}" opacity=".5"/>'
            f'<g opacity=".55">{stroke(rip, LAKE_L, 3)}</g>')


def shore(y: float = 470, col: str = SNOW) -> str:
    return (f'<path filter="url(#p)" d="M0 {y} Q260 {y - 30} 480 {y - 6} T800 {y + 4} V600 H0Z" fill="{col}"/>'
            f'<path d="M0 {y + 60} Q300 {y + 40} 560 {y + 58} T800 {y + 50} V600 H0Z" fill="{SNOW_D}" opacity=".5"/>')


def snowflakes(pts: list, op: float = .85) -> str:
    return f'<g fill="#fff" opacity="{op}">' + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>'


def star(x: float, y: float, s: float = 1) -> str:
    return (f'<polygon transform="translate({x} {y}) scale({s})" points="0,-8 2,-2.6 7.6,-2.5 3,1 4.7,6.5 0,3.2 -4.7,6.5 -3,1 -7.6,-2.5 -2,-2.6" fill="#F3F3FA"/>')


def campfire(x: float, y: float, s: float = 1) -> str:
    inner = ('<g fill="#8A5A36"><rect x="-56" y="-12" width="112" height="16" rx="8" transform="rotate(12)"/>'
             '<rect x="-56" y="-12" width="112" height="16" rx="8" transform="rotate(-12)"/></g>'
             f'<path d="M-34 -6 Q-44 -46 -16 -80 Q-14 -50 0 -60 Q-4 -100 20 -120 Q22 -80 36 -64 Q46 -38 34 -6Z" fill="{FIRE}"/>'
             f'<path d="M-18 -6 Q-22 -34 -4 -54 Q0 -36 10 -44 Q24 -26 18 -6Z" fill="{FLAME}"/>'
             '<g fill="#FFD27A"><circle cx="-30" cy="-120" r="3"/><circle cx="26" cy="-140" r="2.6"/><circle cx="6" cy="-160" r="2.2"/></g>')
    return group(x, y, s, False, 0, inner)


def fire_glow(x: float, y: float) -> str:
    """Soft warm light around the campfire; drawn behind the animals so it never tints them."""
    return "".join(f'<ellipse cx="{x}" cy="{y - 30}" rx="{rx}" ry="{rx * .6:.0f}" fill="{FLAME}" opacity=".09"/>' for rx in (170, 130, 95, 65))


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/waterspider-{n:02d}.svg", "w") as fh:
        fh.write(doc)


FLAKES = snowflakes([(60, 60, 3), (150, 130, 2.4), (240, 50, 3), (330, 160, 2.2), (420, 80, 3), (700, 60, 2.6), (760, 170, 2.2),
                     (640, 230, 2.4), (90, 220, 2.6), (300, 250, 2), (470, 210, 2.2)])


def lakeside(fire: bool = True, smoke: bool = True, heat: bool = False) -> list:
    return [FLAKES, far_hills(), lake(), island(), sycamore(fire=fire, smoke=smoke, heat=heat), shore()]


# 01 cover — Water Spider skating toward the island, bowl empty
svg(1, "Water Spider Brings the Fire", "Paper-cut cover: on a cold blue evening, a little round black water spider with red stripes, big friendly eyes and a small woven bowl on her back skates across a lake, leaving ripples. Ahead of her, on a small snowy island, a tall pale sycamore tree glows orange at the bottom, with grey smoke curling out of its top.", DUSK, [
    star(80, 60, 1.2), star(200, 120, .9), star(340, 50, 1), star(720, 70, 1.1), star(760, 210, .8), star(460, 110, .7),
    far_hills(), lake(), island(), sycamore(), spider(250, 470, 1.5, skate=True),
    stroke("M120 520 Q260 506 420 520", "#fff", 2.4)])

# 02 the world is cold
svg(2, "The world was cold", "Paper-cut scene: on a snowy lake shore with snowflakes falling, six animals shiver in a row with frosty breath: a big pale silver-white raven, a little grey screech owl, a brown hooting owl, a big brown horned owl with tall ear tufts, a pale grey-green snake, and the tiny black water spider with her red stripes. Across the lake, a bare pale tree stands on a little island.", COLD, [
    *lakeside(fire=False, smoke=False),
    raven(130, 560), owl(255, 556, "screech"), owl(350, 558, "hooting"), owl(450, 558, "horned"),
    snake(570, 560), spider(705, 560, bowl_on=False),
    puffs([(222, 462, 7), (238, 452, 5), (250, 444, 3.4)]),
    shiver(255, 500, 26, 38), shiver(705, 525, 18, 40), shiver(450, 470, 30, 54), snowflakes([(120, 400, 3), (520, 420, 2.6), (690, 400, 2.4)])])

# 03 the Thunders send lightning
svg(3, "The Thunders send their lightning", "Paper-cut scene: a big dark storm cloud — the Thunders — sends a bright zig-zag bolt of lightning down onto the top of a tall pale hollow sycamore tree on a little island in a lake. At the bottom of the tree, inside a hollow, an orange fire begins to glow.", STORM, [
    far_hills(366), lake(380), island(IX, 420), sycamore(IX, 420, smoke=False), thunder(250, 110, 1.05),
    bolt("M330 160 L400 186 L376 200 L470 214 L446 226 L556 218"),
    stroke("M590 200 l16 -12 M600 226 l20 -2 M530 190 l-8 -16", "#FFF3B0", 4), shore(560)])

# 04 the animals see the smoke — who will bring the fire?
svg(4, "Who will bring the fire?", "Paper-cut scene: on the snowy shore, the raven, the three owls, the pale snake and the tiny water spider gather together and look across the lake at the island, where grey smoke curls out of the top of the tall tree and an orange glow shines at its bottom.", COLD, [
    *lakeside(),
    raven(120, 560), owl(240, 556, "screech"), owl(330, 558, "hooting"), owl(425, 558, "horned"),
    snake(540, 562), spider(670, 560, bowl_on=False)])

# 05 Raven flies to the tree
svg(5, "Raven flies to the fire", "Paper-cut scene: the big pale silver-white raven flies with wings spread over the lake toward the tall tree on the island, where wavy lines of heat rise around the trunk and smoke curls from the top. On the snowy shore below, the screech owl, the hooting owl, the horned owl, the pale snake and the little water spider watch.", COLD, [
    *lakeside(heat=True), raven(380, 260, .9, pose="fly"),
    owl(110, 556, "screech"), owl(200, 558, "hooting"), owl(300, 558, "horned"), snake(420, 562), spider(545, 560, bowl_on=False)])

# 06 Raven comes back black
svg(6, "Raven comes back black", "Paper-cut scene: on the snowy shore, the raven is back without the fire. He is now glossy black all over, with his eyes squeezed shut, coughing out little grey puffs of smoke. On his left the screech owl, the hooting owl and the horned owl stare at him; on his right the pale snake and the tiny water spider look on.", COLD, [
    *lakeside(), owl(110, 556, "screech"), owl(200, 558, "hooting"), owl(295, 558, "horned"),
    raven(450, 560, black=True, mood="cough"), puffs([(548, 450, 7), (566, 436, 9), (584, 418, 11)], "#8E949E", .8),
    snake(600, 562), spider(720, 560, bowl_on=False)])

# 07 Screech Owl comes back with red eyes
svg(7, "Screech Owl's red eyes", "Paper-cut scene: on the snowy shore the little grey screech owl has come back from the fire, blinking sleepily, with a thin red ring around each yellow eye and a small puff of smoke above his head. The black raven, the hooting owl, the horned owl, the pale snake and the tiny water spider stand beside him.", COLD, [
    *lakeside(), raven(120, 560, black=True), owl(280, 556, "screech", after=True, mood="blink"),
    puffs([(280, 446, 8), (296, 434, 6), (266, 436, 6)], "#8E949E", .75),
    owl(385, 558, "hooting"), owl(485, 558, "horned"), snake(600, 562), spider(722, 560, bowl_on=False)])

# 08 Hooting Owl and Horned Owl come back with white rings
svg(8, "White rings around their eyes", "Paper-cut scene: on the snowy shore the brown hooting owl and the big horned owl have come back from the fire, blinking, wide-eyed, each with big white rings around both eyes and little grey ash specks floating around them. The black raven, the screech owl with his red-rimmed eyes, the pale snake and the tiny water spider stand beside them.", COLD, [
    *lakeside(), raven(115, 560, black=True), owl(235, 556, "screech", after=True),
    owl(355, 558, "hooting", after=True), owl(470, 558, "horned", after=True),
    puffs([(330, 430, 3), (390, 420, 2.6), (440, 410, 3), (500, 400, 2.6), (360, 404, 2.2)], "#9AA0AA", .9),
    snake(600, 562), spider(722, 560, bowl_on=False)])

# 09 the racer swims back, black and zig-zagging
svg(9, "The racer zips home", "Paper-cut scene: across the lake, a slim snake — now black all over — swims quickly back from the island in a zig-zag, leaving a wiggly white wake behind him, while a puff of smoke drifts from the little hole at the bottom of the tree. On the snowy shore, the black raven, the screech owl with red-rimmed eyes, the hooting owl and the horned owl with white rings round their eyes, and the tiny water spider watch.", COLD, [
    *lakeside(), stroke("M476 396 l18 -12 l16 14 l18 -12 l16 14 l18 -12", "#fff", 3), puffs([(590, 302, 7), (604, 290, 9)], "#8E949E", .8),
    snake(380, 404, black=True, pose="swim", flip=True),
    raven(115, 560, black=True), owl(235, 556, "screech", after=True), owl(330, 558, "hooting", after=True),
    owl(430, 558, "horned", after=True), spider(560, 560, bowl_on=False)])

# 10 "I will!" — Water Spider weaves her bowl
svg(10, "Water Spider weaves a bowl", "Paper-cut scene: on the snowy shore, the tiny black water spider with red stripes stands in the middle, smiling, with a freshly woven little tan bowl on her back and loops of white silk thread and sparkles around her. The black raven and the screech owl with red-rimmed eyes stand on her left; the hooting owl and the horned owl with white eye-rings and the black snake, curled up, stand on her right.", COLD, [
    *lakeside(), raven(115, 560, black=True), owl(235, 556, "screech", after=True), spider(380, 560, weave=True),
    owl(500, 558, "hooting", after=True), owl(600, 558, "horned", after=True), snake(705, 562, black=True, pose="coil")])

# 11 skate, skate, skate across the water!
svg(11, "Skate, skate, skate across the water!", "Paper-cut scene: the little water spider, with her empty woven bowl on her back, skates fast across the top of the lake, her eight feet making tiny white ripples and speed lines behind her. Ahead, on the island, the tall tree glows orange at the bottom with smoke curling out of the top.", COLD, [
    FLAKES, far_hills(), lake(), island(), sycamore(),
    spider(290, 470, SPIDER_LAKE, skate=True), stroke("M100 500 Q200 486 300 500", "#fff", 2.4)])

# 12 one little ember — and back she comes
svg(12, "One little ember", "Paper-cut scene: the little water spider skates back across the lake under the evening stars, smiling, with one small glowing orange ember in the woven bowl on her back, shining warm light around her. Behind her, the tall tree on the island still glows and smokes.", DUSK, [
    star(90, 60, 1), star(240, 110, .8), star(700, 70, 1.1), star(430, 50, .8),
    far_hills(), lake(), island(), sycamore(),
    spider(330, 490, SPIDER_LAKE, skate=True, ember=True, flip=True), stroke("M420 520 Q520 506 640 520", "#fff", 2.4)])

# 13 everyone warm around the fire
svg(13, "Warm at last", "Paper-cut scene: in warm golden light on the shore, a big campfire crackles in the middle. Around it everyone is warm and smiling: the black raven, the screech owl with red-rimmed eyes and the hooting owl on the left; the horned owl with white eye-rings, the curled-up black snake and the tiny water spider, proud with her woven bowl on her back, on the right.", WARM, [
    far_hills(), lake(), island(), sycamore(fire=False, smoke=False), shore(470, "#F6EEDF"),
    fire_glow(405, 556), raven(118, 560, black=True), owl(222, 556, "screech", after=True), owl(302, 558, "hooting", after=True),
    campfire(405, 556, .9), owl(515, 558, "horned", after=True), snake(612, 562, black=True, pose="coil"), spider(720, 560, mood="proud")])
