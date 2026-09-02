# Failų žemėlapis

Greita nuoroda: kur kas guli ir ką paleisti. Ilgas kontekstas — `DARBO_ZURNALAS.md`.

**Šaknis:** `D:\Ainera\iot-ids-praktika\`
**Atnaujinta:** 2026-09-02 — sudaryta iš **realaus aplanko turinio**, ne iš plano
**Žymos:** ✅ turi turinį · ⬜ sukurtas, bet tuščias · ⬛ dar nesukurtas

---

## Šaknis

| Kelias | Kas tai |
|---|---|
| ✅ `DARBO_ZURNALAS.md` | Kasdienis žurnalas — **tik sprendimai, radiniai, pamokos** |
| ✅ `STRUKTURA.md` | Šis failas |
| ⬜ `README.md` | Projekto apžvalga |
| ✅ `requirements.txt` · `requirements-lock.txt` | Priklausomybės |
| ✅ `patikra.py` | Aplinkos patikra |
| ✅ `.gitignore` | Komentarai **tik** atskirose eilutėse |
| ✅ `.gitattributes` | Eilučių pabaigų normalizavimas |

## `claude\` — planavimo dokumentai

Atitinka Claude projekto dokumentų erdvę 1:1, kad sinchronizavimas būtų tiesioginis.

| Kelias | Kas tai |
|---|---|
| ✅ `uzduotis_02_planas.md` | **2 užd.** tikslų planas |
| ⬛ `uzduotis_01_planas.md` · `praktikos_planas.md` · `kontekstas.md` | Kol kas tik Claude projekte |

## `ataskaita\`

| Kelias | Kas tai |
|---|---|
| ✅ `ataskaita.tex` | Pagrindinis dokumentas — preambulė + `\input` |
| ✅ `saltiniai.bib` | Visi šaltiniai — **11 įrašų** (po 2 užd. bus 17–19) |
| ✅ `build.ps1` | Kompiliavimas — **gryname ASCII**. `-Clean`, `-Greitas` |
| ✅ `literatura.tex` → `literatura.pdf` | ⭐ Bibliografija atskirai (žr. žemiau) |
| ✅ `bibtestas.tex` | Diagnostikai — ištrinti radus priežastį |
| ✅ `skyriai\00_ivadas.tex` | Įvadas *(rašomas paskutinis)* |
| ✅ `skyriai\01_atakos.tex` | **1 užd.** Baigta — 7 poskyriai, 5 lentelės, ~9 psl. |
| ⬜ `skyriai\02_di_metodai.tex` | **2 užd.** ← **dabartinis darbas** |
| ⬜ `skyriai\03..07_*.tex` | 3–6 užd. ir išvados |
| ✅ `lenteles\rezultatai.tex` | **Generuojama** — ranka neliesti |
| ⬜ `paveikslai\` · `skaidres\` | Grafikai, skaidrės |

## `src\`

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\ikelimas.py` | Patikra, stratifikuota imtis. **2026-09-02: `Label`, kelias `raw/archive/`** |
| ✅ `duomenys\etiketes.py` | ⭐ 34 etiketės → 8 kategorijos. **2026-09-02: registro normalizavimas + `BENIGN` alias** |
| ⬜ `duomenys\pozymiai.py` | Požymių inžinerija |
| ⬜ `duomenys\balansavimas.py` | SMOTE / klasių svoriai |
| ⬜ `modeliai\bazinis.py` | Bendra klasė: `fit` / `predict` / `predict_proba` |
| ⬜ `modeliai\random_forest.py` · `autoencoder.py` · `cnn.py` | Modeliai |
| ⬜ `eksperimentai\paleisti.py` | Konfigas → mokymas → metrikos |
| ✅ `eksperimentai\i_latex.py` | CSV → `ataskaita\lenteles\` |

## Duomenys, konfigūracijos, rezultatai

| Kelias | Kas tai |
|---|---|
| ✅ `duomenys\README.md` | ⭐ **CICIoT2023: 39 požymiai + `Label`, 45,0 mln. eilučių, spąstai** |
| ✅ `duomenys\raw\archive\Merged01..63.csv` | **8,7 GB — ne Git'e** |
| ⬛ `duomenys\processed\` | Parquet imtys — ne Git'e |
| ✅ `konfig\random_forest.yaml` · `autoencoder.yaml` | Eksperimentų konfigūracijos |
| ⬜ `rezultatai\rezultatai.csv` | Metrikos — **Git'e** |
| ⬜ `rezultatai\apmokyti\metadata.json` | Git'e tik metaduomenys |
| ⬛ `rezultatai\darbiniai\` | Juodraščiai |
| ✅ `literatura\anotacijos.md` | Šaltinių anotacijos *(ne ataskaitos tekstas)* |

---

## Kur ką rašyti — kad nesidubliuotų

| Turinys | Vieta |
|---|---|
| Sprendimai, radiniai, pamokos | `DARBO_ZURNALAS.md` |
| Šaltinių anotacijos | `literatura\anotacijos.md` |
| Duomenų rinkinys, požymiai, etiketės | `duomenys\README.md` |
| Kategorijų žodynas (kodas, **importuojamas**) | `src\duomenys\etiketes.py` |
| Užduočių planai | `claude\uzduotis_NN_planas.md` |
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

python -m src.eksperimentai.i_latex

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

### Lietuvių kalba

| Problema | Sprendimas |
|---|---|
| `\cref` duoda „Iš **lentelė 4**" | cleveref nelinksniuoja. **Nenaudoti.** Rašyti `Iš \ref{tab:X} lentelės` |
| Lūžta paketo parametre | Lietuviškų raidžių nedėti į `key=value` |
| Ilgi `\texttt{}` išsikiša | `\usepackage[htt]{hyphenat}` + `\setlength{\emergencystretch}{3em}` |
