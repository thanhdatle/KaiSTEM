"""Shared character and scenery drawers for the Lạc Long Quân and Âu Cơ book (used by lac_gen.py).

Every character is drawn once here and only placed/scaled by the page script, so colours and shapes
never drift between pages. Origins are at the feet (people, animals) or the base (houses, trees).
Base heights at k=1: Lạc Long Quân ~290 with his plumes, Âu Cơ ~285 with her feather crown,
grown-up villagers ~250, one of the hundred children ~128, a "tiny" crowd child ~58.
Clothes and buildings borrow Đông Sơn bronze-drum motifs: feather headdresses, ring-and-zigzag bands,
stilt houses with saddle roofs, long boats with bird-head prows, a many-rayed star, long-billed birds.
"""
import math

INK, CREAM = "#2B2320", "#FFF6E6"
SKIN, SKIN_D, HAIR, BLUSH = "#C98A5E", "#A86E46", "#231915", "#F0705F"
TEAL, TEAL_D, TEAL_L, GOLD, GOLD_D = "#2E9C9A", "#1F7472", "#7FD1C8", "#E8B64A", "#B98A2A"
KILT, KILT_D = "#2F5C8A", "#22466C"
ROSE, ROSE_D, PEACH, FEATHER, FEATHER_D = "#E2738A", "#B9506A", "#F6C6A6", "#FFFFFF", "#CBD2DE"
JADE, JADE_D, BELLY, CREST = "#3BA776", "#22754F", "#F2D27A", "#E9573F"
WOOD, WOOD_D, WOOD_L, THATCH, THATCH_D = "#9C6B3F", "#6E4626", "#C9995F", "#C79A55", "#9A7238"
BRONZE, BRONZE_D, BRONZE_L = "#B98A4A", "#8A6230", "#E0B56A"
SEA, SEA_D, SEA_L = "#3F86B8", "#2C6A98", "#8CC4E6"
SAND, SAND_D = "#EED9A8", "#D9BE84"
GRASS, GRASS_D, GRASS_L = "#7CC46A", "#4E9A4E", "#A6DA84"
HILL_N, HILL_F, HILL_FF = "#5FA872", "#8CC7A0", "#B6DDC6"
PADDY, PADDY_L = "#9CCBD3", "#D3EEF0"
EGG, EGG_D = "#FFF8EC", "#E6D4B5"
BOC, BOC_D, BOC_L = "#F9E3EA", "#E2B6C4", "#FFFFFF"
FISHM, FISHM_D, FIN = "#6F84AE", "#4F628C", "#E58A4A"
FOX, FOX_D, FOX_L = "#E8843A", "#B95E22", "#FFF1DE"
BARK, BARK_D, LEAF, LEAF_D = "#8A6440", "#62462C", "#3F8E4E", "#2E6E3C"
KID_COLS = ("#E36B5B", "#F2B53A", "#5BA6D6", "#7CBF5A", "#B07CC6", "#F08FB0", "#3FA9A0", "#E0874A")
TUNICS = {"m1": ("#C8875A", "#9C6440"), "m2": ("#7A9A5A", "#5A7A3E"), "w1": ("#B9A06A", "#8E7646"), "w2": ("#A97AA0", "#80577A"),
          "w3": ("#D9806A", "#AE5B48"), "m3": ("#8C7AB0", "#665689")}


def stroke(d: str, col: str = INK, w: float = 5, extra: str = "") -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def group(x: float, y: float, s: float, inner: str, flip: bool = False, shadow: bool = True, rot: float = 0) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def arm(sx: float, sy: float, hx: float, hy: float, col: str, w: float = 12, skin: str = SKIN) -> str:
    side = -1 if hx < sx else 1
    mx, my = (sx + hx) / 2 + side * 8, (sy + hy) / 2 + 10
    return stroke(f"M{sx} {sy} Q{mx} {my} {hx} {hy}", col, w) + f'<circle cx="{hx}" cy="{hy}" r="{w * .62:.1f}" fill="{skin}"/>'


def band(x0: float, x1: float, y: float, col: str, bg: str) -> str:
    """A Đông Sơn style decorative band: a strip with little rings and a zig-zag."""
    n = max(2, int((x1 - x0) / 14))
    rings = "".join(f'<circle cx="{x0 + (i + .5) * (x1 - x0) / n:.1f}" cy="{y}" r="2.6" fill="none" stroke="{col}" stroke-width="1.6"/>' for i in range(n))
    zz = "M" + " L".join(f"{x0 + i * (x1 - x0) / (2 * n):.1f} {y + (5 if i % 2 else 9)}" for i in range(2 * n + 1))
    return f'<rect x="{x0}" y="{y - 5}" width="{x1 - x0}" height="16" fill="{bg}"/>' + rings + stroke(zz, col, 1.6)


def sparkles(pts: list, col: str = "#FFF3B0") -> str:
    return "".join(f'<path transform="translate({x} {y}) scale({s})" d="M0 -12 L3 -3 L12 0 L3 3 L0 12 L-3 3 L-12 0 L-3 -3Z" fill="{col}"/>'
                   for x, y, s in pts)


# ---------------------------------------------------------------- faces
def face(cy: float, r: float, mood: str, look: float = 0) -> str:
    ex, ey = r * .36, cy - r * .08
    if mood in ("calm", "big", "proud"):
        eyes = stroke(f"M{-ex - 6:.1f} {ey:.1f} q6 -7 12 0 M{ex - 6:.1f} {ey:.1f} q6 -7 12 0", INK, 3)
    else:
        er = 5 if r > 24 else 3.6
        eyes = "".join(f'<circle cx="{a:.1f}" cy="{ey:.1f}" r="{er}" fill="#fff"/><circle cx="{a + 1 + look:.1f}" cy="{ey + 1:.1f}" r="{er * .6:.1f}" fill="{INK}"/>' for a in (-ex, ex))
    brows = ""
    if mood == "worry":
        brows = stroke(f"M{-ex - 7:.1f} {ey - 9:.1f} l12 -4 M{ex + 7:.1f} {ey - 9:.1f} l-12 -4", INK, 2.6)
    elif mood == "call":  # raised, happy brows
        brows = stroke(f"M{-ex - 7:.1f} {ey - r * .3:.1f} q7 -6 14 0 M{ex - 7:.1f} {ey - r * .3:.1f} q7 -6 14 0", INK, 2.4)
    mo, my = r * .3, cy + r * .45
    mouths = {"smile": stroke(f"M{-mo:.1f} {my - 2:.1f} q{mo:.1f} {r * .3:.1f} {2 * mo:.1f} 0", INK, 2.8),
              "big": f'<path d="M{-mo - 2:.1f} {my - 4:.1f} Q0 {my - 2:.1f} {mo + 2:.1f} {my - 4:.1f} Q{mo:.1f} {my + r * .38:.1f} 0 {my + r * .38:.1f} Q{-mo:.1f} {my + r * .38:.1f} {-mo - 2:.1f} {my - 4:.1f}Z" fill="#5A2E22"/>',
              "oh": f'<ellipse cy="{my:.1f}" rx="{r * .18:.1f}" ry="{r * .22:.1f}" fill="#5A2E22"/>',
              "worry": stroke(f"M{-mo:.1f} {my + 2:.1f} q{mo * .5:.1f} -4 {mo:.1f} 0 q{mo * .5:.1f} 4 {mo:.1f} 0", INK, 2.6),
              "wistful": stroke(f"M{-mo * .7:.1f} {my:.1f} q{mo * .7:.1f} {r * .14:.1f} {mo * 1.4:.1f} 0", INK, 2.6)}
    mouths["calm"] = mouths["proud"] = mouths["smile"]
    mouths["call"] = mouths["big"]
    cheeks = (f'<circle cx="{-r * .62:.1f}" cy="{cy + r * .3:.1f}" r="{r * .2:.1f}" fill="{BLUSH}" opacity=".4"/>'
              f'<circle cx="{r * .62:.1f}" cy="{cy + r * .3:.1f}" r="{r * .2:.1f}" fill="{BLUSH}" opacity=".4"/>')
    return eyes + brows + cheeks + mouths[mood]


