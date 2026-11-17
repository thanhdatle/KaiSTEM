#!/usr/bin/env python3
"""Generates the 13 Finn McCool and the Giant's Causeway flip-book SVGs from shared character parts.

Usage: python3 finn_gen.py <output-dir>
Scale rule: every person is drawn at SIZE[who] on every page (Finn 1, Oonagh .9, Benandonner 1.3),
so Benandonner is always the biggest. Outdoors the giants stand on stepping stones only ~46 px wide,
so the giants are always huge next to the sea and the stones. Indoors uses the same sizes: it is a giant's house.
Outdoor geometry is fixed: Irish cliff top y = 400 (x 0..214), stepping-stone tops y = 470, Scottish shore y = 448 (x 650..).
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SIZE = {"finn": 1.0, "oonagh": .9, "ben": 1.3}
SKIN = {"finn": "#F6C9A0", "oonagh": "#F8D3B0", "ben": "#E8B48A"}
SKIN_D = {"finn": "#E3A77C", "oonagh": "#E9B48E", "ben": "#CF9468"}
FINN_HAIR, FINN_TUNIC, FINN_TUNIC_D, FINN_LEGS = "#E0823A", "#4E9A5A", "#3C7D48", "#8A6A4A"
BEN_HAIR, BEN_TUNIC, BEN_TUNIC_D, BEN_KILT, BEN_KILT_L = "#3B2A22", "#5A6FA8", "#47598C", "#B8433A", "#2F6B4A"
OON_HAIR, OON_DRESS, OON_DRESS_D, APRON = "#8A4B2A", "#8C5BB0", "#734596", "#FFF3DC"
BOOT, BELT, GOLD = "#5A3B22", "#6B4426", "#F2C14E"
STONE, STONE_L, STONE_D = "#7E7F8C", "#A3A4B0", "#53545F"
SEA, SEA_L, SEA_D = "#3E8FC9", "#8FD0F0", "#2F7DB8"
GRASS, GRASS_D, GRASS_L = "#5DB85C", "#3F9A56", "#86D16E"
ROCK, ROCK_D = "#8A7B6A", "#6E6052"
HILL_S, HEATHER = "#8E7FB5", "#9C6FA8"
WALL, WALL_D, FLOOR, WOOD, WOOD_D = "#F3E6CF", "#E2CFAF", "#B9A58A", "#B07A48", "#7E5130"
CAKE, CAKE_D = "#E2A95A", "#B97A34"
DAY = [(0, "#7CCBE8"), (1, "#E9F6FB")]
INDOOR = [(0, "#F3E6CF"), (1, "#F3E6CF")]
GOLDEN = [(0, "#8FB8E0"), (.55, "#FDE0B0"), (1, "#F8C58A")]
CLIFF, PATH, SHORE = 400, 470, 448
IN = 1.25  # indoor close-up zoom, the same on every indoor page


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, inner: str, flip: bool = False) -> str:
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})" filter="url(#p)">{inner}</g>'


# ---------------------------------------------------------------- faces
def eyes(mood: str, look: float) -> str:
    lx = look * 3
    if mood == "laugh":
        return stroke("M-19 -6 q6 -7 12 0 M7 -6 q6 -7 12 0", INK, 3.2)
    if mood == "sleep":
        return stroke("M-19 -4 q6 6 12 0 M7 -4 q6 6 12 0", INK, 3)
    if mood == "cry":
        return stroke("M-20 -8 L-8 -3 L-20 2 M20 -8 L8 -3 L20 2", INK, 3.4)
    if mood == "ouch":
        return (stroke("M-20 -9 L-8 -4 L-20 1", INK, 3.4)
                + f'<circle cx="13" cy="-4" r="7" fill="#fff"/><circle cx="{13 + lx}" cy="-4" r="3.6" fill="{INK}"/>')
    r = 8 if mood in ("oh", "shock") else 7
    return "".join(f'<circle cx="{sx * 13}" cy="-4" r="{r}" fill="#fff"/><circle cx="{sx * 13 + lx}" cy="-3" r="3.6" fill="{INK}"/>' for sx in (-1, 1))


def brows(mood: str, col: str) -> str:
    if mood in ("oh", "worry", "shock"):
        return stroke("M-21 -18 q8 -8 15 -3 M21 -18 q-8 -8 -15 -3", col, 4)
    return stroke("M-20 -16 q7 -5 13 -1 M20 -16 q-7 -5 -13 -1", col, 3.4)


def mouth(mood: str, y: float = 20, col: str = "#7A2E2A") -> str:
    if mood in ("oh", "shock"):
        return f'<ellipse cy="{y + 2}" rx="7" ry="9" fill="{col}"/>'
    if mood == "worry":
        return stroke(f"M-12 {y + 2} q6 -5 12 0 q6 5 12 0", col, 3)
    if mood in ("laugh", "boom"):
        return f'<path d="M-14 {y - 4} Q0 {y + 18} 14 {y - 4}Z" fill="{col}"/><path d="M-8 {y + 4} Q0 {y + 10} 8 {y + 4}Z" fill="#F08C8C"/>'
    if mood == "cry":
        return f'<ellipse cy="{y + 4}" rx="12" ry="13" fill="{col}"/><ellipse cy="{y + 11}" rx="7" ry="4" fill="#F08C8C"/>'
    if mood == "ouch":
        return f'<rect x="-12" y="{y - 3}" width="24" height="9" rx="4" fill="#fff" stroke="{col}" stroke-width="2.4"/>' + stroke(f"M-4 {y - 3} v9 M4 {y - 3} v9", col, 1.6)
    if mood == "shh":
        return f'<ellipse cy="{y + 1}" rx="4" ry="4" fill="{col}"/>'
    if mood == "sleep":
        return stroke(f"M-6 {y} q6 4 12 0", col, 2.6)
    return stroke(f"M-12 {y - 2} Q0 {y + 8} 12 {y - 2}", col, 3.2)


def head(who: str, mood: str, look: float = 0, bonnet: bool = False) -> str:
    """A head centred on (0, 0), radius 38."""
    skin, skin_d = SKIN[who], SKIN_D[who]
    out = ""
    if bonnet:  # a frilly baby bonnet round Finn's face, hiding his hair
        frill = "".join(f'<circle cx="{a}" cy="{b}" r="11" fill="#fff"/>' for a, b in
                        [(-48, 14), (-52, -6), (-48, -26), (-36, -42), (-18, -52), (0, -55), (18, -52), (36, -42), (48, -26), (52, -6), (48, 14)])
        out += f'<g filter="url(#p)">{frill}<circle cy="-8" r="50" fill="#FDFBF5"/></g>'
        out += stroke("M-40 -10 Q0 -46 40 -10", "#F4B6C8", 3)
    if who == "ben":  # big bushy dark hair behind the head
        out += "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{BEN_HAIR}"/>' for a, b, r in
                       [(-34, -22, 18), (-22, -38, 20), (0, -44, 22), (22, -38, 20), (34, -22, 18)])
    if who == "oonagh":  # hair falls behind her shoulders
        out += f'<path d="M-42 -6 Q-48 -50 0 -50 Q48 -50 42 -6 L46 40 L-46 40Z" fill="{OON_HAIR}"/>'
    out += f'<circle cx="-37" cy="4" r="8" fill="{skin_d}"/><circle cx="37" cy="4" r="8" fill="{skin_d}"/>'
    out += f'<circle r="38" fill="{skin}"/>'
    if who == "finn" and not bonnet:
        out += (f'<path d="M-38 -4 Q-44 -46 -4 -46 Q34 -50 40 -6 Q32 -26 18 -28 Q8 -16 -6 -28 Q-22 -22 -38 -4Z" fill="{FINN_HAIR}"/>'
                f'<path d="M-10 -44 q4 -16 18 -14 q-8 6 -6 14Z" fill="{FINN_HAIR}"/>')
    if who == "finn":
        out += "".join(f'<circle cx="{a}" cy="{b}" r="1.6" fill="#C9805A"/>' for a, b in [(-24, 8), (-20, 12), (-27, 13), (24, 8), (20, 12), (27, 13)])
    if who == "oonagh":
        out += f'<path d="M-38 -2 Q-36 -44 0 -42 Q36 -44 38 -2 Q24 -30 0 -30 Q-24 -30 -38 -2Z" fill="{OON_HAIR}"/>'
        out += '<circle cx="-26" cy="-34" r="5" fill="#F7D046"/><circle cx="-26" cy="-34" r="2" fill="#E58A2B"/>'
    if who == "ben":
        out += f'<path d="M-36 -10 Q-30 -34 0 -34 Q30 -34 36 -10 Q24 -24 0 -24 Q-24 -24 -36 -10Z" fill="{BEN_HAIR}"/>'
    if mood != "cry":
        out += '<circle cx="-22" cy="12" r="7" fill="#F0705F" opacity=".4"/><circle cx="22" cy="12" r="7" fill="#F0705F" opacity=".4"/>'
    out += eyes(mood, look) + brows(mood, BEN_HAIR if who == "ben" else ("#B8602A" if who == "finn" else OON_HAIR))
    out += f'<ellipse cy="8" rx="6" ry="5" fill="{skin_d}"/>'
    if who == "ben":  # bushy brown-black beard round his jaw, with a gap for his mouth
        out += f'<path d="M-38 0 Q-46 54 -12 64 Q0 70 12 64 Q46 54 38 0 Q32 30 14 32 Q0 40 -14 32 Q-32 30 -38 0Z" fill="{BEN_HAIR}"/>'
        out += f'<path d="M-18 18 Q-8 10 0 16 Q8 10 18 18 Q8 23 0 20 Q-8 23 -18 18Z" fill="{BEN_HAIR}"/>'
        out += (f'<ellipse cy="29" rx="8" ry="10" fill="#5A1E1A" stroke="#F2C4A0" stroke-width="2.4"/>' if mood in ("oh", "shock") else mouth(mood, 27, "#C2504A"))
    else:
        out += mouth(mood)
    if mood == "cry":
        out += '<path d="M-22 4 q-6 10 0 14 q6 -4 0 -14Z M22 4 q-6 10 0 14 q6 -4 0 -14Z" fill="#8FD0F0"/>'
    if bonnet:
        out += '<path d="M-30 26 Q0 44 30 26" stroke="#F4B6C8" stroke-width="5" fill="none"/>'
        out += '<path d="M0 42 l-14 -8 l0 16Z M0 42 l14 -8 l0 16Z" fill="#F4B6C8"/><circle cy="42" r="4" fill="#E58FA8"/>'
    return out


# ---------------------------------------------------------------- bodies
ARMS = {  # (left control, left hand, right control, right hand) in body units; feet at (0, 0), shoulders at (+-44, -186)
    "down": ((-64, -150), (-62, -104), (64, -150), (62, -104)),
    "carry": ((-74, -150), (-34, -150), (74, -150), (34, -150)),
    "shade": ((-64, -150), (-62, -104), (86, -230), (24, -270)),
    "hips": ((-84, -170), (-58, -128), (84, -170), (58, -128)),
    "wave": ((-64, -150), (-62, -104), (92, -210), (90, -292)),
    "cheeks": ((-74, -196), (-32, -236), (74, -196), (32, -236)),
    "up": ((-82, -214), (-94, -286), (82, -214), (94, -286)),
    "run": ((-80, -160), (-96, -196), (70, -140), (92, -118)),
    "shh": ((-64, -150), (-62, -104), (74, -170), (8, -226)),
    "ouch": ((-74, -150), (-76, -170), (78, -196), (34, -236)),
    "bake": ((-30, -120), (40, -120), (80, -150), (82, -132)),
    "tuck": ((-20, -120), (54, -112), (84, -150), (92, -120)),
}


def arms(name: str, sleeve: str, skin: str) -> str:
    cl, hl, cr, hr = ARMS[name]
    out = stroke(f"M-42 -184 Q{cl[0]} {cl[1]} {hl[0]} {hl[1]}", sleeve, 20) + stroke(f"M42 -184 Q{cr[0]} {cr[1]} {hr[0]} {hr[1]}", sleeve, 20)
    out += f'<circle cx="{hl[0]}" cy="{hl[1]}" r="12" fill="{skin}"/><circle cx="{hr[0]}" cy="{hr[1]}" r="12" fill="{skin}"/>'
    if name == "shh":
        out += stroke(f"M{hr[0]} {hr[1] - 6} v-16", skin, 7)
    return out


def legs(who: str, pose: str) -> str:
    col = {"finn": FINN_LEGS, "ben": SKIN["ben"], "oonagh": SKIN["oonagh"]}[who]
    if who == "oonagh":
        return f'<ellipse cx="-20" cy="-6" rx="20" ry="9" fill="{BOOT}"/><ellipse cx="20" cy="-6" rx="20" ry="9" fill="{BOOT}"/>'
    if pose == "run":
        return (stroke("M-18 -90 L-42 -18", col, 24) + stroke("M18 -90 L44 -54 L70 -64", col, 24)
                + f'<ellipse cx="-48" cy="-10" rx="24" ry="12" fill="{BOOT}"/>'
                + f'<ellipse cx="80" cy="-64" rx="22" ry="12" fill="{BOOT}" transform="rotate(-20 80 -64)"/>')
    return (stroke("M-20 -90 L-22 -16 M20 -90 L22 -16", col, 24)
            + f'<ellipse cx="-26" cy="-8" rx="24" ry="12" fill="{BOOT}"/><ellipse cx="26" cy="-8" rx="24" ry="12" fill="{BOOT}"/>')


def torso(who: str) -> str:
    if who == "oonagh":
        return (f'<path d="M-40 -192 Q-52 -120 -78 -12 Q0 2 78 -12 Q52 -120 40 -192 Q0 -204 -40 -192Z" fill="{OON_DRESS}"/>'
                f'<path d="M-30 -132 L-44 -24 Q0 -16 44 -24 L30 -132Z" fill="{APRON}"/>' + stroke("M-32 -132 H32", APRON, 6)
                + stroke("M-60 -40 Q0 -28 60 -40", OON_DRESS_D, 3))
    tunic, tunic_d = (FINN_TUNIC, FINN_TUNIC_D) if who == "finn" else (BEN_TUNIC, BEN_TUNIC_D)
    out = f'<path d="M-48 -196 Q-58 -140 -62 -84 Q0 -70 62 -84 Q58 -140 48 -196 Q0 -210 -48 -196Z" fill="{tunic}"/>'
    out += stroke("M-14 -200 L0 -176 L14 -200", tunic_d, 4)
    if who == "ben":  # a red tartan kilt
        out += f'<path d="M-60 -124 L-72 -62 Q0 -50 72 -62 L60 -124Z" fill="{BEN_KILT}"/>'
        out += stroke("M-40 -124 L-46 -56 M-12 -124 L-14 -52 M16 -124 L18 -52 M44 -124 L50 -56", BEN_KILT_L, 4)
        out += stroke("M-64 -100 H64 M-68 -76 H68", BEN_KILT_L, 3)
        out += stroke("M-28 -124 L-30 -54 M30 -124 L34 -54", GOLD, 1.6)
    out += f'<rect x="-60" y="-132" width="120" height="14" rx="4" fill="{BELT}"/><rect x="-9" y="-134" width="18" height="18" rx="3" fill="{GOLD}"/>'
    if who == "finn":  # a round gold brooch on his tunic
        out += f'<circle cx="-26" cy="-180" r="7" fill="{GOLD}"/><circle cx="-26" cy="-180" r="3" fill="{FINN_TUNIC_D}"/>'
    return out


def person(x: float, y: float, who: str, arm: str = "down", mood: str = "smile", look: float = 0,
           pose: str = "stand", item: str = "", k: float = 1, flip: bool = False) -> str:
    """A person facing us. (x, y) is their feet. Drawn at SIZE[who] * k (k = IN indoors, 1 outdoors)."""
    skin = SKIN[who]
    sleeve = {"finn": FINN_TUNIC, "ben": BEN_TUNIC, "oonagh": OON_DRESS}[who]
    out = legs(who, pose) + torso(who)
    out += f'<rect x="-12" y="-216" width="24" height="26" fill="{SKIN_D[who]}"/>'
    out += f'<g transform="translate(0 -244)">{head(who, mood, look)}</g>'
    if who == "oonagh":  # her long plait over one shoulder
        out += "".join(f'<ellipse cx="{30 + i * 2}" cy="{-206 + i * 16}" rx="9" ry="10" fill="{OON_HAIR}"/>' for i in range(5))
        out += f'<path d="M36 -128 l-6 12 l12 0Z" fill="{OON_HAIR}"/><rect x="31" y="-140" width="12" height="7" rx="3" fill="#F7D046"/>'
    out += arms(arm, sleeve, skin)
    out += item
    return group(x, y, SIZE[who] * k, out, flip)


# ---------------------------------------------------------------- props
def hexstone(x: float, top: float, w: float = 50, h: float = 44) -> str:
    """A six-sided basalt column seen a little from above: a flat top and a dark side going down."""
    a, b = w / 2, w / 4
    q = w * .22
    top_pts = [(x - a, top), (x - b, top - q), (x + b, top - q), (x + a, top), (x + b, top + q), (x - b, top + q)]
    side = f"M{x - a} {top} L{x - b} {top + q} L{x + b} {top + q} L{x + a} {top} V{top + h} L{x + b} {top + q + h} L{x - b} {top + q + h} L{x - a} {top + h}Z"
    pts = " ".join(f"{p:.1f},{r:.1f}" for p, r in top_pts)
    return (f'<path d="{side}" fill="{STONE_D}"/>' + stroke(f"M{x - b} {top + q} V{top + q + h} M{x + b} {top + q} V{top + q + h}", "#45464F", 1.6)
            + f'<polygon points="{pts}" fill="{STONE}"/><polygon points="{pts}" fill="{STONE_L}" opacity=".45" transform="translate(0 -1.5)"/>')


def path_stones(x0: float, x1: float, step: float = 48) -> str:
    out, x, i = "", x0, 0
    while x <= x1:
        out += hexstone(x, PATH - (2 if i % 2 else 0))
        x += step
        i += 1
    return f'<g filter="url(#p)">{out}</g>'


def carried_stone(y: float = -150) -> str:
    """A stone column held in the arms (body units)."""
    return f'<g transform="translate(0 {y})">{hexstone(0, -24, 54, 46)}</g>'


def cake(x: float, y: float, r: float = 20, stone: bool = False, bitten: bool = False) -> str:
    if bitten:  # a bite out of the top-right, showing the hidden grey stone
        body = (f'<path d="M{x + 2} {y - r} A{r} {r} 0 1 0 {x + r} {y - 2} A7 7 0 0 1 {x + 14} {y - 8} '
                f'A7 7 0 0 1 {x + 8} {y - 14} A7 7 0 0 1 {x + 2} {y - r}Z" fill="{CAKE}" stroke="{CAKE_D}" stroke-width="2.4"/>')
        return body + f'<ellipse cx="{x + 7}" cy="{y - 6}" rx="8" ry="6" fill="{STONE}" stroke="{STONE_D}" stroke-width="2"/>'
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CAKE}" stroke="{CAKE_D}" stroke-width="2.4"/>'
    out += stroke(f"M{x - r * .5} {y - r * .2} l{r * .3} {r * .3} M{x + r * .1} {y - r * .5} l{r * .2} {r * .4} M{x} {y + r * .3} l{r * .3} {r * .1}", CAKE_D, 2)
    if stone:
        out += f'<ellipse cx="{x}" cy="{y}" rx="{r * .45}" ry="{r * .32}" fill="{STONE}" stroke="{STONE_D}" stroke-width="2"/>'
    return out


def cradle(cx: float, cy: float, baby: str = "") -> str:
    """A giant wooden rocking cradle, side view, hood on the left. (x, y) is the floor under its middle.
    baby: '' empty, 'lie' (Finn tucked in, eyes open), 'sleep' (Finn pretending to sleep), 'sit' (Finn sat up crying)."""
    x, y = 0, 0
    out = stroke(f"M{x - 106} {y - 30} Q{x} {y + 6} {x + 106} {y - 30}", WOOD_D, 12)
    out += f'<path d="M{x - 108} {y - 210} Q{x - 108} {y - 236} {x - 82} {y - 236} L{x - 66} {y - 236} Q{x - 46} {y - 236} {x - 46} {y - 210} L{x - 46} {y - 130} L{x - 108} {y - 130}Z" fill="{WOOD_D}"/>'
    if baby in ("lie", "sleep"):
        out += f'<g transform="translate({x - 14} {y - 152}) rotate(-8)">{head("finn", "sleep" if baby == "sleep" else "smile", 1, bonnet=True)}</g>'
        out += (f'<path d="M{x + 18} {y - 128} Q{x + 30} {y - 170} {x + 70} {y - 166} Q{x + 104} {y - 168} {x + 100} {y - 128}Z" fill="#7FB6E0"/>'
                + stroke(f"M{x + 40} {y - 164} V{y - 128} M{x + 76} {y - 166} V{y - 128} M{x + 22} {y - 146} H{x + 96}", "#fff", 2.4))
    if baby == "sit":
        out += f'<path d="M{x - 52} {y - 128} Q{x - 70} {y - 192} {x - 10} {y - 196} Q{x + 50} {y - 192} {x + 34} {y - 128}Z" fill="#FDFBF5"/>'
        out += stroke(f"M{x - 44} {y - 176} Q{x - 82} {y - 196} {x - 92} {y - 236}", "#FDFBF5", 20) + stroke(f"M{x + 24} {y - 176} Q{x + 62} {y - 196} {x + 72} {y - 236}", "#FDFBF5", 20)
        out += f'<circle cx="{x - 92}" cy="{y - 240}" r="12" fill="{SKIN["finn"]}"/><circle cx="{x + 72}" cy="{y - 240}" r="12" fill="{SKIN["finn"]}"/>'
        out += f'<g transform="translate({x - 10} {y - 232})">{head("finn", "cry", 0, bonnet=True)}</g>'
        out += f'<path d="M{x + 30} {y - 128} Q{x + 50} {y - 156} {x + 84} {y - 152} Q{x + 96} {y - 150} {x + 100} {y - 128}Z" fill="#7FB6E0"/>'
    out += f'<rect x="{x - 112}" y="{y - 132}" width="224" height="104" rx="18" fill="{WOOD}"/>'
    out += stroke(f"M{x - 102} {y - 116} H{x + 102}", "#CF9D68", 4) + stroke(f"M{x - 54} {y - 100} v52 M{x} {y - 100} v52 M{x + 54} {y - 100} v52", WOOD_D, 3)
    out += f'<path d="M{x - 30} {y - 76} l8 -8 l8 8 l-8 8Z M{x + 30} {y - 76} l8 -8 l8 8 l-8 8Z" fill="#F2789F"/>'
    return f'<g transform="translate({cx} {cy}) scale({IN})" filter="url(#p)">{out}</g>'


def splash(x: float, y: float, s: float = 1) -> str:
    spikes = "M-60 0 L-48 -34 L-34 -8 L-22 -52 L-8 -10 L4 -60 L16 -12 L30 -48 L40 -8 L52 -32 L60 0Z"
    drops = "".join(f'<path d="M{a} {b} q6 10 0 14 q-6 -4 0 -14z" fill="#fff"/>' for a, b in [(-60, -60), (-24, -86), (30, -84), (64, -56)])
    return f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><path d="{spikes}" fill="{SEA_L}"/><path d="M-36 0 L-24 -30 L-10 -6 L4 -40 L16 -6 L30 -28 L38 0Z" fill="#fff" opacity=".85"/>{drops}</g>'


def marks(ds: list, col: str = INK, w: float = 4) -> str:
    return f'<g opacity=".85">{stroke(" ".join(ds), col, w)}</g>'


def gulls(pts: list) -> str:
    return stroke(" ".join(f"M{a - 12} {b} q6 -8 12 0 q6 -8 12 0" for a, b in pts), "#4A5568", 3)


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def sheep(x: float, y: float) -> str:
    """A tiny sheep, to show how big the giants are."""
    return (f'<g transform="translate({x} {y})" filter="url(#p)"><rect x="-9" y="-6" width="3" height="7" fill="{INK}"/><rect x="5" y="-6" width="3" height="7" fill="{INK}"/>'
            '<circle cx="-6" cy="-11" r="6" fill="#fff"/><circle cx="2" cy="-13" r="7" fill="#fff"/><circle cx="8" cy="-10" r="5" fill="#fff"/>'
            f'<ellipse cx="14" cy="-12" rx="4" ry="3.4" fill="{INK}"/></g>')


# ---------------------------------------------------------------- outdoor scene
def sea(top: float = 330) -> str:
    waves = " ".join(f"M{a} {b} h{w}" for a, b, w in [(250, 380, 30), (420, 360, 40), (560, 400, 26), (300, 430, 34), (480, 420, 30), (380, 540, 40), (560, 560, 30), (260, 575, 26)])
    return (f'<rect y="{top}" width="800" height="{600 - top}" fill="{SEA}"/><rect y="{top}" width="800" height="16" fill="{SEA_L}" opacity=".5"/>'
            + f'<g opacity=".6">{stroke(waves, "#fff", 3.4)}</g>')


def front_wave(y: float = 510) -> str:
    segs = "".join(f" T{x} {y}" for x in range(100, 801, 100))
    return (f'<path d="M0 {y} Q50 {y - 7} 100 {y}{segs} V600 H0Z" fill="{SEA}" opacity=".96"/>'
            + stroke(f"M0 {y - 1} Q50 {y - 8} 100 {y - 1}" + "".join(f" T{x} {y - 1}" for x in range(200, 801, 100)), SEA_L, 4)
            + f'<g opacity=".7">{stroke("M120 540 h34 M330 560 h40 M520 545 h30 M690 565 h34", "#fff", 3.4)}</g>')


SCOT_HILLS = f'<path d="M520 336 Q600 270 680 312 Q740 276 820 300 V340 H520Z" fill="{HILL_S}"/><path d="M640 330 Q700 300 760 322 L760 340 H640Z" fill="#7A6CA3"/>'
IRISH_CLIFF = (f'<path filter="url(#p)" d="M-10 412 L214 412 L224 470 L206 600 H-10Z" fill="{ROCK}"/>'
               + stroke("M40 440 v60 M110 450 v90 M170 436 v70 M70 520 v60", ROCK_D, 3)
               + f'<path d="M-10 394 Q100 388 216 400 L218 418 Q100 410 -10 418Z" fill="{GRASS}"/>')
SCOT_SHORE = (f'<path filter="url(#p)" d="M652 456 Q700 444 820 448 V600 H640Z" fill="{ROCK}"/>'
              + f'<path d="M654 452 Q700 440 820 444 V460 Q720 456 650 466Z" fill="{HEATHER}"/>'
              + stroke("M690 490 v50 M750 480 v70", ROCK_D, 3))


def outdoor(*, stones: str = "", back: list = (), people: list = (), front: list = (), sky: list = (), cloud2: float = 540) -> list:
    return [cloud(160, 90, 1), cloud(cloud2, 70, .8), *sky, SCOT_HILLS, sea(), IRISH_CLIFF, SCOT_SHORE, *back, stones, *people, front_wave(), *front]


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<clipPath id="door"><rect x="40" y="180" width="150" height="380" rx="60"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/finn-{n:02d}.svg", "w") as fh:
        fh.write(doc)


# ---------------------------------------------------------------- indoor scene
def room(door_open: bool = False, door_body: str = "", fire: bool = True) -> list:
    """Inside Finn and Oonagh's giant house: door on the left, fireplace in the middle-left, a window, and the floor."""
    out = [f'<rect width="800" height="600" fill="{WALL}"/>',
           stroke("M0 46 H800 M0 90 H800", WOOD_D, 10),
           f'<rect y="540" width="800" height="60" fill="{FLOOR}"/>' + stroke("M0 540 H800 M90 540 l-20 60 M260 540 l-10 60 M430 540 v60 M600 540 l10 60 M740 540 l20 60", "#A08D72", 3)]
    out.append(f'<rect x="30" y="170" width="170" height="390" rx="66" fill="{WOOD_D}"/>')
    if door_open:
        out.append(f'<g clip-path="url(#door)"><rect x="40" y="180" width="150" height="380" fill="#9FD6EE"/>'
                   f'<rect x="40" y="390" width="150" height="170" fill="{SEA}"/><path d="M40 400 Q120 380 190 396 V400 H40Z" fill="{HILL_S}"/>'
                   f'{door_body}</g>')
    else:
        out.append(f'<rect x="40" y="180" width="150" height="380" rx="60" fill="{WOOD}"/>' + stroke("M80 200 V560 M115 184 V560 M150 200 V560", WOOD_D, 3)
                   + f'<circle cx="172" cy="380" r="7" fill="{GOLD}"/>')
    out.append('<g filter="url(#p)"><path d="M232 560 V300 Q232 280 252 280 H408 Q428 280 428 300 V560Z" fill="#B7AFA4"/>'
               '<path d="M262 560 V350 Q330 320 398 350 V560Z" fill="#3A2E2A"/></g>'
               + stroke("M232 330 H428 M232 390 h30 M398 390 h30 M232 450 h30 M398 450 h30 M232 510 h30 M398 510 h30 M300 280 v50 M360 280 v50", "#958C80", 3)
               + ('<path d="M290 560 Q300 500 318 520 Q326 470 344 512 Q356 486 370 560Z" fill="#F28C38"/><path d="M308 560 Q318 524 330 536 Q340 508 352 560Z" fill="#F7D046"/>'
                  + stroke("M280 560 l90 -10 M286 548 l84 10", WOOD_D, 7) if fire else ""))
    out.append(f'<rect x="470" y="150" width="130" height="120" rx="10" fill="{WOOD_D}"/><rect x="480" y="160" width="110" height="100" rx="6" fill="#9FD6EE"/>'
               f'<rect x="480" y="222" width="110" height="38" fill="{SEA}"/><path d="M520 222 Q550 204 590 216 V222 H520Z" fill="{HILL_S}"/>'
               + stroke("M535 160 V260 M480 210 H590", WOOD_D, 6))
    return out


