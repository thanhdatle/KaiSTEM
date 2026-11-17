#!/usr/bin/env python3
"""Generates the 13 Who's-in-Rabbit's-House flip-book SVGs from shared character parts.

Usage: python3 longone_gen.py <output-dir>
Scale rule: every figure is drawn at SIZE[who] * k, and each page uses ONE k for every figure and the house,
so caterpillar < frog < rabbit < jackal < leopard < rhino < elephant on every page.
Reveal rule: the caterpillar appears only from page 11 on. Before that the doorway is always dark and empty.
"""
import math
import sys

OUT = sys.argv[1]
INK, CREAM, PINK, BLUSH = "#2B2320", "#FFF6E6", "#F2A0A8", "#F0705F"
SIZE = {"cat": .8, "frog": 1, "rabbit": .78, "jackal": .82, "leopard": .95, "rhino": .85, "elephant": 1, "house": 1}
HARE, HARE_D = "#C99A6B", "#A47648"
JACK, JACK_D, SADDLE = "#D39A55", "#A8733A", "#3A302B"
LEO, LEO_D, ROSE = "#EDB648", "#C98F2A", "#5A3A1E"
ELE, ELE_D, IVORY = "#9AA3AD", "#7C8590", "#FBF3E0"
RHI, RHI_D, HORN = "#8F887C", "#6F685D", "#D9D0BF"
FROG, FROG_D, FROG_L = "#5DBB4A", "#3E9A3A", "#B8E68A"
CAT, CAT_D, CAT_S = "#A8D545", "#7FB83A", "#F08A2C"
MUD, MUD_D, THATCH, THATCH_D, DOOR = "#B88B62", "#94694A", "#DDB45C", "#B58C3A", "#2A1E18"
GRASS, GRASS_D, GRASS_B, GREEN, GREEN_D = "#E2C46C", "#BE9C46", "#EBD58E", "#6FA84A", "#4E8A3A"
MTN, SNOW, TRUNK = "#A9B6D0", "#F7FAFF", "#7A5A3A"
DAY = [(0, "#7CCBE8"), (1, "#EAF6F8")]
GOLDEN = [(0, "#8FCFEA"), (.55, "#FDE3B4"), (1, "#F9C98E")]
GROUND = 450


def stroke(d: str, col: str = INK, w: float = 4) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, rot: float = 0, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- faces
def eye(x: float, y: float, r: float, mood: str) -> str:
    if mood == "laugh":
        return stroke(f"M{x - r} {y + 1} q{r} {-r * 1.4} {2 * r} 0", INK, max(2, r * .5))
    pr = r * (.38 if mood == "surprise" else .56)
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/><circle cx="{x + r * .22}" cy="{y}" r="{pr}" fill="{INK}"/>'
    if mood == "worry":
        out += stroke(f"M{x - r} {y - r * 1.5} L{x + r} {y - r * 2.1}", INK, max(1.8, r * .4))
    if mood == "surprise":
        out += stroke(f"M{x - r} {y - r * 1.9} q{r} {-r * .8} {2 * r} 0", INK, max(1.8, r * .4))
    return out


def mouth(x: float, y: float, w: float, mood: str) -> str:
    if mood in ("laugh", "boom"):
        h = w * (1.1 if mood == "boom" else .8)
        return (f'<path d="M{x - w / 2} {y} Q{x} {y - w * .1} {x + w / 2} {y} Q{x + w * .4} {y + h} {x} {y + h} '
                f'Q{x - w * .4} {y + h} {x - w / 2} {y}Z" fill="#5A2E22"/>'
                f'<ellipse cx="{x}" cy="{y + h * .72}" rx="{w * .22}" ry="{h * .18}" fill="{PINK}"/>')
    if mood == "surprise":
        return f'<ellipse cx="{x}" cy="{y + w * .2}" rx="{w * .18}" ry="{w * .26}" fill="#5A2E22"/>'
    if mood == "worry":
        return stroke(f"M{x - w / 2} {y + w * .2} q{w / 4} {-w * .2} {w / 2} 0 q{w / 4} {w * .2} {w / 2} 0", "#5A2E22", max(1.8, w * .12))
    return stroke(f"M{x - w / 2} {y} q{w / 2} {w * .45} {w} 0", "#5A2E22", max(1.8, w * .12))


def face_mood(mood: str) -> str:
    return mood if mood in ("laugh", "surprise", "worry", "boom") else "smile"


