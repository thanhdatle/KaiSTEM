#!/usr/bin/env python3
"""Generates the 13 Rabbit-and-Coyote-and-the-Moon-Cheese flip-book SVGs from shared character parts.

Usage: python3 coyote_gen.py <output-dir>
Scale rule: every near-ground character is drawn at scene scale S, and the rabbit is always
RAB (0.7) of the coyote's size, so Rabbit stays small and Coyote stays big on every page.
The pond shrinks as Coyote drinks (level 1 → .82 → .62 → .45), but the moon's reflection stays.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
FUR, FUR_D, FUR_L, TIP = "#C9A27A", "#9C7656", "#EEDCC0", "#3A2E28"      # Coyote: tan, black-tipped tail
RAB_F, RAB_D, RAB_L, EAR = "#A8968A", "#857367", "#EFE6DA", "#F2A9B0"     # Rabbit: grey-brown cottontail
MOON, MOON_M, GLOW = "#FBE7A1", "#E3C46E", "#FFF3C4"
POND, POND_D, POND_L, MUD = "#2E4C86", "#233B6C", "#5F82C0", "#5A4440"
NOPAL, NOPAL_L, NOPAL_D, TUNA = "#4E9A62", "#76BE7E", "#3A7A4C", "#E0507A"
GROUND, GROUND_N, GROUND_F = "#C98B5B", "#7E5E58", "#5E4646"
MESA, MESA_N = "#B0687A", "#4B3F70"
DUSK = [(0, "#5B4C9A"), (.55, "#E58C7A"), (1, "#FAD19A")]
EVENING = [(0, "#2A2C66"), (.6, "#8A5E96"), (1, "#E6A08A")]
NIGHT = [(0, "#171C47"), (.6, "#33336F"), (1, "#5E4F86")]
S = 1.3      # scene scale for the near-ground characters
RAB = .7     # Rabbit's size relative to Coyote


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, rot: float = 0, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def eye(cx: float, cy: float, r: float, mood: str) -> str:
    if mood == "sleep":
        return stroke(f"M{cx - r} {cy} q{r} {r * .9} {2 * r} 0", INK, r * .55)
    if mood == "wide":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r * 1.25}" fill="#fff"/>'
                f'<circle cx="{cx + r * .2}" cy="{cy}" r="{r * .6}" fill="{INK}"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/><circle cx="{cx + r * .25}" cy="{cy + r * .1}" r="{r * .6}" fill="{INK}"/>'
            f'<circle cx="{cx + r * .45}" cy="{cy - r * .2}" r="{r * .2}" fill="#fff"/>')


# ---------- Coyote ----------
def coyote_head(mood: str = "smile", lick: bool = False) -> str:
    """Head drawn around the neck pivot (0, 0), facing right: tall pointed ears, a long narrow snout."""
    mouth = {
        "smile": stroke("M58 -22 q8 6 18 2", INK, 3),
        "grin": '<path d="M54 -24 Q68 -8 82 -24Z" fill="#7A2E2A"/>',
        "oh": '<ellipse cx="70" cy="-20" rx="6" ry="5" fill="#7A2E2A"/>',
        "sleep": stroke("M60 -22 q7 5 14 1", INK, 3),
    }[mood if mood in ("smile", "grin", "oh", "sleep") else "smile"]
    tongue = '<path d="M74 -22 q10 2 10 12 q-8 2 -12 -8Z" fill="#E86F7E"/>' if lick else ""
    e = "sleep" if mood == "sleep" else ("wide" if mood in ("oh", "grin") else "open")
    return (f'<path d="M-24 -4 Q-6 -34 22 -40 L36 -8 Q10 22 -24 16Z" fill="{FUR}"/>'
            f'<path d="M10 -54 L4 -100 L34 -62Z" fill="{FUR_D}"/><path d="M14 -60 L10 -88 L26 -64Z" fill="{EAR}"/>'
            f'<path d="M28 -60 L40 -104 L52 -58Z" fill="{FUR_D}"/><path d="M33 -62 L41 -92 L47 -61Z" fill="{EAR}"/>'
            f'<ellipse cx="30" cy="-38" rx="28" ry="23" fill="{FUR}"/>'
            f'<path d="M40 -54 Q74 -46 90 -32 Q78 -16 44 -18Z" fill="{FUR}"/>'
            f'<path d="M44 -26 Q70 -26 88 -30 Q76 -14 44 -16Z" fill="{FUR_L}"/>'
            f'<path d="M18 -20 Q30 -6 46 -14 Q40 -24 18 -20Z" fill="{FUR_L}"/>'
            f'<ellipse cx="90" cy="-33" rx="6" ry="5" fill="{INK}"/>{tongue}{mouth}'
            + eye(46, -44, 5.5, e) + '<circle cx="38" cy="-27" r="6" fill="#F0705F" opacity=".45"/>')


def coyote_tail(x: float, y: float, rot: float = 0) -> str:
    return (f'<g transform="translate({x} {y}) rotate({rot})"><path d="M0 0 C-40 -10 -72 12 -84 52 C-68 48 -50 40 -36 26 C-24 16 -12 12 0 12Z" fill="{FUR_D}"/>'
            f'<path d="M-84 52 C-82 38 -76 30 -66 26 C-62 36 -66 44 -84 52Z" fill="{TIP}"/></g>')


def coyote(x: float, y: float, s: float = S, pose: str = "stand", belly: float = 0, head: float = 0,
           mood: str = "smile", flip: bool = False, lick: bool = False) -> str:
    """Coyote facing right with feet on y. belly 0..1 is how full of pond water his tummy is."""
    hd = f'<g transform="translate({{px}} {{py}}) rotate({head})">{coyote_head(mood, lick)}</g>'
    by = -70 + 16 * belly
    tum_rx, tum_ry = 46 + 26 * belly, 18 + 28 * belly
    if pose == "sleep":
        inner = (f'<ellipse cy="-40" rx="96" ry="40" fill="{FUR}"/><path d="M-80 -60 Q0 -92 80 -62 Q0 -76 -80 -60Z" fill="{FUR_D}"/>'
                 + f'<ellipse cx="6" cy="-26" rx="{60 + 16 * belly}" ry="{24 + 12 * belly}" fill="{FUR_L}"/>'
                 + f'<ellipse cx="96" cy="-6" rx="22" ry="8" fill="{FUR_D}"/><ellipse cx="-70" cy="-6" rx="26" ry="9" fill="{FUR_D}"/>'
                 + coyote_tail(-84, -16, -140)
                 + hd.format(px=74, py=-26))
    elif pose == "sit":
        inner = (coyote_tail(-30, -14, 200)
                 + f'<ellipse cx="-24" cy="-52" rx="52" ry="48" fill="{FUR}"/><ellipse cx="-30" cy="-46" rx="38" ry="34" fill="{FUR_D}" opacity=".45"/>'
                 + f'<path d="M-30 -90 Q10 -190 58 -150 Q80 -90 52 -30 Q0 -10 -30 -90Z" fill="{FUR}"/>'
                 + f'<ellipse cx="-24" cy="-6" rx="44" ry="10" fill="{FUR_D}"/>'
                 + stroke("M30 -50 L30 -4", FUR, 15) + stroke("M50 -50 L52 -4", FUR_D, 15)
                 + f'<ellipse cx="32" cy="-3" rx="12" ry="6" fill="{FUR}"/><ellipse cx="55" cy="-3" rx="12" ry="6" fill="{FUR_D}"/>'
                 + f'<ellipse cx="18" cy="{-66 + 22 * belly}" rx="{30 + 34 * belly}" ry="{30 + 32 * belly}" fill="{FUR}"/>'
                 + f'<ellipse cx="22" cy="{-62 + 22 * belly}" rx="{20 + 28 * belly}" ry="{22 + 26 * belly}" fill="{FUR_L}"/>'
                 + hd.format(px=36, py=-142))
    else:  # stand / drink / waddle
        sway = 8 if pose == "waddle" else 0
        legs = (stroke(f"M-46 -72 L{-54 - sway} -2", FUR_D, 16) + stroke(f"M46 -72 L{52 - sway} -2", FUR_D, 16)
                + stroke(f"M-28 -72 L{-30 + sway} -2", FUR, 16) + stroke(f"M60 -72 L{66 + sway} -2", FUR, 16)
                + "".join(f'<ellipse cx="{cx}" cy="-2" rx="11" ry="6" fill="{c}"/>'
                          for cx, c in ((-56 - sway, FUR_D), (54 - sway, FUR_D), (-28 + sway, FUR), (68 + sway, FUR))))
        dip = 7 if pose == "drink" else 0   # drinking: shoulders dip forward, neck goes low
        inner = (coyote_tail(-62, -98, -6 - dip) + legs
                 + f'<g transform="rotate({dip} 60 -72)"><ellipse cy="-90" rx="74" ry="32" fill="{FUR}"/><path d="M-66 -104 Q0 -130 70 -104 Q0 -116 -66 -104Z" fill="{FUR_D}"/></g>'
                 + f'<ellipse cx="6" cy="{by}" rx="{tum_rx + 6}" ry="{tum_ry + 6}" fill="{FUR}"/>'
                 + f'<ellipse cx="8" cy="{by + 2}" rx="{tum_rx}" ry="{tum_ry}" fill="{FUR_L}"/>'
                 + (f'<path d="M30 -112 Q70 -112 84 -66 L62 -52 Q44 -80 20 -84Z" fill="{FUR}"/>' if dip else
                    f'<ellipse cx="54" cy="-104" rx="24" ry="22" fill="{FUR}"/>')
                 + (hd.format(px=76, py=-62) if dip else hd.format(px=62, py=-106)))
    return group(x, y, s, flip, inner)


# ---------- Rabbit ----------
def rabbit_head(mood: str = "smile") -> str:
    m = {"smile": stroke("M20 4 q4 4 9 1", INK, 2.2), "oh": '<ellipse cx="24" cy="6" rx="3.5" ry="4" fill="#7A2E2A"/>',
         "big": '<path d="M18 3 Q24 13 31 3Z" fill="#7A2E2A"/>'}.get(mood, stroke("M20 4 q4 4 9 1", INK, 2.2))
    e = "sleep" if mood == "sleep" else "open"
    return (f'<ellipse cx="-4" cy="-48" rx="9" ry="32" fill="{RAB_D}" transform="rotate(-14 -4 -22)"/>'
            f'<ellipse cx="-4" cy="-48" rx="4.5" ry="24" fill="{EAR}" transform="rotate(-14 -4 -22)"/>'
            f'<ellipse cx="12" cy="-48" rx="9" ry="32" fill="{RAB_F}" transform="rotate(8 12 -22)"/>'
            f'<ellipse cx="12" cy="-48" rx="4.5" ry="24" fill="{EAR}" transform="rotate(8 12 -22)"/>'
            f'<circle cx="6" cy="-6" r="21" fill="{RAB_F}"/><ellipse cx="18" cy="2" rx="12" ry="9" fill="{RAB_L}"/>'
            + eye(14, -12, 5, e) + f'<path d="M26 -4 l5 2 l-5 3Z" fill="{EAR}"/>'
            + '<circle cx="8" cy="0" r="4.5" fill="#F0705F" opacity=".45"/>' + m
            + stroke("M30 0 l14 -4 M30 3 l14 3", "#F3EBDF", 1.4))


def rabbit(x: float, y: float, s: float = S, pose: str = "sit", mood: str = "smile", flip: bool = False,
           head: float = 0) -> str:
    """Señor Conejo, facing right, feet on y; always drawn at RAB of Coyote's scale."""
    arm = f'<ellipse cx="22" cy="-6" rx="8" ry="5" fill="{RAB_F}"/>'
    if pose == "point":
        arm = stroke("M16 -34 L58 -44", RAB_D, 10) + f'<circle cx="60" cy="-44" r="7" fill="{RAB_D}"/>'
    elif pose == "wave":
        arm = stroke("M16 -34 L34 -66", RAB_D, 10) + f'<circle cx="35" cy="-70" r="7" fill="{RAB_D}"/>'
    leg = f'<ellipse cx="-2" cy="-4" rx="26" ry="7" fill="{RAB_D}"/>'
    tilt = 0
    if pose == "hop":
        leg = stroke("M-16 -16 L-48 -2", RAB_D, 12) + f'<ellipse cx="-52" cy="-2" rx="12" ry="5" fill="{RAB_D}"/>'
        arm = stroke("M18 -22 L36 -12", RAB_F, 9)
        tilt = -14
    elif pose == "tiptoe":
        leg = stroke("M-8 -14 L-14 0", RAB_D, 10) + stroke("M4 -14 L8 0", RAB_D, 10)
        tilt = 10
    body = (f'<circle cx="-32" cy="-28" r="11" fill="#fff"/>'
            f'<ellipse cy="-30" rx="32" ry="28" fill="{RAB_F}"/><ellipse cx="-10" cy="-22" rx="24" ry="20" fill="{RAB_D}"/>'
            + leg + f'<ellipse cx="14" cy="-26" rx="13" ry="18" fill="{RAB_L}"/>'
            + f'<g transform="translate(22 -54) rotate({head})">{rabbit_head(mood)}</g>' + arm)
    inner = f'<g transform="rotate({tilt} 0 -20)">{body}</g>' if tilt else body
    return group(x, y, s * RAB, flip, inner)


