# sw-archive



## Katmanlar

| katman | dosya | ne işe yarar |
|---|---|---|
| ham | `raw/*.pdf` | gitignored, dokunulmaz |
| çıkarım | `extracted/*.json` | rapor başına ham çıktı + flag'ler |
| gerçek kaynak | `facts.csv` | agregat metrikler, append-only, tüm vintage'lar |
| export | `sheets/*.csv` | Sheets/site için düzleştirilmiş 4 dosya |
| site | `docs/` | GitHub Pages dashboard |

## Akış

```bash
.venv/bin/python scripts/extract_facts.py    <report_id> --write   # headline
.venv/bin/python scripts/extract_verticals.py <report_id> --write  # sektör
.venv/bin/python scripts/qa.py                # 0 hata görmeden devam etme
.venv/bin/python scripts/build_sheets.py      # -> sheets/
.venv/bin/python scripts/build_site.py        # -> docs/data/
git add -A && git commit -m "…" && git push
```

## Dokümanlar

- [CLAUDE.md](CLAUDE.md) — şema, kısıtlar, yasaklar
- [COVERAGE.md](COVERAGE.md) — hangi rapor hangi metriği hangi yıllar için içeriyor
- [DEALTABLES.md](DEALTABLES.md) — deal-level tablo taraması (henüz çıkarılmadı)
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) — kaynak hataları ve doğrulanmış revizyonlar
- [SHEETS_SETUP.md](SHEETS_SETUP.md) — Google Sheets senkronizasyonu

## GitHub Pages'i açma (tek seferlik)

Site `docs/` klasöründen yayınlanıyor. Repo ayarlarından bir kez açmak gerekiyor:

1. GitHub'da repo → **Settings** → sol menüde **Pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main`, klasör: **`/docs`** → **Save**
4. 1-2 dakika sonra `https://yigitmeteozcan.github.io/sw-archive/` yayında

> Repo private olsa bile **yayınlanan site herkese açıktır** (private Pages
> yalnız GitHub Enterprise'da). `docs/data/` altındaki veri internete açılır.

Sonraki her `git push` siteyi otomatik günceller — ayrıca bir şey yapmaya
gerek yok.
