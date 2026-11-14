#!/usr/bin/env python3
"""Generates the 13 Tiddalik-the-Thirsty-Frog flip-book SVGs from shared character parts.

Usage: python3 tiddalik_gen.py <output-dir>
Every character's origin is the point where it touches the ground (or its perch),
so placing a character at a ground y keeps it standing on the ground.
The land runs green -> turning -> dry -> green; Tiddalik swells (full 0 -> 1) and shrinks back.
"""
import sys

OUT = sys.argv[1]
INK, CREAM = "#2B2320", "#FFF6E6"
FROG, FROG_DK, FROG_LT, BELLY, BELLY_WET = "#6CBF4F", "#4E9A3A", "#9BD77A", "#EAF0B4", "#BFE3EE"
BLUE, BLUE_LT, BLUE_DK = "#4FAEE0", "#8AD0F0", "#2F86C0"
MUD, MUD_LT = "#8A5E3C", "#A47148"
GOLD = "#F6C445"
CHEEK = "#F2A9B0"
DAY = [(0, "#86CDEB"), (1, "#FCEBC6")]
DAWN = [(0, "#F4A68C"), (1, "#FDE6B8")]
HOT = [(0, "#F2B66B"), (1, "#FBE3B0")]
WARM = [(0, "#9AD3E8"), (1, "#FFE6B0")]
# far range, mid hill, near ground, front strip, tuft
LAND = {
    "green": ("#A3C9B4", "#93C46A", "#7DB457", "#5E9E45", "#5E9E45"),
    "turning": ("#C9BC8E", "#CDBA62", "#C9A653", "#A88A3E", "#B39548"),
    "dry": ("#D9A58A", "#D9874E", "#C8693C", "#A9502C", "#C9A55A"),
}
CANOPY = {"green": ("#6E9A6A", "#8DB57E"), "turning": ("#9C9A5E", "#B7B070"), "dry": ("#9A8452", "#B39C62")}


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, rot: float, inner: str, shadow: bool = True) -> str:
    r = f" rotate({rot})" if rot else ""
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}){r} scale({-s if flip else s} {s})"{f}>{inner}</g>'


def eye(cx: float, cy: float, r: float, look: tuple = (1, 0), lid: float = 0, bump: str = FROG) -> str:
    """A googly eye on a bump. lid 0..1 covers the top of the eye (sleepy / stuffed)."""
    lx, ly = look
    out = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 5:.1f}" fill="{bump}"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#fff"/>'
           f'<circle cx="{cx + lx * r * .3:.1f}" cy="{cy + ly * r * .3:.1f}" r="{r * .45:.1f}" fill="{INK}"/>'
           f'<circle cx="{cx + lx * r * .3 + r * .15:.1f}" cy="{cy + ly * r * .3 - r * .15:.1f}" r="{r * .14:.1f}" fill="#fff"/>')
    if lid:
        ly = cy - r * (1 - 2 * lid) * .6
        w = (max(r * r - (ly - cy) ** 2, 0)) ** .5
        big = 1 if ly > cy else 0
        out += f'<path d="M{cx - w:.1f} {ly:.1f} A{r + .5:.1f} {r + .5:.1f} 0 {big} 1 {cx + w:.1f} {ly:.1f}Z" fill="{bump}"/>'
        out += stroke(f"M{cx - w:.1f} {ly:.1f} H{cx + w:.1f}", INK, 2.8)
    return out


def shut(cx: float, cy: float, r: float, up: bool = True, bump: str = FROG) -> str:
    """A closed eye: a happy arch (up) or a sleepy smile line."""
    d = f"M{cx - r * .7:.1f} {cy + 2:.1f} q{r * .7:.1f} {-r * .9 if up else r * .7:.1f} {r * 1.4:.1f} 0"
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 5:.1f}" fill="{bump}"/>' + stroke(d, INK, 3.2)


