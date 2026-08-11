# DEALTABLES

Deal-level (satır = tek yatırım turu) tablo taraması. **Hızlı tespit taraması —
tam coverage değil, sayı çıkarılmadı.** Sadece: tablo var mı, hangi sayfada,
hangi kolonlarla, kaç satır.

Kapsam: raw/ içine yeni eklenen **27 çeyreklik rapor** (2015q1 … 2025q3).
`2026q1` / `2026q2` bu taramanın dışında — onlar zaten COVERAGE.md'de işlenmişti.

Üretim: `scripts/dealtable_scan.py` (rapor başına tek tek çalıştırıldı).
Yöntem başlık ismine güvenmez, tablo geometrisine bakar: kelime koordinatları →
satır kümeleme → kolon çapası histogramı → kayıt gruplama. İki hizalama modu
(sol-hizalı / ortalanmış) denenir. Kalibrasyon: `2015q4.pdf` p6 "ROUNDS &
DETAILS" (34 satır, rapor p3'te "In 34 rounds." diyor — birebir tuttu).

Satır sayıları, raporun kendi beyanıyla (`"$X across N deals"` / `"in N rounds"`)
çapraz doğrulandı; `rapor beyanı` kolonu o değerdir.

---

## A. Tam deal-level tablo — hizalı kolonlar, çeyreğin TÜM deal'leri

| rapor | tablo | sayfa | kolonlar | tahmini satır | rapor beyanı |
|---|---|---|---|---|---|
| 2015q1 | ✅ VAR | **p4** | startup, investors, type, amount, date | 16 | — |
| 2015q3 | ✅ VAR | **p4** | startup, vertical, investor, type, amount | 10 | — |
| 2015q4 | ✅ VAR | **p6** | startup, funding (type), amount ($), vertical, investors, city | 34 | 34 ✓ |
| 2016q1 | ✅ VAR | **p6** | startup, funding type, amount ($), vertical, investors, city | ~20 | 20 ✓ |
| 2016q2 | ✅ VAR | **p6** | startup, investor, type, amount raised ($), tags, city | 13 | 13 ✓ |
| 2016q3 | ✅ VAR | **p8** | startup, investors, round type, amount raised ($), **post-money val. ($)**, tags, date | 17 | 17 ✓ |

Başlık isimleri gerçekten değişiyor: `INVESTMENT ROUNDS` (2015q1, 2015q3) →
`ROUNDS & DETAILS` (2015q4–2016q3). Kolon seti de sabit değil — `city` 2015q4'te
giriyor, `date` 2015q1'de var / 2015q4-2016q2'de yok / 2016q3'te dönüyor,
`post-money valuation` yalnız 2016q3'te var.

**Ara toplam: ~110 deal satırı.**

## B. Kart-ızgara listeleme — çeyreğin TÜM deal'leri, ama tablo değil

Hizalı tablo yok; her deal bir "kart" (üstte startup adı, altında değerler),
sayfada 6-9 sütunluk ızgara halinde. Veri deal-level ama alan seti dar.

| rapor | tablo | sayfa | kolonlar (alanlar) | tahmini satır | rapor beyanı |
|---|---|---|---|---|---|
| 2018q1 | ⚠️ kart ızgara | **p6** | startup, amount | 17 | 17 ✓ |
| 2018q2 | ⚠️ kart ızgara | **p5** | startup, amount | 16 | 16 ✓ |
| 2019q1 | ⚠️ kart ızgara | **p10** | startup, amount, round type, investors | 13 | 13 ✓ |
| 2019q2 | ⚠️ kart ızgara | **p10** | startup, amount, round type, investors | 12 | 12 ✓ |
| 2019q3 | ⚠️ kart ızgara | **p12** | startup, amount, investors | 16 | 16 ✓ |

`vertical` ve `city` bu dönemde tamamen düşüyor. `round type` 2018'de yok,
2019q1-q2'de var, 2019q3'te tekrar yok.

**Ara toplam: ~74 deal satırı.**

## C. Sadece Top-N — çeyreğin tamamı DEĞİL

