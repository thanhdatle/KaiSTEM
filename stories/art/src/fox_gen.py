#!/usr/bin/env python3
"""Generates the 13 Fox-and-the-Sky-Feast flip-book SVGs from shared character parts.

Usage: python3 fox_gen.py <output-dir>
Scale rule: every character is drawn at its base size (FOX_S, CONDOR_S, PARROT_S) on every page,
so the condor is always much bigger than the fox (he can carry him) and the parrots are always
small (about half the fox's length). The mountains stay huge, and far below in the flying pages.
Fox = an Andean fox (culpeo): rufous head and legs, grizzled grey back, white chin,
tall pointed ears, a narrow snout and a long bushy grey tail with a black tip, held low.
"""
import math
import sys

OUT = sys.argv[1]
INK = "#2B2320"
FOX_S, CONDOR_S, PARROT_S = .9, 1.1, 1.0
RUFUS, RUFUS_D, FOX_GREY, FOX_WHITE = "#C9783A", "#A55A27", "#A79E92", "#F6EFE3"
COND, COND_D, COND_SKIN, COND_SKIN_D, BEAK = "#2C2828", "#171515", "#C98E7E", "#8E5A50", "#EDE2C6"
PAR, PAR_D, PAR_Y, PAR_BEAK = "#56B847", "#2F8A3A", "#F2D24A", "#F0C987"
MTN, MTN_D, SNOW = "#9B93C2", "#7C73A6", "#F7FAFF"
HILL, HILL_D, PUNA, PUNA_D, ICHU = "#B98F5E", "#94704A", "#C8B25C", "#A48F3E", "#E3CE7A"
GRASS, GRASS_D = "#7CBF5A", "#5A9A44"
ROPE, ROPE_D = "#D9B865", "#A8873C"
CLOUD, CLOUD_D = "#FFFFFF", "#DCE7F4"
CLAY, CLAY_D = "#B5603A", "#8A4228"
QUINOA = ("#E8A23A", "#D2502F", "#F2D04A", "#B8324A")
POTATO, POTATO_P = "#B98A56", "#8D5A8F"
CORN, CORN_D = "#F2C232", "#D99A1E"
AGUAYO = ("#D8336A", "#F28C28", "#2E9C6A", "#6B3FA0", "#F2C232")
DAY = [(0, "#6FC0E8"), (1, "#E8F6FB")]
HIGH = [(0, "#6E98DA"), (.7, "#CFE0F6"), (1, "#F6EAF4")]
GOLDEN = [(0, "#86C6E8"), (.6, "#FDE6C0"), (1, "#FBD49A")]


def stroke(d: str, col: str = INK, w: float = 5, op: float = 1) -> str:
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{o}/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- the fox (culpeo)
def fox_head(mood: str) -> str:
    """Head facing right, centred on the skull. Tall ears, narrow snout, white chin."""
    out = (f'<path d="M-14 -8 L-12 -50 L4 -14Z" fill="{RUFUS_D}"/><path d="M-10 -14 L-10 -40 L0 -16Z" fill="#5A3020"/>'
           f'<path d="M-2 -12 L8 -52 L18 -10Z" fill="{RUFUS}"/><path d="M2 -14 L8 -42 L14 -14Z" fill="#5A3020"/>')
    out += f'<ellipse rx="22" ry="17" fill="{RUFUS}"/>'
    out += f'<path d="M8 -8 Q30 -6 48 2 Q52 8 46 11 Q28 14 8 12Z" fill="{RUFUS}"/>'
    out += f'<path d="M-6 6 Q20 22 44 11 Q28 24 4 20Z" fill="{FOX_WHITE}"/><path d="M-16 4 Q-4 14 6 8 Q-2 20 -14 14Z" fill="{FOX_WHITE}"/>'
    out += f'<ellipse cx="47" cy="5" rx="4.5" ry="4" fill="{INK}"/>'
    out += '<circle cx="-6" cy="8" r="4.5" fill="#F0705F" opacity=".35"/>'
    if mood == "dazed":
        out += stroke("M8 -4 m-5 0 a5 5 0 1 1 5 5 a3 3 0 1 1 -3 -3", INK, 2)
    elif mood == "sad":
        out += f'<circle cx="12" cy="-3" r="4.6" fill="#fff"/><circle cx="13" cy="-2" r="2.6" fill="{INK}"/>' + stroke("M4 -12 L18 -9", INK, 2.6)
    elif mood == "proud":
        out += stroke("M7 -4 q5 -5 10 0", INK, 2.6)
    else:
        out += f'<circle cx="12" cy="-4" r="4.8" fill="#fff"/><circle cx="13.5" cy="-4" r="2.7" fill="{INK}"/>'
    if mood in ("rude", "proud"):  # mouth wide open, shouting / boasting
        out += '<path d="M22 9 Q36 10 44 10 Q36 22 24 18Z" fill="#6A2A22"/><path d="M26 15 q6 6 12 1" fill="#E77A7A"/>'
    elif mood == "oh":
        out += '<ellipse cx="34" cy="13" rx="4" ry="4.5" fill="#6A2A22"/>' + stroke("M4 -13 q7 -5 14 -1", INK, 2.4)
    elif mood == "sad":
        out += stroke("M26 14 q7 -4 14 0", INK, 2.2)
    elif mood == "eat":  # full cheeks
        out += f'<circle cx="16" cy="9" r="9" fill="{RUFUS}"/>' + stroke("M28 12 q6 3 12 0", INK, 2.2)
    else:
        out += stroke("M26 11 q8 6 16 0", INK, 2.2)
    return out


