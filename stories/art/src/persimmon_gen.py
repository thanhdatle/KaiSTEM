#!/usr/bin/env python3
"""Generates the 13 Tiger-and-the-Dried-Persimmon flip-book SVGs from shared character parts.

Usage: python3 persimmon_gen.py <output-dir>
Scale rule (kept on every page): characters at the same depth share one scale c; the house is
drawn at c / 0.6 and the cowshed at c / 0.62, so the tiger, cow, thief and mother stay the same
size relative to each other and to the buildings (things nearer the viewer may be a little bigger).
Orange-and-black stripes are reserved for the tiger; the deep persimmon orange for the gotgam.
"""
import math
import random
import sys

OUT = sys.argv[1]
INK = "#2B2320"
TIG, TIG_D, TIG_W, TIG_N = "#F0892B", "#C9661A", "#FFF4E2", "#5A2A20"
GAM, GAM_L, GAM_C = "#D4622A", "#EE8A4E", "#5E5A2A"             # gotgam (dried persimmon)
COW, COW_D, COW_M = "#B9773C", "#93592A", "#EBC9A2"
JACKET, PANTS, KER, SKIN, SKIN_D, SHOE = "#5E6E86", "#46526A", "#3A3550", "#F1C9A1", "#D9A27A", "#2F2A3A"
SKIRT, JEOG, RIBBON, HAIR, SWADDLE = "#D9576E", "#FBF1DE", "#C9344A", "#2E2433", "#9FC7E8"
MUD, POST, STONE, STRAW, STRAW_D = "#E6CFA6", "#8A5A3A", "#9A9AA8", "#D6B46E", "#A9864A"
GLOW, PAPER, SHADOW = "#FFD98A", "#F5EBD3", "#8C6A4A"
SHED_IN, SHED_IN_DAY, HAY = "#3A2C30", "#5A4436", "#C9A55A"
SNOW, SNOW_N, SNOW_SH = "#F7F9FD", "#E3E9F7", "#C9D4EA"
PINE, PINE_D = "#2F5D50", "#24483F"
MTN_N, MTN_N2, MTN_D, MTN_D2 = "#3D4C7A", "#50608F", "#8FA3C8", "#A9BAD8"
NIGHT = [(0, "#141C46"), (.6, "#2E3A78"), (1, "#56609E")]
DAWN = [(0, "#6A6FB0"), (.45, "#E9A3B4"), (1, "#FFD9A8")]
MORNING = [(0, "#9CD3F0"), (1, "#FFF1D6")]
HOUSE_K, SHED_K = 0.6, 0.62   # character scale = building scale * K


def stroke(d: str, col: str = INK, w: float = 5, op: float = 1) -> str:
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{o}/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def qpoint(p0: tuple, p1: tuple, p2: tuple, t: float) -> tuple:
    """Point and unit normal on a quadratic Bezier."""
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    n = math.hypot(dx, dy) or 1
    return x, y, -dy / n, dx / n


# ---------------------------------------------------------------- the tiger
TAILS = {"stand": ((-80, -84), (-140, -90), (-138, -152)),
         "run": ((-80, -84), (-130, -84), (-172, -116)),
         "crouch": ((-80, -70), (-124, -34), (-156, -26))}
# (hip x, hip y, paw x, paw y): two near legs first, then two far legs
LEGS = {"stand": [(-30, -60, -26, -4), (62, -60, 66, -4), (-52, -60, -56, -4), (40, -60, 38, -4)],
        "crouch": [(-30, -50, -24, -4), (62, -50, 70, -4), (-52, -50, -60, -4), (40, -50, 40, -4)],
        "run": [(-30, -64, -74, -10), (62, -64, 124, -40), (-52, -64, -104, -24), (40, -64, 98, -14)]}


def tiger_eyes(mood: str) -> str:
    if mood in ("roar", "happy"):
        return stroke("M76 -128 q8 -8 16 0 M108 -128 q8 -8 16 0", INK, 4)
    r, pr = {"scared": (12, 3.4), "oh": (10, 4), "huh": (9, 4.6)}.get(mood, (8.5, 4.6))
    out = "".join(f'<circle cx="{cx}" cy="-126" r="{r}" fill="#fff"/><circle cx="{cx + 1}" cy="-125" r="{pr}" fill="{INK}"/>' for cx in (84, 116))
    if mood == "scared":
        out += stroke("M72 -146 q10 -8 20 -2 M108 -148 q10 -6 20 2", INK, 3.6)
    if mood == "huh":
        out += stroke("M72 -142 l20 4 M128 -142 l-20 4", INK, 4)
    return out


def tiger_mouth(mood: str) -> str:
    if mood == "roar":
        return '<ellipse cx="100" cy="-84" rx="13" ry="11" fill="#7A2A2A"/><ellipse cx="100" cy="-78" rx="7" ry="4" fill="#F28B9B"/>'
    if mood == "oh":
        return '<ellipse cx="100" cy="-86" rx="6" ry="7" fill="#7A2A2A"/>'
    if mood == "scared":
        return stroke("M84 -86 q4 -5 8 0 q4 5 8 0 q4 -5 8 0 q4 5 8 0", INK, 3)
    if mood == "huh":
        return stroke("M90 -88 h20", INK, 3.4)
    return stroke("M100 -100 v6 M90 -92 q5 5 10 0 q5 5 10 0", INK, 3)


