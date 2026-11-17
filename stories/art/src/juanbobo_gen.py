#!/usr/bin/env python3
"""Generates the 13 Juan-Bobo-and-the-Pig flip-book SVGs from shared character parts.

Usage: python3 juanbobo_gen.py <output-dir>
Scale rule: every character is drawn at its own base size times one page factor k, so on every page
the pig (about 105 tall) < Juan Bobo (about 240 with his hat) < Mamá (about 265 with her hat).
The pig's outfit is built up from ITEMS in order; each dressing page adds one or two items, and the little
paper banner at the top shows the growing list (dress, earrings, necklace, lipstick, shoes).
The mud puddle first appears on page 11, so the SPLASH is not spoiled.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
PIG, PIG_D, PIG_L, SNOUT = "#F4A7B5", "#D97F93", "#FBCDD5", "#E98FA2"
DRESS, DRESS_D, GOLD, GOLD_D, PEARL, LIP, SHOE = "#F6C94A", "#C99A1E", "#F2B53A", "#A9771A", "#FFFDF4", "#D8263E", "#D8263E"
MUD, MUD_D, MUD_L = "#8A5A36", "#6A4226", "#A9774E"
J_SKIN, M_SKIN, HAIR = "#B9784E", "#9A5E3C", "#2B1D16"
SHIRT, SHORTS, STRAW, STRAW_D, BAND = "#FFFDF6", "#6F93C2", "#EBCB76", "#C7A04A", "#C8463A"
M_DRESS, M_DRESS_D, M_HAT, M_SHOES = "#4F7FC4", "#3A649F", "#FFFFFF", "#3A2A24"
GRASS, GRASS_D, GRASS_L, HILL, HILL_FAR = "#7CC46A", "#4E9A4E", "#A6DA84", "#5DAE62", "#8ACB8C"
PATH, PATH_D = "#E3C38E", "#C9A66E"
WALL, WALL_D, ROOF, ROOF_D, SHUTTER, DOOR = "#5CC6C0", "#3FA19B", "#D9573F", "#A8402E", "#F28CB0", "#F7D046"
WOOD, WOOD_D = "#B07A48", "#7E5130"
TRUNK, FROND, FROND_D = "#9C7046", "#3F9A56", "#2E7D44"
TUB, TUB_D, WATER = "#B8C4CC", "#8A98A3", "#8FD0F0"
DAY = [(0, "#78CDEE"), (1, "#EAF8F2")]
GOLDEN = [(0, "#8FCFEA"), (.55, "#FDE7C0"), (1, "#FCD39A")]
ITEMS = ("dress", "earrings", "necklace", "lipstick", "shoes")


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, inner: str, flip: bool = False, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


def arm(sx: float, sy: float, hx: float, hy: float, col: str, w: float = 11) -> str:
    side = -1 if hx < sx else 1
    mx, my = (sx + hx) / 2 + side * 10, (sy + hy) / 2 + 12
    return stroke(f"M{sx} {sy} Q{mx} {my} {hx} {hy}", col, w) + f'<circle cx="{hx}" cy="{hy}" r="7.5" fill="{col}"/>'


def sparkle(x: float, y: float, s: float = 1) -> str:
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 -14 L3.5 -3.5 L14 0 L3.5 3.5 L0 14 L-3.5 3.5 L-14 0 L-3.5 -3.5Z" '
            f'fill="#FFF3B0" stroke="{GOLD_D}" stroke-width="1.5"/>')


# ---------------------------------------------------------------- the outfit, as stand-alone objects
def dress_obj(x: float, y: float, s: float = 1) -> str:
    """Mamá's fancy yellow dress, front view, (x, y) = middle of the shoulders."""
    hem = "".join(" q-7 12 -14 0" for _ in range(8))
    d = f"M-18 0 Q0 8 18 0 L24 6 L20 40 L56 112{hem} L-20 40 L-24 6Z"
    flow = "".join(f'<circle cx="{a}" cy="{b}" r="4" fill="{c}"/>' for a, b, c in
                   [(-20, 70, "#fff"), (8, 60, "#F2789F"), (30, 88, "#fff"), (-36, 98, "#F2789F"), (2, 96, "#fff"), (14, 26, "#F2789F")])
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><path d="{d}" fill="{DRESS}" stroke="{DRESS_D}" stroke-width="2.5"/>'
            f'{flow}<path d="M-20 38 Q0 46 20 38 L20 46 Q0 54 -20 46Z" fill="#F2789F"/></g>')


def hoop(cx: float, cy: float, r: float, col: str, w: float) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}"/>'


def earrings_obj(x: float, y: float, s: float = 1) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{hoop(-11, 0, 8, GOLD_D, 4.5)}{hoop(11, 0, 8, GOLD_D, 4.5)}</g>'


