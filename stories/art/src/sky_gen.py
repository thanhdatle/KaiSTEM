#!/usr/bin/env python3
"""Generates the 13 Why-the-Sky-Is-High flip-book SVGs from shared parts.

Usage: python3 sky_gen.py <output-dir>
Scale is fixed: the woman and the man are always drawn at P = 1.4 with feet on y = 520,
the child at 1.0, the hut at 1.1. The low sky's underside sits at y = 250 (pages 1-5),
then 236 after it creaks up "a teeny bit" (pages 6-9). From page 10 the sky is high.
The comb and the bead necklace hang on the low sky from page 4, fly up on page 10, are not
seen on pages 11-12, and come back as the moon (comb) and the stars (beads) on page 13.
"""
import math
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SKIN, SKIN_D, HAIR = "#B9784A", "#94592F", "#2B1D18"
BLOUSE, SKIRT, STRIPE = "#E9785A", "#6C4AA0", "#F2C14E"
SHIRT, PANTS, KIDTOP = "#F3EFE2", "#3D5A80", "#3FA7A0"
WOOD, WOOD_D, RICE = "#8A5A33", "#5E3B20", "#FBF6E9"
COMB, COMB_D = "#E0A443", "#A86F22"
BEAD, BEAD2 = "#FFF7DA", "#F6D77A"
SKYLOW, SKYLOW_D, SKYLOW_L = "#6FB3E0", "#4E93C4", "#A6D3F0"
GRASS, GRASS_D = "#7CC46A", "#4F9A4E"
PADDY = "#B9DE8A"
THATCH, THATCH_D, BAMBOO, BAMBOO_D = "#C9A35A", "#9C7A38", "#EBD39C", "#C2A066"
PALM_T, LEAF, LEAF_D = "#A9764A", "#3F9A56", "#2C7A44"
BONK = "#FFD23F"
P = 1.4
FEET = 520
LOW, LOW2 = 250, 236
DAY = [(0, "#CDE9F7"), (1, "#FFF3DC")]
HIGH = [(0, "#4FA7E0"), (1, "#E3F3FB")]
DUSK = [(0, "#5B5BA6"), (.55, "#E99A8B"), (1, "#FFD9A0")]
NIGHT = [(0, "#141B4A"), (1, "#3B4590")]


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, inner: str, flip: bool = False, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


def to_local(wy: float, s: float = P, feet: float = FEET) -> float:
    """World y -> person-local y (feet at 0)."""
    return round((wy - feet) / s, 1)


# ---------- small things ----------

def comb_shape(x: float, y: float, s: float = 1, fill: str = COMB, dark: str = COMB_D) -> str:
    """A half-round hair comb: curved back on top, teeth along the flat bottom edge. (x, y) is the middle of the flat edge."""
    teeth = "".join(f'<rect x="{-20 + 4 * i:.1f}" y="-1" width="2.4" height="9" rx="1" fill="{fill}"/>' for i in range(11))
    return (f'<g transform="translate({x} {y}) scale({s})">{teeth}<path d="M-22 0 A22 17 0 0 1 22 0Z" fill="{fill}"/>'
            f'<path d="M-14 -3 A14 9 0 0 1 14 -3" stroke="{dark}" stroke-width="2.2" fill="none"/>'
            f'<circle cx="-7" cy="-8" r="2" fill="{dark}"/><circle cx="6" cy="-10" r="2" fill="{dark}"/></g>')


def necklace_loop(x: float, y: float, s: float = 1) -> str:
    """The bead necklace hanging in a U from a point (x, y)."""
    pts = [(-16, 4), (-18, 14), (-17, 24), (-13, 33), (-6, 39), (2, 41), (9, 38), (15, 31), (18, 22), (18, 12), (16, 3)]
    beads = "".join(f'<circle cx="{a}" cy="{b}" r="4.4" fill="{BEAD if i % 2 else BEAD2}" stroke="#C9A64A" stroke-width="1"/>'
                    for i, (a, b) in enumerate(pts))
    return f'<g transform="translate({x} {y}) scale({s})">{stroke("M-16 4 Q0 -4 16 3", "#8C6A2E", 2)}{beads}</g>'


