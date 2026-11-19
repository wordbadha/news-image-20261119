#!/usr/bin/env python3
"""Draw "THE WORLD TODAY" - a one-image newspaper front page summing up
Thursday, 19 November 2026. Pure Pillow, no network, fully deterministic:
the same bytes come out of every run.

Usage: python3 build/gen_image.py <output-dir>
Writes <output-dir>/entry.png (1024x1024, < 1 MiB).
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)   # warm newsprint
INK = (22, 22, 22)        # near-black
RED = (178, 34, 34)       # brick red for kickers and rules
GREY = (90, 86, 78)       # secondary text
FAINT = (210, 204, 190)   # card separators

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def para(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    """Draw wrapped paragraph; returns y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


LEAD = {
    "kicker": "APEC SUMMIT  •  SHENZHEN, CHINA",
    "headline": "Trump, Xi and Putin meet in Shenzhen",
    "body": (
        "The three leaders sit down together at the APEC summit in a "
        "first-of-its-kind trilateral, with trade, nuclear talks and the "
        "war in Ukraine on the table."
    ),
}

CARDS = [
    ("THE HAGUE", "ICJ to rule on Rohingya genocide case",
     "The world court delivers its judgment on Myanmar — a ruling with "
     "sweeping stakes for international law."),
    ("MARKETS", "Anthropic raises $81.3bn in biggest IPO ever",
     "The AI lab's listing tops every debut in history as investors pile "
     "into artificial intelligence."),
    ("WASHINGTON", "Jeffries set to be first Black House Speaker",
     "Democrats nominate Hakeem Jeffries to lead the House — a first for "
     "an African-American."),
    ("BRUSSELS", "EU approves Indonesia trade deal",
     "The pact cuts tariffs and counters US trade pressure, with provisional "
     "application set to begin soon."),
    ("SPACE", "Voyager 1, one light-day from home",
     "Fifty years after launch, NASA's farthest probe sets a distance "
     "record no craft has reached."),
    ("GAZA", "Four nations press Israel over Gaza aid",
     "Australia, Canada, Italy and the UK call for full humanitarian access "
     "as floods worsen the crisis."),
]

ALSO = ("Also today:  Pew projects Islam to become the world's largest faith "
        "by 2035  •  South Korea's Suneung exam held under AI-cheating curbs")


def draw_masthead(draw):
    """Title, dateline and double rule."""
    title = "THE WORLD TODAY"
    f = SERIF_B(66)
    tw = draw.textlength(title, font=f)
    draw.text(((W - tw) / 2, 34), title, font=f, fill=INK)
    date = "T H U R S D A Y ,  1 9  N O V E M B E R  2 0 2 6"
    df = SANS_B(19)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 116), date, font=df, fill=GREY)
    draw.line([(48, 148), (976, 148)], fill=INK, width=3)
    draw.line([(48, 154), (976, 154)], fill=INK, width=1)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: outline, equator, two meridians, three summit dots."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r, cy - r // 3, cx + r, cy + r // 3],
                 outline=GREY, width=2)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
                 outline=GREY, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
             fill=GREY, width=2)
    spots = [("Shenzhen", cx + 52, cy - 58),
             ("Washington", cx - 78, cy - 12),
             ("Moscow", cx + 8, cy - 84)]
    sf = SANS_B(15)
    for name, sx, sy in spots:
        draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=RED)
        draw.text((sx + 10, sy - 8), name, font=sf, fill=INK)
    cap = SANS(14)
    ct = "Three capitals, one table"
    draw.text((cx - draw.textlength(ct, font=cap) / 2, cy + r + 10),
              ct, font=cap, fill=GREY)


def draw_lead(draw):
    """Lead story: kicker, headline, body on the left; globe on the right."""
    x, y = 48, 172
    draw.text((x, y), LEAD["kicker"], font=SANS_B(19), fill=RED)
    y = para(draw, x, y + 30, LEAD["headline"], SERIF_B(42), 580, 50,
             max_lines=3)
    para(draw, x, y + 8, LEAD["body"], SANS(21), 580, 28, color=GREY)
    draw_globe(draw, 818, 292, 108)


def draw_cards(draw):
    """Six story cards in a 2 x 3 grid."""
    cw, ch, gx, gy = 452, 148, 20, 14
    x0, y0 = 48, 458
    for i, (kicker, head, body) in enumerate(CARDS):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        draw.text((x, y), kicker, font=SANS_B(16), fill=RED)
        y = para(draw, x, y + 24, head, SERIF_B(23), cw, 29, max_lines=2)
        para(draw, x, y + 4, body, SANS(17), cw, 22, color=GREY,
             max_lines=2)
        if i % 2 == 0:
            draw.line([(x + cw + 10, y0 + (i // 2) * (ch + gy) + 4),
                       (x + cw + 10, y0 + (i // 2) * (ch + gy) + ch - 8)],
                      fill=FAINT, width=1)


def draw_footer(draw):
    draw.line([(48, 922), (976, 922)], fill=INK, width=1)
    af = SANS(16)
    aw = draw.textlength(ALSO, font=af)
    if aw <= 928:
        draw.text((48, 934), ALSO, font=af, fill=INK)
    else:
        lines = wrap(draw, ALSO, af, 928)
        yy = 934
        for line in lines:
            draw.text((48, yy), line, font=af, fill=INK)
            yy += 20
    foot = "THE WORLD TODAY  —  one image, the whole day."
    ff = SANS_B(15)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 984), foot, font=ff, fill=GREY)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw.line([(48, 440), (976, 440)], fill=INK, width=2)
    draw_cards(draw)
    draw_footer(draw)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()
