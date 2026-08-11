/**
 * sw-archive → Google Sheets (container-bound Apps Script)
 *
 * BÖLÜM 1  veri sync : GitHub'daki sheets/*.csv → latest/facts/dim_verticals/
 *                      revisions sekmeleri. BU 4 SEKME DIŞINA YAZMAZ.
 * BÖLÜM 2  dashboard : DASHBOARD sekmesini sıfırdan kurar (QUERY + sparkline
 *                      + biçim). YALNIZ DASHBOARD'a yazar.
 * BÖLÜM 3  menü      : onOpen → "sw-archive"
 *
 * Kurulum: SHEETS_SETUP.md
 * Token koda GÖMÜLMEZ; Script Properties'ten okunur.
 */

// ================================================================ ayarlar
var OWNER  = 'yigitmeteozcan';
var REPO   = 'sw-archive';
var BRANCH = 'main';

var TOKEN_PROP = 'GITHUB_TOKEN';
var SYNC_PROP  = 'LAST_SYNC';

/** BÖLÜM 1'in yazabileceği TEK sekme kümesi. */
var SYNC_TABS = {
  'latest':        'sheets/latest.csv',
  'facts':         'sheets/facts.csv',
  'dim_verticals': 'sheets/dim_verticals.csv',
  'revisions':     'sheets/revisions.csv'
};

/** BÖLÜM 2'nin yazabileceği TEK sekme. */
var DASH_TAB = 'DASHBOARD';

/**
 * Sayı olarak yazılacak kolonlar. LİSTE DIŞINDAKİ HER KOLON METİN.
 * Sebep: setValues() değerleri "kullanıcı yazmış gibi" yorumlar — "TRUE"
 * boolean'a, period_label'daki "2019" sayıya döner. period_label'da "2019"
 * sayı, "2026-H1" metin olursa kolon KARMA tipe düşer ve QUERY'nin
 * `pivot C` adımı sessizce yanlış sonuç üretir. Bu yüzden metin kolonlara
 * setValues'tan ÖNCE '@' biçimi uygulanıyor.
 */
var NUMERIC_HEADERS = {
  'data_year': 1, 'report_year': 1, 'value': 1, 'page': 1,
  'from_value': 1, 'to_value': 1, 'delta': 1, 'delta_pct': 1, 'n_vintages': 1
};

var FONT = 'Roboto';
var INK = '#202124', MUTED = '#80868b', RULE = '#e8eaed';
var ACCENT = '#1a73e8', WARN_BG = '#fef7e0', WARN_INK = '#7f6000';

// =============================================================== BÖLÜM 3
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('sw-archive')
    .addItem('Verileri güncelle', 'syncAll')
    .addItem('Dashboard\'u yeniden kur', 'buildDashboard')
    .addSeparator()
    .addItem('Bağlantıyı test et', 'testConnection')
    .addToUi();
}

// =============================================================== BÖLÜM 1
function syncAll() {
  var ui = SpreadsheetApp.getUi();
  var token = getToken_();
  if (!token) {
    ui.alert('Token yok', 'Script Properties içinde ' + TOKEN_PROP +
      ' tanımlı değil.\nSHEETS_SETUP.md adım 3\'e bakın.', ui.ButtonSet.OK);
    return;
  }

  var ss = SpreadsheetApp.getActive();
  ss.toast('CSV\'ler indiriliyor…', 'sw-archive', 10);

  // ÖNCE HEPSİNİ İNDİR, SONRA YAZ. Tek tek indirip yazsaydık ağ hatası
  // yarı yolda sekmeleri boş bırakırdı.
  var loaded = {};
  try {
    for (var tab in SYNC_TABS) loaded[tab] = fetchCsv_(SYNC_TABS[tab], token);
  } catch (e) {
    ui.alert('İndirme başarısız',
      String(e) + '\n\nHiçbir sekme değiştirilmedi.', ui.ButtonSet.OK);
    return;
  }

  var stamp = nowStamp_(ss);
  var lines = [];
  for (var t in loaded) lines.push('  ' + t + ': ' + writeTab_(ss, t, loaded[t], stamp) + ' satır');
  PropertiesService.getScriptProperties().setProperty(SYNC_PROP, stamp);

  ss.toast('Güncellendi', 'sw-archive', 5);
  ui.alert('Veriler güncellendi', stamp + '\n\n' + lines.join('\n') +
    '\n\nDiğer sekmelere dokunulmadı.\nDashboard\'daki tarihi tazelemek için ' +
    '"Dashboard\'u yeniden kur" çalıştırın.', ui.ButtonSet.OK);
}