def cupped(mx: float, my: float, gap: float, r: float) -> str:
    """Two hands cupped beside an open mouth, plus three call arcs going out to the right (mirror with flip)."""
    hands = "".join(f'<path d="M{mx + d * gap:.1f} {my - r * 1.3:.1f} Q{mx + d * (gap + r * 1.1):.1f} {my:.1f} {mx + d * gap:.1f} {my + r * 1.3:.1f}" '
                    f'stroke="{SKIN_D}" stroke-width="{r * .9:.1f}" fill="none" stroke-linecap="round"/>' for d in (-1, 1))
    arcs = "".join(stroke(f"M{mx + gap + r * (2.2 + i * 1.6):.1f} {my - r * (1 + i * .55):.1f} q{r * (.9 + i * .3):.1f} {r * (1 + i * .55):.1f} 0 {r * (2 + i * 1.1):.1f}",
                          "#FFFFFF", r * .5) for i in range(3))
    return hands + arcs


# ---------------------------------------------------------------- grown-ups
HANDS = {"down": ((-44, -100), (44, -100)), "wave": ((-44, -100), (62, -238)), "up": ((-66, -236), (66, -236)),
         "point": ((-44, -100), (84, -176)), "hold": ((-22, -126), (22, -126)), "open": ((-80, -152), (80, -152)),
         "call": ((-30, -190), (30, -190)), "chain": ((-58, -104), (58, -104)), "khen": ((-4, -172), (26, -176)), "low": ((-30, -78), (30, -78)), "reach": ((-44, -100), (82, -128)),
         "plant": ((-26, -40), (40, -90)), "hip": ((-30, -112), (30, -112)), "ladle": ((-22, -126), (70, -120)),
         "left": ((-82, -128), (44, -100))}
FACE_Y, HEAD_R = -206, 30


def _legs(col: str = SKIN) -> str:
    return (stroke("M-13 -72 V-8 M13 -72 V-8", col, 13)
            + f'<ellipse cx="-16" cy="-5" rx="13" ry="6" fill="{col}"/><ellipse cx="16" cy="-5" rx="13" ry="6" fill="{col}"/>')


def _head(mood: str, look: float = 0) -> str:
    return f'<rect x="-8" y="-186" width="16" height="18" fill="{SKIN}"/><circle cy="{FACE_Y}" r="{HEAD_R}" fill="{SKIN}"/>' + face(FACE_Y, HEAD_R, mood, look)


def _hair_cap() -> str:
    return f'<path d="M-30 -212 Q-32 -240 0 -240 Q32 -240 30 -212 Q18 -230 0 -228 Q-18 -230 -30 -212Z" fill="{HAIR}"/>'


def llq(x: float, y: float, k: float = 1, arms: str = "down", mood: str = "smile", look: float = 0, flip: bool = False) -> str:
    """Lạc Long Quân as a man: teal tunic with a gold wave band, blue kilt, a gold star pendant, three teal plumes."""
    (lx, ly), (rx, ry) = HANDS[arms]
    o = _legs()
    o += f'<path d="M-36 -114 L36 -114 L42 -60 L-42 -60Z" fill="{KILT}"/>' + stroke("M-40 -66 q7 -7 14 0 q7 7 14 0 q7 -7 14 0 q7 7 14 0 q7 -7 14 0 q7 7 14 0", TEAL_L, 3)
    o += f'<path d="M-38 -168 Q0 -178 38 -168 L40 -108 Q0 -100 -40 -108Z" fill="{TEAL}"/>'
    o += stroke("M-39 -118 q8 -8 16 0 q8 8 16 0 q8 -8 16 0 q8 8 16 0 q8 -8 16 0", GOLD, 4)
    o += _head(mood, look) + _hair_cap() + f'<circle cy="-246" r="12" fill="{HAIR}"/>'
    o += "".join(f'<ellipse cx="{a}" cy="{b}" rx="8" ry="26" fill="{TEAL}" transform="rotate({r} {a} {b})"/>'
                 + stroke(f"M{a} {b + 20} L{a + r * .25:.1f} {b - 18}", TEAL_L, 2) for a, b, r in ((-18, -256, -22), (0, -266, 0), (18, -256, 22)))
    o += f'<rect x="-28" y="-238" width="56" height="9" rx="4" fill="{GOLD}"/>'
    o += arm(-34, -160, lx, ly, TEAL) + arm(34, -160, rx, ry, TEAL)
    o += f'<circle cx="-34" cy="-160" r="12" fill="{TEAL}"/><circle cx="34" cy="-160" r="12" fill="{TEAL}"/>'
    o += f'<circle cy="-150" r="9" fill="{GOLD}"/>' + star_poly(0, -150, 7, 3, 8, GOLD_D)
    if arms == "call":
        o += cupped(0, -192, 14, 8)
    return group(x, y, k, o, flip)


def auco(x: float, y: float, k: float = 1, arms: str = "down", mood: str = "smile", look: float = 0, flip: bool = False,
         held: str = "") -> str:
    """Âu Cơ, the fairy of the mountains: long hair, a white crane-feather crown with flowers, peach top, rose wrap skirt."""
    (lx, ly), (rx, ry) = HANDS[arms]
    o = f'<path d="M-32 -220 Q-44 -170 -36 -118 L36 -118 Q44 -170 32 -220Z" fill="{HAIR}"/>'
    o += stroke("M-11 -40 V-8 M11 -40 V-8", SKIN, 11)
    o += f'<ellipse cx="-14" cy="-5" rx="12" ry="6" fill="{SKIN}"/><ellipse cx="14" cy="-5" rx="12" ry="6" fill="{SKIN}"/>'
    o += f'<path d="M-32 -124 L32 -124 L46 -24 Q0 -14 -46 -24Z" fill="{ROSE}"/>' + band(-44, 44, -40, CREAM, ROSE_D)
    o += f'<path d="M-34 -168 Q0 -176 34 -168 L34 -120 Q0 -114 -34 -120Z" fill="{PEACH}"/>' + stroke("M-33 -132 H33", ROSE_D, 4)
    o += _head(mood, look) + _hair_cap()
    o += "".join(f'<ellipse cx="{a}" cy="{b}" rx="7" ry="24" fill="{FEATHER}" stroke="{FEATHER_D}" stroke-width="1.6" transform="rotate({r} {a} {b})"/>'
                 for a, b, r in ((-26, -244, -40), (-13, -256, -20), (0, -262, 0), (13, -256, 20), (26, -244, 40)))
    o += f'<rect x="-30" y="-238" width="60" height="9" rx="4" fill="{ROSE_D}"/>'
    o += "".join(flower(a, -234, .8, c) for a, c in ((-22, "#F08FB0"), (0, "#F7D046"), (22, "#F08FB0")))
    o += arm(-30, -160, lx, ly, PEACH, 11) + arm(30, -160, rx, ry, PEACH, 11)
    o += f'<circle cx="-30" cy="-160" r="11" fill="{PEACH}"/><circle cx="30" cy="-160" r="11" fill="{PEACH}"/>'
    if held == "flower":
        o += flower(rx + 4, ry - 10, 1.3, "#F08FB0")
    if arms == "call":
        o += cupped(0, -192, 14, 8)
    return group(x, y, k, o, flip)


