#!/usr/bin/env python3
"""Generates the 13 Town-Musicians-of-Bremen flip-book SVGs from shared character parts.

Usage: python3 bremen_gen.py <output-dir>
Scale rule: every figure is drawn at its own natural size times one page-wide k, so the donkey is always
the biggest animal, then the dog, then the cat and the rooster; the robbers are about donkey-head height.
Each animal keeps one colour on every page: grey donkey, brown dog, ginger cat, white rooster with a green tail.
Stack rule (page 08/09): each animal's feet sit on the flat top of the back below it.
  donkey back top = -146, dog back top = -72 (+ its feet), cat back top = -48 (+ its feet).
House geometry (pages 07-13) is fixed: wall x 420..760, y 190..520, window x 450..620 / y 250..390, door x 650..730.
"""
import math
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
DONK, DONK_D, DONK_L, MANE = "#A39C94", "#7A726B", "#E6E0D8", "#4E4640"
DOG, DOG_D, DOG_L = "#A8703F", "#7A4E2B", "#F0DBBA"
CAT, CAT_D, CAT_L = "#EE9A3C", "#BF6A20", "#FCE6C6"
HEN, HEN_D, COMB, BEAK, TAIL, TAIL2 = "#FBF6EC", "#D8CCB6", "#E0372D", "#F2B632", "#1F6B66", "#36A27A"
SKIN, SHIRT, SHIRT2, TROUS, HAT, STACHE = "#F0C8A0", "#3C4A6B", "#EFE7D6", "#6A5240", "#3A3330", "#5A3B22"
WALL, BEAM, ROOF, ROOF_D = "#F3E6C8", "#8A5A36", "#B5523B", "#8E3A2A"
LAMP, LAMP_L, EMBER = "#FFC860", "#FFE6A6", "#F26B3A"
GRASS, GRASS_D, GRASS_L, ROAD, ROAD_D = "#6CBF5E", "#3F9A56", "#9AD67F", "#E3C894", "#C8A56E"
NGRASS, NGRASS_D, NTREE = "#3D5E4A", "#2C4838", "#203A30"
DAY = [(0, "#7CCBE8"), (1, "#EAF6FB")]
DUSK = [(0, "#5D6FB0"), (.55, "#E99A8C"), (1, "#FAD3A0")]
NIGHT = [(0, "#141B3C"), (1, "#3A4A7A")]
GOLDEN = [(0, "#8FCFEA"), (.6, "#FDE7C0"), (1, "#FCD9A0")]


def stroke(d: str, col: str = INK, w: float = 5, op: float = 1) -> str:
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{o}/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, shadow: bool = True, rot: float = 0) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def eye(x: float, y: float, r: float = 4.5, shut: bool = False, wide: bool = False) -> str:
    if shut:
        return stroke(f"M{x - r} {y} q{r} {r} {2 * r} 0", INK, 2.4)
    rr = r * (1.25 if wide else 1)
    return f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#fff"/><circle cx="{x + r * .3}" cy="{y}" r="{rr * .55}" fill="{INK}"/>'


# ---------------------------------------------------------------- the donkey (biggest)
def donkey_head(mood: str) -> str:
    out = (f'<g transform="rotate(-14 -8 -12)"><ellipse cx="-8" cy="-36" rx="8" ry="26" fill="{DONK}"/>'
           f'<ellipse cx="-8" cy="-34" rx="4" ry="18" fill="#E7B9B0"/><ellipse cx="-8" cy="-58" rx="6" ry="6" fill="{MANE}"/></g>'
           f'<g transform="rotate(14 6 -12)"><ellipse cx="6" cy="-36" rx="8" ry="26" fill="{DONK}"/>'
           f'<ellipse cx="6" cy="-34" rx="4" ry="18" fill="#E7B9B0"/><ellipse cx="6" cy="-58" rx="6" ry="6" fill="{MANE}"/></g>')
    out += f'<ellipse rx="21" ry="18" fill="{DONK}"/><ellipse cx="22" cy="14" rx="21" ry="16" fill="{DONK_L}"/>'
    out += f'<circle cx="35" cy="10" r="2.6" fill="{INK}"/><circle cx="-6" cy="8" r="4.5" fill="#F0705F" opacity=".4"/>'
    out += eye(5, -4, 5, shut=mood == "sleep", wide=mood == "wide")
    if mood == "sing":
        out += f'<ellipse cx="30" cy="27" rx="9" ry="7" fill="#5A2E22"/>'
    elif mood == "sad":
        out += stroke("M20 28 q8 -5 16 0", INK, 2.4) + stroke("M-2 -14 L10 -10", INK, 2.4)
    else:
        out += stroke("M20 25 q8 5 16 -1", INK, 2.4)
    return out