def necklace_obj(x: float, y: float, s: float = 1) -> str:
    pts = [(-16 + 4 * i, 12 - 16 * ((i - 4) / 4) ** 2 - 4) for i in range(9)]
    beads = "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4.2" fill="{PEARL}" stroke="{INK}" stroke-width="1"/>' for a, b in pts)
    return f'<g transform="translate({x} {y}) scale({s})">{stroke("M-16 -8 Q0 -22 16 -8", "#C9B79A", 1.6)}{beads}</g>'


def lipstick_obj(x: float, y: float, s: float = 1, rot: float = -20) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-7" y="-2" width="14" height="22" rx="2" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="1.5"/>'
            f'<path d="M-6 -2 V-16 L6 -24 V-2Z" fill="{LIP}"/></g>')


def shoe_obj(x: float, y: float, s: float = 1) -> str:
    """A red high-heeled shoe, side view, toe to the right."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-16 -14 Q-6 -10 2 -2 Q12 2 18 2 L18 6 L-12 6 Q-16 0 -16 -14Z" fill="{SHOE}"/>'
            f'<path d="M-16 -14 L-14 10 L-11 10 L-10 -4Z" fill="#9E1A2C"/></g>')


ICON = {"dress": lambda x, y: dress_obj(x, y - 19, .32), "earrings": lambda x, y: earrings_obj(x, y, .9),
        "necklace": lambda x, y: necklace_obj(x, y, 1.1), "lipstick": lambda x, y: lipstick_obj(x, y + 2, .9, 0),
        "shoes": lambda x, y: shoe_obj(x, y, 1.2)}


def banner(items: tuple) -> str:
    """The paper list across the top of a dressing page: one icon per thing the pig has on so far."""
    w = 30 + 56 * len(items)
    x0 = 400 - w / 2
    out = f'<rect filter="url(#p)" x="{x0}" y="22" width="{w}" height="62" rx="16" fill="{CREAM}" stroke="#E6D3B3" stroke-width="2"/>'
    for i, it in enumerate(items):
        out += ICON[it](x0 + 43 + 56 * i, 53)
    return out


# ---------------------------------------------------------------- the pig
PIG_BASE = 1.0


def pig_shoe(fx: float, lift: float) -> str:
    return (f'<path d="M{fx - 10} {-lift - 4} Q{fx} {-lift - 10} {fx + 12} {-lift} L{fx + 13} {-lift + 4} L{fx - 10} {-lift + 4}Z" fill="{SHOE}"/>'
            f'<path d="M{fx - 10} {-lift + 2} L{fx - 9} 0 L{fx - 5} 0 L{fx - 4} {-lift + 2}Z" fill="#9E1A2C"/>')


def pig_dress() -> str:
    hem = "".join(" q-7 11 -14 0" for _ in range(8))
    d = "M44 -102 Q0 -112 -50 -98 Q-70 -70 -62 -30 L50 -30 Q60 -66 44 -102Z"
    ruffle = f"M52 -32{hem} L-62 -30 L-60 -40 L52 -42Z"
    flow = "".join(f'<circle cx="{a}" cy="{b}" r="4.5" fill="{c}"/>' for a, b, c in
                   [(-40, -70, "#fff"), (-14, -86, "#F2789F"), (10, -60, "#fff"), (30, -84, "#F2789F"), (-24, -48, "#F2789F"), (24, -44, "#fff")])
    bow = (f'<path d="M-36 -104 L-58 -122 L-56 -94Z M-36 -104 L-14 -124 L-16 -96Z" fill="#F2789F" stroke="#C9547A" stroke-width="2"/>'
           f'<circle cx="-36" cy="-104" r="6" fill="#C9547A"/>')
    return (f'<path d="{d}" fill="{DRESS}" stroke="{DRESS_D}" stroke-width="2.5"/><path d="{ruffle}" fill="{DRESS}" stroke="{DRESS_D}" stroke-width="2.5"/>'
            + flow + bow)


def pig_face(items: tuple, mood: str) -> str:
    head = (f'<path d="M40 -104 L44 -132 L62 -110Z" fill="{PIG_D}"/>'
            f'<circle cx="58" cy="-80" r="32" fill="{PIG}"/>'
            f'<path d="M58 -108 L76 -134 L82 -104Z" fill="{PIG}"/><path d="M64 -108 L75 -126 L78 -106Z" fill="{SNOUT}"/>'
            f'<ellipse cx="90" cy="-74" rx="13" ry="15" fill="{SNOUT}"/>'
            f'<ellipse cx="87" cy="-78" rx="2.6" ry="4.2" fill="#9E4E60"/><ellipse cx="94" cy="-70" rx="2.6" ry="4.2" fill="#9E4E60"/>'
            f'<circle cx="62" cy="-66" r="7" fill="#F0705F" opacity=".4"/>')
    if mood in ("squeal", "joy"):
        head += stroke("M64 -95 l9 4 l-9 4", INK, 3)
    else:
        head += f'<circle cx="70" cy="-90" r="5" fill="#fff"/><circle cx="71.5" cy="-90" r="3" fill="{INK}"/>'
    if "lipstick" in items:
        head += (f'<path d="M68 -58 Q75 -65 81 -60 Q87 -65 94 -58 Q82 -46 68 -58Z" fill="{LIP}"/>'
                 + stroke("M70 -58 Q81 -56 92 -58", "#9E1A2C", 1.5))
    elif mood == "squeal":
        head += '<ellipse cx="80" cy="-55" rx="8" ry="7" fill="#7A2E3A"/>'
    elif mood == "joy":
        head += '<path d="M70 -58 Q81 -60 90 -58 Q86 -46 80 -46 Q72 -46 70 -58Z" fill="#7A2E3A"/>'
    else:
        head += stroke("M70 -58 q9 7 18 -1", INK, 2.6)
    if "earrings" in items:
        head += (f'<circle cx="44" cy="-102" r="2.5" fill="{GOLD_D}"/>{hoop(44, -94, 7, GOLD_D, 3.5)}'
                 f'<circle cx="80" cy="-104" r="3" fill="{GOLD_D}"/>{hoop(80, -94, 9, GOLD, 4.5)}')
    if "necklace" in items:
        pts = [(36 - 56 * t * (1 - t) + 6 * t, -108 + 60 * t) for t in [i / 9 for i in range(10)]]
        head += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4.6" fill="{PEARL}" stroke="{INK}" stroke-width="1.1"/>' for a, b in pts)
    return head


MUD_SPOTS = [(-38, -78, 16, 10), (-6, -96, 12, 7), (18, -62, 18, 11), (-30, -44, 12, 8), (52, -100, 8, 6), (90, -88, 7, 5), (48, -60, 9, 7), (-60, -58, 7, 9)]


def pig(x: float, y: float, k: float = 1, items: tuple = (), mood: str = "happy", pose: str = "stand",
        mud: bool = False, legs: bool = True) -> str:
    """The family pig, side view facing right. (x, y) is her feet. pose: stand / trot."""
    lift = 12 if "shoes" in items else 0
    out = ""
    if legs:
        feet = [(-44, -46), (-24, -22), (22, 22), (42, 46)] if pose == "stand" else [(-44, -58), (-24, -14), (22, 10), (42, 56)]
        for top, foot in feet:
            out += stroke(f"M{top} {-40 - lift} L{foot} {-6 - lift}", PIG_D if top in (-24, 42) else PIG, 15)
            out += pig_shoe(foot, lift) if lift else f'<rect x="{foot - 7}" y="-8" width="14" height="8" rx="3" fill="#7A4A4A"/>'
    body = stroke("M-62 -76 q-16 -4 -14 -18 q6 -10 12 0 q4 10 -10 10", PIG_D, 4)
    body += f'<ellipse cx="-2" cy="-66" rx="62" ry="38" fill="{PIG}"/><ellipse cx="-10" cy="-80" rx="40" ry="16" fill="{PIG_L}" opacity=".6"/>'
    if "dress" in items:
        body += pig_dress()
    body += pig_face(items, mood)
    if mud:
        body += "".join(f'<ellipse cx="{a}" cy="{b}" rx="{rx}" ry="{ry}" fill="{MUD}" opacity=".92"/>' for a, b, rx, ry in MUD_SPOTS)
        body += stroke("M-14 -40 v10 M30 -38 v8 M-44 -42 v7", MUD, 5)
    return group(x, y, PIG_BASE * k, out + f'<g transform="translate(0 {-lift})">{body}</g>')


# ---------------------------------------------------------------- Juan Bobo
J_HANDS = {
    "down": ((-40, -96), (40, -96)), "wave": ((-40, -96), (58, -222)),
    "present": ((-40, -96), (72, -130)), "hold": ((-40, -96), (64, -168)),
    "sheepish": ((-40, -96), (24, -214)), "scrub": ((-36, -100), (62, -112)),
    "oh": ((-30, -166), (30, -166)),
}


def juan_face(mood: str) -> str:
    face = f'<circle cy="-186" r="30" fill="{J_SKIN}"/>'
    face += f'<path d="M-28 -196 Q-30 -178 -24 -172 L-20 -196Z M28 -196 Q30 -178 24 -172 L20 -196Z" fill="{HAIR}"/>'
    if mood == "laugh":
        face += stroke("M-16 -188 q6 -6 12 0 M4 -188 q6 -6 12 0", INK, 3)
    else:
        face += "".join(f'<circle cx="{a}" cy="-188" r="5" fill="#fff"/><circle cx="{a + 1}" cy="-187" r="3" fill="{INK}"/>' for a in (-11, 11))
    face += f'<circle cx="-18" cy="-174" r="5.5" fill="#F0705F" opacity=".4"/><circle cx="18" cy="-174" r="5.5" fill="#F0705F" opacity=".4"/>'
    if mood == "oh":
        face += '<ellipse cy="-168" rx="6" ry="7" fill="#5A2E22"/>'
    elif mood in ("laugh", "big"):
        face += '<path d="M-12 -172 Q0 -170 12 -172 Q8 -158 0 -158 Q-8 -158 -12 -172Z" fill="#5A2E22"/>'
    elif mood == "sheepish":
        face += stroke("M-9 -168 q5 -4 9 0 q5 4 9 0", INK, 2.6)
    else:
        face += stroke("M-11 -170 q11 9 22 0", INK, 2.8)
    hat = (f'<ellipse cy="-206" rx="52" ry="11" fill="{STRAW_D}"/><ellipse cy="-208" rx="50" ry="9" fill="{STRAW}"/>'
           f'<path d="M-27 -210 Q-26 -246 0 -250 Q26 -246 27 -210Z" fill="{STRAW}"/>'
           f'<path d="M-27 -218 Q0 -224 27 -218 L27 -210 Q0 -214 -27 -210Z" fill="{BAND}"/>'
           + stroke("M-16 -226 l6 -16 M0 -228 v-18 M16 -226 l-6 -16", STRAW_D, 1.8))
    return face + hat


def juan(x: float, y: float, k: float = 1, hands: str = "down", mood: str = "smile", held: str = "") -> str:
    """Juan Bobo, facing us: a barefoot country boy in a straw pava hat. (x, y) is his feet."""
    (lx, ly), (rx, ry) = J_HANDS[hands]
    out = stroke("M-12 -64 V-8 M12 -64 V-8", J_SKIN, 13)
    out += f'<ellipse cx="-16" cy="-5" rx="13" ry="6" fill="{J_SKIN}"/><ellipse cx="16" cy="-5" rx="13" ry="6" fill="{J_SKIN}"/>'
    out += f'<path d="M-30 -100 L30 -100 L34 -56 L4 -56 L0 -70 L-4 -56 L-34 -56Z" fill="{SHORTS}"/>'
    out += stroke("M-33 -60 h26 M7 -60 h26", "#5679A8", 3)
    out += f'<path d="M-36 -152 Q0 -160 36 -152 L40 -96 Q0 -90 -40 -96Z" fill="{SHIRT}"/>'
    out += f'<rect x="-8" y="-168" width="16" height="16" fill="{J_SKIN}"/>'
    out += f'<path d="M-12 -154 L0 -140 L12 -154Z" fill="{J_SKIN}"/>' + "".join(f'<circle cy="{b}" r="2" fill="#C9B79A"/>' for b in (-130, -116, -102))
    out += juan_face(mood)
    out += arm(-32, -146, lx, ly, J_SKIN) + arm(32, -146, rx, ry, J_SKIN)
    out += f'<circle cx="-32" cy="-146" r="11" fill="{SHIRT}"/><circle cx="32" cy="-146" r="11" fill="{SHIRT}"/>'
    if held == "dress":
        out += dress_obj(rx + 10, ry - 12, .78)
    elif held == "lipstick":
        out += lipstick_obj(rx + 4, ry - 12, 1.3, 20)
    elif held == "brush":
        out += (f'<g transform="translate({rx + 2} {ry}) rotate(-15)"><rect x="-4" y="-4" width="30" height="10" rx="4" fill="{WOOD}"/>'
                f'<rect x="20" y="-8" width="28" height="16" rx="5" fill="{WOOD_D}"/>' + stroke("M24 10 v6 M32 10 v6 M40 10 v6", "#E8D9B8", 2.5) + '</g>')
    return group(x, y, k, out)


# ---------------------------------------------------------------- Mamá
M_HANDS = {
    "down": ((-44, -128), (44, -128)), "point": ((-44, -128), (54, -226)),
    "laugh": ((-16, -134), (16, -134)), "pour": ((-70, -142), (-62, -172)),
}


def mama(x: float, y: float, k: float = 1, hands: str = "down", mood: str = "smile") -> str:
    """Mamá in her blue Sunday church dress and a little white hat with a pink flower. (x, y) is her feet."""
    (lx, ly), (rx, ry) = M_HANDS[hands]
    out = stroke("M-14 -40 V-10 M14 -40 V-10", M_SKIN, 11)
    out += f'<ellipse cx="-16" cy="-6" rx="13" ry="7" fill="{M_SHOES}"/><ellipse cx="16" cy="-6" rx="13" ry="7" fill="{M_SHOES}"/>'
    out += f'<path d="M-34 -184 Q0 -194 34 -184 L40 -130 L64 -34 Q0 -22 -64 -34 L-40 -130Z" fill="{M_DRESS}"/>'
    out += f'<path d="M-40 -132 Q0 -124 40 -132 L42 -122 Q0 -114 -42 -122Z" fill="{M_DRESS_D}"/>'
    out += '<path d="M-62 -40 Q0 -28 62 -40 L64 -34 Q0 -22 -64 -34Z" fill="#fff" opacity=".85"/>'
    out += '<path d="M-16 -186 L0 -168 L16 -186 Q0 -192 -16 -186Z" fill="#fff"/>'
    out += f'<rect x="-8" y="-200" width="16" height="16" fill="{M_SKIN}"/>'
    head = f'<circle cx="-24" cy="-246" r="16" fill="{HAIR}"/><circle cy="-220" r="32" fill="{M_SKIN}"/>'
    head += f'<path d="M-32 -224 Q-34 -256 0 -256 Q34 -256 32 -224 Q20 -244 0 -244 Q-20 -244 -32 -224Z" fill="{HAIR}"/>'
    if mood == "laugh":
        head += stroke("M-18 -222 q6 -7 12 0 M6 -222 q6 -7 12 0", INK, 3)
        head += '<path d="M-13 -206 Q0 -204 13 -206 Q9 -190 0 -190 Q-9 -190 -13 -206Z" fill="#5A2E22"/>'
    else:
        head += "".join(f'<circle cx="{a}" cy="-222" r="5" fill="#fff"/><circle cx="{a + 1}" cy="-221" r="3" fill="{INK}"/>' for a in (-12, 12))
        head += stroke("M-11 -204 q11 8 22 0", INK, 2.8)
    head += '<circle cx="-20" cy="-206" r="6" fill="#F0705F" opacity=".4"/><circle cx="20" cy="-206" r="6" fill="#F0705F" opacity=".4"/>'
    head += f'<circle cx="-31" cy="-214" r="3" fill="{GOLD}"/><circle cx="31" cy="-214" r="3" fill="{GOLD}"/>'
    head += (f'<ellipse cx="6" cy="-254" rx="34" ry="8" fill="{M_HAT}" transform="rotate(-8 6 -254)"/>'
             f'<path d="M-14 -256 Q-10 -276 10 -276 Q26 -274 26 -260Z" fill="{M_HAT}"/>'
             '<g transform="translate(22 -264)">' + "".join(f'<circle cx="{a}" cy="{b}" r="5" fill="#F2789F"/>' for a, b in [(-5, 0), (5, 0), (0, -5), (0, 5)])
             + f'<circle r="3" fill="{DRESS}"/></g>')
    out += head
    out += arm(-32, -178, lx, ly, M_SKIN, 12) + arm(32, -178, rx, ry, M_SKIN, 12)
    out += f'<circle cx="-32" cy="-178" r="12" fill="{M_DRESS}"/><circle cx="32" cy="-178" r="12" fill="{M_DRESS}"/>'
    if hands == "pour":
        out += (f'<g transform="translate(-92 -152) rotate(-100)"><path d="M-26 -22 L26 -22 L20 22 L-20 22Z" fill="{TUB}" stroke="{TUB_D}" stroke-width="3"/>'
                + stroke("M-24 -22 Q0 -56 24 -22", TUB_D, 3) + '</g>')
    return group(x, y, k, out)


# ---------------------------------------------------------------- scenery
def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def church(x: float, y: float, s: float = 1) -> str:
    """A little white country church with a bell tower, far away on a hill. (x, y) is its base."""
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><rect x="-60" y="-70" width="90" height="70" fill="#FFFDF6"/>'
            f'<path d="M-68 -66 L-15 -104 L38 -66Z" fill="{ROOF}"/><rect x="30" y="-120" width="40" height="120" fill="#F4F0E6"/>'
            f'<path d="M24 -116 L50 -150 L76 -116Z" fill="{ROOF}"/><path d="M42 -104 a8 8 0 0 1 16 0 V-90 H42Z" fill="#6B4A2E"/>'
            f'<circle cx="50" cy="-96" r="4" fill="{GOLD}"/><path d="M-26 0 V-30 a11 11 0 0 1 22 0 V0Z" fill="#8A5A36"/>'
            + stroke("M50 -150 V-170 M42 -162 H58", "#8A5A36", 3.5) + '</g>')


def casita(x: float, y: float, s: float = 1) -> str:
    """The family's turquoise wooden house on short stilts with a red tin roof and a porch. (x, y) is the middle of its base."""
    ribs = " ".join(f"M{a} -228 L{a * 1.3:.0f} -170" for a in range(-110, 111, 20))
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            + stroke("M-120 -34 V0 M-40 -34 V0 M40 -34 V0 M120 -34 V0", WOOD_D, 10)
            + f'<rect x="-130" y="-180" width="260" height="148" fill="{WALL}"/><rect x="-130" y="-46" width="260" height="14" fill="{WALL_D}"/>'
            f'<path d="M-160 -168 L-120 -232 L120 -232 L160 -168Z" fill="{ROOF}"/>' + stroke(ribs, ROOF_D, 2.5)
            + f'<rect x="-30" y="-150" width="60" height="104" rx="4" fill="{DOOR}"/><circle cx="18" cy="-98" r="4" fill="{WOOD_D}"/>'
            f'<rect x="-104" y="-148" width="50" height="44" fill="#FFF6E6"/><rect x="54" y="-148" width="50" height="44" fill="#FFF6E6"/>'
            f'<rect x="-120" y="-150" width="16" height="48" fill="{SHUTTER}"/><rect x="-54" y="-150" width="16" height="48" fill="{SHUTTER}"/>'
            f'<rect x="38" y="-150" width="16" height="48" fill="{SHUTTER}"/><rect x="104" y="-150" width="16" height="48" fill="{SHUTTER}"/>'
            f'<path d="M-36 -32 H36 L44 0 H-44Z" fill="{WOOD}"/>' + stroke("M-40 -16 H40", WOOD_D, 3) + '</g>')