def villager(x: float, y: float, k: float = 1, who: str = "m1", arms: str = "down", mood: str = "smile", look: float = 0,
             flip: bool = False, held: str = "") -> str:
    """Lạc villagers: tunics in earthy colours with a Đông Sơn band; men have a topknot, women a high bun."""
    col, dk = TUNICS[who]
    (lx, ly), (rx, ry) = HANDS[arms]
    o = _legs()
    if who.startswith("w"):
        o += f'<circle cx="0" cy="-238" r="13" fill="{HAIR}"/>'
        o += f'<path d="M-30 -118 L30 -118 L40 -26 Q0 -18 -40 -26Z" fill="{dk}"/>' + band(-38, 38, -44, CREAM, dk)
    else:
        o += f'<path d="M-32 -112 L32 -112 L38 -62 L-38 -62Z" fill="{dk}"/>' + band(-36, 36, -74, CREAM, dk)
        o += f'<circle cy="-244" r="10" fill="{HAIR}"/>'
    o += f'<path d="M-34 -168 Q0 -176 34 -168 L36 -110 Q0 -104 -36 -110Z" fill="{col}"/>'
    o += _head(mood, look) + _hair_cap()
    o += arm(-30, -160, lx, ly, col, 11) + arm(30, -160, rx, ry, col, 11)
    if held == "seedling":
        o += rice_tuft(rx, ry + 4, .8)
    elif held == "post":
        o += f'<rect x="{rx - 7}" y="{ry - 120}" width="14" height="170" rx="4" fill="{WOOD}"/>'
    elif held == "khen":
        o += (stroke("M6 -188 L40 -258 M12 -186 L50 -250 M0 -188 L28 -264 M18 -184 L60 -238", "#C9B07A", 5)
              + f'<ellipse cx="10" cy="-182" rx="16" ry="11" fill="{THATCH_D}"/>')
    elif held == "bowl":
        o += f'<path d="M{rx - 18} {ry - 6} Q{rx} {ry + 20} {rx + 18} {ry - 6}Z" fill="{BRONZE_L}"/>'
    if arms == "call":
        o += cupped(0, -192, 14, 8)
    return group(x, y, k, o, flip)


def king(x: float, y: float, k: float = 1, arms: str = "open", mood: str = "big") -> str:
    """The first Hùng King, grown up: a tall Đông Sơn feather crown of white (fairy) and teal (dragon) plumes, gold tunic."""
    (lx, ly), (rx, ry) = HANDS[arms]
    o = _legs()
    o += f'<path d="M-36 -114 L36 -114 L42 -56 L-42 -56Z" fill="{KILT}"/>' + band(-40, 40, -74, GOLD, KILT_D)
    o += f'<path d="M-38 -168 Q0 -178 38 -168 L40 -108 Q0 -100 -40 -108Z" fill="{GOLD}"/>' + band(-39, 39, -128, ROSE_D, GOLD_D)
    o += _head(mood) + _hair_cap()
    plumes = ((-36, -256, -44, TEAL), (-22, -272, -26, FEATHER), (-8, -282, -9, TEAL), (8, -282, 9, FEATHER), (22, -272, 26, TEAL),
              (36, -256, 44, FEATHER))
    o += "".join(f'<ellipse cx="{a}" cy="{b}" rx="8" ry="34" fill="{c}" stroke="{FEATHER_D if c == FEATHER else TEAL_D}" stroke-width="1.6" transform="rotate({r} {a} {b})"/>'
                 for a, b, r, c in plumes)
    o += f'<rect x="-32" y="-242" width="64" height="14" rx="5" fill="{GOLD}"/>' + star_poly(0, -235, 6, 2.6, 8, GOLD_D)
    o += arm(-34, -160, lx, ly, GOLD) + arm(34, -160, rx, ry, GOLD)
    o += f'<circle cx="-34" cy="-160" r="12" fill="{GOLD}"/><circle cx="34" cy="-160" r="12" fill="{GOLD}"/>'
    return group(x, y, k, o)


# ---------------------------------------------------------------- the hundred children
KID_HANDS = {"down": ((-28, -36), (28, -36)), "up": ((-36, -114), (36, -114)), "wave": ((-28, -36), (38, -114)),
             "bowl": ((-14, -52), (14, -52)), "call": ((-20, -84), (20, -84)), "chain": ((-30, -104), (30, -104)), "hold": ((-30, -60), (30, -60))}


def kid(x: float, y: float, k: float = 1, c: int = 0, arms: str = "down", mood: str = "smile", flip: bool = False) -> str:
    """One of the hundred children: round face, black hair with a little topknot, a bright tunic (colour c)."""
    col = KID_COLS[c % len(KID_COLS)]
    (lx, ly), (rx, ry) = KID_HANDS[arms]
    o = stroke("M-8 -34 V-6 M8 -34 V-6", SKIN, 9) + f'<ellipse cx="-10" cy="-4" rx="8" ry="4" fill="{SKIN}"/><ellipse cx="10" cy="-4" rx="8" ry="4" fill="{SKIN}"/>'
    o += f'<path d="M-20 -72 Q0 -76 20 -72 L25 -30 Q0 -26 -25 -30Z" fill="{col}"/>' + stroke("M-23 -38 H23", CREAM, 3)
    o += f'<rect x="-5" y="-80" width="10" height="8" fill="{SKIN}"/><circle cy="-96" r="22" fill="{SKIN}"/>' + face(-96, 22, mood)
    o += f'<path d="M-22 -100 Q-23 -120 0 -120 Q23 -120 22 -100 Q12 -112 0 -111 Q-12 -112 -22 -100Z" fill="{HAIR}"/><circle cy="-122" r="6" fill="{HAIR}"/>'
    o += arm(-18, -66, lx, ly, col, 8) + arm(18, -66, rx, ry, col, 8)
    if arms == "call":
        o += cupped(0, -86, 10, 6)
    if arms == "bowl":
        o += f'<path d="M-20 -58 Q0 -30 20 -58Z" fill="{BRONZE_L}"/><ellipse cy="-60" rx="14" ry="5" fill="#fff"/>'
    return group(x, y, k, o, flip)


