#!/usr/bin/env python3
"""Generates the 13 The-Owl-and-the-Raven flip-book SVGs from shared character parts.

Usage: python3 raven_gen.py <output-dir>
Scale rule: Owl and Raven are about the same size (as a snowy owl and a raven really are) and
use the same scale S on every page. Raven stays plain white until the pot tips over on page 10,
so no earlier picture spoils the reveal. Owl's dots grow page by page (spots = 0 -> .3 -> .72 -> 1).
Snow-house geometry is fixed: floor line y = 440, lamp at x 78, rug centre y 528.
"""
import sys

OUT = sys.argv[1]
INK = "#2B2320"
S = 1.12                                                # one scale for both birds, every page
OWL, OWL_D, FACE, EYE, SPOT = "#FBFAF5", "#D8DEE6", "#FFFFFF", "#F6C431", "#2B2B36"
RAV_W, RAV_WD, RAV_WT = "#F3F0E9", "#D9D9DF", "#CFCDCA"     # white Raven: body, wing, tail
RAV_B, RAV_BD, RAV_BT, SHEEN = "#262838", "#394060", "#1E2030", "#7487B8"  # black Raven
BEAK, BEAK_L, LEG = "#3A3A46", "#6E7390", "#4A4550"
BOOT, BOOT_D = "#A86A3C", "#7A4826"
STONE, STONE_D, SOOT = "#8E8A82", "#6C6862", "#17171F"
SNOW, SNOW_D, BLOCK = "#F4F8FC", "#D2E0EE", "#C9D9EA"
RUG, RUG_D = "#B98A5A", "#94683E"
FLAME, FLAME_I = "#F59A2E", "#FFE07A"
INSIDE = [(0, "#5C7BAA"), (1, "#9CB5D2")]
DAY = [(0, "#4F9FD8"), (1, "#BFE2F4")]
NIGHT = [(0, "#141C46"), (1, "#36508A")]
FLOOR, RUG_Y = 440, 528


def stroke(d: str, col: str = INK, w: float = 5, op: float = 1) -> str:
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{o}/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def brush(x: float, y: float, rot: float, length: float = 52) -> str:
    """A little feather brush with a black soot tip, pointing along +x before rotation."""
    return (f'<g transform="translate({x} {y}) rotate({rot})">' + stroke(f"M0 0 L{length} 0", "#8A5A36", 4)
            + f'<path d="M{length - 2} -5 Q{length + 12} 0 {length - 2} 5Z" fill="{SOOT}"/></g>')


# ---------------------------------------------------------------- Owl (a snowy owl, facing us)
SPOTS = [(-30, -30), (0, -26), (30, -30), (-40, -54), (-14, -50), (14, -50), (40, -54), (-46, -78), (-22, -74),
         (0, -78), (22, -74), (46, -78), (-40, -102), (-16, -98), (16, -98), (40, -102), (-26, -120), (0, -118),
         (26, -120), (-56, -60), (56, -60), (-60, -90), (60, -90), (-30, -196), (0, -204), (30, -196), (-16, -186), (16, -186)]


def owl_wing(side: int, pose: str) -> str:
    if pose == "up":       # wings flung out and up: a happy twirl
        return f'<ellipse cx="{side * 74}" cy="-120" rx="18" ry="48" fill="{OWL_D}" transform="rotate({side * 48} {side * 74} -120)"/>'
    if pose == "brush":    # this wing reaches out to the side, holding the brush
        return (f'<ellipse cx="{side * 80}" cy="-100" rx="16" ry="44" fill="{OWL_D}" transform="rotate({side * 70} {side * 80} -100)"/>'
                + brush(side * 112, -112, 180 if side < 0 else 0))
    if pose == "brushlow":  # brush held short and low, pointing at his chest (not his beak)
        return (f'<ellipse cx="{side * 80}" cy="-100" rx="16" ry="44" fill="{OWL_D}" transform="rotate({side * 70} {side * 80} -100)"/>'
                + brush(side * 112, -112, 160 if side < 0 else 20, 26))
    if pose == "cheek":    # wing tip up at the face: oh!
        return f'<ellipse cx="{side * 56}" cy="-118" rx="16" ry="44" fill="{OWL_D}" transform="rotate({side * -22} {side * 56} -118)"/>'
    return f'<ellipse cx="{side * 54}" cy="-78" rx="19" ry="52" fill="{OWL_D}" transform="rotate({side * 8} {side * 54} -78)"/>'


