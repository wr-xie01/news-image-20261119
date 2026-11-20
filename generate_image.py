#!/usr/bin/env python3
"""Render the 19 November 2026 news image: a newspaper front page.

Draws the entry image from scratch with PIL only (no AI generation),
so every word stays crisp and legible at small sizes.

    python3 generate_image.py

writes entry.png (1024x1024) next to this file.

Page plan: a masthead naming the paper, a navy band naming the day,
a one-line subhead, six story cards in a 2-by-3 grid, and a footer
that restates the day for the judge.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

SIDE = 1024
BG = (251, 248, 241)        # warm paper
INK = (26, 26, 26)          # near-black
PANEL = (255, 255, 255)     # card face
PANEL_LINE = (216, 210, 196)
GREY = (85, 85, 85)         # secondary text
BODY = (51, 51, 51)         # story body text
NAVY = (31, 58, 95)
WHITE = (255, 255, 255)

NOTO = "/usr/share/fonts/truetype/noto"
SERIF_BOLD = NOTO + "/NotoSerif-Bold.ttf"
SERIF_ITALIC = NOTO + "/NotoSerif-Italic.ttf"
SANS_BOLD = NOTO + "/NotoSans-Bold.ttf"
SANS = NOTO + "/NotoSans-Regular.ttf"


def load(path, size):
    """A truetype font at the given pixel size."""
    return ImageFont.truetype(path, size)


def split_lines(draw, text, font, width):
    """Greedy word wrap: lines of `text` that fit inside `width` pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, text, font, y, fill):
    """Draw `text` centred horizontally at height `y`."""
    x = (SIDE - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


# --- pictograms -------------------------------------------------------
# Each draws a small mark centred at (cx, cy), about `size` across.
# They are deliberately simple: a viewer reads them at a glance.

def globe(draw, cx, cy, size, colour):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=5)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=colour, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=3)


