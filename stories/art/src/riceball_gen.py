#!/usr/bin/env python3
"""Generates the 13 Rolling Rice Ball flip-book SVGs from shared character parts.

Usage: python3 riceball_gen.py [out_dir]   (default: the folder above src/)
"""
import math
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

INK, CREAM, GOLD, GOLD_L = "#2B2320", "#F6E7D0", "#F6C445", "#FBE48A"
SKIN, SKIN_D, HAIR = "#F3C9A0", "#C98F62", "#E9E8EF"
JB, JD, JL = "#3F6FB0", "#2F5488", "#A9C6E8"          # Grandpa's jinbei
GK, APRON = "#4E9A9A", "#F6B8C6"                      # Grandma's kimono and apron
FUR, PINK, RED = "#D3CEDB", "#EFA3B0", "#E4572E"      # mice
BARK, BARK_D, HOLE = "#7A5236", "#63412A", "#2B1D16"
G1, G2, G3, LEAF_D, LEAF_L = "#6DB56B", "#A8D8A0", "#8FC2A0", "#2F7D4F", "#58AB6E"
CLOTH, CLOTH_D = "#7A5BA6", "#5E4388"                 # furoshiki
WOOD, WOOD_D = "#B7814F", "#8E5F38"                   # the small box
NOTE = "#F0766B"
KIMONO = ["#E07A5F", "#6A8FD8", "#B48EDB", "#F2A7B8", "#5FB3B3", "#E8A0C8"]
LEAD = "#6DB56B"

NOON = [(0, "#8CCBE0"), (1, "#EAF4D8")]
MORNING = [(0, "#9FD3D6"), (1, "#FBEBD0")]
EARTH = [(0, "#4A3020"), (1, "#33221A")]
UNDER = [(0, "#2E2030"), (1, "#4A3440")]
SUNSET = [(0, "#F08A5D"), (1, "#FBD9A8")]
HOME = [(0, "#B48A62"), (1, "#D8B58A")]


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pt(p):
    return f"{n(p[0])} {n(p[1])}"


def stroke(d, col=INK, w=5):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none"/>'


def marks(ds, col="#fff", w=4):
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def dashed(d, col=CREAM, w=4, dash="3 12"):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}" fill="none"/>'