function testConnection() {
  var ui = SpreadsheetApp.getUi();
  var token = getToken_();
  if (!token) { ui.alert(TOKEN_PROP + ' tanımlı değil. Bkz. SHEETS_SETUP.md'); return; }
  try {
    var rows = fetchCsv_(SYNC_TABS['dim_verticals'], token);
    ui.alert('Bağlantı çalışıyor', 'dim_verticals.csv okundu: ' +
      (rows.length - 1) + ' satır.\nRepo: ' + OWNER + '/' + REPO +
      ' (' + BRANCH + ')', ui.ButtonSet.OK);
  } catch (e) {
    ui.alert('Bağlantı başarısız', String(e), ui.ButtonSet.OK);
  }
}

function getToken_() {
  var t = PropertiesService.getScriptProperties().getProperty(TOKEN_PROP);
  return t ? t.trim() : null;
}

function nowStamp_(ss) {
  return Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(),
                              'yyyy-MM-dd HH:mm');
}

/**
 * Private repo'dan ham dosya okur.
 * raw.githubusercontent.com private repo'da güvenilir biçimde token kabul
 * etmez; Contents API + "Accept: application/vnd.github.raw" belgelenmiş
 * yoldur ve aynı ham içeriği döndürür.
 */
function fetchCsv_(path, token) {
  var url = 'https://api.github.com/repos/' + OWNER + '/' + REPO +
            '/contents/' + path + '?ref=' + encodeURIComponent(BRANCH);
  var res = UrlFetchApp.fetch(url, {
    method: 'get', muteHttpExceptions: true,
    headers: {
      'Authorization': 'Bearer ' + token,
      'Accept': 'application/vnd.github.raw',
      'X-GitHub-Api-Version': '2022-11-28'
    }
  });
  var code = res.getResponseCode();
  if (code === 404) throw new Error(path + ' bulunamadı (404). Dosya push ' +
    'edilmemiş, branch (' + BRANCH + ') yanlış ya da token bu repoyu görmüyor.');
  if (code === 401 || code === 403) throw new Error('Yetki reddedildi (' +
    code + '). Token süresi dolmuş ya da Contents:Read izni yok.');
  if (code !== 200) throw new Error(path + ' için HTTP ' + code + ': ' +
    res.getContentText().slice(0, 200));
  var rows = Utilities.parseCsv(res.getContentText());
  if (!rows || rows.length < 2) throw new Error(path + ' boş.');
  return rows;
}

function writeTab_(ss, name, rows, stamp) {
  if (!SYNC_TABS.hasOwnProperty(name)) throw new Error('İzinsiz sekme: ' + name);
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  var header = rows[0], nCol = header.length, nRow = rows.length;

  sh.clearContents();
  sh.clearNotes();

  // metin kolonlarına ÖNCE '@' biçimi (yorumlanmayı engellemek için)
  for (var c = 0; c < nCol; c++) {
    if (!NUMERIC_HEADERS[header[c]]) {
      sh.getRange(1, c + 1, Math.max(nRow, sh.getMaxRows()), 1)
        .setNumberFormat('@');
    }
  }

  var data = rows.map(function (row) {
    return row.map(function (v, c) {
      if (v === '' || v === null) return '';
      return (NUMERIC_HEADERS[header[c]] && /^-?\d+(\.\d+)?$/.test(v))
        ? Number(v) : v;
    });
  });

  sh.getRange(1, 1, nRow, nCol).setValues(data);
  sh.setFrozenRows(1);
  sh.getRange(1, 1, 1, nCol).setFontWeight('bold');
  sh.getRange(1, 1).setNote('sw-archive · ' + stamp + '\n' + (nRow - 1) +
    ' satır · ' + OWNER + '/' + REPO + '@' + BRANCH);
  return nRow - 1;
}

