#!/usr/bin/env python3
"""Generates the 13 Three-Billy-Goats-Gruff flip-book SVGs from shared character parts.

Usage: python3 goats_gen.py <output-dir>
Scale rule: each goat's size is SIZE[who] * k, and every page that shows the troll uses k = 1,
so little < middle < big < troll on every page. Close-up pages without the troll use one k for all three goats.
Bridge geometry is fixed: deck top y = 330 (x 226..574), posts at x 320 / 480, river surface y = 490.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
SIZE = {"little": .6, "middle": .85, "big": 1.2}
FUR = {"little": ("#FBF5EA", "#DCCDB6"), "middle": ("#D9AE74", "#B0864F"), "big": ("#8E7C6C", "#64554A")}
HORN, HORN_D, HOOF = "#E8D9B8", "#B7A27A", "#4A3B30"
TROLL, TROLL_D, TROLL_L, HAIR, NOSE, SHORTS = "#8DB062", "#6B8E45", "#B4CF85", "#E07A3A", "#D98E74", "#8A5A36"
WOOD, WOOD_D, WOOD_L = "#B07A48", "#7E5130", "#CF9D68"
RIVER, RIVER_L, RIVER_D = "#3E9BD6", "#8FD0F0", "#2F7DB8"
DRY, DRY_D, DRY_HILL = "#CDB878", "#A8925A", "#D8C690"
GRASS, GRASS_D, GRASS_L = "#5DB85C", "#3F9A56", "#86D16E"
MTN, MTN_D, SNOW = "#9DB4CF", "#7F98B8", "#F7FAFF"
DAY = [(0, "#7CCBE8"), (1, "#E9F6FB")]
GOLDEN = [(0, "#8FCFEA"), (.6, "#FDE7C0"), (1, "#FCD9A0")]
DECK, RIVER_Y = 330, 490


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- goats
def horns(who: str) -> str:
    if who == "little":  # two tiny nubs
        return f'<path d="M-6 -12 L-10 -24 L0 -14Z M2 -13 L0 -25 L8 -14Z" fill="{HORN}"/>'
    if who == "middle":  # short swept-back horns
        return (stroke("M-4 -10 Q-10 -30 -28 -30", HORN_D, 9) + stroke("M-4 -10 Q-10 -30 -28 -30", HORN, 6)
                + stroke("M4 -12 Q2 -32 -14 -36", HORN, 6))
    # big: thick curling ram-style horns
    curl = (f'<path d="M-2 -10 Q-6 -52 -40 -50 Q-66 -46 -62 -18 Q-58 0 -42 -4 Q-30 -8 -36 -20 Q-40 -30 -48 -24 '
            f'Q-46 -36 -36 -36 Q-18 -36 -14 -6Z" fill="{HORN}" stroke="{HORN_D}" stroke-width="3"/>')
    ridges = stroke("M-10 -30 l-8 4 M-20 -40 l-4 8 M-32 -44 l0 9 M-46 -42 l3 8 M-56 -32 l7 4", HORN_D, 2.6)
    return curl + ridges


def goat_head(who: str, mood: str, munch: bool) -> str:
    fur, dark = FUR[who]
    beard = {"little": "", "middle": "M8 14 L12 30 L18 16Z", "big": "M6 14 L8 42 L20 16Z"}[who]
    out = horns(who)
    out += f'<ellipse cx="-14" cy="-2" rx="15" ry="6.5" fill="{dark}" transform="rotate(28 -14 -2)"/>'
    out += f'<ellipse rx="19" ry="16" fill="{fur}"/><ellipse cx="17" cy="7" rx="15" ry="11" fill="{fur}"/>'
    if beard:
        out += f'<path d="{beard}" fill="{dark}"/>'
    out += f'<circle cx="29" cy="3" r="2.6" fill="{INK}"/><circle cx="-8" cy="9" r="4.5" fill="#F0705F" opacity=".45"/>'
    if mood == "sleep":
        out += stroke("M2 -5 q4 4 8 0", INK, 2.4)
    else:
        out += f'<circle cx="6" cy="-5" r="5" fill="#fff"/><circle cx="7.5" cy="-5" r="2.8" fill="{INK}"/>'
    if mood == "brave":
        out += stroke("M0 -13 L12 -10", INK, 3)
    out += stroke("M18 13 q6 4 12 -1", INK, 2.2)
    if munch:
        out += stroke("M30 12 l12 -6 M30 13 l14 2 M29 14 l9 9", GRASS_D, 3)
    return out


def goat(x: float, y: float, who: str, k: float = 1, flip: bool = False, pose: str = "stand",
         mood: str = "smile", fat: bool = False, munch: bool = False) -> str:
    """A billy goat in side view facing right. (x, y) is the hooves. pose: stand / walk / butt / graze."""
    s = SIZE[who] * k
    fur, dark = FUR[who]
    if pose == "walk":
        legs = "M-30 -40 L-40 -4 M-18 -40 L-14 -2 M20 -40 L16 -2 M32 -40 L44 -10"
        hooves = [(-41, -2), (-14, 0), (16, 0), (46, -8)]
    else:
        legs = "M-30 -40 L-32 -2 M-18 -40 L-16 -2 M20 -40 L18 -2 M32 -40 L34 -2"
        hooves = [(-32, 0), (-16, 0), (18, 0), (34, 0)]
    out = stroke(legs, dark, 9) + "".join(f'<rect x="{a - 5.5}" y="{b - 5}" width="11" height="7" rx="2" fill="{HOOF}"/>' for a, b in hooves)
    rx, ry = (58, 38) if fat else (50, 27)
    out += f'<path d="M-46 -70 Q-62 -86 -52 -96 Q-48 -84 -40 -76Z" fill="{dark}"/>'
    out += f'<ellipse cx="-2" cy="-58" rx="{rx}" ry="{ry}" fill="{fur}"/>'
    out += f'<path d="M-40 -46 Q-2 -{58 - ry + 52} 40 -46 Q0 -{58 - ry - 2} -40 -46Z" fill="{dark}" opacity=".35"/>'
    hx, hy, rot = {"butt": (58, -62, 48), "graze": (56, -30, 70)}.get(pose, (50, -100, 0))
    out += f'<path d="M20 -80 Q30 -60 44 -66 L{hx + 6} {hy + 6} L{hx - 12} {hy - 6} Q20 -100 14 -84Z" fill="{fur}"/>'
    out += f'<g transform="translate({hx} {hy}) rotate({rot})">{goat_head(who, mood, munch)}</g>'
    return group(x, y, s, flip, 0, out)


# ---------------------------------------------------------------- troll
TROLL_ARMS = {
    "cross": ("M-40 -104 Q-30 -70 22 -84", "M40 -104 Q30 -66 -22 -78", (22, -84), (-22, -78)),
    "up": ("M-40 -104 Q-70 -120 -76 -168", "M40 -104 Q70 -120 76 -168", (-76, -168), (76, -168)),
    "hips": ("M-40 -104 Q-72 -84 -50 -62", "M40 -104 Q72 -84 50 -62", (-50, -62), (50, -62)),
    "shake": ("M-40 -104 Q-70 -84 -50 -62", "M40 -104 Q78 -120 70 -160", (-50, -62), (70, -160)),
    "scratch": ("M-40 -104 Q-30 -70 22 -84", "M40 -104 Q80 -140 46 -196", (22, -84), (46, -196)),
    "paddle": ("M-40 -104 Q-78 -96 -92 -110", "M40 -104 Q78 -96 92 -110", (-92, -110), (92, -110)),
}


def troll_face(mood: str) -> str:
    out = ""
    if mood in ("oh", "splash"):
        out += stroke("M-26 -22 q9 -9 18 -2 M26 -22 q-9 -9 -18 -2", INK, 5)
    else:  # grumpy V brows, but round and bushy
        out += stroke("M-28 -20 L-8 -12 M28 -20 L8 -12", "#5A3B22", 7)
    out += "".join(f'<circle cx="{sx * 15}" cy="-4" r="7.5" fill="#fff"/><circle cx="{sx * 14}" cy="-3" r="3.8" fill="{INK}"/>' for sx in (-1, 1))
    out += f'<circle cx="-28" cy="18" r="8" fill="#F0705F" opacity=".45"/><circle cx="28" cy="18" r="8" fill="#F0705F" opacity=".45"/>'
    if mood == "oh":
        out += f'<ellipse cy="31" rx="7" ry="9" fill="#5A2E22"/>'
    elif mood == "splash":
        out += f'<ellipse cy="31" rx="10" ry="7" fill="#5A2E22"/>'
    elif mood == "shout":
        out += f'<path d="M-16 26 Q0 22 16 26 Q12 42 0 42 Q-12 42 -16 26Z" fill="#5A2E22"/><path d="M4 26 l3 7 l3 -7Z" fill="#fff"/>'
    else:  # grump: a wobbly frown with one silly tooth poking up
        out += stroke("M-17 33 Q0 24 17 33", "#5A2E22", 4) + '<path d="M3 29 l3 -7 l3 7Z" fill="#fff"/>'
    out += f'<ellipse cy="10" rx="19" ry="15" fill="{NOSE}"/><ellipse cx="-6" cy="5" rx="5" ry="3.5" fill="#fff" opacity=".45"/>'
    return out


def troll(x: float, y: float, s: float = 1, arms: str = "cross", mood: str = "grump", shadow: bool = True) -> str:
    """The grumpy-silly troll, facing us. (x, y) is his feet. Mossy green, big potato nose, orange tufty hair."""
    a1, a2, h1, h2 = TROLL_ARMS[arms]
    out = stroke("M-20 -40 V-8 M20 -40 V-8", TROLL_D, 18)
    out += f'<ellipse cx="-26" cy="-5" rx="22" ry="10" fill="{TROLL_D}"/><ellipse cx="26" cy="-5" rx="22" ry="10" fill="{TROLL_D}"/>'
    out += f'<path d="M-46 -30 Q-64 -90 -36 -118 Q0 -132 36 -118 Q64 -90 46 -30 Q0 -18 -46 -30Z" fill="{TROLL}"/>'
    out += f'<ellipse cy="-74" rx="28" ry="28" fill="{TROLL_L}" opacity=".7"/>'
    out += "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{TROLL_D}" opacity=".7"/>' for a, b, r in [(-40, -92, 5), (-34, -80, 3.5), (40, -60, 4.5)])
    out += (f'<path d="M-49 -48 Q0 -38 49 -48 L52 -28 Q36 -16 18 -22 L0 -30 L-18 -22 Q-36 -16 -52 -28Z" fill="{SHORTS}"/>'
            f'<rect x="18" y="-44" width="14" height="12" rx="2" fill="#C9A15A" transform="rotate(-8 25 -38)"/>'
            + stroke("M20 -44 l10 9 M30 -44 l-10 9", "#8A5A36", 1.6))
    out += stroke(a1, TROLL, 16) + stroke(a2, TROLL, 16)
    out += "".join(f'<circle cx="{a}" cy="{b}" r="11" fill="{TROLL_D}"/>' for a, b in (h1, h2))
    head = (f'<path d="M-36 -8 L-68 -26 L-40 14Z M36 -8 L68 -26 L40 14Z" fill="{TROLL}"/>'
            f'<path d="M-40 -2 L-58 -18 L-42 6Z M40 -2 L58 -18 L42 6Z" fill="#E7A68F"/>'
            f'<circle r="42" fill="{TROLL}"/>'
            f'<path d="M-36 -22 L-34 -50 L-20 -36 L-10 -60 L2 -38 L14 -58 L20 -34 L34 -50 L36 -20 Q0 -40 -36 -22Z" fill="{HAIR}"/>'
            f'<path d="M14 -56 q10 -14 22 -8 q-6 12 -22 8Z" fill="{GRASS}"/>' + stroke("M14 -56 l14 -6", GRASS_D, 1.6)
            + troll_face(mood))
    out += f'<g transform="translate(0 -160)">{head}</g>'
    return group(x, y, s, False, 0, out, shadow)


# ---------------------------------------------------------------- scenery
def peak_range(pts: list, base: float, fill: str, snow: bool = True) -> str:
    pts = [(-60, pts[0][1] + 50)] + pts + [(860, pts[-1][1] + 50)]
    d = f"M-60 {base} L" + " L".join(f"{a} {b}" for a, b in pts) + f" L860 {base}Z"
    out = f'<path d="{d}" fill="{fill}"/>'
    if snow:
        full = [(-60, base)] + pts + [(860, base)]
        for i in range(1, len(full) - 1):
            (lx, ly), (px, py), (rx, ry) = full[i - 1], full[i], full[i + 1]
            if py > ly or py > ry:
                continue
            t = 34
            l = (px + (lx - px) * t / (ly - py) * .35 if ly != py else px - 20, py + t * .35 * 1)
            r = (px + (rx - px) * t / (ry - py) * .35 if ry != py else px + 20, py + t * .35)
            out += (f'<path d="M{l[0]:.0f} {l[1]:.0f} L{px} {py} L{r[0]:.0f} {r[1]:.0f} L{(px + r[0]) / 2:.0f} {py + t * .55:.0f} '
                    f'L{px} {py + t * .3:.0f} L{(px + l[0]) / 2:.0f} {py + t * .55:.0f}Z" fill="{SNOW}"/>')
    return out


def pine(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#pn" transform="translate({x} {y}) scale({s})"/>'


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def hut(x: float, y: float, s: float = 1) -> str:
    """A little red Norwegian hut with a grass roof, far away."""
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-22" y="-26" width="44" height="26" fill="#C8463A"/>'
            f'<path d="M-28 -24 L0 -44 L28 -24Z" fill="{GRASS_D}"/><rect x="-5" y="-14" width="10" height="14" fill="#7A2A22"/></g>')


def flowers(pts: list) -> str:
    out = ""
    for i, (a, b) in enumerate(pts):
        col = ("#F7D046", "#F2789F", "#FFFFFF", "#B48BE8")[i % 4]
        out += (f'<g transform="translate({a} {b})"><circle cx="-4" r="3.6" fill="{col}"/><circle cx="4" r="3.6" fill="{col}"/>'
                f'<circle cy="-4" r="3.6" fill="{col}"/><circle cy="4" r="3.6" fill="{col}"/><circle r="2.4" fill="#E58A2B"/></g>')
    return out


def tufts(pts: list, col: str, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def river(level: float = RIVER_Y, amp: float = 7) -> str:
    def wave(y: float) -> str:
        segs = "".join(f" T{x} {y}" for x in range(100, 801, 100))
        return f"M0 {y} Q50 {y - amp} 100 {y}{segs} V600 H0Z"
    ripples = " ".join(f"M{a} {b} h{w}" for a, b, w in [(40, 530, 34), (190, 560, 26), (330, 520, 40), (560, 550, 30), (700, 525, 34), (110, 585, 30), (450, 585, 36)])
    return (f'<path filter="url(#p)" d="{wave(level)}" fill="{RIVER}"/><path d="{wave(level + 30)}" fill="{RIVER_D}" opacity=".3"/>'
            + stroke(f"M0 {level - 2} Q50 {level - amp - 2} 100 {level - 2}" + "".join(f" T{x} {level - 2}" for x in range(200, 801, 100)), RIVER_L, 4)
            + f'<g opacity=".7">{stroke(ripples, "#fff", 4)}</g>')


def splash(x: float, y: float, s: float = 1) -> str:
    spikes = "M-110 0 L-92 -60 L-70 -14 L-56 -96 L-34 -20 L-14 -120 L4 -24 L26 -112 L40 -18 L64 -92 L74 -12 L98 -58 L110 0Z"
    drops = "".join(f'<path d="M{a} {b} q8 13 0 19 q-8 -6 0 -19z" fill="#fff"/>' for a, b in
                    [(-120, -110), (-80, -140), (-30, -168), (30, -164), (84, -138), (128, -100), (-140, -54), (146, -50)])
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><path d="{spikes}" fill="{RIVER_L}"/>'
            f'<path d="M-70 0 L-56 -50 L-38 -8 L-16 -76 L0 -10 L22 -70 L40 -8 L60 -48 L72 0Z" fill="#fff" opacity=".85"/>{drops}</g>')


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def trip(x: float, n: int, size: float) -> str:
    """Trip-trap marks under a goat's hooves on the deck: little curved taps, bigger for bigger goats."""
    out = ""
    for i in range(n):
        a = x - (n - 1) * 18 * size + i * 36 * size
        out += f"M{a - 8 * size:.0f} {DECK - 8} q{8 * size:.0f} {-10 * size:.0f} {16 * size:.0f} 0 "
    return f'<g opacity=".85">{stroke(out, INK, 2 + size)}</g>'