def glow(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" opacity=".12"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * .62:.0f}" fill="{GOLD}" opacity=".2"/>')


def blobs(pts, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g fill="{fill}"{f}>' + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>'


def hill(y, amp, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def cloud(x, y, s=1, fill="#FFF6E6"):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}">'
            '<circle cx="-50" cy="8" r="30"/><circle cx="-18" cy="-14" r="36"/><circle cx="24" cy="-10" r="32"/>'
            '<circle cx="56" cy="10" r="28"/><rect x="-78" y="6" width="160" height="34" rx="17"/></g>')


def sun(x, y, r=46):
    return f'<circle cx="{x}" cy="{y}" r="{r * 1.5:.0f}" fill="#FFF6E6" opacity=".35"/><circle cx="{x}" cy="{y}" r="{r}" fill="#FFF6E6"/>'


def slope(x0, y0, cx, cy, x1, y1, fill=G1):
    """A hillside as one quadratic curve; returns its markup and y(x) for standing things on it."""
    def fy(x):
        a, b, c = x0 - 2 * cx + x1, 2 * (cx - x0), x0 - x
        t = -c / b if abs(a) < 1e-9 else (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
        return (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
    return f'<path filter="url(#p)" d="M{x0} {y0} Q{cx} {cy} {x1} {y1} V600 H0Z" fill="{fill}"/>', fy


# ---------- characters ----------

def head(kind, look, eyes, mouth):
    lx, ly = look
    if kind == "pa":   # bald on top, little topknot, side tufts
        back = f'<g fill="{HAIR}"><circle cx="-21" cy="-26" r="9"/><circle cx="21" cy="-26" r="9"/><ellipse cy="-62" rx="6.5" ry="8"/></g>'
        top = stroke("M-5 -56.5 h10", JD, 3.5)
        extra = (stroke("M-6 -52 q6 -2.5 12 0 M19 -39 l5 -2 M19 -35 l5 1 M-19 -39 l-5 -2 M-19 -35 l-5 1", SKIN_D, 1.7)
                 + '<path d="M0 -25 Q-6 -20 -12 -24 Q-6 -29 0 -25 Q6 -29 12 -24 Q6 -20 0 -25Z" fill="#fff"/>')
    else:              # grey hair swept into a bun
        back = f'<g fill="{HAIR}"><circle cy="-37" r="26.5"/><circle cy="-66" r="10"/></g>' + stroke("M-6 -58 h12", APRON, 3.5)
        top = f'<path d="M-24 -38 Q-16 -59 0 -59 Q16 -59 24 -38 Q12 -51 0 -50 Q-12 -51 -24 -38Z" fill="{HAIR}"/>'
        extra = stroke("M19 -38 l4 -1.5 M-19 -38 l-4 -1.5", SKIN_D, 1.7)
    if eyes == "happy":
        e = stroke("M-15 -35 q6 -7 12 0 M3 -35 q6 -7 12 0", INK, 2.8)
    else:
        e = "".join(
            f'<circle cx="{ex}" cy="-36" r="7" fill="#fff"/><circle cx="{n(ex + lx)}" cy="{n(-36 + ly)}" r="3.5" fill="{INK}"/>'
            f'<circle cx="{n(ex + lx + 1.2)}" cy="{n(-37.4 + ly)}" r="1.1" fill="#fff"/>' for ex in (-9, 9))
    my = -18 if kind == "pa" else -21
    m = (f'<path d="M-6 {my - 1} Q0 {my + 9} 6 {my - 1}Z" fill="#B5483F"/>' if mouth == "open"
         else stroke(f"M-5 {my} Q0 {my + 5} 5 {my}", "#8C4A3B", 2.2))
    return (back + f'<g fill="{SKIN}"><circle cx="-23" cy="-33" r="5.5"/><circle cx="23" cy="-33" r="5.5"/><circle cy="-34" r="24"/></g>' + top
            + stroke("M-15 -47 q6 -4 12 -1 M3 -48 q6 -3 12 1", "#fff", 3.4) + e
            + '<g fill="#F08A7A" opacity=".45"><circle cx="-15" cy="-25" r="5"/><circle cx="15" cy="-25" r="5"/></g>'
            + f'<ellipse cy="-29" rx="3.4" ry="2.7" fill="#E0A678"/>' + extra + m)


def person(kind, x, y, s=1, rot=0, flip=False, look=(0, 0), la=None, ra=None, ll=None, rl=None,
           eyes="open", mouth="smile", back="", extra="", sit=False, screen=False):
    """Grandpa ("pa") or Grandma ("ma"). Limbs are (elbow, hand) / (knee, foot) points in local units.
    screen=True gives limb points as offsets on the page (still in local units), ignoring rot and flip."""
    cloth = JB if kind == "pa" else GK

    def cv(p):
        if not screen:
            return p
        a = math.radians(-rot)
        px, py = p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a)
        return (-px if flip else px, py)

    def arm(sx, lim, default):
        el, ha = (cv(p) for p in (lim or default))
        return (stroke(f"M{sx} -2 L{pt(el)}", cloth, 13) + stroke(f"M{pt(el)} L{pt(ha)}", SKIN, 8)
                + f'<circle cx="{n(ha[0])}" cy="{n(ha[1])}" r="6.5" fill="{SKIN}"/>')

    def leg(sx, lim, default):
        kn, ft = (cv(p) for p in (lim or default))
        return stroke(f"M{sx} 34 L{pt(kn)} L{pt(ft)}", JD, 14) + f'<ellipse cx="{n(ft[0])}" cy="{n(ft[1] + 2)}" rx="9" ry="6" fill="#E8B98C"/>'

    if kind == "pa":
        body = (leg(-9, ll, ((-10, 50), (-11, 64))) + leg(9, rl, ((10, 50), (11, 64)))
                + f'<path d="M-20 -6 Q-22 -10 -14 -10 H14 Q22 -10 20 -6 L24 36 Q24 42 16 42 H-16 Q-24 42 -24 36Z" fill="{JB}"/>'
                + stroke("M-8 -10 L3 8 M9 -10 L-11 24", JL, 3.5) + f'<circle cx="-12" cy="25" r="3.2" fill="{JL}"/>')
    else:
        robe = ("M-18 -8 Q-20 -10 -13 -10 H13 Q20 -10 18 -8 L31 42 Q32 52 21 52 H-21 Q-32 52 -31 42Z" if sit
                else "M-18 -8 Q-20 -10 -13 -10 H13 Q20 -10 18 -8 L26 58 Q26 64 18 64 H-18 Q-26 64 -26 58Z")
        ab = 46 if sit else 56
        feet = "" if sit else '<g fill="#E8B98C"><ellipse cx="-9" cy="66" rx="8" ry="5"/><ellipse cx="9" cy="66" rx="8" ry="5"/></g>'
        body = (feet + f'<path d="{robe}" fill="{GK}"/>' + stroke("M-8 -10 L1 4 L9 -10", "#CFE6E2", 3)
                + f'<path d="M-13 8 H13 L18 {ab - 4} Q18 {ab} 13 {ab} H-13 Q-18 {ab} -18 {ab - 4}Z" fill="{APRON}"/>'
                + stroke("M-13 9 L-8 -9 M13 9 L8 -9", APRON, 3) + '<rect x="-7" y="24" width="14" height="11" rx="3" fill="#EE9FB2"/>')
    sx = -s if flip else s
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({n(sx)} {s})" filter="url(#p)">' + back + body
            + arm(-19, la, ((-27, 14), (-25, 32))) + arm(19, ra, ((27, 14), (25, 32)))
            + head(kind, look, eyes, mouth) + extra + '</g>')


CROSS = {"ll": ((-28, 46), (-4, 52)), "rl": ((28, 46), (4, 52))}     # sitting cross-legged
UP = {"la": ((-36, -12), (-42, -42)), "ra": ((36, -12), (42, -42))}  # both arms in the air

M_ARMS = "M-11 0 q-6 6 -4 11 M11 0 q6 6 4 11"
M_DANCE = "M-11 -1 q-10 -5 -13 -15 M11 -1 q10 -5 13 -15"


def mouse_base():
    """Everything but the arms. Kimono colour comes from the fill on the enclosing <g> or <use>."""
    return (stroke("M8 14 Q27 19 23 0", PINK, 2.5)
            + f'<g fill="{PINK}"><ellipse cx="-6" cy="19" rx="5" ry="3"/><ellipse cx="6" cy="19" rx="5" ry="3"/></g>'
            + '<path d="M-10 -7 H10 L13 14 Q13 18 9 18 H-9 Q-13 18 -13 14Z"/>'
            + stroke("M-6 -6 L1 4 L7 -6", CREAM, 2) + '<rect x="-12" y="6" width="24" height="5" rx="2" fill="#FFF6E6"/>'
            + f'<g fill="{FUR}"><circle cx="-11" cy="-30" r="8.5"/><circle cx="11" cy="-30" r="8.5"/></g>'
            + f'<g fill="{PINK}"><circle cx="-11" cy="-30" r="5"/><circle cx="11" cy="-30" r="5"/></g>'
            + f'<circle cy="-18" r="14" fill="{FUR}"/>'
            + '<g fill="#fff"><circle cx="-5.5" cy="-20" r="4.8"/><circle cx="5.5" cy="-20" r="4.8"/></g>'
            + f'<g fill="{INK}"><circle cx="-5" cy="-19.6" r="2.8"/><circle cx="6" cy="-19.6" r="2.8"/></g>'
            + '<g fill="#fff"><circle cx="-4" cy="-20.8" r=".9"/><circle cx="7" cy="-20.8" r=".9"/></g>'
            + stroke("M-4 -12.5 l-10 -2 M-4 -11 l-10 2 M4 -12.5 l10 -2 M4 -11 l10 2", "#8E8898", 1)
            + f'<circle cy="-13" r="2.2" fill="#F2859A"/>' + stroke("M-3 -9.5 Q0 -7 3 -9.5", "#8C4A3B", 1.4))


def mouse(x, y, s=1, rot=0, col=LEAD, flip=False, shadow=True, arms=M_ARMS, band=False, extra=""):
    """An individually posed mouse built on the shared base (the lead mouse wears band=True)."""
    f = ' filter="url(#p)"' if shadow else ""
    hb = (stroke("M-13 -24.5 Q0 -31 13 -24.5", RED, 4) + stroke("M13 -25 l8 -4 M13 -24 l9 3", RED, 3)) if band else ""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({n(-s if flip else s)} {s})" fill="{col}"{f}><use href="#mk"/>'
            + stroke(arms, FUR, 5) + hb + extra + '</g>')


def mice(lst, ref="mm"):
    """Many identical mice from one <defs> copy: (x, y, scale, rotation, kimono colour index)."""
    return '<g filter="url(#p)">' + "".join(
        f'<use href="#{ref}" fill="{KIMONO[c % len(KIMONO)]}" transform="translate({x} {y}) rotate({r}) scale({s})"/>'
        for x, y, s, r, c in lst) + '</g>'


# ---------- props ----------

def riceball(x, y, s=1, rot=0, op=1, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    o = f' opacity="{op}"' if op < 1 else ""
    return f'<use href="#rb" transform="translate({x} {y}) rotate({rot}) scale({s})"{f}{o}/>'


def cloth(x, y, s=1, balls=3):
    """The furoshiki spread open, with rice balls sitting on it."""
    xs = {3: (-30, 0, 30), 2: (-16, 16), 1: (0,), 0: ()}[balls]
    return (f'<g transform="translate({x} {y}) scale({s})"><path filter="url(#p)" d="M-66 0 Q-30 -16 0 -16 Q30 -16 66 0 Q30 16 0 16 Q-30 16 -66 0Z" fill="{CLOTH}"/>'
            f'<g fill="#C9B6E6"><circle cx="-44" cy="1" r="2.5"/><circle cx="44" cy="1" r="2.5"/><circle cx="-16" cy="9" r="2.5"/><circle cx="18" cy="9" r="2.5"/></g>'
            + "".join(riceball(a, -14, .8, shadow=False) for a in xs) + '</g>')


def tree(x, y, s=1, h=300):
    """Back half of the old hole tree: trunk and the dark hole. Follow with whatever is in the hole, then tree_front."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path filter="url(#p)" d="M-40 -{h} Q-34 -120 -46 -50 Q-56 -16 -86 -2 H86 Q56 -16 46 -50 Q34 -120 40 -{h}Z" fill="{BARK}"/>'
            + stroke("M-16 -200 q8 34 -2 70 M18 -150 q-6 24 2 50", BARK_D, 4)
            + f'<ellipse rx="46" ry="20" fill="{HOLE}"/></g>')


def tree_front(x, y, s=1, ground=G1):
    """Front lip of the hole (hides whatever has dropped in) and the two roots that hug it."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-46 0 A46 20 0 0 0 46 0 H58 V42 H-58 V0Z" fill="{ground}"/>'
            f'<g filter="url(#p)">{stroke("M-50 -36 Q-66 2 -100 16 M50 -36 Q66 2 100 16", BARK, 18)}</g></g>')


def note(x, y, s=1, rot=0, col=NOTE):
    return f'<use href="#n" fill="{col}" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def leaf(x, y, s=1, rot=0, col=LEAF_L):
    return f'<use href="#l" fill="{col}" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def star(x, y, s=1):
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def coin(x, y, s=1, rot=0):
    return f'<use href="#c" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def lantern(x, y, s=1, cord=0, g=True):
    return ((glow(x, y, round(36 * s)) if g else "") + (stroke(f"M{x} {n(y - cord * s)} V{y}", HOLE, 2) if cord else "")
            + f'<use href="#ln" transform="translate({x} {y}) scale({s})"/>')


def lantern_line(d, pts):
    return stroke(d, HOLE, 2.2) + "".join(lantern(a, b, 1.25, cord=c) for a, b, c in pts)


def mhouse(x, y, s=1, roof="#B5574A"):
    return (f'<circle cx="{x}" cy="{y - 14 * s:.0f}" r="{17 * s:.0f}" fill="{GOLD}" opacity=".22"/>'
            f'<g transform="translate({x} {y}) scale({s})"><rect x="-20" y="-26" width="40" height="26" rx="4" fill="#C9A27A"/>'
            f'<path d="M-28 -22 Q0 -58 28 -22Z" fill="{roof}"/><circle cx="-8" cy="-14" r="5" fill="{GOLD}"/>'
            f'<path d="M3 0 V-11 Q8.5 -17 14 -11 V0Z" fill="#5B3A22"/></g>')


def gift(x, y, w, h, col, dark, cord, shadow=True):
    """A wrapped box sitting on (x, y): lid, crossed cord and a bow."""
    b, cw, f = w * .15, max(3, w * .045), ' filter="url(#p)"' if shadow else ""
    return (f'<g transform="translate({x} {y})"{f}><rect x="{n(-w / 2)}" y="{n(-h * .8)}" width="{w}" height="{n(h * .8)}" rx="5" fill="{col}"/>'
            f'<rect x="{n(-w / 2 - 4)}" y="{-h}" width="{w + 8}" height="{n(h * .3)}" rx="5" fill="{dark}"/>'
            + stroke(f"M0 {-h} V0 M{n(-w / 2)} {n(-h * .36)} H{n(w / 2)}", cord, n(cw))
            + f'<path d="M0 {-h} q{n(-b)} {n(-b * 1.5)} {n(-b * 1.7)} {n(-b * .4)} q{n(b * .3)} {n(b * .9)} {n(b * 1.7)} {n(b * .4)} '
              f'q{n(b)} {n(-b * 1.5)} {n(b * 1.7)} {n(-b * .4)} q{n(-b * .3)} {n(b * .9)} {n(-b * 1.7)} {n(b * .4)}z" fill="{cord}"/></g>')


def small_box(x, y, w=84, shadow=True):
    return gift(x, y, w, round(w * .72), WOOD, WOOD_D, RED, shadow)


def cave():
    return ['<path d="M-20 600 V300 Q400 10 820 300 V600Z" fill="#5E4450"/>',
            stroke("M110 0 Q124 60 104 118 M250 0 Q244 40 262 72 M690 0 Q700 52 682 100 M560 0 Q566 26 556 48", BARK, 6)]


def floor(y=480, fill="#8A6A62"):
    return f'<path filter="url(#p)" d="M0 {y} Q400 {y - 30} 800 {y} V600 H0Z" fill="{fill}"/>'


DEFS = {
    "mm": lambda: f'<g id="mm"><use href="#mk"/>{stroke(M_ARMS, FUR, 5)}</g>',
    "md": lambda: f'<g id="md"><use href="#mk"/>{stroke(M_DANCE, FUR, 5)}</g>',
    "mk": lambda: f'<g id="mk">{mouse_base()}</g>',
    "rb": lambda: ('<g id="rb"><path d="M0 -22 Q7 -22 11 -15 L23 7 Q28 18 15 18 H-15 Q-28 18 -23 7 L-11 -15 Q-7 -22 0 -22Z" fill="#FFFDF5"/>'
                   '<path d="M-10 18 V4 Q-10 1 -7 1 H7 Q10 1 10 4 V18Z" fill="#2F3B34"/>'
                   + stroke("M-5 -9 l2 -3 M5 -4 l2 3 M-12 6 l1 -3", "#E3DDCB", 1.8) + '</g>'),
    "ln": lambda: (f'<g id="ln"><ellipse rx="11" ry="14" fill="{GOLD_L}"/>' + stroke("M-10.4 -4 H10.4 M-10.4 4 H10.4", "#E9A91F", 1.4)
                   + '<g fill="#4A2E22"><rect x="-6" y="-17" width="12" height="4" rx="1.5"/><rect x="-6" y="13" width="12" height="4" rx="1.5"/></g></g>'),
    "n": lambda: '<g id="n"><ellipse cx="-3" cy="8" rx="6.5" ry="4.8" transform="rotate(-20 -3 8)"/><rect x="1.6" y="-13" width="2.8" height="21" rx="1"/><path d="M4 -13 q11 2 8 13 q-3 -6 -8 -6z"/></g>',
    "l": lambda: '<path id="l" d="M0 -11 Q10 -4 0 11 Q-10 -4 0 -11Z"/>',
    "c": lambda: f'<g id="c"><ellipse rx="11" ry="8" fill="{GOLD}"/><ellipse rx="6.5" ry="4" fill="{GOLD_L}"/></g>',
    "s": lambda: f'<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="{GOLD}"/>',
}


def svg(num, title, desc, stops, body):
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    defs = ""
    for key, make in DEFS.items():   # dict order lets a def pull in the defs it uses
        if f'href="#{key}"' in joined + defs:
            defs += make()
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)" stroke-linecap="round" stroke-linejoin="round"><rect width="800" height="600" fill="url(#sky)"/>\n'
           + joined + '\n</g>\n</svg>\n')
    with open(os.path.join(OUT, f"riceball-{num:02d}.svg"), "w") as fh:
        fh.write(doc)


