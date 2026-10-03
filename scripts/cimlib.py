"""Helpers to parse CIM (cim.be) TV pages that were cached locally as HTML.
The cache itself is NOT part of this repository (see README > Other > Reproduce)."""
import re, html, glob, os

def cells_of(h):
    out = []
    for r in re.findall(r"<tr.*?</tr>", h, re.S):
        out.append([html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
                    for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)])
    return out

def fix(c):
    """Some 2016-2017 daily rows come back as one malformed string in the title cell."""
    if not c[6]:
        m = re.match(r'^(.*?)[;"]+\s*[;"]*"?([A-Za-z0-9 .]+?)"?[;"]*(\d\d:\d\d:\d\d)[;"]*(\d\d:\d\d:\d\d)[;"]*(\d\d:\d\d:\d\d)[;"]*([\d.]+)', c[1])
        if m:
            title, ch, start, end, dur, viewers = m.groups()
            return [c[0], title.strip(), ch.strip(), c[3], start, dur, viewers.strip(".")]
        return None
    return c

def to_int(v):
    """'1.212.156' -> 1212156 ; '971.420,70' -> 971421"""
    v = v.strip()
    if "," in v:
        whole, dec = v.split(",", 1)
        return int(round(float(whole.replace(".", "") + "." + dec)))
    return int(v.replace(".", ""))

def thousands(v):
    """Yearly Top-100 'Aantal kijkers/1.000': '2.502,4' (2018-22) or '1837.5' (2023+) -> viewers."""
    v = v.strip()
    if "," in v:
        v = v.replace(".", "").replace(",", ".")
    return int(round(float(v) * 1000))

def daily_rows(cache_dir):
    for f in sorted(glob.glob(os.path.join(cache_dir, "raw", "*.html"))):
        d = os.path.basename(f)[:-5]
        cells = [fix(c) for c in cells_of(open(f, encoding="utf-8").read()) if len(c) == 7]
        cells = [c for c in cells if c and c[0].isdigit()]
        for rank, prog, ch, date, start, dur, viewers in cells:
            if not re.fullmatch(r"[\d.,]+", viewers.strip()) or not ch.strip():
                continue  # footer/garbage rows (e.g. 'Total Individuals (North) Universe ...')
            yield d, int(rank), prog, ch, to_int(viewers)

# Channel -> group. Grouping follows the broadcaster groups used by the Vlaamse Regulator voor de Media
# (VRM, Mediaconcentratie in Vlaanderen 2025, p. 211: "VRT", "DPG Media-zenders", "Play Media-zenders").
VRT = {"EEN", "VRT1", "VRT 1", "CANVAS", "VRT CANVAS", "KETNET", "KETNET/CANVAS", "CANVAS/KETNET"}
DPG = {"VTM", "Q2", "VITAYA", "CAZ", "CAZ 2", "CAZ 2 (VTM GOLD)", "VTM 2", "VTM2", "VTM 3", "VTM3", "VTM 4", "VTM4",
       "VTM GOLD", "VTM KIDS", "VTM KIDS JR", "VTMKZOOM", "VTM LIFE", "VTM NON-STOP 90S", "2BE"}
PLAY = {"VIER", "VIJF", "ZES", "PLAY4", "PLAY 4", "PLAY5", "PLAY 5", "PLAY6", "PLAY 6", "PLAY7", "PLAY 7", "PLAY",
        "PLAY FICTIE", "PLAY ACTIE", "PLAY REALITY", "PLAY CRIME", "PLAY 247"}
# Note: 'PLAY SPORTS OPEN' (Telenet sports channel) is NOT counted as Play Media; this reproduces VRM's 2024 total (14.51%).

def group_of(ch):
    c = re.sub(r"\s+", " ", ch.strip().upper())
    if c in VRT: return "VRT"
    if c in DPG: return "DPG Media (VTM family)"
    if c in PLAY: return "Play Media (SBS/Play family)"
    parts = [p.strip() for p in re.split(r"[,/]", c)]
    if len(parts) > 1 and len({group_of(p) for p in parts} - {"Other"}) > 1:
        return "Joint simulcast (several groups)"  # e.g. 'VRT 1/VTM/PLAY4' (Kastaars!, Oekraine 12-12)
    return "Other"

def vrt_brand(ch):
    c = ch.strip().upper()
    if c in ("EEN", "VRT1", "VRT 1"): return "Een / VRT 1"
    if c in ("CANVAS", "VRT CANVAS"): return "Canvas / VRT Canvas"
    if c == "KETNET": return "Ketnet"
    return None
