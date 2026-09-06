# 4 UŽDUOTIS — DI pagrįsto aptikimo sprendimo kūrimas

**Tikslų planas**
**Sudaryta:** 2026 m. rugsėjo 6 d.
**Vykdymas:** rugsėjo 7–9 d. (pirmad.–trečiad.); pradiniame plane — rugs. 9–14 d.
**Rezultatas:** veikianti eksperimentų grandinė, keturi apmokyti modeliai, `rezultatai/rezultatai.csv` su tikrais skaičiais, prototipas su vizualizacija, `ataskaita/skyriai/04_sprendimas.tex`

---

## 0. Būklė prieš pradedant — patikrinta, ne perimta iš užrašų

Ši užduotis yra priešingoje padėtyje nei trečioji. Ten didžioji dalis turinio jau buvo sugeneruota; čia **beveik nieko nėra**, o tai, kas laikoma paruošta, dviejose vietose neatitinka užrakinto protokolo.

**Patikrinta rugsėjo 6 d. realiame aplanke, ne iš `STRUKTURA.md` žymų.**

| Ko 4 užduočiai reikia | Būklė | Kur |
|---|---|---|
| Eksperimento protokolas (24 punktai) | ✅ **Užrakintas** — tai šios užduoties specifikacija | `uzduotis_03_planas.md` 5 sk.; `03_parinkimas.tex` 3.6 |
| Metodų ketvertas | ✅ RF, XGBoost, MLP, autokoderis | `03_parinkimas.tex` 3.7 |
| Duomenys diske | ✅ **63 failai, 8,7 GB** `duomenys/raw/archive/` | — |
| Etikečių žodynas | ✅ **34/34 patikrinta prieš realias etiketes** | `src/duomenys/etiketes.py` |
| Aplinkos patikra | ✅ `ikelimas.py patikra` veikia | — |
| Imtis (`imtis.parquet`) | ⬛ **Nėra.** `duomenys/processed/` tuščias | ⚠️ **T1** |
| Skaidymo indeksai | ⬛ Nėra | ⚠️ **T3** |
| `pozymiai.py` · `balansavimas.py` | ⬜ **0 baitų** | ⚠️ **T2, T4** |
| `bazinis.py` · modeliai | ⬜ **0 baitų** visi keturi | ⚠️ **T5** |
| `paleisti.py` | ⬜ **0 baitų** | ⚠️ **T6** |
| Konfigūracijos | ⬜ **0 baitų** abi (`random_forest.yaml`, `autoencoder.yaml`) | ⚠️ **T6** |
| `rezultatai.csv` | ⬜ **0 baitų** | ⚠️ **T6** |
| `04_sprendimas.tex` | ⬜ **0 baitų** | **T8** |

**Paskutinis commit — rugs. 3 d. (`96ef95a`).** Rugsėjo 4–5 d. nedirbta. Grafikas vis tiek eina **5 dienomis priekyje** pradinio plano, ir visa ta atsarga dabar atitenka būtent šiai užduočiai — taip, kaip ir buvo numatyta.

---

## 1. Trys neatitikimai, rasti peržiūrint — juos reikia uždaryti pirma ⚠️⭐

Visi trys yra to paties tipo klaida, kuri darbe kartojasi jau ketvirtą kartą: **būklė užrašyta neatidarius failo.** Rugsėjo 2 d. tai buvo duomenų aprašas, sudarytas neatidarius duomenų; rugsėjo 3 d. — priėmimo kriterijus, parašytas nepažiūrėjus į `.aux`. Šįkart — trys priėmimo kriterijai, pažymėti atliktais nepažiūrėjus į kodą.

### 1.1. `rezultatai.csv` schema su `i_latex.py` **nesuderinta** ⚠️⚠️

3 užduoties priėmimo kriterijus teigia: *„`rezultatai.csv` stulpelių schema užrašyta ir **suderinta su `i_latex.py`**“.* Sutikrinus failus paaiškėjo, kad tai netiesa.