def tail(d: str, tip: str) -> str:
    return f'<path d="{d}" fill="{FOX_GREY}"/><path d="{tip}" fill="{INK}"/>'


def fox(x: float, y: float, pose: str = "stand", mood: str = "smile", flip: bool = False, k: float = 1,
        shadow: bool = True, seeds: bool = False) -> str:
    """The fox, facing right. (x, y) is his paws. pose: stand / ride / sit / up (on hind legs) / hang."""
    out = ""
    if pose in ("stand", "ride"):
        out += tail("M-44 -72 Q-92 -84 -120 -48 Q-134 -22 -116 -10 Q-104 -18 -96 -32 Q-80 -54 -44 -56Z",
                    "M-122 -40 Q-134 -22 -116 -10 Q-106 -16 -102 -26 Q-112 -30 -122 -40Z")
        legs = ("M-34 -52 L-40 -34 M-22 -52 L-16 -34 M28 -52 L22 -34 M40 -52 L46 -36" if pose == "ride"
                else "M-34 -52 L-38 -2 M-22 -52 L-20 -2 M28 -52 L26 -2 M40 -52 L42 -2")
        out += stroke(legs, RUFUS_D, 9)
        out += f'<ellipse cx="-2" cy="-66" rx="50" ry="22" fill="{RUFUS}"/>'
        out += f'<path d="M-50 -70 Q-10 -98 36 -78 Q0 -82 -50 -64Z" fill="{FOX_GREY}"/>'
        out += f'<path d="M-36 -52 Q0 -42 30 -52 Q0 -48 -36 -52Z" fill="{FOX_WHITE}" opacity=".8"/>'
        out += f'<path d="M22 -80 Q40 -100 58 -112 L72 -92 Q56 -70 40 -56Z" fill="{RUFUS}"/>'
        out += f'<path d="M40 -60 Q54 -74 64 -86 L70 -78 Q58 -62 46 -54Z" fill="{FOX_WHITE}"/>'
        out += f'<g transform="translate(62 -108)">{fox_head(mood)}</g>'
    elif pose == "sit":
        out += tail("M-30 -14 Q-84 -14 -98 -56 Q-104 -84 -84 -92 Q-76 -60 -40 -40Z",
                    "M-98 -56 Q-104 -84 -84 -92 Q-80 -80 -82 -66 Q-90 -60 -98 -56Z")
        out += f'<ellipse cx="-14" cy="-40" rx="32" ry="38" fill="{RUFUS}" transform="rotate(-20 -14 -40)"/>'
        out += f'<path d="M-40 -66 Q-20 -96 10 -94 Q-10 -84 -30 -50Z" fill="{FOX_GREY}"/>'
        out += f'<ellipse cx="-24" cy="-22" rx="24" ry="20" fill="{RUFUS_D}"/>'
        out += stroke("M-6 -2 h16", RUFUS_D, 9)
        out += stroke("M14 -56 L18 -2 M26 -56 L30 -2", RUFUS_D, 9)
        out += f'<path d="M0 -70 Q18 -92 30 -104 L46 -90 Q34 -62 22 -48Z" fill="{RUFUS}"/>'
        out += f'<path d="M14 -60 Q26 -76 34 -88 L40 -80 Q32 -60 24 -48Z" fill="{FOX_WHITE}"/>'
        out += f'<g transform="translate(38 -104)">{fox_head(mood)}</g>'
    else:  # up / hang: upright on hind legs, front paws raised
        hang = pose == "hang"
        if hang:
            out += tail("M-12 -44 Q-40 -20 -38 22 Q-30 34 -20 26 Q-26 -2 -2 -26Z",
                        "M-38 22 Q-30 34 -20 26 Q-22 18 -24 12 Q-34 12 -38 22Z")
        else:
            out += tail("M-12 -44 Q-56 -30 -66 2 Q-62 16 -48 12 Q-42 -6 -8 -24Z",
                        "M-66 2 Q-62 16 -48 12 Q-48 2 -50 -4 Q-60 -4 -66 2Z")
        out += stroke("M-6 -40 L-14 -8 M8 -40 L6 -4" if hang else "M-6 -40 L-12 -2 M8 -40 L12 -2", RUFUS_D, 10)
        out += f'<ellipse cx="0" cy="-74" rx="22" ry="44" fill="{RUFUS}" transform="rotate(8 0 -74)"/>'
        out += f'<path d="M-20 -60 Q-26 -96 -6 -116 Q-12 -86 -10 -48Z" fill="{FOX_GREY}"/>'
        out += f'<path d="M8 -112 Q22 -80 12 -44 Q4 -80 2 -110Z" fill="{FOX_WHITE}"/>'
        if hang:
            arms = "M8 -104 Q30 -122 36 -150 M14 -100 Q42 -112 44 -142"
        elif mood == "proud":
            arms = "M10 -102 Q36 -104 40 -128 M8 -94 Q-6 -78 6 -66"
        else:
            arms = "M10 -100 Q32 -96 40 -110 M10 -92 Q34 -84 44 -96"
        out += stroke(arms, RUFUS_D, 9)
        out += f'<g transform="translate(10 -134)">{fox_head(mood)}</g>'
    if seeds:  # quinoa seeds tucked in his fur "for later"
        pts = [(-30, -76), (-10, -80), (8, -74), (-20, -66), (20, -84)] if pose in ("stand", "ride") else [(-6, -60), (4, -80), (-10, -40)]
        out += "".join(f'<circle cx="{a}" cy="{b}" r="3" fill="{QUINOA[i % 4]}"/>' for i, (a, b) in enumerate(pts))
    return group(x, y, FOX_S * k, flip, out, shadow)