def tiger_leg(hx: float, hy: float, px: float, py: float, col: str, stripe: bool) -> str:
    out = stroke(f"M{hx} {hy} L{px} {py}", col, 22) + f'<ellipse cx="{px + 3}" cy="{py + 2}" rx="14" ry="8" fill="{col}"/>'
    if stripe:
        mx, my = (hx + px) / 2, (hy + py) / 2
        out += stroke(f"M{mx - 8:.0f} {my:.0f} h16", INK, 4)
    return out


def tiger(x: float, y: float, s: float, mood: str = "smile", flip: bool = False, pose: str = "stand",
          rider: str = "", shake: bool = False) -> str:
    """The tiger, side-on and facing right, with his face turned to us. (x, y) is between his paws."""
    dy = 26 if pose == "crouch" else 0
    legs = LEGS[pose]
    far = "".join(tiger_leg(hx, hy + dy, px, py, TIG_D, False) for hx, hy, px, py in legs[2:])
    near = "".join(tiger_leg(hx, hy + dy, px, py, TIG, True) for hx, hy, px, py in legs[:2])
    p0, p1, p2 = TAILS[pose]
    p0 = (p0[0], p0[1] + dy)
    tail = stroke(f"M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}", TIG, 14)
    for t in (.4, .62, .84):
        qx, qy, nx, ny = qpoint(p0, p1, p2, t)
        tail += stroke(f"M{qx - nx * 7:.1f} {qy - ny * 7:.1f} L{qx + nx * 7:.1f} {qy + ny * 7:.1f}", INK, 5)
    tail += f'<circle cx="{p2[0]}" cy="{p2[1]}" r="8.5" fill="{INK}"/>'
    cy = -78 + dy
    body = f'<ellipse cx="0" cy="{cy}" rx="88" ry="44" fill="{TIG}"/><ellipse cx="6" cy="{cy + 32}" rx="62" ry="12" fill="{TIG_W}"/>'
    for sx in (-64, -38, -12, 14, 40):
        top = cy - 44 * math.sqrt(1 - (sx / 88) ** 2) + 3
        body += stroke(f"M{sx} {top:.1f} Q{sx + 11} {top + 18:.1f} {sx - 1} {top + 36:.1f}", INK, 7)
    head = (f'<g transform="translate(0 {dy})">'
            f'<circle cx="70" cy="-154" r="15" fill="{TIG}"/><circle cx="130" cy="-154" r="15" fill="{TIG}"/>'
            '<circle cx="70" cy="-153" r="8" fill="#F4A6A0"/><circle cx="130" cy="-153" r="8" fill="#F4A6A0"/>'
            f'<circle cx="100" cy="-118" r="46" fill="{TIG}"/>'
            + stroke("M100 -163 v13 M87 -161 l3 10 M113 -161 l-3 10", INK, 5)
            + stroke("M55 -124 h13 M57 -108 h11 M145 -124 h-13 M143 -108 h-11", INK, 5)
            + f'<ellipse cx="100" cy="-94" rx="31" ry="20" fill="{TIG_W}"/>'
            + f'<path d="M91 -108 h18 l-9 9z" fill="{TIG_N}"/>'
            + stroke("M70 -98 l-20 -4 M70 -92 l-20 4 M130 -98 l20 -4 M130 -92 l20 4", "#fff", 2.4)
            + '<circle cx="70" cy="-104" r="7" fill="#F0705F" opacity=".45"/><circle cx="130" cy="-104" r="7" fill="#F0705F" opacity=".45"/>'
            + tiger_eyes(mood) + tiger_mouth(mood) + '</g>')
    sh = ""
    if shake:
        hy = -118 + dy
        sh = stroke(f"M-108 {cy - 30} q-10 12 0 24 M-120 {cy - 38} q-12 18 0 36 M160 {hy - 20} q10 12 0 24 M172 {hy - 28} q12 18 0 36", "#fff", 4, .9)
    ride = f'<g transform="translate(-6 {cy - 40})">{rider}</g>' if rider else ""
    return group(x, y, s, flip, 0, far + tail + near + body + ride + head + sh)