def flowers(pts):
    return ('<g fill="#fff">' + "".join(f'<circle cx="{a}" cy="{b}" r="6"/>' for a, b in pts) + '</g><g fill="#F2A7B8">'
            + "".join(f'<circle cx="{a}" cy="{b}" r="2.6"/>' for a, b in pts) + '</g>')


FAR = '<path d="M0 340 Q240 190 520 330 T800 290 V600 H0Z" fill="' + G2 + '"/>'

# 01 cover
hillside, hy = slope(0, 200, 300, 240, 800, 520)
svg(1, "The Rolling Rice Ball", "Paper-cut cover: a triangle rice ball wrapped in seaweed rolls down a green hillside toward a small hole between the roots of an old tree, where a little mouse in a red headband peeks out and waves.", NOON, [
    sun(120, 96), cloud(330, 80, .8), FAR, hillside,
    tree(620, 505, 1.5), mouse(620, 512, 2.3, band=True, arms="M-11 0 q-6 6 -4 11 M11 0 q11 -6 13 -17"), tree_front(620, 505, 1.5),
    blobs([(640, 30, 120), (780, 110, 100), (520, 10, 70)], LEAF_D), blobs([(700, 60, 60), (590, 70, 44)], LEAF_L, False),
    marks(["M96 150 q50 -58 104 2", "M150 196 q30 -30 64 0", "M214 150 q34 -4 50 22"], "#fff", 5),
    dashed("M400 262 Q520 250 580 452", CREAM, 5, "4 15"),
    '<ellipse cx="322" cy="300" rx="62" ry="10" fill="#2F7D4F" opacity=".35"/>', riceball(318, 222, 3, 24),
    flowers([(90, 330), (190, 420), (60, 500), (330, 480), (440, 400), (250, 560), (470, 540)])])

