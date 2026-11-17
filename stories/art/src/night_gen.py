#!/usr/bin/env python3
"""Generates the 13 How-the-Night-Came flip-book SVGs from shared character parts.

Usage: python3 night_gen.py <output-dir>
Scale rule: on every canoe page the canoe and crew use the same scale, so the oldest helper (red) is tallest,
the middle one (yellow) next, the littlest (teal) smallest. The Great Snake's head is always about twice a
helper's head, and the tucumã nut is always about the size of a helper's head (NUT_K everywhere), small enough to hold.
Canoe geometry: gunwale at y = GUN, river surface at y = WATER on canoe pages; the crew sits at x offsets SEATS.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SKIN, SKIN_D, HAIR_C = "#A8714F", "#8A5A3C", "#2B2320"
CREW = [("old", "#D9573B", 1.1), ("mid", "#E8B33C", 1.0), ("lit", "#2F9E8F", .85)]  # stern -> bow
DRESS, HUSB = "#4FA37A", "#7C6BC4"
WOOD, WOOD_D, WOOD_L = "#9B5E34", "#6E3F20", "#C08452"
RIV, RIV_L = "#4FA7A0", "#9AD6CC"
NRIV, NRIV_L = "#1F3E66", "#4C6FA0"
G1, G2, G3 = "#2E7D4F", "#3F9A56", "#5DB85C"
N1, N2, N3 = "#16302F", "#1E433F", "#2A5A50"
SNAKE, SNAKE_D, BELLY = "#3FA58E", "#2A7A68", "#E8D98A"
NUT, NUT_L, WAX = "#5A3A24", "#7E5638", "#E8A33C"
DUSK_IN = "#141B3D"
FONT = "'Arial Rounded MT Bold', 'Comic Sans MS', 'Trebuchet MS', sans-serif"
DAY = [(0, "#8FD3F0"), (1, "#FFF1C4")]
NIGHT = [(0, "#10173A"), (1, "#2D3B7A")]
DAWN = [(0, "#2D3B7A"), (.5, "#C77BA8"), (1, "#FFC48A")]
UNDER = [(0, "#6CC3B8"), (1, "#1F6E78")]
GUN, WATER = 410, 396
SEATS = (-135, 0, 130)
NUT_K = .6


def stroke(d: str, col: str = INK, w: float = 5, op: float = 1) -> str:
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{o}/>'


def group(x: float, y: float, s: float, inner: str, flip: bool = False, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- people
def face(mood: str, cy: float = -90) -> str:
    out = f'<circle cx="-12" cy="{cy + 8}" r="4.5" fill="#F0705F" opacity=".4"/><circle cx="12" cy="{cy + 8}" r="4.5" fill="#F0705F" opacity=".4"/>'
    if mood == "sleep":
        return out + stroke(f"M-12 {cy} q4 4 8 0 M4 {cy} q4 4 8 0", INK, 2.4) + stroke(f"M-4 {cy + 11} q4 3 8 0", INK, 2.2)
    if mood == "tired":  # droopy half-closed eyes, little yawn
        out += f'<path d="M-12.5 {cy} a4 4 0 0 0 8 0Z M4.5 {cy} a4 4 0 0 0 8 0Z" fill="{INK}"/>'
        return out + f'<ellipse cy="{cy + 13}" rx="4" ry="5" fill="#5A2E22"/>'
    look = 2.2 if mood == "listen" else 0
    out += f'<circle cx="{-8 + look}" cy="{cy}" r="3.2" fill="{INK}"/><circle cx="{8 + look}" cy="{cy}" r="3.2" fill="{INK}"/>'
    if mood == "oh":
        out += stroke(f"M-13 {cy - 9} q5 -4 9 0 M4 {cy - 9} q5 -4 9 0", INK, 2.4) + f'<ellipse cy="{cy + 12}" rx="4.5" ry="6" fill="#5A2E22"/>'
    elif mood == "no":
        out += stroke(f"M-13 {cy - 8} l9 3 M13 {cy - 8} l-9 3", INK, 2.6) + stroke(f"M-6 {cy + 12} h12", INK, 2.6)
    else:
        out += stroke(f"M-7 {cy + 9} q7 6 14 0", INK, 2.6)
    return out


ARMS = {  # (arm path a, arm path b, hand a, hand b) from shoulders at (-20,-58) and (20,-58)
    "paddle": ("M-20 -58 Q4 -62 28 -74", "M20 -58 Q38 -42 42 -24", (28, -74), (42, -24)),
    "hold": ("M-20 -58 Q-28 -36 -14 -30", "M20 -58 Q28 -36 14 -30", (-14, -30), (14, -30)),
    "ear": ("M-20 -58 Q-42 -70 -27 -90", "M20 -58 Q30 -36 24 -18", (-27, -90), (24, -18)),
    "up": ("M-20 -58 Q-36 -84 -42 -120", "M20 -58 Q36 -84 42 -120", (-42, -120), (42, -120)),
    "stop": ("M-20 -58 Q-30 -36 -22 -16", "M20 -58 Q44 -70 46 -96", (-22, -16), (46, -96)),
    "reach": ("M-20 -58 Q20 -52 52 -50", "M20 -58 Q44 -54 62 -62", (52, -50), (62, -62)),
    "warm": ("M-20 -58 Q4 -34 34 -30", "M20 -58 Q40 -40 54 -36", (34, -30), (54, -36)),
    "point": ("M-20 -58 Q-30 -36 -22 -16", "M20 -58 Q46 -46 62 -22", (-22, -16), (62, -22)),
    "rest": ("M-20 -58 Q-30 -36 -22 -16", "M20 -58 Q30 -36 22 -16", (-22, -16), (22, -16)),
}


def body_bits(arms: str) -> str:
    a1, a2, h1, h2 = ARMS[arms]
    return stroke(a1, SKIN, 11) + stroke(a2, SKIN, 11) + "".join(f'<circle cx="{a}" cy="{b}" r="6.5" fill="{SKIN}"/>' for a, b in (h1, h2))


def sitter(x: float, y: float, s: float, shirt: str, arms: str = "rest", mood: str = "smile",
           flip: bool = False, paddle: bool = False, legs: bool = False) -> str:
    """A helper sitting down, facing us. (x, y) is the hips (hidden behind the gunwale in the canoe).
    legs=True adds crossed legs for sitting on the ground."""
    out = ""
    if paddle:
        out += stroke("M24 -88 L50 18", WOOD_D, 6) + f'<ellipse cx="52" cy="26" rx="8" ry="18" fill="{WOOD_L}" transform="rotate(-15 52 26)"/>'
    out += f'<path d="M-25 10 Q-30 -48 -19 -62 Q0 -70 19 -62 Q30 -48 25 10Z" fill="{shirt}"/>'
    if legs:
        out += (f'<path d="M-46 14 Q-50 -6 -22 -2 L22 -2 Q50 -6 46 14 Q0 28 -46 14Z" fill="#6E5A44"/>'
                + "".join(f'<ellipse cx="{a}" cy="16" rx="11" ry="6" fill="{SKIN_D}"/>' for a in (-40, 40)))
    out += f'<rect x="-6" y="-72" width="12" height="10" fill="{SKIN_D}"/><circle cy="-90" r="22" fill="{SKIN}"/>'
    out += f'<path d="M-23 -90 Q-25 -118 0 -116 Q25 -118 23 -90 Q14 -104 0 -100 Q-14 -104 -23 -90Z" fill="{HAIR_C}"/>'
    return group(x, y, s, out + face(mood) + body_bits(arms), flip)


def stander(x: float, y: float, s: float, kind: str, arms: str = "rest", mood: str = "smile", flip: bool = False) -> str:
    """A standing grown-up facing us. kind: 'daughter' (long hair, green scale-pattern dress, flower) or 'husband'.
    (x, y) is the feet."""
    out = ""
    if kind == "daughter":
        out += f'<path d="M-24 -150 Q-34 -110 -28 -92 L28 -92 Q34 -110 24 -150Z" fill="{HAIR_C}"/>'
        out += stroke("M-12 -54 V-4 M12 -54 V-4", SKIN_D, 10)
        out += f'<path d="M-20 -116 Q0 -124 20 -116 L38 -40 Q0 -30 -38 -40Z" fill="{DRESS}"/>'
        out += "".join(f'<path d="M{a} {b} q6 6 12 0" stroke="#2F7A55" stroke-width="2.4" fill="none"/>' for a, b in
                       [(-20, -90), (-2, -94), (8, -76), (-14, -66), (14, -58), (-26, -50), (0, -50), (22, -44)])
    else:
        out += stroke("M-12 -54 V-4 M12 -54 V-4", SKIN_D, 11)
        out += '<path d="M-24 -60 L24 -60 L26 -36 L-26 -36Z" fill="#6E5A44"/>'
        out += f'<path d="M-22 -116 Q0 -124 22 -116 Q30 -80 26 -56 L-26 -56 Q-30 -80 -22 -116Z" fill="{HUSB}"/>'
    out += "".join(f'<ellipse cx="{a}" cy="-3" rx="10" ry="5" fill="{SKIN_D}"/>' for a in (-13, 13))
    arm = f'<g transform="translate(0 -54)">{body_bits(arms)}</g>'
    head = f'<g transform="translate(0 -36)"><rect x="-6" y="-90" width="12" height="10" fill="{SKIN_D}"/><circle cy="-104" r="22" fill="{SKIN}"/>'
    head += f'<path d="M-23 -104 Q-25 -132 0 -130 Q25 -132 23 -104 Q14 -118 0 -114 Q-14 -118 -23 -104Z" fill="{HAIR_C}"/>'
    if kind == "daughter":
        head += ('<g transform="translate(18 -122)">' + "".join(f'<circle cx="{a}" cy="{b}" r="5" fill="#F2789F"/>' for a, b in [(-5, 0), (5, 0), (0, -5), (0, 5)])
                 + '<circle r="3" fill="#F7D046"/></g>')
    head += face(mood, -104) + "</g>"
    return group(x, y, s, out + arm + head, flip)


# ---------------------------------------------------------------- the canoe and crew
def canoe(cx: float, y: float, half: float = 220) -> str:
    hull = (f'<path filter="url(#p)" d="M{cx - half - 26} {y - 20} Q{cx - half + 10} {y + 52} {cx} {y + 54} '
            f'Q{cx + half - 10} {y + 52} {cx + half + 26} {y - 20} L{cx + half} {y} L{cx - half} {y}Z" fill="{WOOD}"/>')
    return (hull + stroke(f"M{cx - half} {y + 2} H{cx + half}", WOOD_L, 4)
            + stroke(f"M{cx - half + 40} {y + 26} Q{cx} {y + 36} {cx + half - 40} {y + 26}", WOOD_D, 2.4, .6))


def crew(cx: float, poses: list, moods: list, paddles: tuple = (True, False, True)) -> str:
    return "".join(sitter(cx + SEATS[i], GUN + 14, sz, shirt, poses[i], moods[i], paddle=paddles[i])
                   for i, (_, shirt, sz) in enumerate(CREW))


def nut(x: float, y: float, s: float = NUT_K, state: str = "shut", glow: bool = False) -> str:
    """The sealed tucumã nut: a dark, hard palm nut with a pointy tip and a band of golden wax. (x, y) is its centre."""
    out = '<circle r="44" fill="#FFF3B0" opacity=".35"/>' if glow else ""
    if state == "open":
        out += f'<path d="M-26 6 Q-28 34 0 36 Q28 34 26 6Z" fill="{NUT}"/><ellipse cy="6" rx="26" ry="7" fill="{DUSK_IN}"/>'
        out += (f'<g transform="translate(-34 -24) rotate(-38)"><path d="M-26 0 Q-24 -32 0 -40 Q24 -32 26 0Z" fill="{NUT_L}"/>'
                + stroke("M-26 0 H26", WAX, 5) + '</g>')
        return group(x, y, s, out)
    out += f'<path d="M0 -38 Q26 -28 26 2 Q24 32 0 34 Q-24 32 -26 2 Q-26 -28 0 -38Z" fill="{NUT}"/>'
    out += f'<ellipse cx="-9" cy="-14" rx="6" ry="11" fill="{NUT_L}" opacity=".8"/>'
    out += stroke("M-26 2 Q0 12 26 2", WAX, 7) + f'<path d="M6 8 q3 8 0 11 q-3 -3 0 -11Z" fill="{WAX}"/>'
    return group(x, y, s, out)


def words(items: list, op: float = 1) -> str:
    return "".join(f'<text x="{tx}" y="{ty}" font-family="{FONT}" font-size="{sz}" font-weight="700" fill="#fff" stroke="{INK}" '
                   f'stroke-width="5" paint-order="stroke" text-anchor="middle" opacity="{op}">{w}</text>' for tx, ty, w, sz in items)


def sound(x: float, y: float, items: list, op: float = 1) -> str:
    """Little sound-curls and floating words coming out of the nut."""
    curls = (f"M{x + 32} {y - 10} q10 -10 0 -20 M{x + 44} {y - 4} q16 -16 0 -32 "
             f"M{x - 32} {y - 10} q-10 -10 0 -20 M{x - 44} {y - 4} q-16 -16 0 -32")
    return stroke(curls, "#fff", 3.4, .95) + words(items, op)


# ---------------------------------------------------------------- the Great Snake
def snake_head(mood: str = "smile") -> str:
    """Big friendly snake head facing right, local origin at the back of the head."""
    out = f'<path d="M-10 -28 Q40 -40 74 -14 Q86 0 74 14 Q40 32 -10 24 Q-24 0 -10 -28Z" fill="{SNAKE}"/>'
    out += f'<path d="M0 16 Q40 26 74 12 Q60 26 30 28 Q8 28 0 16Z" fill="{BELLY}"/>'
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="6" ry="4" fill="{SNAKE_D}"/>' for a, b in [(4, -14), (20, -24), (36, -26)])
    if mood == "sleep":
        out += stroke("M36 -14 q7 6 14 0", INK, 3)
    else:
        out += f'<circle cx="44" cy="-14" r="10" fill="#fff"/><circle cx="47" cy="-14" r="5.5" fill="{INK}"/><circle cx="49" cy="-16" r="2" fill="#fff"/>'
    out += f'<circle cx="74" cy="-6" r="2.2" fill="{INK}"/>' + stroke("M46 10 Q60 16 74 8", INK, 3)
    out += '<circle cx="34" cy="4" r="6" fill="#F0705F" opacity=".35"/>'
    if mood != "sleep":
        out += stroke("M84 2 l12 0 l6 -5 M96 2 l6 5", "#D9463B", 2.4)
    return out


def snake_rising(x: float, y: float, s: float = 1, mood: str = "smile", flip: bool = False) -> str:
    """The Great Snake's neck rising out of the river at (x, y), head up and looking right, with two humps of
    body showing behind it in the water and a tail tip."""
    humps = "M-230 8 Q-200 -44 -170 8 M-140 8 Q-100 -60 -60 8"
    out = stroke(humps, SNAKE, 34) + stroke(humps, SNAKE_D, 6, .4) + stroke("M-270 8 Q-258 -18 -246 -8", SNAKE, 14)
    out += stroke("M0 10 Q-14 -60 18 -120", SNAKE, 38) + stroke("M12 4 Q0 -58 28 -112", BELLY, 10, .9)
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="6" ry="4" fill="{SNAKE_D}"/>' for a, b in [(-10, -20), (-8, -56), (4, -92)])
    out += f'<g transform="translate(14 -138) rotate(-6)">{snake_head(mood)}</g>'
    return group(x, y, s, out, flip)


def snake_lying(x: float, y: float, s: float = 1, mood: str = "smile") -> str:
    """The Great Snake resting along the riverbed in gentle S-curves, head raised at the right end."""
    body = "M-260 30 Q-200 -40 -120 20 Q-40 80 40 20 Q100 -24 140 -56"
    out = stroke("M-330 44 Q-300 18 -262 30", SNAKE, 18) + stroke(body, SNAKE, 40) + stroke(body, BELLY, 8, .55)
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="7" ry="5" fill="{SNAKE_D}"/>' for a, b in [(-224, -2), (-150, 0), (-70, 44), (10, 40), (84, 2)])
    out += f'<g transform="translate(130 -80) rotate(-8)">{snake_head(mood)}</g>'
    return group(x, y, s, out)


# ---------------------------------------------------------------- forest, river, sky
def sun(x: float, y: float, r: float = 56) -> str:
    dirs = [(1, 0), (.71, .71), (0, 1), (-.71, .71), (-1, 0), (-.71, -.71), (0, -1), (.71, -.71)]
    rays = " ".join(f"M{x + (r + 14) * c:.0f} {y + (r + 14) * sn:.0f} L{x + (r + 34) * c:.0f} {y + (r + 34) * sn:.0f}" for c, sn in dirs)
    return f'<circle cx="{x}" cy="{y}" r="{r + 16}" fill="#FFE27A" opacity=".45"/><circle cx="{x}" cy="{y}" r="{r}" fill="#FFD23F"/>' + stroke(rays, "#FFC22E", 8)


def star(x: float, y: float, r: float = 7, col: str = "#FFF6C8") -> str:
    q = r * .2
    return (f'<path d="M{x} {y - r} Q{x + q} {y - q} {x + r} {y} Q{x + q} {y + q} {x} {y + r} '
            f'Q{x - q} {y + q} {x - r} {y} Q{x - q} {y - q} {x} {y - r}Z" fill="{col}"/>')


def stars(pts: list) -> str:
    return "".join(star(a, b, r) for a, b, r in pts)


def fireflies(pts: list) -> str:
    return "".join(f'<circle cx="{a}" cy="{b}" r="11" fill="#FFF07A" opacity=".28"/><circle cx="{a}" cy="{b}" r="4" fill="#FFF07A"/>' for a, b in pts)


def canopy(base: float, cols: tuple) -> str:
    """Rounded rainforest treetops along the far bank."""
    far, near = cols
    out = f'<path d="M0 {base} ' + " ".join(f"Q{x + 40} {base - 70 - (x * 37 % 40)} {x + 80} {base - 10}" for x in range(0, 800, 80)) + f' V{base + 120} H0Z" fill="{far}"/>'
    out += f'<path d="M-20 {base + 20} ' + " ".join(f"Q{x + 50} {base - 40 - (x * 53 % 30)} {x + 100} {base + 14}" for x in range(-20, 800, 100)) + f' V{base + 140} H-20Z" fill="{near}"/>'
    return out


def palm(x: float, y: float, s: float = 1, night: bool = False, lean: float = 0) -> str:
    trunk, leaf, leaf2 = ("#3A3328", N2, N3) if night else (WOOD_D, G1, G2)
    l = lean
    out = stroke(f"M0 0 Q{l * .4} -80 {l} -170", trunk, 12)
    tips = [(l - 50, -210, l - 96, -186), (l + 50, -214, l + 96, -180), (l - 60, -150, l - 84, -120), (l + 60, -150, l + 86, -124), (l, -220, l + 14, -214)]
    for i, (qx, qy, ex, ey) in enumerate(tips):
        out += stroke(f"M{l} -170 Q{qx} {qy} {ex} {ey}", leaf if i % 2 else leaf2, 16)
    return group(x, y, s, out)


def bush(x: float, y: float, s: float = 1, col: str = G2, col2: str = G3) -> str:
    return group(x, y, s, f'<path d="M-60 0 Q-70 -50 -30 -56 Q-20 -90 14 -80 Q50 -92 58 -50 Q80 -30 60 0Z" fill="{col}"/>'
                 f'<path d="M-30 -10 Q-34 -40 -6 -42 Q20 -60 34 -30 Q44 -14 30 -4Z" fill="{col2}" opacity=".8"/>')


def big_leaf(x: float, y: float, rot: float, s: float = 1, col: str = G2) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)"><path d="M0 0 Q40 -40 120 -10 Q50 30 0 0Z" fill="{col}"/>'
            + stroke("M4 0 Q60 -14 116 -10", "#fff", 2, .35) + '</g>')


def wave_path(level: float, amp: float) -> str:
    return f"M0 {level} Q50 {level - amp} 100 {level}" + "".join(f" T{x} {level}" for x in range(200, 801, 100))


def river(level: float, night: bool = False) -> str:
    col, light = (NRIV, NRIV_L) if night else (RIV, RIV_L)
    return f'<path d="{wave_path(level, 6)} V600 H0Z" fill="{col}"/>' + stroke(wave_path(level - 2, 6), light, 4)


def front_water(level: float, night: bool = False) -> str:
    col, light = (NRIV, NRIV_L) if night else (RIV, RIV_L)
    ripples = " ".join(f"M{a} {level + b} h{w}" for a, b, w in [(40, 50, 34), (210, 90, 30), (420, 60, 40), (600, 100, 30), (700, 46, 36), (120, 140, 28), (520, 150, 34)])
    return f'<path d="{wave_path(level, 5)} V600 H0Z" fill="{col}"/>' + stroke(wave_path(level - 1, 5), light, 3.4) + stroke(ripples, "#fff", 3.4, .45)


def hut(x: float, y: float, s: float = 1, night: bool = False, lit: bool = False) -> str:
    """A thatched house on short stilts with a doorway. (x, y) is the ground under its middle."""
    wall, roof, roof_d = ("#5E4A3A", "#6E5B3A", "#4F4128") if night else ("#C99A62", "#D9B45A", "#B08A3A")
    out = stroke("M-70 0 V-34 M70 0 V-34 M0 0 V-34", WOOD_D, 8)
    out += f'<rect x="-80" y="-42" width="160" height="10" fill="{WOOD_D}"/><rect x="-70" y="-110" width="140" height="70" fill="{wall}"/>'
    out += stroke(" ".join(f"M{a} -108 V-44" for a in range(-56, 70, 16)), WOOD_D, 1.6, .5)
    out += f'<rect x="-16" y="-98" width="32" height="56" rx="4" fill="{"#F7C85A" if lit else "#4A3226"}"/>'
    out += f'<path d="M-100 -104 L0 -170 L100 -104Z" fill="{roof}"/>' + stroke(" ".join(f"M{a} -106 L{a * .3:.0f} -150" for a in range(-84, 100, 24)), roof_d, 2.4)
    return group(x, y, s, out)


def hammock(x1: float, x2: float, y: float, col: str, sleeper: str = "sleep", hair_long: bool = False, night: bool = False) -> str:
    """A deep hammock slung between two posts. Someone lies snug inside it: only the head peeps over the near edge,
    at the left end, and a little bump shows their feet at the right end."""
    post = "#3A3328" if night else WOOD_D
    mid = (x1 + x2) / 2
    a, b = x1 + 26, x2 - 26
    out = (f'<g filter="url(#p)"><rect x="{x1 - 8}" y="{y - 40}" width="16" height="{640 - y}" fill="{post}"/>'
           f'<rect x="{x2 - 8}" y="{y - 40}" width="16" height="{640 - y}" fill="{post}"/></g>')
    out += stroke(f"M{x1} {y - 30} L{a} {y} M{x2} {y - 30} L{b} {y}", "#E8D9B8", 3)
    out += f'<path d="M{a} {y} Q{mid} {y + 40} {b} {y} Q{mid} {y + 20} {a} {y}Z" fill="{col}" opacity=".6"/>'
    hx, hy = a + 54, y + 12
    if hair_long:
        hair = f'<path d="M{hx - 26} {hy + 8} Q{hx - 34} {hy - 34} {hx} {hy - 28} Q{hx + 30} {hy - 30} {hx + 24} {hy + 8} Q{hx} {hy - 14} {hx - 26} {hy + 8}Z" fill="{HAIR_C}"/>'
    else:
        hair = f'<path d="M{hx - 22} {hy - 2} Q{hx - 24} {hy - 26} {hx} {hy - 24} Q{hx + 24} {hy - 26} {hx + 22} {hy - 2} Q{hx + 12} {hy - 14} {hx} {hy - 12} Q{hx - 12} {hy - 14} {hx - 22} {hy - 2}Z" fill="{HAIR_C}"/>'
    out += f'<circle cx="{hx}" cy="{hy}" r="20" fill="{SKIN}"/>{hair}<g transform="translate({hx} {hy + 90})">{face(sleeper, -90)}</g>'
    out += f'<ellipse cx="{b - 56}" cy="{y + 22}" rx="20" ry="12" fill="{col}"/>'
    out += f'<path filter="url(#p)" d="M{a} {y} Q{a + 20} {y + 30} {hx} {y + 26} Q{mid} {y + 50} {b - 56} {y + 26} Q{b - 20} {y + 20} {b} {y} Q{mid} {y + 140} {a} {y}Z" fill="{col}"/>'
    out += stroke(f"M{a + 16} {y + 30} Q{mid} {y + 108} {b - 16} {y + 26}", "#fff", 2.4, .4)
    out += stroke(f"M{a + 30} {y + 50} Q{mid} {y + 120} {b - 30} {y + 46}", "#fff", 2.4, .3)
    return out


# ---------------------------------------------------------------- creatures
def toucan(x: float, y: float, s: float = 1, mood: str = "smile", flip: bool = False) -> str:
    """A toucan perched on a branch, facing right: black body, cream bib, big orange beak with a black tip."""
    out = f'<path d="M-14 30 L-30 70 L-10 66 L-2 34Z" fill="{INK}"/><ellipse rx="22" ry="36" fill="{INK}"/>'
    out += '<ellipse cx="8" cy="-20" rx="14" ry="14" fill="#FFF6D6"/><path d="M-4 32 L-6 46 M6 32 L8 46" stroke="#5B7FD6" stroke-width="4"/>'
    out += f'<circle cx="6" cy="-32" r="16" fill="{INK}"/>'
    if mood == "yawn":
        out += '<path d="M18 -40 Q54 -54 72 -46 Q60 -38 20 -32Z" fill="#F6922E"/><path d="M20 -28 Q52 -14 66 -4 Q50 -6 18 -22Z" fill="#F6B83E"/>'
        out += '<path d="M20 -32 L64 -42 L60 -8 L20 -24Z" fill="#B8323A"/>'
    else:
        out += f'<path d="M18 -40 Q56 -48 74 -30 Q52 -18 18 -24Z" fill="#F6922E"/><path d="M58 -40 Q72 -36 74 -30 Q66 -28 60 -30Z" fill="{INK}"/>'
        out += stroke("M20 -32 Q48 -34 72 -31", "#C9601E", 2)
    out += '<circle cx="8" cy="-36" r="6" fill="#7FB2E6"/>'
    if mood == "sleep":
        out += stroke("M4 -36 q4 4 8 0", INK, 2.4)
    elif mood == "yawn":
        out += stroke("M4 -37 h8", INK, 2.6)
    else:
        out += f'<circle cx="9" cy="-36" r="3" fill="{INK}"/>'
    return group(x, y, s, out, flip)


def branch(x1: float, y1: float, x2: float, y2: float, night: bool = False) -> str:
    col, leaf = ("#3A3328", N3) if night else (WOOD_D, G2)
    return (f'<g filter="url(#p)">' + stroke(f"M{x1} {y1} Q{(x1 + x2) / 2} {y1 - 14} {x2} {y2}", col, 14)
            + f'<ellipse cx="{x2}" cy="{y2 - 6}" rx="26" ry="12" fill="{leaf}" transform="rotate(-20 {x2} {y2})"/></g>')


def frog(x: float, y: float, s: float = 1, sing: bool = False) -> str:
    """A little green frog on a lily pad: round body, two big eyes on top; a puffed-up throat when it sings."""
    out = f'<ellipse cy="6" rx="46" ry="12" fill="#2F6E4A"/><path d="M0 6 L36 0 L30 12Z" fill="{NRIV}"/>'
    out += '<ellipse cy="-14" rx="26" ry="18" fill="#6CC24A"/>'
    out += "".join(f'<circle cx="{a}" cy="-30" r="10" fill="#6CC24A"/><circle cx="{a}" cy="-31" r="6.5" fill="#fff"/><circle cx="{a}" cy="-31" r="3.4" fill="{INK}"/>' for a in (-12, 12))
    out += '<path d="M-30 0 q-6 -12 6 -12 M30 0 q6 -12 -6 -12" stroke="#4E9A36" stroke-width="7" fill="none" stroke-linecap="round"/>'
    out += '<ellipse cy="-4" rx="14" ry="10" fill="#D9F2A8"/>' if sing else stroke("M-8 -10 q8 6 16 0", INK, 2.4)
    return group(x, y, s, out)


def cujubim(x: float, y: float, s: float = 1, sing: bool = False) -> str:
    """The cujubim: a glossy black forest bird with a white crested head, a red throat, red legs and a long tail."""
    out = stroke("M-8 20 L-12 48 M8 20 L10 48", "#D9463B", 5) + stroke("M-18 48 h12 M4 48 h12", "#D9463B", 4)
    out += '<path d="M-24 0 L-74 30 L-66 40 L-22 16Z" fill="#1E1E2A"/><ellipse rx="34" ry="24" fill="#1E1E2A"/>'
    out += stroke("M-20 -6 q10 8 24 6", "#3A4A7A", 3, .8)
    out += '<path d="M14 -10 Q22 -34 30 -40 L40 -34 Q34 -18 30 -4Z" fill="#1E1E2A"/>'
    out += '<circle cx="36" cy="-44" r="14" fill="#FFFFFF"/><path d="M24 -54 L30 -70 L36 -56 L42 -68 L44 -52Z" fill="#FFFFFF"/>'
    out += f'<circle cx="38" cy="-46" r="3" fill="{INK}"/><path d="M48 -44 L62 -40 L48 -36Z" fill="#7E8AA8"/><ellipse cx="38" cy="-28" rx="5" ry="8" fill="#D9463B"/>'
    if sing:
        out += stroke("M70 -52 q8 -6 4 -16 M80 -44 q14 -10 6 -28", "#fff", 3)
    return group(x, y, s, out)


def inambu(x: float, y: float, s: float = 1) -> str:
    """The inambu (a tinamou): a round, soft grey-brown ground bird with a small head, short beak and almost no tail."""
    out = stroke("M-6 18 L-8 34 M8 18 L10 34", "#C9A07A", 4)
    out += '<ellipse rx="34" ry="24" fill="#9A8C7E"/><path d="M-30 -4 q20 10 46 0" stroke="#7A6C60" stroke-width="3" fill="none"/>'
    out += "".join(f'<circle cx="{a}" cy="{b}" r="2" fill="#6A5C50"/>' for a, b in [(-14, 6), (-2, 10), (10, 6), (-20, -4), (4, -6)])
    out += '<path d="M20 -10 Q28 -26 34 -30 L40 -26 Q36 -14 32 -2Z" fill="#9A8C7E"/><circle cx="38" cy="-32" r="11" fill="#A89A8C"/>'
    out += f'<circle cx="40" cy="-34" r="2.6" fill="{INK}"/><path d="M48 -32 L58 -30 L48 -27Z" fill="#6A5C50"/>'
    return group(x, y, s, out)


def string_ball(x: float, y: float) -> str:
    return (f'<g filter="url(#p)"><circle cx="{x}" cy="{y}" r="13" fill="#F2E3C2"/>'
            + stroke(f"M{x - 10} {y - 4} q10 -8 20 0 M{x - 10} {y + 4} q10 -8 20 0 M{x - 4} {y - 11} q8 10 0 22", "#C9B48A", 1.6) + '</g>')


def zzz(x: float, y: float) -> str:
    return "".join(f'<text x="{x + i * 18}" y="{y - i * 20}" font-family="{FONT}" font-size="{18 + i * 6}" font-weight="700" '
                   f'fill="#DCE6FF" opacity=".85">z</text>' for i in range(3))


# ---------------------------------------------------------------- page scaffolds
def river_day(level: float = WATER, small_palm: bool = True) -> list:
    return [canopy(300, (G1, G2)), palm(90, 340, .9, lean=-20), palm(700, 330, 1, lean=24), palm(560, 336, .7, lean=10) if small_palm else "",
            f'<path d="M0 352 Q200 330 400 346 T800 340 V{level + 20} H0Z" fill="{G3}"/>', river(level)]


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/night-{n:02d}.svg", "w") as fh:
        fh.write(doc)


CX = 400
HELD = (CX + SEATS[1], GUN - 30)  # where the middle helper holds the nut in her hands, above the gunwale

# 01 cover
svg(1, "How the Night Came", "Paper-cut cover: on a wide green river in the rainforest, under a bright sun, three helpers sit in a long wooden canoe. The oldest, in red, paddles at the back; the middle one, in yellow, holds a dark tucumã nut sealed with a band of golden wax; the littlest, in teal, paddles at the front. Palm trees and round treetops line the bank.", DAY, [
    sun(320, 90, 50), *river_day(),
    crew(CX, ["paddle", "hold", "paddle"], ["smile", "smile", "smile"]), canoe(CX, GUN), nut(*HELD),
    front_water(GUN + 30), big_leaf(-10, 560, -30, 1.2), big_leaf(810, 580, 210, 1.2, G1)])

# 02 only day: everybody tired
svg(2, "Only day, day, day", "Paper-cut scene: long ago, under a big blazing sun, a thatched house on stilts stands in the rainforest. In a red hammock slung between two posts, a man lies with droopy, tired eyes, yawning. Up on a branch, a black toucan with a big orange beak gives a huge yawn too.", DAY, [
    sun(400, 96, 64), canopy(300, (G1, G2)), palm(60, 330, .9, lean=-16), palm(760, 320, .9, lean=18),
    f'<path filter="url(#p)" d="M0 350 Q400 320 800 350 V600 H0Z" fill="{G3}"/>',
    hut(560, 410, 1.1), branch(800, 220, 640, 236), toucan(690, 196, 1, "yawn"),
    hammock(70, 340, 440, "#D9573B", "tired"), big_leaf(-10, 590, -24, 1.1), bush(760, 610, 1, G1, G2)])

# 03 the daughter of the Great Snake and her husband
svg(3, "There is no night!", "Paper-cut scene: in front of the thatched house, still under a blazing sun, the daughter of the Great Snake stands with long black hair, a pink flower and a green dress patterned like scales. She looks tired and points one hand down towards the river. Beside her, with a little gap between them, her husband in a purple shirt listens with a surprised look. The river shines below them.", DAY, [
    sun(140, 90, 52), canopy(280, (G1, G2)),
    f'<path filter="url(#p)" d="M0 330 Q400 300 800 330 V500 H0Z" fill="{G3}"/>', hut(640, 380, .9),
    river(500), stander(290, 470, 1.15, "daughter", "point", "tired", flip=True), stander(470, 470, 1.15, "husband", "rest", "oh"),
    big_leaf(-10, 590, -24, 1.1), big_leaf(810, 600, 204, 1.1, G1)])

# 04 under the river: the Great Snake and the sleeping night
weeds = "".join(stroke(f"M{a} 600 Q{a - 16} 520 {a + 6} 470 Q{a + 20} 430 {a} 400", G1, 10) for a in (50, 100, 700, 750))
svg(4, "At the bottom of the river", "Paper-cut scene: deep under the green river, among waving water-weeds and pebbles, the Great Snake rests along the sandy riverbed in gentle curves: long and teal-green, with a pale yellow belly, dark spots and a kind face. Snuggled against a curve of his body is a dark tucumã nut sealed with golden wax, glowing softly. Bubbles float up.", UNDER, [
    stroke("M0 70 Q200 50 400 70 T800 70", "#fff", 6, .25), weeds,
    f'<path filter="url(#p)" d="M0 500 Q400 470 800 500 V600 H0Z" fill="#C9B48A"/>',
    "".join(f'<ellipse cx="{a}" cy="{b}" rx="{r}" ry="{r * .6}" fill="#A8925A"/>' for a, b, r in [(90, 540, 18), (250, 560, 12), (520, 570, 16), (660, 540, 12)]),
    snake_lying(400, 450, 1), nut(360, 440, glow=True),
    "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="none" stroke="#fff" stroke-width="2.4" opacity=".7"/>' for a, b, r in [(600, 230, 8), (616, 190, 5), (606, 160, 4), (300, 300, 6), (290, 260, 4)])])

# 05 the three helpers paddle off down the river
svg(5, "Paddle, paddle", "Paper-cut scene: the three helpers paddle their long wooden canoe down the wide green river through the rainforest, under the bright sun. The oldest, in red, paddles at the back, the middle one, in yellow, sits in the middle, and the littlest, in teal, paddles at the front. The canoe is empty — no nut yet.", DAY, [
    sun(140, 90, 48), *river_day(),
    crew(CX, ["paddle", "rest", "paddle"], ["smile", "smile", "smile"]), canoe(CX, GUN), front_water(GUN + 30),
    stroke("M650 470 h50 M670 492 h40 M120 470 h-44 M140 494 h-40", "#fff", 4, .7), big_leaf(-10, 560, -30, 1.2)])

# 06 the Great Snake gives them the nut
svg(6, "Don't open it!", "Paper-cut scene: the Great Snake rises up out of the river beside the canoe, with his long teal-green neck, his kind face and a little forked tongue. On the water between them floats the dark tucumã nut, sealed with golden wax. The littlest helper, in teal at the front of the canoe, reaches out to take it, while the other two helpers watch.", DAY, [
    sun(100, 80, 44), *river_day(small_palm=False),
    crew(215, ["rest", "rest", "reach"], ["smile", "listen", "oh"], (True, False, False)), canoe(215, GUN, 180),
    nut(462, WATER + 4), snake_rising(560, WATER + 30, .95, flip=True), front_water(GUN + 30)])

# 07 on the way home: sounds inside the nut
SOUNDS = [(230, 214, "tin-tin-tin…", 30), (400, 176, "chirr-chirr…", 30), (580, 214, "croak!", 36)]
svg(7, "Tin-tin-tin, chirr-chirr, croak!", "Paper-cut scene: paddling home along the river, the middle helper in yellow holds the sealed tucumã nut in her lap. Little sound-curls float out of it with the words tin-tin-tin, chirr-chirr and croak. The oldest helper in red and the littlest in teal stop paddling to listen, each with a hand cupped to one ear.", DAY, [
    sun(690, 80, 40), *river_day(),
    crew(CX, ["ear", "hold", "ear"], ["listen", "oh", "listen"], (False, False, False)), canoe(CX, GUN), nut(*HELD),
    sound(HELD[0], HELD[1] + 10, SOUNDS), front_water(GUN + 30)])

# 08 the littlest wants a peek; the oldest says no
svg(8, "Just a little peek?", "Paper-cut scene: in the canoe, the littlest helper in teal leans towards the sealed nut in the middle helper's lap with eager hands, while the oldest helper in red holds up one hand and frowns: no! The nut is still singing tin-tin and croak.", DAY, [
    sun(690, 80, 40), *river_day(),
    crew(CX, ["stop", "hold", "reach"], ["no", "listen", "smile"], (False, False, False)), canoe(CX, GUN), nut(*HELD),
    sound(HELD[0], HELD[1] + 10, [(300, 214, "tin-tin…", 28), (520, 210, "croak!", 32)], .9), front_water(GUN + 30)])

# 09 on the bank by a tiny fire, they soften the wax
FIRE = (f'<g filter="url(#p)"><path d="M370 500 l60 -10 M372 488 l58 12" stroke="{WOOD_D}" stroke-width="10" stroke-linecap="round"/>'
        '<path d="M400 494 Q376 470 392 446 Q394 466 404 456 Q402 436 418 424 Q414 450 426 470 Q424 492 400 494Z" fill="#F6922E"/>'
        '<path d="M402 490 Q390 476 398 462 Q404 474 410 466 Q418 480 402 490Z" fill="#FFD23F"/></g>')
SAND = f'<path filter="url(#p)" d="M0 370 Q400 340 800 380 V600 H0Z" fill="#E6CF96"/>'
BEACHED = canoe(650, 352, 100)
svg(9, "Melting the wax", "Paper-cut scene: far from home, the empty canoe is pulled up on a sandy bank. The three helpers sit cross-legged on the sand around a tiny campfire: the oldest in red and the middle one in yellow warm their hands, and the littlest in teal sits at the end. The sealed tucumã nut sits by the fire, and its golden wax is starting to drip. The sun is lower now over the river.", DAY, [
    sun(660, 150, 40), canopy(260, (G1, G2)), palm(90, 300, .9, lean=-20), river(330), BEACHED, SAND,
    sitter(190, 530, 1.1, CREW[0][1], "warm", "smile", legs=True), FIRE, nut(480, 482),
    sitter(600, 530, 1.0, CREW[1][1], "warm", "oh", flip=True, legs=True),
    sitter(720, 540, .85, CREW[2][1], "rest", "smile", flip=True, legs=True)])

# 10 POP! out spills the night
SWIRL = (f'<path d="M460 470 Q400 380 320 300 Q160 220 -40 260 L-40 -40 L840 -40 L840 180 Q660 140 580 260 Q520 350 500 460Z" fill="{DUSK_IN}" opacity=".93"/>'
         + stroke("M482 460 Q470 360 430 300 Q340 200 160 180", "#3A4A8A", 18, .7))
svg(10, "Out spilled the night!", "Paper-cut scene: the tucumã nut has popped open by the fire, and a great dark-blue swirl of night pours out of it and spreads across the sky, full of twinkling stars and glowing yellow fireflies. Low down on the right the sky is still pale. The three helpers, still sitting on the sand, throw their arms in the air, open-mouthed with surprise.", DAY, [
    canopy(260, (G1, G2)), river(330), BEACHED, SAND,
    SWIRL, stars([(80, 60, 9), (200, 120, 7), (330, 70, 10), (460, 40, 7), (560, 110, 6), (120, 200, 6), (260, 230, 8), (700, 70, 8), (380, 200, 6)]),
    fireflies([(160, 290), (300, 250), (420, 330), (640, 210), (90, 340)]),
    sitter(170, 540, 1.1, CREW[0][1], "up", "oh", legs=True), nut(480, 500, state="open"),
    sitter(620, 540, 1.0, CREW[1][1], "up", "oh", legs=True), sitter(730, 550, .85, CREW[2][1], "up", "oh", legs=True),
    stroke("M90 400 l-14 -10 M250 400 l14 -10 M560 410 l-12 -10 M680 410 l12 -10", "#fff", 3, .8)])

# 11 the first night: gentle, with frogs, fireflies and stars; the daughter smiles
svg(11, "Night at last", "Paper-cut scene: the first night lies softly over the forest. Stars twinkle in a deep blue sky, yellow fireflies glow, and two little green frogs sing on lily pads in the dark river, their throats puffed up. On the bank, the daughter of the Great Snake stands beside the glowing doorway of the thatched house, smiling.", NIGHT, [
    stars([(80, 60, 8), (190, 120, 6), (300, 50, 9), (420, 100, 6), (540, 40, 8), (660, 90, 7), (740, 50, 6), (360, 170, 5), (620, 180, 5), (120, 190, 5)]),
    canopy(300, (N1, N2)), f'<path filter="url(#p)" d="M0 352 Q300 320 800 350 V430 H0Z" fill="{N3}"/>',
    hut(580, 420, 1.0, night=True, lit=True), stander(390, 426, .95, "daughter", "rest", "smile"),
    river(430, True), fireflies([(100, 300), (230, 360), (300, 270), (720, 290), (760, 380), (180, 240)]),
    frog(170, 520, 1, True), frog(620, 540, .9, True)])

# 12 dawn: the daughter makes the cujubim and the inambu
svg(12, "The morning birds", "Paper-cut scene: at dawn the sky glows pink and orange, with one bright morning star still shining. On the riverbank the daughter of the Great Snake holds up a ball of string. On a branch to the right, a glossy black cujubim bird with a white crested head, a red throat and red legs sings to the morning, and on the grass below sits a round, soft grey-brown inambu bird.", DAWN, [
    star(640, 110, 14, "#FFFFFF"), '<circle cx="640" cy="110" r="26" fill="#fff" opacity=".25"/>',
    canopy(360, ("#3E5A5A", "#4A6E60")), f'<path filter="url(#p)" d="M0 420 Q400 390 800 420 V600 H0Z" fill="{G2}"/>',
    stander(240, 550, 1.1, "daughter", "hold", "smile"), string_ball(240, 457),
    branch(800, 300, 560, 330), cujubim(630, 276, 1.1, True), inambu(480, 520, 1.1),
    big_leaf(-10, 600, -20, 1.1, G1)])

# 13 every night since: everyone sleeps well
svg(13, "Goodnight, night", "Paper-cut scene: a calm night in the forest with stars and a few fireflies. Two hammocks hang side by side between three posts, and in each one somebody sleeps snugly: the daughter of the Great Snake in a green hammock and her husband in a purple one. Up on a branch on the left, the toucan sleeps with his eye closed, and a little frog sits on a lily pad by the water. Soft z's float up.", NIGHT, [
    stars([(70, 60, 7), (180, 110, 5), (300, 50, 8), (430, 90, 6), (560, 40, 7), (690, 100, 5), (760, 40, 6), (380, 160, 4)]),
    canopy(300, (N1, N2)), f'<path filter="url(#p)" d="M0 360 Q400 330 800 360 V600 H0Z" fill="{N3}"/>',
    hut(690, 370, .7, night=True), branch(-10, 210, 150, 226, True), toucan(100, 186, .9, "sleep"),
    f'<path d="M560 600 Q600 520 800 530 V600Z" fill="{NRIV}"/>',
    hammock(130, 400, 400, DRESS, "sleep", True, True), hammock(400, 670, 400, HUSB, "sleep", False, True),
    zzz(210, 380), zzz(480, 380), fireflies([(60, 330), (760, 300), (300, 300)]), frog(735, 556, .8, False)])