def palm(x: float, y: float, s: float = 1, lean: float = 1) -> str:
    tx = 40 * lean
    trunk = stroke(f"M0 0 Q{tx * .2} -120 {tx} -230", TRUNK, 18) + stroke(
        " ".join(f"M{tx * f * f - 9:.0f} {-230 * f:.0f} h18" for f in (.2, .35, .5, .65, .8)), "#7A5634", 3)
    fronds = "".join(
        f'<path transform="translate({tx} -232) rotate({r})" d="M0 0 Q50 -28 104 4 Q60 -6 0 6Z" fill="{FROND if i % 2 else FROND_D}"/>'
        for i, r in enumerate((-170, -135, -100, -60, -25, 10, 40, 150)))
    nuts = f'<circle cx="{tx - 8}" cy="-224" r="8" fill="#8A5A36"/><circle cx="{tx + 7}" cy="-222" r="8" fill="#7A4A2A"/>'
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{trunk}{fronds}{nuts}</g>'


def banana(x: float, y: float, s: float = 1) -> str:
    leaves = "".join(f'<path transform="rotate({r})" d="M0 0 Q20 -60 6 -130 Q-24 -70 0 0Z" fill="{c}"/>'
                     for r, c in [(-50, FROND_D), (-20, FROND), (10, "#5DB85C"), (40, FROND_D)])
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><rect x="-7" y="-60" width="14" height="60" fill="#8DBA5E"/>'
            f'<g transform="translate(0 -56)">{leaves}</g></g>')


