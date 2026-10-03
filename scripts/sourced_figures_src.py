"""Writes data/sourced_figures.csv: every hand-extracted figure with its source.
Edit the table below (not the CSV) to correct or add figures, then re-run."""
import csv, os
J = {2015: "https://www.vrt.be/nl/assets/files/2024-09/jaarverslag2015.pdf",
     2016: "https://www.vrt.be/nl/assets/files/2024-09/VRTJaarverslag2016.pdf",
     2017: "https://www.vrt.be/nl/assets/files/2024-09/LRN-VRT-Jaarverslag-2017-web-low-2.pdf",
     2018: "https://www.vrt.be/nl/assets/files/2024-09/VRTJaarverslag2018WEB.pdf",
     2019: "https://www.vrt.be/nl/assets/files/2024-09/VRT_Jaarverslag-2019-CORPS-lowlowres.pdf",
     2020: "https://www.vrt.be/nl/assets/files/2024-09/VRT_jaarverslag2020_A4_030_pages_Compressed.pdf",
     2021: "https://www.vrt.be/nl/assets/files/2024-09/Jaarverslag2021.pdf",
     2022: "https://www.vrt.be/nl/assets/files/2024-09/VRTjaarbeeld2022.pdf",
     2023: "https://www.mediaspecs.be/wp-content/uploads/2024/06/vrt-jaarverslag-2023.pdf",
     2024: "https://www.vrt.be/nl/assets/files/2025-06/Jaarverslag-2024.pdf",
     2025: "https://www.vrt.be/nl/assets/files/2026-07/JVS_2025_0.pdf"}
VRM25 = "https://www.vlaamseregulatormedia.be/sites/default/files/2025-12/mediaconcentratierapport_2025.pdf"
PR24 = "https://communicatie.vrt.be/2024-het-jaar-van-een-nieuwe-groeispurt-voor-vrt-max"
PR25 = "https://communicatie.vrt.be/vrt-bereikt-recordaantal-vlamingen-en-versnelt-digitale-groei-in-2025"
CIM = "https://www.cim.be/nl/televisie"
def jv(y): return f"VRT jaarverslag {y}" + (" (copy hosted by Mediaspecs)" if y == 2023 else "")
def jt(y): return "secondary (copy of primary)" if y == 2023 else "primary"
R = []
def add(year, entity, metric, value, unit, basis, src, url, stype, where, notes=""):
    R.append(dict(year=year, entity=entity, metric=metric, value=value, unit=unit, population_basis=basis,
                  source=src, source_type=stype, source_url=url, location_in_source=where, notes=notes))

# --- VRT TV market share (group), as published by VRT ---
for y, v, rep, where in [(2015, 38.5, 2016, "chart 'Marktaandelen televisie' 2015"), (2016, 39.3, 2017, "chart 'Marktaandelen televisie' 2016"),
                         (2017, 37.1, 2017, "text 'Kijken naar VRT-televisie' + chart"), (2018, 37.3, 2018, "text 'Kijken naar VRT-televisie'"),
                         (2019, 36.6, 2019, "text 'Kijken naar VRT-televisie'"), (2020, 37.6, 2020, "text, section VRT-televisie")]:
    add(y, "VRT (Een+Canvas+Ketnet)", "TV market share, full day", v, "%", "4+ (CIM/GfK audimetry)", jv(rep), J[rep], jt(rep), where,
        "2016 report chart; figure repeated in 2017 report" if y == 2016 else "")