# ---------------------------------------------------------------- the condor
def condor_head(mood: str) -> str:
    out = f'<ellipse rx="19" ry="15" fill="{COND_SKIN}"/>'
    out += f'<path d="M-12 -12 Q-8 -24 0 -18 Q4 -28 10 -18 Q16 -24 18 -10 Q4 -6 -12 -12Z" fill="{COND_SKIN_D}"/>'
    out += f'<path d="M12 -6 Q34 -8 36 8 Q34 16 28 14 Q28 6 14 6Z" fill="{BEAK}"/><path d="M30 6 Q36 10 33 15 Q28 13 28 8Z" fill="#5C4C40"/>'
    out += f'<circle cx="4" cy="-3" r="5" fill="#fff"/><circle cx="5.5" cy="-3" r="2.8" fill="{INK}"/>'
    if mood == "frown":
        out += stroke("M-4 -11 L12 -6", INK, 3)
    out += stroke("M14 10 q6 3 12 0", "#6E4A40", 2)
    return out


def condor_fly(x: float, y: float, k: float = 1, flip: bool = False, rider: str = "", shadow: bool = True) -> str:
    """The great condor flying, facing right, wings raised high. (x, y) is the middle of his body.
    `rider` (in condor-local units) is drawn on his back, between the far wing and the near wing."""
    def fingers(sx: int) -> str:
        return (f" L{sx * 196} -140 L{sx * 222} -132 L{sx * 202} -120 L{sx * 226} -106 L{sx * 204} -98"
                f" L{sx * 222} -82 L{sx * 196} -78")
    far = (f'<path d="M-30 -12 Q-70 -120 -180 -150{fingers(-1)} Q-110 -50 -50 8Z" fill="{COND_D}"/>'
           '<path d="M-44 -30 Q-80 -104 -160 -128 Q-100 -80 -56 -14Z" fill="#E9E6E0" opacity=".85"/>')
    near = (f'<path d="M30 -10 Q60 -120 180 -150{fingers(1)} Q110 -50 44 16Z" fill="{COND}"/>'
            '<path d="M40 -26 Q70 -104 156 -130 Q96 -76 52 -8Z" fill="#F4F1EA"/>')
    body = (f'<path d="M-66 -6 L-128 8 L-124 22 L-62 18Z" fill="{COND_D}"/>'
            f'<ellipse cx="-2" cy="2" rx="76" ry="28" fill="{COND}"/>'
            + stroke("M-50 24 l-4 10 M-38 26 l-2 10", "#7E7068", 4)
            + '<ellipse cx="70" cy="-6" rx="22" ry="20" fill="#FAF7F0"/>'
            f'<path d="M80 -14 Q92 -30 104 -32 L110 -18 Q96 -10 88 2Z" fill="{COND_SKIN}"/>'
            f'<g transform="translate(108 -32)">{condor_head("smile")}</g>')
    return group(x, y, CONDOR_S * k, flip, far + body + rider + near, shadow)