def donkey(x: float, y: float, k: float = 1, flip: bool = False, pose: str = "stand", mood: str = "smile",
           sacks: bool = False, head_rot: float | None = None) -> str:
    """Grey donkey in side view facing right. (x, y) is the hooves. Back top is flat at -146 (stand/walk)."""
    dy = 64 if pose == "lie" else 0
    out = ""
    if pose == "lie":
        out += "".join(f'<ellipse cx="{a}" cy="-10" rx="20" ry="9" fill="{DONK_D}"/>' for a in (-44, 40))
    else:
        legs = ("M-46 -90 L-58 -6 M-30 -90 L-24 -4 M34 -90 L28 -4 M50 -90 L62 -8" if pose == "walk"
                else "M-46 -90 V-4 M-30 -90 V-4 M34 -90 V-4 M50 -90 V-4")
        feet = ((-58, -4), (-24, -2), (28, -2), (62, -6)) if pose == "walk" else ((-46, -2), (-30, -2), (34, -2), (50, -2))
        out += stroke(legs, DONK_D, 13)
        out += "".join(f'<rect x="{a - 8}" y="{b - 6}" width="16" height="9" rx="3" fill="{MANE}"/>' for a, b in feet)
    out += stroke(f"M-70 {-128 + dy} Q-88 {-110 + dy} -86 {-74 + dy}", DONK_D, 6)
    out += f'<ellipse cx="-86" cy="{-66 + dy}" rx="7" ry="12" fill="{MANE}"/>'
    out += f'<rect x="-72" y="{-146 + dy}" width="144" height="70" rx="34" fill="{DONK}"/>'
    out += f'<ellipse cx="0" cy="{-88 + dy}" rx="50" ry="9" fill="{DONK_L}" opacity=".6"/>'
    if sacks:
        out += (f'<rect x="-46" y="{-176 + dy}" width="40" height="34" rx="10" fill="#D9B98A"/>'
                f'<rect x="0" y="{-178 + dy}" width="40" height="36" rx="10" fill="#C9A673"/>')
    out += f'<path d="M30 {-140 + dy} Q56 {-196 + dy} 92 {-196 + dy} L114 {-170 + dy} Q80 {-150 + dy} 72 {-96 + dy}Z" fill="{DONK}"/>'
    out += stroke(f"M34 {-142 + dy} Q56 {-190 + dy} 88 {-200 + dy}", MANE, 8)
    rot = head_rot if head_rot is not None else (-22 if mood == "sing" else (18 if mood == "sad" else 0))
    out += f'<g transform="translate(106 {-176 + dy}) rotate({rot})">{donkey_head(mood)}</g>'
    return group(x, y, k, flip, out)


# ---------------------------------------------------------------- the dog
def dog_head(mood: str) -> str:
    out = f'<circle r="17" fill="{DOG}"/><ellipse cx="15" cy="6" rx="14" ry="9" fill="{DOG_L}"/>'
    out += f'<circle cx="28" cy="3" r="4.2" fill="{INK}"/>'
    out += eye(3, -5, 4.2, shut=mood == "sleep", wide=mood == "wide")
    if mood in ("sing", "tired"):
        out += f'<ellipse cx="19" cy="15" rx="7" ry="5" fill="#5A2E22"/>'
        if mood == "tired":
            out += f'<ellipse cx="20" cy="21" rx="4" ry="6" fill="#F2789F"/>'
    else:
        out += stroke("M14 13 q6 4 12 0", INK, 2.2)
    out += f'<ellipse cx="-7" cy="4" rx="7" ry="15" fill="{DOG_D}" transform="rotate(18 -7 4)"/>'
    return out


def dog(x: float, y: float, k: float = 1, flip: bool = False, pose: str = "stand", mood: str = "smile") -> str:
    """Brown dog in side view facing right. (x, y) is the paws. Back top is flat at -72 (stand)."""
    out = ""
    if pose == "lie":
        out += stroke("M-34 -10 L-52 -4 M26 -12 L58 -4", DOG_D, 9)
        out += stroke("M-42 -36 Q-64 -40 -70 -24", DOG, 7)
        out += f'<rect x="-44" y="-40" width="88" height="36" rx="18" fill="{DOG}"/>'
        out += f'<ellipse cx="26" cy="-14" rx="16" ry="9" fill="{DOG_L}" opacity=".8"/>'
        out += f'<g transform="translate(52 -26)">{dog_head(mood)}</g>'
        return group(x, y, k, flip, out)
    out += stroke("M-30 -40 V-4 M-18 -40 V-4 M20 -40 V-4 M32 -40 V-4", DOG_D, 9)
    out += "".join(f'<ellipse cx="{a + 2}" cy="-3" rx="7" ry="4" fill="{DOG_D}"/>' for a in (-30, -18, 20, 32))
    out += stroke("M-42 -62 Q-62 -76 -58 -100", DOG, 7)
    out += f'<rect x="-44" y="-72" width="88" height="42" rx="20" fill="{DOG}"/>'
    out += f'<ellipse cx="28" cy="-44" rx="14" ry="11" fill="{DOG_L}" opacity=".85"/>'
    out += f'<path d="M22 -70 Q34 -88 44 -90 L54 -72 Q42 -62 38 -46Z" fill="{DOG}"/>'
    rot = -24 if mood == "sing" else 0
    out += f'<g transform="translate(46 -84) rotate({rot})">{dog_head(mood)}</g>'
    return group(x, y, k, flip, out)


# ---------------------------------------------------------------- the cat
def cat_head(mood: str) -> str:
    out = (f'<path d="M-13 -6 L-12 -27 L1 -13Z M-1 -13 L12 -27 L13 -6Z" fill="{CAT}"/>'
           f'<path d="M-10 -10 L-10 -21 L-3 -13Z M3 -13 L10 -21 L10 -10Z" fill="#F2A7A0"/>'
           f'<circle r="15" fill="{CAT}"/>' + stroke("M-4 -14 l1 6 M4 -14 l-1 6", CAT_D, 2.4)
           + f'<ellipse cy="7" rx="9" ry="6" fill="{CAT_L}"/>')
    if mood == "glow":  # just two shining eyes in the dark
        out += '<ellipse cx="-6" cy="-2" rx="4.5" ry="5" fill="#E9FF7A"/><ellipse cx="6" cy="-2" rx="4.5" ry="5" fill="#E9FF7A"/>'
        out += f'<ellipse cx="-6" cy="-2" rx="1.4" ry="4" fill="{INK}"/><ellipse cx="6" cy="-2" rx="1.4" ry="4" fill="{INK}"/>'
    else:
        out += eye(-6, -2, 3.6, shut=mood == "sleep", wide=mood == "wide") + eye(6, -2, 3.6, shut=mood == "sleep", wide=mood == "wide")
    out += '<path d="M-2.5 4 h5 l-2.5 3Z" fill="#E36A7A"/>'
    if mood == "sing":
        out += f'<ellipse cy="11" rx="4" ry="4" fill="#5A2E22"/>'
    elif mood == "sad":
        out += stroke("M-4 12 q4 -3 8 0", INK, 1.8) + stroke("M-10 -8 l6 2 M10 -8 l-6 2", INK, 1.8)
    else:
        out += stroke("M-4 9 q2 3 4 0 q2 3 4 0", INK, 1.6)
    out += stroke("M-8 6 h-12 M-8 9 l-11 4 M8 6 h12 M8 9 l11 4", INK, 1.2, .7)
    return out


