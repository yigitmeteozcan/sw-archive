#!/usr/bin/env python3
"""Headline metrik çıkarımı — ONE report at a time (Altın kural).

PDF'i kod okur, model sadece çıkan sayıları görür. Grafik etiketleri okuma
sırasına göre DEĞİL, x-konumuna göre yıl tick'ine bağlanır (etiketler bar
yüksekliğine göre farklı y'lerde durur; okuma sırası yılları karıştırır).

Sayfa düzeni: her grafiğin altında bir yıl ekseni satırı var. Eksen satırı
grafiği hem tanımlar hem sınırlar:
  - y aralığı : bir önceki eksenden bu eksene kadar
  - x aralığı : tick'lerin min/max'ı ± yarım tick
Bu sınır şart — 2024 p5'te sağdaki düzyazıda "made 231 pre-seed investments"
ve "$2.5B" geçiyor; sınırsız tarama bunları veri sanar.

Kullanım:
    .venv/bin/python scripts/extract_facts.py 2024
    .venv/bin/python scripts/extract_facts.py 2024 --write   # facts.csv'ye append
"""
import argparse
import csv
import json
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "facts.csv")
EXTRACTED = os.path.join(ROOT, "extracted")

FACTS_COLS = ["data_year", "period", "report_id", "report_year", "metric",
              "dim_type", "dim_value_raw", "dim_value_canon", "scope", "unit",
              "value", "source_file", "page", "confidence", "is_provisional"]

# KNOWN_ISSUES.md kayıtları — bu sayfalara dokunan çıkarım uyarı basar.
PAGE_ISSUES = {
    ("2026q1.pdf", 10): ("KI-001", "SKIP",
                         "yıl başlıkları bir kolon kaymış; aynı veri "
                         "2026q2.pdf p7'de doğru başlıklarla var"),
    ("2025.pdf", 13): ("KI-002", "WARN",
                       "sayfa başlığındaki yıl yanlış (2024 yazıyor); "
                       "kolon başlıkları doğru, çıkarıma devam"),
}

# Eksen tick'i: "2024" ya da "2026-H1" / "2026-Q1"
TICK_RE = re.compile(r"^(19|20)\d{2}(-(Q[1-4]|H1))?$")
MONEY_RE = re.compile(r"^\$\s?(\d+(?:\.\d+)?)\s?([KMB])$", re.I)
COUNT_RE = re.compile(r"^\d{1,4}$")
MULT = {"K": 1e3, "M": 1e6, "B": 1e9}

# Rapor tanımları. Grafik sırası sayfada yukarıdan aşağıya.
SPECS = {
    "2024": {
        "source_file": "2024.pdf", "report_year": 2024,
        "pages": [{"page": 4, "scopes": ["all"]},
                  {"page": 5, "scopes": ["ex_getir_bigg"]}],
    },
    "2025": {
        "source_file": "2025.pdf", "report_year": 2025,
        "pages": [{"page": 5, "scopes": ["all", "ex_getir_bigg"]}],
    },
    "2026q2": {
        "source_file": "2026q2.pdf", "report_year": 2026,
        "pages": [{"page": 4, "scopes": ["all", "ex_getir_bigg"]}],
    },
}


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


def parse_tick(t):
    """'2024' -> (2024,'FY') ; '2026-H1' -> (2026,'H1')"""
    if "-" in t:
        y, p = t.split("-", 1)
        return int(y), p
    return int(t), "FY"


def find_charts(page):
    """Sayfadaki her yıl-ekseni satırı için bir grafik bölgesi döndür."""
    words = [w for w in page.get_text("words") if w[4].strip()]
    charts, prev_y = [], 0.0
    for y, rw in rows_of(words, page.rect.height * 0.006):
        ticks = [w for w in rw if TICK_RE.match(w[4])]
        if len(ticks) < 4:
            continue
        ticks.sort(key=lambda w: w[0])
        span = [(t[0] + t[2]) / 2 for t in ticks]
        pitch = (span[-1] - span[0]) / max(len(span) - 1, 1)
        charts.append({
            "axis_y": y, "y_hi": prev_y, "y_lo": y,
            "x_lo": span[0] - pitch * 0.6, "x_hi": span[-1] + pitch * 0.6,
            "ticks": [{"label": t[4], "cx": (t[0] + t[2]) / 2} for t in ticks],
        })
        prev_y = y
    return words, charts


def collect(words, chart):
    """Grafik bölgesindeki para ve sayı etiketlerini tick'lere bağla."""
    series = {"total_deal_size": {}, "total_deal_count": {}}
    dupes = []
    for x0, y0, x1, y1, t, *_ in words:
        if not (chart["y_hi"] < y0 < chart["y_lo"]):
            continue
        cx = (x0 + x1) / 2
        if not (chart["x_lo"] <= cx <= chart["x_hi"]):
            continue
        t = t.strip()
        if TICK_RE.match(t):
            continue
        m = MONEY_RE.match(t)
        if m:
            metric, val = "total_deal_size", float(m.group(1)) * MULT[m.group(2).upper()]
        elif COUNT_RE.match(t):
            metric, val = "total_deal_count", float(t)
        else:
            continue
        j = min(range(len(chart["ticks"])),
                key=lambda k: abs(chart["ticks"][k]["cx"] - cx))
        key = chart["ticks"][j]["label"]
        if key in series[metric]:
            dupes.append((metric, key, series[metric][key]["raw"], t))
        series[metric][key] = {"value": val, "raw": t}
    return series, dupes


