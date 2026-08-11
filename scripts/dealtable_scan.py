#!/usr/bin/env python3
"""Deal-level tablo dedektörü — ONE report at a time (Altın kural).

Amaç: SAYI ÇIKARMAK DEĞİL. Sadece "bu raporda deal-level (satır = tek yatırım
turu) bir tablo var mı, hangi sayfada, hangi kolonlarla, kaç satır" tespiti.

Yöntem (başlık ismine GÜVENMEZ — tablo geometrisine bakar):
  1. Kelimeleri koordinatlarıyla al, y'ye göre satırlara kümele.
  2. Satır içinde büyük x boşluklarından hücrelere böl.
  3. Hücre başlangıç x'lerini sayfa genelinde histogramla → kolon çapaları.
  4. >=MIN_COLS çapaya değen >=MIN_ROWS satır varsa: tablo.
  5. Başlık satırı = tabloya ait, deal-kolon anahtar kelimelerini taşıyan satır.

Örnek sabitler 2015q4.pdf p6 ("ROUNDS & DETAILS") üzerinde kalibre edildi.

Kullanım:
    .venv/bin/python scripts/dealtable_scan.py raw/2015q4.pdf
    .venv/bin/python scripts/dealtable_scan.py raw/2015q4.pdf --json out.json
"""
import json
import re
import sys
from collections import defaultdict

import fitz  # PyMuPDF

MIN_COLS = 4        # deal tablosu en az 4 kolon (startup/round/amount/...)
MIN_ROWS = 5        # en az 5 veri satırı
COL_GAP_PCT = 0.022  # sayfa genişliğinin %2.2'sinden büyük boşluk = kolon sınırı
ROW_TOL_PCT = 0.004  # sayfa yüksekliğinin %0.4'ü içindeki kelimeler aynı satır
BIN_PCT = 0.012      # kolon çapası histogram kutusu

# Deal-level tablo başlığında beklenen kolon adları
HEADER_KEYS = {
    "startup", "startups", "company", "girisim", "girişim",
    "funding", "round", "rounds", "type", "stage", "series",
    "amount", "size", "investment", "deal",
    "vertical", "verticals", "sector", "sectors", "tag", "tags", "industry",
    "investor", "investors", "investment by", "buyer", "acquirer",
    "city", "location", "hq", "country", "date", "month", "valuation",
}
# Bunlar varsa satır bir "deal" satırı gibi kokuyor (round type sözlüğü)
ROUND_TOKENS = re.compile(
    r"\b(pre-?seed|seed|series\s?[a-f]\b|angel|convertible|bridge|"
    r"growth|pre-?a|secondary|acquisition|grant|ico|crowdfunding|"
    r"venture|debt|extension)\b", re.I)


# Kart-ızgara (card-grid) listelemeler için zayıf sinyaller. 2018-2020 raporları
# deal'leri hizalı tablo yerine kart ızgarasında veriyor; geometrik dedektör kaçırır.
AMOUNT_RE = re.compile(r"\$\s?\d[\d.,]*\s?[KMB]?\b|\b\d{1,3}[.,]\d{3}[.,]\d{3}\b")
# startups.watch yatırımcı tipi eki — KAPALI liste. Parantez içindeki her token
# tip kodu DEĞİL: (IFC) (SBS) (GBA) (MBCO) şirket kısaltmasıdır, isme aittir.
INV_SUFFIX_RE = re.compile(r"\((VC|P|BAN|AF|CVC|PE|FI|GE|CR|Angel)\)")
DATE_RE = re.compile(r"\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}\b", re.I)