# ---------------------------------------------------------------- animals (all face right, (x, y) = feet)
def ear(x: float, y: float, rot: float, col: str) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot})"><ellipse cy="-30" rx="9" ry="32" fill="{col}"/>'
            f'<ellipse cy="-28" rx="4.5" ry="24" fill="{PINK}"/></g>')


def rabbit(x, y, k=1, flip=False, mood="smile", pose="stand"):
    """Rabbit, a long-eared brown hare. pose: stand / hop / no (one paw up, waving 'no')."""
    ears = {"stand": (-14, 8), "hop": (-30, -12), "no": (-10, 10)}[pose]
    if mood == "worry":
        ears = (-62, -48)  # ears droop back
    if mood == "surprise":
        ears = (-4, 14)
    out = ear(30, -84, ears[1], HARE_D) + '<circle cx="-36" cy="-42" r="10" fill="#fff"/>'
    out += f'<ellipse cx="-14" cy="-30" rx="24" ry="22" fill="{HARE_D}"/><ellipse cx="0" cy="-38" rx="36" ry="26" fill="{HARE}"/>'
    out += f'<ellipse cx="12" cy="-30" rx="18" ry="13" fill="{CREAM}"/><ellipse cx="-6" cy="-5" rx="25" ry="6.5" fill="{HARE_D}"/>'
    if pose == "no":
        out += stroke("M20 -24 L22 -3", HARE, 9)
    else:
        out += stroke("M20 -24 L22 -3 M30 -26 L34 -4", HARE, 9)
    out += f'<circle cx="32" cy="-68" r="21" fill="{HARE}"/>' + ear(24, -84, ears[0], HARE)
    out += f'<ellipse cx="49" cy="-61" rx="12" ry="9.5" fill="{CREAM}"/><ellipse cx="59" cy="-65" rx="4" ry="3.2" fill="{PINK}"/>'
    out += f'<circle cx="34" cy="-58" r="5" fill="{BLUSH}" opacity=".45"/>' + eye(40, -74, 5.5, mood)
    out += stroke("M56 -60 l16 -3 M56 -57 l15 4", INK, 1.4) + mouth(52, -55, 9, face_mood(mood))
    if pose == "no":  # the paw goes up in FRONT of the body, palm out: "No, no!"
        out += stroke("M22 -36 Q44 -30 58 -14", HARE_D, 9) + stroke("M58 -14 L70 -40", HARE_D, 9)
        out += f'<ellipse cx="71" cy="-44" rx="7" ry="9" fill="{HARE_D}"/>' + stroke("M82 -54 l6 -6 M84 -42 l9 -1", INK, 2.4)
    rot = -10 if pose == "hop" else 0
    return group(x, y, SIZE["rabbit"] * k, flip, out, rot)


def jackal(x, y, k=1, flip=False, mood="smile"):
    """A black-backed jackal: tan, with a dark silvery saddle, big pointed ears and a black-tipped bushy tail."""
    out = stroke("M-30 -46 L-34 -2 M-18 -46 L-16 -2 M24 -46 L22 -2 M36 -46 L40 -2", JACK_D, 8)
    out += "".join(f'<ellipse cx="{a}" cy="-2" rx="6" ry="3.5" fill="{SADDLE}"/>' for a in (-34, -16, 22, 40))
    out += f'<path d="M-40 -64 Q-80 -64 -88 -24 Q-74 -36 -40 -50Z" fill="{JACK}"/><path d="M-84 -36 Q-90 -28 -88 -22 Q-80 -26 -78 -34Z" fill="{SADDLE}"/>'
    out += f'<ellipse cy="-60" rx="44" ry="19" fill="{JACK}"/><ellipse cx="4" cy="-48" rx="32" ry="7" fill="{CREAM}"/>'
    out += f'<path d="M-40 -66 Q-4 -88 36 -70 Q0 -72 -40 -58Z" fill="{SADDLE}"/>'
    out += "".join(f'<circle cx="{a}" cy="{b}" r="1.8" fill="#C9C2B8"/>' for a, b in [(-24, -70), (-8, -75), (8, -76), (22, -72), (-14, -66), (2, -70)])
    out += f'<path d="M28 -70 L50 -100 L66 -90 L46 -54Z" fill="{JACK}"/>'
    out += (f'<path d="M46 -102 L42 -134 L60 -108Z M58 -106 L64 -136 L72 -104Z" fill="{JACK}"/>'
            f'<path d="M48 -106 L46 -126 L56 -108Z M61 -108 L64 -128 L69 -106Z" fill="{SADDLE}" opacity=".7"/>')
    out += f'<ellipse cx="58" cy="-96" rx="18" ry="14" fill="{JACK}"/><path d="M64 -106 L94 -94 L92 -86 L64 -84Z" fill="{JACK}"/>'
    out += f'<path d="M62 -88 L90 -86 Q80 -78 64 -80Z" fill="{CREAM}"/><circle cx="93" cy="-91" r="3.6" fill="{INK}"/>'
    out += eye(64, -100, 4.2, mood) + mouth(80, -85, 10, face_mood(mood))
    return group(x, y, SIZE["jackal"] * k, flip, out)


