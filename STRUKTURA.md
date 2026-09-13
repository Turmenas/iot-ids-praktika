# Failų žemėlapis

Greita nuoroda: kur kas guli ir ką paleisti. Ilgas kontekstas — `DARBO_ZURNALAS.md`.

**Šaknis:** `D:\Ainera\iot-ids-praktika\`
**Atnaujinta:** 2026-09-13 — **ATASKAITA SURINKTA**: visos šešios užduotys, įvadas, išvados ir titulinis puslapis. **57 psl. (54 + bibliografija), 0 klaidų, 0 neišspręstų nuorodų, 0 `TODO`**. **`.bat` failai sunumeruoti paleidimo eile (01–14).** **Atkartojamumas patikrintas švarioje aplinkoje.** Liko tik neprivalomi likučiai
**Žymos:** ✅ turi turinį · ⬜ sukurtas, bet tuščias · ⬛ dar nesukurtas

---

## Šaknis

| Kelias | Kas tai |
|---|---|
| ✅ `DARBO_ZURNALAS.md` | Kasdienis žurnalas — **tik sprendimai, radiniai, pamokos** |
| ✅ `STRUKTURA.md` | Šis failas |
| ✅ `README.md` | Projekto apžvalga — **atnaujinta 09-13:** visos 6 užduotys ✅, rezultatas, pilna `.bat` paleidimo seka |
| ✅ `requirements.txt` · `requirements-lock.txt` | Priklausomybės. **Lock pergeneruotas 09-13** — 95 paketai; ankstesnis (09-01) neturėjo `streamlit`, tad prototipas švarioje aplinkoje nebūtų pasileidęs. ⚠️ PowerShell 5.1 `-Encoding utf8` rašo **su BOM**; `pip` jį nurija — patikrinta švariu diegimu 09-13 |
| ✅ `patikra.py` | Aplinkos patikra (bibliotekos + aplankai). **09-13:** pridėtos `PAPILDOMOS` — `streamlit` rodomas atskirai, nes jo trūkumas nėra klaida, bet turi būti matomas |
| ✅ `sutvarkyti.ps1` | ⭐ **Vienkartinis (09-13), atliktas:** ištrynė nebereikalingus failus, perkėlė `ciciot2023_pozymiai.md` į `duomenys\`, pašalino senus `.bat` vardus |
| ✅ `sutvarkyti_diska.ps1` | ⭐ **Vienkartinis (09-13):** ~4,2 GB — `archive.zip`, Random Forest ir 34 klasių modeliai, `_patikra\`, `__pycache__`. Kiekvienas įrašas turi pastabą, **kaip jį susigrąžinti**. `-Perziura` — peržiūra nieko nekeičiant |
| ✅ `_aplinka.bat` | ⭐ Bendra dalis visiems `.bat`: aktyvuoja `iot-ids`, **nutraukia darbą, jei aktyvi kita aplinka**, išjungia `%APPDATA%` paketų nutekėjimą |
| ✅ `01_patikra.bat` | Keturios patikros prieš mokymą (~1 min., į CSV nerašo) |
| ✅ `02_mokyti_viska.bat` | Visi 12 paleidimų **nuosekliai** + lentelių generavimas |
| ✅ `02a_mokyti_rf.bat` · `02b_mokyti_xgboost.bat` · `02c_mokyti_mlp.bat` · `02d_mokyti_autoencoder.bat` | Po vieną modelį × 3 seed'ai |
| ✅ `03_derinti.bat` | Hiperparametrų paieška — **protokolo 18 punktas** |
| ✅ `04_mokyti_derintus.bat` | Permokymas su suderintais parametrais (`*_derintas.yaml`) |
| ✅ `05_delsa.bat` | Delsos permatavimas CPU be permokymo |
| ✅ `06_slenkstis.bat` | ⭐ FPR biudžeto laikymasis **be permokymo** (naudoja išsaugotus modelius) |
| ✅ `07_prototipas.bat` | **T8** — Streamlit prototipas naršyklėje |
| ✅ `08_vertinti_test.bat` | ⭐ **5 užd. (09-09):** vienintelis prėjimas per `test`. Modeliai **nepermokomi** (`--tik-vertinti`); Random Forest — po vieną seed'ą. Tikrina `aibe` stulpelį prieš ir `val` eilučių skaičių po |
| ✅ `09_slenkstis_test.bat` | ⭐ **5 užd. (09-09):** *τ* imamas iš `val` ir taikomas `test`; išvestis į `*_test` failus. Protokolo **patikra Nr. 4** |
| ✅ `10_klaidos.bat` | ⭐ **5 užd. T4 (09-09):** per-klasę metrikos ir klaidų tipai. **`test` neatidaroma** — skaičiuojama iš išsaugotų sumaišymo matricų |
| ✅ `11_nematytos.bat` | ⭐ **5 užd. T5 (09-09):** trys permokymai be klasės; autokoderis **nepermokomas**. Prieš duomenų įkėlimą tikrina **modelių kontraktą** |
| ✅ `12_formuluotes.bat` | ⭐ **5 užd. T6 (09-09):** dvejetainė ir 34 klasių formuluotės palyginimui su literatūra. Mokymas ant `val`, tada `--tik-vertinti` ant `test` |
| ✅ `13_patikimumas.bat` | ⭐ **5 užd. T7 (09-09):** penkios patikimumo patikros. Trys būsenos: `PRAEJO` · `RADINYS` · `NEPRAEJO` |
| ✅ `14_palyginimas.bat` | ⭐ **6 užd. (09-09):** suvestinė ir požymių svarba. **Naujų matavimų nedaro** — `rezultatai.csv` po jo turi likti nepakitęs |
| ✅ `.gitignore` | Komentarai **tik** atskirose eilutėse |
| ✅ `.gitattributes` | Eilučių pabaigų normalizavimas |

## `claude\` — planavimo dokumentai

Atitinka Claude projekto dokumentų erdvę 1:1, kad sinchronizavimas būtų tiesioginis.

| Kelias | Kas tai |
|---|---|
| ✅ `uzduotis_02_planas.md` | **2 užd.** tikslų planas |
| ✅ `uzduotis_03_planas.md` | **3 užd.** tikslų planas — **dviejų pakopų filtras + eksperimento protokolas** *(2026-09-03)* |
| ✅ `uzduotis_04_planas.md` | **4 užd.** tikslų planas — **įkėlimo grandinė, modelių kontraktas, 3 dienų biudžetas** *(2026-09-06)* |
| ✅ `uzduotis_05_planas.md` | **5 užd.** tikslų planas — **vienas prėjimas per `test`, vertinimo protokolas, nematytų klasių taisyklės** *(2026-09-08)* |
| ✅ `uzduotis_06_planas.md` | **6 užd.** tikslų planas — **naujų matavimų nereikia; palyginimas ties FPR biudžetu, rekomendacija** *(2026-09-09)* |
| ⬛ `uzduotis_01_planas.md` · `praktikos_planas.md` · `kontekstas.md` | Kol kas tik Claude projekte |

## `ataskaita\`

| Kelias | Kas tai |
|---|---|
| ✅ `ataskaita.tex` | Pagrindinis dokumentas — preambulė + `\input`. **09-13: titulinis perdarytas** — be universitetinės atributikos, nes dokumentas teikiamas Aineros vadovui |
| ✅ `saltiniai.bib` | Visi šaltiniai — **20 įrašų**, visi su patikrintu DOI (išsk. `antonakakis2017mirai`) |
| ✅ `build.ps1` | Kompiliavimas — **gryname ASCII**. `-Clean`, `-Greitas` |
| ✅ `literatura.tex` → `literatura.pdf` | ⭐ Bibliografija atskirai (žr. žemiau) |
| ✅ `skyriai\00_ivadas.tex` | **BAIGTAS 09-13** — aktualumas, tikslas, uždaviniai, **prielaidos**, struktūra ir pagrindiniai rezultatai. Naujų šaltinių nepridėta |
| ✅ `skyriai\01_atakos.tex` | **1 užd.** Baigta. **2026-09-03: `tab:atakos` suderinta su 39 požymių leidimu** (15 taisymų). `tab:reikalavimai` **lieka čia** — perkėlimas atšauktas |
| ✅ `skyriai\02_di_metodai.tex` | **2 užd.** Baigta — 8 poskyriai, 3 lentelės, 9,7 psl. |
| ✅ `skyriai\03_parinkimas.tex` | **3 užd. BAIGTA** — 7 poskyriai, 4 lentelės, ~5 psl. Protokolas 3.6 poskyryje |
| ✅ `skyriai\04_sprendimas.tex` | **4 užd. BAIGTA** — 7 poskyriai, 3 lentelės, 2 paveikslai |
| ✅ `skyriai\05_vertinimas.tex` | **5 užd. BAIGTA** — 8 poskyriai, 6 lentelės, 3 paveikslai |
| ✅ `skyriai\06_palyginimas.tex` | **6 užd. BAIGTA** — 7 poskyriai, 2 lentelės, 1 paveikslas, ~6 psl. Baigiasi **rekomendacija** |
| ✅ `skyriai\07_isvados.tex` | **BAIGTOS 09-13** — po vieną išvadą kiekvienam uždaviniui, rekomendacija, apribojimai, 5 tyrimų kryptys |
| ✅ `lenteles\veikimas.tex` · `lenteles\*_test.tex` | **Generuojami** per `i_latex.py` — ranka neliesti. ⚠️ `rezultatai.tex` (val) pašalinta 09-13: nenaudojama nė viename skyriuje ir kaip tik ją lietė `i_latex` vidurkinimo yda |
| ✅ `lenteles\matrica.tex` · `lenteles\jautrumas.tex` | **Generuojami** per `matrica.py` / `jautrumas.py` — ranka neliesti |
| ✅ `lenteles\suvestine.tex` · `lenteles\pozymiai.tex` | **Generuojami** per `suvestine.py` / `pozymiu_svarba.py` — ranka neliesti |
| ✅ `paveikslai\architektura.pdf` · `prototipas.png` · `sumaisymas.pdf` · `kreives.pdf` · `kategorijos.pdf` · `kompromisai.pdf` | Visi **generuojami**, PDF data išjungta |
| ⬜ `skaidres\` | Skaidrės, jei reikės |

## `src\`

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\ikelimas.py` | ⭐ **Perrašytas 09-06 (T0).** Įgyvendina protokolą: valymo tvarka, **dublikatų šalinimas per eilučių maišas** (du prėjimai), riba **100 000** klasei, teorinės ribos perskaičiavimas. Išveda `imtis.parquet` + `imties_ataskaita.md` |
| ✅ `duomenys\etiketes.py` | ⭐ 34 etiketės → 8 kategorijos. **2026-09-02: registro normalizavimas + `BENIGN` alias** |
| ✅ `duomenys\pozymiai.py` | ⭐ **T2 (09-07).** 39 → **36** požymiai, šalinama sąrašu; tapatybės tikrinamos kaskart; `Skale` su apsauga (`fit` tik ant train, antras kvietimas meta klaidą) |
| ✅ `duomenys\skaidymas.py` | ⭐ **T3 (09-07).** Stratifikuotas 70/15/15 pagal **34 etiketes**; **keturios nutekėjimo patikros**; indeksai išsaugomi |
| ✅ `duomenys\balansavimas.py` | ⭐ **T4 (09-07).** Klasių svoriai (santykis 83,9), `sample_weight` XGBoost'ui, SMOTE abliacijai. **Gerybinis srautas nesintetinamas** |
| ✅ `modeliai\bazinis.py` | ⭐ **T5.** Kontraktas: `fit(..., svoriai=)` / `predict` / `predict_proba` / `issaugoti` / **`ikelti`** (09-09) + **`patikra()`** (`python -m src.modeliai.bazinis`) — tikrina, ar visos keturios klasės realizuoja kontraktą; laukai `priziurimas`, `reikia_skales`; delsos matavimas; registras `gauti()`. **`_ikelti` guli šalia `_issaugoti`** kiekvienoje klasėje — įkėlimo logika nebedubliuojama `slenkstis.py` ir `prototipas.py` |
| ✅ `modeliai\random_forest.py` | **T5.** `class_weight=balanced`; normalizavimo nereikia |
| ✅ `modeliai\gradientinis.py` | **T5.** XGBoost. ⚠️ Vardas **ne** `xgboost.py` — uždengtų biblioteką. `sample_weight`, ne `scale_pos_weight` |
| ✅ `modeliai\mlp.py` | **T5.** Keras; ankstyvas stabdymas pagal **mūsų** `val`; `.keras` failas skaičiuojamas į dydį |
| ✅ `modeliai\autoencoder.py` | ⭐ **T5.** Mokomas tik iš `BENIGN`; slenkstis — **99-asis** `val` procentilis (ne 95: procentilis nustato FPR) |
| ✅ `eksperimentai\paleisti.py` | ⭐ **T6.** Konfigas → mokymas → metrikos → `rezultatai.csv`. `--imtis` greitai patikrai (į CSV nerašo), `--vertinimas test` **tik 5 užduočiai**. ⭐ **`--tik-vertinti` (09-09):** įkelia išsaugotą modelį, mokymo aibės neatidaro; `sumaisymas_*` vardas turi aibę |
| ✅ `eksperimentai\metrikos.py` | **T6.** Protokolo 15 stulpelių; FPR = tikro gerybinio srauto dalis, priskirta atakai |
| ✅ `eksperimentai\matrica.py` | ⭐ **3 užd.:** `sprendimu_matrica.csv` → `lenteles\matrica.tex`. Svoriai 30/30/25/15 |
| ✅ `eksperimentai\jautrumas.py` | ⭐ **3 užd. (T5):** ±10 p. p. + tikrųjų ribų paieška → `lenteles\jautrumas.tex` |
| ✅ `prototipas.py` | ⭐ **T8.** Srautas → požymiai → inferencija → signalas. Naudoja **slenkstį, ne argmax**; inferencija CPU; validacijos aibė, test neliečiama |
| ✅ `eksperimentai\slenkstis.py` | ⭐ Sprendimo slenkstis: kreivės + operacinis taškas ties FPR ≤ 1 %. `--modeliai` leidžia paleisti dalimis. ⭐ **`--taikyti test` (09-09):** τ **skaitomas iš `slenkscio_taskai.csv`**, `parinkti()` tame režime nekviečiamas; išvestis — atskiri `*_test` failai, val nepaliečiama |
| ✅ `eksperimentai\derinimas.py` | ⭐ Atsitiktinė paieška ant imties; šalia macro-F1 fiksuoja **modelio dydį** |
| ✅ `eksperimentai\delsa.py` | Delsos permatavimas CPU. ⚠️ Visi modeliai — **vienu paleidimu, vienoje mašinoje** |
| ✅ `eksperimentai\lenteles.py` | `imties_pasiskirstymas.csv` → `lenteles/imtis.tex` |
| ✅ `eksperimentai\patikimumas.py` | ⭐ **T7 (09-09):** patikros **skaičiuojamos, ne surašomos**. 2-oji matuoja dedublikavimo erdvę (39 st.) ir modelio įvestį (36 st.) **atskirai**; 5-oji perskaičiuoja metrikas iš sumaišymo matricų |
| ✅ `eksperimentai\nematytos.py` | ⭐ **T5 (09-09):** nematytų klasių testas. Vertinama **dvejetainiu klausimu**; svoriai iš **pilnos** mokymo aibės; *τ* kiekvienam modeliui iš `val` |
| ✅ `eksperimentai\klaidos.py` | ⭐ **T4 (09-09):** per-klasę P/R/F1 su **`n` stulpeliu**, klaidų skirstymas pagal **eksploatacinę kainą** (klaidingi teigiami / praleistos atakos / **tarp atakų**), sumaišymo matricos paveikslas. Modelių neįkelia |
| ✅ `eksperimentai\suvestine.py` | ⭐ **6 užd. (09-09):** `lenteles/suvestine.tex` + `paveikslai/kompromisai.pdf`. Dvi lentelės dalys; autokoderio aptikimas skaičiuojamas iš per-kategorijų pjūvio su **kontroline patikra** prieš slenksčio failą. **Test aibės neliečia** |
| ✅ `eksperimentai\pozymiu_svarba.py` | ⭐ **6 užd. (09-09):** informacijos prieaugis (gain) **iš paties modelio** — duomenys neatidaromi. `lenteles/pozymiai.tex` |
| ✅ `eksperimentai\paveikslai.py` | `paveikslai/architektura.pdf`, `kreives.pdf`, `kategorijos.pdf`; PDF data išjungta, kad būtų atkartojama |
| ✅ `eksperimentai\eiga.py` | Eigos juosta (RF, XGBoost) |
| ⚠️ `eksperimentai\i_latex.py` | ⭐ **Perrašytas 09-06.** **09-09: `--aibe {val,test}` filtras, aibė įrašoma į išnašą.** ⚠️ `RAKTAI` neapima `konfig`, todėl bazinis ir suderintas modelis suvidurkinami į vieną eilutę — dabar apie tai **pranešama garsiai**, bet nepataisyta (turinio sprendimas).  Protokolo 15 stulpelių schema; agreguoja per seed'us (vidurkis ± std); išveda **dvi** lenteles: `rezultatai.tex` (kokybė) ir `veikimas.tex` (delsa, laikas, dydis). Ryškinama **tik macro-F1** |