add(2024, "VRT", "TV market share, full day (share of average viewing time)", 38.05, "%", "total population, Live+7+guests", "VRM Mediaconcentratie in Vlaanderen 2025", VRM25, "primary (regulator, based on CIM)", "p. 211 (section 3.1.2.3.2.1)")
add(2024, "DPG Media channels", "TV market share, full day", 28.06, "%", "total population, Live+7+guests", "VRM Mediaconcentratie in Vlaanderen 2025", VRM25, "primary (regulator, based on CIM)", "p. 211", "VRM: lowest point was 2021 (27.71%)")
add(2021, "DPG Media channels", "TV market share, full day", 27.71, "%", "total population", "VRM Mediaconcentratie in Vlaanderen 2025", VRM25, "primary (regulator, based on CIM)", "p. 211", "named by VRM as the low point")
add(2024, "Play Media channels", "TV market share, full day", 14.51, "%", "total population, Live+7+guests", "VRM Mediaconcentratie in Vlaanderen 2025", VRM25, "primary (regulator, based on CIM)", "p. 211", "VRM: 'opnieuw een recordpeil'")
for y, c3 in zip(range(2015, 2025), [81.2, 80.4, 80.3, 81.05, 80.09, 80.32, 80.61, 81.32, 82.21, 83.78]):
    add(y, "VRT + DPG Media + Play Media", "C3 concentration (combined TV share of the 3 largest broadcaster groups)", c3, "%", "total population", "VRM Mediaconcentratie in Vlaanderen 2025", VRM25, "primary (regulator, based on CIM)", "Tabel 71, p. 211")
# --- channel shares 2015-2017 from VRT annual reports (CIM/GfK) ---
ch = {2015: dict(Een=31.7, Canvas=5.0, Ketnet=1.8, VTM=20.6, Q2=4.9, Vitaya=4.9, Vier=7.8, Vijf=4.0),
      2016: dict(Een=32.6, Canvas=5.2, Ketnet=1.5, VTM=19.8, Q2=4.4, Vitaya=4.6, CAZ=0.8, Vier=7.7, Vijf=3.5, Zes=0.4),
      2017: dict(Een=30.1, Canvas=5.4, Ketnet=1.6, VTM=19.6, Q2=4.2, Vitaya=5.2, CAZ=1.6, Vier=7.4, Vijf=3.2, Zes=1.6)}
for y, d in ch.items():
    rep = 2016 if y == 2015 else 2017
    for k, v in d.items():
        add(y, k, "TV market share, full day (channel)", v, "%", "4+ (CIM/GfK audimetry, VRT-Studiedienst)", jv(rep), J[rep], jt(rep), "chart 'Marktaandelen televisie (in %)'",
            "Q2 shown as 'Q2 (voorheen 2BE)'; CAZ and Zes not shown separately in 2015 chart" if y == 2015 else "")
# --- VRT daily reach ---
for y, v, rep, basis, where in [(2015, 2793435, 2015, "not stated", "text 'Kijken naar VRT-televisie'"), (2016, 2770761, 2016, "not stated", "infobox 'Dagelijks bereik'"),
                                (2017, 2755523, 2017, "not stated", "infobox + text"), (2018, 2666339, 2018, "not stated", "infobox + text"), (2019, 2643256, 2019, "not stated", "infobox + text"),
                                (2020, 2762049, 2020, "not stated", "infobox 'Dagelijks bereik'"), (2021, 2580861, 2021, "not stated", "infobox 'Dagelijks bereik'"),
                                (2023, 2355396, 2023, "12+ (CIM)", "infobox 'Dagelijks bereik'"), (2024, 2341668, 2024, "4+ (CIM, footnote 2)", "infobox 'Dagelijks bereik'")]:
    add(y, "VRT TV", "Average daily reach (viewers per day)", v, "persons", basis, jv(rep), J[rep], jt(rep), where,
        "population basis changes: 2023 figure is CIM 12+, not comparable with 4+ years" if y == 2023 else "")
for y in (2022, 2025):
    add(y, "VRT TV", "Average daily reach (viewers per day)", "not found", "", "", jv(y), J[y], jt(y), "searched report text", "2022 'jaarbeeld' has no usable daily-reach table; 2025 report has none")
for y, v, rep, basis in [(2016, 3097754, 2016, "not stated"), (2017, 2964195, 2017, "not stated"), (2018, 3095876, 2018, "not stated"), (2019, 2957787, 2019, "not stated"),
                         (2020, 2970097, 2020, "not stated"), (2021, 2693965, 2021, "not stated"), (2023, 2482924, 2023, "12+ (CIM)"), (2024, 2456000, 2024, "12+ (CIM, footnote 3)")]:
    add(y, "VRT radio", "Average daily reach (listeners per day)", v, "persons", basis, jv(rep), J[rep], jt(rep), "infobox 'Dagelijks bereik'")
