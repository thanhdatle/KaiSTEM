#!/usr/bin/env python3
"""Generates the 13 Anansi flip-book SVGs from shared character parts."""
import random
import sys

OUT = sys.argv[1]
BR, LEG, SCARF, CREAM, GOLD = "#4A2E22", "#3A241B", "#E4572E", "#F6E7D0", "#F6C445"
INK, LEO, PY, SILVER = "#2B2320", "#E9B37A", "#4F9A46", "#DADDE8"
NIGHT = [(0, "#1B1E4E"), (1, "#454A96")]
REALM = [(0, "#F6B98A"), (1, "#FBE9C8")]
FOREST = [(0, "#A9D8C4"), (1, "#EEF3D6")]
CLIMB = [(0, "#F6B98A"), (1, "#9FD3D6")]

LEGS = {
    "L1": "M-14 -2 Q-40 -22 -46 -2", "L2": "M-19 6 Q-48 -4 -54 18",
    "L3": "M-19 14 Q-46 16 -50 36", "L4": "M-13 24 Q-32 34 -34 50",
    "R1": "M14 -2 Q40 -22 46 -2", "R2": "M19 6 Q48 -4 54 18",
    "R3": "M19 14 Q46 16 50 36", "R4": "M13 24 Q32 34 34 50",
}


def stroke(d, col=LEG, w=5):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def anansi(x, y, s=1, rot=0, look=(0, 0), legs=None, extra="", mouth="smile"):
    lg = dict(LEGS)
    lg.update(legs or {})
    lx, ly = look
    m = ('<path d="M-5 -15 Q0 -8 5 -15Z" fill="#F2859A"/>' if mouth == "open"
         else stroke("M-5 -15 Q0 -10 5 -15", CREAM, 2))
    eyes = "".join(
        f'<circle cx="{ex}" cy="-25" r="7" fill="#fff"/><circle cx="{ex + lx}" cy="{-25 + ly}" r="3.4" fill="{INK}"/>'
        f'<circle cx="{ex + lx + 1.2}" cy="{-26.4 + ly}" r="1.1" fill="#fff"/>' for ex in (-7.5, 7.5))
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)">'
            + stroke(" ".join(v for v in lg.values() if v))
            + f'<circle cy="8" r="22" fill="{BR}"/><ellipse cy="13" rx="12" ry="10" fill="#6B4433"/>'
            + f'<circle cy="-22" r="17" fill="{BR}"/>'
            + f'<path d="M-16 -11 Q0 -3 16 -11 L15 -3 Q0 5 -15 -3Z M11 -4 L26 8 L19 13 L7 2Z" fill="{SCARF}"/>'
            + stroke("M-7 -7 l-1 7 M7 -7 l1 7 M18 3 l-5 4 M1 -6 v7", CREAM, 2.4)
            + eyes + m + extra + '</g>')


def star(x, y, s=1):
    return f'<use href="#s" transform="translate({x} {y}) scale({s})"/>'


def firefly(x, y, s=1):
    return (f'<circle cx="{x}" cy="{y}" r="{10 * s:.1f}" fill="{GOLD}" opacity=".28"/>'
            f'<circle cx="{x}" cy="{y}" r="{3.6 * s:.1f}" fill="#FBE48A"/>')


def glow(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" opacity=".12"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * .62:.0f}" fill="{GOLD}" opacity=".2"/>')


def box(x, y, s=1, opened=False, g=True):
    back = ""
    lid = f'<rect x="-34" y="-26" width="68" height="16" rx="6" fill="{GOLD}"/><circle cy="-10" r="5" fill="#FBE48A" stroke="#B5781A" stroke-width="2"/>'
    if opened:
        lid = '<ellipse cy="-14" rx="28" ry="7" fill="#FFF3C0"/>'
        back = '<path d="M-31 -12 L-24 -46 Q-23 -52 -16 -52 H30 Q38 -52 37 -45 L31 -12Z" fill="#D9981C"/>'
    return ((glow(x, y, 80 * s) if g else "")
            + f'<g transform="translate({x} {y}) scale({s})">'
            + back + '<rect x="-30" y="-14" width="60" height="38" rx="5" fill="#E9A91F"/>'
            + stroke("M-26 9 l6.5 -8 l6.5 8 l6.5 -8 l6.5 8 l6.5 -8 l6.5 8 l6.5 -8 l6.5 8", "#B5781A", 2.5)
            + lid + '</g>')


def cloud(x, y, s=1, fill="#FFF6E6", shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}"{f}>'
            '<circle cx="-50" cy="8" r="30"/><circle cx="-18" cy="-14" r="36"/><circle cx="24" cy="-10" r="32"/>'
            '<circle cx="56" cy="10" r="28"/><rect x="-78" y="6" width="160" height="34" rx="17"/></g>')