def frog_face(mood: str, ex: float, ey: float, er: float, my: float, mw: float) -> str:
    """Tiddalik's face. mouth centre at (0, my), half-width mw."""
    l, r = -ex, ex
    eyes = {
        "happy": eye(l, ey, er) + eye(r, ey, er),
        "thirsty": eye(l, ey, er, (0, -1)) + eye(r, ey, er, (0, -1)),
        "full": eye(l, ey, er, (0, .5), .55) + eye(r, ey, er, (0, .5), .55),
        "blink": eye(l, ey, er, (-1, 0), .55) + eye(r, ey, er, (-1, 0), .55),
        "twitch": eye(l, ey, er, (-1, .3)) + eye(r, ey, er, (-1, .3)),
        "wobble": eye(l, ey, er, (-1, 0)) + eye(r, ey, er, (-1, 0)),
    }
    if mood in ("sleepy", "gulp", "yawn", "laugh", "joy"):
        e = shut(l, ey, er, mood in ("laugh", "joy")) + shut(r, ey, er, mood in ("laugh", "joy"))
    else:
        e = eyes[mood]
    smile = stroke(f"M{-mw:.1f} {my - 4:.1f} Q0 {my + mw * .45:.1f} {mw:.1f} {my - 4:.1f}", INK, 3.6)
    mouths = {
        "happy": smile, "joy": smile, "sleepy": stroke(f"M{-mw * .5:.1f} {my:.1f} Q0 {my + 10:.1f} {mw * .5:.1f} {my:.1f}", INK, 3.4),
        "thirsty": (f'<path d="M{-mw * .55:.1f} {my - 4:.1f} Q0 {my + mw * .5:.1f} {mw * .55:.1f} {my - 4:.1f}Z" fill="#7A2E2A"/>'
                    f'<path d="M{-mw * .18:.1f} {my + 2:.1f} q{mw * .18:.1f} {mw * .7:.1f} {mw * .36:.1f} 0Z" fill="#F07C8A"/>'),
        "gulp": f'<ellipse cx="0" cy="{my:.1f}" rx="{mw * .22:.1f}" ry="{mw * .18:.1f}" fill="#7A2E2A"/>',
        "full": stroke(f"M{-mw * .8:.1f} {my:.1f} Q0 {my + 6:.1f} {mw * .8:.1f} {my:.1f}", INK, 3.6),
        "blink": stroke(f"M{-mw * .8:.1f} {my + 2:.1f} H{mw * .8:.1f}", INK, 3.6),
        "yawn": f'<ellipse cx="0" cy="{my + 4:.1f}" rx="{mw * .38:.1f}" ry="{mw * .3:.1f}" fill="#7A2E2A"/>',
        "twitch": stroke(f"M{-mw * .8:.1f} {my:.1f} q{mw * .2:.1f} -6 {mw * .4:.1f} 0 t{mw * .4:.1f} 0 t{mw * .4:.1f} 0 t{mw * .4:.1f} -8", INK, 3.6),
        "wobble": stroke(f"M{-mw * .8:.1f} {my:.1f} q{mw * .2:.1f} -8 {mw * .4:.1f} 0 t{mw * .4:.1f} 0 t{mw * .4:.1f} 0 t{mw * .4:.1f} 0", INK, 3.6),
        "laugh": (f'<path d="M{-mw * .8:.1f} {my - 6:.1f} Q0 {my + mw * .95:.1f} {mw * .8:.1f} {my - 6:.1f}Z" fill="#7A2E2A"/>'
                  f'<ellipse cx="0" cy="{my + mw * .42:.1f}" rx="{mw * .34:.1f}" ry="{mw * .14:.1f}" fill="#F07C8A"/>'),
    }
    cheeks = "".join(f'<circle cx="{sx * mw * 1.08:.1f}" cy="{my + 6:.1f}" r="{mw * .17:.1f}" fill="{CHEEK}" opacity=".65"/>' for sx in (-1, 1))
    return e + mouths[mood] + cheeks


def frog(x: float, y: float, s: float = 1, full: float = 0, mood: str = "happy", flip: bool = False, rot: float = 0) -> str:
    """Tiddalik: the same green frog on every page. full 0 = normal frog, 1 = swollen with all the water."""
    rx, ry = 60 + 34 * full, 52 + 22 * full
    cy = -ry + 2
    hx = rx * .74
    hr = (30 + 8 * full, 24 + 8 * full)
    haunch = "".join(f'<ellipse cx="{sx * hx:.1f}" cy="{-hr[1] + 2:.1f}" rx="{hr[0]:.1f}" ry="{hr[1]:.1f}" fill="{FROG_DK}"/>' for sx in (-1, 1))
    toes = "".join(f'<ellipse cx="{sx * (hx + hr[0] * .55 + i * 9):.1f}" cy="-3" rx="7" ry="4.5" fill="{FROG_DK}"/>' for sx in (-1, 1) for i in range(3))
    body = f'<ellipse cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{FROG}"/>'
    spots = "".join(f'<circle cx="{sx * rx * a:.1f}" cy="{cy + ry * b:.1f}" r="{rr * (1 + full * .5):.1f}" fill="{FROG_DK}" opacity=".55"/>'
                    for sx in (-1, 1) for a, b, rr in [(.78, -.15, 6), (.66, .3, 4.5), (.86, .22, 3.5)])
    bfill = BELLY_WET if full > .3 else BELLY
    belly = f'<ellipse cy="{cy + ry * .28:.1f}" rx="{rx * .66:.1f}" ry="{ry * .62:.1f}" fill="{bfill}"/>'
    if full > .3:
        bw = rx * .5
        for k in range(3 if full > .6 else 2):
            wy = cy + ry * (.12 + .2 * k)
            belly += stroke(f"M{-bw:.1f} {wy:.1f} q{bw / 4:.1f} -7 {bw / 2:.1f} 0 t{bw / 2:.1f} 0 t{bw / 2:.1f} 0 t{bw / 2:.1f} 0", BLUE, 3.4)
        belly += stroke(f"M{-rx * .86:.1f} {cy + ry * .05:.1f} q{rx * .02:.1f} {-ry * .32:.1f} {rx * .2:.1f} {-ry * .5:.1f}", "#E4F6FB", 3 + 2 * full)
    arms = "".join(stroke(f"M{sx * rx * .42:.1f} {cy + ry * .55:.1f} q{sx * 4:.1f} 14 {sx * 2:.1f} {-cy - ry * .55 - 6:.1f}", FROG_DK, 9)
                   + "".join(f'<ellipse cx="{sx * (rx * .44 + j * 8 - 8):.1f}" cy="-3" rx="6.5" ry="4.2" fill="{FROG_DK}"/>' for j in range(3))
                   for sx in (-1, 1))
    er = 15 + 3 * full
    face = frog_face(mood, rx * .45, cy - ry * .8, er, cy - ry * .36, rx * .48)
    return group(x, y, s, flip, rot, haunch + toes + body + spots + belly + arms + face)


