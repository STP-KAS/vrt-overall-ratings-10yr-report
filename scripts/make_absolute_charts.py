"""Absolute-number charts (thousands of viewers / persons), styled like the Journaal report."""
import os, pandas as pd, matplotlib

import matplotlib.transforms as mtrans
def covid(a, x0=2019.5, x1=2021.5, ytext=0.985):
    """Grey band for the COVID-19 years 2020-2021 (as in the Journaal report)."""
    a.axvspan(x0, x1, color="grey", alpha=.08, zorder=0)
    a.text((x0 + x1) / 2, ytext, "COVID-19 years", transform=mtrans.blended_transform_factory(a.transData, a.transAxes),
           ha="center", va="top", fontsize=7.5, color="grey")

matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); D = os.path.join(R, "data"); C = os.path.join(R, "charts")
VRT, DPG, PLAY, GREY = "#c8102e", "#1f4e9c", "#7f3fbf", "#555555"
PER = ["2017", "2018", "2019", "2020", "2021", "2022", "2023 H1", "2023 H2", "2024", "2025", "2026"]
XL = ["2017", "2018", "2019", "2020", "2021", "2022", "2023\nJan–Jun", "2023\nJul–Dec", "2024", "2025", "2026\n(Jan–1 Oct)"]
S1, S2 = PER[:7], PER[7:]
X = {p: i for i, p in enumerate(PER)}

def seg_plot(ax, ser, color, label, style="-", marker="o", lw=2.4, labels=True, dy=8):
    for k, seg in enumerate((S1, S2)):
        pts = [(X[p], ser[p]) for p in seg if p in ser and pd.notna(ser[p])]
        if not pts: continue
        xs, ys = zip(*pts)
        ax.plot(xs, [y / 1000 for y in ys], ls=style, marker=marker, color=color, lw=lw, ms=6 if marker else 0,
                mfc=color if k == 0 else "white", label=label if k == 0 else None)
        if labels:
            for x, y in pts:
                ax.annotate(f"{y/1000:.0f}k", (x, y / 1000), textcoords="offset points", xytext=(0, dy), ha="center", fontsize=8, color=color)

def breaks(ax, ytxt, ytop=None):
    ax.axvline(2.5, color="k", ls="--", lw=.8); ax.text(2.55, ytop if ytop else ytxt, "CIM adds online\nviewing (2020→)", fontsize=7.5, va="top" if ytop else "baseline")
    ax.axvline(6.5, color="k", ls="-", lw=1.6)
    ax.text(6.55, ytxt, "Break: from Jul 2023 CIM's\ndaily values are consolidated\n(Live+7; Live+28 from Jul 2024).\nOpen markers: do not compare\nwith the years before.", fontsize=7.5)

# ---- 1 main chart: biggest programme of the day + average Top-20 entry ----
g = pd.read_csv(os.path.join(D, "cim_daily_top20_absolute_by_group_owncalc.csv"), dtype={"period": str})
def ser(group, col): return g[g.group == group].set_index("period")[col].to_dict()
fig, ax = plt.subplots(figsize=(11.5, 6.4))
seg_plot(ax, ser("VRT", "avg_viewers_biggest_programme_of_day"), VRT, "VRT: biggest programme of the day (average)")
seg_plot(ax, ser("VRT", "avg_viewers_per_top20_entry"), VRT, "VRT: average programme in the daily Top 20", marker="s", lw=1.8, dy=-14)
seg_plot(ax, ser("DPG Media (VTM family)", "avg_viewers_biggest_programme_of_day"), DPG, "DPG Media (VTM…): biggest programme of the day (context)", style=":", lw=1.6, dy=-14)
seg_plot(ax, ser("Play Media (SBS/Play family)", "avg_viewers_biggest_programme_of_day"), PLAY, "Play (VIER/Play4/PLAY…): biggest programme of the day (context)*", style=":", lw=1.6, dy=8)
breaks(ax, 200, ytop=270)
ax.set_xticks(range(len(PER))); ax.set_xticklabels(XL, fontsize=8.5); ax.set_ylim(0, 1250); ax.grid(alpha=.3)
ax.set_ylabel("viewers per programme (thousands)")
ax.set_title("How many people watch VRT's programmes? Average viewers per programme, 2017–2026\n"
             "Own calculation from the CIM daily Top 20 (Flanders + Dutch-speaking Brussels, 4+ incl. guests)", fontsize=11)
ax.legend(fontsize=8, loc="lower left")
fig.text(0.01, 0.01, "* Play only on days it has a Top-20 entry (76–95% of days), so its average is flattered. 2016 (Oct–Dec only) is in the CSV, not plotted.",
         fontsize=7.5, color="dimgrey")
