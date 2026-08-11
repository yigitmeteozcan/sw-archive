#!/usr/bin/env python3
"""facts.csv'yi kaynak PDF'e karşı BAĞIMSIZ doğrula.

NEDEN AYRI BİR YOL: extract_facts.py / extract_verticals.py'yi çağırmak ya da
extracted/*.json okumak doğrulama DEĞİL tekrardır — aynı parser aynı hatayı
iki kez yapar. Bu yüzden ikinci yol PDF'in TEXT KATMANINA HİÇ BAKMAZ:
sayfa piksel olarak render edilir, sayılar görsel olarak okunur, okunan
değerler facts.csv ile karşılaştırılır.

Görsel okuma adımı koda gömülemez; akış üç aşamalı:

  1) render   sayfaları PNG'ye çevirir + verify/worklist.md üretir
              (her sayfada facts.csv'nin NE İDDİA ETTİĞİ, okuyucuya rehber)
  2) [insan/model] PNG'lere bakıp verify/readings.json'u doldurur
              — okunan değerler EKRANDA YAZDIĞI GİBİ ("$1.2M", "469")
  3) compare  readings.json ile facts.csv'yi karşılaştırır,
              iç tutarlılık kontrollerini koşar, VERIFY.md +
              verify_report.csv üretir

Kullanım:
    .venv/bin/python scripts/verify_facts.py render
    .venv/bin/python scripts/verify_facts.py compare
    .venv/bin/python scripts/verify_facts.py checks     # yalnız iç tutarlılık
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "facts.csv")
DIM = os.path.join(ROOT, "dim_verticals.csv")
VDIR = os.path.join(ROOT, "verify")
PAGES = os.path.join(VDIR, "pages")
READINGS = os.path.join(VDIR, "readings.json")
REPORT = os.path.join(ROOT, "verify_report.csv")
MD = os.path.join(ROOT, "VERIFY.md")

TOL = 0.005          # %0.5 — basılı etiket yuvarlamasını soğurur
MULT = {"K": 1e3, "M": 1e6, "B": 1e9}
NUM = re.compile(r"^\$?\s*(-?\d+(?:[.,]\d+)?)\s*([KMB])?$", re.I)


def load_facts():
    with open(FACTS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def canon_map():
    m = {}
    with open(DIM, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m[r["raw_name"].strip().lower()] = r["canonical_name"].strip()
    return m


def parse_reading(s):
    """'$1.2M' -> 1200000.0 ; '469' -> 469.0 ; '' / '-' / 'N/A' -> None"""
    s = (s or "").strip()
    if s in ("", "-", "—", "N/A", "n/a", "?"):
        return None
    m = NUM.match(s.replace(",", "."))
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2):
        v *= MULT[m.group(2).upper()]
    return v


def plabel(r):
    return r["data_year"] if r["period"] == "FY" else f'{r["data_year"]}-{r["period"]}'


# ------------------------------------------------------------------ render

def do_render():
    facts = load_facts()
    os.makedirs(PAGES, exist_ok=True)
    by = defaultdict(list)
    for r in facts:
        by[(r["source_file"], int(r["page"]))].append(r)

    lines = ["# verify worklist", "",
             "Her sayfa için facts.csv'nin İDDİASI aşağıda. PNG'ye bakıp",
             "`verify/readings.json` doldurulacak. Değerler EKRANDA YAZDIĞI GİBİ",
             "yazılır (`$1.2M`, `469`); okunamıyorsa `\"?\"`.", ""]
    for (src, page), rows in sorted(by.items()):
        doc = fitz.open(os.path.join(ROOT, "raw", src))
        p = doc[page - 1]
        # 2x ölçek: küçük veri etiketleri okunabilir olsun
        name = f"{src.replace('.pdf','')}_p{page}.png"
        p.get_pixmap(matrix=fitz.Matrix(2, 2)).save(os.path.join(PAGES, name))
        doc.close()

        mets = sorted({r["metric"] for r in rows})
        scopes = sorted({r["scope"] for r in rows})
        vals = sorted({r["dim_value_canon"] for r in rows if r["dim_value_canon"]})
        yrs = sorted({plabel(r) for r in rows})
        lines += [f"## {src} p{page}  → `verify/pages/{name}`",
                  f"- satır: **{len(rows)}** · metrik: {', '.join(mets)}"
                  f" · scope: {', '.join(scopes)}",
                  f"- dönem: {', '.join(yrs)}",
                  f"- sektör ({len(vals)}): {', '.join(vals) if vals else '— (headline)'}",
                  ""]
    with open(os.path.join(VDIR, "worklist.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  {len(by)} sayfa render edildi -> verify/pages/")
    print(f"  rehber: verify/worklist.md")
    if not os.path.exists(READINGS):
        with open(READINGS, "w", encoding="utf-8") as f:
            json.dump({}, f)
        print("  boş verify/readings.json oluşturuldu")


# ----------------------------------------------------------------- compare

def do_compare():
    facts = load_facts()
    cmap = canon_map()
    if not os.path.exists(READINGS):
        sys.exit("verify/readings.json yok — önce `render`, sonra görsel okuma")
    readings = json.load(open(READINGS, encoding="utf-8"))

    # okunan değerleri facts anahtarına çevir
    read = {}          # (period_label, source_file, page, metric, canon, scope) -> (val, raw)
    unresolved = []
    for pkey, blk in readings.items():
        src, page = pkey.split("|")
        page = int(page)
        scope = blk.get("scope", "all")
        if blk.get("kind") == "headline":
            for metric, series in (("total_deal_size", blk.get("size", {})),
                                   ("total_deal_count", blk.get("count", {}))):
                for per, disp in series.items():
                    read[(per, src, page, metric, "", scope)] = (parse_reading(disp), disp)
        else:
            metric = ("funding_by_vertical_size" if blk.get("metric") == "size"
                      else "funding_by_vertical_count")
            for raw, series in blk.get("rows", {}).items():
                canon = cmap.get(raw.strip().lower())
                if canon is None:
                    unresolved.append((pkey, raw))
                    continue
                for per, disp in series.items():
                    read[(per, src, page, metric, canon, scope)] = (parse_reading(disp), disp)

    out, tally = [], defaultdict(int)
    for r in facts:
        k = (plabel(r), r["source_file"], int(r["page"]), r["metric"],
             r["dim_value_canon"], r["scope"])
        fv = float(r["value"])
        hit = read.pop(k, None)
        if hit is None:
            status, vv, note = "UNREADABLE", "", "görsel okuma kaydı yok"
        elif hit[0] is None:
            status, vv, note = "UNREADABLE", hit[1], "etiket okunamadı"
        else:
            vv = hit[1]
            denom = abs(fv) if fv else 1.0
            status = "OK" if abs(hit[0] - fv) / denom <= TOL else "MISMATCH"
            note = "" if status == "OK" else f"görsel={hit[0]:.6g} facts={fv:.6g}"
        tally[status] += 1
        out.append({
            "data_year": r["data_year"], "report_id": r["report_id"],
            "metric": r["metric"], "dim_value_canon": r["dim_value_canon"],
            "scope": r["scope"], "facts_value": r["value"], "verify_value": vv,
            "durum": status, "not": note,
        })

    # görsel okumada olup facts.csv'de olmayanlar
    extra = [(k, v) for k, v in read.items() if v[0] is not None]
    for k, v in extra:
        out.append({"data_year": k[0], "report_id": "", "metric": k[3],
                    "dim_value_canon": k[4], "scope": k[5], "facts_value": "",
                    "verify_value": v[1], "durum": "MISMATCH",
                    "not": "görselde var, facts.csv'de YOK"})
        tally["MISMATCH"] += 1

    with open(REPORT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["data_year", "report_id", "metric",
                                          "dim_value_canon", "scope", "facts_value",
                                          "verify_value", "durum", "not"])
        w.writeheader()
        w.writerows(out)

    checks = run_checks(facts)
    write_md(tally, out, checks, unresolved, len(facts))
    print(f"  {tally['OK']} OK · {tally['MISMATCH']} MISMATCH · "
          f"{tally['UNREADABLE']} UNREADABLE  (toplam {len(facts)})")
    for c in checks:
        print(f"  [{c['status']}] {c['name']}: {c['summary']}")
    return 1 if tally["MISMATCH"] else 0


# --------------------------------------------------- iç tutarlılık kontrolleri

def run_checks(facts):
    res = []
    num = lambda s: float(s) if s not in ("", None) else None

    # 1) raporda YAZAN YoY % ile facts'ten HESAPLANAN YoY %
    res.append(check_printed_yoy(facts))

    # 2) stage toplamı headline total'ı geçiyor mu
    stage = [r for r in facts if r["dim_type"] == "stage"]
    res.append({"name": "Stage toplamı ≤ headline total",
                "status": "N/A" if not stage else "?",
                "summary": "facts.csv'de stage kırılımı yok — kontrol uygulanamıyor"
                if not stage else f"{len(stage)} stage satırı"})

    # 3) vertical toplamı headline total'ın 3 katını geçiyor mu
    tot, vsum = {}, defaultdict(float)
    for r in facts:
        k = (r["data_year"], r["period"], r["report_id"], r["scope"])
        v = num(r["value"])
        if v is None:
            continue
        if r["metric"] == "total_deal_size":
            tot[("size",) + k] = v
        elif r["metric"] == "total_deal_count":
            tot[("count",) + k] = v
        elif r["metric"] == "funding_by_vertical_size":
            vsum[("size",) + k] += v
        elif r["metric"] == "funding_by_vertical_count":
            vsum[("count",) + k] += v
    bad = []
    for k, s in sorted(vsum.items()):
        t = tot.get(k)
        if t and t > 0 and s > 3 * t:
            bad.append(f"{k[1]}-{k[2]} {k[0]} ({k[3]}): vertical Σ={s:.6g} total={t:.6g} "
                       f"oran={s/t:.1f}×")
    res.append({"name": "Vertical Σ ≤ 3× headline total",
                "status": "FAIL" if bad else "PASS",
                "summary": "; ".join(bad) if bad else
                f"{len(vsum)} (yıl,rapor,scope) grubunun hepsi eşiğin altında"})

    # 4) deal count'lar tam sayı
    frac = [f'{r["report_id"]}/{r["data_year"]}/{r["dim_value_canon"] or "total"}={r["value"]}'
            for r in facts if r["unit"] == "count" and num(r["value"]) is not None
            and num(r["value"]) != int(num(r["value"]))]
    res.append({"name": "Deal count'lar tam sayı",
                "status": "FAIL" if frac else "PASS",
                "summary": "; ".join(frac[:5]) if frac else
                f'{sum(1 for r in facts if r["unit"]=="count")} count satırının hepsi tam sayı'})

    # 5) aynı data_year'ın vintage'ları arası %30'u aşan sapma
    by = defaultdict(dict)
    for r in facts:
        v = num(r["value"])
        if v is None:
            continue
        by[(r["data_year"], r["period"], r["metric"], r["dim_value_canon"],
            r["scope"])][r["report_id"]] = v
    spread = []
    for k, vints in by.items():
        if len(vints) < 2:
            continue
        lo, hi = min(vints.values()), max(vints.values())
        if lo > 0 and (hi - lo) / lo > 0.30:
            spread.append((100 * (hi - lo) / lo, k, sorted(vints.items())))
    spread.sort(reverse=True)
    res.append({"name": "Vintage sapması ≤ %30",
                "status": "FLAG" if spread else "PASS",
                "summary": f"{len(spread)} ölçüm %30'u aşıyor"
                if spread else "hiçbiri eşiği aşmıyor",
                "detail": spread})
    return res


def half_step(v, unit):
    """Basılı etiketin yuvarlama yarı-adımı.

    Grafikte yazan `$20M` gerçek değerin [19.5M, 20.5M] aralığında olduğunu
    söyler; facts.csv basılı etiketi taşıdığı için bu belirsizlik veriye
    dahildir. Deal count'lar tam sayı basılır, belirsizlik yok.
    """
    if unit == "count":
        return 0.0
    a = abs(v)
    if a >= 1e9:
        return 0.5e8            # $X.XB  -> son basamak 0.1B
    if a >= 1e6:
        return 0.5e6 if a % 1e6 < 1 else 0.5e5   # $XM ya da $X.XM
    if a >= 1e3:
        return 0.5e3
    return 0.5


def check_printed_yoy(facts):
    """2024.pdf p4/p5'te YoY % DEĞİŞİM etiketleri basılı.

    Bu, değerlerin kendisinden BAĞIMSIZ bir yayıncı beyanı — güçlü bir
    çapraz kontrol. Ama yayıncı yüzdeyi YUVARLANMAMIŞ iç veriden hesaplıyor,
    facts.csv ise grafikte YAZAN (yuvarlanmış) etiketi taşıyor. Bu yüzden
    nokta karşılaştırması yanlış olur: iki etiketin yuvarlama aralığından
    doğan YoY ARALIĞI hesaplanır ve basılı yüzde bu aralıkta mı diye bakılır.
    """
    hits, bad = 0, []
    for src, page, scope in (("2024.pdf", 4, "all"), ("2024.pdf", 5, "ex_getir_bigg")):
        doc = fitz.open(os.path.join(ROOT, "raw", src))
        p = doc[page - 1]
        words = [w for w in p.get_text("words") if w[4].strip()]
        ticks = sorted([w for w in words if re.fullmatch(r"(19|20)\d{2}", w[4])],
                       key=lambda w: w[0])
        if not ticks:
            doc.close()
            continue
        cx = [( t[0] + t[2]) / 2 for t in ticks]
        yrs = [t[4] for t in ticks]
        axis_y = ticks[0][1]
        pct = [w for w in words if re.fullmatch(r"[+-]\d+%", w[4]) and w[1] > axis_y]
        # basılı yüzdeyi yıla x ile bağla; üstteki blok size, alttaki count
        ys = sorted({round(w[1]) for w in pct})
        if not ys:
            doc.close()
            continue
        mid = (min(ys) + max(ys)) / 2
        for w in pct:
            c = (w[0] + w[2]) / 2
            j = min(range(len(cx)), key=lambda i: abs(cx[i] - c))
            if abs(cx[j] - c) > 60:
                continue
            metric = "total_deal_size" if w[1] < mid else "total_deal_count"
            printed = int(w[4].rstrip("%"))
            cur = find(facts, yrs[j], src, metric, scope)
            prv = find(facts, str(int(yrs[j]) - 1), src, metric, scope)
            if cur is None or prv is None or prv == 0:
                continue
            unit = "count" if metric.endswith("count") else "usd"
            hc, hp = half_step(cur, unit), half_step(prv, unit)
            lo = 100 * ((cur - hc) - (prv + hp)) / (prv + hp)
            hi = 100 * ((cur + hc) - (prv - hp)) / (prv - hp)
            hits += 1
            # basılı yüzde tam sayıya yuvarlı: ±0.6 puan pay
            if not (lo - 0.6 <= printed <= hi + 0.6):
                bad.append(f"{src} p{page} {metric} {yrs[j]}: basılı {printed}% "
                           f"mümkün aralık {lo:.1f}%..{hi:.1f}%")
        doc.close()
    return {"name": "Basılı YoY % ∈ yuvarlamadan doğan aralık",
            "status": "FAIL" if bad else ("PASS" if hits else "N/A"),
            "summary": "; ".join(bad[:6]) if bad else
            f"{hits} basılı yüzdenin hepsi, etiket yuvarlamasının izin verdiği "
            f"aralığın içinde"}


def find(facts, year, src, metric, scope):
    for r in facts:
        if (r["data_year"] == year and r["source_file"] == src
                and r["metric"] == metric and r["scope"] == scope
                and r["period"] == "FY"):
            return float(r["value"])
    return None


def write_md(tally, out, checks, unresolved, total):
    mism = [o for o in out if o["durum"] == "MISMATCH"]
    unre = [o for o in out if o["durum"] == "UNREADABLE"]
    cov = 100.0 * tally["OK"] / total if total else 0
    L = ["# VERIFY", "",
         "`facts.csv`'nin kaynak PDF'e karşı **bağımsız** doğrulaması.", "",
         "**Yöntem:** çıkarım kodu (`extract_facts.py`, `extract_verticals.py`) ve",
         "`extracted/*.json` bu doğrulamaya HİÇ girmez — aynı parser aynı hatayı",
         "iki kez yapardı. İkinci yol PDF'in metin katmanına da bakmaz: sayfa",
         "piksel olarak render edilir, sayılar görsel olarak okunur",
         "(`verify/readings.json`), sonra `facts.csv` ile karşılaştırılır.", "",
         "## Sonuç", "",
         f"| durum | satır |", "|---|---|",
         f"| OK | **{tally['OK']}** |",
         f"| MISMATCH | **{tally['MISMATCH']}** |",
         f"| UNREADABLE | **{tally['UNREADABLE']}** |",
         f"| toplam | {total} |", "",
         f"Görsel doğrulama kapsamı: **%{cov:.1f}**", "",
         "Satır bazında tam döküm: `verify_report.csv`", ""]
    if mism:
        L += ["## MISMATCH", "",
              "| data_year | report_id | metrik | sektör | scope | facts | görsel | not |",
              "|---|---|---|---|---|---|---|---|"]
        for o in mism[:60]:
            L.append("| {data_year} | {report_id} | {metric} | {dim_value_canon} | "
                     "{scope} | {facts_value} | {verify_value} | {not} |".format(**o))
        L.append("")
    if unre:
        L += [f"## UNREADABLE ({len(unre)})", "",
              "Görsel okuma kaydı olmayan ya da etiketi okunamayan satırlar.", ""]
        seen = defaultdict(int)
        for o in unre:
            seen[(o["report_id"], o["metric"])] += 1
        for k, n in sorted(seen.items()):
            L.append(f"- {k[0]} · {k[1]}: {n} satır")
        L.append("")
    if unresolved:
        L += ["## Eşlenemeyen ham etiketler", ""]
        for pk, raw in unresolved:
            L.append(f"- `{pk}` → `{raw}` (dim_verticals.csv'de yok)")
        L.append("")

    L += ["## İç tutarlılık kontrolleri", "",
          "| kontrol | durum | özet |", "|---|---|---|"]
    for c in checks:
        L.append(f"| {c['name']} | **{c['status']}** | {c['summary']} |")
    L.append("")
    sp = next((c for c in checks if c.get("detail")), None)
    if sp and sp["detail"]:
        L += ["### Vintage sapması %30 üzeri", "",
              "Bunlar hata değil, yayıncının revizyonu — `KNOWN_ISSUES.md` KI-005.", "",
              "| ölçüm | vintage'lar | sapma |", "|---|---|---|"]
        for pct, k, vints in sp["detail"][:25]:
            vs = ", ".join(f"{r}={v:.6g}" for r, v in vints)
            L.append(f"| {k[3] or 'total'} {k[0]}-{k[1]} {k[2]} | {vs} | %{pct:.0f} |")
        L.append("")
    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["render", "compare", "checks"])
    a = ap.parse_args()
    os.makedirs(VDIR, exist_ok=True)
    if a.cmd == "render":
        do_render()
        return 0
    if a.cmd == "checks":
        for c in run_checks(load_facts()):
            print(f"  [{c['status']}] {c['name']}: {c['summary']}")
        return 0
    return do_compare()


if __name__ == "__main__":
    sys.exit(main())
