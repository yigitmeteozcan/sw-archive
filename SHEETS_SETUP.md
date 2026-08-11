# SHEETS_SETUP

`scripts/sw_dashboard.gs` kurulumu — tek dosya, iki iş yapar:

1. **Veri sync** — GitHub'daki `sheets/*.csv` dosyalarını çekip `latest`,
   `facts`, `dim_verticals`, `revisions` sekmelerini doldurur.
2. **Dashboard** — `DASHBOARD` sekmesini sıfırdan kurar (QUERY pivot,
   dropdown'lar, sparkline, biçimlendirme).

**Script yalnız bu 5 sekmeye yazar.** Sync adımı 4 veri sekmesinin dışına,
dashboard adımı `DASHBOARD` dışına asla yazmaz — COMPARE, pivot, grafik
sekmeleriniz güvende.

---

## 1. GitHub token al

Repo private olduğu için token şart.

1. GitHub → sağ üst avatar → **Settings**
2. Sol menünün en altı → **Developer settings**
3. **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
4. Doldur:
   - **Token name:** `sheets-sync` (serbest)
   - **Expiration:** 90 gün ya da tercihin
   - **Repository access:** *Only select repositories* → **`sw-archive`**
   - **Permissions** → *Repository permissions* → **Contents** → **Read-only**
     (başka izin gerekmiyor)
5. **Generate token** → çıkan `github_pat_…` değerini kopyala

> Token bir daha gösterilmez. Şimdi kopyalamazsan yenisini üretmen gerekir.
> Token'ı hiçbir dosyaya, koda veya hücreye yapıştırma.

---

## 2. Script'i sheet'e yapıştır

1. Hedef Google Sheets dosyanı aç
2. Menü → **Uzantılar** (Extensions) → **Apps Script**
3. Açılan editörde soldaki `Kod.gs` / `Code.gs` dosyasının **içindeki her şeyi
   sil**
4. Bu repodaki `scripts/sw_dashboard.gs` dosyasının **tamamını** kopyala,
   editöre yapıştır
5. Üstteki disket ikonu → **Kaydet**

Apps Script'i sheet'in kendi menüsünden açtığın için script dosyaya bağlı
(container-bound) olur; `SpreadsheetApp.getActive()` doğrudan bu dosyayı
görür. Ayrı bir Apps Script projesi açma.

### Repo bilgileri

Dosyanın başındaki üç satır:

```js
var OWNER  = 'yigitmeteozcan';
var REPO   = 'sw-archive';
var BRANCH = 'main';
```

Repo adını/sahibini değiştirdiysen burayı güncelle. Bunlar gizli değil,
kodda durabilir — **token duramaz**.

---

## 3. Token'ı Script Properties'e gir

1. Apps Script editöründe sol menü → **Proje ayarları** (⚙ Project Settings)
2. En alta in → **Script Properties** (Komut Dosyası Özellikleri)
3. **Add script property** / **Özellik ekle**
4. Doldur:
   - **Property:** `GITHUB_TOKEN`
   - **Value:** 1. adımda kopyaladığın `github_pat_…` değeri
5. **Save script properties**

Token artık projeye bağlı, koda gömülü değil. Kodu paylaşsan token gitmez.

---

## 4. Yetki ver

1. Google Sheets sekmesine dön, sayfayı **yenile** (F5)
2. Menüde **sw-archive** görünecek (birkaç saniye sürebilir)
3. **sw-archive → Bağlantıyı test et**
4. İlk çalıştırmada Google izin isteyecek:
   - *Yetkilendirme gerekiyor* → **İzinleri incele**
   - Hesabını seç
   - "Google bu uygulamayı doğrulamadı" uyarısı çıkarsa →
     **Gelişmiş** → **… (güvenli olmayan) sayfasına git**
     (uygulama sensin, kendi script'in)
   - **İzin ver**
5. Başarılıysa `dim_verticals.csv okundu: 61 satır.` kutusu gelir

---

## 5. Çalıştır — sırası önemli

**Önce veri, sonra dashboard.** Dashboard `latest` sekmesinden beslenir;
o boşken kurulamaz.

### 5a. sw-archive → **Verileri güncelle**

Bittiğinde satır sayıları çıkar:

```
latest: 370 satır
facts: 760 satır
dim_verticals: 61 satır
revisions: 185 satır
```

Her veri sekmesinin **A1 hücresinde not** var (küçük siyah üçgen): son
güncelleme zamanı, satır sayısı, branch.

### 5b. sw-archive → **Dashboard'u yeniden kur**

`DASHBOARD` sekmesi kurulur:

| yer | içerik |
|---|---|
| Satır 1 | `Turkish Startup Ecosystem` (18pt bold) |
| Satır 2 | `startups.watch · son güncelleme: …` (küçük gri) |
| Satır 3 | 3 dropdown: **Metrik** (B3), **Kapsam** (D3), **Yalnız tam yıl** (F3) |
| Satır 5 | QUERY başlığı — dönem etiketleri |
| Satır 6+ | veri: satır = vertical, kolon = dönem, değer = toplam |
| sağda | her satır için **Trend** sparkline'ı |
| altta | provisional uyarı kutusu |

Dropdown'ları değiştirdiğinde tablo **anında** güncellenir; script'i tekrar
çalıştırman gerekmez.

---

## Dashboard hakkında bilmen gerekenler

**Dropdown listeleri veriden türetilir.** Yeni bir metrik ya da scope
eklendiğinde "Dashboard'u yeniden kur" çalıştır; listeler tazelenir. Mevcut
seçimlerin korunur.

**Sayı biçimi tek formülle iki metriği de karşılar:**
`[>=1000000]$#,##0.0,,"M";[>=1000]$#,##0,"K";#,##0`
— 191.800.000 → `$191.8M`, 600.000 → `$600K`, 47 → `47`. Yani $ metriğinden
adet metriğine geçtiğinde biçimi elle değiştirmen gerekmez.

**Headline metrik seçersen** (`total_deal_size`, `total_deal_count`) kırılım
olmadığı için tek satır gelir ve satır etiketi boştur — ilk kolon başlığı
otomatik `Toplam (kırılımsız)` olur. Vertical metriklerinde başlık `Vertical`.

**Tarih satır 2'de sync anını gösterir**, dashboard kurulum anını değil.
Sync ile dashboard arası bir fark olursa "Dashboard'u yeniden kur" ile tazele.
(Sync, kural gereği DASHBOARD'a yazamadığı için tarihi kendi güncelleyemiyor.)

**Üç şeye dikkat:**

- **Yalnız tam yıl = TRUE** bırak. FALSE yaparsan kısmi dönemler
  (`2026-Q1`, `2026-H1`) tabloya girer ve tamamlanmış yıl gibi görünür.
- Kolon başlığı `period_label`'dır, `data_year` değil. `2026-Q1` ile
  `2026-H1` ayrı kolonlarda durur — **toplama**, ikisi çakışan dönemler.
- Alttaki uyarı kutusu boşuna değil: son yıl provisional. 2024 deal count
  469 iken sonraki vintage'da 588 oldu.

---

## Veriyi yeniden üretmek

Sheets GitHub'daki `sheets/` klasörünü okur. Yeni rapor işledikten sonra:

```bash
.venv/bin/python scripts/extract_facts.py <report_id> --write
.venv/bin/python scripts/qa.py            # 0 hata görmeden devam etme
.venv/bin/python scripts/build_sheets.py
git add -A && git commit -m "…" && git push
```

Sonra Sheets'te **Verileri güncelle**. Push edilmemiş değişiklik yansımaz.

---

## Sorun giderme

| Mesaj / belirti | Sebep ve çözüm |
|---|---|
| Menüde **sw-archive** yok | Sayfayı yenile. Hâlâ yoksa Apps Script'te kod kaydedilmemiş. |
| `Token yok` | Adım 3 atlanmış. Property adı tam olarak `GITHUB_TOKEN` olmalı. |
| `Yetki reddedildi (401/403)` | Token süresi dolmuş ya da `sw-archive` erişimi / **Contents: Read** izni verilmemiş. Yeni token üret, Script Properties'teki değeri güncelle — kod aynı kalır. |
| `bulunamadı (404)` | Dosya push edilmemiş ya da `BRANCH` yanlış. GitHub'da `sheets/` klasörü görünüyor mu bak. |
| `İndirme başarısız` | Ağ/GitHub hatası. **Hiçbir sekme değişmedi** — script 4 dosyayı da indirmeden yazmaya başlamaz. Tekrar dene. |
| `latest sekmesi boş` | Dashboard'dan önce "Verileri güncelle" çalıştır. |
| Tabloda `Seçime uyan veri yok` | Dropdown kombinasyonunda kayıt yok (ör. `total_deal_size` + `ex_getir_bigg` + kısmi dönem). Başka kombinasyon seç. |
| Sparkline'lar boş | O satırın serisinde tek nokta var; SPARKLINE en az iki nokta ister. |