# 02 the little wooden house
svg(2, "Grandma wraps three rice balls", "Paper-cut morning scene: outside a little wooden house with a thatched roof, Grandma in her pink apron wraps three rice balls in a purple cloth on a low table while Grandpa, in his blue jinbei, waves.", MORNING, [
    sun(670, 110, 50), cloud(500, 80, .8), hill(330, 46, G2, False), hill(410, 26, G3),
    '<g filter="url(#p)"><rect x="60" y="250" width="350" height="240" fill="#D8B58A"/><path d="M14 268 L112 132 Q122 118 140 118 H330 Q348 118 358 132 L456 268Z" fill="#8A6B4A"/></g>'
    '<path d="M132 128 H338 L350 146 H120Z" fill="#A9895F"/><rect x="246" y="322" width="100" height="168" fill="#5B3A22"/>'
    f'<g fill="{BARK}"><rect x="60" y="262" width="12" height="228"/><rect x="398" y="262" width="12" height="228"/><rect x="226" y="262" width="12" height="228"/></g>'
    '<rect x="98" y="322" width="96" height="74" rx="4" fill="#FFF6E6"/>' + stroke("M146 322 V396 M98 359 H194", BARK, 4),
    '<path filter="url(#p)" d="M0 486 Q400 466 800 490 V600 H0Z" fill="#E6D3A8"/>',
    person("ma", 296, 388, 1.8, look=(2.5, 2), la=((-28, 16), (-12, 30)), ra=((32, 16), (48, 30))),
    f'<g filter="url(#p)"><rect x="376" y="462" width="176" height="15" rx="5" fill="#A56C34"/><g fill="{WOOD_D}"><rect x="390" y="477" width="14" height="50"/><rect x="524" y="477" width="14" height="50"/></g></g>',
    f'<path d="M380 462 Q464 430 548 462 L540 476 H388Z" fill="{CLOTH}"/><path d="M380 462 l-12 -14 l22 4z M548 462 l12 -14 l-22 4z" fill="{CLOTH_D}"/>',
    riceball(424, 436, 1.05), riceball(464, 432, 1.05), riceball(504, 436, 1.05),
    person("pa", 650, 392, 1.8, look=(-2.5, 1.5), ra=((36, -8), (44, -36)), eyes="happy"),
    marks(["M742 300 q12 8 12 22", "M756 284 q18 12 18 34"], "#fff", 4),
    flowers([(60, 540), (720, 560), (600, 575)])])