def nyame(x, y, R, mood="kind"):
    """A sun-and-cloud presence: warm disc, rays, kind eyes. No human features beyond eyes and a smile."""
    c = "#7A4A2A"
    rays = "".join(
        f'<path d="M{-.13 * R:.0f} {-1.1 * R:.0f} L0 {-1.42 * R:.0f} L{.13 * R:.0f} {-1.1 * R:.0f}Z" transform="rotate({30 * i})"/>'
        for i in range(12))
    a, b, e, w = .32 * R, .1 * R, .09 * R, max(3, R * .035)
    if mood == "laugh":
        eyes = stroke(f"M{-a - e:.0f} {-b:.0f} q{e:.0f} {-e * 1.3:.0f} {2 * e:.0f} 0 M{a - e:.0f} {-b:.0f} q{e:.0f} {-e * 1.3:.0f} {2 * e:.0f} 0", c, w)
        mouth = f'<path d="M{-.3 * R:.0f} {.2 * R:.0f} Q0 {.62 * R:.0f} {.3 * R:.0f} {.2 * R:.0f}Z" fill="{c}"/>'
    elif mood == "calm":
        eyes = stroke(f"M{-a - e:.0f} {-b:.0f} q{e:.0f} {e:.0f} {2 * e:.0f} 0 M{a - e:.0f} {-b:.0f} q{e:.0f} {e:.0f} {2 * e:.0f} 0", c, w)
        mouth = stroke(f"M{-.16 * R:.0f} {.26 * R:.0f} Q0 {.36 * R:.0f} {.16 * R:.0f} {.26 * R:.0f}", c, w)
    else:
        big = 1.5 if mood == "amazed" else 1
        eyes = "".join(
            f'<circle cx="{sx * a:.0f}" cy="{-b:.0f}" r="{e * big:.0f}" fill="#fff"/><circle cx="{sx * a:.0f}" cy="{-b + e * .3:.0f}" r="{e * .55 * big:.0f}" fill="{c}"/>'
            for sx in (-1, 1))
        mouth = (f'<ellipse cy="{.34 * R:.0f}" rx="{.1 * R:.0f}" ry="{.13 * R:.0f}" fill="{c}"/>' if mood == "amazed"
                 else stroke(f"M{-.22 * R:.0f} {.24 * R:.0f} Q0 {.44 * R:.0f} {.22 * R:.0f} {.24 * R:.0f}", c, w))
    cheeks = "".join(f'<circle cx="{sx * .52 * R:.0f}" cy="{.16 * R:.0f}" r="{.11 * R:.0f}" fill="#F08A7A" opacity=".45"/>' for sx in (-1, 1))
    return (f'<g transform="translate({x} {y})"><circle r="{1.7 * R:.0f}" fill="#FBD9A8" opacity=".35"/>'
            f'<g fill="#F4A261">{rays}</g><circle r="{R}" fill="#F8BE85" filter="url(#p)"/><circle r="{.86 * R:.0f}" fill="#FBD3A4"/>'
            + eyes + cheeks + mouth + '</g>')


def snake(d, hx, hy, rot=0, w=32, mood="proud"):
    eye = (stroke("M-2 -6 q6 -6 12 0", INK, 2.6) if mood == "proud"
           else f'<circle cx="4" cy="-7" r="6" fill="#fff"/><circle cx="6" cy="-7" r="2.8" fill="{INK}"/>')
    return (stroke(d, PY, w) + f'<path d="{d}" stroke="#9BD37A" stroke-width="{w * .3:.0f}" fill="none" stroke-linecap="round" stroke-dasharray="1 {w * .95:.0f}"/>'
            f'<g transform="translate({hx} {hy}) rotate({rot})" filter="url(#p)">'
            + stroke("M24 3 l12 -1 l6 -5 m-6 5 l7 4", "#E0566B", 2.4)
            + f'<ellipse rx="27" ry="20" fill="{PY}"/><circle cx="10" cy="5" r="5" fill="#F2A9B0" opacity=".7"/>'
            + eye + stroke("M8 10 Q18 13 25 4", "#2F5E2A", 2.6) + '</g>')


