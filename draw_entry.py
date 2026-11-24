#!/usr/bin/env python3
"""Render entry.png for the make.fun news-image-20261123 bounty.

One 1024x1024 newspaper front page summing up Monday 23 November 2026:
a masthead, one lead story (Nvidia reinstates Jensen Huang), two
mid-size stories (Ukraine sinks a Russian warship off Libya; COP31
collapses in Antalya), three short stories (US Iran sanctions; FBI
probes a hack of its NCIC crime database; Indonesia candy-factory
fire), plus an ALSO TODAY ticker and a sources line.

Run: python3 draw_entry.py  -> writes entry.png next to this script.
Stdlib + Pillow only. No network access.
"""
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
EDGE = (210, 203, 185)
INK = (18, 18, 18)
SOFT = (96, 96, 90)
NAVY = (13, 32, 66)
GOLD = (198, 148, 42)
GREEN = (28, 112, 54)
STEEL = (28, 76, 138)
TEAL = (13, 102, 110)
RUST = (176, 42, 28)
PLUM = (106, 40, 138)
OCHRE = (150, 88, 4)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, width):
    """Greedy wrap; returns lines that fit inside width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if d.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def put_lines(d, lines, x, y, fnt, fill, gap):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += gap
    return y


def headline(d, text, x, y, width, max_lines, start, floor, color):
    """Headline that shrinks until it fits max_lines; returns bottom y."""
    size = start
    while size > floor:
        fnt = load(SERIF, size)
        if len(wrap_text(d, text, fnt, width)) <= max_lines:
            break
        size -= 2
    fnt = load(SERIF, size)
    lines = wrap_text(d, text, fnt, width)[:max_lines]
    return put_lines(d, lines, x, y, fnt, color, int(size * 1.14))


def body_text(d, text, x, y, width, max_lines, size, color=INK):
    fnt = load(SANS, size)
    lines = wrap_text(d, text, fnt, width)[:max_lines]
    return put_lines(d, lines, x, y, fnt, color, int(size * 1.32))


def kicker(d, text, x, y, color):
    fnt = load(SANS_B, 17)
    d.text((x, y), text, font=fnt, fill=color)
    return y + 24


def card(d, x0, y0, x1, y1, accent):
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD,
                        outline=EDGE, width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 14], radius=8, fill=accent)
    d.rectangle([x0, y0 + 7, x1, y0 + 14], fill=accent)


def rising_chart(d, x, y, w, h, color):
    """A jagged line climbing to the top right, with an arrowhead."""
    pts = [(x, y + h), (x + w * 0.22, y + h * 0.72),
           (x + w * 0.45, y + h * 0.82), (x + w * 0.66, y + h * 0.38),
           (x + w * 0.84, y + h * 0.48), (x + w, y + h * 0.06)]
    d.line(pts, fill=color, width=6, joint="curve")
    tip = (x + w, y + h * 0.06)
    d.polygon([(tip[0] + 2, tip[1] - 14), (tip[0] + 16, tip[1] + 2),
               (tip[0] - 2, tip[1] + 10)], fill=color)
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=color)


def ship_glyph(d, x, y, w, h, color):
    """Simple warship: hull, bridge, mast, waves."""
    d.polygon([(x, y + h * 0.55), (x + w, y + h * 0.55),
               (x + w * 0.82, y + h * 0.85), (x + w * 0.18, y + h * 0.85)],
              fill=color)
    d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.62, y + h * 0.55],
                fill=color)
    d.line([x + w * 0.52, y + h * 0.18, x + w * 0.52, y], fill=color, width=5)
    for i, wy in enumerate((y + h * 0.94, y + h)):
        d.line([(x + i * 8, wy), (x + w - i * 8, wy)], fill=color, width=3)


def cracked_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.line([(cx - r * 0.3, cy - r), (cx + r * 0.1, cy - r * 0.2),
            (cx - r * 0.25, cy + r * 0.25), (cx + r * 0.2, cy + r * 0.7)],
           fill=color, width=4)


def bank_glyph(d, x, y, w, h, color):
    d.polygon([(x, y + h * 0.22), (x + w / 2, y), (x + w, y + h * 0.22)],
              fill=color)
    d.rectangle([x, y + h * 0.28, x + w, y + h * 0.36], fill=color)
    for i in range(4):
        cx = x + w * (0.14 + i * 0.24)
        d.rectangle([cx - 6, y + h * 0.4, cx + 6, y + h * 0.86], fill=color)
    d.rectangle([x, y + h * 0.9, x + w, y + h], fill=color)


def shield_glyph(d, x, y, w, h, color):
    d.polygon([(x, y), (x + w, y), (x + w, y + h * 0.55),
               (x + w / 2, y + h), (x, y + h * 0.55)], outline=color,
              width=5)
    d.line([(x + w * 0.28, y + h * 0.5), (x + w * 0.45, y + h * 0.68),
            (x + w * 0.75, y + h * 0.3)], fill=color, width=6)


def flame_glyph(d, x, y, w, h, color):
    d.polygon([(x + w * 0.5, y), (x + w * 0.82, y + h * 0.42),
               (x + w, y + h * 0.72), (x + w * 0.68, y + h),
               (x + w * 0.32, y + h), (x, y + h * 0.72),
               (x + w * 0.18, y + h * 0.42)], fill=color)


def draw():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    m = 34  # outer margin

    # ---- masthead ---------------------------------------------------
    d.rectangle([m, 26, SIZE - m, 30], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = load(SERIF, 58)
    tw = d.textlength(title, font=tf)
    d.text(((SIZE - tw) / 2, 44), title, font=tf, fill=NAVY)
    sub = "MONDAY  ·  23 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS IN ONE PICTURE"
    sf = load(SANS_B, 19)
    sw = d.textlength(sub, font=sf)
    d.text(((SIZE - sw) / 2, 118), sub, font=sf, fill=GOLD)
    d.line([m, 152, SIZE - m, 152], fill=NAVY, width=3)
    d.line([m, 158, SIZE - m, 158], fill=NAVY, width=1)

    # ---- lead story: Nvidia -----------------------------------------
    x0, y0, x1, y1 = m, 176, SIZE - m, 408
    card(d, x0, y0, x1, y1, GREEN)
    gx, gy = x1 - 190, y0 + 34
    rising_chart(d, gx, gy, 150, 92, GREEN)
    d.text((gx, gy + 104), "+31% IN A DAY", font=load(SANS_B, 17), fill=GREEN)
    d.text((gx, gy + 126), "~$1 TRILLION BACK", font=load(SANS_B, 15),
           fill=SOFT)
    y = kicker(d, "MARKETS  ·  TECHNOLOGY", x0 + 22, y0 + 30, GREEN)
    y = headline(d, "HUANG IS BACK", x0 + 22, y, 700, 1, 64, 40, INK)
    body_text(d, "Nvidia's board unanimously reinstates Jensen Huang as "
              "CEO, 11 days after he resigned. Shares surge about 31% — "
              "roughly $1 trillion regained; Nasdaq +6.5%, S&P +4.7%.",
              x0 + 22, y + 8, 700, 3, 23)

    # ---- two mid-size stories ---------------------------------------
    mid_y0, mid_y1 = 424, 636
    mid_w = (SIZE - 2 * m - 18) // 2

    # Ukraine
    ax0, ay0, ax1 = m, mid_y0, m + mid_w
    card(d, ax0, ay0, ax1, mid_y1, STEEL)
    ship_glyph(d, ax1 - 84, ay0 + 24, 60, 48, STEEL)
    y = kicker(d, "WAR IN UKRAINE", ax0 + 20, ay0 + 26, STEEL)
    y = headline(d, "KYIV SINKS RUSSIAN WARSHIP OFF LIBYA",
                 ax0 + 20, y, mid_w - 120, 2, 30, 24, INK)
    body_text(d, "Zelensky confirms seven naval drones sank the corvette "
              "Merkury at Benghazi; a Ka-27 helicopter is destroyed.",
              ax0 + 20, y + 6, mid_w - 40, 3, 18)

    # COP31
    bx0, bx1 = m + mid_w + 18, SIZE - m
    card(d, bx0, ay0, bx1, mid_y1, TEAL)
    cracked_globe(d, bx1 - 56, ay0 + 56, 30, TEAL)
    y = kicker(d, "CLIMATE", bx0 + 20, ay0 + 26, TEAL)
    y = headline(d, "CLIMATE TALKS COLLAPSE", bx0 + 20, y,
                 mid_w - 120, 2, 30, 24, INK)
    body_text(d, "COP31 in Antalya ends with no deal — the first failure "
              "since Copenhagen 2009 — after fossil-fuel language is "
              "stripped from the text.", bx0 + 20, y + 6, mid_w - 40, 3, 18)

    # ---- three short stories ----------------------------------------
    sm_y0, sm_y1 = 656, 852
    sm_w = (SIZE - 2 * m - 36) // 3
    shorts = [
        (RUST, "WASHINGTON", "US CUTS IRAN'S 'LAST LIFELINE'",
         "The Trump administration imposes sweeping new sanctions on "
         "Tehran as Vance meets Qatar's PM over the stalled talks."),
        (PLUM, "CYBERSECURITY", "FBI PROBES DATABASE HACK",
         "The NCIC — the database police use for warrants and "
         "fugitives — is apparently breached. Trump: 'not good.'"),
        (OCHRE, "ASIA", "CANDY-FACTORY FIRE KILLS 24",
         "A blaze at a candy factory in Cikande kills 24 workers; "
         "dozens are still missing as rescuers search the ruins."),
    ]
    for i, (accent, kick, head, text) in enumerate(shorts):
        sx0 = m + i * (sm_w + 18)
        sx1 = sx0 + sm_w
        card(d, sx0, sm_y0, sx1, sm_y1, accent)
        y = kicker(d, kick, sx0 + 18, sm_y0 + 24, accent)
        y = headline(d, head, sx0 + 18, y, sm_w - 36, 2, 24, 18, INK)
        body_text(d, text, sx0 + 18, y + 6, sm_w - 36, 4, 16)

    # ---- ticker ------------------------------------------------------
    ty0, ty1 = 868, 936
    d.rounded_rectangle([m, ty0, SIZE - m, ty1], radius=8, fill=NAVY)
    tf2 = load(SANS_B, 18)
    label = "ALSO TODAY  "
    d.text((m + 18, ty0 + 22), label, font=tf2, fill=GOLD)
    lx = m + 18 + d.textlength(label, font=tf2)
    ticker = ("Nigeria funeral boat capsizes, 24 dead  •  UK to host the "
              "2035 Women's World Cup  •  Skubal signs record $450m Mets "
              "deal  •  South Korea says Russian jets entered its "
              "air-defence zone  •  China sentences official to death "
              "for spying")
    y = ty0 + 8
    for line in wrap_text(d, ticker, load(SANS, 16), SIZE - m - lx - 18):
        d.text((lx, y), line, font=load(SANS, 16), fill=(235, 235, 235))
        y += 20

    # ---- sources footer ----------------------------------------------
    foot = ("Sources: Reuters · AP · CNN · BBC · US Treasury · SEC filing  —  "
            "23 November 2026")
    ff = load(SANS, 16)
    fw = d.textlength(foot, font=ff)
    d.text(((SIZE - fw) / 2, 950), foot, font=ff, fill=SOFT)
    d.text((m, 984), "THE WORLD IN ONE DAY — 23 NOVEMBER 2026",
           font=load(SANS_B, 13), fill=SOFT)
    tail = "ONE PICTURE · SIX STORIES · ALL VERIFIED"
    d.text((SIZE - m - d.textlength(tail, font=load(SANS_B, 13)), 984),
           tail, font=load(SANS_B, 13), fill=SOFT)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