# ================================================================ pages
def boat(x: float, y: float) -> str:
    """A tiny fishing boat, to show how big the giants are next to the sea."""
    return (f'<g transform="translate({x} {y})" filter="url(#p)"><path d="M-16 0 L16 0 L11 7 L-11 7Z" fill="#C8463A"/>'
            '<rect x="-1" y="-24" width="2.4" height="24" fill="#5A3B22"/><path d="M2 -22 L14 -3 L2 -3Z" fill="#fff"/></g>')


STONES_ALL = path_stones(244, 628)

# 01 cover
svg(1, "Finn McCool and the Giant's Causeway",
    "Paper-cut cover: the giant Finn McCool, with ginger hair and a green tunic, stands out in the sea on a path of six-sided stepping stones, carrying another stone in his arms and smiling. Behind him the path runs back to a green Irish cliff, where his wife Oonagh, in a purple dress with a long plait, waves. A tiny red fishing boat bobs on the sea far smaller than Finn's boot, the purple hills of Scotland lie across the water, and seagulls fly overhead.",
    DAY, outdoor(stones=path_stones(244, 484), sky=[gulls([(300, 120), (340, 100), (620, 150)])], back=[boat(590, 420)],
                 people=[person(100, CLIFF, "oonagh", "wave", "smile", 1), person(420, PATH, "finn", "carry", "smile", 1, item=carried_stone())]))

