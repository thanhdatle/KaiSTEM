#!/usr/bin/env python3
"""Generates the 40 Lạc-Long-Quân-and-Âu-Cơ flip-book SVGs (lac-01 cover, lac-02 … lac-40 story pages).

Usage: python3 lac_gen.py <output-dir>
All characters come from lac_parts.py, so they look the same on every page.
Scale rule: on any one page every person uses the same factor k, so Lạc Long Quân and Âu Cơ (~290 tall
with headdresses) stay taller than villagers (~250), who stay about twice as tall as one of the hundred
children (~128). In far crowds a "tiny" child at scale s matches kid() at k = .45 s.
Story-order rule: the bọc first appears on page 25, the eggs on 27, the babies on 28, the hundred children on 29;
the fish spirit only on 07–10, the fox on 11–13, the tree spirit on 14–16. Crowd pages draw exact counts:
100 eggs (27), 100 children (29), 50 + 50 children (34 and 36).
"""
import sys

from lac_parts import *  # noqa: F401,F403  (drawers and colours)

OUT = sys.argv[1]
DAY = [(0, "#7FCBEA"), (1, "#EAF7F0")]
SEA_SKY = [(0, "#6FBFE6"), (1, "#E8F6F8")]
DEEP = [(0, "#3F8FC0"), (.5, "#2A6C9E"), (1, "#183F68")]
GOLDEN = [(0, "#8FCFEA"), (.55, "#FDE7C0"), (1, "#FCD39A")]
STORMY = [(0, "#7C8DAA"), (1, "#D6DEE8")]
DUSK = [(0, "#3B4F86"), (.6, "#9A8FC0"), (1, "#F2C9B8")]
MIST = [(0, "#A9D8E6"), (1, "#F4F9F2")]


def svg(n: int, title: str, desc: str, stops: list, body: list) -> None:
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    joined = "\n".join(b for b in body if b)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-labelledby="t d">\n'
           f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n<defs>'
           '<clipPath id="w"><rect width="800" height="600" rx="36"/></clipPath>'
           '<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1b1b33" flood-opacity=".3"/></filter>'
           f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           '</defs>\n<g clip-path="url(#w)"><rect width="800" height="600" fill="url(#sky)"/>\n' + joined + '\n</g>\n</svg>\n')
    with open(f"{OUT}/lac-{n:02d}.svg", "w", encoding="utf-8") as fh:
        fh.write(doc)


# ---------------------------------------------------------------- scenery
def sea(top: float = 330, x0: float = 0, x1: float = 800, col: str = SEA) -> str:
    rip = " ".join(f"M{a} {b} h{w}" for a, b, w in [(60, 30, 40), (220, 56, 30), (400, 80, 46), (680, 40, 34), (120, 120, 36),
                                                     (320, 150, 30), (520, 110, 40), (700, 150, 30), (240, 210, 44), (600, 220, 36)]
                   if x0 <= a <= x1 - w)
    return (f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{600 - top}" fill="{col}"/>'
            f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="10" fill="{SEA_L}" opacity=".6"/>'
            + (f'<g transform="translate(0 {top})" opacity=".6">{stroke(rip, SEA_L, 3)}</g>' if rip else ""))


def front_waves(y: float, x0: float = 0, x1: float = 800) -> str:
    """A strip of curly foreground waves (drawn after a dragon so its tail dips into the sea)."""
    n = int((x1 - x0) / 80) + 1
    crest = "".join(" q20 -26 40 -8 q10 8 40 8" for _ in range(n))
    xe = x0 + n * 80
    end = "V600" if x1 >= 800 else f"Q{xe + 30} {y + 70} {xe - 10} 600"
    return (f'<path d="M{x0} {y}{crest} {end} H{x0}Z" fill="{SEA}"/>'
            + stroke(f"M{x0} {y}{crest}", SEA_L, 4))


def beach(y: float = 470, x0: float = 0, x1: float = 800) -> str:
    end = "V600" if x1 >= 800 else f"Q{x1 + 30} {y + 40} {x1 + 50} 600"
    return (f'<path filter="url(#p)" d="M{x0} {y} Q{(x0 + x1) / 2} {y - 26} {x1} {y + 6} {end} H{x0}Z" fill="{SAND}"/>'
            f'<path d="M{x0} {y + 70} Q{(x0 + x1) / 2} {y + 50} {x1} {y + 66} V600 H{x0}Z" fill="{SAND_D}" opacity=".4"/>')


def ground(y: float = 440, col: str = GRASS, back: str = GRASS_L) -> str:
    return (f'<path filter="url(#p)" d="M0 {y} Q220 {y - 24} 420 {y - 4} T800 {y - 6} V600 H0Z" fill="{col}"/>'
            f'<path d="M0 {y + 80} Q300 {y + 60} 560 {y + 76} T800 {y + 70} V600 H0Z" fill="{back}" opacity=".45"/>')


def hills(top: float = 300, far: str = HILL_F, near: str = HILL_N) -> str:
    return (f'<path d="M0 {top + 30} Q70 {top - 70} 140 {top + 10} Q200 {top - 110} 270 {top} Q340 {top - 60} 420 {top + 20} '
            f'Q500 {top - 100} 580 {top} Q650 {top - 70} 720 {top + 10} Q770 {top - 50} 800 {top} V{top + 160} H0Z" fill="{HILL_FF}"/>'
            f'<path d="M0 {top + 70} Q110 {top - 10} 200 {top + 60} Q300 {top - 30} 400 {top + 60} Q520 {top - 20} 620 {top + 60} '
            f'Q720 {top} 800 {top + 50} V{top + 200} H0Z" fill="{far}"/>'
            f'<path d="M0 {top + 120} Q160 {top + 60} 330 {top + 110} T800 {top + 100} V{top + 260} H0Z" fill="{near}" opacity=".7"/>')


