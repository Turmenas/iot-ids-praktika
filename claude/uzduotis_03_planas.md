# 3 UŽDUOTIS — DI metodų parinkimas ir pagrindimas

**Tikslų planas**
**Sudaryta:** 2026 m. rugsėjo 3 d., 12:35
**Vykdymas:** rugsėjo 3 d. (pradiniame plane — rugs. 8 d.; grafikas eina 5 dienomis į priekį)
**Rezultatas:** `ataskaita/skyriai/03_parinkimas.tex` (~3,5–4 psl.), užrakintas eksperimento protokolas, +2 įrašai `ataskaita/saltiniai.bib`

---

## 0. Būklė prieš pradedant — ką 2 užduotis jau atidavė 3-iajai

Ši užduotis yra neįprastoje padėtyje: **didžioji dalis jos turinio jau sugeneruota vakar.** Tai reikia pasakyti sau atvirai prieš pradedant, nes kitaip diena praeis perrašinėjant tai, kas jau parašyta.

| Ko 3 užduočiai reikėjo | Būklė | Kur guli |
|---|---|---|
| Kandidatų aibė | ✅ **6 kandidatai iš 17 apžvelgtų** | `metodu_apzvalga.md` 7 sk. |
| Ketvertas | ✅ **RF, XGBoost, MLP, autokoderis** — fiksuota T7 | `02_di_metodai.tex` 2.8 |
| Atmetimo priežastys | ✅ **8 atmesti, kiekvienas su tipu** (resursai / delsa / prielaida / duomenų struktūra) | `metodu_apzvalga.md` 7 sk. |
| Atrankos kriterijai | ✅ **Išvesti iš IoT savybių**, ne pasirinkti | 1 užd. `tab:reikalavimai` |
| Kriterijų svoriai | ❌ **Nepagrįsti** — plane duoti skaičiai (30/25/20/15/10 %), bet be argumento | — |
| Užduoties detalumas | ✅ **8 kategorijos** (~20 paleidimų vietoj ~70) | `02_di_metodai.tex` 2.8 |
| Metrikos pasirinkimas | ✅ macro-F1 + PR-AUC; accuracy netinka (41,8:1 ir 5 764:1) | Žurnalas, rugs. 2 d. |
| Realistinis taikinys | ✅ macro-F1 **0,85–0,90**, ne 0,99 | `almahaqeri2026gradient` |
| Delsos biudžetas | ✅ 20–50 ms šliuzui; XGBoost telpa 5 669×, gilieji viršija 2,4–9× | `02_di_metodai.tex` 2.6 |
| Imties riba | ✅ **100 000 eilučių klasei** → 2 429 978 eilutės, disbalansas 84:1 | `uzduotis_02_planas.md` 12 sk. |
| Skaidymo sprendimas | ❌ **Neužrakintas** — nėra `ts`, chronologinis neįmanomas | ⚠️ **šios dienos darbas** |
| Eksperimento protokolas | ❌ **Neužrakintas** | ⚠️ **šios dienos darbas** |
| Nematytos klasės testas | 🟡 Nuspręsta perkelti į privalomą 5 užd. dalį, bet klasės neparinktos | ⚠️ **šios dienos darbas** |

> **Iš to seka dienos svorio centras.** Metodų atranka yra **užrašymo**, o ne sprendimo darbas. Realus, dar nepriimtų sprendimų darbas yra **eksperimento protokolas** — jis vienintelis blokuoja 4 užduotį ir jo neužrakinus rugsėjo 9 d. duomenų paruošimas prasidės nuo spėliojimo.

---

## 1. Pagrindinė šios užduoties problema — ir kaip ji sprendžiama ⭐

Ketvertas fiksuotas vakar. Jei šiandien parašysiu svertinę matricą, kuri „atveda“ būtent prie tų keturių, tai bus **jau priimto sprendimo pagražinimas.** Recenzentui tai matosi iš karto: matrica, kurios rezultatas sutampa su prieš tai paskelbtu atsakymu, o svoriai parinkti be pagrindimo, yra retorinė priemonė, ne metodas.

**Sprendimas: atranka skaidoma į dvi pakopas su skirtinga logika.**

### 1 pakopa — kietieji apribojimai (be svorių, be balų)

Keturi dvejetainiai vartai. Metodas arba tinka, arba ne; kompromiso nėra, todėl svorių čia nereikia.

| Vartai | Turinys | Kilmė |
|---|---|---|
| **K1** | Duomenų struktūra leidžia metodą taikyti | Rugs. 2 d. patikra: nėra `ts`, nėra eilės, nėra mazgų ID |
| **K2** | Modelio prielaidos nepažeistos duomenimis | Rugs. 2 d. patikra: tikslios funkcinės priklausomybės |
| **K3** | Mokymas telpa į ≤ 30 min. be GPU prie 2,43 mln. × 36 | `uzduotis_02_planas.md` 12 sk. |
| **K4** | Inferencija telpa į 20–50 ms šliuzo biudžetą | `sallam2026gap` per 1 užd. `tab:reikalavimai` |