def bonk(x: float, y: float, s: float = 1) -> str:
    pts = " ".join(f"{(34 if i % 2 == 0 else 15) * math.cos(math.pi * i / 8):.1f},{(34 if i % 2 == 0 else 15) * math.sin(math.pi * i / 8):.1f}"
                   for i in range(16))
    return (f'<g transform="translate({x} {y}) scale({s})"><polygon points="{pts}" fill="{BONK}" stroke="#E89B1A" stroke-width="3"/>'
            '<circle r="7" fill="#fff"/></g>')


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def chicken(x: float, y: float, s: float = 1, flip: bool = False) -> str:
    inner = (stroke("M-4 0 V-12 M6 0 V-12", "#E09A2B", 3) + '<path d="M-26 -30 Q-34 -50 -18 -46 Q-24 -34 -14 -30Z" fill="#7A4A2A"/>'
             '<ellipse cx="0" cy="-26" rx="22" ry="16" fill="#F4EEE0"/><circle cx="16" cy="-42" r="10" fill="#F4EEE0"/>'
             '<path d="M12 -52 q3 -8 6 -1 q3 -8 6 0 q2 4 -4 5Z" fill="#E5533D"/><path d="M25 -43 l9 3 l-9 3Z" fill="#E09A2B"/>'
             '<circle cx="19" cy="-44" r="2" fill="#2B2320"/><path d="M20 -36 q3 5 0 8 q-4 -3 0 -8Z" fill="#E5533D"/>'
             + stroke("M-10 -26 Q0 -18 8 -26", "#D8CDB4", 3))
    return group(x, y, s, inner, flip)


# ---------- people ----------

def face(mood: str = "smile", up: bool = False) -> str:
    dy = -2.2 if up else 0
    eyes = "".join(f'<circle cx="{sx}" cy="{-130 + dy}" r="2.6" fill="{INK}"/>' for sx in (-7, 7))
    if mood == "big":
        m = f'<path d="M-8 -121 Q0 -110 8 -121Z" fill="{INK}"/>'
    elif mood == "oh":
        m = f'<ellipse cy="-117" rx="3.4" ry="4.4" fill="{INK}"/>'
    elif mood == "oof":
        eyes = stroke("M-10 -131 l5 2 l-5 2 M10 -131 l-5 2 l5 2", INK, 1.8)
        m = stroke("M-6 -118 q3 -3 6 0 q3 3 6 0", INK, 1.8)
    else:
        m = stroke("M-6 -120 Q0 -114 6 -120", INK, 1.8)
    ch = '<circle cx="-12" cy="-122" r="3.6" fill="#E9604F" opacity=".45"/><circle cx="12" cy="-122" r="3.6" fill="#E9604F" opacity=".45"/>'
    return eyes + m + ch


def arm(sx: float, sy: float, hx: float, hy: float, col: str) -> str:
    """A straight arm; a hand raised high above the head bends out at an elbow so the arm passes outside the face."""
    mid = ""
    if hy < -150 and abs(hx) < 26:
        mid = f" L{sx + (20 if sx > 0 else -20)} -138"
    return stroke(f"M{sx} {sy}{mid} L{hx} {hy}", col, 9) + f'<circle cx="{hx}" cy="{hy}" r="5.6" fill="{SKIN}"/>'


def mortar(x: float = 46) -> str:
    """The wooden rice mortar (lusong), waist-high; its top is at local y = -50."""
    return (f'<path d="M{x - 26} -50 Q{x - 14} -30 {x - 16} -16 Q{x - 24} -6 {x - 24} 0 H{x + 24} Q{x + 24} -6 {x + 16} -16 Q{x + 14} -30 {x + 26} -50Z" fill="{WOOD}"/>'
            f'<ellipse cx="{x}" cy="-50" rx="26" ry="6" fill="{WOOD_D}"/><ellipse cx="{x}" cy="-50" rx="19" ry="3.6" fill="{RICE}"/>'
            + stroke(f"M{x - 12} -28 Q{x} -24 {x + 12} -28", WOOD_D, 2))


def pestle(x1: float, y1: float, x2: float, y2: float) -> str:
    """The long wooden pestle, from top end (x1, y1) to bottom end (x2, y2)."""
    return stroke(f"M{x1} {y1} L{x2} {y2}", "#C88A52", 9) + stroke(f"M{x1} {y1} L{x2} {y2}", "#E2AA6E", 3)


