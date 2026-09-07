# Failų žemėlapis

Greita nuoroda: kur kas guli ir ką paleisti. Ilgas kontekstas — `DARBO_ZURNALAS.md`.

**Šaknis:** `D:\Ainera\iot-ids-praktika\`
**Atnaujinta:** 2026-09-07 — **T0–T4 atlikti**: imtis sudaryta, požymiai, skaidymas, balansavimas
**Žymos:** ✅ turi turinį · ⬜ sukurtas, bet tuščias · ⬛ dar nesukurtas

---

## Šaknis

| Kelias | Kas tai |
|---|---|
| ✅ `DARBO_ZURNALAS.md` | Kasdienis žurnalas — **tik sprendimai, radiniai, pamokos** |
| ✅ `STRUKTURA.md` | Šis failas |
| ✅ `README.md` | Projekto apžvalga *(2026-09-03: turi turinį, anksčiau klaidingai žymėta tuščia)* |
| ✅ `requirements.txt` · `requirements-lock.txt` | Priklausomybės *(lock nuo 09-01; žurnale klaidingai laikyta neatlikta)* |
| ✅ `patikra.py` | Aplinkos patikra |
| ✅ `.gitignore` | Komentarai **tik** atskirose eilutėse |
| ✅ `.gitattributes` | Eilučių pabaigų normalizavimas |

## `claude\` — planavimo dokumentai

Atitinka Claude projekto dokumentų erdvę 1:1, kad sinchronizavimas būtų tiesioginis.

| Kelias | Kas tai |
|---|---|
| ✅ `uzduotis_02_planas.md` | **2 užd.** tikslų planas |
| ✅ `uzduotis_03_planas.md` | **3 užd.** tikslų planas — **dviejų pakopų filtras + eksperimento protokolas** *(2026-09-03)* |
| ✅ `uzduotis_04_planas.md` | **4 užd.** tikslų planas — **įkėlimo grandinė, modelių kontraktas, 3 dienų biudžetas** *(2026-09-06)* |
| ⬛ `uzduotis_01_planas.md` · `praktikos_planas.md` · `kontekstas.md` | Kol kas tik Claude projekte |

## `ataskaita\`

| Kelias | Kas tai |
|---|---|
| ✅ `ataskaita.tex` | Pagrindinis dokumentas — preambulė + `\input` |
| ✅ `saltiniai.bib` | Visi šaltiniai — **20 įrašų**, visi su patikrintu DOI (išsk. `antonakakis2017mirai`) |
| ✅ `build.ps1` | Kompiliavimas — **gryname ASCII**. `-Clean`, `-Greitas` |
| ✅ `literatura.tex` → `literatura.pdf` | ⭐ Bibliografija atskirai (žr. žemiau) |
| ✅ `bibtestas.tex` | Diagnostikai — ištrinti radus priežastį |
| ✅ `skyriai\00_ivadas.tex` | Įvadas *(rašomas paskutinis)* |
| ✅ `skyriai\01_atakos.tex` | **1 užd.** Baigta. **2026-09-03: `tab:atakos` suderinta su 39 požymių leidimu** (15 taisymų). `tab:reikalavimai` **lieka čia** — perkėlimas atšauktas |
| ✅ `skyriai\02_di_metodai.tex` | **2 užd.** Baigta — 8 poskyriai, 3 lentelės, 9,7 psl. |
| ⚠️ `skyriai\ciciot2023_pozymiai.md` | **Ne skyrius** — duomenų dokumentas tarp `.tex` failų. Vieta svarstytina |
| ✅ `skyriai\03_parinkimas.tex` | **3 užd. BAIGTA** — 7 poskyriai, 4 lentelės, ~5 psl. Protokolas 3.6 poskyryje |
| ⬜ `skyriai\04_sprendimas.tex` | **4 užd.** ← **vykdoma rugs. 7–9 d.** Metodika rašoma iš 3.6 protokolo; planas — `claude\uzduotis_04_planas.md` |
| ⬜ `skyriai\05..07_*.tex` | 5–6 užd. ir išvados |
| ⬜ `lenteles\rezultatai.tex` · `lenteles\veikimas.tex` | **Generuojami** per `i_latex.py` — ranka neliesti |
| ✅ `lenteles\matrica.tex` · `lenteles\jautrumas.tex` | **Generuojami** per `matrica.py` / `jautrumas.py` — ranka neliesti |
| ⬜ `paveikslai\` · `skaidres\` | Grafikai, skaidrės |

## `src\`

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\ikelimas.py` | ⭐ **Perrašytas 09-06 (T0).** Įgyvendina protokolą: valymo tvarka, **dublikatų šalinimas per eilučių maišas** (du prėjimai), riba **100 000** klasei, teorinės ribos perskaičiavimas. Išveda `imtis.parquet` + `imties_ataskaita.md` |
| ✅ `duomenys\etiketes.py` | ⭐ 34 etiketės → 8 kategorijos. **2026-09-02: registro normalizavimas + `BENIGN` alias** |
| ✅ `duomenys\pozymiai.py` | ⭐ **T2 (09-07).** 39 → **36** požymiai, šalinama sąrašu; tapatybės tikrinamos kaskart; `Skale` su apsauga (`fit` tik ant train, antras kvietimas meta klaidą) |
| ✅ `duomenys\skaidymas.py` | ⭐ **T3 (09-07).** Stratifikuotas 70/15/15 pagal **34 etiketes**; **keturios nutekėjimo patikros**; indeksai išsaugomi |
| ✅ `duomenys\balansavimas.py` | ⭐ **T4 (09-07).** Klasių svoriai (santykis 83,9), `sample_weight` XGBoost'ui, SMOTE abliacijai. **Gerybinis srautas nesintetinamas** |
| ⬜ `modeliai\bazinis.py` | Bendra klasė: `fit` / `predict` / `predict_proba`. 0 baitų |
| ⬜ `modeliai\random_forest.py` · `autoencoder.py` · `cnn.py` | Sukurti, 0 baitų. ⚠️ **Ketvertas yra RF, XGBoost, MLP, autokoderis** — `cnn.py` **ištrintinas**; reikės `gradientinis.py` (⚠️ **ne** `xgboost.py` — uždengtų biblioteką) ir `mlp.py` |
| ⬜ `eksperimentai\paleisti.py` | Konfigas → mokymas → metrikos. 0 baitų |
| ✅ `eksperimentai\matrica.py` | ⭐ **3 užd.:** `sprendimu_matrica.csv` → `lenteles\matrica.tex`. Svoriai 30/30/25/15 |
| ✅ `eksperimentai\jautrumas.py` | ⭐ **3 užd. (T5):** ±10 p. p. + tikrųjų ribų paieška → `lenteles\jautrumas.tex` |
| ✅ `eksperimentai\i_latex.py` | ⭐ **Perrašytas 09-06 (T0).** Protokolo 15 stulpelių schema; agreguoja per seed'us (vidurkis ± std); išveda **dvi** lenteles: `rezultatai.tex` (kokybė) ir `veikimas.tex` (delsa, laikas, dydis). Ryškinama **tik macro-F1** |