def burrow_rabbit(x: float, y: float, s: float = S) -> str:
    """Just Rabbit's head and paws peeking out of his burrow, looking up."""
    inner = (f'<g transform="translate(0 -18) rotate(-22)">{rabbit_head("smile")}</g>'
             f'<ellipse cx="-6" cy="4" rx="9" ry="6" fill="{RAB_F}"/><ellipse cx="18" cy="4" rx="9" ry="6" fill="{RAB_F}"/>')
    return group(x, y, s * RAB, False, inner)


# ---------- the moon, the pond, the desert ----------
def moon(x: float, y: float, r: float, rabbit_op: float = .1) -> str:
    """The full moon, pale cheese-yellow, with the shape of a rabbit in its shadows."""
    k = r / 100
    bunny = (f'<g transform="translate({x} {y}) scale({k})" fill="{MOON_M}" opacity="{rabbit_op}">'
             '<ellipse cx="-14" cy="22" rx="40" ry="30"/><circle cx="-54" cy="24" r="10"/><circle cx="26" cy="-6" r="20"/>'
             '<ellipse cx="18" cy="-50" rx="8" ry="30" transform="rotate(-14 18 -50)"/><ellipse cx="36" cy="-48" rx="8" ry="28" transform="rotate(12 36 -48)"/>'
             '<ellipse cx="20" cy="50" rx="18" ry="7"/><circle cx="-60" cy="-40" r="7"/><circle cx="56" cy="44" r="6"/></g>')
    return (f'<circle cx="{x}" cy="{y}" r="{r * 1.9:.0f}" fill="{GLOW}" opacity=".08"/><circle cx="{x}" cy="{y}" r="{r * 1.4:.0f}" fill="{GLOW}" opacity=".14"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MOON}"/>' + bunny)