// =============================================================== BÖLÜM 2
/**
 * latest sekmesi kolonları (sheets/latest.csv'den DOĞRULANDI):
 *   A data_year   B period      C period_label  D is_comparable_fy
 *   E metric      F dim_type    G dim_value_canon  H dim_value_raw
 *   I scope       J unit        K value         L report_id
 *   M report_year N is_provisional  O confidence  P source_file  Q page
 */
var COL = { PERIOD_LABEL: 'C', COMPARABLE: 'D', METRIC: 'E',
            CANON: 'G', SCOPE: 'I', VALUE: 'K' };

var CTRL = { METRIC: 'B3', SCOPE: 'D3', COMPARABLE: 'F3' };
var DATA_ROW = 5;   // QUERY sonucunun başlık satırı

function buildDashboard() {
  var ss = SpreadsheetApp.getActive();
  var src = ss.getSheetByName('latest');
  if (!src || src.getLastRow() < 2) {
    SpreadsheetApp.getUi().alert('latest sekmesi boş',
      'Önce "Verileri güncelle" çalıştırın.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }

  var sh = ss.getSheetByName(DASH_TAB);
  var prev = sh ? readControls_(sh) : null;      // seçimleri koru
  if (!sh) sh = ss.insertSheet(DASH_TAB);
  if (sh.getName() !== DASH_TAB) throw new Error('İzinsiz sekme: ' + sh.getName());

  resetSheet_(sh);

  // --- başlık -----------------------------------------------------------
  var stamp = PropertiesService.getScriptProperties().getProperty(SYNC_PROP) ||
              nowStamp_(ss);
  sh.getRange('A1').setValue('Turkish Startup Ecosystem')
    .setFontSize(18).setFontWeight('bold').setFontColor(INK);
  sh.getRange('A2').setValue('startups.watch · son güncelleme: ' + stamp)
    .setFontSize(9).setFontColor(MUTED);

  // --- kontroller -------------------------------------------------------
  var lists = {
    metric:     uniqueCol_(src, COL.METRIC),
    scope:      uniqueCol_(src, COL.SCOPE),
    comparable: uniqueCol_(src, COL.COMPARABLE)
  };
  sh.getRange('A3').setValue('Metrik');
  sh.getRange('C3').setValue('Kapsam');
  sh.getRange('E3').setValue('Yalnız tam yıl');
  sh.getRange('A3:F3').setFontSize(11).setFontColor(MUTED);
  sh.getRange('A3').setFontColor(MUTED);

  dropdown_(sh, CTRL.METRIC, lists.metric,
            pick_(prev && prev.metric, lists.metric, 'funding_by_vertical_size'));
  dropdown_(sh, CTRL.SCOPE, lists.scope,
            pick_(prev && prev.scope, lists.scope, 'all'));
  dropdown_(sh, CTRL.COMPARABLE, lists.comparable,
            pick_(prev && prev.comparable, lists.comparable, 'TRUE'));
  sh.getRange(CTRL.METRIC + ':' + CTRL.COMPARABLE)
    .setFontSize(11).setFontWeight('bold').setFontColor(ACCENT);

  // --- QUERY ------------------------------------------------------------
  // satır = dim_value_canon (G), kolon = period_label (C), değer = sum(value) (K)
  var f = '=IFERROR(QUERY(latest!$A$2:$Q,' +
          '"select ' + COL.CANON + ', sum(' + COL.VALUE + ') where ' +
          COL.METRIC + " = '\"&$" + CTRL.METRIC.charAt(0) + '$3&"\' and ' +
          COL.SCOPE + " = '\"&$" + CTRL.SCOPE.charAt(0) + '$3&"\' and ' +
          COL.COMPARABLE + " = '\"&$" + CTRL.COMPARABLE.charAt(0) + '$3&"\' ' +
          'group by ' + COL.CANON + ' pivot ' + COL.PERIOD_LABEL + '",0),' +
          '"Seçime uyan veri yok")';
  sh.getRange(DATA_ROW, 1).setFormula(f);
  SpreadsheetApp.flush();

  // --- QUERY çıktısının boyutunu ölç ------------------------------------
  var span = spanOf_(sh, DATA_ROW);
  if (span.cols < 2 || span.rows < 1) {
    sh.getRange(DATA_ROW, 1).setFontSize(11).setFontColor(MUTED);
    finish_(sh, span.cols || 1);
    return;
  }
  var firstData = DATA_ROW + 1, lastData = DATA_ROW + span.rows;

  // --- başlıklar / hizalama ---------------------------------------------
  // Headline metriklerde dim_value_canon boştur → tek satırlık toplam serisi.
  var chosen = String(sh.getRange(CTRL.METRIC).getValue());
  sh.getRange(DATA_ROW, 1).setValue(
    chosen.indexOf('by_vertical') >= 0 ? 'Vertical' : 'Toplam (kırılımsız)');
  sh.getRange(DATA_ROW, 1, 1, span.cols)
    .setFontWeight('bold').setFontColor(INK)
    .setBorder(null, null, true, null, null, null, RULE,
               SpreadsheetApp.BorderStyle.SOLID);
  sh.getRange(DATA_ROW, 2, 1, span.cols - 1).setHorizontalAlignment('right');
  sh.getRange(DATA_ROW, 1, span.rows + 1, span.cols).setFontSize(10);

  // Sayı biçimi hem $ hem adet metriğini kendiliğinden karşılar:
  // >=1M -> $191.8M ; >=1K -> $600K ; altı -> düz tam sayı (deal count).
  sh.getRange(firstData, 2, span.rows, span.cols - 1)
    .setNumberFormat('[>=1000000]$#,##0.0,,"M";[>=1000]$#,##0,"K";#,##0');

  // --- renk ölçeği ------------------------------------------------------
  var valueRange = sh.getRange(firstData, 2, span.rows, span.cols - 1);
  sh.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule()
      .setGradientMinpoint('#ffffff')
      .setGradientMaxpoint('#c6dafc')
      .setRanges([valueRange])
      .build()
  ]);

  // --- sparkline (veri bloğunun sağında, bir kolon boşluk bırakarak) ----
  var sparkCol = span.cols + 2;
  var lastLetter = colLetter_(span.cols);
  sh.getRange(DATA_ROW, sparkCol).setValue('Trend')
    .setFontWeight('bold').setFontColor(INK).setFontSize(10);
  var sparks = [];
  for (var r = firstData; r <= lastData; r++) {
    sparks.push(['=IFERROR(SPARKLINE(B' + r + ':' + lastLetter + r +
      ',{"charttype","line";"linewidth",2;"color","' + ACCENT +
      '";"empty","ignore"}),"")']);
  }
  sh.getRange(firstData, sparkCol, sparks.length, 1).setFormulas(sparks);

  // --- uyarı kutusu -----------------------------------------------------
  var wRow = lastData + 2;
  var wWidth = Math.max(span.cols, 4);
  sh.getRange(wRow, 1, 1, wWidth).merge()
    .setValue('⚠  Son data_year provisional — sonraki vintage\'da %25\'e kadar ' +
              'artabilir (2024: 469→588, 2025: 306→388). Kısmi dönemler ' +
              '(2026-Q1, 2026-H1) tamamlanmış yıl değildir; ' +
              '"Yalnız tam yıl = TRUE" ile elenir.')
    .setBackground(WARN_BG).setFontColor(WARN_INK).setFontSize(10)
    .setWrap(true).setVerticalAlignment('middle');
  sh.setRowHeight(wRow, 44);

  finish_(sh, sparkCol);
  SpreadsheetApp.getActive().toast('Dashboard kuruldu', 'sw-archive', 5);
}

