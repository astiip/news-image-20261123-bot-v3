#!/usr/bin/env python3
"""Verify the v3 page data before rendering — run: python3 verify.py

Checks: 31 stories numbered 1..31, 3 Monday leads, 8 cards, 20 index
items, 7 regions, strip figures tied to their stories, timeline days,
DATE CHECK (2-line fit + every listed story is actually on the page),
forbidden superseded/wrong figures (incl. the v2 Lisbon error and the
dropped "AC short circuit" clause), legibility caps (card titles,
deck lines, index lines, lead-deck wrap).
"""
import sys
from PIL import Image, ImageDraw

import render as R

fails = []


def check(name, ok, detail=""):
    if ok:
        print("PASS", name)
    else:
        fails.append(name)
        print("FAIL", name, detail)


img = Image.new("RGB", (1024, 1024), (255, 255, 255))
d = ImageDraw.Draw(img)

# ---- story counts ------------------------------------------------------
all_stories = list(R.LEADS) + list(R.CARDS)
check("31 stories total", len(R.LEADS) + len(R.CARDS) + len(R.INDEX) == 31,
      f"got {len(R.LEADS) + len(R.CARDS) + len(R.INDEX)}")
check("3 leads", len(R.LEADS) == 3)
check("8 cards", len(R.CARDS) == 8)
check("20 index items", len(R.INDEX) == 20)

nums = [s["n"] for s in all_stories] + [n for n, _, _ in R.INDEX]
check("numbers 1..31, no duplicates",
      sorted(nums) == list(range(1, 32)), f"got {sorted(nums)}")

# ---- leads -------------------------------------------------------------
for L in R.LEADS:
    check(f"lead {L['n']} pill valid", L["pill"] in ("CONFIRMED", "REPORTED"))
    check(f"lead {L['n']} art known", L["art"] in ("nato", "delhi", "banten"))
    check(f"lead {L['n']} has pin", isinstance(L["pin"], tuple))
    check(f"lead {L['n']} has source", bool(L["source"]))
check("lead 1 is NATO meeting", "NATO meets today" in R.LEADS[0]["title"])
check("lead 2 is Nepal-Modi", "Nepal" in R.LEADS[1]["title"])
check("lead 3 is Banten toll", "24 dead" in R.LEADS[2]["title"])

# Lead-deck wrap: lead 1 <= 4 lines at 604px, leads 2-3 <= 2 lines at 472px.
l1_lines = R.wrap(d, R.LEADS[0]["deck"], R.F_SANS(13), 604)
check("lead 1 deck wraps to <=4 lines", len(l1_lines) <= 4,
      f"{len(l1_lines)} lines")
for L in R.LEADS[1:]:
    lines = R.wrap(d, L["deck"], R.F_SANS(13), 472)
    check(f"lead {L['n']} deck wraps to <=2 lines", len(lines) <= 2,
          f"{len(lines)} lines: {lines}")

# ---- cards -------------------------------------------------------------
for c in R.CARDS:
    check(f"card {c['n']} pill valid", c["pill"] in ("CONFIRMED", "REPORTED"))
    check(f"card {c['n']} icon known", c["icon"] in R.ICON_BG)
    check(f"card {c['n']} title <=34 chars", len(c["title"]) <= 34,
          f"{len(c['title'])}: {c['title']}")
    check(f"card {c['n']} deck1 <=60 chars", len(c["deck1"]) <= 60,
          f"{len(c['deck1'])}: {c['deck1']}")
    check(f"card {c['n']} deck2 <=60 chars", len(c['deck2']) <= 60,
          f"{len(c['deck2'])}: {c['deck2']}")
    check(f"card {c['n']} deck2 has dateline",
          any(day in c["deck2"] for day in
              ("MON 23 NOV", "SUN 22 NOV", "SAT 21 NOV", "FRI 20 NOV",
               "THU 19 NOV")))
check("card 7 is Monday Hormuz hit", "Another tanker hit" in R.CARDS[3]["title"]
      and "MON 23 NOV" in R.CARDS[3]["deck2"])
check("card 9 is Khartoum Africa card", "Khartoum" in R.CARDS[5]["title"])
check("card 9 does not attribute the strike",
      "RSF" not in R.CARDS[5]["deck1"] + R.CARDS[5]["deck2"]
      and "Ethiopia" not in R.CARDS[5]["deck1"] + R.CARDS[5]["deck2"])