**17 → 9.** Aštuoni atmetami čia, ir **nė vienas atmetimas nepriklauso nuo svorio.** Tai svarbiausias šio skyriaus argumentas: didžiąją atrankos dalį atlieka duomenys ir diegimo vieta, ne mano prioritetai.

### 2 pakopa — svertiniai balai tik likusiems devyniems

Devyni likę: sprendimų medis · Random Forest · XGBoost · LightGBM · Isolation Forest · autokoderis · MLP · 1D-CNN · *(klasterizavimas ir savimoka — už darbo ribų, ne atmesti)*.

Tik čia atsiranda kriterijai, svoriai ir balai. Ir tik čia yra subjektyvumo — **vieninteliame darbo taške, kur jis yra**, todėl jį reikia pažymėti, o ne užglaistyti.

### 3 pakopa — aibės pilnumo taisyklė ⭐

Vien iš balų rikiuotės ketvertas **neišeitų**, ir tai reikia parašyti atvirai, o ne slėpti:

- **Autokoderis** balais pralaimi ansambliams beveik pagal visus kriterijus. Jis aibėje yra ne dėl balo, o dėl to, kad **reikalavimas aptikti nematytas atakas yra funkcinis, ne sveriamas.** Nė vienas prižiūrimas metodas jo neįvykdo jokiu svorių deriniu.
- **MLP** irgi nėra rikiuotės viršūnėje. Jis aibėje todėl, kad 2.4 poskyris iškelia klausimą (ar gilaus mokymosi sudėtingumas apsimoka lentelinei įvesčiai), o be MLP tas klausimas liktų neatsakytas eksperimentu.

**Taisyklė, kuri tai formalizuoja:** galutinė aibė = *rikiuotės viršūnė* + *paradigmų padengimas* (prižiūrimas ir neprižiūrimas) + *sudėtingumo gradientas* (ansamblis → stiprinimas → neuroninis tinklas). Trys sudedamosios, kiekviena su savo pagrindu.

> **Kodėl taip geriau.** Matrica, kuri sąžiningai parodo, kad autokoderis pralaimi balais, bet vis tiek įtraukiamas dėl kitos priežasties, yra **stipresnė** už matricą, kurioje balai stebuklingai sutampa su atsakymu. Pirmoji parodo, kad kriterijai nebuvo derinami prie norimo rezultato.

---

## 2. Konkretūs tikslai

| Nr. | Tikslas | Išmatuojamas rezultatas | Prior. |
|---|---|---|---|
| **T0** | Uždaryti 2 užduoties likučius — **trys skirtingos būklės, žr. žemiau** | `tab:atakos` pataisyta; kodas patikrintas paleidus; smulkmenų būklė sutikrinta | **P0** |
| **T1** | Perkelti `tab:reikalavimai` iš 1 sk. į 3 sk. | 1 sk. susitraukia ~1 psl.; visos `\ref` nuorodos veikia; 0 klaidų | **P0** |
| **T2** | Formalizuoti kietųjų apribojimų filtrą | `tab:filtras`: 17 eilučių × 4 vartai; 17 → 9; kiekvienas ✗ su priežastimi | **P0** |
| **T3** | Pagrįsti kriterijų svorius | 5 svoriai, kiekvienas su nuoroda į konkrečią `tab:reikalavimai` eilutę | **P0** |
| **T4** | Sudaryti sprendimų matricą | `tab:matrica`: 9 metodai × 5 kriterijai; balų skalė apibrėžta **prieš** balų rašymą | **P0** |
| **T5** | Jautrumo analizė | Svoriai keičiami ±10 p. p. → ar keičiasi ketvertas; rezultatas įrašytas nepriklausomai nuo to, koks jis | **P0** |
| **T6** | **Užrakinti eksperimento protokolą** | 14 punktų (5 sk.), kiekvienas su konkrečia reikšme, ne su „reikės nuspręsti“ | **P0** ⭐ |
| **T7** | Parašyti `03_parinkimas.tex` | ~3,5–4 psl., 3 lentelės, kompiliuojasi be klaidų | **P0** |
| **T8** | Papildyti šaltinius | 18 → 20 įrašų (SMOTE, statistinis palyginimas), DOI patikrinti, anotacijos parašytos | P1 |

**Ne šios užduoties tikslai:** joks kodas modeliams, joks duomenų įkėlimas, jokia požymių inžinerija (→ 4 užd.). **Vienintelė leistina išimtis** — 20 eilučių jautrumo skaičiavimo skriptas, nes be jo T5 yra nuomonė.

### T0 detaliau — trys punktai, ne vienas

| Punktas | Būklė dokumentuose | Ką daryti |
|---|---|---|
| **`tab:atakos` eilutės**, mininčios `flow_duration` / srauto asimetriją | ❌ **Neatlikta.** Nėra jokio įrašo nei žurnale, nei `STRUKTURA.md` | **Tikras darbas.** Vienintelė vieta, kur 1 skyrius tebeprieštarauja realiems duomenims |
| **`ikelimas.py` / `etiketes.py`** (`Label`, `.upper()`, `BENIGN`) | ✅ **Greičiausiai atlikta 09-02** — `STRUKTURA.md` abu pažymėti su data | **Tik patikra:** `python -m src.duomenys.etiketes`. Jei `assert` praeina — punktas uždarytas |
| **Smulkmenos** | ⚠️ **Dokumentai prieštarauja** — žr. žemiau | Sutikrinti su realiu aplanku, ne su užrašais |

