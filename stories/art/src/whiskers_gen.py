#!/usr/bin/env python3
"""Generates the 13 Lion's Whiskers flip-book SVGs from shared paper-cut character parts.

Usage: python3 whiskers_gen.py <output-dir>
Scale rule: every figure is drawn at K = 0.8 with (x, y) at the feet, on the same ground band,
so Bizunesh (about 235 px tall), Abebe (about 150 px, up to her chest) and the lion keep the same
sizes on every page. Distance is shown by the gap between Bizunesh and the lion, never by shrinking
anyone. The lion is calm and curious on every page.
Faces are round with dot eyes, like every other KaiSTEM book: no caricature.
Abebe never smiles at Bizunesh or holds her hand before the last pages.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SKIN, SKIN_D, CHEEK, LIP = "#8A5634", "#6F4228", "#C0504A", "#4A2218"
HAIR, HAIR_L, GREY = "#231A16", "#3E3029", "#EDEAE4"
WHITE, WHITE_D = "#FBF7EE", "#E4D9C6"
TEAL, GOLD, RED = "#2F8F86", "#E2A92B", "#C8463A"
LION, LION_D, LION_L, MANE, MANE_D = "#D9A55C", "#B98340", "#F1D3A0", "#7A4E2C", "#563621"
WOOD, WOOD_D = "#9C6A3E", "#6E4628"
MUD, MUD_D, THATCH, THATCH_D = "#C98E5A", "#A9703F", "#D9B464", "#B08C40"
GRASS, GRASS_D, GRASS_L = "#B9B25A", "#8F8A3E", "#D5CB7A"
GREEN, GREEN_D = "#7FA54A", "#5C8236"
LEAF, LEAF_D = "#5E8E3E", "#44702C"
MESA, MESA_D = "#9AAFC7", "#7F95B0"
ROCK, ROCK_D = "#B7A898", "#968676"
CLAY, CLAY_D, MEAT, MEAT_L = "#B86B42", "#8E4E2D", "#B5523F", "#E8A190"
BREAD, BREAD_D = "#E4B877", "#D9A55C"
DAY = [(0, "#7CC6E6"), (1, "#EAF5F8")]
MORNING = [(0, "#8CCDEA"), (.7, "#F6EED8"), (1, "#FBE9C8")]
GOLDEN = [(0, "#8FCFEA"), (.6, "#FDE7C0"), (1, "#FCD3A0")]
K, GROUND = .8, 530

# Body shapes. y values are above the feet (negative = up). arm = how far arm poses reach.
ADULT = dict(head=-262, r=32, sy=-226, sx=34, hem=-4, hx=62, arm=1.7, sleeve=20, hand=10)
SEAT = dict(head=-190, r=32, sy=-154, sx=34, hem=0, hx=96, arm=1.7, sleeve=20, hand=10)
CHILD = dict(head=-158, r=32, sy=-124, sx=26, hem=-58, hx=36, arm=1, sleeve=15, hand=8)
# Arm poses in child units, (ctrl dx, ctrl dy, hand dx, hand dy) from the shoulder, dx OUTWARD.
ARMS = {
    "down": ((12, 26, 10, 54), (12, 26, 10, 54)),
    "hold": ((18, 30, -1, 46), (18, 30, -1, 46)),
    "lap": ((14, 30, -6, 50), (14, 30, -6, 50)),
    "palm": ((12, 26, 10, 54), (34, 6, 30, 24)),
    "open": ((26, 14, 46, 30), (26, 14, 46, 30)),
    "up": ((12, 26, 4, 50), (26, -18, 30, -52)),
    "behind": ((8, 20, 2, 40), (8, 20, 2, 40)),
    "staff": ((12, 26, 10, 54), (20, 20, 26, 30)),
    "give": ((34, 6, 30, 24), (20, 20, 26, 30)),        # left palm held out, staff in the right hand
}


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, inner: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- faces and people
def face(r: float, mood: str, brow: str = HAIR) -> str:
    ex, my = r * .36, r * .44
    out = ""
    if mood in ("sad", "shy"):
        out += stroke(f"M{-ex - 7} -11 L{-ex + 5} -15 M{ex + 7} -11 L{ex - 5} -15", brow, 2.6)
    else:
        out += stroke(f"M{-ex - 6} -14 q6 -4 12 0 M{ex - 6} -14 q6 -4 12 0", brow, 2.6)
    for sx in (-1, 1):
        if mood in ("shy", "sad"):  # eyes looking down and away
            out += f'<circle cx="{sx * ex - 3}" cy="3" r="4.6" fill="{INK}"/>'
        else:
            out += f'<circle cx="{sx * ex}" cy="0" r="4.8" fill="{INK}"/><circle cx="{sx * ex + 1.6}" cy="-1.6" r="1.6" fill="#fff"/>'
    out += "".join(f'<circle cx="{sx * r * .62}" cy="{r * .3}" r="7" fill="{CHEEK}" opacity=".35"/>' for sx in (-1, 1))
    if mood == "smile":
        out += stroke(f"M-8 {my - 2} q8 8 16 0", LIP, 2.6)
    elif mood == "happy":
        out += f'<path d="M-11 {my - 3} Q0 {my - 1} 11 {my - 3} Q9 {my + 10} 0 {my + 10} Q-9 {my + 10} -11 {my - 3}Z" fill="{LIP}"/>'
    elif mood in ("sad", "shy"):
        out += stroke(f"M-7 {my + 4} q7 -6 14 0", LIP, 2.6)
    elif mood == "small":  # a tiny, shy smile
        out += stroke(f"M-5 {my} q5 4 10 0", LIP, 2.4)
    elif mood == "oh":
        out += f'<ellipse cy="{my + 2}" rx="5" ry="6.5" fill="{LIP}"/>'
    return out


def arm_paths(B: dict, pose) -> list:
    left, right = ARMS[pose] if isinstance(pose, str) else pose
    a, sy, sx = B["arm"], B["sy"] + 6, B["sx"]
    out = []
    for sgn, (cx, cy, hx, hy) in ((-1, left), (1, right)):
        x0 = sgn * sx
        out.append((f"M{x0} {sy} Q{x0 + sgn * cx * a:.0f} {sy + cy * a:.0f} {x0 + sgn * hx * a:.0f} {sy + hy * a:.0f}",
                    (x0 + sgn * hx * a, sy + hy * a)))
    return out


def hands(B: dict, pose) -> tuple:
    (_, lh), (_, rh) = arm_paths(B, pose)
    return lh, rh


def tibeb(x: float, y: float, w: float, h: float) -> str:
    """A woven tibeb border band: teal with a gold zigzag and a red edge."""
    n = max(2, int(w / 12))
    zig = f"M{x + 2:.1f} {y + h * .7:.1f}" + "".join(
        f" L{x + 2 + (i + .5) * (w - 4) / n:.1f} {y + h * .3:.1f} L{x + 2 + (i + 1) * (w - 4) / n:.1f} {y + h * .7:.1f}" for i in range(n))
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="2" fill="{TEAL}"/>'
            + stroke(zig, GOLD, 2.4) + f'<rect x="{x:.1f}" y="{y + h - 3:.1f}" width="{w:.1f}" height="3" fill="{RED}"/>')


def head(r: float, mood: str, hair: str, beard: str = "") -> str:
    out = f'<circle cx="{-r}" cy="4" r="7" fill="{SKIN_D}"/><circle cx="{r}" cy="4" r="7" fill="{SKIN_D}"/>'
    out += f'<circle r="{r}" fill="{SKIN}"/>'
    if hair == "braids":  # shuruba: neat braided rows running back over the head
        out += (f'<path d="M{-r - 2} -2 Q{-r - 4} {-r - 8} 0 {-r - 6} Q{r + 4} {-r - 8} {r + 2} -2 '
                f'Q{r - 6} {-r * .5} 0 {-r * .62} Q{-r + 6} {-r * .5} {-r - 2} -2Z" fill="{HAIR}"/>')
        out += stroke(" ".join(f"M{d} {-r * .6 + abs(d) * .12:.0f} Q{d * 1.2:.0f} {-r - 2} {d * .5:.0f} {-r - 4}" for d in (-18, -6, 6, 18)), HAIR_L, 2.2)
    elif hair == "short":
        out += (f'<path d="M{-r - 1} -4 Q{-r - 2} {-r - 6} 0 {-r - 5} Q{r + 2} {-r - 6} {r + 1} -4 '
                f'Q{r - 6} {-r * .55} 0 {-r * .62} Q{-r + 6} {-r * .55} {-r - 1} -4Z" fill="{HAIR}"/>')
        out += "".join(f'<circle cx="{a}" cy="{b}" r="7" fill="{HAIR}"/>' for a, b in [(-24, -20), (-14, -30), (0, -34), (14, -30), (24, -20)])
    elif hair == "elder":  # bald on top, a soft grey ring of hair
        out += stroke(f"M{-r - 1} 0 Q{-r} {-r * .7} {-r * .5} {-r * .82} M{r + 1} 0 Q{r} {-r * .7} {r * .5} {-r * .82}", GREY, 9)
    out += face(r, mood, GREY if hair == "elder" else HAIR)
    if beard == "white":
        out += (f'<path d="M-22 {r * .42} Q-24 {r * 1.5} 0 {r * 2} Q24 {r * 1.5} 22 {r * .42} Q12 {r * .9} 0 {r * .62} Q-12 {r * .9} -22 {r * .42}Z" fill="{GREY}"/>'
                + stroke(f"M-12 {r * .4} q12 -6 24 0", GREY, 5))
    elif beard == "mustache":
        out += stroke(f"M-12 {r * .3} q6 -4 12 0 q6 -4 12 0", HAIR, 4.4)
    return out


def bizunesh(x: float, y: float = GROUND, arms="down", mood: str = "smile", sit: bool = False, held: str = "") -> str:
    """Bizunesh facing us: a white habesha kemis with a woven tibeb border, a white netela shawl,
    braided hair. (x, y) is her feet. sit=True: sitting on the ground, skirt spread around her."""
    B = SEAT if sit else ADULT
    r, sy, sx, hem, hx = B["r"], B["sy"], B["sx"], B["hem"], B["hx"]
    out = (f'<ellipse cx="{-r + 4}" cy="{B["head"] + 34}" rx="9" ry="22" fill="{HAIR}"/>'
           f'<ellipse cx="{r - 4}" cy="{B["head"] + 34}" rx="9" ry="22" fill="{HAIR}"/>')
    if sit:
        out += (f'<path d="M{-sx} {sy} Q{-sx - 6} -70 {-hx} -6 Q0 8 {hx} -6 Q{sx + 6} -70 {sx} {sy} Q0 {sy - 8} {-sx} {sy}Z" fill="{WHITE}"/>'
                + f'<path d="M{-hx + 10} -8 Q{-sx - 4} -60 {-sx} {sy} L{-sx * .4} {sy} L{-hx * .4} -2Z" fill="{WHITE_D}" opacity=".5"/>'
                + tibeb(-hx + 6, -22, 2 * hx - 12, 16))
    else:
        out += f'<ellipse cx="-14" cy="-3" rx="11" ry="5" fill="{SKIN_D}"/><ellipse cx="14" cy="-3" rx="11" ry="5" fill="{SKIN_D}"/>'
        mid = (sy + hem) / 2
        out += (f'<path d="M{-sx} {sy} Q{-hx + 6} {mid} {-hx} {hem} Q0 {hem + 6} {hx} {hem} Q{hx - 6} {mid} {sx} {sy} '
                f'Q0 {sy - 8} {-sx} {sy}Z" fill="{WHITE}"/>')
        out += f'<path d="M{-hx * .2} {hem} L{-hx * .9} {hem} Q{-hx + 8} {mid} {-sx} {sy} L{-sx * .3} {sy}Z" fill="{WHITE_D}" opacity=".5"/>'
        out += tibeb(-hx + 2, hem - 24, 2 * hx - 4, 18)
        out += f'<rect x="-8" y="{sy + 40}" width="16" height="{hem - 24 - sy - 40}" fill="{TEAL}"/>'
        out += "".join(f'<path d="M0 {yy - 6} l5 6 l-5 6 l-5 -6Z" fill="{GOLD}"/>' for yy in range(int(sy + 52), int(hem - 30), 22))
    out += f'<rect x="-8" y="{B["head"] + r - 6}" width="16" height="16" fill="{SKIN_D}"/>'
    # the netela shawl over the shoulders, with a woven border along its edge
    out += (f'<path d="M{-sx - 10} {sy + 4} Q{-sx - 14} {sy + 50} {-sx - 6} {sy + 64} Q0 {sy + 38} {sx + 6} {sy + 64} '
            f'Q{sx + 14} {sy + 50} {sx + 10} {sy + 4} Q0 {sy - 12} {-sx - 10} {sy + 4}Z" fill="#FFFDF8"/>')
    out += stroke(f"M{-sx - 6} {sy + 60} Q0 {sy + 34} {sx + 6} {sy + 60}", TEAL, 5) + stroke(f"M{-sx - 4} {sy + 55} Q0 {sy + 29} {sx + 4} {sy + 55}", GOLD, 2)
    (la, lh), (ra, rh) = arm_paths(B, arms)
    out += stroke(la, WHITE, B["sleeve"]) + stroke(ra, WHITE, B["sleeve"])
    out += held
    out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{B["hand"]}" fill="{SKIN}"/>' for a, b in (lh, rh))
    out += f'<g transform="translate(0 {B["head"]})">{head(r, mood, "braids")}</g>'
    return group(x, y, K, out)


def abebe(x: float, y: float = GROUND, arms="down", mood: str = "shy") -> str:
    """Abebe, a little boy facing us: sky-blue shirt, brown shorts, short curly hair."""
    B = CHILD
    r, sy, sx, hem, hx = B["r"], B["sy"], B["sx"], B["hem"], B["hx"]
    out = stroke("M-11 -46 L-12 -8 M11 -46 L12 -8", SKIN, 13)
    out += f'<ellipse cx="-14" cy="-4" rx="11" ry="5" fill="{SKIN_D}"/><ellipse cx="14" cy="-4" rx="11" ry="5" fill="{SKIN_D}"/>'
    out += '<path d="M-30 -74 L-32 -40 L-4 -40 L0 -50 L4 -40 L32 -40 L30 -74Z" fill="#6B4E36"/>'
    out += (f'<path d="M{-sx} {sy} Q{-hx} {(sy + hem) / 2} {-hx + 2} {hem} Q0 {hem + 6} {hx - 2} {hem} Q{hx} {(sy + hem) / 2} {sx} {sy} '
            f'Q0 {sy - 8} {-sx} {sy}Z" fill="#5FA8D3"/>')
    out += stroke(f"M-8 {sy - 2} L0 {sy + 12} L8 {sy - 2}", "#3F86B5", 3)
    (la, lh), (ra, rh) = arm_paths(B, arms)
    out += stroke(la, "#5FA8D3", B["sleeve"]) + stroke(ra, "#5FA8D3", B["sleeve"])
    out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{B["hand"]}" fill="{SKIN}"/>' for a, b in (lh, rh))
    out += f'<rect x="-7" y="{B["head"] + r - 6}" width="14" height="10" fill="{SKIN_D}"/>'
    out += f'<g transform="translate(0 {B["head"]})">{head(r, mood, "short")}</g>'
    return group(x, y, K, out)


def father(x: float, y: float = GROUND, arms="down", mood: str = "smile") -> str:
    """Abebe's father: a white knee-length shirt over white trousers, a gabi shawl with a teal stripe."""
    B = ADULT
    r, sy, sx = B["r"], B["sy"], B["sx"]
    hem, hx = -96, 54
    out = stroke("M-14 -100 L-15 -8 M14 -100 L15 -8", "#E2D8C4", 22)
    out += f'<ellipse cx="-17" cy="-4" rx="13" ry="6" fill="{WOOD_D}"/><ellipse cx="17" cy="-4" rx="13" ry="6" fill="{WOOD_D}"/>'
    out += (f'<path d="M{-sx} {sy} Q{-hx} {(sy + hem) / 2} {-hx} {hem} Q0 {hem + 6} {hx} {hem} Q{hx} {(sy + hem) / 2} {sx} {sy} '
            f'Q0 {sy - 8} {-sx} {sy}Z" fill="{WHITE}"/>')
    out += f'<path d="M-6 {sy - 2} L0 {sy + 34} L6 {sy - 2}" fill="{TEAL}"/>'
    # gabi over the left shoulder, crossing the chest
    out += f'<path d="M{-sx - 8} {sy + 2} L{sx - 6} {sy - 6} L{hx - 2} {sy + 92} L{hx - 30} {sy + 104} Z" fill="#F3ECDF"/>'
    out += stroke(f"M{-sx - 4} {sy + 14} L{hx - 18} {sy + 100}", TEAL, 4)
    (la, lh), (ra, rh) = arm_paths(B, arms)
    out += stroke(la, WHITE, B["sleeve"]) + stroke(ra, WHITE, B["sleeve"])
    out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{B["hand"]}" fill="{SKIN}"/>' for a, b in (lh, rh))
    out += f'<rect x="-8" y="{B["head"] + r - 6}" width="16" height="12" fill="{SKIN_D}"/>'
    out += f'<g transform="translate(0 {B["head"]})">{head(r, mood, "short", "mustache")}</g>'
    return group(x, y, K, out)


