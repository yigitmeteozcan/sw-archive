# sw-archive

startups.watch'un 2015–2026 yıllık Türkiye ekosistem raporlarını (PDF/Keynote)
tek bir queryable dataset'e çeviriyoruz. Nihai hedef: Google Sheets dashboard'da
istenen HERHANGİ bir yıl kombinasyonunu (örn. 2015 + 2018 + 2026 aynı anda)
sektör/stage/scope bazında anında karşılaştırmak.

## Altın kural
PDF'leri asla toplu okuma. Her seferinde TEK rapor işlenir.
PDF'i kod okur, model sadece çıkan sayıları görür.

## Klasör
raw/         sw_2015.pdf … sw_2026.pdf   (gitignored, ~80MB, dokunma)
extracted/   sw_2015.json …              (rapor başına ham çıktı)
scripts/     extract.py, qa.py
facts.csv    tek gerçek kaynak (append-only)
COVERAGE.md  hangi rapor hangi metriği hangi yıllar için içeriyor
PROGRESS.md  hangi rapor bitti / şüpheli / bekliyor

Dosya adı = rapor yılı. Vintage bilgisi buradan geliyor, asla karıştırma.

## Şema (facts.csv)
data_year | report_year | metric | dim_type | dim_value_raw | dim_value_canon |
scope | unit | value | source_file | page | confidence

- data_year   : verinin ait olduğu yıl
- report_year : hangi raporda böyle yayınlandığı (vintage)
- scope       : all | ex_bigg | ex_getir_bigg | diaspora
- confidence  : high | medium | low (low = insan doğrulaması şart)

## Kritik kısıtlar
1. startups.watch geçmişi her yıl revize ediyor. Aynı data_year farklı
   report_year'larda farklı değer taşır. İkisi de saklanır, hiçbiri silinmez.
2. Headline metrikler her raporda 10+ yıl geriye gider; vertical/stage/CVC
   kırılımları sadece ~6 yıl. Eski yıllar için birden fazla rapor dikilir.
3. Vertical tag'leri mutually exclusive DEĞİL → asla toplama.
4. Bir yılda tag yoksa değer BOŞTUR, 0 DEĞİL. (yok ≠ sıfır)
5. Geçmişi asla sessizce düzeltme. Ham değer kalır, düzeltme ayrı kolon olur.

## Sektör harmonizasyonu
dim_verticals.csv: raw_name | canonical_name | first_seen_year | comparable_from
Tag isimleri yıllara göre değişiyor, bazıları eski yıllarda yok.
Tek canonical filtre tüm yılları taramalı.

## QA kuralları (qa.py)
- Raporda yazan YoY % ile hesaplanan YoY % uyuşmalı
- Stage toplamları total'ı geçemez
- Deal count'lar integer
- (data_year, report_year, metric, dim_value_canon, scope) unique olmalı
- Aynı data_year'ın farklı vintage'ları arasındaki fark %20'yi geçerse flag

## Yasak
- Okunamayan sayıyı tahmin etme. `confidence: low` yaz ve PROGRESS.md'ye düş.
- Tek geçişe güvenme. Chart slide'larında text layer + vision, uyuşmazsa flag.
- raw/ içine yazma, oradaki dosyaları değiştirme.

## Session akışı
PROGRESS.md oku → sıradaki raporu işle → extracted/ yaz → qa.py → PROGRESS güncelle