⚠️ **`requirements-lock.txt`: du dokumentai sako skirtingai.** `STRUKTURA.md` (sudaryta 09-02 **iš realaus aplanko turinio**) jį žymi ✅; žurnalo rugs. 1 d. „Nebaigta“ ir `uzduotis_02_planas.md` 11 sk. tebelaiko jį neatliktu. Tikėtina, kad failas yra, o žymos liko neatnaujintos — bet **tai tikrinama `dir`, ne spėjimu.** Ta pati rugsėjo 2 d. pamoka: užrašas, sudarytas neatidarius failo, yra hipotezė.

**Kiti smulkūs:** titulinis puslapis — neatlikta · `houichi` metrikos — užblokuota (Wiley 403) · `literatura_anotacijos.md` dublikatas — tebeguli.

---

## 3. Skyriaus `03_parinkimas.tex` struktūra

```
3. DI metodų parinkimas ir pagrindimas
   3.1. Atrankos rėmas: du filtrai, ne vienas               (~0,4 psl.)
        - kodėl kietieji apribojimai atskiriami nuo sveriamų kriterijų
        - kur šiame darbe yra subjektyvumas ir kur jo nėra
   3.2. Kietieji apribojimai                                (~0,7 psl.)
        --> tab:filtras (17 metodų x K1-K4)
        - 8 atmetimai, iš kurių tik 2 dėl resursų
   3.3. Vertinimo kriterijai ir jų svoriai                  (~0,8 psl.)
        --> tab:reikalavimai (PERKELTA iš 1 skyriaus)
        - kiekvienas svoris <- konkreti tab:reikalavimai eilute
   3.4. Sprendimų matrica                                   (~0,7 psl.)
        --> tab:matrica (9 metodai x 5 kriterijai)
        - balu skale apibrezta pries balus
   3.5. Jautrumo analizė ir aibės pilnumo taisyklė          (~0,5 psl.)
        - +-10 p. p. rezultatas
        - kodel autokoderis aibeje, nors balais pralaimi
   3.6. Eksperimento protokolas                             (~0,8 psl.)
        - tekstas + kompaktiskas sarasas, NE ketvirta lentele
   3.7. Apibendrinimas                                      (~0,2 psl.)
```

**Iš viso ~4,1 psl.** Taikinys plane buvo 3–4.

> **Apimties stabdis — bet dabar jis matuoja laiką, ne puslapius.** Formalių reikalavimų nėra (žr. 12 sk.), todėl 4 psl. taikinys nėra atskaitomybė — jis yra **valandos, kurių neatiduodu 4–6 užduotims.** 1 skyrius davė 9 psl. vietoj 4–5, 2 skyrius 9,7 vietoj 5–6; trečias kartas iš eilės kainuotų ne įvertinimą, o dieną. Todėl:
>
> - **Trys naujos lentelės maksimumas** (`tab:filtras`, `tab:matrica` + perkelta `tab:reikalavimai`). Protokolas — **tekstu**, ne lentele.
> - Išmatuotas tankis: 2 sk. **269 žod./psl.** dėl lentelių, 1 sk. — 374. Vadinasi, ~4 psl. čia reiškia **~1 200–1 400 žodžių teksto**. Tai biudžetas, ne apytikslis skaičius.
> - Jei 17:00 tekstas viršija 4,5 psl. — pjaunama 3.1 (suliejama su 3.2) ir 3.4 proza (matrica kalba pati).

---

## 4. Lentelių specifikacija — stulpeliai fiksuojami dabar

### `tab:filtras` — kietieji apribojimai (T2)

| Stulpelis | Turinys |
|---|---|
| Metodas | 17 apžvelgtų, ta pati eilių tvarka kaip `tab:metodai` |
| K1 duomenų struktūra | ✓ / ✗ |
| K2 prielaidos | ✓ / ✗ |
| K3 mokymo kaina | ✓ / ✗ |
| K4 inferencijos delsa | ✓ / ✗ |
| Rezultatas | **Praeina** / atmetimo priežastis, 3–5 žodžiai |

> **Šios lentelės vertė — stulpelių pasiskirstymas.** Iš aštuonių atmetimų **keturi** krenta ties K1, **vienas** ties K2, **du** ties K3 ir **vienas** ties K4. Taigi kietuosius vartus daugiausia uždaro duomenys, ne aparatūra. Tas pats faktas, kuris `metodu_apzvalga.md` užrašytas proza, čia tampa matomas vienu žvilgsniu.
>
> ⚠️ **Formatas:** `tabularx`, `\small`, **be `table` float'o**, jei netelpa (1 užd. `xltabular` pamoka). 17 eilučių × 6 stulpeliai ≈ 0,6 psl.

### `tab:matrica` — sprendimų matrica (T4) ⭐