## Duomenys, konfigūracijos, rezultatai

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\ciciot2023_pozymiai.md` | Perkeltas iš `ataskaita\skyriai\` **09-13** — tai duomenų dokumentas, ne skyrius |
| ✅ `duomenys\README.md` | ⭐ **CICIoT2023: 39 požymiai + `Label`, 45,0 mln. eilučių, spąstai** |
| ✅ `duomenys\raw\archive\Merged01..63.csv` | **8,7 GB — ne Git'e** |
| — | *`duomenys\raw\archive.zip` pašalintas 09-13 (1,79 GB). Atsisiuntimas iš naujo — `README.md`* |
| ✅ `duomenys\processed\imtis.parquet` | Imtis (100 000 / klasei) — sudaroma **vieną kartą**, ne Git'e. Vardas suvienodintas 09-06 |
| ✅ `duomenys\processed\imtis_metadata.json` | Sudarymo data, SEED, valymo skaitliukai, teorinė riba |
| ✅ `duomenys\processed\skaidymas.npz` | Train/val/test indeksai *(09-07: 1 698 155 / 363 891 / 363 891)* — **išsaugoti**, ne perskaičiuojami |
| ✅ `konfig\random_forest.yaml` · `gradientinis.yaml` · `mlp.yaml` · `autoencoder.yaml` | Eksperimentų konfigūracijos — **visos keturios užpildytos** |
| ✅ `konfig\gradientinis_dvejetaine.yaml` · `gradientinis_34klases.yaml` | ⭐ **T6 (09-09):** tik palyginimui su literatūra. Hiperparametrai tie patys kaip `_derintas` |
| ✅ `rezultatai\rezultatai.csv` | Metrikos — **Git'e**, **45 eilutės** (27 `val` + 18 `test`); 6 užduotis jų nekeičia. ⭐ **`aibe` stulpelis pridėtas 09-09** ir įrašytas į `RAKTAS`: `test` eilutė nebegali užimti `val` eilutės vietos. Kontroliniu paleidimu patvirtinta, kad senas kodas jas naikino tyliai |
| ✅ `rezultatai\apmokyti\` | Apmokyti modeliai — **ne Git'e**. Vardai: `<konfigas>_<formuluotė>_seed<N>.joblib` + `.skale.joblib` + `.json`. **09-13 pašalinti** Random Forest (2,0 GB) ir 34 klasių (355 MB) modeliai — permokomi per `04_mokyti_derintus.bat` ir `12_formuluotes.bat` |
| ✅ `rezultatai\darbiniai\imties_ataskaita.md` | ⭐ **Generuojama** — valymas, dublikatai, disbalansas, **patikslinta teorinė riba**. Skaičiai eina į 4 ir 5 skyrius |
| ✅ `rezultatai\darbiniai\rezultatai_pavyzdys.csv` | `rezultatai.csv` schemos pavyzdys — `paleisti.py` atskaitos taškas |
| ✅ `rezultatai\darbiniai\klasiu_pasiskirstymas.txt` | ⭐ **Pilnas skenavimas:** 34 klasės, 45 019 243 eilutės |
| ✅ `rezultatai\darbiniai\sprendimu_matrica.csv` | ⭐ **3 užd.:** 8 metodai × 4 kriterijai. **Vienintelis balų šaltinis** — `matrica.tex` ranka neliesti |
| ✅ `literatura\anotacijos.md` | Šaltinių anotacijos *(ne ataskaitos tekstas)*. Dublikatas ištrintas 09-03 |

---

## Kur ką rašyti — kad nesidubliuotų

| Turinys | Vieta |
|---|---|
| Sprendimai, radiniai, pamokos | `DARBO_ZURNALAS.md` |
| Šaltinių anotacijos | `literatura\anotacijos.md` |
| Duomenų rinkinys, požymiai, etiketės | `duomenys\README.md` |
| Kategorijų žodynas (kodas, **importuojamas**) | `src\duomenys\etiketes.py` |
| Užduočių planai | `claude\uzduotis_NN_planas.md` |
| **Eksperimento protokolas** | `claude\uzduotis_03_planas.md` 5 sk. → `04_sprendimas.tex` metodika |
| Ataskaitos tekstas | `ataskaita\skyriai\*.tex` |

---

## Komandos

### Paprasčiausias būdas — `.bat` failai

```
01_patikra.bat            04_mokyti_derintus.bat    09_slenkstis_test.bat
02_mokyti_viska.bat       05_delsa.bat              10_klaidos.bat
  02a..02d_mokyti_*.bat   06_slenkstis.bat          11_nematytos.bat