| Protokolo 24 punktas | `i_latex.py` `STULPELIAI` | Sutampa? |
|---|---|---|
| `modelis` | `modelis` | ✅ |
| `accuracy` | `accuracy` | ✅ |
| `fpr` | `fpr` | ✅ |
| `macro_f1` | `f1_macro` | ❌ **kitas pavadinimas** |
| — | `precision_macro`, `recall_macro` | ❌ **protokole jų nėra** |
| `inferencija_us` | `inferencijos_ms` | ❌ **kitas vardas ir kitas vienetas** |
| `formuluote`, `seed`, `weighted_f1`, `pr_auc`, `roc_auc`, `mcc`, `mokymo_laikas_s`, `modelio_dydis_mb`, `konfig`, `data` | — | ❌ **skripte jų nėra** |

Sutampa **trys stulpeliai iš penkiolikos.** Paleistas su protokolo schema `i_latex.py` mestų `SystemExit: CSV trūksta stulpelių`.

**Sprendimas: perrašomas `i_latex.py`, ne protokolas.** Protokolas užrakintas ir kiekvienas jo stulpelis turi pagrindimą (macro-F1 — pagrindinė metrika, PR-AUC — stabilesnė prie 84:1, `inferencija_us` — mikrosekundės, nes XGBoost delsa milisekundėmis būtų 0,004). Skriptas rašytas rugsėjo 1 d., kai nieko iš to dar nebuvo nuspręsta.

⭐ **Kartu keičiasi ir skripto vaidmuo.** 15 stulpelių lentelė į puslapį netelpa, o `rezultatai.csv` turi 3 seed'ų eilutes kiekvienam modeliui. Vadinasi, `i_latex.py` nebėra „CSV → lentelė“, o **agregavimo žingsnis**: grupuoja pagal `modelis` + `formuluote`, skaičiuoja vidurkį ± std per seed'us ir išveda **du** failus — `lenteles/rezultatai.tex` (pagrindinės metrikos, 5 užd.) ir `lenteles/veikimas.tex` (delsa, mokymo laikas, dydis). Tai vis dar penkios minutės dabar arba pusdienis rugsėjo 12 d.

### 1.2. `ikelimas.py` neįgyvendina užrakinto protokolo ⚠️

Kode: `FRAKCIJA = 0.05`, `MIN_EILUCIU = 5000`. Protokole: **riba 100 000 eilučių klasei, retos klasės imamos visos.**

Tai ne tas pats ir duoda kitokią imtį:

| | `ikelimas.py` dabar | Protokolas |
|---|---|---|
| Didžiausia klasė (`DDOS-ICMP_FLOOD`, 6,89 mln.) | 5 % = **344 500** | riba **100 000** |
| Reta klasė (`UPLOADING_ATTACK`, 1 196) | max(59, 1 196) = **1 196** | **1 196** (visos) |
| Disbalansas imtyje | ~288:1 | **84:1** |

Retoms klasėms rezultatas sutampa, gausioms — ne. **Proporcinga frakcija disbalanso nemažina** (jis lieka toks pat, koks buvo), o būtent disbalanso sumažinimas nuo 5 764:1 iki 84:1 buvo pusė argumento, kodėl riba 100 000 pasirinkta.

Kartu kode nėra: **dublikatų šalinimo**, `dropna(subset=["Label"])`, `replace([inf,-inf], nan)`, skaidymo išsaugojimo. Visa tai aprašyta `duomenys/README.md` ir protokole, bet **kode neegzistuoja**.

**Failo vardas taip pat skiriasi:** kodas rašo `ciciot2023_imtis.parquet`, `STRUKTURA.md` žada `imtis.parquet`. Suvienodinti į **`imtis.parquet`** (trumpesnis, aplanko vardas jau sako, kokie tai duomenys).

### 1.3. Dublikatų matavimo skripto nėra ⚠️

33,1 % dublikatų ir ~95 % teorinė riba yra **stipriausi darbo radiniai** — jais remiasi 3, 5 ir 6 skyriai. Bet `rezultatai/darbiniai/` juos pagrindžiančio failo nėra: yra tik `klasiu_pasiskirstymas.txt`, `metodu_apzvalga.md` ir `sprendimu_matrica.csv`. Skaičiai gauti ad hoc ir **neatkartojami**.