def pond(x: float, y: float, rx: float, ry: float, level: float = 1, refl: tuple = None, shine: str = MOON) -> str:
    """A desert pond: a wet mud bank, then the water, which shrinks with `level`. refl=(dx, r) puts the moon in it."""
    wx, wy = rx * level, ry * level
    out = (f'<ellipse cx="{x}" cy="{y}" rx="{rx + 14}" ry="{ry + 8}" fill="{MUD}" filter="url(#p)"/>'
           f'<ellipse cx="{x}" cy="{y + 2}" rx="{rx}" ry="{ry}" fill="#4A3836"/>'
           f'<ellipse cx="{x}" cy="{y + (ry - wy) * .5:.1f}" rx="{wx:.1f}" ry="{wy:.1f}" fill="{POND}"/>'
           f'<ellipse cx="{x}" cy="{y + (ry - wy) * .5 + wy * .25:.1f}" rx="{wx * .9:.1f}" ry="{wy * .6:.1f}" fill="{POND_D}" opacity=".5"/>')
    if refl:
        dx, r = refl
        cy = y + (ry - wy) * .5
        out += (f'<ellipse cx="{x + dx}" cy="{cy:.1f}" rx="{r * 1.5:.0f}" ry="{r * .7:.0f}" fill="{shine}" opacity=".18"/>'
                f'<ellipse cx="{x + dx}" cy="{cy:.1f}" rx="{r}" ry="{r * .46:.1f}" fill="{shine}"/>'
                + stroke(f"M{x + dx - r * .7:.0f} {cy - r * .1:.0f} h{r * 1.4:.0f} M{x + dx - r * .5:.0f} {cy + r * .2:.0f} h{r:.0f}", POND_L, 3))
    out += stroke(f"M{x - wx * .7:.0f} {y + (ry - wy) * .5 - wy * .5:.0f} q{wx * .2:.0f} -6 {wx * .4:.0f} 0", POND_L, 3)
    return out