BACK = [cloud(170, 80, 1), cloud(620, 60, .9),
        peak_range([(80, 190), (180, 250), (290, 130), (400, 230), (520, 150), (640, 240), (740, 170)], 360, MTN),
        f'<path d="M0 300 Q140 250 330 300 V500 H0Z" fill="{DRY_HILL}"/>',
        f'<path d="M470 300 Q640 236 800 270 V500 H470Z" fill="{GRASS_L}"/>',
        hut(605, 268, .9), pine(520, 300, .7), pine(552, 300, .8), pine(770, 282, .8), pine(40, 290, .7)]
LEFT_BANK = (f'<path filter="url(#p)" d="M0 318 Q140 312 250 330 L264 500 H0Z" fill="{DRY}"/>'
             + tufts([(30, 340), (110, 360), (190, 345), (70, 420), (160, 410)], DRY_D, 2.6))
RIGHT_BANK = (f'<path filter="url(#p)" d="M800 318 Q660 312 550 330 L536 500 H800Z" fill="{GRASS}"/>'
              + tufts([(600, 350), (680, 342), (770, 356), (640, 420), (740, 410)], GRASS_D, 3)
              + flowers([(580, 380), (660, 370), (720, 392), (780, 372), (620, 450), (700, 440)]))
POSTS = f'<g filter="url(#p)"><rect x="310" y="344" width="20" height="200" fill="{WOOD_D}"/><rect x="470" y="344" width="20" height="200" fill="{WOOD_D}"/></g>'
RAIL = (stroke(" ".join(f"M{x} {DECK} V292" for x in (240, 320, 400, 480, 560)), WOOD_D, 7) + stroke("M234 292 H566", WOOD, 7))
DECK_ART = (f'<rect filter="url(#p)" x="226" y="{DECK}" width="348" height="20" rx="4" fill="{WOOD}"/>'
            + stroke(" ".join(f"M{x} {DECK + 3} v14" for x in range(246, 574, 22)), WOOD_D, 2)
            + stroke(f"M230 {DECK + 2} H570", WOOD_L, 2.4))
