# COVERAGE

Hangi rapor, hangi metriği, hangi data_year'lar için içeriyor. SAYI YOK — sadece kapsam.
Kaynak: sayfa/tablo/grafik başlıkları + eksen yıl etiketleri. Üretim: `scripts/render_coverage.py` (elle düzenleme).

Hücre = o raporun o metrik için kapsadığı data_year aralığı. `[Q1]`/`[H1]` period, `[ex_bigg]` gibi etiketler scope. Boş = o raporda o metrik yok (0 DEĞİL).

| metric × dim | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026q1 | 2026q2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Total deal count | 2010-2015 | 2012-2016 | 2010-2017 | 2010-2018 | 2010-2019 | 2010-2020 | 2017-2021 | 2017-2022 | 2010-2023 | 2010-2024 | 2015-2025 | 2016-2025; 2026 [Q1] | 2016-2025; 2026 [H1] |
| Total investment amount | 2010-2015 | 2012-2016 | 2010-2017 |  | 2010-2019 | 2010-2020 | 2017-2021 | 2017-2022 | 2010-2023 | 2010-2024; 2019-2024 [ex_getir_bigg] | 2015-2025 | 2016-2025; 2026 [Q1] | 2016-2025; 2026 [H1] |
| Investment by stage × stage | 2010-2015 | 2012-2016 | 2010-2017 | 2010-2018 | 2010-2019 | 2010-2020 | 2017-2021 | 2017-2022 | 2018-2023 | 2019-2024 | 2020-2025 |  |  |
| VC vs PE × investor_type | 2010-2015 |  | 2010-2017 | 2010-2018 |  |  |  |  |  |  |  |  |  |
| Round size distribution × deal_size | 2015 |  |  |  |  | 2010-2020 | 2017-2021 |  |  |  |  |  |  |
| Monthly activity × month | 2015 |  |  |  |  |  |  |  |  |  |  |  |  |
| Median round size × stage |  | 2012-2016 |  |  |  |  |  |  |  |  |  |  |  |
| Median pre-money valuation × stage |  | 2012-2016 |  |  |  |  |  |  |  |  |  |  |  |
| Investment by vertical × vertical |  | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2018-2023 | 2019-2024 | 2020-2025 | 2020-2025; 2026 [Q1] | 2021-2025; 2026 [H1] |
| Country comparison × country |  | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2022-2024 | 2023-2025 | 2026 [Q1] | 2026 [H1] |
| CVC / corporate investment × investor_type |  |  | 2010-2017 | 2010-2018 | 2010-2019 | 2010-2020 | 2017-2021 | 2017-2022 | 2018-2023 | 2019-2024 | 2020-2025 | 2021-2025; 2026 [Q1] | 2021-2025; 2026 [H1] |
| Turkey vs abroad funding (diaspora) × scope |  |  | 2010-2017 [diaspora] |  | 2010-2019 [diaspora] | 2020 [diaspora] |  |  |  |  | 2015-2025 [diaspora] |  |  |
| Acquisitions & secondary |  |  | 2017 | 2010-2018 | 2010-2019 | 2010-2020 | 2017-2021 | 2017-2022 | 2018-2023 | 2024 | 2020-2025 | 2021-2025; 2026 [Q1] | 2021-2025; 2026 [H1] |
| First-time investors |  |  | 2017 |  |  |  |  |  |  |  |  |  |  |
| Grants / non-equity financing × stage |  |  |  | 2018 | 2019 | 2019-2020 | 2019-2021 |  |  |  |  |  |  |
| VC fundraising (fund formation) |  |  |  | 2012-2018 | 2012-2019 | 2012-2020 | 2017-2021 | 2017-2022 | 2018-2023 | 2019-2024 | 2020-2025 | 2021-2025; 2026 [Q1] | 2021-2025; 2026 [H1] |
| New investors/funds |  |  |  | 2018 | 2019 |  |  |  |  |  |  |  |  |
| New accelerators/hubs |  |  |  | 2018 |  |  |  |  |  |  |  |  |  |
| Funding concentration (top startups) |  |  |  |  | 2019 |  |  | 2022 |  |  | 2024-2025 | 2026 [Q1] | 2026 [H1] |
| Turkish investors' foreign investment |  |  |  |  | 2010-2019 |  |  |  |  |  |  |  |  |
| Investment by legal structure (TR vs abroad) × legal_structure |  |  |  |  |  | 2010-2020 |  |  |  |  |  |  |  |
| Startups founded by vertical × vertical |  |  |  |  |  | 2010-2020 |  | 2017-2022 |  |  |  |  |  |
| Founders' universities (formation) × university |  |  |  |  |  | 2020 |  |  |  |  |  |  |  |
| Investment by university × university |  |  |  |  |  | 2020 |  |  |  |  |  |  |  |
| Investment by city × city |  |  |  |  |  | 2020 | 2021 | 2022 |  |  |  |  |  |
| Gender diversity (founder gender share) × gender |  |  |  |  |  | 2010-2020 | 2021 | 2017-2022 | 2018-2023 | 2019-2024 | 2020-2025 |  |  |
| Female-founder deal activity × gender |  |  |  |  |  | 2010-2020 |  |  |  |  |  |  |  |
| Exits |  |  |  |  |  | 2020 |  |  |  |  |  |  |  |
| Gaming deals (sector) × vertical |  |  |  |  |  |  | 2017-2021 | 2017-2022 | 2018-2023 |  |  |  |  |
| Valuations × stage |  |  |  |  |  |  | 2017,2019,2021 |  |  |  |  |  |  |
| Foreign investor participation × investor_type |  |  |  |  |  |  | 2017-2021 | 2017-2022 | 2018-2023 | 2019-2024 | 2020-2025 |  |  |
| Maturity stage (GE/PE) activity × stage |  |  |  |  |  |  | 2017-2021 | 2017-2022 |  |  |  |  |  |
| Most active investors × investor |  |  |  |  |  |  | 2021 |  |  |  |  |  |  |
| Quarterly deal activity × quarter |  |  |  |  |  |  |  | 2019-2022 | 2019-2023 |  |  | 2024-2026 [Q1] | 2024-2026 [H1] |
| Fintech deals (sector) × vertical |  |  |  |  |  |  |  | 2017-2022 |  |  |  |  |  |
| Equity crowdfunding deals |  |  |  |  |  |  |  | 2017-2022 | 2020-2023 | 2021-2024 | 2021-2025 | 2021-2025; 2026 [Q1] | 2021-2025; 2026 [H1] |
| VCIF/GSYF participation × investor_type |  |  |  |  |  |  |  | 2017-2022 | 2018-2023 | 2019-2024 |  |  |  |
| VC survey (sentiment) × survey |  |  |  |  |  |  |  |  | 2023 | 2024 | 2025 |  |  |
| VC snapshots (fund profiles) × investor |  |  |  |  |  |  |  |  | 2023 |  |  |  |  |
| Global overview (context) |  |  |  |  |  |  |  |  | 2023 |  |  |  |  |
| Startup survey (funded startups) × survey |  |  |  |  |  |  |  |  |  | 2024 |  |  |  |
| Acquisitions & secondary (diaspora) |  |  |  |  |  |  |  |  |  |  | 2020-2025 [diaspora] |  |  |
| Angel investors/networks × investor_type |  |  |  |  |  |  |  |  |  |  |  |  | 2021-2025; 2026 [H1] |