def kookaburra(x: float, y: float, s: float = 1, flip: bool = False, mood: str = "calm") -> str:
    """Kookaburra, perched: origin is where her feet grip the branch."""
    laugh = mood == "laugh"
    tail = ('<path d="M-20 -26 L-60 -2 L-50 8 L-14 -14Z" fill="#B5652F"/>' + stroke("M-30 -16 l5 7 M-40 -10 l5 7 M-50 -4 l4 6", "#6E3A1C", 2.6))
    body = (f'<ellipse cx="0" cy="-36" rx="27" ry="31" fill="#F4ECDC"/><path d="M-24 -52 Q4 -64 14 -36 Q4 -10 -22 -16Z" fill="#7A5434"/>'
            '<ellipse cx="-4" cy="-40" rx="9" ry="5" fill="#4F9BD0"/>')
    feet = stroke("M-6 -8 V0 M8 -8 V0", "#6B6460", 4)
    beak = ('<path d="M30 -84 L66 -94 L34 -72Z" fill="#3C3530"/><path d="M33 -70 L62 -58 L30 -64Z" fill="#D8C9A6"/><path d="M34 -72 L50 -70 L33 -68Z" fill="#7A2E2A"/>'
            if laugh else '<path d="M30 -82 L66 -72 L32 -70Z" fill="#3C3530"/><path d="M32 -70 L64 -71 L30 -64Z" fill="#D8C9A6"/>')
    head = (f'<g transform="rotate({-18 if laugh else 0} 8 -58)"><circle cx="12" cy="-74" r="22" fill="#F4ECDC"/>'
            '<path d="M-8 -82 Q8 -102 30 -88 Q14 -86 -6 -74Z" fill="#6E4A2E"/><path d="M-6 -72 Q14 -82 32 -76 L30 -70 Q14 -74 -6 -66Z" fill="#7A5434"/>'
            + (stroke("M12 -78 q5 -6 10 0", INK, 2.8) if laugh else
               f'<circle cx="17" cy="-76" r="5" fill="{INK}"/><circle cx="18.5" cy="-77.5" r="1.6" fill="#fff"/>')
            + beak + '</g>')
    return group(x, y, s, flip, 0, tail + feet + body + head)


def kangaroo(x: float, y: float, s: float = 1, flip: bool = False, mood: str = "calm") -> str:
    """Kangaroo standing on its big feet: origin under the feet."""
    c, lt, dk = "#C8743A", "#ECBE8A", "#9C5226"
    tail = f'<path d="M-24 -40 Q-70 -24 -100 -2 Q-96 4 -84 2 Q-56 -8 -14 -22Z" fill="{dk}"/>'
    legs = (f'<ellipse cx="-6" cy="-42" rx="30" ry="28" fill="{c}"/><path d="M-20 -18 Q-4 -6 48 -4 Q52 2 44 2 H-26 Q-30 -10 -20 -18Z" fill="{dk}"/>')
    body = (f'<ellipse cx="6" cy="-88" rx="25" ry="46" fill="{c}" transform="rotate(16 6 -88)"/>'
            f'<ellipse cx="16" cy="-82" rx="13" ry="30" fill="{lt}" transform="rotate(16 16 -82)"/>')
    arms = stroke("M24 -108 q16 6 18 20 M18 -102 q14 10 12 24", dk, 7)
    eye_ = (stroke("M19 -146 q5 -5 10 0", INK, 2.8) if mood == "joy" else
            f'<circle cx="24" cy="-146" r="4" fill="{INK}"/><circle cx="25.2" cy="-147.2" r="1.3" fill="#fff"/>')
    head = (f'<ellipse cx="10" cy="-172" rx="6" ry="17" fill="{dk}" transform="rotate(-16 10 -172)"/>'
            f'<ellipse cx="22" cy="-174" rx="6" ry="17" fill="{c}" transform="rotate(8 22 -174)"/>'
            f'<ellipse cx="20" cy="-144" rx="18" ry="16" fill="{c}"/><ellipse cx="40" cy="-138" rx="15" ry="10" fill="{c}"/>'
            f'<ellipse cx="53" cy="-140" rx="4.5" ry="3.5" fill="{INK}"/>{eye_}<circle cx="34" cy="-132" r="4" fill="{CHEEK}" opacity=".6"/>')
    return group(x, y, s, flip, 0, tail + legs + body + arms + head)


def wombat(x: float, y: float, s: float = 1, flip: bool = False, roll: bool = False) -> str:
    """Wombat: a round brown barrel on short legs. roll=True puts him on his back, legs in the air."""
    c, dk = "#8A6A52", "#6B4F3C"
    legs = "".join(f'<rect x="{a}" y="-16" width="16" height="18" rx="7" fill="{dk}"/>' for a in (-44, -22, 14, 34))
    body = f'<ellipse cx="0" cy="-40" rx="58" ry="36" fill="{c}"/><ellipse cx="-6" cy="-26" rx="34" ry="14" fill="#A08068"/>'
    head = (f'<circle cx="50" cy="-48" r="26" fill="{c}"/><circle cx="34" cy="-72" r="8" fill="{dk}"/><circle cx="54" cy="-74" r="8" fill="{dk}"/>'
            f'<ellipse cx="70" cy="-44" rx="10" ry="8" fill="#3A2C24"/>'
            + (stroke("M46 -56 q5 -5 10 0", INK, 2.8) if roll else f'<circle cx="52" cy="-54" r="4" fill="{INK}"/><circle cx="53.2" cy="-55.2" r="1.3" fill="#fff"/>')
            + stroke("M58 -34 q6 4 12 0", INK, 2.6) + f'<circle cx="42" cy="-38" r="4.5" fill="{CHEEK}" opacity=".6"/>')
    inner = legs + body + head
    if roll:
        inner = f'<g transform="rotate(180 0 -39)">{inner}</g>'
    return group(x, y, s, flip, 0, inner)