def condor_perch(x: float, y: float, flip: bool = False, mood: str = "smile") -> str:
    """The condor standing, side view facing right. (x, y) is his feet."""
    out = f'<path d="M-30 -44 L-74 4 L-54 10 L-14 -30Z" fill="{COND_D}"/>'
    out += stroke("M-6 -34 L-8 -2 M14 -34 L16 -2", "#7E7068", 7) + stroke("M-18 -1 h16 M4 -1 h18", "#7E7068", 5)
    out += f'<ellipse cx="0" cy="-92" rx="46" ry="66" fill="{COND}" transform="rotate(14 0 -92)"/>'
    out += f'<path d="M-36 -126 Q6 -150 40 -118 Q34 -48 -42 -16 Q-58 -80 -36 -126Z" fill="{COND_D}"/>'
    out += '<path d="M-30 -118 Q6 -138 34 -112 Q16 -92 -32 -86Z" fill="#F1EEE7"/>'
    out += '<ellipse cx="22" cy="-150" rx="32" ry="18" fill="#FAF7F0"/>'
    out += f'<path d="M14 -158 Q18 -186 40 -194 L56 -182 Q40 -172 36 -156Z" fill="{COND_SKIN}"/>'
    out += f'<g transform="translate(50 -194)">{condor_head(mood)}</g>'
    return group(x, y, CONDOR_S, flip, out)


# ---------------------------------------------------------------- the parrots
def parrot(x: float, y: float, flip: bool = False, mood: str = "smile", wing: str = "up") -> str:
    """A small green mountain parrot flying, facing right. (x, y) is its body."""
    out = f'<path d="M-16 2 L-54 18 L-50 10 L-16 -4Z" fill="{PAR_D}"/>'
    out += f'<ellipse rx="22" ry="12" fill="{PAR}"/><ellipse cx="2" cy="5" rx="14" ry="6" fill="{PAR_Y}" opacity=".8"/>'
    wing_d = "M-4 -6 Q-8 -42 -30 -48 Q-20 -22 -16 -2Z" if wing == "up" else "M-4 -2 Q-12 22 -32 28 Q-20 8 -16 0Z"
    out += f'<path d="{wing_d}" fill="{PAR_D}"/>'
    out += f'<circle cx="20" cy="-8" r="11" fill="{PAR}"/><path d="M14 -18 Q22 -22 28 -14 Q20 -14 14 -18Z" fill="{PAR_Y}"/>'
    out += f'<path d="M28 -10 Q40 -10 38 2 Q34 -2 28 -2Z" fill="{PAR_BEAK}"/>'
    out += f'<circle cx="22" cy="-10" r="3.4" fill="#fff"/><circle cx="23" cy="-10" r="2" fill="{INK}"/>'
    if mood == "cross":
        out += stroke("M16 -16 L27 -13", INK, 2.2)
    return group(x, y, PARROT_S, flip, out)


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
            t = 40
            lxx = px + (lx - px) * t * .35 / (ly - py) if ly != py else px - 20
            rxx = px + (rx - px) * t * .35 / (ry - py) if ry != py else px + 20
            yy = py + t * .35
            out += (f'<path d="M{lxx:.0f} {yy:.0f} L{px} {py} L{rxx:.0f} {yy:.0f} L{(px + rxx) / 2:.0f} {py + t * .55:.0f} '
                    f'L{px} {py + t * .3:.0f} L{(px + lxx) / 2:.0f} {py + t * .55:.0f}Z" fill="{SNOW}"/>')
    return out


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def tufts(pts: list, col: str = PUNA_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 7} {b} l3 -12 M{a} {b} l0 -15 M{a + 7} {b} l-3 -12" for a, b in pts), col, w)


def ichu(x: float, y: float, s: float = 1) -> str:
    """A soft, round tussock of ichu grass."""
    blades = " ".join(f"M0 0 q{dx * .4:.0f} -24 {dx} -{h}" for dx, h in [(-30, 26), (-20, 38), (-8, 44), (6, 46), (18, 40), (30, 28)])
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cy="-6" rx="30" ry="12" fill="{PUNA}"/>'
            f'{stroke(blades, ICHU, 4)}{stroke(blades, PUNA_D, 1.2)}</g>')


def far_andes(base: float = 380) -> list:
    return [peak_range([(60, base - 150), (170, base - 90), (290, base - 220), (420, base - 120), (540, base - 200), (650, base - 110), (760, base - 170)], 640, MTN),
            peak_range([(0, base - 40), (120, base - 100), (260, base - 30), (380, base - 70), (520, base - 10), (640, base - 80), (800, base - 30)], 640, MTN_D, False)]


def low_andes(top: float = 430) -> list:
    """The mountains seen far, far below from the sky: snowy peaks whose feet run off the bottom edge."""
    return [peak_range([(40, top + 40), (150, top), (270, top + 60), (390, top + 10), (520, top + 70), (640, top + 6), (770, top + 50)], 640, MTN),
            peak_range([(0, top + 110), (110, top + 80), (240, top + 120), (360, top + 90), (500, top + 130), (620, top + 96), (800, top + 120)], 640, HILL, False)]