## Provenans (rapor × metrik × sayfa)

| rapor | metric_raw | dim | period | data_years | scope | sayfa | not |
|---|---|---|---|---|---|---|---|
| 2015.pdf | INVESTMENTS BY YEAR (# Rounds) | none | FY | 2010-2015 | all | 5 |  |
| 2015.pdf | INVESTMENTS BY YEAR (Amount Raised) | none | FY | 2010-2015 | all | 5 |  |
| 2015.pdf | INVESTMENTS BY YEAR / INVESTMENT DISTRIBUTION BY ROUND TYPE | stage | FY | 2010-2015 | all | 3,5 | p3 tek yıl 2015 dağılım, p5 yıl×stage |
| 2015.pdf | VENTURE CAPITAL VS PRIVATE EQUITY | investor_type | FY | 2010-2015 | all | 6 | sadece angel+VC sayılıyor; minority/PE ayrı |
| 2015.pdf | NEED FOR MORE SERIES B AND MEGA ROUNDS | deal_size | FY | 2015 | all | 7 | $10K-$100K … $2.5M+ kovaları |
| 2015.pdf | MONTHLY INVESTMENT ACTIVITIES | month | FY | 2015 | all | 4 |  |
| 2016.pdf | 2012-2016 FUNDING ACTIVITIES ($ INVESTED) | none | FY | 2012-2016 | all | 4 |  |
| 2016.pdf | 2012-2016 FUNDING ACTIVITIES (# ROUNDS) | none | FY | 2012-2016 | all | 5 |  |
| 2016.pdf | 2012-2016 FUNDING ACTIVITIES ($ INVESTED / # ROUNDS) | stage | FY | 2012-2016 | all | 4,5 | stage: Pre-Seed…Series D |
| 2016.pdf | MEDIAN ROUND SIZES ($) | stage | FY | 2012-2016 | all | 6 | stage kırılımı |
| 2016.pdf | MEDIAN PRE-MONEY VALUATIONS ($) | stage | FY | 2012-2016 | all | 7 | stage kırılımı |
| 2016.pdf | FUNDING BY VERTICAL (Money Raised / # Rounds) | vertical | FY | 2016 | all | 8 | FLAG: başlık 2012-2016 der, tablo tek-yıl 2016 gibi; doğrula. Vertical'lar mutually exclusive değil |
| 2016.pdf | COMPARISON OF TURKEY WITH OTHER COUNTRIES | country | FY | 2016 | all | 9 | per-capita, GDP oranı; kaynak Crunchbase/TiA |
| 2017.pdf | Early stage investments … (Melek&VC + GE&PE stacked) | none | FY | 2010-2017 | all | 5 | erken aşama odak; segment split var |
| 2017.pdf | # Rounds (line, 11…167) | none | FY | 2010-2017 | all | 5 |  |
| 2017.pdf | In 2017 there are investments in all stages (Seed/Series A/B/C, $) | stage | FY | 2010-2017 | all | 7 | amount; convertible hariç |
| 2017.pdf | Melek&VC vs Growth Equity&PE | investor_type | FY | 2010-2017 | all | 5 | p5 stacked segment |
| 2017.pdf | Corporates are increasingly interested (funding amount + share of corporate investors) | investor_type | FY | 2010-2017 | all | 8 | corporate amount + %share |
| 2017.pdf | Most funded verticals in 2017 (Angel & VC) | vertical | FY | 2017 | all | 9 | vertical mutually exclusive değil |
| 2017.pdf | Startups in Turkey vs Turkish Immigrants' Startups Comparison | scope | FY | 2010-2017 | diaspora | 15 | yurtiçi vs yurtdışı funding + #rounds |
| 2017.pdf | Turkey, Europe and MENA — 2017 Early Investment League | country | FY | 2017 | all | 18-21 | Europe + MENA lig tabloları, per-capita, dev sayısı |
| 2017.pdf | Prominent Acquisitions in 2017 | none | FY | 2017 | all | 12 | liste; asset/majority/minority |
| 2017.pdf | First Time Investors in 2017 | none | FY | 2017 | all | 13 | liste |
| 2018.pdf | Deal Volume by Angel & VC (# Deals) | none | FY | 2010-2018 | all | 4 | count-merkezli rapor |
| 2018.pdf | Deal Volume by Angel&VC vs PE (# Deals) | investor_type | FY | 2010-2018 | all | 4,5 | VC/GE/PE/CR tanımı p5 |
| 2018.pdf | Seed & Series A deals see sharp decline (# Deals by stage) | stage | FY | 2010-2018 | all | 7 | COUNT bazlı (amount değil); Pre-Seed…Series D |
| 2018.pdf | Fintech, SaaS, Marketing-tech biggest bets | vertical | FY | 2018 | all | 8 |  |
| 2018.pdf | Investments w/ Corporate Participation vs Total (Early Stage) | investor_type | FY | 2010-2018 | all | 9 | count bazlı; 1/3 deals corporate |
| 2018.pdf | Grants are the best option for idea stage | stage | FY | 2018 | all | 10 | Tubitak/KOSGEB grant vs Angel&VC; snapshot |
| 2018.pdf | Heatmap + Europe/MENA league + per-capita | country | FY | 2018 | all | 11-15 | Europe 21st, MENA 4th, per-capita |
| 2018.pdf | Acquisitions & Secondary Transaction by Year (Amount + #) | none | FY | 2010-2018 | all | 16,17 | tam zaman serisi; 2018 detay liste p17 |
| 2018.pdf | VC (Local) Fundraising by Year (Capital Raised + # Funds Closed) | none | FY | 2012-2018 | all | 18 | veri 2012'de başlıyor, 2010-11 boş |
| 2018.pdf | New Stakeholders — New Funds / Investors | none | FY | 2018 | all | 19 | liste |
| 2018.pdf | New Stakeholders — New Accelerators / Hubs | none | FY | 2018 | all | 20 | liste |
| 2019.pdf | DISCLOSED EQUITY FUNDING ROUNDS ($) | none | FY | 2010-2019 | all | 4 | amount + #deals line |
| 2019.pdf | DISCLOSED EQUITY FUNDING ROUNDS (# line 11..94) | none | FY | 2010-2019 | all | 4 |  |
| 2019.pdf | INVESTMENTS BY STAGES ($) | stage | FY | 2010-2019 | all | 5 | SEAM: taksonomi Seed/Early VC/Later VC (Pre-Seed…Series D DEĞİL) |
| 2019.pdf | MOST FUNDED STARTUPS/SCALEUPS (top10=72%) | none | FY | 2019 | all | 6 | yoğunlaşma metriği; NEW |
| 2019.pdf | MOST FUNDED VERTICALS (Amount + # Deals) | vertical | FY | 2019 | all | 7 |  |
| 2019.pdf | VC DEALS BY CVC PARTICIPATION ($ + %) | investor_type | FY | 2010-2019 | all | 8,9 | amount p8, share% p9 |
| 2019.pdf | GRANTS VS EQUITY FUNDING (TUBITAK/KOSGEB) | stage | FY | 2019 | all | 10 | 985 startup $8.6M grant vb. |
| 2019.pdf | FUNDING LEAGUE (1/4-4/4) | country | FY | 2019 | all | 11-14 | global $294B; US/China/India/Europe |
| 2019.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS ($, VB vs Bootstrapped) | none | FY | 2010-2019 | all | 15-17 | venture-backed vs bootstrapped split |
| 2019.pdf | VC FUNDRAISING IN TURKEY (New Funds) | none | FY | 2012-2019 | all | 18 | sadece yerel fonlar |
| 2019.pdf | NEW STAKEHOLDERS IN TURKEY | none | FY | 2019 | all | 19 | investor+accelerator |
| 2019.pdf | TURKISH DIASPORA ($ by year) | scope | FY | 2010-2019 | diaspora | 20,21 | diaspora funding serisi; p21 top10=92% |
| 2019.pdf | TURKISH INVESTORS' FOREIGN INVESTMENT PARTICIPATION | none | FY | 2010-2019 | all | 22 | NEW; yurtdışı girişimlere TR yatırımcı katılımı |
| 2020.pdf | TURKEY YEARLY ANGEL & VC DEAL ACTIVITY ($) | none | FY | 2010-2020 | all | 8 | amount + #deals |
| 2020.pdf | TURKEY YEARLY ANGEL & VC DEAL ACTIVITY (# line) | none | FY | 2010-2020 | all | 8 |  |
| 2020.pdf | … BY LEGAL STRUCTURE (in Turkey vs Abroad) | legal_structure | FY | 2010-2020 | all | 9 | NEW dim; overseas entity temasi; amount+# |
| 2020.pdf | TURKEY YEARLY DEAL (#) ACTIVITY BY STAGES | stage | FY | 2010-2020 | all | 10 | COUNT; Seed/Early VC/Later VC |
| 2020.pdf | DEAL (#) ACTIVITY BY SIZE (Under$1M…$25-50M) | deal_size | FY | 2010-2020 | all | 12 | ZAMAN SERISI (2015'te tek yıldı); % by year |
| 2020.pdf | TOP 10 FUNDED VERTICALS IN 2020 | vertical | FY | 2020 | all | 14 | amount+#; tags mutually exclusive değil |
| 2020.pdf | MOST PREFERRED (FOUNDED) VERTICALS BY ENTREPRENEURS | vertical | FY | 2010-2020 | all | 5 | NEW; kurulan startup top5 vertical/yıl |
| 2020.pdf | FOUNDERS' UNIVERSITIES FOR STARTUPS FOUNDED 2020 | university | FY | 2020 | all | 6 | NEW; 2019 ref var |
| 2020.pdf | FOUNDERS' UNIVERSITIES FOR ANGEL & VC DEALS 2020 | university | FY | 2020 | all | 15 | NEW; ITU $55.5M raised |
| 2020.pdf | ANGEL & VC DEALS BY CITIES IN 2020 | city | FY | 2020 | all | 16 | NEW; Istanbul %90 amount |
| 2020.pdf | … DEAL ACTIVITY WITH CVC PARTICIPATION | investor_type | FY | 2010-2020 | all | 18,19 | amount+#; 2020 rekor 37% deals |
| 2020.pdf | SHARE OF STARTUPS BY FOUNDING TEAM GENDER | gender | FY | 2010-2020 | all | 22 | NEW; female-founded share; 2010-2020 median |
| 2020.pdf | … DEAL ACTIVITY WITH FEMALE FOUNDERS/COFOUNDERS | gender | FY | 2010-2020 | all | 23,24 | NEW; deal value+# female-founded |
| 2020.pdf | TURKEY VC FUNDRAISING ACTIVITY (TR vs Abroad + #Funds) | none | FY | 2012-2020 | all | 27 | veri 2012 basliyor; UPDATED; TR/abroad split |
| 2020.pdf | FUNDING LEAGUE 2020 (Global/Europe/MENA + biggest deals) | country | FY | 2020 | all | 30-33 |  |
| 2020.pdf | TOP 10 EXITS IN EUROPE 2020 | none | FY | 2020 | all | 34 | NEW; Peak Games ilk unicorn $1.85B |
| 2020.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS ($) | none | FY | 2010-2020 | all | 36,37 | 2020 detay p38 |
| 2020.pdf | TOP 10 TURKISH DIASPORA DEALS 2020 | scope | FY | 2020 | diaspora | 40 | FLAG: sadece 2020 top10; by-year diaspora serisi YOK (2019'da vardı) |
| 2020.pdf | GRANTS VS EQUITY FUNDING (TUBITAK TEYDEB) | stage | FY | 2019-2020 | all | 42 |  |
| 2021.pdf | TURKIYE YEARLY ANGEL & VC DEAL ACTIVITY (Deal Size $) | none | FY | 2017-2021 | all | 4 | SEAM: ufuk 5 yıla düştü (2020 raporu 2010'a gidiyordu) |
| 2021.pdf | TURKIYE YEARLY ANGEL & VC DEAL ACTIVITY (Deal Count) | none | FY | 2017-2021 | all | 4 |  |
| 2021.pdf | TURKIYE YEARLY DEAL ($/#) ACTIVITY BY STAGES | stage | FY | 2017-2021 | all | 5 | Seed/Early VC/Later VC; $ ve # |
| 2021.pdf | TURKIYE YEARLY DEAL (#) ACTIVITY BY SIZE | deal_size | FY | 2017-2021 | all | 6 | 13 deal >$10M |
| 2021.pdf | TOP 5 FUNDED VERTICALS IN 2021 | vertical | FY | 2021 | all | 9 | Grocery/Game/Proptech/Fintech/Blockchain |
| 2021.pdf | GAMING DEALS IN TURKIYE | vertical | FY | 2017-2021 | all | 10 | NEW; oyun sektörü derinlemesine; $265M |
| 2021.pdf | VALUATIONS (avg seed, gaming vs non-gaming) | stage | FY | 2017,2019,2021 | all | 11 | NEW flavor; spot yıllar; gaming $3.6M non-gaming $2M |
| 2021.pdf | FOREIGN INVESTOR PARTICIPATION | investor_type | FY | 2017-2021 | all | 8 | NEW; 89% amount, 44 deals foreign |
| 2021.pdf | DEALS LEAGUE 2021 (Global/Europe/MENA + per capita) | country | FY | 2021 | all | 12-15 | Europe 10th, MENA 2nd, per-capita 21st |
| 2021.pdf | ANGEL & VC DEALS IN EUROPEAN CITIES 2021 | city | FY | 2021 | all | 16 | Istanbul 13th ($), 4th (#) |
| 2021.pdf | … DEAL ACTIVITY WITH CVC PARTICIPATION | investor_type | FY | 2017-2021 | all | 17 | 87/294 deals corporate |
| 2021.pdf | GENDER DIVERSITY IN 2021 | gender | FY | 2021 | all | 18 | FLAG: 2021 narrative; by-year serisi yok (2020'de 2010-2020 vardı); 5yr ref %16-18 |
| 2021.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS | none | FY | 2017-2021 | all | 19 | ufuk 5 yıl |
| 2021.pdf | TURKIYE YEARLY MATURITY STAGE ACTIVITY | stage | FY | 2017-2021 | all | 20 | NEW; GE/PE deals; Trendyol decacorn $1.85B |
| 2021.pdf | TURKIYE VC FUNDRAISING ACTIVITY (Fund Size + Count) | none | FY | 2017-2021 | all | 21 | sadece TR'ye ayrılan tutar |
| 2021.pdf | MOST ACTIVE VC/CVC FUNDS IN 2021 | investor | FY | 2021 | all | 22 |  |
| 2021.pdf | PRE-SEED STAGE GRANTS BY TUBITAK (BIGG) | stage | FY | 2019-2021 | all | 23 | BIGG; amount+#startups |
| 2022.pdf | TURKIYE YEARLY ANGEL & VC DEAL ACTIVITY (Getir vs Others) | none | FY | 2017-2022 | all | 6 | $1.593B; ex-Getir $825M rekor |
| 2022.pdf | TURKIYE YEARLY ANGEL & VC DEAL ACTIVITY (#) | none | FY | 2017-2022 | all | 6 | 300 deals |
| 2022.pdf | TURKIYE QUARTERLY ANGEL & VC DEAL ACTIVITY | quarter | FY | 2019-2022 | all | 7 | NEW; çeyreklik seri 2019Q1-2022Q4; 2026 çeyreklik raporların öncüsü |
| 2022.pdf | TURKIYE YEARLY DEAL ($/#) ACTIVITY BY STAGES | stage | FY | 2017-2022 | all | 10 | Seed/Early VC/Later VC |
| 2022.pdf | DISTRIBUTION OF DEALS (Getir/DreamGames/Insider/Others) | none | FY | 2022 | all | 8 | top3 $1.144B |
| 2022.pdf | TOP 5 FUNDED VERTICALS IN 2022 | vertical | FY | 2022 | all | 11 | Grocery/Gaming/AI/SaaS/Mktech |
| 2022.pdf | FINTECH IN TURKIYE | vertical | FY | 2017-2022 | all | 12 | NEW sector deep-dive |
| 2022.pdf | GAMING IN TURKIYE (+ country ranking) | vertical | FY | 2017-2022 | all | 13 | TR 4th globally in gaming |
| 2022.pdf | TURKIYE YEARLY EQUITY BASED CROWDFUNDING DEALS | none | FY | 2017-2022 | all | 9 | NEW; 46 startup 2022; avg $230K |
| 2022.pdf | FOREIGN INVESTOR PARTICIPATION | investor_type | FY | 2017-2022 | all | 14 | ~1/5 deals foreign |
| 2022.pdf | … DEAL ACTIVITY WITH CVC PARTICIPATION | investor_type | FY | 2017-2022 | all | 15 | 116/300 rekor |
| 2022.pdf | … WITH VCIF(GSYF) PARTICIPATION + NEW VCIF ESTABLISHED | investor_type | FY | 2017-2022 | all | 16 | NEW; 103/300; onshore micro funds |
| 2022.pdf | FEMALE FOUNDERS IN TURKIYE | gender | FY | 2017-2022 | all | 17 | by-year chart geri geldi; 64/300; deals w/ female $ |
| 2022.pdf | ANGEL & VC DEALS IN EUROPEAN CITIES 2022 | city | FY | 2022 | all | 18 |  |
| 2022.pdf | DEALS LEAGUE 2022 (Global/Europe/MENA) | country | FY | 2022 | all | 5,19,20 |  |
| 2022.pdf | TURKIYE YEARLY MATURITY STAGE ACTIVITY | stage | FY | 2017-2022 | all | 21 | düşük; startuplar Series A sonrası yurtdışına taşınıyor |
| 2022.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS | none | FY | 2017-2022 | all | 22 | Alictus/Airties/ZES/Volt Lines exits |
| 2022.pdf | MOST PREFERRED (FOUNDED) VERTICALS BY ENTREPRENEURS | vertical | FY | 2017-2022 | all | 23 | top5 founded/yıl |
| 2022.pdf | TURKIYE VC FUNDRAISING ACTIVITY | none | FY | 2017-2022 | all | 24 | GSYF/GSYO; bilinmeyen fon boyutu hariç |
| 2023.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE ($) | none | FY | 2010-2023 | all | 11 | HEADLINE 10yr GERİ GELDİ (2021/22 vintage 2017'den başlıyordu). $722M; +convertible/crypto=$889M; ex-Getir $222M |
| 2023.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE (# line) | none | FY | 2010-2023 | all | 11 | 325 deals |
| 2023.pdf | QUARTERLY ANGEL & VC DEALS IN TURKIYE | quarter | FY | 2019-2023 | all | 12 | 2019Q4-2023 |
| 2023.pdf | TURKIYE YEARLY DEAL ($/#) ACTIVITY BY STAGES | stage | FY | 2018-2023 | all | 13 | breakdown 6yr; BiGG Q1-2024 forecast notu |
| 2023.pdf | TOP 10 FUNDED VERTICALS 2023 (Deal Size + Deal Count) | vertical | FY | 2018-2023 | all | 14,15 | AI & Gaming +50% deal |
| 2023.pdf | VC DEAL ACTIVITY WITH VCIF(GSYF) PARTICIPATION + NEW VCIF | investor_type | FY | 2018-2023 | all | 16 | ~1/2 deals GSYF |
| 2023.pdf | EQUITY BASED CROWDFUNDING DEALS | none | FY | 2020-2023 | all | 17 | tech kampanyaları; efonla |
| 2023.pdf | FOREIGN INVESTOR PARTICIPATION | investor_type | FY | 2018-2023 | all | 18 | 5 yılın en düşüğü |
| 2023.pdf | VC DEAL ACTIVITY WITH CVC+CORPORATE PARTICIPATION | investor_type | FY | 2018-2023 | all | 19 | 124/325; 82 total CVC |
| 2023.pdf | GAMING INVESTMENTS (ANGEL & VC) | vertical | FY | 2018-2023 | all | 20 | VINTAGE REVİZYON: Dream Games 2022 dealı 2021'e taşındı |
| 2023.pdf | VC FUNDRAISING | none | FY | 2018-2023 | all | 21 | GSYF hedef tutar; TR payı bilinmiyor |
| 2023.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS | none | FY | 2018-2023 | all | 22 | M&A +67% $644M; Mackolik/ebebek IPO, Martı SPAC |
| 2023.pdf | FEMALE FOUNDERS IN TURKIYE | gender | FY | 2018-2023 | all | 23 | 70/325; gaming %9 en düşük, biotech %47 en yüksek |
| 2023.pdf | DEALS LEAGUE 2023 (Global/Europe/MENA) | country | FY | 2023 | all | 7-9 | TR Europe 5th, MENA 1st (deal count) |
| 2023.pdf | VC SURVEY 2023 (quality/competition/fundraising/exit/problems) | survey | FY | 2023 | all | 24-30 | NEW; 35 TR VC anketi; nitel |
| 2023.pdf | VC SNAPSHOTS | investor | FY | 2023 | all | 31-40 | NEW; fon profilleri |
| 2023.pdf | GLOBAL OVERVIEW (layoffs, gov acts, diversity) | none | FY | 2023 | all | 5,6 | referans; global bağlam |
| 2024.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE ($) | none | FY | 2010-2024 | all | 4 | $1.1B; dönem etiketleri Learning/Early/Restructuring/Experienced |
| 2024.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE (#) | none | FY | 2010-2024 | all | 4 | 469 deals (+31% YoY; BiGG dahil şiştи) |
| 2024.pdf | … (GETIR & BIGG FUND EXCLUDED) | none | FY | 2019-2024 | ex_getir_bigg | 5 | NEW scope=ex_getir_bigg; temiz karşılaştırma |
| 2024.pdf | TURKIYE YEARLY DEAL ($/#) ACTIVITY BY STAGES | stage | FY | 2019-2024 | all | 10 | Seed/Early/Later; p11 ülke-bazlı stage 2024 |
| 2024.pdf | TOP 10 FUNDED VERTICALS 2024 (Size + Count) | vertical | FY | 2019-2024 | all | 12,13 | BiGG etkisi: biotech/healthtech/AI; ex-BiGG AI lider |
| 2024.pdf | VC DEAL ACTIVITY WITH CVC+CORPORATE + NEW CVCS | investor_type | FY | 2019-2024 | all | 14 | 139/358→; 91 CVC (101 w/ accel) |
| 2024.pdf | VC DEAL ACTIVITY WITH VCIF(GSYF) + NEW VCIF | investor_type | FY | 2019-2024 | all | 15 | 455 GSYF authorized rekor |
| 2024.pdf | EQUITY BASED CROWDFUNDING DEALS (# Active Platforms) | none | FY | 2021-2024 | all | 16 | $8M/32 campaign; -61% volume |
| 2024.pdf | FOREIGN INVESTOR PARTICIPATION | investor_type | FY | 2019-2024 | all | 17 | 25/469 |
| 2024.pdf | TURKIYE DEAL ACTIVITY WITH FEMALE FOUNDER | gender | FY | 2019-2024 | all | 18 | 124/469 belirgin artış |
| 2024.pdf | VC FUNDRAISING (Traditional VC Funds) | none | FY | 2019-2024 | all | 19 | fund size+count |
| 2024.pdf | ACQUISITIONS AND SECONDARY TRANSACTIONS | none | FY | 2024 | all | 20 | FLAG: 2024 narrative (by-year chart yok); Kaspi/Hepsiburada $1.127B, IPOlar, 212 dragon exit |
| 2024.pdf | DEALS LEAGUE 2024 + COUNTRY COMPARISON | country | FY | 2022-2024 | all | 6-9,11 | p9 animal analogy 2022-2024; p11 stage cross-country |
| 2024.pdf | STARTUP SURVEY RESULTS | survey | FY | 2024 | all | 21 | NEW; 23 startup; 74 gün bulma, %56 red |
| 2024.pdf | VC SURVEY (quality/competition/fundraising/exit/problems) | survey | FY | 2024 | all | 22-26 | 21 TR VC |
| 2025.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE ($) | none | FY | 2015-2025 | all | 5 | $589M -45% YoY; ufuk 2015 başlıyor (2010 değil) |
| 2025.pdf | YEARLY ANGEL & VC DEALS IN TURKIYE (#) | none | FY | 2015-2025 | all | 5 | 306 deals -48% |
| 2025.pdf | DEALS IN TURKIYE VS DEALS OF TURKISH DIASPORA | scope | FY | 2015-2025 | diaspora | 6 | diaspora serisi GERİ GELDİ; diaspora $1.1B/41 deal, 3 unicorn (Airalo/Periodic/Fal) |
| 2025.pdf | TURKIYE YEARLY DEAL ($) ACTIVITY BY STAGES | stage | FY | 2020-2025 | all | 8,9 | 2025 later-stage SIFIR; p9 cross-country stage |
| 2025.pdf | TOP 10 FUNDED VERTICALS 2025 (Size + Count) | vertical | FY | 2020-2025 | all | 12,13 | AI deal count lider ama capital düşük |
| 2025.pdf | BREAKDOWN OF INVESTMENTS (AI / Gaming+Fintech / top startups) | none | FY | 2024-2025 | all | 10,11 | Gaming+Fintech %68 capital; 1/4 deal AI |
| 2025.pdf | VC DEAL ACTIVITY WITH CVC+CORPORATE + NEW CVCS | investor_type | FY | 2020-2025 | all | 17 | 96 CVC; ~1/3 deals |
| 2025.pdf | VC FUNDRAISING (VCIF + Traditional; median sizes) | none | FY | 2020-2025 | all | 18,19 | son 3 yıl $1.5B; median VCIF $2M, VC $43M |
| 2025.pdf | EQUITY BASED CROWDFUNDING DEALS | none | FY | 2021-2025 | all | 20 | 22 campaign $4.8M; 11 active platform |
| 2025.pdf | FOREIGN INVESTOR PARTICIPATION | investor_type | FY | 2020-2025 | all | 21 | gaming lider |
| 2025.pdf | FEMALE FOUNDERS IN TURKIYE | gender | FY | 2020-2025 | all | 22 | %22 yeni startup; 1/4 investment female |
| 2025.pdf | ACQUISITIONS & SECONDARY TRANSACTIONS IN TURKIYE | none | FY | 2020-2025 | all | 23 | by-year + IPO; $2.4B |
| 2025.pdf | ACQUISITIONS & SECONDARY FOR TURKISH DIASPORA | none | FY | 2020-2025 | diaspora | 24 | NEW; diaspora M&A/IPO/secondary |
| 2025.pdf | DEALS LEAGUE 2025 + COUNTRY COMPARISON | country | FY | 2023-2025 | all | 7,9,14-16 | p7 2023-2025; Europe/MENA leagues |
| 2025.pdf | VC SURVEY 2025 (+ magic wand) | survey | FY | 2025 | all | 26-31 | 16 TR VC; p31 diaspora köprü isteği |
| 2026q1.pdf | YEARLY ANGEL & VC DEALS ($) — historical FY bars | none | FY | 2016-2025 | all | 4 | çeyreklik rapordaki geçmiş FY serisi |
| 2026q1.pdf | YEARLY ANGEL & VC DEALS — Q1 datapoint | none | Q1 | 2026 | all | 4 | $64M/39 rounds; adj TaleMonster+Fimple $40M zayıf çeyrek; ex-BiGG 23 startup |
| 2026q1.pdf | YEARLY ANGEL & VC DEALS (#) — historical FY | none | FY | 2016-2025 | all | 4 |  |
| 2026q1.pdf | YEARLY ANGEL & VC DEALS (#) — Q1 datapoint | none | Q1 | 2026 | all | 4 | 39 rounds |
| 2026q1.pdf | QUARTERLY ANGEL & VC DEALS IN TURKIYE | quarter | Q1 | 2024-2026 | all | 5 | 2024Q1-2026Q1 çeyreklik seri |
| 2026q1.pdf | TOP 10 FUNDED VERTICALS (Size+Count) — historical FY | vertical | FY | 2020-2025 | all | 9,10 |  |
| 2026q1.pdf | TOP 10 FUNDED VERTICALS — Q1 | vertical | Q1 | 2026 | all | 9,10 | gaming+fintech taşıyor |
| 2026q1.pdf | CVC+CORPORATE PARTICIPATION — historical FY | investor_type | FY | 2021-2025 | all | 14 |  |
| 2026q1.pdf | CVC+CORPORATE PARTICIPATION — Q1 | investor_type | Q1 | 2026 | all | 14 |  |
| 2026q1.pdf | VC FUNDRAISING — historical FY | none | FY | 2021-2025 | all | 15 |  |
| 2026q1.pdf | VC FUNDRAISING — Q1 | none | Q1 | 2026 | all | 15 | $42M |
| 2026q1.pdf | EQUITY BASED CROWDFUNDING — historical FY | none | FY | 2021-2025 | all | 16 |  |
| 2026q1.pdf | EQUITY BASED CROWDFUNDING — Q1 | none | Q1 | 2026 | all | 16 | 5 campaign $1.2M; 14 active platform |
| 2026q1.pdf | ACQUISITIONS & SECONDARY IN TURKIYE — historical FY | none | FY | 2021-2025 | all | 17 |  |
| 2026q1.pdf | ACQUISITIONS & SECONDARY — Q1 | none | Q1 | 2026 | all | 17 | $602M |
| 2026q1.pdf | BREAKDOWN OF INVESTMENTS (TaleMonster/Fimple/Dataroid/Vento) | none | Q1 | 2026 | all | 8 |  |
| 2026q1.pdf | DEALS LEAGUE 2026-Q1 + COUNTRY COMPARISON + AI DOMINANCE | country | Q1 | 2026 | all | 6,7,11-13 | p6 çeyreklik 2025Q3-2026Q1; UK top5 AI $3.6B |
| 2026q2.pdf | YEARLY ANGEL & VC DEALS ($) — historical FY | none | FY | 2016-2025 | all | 4 |  |
| 2026q2.pdf | YEARLY ANGEL & VC DEALS — H1 datapoint | none | H1 | 2026 | all | 4 | $172M/87 rounds; rapor H1 diyor (Q2 değil) |
| 2026q2.pdf | YEARLY ANGEL & VC DEALS (#) — historical FY | none | FY | 2016-2025 | all | 4 |  |
| 2026q2.pdf | YEARLY ANGEL & VC DEALS (#) — H1 datapoint | none | H1 | 2026 | all | 4 | 87 rounds |
| 2026q2.pdf | QUARTERLY ANGEL & VC DEALS | quarter | H1 | 2024-2026 | all | 5 | 2024Q2-2026Q2; çeyreklik 2026Q1+2026Q2 ayrı noktalar |
| 2026q2.pdf | TOP 10 FUNDED VERTICALS (Size+Count) — historical FY | vertical | FY | 2021-2025 | all | 6,7 |  |
| 2026q2.pdf | TOP 10 FUNDED VERTICALS — H1 | vertical | H1 | 2026 | all | 6,7 | Gaming %65 volume; AI deal count lider |
| 2026q2.pdf | BREAKDOWN OF INVESTMENTS (6 startup=%75) | none | H1 | 2026 | all | 8 | yüksek yoğunlaşma |
| 2026q2.pdf | CVC+CORPORATES PARTICIPATION — historical FY | investor_type | FY | 2021-2025 | all | 14 | BiGG deals excluded varyantı |
| 2026q2.pdf | CVC+CORPORATES — H1 | investor_type | H1 | 2026 | all | 14 | Future of Mobility Fund tek yeni CVC |
| 2026q2.pdf | VC FUNDRAISING (VCIF + Traditional) — historical FY | none | FY | 2021-2025 | all | 15,16 | traditional VC 2022-2026 dağılımı |
| 2026q2.pdf | VC FUNDRAISING — H1 | none | H1 | 2026 | all | 15,16 | 54 yeni VCIF, 602 aktif; traditional lull; Sanayi Bak. yeni tahsis |
| 2026q2.pdf | EQUITY BASED CROWDFUNDING — historical FY | none | FY | 2021-2025 | all | 17 |  |
| 2026q2.pdf | EQUITY BASED CROWDFUNDING — H1 | none | H1 | 2026 | all | 17 |  |
| 2026q2.pdf | ANGEL INVESTORS AND ANGEL NETWORKS — historical FY | investor_type | FY | 2021-2025 | all | 18 | NEW metrik; lisanslı melek + akredite ağlar |
| 2026q2.pdf | ANGEL NETWORKS PARTICIPATION IN DEALS — H1 | investor_type | H1 | 2026 | all | 18 | % of deal count |
| 2026q2.pdf | ACQUISITIONS & SECONDARY IN TURKIYE — historical FY | none | FY | 2021-2025 | all | 19 |  |
| 2026q2.pdf | ACQUISITIONS & SECONDARY — H1 | none | H1 | 2026 | all | 19 | $1.1B; Uber/GetirYemek, Insider One/Bluecore, Loom Games |
| 2026q2.pdf | DEALS LEAGUE 2026-H1 + COUNTRY COMPARISON + AI DOMINANCE | country | H1 | 2026 | all | 9-13 | p9 çeyreklik 2025Q4-2026Q2; Germany AI $5.6B |


## Sentez (13 rapor tarandıktan sonra)

### 1) Hangi metrik için kaç rapor dikmek gerek (en uzun + en güncel vintage seri)

**Kolay — 1-2 rapor yeter (her yıllık rapor tüm geçmişi yeniden yayınlıyor):**
- **Total investment amount / Total deal count** — 2024 raporu tek başına 2010-2024
  verir; 2025 raporu 2025'i ekler (2015-2025). FY 2010-2025 = **2 rapor (2024 + 2025)**.
  + 2026 için 2026q1/q2 (Q1/H1, ayrı period). İstisna: 2018 raporunda amount serisi YOK
  (sadece deal count) ve 2021/2022 vintage'ı 2017'den başlar → 2010-2016'yı onlardan çekme.
- **Investment by stage** — 2020 raporu 2010-2020, 2025 raporu 2020-2025.
  = **2 rapor (2020 + 2025)**; ama S3 (taksonomi) + S4 (amount vs count) dikişleri var.
- **CVC / corporate** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**.
- **Acquisitions & secondary** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**
  (2024 raporu sadece narrative, by-year chart yok → S10).
- **Gender diversity** — 2020 (2010-2020) + 2025 (2020-2025) = **2 rapor**; 2021 boşluğu.
- **VC fundraising** — 2020 (2012-2020) + 2025 (2020-2025) = **2 rapor**; veri 2012'de başlar.
- **Turkey vs abroad (diaspora)** — 2019 (2010-2019) + 2025 (2015-2025) = **2 rapor**;
  ama 2020-2024 arası çağdaş vintage YOK (S8).

### 2) Dikişler tam olarak nerede (vintage/tanım değişimi)

- **S1 — Ufuk daralması (EN KRİTİK):** 2021 ve 2022 raporları TÜM serileri 2017-başlangıca
  kırpar (5-6 yıl). 2010-2016 yıllarını 2021/2022'den ÇEKME — onlarda yok. Çağdaş kaynak
  2019/2020 raporları, revize kaynak 2023/2024 raporları.
- **S2 — Ufuk geri gelişi ama kısmi:** 2023 headline'ı 2010-2023'e geri açar, 2024 → 2010-2024;
  ama 2025 raporu tekrar 2015-2025'e kırpar (2010-2014 düşer). 2010-2014 için en güncel
  vintage = 2024 raporu.
- **S3 — Stage taksonomisi (2018→2019):** ≤2018 Pre-Seed/Seed/Series A-D; 2019+ Seed/Early VC/
  Later VC. Dikiş için eşleme şart.
- **S4 — Stage ölçü tabanı:** kimi rapor stage'i $ ile (2016,2017,2019,2021,2022,2025), kimi #
  ile (2018,2020) verir. unit'i karıştırma.
- **S5 — 2018 sadece deal count:** total amount-by-year yok.
- **S6 — BiGG dahil edilmesi (2023→2024):** 2024+ TÜBİTAK BiGG pre-seed'i ana veriye katar,
  deal count'u şişirir (2024: 469). Temiz karşılaştırma için scope=ex_getir_bigg (2024 p5).
- **S7 — Açık revizyon:** 2023 raporu Dream Games'in 2022 dealını 2021'e taşıdı → aynı
  data_year farklı vintage'ta farklı değer (CLAUDE.md kısıt #1'in kanıtı).
- **S8 — Diaspora aç/kapa:** seri 2017 & 2019'da var; 2020'de sadece snapshot; 2021-2024 YOK;
  2025'te 2015-2025 olarak geri geldi.
- **S10 — Acquisitions 2024 boşluğu:** 2024 raporu M&A'yı sadece anlatı olarak verir (chart yok);
  2024 by-year değeri için 2025 raporunu (2020-2025) kullan.
- **S11 — 2026 karma period:** 2026q1/q2 raporlarında geçmiş FY barları (2016-2025) ile 2026
  Q1/H1 noktası bir arada. 2026q2 = H1 (Q2 değil). 2026 kısmi değerini FY serisine katma.

### 3) Hiçbir raporda 10 yıllık seri kurulamayacak metrikler

- **Investment by vertical** — 2018 öncesi sadece tek-yıl snapshot (2016,2017,2018,2019);
  gerçek çok-yıl seri ancak 2018'den (2023/2024/2025 raporları). Üstelik tag'ler mutually
  exclusive değil ve isimleri yıllara göre değişiyor → 10 yıllık karşılaştırılabilir seri YOK.
- **Foreign investor participation** — sadece 2017'den itibaren (en fazla 2017-2025 ≈ 9 yıl).
- **Round size distribution** — zaman serisi yalnız 2020 (2010-2020) ve 2021 (2017-2021);
  2022'den sonra tamamen düştü → bugüne uzanmaz (max 2010-2021).
- **Median round size & Median pre-money valuation** — yalnız 2016 raporu (2012-2016);
  tek-rapor metriği, seri kurulamaz. (2021'deki "valuations" farklı, spot yıllar 2017/2019/2021.)
- **Maturity stage (GE/PE)** — yalnız 2021 & 2022 (2017-2022); sonra düştü.
- **Gaming/Fintech sektör derin-dalış** — dağınık (gaming 2021-2023, fintech yalnız 2022).
- **VCIF/GSYF participation** — 2022-2024 (2017-2024); en fazla 8 yıl, 2017'den önce yok.
- **Tek-rapor / geç-başlayan metrikler (seri yok):** Investment by city (2020-2022),
  university (2020), legal structure (2020), Turkish investors' foreign investment (2019),
  exits (2020), startups founded by vertical (2020,2022), most active investors (2021),
  valuations (2021), grants (dağınık 2018-2021), VC/startup survey (2023-2025),
  angel investors/networks (yalnız 2026q2), funding concentration (dağınık).

### Pratik dikiş reçetesi (10+ yıl hedefleyen metrikler için)
Headline & CVC & acquisitions & gender & stage: **2020 raporu (2010-2020) + 2025 raporu
(2020-2025)** ana omurga; 2026'yı yalnız Q1/H1 period'la ekle. 2010-2014'te en güncel
vintage 2024 raporu. Diaspora için 2019 + 2025. Fundraising 2012'den başlar.
