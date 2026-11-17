#!/usr/bin/env python3
"""Generates the 13 Empty Pot flip-book SVGs from shared paper-cut character parts.

Usage: python3 pot_gen.py <output-dir>
Scale rule: every person is drawn by person(x, y, k, who) with (x, y) at the feet. Pages that show
an adult use k = 1, so a child (about 210 tall) always comes up to an adult's chest (about 300 tall).
Ping's blue-and-white pot is drawn in Ping's own units, so it stays the same size beside him.
Faces are round with round dot eyes (the same faces as every other KaiSTEM book): no caricature.
Ping's pot shows only bare soil until the last page; the cooked seeds appear only on page 12.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SKIN, SKIN_D, CHEEK = "#F3C9A0", "#DDA57A", "#F0705F"
HAIR, GREY = "#2A2422", "#ECE8E2"
SOIL = "#5A3B22"
PORC, PORC_B, PORC_D = "#F7F9FC", "#2F6DB5", "#C9D6E8"
CLAY, CLAY_D = "#C9714A", "#9E5232"
GOLD, GOLD_D = "#E9B53B", "#B98A22"
RED, RED_D = "#C8463A", "#9C2F27"
STONE, STONE_D = "#E8DCC8", "#C9B99E"
WALL, WALL_D, TILE, TILE_D = "#FBF3E4", "#E6D8BE", "#7D8A99", "#5C6876"
GRASS, GRASS_D, GRASS_L, LEAF = "#6BB86A", "#3F9A56", "#9AD27E", "#4E9E4E"
BARK, BLOSSOM, BLOSSOM_D = "#7E5130", "#F7B8CC", "#E98AA8"
DAY = [(0, "#86CDEB"), (1, "#EAF6FB")]
SPRING = [(0, "#9BD3EE"), (.7, "#FBE6EE"), (1, "#FDF0E6")]
GOLDEN = [(0, "#8FCFEA"), (.6, "#FDE7C0"), (1, "#FCD9A0")]
INDOOR = [(0, "#F4E3C6"), (1, "#EBD3AE")]

# Body shapes. All y values are above the feet (negative = up). arm = how far arm poses reach.
CHILD = dict(head=-158, r=34, sy=-124, sx=26, hem=-46, hx=40, sash=-80, leg=-50, arm=1, sleeve=15, hand=8)
ADULT = dict(head=-262, r=33, sy=-226, sx=36, hem=-84, hx=52, sash=-160, leg=-88, arm=1.7, sleeve=20, hand=10)
WHO = {  # body, tunic, tunic shade, collar, sash, trousers, hair style
    "ping": (CHILD, "#3E7CC4", "#2F65A6", "#F6E7C8", "#E25A4A", "#2F4F7A", "boy"),
    "mei": (CHILD, "#E98AA8", "#CF6C8C", "#FFF1C9", "#7FB6E0", "#7A4E66", "girl"),
    "bo": (CHILD, "#F0954A", "#D27630", "#FFF1C9", "#4E9E4E", "#6B4E36", "boy"),
    "lan": (CHILD, "#6BB36A", "#4E944E", "#FFF1C9", "#F2C230", "#3F5E44", "girl"),
    "tao": (CHILD, "#9C7CD0", "#7F60B3", "#FFF1C9", "#F0954A", "#4E3F6B", "boy"),
    "papa": (ADULT, "#5E8C5A", "#4A7347", "#F6E7C8", "#B07A48", "#6B4E36", "man"),
    "emperor": (ADULT, "#F2C230", "#D49A1E", "#C8463A", "#C8463A", None, "emperor"),
}
# Arm poses in child units: (left arm, right arm), each (ctrl dx, ctrl dy, hand dx, hand dy) from the
# shoulder, with dx measured OUTWARD from the body (so the same numbers mirror for both arms).
ARMS = {
    "down": ((12, 26, 10, 54), (12, 26, 10, 54)),
    "hold": ((18, 30, -1, 46), (18, 30, -1, 46)),        # hands on a pot held at the tummy
    "low": ((16, 34, 2, 62), (16, 34, 2, 62)),           # hands on a pot held low
    "palm": ((12, 26, 10, 54), (34, 6, 30, 24)),         # right hand held out flat, palm up
    "open": ((26, 14, 46, 30), (26, 14, 46, 30)),        # arms open wide
    "up": ((26, -18, 30, -52), (26, -18, 30, -52)),      # hooray
    "pat": ((12, 26, 10, 54), (34, 22, 50, 46)),         # right hand reaching out and down
    "bowl": ((16, 30, -4, 44), (16, 30, -4, 44)),        # holding a bowl at the chest
    "behind": ((8, 20, 2, 40), (8, 20, 2, 40)),          # hands tucked behind the back
}


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, inner: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({s})"{f}>{inner}</g>'


# ---------------------------------------------------------------- faces and people
def face(r: float, mood: str, who: str) -> str:
    ex, my = r * .36, r * .44
    out = ""
    if who == "emperor":  # white bushy brows
        out += stroke(f"M{-ex - 9} -12 q8 -6 15 -2 M{ex + 9} -12 q-8 -6 -15 -2", GREY, 5)
    elif mood in ("sad", "tear"):
        out += stroke(f"M{-ex - 7} -11 L{-ex + 5} -15 M{ex + 7} -11 L{ex - 5} -15", HAIR, 2.6)
    elif mood == "brave":
        out += stroke(f"M{-ex - 7} -15 L{-ex + 6} -12 M{ex + 7} -15 L{ex - 6} -12", HAIR, 2.8)
    else:
        out += stroke(f"M{-ex - 6} -14 q6 -4 12 0 M{ex - 6} -14 q6 -4 12 0", HAIR, 2.4)
    for sx in (-1, 1):
        out += f'<circle cx="{sx * ex}" cy="0" r="4.8" fill="{INK}"/><circle cx="{sx * ex + 1.6}" cy="-1.6" r="1.6" fill="#fff"/>'
    out += f'<circle cx="{-r * .62}" cy="{r * .3}" r="7" fill="{CHEEK}" opacity=".42"/><circle cx="{r * .62}" cy="{r * .3}" r="7" fill="{CHEEK}" opacity=".42"/>'
    if mood == "frown":
        out += stroke(f"M-7 {my + 2} h14", "#7A3B2E", 2.6)
    elif mood == "smile":
        out += stroke(f"M-8 {my - 2} q8 8 16 0", "#7A3B2E", 2.6)
    elif mood == "happy":
        out += f'<path d="M-11 {my - 3} Q0 {my - 1} 11 {my - 3} Q9 {my + 10} 0 {my + 10} Q-9 {my + 10} -11 {my - 3}Z" fill="#7A3B2E"/>'
    elif mood in ("sad", "tear"):
        out += stroke(f"M-7 {my + 4} q7 -6 14 0", "#7A3B2E", 2.6)
    elif mood == "brave":
        out += stroke(f"M-6 {my + 1} q6 2 12 0", "#7A3B2E", 2.6)
    elif mood == "oh":
        out += f'<ellipse cy="{my + 2}" rx="5" ry="6.5" fill="#7A3B2E"/>'
    if mood == "tear":
        out += f'<path d="M{-ex} 8 q5 8 0 12 q-5 -4 0 -12z" fill="#8FD0F0"/>'
    return out


def hair(r: float, style: str) -> str:
    def bangs(c: str) -> str:
        return (f'<path d="M{-r - 1} 2 Q{-r - 3} {-r - 6} 0 {-r - 4} Q{r + 3} {-r - 6} {r + 1} 2 '
                f'Q{r - 4} {-r * .5} {r * .4} {-r * .58} Q0 {-r * .42} {-r * .4} {-r * .58} Q{-r + 4} {-r * .5} {-r - 1} 2Z" fill="{c}"/>')
    if style == "girl":
        return (f'<circle cx="{-r + 2}" cy="{-r + 6}" r="13" fill="{HAIR}"/><circle cx="{r - 2}" cy="{-r + 6}" r="13" fill="{HAIR}"/>'
                + bangs(HAIR) + stroke(f"M{-r - 6} {-r + 14} l8 -6 M{r + 6} {-r + 14} l-8 -6", "#E25A4A", 3.4))
    if style == "emperor":
        return (bangs(GREY) + f'<circle cy="{-r - 6}" r="12" fill="{GREY}"/>'
                f'<path d="M-15 {-r - 10} L-12 {-r - 30} L-4 {-r - 20} L0 {-r - 34} L4 {-r - 20} L12 {-r - 30} L15 {-r - 10}Z" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="2"/>'
                + stroke(f"M-24 {-r - 13} H24", GOLD_D, 4))
    out = bangs(HAIR) + f'<circle cy="{-r - 6}" r="11" fill="{HAIR}"/>'
    return out + stroke(f"M-9 {-r - 1} h18", "#E25A4A" if style == "boy" else "#8A5A36", 3.4)


def beard(r: float, who: str) -> str:
    if who == "emperor":
        return (f'<path d="M-20 {r * .5} Q-22 {r * 1.6} 0 {r * 2.3} Q22 {r * 1.6} 20 {r * .5} Q0 {r * .8} -20 {r * .5}Z" fill="{GREY}"/>'
                + stroke(f"M-4 {r * .46} q-12 2 -22 14 M4 {r * .46} q12 2 22 14", GREY, 5))
    if who == "papa":
        return stroke(f"M-3 {r * .32} q-8 2 -14 8 M3 {r * .32} q8 2 14 8", HAIR, 4)
    return ""


def arm_paths(B: dict, pose) -> list:
    left, right = ARMS[pose] if isinstance(pose, str) else pose
    a, sy, sx = B["arm"], B["sy"] + 6, B["sx"]
    out = []
    for sgn, (cx, cy, hx, hy) in ((-1, left), (1, right)):
        x0 = sgn * sx
        out.append((f"M{x0} {sy} Q{x0 + sgn * cx * a:.0f} {sy + cy * a:.0f} {x0 + sgn * hx * a:.0f} {sy + hy * a:.0f}",
                    (x0 + sgn * hx * a, sy + hy * a)))
    return out


def person(x: float, y: float, k: float, who: str, arms="down", mood: str = "smile", held: str = "",
           sash: str = "") -> str:
    """A person facing us. (x, y) is the feet. held = svg drawn between the sleeves and the hands."""
    B, tunic, shade, collar, belt, trousers, style = WHO[who]
    r, sy, sx, hem, hx = B["r"], B["sy"], B["sx"], B["hem"], B["hx"]
    out = ""
    if who == "emperor":  # a long robe to the ground, black shoe tips peeping out
        hem, hx = -6, 66
        out += f'<ellipse cx="-22" cy="-3" rx="16" ry="6" fill="{HAIR}"/><ellipse cx="22" cy="-3" rx="16" ry="6" fill="{HAIR}"/>'
    else:
        lt = B["leg"]
        out += stroke(f"M-12 {lt} L-14 -8 M12 {lt} L14 -8", trousers, 16 * (1.3 if B is ADULT else 1))
        out += f'<ellipse cx="-17" cy="-4" rx="12" ry="6" fill="{HAIR}"/><ellipse cx="17" cy="-4" rx="12" ry="6" fill="{HAIR}"/>'
    mid = (sy + hem) / 2
    out += (f'<path d="M{-sx} {sy} Q{-hx - 4} {mid} {-hx} {hem} Q0 {hem + 8} {hx} {hem} Q{hx + 4} {mid} {sx} {sy} '
            f'Q0 {sy - 8} {-sx} {sy}Z" fill="{tunic}"/>')
    out += f'<path d="M{-hx * .2} {hem + 2} L{-hx * .9} {hem} Q{-hx - 2} {mid} {-sx} {sy} L{-sx * .3} {sy}Z" fill="{shade}" opacity=".35"/>'
    # cross-over collar: the left panel overlaps to the wearer's right
    out += stroke(f"M{sx * .5} {sy - 3} L{-sx * .85} {sy + (hem - sy) * .42:.0f}", collar, 7 if B is CHILD else 9)
    out += stroke(f"M{-sx * .5} {sy - 3} L-2 {sy + 12}", collar, 6 if B is CHILD else 8)
    w = sx + (hx - sx) * (B["sash"] - sy) / (hem - sy) + 2
    out += f'<rect x="{-w:.0f}" y="{B["sash"]}" width="{2 * w:.0f}" height="{10 if B is CHILD else 14}" rx="3" fill="{sash or belt}"/>'
    if who == "emperor":  # a round golden badge on the chest
        out += (f'<circle cx="0" cy="{sy + 34}" r="17" fill="{GOLD_D}"/><circle cx="0" cy="{sy + 34}" r="12" fill="{GOLD}"/>'
                + stroke(f"M-7 {sy + 34} q3 -6 7 0 q4 6 7 0", RED, 2.4))
    (la, lh), (ra, rh) = arm_paths(B, arms)
    out += stroke(la, tunic, B["sleeve"]) + stroke(ra, tunic, B["sleeve"])
    out += held
    out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="{B["hand"]}" fill="{SKIN}"/>' for a, b in (lh, rh))
    head = (f'<circle cx="{-r}" cy="4" r="7" fill="{SKIN_D}"/><circle cx="{r}" cy="4" r="7" fill="{SKIN_D}"/>'
            f'<circle r="{r}" fill="{SKIN}"/>' + hair(r, style) + face(r, mood, who) + beard(r, who))
    out += f'<g transform="translate(0 {B["head"]})">{head}</g>'
    return group(x, y, k, out)


def hands_of(who: str, arms) -> tuple:
    """Where a person's two hands are, in their own units (for placing held things)."""
    (_, lh), (_, rh) = arm_paths(WHO[who][0], arms)
    return lh, rh