def elder(x: float, y: float = GROUND, arms="staff", mood: str = "smile", held: str = "") -> str:
    """The wise old man: a long white robe and gabi, a white beard, a tall wooden walking stick."""
    B = ADULT
    r, sy, sx, hem, hx = B["r"], B["sy"], B["sx"], -6, 58
    _, rh = hands(B, arms)
    out = f'<ellipse cx="-14" cy="-3" rx="11" ry="5" fill="{SKIN_D}"/><ellipse cx="14" cy="-3" rx="11" ry="5" fill="{SKIN_D}"/>'
    out += (f'<path d="M{-sx} {sy} Q{-hx} {(sy + hem) / 2} {-hx} {hem} Q0 {hem + 6} {hx} {hem} Q{hx} {(sy + hem) / 2} {sx} {sy} '
            f'Q0 {sy - 8} {-sx} {sy}Z" fill="#F7F3EA"/>')
    out += (f'<path d="M{-sx - 12} {sy + 4} Q{-hx - 6} {sy + 110} {-hx + 4} {sy + 150} L{hx - 4} {sy + 150} '
            f'Q{hx + 6} {sy + 110} {sx + 12} {sy + 4} Q0 {sy - 14} {-sx - 12} {sy + 4}Z" fill="#FFFDF8"/>')
    out += stroke(f"M{-hx + 6} {sy + 146} H{hx - 6}", TEAL, 5) + stroke(f"M{-hx + 6} {sy + 140} H{hx - 6}", GOLD, 2)
    out += stroke(f"M{-sx * .4} {sy + 6} Q-2 {sy + 80} {-hx * .3} {sy + 148}", WHITE_D, 3)
    staff_x = rh[0]
    out += stroke(f"M{staff_x:.0f} {B['head'] - 40} L{staff_x + 4:.0f} -2", WOOD_D, 9) + stroke(f"M{staff_x - 2:.0f} {B['head'] - 38} L{staff_x + 2:.0f} -6", WOOD, 4)
    (la, lh), (ra, rh) = arm_paths(B, arms)
    out += stroke(la, "#FFFDF8", B["sleeve"]) + stroke(ra, "#FFFDF8", B["sleeve"])
    out += held
    out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{B["hand"]}" fill="{SKIN}"/>' for a, b in (lh, rh))
    out += f'<rect x="-8" y="{B["head"] + r - 6}" width="16" height="12" fill="{SKIN_D}"/>'
    out += f'<g transform="translate(0 {B["head"]})">{head(r, mood, "elder", "white")}</g>'
    return group(x, y, K, out)