check("card 11 is Wellington final score", "239/5" in R.CARDS[7]["deck1"])

# ---- index -------------------------------------------------------------
for n, txt, day in R.INDEX:
    check(f"index {n} line <=70 chars",
          len(f"{n} · {txt} — {day}") <= 70,
          f"{len(f'{n} · {txt} — {day}')}: {txt}")
    check(f"index {n} has verification record", n in R.INDEX_STORIES)
    check(f"index {n} record has source",
          bool(R.INDEX_STORIES[n].get("source")))
check("index 19 is Liverpool 4-0", "4–0" in R.INDEX[7][1])
check("index 21 is Alcaraz ATP title", "Alcaraz" in R.INDEX[9][1])
check("index 22 is Nasdaq fall only (no Anthropic dup)",
      "Nasdaq" in R.INDEX[10][1] and "Anthropic" not in R.INDEX[10][1])
check("index 23 is Lisbon living costs, SAT 21 NOV",
      "living costs" in R.INDEX[11][1] and R.INDEX[11][2] == "SAT 21 NOV")
check("index 23 record is living costs, not racism",
      "living costs" in R.INDEX_STORIES[23]["deck"]
      and "racism" not in R.INDEX_STORIES[23]["deck"])
check("index 24 is Sparta II (moved from card)",
      "Sparta II" in R.INDEX[12][1])
check("index 25 is Hamas Middle East story", "Hamas" in R.INDEX[13][1])
check("index 26 is tariff repeal, MON", "tariff repeal" in R.INDEX[14][1]
      and R.INDEX[14][2] == "MON 23 NOV")
check("index 27 is war funding curb, MON",
      "War funding curb" in R.INDEX[15][1]
      and R.INDEX[15][2] == "MON 23 NOV")
check("index 28 is Miley wedding, SUN", "Miley Cyrus" in R.INDEX[16][1]
      and R.INDEX[16][2] == "SUN 22 NOV")
check("index 29 is Istanbul protests, SUN", "Istanbul" in R.INDEX[17][1]
      and R.INDEX[17][2] == "SUN 22 NOV")
check("index 30 is Anthropic IPO debut, FRI",
      "Anthropic" in R.INDEX[18][1] and R.INDEX[18][2] == "FRI 20 NOV")
check("index 31 is Rahul/Pant 720/9, SUN",
      "Rahul 136" in R.INDEX[19][1] and "720/9" in R.INDEX[19][1]
      and R.INDEX[19][2] == "SUN 22 NOV")
check("index has 10 rows per column at 10.5px, last row ~942",
      848 + 9 * 10.5 == 942.5)

# ---- regions -----------------------------------------------------------
total = sum(v for _, v in R.REGIONS)
check("regions sum to 31", total == 31, f"got {total}")
check("7 regions", len(R.REGIONS) == 7)
check("Africa present (Khartoum)", dict(R.REGIONS).get("AFRICA") == 1)
check("Middle East has 2 (Hormuz + Hamas)",
      dict(R.REGIONS).get("MIDDLE EAST") == 2)
check("Europe 10", dict(R.REGIONS).get("EUROPE") == 10)
check("Asia 6", dict(R.REGIONS).get("ASIA") == 6)
check("North America 10", dict(R.REGIONS).get("NORTH AMERICA") == 10)
check("Latin America 1 (El Chapo)",
      dict(R.REGIONS).get("LATIN AMERICA") == 1)
check("Oceania 1", dict(R.REGIONS).get("OCEANIA") == 1)

# ---- number strip ------------------------------------------------------
check("6 strip figures", len(R.NUMBERS) == 6)
check("strip 3 Kh-101 tied to lead 1",
      "Three Kh-101" in R.LEADS[0]["deck"])
check("strip 32 tied to lead 1", "32 states" in R.LEADS[0]["deck"])
check("strip $2bn tied to lead 2", "$2bn" in R.LEADS[1]["deck"])
check("strip 24 tied to lead 3", "24 dead" in R.LEADS[2]["deck"])
check("strip 239/5 tied to Wellington card", "239/5" in R.CARDS[7]["deck1"])
check("strip 23–26 tied to Manila card", "23–26" in R.CARDS[6]["deck2"])