def tiny(x: float, y: float, s: float = 1, c: int = 0, wave: bool = False) -> str:
    """A crowd-size child (same colours as kid()), for pages that show all fifty or all hundred."""
    col = KID_COLS[c % len(KID_COLS)]
    a = (stroke("M8 -30 L17 -50", col, 4.5) + f'<circle cx="17" cy="-51" r="3" fill="{SKIN}"/>') if wave else stroke("M9 -30 L12 -16", col, 4.5)
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.2f})">' + stroke("M-4 -14 V-1 M4 -14 V-1", SKIN, 4)
            + f'<path d="M-9 -34 L9 -34 L12 -13 L-12 -13Z" fill="{col}"/>' + stroke("M-9 -30 L-12 -16", col, 4.5) + a
            + f'<circle cy="-43" r="10" fill="{SKIN}"/><path d="M-10 -45 Q-10 -54 0 -54 Q10 -54 10 -45 Q5 -50 0 -50 Q-5 -50 -10 -45Z" fill="{HAIR}"/>'
            f'<circle cy="-56" r="3" fill="{HAIR}"/><circle cx="-3.4" cy="-43" r="1.5" fill="{INK}"/><circle cx="3.4" cy="-43" r="1.5" fill="{INK}"/>'
            + stroke("M-3 -38.5 q3 2.4 6 0", INK, 1.2) + '</g>')


def crowd(n: int, x0: float, x1: float, y_back: float, y_front: float, rows: int, s_back: float, s_front: float,
          wave_every: int = 3, start: int = 0) -> str:
    """Exactly n tiny children in `rows` rows, back (smaller, higher) to front. Rows are staggered."""
    per = [n // rows + (1 if i < n % rows else 0) for i in range(rows)]
    out, idx = [], start
    for r, m in enumerate(per):
        t = r / max(1, rows - 1)
        yy, ss = y_back + (y_front - y_back) * t, s_back + (s_front - s_back) * t
        step = (x1 - x0) / m
        for i in range(m):
            xx = x0 + step * (i + .5) + (step * .25 if r % 2 else -step * .1)
            out.append(tiny(xx, yy, ss, idx * 3 + r, wave=(idx % wave_every == 0)))
            idx += 1
    return f'<g filter="url(#p)">{"".join(out)}</g>'


def along(n: int, pts: list, s0: float, s1: float, start: int = 0) -> str:
    """Exactly n tiny children walking two-by-two along a polyline path (from first point = nearest to last = farthest)."""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    total = sum(lens)
    out = []
    pairs = (n + 1) // 2
    for j in range(n):
        p = j // 2
        d = total * p / max(1, pairs - 1)
        for (a, b), ln in zip(segs, lens):
            if d <= ln or (a, b) == segs[-1]:
                t = min(1, d / ln)
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                break
            d -= ln
        s = s0 + (s1 - s0) * p / max(1, pairs - 1)
        out.append((y, tiny(x + (-9 if j % 2 == 0 else 9) * s, y + (0 if j % 2 == 0 else 3 * s), s, start + j, wave=(j % 4 == 1))))
    out.sort(key=lambda t: t[0])
    return f'<g filter="url(#p)">{"".join(t[1] for t in out)}</g>'


def egg(x: float, y: float, s: float = 1, crack: bool = False) -> str:
    c = stroke("M-10 -16 l5 4 l4 -5 l5 5 l5 -4", "#B9A27E", 1.8) if crack else ""
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"><ellipse cy="-16" rx="12" ry="16" fill="{EGG}" stroke="{EGG_D}" stroke-width="1.6"/>'
            f'<ellipse cx="-4" cy="-22" rx="3" ry="5" fill="#fff"/>{c}</g>')


EGG_ROWS = (15, 14, 14, 13, 12, 11, 9, 7, 5)  # = 100


def egg_pile(x: float, y: float, rows: tuple = EGG_ROWS, dx: float = 25, dy: float = 19, cracked: tuple = ()) -> str:
    """A mound of eggs; the default rows add up to exactly one hundred. `cracked` = (row, index) pairs."""
    out = []
    for r, m in enumerate(rows):
        for i in range(m):
            out.append(egg(x + (i - (m - 1) / 2) * dx, y - r * dy, 1, (r, i) in cracked))
    return f'<g filter="url(#p)">{"".join(out)}</g>'


def baby(x: float, y: float, s: float = 1, c: int = 0) -> str:
    """A just-hatched baby popping out of a broken egg shell, arms up."""
    col = KID_COLS[c % len(KID_COLS)]
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})">' + stroke("M-10 -30 L-20 -50 M10 -30 L20 -50", SKIN, 6)
            + f'<ellipse cy="-26" rx="13" ry="12" fill="{col}"/><circle cy="-44" r="12" fill="{SKIN}"/>'
            f'<circle cy="-57" r="3" fill="{HAIR}"/><circle cx="-4" cy="-45" r="1.7" fill="{INK}"/><circle cx="4" cy="-45" r="1.7" fill="{INK}"/>'
            + stroke("M-4 -39 q4 3 8 0", INK, 1.4)
            + f'<path d="M-16 -22 L-10 -28 L-5 -21 L0 -28 L5 -21 L10 -28 L16 -22 Q16 0 0 0 Q-16 0 -16 -22Z" fill="{EGG}" stroke="{EGG_D}" stroke-width="1.6"/></g>')


def boc(x: float, y: float, s: float = 1, opened: bool = False) -> str:
    """The bọc: a soft, pearly bundle. Opened, its sides fold down like petals (the eggs are drawn separately)."""
    glow = '<ellipse cx="0" cy="-80" rx="170" ry="120" fill="#FFF3B0" opacity=".28"/>'
    if not opened:
        body = (f'<path d="M-110 0 Q-136 -120 -46 -168 Q0 -186 46 -168 Q136 -120 110 0 Q0 22 -110 0Z" fill="{BOC}" stroke="{BOC_D}" stroke-width="3"/>'
                + stroke("M-70 -130 Q-40 -160 0 -164", BOC_L, 8) + stroke("M-80 -40 Q0 -20 80 -40", BOC_D, 2.4))
    else:
        body = (f'<path d="M-40 0 Q-150 4 -206 -50 Q-150 -84 -60 -40Z" fill="{BOC}" stroke="{BOC_D}" stroke-width="3"/>'
                f'<path d="M40 0 Q150 4 206 -50 Q150 -84 60 -40Z" fill="{BOC}" stroke="{BOC_D}" stroke-width="3"/>'
                f'<path d="M-210 -2 Q0 30 210 -2 Q0 14 -210 -2Z" fill="{BOC_D}"/>')
    return group(x, y, s, glow + body)


def banana_mat(x: float, y: float, s: float = 1) -> str:
    def leaf(r: float) -> str:
        return (f'<path transform="rotate({r})" d="M-160 0 Q0 -40 160 0 Q0 30 -160 0Z" fill="#5DB36A"/>'
                f'<path transform="rotate({r})" d="M-156 0 Q0 -6 156 0" stroke="#3E8A4C" stroke-width="3" fill="none"/>')
    return group(x, y, s, leaf(-3) + leaf(4))