def leopard(x, y, k=1, flip=False, mood="smile", pose="stand"):
    """A leopard: golden with dark rosettes, a long spotted tail and a round face. pose 'claws' lifts a paw."""
    front = "M30 -40 L28 -3 M44 -40 L48 -3" if pose != "claws" else "M30 -40 L28 -3 M44 -44 Q74 -40 98 -52"
    out = stroke("M-40 -40 L-42 -3 M-24 -40 L-22 -3", LEO_D, 13) + stroke(front, LEO_D, 13)
    feet = [(-42, -3), (-22, -3), (28, -3)] + ([(48, -3)] if pose != "claws" else [])
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="9" ry="4.5" fill="{LEO_D}"/>' for a, b in feet)
    if pose == "claws":
        out += f'<circle cx="100" cy="-53" r="9" fill="{LEO_D}"/>' + stroke("M108 -60 l8 -4 M110 -53 l9 0 M108 -46 l8 4", "#fff", 2.6)
    out += stroke("M-54 -56 Q-100 -44 -102 -82 Q-102 -102 -86 -100", LEO, 11) + f'<circle cx="-86" cy="-100" r="6" fill="{ROSE}"/>'
    out += f'<ellipse cy="-52" rx="58" ry="24" fill="{LEO}"/><ellipse cx="6" cy="-38" rx="40" ry="9" fill="{CREAM}"/>'
    spots = [(-40, -60), (-24, -66), (-6, -68), (12, -66), (30, -62), (-30, -48), (-12, -52), (6, -54), (24, -50), (40, -54), (-98, -70), (-96, -88)]
    out += "".join(f'<circle cx="{a}" cy="{b}" r="5" fill="none" stroke="{ROSE}" stroke-width="2.6"/>' for a, b in spots)
    out += f'<circle cx="52" cy="-92" r="7.5" fill="{LEO}"/><circle cx="76" cy="-94" r="7.5" fill="{LEO}"/>'
    out += f'<circle cx="52" cy="-92" r="3.5" fill="{ROSE}"/><circle cx="76" cy="-94" r="3.5" fill="{ROSE}"/>'
    out += f'<circle cx="64" cy="-72" r="23" fill="{LEO}"/><ellipse cx="76" cy="-62" rx="13" ry="10" fill="{CREAM}"/>'
    out += "".join(f'<circle cx="{a}" cy="{b}" r="2" fill="{ROSE}"/>' for a, b in [(56, -88), (64, -90), (72, -88), (48, -74), (50, -64)])
    out += '<path d="M80 -70 l7 0 l-3.5 5Z" fill="#B85A4A"/>' + eye(62, -78, 4.6, mood) + eye(78, -79, 4.6, mood)
    out += mouth(84, -61, 9, face_mood(mood)) + stroke("M86 -64 l14 -3 M86 -61 l13 3", INK, 1.3)
    return group(x, y, SIZE["leopard"] * k, flip, out)