def hibiscus(pts: list) -> str:
    out = ""
    for i, (a, b) in enumerate(pts):
        col = ("#E8384F", "#F7D046", "#F2789F")[i % 3]
        out += (f'<g transform="translate({a} {b})">' + "".join(f'<circle cx="{c}" cy="{d}" r="5" fill="{col}"/>' for c, d in [(-5, 0), (5, 0), (0, -5), (0, 5)])
                + '<circle r="2.6" fill="#FFF3B0"/></g>')
    return out


def tufts(pts: list, col: str = GRASS_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def hills(church_at: tuple = (540, 236, .62)) -> list:
    cx, cy, cs = church_at
    return ['<circle cx="690" cy="92" r="40" fill="#FFE27A"/>', cloud(170, 86, 1), cloud(480, 62, .8, .85),
            f'<path d="M0 290 Q120 200 250 260 Q380 170 520 240 Q640 150 800 220 V600 H0Z" fill="{HILL_FAR}"/>',
            church(cx, cy, cs) if cs else "",
            f'<path d="M0 340 Q200 280 400 330 T800 310 V600 H0Z" fill="{HILL}"/>']


def ground(y0: float = 400, road: bool = True) -> list:
    out = [f'<path filter="url(#p)" d="M0 {y0} Q400 {y0 - 30} 800 {y0} V600 H0Z" fill="{GRASS}"/>']
    if road:
        out.append(f'<path d="M0 {y0 + 110} Q300 {y0 + 70} 520 {y0 + 40} T800 {y0 + 6} L800 {y0 + 40} Q600 {y0 + 74} 520 {y0 + 84} '
                   f'Q300 {y0 + 130} 0 {y0 + 170}Z" fill="{PATH}"/>')
    return out


def yard(house_x: float = 120, church_at: tuple = (540, 236, .62)) -> list:
    return (hills(church_at) + [palm(760, 380, .95, -1)] + ground(390)
            + [casita(house_x, 420, .85), banana(286, 420, .8),
               tufts([(320, 470), (500, 455), (720, 470), (60, 580), (420, 590), (680, 585)]),
               hibiscus([(250, 440), (690, 440), (40, 470), (760, 500)])])


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/juanbobo-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def squeal_marks(x: float, y: float, s: float = 1) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">' + stroke("M0 -30 l18 -14 M6 0 h24 M0 30 l18 14", INK, 4) + '</g>'


def mud_puddle(cx: float, cy: float, front: bool) -> str:
    if not front:
        return (f'<ellipse filter="url(#p)" cx="{cx}" cy="{cy}" rx="230" ry="56" fill="{MUD_D}"/>'
                f'<ellipse cx="{cx}" cy="{cy - 4}" rx="214" ry="46" fill="{MUD}"/>')
    lip = (f'<path d="M{cx - 226} {cy + 4} Q{cx} {cy + 30} {cx + 226} {cy + 4} Q{cx + 230} {cy + 50} {cx} {cy + 58} '
           f'Q{cx - 230} {cy + 50} {cx - 226} {cy + 4}Z" fill="{MUD_D}"/>')
    blob = "".join(f'<ellipse cx="{cx + a}" cy="{cy + b}" rx="{rx}" ry="{ry}" fill="{MUD_L}" opacity=".7"/>' for a, b, rx, ry in
                   [(-150, 4, 26, 6), (120, 10, 34, 7), (-40, 22, 30, 6)])
    return lip + blob


def mud_splash(x: float, y: float, s: float = 1) -> str:
    """A crown of round mud blobs thrown up behind the puddle, with drops flying out."""
    lobes = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{MUD_L}"/>' for a, b, r in
                    [(-170, -20, 26), (-140, -60, 30), (-96, -96, 32), (-40, -116, 30), (24, -118, 30), (86, -100, 32), (136, -64, 30), (168, -22, 26)])
    drops = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{MUD}"/>' for a, b, r in
                    [(-210, -90, 9), (-170, -150, 11), (-90, -170, 8), (-10, -190, 10), (70, -176, 9), (150, -150, 11), (214, -84, 9), (-236, -30, 7), (240, -26, 7)])
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{lobes}{drops}</g>'