def emu(x: float, y: float, s: float = 1, flip: bool = False, dance: bool = False) -> str:
    """Emu: tall, shaggy, long blue-grey neck. dance=True lifts one leg."""
    lc = "#6E7A8A"
    back_leg = "M-8 -96 L-12 0 M-22 0 H-2"
    front_leg = "M10 -96 L40 -62 L22 -44 M22 -44 l10 4" if dance else "M10 -96 L14 0 M4 0 H26"
    legs = stroke(back_leg + " " + front_leg, lc, 7)
    body = ('<ellipse cx="-4" cy="-122" rx="54" ry="40" fill="#6B5A4A"/>'
            + stroke("M-44 -112 q8 10 16 0 q8 10 16 0 q8 10 16 0 q8 10 16 0 M-36 -136 q8 10 16 0 q8 10 16 0 q8 10 16 0", "#8C7964", 3.4)
            + '<path d="M-52 -116 Q-74 -100 -60 -84 Q-54 -100 -42 -104Z" fill="#5A4A3C"/>')
    neck = stroke("M28 -140 Q44 -176 40 -212", "#7FA0B8", 15)
    head = ('<ellipse cx="46" cy="-218" rx="16" ry="13" fill="#5D6B78"/><path d="M58 -224 L76 -216 L58 -210Z" fill="#3E3A36"/>'
            '<circle cx="50" cy="-222" r="4.6" fill="#C8642E"/><circle cx="51" cy="-222" r="2.2" fill="#2B2320"/>'
            f'<circle cx="46" cy="-210" r="3.6" fill="{CHEEK}" opacity=".6"/>')
    return group(x, y, s, flip, 0, legs + body + neck + head)


def koala(x: float, y: float, s: float = 1, flip: bool = False, silly: bool = False) -> str:
    """Koala sitting on the ground: big round ears, big black nose. silly=True: tongue out, crossed eyes."""
    c, lt = "#9AA0A6", "#E9E4DC"
    body = (f'<ellipse cx="0" cy="-40" rx="34" ry="40" fill="{c}"/><ellipse cx="0" cy="-34" rx="20" ry="26" fill="{lt}"/>'
            f'<ellipse cx="-20" cy="-6" rx="14" ry="8" fill="#7E848A"/><ellipse cx="20" cy="-6" rx="14" ry="8" fill="#7E848A"/>')
    arms = (stroke("M-28 -60 q-24 -18 -30 -44 M28 -60 q24 -18 30 -44", "#7E848A", 12) if silly else
            stroke("M-28 -60 q-6 20 6 30 M28 -60 q6 20 -6 30", "#7E848A", 12))
    ears = "".join(f'<circle cx="{a}" cy="-122" r="19" fill="{c}"/><circle cx="{a}" cy="-120" r="11" fill="{lt}"/>' for a in (-32, 32))
    head = f'<circle cx="0" cy="-98" r="33" fill="{c}"/>'
    if silly:
        eyes = ('<circle cx="-13" cy="-106" r="7" fill="#fff"/><circle cx="13" cy="-106" r="7" fill="#fff"/>'
                f'<circle cx="-9.5" cy="-105" r="3.4" fill="{INK}"/><circle cx="9.5" cy="-105" r="3.4" fill="{INK}"/>')
        mouth = '<path d="M-7 -78 q7 18 14 0Z" fill="#F07C8A"/>'
    else:
        eyes = f'<circle cx="-13" cy="-106" r="3.8" fill="{INK}"/><circle cx="13" cy="-106" r="3.8" fill="{INK}"/>'
        mouth = stroke("M-6 -76 q6 5 12 0", INK, 2.6)
    nose = '<ellipse cx="0" cy="-92" rx="10" ry="13" fill="#2F2A2A"/><ellipse cx="-3" cy="-97" rx="3" ry="4" fill="#5A5454"/>'
    cheeks = f'<circle cx="-22" cy="-86" r="5" fill="{CHEEK}" opacity=".6"/><circle cx="22" cy="-86" r="5" fill="{CHEEK}" opacity=".6"/>'
    return group(x, y, s, flip, 0, ears + body + arms + head + eyes + mouth + nose + cheeks)


EEL_PATHS = {
    "peek": ("M0 16 C-4 -16 14 -40 36 -50", (36, -50)),
    "knot": ("M-20 18 C-30 -30 30 -50 20 -20 C10 6 -50 -10 -40 -60 C-30 -110 40 -110 40 -80 "
             "C40 -50 0 -60 10 -100 C20 -140 70 -150 80 -126", (80, -126)),
}


def eel(x: float, y: float, s: float = 1, pose: str = "peek", flip: bool = False) -> str:
    """Eel rising out of the water: a dark grey-blue body edged with a frilly fin ribbon, and a smiling head."""
    d, (hx, hy) = EEL_PATHS[pose]
    body = (stroke(d, "#A9BCCF", 32) + f'<path d="{d}" stroke="#7F93A8" stroke-width="32" stroke-dasharray="2 7" fill="none"/>'
            + stroke(d, "#3F5268", 18))
    head = (f'<ellipse cx="{hx + 6}" cy="{hy}" rx="17" ry="13" fill="#3F5268"/>'
            f'<circle cx="{hx + 10}" cy="{hy - 4}" r="5" fill="#fff"/><circle cx="{hx + 11.5}" cy="{hy - 4}" r="2.6" fill="{INK}"/>'
            + stroke(f"M{hx + 12} {hy + 5} q6 3 10 -2", INK, 2.4) + f'<circle cx="{hx + 2}" cy="{hy + 4}" r="3.6" fill="{CHEEK}" opacity=".7"/>')
    return group(x, y, s, flip, 0, body + head)