def extract(report_id):
    spec = SPECS[report_id]
    path = os.path.join(ROOT, "raw", spec["source_file"])
    doc = fitz.open(path)
    out = {"report_id": report_id, "source_file": spec["source_file"],
           "report_year": spec["report_year"], "rows": [], "flags": []}

    for pg in spec["pages"]:
        issue = PAGE_ISSUES.get((spec["source_file"], pg["page"]))
        if issue:
            code, action, msg = issue
            out["flags"].append(f"p{pg['page']}: {code} ({action}) — {msg}")
            if action == "SKIP":
                continue
        page = doc[pg["page"] - 1]
        words, charts = find_charts(page)
        if len(charts) != len(pg["scopes"]):
            out["flags"].append(
                f"p{pg['page']}: {len(charts)} grafik bulundu, "
                f"{len(pg['scopes'])} scope bekleniyordu — spec gözden geçir")
        for chart, scope in zip(charts, pg["scopes"]):
            series, dupes = collect(words, chart)
            for metric, vals in series.items():
                for tick in chart["ticks"]:
                    lbl = tick["label"]
                    dy, period = parse_tick(lbl)
                    hit = vals.get(lbl)
                    if hit is None:
                        # Okunamayan sayıyı TAHMİN ETME (CLAUDE.md yasak).
                        out["flags"].append(
                            f"p{pg['page']} {scope} {metric} {lbl}: etiket yok")
                        continue
                    conf = "high"
                    if any(d[0] == metric and d[1] == lbl for d in dupes):
                        conf = "low"
                        out["flags"].append(
                            f"p{pg['page']} {scope} {metric} {lbl}: "
                            f"birden fazla etiket eşleşti")
                    out["rows"].append({
                        "data_year": dy, "period": period,
                        "report_id": report_id,
                        "report_year": spec["report_year"], "metric": metric,
                        "dim_type": "none", "dim_value_raw": "",
                        "dim_value_canon": "", "scope": scope,
                        "unit": "usd" if metric == "total_deal_size" else "count",
                        "value": hit["value"], "source_file": spec["source_file"],
                        "page": pg["page"], "confidence": conf,
                        "is_provisional": "FALSE",
                        "_raw": hit["raw"],
                    })
    mark_provisional(out["rows"])
    return out


def mark_provisional(rows):
    """Raporun EN SON data_year'ına ait tüm satırlar provisional."""
    if not rows:
        return
    last = max(r["data_year"] for r in rows)
    for r in rows:
        r["is_provisional"] = "TRUE" if r["data_year"] == last else "FALSE"


def append_facts(rows):
    """Append-only; dosyada zaten olan anahtarı atla (idempotent).

    Batch İÇİNDE aynı anahtarın iki kez üretilmesi ayrı bir durumdur: bu
    şema hatasıdır, atlanırsa veri SESSİZCE kaybolur. Bir kez böyle oldu —
    verticals'ta $ ve # satırları tek metrik adı altındaydı ve unique anahtar
    unit içermediği için biri düştü. O yüzden burada sessizce atlamak yerine
    hata veriyoruz.
    """
    existing = set()
    if os.path.exists(FACTS):
        with open(FACTS, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                existing.add((r["data_year"], r["period"], r["report_id"],
                              r["metric"], r["dim_value_canon"], r["scope"]))
    new, skipped, batch = [], 0, {}
    for r in rows:
        key = (str(r["data_year"]), r["period"], str(r["report_id"]),
               r["metric"], r["dim_value_canon"], r["scope"])
        if key in batch:
            raise SystemExit(
                f"HATA: aynı batch'te tekrar eden unique anahtar {key}\n"
                f"  önceki: unit={batch[key]['unit']} value={batch[key]['value']}\n"
                f"  şimdi : unit={r['unit']} value={r['value']}\n"
                "  Anahtar unit içermiyor — metrik adı ölçü tabanını taşımalı "
                "(ör. ..._size / ..._count).")
        batch[key] = r
        if key in existing:
            skipped += 1
            continue
        existing.add(key)
        new.append({k: r[k] for k in FACTS_COLS})
    fresh = not os.path.exists(FACTS)
    with open(FACTS, "a", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=FACTS_COLS)
        if fresh:
            wr.writeheader()
        wr.writerows(new)
    return len(new), skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report_id", choices=sorted(SPECS))
    ap.add_argument("--write", action="store_true", help="facts.csv'ye append et")
    a = ap.parse_args()

    out = extract(a.report_id)
    os.makedirs(EXTRACTED, exist_ok=True)
    dst = os.path.join(EXTRACTED, f"{a.report_id}.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"{a.report_id}: {len(out['rows'])} satır -> {dst}")
    for fl in out["flags"]:
        print(f"  FLAG {fl}")
    if a.write:
        n, sk = append_facts(out["rows"])
        print(f"  facts.csv: +{n} satır, {sk} atlandı (zaten var)")
    else:
        print("  (--write verilmedi, facts.csv'ye yazılmadı)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