def woman(x: float, hands: tuple, mood: str = "smile", up: bool = False, comb: bool = True, beads: bool = True,
          tool: str = "", tip: float = 0, toes: bool = False) -> str:
    """The rice-pounding woman, feet at (x, FEET), with her mortar to her right.
    hands = ((lx, ly), (rx, ry)) in local units. tool: 'up' (pestle upright over the mortar, top at local y = tip),
    'lean' (pestle leaning on the mortar) or '' (no mortar)."""
    lift = -6 if toes else 0
    out = ""
    if tool:
        out += mortar()
    if tool == "up":
        out += pestle(46, tip, 46, min(tip + 120, -50))
    elif tool == "lean":
        out += pestle(92, -168, 60, -50)
    feet = (f'<ellipse cx="-10" cy="{-2 + lift}" rx="8" ry="4" fill="{SKIN_D}"/><ellipse cx="10" cy="{-2 + lift}" rx="8" ry="4" fill="{SKIN_D}"/>'
            + (stroke("M-10 -2 V-8 M10 -2 V-8", SKIN_D, 5) if toes else ""))
    body = (f'<g transform="translate(0 {lift})">'
            f'<path d="M-24 -76 Q-30 -34 -26 -6 H26 Q30 -34 24 -76Z" fill="{SKIRT}"/>'
            + stroke("M-27 -52 H27 M-27 -42 H27 M-26 -20 H26", STRIPE, 3)
            + f'<rect x="-5" y="-114" width="10" height="10" fill="{SKIN}"/>'
            f'<path d="M-22 -74 Q-25 -100 -12 -108 H12 Q25 -100 22 -74Z" fill="{BLOUSE}"/>'
            + stroke("M-12 -108 Q0 -100 12 -108", "#F7B49B", 2.4))
    if beads:
        body += "".join(f'<circle cx="{a}" cy="{b}" r="2.6" fill="{BEAD if i % 2 else BEAD2}" stroke="#C9A64A" stroke-width=".8"/>'
                        for i, (a, b) in enumerate([(-10, -107), (-7, -103), (-3.5, -101), (0, -100.5), (3.5, -101), (7, -103), (10, -107)]))
    head = (f'<circle cx="-15" cy="-146" r="10" fill="{HAIR}"/><circle cy="-128" r="20" fill="{SKIN}"/>'
            f'<path d="M-20 -128 Q-22 -150 0 -150 Q20 -150 21 -132 Q10 -142 -6 -140 Q-14 -138 -20 -128Z" fill="{HAIR}"/>')
    if comb:
        head += comb_shape(-15, -152, .42)
    head += face(mood, up)
    (lx, ly), (rx, ry) = hands
    arms = arm(-14, -102, lx, ly, "#C9573C") + arm(14, -102, rx, ry, BLOUSE)
    out += feet + body + head + arms + "</g>"
    return group(x, FEET, P, out)


def man(x: float, hands: tuple, mood: str = "smile", up: bool = False, s: float = P, feet: float = FEET, kid: bool = False) -> str:
    """A villager in a white shirt and blue trousers, or (kid=True) a little boy in a teal top and blue shorts."""
    top = KIDTOP if kid else SHIRT
    legs = (stroke("M-10 -62 L-11 -6 M10 -62 L11 -6", PANTS, 13) if not kid else
            f'<path d="M-20 -64 H20 L20 -40 H-20Z" fill="{PANTS}"/>' + stroke("M-10 -40 L-11 -6 M10 -40 L11 -6", SKIN, 8))
    out = (legs + f'<ellipse cx="-12" cy="-2" rx="9" ry="4.4" fill="{SKIN_D}"/><ellipse cx="12" cy="-2" rx="9" ry="4.4" fill="{SKIN_D}"/>'
           f'<rect x="-5" y="-114" width="10" height="10" fill="{SKIN}"/>'
           f'<path d="M-22 -60 Q-25 -100 -12 -108 H12 Q25 -100 22 -60Z" fill="{top}"/>'
           + stroke("M-6 -108 L0 -98 L6 -108", "#C9C2AE" if not kid else "#2C807A", 2.4)
           + f'<circle cy="-128" r="20" fill="{SKIN}"/>'
           f'<path d="M-20 -128 Q-23 -152 0 -151 Q23 -152 20 -128 Q18 -140 6 -142 Q-6 -136 -20 -128Z" fill="{HAIR}"/>'
           + face(mood, up))
    (lx, ly), (rx, ry) = hands
    out += arm(-14, -102, lx, ly, top) + arm(14, -102, rx, ry, top)
    return group(x, feet, s, out)


