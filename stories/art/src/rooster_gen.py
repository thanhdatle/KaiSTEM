#!/usr/bin/env python3
"""Generates the 13 Rooster-and-the-Wedding flip-book SVGs from shared character parts.

Usage: python3 rooster_gen.py <output-dir>
Gold (GOLD / RAY / the #s star) is reserved for the Sun and its warmth.
"""
import sys

OUT = sys.argv[1]
INK, CREAM, RED, BEAK, MUD = "#2B2320", "#FFF6E6", "#E0312F", "#F0962E", "#7A5234"
BODY, NECK, WING, BOW = "#C9482B", "#F2994A", "#9E3520", "#2F80D0"
GOLD, RAY, PINK = "#F6C445", "#F4A720", "#F2789F"
G_DARK, G_MID, G_LITE = "#3F9A56", "#5DB85C", "#7CC96B"
BLUE, BLUE_LITE, SAND = "#4FAEE0", "#8AD0F0", "#EBCB98"
FLAGS = ["#F2789F", "#2FB5B0", "#E5344A", "#FFF6E6", "#8E6FD1"]
DAY = [(0, "#7CCBE8"), (1, "#FDEBC8")]
DAWN = [(0, "#F7A9A0"), (1, "#FDE9C4")]
GREY = [(0, "#9DBFD3"), (1, "#EFE6D2")]
WARM = [(0, "#8ED3E6"), (1, "#FFE9B0")]
VILLAGE = [(110, 346, .9, "#F7A8B8"), (165, 340, 1.1, "#A8E6CF"), (228, 344, .9, "#C9B6E4"),
           (600, 362, 1, "#FFC9A3"), (655, 366, .85, "#8ED6D9")]


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def hibiscus(x: float, y: float, s: float = 1) -> str:
    petals = "".join(f'<circle cy="-9" r="8" transform="rotate({72 * i})"/>' for i in range(5))
    return (f'<g transform="translate({x} {y}) scale({s})"><g fill="#E5344A">{petals}</g>'
            '<circle r="4.5" fill="#B81F3A"/><circle cx="2" cy="-3" r="2" fill="#FFE3EC"/></g>')


TAIL = ('<path d="M-22 8 Q-92 10 -104 -26 Q-58 -18 -16 0Z" fill="#1E7F74"/><path d="M-20 14 Q-78 36 -100 12 Q-56 10 -16 6Z" fill="#F6A04D"/>'
        '<path d="M-22 0 Q-80 -14 -88 -58 Q-46 -40 -14 -8Z" fill="#F28C38"/><path d="M-20 -6 Q-58 -30 -52 -78 Q-22 -52 -10 -14Z" fill="#2FA36B"/>'
        + stroke("M-34 -32 Q-44 -48 -46 -62 M-48 -20 Q-66 -30 -76 -44 M-54 -4 Q-76 -8 -92 -18", CREAM, 2.2))
LEGS = {"stand": "M-8 30 V54 h11 M12 30 V54 h11", "walk": "M-8 30 L-20 54 h11 M12 30 L26 49 l10 -3",
        "sit": "M-4 32 q16 12 28 6 M10 32 q14 10 24 2"}
WINGS = {"down": "M-18 0 Q8 -8 16 10 Q0 30 -22 18Z", "up": "M4 8 Q36 4 64 -20 Q62 12 22 27Z",
         "flap": "M-6 6 Q-28 -30 -46 -36 Q-38 -4 -4 20Z"}


