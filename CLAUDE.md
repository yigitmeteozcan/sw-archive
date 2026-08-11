# sw-archive

startups.watch'un 2015–2026 yıllık Türkiye ekosistem raporlarını (PDF/Keynote)
tek bir queryable dataset'e çeviriyoruz. Nihai hedef: Google Sheets dashboard'da
istenen HERHANGİ bir yıl kombinasyonunu (örn. 2015 + 2018 + 2026 aynı anda)
sektör/stage/scope bazında anında karşılaştırmak.

## Altın kural
PDF'leri asla toplu okuma. Her seferinde TEK rapor işlenir.
PDF'i kod okur, model sadece çıkan sayıları görür.

## Klasör
raw/         sw_2015.pdf … sw_2025.pdf + 2026q1.pdf, 2026q2.pdf
             (gitignored, ~80MB, dokunma)
extracted/   sw_2015.json …              (rapor başına ham çıktı)
scripts/     extract.py, qa.py
facts.csv    agregat metrikler — tek gerçek kaynak (append-only)
deals.csv    deal-level satırlar (satır = tek yatırım turu). AYRI TABLO.
             facts.csv'ye karışmaz, facts.csv'yi beslemez. Bkz. "deals.csv".
COVERAGE.md  hangi rapor hangi metriği hangi yıllar için içeriyor
DEALTABLES.md hangi raporda deal-level tablo var (kapsam taraması)
PROGRESS.md  hangi rapor bitti / şüpheli / bekliyor

Dosya adı = rapor yılı. Vintage bilgisi buradan geliyor, asla karıştırma.

## Şema (facts.csv)
data_year | period | report_id | report_year | metric | dim_type |
dim_value_raw | dim_value_canon | scope | unit | value | source_file | page |
confidence | is_provisional