# Kart ızgarasında her deal'in bir "değer" hücresi var: tutar, N/A ya da tire.
VALUE_RE = re.compile(r"^(\$?\s?\d[\d.,]*\s?[KMB]?\*?|N/A|-|–)\b", re.I)
# Raporun kendi beyanı: "$19.6M across 27 deals" / "in 34 rounds"
SELF_COUNT_RE = re.compile(
    r"across\s+(\d+)\s+(?:deals?|rounds?|investments?)|"
    r"in\s+(\d+)\s+(?:deals?|rounds?)\b", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


YEAR_RE = re.compile(r"\b20[0-2]\d\b")
# Kart-ızgara sayfasının başlığı deal listelemesine işaret ediyor mu?
LIST_TITLE_RE = re.compile(
    r"rounds?\b|deals?\b|investments?\b|fundings?\b|acquisitions?\b|exits?\b",
    re.I)


def weak_signals(page):
    """Hizalı tablo olmasa da deal-level listeleme var mı? Sayı ÇIKARMAZ, sayar."""
    text = page.get_text("text")
    return {
        "round_tok": len(ROUND_TOKENS.findall(text)),
        "amount_tok": len(AMOUNT_RE.findall(text)),
        "inv_suffix": len(INV_SUFFIX_RE.findall(text)),
        "date_tok": len(DATE_RE.findall(text)),
        # >=6 farklı yıl = grafik ekseni, deal listesi değil
        "years": len(set(YEAR_RE.findall(text))),
    }


def rows_of(page, w, h):
    """Kelimeleri y'ye göre satırlara kümele."""
    tol = h * ROW_TOL_PCT
    words = [x for x in page.get_text("words") if x[4].strip()]
    words.sort(key=lambda t: (t[1], t[0]))
    rows, cur, cur_y = [], [], None
    for x0, y0, x1, y1, txt, *_ in words:
        if cur_y is None or abs(y0 - cur_y) <= tol:
            cur.append((x0, x1, txt))
            cur_y = y0 if cur_y is None else cur_y
        else:
            rows.append((cur_y, sorted(cur)))
            cur, cur_y = [(x0, x1, txt)], y0
    if cur:
        rows.append((cur_y, sorted(cur)))
    return rows


def cells_of(row_words, w):
    """Satırı büyük x boşluklarından hücrelere böl. -> [(x_left, x_center, text)]"""
    gap = w * COL_GAP_PCT
    out, cur, prev_end = [], [], None

    def flush(c):
        return (c[0][0], (c[0][0] + c[-1][1]) / 2, " ".join(t for _, _, t in c))

    for x0, x1, txt in row_words:
        if prev_end is not None and x0 - prev_end > gap:
            out.append(flush(cur))
            cur = []
        cur.append((x0, x1, txt))
        prev_end = x1
    if cur:
        out.append(flush(cur))
    return out


def analyze(table, w, h, mode):
    """Tek hizalama modunda (sol-hizalı / ortalanmış) tablo çıkar. -> dict | None

    mode='left'   : kolonlar sol kenardan hizalı (2015q4, 2016q3)
    mode='center' : kolonlar ortalanmış (2015q1) — sol kenar çapası tutmaz
    """
    xi = 0 if mode == "left" else 1
    binw = w * BIN_PCT
    # NOT: tek hücreli satırlar da sayılır — bazı raporlarda (2016q2) startup adı
    # kendi satırında tek başına durur; dışlanırsa en sol kolon çapası kaybolur.
    hist = defaultdict(set)
    for i, (_, cells, _rw) in enumerate(table):
        for c in cells:
            hist[int(c[xi] / binw)].add(i)
    anchors = sorted(b for b, ri in hist.items() if len(ri) >= MIN_ROWS)
    # bitişik kutuları tek çapaya indir
    merged = []
    for b in anchors:
        if merged and b - merged[-1][-1] <= 1:
            merged[-1].append(b)
        else:
            merged.append([b])
    anchor_bins = [set(g) for g in merged]
    if len(anchor_bins) < MIN_COLS:
        return None

    def hits(cells):
        return sum(1 for g in anchor_bins
                   if any(int(c[xi] / binw) in g for c in cells))

    # kolon sınırları: ardışık çapaların orta noktası
    centers = [sum(g) / len(g) * binw for g in anchor_bins]
    bounds = [(centers[i] + centers[i + 1]) / 2 for i in range(len(centers) - 1)]

    def by_column(cells):
        cols = [[] for _ in centers]
        for c in cells:
            idx = sum(1 for b in bounds if c[xi] >= b)
            cols[idx].append(c[2])
        return [" ".join(v).strip() for v in cols]

    # başlık: sayfadaki en yüksek skorlu, anahtar-kelime yoğun satır
    header, hdr_score, hdr_y = None, 0, None
    for y, cells, _rw in table:
        texts = by_column(cells)
        score = sum(1 for t in texts if norm(t) in HEADER_KEYS)
        if score > hdr_score and score >= 2:
            header, hdr_score, hdr_y = texts, score, y

    # KAYIT gruplama: satır=deal varsayımı tutmuyor — bazı raporlarda (2016q2)
    # startup adı ile kalan alanlar yarım satır kayık, hatta ters sırada.
    # Bu yüzden EN SOL kolonun (startup) y'leri kayıt çapası kabul edilir;
    # diğer tüm hücreler en yakın çapaya yazılır.
    col0 = anchor_bins[0]
    below = [(y, c) for y, c, _rw in table if hdr_y is None or y > hdr_y]
    seeds = sorted(y for y, cells in below
                   if any(int(c[xi] / binw) in col0 for c in cells))
    if len(seeds) < MIN_ROWS:
        return None

    def median(v):
        v = sorted(v)
        return v[len(v) // 2] if v else 0.0

    # Satır adımı (pitch): deal tabloları düzenli dikey adımla dizilir. Sarmalanmış
    # adlar küçük, tablo dışı metin (dipnot) büyük boşluk üretir; ikisini de ele.
    gaps = [b - a for a, b in zip(seeds, seeds[1:])]
    pitch = median(gaps)
    pitch = median([g for g in gaps if g >= 0.6 * pitch]) or pitch
    if pitch <= 0:
        return None
    # tablo gövdesi = adım'a uyan en uzun kesintisiz dizi (dipnot/başlık dışarıda)
    runs, cur = [], [seeds[0]]
    for a, b in zip(seeds, seeds[1:]):
        if b - a > 2.5 * pitch:
            runs.append(cur)
            cur = []
        cur.append(b)
    runs.append(cur)
    seeds = max(runs, key=len)
    # sarmalanmış startup adı (ör. "Peoplise / (Yüzyüzeyiz)") iki çapa üretir
    anchors_y = [seeds[0]]
    for y in seeds[1:]:
        if y - anchors_y[-1] >= 0.6 * pitch:
            anchors_y.append(y)
    if len(anchors_y) < MIN_ROWS:
        return None

    records = [[] for _ in anchors_y]
    for y, cells in below:
        j = min(range(len(anchors_y)), key=lambda k: abs(anchors_y[k] - y))
        if abs(anchors_y[j] - y) <= 1.2 * pitch:
            records[j].extend(cells)

    # kalite kapısı: kayıtların en az yarısı tam kolon setine değmeli
    full = [(anchors_y[j], c) for j, c in enumerate(records) if hits(c) >= MIN_COLS]
    if len(full) < MIN_ROWS or len(full) < 0.5 * len(anchors_y):
        return None

    round_hits = sum(1 for c in records
                     if any(ROUND_TOKENS.search(t) for _, _, t in c))
    sample = [re.sub(r"\d", "#", t) for t in by_column(sorted(records[0]))]
    return {
        "mode": mode,
        "n_cols": len(anchor_bins),
        "n_rows": len(anchors_y),
        "n_full_rows": len(full),
        # kayıt × kolon değerleri (harmonizasyon eşlemesi için; sayı çıkarmaz)
        "records_cols": [by_column(sorted(c)) for c in records],
        "header": header,
        "header_score": hdr_score,
        "round_token_rows": round_hits,
        "sample_masked": sample,
    }


def count_cards(page, w, h):
    """Kart-ızgara listelemesinde deal sayısını tahmin et.

    Izgarada her deal bir kart: üst bantta startup adı, alt bantta değer
    (tutar / N/A / tire). Değer bantlarındaki hücreleri sayarız.
    """
    n = 0
    for _y, rw in rows_of(page, w, h):
        cells = cells_of(rw, w)
        vals = sum(1 for c in cells if VALUE_RE.match(c[2].strip()))
        if vals >= 3:          # değer bandı: en az 3 kart yan yana
            n += len(cells)
    return n


def detect(page, w, h):
    """Sayfada deal-level tablo var mı? İki hizalama modunu dener. -> dict | None"""
    rows = rows_of(page, w, h)
    if len(rows) < MIN_ROWS:
        return None
    table = [(y, cells_of(rw, w), rw) for y, rw in rows]
    cands = [c for c in (analyze(table, w, h, m) for m in ("left", "center")) if c]
    if not cands:
        return None
    # en iyi aday: en çok kayıt yakalayan mod (hizalama modu yanlışsa kayıt
    # çapaları kaçar ve satır sayısı çöker), sonra başlık skoru, sonra kolon
    return max(cands, key=lambda d: (d["n_rows"], d["header_score"], d["n_cols"]))


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: dealtable_scan.py <pdf> [--json out.json]")
    path = sys.argv[1]
    doc = fitz.open(path)
    out = {"file": path, "pages": doc.page_count, "tables": [], "no_text_pages": 0,
           "self_reported": []}
    for i, page in enumerate(doc, 1):
        w, h = page.rect.width, page.rect.height
        if len(page.get_text("words")) < 5:
            out["no_text_pages"] += 1
            continue
        # sayfa üst başlığı (en üstteki metin bloğu)
        text = page.get_text("text")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = " / ".join(lines[:4])[:90]
        # raporun kendi beyan ettiği deal sayısı (doğrulama çapası)
        for m in SELF_COUNT_RE.finditer(text):
            out["self_reported"].append(
                {"page": i, "n": int(m.group(1) or m.group(2))})
        d = detect(page, w, h)
        if d:
            d["page"] = i
            d["page_title"] = title
            d["signals"] = weak_signals(page)
            out["tables"].append(d)
        else:
            s = weak_signals(page)
            # kart-ızgara eşiği: >=5 round-type token, grafik ekseni DEĞİL
            # (>=6 farklı yıl), ve başlık listeleme sayfasına işaret ediyor
            cards = count_cards(page, w, h)
            if (s["years"] < 6 and LIST_TITLE_RE.search(title)
                    and (cards >= MIN_ROWS or s["round_tok"] >= 5)):
                out.setdefault("cardgrids", []).append(
                    {"page": i, "page_title": title, "n_cards": cards,
                     "signals": s})
    # records_cols çıktıyı şişirir; yalnız --dump-cols ile göster
    if "--dump-cols" not in sys.argv:
        for t in out["tables"]:
            t.pop("records_cols", None)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if "--json" in sys.argv:
        dst = sys.argv[sys.argv.index("--json") + 1]
        with open(dst, "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
