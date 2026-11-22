#!/usr/bin/env python3
"""One-day newspaper front page: Saturday 21 November 2026.
Built fresh from the brief's prose spec. 1024x1024, flat vector panels,
PIL only. Deterministic output."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 219)
PAPER = (252, 248, 236)
INK = (26, 26, 26)
RED = (176, 30, 36)
DARKRED = (140, 20, 26)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GOLD = (201, 162, 39)
GREY = (90, 88, 80)
LIGHT = (215, 227, 238)
SKY = (178, 210, 232)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, maxw, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, maxw, lines, font, fill=INK, leading=None):
    if leading is None:
        leading = font.size + 3
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------- flat illustrations ----------------
def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 92, 99))
    d.ellipse([x + w * 0.34, y + h * 0.20, x + w * 0.66, y + h * 0.85], fill=(46, 160, 140))
    d.ellipse([x + w * 0.34, y + h * 0.20, x + w * 0.66, y + h * 0.85], outline=(255, 255, 255), width=2)
    for f in (0.36, 0.52, 0.68):
        d.arc([x + w * 0.34, y + h * f - 8, x + w * 0.66, y + h * f + 8],
              0, 180, fill=(255, 255, 255), width=1)
    d.line([x + w * 0.50, y + h * 0.20, x + w * 0.50, y + h * 0.85], fill=(255, 255, 255), width=1)
    d.ellipse([x + w * 0.72, y + h * 0.08, x + w * 0.88, y + h * 0.30], fill=(255, 196, 0))
    d.text((x + 8, y + 6), "DAY 13  •  NO DEAL", font=F(SANSB, 11), fill=(255, 255, 255))


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.38, y + h], fill=(120, 116, 108))
    d.rectangle([x + w * 0.44, y + h * 0.30, x + w * 0.74, y + h], fill=(96, 92, 84))
    d.rectangle([x + w * 0.78, y + h * 0.52, x + w * 0.95, y + h], fill=(140, 136, 128))
    for bx in (0.14, 0.24, 0.50, 0.60, 0.83):
        for by in (0.50, 0.62, 0.74):
            d.rectangle([x + w * bx, y + h * by, x + w * bx + 8, y + h * by + 7],
                        fill=(255, 220, 120))
    d.polygon([(x + w * 0.55, y + h * 0.30), (x + w * 0.68, y + h * 0.02),
               (x + w * 0.80, y + h * 0.30)], fill=(230, 90, 30))
    d.polygon([(x + w * 0.62, y + h * 0.30), (x + w * 0.68, y + h * 0.14),
               (x + w * 0.74, y + h * 0.30)], fill=(255, 196, 0))
    d.text((x + 8, y + 6), "DOUBLE-TAP STRIKE", font=F(SANSB, 11), fill=(120, 20, 20))


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 32, 64))
    for sx, sy in [(0.12, 0.18), (0.35, 0.10), (0.60, 0.22), (0.82, 0.12), (0.50, 0.30)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(255, 255, 255))
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h], fill=(10, 18, 38))
    for bx, bw, bh in [(0.08, 0.10, 0.30), (0.22, 0.08, 0.38), (0.34, 0.12, 0.26),
                       (0.50, 0.09, 0.36), (0.63, 0.11, 0.28), (0.78, 0.09, 0.34)]:
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h], fill=(52, 68, 110))
        for wy in (0.70, 0.80, 0.90):
            d.rectangle([x + w * (bx + 0.02), y + h * wy, x + w * (bx + bw - 0.02), y + h * wy + 4],
                        fill=(255, 220, 120))
    for cx, cy in [(0.30, 0.45), (0.55, 0.35), (0.78, 0.48)]:
        d.arc([x + w * (cx - 0.22), y + h * (cy - 0.22), x + w * (cx + 0.22), y + h * (cy + 0.22)],
              200, 340, fill=(255, 196, 0), width=3)
        d.ellipse([x + w * cx - 5, y + h * cy - 5, x + w * cx + 5, y + h * cy + 5],
                  fill=(255, 120, 0))
        for a in range(0, 360, 45):
            r = 12
            d.line([x + w * cx + r * math.cos(math.radians(a)), y + h * cy + r * math.sin(math.radians(a)),
                    x + w * cx + (r + 7) * math.cos(math.radians(a)), y + h * cy + (r + 7) * math.sin(math.radians(a))],
                   fill=(255, 196, 0), width=2)
    d.text((x + 8, y + h - 18), "3 MISSILES INTERCEPTED", font=F(SANSB, 11), fill=(255, 255, 255))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 196))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(150, 110, 70))
    d.polygon([(x, y + h * 0.62), (x + w * 0.30, y + h * 0.28), (x + w * 0.45, y + h * 0.62),
               (x + w * 0.62, y + h * 0.40), (x + w * 0.80, y + h * 0.62), (x + w, y + h * 0.55),
               (x + w, y + h * 0.62)], fill=(110, 80, 50))
    pts = []
    for i in range(21):
        px = x + i * w / 20
        py = y + h * 0.22 + (14 if i % 2 else -14) * (1 if 5 < i < 15 else 0.25)
        pts.append((px, py))
    d.line(pts, fill=(176, 30, 36), width=2)
    d.text((x + 8, y + h - 20), "M6.7  •  108 KM DEEP", font=F(SANSB, 11), fill=(120, 20, 20))


def ill_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 30))
    for sx, sy in [(0.10, 0.15), (0.30, 0.08), (0.55, 0.18), (0.80, 0.10), (0.90, 0.30), (0.20, 0.35)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w * 0.58, y + h * 0.30, x + w * 0.92, y + h * 0.95], fill=(214, 132, 60))
    d.ellipse([x + w * 0.62, y + h * 0.36, x + w * 0.72, y + h * 0.52], fill=(170, 95, 40))
    d.ellipse([x + w * 0.76, y + h * 0.60, x + w * 0.84, y + h * 0.72], fill=(170, 95, 40))
    for i in range(6):
        t = i / 5
        d.ellipse([x + w * (0.10 + t * 0.40), y + h * (0.75 - t * 0.45) - 2,
                   x + w * (0.10 + t * 0.40) + 4, y + h * (0.75 - t * 0.45) + 2],
                  fill=(255, 196, 0))
    d.rectangle([x + w * 0.08, y + h * 0.62, x + w * 0.16, y + h * 0.74], fill=(200, 200, 210))
    d.rectangle([x + w * 0.02, y + h * 0.66, x + w * 0.08, y + h * 0.70], fill=(90, 130, 200))
    d.rectangle([x + w * 0.16, y + h * 0.66, x + w * 0.22, y + h * 0.70], fill=(90, 130, 200))
    d.text((x + 8, y + 6), "8 YEARS  •  19:24 CET", font=F(SANSB, 10), fill=(255, 255, 255))


def ill_warsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 78, 121))
    cx, cy, r = x + w * 0.5, y + h * 0.55, h * 0.24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    for a in (0, 90, 180, 270):
        d.polygon([(cx, cy - r * 0.85), (cx + 5, cy), (cx, cy + r * 0.85), (cx - 5, cy)],
                  fill=(255, 255, 255)) if a in (0, 180) else None
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
               (cx + r * 0.28, cy + r * 0.28), (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
               (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=(255, 255, 255))
    d.text((x + 8, y + 5), "NATO  •  RUTTE IN WARSAW", font=F(SANSB, 10), fill=(255, 255, 255))


def ill_rahul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 60))
    d.ellipse([x + w * 0.10, y + h * 0.15, x + w * 0.90, y + h * 0.95], fill=(120, 180, 90))
    d.ellipse([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.80], outline=(255, 255, 255), width=2)
    d.line([x + w * 0.30, y + h * 0.18, x + w * 0.42, y + h * 0.55], fill=(222, 184, 135), width=6)
    d.ellipse([x + w * 0.62, y + h * 0.42, x + w * 0.70, y + h * 0.54], fill=(176, 30, 36))
    d.text((x + 8, y + 6), "124*  •  INDIA 344/2", font=F(SANSB, 11), fill=(255, 255, 255))


def ill_zelensky(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(70, 130, 200))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(255, 213, 0))
    d.rectangle([x + w * 0.10, y + h * 0.62, x + w * 0.90, y + h * 0.70], fill=(90, 90, 95))
    d.line([x + w * 0.18, y + h * 0.62, x + w * 0.18, y + h * 0.30], fill=(90, 90, 95), width=3)
    d.line([x + w * 0.82, y + h * 0.62, x + w * 0.82, y + h * 0.30], fill=(90, 90, 95), width=3)
    d.arc([x + w * 0.18, y + h * 0.30, x + w * 0.82, y + h * 0.95], 180, 360, fill=(90, 90, 95), width=4)
    d.text((x + 8, y + 6), "KYIV  •  NBC INTERVIEW", font=F(SANSB, 10), fill=(255, 255, 255))


def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 205, 210))
    d.ellipse([x + w * 0.30, y + h * 0.38, x + w * 0.70, y + h * 0.58], fill=(70, 74, 80))
    d.rectangle([x + w * 0.05, y + h * 0.44, x + w * 0.95, y + h * 0.50], fill=(70, 74, 80))
    d.text((x + 8, y + h - 20), "CLAIM No. 58  •  UNCONFIRMED", font=F(SANSB, 10), fill=(120, 20, 20))


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 210, 232))
    d.ellipse([x + w * 0.68, y + h * 0.10, x + w * 0.86, y + h * 0.34], fill=(255, 255, 255))
    d.ellipse([x + w * 0.10, y + h * 0.22, x + w * 0.24, y + h * 0.40], fill=(255, 255, 255))
    d.polygon([(x + w * 0.15, y + h * 0.55), (x + w * 0.75, y + h * 0.55),
               (x + w * 0.85, y + h * 0.65), (x + w * 0.15, y + h * 0.65)], fill=(240, 240, 240))
    d.polygon([(x + w * 0.55, y + h * 0.55), (x + w * 0.68, y + h * 0.32),
               (x + w * 0.74, y + h * 0.55)], fill=(200, 200, 205))
    d.rectangle([x, y + h * 0.82, x + w, y + h * 0.90], fill=(90, 90, 90))
    d.ellipse([x + w * 0.86, y + h * 0.68, x + w * 0.98, y + h * 0.90], outline=(15, 118, 110), width=3)
    d.line([x + w * 0.89, y + h * 0.73, x + w * 0.95, y + h * 0.85], fill=(15, 118, 110), width=3)
    d.line([x + w * 0.95, y + h * 0.73, x + w * 0.89, y + h * 0.85], fill=(15, 118, 110), width=3)
    d.text((x + 8, y + h - 20), "146 ABOARD  •  ALL SAFE", font=F(SANSB, 10), fill=(15, 90, 80))


def ill_ai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 40, 66))
    nodes = [(0.20, 0.44), (0.80, 0.44), (0.30, 0.72), (0.65, 0.68), (0.50, 0.90)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            d.line([x + w * nodes[i][0], y + h * nodes[i][1],
                    x + w * nodes[j][0], y + h * nodes[j][1]], fill=(90, 140, 200), width=1)
    for nx, ny in nodes:
        d.ellipse([x + w * nx - 6, y + h * ny - 6, x + w * nx + 6, y + h * ny + 6],
                  fill=(255, 196, 0), outline=(255, 255, 255))
    d.text((x + 8, y + 5), "CANBERRA  •  11-DAY TRIP ENDS", font=F(SANSB, 10), fill=(255, 255, 255))


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 243, 205))
    d.ellipse([x + w * 0.30, y + h * 0.12, x + w * 0.70, y + h * 0.80], fill=(247, 147, 26))
    d.text((x + w * 0.44, y + h * 0.24), "₿", font=F(SANSB, 34), fill=(255, 255, 255))
    pts = [(x + w * 0.08, y + h * 0.30), (x + w * 0.30, y + h * 0.42),
           (x + w * 0.50, y + h * 0.36), (x + w * 0.68, y + h * 0.58), (x + w * 0.80, y + h * 0.68)]
    d.line(pts, fill=(176, 30, 36), width=3)
    d.polygon([(x + w * 0.80, y + h * 0.68), (x + w * 0.74, y + h * 0.62), (x + w * 0.80, y + h * 0.58)],
              fill=(176, 30, 36))
    d.text((x + 8, y + h - 20), "$58,983  •  −3.9% IN 24H", font=F(SANSB, 10), fill=(120, 20, 20))


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 34))
    for r in range(3):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle([x + w * 0.06 + c * 12, y + h * 0.12 + r * 12,
                             x + w * 0.06 + c * 12 + 12, y + h * 0.12 + r * 12 + 12],
                            fill=(255, 255, 255))
    d.rounded_rectangle([x + w * 0.10, y + h * 0.58, x + w * 0.88, y + h * 0.76],
                        radius=8, fill=(200, 30, 40))
    d.ellipse([x + w * 0.22, y + h * 0.72, x + w * 0.34, y + h * 0.88], fill=(20, 20, 20))
    d.ellipse([x + w * 0.66, y + h * 0.72, x + w * 0.78, y + h * 0.88], fill=(20, 20, 20))
    d.text((x + 8, y + h - 20), "1:34.041  •  WET PRACTICE", font=F(SANSB, 10), fill=(255, 255, 255))


ILL = {"cop31": ill_cop31, "kryvyi": ill_kryvyi, "riyadh": ill_riyadh, "peru": ill_peru,
       "bepi": ill_bepi, "warsaw": ill_warsaw, "rahul": ill_rahul, "zelensky": ill_zelensky,
       "drone": ill_drone, "plane": ill_plane, "ai": ill_ai, "bitcoin": ill_bitcoin, "f1": ill_f1}

# ---------------- stories: 13 panels ----------------
# (num, region, headline, body, source, illustration)
PANELS = [
    (1, "Europe", "COP31 runs into overtime with no deal in sight",
     "Climate summit enters day 13 in Antalya. A third draft with no fossil-fuel phase-out splits nearly 200 nations.",
     "Reuters", "cop31"),
    (2, "Europe", "Russia hits Kryvyi Rih twice; 2 killed, 42 hurt",
     "A double-tap strike on the Ukrainian city kills two people and wounds 42, officials say, as rescue work goes on.",
     "Reuters", "kryvyi"),
    (3, "Middle East", "Three missiles downed over Riyadh",
     "A Saudi-led coalition intercepts three Houthi missiles on a third night of warnings. Two blasts about 02:00; no casualties.",
     "AP", "riyadh"),
    (4, "Americas", "Magnitude 6.7 quake shakes Peru",
     "The tremor strikes Junín at 00:09 UTC, 108 km deep. No deaths and no tsunami are reported.",
     "USGS", "peru"),
    (5, "Europe", "BepiColombo reaches Mercury after 8 years",
     "The ESA–JAXA probe arrives at Mercury, firing thrusters at 19:24 CET to end its long journey from Earth.",
     "ESA", "bepi"),
    (6, "Europe", "Rutte in Warsaw as NATO weighs its next move",
     "The NATO chief visits Poland for talks on the alliance's eastern flank and support for Ukraine.",
     "Reuters", "warsaw"),
    (7, "Oceania", "Rahul's 124* puts India on top in Wellington",
     "KL Rahul is unbeaten on 124 at tea as India reach 344 for 2, replying to New Zealand's 368.",
     "AP", "rahul"),
    (8, "Europe", "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "Ukraine's president tells NBC the bridge linking Russia to occupied Crimea will not survive the war.",
     "NBC", "zelensky"),
    (9, "Middle East", "Iran says it shot down a US MQ-9 over Hormuz",
     "Tehran claims its 58th downing of an American drone. Washington has not confirmed the claim.",
     "Reuters", "drone"),
    (10, "Asia", "Air Niugini 767 lands safely in Davao",
     "All 146 people aboard survive after the Boeing 767 makes an emergency landing in the Philippines.",
     "AP", "plane"),
    (11, "Oceania", "Australia and China agree to talk on AI",
     "Canberra and Beijing will open talks on artificial intelligence as Albanese ends an 11-day trip.",
     "Reuters", "ai"),
    (12, "Americas", "Bitcoin falls below $59,000",
     "Bitcoin drops to $58,983, down 3.9% in 24 hours, as the sell-off in crypto deepens.",
     "Reuters", "bitcoin"),
    (13, "Americas", "Russell fastest in wet Las Vegas practice",
     "George Russell clocks 1:34.041 in rain-hit practice for the Las Vegas Grand Prix; Verstappen takes pole.",
     "AP", "f1"),
]

# ---------------- ALSO: items 14-33, two columns ----------------
ALSO = [
    (14, "Middle East", "Iran: uranium stock stays at home", "Reuters"),
    (15, "Americas", "Trump vows tax on foreign data centres", "Reuters"),
    (16, "Asia", "China: Japan must \u201ccorrect\u201d Taiwan words", "AP"),
    (17, "Africa", "Funeral boat sinks, Bayelsa; 4+ dead", "AP"),
    (18, "Africa", "ANC falls to 31%, worst since 1994", "Reuters"),
    (19, "Europe", "ATP semis in Turin: Medvedev v Zverev", "AP"),
    (20, "Middle East", "Israeli strikes on Gaza kill 6", "Al Jazeera"),
    (21, "Asia", "Freight train derails in Sejong", "AP"),
    (22, "Europe", "Denmark expels Russian defence attach\u00e9", "Reuters"),
    (23, "Americas", "Vance: Iran strike is Trump's call", "AP"),
    (24, "Americas", "Roundup deal in Missouri: $7.25bn", "Reuters"),
    (25, "Americas", "Texas execution takes 63 minutes", "AP"),
    (26, "Americas", "Palisades fire verdict: 12 dead in LA", "AP"),
    (27, "Asia", "Kim visits a factory in Pyongyang", "AP"),
    (28, "Asia", "Taipei passes its budget", "Reuters"),
    (29, "Asia", "Bangkok unveils arsenic plan", "AP"),
    (30, "Asia", "SCO forum opens in New Delhi", "Reuters"),
    (31, "Oceania", "Starc takes 7/58 in Ashes at Perth", "AP"),
    (32, "Africa", "Rating agency opens in Port Louis", "Reuters"),
    (33, "Asia", "New sanctions target Myanmar", "Reuters"),
]

REGIONS = [("Europe", 7, (31, 78, 121)), ("Asia", 8, (15, 118, 110)),
           ("Middle East", 4, (176, 30, 36)), ("Africa", 3, (201, 162, 39)),
           ("Americas", 8, (90, 60, 140)), ("Oceania", 3, (220, 110, 40))]

STATS = [("3", "MISSILES DOWNED", "over Riyadh"),
         ("M6.7", "QUAKE IN PERU", "108 km deep"),
         ("146", "SAFE IN DAVAO", "emergency landing"),
         ("2 KILLED", "KRYVYI RIH", "42 wounded"),
         ("$58,983", "BITCOIN", "down 3.9% in 24h"),
         ("124*", "RAHUL", "Wellington, India 344/2")]

# lon/lat of each numbered story for the map
GEO = {1: (30.7, 36.9), 2: (33.4, 47.9), 3: (46.7, 24.7), 4: (-75.9, -11.2),
       5: (8.6, 49.9), 6: (21.0, 52.2), 7: (174.8, -41.3), 8: (30.5, 50.4),
       9: (56.5, 26.5), 10: (125.6, 7.1), 11: (149.1, -35.3), 12: (-74.0, 40.7),
       13: (-115.1, 36.2)}
# BepiColombo has no Earth site: pin 5 at ESA Darmstadt (8.6E, 49.9N).
# nudge apart the crowded Europe / Gulf pins (dx, dy in px)
NUDGE = {1: (0, 12), 2: (12, 10), 3: (-10, 10), 5: (-6, -8), 6: (6, 6),
         8: (-8, -12), 9: (12, -6)}


def draw_panel(d, x, y, w, h, num, headline, body, source, ill, hero=False):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=(180, 170, 145), width=1)
    ih = 78 if hero else 50
    ILL[ill](d, x + 1, y + 1, w - 2, ih)
    d.ellipse([x + 6, y + ih + 6, x + 26, y + ih + 26], fill=RED)
    tw = d.textlength(str(num), font=F(SANSB, 12))
    d.text((x + 16 - tw / 2, y + ih + 8), str(num), font=F(SANSB, 12), fill=(255, 255, 255))
    tx = x + 32
    hf = F(SANSB, 14 if hero else 11)
    lines = wrap(headline, hf, w - 40, d)[:2]
    yy = block(d, tx, y + ih + 5, w - 40, lines, hf, leading=16 if hero else 13)
    bf = F(SANS, 10 if hero else 9)
    blines = wrap(body, bf, w - 16, d)[:3]
    yy = block(d, x + 8, yy + 3, w - 16, blines, bf, leading=12 if hero else 11)
    d.text((x + 8, y + h - 13), source.upper(), font=F(SANSB, 8), fill=GREY)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(180, 170, 145), width=1)
    d.text((x + 10, y + 7), "WHERE IT HAPPENED", font=F(SANSB, 13), fill=INK)
    d.text((x + 10, y + 24), "13 places, 13 stories \u2014 numbers match the panels above",
           font=F(SANS, 9), fill=GREY)
    mx, my, mw, mh = x + 8, y + 42, w - 16, h - 50
    d.rectangle([mx, my, mx + mw, my + mh], fill=(235, 240, 246))
    # rough continent blobs (lon/lat polygons)
    conts = [
        [(-168, 66), (-140, 70), (-120, 70), (-95, 68), (-80, 62), (-60, 55), (-55, 47),
         (-70, 42), (-75, 30), (-80, 25), (-85, 15), (-95, 18), (-105, 22), (-115, 30),
         (-125, 40), (-125, 55), (-150, 60), (-165, 60)],
        [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -40),
         (-68, -52), (-72, -40), (-75, -20), (-80, -5)],
        [(-10, 36), (-8, 44), (-2, 48), (0, 52), (5, 58), (10, 60), (18, 66), (28, 70),
         (35, 68), (40, 60), (38, 50), (30, 45), (28, 40), (20, 40), (12, 38), (0, 36)],
        [(-18, 32), (-10, 30), (0, 35), (10, 34), (20, 32), (32, 30), (38, 22), (45, 12),
         (50, 10), (42, 0), (40, -12), (36, -22), (32, -30), (25, -34), (18, -30), (12, -18),
         (8, -5), (0, 5), (-8, 8), (-16, 15)],
        [(40, 70), (60, 72), (80, 73), (100, 75), (130, 72), (160, 70), (178, 65), (170, 60),
         (160, 55), (140, 42), (130, 35), (122, 30), (110, 20), (105, 8), (100, 5), (95, 12),
         (85, 20), (75, 8), (65, 8), (58, 25), (50, 30), (45, 40), (42, 50)],
        [(113, -22), (122, -14), (132, -12), (142, -10), (150, -20), (153, -28), (150, -37),
         (140, -38), (130, -32), (120, -34), (113, -30)],
    ]
    for poly in conts:
        pts = [(mx + (lon + 180) / 360 * mw, my + (90 - lat) / 180 * mh) for lon, lat in poly]
        d.polygon(pts, fill=LIGHT, outline=(160, 175, 195))
    # graticule
    for lon in range(-150, 181, 30):
        gx = mx + (lon + 180) / 360 * mw
        d.line([gx, my, gx, my + mh], fill=(220, 228, 236), width=1)
    for lat in (-60, -30, 0, 30, 60):
        gy = my + (90 - lat) / 180 * mh
        d.line([mx, gy, mx + mw, gy], fill=(220, 228, 236), width=1)
    for num, (lon, lat) in GEO.items():
        px = mx + (lon + 180) / 360 * mw
        py = my + (90 - lat) / 180 * mh
        dx, dy = NUDGE.get(num, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
        tw = d.textlength(str(num), font=F(SANSB, 9))
        d.text((px - tw / 2, py - 6), str(num), font=F(SANSB, 9), fill=(255, 255, 255))

# ---------------- page build ----------------
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 24
    # top dateline strip
    d.text((M, 8), "SATURDAY EDITION  \u2022  ALL THE NEWS THAT FIT ONE DAY",
           font=F(SANSB, 10), fill=GREY)
    rt = "33 STORIES  \u2022  6 REGIONS  \u2022  ONE PAGE"
    d.text((W - M - d.textlength(rt, font=F(SANSB, 10)), 8), rt,
           font=F(SANSB, 10), fill=GREY)
    d.line([M, 26, W - M, 26], fill=INK, width=2)
    # masthead
    mast = "THE WORLD IN ONE DAY"
    mf = F(SERIFB, 60)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 32), mast, font=mf, fill=RED)
    d.line([M, 100, W - M, 100], fill=RED, width=2)
    # date title
    title = "Saturday 21 November 2026"
    tf = F(SERIFB, 52)
    d.text(((W - d.textlength(title, font=tf)) / 2, 106), title, font=tf, fill=INK)
    sub = "COP31 talks run into overtime without a deal  \u2014  Three missiles downed over Riyadh  \u2014  Magnitude 6.7 quake shakes Peru"
    sf = F(SERIFI, 15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 162), sub, font=sf, fill=INK)
    d.line([M, 186, W - M, 186], fill=INK, width=1)
    # stats strip: 6 boxes
    bw, gap = 158, 6
    y0 = 192
    for i, (big, lab, sub2) in enumerate(STATS):
        x0 = M + i * (bw + gap)
        d.rectangle([x0, y0, x0 + bw, y0 + 44], fill=PAPER, outline=(180, 170, 145), width=1)
        bf = F(SANSB, 19)
        d.text((x0 + (bw - d.textlength(big, font=bf)) / 2, y0 + 3), big, font=bf, fill=RED)
        lf = F(SANSB, 9)
        d.text((x0 + (bw - d.textlength(lab, font=lf)) / 2, y0 + 25), lab, font=lf, fill=INK)
        sf2 = F(SANS, 8)
        d.text((x0 + (bw - d.textlength(sub2, font=sf2)) / 2, y0 + 35), sub2, font=sf2, fill=GREY)
    # region bar
    y0 = 244
    d.text((M, y0), "33 STORIES ACROSS 6 REGIONS", font=F(SANSB, 12), fill=INK)
    bar_y, bar_h = y0 + 18, 14
    total = sum(c for _, c, _ in REGIONS)
    assert total == 33, total
    x = M
    for name, count, color in REGIONS:
        seg = (W - 2 * M) * count / total
        d.rectangle([x, bar_y, x + seg, bar_y + bar_h], fill=color)
        if seg > 34:
            lbl = str(count)
            lf = F(SANSB, 10)
            d.text((x + (seg - d.textlength(lbl, font=lf)) / 2, bar_y + 2), lbl,
                   font=lf, fill=(255, 255, 255))
        x += seg
    d.rectangle([M, bar_y, W - M, bar_y + bar_h], outline=INK, width=1)
    leg = "   ".join(f"{n} {c}" for n, c, _ in REGIONS) + "   =  33"
    d.text((M, bar_y + 18), leg, font=F(SANS, 10), fill=INK)
    # heroes: 3 across
    hy, hh, hw, hgap = 300, 168, 317, 12
    for i in range(3):
        num, region, head, body, src, ill = PANELS[i]
        draw_panel(d, M + i * (hw + hgap), hy, hw, hh, num, head, body, src, ill, hero=True)
    # small panels: 2 rows x 5
    pw, pgap, ph = 188, 9, 134
    for r in range(2):
        for c in range(5):
            idx = 3 + r * 5 + c
            num, region, head, body, src, ill = PANELS[idx]
            draw_panel(d, M + c * (pw + pgap), 476 + r * (ph + 8), pw, ph,
                       num, head, body, src, ill)
    # map (left) + ALSO list (right)
    my, mh2 = 752, 142
    draw_map(d, M, my, 500, mh2)
    ax, aw = 536, 464
    d.rectangle([ax, my, ax + aw, my + mh2], fill=PAPER, outline=(180, 170, 145), width=1)
    d.text((ax + 10, my + 6), "ALSO ON SATURDAY 21 NOVEMBER \u2014 20 MORE STORIES",
           font=F(SANSB, 12), fill=INK)
    d.line([ax + 10, my + 24, ax + aw - 10, my + 24], fill=(180, 170, 145), width=1)
    af = F(SANS, 9)
    colw = (aw - 20 - 12) // 2
    for k, (num, region, text, src) in enumerate(ALSO):
        col = k // 10
        row = k % 10
        xx = ax + 10 + col * (colw + 12)
        yy = my + 30 + row * 11
        label = f"{num}. {text}"
        lines = wrap(label, af, colw, d)
        line = lines[0]
        if len(lines) > 1:
            line = line[:-1] + "\u2026" if len(line) > 3 else line
        d.text((xx, yy), line, font=af, fill=INK)
    # DATE CHECK
    dy, dh = 902, 58
    d.rectangle([M, dy, W - M, dy + dh], fill=(255, 250, 240), outline=RED, width=2)
    d.text((M + 10, dy + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=F(SANSB, 11), fill=RED)
    dc = ("Left out on purpose \u2014 all Friday 20 November, not today: Wall Street's slide into "
          "correction; Russia's strike on a Kyiv bridge; a missile landing in Poland; the UK\u2013EU "
          "reset deal; Cyclone Akvan's landfall. Voyager 1 passed one light-day out on 18 Nov. "
          "Not yet confirmed at press time: the final COP31 text; BepiColombo's entry into orbit.")
    df = F(SANS, 10)
    block(d, M + 10, dy + 21, W - 2 * M - 20, wrap(dc, df, W - 2 * M - 20, d), df, leading=12)
    # footer
    fy = 968
    d.line([M, fy, W - M, fy], fill=INK, width=1)
    f1 = "Every story here happened, or was first reported, on Saturday 21 November 2026."
    ff = F(SERIFB, 12)
    d.text(((W - d.textlength(f1, font=ff)) / 2, fy + 6), f1, font=ff, fill=INK)
    f2 = "Sources: Reuters  \u2022  AP  \u2022  AFP  \u2022  Al Jazeera  \u2022  USGS  \u2022  ESA  \u2022  NBC  \u2022  BBC"
    f2f = F(SANS, 10)
    d.text(((W - d.textlength(f2, font=f2f)) / 2, fy + 24), f2, font=f2f, fill=GREY)
    f3 = ("HOW WE CHECKED: every story matched to its first wire report of 21 November 2026; "
          "unconfirmed claims are marked CLAIM.  \u2014  THE WORLD IN ONE DAY, Saturday 21 November 2026.")
    f3f = F(SANS, 9)
    d.text(((W - d.textlength(f3, font=f3f)) / 2, fy + 38), f3, font=f3f, fill=GREY)
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)
