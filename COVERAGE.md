# COVERAGE

Hangi rapor, hangi metriği, hangi data_year'lar için içeriyor.
Sayı yok — sadece kapsam. Kaynak: sayfa başlıkları + tablo/grafik başlıkları.

> **DURUM: BOŞ — hiçbir rapor işlenmedi.**
> `raw/` bu checkout'ta mevcut değil (gitignored, ~80MB, klonla gelmiyor).
> Aşağıdaki tablolar iskelet; PDF'ler olmadan doldurulamaz.
> Kapsamı hatırlayarak/tahmin ederek doldurmak YASAK — bu dosya
> "hangi yıl için hangi rapora bakacağız" kararının tek dayanağı.

## Nasıl doldurulur

Altın kural geçerli: tek seferde TEK rapor. Sırayla `sw_2015` → `2026q2`.
Her rapor için aşağıdaki bloğu doldur, kaydet, sonrakine geç.

Her satır bir (metrik × kırılım) ekseni:

| metric | dim_type | period | data_years | scope | sayfa | not |
|---|---|---|---|---|---|---|

- **metric**     : raporda geçen başlık (ham hâliyle, çevirme)
- **dim_type**   : none (headline) / vertical / stage / city / investor_type / …
- **period**     : FY | Q1 | Q2 | H1
- **data_years** : kapsanan yıl aralığı, kesikliyse aralık değil liste yaz
                   (`2015-2024` vs `2019,2021-2024`)
- **scope**      : all | ex_bigg | ex_getir_bigg | diaspora
- **sayfa**      : slayt/sayfa no — dikişi sonra doğrulamak için şart
- **not**        : kırılım eksikse, tag seti değiştiyse, scope belirsizse yaz

Kapsam yoksa satır AÇMA. "Yok" ile "0" farkı burada da geçerli —
boş satır, metriğin o raporda bulunmadığı anlamına gelir.

## Rapor listesi

Yıllıklar (period=FY), 11 rapor:

| rapor | dosya | durum |
|---|---|---|
| 2015 | `sw_2015.pdf` | bekliyor |
| 2016 | `sw_2016.pdf` | bekliyor |
| 2017 | `sw_2017.pdf` | bekliyor |
| 2018 | `sw_2018.pdf` | bekliyor |
| 2019 | `sw_2019.pdf` | bekliyor |
| 2020 | `sw_2020.pdf` | bekliyor |
| 2021 | `sw_2021.pdf` | bekliyor |
| 2022 | `sw_2022.pdf` | bekliyor |
| 2023 | `sw_2023.pdf` | bekliyor |
| 2024 | `sw_2024.pdf` | bekliyor |
| 2025 | `sw_2025.pdf` | bekliyor |

Çeyreklikler (2026 yıllık rapor YOK), 2 rapor:

| rapor | dosya | durum |
|---|---|---|
| 2026 Q1 | `2026q1.pdf` | bekliyor |
| 2026 Q2 | `2026q2.pdf` | bekliyor |

Çeyreklik raporlar iki period birden taşır: 2026 satırları Q1/Q2/H1,
geriye giden headline serisi period=FY. İkisini ayrı satırlarda yaz.

## Taranacak eksenler (kontrol listesi)

CLAUDE.md'den türetilen beklenen eksenler. Bu bir kapsam iddiası DEĞİL —
her raporda tek tek doğrulanacak kontrol listesi:

- headline (dim_type=none): toplam yatırım, deal count — ~10 yıl geriye
- vertical kırılımı — ~6 yıl, tag setleri yıllara göre değişiyor
- stage kırılımı — ~6 yıl
- CVC / yatırımcı tipi — ~6 yıl
- scope varyantları: ex_bigg, ex_getir_bigg, diaspora — hangi yıllarda ayrı
  raporlanmış, hangilerinde sadece `all` var

## Dikiş kaydı

Bir metriğin tek raporda kapsanmadığı, birden fazla rapordan birleştirilmesi
gereken yerler. Raporlar işlendikçe doldurulur.

| metric | dim_type | hedef aralık | dikilecek raporlar | dikiş noktası | risk |
|---|---|---|---|---|---|

Dikiş noktasında aynı data_year iki raporda da varsa: ikisi de facts.csv'de
kalır (farklı report_year), silme yok. Fark %20'yi geçerse qa.py flag'ler.

---

## Raporlar

<!-- Her rapor işlendikçe buraya bir bölüm eklenir. Format:

### sw_YYYY.pdf  (report_year YYYY, N sayfa)

| metric | dim_type | period | data_years | scope | sayfa | not |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

**Kapsam dışı:** bu raporda beklenip bulunmayan eksenler
**Şüpheli:** okunamayan/çelişkili başlıklar → PROGRESS.md'ye de düşür

-->

_(henüz rapor işlenmedi)_