def peaks_right(x0: float = 380) -> str:
    """The mountain side of the split pages: green peaks rising on the right."""
    return (f'<path filter="url(#p)" d="M{x0} 600 L{x0 + 20} 400 Q{x0 + 70} 300 {x0 + 120} 330 Q{x0 + 180} 170 {x0 + 260} 250 '
            f'Q{x0 + 320} 120 {x0 + 400} 220 L{x0 + 440} 600Z" fill="{HILL_F}"/>'
            f'<path d="M{x0 + 10} 600 L{x0 + 40} 470 Q{x0 + 120} 380 {x0 + 200} 430 Q{x0 + 300} 330 {x0 + 440} 380 V600Z" fill="{HILL_N}"/>')


def paddy(top: float = 400) -> str:
    rows = "".join(rice_tuft(a + (b % 2) * 30, b, .6 + (b - top) / 500) for b in range(int(top) + 30, 600, 40) for a in range(30, 800, 70))
    return (f'<rect y="{top}" width="800" height="{600 - top}" fill="{PADDY}"/>'
            + stroke(" ".join(f"M0 {b} H800" for b in range(int(top) + 50, 600, 80)), "#7FAF5E", 6) + f'<g opacity=".9">{rows}</g>'
            + stroke(" ".join(f"M{a} {top + 20 + (a * 7) % 140} h30" for a in range(40, 800, 110)), PADDY_L, 3))


def light_rays() -> str:
    return ('<g fill="#fff" opacity=".07"><path d="M120 0 L200 0 L330 600 L190 600Z"/><path d="M420 0 L470 0 L560 600 L470 600Z"/>'
            '<path d="M640 0 L700 0 L780 600 L700 600Z"/></g>')


def seafloor(y: float = 520) -> str:
    return f'<path d="M0 {y} Q200 {y - 20} 420 {y} T800 {y - 4} V600 H0Z" fill="#D9C08C" filter="url(#p)"/>'


def rock(x: float, y: float, s: float = 1) -> str:
    return group(x, y, s, '<path d="M-70 0 Q-80 -50 -30 -70 Q20 -86 60 -50 Q84 -20 70 0Z" fill="#9AA39A"/>'
                 '<path d="M-30 -60 Q0 -70 30 -54" stroke="#BCC4BC" stroke-width="6" fill="none"/>')


def glow_stone(x: float, y: float, r: float = 14) -> str:
    return (f'<circle cx="{x}" cy="{y}" r="{r * 2.4:.0f}" fill="#FFC23A" opacity=".3"/><circle cx="{x}" cy="{y}" r="{r}" fill="#F2652A"/>'
            f'<circle cx="{x - r * .3:.1f}" cy="{y - r * .3:.1f}" r="{r * .4:.1f}" fill="#FFD27A"/>')


def rainbow(x0: float, x1: float, y: float, h: float) -> str:
    cols = ("#E36B5B", "#F2B53A", "#F7D046", "#7CBF5A", "#5BA6D6", "#B07CC6")
    return '<g opacity=".75">' + "".join(stroke(f"M{x0 + i * 10} {y} Q{(x0 + x1) / 2} {y - h + i * 12} {x1 - i * 10} {y}", c, 10)
                                        for i, c in enumerate(cols)) + '</g>'


def rocky_hill(cave: bool = True) -> str:
    out = '<path filter="url(#p)" d="M0 520 L0 300 Q60 220 160 240 Q260 250 330 360 Q380 450 380 520Z" fill="#9AA39A"/>'
    return out + ('<path d="M120 470 Q120 400 190 400 Q260 400 260 470Z" fill="#3A3A40"/>' if cave else "")


def split_bg(mid: float = 400) -> list:
    """Sea on the left, mountains on the right — for the pages where the family decides to share."""
    return [sun(400, 84, 34), cloud(150, 90, .7), cloud(620, 70, .6), sea(330), peaks_right(mid - 20),
            beach(500, 0, mid - 40), f'<path d="M{mid - 60} 600 Q{mid - 40} 520 {mid + 40} 512 Q{mid + 200} 490 800 510 V600Z" fill="{GRASS}" filter="url(#p)"/>']


WARM_HILLS = ("#B5CF9A", "#8FB878")
WARM_GROUND = ("#A9C77A", "#C9DE9E")
MOUNT_HILLS = ("#9FD0B0", "#6FB384")
MOUNT_GROUND = ("#86CA7A", "#B4E0A0")
LEAVES = ('<g fill="#3F8E4E"><ellipse cx="{0}" cy="{1}" rx="9" ry="4" transform="rotate(30 {0} {1})"/>'
          '<ellipse cx="{2}" cy="{3}" rx="9" ry="4"/><ellipse cx="{4}" cy="{5}" rx="9" ry="4" transform="rotate(-20 {4} {5})"/></g>')

# ================================================================ pages
# 01 cover
svg(1, "Lạc Long Quân and Âu Cơ", "Paper-cut cover: on the left, a long friendly jade-green dragon with a flame-like red crest and curly gold whiskers rises out of blue sea waves. On the right, on green mountains, the fairy Âu Cơ stands smiling and waving, in a peach top and rose skirt, with a crown of white feathers and pink flowers in her long black hair. A white egret flies above her, and a golden sun with a many-pointed star shines between them.", DAY, [
    sun(400, 90, 42), cloud(560, 70, .6), sea(360, 0, 800), peaks_right(380),
    dragon(200, 338, .56, rot=-26, amp=30), front_waves(420, 0, 430),
    auco(610, 540, .72, arms="wave"), crane(660, 160, .6), flowers([(520, 560, .9), (720, 570, 1), (560, 590, .8), (760, 530, .8)])])