# ---------------------------------------------------------------- the cow thief
def thief_top(mood: str, arms: str, lean: float = 0) -> str:
    """Upper body with the bottom of the jacket at y = 0, facing right."""
    sack = ""
    if arms == "sneak":
        sack = f'<ellipse cx="-40" cy="-90" rx="22" ry="26" fill="#A57C52"/>' + stroke("M-46 -112 q6 -8 14 -2", "#7E5A36", 4)
        a = (stroke("M16 -60 Q40 -50 54 -66", JACKET, 12) + f'<circle cx="56" cy="-68" r="7" fill="{SKIN}"/>'
             + stroke("M-16 -60 Q-34 -76 -28 -98", JACKET, 12) + f'<circle cx="-28" cy="-100" r="7" fill="{SKIN}"/>')
    elif arms == "up":  # both arms flung up in surprise
        a = (stroke("M16 -60 Q40 -76 46 -106", JACKET, 12) + f'<circle cx="47" cy="-110" r="7.5" fill="{SKIN}"/>'
             + stroke("M-16 -60 Q-40 -76 -46 -106", JACKET, 12) + f'<circle cx="-47" cy="-110" r="7.5" fill="{SKIN}"/>')
    else:  # "hold": both hands forward, gripping
        a = (stroke("M14 -60 Q42 -54 52 -36", JACKET, 12) + f'<circle cx="53" cy="-34" r="7.5" fill="{SKIN}"/>'
             + stroke("M-6 -58 Q26 -40 42 -24", JACKET, 12) + f'<circle cx="43" cy="-22" r="7.5" fill="{SKIN}"/>')
    torso = (f'<path d="M-24 0 Q-28 -48 -16 -70 H16 Q28 -48 24 0 Q0 6 -24 0Z" fill="{JACKET}"/>'
             + stroke("M-23 -14 Q0 -8 23 -14", SHOE, 5) + stroke("M-8 -68 L2 -54 L12 -68", "#E3E6EE", 3))
    head = (f'<circle cx="2" cy="-98" r="27" fill="{SKIN}"/>'
            f'<path d="M-26 -102 Q-24 -133 4 -133 Q30 -131 29 -104 Q4 -114 -26 -102Z" fill="{KER}"/>'
            f'<circle cx="-26" cy="-112" r="6" fill="{KER}"/>' + stroke("M-28 -110 l-16 -6 M-28 -108 l-14 7", KER, 6)
            + f'<circle cx="31" cy="-92" r="4.5" fill="{SKIN_D}"/><circle cx="16" cy="-84" r="5" fill="#F0705F" opacity=".45"/>')
    if mood == "sneaky":
        face = ('<ellipse cx="9" cy="-98" rx="6" ry="3.4" fill="#fff"/><ellipse cx="22" cy="-98" rx="6" ry="3.4" fill="#fff"/>'
                f'<circle cx="12" cy="-98" r="2.6" fill="{INK}"/><circle cx="25" cy="-98" r="2.6" fill="{INK}"/>'
                + stroke("M3 -104 l12 2 M17 -103 l11 -1", INK, 2.6) + stroke("M10 -80 q9 5 16 -4", INK, 2.8))
    elif mood == "whee":
        face = stroke("M4 -98 q5 -6 10 0 M18 -98 q5 -6 10 0", INK, 3) + '<path d="M8 -84 Q18 -70 28 -86Z" fill="#7A2A2A"/>'
    else:  # shock
        face = ('<circle cx="9" cy="-99" r="7" fill="#fff"/><circle cx="23" cy="-99" r="7" fill="#fff"/>'
                f'<circle cx="11" cy="-99" r="3" fill="{INK}"/><circle cx="25" cy="-99" r="3" fill="{INK}"/>'
                '<ellipse cx="18" cy="-80" rx="5" ry="7" fill="#7A2A2A"/>' + stroke("M2 -112 q7 -5 14 0 M18 -112 q7 -5 14 0", INK, 2.6))
    r = f' transform="rotate({lean})"' if lean else ""
    return f'<g{r}>{sack}{torso}{a}{head}{face}</g>'


def thief(x: float, y: float, s: float, flip: bool = False) -> str:
    """The cow thief tiptoeing with his sack. (x, y) is at his feet."""
    legs = (stroke("M-8 -80 Q-14 -40 -28 -10", PANTS, 14) + f'<ellipse cx="-32" cy="-6" rx="11" ry="6" fill="{SHOE}"/>'
            + stroke("M10 -80 Q40 -64 38 -30", PANTS, 14) + f'<ellipse cx="44" cy="-28" rx="11" ry="6" fill="{SHOE}" transform="rotate(-20 44 -28)"/>')
    return group(x, y, s, flip, 0, legs + f'<g transform="translate(0 -80)">{thief_top("sneaky", "sneak")}</g>')


def thief_rider(mood: str) -> str:
    """The thief sitting astride, for the tiger's back. Origin is the seat."""
    leg = stroke("M2 2 Q30 6 34 36", PANTS, 14) + f'<ellipse cx="40" cy="40" rx="11" ry="6" fill="{SHOE}"/>'
    return leg + thief_top(mood, "hold", 10)


def thief_sitting(x: float, y: float, s: float) -> str:
    """Sitting up in a snowdrift, startled, with snow on his head. (x, y) is where his jacket meets the snow."""
    top = thief_top("shock", "up")
    cap = '<ellipse cx="2" cy="-132" rx="28" ry="10" fill="#fff"/><circle cx="-10" cy="-138" r="8" fill="#fff"/><circle cx="12" cy="-139" r="7" fill="#fff"/>'
    return group(x, y, s, False, 0, top + cap)


# ---------------------------------------------------------------- cow, mother, gotgam
def cow(x: float, y: float, s: float, mood: str = "calm", flip: bool = False) -> str:
    """A yellow-brown Korean cow, side-on facing right, face turned to us. (x, y) is at her hooves."""
    def leg(a: float, b: float, col: str) -> str:
        return stroke(f"M{a} -60 L{b} -2", col, 18) + f'<rect x="{b - 9}" y="-8" width="18" height="9" rx="3" fill="{SHOE}"/>'
    far = leg(-52, -54, COW_D) + leg(40, 42, COW_D)
    near = leg(-28, -26, COW) + leg(62, 64, COW)
    tail = stroke("M-84 -96 Q-104 -64 -98 -30", COW, 7) + f'<ellipse cx="-98" cy="-24" rx="7" ry="11" fill="{COW_D}"/>'
    body = f'<ellipse cx="0" cy="-82" rx="86" ry="42" fill="{COW}"/><ellipse cx="-30" cy="-98" rx="22" ry="12" fill="#C98A50" opacity=".7"/>'
    head = (stroke("M84 -128 Q76 -142 70 -154 M116 -128 Q124 -142 130 -154", "#F3E6C8", 8)
            + f'<ellipse cx="62" cy="-118" rx="16" ry="8" fill="{COW_D}" transform="rotate(-20 62 -118)"/>'
            f'<ellipse cx="138" cy="-118" rx="16" ry="8" fill="{COW_D}" transform="rotate(20 138 -118)"/>'
            f'<ellipse cx="100" cy="-102" rx="34" ry="38" fill="{COW}"/><ellipse cx="102" cy="-76" rx="29" ry="18" fill="{COW_M}"/>'
            f'<ellipse cx="92" cy="-76" rx="4" ry="5" fill="{COW_D}"/><ellipse cx="112" cy="-76" rx="4" ry="5" fill="{COW_D}"/>')
    if mood == "oh":
        head += ('<circle cx="88" cy="-110" r="8" fill="#fff"/><circle cx="114" cy="-110" r="8" fill="#fff"/>'
                 f'<circle cx="89" cy="-109" r="3.6" fill="{INK}"/><circle cx="115" cy="-109" r="3.6" fill="{INK}"/>'
                 '<ellipse cx="102" cy="-62" rx="6" ry="5" fill="#7A2A2A"/>')
    else:
        head += ('<circle cx="88" cy="-110" r="6" fill="#fff"/><circle cx="114" cy="-110" r="6" fill="#fff"/>'
                 f'<circle cx="89" cy="-109" r="3.4" fill="{INK}"/><circle cx="115" cy="-109" r="3.4" fill="{INK}"/>' + stroke("M94 -62 q8 5 16 0", INK, 2.6))
    return group(x, y, s, flip, 0, far + tail + near + body + head)