def rooster(x: float, y: float, s: float = 1, flip: bool = False, rot: float = 0, head: float = 0,
            look: tuple = (1.5, 0), mood: str = "happy", mud: bool = False, crow: bool = False,
            wing: str = "down", legs: str = "stand", tail: float = 0, flower: bool = False) -> str:
    """The same rooster on every page: red comb, orange-and-green tail, blue bow tie."""
    bk = MUD if mud else BEAK
    lx, ly = look
    if crow or mood == "shock":
        beak = f'<path d="M41 -44 L56 -40 L41 -35Z" fill="#B8323A"/><path d="M40 -52 L63 -55 L43 -42Z M40 -38 L58 -27 L41 -33Z" fill="{bk}"/>'
    else:
        beak = f'<path d="M41 -49 L63 -41 L41 -33Z" fill="{bk}"/>'
    if mud:
        beak += f'<g fill="{MUD}"><ellipse cx="55" cy="-41" rx="13" ry="9"/><circle cx="43" cy="-33" r="5"/><path d="M56 -35 q5 15 0 20 q-6 -5 0 -20z"/></g>'
    if mood == "joy":
        eye = stroke("M21 -45 q7 -9 14 0", INK, 3)
    else:
        r, pr = (10, 3) if mood == "shock" else (8, 3.8)
        eye = (f'<circle cx="28" cy="-47" r="{r}" fill="#fff"/><circle cx="{28 + lx}" cy="{-47 + ly}" r="{pr}" fill="{INK}"/>'
               f'<circle cx="{29.3 + lx}" cy="{-48.5 + ly}" r="1.2" fill="#fff"/>')
        if mood == "sad":
            eye += f'<path d="M17 -46 V-58 H40 V-53Z" fill="{NECK}"/>' + stroke("M18 -46 L39 -53", INK, 2.6)
    hd = (f'<g transform="rotate({head} 14 -6)"><g fill="{RED}"><circle cx="12" cy="-62" r="8"/><circle cx="24" cy="-67" r="9"/><circle cx="35" cy="-60" r="8"/>'
          f'<ellipse cx="40" cy="-22" rx="5" ry="9"/></g><path d="M-2 0 Q2 -40 10 -50 L40 -30 Q32 -6 30 6Z" fill="{NECK}"/>'
          f'<circle cx="24" cy="-42" r="20" fill="{NECK}"/>{beak}{eye}<circle cx="37" cy="-34" r="4.5" fill="#F0705F" opacity=".6"/></g>')
    bow = (hibiscus(18, -8, .62) if flower else f'<circle cx="18" cy="-6" r="5" fill="#1F5FA8"/>')
    inner = (f'<g transform="rotate({tail} -20 4)">{TAIL}</g>' + stroke(LEGS[legs], "#E07B2A", 5) + hd
             + f'<ellipse cy="8" rx="36" ry="30" fill="{BODY}"/><path d="{WINGS[wing]}" fill="{WING}"/>'
             + f'<path d="M18 -6 L2 -17 V5Z M18 -6 L34 -17 V5Z" fill="{BOW}"/>' + bow)
    return group(x, y, s, flip, rot, inner)


def grass(x: float, y: float, s: float = 1, mood: str = "away", flip: bool = False) -> str:
    """A tuft with a face. 'away' turns its face aside with closed eyes; 'kind' smiles."""
    blades = (f'<path d="M-40 0 Q-60 -50 -46 -84 Q-34 -44 -22 0Z M-8 0 Q-12 -70 6 -104 Q14 -56 14 0Z M24 0 Q44 -50 58 -72 Q50 -30 44 0Z" fill="{G_DARK}"/>'
              f'<path d="M-26 0 Q-34 -60 -20 -92 Q-10 -50 -4 0Z M10 0 Q24 -60 38 -90 Q36 -40 30 0Z" fill="{G_LITE}"/>'
              f'<path d="M-54 4 Q-54 -44 0 -44 Q54 -44 54 4Z" fill="{G_MID}"/>')
    if mood == "away":
        face = (stroke("M4 -24 q6 5 12 0 M28 -24 q6 5 12 0", INK, 3) + stroke("M18 -9 q5 -4 10 0", INK, 2.6)
                + '<circle cx="40" cy="-13" r="5" fill="#F2A9B0" opacity=".6"/>')
    else:
        face = "".join(f'<circle cx="{c}" cy="-24" r="7" fill="#fff"/><circle cx="{c + 1.5}" cy="-23" r="3.4" fill="{INK}"/>' for c in (-13, 13))
        face += stroke("M-8 -10 Q0 -2 8 -10", INK, 2.6) + '<circle cx="-24" cy="-11" r="5" fill="#F2A9B0" opacity=".7"/><circle cx="24" cy="-11" r="5" fill="#F2A9B0" opacity=".7"/>'
    return group(x, y, s, flip, 0, blades + face)


def water(x: float, y: float, s: float = 1, mood: str = "sleepy") -> str:
    """A puddle with a face: a low dome rising from a pool."""
    body = (f'<ellipse cy="6" rx="96" ry="26" fill="{BLUE}"/><ellipse cy="9" rx="70" ry="13" fill="{BLUE_LITE}"/>'
            f'<path d="M-46 6 Q-52 -54 0 -54 Q52 -54 46 6Z" fill="{BLUE}"/>' + stroke("M-32 -30 q6 -12 18 -14", "#fff", 4))
    cheeks = '<circle cx="-27" cy="-12" r="6" fill="#F2A9B0" opacity=".6"/><circle cx="27" cy="-12" r="6" fill="#F2A9B0" opacity=".6"/>'
    if mood == "sleepy":
        face = (stroke("M-22 -24 q7 6 14 0 M8 -24 q7 6 14 0", "#1F5F9A", 3) + '<ellipse cy="-6" rx="8" ry="10" fill="#1F5F9A"/>'
                + stroke("M42 -62 h10 l-10 10 h10 M62 -86 h13 l-13 13 h13", "#fff", 3))
    else:
        face = "".join(f'<circle cx="{c}" cy="-26" r="8" fill="#fff"/><circle cx="{c - 1.5}" cy="-27" r="3.8" fill="{INK}"/>' for c in (-15, 15))
        face += '<path d="M-10 -12 Q0 2 10 -12Z" fill="#1F5F9A"/>'
    return group(x, y, s, False, 0, body + face + cheeks)


