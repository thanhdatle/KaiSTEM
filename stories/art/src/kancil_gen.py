#!/usr/bin/env python3
"""Generates the 13 Mouse-deer-and-the-Crocodiles flip-book SVGs from shared character parts.

Usage: python3 kancil_gen.py <output-dir>
Scale rule: every page draws Kancil at KAN_SIZE * k and every crocodile at k, with ONE k per page,
so the mouse-deer is always much smaller than a crocodile (Kancil ~ 85 units long, a crocodile 200).
River pages (side view) use k = .39: water surface y = 396, left bank ends x = 60, right bank starts x = 724,
and the crossing line is exactly 8 crocodiles, centred at LINE_X.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
KAN, KAN_D, KAN_L = "#B8743E", "#80492A", "#F4E3C8"
CROC, CROC_D, CROC_L, SCUTE = "#5C8A3E", "#33552A", "#B5CF86", "#33552A"
WATER_C, WATER_L, WATER_D = "#4CA6A8", "#9FD9D2", "#2F7F86"
EARTH, EARTH_D, GRASS, GRASS_D, GRASS_L = "#B98A55", "#8E6538", "#5DB85C", "#3F9A56", "#86D16E"
JUNGLE, JUNGLE_D, JUNGLE_F = "#4F9A5E", "#357A4A", "#7BBF7A"
TRUNK, TRUNK_D, FRUIT, FRUIT_D = "#8A5A36", "#6A4026", "#E0392F", "#A82620"
DAY = [(0, "#7CCBE8"), (1, "#E9F6FB")]
GOLDEN = [(0, "#8FCFEA"), (.6, "#FDE7C0"), (1, "#FCD9A0")]
KAN_SIZE = .85
K_RIVER = .39
WATER, BANK_Y, BANK_L, BANK_R = 396, 380, 60, 724
PITCH = (BANK_R - BANK_L) / 8
LINE_X = [BANK_L + PITCH * (i + .5) for i in range(8)]
BACK_TOP = 58  # croc back height above the waterline, in croc units


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, shadow: bool = True, rot: float = 0) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x:.1f} {y:.1f}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- Kancil the mouse-deer
KAN_LEGS = {
    "stand": "M-26 -36 L-28 0 M-16 -36 L-14 0 M22 -36 L20 0 M30 -36 L32 0",
    "hop": "M-26 -38 L-46 -14 M-16 -38 L-38 -8 M22 -38 L42 -18 M30 -38 L50 -24",
}


def kancil(x: float, y: float, k: float = 1, flip: bool = False, pose: str = "stand", mood: str = "smile") -> str:
    """Kancil in side view facing right. (x, y) = hooves. Tiny, thin legs, NO antlers, white throat stripes."""
    out = stroke(KAN_LEGS[pose], KAN_D, 5)
    if pose == "stand":
        out += "".join(f'<rect x="{a - 3}" y="-4" width="6" height="5" rx="1.5" fill="{INK}"/>' for a in (-28, -14, 20, 32))
    out += f'<path d="M-46 -64 q-8 -6 -4 -12 q6 2 8 10Z" fill="{KAN_D}"/><path d="M-47 -66 q-4 -2 -2 -6 q3 1 4 5Z" fill="#fff"/>'
    out += (f'<path d="M-44 -52 Q-46 -78 -16 -80 Q14 -80 30 -66 Q40 -50 28 -36 Q0 -30 -30 -34 Q-46 -38 -44 -52Z" fill="{KAN}"/>'
            f'<ellipse cx="-6" cy="-38" rx="28" ry="5.5" fill="{KAN_L}" opacity=".75"/>')
    out += stroke("M16 -64 Q28 -76 42 -86", KAN, 18)
    out += stroke("M26 -66 L36 -75 M23 -59 L32 -67", "#fff", 2.2)  # the mouse-deer's white throat stripes
    out += f'<ellipse cx="34" cy="-104" rx="6" ry="11" fill="{KAN_D}" transform="rotate(-24 34 -104)"/>'
    out += f'<ellipse cx="34" cy="-103" rx="3" ry="6.5" fill="#E7A68F" transform="rotate(-24 34 -103)"/>'
    out += f'<ellipse cx="46" cy="-90" rx="15" ry="12" fill="{KAN}"/>'
    out += f'<path d="M50 -98 L74 -88 Q78 -82 70 -79 L50 -82Z" fill="{KAN}"/><path d="M56 -82 L71 -80 Q66 -76 56 -78Z" fill="{KAN_L}"/>'
    out += f'<circle cx="73" cy="-86" r="2.6" fill="{INK}"/>'
    if mood == "happy":
        out += stroke("M45 -94 q4 -4 8 0", INK, 2.2)
    else:
        lx = 2 if mood != "think" else 1
        ly = -1.5 if mood == "think" else 0
        out += f'<circle cx="50" cy="-93" r="4.6" fill="#fff"/><circle cx="{50 + lx}" cy="{-93 + ly}" r="2.9" fill="{INK}"/>'
        out += f'<circle cx="{51 + lx}" cy="{-94 + ly}" r="1" fill="#fff"/>'
    out += f'<circle cx="54" cy="-84" r="3.5" fill="#F0705F" opacity=".45"/>'
    if mood == "talk":
        out += f'<ellipse cx="64" cy="-79" rx="3.6" ry="2.6" fill="#5A2E22"/>'
    elif mood == "eat":
        out += rambutan_shape(72, -78, 7)
    else:
        out += stroke("M60 -80 q4 2 8 -1", INK, 1.8)
    return group(x, y, KAN_SIZE * k, flip, out)


# ---------------------------------------------------------------- crocodiles
CROC_BODY = "M-100 0 Q-80 -10 -64 -22 Q-46 -56 -6 -58 Q26 -58 36 -40 L92 -30 Q106 -24 104 0Z"
SCUTES = [(-86, -12), (-74, -18), (-62, -26), (-50, -40), (-38, -50), (-24, -56), (-10, -58), (4, -58), (18, -54)]


def croc_parts(mood: str) -> str:
    """A floating crocodile, side view facing right, waterline at y = 0: long toothy snout, eye bumps, back ridges."""
    out = f'<ellipse cx="-10" cy="12" rx="78" ry="16" fill="{WATER_D}" opacity=".35"/>'
    out += "".join(f'<path d="M{a - 7} {b + 3} L{a} {b - 11} L{a + 7} {b + 3}Z" fill="{SCUTE}"/>' for a, b in SCUTES)
    out += f'<path d="{CROC_BODY}" fill="{CROC}" stroke="{CROC_D}" stroke-width="3" stroke-linejoin="round"/>'
    out += f'<path d="M-64 -8 Q-10 -26 38 -18 L100 -12 L102 0 H-76Z" fill="{CROC_L}" opacity=".6"/>'
    out += stroke("M-42 -42 l6 14 M-24 -48 l4 16 M-6 -50 l2 16 M12 -47 l0 15", CROC_D, 3)
    out += f'<circle cx="96" cy="-30" r="7.5" fill="{CROC}" stroke="{CROC_D}" stroke-width="3"/><circle cx="98" cy="-32" r="2.2" fill="{INK}"/>'
    out += f'<circle cx="48" cy="-44" r="15" fill="{CROC}" stroke="{CROC_D}" stroke-width="3"/>'
    # mouth with a gentle crocodile grin and little white teeth along the side
    out += "".join(f'<path d="M{a} -14 l4 8 l4 -8Z" fill="#fff"/>' for a in (54, 66, 78, 90))
    out += stroke("M40 -24 q2 10 12 10 L102 -14", INK, 3)
    if mood == "grump":
        out += f'<circle cx="49" cy="-46" r="8.5" fill="#F4E27A"/><circle cx="50" cy="-43" r="3.8" fill="{INK}"/>'
        out += f'<path d="M39 -48 Q49 -58 59 -48 L59 -45 L39 -45Z" fill="{CROC_D}"/>'
    elif mood == "wow":
        out += f'<circle cx="49" cy="-47" r="10" fill="#F4E27A"/><circle cx="49" cy="-47" r="3.2" fill="{INK}"/>'
        out += stroke("M38 -64 q10 -7 20 0", INK, 3)
    else:  # smile / still
        out += f'<circle cx="49" cy="-46" r="8.5" fill="#F4E27A"/><ellipse cx="50.5" cy="-46" rx="2.4" ry="6" fill="{INK}"/>'
    return out


def croc(x: float, y: float, k: float = 1, flip: bool = False, mood: str = "smile", peek: bool = False, rot: float = 0) -> str:
    """(x, y) = middle of the crocodile at the waterline. peek: sunk so only eyes, nose and back ridges show."""
    inner = croc_parts(mood)
    if peek:
        inner = f'<g clip-path="url(#wl)"><g transform="translate(0 26)">{inner}</g></g>'
    ripple = stroke("M-108 2 q8 -4 16 0 M96 2 q8 -4 16 0", "#fff", 2.4)
    return group(x, y, k, flip, inner + f'<g opacity=".8">{ripple}</g>', rot=rot)


def croc_back(x: float, k: float) -> float:
    """y of the top of a lined-up crocodile's back (where Kancil's hooves land)."""
    return WATER - BACK_TOP * k


# ---------------------------------------------------------------- scenery
def rambutan_shape(x: float, y: float, r: float) -> str:
    """A rambutan: red ball covered in soft spiky hairs with green tips (so it can't be mistaken for a tomato)."""
    dirs = [(c / 100, sn / 100) for c, sn in [(100, 0), (87, 50), (50, 87), (0, 100), (-50, 87), (-87, 50),
                                               (-100, 0), (-87, -50), (-50, -87), (0, -100), (50, -87), (87, -50)]]
    hairs = " ".join(f"M{x + r * .6 * c:.1f} {y + r * .6 * sn:.1f} L{x + r * 1.3 * c:.1f} {y + r * 1.3 * sn:.1f}" for c, sn in dirs)
    tips = " ".join(f"M{x + r * 1.15 * c:.1f} {y + r * 1.15 * sn:.1f} L{x + r * 1.42 * c:.1f} {y + r * 1.42 * sn:.1f}" for c, sn in dirs)
    inner = " ".join(f"M{x + r * .3 * c:.1f} {y + r * .3 * sn:.1f} l{r * .25 * c:.1f} {r * .25 * sn:.1f}" for c, sn in dirs[1::3])
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FRUIT}"/>' + stroke(hairs, FRUIT, r * .2) + stroke(tips, "#8BC34A", r * .17)
            + stroke(inner, FRUIT_D, r * .12)
            + f'<circle cx="{x - r * .35}" cy="{y - r * .35}" r="{r * .25}" fill="#fff" opacity=".4"/>')


