#!/usr/bin/env python3
"""Generates the 13 Why-the-Sun-and-the-Moon-Live-in-the-Sky flip-book SVGs from shared character parts.

Usage: python3 sunmoon_gen.py <output-dir>
Gold (GOLD / RAY) is reserved for the Sun; silver-lilac (SILVER / SHADE) for the Moon.
The water level (y of the water's surface) rises page by page: 487 → 445 → 450 (roof) → 318.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
GOLD, RAY, GOLD_IN, SUN_C = "#F6C445", "#F4A720", "#FBD764", "#8A5318"
SILVER, SHADE, MOON_C = "#F3F3FA", "#D3D5EC", "#4A4E7A"
ROBE_S, ROBE_SD = "#E0612F", "#9E3A1A"           # Sun's robe
ROBE_M, ROBE_MD, GELE = "#3E54A3", "#28356F", "#7A4FB5"  # Moon's robe, her headwrap
WALL, WALL_D, WALL_L = "#C98A4B", "#A86C36", "#E2B07A"
THATCH, THATCH_D = "#D9A441", "#B07F2B"
EARTH, EARTH_L = "#D9A86C", "#E8BF86"
SEA, SEA_L, SEA_D = "#3E9BD6", "#7FC6EC", "#2F7DB8"
SAND = "#EBCB98"
G_DARK, G_MID, G_LITE = "#3F9A56", "#5DB85C", "#7CC96B"
CORAL, TEAL, PINK, PURPLE, CRAB, WHALE = "#F28B66", "#2FB5B0", "#F2789F", "#8E6FD1", "#E5533D", "#4A6FB0"
DAY = [(0, "#7CCBE8"), (1, "#FDEBC8")]
HIGH = [(0, "#5DB4E4"), (1, "#E3F3FB")]
DUSK = [(0, "#3A3F86"), (.5, "#B98AB8"), (1, "#FBD9A8")]
NIGHT = [(0, "#1D2457"), (1, "#4A4F94")]


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def eyes(R: float, col: str, mood: str) -> str:
    if mood == "sleep":
        return "".join(stroke(f"M{sx * .32 * R - .12 * R:.1f} {-.1 * R:.1f} q{.12 * R:.1f} {.1 * R:.1f} {.24 * R:.1f} 0", col, max(2.4, R * .06))
                       for sx in (-1, 1))
    return "".join(f'<circle cx="{sx * .32 * R:.1f}" cy="{-.14 * R:.1f}" r="{.1 * R:.1f}" fill="#fff"/>'
                   f'<circle cx="{sx * .32 * R:.1f}" cy="{-.11 * R:.1f}" r="{.055 * R:.1f}" fill="{col}"/>' for sx in (-1, 1))


def mouth(R: float, col: str, mood: str) -> str:
    if mood == "big":
        return f'<path d="M{-.36 * R:.1f} {.16 * R:.1f} Q0 {.7 * R:.1f} {.36 * R:.1f} {.16 * R:.1f}Z" fill="{col}"/>'
    if mood == "oh":
        return f'<ellipse cy="{.3 * R:.1f}" rx="{.12 * R:.1f}" ry="{.16 * R:.1f}" fill="{col}"/>'
    return stroke(f"M{-.26 * R:.1f} {.22 * R:.1f} Q0 {.48 * R:.1f} {.26 * R:.1f} {.22 * R:.1f}", col, max(2.4, R * .06))


def cheeks(R: float) -> str:
    return "".join(f'<circle cx="{sx * .56 * R:.1f}" cy="{.14 * R:.1f}" r="{.11 * R:.1f}" fill="#F0705F" opacity=".5"/>' for sx in (-1, 1))


def sun_face(x: float, y: float, R: float, mood: str = "smile", halo: bool = True) -> str:
    """The Sun: a round gold face with twelve rays. The only gold thing in the book."""
    rays = "".join(f'<path d="M{-.14 * R:.1f} {-1.08 * R:.1f} L0 {-1.45 * R:.1f} L{.14 * R:.1f} {-1.08 * R:.1f}Z" transform="rotate({30 * i})"/>'
                   for i in range(12))
    h = f'<circle r="{1.8 * R:.1f}" fill="{GOLD}" opacity=".22"/>' if halo else ""
    return (f'<g transform="translate({x} {y})">{h}<g fill="{RAY}">{rays}</g><circle r="{R}" fill="{GOLD}"/>'
            f'<circle r="{.86 * R:.1f}" fill="{GOLD_IN}"/>{eyes(R, SUN_C, mood)}{cheeks(R)}{mouth(R, SUN_C, mood)}</g>')


def moon_face(x: float, y: float, R: float, mood: str = "smile", halo: bool = False, wave: bool = False) -> str:
    """The Moon: a pale silver face with a lilac crescent shadow, wearing her purple gele (headwrap)."""
    h = f'<circle r="{1.7 * R:.1f}" fill="{SILVER}" opacity=".16"/><circle r="{1.3 * R:.1f}" fill="{SILVER}" opacity=".18"/>' if halo else ""
    gele = (f'<path d="M{-1.04 * R:.1f} {-.3 * R:.1f} Q{-1.12 * R:.1f} {-1.16 * R:.1f} 0 {-1.2 * R:.1f} '
            f'Q{1.12 * R:.1f} {-1.16 * R:.1f} {1.04 * R:.1f} {-.3 * R:.1f} Q0 {-.66 * R:.1f} {-1.04 * R:.1f} {-.3 * R:.1f}Z" fill="{GELE}"/>'
            f'<path d="M0 {-1.1 * R:.1f} Q{-.7 * R:.1f} {-1.7 * R:.1f} {-.2 * R:.1f} {-1.62 * R:.1f} Z M0 {-1.1 * R:.1f} Q{.7 * R:.1f} {-1.75 * R:.1f} {.24 * R:.1f} {-1.66 * R:.1f}Z" fill="#9B6FD0"/>'
            + stroke(f"M{-.8 * R:.1f} {-.62 * R:.1f} Q0 {-.9 * R:.1f} {.8 * R:.1f} {-.62 * R:.1f}", "#B79BE3", max(2, R * .05)))
    hand = ""
    if wave:
        hand = (stroke(f"M{.9 * R:.1f} {.5 * R:.1f} Q{1.35 * R:.1f} {.4 * R:.1f} {1.45 * R:.1f} {-.2 * R:.1f}", ROBE_M, R * .2)
                + f'<circle cx="{1.47 * R:.1f}" cy="{-.3 * R:.1f}" r="{.17 * R:.1f}" fill="{SILVER}"/>')
    return (f'<g transform="translate({x} {y})">{h}{hand}<circle r="{R}" fill="{SHADE}"/><circle cx="{-.13 * R:.1f}" cy="{-.04 * R:.1f}" r="{.88 * R:.1f}" fill="{SILVER}"/>'
            f'{gele}{eyes(R, MOON_C, mood)}{cheeks(R)}{mouth(R, MOON_C, mood)}</g>')


ARM = {"down": (28, -36), "wave": (40, -128), "up": (50, -126), "carry": (38, -152), "reach": (56, -66),
       "hold": (48, -52), "open": (48, -78)}


def person(x: float, y: float, s: float, who: str, arms: tuple = ("down", "down"), mood: str = "smile",
           legs: str = "stand", flip: bool = False) -> str:
    """Sun (orange robe, gold trim) or Moon (indigo robe with white dots, gele). (x, y) is the feet; for 'sit', the seat."""
    sun = who == "sun"
    robe, dark, hand = (ROBE_S, ROBE_SD, GOLD) if sun else (ROBE_M, ROBE_MD, SILVER)
    trim = GOLD if sun else "#DCDDF0"
    if legs == "sit":
        y += 16 * s
        lg = stroke("M-11 -22 Q-16 -6 -26 2 M11 -22 Q8 -4 -2 4", dark, 9)
    else:
        lg = stroke("M-10 -22 L-12 -2 M10 -22 L12 -2", dark, 9) + f'<ellipse cx="-15" cy="0" rx="9" ry="4.5" fill="{dark}"/><ellipse cx="15" cy="0" rx="9" ry="4.5" fill="{dark}"/>'
    body = f'<path d="M-32 -18 Q-34 -58 -16 -84 H16 Q34 -58 32 -18 Q0 -10 -32 -18Z" fill="{robe}"/>' + stroke("M-30 -24 Q0 -16 30 -24", trim, 5)
    body += stroke("M-9 -82 L0 -70 L9 -82", trim, 4)
    if not sun:
        body += "".join(f'<circle cx="{a}" cy="{b}" r="2.6" fill="#fff" opacity=".85"/>'
                        for a, b in [(-18, -36), (-6, -48), (8, -36), (20, -50), (-14, -62), (12, -64), (0, -30), (22, -32)])
    arm = ""
    for side, key in ((-1, arms[0]), (1, arms[1])):
        ex, ey = ARM[key]
        ex *= side
        arm += stroke(f"M{17 * side} -74 L{ex} {ey}", robe, 11) + f'<circle cx="{ex}" cy="{ey}" r="7.5" fill="{hand}"/>'
    head = sun_face(0, -112, 30, mood, False) if sun else moon_face(0, -112, 30, mood)
    return group(x, y, s, flip, 0, lg + body + arm + head)


def water_char(x: float, y: float, s: float = 1, mood: str = "happy", flip: bool = False) -> str:
    """Friend Water: a big curling wave with a friendly face. (x, y) is where he meets the sea."""
    shape = (f'<path d="M-92 0 Q-100 -72 -46 -104 Q6 -132 52 -102 Q86 -78 64 -56 Q50 -70 34 -60 Q70 -34 92 0Z" fill="{SEA}"/>'
             f'<path d="M-70 0 Q-74 -54 -36 -80 Q-16 -92 4 -92 Q-48 -66 -48 0Z" fill="{SEA_L}" opacity=".7"/>'
             + stroke("M-30 -104 Q12 -124 50 -100", "#fff", 6) + '<circle cx="62" cy="-62" r="7" fill="#fff"/>')
    if mood == "shake":
        face = (stroke("M-30 -64 q8 -6 16 0 M2 -64 q8 -6 16 0", "#1F5F9A", 3.4) + stroke("M-20 -42 q10 10 20 0", "#1F5F9A", 3.4)
                + stroke("M-108 -70 q-10 18 0 34 M100 -100 q12 16 4 34", "#fff", 4))
    elif mood == "sleep":
        face = stroke("M-30 -60 q8 7 16 0 M2 -60 q8 7 16 0", "#1F5F9A", 3.4) + stroke("M-16 -38 q6 4 12 0", "#1F5F9A", 3)
    else:
        face = "".join(f'<circle cx="{c}" cy="-62" r="9" fill="#fff"/><circle cx="{c + 1.5}" cy="-61" r="4.2" fill="{INK}"/>' for c in (-22, 10))
        face += '<path d="M-24 -42 Q-6 -20 12 -42Z" fill="#1F5F9A"/>'
    face += '<circle cx="-40" cy="-44" r="7" fill="#F2A9B0" opacity=".6"/><circle cx="26" cy="-44" r="7" fill="#F2A9B0" opacity=".6"/>'
    return group(x, y, s, flip, 0, shape + face)


def sea(level: float, amp: float = 9) -> str:
    """Water filling the picture up to y = level, with a lighter top band and foam."""
    def wave(y: float) -> str:
        segs = "".join(f" T{x} {y}" for x in range(100, 801, 100))
        return f"M0 {y} Q50 {y - amp} 100 {y}{segs} V600 H0Z"
    foam = " ".join(f"M{x} {level + 26} h{w}" for x, w in [(40, 30), (190, 22), (330, 36), (520, 24), (660, 32)])
    return (f'<path filter="url(#p)" d="{wave(level)}" fill="{SEA}"/><path d="{wave(level + 16)}" fill="{SEA_D}" opacity=".35"/>'
            + stroke(f"M0 {level - 2} Q50 {level - amp - 2} 100 {level - 2}" + "".join(f" T{x} {level - 2}" for x in range(200, 801, 100)), SEA_L, 4)
            + f'<g opacity=".7">{stroke(foam, "#fff", 4)}</g>')


def fish(x: float, y: float, s: float = 1, col: str = CORAL, flip: bool = False, rot: float = 0, sleep: bool = False) -> str:
    eye = (stroke("M14 -4 q4 4 8 0", INK, 2.4) if sleep else '<circle cx="18" cy="-4" r="5" fill="#fff"/><circle cx="19" cy="-4" r="2.6" fill="#2B2320"/>')
    inner = (f'<path d="M-22 0 L-44 -18 L-40 0 L-44 18Z" fill="{col}"/><ellipse rx="30" ry="18" fill="{col}"/>'
             + stroke("M-6 -14 Q2 0 -6 14", "#fff", 3) + eye + stroke("M28 6 q-4 3 -8 1", INK, 2.2))
    return group(x, y, s, flip, rot, inner)


def crab(x: float, y: float, s: float = 1, rot: float = 0) -> str:
    legs = stroke("M-20 6 l-16 12 M-14 10 l-10 16 M20 6 l16 12 M14 10 l10 16", CRAB, 5)
    claws = (stroke("M-24 -6 Q-40 -18 -40 -32 M24 -6 Q40 -18 40 -32", CRAB, 6)
             + f'<path d="M-40 -32 l-10 -14 l8 2 l2 -10 l8 14z M40 -32 l10 -14 l-8 2 l-2 -10 l-8 14z" fill="{CRAB}"/>')
    inner = (legs + claws + f'<ellipse rx="28" ry="18" fill="{CRAB}"/>' + stroke("M-8 -14 V-28 M8 -14 V-28", CRAB, 4)
             + '<circle cx="-8" cy="-30" r="6" fill="#fff"/><circle cx="8" cy="-30" r="6" fill="#fff"/><circle cx="-7" cy="-30" r="3" fill="#2B2320"/>'
             '<circle cx="9" cy="-30" r="3" fill="#2B2320"/>' + stroke("M-8 0 Q0 7 8 0", INK, 2.6))
    return group(x, y, s, False, rot, inner)


def turtle(x: float, y: float, s: float = 1, flip: bool = False) -> str:
    inner = ('<g fill="#7CC96B"><ellipse cx="-26" cy="12" rx="12" ry="7"/><ellipse cx="22" cy="14" rx="12" ry="7"/><circle cx="40" cy="-4" r="13"/></g>'
             f'<path d="M-36 6 Q-34 -32 0 -32 Q34 -32 36 6Z" fill="{G_DARK}"/>'
             + stroke("M-20 4 Q-18 -20 0 -24 Q18 -20 20 4 M0 -24 V6", "#2C7A44", 3)
             + '<circle cx="44" cy="-7" r="4" fill="#fff"/><circle cx="45" cy="-7" r="2" fill="#2B2320"/>' + stroke("M40 2 q4 3 8 0", INK, 2.2))
    return group(x, y, s, flip, 0, inner)


def octopus(x: float, y: float, s: float = 1, wave: bool = True) -> str:
    """Head at (x, y); four curly arms below, one waving."""
    arms = stroke("M-26 20 q-26 20 -14 44 q6 8 14 0 M-10 26 q-10 26 4 40 M10 26 q10 26 -4 40 M26 20 q26 20 14 44 q-6 8 -14 0", PURPLE, 10)
    up = stroke("M34 0 q30 -10 30 -42 q0 -12 -10 -10", PURPLE, 10) if wave else ""
    inner = (arms + up + f'<ellipse cy="-6" rx="38" ry="34" fill="{PURPLE}"/><ellipse cx="-12" cy="-24" rx="10" ry="6" fill="#B49BE6"/>'
             '<circle cx="-12" cy="0" r="8" fill="#fff"/><circle cx="12" cy="0" r="8" fill="#fff"/><circle cx="-11" cy="1" r="4" fill="#2B2320"/>'
             '<circle cx="13" cy="1" r="4" fill="#2B2320"/>' + stroke("M-8 14 Q0 20 8 14", INK, 2.6)
             + '<circle cx="-26" cy="12" r="5" fill="#F2A9B0" opacity=".7"/><circle cx="26" cy="12" r="5" fill="#F2A9B0" opacity=".7"/>')
    return group(x, y, s, False, 0, inner)


def whale(x: float, y: float, s: float = 1, flip: bool = False, spout: bool = True, sleep: bool = False) -> str:
    """A big blue whale floating at the surface. (x, y) is the water line through her middle."""
    sp = (stroke("M30 -50 V-82 M30 -76 q-22 -26 -40 -10 M30 -76 q22 -26 40 -10", SEA_L, 7) if spout else "")
    eye = stroke("M50 -6 q5 5 10 0", INK, 3) if sleep else '<circle cx="54" cy="-8" r="6" fill="#fff"/><circle cx="55" cy="-8" r="3" fill="#2B2320"/>'
    inner = (sp + f'<path d="M-90 -6 Q-120 -40 -138 -50 Q-128 -20 -112 -10 Q-130 -4 -142 14 Q-116 12 -90 6Z" fill="{WHALE}"/>'
             f'<path d="M-96 0 Q-90 -52 0 -54 Q90 -54 96 0 Q90 30 0 32 Q-90 30 -96 0Z" fill="{WHALE}"/>'
             '<path d="M-70 10 Q0 30 92 6 Q84 28 0 30 Q-60 28 -70 10Z" fill="#CFE3F5"/>' + eye
             + stroke("M66 12 q14 4 26 -6", INK, 3) + '<circle cx="62" cy="6" r="6" fill="#F2A9B0" opacity=".6"/>')
    return group(x, y, s, flip, 0, inner)


def starfish(x: float, y: float, s: float = 1, rot: float = 0) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)"><polygon points="0,-20 6,-6 20,-6 9,3 13,18 0,9 -13,18 -9,3 -20,-6 -6,-6" fill="{PINK}"/>'
            '<circle cx="-3" cy="-1" r="1.8" fill="#2B2320"/><circle cx="3" cy="-1" r="1.8" fill="#2B2320"/></g>')


def roundhouse(x: float, y: float, s: float = 1, roof_only: bool = False) -> str:
    """A round mud-walled house with white zigzags and a tall thatched cone roof. (x, y) is the base."""
    wall = (f'<path d="M-60 0 V-70 Q0 -80 60 -70 V0 Q0 10 -60 0Z" fill="{WALL}"/><path d="M30 -73 Q50 -72 60 -70 V0 Q46 4 30 6Z" fill="{WALL_D}" opacity=".5"/>'
            + stroke("M-56 -40 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10", CREAM, 3.4)
            + '<path d="M-16 4 V-30 Q0 -46 16 -30 V4 Q0 6 -16 4Z" fill="#5A3520"/>')
    roof = (f'<path d="M-80 -64 Q0 -54 80 -64 L7 -170 Q0 -177 -7 -170Z" fill="{THATCH}"/>'
            + stroke("M-60 -64 L-6 -164 M-34 -60 L-3 -166 M-8 -58 L0 -168 M18 -58 L3 -166 M44 -60 L6 -164 M66 -63 L8 -160", THATCH_D, 2.4)
            + stroke("M-78 -64 Q0 -52 78 -64", THATCH_D, 6) + f'<path d="M-9 -168 L0 -190 L9 -168Z" fill="{THATCH_D}"/>')
    return group(x, y, s, False, 0, roof if roof_only else wall + roof)


def compound_wall(top: float, bottom: float, gate: tuple = None) -> str:
    """The long round outer wall seen from inside the courtyard, with an optional open gate (x1, x2)."""
    d = f"M0 {top} Q400 {top - 26} 800 {top} V{bottom} H0Z"
    out = (f'<path filter="url(#p)" d="{d}" fill="{WALL}"/>' + stroke(f"M0 {top} Q400 {top - 26} 800 {top}", WALL_D, 10)
           + stroke(" ".join(f"M{x} {top + 34} l14 -14 l14 14" for x in range(10, 800, 28)), CREAM, 3.4))
    if gate:
        a, b = gate
        out += f'<path d="M{a} {bottom} V{top + 10} Q{(a + b) / 2} {top - 40} {b} {top + 10} V{bottom}Z" fill="#8FC9E6"/>'
        out += stroke(f"M{a} {bottom} V{top + 10} Q{(a + b) / 2} {top - 40} {b} {top + 10} V{bottom}", WALL_D, 9)
    return out


def cloud(x: float, y: float, s: float = 1, fill: str = "#fff", op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def palm(x: float, y: float, s: float = 1, flip: bool = False) -> str:
    return f'<use href="#pm" transform="translate({x} {y}) scale({-s if flip else s} {s})"/>'


def spark(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#k" transform="translate({x} {y}) scale({s})"/>'


def star(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def hill(y: float, amp: float, fill: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def drops(pts: list, fill: str = SEA_L) -> str:
    return f'<g fill="{fill}">' + "".join(f'<path d="M{a} {b} q7 12 0 17 q-7 -5 0 -17z"/>' for a, b in pts) + '</g>'


GROUND = f'<path filter="url(#p)" d="M0 470 Q400 446 800 470 V600 H0Z" fill="{EARTH}"/>'
YARD = f'<path filter="url(#p)" d="M0 462 Q400 448 800 462 V600 H0Z" fill="{EARTH}"/>'
FRONT = f'<path d="M0 600 V574 Q400 546 800 580 V600Z" fill="{G_DARK}"/>'
DEFS = {
    "pm": ('<g id="pm" filter="url(#p)"><path d="M0 0 Q-16 -80 6 -160" stroke="#A9764A" stroke-width="15" fill="none" stroke-linecap="round"/>'
           '<g transform="translate(6 -162)"><g id="pf"><path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#2F8F4E" transform="rotate(-52)"/>'
           '<path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#5DB85C" transform="rotate(-12)"/><path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#2F8F4E" transform="rotate(28)"/></g>'
           '<use href="#pf" transform="scale(-1 1)"/><circle cx="-5" cy="6" r="7" fill="#C2552E"/><circle cx="7" cy="9" r="7" fill="#D9663A"/></g></g>'),
    "k": '<path id="k" d="M0 -10 Q1 -1 10 0 Q1 1 0 10 Q-1 1 -10 0 Q-1 -1 0 -10Z" fill="#fff"/>',
    "s": '<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="#F3F3FA"/>',
}


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    defs = "".join(d for k, d in DEFS.items() if f'href="#{k}"' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/sunmoon-{n:02d}.svg", "w") as fh:
        fh.write(doc)


FAR = hill(400, 24, "#A9DB8E", False)

# 01 cover — Sun and Moon in the evening sky above the sea that covers their compound
svg(1, "Why the Sun and the Moon Live in the Sky", "Paper-cut cover: in an evening sky that fades from deep purple-blue at the top to pink and peach at the bottom, the smiling golden Sun and the silver Moon in her purple headwrap shine side by side. Below, the top of a round thatched roof pokes up out of the sea, and a whale, an octopus and leaping fish play in the water beside friendly Water, a big smiling wave.", DUSK, [
    star(560, 50, 1.3), star(700, 90, 1), star(480, 110, .8), star(760, 40, .9), star(620, 150, .7),
    sun_face(230, 180, 78, "big"), moon_face(560, 200, 62, "smile", True),
    cloud(380, 300, 1.1, "#FFE1D2", .8),
    roundhouse(420, 560, 1.6, True), water_char(130, 420, 1.15), sea(396),
    whale(600, 452, .95), octopus(400, 470, .8),
    fish(250, 520, .9, CORAL), fish(520, 548, .8, TEAL, True), fish(720, 530, .8, PINK, True),
    drops([(300, 380), (330, 360), (680, 380)], "#fff")])

# 02 Sun and Moon on the earth, at their little round house
svg(2, "Sun and Moon live on the earth", "Paper-cut scene: long ago, the Sun — a round golden face with rays, in an orange robe — waves beside his wife the Moon — a silver face in a purple headwrap and an indigo dotted robe. They stand on red-brown earth next to their little round mud house with a thatched roof, under palm trees.", DAY, [
    cloud(150, 100, 1.2), cloud(620, 80, 1), FAR, palm(720, 440, 1.2, True), palm(70, 450, 1),
    GROUND, roundhouse(570, 492, 1.1),
    person(270, 500, 1.5, "sun", ("down", "wave"), "big"), person(400, 500, 1.5, "moon", ("down", "down")),
    FRONT])

# 03 Sun visits his friend Water
svg(3, "Sun visits his friend Water", "Paper-cut scene: the Sun walks along a sandy beach to visit his friend Water, a big smiling blue wave rising out of the sea; two little fish peek up from the water to say hello.", DAY, [
    cloud(200, 90, 1.1), cloud(650, 120, .9), hill(380, 10, "#A9DB8E", False),
    f'<path filter="url(#p)" d="M0 470 Q260 440 420 440 H800 V600 H0Z" fill="{SAND}"/>',
    water_char(640, 470, 1.55),
    f'<path filter="url(#p)" d="M420 440 Q600 432 800 440 V600 H540 Q480 500 420 440Z" fill="{SEA}"/>',
    stroke("M430 446 Q600 432 800 446", SEA_L, 4), fish(500, 520, .7, CORAL, True, -10), fish(740, 540, .7, TEAL, True, 10),
    person(250, 515, 1.45, "sun", ("down", "wave"), "big"),
    starfish(110, 560, 1.3, 20), marks(["M560 270 l-6 -20", "M600 256 v-22", "M640 262 l8 -20"])])

# 04 "Your house isn't big enough for my people"
svg(4, "Water's many people", "Paper-cut scene: the Sun stands on the beach with his arms open, asking Water to visit. Water, the big blue wave, smiles and kindly shakes his head, while all his people peek out of the sea around him: three fish, an octopus, a crab on a rock, a turtle, and a whale's tail sticking up out of the sea. The Sun's little round house looks tiny on the hill behind.", DAY, [
    cloud(160, 90, 1), cloud(560, 70, 1.1), hill(380, 10, "#A9DB8E", False), roundhouse(110, 384, .42),
    f'<path filter="url(#p)" d="M0 470 Q200 446 330 430 H800 V600 H0Z" fill="{SAND}"/>',
    water_char(570, 470, 1.4, "shake"),
    f'<path filter="url(#p)" d="M330 430 Q560 420 800 430 V600 H440 Q390 500 330 430Z" fill="{SEA}"/>',
    stroke("M340 436 Q560 420 800 436", SEA_L, 4),
    f'<path d="M705 468 Q722 420 750 440 Q760 402 790 410 Q772 456 762 474Z" fill="{WHALE}" filter="url(#p)"/>',
    octopus(430, 470, .7), turtle(720, 500, .8, True),
    f'<ellipse cx="690" cy="580" rx="70" ry="26" fill="#9A9288" filter="url(#p)"/>', crab(690, 548, .8),
    fish(470, 555, .7, CORAL, True), fish(560, 575, .7, TEAL), fish(530, 505, .6, PINK, True),
    person(190, 520, 1.4, "sun", ("open", "open"), "smile")])

# 05 Building the big compound
bricks = ''.join(f'<rect x="{x}" y="{y}" width="34" height="18" rx="4" fill="{WALL}" stroke="{WALL_D}" stroke-width="2"/>'
                 for x, y in [(80, 520), (116, 520), (98, 502), (152, 520)])
half = (f'<g filter="url(#p)"><path d="M380 492 V420 Q470 404 560 420 V492 Q470 502 380 492Z" fill="{WALL}"/></g>'
        + stroke("M384 460 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10 l10 10 l10 -10", CREAM, 3.4)
        + stroke("M380 420 Q470 404 560 420", WALL_D, 6))
thatch = (f'<g filter="url(#p)"><path d="M-46 0 Q0 -16 46 0 Q48 14 40 18 Q0 8 -40 18 Q-48 14 -46 0Z" fill="{THATCH}"/></g>'
          + stroke("M-40 6 L-34 -8 M-20 6 L-18 -10 M0 6 V-10 M20 6 L18 -10 M40 6 L34 -8", THATCH_D, 2.4))
svg(5, "Building a big compound", "Paper-cut scene: the Sun pats wet red mud onto a new round wall, beside a pile of mud bricks, while the Moon walks up with a bundle of golden thatch balanced on her head, steadying it with one hand.", DAY, [
    cloud(200, 100, 1.1), cloud(640, 70, .9), FAR, palm(730, 440, 1.1, True), GROUND, bricks, half,
    person(300, 520, 1.45, "sun", ("reach", "reach"), "smile"),
    person(640, 520, 1.45, "moon", ("down", "carry"), "smile"),
    f'<g transform="translate(640 278) scale(1.2)">{thatch}</g>',
    drops([(560, 380), (580, 404)], WALL), marks(["M470 380 l-4 -18", "M500 376 v-20", "M530 380 l4 -18"]), FRONT])

# 06 The big compound is ready
svg(6, "The big compound is ready", "Paper-cut scene: a huge new compound with a long round mud wall decorated with white zigzags, a wide open gate, and the thatched cone roofs of four round houses rising behind it. The Sun and the Moon stand in front of the gate, waving to invite their friend Water.", DAY, [
    cloud(140, 80, 1), cloud(660, 90, 1.2), FAR, palm(40, 430, 1.1),
    roundhouse(170, 360, .9), roundhouse(320, 340, 1.05), roundhouse(500, 340, 1.05), roundhouse(650, 360, .9),
    f'<path filter="url(#p)" d="M70 460 V352 Q400 316 730 352 V460 Q400 490 70 460Z" fill="{WALL}"/>',
    stroke("M70 352 Q400 316 730 352", WALL_D, 10),
    stroke(" ".join(f"M{x} {392 - 34 * (1 - ((x - 400) / 330) ** 2):.0f} l14 -14 l14 14" for x in range(80, 720, 28)), CREAM, 3.4),
    '<path d="M350 476 V400 Q400 360 450 400 V476Z" fill="#5A3520"/>', stroke("M350 476 V400 Q400 360 450 400 V476", WALL_D, 8),
    f'<path filter="url(#p)" d="M0 470 Q400 470 800 470 V600 H0Z" fill="{EARTH}"/>',
    person(300, 560, 1.25, "sun", ("down", "wave"), "big"), person(500, 560, 1.25, "moon", ("wave", "down"), "big"),
    FRONT])

LEVEL_KNEE, LEVEL_TUMMY = 487, 445
YARD_BACK = [compound_wall(318, 470, (600, 720)), roundhouse(110, 470, 1.0), YARD]

# 07 "Can my people come in?" — water to their knees, three fish
svg(7, "Water comes in, up to their knees", "Paper-cut scene: inside the compound, Water, the big blue wave, pours in through the open gate. The water is up to the knees of the Sun and the Moon, who stand in the courtyard smiling, and three fish — orange, teal and pink — swim around their feet.", DAY, [
    cloud(200, 90, 1), cloud(560, 70, .9), *YARD_BACK,
    person(300, 520, 1.5, "sun", ("down", "open"), "big"), person(440, 520, 1.5, "moon", ("down", "down"), "smile"),
    water_char(660, LEVEL_KNEE + 4, 1.05), sea(LEVEL_KNEE),
    fish(150, 540, .8, CORAL), fish(380, 565, .8, TEAL, True), fish(560, 530, .8, PINK, True)])

# 08 more people — water to their tummies, crabs and a turtle
svg(8, "Up to their tummies", "Paper-cut scene: more of Water's people have come in, and the water in the courtyard is up to the tummies of the Sun and the Moon; the Sun throws up his arms and the Moon holds hers out wide, and both laugh. Three red crabs, a green turtle and the three fish swim around them, and the water covers the bottom of the round house's door.", DAY, [
    cloud(200, 90, 1), cloud(560, 70, .9), *YARD_BACK,
    person(300, 520, 1.5, "sun", ("up", "up"), "big"), person(440, 520, 1.5, "moon", ("open", "open"), "big"),
    water_char(660, LEVEL_TUMMY + 4, 1.1), sea(LEVEL_TUMMY),
    crab(150, 492, .75), crab(560, 500, .75, 10), crab(380, 548, .75, -10), turtle(210, 560, .85),
    fish(90, 540, .65, CORAL), fish(660, 560, .65, TEAL, True), fish(500, 580, .65, PINK, True)])

# 09 up to the roof — Sun and Moon sit on top of the roof; an octopus waves
svg(9, "Up onto the roof", "Paper-cut scene: the whole compound is under water — the walls have disappeared below the waves, and only thatched roof tops poke out. The water is right up to the roof of the big round house, so the Sun and the Moon sit high on the roof, one on each side, smiling. Around them the octopus waves an arm, the turtle swims, a pink fish leaps, and Water, the big wave, laughs beside them.", DAY, [
    cloud(150, 80, 1), cloud(640, 110, 1.1), roundhouse(110, 520, .8, True), roundhouse(610, 510, .6, True),
    roundhouse(400, 610, 2.2),
    person(318, 428, 1.25, "sun", ("down", "wave"), "big", "sit"), person(482, 428, 1.25, "moon", ("wave", "down"), "smile", "sit", True),
    water_char(705, 462, 1.0), sea(450), octopus(150, 470, .85), turtle(600, 520, .8), fish(250, 540, .7, CORAL, True), fish(480, 560, .7, TEAL),
    fish(120, 380, .65, PINK, False, -30), drops([(160, 410), (180, 430)], SEA_L)])

# 10 the whale comes — water over the roof, Sun and Moon float up into the sky
svg(10, "Up, up into the sky", "Paper-cut scene: last of all comes the big blue whale, and the water rises over the roof until only the very tip of the thatch pokes out. Holding hands, the Sun and the Moon float gently up into the sky, while the whale sprays a fountain of water below them and Water waves goodbye.", HIGH, [
    cloud(130, 110, 1.1), cloud(680, 90, 1),
    person(330, 260, 1.1, "sun", ("up", "hold"), "big"), person(450, 250, 1.1, "moon", ("hold", "up"), "big"),
    marks(["M316 290 v40", "M346 296 v30", "M436 280 v40", "M466 286 v30"]),
    roundhouse(400, 560, 1.6, True), water_char(150, 336, .9), sea(318),
    whale(590, 360, 1.1), fish(300, 430, .7, CORAL), fish(460, 470, .7, TEAL, True), fish(700, 480, .7, PINK, True),
    spark(250, 200, 1.2), spark(540, 190, 1), spark(390, 120, 1.3)])

# 11 Sun and Moon in the sky
svg(11, "At home in the sky", "Paper-cut scene: high up in the big blue sky, the Sun and the Moon sit on two soft white clouds, waving happily. Far below, the sea sparkles, with the tip of the old roof, a whale and leaping fish.", HIGH, [
    person(270, 300, 1.25, "sun", ("down", "wave"), "big", "sit"), cloud(270, 346, 1.35, "#fff", 1),
    person(540, 270, 1.25, "moon", ("wave", "down"), "smile", "sit"), cloud(540, 316, 1.35, "#fff", 1),
    cloud(110, 120, .7), cloud(720, 150, .8),
    roundhouse(150, 497, .45, True), sea(470, 6),
    whale(600, 492, .5, True), fish(330, 520, .5, CORAL, False, -20), fish(420, 545, .5, TEAL, True), fish(250, 560, .5, PINK),
    spark(400, 180, 1.2), spark(660, 360, 1), spark(140, 260, .9)])

# 12 by day the Sun shines on everybody, and Water's people splash
svg(12, "The Sun shines on everybody", "Paper-cut scene: by day the big golden Sun beams down from the sky, and below him Water and all his people splash and play: a whale sprays a fountain, an octopus waves, a crab sits on a rock, the turtle swims and fish leap out of the sparkling sea. A pale daytime Moon smiles faintly in a corner of the sky.", DAY, [
    f'<g opacity=".55">{moon_face(110, 90, 30, "sleep")}</g>',
    f'<g fill="{GOLD}"><path d="M400 170 L60 600 H300Z" opacity=".16"/><path d="M400 170 L560 600 H800Z" opacity=".16"/></g>',
    sun_face(400, 170, 96, "big"), water_char(130, 410, 1.0), sea(390),
    whale(600, 420, 1.0, True), octopus(370, 450, .7),
    f'<ellipse cx="700" cy="560" rx="80" ry="28" fill="#9A9288" filter="url(#p)"/>', crab(700, 528, .75), turtle(230, 530, .8),
    fish(470, 360, .7, CORAL, False, -35), fish(300, 360, .65, TEAL, True, 35), fish(500, 540, .7, PINK, True),
    drops([(460, 330), (490, 320), (320, 330), (290, 316)], SEA_L), spark(560, 330, 1), spark(250, 300, 1.1)])

# 13 goodnight, Moon
moonpath = stroke("M370 430 h70 M350 470 h110 M380 510 h60 M360 550 h90", "#F3F3FA", 5)
svg(13, "Goodnight, Moon", "Paper-cut night scene: in a deep blue starry sky the silver Moon in her purple headwrap smiles down. Below, a silver path of moonlight shines across the calm sea, where Water, a whale and two fish have closed their eyes and are drifting off to sleep.", NIGHT, [
    star(80, 70, 1.4), star(200, 140, 1), star(300, 60, .8), star(640, 90, 1.2), star(720, 200, 1), star(560, 40, .9), star(110, 260, .8), star(690, 300, .7),
    moon_face(410, 190, 84, "smile", True), water_char(150, 414, .9, "sleep"), sea(400, 6), f'<g opacity=".8">{moonpath}</g>',
    whale(650, 430, .8, True, False, True),
    fish(270, 520, .6, CORAL, False, 0, True), fish(560, 540, .6, TEAL, True, 0, True),
    marks(["M200 300 h12 l-12 12 h12", "M230 270 h9 l-9 9 h9"], "#F3F3FA", 3)])