def cat(x: float, y: float, k: float = 1, flip: bool = False, pose: str = "stand", mood: str = "smile") -> str:
    """Ginger striped cat facing right (face turned to us). (x, y) is the paws. Back top is flat at -48 (stand)."""
    out = ""
    if pose == "sit":
        out += stroke("M12 -6 Q36 -4 34 -22", CAT, 7)
        out += f'<ellipse cy="-28" rx="20" ry="27" fill="{CAT}"/><ellipse cx="4" cy="-22" rx="10" ry="16" fill="{CAT_L}"/>'
        out += stroke("M-14 -40 q6 3 10 0 M-16 -28 q6 3 10 0", CAT_D, 2.6)
        out += stroke("M-6 -18 V-3 M8 -18 V-3", CAT, 7)
        out += f'<g transform="translate(2 -62)">{cat_head(mood)}</g>'
        return group(x, y, k, flip, out)
    if pose == "curl":
        out += f'<ellipse cy="-16" rx="34" ry="16" fill="{CAT}"/>' + stroke("M-30 -6 Q0 6 30 -4", CAT_D, 6)
        out += stroke("M-14 -30 q4 8 0 14 M2 -32 q4 8 0 14", CAT_D, 2.6)
        out += f'<g transform="translate(26 -20) scale(.9)">{cat_head(mood)}</g>'
        return group(x, y, k, flip, out)
    out += stroke("M-20 -26 V-3 M-12 -26 V-3 M14 -26 V-3 M22 -26 V-3", CAT, 7)
    out += stroke("M-28 -38 Q-52 -38 -56 -52 Q-58 -62 -50 -64", CAT_D, 8) + stroke("M-28 -38 Q-52 -38 -56 -52 Q-58 -62 -50 -64", CAT, 5)
    out += f'<rect x="-30" y="-48" width="60" height="28" rx="14" fill="{CAT}"/>'
    out += stroke("M-16 -47 v8 M-4 -48 v9 M8 -47 v8", CAT_D, 2.8)
    out += f'<ellipse cx="18" cy="-26" rx="9" ry="5" fill="{CAT_L}"/>'
    rot = -10 if mood == "sing" else 0
    out += f'<g transform="translate(34 -54) rotate({rot})">{cat_head(mood)}</g>'
    return group(x, y, k, flip, out)


# ---------------------------------------------------------------- the rooster
def rooster(x: float, y: float, k: float = 1, flip: bool = False, mood: str = "smile") -> str:
    """White rooster with a red comb and a green tail, facing right. (x, y) is his toes."""
    out = stroke("M-5 -26 V-2 M7 -26 V-2", BEAK, 4) + stroke("M-12 -1 h12 M0 -1 h14", BEAK, 3)
    out += (f'<path d="M-14 -50 Q-44 -104 -58 -86 Q-42 -72 -22 -40Z" fill="{TAIL}"/>'
            f'<path d="M-16 -46 Q-56 -82 -62 -60 Q-44 -54 -22 -36Z" fill="{TAIL2}"/>'
            f'<path d="M-12 -54 Q-26 -108 -42 -98 Q-30 -82 -18 -46Z" fill="{TAIL2}"/>')
    out += f'<ellipse cy="-42" rx="24" ry="19" fill="{HEN}"/><ellipse cx="-3" cy="-42" rx="15" ry="9" fill="{HEN_D}"/>'
    out += f'<path d="M6 -54 Q12 -70 16 -78 L30 -72 Q26 -54 20 -40Z" fill="{HEN}"/>'
    rot = -30 if mood == "crow" else 0
    head = (f'<path d="M-8 -6 L-6 -18 L-1 -11 L3 -22 L7 -12 L12 -18 L10 -4Z" fill="{COMB}"/>'
            f'<circle r="10" fill="{HEN}"/><ellipse cx="7" cy="12" rx="4" ry="6" fill="{COMB}"/>')
    if mood in ("crow", "sing"):
        head += f'<path d="M8 -3 L22 -4 L9 1Z M8 3 L20 8 L8 5Z" fill="{BEAK}"/>'
    else:
        head += f'<path d="M8 -3 L21 1 L8 5Z" fill="{BEAK}"/>'
    head += eye(2, -2, 3, shut=mood == "sleep", wide=mood == "wide")
    out += f'<g transform="translate(22 -78) rotate({rot})">{head}</g>'
    return group(x, y, k, flip, out)


# ---------------------------------------------------------------- a comic robber (round, stripy, a little silly)
def stripes(cy: float, rx: float, ry: float) -> str:
    out = ""
    for yy in range(int(cy - ry) + 10, int(cy + ry) - 4, 14):
        half = rx * math.sqrt(max(0, 1 - ((yy - cy) / ry) ** 2)) - 2
        out += f"M{-half:.0f} {yy} H{half:.0f} "
    return stroke(out, SHIRT2, 6)


ROBBER_ARMS = {
    "feast": ("M-32 -106 Q-60 -90 -50 -64", "M32 -106 Q64 -120 58 -150", (-50, -64), (58, -150)),
    "up": ("M-32 -106 Q-62 -130 -64 -168", "M32 -106 Q62 -130 64 -168", (-64, -168), (64, -168)),
    "tiptoe": ("M-32 -106 Q-56 -110 -36 -142", "M32 -106 Q66 -100 70 -124", (-36, -142), (70, -124)),
}