# ---------- places ----------

def low_sky(level: float) -> str:
    """The low sky: a thick blue ceiling, bumpy underneath like coral rock, filling the top of the picture down to y = level."""
    d = f"M0 0 H800 V{level}" + "".join(f" Q{775 - x} {level + (14 if (x // 50) % 2 else 9)} {750 - x} {level}" for x in range(0, 800, 50)) + "Z"
    top = max(int(level - 30), 12)
    pores = "".join(f'<circle cx="{(37 * i) % 790 + 8}" cy="{(53 * i) % top + 10}" r="{3 + i % 3}" fill="{SKYLOW_D}" opacity=".35"/>'
                    for i in range(46))
    shine = "".join(f'<circle cx="{(71 * i + 20) % 780 + 10}" cy="{(29 * i) % top + 12}" r="{4 + i % 2}" fill="{SKYLOW_L}" opacity=".55"/>'
                    for i in range(22))
    return (f'<g filter="url(#p)"><path d="{d}" fill="{SKYLOW}"/></g>{pores}{shine}'
            + stroke(f"M0 {level - 6}" + "".join(f" Q{x + 25} {level + 4} {x + 50} {level - 6}" for x in range(0, 800, 50)), SKYLOW_D, 3))


def cloud(x: float, y: float, s: float = 1, mood: str = "", op: float = .96) -> str:
    body = (f'<g fill="#fff" opacity="{op}"><circle cx="-40" cy="6" r="24"/><circle cx="-8" cy="-10" r="30"/><circle cx="30" cy="-2" r="26"/>'
            '<rect x="-64" y="4" width="122" height="28" rx="14"/></g>')
    f = ""
    if mood:
        if mood == "sleep":
            f = stroke("M-20 4 q5 4 10 0 M6 4 q5 4 10 0", "#7C8FB0", 2.6)
        else:
            f = '<circle cx="-15" cy="4" r="3.2" fill="#56688C"/><circle cx="11" cy="4" r="3.2" fill="#56688C"/>'
        if mood == "oof":
            f += stroke("M-8 18 q4 -4 8 0", "#56688C", 2.6)
        elif mood == "oh":
            f += '<ellipse cx="-2" cy="18" rx="3.4" ry="4.4" fill="#56688C"/>'
        elif mood != "sleep":
            f += stroke("M-9 15 Q-2 22 5 15", "#56688C", 2.6)
        f += '<circle cx="-26" cy="14" r="4.6" fill="#F2A9B0" opacity=".6"/><circle cx="22" cy="14" r="4.6" fill="#F2A9B0" opacity=".6"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{body}{f}</g>'


def hut(x: float, s: float = 1.1, night: bool = False) -> str:
    """A bamboo house on stilts with a steep thatched roof and a little ladder. Base on the ground at (x, FEET)."""
    win = "#F6C445" if night else "#5E3B20"
    weave = stroke(" ".join(f"M{a} -126 L{a + 30} -62" for a in range(-100, 80, 18)) + " "
                   + " ".join(f"M{a} -126 L{a - 30} -62" for a in range(-70, 110, 18)), BAMBOO_D, 1.4)
    inner = (stroke("M-62 0 V-58 M-22 0 V-58 M22 0 V-58 M62 0 V-58", WOOD, 8)
             + f'<rect x="-80" y="-64" width="160" height="10" rx="3" fill="{WOOD_D}"/>'
             f'<rect x="-70" y="-126" width="140" height="64" fill="{BAMBOO}"/>'
             f'<g clip-path="url(#hw)">{weave}</g>'
             f'<rect x="-16" y="-116" width="30" height="54" rx="3" fill="#5E3B20"/>'
             f'<rect x="32" y="-114" width="26" height="22" rx="3" fill="{win}"/>'
             + stroke("M45 -114 V-92", BAMBOO_D, 2)
             + stroke("M-6 -56 L6 0 M14 -56 L26 0", WOOD, 4) + stroke("M-4 -44 H16 M-1 -30 H19 M2 -16 H22", WOOD, 3)
             + f'<path d="M-104 -120 L-8 -206 Q0 -212 8 -206 L104 -120 Q0 -112 -104 -120Z" fill="{THATCH}"/>'
             + stroke("M-80 -122 L-6 -198 M-50 -118 L-3 -202 M-20 -116 L0 -204 M20 -116 L3 -202 M50 -118 L6 -198 M80 -122 L8 -194", THATCH_D, 2.2)
             + stroke("M-102 -120 Q0 -110 102 -120", THATCH_D, 5))
    return group(x, FEET, s, inner)