# ---------------------------------------------------------------- pots and plants
def pot_shape(kind: str, top: float, h: float = 54, w: float = 64) -> str:
    """A pot whose rim top is at y=top (local, centred on x=0), h tall, w wide at the rim."""
    b = top + h
    if kind == "blue":
        body, rim = PORC, PORC_D
        deco = (f'<path d="M{-w / 2 + 5} {top + 18} H{w / 2 - 5} L{w / 2 - 7} {top + 26} H{-w / 2 + 7}Z" fill="{PORC_B}"/>'
                + stroke(f"M-12 {top + 38} q6 -8 12 0 q6 8 12 0", PORC_B, 3)
                + f'<path d="M{-w / 2 + 12} {b - 6} H{w / 2 - 12}" stroke="{PORC_B}" stroke-width="3"/>')
    else:
        body, rim = {"clay": (CLAY, CLAY_D), "green": ("#7FB89A", "#5B957A"), "red": ("#D9604F", "#B04538"),
                     "yellow": ("#EBC357", "#C79E35")}[kind]
        deco = f'<path d="M{-w / 2 + 6} {top + 22} H{w / 2 - 6}" stroke="{rim}" stroke-width="4" opacity=".7"/>'
    return (f'<path d="M{-w / 2 + 2} {top + 8} L{-w / 2 + 12} {b} Q0 {b + 4} {w / 2 - 12} {b} L{w / 2 - 2} {top + 8}Z" fill="{body}"/>'
            + deco + f'<rect x="{-w / 2 - 3}" y="{top}" width="{w + 6}" height="10" rx="4" fill="{rim}"/>'
            f'<ellipse cy="{top + 2}" rx="{w / 2 - 2}" ry="5" fill="{SOIL}"/>')