**Tai neleistina būklė teiginiui, kuris ataskaitoje pavadintas atskaitos tašku.** T1 turi jį atkurti kaip skriptą, o rezultatą įrašyti į failą — lygiai taip, kaip `sprendimu_matrica.csv` yra vienintelis balų šaltinis.

> **Bendra pamoka, kurią verta užrašyti dabar:** priėmimo kriterijus, kurį pažymiu atliktu nepaleidęs ar neatidaręs failo, yra **spėjimas apie savo paties darbą**. Tai jau ketvirtas to paties tipo atvejis, ir visi keturi rasti tik po to, kai kas nors juos sutikrino. **Nuo šiol kriterijus, kurio patikra yra viena komanda, žymimas tik po tos komandos.**

---

## 2. Konkretūs tikslai

| Nr. | Tikslas | Išmatuojamas rezultatas | Prior. |
|---|---|---|---|
| **T0** | Uždaryti tris neatitikimus (1 sk.) + likučius | `i_latex.py` perrašytas; `ikelimas.py` atitinka protokolą; `imtis.parquet` vardas suvienodintas | **P0** |
| **T1** | ⭐ **Įkėlimo grandinė:** valymas → dublikatai → imtis | `duomenys/processed/imtis.parquet` + `rezultatai/darbiniai/imties_ataskaita.md` su **realiais** skaičiais | **P0** |
| **T2** | Požymių paruošimas | `pozymiai.py`: 39 → **36** požymiai, šalinama sąrašu; normalizavimas `fit` tik ant `train` | **P0** |
| **T3** | Skaidymas 70/15/15 + nutekėjimo patikros | `skaidymas.npz`; patikra, kad `train ∩ test = ∅` | **P0** |
| **T4** | Balansavimas | `balansavimas.py`: `class_weight`/`scale_pos_weight` + SMOTE abliacijai | P1 |
| **T5** | ⭐ **Keturi modeliai su vienoda sąsaja** | `bazinis.py` + `random_forest.py`, `xgboost.py`, `mlp.py`, `autoencoder.py` | **P0** |
| **T6** | Eksperimentų infrastruktūra | `paleisti.py` + 4 YAML konfigai → `rezultatai.csv` protokolo schema | **P0** |
| **T7** | ⭐ **Kontrolinis taškas: pilnas ciklas** | RF, 1 seed, nuo `imtis.parquet` iki eilutės `rezultatai.csv` | **P0** |
| **T8** | Prototipas su vizualizacija | Streamlit: CSV eilutės → požymiai → inferencija → signalai + grafikai | P1 |
| **T9** | `04_sprendimas.tex` | 7 poskyriai, ~5–6 psl. | **P0** |

**Ne šios užduoties tikslai:** hiperparametrų derinimas visiems modeliams (tik jei liks laiko — T6 numatytas Random Search yra 5 užduoties darbo dalis), SHAP (→ 6 užd.), Isolation Forest (→ jei liks laiko), INT8 kvantavimas (→ tik jei MLP netikėtai nugalės ansamblius).

---

## 3. T1 — įkėlimo grandinė ir jos vienintelė reali techninė problema ⭐⭐

### 3.1. Konfliktas: „dublikatai šalinami prieš imtį“ nesuderinamas su RAM

Protokolo 9 punktas sako šalinti tikslius dublikatus **prieš** skaidymą ir prieš imties sudarymą. Priežastis teisinga: dublikatai pasiskirstę netolygiai (potvynio klasėse 32–50 %, retose 0 %), todėl šalinimas **keičia klasių proporcijas**, o imtis, sudaryta prieš šalinimą, jau būtų iškreipta.

**Bet `df.duplicated()` ant viso rinkinio neįmanomas.** 45,0 mln. eilučių × 39 skaitiniai požymiai `float64` ≈ **14 GB** vien duomenų, neskaičiuojant `pandas` papildomų kopijų palyginimo metu. Nešiojamame kompiuteryje tai baigsis `MemoryError` arba valandų trukmės swap'inimu.

### 3.2. Sprendimas: dublikatai šalinami **klasės viduje, srautu** ⭐