def palm(x: float, base: float, cx: float, cy: float, s: float = 1, night: bool = False) -> str:
    """A coconut palm from (x, base) with its crown at (cx, cy) — bent if the sky is pressing on it."""
    mx, my = (x + cx) / 2 + 40, (base + cy) / 2
    trunk = stroke(f"M{x} {base} Q{mx:.0f} {my:.0f} {cx} {cy}", "#6E4C2E" if night else PALM_T, 15 * s)
    leaf_c = "#25553A" if night else LEAF
    leaf_d = "#1C4430" if night else LEAF_D
    leaves = "".join(f'<path d="M0 0 Q40 -34 92 -4 Q44 -16 0 0Z" fill="{leaf_c if i % 2 else leaf_d}" transform="rotate({a})"/>'
                     for i, a in enumerate([-160, -125, -55, -20, 15, 160, 195]))
    nuts = '<circle cx="-6" cy="8" r="7" fill="#7A5230"/><circle cx="7" cy="10" r="7" fill="#8A5E36"/>'
    return f'<g filter="url(#p)">{trunk}<g transform="translate({cx} {cy}) scale({s})">{leaves}{nuts}</g></g>'


def ground(night: bool = False) -> str:
    g, gd, pd = (GRASS, GRASS_D, PADDY) if not night else ("#2F5A44", "#22412F", "#3B6A4C")
    return (f'<path d="M0 452 Q400 432 800 452 V600 H0Z" fill="{pd}"/>'
            + stroke(" ".join(f"M{x} 450 l-6 -14 M{x + 6} 450 l0 -16 M{x + 12} 450 l6 -14" for x in range(16, 800, 46)), gd, 2.4)
            + f'<path filter="url(#p)" d="M0 486 Q400 470 800 488 V600 H0Z" fill="{g}"/>'
            + f'<path d="M0 600 V572 Q400 548 800 576 V600Z" fill="{gd}"/>')


def hills(night: bool = False) -> str:
    c1, c2 = ("#9CCB8C", "#B6DAA0") if not night else ("#283C5E", "#33496E")
    return (f'<path d="M0 420 Q120 340 260 400 Q380 330 520 392 Q650 340 800 396 V470 H0Z" fill="{c1}"/>'
            f'<path d="M0 446 Q200 400 400 436 T800 432 V470 H0Z" fill="{c2}"/>')


# ---------- page writer ----------

def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<clipPath id="hw"><rect x="-70" y="-126" width="140" height="64"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '<radialGradient id="glow"><stop offset="0" stop-color="#FFF4C8" stop-opacity=".55"/><stop offset="1" stop-color="#FFF4C8" stop-opacity="0"/></radialGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/sky-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def on_pestle(tip: float) -> tuple:
    """Both hands gripping the upright pestle whose top is at local y = tip."""
    return ((36, tip + 100), (42, tip + 28))


TIP_DOWN = -170                      # pestle resting in the mortar (top at world y ~282)
TIP_LOW = to_local(LOW)              # raised until it bonks the sky at y = 250
TIP_LOW2 = to_local(LOW2)            # bonks the sky at y = 236
WX = 300                             # the woman's feet x; her pestle stands at PX
PX = WX + 46 * P

LOW_PALM = palm(100, 500, 130, LOW + 34)
LOW_PALM2 = palm(100, 500, 130, LOW2 + 34)
TALL_PALM = palm(110, 500, 120, 230)
COMB_AT, BEADS_AT = WX + 11, WX - 56


