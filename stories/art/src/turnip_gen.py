#!/usr/bin/env python3
"""Generates the 13 Enormous Turnip flip-book SVGs from shared character parts.

Usage: python3 turnip_gen.py <output-dir>

Every character is drawn standing on its own feet at (x, ground). When a character
pulls, it leans back and its hands are aimed at a point on the page (the turnip's
leaf stems, or the back of the waist of the one in front), so the chain always joins.
Purple is reserved for the turnip.
"""
import math
import sys

OUT = sys.argv[1]
INK, CREAM, SKIN, SKIN_D = "#2B2320", "#FFF6E6", "#F3C9A0", "#C98F62"
RED, RED_D, GOLD = "#D8433A", "#A9302A", "#F6C445"
SHIRT, SHIRT_D, TROUS, BOOT, CAP, BEARD = "#3F6FB0", "#2F5488", "#6B4A36", "#3A2A22", "#5B4636", "#F4F1EA"
DRESS, DRESS_D = "#3E8E5A", "#2E6E45"
SARAFAN, SARAFAN_D, HAIR, RIBBON = "#E25563", "#B83A4A", "#F2C14E", "#2F80D0"
DOG, DOG_D, DOG_L = "#B07A4A", "#7A5234", "#E8C9A0"
CAT, CAT_D, CAT_L = "#F09A3E", "#C8702A", "#FBE0BE"
MOUSE, MOUSE_D, PINK = "#A7A2B0", "#857F90", "#F2A9B0"
T_BULB, T_TOP, T_TOP_D = "#F6EEDC", "#9B5BA8", "#7A4388"
LEAF_D, LEAF_L, G_MID, G_FAR = "#3F9A56", "#6CC266", "#5DB85C", "#A9DB8E"
SOIL, SOIL_D, SOIL_L = "#8A5E3C", "#6E4A2E", "#A47148"
WOOD, WOOD_D = "#B7814F", "#8E5F38"

SPRING = [(0, "#9ED6EE"), (1, "#F4F7DA")]
SUMMER = [(0, "#7CC4E8"), (1, "#FDF1C8")]
HOT = [(0, "#8ED3E6"), (1, "#FFE9B0")]
DUSK = [(0, "#F2A07B"), (1, "#FCE3B4")]
GROUND = 505