Trys pastebėjimai, kurie kartu problemą panaikina:

1. **Dublikatas visada yra tos pačios klasės viduje.** Eilutė su ta pačia požymių aibe ir kita etikete yra ne dublikatas, o prieštaringa etiketė (55 440 vektorių) — ir protokolas aiškiai sako tokias **palikti**. Vadinasi, dublikatų paieškos niekada nereikia daryti per visą rinkinį iš karto.
2. **Palyginti reikia ne eilučių, o jų maišos.** `pd.util.hash_pandas_object` duoda `uint64` vienai eilutei: 45 mln. × 8 B = **360 MB** vietoj 14 GB. Susidūrimo tikimybė prie 45 mln. eilučių ir 64 bitų yra apie 5·10⁻⁸ — nereikšminga, bet **įvardijama ataskaitoje**, nes tai apytikslis, o ne tikslus metodas.
3. ⭐ **Gausioms klasėms tvarka nesvarbi.** Klasė, kurioje po dublikatų šalinimo lieka daugiau nei 100 000 eilučių, vis tiek bus apkirpta iki 100 000 — todėl jai „prieš“ ir „po“ duoda **tą patį rezultatą**. Tvarka svarbi tik toms klasėms, kurios po šalinimo nukrenta **žemiau ribos**. Jų nedaug, ir kaip tik jos yra tos, kurioms atsakymas turi būti tikslus.

**Iš to seka algoritmas — vienas praėjimas per 63 failus:**

```
kiekvienam failui, gabalais po 500 000 eilučių:
    dropna(subset=["Label"])            # nutrūkusios eilutės — pirmos
    Label -> strip().upper()            # BENIGN, ne BENIGNTRAFFIC
    replace([inf, -inf], nan).dropna()  # 991 eilutė su Rate = Infinity
    h = hash_pandas_object(eilutė)      # uint64
    kiekvienai klasei:
        naujos = h, kurių dar nėra matytų[klasė] rinkinyje
        matytų[klasė] |= naujos
        jei surinkta[klasė] < 100 000:  imti eilutes iš naujų
```

**Rezultatas:** viena eiga, dublikatai pašalinti klasės viduje, riba pritaikyta, `random_state` fiksuotas. Atmintis — maišos rinkiniai, ne eilutės.

⚠️ **Vienas nukrypimas nuo protokolo, kurį reikia įvardyti atvirai:** eilutės imamos ta tvarka, kokia jos yra failuose, o ne atsitiktinai iš viso rinkinio. Jei CICIoT2023 failai sudaryti chronologiškai, riba 100 000 paims ankstyviausias eilutes. **Apsauga:** iš kiekvienos klasės surenkama iki 150 000 unikalių eilučių, o galutinė 100 000 imtis atrenkama atsitiktinai iš jų — 50 % atsargos už ~0,5 GB tarpinės atminties.

### 3.3. Ką T1 privalo išvesti į `rezultatai/darbiniai/imties_ataskaita.md`

Šie skaičiai eina tiesiai į 4 ir 5 skyrius, todėl jie yra T1 produktas, ne šalutinis efektas:

- eilučių prieš valymą / po valymo / po dublikatų šalinimo / imtyje;
- **faktinis dublikatų procentas** visame rinkinyje (iki šiol turime tik 33,1 % iš 1,9 mln. imties);
- klasių pasiskirstymas imtyje ir **faktinis disbalanso santykis** (laukiama ~84:1);
- kiek klasių po šalinimo nukrito žemiau 100 000 ribos;
- `BENIGN` eilučių skaičius imtyje — **autokoderio mokymo aibės dydis**;
- ⭐ **patikslinta teorinė tikslumo riba** darbinėje imtyje (protokolas žada ją tikslinti; dabar ~95 % iš 1,9 mln.).

> **Jei patikslinta riba stipriai skirsis nuo 95 %, tai keičia 3 skyriaus tekstą.** Protokolas tokį tikslinimą numatė, tad tai ne klaida — bet pakeitimas turi būti padarytas iš karto, ne rugsėjo 15 d.

---