def hung(level: float) -> str:
    """The comb and the necklace hanging on the low sky at their usual spots."""
    return comb_shape(COMB_AT, level + 12, 1.0) + necklace_loop(BEADS_AT, level + 4, 1.1)


# 01 cover
svg(1, "Why the Sky Is High", "Paper-cut cover: long ago, in a village of green rice fields, the sky hangs very low — a thick, bumpy blue ceiling just above everyone's heads. A woman in a coral blouse and a purple striped skirt, with a comb in her hair and a bead necklace, lifts her long wooden pestle over her rice mortar, and the top of the pestle bonks the sky with a yellow burst. A little cloud squashed under the sky beside her says 'oof', another peeks out on the left by a bent coconut palm, a bamboo house on stilts stands on the right, and a white hen watches.", DAY, [
    hills(), ground(), LOW_PALM, hut(640),
    woman(WX, on_pestle(TIP_LOW), "big", True, tool="up", tip=TIP_LOW),
    low_sky(LOW), bonk(PX, LOW + 4, .9),
    cloud(500, LOW + 30, .62, "oof"), cloud(190, LOW + 26, .55, "oh"),
    chicken(480, 534, .9)])

# 02 long ago the sky was low
svg(2, "When the sky was low", "Paper-cut scene: long ago the sky was so low it was like a bumpy blue ceiling just over the village. A man in a white shirt and blue trousers holds his head with both hands because a puffy cloud has bumped into it, and a little boy in a teal top and blue shorts stands under another cloud, giggling. A coconut palm is bent sideways under the sky, and a bamboo house on stilts stands with its roof nearly touching it.", DAY, [
    hills(), ground(), LOW_PALM, hut(650),
    man(300, ((-18, -146), (18, -146)), "oof"),
    man(470, ((-30, -110), (30, -110)), "big", True, s=1.0, kid=True),
    low_sky(LOW),
    cloud(300, LOW + 28, .6, "oh"), cloud(480, LOW + 72, .5, "smile"),
    marks(["M258 300 l-14 -6", "M342 300 l14 -6"], INK, 3)])

# 03 the woman pounds rice
svg(3, "Pounding rice", "Paper-cut scene: under the low bumpy sky, a smiling woman in a coral blouse and purple striped skirt, with a half-round comb in her hair and a necklace of cream and gold beads, holds her long wooden pestle upright in a wooden mortar full of white rice. Her bamboo house on stilts is behind her on the right, a bent coconut palm is on the left, and a white hen pecks nearby.", DAY, [
    hills(), ground(), LOW_PALM, hut(640),
    woman(WX, on_pestle(TIP_DOWN), "smile", tool="up", tip=TIP_DOWN),
    low_sky(LOW), cloud(560, LOW + 26, .5), chicken(200, 536, .9, True),
    '<g fill="#fff">' + "".join(f'<ellipse cx="{PX + dx}" cy="{438 + dy}" rx="3" ry="2"/>' for dx, dy in [(-30, -10), (26, -16), (-18, -26), (32, -4)]) + '</g>'])

# 04 she hangs her comb and necklace on the sky
svg(4, "Hanging them on the sky", "Paper-cut scene: the woman stretches one arm up and hooks her half-round comb onto a bump of the low blue sky, right above her head. Her bead necklace already hangs from the sky to her left in a U shape. Her long pestle leans against the rice mortar beside her. The bamboo house on stilts is on the right and a bent palm on the left.", DAY, [
    hills(), ground(), LOW_PALM, hut(640),
    woman(WX, ((-30, -84), (10, to_local(LOW + 20))), "smile", True, comb=False, beads=False, tool="lean"),
    low_sky(LOW), hung(LOW), cloud(560, LOW + 26, .5)])

# 05 Thump! BONK!
svg(5, "Thump! BONK!", "Paper-cut scene: the woman lifts her long pestle to pound the rice, but straight away the top of it bonks the low sky — a yellow burst flashes where it hits. Her eyes look up and her mouth is a little 'oh'. Her comb and bead necklace still hang on the sky above her, and a little cloud to the right says 'oof'.", DAY, [
    hills(), ground(), LOW_PALM, hut(640),
    woman(WX, on_pestle(TIP_LOW), "oh", True, comb=False, beads=False, tool="up", tip=TIP_LOW),
    low_sky(LOW), hung(LOW), bonk(PX, LOW + 4, 1),
    cloud(530, LOW + 30, .55, "oof")])

