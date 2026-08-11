#!/usr/bin/env python3
"""sheets/*.csv -> docs/data/*.json  (GitHub Pages statik sitesi için)

build_sheets.py'den SONRA çalışır. Site private repo'dan veri çekmez —
veri build sırasında docs/ altına kopyalanır, runtime'da token gerekmez.

Üretilenler:
  docs/data/data.json   sitenin tek veri kaynağı
  docs/data/*.csv       ham CSV'ler (siteden "indir" bağlantısı için)

Kullanım:
    .venv/bin/python scripts/build_site.py
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = os.path.join(ROOT, "sheets")
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(DOCS, "data")

TOTAL_ID = "__total__"
QSUF = re.compile(r"^(\d{4})(?:q([1-4]))?$")

# facts metrik adı -> (site metriği, vertical kimliği)
METRIC_MAP = {
    "funding_by_vertical_size":  ("size", None),
    "funding_by_vertical_count": ("count", None),
    "total_deal_size":           ("size", TOTAL_ID),
    "total_deal_count":          ("count", TOTAL_ID),
}


def vintage_rank(report_id):
    """Aynı yılın çeyrekliği yıllıktan ÖNCE gelir: 2026q1 < 2026q2 < 2026."""
    m = QSUF.match(report_id or "")
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else 9)


def read(name):
    with open(os.path.join(SHEETS, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def label_for(canon, raws_by_vintage):
    """Görünen ad = EN GÜNCEL vintage'ın kullandığı ham ad.

    Taksonomi zamanla değişiyor (AI -> Artificial intelligence,
    Game -> Gaming); en yeni raporun terminolojisi doğru olandır.
    """
    if not raws_by_vintage:
        return canon.replace("_", " ").title()
    best = max(raws_by_vintage, key=lambda t: vintage_rank(t[0]))
    return best[1]


def git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


def main():
    if not os.path.isdir(SHEETS):
        sys.exit("sheets/ yok — önce build_sheets.py çalıştır")
    os.makedirs(DATA, exist_ok=True)

    latest = read("latest.csv")
    facts = read("facts.csv")
    revisions = read("revisions.csv")
    dim = read("dim_verticals.csv")

    # --- vintage derinliği: bir ölçümün kaç farklı raporda yayınlandığı ----
    vintages = defaultdict(set)
    for r in facts:
        m = METRIC_MAP.get(r["metric"])
        if not m:
            continue
        vid = m[1] or r["dim_value_canon"]
        vintages[(m[0], r["scope"], vid, r["period_label"] if "period_label" in r
                  else _plabel(r))].add(r["report_id"])

    # --- önceki vintage değeri (hover'da "revize edildi" göstermek için) ---
    prev = {}
    for r in revisions:
        if r["is_latest_step"] != "TRUE":
            continue
        m = METRIC_MAP.get(r["metric"])
        if not m:
            continue
        vid = m[1] or r["dim_value_canon"]
        prev[(m[0], r["scope"], vid, r["period_label"])] = {
            "rid": r["from_report_id"], "val": float(r["from_value"]),
            "pct": float(r["delta_pct"]) if r["delta_pct"] else None,
        }

    # --- dönemler ---------------------------------------------------------
    periods = {}
    for r in latest:
        periods[r["period_label"]] = (r["is_comparable_fy"] == "TRUE")
    # Kronolojik sıra: FY, sonra Q1..Q4, sonra H1. Düz alfabetik sıralama
    # "2026-H1"i "2026-Q1"in önüne atardı (H < Q).
    prank = {"": 0, "Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "H1": 5}
    plist = sorted(periods, key=lambda p: (int(p[:4]),
                                           prank.get(p[5:], 9)))
    period_meta = [{"id": p, "fy": periods[p]} for p in plist]

    # --- sektör boyutu ----------------------------------------------------
    raws = defaultdict(list)
    for r in latest:
        if r["dim_type"] == "vertical" and r["dim_value_raw"]:
            raws[r["dim_value_canon"]].append((r["report_id"], r["dim_value_raw"]))
    dim_meta = {}
    for d in dim:
        c = d["canonical_name"]
        dim_meta.setdefault(c, {"first": d["first_seen_report"],
                                "from": d["comparable_from"], "notes": []})
        if d["notes"]:
            dim_meta[c]["notes"].append(d["notes"])

    used = sorted({r["dim_value_canon"] for r in latest
                   if r["dim_type"] == "vertical" and r["dim_value_canon"]})
    verticals = [{
        "id": c,
        "label": label_for(c, raws.get(c, [])),
        "first": dim_meta.get(c, {}).get("first", ""),
        "from": dim_meta.get(c, {}).get("from", ""),
        "note": " · ".join(dim_meta.get(c, {}).get("notes", []))[:300],
    } for c in used]
    verticals.insert(0, {
        "id": TOTAL_ID, "label": "Tüm ekosistem (toplam)",
        "first": "", "from": "",
        "note": "Raporun kendi headline toplamı. Sektör satırlarının toplamı DEĞİLDİR "
                "— sektör tag'leri birbirini dışlamaz.",
    })

    # --- ölçüm satırları --------------------------------------------------
    rows, avail = [], defaultdict(set)
    for r in latest:
        m = METRIC_MAP.get(r["metric"])
        if not m:
            continue
        metric, forced = m
        vid = forced or r["dim_value_canon"]
        if not vid:
            continue
        key = (metric, r["scope"], vid, r["period_label"])
        row = {
            "m": metric, "s": r["scope"], "v": vid, "p": r["period_label"],
            "val": float(r["value"]), "r": r["report_id"],
            "pv": 1 if r["is_provisional"] == "TRUE" else 0,
        }
        if r["confidence"] != "high":
            row["c"] = r["confidence"]
        nv = len(vintages.get(key, ()))
        if nv > 1:
            row["nv"] = nv
        if key in prev:
            row["pr"] = prev[key]
        rows.append(row)
        avail[(metric, r["scope"])].add(vid)

    # sektör kırılımı hangi kapsamlarda VAR? (ex_getir_bigg'de yok)
    scope_meta = []
    for sid, label in (("all", "Tümü"),
                       ("ex_getir_bigg", "Getir & BiGG hariç")):
        has_v = any(v != TOTAL_ID for v in avail.get(("size", sid), ()))
        scope_meta.append({"id": sid, "label": label, "verticals": has_v})

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "commit": git_commit(),
        "counts": {"facts": len(facts), "latest": len(latest),
                   "verticals": len(used), "revisions": len(revisions)},
        "metrics": [
            {"id": "size", "label": "Yatırım tutarı", "unit": "usd"},
            {"id": "count", "label": "Deal sayısı", "unit": "count"},
        ],
        "scopes": scope_meta,
        "periods": period_meta,
        "verticals": verticals,
        "rows": rows,
    }

    dst = os.path.join(DATA, "data.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    for name in ("facts.csv", "latest.csv", "dim_verticals.csv", "revisions.csv"):
        shutil.copyfile(os.path.join(SHEETS, name), os.path.join(DATA, name))

    kb = os.path.getsize(dst) / 1024
    print(f"  docs/data/data.json   {len(rows):4d} ölçüm · {kb:.0f} KB")
    print(f"  docs/data/*.csv       4 ham dosya kopyalandı")
    print(f"  sektör: {len(used)} · dönem: {len(plist)} "
          f"({sum(1 for p in period_meta if p['fy'])} FY)")
    return 0


def _plabel(r):
    return r["data_year"] if r["period"] == "FY" else f"{r['data_year']}-{r['period']}"


if __name__ == "__main__":
    sys.exit(main())