def peony(x: float, y: float, s: float, col: str, dark: str) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})"><circle r="17" fill="{dark}"/>'
            + "".join(f'<circle cx="{a}" cy="{b}" r="11" fill="{col}"/>' for a, b in [(-9, -6), (9, -6), (-10, 6), (10, 6), (0, -12), (0, 11)])
            + f'<circle r="9" fill="{dark}"/><circle r="5" fill="#F7D046"/></g>')


def mum(x: float, y: float, s: float, col: str, dark: str) -> str:
    petals = "".join(f'<ellipse cx="0" cy="-12" rx="4" ry="11" fill="{col}" transform="rotate({a})"/>' for a in range(0, 360, 30))
    return f'<g transform="translate({x} {y}) scale({s})">{petals}<circle r="8" fill="{dark}"/></g>'


FLOWER_SETS = [  # (draw, colour, dark) — one bunch per child's pot
    (peony, "#F28FAE", "#D9607F"), (mum, "#F7D046", "#D9A21E"), (peony, "#E8574A", "#B8352B"),
    (mum, "#F4F1EA", "#D2C6B0"), (peony, "#C9A2EA", "#9C7CD0"),
]


def plant(top: float, n: int, height: float = 70) -> str:
    """A bushy flowering plant growing out of a pot rim at y=top. n chooses the flower set."""
    draw, col, dark = FLOWER_SETS[n % len(FLOWER_SETS)]
    out = stroke(f"M0 {top} Q-4 {top - height * .5} -20 {top - height * .8} M0 {top} V{top - height} "
                 f"M0 {top} Q4 {top - height * .5} 20 {top - height * .78}", GRASS_D, 3.4)
    for a, b, rot in [(-14, top - 18, -40), (14, top - 24, 40), (-8, top - height * .55, -30), (10, top - height * .6, 30)]:
        out += f'<ellipse cx="{a}" cy="{b:.0f}" rx="12" ry="5.5" fill="{LEAF}" transform="rotate({rot} {a} {b:.0f})"/>'
    for a, b, s in [(-20, top - height * .8, .85), (20, top - height * .78, .85), (0, top - height, 1)]:
        out += draw(a, round(b), s, col, dark)
    return out


