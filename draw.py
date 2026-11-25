#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Tuesday 24 November 2026. Original illustration, drawn with Pillow shapes
only -- no photographs, no copied artwork. Run: python3 draw.py"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 38, 63)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
GREY = (110, 108, 100)
CARD = (255, 255, 255)
RULE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def scales(draw, cx, cy, s, col):
    """Scales of justice pictogram, centred at (cx, cy), size s."""
    draw.line([(cx - s, cy - s * 0.2), (cx + s, cy - s * 0.2)], fill=col, width=5)
    draw.line([(cx, cy - s * 0.7), (cx, cy + s * 0.5)], fill=col, width=5)
    draw.line([(cx - s, cy - s * 0.2), (cx - s, cy + s * 0.25)], fill=col, width=4)
    draw.line([(cx + s, cy - s * 0.2), (cx + s, cy + s * 0.25)], fill=col, width=4)
    draw.arc([cx - s - s * 0.35, cy + s * 0.05, cx - s + s * 0.35, cy + s * 0.55],
             0, 180, fill=col, width=4)
    draw.arc([cx + s - s * 0.35, cy + s * 0.05, cx + s + s * 0.35, cy + s * 0.55],
             0, 180, fill=col, width=4)
    draw.line([(cx - s * 0.35, cy - s * 0.7), (cx + s * 0.35, cy - s * 0.7)],
             fill=col, width=5)


def tanker(draw, cx, cy, s, col):
    """Oil tanker on waves with a flame above it."""
    draw.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 0.8, cy + s * 0.45),
                  (cx - s * 0.8, cy + s * 0.45)], fill=col)
    draw.rectangle([cx - s * 0.55, cy - s * 0.55, cx - s * 0.15, cy - s * 0.05],
                   fill=col)
    draw.rectangle([cx + s * 0.1, cy - s * 0.4, cx + s * 0.45, cy - s * 0.05],
                   fill=col)
    draw.polygon([(cx + s * 0.1, cy - s * 1.05), (cx + s * 0.3, cy - s * 0.55),
                  (cx + s * 0.5, cy - s * 1.05)], fill=(224, 122, 26))
    for i, wx in enumerate([-1.1, -0.35, 0.4, 1.05]):
        draw.arc([cx + wx * s - s * 0.3, cy + s * 0.6, cx + wx * s + s * 0.3,
                  cy + s * 1.0], 180, 360, fill=(70, 130, 160), width=4)


def skyline(draw, cx, cy, s, col):
    """City towers with a smoke plume."""
    for bx, bw, bh in [(-1.0, 0.45, 0.9), (-0.45, 0.5, 1.25), (0.15, 0.45, 0.8),
                       (0.65, 0.35, 1.05)]:
        draw.rectangle([cx + bx * s, cy + s * 0.6 - bh * s,
                        cx + (bx + bw) * s, cy + s * 0.6], fill=col)
    draw.ellipse([cx - s * 0.15, cy - s * 1.15, cx + s * 0.25, cy - s * 0.75],
                 fill=(150, 150, 148))
    draw.ellipse([cx + s * 0.05, cy - s * 0.75, cx + s * 0.45, cy - s * 0.35],
                 fill=(170, 170, 168))
    draw.ellipse([cx - s * 0.35, cy - s * 0.4, cx + s * 0.05, cy],
                 fill=(190, 190, 188))


def drone_ship(draw, cx, cy, s, col):
    """Small drone above a ship hull."""
    draw.polygon([(cx - s * 0.9, cy + s * 0.25), (cx + s * 0.9, cy + s * 0.25),
                  (cx + s * 0.65, cy + s * 0.6), (cx - s * 0.65, cy + s * 0.6)],
                 fill=col)
    draw.rectangle([cx - s * 0.4, cy - s * 0.15, cx + s * 0.4, cy + s * 0.25],
                   fill=col)
    draw.ellipse([cx - s * 0.22, cy - s * 0.85, cx + s * 0.22, cy - s * 0.45],
                 outline=col, width=4)
    for dx in (-0.75, 0.75):
        draw.line([(cx + dx * s - s * 0.3, cy - s * 0.65),
                   (cx + dx * s + s * 0.3, cy - s * 0.65)], fill=col, width=4)
        draw.ellipse([cx + dx * s - s * 0.14, cy - s * 0.79,
                      cx + dx * s + s * 0.14, cy - s * 0.51], fill=col)


def helicopter(draw, cx, cy, s, col):
    """Helicopter side view."""
    draw.ellipse([cx - s * 0.75, cy - s * 0.35, cx + s * 0.35, cy + s * 0.35],
                 fill=col)
    draw.polygon([(cx + s * 0.3, cy - s * 0.1), (cx + s * 1.05, cy - s * 0.22),
                  (cx + s * 1.05, cy + s * 0.02), (cx + s * 0.3, cy + s * 0.12)],
                 fill=col)
    draw.line([(cx - s * 0.9, cy - s * 0.75), (cx + s * 0.9, cy - s * 0.75)],
              fill=col, width=5)
    draw.line([(cx - s * 0.05, cy - s * 0.35), (cx - s * 0.05, cy - s * 0.75)],
              fill=col, width=4)
    draw.line([(cx + s * 1.05, cy - s * 0.55), (cx + s * 1.05, cy + s * 0.25)],
              fill=col, width=4)
    draw.ellipse([cx - s * 0.55, cy - s * 0.2, cx - s * 0.2, cy + s * 0.15],
                 fill=(246, 241, 231))