# 03 chopping wood, then lunch under the big tree
axe = stroke("M30 -8 L50 -72", BARK, 5) + '<path d="M42 -82 L64 -76 L62 -56 Q52 -62 42 -66Z" fill="#B8BDC8"/>'
svg(3, "Grandpa chops wood, then sits down for lunch", "Paper-cut noon scene: far off on the mountain a small Grandpa swings his axe at a log, with motion marks; in front, Grandpa sits under a big old tree and opens his purple cloth to find three rice balls.", NOON, [
    sun(96, 84, 44),
    f'<path filter="url(#p)" d="M-40 440 Q60 190 250 196 Q420 200 500 440Z" fill="{G3}"/>',
    f'<g filter="url(#p)"><rect x="296" y="168" width="34" height="32" rx="4" fill="{BARK}"/><rect x="301" y="150" width="24" height="18" rx="4" fill="#C98B4A"/></g>'
    '<g fill="#C98B4A"><rect x="340" y="190" width="30" height="12" rx="5"/><rect x="348" y="178" width="30" height="12" rx="5"/></g>',
    person("pa", 230, 146, .8, look=(2.5, 1.5), la=((4, 6), (30, -10)), ra=((36, 2), (36, -24)), extra=axe),
    marks(["M292 62 q30 8 38 44", "M306 44 q40 12 48 56", "M330 140 l12 -8", "M294 136 l-10 -10"], "#fff", 4),
    dashed("M300 232 Q360 330 430 400", CREAM, 4), hill(436, 20, G1),
    f'<path filter="url(#p)" d="M500 0 Q520 300 484 478 H650 Q606 300 624 0Z" fill="{BARK}"/>' + stroke("M540 120 q10 60 -4 120 M590 60 q-8 50 4 90", BARK_D, 5),
    blobs([(440, 10, 100), (600, -10, 120), (750, 60, 110), (800, 190, 70)], LEAF_D), blobs([(520, 50, 54), (690, 40, 60), (780, 150, 40)], LEAF_L, False),
    '<ellipse cx="566" cy="500" rx="210" ry="34" fill="#2F7D4F" opacity=".3"/>',
    person("pa", 566, 380, 1.8, look=(0, 2.5), la=((-32, 18), (-34, 40)), ra=((32, 18), (34, 40)), mouth="open", **CROSS),
    cloth(566, 492, 1.5, 3), flowers([(90, 500), (250, 540), (380, 500), (760, 540)])])

# 04 the rice ball rolls away
hillside, hy = slope(0, 250, 400, 290, 800, 520)
hops = [(292, .4, -30), (392, .6, 10)]
svg(4, "One rice ball rolls down the hill", "Paper-cut scene: one rice ball slips from Grandpa's hands and bounces away down the green hill in big hops toward a tree at the bottom, while Grandpa reaches after it in surprise; two rice balls are still on his cloth.", NOON, [
    sun(600, 90, 44), cloud(380, 70, .8), FAR, hillside,
    f'<path filter="url(#p)" d="M30 0 Q52 150 20 280 H150 Q116 150 126 0Z" fill="{BARK}"/>',
    blobs([(40, 10, 110), (190, -10, 90), (-10, 130, 60)], LEAF_D), blobs([(120, 40, 50), (230, 40, 36)], LEAF_L, False),
    tree(716, 512, .9, 250), tree_front(716, 512, .9), blobs([(716, 262, 74), (784, 300, 50), (650, 296, 50)], LEAF_D), blobs([(736, 250, 36)], LEAF_L, False),
    person("pa", 120, round(hy(120)) - 72, 1.4, look=(2.5, 1.5), la=((-4, 16), (26, 12)), ra=((38, 2), (56, -4)), mouth="open", **CROSS),
    cloth(232, round(hy(232)) + 16, 1.05, 2),
    dashed("M222 232 Q262 190 300 282 Q346 200 400 304 Q470 210 540 372 Q590 330 624 452 Q650 430 676 492", CREAM, 5, "4 14"),
    *[riceball(x, round(hy(x)) - 40, 1.25, r, o, False) for x, o, r in hops],
    marks(["M452 270 q-22 -4 -34 12", "M470 244 q-30 -10 -52 10"], "#fff", 5),
    riceball(520, round(hy(520)) - 78, 1.9, 38),
    flowers([(80, 420), (200, 520), (330, 440), (420, 540), (560, 520)])])