# ---- Part 1: the dragon lord of the sea
svg(2, "The water palace", "Paper-cut scene deep under the sea: a palace with a big glowing pearl dome on coral-pink arches, with a gold star on top, stands on the sandy sea floor among swaying sea grass and shells. In front of it a long jade-green dragon with a red crest and a gold belly swims happily, with little yellow and orange fish and bubbles all around.", DEEP, [
    light_rays(), seafloor(), sea_palace(560, 520, .85), seagrass([(70, 560), (130, 580), (330, 560), (760, 560)]),
    dragon(270, 300, .6, amp=40), fishy(120, 150, .8), fishy(170, 190, .6, "#F08FB0"), fishy(700, 140, .7, "#F2B53A", True),
    fishy(440, 440, .6, "#E0874A"), bubbles([(390, 220, 6), (400, 190, 4), (410, 160, 8), (90, 380, 5), (100, 350, 3)]),
    shell(240, 560), shell(420, 570, "#F2B0C0"), shell(720, 585)])

svg(3, "Part dragon", "Paper-cut scene under the sea: the jade-green dragon Lạc Long Quân swims in a big swooping S-shape, smiling, with his red crest and curly gold whiskers, while a little school of yellow, pink and orange fish swims along with him. Far away, the pearl dome of the water palace glows on the sea floor.", DEEP, [
    light_rays(), seafloor(540), sea_palace(700, 540, .4), seagrass([(40, 580), (300, 590), (560, 580)]),
    dragon(380, 290, .78, amp=56, waves=1.6),
    *[fishy(x, y, .55, c, f) for x, y, c, f in [(120, 110, "#F2B53A", False), (160, 140, "#F08FB0", False), (200, 112, "#E0874A", False),
                                                 (610, 470, "#F2B53A", True), (650, 500, "#F08FB0", True), (560, 510, "#E0874A", True)]],
    bubbles([(520, 120, 6), (530, 90, 4), (300, 470, 5)])])

svg(4, "Up out of the sea", "Paper-cut scene on a sunny beach: Lạc Long Quân, now looking like a tall young man, walks up out of the waves, waving, with sparkles around him. He wears a teal tunic with a gold wave pattern, a blue kilt, a gold star pendant and three teal plumes in his hair. On the sand, villagers, a man, a woman and two children, wave back. A low hut woven from grass stands behind them.", SEA_SKY, [
    sun(660, 80, 34), cloud(200, 80, .7), sea(300), f'<path filter="url(#p)" d="M380 600 Q390 470 520 450 Q660 436 800 446 V600Z" fill="{SAND}"/>',
    grass_hut(740, 458, .55), llq(230, 566, .74, arms="wave"), front_waves(500, 0, 400), stroke("M160 512 q30 -14 70 -4 q40 -8 70 6", "#fff", 5),
    sparkles([(170, 330, 1), (350, 300, .8), (330, 420, .7), (180, 450, .6)]),
    kid(450, 576, .74, 2, "wave"), villager(540, 570, .74, "m1", "wave"), villager(630, 572, .74, "w1", "wave", flip=True), kid(730, 578, .74, 5, "up")])

svg(5, "Just call me", "Paper-cut scene in a green village of low grass huts: Lạc Long Quân stands in the middle with his arms open wide, smiling at the villagers gathered round him — two women, a man and three children. Green hills rise behind them.", DAY, [
    cloud(160, 80, .7), cloud(620, 60, .6), hills(250), ground(440), grass_hut(110, 462, .8), grass_hut(690, 452, .72),
    villager(170, 572, .72, "w2"), kid(270, 578, .72, 1), llq(400, 568, .72, arms="open", mood="big"), kid(520, 580, .72, 3, "up"),
    villager(600, 572, .72, "m2"), kid(700, 580, .72, 6), villager(760, 576, .72, "w3", flip=True)])

svg(6, "Splash! Home to the sea", "Paper-cut scene: the long jade-green dragon dives head-first back into the sea with a big white splash, his red tail tuft still up in the air. On the sandy beach at the bottom left, a villager and two children wave goodbye.", SEA_SKY, [
    sun(120, 80, 30), cloud(600, 90, .7), sea(300), dragon(470, 300, .5, rot=48, amp=24),
    front_waves(380, 0, 800), '<g fill="#fff"><path d="M500 390 L520 330 L540 380 L560 300 L580 378 L606 320 L616 392Z"/><circle cx="500" cy="300" r="9"/><circle cx="626" cy="290" r="8"/><circle cx="470" cy="340" r="7"/><circle cx="650" cy="350" r="6"/><circle cx="560" cy="268" r="7"/></g>',
    beach(500, 0, 380), villager(80, 590, .52, "m3", "wave"), kid(150, 592, .52, 4, "wave"), kid(210, 592, .52, 7, "up")])

# ---- Part 2: Bố ơi, come and help us!
svg(7, "The giant fish spirit", "Paper-cut scene on a grey, stormy sea: a giant slate-blue fish spirit with orange spiky fins, a row of little fins underneath and a grumpy frown thrashes in the water, making big waves. Two little wooden boats with bird-head prows are tossed about. On the shore at the bottom left, a man, a woman and a child look on, worried.", STORMY, [
    cloud(160, 70, .8, .7), cloud(560, 60, .9, .7), sea(260), f'<g transform="rotate(-14 130 330)">{boat(130, 330, .56)}</g>', f'<g transform="rotate(16 700 310)">{boat(690, 310, .54, True)}</g>',
    big_fish(450, 360, .92), front_waves(420, 260, 800), stroke("M250 300 q30 -30 60 0 M600 290 q30 -30 60 0", "#fff", 4),
    beach(520, 0, 330), villager(70, 596, .5, "m1", "hip", "worry"), villager(150, 598, .5, "w3", "low", "worry"), kid(220, 598, .5, 0, "hold", "worry")])