def ripples(x: float, y: float, n: int = 2) -> str:
    return "".join(f'<ellipse cx="{x}" cy="{y}" rx="{16 + 16 * i}" ry="{5 + 5 * i}" fill="none" stroke="{POND_L}" stroke-width="3" opacity="{.9 - .3 * i}"/>'
                   for i in range(n))


def nopal(x: float, y: float, s: float = 1, flip: bool = False, fruit: bool = True, night: bool = True) -> str:
    """A prickly-pear cactus: flat oval pads stacked on pads, with spine dots and pink tuna fruit."""
    pads = [(0, -50, 30, 50, 0), (-38, -116, 24, 40, -28), (34, -124, 26, 42, 22), (-4, -178, 20, 34, 6), (62, -176, 16, 28, 34)]
    body = ""
    for dx, dy, rx, ry, rot in pads:
        body += (f'<ellipse cx="{dx}" cy="{dy}" rx="{rx}" ry="{ry}" fill="{NOPAL}" transform="rotate({rot} {dx} {dy})"/>'
                 f'<ellipse cx="{dx - rx * .2:.0f}" cy="{dy - ry * .15:.0f}" rx="{rx * .62:.0f}" ry="{ry * .7:.0f}" fill="{NOPAL_L}" opacity=".45" transform="rotate({rot} {dx} {dy})"/>')
        body += "".join(f'<circle cx="{dx + ox * rx:.0f}" cy="{dy + oy * ry:.0f}" r="2.2" fill="{CREAM}"/>'
                        for ox, oy in ((-.4, -.4), (.35, -.2), (-.1, .2), (.4, .45), (-.45, .5), (.05, -.7)))
    if fruit:
        body += "".join(f'<ellipse cx="{a}" cy="{b}" rx="8" ry="10" fill="{TUNA}"/>' for a, b in ((-8, -214), (8, -210), (44, -164), (70, -202)))
    body += f'<path d="M-30 -2 Q0 -12 30 -2Z" fill="{NOPAL_D}"/>'
    return group(x, y, s, flip, body)