# 05 plop — and a song comes out
G_FLAT = '<path filter="url(#p)" d="M0 410 Q400 380 800 410 V600 H0Z" fill="' + G1 + '"/>'
svg(5, "The rice ball drops into the hole", "Paper-cut scene: the rice ball drops into a hole between the roots of the old tree, and little music notes float up out of the hole on curly swirls while Grandpa cups a hand to his ear.", NOON, [
    cloud(170, 90, .9), FAR, G_FLAT,
    tree(520, 478, 2.3), riceball(520, 512, 1.7, 14, shadow=False), tree_front(520, 478, 2.3),
    blobs([(520, -30, 150), (700, 30, 110), (350, 20, 90)], LEAF_D), blobs([(620, 30, 60), (420, 50, 44)], LEAF_L, False),
    marks(["M492 408 v-22", "M520 398 v-28", "M548 408 v-22"], "#fff", 5),
    stroke("M468 440 Q380 390 430 320 T380 190 q-8 -22 12 -26 M572 440 Q670 380 610 300 T664 160 q10 -20 -10 -26", CREAM, 4),
    note(410, 350, 1.7, -10), note(396, 232, 2.1, 8, "#FFFDF5"), note(640, 330, 1.9, 10, "#FFFDF5"), note(632, 214, 2.3, -8), note(520, 300, 1.5, 4), note(700, 130, 1.5, 12),
    person("pa", 170, 372, 1.6, look=(2.5, 1.5), ra=((36, -14), (31, -34)), la=((-30, 12), (-34, 28)), mouth="open"),
    flowers([(60, 540), (300, 520), (720, 540)])])

# 06 ear to the hole, and a second rice ball
svg(6, "Grandpa listens and drops in another", "Paper-cut scene: Grandpa kneels with his ear to the hole between the tree roots, smiling with his eyes closed, and drops a second rice ball in; music notes drift up and one rice ball waits on his cloth.", NOON, [
    cloud(200, 90, .9), FAR, G_FLAT,
    tree(580, 478, 2), riceball(580, 422, 1.5, -12), tree_front(580, 478, 2),
    blobs([(580, -30, 150), (750, 40, 100), (420, 10, 80)], LEAF_D), blobs([(670, 30, 56)], LEAF_L, False),
    marks(["M556 366 v-20", "M580 358 v-26", "M604 366 v-20"], "#fff", 5),
    stroke("M640 430 Q720 380 680 310 T720 190", CREAM, 4), note(690, 330, 1.7, 10), note(716, 210, 2, -8, "#FFFDF5"), note(640, 250, 1.4, 6),
    cloth(130, 512, 1.2, 1),
    person("pa", 396, 420, 1.7, rot=52, eyes="happy", screen=True,
           ll=((-14, 46), (-52, 50)), rl=((-30, 48), (-66, 54)), la=((-18, 14), (-4, 46)), ra=((40, 14), (66, 6))),
    flowers([(60, 430), (300, 560), (740, 550)])])

# 07 wheee — down the leafy tunnel
tl = [(60, 150, 30, 0), (210, 110, -40, 1), (120, 300, 60, 1), (300, 190, 20, 0), (250, 400, -30, 0), (470, 230, 70, 1), (560, 280, -20, 0),
      (400, 440, 40, 1), (640, 330, 30, 1), (540, 470, -60, 0), (30, 40, 10, 1), (700, 400, -40, 0)]
pile = [(600, 540, 20, 0), (640, 500, -50, 2), (690, 480, 30, 1), (740, 500, 70, 0), (770, 540, -20, 2), (700, 540, 10, 1), (650, 560, 80, 0),
        (560, 575, -30, 1), (740, 575, 40, 2), (610, 585, 60, 2)]
LC = [LEAF_L, "#8CC49A", "#D9773C"]
svg(7, "Grandpa slides down the leafy tunnel", "Paper-cut scene underground: Grandpa slides down a long leafy tunnel like a playground slide, arms in the air and laughing, with leaves flying behind him and a big soft pile of leaves waiting at the bottom.", EARTH, [
    '<g fill="#5B3F2C"><ellipse cx="640" cy="120" rx="46" ry="26"/><ellipse cx="90" cy="500" rx="56" ry="30"/><ellipse cx="330" cy="560" rx="34" ry="18"/></g>',
    stroke("M130 -40 Q170 250 420 330 Q600 390 690 520", "#8A6242", 216), stroke("M130 -40 Q170 250 420 330 Q600 390 690 520", "#A57C55", 176),
    '<circle cx="124" cy="-20" r="92" fill="#8CCBE0"/>',
    stroke("M250 110 q24 10 30 34 M470 220 q-6 24 12 40 M250 372 q22 -6 34 -26", BARK, 6),
    "".join(leaf(a, b, 1.5, r, LC[c]) for a, b, r, c in tl),
    blobs([(620, 575, 70), (720, 550, 84), (800, 580, 64), (540, 610, 50)], "#6DB56B"), "".join(leaf(a, b, 2.2, r, LC[c]) for a, b, r, c in pile),
    marks(["M236 170 q-26 -40 -18 -86", "M296 150 q-24 -40 -10 -84", "M190 230 q-30 -30 -34 -70"], CREAM, 5),
    dashed("M500 372 Q580 400 640 480", CREAM, 5, "4 14"),
    person("pa", 372, 286, 1.55, rot=-16, look=(2, 2), mouth="open", ll=((18, 44), (42, 52)), rl=((22, 50), (48, 62)), **UP),
    leaf(250, 250, 1.7, 30, "#D9773C"), leaf(470, 180, 1.7, -40, LEAF_L), leaf(300, 330, 1.5, 80, "#8CC49A")])