Tam liste yayınlanmıyor; yalnız en büyük 5-10 deal gösteriliyor. Deal-level ama
kapsam kısmi → seri kurmaya uygun değil.

| rapor | sayfa | başlık | alanlar | satır |
|---|---|---|---|---|
| 2020q1 | p7 | TURKEY TOP 10 VC DEALS | startup (yalnız isim) | 10 |
| 2020q2 | p8 | TURKEY TOP 10 VC DEALS | startup (yalnız isim) | 10 |
| 2020q3 | p9 | TURKEY TOP 10 VC DEALS | startup (yalnız isim) | 10 |
| 2021q1 | p9 | TOP 10 ANGEL & VC DEALS | startup, amount, round type | 10 |
| 2021q2 | p9 | TOP 10 ANGEL & VC DEALS | startup, amount, round type | 10 |
| 2021q3 | p8 | TOP 10 ANGEL & VC DEALS | startup, amount, round type | 10 |
| 2022q1 | p6 | TOP 5 ANGEL & VC DEALS | anlatı metni (tablo değil) | 5 |

2020 üçlüsü logo/isim ızgarası — tutar ve tur tipi deal bazında YOK, sadece
"10 startup toplam funding'in %X'ini aldı" toplamı var.

## D. Deal-level tablo YOK

`2022q3`, `2023q1`, `2023q3`, `2024q1`, `2024q2`, `2024q3`, `2025q1`, `2025q2`,
`2025q3`

Bu raporlarda tespit edilen tüm "tablo"lar grafik/sıralama tablosu (vertical ×
yıl, city league, stage × yıl). Dedektör bunları başlıksız (`header: None`) ve
kolonları yıl etiketi olarak işaretliyor — deal-level değil.
Tek istisna: `2023q1` p15 `CRYPTO TOKEN DEALS` — tek deal (Metatime), seri değeri yok.

---

## Ek listeler (ayrı metrik / ayrı scope — deal tablosu sayılmaz)

- **Exits & acquisitions tabloları:** 2015q1 p5, 2015q3 p8, 2016q1 p7,
  2016q2 p7, 2016q3 p9, 2018q1 p14, 2018q2 p11, 2019q1 p11, 2019q2 p11,
  2019q3 p14. Kolonlar: startup, acquirer, %, amount, tags/vertical, investors.
  Her biri 2-8 satır, toplam ~45. Bu `Acquisitions & secondary` metriği — yatırım
  turu değil, karıştırma.
- **Diaspora / yurtdışı listeleri:** 2019q1 p19 (9), 2019q2 p17 (4),
  2019q3 p13 (6), 2020q3 p16, 2021q1 p25. `scope=diaspora`, ayrı tutulmalı.

---

---

## Kolon harmonizasyon eşlemesi

Makine-okunur hali: `dim_deal_fields.tsv` (report_id | deals_field | raw_label |
present | note). Aşağısı özet.

### Alan × rapor matrisi

`•` = var (ham başlık), `·` = pozisyonel (başlıksız kart), boş = yok

| deals.csv alanı | 15q1 | 15q3 | 15q4 | 16q1 | 16q2 | 16q3 | 18q1 | 18q2 | 19q1 | 19q2 | 19q3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| startup         | • | • | • | • | • | • | · | · | · | · | · |
| round_type      | • | • | • | • | • | • |   |   | · | · |   |
| amount_usd      | • | • | • | • | • | • | · | · | · | · | · |
| amount_status   |   |   | • | • |   |   |   |   |   |   |   |
| verticals_raw   |   | • | • | • | • | • |   |   |   |   |   |
| investors       | • | • | • | • | • | • |   |   | · | · | · |
| investor_types  | • | • | • | • | • | • |   |   |   |   |   |
| city            |   |   | • | • | • |   |   |   |   |   |   |

### Alan ne zaman giriyor / çıkıyor

- `city` → **2015q4'te girer**, 2016q3'te **çıkar**. Yalnız 3 raporda var.
- `verticals_raw` → 2015q3'te girer, 2016q3'e kadar sürer, **2018'de tamamen düşer**.
  Başlık adı 2016q2'de `Vertical` → `Tags` olur (aynı alan, farklı ad).