def leopard(x, y, s=1, rot=0, mood="proud"):
    spots = [(-40, -14), (-18, -22), (6, -16), (28, -8), (-28, 6), (-4, 6), (20, 12), (-52, 0), (44, 12), (-8, -6), (52, -60), (74, -62)]
    eyes = (stroke("M46 -40 q5 -5 10 0 M68 -40 q5 -5 10 0", INK, 2.6) if mood == "proud" else
            f'<circle cx="51" cy="-40" r="3.4" fill="{INK}"/><circle cx="73" cy="-40" r="3.4" fill="{INK}"/>')
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)">'
            + stroke("M-64 -6 Q-104 -10 -100 -50 Q-98 -62 -90 -60", LEO, 10) + f'<circle cx="-90" cy="-60" r="6.5" fill="#5B3A22"/>'
            + '<g fill="#D49C62"><rect x="-36" y="18" width="14" height="40" rx="7"/><rect x="46" y="18" width="14" height="40" rx="7"/></g>'
            + f'<g fill="{LEO}"><rect x="-54" y="18" width="15" height="42" rx="7"/><rect x="28" y="18" width="15" height="42" rx="7"/>'
            + '<ellipse rx="70" ry="36"/><circle cx="43" cy="-58" r="10"/><circle cx="81" cy="-60" r="10"/><circle cx="62" cy="-34" r="30"/></g>'
            + '<ellipse cx="62" cy="-22" rx="17" ry="12" fill="#FBF3E6"/><path d="M57 -30 h10 l-5 6z" fill="#8C3B3B"/>'
            + '<g fill="#5B3A22">' + "".join(f'<circle cx="{a}" cy="{b}" r="5"/>' for a, b in spots) + '</g>'
            + eyes + stroke("M55 -19 Q62 -13 69 -19", "#5B3A22", 2.4) + '</g>')


def hornet(x, y, s=1, rot=0):
    return f'<use href="#h" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def hornet_def():
    return ('<g id="h">'
            '<g fill="#fff" opacity=".9"><ellipse cx="-4" cy="-10" rx="6" ry="10" transform="rotate(-25 -4 -10)"/><ellipse cx="5" cy="-10" rx="6" ry="10" transform="rotate(15 5 -10)"/></g>'
            '<ellipse rx="12" ry="9" fill="#F08A3C"/>' + stroke("M-4 -8 V8 M3 -8.5 V8.5", BR, 3)
            + f'<circle cx="12" r="7" fill="#F5A65B"/><circle cx="14" cy="-2" r="1.8" fill="{INK}"/>'
            + stroke("M11 3 q3 2 5 -1", BR, 1.4) + '</g>')


def gourd(x, y, s=1, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#p)">'
            '<ellipse cy="12" rx="40" ry="36" fill="#C98B4A"/><ellipse cy="-28" rx="22" ry="20" fill="#C98B4A"/>'
            + stroke("M-36 0 Q0 12 36 0", "#A56C34", 4) + stroke("M-22 20 q-6 -14 4 -26", "#DDA868", 5)
            + '<ellipse cy="-45" rx="15" ry="7" fill="#5B3A22"/></g>')


def hand(x, y, s=1):
    """Nyame's cloud hand: fingers to the right, arm trailing up-left."""
    pts = [(-170, -95, 54), (-110, -60, 46), (-55, -25, 42), (0, 0, 44), (48, -14, 20), (58, 8, 20), (50, 30, 19), (8, -44, 18)]
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#FFF6E6" filter="url(#p)">'
            + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>')


def hut(x, y, s=1, lit=False, wall="#2F3570", roof="#141A40"):
    win = GOLD if lit else roof
    return ((f'<circle cx="{x}" cy="{y - 11 * s:.0f}" r="{16 * s:.0f}" fill="{GOLD}" opacity=".22"/>' if lit else "")
            + f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-22" width="36" height="22" rx="3" fill="{wall}"/>'
            f'<path d="M-26 -20 L0 -48 L26 -20Z" fill="{roof}"/><rect x="-5" y="-16" width="10" height="10" rx="2" fill="{win}"/></g>')