- data_year   : verinin ait olduğu yıl
- period      : FY | Q1 | Q2 | Q3 | Q4 | H1 — data_year'ın hangi dilimi
                Yıllık rapordaki tüm satırlar FY. Çeyreklik raporlar Q1..Q4/H1.
                period, data_year'ı nitelendirir; raporun vintage'ı DEĞİLDİR
                (o report_year + source_file'da).
- report_id   : kaynak raporun kimliği (ör. 2025, 2026q1, 2026q2) — GERÇEK
                vintage anahtarı. report_year tek başına yetmez: 2026q1 ve
                2026q2 ikisi de report_year=2026 ama farklı vintage'lar ve
                aynı FY yılları için FARKLI değer yayınlıyorlar.
- report_year : raporun yılı (vintage kabaca). Gruplama/sıralama için;
                tek başına unique anahtar olamaz.
- scope       : all | ex_bigg | ex_getir_bigg | diaspora
- confidence  : high | medium | low (low = insan doğrulaması şart)
- is_provisional : TRUE | FALSE — bu satır raporun EN SON data_year'ı mı

### is_provisional — son yıl her zaman geçici

Her rapor kendi son yılını eksik raporlar; sonraki vintage'da şişer:
  2024 deal count: rapor 2024 → 469, rapor 2025 → 588 (+%25)
  2025 deal count: rapor 2025 → 306, rapor 2026q2 → 388 (+%27)
Tutar tarafında bu kayma yok, kırılma deal count'ta.

Kural: bir raporun EN SON data_year'ına ait TÜM satırlar `is_provisional=TRUE`.
Aynı data_year daha yeni bir raporda tekrar yayınlandığında o satır
`is_provisional=FALSE` olur (eski satır TRUE kalır, silinmez).

- Dashboard'da provisional yıl "kısmi/geçici" işaretlenmeli, trend çizgisinin
  son noktası olarak sunulmamalı.
- YoY hesaplarken provisional yılı kullanma; kullanıyorsan etiketle.
- Provisional satır yanlış değildir — o tarihteki en iyi bilgidir. Silme.

Farklı period'lar asla karşılaştırılmaz ve asla toplanmaz.
Q1 + Q2 = H1 varsayma; rapor H1 diyorsa H1 yaz, demiyorsa boş bırak.
Aynı şekilde Q1+Q2+Q3+Q4 = FY varsayma. Çeyrekler yıl toplamını vermez.

## deals.csv (deal-level, AYRI TABLO)

deal_id | report_id | period | data_year | startup | round_type |
amount_usd | amount_status | verticals_raw | verticals_canon |
investors | investor_types | city | confidence

- deal_id       : stabil satır kimliği (report_id + sıra)
- report_id     : kaynak rapor (ör. 2015q4) — vintage buradan
- period        : FY | Q1 | Q2 | Q3 | Q4 | H1 (facts.csv ile aynı enum)
- amount_status : exact | est — rapor "(est)" diyorsa est, tutar yoksa boş.
                  Açık "(est)" eki YALNIZ 2015q4 ve 2016q1'de var; diğer
                  raporlarda nitelendirme yok → exact VARSAYMA, boş bırak.
- verticals_raw : rapordaki ham tag'ler (virgüllü, olduğu gibi)
- investor_types: KAPALI liste — VC | P | BAN | AF | CVC | PE | FI | GE | CR
                  (Angel = P eşanlamlısı, 2016q2'de kullanılıyor).
                  Parantez içindeki her token tip kodu DEĞİLDİR: (IFC) (SBS)
                  (GBA) (MBCO) şirket kısaltmasıdır, yatırımcı İSMİNE aittir.
                  Liste dışı parantezi isme dahil et, tip üretme.

Alan seti rapordan rapora değişir; olmayan alan BOŞ kalır, 0/N-A yazılmaz.
Hangi raporun hangi alanı verdiği: DEALTABLES.md.

### YASAK: deals.csv'den agregat türetme

deals.csv KISMİ KAPSAMLIDIR. Çeyreklik raporlar o çeyreğin tüm turlarını
yayınlamaz; yıllık rapordaki toplamın çok altında kalır:
  2015 → deals.csv'de ~60 tur, yıllık rapor 100 tur diyor
  2016 → deals.csv'de ~50 tur, yıllık rapor 156 tur diyor
Üstelik bazı yıllar hiç yok (2017'nin tek bir çeyrekliği bile raw/'da yok) ve
mevcut yıllarda da çeyrek boşlukları var (2015Q2, 2016Q4, 2018Q3-Q4, 2019Q4).

Bu yüzden:
- deals.csv'den SUM/COUNT alıp facts.csv'ye yazma. Hiçbir koşulda.
- deals.csv'den toplam/ortalama/YoY/pay (%) hesaplama, dashboard'a koyma.
- deals.csv ile facts.csv'yi aynı grafikte toplama veya oranlama.
- deals.csv yalnız TEKİL deal sorgusu içindir: "hangi startup, hangi turda,
  kimden, ne zaman". Kapsam sorusunun cevabı değildir.
Toplamlar YALNIZCA facts.csv'den gelir (kaynağı raporun kendi agregatı).

## Kritik kısıtlar
1. startups.watch geçmişi her yıl revize ediyor. Aynı data_year farklı
   report_year'larda farklı değer taşır. İkisi de saklanır, hiçbiri silinmez.
2. Headline metrikler her raporda 10+ yıl geriye gider; vertical/stage/CVC
   kırılımları sadece ~6 yıl. Eski yıllar için birden fazla rapor dikilir.
3. Vertical tag'leri mutually exclusive DEĞİL → asla toplama.
4. Bir yılda tag yoksa değer BOŞTUR, 0 DEĞİL. (yok ≠ sıfır)
5. Geçmişi asla sessizce düzeltme. Ham değer kalır, düzeltme ayrı kolon olur.
6. 2026 YILLIK RAPOR YOK. raw/ içinde 2026q1.pdf ve 2026q2.pdf var — çeyreklik.
   - 2026 satırları period=Q1 / Q2 (rapor H1 diyorsa H1) taşır, asla FY.
   - 2026'yı yıllık serilere karıştırma; dashboard'da FY yıllarıyla yan yana
     koyma. Kısmi yıl, tamamlanmış yıl gibi görünmemeli.
   - "Dosya adı = rapor yılı" kuralı burada da geçerli: 2026q1.pdf →
     report_year 2026. Çeyrek bilgisi period kolonunda, report_year'da değil.
   - Çeyreklik raporlar geçmiş FY yıllarını da yayınlar (10 yıl geriye giden
     headline serisi). O satırlar period=FY kalır, sadece 2026 satırları
     çeyrekliktir. Tek raporda iki period bir arada olabilir.

## Sektör harmonizasyonu
dim_verticals.csv: raw_name | canonical_name | first_seen_year | comparable_from
Tag isimleri yıllara göre değişiyor, bazıları eski yıllarda yok.
Tek canonical filtre tüm yılları taramalı.

## QA kuralları (qa.py)
- Raporda yazan YoY % ile hesaplanan YoY % uyuşmalı
- Stage toplamları total'ı geçemez
- Deal count'lar integer
- (data_year, period, report_id, metric, dim_value_canon, scope) unique olmalı
  (report_year DEĞİL — aynı yılın iki çeyrekliği ayırt edilemez, bkz. KI-004)
- report_id ↔ source_file eşlemesi 1:1 olmalı
- Aynı data_year'ın farklı vintage'ları arasındaki fark %20'yi geçerse flag
- YoY sadece aynı period içinde hesaplanır (Q1 vs Q1). Period karışırsa hata.
- period ∈ {FY, Q1, Q2, Q3, Q4, H1}, boş olamaz (her iki tabloda da)
- deals.csv şeması facts.csv'ye sızmamalı (deal_id/startup kolonu facts'te olamaz)
- facts.csv'nin hiçbir satırı deals.csv kaynaklı olamaz (source_file kontrolü)
- deals.csv'deki deal sayısı, aynı (data_year, period) için facts.csv'deki
  toplam deal count'a EŞİT VEYA ÜSTÜNDE çıkarsa HATA — deals.csv kısmi
  olmalı; eşitlik "tam kapsam" yanılsaması demektir
- deals.csv'de agregat satırı olamaz (startup: total/toplam/other/diğer…)

## Yasak
- Okunamayan sayıyı tahmin etme. `confidence: low` yaz ve PROGRESS.md'ye düş.
- Tek geçişe güvenme. Chart slide'larında text layer + vision, uyuşmazsa flag.
- raw/ içine yazma, oradaki dosyaları değiştirme.
- deals.csv'den agregat türetme (yukarıdaki bölüm — en sık yapılacak hata bu).

## Session akışı
PROGRESS.md oku → sıradaki raporu işle → extracted/ yaz → qa.py → PROGRESS güncelle
