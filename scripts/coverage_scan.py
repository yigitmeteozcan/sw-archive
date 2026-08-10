#!/usr/bin/env python3
"""Coverage scanner — ONE report at a time (Altın kural).

Amaç: sayı çıkarmak DEĞİL, kapsam çıkarmak. Her sayfanın metnini (başlıklar,
tablo/grafik başlıkları, eksen etiketleri) ve o sayfada geçen yıl token'larını
listeler. Model bu çıktıya bakıp COVERAGE.md'yi doldurur.

Kullanım:
    .venv/bin/python scripts/coverage_scan.py raw/2015.pdf
    .venv/bin/python scripts/coverage_scan.py raw/2015.pdf --full   # tüm metin
"""
import re
import sys

import fitz  # PyMuPDF

YEAR_RE = re.compile(r"\b(20[0-2]\d)\b")
YEAR_MIN, YEAR_MAX = 2008, 2027


def years_on_page(text):
    ys = sorted({int(y) for y in YEAR_RE.findall(text) if YEAR_MIN <= int(y) <= YEAR_MAX})
    return ys


def compact_range(ys):
    """Yıl listesini kompakt aralık string'ine çevir: 2015,2016,2017,2019 -> 2015-2017,2019."""
    if not ys:
        return ""
    parts, start, prev = [], ys[0], ys[0]
    for y in ys[1:]:
        if y == prev + 1:
            prev = y
            continue
        parts.append(f"{start}-{prev}" if start != prev else f"{start}")
        start = prev = y
    parts.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ",".join(parts)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: coverage_scan.py <pdf> [--full]")
    path = sys.argv[1]
    full = "--full" in sys.argv
    doc = fitz.open(path)
    print(f"# {path}  ({doc.page_count} pages)\n")
    for i, page in enumerate(doc, 1):
        text = page.get_text("text")
        ys = years_on_page(text)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        # Başlık adayları: kısa, yıl olmayan, uzunca satırlar genelde başlık/etiket.
        titles = [ln for ln in lines if not re.fullmatch(r"[\d\s.,%$€₺+\-–—]+", ln)]
        print(f"--- page {i} | years: {compact_range(ys)} ---")
        if full:
            for ln in lines:
                print(f"    {ln}")
        else:
            # kompakt: ilk ~12 metin-ağırlıklı satır (başlıklar/etiketler)
            for ln in titles[:12]:
                print(f"    {ln}")
        print()


if __name__ == "__main__":
    main()