# 06 she asks the sky politely to go up
svg(6, "Please go up a little", "Paper-cut scene: the woman looks up at the low sky with one hand cupped beside her mouth, calling to it politely; her other hand rests on her hip, and her pestle leans on the mortar. The sky has creaked up just a teeny bit — little lines show it moving — with her comb and necklace still hanging from it. A small cloud peeks down, listening.", DAY, [
    hills(), ground(), LOW_PALM2, hut(640),
    woman(WX, ((-28, -80), (16, -120)), "big", True, comb=False, beads=False, tool="lean"),
    low_sky(LOW2), hung(LOW2), cloud(560, LOW2 + 30, .55, "smile"),
    marks(["M470 300 v-26", "M490 304 v-18", "M220 300 v-26", "M200 304 v-18"], "#fff", 4)])

# 07 BONK again
svg(7, "BONK again", "Paper-cut scene: the woman pounds again, and — BONK! — the top of her pestle hits the sky once more with a yellow burst. A little cloud has bumped down onto her head too, and she squeezes her eyes shut with a funny wobbly 'oof' face. Her comb and bead necklace hang on the sky above her.", DAY, [
    hills(), ground(), LOW_PALM2, hut(640),
    woman(WX, on_pestle(TIP_LOW2), "oof", comb=False, beads=False, tool="up", tip=TIP_LOW2),
    low_sky(LOW2), hung(LOW2), bonk(PX, LOW2 + 4, 1),
    cloud(WX - 6, 282, .42, "oh")])

# 08 she asks again; the clouds are asleep and the sky doesn't move
svg(8, "Higher, please!", "Paper-cut scene: the woman stands with both hands on her hips and calls up to the sky again, more loudly. Her pestle leans on the mortar. Two little clouds under the sky have closed their eyes, fast asleep, and the sky does not move at all. Her comb and bead necklace hang on the sky.", DAY, [
    hills(), ground(), LOW_PALM2, hut(640),
    woman(WX, ((-28, -78), (28, -78)), "big", True, comb=False, beads=False, tool="lean"),
    low_sky(LOW2), hung(LOW2),
    cloud(540, LOW2 + 30, .55, "sleep"), cloud(160, LOW2 + 28, .5, "sleep"),
    marks(["M580 266 h10 l-10 10 h10", "M600 248 h8 l-8 8 h8"], "#56688C", 2.6)])

# 09 the big push
TIP_PUSH = to_local(LOW2, P, FEET - 6 * P)
svg(9, "One, two, three — PUSH!", "Paper-cut scene: the woman stands up on her tiptoes, holds her long pestle with both hands high above her head, and gives the low sky a great big push, with a big yellow burst where the pestle presses it. White lines show the sky starting to move up. Her comb and necklace still hang on the sky. The two little clouds have woken up with surprised faces.", DAY, [
    hills(), ground(), LOW_PALM2, hut(640),
    woman(WX, ((36, TIP_PUSH + 90), (42, TIP_PUSH + 18)), "big", True, comb=False, beads=False, tool="up", tip=TIP_PUSH, toes=True),
    low_sky(LOW2), hung(LOW2), bonk(PX, LOW2 + 2, 1.25),
    cloud(560, LOW2 + 30, .55, "oh"), cloud(160, LOW2 + 28, .5, "oh"),
    marks(["M470 228 v-30", "M510 232 v-24", "M140 228 v-30", "M100 232 v-24"], "#fff", 5)])

# 10 WHOOSH — the sky flies up, carrying the comb and necklace
svg(10, "Whoosh!", "Paper-cut scene: whoosh! The bumpy blue sky flies up and up, high over the village, with white lines rushing upward. Just under it, very small, float the woman's comb and her bead necklace, carried away with the sky. Two clouds rise too, smiling. Down below, the woman holds her pestle up and looks up with her mouth open in surprise, the palm tree springs up straight, and the bamboo house stands tall.", HIGH, [
    hills(), ground(), TALL_PALM, hut(640),
    woman(WX, on_pestle(TIP_DOWN - 18), "oh", True, comb=False, beads=False, tool="up", tip=TIP_DOWN - 18),
    low_sky(64), comb_shape(380, 88, .55), necklace_loop(320, 74, .6),
    cloud(190, 170, .7, "big"), cloud(600, 150, .75, "big"),
    marks(["M280 260 v-60", "M470 250 v-70", "M540 280 v-50", "M60 260 v-60", "M740 250 v-60", "M380 210 v-40"], "#fff", 5)])