def robber(x: float, y: float, k: float = 1, pose: str = "feast", mood: str = "grin", hat: str = "on",
           tone: str = SHIRT, shadow: bool = True, lean: float = 0) -> str:
    """A round, stripy robber facing us. (x, y) is his boots. pose: feast / up (running away) / tiptoe."""
    a1, a2, h1, h2 = ROBBER_ARMS["up" if pose == "run" else pose]
    if pose == "run":
        out = stroke("M-14 -50 L-36 -6 M14 -50 L34 -14", TROUS, 15)
        out += f'<ellipse cx="-40" cy="-4" rx="16" ry="8" fill="{HAT}"/><ellipse cx="40" cy="-12" rx="16" ry="8" fill="{HAT}" transform="rotate(-20 40 -12)"/>'
    elif pose == "tiptoe":
        out = stroke("M-14 -50 L-22 -8 M14 -50 L26 -14", TROUS, 15)
        out += f'<ellipse cx="-24" cy="-5" rx="13" ry="7" fill="{HAT}"/><ellipse cx="30" cy="-12" rx="13" ry="7" fill="{HAT}" transform="rotate(-30 30 -12)"/>'
    else:
        out = stroke("M-14 -50 V-8 M14 -50 V-8", TROUS, 15)
        out += f'<ellipse cx="-18" cy="-5" rx="16" ry="8" fill="{HAT}"/><ellipse cx="18" cy="-5" rx="16" ry="8" fill="{HAT}"/>'
    out += f'<ellipse cy="-88" rx="38" ry="42" fill="{tone}"/>' + stripes(-88, 38, 42)
    out += f'<rect x="-38" y="-58" width="76" height="9" rx="4" fill="{STACHE}"/><rect x="-6" y="-60" width="12" height="13" rx="2" fill="#E8C35A"/>'
    out += stroke(a1, tone, 13) + stroke(a2, tone, 13)
    out += "".join(f'<circle cx="{a}" cy="{b}" r="8" fill="{SKIN}"/>' for a, b in (h1, h2))
    if pose == "feast":  # a big drumstick to wave about
        out += f'<g transform="translate({h2[0]} {h2[1]}) rotate(-20)"><rect x="-3" y="-4" width="6" height="16" rx="3" fill="#FFF6E6"/><ellipse cy="-14" rx="10" ry="13" fill="#C7792F"/></g>'
    if pose == "tiptoe":  # a little candle
        out += (f'<g transform="translate({h2[0]} {h2[1]})"><rect x="-5" y="-26" width="10" height="22" rx="2" fill="#FFF6E6"/>'
                f'<path d="M0 -42 q7 8 0 14 q-7 -6 0 -14Z" fill="{LAMP}"/><circle cy="-34" r="14" fill="{LAMP_L}" opacity=".35"/></g>')
    head = f'<circle r="25" fill="{SKIN}"/><ellipse cx="-24" cy="2" rx="5" ry="7" fill="{SKIN}"/><ellipse cx="24" cy="2" rx="5" ry="7" fill="{SKIN}"/>'
    head += f'<rect x="-24" y="-12" width="48" height="13" rx="6" fill="{INK}"/>'
    wide = mood in ("scared", "oh")
    head += eye(-10, -6, 4, wide=wide) + eye(10, -6, 4, wide=wide)
    if wide:
        head += stroke("M-16 -20 q6 -6 12 0 M4 -20 q6 -6 12 0", STACHE, 3)
    head += f'<ellipse cy="5" rx="6" ry="5" fill="#E2A27E"/>'
    head += f'<path d="M-2 10 Q-12 6 -20 14 Q-10 16 -2 13 Q0 15 2 13 Q10 16 20 14 Q12 6 2 10Z" fill="{STACHE}"/>'
    if wide:
        head += f'<ellipse cy="19" rx="5" ry="5" fill="#5A2E22"/>'
    elif mood == "shh":
        head += stroke("M-5 19 h10", "#5A2E22", 2.4)
    else:
        head += f'<path d="M-8 17 Q0 25 8 17Z" fill="#5A2E22"/>'
    if hat == "on":
        head += f'<path d="M-28 -12 Q-30 -44 0 -46 Q24 -46 36 -30 Q44 -18 30 -14 Q4 -22 -28 -12Z" fill="{HAT}"/><ellipse cx="0" cy="-12" rx="32" ry="6" fill="{HAT}"/>'
    out += f'<g transform="translate(0 -150)">{head}</g>'
    if hat == "fly":
        out += (f'<g transform="translate(26 -232) rotate(28)"><path d="M-28 -12 Q-30 -44 0 -46 Q24 -46 36 -30 Q44 -18 30 -14 Q4 -22 -28 -12Z" fill="{HAT}"/>'
                f'<ellipse cx="0" cy="-12" rx="32" ry="6" fill="{HAT}"/></g>' + stroke("M-2 -200 q4 -10 0 -18 M40 -196 q6 -8 4 -18", "#fff", 3))
    return group(x, y, k, False, out, shadow, lean)


# ---------------------------------------------------------------- scenery
def cloud(x: float, y: float, s: float = 1, op: float = .92, col: str = "#fff") -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{col}" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def tree(x: float, y: float, s: float = 1, col: str = GRASS_D, trunk: str = BEAM) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><rect x="-8" y="-60" width="16" height="60" fill="{trunk}"/>'
            f'<circle cy="-90" r="40" fill="{col}"/><circle cx="-30" cy="-66" r="28" fill="{col}"/><circle cx="30" cy="-66" r="28" fill="{col}"/></g>')


def pine(x: float, y: float, s: float = 1, col: str = NTREE) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-5" y="-16" width="10" height="16" fill="#1A2A24"/>'
            f'<path d="M0 -130 L-30 -70 L-16 -72 L-40 -30 L-20 -32 L-46 -14 L46 -14 L20 -32 L40 -30 L16 -72 L30 -70Z" fill="{col}"/></g>')


