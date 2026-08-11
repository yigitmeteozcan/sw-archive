#!/usr/bin/env python3
"""funding_by_vertical çıkarımı — ONE report at a time (Altın kural).

Üç farklı sayfa düzeni var, üçü de ayrı ele alınır:

  matrix  2023+ : satır = vertical, kolon = yıl. Tek sayfa tek metrik.
  bars    2019-2022 : bar chart, x ekseni = vertical adı. Sayfada iki alt
          grafik (BY DEAL SIZE / BY DEAL COUNT), ikisi de HEM tutar HEM
          adet gösterir. Her grafik kendi sıralama metriğinde otoritedir;
          çakışırsa otorite kazanır ve satır confidence=low ile işaretlenir.
  hbar18  2018 : yatay bar; grafikte yalnız "(N deals)" var, tutar yok.
          4 tag'in tutarı yalnız düzyazı madde işaretlerinde geçiyor.

Top-10/top-5 dışında kalan tag için satır YAZILMAZ (yok ≠ sıfır).
Okunamayan sayı TAHMİN EDİLMEZ.

Kullanım:
    .venv/bin/python scripts/extract_verticals.py 2023
    .venv/bin/python scripts/extract_verticals.py 2023 --write
"""
import argparse
import csv
import json
import os
import re
import sys

import fitz

from extract_facts import (FACTS_COLS, PAGE_ISSUES, append_facts,
                           mark_provisional, parse_tick, ROOT, TICK_RE)

EXTRACTED = os.path.join(ROOT, "extracted")
DIM = os.path.join(ROOT, "dim_verticals.csv")

MONEY_RE = re.compile(r"^\$(\d+(?:\.\d+)?)([KMB])?$", re.I)
COUNT_RE = re.compile(r"^\d{1,4}$")
MULT = {"K": 1e3, "M": 1e6, "B": 1e9}
# Metrik adı ölçü tabanını TAŞIMALI. Unique anahtar (CLAUDE.md) unit içermiyor:
# (data_year, period, report_year, metric, dim_value_canon, scope). Tek bir
# "funding_by_vertical" adı kullanılsaydı aynı tag'in $ ve # satırları aynı
# anahtara düşer ve biri sessizce kaybolurdu. Headline'daki
# total_deal_size/total_deal_count ayrımıyla aynı gerekçe.
METRIC = {"size": "funding_by_vertical_size",
          "count": "funding_by_vertical_count"}

SPECS = {
    "2018": {"source_file": "2018.pdf", "report_year": 2018, "pages": [
        {"page": 8, "layout": "hbar18", "data_year": 2018},
    ]},
    "2019": {"source_file": "2019.pdf", "report_year": 2019, "pages": [
        {"page": 7, "layout": "bars", "data_year": 2019, "regions": [
            {"x": (60, 960), "y": (240, 815), "label_y": 812, "auth": "size"},
            {"x": (960, 1900), "y": (240, 818), "label_y": 814, "auth": "count"},
        ]},
    ]},
    "2020": {"source_file": "2020.pdf", "report_year": 2020, "pages": [
        {"page": 14, "layout": "bars", "data_year": 2020, "regions": [
            {"x": (100, 1860), "y": (120, 519), "label_y": 518, "auth": "size"},
            {"x": (100, 1860), "y": (580, 984), "label_y": 983, "auth": "count"},
        ]},
    ]},
    "2021": {"source_file": "2021.pdf", "report_year": 2021, "pages": [
        {"page": 9, "layout": "bars", "data_year": 2021, "regions": [
            {"x": (1000, 1860), "y": (130, 450), "label_y": 449, "auth": "size"},
            {"x": (1000, 1860), "y": (595, 931), "label_y": 930, "auth": "count"},
        ]},
    ]},
    "2022": {"source_file": "2022.pdf", "report_year": 2022, "pages": [
        {"page": 11, "layout": "bars", "data_year": 2022, "regions": [
            {"x": (1000, 1860), "y": (115, 454), "label_y": 453, "auth": "size"},
            {"x": (1000, 1860), "y": (595, 931), "label_y": 930, "auth": "count"},
        ]},
    ]},
    "2023": {"source_file": "2023.pdf", "report_year": 2023, "pages": [
        {"page": 14, "layout": "matrix", "metric": "size"},
        {"page": 15, "layout": "matrix", "metric": "count"},
    ]},
    "2024": {"source_file": "2024.pdf", "report_year": 2024, "pages": [
        {"page": 12, "layout": "matrix", "metric": "size"},
        {"page": 13, "layout": "matrix", "metric": "count"},
    ]},
    "2025": {"source_file": "2025.pdf", "report_year": 2025, "pages": [
        {"page": 12, "layout": "matrix", "metric": "size"},
        {"page": 13, "layout": "matrix", "metric": "count"},
    ]},
    "2026q1": {"source_file": "2026q1.pdf", "report_year": 2026, "pages": [
        {"page": 9, "layout": "matrix", "metric": "size"},
        {"page": 10, "layout": "matrix", "metric": "count"},  # KI-001 -> SKIP
    ]},
    "2026q2": {"source_file": "2026q2.pdf", "report_year": 2026, "pages": [
        {"page": 6, "layout": "matrix", "metric": "size"},
        {"page": 7, "layout": "matrix", "metric": "count"},
    ]},
}