# ---------------------------------------------------------------- the lion
def lion_head(mood: str) -> str:
    """A front-facing lion head: a big dark mane, tan face, cream muzzle and long pale whiskers."""
    pts = [(1, 0), (.87, .5), (.5, .87), (0, 1), (-.5, .87), (-.87, .5), (-1, 0), (-.87, -.5), (-.5, -.87), (0, -1), (.5, -.87), (.87, -.5)]
    out = "".join(f'<circle cx="{62 * c:.1f}" cy="{62 * s:.1f}" r="20" fill="{MANE}"/>' for c, s in pts)
    out += f'<circle r="64" fill="{MANE}"/><circle r="52" fill="{MANE_D}" opacity=".45"/>'
    out += f'<circle cx="-30" cy="-34" r="12" fill="{LION}"/><circle cx="30" cy="-34" r="12" fill="{LION}"/>'
    out += f'<circle cx="-30" cy="-34" r="6" fill="{LION_D}"/><circle cx="30" cy="-34" r="6" fill="{LION_D}"/>'
    out += f'<ellipse cy="2" rx="40" ry="42" fill="{LION}"/>'
    if mood == "calm":  # softly closed, contented eyes
        out += stroke("M-22 -6 q7 5 14 0 M8 -6 q7 5 14 0", INK, 3)
    else:  # curious: round eyes looking toward the left (toward Bizunesh)
        out += "".join(f'<circle cx="{sx * 15}" cy="-6" r="7" fill="#F7E7B0"/><circle cx="{sx * 15 - 2}" cy="-6" r="4" fill="{INK}"/>' for sx in (-1, 1))
        out += stroke("M-23 -18 q8 -4 15 0 M8 -18 q8 -4 15 0", LION_D, 3)
    out += f'<ellipse cx="-10" cy="20" rx="13" ry="10" fill="{LION_L}"/><ellipse cx="10" cy="20" rx="13" ry="10" fill="{LION_L}"/>'
    out += f'<ellipse cy="31" rx="10" ry="8" fill="{LION_L}"/>'
    out += '<path d="M-9 7 L9 7 L0 17Z" fill="#8A4A3A"/>'
    out += stroke("M0 17 v6 M0 23 q-6 5 -10 2 M0 23 q6 5 10 2", "#6A3A2A", 2.4)
    out += "".join(f'<circle cx="{sx * a}" cy="{b}" r="1.6" fill="{LION_D}"/>' for sx in (-1, 1) for a, b in [(8, 18), (14, 22), (10, 24)])
    out += stroke("M-16 17 L-58 8 M-16 21 L-60 22 M-16 25 L-56 36 M16 17 L58 8 M16 21 L60 22 M16 25 L56 36", "#FFF6E6", 2.4)
    return out