ALL = ITEMS

# 01 cover: Juan Bobo holds up Mamá's yellow dress beside the plain pig
svg(1, "Juan Bobo and the Pig", "Paper-cut cover: in the green hills of Puerto Rico, by a turquoise wooden house with a red tin roof, a smiling boy in a straw hat, Juan Bobo, holds up a fancy yellow dress with pink flowers. Beside him a round pink pig looks up at the dress. Palm and banana trees grow nearby, and a little white church stands on a far hill.", DAY,
    yard() + [juan(400, 520, 1, "hold", "big", "dress"), pig(610, 525, 1)])

# 02 meet Juan Bobo, Mamá and the pig
svg(2, "Juan Bobo, Mamá and the pig", "Paper-cut scene: in front of the turquoise house stand Mamá in a blue Sunday dress and a little white hat with a pink flower, Juan Bobo in his straw hat, white shirt and blue shorts, and the round pink pig, all smiling.", DAY,
    yard() + [mama(330, 520, 1), juan(470, 524, 1), pig(630, 530, 1)])

# 03 Mamá goes to church: "Watch the pig!"
svg(3, "Watch the pig!", "Paper-cut scene: Mamá, in her blue Sunday dress and white hat, stands on the dirt road on her way to the little white church on the hill, raising one hand as she calls back to Juan Bobo. Juan Bobo waves goodbye from the yard, with the pink pig beside him.", DAY,
    yard() + [juan(250, 528, 1, "wave"), pig(400, 536, 1), mama(620, 470, 1, "point")])