def owl_face(mood: str) -> str:
    out = (f'<circle cx="-21" cy="-160" r="25" fill="{FACE}" stroke="{OWL_D}" stroke-width="2"/>'
           f'<circle cx="21" cy="-160" r="25" fill="{FACE}" stroke="{OWL_D}" stroke-width="2"/>')
    if mood == "laugh":
        out += stroke("M-31 -160 q10 -10 20 0 M11 -160 q10 -10 20 0", INK, 4)
    else:
        big = 15 if mood == "oh" else 13
        for sx in (-1, 1):
            out += (f'<circle cx="{sx * 21}" cy="-161" r="{big}" fill="{EYE}" stroke="#C9921A" stroke-width="2"/>'
                    f'<circle cx="{sx * 21}" cy="-160" r="7" fill="{INK}"/><circle cx="{sx * 21 + 3}" cy="-164" r="2.4" fill="#fff"/>')
        if mood == "cross":   # a little frown: eyebrows down in the middle
            out += stroke("M-34 -183 L-10 -181 M34 -183 L10 -181", INK, 4)
    out += '<circle cx="-40" cy="-138" r="7" fill="#F0705F" opacity=".35"/><circle cx="40" cy="-138" r="7" fill="#F0705F" opacity=".35"/>'
    if mood == "oh":
        out += '<path d="M-7 -146 L7 -146 L0 -128Z" fill="#4A3B30"/><ellipse cy="-124" rx="5" ry="6" fill="#5A2E22"/>'
    else:
        out += '<path d="M-7 -146 L7 -146 L0 -128Z" fill="#4A3B30"/>'
    return out


def owl(x: float, y: float, spots: float = 0, pose: str = "down", mood: str = "smile", pose2: str = "", s: float = S) -> str:
    """A round white snowy owl facing us. (x, y) is her feet. spots: 0..1 of her dots painted.
    pose is her right-hand (our left) wing, pose2 her other wing (defaults to the same)."""
    out = ""
    for sx in (-1, 1):
        out += f'<ellipse cx="{sx * 20}" cy="-7" rx="16" ry="9" fill="{OWL}" stroke="{OWL_D}" stroke-width="2"/>'
        out += stroke(f"M{sx * 20 - 9} -1 l-2 5 M{sx * 20} 1 l0 5 M{sx * 20 + 9} -1 l2 5", INK, 2.6)
    out += f'<ellipse cy="-82" rx="60" ry="74" fill="{OWL}"/>'
    out += f'<path d="M-44 -40 Q0 -12 44 -40 Q0 -6 -44 -40Z" fill="{OWL_D}" opacity=".6"/>'
    out += owl_wing(-1, pose) + owl_wing(1, pose2 or pose)
    out += f'<path d="M-30 -196 L-42 -222 L-16 -204Z M30 -196 L42 -222 L16 -204Z" fill="{OWL}" stroke="{OWL_D}" stroke-width="2"/>'
    out += f'<circle cy="-164" r="52" fill="{OWL}"/>'
    n = round(len(SPOTS) * spots)
    out += "".join(f'<ellipse cx="{a}" cy="{b}" rx="5" ry="3.6" fill="{SPOT}"/>' for a, b in SPOTS[:n])
    out += owl_face(mood)
    return group(x, y, s, False, 0, out)


