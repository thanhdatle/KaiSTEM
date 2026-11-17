#!/usr/bin/env python3
"""Generates the 13 "Eat, My Coat, Eat!" flip-book SVGs (Nasreddin Hodja, Türkiye) from shared parts.

Usage: python3 coat_gen.py <output-dir>
Scale rule: every person is drawn with the page's single k, so grown-ups are all one size, Elif is always
about half a grown-up, and the donkey's back is about at Hodja's chest.
Two outfits: WORK = a patched, dusty brown robe with a rope sash; COAT = a long crimson coat with a wide
golden fur collar, fur cuffs, a fur front band and a fur hem. Hodja always has a big white turban with a
green cap on top and a white beard.
Courtyard pages: the low round table (sofra) has its tray top at TRAY_Y; people seated behind it sit at
SEAT_Y so the tray hides their laps.
"""
import re
import sys

OUT = sys.argv[1]
INK = "#2B2320"
SKIN = {"hodja": "#E2B38A", "g1": "#D29C72", "g2": "#ECC29C", "g3": "#C68C60", "host": "#DDA982", "elif": "#E8B790"}
WORK, WORK_D, PATCH, PATCH2, ROPE, DUST = "#8B6B47", "#6E5236", "#B08A5A", "#6A7A4A", "#D8C08A", "#E6D6B6"
COAT, COAT_D, FUR, FUR_D, GOLD = "#A8323E", "#7E2230", "#D3A062", "#A87A44", "#F2C14E"
TURBAN, TURBAN_D, CAPG, BEARD, BEARD_D = "#FBF8F0", "#D9D0BE", "#4F8F5A", "#F3F0E8", "#CFC9BC"
WALL, WALL_D, TILE, TILE_D, STONE, STONE_D = "#F4E8D2", "#E2D2B4", "#C8643C", "#A34E2E", "#E6D2AA", "#CDB68A"
WOOD, WOOD_D, BLUE, BLUE_D = "#A7703F", "#7A4E2A", "#3D7FA8", "#2C5E80"
LEAF, LEAF_D, GRAPE = "#6FAF55", "#4F8C3E", "#7A4C8E"
COPPER, COPPER_L, COPPER_D = "#CF8740", "#EDB373", "#9C5F28"
SOUP, BOWL, BOWL_B = "#E58B33", "#F6F2EA", "#3D7FA8"
RUG, RUG_D, RUG_Y = "#B8433A", "#8E2F2A", "#F2C14E"
ROAD, ROAD_D, GRASS, GRASS_D = "#E7CF9F", "#CDB27C", "#8CC46A", "#5E9E4A"
MTN, MTN_D = "#A9B9D3", "#8FA2C2"
DAY = [(0, "#86CDEA"), (1, "#EAF6FA")]
EVENING = [(0, "#F6B98A"), (.55, "#FBE0B6"), (1, "#FFF1D6")]
TRAY_Y, SEAT_Y = 505, 482


def stroke(d: str, col: str = INK, w: float = 5) -> str:
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def group(x: float, y: float, s: float, flip: bool, inner: str, shadow: bool = True) -> str:
    f = ' filter="url(#p)"' if shadow else ""
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{f}>{inner}</g>'


def end_pt(d: str) -> tuple:
    nums = re.findall(r"-?\d+(?:\.\d+)?", d)
    return float(nums[-2]), float(nums[-1])


# ---------------------------------------------------------------- people
ARMS = {  # (screen-left arm, screen-right arm) from shoulders at (-30,-160) / (30,-160), standing coordinates
    "down": ("M-30 -160 Q-48 -120 -44 -84", "M30 -160 Q48 -120 44 -84"),
    "wave": ("M-30 -160 Q-48 -120 -44 -84", "M30 -160 Q66 -176 68 -226"),
    "open": ("M-30 -160 Q-62 -140 -80 -158", "M30 -160 Q62 -140 80 -158"),
    "hug": ("M-30 -160 Q-66 -168 -84 -196", "M30 -160 Q66 -168 84 -196"),
    "belly": ("M-30 -160 Q-50 -120 -16 -110", "M30 -160 Q50 -120 16 -110"),
    "dip": ("M-30 -160 Q-70 -140 -80 -80", "M30 -160 Q48 -120 44 -84"),
    "heart": ("M-30 -160 Q-44 -118 -6 -138", "M30 -160 Q48 -120 44 -84"),
    "spoon": ("M-30 -160 Q-48 -120 -40 -96", "M30 -160 Q54 -120 20 -160"),
    "think": ("M-30 -160 Q-48 -120 -44 -84", "M30 -160 Q54 -126 14 -142"),
    "hoe": ("M-30 -160 Q-12 -126 22 -128", "M30 -160 Q46 -120 36 -98"),
    "walk": ("M-30 -160 Q-50 -120 -30 -88", "M30 -160 Q50 -120 58 -94"),
    "ladle": ("M-30 -160 Q-48 -120 -44 -84", "M30 -160 Q58 -134 54 -112"),
    "offer": ("M-30 -160 Q-24 -118 14 -120", "M30 -160 Q62 -134 56 -120"),
    "welcome": ("M-30 -160 Q-66 -168 -84 -196", "M30 -160 Q48 -120 44 -84"),
    "eat": ("M-30 -160 Q-46 -122 -36 -96", "M30 -160 Q46 -122 36 -96"),
}
FRONT_ARMS = {"spoon", "think", "heart", "belly"}


def eyes(mood: str, look: float, ey: float = -194) -> str:
    lx = look * 3
    if mood in ("laugh", "happy"):
        return stroke(f"M-17 {ey + 2} q6 -7 12 0 M5 {ey + 2} q6 -7 12 0", INK, 3)
    if mood == "stare":
        return "".join(f'<circle cx="{sx * 11}" cy="{ey}" r="7" fill="#fff"/><circle cx="{sx * 11 + lx}" cy="{ey}" r="3.6" fill="{INK}"/>'
                       for sx in (-1, 1)) + stroke(f"M-18 {ey - 12} q7 -5 13 -1 M18 {ey - 12} q-7 -5 -13 -1", INK, 2.6)
    if mood == "busy":
        return stroke(f"M-16 {ey} q5 4 10 0 M6 {ey} q5 4 10 0", INK, 3)
    out = "".join(f'<circle cx="{sx * 11 + lx}" cy="{ey + (-2 if mood == "think" else 0)}" r="3.4" fill="{INK}"/>' for sx in (-1, 1))
    if mood == "sad":
        out += stroke(f"M-19 {ey - 9} L-6 {ey - 13} M19 {ey - 9} L6 {ey - 13}", INK, 2.6)
    if mood == "think":
        out += stroke(f"M-18 {ey - 11} L-6 {ey - 11} M6 {ey - 14} q6 -4 12 0", INK, 2.6)
    return out