# 02 Finn and Oonagh by their giant house; tiny sheep at their feet
house = (f'<g filter="url(#p)"><rect x="486" y="270" width="280" height="270" fill="#FBF7EF"/>'
         f'<path d="M466 284 Q470 190 626 176 Q782 190 786 284Z" fill="#D9B45A"/></g>'
         + stroke("M490 252 Q626 236 762 252 M500 226 Q626 206 752 226", "#B8913E", 3)
         + f'<path d="M590 540 V340 Q590 304 626 304 Q662 304 662 340 V540Z" fill="{WOOD}"/>' + stroke("M614 316 V540 M638 316 V540", WOOD_D, 3)
         + f'<rect x="506" y="330" width="58" height="60" rx="6" fill="{WOOD_D}"/><rect x="512" y="336" width="46" height="48" fill="#9FD6EE"/>'
         + f'<rect x="690" y="330" width="58" height="60" rx="6" fill="{WOOD_D}"/><rect x="696" y="336" width="46" height="48" fill="#9FD6EE"/>')
ground2 = (f'<path filter="url(#p)" d="M0 520 Q400 500 800 520 V600 H0Z" fill="{GRASS}"/>'
           + stroke("M60 560 l3 -10 M66 560 v-13 M72 560 l-3 -10 M420 570 l3 -10 M426 570 v-13 M432 570 l-3 -10 M740 575 l3 -10 M746 575 v-13 M752 575 l-3 -10", GRASS_D, 3))