def stars(pts: list) -> str:
    return "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="#FFF6D6" opacity=".9"/>' for a, b, r in pts)


def moon(x: float, y: float) -> str:
    return f'<circle cx="{x}" cy="{y}" r="34" fill="#FFF3C4"/><circle cx="{x + 16}" cy="{y - 8}" r="30" fill="url(#sky)"/>'


def notes(pts: list, col: str = "#fff") -> str:
    """Little music notes; each point is (x, y, scale, tilt)."""
    out = ""
    for a, b, s, r in pts:
        out += (f'<g transform="translate({a} {b}) rotate({r}) scale({s})" fill="{col}" filter="url(#p)">'
                '<ellipse cx="-4" cy="10" rx="9" ry="7" transform="rotate(-20 -4 10)"/><rect x="3" y="-24" width="4" height="34"/>'
                '<path d="M3 -24 q16 6 14 20 q-4 -10 -14 -12Z"/></g>')
    return out


def burst(x: float, y: float, r: float, col: str, n: int = 9) -> str:
    """A spiky 'loud noise' burst, in the colour of the animal making the noise."""
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * .62
        pts.append(f"{x + rr * math.cos(a):.0f} {y + rr * math.sin(a):.0f}")
    return f'<path d="M{" L".join(pts)}Z" fill="{col}" stroke="#fff" stroke-width="4" stroke-linejoin="round" filter="url(#p)"/>'


def rain_cloud(x: float, y: float) -> str:
    return cloud(x, y, .55, 1, "#A9B4C8") + stroke(f"M{x - 22} {y + 30} l-4 12 M{x - 4} {y + 32} l-4 12 M{x + 14} {y + 30} l-4 12", "#6FA8DC", 3)


def zzz(x: float, y: float, s: float = 1) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" opacity=".85">'
            + stroke("M0 0 h10 l-10 12 h10 M16 -16 h8 l-8 10 h8 M28 -30 h6 l-6 8 h6", "#DDE6FF", 2.6) + '</g>')


def signpost(x: float, y: float) -> str:
    """A wooden signpost with an arrow pointing right and a tiny town (towers and roofs) painted on it: the way to Bremen."""
    town = (f'<rect x="20" y="-24" width="12" height="20" fill="{ROOF}"/><path d="M18 -24 L26 -38 L34 -24Z" fill="{ROOF_D}"/>'
            f'<rect x="38" y="-18" width="16" height="14" fill="{ROOF}"/><path d="M36 -18 L46 -28 L56 -18Z" fill="{ROOF_D}"/>'
            f'<rect x="60" y="-30" width="10" height="26" fill="{ROOF}"/><path d="M58 -30 L65 -46 L72 -30Z" fill="{ROOF_D}"/>')
    return (f'<g transform="translate({x} {y})" filter="url(#p)"><rect x="-7" y="-150" width="14" height="150" fill="{BEAM}"/>'
            f'<path d="M-6 -150 H84 L104 -126 L84 -102 H-6Z" fill="#E9C98E"/><g transform="translate(0 -110)">{town}</g></g>')


def day_land(ground: float = 470) -> list:
    return [cloud(160, 90, 1), cloud(620, 70, .9),
            f'<path d="M0 {ground - 120} Q200 {ground - 190} 420 {ground - 130} T800 {ground - 140} V{ground} H0Z" fill="{GRASS_L}"/>',
            tree(700, ground - 110, .7), tree(90, ground - 120, .6),
            f'<path filter="url(#p)" d="M0 {ground - 30} Q400 {ground - 60} 800 {ground - 30} V600 H0Z" fill="{GRASS}"/>',
            f'<path d="M0 {ground + 10} Q400 {ground - 14} 800 {ground + 10} V{ground + 80} Q400 {ground + 60} 0 {ground + 80}Z" fill="{ROAD}"/>',
            stroke(f"M60 {ground + 40} h40 M260 {ground + 30} h30 M520 {ground + 34} h40 M700 {ground + 44} h30", ROAD_D, 4)]


def flowers(pts: list) -> str:
    out = ""
    for i, (a, b) in enumerate(pts):
        col = ("#F7D046", "#F2789F", "#FFFFFF", "#B48BE8")[i % 4]
        out += (f'<g transform="translate({a} {b})"><circle cx="-4" r="3.6" fill="{col}"/><circle cx="4" r="3.6" fill="{col}"/>'
                f'<circle cy="-4" r="3.6" fill="{col}"/><circle cy="4" r="3.6" fill="{col}"/><circle r="2.4" fill="#E58A2B"/></g>')
    return out


# ---------------------------------------------------------------- the robbers' house (fixed geometry)
WIN = (450, 250, 170, 140)  # x, y, w, h
DOOR = (650, 380, 80, 140)


