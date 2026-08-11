#!/usr/bin/env python3
"""facts.csv -> sheets/ (Google Sheets'e yüklenecek 4 düz CSV).

Üretilenler:
  sheets/facts.csv        ham, TÜM vintage'lar (hiçbir şey elenmez)
  sheets/latest.csv       her ölçüm için EN GÜNCEL vintage — pivot'a hazır
  sheets/dim_verticals.csv tag harmonizasyon eşlemesi
  sheets/revisions.csv    aynı ölçümün vintage'lar arası değişimi

latest.csv düz (long) formattadır: Sheets pivot'unda
  satır = dim_value_canon, kolon = period_label, değer = value
kurulabilir. Filtre kolonları: metric, scope, period, is_comparable_fy.

period_label neden var: FY yılı ile kısmi dönem (2026-H1) AYNI kolonda
görünmemeli. Etiketi ayırmak, pivot'ta yanlışlıkla yan yana gelmelerini
engeller (CLAUDE.md: kısmi yıl tamamlanmış yıl gibi görünmemeli).

Kullanım:
    .venv/bin/python scripts/build_sheets.py
"""
import csv
import os
import re
import shutil
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "facts.csv")
DIM = os.path.join(ROOT, "dim_verticals.csv")
OUT = os.path.join(ROOT, "sheets")

# Ölçümü tanımlayan anahtar (vintage HARİÇ) — latest/revisions bunun üzerinden
MEASURE_KEY = ("data_year", "period", "metric", "dim_value_canon", "scope",
               "unit")

LATEST_COLS = ["data_year", "period", "period_label", "is_comparable_fy",
               "metric", "dim_type", "dim_value_canon", "dim_value_raw",
               "scope", "unit", "value", "report_id", "report_year",
               "is_provisional", "confidence", "source_file", "page"]

REVISION_COLS = ["data_year", "period", "period_label", "metric",
                 "dim_value_canon", "scope", "unit", "from_report_id",
                 "from_value", "to_report_id", "to_value", "delta",
                 "delta_pct", "is_latest_step", "n_vintages"]

QSUF = re.compile(r"^(\d{4})(?:q([1-4]))?$")


def vintage_rank(report_id):
    """Vintage sırası. Aynı yılın çeyrekliği yıllıktan ÖNCE gelir:
    2026q1 < 2026q2 < 2026(yıllık). Yıllık raporu 9 ile işaretliyoruz."""
    m = QSUF.match(report_id)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else 9)


def period_label(data_year, period):
    return str(data_year) if period == "FY" else f"{data_year}-{period}"


def main():
    if not os.path.exists(FACTS):
        sys.exit("facts.csv yok — önce extract çalıştır")
    os.makedirs(OUT, exist_ok=True)
    rows = list(csv.DictReader(open(FACTS, newline="", encoding="utf-8")))

    # 1) ham
    shutil.copyfile(FACTS, os.path.join(OUT, "facts.csv"))
    # 3) dim
    shutil.copyfile(DIM, os.path.join(OUT, "dim_verticals.csv"))

    # ölçüm başına vintage'lar
    by = defaultdict(list)
    for r in rows:
        by[tuple(r[k] for k in MEASURE_KEY)].append(r)
    for v in by.values():
        v.sort(key=lambda r: vintage_rank(r["report_id"]))

    # 2) latest
    latest = []
    for key, vints in by.items():
        r = vints[-1]
        latest.append({
            "data_year": r["data_year"], "period": r["period"],
            "period_label": period_label(r["data_year"], r["period"]),
            "is_comparable_fy": "TRUE" if r["period"] == "FY" else "FALSE",
            "metric": r["metric"], "dim_type": r["dim_type"],
            "dim_value_canon": r["dim_value_canon"],
            "dim_value_raw": r["dim_value_raw"], "scope": r["scope"],
            "unit": r["unit"], "value": r["value"],
            "report_id": r["report_id"], "report_year": r["report_year"],
            "is_provisional": r["is_provisional"],
            "confidence": r["confidence"], "source_file": r["source_file"],
            "page": r["page"],
        })
    latest.sort(key=lambda r: (r["metric"], r["scope"], r["dim_value_canon"],
                               int(r["data_year"]), r["period"]))
    write(os.path.join(OUT, "latest.csv"), LATEST_COLS, latest)

    # 4) revisions — ardışık vintage çiftleri
    revs = []
    for key, vints in by.items():
        if len(vints) < 2:
            continue
        for i in range(len(vints) - 1):
            a, b = vints[i], vints[i + 1]
            av, bv = float(a["value"]), float(b["value"])
            if av == bv:
                continue
            revs.append({
                "data_year": a["data_year"], "period": a["period"],
                "period_label": period_label(a["data_year"], a["period"]),
                "metric": a["metric"],
                "dim_value_canon": a["dim_value_canon"], "scope": a["scope"],
                "unit": a["unit"],
                "from_report_id": a["report_id"], "from_value": a["value"],
                "to_report_id": b["report_id"], "to_value": b["value"],
                "delta": f"{bv - av:.6g}",
                "delta_pct": f"{100.0 * (bv - av) / av:.2f}" if av else "",
                "is_latest_step": "TRUE" if i == len(vints) - 2 else "FALSE",
                "n_vintages": len(vints),
            })
    revs.sort(key=lambda r: -abs(float(r["delta_pct"] or 0)))
    write(os.path.join(OUT, "revisions.csv"), REVISION_COLS, revs)

    for name in ("facts.csv", "latest.csv", "dim_verticals.csv",
                 "revisions.csv"):
        path = os.path.join(OUT, name)
        n = sum(1 for _ in open(path, encoding="utf-8")) - 1
        print(f"  sheets/{name:20s} {n:5d} satır")
    return 0


def write(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    sys.exit(main())