def wind(x: float, y: float, s: float = 1, mood: str = "busy", flip: bool = False) -> str:
    """A swirly cloud with puffed cheeks, always blowing forwards."""
    body = ('<g fill="#E4EDFA"><circle cx="-40" cy="6" r="28"/><circle cx="-10" cy="-16" r="34"/><circle cx="30" cy="-8" r="32"/>'
            '<circle cx="56" cy="12" r="22"/><rect x="-66" y="6" width="142" height="30" rx="15"/></g>')
    trail = stroke("M-74 2 q-40 -8 -62 8 M-70 24 q-46 2 -70 22", "#C3D3EA", 7)
    swirl = stroke("M-44 2 q4 -30 30 -20 q16 10 0 24 q-14 6 -14 -8", "#A9BEDD", 4.5)
    eyes = (stroke("M14 -16 l11 4 M52 -16 l-11 4", INK, 3) if mood == "busy" else
            "".join(f'<circle cx="{c}" cy="-14" r="6.5" fill="#fff"/><circle cx="{c + 1.5}" cy="-13" r="3.2" fill="{INK}"/>' for c in (20, 46)))
    face = ('<circle cx="12" cy="8" r="11" fill="#F2A9B0"/><circle cx="56" cy="8" r="11" fill="#F2A9B0"/><circle cx="35" cy="10" r="5.5" fill="#6C7FA6"/>'
            + stroke("M84 6 h34 M82 20 q22 8 40 2 M82 -8 q22 -8 40 -2", "#fff", 4))
    return group(x, y, s, flip, 0, trail + body + swirl + eyes + face)


def sun(x: float, y: float, R: float, mood: str = "big") -> str:
    """The golden Sun: the only gold thing in the book."""
    c = "#8A5318"
    rays = "".join(f'<path d="M{-.13 * R:.0f} {-1.1 * R:.0f} L0 {-1.42 * R:.0f} L{.13 * R:.0f} {-1.1 * R:.0f}Z" transform="rotate({30 * i})"/>' for i in range(12))
    eyes = "".join(f'<circle cx="{sx * .32 * R:.0f}" cy="{-.14 * R:.0f}" r="{.1 * R:.0f}" fill="#fff"/><circle cx="{sx * .32 * R:.0f}" cy="{-.11 * R:.0f}" r="{.055 * R:.1f}" fill="{c}"/>'
                   for sx in (-1, 1))
    cheeks = "".join(f'<circle cx="{sx * .56 * R:.0f}" cy="{.14 * R:.0f}" r="{.11 * R:.0f}" fill="#F0705F" opacity=".5"/>' for sx in (-1, 1))
    mouth = (f'<path d="M{-.36 * R:.0f} {.16 * R:.0f} Q0 {.7 * R:.0f} {.36 * R:.0f} {.16 * R:.0f}Z" fill="{c}"/>' if mood == "big"
             else stroke(f"M{-.26 * R:.0f} {.22 * R:.0f} Q0 {.48 * R:.0f} {.26 * R:.0f} {.22 * R:.0f}", c, max(3, R * .045)))
    return (f'<g transform="translate({x} {y})"><circle r="{1.75 * R:.0f}" fill="{GOLD}" opacity=".25"/><g fill="{RAY}">{rays}</g>'
            f'<circle r="{R}" fill="{GOLD}" filter="url(#p)"/><circle r="{.86 * R:.0f}" fill="#FBD764"/>{eyes}{cheeks}{mouth}</g>')