def trophy(draw, cx, cy, s, col):
    """Cup trophy with a football beside it."""
    draw.polygon([(cx - s * 0.55, cy - s * 0.7), (cx + s * 0.55, cy - s * 0.7),
                  (cx + s * 0.4, cy + s * 0.1), (cx - s * 0.4, cy + s * 0.1)],
                 fill=col)
    draw.arc([cx - s * 0.95, cy - s * 0.7, cx - s * 0.35, cy - s * 0.05],
             90, 270, fill=col, width=5)
    draw.arc([cx + s * 0.35, cy - s * 0.7, cx + s * 0.95, cy - s * 0.05],
             270, 90, fill=col, width=5)
    draw.rectangle([cx - s * 0.12, cy + s * 0.1, cx + s * 0.12, cy + s * 0.5],
                   fill=col)
    draw.rectangle([cx - s * 0.45, cy + s * 0.5, cx + s * 0.45, cy + s * 0.62],
                   fill=col)
    draw.ellipse([cx + s * 0.45, cy + s * 0.25, cx + s * 0.95, cy + s * 0.75],
                 fill=(255, 255, 255), outline=col, width=3)
    draw.polygon([(cx + s * 0.7, cy + s * 0.38), (cx + s * 0.82, cy + s * 0.5),
                  (cx + s * 0.7, cy + s * 0.62), (cx + s * 0.58, cy + s * 0.5)],
                 fill=col)


ICONS = [scales, tanker, skyline, drone_ship, helicopter, trophy]

STORIES = [
    ("UNITED STATES · CHINA", "Huawei found guilty",
     "A US jury convicts the tech giant of stealing trade secrets and bank fraud — but clears it of racketeering.",
     (38, 84, 124)),
    ("STRAIT OF HORMUZ", "Four tankers hit by mines",
     "Iran says four tankers struck naval mines in the strait; its Revolutionary Guard says it hit a container ship.",
     (14, 110, 110)),
    ("GAZA", "Hamas security chief killed",
     "Israeli airstrikes kill Naeem Abu Nahel, head of Hamas' internal security, and six others in Gaza.",
     (150, 44, 38)),
    ("UKRAINE WAR", "Kyiv strikes Russian ships",
     "Ukraine says its drones hit the Russian cargo ship Sparta II in the Gulf of Finland and another off Libya.",
     (88, 96, 44)),
    ("TURKIYE", "Military helicopter crash",
     "A Turkish Air Force helicopter comes down after take-off from Eskisehir; all five crew members are killed.",
     (70, 76, 88)),
    ("FOOTBALL · AFRICA", "Senegal take the Cup back",
     "Senegal regain the Africa Cup of Nations title after a sports court appeal overturns the final result.",
     (28, 110, 66)),
]

ALSO = ("Also: Nvidia brings back Huang  ·  "
        "Oregon, Virginia sue SpaceX  ·  "
        "Germany into Ukraine's Delta system")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 88), "TUESDAY  ·  24 NOVEMBER 2026", font=font(SANS_B, 21),
           fill=GOLD, anchor="ma")
    d.line([(0, 118), (W, 118)], fill=GOLD, width=3)

    # Standfirst
    d.text((512, 138), "Six stories that defined the day — from a US courtroom to the Strait of Hormuz",
           font=font(SANS, 20), fill=INK, anchor="ma")
    d.line([(28, 168), (W - 28, 168)], fill=RULE, width=2)

    # Panel grid: 2 columns x 3 rows
    mx, gap = 28, 20
    top, panel_h = 186, 244
    pw = (W - 2 * mx - gap) // 2
    for i, (kicker, headline, summary, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = mx + col * (pw + gap)
        y0 = top + row * (panel_h + 18)
        x1, y1 = x0 + pw, y0 + panel_h
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=accent)
        # Pictogram on the left of the panel's top area
        icon_cx, icon_cy = x0 + 62, y0 + 78
        d.ellipse([icon_cx - 52, icon_cy - 52, icon_cx + 52, icon_cy + 52],
                  fill=(238, 233, 220))
        ICONS[i](d, icon_cx, icon_cy + 4, 34, accent)
        # Kicker + headline to the right of the pictogram
        tx = x0 + 132
        d.text((tx, y0 + 30), kicker, font=font(SANS_B, 15), fill=accent)
        head_lines = wrap(d, headline, font(SANS_B, 25), pw - 132 - 14)
        text_block(d, (tx, y0 + 52), head_lines[:2], font(SANS_B, 25), INK, 30)
        # Summary across the full panel width below
        sum_lines = wrap(d, summary, font(SANS, 17), pw - 28)
        text_block(d, (x0 + 14, y0 + 148), sum_lines[:3], font(SANS, 17),
                   (60, 58, 52), 23)

    # Footer
    fy = top + 3 * panel_h + 2 * 18 + 14
    d.line([(28, fy), (W - 28, fy)], fill=RULE, width=2)
    also_lines = wrap(d, ALSO, font(SANS_B, 16), W - 56)
    text_block(d, (28, fy + 10), also_lines, font(SANS_B, 16), INK, 22)
    d.text((512, H - 22), "Drawn from wire reports of 24 November 2026  ·  Reuters  ·  AP  ·  Al Jazeera  ·  AFP",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