| Stulpelis | Turinys |
|---|---|
| Metodas | 9 likę po filtro |
| Tikslumo potencialas (w₁) | Balas 1–5 |
| Atsparumas disbalansui (w₂) | Balas 1–5 |
| Resursai: inferencija + dydis (w₃) | Balas 1–5 |
| Interpretuojamumas (w₄) | Balas 1–5 |
| Realizavimo rizika (w₅) | Balas 1–5 |
| **Svertinė suma** | 1,00–5,00, du skaitmenys |
| Šaltinis | `\cite{}` arba **(aut.)** |

> **Taisyklė, be kurios matrica bevertė: balų skalė apibrėžiama PRIEŠ balus.** Kiekvienam kriterijui — viena eilutė, ką reiškia 1 ir ką reiškia 5. Pvz., „Resursai: 5 = inferencija < 10 µs ir modelis < 5 MB; 1 = inferencija > 100 ms arba modelis > 100 MB“. Be to balai yra nuojauta skaičiaus pavidalu — tiksliai ta klaida, nuo kurios saugo `tab:metodai` stulpelis „Šaltinis“.

> ⭐ **Matrica generuojama iš CSV, ne rašoma ranka.** `rezultatai/darbiniai/sprendimu_matrica.csv` → `tab:matrica`. Priežastis praktinė: jautrumo analizė (T5) perskaičiuoja svertines sumas, ir perrašinėti jas ranka reiškia įvesti klaidų klasę, kurios visame darbe sąmoningai atsisakyta (žr. `praktikos_planas.md` „Svarbiausias triukas“). Tas pats `i_latex.py` principas, tik anksčiau nei planuota.

### `tab:reikalavimai` — **perkeliama**, ne kuriama (T1)

Lentelė jau egzistuoja `01_atakos.tex`. Perkėlimas numatytas dar pradiniame plane, ir jis sprendžia du dalykus vienu veiksmu: **1 skyrius susitraukia**, o 3 skyrius gauna savo kriterijų pagrindą į savo vietą, o ne per nuorodą atgal.

⚠️ **Techninė seka, kad nesulūžtų:** perkelti bloką → patikrinti, kad `\label{tab:reikalavimai}` liko **vienas** visame darbe → surasti visas `\ref{tab:reikalavimai}` 1 skyriuje → perrašyti sakinius, kurie dabar rodo pirmyn, ne atgal → `build.ps1` → **0 neišspręstų nuorodų**. Rugs. 2 d. dubliuoto `\label` pamoka: `.aux` failas parodo problemą, jei jo išvestį skaitai *ieškodamas dublikatų*, o ne ko kito.

---

## 5. Eksperimento protokolas — dienos svarbiausias rezultatas ⭐

**Tai vienintelė šios dienos dalis, kurios turinio dar niekur nėra.** Kiekvienas punktas turi baigtis konkrečia reikšme. Punktas, kuriame parašyta „bus nuspręsta 4 užduotyje“, yra neužrakintas punktas ir grąžina mus į rugsėjo 9 d. spėliojimą.

### 5.1. Duomenų imtis

1. **Riba 100 000 eilučių klasei**, stratifikuota; retos klasės imamos visos. Rezultatas — 2 429 978 eilutės (5,40 % rinkinio).
2. **Imties `random_state` fiksuojamas** ir įrašomas į `konfig/`. Imtis sudaroma **vieną kartą** ir išsaugoma kaip `duomenys/processed/imtis.parquet`. Visi keturi modeliai mato **tą patį** failą — kitaip palyginimas lygina ir duomenų atsitiktinumą.

### 5.2. Valymas — tvarka fiksuota

3. `dropna(subset=["Label"])` → `replace([inf, -inf], nan)` → `dropna()`. Pašalinama ~1 700 eilučių iš 45 mln. **Tvarka svarbi:** nutrūkusios eilutės šalinamos pirmos, nes jos duotų 35-ą klasę.
4. Etikečių normalizavimas: `.str.strip().str.upper()` + `BENIGN` atitikmuo (**ne** `BENIGNTRAFFIC`).

### 5.3. Požymiai

5. **Šalinama sąrašu, ne koreliacijos filtru.** Pašalinami: `Variance` (= `Std`²), `Tot size` **arba** `AVG` (paliekamas `AVG`, nes jis tiesiogiai interpretuojamas), `Tot sum` (= `AVG` × `Number`). **`Rate` lieka** — tapatybė `Rate` = 1/`IAT` rugs. 2 d. **paneigta** (305 006 nesutapimai iš 499 988).
6. Lieka **36 požymiai**. Pagrindimas ataskaitoje: 0,95 koreliacijos filtras `Variance`/`Std` poros nepašalintų (tiesinė koreliacija tik 0,737), nors ryšys yra tikslus — automatinis filtras čia netinka iš principo.

### 5.4. Skaidymas — ⚠️ pagrindinis dienos sprendimas

