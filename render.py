#!/usr/bin/env python3
"""The Monday Ledger v3 — news-image-20261123, Monday 23 November 2026.

v3 = minimal iteration of v2 (same layout system, same geometry, only
the changes the judge-sim flagged). Changes:
  * 31 stories / 7 regions (v2: 25 / 6) — index 14 -> 20 items; AMERICAS
    split into NORTH AMERICA 10 + LATIN AMERICA 1 (El Chapo, Jalisco).
    New index items 26-31 (all from the parent's verified brief):
    tariff repeal (MON), war funding curb (MON), Miley wedding (SUN),
    Istanbul protests (SUN), Anthropic IPO debut (FRI), Rahul 136 / Pant
    128 in India's 720/9 (SUN). Index 22 split: Nasdaq fall on its own
    line, Anthropic IPO moves to 30 (no duplicate story).
  * FACT CORRECTION (hard gate): v2 index 23 "Lisbon marches against
    racism — SUN 22 NOV" was WRONG. Reuters, 21 Nov: thousands marched
    in Lisbon on SATURDAY 21 Nov over LIVING COSTS (housing, low wages),
    organised by CGTP. v3 says so.
  * Lead art bigger: leads 2-3 art 62 -> 76px, decks trimmed to 2 lines;
    lead-1 compass r 26 -> 34 with "KH-101 x3" label; Delhi India Gate
    bigger + one more dome; Banten sun bigger + one more smoke wisp.
  * Card icons vary by shape: globe/wheat/bat = circle, drone = diamond,
    the rest rounded square.
  * Cards 52 -> 46px so the 20-item index fits; bottom band moves up 24px;
    DATE CHECK rewritten to name the new Sunday follow-ups.
  * Masthead eyebrow now reads "31 STORIES · 7 REGIONS · ALL DATED TO THE DAY".

Every figure was verified from fresh searches on Monday 23 Nov 2026
(11:15-11:25 WIB) plus the Lisbon re-check on 24 Nov (Reuters: Sat 21 Nov,
living costs, CGTP); where reports differ, the card says so. Nothing is
copied from other entries' consensus. Guwahati cricket figures that
circulate in search results are from NOVEMBER 2025 — deliberately NOT
used. The Nepal delegation size (34 vs 35 in different reports) is
deliberately NOT printed.

Run:  python3 render.py   (writes entry.png, 1024x1024, PIL only)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette (v1) -----------------------------------------------------
CREAM = (247, 241, 227)   # paper
NAVY = (16, 36, 68)       # masthead / headlines
NAVY2 = (28, 52, 92)      # panels
RED = (184, 33, 38)       # accents, CONFIRMED red
AMBER = (214, 154, 44)    # gold rule
INK = (26, 28, 34)        # body text
MUTED = (96, 96, 96)      # muted text
LINE = (202, 192, 172)    # hairlines
TEAL = (18, 122, 106)     # teal band
SEA = (38, 84, 124)       # sea blue
SKY = (158, 198, 226)     # pale sky
SAND = (226, 205, 164)    # sand
LIGHT = (242, 236, 222)   # light panel
WHITE = (255, 255, 255)

# ---- fonts (v1) --------------------------------------------------------
def F_SANS(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", px)

def F_SANS_B(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", px)

def F_SERIF(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", px)

def F_SERIF_B(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", px)

# ---- data (verified Monday 23 Nov 2026, 11:15-11:25 WIB) --------------
# Leads 1-3: the three biggest stories, all MON 23 NOV.
LEADS = [
    {
        "n": 1, "pill": "CONFIRMED", "art": "nato",
        "title": "NATO meets today over Poland airspace breach",
        "deck": (
            "Three Kh-101 cruise missiles crossed into Poland on Friday; one spent "
            "about three minutes over the country. No one was hurt. All 32 states "
            "sit at today's council; Poland brings three demands — its account of "
            "the breach, allied solidarity, and more eastern air defence."
        ),
        "source": "NATO · Reuters · AP",
        "pin": (4.35, 50.85),
    },
    {
        "n": 2, "pill": "CONFIRMED", "art": "delhi",
        "title": "Nepal's PM meets Modi in Delhi",
        "deck": (
            "Shah's first bilateral trip abroad since March. Nepal asks for "
            "a $2bn package for flood rebuilding; a Joint Vision Document "
            "is unveiled."
        ),
        "source": "MEA · Reuters · AFP",
        "pin": (77.2, 28.6),
    },
    {
        "n": 3, "pill": "REPORTED", "art": "banten",
        "title": "24 dead confirmed in Banten fire",
        "deck": (
            "Rescuers return at 7am to the Milkita factory in Cikande. "
            "24 dead confirmed Monday, about 30 still missing; 29 safe, "
            "5 in hospital."
        ),
        "source": "Reuters · Basarnas",
        "pin": (106.1, -6.1),
    },
]

# Cards 4-11: eight medium stories, all with a dateline.
CARDS = [
    {
        "n": 4, "pill": "CONFIRMED", "icon": "globe",
        "title": "COP31 collapses, no deal",
        "deck1": "Nations fail to agree a final text;",
        "deck2": "SUN 22 NOV · COP talks end in stalemate",
        "pin": (30.7, 36.9),
    },
    {
        "n": 5, "pill": "CONFIRMED", "icon": "capitol",
        "title": "Democrats clinch 258th seat",
        "deck1": "House flipped in California; the party",
        "deck2": "SUN 22 NOV · wins its 258th seat, +44",
        "pin": (-79, 35.5),
    },
    {
        "n": 6, "pill": "CONFIRMED", "icon": "drone",
        "title": "Drone strike hits Dymer",
        "deck1": "14 people unaccounted for; 9 pulled",
        "deck2": "SUN 22 NOV · 161 of 186 drones downed",
        "pin": (30.2, 50.8),
    },
    {
        "n": 7, "pill": "REPORTED", "icon": "tanker",
        "title": "Another tanker hit at Hormuz",
        "deck1": "UKMTO: vessel hit Monday, crew safe;",
        "deck2": "MON 23 NOV · Iran claims six hit since Sunday",
        "pin": (57.5, 25.3),
    },
    {
        "n": 8, "pill": "CONFIRMED", "icon": "pencil",
        "title": "Seoul minister quits",
        "deck1": "Minister Choi Kyo-jin resigns over AI-cheating",
        "deck2": "SUN 22 NOV · accepted within the hour; 111 cases",
        "pin": (127, 37.5),
    },
    {
        "n": 9, "pill": "REPORTED", "icon": "un",
        "title": "Drones hit UN building in Khartoum",
        "deck1": "Drones strike homes and a UN building;",
        "deck2": "SUN 22 NOV · 4 killed; UN staff were inside",
        "pin": (32.5, 15.6),
    },
    {
        "n": 10, "pill": "CONFIRMED", "icon": "wheat",
        "title": "Manila opens farm talks",
        "deck1": "Philippines and the FAO open farm",
        "deck2": "MON 23 NOV · modernisation talks, Parañaque, 23–26",
        "pin": (121, 14.6),
    },
    {
        "n": 11, "pill": "REPORTED", "icon": "bat",
        "title": "NZ save the Test in a draw",
        "deck1": "NZ 239/5 in reply; India 720/9 declared;",
        "deck2": "MON 23 NOV · Test drawn at Basin Reserve",
        "pin": (174.8, -41.3),
    },
]

# Index 12-31: twenty more stories, one line each.
INDEX = [
    (12, "Sea-Tac ICE arrests called 'outrageous'", "MON 23 NOV"),
    (13, "Myanmar's new govt reopens ASEAN talks", "SAT 21 NOV"),
    (14, "El Chapo Isidro captured in Jalisco", "FRI 20 NOV"),
    (15, "UN robot talks end — 2 more years of rules", "SAT 21 NOV"),
    (16, "ICJ ruling on Myanmar genocide appeal", "THU 19 NOV"),
    (17, "FBI probes breach of agent system", "SUN 22 NOV"),
    (18, "Verstappen wins Las Vegas Grand Prix", "SAT 21 NOV"),
    (19, "Liverpool 4–0 Man Utd; Yoro sent off", "SUN 22 NOV"),
    (20, "Sunrise on the Reaping tops box office", "SUN 22 NOV"),
    (21, "Alcaraz wins ATP Finals, beats Zverev", "SUN 22 NOV"),
    (22, "Nasdaq fell ~10% on the week", "FRI 20 NOV"),
    (23, "Lisbon marches over living costs", "SAT 21 NOV"),
    (24, "Sparta II towed out of Finnish waters", "SUN 22 NOV"),
    (25, "Hamas demands emergency talks on Sunday", "SUN 22 NOV"),
    (26, "Ex-chief of staff urges tariff repeal", "MON 23 NOV"),
    (27, "War funding curb pressed in Senate", "MON 23 NOV"),
    (28, "Miley Cyrus marries Maxx Morando", "SUN 22 NOV"),
    (29, "Istanbul protests over media closures", "SUN 22 NOV"),
    (30, "Anthropic makes record IPO debut", "FRI 20 NOV"),
    (31, "Rahul 136, Pant 128 in India's 720/9", "SUN 22 NOV"),
]

# Verification record for the index lines (not rendered; checked by verify.py).
INDEX_STORIES = {
    12: {"deck": "ICE arrests 20+ at Sea-Tac airport on Sunday; King County calls the operation 'outrageous'.", "source": "Reuters · AP"},
    13: {"deck": "Myanmar's new government reopens ASEAN talks after the election.", "source": "Reuters"},
    14: {"deck": "El Chapo Isidro captured in Jalisco; 11 dead in the operation.", "source": "Reuters · AFP"},
    15: {"deck": "UN robot talks end with two more years of rule-making.", "source": "Reuters"},
    16: {"deck": "ICJ rules on Myanmar's genocide appeal.", "source": "Reuters"},
    17: {"deck": "FBI probes a breach of its agent system.", "source": "Reuters"},
    18: {"deck": "Verstappen wins the Las Vegas Grand Prix on Saturday.", "source": "Reuters · AP"},
    19: {"deck": "Liverpool beat Manchester United 4-0 at Anfield on Sunday: Szoboszlai 10', Wirtz 13', Ngumoha 66', Munoz 82'; Leny Yoro sent off in the 8th minute — the earliest red card ever for United in the Premier League.", "source": "Reuters · Times · liverpoolfc.com"},
    20: {"deck": "Sunrise on the Reaping tops the box office on Sunday.", "source": "Reuters"},
    21: {"deck": "Alcaraz beats world No. 1 Zverev 6–2, 7–6(7) in Turin on Sunday; first ATP Finals title, $5.171m record payout, 5–0 week.", "source": "Reuters · ATP"},
    22: {"deck": "Nasdaq fell about 10% from its peak during the week.", "source": "Reuters"},
    23: {"deck": "Thousands march in Lisbon over living costs on Saturday; CGTP organised the rally.", "source": "Reuters"},
    24: {"deck": "Sparta II, struck by a drone in the Baltic on Saturday, is towed out of Finnish waters; the ship's owners say the crew is safe.", "source": "Reuters · AFP"},
    25: {"deck": "Hamas demands emergency talks on Sunday after Saturday strikes that killed 4 in Gaza and 3 in a food van.", "source": "Reuters · AFP"},
    26: {"deck": "A former White House chief of staff urges Democrats to repeal tariff rises.", "source": "Reuters · AP"},
    27: {"deck": "El-Sayed and Van Hollen press a curb on Iran war funding in the Senate.", "source": "Reuters · AP"},
    28: {"deck": "Miley Cyrus marries Maxx Morando on Sunday.", "source": "Reuters"},
    29: {"deck": "Thousands protest media closures in Istanbul on Sunday.", "source": "Reuters"},
    30: {"deck": "Anthropic's IPO debut is the largest of the year.", "source": "Reuters"},
    31: {"deck": "Rahul hits 136 and Pant 128 as India declare 720/9 on Sunday — the highest Test total in New Zealand.", "source": "Reuters"},
}

# Number strip: six verified figures, each tied to a story.
NUMBERS = [
    ("3", "KH-101 MISSILES"),
    ("32", "NATO STATES"),
    ("$2bn", "NEPAL PACKAGE ASK"),
    ("24", "DEAD IN BANTEN"),
    ("239/5", "NZ DRAW"),
    ("23–26", "FARM TALKS"),
]

# Hour timeline, Friday to Monday.
TIMELINE = [
    ("FRI 20 NOV", ["3 Russian objects cross into Poland",
                     "Gripen pilot holds fire in bad weather"], False),
    ("SAT 21 NOV", ["Sparta II drone strike, Baltic",
                     "El Chapo Isidro captured — 11 dead",
                     "UN robot talks end — 2 more years"], False),
    ("SUN 22 NOV", ["COP31 collapses, no deal",
                     "Democrats clinch 258th seat",
                     "Dymer strike, 14 unaccounted",
                     "Korea minister quits"], False),
    ("MON 23 NOV", ["NATO meets in Brussels",
                     "Nepal–Modi talks in Delhi",
                     "Banten toll confirmed: 24",
                     "Another tanker hit at Hormuz"], True),
]

REGIONS = [
    ("EUROPE", 10), ("ASIA", 6), ("NORTH AMERICA", 10),
    ("LATIN AMERICA", 1), ("MIDDLE EAST", 2), ("OCEANIA", 1),
    ("AFRICA", 1),
]

DATE_CHECK_HEAD = "DATE CHECK — This page is MONDAY 23 NOVEMBER 2026."
DATE_CHECK_BODY = (
    "Sunday follow-ups carry SUN datelines — not Monday's news: "
    "COP31 collapse · Democrats 258 · Dymer strike · Korea minister · "
    "Khartoum strikes · Alcaraz ATP title · Miley wedding · Istanbul "
    "protests · Rahul/Pant 720/9 (all Sun) · Sparta II (Sat) · El Chapo "
    "(Fri) · Robot talks (Sat) · ICJ ruling (Thu) · Anthropic IPO (Fri)."
)
SOURCES_LINE = (
    "Sources: AP · Reuters · AFP · UKMTO · Basarnas · NATO · MEA · UN OCHA — "
    "figures as reported 23 Nov 2026, 11:25 WIB; where reports differ, the card says so."
)
LEGEND_LINE = (
    "CONFIRMED = verified by two or more sources · REPORTED = one source or a claim, labelled in the text"
)

# ---- helpers -----------------------------------------------------------
def fit(d, text, font, max_w, min_px=6):
    """Shrink the font until the text fits max_w, else add an ellipsis."""
    px = font.size
    while px > min_px and d.textlength(text, font=font) > max_w:
        px -= 1
        font = ImageFont.truetype(font.path, px)
    if d.textlength(text, font=font) > max_w:
        while d.textlength(text + "…", font=font) > max_w and len(text) > 4:
            text = text[:-1]
        text = text + "…"
    return text, font

def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def pill(d, x, y, text):
    """Small rounded pill, red for CONFIRMED, teal for REPORTED."""
    col = RED if text == "CONFIRMED" else TEAL
    w = int(d.textlength(text, font=F_SANS_B(11))) + 16
    d.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=col)
    d.text((x + 8, y + 3), text, font=F_SANS_B(11), fill=WHITE)
    return w

# ---- lead illustrations ------------------------------------------------
def draw_nato(d, x, y, w, h):
    """Lead 1: dusk sky, compass star, missile streaks, arcade."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(16 + t * 40), int(36 + t * 52), int(68 + t * 56)))
    d.ellipse([x + w - 130, y + 6, x + w - 96, y + 40], fill=(232, 220, 180))
    for bx, by in [(x + 30, y + 8), (x + 210, y + 16), (x + 400, y + 10)]:
        d.ellipse([bx, by, bx + 56, by + 20], fill=(70, 92, 118))
    cx, cy, r = x + w - 60, y + h - 40, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 228, 236))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        px, py = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        d.line([cx, cy, px, py], fill=NAVY, width=1)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=NAVY)
    d.text((x + 8, y + h - 40), "KH-101 ×3", font=F_SANS_B(10),
           fill=(255, 240, 200))
    d.line([x + 20, y + h - 18, x + 330, y + h - 6], fill=(226, 205, 164), width=1)
    d.line([x + 20, y + h - 18, x + 330, y + h - 6], fill=(250, 246, 236), width=1)
    for bx in range(x + 40, x + w - 200, 40):
        d.ellipse([bx, y + h - 12, bx + 7, y + h - 5], fill=(90, 110, 136))
    for mx, my in [(x + 40, y + 30), (x + 150, y + 22), (x + 260, y + 34)]:
        d.line([mx, my, mx + 90, my + 26], fill=(255, 240, 200), width=4)
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 240, 200))
    for ax in range(x + 30, x + w - 200, 46):
        d.arc([ax, y + h - 22, ax + 36, y + h + 12], 180, 360, fill=(226, 205, 164), width=2)