def mouth(mood: str, m: float) -> str:
    if mood == "laugh":
        return f'<path d="M-10 {m} Q0 {m + 2} 10 {m} Q8 {m + 12} 0 {m + 12} Q-8 {m + 12} -10 {m}Z" fill="#7A2E28"/>'
    if mood == "stare":
        return f'<ellipse cy="{m + 4}" rx="5" ry="6" fill="#7A2E28"/>'
    if mood == "sad":
        return stroke(f"M-7 {m + 5} q7 -6 14 0", "#7A2E28", 2.6)
    if mood == "think":
        return stroke(f"M-6 {m + 2} h12", "#7A2E28", 2.6)
    return stroke(f"M-9 {m} q9 8 18 0", "#7A2E28", 2.8)


def hat_back(hat: str, col: str) -> str:
    if hat == "turban":
        return f'<circle cy="-254" r="16" fill="{CAPG}"/><circle cx="-5" cy="-259" r="4" fill="#fff" opacity=".25"/>'
    if hat == "scarf":
        return f'<path d="M-36 -190 Q-42 -236 0 -238 Q42 -236 36 -190 Q42 -156 28 -146 L-28 -146 Q-42 -156 -36 -190Z" fill="{col}"/>'
    return ""


def hat_front(hat: str, col: str) -> str:
    if hat == "turban":
        return (f'<ellipse cy="-230" rx="43" ry="23" fill="{TURBAN}"/>'
                + stroke("M-38 -226 Q0 -208 38 -230 M-36 -240 Q0 -222 37 -242 M-24 -250 Q4 -236 28 -251", TURBAN_D, 3))
    if hat == "cap":
        return (f'<path d="M-29 -204 Q-31 -240 0 -242 Q31 -240 29 -204 Q0 -212 -29 -204Z" fill="{col}"/>'
                + stroke("M-29 -208 Q0 -216 29 -208", "#00000033", 4))
    if hat == "tall":
        return (f'<path d="M-27 -206 L-22 -262 Q0 -272 22 -262 L27 -206 Q0 -214 -27 -206Z" fill="{col}"/>'
                + f'<path d="M-28 -206 Q0 -216 28 -206 L28 -216 Q0 -226 -28 -216Z" fill="{RUG}"/>')
    if hat == "scarf":
        dots = "".join(f'<circle cx="{a}" cy="{b}" r="2.6" fill="#fff" opacity=".8"/>' for a, b in [(-16, -224), (0, -230), (16, -224), (-26, -208), (26, -208)])
        return (f'<path d="M-31 -200 Q-30 -234 0 -234 Q30 -234 31 -200 Q0 -220 -31 -200Z" fill="{col}"/>' + dots
                + f'<path d="M-10 -164 L0 -150 L10 -164Z" fill="{col}"/>')
    return ""


def beard_art(beard: str) -> str:
    if beard == "hodja":
        return (f'<path d="M-29 -198 Q-32 -158 0 -128 Q32 -158 29 -198 Q16 -178 0 -180 Q-16 -178 -29 -198Z" fill="{BEARD}"/>'
                + stroke("M-14 -164 q2 12 8 20 M10 -166 q-2 12 -6 20 M-2 -170 v22", BEARD_D, 2)
                + f'<path d="M-18 -180 Q-8 -188 0 -184 Q8 -188 18 -180 Q8 -175 0 -179 Q-8 -175 -18 -180Z" fill="{BEARD_D}"/>')
    if beard == "dark":
        return (f'<path d="M-27 -196 Q-26 -166 0 -158 Q26 -166 27 -196 Q12 -180 0 -182 Q-12 -180 -27 -196Z" fill="#4A3B32"/>'
                + f'<path d="M-15 -181 Q0 -188 15 -181 Q0 -177 -15 -181Z" fill="#3A2E28"/>')
    if beard == "stache":
        return f'<path d="M-22 -180 Q-10 -190 0 -184 Q10 -190 22 -180 Q12 -176 0 -180 Q-12 -176 -22 -180Z" fill="#2E2420"/>'
    return ""


def head(skin: str, hat: str, hat_col: str, beard: str, mood: str, look: float) -> str:
    out = hat_back(hat, hat_col)
    out += f'<circle cx="-30" cy="-196" r="7" fill="{skin}"/><circle cx="30" cy="-196" r="7" fill="{skin}"/>'
    out += f'<circle cy="-196" r="30" fill="{skin}"/>'
    if hat in ("cap", "tall"):
        out += f'<path d="M-30 -200 Q-32 -186 -26 -180 L-24 -200Z M30 -200 Q32 -186 26 -180 L24 -200Z" fill="#2E2420"/>'
    out += eyes(mood, look)
    out += f'<circle cx="-19" cy="-182" r="6" fill="#F0705F" opacity=".4"/><circle cx="19" cy="-182" r="6" fill="#F0705F" opacity=".4"/>'
    out += f'<ellipse cx="{look * 2}" cy="-186" rx="5" ry="6" fill="{skin}" stroke="#00000022" stroke-width="2"/>'
    out += beard_art(beard)
    out += mouth(mood, -171 if beard else -174)
    out += hat_front(hat, hat_col)
    return out


def arm(d: str, sleeve: str, skin: str, coat: bool, hand: bool = True, wet: bool = False) -> str:
    hx, hy = end_pt(d)
    out = stroke(d, sleeve, 17)
    if coat:
        out += f'<circle cx="{hx}" cy="{hy}" r="13" fill="{FUR}"/>'
        if wet:
            out += f'<path d="M{hx - 8} {hy + 6} q8 8 16 0 q-2 14 -8 16 q-6 -2 -8 -16Z" fill="{SOUP}"/>'
    if hand:
        out += f'<circle cx="{hx}" cy="{hy}" r="9" fill="{skin}"/>'
    return out


def body_path(pose: str, coat: bool) -> str:
    if coat:
        if pose == "sit":
            return "M-37 -174 Q-48 -130 -52 -94 L52 -94 Q48 -130 37 -174 Q0 -188 -37 -174Z"
        return "M-37 -174 Q-55 -100 -60 -8 L60 -8 Q55 -100 37 -174 Q0 -188 -37 -174Z"
    if pose == "sit":
        return "M-30 -172 Q-38 -130 -41 -94 L41 -94 Q38 -130 30 -172 Q0 -184 -30 -172Z"
    return "M-30 -172 Q-42 -100 -46 -10 L46 -10 Q42 -100 30 -172 Q0 -184 -30 -172Z"


def scallops(x0: float, x1: float, y: float, r: float, col: str) -> str:
    n = max(2, int((x1 - x0) / (r * 1.6)))
    step = (x1 - x0) / n
    return "".join(f'<circle cx="{x0 + step * (i + .5):.1f}" cy="{y}" r="{r}" fill="{col}"/>' for i in range(n))