def pot(x: float, y: float, k: float, kind: str = "blue", flowers: int = -1, big: bool = False) -> str:
    """A pot standing on the ground at (x, y). Ping's pot is kind='blue' with no flowers."""
    h, w = (66, 80) if big else (54, 64)
    inner = pot_shape(kind, -h, h, w) + (plant(-h, flowers) if flowers >= 0 else "")
    return group(x, y, k, inner)


def held_pot(who: str, arms: str, kind: str = "blue", flowers: int = -1, big: bool = False) -> str:
    """A pot held between the hands of a pose, in the holder's own units, so it scales with them."""
    (lx, ly), (rx, _) = hands_of(who, arms)
    h, w = (66, 80) if big else (54, 64)
    top = ly - 18
    inner = pot_shape(kind, top, h, w) + (plant(top, flowers, 60) if flowers >= 0 else "")
    return f'<g transform="translate({(lx + rx) / 2:.0f} 0)" filter="url(#p)">{inner}</g>'


# ---------------------------------------------------------------- scenery
def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def sun(x: float, y: float, s: float = 1) -> str:
    rays = " ".join(f"M{x + 58 * s * c:.0f} {y + 58 * s * d:.0f} L{x + 78 * s * c:.0f} {y + 78 * s * d:.0f}"
                    for c, d in [(1, 0), (.71, .71), (0, 1), (-.71, .71), (-1, 0), (-.71, -.71), (0, -1), (.71, -.71)])
    return stroke(rays, "#F7C844", 7 * s) + f'<circle cx="{x}" cy="{y}" r="{46 * s}" fill="#F7D046" filter="url(#p)"/>'


def roof(w: float, top: float, base: float, fill: str, dark: str) -> str:
    """A curved roof with upturned eave tips, centred on x=0, ridge at y=top, eaves at y=base."""
    t = w / 2
    d = (f"M{-t - 22} {base - 18} Q{-t + 6} {base + 4} {-t + 30} {base} L{t - 30} {base} Q{t - 6} {base + 4} {t + 22} {base - 18} "
         f"Q{t - 10} {base - 10} {t - 46} {top} L{-t + 46} {top} Q{-t + 10} {base - 10} {-t - 22} {base - 18}Z")
    lines = " ".join(f"M{a} {top + 4} L{a * 1.12:.0f} {base - 2}" for a in range(int(-t + 60), int(t - 50), 24))
    return (f'<path d="{d}" fill="{fill}"/>' + stroke(lines, dark, 2.4)
            + f'<rect x="{-t + 36}" y="{top - 9}" width="{w - 72}" height="11" rx="5" fill="{dark}"/>')


def palace(x: float, y: float, s: float = 1) -> str:
    """A red palace hall with a golden roof, standing on stone steps; (x, y) is the bottom step."""
    cols = "".join(f'<rect x="{a - 9}" y="-150" width="18" height="150" fill="{RED_D}"/>' for a in (-150, -86, 86, 150))
    door = (f'<rect x="-46" y="-118" width="92" height="118" rx="4" fill="{RED_D}"/><rect x="-40" y="-112" width="38" height="112" fill="{RED}"/>'
            f'<rect x="2" y="-112" width="38" height="112" fill="{RED}"/>'
            + "".join(f'<circle cx="{a}" cy="{b}" r="3" fill="{GOLD}"/>' for a in (-28, -14, 14, 28) for b in (-90, -70, -50, -30)))
    inner = (f'<rect x="-210" y="-6" width="420" height="34" fill="{STONE}"/><rect x="-170" y="-34" width="340" height="30" fill="{STONE_D}"/>'
             + stroke("M-210 12 H210", STONE_D, 2) + f'<g transform="translate(0 -34)">'
             f'<rect x="-180" y="-150" width="360" height="150" fill="{RED}"/>{cols}{door}'
             + roof(420, -236, -146, GOLD, GOLD_D) + '</g>')
    return group(x, y, s, inner)