def parrot(x: float, y: float, s: float = 1, flip: bool = False, role: str = "groom", wing: str = "down") -> str:
    """Uncle Perico (green, top hat) and his bride (blue, veil and flowers). Same body for both."""
    col, dark, light = ("#3DAA5C", "#2A7F45", "#8FD98A") if role == "groom" else ("#3F8FD8", "#2C68B0", "#9CCBF2")
    w = "M-20 -6 Q-36 24 -14 44 Q0 20 -4 -8Z" if wing == "down" else "M-16 4 Q-50 -14 -58 -46 Q-28 -30 -4 -10Z"
    veil = '<path d="M-2 -58 Q-48 -40 -46 44 Q-20 10 -6 -40Z" fill="#fff" opacity=".8"/>' if role == "bride" else ""
    top = ('<path d="M-10 -56 V-80 H20 V-56Z" fill="#2B2320"/><rect x="-18" y="-60" width="46" height="7" rx="3.5" fill="#2B2320"/><rect x="-10" y="-67" width="30" height="5" fill="#E5344A"/>'
           if role == "groom" else
           f'<circle cx="-8" cy="-54" r="6" fill="{PINK}"/><circle cx="5" cy="-59" r="6.5" fill="#fff"/><circle cx="18" cy="-55" r="6" fill="{PINK}"/>')
    inner = (veil + f'<path d="M-12 28 L-44 62 L-28 60 L-26 76 L8 36Z" fill="{dark}"/>' + stroke("M-4 40 v9 h7 M10 40 v9 h7", "#6B5B53", 4)
             + f'<ellipse cy="8" rx="26" ry="36" fill="{col}"/><ellipse cx="7" cy="14" rx="14" ry="24" fill="{light}"/><path d="{w}" fill="{dark}"/>'
             + f'<circle cx="6" cy="-36" r="22" fill="{col}"/><circle cx="14" cy="-38" r="11" fill="{CREAM}"/><circle cx="16" cy="-38" r="4.2" fill="{INK}"/>'
             + '<circle cx="17.3" cy="-39.5" r="1.3" fill="#fff"/><path d="M23 -47 Q46 -44 37 -18 Q32 -30 21 -30Z" fill="#F4D9A8"/>'
             + '<circle cx="14" cy="-22" r="4" fill="#F0705F" opacity=".5"/>' + top)
    return group(x, y, s, flip, 0, inner)


def hen(x: float, y: float, s: float = 1, flip: bool = False, col: str = CREAM, rot: float = 0) -> str:
    r = f" rotate({rot})" if rot else ""
    return f'<use href="#hn" fill="{col}" filter="url(#p)" transform="translate({x} {y}){r} scale({-s if flip else s} {s})"/>'


def goat(x: float, y: float, s: float = 1, flip: bool = False, rot: float = 0) -> str:
    inner = ('<g fill="#CFC6B8"><rect x="-28" y="14" width="10" height="36" rx="5"/><rect x="14" y="14" width="10" height="36" rx="5"/></g>'
             '<rect x="-38" y="-18" width="72" height="44" rx="22" fill="#F1EBE0"/>' + stroke("M30 -50 q-4 -18 -16 -22 M41 -50 q8 -14 2 -26", "#8A7A66", 5)
             + '<path d="M18 -42 l-18 -4 l14 12z M52 -42 l16 -6 l-10 14z" fill="#CFC6B8"/><ellipse cx="35" cy="-34" rx="18" ry="20" fill="#F1EBE0"/>'
             '<path d="M29 -16 l6 16 l6 -16z" fill="#CFC6B8"/><ellipse cx="36" cy="-25" rx="5" ry="3.5" fill="#F2A9B0"/>'
             f'<circle cx="28" cy="-38" r="3" fill="{INK}"/><circle cx="43" cy="-38" r="3" fill="{INK}"/>')
    return group(x, y, s, flip, rot, inner)


def pig(x: float, y: float, s: float = 1, flip: bool = False, rot: float = 0) -> str:
    inner = ('<g fill="#E58FA3"><rect x="-20" y="10" width="10" height="24" rx="5"/><rect x="8" y="10" width="10" height="24" rx="5"/></g>'
             + stroke("M-30 -4 q-12 -4 -8 -12 q6 -4 6 4", "#E58FA3", 4)
             + '<ellipse rx="32" ry="24" fill="#F6B3C1"/><path d="M8 -28 l2 -18 l12 12z M32 -30 l12 -12 l2 18z" fill="#E58FA3"/><circle cx="24" cy="-12" r="20" fill="#F6B3C1"/>'
             '<ellipse cx="31" cy="-6" rx="10" ry="7" fill="#E58FA3"/><circle cx="28" cy="-6" r="1.8" fill="#B85C74"/><circle cx="34" cy="-6" r="1.8" fill="#B85C74"/>'
             f'<circle cx="18" cy="-19" r="3" fill="{INK}"/><circle cx="33" cy="-20" r="3" fill="{INK}"/>')
    return group(x, y, s, flip, rot, inner)


def cloud(x: float, y: float, s: float = 1, fill: str = "#fff") -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" opacity=".9">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def palm(x: float, y: float, s: float = 1, flip: bool = False) -> str:
    return f'<use href="#pm" transform="translate({x} {y}) scale({-s if flip else s} {s})"/>'