def person(x: float, y: float, k: float, *, robe: str, robe_d: str, skin: str, hat: str = "cap", hat_col: str = "#5A4A9A",
           beard: str = "", mood: str = "smile", look: float = 0, arms: str = "down", pose: str = "stand",
           flip: bool = False, coat: bool = False, dusty: bool = False, sash: str = "", wet: bool = False,
           prop: str = "", cushion: str = "#5B8FB0") -> str:
    """A person facing us. (x, y) is the feet (or, sitting, the floor under the cushion)."""
    sit = pose == "sit"
    torso = f'<path d="{body_path(pose, coat)}" fill="{robe}"/>'
    bottom = -94 if sit else -9
    if coat:
        torso += f'<rect x="-7" y="-172" width="14" height="{172 + bottom}" fill="{FUR}"/>'
        torso += "".join(f'<rect x="-11" y="{yy}" width="22" height="4" rx="2" fill="{GOLD}"/>' for yy in (-150, -132, -114) if yy < bottom - 6)
        if not sit:
            torso += scallops(-60, 60, -10, 9, FUR)
        torso += f'<ellipse cy="-170" rx="48" ry="17" fill="{FUR}"/>' + scallops(-46, 46, -158, 7, FUR) + scallops(-40, 40, -178, 7, FUR_D)
    if dusty:
        torso += (f'<rect x="-30" y="-74" width="18" height="16" rx="2" fill="{PATCH}" transform="rotate(-8 -21 -66)"/>'
                  f'<rect x="12" y="-138" width="15" height="13" rx="2" fill="{PATCH2}" transform="rotate(10 19 -131)"/>'
                  + stroke("M-28 -72 h14 M-28 -62 h14 M14 -136 h11", "#00000040", 1.6)) if not sit else (
                  f'<rect x="12" y="-138" width="15" height="13" rx="2" fill="{PATCH2}" transform="rotate(10 19 -131)"/>')
        torso += "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{DUST}" opacity=".7"/>' for a, b, r in
                         [(-20, -150, 3), (18, -100, 3.5), (-34, -40, 4), (28, -30, 3), (-8, -120, 2.5), (36, -66, 3)] if b < bottom)
    if sash:
        torso += f'<path d="M-40 -116 Q0 -108 40 -116 L41 -104 Q0 -96 -41 -104Z" fill="{sash}"/>'
        if not sit:
            torso += stroke("M14 -104 l-4 26 M20 -104 l6 24", sash, 4)
    a1, a2 = ARMS[arms]
    sleeve = robe_d if not coat else COAT
    arms_art = arm(a1, sleeve, skin, coat, hand=arms != "dip", wet=wet) + arm(a2, sleeve, skin, coat)
    hd = head(skin, hat, hat_col, beard, mood, look)
    upper = torso + (hd + arms_art if arms in FRONT_ARMS else arms_art + hd) + prop
    if sit:
        lap_col = COAT if coat else robe
        base = f'<ellipse cy="-4" rx="66" ry="13" fill="{cushion}"/>'
        base += f'<ellipse cy="-18" rx="{64 if coat else 58}" ry="22" fill="{lap_col}"/>'
        if coat:
            base += stroke("M-60 -10 Q0 8 60 -10", FUR, 8)
        out = base + f'<g transform="translate(0 90)">{upper}</g>'
    else:
        if pose == "walk":
            feet = f'<ellipse cx="-24" cy="-4" rx="15" ry="7" fill="#4A3426"/><ellipse cx="26" cy="-7" rx="15" ry="7" fill="#4A3426" transform="rotate(-12 26 -7)"/>'
        else:
            feet = f'<ellipse cx="-16" cy="-4" rx="15" ry="7" fill="#4A3426"/><ellipse cx="16" cy="-4" rx="15" ry="7" fill="#4A3426"/>'
        out = feet + upper
    return group(x, y, k, flip, out)


def hodja(x, y, k, outfit="work", **kw):
    if outfit == "coat":
        return person(x, y, k, robe=COAT, robe_d=COAT_D, skin=SKIN["hodja"], hat="turban", beard="hodja", coat=True, **kw)
    return person(x, y, k, robe=WORK, robe_d=WORK_D, skin=SKIN["hodja"], hat="turban", beard="hodja", dusty=True, sash=ROPE, **kw)


def dip_sleeve(x: float, y: float, k: float) -> str:
    """The dipping coat sleeve again, drawn in front of the tray so it visibly reaches into the bowl."""
    d = ARMS["dip"][0]
    hx, hy = end_pt(d)
    cuff = f'<circle cx="{hx}" cy="{hy}" r="14" fill="{FUR}" stroke="{FUR_D}" stroke-width="3"/>' + scallops(hx - 12, hx + 12, hy - 12, 4, FUR_D)
    return group(x, y, k, False, f'<g transform="translate(0 90)">{stroke(d, COAT, 17)}{cuff}</g>')


def guest(who, x, y, k, **kw):
    spec = {
        "g1": dict(robe="#3E6FA0", robe_d="#2E5680", hat="cap", hat_col="#7A4E2A", beard="dark", cushion="#D9A441"),
        "g2": dict(robe="#4E9A6A", robe_d="#3A7A52", hat="scarf", hat_col="#E2748C", cushion="#8E5AA8"),
        "g3": dict(robe="#D9A441", robe_d="#B4832C", hat="cap", hat_col="#B23A3A", cushion="#3E6FA0"),
        "host": dict(robe="#2F8F8A", robe_d="#22706C", hat="tall", hat_col="#F1E4C8", beard="stache", sash="#E58B33", cushion="#B23A3A"),
    }[who]
    spec.update(kw)
    return person(x, y, k, skin=SKIN[who], **spec)


def elif_(x: float, y: float, k: float, arms: str = "down", mood: str = "smile", pose: str = "stand", look: float = 0, flip=False, prop="") -> str:
    """Elif, a little girl about half a grown-up's height: dark braids with red ribbons, yellow dress with red flowers."""
    sk = SKIN["elif"]
    arm_d = {"down": ("M-15 -88 Q-28 -62 -26 -48", "M15 -88 Q28 -62 26 -48"),
             "wave": ("M-15 -88 Q-28 -62 -26 -48", "M15 -88 Q36 -98 40 -132"),
             "both": ("M-15 -88 Q-36 -98 -40 -130", "M15 -88 Q36 -98 40 -130"),
             "spoon": ("M-15 -88 Q-26 -66 -14 -62", "M15 -88 Q30 -70 12 -98")}[arms]
    dress = f'<path d="M-16 -96 Q-30 -46 -31 -20 L31 -20 Q30 -46 16 -96 Q0 -102 -16 -96Z" fill="#F2C14E"/>'
    dress += "".join(f'<circle cx="{a}" cy="{b}" r="3.2" fill="#D9483B"/>' for a, b in [(-14, -40), (6, -32), (20, -52), (-6, -62), (12, -78), (-18, -28)])
    arms_art = "".join(stroke(d, "#F2C14E", 11) + f'<circle cx="{end_pt(d)[0]}" cy="{end_pt(d)[1]}" r="6.5" fill="{sk}"/>' for d in arm_d)
    hd = (stroke("M-21 -114 Q-30 -96 -26 -78 M21 -114 Q30 -96 26 -78", "#3A2A22", 9)
          + f'<circle cx="-26" cy="-78" r="4.5" fill="#D9483B"/><circle cx="26" cy="-78" r="4.5" fill="#D9483B"/>'
          + f'<circle cy="-118" r="24" fill="{sk}"/>'
          + f'<path d="M-25 -116 Q-28 -146 0 -146 Q28 -146 25 -116 Q14 -134 0 -130 Q-14 -134 -25 -116Z" fill="#3A2A22"/>')
    lx = look * 2.5
    if mood == "happy":
        hd += stroke("M-13 -116 q4 -5 9 0 M4 -116 q4 -5 9 0", INK, 2.6)
    else:
        hd += f'<circle cx="{-8 + lx}" cy="-117" r="3" fill="{INK}"/><circle cx="{8 + lx}" cy="-117" r="3" fill="{INK}"/>'
    hd += f'<circle cx="-15" cy="-106" r="5" fill="#F0705F" opacity=".45"/><circle cx="15" cy="-106" r="5" fill="#F0705F" opacity=".45"/>'
    hd += f'<path d="M-8 -104 Q0 -98 8 -104 Q6 -94 0 -94 Q-6 -94 -8 -104Z" fill="#7A2E28"/>' if arms in ("wave", "both") else stroke("M-6 -104 q6 6 12 0", "#7A2E28", 2.4)
    upper = dress + hd + arms_art + prop
    if pose == "sit":
        out = f'<ellipse cy="-4" rx="40" ry="10" fill="#D9A441"/><ellipse cy="-14" rx="34" ry="15" fill="#F2C14E"/><g transform="translate(0 44)">{upper}</g>'
    else:
        out = stroke("M-9 -22 V-6 M9 -22 V-6", sk, 8) + f'<ellipse cx="-10" cy="-4" rx="9" ry="5" fill="#D9483B"/><ellipse cx="10" cy="-4" rx="9" ry="5" fill="#D9483B"/>' + upper
    return group(x, y, k, flip, out)