svg(2, "Finn and Oonagh",
    "Paper-cut scene: on a green clifftop by the sea, the giant Finn McCool, with ginger hair, freckles and a green tunic, stands smiling next to his wife Oonagh in a purple dress and cream apron, with a long chestnut plait and a yellow flower in her hair. Behind them is their big white house with a golden thatched roof. Four tiny sheep graze around their feet, no bigger than the giants' boots.",
    DAY, [cloud(150, 80, 1), cloud(420, 60, .8), SCOT_HILLS, sea(330), house, ground2,
          sheep(60, 548), sheep(250, 556), sheep(420, 552), sheep(450, 580),
          person(160, 545, "finn", "down", "smile", .5), person(340, 548, "oonagh", "down", "smile", -.5)])

# 03 Finn looks out across the sea at Scotland
svg(3, "Across the sea to Scotland",
    "Paper-cut scene: Finn McCool stands on the green Irish cliff, shading his eyes with one hand, looking out across the empty blue sea at the purple hills of Scotland on the other side. Two tiny fishing boats sail on the sea. There is no path yet.",
    DAY, outdoor(sky=[gulls([(420, 150), (460, 130)])], back=[boat(380, 420), boat(560, 452)],
                 people=[person(110, CLIFF, "finn", "shade", "smile", 1.4)]))