# ---------------------------------------------------------------- the dragon
def dragon(x: float, y: float, s: float = 1, rot: float = 0, flip: bool = False, amp: float = 34, length: float = 460,
           waves: float = 1.25, mood: str = "smile") -> str:
    """Lạc Long Quân as a dragon: a long friendly jade body with a gold belly, red crest and tail tuft,
    a flame-like crest on the head (no antlers, like Lý-dynasty dragons), curly whiskers and four small legs. Local origin = middle of the body; head at the right."""
    n = 64
    pts = [(-length / 2 + length * i / n, amp * math.sin(i / n * 2 * math.pi * waves)) for i in range(n + 1)]

    def width(t: float) -> float:
        return 8 + 34 * min(1, t / .55) - (6 if t > .9 else 0)

    def nrm(i: int) -> tuple:
        a, b = pts[max(0, i - 1)], pts[min(n, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        return -dy / ln, dx / ln

    def seg(i: int, col: str, w: float) -> str:
        return (f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[i + 1][0]:.1f}" y2="{pts[i + 1][1]:.1f}" '
                f'stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round"/>')
    out = ""
    for i in range(6, n - 3, 5):  # crest spikes along the back
        t, (nx, ny) = i / n, nrm(i)
        w = width(t) / 2
        bx, by = pts[i][0] - nx * w * .8, pts[i][1] - ny * w * .8
        out += f'<path d="M{bx - 9:.1f} {by:.1f} L{bx - nx * 22:.1f} {by - ny * 22:.1f} L{bx + 9:.1f} {by:.1f}Z" fill="{CREST}"/>'
    for t0 in (.32, .74):  # little legs on the belly side
        i = int(t0 * n)
        nx, ny = nrm(i)
        w = width(t0) / 2
        bx, by = pts[i][0] + nx * w * .6, pts[i][1] + ny * w * .6
        fx, fy = bx + nx * 30 + 10, by + ny * 30
        out += stroke(f"M{bx:.1f} {by:.1f} L{fx:.1f} {fy:.1f}", JADE_D, 11) + stroke(f"M{fx:.1f} {fy:.1f} l8 6 M{fx:.1f} {fy:.1f} l0 9 M{fx:.1f} {fy:.1f} l-7 6", GOLD, 3)
    out += "".join(seg(i, JADE_D, width(i / n) + 6) for i in range(n))
    out += "".join(seg(i, JADE, width(i / n)) for i in range(n))
    belly = [(p[0] + nrm(i)[0] * width(i / n) * .22, p[1] + nrm(i)[1] * width(i / n) * .22) for i, p in enumerate(pts)]
    out += stroke("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in belly[8:n - 2]), BELLY, 9, ' stroke-dasharray="10 5"')
    out += f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f} q-30 -20 -46 -4 q22 0 18 14 q-14 -2 -22 10 q24 2 50 -20Z" fill="{CREST}"/>'
    hx, hy = pts[-1]
    a = math.degrees(math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]))
    mouth = ('<path d="M30 6 Q58 12 74 4 Q60 30 32 18Z" fill="#B23A3A"/>' if mood == "roar" else stroke("M26 10 Q48 20 68 10", INK, 3))
    head = (f'<path d="M-30 -18 L-52 -30 L-42 -8 L-60 -6 L-40 6 L-54 18 L-28 14Z" fill="{CREST}"/>'
            + f'<path d="M24 -20 Q20 -46 4 -58 Q14 -40 2 -34 Q0 -56 -18 -66 Q-8 -46 -18 -36 Q-26 -50 -40 -52 Q-28 -36 -24 -14Z" fill="{CREST}"/>'
            + f'<ellipse cx="0" cy="0" rx="32" ry="28" fill="{JADE}"/><ellipse cx="38" cy="4" rx="38" ry="18" fill="{JADE}"/>'
            + f'<ellipse cx="40" cy="12" rx="30" ry="7" fill="{BELLY}"/>' + mouth
            + f'<circle cx="68" cy="-4" r="3" fill="{JADE_D}"/>'
            + stroke("M70 2 q30 -4 34 -26 q2 -14 -10 -12 M66 10 q26 16 46 6 q12 -8 2 -16", GOLD, 3)
            + f'<circle cx="10" cy="-10" r="10" fill="#fff"/><circle cx="13" cy="-9" r="6" fill="{INK}"/><circle cx="15" cy="-12" r="2.2" fill="#fff"/>'
            + stroke("M0 -24 q10 -6 22 0", JADE_D, 3))
    out += f'<g transform="translate({hx:.1f} {hy:.1f}) rotate({a:.1f})">{head}</g>'
    return group(x, y, s, out, flip, True, rot)


# ---------------------------------------------------------------- the three spirits
def big_fish(x: float, y: float, s: float = 1, mouth: str = "shut", flip: bool = False, mood: str = "grumpy") -> str:
    """Ngư Tinh, the giant fish spirit: slate-blue, orange spiky fins, a row of little fins underneath, a big mouth.
    Facing right. mouth = shut | open | spit."""
    fins = "".join(f'<path d="M{a} 46 q-6 26 10 30 q2 -16 10 -30Z" fill="{FIN}"/>' for a in (-120, -84, -48, -12, 24))
    spikes = "".join(f'<path d="M{a} -50 L{a + 12} -86 L{a + 28} -48Z" fill="{FIN}"/>' for a in (-110, -76, -42, -8, 26))
    tail = f'<path d="M-140 0 L-220 -60 Q-196 0 -220 60Z" fill="{FIN}"/>'
    body = f'<path d="M-150 0 Q-110 -64 20 -58 Q110 -50 150 -8 Q110 50 20 56 Q-110 62 -150 0Z" fill="{FISHM}"/>'
    body += stroke(" ".join(f"M{a} -20 q10 12 0 24" for a in (-90, -60, -30, 0, 30)), FISHM_D, 3)
    body += f'<path d="M60 -40 Q40 0 60 40" stroke="{FISHM_D}" stroke-width="5" fill="none"/>'
    eye = f'<circle cx="92" cy="-20" r="14" fill="#fff"/><circle cx="96" cy="-18" r="7" fill="{INK}"/>'
    eye += stroke("M76 -42 L108 -32" if mood == "grumpy" else "M78 -40 q14 -8 28 0", INK, 5)
    if mouth == "open":
        mo = '<path d="M152 -10 L100 8 L152 34Z" fill="#7A2F3A"/>'
    elif mouth == "spit":
        mo = '<ellipse cx="146" cy="8" rx="8" ry="10" fill="#7A2F3A"/>'
    else:
        mo = stroke("M150 -6 Q130 10 114 6", INK, 4)
    return group(x, y, s, tail + spikes + fins + body + eye + mo, flip)