def donkey(x: float, y: float, k: float, flip: bool = False, mood: str = "calm") -> str:
    """Hodja's grey donkey in side view facing right, (x, y) at the hooves, with a striped saddle cloth."""
    g, gd, gl = "#A39C92", "#7D766D", "#D9D2C6"
    out = stroke("M-66 -122 Q-84 -110 -82 -74", gd, 6) + f'<ellipse cx="-82" cy="-70" rx="6" ry="10" fill="#5A544C"/>'
    out += stroke("M-46 -90 V-6 M-28 -90 V-6 M34 -90 V-6 M52 -90 V-6", gd, 14)
    out += "".join(f'<rect x="{a - 8}" y="-9" width="16" height="9" rx="2" fill="#4A4038"/>' for a in (-46, -28, 34, 52))
    out += f'<ellipse cy="-112" rx="72" ry="40" fill="{g}"/><ellipse cy="-92" rx="50" ry="16" fill="{gl}"/>'
    out += f'<path d="M-24 -150 L22 -150 L26 -112 L-28 -112Z" fill="{RUG}"/>' + stroke("M-25 -140 H23 M-26 -126 H24", RUG_Y, 4)
    out += f'<path d="M32 -140 Q50 -168 66 -184 L94 -168 Q76 -138 62 -108Z" fill="{g}"/>' + stroke("M36 -146 Q52 -172 68 -188", "#5A544C", 6)
    out += (f'<ellipse cx="62" cy="-210" rx="7" ry="22" fill="{g}" transform="rotate(-28 62 -210)"/>'
            f'<ellipse cx="78" cy="-212" rx="7" ry="22" fill="{g}" transform="rotate(-8 78 -212)"/>'
            f'<ellipse cx="78" cy="-212" rx="3" ry="15" fill="#E7B7AE" transform="rotate(-8 78 -212)"/>')
    out += f'<ellipse cx="90" cy="-170" rx="31" ry="19" fill="{g}" transform="rotate(30 90 -170)"/>'
    out += f'<ellipse cx="108" cy="-152" rx="15" ry="13" fill="{gl}"/><circle cx="114" cy="-154" r="2.6" fill="{INK}"/>'
    if mood == "wow":
        out += f'<circle cx="84" cy="-180" r="7" fill="#fff"/><circle cx="86" cy="-180" r="3.6" fill="{INK}"/>' + stroke("M104 -146 q4 5 9 0", INK, 2.4)
    else:
        out += f'<circle cx="86" cy="-178" r="3.4" fill="{INK}"/>' + stroke("M102 -144 q5 4 10 -1", INK, 2.4)
    return group(x, y, k, flip, out)


# ---------------------------------------------------------------- table things
def bowl(x: float, y: float, s: float = 1, steam: bool = False) -> str:
    out = (f'<path d="M{x - 22 * s} {y} Q{x - 20 * s} {y + 20 * s} {x} {y + 21 * s} Q{x + 20 * s} {y + 20 * s} {x + 22 * s} {y}Z" fill="{BOWL}"/>'
           + stroke(f"M{x - 19 * s} {y + 8 * s} Q{x} {y + 14 * s} {x + 19 * s} {y + 8 * s}", BOWL_B, 3 * s)
           + f'<ellipse cx="{x}" cy="{y}" rx="{22 * s}" ry="{7 * s}" fill="{BOWL}"/><ellipse cx="{x}" cy="{y + .5}" rx="{18.5 * s}" ry="{5 * s}" fill="{SOUP}"/>')
    if steam:
        out += steam_at(x, y - 8, .6 * s)
    return out


def bowl_front(x: float, y: float, s: float = 1) -> str:
    """Just the front of a bowl (body and front lip), drawn over a sleeve to tuck it into the soup."""
    return (f'<path d="M{x - 22 * s} {y} Q{x - 20 * s} {y + 20 * s} {x} {y + 21 * s} Q{x + 20 * s} {y + 20 * s} {x + 22 * s} {y} '
            f'Q{x} {y + 7 * s} {x - 22 * s} {y}Z" fill="{BOWL}"/>'
            + stroke(f"M{x - 19 * s} {y + 8 * s} Q{x} {y + 14 * s} {x + 19 * s} {y + 8 * s}", BOWL_B, 3 * s)
            + f'<path d="M{x - 18 * s} {y + 2} Q{x} {y + 6 * s} {x + 18 * s} {y + 2} Q{x} {y + 4 * s} {x - 18 * s} {y + 2}Z" fill="{SOUP}"/>')


def steam_at(x: float, y: float, s: float = 1) -> str:
    return f'<g opacity=".75">{stroke(f"M{x - 10 * s} {y} q-8 -14 0 -26 q8 -12 0 -26 M{x + 10 * s} {y - 4} q-8 -14 0 -26 q8 -12 0 -24", "#fff", 4 * s)}</g>'


def bread(x: float, y: float) -> str:
    return (f'<ellipse cx="{x}" cy="{y}" rx="26" ry="9" fill="#D9A25A"/><ellipse cx="{x}" cy="{y - 2}" rx="21" ry="6" fill="#E9BC72"/>'
            + "".join(f'<circle cx="{x + a}" cy="{y - 2}" r="1.6" fill="#8A5A2A"/>' for a in (-10, -3, 4, 11)))


def pilaf(x: float, y: float) -> str:
    return (f'<ellipse cx="{x}" cy="{y + 4}" rx="30" ry="8" fill="{BOWL}"/><path d="M{x - 24} {y + 2} Q{x} {y - 26} {x + 24} {y + 2}Z" fill="#FFFDF4"/>'
            + "".join(f'<circle cx="{x + a}" cy="{y + b}" r="1.6" fill="#E3D9B8"/>' for a, b in [(-10, -4), (0, -12), (8, -6), (-2, -2), (12, 0)]))