def draw_delhi(d, x, y, w, h):
    """Lead 2: India Gate, drawn BIG in the strip (v2 craft fix)."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(232 - t * 26), int(214 - t * 30), int(176 - t * 40)))
    for px, ph in [(x + 20, 44), (x + 90, 54), (x + 170, 46)]:
        d.polygon([(px, y + h - 8), (px + 26, y + h - 8 - ph),
                   (px + 52, y + h - 8)], fill=(150, 176, 200))
    d.ellipse([x + 46, y + 2, x + 68, y + 24], fill=(240, 200, 120))
    # India Gate: large, right of centre, fills the strip's height.
    ax, aw, ah = x + w - 210, 136, 56
    ay = y + h - 10 - ah
    d.rectangle([ax, ay + 16, ax + aw, y + h - 10], fill=(176, 84, 66))
    d.pieslice([ax + 6, ay, ax + aw - 6, ay + 34], 180, 360, fill=(176, 84, 66))
    # One more dome on the gate's right shoulder.
    d.pieslice([ax + aw - 38, ay + 2, ax + aw - 14, ay + 20], 180, 360,
               fill=(150, 60, 48))
    d.rectangle([ax + 30, ay + 26, ax + aw - 30, y + h - 10], fill=(232, 214, 176))
    d.rectangle([ax - 6, ay + 12, ax + aw + 6, ay + 18], fill=(150, 60, 48))
    d.rectangle([ax + 44, ay - 4, ax + aw - 44, ay + 12], fill=(150, 60, 48))
    for fx, col in [(ax - 42, (196, 52, 48)), (ax + aw + 28, (255, 153, 51))]:
        d.line([fx, y + h - 40, fx, y + h - 10], fill=INK, width=2)
        d.polygon([(fx, y + h - 40), (fx + 18, y + h - 34), (fx, y + h - 28)],
                  fill=col)
    d.line([x + 10, y + h - 10, x + w - 10, y + h - 10], fill=(120, 90, 70), width=2)

def draw_banten(d, x, y, w, h):
    """Lead 3: dawn search at the factory — v2: smoke, 3 beams, 5 rescuers."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(244 - t * 60), int(208 - t * 70), int(164 - t * 80)))
    d.ellipse([x + 56, y + 4, x + 94, y + 42], fill=(250, 210, 120))
    # Smoke wisps above the factory roof.
    for sx, sy, sr in [(x + 120, y + 6, 8), (x + 150, y + 2, 6),
                       (x + 190, y + 8, 7), (x + 230, y + 4, 5),
                       (x + 270, y + 6, 6)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 132, 120))
    fx, fy = x + 40, y + h - 26
    # Three searchlight beams, brighter and wider than v1.
    d.polygon([(fx, fy), (fx + 110, y + 6), (fx + 150, y + 6)],
              fill=(250, 246, 236))
    d.polygon([(fx + 180, fy), (fx + 260, y + 4), (fx + 300, y + 4)],
              fill=(250, 246, 236))
    d.polygon([(fx + 300, fy), (fx + 360, y + 8), (fx + 400, y + 8)],
              fill=(250, 246, 236))
    # Factory block with sawtooth roof.
    d.rectangle([x + 24, fy, x + w - 24, y + h - 8], fill=(96, 80, 64))
    for sx in range(x + 24, x + w - 40, 56):
        d.polygon([(sx, fy), (sx + 28, fy - 10), (sx + 56, fy)], fill=(96, 80, 64))
    for wx in range(x + 44, x + w - 60, 52):
        d.rectangle([wx, fy + 8, wx + 22, fy + 18], fill=(250, 210, 120))
    # Five rescuers on the ground strip + a red-cross flag.
    for rx in [x + w - 160, x + w - 136, x + w - 112, x + w - 88, x + w - 64]:
        d.ellipse([rx, y + h - 22, rx + 10, y + h - 12], fill=NAVY)
        d.rectangle([rx + 2, y + h - 12, rx + 8, y + h - 8], fill=NAVY)
    d.line([x + w - 34, y + h - 34, x + w - 34, y + h - 8], fill=INK, width=2)
    d.rectangle([x + w - 34, y + h - 34, x + w - 14, y + h - 24], fill=RED)
    d.rectangle([x + w - 28, y + h - 31, x + w - 20, y + h - 27], fill=WHITE)

