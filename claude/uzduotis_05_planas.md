# 5 UŽDUOTIS — Eksperimentinis vertinimas

**Tikslų planas**
**Sudaryta:** 2026 m. rugsėjo 8 d. vakare
**Vykdymas:** rugsėjo 9 d. (trečiadienis). Pradiniame plane — rugs. 15–16 d.; grafikas eina **6 dienomis į priekį**
**Rezultatas:** `ataskaita/skyriai/05_vertinimas.tex` (~5–6 psl.), `rezultatai/rezultatai.csv` su **test** eilutėmis, 3 generuojami paveikslai

---

## 0. Būklė — patikrinta failuose, ne žymose ⭐

> Žurnale penkis kartus kartojasi ta pati klaida: būklė pažymima neatidarius failo. Todėl šis planas pradedamas nuo faktinės repozitorijos patikros, ne nuo `uzduotis_04_planas.md` žymų. **Trys iš keturių patikrintų dalykų nesutapo su žymomis.**

| Ko 5 užduočiai reikia | Faktinė būklė | Kaip patikrinta |
|---|---|---|
| **Permokymas su suderintais parametrais** | ✅ **ATLIKTAS.** `*_derintas_8kat_seed42..44` yra visiems trims prižiūrimiems | `ls rezultatai/apmokyti/` |
| `rezultatai.csv` | ✅ **21 eilutė:** 9 baziniai + 9 suderinti + 3 autokoderis | `wc -l` |
| Apmokyti modeliai įsikelia | ⚠️ **Nepatikrinta.** RF suderintas — **670 MB** faile (ne 637,9) | `ls -la` |
| `slenkscio_taskai.csv`, kreivės | ✅ Yra | 4 užd. |
| Nematytų klasių sąrašas | ✅ `DDOS-SLOWLORIS`, `RECON-PORTSCAN`, `DICTIONARYBRUTEFORCE` | protokolo 22 p. |
| Reikšmingumo taisyklė | ✅ Skirtumas tikras tik viršijęs paleidimų sklaidą | `dietterich1998tests` |
| **`test` aibė** | ✅ **Neliesta** | `paleisti.py` be `--vertinimas test` jos neįkelia |
| **Infrastruktūra `test` vertinimui** | ❌ **Neparuošta — trys blokuojantys dalykai** | žr. 2.1 sk. |
| **Vertinimo protokolas ant `test`** | ❌ **Neužrakintas** | ⚠️ **šios dienos darbas** |

**`uzduotis_04_planas.md` žyma „Permokymas — dar nepaleistas“ yra pasenusi** — permokymas atliktas rugsėjo 8 d. rytą (failų laikai 06:07–06:47). Žymą pataisyti.

**Turimi `val` skaičiai ties FPR ≤ 1 % (suderinti modeliai):** XGBoost **0,6578** · Random Forest 0,6423 · MLP 0,5906 · autokoderis 0,220 *(FPR 1 %, aptinka 11,8 %)*.

---

## 1. Pagrindinė šios užduoties problema — ir kaip ji sprendžiama ⭐

### 1.1. `test` aibę nori paliesti keturi skirtingi dalykai