def house(window: str = "dark", inside: str = "", door: str = "shut", smoke: bool = False, day: bool = False) -> list:
    wx, wy, ww, wh = WIN
    dx, dy, dw, dh = DOOR
    pane = {"lit": LAMP, "dark": "#26304F", "ember": "#3A2C3A"}[window]
    out = [f'<path filter="url(#p)" d="M396 198 L590 52 L784 198Z" fill="{ROOF}"/>',
           stroke("M450 160 H730 M500 122 H680 M548 88 H632", ROOF_D, 4, .6),
           f'<rect filter="url(#p)" x="676" y="70" width="34" height="80" fill="{ROOF_D}"/>']
    if smoke:
        out.append('<g fill="#fff" opacity=".8"><circle cx="694" cy="67" r="12"/><circle cx="706" cy="45" r="15"/><circle cx="690" cy="23" r="13"/></g>')
    out.append(f'<rect filter="url(#p)" x="420" y="190" width="340" height="330" fill="{WALL if day else "#C9BBA0"}"/>')
    out.append(stroke("M420 190 V520 M760 190 V520 M420 194 H760 M420 230 H760 M640 230 V520 M740 230 V520", BEAM, 8))
    out.append(f'<rect x="{wx - 8}" y="{wy - 8}" width="{ww + 16}" height="{wh + 16}" rx="6" fill="{BEAM}"/>')
    out.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{pane}"/>')
    if inside:
        out.append(f'<g clip-path="url(#win)">{inside}</g>')
    out.append(stroke(f"M{wx + ww / 2} {wy} V{wy + wh}", BEAM, 5))
    out.append(f'<rect x="{wx - 14}" y="{wy + wh + 4}" width="{ww + 28}" height="10" rx="3" fill="{BEAM}"/>')
    if door == "open":
        out.append(f'<path d="M{dx} {dy + 40} Q{dx + dw / 2} {dy - 6} {dx + dw} {dy + 40} V{dy + dh} H{dx}Z" fill="{LAMP if window == "lit" else "#1E2440"}"/>')
        out.append(f'<path d="M{dx + dw} {dy + 40} L{dx + dw + 22} {dy + 30} V{dy + dh + 6} L{dx + dw} {dy + dh}Z" fill="{ROOF_D}"/>')
    else:
        out.append(f'<path d="M{dx} {dy + 40} Q{dx + dw / 2} {dy - 6} {dx + dw} {dy + 40} V{dy + dh} H{dx}Z" fill="{ROOF_D}"/>')
        out.append(stroke(f"M{dx + dw / 2} {dy + 20} V{dy + dh}", "#6E2C20", 3) + f'<circle cx="{dx + dw - 14}" cy="{dy + 84}" r="4" fill="#E8C35A"/>')
    return out


def feast(scared: bool = False) -> str:
    """What you see through the lit window: robbers round a table of good food."""
    wx, wy, ww, wh = WIN
    out = f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{LAMP}"/><circle cx="{wx + 85}" cy="{wy + 30}" r="60" fill="{LAMP_L}" opacity=".6"/>'
    if not scared:  # once the robbers have run off, the room is empty and the food is left on the table
        out += (robber(wx + 40, wy + 150, .62, "feast", "grin", "on", SHIRT, False)
                + robber(wx + 126, wy + 152, .62, "feast", "grin", "on", "#6B3C4A", False))
    out += (f'<rect x="{wx - 4}" y="{wy + 108}" width="{ww + 8}" height="40" fill="{BEAM}"/>'
            f'<ellipse cx="{wx + 50}" cy="{wy + 104}" rx="22" ry="12" fill="#C7792F"/><ellipse cx="{wx + 50}" cy="{wy + 109}" rx="28" ry="5" fill="#fff"/>'
            f'<ellipse cx="{wx + 118}" cy="{wy + 102}" rx="20" ry="11" fill="#E0B36A"/>'
            f'<rect x="{wx + 80}" y="{wy + 82}" width="14" height="26" rx="4" fill="#8E5BB0"/><circle cx="{wx + 150}" cy="{wy + 102}" r="7" fill="#E5344A"/>')
    return out


def night_ground(extra: str = "") -> list:
    return [stars([(40, 40, 2), (130, 90, 1.6), (240, 30, 2), (330, 110, 1.5), (60, 170, 1.6), (370, 50, 2.2), (300, 180, 1.4), (720, 30, 1.8), (780, 120, 1.6)]),
            moon(180, 120),
            pine(40, 470, 1.2), pine(130, 440, .9), pine(330, 450, 1), pine(780, 470, 1.1),
            f'<path filter="url(#p)" d="M0 480 Q400 470 800 486 V600 H0Z" fill="{NGRASS}"/>',
            f'<path d="M0 560 Q300 530 640 540 L800 534 V600 H0Z" fill="{NGRASS_D}" opacity=".6"/>', extra]


def svg(n: int, title: str, desc: str, stops: list, body: list, win_clip: bool = False) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    wx, wy, ww, wh = WIN
    clip = f'<clipPath id="win"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/></clipPath>' if 'url(#win)' in joined else ""
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{clip}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/bremen-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def stack(x: float, y: float, k: float = 1, mood: str = "smile") -> list:
    """THE picture: dog on the donkey's back, cat on the dog's back, rooster on the cat's back — four animals, four feet-levels."""
    m = {"smile": ("smile",) * 4, "sing": ("sing", "sing", "sing", "crow")}[mood]
    dog_y = y - 146 * k
    cat_y = dog_y - 72 * k
    roo_y = cat_y - 48 * k
    return [donkey(x, y, k, mood=m[0], head_rot=8), dog(x - 12 * k, dog_y, k, mood=m[1]), cat(x - 12 * k, cat_y, k, mood=m[2]),
            rooster(x - 20 * k, roo_y, k, mood=m[3])]


# 01 cover: four friends on the road to Bremen
svg(1, "The Town Musicians of Bremen", "Paper-cut cover: on a sunny country road, four animals walk in a line to the right — a grey donkey, a brown dog, a ginger striped cat and a white rooster with a red comb and a green tail — towards a wooden signpost with an arrow pointing the way, painted with a tiny town of towers and red roofs. Little music notes float above them.", DAY, [
    *day_land(470), signpost(682, 500),
    donkey(150, 500, 1, pose="walk"), dog(380, 506, 1), cat(500, 510, 1), rooster(612, 512, 1),
    notes([(250, 200, 1, -10), (390, 330, .8, 8), (510, 380, .7, -6), (620, 350, .7, 10)])])

# 02 the old donkey: "too old to carry the sacks"
barn = (f'<g filter="url(#p)"><path d="M30 250 L150 180 L270 250Z" fill="{ROOF_D}"/><rect x="40" y="248" width="220" height="220" fill="#C8463A"/>'
        f'<rect x="110" y="330" width="80" height="138" fill="#8E2E26"/>' + stroke("M110 330 L190 468 M190 330 L110 468", "#E9C98E", 5) + '</g>')