for y, v, rep, note in [(2016, 918254, 2016, ""), (2017, 1070174, 2017, ""), (2018, 1217037, 2018, ""), (2019, 1486776, 2019, ""),
                        (2020, 2080588, 2020, "infobox label says '(Vrtnws.be)'"), (2021, 2115160, 2021, ""),
                        (2023, 1068769, 2023, "CIM 12+, own VRT sites and apps; measurement change, not comparable with earlier years"),
                        (2024, 1304188, 2024, "own VRT sites and apps")]:
    add(y, "VRT online", "Average daily reach (surfers per day)", v, "persons", "", jv(rep), J[rep], jt(rep), "infobox 'Dagelijks bereik'", note)
for y, v, rep in [(2019, 71.6, 2020), (2020, 79.4, 2020), (2021, 75.0, 2021), (2023, 71, 2023), (2024, 74, 2024)]:
    add(y, "VRT (all platforms)", "Daily reach across platforms and brands", v, "% of Flemings", "VRT totaalbereik survey", jv(rep), J[rep], jt(rep), "infobox 'Dagelijks bereik'")
for y, v, rep, basis in [(2016, 90.7, 2016, "15+"), (2017, 89.4, 2017, "15+"), (2018, 88.7, 2018, "15+"), (2019, 90.2, 2019, "not stated"), (2020, 90.2, 2020, "not stated"),
                         (2021, 92.4, 2021, "not stated"), (2022, 90.0, 2023, "12+"), (2023, 88.9, 2023, "12+"), (2024, 89.9, 2024, "12+"), (2025, 90.6, 2025, "not stated")]:
    add(y, "VRT (all platforms)", "Weekly reach (totaalbereik)", v, "% of Flemings", basis, jv(rep), J[rep], jt(rep),
        "text 'ten opzichte van 90,0% in 2022'" if y == 2022 else "infobox / KPI text", "also stated in VRT press release of 2 Jul 2026" if y == 2025 else "")
add(2025, "VRT (all platforms)", "Weekly reach (totaalbereik)", 90.6, "% of Flemings", "", "VRT press release 2 Jul 2026", PR25, "primary", "section 'Groot bereik'")
# --- time spent and live vs delayed ---
for y, v, rep in [(2015, 73.3, 2015), (2016, 73.7, 2016), (2017, 75.0, 2017), (2018, 73.1, 2018), (2019, 72.8, 2019), (2020, 73.2, 2020)]:
    add(y, "All TV (Flanders)", "Share of Flemings (4+) watching TV on an average day (live and/or delayed)", v, "%", "4+ (CIM)", jv(rep), J[rep], jt(rep), "section 'Kijken naar televisie'")
for y, v, rep in [(2015, "3:56", 2015), (2016, "3:54", 2016), (2017, "3:47", 2017), (2018, "3:44", 2018), (2019, "3:44", 2019)]:
    add(y, "All TV (Flanders)", "Average daily viewing time per TV viewer (those who watched that day), live and delayed", v, "h:mm", "4+ (CIM)", jv(rep), J[rep], jt(rep), "section 'Kijken naar televisie'",
        "per TV viewer, not per inhabitant")
for y, v, rep in [(2015, "1:50", 2015), (2016, "1:54", 2016), (2017, "1:49", 2017), (2018, "1:49", 2018), (2019, "1:47", 2019)]:
    add(y, "VRT TV", "Average daily viewing time per Fleming (4+) on VRT channels incl. delayed", v, "h:mm", "4+", jv(rep), J[rep], jt(rep), "text 'Kijken naar VRT-televisie'")