def grapes(x: float, y: float) -> str:
    pts = [(0, 0), (-8, -6), (8, -6), (-4, -13), (4, -13), (0, -20), (-12, -1), (12, -1)]
    return (f'<ellipse cx="{x}" cy="{y + 4}" rx="20" ry="6" fill="{BOWL}"/>' + "".join(f'<circle cx="{x + a}" cy="{y + b}" r="5" fill="{GRAPE}"/>' for a, b in pts)
            + f'<path d="M{x} {y - 24} q6 -4 10 -2" stroke="{LEAF_D}" stroke-width="2.4" fill="none"/>')


def tureen(x: float, y: float, steam: bool = True) -> str:
    out = (f'<g filter="url(#p)"><path d="M{x - 40} {y - 30} Q{x - 44} {y + 6} {x} {y + 10} Q{x + 44} {y + 6} {x + 40} {y - 30}Z" fill="{COPPER}"/>'
           f'<ellipse cx="{x}" cy="{y - 30}" rx="42" ry="10" fill="{COPPER_L}"/><ellipse cx="{x}" cy="{y - 29}" rx="35" ry="7" fill="{SOUP}"/>'
           + stroke(f"M{x - 34} {y - 14} Q{x} {y - 4} {x + 34} {y - 14}", COPPER_D, 3)
           + f'<path d="M{x - 42} {y - 24} q-12 0 -12 9 q0 7 8 7" stroke="{COPPER_D}" stroke-width="4" fill="none"/>'
           f'<path d="M{x + 42} {y - 24} q12 0 12 9 q0 7 -8 7" stroke="{COPPER_D}" stroke-width="4" fill="none"/></g>')
    if steam:
        out += steam_at(x, y - 44, 1)
    return out


def table(cx: float, rx: float, items: list) -> str:
    stand = f'<path filter="url(#p)" d="M{cx - 70} {TRAY_Y} L{cx - 56} {TRAY_Y + 44} L{cx + 56} {TRAY_Y + 44} L{cx + 70} {TRAY_Y}Z" fill="{WOOD_D}"/>'
    tray = (f'<ellipse filter="url(#p)" cx="{cx}" cy="{TRAY_Y}" rx="{rx}" ry="30" fill="{COPPER}"/>'
            f'<ellipse cx="{cx}" cy="{TRAY_Y - 2}" rx="{rx - 12}" ry="23" fill="{COPPER_L}"/>'
            + stroke(f"M{cx - rx + 30} {TRAY_Y + 6} Q{cx} {TRAY_Y + 30} {cx + rx - 30} {TRAY_Y + 6}", COPPER, 2.4))
    return stand + tray + "".join(items)


def rug(cx: float, w: float) -> str:
    x0, x1 = cx - w / 2, cx + w / 2
    out = f'<path d="M{x0 + 30} 486 L{x1 - 30} 486 L{x1 + 10} 584 L{x0 - 10} 584Z" fill="{RUG}"/>'
    out += f'<path d="M{x0 + 42} 496 L{x1 - 42} 496 L{x1 - 6} 574 L{x0 + 6} 574Z" fill="none" stroke="{RUG_Y}" stroke-width="4"/>'
    for i in range(6):
        a = x0 + 30 + (w - 60) * (i + .5) / 6
        out += f'<path d="M{a} 548 l14 14 l-14 14 l-14 -14Z" fill="{RUG_Y}"/><path d="M{a} 556 l6 6 l-6 6 l-6 -6Z" fill="{RUG_D}"/>'
    return out


# ---------------------------------------------------------------- scenery
def cloud(x: float, y: float, s: float = 1, op: float = .92) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{op}">'
            '<circle cx="-40" cy="6" r="26"/><circle cx="-8" cy="-12" r="32"/><circle cx="32" cy="-4" r="28"/><rect x="-66" y="6" width="126" height="28" rx="14"/></g>')


def house(x: float, y: float, w: float, h: float, door: str = BLUE, wall: str = "#FBF6EC", windows: int = 1) -> str:
    """A whitewashed village house with a red-tile roof. (x, y) is its bottom-left corner."""
    out = f'<g filter="url(#p)"><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/>'
    out += f'<path d="M{x - 12} {y - h + 4} L{x + w / 2} {y - h - 34} L{x + w + 12} {y - h + 4}Z" fill="{TILE}"/>'
    out += stroke(f"M{x - 4} {y - h - 2} L{x + w + 4} {y - h - 2}", TILE_D, 3) + "</g>"
    out += f'<rect x="{x + w / 2 - 13}" y="{y - 46}" width="26" height="46" rx="12" fill="{door}"/>'
    for i in range(windows):
        wx = x + (w / (windows + 1)) * (i + 1) - 10 if windows > 1 else x + 14
        out += f'<rect x="{wx}" y="{y - h + 18}" width="20" height="22" rx="8" fill="{BLUE_D}"/>'
    return out


def mosque_far(x: float, y: float) -> str:
    c = "#C9D3E4"
    return (f'<g opacity=".9"><rect x="{x - 40}" y="{y - 40}" width="80" height="40" fill="{c}"/><path d="M{x - 32} {y - 40} Q{x} {y - 90} {x + 32} {y - 40}Z" fill="{c}"/>'
            f'<rect x="{x + 50}" y="{y - 120}" width="12" height="120" fill="{c}"/><path d="M{x + 48} {y - 120} L{x + 56} {y - 146} L{x + 64} {y - 120}Z" fill="{c}"/>'
            f'<rect x="{x + 46}" y="{y - 92}" width="20" height="5" fill="{c}"/></g>')


def street_back() -> list:
    return [cloud(150, 80, 1), cloud(640, 64, .85),
            f'<path d="M-20 300 L120 200 L210 250 L330 160 L470 250 L560 190 L700 260 L820 210 V320 H-20Z" fill="{MTN}"/>',
            f'<path d="M290 190 L330 160 L370 190 L350 186 L330 196 L310 186Z" fill="#F7FAFF"/>',
            mosque_far(500, 318), f'<path d="M0 318 H800 V430 H0Z" fill="{GRASS}" opacity=".55"/>']


def ground(y: float = 430) -> str:
    return (f'<path filter="url(#p)" d="M0 {y} Q400 {y - 18} 800 {y} V600 H0Z" fill="{ROAD}"/>'
            + "".join(f'<ellipse cx="{a}" cy="{b}" rx="{r}" ry="{r * .45}" fill="{ROAD_D}" opacity=".6"/>' for a, b, r in
                      [(60, 560, 14), (210, 480, 9), (380, 590, 12), (560, 470, 10), (700, 560, 13), (300, 520, 7), (760, 470, 8)]))


def dust(x: float, y: float, s: float = 1) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{DUST}" opacity=".9">'
            '<circle cx="-10" cy="-6" r="10"/><circle cx="6" cy="-10" r="12"/><circle cx="20" cy="-4" r="8"/></g>')


def sparkle(x: float, y: float, s: float = 1, col: str = GOLD) -> str:
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4Z" fill="{col}"/>'


