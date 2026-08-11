# KNOWN ISSUES

Kaynak raporlardaki hatalar. **Sessizce düzeltilmez** (CLAUDE.md kısıt #5) —
ham değer olduğu gibi kalır, hata burada kayda geçer, çıkarım kodu uyarır.

Her kayıt: nerede, ne yanlış, nasıl anlaşıldı, çıkarımda ne yapılacak.

---

## KI-001 — 2026q1.pdf p10: yıl başlıkları bir kolon kaymış

**Sayfa:** `2026q1.pdf` p10 — TOP 10 FUNDED VERTICALS (DEAL COUNT)

**Sorun:** Kolon başlıkları `2020 2021 2022 2023 2024 2025` yazıyor. Aynı
raporun p9'unda (DEAL SIZE) aynı grafiğin başlıkları `2021 2022 2023 2024 2025
2026-Q1`. p10'un başlıkları bir kolon geride.

**Kanıt:** Son kolonun değerleri çeyreklik ölçekte — Artificial intelligence
`12`, bir önceki kolon `106`; Healthtech `6`, önceki `49`. Yıllık bir düşüş
değil, Q1 kısmi verisi. Ayrıca p9 ile p10'un tick x-koordinatları aynı
(409/659/908/1157/1406), yalnız etiket metinleri farklı.

**Doğru okuma:** p10 kolonları `2021 2022 2023 2024 2025 2026-Q1` olmalı.

**Çıkarımda:** Bu sayfadan otomatik çıkarım YAPILMAZ. `extract_facts.py`
sayfayı görürse uyarır ve atlar. Aynı veri `2026q2.pdf` p7'de doğru
başlıklarla var (2021…2026-H1) — oradan alınmalı.

---

## KI-002 — 2025.pdf p13: başlık yılı yanlış

**Sayfa:** `2025.pdf` p13 — başlık "TOP 10 FUNDED VERTICALS IN **2024**
(DEAL COUNT)"

**Sorun:** 2025 raporu, kolonlar `2020 2021 2022 2023 2024 2025`, son kolon
2025 verisi. Başlıkta yazan `2024` yanlış; p12 (DEAL SIZE) doğru şekilde
"IN 2025" diyor.

**Kanıt:** Kolon başlıkları 2020-2025; p12 ile aynı yıl aralığı ve aynı rapor.

**Çıkarımda:** Yalnız başlık metni hatalı, VERİ DOĞRU. Kolon başlıklarından
çıkarım yapılır, sayfa başlığındaki yıl kullanılmaz. `extract_facts.py` bu
sayfada uyarı basar ama çıkarıma devam eder.

---

## KI-003 — 2022.pdf p11: SaaS deal count aynı sayfada iki farklı değer

**Sayfa:** `2022.pdf` p11 — TOP 5 FUNDED VERTICALS IN 2022

**Sorun:** Sayfada iki grafik var. Üstteki (BY DEAL SIZE) SaaS deal count'unu
**23**, alttaki (BY DEAL COUNT) **33** gösteriyor. Aynı rapor, aynı yıl, aynı
tag. İkisi de aynı sayfada.

**Kanıt:** Vision + text layer ikisinde de aynı; çıkarım hatası değil, kaynakta
var. Alttaki grafik deal count'a göre azalan sıralı: 34, **33**, 26, 24, 24 —
23 olsaydı sıra bozulurdu (23 < 26). Sonraki vintage'lar da 33'ü destekliyor:
2023 raporu SaaS 2022 = 35, 2024 = 36, 2025 = 35. Yani üstteki grafikteki
**23 dizgi hatası**.

**Çıkarımda:** Her grafik KENDİ sıralama metriğinde otorite kabul edilir —
deal count için BY DEAL COUNT grafiği kazanır. `33` yazılır, satır
`confidence=low` işaretlenir. Ham `23` değeri
`extracted/2022_verticals.json` içindeki ÇAKIŞMA flag'inde durur, silinmez.

---

## KI-004 — ŞEMA AÇIĞI: aynı yılın iki çeyrekliği ayırt edilemiyor

**Bu bir kaynak hatası değil, facts.csv şemasının açığı. Karar gerekiyor.**

`2026q1.pdf` ve `2026q2.pdf` ikisi de `report_year=2026` (CLAUDE.md: dosya adı =
rapor yılı, çeyrek bilgisi period'da). Ama `period`, data_year'ı nitelendirir,
vintage'ı değil. İkisinin de yayınladığı geçmiş FY satırlarında
`period=FY` olur → unique anahtar
`(data_year, period, report_year, metric, dim_value_canon, scope)` ÇAKIŞIR.

Oysa değerler farklı: 2026q2, 2026q1'in yayınladığı geçmişi revize ediyor.
40 ortak anahtarın **8'i farklı**:

| data_year | tag | 2026q1 | 2026q2 |
|---|---|---|---|
| 2023 | artificial_intelligence | $49.8M | $50.3M |
| 2023 | marketingtech | $4.7M | $5.2M |
| 2023 | saas | $43.9M | $44.4M |
| 2024 | fintech | $196.6M | $196.9M |
| 2025 | artificial_intelligence | $40.3M | $40.5M |
| 2025 | fintech | $220M | $220.4M |
| 2025 | gaming | **$181M** | **$191.8M** |
| 2025 | marketingtech | $16.3M | $16.4M |

**ÇÖZÜLDÜ.** facts.csv'ye `report_id` kolonu eklendi ve unique anahtar
`(data_year, period, report_id, metric, dim_value_canon, scope)` oldu.
`2026q1` ve `2026q2` artık ayrı vintage olarak yan yana duruyor; yukarıdaki
8 revizyonun ikisi de saklanıyor, hiçbiri düşmüyor — CLAUDE.md kısıt #1.

`report_year` kolonu kaldı ama artık yalnız gruplama/sıralama için;
tek başına vintage anahtarı değil. qa.py `report_id ↔ source_file` 1:1
eşlemesini denetliyor.

---

## KI-005 — gaming 2022: $362M → $108M (DOĞRULANMIŞ REVİZYON, hata değil)

**Kayıt:** `funding_by_vertical_size`, `dim_value_canon=gaming`,
`data_year=2022`

| report_id | değer |
|---|---|
| 2022 | **$362M** |
| 2023 | **$108.3M** |
| 2024 | $113.3M |
| 2025 | $116M |
| 2026q2 | $116M |

**Sebep:** COVERAGE.md sentez bölümü **S7** — 2023 raporu, Dream Games'in 2022
dealını 2021'e taşıdı.

**Doğrulama:** Taşımanın iki yarısı da `sheets/revisions.csv`'de aynı vintage
adımında (2022→2023) yan yana duruyor ve birbirini tutuyor:

| kayıt | 2022 raporu | 2023 raporu | değişim |
|---|---|---|---|
| gaming 2021 size | $265M | $520M | **+$255M** |
| gaming 2022 size | $362M | $108.3M | **−$254M** |

Yani ~$254M 2022'den çıkıp 2021'e eklenmiş; toplam korunmuş. Bu, revizyonun
gerçekten bir deal taşıması olduğunun (yeniden ölçüm değil) kanıtı.

**Bu bir hata DEĞİL.** Yayıncının bilinçli vintage revizyonu; CLAUDE.md
kısıt #1'in ta kendisi. Her iki değer de facts.csv'de duruyor, hiçbiri
silinmedi, düzeltilmedi. `confidence=high` — okuma doğru, değişen veri.

**Dashboard'da:** gaming 2022'yi tek bir sayı olarak gösterme; hangi
report_id'den geldiğini belirt. 2022 raporu vintage'ıyla 2023+ vintage'ını
aynı seride birleştirmek 3x'lik sahte bir düşüş üretir.

**Aynı sınıftan diğer doğrulanmış revizyonlar** (185 adımın tamamı
`sheets/revisions.csv`'de): artificial_intelligence 2018 $0.6M→$9.5M (2018
raporu bu tag'i yalnız düzyazıda veriyordu, kapsam dardı),
grocery_delivery 2020 $10M→$0M, gaming 2020 $8M→$14.7M→$20M,
healthtech 2025 29→51 deal (2025 raporu → 2026q2).

---

## Bunlar hata DEĞİL (karıştırmayın)

- **Aynı data_year'ın vintage'lar arası farkı** revizyondur, hata değil.
  Her ikisi de saklanır (CLAUDE.md kısıt #1). Bkz. `is_provisional`.
- **Bir tag'in bir raporun top-10'unda olmaması** sıfır değil, "yok"tur.
  Satır yazılmaz (CLAUDE.md kısıt #4).
- **2020 p14'te "Education", p5'te "EDTECH"** — yazım farkı, `dim_verticals.csv`
  ikisini de `edtech` altında topluyor.
