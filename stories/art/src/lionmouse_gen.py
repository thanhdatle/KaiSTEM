#!/usr/bin/env python3
"""Generates the 13 Lion-and-the-Mouse flip-book SVGs from shared character parts.

Usage: python3 lionmouse_gen.py <output-dir>
Scale rule: the lion is always drawn at scale 1 and the mouse always at MS, on every page,
so the mouse stays tiny and the lion stays huge. The mouse's home hole is always on the right.
Net geometry is fixed relative to the lion: five tie-down ropes run from the net's edge to five pegs.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
BODY, BODY_D, BODY_L = "#E9AE4E", "#C88A33", "#F7D697"
MANE, MANE_D = "#B45A28", "#8C421D"
NOSE, MOUTH = "#6E3528", "#7A2630"
MOUSE, MOUSE_D, MOUSE_L, PINK = "#8E8C9C", "#6E6C7E", "#CFCDD8", "#EE9FAA"
ROPE, ROPE_L, PEG = "#7A4E2A", "#C99A62", "#6B4428"
GRASS, GRASS_D, GRASS_L = "#B9C56B", "#93A44E", "#D3DA8E"
HILL, HILL_FAR = "#A6B9A0", "#B8C4D8"
OLIVE, OLIVE_D, TRUNK = "#AAB78E", "#7F9068", "#76604A"
ROCK, ROCK_D = "#C9B9A2", "#A8977F"
POPPY = "#E2463A"
DAY = [(0, "#79C3EA"), (1, "#EEF7FB")]
GOLDEN = [(0, "#8CC4E6"), (.55, "#FDE3B8"), (1, "#FBCB8E")]
MS = 1.45  # the mouse's fixed scale
HOLE = (718, 452)  # the mouse's home, a hole under a rock, always on the right
# tie-down ropes: (attach point on the net edge, peg in the ground), relative to the lion's (x0, y0)
ROPES = [((-262, -12), (-298, 46)), ((-150, -2), (-166, 62)), ((-22, 0), (-22, 70)),
         ((100, -2), (116, 62)), ((192, -14), (232, 46))]
DOME = "M-275 0 C-275 -150 -165 -238 -40 -238 C95 -238 206 -170 206 0Z"


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- the lion
def lion_face(mood: str) -> str:
    """Face parts, drawn around the face centre, lion looking right."""
    out = ""
    if mood == "sleep":
        out += stroke("M2 -8 q7 6 14 0 M28 -10 q7 6 14 0", INK, 3.2)
    elif mood in ("laugh", "roar"):
        out += stroke("M2 -6 q7 -8 14 0 M28 -8 q7 -8 14 0", INK, 3.4)
    else:
        out += "".join(f'<circle cx="{a}" cy="-8" r="7" fill="#fff"/><circle cx="{a + 2}" cy="-8" r="4" fill="{INK}"/>' for a in (10, 36))
        if mood == "worry":
            out += stroke("M2 -22 L16 -26 M30 -27 L44 -22", INK, 3.2)
        elif mood == "hmm":
            out += stroke("M2 -20 L16 -20 M30 -26 L44 -22", INK, 3.2)
        elif mood == "wake":
            out += stroke("M2 -24 L16 -22 M30 -23 L44 -25", INK, 3)
    out += '<circle cx="2" cy="16" r="7" fill="#F0705F" opacity=".35"/>'
    out += f'<ellipse cx="36" cy="18" rx="26" ry="18" fill="{BODY_L}"/>'
    if mood == "roar":
        out += f'<path d="M18 26 Q36 18 56 24 Q58 52 36 54 Q18 52 18 26Z" fill="{MOUTH}"/>'
        out += '<path d="M22 27 l4 8 l4 -9Z M46 23 l4 8 l4 -8Z" fill="#fff"/>'
    elif mood == "laugh":
        out += f'<path d="M20 26 Q38 22 54 24 Q52 44 36 44 Q22 42 20 26Z" fill="{MOUTH}"/><ellipse cx="37" cy="38" rx="9" ry="4" fill="#E87A86"/>'
    elif mood == "worry":
        out += stroke("M28 32 q8 -5 16 0", INK, 3)
    else:
        out += stroke("M24 26 q6 6 12 0 q6 6 12 0", INK, 3)
    out += f'<path d="M30 6 L50 6 Q48 16 40 18 Q32 16 30 6Z" fill="{NOSE}"/>'
    out += '<g fill="#8C5A2A" opacity=".55"><circle cx="26" cy="22" r="1.6"/><circle cx="30" cy="27" r="1.6"/><circle cx="48" cy="22" r="1.6"/><circle cx="52" cy="27" r="1.6"/></g>'
    return out


def lion_head(mood: str, tilt: float = 0) -> str:
    scallops = "".join(
        f'<circle cx="{c[0]}" cy="{c[1]}" r="22" fill="{MANE}"/>'
        for c in [(-52, -30), (-60, 4), (-50, 38), (-22, 58), (12, 62), (44, 50), (-30, -56), (2, -66), (34, -58), (58, -34)])
    out = scallops + f'<circle r="60" fill="{MANE}"/><circle cx="-8" cy="4" r="44" fill="{MANE_D}" opacity=".35"/>'
    out += f'<circle cx="-14" cy="-42" r="14" fill="{BODY}"/><circle cx="-14" cy="-42" r="7" fill="#E6918A"/>'
    out += f'<circle cx="30" cy="-46" r="13" fill="{BODY}"/><circle cx="30" cy="-46" r="6.5" fill="#E6918A"/>'
    out += f'<ellipse cx="14" cy="2" rx="44" ry="46" fill="{BODY}"/>'
    out += f'<g transform="translate(-4 0)">{lion_face(mood)}</g>'
    return f'<g transform="rotate({tilt})">{out}</g>'


def lion_lie(x: float, y: float, mood: str = "wake", tilt: float = 0) -> str:
    """The lion lying down, side view facing right. (x, y) is the ground under his chest."""
    out = stroke("M-196 -26 Q-240 -4 -262 -18", BODY_D, 9)
    out += f'<ellipse cx="-270" cy="-22" rx="13" ry="10" fill="{MANE}"/>'
    out += f'<ellipse cx="-62" cy="-58" rx="140" ry="56" fill="{BODY}"/>'
    out += f'<ellipse cx="-60" cy="-26" rx="110" ry="20" fill="{BODY_L}" opacity=".55"/>'
    out += f'<ellipse cx="-150" cy="-58" rx="58" ry="52" fill="{BODY_D}"/>'
    out += f'<ellipse cx="-108" cy="-12" rx="38" ry="13" fill="{BODY_D}"/>'
    r = 186 if mood == "sleep" else 146  # paws reach further out when his head rests on them
    out += stroke(f"M20 -26 L{r - 36} -18", BODY_D, 28)
    out += f'<ellipse cx="{r - 30}" cy="-16" rx="24" ry="15" fill="{BODY_D}"/>'
    out += f'<ellipse cx="44" cy="-28" rx="36" ry="24" fill="{BODY}"/>'
    out += f'<path d="M30 -38 Q{r - 40} -30 {r - 6} -26 L{r - 6} -2 Q{r - 60} -4 36 -4Z" fill="{BODY}"/>'
    out += f'<ellipse cx="{r + 8}" cy="-15" rx="28" ry="16" fill="{BODY}"/>'
    out += "".join(f'<circle cx="{r + 26 + dx}" cy="{cy}" r="7" fill="{BODY}"/>' for dx, cy in ((0, -22), (5, -13), (0, -4)))
    out += stroke(f"M{r + 22} -18 h8 M{r + 24} -9 h8", BODY_D, 2.4)
    hx, hy = (84, -70) if mood == "sleep" else (74, -118)
    out += f'<g transform="translate({hx} {hy})">{lion_head(mood, tilt)}</g>'
    return group(x, y, 1, False, out)


def lion_stand(x: float, y: float, mood: str = "smile") -> str:
    """The lion standing, side view facing right. (x, y) is the ground under him."""
    out = stroke("M-140 -176 Q-210 -210 -214 -134", BODY_D, 10)
    out += f'<ellipse cx="-214" cy="-128" rx="13" ry="16" fill="{MANE}"/>'
    out += stroke("M-118 -130 V-10 M70 -130 V-10", BODY_D, 32)
    out += f'<ellipse cx="-114" cy="-8" rx="24" ry="11" fill="{BODY_D}"/><ellipse cx="76" cy="-8" rx="24" ry="11" fill="{BODY_D}"/>'
    out += f'<ellipse cx="-10" cy="-158" rx="140" ry="56" fill="{BODY}"/>'
    out += f'<ellipse cx="-104" cy="-150" rx="52" ry="50" fill="{BODY_D}"/>'
    out += stroke("M-84 -130 V-10 M104 -130 V-10", BODY, 32)
    out += f'<ellipse cx="-80" cy="-8" rx="24" ry="11" fill="{BODY}"/><ellipse cx="110" cy="-8" rx="24" ry="11" fill="{BODY}"/>'
    out += f'<g transform="translate(124 -214)">{lion_head(mood)}</g>'
    return group(x, y, 1, False, out)


# ---------------------------------------------------------------- the mouse
def mouse_face(eye: str) -> str:
    if eye == "wide":
        return f'<circle cx="0" cy="0" r="3.6" fill="#fff"/><circle cx=".6" cy="0" r="2.2" fill="{INK}"/>'
    if eye == "happy":
        return stroke("M-2.6 .8 q2.6 -3.2 5.2 0", INK, 1.6)
    return f'<circle r="2.3" fill="{INK}"/><circle cx=".7" cy="-.7" r=".8" fill="#fff"/>'


def mouse(x: float, y: float, pose: str = "run", flip: bool = False, eye: str = "dot") -> str:
    """A tiny grey mouse, side view facing right (flip faces left). (x, y) is her feet.
    pose: run (on all fours), sit (sitting up, paws together), cheer (sitting up, arms up)."""
    if pose == "run":
        out = stroke("M-15 -8 Q-34 -2 -44 -15", PINK, 2.6)
        out += f'<ellipse cx="-8" cy="-1.5" rx="4.5" ry="2.4" fill="{PINK}"/><ellipse cx="9" cy="-1.5" rx="4.5" ry="2.4" fill="{PINK}"/>'
        out += f'<ellipse cy="-11" rx="17" ry="11" fill="{MOUSE}"/><ellipse cx="2" cy="-6" rx="11" ry="4.5" fill="{MOUSE_L}"/>'
        out += f'<path d="M10 -22 Q22 -24 34 -12 Q24 -6 12 -8Z" fill="{MOUSE}"/>'
        out += f'<circle cx="34" cy="-12" r="2.6" fill="{PINK}"/>'
        out += f'<circle cx="9" cy="-24" r="7.5" fill="{MOUSE_D}"/><circle cx="9" cy="-24" r="4.5" fill="{PINK}"/>'
        out += f'<g transform="translate(21 -16)">{mouse_face(eye)}</g>'
        out += stroke("M31 -12 l9 -3 M31 -11 l9 2", MOUSE_D, 1)
    else:
        out = stroke("M-8 -3 Q-30 0 -32 -14", PINK, 2.6)
        out += f'<ellipse cx="-2" cy="-1.5" rx="5" ry="2.4" fill="{PINK}"/><ellipse cx="8" cy="-1.5" rx="5" ry="2.4" fill="{PINK}"/>'
        out += f'<ellipse cy="-16" rx="12" ry="16" fill="{MOUSE}"/><ellipse cx="3" cy="-14" rx="7" ry="11" fill="{MOUSE_L}"/>'
        out += f'<path d="M-6 -46 Q8 -48 20 -36 Q10 -30 -2 -32Z" fill="{MOUSE}"/><ellipse cx="0" cy="-38" rx="9" ry="8" fill="{MOUSE}"/>'
        out += f'<circle cx="20" cy="-36" r="2.6" fill="{PINK}"/>'
        out += f'<circle cx="-4" cy="-48" r="7.5" fill="{MOUSE_D}"/><circle cx="-4" cy="-48" r="4.5" fill="{PINK}"/>'
        out += f'<g transform="translate(7 -40)">{mouse_face(eye)}</g>'
        out += stroke("M17 -36 l9 -3 M17 -35 l9 2", MOUSE_D, 1)
        if pose == "cheer":
            out += stroke("M6 -24 L14 -40 M-6 -24 L-12 -40", MOUSE, 4) + f'<circle cx="14" cy="-41" r="2.6" fill="{PINK}"/><circle cx="-12" cy="-41" r="2.6" fill="{PINK}"/>'
        else:
            out += stroke("M4 -24 L11 -22", MOUSE, 4) + f'<circle cx="12" cy="-22" r="2.8" fill="{PINK}"/>'
    return group(x, y, MS, flip, out)


# ---------------------------------------------------------------- the net
def net(x0: float, y0: float, snapped: tuple = ()) -> str:
    """A rope net over the lying lion, held down by five tie-down ropes. snapped: rope numbers 1-5 already cut."""
    out = f'<g transform="translate({x0} {y0})">'
    out += f'<path d="{DOME}" fill="url(#mesh)"/>'
    out += stroke(DOME[:-1], ROPE, 7) + stroke(DOME[:-1], ROPE_L, 2.4)
    for i, ((ax, ay), (px, py)) in enumerate(ROPES, start=1):
        out += f'<rect x="{px - 6}" y="{py - 20}" width="12" height="24" rx="4" fill="{PEG}"/><rect x="{px - 8}" y="{py - 14}" width="16" height="5" rx="2" fill="{ROPE_L}"/>'
        if i in snapped:
            m1 = (ax + (px - ax) * .3, ay + (py - ay) * .3)
            m2 = (ax + (px - ax) * .72, ay + (py - ay) * .72)
            for (sx, sy), (ex, ey) in (((ax, ay), m1), ((px, py - 10), m2)):
                out += stroke(f"M{sx} {sy} L{ex:.0f} {ey:.0f}", ROPE, 6)
                out += stroke(f"M{ex:.0f} {ey:.0f} l-4 5 M{ex:.0f} {ey:.0f} l4 5 M{ex:.0f} {ey:.0f} l0 6", ROPE_L, 1.8)
        else:
            out += stroke(f"M{ax} {ay} L{px} {py - 10}", ROPE, 6) + stroke(f"M{ax} {ay} L{px} {py - 10}", ROPE_L, 1.8)
    return out + '</g>'


def rope_point(x0: float, y0: float, i: int, t: float) -> tuple:
    (ax, ay), (px, py) = ROPES[i - 1]
    return x0 + ax + (px - ax) * t, y0 + ay + (py - 10 - ay) * t


def snip(x: float, y: float, s: float = 1) -> str:
    """A little white burst where a rope goes snip."""
    rays = " ".join(f"M{a * 10} {b * 10} L{a * 20} {b * 20}" for a, b in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)])
    return f'<g transform="translate({x} {y}) scale({s})" opacity=".95">{stroke(rays, "#fff", 4)}</g>'


def net_heap(x: float, y: float) -> str:
    """The net, pushed off, lying in a loose heap with its cut ropes."""
    d = "M-110 0 Q-120 -40 -70 -52 Q-20 -70 30 -48 Q90 -46 100 0Z"
    out = f'<g transform="translate({x} {y})" filter="url(#p)"><path d="{d}" fill="url(#mesh)"/>'
    out += stroke(d[:-1], ROPE, 6) + stroke(d[:-1], ROPE_L, 2)
    out += stroke("M-100 -2 L-140 10 M96 -4 L136 8 M-40 0 L-52 22 M40 0 L50 22", ROPE, 5)
    return out + '</g>'


# ---------------------------------------------------------------- scenery
def sun(x: float, y: float, r: float = 44) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r + 14}" fill="#FFE9A8" opacity=".6"/><circle cx="{x}" cy="{y}" r="{r}" fill="#FFD05A"/>'


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def olive_tree(x: float, y: float, s: float = 1) -> str:
    """A twisty olive tree, as on the hills of Greece. (x, y) is the base of the trunk."""
    out = f'<path d="M-26 0 Q-10 -30 -22 -56 Q-34 -80 -40 -104 L-26 -108 Q-14 -80 0 -70 Q14 -84 30 -108 L42 -102 Q24 -70 18 -50 Q8 -26 24 0Z" fill="{TRUNK}"/>'
    out += f'<path d="M-8 -60 q4 -12 -2 -22" stroke="#5E4C3A" stroke-width="3" fill="none"/>'
    blobs = [(-62, -128, 44, 34), (0, -158, 54, 40), (60, -132, 44, 34), (-34, -100, 48, 26), (34, -102, 48, 26), (-92, -106, 30, 22), (92, -108, 30, 22)]
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="{rx}" ry="{ry}" fill="{OLIVE_D}"/>' for a, b, rx, ry in blobs)
    out += "".join(f'<ellipse cx="{a}" cy="{b - 8}" rx="{rx - 10}" ry="{ry - 8}" fill="{OLIVE}"/>' for a, b, rx, ry in blobs)
    out += '<g fill="#4F5E3A">' + "".join(f'<ellipse cx="{a}" cy="{b}" rx="3.4" ry="4.6"/>' for a, b in [(-60, -130), (-20, -160), (20, -150), (66, -136), (-30, -104), (44, -106), (-92, -108), (90, -110)]) + '</g>'
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{out}</g>'


def tufts(pts: list, col: str = GRASS_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def poppies(pts: list) -> str:
    out = ""
    for i, (a, b) in enumerate(pts):
        col = (POPPY, "#F7D046", "#FFFFFF")[i % 3]
        out += (f'<g transform="translate({a} {b})">{stroke("M0 0 v12", GRASS_D, 2)}<circle cx="-3.5" cy="0" r="4" fill="{col}"/>'
                f'<circle cx="3.5" cy="0" r="4" fill="{col}"/><circle cy="-3.5" r="4" fill="{col}"/><circle r="2" fill="#3A2E28"/></g>')
    return out


def hole(x: float = HOLE[0], y: float = HOLE[1]) -> str:
    """The mouse's home: a round hole under a grey rock."""
    return (f'<g transform="translate({x} {y}) scale(.88)" filter="url(#p)"><path d="M-62 4 Q-66 -50 -18 -64 Q30 -76 60 -40 Q74 -14 64 4Z" fill="{ROCK}"/>'
            f'<path d="M-40 -40 Q-10 -60 28 -50" stroke="{ROCK_D}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M-22 4 Q-22 -30 0 -30 Q22 -30 22 4Z" fill="#3E3128"/></g>')