## Duomenys, konfigūracijos, rezultatai

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\README.md` | ⭐ **CICIoT2023: 39 požymiai + `Label`, 45,0 mln. eilučių, spąstai** |
| ✅ `duomenys\raw\archive\Merged01..63.csv` | **8,7 GB — ne Git'e** |
| 🗑 `duomenys\raw\archive.zip` | **~2,3 GB** — CSV išpakuoti, archyvas nebereikalingas |
| ✅ `duomenys\processed\imtis.parquet` | Imtis (100 000 / klasei) — sudaroma **vieną kartą**, ne Git'e. Vardas suvienodintas 09-06 |
| ✅ `duomenys\processed\imtis_metadata.json` | Sudarymo data, SEED, valymo skaitliukai, teorinė riba |
| ✅ `duomenys\processed\skaidymas.npz` | Train/val/test indeksai *(09-07: 1 698 155 / 363 891 / 363 891)* — **išsaugoti**, ne perskaičiuojami |
| ✅ `konfig\random_forest.yaml` · `autoencoder.yaml` | Eksperimentų konfigūracijos |
| ⬜ `rezultatai\rezultatai.csv` | Metrikos — **Git'e**. Schema fiksuota 3 užd. protokolo 24 punkte |
| ⬜ `rezultatai\apmokyti\metadata.json` | Git'e tik metaduomenys |
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
python -m src.eksperimentai.i_latex        # -> rezultatai.tex + veikimas.tex

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

### LaTeX

| Problema | Sprendimas |
|---|---|
| `no legal \end found` | `.tex` failas tuščias arba neperkeltas |
| `Undefined control sequence` ties `.aux` | `.\build.ps1 -Clean` |
| `Float too large for page` | `xltabular`/`longtable` **negali būti** `table` float'e |
| `Improper alphabetic constant` | Žinoma; todėl bibliografija atskirai |
| Tuščias skyrius, turinys nuslinkęs | Skyrių failuose **`\section` būti negali**; `\label` turi būti unikalūs |

### Lietuvių kalba

| Problema | Sprendimas |
|---|---|
| `\cref` duoda „Iš **lentelė 4**" | cleveref nelinksniuoja. **Nenaudoti.** Rašyti `Iš \ref{tab:X} lentelės` |
| Lūžta paketo parametre | Lietuviškų raidžių nedėti į `key=value` |
| Ilgi `\texttt{}` išsikiša | `\usepackage[htt]{hyphenat}` + `\setlength{\emergencystretch}{3em}` |
| **Kirilicos raidės tekste** | `а`, `о` vizualiai neatskiriamos. **Automatinė patikra privaloma prieš kiekvieną commit'ą** — pasitaikė jau tris kartus |