def hill(y, amp, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<path{f} d="M0 {y} Q200 {y - amp} 400 {y} T800 {y} V600 H0Z" fill="{fill}"/>'


def stars(seed, n, ymax):
    r = random.Random(seed)
    return '<g fill="#F4F1EA" opacity=".85">' + "".join(
        f'<circle cx="{r.randint(10, 790)}" cy="{r.randint(10, ymax)}" r="{r.choice([1.5, 2, 2, 2.6])}"/>' for _ in range(n)) + '</g>'


def blobs(pts, fill, shadow=True):
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g fill="{fill}"{f}>' + "".join(f'<circle cx="{a}" cy="{b}" r="{r}"/>' for a, b, r in pts) + '</g>'


def marks(ds, col="#fff", w=4):
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def car(x, y, s=1):
    return (f'<ellipse cx="{x}" cy="{y + 40 * s:.0f}" rx="{100 * s:.0f}" ry="{8 * s:.0f}" fill="#000" opacity=".18"/>'
            f'<g transform="translate({x} {y}) scale({s})" filter="url(#p)">'
            '<path d="M-90 10 Q-90 -14 -64 -18 L-44 -48 Q-38 -58 -24 -58 H34 Q48 -58 56 -46 L72 -18 Q94 -14 94 10 V22 H-90Z" fill="#4A90C2"/>'
            '<path d="M-36 -22 L-22 -48 H2 V-22Z" fill="#2E5F86"/><path d="M10 -22 V-48 H32 L50 -22Z" fill="#DDF1F5"/>'
            '<rect x="84" y="-8" width="10" height="10" rx="4" fill="#FFF6E6"/><rect x="-90" y="-6" width="8" height="10" rx="3" fill="#E0563F"/>'
            '<g fill="#2B2320"><circle cx="-52" cy="24" r="17"/><circle cx="54" cy="24" r="17"/></g>'
            '<g fill="#DADDE8"><circle cx="-52" cy="24" r="7"/><circle cx="54" cy="24" r="7"/></g></g>')


def svg(n, title, desc, stops, body):
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           f'<polygon id="s" points="0,-10 2.4,-3.2 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.4,-3.2" fill="{GOLD}"/>'
           + (hornet_def() if any('#h"' in b for b in body) else "") +
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n'
           + "\n".join(body) + '\n</g>\n</svg>\n')
    with open(f"{OUT}/anansi-{n:02d}.svg", "w") as fh:
        fh.write(doc)


GRIP_UP = {"L1": "M-14 -2 Q-42 -40 -3 -70", "R1": "M14 -2 Q42 -40 3 -70"}
FOREST_BACK = [hill(330, 50, "#8CC49A"), hill(400, 40, "#4E9A6B")]

# 01 cover
hug = box(0, 24, .72, g=False) + stroke("M-21 8 Q-40 16 -22 28 M21 8 Q40 16 22 28 M-18 22 Q-36 36 -18 42 M18 22 Q36 36 18 42")
svg(1, "Anansi and the Box of Stories", "Paper-cut cover: Anansi, a small brown spider in a striped red scarf, hangs on a silver thread under a starry night sky, hugging a glowing golden box.", NIGHT, [
    stars(1, 46, 430), hill(520, 40, "#232B66"),
    blobs([(60, 590, 70), (180, 610, 80), (320, 600, 70), (470, 612, 84), (620, 598, 72), (750, 606, 80)], "#141A40"),
    stroke("M400 0 V190", SILVER, 3.5), star(400, 96, 1.1), glow(400, 330, 170),
    anansi(400, 270, 2.3, look=(0, 1.5), legs={**GRIP_UP, "L2": "", "L3": "", "R2": "", "R3": ""}, extra=hug),
    star(250, 300, .6), star(560, 250, .7), star(520, 420, .5), star(290, 440, .5)])