# 04 Finn builds the stepping-stone path
svg(4, "Stomp, stomp, stomp!",
    "Paper-cut scene: Finn McCool stands out in the sea on a row of six-sided stepping stones that runs from the Irish cliff, laughing, carrying a new stone in his arms to add to the end of the path. Little splash marks fly up by his boots. A tiny fishing boat sails nearby, and Scotland's purple hills wait across the water.",
    DAY, outdoor(stones=path_stones(244, 484), back=[boat(600, 430)], people=[person(380, PATH, "finn", "carry", "laugh", 1, item=carried_stone())],
                 front=[marks(["M318 470 l-12 -10", "M442 470 l12 -10", "M322 486 l-14 0", "M438 486 l14 0"], "#fff", 4)]))

# 05 Finn sees Benandonner, who is even bigger
svg(5, "Benandonner",
    "Paper-cut scene: the stepping-stone path now reaches almost all the way across the sea. Finn McCool stands on it, eyes wide and mouth in a round 'oh', hands on his cheeks. On the Scottish shore stands Benandonner, a giant even bigger than Finn, with a bushy dark beard, a blue tunic and a red tartan kilt, hands on his hips, booming across the water.",
    DAY, outdoor(stones=path_stones(244, 628),
                 people=[person(400, PATH, "finn", "cheeks", "oh", 1.4), person(676, SHORE, "ben", "hips", "boom", -1.4)],
                 front=[marks(["M574 150 q-12 -10 0 -24", "M558 166 q-22 -18 0 -50"], INK, 3.6)]))