for y, v, rep in [(2017, 87.7, 2017), (2018, 86.1, 2018), (2019, 83.6, 2019), (2020, 81.5, 2020)]:
    add(y, "VRT TV", "Share of VRT TV viewing watched live (rest = delayed up to 7 days)", v, "%", "", jv(rep), J[rep], jt(rep), "text",
        "2020 report states 18.5% delayed; 81.5% = 100 - 18.5" if y == 2020 else "")
add(2025, "All TV (North)", "Share of TV viewing watched live", 71, "%", "CIM", "CIM TV key figures 2025", CIM, "primary", "key figures, region North", "29% delayed")
# --- VRT NU / VRT MAX ---
add(2017, "VRT NU", "Launch date", "2017-01-30", "date", "", jv(2016), J[2016], "primary", "text on VRT NU launch")
for y, v, rep, note in [(2017, 33513764, 2018, ""), (2018, 52799274, 2018, "2019 report gives 52,960,012 for 2018"), (2019, 71552287, 2019, ""),
                        (2020, 120708377, 2020, "+68.7% vs 2019"), (2021, 142852816, 2021, "")]:
    add(y, "VRT NU", "Video starts in the year", v, "starts", "", jv(rep), J[rep], jt(rep), "section on VRT NU / infobox", note)
add(2024, "VRT MAX", "Starts of video, podcast or other digital content in the year", 284000000, "starts", "", "VRT press release 20 Dec 2024", PR24, "primary", "bullet list",
    "includes audio and other content: NOT comparable with VRT NU video starts")
add(2024, "VRT MAX", "Monthly media users", 1500000, "users per month (approx.)", "", "VRT press release 20 Dec 2024", PR24, "primary", "bullet list", "'zo'n 1,5 miljoen'")
add(2021, "VRT NU", "Monthly reach (approx.)", 800000, "Flemings per month", "", jv(2021), J[2021], "primary", "text on VRT NU", "'ongeveer 800.000'")
add(2023, "VRT MAX", "Weekly reach", 1046703, "Flemings per week", "", jv(2023), J[2023], jt(2023), "text on VRT MAX")
add(2022, "VRT MAX", "Rename VRT NU -> VRT MAX", "2022", "year", "", "VRT press release 20 Dec 2024", PR24, "primary", "intro: 'Toen VRT MAX in 2022 het daglicht zag'")
for y, v, rep, note in [(2018, 1542167, 2018, "VRT NU accounts"), (2019, 2235543, 2019, "VRT NU accounts"), (2021, 2871262, 2021, "registered VRT profiles (13+)"),
                        (2022, 3383300, 2023, "registered VRT profiles"), (2023, 3662544, 2023, "registered VRT profiles"),
                        (2024, 4284025, 2025, "registered VRT profiles"), (2025, 4407068, 2025, "registered VRT profiles; press release: 4.4M = 64.2% of Flemings")]:
    add(y, "VRT NU / VRT MAX", "Registered users at year end", v, "accounts/profiles", "", jv(rep), J[rep], jt(rep), "text on registered users",
        note + ("; definition changes from 'VRT NU accounts' to 'VRT profiles'" if y == 2021 else ""))
for y, v, rep in [(2021, 1118784, 2021), (2022, 1358728, 2023), (2023, 1627182, 2023), (2024, 2116990, 2024), (2025, 2111700, 2025)]:
    add(y, "VRT NU / VRT MAX", "Active VRT profiles at year end", v, "profiles", "", jv(rep), J[rep], jt(rep), "text on active profiles")
# --- radio share (context) ---
for y, v, rep in [(2015, 62.2, 2016), (2016, 64.1, 2016)]:
    add(y, "VRT radio", "Radio market share", v, "%", "", jv(rep), J[rep], "primary", "text radio")
# --- top programmes not on the CIM yearly page ---
add(2017, "Reizen Waes (Een, 5 Mar 2017)", "Most-watched programme of the year", 1944400, "viewers", "CIM", "VRT NWS / Belga, 12 Feb 2018",
    "https://www.vrt.be/vrtnws/nl/2018/02/12/deze-programma-s-haalden-in-2017-de-hoogste-kijkcijfers/", "secondary (news report of CIM data)", "article", "18 of the 2017 top 20 were VRT programmes")