svg(8, "Bố ơi! Come and help us!", "Paper-cut scene: on a sandy shore under a grey sky, three villagers and a child cup their hands beside their open, smiling mouths and call out across the sea. Out in the waves, the long jade-green dragon is rising up out of the water, heading toward them.", STORMY, [
    cloud(560, 70, .8, .7), sea(300), dragon(620, 300, .5, rot=52, amp=24, flip=True), front_waves(370, 380, 800),
    beach(470, 0, 800), villager(110, 580, .7, "m1", "call", "call"), villager(210, 582, .7, "w1", "call", "call"),
    kid(300, 586, .7, 2, "call", "call"), villager(390, 584, .7, "m3", "call", "call")])

svg(9, "Hot, hot, hot!", "Paper-cut scene on the sea: Lạc Long Quân, in his teal tunic and teal plumes, stands in a long wooden boat with a bird-head prow and throws a glowing orange-red stone. On the right, the giant blue fish spirit has opened its big mouth wide to gobble, and the hot stone is flying straight toward it.", STORMY, [
    sea(270), big_fish(590, 350, .8, mouth="open", flip=True),
    front_waves(452, 0, 800), llq(190, 432, .6, arms="point"), boat(190, 440, .62), stroke("M250 330 Q330 260 400 300", "#FFD27A", 4, ' stroke-dasharray="8 8"'),
    glow_stone(420, 312)])

svg(10, "Far, far away", "Paper-cut scene on a calm, sunny sea: far away on the horizon, the giant fish spirit, now very small, swims off out of sight. Near the shore, two long wooden boats sail happily, with smiling villagers waving in them, and two children cheer on the sand.", DAY, [
    sun(140, 90, 40), cloud(520, 80, .7), sea(300), big_fish(690, 310, .2), stroke("M630 300 h-30 M640 314 h-26", "#fff", 3),
    villager(250, 392, .4, "m2", "up", "big"), boat(250, 410, .5), villager(530, 448, .38, "w1", "wave", "big"), boat(530, 462, .45, True),
    beach(520, 0, 800), kid(120, 594, .55, 3, "up", "big"), kid(700, 594, .55, 1, "wave")])

svg(11, "The nine-tailed fox", "Paper-cut scene: at the mouth of a dark cave in a grey rocky hill sits a sly orange fox spirit with nine separate bushy, wavy, cream-tipped tails waving behind it, grinning, with a stolen basket of fish. Down in the green village nearby, a woman and a child stand by their low grass huts, looking worried.", DAY, [
    cloud(560, 80, .7), hills(270), ground(470), rocky_hill(),
    fox(250, 560, .95, held="basket"), grass_hut(540, 492, .7), grass_hut(730, 500, .62),
    villager(600, 580, .7, "w2", "hip", "worry"), kid(690, 584, .7, 4, "hold", "worry")])

svg(12, "Here comes the water!", "Paper-cut scene: Lạc Long Quân stands on the right with both arms raised high, and sparkles fly around his hands as a huge blue sea wave with a curling white crest rises behind them and rolls toward the grey rocky hill on the left. At the mouth of the cave, the nine-tailed fox spirit stares at the wave with wide eyes. Both stand on green grass, and a villager behind Lạc Long Quân cheers with his arms up.", STORMY, [
    hills(280),
    f'<path filter="url(#p)" d="M800 600 V300 Q660 200 520 240 Q420 270 400 340 Q430 300 470 310 Q500 330 480 370 Q540 380 560 460 Q600 540 560 600Z" fill="{SEA}"/>',
    f'<path d="M800 380 Q700 330 620 360 Q580 380 600 440 Q640 520 620 600 H800Z" fill="{SEA_D}" opacity=".5"/>',
    stroke("M404 336 Q430 280 520 248 Q640 214 790 290", "#fff", 9) + stroke("M470 312 q16 10 8 30", "#fff", 6),
    '<g fill="#fff"><circle cx="390" cy="320" r="8"/><circle cx="372" cy="296" r="6"/><circle cx="410" cy="290" r="5"/></g>',
    ground(480), rocky_hill(), fox(200, 560, .8, mood="oh"),
    villager(730, 586, .62, "m2", "up", "big"), llq(620, 590, .62, arms="up", mood="big"),
    sparkles([(570, 420, .9), (668, 414, .9), (620, 396, .6)])])

svg(13, "A big new lake", "Paper-cut scene: where the rocky hill used to be, there is now a wide, calm blue lake. Far away on the right, the little nine-tailed fox spirit runs off into the green forest, tails streaming behind. On the near shore, Lạc Long Quân and the villagers, a man, a woman and two children, cheer.", DAY, [
    sun(120, 80, 34), hills(230), ground(380),
    f'<ellipse cx="380" cy="440" rx="350" ry="62" fill="{SEA_L}" filter="url(#p)"/><ellipse cx="380" cy="437" rx="322" ry="50" fill="{SEA}"/>',
    stroke("M200 430 h40 M420 450 h50 M300 460 h30 M520 424 h34", SEA_L, 3), tree(700, 380, .55), tree(760, 390, .5), tree(640, 392, .45),
    fox(690, 360, .26, pose="run", mood="oh"),
    ground(520, GRASS_D, GRASS), villager(120, 590, .66, "m1", "up", "big"), kid(210, 594, .66, 6, "up", "big"),
    llq(330, 590, .66, mood="big"), villager(450, 592, .66, "w3", "up", "big"), kid(540, 596, .66, 2, "up", "big")])

