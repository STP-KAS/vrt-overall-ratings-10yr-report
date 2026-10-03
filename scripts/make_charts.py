"""Draw the PNG charts in charts/ from the CSVs in data/ (needs pandas + matplotlib)."""
import os, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); D = os.path.join(R, "data"); C = os.path.join(R, "charts")
os.makedirs(C, exist_ok=True)
sf = pd.read_csv(os.path.join(D, "sourced_figures.csv"), dtype=str)
grp = pd.read_csv(os.path.join(D, "cim_yearly_market_share_by_group_owncalc.csv"))
chn = pd.read_csv(os.path.join(D, "cim_yearly_market_share_by_channel.csv"))
COL = {"VRT": "#1f5fbf", "DPG Media (VTM family)": "#d62728", "Play Media (SBS/Play family)": "#7f3fbf"}
def breaks(ax, ymax):
    lo, hi = ax.get_ylim() if ax.get_ylim()[1] > 1 else (0, ymax)
    for i, (x, t) in enumerate([(2020, "CIM adds online viewing (2020)"), (2021, "+ fragments, live streams,\nTotal TV redefined (2021)")]):
        ax.axvline(x - 0.5, color="grey", ls=":", lw=1)
        ax.text(x - 0.45, ymax - i * 0.07 * (hi - lo), t, fontsize=7, color="grey", va="top")

# 1 group market shares
early = sf[sf.metric == "TV market share, full day (channel)"].copy(); early["value"] = early.value.astype(float); early["year"] = early.year.astype(int)
m = {"Een": "VRT", "Canvas": "VRT", "Ketnet": "VRT", "VTM": "DPG Media (VTM family)", "Q2": "DPG Media (VTM family)", "Vitaya": "DPG Media (VTM family)",
     "CAZ": "DPG Media (VTM family)", "Vier": "Play Media (SBS/Play family)", "Vijf": "Play Media (SBS/Play family)", "Zes": "Play Media (SBS/Play family)"}
early["group"] = early.entity.map(m); e = early.groupby(["year", "group"]).value.sum().round(2)
fig, ax = plt.subplots(figsize=(9, 5))
for g, c in COL.items():
    s = grp[grp.group == g].set_index("year").share_pct
    es = e.xs(g, level="group")
    ax.plot(es.index, es.values, "--o", color=c, ms=4)
    ax.plot([es.index[-1], s.index[0]], [es.values[-1], s.values[0]], ":", color=c)
    ax.plot(s.index, s.values, "-o", color=c, label=g, ms=5)
    for x, y in [(s.index[0], s.values[0]), (s.index[-1], s.values[-1])]:
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, color=c)
ax.set_ylim(0, 45); breaks(ax, 44.5)
ax.set_title("Flemish TV market share by broadcaster group, 2015-2025 (4+, full day)")
ax.set_ylabel("% of total viewing time"); ax.set_xticks(range(2015, 2026)); ax.grid(alpha=.3); ax.legend(loc="lower left", fontsize=8)
fig.text(0.01, 0.01, "Solid: own sum of CIM yearly channel shares (2018-25). Dashed: own sum of channel shares in VRT annual reports 2016/2017 (CIM/GfK; 2015 excl. CAZ).\n"
         "Group = channels grouped as by VRM (VRT / DPG Media / Play Media). Channel renames do not break group totals.", fontsize=7, color="dimgrey")
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(os.path.join(C, "group_market_share.png"), dpi=130); plt.close(fig)

# 2 VRT channels
def vb(ch):
    c = ch.upper()
    return "Een / VRT 1" if c in ("EEN", "VRT1", "VRT 1") else "Canvas / VRT Canvas" if c in ("CANVAS", "VRT CANVAS") else "Ketnet" if c == "KETNET" else None