# 06 Finn runs home; Benandonner stomps onto the path
svg(6, "Oonagh! Oonagh!",
    "Paper-cut scene: Finn McCool runs back along the stepping stones towards the Irish cliff, looking worried, where Oonagh waits with her hands on her cheeks. Behind him, at the Scottish end of the path, the huge giant Benandonner has started to stomp across the sea.",
    DAY, outdoor(stones=STONES_ALL,
                 people=[person(96, CLIFF, "oonagh", "cheeks", "oh", 1), person(310, PATH, "finn", "run", "worry", -1.4, pose="run"),
                         person(630, PATH, "ben", "down", "smile", -1)],
                 front=[marks(["M418 280 h40", "M412 310 h52", "M420 340 h36"], INK, 3.4),
                        marks(["M546 470 l-14 -12", "M714 470 l14 -12"], "#fff", 4)]))

# 07 Finn in a bonnet, tucked into a giant cradle
svg(7, "The giant baby",
    "Paper-cut scene: inside the giant house, Finn McCool lies tucked into an enormous wooden rocking cradle, wearing a frilly white baby bonnet tied with a pink bow, a blue patchwork blanket over him, smiling. Oonagh stands beside the cradle, reaching out to tuck him in. A fire glows in the stone fireplace.",
    INDOOR, [*room(), person(350, 560, "oonagh", "tuck", "smile", 1.4, k=IN), cradle(630, 560, "lie")])