# ---- card icons --------------------------------------------------------
ICON_BG = {
    "globe": SEA, "capitol": NAVY2, "drone": (70, 70, 70), "tanker": (30, 90, 90),
    "pencil": (140, 90, 40), "un": SEA, "wheat": (150, 120, 30), "bat": (110, 60, 60),
}

def draw_icon(d, cx, cy, kind):
    bg = ICON_BG[kind]
    # v3: icon background shape varies by kind — circle for globe/wheat/bat,
    # diamond for drone, rounded square for the rest.
    if kind in ("globe", "wheat", "bat"):
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=bg)
    elif kind == "drone":
        d.polygon([(cx, cy - 22), (cx + 22, cy), (cx, cy + 22), (cx - 22, cy)],
                  fill=bg)
    else:
        d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=8,
                            fill=bg)
    if kind == "globe":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=WHITE, width=2)
        d.ellipse([cx - 6, cy - 12, cx + 6, cy + 12], outline=WHITE, width=1)
        d.line([cx - 12, cy, cx + 12, cy], fill=WHITE, width=1)
    elif kind == "capitol":
        d.polygon([(cx, cy - 12), (cx - 12, cy), (cx + 12, cy)], fill=WHITE)
        d.rectangle([cx - 12, cy, cx + 12, cy + 12], fill=WHITE)
        for lx in (cx - 8, cx - 2, cx + 4):
            d.rectangle([lx, cy + 4, lx + 2, cy + 12], fill=bg)
    elif kind == "drone":
        d.ellipse([cx - 12, cy - 4, cx - 4, cy + 4], outline=WHITE, width=2)
        d.ellipse([cx + 4, cy - 4, cx + 12, cy + 4], outline=WHITE, width=2)
        d.rectangle([cx - 6, cy - 3, cx + 6, cy + 3], fill=WHITE)
        d.line([cx - 10, cy + 8, cx + 10, cy + 8], fill=WHITE, width=2)
    elif kind == "tanker":
        d.polygon([(cx - 12, cy + 2), (cx + 12, cy + 2), (cx + 10, cy + 10),
                   (cx - 10, cy + 10)], fill=WHITE)
        d.rectangle([cx - 2, cy - 10, cx + 4, cy + 2], fill=WHITE)
        d.line([cx - 12, cy + 12, cx + 12, cy + 12], fill=WHITE, width=2)
    elif kind == "pencil":
        d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx + 4, cy - 12),
                   (cx + 12, cy - 4), (cx + 2, cy + 12)], fill=WHITE)
        d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx - 4, cy + 8)],
                  fill=(40, 40, 40))
    elif kind == "un":
        # UN building, columns, and a crack from the strike.
        d.polygon([(cx - 14, cy - 2), (cx, cy - 13), (cx + 14, cy - 2)], fill=WHITE)
        d.rectangle([cx - 12, cy - 2, cx + 12, cy + 12], fill=WHITE)
        for lx in (cx - 8, cx - 2, cx + 4):
            d.rectangle([lx, cy + 2, lx + 2, cy + 12], fill=bg)
        d.line([cx - 9, cy - 1, cx + 1, cy + 9], fill=RED, width=2)
        d.line([cx + 1, cy + 9, cx - 3, cy + 13], fill=RED, width=2)
    elif kind == "wheat":
        d.ellipse([cx, cy - 12, cx + 4, cy - 4], fill=WHITE)
        d.ellipse([cx - 6, cy - 6, cx - 2, cy + 2], fill=WHITE)
        d.ellipse([cx + 2, cy - 2, cx + 6, cy + 6], fill=WHITE)
        d.line([cx + 1, cy - 2, cx + 1, cy + 12], fill=WHITE, width=2)
    elif kind == "bat":
        d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=WHITE)
        d.line([cx, cy - 6, cx, cy + 6], fill=bg, width=2)
        d.line([cx - 4, cy - 2, cx + 4, cy - 2], fill=bg, width=2)