# 02 no stories on earth
dark_huts = [hut(a, b, s) for a, b, s in [(300, 470, 1.2), (390, 480, 1), (480, 462, 1.3), (590, 478, 1.1), (680, 470, 1.2), (230, 500, .9)]]
svg(2, "Long ago the earth had no stories", "Paper-cut night scene: a quiet, dark village sleeps below while high in the clouds a golden box glows beside Nyame the Sky God, shown as a warm sun resting in cloud; little Anansi looks up from a hill.", NIGHT, [
    stars(2, 30, 330), nyame(600, 120, 74, "calm"), cloud(600, 262, 1.5, "#8E90CC"), cloud(455, 150, 1, "#7C7FC4"), cloud(745, 235, 1.1, "#7C7FC4"),
    cloud(350, 205, 1.2, "#8E90CC"), box(350, 150, 1), cloud(160, 110, .9, "#5E61A8"),
    hill(430, 30, "#232B66"), *dark_huts, blobs([(740, 470, 34), (60, 470, 30)], "#141A40"),
    hill(520, 24, "#1A2556"), anansi(140, 380, .8, look=(2, -2))])

# 03 the big idea
svg(3, "Anansi has a big idea", "Paper-cut forest scene: tiny Anansi sits on a big green leaf and stares up at a far-off golden glow in the sky, with a little golden sparkle above his head for his big idea.", [(0, "#1F5A4A"), (1, "#4E9A6B")], [
    glow(650, 90, 120), f'<circle cx="650" cy="90" r="9" fill="#FBE48A"/>',
    blobs([(80, 40, 130), (260, 10, 120), (440, 0, 90), (790, 150, 90)], "#17463A"), blobs([(160, 90, 70), (350, 50, 60), (760, 60, 50)], "#2F7D4F", False),
    '<g fill="#3B2A22" filter="url(#p)"><rect x="60" y="0" width="54" height="600"/><rect x="700" y="120" width="64" height="480"/></g>',
    hill(540, 20, "#17463A"),
    '<g filter="url(#p)"><path d="M90 480 Q300 350 600 425 Q390 540 90 480Z" fill="#58AB6E"/></g>' + stroke("M40 500 Q300 440 590 428", "#3F9460", 6),
    anansi(330, 372, 1.5, look=(2.5, -2.5)), star(430, 280, 1.6), star(470, 240, .8), star(400, 235, .6),
    '<g fill="#17463A" filter="url(#p)"><path d="M0 600 Q20 480 110 450 Q90 540 70 600Z"/><path d="M800 600 Q780 500 700 470 Q715 545 740 600Z"/><path d="M560 600 Q600 520 690 520 Q650 570 640 600Z"/></g>'])

# 04 climbing the thread
svg(4, "Anansi climbs to the sky", "Paper-cut scene: a silver thread stretches from the treetops up into the clouds, and Anansi climbs it, high above the forest.", CLIMB, [
    glow(455, 20, 150), cloud(330, 40, 1.8), cloud(600, 50, 1.9), cloud(120, 200, .9, "#FFF6E6"), cloud(690, 300, 1, "#FFF6E6"),
    stroke("M370 600 L455 0", SILVER, 3.5), star(440, 110, 1.1),
    stroke("M250 330 q10 -10 20 0 q10 -10 20 0 M560 190 q8 -8 16 0 q8 -8 16 0", "#5B6A7A", 3),
    anansi(413, 295, 1.5, rot=8, look=(0, -2.5), legs={**GRIP_UP, "L4": "M-13 24 Q-30 42 -3 58", "R4": "M13 24 Q30 42 3 58"}),
    marks(["M330 330 q-10 12 -4 26", "M500 250 q10 12 4 26"]),
    blobs([(40, 600, 90), (200, 620, 100), (380, 610, 90), (560, 625, 100), (740, 605, 90)], "#2F7D4F"),
    blobs([(120, 600, 50), (300, 612, 46), (470, 606, 52), (660, 610, 50)], "#58AB6E", False)])

# 05 Nyame laughs
svg(5, "Nyame the Sky God laughs", "Paper-cut scene in the clouds: Nyame, a huge warm sun with kind laughing eyes, looks down at tiny Anansi standing on a cloud while the clouds billow around them.", REALM, [
    nyame(400, 200, 158, "laugh"), cloud(110, 330, 1.7), cloud(700, 320, 1.7), cloud(400, 430, 2.2, "#F3DCC2"),
    marks(["M40 230 q-14 20 -4 44", "M770 220 q14 20 4 44", "M210 250 q-10 12 -4 28", "M600 250 q10 12 4 28"]),
    cloud(170, 520, 1.7), box(170, 430, .9), cloud(560, 520, 1.9), anansi(560, 385, .95, look=(-1.5, -2.5)), cloud(380, 600, 2.4, "#F3DCC2")])