def house(x: float, y: float, s: float = 1, door: bool = True) -> str:
    """Ping's little home: white walls, grey tiled roof, a round lattice window."""
    inner = (f'<rect x="-140" y="-150" width="280" height="150" fill="{WALL}"/><rect x="-140" y="-16" width="280" height="16" fill="{WALL_D}"/>'
             f'<circle cx="-72" cy="-86" r="30" fill="#B07A48"/><circle cx="-72" cy="-86" r="24" fill="#F4E3C6"/>'
             + stroke("M-96 -86 H-48 M-72 -110 V-62 M-89 -103 L-55 -69 M-55 -103 L-89 -69", "#B07A48", 3)
             + (f'<rect x="30" y="-112" width="64" height="112" rx="4" fill="#8A5A36"/><rect x="36" y="-106" width="25" height="106" fill="#A86E44"/>'
                f'<rect x="63" y="-106" width="25" height="106" fill="#A86E44"/>' if door else "")
             + roof(330, -210, -146, TILE, TILE_D))
    return group(x, y, s, inner)


def tree(x: float, y: float, s: float = 1, col: str = BLOSSOM, dark: str = BLOSSOM_D) -> str:
    """A round blossom tree (peach or plum, pink in spring)."""
    blobs = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in
                    [(-50, -170, 46, dark), (40, -176, 50, dark), (-6, -214, 52, col), (-60, -150, 40, col), (56, -150, 42, col), (0, -160, 46, col)])
    dots = "".join(f'<circle cx="{a}" cy="{b}" r="4" fill="#fff" opacity=".85"/>' for a, b in
                   [(-40, -200), (10, -232), (50, -180), (-70, -160), (24, -150), (-14, -176), (70, -140)])
    return group(x, y, s, f'<path d="M-10 0 L-6 -120 L-30 -160 M-6 -120 L22 -170" stroke="{BARK}" stroke-width="16" fill="none" stroke-linecap="round"/>{blobs}{dots}')


def willow(x: float, y: float, s: float = 1) -> str:
    strands = " ".join(f"M{a} -170 q{6 if a < 0 else -6} 60 {a * .1:.0f} 120" for a in range(-60, 70, 20))
    return group(x, y, s, f'<path d="M-6 0 L-4 -150 Q0 -190 30 -200" stroke="{BARK}" stroke-width="14" fill="none" stroke-linecap="round"/>'
                 f'<ellipse cy="-180" rx="80" ry="34" fill="{GRASS_D}"/>' + stroke(strands, GRASS, 8))


def bed(pts: list) -> str:
    """A row of garden flowers standing in the grass."""
    out = ""
    for i, (a, b) in enumerate(pts):
        draw, col, dark = FLOWER_SETS[i % len(FLOWER_SETS)]
        out += stroke(f"M{a} {b} V{b - 40}", GRASS_D, 3.4)
        out += f'<ellipse cx="{a - 9}" cy="{b - 14}" rx="10" ry="4.5" fill="{LEAF}" transform="rotate(-30 {a - 9} {b - 14})"/>'
        out += draw(a, b - 44, .9, col, dark)
    return out


def tufts(pts: list, col: str = GRASS_D, w: float = 3) -> str:
    return stroke(" ".join(f"M{a - 6} {b} l3 -10 M{a} {b} l0 -13 M{a + 6} {b} l-3 -10" for a, b in pts), col, w)


def ground(y: float, col: str = GRASS, back: str = GRASS_L) -> list:
    return [f'<path d="M0 {y - 30} Q260 {y - 70} 520 {y - 40} T800 {y - 50} V600 H0Z" fill="{back}"/>',
            f'<path filter="url(#p)" d="M0 {y} Q400 {y - 34} 800 {y} V600 H0Z" fill="{col}"/>']


def courtyard(y: float) -> str:
    """Pale stone paving in front of the palace."""
    lines = " ".join([f"M0 {y + d} H800" for d in (40, 90, 150)] + [f"M{a} {y} L{a * 1.3 - 120:.0f} 600" for a in range(80, 800, 130)])
    return f'<path filter="url(#p)" d="M0 {y} H800 V600 H0Z" fill="{STONE}"/>' + stroke(lines, STONE_D, 2.4)


def bench(x: float, y: float, w: float = 120, h: float = 54) -> str:
    """A low stone garden bench; its top is at y - h."""
    return (f'<g filter="url(#p)"><rect x="{x - w / 2 + 10}" y="{y - h}" width="18" height="{h}" fill="{STONE_D}"/>'
            f'<rect x="{x + w / 2 - 28}" y="{y - h}" width="18" height="{h}" fill="{STONE_D}"/>'
            f'<rect x="{x - w / 2}" y="{y - h - 12}" width="{w}" height="16" rx="5" fill="{STONE}"/></g>')


def can(x: float, y: float, s: float = 1, pour: bool = False) -> str:
    """A little green watering can, its bottom at (x, y), spout to the right."""
    drops = "".join(f'<path d="M{a} {b} q4 7 0 10 q-4 -3 0 -10z" fill="#8FD0F0"/>' for a, b in [(66, -40), (76, -24), (60, -18)]) if pour else ""
    return group(x, y, s, f'<path d="M14 -40 L52 -58 L56 -52 L22 -28Z" fill="#4E944E"/>'
                 + stroke("M-18 -46 Q0 -78 18 -46", "#3F7A3F", 6)
                 + f'<rect x="-26" y="-46" width="48" height="46" rx="8" fill="#6BB36A"/>{drops}')


def pats(x: float, y: float) -> str:
    return f'<g opacity=".9">{stroke(f"M{x - 22} {y - 8} l-8 -8 M{x} {y - 14} v-12 M{x + 22} {y - 8} l8 -8", INK, 3)}</g>'