def star(x: float, y: float, s: float = 1) -> str:
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def stars(pts: list) -> str:
    return "".join(star(a, b, c) for a, b, c in pts)


def mesas(y: float, col: str) -> str:
    return (f'<path d="M0 {y} L0 {y - 60} L70 {y - 60} L96 {y - 30} L220 {y - 30} L250 {y - 100} L370 {y - 100} L400 {y - 40} '
            f'L520 {y - 40} L548 {y - 86} L640 {y - 86} L670 {y - 34} L800 {y - 50} V{y}Z" fill="{col}"/>')


def ground(y: float, col: str, amp: float = 16) -> str:
    return f'<path filter="url(#p)" d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{col}"/>'


def front(col: str = GROUND_F) -> str:
    return f'<path d="M0 600 V570 Q400 548 800 576 V600Z" fill="{col}"/>'


def pebbles(pts: list, col: str = "#9A7A70") -> str:
    return "".join(f'<ellipse cx="{a}" cy="{b}" rx="{c}" ry="{c * .55:.1f}" fill="{col}"/>' for a, b, c in pts)


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def slosh(x: float, y: float) -> str:
    """Little wavy water lines for a sloshing tummy."""
    return marks([f"M{x} {y} q8 -8 16 0 q8 8 16 0", f"M{x + 6} {y + 16} q8 -8 16 0 q8 8 16 0"], "#BFD7FF", 4)