03_derinti.bat            07_prototipas.bat         12_formuluotes.bat
                          08_vertinti_test.bat      13_patikimumas.bat
                                                    14_palyginimas.bat
```

Numeris = paleidimo eile. `_aplinka.bat` numerio neturi: tai ne zingsnis, o bendra dalis.

Jie patys aktyvuoja `iot-ids` ir **nutraukia darbą**, jei aktyvi kita aplinka —
būtent tai, kas atsitiko 2026-09-07.

### Rankomis

```powershell
conda activate iot-ids
cd D:\Ainera\iot-ids-praktika

cd ataskaita ; .\build.ps1
.\build.ps1 -Clean       # po mpm --update arba nutrukusio paleidimo
.\build.ps1 -Greitas     # vienas praejimas, be biber

python -m src.duomenys.ikelimas patikra
python -m src.duomenys.ikelimas imtis
python -m src.duomenys.etiketes
python -m src.duomenys.pozymiai          # 36 pozymiai + tapatybiu patikra
python -m src.duomenys.skaidymas         # 70/15/15 -> skaidymas.npz
python -m src.duomenys.skaidymas patikra # tik nutekejimo patikros
python -m src.duomenys.balansavimas      # klasiu svoriai + SMOTE abliacija

python -m src.eksperimentai.matrica     # CSV -> lenteles/matrica.tex
python -m src.eksperimentai.jautrumas   # T5: svoriu jautrumas
python -m src.eksperimentai.paleisti konfig/random_forest.yaml --seed 42 43 44
python -m src.eksperimentai.paleisti konfig/*.yaml --seed 42 43 44
python -m src.eksperimentai.paleisti konfig/mlp.yaml --imtis 50000   # greita patikra
python -m src.eksperimentai.i_latex --aibe test --priesaga _test
python -m src.eksperimentai.klaidos --aibe test    # -> perklase.tex + sumaisymas.pdf
python -m src.eksperimentai.suvestine              # 6 uzd. -> suvestine.tex + kompromisai.pdf
python -m src.eksperimentai.pozymiu_svarba         # 6 uzd. -> pozymiai.tex

git add . ; git commit -m "..." ; git push
```

---

## Bibliografija generuojama atskirai

Pilnoje `ataskaita.tex` preambulėje `\printbibliography` lūžta; minimalioje veikia. Priežastis nerasta (įtariamas `csquotes` su lietuviškomis kabutėmis).

Apėjimas: `literatura.tex` → `literatura.pdf` → `\includepdf`. **`build.ps1` tai daro pats — rankinio sujungimo nereikia.** Citavimai veikia; neveikia tik nuorodos iš citavimo į įrašą.

---

## Spąstai

### Duomenys *(patikrinta 2026-09-02)*

| Problema | Sprendimas |
|---|---|
| `df["label"]` → `KeyError` | Stulpelis yra **`Label`** |
| Etiketė nerandama žodyne | Faile **DIDŽIOSIOS**; `BenignTraffic` → **`BENIGN`**. Naudoti `etiketes.normalizuoti()` |
| `Merged*.csv` nerandami | Jie ne `duomenys\raw\`, o **`duomenys\raw\archive\`** |
| sklearn: `Input contains infinity` | **991 eilutė** turi `Rate` = `Infinity` → `replace([inf,-inf], nan).dropna()` |
| Tyliai atsiranda 35-a klasė | 9 failai baigiasi **nutrūkusia eilute** → `dropna(subset=["Label"])` |
| Koreliacijos filtras palieka `Variance` | `Variance` = `Std`², bet tiesinė koreliacija 0,737 — šalinti **sąrašu** |
| **Išpūsti rezultatai be matomos klaidos** | ⭐ **53,3 % eilučių — tikslūs dublikatai** *(išmatuota visame rinkinyje 09-06; ankstesnis 33,1 % buvo iš 1,9 mln. imties)*. Šalinti pagal **visą eilutę**, **prieš** imtį ir skaidymą |
| Rezultatas aukštesnis nei **99,78 %** | Teorinė riba darbinėje imtyje *(09-06)*: 0,43 % eilučių turi prieštaringas etiketes. Aukštesnis rezultatas = nutekėjimas |

### Aplinka

| Problema | Sprendimas |
|---|---|
| Atsisiųstas `.ps1` neveikia | `Unblock-File .\failas.ps1` |
| `.ps1` meta `Unexpected token` | Faile yra ne-ASCII simbolių |
| `.gitignore` eilutė neveikia | Komentaras eilutės gale — perkelti į atskirą eilutę |
| `ModuleNotFoundError` | Promptas rodo `(base)` — `conda activate iot-ids` |
| ⚠️ **`NumPy 1.x cannot be run in NumPy 2.x`** | Paleista `(base)`, ne `(iot-ids)`. Base aplinkoje `%APPDATA%\Python\Python312\site-packages` uždengia anaconda paketus. `iot-ids` yra Python 3.11, todėl jos tai neliečia |
| `pip install -r requirements-lock.txt` nesuveikia | PowerShell `>` rašo **UTF-16**, pip laukia UTF-8. Naudoti `\| Out-File -Encoding utf8`. ⚠️ PS 5.1 tai duoda UTF-8 **su BOM** — pip jį nurija, bet failui be BOM reikia `Set-Content -Encoding ascii` |

### LaTeX

| Problema | Sprendimas |
|---|---|
| `no legal \end found` | `.tex` failas tuščias arba neperkeltas |
| `Undefined control sequence` ties `.aux` | `.\build.ps1 -Clean` |
| `Float too large for page` | `xltabular`/`longtable` **negali būti** `table` float'e |
| `Improper alphabetic constant` | Žinoma; todėl bibliografija atskirai |
| Tuščias skyrius, turinys nuslinkęs | Skyrių failuose **`\section` būti negali**; `\label` turi būti unikalūs |
| **PDF'e `??`, nors kodas pataisytas** | *(09-09)* Generuojamas `lenteles/*.tex` liko senos versijos. **Pataisius generatorių — pergeneruoti išvestį**, kitaip taisymas galioja tik kode |

### Lietuvių kalba

| Problema | Sprendimas |
|---|---|
| `\cref` duoda „Iš **lentelė 4**" | cleveref nelinksniuoja. **Nenaudoti.** Rašyti `Iš \ref{tab:X} lentelės` |
| Lūžta paketo parametre | Lietuviškų raidžių nedėti į `key=value` |
| Ilgi `\texttt{}` išsikiša | `\usepackage[htt]{hyphenat}` + `\setlength{\emergencystretch}{3em}` |
| **Kirilicos raidės tekste** | `а`, `о` vizualiai neatskiriamos. **Automatinė patikra privaloma prieš kiekvieną commit'ą** — pasitaikė jau tris kartus |