TREE_TRUNK = ("M-14 0 Q-10 -80 -6 -140 Q-40 -176 -84 -188 L-80 -198 Q-36 -190 -2 -164 Q12 -206 40 -232 L48 -224 Q24 -198 14 -150 "
              "Q36 -134 92 -128 L92 -118 Q40 -120 14 -128 Q16 -70 18 0Z")
PERCH = (88, -123)  # where a bird sits on the long right-hand branch


def gum(x: float, y: float, s: float = 1, flip: bool = False, land: str = "green") -> str:
    """A gum tree with a pale trunk and a long right-hand branch for perching. Dry trees thin and droop."""
    dark, light = CANOPY[land]
    blobs = [(-84, -212, 38), (-36, -246, 46), (20, -262, 48), (66, -232, 38), (-4, -206, 36), (48, -196, 26)]
    if land == "dry":
        blobs = [(-84, -206, 26), (-30, -240, 32), (24, -252, 32), (64, -222, 24)]
    canopy = "".join(f'<ellipse cx="{a}" cy="{b}" rx="{r}" ry="{r * .78:.0f}" fill="{dark}"/>' for a, b, r in blobs)
    canopy += "".join(f'<ellipse cx="{a - 6}" cy="{b - 8}" rx="{r * .62:.0f}" ry="{r * .45:.0f}" fill="{light}"/>' for a, b, r in blobs)
    leaves = "".join(f'<path d="M{a} {b} q7 9 0 {20 if land == "dry" else 16} q-7 -9 0 {-20 if land == "dry" else -16}z" fill="{dark}"/>'
                     for a, b in [(60, -124), (74, -122), (-76, -190), (-62, -184)])
    trunk = (f'<path d="{TREE_TRUNK}" fill="#EDE2D2"/>'
             '<path d="M-8 -40 q8 -6 14 2 q-4 14 -12 8z M0 -96 q8 -4 10 6 q-6 8 -10 0z" fill="#C9B9A2"/>')
    return group(x, y, s, flip, 0, trunk + leaves + canopy)


def perch(x: float, y: float, s: float = 1, flip: bool = False) -> tuple:
    px, py = PERCH
    return (x + (-px if flip else px) * s, y + py * s)


def tuft(x: float, y: float, s: float, col: str) -> str:
    return (f'<path d="M{x - 16 * s} {y} L{x - 10 * s} {y - 22 * s} L{x - 4 * s} {y - 4 * s} L{x} {y - 30 * s} L{x + 5 * s} {y - 4 * s} '
            f'L{x + 12 * s} {y - 24 * s} L{x + 16 * s} {y}Z" fill="{col}"/>')


def billabong(x: float, y: float, rx: float, ry: float, level: float = 1, reeds: bool = True) -> str:
    """A waterhole. level 1 is full; lower levels show a mud rim where the water used to be; 0 is cracked mud."""
    out = f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{MUD if level < 1 else BLUE_DK}" filter="url(#p)"/>'
    if level <= 0:
        out += f'<ellipse cx="{x}" cy="{y}" rx="{rx * .9:.0f}" ry="{ry * .8:.0f}" fill="{MUD_LT}"/>'
        out += stroke(f"M{x - rx * .6:.0f} {y - 4} l{rx * .2:.0f} 8 l{rx * .16:.0f} -10 l{rx * .2:.0f} 9 M{x - rx * .1:.0f} {y + ry * .4:.0f} l{rx * .14:.0f} -10 l{rx * .2:.0f} 6 l{rx * .2:.0f} -8"
                      f" M{x - rx * .3:.0f} {y - ry * .5:.0f} l{rx * .12:.0f} 8", MUD, 3)
    else:
        wx, wy = rx * (.92 if level >= 1 else .9 * level), ry * (.8 if level >= 1 else .78 * level)
        out += f'<ellipse cx="{x}" cy="{y + (1 - min(level, 1)) * ry * .1:.0f}" rx="{wx:.0f}" ry="{wy:.0f}" fill="{BLUE}"/>'
        out += stroke(f"M{x - wx * .5:.0f} {y - wy * .25:.0f} h{wx * .3:.0f} M{x + wx * .1:.0f} {y + wy * .2:.0f} h{wx * .35:.0f}", BLUE_LT, 4)
    if reeds:
        rc = "#4E8A3A" if level > .5 else "#A08A4A"
        out += stroke(f"M{x - rx * .95:.0f} {y - 2} q-6 -30 -2 -54 M{x - rx * .88:.0f} {y + 4} q4 -28 10 -46 M{x + rx * .9:.0f} {y} q6 -26 2 -48", rc, 5)
        out += "".join(f'<ellipse cx="{a:.0f}" cy="{b:.0f}" rx="4.5" ry="10" fill="#8A5A3C"/>' for a, b in [(x - rx * .95 - 2, y - 56), (x + rx * .9 + 2, y - 50)])
    return out


def lip(x: float, y: float, rx: float, ry: float, water: str = BLUE, rim: str = MUD) -> str:
    """The near half of a pool, drawn over whatever rises out of it so it looks like it comes up from under the water."""
    return (f'<path d="M{x - rx} {y} A{rx} {ry} 0 0 0 {x + rx} {y}Z" fill="{rim}"/>'
            f'<path d="M{x - rx * .9:.0f} {y} A{rx * .9:.0f} {ry * .75:.0f} 0 0 0 {x + rx * .9:.0f} {y}Z" fill="{water}"/>'
            + stroke(f"M{x - rx * .5:.0f} {y + ry * .3:.0f} q{rx * .25:.0f} -6 {rx * .5:.0f} 0", BLUE_LT, 3))


def sip_arrows(p0: tuple, p1: tuple, p2: tuple, ts: tuple = (.45, .72)) -> str:
    """White chevrons riding along a quadratic stream, pointing towards its end (the drinker's mouth)."""
    from math import atan2, degrees
    out = ""
    for t in ts:
        bx = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0]
        by = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        out += f'<g transform="translate({bx:.0f} {by:.0f}) rotate({degrees(atan2(dy, dx)):.0f})">{stroke("M-5 -8 L5 0 L-5 8", "#fff", 4)}</g>'
    return out