# 04 the pig squeals: she wants to go too
svg(4, "Oink, oink! Squeal!", "Paper-cut scene: the pink pig stands with her eyes squeezed shut and her mouth wide open, squealing loudly towards the little white church on the far hill. Juan Bobo stands beside her with his mouth in a surprised O and his hands up by his face.", DAY,
    hills((560, 250, .7)) + ground(400) + [banana(60, 430, .9), tufts([(300, 480), (720, 470), (80, 590), (600, 590)]),
                                         hibiscus([(140, 470), (700, 450), (760, 520)]),
                                         juan(190, 545, 1.3, "oh", "oh"), pig(450, 550, 1.3, mood="squeal"), squeal_marks(606, 430, 1.2)])

# 05 Juan Bobo fetches Mamá's fancy yellow dress
svg(5, "A fancy yellow dress", "Paper-cut scene: by the turquoise house, Juan Bobo grins and holds up Mamá's fancy yellow dress with pink flowers and a pink sash. The pink pig looks up at it with a happy smile.", DAY,
    yard() + [juan(370, 545, 1.2, "hold", "big", "dress"), pig(610, 550, 1.2)])


def dressing(n: int, title: str, desc: str, items: tuple, hands: str, held: str, glints: list) -> None:
    svg(n, title, desc, DAY, hills((660, 250, .62)) + ground(400, road=False) + [
        casita(110, 430, .85), banana(290, 430, .8), tufts([(330, 480), (720, 470), (60, 590), (600, 590)]),
        hibiscus([(270, 460), (700, 452), (760, 520)]), banner(items),
        juan(220, 560, 1.25, hands, "big", held), pig(510, 562, 1.4, items, mood="happy")] + [sparkle(a, b, .9) for a, b in glints])