## 4. T5 — vienoda sąsaja yra brangiausias sprendimas šioje užduotyje ⭐

Nuo `bazinis.py` kontrakto tiesiogiai priklauso, ar 6 užduotis bus vienas ciklas, ar keturios dienos rankų darbo. Jis fiksuojamas **prieš** rašant pirmą modelį.

```python
class Modelis(ABC):
    vardas: str                  # -> rezultatai.csv "modelis"
    priziurimas: bool            # lemia, kaip modelis vertinamas

    def fit(X_train, y_train, X_val, y_val) -> None
    def predict(X) -> np.ndarray          # klasių etiketės
    def predict_proba(X) -> np.ndarray    # tikimybės arba anomalijos įvertis
    def issaugoti(kelias) -> None         # + metadata.json su versija
    def dydis_mb() -> float
```

⚠️ **Autokoderis į šį kontraktą telpa tik su išlyga, ir ją reikia numatyti dabar.** Jis neturi klasių: `predict_proba` grąžina atkūrimo paklaidą, o `predict` — dvejetainį sprendimą pagal slenkstį, kalibruotą ant `val` `BENIGN` dalies (95-asis procentilis). Todėl:

- `predict_proba` kontrakte apibrėžiamas kaip **„įvertis, kurio didesnė reikšmė reiškia didesnę atakos tikimybę“**, ne kaip tikimybių matrica;
- `priziurimas = False` yra tas laukas, pagal kurį `paleisti.py` žino, kad šiam modeliui macro-F1 per 8 kategorijas skaičiuoti negalima.

Tai ta pati palyginimo asimetrija, numatyta rugsėjo 2 d. (2.8 poskyris) ir įgyvendinta rugsėjo 3 d. matricos sandaroje. **Čia ji įgyvendinama trečią kartą — kode.** Jei ji nebus kontrakte, ji išlįs rugsėjo 15 d. kaip `ValueError` viduryje eksperimentų ciklo.

**Papildomas tvarkymas:** `src/modeliai/cnn.py` (0 B) nebeatitinka ketverto — **ištrinti**; sukurti `xgboost.py` ir `mlp.py`.

⚠️ **Failo vardas `xgboost.py` `src/modeliai/` aplanke uždengtų biblioteką `import xgboost`**, jei kur nors būtų reliatyvus importas. Saugiau — **`gradientinis.py`** arba `xgb.py`. Pigi klaida, kurią vėliau būtų sunku diagnozuoti.

---

## 5. Skyriaus `04_sprendimas.tex` struktūra

```
4. DI pagrįsto aptikimo sprendimo kūrimas        (taikinys ~5,5 psl.)
   4.1. Sprendimo architektūra                          (~0,7 psl.)
        --> pav: srautas -> pozymiai -> modelis -> signalas
        - diegimo vieta: krastinis sliuzas (1 sk. isvada)
   4.2. Duomenu paruosimas                              (~1,2 psl.)
        --> tab:imtis (klase | pilnas | po dublikatu | imtyje)
        - valymo tvarka; dublikatu salinimas klases viduje
        - PATIKSLINTA teorine riba
   4.3. Pozymiai                                        (~0,6 psl.)
        - 39 -> 36 sarasu; kodel ne koreliacijos filtras
   4.4. Modeliu realizacija ir bendra sasaja            (~1,0 psl.)
        - kontraktas; autokoderio islyga
   4.5. Klasiu disbalanso sprendimas                    (~0,5 psl.)
   4.6. Eksperimentu infrastruktura ir prototipas       (~1,0 psl.)
        --> pav: prototipo ekrano nuotrauka
        - konfigas -> paleidimas -> rezultatai.csv -> LaTeX
   4.7. Apibendrinimas                                  (~0,3 psl.)
        - MATOMAS uzduoties rezultatas
```

**Apimties taikinys nemažinamas, ir tai sąmoningas pokytis.** 1–3 skyriuose taikinys buvo stabdis (+90 %, +62 %, +11 % perviršio). Čia jis yra **grindys**: vienintelė reali apimties rizika, likusi po rugsėjo 3 d., yra ~23 psl. teorijos prieš plonus 4–6 skyrius. Vadovui rūpi, kas sukurta ir išmatuota.

