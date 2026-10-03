"""Charts for 'Public funding vs results' (reads data/public_funding*.csv and data/management_contract_kpis.csv)."""
import os, matplotlib
import matplotlib.transforms as mtrans
import pandas as pd
matplotlib.use("Agg"); import matplotlib.pyplot as plt

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); D = os.path.join(R, "data"); C = os.path.join(R, "charts")
VRT, DPG, GREY = "#c8102e", "#1f4e9c", "#555555"


def covid(a, x0=2019.5, x1=2021.5, ytext=0.985):
    a.axvspan(x0, x1, color="grey", alpha=.08, zorder=0)
    a.text((x0 + x1) / 2, ytext, "COVID-19 years", transform=mtrans.blended_transform_factory(a.transData, a.transAxes),
           ha="center", va="top", fontsize=7.5, color="grey")


def num(s):
    return pd.to_numeric(s, errors="coerce")


def line(a, x, y, color, label, ls="-", fmt="{:.0f}", dy=6, marker="o"):
    x, y = list(x), list(y)
    # break the line at missing values
    seg = []
    for xi, yi in zip(x + [None], y + [float("nan")]):
        if xi is None or pd.isna(yi):
            if seg:
                a.plot([p[0] for p in seg], [p[1] for p in seg], ls=ls, marker=marker, color=color, lw=2.2, ms=5,
                       label=label)
                label = None
            seg = []
        else:
            seg.append((xi, yi))
    for xi, yi in zip(x, y):
        if not pd.isna(yi):
            a.annotate(fmt.format(yi), (xi, yi), textcoords="offset points", xytext=(0, dy), ha="center",
                       fontsize=7.5, color=color)


# ------------------------------------------------------------ funding chart
o = pd.read_csv(os.path.join(D, "public_funding_real_and_per_person_owncalc.csv"))
fig, ax = plt.subplots(1, 2, figsize=(13, 5.2))
a = ax[0]
covid(a)
line(a, o.year, o.pillar1_nominal_meur, VRT, "Nominal (as reported by VRT)", fmt="{:.1f}", dy=-13)
line(a, o.year, o.pillar1_real_2025_prices_meur, GREY, "In 2025 prices (own calculation, Eurostat HICP Belgium)",
     ls="--", fmt="{:.0f}", dy=7)
a.set_ylim(240, 400); a.set_xticks(range(2015, 2026)); a.set_ylabel("million EUR")
a.set_title("VRT public funding (pillar 1 'Overheidsfinanciering'), 2015–2025", fontsize=11)
a.legend(loc="lower right", fontsize=8, frameon=False); a.grid(axis="y", alpha=.3)
a.text(2017, 250, "2017 incl. one-off\npension-fund dotation", fontsize=7, color=GREY, ha="center")

a = ax[1]
covid(a)
line(a, o.year, num(o.pillar1_per_tv_daily_reach_person_eur_nominal), VRT, "Nominal", fmt="{:.0f}", dy=-13)
line(a, o.year, num(o.pillar1_per_tv_daily_reach_person_eur_2025_prices), GREY, "In 2025 prices", ls="--",
     fmt="{:.0f}", dy=7)
a.axvline(2022.5, color=GREY, ls="-.", lw=1)
a.text(2022.55, 0.03, "VRT reach basis\nchanges (2023)", transform=mtrans.blended_transform_factory(a.transData, a.transAxes),
       fontsize=7, color=GREY)
a.set_ylim(60, 160); a.set_xticks(range(2015, 2026)); a.set_ylabel("EUR per person per year")
a.set_title("Public funding per person reached by VRT TV on an average day\n(own calculation; funding also pays radio and online; 2022 and 2025 reach not found)",
            fontsize=9.5)
a.legend(loc="lower left", fontsize=8, frameon=False); a.grid(axis="y", alpha=.3)
fig.text(0.01, 0.01, "Sources: VRT annual reports 2015–2025 (financing-pillar tables); Eurostat HICP (prc_hicp_aind, BE); "
         "VRT TV average daily reach from the VRT annual reports. See data/public_funding*.csv.", fontsize=7, color=GREY)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "public_funding_vs_results.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------ KPI chart
k = pd.read_csv(os.path.join(D, "management_contract_kpis.csv"))
k = k[k.year.astype(str).str.fullmatch(r"\d{4}")].copy(); k["year"] = k.year.astype(int); k["v"] = num(k.value)


def ser(prefix):
    s = k[k.kpi.str.startswith(prefix)].sort_values("year")
    return s.year, s.v


fig, a = plt.subplots(figsize=(11, 5.6))
covid(a)
x, y = ser("Weekly reach of all VRT offer"); x2, y2 = ser("KPI 9: weekly reach of all VRT offer")
line(a, list(x) + list(x2), list(y) + list(y2), VRT, "Weekly reach, all VRT (target ≥ 85%)", fmt="{:.1f}", dy=6)
x, y = ser("Weekly reach of the total information"); x2, y2 = ser("KPI 19: weekly reach of VRT NWS (total")
line(a, list(x) + list(x2), list(y) + list(y2), DPG, "Weekly reach, news offer / VRT NWS (target ≥ 75%)", fmt="{:.1f}", dy=-13)
x, y = ser("Trust in VRT TV as a news source"); x2, y2 = ser("KPI 20: trust in VRT TV")
line(a, list(x) + list(x2), list(y) + list(y2), "#2a9d8f", "Trust in VRT TV as news source (no numeric target until 2026)",
     fmt="{:.0f}", dy=6)
x, y = ser("KPI 18")
line(a, x, y, "#e76f51", "Registered users active per month (target ≥ 50%, not met)", fmt="{:.1f}", dy=-13)
for t, c in [(85, VRT), (75, DPG), (50, "#e76f51")]:
    a.axhline(t, color=c, ls=":", lw=1)
a.plot([2025.6, 2026.4], [70, 70], color="#2a9d8f", ls=":", lw=1.5)
a.text(2026, 66, "2026–2030\ntrust target\n≥ 70%", fontsize=7, color="#2a9d8f", ha="center", va="top")
a.axvline(2020.5, color=GREY, ls="-.", lw=1)
a.text(2020.55, 0.47, "new contract\n(KPIs 2021–2025)", transform=mtrans.blended_transform_factory(a.transData, a.transAxes),
       fontsize=7, color=GREY)
a.set_xlim(2015.5, 2026.6); a.set_ylim(30, 100); a.set_xticks(range(2016, 2027)); a.set_ylabel("%")
a.set_title("VRT management-contract indicators vs targets, 2016–2025 (as reported by VRT)", fontsize=11)
a.legend(loc="lower left", fontsize=8, frameon=False, ncol=2); a.grid(axis="y", alpha=.3)
fig.text(0.01, 0.01, "Source: VRT annual reports 2016–2025 (performance measures / KPIs 9, 18, 19, 20); "
         "trust 2017–2018 not found on a comparable question. See data/management_contract_kpis.csv.",
         fontsize=7, color=GREY)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(C, "management_contract_kpis.png"), dpi=150); plt.close(fig)
print("ok")