def gotgam(x: float, y: float, r: float) -> str:
    """One dried persimmon: a squashed deep-orange round with a dark four-leaf cap."""
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .8:.1f}" fill="{GAM}"/>'
            f'<ellipse cx="{x - r * .35:.1f}" cy="{y - r * .2:.1f}" rx="{r * .3:.1f}" ry="{r * .2:.1f}" fill="{GAM_L}" opacity=".8"/>'
            f'<path d="M{x} {y - r * .95:.1f} l{r * .45:.1f} {-r * .2:.1f} l{-r * .25:.1f} {r * .35:.1f} l{r * .2:.1f} {r * .25:.1f} '
            f'l{-r * .4:.1f} {-r * .05:.1f} l{-r * .4:.1f} {r * .05:.1f} l{r * .2:.1f} {-r * .25:.1f} l{-r * .25:.1f} {-r * .35:.1f}z" fill="{GAM_C}"/>')


def gotgam_string(x: float, top: float, n: int, gap: float, r: float) -> str:
    """Dried persimmons hung on a straw string under the eaves, the Korean way."""
    return stroke(f"M{x} {top} V{top + gap * n}", "#B39060", max(1.6, r * .3)) + "".join(gotgam(x, top + gap * (i + .9), r) for i in range(n))


def mother(x: float, y: float, s: float) -> str:
    """Mother in a hanbok, holding the baby, who munches a gotgam. (x, y) is at her feet."""
    inner = (f'<path d="M-42 0 Q-38 -60 -18 -100 H18 Q38 -60 42 0 Q0 8 -42 0Z" fill="{SKIRT}"/>'
             + stroke("M-30 -40 Q-26 -70 -12 -96", "#E8798C", 4)
             + f'<path d="M-22 -96 Q-24 -128 -14 -140 H14 Q24 -128 22 -96Z" fill="{JEOG}"/>'
             + stroke("M2 -126 l10 24 M2 -126 l-4 26", RIBBON, 5)
             + f'<ellipse cx="18" cy="-112" rx="26" ry="20" fill="{SWADDLE}"/><circle cx="28" cy="-130" r="13" fill="{SKIN}"/>'
             + f'<path d="M15 -134 Q20 -146 34 -142 Q30 -138 15 -134Z" fill="{HAIR}"/>'
             + stroke("M24 -131 q3 -3 6 0 M32 -131 q3 -3 6 0", INK, 2) + '<circle cx="38" cy="-124" r="3" fill="#F0705F" opacity=".5"/>'
             + gotgam(43, -118, 7) + f'<circle cx="38" cy="-112" r="4.5" fill="{SKIN}"/>'
             + stroke("M-16 -128 Q-10 -100 20 -100", JEOG, 9) + f'<circle cx="22" cy="-100" r="5" fill="{SKIN}"/>'
             + f'<circle cx="0" cy="-162" r="22" fill="{SKIN}"/>'
             f'<path d="M-23 -160 Q-24 -188 0 -186 Q20 -186 22 -168 Q4 -178 -6 -170 Q-14 -160 -23 -160Z" fill="{HAIR}"/>'
             f'<circle cx="-22" cy="-158" r="9" fill="{HAIR}"/>' + stroke("M-34 -158 h22", "#E3C46A", 3)
             + stroke("M4 -162 q4 -4 8 0 M14 -162 q4 -4 8 0", INK, 2.4) + stroke("M8 -150 q5 4 10 0", INK, 2.4)
             + '<circle cx="18" cy="-154" r="4" fill="#F0705F" opacity=".45"/>')
    return group(x, y, s, False, 0, inner)