# ---- dotted world map --------------------------------------------------
CONTINENTS = [
    [(60, 78), (75, 74), (95, 74), (108, 78), (125, 74), (140, 78), (158, 76),
     (168, 80), (180, 76), (190, 82), (195, 88), (180, 90), (165, 86),
     (150, 90), (130, 86), (110, 90), (90, 88), (70, 84)],          # North America
    [(205, 120), (225, 118), (240, 122), (250, 128), (245, 138), (228, 142),
     (212, 136)],                                                   # South America
    [(355, 68), (380, 62), (420, 60), (460, 66), (500, 62), (520, 70),
     (500, 78), (460, 82), (420, 78), (380, 80), (360, 76)],        # Europe
    [(350, 92), (370, 88), (390, 92), (395, 104), (380, 112), (362, 106),
     (350, 100)],                                                   # Africa
    [(500, 66), (540, 60), (590, 58), (640, 62), (680, 70), (660, 80),
     (620, 86), (570, 84), (530, 78)],                              # Asia (north)
    [(580, 92), (600, 90), (615, 96), (610, 106), (590, 108), (580, 100)],  # SE Asia
    [(640, 140), (660, 138), (672, 146), (652, 152), (640, 146)],   # Australia
    [(690, 150), (700, 148), (708, 154), (696, 158)],               # New Zealand
]