⚠️ **Du paveikslai — pirmi visame darbe.** `paveikslai/` aplankas tuščias, `\includegraphics` niekur nenaudotas, taigi nepatikrintas. **Taisyklė „naudoti tik tai, kas darbe jau įrodyta veikiant“ čia neišvengiamai laužoma** — todėl pirmas paveikslas įdedamas **anksti** (T7 dieną, ne T9), kad kompiliavimo problema, jei tokia bus, iškiltų turint laiko.

---

## 6. Laiko biudžetas — rugsėjo 7–9 d.

### Rugsėjo 7 d. (pirmadienis) — duomenų grandinė

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| 09:00–09:45 | **T0:** `i_latex.py` perrašymas (agregavimas + 2 lentelės); `imtis.parquet` vardo suvienodinimas | Skriptas atitinka protokolo schemą | **P0** |
| 09:45–11:30 | **T1:** `ikelimas.py` perrašymas — valymas + maišos + riba 100 000 | Skriptas paruoštas, paleidžiamas | **P0** |
| 11:30–13:00 | **T1:** paleidimas ant 63 failų *(fone; tuo metu — T2 kodas)* | `imtis.parquet` + `imties_ataskaita.md` | **P0** |
| 13:00–13:40 | *Pietūs* | | |
| 13:40–14:40 | **T2:** `pozymiai.py` — 36 požymiai, normalizavimas | Modulis + patikra | **P0** |
| 14:40–15:30 | **T3:** `skaidymas.npz` + nutekėjimo patikros | Indeksai išsaugoti; `train ∩ test = ∅` | **P0** |
| 15:30–16:15 | ⭐ **Realių skaičių sutikrinimas su 3 skyriumi** — jei dublikatų % ar teorinė riba skiriasi, taisomas `03_parinkimas.tex` | 3 sk. atitinka duomenis | **P0** |
| 16:15–17:00 | **T4:** `balansavimas.py` | Modulis | P1 |
| 17:00–17:30 | `build.ps1` · commit · žurnalas | Kompiliuojasi | **P0** |

**Dienos minimumas:** `imtis.parquet` ir `skaidymas.npz` egzistuoja, skaičiai užrašyti.

### Rugsėjo 8 d. (antradienis) — modeliai ir pirmas ciklas

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| 09:00–10:00 | **T5:** `bazinis.py` kontraktas + `random_forest.py` | Kontraktas fiksuotas | **P0** |
| 10:00–11:00 | **T6:** `paleisti.py` + `random_forest.yaml` | Konfigas → mokymas → CSV eilutė | **P0** |
| 11:00–12:00 | ⭐ **T7: KONTROLINIS TAŠKAS** — RF, 1 seed, pilnas ciklas | Pirma eilutė `rezultatai.csv`; `i_latex.py` sugeneruoja lentelę | **P0** |
| 12:00–13:00 | **T5:** `gradientinis.py` (XGBoost) + konfigas | Antras modelis | **P0** |
| 13:00–13:40 | *Pietūs* | | |
| 13:40–14:40 | **T5:** `mlp.py` + konfigas | Trečias modelis | **P0** |
| 14:40–16:00 | **T5:** `autoencoder.py` — slenkstis ant `val` `BENIGN` | Ketvirtas modelis | **P0** |
| 16:00–17:00 | Visų keturių paleidimas su 1 seed'u | 4 eilutės `rezultatai.csv` | **P0** |
| 17:00–17:30 | Pirmas paveikslas į `04_sprendimas.tex` — **anksti, dėl kompiliavimo rizikos** | `\includegraphics` veikia | **P0** |
| 17:30–18:00 | commit · žurnalas | | **P0** |

**Dienos minimumas:** keturi modeliai duoda metrikas; `\includegraphics` patikrintas.