7. **Stratifikuotas atsitiktinis 70 / 15 / 15**, `random_state` fiksuotas. Chronologinis neįmanomas — rinkinyje nėra `ts`. Apribojimas įvardijamas **atvirai**, viename sakinyje, 3.6 poskyryje.
8. **Skaidymas atliekamas vieną kartą, indeksai išsaugomi** (`duomenys/processed/skaidymas.npz`). Kiekvienas paleidimas juos įkelia, ne perskaido.
9. ⭐ **Dublikatų patikra prieš skaidymą — privaloma.** 97,7 % rinkinio yra potvynio srautas, kurio eilutės gali sutapti tiksliai. Jei tokios eilutės pasiskirsto tarp `train` ir `test`, modelis testuojamas tuo, ką matė mokantis, ir **rezultatas išpūstas be jokios akivaizdžios klaidos.** Veiksmas: suskaičiuoti `df.duplicated().sum()` ant imties; jei > 1 %, **tikslūs dublikatai šalinami prieš skaidymą**, skaičius įrašomas į ataskaitą.

> Tai stipriausia turima apsauga nuo nutekėjimo po to, kai atmesti antriniai rinkiniai. Ir ji pigi — viena eilutė kodo prieš skaidymą.

### 5.5. Balansavimas

10. **Pirmas variantas — `class_weight="balanced"`** (RF, MLP) ir `scale_pos_weight` (XGBoost). Duomenys nedubliuojami.
11. **SMOTE — tik kaip abliacija vienam modeliui** (XGBoost), ne visiems: `imani2025imbalance` rodo, kad geriausias derinys yra suderintas XGBoost su SMOTE, todėl vertą patikrinti, bet ne dauginti iš keturių. **Taikoma tik `train`, niekada `val`/`test`** — ir tai užrašoma kaip taisyklė, ne kaip ketinimas.

### 5.6. Užduoties formuluotė

12. **Pagrindinė: 8 kategorijos** (`etiketes.py` žodynas). Dvejetainė ir 34 klasių — **tik geriausiam prižiūrimam modeliui**, palyginimui su `almahaqeri2026gradient`.
13. **Autokoderis vertinamas dvejetainėje formuluotėje** — 6 sk. lentelė turės dvi dalis (palyginimo asimetrija, numatyta 2.8).

### 5.7. Metrikos — fiksuojamos dabar

14. **Pagrindinė: macro-F1.** Šalia: per-klasę P/R/F1, **PR-AUC** (stabilesnė už F1 prie 84:1 — `imani2025imbalance`), ROC-AUC, MCC, sumaišymo matrica.
15. **Accuracy pateikiama**, bet **tik** palyginimui su literatūra, su pastaba, kad prie 41,8:1 ji nėra rodiklis. Nepateikti jos būtų nesąžininga kita kryptimi — ji yra tai, ką skelbia visi cituojami darbai.
16. **Veikimo rodikliai:** grynoji inferencijos delsa (µs/įrašui), **atskirai** nuo lango sukaupimo laiko (2 užd. 12-as radinys), mokymo laikas, modelio dydis MB.

### 5.8. Kartojimai ir hiperparametrai

17. **3 seed'ai (42, 43, 44)**, vidurkis ± std. 5, jei liks laiko. Prie 4 modelių × 3 seed'ai ≈ **12 pagrindinių paleidimų** + abliacijos.
18. **Random Search, 20–30 bandymų, tik ant `val`.** Ne Grid Search. Biudžetas ≤ 30 min. vienam modeliui be GPU.
19. **`test` aibė neliečiama iki 5 užduoties.** Užrašoma kaip taisyklė, nes ją pažeisti lengviausia netyčia — vieną kartą „tik pažiūrėti“.

### 5.9. Autokoderio protokolas — atskirai

20. Mokoma **tik ant `train` `BENIGN` dalies** (1 051 373 eilutės rinkinyje, imtyje — 100 000).
21. ⚠️ **Slenkstis kalibruojamas ant `val` `BENIGN` dalies** (pvz., 95-asis atkūrimo paklaidos procentilis), **niekada ant `test`.** Tai antras pagal tikimybę nutekėjimo kelias po dublikatų.

### 5.10. Nematytos atakų klasės testas — privaloma 5 užd. dalis

22. **Klasės parenkamos šiandien**, ne rugsėjo 15 d. Kriterijai: (a) skirtingos kategorijos, (b) pakankamai `test` pavyzdžių išmatuoti, (c) ne tokia klasė, kurios pašalinimas ištuštintų visą kategoriją.
23. **Kaina: 2–3 papildomi mokymai**, tik geriausiam prižiūrimam modeliui ir autokoderiui. Telpa į biudžetą.

### 5.11. Rezultatų failo schema — fiksuojama dabar ⭐

24. `rezultatai/rezultatai.csv` stulpeliai: `modelis · formuluote · seed · macro_f1 · weighted_f1 · accuracy · pr_auc · roc_auc · mcc · fpr · mokymo_laikas_s · inferencija_us · modelio_dydis_mb · konfig · data`.

> **Kodėl schema rakinama dabar.** `i_latex.py` jau parašytas ir 5–6 užduočių lentelės generuojamos iš šio failo. Pakeitus stulpelius rugsėjo 15 d., perrašomas ir skriptas, ir jau surinktos eilutės. Penkios minutės dabar — arba pusdienis tada.

---

## 6. Jautrumo analizė (T5) — kaip tiksliai

**Klausimas:** ar ketvertas priklauso nuo to, kad tikslumui daviau 30 %, o ne 25 %?

**Procedūra:**

