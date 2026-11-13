#!/usr/bin/env python3
"""Generates the 13 Starfruit Tree (Cay Khe) flip-book SVGs from shared character parts.

Usage: python3 khe_gen.py [output_dir]   (default: the folder above this script)
Writes khe-p01.svg ... khe-p13.svg and nothing else.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOLD, GOLD_D, GOLD_L, ORANGE = "#F6C445", "#E19A2A", "#F9D56B", "#E8743B"
BIRD, INK, CREAM, SKIN, HAIR = "#F2B93B", "#2B2320", "#F6E7D0", "#EDBE94", "#2B2320"
TROUSER, WOOD, BAGRED, PINK = "#5B4636", "#7A5236", "#C9553F", "#F08A7A"
TUNIC = {"little": "#6FA8DC", "big": "#B5533C", "v1": "#2A8C82", "v2": "#7A8F4A", "v3": "#D98CA6"}
DAWN = [(0, "#5B5A9E"), (.55, "#E79B8C"), (1, "#F8D2B0")]
DAY = [(0, "#9FD3D6"), (1, "#F6EBCF")]
NIGHT = [(0, "#1B1E4E"), (1, "#454A96")]


def stroke(d, col, w, extra=""):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def star(x, y, s=1, rot=0):
    return f'<use href="#s" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def fruit(x, y, s=1.3, rot=0):
    return f'<use href="#kf" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def slice_(x, y, s=1, rot=0):
    """A cut starfruit slice: a clear star with a paler heart and seeds."""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><use href="#s"/>'
            f'<polygon transform="scale(.55)" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="#FFF3C0"/>'
            '<circle r=".9" fill="#B5781A"/></g>')


def hill(y, amp, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def blobs(pts, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g fill="{fill}"{f}>' + "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{r:.0f}"/>' for a, b, r in pts) + '</g>'


def marks(ds, col="#fff", w=4):
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def trunk(tx, by, ty, w=40):
    m = (by + ty) / 2
    return (f'<path filter="url(#p)" d="M{tx - w} {by} Q{tx - w * .5:.0f} {m:.0f} {tx - w * .55:.0f} {ty} H{tx + w * .55:.0f} '
            f'Q{tx + w * .5:.0f} {m:.0f} {tx + w} {by}Z" fill="{WOOD}"/>')


def branch(x1, y1, x2, y2, w=18):
    return f'<g filter="url(#p)">{stroke(f"M{x1} {y1} Q{(x1 + x2) / 2:.0f} {min(y1, y2) - 16} {x2} {y2}", WOOD, w)}</g>'


def canopy(cx, cy, s=1):
    dark = [(-120, -30, 80), (130, -50, 92), (0, -80, 112), (205, 25, 60), (60, -145, 80)]
    mid = [(-60, -110, 50), (100, -120, 44), (-140, -20, 34)]
    sc = lambda pts: [(cx + a * s, cy + b * s, r * s) for a, b, r in pts]
    return blobs(sc(dark[:2]), "#2F7D4F") + blobs(sc(dark[2:]), "#3F9460") + blobs(sc(mid), "#58AB6E", False)


def fruits(cx, cy, s=1, pts=None):
    pts = pts or [(-150, 40), (-110, -40), (-40, -140), (60, -90), (150, 10), (210, 80), (180, -70), (30, -170), (-185, -25)]
    return "".join(fruit(round(cx + a * s), round(cy + b * s), 1.3 * s) for a, b in pts)


def cloud(x, y, s=1, fill="#FFF6E6"):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" filter="url(#p)">'
            '<circle cx="-50" cy="8" r="30"/><circle cx="-18" cy="-14" r="36"/><circle cx="24" cy="-10" r="32"/>'
            '<circle cx="56" cy="10" r="28"/><rect x="-78" y="6" width="160" height="34" rx="17"/></g>')


# ---------- the golden bird ----------
def _bird_face(hx, hy, look, sing=False):
    lx, ly = look
    beak = (f'<path d="M{hx - 24} {hy - 4} L{hx - 54} {hy + 6} L{hx - 24} {hy + 13}Z" fill="{ORANGE}"/>' if not sing else
            f'<path d="M{hx - 24} {hy - 5} L{hx - 54} {hy - 4} L{hx - 24} {hy + 4}Z M{hx - 24} {hy + 7} L{hx - 48} {hy + 16} L{hx - 23} {hy + 14}Z" fill="{ORANGE}"/>')
    return (beak + f'<circle cx="{hx - 8}" cy="{hy - 3}" r="7.5" fill="#fff"/><circle cx="{hx - 10 + lx}" cy="{hy - 1 + ly}" r="3.8" fill="{INK}"/>'
            f'<circle cx="{hx + 6}" cy="{hy + 13}" r="6.5" fill="{PINK}" opacity=".6"/>')


def bird(x, y, s=1, flip=False, look=(0, 0), sing=False):
    """Perched, facing left (flip=True faces right)."""
    sx = -s if flip else s
    return (f'<g transform="translate({x} {y}) scale({sx} {s})" filter="url(#p)">'
            f'<path d="M40 10 Q110 30 135 120 Q95 75 35 45Z" fill="{GOLD_D}"/><path d="M45 5 Q130 10 170 85 Q115 50 40 35Z" fill="{GOLD}"/>'
            f'<path d="M48 -2 Q140 -10 190 45 Q125 25 42 22Z" fill="{GOLD_L}"/>'
            + stroke("M-10 44 v15 M12 44 v15", ORANGE, 5)
            + f'<ellipse rx="62" ry="46" transform="rotate(-20)" fill="{BIRD}"/><path d="M-74 -44 L-32 -42 L-18 0 L-60 -8Z" fill="{BIRD}"/>'
            f'<ellipse cx="-18" cy="14" rx="34" ry="25" fill="{GOLD_L}"/>'
            f'<path d="M-62 -82 q-5 -20 8 -27 q3 14 0 27z M-52 -84 q6 -21 21 -21 q-4 14 -13 23z" fill="{ORANGE}"/>'
            f'<circle cx="-58" cy="-58" r="26" fill="{BIRD}"/>' + _bird_face(-58, -58, look, sing)
            + f'<path d="M-12 -22 Q40 -42 70 8 Q30 34 -8 18 Q-22 0 -12 -22Z" fill="{GOLD_D}"/>'
            + stroke("M5 -8 q14 6 12 20 M25 -12 q14 6 12 22 M45 -6 q10 6 8 16", GOLD_L, 3) + '</g>')


def bird_fly(x, y, s=1, rot=0, look=(0, 0), rider=""):
    """Wings spread, flying left; `rider` is drawn sitting on its back."""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)">'
            '<path d="M-20 -15 Q-60 -110 -150 -150 Q-110 -70 -60 0Z" fill="#C98420"/>'
            f'<path d="M70 5 Q170 0 240 50 Q160 40 75 30Z" fill="{GOLD}"/><path d="M70 0 Q170 -30 250 -10 Q165 0 75 22Z" fill="{GOLD_L}"/>'
            f'<path d="M68 12 Q150 40 215 100 Q140 70 70 36Z" fill="{GOLD_D}"/><path d="M10 -10 Q30 -120 150 -170 Q125 -80 80 0Z" fill="{GOLD_D}"/>'
            + stroke("M50 -40 q20 -40 60 -70 M72 -24 q16 -30 44 -56", GOLD_L, 3)
            + f'<ellipse rx="88" ry="40" transform="rotate(-6)" fill="{BIRD}"/><ellipse cx="-10" cy="16" rx="56" ry="20" transform="rotate(-6 -10 16)" fill="{GOLD_L}"/>'
            f'<path d="M-114 -10 L-60 -32 L-48 10 L-90 16Z" fill="{BIRD}"/>'
            f'<path d="M-96 -54 q12 -20 34 -16 q-12 10 -24 22z M-104 -52 q0 -20 16 -28 q0 14 -6 28z" fill="{ORANGE}"/>'
            f'<circle cx="-100" cy="-28" r="26" fill="{BIRD}"/>' + _bird_face(-100, -28, look) + rider + '</g>')


# ---------- the brothers and villagers ----------
def person(x, y, s=1, who="little", arms=None, legs="stand", look=(0, 0), mouth="smile", eyes="dot",
           hat=True, tear=False, under="", extra="", shadow=True):
    """Origin at the feet. Little Brother: blue tunic + leaf hat. Big Brother: red-brown tunic, cream sash, plum cap."""
    big = who == "big"
    tun, hw = TUNIC[who], (20 if big else 14)
    hy, hr, aw = (-84, 17, 8) if big else (-78, 15, 6.5)
    lx, ly = look
    if legs == "stand":
        lg = f'<g fill="{TROUSER}"><rect x="{-hw + 4}" y="-28" width="8" height="28" rx="3"/><rect x="{hw - 12}" y="-28" width="8" height="28" rx="3"/></g>'
        dy = 0
    elif legs == "sit":
        lg = (f'<ellipse cx="{-hw - 10}" cy="-3" rx="7" ry="4.5" fill="{SKIN}"/><ellipse cx="{hw + 10}" cy="-3" rx="7" ry="4.5" fill="{SKIN}"/>'
              f'<ellipse cy="-7" rx="{hw + 13}" ry="10" fill="{TROUSER}"/>')
        dy = 18
    else:
        lg, dy = "", 0
    if arms is None:
        arms = [(f"M{-hw + 3} -54 Q{-hw - 7} -44 {-hw - 5} -32", -hw - 5, -30), (f"M{hw - 3} -54 Q{hw + 7} -44 {hw + 5} -32", hw + 5, -30)]
    arm_svg = "".join(stroke(d, tun, aw) + f'<circle cx="{ax}" cy="{ay}" r="{aw * .7:.1f}" fill="{SKIN}"/>' for d, ax, ay in arms)
    body = f'<path d="M{-hw} -26 Q{-hw - 2} -62 0 -{66 if big else 64} Q{hw + 2} -62 {hw} -26Z" fill="{tun}"/>'
    if big:
        body += stroke(f"M{-hw + 1} -42 Q0 -35 {hw - 1} -42", CREAM, 4)
    cap = (f"M{-hr} {hy - 3} Q{-hr - 1} {hy - hr - 4} 0 {hy - hr - 3} Q{hr + 1} {hy - hr - 4} {hr} {hy - 2} "
           f"Q{hr * .5:.0f} {hy - hr * .7:.0f} {-hr * .3:.0f} {hy - hr * .65:.0f} Q{-hr * .7:.0f} {hy - hr * .6:.0f} {-hr} {hy - 3}Z")
    if who == "little":
        hair = stroke(f"M{-hr + 1} {hy - 2} q-1 7 2 11 M{hr - 1} {hy - 2} q1 7 -2 11", HAIR, 4)
        top = (f'<path d="M-28 {hy - 6} L0 {hy - 33} L28 {hy - 6} Q0 {hy + 1} -28 {hy - 6}Z" fill="#F1DFB5"/>'
               + stroke(f"M-28 {hy - 6} Q0 {hy + 1} 28 {hy - 6}", "#D2B98A", 2)) if hat else f'<path d="{cap}" fill="{HAIR}"/>'
    else:
        hair = f'<path d="{cap}" fill="{HAIR}"/>'
        top = (f'<path d="M-19 {hy - 7} Q-18 {hy - 27} 0 {hy - 27} Q18 {hy - 27} 19 {hy - 7}Z" fill="#6B3B5E"/>'
               + stroke(f"M-20 {hy - 7} h40", "#8A5479", 4)) if (hat and big) else ""
    ey = hy - 1 + ly
    if eyes == "happy":
        eye = stroke(f"M-9 {hy} q3.5 -4.5 7 0 M2 {hy} q3.5 -4.5 7 0", INK, 2.2)
    elif eyes == "wide":
        eye = "".join(f'<circle cx="{e}" cy="{hy - 1}" r="4.4" fill="#fff"/><circle cx="{e + lx}" cy="{ey}" r="2.2" fill="{INK}"/>' for e in (-6, 6))
    else:
        eye = "".join(f'<circle cx="{e + lx}" cy="{ey}" r="2.1" fill="{INK}"/>' for e in (-5.5, 5.5))
    mo = {"smile": stroke(f"M-4 {hy + 6} Q0 {hy + 10} 4 {hy + 6}", "#5B3A22", 1.9),
          "open": f'<path d="M-5 {hy + 5} Q0 {hy + 13} 5 {hy + 5}Z" fill="#8C3B3B"/>',
          "smug": stroke(f"M-4 {hy + 8} Q2 {hy + 9} 6 {hy + 4}", "#5B3A22", 1.9),
          "o": f'<ellipse cy="{hy + 8}" rx="2.6" ry="3.2" fill="#8C3B3B"/>'}[mouth]
    cheeks = f'<circle cx="-10" cy="{hy + 5}" r="3.4" fill="{PINK}" opacity=".6"/><circle cx="10" cy="{hy + 5}" r="3.4" fill="{PINK}" opacity=".6"/>'
    drop = f'<path d="M-9 {hy + 3} q4 7 0 10 q-4 -3 0 -10z" fill="#6FB7E8"/>' if tear else ""
    f = ' filter="url(#p)"' if shadow else ""
    return (f'<g transform="translate({x} {y}) scale({s})"{f}>{lg}<g transform="translate(0 {dy})">{body}{under}{arm_svg}'
            f'<circle cy="{hy}" r="{hr}" fill="{SKIN}"/>{hair}{top}{eye}{cheeks}{mo}{drop}{extra}</g></g>')


# ---------- props ----------
def hut(x, y, s=1, mended=False):
    wall, roof, line = ("#DDB98E", "#B58A4E", "#D2A868") if mended else ("#C9A27A", "#8B6A46", "#A8845A")
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><rect x="-46" y="-62" width="92" height="62" fill="{wall}"/>'
            f'<rect x="-10" y="-38" width="24" height="38" fill="#6B4A35"/><path d="M-64 -56 L0 -110 L64 -56Z" fill="{roof}"/>'
            + stroke("M-48 -56 L0 -96 L48 -56", line, 4) + '</g>')


def big_house(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><rect x="-90" y="-90" width="180" height="90" fill="#E9D8BC"/>'
            '<g fill="#6B4A35"><rect x="-16" y="-52" width="32" height="52"/><rect x="-70" y="-64" width="30" height="26" rx="3"/><rect x="40" y="-64" width="30" height="26" rx="3"/></g>'
            '<path d="M-118 -84 Q-100 -96 -72 -132 H72 Q100 -96 118 -84Z" fill="#9C4A35"/><path d="M-60 -130 Q-46 -140 -34 -162 H34 Q46 -140 60 -130Z" fill="#B55A40"/>'
            + stroke("M-96 -104 H96", "#7E3828", 4) + '<g fill="#B5533C"><rect x="-92" y="-90" width="10" height="90"/><rect x="82" y="-90" width="10" height="90"/></g></g>')


def buffalo(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">' + stroke("M-44 -8 q-14 6 -12 26", "#6E6A72", 5)
            + '<g fill="#5E5A62"><rect x="-30" y="12" width="11" height="30" rx="5"/><rect x="24" y="12" width="11" height="30" rx="5"/></g>'
            '<g fill="#6E6A72"><rect x="-40" y="12" width="12" height="32" rx="5"/><rect x="12" y="12" width="12" height="32" rx="5"/><ellipse rx="48" ry="28"/><circle cx="50" cy="-18" r="21"/></g>'
            + stroke("M38 -34 Q26 -58 50 -62 M62 -34 Q76 -56 54 -64", CREAM, 6)
            + f'<ellipse cx="58" cy="-9" rx="13" ry="10" fill="#8E8A92"/><circle cx="54" cy="-9" r="1.8" fill="{INK}"/><circle cx="62" cy="-9" r="1.8" fill="{INK}"/>'
            f'<circle cx="46" cy="-24" r="2.6" fill="{INK}"/></g>')


def bag(x, y, s=1, full=False):
    top = ("".join(f'<circle cx="{a}" cy="{b}" r="6" fill="{c}"/>' for a, b, c in [(-6, -11, GOLD), (6, -12, GOLD_L), (0, -17, GOLD)])
           if full else f'<path d="M-9 -8 l9 -12 l9 12z" fill="{BAGRED}"/>')
    return (f'<g transform="translate({x} {y}) scale({s})">{top}<path d="M-14 -8 Q-22 22 0 26 Q22 22 14 -8 Q0 -2 -14 -8Z" fill="{BAGRED}"/>'
            + stroke("M-12 -6 Q0 -1 12 -6", "#7E2F22", 2.6) + '</g>')


def giant_bag(x, y, s=1, full=False):
    top = ("".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in
                   [(196, -78, 16, GOLD), (220, -64, 15, GOLD_L), (176, -66, 14, GOLD_D), (204, -96, 12, GOLD_L), (236, -80, 11, GOLD)]) if full else "")
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">{top}'
            f'<path d="M10 0 Q-20 -40 20 -72 Q60 -104 120 -90 Q180 -106 222 -62 Q244 -40 234 -18 Q222 8 170 4Z" fill="{BAGRED}"/>'
            '<path d="M60 -60 l26 -6 l4 24 l-26 6z M140 -40 l22 4 l-4 22 l-22 -4z" fill="#A8432F"/>'
            + stroke("M214 -70 Q232 -52 232 -26", "#7E2F22", 5) + stroke("M40 -30 q10 -22 34 -30 M120 -70 q30 -6 50 8", "#DB7A66", 4) + '</g>')


def gold_pile(x, y, s=1):
    pts = [(-16, 2, 12, GOLD_D), (14, 4, 11, GOLD_D), (0, -6, 14, GOLD), (-8, -16, 8, GOLD_L), (12, -12, 7, GOLD_L)]
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            + "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in pts) + '<circle cx="-4" cy="-10" r="3" fill="#FFF3C0"/></g>')


def pool(x, y, s=1):
    gems = [(-24, -2, "#E0566B"), (2, 3, "#4FB286"), (24, -3, "#4A90C2"), (-6, -8, "#9A6FD0")]
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><ellipse rx="62" ry="24" fill="#8E8478"/><ellipse rx="48" ry="16" fill="#5FB7C4"/>'
            + "".join(f'<path d="M{a} {b - 8} l7 8 l-7 8 l-7 -8z" fill="{c}"/><circle cx="{a - 2}" cy="{b - 3}" r="1.6" fill="#fff"/>' for a, b, c in gems) + '</g>')


def crab(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})">' + stroke("M-8 2 l-7 5 M8 2 l7 5 M-7 -2 l-8 -6 M7 -2 l8 -6", "#C7422B", 2.4)
            + f'<circle cx="-16" cy="-10" r="4.5" fill="#E8573B"/><circle cx="16" cy="-10" r="4.5" fill="#E8573B"/><ellipse rx="10" ry="7" fill="#E8573B"/>'
            f'<circle cx="-3.5" cy="-2" r="1.6" fill="{INK}"/><circle cx="3.5" cy="-2" r="1.6" fill="{INK}"/></g>')


def bowl(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cy="-4" rx="13" ry="8" fill="#fff"/>'
            '<path d="M-15 -3 Q-13 12 0 12 Q13 12 15 -3Z" fill="#E9D8BC"/></g>')


def hand(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{SKIN}" filter="url(#p)"><rect x="-17" y="-6" width="34" height="30" rx="10"/>'
            + "".join(f'<rect x="{a}" y="{-30 + abs(a + 4) * .5:.0f}" width="7.5" height="32" rx="3.7"/>' for a in (-17, -8, 1, 10))
            + '<rect x="-27" y="0" width="14" height="8" rx="4" transform="rotate(-30 -20 4)"/></g>')


def swirl(x, y, s=1, rot=0):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{stroke("M0 0 q10 -16 24 -6 q10 10 -3 18 q-12 4 -13 -7 q1 -6 7 -5", GOLD, 4.5)}</g>'


def heart(x, y, s=1):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 6 Q-12 -4 -6 -10 Q-1 -13 0 -6 Q1 -13 6 -10 Q12 -4 0 6Z" fill="#E0566B"/>'


def svg(n, title, desc, stops, body):
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1c2030" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           f'<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="{GOLD}"/>'
           f'<g id="kf"><path d="M0 -14 v-7" stroke="#5B3A22" stroke-width="2" stroke-linecap="round"/><path d="M0 -14 Q8 -9 7 2 Q6 13 0 16 Q-6 13 -7 2 Q-8 -9 0 -14Z" fill="{GOLD}"/><path d="M0 -12 V14" stroke="#D99A1E" stroke-width="1.8"/></g>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n'
           + "\n".join(body) + '\n</g>\n</svg>\n')
    with open(os.path.join(OUT, f"khe-p{n:02d}.svg"), "w") as fh:
        fh.write(doc)


LAND = [hill(390, 44, "#8FC2A0"), hill(455, 28, "#5FA06C"), hill(525, 18, "#3F7D5A")]
BASKET = lambda x, y: (f'<g filter="url(#p)"><path d="M{x - 26} {y - 26} h52 l-8 30 h-36z" fill="#C9A27A"/>{stroke(f"M{x - 28} {y - 26} h56", "#8B6A46", 5)}</g>'
                       + fruit(x - 12, y - 36, 1.1, -30) + fruit(x + 2, y - 40, 1.1) + fruit(x + 14, y - 36, 1.1, 30))
WAVE = lambda: [("M11 -54 Q26 -66 30 -86", 31, -90)]

# 01 cover
svg(1, "The Starfruit Tree", "Paper-cut cover at dawn: a giant golden bird sits in a starfruit tree full of golden fruit, and Little Brother in his leaf hat waves up at it from beside his little hut.", DAWN, [
    '<circle cx="250" cy="410" r="84" fill="#FBE6CF"/>', hill(400, 60, "#9A86B8"), hill(465, 40, "#5F8F7F"), hill(525, 24, "#3F7D5A"),
    hut(110, 532, 1.15), trunk(585, 550, 250, 42), branch(580, 352, 400, 348), canopy(575, 165, 1),
    bird(552, 264, 1.25, look=(-1, 2)), blobs([(745, 130, 54)], "#3F9460"), fruits(575, 165, 1),
    person(300, 552, 1.35, arms=[(f"M-11 -54 Q-21 -44 -19 -32", -19, -30)] + WAVE(), look=(2.5, -2)), BASKET(390, 560),
    star(410, 262, 1.2), star(370, 205, .7), star(455, 305, .6)])

# 02 dividing things up
field = ('<path filter="url(#p)" d="M0 500 Q200 484 430 500 L400 600 H0Z" fill="#7DB86E"/>'
         + stroke("M30 520 Q210 506 420 520 M10 548 Q200 534 412 548 M0 578 Q190 562 404 578", "#5FA06C", 5))
svg(2, "The brothers share things out", "Paper-cut scene: Big Brother stands proudly by the big house with its rice fields and a water buffalo, while Little Brother stands happily by one starfruit tree and a tiny hut.", DAY, [
    *LAND[:2], big_house(215, 478, 1.25), field, buffalo(330, 530, 1),
    person(95, 566, 1.7, "big", arms=[("M-17 -54 Q-36 -46 -21 -36", -21, -36), ("M17 -54 Q36 -46 21 -36", 21, -36)], eyes="happy", mouth="smug"),
    '<path filter="url(#p)" d="M430 500 Q600 480 800 500 V600 H400Z" fill="#3F7D5A"/>',
    '<g fill="#8B6A46" filter="url(#p)"><rect x="436" y="470" width="9" height="46" rx="3"/><rect x="424" y="520" width="9" height="46" rx="3"/><rect x="412" y="566" width="9" height="40" rx="3"/></g>',
    trunk(655, 535, 330, 24), canopy(650, 285, .6), fruits(650, 285, .6), hut(748, 540, .7),
    person(545, 556, 1.3, arms=[("M-11 -54 Q-21 -44 -19 -32", -19, -30), ("M11 -54 Q26 -56 36 -62", 38, -63)], look=(2.5, -1))])

# 03 looking after the tree
drops = "".join(f'<path d="M{a} {b} q6 11 0 15 q-6 -4 0 -15z" fill="#6FB7E8"/>' for a, b in [(498, 470), (520, 492), (536, 516), (508, 506), (548, 536)])
svg(3, "Little Brother looks after his tree", "Paper-cut scene: Little Brother waters his starfruit tree and talks to it, and a cut slice of starfruit beside him shows a big golden star.", DAY, [
    *LAND, trunk(635, 565, 220, 46), canopy(640, 130, 1.1), fruits(640, 130, 1.1),
    '<ellipse cx="610" cy="566" rx="70" ry="10" fill="#6FB7E8" opacity=".5"/>', drops,
    f'<g filter="url(#p)" transform="translate(468 468) rotate(38)"><path d="M-16 -14 h32 l-5 28 h-22z" fill="#A8845A"/>{stroke("M-16 -14 h32", "#6B4A35", 4)}</g>',
    person(385, 556, 1.6, arms=[("M-11 -54 Q-21 -44 -19 -32", -19, -30), ("M11 -54 Q26 -54 40 -52", 42, -52)], look=(2.5, 0), mouth="open"),
    heart(470, 380, 1.4), heart(505, 345, 1), heart(520, 395, .8),
    '<circle cx="190" cy="185" r="128" fill="#FFF6E6" filter="url(#p)"/>', slice_(190, 188, 9.5, 8),
    fruit(86, 372, 2.6, -20), stroke("M52 372 L120 372", CREAM, 4, ' stroke-dasharray="4 9"'), stroke("M112 330 Q150 318 160 300", CREAM, 4, ' stroke-dasharray="2 9"')])

# 04 whoosh
leaves = "".join(f'<ellipse cx="{a}" cy="{b}" rx="11" ry="5" transform="rotate({r} {a} {b})" fill="#58AB6E"/>' for a, b, r in [(330, 110, 30), (120, 330, -40), (390, 400, 20), (60, 120, 60), (300, 470, -20)])
svg(4, "Whoosh — the golden bird", "Paper-cut scene: with a whoosh, a giant golden bird as big as a boat swoops down onto the starfruit tree, bending its branches, while Little Brother holds on to his hat in surprise.", DAY, [
    *LAND, '<path filter="url(#p)" d="M190 555 Q200 420 150 300 L205 285 Q262 420 272 555Z" fill="#7A5236"/>',
    f'<g transform="rotate(-12 200 300)">{canopy(215, 200, .95)}{fruits(215, 200, .95)}</g>', leaves,
    marks(["M560 90 q70 -34 150 -10", "M600 140 q70 -24 140 -4", "M640 360 q60 14 110 -10", "M430 60 q30 -24 70 -22"], CREAM, 6),
    bird_fly(470, 258, 1.42, -10, look=(-1, 2)),
    marks(["M100 250 q-20 20 -14 48"], "#fff", 4),
    person(690, 556, 1.3, arms=[("M-11 -54 Q-26 -70 -17 -94", -16, -97), ("M11 -54 Q21 -44 19 -32", 19, -30)], look=(-2.5, -2), eyes="wide", mouth="o")])

# 05 the bird sings
svg(5, "The bird sings its rhyme", "Paper-cut scene: Little Brother looks up at the golden bird with a tear on his cheek and his hands held politely together, and the bird looks kindly back at him as it sings in golden swirls.", DAY, [
    *LAND, trunk(610, 565, 280, 42), branch(605, 362, 385, 356), canopy(605, 170, 1.05),
    bird(548, 268, 1.3, look=(-1.5, 2.5), sing=True), fruits(605, 170, 1.05),
    swirl(345, 215, 1.5, -10), swirl(300, 290, 1.2, 20), swirl(250, 350, 1, -20), star(400, 268, .7), star(290, 240, .6), star(330, 360, .5),
    person(215, 556, 1.65, arms=[("M-11 -54 Q-9 -42 -2 -40", -1, -40), ("M11 -54 Q9 -42 2 -40", 1, -40)], look=(2.5, -2.5), tear=True)])

# 06 three hands long
dots = "".join(f'<circle cx="{380 + 130 * i + 16 * j - 8 * i}" cy="424" r="6" fill="{CREAM}"/>' for i in range(3) for j in range(i + 1))
svg(6, "A bag three hands long", "Paper-cut scene inside the hut: Little Brother sits sewing a small red cloth bag and measures it with his hands in a row — one hand, two hands, three hands.", [(0, "#B98A5E"), (1, "#D9B88E")], [
    stroke("M0 120 H800 M0 250 H800 M0 380 H800", "#A87C52", 4),
    '<g filter="url(#p)"><rect x="560" y="60" width="170" height="150" rx="10" fill="#9FD3D6"/><circle cx="700" cy="70" r="60" fill="#3F9460"/></g>' + fruit(660, 120, 1.6) + fruit(705, 150, 1.4)
    + stroke("M560 60 h170 v150 h-170z M645 60 v150", "#7A5236", 8),
    '<rect y="470" width="800" height="130" fill="#C9A27A"/>' + stroke("M0 500 H800 M0 535 H800 M0 570 H800", "#B58E63", 3),
    f'<rect x="310" y="462" width="420" height="92" rx="12" fill="{BAGRED}" filter="url(#p)"/>'
    + stroke("M326 476 H714 M326 540 H714", CREAM, 3, ' stroke-dasharray="10 8"'),
    hand(380, 510, 1.7), hand(510, 510, 1.7), hand(640, 510, 1.7), dots,
    stroke("M716 470 L770 420", "#DADDE8", 4) + stroke("M770 420 q-30 -20 -10 -44 q24 -20 -6 -40", "#E0566B", 3),
    person(200, 548, 2.1, legs="sit", arms=[("M-11 -54 Q-21 -44 -16 -34", -15, -32), ("M11 -54 Q30 -48 42 -36", 44, -34)], look=(2.5, 2), mouth="open")])

# 07 moonlit flight
rider = person(-22, -4, 1, arms=[("M-10 -54 Q-26 -48 -36 -36", -38, -34), ("M10 -54 Q22 -48 26 -40", 27, -38)], legs="none", look=(-2.5, 0),
               mouth="open", shadow=False, extra=bag(28, -22, .9)).replace('<g transform="translate(0 0)">', f'<g><ellipse cx="2" cy="-22" rx="10" ry="16" fill="{TROUSER}"/>')
sea = lambda y, c: f'<path filter="url(#p)" d="M0 {y} Q50 {y - 10} 100 {y} T200 {y} T300 {y} T400 {y} T500 {y} T600 {y} T700 {y} T800 {y} V600 H0Z" fill="{c}"/>'
moonpath = '<g fill="#F7F0D8" opacity=".6">' + "".join(f'<rect x="{600 - w / 2:.0f}" y="{y}" width="{w}" height="6" rx="3"/>' for y, w in [(452, 90), (468, 56), (500, 110), (518, 52), (556, 84), (578, 40)]) + '</g>'
svg(7, "Flying over the moonlit sea", "Paper-cut night scene: Little Brother rides on the golden bird's back over a calm silver sea, holding his small cloth bag, under a big round moon with a glittering island far away.", NIGHT, [
    '<circle cx="600" cy="130" r="98" fill="#F7F0D8" opacity=".12"/><circle cx="600" cy="130" r="64" fill="#F7F0D8"/><g fill="#E6DDBF"><circle cx="582" cy="112" r="10"/><circle cx="620" cy="146" r="13"/><circle cx="608" cy="100" r="5"/></g>',
    cloud(90, 190, 1.1, "#3A3E88"), cloud(720, 260, 1, "#3A3E88"),
    *[star(a, b, s) for a, b, s in [(70, 70, 1.1), (190, 130, .7), (300, 50, .9), (430, 100, .6), (740, 60, .8), (50, 300, .7), (150, 30, .5), (480, 30, .5)]],
    '<rect y="440" width="800" height="160" fill="#2E3F84"/>', '<path filter="url(#p)" d="M70 442 Q100 408 135 418 Q165 398 190 442Z" fill="#141A40"/>',
    star(124, 420, .6), star(150, 428, .45), star(104, 430, .4), sea(482, "#253473"), sea(540, "#1A2556"), moonpath,
    bird_fly(390, 300, 1.25, rider=rider), star(700, 340, .7), star(730, 400, .5), star(300, 190, .5)])

# 08 enough
ISLAND = ['<rect y="300" width="800" height="90" fill="#7C86C2"/>' + stroke("M40 330 h90 M300 350 h120 M560 326 h100 M690 356 h70", "#A9B1DC", 4),
          hill(385, 22, "#EBD3BE"), hill(490, 16, "#E0C2A8")]
svg(8, "Just one small bag", "Paper-cut scene on the sparkling island: Little Brother kneels among golden stones and jewel-coloured rock pools with his small bag full, and holds up a hand to say that is enough.", DAWN, [
    *ISLAND, bird(650, 330, .8, look=(-1, 2)), '<ellipse cx="640" cy="386" rx="80" ry="22" fill="#8E8478" filter="url(#p)"/>',
    pool(150, 472, 1.25), pool(640, 530, 1.3), gold_pile(270, 430, 1.2), gold_pile(520, 440, 1.1), gold_pile(80, 560, 1.3), gold_pile(740, 440, 1), gold_pile(470, 566, 1.2),
    star(300, 380, .8), star(560, 396, .7), star(110, 400, .6), star(700, 470, .6), star(230, 520, .6),
    person(380, 548, 1.9, legs="sit", arms=[("M-11 -54 Q-20 -44 -12 -36", -11, -34), ("M11 -54 Q30 -58 34 -76", 35, -79)], look=(0, 1.5), extra=bag(-4, -30, 1, True))])

# 09 sharing rice
svg(9, "Rice for everyone", "Paper-cut village scene: outside his newly mended hut, Little Brother hands bowls of rice to smiling neighbours — a woman, an old man and a child.", DAY, [
    cloud(180, 130, 1.1), cloud(520, 90, .8), *LAND, trunk(725, 525, 340, 22), canopy(722, 300, .55), fruits(722, 300, .55), hut(150, 536, 1.55, True),
    '<g filter="url(#p)"><path d="M228 556 Q220 500 246 490 h34 Q306 500 298 556Z" fill="#F6EFE0"/></g>' + stroke("M246 492 h34", "#B58E63", 5),
    person(345, 560, 1.45, arms=[("M-11 -54 Q-21 -44 -19 -32", -19, -30), ("M11 -54 Q26 -54 38 -52", 40, -52)], look=(2.5, 0), mouth="open"), bowl(412, 480, 1.3),
    person(495, 560, 1.45, "v1", arms=[("M-11 -54 Q-26 -52 -36 -48", -38, -48), ("M11 -54 Q21 -44 19 -32", 19, -30)], eyes="happy", mouth="open"),
    person(640, 562, 1.5, "v2", arms=[("M-11 -54 Q-16 -42 -6 -38", -5, -38), ("M11 -54 Q16 -42 6 -38", 5, -38)], eyes="happy", extra=bowl(0, -42, .9)),
    person(568, 572, .95, "v3", arms=[("M-11 -54 Q-26 -66 -28 -84", -28, -87), ("M11 -54 Q26 -66 28 -84", 28, -87)], eyes="happy", mouth="open"),
    heart(440, 400, 1.3), heart(590, 380, 1), heart(520, 350, .8)])

# 10 the giant bag
svg(10, "Big Brother's giant bag", "Paper-cut scene: Big Brother, looking very pleased with himself, drags a giant red bag along the ground under the starfruit tree while the golden bird watches from a branch.", DAY, [
    *LAND, trunk(630, 565, 290, 42), branch(625, 372, 430, 364), canopy(625, 180, 1), bird(590, 276, 1.2, look=(-2, 2.5)), fruits(625, 180, 1),
    marks(["M10 566 h70 M30 582 h90"], "#2F5E44", 5), giant_bag(30, 552, 1.05), stroke("M270 520 Q300 500 296 488", "#F6EFE0", 4),
    person(370, 562, 1.75, "big", arms=[("M-17 -54 Q-36 -50 -42 -42", -43, -41), ("M17 -54 Q27 -44 25 -32", 25, -30)], eyes="happy", mouth="smug", look=(2, 0))])

# 11 more, more, more
cap_full = (f'<g transform="translate(-42 -46)"><circle cx="-6" cy="-4" r="7" fill="{GOLD}"/><circle cx="6" cy="-5" r="7" fill="{GOLD_L}"/><circle cy="-11" r="6" fill="{GOLD}"/>'
            '<path d="M-16 -2 Q-15 15 0 15 Q15 15 16 -2Z" fill="#6B3B5E"/></g>')
stuffed = (f'<g fill="{GOLD}"><circle cx="-15" cy="-34" r="5"/><circle cx="15" cy="-34" r="5"/><circle cx="-11" cy="-39" r="4"/><circle cx="12" cy="-40" r="4"/>'
           f'<circle cx="-13" cy="-2" r="4.5"/><circle cx="13" cy="-2" r="4.5"/><circle cx="-8" cy="-5" r="3.5"/><circle cx="9" cy="-5" r="3.5"/><circle cx="42" cy="-90" r="5.5"/><circle cx="36" cy="-95" r="4"/></g>')
svg(11, "More, more, more!", "Paper-cut scene on the sparkling island: Big Brother grabs gold with a huge grin — his giant bag bulging, his pockets stuffed, his hat full and even his shoes full — while the golden bird looks on.", DAWN, [
    *ISLAND, bird(690, 330, .8, look=(-2, 1)), '<ellipse cx="680" cy="386" rx="80" ry="22" fill="#8E8478" filter="url(#p)"/>',
    pool(620, 540, 1.2), gold_pile(540, 440, 1.1), gold_pile(730, 470, 1), gold_pile(330, 420, .9),
    giant_bag(20, 560, 1.15, True),
    person(430, 556, 2.05, "big", hat=False, arms=[("M-17 -54 Q-34 -54 -42 -46", -42, -44), ("M17 -54 Q38 -62 40 -82", 40, -84)], eyes="wide", mouth="open", look=(0, 1), extra=cap_full + stuffed),
    *[star(a, b, s, r) for a, b, s, r in [(560, 330, 1, 10), (350, 300, .8, 0), (590, 250, .6, 20), (300, 360, .6, 0), (480, 300, .5, 0)]],
    marks(["M545 370 q10 -16 2 -30", "M330 330 q-12 -12 -6 -28"], "#fff", 4)])

# 12 splash
weed = stroke("M-14 -99 q-8 6 -7 16 M-3 -103 q5 6 1 13 M9 -101 q9 5 9 15", "#3F9460", 5)
splash = "".join(f'<path d="M{a} {b} q8 14 0 20 q-8 -6 0 -20z" fill="#fff" transform="rotate({r} {a} {b})"/>' for a, b, r in
                 [(320, 410, -30), (296, 446, -50), (570, 410, 30), (594, 446, 50), (350, 372, -20), (540, 372, 20)])
svg(12, "Splash!", "Paper-cut scene: the golden bird wobbles low over the waves close to the beach, and Big Brother sits with a splash in warm shallow water up to his tummy, seaweed on his head and a little crab on his nose.", DAY, [
    hill(330, 30, "#8FC2A0"), '<rect y="340" width="800" height="260" fill="#6FB7C8"/>',
    '<path filter="url(#p)" d="M470 600 Q560 470 800 410 V600Z" fill="#EBD3BE"/>', hut(735, 440, .6), trunk(670, 440, 350, 12), canopy(668, 330, .32),
    '<g fill="#D9BFA6"><ellipse cx="640" cy="520" rx="9" ry="5"/><ellipse cx="672" cy="498" rx="9" ry="5"/><ellipse cx="700" cy="474" rx="9" ry="5"/></g>',
    bird_fly(215, 232, 1, 12, look=(2, 3)), marks(["M60 150 q-16 16 -10 40", "M380 120 q16 16 10 40", "M110 322 q20 14 46 6"], "#fff", 5),
    f'<g filter="url(#p)" transform="translate(250 470) rotate(-20)"><path d="M-40 0 Q-50 -40 0 -46 Q50 -40 40 0Z" fill="{BAGRED}"/></g>' + star(236, 520, .7) + star(270, 548, .5),
    person(445, 556, 2.4, "big", hat=False, legs="none", arms=[("M-17 -54 Q-38 -62 -42 -82", -42, -85), ("M17 -54 Q38 -62 42 -82", 42, -85)], eyes="wide", mouth="o",
           extra=weed + crab(0, -77, .42)),
    '<path d="M0 468 Q50 458 100 468 T200 468 T300 468 T400 468 T500 468 Q540 462 560 480 Q500 560 470 600 H0Z" fill="#5FA7BC"/>',
    '<ellipse cx="445" cy="470" rx="96" ry="16" fill="none" stroke="#fff" stroke-width="5" opacity=".9"/>', splash,
    marks(["M60 520 q16 -8 32 0", "M180 560 q16 -8 32 0", "M330 540 q16 -8 32 0", "M120 400 q16 -8 32 0", "M620 380 q16 -8 32 0"], "#DDF1F5", 4),
    '<g fill="#fff" opacity=".8"><circle cx="232" cy="446" r="5"/><circle cx="262" cy="430" r="3.5"/><circle cx="246" cy="412" r="2.6"/></g>'])

# 13 sharing stars
towel = '<path d="M-26 -30 Q-29 -68 0 -70 Q29 -68 26 -30 Q14 -48 0 -49 Q-14 -48 -26 -30Z" fill="#F6EFE0"/>' + stroke("M-21 -38 q4 -6 8 -8 M21 -38 q-4 -6 -8 -8", "#D9CDB4", 2)
svg(13, "Sharing stars", "Paper-cut scene: the two brothers sit together under the starfruit tree eating star-shaped slices of golden fruit, Big Brother with a towel round his shoulders, while the golden bird watches from a branch.", DAY, [
    *LAND, trunk(660, 575, 230, 46), '<g filter="url(#p)">' + stroke("M650 300 Q420 220 120 252", WOOD, 22) + '</g>',
    blobs([(110, 70, 100), (560, 60, 120)], "#2F7D4F"), blobs([(330, 30, 115), (740, 150, 80)], "#3F9460"), blobs([(220, 50, 56), (470, 30, 60), (690, 90, 44)], "#58AB6E", False),
    *[fruit(a, b) for a, b in [(70, 165), (330, 158), (420, 130), (520, 190), (740, 240), (640, 150), (250, 120)]],
    bird(205, 196, .75, True, look=(-1.5, 2.5)),
    person(285, 578, 1.9, "big", hat=False, legs="sit", under=towel, eyes="happy", mouth="open",
           arms=[("M-17 -54 Q-32 -40 -26 -28", -25, -26), ("M17 -54 Q34 -56 34 -72", 34, -75)], extra=slice_(36, -90, 1.5, 12)),
    person(515, 582, 1.5, legs="sit", eyes="happy", mouth="open",
           arms=[("M-11 -54 Q-28 -56 -28 -72", -28, -75), ("M11 -54 Q24 -40 20 -28", 19, -26)], extra=slice_(-30, -90, 1.5, -12)),
    BASKET(405, 578), star(400, 470, .8), star(150, 340, .6), star(600, 420, .5)])