sacks = (f'<g filter="url(#p)"><rect x="236" y="430" width="50" height="46" rx="14" fill="#D9B98A"/><rect x="270" y="420" width="48" height="56" rx="14" fill="#C9A673"/>'
         f'<rect x="250" y="390" width="46" height="44" rx="14" fill="#E3C79A"/></g>')
svg(2, "The old donkey sets off", "Paper-cut scene: outside a red barn, beside a little pile of grain sacks, a grey donkey with a pale grey muzzle sets off down the road to the right, smiling, with music notes floating up from him as he sings hee-haw.", DAY, [
    *day_land(470), barn, sacks, donkey(470, 500, 1, pose="walk", mood="sing"),
    notes([(640, 250, 1.1, -10), (690, 190, .9, 12), (600, 180, .8, 4)])])

# 03 the tired dog by the road
svg(3, "A tired old dog", "Paper-cut scene: on the country road, the grey donkey stands on the left and looks at a tired brown dog lying by the roadside on the right, panting with his pink tongue out.", DAY, [
    *day_land(470), donkey(250, 500, 1), dog(560, 508, 1.05, pose="lie", mood="tired"),
    stroke("M630 430 q10 -6 18 0 M640 412 q10 -6 18 0", "#fff", 3)])

# 04 the cat with a face like three rainy days
svg(4, "A sad old cat", "Paper-cut scene: the grey donkey and the brown dog stand on the road on the left, looking at a ginger striped cat who sits on the right with a very gloomy face and a little grey rain cloud dripping over her head.", DAY, [
    *day_land(470), donkey(180, 500, 1), dog(420, 506, 1), cat(620, 510, 1.15, pose="sit", mood="sad"), rain_cloud(626, 380)])

# 05 the rooster on the gate, crowing
gate = (f'<g filter="url(#p)"><rect x="612" y="372" width="30" height="150" fill="{BEAM}"/><rect x="740" y="372" width="30" height="150" fill="{BEAM}"/>'
        + stroke("M642 400 H740 M642 450 H740 M642 500 H740 M642 500 L740 400", "#CF9D68", 9) + '</g>')
svg(5, "A loud old rooster", "Paper-cut scene: on top of a wooden farm gate on the right, a white rooster with a red comb and a green tail stretches up his neck and crows. Below him on the road, the grey donkey, the brown dog and the ginger cat stop to listen.", DAY, [
    *day_land(470), gate, donkey(150, 500, 1), dog(360, 506, 1), cat(490, 510, 1), rooster(624, 372, 1.15, mood="crow"),
    stroke("M680 270 q14 -8 22 4 M690 248 q18 -12 30 6", "#fff", 3.5)])

# 06 night in the forest; the rooster spots a light
big_tree = (f'<g filter="url(#p)"><path d="M370 520 Q380 380 384 250 H416 Q420 380 430 520Z" fill="#5A3A26"/>'
            + stroke("M400 330 Q470 320 540 290", "#5A3A26", 18) + stroke("M400 250 Q330 220 270 210", "#5A3A26", 14) + '</g>'
            f'<g filter="url(#p)" fill="#2F5E46"><circle cx="400" cy="200" r="76"/><circle cx="300" cy="236" r="54"/><circle cx="510" cy="236" r="58"/><circle cx="560" cy="290" r="34"/></g>')
svg(6, "A light in the woods", "Paper-cut scene: in the woods at dusk, under a big tree, the grey donkey lies down on the left and the brown dog lies down on the right. The ginger cat sits out on a branch, and the white rooster stands at the very top of the tree, looking far away at a little yellow light shining between the trees.", DUSK, [
    stars([(60, 50, 1.6), (720, 40, 1.8), (640, 90, 1.4)]),
    pine(60, 470, 1, "#3B5A4A"), pine(150, 480, .8, "#3B5A4A"), pine(700, 460, 1, "#3B5A4A"), pine(780, 480, .9, "#3B5A4A"),
    f'<path d="M708 494 V464 L740 440 L772 464 V494Z" fill="#2E3A44"/><circle cx="740" cy="470" r="20" fill="#FFE6A6" opacity=".45"/><rect x="731" y="462" width="18" height="16" fill="#FFC860"/>',
    f'<path filter="url(#p)" d="M0 500 Q400 480 800 500 V600 H0Z" fill="#4E7A55"/>', big_tree,
    donkey(200, 560, 1, pose="lie", mood="sleep"), dog(560, 556, 1, pose="lie", mood="sleep"),
    cat(520, 304, .95, pose="sit"), rooster(392, 128, .95, mood="wide"),
    stroke("M452 110 q60 4 96 44", "#fff", 3, .8), stroke("M448 128 q50 10 80 46", "#fff", 3, .8)])

# 07 the donkey peeks in: robbers having a feast
svg(7, "Robbers having a feast", "Paper-cut scene at night: a timber-framed house with a red roof stands in the dark woods. Its window glows yellow, and inside two robbers in striped shirts, black eye masks and floppy hats sit at a table piled with food, one waving a drumstick. The grey donkey stands with his nose by the window, peeking in, while the brown dog, the ginger cat and the white rooster wait behind him on the grass.", NIGHT, [
    *night_ground(), *house("lit", feast()),
    donkey(300, 522, 1), dog(150, 560, .95), cat(56, 568, .9, pose="sit"), rooster(440, 576, .95)])

# 08 the plan: up they climb — THE picture
svg(8, "Up they climb!", "Paper-cut scene at night: beside the glowing window of the robbers' house, the four animals stand on each other's backs. At the bottom is the big grey donkey; the brown dog stands on the donkey's back; the ginger cat stands on the dog's back; and the white rooster with his red comb stands right on top, on the cat's back.", NIGHT, [
    *night_ground(), *house("lit", feast()), *stack(280, 528, 1)])