# ---------------------------------------------------------------- Raven (side view, facing right)
def raven(x: float, y: float, black: bool = False, pose: str = "stand", mood: str = "smile", wing: str = "down",
          boots: bool = False, flip: bool = False, lift: float = 0, s: float = S) -> str:
    """Raven in side view facing right. (x, y) is the ground under his feet; lift raises him off it (a hop).
    pose: stand / hop / sit. wing: down / up / reach (holding a brush forward). mood: smile / dazed / laugh."""
    body, wcol, tail = (RAV_B, RAV_BD, RAV_BT) if black else (RAV_W, RAV_WD, RAV_WT)
    out = ""
    if pose == "sit":      # sitting on his tail, legs stuck out in front, head up
        legs = "M-2 -36 L10 -4 M12 -36 L30 -4"
        feet = [(12, -2), (32, -2)]
        rot = -14
    elif pose == "hop":
        legs = "M-8 -44 L-14 -24 L-4 -14 M8 -44 L4 -24 L14 -14"
        feet = [(-2, -14), (16, -14)]
        rot = -8
    else:
        legs = "M-8 -44 L-10 -2 M8 -44 L6 -2"
        feet = [(-10, -2), (6, -2)]
        rot = 0
    out += stroke(legs, LEG, 6)
    for fx, fy in feet:
        if boots:
            out += f'<path d="M{fx - 8} {fy - 22} h14 v14 h12 q6 0 6 6 v2 h-32Z" fill="{BOOT}" stroke="{BOOT_D}" stroke-width="2"/>'
            out += stroke(f"M{fx - 8} {fy - 16} h14", "#F4E3C8", 2.4)
        else:
            out += stroke(f"M{fx} {fy} l14 2 M{fx} {fy} l-10 3 M{fx} {fy} l8 6", LEG, 3)
    b = f'<path d="M-62 -84 L-132 -62 L-128 -80 L-136 -96 Z" fill="{tail}"/>'          # wedge tail
    b += f'<ellipse cx="-12" cy="-82" rx="64" ry="42" fill="{body}" transform="rotate(-16 -12 -82)"/>'
    if wing == "up":
        b += f'<ellipse cx="-26" cy="-132" rx="54" ry="22" fill="{wcol}" transform="rotate(-48 -26 -132)"/>'
    elif wing == "reach":
        b += f'<ellipse cx="38" cy="-82" rx="50" ry="18" fill="{wcol}" transform="rotate(8 38 -82)"/>' + brush(82, -74, -8)
    else:
        b += f'<ellipse cx="-22" cy="-80" rx="52" ry="26" fill="{wcol}" transform="rotate(-14 -22 -80)"/>'
        b += stroke("M-56 -70 l-16 8 M-50 -60 l-16 8", body, 3, .7)
    b += f'<path d="M30 -104 L44 -86 L52 -102 L60 -88 L66 -106 Z" fill="{body}"/>'       # shaggy throat
    b += f'<circle cx="44" cy="-126" r="31" fill="{body}"/>'
    b += (f'<path d="M64 -142 Q104 -140 126 -122 Q110 -110 66 -108 Z" fill="{BEAK}"/>'    # big heavy beak
          + stroke("M70 -134 Q100 -134 118 -122", BEAK_L, 2.6))
    if mood == "dazed":
        b += f'<circle cx="52" cy="-132" r="8" fill="#fff"/>' + stroke("M52 -132 m-4 0 a4 4 0 1 1 4 4", INK, 2.2)
        b += "".join(f'<use href="#st" transform="translate({a} {c}) scale(.9)"/>' for a, c in [(20, -176), (52, -184), (82, -170)])
    elif mood == "laugh":
        b += stroke("M45 -134 q7 -8 14 0", "#fff" if black else INK, 3.6)
    else:
        b += f'<circle cx="52" cy="-132" r="8" fill="#fff"/><circle cx="54" cy="-132" r="4.4" fill="{INK}"/><circle cx="55.5" cy="-134" r="1.5" fill="#fff"/>'
    b += f'<circle cx="34" cy="-112" r="6" fill="#F0705F" opacity="{.25 if black else .4}"/>'
    if black:
        b += stroke("M-40 -110 Q-6 -126 26 -114 M24 -150 Q40 -158 58 -152", SHEEN, 3.4, .8)
    out += f'<g transform="rotate({rot} 0 -44)">{b}</g>'
    inner = f'<g transform="translate(0 {-lift})">{out}</g>' if lift else out
    return group(x, y, s, flip, 0, inner)


def ground_shadow(x: float, w: float, y: float = RUG_Y + 6) -> str:
    return f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .18:.0f}" fill="#1b1b33" opacity=".18"/>'