def monster(x: float, y: float, s: float) -> str:
    """The silly monster the tiger IMAGINES a gotgam must be."""
    inner = (stroke("M-80 0 Q-120 -30 -112 -70 M80 0 Q120 -30 112 -70", GAM, 12)
             + f'<circle cx="-112" cy="-74" r="10" fill="{GAM}"/><circle cx="112" cy="-74" r="10" fill="{GAM}"/>'
             + f'<ellipse rx="90" ry="72" fill="{GAM}"/>' + stroke("M-40 -66 Q-58 0 -36 66 M40 -66 Q58 0 36 66", "#B44E1E", 3, .6)
             + f'<ellipse cx="-40" cy="-30" rx="22" ry="14" fill="{GAM_L}" opacity=".7"/>'
             + f'<path d="M0 -66 l40 -22 l-18 30 l26 16 l-40 -4 l-8 18 l-8 -18 l-40 4 l26 -16 l-18 -30z" fill="{GAM_C}"/>'
             + stroke("M0 -80 q4 -16 -4 -26", GAM_C, 6)
             + '<circle cx="-28" cy="-6" r="17" fill="#fff"/><circle cx="28" cy="-6" r="17" fill="#fff"/>'
             f'<circle cx="-24" cy="-4" r="7" fill="{INK}"/><circle cx="24" cy="-4" r="7" fill="{INK}"/>'
             + stroke("M-50 -28 Q-34 -50 -14 -32 M50 -28 Q34 -50 14 -32", INK, 7)
             + '<path d="M-40 26 Q0 60 40 26Z" fill="#7A2A2A"/><rect x="-17" y="27" width="12" height="13" rx="2" fill="#fff"/>'
             '<rect x="5" y="27" width="12" height="13" rx="2" fill="#fff"/>')
    return group(x, y, s, False, 0, inner)


# ---------------------------------------------------------------- buildings
def house(x: float, y: float, s: float, night: bool = True, strings: tuple = (100, 140), window: str = "", snowy: bool = True) -> str:
    """A Korean choga-jip: mud walls, paper-lattice window and door, thick rounded straw roof. (x, y) is the base."""
    lit = GLOW if night else PAPER
    out = (f'<rect x="-186" y="-16" width="372" height="16" rx="4" fill="{STONE}"/><rect x="-180" y="-124" width="360" height="110" fill="{MUD}"/>'
           + "".join(f'<rect x="{px}" y="-124" width="10" height="110" fill="{POST}"/>' for px in (-180, -22, 68, 170))
           + f'<rect x="-150" y="-104" width="80" height="68" fill="{lit}"/>{window}'
           + stroke("M-150 -104 h80 v68 h-80z M-130 -104 v68 M-110 -104 v68 M-90 -104 v68 M-150 -82 h80 M-150 -60 h80", POST, 2.6)
           + f'<rect x="-6" y="-108" width="66" height="92" fill="{lit}"/>'
           + stroke("M-6 -108 h66 v92 h-66z M16 -108 v92 M38 -108 v92 M-6 -84 h66 M-6 -60 h66 M-6 -36 h66", POST, 2.6))
    roof = (f'<path d="M-216 -114 Q-206 -232 0 -238 Q206 -232 216 -114 Q0 -98 -216 -114Z" fill="{STRAW}"/>'
            + stroke("M-196 -150 Q0 -136 196 -150 M-176 -190 Q0 -180 176 -190 M-120 -222 Q0 -214 120 -222", STRAW_D, 3)
            + stroke("M-150 -112 Q-170 -190 -90 -228 M-60 -104 Q-74 -200 -30 -236 M40 -104 Q50 -200 30 -236 M140 -112 Q160 -190 90 -228", STRAW_D, 3)
            + stroke("M-214 -114 Q0 -98 214 -114", STRAW_D, 8))
    if snowy:
        roof += ('<path d="M-200 -176 Q-192 -236 0 -242 Q192 -236 200 -176 Q160 -196 110 -188 Q50 -206 -10 -194 '
                 'Q-80 -210 -136 -190 Q-170 -196 -200 -176Z" fill="#fff"/>')
    hang = "".join(gotgam_string(sx, -110, 5, 12, 5.2) for sx in strings)
    return group(x, y, s, False, 0, out + roof + hang)


def shed(x: float, y: float, s: float, night: bool = True, inside: str = "", snowy: bool = True) -> str:
    """An open-fronted cowshed of wood with a straw roof. (x, y) is the base; `inside` is drawn in its local coords."""
    inn = SHED_IN if night else SHED_IN_DAY
    out = (f'<rect x="-142" y="-204" width="284" height="204" fill="{inn}"/>'
           + stroke(" ".join(f"M{px} -200 V-4" for px in range(-120, 141, 30)), "#4D3B3C" if night else "#6A5242", 3)
           + f'<path d="M-142 0 Q-100 -26 -40 -16 Q20 -30 80 -14 Q120 -24 142 0Z" fill="{HAY}"/>'
           + inside
           + f'<rect x="-152" y="-206" width="16" height="206" fill="{POST}"/><rect x="136" y="-206" width="16" height="206" fill="{POST}"/>'
           + '<rect x="-160" y="-218" width="320" height="16" rx="3" fill="#7A5236"/>'
           + f'<path d="M-180 -210 L180 -210 Q172 -248 0 -262 Q-172 -248 -180 -210Z" fill="{STRAW}"/>'
           + stroke("M-170 -224 Q0 -240 170 -224", STRAW_D, 3) + stroke("M-180 -210 H180", STRAW_D, 7))
    if snowy:
        out += '<path d="M-168 -232 Q-150 -252 0 -264 Q150 -252 168 -232 Q100 -244 40 -238 Q-30 -250 -90 -238 Q-130 -244 -168 -232Z" fill="#fff"/>'
    return group(x, y, s, False, 0, out)