Pagrindinis ciklas (4 modeliai × 3 seed'ai), nematytų klasių testas, dvejetainė ir 34 klasių formuluotės, klaidų analizė su sumaišymo matricomis. **Jei kiekvienas bus atskiras „paleidimas ir pažiūrėjimas“, `test` aibė bus panaudota keturis kartus, o kiekvienas paskesnis sprendimas priimtas jau matant ankstesnį rezultatą.**

Formaliai nutekėjimo nebus — modeliai nepermokomi. Bet **atrankos nutekėjimas bus**: pamatęs, kad kažkuris pjūvis atrodo prastai, imsiu rinktis kitą. Tai ta pati yda, nuo kurios 3 užduotyje saugojo dviejų pakopų filtras.

**Sprendimas — tas pats principas, kitoje vietoje:**

| Pakopa | Kur vyksta | Kas sprendžiama |
|---|---|---|
| **A. Sprendimai** | **Tik ant `val`**, prieš liečiant `test` | Operacinis taškas *τ*, kurie modeliai lyginami, kokios lentelės ir paveikslai, kokie pjūviai |
| **B. Matavimas** | **Vienas prėjimas per `test`** | Vienas rezultatų failas su visais reikalingais pjūviais iš karto |
| **C. Aprašymas** | Iš to failo | Visos lentelės ir paveikslai generuojami; `test` nebeliečiama |

**Praktinė išraiška:** prieš pirmą `--vertinimas test` paleidimą užrašomas sąrašas, **kokie skaičiai bus gauti ir kokios lentelės iš jų sudaromos**. Jei po paleidimo prireiks pjūvio, kurio sąraše nebuvo — jis pridedamas **įvardijant, kad pridėtas po fakto**.

### 1.2. Nematytų klasių testas turi tris spąstus, ir visi trys pigūs dabar ⚠️

**1. `DICTIONARYBRUTEFORCE` pašalinimas ištuština visą `BruteForce` kategoriją.** Ji yra vienintelė savo kategorijos klasė. Vadinasi, permokytas prižiūrimas modelis 8 kategorijų formuluotėje turės **7 klases**, ir jo macro-F1 su bazinio modelio macro-F1 **tiesiogiai nepalyginamas** — vidurkinama per skirtingą klasių skaičių.

> **Užrakinama dabar:** nematytų klasių testas vertinamas **dvejetainiu klausimu** — ar pašalintos klasės eilutės `test` aibėje pažymimos kaip ataka (bet kuri), ar praleidžiamos. Rodiklis: **aptikimo dalis pašalintoje klasėje** prie to paties FPR biudžeto. macro-F1 čia nenaudojamas nė vienam modeliui.

**2. Autokoderiui nematytų klasių testas yra tuščias veiksmas.** Jis mokomas **tik iš `BENIGN`**, todėl **visos 33 atakų klasės jam ir taip nematytos**. Permokyti jį be `DDOS-SLOWLORIS` reikštų gauti tą patį modelį.

> **Užrakinama dabar:** autokoderis **nepermokomas**. Jo skaičius šioms trims klasėms imamas iš **bazinio `test` paleidimo per-klasę aptikimo dalies**. Tai ne apėjimas, o teisingas palyginimas: klausimas yra „ar neprižiūrimas metodas aptinka tai, ko prižiūrimas nematė“, ir jam atsakyti permokymo nereikia.

**3. Kaina — 3 permokymai, ne 6.** Tik geriausias prižiūrimas modelis (pagal `val` — XGBoost), po vieną permokymą kiekvienai pašalintai klasei, vienas seed'as. Trys paleidimai po ~2 min. GPU.

> ⭐ **Iš to seka lentelės sandara, kurią verta užrašyti prieš matavimą:** eilutė = pašalinta klasė; stulpeliai = *n* `test` pavyzdžių · prižiūrimo modelio, **permokyto be tos klasės**, aptikimo dalis · autokoderio aptikimo dalis (bazinis) · prižiūrimo modelio aptikimo dalis, **kai klasė buvo mokyme**. **Ketvirtasis stulpelis yra tas, kuris paverčia lentelę atsakymu** — jis parodo, *kiek kainuoja* nematyti klasės, o ne tik ar ji aptinkama.

### 1.3. Rezultatas bus žemesnis už 2 užduotyje užsibrėžtą taikinį — planuojama iš anksto

`val` ties FPR biudžetu duoda macro-F1 **0,66**, o 2 skyriuje užrašytas realistinis taikinys buvo **0,85–0,90** (`almahaqeri2026gradient`). `test` skaičiai bus panašūs.

**Abu variantai užrašomi dabar, kad po matavimo nebūtų pagundos interpretuoti palankiai** — ta pati taisyklė kaip 3 užduoties jautrumo analizėje:

- **Jei `test` ≈ `val`** (skirtumas < paleidimų sklaidos): patvirtinta, kad skaidymas ir slenksčio parinkimas rezultatų neišpūtė. Skirtumas nuo literatūros aiškinamas **trimis išmatuotais veiksniais** — pašalinti 53,3 % dublikatų, 39 požymių leidimas vietoj 46, palyginimas ties FPR biudžetu, o ne ties argmax. Nė vienas nėra prielaida.
- **Jei `test` pastebimai skiriasi nuo `val`:** tai savarankiškas radinys ir rašomas pirmiau už viską. Geresnis → tikrinamas nutekėjimas (5 sk.). Blogesnis → tikrinama, ar *τ*, parinktas ant `val`, ant `test` duoda tą patį FPR. Jei ne, tai rezultatas apie **operacinio taško perkeliamumą**, ir 6 skyriui jis vertingesnis už bet kurį macro-F1.

> **Ko nedaryti:** nerinkti *τ* iš naujo ant `test`. Tai būtų nutekėjimas — būtent tas, kurį protokolo 21 punktas įvardija kaip antrą pagal tikimybę.

---

## 2. Konkretūs tikslai

| Nr. | Tikslas | Išmatuojamas rezultatas | Prior. |
|---|---|---|---|
| **T0** | **Paruošti infrastruktūrą `test` vertinimui** — trys blokuojantys taisymai (2.1) | Paleidus `--vertinimas test`, val eilutės **išlieka** | **P0** |
| **T1** | **Užrakinti vertinimo protokolą** prieš liečiant `test` | 3 sk. — 12 punktų, visi su konkrečia reikšme | **P0** |
| **T2** | Pagrindinis ciklas ant `test`: 4 modeliai × 3 seed'ai × 8 kategorijos | `rezultatai.csv` +12 eilučių su `aibe=test` | **P0** |
| **T3** | Veikimo rodikliai — **vienu paleidimu, vienoje mašinoje, CPU** | `veikimas.tex` | **P0** |
| **T4** | Klaidų analizė: sumaišymo matricos, per-klasę P/R/F1, `Benign`↔`Recon` | `pav:sumaisymas`; per-klasę lentelė su *n* stulpeliu | **P0** |
| **T5** | **Nematytų klasių testas** — 3 klasės, taisyklės iš 1.2 | `tab:nematytos`, 3 permokymai | **P0** |
| **T6** | Dvejetainė ir 34 klasių formuluotės **tik geriausiam prižiūrimam** | 2 eilutės; palyginimas su `almahaqeri2026gradient` | P1 |
| **T7** | Rezultatų patikimumo patikra — penki punktai (5 sk.) | Visi penki užrašyti | **P0** |
| **T8** | Paveikslai: sumaišymo matrica · FPR–aptikimo kreivės · PR kreivės | 3 PDF, **generuojami** | P1 |
| **T9** | Parašyti `05_vertinimas.tex` | 8 poskyriai, ~5–6 psl., 0 klaidų | **P0** |

**Ne šios užduoties tikslai:** SHAP ir požymių svarba (→ 6 užd.), suvestinis palyginimas ir rekomendacija (→ 6 užd.), Isolation Forest (tik jei liks laiko), naujas hiperparametrų derinimas (atliktas).

### 2.1. T0 — trys blokuojantys dalykai, rasti skaitant kodą ⚠️⚠️

Visi trys patikrinti `metrikos.py`, `paleisti.py` ir `slenkstis.py` failuose. **Nė vieno nebuvo 4 užduoties likučių sąraše.**

#### 1. `rezultatai.csv` neturi `aibe` stulpelio — `test` paleidimas **perrašytų** `val` rezultatus ⚠️⚠️⚠️

```
SCHEMA = [modelis, formuluote, seed, macro_f1, ..., konfig, data]
RAKTAS = [modelis, formuluote, seed, konfig]
```

`metrikos.prideti()` eilutę su tuo pačiu RAKTU **perrašo** — tai buvo teisingas rugsėjo 7 d. sprendimas prieš dublikatus. Bet **vertinimo aibės rakte nėra.** Paleidus `--vertinimas test` su tuo pačiu konfigu ir seed'u, `test` eilutė **užimtų `val` eilutės vietą**, ir visi 21 `val` rezultatas dingtų.

**Blogiausia, kad tyliai:** klaidos nebūtų, failas liktų tvarkingas, o `rezultatai.tex` rodytų `test` skaičius po išnaša apie `val`. **Tai tiksliai tos rūšies klaida, kurių šiame darbe jau buvo penkios: dalykas, kurio supainiojimas nepasirodo kaip klaida.**

**Taisymas:** į `SCHEMA` ir į `RAKTAS` įrašomas `aibe` (`val` / `test`). Esamos 21 eilutė papildoma `aibe=val`. `i_latex.py` filtruoja pagal `aibe`.

#### 2. `sumaisymas_{zyma}.csv` vardas irgi neturi aibės

`zyma = <konfigas>_<formuluotė>_seed<N>` — ta pati problema mažesniu mastu: `test` sumaišymo matricos perrašytų `val`. **Ta pati pamoka kaip rugsėjo 8 d. su modelių vardais** (`mokyti_derintus.bat` užrašė bazinius modelius), tik dabar pagauta **prieš**, ne po.

**Taisymas:** `zyma` papildoma aibe.

#### 3. `--vertinimas test` **permoko** modelius, o ne tik vertina

`paleisti()` visada kviečia `fit()` ir `issaugoti()`. Vadinasi, 12 „vertinimo“ paleidimų iš tikrųjų yra 12 permokymų: **suderintas Random Forest mokosi ~8 min.**, tad vien jis suvalgytų ~25 min., o modelių failai būtų be reikalo perrašyti.

**Taisymas:** `--tik-vertinti` veliava — įkelti išsaugotą modelį (`bazinis.rasti_issaugotus()` jau egzistuoja) ir tik vertinti. Šalutinė nauda: mokymo laiko stulpelis tada imamas iš mokymo paleidimo, o ne matuojamas iš naujo.

#### 4. `slenkstis.py` `test` aibės neatidaro visai

Kode `idx["val"]` įkalta, o modulio dokumentacijoje parašyta „test aibė čia neatidaroma“ — sąmoningas 4 užduoties sprendimas. **5 užduočiai reikia režimo, kurio nėra:** *τ* imamas iš `val` (jau apskaičiuotas, `slenkscio_taskai.csv`), o **taikomas `test`**.

**Taisymas:** `--taikyti test` režimas, kuris *τ* **skaito iš failo** ir jokiu būdu neperskaičiuoja. Perskaičiavimo galimybės tame režime neturi būti iš viso — taisyklė, kurios niekas netikrina, yra ketinimas.

#### 5. Ne blokuojantys, bet uždaromi kartu

| Kas | Pastaba |
|---|---|
| **Delsa matuojama CPU** | XGBoost GPU davė 4,13 µs, CPU 27,42 µs (6,5×). Šliuzas GPU neturi |
| **Random Forest 670 MB** | Trys seed'ai ≈ 2 GB. `joblib.load` anksčiau buvo nužudytas. `min_samples_leaf` — vienintelis likęs svertas |
| **`class_weight` aiškiu žodynu** | `"balanced"` persiskaičiuotų permokant be klasės (T5), ir testas matuotų **du pokyčius vienu metu** |
| **MLP `.keras` versijų suderinamumas** | `quantization_config` klaida įkeliant |
| **`rezultatai/apmokyti/metadata.json` tuščias** | `{"modeliai": {}}`, nors `STRUKTURA.md` jį vadina metaduomenų vieta. Kiekvienas modelis turi savo `.json` šalia — arba pildyti, arba išbraukti iš `STRUKTURA.md` |

---

## 3. Vertinimo protokolas — užrakinama prieš pirmą `test` paleidimą ⭐

**Kiekvienas punktas turi baigtis konkrečia reikšme.** Punktas, kuriame parašyta „bus matyti“, grąžina mus į sprendimą, priimtą matant rezultatą.

### 3.1. Operacinis taškas

1. **Naudojamas *τ*, parinktas ant `val`** (`slenkscio_taskai.csv`). Ant `test` **neperrenkamas jokiomis aplinkybėmis.** Jei ant `test` FPR pasirodo kitoks, tai **rezultatas**, ne klaida.
2. **Pagrindinis palyginimas — tik ties suderintu FPR biudžetu (≤ 1 %).** argmax skaičiai pateikiami **šalia**, antra lentelės dalimi, su nuoroda, kad rikiuotė ten kitokia. *(Rugs. 8 d.: prie argmax pirmauja Random Forest, ties biudžetu — XGBoost. Palyginimas ties argmax yra metodinė klaida, bet jo nuslėpimas būtų antra.)*
3. **Autokoderio *τ*** — 99-asis `val` `BENIGN` atkūrimo paklaidos procentilis. Nekeičiamas.

### 3.2. Ką matuoja vienas `test` prėjimas

4. **Modeliai:** RF, XGBoost, MLP, autokoderis — **suderintomis** konfigūracijomis. Baziniai konfigai į `test` **neina**: jų vaidmuo buvo parodyti derinimo prieaugį, ir tai padaryta ant `val`.
5. **Seed'ai:** 42, 43, 44. Vidurkis ± standartinis nuokrypis.
6. **Formuluotė:** 8 kategorijos. Dvejetainė ir 34 klasių — tik geriausiam prižiūrimam (T6).
7. **Vienu prėjimu išsaugoma visa, ko reikės:** 15 stulpelių · per-klasę P/R/F1 su *n* · sumaišymo matrica · **prognozių tikimybės** · nematytų klasių aptikimo dalys. Tikimybių masyvai išsaugomi, kad paveikslus būtų galima pergeneruoti **neliečiant `test` antrą kartą**.

### 3.3. Reikšmingumas ir tikslumas

8. **Skirtumas tikras tik viršijęs paleidimų sklaidą** (`dietterich1998tests`). Formalus testas neatliekamas — trijų paleidimų t-testo I tipo klaida pervertinta.
9. ⚠️ **Retų klasių metrikos pateikiamos su *n* stulpeliu.** `UPLOADING_ATTACK` turi **179** `test` pavyzdžius; vienas sprendimas keičia atkūrimą 0,6 p. p. **Tai ne kosmetika: retos klasės lemia macro-F1, tad jų neapibrėžtumas yra pagrindinio rodiklio neapibrėžtumas.**

### 3.4. Veikimo rodikliai

10. **Visi keturi modeliai — vienu paleidimu, vienoje mašinoje, CPU.** Taisyklė jau `delsa.py`; kartojama, nes ją lengviausia pažeisti netyčia.
11. **Grynoji inferencijos delsa atskiriama nuo lango sukaupimo laiko** (2 užd. 12-as radinys).

### 3.5. Kada rezultatas laikomas įtartinu

12. ⭐ **Tikslumas virš 99,78 % yra nutekėjimo požymis**, ne pasiekimas. Riba išmatuota savo duomenyse (`imties_ataskaita.md`). Tokiu atveju pirma 5 sk. patikros, ir tik jas praėjus skaičius rašomas.

---

## 4. Skyriaus `05_vertinimas.tex` struktūra

```
5. Eksperimentinis vertinimas
   5.1. Vertinimo protokolas ir operacinis taskas          (~0,6 psl.)
   5.2. Pagrindiniai rezultatai                            (~1,0 psl.)
        --> tab:rezultatai + tab:veikimas (generuojamos)
   5.3. Klaidu analize                                     (~1,2 psl.)
        --> pav:sumaisymas; per-klase lentele su n stulpeliu
        - Benign <-> Recon: 1 uzd. prognoze, patvirtinta matavimu
   5.4. Klaidingi teigiami ir slenkscio kompromisas        (~0,8 psl.)
        --> pav:fpr_kreives; autokoderio skardis 95 -> 99
   5.5. Nematytu ataku klasiu testas                       (~0,9 psl.)
        --> tab:nematytos
   5.6. Dvejetaine ir 34 klasiu formuluotes                (~0,5 psl.)
   5.7. Rezultatu patikimumas                              (~0,6 psl.)
   5.8. Apibendrinimas                                     (~0,3 psl.)
```

**Iš viso ~5,9 psl.**

> ⭐ **Apimties taikinys čia yra grindys, ne stabdis.** 1–3 skyriuose taikinys ribojo; nuo 4 skyriaus galioja priešinga taisyklė: **vienintelė likusi apimties rizika yra ~23 psl. teorijos prieš plonus 4–6 skyrius.** Jei 5 skyrius išeis 7 psl. — gerai. Jei 3 psl. — blogai.

**Kas rašoma, o kas ne** *(rugs. 3 d. vadovo taisyklė):* į skyrių — **kas išmatuota, kas pasirinkta, kokia to pasekmė**. Kaip prie to priėjau, ką bandžiau, kur suklydau — **į žurnalą.** Apribojimas rašomas kaip duomenų ar metodo savybė, ne kaip pasiaiškinimas.

---

## 5. Rezultatų patikimumo patikra — penki punktai

Atliekama **prieš** rašant skaičius į skyrių, ne po.

| Nr. | Patikra | Kaip |
|---|---|---|
| 1 | `test` nebuvo naudota parenkant nieką | *τ*, hiperparametrai, ankstyvas stabdymas, požymių sąrašas — visi iš `train`/`val` |
| 2 | Tarp `train` ir `test` nėra vienodų eilučių | `skaidymas.py` patikra Nr. 3 — kviečiama tiesiogiai |
| 3 | Tikslumas neviršija 99,78 % | Teorinė riba iš `imties_ataskaita.md` |
| 4 | **`test` FPR atitinka `val` FPR ties tuo pačiu *τ*** | Jei skiriasi > 2×, tai radinys apie operacinio taško perkeliamumą |
| 5 | Metrikos atkartojamos | Antras paleidimas duoda tuos pačius kokybės skaičius |

> **Ketvirtoji yra vienintelė, kurios rezultato nežinau iš anksto**, ir todėl vertingiausia. Trys pirmosios turėtų praeiti; jei nepraeitų, tai reikštų klaidą. Ketvirtoji gali duoti tikrą naują informaciją abiem kryptimis.

---

## 6. Laiko biudžetas — rugsėjo 9 d. (trečiadienis)

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| 09:30–11:00 | **T0:** `aibe` stulpelis · `zyma` · `--tik-vertinti` · `slenkstis --taikyti test` | Paleidus `test`, `val` eilutės **išlieka** | **P0** |
| 11:00–11:30 | **T0:** delsa CPU · `class_weight` žodynu · RF `min_samples_leaf` · MLP įsikelia | Visi keturi modeliai įsikelia | **P0** |
| 11:30–12:00 | **T1:** protokolo 12 punktų peržiūra; laukiamų lentelių sąrašas | ⭐ **Prieš pirmą `test` paleidimą** | **P0** |
| *12:00–12:30* | *Pietūs* | | |
| 12:30–13:00 | **T2:** `--vertinimas test --tik-vertinti` (12 paleidimų) | +12 eilučių `aibe=test` | **P0** |
| 13:00–13:30 | **T3:** `delsa.bat` — keturi modeliai vienu paleidimu, CPU | `veikimas.tex` | **P0** |
| 13:30–14:45 | **T4 + T8:** sumaišymo matricos, per-klasę lentelė su *n*, du paveikslai | `pav:sumaisymas`, `pav:fpr_kreives` | **P0** |
| 14:45–16:00 | **T5:** trys permokymai be klasės (fone) + `tab:nematytos` | Autokoderis **nepermokomas** (1.2) | **P0** |
| 16:00–16:30 | **T6:** dvejetainė ir 34 klasių formuluotės | 2 eilutės; palyginimas su literatūra | P1 |
| 16:30–17:00 | **T7:** penkios patikimumo patikros | Visos penkios užrašytos | **P0** |
| 17:00–18:30 | **T9:** 5.2–5.7 tekstas aplink lenteles | ~5 psl. | **P0** |
| 18:30–18:50 | **T9:** 5.1 ir 5.8 — **rašomi paskutiniai** | ~0,9 psl. | P1 |
| 18:50–19:15 | `build.ps1` · commit · `DARBO_ZURNALAS.md` · `STRUKTURA.md` | Kompiliuojasi | **P0** |

**Dienos pabaigos minimumas:** `test` rezultatai gauti ir įrašyti **nesunaikinus `val`**, nematytų klasių lentelė užpildyta, PDF kompiliuojasi. Skyriaus tekstas gali persikelti į rugs. 10 d. rytą — **grafikas eina 6 dienomis į priekį.**

> **Ko į šią dieną nekelti:** SHAP, Isolation Forest, titulinis puslapis, `houichi` eilutė. Visos pigios ir todėl viliojančios, bet šiandien yra vienas dalykas, kurio negalima pakartoti — **pirmas prėjimas per `test`.**

---

## 7. Priėmimo kriterijai

- [ ] ⭐ **`aibe` stulpelis yra `SCHEMA` ir `RAKTAS`;** paleidus `test`, 21 `val` eilutė **išlieka** — patikrinta `wc -l` prieš ir po
- [ ] `sumaisymas_*.csv` vardai skiria `val` ir `test`
- [ ] `--tik-vertinti` įkelia išsaugotą modelį; **12 `test` paleidimų trunka minutes, ne pusvalandį**
- [ ] `slenkstis --taikyti test` *τ* **skaito iš failo**; perskaičiavimo galimybės tame režime nėra
- [ ] Keturi modeliai **įsikelia** (RF 670 MB! MLP `.keras`) — patikrinta paleidimu, ne pažymėta
- [ ] ⭐ **Protokolo 12 punktų ir laukiamų lentelių sąrašas užrašytas PRIEŠ pirmą `--vertinimas test`**
- [ ] `test` paliesta **vienu prėjimu**; prognozių masyvai išsaugoti paveikslams
- [ ] *τ* imtas iš `val`; ant `test` neperrinktas nė vienam modeliui
- [ ] Veikimo rodikliai — visi keturi **vienu paleidimu, CPU**; GPU skaičiai į lentelę nepatenka
- [ ] Per-klasę lentelėje yra **_n_ stulpelis**; `UPLOADING_ATTACK` eilutėje matyti 179
- [ ] `tab:nematytos`: trys klasės, keturi stulpeliai; **autokoderio nepermokymas pagrįstas tekste**
- [ ] Nematytos klasės vertinamos **dvejetainiu klausimu**; `BruteForce` ištuštėjimas įvardytas
- [ ] Penkios patikimumo patikros atliktos; **4-osios rezultatas užrašytas, koks bebūtų**
- [ ] Skirtumas nuo `almahaqeri2026gradient` paaiškintas **trimis išmatuotais veiksniais**, ne prielaidomis
- [ ] macro-F1 0,85–0,90 nepasiekimas **įvardytas atvirai**, su priežastimis
- [ ] Paveikslai **generuojami** skriptu; PDF data išjungta
- [ ] **5.8 poskyryje matomas užduoties rezultatas** *(vadovo vienintelis kriterijus)*
- [ ] Automatinė patikra: kirilica 0 · `\SI`/`\num` argumentai sutikrinti · `\section` skyriaus faile 0 · dubliuotų `\label` nėra
- [ ] Kompiliuojasi: **0 klaidų, 0 neišspręstų nuorodų**
- [ ] `uzduotis_04_planas.md` permokymo žyma pataisyta · `DARBO_ZURNALAS.md` · `STRUKTURA.md` · commit

---

## 8. Rizikos

| Rizika | Ženklas | Veiksmas |
|---|---|---|
| ⭐⭐ **`test` paleidimas sunaikina `val` rezultatus** | `rezultatai.csv` po paleidimo turi 12 eilučių vietoj 33 | **T0 taisymas Nr. 1 prieš bet ką kitą.** Prieš pirmą paleidimą — `git commit` su esamu CSV |
| ⭐ **`test` liečiamas kelis kartus, sprendimai priimami matant rezultatą** | Antras `test` paleidimas kitais parametrais | 1.1 sk. trijų pakopų tvarka. **Dienos metodinė ašis** |
| **Random Forest neįsikelia į atmintį** | `joblib.load` išėjimo kodas 137 | T0 **prieš** ciklą. Nepavykus — RF vertinamas mokymo mašinoje, ir tai įvardijama |
| **MLP `.keras` neįsikelia** | `quantization_config` klaida | T0; blogiausiu atveju permokymas (50 s) |
| `test` rezultatai geresni už `val` | Tikslumas > 99,78 % | **Nutekėjimo požymis.** Penkios patikros prieš rašant |
| Nematytų klasių testas duoda 0 % visiems | Nė viena eilutė nepažymėta | **Rašoma, kaip yra** — tai atsakymas į zero-day klausimą, ne nesėkmė |
| Autokoderis atrodo bevertis | macro-F1 0,22 | Jis vertinamas **ne macro-F1**, o aptikimo dalimi ties FPR biudžetu ir nematytose klasėse |
| Skyrius per plonas | < 4 psl. | Perviršis čia **nėra** problema — problema priešinga |
| Aplinkos problemos | Kompiliavimo ar importo klaida | **Po pirmo nepavykusio taisymo — ne antras spėjimas, o duomenys** |

---

## 9. Kas keliauja į 6 užduotį

- **Suvestinė lentelė turės dvi dalis** — prižiūrimi 8 kategorijų formuluotėje, autokoderis dvejetainėje. Numatyta 2.8 poskyryje, įgyvendinta matricos sandaroje ir kode; 6 skyriuje — ketvirtas to paties dalyko pavidalas
- **Palyginimas tik ties suderintu FPR.** Rikiuotė ties argmax kitokia — savarankiškas radinys
- **SHAP** — požymių svarba (`mohale2025xai`)
- **Kompromisų ašys:** tikslumas vs. dydis (XGBoost 47 MB prieš RF **670 MB**), tikslumas vs. interpretuojamumas, prižiūrimas vs. neprižiūrimas
- **Nematytų klasių rezultatas yra autokoderio hipotezės verdiktas** — 3 užduotyje jis įtrauktas dėl funkcinio reikalavimo, ne dėl balo; 6 skyriuje reikia pasakyti, ar reikalavimas pasiteisino
- ⭐ **Sprendimų matrica prognozavo XGBoost 4,70 · RF 3,55 · MLP 3,25; matavimas ties biudžetu davė tą pačią tvarką.** Tai **prognozė, pateikta prieš eksperimentą ir pasitvirtinusi** — verta atskiro poskyrio
- **Reikšmingumo formuluotė:** skirtumas tikras tik viršijęs paleidimų sklaidą; formalus testas neatliekamas ir kodėl

---

## 10. Neuždaryti likučiai *(rezervo laikas, ne P0)*

- [ ] ⚠️ **Titulinio puslapio fakultetas ir vadovas** — atviras nuo rugs. 1 d., reikia sprendimo
- [ ] `houichi2025smartcity` eilutė iš `tab:susije` — terminas praėjo, išimtina
- [ ] `praktikos_planas.md` 4 sk. — pažymėti, kad 26–34 psl. norma neegzistuoja
- [ ] `rezultatai/apmokyti/metadata.json` tuščias — pildyti arba išbraukti iš `STRUKTURA.md`
- [ ] Ištrinti: `bibtestas.tex` · `*.bak` · `src/modeliai/cnn.py`
- [ ] `duomenys/raw/archive.zip` — ~2,3 GB atgaunama
- [ ] `ataskaita/skyriai/ciciot2023_pozymiai.md` → perkelti į `duomenys/`
- [ ] `claude/` — `uzduotis_01_planas.md`, `praktikos_planas.md`, `kontekstas.md` tebėra tik Claude projekte