def _fox_tail(bx: float, by: float, ang: float, ln: float, bend: int) -> str:
    r = math.radians(ang)
    dx, dy, px, py = math.cos(r), math.sin(r), -math.sin(r), math.cos(r)
    m = 24

    def side(sgn: int, t0: float) -> list:
        pts = []
        for j in range(m + 1):
            t = t0 + (1 - t0) * j / m
            off = bend * 13 * math.sin(2 * math.pi * t)
            w = (2 + 9.5 * min(1, t / .7)) * (math.sqrt(max(0, 1 - ((t - .8) / .2) ** 2)) if t > .8 else 1)
            pts.append((bx + dx * ln * t + px * (off + sgn * w), by + dy * ln * t + py * (off + sgn * w)))
        return pts

    def poly(t0: float, col: str, edge: str) -> str:
        pts = side(1, t0) + side(-1, t0)[::-1]
        return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{col}"{edge}/>'
    return poly(0, FOX, f' stroke="{FOX_D}" stroke-width="2" stroke-linejoin="round"') + poly(.78, FOX_L, "")


def fox(x: float, y: float, s: float = 1, pose: str = "sit", mood: str = "sly", flip: bool = False, held: str = "") -> str:
    """Hồ Tinh, the nine-tailed fox spirit: orange, nine separate wavy tails with cream tips. Facing right. pose = sit | run."""
    tails = ""
    bx, by = (-24, -18) if pose == "sit" else (-40, -48)
    for i in range(9):  # nine separate S-curved tails, thin at the base, bushy towards a cream tip
        a = (-192 + i * 15.5) if pose == "sit" else (-236 + i * 15)
        tails += _fox_tail(bx, by, a, (118, 146, 126, 152, 134, 156, 128, 150, 124)[i], 1 if i % 2 else -1)
    if pose == "run":
        body = f'<ellipse cx="10" cy="-48" rx="54" ry="24" fill="{FOX}"/>' + stroke("M-24 -30 l-22 22 M-8 -28 l-8 26 M34 -30 l26 20 M46 -32 l12 28", FOX_D, 9)
        hx, hy = 70, -68
    else:
        body = (f'<path d="M-30 0 Q-40 -60 0 -84 Q40 -60 30 0Z" fill="{FOX}"/><path d="M-12 -4 Q0 -60 12 -4Z" fill="{FOX_L}"/>'
                + stroke("M-14 -2 V-30 M14 -2 V-30", FOX_D, 9))
        hx, hy = 0, -104
    grin = stroke(f"M{hx - 2} {hy + 14} q10 8 20 -2", INK, 3) if mood == "sly" else f'<ellipse cx="{hx + 8}" cy="{hy + 16}" rx="5" ry="6" fill="#5A2E22"/>'
    head = (f'<path d="M{hx - 26} {hy - 4} L{hx - 22} {hy - 44} L{hx - 4} {hy - 20}Z M{hx + 26} {hy - 4} L{hx + 24} {hy - 44} L{hx + 6} {hy - 20}Z" fill="{FOX_D}"/>'
            f'<circle cx="{hx}" cy="{hy}" r="28" fill="{FOX}"/><path d="M{hx - 4} {hy + 4} L{hx + 40} {hy + 10} L{hx - 2} {hy + 24}Z" fill="{FOX_L}"/>'
            f'<circle cx="{hx + 40}" cy="{hy + 10}" r="5" fill="{INK}"/>')
    if mood == "sly":
        head += stroke(f"M{hx - 14} {hy - 6} q5 -4 10 0 M{hx + 6} {hy - 6} q5 -4 10 0", INK, 3)
    else:
        head += "".join(f'<circle cx="{hx + a}" cy="{hy - 6}" r="6" fill="#fff"/><circle cx="{hx + a + 1}" cy="{hy - 6}" r="3.4" fill="{INK}"/>' for a in (-8, 12))
    extra = ""
    if held == "basket":  # a stolen basket of fish, on the ground beside the fox
        fish = "".join(f'<g transform="translate({fx} {fy}) rotate({fr})"><ellipse rx="16" ry="7" fill="{fc}"/><path d="M-14 0 L-26 -8 L-26 8Z" fill="{fc}"/>'
                       f'<circle cx="9" cy="-1.5" r="1.8" fill="{INK}"/></g>' for fx, fy, fr, fc in ((-8, -22, -24, FISHM), (12, -20, 18, "#F2B53A")))
        extra = (f'<g transform="translate({hx + 72} -2) scale(1.35)">{fish}<path d="M-30 -16 Q-26 4 0 4 Q26 4 30 -16Z" fill="{THATCH}"/>'
                 + stroke("M-26 -9 h52 M-20 -2 h40", THATCH_D, 2) + '</g>')
    return group(x, y, s, tails + body + head + grin + extra, flip)


def tree_spirit(x: float, y: float, s: float = 1, mood: str = "grumpy", pose: str = "stomp") -> str:
    """Mộc Tinh, the grumpy old tree spirit: a gnarled trunk with a face, branch arms and root feet."""
    canopy = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in
                     [(-110, -300, 60, LEAF_D), (100, -300, 62, LEAF_D), (-60, -350, 70, LEAF), (50, -356, 72, LEAF), (0, -300, 70, LEAF),
                      (-130, -250, 44, LEAF), (130, -252, 44, LEAF)])
    lift = -18 if pose == "run" else -8
    roots = (stroke(f"M-40 -20 Q-70 -6 -96 {lift} M-20 -10 Q-30 4 -46 6", BARK_D, 16)
             + stroke(f"M40 -20 Q70 -6 96 {-4 if pose == 'run' else lift} M20 -10 Q30 4 46 6", BARK_D, 16))
    trunk = (f'<path d="M-56 -10 Q-44 -120 -60 -250 L60 -250 Q44 -120 56 -10 Q0 4 -56 -10Z" fill="{BARK}"/>'
             + stroke("M-30 -40 q-8 -40 4 -80 M30 -60 q10 -40 -2 -90 M-10 -230 q6 -20 -2 -40", BARK_D, 4))
    if pose == "run":
        arms_ = stroke("M-50 -170 Q-120 -170 -170 -120 M50 -170 Q120 -170 170 -220", BARK, 18)
    else:
        arms_ = stroke("M-50 -170 Q-120 -150 -176 -186 M50 -170 Q120 -150 176 -186 M-150 -172 l-24 10 M150 -172 l24 10", BARK, 18)
    if mood == "grumpy":
        fc = (stroke("M-38 -178 L-8 -168 M38 -178 L8 -168", INK, 6)
              + '<circle cx="-22" cy="-156" r="9" fill="#F5E7C0"/><circle cx="22" cy="-156" r="9" fill="#F5E7C0"/>'
              f'<circle cx="-20" cy="-154" r="4.5" fill="{INK}"/><circle cx="20" cy="-154" r="4.5" fill="{INK}"/>' + stroke("M-22 -112 Q0 -126 22 -112", INK, 6))
    else:
        fc = ('<circle cx="-22" cy="-160" r="13" fill="#F5E7C0"/><circle cx="22" cy="-160" r="13" fill="#F5E7C0"/>'
              f'<circle cx="-20" cy="-158" r="6" fill="{INK}"/><circle cx="20" cy="-158" r="6" fill="{INK}"/><ellipse cx="0" cy="-112" rx="12" ry="16" fill="#3A2A1E"/>')
    return group(x, y, s, roots + canopy + arms_ + trunk + fc, rot=-10 if pose == "run" else 0)