def window_shadow(stage: str) -> str:
    """Mother and baby's shadow on the paper window, in house coords (window x -150..-70, y -104..-36)."""
    sh = (f'<g fill="{SHADOW}" opacity=".6"><path d="M-146 -36 Q-146 -60 -126 -66 Q-108 -70 -94 -64 Q-80 -54 -76 -36Z"/>'
          '<circle cx="-114" cy="-80" r="13"/><circle cx="-128" cy="-86" r="7"/>')
    if stage == "gotgam":
        sh += '<circle cx="-92" cy="-66" r="9"/><circle cx="-78" cy="-74" r="5.5"/>' + stroke("M-110 -54 Q-92 -46 -80 -68", SHADOW, 5)
    else:
        sh += '<circle cx="-90" cy="-68" r="9"/>'
    return sh + '</g>'


# ---------------------------------------------------------------- scenery
def mountain(cx: float, top: float, w: float, base: float, col: str, cap: bool = True) -> str:
    out = f'<path d="M{cx - w} {base} L{cx} {top} L{cx + w} {base}Z" fill="{col}"/>'
    if cap:
        h = base - top
        out += (f'<path d="M{cx - w * .3:.0f} {top + h * .3:.0f} L{cx} {top} L{cx + w * .3:.0f} {top + h * .3:.0f} '
                f'L{cx + w * .14:.0f} {top + h * .24:.0f} L{cx} {top + h * .33:.0f} L{cx - w * .14:.0f} {top + h * .24:.0f}Z" fill="#fff" opacity=".9"/>')
    return out


def pine(x: float, y: float, s: float = 1, snowy: bool = True) -> str:
    inner = '<rect x="-7" y="-24" width="14" height="26" fill="#6B4630"/>'
    for (w, b, t), col in zip([(46, -20, -86), (38, -62, -124), (28, -100, -156)], (PINE_D, PINE, PINE)):
        inner += f'<path d="M{-w} {b} L0 {t} L{w} {b}Z" fill="{col}"/>'
        if snowy:
            inner += f'<path d="M{-w * .7:.0f} {b - 6} Q0 {b - 18} {w * .7:.0f} {b - 6} Q0 {b - 10} {-w * .7:.0f} {b - 6}Z" fill="#fff"/>'
    return group(x, y, s, False, 0, inner)


def snowfield(y: float, amp: float, col: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{col}"/>'


def moon(x: float, y: float, r: float) -> str:
    return (f'<circle cx="{x}" cy="{y}" r="{r * 1.8:.0f}" fill="#FFF4C9" opacity=".12"/><circle cx="{x}" cy="{y}" r="{r * 1.35:.0f}" fill="#FFF4C9" opacity=".16"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF4C9"/><circle cx="{x - r * .3:.0f}" cy="{y + r * .2:.0f}" r="{r * .16:.1f}" fill="#EDE0A8"/>'
            f'<circle cx="{x + r * .35:.0f}" cy="{y - r * .25:.0f}" r="{r * .11:.1f}" fill="#EDE0A8"/>')


def snowflakes(seed: int, n: int = 40, top: float = 0, bottom: float = 600) -> str:
    rnd = random.Random(seed)
    return '<g fill="#fff" opacity=".85">' + "".join(
        f'<circle cx="{rnd.uniform(10, 790):.0f}" cy="{rnd.uniform(top, bottom):.0f}" r="{rnd.choice((2, 2.5, 3, 3.5)):.1f}"/>' for _ in range(n)) + '</g>'


def stars(seed: int, n: int = 14, bottom: float = 220) -> str:
    rnd = random.Random(seed)
    return '<g fill="#FFF4C9">' + "".join(
        f'<circle cx="{rnd.uniform(20, 780):.0f}" cy="{rnd.uniform(16, bottom):.0f}" r="{rnd.choice((1.4, 1.8, 2.4)):.1f}"/>' for _ in range(n)) + '</g>'


def cries(x: float, y: float, k: float) -> str:
    """Wavy 'waaah' lines spilling out of the window."""
    return stroke(f"M{x} {y} q{12 * k} {-10 * k} {24 * k} 0 t{24 * k} 0 M{x + 6} {y - 26 * k} q{12 * k} {-10 * k} {24 * k} 0 t{24 * k} 0 "
                  f"M{x + 12} {y - 52 * k} q{10 * k} {-8 * k} {20 * k} 0", "#fff", 4 + k)


def puffs(pts: list) -> str:
    return '<g fill="#fff" opacity=".9">' + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>'


def prints(pts: list, col: str = SNOW_SH) -> str:
    return f'<g fill="{col}">' + "".join(f'<ellipse cx="{a}" cy="{b}" rx="9" ry="4"/>' for a, b in pts) + '</g>'


def bubble(x: float, y: float, rx: float, ry: float) -> str:
    lobes = "".join(f'<circle cx="{x + rx * math.cos(a):.0f}" cy="{y + ry * math.sin(a):.0f}" r="{ry * .42:.0f}"/>'
                    for a in [i * math.pi / 5 for i in range(10)])
    return f'<g fill="#fff" filter="url(#p)">{lobes}<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/></g>'


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + "\n".join(body) + '\n</g>\n</svg>\n')
    with open(f"{OUT}/persimmon-{n:02d}.svg", "w") as fh:
        fh.write(doc)


FAR_MTNS = [mountain(120, 200, 230, 470, MTN_N2), mountain(420, 150, 260, 470, MTN_N), mountain(700, 210, 220, 470, MTN_N2)]