def zzz(x: float, y: float) -> str:
    return marks([f"M{x} {y} h16 l-16 16 h16", f"M{x + 26} {y - 30} h12 l-12 12 h12", f"M{x + 46} {y - 54} h9 l-9 9 h9"], CREAM, 3.4)


def footprints(pts: list) -> str:
    return "".join(f'<g transform="translate({a} {b}) rotate({r})" fill="#4A3836"><ellipse cx="0" cy="0" rx="{4 * k}" ry="{8 * k}"/><ellipse cx="{10 * k}" cy="{-3 * k}" rx="{4 * k}" ry="{8 * k}"/></g>'
                   for a, b, r, k in pts)


DEFS = {"s": '<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="#FFF3C4"/>'}


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(body)
    defs = "".join(d for k, d in DEFS.items() if f'href="#{k}"' in joined)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>{defs}'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/coyote-{n:02d}.svg", "w") as fh:
        fh.write(doc)


SKY_STARS = stars([(60, 60, 1.2), (180, 40, .8), (300, 90, 1), (420, 40, .7), (120, 160, .7), (360, 170, .6), (740, 220, .7), (250, 220, .6)])
NIGHT_BACK = [SKY_STARS, mesas(400, MESA_N)]
POND_X, POND_Y, POND_RX, POND_RY = 560, 500, 190, 52

# 01 cover — Coyote gazes into the pond at the moon's reflection while Rabbit points
svg(1, "Rabbit and Coyote and the Moon Cheese", "Paper-cut cover: under a deep blue starry sky, a big round pale-yellow full moon shines over a desert valley with flat-topped mesas and prickly-pear cactus. A tall tan coyote with pointed ears and a black-tipped bushy tail leans over a pond, licking his lips at the moon's round reflection in the water, while a little grey-brown rabbit beside a cactus points at it.", NIGHT, [
    *NIGHT_BACK, moon(600, 130, 70), ground(420, GROUND_N, 12), nopal(90, 470, 1.1),
    pond(POND_X, POND_Y, POND_RX, POND_RY, 1, (40, 46)),
    coyote(250, 500, 1.15, "stand", 0, 46, "smile", lick=True),
    nopal(745, 455, .8, True), rabbit(730, 540, 1.15, "point", "big", True), front()])

# 02 Señor Conejo, the quick little rabbit
svg(2, "Señor Conejo", "Paper-cut scene at sunset: in a dry, dusty valley with pink flat-topped mesas, a little grey-brown rabbit with long pink-lined ears and a white cotton tail hops happily between two prickly-pear cactuses covered in pink fruit.", DUSK, [
    f'<circle cx="440" cy="320" r="70" fill="#FFD27A" opacity=".85"/>', mesas(390, MESA), ground(410, GROUND, 14),
    nopal(150, 440, .8), nopal(650, 436, .75, True),
    pebbles([(330, 540, 9), (520, 560, 7), (720, 540, 8), (90, 560, 7)], "#B07A50"),
    rabbit(420, 520, 1.8, "hop", "big"), marks(["M270 470 q-12 -18 -28 -12", "M292 444 q-12 -18 -28 -12"], CREAM, 4),
    front("#A9704A")])

