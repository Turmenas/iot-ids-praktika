# IoT kibernetinių atakų prevencija naudojant DI sistemas

Praktikos darbas. **Gabrielius Tumėnas**, VILNIUS TECH, Dirbtinio intelekto programinės sistemos.
Laikotarpis: 2026 m. rugsėjo 1–18 d.

Tikslas — palyginti dirbtinio intelekto metodus IoT tinklo įsibrovimų aptikimui ir įvertinti, kurie iš jų realiai tinka kraštiniam šliuzui: ne tik pagal aptikimo tikslumą, bet ir pagal inferencijos delsą, resursų poreikį bei atsparumą klasių disbalansui.

## Darbo eiga

| Užd. | Turinys | Skyrius | Būklė |
|---|---|---|---|
| 1 | IoT atakų ir aptikimo metodų analizė | `01_atakos.tex` | ✅ Baigta |
| 2 | DI ir MM metodų taikymo galimybės | `02_di_metodai.tex` | ✅ Baigta |
| 3 | Metodų parinkimas ir pagrindimas | `03_parinkimas.tex` | ✅ Baigta |
| 4 | Aptikimo sprendimo kūrimas | `04_sprendimas.tex` | ✅ Baigta |
| 5 | Eksperimentinis vertinimas | `05_vertinimas.tex` | ✅ Baigta |
| 6 | Metodų efektyvumo palyginimas | `06_palyginimas.tex` | ✅ Baigta |

## Rezultatas

Ties reikalaujamu **1 % klaidingų teigiamų biudžetu** geriausias yra **XGBoost su sprendimo slenksčiu**: makro-F1 **0,663**, aptinka **88,5 %** atakų srauto prie **0,95 %** klaidingų teigiamų, modelis **45 MB**, inferencija **29,6 µs** vienam įrašui.

Du dalykai, kuriuos verta žinoti prieš skaitant skaičius:

- **Palyginimas ties didžiausios tikimybės tašku duoda kitą nugalėtoją** (Random Forest). Tas taškas duoda 21–31 % klaidingų teigiamų, todėl eksploatacijai netinka — visas palyginimas atliekamas ties biudžetu.
- **Iš duomenų pašalinta 53,3 % tikslių dublikatų.** Dėl to skaičiai žemesni nei literatūroje skelbiami 99 %+, ir tai sąmoninga: be šio žingsnio dalis testavimo aibės modeliui būtų jau matyta.

## Duomenys

**CICIoT2023**, Kaggle leidimas „official IoT flow feature dataset" — 63 CSV, 8,7 GB, **45 019 243 eilutės**, **39 požymiai + `Label`**, 34 klasės.

> ⚠️ **Tai ne kanoninė 46 požymių versija.** Skirtumai, spąstai ir jų pasekmės — **`duomenys/README.md`**. Perskaityti prieš liečiant duomenis: yra tylių problemų (nutrūkusios eilutės, `Rate` = `Infinity`, etikečių registras), kurių `pandas` nepraneša.

Duomenys į Git nekeliami. Atsisiuntimas:

```bash
kaggle datasets download -d shadman1028/cic-iot2023-official-iot-flow-feature-dataset \
    --unzip -p duomenys/raw/
```

## Paleidimas

`.bat` failai sunumeruoti paleidimo eile — iš eilės nuo 01 iki 14:

```powershell
01_patikra.bat               # aplinka + duomenys, ~1 min.
02_mokyti_viska.bat          # 12 paleidimu (4 modeliai x 3 seed'ai)
   02a..02d_mokyti_*.bat     #   tas pats dalimis, po viena modeli
03_derinti.bat               # hiperparametru paieska ant imties
04_mokyti_derintus.bat       # permokymas suderintais parametrais
05_delsa.bat                 # delsa CPU, visi modeliai vienu paleidimu
06_slenkstis.bat             # operacinis taskas ties FPR <= 1 % (val)
07_prototipas.bat            # Streamlit demonstracija narsykleje

08_vertinti_test.bat         # VIENINTELIS prejimas per test aibe
09_slenkstis_test.bat        # tau is val -> taikomas test
10_klaidos.bat               # per-klase metrikos, sumaisymo matricos
11_nematytos.bat             # nematytu klasiu testas
12_formuluotes.bat           # dvejetaine ir 34 klasiu formuluotes
13_patikimumas.bat           # penkios patikimumo patikros
14_palyginimas.bat           # 6 uzd.: suvestine + pozymiu svarba

cd ataskaita ; .\build.ps1    # ataskaita.pdf
```

`_aplinka.bat` numerio neturi: tai ne žingsnis, o bendra dalis, kurią kviečia visi kiti — ji aktyvuoja `iot-ids` ir **nutraukia darbą**, jei aktyvi kita aplinka.

⚠️ **`08_vertinti_test.bat` liečia testavimo aibę.** Protokolas leidžia vieną prėjimą: visi sprendimai priimami validacijos aibėje prieš tai. `14_palyginimas.bat` ir `10_klaidos.bat` testavimo aibės neatidaro — jie skaičiuoja iš jau išsaugotų failų.

Rankiniu būdu:

```powershell
conda activate iot-ids
python patikra.py                          # aplinkos patikra
python -m src.duomenys.ikelimas patikra    # duomenu patikra
python -m src.duomenys.ikelimas imtis      # imtis.parquet (vienas kartas)
python -m src.duomenys.etiketes            # etikeciu zodyno savipatikra
python -m src.modeliai.bazinis             # modeliu kontrakto patikra
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