def elephant(x, y, k=1, flip=False, mood="smile"):
    """A big grey elephant with flappy ears, a curling trunk and two ivory tusks."""
    out = "".join(f'<rect x="{a}" y="-122" width="38" height="122" rx="10" fill="{ELE_D}"/>' for a in (-64, 78))
    out += stroke("M-122 -150 Q-142 -110 -134 -90", ELE_D, 6)
    out += f'<ellipse cy="-150" rx="125" ry="80" fill="{ELE}"/>'
    out += "".join(f'<rect x="{a}" y="-120" width="40" height="120" rx="10" fill="{ELE}"/>' for a in (-104, 36))
    out += "".join(f'<path d="M{a + 6} 0 v-8 a5 5 0 0 1 10 0 v8Z M{a + 22} 0 v-8 a5 5 0 0 1 10 0 v8Z" fill="{IVORY}"/>' for a in (-104, 36))
    out += f'<circle cx="118" cy="-176" r="58" fill="{ELE}"/>'
    out += stroke("M150 -150 Q182 -100 170 -48 Q166 -26 186 -30", ELE, 28) + stroke("M160 -120 l14 -2 M168 -94 l14 0 M170 -70 l13 2", ELE_D, 2.4)
    out += f'<path d="M138 -138 Q160 -108 192 -116 Q166 -124 152 -144Z" fill="{IVORY}"/>'
    out += f'<ellipse cx="78" cy="-176" rx="46" ry="62" fill="{ELE_D}"/><ellipse cx="80" cy="-176" rx="32" ry="46" fill="#B9A3A8" opacity=".55"/>'
    out += eye(138, -196, 7, mood) + f'<circle cx="122" cy="-168" r="9" fill="{BLUSH}" opacity=".35"/>'
    out += mouth(136, -142, 14, face_mood(mood))
    return group(x, y, SIZE["elephant"] * k, flip, out)


def rhino(x, y, k=1, flip=False, mood="smile"):
    """A grey rhino with two horns on its nose: a big one in front and a small one behind."""
    out = "".join(f'<rect x="{a}" y="-52" width="30" height="52" rx="8" fill="{RHI_D}"/>' for a in (-40, 64))
    out += stroke("M-88 -84 Q-104 -70 -100 -52", RHI_D, 5)
    out += f'<ellipse cy="-80" rx="92" ry="48" fill="{RHI}"/>'
    out += "".join(f'<rect x="{a}" y="-52" width="30" height="52" rx="8" fill="{RHI}"/>' for a in (-70, 34))
    out += stroke("M-30 -120 q-10 30 0 70 M30 -122 q10 30 0 70", RHI_D, 3)
    out += f'<path d="M60 -114 Q102 -122 134 -86 L152 -62 Q152 -44 132 -42 L68 -46Z" fill="{RHI}"/>'
    out += f'<path d="M128 -76 Q146 -110 164 -140 Q154 -98 152 -62Z" fill="{HORN}"/><path d="M102 -98 Q110 -112 118 -126 Q120 -106 120 -92Z" fill="{HORN}"/>'
    out += f'<path d="M66 -112 L58 -138 L80 -116Z" fill="{RHI}"/><path d="M67 -116 L62 -132 L76 -117Z" fill="{RHI_D}"/>'
    out += eye(98, -88, 5, mood) + mouth(138, -50, 12, face_mood(mood))
    return group(x, y, SIZE["rhino"] * k, flip, out)


def frog(x, y, k=1, flip=False, mood="smile", pose="sit"):
    """A small green frog with big eyes on top of its head. pose: sit / boom (puffed up, arms high)."""
    puff = pose == "boom"
    out = f'<ellipse cx="-16" cy="-12" rx="18" ry="12" fill="{FROG_D}"/><ellipse cx="-4" cy="-2" rx="17" ry="4.5" fill="{FROG_D}"/>'
    out += f'<ellipse cy="{-28 if puff else -24}" rx="26" ry="{27 if puff else 22}" fill="{FROG}"/>'
    out += f'<ellipse cx="8" cy="{-20 if puff else -16}" rx="17" ry="{15 if puff else 12}" fill="{FROG_L}"/>'
    out += "".join(f'<circle cx="{a}" cy="{b}" r="3" fill="{FROG_D}"/>' for a, b in [(-14, -36), (-6, -42), (-18, -26)])
    if puff:
        out += stroke("M22 -30 Q36 -36 44 -52 M-22 -32 Q-34 -38 -40 -54", FROG, 7)
        out += f'<circle cx="45" cy="-55" r="5" fill="{FROG_D}"/><circle cx="-41" cy="-57" r="5" fill="{FROG_D}"/>'
    else:
        out += stroke("M14 -12 L18 -2", FROG, 7) + f'<ellipse cx="22" cy="-2" rx="7" ry="3" fill="{FROG_D}"/>'
    top = -50 if puff else -44
    out += f'<circle cx="2" cy="{top}" r="10" fill="{FROG}"/><circle cx="18" cy="{top + 2}" r="10" fill="{FROG}"/>'
    out += eye(3, top - 1, 6, mood) + eye(19, top + 1, 6, mood)
    out += mouth(16, top + 20, 16, "boom" if puff else face_mood(mood))
    return group(x, y, SIZE["frog"] * k, flip, out)