def load_dim():
    """raw_name -> canonical_name (case-insensitive arama için normalize)."""
    m = {}
    with open(DIM, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m[r["raw_name"].strip().lower()] = r["canonical_name"].strip()
    return m


def words_of(page):
    return [w for w in page.get_text("words") if w[4].strip()]


def rows_of(words, tol):
    words = sorted(words, key=lambda t: (t[1], t[0]))
    out, cur, cy = [], [], None
    for wd in words:
        if cy is None or abs(wd[1] - cy) <= tol:
            cur.append(wd)
            cy = wd[1] if cy is None else cy
        else:
            out.append((cy, cur))
            cur, cy = [wd], wd[1]
    if cur:
        out.append((cy, cur))
    return out


def group_by_gap(items, gap):
    """[(x0,x1,text)] -> [(cx, text)] ; büyük x boşluğundan böl."""
    out, cur = [], []
    for x0, x1, t in sorted(items):
        if cur and x0 - cur[-1][1] > gap:
            out.append(((cur[0][0] + cur[-1][1]) / 2,
                        " ".join(v[2] for v in cur)))
            cur = []
        cur.append((x0, x1, t))
    if cur:
        out.append(((cur[0][0] + cur[-1][1]) / 2, " ".join(v[2] for v in cur)))
    return out


def parse_value(t, kind):
    m = MONEY_RE.match(t)
    if m and kind == "size":
        return float(m.group(1)) * MULT.get((m.group(2) or "").upper(), 1.0)
    if not m and COUNT_RE.match(t) and kind == "count":
        return float(t)
    return None


# --------------------------------------------------------------- matrix

def do_matrix(page, pg, out, spec):
    words = words_of(page)
    kind = pg["metric"]
    header = None
    for y, rw in rows_of(words, page.rect.height * 0.006):
        ticks = [w for w in rw if TICK_RE.match(w[4])]
        if len(ticks) >= 4:
            ticks.sort(key=lambda w: w[0])
            header = (y, [{"label": t[4], "cx": (t[0] + t[2]) / 2} for t in ticks])
            break
    if header is None:
        out["flags"].append(f"p{pg['page']}: yıl başlığı bulunamadı")
        return []
    hy, cols = header
    centers = [c["cx"] for c in cols]
    pitch = (centers[-1] - centers[0]) / max(len(centers) - 1, 1)
    left_bound = centers[0] - pitch * 0.5

    rows = [(y, rw) for y, rw in rows_of(words, page.rect.height * 0.004) if y > hy]
    # Değer satırı = kolonların NEREDEYSE HEPSİ dolu. Eşik düşük tutulursa
    # düzyazı satırları da yakalanır: 2024 p13'te "BiGG Fund made 42
    # investments in biotech, 32 in healthtech, and 27 in ..." üç sayı taşıyor.
    need = len(cols) - 1
    vrows = []
    for y, rw in rows:
        vals = [(w, parse_value(w[4], kind)) for w in rw
                if (w[0] + w[2]) / 2 > left_bound]
        vals = [(w, v) for w, v in vals if v is not None]
        if len(vals) >= need:
            vrows.append((y, vals))
    if not vrows:
        out["flags"].append(f"p{pg['page']}: değer satırı bulunamadı")
        return []
    rpitch = ((vrows[-1][0] - vrows[0][0]) / max(len(vrows) - 1, 1)) or 50.0

    recs = []
    for y, vals in vrows:
        label = [w for yy, rw in rows for w in rw
                 if (w[0] + w[2]) / 2 <= left_bound
                 and abs(w[1] - y) <= rpitch * 0.55]
        label.sort(key=lambda w: (w[1], w[0]))
        name = " ".join(w[4] for w in label).strip()
        if not name:
            out["flags"].append(f"p{pg['page']}: y={y:.0f} satırının etiketi yok")
            continue
        seen = {}
        for w, v in vals:
            cx = (w[0] + w[2]) / 2
            j = min(range(len(centers)), key=lambda k: abs(centers[k] - cx))
            if abs(centers[j] - cx) > pitch * 0.5:
                continue          # (BiGG) gibi kolon dışı ek — atla
            seen[cols[j]["label"]] = (v, w[4])
        for tick, (v, raw) in seen.items():
            dy, period = parse_tick(tick)
            recs.append({"raw_name": name, "data_year": dy, "period": period,
                         "kind": kind, "value": v, "raw": raw,
                         "page": pg["page"], "auth": True})
    return recs


# ----------------------------------------------------------------- bars

def do_bars(page, pg, out, spec):
    words = words_of(page)
    recs = []
    for reg in pg["regions"]:
        (xl, xh), (yl, yh) = reg["x"], reg["y"]
        inreg = [w for w in words
                 if xl <= (w[0] + w[2]) / 2 <= xh and yl <= w[1] <= yh]
        lab = [w for w in inreg if abs(w[1] - reg["label_y"]) <= 12]
        cats = group_by_gap([(w[0], w[2], w[4]) for w in lab], 9)
        if len(cats) < 3:
            out["flags"].append(
                f"p{pg['page']}: {reg['auth']} grafiğinde kategori bulunamadı")
            continue
        cxs = [c[0] for c in cats]
        pitch = (cxs[-1] - cxs[0]) / max(len(cxs) - 1, 1)
        for w in inreg:
            if w[1] >= reg["label_y"] - 12:
                continue
            for kind in ("size", "count"):
                v = parse_value(w[4], kind)
                if v is None:
                    continue
                cx = (w[0] + w[2]) / 2
                j = min(range(len(cxs)), key=lambda k: abs(cxs[k] - cx))
                if abs(cxs[j] - cx) > pitch * 0.5:
                    continue
                recs.append({"raw_name": cats[j][1], "data_year": pg["data_year"],
                             "period": "FY", "kind": kind, "value": v,
                             "raw": w[4], "page": pg["page"],
                             "auth": reg["auth"] == kind})
    return recs


# --------------------------------------------------------------- hbar18

DEALS_RE = re.compile(r"^\((\d+)$")
PROSE_RE = re.compile(
    r"^([A-Za-z][A-Za-z \-]+?)\s*:\s*\$(\d+(?:\.\d+)?)M\s*,?\s*(\d+)\s*deals?",
    re.I)
PROSE_X = 1000      # düzyazı madde işaretleri sayfanın sağ yarısında


def do_hbar18(page, pg, out, spec):
    words = words_of(page)
    recs = []
    # 1) grafik: sol kenardaki etiket (x<=240) + "(N deals)" anotasyonu, y ile eşleş
    labels = [w for w in words if w[2] <= 240 and w[1] > 150]
    ann = [(w[1], int(DEALS_RE.match(w[4]).group(1)), w[4])
           for w in words if DEALS_RE.match(w[4])]
    for y, name in group_rows_by_y(labels):
        near = [a for a in ann if abs(a[0] - y) <= 20]
        if len(near) != 1:
            out["flags"].append(f"p{pg['page']}: '{name}' için deal sayısı eşleşmedi")
            continue
        recs.append({"raw_name": name, "data_year": 2018, "period": "FY",
                     "kind": "count", "value": float(near[0][1]),
                     "raw": f"{near[0][1]} deals", "page": pg["page"],
                     "auth": True})

    # 2) düzyazı maddeleri: "•Foodtech : $1M , 6 deals"
    # Okuma sırasına GÜVENİLMEZ: madde iki satıra sarıyor ve araya sol taraftaki
    # grafik etiketleri giriyor. Bu yüzden madde blokları y ile kümelenir,
    # blok içi sıralama X'e göre yapılır (madde soldan sağa okunur).
    prose = [w for w in words if w[0] >= PROSE_X and w[1] > 700]
    for _y, blk in group_blocks(prose, tol=20):
        if not any("$" in w[4] for w in blk):
            continue          # altbilgi/sayfa no gibi bloklar
        line = " ".join(w[4] for w in sorted(blk, key=lambda w: w[0]))
        line = line.replace("•", " ").strip()
        m = PROSE_RE.match(line)
        if not m:
            out["flags"].append(f"p{pg['page']}: düzyazı maddesi çözülemedi: {line[:60]!r}")
            continue
        name = m.group(1).strip()
        recs.append({"raw_name": name, "data_year": 2018, "period": "FY",
                     "kind": "size", "value": float(m.group(2)) * 1e6,
                     "raw": f"${m.group(2)}M", "page": pg["page"], "auth": True})
        recs.append({"raw_name": name, "data_year": 2018, "period": "FY",
                     "kind": "count", "value": float(m.group(3)),
                     "raw": f"{m.group(3)} deals", "page": pg["page"],
                     "auth": True})
    return recs


def group_blocks(ws, tol):
    """Kelimeleri y'ye göre bloklara ayır; blok içi sıra çağırana bırakılır."""
    out, cur, cy = [], [], None
    for w in sorted(ws, key=lambda w: w[1]):
        if cy is None or w[1] - cy <= tol:
            cur.append(w)
            cy = w[1] if cy is None else cy
        else:
            out.append((cy, cur))
            cur, cy = [w], w[1]
    if cur:
        out.append((cy, cur))
    return out


def group_rows_by_y(ws, tol=14):
    out, cur, cy = [], [], None
    for w in sorted(ws, key=lambda w: (w[1], w[0])):
        if cy is None or abs(w[1] - cy) <= tol:
            cur.append(w)
            cy = w[1] if cy is None else cy
        else:
            out.append((cy, " ".join(v[4] for v in cur)))
            cur, cy = [w], w[1]
    if cur:
        out.append((cy, " ".join(v[4] for v in cur)))
    return out


HANDLERS = {"matrix": do_matrix, "bars": do_bars, "hbar18": do_hbar18}


def extract(report_id):
    spec = SPECS[report_id]
    dim = load_dim()
    doc = fitz.open(os.path.join(ROOT, "raw", spec["source_file"]))
    out = {"report_id": report_id, "source_file": spec["source_file"],
           "report_year": spec["report_year"], "rows": [], "flags": [],
           "unmapped": []}

    recs = []
    for pg in spec["pages"]:
        issue = PAGE_ISSUES.get((spec["source_file"], pg["page"]))
        if issue:
            code, action, msg = issue
            out["flags"].append(f"p{pg['page']}: {code} ({action}) — {msg}")
            if action == "SKIP":
                continue
        recs += HANDLERS[pg["layout"]](doc[pg["page"] - 1], pg, out, spec)

    # canonical eşleme + çakışma çözümü
    best = {}
    for r in recs:
        canon = dim.get(r["raw_name"].strip().lower())
        if canon is None:
            if r["raw_name"] not in out["unmapped"]:
                out["unmapped"].append(r["raw_name"])
            out["flags"].append(
                f"p{r['page']}: '{r['raw_name']}' dim_verticals.csv'de yok — atlandı")
            continue
        key = (r["data_year"], r["period"], r["kind"], canon)
        prev = best.get(key)
        if prev is None:
            best[key] = dict(r, canon=canon, conflict=False)
        elif abs(prev["value"] - r["value"]) < 1e-6:
            pass                                   # aynı değer, sorun yok
        else:
            # iki grafik farklı değer veriyor: sıralama metriğinde otorite kazanır
            win = r if r["auth"] and not prev["auth"] else prev
            lose = prev if win is r else r
            best[key] = dict(win, canon=canon, conflict=True)
            out["flags"].append(
                f"ÇAKIŞMA {canon} {r['data_year']} {r['kind']}: "
                f"p{prev['page']}={prev['raw']} vs p{r['page']}={r['raw']} "
                f"-> otorite grafiği seçildi ({win['raw']}), confidence=low")

    for (dy, period, kind, canon), r in sorted(best.items()):
        out["rows"].append({
            "data_year": dy, "period": period, "report_id": report_id,
            "report_year": spec["report_year"], "metric": METRIC[kind],
            "dim_type": "vertical", "dim_value_raw": r["raw_name"],
            "dim_value_canon": canon, "scope": "all",
            "unit": "usd" if kind == "size" else "count",
            "value": r["value"], "source_file": spec["source_file"],
            "page": r["page"],
            "confidence": "low" if r["conflict"] else "high",
            "is_provisional": "FALSE", "_raw": r["raw"],
        })
    mark_provisional(out["rows"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report_id", choices=sorted(SPECS))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    out = extract(a.report_id)
    os.makedirs(EXTRACTED, exist_ok=True)
    dst = os.path.join(EXTRACTED, f"{a.report_id}_verticals.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"{a.report_id}: {len(out['rows'])} satır -> {dst}")
    for fl in out["flags"]:
        print(f"  FLAG {fl}")
    if a.write:
        n, sk = append_facts(out["rows"])
        print(f"  facts.csv: +{n} satır, {sk} atlandı")
    else:
        print("  (--write verilmedi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