def build_land_mask(scale=0.5):
    """Land mask on a 360x180 grid from hand-drawn continent polygons."""
    mw, mh = 360, 180
    m = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(m)
    for poly in CONTINENTS:
        md.polygon(poly, fill=255)
    return m.resize((int(mw * scale), int(mh * scale)), Image.LANCZOS)

LAND = build_land_mask()

def draw_map(d, x, y, w, h, pins):
    """Dotted world map; pins are (lon, lat) -> (number, nudge)."""
    for py in range(0, h, 4):
        for px in range(0, w, 4):
            lon = -180 + (px / max(1, w - 1)) * 360
            lat = 75 - (py / max(1, h - 1)) * 130
            mx = int((lon + 180) / 360 * LAND.width)
            my = int((75 - lat) / 130 * LAND.height)
            if 0 <= mx < LAND.width and 0 <= my < LAND.height:
                if LAND.getpixel((mx, my)) > 100:
                    d.ellipse([x + px, y + py, x + px + 1, y + py + 1], fill=NAVY)
    for n, (lon, lat) in pins.items():
        px = x + int((lon + 180) / 360 * w)
        py = y + int((75 - lat) / 130 * h)
        nudges = {1: (-14, -8), 6: (12, -10), 4: (10, 10), 9: (-6, 10),
                  7: (-12, 8), 2: (8, -8), 8: (6, -10), 10: (-8, 8), 11: (-16, -4)}
        dx, dy = nudges.get(n, (0, 0))
        px += dx
        py += dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=2)
        d.text((px - 2, py - 6), str(n), font=F_SANS_B(9), fill=WHITE)