# 03 Señor Coyote, always hungry
svg(3, "Señor Coyote", "Paper-cut scene at dusk, with the full moon rising over the mesas: a tall tan coyote with big pointed ears, a long snout and a bushy black-tipped tail stands by a prickly-pear cactus, his hungry tummy rumbling as he looks around for something to eat.", EVENING, [
    stars([(80, 60, 1), (220, 40, .7), (700, 50, .8)]), moon(620, 250, 56), mesas(400, "#7A5280"), ground(420, "#9C6E5C", 14),
    nopal(700, 480, 1.0, True), coyote(330, 500, S, "stand", .1, -6, "oh"),
    marks(["M318 470 q8 -8 16 0 q8 8 16 0", "M310 492 q8 -8 16 0 q8 8 16 0"], CREAM, 3.4),
    pebbles([(120, 540, 8), (560, 560, 7)], "#7A5450"), front("#6E4C46")])

# 04 Coyote jumps out at Rabbit
svg(4, "Aha, Rabbit!", "Paper-cut night scene under a starry sky and a big full moon: a tall tan coyote jumps out from behind a prickly-pear cactus, grinning at a little grey-brown rabbit, who sits up in surprise with his long ears standing straight up. The rabbit is less than half the coyote's size.", NIGHT, [
    *NIGHT_BACK, moon(140, 120, 62), ground(420, GROUND_N, 12), nopal(330, 470, 1.2),
    coyote(300, 512, S, "stand", 0, -8, "grin"), rabbit(620, 512, S, "sit", "oh", True),
    marks(["M560 380 l-10 -14", "M590 370 v-18", "M620 380 l10 -14"], CREAM, 3.4), front()])

# 05 Rabbit points at the "cheese" in the pond
svg(5, "A big round cheese", "Paper-cut night scene: the little rabbit, standing on the bank, points down at the round pale-yellow reflection of the full moon in a dark blue pond, while the tall coyote turns his head to look. The real moon shines above in the starry sky.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12), nopal(80, 470, 1.0),
    pond(POND_X, POND_Y, POND_RX, POND_RY, 1, (40, 42)),
    coyote(200, 500, S, "stand", 0, 18, "oh"), rabbit(380, 522, S, "point", "big"), front()])

# 06 Coyote peers in, licking his lips
svg(6, "Mmm, cheese!", "Paper-cut night scene: the tall coyote leans over the edge of the pond, licking his lips at the round shining yellow shape in the water, the moon's reflection. The little rabbit sits on the bank beside him, smiling, and the real full moon glows in the sky above.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12), nopal(740, 450, .9, True),
    pond(POND_X, POND_Y, POND_RX, POND_RY, 1, (40, 42)),
    coyote(250, 500, S, "stand", 0, 46, "smile", lick=True), rabbit(110, 526, S, "sit", "smile"), front()])

# 07 Slurp, slurp, slurp — the pond starts to go down
svg(7, "Slurp, slurp, slurp!", "Paper-cut night scene: the coyote has his nose in the pond and is drinking, making ripples. The water has gone down a little, showing a ring of wet mud around the edge, and his tummy is getting rounder. The moon's yellow reflection still shines in the middle of the pond. The little rabbit sits on the bank, cheering him on.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12), nopal(740, 450, .9, True),
    pond(POND_X, POND_Y, POND_RX, POND_RY, .82, (40, 38)), ripples(432, 468),
    coyote(268, 500, S, "drink", .35, 45, "smile"), rabbit(100, 526, S, "wave", "big"),
    marks(["M380 380 v-16", "M404 386 l8 -14"], CREAM, 3.4), front()])

# 08 still slurping — Rabbit tiptoes away
svg(8, "Rabbit tiptoes away", "Paper-cut night scene: the coyote keeps drinking with his eyes on the pond, and his tummy is now very round. The pond is smaller, with a wide ring of wet mud, but the moon's reflection is still shining in it. Behind the coyote's back, the little rabbit tiptoes quietly away toward the cactus.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12), nopal(90, 460, 1.0),
    pond(POND_X, POND_Y, POND_RX, POND_RY, .62, (30, 32)), ripples(474, 478),
    coyote(312, 506, S, "drink", .7, 45, "smile"), rabbit(140, 528, S, "tiptoe", "smile", True),
    marks(["M170 548 q6 -8 12 0", "M196 552 q6 -8 12 0"], CREAM, 3), front()])