# ---------------------------------------------------------------- birds, fish, plants
def crane(x: float, y: float, s: float = 1, pose: str = "fly", flip: bool = False) -> str:
    """An all-white egret (cò) with a long yellow bill and dark legs, like the long-billed birds on Đông Sơn drums. Facing right."""
    bill = "#E8B020"
    if pose == "fly":
        o = (f'<path d="M-10 -6 Q-30 -70 -86 -80 Q-60 -40 -30 -4Z" fill="{FEATHER}" stroke="{FEATHER_D}" stroke-width="2"/>'
             f'<ellipse cx="0" cy="0" rx="40" ry="14" fill="{FEATHER}"/>' + stroke("M34 -4 Q52 -18 60 -10 Q66 -4 72 -10", FEATHER, 8)
             + f'<circle cx="74" cy="-12" r="8" fill="{FEATHER}"/>' + stroke("M80 -12 L116 -6", bill, 4)
             + f'<circle cx="76" cy="-14" r="1.8" fill="{INK}"/>' + stroke("M-36 2 L-90 10 M-36 6 L-88 16", "#3A3A3A", 3)
             + f'<path d="M-4 4 Q-20 50 -70 60 Q-46 30 -26 6Z" fill="{FEATHER}" stroke="{FEATHER_D}" stroke-width="2"/>')
    else:
        o = (stroke("M-6 0 V-50 M8 0 V-50", "#3A3A3A", 4) + f'<ellipse cx="0" cy="-66" rx="34" ry="20" fill="{FEATHER}" stroke="{FEATHER_D}" stroke-width="2"/>'
             + stroke("M-28 -60 Q-48 -52 -56 -44", FEATHER_D, 3)
             + stroke("M24 -74 Q40 -96 26 -118 Q18 -134 34 -140", FEATHER, 8)
             + f'<circle cx="36" cy="-142" r="8" fill="{FEATHER}"/>' + stroke("M30 -146 Q16 -150 8 -142", FEATHER_D, 2)
             + stroke("M42 -142 L78 -136", bill, 4) + f'<circle cx="38" cy="-143" r="1.8" fill="{INK}"/>')
    return group(x, y, s, o, flip)


def fishy(x: float, y: float, s: float = 1, col: str = "#F2B53A", flip: bool = False) -> str:
    return group(x, y, s, f'<path d="M-24 0 L-38 -12 L-38 12Z" fill="{col}"/><ellipse cx="0" cy="0" rx="24" ry="13" fill="{col}"/>'
                 f'<circle cx="12" cy="-3" r="3" fill="{INK}"/>' + stroke("M-6 -8 q4 8 0 16", "#fff", 2), flip, False)


def flower(x: float, y: float, s: float = 1, col: str = "#F08FB0") -> str:
    p = "".join(f'<circle cx="{6 * math.cos(math.radians(a)):.1f}" cy="{6 * math.sin(math.radians(a)):.1f}" r="5" fill="{col}"/>' for a in range(-90, 270, 72))
    return f'<g transform="translate({x} {y}) scale({s})">{p}<circle r="3.6" fill="#FFF3B0"/></g>'


def flowers(pts: list) -> str:
    cols = ("#F08FB0", "#F7D046", "#FFFFFF", "#E36B5B", "#B07CC6")
    return "".join(stroke(f"M{x} {y} v14", GRASS_D, 2.4) + flower(x, y, s, cols[i % 5]) for i, (x, y, s) in enumerate(pts))


def rice_tuft(x: float, y: float, s: float = 1, ripe: bool = False) -> str:
    col = "#C9B34A" if ripe else "#5DAE4A"
    head = stroke("M4 -34 q12 -4 14 10", "#E2C25A", 4) if ripe else ""
    return f'<g transform="translate({x} {y}) scale({s})">' + stroke("M0 0 Q-10 -18 -14 -30 M0 0 Q0 -20 4 -36 M0 0 Q10 -16 16 -26", col, 3.4) + head + '</g>'