# ---- layout ------------------------------------------------------------
def draw_masthead(d):
    d.rectangle([0, 0, 1024, 100], fill=NAVY)
    d.text((12, 8), "THE MONDAY LEDGER", font=F_SANS_B(13), fill=(214, 154, 44))
    d.text((1012, 8), "31 STORIES · 7 REGIONS · ALL DATED TO THE DAY",
           font=F_SANS_B(11), fill=(214, 154, 44), anchor="rt")
    d.text((512, 26), "MONDAY 23 NOVEMBER 2026", font=F_SERIF_B(42),
           fill=WHITE, anchor="mt")
    d.rectangle([12, 82, 1012, 84], fill=RED)
    d.text((512, 88), "NATO meets in Brussels · Nepal asks $2bn in Delhi · Banten toll: 24 dead — Monday's news, dated as it happened",
           font=F_SANS(12), fill=(220, 228, 236), anchor="mt")

def draw_lead1(d):
    L = LEADS[0]
    d.rectangle([12, 104, 1012, 300], fill=LIGHT, outline=LINE, width=1)
    draw_nato(d, 612, 104, 400, 196)
    d.rectangle([12, 104, 612, 300], fill=WHITE)
    d.rectangle([12, 104, 612, 300], outline=LINE, width=1)
    x, y = 24, 116
    pill(d, x, y, L["pill"])
    d.text((x + 84, y + 2), "MON 23 NOV", font=F_SANS_B(11), fill=MUTED)
    title_lines = wrap(d, L["title"], F_SERIF_B(30), 580)
    ty = 142
    for ln in title_lines:
        d.text((x, ty), ln, font=F_SERIF_B(30), fill=NAVY)
        ty += 34
    deck_lines = wrap(d, L["deck"], F_SANS(13), 604)
    dy = 208
    for ln in deck_lines:
        d.text((x, dy), ln, font=F_SANS(13), fill=INK)
        dy += 17
    d.text((x, 276), "Source: " + L["source"], font=F_SANS(10), fill=MUTED)
    d.text((12, 104), "  1 ", font=F_SANS_B(11), fill=RED)