for _a in fig.axes: covid(_a, 2.5, 4.5)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "absolute_vrt_programme_audiences.png"), dpi=150); plt.close(fig)

# ---- 2 per channel ----
c = pd.read_csv(os.path.join(D, "cim_daily_top20_absolute_by_channel_owncalc.csv"), dtype={"period": str})
def cser(ch, col): return c[c.channel == ch].set_index("period")[col].to_dict()
fig, ax = plt.subplots(figsize=(11.5, 6.2))
seg_plot(ax, cser("Een / VRT 1", "avg_viewers_per_top20_entry"), VRT, "Eén / VRT 1")
seg_plot(ax, cser("Canvas / VRT Canvas", "avg_viewers_per_top20_entry"), "#ff7f0e", "Canvas / VRT Canvas", marker="s")
seg_plot(ax, cser("VTM (main channel)", "avg_viewers_per_top20_entry"), DPG, "VTM (context)", style=":", lw=1.6, dy=-14)
seg_plot(ax, cser("VIER / Play4 / PLAY (main channel)", "avg_viewers_per_top20_entry"), PLAY, "VIER / Play4 / PLAY (context)", style=":", lw=1.6, dy=-14)
breaks(ax, 40, ytop=150)
ax.set_xticks(range(len(PER))); ax.set_xticklabels(XL, fontsize=8.5); ax.set_ylim(0, 720); ax.grid(alpha=.3)
ax.set_ylabel("average viewers per Top-20 programme (thousands)")
ax.set_title("Average viewers per programme in the daily Top 20, by channel, 2017–2026 (own calculation, CIM)", fontsize=11)
ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0, 0.02))
fig.text(0.01, 0.01, "Mean viewers of the channel's own entries in the CIM daily Top 20 (VRT 1 ~10 entries a day, Canvas ~1.5, VTM ~6, Play ~1.5). "
         "Ketnet is in the Top 20 on ≤14 days a year: not shown.", fontsize=7.5, color="dimgrey")
for _a in fig.axes: covid(_a, 2.5, 4.5)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "absolute_channel_programme_audiences.png"), dpi=150); plt.close(fig)

# ---- 3 reach in persons ----
sf = pd.read_csv(os.path.join(D, "sourced_figures.csv"), dtype=str)
def s2(entity, metric):
    x = sf[(sf.entity == entity) & (sf.metric == metric) & (sf.value != "not found")].drop_duplicates("year")
    return dict(zip(x.year.astype(int), x.value.astype(float)))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.8), gridspec_kw=dict(width_ratios=[1.25, 1]))
for ent, met, lab, col, mk in [("VRT TV", "Average daily reach (viewers per day)", "VRT TV: viewers per day", VRT, "o"),
                               ("VRT radio", "Average daily reach (listeners per day)", "VRT radio: listeners per day", "#2ca02c", "s"),
                               ("VRT online", "Average daily reach (surfers per day)", "VRT sites/apps: users per day", "#ff7f0e", "^")]:
    d = s2(ent, met)
    old = {k: v for k, v in d.items() if k <= 2021}; new = {k: v for k, v in d.items() if k >= 2023}
    a1.plot(list(old), [v / 1000 for v in old.values()], marker=mk, color=col, lw=2.2, label=lab)
    a1.plot(list(new), [v / 1000 for v in new.values()], marker=mk, color=col, lw=1.2, ls="--", mfc="white")
    for k, v in d.items():
        a1.annotate(f"{v/1000:,.0f}k", (k, v / 1000), textcoords="offset points", xytext=(0, 8 if ent != "VRT TV" else -14), ha="center", fontsize=7, color=col)
a1.axvline(2022, color="k", lw=1.4); a1.text(2022.08, 400, "2022: not found.\nFrom 2023 VRT uses\nCIM-based figures\n(12+; TV 4+ in 2024):\nnot comparable", fontsize=7.5)
a1.set_xticks(range(2015, 2025)); a1.set_ylim(0, 3500); a1.grid(alpha=.3); a1.legend(fontsize=8, loc="lower left")
a1.set_ylabel("persons (thousands)"); a1.set_title("VRT average daily reach in persons, 2015–2024", fontsize=10.5)
reg = s2("VRT NU / VRT MAX", "Registered users at year end"); act = s2("VRT NU / VRT MAX", "Active VRT profiles at year end")
a2.plot(list(reg), [v / 1000 for v in reg.values()], "-o", color=VRT, lw=2.2, label="registered users (VRT NU accounts to 2019; VRT profiles from 2021)")
a2.plot(list(act), [v / 1000 for v in act.values()], "-s", color=GREY, lw=1.8, label="active VRT profiles")
for d, col in ((reg, VRT), (act, GREY)):
    for k, v in d.items(): a2.annotate(f"{v/1000:,.0f}k", (k, v / 1000), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7.5, color=col)