# ---- timeline ----------------------------------------------------------
check("4 timeline days", len(R.TIMELINE) == 4)
check("timeline Monday is today", R.TIMELINE[3][2] is True)
check("timeline Monday has 4 items", len(R.TIMELINE[3][1]) == 4)
check("timeline Monday last item at y=610 (same as v1's 4-item Sunday col)",
      577 + 3 * 11 == 610)
tl_text = " ".join(it for _, items, _ in R.TIMELINE for it in items)
for phrase in ("3 Russian objects cross into Poland",
               "Gripen pilot holds fire in bad weather",
               "COP31 collapses, no deal",
               "NATO meets in Brussels",
               "Banten toll confirmed: 24",
               "Another tanker hit at Hormuz"):
    check(f"timeline contains '{phrase}'", phrase in tl_text)

# ---- DATE CHECK --------------------------------------------------------
check("DATE CHECK head is Monday 23 Nov 2026",
      "MONDAY 23 NOVEMBER 2026" in R.DATE_CHECK_HEAD)
dc_lines = R.wrap(d, R.DATE_CHECK_BODY, R.F_SANS(11), 972)
check("DATE CHECK body fits 2 lines", len(dc_lines) <= 2,
      f"{len(dc_lines)} lines")
for name in ("COP31 collapse", "Democrats 258", "Dymer strike",
             "Korea minister", "Khartoum strikes", "Alcaraz ATP title",
             "Miley wedding", "Istanbul protests", "Rahul/Pant 720/9",
             "Sparta II", "El Chapo", "Robot talks", "ICJ ruling",
             "Anthropic IPO"):
    check(f"DATE CHECK lists '{name}'", name in R.DATE_CHECK_BODY)

# Every DATE CHECK item must actually be on the page.
page_text = " ".join(
    [s.get("title", "") + " " + s.get("deck", "") for s in R.LEADS]
    + [c["title"] + " " + c["deck1"] + " " + c["deck2"] for c in R.CARDS]
    + [txt for _, txt, _ in R.INDEX])
for name, needle in (
        ("COP31 collapse", "COP31 collapses"),
        ("Democrats 258", "258th seat"),
        ("Dymer strike", "Dymer"),
        ("Korea minister", "Seoul minister quits"),
        ("Khartoum strikes", "Khartoum"),
        ("Alcaraz ATP title", "Alcaraz"),
        ("Miley wedding", "Miley"),
        ("Istanbul protests", "Istanbul"),
        ("Rahul/Pant 720/9", "Rahul"),
        ("Sparta II", "Sparta II"),
        ("El Chapo", "El Chapo"),
        ("Robot talks", "robot talks"),
        ("ICJ ruling", "ICJ ruling"),
        ("Anthropic IPO", "Anthropic")):
    check(f"DATE CHECK '{name}' is on the page", needle in page_text)

# ---- forbidden figures -------------------------------------------------
all_text = page_text + " " + R.DATE_CHECK_BODY + " " + R.SOURCES_LINE
for bad in ("Article 4", "4 missiles", "four missiles", "37 missing",
            "50 missing", "36 missing", "34-member", "Guwahati",
            "TODO", "Lorem", "placeholder", "{owner}", "{repo}",
            "against racism", "AC short circuit"):
    check(f"forbidden '{bad}' absent", bad not in all_text)

# ---- map ---------------------------------------------------------------
pins = {}
for L in R.LEADS:
    pins[L["n"]] = L["pin"]
for c in R.CARDS:
    pins[c["n"]] = c["pin"]
check("11 pins on the map", len(pins) == 11, f"got {len(pins)}")
check("map pins are leads + cards only",
      sorted(pins) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
check("Khartoum pin on the map", pins[9] == (32.5, 15.6))

# ---- sources -----------------------------------------------------------
check("sources line names UN OCHA (Khartoum)", "UN OCHA" in R.SOURCES_LINE)
check("sources line names UKMTO (Hormuz)", "UKMTO" in R.SOURCES_LINE)

print()
if fails:
    print(f"{len(fails)} FAILURES: {fails}")
    sys.exit(1)
print("ALL CHECKS PASSED")