# 06 Python
ticks = " ".join(f"M{a} {b} v-12" for a, b in [(190, 292), (245, 288), (430, 290), (485, 292), (540, 288), (595, 280)])
svg(6, "Anansi measures Python", "Paper-cut forest scene: a long green python lies stretched proudly along a palm branch while Anansi stands on his back and measures him with his legs.", FOREST, [
    *FOREST_BACK,
    '<g filter="url(#p)"><path d="M70 600 Q60 300 110 0 H160 Q120 300 140 600Z" fill="#7A5236"/><path d="M110 350 Q400 318 800 338 V372 Q400 352 120 392Z" fill="#7A5236"/></g>',
    '<g fill="#2F7D4F" filter="url(#p)"><path d="M130 60 Q260 -20 400 50 Q260 60 130 60Z"/><path d="M130 80 Q270 90 360 190 Q230 150 130 80Z"/><path d="M110 60 Q20 80 -20 180 Q70 150 110 60Z"/></g>',
    snake("M150 324 Q300 294 420 312 T640 294", 668, 278, -18, 38), stroke(ticks, CREAM, 3),
    anansi(335, 238, 1.15, look=(2, 2), legs={"L2": "M-19 6 Q-52 0 -62 26", "R2": "M19 6 Q52 0 62 26"}),
    '<g fill="#3F9460" filter="url(#p)"><path d="M0 600 Q30 500 130 480 Q100 550 80 600Z"/><path d="M800 600 Q770 510 680 490 Q700 550 720 600Z"/></g>'])

# 07 Hornets
drops = "".join(f'<path d="M{a} {b} q7 12 0 17 q-7 -5 0 -17z" fill="#6FB7E8"/>' for a, b in [(420, 220), (440, 265), (405, 290), (455, 320), (425, 350), (470, 250)])
bees = [(340, 345, 20), (395, 300, 30), (450, 375, 25), (505, 335, 35), (385, 405, 15), (545, 395, 40)]
trails = " ".join(f"M{a - 34} {b - 14} q12 -4 20 6" for a, b, _ in bees)
svg(7, "Anansi and the Hornets", "Paper-cut forest scene: Anansi tips water from a big leaf like rain, and a little cloud of friendly round hornets zooms into an open gourd to keep dry.", FOREST, [
    *FOREST_BACK, hill(500, 20, "#3F7D4A"),
    '<g filter="url(#p)"><path d="M0 236 Q160 246 340 226 L340 246 Q160 270 0 264Z" fill="#7A5236"/></g>',
    blobs([(40, 150, 90), (150, 90, 70)], "#2F7D4F"),
    '<g filter="url(#p)" transform="translate(300 172) rotate(24)"><path d="M0 0 Q50 -36 120 -6 Q60 30 0 0Z" fill="#58AB6E"/></g>' + stroke("M300 172 L408 218", "#3F9460", 4),
    anansi(225, 178, 1.15, look=(2.5, 1.5), legs={"R1": "M14 -2 Q44 -20 62 -6", "R2": "M19 6 Q50 4 64 0"}), drops,
    gourd(630, 450, 1.6, -38), hornet(596, 418, 1.2, 40),
    marks([trails], "#fff", 3), *[hornet(a, b, 1.5, r) for a, b, r in bees]])

# 08 Leopard
svg(8, "Anansi counts Leopard's spots", "Paper-cut scene: Leopard stands proudly with his chin up, showing off his spots, while Anansi points one leg and counts them from a rock.", FOREST, [
    *FOREST_BACK, blobs([(700, 200, 90), (790, 260, 70), (30, 230, 80)], "#2F7D4F"),
    '<g fill="#7A5236" filter="url(#p)"><rect x="690" y="240" width="34" height="260"/></g>', hill(500, 20, "#5E8E48"),
    leopard(500, 400, 1.6), '<ellipse cx="190" cy="490" rx="110" ry="58" fill="#8E8478" filter="url(#p)"/><ellipse cx="160" cy="470" rx="50" ry="20" fill="#A49A8E"/>',
    f'<path d="M285 345 L400 372" stroke="{CREAM}" stroke-width="3.5" stroke-dasharray="3 10" stroke-linecap="round"/>',
    anansi(195, 372, 1.3, look=(2.5, 0), legs={"R1": "M14 -2 Q40 -30 62 -22"}, mouth="open"),
    '<g fill="#3F9460" filter="url(#p)"><path d="M800 600 Q770 510 680 500 Q700 560 720 600Z"/><path d="M330 600 Q350 540 420 536 Q395 575 390 600Z"/></g>'])