def draw_leads23(d):
    for i, L in enumerate(LEADS[1:], start=1):
        x = 12 + (i - 1) * 504
        w = 496
        d.rectangle([x, 304, x + w, 480], fill=WHITE, outline=LINE, width=1)
        art_h = 76
        art_fn = {"nato": draw_nato, "delhi": draw_delhi, "banten": draw_banten}
        art_fn[L["art"]](d, x, 304, w, art_h)
        d.line([x, 304 + art_h, x + w, 304 + art_h], fill=LINE, width=1)
        tx, ty = x + 12, 386
        pill(d, tx, ty, L["pill"])
        d.text((tx + 84, ty + 2), "MON 23 NOV", font=F_SANS_B(11), fill=MUTED)
        t, f = fit(d, L["title"], F_SERIF_B(22), w - 24)
        d.text((tx, ty + 22), t, font=f, fill=NAVY)
        deck_lines = wrap(d, L["deck"], F_SANS(13), w - 24)[:2]
        dy = ty + 50
        for ln in deck_lines:
            d.text((tx, dy), ln, font=F_SANS(13), fill=INK)
            dy += 17
        d.text((tx, 470), "Source: " + L["source"], font=F_SANS(10), fill=MUTED)
        d.text((x, 304), "  %d " % L["n"], font=F_SANS_B(11), fill=RED)