# 08 Oonagh bakes griddle cakes and hides a stone in one
table8 = (f'<g filter="url(#p)"><rect x="330" y="420" width="146" height="16" rx="4" fill="{WOOD_D}"/><rect x="344" y="436" width="14" height="124" fill="{WOOD_D}"/><rect x="448" y="436" width="14" height="124" fill="{WOOD_D}"/></g>'
          + cake(392, 404, 18) + cake(428, 404, 18) + cake(464, 404, 18))
svg(8, "Griddle cakes",
    "Paper-cut scene: inside the giant house, Oonagh stands in front of the fireplace next to a wooden table with three round golden griddle cakes on it. In her hand she holds a fourth cake with a flat grey stone pressed into its middle, and she smiles a secret smile. Over in the giant cradle, Finn in his baby bonnet peeks out to watch.",
    INDOOR, [*room(), person(250, 560, "oonagh", "bake", "smile", 1, k=IN), table8, cake(352, 404, 22, stone=True), cradle(630, 560, "lie")])

# 09 Benandonner stoops to look in at the door
ben_peek = (f'<g transform="translate(116 312) rotate(-14) scale({SIZE["ben"] * IN})" filter="url(#p)">'
            f'<path d="M-62 40 Q0 20 62 40 L72 220 H-72Z" fill="{BEN_TUNIC}"/>' + stroke("M-14 26 L0 50 L14 26", BEN_TUNIC_D, 4)
            + f'<rect x="-12" y="20" width="24" height="26" fill="{SKIN_D["ben"]}"/><g>{head("ben", "smile", 1.4)}</g></g>')
hand9 = f'<circle cx="198" cy="320" r="19" fill="{SKIN["ben"]}" filter="url(#p)"/>' + stroke("M184 308 h-12 M182 320 h-14 M184 332 h-12", SKIN_D["ben"], 3)
svg(9, "Knock, knock!",
    "Paper-cut scene: inside the giant house, the front door stands open and the huge giant Benandonner bends down to peer in. His big bearded face and blue shoulders fill the whole doorway, and one big hand holds the door frame. Oonagh stands in the room with a finger to her lips, and in the giant cradle Finn, in his baby bonnet, pretends to be asleep.",
    INDOOR, [*room(True, ben_peek), hand9, person(380, 560, "oonagh", "shh", "shh", -1, k=IN), cradle(630, 560, "sleep")])