### Rugsėjo 9 d. (trečiadienis) — prototipas ir skyrius

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| 09:00–11:00 | **T8:** prototipas su vizualizacija (Streamlit) | Veikia lokaliai | P1 |
| 11:00–11:30 | Ekrano nuotrauka į `paveikslai/` | PNG/PDF ataskaitai | P1 |
| 11:30–13:00 | **T9:** 4.2–4.6 tekstas aplink lenteles ir paveikslus | ~4 psl. | **P0** |
| 13:00–13:40 | *Pietūs* | | |
| 13:40–14:40 | **T9:** 4.1 ir 4.7 — **rašomi paskutiniai** | ~1 psl. | **P0** |
| 14:40–15:30 | Automatinė patikra (kirilica · `\SI`/`\num` · `\section` · `\label`) + `build.ps1` | 0 klaidų | **P0** |
| 15:30–16:30 | 3 seed'ai visiems modeliams *(fone)* | 12 eilučių `rezultatai.csv` | P1 |
| 16:30–17:30 | Likučiai (7 sk.) · commit · žurnalas · `STRUKTURA.md` | | P1 |

> **Ko į šias tris dienas NEKELTI.** SHAP, Isolation Forest, kvantavimas, hiperparametrų derinimas visiems keturiems. Visi jie pigūs atrodyti ir brangūs padaryti, o šios užduoties matas yra vienas: **ar rugsėjo 9 d. vakare `rezultatai.csv` turi tikrus skaičius.**

---

## 7. Priėmimo kriterijai

**Kiekvienas iš jų tikrinamas komanda, ne atmintimi** (žr. 1 sk. pamoką).

- [ ] `python -m src.eksperimentai.i_latex` praeina su protokolo schemos CSV *(patikra: paleisti)*
- [ ] `duomenys/processed/imtis.parquet` egzistuoja; eilučių skaičius įrašytas ataskaitoje
- [ ] `imties_ataskaita.md` turi **visus šešis** 3.3 skyriuje išvardytus skaičius
- [ ] **Faktinis dublikatų procentas** išmatuotas visame rinkinyje, ne imtyje; skriptas išsaugotas
- [ ] **Teorinė tikslumo riba patikslinta**; jei skiriasi nuo 95 %, `03_parinkimas.tex` pataisytas **tą pačią dieną**
- [ ] `skaidymas.npz` išsaugotas; patikrinta, kad `train`, `val`, `test` indeksai nesikerta
- [ ] Normalizavimo `fit` iškviestas **tik** ant `train` — patikrinta kode, ne prielaida
- [ ] SMOTE ir klasių svoriai taikomi **tik** `train`
- [ ] Visi keturi modeliai realizuoja tą patį `bazinis.py` kontraktą; `priziurimas` laukas užpildytas
- [ ] Autokoderio slenkstis kalibruotas ant `val` `BENIGN`, **ne** ant `test`
- [ ] `rezultatai.csv` turi **15 protokolo stulpelių**, ne mažiau
- [ ] `test` aibė nė karto nepaliesta iki 5 užduoties — patikra: `paleisti.py` jos neįkelia be `--vertinimas` vėliavos
- [ ] `\includegraphics` veikia; PDF kompiliuojasi (0 klaidų, 0 neišspręstų nuorodų)
- [ ] Automatinė patikra: kirilica 0 · `\SI`/`\num` argumentai sutikrinti · `\section` skyriaus faile 0 · dubliuotų `\label` nėra
- [ ] 4.7 poskyryje **matomas užduoties rezultatas** — kas sukurta ir kas išmatuota
- [ ] `DARBO_ZURNALAS.md` ir `STRUKTURA.md` atnaujinti; commit'ai su prasmingomis žinutėmis

---

## 8. Rizikos