def dish_svg(x: float, y: float, s: float = 1) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-14 -24 q8 -14 26 -8 q12 6 2 14 q-14 6 -28 -6Z" fill="{MEAT}"/>'
            + stroke("M-6 -24 q8 -4 14 2", MEAT_L, 3)
            + f'<path d="M-34 -18 H34 Q30 0 0 0 Q-30 0 -34 -18Z" fill="{CLAY}"/><rect x="-36" y="-21" width="72" height="6" rx="3" fill="{CLAY_D}"/></g>')


def lion(x: float, y: float = GROUND, pose: str = "stand", mood: str = "curious", dish: bool = False) -> str:
    """The lion in side view facing left, with a front-facing head. (x, y) is the paws.
    pose: lie (resting, head up) / stand / eat (head lowered in front of the body to a dish)."""
    out = ""
    if pose == "lie":
        out += stroke("M120 -38 Q190 -30 214 -10", LION_D, 11) + f'<ellipse cx="220" cy="-10" rx="14" ry="10" fill="{MANE}"/>'
        out += f'<ellipse cx="20" cy="-48" rx="128" ry="46" fill="{LION}"/>'
        out += f'<ellipse cx="96" cy="-46" rx="50" ry="40" fill="{LION_D}" opacity=".45"/>'
        out += f'<ellipse cx="20" cy="-20" rx="100" ry="16" fill="{LION_L}" opacity=".6"/>'
        out += f'<rect x="-178" y="-24" width="100" height="22" rx="11" fill="{LION}"/><ellipse cx="-176" cy="-11" rx="18" ry="12" fill="{LION_L}"/>'
        hx, hy = -100, -104
    else:
        out += stroke("M134 -130 Q190 -120 196 -70 Q198 -36 222 -44", LION_D, 11) + f'<ellipse cx="226" cy="-46" rx="13" ry="15" fill="{MANE}"/>'
        for lx, c in [(-70, LION_D), (90, LION_D), (-40, LION), (120, LION)]:
            out += f'<rect x="{lx - 15}" y="-120" width="30" height="114" rx="13" fill="{c}"/><ellipse cx="{lx - 4}" cy="-6" rx="20" ry="9" fill="{LION_L}"/>'
        out += f'<ellipse cx="25" cy="-130" rx="125" ry="50" fill="{LION}"/>'
        out += f'<ellipse cx="112" cy="-128" rx="44" ry="42" fill="{LION_D}" opacity=".4"/>'
        out += f'<ellipse cx="25" cy="-98" rx="96" ry="14" fill="{LION_L}" opacity=".6"/>'
        hx, hy = (-140, -98) if pose == "eat" else (-108, -160)
    out += f'<g transform="translate({hx} {hy})">{lion_head(mood)}</g>'
    if dish:  # a clay dish of meat on the ground, right under the eating lion's mouth
        out += dish_svg(hx, -2, 1.25)
    return group(x, y, K, out)