# 01 cover — the tiger in the snow, staring at the gotgam hanging under a cottage roof
svg(1, "The Tiger and the Dried Persimmon", "Paper-cut cover: on a snowy moonlit night in the Korean mountains, a big orange-and-black striped tiger stands in the snow and stares in surprise at a little village cottage with a thick straw roof and glowing paper windows. Strings of orange dried persimmons hang under the cottage's snowy eaves.", NIGHT, [
    stars(1), moon(110, 100, 42), *FAR_MTNS, pine(40, 470, .8),
    snowfield(470, 14, SNOW_N), house(540, 476, 1.1),
    prints([(30, 560), (60, 548), (90, 566)]), tiger(190, 540, 1.1 * HOUSE_K, "oh"), snowflakes(1, 46)])

# 02 the hungry tiger comes down the mountain
svg(2, "A hungry tiger", "Paper-cut scene: on a cold, snowy night a big orange tiger with black stripes strides down a snowy mountainside between dark pine trees, his mouth open in a big friendly ROAR. Far below in the valley, the little windows of a village glow yellow.", NIGHT, [
    stars(2), moon(650, 90, 36), mountain(160, 170, 260, 430, MTN_N), mountain(560, 200, 280, 430, MTN_N2),
    snowfield(430, 10, "#C7D1EA", False),
    *[f'<path d="M{a - 22} 470 Q{a} 444 {a + 22} 470Z" fill="{STRAW_D}"/><rect x="{a - 5}" y="460" width="9" height="8" fill="{GLOW}"/>' for a in (590, 640, 700, 742)],
    f'<path filter="url(#p)" d="M0 330 Q260 380 560 470 Q700 520 800 520 V600 H0Z" fill="{SNOW_N}"/>',
    pine(70, 380, 1.2), pine(150, 420, .95), pine(560, 492, .9),
    tiger(330, 470, 1.25, "roar"), prints([(560, 590), (520, 574)]), snowflakes(2, 50)])

# 03 he creeps to the village: a cottage and a cowshed
C3 = .85 * HOUSE_K
svg(3, "Creeping to the village", "Paper-cut scene: the tiger tiptoes through the snow towards a village cottage with a thick snowy straw roof, glowing paper windows and strings of dried persimmons under its eaves, and a wooden cowshed beside it where a brown cow is standing inside. His paw prints trail behind him.", NIGHT, [
    stars(3), moon(90, 80, 32), *FAR_MTNS, snowfield(470, 12, SNOW_N),
    house(210, 478, .85), shed(612, 478, C3 / SHED_K, inside=cow(-10, -4, SHED_K)),
    prints([(30, 560), (70, 572), (110, 556), (150, 570), (190, 560)]),
    tiger(330, 560, C3 * 1.15, "smile", pose="crouch"), snowflakes(3, 40)])

YARD = [stars(4, 6, 100), snowfield(520, 6, SNOW_N), pine(70, 520, 1.0)]
CLOSE_HOUSE = dict(strings=(-40, -172, 110))

# 04 the baby is crying
svg(4, "A baby is crying", "Paper-cut scene: close up at the cottage wall, the tiger stands under a glowing paper window, listening. On the window paper is the soft shadow of a mother rocking her baby, and wavy crying lines spill out of the window. Strings of dried persimmons hang from the snowy straw eaves.", NIGHT, [
    *YARD, house(830, 520, 2.5, window=window_shadow("cry"), **CLOSE_HOUSE), cries(667, 262, 1.4),
    tiger(230, 562, 2.5 * HOUSE_K, "smile"), snowflakes(4, 30)])

# 05 "a tiger is coming!" — the baby cries even louder
svg(5, "Not scared of a tiger", "Paper-cut scene: under the glowing paper window, the tiger frowns in surprise with a flat little mouth, as even bigger crying lines pour out of the window where the shadow of the mother rocks her baby.", NIGHT, [
    *YARD, house(830, 520, 2.5, window=window_shadow("cry"), **CLOSE_HOUSE), cries(667, 254, 1.5), cries(380, 230, 1.1),
    tiger(230, 562, 2.5 * HOUSE_K, "huh"), snowflakes(5, 30)])

# 06 "here's a gotgam!" — the baby stops crying
svg(6, "Here's a gotgam!", "Paper-cut scene: the crying lines have gone. On the window paper, the shadow of the mother holds a small round dried persimmon up to her baby, and all is quiet. Outside, the tiger's eyes are wide and his mouth is a small round O. Right beside him, strings of real dried persimmons hang under the eaves.", NIGHT, [
    *YARD, house(830, 520, 2.5, window=window_shadow("gotgam"), **CLOSE_HOUSE),
    tiger(230, 562, 2.5 * HOUSE_K, "oh"), snowflakes(6, 30)])

# 07 the tiger imagines a terrible gotgam
svg(7, "What is a gotgam?", "Paper-cut scene: the tiger backs away from the cottage, shivering, his eyes huge and his mouth wobbly. In a big white thought bubble he imagines a gotgam as a silly giant orange monster with a leafy hat, round silly eyebrows, goggly eyes, big square teeth and little waving arms. The strings of real dried persimmons hang quietly under the eaves behind him.", NIGHT, [
    *YARD, house(830, 520, 2.5, window=window_shadow("gotgam"), **CLOSE_HOUSE),
    tiger(440, 562, 2.5 * HOUSE_K, "scared", flip=True, shake=True),
    '<g fill="#fff" filter="url(#p)"><circle cx="196" cy="318" r="11"/><circle cx="186" cy="286" r="16"/></g>',
    snowflakes(7, 24), bubble(220, 160, 150, 100), monster(220, 172, .9)])  # snow behind the bubble so no flake lands on the monster