def zzz(x: float, y: float) -> str:
    return (f'<g transform="translate({x} {y})">' + stroke("M0 0 h14 l-14 16 h14", "#fff", 4)
            + stroke("M22 -26 h18 l-18 20 h18", "#fff", 4.6) + stroke("M48 -60 h22 l-22 26 h22", "#fff", 5.2) + '</g>')


def roar_lines(x: float, y: float) -> str:
    return (f'<g transform="translate({x} {y})" opacity=".95">'
            + stroke("M0 -30 q16 30 0 60 M26 -46 q24 46 0 92 M54 -62 q32 62 0 124", "#fff", 6) + '</g>')


def land(stops_sun: tuple = (650, 96), tree: tuple = (215, 372, 1.15), evening: bool = False) -> list:
    """Sky, sun, far hills, a golden-green meadow and an olive tree."""
    out = [sun(*stops_sun, 50 if evening else 44), cloud(170, 80, .9, .85) if not evening else "",
           f'<path d="M0 330 Q140 270 290 310 Q430 250 580 300 Q700 262 800 296 V600 H0Z" fill="{HILL_FAR}"/>',
           f'<path d="M0 360 Q200 320 420 350 Q620 322 800 344 V600 H0Z" fill="{HILL}"/>',
           f'<path d="M0 384 Q400 356 800 380 V600 H0Z" fill="{GRASS_L}"/>']
    if tree:
        out.append(olive_tree(*tree))
    out += [f'<path filter="url(#p)" d="M0 400 Q400 380 800 398 V600 H0Z" fill="{GRASS}"/>',
            tufts([(40, 430), (300, 418), (520, 424), (770, 432), (90, 570), (360, 585), (600, 578), (760, 560)])]
    return out


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    mesh = ('<pattern id="mesh" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<path d="M0 0 H26 M0 0 V26" stroke="{ROPE}" stroke-width="3.4" fill="none"/></pattern>') if "url(#mesh)" in joined else ""
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{mesh}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/lionmouse-{n:02d}.svg", "w") as fh:
        fh.write(doc)