svg(14, "The grumpy tree spirit", "Paper-cut scene in misty green hills: a huge, gnarled old tree spirit with a grumpy face in its bark stomps on its root feet and shakes its branch arms, so leaves fly everywhere. White egrets fly away from it. On the left, a villager and a child peek out, worried, from behind a big rock.", MIST, [
    hills(250), ground(470), tree_spirit(450, 556, .9),
    stroke("M260 220 q-14 10 0 20 M640 220 q14 10 0 20 M280 300 q-14 10 0 20 M620 300 q14 10 0 20", INK, 4),
    LEAVES.format(240, 380, 680, 400, 300, 460), crane(660, 110, .45), crane(740, 160, .38),
    villager(100, 585, .6, "m3", "hip", "worry"), kid(170, 588, .6, 5, "hold", "worry"), rock(120, 600, 1.1)])

svg(15, "A great big dragon ROAR!", "Paper-cut scene in the green hills: the long jade-green dragon flies in from the left with his mouth wide open, giving a great big roar, with roar lines coming from his mouth. On the right, the tree spirit jumps in surprise, its eyes wide and its mouth an O, and leaves flutter off its branches.", MIST, [
    hills(260), ground(480), dragon(215, 200, .72, rot=8, amp=26, mood="roar"),
    stroke("M446 236 q20 10 0 30 M470 222 q30 16 0 54 M496 208 q40 22 0 80", "#fff", 5),
    tree_spirit(650, 566, .8, mood="oh"), LEAVES.format(470, 330, 770, 300, 500, 420)])

svg(16, "Stomp, stomp, far away", "Paper-cut scene: far away over the green mountains, the tree spirit, now very small, hurries off on its root feet, leaning forward. Nearby, white egrets come back to a leafy tree with a nest in it. In front, Lạc Long Quân, two villagers and two children smile and wave.", MIST, [
    hills(250), tree_spirit(640, 330, .26, mood="oh", pose="run"), stroke("M690 300 h26 M694 316 h20", INK, 3), ground(460),
    tree(150, 470, 1.1, nest=True), crane(250, 200, .45, flip=True), crane(200, 300, .5, pose="stand"),
    kid(320, 586, .64, 7, "wave"), llq(420, 582, .64, arms="wave", mood="big"), villager(520, 584, .64, "m2", "up", "big"),
    villager(610, 586, .64, "w1"), kid(700, 590, .64, 3, "up", "big")])

svg(17, "Planting rice", "Paper-cut scene in a flooded rice field below green hills: Lạc Long Quân stands in the shallow water showing how to push a little rice seedling into the mud. Beside him, a woman and a man plant seedlings too, and a child watches, smiling. Rows of young green rice plants grow all around.", DAY, [
    sun(680, 80, 34), cloud(220, 80, .7), hills(220), paddy(380),
    llq(240, 560, .7, arms="plant"), rice_tuft(268, 500, 1.1), villager(410, 566, .7, "w1", "plant", held="seedling"),
    villager(560, 568, .7, "m2", "plant", held="seedling"), kid(680, 578, .7, 2, "hold", "big"),
    stroke("M190 560 q40 -10 90 0 M370 566 q40 -10 90 0 M520 568 q40 -10 90 0", PADDY_L, 4)])

svg(18, "Rice in bamboo tubes", "Paper-cut scene in warm evening light beside a bamboo grove: rice cooks in green bamboo tubes leaning over a crackling fire, with steam puffing out of their tops. Lạc Long Quân points to show how, while a child holding a bowl, a woman, and a man holding a bowl watch, smiling.", GOLDEN, [
    hills(250, *WARM_HILLS), ground(430, *WARM_GROUND), bamboo(660, 470, 300), bamboo(700, 480, 260), bamboo(760, 470, 320),
    bamboo_tube(370, 552, -24), bamboo_tube(420, 554, 22), bamboo_tube(396, 556, 0), fire(396, 566, .9),
    llq(220, 572, .7, arms="point"), kid(510, 582, .7, 0, "bowl", "big"), villager(590, 576, .7, "w2", "low"),
    villager(700, 580, .7, "m1", "reach", held="bowl", flip=True)])

svg(19, "Houses up high", "Paper-cut scene on a sunny day: villagers are building houses on stilts. On the left, a frame of wooden posts stands on a raised platform with a ladder; on the right, a finished house on tall stilts has woven walls and a saddle-shaped thatched roof whose ends sweep up like a boat. Lạc Long Quân points to show the way, a man carries a long wooden post, a child helps, and a woman waves.", DAY, [
    cloud(400, 70, .7), hills(230), ground(440), stilt_house(240, 520, .85, built=False), stilt_house(620, 520, .85),
    villager(110, 584, .64, "m1", "hold", held="post"), llq(400, 584, .64, arms="point"), kid(480, 590, .64, 4, "hold", "big"),
    villager(740, 588, .64, "w3", "wave")])