def dish(x: float, y: float = GROUND) -> str:
    return group(x, y, K, dish_svg(0, 0, 1.25))


def basket(cx: float, cy: float, fill: str = "") -> str:
    """A woven basket carried at the tummy (drawn in the carrier's own units). fill: meat / bread / ''."""
    top = ""
    if fill == "meat":
        top = f'<path d="M{cx - 18} {cy - 18} q10 -16 30 -8 q12 6 0 12Z" fill="{MEAT}"/>'
    elif fill == "bread":
        top = (f'<ellipse cx="{cx - 12}" cy="{cy - 20}" rx="22" ry="10" fill="{BREAD}"/>'
               f'<ellipse cx="{cx + 16}" cy="{cy - 18}" rx="20" ry="9" fill="{BREAD_D}"/>')
    return (top + f'<path d="M{cx - 40} {cy - 16} H{cx + 40} L{cx + 32} {cy + 28} Q{cx} {cy + 36} {cx - 32} {cy + 28}Z" fill="{THATCH}"/>'
            + stroke(f"M{cx - 36} {cy - 2} H{cx + 36} M{cx - 34} {cy + 12} H{cx + 34}", THATCH_D, 2.4)
            + stroke(f"M{cx - 30} {cy - 14} l-2 40 M{cx} {cy - 14} v46 M{cx + 30} {cy - 14} l2 40", RED, 2)
            + f'<rect x="{cx - 44}" y="{cy - 20}" width="88" height="7" rx="3" fill="{THATCH_D}"/>')