chn["brand"] = chn.channel_as_listed_by_cim.map(vb)
fig, ax = plt.subplots(figsize=(9, 5))
for b, (k, c) in {"Een / VRT 1": ("Een", "#1f5fbf"), "Canvas / VRT Canvas": ("Canvas", "#ff7f0e"), "Ketnet": ("Ketnet", "#2ca02c")}.items():
    es = early[early.entity == k].set_index("year").value
    s = chn[chn.brand == b].set_index("year").share_pct_4plus_fullday
    ax.plot(es.index, es.values, "--o", color=c, ms=4); ax.plot([es.index[-1], s.index[0]], [es.values[-1], s.values[0]], ":", color=c)
    ax.plot(s.index, s.values, "-o", color=c, label=b, ms=5)
    for x, y in [(es.index[0], es.values[0]), (s.index[-1], s.values[-1])]:
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, color=c)
ax.axvline(2023.33, color="grey", ls=":", lw=1); ax.text(2023.38, 20, "Een -> VRT 1 (1 May 2023)\nCanvas -> VRT CANVAS (4 Sep 2023)", fontsize=7, color="grey")
breaks(ax, 37)
ax.set_ylim(0, 38); ax.set_xticks(range(2015, 2026)); ax.grid(alpha=.3); ax.legend(loc="center left", fontsize=8)
ax.set_title("VRT channels: TV market share, 2015-2025 (4+, full day)"); ax.set_ylabel("% of total viewing time")
fig.text(0.01, 0.01, "Solid: CIM yearly market shares (2018-25). Dashed: VRT annual reports 2016 and 2017 (CIM/GfK, rounded to 0.1).", fontsize=7, color="dimgrey")
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(C, "vrt_channel_shares.png"), dpi=130); plt.close(fig)

# 3 reach
def series(entity, metric):
    x = sf[(sf.entity == entity) & (sf.metric == metric) & (sf.value != "not found")].drop_duplicates("year")
    return x.year.astype(int).values, x.value.astype(float).values
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
for (ent, met, lab, c) in [("VRT TV", "Average daily reach (viewers per day)", "TV viewers", "#1f5fbf"),
                           ("VRT radio", "Average daily reach (listeners per day)", "radio listeners", "#2ca02c"),
                           ("VRT online", "Average daily reach (surfers per day)", "online surfers", "#ff7f0e")]:
    x, y = series(ent, met)
    old = x <= 2021
    a1.plot(x[old], y[old] / 1e6, "-o", color=c, label=lab, ms=4); a1.plot(x[~old], y[~old] / 1e6, "s", color=c, ms=6, mfc="white")
    a1.annotate(f"{y[old][-1]/1e6:.2f}M", (x[old][-1], y[old][-1] / 1e6), textcoords="offset points", xytext=(14, -10 if ent == "VRT TV" else 4), fontsize=7, color=c, ha="center")
a1.axvline(2022, color="grey", ls=":", lw=1); a1.text(2022.1, 0.35, "2022 not found;\n2023+ (open squares): new\nCIM-based definitions", fontsize=7, color="grey")
a1.set_ylim(0, 3.4); a1.set_xticks(range(2015, 2025)); a1.tick_params(axis="x", labelsize=7); a1.grid(alpha=.3); a1.legend(fontsize=8, loc="lower left")
a1.set_title("VRT average daily reach (millions)", fontsize=10)
x, y = series("VRT (all platforms)", "Weekly reach (totaalbereik)")
a2.plot(x, y, "-o", color="#1f5fbf", label="weekly reach, all VRT"); [a2.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 6), fontsize=7, ha="center") for i, v in zip(x, y)]
x, y = series("VRT (all platforms)", "Daily reach across platforms and brands")
a2.plot(x, y, "-o", color="#9467bd", label="daily reach, all VRT"); [a2.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, -12), fontsize=7, ha="center") for i, v in zip(x, y)]
a2.axhline(85, color="grey", lw=.8, ls="--"); a2.set_ylim(60, 100); a2.set_xticks(range(2016, 2026)); a2.tick_params(axis="x", labelsize=7); a2.grid(alpha=.3); a2.legend(fontsize=8, loc="lower right")
a2.set_title("VRT reach across TV, radio and online (% of Flemings)", fontsize=10)
fig.text(0.01, 0.01, "Source: VRT annual reports 2015-2025 (VRT totaalbereik survey; CIM). Survey base 15+ until 2018, 12+ in 2022-2024 reports. Dashed line: 85% weekly-reach norm cited in the VRT 2017 report.", fontsize=7, color="dimgrey")
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(C, "vrt_reach.png"), dpi=130); plt.close(fig)