# 09 everyone climbs
coil = "".join(f'<ellipse cx="{384 + i * 3}" cy="{418 - i * 22}" rx="30" ry="13" stroke="{PY}" stroke-width="17" fill="none"/>' for i in range(3))
svg(9, "Everyone climbs to the sky", "Paper-cut scene: the silver thread wobbles as everyone climbs to the sky — Leopard holding on at the bottom, Python coiled around the middle, and Anansi at the top carrying the gourd of hornets.", CLIMB, [
    cloud(150, 120, 1.3), cloud(660, 60, 1.6), cloud(690, 380, 1), cloud(110, 380, .9),
    blobs([(60, 620, 80), (220, 640, 90), (600, 640, 90), (760, 620, 80)], "#2F7D4F"),
    stroke("M260 600 Q360 500 380 400 Q400 300 470 220 Q540 140 560 0", SILVER, 3.5),
    marks(["M300 470 q-16 -4 -24 8", "M440 430 q16 -2 22 10", "M400 250 q-14 -6 -24 4", "M545 200 q14 2 18 14", "M500 90 q-14 -4 -22 6"]),
    leopard(318, 508, .8, -52, "open"),
    f'<g filter="url(#p)">{coil}</g>' + snake("M392 372 Q400 350 420 344", 432, 336, -30, 17, "open"),
    gourd(436, 196, .75, -28), hornet(410, 150, 1.1, -30), hornet(388, 190, 1, 190),
    anansi(480, 212, 1.1, rot=18, look=(0, -2.5), legs={**GRIP_UP, "L2": "M-19 6 Q-40 2 -44 -8"}), star(528, 120, .9)])

# 10 Nyame is amazed
svg(10, "Nyame is amazed", "Paper-cut scene in the clouds: Nyame the warm sun looks down wide-eyed as Anansi proudly presents Python stretched out long, the hornets flying happily out of the gourd, and Leopard sitting beside them.", REALM, [
    nyame(400, 160, 128, "amazed"), cloud(120, 250, 1.5), cloud(690, 240, 1.5),
    f'<rect y="450" width="800" height="150" fill="#FFF6E6"/>', cloud(130, 460, 2), cloud(420, 470, 2.2), cloud(700, 460, 2),
    leopard(165, 405, .8), gourd(690, 470, 1.1, 24),
    *[hornet(a, b, 1.3, r) for a, b, r in [(650, 385, -60), (715, 340, -40), (745, 410, -20), (665, 300, -70), (600, 335, -110)]],
    marks(["M690 420 q-10 -14 -4 -28", "M728 372 q-4 -14 6 -24"], "#B98A5E", 3),
    anansi(420, 400, 1.15, look=(0, -2.5), legs={"L1": "M-14 -2 Q-40 -26 -52 -46", "R1": "M14 -2 Q40 -26 52 -46"}, mouth="open"),
    snake("M70 540 Q200 512 330 530 T560 520", 590, 504, -16), cloud(700, 620, 2, "#F3DCC2"), cloud(60, 630, 1.8, "#F3DCC2")])

# 11 the gift
svg(11, "Nyame gives Anansi the box", "Paper-cut scene in the clouds: Nyame's big soft cloud hand reaches down and gives the glowing golden box of stories to little Anansi, who reaches up for it.", REALM, [
    nyame(215, 170, 140, "kind"), cloud(90, 330, 1.6), glow(480, 320, 150),
    f'<g transform="translate(480 392)">{hand(0, 0, 1.15)}</g>', box(480, 318, 1.5, g=False),
    star(400, 250, .8), star(570, 240, 1), star(600, 330, .6),
    cloud(660, 560, 2.1), anansi(650, 418, 1.3, look=(-2.5, -2), legs={"L1": "M-14 -2 Q-44 -30 -62 -42", "L2": "M-19 6 Q-52 -8 -66 -18"}, mouth="open"),
    cloud(260, 600, 2.4, "#F3DCC2")])