def plant_pot(x: float, y: float) -> str:
    return (f'<g filter="url(#p)"><path d="M{x - 22} {y - 40} L{x - 16} {y} L{x + 16} {y} L{x + 22} {y - 40}Z" fill="{TILE}"/>'
            f'<circle cx="{x - 12}" cy="{y - 52}" r="13" fill="{LEAF}"/><circle cx="{x + 10}" cy="{y - 56}" r="14" fill="{LEAF_D}"/>'
            f'<circle cx="{x}" cy="{y - 66}" r="12" fill="{LEAF}"/></g>'
            + "".join(f'<circle cx="{x + a}" cy="{y + b}" r="6" fill="#E2485A"/>' for a, b in [(-14, -60), (8, -70), (14, -50), (-2, -54)]))


def courtyard(gate: bool = True, window_x: float = 300) -> list:
    tiles = "".join(f'<path d="M{a} 126 a17 17 0 0 1 34 0Z" fill="{TILE}"/>' for a in range(-10, 810, 30))
    vine = stroke("M0 140 Q100 130 200 142 T400 140 T600 142 T800 138", WOOD_D, 4)
    leaves = "".join(f'<ellipse cx="{a}" cy="{b}" rx="13" ry="9" fill="{LEAF if i % 2 else LEAF_D}" transform="rotate({(-25, 20, -10)[i % 3]} {a} {b})"/>'
                     for i, (a, b) in enumerate([(40, 146), (120, 136), (180, 150), (260, 140), (340, 152), (430, 138), (500, 150), (580, 140), (660, 152), (740, 138), (780, 150)]))
    bunches = "".join(f'<g fill="{GRAPE}"><circle cx="{a}" cy="{b}" r="5"/><circle cx="{a - 6}" cy="{b - 8}" r="5"/><circle cx="{a + 6}" cy="{b - 8}" r="5"/><circle cx="{a}" cy="{b - 15}" r="5"/></g>'
                      for a, b in [(150, 170), (470, 168), (705, 170)])
    out = [f'<rect y="112" width="800" height="370" fill="{WALL}"/>',
           f'<path d="M500 200 q30 -10 60 4 q-10 22 -60 -4Z M90 380 q40 -8 70 6 q-30 14 -70 -6Z M620 330 q40 -6 60 8 q-34 10 -60 -8Z" fill="{WALL_D}"/>',
           f'<rect y="110" width="800" height="18" fill="{TILE_D}"/>', tiles, vine, leaves, bunches,
           f'<path d="M{window_x - 30} 250 V196 a30 30 0 0 1 60 0 V250Z" fill="{BLUE}"/><path d="M{window_x - 22} 244 V198 a22 22 0 0 1 44 0 V244Z" fill="#2B3F55"/>'
           + stroke(f"M{window_x} 176 V244 M{window_x - 22} 214 H{window_x + 22}", BLUE, 4)]
    if gate:
        out.append(f'<path d="M36 482 V300 a58 58 0 0 1 116 0 V482Z" fill="{WALL_D}"/>'
                   f'<path d="M46 482 V302 a48 48 0 0 1 96 0 V482Z" fill="#BFE3F2"/>'
                   f'<path d="M46 482 V420 Q94 410 142 420 V482Z" fill="{ROAD}"/>'
                   f'<path d="M46 482 V318 L66 326 V474Z" fill="{WOOD}"/>')
    out.append(f'<rect y="476" width="800" height="124" fill="{STONE}"/>' + stroke("M0 478 H800", STONE_D, 5)
               + stroke("M0 520 H800 M0 566 H800 M120 478 v42 M300 478 v42 M520 478 v42 M700 478 v42 M40 520 v46 M220 520 v46 M420 520 v46 M620 520 v46 M760 520 v46", STONE_D, 2))
    return out


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/coat-{n:02d}.svg", "w") as fh:
        fh.write(doc)


K = 1.0    # outdoor pages
KF = .95   # courtyard pages
FEAST_A = 560  # table centre on the arrival pages (4, 5, 8): room for the gate on the left
FEAST_B = 450  # table centre on the close pages (9-13)


def guests_a(mood: str = "smile", looks=(1, -1, -1)) -> list:
    """Three guests seated behind the table on the arrival pages."""
    return [guest("g1", 440, SEAT_Y, KF, pose="sit", mood=mood, look=looks[0], arms="eat"),
            guest("g2", 560, SEAT_Y, KF, pose="sit", mood=mood, look=looks[1], arms="eat"),
            guest("g3", 680, SEAT_Y, KF, pose="sit", mood=mood, look=looks[2], arms="eat")]


def items_a(steam=True) -> list:
    return [bowl(440, TRAY_Y - 18), bowl(560, TRAY_Y - 18), bowl(680, TRAY_Y - 18), bread(500, TRAY_Y + 8), pilaf(620, TRAY_Y + 2),
            tureen(560, TRAY_Y + 20, steam)]


# 01 cover: Hodja, Elif and the donkey on the village road
svg(1, "Eat, My Coat, Eat!", "Paper-cut scene: on a sunny village road in Türkiye, with white houses, red-tile roofs and blue mountains behind, Nasreddin Hodja stands smiling in his patched brown work robe, with his big white turban and white beard. Beside him little Elif in a yellow dress waves, and his grey donkey with a striped saddle cloth stands on the other side.", DAY, [
    *street_back(), house(30, 420, 150, 110, windows=1), house(600, 420, 160, 120, door="#B23A3A", windows=2),
    ground(), hodja(380, 548, K, arms="wave", mood="smile"), elif_(250, 552, K, arms="wave", look=1),
    donkey(560, 546, K * .9, flip=True)])

# 02 Hodja works in his garden all day
rows = "".join(f'<ellipse cx="{a}" cy="{b}" rx="{r}" ry="{r * .7}" fill="{c}"/>' for a, b, r, c in
               [(470, 470, 16, LEAF_D), (520, 474, 14, LEAF), (570, 470, 16, LEAF_D), (620, 474, 14, LEAF), (680, 470, 16, LEAF_D),
                (460, 530, 18, LEAF), (520, 536, 16, LEAF_D), (585, 530, 18, LEAF), (650, 536, 16, LEAF_D), (720, 530, 18, LEAF)])
toms = "".join(f'<circle cx="{a}" cy="{b}" r="6" fill="#E2483A"/>' for a, b in [(466, 462), (574, 462), (684, 462), (590, 522), (724, 524), (464, 522)])
svg(2, "Hodja in his garden", "Paper-cut scene: Nasreddin Hodja, in his big white turban and patched brown work robe tied with a rope, digs in his vegetable garden with a hoe. His robe is dusty, the sun is high, and rows of green plants with red tomatoes grow beside him. His grey donkey rests by a little white house with a red roof.", DAY, [
    f'<circle cx="670" cy="90" r="42" fill="#FFD866"/>', cloud(200, 90, .9),
    f'<path d="M-20 300 L120 210 L240 260 L360 180 L500 260 L640 200 L820 270 V340 H-20Z" fill="{MTN}"/>',
    house(40, 400, 170, 120, windows=1), f'<path filter="url(#p)" d="M0 400 Q400 380 800 404 V600 H0Z" fill="#B88D5A"/>',
    f'<path d="M420 448 H770 M420 506 H770" stroke="#8E6A3E" stroke-width="10" stroke-linecap="round"/>', rows, toms,
    donkey(150, 480, K * .9), hodja(350, 568, K, arms="hoe", mood="smile",
                                    prop=stroke("M-5 -190 L76 -4", WOOD_D, 7) + '<path d="M66 -12 L102 -10 L100 2 L70 4Z" fill="#8A8F96"/>'),
    dust(460, 566, .8)])

