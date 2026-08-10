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
facts.csv    tek gerçek kaynak (append-only)
COVERAGE.md  hangi rapor hangi metriği hangi yıllar için içeriyor
PROGRESS.md  hangi rapor bitti / şüpheli / bekliyor

Dosya adı = rapor yılı. Vintage bilgisi buradan geliyor, asla karıştırma.

## Şema (facts.csv)
data_year | period | report_year | metric | dim_type | dim_value_raw |
dim_value_canon | scope | unit | value | source_file | page | confidence

- data_year   : verinin ait olduğu yıl
- period      : FY | Q1 | Q2 | H1 — data_year'ın hangi dilimi
                Yıllık rapordaki tüm satırlar FY. Çeyreklik raporlar Q1/Q2/H1.
                period, data_year'ı nitelendirir; raporun vintage'ı DEĞİLDİR
                (o report_year + source_file'da).
- report_year : hangi raporda böyle yayınlandığı (vintage)
- scope       : all | ex_bigg | ex_getir_bigg | diaspora
- confidence  : high | medium | low (low = insan doğrulaması şart)

Farklı period'lar asla karşılaştırılmaz ve asla toplanmaz.
Q1 + Q2 = H1 varsayma; rapor H1 diyorsa H1 yaz, demiyorsa boş bırak.

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
- (data_year, period, report_year, metric, dim_value_canon, scope) unique olmalı
- Aynı data_year'ın farklı vintage'ları arasındaki fark %20'yi geçerse flag
- YoY sadece aynı period içinde hesaplanır (Q1 vs Q1). Period karışırsa hata.
- period ∈ {FY, Q1, Q2, H1}, boş olamaz

## Yasak
- Okunamayan sayıyı tahmin etme. `confidence: low` yaz ve PROGRESS.md'ye düş.
- Tek geçişe güvenme. Chart slide'larında text layer + vision, uyuşmazsa flag.
- raw/ içine yazma, oradaki dosyaları değiştirme.

## Session akışı
PROGRESS.md oku → sıradaki raporu işle → extracted/ yaz → qa.py → PROGRESS güncelle
