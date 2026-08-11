#!/usr/bin/env python3
"""QA — facts.csv ve deals.csv doğrulaması.

CLAUDE.md "QA kuralları" bölümünün uygulaması. Veri üretmez, sadece denetler.

Kullanım:
    .venv/bin/python scripts/qa.py
    .venv/bin/python scripts/qa.py --facts facts.csv --deals deals.csv

Çıkış kodu: 0 = temiz (uyarı olabilir), 1 = en az bir HATA.
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict

PERIODS = {"FY", "Q1", "Q2", "Q3", "Q4", "H1"}
SCOPES = {"all", "ex_bigg", "ex_getir_bigg", "diaspora"}
CONFIDENCE = {"high", "medium", "low"}
AMOUNT_STATUS = {"exact", "est", ""}

FACTS_COLS = ["data_year", "period", "report_id", "report_year", "metric",
              "dim_type", "dim_value_raw", "dim_value_canon", "scope", "unit",
              "value", "source_file", "page", "confidence", "is_provisional"]
BOOL = {"TRUE", "FALSE"}
DEALS_COLS = ["deal_id", "report_id", "period", "data_year", "startup",
              "round_type", "amount_usd", "amount_status", "verticals_raw",
              "verticals_canon", "investors", "investor_types", "city",
              "confidence"]

# deals.csv'de olmaması gereken agregat satırı işaretleri
AGGREGATE_MARKERS = re.compile(
    r"^(total|toplam|sum|subtotal|ara toplam|other|others|diğer|diger|"
    r"undisclosed total|all|genel toplam|n=\d+)$", re.I)
# facts.csv satırı deal-level kaynaktan türetilmiş mi?
DEAL_SOURCE = re.compile(r"deals\.csv|deal[-_ ]?level|derived", re.I)

# Toplam deal count metriğinin adı (kısmi-kapsam kontrolü için)
DEAL_COUNT_METRICS = {"total deal count", "deal count", "# deals", "# rounds"}


class Report:
    def __init__(self):
        self.errors, self.warns = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warns.append(f"{where}: {msg}")


def load(path):
    if not os.path.exists(path):
        return None
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(s):
    """'1.234,5' / '1,234.5' / '$12M' gibi değil — ham sayı bekleriz."""
    s = (s or "").strip().replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


# --------------------------------------------------------------- facts.csv

def check_facts(rows, r):
    if rows is None:
        r.warn("facts.csv", "dosya yok — atlandı")
        return
    if not rows:
        r.warn("facts.csv", "boş")
        return

    missing = [c for c in FACTS_COLS if c not in rows[0]]
    if missing:
        r.err("facts.csv", f"eksik kolon: {missing}")
        return
    # deals.csv şeması facts.csv'ye sızmış mı?
    leaked = [c for c in ("deal_id", "startup", "investors", "round_type")
              if c in rows[0]]
    if leaked:
        r.err("facts.csv", f"deal-level kolon sızmış: {leaked} — deals.csv ayrı tablo")

    seen = {}
    for i, row in enumerate(rows, 2):  # 2 = başlık sonrası ilk satır
        at = f"facts.csv:{i}"
        p = (row["period"] or "").strip()
        if p not in PERIODS:
            r.err(at, f"period '{p}' geçersiz (izinli: {sorted(PERIODS)})")
        if (row["scope"] or "").strip() not in SCOPES:
            r.err(at, f"scope '{row['scope']}' geçersiz")
        if (row["confidence"] or "").strip() not in CONFIDENCE:
            r.err(at, f"confidence '{row['confidence']}' geçersiz")
        if (row["is_provisional"] or "").strip() not in BOOL:
            r.err(at, f"is_provisional '{row['is_provisional']}' geçersiz")

        # deal count'lar integer olmalı
        v = num(row["value"])
        unit = (row["unit"] or "").strip().lower()
        if unit in ("count", "deals", "#") and v is not None and v != int(v):
            r.err(at, f"deal count integer değil: {row['value']}")

        # provenans: her agregat satırı bir rapor sayfasına dayanmalı
        if DEAL_SOURCE.search(row["source_file"] or ""):
            r.err(at, "source_file deal-level kaynağa işaret ediyor — "
                      "toplamlar yalnız raporun kendi agregatından gelir")
        if not (row["source_file"] or "").strip():
            r.err(at, "source_file boş")
        if not (row["page"] or "").strip():
            r.warn(at, "page boş — provenans eksik")

        key = (row["data_year"], p, row["report_id"], row["metric"],
               row["dim_value_canon"], row["scope"])
        if key in seen:
            r.err(at, f"unique ihlali, {seen[key]}. satırla aynı anahtar: {key}")
        else:
            seen[key] = i

    check_stage_sums(rows, r)
    check_vintage_spread(rows, r)
    check_vintage_collision(rows, r)


def check_vintage_collision(rows, r):
    """report_id ↔ source_file 1:1 olmalı (KI-004 çözümünün bütünlüğü)."""
    by = defaultdict(set)
    for row in rows:
        by[row["report_id"]].add(row["source_file"])
    for rid, files in sorted(by.items()):
        if len(files) > 1:
            r.err("facts.csv",
                  f"report_id={rid} birden çok kaynak dosyaya bağlı: "
                  f"{sorted(files)} — vintage kimliği bozuk")


def check_stage_sums(rows, r):
    """Stage kırılımı toplamı aynı anahtardaki total'ı geçemez."""
    totals, stages = {}, defaultdict(float)
    for row in rows:
        v = num(row["value"])
        if v is None:
            continue
        key = (row["data_year"], row["period"], row["report_year"],
               row["scope"], (row["unit"] or "").strip().lower())
        if (row["dim_type"] or "").strip() in ("", "none"):
            m = (row["metric"] or "").strip().lower()
            if "total" in m or m in DEAL_COUNT_METRICS:
                totals[key] = max(totals.get(key, 0.0), v)
        elif (row["dim_type"] or "").strip() == "stage":
            stages[key] += v
    for key, s in stages.items():
        t = totals.get(key)
        # %1 tolerans: yuvarlama payı
        if t is not None and s > t * 1.01:
            r.err("facts.csv", f"stage toplamı total'ı aşıyor {key}: {s} > {t}")