a2.set_xticks(range(2018, 2026)); a2.set_ylim(0, 5000); a2.grid(alpha=.3); a2.legend(fontsize=7.5, loc="lower right")
a2.set_title("VRT NU / VRT MAX users at year end (thousands)", fontsize=10.5)
fig.text(0.01, 0.01, "Source: VRT annual reports 2015–2025 (CIM; VRT data). 2020 user count not found. VRT MAX weekly reach 2023: 1,046,703 (not plotted).",
         fontsize=7.5, color="dimgrey")
for _a in fig.axes: covid(_a)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "absolute_vrt_reach_persons.png"), dpi=150); plt.close(fig)

# ---- 4 biggest audiences per year ----
t = pd.read_csv(os.path.join(D, "cim_yearly_top100_absolute_owncalc.csv"))
def tser(gp, col): return t[t.group == gp].set_index("year")[col].to_dict()
def nice(n): return n.title().replace("Vb. Wk. 1/2F - ", "WK semi ").replace("Vb. Ek. 1/8F - ", "EK last-16 ").replace("Vb. Wk. Schift. - ", "WK ").replace("Fc ", "FC ").replace(" - Kerstspecial", " (Xmas)")
fig, ax = plt.subplots(figsize=(11.5, 6.4))
for gp, col, lab in [("DPG Media (VTM family)", DPG, "DPG Media (VTM…): biggest of the year"), ("Play Media (SBS/Play family)", PLAY, "Play: biggest of the year")]:
    d = tser(gp, "best_entry_viewers"); ax.plot(list(d), [v / 1000 for v in d.values()], marker="o", ls=":", color=col, lw=1.4, ms=4, label=lab)
d = tser("VRT", "best_entry_viewers"); nm = tser("VRT", "best_entry_programme")
ax.plot(list(d), [v / 1000 for v in d.values()], "-o", color=VRT, lw=2.6, label="VRT: biggest audience of the year")
top = tser("All channels", "best_entry_viewers"); tn = tser("All channels", "best_entry_programme"); tc = tser("All channels", "best_entry_channel")
for k, v in d.items():
    below = top[k] != v
    ax.annotate(f"{v/1000:,.0f}k\n{nice(nm[k])}", (k, v / 1000), textcoords="offset points", xytext=(0, -26 if below else 9), ha="center", fontsize=7, color=VRT)
for k, v in top.items():
    if v != d[k]:
        ax.plot([k], [v / 1000], marker="*", ms=14, color="k", ls="none")
        ax.annotate(f"#1: {nice(tn[k])} ({tc[k]})\n{v/1000:,.0f}k", (k, v / 1000), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=7)
ax.plot([], [], marker="*", ms=12, color="k", ls="none", label="#1 of the year when not on VRT")
a10 = {k: float(v) for k, v in tser("All channels", "avg_viewers_top10_entries").items()}
ax.plot(list(a10), [v / 1000 for v in a10.values()], "-s", color=GREY, lw=1.8, label="average of the year's 10 biggest audiences (all channels)")
for k, v in a10.items(): ax.annotate(f"{v/1000:,.0f}k", (k, v / 1000), textcoords="offset points", xytext=(7, -4), ha="left", fontsize=7.5, color=GREY)
ax.axvline(2023.5, color="k", ls="--", lw=.8); ax.text(2023.55, 250, "from 1 Jul 2024: Live+28\n(older years Live+7;\nboth incl. online)", fontsize=7.5)
ax.set_xticks(range(2018, 2026)); ax.set_ylim(0, 2900); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="lower left")
ax.set_ylabel("viewers (thousands)")
ax.set_title("Biggest TV audiences per year in Flanders, 2018–2025 (CIM yearly Top 100, 4+)", fontsize=11)
fig.text(0.01, 0.01, "Source: CIM yearly Top 100 (region North). 2016: Euro 2016 Hungary–Belgium, Eén, 2,420,200 (Sporza); 2017: Reizen Waes, Eén, 1,944,400 (VRT NWS/Belga).",
         fontsize=7.5, color="dimgrey")
for _a in fig.axes: covid(_a)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "absolute_biggest_audiences_per_year.png"), dpi=150); plt.close(fig)
print("absolute charts written")