// --------------------------------------------------------------- yardım
function resetSheet_(sh) {
  sh.clear();
  sh.clearNotes();
  sh.setConditionalFormatRules([]);
  sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns()).clearDataValidations();
  var merges = sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns()).getMergedRanges();
  for (var i = 0; i < merges.length; i++) merges[i].breakApart();
  sh.setFrozenRows(0);
  sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns())
    .setFontFamily(FONT).setFontColor(INK).setBackground(null);
}

function finish_(sh, lastCol) {
  sh.setHiddenGridlines(true);
  sh.setFrozenRows(DATA_ROW);
  sh.setColumnWidth(1, 210);                       // vertical adları geniş
  for (var c = 2; c <= lastCol; c++) sh.autoResizeColumn(c);
  for (var c2 = 2; c2 <= lastCol; c2++) {
    if (sh.getColumnWidth(c2) < 78) sh.setColumnWidth(c2, 78);
  }
  sh.setRowHeight(2, 18);
  sh.setRowHeight(4, 10);                          // beyaz alan
}

function readControls_(sh) {
  return {
    metric:     sh.getRange(CTRL.METRIC).getValue(),
    scope:      sh.getRange(CTRL.SCOPE).getValue(),
    comparable: sh.getRange(CTRL.COMPARABLE).getValue()
  };
}