def caterpillar(x, y, k=1, flip=False, mood="smile"):
    """The Long One: a little fuzzy caterpillar with green segments, orange spots and two antennae."""
    segs = [(-52, -10), (-42, -16), (-32, -12), (-22, -9), (-12, -12), (-2, -16)]
    out = "".join(f'<ellipse cx="{a}" cy="{b + 7}" rx="2.6" ry="2" fill="{INK}" opacity=".7"/>' for a, b in segs)
    for i, (a, b) in enumerate(segs):
        out += stroke(f"M{a - 4} {b - 8} l-2 -6 M{a} {b - 9} l0 -7 M{a + 4} {b - 8} l2 -6", "#F4E9B0", 1.6)
        out += f'<circle cx="{a}" cy="{b}" r="8.5" fill="{CAT if i % 2 else CAT_D}"/><circle cx="{a}" cy="{b - 3}" r="2.4" fill="{CAT_S}"/>'
    out += stroke("M12 -32 q-2 -12 -8 -16 M20 -32 q4 -12 10 -14", INK, 2.4)
    out += f'<circle cx="4" cy="-48" r="2.6" fill="{CAT_S}"/><circle cx="30" cy="-46" r="2.6" fill="{CAT_S}"/>'
    out += f'<circle cx="14" cy="-22" r="12" fill="{CAT}"/><circle cx="12" cy="-15" r="3" fill="{BLUSH}" opacity=".5"/>'
    out += eye(13, -25, 3.4, mood) + eye(21, -24, 3.4, mood) + mouth(20, -16, 7, face_mood(mood))
    return group(x, y, SIZE["cat"] * k, flip, out)


# ---------------------------------------------------------------- scenery
def house(x: float, y: float, k: float = 1) -> str:
    """Rabbit's little round house: mud walls, a thatched roof, a round window and an arched DARK doorway."""
    out = f'<rect x="-140" y="-112" width="280" height="112" rx="26" fill="{MUD}"/>'
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="7" ry="4" fill="{MUD_D}" opacity=".5"/>' for a, b in [(-110, -30), (-60, -86), (-20, -24), (100, -40), (110, -86), (-100, -70)])
    out += (f'<path d="M-168 -92 Q-150 -170 0 -188 Q150 -170 168 -92 Q140 -100 120 -88 Q96 -102 70 -90 Q46 -104 20 -92 Q-6 -104 -30 -92 '
            f'Q-56 -104 -80 -90 Q-106 -102 -130 -88 Q-150 -100 -168 -92Z" fill="{THATCH}"/>')
    out += stroke("M-120 -110 l-10 16 M-80 -130 l-8 22 M-40 -144 l-4 26 M0 -150 v28 M40 -144 l4 26 M80 -130 l8 22 M120 -110 l10 16", THATCH_D, 3)
    out += f'<path d="M10 0 V-62 A30 30 0 0 1 70 -62 V0Z" fill="{DOOR}"/>' + stroke("M10 0 V-62 A30 30 0 0 1 70 -62 V0", MUD_D, 5)
    out += f'<circle cx="-80" cy="-56" r="14" fill="{DOOR}"/><circle cx="-80" cy="-56" r="14" fill="none" stroke="{MUD_D}" stroke-width="4"/>'
    out += '<rect x="4" y="-2" width="72" height="8" rx="4" fill="#C8463A"/>'
    out += ('<path d="M96 0 L92 -24 H122 L118 0Z" fill="#C8673A"/>'
            + stroke("M100 -26 v-4 M112 -26 v-8 M120 -26 v-4", GREEN_D, 2.4)
            + "".join(f'<circle cx="{a}" cy="{b}" r="5" fill="{c}"/>' for a, b, c in [(100, -30, "#F2789F"), (112, -34, "#F7D046"), (122, -28, "#fff")]))
    return group(x, y, SIZE["house"] * k, False, out)


def door_at(hx: float, hy: float, k: float) -> tuple:
    return hx + 40 * k, hy - 40 * k  # door centre in page coordinates