# 03 dusty Hodja walks to the feast; a smell of soup drifts from the big house
smell = stroke("M525 392 q-20 -20 0 -40 q20 -20 0 -40 M560 384 q-20 -20 0 -40 q20 -20 0 -40 M600 370 q-16 -18 0 -36", "#F2A65A", 5)
svg(3, "Off to the feast", "Paper-cut scene: Nasreddin Hodja walks along the dusty village road in his patched brown work robe, with little puffs of dust at his feet. Ahead on the right is a big white house with an open arched gate, and a warm orange smell of soup curls up out of it.", DAY, [
    *street_back(), house(20, 420, 130, 100, windows=1),
    f'<g filter="url(#p)"><rect x="440" y="250" width="340" height="176" fill="#FBF6EC"/><path d="M426 254 L610 190 L794 254Z" fill="{TILE}"/></g>',
    f'<path d="M500 426 V346 a40 40 0 0 1 80 0 V426Z" fill="#E0C79A"/><path d="M500 426 V340 L516 348 V420Z" fill="{WOOD}"/>',
    f'<rect x="640" y="290" width="40" height="44" rx="16" fill="{BLUE_D}"/>', f'<g opacity=".9">{smell}</g>',
    ground(), hodja(250, 560, K, arms="walk", pose="walk", mood="smile"), dust(170, 566, 1), dust(320, 572, .7)])

# 04 at the gate: Elif says hello, the guests don't look
svg(4, "Hello, Hodja!", "Paper-cut scene: in a courtyard with a red-tile wall and grapevines, Hodja, in his dusty patched work robe, steps in through the arched gate on the left and waves. Little Elif in her yellow dress waves back to him. At a low round copper table on a red rug, three guests and the host chat and eat soup, all looking at each other and not at Hodja.", DAY, [
    *courtyard(window_x=300), rug(FEAST_A, 400), plant_pot(758, 500),
    guest("host", 350, 492, KF, mood="busy", arms="ladle", look=1, prop=stroke("M54 -112 L78 -60", "#8A8F96", 4) + '<ellipse cx="80" cy="-58" rx="9" ry="5" fill="#8A8F96"/>'),
    *guests_a(), table(FEAST_A, 170, items_a()),
    hodja(100, 568, KF, arms="wave", mood="smile"), elif_(210, 574, KF, arms="wave", look=-1)])

# 05 nobody talks to him, nobody gives him soup
rumble = stroke("M150 512 q8 -8 16 0 q8 8 16 0 q8 -8 16 0 M154 528 q8 -8 16 0 q8 8 16 0", "#8E2F2A", 3.4)
svg(5, "Nobody passes the soup", "Paper-cut scene: Hodja, in his dusty patched robe, sits all alone on a little cushion near the gate, with nothing in front of him and a wobbly tummy-rumble beside him. At the copper table, the host holds out a bowl of soup to the guests, and the three guests eat and chat with each other. Nobody looks at Hodja.", DAY, [
    *courtyard(window_x=300), rug(FEAST_A, 400), plant_pot(758, 500),
    guest("host", 350, 492, KF, mood="smile", arms="offer", look=1, prop=bowl(40, -128, 1.1)),
    *guests_a(), table(FEAST_A, 170, items_a()),
    hodja(110, 576, KF, pose="sit", arms="down", mood="sad", cushion="#9A8A70"), f'<g opacity=".9">{rumble}</g>'])

# 06 Hodja walks home, thinking: "Hmm!"
coat_icon = (f'<path d="M-22 -40 Q-30 0 -34 36 L34 36 Q30 0 22 -40 Q0 -48 -22 -40Z" fill="{COAT}"/><rect x="-4" y="-40" width="8" height="76" fill="{FUR}"/>'
             f'<ellipse cy="-40" rx="26" ry="9" fill="{FUR}"/>' + stroke("M-22 -36 L-40 16 M22 -36 L40 16", COAT, 10)
             + f'<circle cx="-40" cy="16" r="7" fill="{FUR}"/><circle cx="40" cy="16" r="7" fill="{FUR}"/>')
thought = (f'<g filter="url(#p)"><ellipse cx="520" cy="190" rx="92" ry="74" fill="#fff"/><circle cx="436" cy="290" r="14" fill="#fff"/><circle cx="412" cy="322" r="9" fill="#fff"/></g>'
           f'<g transform="translate(520 190) scale(1.2)">{coat_icon}</g>')
svg(6, "Hmm!", "Paper-cut scene: Hodja walks home along the village road in his dusty patched robe, one hand on his white beard, thinking hard. A big white thought bubble above him shows a fine crimson coat with a golden fur collar.", DAY, [
    *street_back(), house(560, 420, 180, 120, windows=2), ground(),
    hodja(330, 562, K, arms="think", pose="walk", mood="think", flip=True), thought])

# 07 at home he puts on his fine fur coat; the donkey is amazed
svg(7, "The fine fur coat", "Paper-cut scene: in front of his little white house, Hodja stands proudly with his arms out, wearing his fine long crimson coat with a wide golden fur collar, fur cuffs, a fur hem and shiny gold buttons. Gold sparkles twinkle around him, and his grey donkey stares with big round eyes.", DAY, [
    cloud(180, 80, .9), cloud(650, 70, .8),
    f'<path d="M-20 300 L140 200 L260 250 L400 170 L520 250 L660 190 L820 260 V330 H-20Z" fill="{MTN}"/>',
    f'<path d="M0 320 H800 V430 H0Z" fill="{GRASS}" opacity=".55"/>', house(60, 430, 200, 150, windows=1),
    ground(), hodja(400, 560, K, outfit="coat", arms="open", mood="happy"),
    sparkle(300, 260, 1), sparkle(510, 240, .8), sparkle(290, 430, .7), sparkle(500, 300, .9),
    donkey(665, 552, K * .9, flip=True, mood="wow")])

# 08 back at the gate in the coat: Elif says hello again, the host rushes to welcome him
svg(8, "Welcome! Welcome!", "Paper-cut scene: Hodja steps back in through the arched gate, now wearing his fine crimson fur coat. Little Elif, in her yellow dress, waves to him just like before. The host in his tall cap hurries over, waving one arm high in welcome, and the three guests at the copper table turn to smile at Hodja.", DAY, [
    *courtyard(window_x=300), rug(FEAST_A, 400), plant_pot(758, 500),
    *guests_a("smile", looks=(-1, -1, -1)), table(FEAST_A, 170, items_a()),
    elif_(232, 574, KF, arms="wave", look=-1), hodja(110, 568, KF, outfit="coat", arms="down", mood="smile"),
    guest("host", 320, 566, KF, arms="welcome", mood="happy", look=-1)])

