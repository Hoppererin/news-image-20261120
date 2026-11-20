#!/usr/bin/env python3
"""Render the news-image-20261120 entry: a 1024x1024 newspaper front page
summing up Friday 20 November 2026 (six verified stories, see RESEARCH.md).

Deterministic: fixed text, fixed geometry, no randomness, no timestamps,
no network. PIL's PNG writer embeds no time chunk, so re-running this
script writes byte-identical entry.png. Run: python3 render.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (246, 241, 231)
NAVY = (20, 33, 61)
NAVY2 = (31, 48, 84)
RED = (185, 28, 28)
GOLD = (217, 164, 65)
INK = (31, 41, 55)
GRAY = (107, 114, 128)
WHITE = (255, 255, 255)
BORDER = (216, 210, 196)
TEAL = (13, 110, 96)
GREEN = (34, 120, 60)
BLUE = (30, 90, 160)
ORANGE = (200, 90, 20)
LIGHT = (200, 205, 215)
WOOD = (217, 160, 102)

FD = "/usr/share/fonts/truetype/dejavu"
F_TITLE = ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 62)
F_DATE = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 30)
F_SUB = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 16)
F_TAG = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 15)
F_HEAD = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 27)
F_BODY = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 19)
F_FOOT = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 14)
F_CAL = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 24)
F_CALSM = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 12)


def star_points(cx, cy, r_out, r_in, rot=-90.0):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons -----
# Each icon draws inside a band (bx, by, bw, bh); cx/cy = band centre.
def icon_flags(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    fw, fh, gap = 64, 42, 34
    x0 = cx - (3 * fw + 2 * gap) // 2
    fy = cy - fh // 2
    for i in range(3):
        fx = x0 + i * (fw + gap)
        # pole
        d.rectangle([fx - 5, fy - 7, fx - 2, fy + fh + 4], fill=NAVY)
        d.ellipse([fx - 7, fy - 11, fx - 1, fy - 5], fill=GOLD)
        if i == 0:  # USA: stripes + canton
            for s in range(7):
                d.rectangle([fx, fy + s * 6, fx + fw, fy + (s + 1) * 6],
                            fill=RED if s % 2 == 0 else WHITE)
            d.rectangle([fx, fy, fx + 26, fy + 18], fill=NAVY2)
            for r in range(2):
                for c in range(3):
                    d.ellipse([fx + 4 + c * 8, fy + 4 + r * 8,
                               fx + 7 + c * 8, fy + 7 + r * 8], fill=WHITE)
        elif i == 1:  # China: red + gold stars
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=RED)
            d.polygon(star_points(fx + 15, fy + 14, 8, 3.4), fill=GOLD)
            for sx, sy in [(38, 8), (45, 14), (45, 22), (38, 28)]:
                d.polygon(star_points(fx + sx, fy + sy, 3.2, 1.4), fill=GOLD)
        else:  # Russia: white / blue / red bands
            d.rectangle([fx, fy, fx + fw, fy + 14], fill=WHITE)
            d.rectangle([fx, fy + 14, fx + fw, fy + 28], fill=BLUE)
            d.rectangle([fx, fy + 28, fx + fw, fy + 42], fill=RED)
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=NAVY, width=1)


def icon_calendar(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    d.rectangle([cx - 40, cy - 28, cx + 40, cy + 28], fill=WHITE, outline=NAVY, width=2)
    d.rectangle([cx - 40, cy - 28, cx + 40, cy - 14], fill=RED)
    d.rectangle([cx - 25, cy - 33, cx - 20, cy - 24], fill=NAVY)
    d.rectangle([cx + 20, cy - 33, cx + 25, cy - 24], fill=NAVY)
    d.text((cx, cy - 27), "NOV 20", font=F_CALSM, fill=WHITE, anchor="mt")
    d.text((cx, cy - 10), "2027", font=F_CAL, fill=NAVY, anchor="mt")


def icon_cyclone(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    scx, scy = cx - 36, cy + 2
    pts = []
    for k in range(91):
        t = k / 90.0
        th = t * 4.6 * math.pi
        r = 3 + 29 * t
        pts.append((scx + r * math.cos(th), scy + r * math.sin(th)))
    d.line(pts, fill=TEAL, width=5, joint="curve")
    d.ellipse([scx - 4, scy - 4, scx + 4, scy + 4], fill=PAPER)
    for x0, y0 in [(50, -16), (64, -4), (50, 10)]:
        d.line([cx + x0, cy + y0, cx + x0 - 6, cy + y0 + 14], fill=BLUE, width=4)


def icon_cricket(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    # stumps + bails
    for i in range(3):
        sx = cx - 82 + i * 10
        d.rectangle([sx, cy - 8, sx + 7, cy + 28], fill=GOLD, outline=(150, 110, 40))
    d.rectangle([cx - 82, cy - 12, cx - 73, cy - 9], fill=GOLD)
    d.rectangle([cx - 70, cy - 12, cx - 61, cy - 9], fill=GOLD)
    # bat: vertical blade + handle
    d.rectangle([cx + 12, cy - 32, cx + 18, cy - 12], fill=NAVY)
    d.polygon([(cx + 4, cy - 12), (cx + 26, cy - 12), (cx + 26, cy + 20),
               (cx + 4, cy + 20)], fill=WOOD, outline=(150, 100, 50))
    # ball + seam
    d.ellipse([cx + 40, cy - 6, cx + 66, cy + 20], fill=RED)
    d.arc([cx + 40, cy - 6, cx + 66, cy + 20], start=200, end=340, fill=WHITE, width=2)


def icon_eu_uk(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    # EU flag
    ex, ey = cx - 118, cy - 21
    d.rectangle([ex, ey, ex + 64, ey + 42], fill=BLUE)
    for k in range(8):
        a = math.radians(k * 45)
        d.ellipse([ex + 32 + 13 * math.cos(a) - 2.5, ey + 21 + 13 * math.sin(a) - 2.5,
                   ex + 32 + 13 * math.cos(a) + 2.5, ey + 21 + 13 * math.sin(a) + 2.5],
                  fill=GOLD)
    # UK flag (simplified Union Jack)
    ux, uy = cx + 54, cy - 21
    d.rectangle([ux, uy, ux + 64, uy + 42], fill=BLUE)
    d.line([ux, uy, ux + 64, uy + 42], fill=WHITE, width=7)
    d.line([ux + 64, uy, ux, uy + 42], fill=WHITE, width=7)
    d.rectangle([ux + 27, uy, ux + 37, uy + 42], fill=WHITE)
    d.rectangle([ux, uy + 16, ux + 64, uy + 26], fill=WHITE)
    d.rectangle([ux + 29, uy, ux + 35, uy + 42], fill=RED)
    d.rectangle([ux, uy + 18, ux + 64, uy + 24], fill=RED)


def icon_dialogue(d, bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + bh // 2
    # Japan bubble (white, red sun) + China bubble (red, gold star)
    d.rounded_rectangle([cx - 118, cy - 26, cx - 28, cy + 18], radius=10,
                        fill=WHITE, outline=NAVY, width=2)
    d.polygon([(cx - 102, cy + 17), (cx - 88, cy + 17), (cx - 104, cy + 30)],
              fill=WHITE, outline=NAVY)
    d.ellipse([cx - 82, cy - 13, cx - 64, cy + 5], fill=RED)
    d.rounded_rectangle([cx + 28, cy - 26, cx + 118, cy + 18], radius=10, fill=RED)
    d.polygon([(cx + 88, cy + 17), (cx + 102, cy + 17), (cx + 104, cy + 30)], fill=RED)
    d.polygon(star_points(cx + 73, cy - 4, 10, 4.2), fill=GOLD)


# ------------------------------------------------------------------ data ----
STORIES = [
    dict(tag="SUMMIT \u2014 SHENZHEN", color=NAVY2, tint=(233, 236, 244),
         headline="TRUMP, XI AND PUTIN MEET IN SHENZHEN",
         body="Historic three-way talks at the APEC summit; Ukraine tops the agenda.",
         icon=icon_flags),
    dict(tag="US \u2014 IRAN", color=RED, tint=(247, 231, 231),
         headline="TRUMP PUTS IRAN WAR DECISION OFF TO 2027",
         body="The US president says there is no rush \u2014 a decision on war can wait until next year.",
         icon=icon_calendar),
    dict(tag="WEATHER \u2014 INDIA", color=TEAL, tint=(224, 240, 236),
         headline="CYCLONE AKVAN SLAMS INTO ODISHA",
         body="80,000 evacuated as heavy rain begins; 1,000 tourists stranded off Bangladesh.",
         icon=icon_cyclone),
    dict(tag="SPORT \u2014 CRICKET", color=GREEN, tint=(226, 242, 230),
         headline="NICHOLLS 113* SAVES NEW ZEALAND",
         body="New Zealand 243 for 5 at stumps on day one of the first Test in Wellington.",
         icon=icon_cricket),
    dict(tag="EUROPE", color=BLUE, tint=(227, 237, 247),
         headline="EU AND UK SUMMIT IN BRUSSELS",
         body="Burnham, Costa and von der Leyen talk trade, security and migration.",
         icon=icon_eu_uk),
    dict(tag="ASIA \u2014 DIPLOMACY", color=ORANGE, tint=(253, 235, 208),
         headline="TAKAICHI SEEKS DIALOGUE WITH CHINA",
         body="Japan's prime minister calls for talks to ease tensions with Beijing.",
         icon=icon_dialogue),
]


def draw_card(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BORDER, width=2)
    d.rectangle([x, y, x + w, y + 6], fill=s["color"])
    d.rectangle([x + 2, y + 6, x + w - 2, y + 74], fill=s["tint"])
    s["icon"](d, x + 2, y + 6, w - 4, 68)
    d.text((x + 16, y + 82), s["tag"], font=F_TAG, fill=s["color"], anchor="lt")
    head = wrap(d, s["headline"], F_HEAD, w - 32)
    assert len(head) <= 2, f"headline too long: {s['headline']} -> {head}"
    hy = y + 102
    for ln in head:
        d.text((x + 16, hy), ln, font=F_HEAD, fill=INK, anchor="lt")
        hy += 33
    body = wrap(d, s["body"], F_BODY, w - 32)
    assert len(body) <= 3, f"body too long: {s['body']} -> {body}"
    by = y + 172
    for ln in body:
        d.text((x + 16, by), ln, font=F_BODY, fill=(70, 78, 90), anchor="lt")
        by += 24


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([24, 10, W - 24, 13], fill=GOLD)
    d.text((W // 2, 26), "THE WORLD TODAY", font=F_TITLE, fill=WHITE, anchor="mt")
    d.text((W // 2, 96), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=GOLD, anchor="mt")
    d.text((W // 2, 134), "SIX STORIES THAT DEFINED THE DAY", font=F_SUB,
           fill=LIGHT, anchor="mt")
    d.rectangle([24, 155, W - 24, 158], fill=GOLD)
    # grid: 2 cols x 3 rows
    margin, gap, card_w, card_h, top = 24, 16, 480, 250, 184
    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(d, s, margin + col * (card_w + gap), top + row * (card_h + gap),
                  card_w, card_h)
    # footer
    d.text((W // 2, 978), "SOURCES: REUTERS \u00b7 ASSOCIATED PRESS \u00b7 TIMES OF INDIA \u00b7 JAGRAN \u00b7 NDTV",
           font=F_FOOT, fill=GRAY, anchor="mt")
    return img


if __name__ == "__main__":
    build().save(OUT, format="PNG")
    print(f"wrote {OUT}")