def tree(x: float, y: float, s: float = 1, nest: bool = False) -> str:
    o = (f'<path d="M-10 0 Q-6 -50 -8 -90 H8 Q6 -50 10 0Z" fill="{BARK}"/>'
         + "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a, b, r, c in [(-30, -100, 32, LEAF_D), (28, -104, 34, LEAF_D), (0, -126, 40, LEAF)]))
    if nest:
        o += f'<ellipse cx="18" cy="-164" rx="20" ry="7" fill="{THATCH_D}"/>'
    return group(x, y, s, o)


def bamboo(x: float, y: float, h: float = 240) -> str:
    o = stroke(f"M0 0 V{-h}", "#7DB85A", 12) + "".join(stroke(f"M-7 {-j} h14", "#5A9440", 3) for j in range(40, int(h), 46))
    o += "".join(f'<path d="M0 {-j} q24 -12 40 -4 q-20 8 -40 4Z" fill="#6FAE4E"/>' for j in range(70, int(h), 70))
    return f'<g transform="translate({x} {y})">{o}</g>'


def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def star_poly(x: float, y: float, r: float, ri: float, n: int, col: str) -> str:
    pts = " ".join(f"{x + (r if i % 2 == 0 else ri) * math.sin(math.pi * i / n):.1f},{y - (r if i % 2 == 0 else ri) * math.cos(math.pi * i / n):.1f}" for i in range(2 * n))
    return f'<polygon points="{pts}" fill="{col}"/>'


def sun(x: float, y: float, r: float = 46) -> str:
    """A sun with the fourteen-pointed star found at the centre of the Ngọc Lũ drum."""
    return (f'<circle cx="{x}" cy="{y}" r="{r * 1.5:.0f}" fill="#FFF3B0" opacity=".35"/><circle cx="{x}" cy="{y}" r="{r}" fill="#F7C948"/>'
            + star_poly(x, y, r * .86, r * .42, 14, "#E8A23A") + f'<circle cx="{x}" cy="{y}" r="{r * .3:.0f}" fill="#F7C948"/>')


def moon(x: float, y: float, r: float = 26, bg: str = "#3B4F86") -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF4CC"/><circle cx="{x + r * .45:.1f}" cy="{y - r * .2:.1f}" r="{r * .9:.1f}" fill="{bg}"/>'


def stars(pts: list) -> str:
    return "".join(star_poly(a, b, 6 * s, 2.6 * s, 5, "#F3F3FA") for a, b, s in pts)


# ---------------------------------------------------------------- buildings and things
def stilt_house(x: float, y: float, s: float = 1, built: bool = True) -> str:
    """A Đông Sơn style house on stilts with a boat-shaped saddle roof whose ends sweep up like horns."""
    posts = "".join(f'<rect x="{a - 5}" y="-66" width="10" height="66" fill="{WOOD_D}"/>' for a in (-64, -22, 22, 64))
    ladder = stroke("M84 0 L70 -62 M100 0 L86 -62", WOOD, 5) + stroke(" ".join(f"M{82 - j * .22:.1f} {-j} h16" for j in (12, 28, 44)), WOOD, 4)
    plat = f'<rect x="-86" y="-72" width="172" height="12" rx="3" fill="{WOOD}"/>'
    if not built:
        frame = stroke("M-64 -72 V-176 M64 -72 V-176 M0 -72 V-166 M-120 -206 Q-90 -178 -64 -176 Q0 -160 64 -176 Q90 -178 120 -206", WOOD, 7)
        return group(x, y, s, posts + plat + ladder + frame)
    walls = (f'<rect x="-66" y="-130" width="132" height="60" fill="{WOOD_L}"/>'
             + stroke(" ".join(f"M{a} -128 V-72" for a in range(-52, 60, 16)), WOOD, 2) + f'<rect x="-14" y="-118" width="28" height="46" fill="{WOOD_D}"/>')
    roof = (f'<path d="M-150 -232 Q-118 -198 -92 -194 Q0 -168 92 -194 Q118 -198 150 -232 Q136 -186 100 -124 L-100 -124 Q-136 -186 -150 -232Z" fill="{THATCH}"/>'
            + stroke(" ".join(f"M{a} -{176 + abs(a) * .12:.0f} L{a * 1.05:.0f} -128" for a in (-80, -48, -16, 16, 48, 80)), THATCH_D, 3)
            + stroke("M-150 -232 Q-118 -198 -92 -194 Q0 -168 92 -194 Q118 -198 150 -232", WOOD_D, 5))
    return group(x, y, s, posts + plat + ladder + walls + roof)


def grass_hut(x: float, y: float, s: float = 1) -> str:
    """A low hut woven from grass, sitting on the ground (before the people learn to build up high)."""
    o = (f'<path d="M-90 0 Q-96 -70 -40 -96 Q0 -112 40 -96 Q96 -70 90 0Z" fill="{THATCH}"/>'
         + stroke("M-70 -20 Q-66 -70 -30 -88 M-36 -10 Q-30 -70 -6 -98 M0 -6 Q4 -60 22 -96 M36 -10 Q44 -60 56 -84 M70 -16 Q74 -46 80 -58", THATCH_D, 3)
         + f'<path d="M-20 0 Q-20 -46 0 -48 Q20 -46 20 0Z" fill="{WOOD_D}"/>')
    return group(x, y, s, o)


def bronze_drum(x: float, y: float, s: float = 1, shadow: bool = True) -> str:
    """A Đông Sơn bronze drum: a waisted body with ring bands and a star on its flat top."""
    o = (f'<path d="M-50 0 L-44 -30 Q-58 -50 -54 -66 L54 -66 Q58 -50 44 -30 L50 0Z" fill="{BRONZE}"/>'
         + band(-50, 50, -48, BRONZE_L, BRONZE_D) + stroke("M-46 -16 H46", BRONZE_D, 3)
         + f'<ellipse cy="-66" rx="56" ry="14" fill="{BRONZE_L}"/>' + f'<g transform="translate(0 -66) scale(1 .25)">{star_poly(0, 0, 40, 16, 14, BRONZE_D)}</g>')
    return group(x, y, s, o, shadow=shadow)


def boat(x: float, y: float, s: float = 1, flip: bool = False) -> str:
    """A long Đông Sơn boat with a bird-head prow, facing right."""
    o = (f'<path d="M-140 -30 Q0 16 120 -24 Q136 -50 132 -72 Q150 -76 160 -70 Q146 -66 142 -58 Q148 -30 120 0 Q0 30 -130 0 Q-150 -16 -140 -30Z" fill="{WOOD}"/>'
         + band(-110, 100, -8, WOOD_L, WOOD_D) + f'<circle cx="138" cy="-70" r="4" fill="{INK}"/>')
    return group(x, y, s, o, flip)


def fire(x: float, y: float, s: float = 1) -> str:
    o = ('<g fill="#8A5A36"><rect x="-46" y="-10" width="92" height="14" rx="7" transform="rotate(12)"/>'
         '<rect x="-46" y="-10" width="92" height="14" rx="7" transform="rotate(-12)"/></g>'
         '<path d="M-28 -6 Q-36 -40 -12 -66 Q-10 -42 0 -50 Q-2 -80 16 -96 Q18 -64 30 -52 Q38 -30 28 -6Z" fill="#F2652A"/>'
         '<path d="M-14 -6 Q-18 -28 -2 -44 Q0 -30 8 -36 Q20 -20 14 -6Z" fill="#FFC23A"/>')
    return group(x, y, s, o)


def bamboo_tube(x: float, y: float, rot: float = -20) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot})" filter="url(#p)"><rect x="-9" y="-90" width="18" height="90" rx="5" fill="#7DB85A"/>'
            + stroke("M-9 -60 h18 M-9 -30 h18", "#5A9440", 3) + '<g fill="#fff" opacity=".8"><circle cx="0" cy="-102" r="7"/><circle cx="6" cy="-118" r="9"/><circle cx="-2" cy="-138" r="11"/></g></g>')


def big_pot(x: float, y: float, s: float = 1) -> str:
    o = (f'<path d="M-60 -70 Q-74 0 0 0 Q74 0 60 -70Z" fill="{BRONZE}"/>' + band(-62, 62, -54, BRONZE_L, BRONZE_D)
         + '<ellipse cy="-70" rx="62" ry="12" fill="#fff"/><g fill="#fff" opacity=".8"><circle cx="-10" cy="-90" r="8"/><circle cx="8" cy="-108" r="10"/></g>')
    return group(x, y, s, o)


def sea_palace(x: float, y: float, s: float = 1) -> str:
    """The water palace: a glowing pearl dome on coral arches, with a star on top (no land-style roofs)."""
    o = ('<ellipse cx="0" cy="-200" rx="150" ry="130" fill="#FFFFFF" opacity=".12"/>'
         '<path d="M-150 0 V-110 Q-150 -150 -110 -150 H110 Q150 -150 150 -110 V0Z" fill="#E9A6A0"/>'
         + "".join(f'<path d="M{a - 30} 0 V-70 Q{a} -112 {a + 30} -70 V0Z" fill="#2C5F8E"/>' for a in (-90, 0, 90))
         + '<circle cx="0" cy="-200" r="80" fill="#F4F0FA"/><circle cx="-26" cy="-226" r="20" fill="#fff"/>'
         + star_poly(0, -292, 18, 8, 14, GOLD) + band(-150, 150, -140, "#FFF6E6", "#C97F7A")
         + "".join(f'<circle cx="{a}" cy="-150" r="12" fill="#F4F0FA"/>' for a in (-130, -70, 70, 130)))
    return group(x, y, s, o)


def seagrass(pts: list) -> str:
    return "".join(stroke(f"M{a} {b} q-12 -30 0 -60 q12 -30 0 -60", "#3E9A6A", 7) for a, b in pts)


def bubbles(pts: list) -> str:
    return "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="none" stroke="#CFE9F7" stroke-width="2.4"/>' for a, b, r in pts)


def shell(x: float, y: float, col: str = "#F7C6A0") -> str:
    return f'<g transform="translate({x} {y})"><path d="M-14 0 Q0 -26 14 0Z" fill="{col}"/>' + stroke("M0 0 V-14 M-6 0 l-3 -10 M6 0 l3 -10", "#D98E6A", 1.6) + '</g>'