X0, Y0 = 390, 470    # the lion under the olive tree, pages 1-6 and 13
NX, NY = 350, 480    # the lion in the net, pages 7-11
FAR = (120, 372, .55)  # a smaller olive tree further off, on the net pages
FLOWERS = poppies([(60, 500), (130, 560), (640, 548), (560, 590), (30, 590), (720, 520)])
SLEEP = [lion_lie(X0, Y0, "sleep"), zzz(X0 + 150, 330)]

# 01 cover
svg(1, "The Lion and the Mouse", "Paper-cut cover: on a sunny Greek hillside, a huge golden lion with a big orange-brown mane lies asleep under a silvery-green olive tree, his head resting near his paws. On the right, a tiny grey mouse with pink ears sits up beside her hole under a grey rock and looks at him.", DAY,
    land() + [hole(), FLOWERS] + SLEEP + [mouse(636, 470, "sit", True)])

# 02 the lion asleep
svg(2, "A lion fast asleep", "Paper-cut scene: a huge golden lion lies fast asleep in the shade of a silvery-green olive tree, his big front paws stretched out in front of him, with Zzz floating up. Red, yellow and white flowers dot the green grass, and a grey rock with a little hole sits on the right.", DAY,
    land() + [hole(), FLOWERS] + SLEEP)

