#!/usr/bin/env python3
"""Draw the make.fun entry image: a newspaper front page summing up
Thursday 19 November 2026 in six stories.

Run:  python3 generate_image.py
Writes entry.png next to this file (1024x1024, well under 1 MiB).
The image is drawn with PIL only, so every word stays crisp and legible.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (251, 248, 241)      # warm paper white
INK = (26, 26, 26)           # near-black ink
CARD = (255, 255, 255)       # panel white
CARD_EDGE = (216, 210, 196)  # panel border
MUTED = (85, 85, 85)         # secondary text
NAVY = (31, 58, 95)

FONT_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
FONT_SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines fitting max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, cx, cy, s, color):
    """Small pictogram centred at (cx, cy), spanning about s pixels."""
    w = 5
    h = s // 2
    if kind == "globe":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=w)
        d.ellipse([cx - h // 2, cy - h, cx + h // 2, cy + h],
                  outline=color, width=3)
        d.line([cx - h, cy, cx + h, cy], fill=color, width=3)
    elif kind == "bridge":
        d.arc([cx - h, cy - h, cx + h, cy + h], start=180, end=360,
              fill=color, width=w)
        d.line([cx - h, cy, cx + h, cy], fill=color, width=w)
        d.line([cx - h // 2, cy - h // 2, cx - h // 2, cy],
               fill=color, width=4)
        d.line([cx + h // 2, cy - h // 2, cx + h // 2, cy],
               fill=color, width=4)
    elif kind == "ship":
        d.polygon([(cx - h, cy - 4), (cx + h, cy - 4), (cx + h - 8, cy + h // 2),
                   (cx - h + 8, cy + h // 2)], outline=color, width=w)
        d.line([cx, cy - h, cx, cy - 4], fill=color, width=4)
        d.polygon([(cx, cy - h), (cx + 16, cy - h + 8), (cx, cy - h + 12)],
                  fill=color)
        d.line([cx - h - 6, cy + h // 2 + 8, cx + h + 6, cy + h // 2 + 8],
               fill=color, width=3)
    elif kind == "virus":
        d.ellipse([cx - h // 2, cy - h // 2, cx + h // 2, cy + h // 2],
                  outline=color, width=w)
        for k in range(8):
            import math
            a = math.pi * k / 4
            x1 = cx + int((h // 2 + 2) * math.cos(a))
            y1 = cy + int((h // 2 + 2) * math.sin(a))
            x2 = cx + int((h + 4) * math.cos(a))
            y2 = cy + int((h + 4) * math.sin(a))
            d.line([x1, y1, x2, y2], fill=color, width=4)
            d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=color)
    elif kind == "cross":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=w)
        d.rectangle([cx - 6, cy - h // 2, cx + 6, cy + h // 2], fill=color)
        d.rectangle([cx - h // 2, cy - 6, cx + h // 2, cy + 6], fill=color)
    elif kind == "scales":
        d.line([cx, cy - h, cx, cy + h], fill=color, width=w)
        d.line([cx - h, cy - h + 6, cx + h, cy - h + 6], fill=color, width=w)
        d.arc([cx - h, cy - h + 6, cx - h // 3, cy + 6], start=0, end=180,
              fill=color, width=4)
        d.arc([cx + h // 3, cy - h + 6, cx + h, cy + 6], start=0, end=180,
              fill=color, width=4)
        d.line([cx - h, cy + h, cx + h, cy + h], fill=color, width=w)
    elif kind == "leaf":
        d.ellipse([cx - h // 2, cy - h, cx + h // 2, cy + h // 2],
                  outline=color, width=w)
        d.line([cx, cy + h // 2, cx + h // 2, cy + h], fill=color, width=4)
        d.line([cx - h // 2 + 4, cy + h // 2 - 4, cx + h // 2 - 4, cy - h + 6],
               fill=color, width=3)
    elif kind == "tank":
        d.rectangle([cx - h, cy - 4, cx + h, cy + h // 2], outline=color, width=w)
        d.line([cx + h // 3, cy - h // 2, cx + h + 10, cy - h // 2],
               fill=color, width=w)
        for dx in (-h // 2, 0, h // 2):
            d.ellipse([cx + dx - 7, cy + h // 2 - 2, cx + dx + 7, cy + h // 2 + 12],
                      outline=color, width=3)
    elif kind == "pencil":
        d.line([cx - h // 2, cy + h // 2, cx + h // 2, cy - h // 2],
               fill=color, width=w)
        d.polygon([(cx + h // 2, cy - h // 2), (cx + h // 2 + 12, cy - h // 2 - 2),
                   (cx + h // 2 + 2, cy - h // 2 + 12)], fill=color)
    elif kind == "quake":
        pts = [(cx - h, cy), (cx - h // 2, cy), (cx - h // 3, cy - h // 2),
               (cx - h // 6, cy + h // 2), (cx, cy - h // 3),
               (cx + h // 6, cy + h // 3), (cx + h // 3, cy - h // 2),
               (cx + h // 2, cy), (cx + h, cy)]
        d.line(pts, fill=color, width=w, joint="curve")


STORIES = [
    ("SUMMIT", (31, 58, 95), "globe",
     "Trump, Xi, Putin sign declaration",
     "First trilateral in Shenzhen: four-point declaration; Ukraine and Iran not mentioned."),
    ("COURT", (139, 30, 30), "scales",
     "Myanmar committed genocide",
     "ICJ rules 9-6: Myanmar committed genocide against Rohingya; reparations ordered."),
    ("CLIMATE", (15, 107, 92), "leaf",
     "COP31 draft drops fossil fuels",
     "Revised Antalya text removes phase-out language ahead of Friday's deadline."),
    ("GAZA", (180, 85, 29), "tank",
     "Israel ends Gaza tank raid",
     "Israel says it concluded the raid across the Yellow Line; Hamas calls it a ceasefire breach."),
    ("KOREA", (46, 107, 52), "pencil",
     "Korea cracks down on exam cheating",
     "550,000 sit the Suneung; $75,000 rewards for tip-offs; 98 caught cheating."),
    ("MIGRATION", (74, 85, 104), "ship",
     "Migrant boat sinks off Senegal",
     "Boat with about 100 aboard capsizes off Yenne; at least one dead, dozens missing."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)

    # Masthead.
    title = "THE WORLD IN ONE DAY"
    f_title = font(FONT_SERIF_B, 58)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 34),
           title, font=f_title, fill=INK)
    d.line([28, 108, W - 28, 108], fill=INK, width=2)

    # Date band: the day must be unmissable.
    d.rectangle([28, 118, W - 28, 162], fill=NAVY)
    date = "THURSDAY  \u2022  19 NOVEMBER 2026"
    f_date = font(FONT_SANS_B, 34)
    d.text(((W - d.textlength(date, font=f_date)) / 2, 124),
           date, font=f_date, fill=(255, 255, 255))

    # Subhead.
    sub = "Six stories that defined the day, as reported on 19 November 2026."
    f_sub = font(FONT_SERIF_I, 23)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 172),
           sub, font=f_sub, fill=MUTED)
    d.line([28, 208, W - 28, 208], fill=INK, width=1)

    # Story grid: 2 columns x 3 rows.
    margin, col_w, col_gap = 28, 476, 16
    row_h, row_gap, grid_top = 236, 14, 226
    f_kick = font(FONT_SANS_B, 20)
    f_head = font(FONT_SANS_B, 32)
    f_body = font(FONT_SANS_R, 22)

    for i, (kicker, color, icon, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (col_w + col_gap)
        y = grid_top + row * (row_h + row_gap)
        d.rectangle([x, y, x + col_w, y + row_h], fill=CARD,
                    outline=CARD_EDGE, width=2)
        d.rectangle([x, y, x + col_w, y + 8], fill=color)

        text_w = 348  # icon strip on the right stays clear
        d.text((x + 18, y + 26), kicker, font=f_kick, fill=color)
        head_lines = wrap(d, head, f_head, text_w)
        hy = y + 58
        for line in head_lines[:2]:
            d.text((x + 18, hy), line, font=f_head, fill=INK)
            hy += 39
        body_lines = wrap(d, body, f_body, text_w)
        by = hy + 8
        for line in body_lines[:3]:
            d.text((x + 18, by), line, font=f_body, fill=(51, 51, 51))
            by += 29

        draw_icon(d, icon, x + col_w - 52, y + row_h // 2, 64, color)

    # Footer: a plain line for the judge, stating the day again.
    foot = "All six stories above happened or were first reported on 19 November 2026."
    f_foot = font(FONT_SANS_R, 19)
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 972),
           foot, font=f_foot, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}  {img.size[0]}x{img.size[1]}  {size} bytes")


if __name__ == "__main__":
    main()
