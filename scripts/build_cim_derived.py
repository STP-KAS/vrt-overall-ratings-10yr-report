"""Build derived CSVs from locally cached CIM pages.

Usage:  python scripts/build_cim_derived.py --cache PATH_TO_CIM_CACHE
The cache must contain raw/YYYY-MM-DD.html (CIM daily Top 20, region North) and
raw_yearly/{market_shares,yearly_top_100}_YYYY.html, as fetched with the CIM AJAX endpoint
(POST https://www.cim.be/nl/tv-media-response). The cache is not committed (CIM terms; size).
Outputs go to data/."""
import argparse, csv, os, collections, re
import cimlib

CIM = "https://www.cim.be/nl/televisie"
ap = argparse.ArgumentParser(); ap.add_argument("--cache", required=True); a = ap.parse_args()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(OUT, exist_ok=True)

def write(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", name, len(rows))

# ---------- 1. CIM yearly market shares (4+, full day 02-26h), 2018-2025, every listed channel ----------
ms = []
for y in range(2017, 2026):
    p = os.path.join(a.cache, "raw_yearly", f"market_shares_{y}.html")
    rows = [c for c in cimlib.cells_of(open(p, encoding="utf-8").read())[1:] if len(c) >= 3]
    for c in rows:
        ms.append(dict(year=y, channel_as_listed_by_cim=c[1], group=cimlib.group_of(c[1]),
                       share_pct_4plus_fullday=round(int(c[2]) / 100, 2),
                       metric="Market share (marktaandeel), total population 4+, full day 02:00-26:00",
                       source="CIM TV yearly market shares (region North), as published on cim.be",
                       source_url=f"{CIM} (tab Marktaandelen, jaar {y}, regio Noord)",
                       notes="value published in basis points (e.g. 3036 = 30.36%)"))
    if not rows:
        print("no market-share rows for", y)
write("cim_yearly_market_share_by_channel.csv", ms)

grp = collections.defaultdict(float); listed = collections.defaultdict(float)
for r in ms:
    grp[(r["year"], r["group"])] += r["share_pct_4plus_fullday"]; listed[r["year"]] += r["share_pct_4plus_fullday"]
gs = []
for (y, g), v in sorted(grp.items()):
    gs.append(dict(year=y, group=g, share_pct=round(v, 2), method="own calculation: sum of CIM channel shares in group",
                   source_url=f"{CIM} (tab Marktaandelen, jaar {y}, regio Noord)",
                   notes=f"CIM lists channels covering {listed[y]:.2f}% of viewing in {y}; 'Other' = listed non-group channels only"))
write("cim_yearly_market_share_by_group_owncalc.csv", gs)

# ---------- 2. CIM yearly Top 100 programmes, 2018-2025 ----------
top = []; t100 = []
for y in range(2018, 2026):
    p = os.path.join(a.cache, "raw_yearly", f"yearly_top_100_{y}.html")
    rows = [c for c in cimlib.cells_of(open(p, encoding="utf-8").read())[1:] if len(c) == 6 and c[0].isdigit()]
    rows = [c for c in rows if int(c[0]) <= 100]
    cnt = collections.Counter(cimlib.group_of(c[3]) for c in rows)
    for rk, prog, typ, ch, date, v in rows[:5]:
        top.append(dict(year=y, rank=int(rk), programme=prog, genre_cim=typ, channel=ch, group=cimlib.group_of(ch),
                        broadcast_date=date, viewers=cimlib.thousands(v),
                        source="CIM TV yearly Top 100 (region North, 4+); published in thousands",
                        source_url=f"{CIM} (tab Top 100 jaar, jaar {y}, regio Noord)"))
    for g in ["VRT", "DPG Media (VTM family)", "Play Media (SBS/Play family)", "Other", "Joint simulcast (several groups)"]:
        t100.append(dict(year=y, group=g, entries_in_top100=cnt.get(g, 0), n_entries=len(rows),
                         method="own calculation: count of CIM yearly Top 100 entries by channel group",
                         source_url=f"{CIM} (tab Top 100 jaar, jaar {y}, regio Noord)"))
write("cim_yearly_top5_programmes.csv", top)
write("cim_yearly_top100_entries_by_group_owncalc.csv", t100)

# ---------- 3. CIM daily Top 20 (2016-10-01 .. latest cached day) ----------
days = collections.defaultdict(list)
for d, rk, prog, ch, v in cimlib.daily_rows(a.cache):
    days[d].append((rk, prog, ch, v))
by_year = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
n1 = collections.defaultdict(collections.Counter); ndays = collections.Counter(); best = {}
first, last = min(days), max(days)
for d, lst in days.items():
    seen = set(); clean = []
    for rk, prog, ch, v in sorted(lst):
        k = (prog, ch, v)
        if k in seen: continue  # 2018-04-01 page lists every row twice
        seen.add(k); clean.append((rk, prog, ch, v))
    clean = clean[:20]  # some spring-2022 days list a Top 25
    y = int(d[:4]); ndays[y] += 1
    for i, (rk, prog, ch, v) in enumerate(clean):
        g = cimlib.group_of(ch)
        by_year[y][g][0] += 1; by_year[y][g][1] += v
        if i == 0: n1[y][g] += 1
        if y not in best or v > best[y][3]: best[y] = (d, prog, ch, v)
dt = []
for y in sorted(by_year):
    slots = sum(s for s, _ in by_year[y].values()); vw = sum(v for _, v in by_year[y].values())
    span = f"{max(first, f'{y}-01-01')}..{min(last, f'{y}-12-31')}"
    for g in ["VRT", "DPG Media (VTM family)", "Play Media (SBS/Play family)", "Other", "Joint simulcast (several groups)"]:
        s, v = by_year[y].get(g, [0, 0])
        dt.append(dict(year=y, period=span, days_with_data=ndays[y], group=g, top20_slots=s,
                       share_of_slots_pct=round(100 * s / slots, 1), summed_viewers=v,
                       share_of_top20_viewers_pct=round(100 * v / vw, 1),
                       days_ranked_no1=n1[y].get(g, 0), share_of_days_no1_pct=round(100 * n1[y].get(g, 0) / ndays[y], 1),
                       method="own calculation from CIM daily Top 20 (North, 4+); partial years flagged by 'period'",
                       source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord, every day in period)"))
write("cim_daily_top20_share_by_group_owncalc.csv", dt)
bt = [dict(year=y, date=b[0], programme=b[1], channel=b[2], viewers=b[3], period=dt[[r['year'] for r in dt].index(y)]["period"],
           method="own calculation: highest single entry in the CIM daily Top 20 within the period",
           source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord, {b[0]})") for y, b in sorted(best.items())]
write("cim_daily_top20_highest_entry_per_year_owncalc.csv", bt)