def boom(x: float, y: float, s: float = 1) -> str:
    """A big jagged shout-burst, with a tail pointing down-left to where the voice comes from."""
    pts = []
    for i in range(24):
        r = 46 if i % 2 == 0 else 30
        a = math.pi * 2 * i / 24
        pts.append(f"{r * 1.3 * math.cos(a):.1f} {r * math.sin(a):.1f}")
    zig = stroke("M-27 -9 l9 -9 l9 9 l9 -9 l9 9 l9 -9 M-27 11 l9 -9 l9 9 l9 -9 l9 9 l9 -9", "#C8463A", 4)
    tail = f'<path d="M-30 22 L-70 62 L-8 34Z" fill="#FFE27A" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    body = tail + f'<path d="M{" L".join(pts)}Z" fill="#FFE27A" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>' + zig
    return group(x, y, s, False, body)


def shout_lines(x: float, y: float, s: float = 1) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{stroke("M34 -34 l16 -14 M42 -8 l20 -2 M34 18 l16 12", INK, 3.4)}</g>'


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def kili(x: float, base: float, s: float = 1) -> str:
    """Far-away Kilimanjaro: a wide mountain with a flat, snowy top."""
    return (f'<g transform="translate({x} {base}) scale({s})"><path d="M-260 0 L-70 -120 Q0 -136 70 -120 L260 0Z" fill="{MTN}"/>'
            f'<path d="M-70 -120 Q0 -136 70 -120 L96 -104 L70 -96 L44 -108 L20 -94 L-6 -110 L-30 -96 L-52 -108 L-92 -106Z" fill="{SNOW}"/></g>')


def acacia(x: float, y: float, s: float = 1, shadow: bool = True) -> str:
    """A flat-topped acacia tree."""
    f = ' filter="url(#p)"' if shadow else ""
    return (f'<g transform="translate({x} {y}) scale({s})"{f}>' + stroke("M0 0 Q-4 -60 -30 -110 M-2 -60 Q20 -90 40 -112 M-18 -86 Q-50 -100 -70 -108", TRUNK, 9)
            + f'<path d="M-110 -108 Q-90 -142 -30 -146 Q20 -158 70 -140 Q112 -132 110 -110 Q60 -98 0 -104 Q-60 -96 -110 -108Z" fill="{GREEN_D}"/>'
            + f'<path d="M-90 -118 Q-60 -138 -20 -136 Q30 -146 80 -128 Q40 -118 -10 -120 Q-50 -114 -90 -118Z" fill="{GREEN}"/></g>')


def bush(x: float, y: float, s: float = 1) -> str:
    """A low leafy bush beside the house (the caterpillar's new home on the last page)."""
    leaves = [(-50, -40, 34), (-10, -62, 40), (36, -44, 34), (-30, -20, 30), (20, -18, 30)]
    out = stroke("M0 0 V-40 M0 -30 L-26 -50 M0 -36 L24 -58", TRUNK, 6)
    out += "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{GREEN_D if i % 2 else GREEN}"/>' for i, (a, b, r) in enumerate(leaves))
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="7" ry="4" fill="#8CC25C" transform="rotate(-30 {a} {b})"/>' for a, b in [(-50, -54), (-14, -84), (30, -66), (-30, -30), (40, -28)])
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{out}</g>'