add(2016, "EK 1/8 final Hungary-Belgium (Een, 26 Jun 2016)", "Highest-rated broadcast (all-time record at the time)", 2420200, "viewers", "Live+7, 4+ incl. guests (corrected by CIM)",
    "Sporza, 1 Aug 2016", "https://sporza.be/nl/2016/08/01/ek-match-hongarije-belgie-levert-kijkcijferrecord-op-1-2727087/", "secondary (news report of CIM data)", "table", "80.5% market share; CIM corrected guest viewing for 18 May-17 Jul 2016")
add(2024, "Lotte Kopecky bronze, Olympic Games (VRT)", "Peak audience", 1037052, "viewers (peak)", "", jv(2024), J[2024], "primary", "Sporza box")
# --- renames / launches (dates) ---
for y, ent, val, src, url in [
    (2020, "DPG Media", "Q2 -> VTM 2, Vitaya -> VTM 3, CAZ -> VTM 4 on 2020-08-31", "DPG Media press release", "https://communicatie.dpgmedia.be/van-familiezender-naar-een-familie-van-zenders-vtm-breidt-vanaf-het-najaar-uit-met-vtm-2-vtm-3-en-vtm-4"),
    (2021, "SBS Belgium / Play Media", "VIER/VIJF/ZES -> Play4/Play5/Play6 on 2021-01-28; Play7 launched 2021-04-02", "Mediaspecs (reprint of press release)", "https://www.mediaspecs.be/vier-vijf-en-zes-worden-play4-play5-en-play6-vanaf-2-april-nieuwe-vrouwenzender-play7/"),
    (2023, "VRT", "Een -> VRT 1 on 2023-05-01", "VRT NWS", "https://www.vrt.be/vrtnws/nl/2023/04/28/een-wordt-vanaf-vandaag-vrt-1/"),
    (2023, "VRT", "Canvas -> VRT CANVAS on 2023-09-04", "VRT", "https://www.vrt.be/nl/over-ons/nieuws-over-vrt/canvas-wordt-vrt-canvas"),
    (2025, "Play Media", "Play4 -> PLAY; Play5/6/7 -> Play Fictie/Actie/Reality on 2025-10-14", "Telenet customer notice", "https://www2.telenet.be/residential/nl/klantenservice/tv-en-entertainment/zenders/zenderaanpassingen.html")]:
    add(y, ent, "Channel rename / launch", val, "event", "", src, url, "primary" if "Mediaspecs" not in src else "secondary", "page")
# --- own calculation: group sums of the 2015-2017 channel shares above ---
G = {"Een": "VRT", "Canvas": "VRT", "Ketnet": "VRT", "VTM": "DPG Media (VTM family)", "Q2": "DPG Media (VTM family)", "Vitaya": "DPG Media (VTM family)",
     "CAZ": "DPG Media (VTM family)", "Vier": "Play Media (SBS/Play family)", "Vijf": "Play Media (SBS/Play family)", "Zes": "Play Media (SBS/Play family)"}
E2 = []
for y, d in ch.items():
    rep = 2016 if y == 2015 else 2017
    for g in ["VRT", "DPG Media (VTM family)", "Play Media (SBS/Play family)"]:
        members = [k for k in d if G[k] == g]
        E2.append(dict(year=y, group=g, share_pct=round(sum(d[k] for k in members), 1), members="+".join(members),
                       method="own calculation: sum of channel shares printed in the VRT annual report chart (CIM/GfK, rounded to 0.1)",
                       source_url=J[rep], notes="CAZ and Zes not shown in the 2015 chart" if y == 2015 and g != "VRT" else ""))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "early_group_shares_2015_2017_owncalc.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(E2[0].keys())); w.writeheader(); w.writerows(E2)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sourced_figures.csv")
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(R[0].keys())); w.writeheader(); w.writerows(R)
print("wrote", out, len(R))