def hop_marks(x: float, y: float, k: float = 1) -> str:
    return stroke(f"M{x - 24 * k:.0f} {y} v{-20 * k:.0f} M{x} {y - 6} v{-26 * k:.0f} M{x + 24 * k:.0f} {y} v{-20 * k:.0f}", "#fff", 4, .85)


# ---------------------------------------------------------------- props
def pot(x: float, y: float, tipped: bool = False) -> str:
    """The little stone pot of black soot-oil from the lamp. (x, y) is its base."""
    if tipped:  # lying on its side, mouth to the left, a black puddle running out
        return (f'<g filter="url(#p)"><ellipse cx="{x - 70}" cy="{y + 2}" rx="78" ry="13" fill="{SOOT}"/>'
                f'<g transform="translate({x} {y}) rotate(-90 0 -22)"><path d="M-26 -44 L26 -44 L20 0 L-20 0Z" fill="{STONE}"/>'
                f'<ellipse cy="-44" rx="26" ry="7" fill="{SOOT}"/><path d="M-20 -14 L20 -14" stroke="{STONE_D}" stroke-width="3"/></g></g>')
    return (f'<g transform="translate({x} {y})" filter="url(#p)"><path d="M-26 -44 L26 -44 L20 0 L-20 0Z" fill="{STONE}"/>'
            f'<ellipse cy="-44" rx="26" ry="7" fill="{STONE_D}"/><ellipse cy="-44" rx="21" ry="5" fill="{SOOT}"/>'
            f'<path d="M-22 -14 L22 -14" stroke="{STONE_D}" stroke-width="3"/></g>')


def lamp(x: float, y: float, glow: bool = True) -> str:
    """A qulliq: a half-moon soapstone oil lamp with a row of little flames along its straight edge."""
    out = f'<circle cx="{x}" cy="{y - 40}" r="190" fill="url(#glow)"/>' if glow else ""
    out += f'<g filter="url(#p)"><path d="M{x - 62} {y - 30} L{x + 62} {y - 30} Q{x + 56} {y + 4} {x} {y + 4} Q{x - 56} {y + 4} {x - 62} {y - 30}Z" fill="{STONE}"/>'
    out += f'<ellipse cx="{x}" cy="{y - 30}" rx="62" ry="6" fill="{STONE_D}"/></g>'
    for i in range(6):
        fx = x - 50 + i * 20
        out += f'<path d="M{fx} {y - 32} q-8 -10 0 -26 q8 16 0 26Z" fill="{FLAME}"/><path d="M{fx} {y - 33} q-3 -6 0 -13 q3 7 0 13Z" fill="{FLAME_I}"/>'
    return out


def snow_house() -> list:
    """Inside the snow house: a dome of snow blocks, a fur rug, the lamp on the left."""
    rows = ""
    for i, yy in enumerate(range(70, FLOOR, 74)):
        rows += f"M0 {yy} Q400 {yy - 34} 800 {yy} "
        off = 50 if i % 2 else 0
        rows += " ".join(f"M{xx} {yy - 30 + abs(xx - 400) * .06:.0f} l0 70" for xx in range(off + 40, 800, 120)) + " "
    return [f'<g opacity=".55">{stroke(rows, BLOCK, 3.4)}</g>',
            f'<path filter="url(#p)" d="M0 {FLOOR} Q400 {FLOOR - 16} 800 {FLOOR} V600 H0Z" fill="{SNOW}"/>',
            f'<ellipse cx="430" cy="{RUG_Y}" rx="330" ry="46" fill="{RUG}"/><ellipse cx="430" cy="{RUG_Y}" rx="300" ry="34" fill="none" stroke="{RUG_D}" stroke-width="3" stroke-dasharray="8 10"/>',
            lamp(78, 500)]


def stars(pts: list) -> str:
    return "".join(f'<use href="#st" transform="translate({a} {b}) scale({c})"/>' for a, b, c in pts)