def cracks(segs: list, col: str = "#9E4A28") -> str:
    return stroke(" ".join(segs), col, 3.4)


def sun(x: float, y: float, r: float, hot: bool = False) -> str:
    """A plain, faceless sun. Hot suns get a big shimmering halo."""
    halo = f'<circle cx="{x}" cy="{y}" r="{r * (2.1 if hot else 1.6):.0f}" fill="{GOLD}" opacity="{.28 if hot else .2}"/>'
    rays = "".join(f'<path d="M{x - r * .14:.1f} {y - r * 1.15:.1f} L{x} {y - r * 1.45:.1f} L{x + r * .14:.1f} {y - r * 1.15:.1f}Z" transform="rotate({30 * i} {x} {y})"/>' for i in range(12))
    return f'{halo}<g fill="#F4A720">{rays}</g><circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" filter="url(#p)"/><circle cx="{x}" cy="{y}" r="{r * .82:.0f}" fill="#FBD764"/>'


def cloud(x: float, y: float, s: float = 1, fill: str = "#fff") -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" opacity=".9">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def back(land: str = "green", ground: float = 450) -> list:
    """Far ranges, a mid hill and the near ground, all in the colours of the land's state."""
    far, mid, near, _, _ = LAND[land]
    return [f'<path d="M0 352 Q120 318 240 344 Q370 300 500 340 Q650 306 800 346 V600 H0Z" fill="{far}"/>',
            f'<path filter="url(#p)" d="M0 404 Q200 380 400 404 T800 404 V600 H0Z" fill="{mid}"/>',
            f'<path filter="url(#p)" d="M0 {ground} Q400 {ground - 30} 800 {ground + 2} V600 H0Z" fill="{near}"/>']


def front(land: str) -> str:
    return f'<path d="M0 600 V578 Q400 550 800 584 V600Z" fill="{LAND[land][3]}"/>'


def marks(ds: list, col: str = "#fff", w: float = 4) -> str:
    return f'<g opacity=".9">{stroke(" ".join(ds), col, w)}</g>'


def drops(pts: list, fill: str = BLUE) -> str:
    return f'<g fill="{fill}">' + "".join(f'<path d="M{a} {b} q7 12 0 17 q-7 -5 0 -17z"/>' for a, b in pts) + '</g>'


def heat(pts: list) -> str:
    return marks([f"M{a} {b} q8 -10 0 -20 q-8 -10 0 -20" for a, b in pts], "#FFF3D6", 3.4)


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + "\n".join(body) + '\n</g>\n</svg>\n')
    with open(f"{OUT}/tiddalik-{n:02d}.svg", "w") as fh:
        fh.write(doc)


def tufts(land: str, pts: list) -> str:
    return "".join(tuft(a, b, sc, LAND[land][4]) for a, b, sc in pts)


GREEN_TUFTS = [(40, 470, 1), (760, 480, 1.1), (90, 560, 1.3), (700, 570, 1.2)]

# 01 cover
kx, ky = perch(130, 476, 1.25)
svg(1, "Tiddalik the Thirsty Frog", "Paper-cut cover: a round green frog called Tiddalik sits smiling at the edge of a blue billabong, under a pale gum tree where a kookaburra perches on a branch, with green hills behind.", DAY, [
    sun(680, 100, 40), cloud(200, 100, 1.1), cloud(470, 70, .8), *back("green"),
    gum(130, 476, 1.25), kookaburra(kx, ky, .95), billabong(540, 500, 210, 44),
    frog(330, 538, 1.45, 0, "happy"), tufts("green", GREEN_TUFTS), front("green")])

# 02 waking up thirsty
svg(2, "Tiddalik wakes up thirsty", "Paper-cut dawn scene: as the sun rises over the hills, Tiddalik the green frog wakes up by the full billabong with his eyes on the water and his pink tongue hanging out, very thirsty.", DAWN, [
    sun(620, 360, 60), cloud(180, 120, 1.2, "#FFE1D2"), cloud(520, 90, 1, "#FFE1D2"), *back("green"),
    gum(100, 470, 1.15), billabong(560, 506, 200, 42),
    frog(300, 540, 1.4, 0, "thirsty"), drops([(392, 352)], BLUE_LT), marks(["M238 384 l-14 -12", "M364 378 l14 -12"], "#fff", 4),
    tufts("green", GREEN_TUFTS), front("green")])