def whiskers_held(x: float, y: float) -> str:
    """Three long whiskers pinched in a hand at (x, y), dark-edged so they read on the sky."""
    d = f"M{x} {y} L{x - 20} {y - 72} M{x} {y} L{x + 2} {y - 78} M{x} {y} L{x + 24} {y - 70}"
    return stroke(d, MANE_D, 6) + stroke(d, "#FFF6E6", 3)


# ---------------------------------------------------------------- scenery
def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def ambas(base: float = 380) -> str:
    """Far flat-topped highland mountains (ambas)."""
    return (f'<path d="M-20 {base} L40 {base - 70} L150 {base - 76} L190 {base - 30} L260 {base - 40} L300 {base - 120} '
            f'L430 {base - 126} L470 {base - 50} L560 {base - 60} L600 {base - 96} L700 {base - 100} L740 {base - 40} L820 {base - 50} V{base}Z" fill="{MESA}"/>'
            f'<path d="M300 {base - 120} L430 {base - 126} L436 {base - 112} L306 {base - 106}Z M40 {base - 70} L150 {base - 76} L154 {base - 64} L46 {base - 60}Z '
            f'M600 {base - 96} L700 {base - 100} L704 {base - 88} L606 {base - 84}Z" fill="{MESA_D}"/>')


def acacia(x: float, y: float, s: float = 1) -> str:
    """A flat-topped acacia tree."""
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            + stroke("M0 0 Q-4 -60 0 -110 M0 -80 Q-30 -110 -60 -128 M0 -96 Q30 -118 58 -130 M-2 -110 L-6 -134", WOOD_D, 9)
            + f'<ellipse cx="-50" cy="-140" rx="62" ry="18" fill="{LEAF}"/><ellipse cx="44" cy="-146" rx="66" ry="20" fill="{LEAF}"/>'
            f'<ellipse cx="-4" cy="-156" rx="70" ry="20" fill="{LEAF}"/><ellipse cx="0" cy="-150" rx="60" ry="10" fill="{LEAF_D}" opacity=".5"/></g>')


def fig_tree(x: float, y: float, s: float = 1) -> str:
    """A big round shade tree for the wise man's hill."""
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            + f'<path d="M-22 0 Q-14 -80 -20 -150 L20 -150 Q14 -80 22 0Z" fill="{WOOD_D}"/>'
            + "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in
                      [(-90, -180, 60, LEAF_D), (90, -180, 60, LEAF_D), (-40, -230, 70, LEAF), (50, -230, 70, LEAF), (0, -180, 70, LEAF)])
            + '</g>')


def tukul(x: float, y: float, s: float = 1) -> str:
    """A round tukul house: mud walls, a tall cone of thatch, a dark doorway."""
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            f'<path d="M-100 0 V-150 Q0 -166 100 -150 V0 Q0 14 -100 0Z" fill="{MUD}"/>'
            f'<path d="M30 6 V-158 Q70 -156 100 -150 V0 Q70 8 30 6Z" fill="{MUD_D}" opacity=".5"/>'
            f'<path d="M-32 6 V-104 Q0 -134 32 -104 V6 Q0 10 -32 6Z" fill="#4A3020"/>'
            f'<path d="M-126 -136 Q0 -180 126 -136 L8 -300 L-8 -300Z" fill="{THATCH}"/>'
            + stroke("M-80 -150 L-4 -292 M-30 -160 L-2 -292 M30 -160 L2 -292 M80 -150 L4 -292 M-112 -140 Q0 -180 112 -140", THATCH_D, 3)
            + f'<rect x="-4" y="-322" width="8" height="26" fill="{WOOD_D}"/><circle cy="-324" r="6" fill="{GOLD}"/></g>')


def rocks(x: float, y: float, s: float = 1) -> str:
    """The lion's big rounded rocks."""
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            f'<path d="M-160 0 Q-170 -110 -70 -130 Q-10 -190 70 -150 Q160 -150 170 -60 Q180 -10 160 0Z" fill="{ROCK}"/>'
            f'<path d="M20 -150 Q110 -150 150 -80 Q120 -60 70 -70 Q40 -110 20 -150Z" fill="{ROCK_D}" opacity=".6"/>'
            + stroke("M-90 -60 q30 -10 50 6 M30 -40 q20 -16 46 -6", ROCK_D, 3) + '</g>')