1. Bazinis rinkinys: w = (0,30 · 0,25 · 0,20 · 0,15 · 0,10).
2. Kiekvienam kriterijui atskirai: **+10 p. p.** ir **−10 p. p.**, likusieji perskirstomi proporcingai (suma visada 1,00). Gaunama **10 alternatyvių rinkinių**.
3. Kiekvienam — perskaičiuojama svertinė suma ir rikiuotė.
4. Fiksuojama: **kiek kartų iš 10 keičiasi pirmieji trys prižiūrimi metodai.**

**Ką rašyti į ataskaitą — abiem atvejais:**

- Jei rikiuotė nesikeičia → atranka nuo svorių nepriklauso, ir tai **stipriausias įmanomas argumentas** už jos objektyvumą.
- Jei keičiasi → **tai irgi rašoma**, kartu su tuo, kuris kriterijus lemiamas. Tada išvada formuluojama atsargiau: „RF ir XGBoost pozicijos stabilios, MLP ir 1D-CNN vietomis keičiasi priklausomai nuo interpretuojamumo svorio.“

> **Kodėl svarbu užsirašyti tai iš anksto.** Jei rezultatą interpretuosiu po to, kai jį pamatysiu, atsiras pagunda pakoreguoti svorius, kol rikiuotė „nusistovės“. Užrašius abu variantus dabar, ta pagunda dingsta. Tas pats principas kaip su hipotezės registravimu prieš eksperimentą.

**Įgyvendinimas:** ~20 eilučių `pandas`; CSV → svertinės sumos → `tab:matrica` per `to_latex()`. Vienas failas: `src/eksperimentai/jautrumas.py`.

---

## 7. Laiko biudžetas — rugsėjo 3 d. (ketvirtadienis)

Diena prasideda 12:45, todėl biudžetas trumpesnis nei įprastas. **Tai įmanoma tik todėl, kad atranka jau padaryta vakar** — šiandien ji perkeliama į popierių, o tikras naujas darbas yra protokolas.

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| 12:45–13:15 | **T0:** `tab:atakos` eilutės, mininčios `flow_duration` ir asimetriją → `Number`/`IAT`/`Rate` arba žyma „nepadengta duomenimis“ | 1 sk. atitinka realius duomenis | **P0** |
| 13:15–13:35 | **T0:** kodo likučiai — patikrinti `ikelimas.py` / `etiketes.py` (`Label`, `.upper()`, `BENIGN`); paleisti `python -m src.duomenys.etiketes` | `assert` praeina | **P0** |
| 13:35–14:05 | **T1:** `tab:reikalavimai` perkėlimas + nuorodų taisymas + `build.ps1` | 0 klaidų, 0 neišspręstų nuorodų | **P0** |
| *14:05–14:35* | *Pietūs* | | |
| 14:35–15:15 | **T2:** `tab:filtras` — pildoma **mechaniškai** iš `metodu_apzvalga.md` 7 sk. atmetimo lentelės | 17 eilučių, tuščių langelių nėra | **P0** |
| 15:15–15:45 | **T3 + T4:** balų skalė (5 eilutės) → `sprendimu_matrica.csv` → `tab:matrica` | CSV + generuota lentelė | **P0** |
| 15:45–16:05 | **T5:** `jautrumas.py`, 10 svorių rinkinių | Rezultatas užrašytas, koks bebūtų | **P0** |
| **16:05–17:05** | **T6: eksperimento protokolas** — 24 punktai (5 sk.) | ⭐ **Dienos svarbiausias rezultatas** | **P0** |
| 17:05–17:50 | **T7:** 3.2–3.6 tekstas aplink lenteles | ~3,5 psl. | **P0** |
| 17:50–18:05 | **T7:** 3.1 ir 3.7 — **rašomi paskutiniai** | ~0,6 psl. | P1 |
| 18:05–18:30 | `build.ps1` · git commit + push · `DARBO_ZURNALAS.md` · `STRUKTURA.md` | Kompiliuojasi | **P0** |
| *rezervas* | **T8:** 2 nauji šaltiniai + anotacijos | 20 įrašų | P1 |

**Dienos pabaigos minimumas:** protokolas užrakintas (24 punktai), `tab:filtras` ir `tab:matrica` užpildytos, PDF kompiliuojasi. Viskas kita gali persikelti į rugsėjo 4 d. rytą — **grafikas eina 5 dienomis į priekį, rezervo yra daugiau nei bet kada.**

> **Ko į šią dieną NEKELTI.** Smulkmenos (`requirements-lock.txt`, titulinis puslapis, `houichi` eilutė, dubliuotos anotacijos) — **rezervo laikas arba rugs. 4 d.** Jos pigios, todėl viliojančios; bet kiekviena iš jų yra konteksto perjungimas, o šiandien yra vienas P0 darbas, kuriam reikia ištisos valandos susikaupimo.

---

## 8. Priėmimo kriterijai

