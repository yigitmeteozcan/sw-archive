#!/usr/bin/env python3
"""coverage.tsv (append-only, tek gerçek kaynak) -> COVERAGE.md matrisi.

Her rapor işlendikçe coverage.tsv'ye satır eklenir ve bu script çalıştırılır.
COVERAGE.md elle düzenlenmez; buradan üretilir.

coverage.tsv kolonları (tab-separated, başlık satırı zorunlu):
  report_year  source_file  metric_canon  metric_raw  dim_type  period
  data_years  scope  pages  note
"""
import csv
import sys
from collections import OrderedDict, defaultdict

TSV = "coverage.tsv"
OUT = "COVERAGE.md"

# Rapor kolonlarının sırası (dosya adı = rapor). 2026 çeyreklik.
REPORT_ORDER = ["2015", "2016", "2017", "2018", "2019", "2020", "2021",
                "2022", "2023", "2024", "2025", "2026q1", "2026q2"]


def cell_text(rows):
    """Bir (metric,dim) x rapor hücresi: data_years + period/scope işareti."""
    outs = []
    for r in rows:
        s = r["data_years"]
        tags = []
        if r["period"] and r["period"] != "FY":
            tags.append(r["period"])
        if r["scope"] and r["scope"] != "all":
            tags.append(r["scope"])
        if tags:
            s += f" [{'/'.join(tags)}]"
        outs.append(s)
    # aynı hücrede birden fazla kayıt varsa ; ile ayır
    seen, uniq = set(), []
    for s in outs:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return "; ".join(uniq)