def puna(top: float = 440) -> str:
    return (f'<path filter="url(#p)" d="M0 {top} Q200 {top - 30} 420 {top - 6} T800 {top - 12} V600 H0Z" fill="{PUNA}"/>'
            + tufts([(60, top + 40), (210, top + 30), (420, top + 50), (620, top + 36), (740, top + 60), (120, top + 120), (330, top + 130), (560, top + 120)]))


def rock(x: float, y: float, w: float = 140, h: float = 70) -> str:
    return (f'<path filter="url(#p)" d="M{x - w / 2} {y} Q{x - w / 2 + 10} {y - h} {x} {y - h - 6} Q{x + w / 2 - 6} {y - h + 4} {x + w / 2} {y}Z" fill="#9A8E84"/>'
            f'<path d="M{x - w / 4} {y - h * .7} q{w * .2} -{h * .2} {w * .4} 0" stroke="#B9AFA6" stroke-width="4" fill="none"/>')


def sky_floor(top: float = 450) -> str:
    """The big fluffy cloud the feast sits on."""
    bumps = "".join(f'<circle cx="{a}" cy="{top + 10 + (i % 2) * 12}" r="{46 + (i % 3) * 8}"/>' for i, a in enumerate(range(-20, 860, 70)))
    return (f'<g filter="url(#p)" fill="{CLOUD}">{bumps}<rect x="0" y="{top + 20}" width="800" height="{600 - top}"/></g>'
            f'<path d="M0 {top + 90} Q200 {top + 70} 400 {top + 90} T800 {top + 86} V600 H0Z" fill="{CLOUD_D}" opacity=".6"/>')


def aguayo(x: float, y: float, w: float, h: float = 40) -> str:
    """A striped Andean weaving laid flat on the cloud like a tablecloth (a trapezoid in perspective)."""
    inset = h * .7

    def band(t0: float, t1: float, col: str) -> str:
        xa0, xa1 = x + inset * (1 - t0), x + w - inset * (1 - t0)
        xb0, xb1 = x + inset * (1 - t1), x + w - inset * (1 - t1)
        return f'<path d="M{xa0:.1f} {y + h * t0:.1f} H{xa1:.1f} L{xb1:.1f} {y + h * t1:.1f} H{xb0:.1f}Z" fill="{col}"/>'
    out = '<g filter="url(#p)">' + band(0, 1, AGUAYO[0])
    for i in range(1, 7):
        out += band(i / 7, i / 7 + .6 / 7, AGUAYO[i % 5])
    mid = y + h * .5
    out += "".join(f'<path d="M{a} {mid} l7 -5 l7 5 l-7 5Z" fill="#fff" opacity=".8"/>' for a in range(int(x + inset), int(x + w - inset), 40))
    return out + '</g>'


def bowl(x: float, y: float, food: str, full: bool = True) -> str:
    """A clay bowl on the cloth: quinoa, potatoes or corn."""
    out = f'<g transform="translate({x} {y}) scale(1.35)" filter="url(#p)">'
    if full:
        if food == "quinoa":
            out += f'<ellipse cy="-20" rx="30" ry="16" fill="{QUINOA[0]}"/>' + "".join(
                f'<circle cx="{a}" cy="{b}" r="2.6" fill="{QUINOA[(i + 1) % 4]}"/>'
                for i, (a, b) in enumerate([(-18, -22), (-8, -30), (4, -24), (14, -32), (20, -20), (-2, -16), (-14, -14), (10, -14)]))
        elif food == "potato":
            out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="13" ry="10" fill="{c}"/>' for a, b, c in [(-14, -18, POTATO), (12, -20, POTATO_P), (0, -30, POTATO)])
        else:
            out += "".join(f'<g transform="translate({a} -24) rotate({r})"><ellipse rx="8" ry="20" fill="{CORN}"/>{stroke("M-3 -12 v24 M3 -12 v24", CORN_D, 1.6)}</g>'
                           for a, r in [(-12, -24), (2, 0), (16, 22)])
    out += f'<path d="M-36 -12 Q-34 18 0 18 Q34 18 36 -12Z" fill="{CLAY}"/><ellipse cy="-12" rx="36" ry="6" fill="{CLAY_D}"/>'
    out += stroke("M-26 0 h52", "#E6B07A", 3)
    return out + '</g>'


