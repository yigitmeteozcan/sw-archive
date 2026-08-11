# sw-archive

Yıllık ve çeyreklik ekosistem raporlarındaki sayıları tek bir queryable
dataset'e çeviren pipeline.

## Pipeline

```bash
.venv/bin/python scripts/extract_facts.py     <report_id> --write
.venv/bin/python scripts/extract_verticals.py <report_id> --write
.venv/bin/python scripts/qa.py                 # 0 hata görmeden devam etme
.venv/bin/python scripts/build_sheets.py       # -> sheets/
.venv/bin/python scripts/build_site.py         # -> docs/data/
```

Doğrulama, çıkarım kodundan bağımsız ikinci yoldan koşar:

```bash
.venv/bin/python scripts/verify_facts.py render
.venv/bin/python scripts/verify_facts.py compare
.venv/bin/python scripts/verify_facts.py checks
```

## Dokümanlar

| dosya | ne |
|---|---|
| [CLAUDE.md](CLAUDE.md) | şema, kısıtlar, yasaklar |
| [COVERAGE.md](COVERAGE.md) | hangi rapor hangi metriği hangi yıllar için içeriyor |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | kaynak hataları ve doğrulanmış revizyonlar |
| [VERIFY.md](VERIFY.md) | doğrulama sonucu |
| [DEALTABLES.md](DEALTABLES.md) | deal-level tablo kapsam taraması |
| [SHEETS_SETUP.md](SHEETS_SETUP.md) | Google Sheets senkronu |
