#!/usr/bin/env python3
"""Generate entry.png: a 1024x1024 newspaper poster summing up the world news
of Tuesday 17 November 2026. All facts come from the researched brief; nothing
is invented. Drawn with PIL shapes only — no photos, no copied artwork.

Deterministic: no randomness, no timestamps, fixed fonts.
Usage: python3 tools/make-image.py  (writes entry.png next to the repo root)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)      # off-white newsprint
PANEL = (255, 253, 247)      # slightly lighter panel
INK = (20, 20, 20)
RED = (185, 28, 28)
BLUE = (30, 58, 95)
WATER = (47, 109, 163)
STEEL = (58, 58, 58)
GREY = (154, 163, 168)
SMOKE = (120, 128, 134)
ORANGE = (232, 89, 12)
GOLD = (245, 159, 0)
TAN = (196, 164, 120)
TAN_DARK = (170, 140, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, text, max_w, start, path=BOLD, minimum=12):
    """Largest bold size (<= start) at which text fits max_w."""
    size = start
    while size > minimum and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return size


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r_outer, r_inner, points, fill, outline=None):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill, outline=outline)


def smoke(draw, puffs, fill=SMOKE):
    for (x, y, r) in puffs:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)


def waves(draw, x0, x1, y, color=(255, 255, 255), width=2):
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, y + 3 * math.sin((x - x0) / 14.0)))
        x += 4
    draw.line(pts, fill=color, width=width)


# ---------------------------------------------------------------- pictograms

def draw_bridge(draw, x0, y0, w, h):
    """Collapsing bridge over water: two deck segments, a gap, a falling
    section, smoke and flame."""
    water_top = y0 + h - 42
    deck_y = y0 + 68
    # water
    draw.rectangle((x0, water_top, x0 + w, y0 + h), fill=WATER)
    waves(draw, x0 + 6, x0 + w - 6, water_top + 12)
    waves(draw, x0 + 6, x0 + w - 6, water_top + 28)
    # pillars
    for px in (x0 + 32, x0 + 96, x0 + 212, x0 + 276):
        draw.rectangle((px, deck_y + 14, px + 10, water_top), fill=STEEL)
    # deck segments with a gap in the middle
    draw.rectangle((x0, deck_y, x0 + 132, deck_y + 14), fill=STEEL)
    draw.rectangle((x0 + 180, deck_y, x0 + w, deck_y + 14), fill=STEEL)
    # falling middle section, tilted into the water
    draw.polygon([(x0 + 136, deck_y + 2), (x0 + 178, deck_y + 22),
                  (x0 + 172, deck_y + 32), (x0 + 132, deck_y + 12)],
                 fill=(107, 114, 128))
    # smoke above the gap
    smoke(draw, [(x0 + 152, y0 + 38, 16), (x0 + 168, y0 + 22, 18),
                 (x0 + 136, y0 + 26, 12), (x0 + 182, y0 + 40, 13)])
    # flame at the gap
    star(draw, x0 + 156, deck_y - 6, 16, 7, 8, ORANGE, outline=RED)


def draw_explosion(draw, x0, y0, w, h):
    """Blast over a military base silhouette."""
    draw.rectangle((x0 + 8, y0 + h - 24, x0 + w - 8, y0 + h), fill=STEEL)
    draw.rectangle((x0 + 36, y0 + h - 40, x0 + 56, y0 + h - 24), fill=STEEL)
    smoke(draw, [(x0 + 30, y0 + 18, 10), (x0 + 62, y0 + 12, 12),
                 (x0 + 46, y0 + 8, 9)], fill=GREY)
    star(draw, x0 + w // 2, y0 + 58, 34, 14, 10, ORANGE, outline=RED)
    star(draw, x0 + w // 2, y0 + 58, 16, 7, 8, GOLD)


def draw_tanker(draw, x0, y0, w, h):
    """Oil tanker on the water, pipeline with a break above, a mine below."""
    # pipeline with a break and a flame
    draw.rectangle((x0 + 2, y0 + 18, x0 + w - 2, y0 + 28), fill=(90, 90, 90))
    draw.rectangle((x0 + 40, y0 + 18, x0 + 52, y0 + 28), fill=PANEL)
    star(draw, x0 + 46, y0 + 12, 11, 5, 8, ORANGE, outline=RED)
    # tanker
    draw.polygon([(x0 + 4, y0 + 68), (x0 + w - 4, y0 + 68),
                  (x0 + w - 12, y0 + 92), (x0 + 12, y0 + 92)], fill=(40, 40, 40))
    draw.rectangle((x0 + 62, y0 + 42, x0 + 80, y0 + 68), fill=STEEL)
    draw.rectangle((x0 + 10, y0 + 52, x0 + 28, y0 + 68), fill=RED)
    draw.rectangle((x0 + 30, y0 + 52, x0 + 48, y0 + 68), fill=BLUE)
    # water + mine
    draw.rectangle((x0, y0 + 96, x0 + w, y0 + h), fill=WATER)
    waves(draw, x0 + 4, x0 + w - 4, y0 + 104)
    draw.ellipse((x0 + 16, y0 + 102, x0 + 26, y0 + 112), fill=INK)
    for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6)):
        draw.line((x0 + 21 + dx, y0 + 107 + dy, x0 + 21, y0 + 107),
                  fill=INK, width=2)


def draw_aid(draw, x0, y0, w, h):
    """Aid boxes with a red cross."""
    draw.rectangle((x0 + 6, y0 + 22, x0 + 42, y0 + 54), fill=TAN, outline=INK, width=2)
    draw.rectangle((x0 + 21, y0 + 27, x0 + 27, y0 + 49), fill=RED)
    draw.rectangle((x0 + 11, y0 + 35, x0 + 37, y0 + 41), fill=RED)
    draw.rectangle((x0 + 36, y0 + 38, x0 + 56, y0 + 54), fill=TAN_DARK,
                   outline=INK, width=2)


def draw_swap(draw, x0, y0, w, h):
    """Two arrows in opposite directions: a prisoner swap."""
    draw.rectangle((x0 + 6, y0 + 16, x0 + 44, y0 + 22), fill=BLUE)
    draw.polygon([(x0 + 44, y0 + 10), (x0 + 56, y0 + 19), (x0 + 44, y0 + 28)],
                 fill=BLUE)
    draw.rectangle((x0 + 16, y0 + 36, x0 + 54, y0 + 42), fill=RED)
    draw.polygon([(x0 + 16, y0 + 30), (x0 + 4, y0 + 39), (x0 + 16, y0 + 48)],
                 fill=RED)


# ------------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle((14, 14, 1010, 1010), outline=INK, width=3)

    # ---- masthead
    title = "THE WORLD IN ONE IMAGE"
    tsize = fit_size(d, title, 940, 62)
    centered(d, 512, 36, title, font(BOLD, tsize))
    d.rectangle((28, 116, 996, 121), fill=RED)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dsize = fit_size(d, date, 940, 42)
    centered(d, 512, 130, date, font(BOLD, dsize))
    d.rectangle((28, 182, 996, 184), fill=INK)

    # ---- hero panel: Kerch Bridge
    d.rectangle((28, 196, 996, 452), fill=PANEL, outline=INK, width=2)
    hero_head = "KERCH BRIDGE PARTLY COLLAPSES"
    hsize = fit_size(d, hero_head, 940, 44)
    centered(d, 512, 208, hero_head, font(BOLD, hsize), fill=RED)
    draw_bridge(d, 44, 262, 316, 178)
    d.text((380, 262), "UKRAINE WAR", font=font(BOLD, 19), fill=BLUE)
    hero_cap = ("Ukraine says a section of the bridge linking Russia to Crimea "
                "collapsed after a weeks-long missile and drone operation. "
                "Zelenskyy hails an 'unprecedented' attack.")
    y = 290
    for line in wrap(d, hero_cap, font(REG, 23), 600):
        d.text((380, y), line, font=font(REG, 23), fill=INK)
        y += 30

    # ---- medium row
    panels = [
        (28, "IRAN STRIKES US TARGETS IN BAHRAIN",
         "Third attack in days on US military targets in Bahrain. "
         "The US had hit Qeshm Island. Trump: Iran will 'pay a huge price' "
         "if it hits US soil.",
         draw_explosion),
        (522, "HOUTHIS HIT SAUDI OIL PIPELINE",
         "Houthis say they launched drones at Saudi Arabia's East-West oil "
         "pipeline. An LPG tanker was attacked in the Strait of Hormuz; "
         "Iran reports more tankers hit by mines.",
         draw_tanker),
    ]
    for (px, head, cap, pic) in panels:
        d.rectangle((px, 466, px + 474, 686), fill=PANEL, outline=INK, width=2)
        hy = 466 + 12
        for line in wrap(d, head, font(BOLD, 28), 446):
            d.text((px + 14, hy), line, font=font(BOLD, 28), fill=BLUE)
            hy += 33
        pic(d, px + 14, 466 + 82, 92, 120)
        cy = 466 + 82
        for line in wrap(d, cap, font(REG, 18), 342):
            d.text((px + 118, cy), line, font=font(REG, 18), fill=INK)
            cy += 22

    # ---- Gaza panel: two items side by side
    d.rectangle((28, 700, 996, 838), fill=PANEL, outline=INK, width=2)
    d.line((512, 712, 512, 826), fill=INK, width=2)
    halves = [
        (28, "GAZA AID CALL",
         "UK, Australia, Canada and Italy urge Israel to open Gaza crossings "
         "for aid. Situation 'catastrophic'.",
         draw_aid),
        (522, "POW EXCHANGE",
         "Zelenskyy announces a large prisoner swap, over 1,000 each side, "
         "after talks in Abu Dhabi.",
         draw_swap),
    ]
    for (hx, head, cap, pic) in halves:
        d.text((hx + 14, 712), head, font=font(BOLD, 24), fill=BLUE)
        pic(d, hx + 14, 744, 60, 60)
        cy = 744
        for line in wrap(d, cap, font(REG, 18), 360):
            d.text((hx + 86, cy), line, font=font(REG, 18), fill=INK)
            cy += 22

    # ---- bottom strip: secondary stories
    d.line((28, 852, 996, 852), fill=INK, width=2)
    d.text((28, 860), "ALSO TODAY", font=font(BOLD, 20), fill=RED)
    items = [
        "Gérard Depardieu pleads guilty to sexual assault, drops appeal",
        "US loses measles elimination status after 26 years, with 5,400+ cases",
        "Mongolian president resigns amid corruption scandal",
        "Japan scrambles fighter jets after Russian aircraft violate its airspace",
        "Trump in Asia ahead of talks with Putin and Xi; Nvidia spy scandal "
        "shadows China AI hopes",
    ]
    y = 884
    for item in items:
        for line in wrap(d, item, font(REG, 19), 940):
            d.rectangle((28, y + 6, 35, y + 13), fill=RED)
            d.text((44, y), line, font=font(REG, 19), fill=INK)
            y += 20

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "..", "entry.png")
    img = build()
    img.save(out_path, format="PNG")
    print("wrote", out_path, img.size, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