function pick_(prev, list, fallback) {
  if (prev && list.indexOf(prev) >= 0) return prev;
  if (list.indexOf(fallback) >= 0) return fallback;
  return list[0];
}

function dropdown_(sh, a1, list, value) {
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(list, true).setAllowInvalid(false).build();
  sh.getRange(a1).setDataValidation(rule).setValue(value);
}

function uniqueCol_(src, letter) {
  var idx = letter.charCodeAt(0) - 65;
  var vals = src.getRange(2, idx + 1, src.getLastRow() - 1, 1).getValues();
  var seen = {}, out = [];
  for (var i = 0; i < vals.length; i++) {
    var v = vals[i][0];
    if (v === '' || v === null) continue;
    v = String(v);
    if (!seen[v]) { seen[v] = 1; out.push(v); }
  }
  out.sort();
  return out;
}

/** DATA_ROW'dan başlayan QUERY bloğunun boyutu (başlık satırı hariç satır sayısı). */
function spanOf_(sh, headerRow) {
  var maxC = sh.getMaxColumns(), maxR = sh.getMaxRows();
  var head = sh.getRange(headerRow, 1, 1, maxC).getValues()[0];
  var cols = 0;
  for (var c = 0; c < maxC; c++) if (head[c] !== '' && head[c] !== null) cols = c + 1;
  if (cols === 0) return { cols: 0, rows: 0 };
  // Satır sayısı TÜM blok taranarak bulunur, yalnız 1. kolona bakılarak
  // değil: headline metriklerde dim_value_canon boştur ve tek veri satırının
  // 1. hücresi boş gelir — kolon taraması onu "veri yok" sanardı.
  var body = sh.getRange(headerRow + 1, 1, maxR - headerRow, cols).getValues();
  var rows = 0;
  for (var r = 0; r < body.length; r++) {
    var empty = true;
    for (var c2 = 0; c2 < cols; c2++) {
      if (body[r][c2] !== '' && body[r][c2] !== null) { empty = false; break; }
    }
    if (empty) break;
    rows = r + 1;
  }
  return { cols: cols, rows: rows };
}

function colLetter_(n) {
  var s = '';
  while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = (n - m - 1) / 26; }
  return s;
}