def main():
    with open(TSV, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    # satır anahtarı: metric_canon + dim_type
    row_keys = OrderedDict()
    grid = defaultdict(list)  # (rowkey, report_year) -> [rows]
    for r in rows:
        dim = r["dim_type"].strip()
        label = r["metric_canon"] if dim in ("", "none") else f"{r['metric_canon']} × {dim}"
        row_keys.setdefault(label, None)
        grid[(label, r["report_year"])].append(r)

    reports = [ry for ry in REPORT_ORDER if any(r["report_year"] == ry for r in rows)]

    lines = []
    lines.append("# COVERAGE")
    lines.append("")
    lines.append("Hangi rapor, hangi metriği, hangi data_year'lar için içeriyor. "
                 "SAYI YOK — sadece kapsam.")
    lines.append("Kaynak: sayfa/tablo/grafik başlıkları + eksen yıl etiketleri. "
                 "Üretim: `scripts/render_coverage.py` (elle düzenleme).")
    lines.append("")
    lines.append("Hücre = o raporun o metrik için kapsadığı data_year aralığı. "
                 "`[Q1]`/`[H1]` period, `[ex_bigg]` gibi etiketler scope. "
                 "Boş = o raporda o metrik yok (0 DEĞİL).")
    lines.append("")

    header = "| metric × dim | " + " | ".join(reports) + " |"
    sep = "|" + "---|" * (len(reports) + 1)
    lines.append(header)
    lines.append(sep)
    for label in row_keys:
        cells = []
        for ry in reports:
            cells.append(cell_text(grid.get((label, ry), [])) or "")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.append("")

    # Provenans: rapor bazında sayfa detayları
    lines.append("## Provenans (rapor × metrik × sayfa)")
    lines.append("")
    lines.append("| rapor | metric_raw | dim | period | data_years | scope | sayfa | not |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for ry in reports:
        for r in [x for x in rows if x["report_year"] == ry]:
            lines.append(f"| {r['source_file']} | {r['metric_raw']} | {r['dim_type']} "
                         f"| {r['period']} | {r['data_years']} | {r['scope']} "
                         f"| {r['pages']} | {r['note']} |")
    lines.append("")

    lines.append(SYNTHESIS)

    with open(OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT}: {len(row_keys)} metric-rows, {len(reports)} reports, {len(rows)} records")


SYNTHESIS = r"""
## Sentez (13 rapor tarandıktan sonra)

### 1) Hangi metrik için kaç rapor dikmek gerek (en uzun + en güncel vintage seri)

**Kolay — 1-2 rapor yeter (her yıllık rapor tüm geçmişi yeniden yayınlıyor):**
- **Total investment amount / Total deal count** — 2024 raporu tek başına 2010-2024
  verir; 2025 raporu 2025'i ekler (2015-2025). FY 2010-2025 = **2 rapor (2024 + 2025)**.
  + 2026 için 2026q1/q2 (Q1/H1, ayrı period). İstisna: 2018 raporunda amount serisi YOK
  (sadece deal count) ve 2021/2022 vintage'ı 2017'den başlar → 2010-2016'yı onlardan çekme.
- **Investment by stage** — 2020 raporu 2010-2020, 2025 raporu 2020-2025.
  = **2 rapor (2020 + 2025)**; ama S3 (taksonomi) + S4 (amount vs count) dikişleri var.
- **CVC / corporate** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**.
- **Acquisitions & secondary** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**
  (2024 raporu sadece narrative, by-year chart yok → S10).
- **Gender diversity** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**; 2021 boşluğu.
- **VC fundraising** — 2020 (2012-2020) + 2025 (2020-2025) = **2 rapor**; veri 2012'de başlar.
- **Turkey vs abroad (diaspora)** — 2019 (2010-2019) + 2025 (2015-2025) = **2 rapor**;
  ama 2020-2024 arası çağdaş vintage YOK (S8).

### 2) Dikişler tam olarak nerede (vintage/tanım değişimi)

- **S1 — Ufuk daralması (EN KRİTİK):** 2021 ve 2022 raporları TÜM serileri 2017-başlangıca
  kırpar (5-6 yıl). 2010-2016 yıllarını 2021/2022'den ÇEKME — onlarda yok. Çağdaş kaynak
  2019/2020 raporları, revize kaynak 2023/2024 raporları.
- **S2 — Ufuk geri gelişi ama kısmi:** 2023 headline'ı 2010-2023'e geri açar, 2024 → 2010-2024;
  ama 2025 raporu tekrar 2015-2025'e kırpar (2010-2014 düşer). 2010-2014 için en güncel
  vintage = 2024 raporu.
- **S3 — Stage taksonomisi (2018→2019):** ≤2018 Pre-Seed/Seed/Series A-D; 2019+ Seed/Early VC/
  Later VC. Dikiş için eşleme şart.
- **S4 — Stage ölçü tabanı:** kimi rapor stage'i $ ile (2016,2017,2019,2021,2022,2025), kimi #
  ile (2018,2020) verir. unit'i karıştırma.
- **S5 — 2018 sadece deal count:** total amount-by-year yok.
- **S6 — BiGG dahil edilmesi (2023→2024):** 2024+ TÜBİTAK BiGG pre-seed'i ana veriye katar,
  deal count'u şişirir (2024: 469). Temiz karşılaştırma için scope=ex_getir_bigg (2024 p5).
- **S7 — Açık revizyon:** 2023 raporu Dream Games'in 2022 dealını 2021'e taşıdı → aynı
  data_year farklı vintage'ta farklı değer (CLAUDE.md kısıt #1'in kanıtı).
- **S8 — Diaspora aç/kapa:** seri 2017 & 2019'da var; 2020'de sadece snapshot; 2021-2024 YOK;
  2025'te 2015-2025 olarak geri geldi.
- **S10 — Acquisitions 2024 boşluğu:** 2024 raporu M&A'yı sadece anlatı olarak verir (chart yok);
  2024 by-year değeri için 2025 raporunu (2020-2025) kullan.
- **S11 — 2026 karma period:** 2026q1/q2 raporlarında geçmiş FY barları (2016-2025) ile 2026
  Q1/H1 noktası bir arada. 2026q2 = H1 (Q2 değil). 2026 kısmi değerini FY serisine katma.

### 3) Hiçbir raporda 10 yıllık seri kurulamayacak metrikler

- **Investment by vertical** — 2018 öncesi sadece tek-yıl snapshot (2016,2017,2018,2019);
  gerçek çok-yıl seri ancak 2018'den (2023/2024/2025 raporları). Üstelik tag'ler mutually
  exclusive değil ve isimleri yıllara göre değişiyor → 10 yıllık karşılaştırılabilir seri YOK.
- **Foreign investor participation** — sadece 2017'den itibaren (en fazla 2017-2025 ≈ 9 yıl).
- **Round size distribution** — zaman serisi yalnız 2020 (2010-2020) ve 2021 (2017-2021);
  2022'den sonra tamamen düştü → bugüne uzanmaz (max 2010-2021).
- **Median round size & Median pre-money valuation** — yalnız 2016 raporu (2012-2016);
  tek-rapor metriği, seri kurulamaz. (2021'deki "valuations" farklı, spot yıllar 2017/2019/2021.)
- **Maturity stage (GE/PE)** — yalnız 2021 & 2022 (2017-2022); sonra düştü.
- **Gaming/Fintech sektör derin-dalış** — dağınık (gaming 2021-2023, fintech yalnız 2022).
- **VCIF/GSYF participation** — 2022-2024 (2017-2024); en fazla 8 yıl, 2017'den önce yok.
- **Tek-rapor / geç-başlayan metrikler (seri yok):** Investment by city (2020-2022),
  university (2020), legal structure (2020), Turkish investors' foreign investment (2019),
  exits (2020), startups founded by vertical (2020,2022), most active investors (2021),
  valuations (2021), grants (dağınık 2018-2021), VC/startup survey (2023-2025),
  angel investors/networks (yalnız 2026q2), funding concentration (dağınık).

### Pratik dikiş reçetesi (10+ yıl hedefleyen metrikler için)
Headline & CVC & acquisitions & gender & stage: **2020 raporu (2010-2020) + 2025 raporu
(2020-2025)** ana omurga; 2026'yı yalnız Q1/H1 period'la ekle. 2010-2014'te en güncel
vintage 2024 raporu. Diaspora için 2019 + 2025. Fundraising 2012'den başlar.
"""


if __name__ == "__main__":
    main()