# 03 drinking the billabong
svg(3, "Gulp, gulp, gulp!", "Paper-cut scene: Tiddalik, already bigger and rounder with water sloshing in his tummy, gulps a stream of water from the billabong, which has shrunk to a small pool inside a wide ring of brown mud.", DAY, [
    sun(690, 90, 38), cloud(200, 100, 1.1), *back("green"),
    gum(80, 470, 1.1), billabong(560, 506, 200, 42, .5),
    frog(300, 548, 1.55, .35, "gulp"),
    stroke("M545 504 Q460 300 304 424", BLUE, 14) + stroke("M540 496 Q460 318 314 422", BLUE_LT, 4), sip_arrows((545, 504), (460, 300), (304, 424)),
    tufts("turning", [(40, 470, 1), (760, 480, 1.1)]), tufts("green", [(90, 560, 1.3), (700, 570, 1.2)]), front("green")])

# 04 drinking the river
river_bed = ('<path filter="url(#p)" d="M470 360 Q430 390 470 420 Q520 460 420 500 Q330 540 360 600 H540 Q500 548 590 506 Q680 460 560 418 Q520 396 540 360Z" fill="#B8865A"/>'
             '<path d="M496 372 Q470 394 500 420 Q536 452 460 494 Q400 528 420 560 Q470 520 530 498 Q600 462 530 424 Q500 400 516 372Z" fill="#CE9E70"/>')
svg(4, "He drinks the river too", "Paper-cut scene: the grass has turned yellow, and Tiddalik, now as round as a ball, slurps the very last of the river, leaving a dry, sandy riverbed winding back to the hills.", HOT, [
    sun(140, 100, 46, True), cloud(560, 90, 1, "#FFF1DC"), *back("turning"),
    gum(700, 470, 1.15, True, "turning"), river_bed,
    '<ellipse cx="480" cy="530" rx="40" ry="10" fill="#4FAEE0"/>',
    frog(230, 560, 1.75, .65, "gulp"),
    stroke("M480 528 Q400 300 234 404", BLUE, 13) + stroke("M474 520 Q400 318 244 402", BLUE_LT, 4), sip_arrows((480, 528), (400, 300), (234, 404)),
    tufts("turning", [(40, 470, 1), (620, 560, 1.2), (760, 560, 1.1)]), front("turning")])

# 05 as big as a hill, the land is dry
svg(5, "As big as a hill", "Paper-cut scene: Tiddalik sits huge and swollen, as big as a hill, with all the water sloshing inside his tummy. All around him the red earth is dry and cracked, the waterhole is only mud, and the gum trees droop in the heat.", HOT, [
    sun(110, 90, 50, True), *back("dry"),
    gum(70, 480, 1.0, False, "dry"), gum(760, 470, .9, True, "dry"),
    billabong(170, 548, 120, 26, 0), cracks(["M40 600 l18 -22 l24 4", "M30 470 l18 10 l20 -6"]),
    frog(470, 566, 2.4, 1, "full"),
    heat([(150, 330), (190, 316), (770, 330)]), tufts("dry", [(300, 590, 1)]), front("dry")])

# 06 the animals meet
kx, ky = perch(120, 520, 1.15)
far6, mid6, near6 = back("dry")
svg(6, "The thirsty animals", "Paper-cut scene: on the dry red earth, the thirsty animals gather under a drooping gum tree to make a plan — Kookaburra on a branch, Koala at the foot of the tree, Kangaroo, Wombat and Emu — while behind the hills, huge round Tiddalik rises up as big as a hill himself.", HOT, [
    sun(250, 80, 40, True), far6, frog(560, 446, 1.6, 1, "full"), mid6, near6,
    gum(120, 520, 1.15, False, "dry"), kookaburra(kx, ky, .95),
    koala(200, 540, .9), kangaroo(330, 548, 1.05), wombat(486, 556, .95, True), emu(630, 556, .95, True),
    cracks(["M60 590 l18 -12 l22 6", "M560 590 l20 -12 l20 6 l18 -10"]),
    front("dry")])

# huge Tiddalik used on pages 7-11
BIG = (568, 566, 1.95)
TREE_L = (110, 520, 1.15)

# 07 Kookaburra laughs
kx, ky = perch(*TREE_L)
svg(7, "Kookaburra laughs", "Paper-cut scene: Kookaburra sits on the branch of a dry gum tree, throws back her head and laughs a great big laugh, but huge round Tiddalik just blinks at her with sleepy eyes.", HOT, [
    sun(400, 80, 36, True), *back("dry"),
    gum(*TREE_L, False, "dry"), kookaburra(kx, ky, 1.25, mood="laugh"),
    marks([f"M{kx + 90} {ky - 110} q14 -12 30 -6", f"M{kx + 96} {ky - 82} q20 -6 34 4", f"M{kx + 84} {ky - 136} q8 -18 26 -18"], "#fff", 5),
    frog(*BIG, 1, "blink"),
    cracks(["M60 590 l18 -12 l22 6", "M230 520 l18 8 l18 -8"]), front("dry")])

# 08 Kangaroo hops
svg(8, "Kangaroo hops", "Paper-cut scene: Kangaroo bounces high up in the air with his feet tucked, above his own shadow on the dry red earth, but huge round Tiddalik just sits and stares.", HOT, [
    sun(400, 80, 36, True), *back("dry"),
    '<ellipse cx="220" cy="552" rx="70" ry="12" fill="#8F3F22" opacity=".35"/>',
    marks(["M120 520 q-20 -60 10 -120", "M150 470 q-12 -40 6 -80", "M160 552 q30 -18 60 0", "M200 560 q20 -12 40 0"], "#FFF3D6", 4),
    kangaroo(220, 420, 1.15),
    frog(*BIG, 1, "full"),
    cracks(["M60 590 l18 -12 l22 6", "M330 540 l18 8 l18 -8"]), front("dry")])