# 09 all together: HEE-HAW! WOOF! MEOW! COCK-A-DOODLE-DOO!
svg(9, "All together — sing!", "Paper-cut scene at night: the four animals, still standing on each other's backs by the window — donkey, dog, cat and rooster — all sing at once with their mouths wide open, and four big spiky noise-bursts in grey, brown, orange and red burst out around them. The house door has flown open and the two robbers in striped shirts tumble out, arms in the air and one hat flying off, running away.", NIGHT, [
    *night_ground(), *house("lit", feast(True), "open"), *stack(280, 528, 1, "sing"),
    burst(455, 326, 28, DONK), burst(392, 196, 24, DOG), burst(346, 128, 22, CAT), burst(326, 40, 22, COMB),
    notes([(140, 240, .9, -12), (110, 330, .8, 10), (170, 160, .7, 0)]),
    robber(530, 578, .8, "run", "scared", "fly", SHIRT, lean=-6), robber(680, 582, .8, "run", "scared", "on", "#6B3C4A", lean=6)])

# 10 lights out: everyone in their own sleeping place
embers = (f'<rect x="{WIN[0]}" y="{WIN[1]}" width="{WIN[2]}" height="{WIN[3]}" fill="#2E2436"/>'
          f'<rect x="{WIN[0] + 10}" y="{WIN[1] + 70}" width="80" height="70" fill="#4A3A40"/><ellipse cx="{WIN[0] + 50}" cy="{WIN[1] + 130}" rx="34" ry="8" fill="{EMBER}"/>'
          f'<circle cx="{WIN[0] + 50}" cy="{WIN[1] + 124}" r="40" fill="{EMBER}" opacity=".18"/>')
svg(10, "Goodnight, musicians", "Paper-cut scene at night: the robbers' house is dark now. The grey donkey lies asleep on the grass in the yard on the left, the brown dog sleeps by the front door, the ginger cat sleeps curled up by the glowing fire, which you can see through the window, and the white rooster sleeps up on the roof. Little z's float up from them.", NIGHT, [
    *night_ground(), *house("ember", embers + cat(WIN[0] + 122, WIN[1] + 138, 1.15, pose="curl", mood="sleep", flip=True)),
    donkey(190, 560, 1, pose="lie", mood="sleep"), dog(704, 556, .9, pose="lie", mood="sleep", flip=True),
    rooster(540, 128, .9, mood="sleep"), zzz(320, 430), zzz(600, 70, .8), zzz(560, 300, .7), zzz(630, 470, .8)])

# 11 one robber creeps back
eyes_dark = embers.replace(EMBER, "#7A3A30") + cat(WIN[0] + 122, WIN[1] + 138, 1.15, pose="curl", mood="glow", flip=True)
svg(11, "Creep, creep… who's there?", "Paper-cut scene at night: one robber in a striped shirt and floppy hat tiptoes towards the dark house, holding up a little candle. The donkey still sleeps on the grass on the left, the dog sleeps by the door and the rooster sleeps on the roof. In the dark window, the cat's two eyes are shining.", NIGHT, [
    *night_ground(), *house("ember", eyes_dark),
    donkey(130, 560, 1, pose="lie", mood="sleep"), dog(704, 556, .9, pose="lie", mood="sleep", flip=True),
    rooster(540, 128, .9, mood="sleep"), robber(420, 580, .95, "tiptoe", "shh", "on", SHIRT)])

# 12 HEE-HAW! WOOF! MEOW! COCK-A-DOODLE-DOO! — and away he runs
cat_wide = embers.replace(EMBER, "#7A3A30") + cat(WIN[0] + 100, WIN[1] + 138, 1, pose="sit", mood="sing", flip=True)
svg(12, "Away runs the robber!", "Paper-cut scene at night: everyone is awake and making their noise at once. The donkey stands in the yard on the left braying, the dog stands by the door barking, the cat sits in the window meowing and the rooster crows on the roof, with big spiky noise-bursts around each of them. In the middle the startled robber runs off, arms in the air and his hat flying, not hurt at all.", NIGHT, [
    *night_ground(), *house("ember", cat_wide),
    donkey(110, 540, .9, mood="sing"), dog(690, 556, .95, mood="sing", flip=True), rooster(540, 130, .9, mood="crow"),
    burst(240, 330, 26, DONK), burst(570, 404, 22, DOG), burst(640, 236, 22, CAT), burst(610, 40, 22, COMB),
    robber(380, 572, .95, "run", "scared", "fly", SHIRT, lean=-8)])

# 13 home at last (and they never got to Bremen)
svg(13, "Happy at home", "Paper-cut scene on a golden morning: smoke curls from the chimney of the cosy timber-framed house with its red roof and flowers by the door. On the grass in front, the four friends make music together in a row — the grey donkey, the brown dog, the ginger cat and the white rooster — with music notes floating up around them.", GOLDEN, [
    cloud(160, 90, 1), cloud(320, 150, .7, .8), tree(80, 420, .8), tree(330, 430, .6),
    f'<path filter="url(#p)" d="M0 470 Q400 450 800 470 V600 H0Z" fill="{GRASS}"/>',
    *house("lit", f'<rect x="{WIN[0]}" y="{WIN[1]}" width="{WIN[2]}" height="{WIN[3]}" fill="{LAMP}"/><circle cx="{WIN[0] + 85}" cy="{WIN[1] + 70}" r="50" fill="{LAMP_L}"/>', smoke=True, day=True),
    flowers([(436, 512), (460, 516), (746, 512), (640, 516), (40, 560), (300, 580), (700, 580)]),
    donkey(140, 560, 1, mood="sing"), dog(326, 566, 1, mood="sing"), cat(472, 570, 1, pose="sit", mood="sing"), rooster(584, 572, 1, mood="crow"),
    notes([(250, 300, 1, -10), (380, 400, .8, 8), (470, 420, .7, -6), (600, 400, .8, 10), (180, 240, .8, 6)])])