def tufts(pts: list, col: str = GRASS_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def flowers(pts: list) -> str:
    """Little yellow highland daisies."""
    ring = [(1, 0), (0, 1), (-1, 0), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)]
    return "".join(f'<g transform="translate({a} {b})">' + "".join(f'<circle cx="{c * 5:.1f}" cy="{s * 5:.1f}" r="3.6" fill="#F7D046"/>' for c, s in ring)
                   + '<circle r="3" fill="#B8742A"/></g>' for a, b in pts)


def suns(n: int) -> str:
    """Little sun tallies at the top left: one sun for each day so far."""
    out = ""
    ring = [(1, 0), (0, 1), (-1, 0), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)]
    for i in range(n):
        cx = 64 + i * 52
        out += stroke(" ".join(f"M{cx + 15 * c:.1f} {58 + 15 * s:.1f} L{cx + 22 * c:.1f} {58 + 22 * s:.1f}" for c, s in ring), "#F2A41F", 4)
        out += f'<circle cx="{cx}" cy="58" r="12" fill="#F7C33B"/>'
    return f'<g filter="url(#p)">{out}</g>'


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def heart(x: float, y: float, s: float = 1) -> str:
    return f'<path transform="translate({x} {y}) scale({s})" filter="url(#p)" d="M0 14 C-30 -6 -22 -30 0 -18 C22 -30 30 -6 0 14Z" fill="{RED}"/>'


WILD = [cloud(560, 90, 1), cloud(250, 120, .7, .8), ambas(),
        f'<path d="M0 392 Q200 370 400 386 T800 380 V600 H0Z" fill="{GRASS_L}"/>',
        acacia(330, 398, .7), rocks(668, 450, 1.05),
        f'<path filter="url(#p)" d="M0 440 Q260 416 520 434 T800 430 V600 H0Z" fill="{GRASS}"/>',
        tufts([(60, 470), (230, 480), (420, 462), (130, 585), (360, 590), (560, 585), (740, 590)])]


def wild(day: int, figures: list) -> list:
    return [*WILD, *figures, suns(day) if day else ""]


HOME_BACK = [cloud(160, 90, 1), cloud(420, 70, .9), ambas(360),
             f'<path d="M0 372 Q200 350 400 366 T800 360 V600 H0Z" fill="{GREEN}"/>',
             acacia(755, 380, .6), tukul(600, 440, 1.05),
             f'<path filter="url(#p)" d="M0 446 Q300 426 560 438 T800 434 V600 H0Z" fill="{GRASS}"/>',
             tufts([(40, 476), (300, 486), (470, 476), (760, 482), (140, 585), (400, 590), (650, 585)])]

HILL = [cloud(160, 80, 1), cloud(380, 120, .7, .8), ambas(),
        f'<path d="M0 372 Q200 350 400 366 T800 360 V600 H0Z" fill="{GREEN}"/>', fig_tree(640, 440, 1),
        f'<path filter="url(#p)" d="M0 440 Q300 410 560 430 T800 424 V600 H0Z" fill="{GREEN_D}"/>',
        tufts([(60, 486), (300, 476), (720, 480), (150, 585), (450, 590)], LEAF_D),
        flowers([(90, 520), (380, 566), (720, 556), (220, 590), (600, 590)])]


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/whiskers-{n:02d}.svg", "w") as fh:
        fh.write(doc)


TUMMY = hands(ADULT, "hold")[0][1] + 4
WHISKERS_UP = whiskers_held(*hands(SEAT, "up")[1])

# 01 cover
svg(1, "The Lion's Whiskers", "Paper-cut cover: in the Ethiopian highlands, under flat-topped blue mountains, a woman in a long white dress with a woven teal-and-gold border and a white shawl stands on the left holding a basket of meat. On the right a big lion with a dark brown mane lies calmly on the golden grass in front of his grey rocks and an acacia tree, looking at her with curious eyes.", MORNING, wild(0, [
    bizunesh(150, arms="hold", held=basket(0, TUMMY, "meat")), lion(560, 548, "lie")]))

# 02 a new mum comes to the round house
svg(2, "A new mum for Abebe", "Paper-cut scene: outside a round house with a tall thatched roof in the green highlands, Abebe's father and his new wife Bizunesh stand together on the left, smiling, Bizunesh holding her arms open. On the right, a little boy, Abebe, in a sky-blue shirt and brown shorts, stands by himself with his hands behind his back, looking down, shy and sad.", DAY, [
    *HOME_BACK, father(90), bizunesh(250, arms="open"), abebe(660, 545, "behind", "shy")])

# 03 Abebe turns away
svg(3, "Abebe turns away", "Paper-cut scene: in front of the round house, Bizunesh holds out a basket of warm bread with a kind smile. Abebe stands a little way off on the right with his hands behind his back, looking down and away, not taking it.", DAY, [
    *HOME_BACK, bizunesh(280, arms="hold", held=basket(0, TUMMY, "bread")), abebe(700, 545, "behind", "sad")])

# 04 the wise old man
svg(4, "Three whiskers from a living lion", "Paper-cut scene: on a grassy hill under a big round shade tree, a wise old man with a white beard, a long white robe and a tall wooden walking stick stands on the right and speaks kindly. Bizunesh stands on the left with her hands together, listening.", DAY, [
    *HILL, bizunesh(260, arms="lap"), elder(530)])

