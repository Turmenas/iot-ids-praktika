# IoT kibernetinių atakų prevencija naudojant DI sistemas

Praktikos darbas. **Gabrielius Tumėnas**, VILNIUS TECH, Dirbtinio intelekto programinės sistemos.
Laikotarpis: 2026 m. rugsėjo 1–18 d.

Tikslas — palyginti dirbtinio intelekto metodus IoT tinklo įsibrovimų aptikimui ir įvertinti, kurie iš jų realiai tinka kraštiniam šliuzui: ne tik pagal aptikimo tikslumą, bet ir pagal inferencijos delsą, resursų poreikį bei atsparumą klasių disbalansui.

## Darbo eiga

| Užd. | Turinys | Skyrius | Būklė |
|---|---|---|---|
| 1 | IoT atakų ir aptikimo metodų analizė | `01_atakos.tex` | ✅ Baigta |
| 2 | DI ir MM metodų taikymo galimybės | `02_di_metodai.tex` | 🔄 Vykdoma |
| 3 | Metodų parinkimas ir pagrindimas | `03_parinkimas.tex` | ⬜ |
| 4 | Aptikimo sprendimo kūrimas | `04_sprendimas.tex` | ⬜ |
| 5 | Eksperimentinis vertinimas | `05_vertinimas.tex` | ⬜ |
| 6 | Metodų efektyvumo palyginimas | `06_palyginimas.tex` | ⬜ |

## Duomenys

**CICIoT2023**, Kaggle leidimas „official IoT flow feature dataset" — 63 CSV, 8,7 GB, **45 019 243 eilutės**, **39 požymiai + `Label`**, 34 klasės.

> ⚠️ **Tai ne kanoninė 46 požymių versija.** Skirtumai, spąstai ir jų pasekmės — **`duomenys/README.md`**. Perskaityti prieš liečiant duomenis: yra tylių problemų (nutrūkusios eilutės, `Rate` = `Infinity`, etikečių registras), kurių `pandas` nepraneša.

Duomenys į Git nekeliami. Atsisiuntimas:

```bash
kaggle datasets download -d shadman1028/cic-iot2023-official-iot-flow-feature-dataset \
    --unzip -p duomenys/raw/
```

## Paleidimas

```powershell
conda activate iot-ids
python patikra.py                          # aplinkos patikra
python -m src.duomenys.ikelimas patikra    # duomenu patikra
python -m src.duomenys.etiketes            # etikeciu zodyno savipatikra

cd ataskaita ; .\build.ps1                 # ataskaita.pdf
```

Aplinka: Python 3.11, conda `iot-ids`; LaTeX — MiKTeX. Priklausomybės — `requirements.txt` (tikslios versijos: `requirements-lock.txt`).

## Kur ieškoti

| Klausimas | Failas |
|---|---|
| Kur kas guli, ką paleisti, spąstai | `STRUKTURA.md` |
| Kas ir kada padaryta, kodėl taip nuspręsta | `DARBO_ZURNALAS.md` |
| Duomenų rinkinys: požymiai, etiketės, spąstai | `duomenys/README.md` |
| Šaltinių anotacijos | `literatura/anotacijos.md` |
| Užduočių planai | `claude/uzduotis_NN_planas.md` |

## Citavimas

Naudojamas duomenų rinkinys cituojamas per originalų straipsnį, ne per Kaggle veidrodį:

> E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, A. A. Ghorbani. *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment.* Sensors 23(13):5941, 2023. DOI: 10.3390/s23135941