# 06 dress
dressing(6, "Dress!", "Paper-cut scene: the pink pig now wears Mamá's fancy yellow dress with pink and white flowers, a ruffled hem and a big pink bow on her back, and smiles proudly. Juan Bobo points at her with a big grin. Across the top a little paper list shows one thing: a yellow dress.",
         ("dress",), "present", "", [(430, 400), (600, 470)])
# 07 earrings and necklace
dressing(7, "Earrings and a necklace!", "Paper-cut scene: the pig in the yellow dress now also wears gold hoop earrings by her ears and a long necklace of white pearls around her neck. Juan Bobo points at her, grinning. The paper list at the top shows a dress, gold earrings and a pearl necklace.",
         ("dress", "earrings", "necklace"), "present", "", [(640, 400), (520, 430)])
# 08 lipstick
dressing(8, "Lipstick!", "Paper-cut scene: the pig in the yellow dress, gold earrings and pearl necklace now has bright red lipstick on her smile. Juan Bobo holds up the lipstick, grinning. The paper list at the top shows a dress, earrings, a necklace and a lipstick.",
         ("dress", "earrings", "necklace", "lipstick"), "hold", "lipstick", [(660, 480)])
# 09 high-heeled shoes, all four
dressing(9, "And SHOES!", "Paper-cut scene: the pig, in her yellow dress, gold earrings, pearl necklace and red lipstick, now stands up on red high-heeled shoes, one on each of her four feet. Juan Bobo points at her, grinning. The paper list at the top shows all five things: dress, earrings, necklace, lipstick and shoes.",
         ALL, "present", "", [(430, 560), (600, 560)])