def snow(pts: list) -> str:
    return "".join(f'<circle cx="{a}" cy="{b}" r="{3 + (i % 3)}" fill="#fff"/>' for i, (a, b) in enumerate(pts))


def bubble(x: float, y: float, w: float, h: float, tail: tuple, inner: str) -> str:
    """A thought bubble centred on (x, y) with little circles trailing to tail."""
    tx, ty = tail
    dots = "".join(f'<circle cx="{x + (tx - x) * t:.0f}" cy="{y + h / 2 + (ty - y - h / 2) * t:.0f}" r="{r}" fill="#fff"/>'
                   for t, r in [(.45, 9), (.8, 6)])
    return (f'<g filter="url(#p)"><ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{h / 2}" fill="#fff"/>{dots}</g>'
            f'<g transform="translate({x} {y})">{inner}</g>')


def cooking() -> str:
    """Inside the bubble: a cooking pot on a little fire, steam rising, seeds tumbling in."""
    seeds = "".join(f'<ellipse cx="{a}" cy="{b}" rx="4" ry="6" fill="#C9A15A" stroke="#8A5A36" stroke-width="1.4" transform="rotate({r} {a} {b})"/>'
                    for a, b, r in [(-30, -50, 20), (-16, -60, -10), (-2, -48, 30)])
    return (stroke("M-26 -38 q-8 -12 0 -22 M0 -40 q-8 -12 0 -22 M26 -38 q-8 -12 0 -22", "#B9C4D0", 4) + seeds
            + f'<path d="M-44 -26 H44 L38 18 Q0 28 -38 18Z" fill="#5C6876"/><rect x="-50" y="-32" width="100" height="10" rx="5" fill="#7D8A99"/>'
            + stroke("M-50 -24 h-12 M50 -24 h12", "#5C6876", 6)
            + '<path d="M-24 40 Q-16 22 -8 34 Q0 16 8 34 Q16 22 24 40Z" fill="#F0954A"/><path d="M-12 40 Q0 26 12 40Z" fill="#F7D046"/>')


def sprout(x: float, y: float, s: float = 1, bloom: bool = True) -> str:
    out = stroke("M0 0 V-46", GRASS_D, 4)
    out += '<ellipse cx="-12" cy="-26" rx="12" ry="5.5" fill="#6BB86A" transform="rotate(-30 -12 -26)"/>'
    out += '<ellipse cx="12" cy="-34" rx="12" ry="5.5" fill="#6BB86A" transform="rotate(30 12 -34)"/>'
    if bloom:
        out += peony(0, -54, .75, "#F28FAE", "#D9607F")
    return group(x, y, s, out)


def sparkles(pts: list, col: str = "#fff") -> str:
    return "".join(f'<path d="M{a} {b - 9} L{a + 2.5} {b - 2.5} L{a + 9} {b} L{a + 2.5} {b + 2.5} L{a} {b + 9} L{a - 2.5} {b + 2.5} '
                   f'L{a - 9} {b} L{a - 2.5} {b - 2.5}Z" fill="{col}"/>' for a, b in pts)


def butterfly(x: float, y: float, col: str = "#F7D046") -> str:
    return (f'<g transform="translate({x} {y})"><ellipse cx="-8" cy="-4" rx="9" ry="7" fill="{col}"/><ellipse cx="8" cy="-4" rx="9" ry="7" fill="{col}"/>'
            f'<ellipse cx="-6" cy="6" rx="6" ry="5" fill="{col}"/><ellipse cx="6" cy="6" rx="6" ry="5" fill="{col}"/>'
            f'<rect x="-1.6" y="-8" width="3.2" height="18" rx="1.6" fill="{INK}"/></g>')


# ---------------------------------------------------------------- page assembly
def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/pot-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def ping(x: float, y: float, k: float = 1, arms="hold", mood: str = "smile", **kw) -> str:
    """Ping holding his bigger blue-and-white pot (from page 6 on; always bare soil)."""
    held = held_pot("ping", arms, big=True) if arms in ("hold", "low") else ""
    return person(x, y, k, "ping", arms, mood, held, **kw)


def kid(x: float, y: float, who: str, n: int, arms: str = "low", mood: str = "smile", kind: str = "clay") -> str:
    return person(x, y, 1, who, arms, mood, held_pot(who, arms, kind, n))


KS = 1.3  # Ping's size on the pages where he is alone

# 01 cover
svg(1, "The Empty Pot", "Paper-cut cover: a boy called Ping, with black hair tied in a little topknot and a blue tunic with a cream cross-over collar and a red sash, stands smiling in a garden, holding a blue-and-white pot of bare brown soil. Behind him is a red palace with a golden curved roof on stone steps, and pink and yellow flowers grow on both sides.", DAY, [
    cloud(130, 80, .9), cloud(680, 70, .8),
    *ground(470), palace(400, 400, .82),
    bed([(60, 520), (120, 540), (170, 510), (630, 512), (690, 540), (750, 520)]),
    ping(400, 560, KS, "hold", "smile")])

# 02 the old emperor who loves flowers
svg(2, "An emperor who loved flowers", "Paper-cut scene: an old emperor with a long white beard, a small gold crown on his white topknot and a long yellow robe with a red sash stands smiling in his palace garden with his arms open wide. Flowers grow all around him — pink and red peonies, yellow and white chrysanthemums and purple flowers — and two butterflies flutter by. A golden palace roof shows over the wall behind.", DAY, [
    cloud(140, 70, .9), cloud(660, 60, .8),
    *ground(470), palace(400, 330, .6),
    f'<rect x="-10" y="372" width="820" height="70" fill="{WALL}" filter="url(#p)"/><rect x="-10" y="364" width="820" height="12" fill="{TILE}"/>',
    willow(80, 470, .9), bed([(130, 520), (200, 545), (250, 515), (560, 515), (610, 545), (680, 520), (740, 548)]),
    person(400, 560, 1, "emperor", "open", "smile"),
    butterfly(250, 250, "#F7D046"), butterfly(590, 220, "#F28FAE")])