# 03 the mouse scurries over his paw
svg(3, "Scurry, scurry", "Paper-cut scene: a tiny grey mouse scurries right across the tip of the sleeping lion's big front paw, heading for her hole under the rock on the right. The lion is still asleep with Zzz above his head.", DAY,
    land() + [hole(), FLOWERS] + SLEEP + [mouse(X0 + 220, Y0 - 29, "run")])

# 04 plop! the paw comes down on her tail
svg(4, "Caught by the tail", "Paper-cut scene: the lion is awake, with his head up and his eyes open. The tip of the tiny mouse's tail is stuck under his big front paw. The mouse, just in front of the paw, is trying to run to her hole on the right, her eyes wide.", DAY,
    land() + [hole(), FLOWERS, mouse(X0 + 238, Y0 + 2, "run", eye="wide"), lion_lie(X0, Y0, "wake")])

# 05 please let me go
svg(5, "Please let me go!", "Paper-cut scene: the tiny mouse has turned round and sits up in the grass in front of the lion's paws, her little paws held together, asking to be let go. The huge lion looks at her with one eyebrow raised.", DAY,
    land() + [hole(), FLOWERS, lion_lie(X0, Y0, "hmm"), mouse(X0 + 236, Y0 + 10, "sit", True)])

# 06 the lion laughs and lets her go
svg(6, "Ho, ho, ho!", "Paper-cut scene: the lion throws back his head and laughs, his mouth wide open and his eyes squeezed shut. The tiny mouse runs away through the grass towards her hole under the rock on the right.", DAY,
    land() + [hole(), FLOWERS, lion_lie(X0, Y0, "laugh", -14), mouse(624, 500, "run", eye="happy"),
              stroke("M560 488 h-20 M564 498 h-24", "#fff", 3)])

