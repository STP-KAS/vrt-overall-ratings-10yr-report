"""Absolute-viewer series (own calculation) from the locally cached CIM pages.

Usage: python scripts/build_absolute.py --cache PATH_TO_CIM_CACHE   (same cache as build_cim_derived.py)

IMPORTANT measurement break found in the cached daily Top 20: for dates up to late June 2023 the values are
same-day figures (Live+VOSDAL); from early July 2023 they equal CIM's consolidated figures (Live+7, and Live+28
incl. online from 1 Jul 2024). Evidence: data/cim_daily_vs_yearly_ratio_by_month_owncalc.csv. Every series below
is therefore split at BREAK_DATE and the two segments must not be compared directly."""
import argparse, csv, os, collections, statistics
import cimlib

BREAK_DATE = "2023-07-01"   # first segment: < BREAK_DATE (same-day); second: >= BREAK_DATE (consolidated)
CIM = "https://www.cim.be/nl/televisie"
ap = argparse.ArgumentParser(); ap.add_argument("--cache", required=True); a = ap.parse_args()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

def write(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", name, len(rows))

def chan(ch):
    c = ch.strip().upper()
    if c in ("EEN", "VRT1", "VRT 1"): return "Een / VRT 1"
    if c in ("CANVAS", "VRT CANVAS"): return "Canvas / VRT Canvas"
    if c == "KETNET": return "Ketnet"
    if c == "VTM": return "VTM (main channel)"
    if c in ("VIER", "PLAY4", "PLAY 4", "PLAY"): return "VIER / Play4 / PLAY (main channel)"
    return None

# ---- load + clean daily Top 20 (same cleaning as build_cim_derived.py) ----
raw = collections.defaultdict(list)
for d, rk, prog, ch, v in cimlib.daily_rows(a.cache):
    raw[d].append((rk, prog, ch, v))
days = {}
for d, lst in raw.items():
    seen = set(); clean = []
    for rk, prog, ch, v in sorted(lst):
        k = (prog, ch, v)
        if k in seen: continue
        seen.add(k); clean.append((rk, prog, ch, v))
    days[d] = clean[:20]
first, last = min(days), max(days)

def seg_of(d):
    y = d[:4]
    if y == "2023": return "2023 H1" if d < BREAK_DATE else "2023 H2"
    return y
def basis(s): return "same-day (Live+VOSDAL), as cached" if s < "2023 H2" else "consolidated (Live+7; Live+28 incl. online from 1 Jul 2024), as cached"

# ---- per segment x group ----
G = ["VRT", "DPG Media (VTM family)", "Play Media (SBS/Play family)"]
acc = collections.defaultdict(lambda: dict(days=0, present=0, top=[], entries=0, viewers=0, sum_per_day=[]))
seg_days = collections.Counter(); seg_span = {}
allday = collections.defaultdict(lambda: dict(no1=[], all=[]))
for d, lst in sorted(days.items()):
    s = seg_of(d); seg_days[s] += 1
    seg_span.setdefault(s, [d, d]); seg_span[s][1] = d
    allday[s]["no1"].append(lst[0][3]); allday[s]["all"] += [x[3] for x in lst]
    by = collections.defaultdict(list)
    for rk, prog, ch, v in lst: by[cimlib.group_of(ch)].append(v)
    for g in G:
        r = acc[(s, g)]; r["days"] += 1
        vals = by.get(g, [])
        r["sum_per_day"].append(sum(vals))
        if vals:
            r["present"] += 1; r["top"].append(max(vals)); r["entries"] += len(vals); r["viewers"] += sum(vals)
rows = []
for (s, g), r in sorted(acc.items()):
    rows.append(dict(period=s, date_from=seg_span[s][0], date_to=seg_span[s][1], cim_value_basis=basis(s), group=g,
        days=r["days"], days_group_in_top20=r["present"],
        avg_viewers_biggest_programme_of_day=round(statistics.mean(r["top"])) if r["top"] else "",
        median_viewers_biggest_programme_of_day=round(statistics.median(r["top"])) if r["top"] else "",
        avg_viewers_per_top20_entry=round(r["viewers"] / r["entries"]) if r["entries"] else "",
        avg_top20_entries_per_day=round(r["entries"] / r["days"], 2),
        avg_summed_top20_viewers_per_day=round(statistics.mean(r["sum_per_day"])),
        method="own calculation from CIM daily Top 20 (North, 4+ incl. guests); 'biggest programme of day' only over days the group has an entry",
        source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord, every day in period)"))
for s in sorted(allday):
    x = allday[s]
    rows.append(dict(period=s, date_from=seg_span[s][0], date_to=seg_span[s][1], cim_value_basis=basis(s), group="All channels (context)",
        days=seg_days[s], days_group_in_top20=seg_days[s],
        avg_viewers_biggest_programme_of_day=round(statistics.mean(x["no1"])), median_viewers_biggest_programme_of_day=round(statistics.median(x["no1"])),
        avg_viewers_per_top20_entry=round(statistics.mean(x["all"])), avg_top20_entries_per_day=round(len(x["all"]) / seg_days[s], 2),
        avg_summed_top20_viewers_per_day=round(sum(x["all"]) / seg_days[s]),
        method="own calculation from CIM daily Top 20 (North, 4+ incl. guests)", source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord, every day in period)"))
write("cim_daily_top20_absolute_by_group_owncalc.csv", rows)

# ---- per channel ----
cacc = collections.defaultdict(lambda: dict(entries=0, viewers=0, present=0, top=[]))
for d, lst in days.items():
    s = seg_of(d); by = collections.defaultdict(list)
    for rk, prog, ch, v in lst:
        c = chan(ch)
        if c: by[c].append(v)
    for c, vals in by.items():
        r = cacc[(s, c)]; r["entries"] += len(vals); r["viewers"] += sum(vals); r["present"] += 1; r["top"].append(max(vals))
crow = []
for (s, c), r in sorted(cacc.items()):
    crow.append(dict(period=s, cim_value_basis=basis(s), channel=c, days=seg_days[s], days_channel_in_top20=r["present"],
        top20_entries=r["entries"], avg_top20_entries_per_day=round(r["entries"] / seg_days[s], 2),
        avg_viewers_per_top20_entry=round(r["viewers"] / r["entries"]),
        avg_viewers_biggest_programme_of_day=round(statistics.mean(r["top"])),
        method="own calculation from CIM daily Top 20 (North, 4+ incl. guests); averages only over the channel's own Top-20 entries",
        source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord, every day in period)"))
write("cim_daily_top20_absolute_by_channel_owncalc.csv", crow)

# ---- evidence for the break: daily value / yearly Top-100 value for the same programme+date ----
daily = {}
for d, lst in days.items():
    for rk, prog, ch, v in lst: daily.setdefault((d, prog.strip().upper()), v)
ratio = collections.defaultdict(list)
t10 = []
for y in range(2018, 2026):
    p = os.path.join(a.cache, "raw_yearly", f"yearly_top_100_{y}.html")
    rows100 = [c for c in cimlib.cells_of(open(p, encoding="utf-8").read())[1:] if len(c) == 6 and c[0].isdigit() and int(c[0]) <= 100]
    by = collections.defaultdict(list); best = {}
    for rk, prog, typ, ch, date, v in rows100:
        g0 = cimlib.group_of(ch)
        if g0 not in best: best[g0] = (prog, ch, date)
        if "All channels" not in best: best["All channels"] = (prog, ch, date)
        dd, mm, yy = date.split("/"); d = f"{yy}-{mm}-{dd}"
        if (d, prog.strip().upper()) in daily:
            ratio[d[:7]].append(daily[(d, prog.strip().upper())] / cimlib.thousands(v))
        by[cimlib.group_of(ch)].append(cimlib.thousands(v))
    allv = sorted([cimlib.thousands(c[5]) for c in rows100], reverse=True)
    for g in ["All channels"] + G:
        vals = allv if g == "All channels" else sorted(by.get(g, []), reverse=True)
        t10.append(dict(year=y, group=g, entries_in_top100=len(vals),
            avg_viewers_top10_entries=round(statistics.mean(vals[:10])) if len(vals) >= 10 else "fewer than 10 entries",
            best_entry_viewers=vals[0] if vals else "", best_entry_programme=best.get(g, ("", "", ""))[0],
            best_entry_channel=best.get(g, ("", "", ""))[1], best_entry_date=best.get(g, ("", "", ""))[2], avg_viewers_all_top100_entries_of_group=round(statistics.mean(vals)) if vals else "",
            cim_value_basis="CIM yearly Top 100: Live+7 incl. online (2018-H1 2024); Live+28 incl. online for broadcasts from 1 Jul 2024",
            method="own calculation from CIM yearly Top 100 (North, 4+); top-10 = the group's 10 biggest entries in the list",
            source_url=f"{CIM} (tab Top 100 jaar, jaar {y}, regio Noord)"))
write("cim_yearly_top100_absolute_owncalc.csv", t10)
write("cim_daily_vs_yearly_ratio_by_month_owncalc.csv",
      [dict(month=m, matched_programmes=len(r), mean_ratio_daily_to_yearly=round(statistics.mean(r), 3), min_ratio=round(min(r), 3), max_ratio=round(max(r), 3),
            method="own calculation: CIM daily Top-20 value / CIM yearly Top-100 value for the same programme title and date",
            source_url=f"{CIM} (daily Top 20 and yearly Top 100, regio Noord)") for m, r in sorted(ratio.items())])

# ---- same-period comparisons (seasonality-safe), incl. one that straddles the break ----
def window(d0, d1):
    out = {}
    sel = [lst for d, lst in days.items() if d0 <= d <= d1]
    for g in G + ["All channels (context)"]:
        tops, ent = [], []
        for lst in sel:
            vals = [x[3] for x in lst] if g.startswith("All") else [x[3] for x in lst if cimlib.group_of(x[2]) == g]
            if vals: tops.append(max(vals)); ent += vals
        out[g] = (len(sel), round(statistics.mean(tops)) if tops else "", round(statistics.mean(ent)) if ent else "", len(tops))
    return out
sp = []
for label, a0, a1, b0, b1, note in [
        ("Jan-Jun 2022 vs Jan-Jun 2023", "2022-01-01", "2022-06-30", "2023-01-01", "2023-06-30", "both same-day: like-for-like"),
        ("Jul-Dec 2022 vs Jul-Dec 2023", "2022-07-01", "2022-12-31", "2023-07-01", "2023-12-31", "STRADDLES THE BREAK: second period consolidated, so the change mixes real change and method effect"),
        ("Jan-1 Oct 2025 vs Jan-1 Oct 2026", "2025-01-01", "2025-10-01", "2026-01-01", "2026-10-01", "both consolidated: like-for-like (2026 includes the football World Cup)")]:
    A, B = window(a0, a1), window(b0, b1)
    for g in A:
        ca = (B[g][1] / A[g][1] - 1) * 100 if A[g][1] and B[g][1] else ""
        cb = (B[g][2] / A[g][2] - 1) * 100 if A[g][2] and B[g][2] else ""
        sp.append(dict(comparison=label, group=g, days_a=A[g][0], days_b=B[g][0],
            avg_biggest_programme_a=A[g][1], avg_biggest_programme_b=B[g][1], change_biggest_pct=round(ca, 1) if ca != "" else "",
            avg_per_entry_a=A[g][2], avg_per_entry_b=B[g][2], change_per_entry_pct=round(cb, 1) if cb != "" else "", note=note,
            method="own calculation from CIM daily Top 20 (North, 4+)", source_url=f"{CIM} (tab Dagelijkse top 20, regio Noord)"))
write("cim_daily_top20_same_period_comparisons_owncalc.csv", sp)