# 4 daily top 20
dt = pd.read_csv(os.path.join(D, "cim_daily_top20_share_by_group_owncalc.csv"))
fig, ax = plt.subplots(figsize=(9, 5))
for g, c in COL.items():
    s = dt[dt.group == g].set_index("year")
    ax.plot(s.index, s.share_of_top20_viewers_pct, "-o", color=c, label=f"{g}: share of Top-20 viewers", ms=4)
    if g == "VRT":
        ax.plot(s.index, s.share_of_days_no1_pct, "--", color=c, label="VRT: share of days with the #1 programme", lw=1.2)
        for x, y in s.share_of_top20_viewers_pct.items(): ax.annotate(f"{y:.0f}", (x, y), textcoords="offset points", xytext=(0, 6), fontsize=7, ha="center", color=c)
ax.set_ylim(0, 105); ax.set_xticks(range(2016, 2027)); ax.set_xticklabels(["2016*"] + [str(y) for y in range(2017, 2026)] + ["2026*"]); ax.grid(alpha=.3)
breaks(ax, 22); ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(0, 0.47))
ax.set_title("Who fills the CIM daily Top 20? Own calculation, 2016-2026")
ax.set_ylabel("%")
fig.text(0.01, 0.01, "Own calculation from the CIM daily Top 20 (region North). *2016 = 1 Oct-31 Dec; 2026 = 1 Jan-1 Oct. Sum of viewers of all Top-20 entries per group / total.", fontsize=7, color="dimgrey")
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(C, "daily_top20_group_share.png"), dpi=130); plt.close(fig)

# 5 digital
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4))
x, y = series("VRT NU", "Video starts in the year")
a1.bar(x, y / 1e6, color="#1f5fbf"); [a1.annotate(f"{v/1e6:.0f}M", (i, v / 1e6), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8) for i, v in zip(x, y)]
a1.set_title("VRT NU video starts per year (millions)", fontsize=10); a1.set_xticks(x); a1.grid(axis="y", alpha=.3)
a1.text(2016.6, 150, "2022+: not published on a comparable basis.\nVRT MAX 2024: 284M starts incl. audio (not comparable).", fontsize=7, color="grey")
a1.set_ylim(0, 175)
x, y = series("VRT NU / VRT MAX", "Registered users at year end")
a2.plot(x, y / 1e6, "-o", color="#1f5fbf", label="registered (VRT NU accounts to 2019, VRT profiles 2021+)")
x2, y2 = series("VRT NU / VRT MAX", "Active VRT profiles at year end")
a2.plot(x2, y2 / 1e6, "-o", color="#ff7f0e", label="active VRT profiles")
for i, v in list(zip(x, y)) + list(zip(x2, y2)): a2.annotate(f"{v/1e6:.2f}", (i, v / 1e6), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7)
a2.set_ylim(0, 5); a2.set_xticks(range(2018, 2026)); a2.grid(alpha=.3); a2.legend(fontsize=7, loc="upper left")
a2.set_title("VRT NU / VRT MAX users at year end (millions)", fontsize=10)
fig.text(0.01, 0.01, "Source: VRT annual reports 2018-2025. VRT NU was renamed VRT MAX in 2022. 2020 user count not found.", fontsize=7, color="dimgrey")
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(C, "vrt_digital.png"), dpi=130); plt.close(fig)
print("charts written")