# 07 caught in a net
svg(7, "Caught in a net", "Paper-cut scene: days later, the lion lies in the grass caught under a big brown rope net, looking worried. The net is held down by five ropes tied to five wooden pegs in the ground. On the right is the grey rock with the mouse's hole.", DAY,
    land(tree=FAR) + [hole(), lion_lie(NX, NY, "worry"), net(NX, NY)])

# 08 ROAR!
svg(8, "ROAR!", "Paper-cut scene: the lion, still caught under the rope net, roars with his mouth wide open, and big white roar lines spread out to the right. Beside her hole under the rock on the right, the tiny mouse sits up with wide eyes, listening.", DAY,
    land(tree=FAR) + [hole(), lion_lie(NX, NY, "roar", -10), net(NX, NY), roar_lines(574, 330),
                      mouse(650, 470, "sit", eye="wide")])

# 09 the mouse runs to help
svg(9, "I'm coming!", "Paper-cut scene: the tiny mouse runs as fast as she can through the grass from her hole on the right towards the lion, who is still caught under the rope net with its five ropes and pegs. The lion looks at her in surprise.", DAY,
    land(tree=FAR) + [hole(), lion_lie(NX, NY, "wake"), net(NX, NY), mouse(670, 540, "run", True),
                      stroke("M714 520 h20 M710 530 h24", "#fff", 3)])