def rope_line(x1: float, y1: float, x2: float, y2: float, w: float = 9) -> str:
    """A twisted grass rope."""
    n = max(2, int(math.hypot(x2 - x1, y2 - y1) // 14))
    ticks = " ".join(f"M{x1 + (x2 - x1) * i / n - 4:.0f} {y1 + (y2 - y1) * i / n - 3:.0f} l8 6" for i in range(n))
    return stroke(f"M{x1} {y1} L{x2} {y2}", ROPE_D, w + 3) + stroke(f"M{x1} {y1} L{x2} {y2}", ROPE, w) + stroke(ticks, ROPE_D, 1.8)


def coil(x: float, y: float) -> str:
    rings = "".join(f'<ellipse cx="{x}" cy="{y - i * 9}" rx="{60 - i * 6}" ry="{16 - i}" fill="none" stroke="{ROPE_D}" stroke-width="12"/>'
                    f'<ellipse cx="{x}" cy="{y - i * 9}" rx="{60 - i * 6}" ry="{16 - i}" fill="none" stroke="{ROPE}" stroke-width="8"/>' for i in range(4))
    return f'<g filter="url(#p)">{rings}</g>'


def quinoa_plant(x: float, y: float, s: float = 1, i: int = 0) -> str:
    col = QUINOA[i % 4]
    head = "".join(f'<circle cx="{a}" cy="{b}" r="7" fill="{col}"/>' for a, b in [(0, -96), (-6, -84), (6, -84), (0, -74), (-8, -66), (8, -66), (0, -110)])
    leaves = f'<path d="M0 -40 q-24 -6 -26 -22 q18 0 26 18Z M0 -54 q24 -6 26 -22 q-18 0 -26 18Z" fill="{GRASS_D}"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{stroke("M0 0 V-70", GRASS_D, 5)}{leaves}{head}</g>'


def potato_plant(x: float, y: float, s: float = 1) -> str:
    """A bushy potato plant: a stem with many small pointed leaves and one cluster of lilac flowers."""
    leaf = '<path d="M0 0 q8 -10 18 -4 q-8 10 -18 4Z" fill="{c}" transform="translate({a} {b}) rotate({r})"/>'
    leaves = "".join(leaf.format(c=GRASS if i % 2 else GRASS_D, a=a, b=b, r=r)
                     for i, (a, b, r) in enumerate([(0, -10, -150), (0, -10, -30), (0, -22, -160), (0, -22, -20),
                                                    (0, -34, -140), (0, -34, -40), (0, -44, -100), (-2, -4, 180), (2, -4, 0)]))
    star = "M0 -6 L2 -2 L6 -2 L3 1 L4 5 L0 3 L-4 5 L-3 1 L-6 -2 L-2 -2Z"
    fl = "".join(f'<path d="{star}" transform="translate({a} {b})" fill="#C9A6E4"/>' for a, b in [(10, -50), (16, -44), (6, -42)])
    return f'<g transform="translate({x} {y}) scale({s})">{stroke("M0 0 V-46", GRASS_D, 3)}{leaves}{fl}</g>'


def terrace(y: float, x0: float, x1: float, h: float = 26) -> str:
    return (f'<path filter="url(#p)" d="M{x0} {y} H{x1} L{x1 + 10} {y + h} H{x0 - 10}Z" fill="{HILL}"/>'
            + stroke(" ".join(f"M{a} {y + h * .5} h18" for a in range(int(x0) + 10, int(x1) - 10, 44)), HILL_D, 2.4))


def motion(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def stars(x: float, y: float) -> str:
    one = 'M0 -9 L2.6 -2.6 L9 0 L2.6 2.6 L0 9 L-2.6 2.6 L-9 0 L-2.6 -2.6Z'
    return "".join(f'<path d="{one}" transform="translate({x + a} {y + b})" fill="#F7D046" stroke="{INK}" stroke-width="1.2"/>' for a, b in [(-34, 4), (0, -12), (34, 2)])


def seed_spray(x: float, y: float) -> str:
    pts = [(-120, -40), (-90, -90), (-60, -120), (-20, -140), (30, -136), (70, -116), (110, -84), (140, -40),
           (-150, 0), (160, 4), (-80, -60), (90, -56), (-40, -100), (50, -96), (0, -110)]
    out = "".join(f'<circle cx="{x + a}" cy="{y + b}" r="4.4" fill="{QUINOA[i % 4]}"/>' for i, (a, b) in enumerate(pts))
    out += "".join(f'<ellipse cx="{x + a}" cy="{y + b}" rx="9" ry="7" fill="{c}"/>' for a, b, c in [(-106, -64, POTATO), (124, -66, POTATO_P), (-30, -160, POTATO_P)])
    return f'<g filter="url(#p)">{out}</g>'


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/fox-{n:02d}.svg", "w") as fh:
        fh.write(doc)


# The rider sits inside the condor's group, so it inherits CONDOR_S; divide it out to keep the fox at FOX_S.
RIDER = fox(-24, 6, "ride", "smile", shadow=False, k=1 / CONDOR_S)
FEAST_FULL = [aguayo(170, 456, 480, 70), bowl(260, 506, "quinoa"), bowl(400, 506, "potato"), bowl(540, 506, "corn")]

# 01 cover: the condor flies over the Andes with the fox on his back
svg(1, "The Fox and the Sky Feast", "Paper-cut cover: high above the snowy Andes mountains, the great black condor with his white collar and white wing patches flies with his wings raised, and a red-brown Andean fox with tall pointed ears and a bushy black-tipped tail rides on his back, smiling. White clouds float around them.", DAY, [
    cloud(130, 110, 1), cloud(690, 90, .9), cloud(640, 330, .8, .8),
    *low_andes(400),
    condor_fly(390, 290, rider=RIDER)])

# 02 the hungry fox at the foot of the mountains; the condor soars above
svg(2, "Atoq the fox", "Paper-cut scene: on the golden grassland at the foot of huge snowy mountains stands a red-brown Andean fox with tall pointed ears, a white chin, a grey back and a long bushy grey tail with a black tip. High in the sky above, the great black condor soars with his wings spread.", DAY, [
    cloud(120, 90, 1), *far_andes(390), puna(450), ichu(620, 520, 1.2), ichu(90, 540),
    condor_fly(470, 215),
    fox(300, 540, "stand", "smile")])

# 03 the condor lands; the fox begs to come along
svg(3, "Take me too!", "Paper-cut scene: the big black condor stands on a grey rock on the right, looking down at the fox. The fox, much smaller, stands up on his hind legs on the golden grass with his front paws together, begging to come to the sky feast.", DAY, [
    cloud(160, 90, 1), cloud(560, 70, .8), *far_andes(390), puna(450), ichu(110, 540),
    rock(580, 470, 200, 70), condor_perch(570, 410, flip=True),
    fox(300, 530, "up", "smile")])

# 04 up, up, up they fly
svg(4, "Up, up, up!", "Paper-cut scene: the condor flies up past the snowy mountain tops with the fox riding on his back. The mountains are far below, and white clouds drift past.", HIGH, [
    cloud(100, 100, .9), cloud(700, 140, 1), cloud(160, 380, .9, .8),
    *low_andes(470),
    condor_fly(420, 270, rider=RIDER),
    motion(["M120 240 h60", "M100 270 h50", "M130 300 h40"])])

# 05 the feast on the clouds; the fox gobbles
svg(5, "The sky feast", "Paper-cut scene: on top of the clouds a striped Andean cloth is spread with three clay bowls, of quinoa, potatoes and corn. The fox gobbles from the quinoa bowl with his cheeks stuffed full and seeds stuck in his fur, while the condor stands on the other side of the cloth.", HIGH, [
    cloud(150, 90, .8), cloud(640, 110, .9), sky_floor(420), *FEAST_FULL,
    condor_perch(705, 520, flip=True),
    fox(150, 540, "stand", "eat", seeds=True),
    motion(["M232 420 l-6 -12", "M250 414 v-14", "M268 420 l6 -12"], QUINOA[1], 3)])

# 06 the fox boasts; the condor frowns
svg(6, "I'm the best!", "Paper-cut scene: on the cloud, the fox stands up on his hind legs, one paw in the air, boasting with his mouth wide open and seeds in his fur. The big condor stands on the other side of the striped cloth and frowns. Two of the bowls are already empty.", HIGH, [
    cloud(150, 90, .8), cloud(640, 110, .9), sky_floor(420), aguayo(170, 456, 480, 70),
    bowl(260, 506, "quinoa", False), bowl(400, 506, "potato", False), bowl(540, 506, "corn"),
    condor_perch(705, 520, flip=True, mood="frown"),
    fox(100, 545, "up", "proud", seeds=True)])

# 07 the condor flies home; the fox is left alone
svg(7, "Oh no!", "Paper-cut scene: the condor flies away to the right, high in the sky, with whoosh lines behind him. On the cloud below, the fox sits all alone beside the striped cloth and the empty clay bowls, looking sad.", HIGH, [
    cloud(140, 100, .8), sky_floor(420), aguayo(170, 456, 480, 70),
    bowl(260, 506, "quinoa", False), bowl(400, 506, "potato", False), bowl(540, 506, "corn", False),
    condor_fly(530, 215),
    motion(["M200 150 h70", "M180 190 h60", "M210 230 h50"]),
    fox(100, 545, "sit", "sad", seeds=True)])

# 08 the fox weaves a grass rope and starts down
svg(8, "A long, long rope", "Paper-cut scene: on the cloud, tufts of golden sky grass grow. The fox holds a twisted grass rope beside a big coil of more rope; the rope runs to the edge of the cloud and drops down over the side.", HIGH, [
    cloud(150, 90, .8), cloud(660, 80, .7), sky_floor(420),
    ichu(80, 520, 1), ichu(200, 560, .9), ichu(700, 540, .9),
    coil(470, 520), rope_line(470, 500, 690, 470), rope_line(690, 470, 770, 600),
    fox(300, 545, "up", "smile", seeds=True), rope_line(330, 452, 420, 512, 7)])

# 09 down the rope; the parrots fly by
svg(9, "Down, down, down!", "Paper-cut scene: the fox hangs on a long grass rope that comes down from the clouds at the top, high above the snowy mountains. Three small green parrots fly past, and the fox shouts rude names at them with his mouth wide open.", HIGH, [
    cloud(400, 30, 1.6), *low_andes(480), cloud(120, 420, .8, .8),
    rope_line(420, 0, 420, 470),
    fox(395, 430, "hang", "rude", seeds=True),
    parrot(610, 170), parrot(660, 270, wing="down"), parrot(190, 210, flip=True)])

# 10 the parrots peck the rope: SNAP!
svg(10, "Peck, peck, SNAP!", "Paper-cut scene: two small green parrots peck at the grass rope high up near the clouds, and the rope is fraying with snap marks. A third parrot flaps nearby. Lower down, the fox clings to the rope and looks up in surprise.", HIGH, [
    cloud(400, 30, 1.6), *low_andes(480), cloud(670, 420, .8, .8),
    rope_line(420, 0, 420, 124), rope_line(420, 160, 420, 470),
    stroke("M414 124 l-8 12 M420 124 v14 M426 124 l8 12 M414 160 l-8 -12 M420 160 v-14 M426 160 l8 -12", ROPE_D, 3.4),
    motion(["M380 130 l-20 -6", "M378 148 l-22 4", "M460 130 l20 -6", "M462 148 l22 4"], INK, 3),
    parrot(366, 160, mood="cross"), parrot(474, 160, flip=True, mood="cross"), parrot(620, 230, wing="down"),
    fox(395, 430, "hang", "oh", seeds=True)])

# 11 a soft bump on a grassy hill; the seeds scatter
svg(11, "A soft BUMP", "Paper-cut scene: the fox sits up on a soft, round grassy hill, a little dizzy, with three yellow stars circling his head, but not hurt. Quinoa seeds and little potatoes fly out all around him, and the broken end of the grass rope lies beside him. Two green parrots fly overhead.", DAY, [
    cloud(140, 90, .9), *far_andes(380),
    f'<path filter="url(#p)" d="M-20 600 Q60 420 400 420 Q740 420 820 600Z" fill="{GRASS}"/>',
    ichu(160, 520, 1.1), ichu(640, 520, 1.1), ichu(260, 470, .8), ichu(560, 470, .8),
    rope_line(520, 560, 600, 548), rope_line(600, 548, 680, 566), seed_spray(420, 440),
    fox(400, 470, "sit", "dazed"), stars(420, 330),
    parrot(170, 160), parrot(640, 150, flip=True, wing="down")])

# 12 quinoa and potatoes grow all over the mountains
svg(12, "Quinoa on the mountains", "Paper-cut scene: green terraced fields climb the mountainside, full of quinoa plants with bright orange, red and yellow seed heads, and leafy potato plants with little lilac flowers. The fox stands at the bottom, smiling at the new plants, and two green parrots fly over the snowy peaks.", DAY, [
    cloud(130, 80, .9), cloud(650, 70, .8),
    *far_andes(300),
    f'<path filter="url(#p)" d="M60 600 L150 290 Q400 260 650 290 L760 600Z" fill="{HILL_D}"/>',
    terrace(300, 140, 660), terrace(360, 100, 700), terrace(420, 60, 740), terrace(480, 20, 780),
    *[quinoa_plant(a, 302, .5, i) for i, a in enumerate(range(180, 640, 70))],
    *[potato_plant(a, 362, .7) for a in range(140, 680, 80)],
    *[quinoa_plant(a, 422, .65, i + 1) for i, a in enumerate(range(100, 720, 76))],
    *[potato_plant(a, 482, .9) for a in range(560, 780, 90)],
    f'<path filter="url(#p)" d="M0 520 Q400 500 800 520 V600 H0Z" fill="{PUNA}"/>',
    fox(250, 572, "stand", "smile"),
    parrot(300, 170), parrot(500, 140, wing="down")])

# 13 a polite fox: thank you, Condor! sorry, parrots!
svg(13, "Thank you, Condor!", "Paper-cut scene: in warm golden light, the fox sits politely on the grass, with bright quinoa plants growing nearby, smiling up at the big condor standing on a rock beside him. Two green parrots fly happily overhead, and snowy mountains rise behind.", GOLDEN, [
    cloud(150, 80, .9, .8), *far_andes(380), puna(450),
    quinoa_plant(70, 560, 1, 0), quinoa_plant(130, 590, .8, 2), quinoa_plant(740, 580, .9, 1),
    rock(560, 500, 200, 60), condor_perch(550, 445, flip=True),
    fox(300, 540, "sit", "smile"),
    parrot(260, 170), parrot(420, 130, flip=True, wing="down")])