def n(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{n(w)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


# ---------- geometry ----------

def to_page(p: tuple, x: float, y: float, s: float, rot: float) -> tuple:
    a = math.radians(rot)
    return (x + s * (p[0] * math.cos(a) - p[1] * math.sin(a)), y + s * (p[0] * math.sin(a) + p[1] * math.cos(a)))


def to_local(p: tuple, x: float, y: float, s: float, rot: float) -> tuple:
    a = math.radians(-rot)
    dx, dy = (p[0] - x) / s, (p[1] - y) / s
    return (dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a))


def joint(a: tuple, b: tuple, half: float, side: float = 1) -> tuple:
    """The elbow/knee between a and b for two segments of length `half`, bent towards +y (side=1) or -y."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1
    bend = math.sqrt(max(0.0, half * half - d * d / 4))
    px, py = -dy / d, dx / d
    if py * side < 0:
        px, py = -px, -py
    return (mx + px * bend, my + py * bend)


def pt(p: tuple) -> str:
    return f"{n(p[0])} {n(p[1])}"


def shade(col: str) -> str:
    """A slightly darker copy of a colour, for the far arm and far leg."""
    r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(c * .82):02X}" for c in (r, g, b))


# ---------- characters ----------
# hip/sh: hip and shoulder heights; head: head centre; grab: the back of the waist the next helper holds;
# arm: full arm length; base: built-in size (Granddaughter is smaller than the grown-ups);
# stance: front and back foot offsets when pulling.
SPEC = {
    "pa": dict(hip=-60, sh=-112, head=(2, -140), grab=(-20, -80), arm=64, base=1, sleeve=SHIRT, hand=SKIN, leg=TROUS, foot=BOOT, lw=13, stance=(24, -20)),
    "ma": dict(hip=-60, sh=-110, head=(2, -138), grab=(-22, -78), arm=62, base=.96, sleeve=DRESS, hand=SKIN, leg="#5A3E36", foot=BOOT, lw=10, stance=(22, -20)),
    "girl": dict(hip=-46, sh=-90, head=(2, -116), grab=(-19, -64), arm=50, base=.84, sleeve=CREAM, hand=SKIN, leg=CREAM, foot=RED, lw=9, stance=(18, -16)),
    "dog": dict(hip=-30, sh=-68, head=(6, -94), grab=(-21, -46), arm=36, base=1, sleeve=DOG, hand=DOG, leg=DOG, foot=DOG_D, lw=11, stance=(14, -12)),
    "cat": dict(hip=-22, sh=-52, head=(4, -75), grab=(-17, -30), arm=30, base=1, sleeve=CAT, hand=CAT, leg=CAT, foot=CAT_D, lw=9, stance=(11, -9)),
    "mouse": dict(hip=-8, sh=-20, head=(2, -32), grab=(-8, -12), arm=14, base=1, sleeve=MOUSE, hand=PINK, leg=MOUSE, foot=PINK, lw=4, stance=(5, -4)),
}
ORDER = ["pa", "ma", "girl", "dog", "cat", "mouse"]
LEAN = {"pa": -20, "ma": -19, "girl": -17, "dog": -14, "cat": -13, "mouse": -10}
HUMAN = ("pa", "ma", "girl")
MOUSE_S = 1.3                  # Mouse is drawn at this one size on every page


def eyes_svg(eyes: str, r: float, gap: float, ey: float, look: tuple) -> str:
    lx, ly = look
    w = max(1.4, r * .42)
    if eyes == "happy":
        return stroke(f"M{n(-gap - r)} {n(ey)} q{n(r)} {n(-r * 1.2)} {n(2 * r)} 0 M{n(gap - r)} {n(ey)} q{n(r)} {n(-r * 1.2)} {n(2 * r)} 0", INK, w)
    if eyes == "shut":   # squeezed tight with effort: > <
        return stroke(f"M{n(-gap - r)} {n(ey - r * .8)} l{n(r * 1.6)} {n(r * .8)} l{n(-r * 1.6)} {n(r * .8)} "
                      f"M{n(gap + r)} {n(ey - r * .8)} l{n(-r * 1.6)} {n(r * .8)} l{n(r * 1.6)} {n(r * .8)}", INK, w)
    out = "".join(f'<circle cx="{n(ex)}" cy="{n(ey)}" r="{n(r)}" fill="#fff"/><circle cx="{n(ex + lx * r / 6)}" cy="{n(ey + ly * r / 6)}" r="{n(r * .52)}" fill="{INK}"/>'
                  f'<circle cx="{n(ex + lx * r / 6 + r * .2)}" cy="{n(ey + ly * r / 6 - r * .24)}" r="{n(r * .17)}" fill="#fff"/>' for ex in (-gap, gap))
    if eyes == "sad":
        out += stroke(f"M{n(-gap - r)} {n(ey - r * 1.3)} L{n(-gap + r)} {n(ey - r * 1.8)} M{n(gap + r)} {n(ey - r * 1.3)} L{n(gap - r)} {n(ey - r * 1.8)}", INK, max(1.4, r * .35))
    return out


def mouth_svg(mouth: str, w: float, my: float, col: str = "#8C4A3B") -> str:
    if mouth == "open":
        return f'<path d="M{n(-w)} {n(my - 1)} Q0 {n(my + w * 1.8)} {n(w)} {n(my - 1)}Z" fill="#B5483F"/>'
    if mouth == "strain":
        return f'<rect x="{n(-w)}" y="{n(my - w * .4)}" width="{n(2 * w)}" height="{n(w * .8)}" rx="{n(w * .3)}" fill="#fff" stroke="{col}" stroke-width="{n(max(1, w * .25))}"/>'
    if mouth == "puff":
        return f'<ellipse cy="{n(my + 1)}" rx="{n(w * .5)}" ry="{n(w * .6)}" fill="#B5483F"/>'
    return stroke(f"M{n(-w)} {n(my)} Q0 {n(my + w)} {n(w)} {n(my)}", col, max(1.2, w * .4))


def cheeks(dx: float, cy: float, r: float) -> str:
    return f'<g fill="#F08A7A" opacity=".45"><circle cx="{-dx}" cy="{cy}" r="{r}"/><circle cx="{dx}" cy="{cy}" r="{r}"/></g>'


def head(kind: str, eyes: str, mouth: str, look: tuple) -> str:
    """Front-facing heads, centred on (0, 0)."""
    if kind == "pa":
        return (f'<circle r="22" fill="{SKIN}"/><g fill="{BEARD}"><circle cx="-21" cy="-2" r="7"/><circle cx="21" cy="-2" r="7"/>'
                '<path d="M-21 0 Q-24 30 0 38 Q24 30 21 0 Q12 10 0 10 Q-12 10 -21 0Z"/></g>'
                f'<path d="M-23 -10 Q-22 -32 2 -32 Q26 -32 24 -10 Z" fill="{CAP}"/><path d="M4 -14 Q22 -16 34 -9 Q22 -6 4 -9Z" fill="#4A382B"/>'
                + eyes_svg(eyes, 5.5, 8, -3, look) + cheeks(14, 5, 4.5) + '<ellipse cy="4" rx="3.6" ry="3" fill="#E0A678"/>'
                + '<path d="M0 9 Q-8 6 -14 11 Q-6 14 0 11 Q6 14 14 11 Q8 6 0 9Z" fill="#fff"/>' + mouth_svg(mouth, 4.5, 15))
    if kind == "ma":
        dots = "".join(f'<circle cx="{a}" cy="{b}" r="2" fill="#fff"/>' for a, b in [(-16, -14), (-6, -22), (6, -22), (16, -14), (-24, 4), (24, 4)])
        return (f'<circle r="27" fill="{RED}"/><path d="M-6 20 L-18 40 L-2 30Z M6 20 L18 40 L2 30Z" fill="{RED_D}"/>'
                f'<circle r="21" fill="{SKIN}"/>'
                f'<path d="M-24 -2 Q-24 -28 0 -28 Q24 -28 24 -2 Q14 -15 0 -15 Q-14 -15 -24 -2Z" fill="{RED}"/>' + dots
                + '<path d="M-15 -14 Q0 -20 15 -14 Q0 -10 -15 -14Z" fill="#E9E8EF"/>'
                + eyes_svg(eyes, 5.5, 8, -2, look) + cheeks(13, 7, 4.5) + '<ellipse cy="5" rx="3.2" ry="2.6" fill="#E0A678"/>'
                + mouth_svg(mouth, 4.5, 12) + f'<circle cy="22" r="5" fill="{RED_D}"/>')
    if kind == "girl":
        braid = "".join(f'<ellipse cx="{n(-20 - i * 2.5)}" cy="{n(12 + i * 11)}" rx="7" ry="7.5" fill="{HAIR}"/>' for i in range(4))
        return (braid + f'<path d="M-40 52 l10 -6 l10 6 l-10 4z" fill="{RIBBON}"/><circle r="24" fill="{HAIR}"/><circle cy="3" r="20" fill="{SKIN}"/>'
                f'<path d="M-22 -2 Q-20 -22 0 -22 Q22 -22 22 -2 Q16 -12 6 -11 Q4 -6 -2 -11 Q-12 -12 -22 -2Z" fill="{HAIR}"/>'
                f'<path d="M14 -18 l12 -8 l-2 12z M14 -18 l14 4 l-12 6z" fill="{RIBBON}"/>'
                + eyes_svg(eyes, 6, 8, 2, look) + cheeks(13, 10, 4.5) + '<ellipse cy="8" rx="2.6" ry="2" fill="#E0A678"/>' + mouth_svg(mouth, 4, 14))
    if kind == "dog":
        return (f'<g fill="{DOG_D}"><path d="M-16 -12 Q-34 -8 -30 22 Q-20 22 -12 4Z"/><path d="M16 -12 Q34 -8 30 22 Q20 22 12 4Z"/></g>'
                f'<circle r="20" fill="{DOG}"/><ellipse cx="7" cy="-8" rx="7" ry="6" fill="{DOG_D}"/>'
                f'<ellipse cy="9" rx="12" ry="9" fill="{DOG_L}"/><ellipse cy="4" rx="5" ry="3.6" fill="{INK}"/>'
                + eyes_svg(eyes, 5, 8, -6, look) + mouth_svg(mouth, 4, 12, INK)
                + ('<path d="M-3 14 q3 10 6 0z" fill="#E86A7A"/>' if mouth in ("open", "smile") else ""))
    if kind == "cat":
        stripes = stroke("M-5 -16 l2 6 M0 -17 v6 M5 -16 l-2 6", CAT_D, 2.4)
        return (f'<path d="M-16 -6 L-14 -26 L-2 -14Z M16 -6 L14 -26 L2 -14Z" fill="{CAT}"/><path d="M-13 -9 L-12 -20 L-6 -13Z M13 -9 L12 -20 L6 -13Z" fill="{PINK}"/>'
                f'<circle r="17" fill="{CAT}"/>' + stripes + f'<ellipse cy="7" rx="9" ry="6.5" fill="{CAT_L}"/><path d="M-2.6 3 h5.2 l-2.6 3z" fill="#E86A7A"/>'
                + eyes_svg(eyes, 4.6, 7, -3, look) + mouth_svg(mouth, 3, 10, INK)
                + stroke("M-7 6 l-12 -2 M-7 9 l-12 3 M7 6 l12 -2 M7 9 l12 3", "#fff", 1.3))
    return (f'<g fill="{MOUSE}"><circle cx="-7" cy="-7" r="6.5"/><circle cx="7" cy="-7" r="6.5"/></g><g fill="{PINK}"><circle cx="-7" cy="-7" r="3.8"/><circle cx="7" cy="-7" r="3.8"/></g>'
            f'<circle r="9" fill="{MOUSE}"/>' + eyes_svg(eyes, 2.6, 3.6, -1, look) + '<circle cy="3.4" r="1.8" fill="#F2859A"/>'
            + stroke("M-3 4 l-8 -1.5 M-3 5.5 l-8 1.5 M3 4 l8 -1.5 M3 5.5 l8 1.5", "#6E6878", .8) + mouth_svg(mouth, 2, 6.5))


def torso(kind: str, sit: bool = False) -> str:
    """The body in local coordinates, feet at y=0. Sitting skirts become a lap over the knees."""
    if sit and kind == "ma":
        return (f'<path d="M-18 -114 Q-20 -118 -10 -118 H12 Q22 -118 20 -114 L26 -62 H-26Z" fill="{DRESS}"/>'
                f'<path d="M-30 -74 H30 Q62 -76 66 -60 Q66 -50 56 -50 H-24 Q-32 -50 -32 -58Z" fill="{DRESS}"/>'
                f'<path d="M-4 -88 H22 L24 -66 Q40 -66 46 -54 H-2Z" fill="{CREAM}"/>' + stroke("M-4 -88 H22", RED, 4))
    if sit and kind == "girl":
        return (f'<path d="M-15 -92 Q-16 -96 -8 -96 H10 Q18 -96 16 -92 L20 -50 H-20Z" fill="{CREAM}"/>'
                + stroke("M-12 -84 L-6 -96 M10 -96 L14 -84", SARAFAN, 5)
                + f'<path d="M-14 -84 H16 L20 -60 Q46 -62 50 -48 Q50 -40 42 -40 H-18 Q-24 -40 -24 -46Z" fill="{SARAFAN}"/>'
                + stroke("M-20 -44 H46", GOLD, 4))
    if kind == "pa":
        return (f'<path d="M-20 -116 Q-22 -120 -12 -120 H14 Q24 -120 22 -116 L26 -60 Q26 -54 18 -54 H-18 Q-26 -54 -26 -60Z" fill="{SHIRT}"/>'
                + stroke("M6 -118 V-96", SHIRT_D, 3) + f'<g fill="{CREAM}"><circle cx="9" cy="-110" r="2"/><circle cx="9" cy="-102" r="2"/></g>'
                + f'<rect x="-26" y="-74" width="52" height="7" rx="3" fill="{RED}"/><path d="M-22 -67 l-4 12 l8 -2z" fill="{RED}"/>')
    if kind == "ma":
        return (f'<path d="M-18 -114 Q-20 -118 -10 -118 H12 Q22 -118 20 -114 L34 -24 Q34 -16 24 -16 H-24 Q-34 -16 -34 -24Z" fill="{DRESS}"/>'
                f'<path d="M-6 -88 H22 L28 -26 Q28 -22 22 -22 H0 Q-8 -22 -8 -26Z" fill="{CREAM}"/>'
                + stroke("M-6 -88 H22", RED, 4) + stroke("M-6 -34 Q11 -30 28 -34", RED, 3)
                + f'<g fill="{RED}"><circle cx="4" cy="-60" r="3"/><circle cx="16" cy="-50" r="3"/><circle cx="6" cy="-44" r="2.4"/></g>')
    if kind == "girl":
        return (f'<path d="M-15 -92 Q-16 -96 -8 -96 H10 Q18 -96 16 -92 L28 -26 Q28 -20 20 -20 H-20 Q-28 -20 -28 -26Z" fill="{CREAM}"/>'
                + stroke("M-12 -84 L-6 -96 M10 -96 L14 -84", SARAFAN, 5)
                + f'<path d="M-14 -84 H16 L28 -26 Q28 -20 20 -20 H-20 Q-28 -20 -28 -26Z" fill="{SARAFAN}"/>'
                + stroke("M-25 -32 H26", GOLD, 4) + f'<g fill="{GOLD}"><circle cx="1" cy="-74" r="2.6"/><circle cx="1" cy="-62" r="2.6"/><circle cx="1" cy="-50" r="2.6"/></g>')
    if kind == "dog":
        return (stroke("M-18 -40 Q-40 -50 -36 -76", DOG, 8) + f'<ellipse cy="-50" rx="24" ry="30" fill="{DOG}"/><ellipse cx="6" cy="-46" rx="13" ry="20" fill="{DOG_L}"/>'
                + f'<path d="M-14 -76 Q6 -84 22 -74 L18 -68 Q4 -76 -12 -70Z" fill="{RED}"/>')
    if kind == "cat":
        return (stroke("M-16 -16 Q-46 -14 -42 -48 Q-40 -64 -28 -62", CAT, 8) + stroke("M-41 -44 l7 3 M-40 -54 l7 1", CAT_D, 3)
                + f'<ellipse cy="-36" rx="19" ry="23" fill="{CAT}"/><ellipse cx="5" cy="-33" rx="10" ry="15" fill="{CAT_L}"/>'
                + stroke("M-17 -40 l7 2 M-18 -30 l7 1", CAT_D, 3))
    return (stroke("M-6 -6 Q-26 -2 -24 -20 Q-22 -30 -14 -30", PINK, 2.2)
            + f'<ellipse cy="-13" rx="9" ry="11" fill="{MOUSE}"/><ellipse cx="2.5" cy="-12" rx="5" ry="7" fill="#C9C5D1"/>')


def legs_svg(kind: str, pose: str, x: float, y: float, S: float, rot: float, hip: float) -> str:
    sp = SPEC[kind]
    if pose == "pull":
        fwd, bk = sp["stance"]
        feet = [to_local((x + fwd * S, y), x, y, S, rot), to_local((x + bk * S, y), x, y, S, rot)]
    elif pose == "sit":
        feet = [(-sp["hip"] * .95, -2), (-sp["hip"] * .7, -2)]
    else:
        feet = [(sp["stance"][0] * .35, 0), (-sp["stance"][0] * .35, 0)]
    skirt = kind in ("ma", "girl") and pose != "sit"
    out = ""
    for i, ft in enumerate(feet):
        h = (4 - 8 * i, hip + (18 if skirt else 0))
        half = math.hypot(ft[0] - h[0], ft[1] - h[1]) / 2 + 1 if skirt else -sp["hip"] / 2 + 1
        kn = joint(h, ft, half, -1 if pose == "sit" else 1)
        if pose == "pull" and i == 0:   # front knee bent forward
            kn = joint(h, ft, half + 4, -1)
            kn = (max(kn[0], (h[0] + ft[0]) / 2 + 4), kn[1])
        col = sp["leg"] if i == 0 else shade(sp["leg"])
        lw = sp["lw"]
        out = (stroke(f"M{pt(h)} L{pt(kn)} L{pt(ft)}", col, lw)
               + f'<ellipse cx="{n(ft[0] + lw * .35)}" cy="{n(ft[1] - lw * .3)}" rx="{n(lw * .8)}" ry="{n(lw * .5)}" fill="{sp["foot"]}"/>') + out
    return out


def figure(kind: str, x: float, y: float = GROUND, s: float = 1, rot: float = 0, pose: str = "stand",
           hp: tuple | None = None, hl: tuple | None = None, eyes: str = "open", mouth: str = "smile",
           look: tuple = (0, 0)) -> str:
    """One character with feet on (x, y), facing right. pose: stand / pull / sit.
    hp: two hand targets in page coordinates; hl: two hand targets in local coordinates."""
    sp = SPEC[kind]
    S = s * sp["base"]
    drop = (-sp["hip"] - (8 if kind != "mouse" else 2)) if pose == "sit" else 0
    hip, sh = sp["hip"] + drop, sp["sh"] + drop
    hx, hy = sp["head"][0], sp["head"][1] + drop
    if hp:
        hands = [to_local(p, x, y, S, rot) for p in hp]
    elif hl:
        hands = [(a, b + drop) for a, b in hl]
    else:
        hands = [(14, sh + sp["arm"] * .88), (-8, sh + sp["arm"] * .88)]
    arms = []
    for i, (sho, hd) in enumerate(zip([(6, sh + 4), (-6, sh + 4)], hands)):
        el = joint(sho, hd, sp["arm"] / 2, 1)
        col = sp["sleeve"] if i == 0 else shade(sp["sleeve"])
        hand = sp["hand"] if i == 0 else shade(sp["hand"])
        w = sp["lw"]
        fore = hand if kind in HUMAN else col
        arms.append(stroke(f"M{pt(sho)} L{pt(el)}", col, w) + stroke(f"M{pt(el)} L{pt(hd)}", fore, w * .75)
                    + f'<circle cx="{n(hd[0])}" cy="{n(hd[1])}" r="{n(w * .55)}" fill="{hand}"/>')
    hscale = 1.12 if kind == "girl" else 1
    raised = hands[0][1] < sh - sp["arm"] * .25
    body = (arms[1] + legs_svg(kind, pose, x, y, S, rot, hip) + f'<g transform="translate(0 {n(drop)})">{torso(kind, pose == "sit")}</g>'
            + (arms[0] if raised else "")
            + f'<g transform="translate({n(hx)} {n(hy)}) scale({hscale})">{head(kind, eyes, mouth, look)}</g>' + ("" if raised else arms[0]))
    return f'<g transform="translate({n(x)} {n(y)}) rotate({n(rot)}) scale({n(S)})" filter="url(#p)">{body}</g>'


def grab_point(kind: str, x: float, y: float, s: float, rot: float) -> tuple:
    sp = SPEC[kind]
    return to_page(sp["grab"], x, y, s * sp["base"], rot)


def place_behind(kind: str, target: tuple, s: float, rot: float, reach: float = 1.12, y: float = GROUND) -> float:
    """The x for a pulling helper whose shoulders sit `reach` of an arm behind the target."""
    sp = SPEC[kind]
    S = s * sp["base"]
    shx, _ = to_page((0, sp["sh"]), 0, y, S, rot)
    return target[0] - reach * sp["arm"] * S - shx


def chain(count: int, hold: tuple, s: float = 1, y: float = GROUND) -> list:
    """The first `count` helpers in order, each holding the one in front; Grandpa holds `hold`.
    Drawn front to back so each helper's hands land on top of the back they hold."""
    parts, target = [], hold
    for kind in ORDER[:count]:
        rot, sc = LEAN[kind], (MOUSE_S if kind == "mouse" else s)
        x = place_behind(kind, target, sc, rot, y=y)
        off = 3 * sc * SPEC[kind]["base"]
        e = "open" if kind == "mouse" else "shut"
        parts.append(figure(kind, x, y, sc, rot, "pull", hp=((target[0] + off, target[1] - off), (target[0] - off, target[1] + off)),
                            eyes=e, mouth="strain" if kind in HUMAN else "puff", look=(3, 0)))
        target = grab_point(kind, x, y, sc, rot)
    return parts


# ---------- the turnip ----------

def leaf(x: float, y: float, L: float, rot: float, col: str = LEAF_D) -> str:
    vein = "#2F7D45" if col == LEAF_L else LEAF_L
    return (f'<g transform="translate({n(x)} {n(y)}) rotate({n(rot)})"><path d="M0 0 Q{n(-L * .42)} {n(-L * .55)} 0 {n(-L)} Q{n(L * .42)} {n(-L * .55)} 0 0Z" fill="{col}"/>'
            + stroke(f"M0 {n(-L * .05)} V{n(-L * .8)}", vein, max(1.5, L * .03)) + '</g>')


def turnip(cx: float, cy: float, R: float, rot: float = 0, buried: bool = True, stems_to: tuple | None = None,
           ground: float = GROUND) -> str:
    """A cream-and-purple turnip of radius R centred on (cx, cy) with a crown of leaves.
    buried: soil heaped over the bottom. stems_to: page point the leaf stems are pulled towards."""
    L = max(26, R * 1.25)
    leaves = "".join(leaf(0, -R * .92, L * k, a, c) for a, k, c in
                     [(-46, .85, LEAF_D), (40, .9, LEAF_D), (-18, 1, LEAF_L), (14, 1.05, LEAF_D), (-2, .8, LEAF_L)])
    root = "" if buried else stroke(f"M0 {n(R)} q{n(R * .08)} {n(R * .3)} {n(-R * .05)} {n(R * .55)}", "#E6D7BA", max(3, R * .07))
    bulb = (root + f'<path d="M0 {n(-R)} C{n(R * .62)} {n(-R)} {n(R * 1.05)} {n(-R * .45)} {n(R)} {n(R * .12)} C{n(R * .95)} {n(R * .62)} {n(R * .35)} {n(R * .9)} 0 {n(R * 1.04)}'
            f' C{n(-R * .35)} {n(R * .9)} {n(-R * .95)} {n(R * .62)} {n(-R)} {n(R * .12)} C{n(-R * 1.05)} {n(-R * .45)} {n(-R * .62)} {n(-R)} 0 {n(-R)}Z" fill="{T_BULB}"/>'
            + f'<path d="M{n(-R * .99)} {n(-R * .05)} C{n(-R * .97)} {n(-R * .7)} {n(-R * .5)} {n(-R)} 0 {n(-R)} C{n(R * .5)} {n(-R)} {n(R * .97)} {n(-R * .7)} {n(R * .99)} {n(-R * .05)}'
            f' Q{n(R * .5)} {n(-R * .24)} 0 {n(-R * .12)} Q{n(-R * .5)} {n(0)} {n(-R * .99)} {n(-R * .05)}Z" fill="{T_TOP}"/>'
            + stroke(f"M{n(-R * .55)} {n(-R * .6)} Q{n(-R * .35)} {n(-R * .82)} {n(-R * .1)} {n(-R * .85)}", "#C79AD2", max(2, R * .06))
            + stroke(f"M{n(-R * .5)} {n(R * .35)} q{n(R * .1)} {n(R * .2)} {n(R * .3)} {n(R * .25)} M{n(R * .2)} {n(R * .55)} q{n(R * .12)} {n(-R * .05)} {n(R * .25)} {n(-R * .22)}",
                     "#E6D7BA", max(1.5, R * .03)))
    out = f'<g transform="translate({n(cx)} {n(cy)}) rotate({n(rot)})" filter="url(#p)">{leaves}{bulb}</g>'
    if stems_to:
        tx, ty = cx - R * .15, cy - R * .88
        hx, hy = stems_to
        out += (f'<g filter="url(#p)">' + stroke(f"M{n(tx)} {n(ty)} Q{n(tx - R * .75)} {n(ty - R * .05)} {n(hx)} {n(hy)}", "#2F7D45", 11)
                + stroke(f"M{n(tx + 8)} {n(ty + 2)} Q{n(tx - R * .6)} {n(ty + R * .05)} {n(hx + 3)} {n(hy + 4)}", LEAF_L, 7) + '</g>'
                + leaf(tx - R * .2, ty - 4, R * .55, -70, LEAF_L))
    if buried:
        w = R * 1.35
        out += (f'<path filter="url(#p)" d="M{n(cx - w)} {n(ground + 6)} Q{n(cx - w * .55)} {n(cy + R * .32)} {n(cx)} {n(cy + R * .28)} '
                f'Q{n(cx + w * .55)} {n(cy + R * .32)} {n(cx + w)} {n(ground + 6)} Q{n(cx)} {n(max(ground + 40, cy + R * 1.2))} {n(cx - w)} {n(ground + 6)}Z" fill="{SOIL_L}"/>'
                + "".join(f'<circle cx="{n(cx + a * R)}" cy="{n(cy + R * .42 + b * R)}" r="{n(max(2, R * .045))}" fill="{SOIL_D}"/>'
                          for a, b in [(-.7, .12), (-.2, .05), (.4, .1), (.85, .2), (0, .24)]))
    return out


# ---------- scenery ----------

def cloud(x: float, y: float, s: float = 1, fill: str = "#fff") -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" opacity=".92">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def sun(x: float, y: float, r: float = 44, face: bool = False) -> str:
    rays = "".join(f'<path d="M{n(-r * .14)} {n(-r * 1.15)} L0 {n(-r * 1.45)} L{n(r * .14)} {n(-r * 1.15)}Z" transform="rotate({30 * i})"/>' for i in range(12))
    f = ""
    if face:
        f = (eyes_svg("happy", r * .12, r * .3, -r * .1, (0, 0)) + cheeks(r * .5, r * .15, r * .1)
             + stroke(f"M{n(-r * .25)} {n(r * .22)} Q0 {n(r * .45)} {n(r * .25)} {n(r * .22)}", "#8A5318", r * .06))
    return (f'<g transform="translate({x} {y})"><circle r="{n(r * 1.7)}" fill="{GOLD}" opacity=".22"/><g fill="#F4A720">{rays}</g>'
            f'<circle r="{r}" fill="{GOLD}" filter="url(#p)"/><circle r="{n(r * .84)}" fill="#FBD764"/>{f}</g>')


def hill(y: float, amp: float, fill: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def birch(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#bi" transform="translate({x} {y}) scale({s})"/>'


def izba(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#iz" transform="translate({x} {y}) scale({s})"/>'


def fence(x1: float, x2: float, y: float, h: float = 60) -> str:
    posts = "".join(f'<path d="M{x} {y} v{-h} l9 -10 l9 10 v{h}Z"/>' for x in range(int(x1), int(x2), 26))
    return (f'<g filter="url(#p)">' + stroke(f"M{x1} {y - h * .3} H{x2} M{x1} {y - h * .75} H{x2}", WOOD_D, 7)
            + f'<g fill="{WOOD}">{posts}</g></g>')


def field(y: float = GROUND) -> str:
    """The vegetable garden: brown earth with furrows, and a grassy strip at the front."""
    rows = stroke(f"M0 {y + 28} Q400 {y + 18} 800 {y + 30} M0 {y + 58} Q400 {y + 48} 800 {y + 62}", SOIL_D, 4)
    return (f'<path filter="url(#p)" d="M0 {y - 16} Q400 {y - 34} 800 {y - 14} V600 H0Z" fill="{SOIL}"/>' + rows
            + f'<path d="M0 600 V{y + 76} Q400 {y + 60} 800 {y + 80} V600Z" fill="{LEAF_D}"/>')


def back(far: str = G_FAR, mid: str = G_MID, house: tuple | None = (150, 392, 1), trees: tuple = ((60, 400, 1.1), (745, 395, 1.2))) -> list:
    return [hill(350, 34, far, False), *([izba(*house)] if house else []), *[birch(*a) for a in trees], hill(415, 18, mid)]


def sprout(x: float, y: float, s: float = 1) -> str:
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{leaf(0, 0, 26, -30, LEAF_L)}{leaf(0, 0, 30, 25, LEAF_D)}</g>'


def drops(pts: list, fill: str = "#4FAEE0") -> str:
    return f'<g fill="{fill}">' + "".join(f'<path d="M{n(a)} {n(b)} q7 12 0 17 q-7 -5 0 -17z"/>' for a, b in pts) + '</g>'


def crumbs(pts: list) -> str:
    return f'<g fill="{SOIL_D}">' + "".join(f'<circle cx="{n(a)}" cy="{n(b)}" r="{r}"/>' for a, b, r in pts) + '</g>'


def star(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def spark(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#k" transform="translate({x} {y}) scale({s})"/>'


DEFS = {
    "bi": ('<g id="bi" filter="url(#p)"><g fill="#4F9A4E"><circle cx="-28" cy="-150" r="34"/><circle cx="20" cy="-170" r="38"/><circle cx="30" cy="-120" r="30"/>'
           '<circle cx="-14" cy="-206" r="30"/></g><g fill="#7CC96B"><circle cx="-6" cy="-180" r="22"/><circle cx="-34" cy="-128" r="16"/></g>'
           '<path d="M-8 0 L-6 -170 H6 L8 0Z" fill="#F4F1EA"/><g fill="#2B2320"><rect x="-6" y="-40" width="8" height="3" rx="1.5"/>'
           '<rect x="-1" y="-78" width="7" height="3" rx="1.5"/><rect x="-6" y="-112" width="6" height="3" rx="1.5"/><rect x="0" y="-140" width="6" height="3" rx="1.5"/></g></g>'),
    "iz": ('<g id="iz" filter="url(#p)"><rect x="-70" y="-90" width="140" height="90" fill="#A86B3E"/>'
           + stroke("M-70 -72 H70 M-70 -54 H70 M-70 -36 H70 M-70 -18 H70", "#8A5530", 3)
           + '<path d="M-84 -86 L0 -150 L84 -86Z" fill="#7A4A2A"/><path d="M-62 -92 L0 -138 L62 -92Z" fill="#C38A57"/>'
           '<path d="M-12 -110 h24 v16 h-24z" fill="#FFF6E6"/>'
           '<rect x="-26" y="-70" width="52" height="40" fill="#BFE3F2"/><path d="M-34 -78 h68 l-8 8 h-52z" fill="#2F80D0"/>'
           '<rect x="-38" y="-70" width="12" height="40" fill="#2F80D0"/><rect x="26" y="-70" width="12" height="40" fill="#2F80D0"/>'
           + stroke("M0 -70 V-30 M-26 -50 H26", "#FFF6E6", 3) + '<path d="M-30 -30 h60 l-6 8 h-48z" fill="#FFF6E6"/></g>'),
    "s": f'<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="{GOLD}"/>',
    "k": '<path id="k" d="M0 -10 Q1 -1 10 0 Q1 1 0 10 Q-1 1 -10 0 Q-1 -1 0 -10Z" fill="#fff"/>',
}


def svg(num: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    defs = "".join(d for k, d in DEFS.items() if f'href="#{k}"' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/turnip-{num:02d}.svg", "w") as fh:
        fh.write(doc)


# ---------- pages ----------
BIG = (650, 405, 120)          # the enormous turnip: centre x, centre y, radius
HOLD = (526, 404)              # where Grandpa grips the leaf stems
CX, CY, R = BIG


def garden(sky_sun: bool = True) -> list:
    return [*([sun(90, 80, 38)] if sky_sun else []), cloud(330, 90, 1.1), cloud(600, 70, .9),
            *back(trees=((60, 400, 1.1),)), fence(250, 800, 452), field()]


def pull_page(count: int, s: float = 1.3) -> list:
    return [*garden(), turnip(CX, CY, R, stems_to=HOLD), *chain(count, HOLD, s)]


# 01 cover — the whole family beside the enormous turnip, with Mouse sitting on top
svg(1, "The Enormous Turnip", "Paper-cut cover: an enormous purple-and-cream turnip with a crown of green leaves grows in a vegetable garden beside a wooden cottage and birch trees. Grandpa with his white beard, Grandma in her red headscarf, Granddaughter with her yellow braid, a brown dog and a ginger cat stand in a row and smile up at it, and a tiny grey mouse sits on top of the turnip.", SUMMER, [
    *garden(), turnip(*BIG),
    figure("mouse", CX - 6, CY - R * .9, MOUSE_S, pose="sit", hl=((10, -26), (-6, -14)), eyes="happy", mouth="open"),
    figure("cat", 160, GROUND + 18, 1.1, look=(3, -2)),
    figure("dog", 225, GROUND + 14, 1.05, look=(3, -2), mouth="open"),
    figure("girl", 300, GROUND + 10, 1, hl=((24, -136), (-8, -28)), look=(3, -2), mouth="open"),
    figure("ma", 385, GROUND + 6, 1, look=(3, -2)),
    figure("pa", 470, GROUND + 2, 1, hl=((44, -150), (-12, -36)), look=(3, -2))])

# 02 Grandpa plants a seed
svg(2, "Grandpa plants a seed", "Paper-cut spring scene: in the brown vegetable garden in front of a wooden cottage with a blue window, Grandpa with his white beard and cap bends down and drops one tiny seed into a little hole in the earth, with a green watering can beside him.", SPRING, [
    cloud(160, 110, 1.2), cloud(600, 80, 1), *back(), fence(330, 800, 452), field(),
    f'<ellipse cx="530" cy="{GROUND + 10}" rx="26" ry="8" fill="{SOIL_D}"/>',
    f'<ellipse cx="530" cy="492" rx="6" ry="8" fill="#E9D7A8" stroke="{INK}" stroke-width="1.5"/>',
    marks(["M508 486 l-10 -6", "M552 486 l10 -6"], INK, 2.5),
    figure("pa", 430, GROUND, 1.4, rot=10, hp=((536, 478), (440, 400)), look=(3, 3)),
    '<g filter="url(#p)" transform="translate(660 520)"><path d="M-30 0 L-26 -44 H26 L30 0Z" fill="#2FA36B"/><path d="M26 -36 L64 -64 L70 -58 L30 -24Z" fill="#2FA36B"/>'
    + stroke("M-22 -40 Q0 -76 22 -40", "#1E7F55", 6) + '</g>'])

# 03 sun, rain, growing
svg(3, "The sun shines and the rain falls", "Paper-cut scene: the smiling sun shines on one side of the sky and a grey rain cloud sprinkles blue raindrops on the other, while in the garden a round purple-topped turnip pushes up out of the earth with big leaves, growing bigger every day.", HOT, [
    sun(140, 110, 56, face=True), cloud(600, 110, 1.4, "#C9D6E2"),
    drops([(530, 170), (580, 200), (630, 175), (680, 205), (555, 245), (610, 260), (665, 240), (720, 180)]),
    *back(house=None, trees=((60, 400, 1.1), (360, 390, 1))), fence(0, 800, 452), field(),
    sprout(250, GROUND + 8, 1), sprout(690, GROUND + 10, 1.1),
    turnip(450, GROUND - 26, 50),
    marks(["M450 350 v-30", "M404 362 l-16 -20", "M496 362 l16 -20"], "#fff", 5)])

# 04 an ENORMOUS turnip
svg(4, "An enormous turnip", "Paper-cut scene: the turnip has grown ENORMOUS — a huge purple-and-cream turnip taller than Grandpa, with giant green leaves — and Grandpa stands beside it with both arms thrown up in surprise and his mouth wide open.", SUMMER, [
    *garden(), turnip(*BIG),
    figure("pa", 400, GROUND, 1.3, hl=((52, -184), (-44, -180)), look=(3, -3), mouth="open"),
    marks(["M326 252 l-18 -14", "M318 286 h-24", "M496 236 l16 -14", "M504 270 h22"], INK, 3.5)])

# 05-09 one more helper each time
svg(5, "Grandpa pulls", "Paper-cut scene: Grandpa grips the enormous turnip's leaf stems with both hands and leans far back, pulling with all his might, his eyes squeezed shut — but the turnip stays stuck in the ground.", SUMMER, pull_page(1))
svg(6, "Grandma helps", "Paper-cut scene: Grandma in her red headscarf holds Grandpa around the waist, and Grandpa holds the turnip's leaves; they both lean back and pull with their eyes squeezed shut, but the enormous turnip does not move.", SUMMER, pull_page(2))
svg(7, "Granddaughter helps", "Paper-cut scene: Granddaughter with her yellow braid holds Grandma, Grandma holds Grandpa, and Grandpa holds the turnip; all three lean back and pull, but the enormous turnip stays stuck.", SUMMER, pull_page(3))
svg(8, "Dog helps", "Paper-cut scene: a brown dog with floppy ears and a red collar holds Granddaughter, who holds Grandma, who holds Grandpa, who holds the turnip; they all lean back and pull, but the enormous turnip will not come out.", SUMMER, pull_page(4))
svg(9, "Cat helps", "Paper-cut scene: a ginger cat holds the dog, the dog holds Granddaughter, Granddaughter holds Grandma, Grandma holds Grandpa, and Grandpa holds the turnip; five helpers lean back and pull, and still the enormous turnip stays stuck.", SUMMER, pull_page(5))

# 10 everyone sits down, puffing — and a tiny mouse arrives
svg(10, "A tiny mouse wants to help", "Paper-cut scene: Grandpa, Grandma, Granddaughter, the dog and the cat sit on the ground in a tired row beside the enormous turnip, puffing, while a tiny grey mouse stands on the earth in front of them, waving one paw high and squeaking that it wants to help.", SUMMER, [
    *garden(), turnip(*BIG),
    figure("cat", 105, GROUND + 14, 1.1, pose="sit", eyes="sad", mouth="puff", look=(3, 2)),
    figure("dog", 180, GROUND + 10, 1.05, pose="sit", eyes="sad", mouth="puff", look=(3, 2)),
    figure("girl", 255, GROUND + 6, 1, pose="sit", eyes="sad", mouth="puff", look=(3, 2)),
    figure("ma", 340, GROUND + 4, 1, pose="sit", eyes="sad", mouth="puff", look=(3, 2)),
    figure("pa", 430, GROUND, 1, pose="sit", eyes="sad", mouth="puff", look=(3, 2)),
    marks(["M480 360 q12 -6 22 2", "M392 368 q12 -6 22 2", "M300 388 q12 -6 22 2"], "#fff", 3.5),
    figure("mouse", 500, 588, MOUSE_S, hl=((12, -34), (-8, -10)), mouth="open", look=(-2, -2)),
    marks(["M488 530 l-8 -10", "M502 524 v-12", "M516 530 l8 -10"], INK, 3)])

# 11 everyone pulls — heave-ho!
svg(11, "Heave-ho!", "Paper-cut scene: all six helpers pull together in a long line — the tiny mouse holds the cat, the cat holds the dog, the dog holds Granddaughter, Granddaughter holds Grandma, Grandma holds Grandpa, and Grandpa holds the enormous turnip's leaves — and the turnip starts to wobble, with crumbs of earth flying.", HOT, [
    *pull_page(6),
    crumbs([(CX - 150, GROUND - 30, 6), (CX - 120, GROUND - 56, 4), (CX + 150, GROUND - 46, 5), (CX + 170, GROUND - 18, 6), (CX + 128, GROUND - 74, 4)]),
    marks([f"M{CX - 120} {CY - 170} q-16 8 -14 24", f"M{CX + 100} {CY - 180} q16 8 14 24", f"M{CX - 140} {CY - 120} q-14 8 -12 22"], INK, 3.5)])

# 12 POP! — a soft, giggly heap
svg(12, "Pop! Out comes the turnip", "Paper-cut scene: POP! The enormous turnip has come out of the ground and lies on its side with its long root showing, leaving a hole in the earth; the whole family has tumbled onto their bottoms in a soft, laughing heap with their arms in the air, and the tiny mouse sits on top of the turnip, waving.", HOT, [
    sun(720, 80, 40, face=True), cloud(220, 80, 1), *back(trees=((60, 400, 1.1),)), fence(250, 800, 452), field(),
    f'<ellipse cx="700" cy="{GROUND + 14}" rx="70" ry="16" fill="{SOIL_D}"/>',
    crumbs([(660, 470, 6), (700, 452, 5), (740, 470, 6), (760, 444, 4), (640, 446, 4)]),
    turnip(600, 440, 100, rot=-80, buried=False),
    figure("mouse", 606, 344, MOUSE_S, pose="sit", hl=((10, -30), (-8, -14)), eyes="happy", mouth="open"),
    figure("cat", 120, GROUND + 22, 1.1, rot=-24, pose="sit", eyes="happy", mouth="open", hl=((16, -88), (-12, -84))),
    figure("dog", 185, GROUND + 18, 1.05, rot=-22, pose="sit", eyes="happy", mouth="open", hl=((20, -106), (-14, -102))),
    figure("girl", 255, GROUND + 14, 1, rot=-20, pose="sit", eyes="happy", mouth="open", hl=((28, -132), (-18, -128))),
    figure("ma", 335, GROUND + 10, 1, rot=-18, pose="sit", eyes="happy", mouth="open", hl=((32, -152), (-22, -148))),
    figure("pa", 420, GROUND + 6, 1, rot=-16, pose="sit", eyes="happy", mouth="open", hl=((36, -156), (-24, -150))),
    star(500, 300, 1.6), star(460, 240, 1.1), star(380, 250, 1.3), spark(520, 380, 1.4), spark(250, 300, 1.2),
    marks(["M490 330 l20 -16", "M500 360 h26", "M690 320 l14 -20", "M730 350 l20 -10"], INK, 3.5)])

# 13 turnip soup for everyone
TABLE_Y = 448
bowls = "".join(f'<g transform="translate({a} {TABLE_Y})"><path d="M{-w} 0 H{w} Q{n(w * .8)} {n(w * .9)} 0 {n(w * .9)} Q{n(-w * .8)} {n(w * .9)} {-w} 0Z" fill="#E9E1D0"/>'
                f'<ellipse rx="{w}" ry="{n(w * .25)}" fill="#F3D27A"/>' + stroke(f"M{n(w * .4)} -2 l{n(w * .6)} {n(-w * 1.2)}", WOOD_D, 3) + '</g>'
                for a, w in [(138, 16), (222, 16), (318, 16), (404, 18), (672, 18)])
svg(13, "Turnip soup for everyone", "Paper-cut evening scene: as the sun sets behind the hill, at a long wooden table outside the cottage, Grandpa, Grandma, Granddaughter, the dog and the cat smile over bowls of warm turnip soup, with a big steaming pot in the middle, and the tiny mouse sits on the table with its own little bowl.", DUSK, [
    sun(250, 336, 40), cloud(560, 100, 1, "#FFE1D2"), hill(350, 34, "#B9DDA0", False), izba(700, 392, 1), birch(60, 400, 1.1), hill(415, 18, "#8FCF7A"),
    f'<path d="M0 {GROUND - 20} Q400 {GROUND - 36} 800 {GROUND - 18} V600 H0Z" fill="{LEAF_L}" filter="url(#p)"/>',
    figure("cat", 120, 462, 1.15, hl=((22, -12), (-4, -10)), eyes="happy"),
    figure("dog", 205, 478, 1.1, hl=((20, -30), (-4, -26)), eyes="happy", mouth="open"),
    figure("girl", 300, 500, 1, hl=((30, -60), (-6, -56)), eyes="happy"),
    figure("ma", 385, 520, 1, hl=((32, -78), (-4, -74)), eyes="happy"),
    figure("pa", 655, 520, 1, hl=((28, -76), (-4, -72)), eyes="happy", mouth="open"),
    f'<g filter="url(#p)"><rect x="40" y="{TABLE_Y}" width="740" height="18" rx="6" fill="#C38A57"/><rect x="60" y="{TABLE_Y + 18}" width="700" height="10" fill="#8E5F38"/>'
    f'<rect x="80" y="{TABLE_Y + 18}" width="18" height="110" fill="#A86B3E"/><rect x="720" y="{TABLE_Y + 18}" width="18" height="110" fill="#A86B3E"/></g>',
    bowls,
    f'<g filter="url(#p)" transform="translate(540 {TABLE_Y})"><path d="M-54 0 L-48 -58 H48 L54 0Z" fill="#3A3A44"/><rect x="-58" y="-66" width="116" height="12" rx="6" fill="#4A4A56"/>'
    f'<ellipse cy="-62" rx="50" ry="9" fill="#F3D27A"/><circle cx="-18" cy="-63" r="7" fill="{T_BULB}"/><circle cx="12" cy="-62" r="6" fill="{T_TOP}"/><circle cx="30" cy="-64" r="5" fill="{T_BULB}"/></g>',
    marks(["M510 360 q-12 -16 0 -32 q12 -16 0 -32", "M540 352 q-12 -16 0 -32 q12 -16 0 -32", "M570 360 q-12 -16 0 -32 q12 -16 0 -32"], "#fff", 5),
    figure("mouse", 470, TABLE_Y, MOUSE_S, pose="sit", hl=((20, -10), (-6, -8)), eyes="happy"),
    f'<g transform="translate(490 {TABLE_Y - 1})"><path d="M-6 0 H6 Q5 6 0 6 Q-5 6 -6 0Z" fill="#E9E1D0"/><ellipse rx="6" ry="1.8" fill="#F3D27A"/></g>'])