# ---- Part 3: the fairy of the mountains
svg(20, "Âu Cơ, the mountain fairy", "Paper-cut scene high in misty green mountains: the fairy Âu Cơ stands in a meadow of pink, yellow and white flowers, smiling and holding up a pink flower. She has long black hair, a crown of white feathers and flowers, a peach top and a rose wrap skirt with a patterned band. A white egret stands beside her, and two more fly among the peaks.", MIST, [
    hills(200, *MOUNT_HILLS), cloud(170, 120, .7), cloud(640, 90, .6), crane(150, 220, .4), crane(640, 180, .36, flip=True),
    ground(470, *MOUNT_GROUND), auco(390, 566, .82, arms="reach", held="flower"), crane(560, 570, .74, pose="stand", flip=True),
    flowers([(90, 520, 1), (160, 560, 1.1), (240, 530, .9), (250, 590, 1), (520, 520, .9), (650, 560, 1.1), (720, 520, 1), (700, 590, .9), (130, 590, .9)])])

svg(21, "Down the mountain path", "Paper-cut scene: a winding path leads down from the green mountains to the lowlands, where a river shines. Âu Cơ, small in the distance, walks down the path among flowers, and a white egret flies ahead of her toward the lowlands.", MIST, [
    hills(170, *MOUNT_HILLS), ground(380, *MOUNT_GROUND),
    f'<path d="M0 600 Q120 520 220 540 Q300 556 340 520" stroke="{SEA}" stroke-width="40" fill="none"/>',
    stroke("M760 380 Q640 420 600 460 Q540 520 420 540 Q340 556 300 600", SAND, 34),
    auco(560, 490, .42), crane(330, 300, .5, flip=True),
    flowers([(680, 440, .8), (720, 470, .9), (470, 480, .8), (480, 580, 1), (640, 560, 1), (740, 560, 1), (260, 470, .8)])])

svg(22, "Hello!", "Paper-cut scene beside a sparkling river: on the left, among flowers, Âu Cơ waves and smiles. On the right, by the river, Lạc Long Quân waves and smiles back. Little sparkles float in the air between them.", DAY, [
    cloud(220, 80, .7), hills(240), ground(440),
    f'<path d="M560 440 Q620 500 600 600 H800 V440Z" fill="{SEA}"/>' + stroke("M640 470 h30 M690 520 h40 M650 560 h30", SEA_L, 3),
    flowers([(80, 520, 1), (150, 580, 1), (330, 560, .9), (110, 470, .8), (280, 480, .8)]),
    auco(240, 570, .76, arms="wave", look=2), llq(560, 570, .76, arms="wave", flip=True, look=-2),
    sparkles([(380, 280, .8), (420, 240, .6), (400, 330, .5)])])

svg(23, "Talking and talking", "Paper-cut scene at sunset beside the river: Âu Cơ and Lạc Long Quân stand facing each other, both laughing happily as they talk. A little fish leaps out of the river behind him, and a white egret flies across the indigo and purple sky behind her.", DUSK, [
    hills(260, "#8C9FB0", "#6F8A88"), ground(450, "#7DB56E", "#A6CC90"),
    f'<path d="M520 450 Q600 520 580 600 H800 V450Z" fill="{SEA}"/>', fishy(680, 480, .8, "#F2B53A"), stroke("M650 500 q30 -40 60 -20", "#fff", 3),
    crane(160, 160, .45), auco(300, 572, .78, arms="low", mood="big"), llq(500, 572, .78, arms="open", mood="big", flip=True)])

svg(24, "A wedding with drums", "Paper-cut scene in golden light: in front of a big house on stilts with a saddle-shaped thatched roof, Lạc Long Quân and Âu Cơ hold hands and smile at their wedding. On the left, a man beats a bronze drum with a star on top and another plays a bamboo mouth organ. On the right, a woman and a child cheer with their arms up, and another woman smiles.", GOLDEN, [
    hills(240, *WARM_HILLS), ground(430, *WARM_GROUND), stilt_house(400, 440, 1.1),
    villager(90, 568, .68, "m1", "low"), bronze_drum(90, 584, .82), villager(200, 576, .68, "m2", "khen", held="khen"),
    llq(340, 580, .68, arms="reach", mood="big"), auco(460, 580, .68, arms="left", mood="big"),
    villager(580, 580, .68, "w2", "up", "big"), kid(660, 588, .68, 5, "up", "big"), villager(745, 582, .68, "w3", "hold", "big", flip=True),
    sparkles([(280, 300, .7), (520, 300, .7), (400, 250, .9)], "#F08FB0")])

# ---- Part 4: one hundred eggs
svg(25, "A big surprise: a bọc!", "Paper-cut scene in front of the big stilt house: on a mat of green banana leaves rests a large, soft, pearly pink bundle — the bọc — glowing softly. Âu Cơ stands beside it with her arms open, delighted, and Lạc Long Quân stands on the other side, amazed, his mouth a little O.", DAY, [
    hills(230), ground(420), stilt_house(400, 420, .9), banana_mat(450, 574, .7), boc(450, 566, .62),
    auco(240, 576, .72, arms="open", mood="big"), llq(660, 576, .72, arms="open", mood="oh")])

svg(26, "Seven days of waiting", "Paper-cut scene: seven little golden suns make an arch across the sky, one for each day of waiting. Below, the soft pearly bọc rests on its banana-leaf mat, glowing. Âu Cơ and Lạc Long Quân stand on either side, watching it calmly and patiently.", GOLDEN, [
    *[sun(120 + i * 93.3, 150 - 70 * (1 - ((i - 3) / 3) ** 2), 18) for i in range(7)],
    hills(280, *WARM_HILLS), ground(440, *WARM_GROUND), banana_mat(400, 560, .85), boc(400, 552, .8),
    auco(150, 578, .68, arms="hold", mood="calm"), llq(650, 578, .68, arms="hip", mood="calm")])