def igloo(x: float, y: float, s: float = 1, glow: bool = False) -> str:
    door = "#F7C46A" if glow else "#5E7FAE"
    lines = stroke("M-82 -30 Q0 -44 82 -30 M-62 -64 Q0 -78 62 -64 M-30 -92 Q0 -98 30 -92 M-40 0 v-30 M40 0 v-30 M0 -38 v-30 M-34 -68 v-26 M34 -68 v-26", SNOW_D, 3)
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)"><path d="M-96 0 Q-96 -110 0 -110 Q96 -110 96 0Z" fill="{SNOW}"/>'
            f'{lines}<path d="M60 0 Q60 -46 96 -46 Q132 -46 132 0Z" fill="{SNOW}"/><path d="M78 0 Q78 -28 96 -28 Q114 -28 114 0Z" fill="{door}"/></g>')


def cloud(x: float, y: float, s: float = 1, op: float = .9) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def lights() -> str:
    """Northern lights: soft green and pink ribbons."""
    return ('<g opacity=".55"><path d="M-20 140 Q160 40 330 120 T700 90 T840 130 L840 170 Q700 130 600 160 T330 170 T-20 190Z" fill="#5FE0A0"/>'
            '<path d="M60 70 Q240 0 420 60 T820 40 L820 70 Q640 60 520 90 T60 100Z" fill="#B48BE8" opacity=".7"/></g>')


