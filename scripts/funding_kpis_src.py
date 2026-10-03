"""Sourced figures for 'Reasons for the decline' and 'Public funding vs results'.

Every number below was read from the source named next to it. Nothing is estimated.
Missing values are written as 'not found'. Own calculations are written to a
separate *_owncalc.csv file and labelled as such.
Run: python3 scripts/funding_kpis_src.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

JV = {
    2015: "https://www.vrt.be/nl/assets/files/2024-09/jaarverslag2015.pdf",
    2016: "https://www.vrt.be/nl/assets/files/2024-09/VRTJaarverslag2016.pdf",
    2017: "https://www.vrt.be/nl/assets/files/2024-09/LRN-VRT-Jaarverslag-2017-web-low-2.pdf",
    2018: "https://www.vrt.be/nl/assets/files/2024-09/VRTJaarverslag2018WEB.pdf",
    2019: "https://www.vrt.be/nl/assets/files/2024-09/VRT_Jaarverslag-2019-CORPS-lowlowres.pdf",
    2020: "https://www.vrt.be/nl/assets/files/2024-09/VRT_jaarverslag2020_A4_030_pages_Compressed.pdf",
    2021: "https://www.vrt.be/nl/assets/files/2024-09/Jaarverslag2021.pdf",
    2022: "https://www.vrt.be/nl/assets/files/2024-09/VRTjaarbeeld2022.pdf",
    2023: "https://www.mediaspecs.be/wp-content/uploads/2024/06/vrt-jaarverslag-2023.pdf",
    2024: "https://www.vrt.be/nl/assets/files/2025-06/Jaarverslag-2024.pdf",
    2025: "https://www.vrt.be/nl/assets/files/2026-07/JVS_2025_0.pdf",
}
HICP_URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_aind"
            "?geo=BE&coicop=CP00&unit=INX_A_AVG&format=JSON")
BHO26 = "https://www.vrt.be/nl/assets/files/2025-10/BHO_VRT_2025_digitaal-14-10-2025.pdf"
DIGI = "https://www.imec.be/sites/default/files/2026-03/imec.digimeter-2025-rapport.pdf"
DNR = ("https://smit.research.vub.be/en/policy-brief-93-digital-news-report-2025-wider-access-"
       "weaker-pull-more-channels-less-interest-and-a")
VRT_FIN = "https://www.vrt.be/nl/over-ons/financien/financieel-kader"
VRT_BHO_PR = ("https://www.vrt.be/nl/over-ons/nieuws-over-vrt/met-een-nieuwe-beheersovereenkomst-vrt-"
              "klaar-voor-de-toekomst-vertrouwen-vernieuwing-en-ambitie-centraal")
VRTNWS_SAV = ("https://www.vrt.be/vrtnws/nl/2026/09/30/vrt-moet-10-miljoen-euro-extra-besparen-"
              "vrt-max-mag-betalend-lu/")
PARL_2025 = "https://docs.vlaamsparlement.be/files/pfile?id=2185801"
REKENHOF_2001 = "https://www.ccrek.be/sites/default/files/Docs/sept_2001_beheersovereenkomsten.pdf"


def jvsrc(y):
    return ("VRT annual report 2023 (copy hosted by Mediaspecs; secondary)" if y == 2023
            else f"VRT annual report {y}" if y != 2022 else "VRT jaarbeeld 2022")


def write(name, header, rows):
    with open(os.path.join(DATA, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows), "rows")


# ---------------------------------------------------------------- 1. funding
# Pillar 1 'Overheidsfinanciering' in the 'Financieringspijlers' table (first-reported value)
pillar1 = {  # year: (value M EUR, report year used, page, note)
    2015: (277.1, 2015, "p.74 (PDF page), table 'Financieringspijlers'", ""),
    2016: (267.2, 2016, "p.191, table 'Financieringspijlers'", ""),
    2017: (286.6, 2017, "p.183, table 'Financieringspijlers'",
           "includes an extra dotation to support the assets of the pension fund (text on same page); "
           "restated as 268.3 in the 2018 report (p.154)"),
    2018: (276.1, 2018, "p.154, table 'Financieringspijlers'", ""),
    2019: (273.7, 2019, "p.161, table 'Financieringspijlers'", ""),
    2020: (273.6, 2020, "p.128, table 'Financieringspijlers'", ""),
    2021: (273.4, 2021, "p.80, table 'Financieringspijlers'", ""),
    2022: (290.6, 2023, "p.80, table 'Financieringspijlers', prior-year column",
           "the 2022 jaarbeeld has no financing table; value taken from the 2023 report"),
    2023: (297.9, 2023, "p.80, table 'Financieringspijlers'", ""),
    2024: (304.4, 2024, "p.79, table 'Financieringspijlers'", ""),
    2025: (319.4, 2025, "p.74, table 'Financieringspijlers'",
           "the 2025 report states this includes 20.0 M EUR of extra policy funds"),
}
per_user = {  # 'Totale overheidsfinanciering per mediagebruiker' (EUR); mediagebruikers = inhabitants of Flanders
    2015: (43.0, 2015, "p.80"), 2016: (41.2, 2016, "p.199"), 2017: (44.0, 2017, "p.191"),
    2018: (41.2, 2018, "p.161"), 2019: (40.6, 2019, "p.169"), 2020: (37.95, 2020, "p.134"),
    2021: (41.22, 2021, "p.85"), 2023: (42.07, 2023, "p.85"), 2024: (44.59, 2024, "p.84"),
    2025: (44.58, 2025, "p.80"),
}
hicp = {2015: 100.0, 2016: 101.77, 2017: 104.03, 2018: 106.44, 2019: 107.77, 2020: 108.23,
        2021: 111.71, 2022: 123.26, 2023: 126.07, 2024: 131.52, 2025: 135.49}

H = ["year", "entity", "metric", "value", "unit", "source", "source_type", "source_url",
     "location_in_source", "notes"]
rows = []
for y in range(2015, 2027):
    if y in pillar1:
        v, ry, loc, note = pillar1[y]
        rows.append([y, "VRT", "Public funding (pillar 1 'Overheidsfinanciering')", v, "M EUR (nominal)",
                     jvsrc(ry), "secondary" if ry == 2023 else "primary", JV[ry], loc, note])
    else:
        rows.append([y, "VRT", "Public funding (pillar 1 'Overheidsfinanciering')", "not found", "M EUR (nominal)",
                     "", "", "", "",
                     "no 2026 annual report yet; the 2026 Flemish budget lines checked do not state the dotation"])
for y in range(2015, 2026):
    if y in per_user:
        v, ry, loc = per_user[y]
        rows.append([y, "VRT", "Public funding per media user (= per inhabitant of Flanders)", v, "EUR",
                     jvsrc(ry), "secondary" if ry == 2023 else "primary", JV[ry],
                     loc + ", table 'De kosten per mediagebruiker'",
                     "VRT defines 'mediagebruikers' as the number of inhabitants of Flanders"])
    else:
        rows.append([y, "VRT", "Public funding per media user (= per inhabitant of Flanders)", "not found", "EUR",
                     "", "", "", "", "the 2022 jaarbeeld does not publish it"])
for y, v in hicp.items():
    rows.append([y, "Belgium", "HICP, all items, annual average index", v, "index 2015=100",
                 "Eurostat prc_hicp_aind", "primary", HICP_URL, "geo=BE, coicop=CP00, unit=INX_A_AVG",
                 "used instead of the Statbel CPI, whose website could not be accessed from our machine"])
# savings / funding decisions (text facts, value in M EUR where stated)
rows += [
    [2022, "VRT", "Transformation plan: structural saving on operations", 25, "M EUR per year",
     "Flemish Parliament, hearing on the new management contract, 13 Mar 2025 (VRT CEO)", "primary",
     PARL_2025, "statement of the VRT CEO", "plan agreed with the Flemish Government in the 2021-2025 contract; "
     "reported as completed"],
    [2026, "VRT", "Cost control in the 2026-2030 contract, rising to (by 2030)", 16, "M EUR per year",
     "VRT press release on the 2026-2030 management contract", "primary", VRT_BHO_PR, "press release text", ""],
    [2027, "VRT", "Additional dotation cut announced Sep 2026 (2027; rising to 7 M EUR by 2029)", 3.4, "M EUR",
     "VRT NWS, 30 Sep 2026", "primary", VRTNWS_SAV, "article text",
     "together with no indexation of operating funds, about 10 M EUR of extra savings according to the article"],
    [2026, "VRT", "Ceiling on digital advertising revenue (raised from 13 M EUR)", 20, "M EUR",
     "VRT, Financieel kader", "primary", VRT_FIN, "page text", ""],
]
write("public_funding.csv", H, rows)

# own calculations
tvreach = {2015: 2793435, 2016: 2770761, 2017: 2755523, 2018: 2666339, 2019: 2643256,
           2020: 2762049, 2021: 2580861, 2023: 2355396, 2024: 2341668}  # from data/sourced_figures.csv
OH = ["year", "pillar1_nominal_meur", "hicp_2015_100", "pillar1_real_2025_prices_meur",
      "vrt_tv_avg_daily_reach_persons", "pillar1_per_tv_daily_reach_person_eur_nominal",
      "pillar1_per_tv_daily_reach_person_eur_2025_prices", "method", "caveats"]
orows = []
for y in range(2015, 2026):
    nom = pillar1[y][0]
    real = round(nom * hicp[2025] / hicp[y], 1)
    r = tvreach.get(y)
    orows.append([y, nom, hicp[y], real, r if r else "not found",
                  round(nom * 1e6 / r, 1) if r else "not found",
                  round(real * 1e6 / r, 1) if r else "not found",
                  "own calculation: real = nominal x HICP(2025)/HICP(year); per person = pillar 1 / VRT TV "
                  "average daily reach (data/sourced_figures.csv)",
                  "pillar 1 pays for radio, online and all other VRT activity, not only TV; the VRT reach "
                  "basis changes in 2023 (see Other); 2017 includes a one-off pension-fund dotation"])
write("public_funding_real_and_per_person_owncalc.csv", OH, orows)

# ---------------------------------------------------------------- 2. KPIs
KH = ["contract", "kpi", "target", "year", "value", "unit", "met_as_reported", "source", "source_url",
      "location_in_source", "notes"]
k = []
c1 = "management contract 2016-2020"
for y, v, loc in [(2016, 90.7, "p.19"), (2017, 89.4, "2019 report p.15 (5-year table)"),
                  (2018, 88.7, "2019 report p.15 (5-year table)"), (2019, 90.2, "p.15"), (2020, 90.2, "p.21")]:
    ry = 2019 if y in (2017, 2018) else y
    k.append([c1, "Weekly reach of all VRT offer", ">= 85% of Flemings (15+; 16+ in 2020)", y, v, "%", "yes",
              jvsrc(ry), JV[ry], loc, "VRT totaalbereik survey"])
for y, v, loc in [(2016, 81.0, "p.210"), (2017, 77.5, "p.203"), (2018, 78.9, "p.169"), (2019, 79.7, "p.43"),
                  (2020, 82.6, "p.36")]:
    k.append([c1, "Weekly reach of the total information (news) offer", ">= 75% of Flemings", y, v, "%", "yes",
              jvsrc(y), JV[y], loc, ""])
k += [
    [c1, "Trust in VRT TV as a news source", "no numeric target (trust to be measured)", 2016, 76, "% (much) trust",
     "n/a", jvsrc(2016), JV[2016], "trust section", "radio 74%, website 71%; 2015: TV 74, radio 72, site 69"],
    [c1, "Trust in VRT TV as a news source", "no numeric target", 2017, "not found", "% (much) trust", "n/a",
     jvsrc(2017), JV[2017], "", "2017 report uses another question: 80% find VRT news reliable"],
    [c1, "Trust in VRT TV as a news source", "no numeric target", 2018, "not found", "% (much) trust", "n/a",
     "", "", "", ""],
    [c1, "Trust in VRT TV as a news source", "no numeric target", 2019, 73, "% (much) trust", "n/a",
     jvsrc(2019), JV[2019], "trust section", "radio 74%, website 70%"],
    [c1, "Trust in VRT TV as a news source", "no numeric target", 2020, 75.4, "% (much) trust", "n/a",
     jvsrc(2020), JV[2020], "trust section", "radio 72.6%, website 71.4%"],
    [c1, "Spoken subtitling of all non-Dutch-language news content", "100%", 2019, "not met", "", "no",
     jvsrc(2019), JV[2019], "appendix 'performantiemaatstaven' (p.175 ff.)", ""],
    [c1, "Market-share or programme-audience target", "", "2016-2020", "not found", "", "n/a",
     jvsrc(2019), JV[2019], "appendix 'performantiemaatstaven' (p.175 ff.)",
     "no such target in the list of performance measures"],
]
for y, e, cv in [(2016, 8.2, 8.1), (2017, 8.2, 8.2), (2018, 8.1, 8.2), (2019, 8.1, 8.1), (2020, 8.2, 8.2),
                 (2021, 8.1, 8.1)]:
    k.append([c1 if y <= 2020 else "management contract 2021-2025", "Appreciation ('waardering') of Een / VRT 1",
              "no numeric target (reported indicator)", y, e, "score out of 10", "n/a", jvsrc(y), JV[y],
              "infobox", f"Canvas {cv}"])
for y in (2022, 2023, 2024, 2025):
    k.append(["management contract 2021-2025", "Appreciation ('waardering') of Een / VRT 1",
              "no numeric target (reported indicator)", y, "not found", "score out of 10", "n/a", "", "", "", ""])
c2 = "management contract 2021-2025"
reach9 = {2021: 92.4, 2022: 90.0, 2023: 88.9, 2024: 89.9, 2025: 90.6}
for y, v in reach9.items():
    k.append([c2, "KPI 9: weekly reach of all VRT offer", ">= 85% of Flemings and >= 75% of each relevant group",
              y, v, "%", "yes", jvsrc(y), JV[y], "KPI 9" + (" (p.12)" if y == 2025 else ""), ""])
news19 = {2021: (87.0, 80.8, "p.36"), 2022: (82.4, 76.6, ""), 2023: (82.0, 84.4, "p.34"),
          2024: (81.7, 79.8, "p.30"), 2025: (83.2, 86.7, "p.20")}
for y, (v, yv, loc) in news19.items():
    k.append([c2, "KPI 19: weekly reach of VRT NWS (total information offer)", ">= 75% of Flemings", y, v, "%",
              "yes", jvsrc(y), JV[y], ("KPI 19 " + loc).strip(), "2021: population 12+"])
    k.append([c2, "KPI 19: weekly reach of VRT NWS among 16-24", ">= 65% (aim)", y, yv, "%", "yes",
              jvsrc(y), JV[y], ("KPI 19 " + loc).strip(), ""])
trust20 = {2021: (73, 68, 66, "p.36"), 2022: (74, 71, 69, ""), 2023: (75, 71, 71, "p.35"),
           2024: (75, 72, 73, "p.30"), 2025: (75, 71, 71, "p.20")}
for y, (tv, rad, web, loc) in trust20.items():
    k.append([c2, "KPI 20: trust in VRT TV as a news source", "no numeric target", y, tv, "% (much) trust", "n/a",
              jvsrc(y), JV[y], ("KPI 20 " + loc).strip(), f"radio {rad}%, vrtnws.be {web}%"])
act18 = {2021: (39.0, "p.33"), 2022: (40.2, ""), 2023: (44.4, "p.32"), 2024: (49.4, "p.28"), 2025: (47.9, "p.18")}
for y, (v, loc) in act18.items():
    k.append([c2, "KPI 18: share of registered users active in the month", ">= 50%", y, v, "%", "no",
              jvsrc(y), JV[y], ("KPI 18 " + loc).strip(), ""])
k += [
    [c2, "KPI 10: balanced and inclusive portrayal", "targets per group", 2025,
     "not met for women and for people with a disability", "", "partly", jvsrc(2025), JV[2025], "KPI 10 (p.13)", ""],
    [c2, "KPI 31: culture items in Het Journaal", ">= 365 per year", 2024, 647, "items", "yes", jvsrc(2024),
     JV[2024], "KPI 31", ""],
    [c2, "KPI 31: culture items in Het Journaal", ">= 365 per year", 2025, 662, "items", "yes", jvsrc(2025),
     JV[2025], "KPI 31", ""],
    [c2, "Market-share or programme-audience target", "", "2021-2025", "not found", "", "n/a", jvsrc(2025),
     JV[2025], "KPI list", "no such KPI in the list reported on"],
]
c3 = "management contract 2026-2030"
for kpi, tgt in [
    ("KPI 1: trust in VRT", ">= 70% of Flemings"),
    ("KPI 11: trust in VRT NWS via TV, radio or online", ">= 70% of Flemings"),
    ("KPI 13: investigative stories", ">= 15 in 2026, rising to 20 in 2030"),
    ("KPI 14: weekly reach of VRT NWS", ">= 75% of Flemings and >= 65% of each relevant group"),
    ("KPI 16: reach of the analysis ('duiding') offer", ">= 45% of media users, 50% by 2030"),
    ("KPI 18: culture items in Het Journaal", ">= 365 per year"),
    ("KPI 24: at least one programme on important social themes", "aim: reach of >= 1 million media users"),
    ("KPI 25: weekly reach of all VRT offer", ">= 85% of Flemings and >= 75% of each relevant group"),
    ("KPI 26: daily reach", ">= 70%"),
    ("Market-share or programme-audience target", "not found in the KPI list"),
]:
    k.append([c3, kpi, tgt, "2026-2030", "first results due by 1 June 2027", "", "n/a",
              "Beheersovereenkomst VRT 2026-2030", BHO26, "KPI list (pp. 30-33 of the PDF)", ""])
write("management_contract_kpis.csv", KH, k)

# ---------------------------------------------------------------- 3. drivers
DH = ["driver", "indicator", "year_from", "value_from", "year_to", "value_to", "unit", "population",
      "source", "source_url", "location_in_source", "notes"]
d = [
    ["less live TV", "watch live TV daily", 2020, 56, 2025, 40, "%", "Flemings 18+", "imec.digimeter 2025",
     DIGI, "p.23", "2025 = -1 point vs 2024"],
    ["less live TV", "watch live TV daily, age 25-34", "", "", 2025, 14, "%", "Flemings 25-34",
     "imec.digimeter 2025", DIGI, "p.23", "18-24: 17%; 55-64: 51%; 65-74: 65%; 75+: 71%"],
    ["time-shifted viewing", "watch delayed TV daily", 2024, 32, 2025, 37, "%", "Flemings 18+",
     "imec.digimeter 2025", DIGI, "p.23", ""],
    ["cord-cutting", "no cable/TV subscription", "", "", 2025, 26, "%", "Flemings 18+", "imec.digimeter 2025",
     DIGI, "p.23", "cord-nevers 15%, cord-cutters 11%"],
    ["streaming competition", "access to at least one paid streaming subscription", "", "", 2025, 59, "%", "Flemings 18+",
     "imec.digimeter 2025", DIGI, "p.25", "56% use one actively"],
    ["news via social media", "follow news via social media daily", "", "", 2025, 44, "%", "Flemings 18+",
     "imec.digimeter 2025", DIGI, "p.39", "national TV news daily 51% (-2); radio news 55%"],
    ["news via search/AI", "follow news via search engines daily", 2024, 22, 2025, 33, "%", "Flemings 18+",
     "imec.digimeter 2025", DIGI, "p.39", ""],
    ["fragmentation", "share of viewing by listed channels outside the three groups", 2018, 9.2, 2025, 13.1, "%",
     "4+", "CIM yearly market shares (own sum)", "https://www.cim.be/nl/televisie",
     "tab Marktaandelen", "see data/cim_yearly_market_share_by_group_owncalc.csv"],
    ["less TV news", "watch TV evening news (weekly news source)", 2017, 73, 2026, 51, "%",
     "Flemish online population (DNR survey)", "SMIT/VUB, Digital News Report Flanders, policy brief 93", DNR,
     "brief text", ""],
    ["news avoidance", "sometimes or often avoid the news", 2017, 48, 2026, 66, "%", "Flemish news users",
     "SMIT/VUB policy brief 93", DNR, "brief text", ""],
    ["interest in news", "very or extremely interested in news", 2017, 62, 2026, 36, "%", "Flemish news users",
     "SMIT/VUB policy brief 93", DNR, "brief text", "59% in 2021"],
    ["daily news use", "use news daily", 2017, 89, 2026, 72, "%", "Flemish news users", "SMIT/VUB policy brief 93",
     DNR, "brief text", ""],
    ["young audiences", "social media as main news source, age 18-24", 2017, 23, 2026, 43, "%", "18-24",
     "SMIT/VUB policy brief 93", DNR, "brief text", ""],
    ["trust", "trust most news most of the time", 2017, 57, 2026, "just under 50", "%", "Flemish news users",
     "SMIT/VUB policy brief 93", DNR, "brief text", "61% in 2020"],
    ["online news", "use VRT NWS online weekly", "", 33, 2026, 40, "%", "Flemish news users",
     "SMIT/VUB policy brief 93", DNR, "brief text", "earlier year as stated in the brief"],
    ["general media change", "VRT explanation of falling viewing time", "", "", 2019, "text", "", "",
     jvsrc(2019), JV[2019], "TV section",
     "VRT: the decline 'sluit aan bij het algemene, veranderende mediagedrag'"],
]
write("decline_drivers_sourced.csv", DH, d)