- [ ] `tab:atakos` neminimi požymiai, kurių 39 požymių leidime nėra
- [ ] `python -m src.duomenys.etiketes` praeina be `AssertionError`
- [ ] `tab:reikalavimai` yra 3 skyriuje; `\label{tab:reikalavimai}` visame darbe **vienas**; 0 neišspręstų nuorodų
- [ ] `tab:filtras` — **17 eilučių**; kiekvienas ✗ turi priežastį; atmetimų suma = **8**
- [ ] Balų skalė (1–5) apibrėžta **kiekvienam** iš 5 kriterijų **prieš** balus
- [ ] Kiekvienas iš 5 svorių turi sakinį, nurodantį konkrečią `tab:reikalavimai` eilutę
- [ ] `tab:matrica` sugeneruota iš CSV, ne surinkta ranka
- [ ] Jautrumo rezultatas įrašytas — **nesvarbu, patvirtina jis ketvertą ar ne**
- [ ] Autokoderio įtraukimas pagrįstas **atvirai** kaip funkcinis reikalavimas, o ne kaip balų rezultatas
- [ ] **Visi 24 protokolo punktai turi konkrečią reikšmę.** Nė viename nėra „bus nuspręsta vėliau“
- [ ] `rezultatai.csv` stulpelių schema užrašyta ir suderinta su `i_latex.py`
- [ ] Nematytos klasės testui **klasės įvardytos vardais**, ne „2–3 klasės“
- [ ] Dublikatų patikros sprendimas (slenkstis, veiksmas) užrašytas prieš skaidymą
- [ ] Skyrius kompiliuojasi be klaidų · TODO nėra · **≤ 4,5 psl.** *(laiko, ne formato biudžetas — žr. 12 sk.)*
- [ ] ⭐ **3 skyrius PDF'e yra trečias** — numeracija atitinka užduočių sąrašą, nes tai vienintelis vadovo turimas kriterijus
- [ ] ⭐ **3.7 poskyryje matomas užduoties rezultatas** — kas pasirinkta ir kas užrakinta — neverčiant skaityti viso skyriaus
- [ ] Automatinė patikra praleista: kirilica · `\SI` reikšmės · `\section` skyrių failuose · dubliuoti `\label`
- [ ] `git push` · `DARBO_ZURNALAS.md` papildytas · `STRUKTURA.md` atnaujinta

---

## 9. Rizikos

