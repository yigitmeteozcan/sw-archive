# sw-archive

startups.watch'un 2015–2026 Türkiye ekosistem raporlarındaki sayılar, PDF'lerin
içinden çıkarılıp tek bir queryable dataset'e dönüştürülmüş hali.

**→ [Canlı dashboard](https://yigitmeteozcan.github.io/sw-archive/)** — sektör ve
yıl seçip karşılaştırma, tam seri grafiği, paylaşılabilir link.

## Veri

760 kayıt · 33 sektör · 2010–2026 · 10 rapordan 18 sayfa.

Her sayı iki kez okundu: PDF metin katmanından koordinat bazlı çıkarım, sonra
sayfa render edilip görsel kontrol. İkisi uyuşmazsa satır `confidence: low`
işaretlenir. Tahmin ya da enterpolasyon yok — okunamayan sayı yazılmaz.

| dosya | ne |
|---|---|
| `facts.csv` | tek gerçek kaynak. Agregat metrikler, append-only, **tüm vintage'lar** |
| `sheets/` | düzleştirilmiş export — `latest` (en güncel vintage), `revisions` (vintage farkları) |
| `docs/data/` | sitenin okuduğu JSON + indirilebilir CSV'ler |
| `extracted/` | rapor başına ham çıkarım çıktısı ve flag'ler |
| `dim_verticals.csv` | 61 ham sektör adı → 37 canonical eşlemesi |

Şema, kısıtlar ve yasaklar: **[CLAUDE.md](CLAUDE.md)**.
Hangi rapor hangi metriği hangi yıllar için içeriyor: **[COVERAGE.md](COVERAGE.md)**.

## Pipeline

```bash
.venv/bin/python scripts/extract_facts.py     <report_id> --write   # headline
.venv/bin/python scripts/extract_verticals.py <report_id> --write   # sektör
.venv/bin/python scripts/qa.py                 # 0 hata görmeden devam etme
.venv/bin/python scripts/build_sheets.py       # -> sheets/
.venv/bin/python scripts/build_site.py         # -> docs/data/
```

Doğrulama ayrı bir yoldan koşar (çıkarım koduna hiç dokunmaz):

```bash
.venv/bin/python scripts/verify_facts.py render    # sayfaları PNG'ye çevirir
.venv/bin/python scripts/verify_facts.py compare   # görsel okuma vs facts.csv
.venv/bin/python scripts/verify_facts.py checks    # iç tutarlılık
```

## Bilinen sınırlar

- **Son yıl her zaman geçici.** Rapor kendi son yılını eksik raporlar, sonraki
  vintage'da şişer: 2024 deal count 469 → 588, 2025 306 → 388. Bu satırlar
  `is_provisional=TRUE`.
- **Aynı yıl farklı raporlarda farklı değer taşır.** Hepsi saklanır, hiçbiri
  silinmez. En büyük revizyon: gaming 2022 $362M → $108M (Dream Games'in dealı
  2021'e taşındı).
- **Sektör tag'leri birbirini dışlamaz** — toplamları ekosistem toplamını vermez.
- **Boş hücre "yok" demek, sıfır değil.** Tag o yıl raporun ilk 10'unda değilse
  satır yazılmaz.
- **Kısmi dönemler** (2026-Q1, 2026-H1) tamamlanmış yılla aynı eksene konmaz.
- **`ex_getir_bigg` kapsamında sektör kırılımı yok** — startups.watch o kapsamda
  yalnız ekosistem toplamını yayınlıyor.
- **Deal-level tablolar henüz çıkarılmadı** — kapsam taraması
  [DEALTABLES.md](DEALTABLES.md)'de, ~184 satır bekliyor.

Kaynak hataları ve doğrulanmış revizyonlar: **[KNOWN_ISSUES.md](KNOWN_ISSUES.md)**.
Doğrulama sonucu: **[VERIFY.md](VERIFY.md)**.

## Google Sheets

Veri katmanı olarak Sheets'e de senkronlanıyor (QA ve elle inceleme için).
Kurulum: [SHEETS_SETUP.md](SHEETS_SETUP.md).

---

Veri startups.watch'a aittir; bu repo yalnız yayınlanmış raporlardaki sayıları
makine-okunur hale getirir.