svg(27, "One hundred eggs!", "Paper-cut scene: the pearly bọc has opened its soft sides like petals, and inside is a big round heap of exactly one hundred cream-white eggs, glowing. On the left, Âu Cơ throws her arms up in delight; on the right, Lạc Long Quân throws his arms up too, amazed.", GOLDEN, [
    hills(280, *WARM_HILLS), ground(440, *WARM_GROUND), banana_mat(400, 576, 1), boc(400, 568, 1, opened=True),
    egg_pile(400, 560), auco(100, 584, .62, arms="up", mood="big"), llq(700, 584, .62, arms="up", mood="oh"),
    sparkles([(220, 300, .8), (580, 300, .8), (400, 240, 1)])])

svg(28, "Crack! Crack! Crack!", "Paper-cut scene: eggs are cracking open everywhere. In front, a row of happy babies with little black topknots and bright little tunics pop out of their broken egg shells with their arms up, while behind them, on the open bọc, more eggs are cracking.", GOLDEN, [
    ground(400, *WARM_GROUND), boc(400, 470, .8, opened=True),
    egg_pile(400, 464, (13, 12, 10, 8, 5), 25, 19, ((0, 2), (0, 7), (0, 11), (1, 4), (1, 9), (2, 1), (2, 6), (3, 3), (4, 2))),
    f'<g filter="url(#p)">{"".join(baby(110 + i * 72.5, 585 - (i % 2) * 18, 1.25, i) for i in range(9))}</g>',
    sparkles([(70, 480, .8), (730, 480, .8)], "#fff"),
    sparkles([(150, 420, .6), (650, 420, .6), (400, 300, .7)])])

svg(29, "One hundred children", "Paper-cut scene in front of the big stilt house: a big crowd of exactly one hundred children, all with little black topknots and bright tunics in red, yellow, blue, green, purple, pink, teal and orange, stand in rows from the front to the back, many of them waving. Âu Cơ on the left and Lạc Long Quân on the right smile proudly.", DAY, [
    hills(200), ground(330), stilt_house(400, 340, .7),
    crowd(100, 160, 640, 380, 588, 10, .52, .95), auco(80, 588, .72, arms="open", mood="big"), llq(720, 588, .72, arms="open", mood="big")])

svg(30, "A hundred breakfasts", "Paper-cut scene in warm morning light: Âu Cơ ladles rice from a big bronze pot, while a line of children holds out their bowls, smiling. Lạc Long Quân carries a stack of bowls on the right. Behind them, eight more children stand eating from their bowls.", GOLDEN, [
    hills(250, *WARM_HILLS), ground(420, *WARM_GROUND),
    *[kid(x, 466, .5, i + 2, "bowl", "big") for i, x in enumerate((52, 116, 268, 330, 392, 454, 516, 578))],
    auco(200, 576, .7, arms="ladle"), big_pot(310, 584, .8), kid(420, 586, .7, 0, "bowl", "big"), kid(490, 588, .7, 3, "bowl"),
    kid(560, 590, .7, 5, "bowl", "big"), llq(680, 584, .7, arms="low"),
    "".join(f'<path d="M656 {530 - j * 12} Q680 {546 - j * 12} 704 {530 - j * 12}Z" fill="{BRONZE_L}" stroke="{BRONZE_D}" stroke-width="1.4"/>' for j in range(4)),
    stroke("M249 492 L296 520", WOOD_D, 5) + f'<ellipse cx="300" cy="522" rx="10" ry="6" fill="{WOOD_D}"/>'])

# ---- Part 5: the mountain and the sea
svg(31, "Missing the sea", "Paper-cut scene at dusk on a quiet beach: Lạc Long Quân stands alone on the sand, facing us with a small, wistful smile and glancing sideways toward the sea. Out on the sparkling water a fish leaps, and a crescent moon rises in the purple sky.", DUSK, [
    moon(640, 100, 28, "#566A9E"), stars([(120, 60, 1), (300, 90, .8), (480, 50, .9), (720, 180, .7)]), sea(320), fishy(600, 360, .8, "#F2B53A"),
    stroke("M560 380 q30 -40 70 -16", "#fff", 3), stroke("M420 350 h40 M500 420 h60 M680 400 h40", "#FFF3B0", 3),
    beach(460), llq(260, 576, .78, mood="wistful", look=3)])

svg(32, "Bố ơi! Come back to us!", "Paper-cut scene at dusk on the shore: Âu Cơ and four of the children cup their hands beside their open, smiling mouths and call out across the sea. Out in the waves, the long jade-green dragon is rising out of the water, heading back toward them.", DUSK, [
    moon(120, 90, 24, "#4A5E94"), sea(310), dragon(640, 300, .46, rot=52, amp=22, flip=True), front_waves(370, 380, 800),
    beach(470), auco(150, 580, .66, arms="call", mood="call"), kid(250, 586, .66, 0, "call", "call"), kid(320, 588, .66, 3, "call", "call"),
    kid(390, 586, .66, 5, "call", "call"), kid(460, 590, .66, 2, "call", "call")])

svg(33, "Water and mountain", "Paper-cut scene split in two: on the left is the blue sea with a sandy beach, and on the right rise green mountains. Lạc Long Quân stands on the sea side and Âu Cơ on the mountain side, close together, talking gently and kindly with calm faces.", DAY, [
    *split_bg(), llq(320, 580, .8, arms="low", mood="calm"), auco(480, 580, .8, arms="low", mood="wistful", look=-2)])

svg(34, "Fifty and fifty", "Paper-cut scene split in two, the sea on the left and green mountains on the right: on the beach side, Lạc Long Quân stands beside a group of exactly fifty children; on the mountain side, Âu Cơ stands beside another group of exactly fifty children. Everyone is smiling, and many children wave.", DAY, [
    *split_bg(), crowd(50, 150, 385, 432, 590, 5, .66, 1.0), crowd(50, 415, 650, 432, 590, 5, .66, 1.0, start=50),
    llq(80, 588, .66, arms="open", mood="big"), auco(720, 588, .66, arms="open", mood="big")])