# 09 Coyote can't drink one more drop
svg(9, "Slosh, slosh!", "Paper-cut night scene: the coyote sits back on the bank with an enormous round tummy full of pond water, looking very surprised; wavy lines show the water sloshing inside. The pond has shrunk to a small puddle, and the moon's yellow reflection still shines in it. The rabbit is nowhere to be seen.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12), nopal(80, 460, .95),
    pond(POND_X, POND_Y, POND_RX, POND_RY, .45, (14, 26)),
    coyote(300, 520, S, "sit", 1.0, -4, "oh"), slosh(330, 430), slosh(250, 450), front()])

# 10 Rabbit is gone — only footprints, and the "cheese" is still in the pond
svg(10, "Where is Rabbit?", "Paper-cut night scene: the coyote, with his huge round tummy, looks around in surprise. A trail of little rabbit footprints leads away up the hill, where the rabbit, tiny in the distance, waves goodbye from beside a cactus. In the small pond the moon's reflection still shines, just like the real moon above.", NIGHT, [
    *NIGHT_BACK, moon(600, 120, 62), ground(420, GROUND_N, 12),
    nopal(90, 412, .38), rabbit(130, 414, .5, "wave", "big"),
    footprints([(170, 432, 30, .6), (200, 452, 30, .7), (236, 474, 26, .8), (276, 498, 22, .9)]),
    pond(380, POND_Y + 10, POND_RX, POND_RY, .45, (14, 26)),
    coyote(650, 540, S, "sit", 1.0, 0, "oh", True), slosh(620, 440), front()])

# 11 Coyote waddles home
svg(11, "Waddle, waddle home", "Paper-cut night scene: the coyote waddles slowly home across the desert past the prickly-pear cactus, his tummy so round and full of water that it nearly touches the ground. Wavy lines show the water sloshing inside, and the full moon lights his way.", NIGHT, [
    *NIGHT_BACK, moon(160, 120, 62), ground(420, GROUND_N, 12), nopal(660, 470, 1.05, True),
    coyote(360, 520, S, "waddle", 1.0, -4, "smile"), slosh(330, 470), slosh(400, 480),
    marks(["M150 470 q-8 -10 -20 -6", "M160 500 q-8 -10 -20 -6"], CREAM, 3.4),
    pebbles([(120, 560, 8), (560, 560, 7), (720, 546, 6)], "#9A7A70"), front()])

# 12 Coyote fast asleep, too full to be hungry
svg(12, "Too full to be hungry", "Paper-cut night scene: the coyote is curled up fast asleep under a prickly-pear cactus, smiling, with his round full tummy and his bushy tail wrapped around him. Little Zs float up toward the full moon.", NIGHT, [
    *NIGHT_BACK, moon(620, 120, 62), ground(420, GROUND_N, 12), nopal(160, 480, 1.2),
    coyote(420, 520, S, "sleep", 1.0, 12, "sleep"), zzz(640, 330), front()])

# 13 Rabbit, safe at home, sees a rabbit in the moon
svg(13, "The rabbit in the moon", "Paper-cut night scene: an enormous pale-yellow full moon fills the starry sky, and in its shadows you can see the shape of a rabbit. Down below, the little grey-brown rabbit peeks happily out of his burrow beside a prickly-pear cactus and looks up at it.", NIGHT, [
    SKY_STARS, stars([(600, 40, 1), (720, 90, .8), (520, 300, .6)]), moon(420, 200, 150, .7), mesas(430, MESA_N),
    ground(450, GROUND_N, 12), nopal(560, 500, 1.0, True),
    f'<ellipse cx="300" cy="530" rx="96" ry="38" fill="#3A2A2A" filter="url(#p)"/>',
    burrow_rabbit(300, 526, 2.4), f'<path d="M200 540 Q300 570 400 540 Q300 590 200 540Z" fill="{GROUND_N}"/>', front()])
