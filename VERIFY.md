# VERIFY

`facts.csv`'nin kaynak PDF'e karşı **bağımsız** doğrulaması.

**Yöntem:** çıkarım kodu (`extract_facts.py`, `extract_verticals.py`) ve
`extracted/*.json` bu doğrulamaya HİÇ girmez — aynı parser aynı hatayı
iki kez yapardı. İkinci yol PDF'in metin katmanına da bakmaz: sayfa
piksel olarak render edilir, sayılar görsel olarak okunur
(`verify/readings.json`), sonra `facts.csv` ile karşılaştırılır.

## Sonuç

| durum | satır |
|---|---|
| OK | **420** |
| MISMATCH | **0** |
| UNREADABLE | **340** |
| toplam | 760 |

Görsel doğrulama kapsamı: **%55.3**

Satır bazında tam döküm: `verify_report.csv`

## UNREADABLE (340)

Görsel okuma kaydı olmayan ya da etiketi okunamayan satırlar.

- 2018 · funding_by_vertical_count: 14 satır
- 2018 · funding_by_vertical_size: 4 satır
- 2019 · funding_by_vertical_count: 7 satır
- 2019 · funding_by_vertical_size: 7 satır
- 2020 · funding_by_vertical_count: 14 satır
- 2020 · funding_by_vertical_size: 14 satır
- 2021 · funding_by_vertical_count: 8 satır
- 2021 · funding_by_vertical_size: 8 satır
- 2022 · funding_by_vertical_count: 7 satır
- 2022 · funding_by_vertical_size: 7 satır
- 2024 · total_deal_count: 21 satır
- 2024 · total_deal_size: 21 satır
- 2025 · total_deal_count: 22 satır
- 2025 · total_deal_size: 22 satır
- 2026q2 · funding_by_vertical_count: 60 satır
- 2026q2 · funding_by_vertical_size: 60 satır
- 2026q2 · total_deal_count: 22 satır
- 2026q2 · total_deal_size: 22 satır

## İç tutarlılık kontrolleri

| kontrol | durum | özet |
|---|---|---|
| Basılı YoY % ∈ yuvarlamadan doğan aralık | **PASS** | 38 basılı yüzdenin hepsi, etiket yuvarlamasının izin verdiği aralığın içinde |
| Stage toplamı ≤ headline total | **N/A** | facts.csv'de stage kırılımı yok — kontrol uygulanamıyor |
| Vertical Σ ≤ 3× headline total | **PASS** | 64 (yıl,rapor,scope) grubunun hepsi eşiğin altında |
| Deal count'lar tam sayı | **PASS** | 355 count satırının hepsi tam sayı |
| Vintage sapması ≤ %30 | **FLAG** | 40 ölçüm %30'u aşıyor |

### Vintage sapması %30 üzeri

Bunlar hata değil, yayıncının revizyonu — `KNOWN_ISSUES.md` KI-005.

| ölçüm | vintage'lar | sapma |
|---|---|---|
| artificial_intelligence 2018-FY funding_by_vertical_size | 2018=600000, 2023=9.5e+06 | %1483 |
| gaming 2022-FY funding_by_vertical_size | 2022=3.62e+08, 2023=1.083e+08, 2024=1.133e+08, 2025=1.16e+08, 2026q1=1.16e+08, 2026q2=1.16e+08 | %234 |
| artificial_intelligence 2018-FY funding_by_vertical_count | 2018=5, 2023=13 | %160 |
| gaming 2020-FY funding_by_vertical_size | 2020=8e+06, 2023=1.47e+07, 2024=2e+07, 2025=2e+07 | %150 |
| internet_of_things 2018-FY funding_by_vertical_count | 2018=5, 2023=10 | %100 |
| gaming 2021-FY funding_by_vertical_size | 2021=2.65e+08, 2023=5.2e+08, 2024=5.2e+08, 2025=4.915e+08, 2026q1=4.915e+08, 2026q2=4.915e+08 | %96 |
| fintech 2019-FY funding_by_vertical_size | 2019=8.4e+06, 2023=4.3e+06, 2024=4.3e+06 | %95 |
| fintech 2018-FY funding_by_vertical_count | 2018=10, 2023=18 | %80 |
| artificial_intelligence 2020-FY funding_by_vertical_count | 2020=14, 2023=19, 2024=19, 2025=25 | %79 |
| healthtech 2025-FY funding_by_vertical_count | 2025=29, 2026q2=51 | %76 |
| saas 2018-FY funding_by_vertical_count | 2018=10, 2023=17 | %70 |
| gaming 2020-FY funding_by_vertical_count | 2020=12, 2023=18, 2024=20, 2025=20 | %67 |
| artificial_intelligence 2022-FY funding_by_vertical_count | 2022=26, 2023=31, 2024=38, 2025=43, 2026q2=43 | %65 |
| artificial_intelligence 2020-FY funding_by_vertical_size | 2020=3.9e+07, 2023=4.33e+07, 2024=4.33e+07, 2025=6.32e+07 | %62 |
| artificial_intelligence 2021-FY funding_by_vertical_size | 2021=1.8e+07, 2023=1.91e+07, 2024=2.05e+07, 2025=2.57e+07, 2026q1=2.86e+07, 2026q2=2.86e+07 | %59 |
| ecommerce 2020-FY funding_by_vertical_count | 2020=7, 2023=11 | %57 |
| marketplace 2020-FY funding_by_vertical_size | 2020=3e+06, 2025=4.7e+06 | %57 |
| fintech 2020-FY funding_by_vertical_count | 2020=16, 2023=25, 2024=25, 2025=25 | %56 |
| artificial_intelligence 2024-FY funding_by_vertical_count | 2024=75, 2025=115, 2026q2=116 | %55 |
| sustainability 2025-FY funding_by_vertical_count | 2025=10, 2026q2=15 | %50 |
| sustainability 2024-FY funding_by_vertical_count | 2024=28, 2025=40, 2026q2=42 | %50 |
| marketingtech 2020-FY funding_by_vertical_count | 2020=4, 2025=6 | %50 |
| biotech 2025-FY funding_by_vertical_count | 2025=17, 2026q2=25 | %47 |
| artificial_intelligence 2023-FY funding_by_vertical_count | 2023=47, 2024=59, 2025=65, 2026q2=69 | %47 |
| restaurant 2018-FY funding_by_vertical_size | 2018=1.5e+06, 2023=2.2e+06 | %47 |