def house(x: float, y: float, s: float, col: str) -> str:
    return f'<use href="#hs" fill="{col}" transform="translate({x} {y}) scale({s})"/>'


def spark(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#k" transform="translate({x} {y}) scale({s})"/>'


def star(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def hill(y: float, amp: float, fill: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def drops(pts: list, fill: str = BLUE) -> str:
    return f'<g fill="{fill}">' + "".join(f'<path d="M{a} {b} q7 12 0 17 q-7 -5 0 -17z"/>' for a, b in pts) + '</g>'


def bunting(x1: float, y1: float, x2: float, y2: float, sag: float, n: int, sz: float = 14) -> str:
    flags = ""
    for i in range(n):
        t = (i + .5) / n
        fx, fy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t + sag * 4 * t * (1 - t)
        flags += f'<path d="M{fx - sz * .6:.0f} {fy:.0f} h{sz * 1.2:.0f} l{-sz * .6:.0f} {sz * 1.5:.0f}z" fill="{FLAGS[i % len(FLAGS)]}"/>'
    return stroke(f"M{x1} {y1} Q{(x1 + x2) / 2:.0f} {(y1 + y2) / 2 + 2 * sag:.0f} {x2} {y2}", "#fff", 2.5) + flags


def arch(x: float, y: float, s: float = 1) -> str:
    """The wedding arch: two poles, a palm-leaf bow, paper flags and pink flowers."""
    bow = "M-92 -112 Q0 -196 92 -112"
    inner = (stroke("M-92 0 V-112 M92 0 V-112", "#A9764A", 9) + stroke(bow, "#2F8F4E", 22)
             + f'<path d="{bow}" stroke="{G_LITE}" stroke-width="10" fill="none" stroke-dasharray="14 12"/>' + bunting(-88, -100, 88, -100, 24, 7, 11)
             + "".join(f'<circle cx="{a}" cy="{b}" r="10" fill="{PINK}"/><circle cx="{a}" cy="{b}" r="4" fill="#fff"/>' for a, b in [(-92, -116), (92, -116), (0, -156)]))
    return group(x, y, s, False, 0, inner)


def back(far: str = "#A9DB8E", mid: str = "#74C26B", houses: list = VILLAGE) -> list:
    """Sea, far hill with the pastel village, and the near hill."""
    return ['<rect y="290" width="800" height="80" fill="#5CC7C9"/>', hill(345, 26, far, False),
            *[house(*h) for h in houses], hill(408, 22, mid)]


ROAD = f'<path filter="url(#p)" d="M0 462 Q400 430 800 470 V566 Q400 528 0 556Z" fill="{SAND}"/>'
FRONT = f'<path d="M0 600 V572 Q400 540 800 580 V600Z" fill="{G_DARK}"/>'
PLAZA = f'<path filter="url(#p)" d="M0 452 Q400 424 800 452 V600 H0Z" fill="{SAND}"/>'
DEFS = {
    "pm": ('<g id="pm" filter="url(#p)"><path d="M0 0 Q-16 -80 6 -160" stroke="#A9764A" stroke-width="15" fill="none" stroke-linecap="round"/>'
           '<g transform="translate(6 -162)"><g id="pf"><path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#2F8F4E" transform="rotate(-52)"/>'
           '<path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#5DB85C" transform="rotate(-12)"/><path d="M0 0 Q44 -40 96 -4 Q46 -18 0 0Z" fill="#2F8F4E" transform="rotate(28)"/></g>'
           '<use href="#pf" transform="scale(-1 1)"/><circle cx="-5" cy="6" r="7" fill="#7A5236"/><circle cx="7" cy="9" r="7" fill="#8A5E3C"/></g></g>'),
    "hs": ('<g id="hs"><rect x="-24" y="-34" width="48" height="34" rx="3"/><path d="M-31 -32 L0 -58 L31 -32Z" fill="#D9603B"/>'
           '<rect x="-6" y="-18" width="12" height="18" rx="3" fill="#8A5A3C"/><rect x="10" y="-27" width="9" height="9" rx="2" fill="#FFF6E6"/></g>'),
    "hn": ('<g id="hn">' + stroke("M-6 18 V32 h7 M8 18 V32 h7", "#E07B2A", 4) + '<path d="M-18 -6 L-38 -22 L-30 8Z"/><ellipse rx="24" ry="20"/>'
           f'<circle cx="18" cy="-20" r="13"/><circle cx="15" cy="-34" r="5" fill="{RED}"/><circle cx="23" cy="-32" r="4" fill="{RED}"/>'
           f'<path d="M29 -25 L41 -20 L29 -15Z" fill="{BEAK}"/><circle cx="21" cy="-23" r="3" fill="{INK}"/><path d="M-12 -4 Q6 -6 8 8 Q-6 14 -14 6Z" fill="#E3C9A3"/></g>'),
    "k": '<path id="k" d="M0 -10 Q1 -1 10 0 Q1 1 0 10 Q-1 1 -10 0 Q-1 -1 0 -10Z" fill="#fff"/>',
    "s": f'<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="{GOLD}"/>',
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
    with open(f"{OUT}/rooster-{n:02d}.svg", "w") as fh:
        fh.write(doc)


# 01 cover
svg(1, "The Rooster and the Wedding", "Paper-cut cover: a proud rooster with a red comb, a glossy orange and green tail and a little blue bow tie struts along a sunny country road between palm trees, towards a far-off wedding arch hung with paper flags.", DAY, [
    cloud(170, 110, 1.2), cloud(640, 80, 1), *back(),
    f'<path filter="url(#p)" d="M60 600 Q330 480 520 420 Q590 396 594 372 H622 Q650 420 610 460 Q540 530 600 600Z" fill="{SAND}"/>',
    arch(608, 376, .5), palm(470, 425, .6), palm(715, 430, .75, True),
    palm(80, 560, 1.75), palm(735, 590, 1.6, True),
    rooster(330, 440, 1.9, head=-6, legs="walk"),
    marks(["M120 420 h44", "M100 462 h56", "M130 504 h40"]),
    hibiscus(560, 560, 1.3), hibiscus(660, 520, 1), hibiscus(40, 575, 1.1),
    f'<path d="M0 600 V584 Q60 570 150 600Z" fill="{G_DARK}"/>'])

# 02 getting ready at dawn
fence = (stroke("M0 440 H800 M0 486 H800", "#D8B48A", 12)
         + '<g fill="#C39A6C" filter="url(#p)">' + "".join(f'<rect x="{a}" y="400" width="22" height="130" rx="6"/>' for a in (30, 180, 700))
         + '<rect x="548" y="350" width="26" height="180" rx="6"/></g>')
mirror = ('<g filter="url(#p)"><rect x="556" y="318" width="10" height="36" fill="#2FB5B0"/><circle cx="561" cy="270" r="54" fill="#2FB5B0"/></g>'
          f'<circle cx="561" cy="270" r="44" fill="#DDF3F6"/><circle cx="552" cy="282" r="17" fill="{NECK}"/><circle cx="546" cy="262" r="7" fill="{RED}"/>'
          f'<circle cx="556" cy="259" r="7" fill="{RED}"/><path d="M536 280 l-14 5 l14 6z" fill="{BEAK}"/><circle cx="546" cy="279" r="3" fill="{INK}"/>'
          f'<path d="M552 300 l-12 -8 v16z M552 300 l12 -8 v16z" fill="{BOW}"/>' + stroke("M580 240 q12 10 12 26", "#fff", 5))
svg(2, "Rooster gets ready", "Paper-cut dawn scene: under a pink morning sky, the rooster in his blue bow tie preens his shiny feathers in front of a little round mirror on a fence post, excited for the wedding.", DAWN, [
    cloud(160, 150, 1.3, "#FFE1D2"), cloud(600, 100, 1.5, "#FFE1D2"), cloud(380, 60, .9, "#FFD3C4"),
    hill(350, 30, "#B9DDA0", False), house(110, 420, 2.6, "#F7A8B8"), hill(430, 18, "#8FCF7A"),
    palm(745, 500, 1.5, True), fence, mirror,
    rooster(300, 420, 1.8, look=(2.5, 0), wing="up", tail=-6),
    spark(120, 320, 1.6), spark(190, 270, 1), spark(380, 300, .9), spark(250, 470, .8), spark(430, 250, 1.2), FRONT])

# 03 a kernel in the mud
puddle = '<ellipse cx="590" cy="512" rx="110" ry="30" fill="#8A5E3C" filter="url(#p)"/><ellipse cx="580" cy="508" rx="76" ry="17" fill="#A47148"/>'
svg(3, "A kernel of corn", "Paper-cut scene: strutting down the country road, the rooster spots one plain yellow kernel of corn sitting in the middle of a brown mud puddle.", DAY, [
    cloud(600, 110, 1.3), cloud(130, 80, 1), *back(), palm(730, 440, 1.3, True), palm(60, 440, 1.1), ROAD, puddle,
    '<path d="M580 488 q14 4 13 16 q-1 9 -13 9 q-12 0 -13 -9 q-1 -12 13 -16z" fill="#F7E463"/><ellipse cx="580" cy="508" rx="6" ry="3" fill="#FFF8D6"/>',
    marks(["M548 470 l-10 -14", "M580 462 v-16", "M612 470 l10 -14"]),
    rooster(250, 410, 1.6, head=14, look=(2.5, 2.5), legs="walk"),
    marks(["M70 380 h46", "M50 420 h58", "M76 460 h42"]), FRONT])

# 04 oh no
svg(4, "Oh no, a muddy beak", "Paper-cut scene: the rooster has pecked the corn, and now his beak is covered in brown mud; his eyes are wide and his beak hangs open in shock.", DAY, [
    cloud(140, 90, 1.2), cloud(690, 150, 1), *back(), palm(60, 450, 1.2), ROAD,
    '<ellipse cx="640" cy="520" rx="120" ry="30" fill="#8A5E3C" filter="url(#p)"/><ellipse cx="630" cy="516" rx="84" ry="17" fill="#A47148"/>',
    rooster(350, 400, 2.3, mood="shock", mud=True, wing="flap", look=(2, 2), tail=8),
    drops([(540, 330), (575, 380), (520, 400), (600, 440), (555, 455)], MUD),
    marks(["M470 190 l10 -30", "M520 215 l26 -22", "M545 270 h34", "M410 185 l-6 -30"]), FRONT])

# 05 Grass says no
svg(5, "Grass says no", "Paper-cut scene: the muddy-beaked rooster holds out a wing and asks a tuft of Grass for help, but Grass closes its eyes and turns its face away.", DAY, [
    cloud(420, 90, 1.3), cloud(700, 170, .9), *back(), palm(60, 440, 1.2), ROAD,
    grass(580, 486, 1.9), marks(["M700 330 q16 -8 28 2", "M710 364 q14 -4 24 6"]),
    rooster(250, 410, 1.6, mud=True, wing="up", look=(2.5, 1)), FRONT])

# 06 Water says no
svg(6, "Water says no", "Paper-cut scene: the muddy-beaked rooster asks the sleepy puddle of Water for help, but Water just yawns a big yawn with its eyes closed.", DAY, [
    cloud(150, 100, 1.2), cloud(640, 80, 1.1), *back(), palm(740, 440, 1.3, True), ROAD,
    water(570, 508, 1.75),
    rooster(240, 410, 1.6, mud=True, wing="up", look=(2.5, 2)), FRONT])

# 07 Wind says no
leaf = "".join(f'<path d="M0 0 Q10 -12 24 0 Q10 8 0 0Z" fill="{c}" transform="translate({a} {b}) rotate({r})"/>'
               for a, b, r, c in [(420, 330, 20, G_LITE), (520, 370, -30, G_DARK), (690, 330, 40, G_LITE), (330, 250, -10, G_DARK), (760, 250, 10, G_DARK)])
svg(7, "Wind says no", "Paper-cut scene: the rooster looks up and calls to the Wind, a swirly cloud with puffed cheeks, but Wind is too busy blowing and whooshes right past with leaves flying.", DAY, [
    cloud(120, 110, 1), *back(), ROAD,
    marks(["M110 170 q70 -20 150 -4", "M80 215 q80 -16 170 0", "M130 262 q60 -12 120 2"]),
    wind(540, 210, 1.9), leaf,
    rooster(220, 415, 1.6, mud=True, wing="up", head=-20, look=(1.5, -2.5)), FRONT])

# 08 sad on a stone
svg(8, "Rooster sits down sadly", "Paper-cut scene: the rooster sits sadly on a grey stone by the road, his beak still muddy, and looks up at the sky, where a soft golden light peeks from behind a cloud.", GREY, [
    f'<circle cx="610" cy="130" r="70" fill="{GOLD}" opacity=".3"/><circle cx="610" cy="130" r="44" fill="{GOLD}"/>',
    cloud(600, 160, 2), cloud(170, 110, 1.3, "#F4F1EA"), *back("#A3CF93", "#6FB56C"), palm(60, 440, 1.2), ROAD,
    rooster(350, 392, 1.7, mood="sad", mud=True, head=-26, look=(1.5, -2.5), legs="sit", tail=10),
    drops([(371, 324)]),
    '<ellipse cx="340" cy="488" rx="104" ry="50" fill="#9A9288" filter="url(#p)"/><ellipse cx="316" cy="468" rx="52" ry="18" fill="#B3ABA0"/>', FRONT])

# 09 the kind Sun
svg(9, "The kind Sun helps", "Paper-cut scene: the big golden Sun beams down with a huge kind smile, and warm golden rays pour all around the little rooster, who looks up in wonder.", WARM, [
    cloud(120, 100, 1.1), *back(),
    f'<g fill="{GOLD}"><path d="M500 240 L40 500 L330 600Z" opacity=".22"/><path d="M520 250 L250 600 H500Z" opacity=".2"/><circle cx="270" cy="420" r="170" opacity=".2"/></g>',
    sun(580, 170, 112), ROAD, f'<circle cx="270" cy="430" r="110" fill="{GOLD}" opacity=".28"/>',
    rooster(270, 420, 1.7, mud=True, head=-22, look=(1.5, -2.5), wing="up"),
    star(120, 330, 1.5), star(430, 400, 1.3), star(170, 250, 1), star(400, 290, .9), star(90, 470, 1), star(460, 520, 1.1), FRONT])

# 10 Water washes
svg(10, "Water washes his beak", "Paper-cut scene: Water wakes up bright and sparkling and splashes the rooster's beak clean, with water droplets flying everywhere while the Sun smiles above.", WARM, [
    sun(700, 95, 56, "smile"), cloud(150, 100, 1.2), *back(), ROAD,
    stroke("M500 430 Q450 280 372 338", BLUE, 26) + stroke("M496 420 Q450 296 380 334", BLUE_LITE, 8),
    water(550, 500, 1.9, "awake"),
    rooster(240, 415, 1.7, mood="joy", wing="flap", head=-4),
    drops([(390, 270), (430, 240), (340, 262), (470, 300), (410, 372), (360, 400), (300, 240), (520, 250), (455, 380), (640, 380), (690, 430), (420, 190)]),
    drops([(372, 420), (396, 452)], MUD),
    spark(600, 400, 1.3), spark(660, 470, 1), spark(470, 470, 1), spark(350, 210, 1.2), spark(500, 200, .9), FRONT])

# 11 Wind dries, Grass gives a flower
svg(11, "Wind dries him and Grass gives a flower", "Paper-cut scene: Wind whooshes kindly to dry the rooster's fluttering feathers, and Grass smiles and holds out a red hibiscus flower for his bow tie, while the Sun shines.", WARM, [
    sun(715, 90, 54, "smile"), *back(), ROAD,
    wind(175, 215, 1.6, "kind"),
    marks(["M250 340 q30 20 26 50", "M200 380 q30 14 34 44", "M300 300 q26 14 30 40"]),
    grass(660, 488, 1.8, "kind", True), stroke("M610 440 Q590 400 562 392", G_DARK, 7), hibiscus(552, 386, 1.9),
    rooster(400, 420, 1.7, tail=-14, wing="flap", look=(2.5, 1)), FRONT])

# 12 the wedding
svg(12, "Just in time for the wedding", "Paper-cut scene: under a palm-leaf arch hung with paper flags stand Uncle Perico, a green parrot in a top hat, and his bride, a blue parrot in a veil; the hens, a goat and a little pig all turn to look as the rooster arrives with a red flower on his bow tie.", DAY, [
    *back(houses=VILLAGE[:3]), palm(45, 470, 1.5), PLAZA,
    arch(500, 486, 1.85), parrot(446, 404, 1.3, True), parrot(556, 408, 1.3, True, "bride"),
    hen(330, 472, 1.05, True, "#F3D9B1"), goat(738, 500, 1.2, True),
    rooster(150, 440, 1.5, wing="up", flower=True, look=(2.5, 0), legs="walk"),
    hen(290, 545, 1.3, True), pig(620, 552, 1.25, True)])

# 13 the party
svg(13, "Cock-a-doodle-doo!", "Paper-cut scene: everyone dances at the wedding party — the two parrots, the hens, the goat and the little pig — while the rooster throws back his head and crows a great big crow, and the golden Sun smiles over them all.", WARM, [
    sun(675, 105, 70, "smile"), bunting(0, 70, 520, 40, 60, 9, 16), *back(houses=[]), PLAZA,
    parrot(95, 430, 1.25, False, "groom", "up"), parrot(200, 436, 1.25, True, "bride", "up"),
    goat(690, 462, 1.25, True, 8), hen(735, 548, 1.2, True, CREAM, -10), hen(290, 556, 1.1, False, "#F3D9B1", -8), pig(600, 545, 1.2, True, -8),
    stroke("M508 280 q26 -30 4 -56 q-22 -28 8 -56", "#E5344A", 6) + stroke("M546 300 q34 -24 20 -56 q-12 -28 16 -48", "#fff", 6)
    + stroke("M470 262 q10 -30 -10 -50 q-16 -20 0 -44", "#fff", 6),
    rooster(440, 420, 1.8, mood="joy", crow=True, head=-38, wing="flap", flower=True, tail=6),
    marks(["M30 380 q-14 -16 -6 -34", "M262 372 q14 -14 8 -32", "M770 420 q12 -16 4 -34", "M530 500 q-12 -10 -10 -26"])])