UNDER = (DECK + 20) + 222  # troll's feet when he stands in the river under the bridge (hair just under the deck)


def scene(*, under: str = "", deck: list = (), bank_l: list = (), bank_r: list = (), front: list = ()) -> list:
    """The bridge scene in draw order: back, banks, posts, troll under the bridge, deck, rail, goats, river, foreground."""
    return [*BACK, LEFT_BANK, RIGHT_BANK, *bank_l, *bank_r, POSTS, under, RAIL, DECK_ART, *deck, river(), *front]


DEFS = {
    "pn": (f'<g id="pn" filter="url(#p)"><rect x="-5" y="-16" width="10" height="16" fill="{WOOD_D}"/>'
           f'<path d="M0 -110 L-26 -60 L-14 -62 L-34 -24 L-18 -26 L-40 -12 L40 -12 L18 -26 L34 -24 L14 -62 L26 -60Z" fill="#2E7D4F"/></g>'),
}


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    defs = "".join(d for k, d in DEFS.items() if f'href="#{k}"' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/goats-{n:02d}.svg", "w") as fh:
        fh.write(doc)


L_ROW = [goat(95, 338, "big"), goat(165, 392, "middle"), goat(70, 446, "little")]  # big behind; middle and little in front, each with its own silhouette  # all three waiting on the left bank

# 01 cover
svg(1, "The Three Billy Goats Gruff", "Paper-cut cover: in a Norwegian valley with snowy blue mountains and dark pine trees, the three billy goats Gruff — a little white one, a middle-sized tan one and a big grey-brown one with great curly horns — stand in a row on the dry, brown side of the river. A wooden bridge crosses to a green hillside full of flowers, and under the bridge a grumpy green troll with a big potato nose and orange tufty hair peeks out from the river with a frown.", DAY, scene(
    under=troll(400, UNDER, 1, "cross", "grump"), bank_l=L_ROW))

# 02 three goats, close up, on the dry hillside
K2 = 1.45
svg(2, "Three billy goats called Gruff", "Paper-cut scene: three billy goats stand in a row on a dry, brown hillside, smiling — a little white goat with tiny horn bumps, a middle-sized tan goat with short horns and a little beard, and a big grey-brown goat with huge curly horns and a long beard.", DAY, [
    cloud(150, 90, 1.1), cloud(640, 70, 1),
    peak_range([(90, 210), (230, 290), (360, 170), (500, 280), (640, 190), (760, 260)], 400, MTN),
    pine(60, 350, .8), pine(740, 345, .9), pine(700, 352, .7),
    f'<path filter="url(#p)" d="M0 380 Q400 340 800 380 V600 H0Z" fill="{DRY}"/>',
    tufts([(60, 430), (300, 420), (520, 430), (720, 440), (160, 540), (420, 560), (650, 550)], DRY_D),
    goat(150, 520, "little", K2), goat(350, 525, "middle", K2), goat(600, 530, "big", K2)])

# 03 nothing left to eat on this side; green grass across the bridge
svg(3, "Green grass across the river", "Paper-cut scene: the three billy goats stand on the dry, brown side of a river where all the grass has been eaten, looking across a wooden bridge at the green hillside on the other side, full of grass and flowers. The bridge is quiet, and the space under it is dark and empty.", DAY, scene(
    bank_l=L_ROW, front=[marks(["M600 292 l6 -14", "M640 284 v-16", "M680 290 l-6 -14"], "#fff", 3.5)]))

# 04 the troll under the bridge
svg(4, "The grumpy troll under the bridge", "Paper-cut scene: under the wooden bridge, standing in the river, lives a grumpy troll. He is mossy green, with big pointy ears, a huge round potato nose, a tuft of orange hair with a leaf stuck in it, one silly tooth and a big grumpy frown. Nobody is on the bridge.", DAY, scene(
    under=troll(400, UNDER, 1, "cross", "grump"),
    front=[marks(["M330 430 q-14 -10 -26 -2", "M470 430 q14 -10 26 -2"], INK, 3)]))

# 05 the little goat trips across
svg(5, "Trip, trap! The little goat", "Paper-cut scene: the little white billy goat trots across the wooden bridge — trip, trap — while under the bridge the troll looks up crossly and shakes his fist. The middle-sized and big goats wait on the dry bank.", DAY, scene(
    under=troll(400, UNDER, 1, "shake", "shout"), bank_l=L_ROW[:2],
    deck=[goat(380, DECK, "little", pose="walk"), trip(380, 2, .7)]))

# 06 the little goat goes on to the grass
svg(6, "The little goat goes on", "Paper-cut scene: the little white goat has crossed the bridge and is happily munching grass among the flowers on the green side. Under the bridge the troll scratches his orange hair, waiting for a bigger goat. The middle and big goats are still on the dry bank.", DAY, scene(
    under=troll(400, UNDER, 1, "scratch", "grump"), bank_l=L_ROW[:2], bank_r=[goat(690, 352, "little", pose="graze", munch=True)]))

# 07 the middle goat trips across
svg(7, "Trip, trap! The middle goat", "Paper-cut scene: the middle-sized tan goat walks across the bridge — trip, trap, a little louder — and under the bridge the troll looks up and shakes his fist. The big goat waits on the dry bank, and the little goat munches on the green side.", DAY, scene(
    under=troll(400, UNDER, 1, "shake", "shout"), bank_l=[L_ROW[0]], bank_r=[goat(720, 352, "little", pose="graze", munch=True)],
    deck=[goat(400, DECK, "middle", pose="walk"), trip(400, 2, 1)]))

# 08 the middle goat goes on
svg(8, "The middle goat goes on", "Paper-cut scene: the middle-sized goat has joined the little goat on the green hillside, and both are eating grass. Under the bridge the troll frowns and grumbles. Only the big billy goat is left on the dry bank, with his great curly horns.", DAY, scene(
    under=troll(400, UNDER, 1, "cross", "grump"), bank_l=[L_ROW[0]],
    bank_r=[goat(620, 350, "middle", pose="graze", munch=True), goat(735, 356, "little", pose="graze", munch=True)]))

# 09 the big goat tramps across; the bridge creaks
svg(9, "TRIP, TRAP! The big goat", "Paper-cut scene: the big grey-brown billy goat with huge curly horns tramps onto the bridge — TRIP, TRAP! — so heavily that the planks wobble. Under the bridge the troll's eyebrows shoot up in surprise. The little and middle goats watch from the green side.", DAY, scene(
    under=troll(400, UNDER, 1, "up", "oh"),
    bank_r=[goat(640, 350, "middle"), goat(740, 356, "little")],
    deck=[goat(330, DECK, "big", pose="walk"), trip(330, 3, 1.3)],
    front=[marks(["M300 362 q10 6 20 0", "M480 362 q10 6 20 0", "M250 368 q-6 8 -16 6", "M560 368 q6 8 16 6"], INK, 3)]))

# 10 the troll climbs up; the big goat lowers his horns
svg(10, "Well, come along then!", "Paper-cut scene: the grumpy troll has climbed up onto the bridge and stands with his hands on his hips, shouting. Facing him, the big billy goat lowers his head and his great curly horns, ready to push. The little and middle goats watch from the green side.", DAY, scene(
    bank_r=[goat(650, 350, "middle"), goat(740, 356, "little")],
    deck=[goat(300, DECK, "big", pose="butt", mood="brave"), troll(480, DECK, 1, "hips", "shout")]))

# 11 SPLASH! the troll lands in the river
svg(11, "SPLASH!", "Paper-cut scene: SPLASH! The big billy goat has butted the troll right off the bridge. The troll sits in the river in a great white splash, arms in the air, looking very surprised but not hurt, while the big goat stands proudly on the bridge and the little and middle goats watch from the green side.", DAY, scene(
    bank_r=[goat(650, 350, "middle"), goat(740, 356, "little")],
    deck=[goat(320, DECK, "big", mood="brave")],
    front=[splash(470, RIVER_Y + 44, 1.25), troll(470, 600, 1, "up", "splash", False), river(RIVER_Y + 40, 5),
           f'<g filter="url(#p)" fill="#fff" opacity=".9"><ellipse cx="400" cy="{RIVER_Y + 38}" rx="34" ry="9"/><ellipse cx="540" cy="{RIVER_Y + 38}" rx="34" ry="9"/></g>']))

# 12 the troll swims away, grumbling, and never comes back
grumble = (f'<g transform="translate(250 372)" filter="url(#p)"><ellipse rx="44" ry="26" fill="#fff"/>'
           + stroke("M-28 2 q6 -12 12 0 q6 12 12 0 q6 -12 12 0 q6 12 12 0", "#5A3B22", 3.4) + '</g>'
           + '<path d="M222 390 l-14 20 l24 -16Z" fill="#fff"/>')
svg(12, "The troll swims away", "Paper-cut scene: the soggy troll swims away down the river, paddling his arms and grumbling, with a little grumble-cloud over his head and bubbles behind him. The big billy goat stands on the bridge, and the middle and little goats watch from the green hillside.", DAY, scene(
    deck=[goat(470, DECK, "big")], bank_r=[goat(650, 350, "middle"), goat(740, 356, "little")],
    front=[troll(160, 630, 1, "paddle", "grump", False), river(RIVER_Y + 4, 5),
           marks(["M280 512 h40", "M288 532 h56", "M280 552 h38"], "#fff", 4),
           '<g fill="#fff" opacity=".9"><circle cx="348" cy="500" r="6"/><circle cx="370" cy="488" r="4"/><circle cx="386" cy="502" r="3"/></g>',
           grumble]))

# 13 three fat goats on the green hillside
K13 = 1.3
svg(13, "Fat and happy on the hillside", "Paper-cut scene: in the warm golden light, the three billy goats Gruff — little, middle and big — munch sweet green grass on the hillside among yellow, pink and white flowers. They have grown round and well-fed, and snowy mountains rise behind them.", GOLDEN, [
    cloud(160, 90, 1), cloud(620, 70, .9, .8),
    peak_range([(90, 200), (240, 280), (380, 160), (520, 270), (650, 180), (770, 250)], 390, MTN),
    f'<path d="M0 390 Q200 360 400 380 T800 370 V600 H0Z" fill="{GRASS_L}"/>',
    pine(40, 380, .6), pine(760, 372, .7),
    f'<path filter="url(#p)" d="M0 430 Q400 396 800 430 V600 H0Z" fill="{GRASS}"/>',
    tufts([(60, 470), (250, 460), (480, 455), (700, 470), (120, 580), (380, 590), (620, 585)], GRASS_D),
    flowers([(90, 500), (220, 560), (300, 470), (450, 575), (540, 470), (720, 520), (760, 580), (60, 570), (650, 455)]),
    goat(150, 545, "little", K13, pose="graze", fat=True, munch=True),
    goat(350, 560, "middle", K13, pose="graze", fat=True, munch=True),
    goat(600, 565, "big", K13, fat=True, munch=True)])