# 10 off to church, click-clack down the road
svg(10, "Off to church!", "Paper-cut scene: the pig, all dressed up in her yellow dress, earrings, pearls, lipstick and red high-heeled shoes, trots happily along the dirt road towards the little white church on the hill. Juan Bobo waves goodbye from beside the turquoise house.", DAY,
    yard(110) + [juan(260, 540, 1, "wave", "big"), pig(560, 470, 1, ALL, pose="trot"),
                 stroke("M486 444 l-16 4 M488 430 l-18 0", INK, 3)])

# 11 SPLASH! into the mud puddle
svg(11, "SPLASH!", "Paper-cut scene: SPLASH! Beside the dirt road, the pig in her yellow dress and pearls has jumped right into a big brown mud puddle. Mud flies up all around her and there are brown splotches all over her dress and face, and she is grinning with her eyes shut in joy. The little white church is on the hill behind.", DAY,
    hills((560, 250, .62)) + ground(400) + [banana(80, 440, .9), palm(740, 420, .9, -1), tufts([(70, 590), (720, 590)]),
                                         mud_puddle(400, 500, False), mud_splash(400, 470, 1),
                                         pig(390, 574, 1.4, ALL, mood="joy", mud=True, legs=False), mud_puddle(400, 500, True)])

# 12 Mamá comes home and laughs
svg(12, "Mamá laughs", "Paper-cut scene: back home by the turquoise house, Mamá in her blue Sunday dress laughs with her eyes crinkled and her hands together at her chest. Juan Bobo scratches his head under his straw hat with a sheepish smile. The pig stands beside them, splotched all over with mud on her yellow dress, pearls and red shoes, smiling.", DAY,
    yard() + [juan(190, 532, 1, "sheepish", "sheepish"), mama(380, 528, 1, "laugh", "laugh"), pig(610, 536, 1, ALL, mud=True)])

# 13 scrub-a-dub: everyone washes the pig
tub = (f'<g filter="url(#p)"><path d="M300 470 L560 470 L540 560 L320 560Z" fill="{TUB}"/><rect x="292" y="462" width="276" height="18" rx="9" fill="{TUB_D}"/>'
       + stroke("M318 510 H542 M326 540 H534", TUB_D, 3) + '</g>')
suds = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="#fff" opacity=".95"/>' for a, b, r in
               [(310, 462, 18), (340, 452, 22), (376, 462, 18), (414, 456, 18), (446, 466, 14), (556, 458, 14), (430, 350, 9), (456, 330, 6), (404, 334, 7)])
line = (stroke("M40 170 Q170 188 300 172", "#8A7A6A", 2.5) + stroke("M40 170 V420 M300 172 V420", WOOD_D, 6)
        + dress_obj(170, 180, .75) + stroke("M156 178 v-8 M184 178 v-8", WOOD_D, 3))
water = stroke("M584 418 Q560 430 548 462", WATER, 9) + "".join(f'<circle cx="{a}" cy="{b}" r="5" fill="{WATER}"/>' for a, b in [(536, 452), (562, 450), (528, 466)])
svg(13, "Scrub-a-dub!", "Paper-cut scene in warm evening light: the clean pink pig sits in a big tin washtub full of white soap bubbles, grinning with her eyes shut. Juan Bobo scrubs her with a wooden brush, and Mamá pours water from a bucket. The yellow dress hangs drying on a washing line behind them.", GOLDEN,
    hills((0, 0, 0)) + ground(400, road=False) + [palm(740, 410, .9, -1), line,
                                                    pig(410, 538, 1.3, mood="joy", legs=False), tub, suds,
                                                    juan(220, 560, 1, "scrub", "laugh", "brush"), mama(700, 560, 1, "pour", "laugh"), water])