def tufts(pts: list, col: str = GRASS_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def savanna(horizon: float = 330, sun: bool = True, far_trees: bool = True) -> list:
    out = [cloud(150, 80, 1), cloud(660, 60, .85)]
    if sun:
        out.append('<circle cx="740" cy="130" r="34" fill="#FFE27A" opacity=".9"/>')
    out.append(kili(470, horizon + 4, 1))
    out.append(f'<path d="M0 {horizon} Q200 {horizon - 18} 400 {horizon} T800 {horizon - 6} V600 H0Z" fill="{GRASS_B}"/>')
    if far_trees:
        out += [acacia(90, horizon + 8, .38, False), acacia(700, horizon + 6, .45, False)]
    out.append(f'<path filter="url(#p)" d="M0 {horizon + 40} Q400 {horizon + 10} 800 {horizon + 40} V600 H0Z" fill="{GRASS}"/>')
    out.append(tufts([(40, horizon + 70), (330, horizon + 50), (560, horizon + 60), (760, horizon + 74), (120, 580), (420, 588), (680, 580)]))
    return out


def path_to(hx: float) -> str:
    return f'<path d="M{hx + 20} {GROUND + 4} Q{hx + 200} {GROUND + 30} 820 {GROUND + 90} V610 H{hx + 300} Q{hx + 140} {GROUND + 50} {hx + 80} {GROUND + 4}Z" fill="#D8B57A" opacity=".8"/>'


def birds(pts: list) -> str:
    return stroke(" ".join(f"M{a - 9} {b} q4.5 -6 9 0 q4.5 -6 9 0" for a, b in pts), INK, 2.4)


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/longone-{n:02d}.svg", "w") as fh:
        fh.write(doc)


K1 = 1.2  # one scale for the house and every figure on the single-scene pages
HX = 205
DX, DY = door_at(HX, GROUND, K1)


def home(hx: float = HX) -> list:
    return [path_to(hx), house(hx, GROUND, K1)]


def shout(s: float = 1) -> list:
    return [boom(DX + 120, DY - 150, s), shout_lines(DX + 6, DY, 1.1)]


# 01 cover
svg(1, "Who's in Rabbit's House?", "Paper-cut cover: on the golden grassland, with snowy flat-topped Kilimanjaro far behind and acacia trees, stands Rabbit's little round house with mud walls and a thatched roof. A big yellow shout-burst bursts out of its dark doorway, and Rabbit, a long-eared brown hare, stands in front of the house staring at it in surprise.", DAY, [
    *savanna(), acacia(690, 470, .8), *home(), *shout(), rabbit(520, 480, K1, True, "surprise")])

# 02 Rabbit hops home
svg(2, "Rabbit hops home", "Paper-cut scene: Rabbit, a long-eared brown hare, hops happily along a sandy path towards her little round house, which has mud walls, a thatched roof, a red mat and a pot of flowers by the dark doorway. Kilimanjaro rises far away, and two birds fly in the blue sky.", DAY, [
    *savanna(), acacia(700, 468, .8), *home(), birds([(300, 140), (340, 120)]),
    rabbit(560, 530, K1, True, "smile", "hop"), stroke("M640 540 q10 -22 24 -6 M676 542 q10 -22 24 -6", "#fff", 3)])

# 03 Who's in my house?
svg(3, "Who's in my house?", "Paper-cut scene: Rabbit has jumped back from her own front door, her ears straight up and her eyes wide. A big yellow shout-burst bursts out of the dark doorway of her little round house: someone inside has a HUGE voice. Nobody can be seen inside.", DAY, [
    *savanna(), *home(), *shout(1.1), rabbit(540, 480, K1, True, "surprise")])

# 04 Jackal: I'll dig it down
svg(4, "Jackal has a plan", "Paper-cut scene: a black-backed jackal, tan with a dark silvery back and big pointed ears, trots up grinning, ready to dig. Rabbit stands between him and her little round house, holding up one paw: No, no, that's my house! The doorway is dark and empty.", DAY, [
    *savanna(), *home(), rabbit(470, 480, K1, False, "worry", "no"), jackal(680, 486, K1, True, "smile"),
    stroke("M590 494 l-10 8 M606 498 l-6 10", INK, 3)])

# 05 Leopard: I'll scratch a hole in the roof
svg(5, "Leopard has a plan", "Paper-cut scene: a golden leopard with dark spots and a long spotted tail strolls up, smiling, ready to scratch a hole in the roof. Rabbit holds up her paw: No, no, that's my house! The doorway is dark and empty.", DAY, [
    *savanna(), *home(), rabbit(448, 480, K1, False, "worry", "no"), leopard(642, 488, K1, True, "smile")])

# 06 Elephant: I'll sit on it! (one step further back, k = .95, so the big elephant fits beside Rabbit)
K6 = .95
svg(6, "Elephant has a plan", "Paper-cut scene: a huge grey elephant with flappy ears, a curling trunk and white tusks, much bigger than the little house, says she will SIT on it. Rabbit, small beside her, holds up her paw: No, no, that's my house! The doorway is dark and empty.", DAY, [
    *savanna(far_trees=False), path_to(170), house(170, GROUND, K6), rabbit(375, 476, K6, False, "worry", "no"), elephant(645, 488, K6, True, "smile")])

# 07 Rhino: I'll bump it over!
svg(7, "Rhino has a plan", "Paper-cut scene: a grey rhino with a big horn and a small horn on her nose comes to bump the little house over. Rabbit holds up her paw: No, no, that's my house! A big yellow shout-burst bursts out of the dark doorway, and the rhino's eyes go wide.", DAY, [
    *savanna(), *home(), *shout(.95), rabbit(408, 480, K1, False, "worry", "no"), rhino(672, 494, K1, True, "surprise")])
# 08 everyone is stuck. Frog laughs.
K = .7
HX2 = 120
svg(8, "Who can help?", "Paper-cut scene: everyone stands outside the little round house, looking worried: the elephant, the rhino, the leopard, the jackal and Rabbit. A small green frog has hopped up on the right and is laughing, ha ha ha! The doorway is dark and empty.", DAY, [
    *savanna(far_trees=False), house(HX2, GROUND, K), rhino(420, 456, K, True, "worry"), elephant(660, 456, K, True, "worry"),
    rabbit(240, 560, K, False, "worry"), leopard(400, 566, K, True, "worry"), jackal(560, 566, K, True, "worry"),
    frog(720, 566, K * 1.15, True, "laugh")])

# 09 Frog: I'll get him out! Everyone laughs at the little frog.
svg(9, "You? You're so little!", "Paper-cut scene: the little green frog sits in the middle, smiling, ready to help. All around him the elephant, the rhino, the leopard, the jackal and even Rabbit are laughing, because the frog is so small. The little round house stands at the left with its doorway dark and empty.", DAY, [
    *savanna(far_trees=False), house(HX2, GROUND, K), rhino(420, 456, K, True, "laugh"), elephant(660, 456, K, True, "laugh"),
    rabbit(220, 560, K, False, "laugh"), frog(330, 566, K * 1.15, False, "smile"), leopard(480, 566, K, True, "laugh"), jackal(650, 566, K, True, "laugh")])

# 10 Frog BOOMS at the door
svg(10, "The Great Big Leaper", "Paper-cut scene: right by the dark doorway of the little round house, the small green frog has puffed himself up as big as he can, arms out wide, shouting his very loudest. Rabbit and the jackal watch from the right with wide eyes. The doorway is still dark and empty.", DAY, [
    *savanna(far_trees=False), *home(), frog(440, 488, K1, True, "boom", "boom"), shout_lines(400, 452, -1),
    rabbit(575, 480, K1, True, "surprise"), jackal(696, 486, K1, True, "surprise")])

# 11 the reveal (frog and caterpillar scaled down so frog:rabbit and caterpillar:frog match pages 8, 9 and 12)
K3 = 1.8
HX3 = 40
DX3, _ = door_at(HX3, 520, K3)
svg(11, "Only a little caterpillar!", "Paper-cut close-up: out of the dark doorway of the little round house creeps the Long One. It is only a little fuzzy caterpillar, green with orange spots and two tiny antennae, smiling shyly. The small green frog and Rabbit look at it in surprise.", DAY, [
    *savanna(380, far_trees=False), house(HX3, 520, K3),
    caterpillar(140, 528, K3 * .67, False, "smile"), frog(360, 528, K3 * .6, True, "surprise"), rabbit(600, 532, K3, True, "surprise")])

# 12 everybody laughs
svg(12, "Everybody laughed", "Paper-cut scene: everyone is laughing together outside the little round house: the elephant, the rhino, the leopard, the jackal, Rabbit, the little frog, and the little fuzzy caterpillar too, sitting on a flat stone at the front.", DAY, [
    *savanna(far_trees=False), house(HX2, GROUND, K), rhino(420, 456, K, True, "laugh"), elephant(660, 456, K, True, "laugh"),
    rabbit(220, 560, K, False, "laugh"), f'<ellipse filter="url(#p)" cx="330" cy="566" rx="42" ry="11" fill="#B9A58A"/>',
    caterpillar(342, 560, K * 1.25, False, "laugh"), frog(420, 566, K * 1.15, True, "laugh"),
    leopard(530, 566, K, True, "laugh"), jackal(690, 566, K, True, "laugh")])

# 13 evening: the caterpillar eats leaves in Rabbit's bush; Rabbit at home
K4 = 1.25
svg(13, "Home again", "Paper-cut scene in warm golden evening light: Rabbit sits happily beside her little round house. Beside it grows a low leafy bush, and on top of the bush the little fuzzy caterpillar munches a leaf. Kilimanjaro glows far behind.", GOLDEN, [
    *savanna(360, sun=False, far_trees=False), '<circle cx="660" cy="250" r="40" fill="#FFD27A" opacity=".9"/>',
    house(170, 530, K4), rabbit(450, 540, K4, False, "smile"), bush(660, 540, 1.4),
    caterpillar(660, 432, K4, True, "smile")])