# 10 nibble, nibble, snip: ONE
p = rope_point(NX, NY, 5, .5)
svg(10, "Nibble, nibble, snip! One!", "Paper-cut scene: the tiny mouse has nibbled through the rope on the right-hand side of the net, and it has snapped in two with a little white burst. Four ropes still hold the net down over the lion, who watches her.", DAY,
    land(tree=FAR) + [hole(), lion_lie(NX, NY, "wake"), net(NX, NY, (5,)), snip(*p),
                      mouse(NX + 284, NY + 48, "run", True, "happy")])

# 11 snip TWO, snip THREE
p3 = rope_point(NX, NY, 3, .5)
svg(11, "Two! Three!", "Paper-cut scene: three ropes, from the right side of the net to the middle, have now snapped in two, each with a little white burst, the biggest at the middle one. The tiny mouse stands just beside the middle peg, and two ropes on the left still hold the net down over the lion, who is starting to smile.", DAY,
    land(tree=FAR) + [hole(), lion_lie(NX, NY, "smile"), net(NX, NY, (5, 4, 3)), snip(*p3, .8), snip(*rope_point(NX, NY, 4, .5), .5), snip(*rope_point(NX, NY, 5, .5), .5),
                      mouse(NX + 46, NY + 78, "run", True)])

# 12 four, five, FREE
svg(12, "Free!", "Paper-cut scene: the lion stands up tall and happy, free at last. The cut rope net lies in a loose heap on the grass behind him on the left, and the tiny mouse sits up in front of him on the right, cheering with both arms in the air.", DAY,
    land(tree=FAR) + [hole(), net_heap(170, 560), lion_stand(410, 500, "smile"), mouse(612, 540, "cheer", True, "happy")])

# 13 friends
svg(13, "Little friends, big help", "Paper-cut scene: in the warm golden evening under the olive tree, the huge lion lies smiling in the grass, and the tiny mouse sits on the tip of his big front paw, smiling back up at him. They are friends.", GOLDEN,
    land(stops_sun=(660, 150), evening=True) + [hole(), FLOWERS, lion_lie(X0, Y0, "smile"), mouse(X0 + 180, Y0 - 30, "sit", True, "happy")])