- `investor_types` → 2015q1–2016q3 arası kodlu, **2019'da kod eki tamamen kalkar**
  (yatırımcı yalnız düz isim). 2018'de yatırımcı alanı hiç yok.
- `round_type` → 2015q1–2016q3 var, **2018'de düşer**, 2019q1–q2'de **döner**,
  2019q3'te **yine düşer**. En kırılgan alan.
- `amount_status` → yalnız 2015q4 ve 2016q1'de açık `(est)` eki var. Diğerlerinde
  ya `N/A` (tutar yok) ya da hiç nitelendirme yok → `exact` VARSAYMA, boş bırak.
- Şema dışı iki alan: `date` (2015q1, 2016q3) ve `post_money_valuation` (2016q3).
  Kararlaştırılan deals.csv şemasında karşılıkları yok → çıkarımda düşecekler.

### Değer harmonizasyonu

**round_type** — büyük/küçük harf tutarsız, ham değer korunmalı, canon ayrı:
`seed` / `Seed` → `Seed` · `Pre-seed` / `pre-seed` → `Pre-Seed` ·
`Series A|B|C` → aynen · `Corporate Round` (yalnız 2019q2) → `Corporate`

**investor_types** — **KAPALI liste** kullan:
`P` (kişi/melek) · `VC` · `BAN` (melek ağı) · `PE` · `FI` (finansal kuruluş) ·
`AF` (hızlandırıcı fonu, 2015q4'te girer) · `CVC` · `GE` · `CR` ·
`Angel` (2016q2'de `P` yerine geçer — eşanlamlı say)

⚠️ Parantez içindeki her token tip kodu **değildir**. `(IFC)`, `(SBS)`, `(GBA)`,
`(MBCO)` şirket kısaltmasıdır ve yatırımcı **ismine** aittir. Kapalı liste dışı
her parantez isme dahil edilmeli — aksi halde sahte tip kodları üretilir.
(Bu, ilk taramada dedektörün de düştüğü hataydı; `dealtable_scan.py` düzeltildi.)

**amount_usd** — biçim raporlar arası değişiyor: `$1,234,567` (2015q1),
`85.000` (2015q3+), `$1M` / `$500K` kısaltmalı (2018+). Ayraç ve kısaltma
normalize edilmeli; `N/A` ve `-` → BOŞ (0 değil).

**verticals_raw** — çoklu tag virgüllü tek hücrede. Mutually exclusive değil,
`verticals_canon` eşlemesi `dim_verticals.csv` üzerinden yapılmalı.

## Uyarılar

1. **`period` şeması Q3/Q4'ü kaldırmıyor.** CLAUDE.md ve qa.py `period ∈
   {FY, Q1, Q2, H1}` diyor. Deal tablosu olan raporların yarısı Q3 çeyreği
   (2015q3, 2016q3, 2019q3, 2020q3, 2021q3, 2022q3, 2023q3, 2024q3, 2025q3).
   Bu satırlar yazılmadan önce şema Q3/Q4'e (ve muhtemelen 9M/YTD'ye)
   genişletilmeli — yoksa QA hepsini reddeder.
2. **Grain farklı.** facts.csv agregat şemasında (metric/dim/value). Deal-level
   tablo satır=deal grain'inde; facts.csv'ye sığmaz, ayrı `deals.csv` ister.
   Agregatlar oradan türetilirse `facts.csv` ile çift sayım riski doğar.
3. **Bu bir tespit taraması.** Satır sayıları geometrik tahmindir (±1-3).
   Rapor beyanı olan yerlerde beyan esastır. Gerçek çıkarımda her tablo tek tek
   ve `confidence` etiketiyle işlenmeli.
4. **2018q1'de 3 sayfa text layer'sız** (p19, p21, p24) — hepsi etkinlik/foto
   sayfası, deal tablosu değil. Diğer 26 raporda text layer eksiği yok.