# 08 the mouse village
front = [(392, 512, 1.35, -24, 0), (474, 520, 1.35, -24, 1), (556, 512, 1.35, -24, 2), (638, 520, 1.35, -24, 3), (722, 512, 1.35, -24, 4)]
rear = [(430, 446, 1.05, -22, 3), (506, 440, 1.05, -22, 4), (582, 446, 1.05, -22, 5), (658, 440, 1.05, -22, 0), (736, 446, 1.05, -22, 1)]
svg(8, "The mouse village", "Paper-cut scene underground: a cosy mouse village of tiny houses with lit windows and glowing paper lanterns, where many little mice in kimono bow politely to a smiling Grandpa; the lead mouse wears a red headband.", UNDER, [
    *cave(), '<path d="M300 356 Q560 318 800 350 V470 H300Z" fill="#4E3842"/>',
    mhouse(380, 350, 1.3), mhouse(470, 340, 1.5, "#6A8FD8"), mhouse(570, 336, 1.3, "#7FB77E"), mhouse(662, 340, 1.5), mhouse(756, 346, 1.3, "#B48EDB"),
    lantern_line("M270 70 Q520 190 800 110", [(350, 142, 36), (460, 180, 40), (580, 194, 44), (700, 176, 44)]),
    floor(), mice(rear), person("pa", 150, 398, 1.75, rot=5, look=(2.5, 2.5), ra=((34, 10), (22, 26)), la=((-30, 12), (-18, 28))),
    mice(front), mouse(300, 500, 1.7, -24, band=True)])

# 09 the mochi party
mallet = lambda d, hx, hy, r: stroke(d, "#C98B4A", 3.5) + f'<rect x="{hx - 7}" y="{hy - 12}" width="14" height="24" rx="4" fill="#E0B07A" transform="rotate({r} {hx} {hy})"/>'
dancers = [(86, 470, 1.25, -12, 0), (176, 398, 1.15, 12, 1), (110, 316, 1, -10, 2), (300, 318, 1, 10, 3), (400, 296, 1, -10, 4), (500, 318, 1, 10, 5)]
svg(9, "The mochi party", "Paper-cut scene underground: under glowing lanterns two mice pound sticky rice in a wooden mortar with big mallets while other mice dance with their arms up, and Grandpa sits and claps along, laughing.", UNDER, [
    *cave(), lantern_line("M0 100 Q400 210 800 90", [(120, 142, 30), (270, 176, 36), (530, 174, 36), (680, 138, 30)]),
    floor(), mice(dancers, "md"), note(210, 290, 1.5, -10), note(580, 270, 1.7, 10, "#FFFDF5"), note(40, 380, 1.3, 8, "#FFFDF5"),
    f'<g filter="url(#p)"><path d="M344 428 H456 L440 520 Q400 530 360 520Z" fill="#A56C34"/><ellipse cx="400" cy="428" rx="56" ry="14" fill="#C98B4A"/></g>'
    '<path d="M362 428 Q372 396 400 400 Q430 396 438 428 Q400 440 362 428Z" fill="#FFFDF5"/>' + stroke("M352 462 Q400 474 448 462", WOOD_D, 4),
    mouse(290, 462, 2, band=True, arms="M-9 0 L13 -8 M11 2 L17 -9", extra=mallet("M9 -3 L32 -46", 35, -52, 62)),
    mouse(510, 462, 2, col=KIMONO[1], flip=True, arms="M-9 2 L13 2 M11 4 L18 3", extra=mallet("M9 3 L50 -12", 54, -14, 0)),
    marks(["M330 330 q34 -10 56 14", "M316 306 q44 -18 78 12", "M418 372 l10 -14", "M382 372 l-10 -14"], CREAM, 4),
    person("pa", 668, 392, 1.7, eyes="happy", mouth="open", la=((-27, 16), (-6, 4)), ra=((27, 16), (6, 4)), **CROSS),
    marks(["M650 350 l-14 -12", "M686 350 l14 -12", "M668 344 v-16"], CREAM, 4)])

# 10 big box or small box?
svg(10, "A big box and a small box", "Paper-cut scene underground: the lead mouse in the red headband offers two wrapped presents, one very big and one small, and Grandpa smiles and points at the small one while other mice peek out.", UNDER, [
    *cave(), lantern_line("M0 80 Q400 170 800 80", [(150, 126, 30), (400, 152, 30), (650, 126, 30)]), floor(),
    mice([(214, 318, 1.4, -8, 1), (330, 322, 1.4, 8, 3)]),
    gift(270, 500, 210, 176, "#D9577A", "#B03F60", CREAM), small_box(462, 508),
    mouse(96, 492, 2.1, band=True, arms="M-11 0 q-6 6 -4 11 M11 0 L25 -5"),
    person("pa", 650, 398, 1.8, look=(-2.5, 2), la=((-36, 12), (-60, 24)), ra=((30, 16), (26, 38)), **CROSS),
    dashed("M528 446 L496 462", CREAM, 4, "2 9")])

# 11 back up the tunnel at sunset
box_back = small_box(-27, 34, 40, False) + stroke("M-16 -8 L12 34", CLOTH, 5)
stick = stroke("M17 -9 L26 -34", "#C98B4A", 2.5)
wavers = [(130, 520, 1.6, -8, LEAD, True), (236, 478, 1.5, 6, KIMONO[1], False), (330, 536, 1.5, -4, KIMONO[3], False)]
svg(11, "Grandpa climbs home at sunset", "Paper-cut scene: under an orange sunset sky Grandpa climbs back up the leafy tunnel toward the hole by the tree with the small box tied on his back, while the mice wave their glowing lanterns goodbye below.", SUNSET, [
    '<circle cx="190" cy="176" r="74" fill="#FFE9C4"/>', cloud(420, 70, .8, "#FBD0A8"),
    f'<path filter="url(#p)" d="M640 0 Q650 120 630 200 H730 Q704 120 712 0Z" fill="{BARK_D}"/>', blobs([(680, -20, 110), (800, 60, 80), (560, 0, 60)], "#3F6B4A"),
    '<path filter="url(#p)" d="M0 186 Q400 168 800 190 V600 H0Z" fill="#4A3020"/><path d="M0 186 Q400 168 800 190 V206 Q400 184 0 202Z" fill="#6E9A5A"/>',
    stroke("M566 196 Q540 330 340 420 Q200 480 110 620", "#8A6242", 190), stroke("M566 196 Q540 330 340 420 Q200 480 110 620", "#A57C55", 150),
    '<ellipse cx="566" cy="192" rx="76" ry="20" fill="#FBD9A8"/>',
    "".join(leaf(a, b, 1.5, r, LC[c]) for a, b, r, c in [(600, 300, 30, 0), (450, 420, -40, 1), (380, 330, 60, 0), (250, 400, 20, 1), (520, 240, -30, 2), (60, 560, 40, 0), (400, 480, 10, 2)]),
    person("pa", 486, 318, 1.45, rot=26, look=(1, -2.5), back=box_back, la=((-34, -10), (-30, -40)), ra=((36, -6), (40, -38)), ll=((-20, 48), (-12, 64)), rl=((18, 42), (26, 56))),
    marks(["M560 400 q10 -20 0 -40", "M400 300 q-4 -22 10 -38"], CREAM, 4),
    *[lantern(round(x + 26 * s), round(y - 46 * s), 1.2) for x, y, s, r, c, b in wavers],
    *[mouse(x, y, s, 0, c, band=b, arms="M-11 0 q-6 6 -4 11 M11 0 L17 -9", extra=stick) for x, y, s, r, c, b in wavers]])