# 05 day one: far away
svg(5, "Day one", "Paper-cut scene: one little sun in the top corner for day one. Far over on the left, Bizunesh stands holding an empty basket, and she has put a clay dish of meat down on the grass beside her. Far away on the right, the big lion lies in front of his rocks under an acacia tree, watching her with curious eyes. There is a lot of grass between them.", MORNING, wild(1, [
    bizunesh(110, arms="hold", held=basket(0, TUMMY)), dish(215), lion(570, 548, "lie")]))

# 06 day two: a few steps closer; the lion stands up
svg(6, "Day two", "Paper-cut scene: two little suns in the top corner for day two. Bizunesh stands a few steps closer, holding her empty basket, with a clay dish of meat on the grass in front of her. The big lion has stood up in front of his rocks and looks at her with curious eyes. There is still a wide space between them.", MORNING, wild(2, [
    bizunesh(170, arms="hold", held=basket(0, TUMMY)), dish(285), lion(590, 545, "stand")]))

# 07 day three: the lion comes and eats
svg(7, "Day three", "Paper-cut scene: three little suns in the top corner for day three. Bizunesh stands quietly on the left with her empty basket. The big lion has walked up to the clay dish she left on the grass and has lowered his head to eat the meat, calm and peaceful. There is still a gap between them.", MORNING, wild(3, [
    bizunesh(140, arms="hold", held=basket(0, TUMMY)), lion(520, 545, "eat", dish=True)]))

# 08 day four: she sits down, close by
svg(8, "Day four", "Paper-cut scene: four little suns in the top corner for day four. Bizunesh sits on the grass with her hands in her lap, closer to the lion now, smiling softly. The big lion eats the meat from the clay dish a few steps away from her, calm and not afraid.", MORNING, wild(4, [
    bizunesh(200, 545, arms="lap", sit=True), lion(540, 545, "eat", dish=True)]))

# 09 day five: the lion eats right beside her
svg(9, "Day five", "Paper-cut scene: five little suns in the top corner for day five. Bizunesh sits on the grass right beside the big lion, smiling. The lion eats from the clay dish next to her, peaceful, with his eyes softly closed.", MORNING, wild(5, [
    bizunesh(190, 545, arms="lap", sit=True), lion(490, 545, "eat", "calm", dish=True)]))

# 10 three whiskers
svg(10, "One, two, three whiskers", "Paper-cut scene: five little suns in the top corner. The big lion lies peacefully on the grass beside Bizunesh with his eyes closed, full and sleepy, with little white purring marks above him. Bizunesh sits beside him and holds up three long, pale whiskers in her hand, smiling.", MORNING, wild(5, [
    bizunesh(200, 545, arms="up", sit=True, held=WHISKERS_UP), lion(520, 548, "lie", "calm"),
    marks(["M372 400 q6 -7 12 0 q6 7 12 0", "M362 380 q6 -7 12 0 q6 7 12 0", "M376 360 q6 -7 12 0 q6 7 12 0"], "#fff", 3.4)]))

FLOAT = "M450 350 l-18 -42 M420 290 l-36 -22 M468 286 l-4 -46"
# 11 the wise old man: no potion needed
svg(11, "You don't need a potion", "Paper-cut scene: back on the grassy hill under the big shade tree, the wise old man smiles and holds out his open hand, and three pale lion whiskers float away on the breeze, with little swirls of wind. Bizunesh stands on the left with her hands open, surprised and thinking.", DAY, [
    *HILL, bizunesh(240, arms="open", mood="oh"), elder(540, arms="give"),
    stroke(FLOAT, MANE_D, 6), stroke(FLOAT, "#FFF6E6", 3),
    marks(["M330 230 q16 -12 32 0 q16 12 32 0", "M420 200 q14 -10 28 0 q14 10 28 0"], "#fff", 3.4)])

# 12 slowly, slowly with Abebe
svg(12, "Slowly, slowly with Abebe", "Paper-cut scene: in front of the round house, Bizunesh sits quietly on the grass with a basket of warm bread beside her, smiling. Abebe stands a little way off on the right and peeks at her with a tiny, shy smile.", DAY, [
    *HOME_BACK, bizunesh(230, 545, arms="lap", sit=True), group(345, 548, K, basket(0, -36, "bread")),
    abebe(500, 548, "behind", "small")])

# 13 Abebe loves his new mum: holding hands, with a clear gap between the two of them
BW = 330
HOLD = ((26, 14, 46, 30), (30, 36, 52, 66))
b_rh = hands(ADULT, HOLD)[1]
hand_x, hand_y = BW + b_rh[0] * K, GROUND + b_rh[1] * K
boy_x = hand_x + (CHILD["sx"] + 30) * K
boy_hy = (hand_y - GROUND) / K - (CHILD["sy"] + 6)
svg(13, "Abebe and his new mum", "Paper-cut scene: in the warm golden evening light outside the round house, Abebe and Bizunesh stand side by side holding hands, both smiling happily, with a red heart above them. Abebe's father stands on the left, smiling at them.", GOLDEN, [
    *HOME_BACK, father(150, mood="happy"), bizunesh(BW, arms=HOLD, mood="happy"),
    abebe(boy_x, GROUND, ((20, boy_hy * .5, 30, boy_hy), (12, 26, 10, 54)), "happy"),
    heart(400, 230, 1.3)])