# 03 Ping, who could make anything grow
svg(3, "Ping could make anything grow", "Paper-cut scene: outside a little white house with a grey tiled roof, the boy Ping stands smiling in his garden, pouring water from a green watering can onto a row of big, bright flowers — pink, yellow, red and white. A pink blossom tree grows beside the house.", DAY, [
    sun(680, 90, .8), cloud(180, 80, .9),
    *ground(460), house(330, 420, .9), tree(640, 440, .9),
    person(240, 556, KS, "ping", ((12, 26, 10, 54), (30, 14, 46, 18)), "happy",
           held=f'<g transform="translate(70 -96)">{can(0, 0, .9, True)}</g>'),
    bed([(370, 560), (420, 540), (470, 562), (520, 545), (570, 565)]),
    tufts([(60, 520), (700, 500), (760, 560)])])

# 04 one seed for every child
svg(4, "One seed for every child", "Paper-cut scene: in front of the red palace, the old emperor in his yellow robe holds a golden bowl of seeds and smiles. Four children stand in a row beside him — a girl in pink, a boy in orange, a girl in green, and Ping in blue, nearest the emperor. Ping holds out one hand towards the emperor with a single small seed on it, sparkling, and his mouth is open in wonder.", DAY, [
    cloud(120, 70, .8), cloud(690, 64, .8),
    palace(470, 380, .78), courtyard(420),
    person(610, 556, 1, "emperor", "bowl", "smile",
           held="".join(f'<ellipse cx="{a}" cy="-158" rx="3.6" ry="5.4" fill="#C9A15A" stroke="#8A5A36" stroke-width="1.2"/>' for a in (-22, -10, 2, 14, 24))
                + f'<path d="M-40 -158 H40 Q36 -122 0 -118 Q-36 -122 -40 -158Z" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="3"/>'),
    person(90, 540, 1, "mei", "down", "smile"), person(195, 545, 1, "bo", "down", "smile"),
    person(300, 550, 1, "lan", "down", "smile"),
    person(420, 556, 1, "ping", "palm", "oh",
           held='<ellipse cx="56" cy="-102" rx="4" ry="6" fill="#C9A15A" stroke="#8A5A36" stroke-width="1.4"/>'),
    sparkles([(478, 420), (502, 438), (486, 456)], "#F7D046")])

# 05 pat, pat, pat — and water every day
svg(5, "Pat, pat, pat", "Paper-cut scene: in the little garden by his white house, Ping reaches out and pats the brown soil in his blue-and-white pot, which stands on a low stone bench. Little lines show the pat, pat, pat. A green watering can waits on the grass. There is nothing growing in the pot.", DAY, [
    sun(110, 90, .7), cloud(620, 80, .9),
    *ground(460), house(560, 420, .9),
    bench(470, 556, 140, 58),
    pot(470, 484, KS * .9, "blue"), pats(466, 400),
    person(300, 560, KS, "ping", "pat", "smile"),
    can(640, 560, 1.1), tufts([(80, 540), (700, 510), (760, 570)])])

# 06 a bigger pot, more sunshine
svg(6, "A bigger pot, more sunshine", "Paper-cut scene: under a big yellow sun, Ping lifts a bigger blue-and-white pot of rich brown soil up towards the sunshine, hoping. Nothing is growing in it. A pink blossom tree and the little white house are behind him.", DAY, [
    sun(620, 110, 1.05), cloud(170, 80, .9),
    *ground(470), house(190, 430, .8), tree(700, 460, .85),
    person(400, 560, KS, "ping", "hold", "brave", held_pot("ping", "hold", big=True)),
    tufts([(80, 540), (560, 520), (740, 560)])])

# 07 summer, autumn, winter — still nothing
svg(7, "Still nothing", "Paper-cut scene: inside the little house in winter. Through a round window, snow falls on a bare tree. The blue-and-white pot sits on the windowsill with only brown soil in it. Ping stands beside it, sad, with a tear on his cheek.", INDOOR, [
    f'<rect x="0" y="470" width="800" height="130" fill="#C9A47A" filter="url(#p)"/>' + stroke("M0 520 H800 M0 570 H800", "#B08A60", 2.4),
    f'<circle cx="520" cy="230" r="138" fill="#B07A48" filter="url(#p)"/><circle cx="520" cy="230" r="124" fill="#C9D9EA"/>',
    f'<path d="M420 300 Q520 270 640 300 L640 360 H400Z" fill="#fff"/>',
    f'<path d="M470 320 L476 230 L450 196 M476 230 L506 186 M476 250 L500 236" stroke="{BARK}" stroke-width="9" fill="none" stroke-linecap="round"/>',
    snow([(440, 150), (500, 130), (570, 160), (610, 220), (450, 230), (540, 210), (600, 290), (470, 280), (560, 110), (420, 200), (630, 170), (520, 250)]),
    stroke("M396 230 H644 M520 106 V354", "#B07A48", 5),
    f'<rect x="360" y="352" width="320" height="18" rx="4" fill="#8A5A36" filter="url(#p)"/>',
    pot(560, 352, KS, "blue", big=True),
    person(250, 556, KS, "ping", "down", "tear")])