# 11 everyone stands tall; pound with no bonk
svg(11, "Room to stand tall", "Paper-cut scene: now the sky is high and wide and blue, with clouds far up. The woman pounds her rice with her long pestle held high, smiling; the man in the white shirt stretches both arms up to the sky, and the little boy in the teal top jumps for joy. The coconut palm stands straight and tall, and the bamboo house is on the right.", HIGH, [
    cloud(200, 90, .8), cloud(560, 70, .7), cloud(730, 160, .5),
    hills(), ground(), TALL_PALM, hut(680),
    woman(WX - 40, on_pestle(TIP_DOWN - 26), "big", True, comb=False, beads=False, tool="up", tip=TIP_DOWN - 26),
    man(440, ((-38, -164), (38, -164)), "big", True),
    man(540, ((-30, -150), (30, -150)), "big", True, s=1.0, feet=FEET - 26, kid=True),
    marks(["M522 516 l-8 10", "M558 516 l8 10"], INK, 3)])

# 12 but where are her comb and beads?
svg(12, "Where did they go?", "Paper-cut scene: in the golden evening the woman stands with a hand on her cheek, looking up at the high empty sky, wondering where her comb and necklace have gone. The sky is purple, pink and orange with a few soft clouds, and there is no comb or necklace anywhere. Her pestle leans on the mortar, and the bamboo house and the palm tree stand beside her.", DUSK, [
    cloud(200, 120, .7, "", .7), cloud(600, 90, .6, "", .7),
    hills(), ground(), TALL_PALM, hut(640),
    woman(WX, ((-26, -82), (16, -118)), "oh", True, comb=False, beads=False, tool="lean")])

# 13 night: the comb is the moon, the beads are the stars
STARS = [(70, 70), (150, 140), (240, 60), (320, 160), (420, 50), (400, 250), (700, 60), (740, 150), (120, 250),
         (260, 230), (720, 260), (40, 180), (60, 330), (470, 150)]
starry = "".join(f'<circle cx="{a}" cy="{b}" r="{12 if i % 3 else 16}" fill="#FFF4C8" opacity=".18"/>'
                 f'<circle cx="{a}" cy="{b}" r="{5 if i % 3 else 7}" fill="{BEAD if i % 2 else BEAD2}"/>' for i, (a, b) in enumerate(STARS))
moon = ('<circle cx="580" cy="150" r="130" fill="url(#glow)"/>'
        '<g transform="translate(580 180)">'
        + "".join(f'<rect x="{-66 + 12 * i}" y="-1" width="5" height="10" rx="2" fill="#FBE7A6" opacity=".6"/>' for i in range(12))
        + '<path d="M-74 0 A74 58 0 0 1 74 0Z" fill="#FBE7A6"/>'
        '<path d="M-50 -10 A50 32 0 0 1 50 -10" stroke="#EBCB78" stroke-width="5" fill="none"/>'
        '<circle cx="-14" cy="-28" r="3.4" fill="#5A4A2A"/><circle cx="14" cy="-28" r="3.4" fill="#5A4A2A"/>'
        + stroke("M-9 -18 Q0 -11 9 -18", "#5A4A2A", 2.6) + '</g>')
svg(13, "The moon and the stars", "Paper-cut night scene: high up in the deep blue night sky shines a glowing half-moon shaped just like the woman's comb, with a gentle smiling face and faint comb teeth along its flat edge. All around it, cream and gold stars twinkle, just like the beads of her necklace. Down below, beside her bamboo house with a warm yellow window and a dark palm tree, the woman smiles and points up at the moon.", NIGHT, [
    starry, moon, hills(True), ground(True), palm(110, 500, 120, 230, 1, True), hut(640, night=True),
    woman(WX, ((-26, -82), (34, -176)), "big", True, comb=False, beads=False, tool="lean")])