# 08 he hides in the cowshed behind the cow (shed at 2.0, so characters at 2.0 * 0.62 = 1.24)
svg(8, "Hiding in the cowshed", "Paper-cut scene: inside a dark wooden cowshed with straw on the floor, a brown cow turns her face in surprise with her mouth open in a 'Moo?'. In front of her, the big tiger crouches low in the straw, trembling, with his tail tucked down and his eyes wide.", NIGHT, [
    snowfield(560, 4, SNOW_N, False),
    shed(400, 590, 2.0, inside=cow(-54, -8, SHED_K, "oh", True) + tiger(44, -2, SHED_K, "scared", True, "crouch", shake=True)),
    snowflakes(8, 12, 0, 80)])

# 09 the cow thief sneaks up
C9 = 1.4 * SHED_K
svg(9, "A sneaky cow thief", "Paper-cut scene: a silly sneaky man in a grey-blue jacket and a dark headscarf tiptoes through the snow with an empty sack over his shoulder, heading for the dark cowshed. He has a sly little smile. Inside the shed, the cow and the crouching tiger are just dim shapes in the dark.", NIGHT, [
    stars(9), moon(700, 80, 32), *FAR_MTNS, snowfield(480, 10, SNOW_N),
    shed(540, 482, 1.4, inside=f'<g opacity=".55">{cow(-66, -4, SHED_K) + tiger(60, -4, SHED_K, "scared", True, "crouch")}</g>'),
    prints([(30, 586), (70, 576), (110, 588)]), thief(180, 572, C9 * 1.1), snowflakes(9, 34)])

# 10 thump! the thief lands on the tiger's back (tiger nearer the viewer than the shed)
svg(10, "Thump!", "Paper-cut scene: in front of the cowshed, the sneaky thief has jumped onto the tiger's back thinking he is a big cow, and sits there grinning and holding on. The tiger's eyes are huge with fright and he is trembling all over. Inside the shed, the real cow watches with her mouth open.", NIGHT, [
    stars(10, 8, 120), moon(110, 80, 30), snowfield(470, 8, SNOW_N),
    shed(630, 470, 1.3, inside=cow(-30, -4, SHED_K, "oh")),
    tiger(320, 570, 1.1, "scared", rider=thief_rider("sneaky"), shake=True),
    puffs([(220, 570, 12), (250, 578, 9), (430, 576, 11)]), snowflakes(10, 30)])

# 11 run, run, run through the snow
svg(11, "Run, run, run!", "Paper-cut scene: under the moon, the frightened tiger gallops across a snowy field past pine trees, with snow puffing up behind his paws. The thief clings to the tiger's back with his eyes squeezed shut and his mouth wide open, having a very fast, bumpy ride.", NIGHT, [
    stars(11), moon(640, 90, 34), mountain(200, 210, 260, 430, MTN_N2), mountain(560, 180, 280, 430, MTN_N),
    snowfield(430, 10, SNOW_N), pine(720, 440, 1.0), pine(640, 430, .7),
    tiger(360, 520, 1.15, "scared", pose="run", rider=thief_rider("whee")),
    puffs([(120, 520, 16), (90, 500, 11), (150, 540, 10), (60, 530, 8)]),
    stroke("M40 420 h70 M30 452 h90 M60 484 h60", "#fff", 4, .7), snowflakes(11, 36)])

# 12 the thief sees stripes, tumbles into a snowdrift; the tiger runs off towards the mountains
svg(12, "A TIGER!", "Paper-cut scene: at dawn, as the sky turns pink, the thief has tumbled off into a soft snowdrift and sits up in it, wide-eyed, with his arms in the air, snow on his head and a puff of snow flying around him. His empty sack lies nearby. Further off on the right, the tiger races away towards the mountains, still frightened.", DAWN, [
    mountain(560, 170, 300, 440, MTN_D), mountain(240, 220, 240, 440, MTN_D2),
    snowfield(440, 10, SNOW), pine(740, 450, .8), pine(680, 440, .6),
    tiger(560, 500, .75, "scared", pose="run"), puffs([(450, 500, 10), (430, 488, 7)]),
    thief_sitting(230, 548, 1.2), f'<path filter="url(#p)" d="M90 600 Q110 548 230 540 Q350 548 380 600Z" fill="#EAF0FA"/>',
    '<ellipse cx="420" cy="570" rx="26" ry="14" fill="#A57C52" filter="url(#p)"/>',
    puffs([(150, 520, 12), (310, 516, 13), (170, 470, 8), (296, 452, 9), (130, 494, 7), (330, 486, 7)])])

# 13 morning: the baby munches a gotgam, the cow is safe, the tiger peeks from far up the mountain
svg(13, "Morning", "Paper-cut scene: on a bright snowy morning, the mother in a pink and cream hanbok stands outside the cottage holding her baby, who happily munches a dried persimmon. The cow looks out of the cowshed, safe and sound. Far, far away up on the snowy mountain, a tiny tiger peeks out between two pine trees.", MORNING, [
    mountain(620, 170, 280, 430, MTN_D2), mountain(330, 110, 320, 430, MTN_D),
    pine(320, 196, .42), tiger(304, 188, .15, "oh"), pine(342, 202, .38),
    snowfield(470, 12, SNOW), house(230, 500, 1.1, night=False),
    shed(650, 500, 1.1 * HOUSE_K / SHED_K, night=False, inside=cow(-20, -4, SHED_K)),
    mother(330, 570, 1.1 * HOUSE_K * 1.3)])