# 08 spring: the children carry their flowers to the palace
svg(8, "Off to the palace", "Paper-cut scene: in spring, under pink blossom trees, children walk along the path towards the red palace far away, each carrying a pot of flowers — a girl in pink with pink peonies, a boy in orange with yellow chrysanthemums, and a girl in green with red peonies. Last of all comes Ping, holding his blue-and-white pot of bare soil, looking down and sad.", SPRING, [
    cloud(160, 70, .8), cloud(640, 60, .7),
    *ground(430), palace(400, 300, .42),
    f'<path d="M340 330 Q400 320 460 330 L700 600 H100Z" fill="{STONE}"/>',
    tree(90, 470, .95), tree(730, 470, .95),
    kid(170, 540, "mei", 0), kid(305, 545, "bo", 1, kind="yellow"), kid(440, 550, "lan", 2, kind="green"),
    ping(610, 560, 1, "low", "sad")])

# 09 Ping's father: your best is good enough
svg(9, "You did your best", "Paper-cut scene: at the door of the little white house, Ping's father, a tall man in a green tunic with a little moustache, rests one hand gently on Ping's shoulder and smiles. Ping holds his blue-and-white pot of bare soil and looks up, ready to be brave.", DAY, [
    cloud(640, 70, .8),
    *ground(460), house(330, 420, .95), tree(700, 460, .8),
    ping(395, 560, 1, "hold", "brave"),
    person(270, 556, 1, "papa", ((12, 26, 10, 54), (34, 16, 37, 59)), "smile"),
    tufts([(80, 540), (620, 540), (760, 570)])])

# 10 the emperor walks past every flower, frowning
ROW = [(300, 0, "clay"), (410, 1, "yellow"), (520, 2, "green"), (630, 4, "red")]
svg(10, "The emperor did not smile", "Paper-cut scene: in the palace courtyard, five children stand in a row. In front of four of them is a pot full of flowers — pink peonies, yellow chrysanthemums, red peonies and purple flowers. At the end of the row Ping holds his blue-and-white pot of bare soil. On the left, the old emperor stands looking along the row, not smiling.", DAY, [
    palace(470, 330, .6), courtyard(380),
    person(140, 560, 1, "emperor", "behind", "frown"),
    person(300, 480, 1, "mei", "down", "smile"), person(410, 482, 1, "bo", "down", "smile"),
    person(520, 484, 1, "lan", "down", "smile"), person(630, 486, 1, "tao", "down", "smile"),
    *[pot(a, 556, 1, kind, n) for a, n, kind in ROW],
    ping(730, 560, 1, "hold", "sad")])

# 11 why an empty pot? Ping tells the truth
svg(11, "Ping tells the truth", "Paper-cut scene: in the palace courtyard, the old emperor in his yellow robe, not smiling, stands beside Ping, who only comes up to his chest. Ping holds his blue-and-white pot of bare soil and speaks bravely, his eyebrows set firm. A pot of pink peonies stands on the stones behind them.", DAY, [
    palace(400, 330, .6), courtyard(380),
    pot(650, 470, 1, "clay", 0),
    person(310, 560, 1, "emperor", "behind", "frown"),
    ping(490, 560, 1, "hold", "brave")])

LIFT = ((10, -30, 26, -56), (12, 26, 10, 54))  # the emperor holds the pot up high on one hand

# 12 the seeds were cooked!
svg(12, "The seeds were cooked!", "Paper-cut scene: the old emperor beams and lifts Ping's empty blue-and-white pot up high. A thought bubble beside him shows a cooking pot steaming over a little fire with seeds tumbling in: the seeds he gave out had been cooked. Ping, beside him, looks up with his mouth open in surprise, and so do a girl in pink and a boy in orange standing behind their flower pots.", DAY, [
    palace(400, 330, .6), courtyard(380),
    bubble(610, 150, 190, 150, (400, 262), cooking()),
    person(330, 560, 1, "emperor", LIFT, "happy",
           f'<g transform="translate({hands_of("emperor", LIFT)[0][0]:.0f} 0)" filter="url(#p)">{pot_shape("blue", hands_of("emperor", LIFT)[0][1] - 74, 66, 80)}</g>'),
    person(480, 560, 1, "ping", "down", "oh"),
    person(600, 484, 1, "mei", "down", "oh"), person(715, 488, 1, "bo", "down", "oh"),
    pot(600, 556, 1, "clay", 0), pot(715, 558, 1, "yellow", 1)])

# 13 Ping will be emperor; together they plant a real seed
svg(13, "Grow, little seed, grow!", "Paper-cut scene: in the palace garden in warm golden light, the old emperor and Ping stand side by side, both smiling. Ping now wears a golden sash. Between them, a new clay pot has a green sprout with two leaves and one pink flower just opening. Flowers grow all around, and the golden palace roof rises behind them.", GOLDEN, [
    cloud(150, 80, .8, .8), cloud(660, 70, .7, .7),
    *ground(470), palace(400, 330, .6),
    bed([(60, 530), (110, 556), (690, 530), (740, 556), (160, 520), (640, 520)]),
    person(250, 556, 1, "emperor", "open", "smile"),
    pot(410, 556, 1.1, "clay"), sprout(410, 486, 1.1), sparkles([(380, 400), (446, 410), (412, 372)], "#fff"),
    person(560, 560, 1, "ping", "up", "happy", sash=GOLD)])