| Rizika | Ženklas | Veiksmas |
|---|---|---|
| ⭐ **Dublikatų šalinimas nesutelpa į atmintį** | `MemoryError` arba swap'inimas | Maišos vietoj eilučių, klasės viduje, srautu (3.2). **Jei ir tai lūžta** — maišos rašomos į diską po klasę |
| ⭐ **Patikslinta teorinė riba stipriai skiriasi nuo 95 %** | `imties_ataskaita.md` rodo kitą skaičių | Protokolas tikslinimą numatė. Taisyti `03_parinkimas.tex` **tą pačią dieną**, ne rugs. 15 d. |
| **T1 paleidimas trunka valandas** | 63 failai × 8,7 GB | Vienas praėjimas, `usecols` kur galima. Paleidžiama fone, tuo metu rašomas T2 kodas |
| **Autokoderis nesimoko** | Atkūrimo paklaida nesiskiria tarp `BENIGN` ir atakų | RF ir XGBoost jau duos rezultatą. Autokoderio nesėkmė yra **rezultatas**, ne blokuotė — 6 sk. tai atsakymas į zero-day hipotezę |
| **Vienodas kontraktas atsiranda per vėlai** | Antras modelis rašomas nežiūrint į `bazinis.py` | Kontraktas fiksuojamas **prieš** pirmą modelį (T5, 09:00) |
| **`\includegraphics` lūžta** | Pirmas paveikslas visame darbe | Įdedamas rugs. 8 d., ne 9 d. — turint dieną atsargos |
| **Prototipas suvalgo skyriaus laiką** | 13:00 rugs. 9 d. vis dar derinamas Streamlit | T8 yra **P1**. Po 11:30 jis stabdomas, koks bebūtų — skyrius svarbiau |
| **Skyrius išplinta ketvirtą kartą** | > 6,5 psl. | Šįkart perviršis **nėra problema** (žr. 5 sk.). Problema būtų priešinga |
| Aplinkos problemos | Kompiliavimo ar `conda` klaida | Ta pati taisyklė: **po pirmo nepavykusio taisymo — ne antras spėjimas, o duomenys** |

---

## 9. Likučiai — rezervo laikas

- [ ] ⚠️ **Titulinio puslapio fakultetas ir vadovas** — atviras nuo rugs. 1 d., reikia sprendimo (dokumentas Aineros vadovui, tad klausimas platesnis nei du laukai)
- [ ] `houichi2025smartcity` metrikos (Wiley 403) — **riba rugs. 8 d.**, po jos eilutė iš `tab:susije` išimama
- [ ] `praktikos_planas.md` 4 sk. — pažymėti, kad **26–34 psl. norma neegzistuoja** (žurnale pažymėta nuo rugs. 3 d., plane — ne)
- [ ] `bibtestas.tex` / `bibtestas2.tex` · `saltiniai.bib.bak` · `etiketes.py.bak` · `ikelimas.py.bak` — ištrinti
- [ ] `ataskaita/skyriai/ciciot2023_pozymiai.md` — **ne skyrius**, guli tarp `.tex` failų. Perkelti į `duomenys/`
- [ ] `src/modeliai/cnn.py` — ištrinti (nebeatitinka ketverto)
- [ ] `duomenys/raw/archive.zip` — **~2,3 GB** atgaunama ištrynus, CSV jau išpakuoti
- [ ] `claude/` aplanke tik du planai iš penkių; `uzduotis_01_planas.md`, `praktikos_planas.md`, `kontekstas.md` tebėra tik Claude projekte

---

## 10. Kas keliauja į 5 užduotį

Užsirašyti dabar, kad rugsėjo 10 d. nereikėtų atkurti:

- **`test` aibė iki tol neliesta.** Tai vienintelė taisyklė, kurią pažeisti lengviausia netyčia — vieną kartą „tik pažiūrėti“
- **3 seed'ai (42, 43, 44)** → vidurkis ± std. Skirtumas reikšmingas tik viršijęs paleidimų sklaidą (`dietterich1998tests`)
- **Nematytų klasių testas** — `DDOS-SLOWLORIS`, `RECON-PORTSCAN`, `DICTIONARYBRUTEFORCE`. **Privaloma 5 užd. dalis**, ne papildoma
- **Delsa matuojama gryna**, atskirai nuo lango sukaupimo; lyginama su **20–50 ms** šliuzo biudžetu
- **Realistinis taikinys — macro-F1 0,85–0,90**, ne 0,99. Aukštesnis už patikslintą teorinę ribą rezultatas reiškia nutekėjimą, ne sėkmę
- **Isolation Forest** — pigus etalonas autokoderiui, jei liks laiko
- **SHAP → 6 užduotis**, ne 5