def rambutan_tree(x: float, y: float, s: float = 1, fruit: bool = True, lean: float = 0) -> str:
    """Trunk base at (x, y). Canopy spans about x-150..x+60 at s=1, shifted by `lean` units (negative = leans left)."""
    out = f'<path d="M-16 0 Q-10 -90 {-20 + lean} -170 L{14 + lean} -170 Q8 -90 18 0Z" fill="{TRUNK}"/>'
    inner = stroke("M-6 -120 Q-50 -150 -96 -150", TRUNK, 12) + stroke("M2 -150 Q20 -190 30 -200", TRUNK, 10)
    blobs = [(-110, -175, 46), (-60, -205, 56), (0, -215, 52), (-130, -215, 40), (20, -175, 40), (-20, -170, 44)]
    inner += "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{JUNGLE_D}"/>' for a, b, r in blobs)
    inner += "".join(f'<circle cx="{a - 8}" cy="{b - 10}" r="{r * .6}" fill="{JUNGLE}"/>' for a, b, r in blobs)
    if fruit:
        inner += "".join(rambutan_shape(a, b, 8) for a, b in
                         [(-118, -158), (-104, -164), (-112, -146), (-50, -180), (-38, -186), (-44, -170), (10, -196),
                          (22, -188), (16, -178), (-80, -222), (-68, -230), (-20, -238), (-140, -200), (34, -160)])
    out += f'<g transform="translate({lean} 0)">{inner}</g>'
    return group(x, y, s, False, out)


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def palm(x: float, y: float, s: float = 1, col: str = JUNGLE_D) -> str:
    fronds = "".join(f'<path d="M0 -150 Q{a * .5} {-170 + b * .3} {a} {b}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                     for a, b in [(-70, -120), (-60, -175), (0, -195), (60, -178), (74, -124)])
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-6 0 Q-2 -80 0 -150 L6 -150 Q6 -80 8 0Z" fill="{col}"/>{fronds}</g>'


def fern(x: float, y: float, s: float = 1, col: str = GRASS_D, flip: bool = False) -> str:
    leaf = "".join(f'<path d="M0 0 Q{a * .4} {b * .6} {a} {b} Q{a * .7} {b * .5} 0 0Z" fill="{col}"/>'
                   for a, b in [(-60, -40), (-40, -80), (0, -100), (40, -82), (62, -44)])
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})" filter="url(#p)">{leaf}</g>'


def tufts(pts: list, col: str, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def water(level: float = WATER, amp: float = 5) -> str:
    def wave(y: float) -> str:
        segs = "".join(f" T{x} {y}" for x in range(100, 801, 100))
        return f"M0 {y} Q50 {y - amp} 100 {y}{segs} V600 H0Z"
    ripples = " ".join(f"M{a} {b} h{w}" for a, b, w in [(120, 470, 30), (300, 520, 26), (470, 480, 36), (620, 540, 28), (200, 575, 30), (560, 585, 34), (700, 470, 24)])
    return (f'<path d="{wave(level)}" fill="{WATER_C}"/><path d="{wave(level + 40)}" fill="{WATER_D}" opacity=".25"/>'
            + stroke(f"M0 {level - 1} Q50 {level - amp - 1} 100 {level - 1}" + "".join(f" T{x} {level - 1}" for x in range(200, 801, 100)), WATER_L, 3.5)
            + f'<g opacity=".6">{stroke(ripples, "#fff", 3.5)}</g>')


JUNGLE_BACK = [cloud(160, 70, .9), cloud(520, 50, .8),
               f'<path d="M0 260 Q120 200 260 240 Q400 180 540 236 Q680 196 800 230 V400 H0Z" fill="{JUNGLE_F}"/>',
               palm(150, 330, .9, JUNGLE), palm(330, 320, 1.05, JUNGLE), palm(470, 330, .85, JUNGLE),
               f'<path d="M0 320 Q200 280 400 310 Q600 280 800 316 V400 H0Z" fill="{JUNGLE}"/>',
               f'<path d="M0 352 Q400 340 800 352 V400 H0Z" fill="#EBDCA8"/>']
LEFT_BANK = (f'<path filter="url(#p)" d="M0 {BANK_Y} H{BANK_L - 6} Q{BANK_L + 4} {BANK_Y + 6} {BANK_L + 2} {WATER + 20} L{BANK_L - 10} 600 H0Z" fill="{EARTH}"/>'
             f'<path d="M0 {BANK_Y - 4} H{BANK_L - 4} Q{BANK_L + 2} {BANK_Y} {BANK_L} {BANK_Y + 6} H0Z" fill="{GRASS}"/>'
             + tufts([(12, BANK_Y + 2)], GRASS_D, 2.4))
RIGHT_BANK = (f'<path filter="url(#p)" d="M800 {BANK_Y} H{BANK_R + 6} Q{BANK_R - 4} {BANK_Y + 6} {BANK_R - 2} {WATER + 20} L{BANK_R + 10} 600 H800Z" fill="{EARTH}"/>'
              f'<path d="M800 {BANK_Y - 4} H{BANK_R + 4} Q{BANK_R - 2} {BANK_Y} {BANK_R} {BANK_Y + 6} H800Z" fill="{GRASS}"/>')
TREE = rambutan_tree(790, BANK_Y, .82, lean=-70)  # canopy leans over the river, clear of the frame edge


def river_scene(*, under: list = (), mid: list = (), front: list = ()) -> list:
    """Side view of the river in draw order: jungle, tree and banks, water, crocodiles, things in front."""
    return [*JUNGLE_BACK, TREE, *under, water(), LEFT_BANK, RIGHT_BANK, *mid, *front]


def number_disc(x: float, n: int) -> str:
    """A cream counting disc in the water under the crocodile Kancil has just counted."""
    y = WATER + 44
    return (f'<g filter="url(#p)"><circle cx="{x:.1f}" cy="{y}" r="15" fill="{CREAM}"/>'
            f'<text x="{x:.1f}" y="{y + 7}" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif" '
            f'font-weight="700" font-size="21" fill="{INK}">{n}</text></g>')


def hop_arcs(n: int, end_x: float = None) -> str:
    """Dashed hop arcs from the left bank over the first n crocodiles (and onward to end_x, if given)."""
    pts = [BANK_L - 30] + LINE_X[:n] + ([end_x] if end_x is not None else [])
    d = " ".join(f"M{a:.0f} {BANK_Y - 8 if i == 0 else croc_back(a, K_RIVER) - 4:.0f} Q{(a + b) / 2:.0f} {BANK_Y - 74} {b:.0f} {croc_back(b, K_RIVER) - 4 if b < BANK_R else BANK_Y - 4:.0f}"
                 for i, (a, b) in enumerate(zip(pts, pts[1:])))
    return f'<path d="{d}" stroke="#fff" stroke-width="3" stroke-dasharray="2 8" fill="none" stroke-linecap="round" opacity=".95"/>'


def line_crocs(mood: str = "smile", first: int = 0, last: int = 8) -> list:
    return [croc(LINE_X[i], WATER, K_RIVER, mood=mood) for i in range(first, last)]


def kancil_on(i: int, pose: str = "stand", mood: str = "smile") -> str:
    x = LINE_X[i]
    return kancil(x - 4, croc_back(x, K_RIVER), K_RIVER, pose=pose, mood=mood)


DEFS = {
    "wl": '<clipPath id="wl"><rect x="-200" y="-200" width="400" height="200"/></clipPath>',
}


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    defs = "".join(d for k, d in DEFS.items() if f'url(#{k})' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/kancil-{n:02d}.svg", "w") as fh:
        fh.write(doc)


K = K_RIVER
ON_LEFT = kancil(40, BANK_Y, K)
ON_RIGHT_X = 742  # Kancil on the far bank, clear of the trunk at x 790

# 01 cover
svg(1, "Mouse-deer and the Crocodiles", "Paper-cut cover: tiny Kancil the mouse-deer, reddish-brown with thin legs and no antlers, stands on the left bank of a wide jungle river. Across the water a rambutan tree is full of red, hairy fruit. In the river, three crocodiles peek up, so that only their bumpy eyes, noses and ridged backs show.", DAY, river_scene(
    mid=[croc(250, WATER + 30, K, peek=True), croc(430, WATER + 80, K, flip=True, peek=True), croc(600, WATER + 40, K, peek=True), ON_LEFT]))

# 02 Kancil, close up, in the jungle
K2 = 2.2
svg(2, "Kancil the mouse-deer", "Paper-cut scene: in the green jungle, Kancil the mouse-deer stands among ferns that tower over him. He is small and reddish-brown, with a round body, legs as thin as sticks, round ears, white stripes on his throat, a big shiny eye and no antlers. A yellow butterfly flutters near his nose.", DAY, [
    cloud(640, 80, 1),
    f'<path d="M0 230 Q200 170 400 210 Q600 170 800 220 V600 H0Z" fill="{JUNGLE_F}"/>',
    palm(110, 420, 1.4, JUNGLE), palm(690, 420, 1.3, JUNGLE),
    f'<path d="M0 380 Q200 340 400 370 Q600 340 800 376 V600 H0Z" fill="{JUNGLE}"/>',
    f'<path filter="url(#p)" d="M0 470 Q400 430 800 470 V600 H0Z" fill="{GRASS}"/>',
    fern(120, 500, 2.1, GRASS_D), fern(690, 500, 2.3, GRASS_D, True), fern(560, 520, 1.3, JUNGLE_D),
    tufts([(60, 540), (240, 560), (520, 570), (720, 560), (380, 585)], GRASS_D),
    kancil(360, 540, K2),
    f'<g transform="translate(560 300)" filter="url(#p)"><path d="M0 0 q-22 -24 -26 -4 q4 16 26 4Z M0 0 q22 -24 26 -4 q-4 16 -26 4Z" fill="#F7D046"/>'
    f'<path d="M0 -8 v14" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>'])

# 03 the rambutans across the wide river
svg(3, "Rambutans across the river", "Paper-cut scene: tiny Kancil stands at the edge of the left bank and looks across a wide, empty jungle river. On the far bank a rambutan tree is heavy with red, hairy fruit.", DAY, river_scene(
    mid=[kancil(40, BANK_Y, K, mood="think")]))

# 04 crocodiles!
svg(4, "Crocodiles!", "Paper-cut scene: five crocodiles have popped up in the river: four peek out with only their bumpy eyes, noses and ridged backs showing, and one big one floats near the left bank, grinning, with its long toothy snout pointed at tiny Kancil, who has hopped back from the edge.", DAY, river_scene(
    mid=[croc(190, WATER + 18, K, flip=True, mood="smile"),
         croc(330, WATER + 70, K, flip=True, peek=True), croc(460, WATER + 30, K, flip=True, peek=True),
         croc(560, WATER + 110, K, flip=True, peek=True), croc(650, WATER + 56, K, flip=True, peek=True),
         kancil(34, BANK_Y, K, pose="hop", mood="wow")]))

# 05 Kancil speaks to the biggest crocodile, close up
K5 = 1.25
svg(5, "The King has sent me", "Paper-cut scene, close up: tiny Kancil stands tall at the edge of the riverbank and speaks to a big crocodile floating in the water below him. The crocodile, more than twice as long as Kancil, looks up at him with a friendly grin, its long snout and little white teeth pointing toward the bank.", DAY, [
    cloud(560, 80, 1),
    f'<path d="M0 220 Q200 170 400 200 Q600 170 800 210 V420 H0Z" fill="{JUNGLE_F}"/>',
    palm(520, 360, 1.2, JUNGLE), palm(700, 350, 1.0, JUNGLE),
    f'<path d="M0 330 Q400 300 800 330 V440 H0Z" fill="{JUNGLE}"/>',
    water(440, 7),
    f'<path filter="url(#p)" d="M0 400 H290 Q312 410 306 460 L290 600 H0Z" fill="{EARTH}"/>',
    f'<path d="M0 394 H292 Q306 400 302 410 H0Z" fill="{GRASS}"/>',
    fern(40, 402, 1.0, GRASS_D), tufts([(120, 440), (220, 470), (60, 520)], EARTH_D, 2.6),
    croc(530, 450, K5, flip=True, mood="smile"),
    kancil(190, 400, K5, mood="talk")])

# 06 the crocodiles swim into a line
svg(6, "Line up, nose to tail!", "Paper-cut scene: five crocodiles already float in a line from the left bank, nose to tail, while three more swim in through the water to fill the gap to the far bank. That makes eight crocodiles. Tiny Kancil watches from the left bank.", DAY, river_scene(
    mid=[*line_crocs(last=5), croc(560, WATER + 80, K, flip=True, peek=True), croc(680, WATER + 130, K, flip=True, peek=True),
         croc(470, WATER + 150, K, flip=True, peek=True), ON_LEFT],
    front=[stroke("M622 468 q12 -6 24 0 M742 518 q12 -6 24 0 M532 538 q12 -6 24 0", "#fff", 3)]))

# 07 the crocodile bridge is complete
svg(7, "A crocodile bridge", "Paper-cut scene: eight crocodiles float in a long, straight line all the way across the river, nose to tail, from the left bank to the far bank, holding very still. Tiny Kancil stands on the left bank, ready to start counting.", DAY, river_scene(
    mid=[*line_crocs(), kancil(40, BANK_Y, K, mood="talk")]))

# 08 one, two, three
svg(8, "One! Two! Three!", "Paper-cut scene: tiny Kancil has hopped onto the backs of the first three crocodiles in the line of eight and stands on the third one. Dotted hop-marks curve from the bank over crocodiles one, two and three, and cream number discs 1, 2 and 3 float in the water under them.", DAY, river_scene(
    mid=[*line_crocs(), kancil_on(2, mood="talk"), hop_arcs(3), *[number_disc(LINE_X[i], i + 1) for i in range(3)]]))

# 09 four, five, six
svg(9, "Four! Five! Six!", "Paper-cut scene: tiny Kancil hops on across the line of eight crocodiles and stands on the sixth one. Dotted hop-marks curve over crocodiles one to six, and cream number discs 1 to 6 float in the water under them. Two crocodiles are still left to count.", DAY, river_scene(
    mid=[*line_crocs(), kancil_on(5, mood="talk"), hop_arcs(6), *[number_disc(LINE_X[i], i + 1) for i in range(6)]]))

# 10 seven, eight, and HOP onto the far bank
svg(10, "Seven! Eight! HOP!", "Paper-cut scene: tiny Kancil has hopped over the seventh and eighth crocodiles and landed on the far bank under the rambutan tree. Dotted hop-marks curve over all eight crocodiles to the bank, and cream number discs 1 to 8 float in the water under them.", DAY, river_scene(
    mid=[*line_crocs(), kancil(ON_RIGHT_X, BANK_Y, K, pose="hop", mood="happy"), hop_arcs(8, ON_RIGHT_X),
         *[number_disc(LINE_X[i], i + 1) for i in range(8)]]))

# 11 "I just wanted to cross!"
svg(11, "I just wanted to cross!", "Paper-cut scene: tiny Kancil stands on the far bank under the rambutan tree, turned back toward the river, calling out. The eight crocodiles are still in their line, and every one has its eyes wide open in surprise.", DAY, river_scene(
    mid=[*line_crocs("wow"), kancil(ON_RIGHT_X + 6, BANK_Y, K, flip=True, mood="talk")],
    front=[stroke("M700 330 q-10 -6 -6 -16 M692 344 q-14 -2 -16 -12", "#fff", 3)]))

# 12 the crocodiles grumble and swim off
grumble = "".join(
    f'<g transform="translate({a} {b})" filter="url(#p)"><ellipse rx="30" ry="17" fill="#fff"/>'
    + stroke("M-18 1 q4 -8 8 0 q4 8 8 0 q4 -8 8 0 q4 8 8 0", "#5A3B22", 2.6) + '</g>'
    for a, b in [(200, 344), (430, 352), (600, 338)])
splashes = stroke("M186 404 l-8 -16 M194 402 l0 -18 M202 404 l8 -16 M504 508 l-8 -16 M512 506 l0 -18 M520 508 l8 -16", "#fff", 3.4)
svg(12, "Grumble, grumble!", "Paper-cut scene: the eight crocodiles have broken up their line and swim off in every direction, grumbling, with sleepy cross eyes, little grumble-clouds above them and splashes from their tails. Nobody is hurt. Tiny Kancil stands safe on the far bank under the rambutan tree.", DAY, river_scene(
    mid=[croc(150, WATER + 16, K, flip=True, mood="grump"), croc(270, WATER + 70, K, mood="grump"),
         croc(380, WATER + 20, K, flip=True, mood="grump"), croc(470, WATER + 120, K, flip=True, mood="grump"),
         croc(560, WATER + 60, K, mood="grump"), croc(640, WATER + 18, K, flip=True, mood="grump"),
         croc(250, WATER + 160, K, flip=True, mood="grump"), croc(640, WATER + 160, K, mood="grump"),
         kancil(ON_RIGHT_X + 6, BANK_Y, K, flip=True, mood="smile")],
    front=[grumble, splashes]))

# 13 Kancil eats rambutans, close up, in golden light
K13 = 2.0
pile = "".join(rambutan_shape(a, b, 13) for a, b in [(560, 540), (590, 548), (575, 522), (620, 544)])
peel = (f'<path d="M470 552 q10 -16 22 -2 q-10 8 -22 2Z" fill="{FRUIT_D}"/><ellipse cx="510" cy="556" rx="7" ry="5" fill="#F5F0E0"/>')
svg(13, "Rambutans for Kancil", "Paper-cut scene in warm golden light: under the rambutan tree on the far bank, tiny Kancil happily munches a red, hairy rambutan, with a small pile of rambutans beside him and a bit of peel on the grass. His tummy is round and full.", GOLDEN, [
    cloud(160, 80, 1, .8),
    f'<path d="M0 260 Q200 210 400 240 Q600 210 800 250 V600 H0Z" fill="{JUNGLE_F}"/>',
    palm(120, 420, 1.2, JUNGLE),
    rambutan_tree(560, 470, 1.6),
    f'<path filter="url(#p)" d="M0 450 Q400 420 800 450 V600 H0Z" fill="{GRASS}"/>',
    tufts([(60, 500), (240, 520), (700, 510), (120, 580), (680, 585)], GRASS_D),
    fern(60, 470, 1.3, GRASS_D),
    pile, peel,
    kancil(370, 560, K13, mood="eat")])