| Rizika | Ženklas | Veiksmas |
|---|---|---|
| ⭐ **Matrica virsta jau priimto sprendimo pagražinimu** | Balai suvedami taip, kad „išeitų“ ketvertas | Dviejų pakopų filtras + jautrumo analizė + atviras pripažinimas, kad autokoderis balais pralaimi. **Tai visos dienos metodinė ašis** |
| **Protokolas lieka pusiau atviras** | Punkte parašyta „reikės nuspręsti“ | Priėmimo kriterijus to neleidžia. Neužrakintas punktas = rugs. 9 d. spėliojimas |
| `tab:reikalavimai` perkėlimas sulaužo nuorodas | Neišspręsta nuoroda `build.ps1` išvestyje | Prieš perkeliant — `\ref{tab:reikalavimai}` paieška visame darbe. Po — `.aux` tikrinamas **ieškant dublikatų**, ne ko kito (rugs. 2 d. pamoka) |
| **Skyrius išplinta trečią kartą iš eilės** | 17:00 tekstas > 4,5 psl. | Protokolas **tekstu**, ne lentele. Pjaunama 3.1 (į 3.2) ir 3.4 proza |
| Jautrumo analizė paneigia ketvertą | Rikiuotė keičiasi > 3 kartus iš 10 | **Rašoma, kaip yra.** Ketvertas nesikeičia — jį gina paradigmų padengimas, ne balai. Bet rikiuotės nestabilumas turi būti įvardytas |
| Dienos likutis trumpas (prasidedama 12:45) | 16:05 protokolas nepradėtas | **T7 tekstas persikelia į rugs. 4 d.** Protokolas — ne. Tekstą galima parašyti bet kada, protokolas blokuoja 4 užduotį |
| Smulkmenos suvalgo P0 laiką | 15:00 vis dar taisomas titulinis puslapis | Jos **ne šios dienos** darbas (žr. 7 sk. pastabą) |
| Aplinkos problemos | Kompiliavimo klaida | Ta pati taisyklė: **po pirmo nepavykusio taisymo — ne antras spėjimas, o duomenys** (pilnas log'as, `-Clean`, bisekcija) |

---

## 10. Kas keliauja į 4 užduotį (rugs. 4 d. arba 9 d.)

Užsirašyti dabar, kad rugsėjo 9 d. nereikėtų atkurti:

- **Protokolo 24 punktai yra 4 užduoties specifikacija.** `pozymiai.py`, `balansavimas.py` ir `paleisti.py` rašomi tiesiai iš jų
- **Skaidymas ir imtis sudaromi vieną kartą ir išsaugomi** — ne perskaičiuojami kiekvieno paleidimo metu
- **Dublikatų patikra — pirmas žingsnis** po įkėlimo, prieš bet ką kita
- **Vienodas modelių sąsajos kontraktas** (`fit` / `predict` / `predict_proba`) — nuo to tiesiogiai priklauso, ar 6 užduotis bus vienas ciklas, ar keturios dienos rankų darbo
- **`rezultatai.csv` schema fiksuota** — `i_latex.py` jau tinka
- **Isolation Forest** pridedamas, **jei liks laiko** — pigus etalonas autokoderiui, mokymas minutėmis
- **INT8 kvantavimas** — tik jei MLP netikėtai nugalės ansamblius
- **SHAP → 6 užduotis**, ne 4 (`mohale2025xai`: brangus, ne inferencijos grandinės dalis)
- **Grafikas 5 dienomis priekyje.** Tai ne raginimas skubėti, o atsarga 4 užduočiai — būtent joje plane numatyta didžiausia techninė rizika

---

## 11. Likučiai — rezervo laikas arba rugs. 4 d. rytas

- [ ] `pip freeze > requirements-lock.txt`
- [ ] Titulinio puslapio fakultetas ir praktikos vadovas
- [ ] `houichi2025smartcity` metrikos — reikia universiteto prieigos (Wiley 403). Jei negaunama iki rugs. 8 d., eilutė iš `tab:susije` **išimama**, o šaltinis lieka tekste
- [ ] `literatura/literatura_anotacijos.md` — **ištrinti** dubliuotą kopiją, palikti `anotacijos.md`
- [ ] `bibtestas.tex` / `bibtestas2.tex` — ištrinti radus biblatex priežastį (arba rugs. 18 d.)
- [ ] `praktikos_planas.md` 4 sk. („Realistinė apimtis“) — **pažymėti, kad 26–34 psl. norma neegzistuoja** (žurnale jau pažymėta)
- [ ] T8: 2 nauji šaltiniai — SMOTE pirminis šaltinis ir statistinio klasifikatorių palyginimo metodika. **Taisyklė nesikeičia: be patikrinto DOI į `.bib` nepatenka**

---

## 12. Apimties klausimas uždarytas ✅

**Patikslinta (2026-09-03).** Du dalykai, kurie panaikina visą šio skyriaus ginčą:

1. `ataskaita.tex` **nėra visa VILNIUS TECH praktikos ataskaita** — tai dokumentas, teikiamas **Aineros praktikos vadovui**.
2. **Jokių reikalavimų nėra.** Nei apimties, nei struktūros, nei formato. Yra **tik užduočių sąrašas.**

**Vadinasi, 26–34 psl. normos neegzistuoja.** Ji buvo mano prielaida, ir visa nuo jos išvesta apskaita — trumpinimo kandidatų sąrašas, −6 psl. nuo eilučių intervalo, „proporcijų“ pastaba — matavo atstumą iki taikinio, kurio nėra.

### Kas užima jos vietą

**Vienintelis išorinis kriterijus yra pats užduočių sąrašas.** Vadovas neturi kuo tikrinti darbo, išskyrus klausimą: *ar visos šešios užduotys atliktos ir ar tai matyti.* Iš to seka du konkretūs dalykai, ir abu pigūs:

- **Skyrių numeracija turi sutapti su užduočių numeracija** — 1 sk. = 1 užd. ir t. t. Dabar taip ir yra (`01_atakos` … `06_palyginimas`), tad **nieko daryti nereikia, tik nesugriauti.** Rugsėjo 2 d. dubliuoto `\section` klaida kaip tik buvo tai sugriovusi: turinys nuslinko į 4 skyrių ir sutapimas dingo. Tai buvo rimčiau, nei atrodė.
- **Kiekvienas skyrius baigiasi matomu tos užduoties rezultatu.** 2 skyriuje tai 2.8 (kandidatų aibė), 3 skyriuje bus 3.7. Vienas poskyris, iš kurio skaitantysis mato, kad užduotis uždaryta.

### Apimtis dabar yra laiko biudžetas

Puslapiai nebeturi kam atsiskaityti, todėl **4 psl. taikinys lieka, bet kito pagrindo:** kiekviena diena, praleista rašant teoriją, yra diena, neatiduota 4–6 užduotims — o būtent jos yra tos, kurių vadovas negalės pamatyti, jei nespėsiu.

**Sprendimai, kurie iš to seka:**

- **Trumpinimo klausimas uždaromas visai.** Ne atidedamas — uždaromas. Rugsėjo 17 d. jam nebegrįžtame; jei kas nors trumpinama, tai tik todėl, kad netarnauja skaitytojui, ne dėl skaičiaus.
- **Eilučių intervalas nekeičiamas.** Matavimas (−6 psl.) buvo teisingas ir dabar nereikalingas.
- ⭐ **Vienintelė likusi apimties rizika yra priešinga tai, kurios bijojau:** ne per ilgas dokumentas, o **~23 psl. teorijos prieš plonus 4–6 skyrius.** Tai vienintelė proporcija, kuri iš tikrųjų svarbi, ir ji sako **nemažinti 4–6 skyrių**, kai rugsėjo 9–17 d. spaus laikas.

⚠️ **Taisytina kituose failuose:** 26–34 psl. norma tebeguli `praktikos_planas.md` 4 skyriuje („Realistinė apimtis“) ir žurnalo rugsėjo 2 d. 24 punkte. **Žurnalo įrašas pažymėtas**; `praktikos_planas.md` — dar ne. Kol nepažymėta, po savaitės vėl bus skaičiuojama nuo neegzistuojančio skaičiaus.