# 12 whoosh
flies = [(262, 420, 1.6), (290, 380, 1.3), (268, 345, 1), (318, 330, 1.5), (350, 290, 1.1), (392, 262, 1.6), (430, 232, 1), (470, 250, 1.3),
         (512, 214, 1.5), (556, 232, 1), (600, 200, 1.4), (640, 236, 1.1), (690, 210, 1.5), (742, 250, 1.1), (430, 310, 1), (520, 300, 1.2),
         (600, 310, 1), (690, 300, 1.2), (340, 240, .9), (760, 180, 1), (470, 180, .9), (570, 150, 1.1), (660, 140, .9)]
lit = [(330, 400, .9), (430, 388, 1), (520, 400, .9), (610, 384, 1.1), (710, 396, 1), (480, 470, 1.2), (590, 480, 1.1), (700, 476, 1.3), (380, 482, 1.1)]
svg(12, "The stories fly out", "Paper-cut dusk scene: Anansi opens the golden box and, with a whoosh, golden fireflies stream out across the hills to many little houses, whose windows light up one by one.", [(0, "#2A2F70"), (1, "#9A5E96")], [
    stars(12, 24, 200), hill(410, 36, "#3A3E88"), *[hut(a, b, s, True) for a, b, s in lit[:5]],
    hill(490, 28, "#2B3476"), *[hut(a, b, s, True) for a, b, s in lit[5:]], hill(560, 30, "#1A2556"),
    marks(["M300 440 q30 -40 20 -90", "M320 470 q60 -50 70 -130", "M215 410 q-10 -40 20 -80"], CREAM, 4),
    glow(245, 440, 110), *[firefly(a, b, s) for a, b, s in flies],
    box(240, 500, 1.7, opened=True, g=False), anansi(110, 455, 1.35, look=(2.5, -2), legs={"R1": "M14 -2 Q44 -24 60 -40"}, mouth="open")])

# 13 one flew to you
trail = [(330, 30, .7), (362, 78, .8), (380, 130, .9), (384, 185, 1), (376, 240, 1.1), (374, 292, 1.2), (384, 342, 1.4), (398, 388, 1.6)]
svg(13, "And one flew all the way to you", "Paper-cut morning scene: a small blue car drives along a sunny road while one golden firefly streams in through its window, and Anansi waves from his thread in a roadside tree.", [(0, "#9FD3D6"), (1, "#FBEBD0")], [
    '<circle cx="650" cy="110" r="52" fill="#FFF6E6"/>', cloud(520, 80, .9),
    hill(370, 44, "#8FC2A0"), hill(430, 30, "#5FA06C"),
    '<path filter="url(#p)" d="M0 462 Q400 424 800 474 V566 Q400 506 0 552Z" fill="#6E6A78"/>',
    f'<path d="M0 506 Q400 466 800 520" stroke="{CREAM}" stroke-width="5" stroke-dasharray="30 26" fill="none"/>',
    '<g filter="url(#p)"><path d="M40 470 Q50 300 70 180 h36 Q90 300 96 470Z" fill="#7A5236"/><path d="M80 230 Q150 200 230 210 v18 Q150 222 90 258Z" fill="#7A5236"/></g>',
    blobs([(60, 120, 100), (180, 90, 80), (-10, 220, 70)], "#2F7D4F"), blobs([(110, 80, 50), (210, 120, 40)], "#58AB6E", False),
    stroke("M200 222 V290", SILVER, 3), anansi(200, 338, 1, look=(2.5, 1.5), legs={**GRIP_UP, "R2": "M19 6 Q48 -14 60 -30"}, mouth="open"),
    car(430, 450, 1.3), glow(404, 400, 46),
    f'<path d="M330 30 Q410 130 376 240 T400 398" stroke="{GOLD}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round" fill="none" opacity=".8"/>',
    *[firefly(a, b, s) for a, b, s in trail],
    '<path d="M0 600 V560 Q400 520 800 580 V600Z" fill="#3F7D5A"/>'])