def check_vintage_spread(rows, r):
    """Aynı data_year'ın farklı vintage'ları %20'den fazla ayrışırsa flag."""
    by = defaultdict(dict)
    for row in rows:
        v = num(row["value"])
        if v is None:
            continue
        key = (row["data_year"], row["period"], row["metric"],
               row["dim_value_canon"], row["scope"])
        by[key][row["report_year"]] = v
    for key, vints in by.items():
        if len(vints) < 2:
            continue
        lo, hi = min(vints.values()), max(vints.values())
        if lo > 0 and (hi - lo) / lo > 0.20:
            r.warn("facts.csv",
                   f"vintage sapması >%20 {key}: {sorted(vints.items())}")


# --------------------------------------------------------------- deals.csv

def check_deals(rows, r):
    if rows is None:
        r.warn("deals.csv", "dosya yok — atlandı")
        return
    if not rows:
        r.warn("deals.csv", "boş")
        return

    missing = [c for c in DEALS_COLS if c not in rows[0]]
    if missing:
        r.err("deals.csv", f"eksik kolon: {missing}")
        return

    ids = {}
    for i, row in enumerate(rows, 2):
        at = f"deals.csv:{i}"
        p = (row["period"] or "").strip()
        if p not in PERIODS:
            r.err(at, f"period '{p}' geçersiz (izinli: {sorted(PERIODS)})")
        if (row["confidence"] or "").strip() not in CONFIDENCE:
            r.err(at, f"confidence '{row['confidence']}' geçersiz")
        if (row["amount_status"] or "").strip() not in AMOUNT_STATUS:
            r.err(at, f"amount_status '{row['amount_status']}' geçersiz")

        did = (row["deal_id"] or "").strip()
        if not did:
            r.err(at, "deal_id boş")
        elif did in ids:
            r.err(at, f"deal_id tekrar ediyor ({ids[did]}. satır): {did}")
        else:
            ids[did] = i

        startup = (row["startup"] or "").strip()
        if not startup:
            r.err(at, "startup boş — deal-level satır startup'sız olamaz")
        elif AGGREGATE_MARKERS.match(startup):
            r.err(at, f"agregat satırı: startup='{startup}' — "
                      "deals.csv yalnız tekil deal taşır")

        # tutar yoksa amount_status da boş olmalı (yok ≠ sıfır)
        amt = (row["amount_usd"] or "").strip()
        if amt and num(amt) is None:
            r.err(at, f"amount_usd sayı değil: {amt}")
        if amt and num(amt) == 0:
            r.err(at, "amount_usd 0 — açıklanmayan tutar BOŞ bırakılır")
        if not amt and (row["amount_status"] or "").strip():
            r.err(at, "amount_usd boşken amount_status dolu")


def check_partial_coverage(facts, deals, r):
    """KRİTİK: deals.csv kısmi kapsamlı olmalı.

    Aynı (data_year, period) için deals.csv'deki satır sayısı facts.csv'deki
    toplam deal count'a eşit ya da ondan büyükse, deals.csv tam kapsamlı
    sanılıyor demektir — agregat türetme riski. HATA ver.
    """
    if not facts or not deals:
        return
    totals = {}
    for row in facts:
        if (row.get("dim_type") or "").strip() not in ("", "none"):
            continue
        if (row.get("metric") or "").strip().lower() not in DEAL_COUNT_METRICS:
            continue
        if (row.get("scope") or "").strip() != "all":
            continue
        v = num(row.get("value"))
        if v is None:
            continue
        key = (row["data_year"], row["period"])
        # en güncel vintage'ı al
        prev = totals.get(key)
        if prev is None or row["report_year"] >= prev[0]:
            totals[key] = (row["report_year"], v)

    counted = defaultdict(int)
    for row in deals:
        counted[(row["data_year"], row["period"])] += 1

    for key, n in sorted(counted.items()):
        ref = totals.get(key)
        if ref is None:
            # FY toplamıyla da kıyasla: çeyreklik satırlar yılın altında kalmalı
            ref = totals.get((key[0], "FY"))
            if ref is None:
                r.warn("deals.csv",
                       f"{key} için facts.csv'de karşılaştırılacak toplam yok")
                continue
        if n >= ref[1]:
            r.err("deals.csv",
                  f"{key}: {n} deal satırı, facts.csv toplamı {ref[1]:.0f} "
                  f"(vintage {ref[0]}). deals.csv KISMİ olmalı — bu değer "
                  "tam kapsam yanılsaması yaratır, agregat türetilemez")
        else:
            pct = 100.0 * n / ref[1] if ref[1] else 0
            r.warn("deals.csv",
                   f"{key}: kapsam %{pct:.0f} ({n}/{ref[1]:.0f}) — "
                   "agregat türetme YASAK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", default="facts.csv")
    ap.add_argument("--deals", default="deals.csv")
    a = ap.parse_args()

    r = Report()
    facts, deals = load(a.facts), load(a.deals)
    check_facts(facts, r)
    check_deals(deals, r)
    check_partial_coverage(facts, deals, r)

    for w in r.warns:
        print(f"UYARI  {w}")
    for e in r.errors:
        print(f"HATA   {e}")
    print(f"\n{len(r.errors)} hata, {len(r.warns)} uyarı")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