svg(35, "Mountain or sea, we'll help each other!", "Paper-cut scene with the sea on the left and the mountains on the right, joined by a rainbow across the sky. Lạc Long Quân and Âu Cơ hold hands in the middle, smiling, with four children around them throwing their arms up. High in the sky on the mountain side flies a white egret.", DAY, [
    *split_bg(), rainbow(60, 740, 330, 230), crane(650, 150, .55, flip=True),
    kid(160, 588, .74, 1, "up", "big"), kid(240, 592, .74, 4, "up", "big"), llq(345, 584, .74, arms="reach", mood="big"),
    auco(455, 584, .74, arms="left", mood="big"), kid(560, 592, .74, 2, "up", "big"), kid(640, 588, .74, 6, "up", "big")])

svg(36, "Waving and waving", "Paper-cut scene with the sea on the left and the mountains on the right: two lines of children, waving, walk away from the middle, two by two. On the left, fifty children walk down to the beach behind Lạc Long Quân, who is small in the distance at the water's edge; on the right, fifty children climb a path up the green mountain behind Âu Cơ, small near the top.", DAY, [
    *split_bg(), stroke("M380 600 Q300 540 220 500 Q150 466 90 440", "#F6E6BC", 30), stroke("M420 600 Q520 540 580 480 Q630 420 690 350", "#CFE6B0", 26),
    along(50, [(370, 596), (300, 548), (220, 506), (150, 470), (110, 452)], 1.0, .48),
    along(50, [(430, 596), (510, 540), (575, 482), (630, 420), (675, 372)], 1.0, .48, start=50),
    f'<ellipse cx="86" cy="446" rx="70" ry="16" fill="{SAND}"/>', llq(78, 444, .21, arms="wave"), auco(696, 360, .21, arms="wave")])

# ---- Part 6: children of the Dragon, grandchildren of the Fairy
svg(37, "The first Hùng King", "Paper-cut scene in the land of Văn Lang: golden rice fields, stilt houses with saddle-shaped roofs, and green hills. In the middle stands the eldest son, now a grown-up king, in a gold tunic and a tall feather crown of white fairy feathers and teal dragon feathers, smiling with his arms open. Beside him Âu Cơ smiles proudly. A bronze drum stands nearby, and a villager and a child cheer.", DAY, [
    sun(660, 80, 34), hills(220), ground(400),
    "".join(rice_tuft(a, b, .9, True) for b in (440, 470) for a in range(20, 800, 60)),
    stilt_house(130, 440, .62), stilt_house(680, 436, .6), auco(250, 580, .76, arms="hip", mood="proud"), king(400, 580, .76),
    bronze_drum(530, 590, .76), villager(640, 584, .76, "m1", "up", "big"), kid(740, 590, .76, 3, "up", "big")])

svg(38, "Đồng bào", "Paper-cut scene in golden light over green hills: a long line of grown-ups and children hold hands across the page, smiling, with a soft pearly glow behind them shaped like a big bundle, as if they all came from the same bọc.", GOLDEN, [
    hills(260, *WARM_HILLS), ground(450, *WARM_GROUND),
    f'<path d="M110 600 Q60 380 250 300 Q400 250 550 300 Q740 380 690 600Z" fill="{BOC}" opacity=".6"/>', stroke("M190 380 Q240 312 340 292", BOC_L, 10),
    *[(villager(204 + i * 49, 575, .56, ("m1", "w1", "m2", "w3", "m3")[i // 2], "chain", "big") if i % 2 == 0
       else kid(204 + i * 49, 580, .56, i, "chain", "big")) for i in range(9)]])

svg(39, "Dragon from the sea! Fairy from the mountains!", "Paper-cut scene: on the left, the jade-green dragon rises from the blue sea; on the right, on a green mountain top, Âu Cơ waves, with a white egret flying beside her. Between them, under a golden star-sun, lie rice fields and a little village of stilt houses.", DAY, [
    sun(400, 90, 40), sea(330), dragon(170, 318, .45, rot=-30, amp=24), front_waves(400, 0, 240),
    peaks_right(470), auco(660, 476, .55, arms="wave"), crane(730, 160, .4, flip=True),
    f'<path d="M200 600 Q236 470 330 444 Q430 424 560 456 L600 600Z" fill="{SAND}" filter="url(#p)"/>',
    f'<path d="M250 600 Q280 486 350 464 Q440 446 560 470 L590 600Z" fill="{GRASS}"/>',
    "".join(rice_tuft(a, b, .7, True) for b in (500, 540, 580) for a in range(340, 520, 40)), stilt_house(420, 470, .32)])

svg(40, "Con Rồng cháu Tiên", "Paper-cut scene in warm golden light: a happy little child with a black topknot and a bright red tunic stands on a green hill with both arms up, laughing. On the left the sea shines, with the jade-green dragon flying above it; on the right rise the green mountains, with a white egret flying above them, and a golden star-sun shines in the middle.", GOLDEN, [
    sun(400, 96, 40), sea(360), peaks_right(420), dragon(160, 190, .34, amp=20), crane(650, 150, .55, flip=True),
    f'<path filter="url(#p)" d="M120 600 Q260 450 400 440 Q560 450 700 600Z" fill="{GRASS}"/>',
    flowers([(280, 540, 1), (520, 540, 1), (360, 580, .9), (460, 586, .9)]), kid(400, 576, 1.15, 0, "up", "big")])