# 12 the small box sparkles
treasure = [(372, 430, 1.3, -20), (404, 424, 1.4, 10), (432, 432, 1.2, 30), (388, 444, 1.2, 0), (420, 446, 1.2, -10),
            (330, 360, 1.2, -30), (476, 340, 1.3, 24), (400, 290, 1.4, 0), (300, 250, 1, 40), (510, 240, 1.1, -30), (430, 190, 1, 16)]
svg(12, "The small box sparkles", "Paper-cut evening scene at home: Grandma and Grandpa open the small box together and golden light spills out, full of shiny gold coins, gems and sparkles; they throw up their hands in happy surprise.", HOME, [
    stroke("M130 0 V430 M270 0 V430 M410 0 V430 M550 0 V430 M690 0 V430", "#A57C55", 3),
    '<g filter="url(#p)"><rect x="52" y="50" width="150" height="120" rx="8" fill="#7A5236"/></g><rect x="62" y="60" width="130" height="100" rx="4" fill="#3A3E88"/>'
    '<circle cx="150" cy="100" r="20" fill="#FFF6E6"/><circle cx="92" cy="86" r="2.5" fill="#fff"/><circle cx="110" cy="134" r="2" fill="#fff"/>',
    '<path filter="url(#p)" d="M0 430 H800 V600 H0Z" fill="#C3C58F"/>' + stroke("M0 500 H800 M260 430 V500 M560 430 V500 M120 500 V600 M420 500 V600 M700 500 V600", "#A3A870", 3),
    f'<path d="M352 440 L230 110 Q400 40 570 110 L448 440Z" fill="{GOLD}" opacity=".22"/>', glow(400, 400, 170),
    person("ma", 180, 404, 1.8, look=(2.5, 1.5), mouth="open", sit=True, **UP),
    person("pa", 624, 400, 1.8, look=(-2.5, 1.5), mouth="open", **UP, **CROSS),
    f'<g filter="url(#p)"><rect x="340" y="436" width="120" height="76" rx="6" fill="{WOOD}"/><ellipse cx="400" cy="440" rx="56" ry="13" fill="{GOLD_L}"/>'
    f'<g transform="rotate(-24 520 500)"><rect x="466" y="486" width="128" height="26" rx="6" fill="{WOOD_D}"/><rect x="524" y="486" width="8" height="26" fill="{RED}"/></g></g>'
    + stroke("M400 452 V512", RED, 5),
    "".join(coin(a, b, s, r) for a, b, s, r in treasure),
    '<path d="M352 300 l12 -14 l12 14 l-12 16z" fill="#5FB3B3"/><path d="M452 262 l11 -13 l11 13 l-11 15z" fill="#F2859A"/><path d="M356 196 l9 -11 l9 11 l-9 13z" fill="#B48EDB"/>',
    star(280, 320, 1.6), star(530, 310, 1.4), star(400, 130, 1.8), star(330, 150, 1), star(480, 130, 1.1), star(250, 180, .9), star(560, 180, .9), star(440, 370, 1)])

# 13 one more for the mice
G_MORN = '<path filter="url(#p)" d="M0 420 Q400 390 800 420 V600 H0Z" fill="' + G1 + '"/>'
svg(13, "One more rice ball for the mice", "Paper-cut morning scene: Grandpa and Grandma together roll a rice ball into the hole between the tree roots, and happy music notes swirl back up out of it while a little mouse peeks from behind a root.", MORNING, [
    sun(120, 100, 48), cloud(300, 70, .8), hill(350, 40, G2, False), G_MORN,
    tree(400, 492, 2), mice([(446, 512, 1.5, 8, 0)], "md"), riceball(392, 436, 1.6, -14), tree_front(400, 492, 2),
    blobs([(400, -40, 150), (560, 20, 100), (250, 20, 100)], LEAF_D), blobs([(480, 30, 56), (320, 50, 44)], LEAF_L, False),
    marks(["M376 388 v-20", "M400 380 v-26", "M424 388 v-20"], "#fff", 5),
    stroke("M352 440 Q280 380 330 300 T290 170 q-8 -22 12 -26 M448 440 Q530 380 476 300 T520 160 q10 -20 -10 -26", CREAM, 4),
    note(316, 330, 1.8, -10), note(300, 210, 2.1, 8, "#FFFDF5"), note(498, 330, 1.8, 10, "#FFFDF5"), note(506, 200, 2.2, -8), note(400, 290, 1.5, 4), note(580, 130, 1.4, 12),
    person("pa", 196, 410, 1.75, look=(2.5, 1.5), eyes="happy", ra=((38, 2), (62, 8)), la=((-30, 14), (-26, 34)), **CROSS),
    person("ma", 622, 392, 1.75, look=(-2.5, 1.5), eyes="happy", la=((-38, 4), (-62, 10)), ra=((30, 12), (26, 30))),
    flowers([(60, 540), (300, 560), (520, 566), (740, 550)])])