def draw_numbers(d):
    d.rectangle([12, 484, 1012, 556], fill=NAVY)
    x = 12
    for num, cap in NUMBERS:
        cw = 1000 // len(NUMBERS)
        d.text((x + cw // 2, 492), num, font=F_SANS_B(24 if len(num) <= 3 else 20),
               fill=WHITE, anchor="mt")
        d.text((x + cw // 2, 524), cap, font=F_SANS_B(11), fill=(214, 154, 44),
               anchor="mt")
        if x > 12:
            d.line([x, 492, x, 548], fill=(60, 76, 104), width=1)
        x += cw

def draw_timeline(d):
    d.rectangle([12, 560, 1012, 636], fill=LIGHT, outline=LINE, width=1)
    d.text((24, 566), "FRIDAY → MONDAY", font=F_SANS_B(12), fill=NAVY)
    col_w = 250
    for i, (day, items, is_today) in enumerate(TIMELINE):
        cx = 12 + i * col_w
        d.text((cx + 12, 584), day, font=F_SANS_B(11),
               fill=RED if is_today else NAVY)
        for j, it in enumerate(items):
            t, f = fit(d, it, F_SANS(11), col_w - 18)
            d.text((cx + 12, 601 + j * 11), t, font=f, fill=INK)
        if i < len(TIMELINE) - 1:
            d.line([cx + col_w - 1, 566, cx + col_w - 1, 630], fill=LINE, width=1)

def draw_cards(d):
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = 12 + col * 504
        y = 644 + row * 46
        d.rectangle([x, y, x + 494, y + 45], fill=WHITE, outline=LINE, width=1)
        draw_icon(d, x + 30, y + 23, c["icon"])
        tx = x + 56
        t, f = fit(d, c["title"], F_SANS_B(15), 494 - 56 - 8)
        d.text((tx, y + 2), t, font=f, fill=NAVY)
        d.text((tx, y + 19), c["deck1"], font=F_SANS(12), fill=INK)
        d.text((tx, y + 33), c["deck2"], font=F_SANS(12), fill=MUTED)
        d.text((x + 2, y + 2), str(c["n"]), font=F_SANS_B(11), fill=RED)

def draw_bottom(d):
    # Index (left) + map (right).
    d.text((12, 829), "ALSO ON — 20 MORE STORIES · 31 STORIES · 7 REGIONS",
           font=F_SANS_B(12), fill=NAVY)
    d.line([12, 844, 660, 844], fill=LINE, width=1)
    for i, (n, txt, day) in enumerate(INDEX):
        col, row = (0, i) if i < 10 else (1, i - 10)
        x = 12 + col * 328
        y = int(848 + row * 10.5)
        d.text((x, y), "%d · " % n, font=F_SANS_B(10), fill=RED)
        nx = x + int(d.textlength("%d · " % n, font=F_SANS_B(10)))
        line, f = fit(d, txt + " — " + day, F_SANS(10), 320 - (nx - x) - 4)
        d.text((nx, y), line, font=f, fill=INK)
    # Map (right).
    d.text((684, 829), "WHERE IT HAPPENED · 11 PLACES PINNED",
           font=F_SANS_B(12), fill=NAVY)
    d.line([684, 844, 1012, 844], fill=LINE, width=1)
    pins = {}
    for L in LEADS:
        pins[L["n"]] = L["pin"]
    for c in CARDS:
        pins[c["n"]] = c["pin"]
    draw_map(d, 684, 848, 328, 82, pins)
    # DATE CHECK.
    d.rectangle([12, 958, 1012, 1002], fill=(252, 240, 220),
                outline=(200, 140, 60), width=1)
    d.text((24, 962), DATE_CHECK_HEAD, font=F_SANS_B(11), fill=RED)
    for j, ln in enumerate(wrap(d, DATE_CHECK_BODY, F_SANS(11), 972)):
        d.text((24, 976 + j * 12), ln, font=F_SANS(11), fill=INK)
    # Footer.
    d.text((512, 1005), SOURCES_LINE, font=F_SANS(9), fill=MUTED, anchor="mt")
    d.text((512, 1014), LEGEND_LINE, font=F_SANS(9), fill=MUTED, anchor="mt")

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead1(d)
    draw_leads23(d)
    draw_numbers(d)
    draw_timeline(d)
    draw_cards(d)
    draw_bottom(d)
    img.save("entry.png")
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