# 09 Wombat rolls
svg(9, "Wombat rolls", "Paper-cut scene: round brown Wombat rolls about on his back on the dry earth, with his short legs waving in the air, but huge Tiddalik only yawns a big yawn.", HOT, [
    sun(400, 80, 36, True), *back("dry"),
    wombat(220, 552, 1.3, False, True),
    marks(["M150 430 q-10 -14 0 -26", "M200 418 v-26", "M250 430 q10 -14 0 -26", "M110 540 q-20 -18 -10 -40", "M330 540 q20 -18 10 -40"], "#FFF3D6", 4),
    frog(*BIG, 1, "yawn"),
    cracks(["M60 590 l18 -12 l22 6", "M330 470 l18 8 l18 -8"]), front("dry")])

# 10 Emu dances, Koala pulls a face
svg(10, "Emu dances, Koala pulls a face", "Paper-cut scene: Emu dances a wobbly dance on one leg while Koala sits on the ground pulling a silly face, crossed eyes and tongue out, and the corner of huge Tiddalik's mouth starts to twitch.", HOT, [
    sun(400, 80, 36, True), *back("dry"),
    emu(130, 556, 1.0, False, True), koala(280, 552, 1.0, False, True),
    marks(["M60 360 q-12 -14 -2 -30", "M200 330 q12 -14 2 -30", "M330 400 q12 -12 6 -28"], "#FFF3D6", 4),
    frog(*BIG, 1, "twitch"),
    marks(["M672 360 l14 -10", "M676 376 h16"], INK, 3),
    cracks(["M60 590 l18 -12 l22 6"]), front("dry")])

# 11 Eel ties herself in a knot
kx, ky = perch(80, 500, 1.0)
svg(11, "Eel ties herself in a knot", "Paper-cut scene: Eel rises out of the last little muddy puddle and twists herself into a big, loopy, silly knot, while Kookaburra watches from a branch and huge Tiddalik's tummy starts to wobble.", HOT, [
    sun(400, 80, 36, True), *back("dry"),
    gum(80, 500, 1.0, False, "dry"), kookaburra(kx, ky, .9),
    billabong(210, 550, 95, 20, .35, False),
    eel(220, 548, 1.2, "knot"), lip(210, 550, 95, 20, "#6FA9C9"),
    frog(*BIG, 1, "wobble"),
    marks(["M392 330 q-14 10 0 22 q14 10 0 22", "M420 270 q-12 -8 -4 -22", "M748 262 q12 -8 4 -22"], INK, 3.4),
    cracks(["M40 590 l18 -12 l22 6"]), front("dry")])

# 12 SPLOOSH!
gush = ('<path d="M388 446 Q410 452 432 446 L470 566 H350Z" fill="#4FAEE0" opacity=".9"/>'
        + stroke("M400 452 L382 556 M420 452 L438 556", BLUE_LT, 5)
        + stroke("M372 446 Q230 400 120 510", BLUE, 30) + stroke("M372 440 Q236 396 132 500", BLUE_LT, 9)
        + stroke("M448 446 Q590 400 700 510", BLUE, 30) + stroke("M448 440 Q584 396 688 500", BLUE_LT, 9))
svg(12, "SPLOOSH!", "Paper-cut scene: Tiddalik laughs so hard that the water gushes out of his wide-open mouth in great blue fountains, splashing down to fill a big new pool around him, and he is already shrinking back down to frog size.", WARM, [
    cloud(160, 90, 1.1), cloud(650, 80, 1), *back("turning"),
    '<ellipse cx="400" cy="560" rx="460" ry="70" fill="#2F86C0" filter="url(#p)"/><ellipse cx="400" cy="566" rx="420" ry="52" fill="#4FAEE0"/>',
    frog(410, 560, 1.75, .45, "laugh"), gush,
    drops([(250, 330), (200, 360), (580, 330), (630, 360), (150, 430), (680, 430), (300, 470), (530, 470)]),
    marks(["M300 270 q-14 -16 -6 -36", "M520 270 q14 -16 6 -36", "M410 250 v-36"], "#fff", 6),
    marks(["M60 540 q20 -24 46 0", "M700 540 q24 -24 50 0", "M180 570 q14 -14 30 0", "M610 574 q14 -14 30 0"], "#fff", 5)])

# 13 water for everyone
kx, ky = perch(110, 480, 1.15)
svg(13, "Water is for sharing", "Paper-cut scene: the land is green again and the billabong is full. Tiddalik, a little frog once more, smiles on the bank while Kangaroo, Emu and Wombat come to drink, Eel peeks out of the water, Koala sits by the gum tree and Kookaburra perches above.", DAY, [
    sun(690, 90, 38), cloud(330, 90, 1.1), *back("green"),
    gum(110, 480, 1.15), kookaburra(kx, ky, .9), koala(66, 548, .75),
    billabong(390, 500, 175, 42, 1, False),
    eel(400, 506, .9, "peek"), marks(["M372 516 q16 8 36 0"], BLUE_LT, 3),
    emu(745, 524, .85, True), kangaroo(615, 516, .95, True, "joy"),
    frog(250, 546, 1.15, 0, "joy"), wombat(570, 574, .95, True),
    tufts("green", [(330, 572, 1), (760, 580, 1.1)]), front("green")])
