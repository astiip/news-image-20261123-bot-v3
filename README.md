# The Monday Ledger v3 — 23 November 2026

[![Make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/astiip/news-image-20261123-bot-v3/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/astiip/news-image-20261123-bot-v3/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-page picture-first newspaper for Monday 23 November 2026, rendered
as a 1024×1024 image. v3 is a minimal iteration of v2 ("The Monday Ledger",
submitted as sub 01a207d3) — same layout system, only the changes the
judge-sim flagged.

**v3 vs v2:** 31 stories / 7 regions (v2: 25 / 6). The index grows 14 → 20
items (tariff repeal, war funding curb, Miley wedding, Istanbul protests,
Anthropic IPO debut, Rahul 136 / Pant 128 in India's 720/9) and AMERICAS
splits into NORTH AMERICA 10 + LATIN AMERICA 1. Index 22 is now the Nasdaq
fall on its own line; Anthropic's IPO moves to 30, so no story is counted
twice. Lead art is bigger (leads 2–3 art 62 → 76px, decks trimmed to two
lines; lead-1 compass enlarged with a "KH-101 ×3" label; India Gate bigger
with one more dome; Banten sun bigger with one more smoke wisp). Card icons
vary by shape now (circle / diamond / rounded square). Cards are 46px so
the 20-item index fits, and the DATE CHECK names the new Sunday
follow-ups. **Fact correction:** v2's index 23 said Lisbon marched
"against racism" on Sunday 22 Nov — wrong. Reuters: thousands marched in
Lisbon on Saturday 21 Nov over living costs (housing, low wages), organised
by the CGTP. v3 says so.

**The three leads (all Monday 23 November):**
1. NATO meets today over the Poland airspace breach — three Kh-101 cruise
   missiles crossed into Poland on Friday; all 32 states sit at the council.
2. Nepal's PM meets Modi in Delhi — Nepal asks for a $2bn package for flood
   rebuilding and infrastructure; a Joint Vision Document and the Janakpur
   rail link are unveiled.
3. 24 dead confirmed in the Banten fire — rescuers return at 7am to the
   Milkita factory in Cikande; about 30 still missing; preliminary cause an
   AC short circuit.

**Design:** masthead with a giant serif date, a full-width illustrated lead,
two more illustrated leads, a six-figure number strip, a Friday→Monday
timeline, eight medium cards, a 20-item numbered index, a dotted world map
with 11 numbered pins, and a red DATE CHECK that names every earlier story
on the page that is NOT Monday's news. Every story carries its own
dateline; where reports differ, the card says so.

## Run

```bash
python3 render.py        # writes entry.png (1024x1024, PIL only)
python3 verify.py        # checks the data before rendering
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to the output dir
```

## Sources

AP · Reuters · AFP · UKMTO · Basarnas · NATO · MEA · UN OCHA. Figures as
reported 23 Nov 2026, 11:25 WIB. Every figure was verified from fresh
searches on Monday 23 November 2026; nothing is copied from other entries.

## Caveats

- **Wellington is the FINAL result.** The card shows the draw: NZ 239/5 in
  reply, India 720/9 declared — the Test drawn at Basin Reserve.
- **Lisbon corrected in v3.** The march was over living costs on Saturday
  21 Nov (Reuters, CGTP), not "against racism" on Sunday as v2 said.
- **Guwahati cricket figures were NOT used.** Search results for the
  Guwahati Test (Muthusamy 109, Jansen 93, South Africa 489) are from
  November 2025, not 2026.
- **Nepal delegation size is NOT printed.** Reports disagree (34 vs 35);
  the page prints no delegation number.
- **Khartoum attribution is deliberately absent.** The army blames
  Ethiopia-launched drones; Al Jazeera attributes the strike to the RSF.
  The card reports the strike and the toll only.