# 10 CRUNCH! Ouch, too hard!
held_cake = cake(-70, -172, 24, bitten=True)
plate = '<ellipse cx="0" cy="-150" rx="50" ry="10" fill="#fff" stroke="#C9C1B5" stroke-width="3"/>' + cake(-18, -162, 15) + cake(16, -162, 15)
svg(10, "Ouch! Too hard!",
    "Paper-cut scene: inside the giant house, Benandonner stands by the door, so tall his head reaches right up to the roof beams. He holds out a bitten griddle cake with a grey stone showing in the bite, and rubs his cheek with his other hand, one eye squeezed shut: ouch! A little yellow star pops out by his cheek. Oonagh holds a plate of cakes and smiles, and Finn peeks from the giant cradle.",
    INDOOR, [*room(fire=False), person(194, 560, "ben", "ouch", "ouch", 1, k=IN, item=held_cake),
             marks(["M278 150 l20 -12", "M284 176 l24 0", "M278 202 l20 12"], INK, 3.6),
             f'<g fill="{GOLD}" filter="url(#p)"><path d="M308 116 l5 11 l12 1 l-9 8 l3 12 l-11 -7 l-11 7 l3 -12 l-9 -8 l12 -1Z"/></g>',
             person(402, 560, "oonagh", "carry", "smile", -1, item=plate, k=IN), cradle(630, 560, "lie")])

# 11 WAAH! The baby sits up
svg(11, "WAAH!",
    "Paper-cut scene: inside the giant house, the enormous baby, Finn in his frilly bonnet and white nightie, sits up in the giant cradle with his arms in the air, crying WAAH with his mouth wide open. Benandonner leaps back in surprise with both hands up, his eyes wide. Oonagh stands by the door with a little smile.",
    INDOOR, [*room(fire=False), person(96, 560, "oonagh", "down", "smile", 1, k=IN), person(330, 560, "ben", "up", "shock", 1.4, k=IN),
             cradle(630, 560, "sit"), marks(["M508 236 l-14 -12", "M506 262 l-18 0", "M508 288 l-14 12", "M752 196 l16 -14", "M760 224 l20 -4"], INK, 4)])

# 12 Benandonner runs home, kicking the stones away
flying = (f'<g transform="translate(370 330) rotate(-24)" filter="url(#p)">{hexstone(0, 0, 44, 36)}</g>'
          f'<g transform="translate(440 260) rotate(18)" filter="url(#p)">{hexstone(0, 0, 44, 36)}</g>'
          f'<g transform="translate(316 386) rotate(40)" filter="url(#p)">{hexstone(0, 0, 40, 32)}</g>')
svg(12, "Stomp, stomp, stomp, home!",
    "Paper-cut scene: Benandonner runs back across the sea towards Scotland as fast as he can, looking back over his shoulder in a worry. Behind him the stepping stones he has kicked away fly up into the air and land with big white splashes, leaving a gap in the path. The part of the path near the Irish cliff is still there.",
    DAY, outdoor(stones=path_stones(244, 292) + path_stones(484, 628),
                 people=[person(570, PATH, "ben", "run", "worry", 1.4, pose="run", flip=True)], cloud2=290,
                 back=[splash(360, 500, 1.1), splash(430, 500, .9)],
                 front=[flying]))

# 13 The Giant's Causeway is still there today
causeway = ""
for y0, xs in [(418, range(346, 400, 34)), (440, range(330, 470, 34)), (462, range(346, 540, 34)), (486, range(330, 600, 34))]:
    for i, cx in enumerate(xs):
        causeway += hexstone(cx, y0 + (i % 3) * 5, 36, 70)
scot_stub = "".join(hexstone(x, 462 + (i % 2) * 6, 30, 50) for i, x in enumerate(range(660, 730, 28)))
cliff13 = (f'<path filter="url(#p)" d="M-10 412 L316 412 L326 470 L306 600 H-10Z" fill="{ROCK}"/>'
           + stroke("M40 440 v60 M110 450 v90 M170 436 v70 M70 520 v60 M240 444 v80 M290 470 v60", ROCK_D, 3)
           + f'<path d="M-10 394 Q150 388 318 400 L320 418 Q150 410 -10 418Z" fill="{GRASS}"/>')
bonnet_in_hand = (f'<g transform="translate(90 -300)">'
                  + "".join(f'<circle cx="{a}" cy="{b}" r="7" fill="#fff"/>' for a, b in [(-24, 4), (-22, -10), (-12, -20), (0, -24), (12, -20), (22, -10), (24, 4)])
                  + '<path d="M-24 6 Q-26 -26 0 -26 Q26 -26 24 6Z" fill="#FDFBF5"/>' + stroke("M-18 6 L-24 40 M18 6 L26 38", "#F4B6C8", 4) + '</g>')
svg(13, "The Giant's Causeway",
    "Paper-cut scene: in warm golden evening light, Finn McCool, back in his green tunic and waving the baby bonnet over his head, and Oonagh stand on the Irish cliff, laughing together. At the foot of the cliff, a crowd of six-sided stone columns steps down into the sea: all that is left of the path, the Giant's Causeway. Far across the water, a few more columns stand at the Scottish shore.",
    GOLDEN, ['<circle cx="600" cy="230" r="46" fill="#FFE29A"/>', cloud(160, 90, .9, .7), SCOT_HILLS, sea(), cliff13, SCOT_SHORE,
             f'<g filter="url(#p)">{causeway}</g>', f'<g filter="url(#p)">{scot_stub}</g>',
             person(88, CLIFF, "oonagh", "down", "laugh", 1),
             person(250, CLIFF + 2, "finn", "wave", "laugh", -1, item=bonnet_in_hand),
             front_wave(530)])