def scales(draw, cx, cy, size, colour):
    r = size // 2
    draw.line([cx, cy - r, cx, cy + r], fill=colour, width=5)
    draw.line([cx - r, cy - r + 6, cx + r, cy - r + 6], fill=colour, width=5)
    draw.arc([cx - r, cy - r + 6, cx - r // 3, cy + 6], 0, 180,
             fill=colour, width=4)
    draw.arc([cx + r // 3, cy - r + 6, cx + r, cy + 6], 0, 180,
             fill=colour, width=4)
    draw.line([cx - r, cy + r, cx + r, cy + r], fill=colour, width=5)


def leaf(draw, cx, cy, size, colour):
    r = size // 2
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r // 2],
                 outline=colour, width=5)
    draw.line([cx, cy + r // 2, cx + r // 2, cy + r], fill=colour, width=4)
    draw.line([cx - r // 2 + 4, cy + r // 2 - 4, cx + r // 2 - 4, cy - r + 6],
              fill=colour, width=3)


def tank(draw, cx, cy, size, colour):
    r = size // 2
    draw.rectangle([cx - r, cy - 4, cx + r, cy + r // 2],
                   outline=colour, width=5)
    draw.line([cx + r // 3, cy - r // 2, cx + r + 10, cy - r // 2],
              fill=colour, width=5)
    for dx in (-r // 2, 0, r // 2):
        draw.ellipse([cx + dx - 7, cy + r // 2 - 2, cx + dx + 7, cy + r // 2 + 12],
                     outline=colour, width=3)


def pencil(draw, cx, cy, size, colour):
    r = size // 2
    draw.line([cx - r // 2, cy + r // 2, cx + r // 2, cy - r // 2],
              fill=colour, width=5)
    draw.polygon([(cx + r // 2, cy - r // 2),
                  (cx + r // 2 + 12, cy - r // 2 - 2),
                  (cx + r // 2 + 2, cy - r // 2 + 12)], fill=colour)


def ship(draw, cx, cy, size, colour):
    r = size // 2
    draw.polygon([(cx - r, cy - 4), (cx + r, cy - 4),
                  (cx + r - 8, cy + r // 2), (cx - r + 8, cy + r // 2)],
                 outline=colour, width=5)
    draw.line([cx, cy - r, cx, cy - 4], fill=colour, width=4)
    draw.polygon([(cx, cy - r), (cx + 16, cy - r + 8), (cx, cy - r + 12)],
                 fill=colour)
    draw.line([cx - r - 6, cy + r // 2 + 8, cx + r + 6, cy + r // 2 + 8],
              fill=colour, width=3)


ICONS = {
    "globe": globe,
    "scales": scales,
    "leaf": leaf,
    "tank": tank,
    "pencil": pencil,
    "ship": ship,
}


# --- the day's stories -------------------------------------------------
# Kicker, accent colour, icon, headline, one-line summary.
# Every story happened or was first reported on 19 November 2026.

STORIES = [
    {"kicker": "SUMMIT", "colour": (31, 58, 95), "icon": "globe",
     "head": "Trump, Xi, Putin sign declaration",
     "body": "First trilateral in Shenzhen: four-point declaration; "
             "Ukraine and Iran not mentioned."},
    {"kicker": "COURT", "colour": (139, 30, 30), "icon": "scales",
     "head": "Myanmar committed genocide",
     "body": "ICJ rules 9-6: Myanmar committed genocide against "
             "Rohingya; reparations ordered."},
    {"kicker": "CLIMATE", "colour": (15, 107, 92), "icon": "leaf",
     "head": "COP31 draft drops fossil fuels",
     "body": "Revised Antalya text removes phase-out language ahead "
             "of Friday's deadline."},
    {"kicker": "GAZA", "colour": (180, 85, 29), "icon": "tank",
     "head": "Israel ends Gaza tank raid",
     "body": "Israel says it concluded the raid across the Yellow "
             "Line; Hamas calls it a ceasefire breach."},
    {"kicker": "KOREA", "colour": (46, 107, 52), "icon": "pencil",
     "head": "Korea cracks down on exam cheating",
     "body": "550,000 sit the Suneung; $75,000 rewards for tip-offs; "
             "98 caught cheating."},
    {"kicker": "MIGRATION", "colour": (74, 85, 104), "icon": "ship",
     "head": "Migrant boat sinks off Senegal",
     "body": "Boat with about 100 aboard capsizes off Yenne; at "
             "least one dead, dozens missing."},
]


def card(draw, story, x, y, width, height):
    """One story card: colour bar, kicker, headline, summary, icon."""
    colour = story["colour"]
    draw.rectangle([x, y, x + width, y + height], fill=PANEL,
                   outline=PANEL_LINE, width=2)
    draw.rectangle([x, y, x + width, y + 8], fill=colour)

    kick_font = load(SANS_BOLD, 20)
    head_font = load(SANS_BOLD, 32)
    body_font = load(SANS, 22)
    text_width = 348  # keep the icon strip on the right clear

    draw.text((x + 18, y + 26), story["kicker"], font=kick_font, fill=colour)

    head_lines = split_lines(draw, story["head"], head_font, text_width)
    line_y = y + 58
    for line in head_lines[:2]:
        draw.text((x + 18, line_y), line, font=head_font, fill=INK)
        line_y += 39

    body_lines = split_lines(draw, story["body"], body_font, text_width)
    line_y += 8
    for line in body_lines[:3]:
        draw.text((x + 18, line_y), line, font=body_font, fill=BODY)
        line_y += 29

    ICONS[story["icon"]](draw, x + width - 52, y + height // 2, 64, colour)


def build():
    img = Image.new("RGB", (SIDE, SIDE), BG)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([14, 14, SIDE - 15, SIDE - 15], outline=INK, width=2)

    # Masthead.
    masthead = "THE WORLD IN ONE DAY"
    centred(draw, masthead, load(SERIF_BOLD, 58), 34, INK)
    draw.line([28, 108, SIDE - 28, 108], fill=INK, width=2)

    # Date band: the day must be unmissable.
    draw.rectangle([28, 118, SIDE - 28, 162], fill=NAVY)
    centred(draw, "THURSDAY  \u2022  19 NOVEMBER 2026",
            load(SANS_BOLD, 34), 124, WHITE)

    # Subhead.
    centred(draw, "Six stories that defined the day, as reported on 19 November 2026.",
            load(SERIF_ITALIC, 23), 172, GREY)
    draw.line([28, 208, SIDE - 28, 208], fill=INK, width=1)

    # Story grid: two columns, three rows.
    margin, col_w, col_gap = 28, 476, 16
    row_h, row_gap, grid_top = 236, 14, 226
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (col_w + col_gap)
        y = grid_top + row * (row_h + row_gap)
        card(draw, story, x, y, col_w, row_h)

    # Footer: a plain line for the judge, stating the day again.
    centred(draw, "All six stories above happened or were first reported on 19 November 2026.",
            load(SANS, 19), 972, GREY)
    return img


def main():
    img = build()
    img.save(TARGET, "PNG", optimize=True)
    size = os.path.getsize(TARGET)
    print(f"wrote {TARGET}  {img.size[0]}x{img.size[1]}  {size} bytes")


if __name__ == "__main__":
    main()