DEFS = {
    "st": '<polygon id="st" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="#FFE07A"/>',
    "glow": '<radialGradient id="glow"><stop offset="0" stop-color="#FFD58A" stop-opacity=".75"/><stop offset="1" stop-color="#FFD58A" stop-opacity="0"/></radialGradient>',
}


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    defs = "".join(d for k, d in DEFS.items() if f'#{k}"' in joined or f'#{k})' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/raven-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def outside_day() -> list:
    return [cloud(150, 90, 1), cloud(640, 70, .85),
            f'<path d="M0 300 Q200 270 420 300 T800 290 V600 H0Z" fill="{SNOW_D}"/>',
            igloo(640, 330, 1.05),
            f'<path filter="url(#p)" d="M0 400 Q400 360 800 400 V600 H0Z" fill="{SNOW}"/>',
            stroke("M60 470 h50 M300 560 h70 M560 520 h60 M700 580 h50", SNOW_D, 4)]


OWL_X, RAV_X, FEET = 600, 310, RUG_Y + 4
POT_X = 462

# 01 cover: two plain white friends outside their snow house
svg(1, "The Owl and the Raven", "Paper-cut cover: under a bright blue Arctic sky, two plain white birds stand side by side on the snow in front of a round snow house: a round snowy owl with big yellow eyes on the right, and a raven with a big heavy dark beak on the left, facing her. Neither has any spots or black feathers yet.", DAY,
    outside_day() + [ground_shadow(220, 80, 470), ground_shadow(470, 70, 470),
                     raven(220, 466), owl(470, 466)])

# 02 long ago, both white, best friends
svg(2, "Two white friends", "Paper-cut scene: on a snowy hill under a blue sky, a plain white owl and a plain white raven with a big dark beak stand close together, facing each other. A little pink heart floats between them.", DAY,
    [cloud(160, 80, 1), cloud(660, 110, .8),
     f'<path filter="url(#p)" d="M0 420 Q400 330 800 420 V600 H0Z" fill="{SNOW}"/>',
     stroke("M90 500 h60 M600 520 h70 M330 570 h60", SNOW_D, 4),
     ground_shadow(270, 80, 456), ground_shadow(525, 70, 452),
     raven(270, 452), owl(525, 448),
     '<path filter="url(#p)" d="M412 186 c-14 -20 -40 -4 -24 16 l24 22 l24 -22 c16 -20 -10 -36 -24 -16z" fill="#F2789F"/>'])

# 03 inside the snow house, by the lamp: let's make each other new clothes
svg(3, "Let's make new clothes!", "Paper-cut scene: inside a snow house made of snow blocks, a stone oil lamp glows with a row of little orange flames on the left. The white raven and the white owl stand on a brown fur rug, facing each other. Between them, a little stone pot holds black soot-oil from the lamp.", INSIDE,
    snow_house() + [ground_shadow(RAV_X, 80), ground_shadow(OWL_X, 70),
                    raven(RAV_X, FEET), owl(OWL_X, FEET), pot(POT_X, RUG_Y + 26)])

# 04 Raven paints Owl's dress: dot, dot, dot (first dots)
svg(4, "Dot, dot, dot!", "Paper-cut scene: in the glowing snow house, the white raven reaches out with a little feather brush dipped in black soot and dots the white owl's tummy. The owl sits very still. She has a few black dots on her lower tummy so far. The soot pot stands between them on the rug.", INSIDE,
    snow_house() + [ground_shadow(RAV_X + 55, 80), ground_shadow(OWL_X, 70),
                    raven(RAV_X + 55, FEET, wing="reach"), owl(OWL_X, FEET, .3), pot(POT_X, RUG_Y + 26)])

# 05 more dots; Owl sits as still as a stone
svg(5, "Still as a stone", "Paper-cut scene: the white raven keeps dotting with his feather brush, and now the white owl has rows of black dots all over her tummy and wings. She keeps her eyes on him and sits as still as a stone. The soot pot stands between them.", INSIDE,
    snow_house() + [ground_shadow(RAV_X + 55, 80), ground_shadow(OWL_X, 70),
                    raven(RAV_X + 55, FEET, wing="reach"), owl(OWL_X, FEET, .72), pot(POT_X, RUG_Y + 26)])

# 06 the spotted dress is finished
svg(6, "A beautiful spotted dress", "Paper-cut scene: the owl has a finished dress of black dots all over her body, wings and the top of her head, like a real snowy owl. She flings her wings out and up for joy, with sparkles around her. The white raven raises a wing to cheer.", INSIDE,
    snow_house() + [ground_shadow(RAV_X, 80), ground_shadow(OWL_X, 70),
                    raven(RAV_X, FEET, wing="up"), owl(OWL_X, FEET, 1, "up", "laugh"), pot(POT_X, RUG_Y + 26),
                    stars([(470, 200, 1.4), (670, 220, 1.2), (690, 330, 1), (450, 320, 1)])])

# 07 Raven's turn: new boots first, then sit still for dots
svg(7, "Raven's turn", "Paper-cut scene: now the spotted owl holds the feather brush out toward the white raven. The raven is wearing a new pair of brown boots and stands still for a moment. The soot pot stands between them.", INSIDE,
    snow_house() + [ground_shadow(RAV_X - 20, 80), ground_shadow(OWL_X + 20, 70),
                    raven(RAV_X - 20, FEET, boots=True), owl(OWL_X + 20, FEET, 1, "brushlow", pose2="down"), pot(POT_X, RUG_Y + 26)])

# 08 hop, hop
svg(8, "Hop, hop!", "Paper-cut scene: the white raven in his brown boots gives a little hop off the rug, too excited to keep still. The spotted owl holds out her brush and waits. The soot pot stands between them.", INSIDE,
    snow_house() + [ground_shadow(RAV_X, 64), ground_shadow(OWL_X, 70),
                    raven(RAV_X, FEET, pose="hop", boots=True, lift=40), hop_marks(RAV_X, FEET - 10),
                    owl(OWL_X, FEET, 1, "brush", pose2="down"), pot(POT_X, RUG_Y + 26)])

# 09 hop, HOP: higher, Owl frowns a little
svg(9, "Sit still, Raven!", "Paper-cut scene: the white raven hops even higher off the rug, one wing up, in his brown boots. The spotted owl frowns a little, her brush held out, waiting. The soot pot stands right between them.", INSIDE,
    snow_house() + [ground_shadow(RAV_X + 20, 54), ground_shadow(OWL_X, 70),
                    raven(RAV_X + 20, FEET, pose="hop", wing="up", boots=True, lift=86), hop_marks(RAV_X + 20, FEET - 12, 1.2),
                    owl(OWL_X, FEET, 1, "brush", "cross", pose2="down"), pot(POT_X, RUG_Y + 26)])

# 10 the BIG hop: his boot knocks the pot over, SPLOSH
def splosh(x: float, y: float) -> str:
    """Big drops of black soot-oil flying out in a ring around (x, y), with little whoosh lines."""
    out = ""
    for a, b, r in [(-150, -40, -60), (-130, -120, -30), (-70, -170, -10), (10, -190, 0), (90, -170, 15), (150, -110, 40),
                    (170, -20, 70), (-170, 40, -80), (120, 60, 100)]:
        out += (f'<g transform="translate({x + a} {y + b}) rotate({r}) scale(1.7)"><path d="M0 0 q8 13 0 19 q-8 -6 0 -19z" fill="{SOOT}"/></g>')
    out += stroke(f"M{x - 120} {y - 150} l-16 -16 M{x + 120} {y - 150} l16 -16 M{x - 160} {y - 80} l-22 -4 M{x + 165} {y - 70} l22 -4", "#fff", 4, .9)
    return f'<g filter="url(#p)">{out}</g>'


svg(10, "SPLOSH!", "Paper-cut scene: SPLOSH! The raven lands from his big hop and his boot knocks over the little pot. Big black drops of soot-oil fly all around him, and now he is black from beak to tail, except his brown boots. The pot lies on its side in a black puddle, and the spotted owl stares with big round eyes and an open beak.", INSIDE,
    snow_house() + [splosh(RAV_X + 30, FEET - 110), ground_shadow(RAV_X + 20, 70), raven(RAV_X + 20, FEET, True, pose="hop", boots=True, wing="up", lift=30),
                    pot(RAV_X + 140, RUG_Y + 22, True), owl(OWL_X + 30, FEET, 1, "cheek", "oh", pose2="down")])

# 11 Raven sits up, black all over: Quawk!
svg(11, "Quawk! Quawk!", "Paper-cut scene: the raven sits on the rug, black all over except his brown boots, blinking and a little dazed, with three small yellow stars twinkling over his head. He is fine, not hurt. The spotted owl stares at him with big round eyes and an open beak. The pot lies on its side in a black puddle.", INSIDE,
    snow_house() + [ground_shadow(RAV_X + 20, 80), raven(RAV_X + 20, FEET, True, "sit", "dazed", boots=True),
                    pot(RAV_X + 140, RUG_Y + 22, True), owl(OWL_X + 30, FEET, 1, "down", "oh")])

# 12 friends still: shiny black and spotted, laughing
svg(12, "Still best friends", "Paper-cut scene: the black raven stands tall and shiny, his feathers gleaming with blue sparkles, and laughs with his eyes closed, one wing up. The spotted owl laughs too, wings out. A pink heart floats between them over the rug, and the little pot stands upright again.", INSIDE,
    snow_house() + [ground_shadow(RAV_X, 80), ground_shadow(OWL_X, 70),
                    raven(RAV_X, FEET, True, wing="up", mood="laugh", boots=True), owl(OWL_X, FEET, 1, "up", "laugh"),
                    pot(POT_X, RUG_Y + 26),
                    stars([(200, 250, 1), (330, 160, 1.2), (230, 180, .9)]),
                    '<path filter="url(#p)" d="M455 300 c-12 -18 -36 -4 -22 14 l22 20 l22 -20 c14 -18 -10 -32 -22 -14z" fill="#F2789F"/>'])

# 13 outside under the stars and northern lights, the spotted owl and the black raven together
svg(13, "The spotted owl and the black raven", "Paper-cut scene: at night under twinkling stars and green and purple northern lights, the spotted snowy owl and the shiny black raven in his brown boots stand side by side on a big white snowdrift. Off to the right, the snow house glows with warm light at its door.", NIGHT,
    [stars([(60, 40, 1), (200, 30, .8), (360, 60, 1.1), (520, 30, .9), (700, 50, 1), (760, 200, .8), (40, 220, .9)]), lights(),
     igloo(690, 332, .8, glow=True),
     f'<path filter="url(#p)" d="M0 340 Q200 210 420 230 Q620 250 800 360 V600 H0Z" fill="{SNOW}"/>',
     f'<ellipse cx="720" cy="340" rx="130" ry="22" fill="{SNOW}"/>',
     f'<path d="M0 470 Q400 430 800 480 V600 H0Z" fill="{SNOW_D}" opacity=".5"/>',
     ground_shadow(260, 80, 486), ground_shadow(520, 70, 482),
     raven(260, 482, True, boots=True), owl(520, 478, 1)])