# 09-12: the close view. Hodja has the best seat in the middle; his bowl sits to his left at DIP_X.
KB, SEAT_B = 1.1, 478  # closer camera for 9-12
DIP_X, DIP_Y = FEAST_B - 80 * KB, SEAT_B + (-80 + 90) * KB + 2


def guests_b(mood="smile", looks=(1, -1, -1)) -> list:
    return [guest("g1", 262, SEAT_B, KB, pose="sit", mood=mood, look=looks[0], arms="eat"),
            guest("g2", 590, SEAT_B, KB, pose="sit", mood=mood, look=looks[1], arms="eat"),
            guest("g3", 702, SEAT_B, KB, pose="sit", mood=mood, look=looks[2], arms="eat")]


def items_b(dip: bool = False) -> list:
    return [bowl(262, TRAY_Y - 18), bowl(590, TRAY_Y - 18), bread(470, TRAY_Y + 16), pilaf(530, TRAY_Y + 4), grapes(280, TRAY_Y + 18),
            tureen(620, TRAY_Y + 22, True), bowl(DIP_X, DIP_Y, 1.25, steam=not dip)]


svg(9, "Sit here! Have some soup!", "Paper-cut scene: now Hodja in his fine crimson fur coat sits in the best seat in the middle of the copper table, with a steaming bowl of orange soup in front of him. The guests smile at him, and the host stands beside the table holding out his hands to offer soup. Bread, rice and grapes are all around.", DAY, [
    *courtyard(window_x=230), rug(FEAST_B, 480),
    guest("host", 112, 566, KB, arms="offer", mood="happy", look=1),
    hodja(FEAST_B, SEAT_B, KB, outfit="coat", pose="sit", arms="down", mood="smile", cushion="#E2B04A"),
    *guests_b(looks=(1, -1, -1)), table(FEAST_B, 230, items_b())])

slurp = (stroke(f"M{DIP_X - 40} {DIP_Y - 14} l-12 -10 M{DIP_X + 40} {DIP_Y - 14} l12 -10 M{DIP_X} {DIP_Y - 26} v-14", SOUP, 4)
         + "".join(f'<circle cx="{DIP_X + a}" cy="{DIP_Y + b}" r="4" fill="{SOUP}"/>' for a, b in [(-30, -26), (32, -28), (-14, -38), (16, -40)]))
svg(10, "Eat, my coat, eat!", "Paper-cut scene: Hodja, sitting in the middle in his crimson fur coat, has dipped his furry coat sleeve right into his bowl of orange soup, and little drops of soup splash up. Everyone at the table stares with wide eyes and round open mouths, and the host stands frozen beside the table.", DAY, [
    *courtyard(window_x=230), rug(FEAST_B, 480),
    guest("host", 112, 566, KB, arms="down", mood="stare", look=1),
    hodja(FEAST_B, SEAT_B, KB, outfit="coat", pose="sit", arms="dip", mood="smile", look=-1, cushion="#E2B04A"),
    *guests_b("stare", looks=(1, -1, -1)), table(FEAST_B, 230, items_b(dip=True)), dip_sleeve(FEAST_B, SEAT_B, KB), bowl_front(DIP_X, DIP_Y, 1.25), slurp])

svg(11, "The coat must be the guest!", "Paper-cut scene: Hodja, in his crimson fur coat with one soupy orange cuff, holds his hands out and smiles as he explains. The three guests and the host, with his hand on his chest, still stare at him with wide eyes and open mouths.", DAY, [
    *courtyard(window_x=230), rug(FEAST_B, 480),
    guest("host", 112, 566, KB, arms="heart", mood="stare", look=1),
    hodja(FEAST_B, SEAT_B, KB, outfit="coat", pose="sit", arms="open", mood="smile", wet=True, cushion="#E2B04A"),
    *guests_b("stare", looks=(1, -1, -1)), table(FEAST_B, 230, items_b(dip=True))])

svg(12, "Sorry, Hodja!", "Paper-cut scene: the host stands beside the table with his hand on his heart, laughing and saying sorry. Hodja, in his crimson fur coat, laughs too with his eyes shut tight, and the three guests laugh along with him.", DAY, [
    *courtyard(window_x=230), rug(FEAST_B, 480),
    guest("host", 112, 566, KB, arms="heart", mood="laugh", look=1),
    hodja(FEAST_B, SEAT_B, KB, outfit="coat", pose="sit", arms="belly", mood="laugh", wet=True, cushion="#E2B04A"),
    *guests_b("laugh"), table(FEAST_B, 230, items_b(dip=True))])

# 13 everyone eats together; the coat hangs on a peg and Hodja shares his bowl with Elif
hung = (f'<g filter="url(#p)"><circle cx="0" cy="-6" r="5" fill="{WOOD_D}"/>'
        f'<path d="M-30 6 Q-40 80 -44 150 L44 150 Q40 80 30 6 Q0 -6 -30 6Z" fill="{COAT}"/>'
        f'<rect x="-6" y="4" width="12" height="146" fill="{FUR}"/>' + scallops(-44, 44, 150, 7, FUR)
        + f'<ellipse cy="8" rx="34" ry="12" fill="{FUR}"/>' + stroke("M-30 10 Q-46 60 -44 110 M30 10 Q46 60 44 110", COAT_D, 14)
        + f'<circle cx="-44" cy="112" r="9" fill="{FUR}"/><circle cx="44" cy="112" r="9" fill="{FUR}"/>'
        + f'<path d="M38 112 q6 8 12 0 q-2 10 -6 12 q-4 -2 -6 -12Z" fill="{SOUP}"/></g>')
spoon = stroke("M20 -160 L14 -136", "#8A8F96", 3.4)
svg(13, "Everyone eats together", "Paper-cut scene: in the warm evening light, Hodja's crimson fur coat hangs on a peg on the courtyard wall. Hodja, back in his old patched robe, sits at the copper table and shares a bowl of soup with little Elif beside him; both hold spoons. The host and the three guests eat and smile all around the table.", EVENING, [
    *courtyard(gate=False, window_x=160), f'<g transform="translate(640 150)">{hung}</g>', rug(FEAST_B, 520),
    guest("host", 172, SEAT_Y, KF, pose="sit", arms="eat", mood="happy"),
    guest("g1", 284, SEAT_Y, KF, pose="sit", arms="eat", mood="smile", look=1),
    hodja(418, SEAT_Y, KF, pose="sit", arms="spoon", mood="happy", cushion="#E2B04A", prop=spoon),
    elif_(512, SEAT_Y, KF, pose="sit", arms="spoon", mood="happy", prop=stroke("M12 -98 L6 -78", "#8A8F96", 3)),
    guest("g2", 618, SEAT_Y, KF, pose="sit", arms="eat", mood="laugh", look=-1),
    guest("g3", 720, SEAT_Y, KF, pose="sit", arms="eat", mood="smile", look=-1),
    table(FEAST_B, 230, [bowl(172, TRAY_Y - 18), bowl(284, TRAY_Y - 18), bowl(618, TRAY_Y - 18), bowl(720, TRAY_Y - 18),
                         bread(380, TRAY_Y + 14), pilaf(560, TRAY_Y + 10), grapes(650, TRAY_Y + 18), bowl(466, TRAY_Y - 14, 1.1, steam=True)])])
