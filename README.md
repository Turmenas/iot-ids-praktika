# IoT kibernetinių atakų prevencija naudojant DI sistemas

Praktikos darbas. Gabrielius Tumėnas, VILNIUS TECH, Dirbtinio intelekto programinės sistemos.
2026 m. rugsėjo 1–18 d.

Repozitorijoje yra visas kodas, ataskaitos LaTeX šaltinis ir eksperimentų rezultatai. Ataskaita (`ataskaita/ataskaita.pdf`, 57 psl.) yra pagrindinis darbo dokumentas; šis failas paaiškina, kas čia guli ir kaip tai paleisti.

## Ką sistema daro

Klausimas paprastas: ar iš tinklo srauto matyti, kad IoT įrenginys puolamas arba pats dalyvauja atakoje.

**Įvestis** — vieno srauto lango santrauka: 39 skaitiniai požymiai, apskaičiuoti iš 10 arba 100 paketų (paketų skaičius, dydžių statistika, protokolų ir TCP vėliavėlių dalys, intensyvumas). Pavienių paketų turinio sistema nemato.

**Išvestis** — viena iš aštuonių kategorijų (`Benign`, `DDoS`, `DoS`, `Mirai`, `Recon`, `Spoofing`, `Web`, `BruteForce`) ir pavojaus signalas, kai bendra atakų tikimybė viršija nustatytą slenkstį.

**Numatoma diegimo vieta** — kraštinis šliuzas, t. y. įrenginys tarp IoT tinklo ir interneto. Jis mato visų įrenginių srautą, o į pačius jutiklius nieko diegti nereikia. Iš tos vietos kyla du reikalavimai, kurie darbe traktuojami kaip privalomi:

- **Delsa** iki 20–50 ms vienam sprendimui.
- **Klaidingi teigiami** iki 1 %. Prie didesnio skaičiaus tipiniame tinkle susidaro ~1000 nepagrįstų signalų per parą, ir sistemą personalas išjungia.

## Rezultatai

Palyginti keturi metodai: Random Forest, XGBoost, MLP (neuroninis tinklas) ir autokoderis. Vertinta nepriklausomoje testavimo aibėje, po tris paleidimus su skirtingais seed'ais.

Naudojama pagrindinė metrika — **makro-F1**: vidurkis per visas aštuonias kategorijas, kiekvienai suteikiant vienodą svorį. Bendras tikslumas šiems duomenims netinka, nes atakų juose ~42 kartus daugiau nei gerybinio srauto: modelis, viską žymintis kaip ataką, gautų ~97 %.

**Sprendimo slenkstis.** Visi modeliai grąžina tikimybes, tad sprendimo tašką galima rinktis po mokymo. Ataka skelbiama, kai bendra atakų tikimybė viršija τ; τ parenkamas validacijos aibėje taip, kad klaidingi teigiami tilptų į 1 % biudžetą. Testavimo aibė šiame žingsnyje neliečiama.

| Modelis | makro-F1 ties biudžetu | Klaidingi teigiami | Dydis | Delsa (CPU) |
|---|---:|---:|---:|---:|
| **XGBoost** | **0,663** | 0,95 % | 45 MB | 27,4 µs |
| Random Forest | 0,646 | 1,02 % ⚠️ | 638 MB | 10,9 µs |
| MLP | 0,595 | 0,64 % | 0,52 MB | 3,0 µs |
| Autokoderis | 0,220 | 1,00 % | 0,06 MB | 2,8 µs |

**Rekomenduojamas sprendimas — XGBoost su slenksčiu.** Jis aptinka 88,5 % atakų srauto prie 0,95 % klaidingų teigiamų. Random Forest ties tuo pačiu biudžetu peržengia ribą ir užima 638 MB, o kraštinio šliuzo klasės įrenginiai turi 1–8 GB atminties. Delsa nė vienam modeliui nėra ribojantis veiksnys: visi telpa į 20–50 ms biudžetą su maždaug tūkstantkarte atsarga.

### Ką sistema aptinka gerai ir prastai

Bendras 88,5 % skaičius yra svertinis vidurkis, kurį lemia gausiausios kategorijos. Per kategorijas aptikimas ties tuo pačiu operaciniu tašku svyruoja:

| Kategorija | Aptinkama |
|---|---:|
| DDoS · DoS · Mirai | 100 % |
| Spoofing | 81 % |
| BruteForce | 46 % |
| Recon (žvalgyba) | 44 % |
| Web | 38 % |

Trys prasčiausiai atpažįstamos yra kaip tik tos, kurios svarbios ankstyvam įspėjimui. Priežastis matoma iš duomenų: naudojamame rinkinio leidime nėra srauto krypties ir trukmės požymių, todėl žvalgyba požymių erdvėje persidengia su įprastu srautu. 14–28 % tikro gerybinio srauto klasifikuojama kaip `Recon`.

Dar vienas rezultatas, prieštaraujantis pradinei prielaidai: prižiūrimas modelis, mokymo metu **niekada nematęs** kurios nors atakos klasės, ją aptinka geriau už autokoderį (dviem atvejais iš trijų). Lemiamas veiksnys — ar mokymo aibėje lieka bent viena tos pačios kategorijos klasė. Jei lieka, apibendrinimas kainuoja 0–1,5 procentinio punkto; jei kategorija ištuštėja, aptikimas krenta 21 punktu.

### Kodėl skaičiai žemesni nei literatūroje

Straipsniuose apie CICIoT2023 įprastai skelbiama 99 %+ tikslumo. Čia didžiausias pasiektas tikslumas — 0,834. Skirtumą lemia du sąmoningi sprendimai:

1. **Pašalinta 53,3 % tikslių dublikatų.** Rinkinyje kas antra eilutė yra kitos kopija, ypač potvynio atakose (41–72 %). Be šalinimo dalis testavimo aibės modeliui būtų jau matyta mokymo metu, ir rezultatas išsipūstų be jokios matomos klaidos.
2. **Naudojamas 39 požymių leidimas**, kuriame trūksta aštuonių išvestinių požymių, aprašytų originaliame straipsnyje.

Papildomas kontekstas skaičiui 0,834: 79 % visų klaidų yra painiava tarp atakų kategorijų, kur pavojaus signalas vis tiek įvyksta. Iš jų du trečdaliai — riba tarp `DoS` ir `DDoS`, kurią skiria srauto šaltinių skaičius, o šiame leidime tokio požymio nėra.

## Duomenys

**CICIoT2023**, Kaggle leidimas „official IoT flow feature dataset": 63 CSV failai, 8,7 GB, 45 019 243 eilutės, 39 požymiai + `Label`, 34 atakų klasės.

> ⚠️ Šis leidimas skiriasi nuo kanoninės 46 požymių versijos. Skirtumai, spąstai ir jų pasekmės surašyti faile **`duomenys/README.md`** — perskaitykite prieš liesdami duomenis. Kai kurios problemos tylios: nutrūkusios eilutės failų gale, `Rate = Infinity`, kitoks etikečių registras. `pandas` apie jas nepraneša.

Duomenys į Git nekeliami. Atsisiuntimas:

```bash
kaggle datasets download -d shadman1028/cic-iot2023-official-iot-flow-feature-dataset \
    --unzip -p duomenys/raw/
```

Iš viso rinkinio sudaroma darbinė imtis: dublikatai pašalinami, kiekvienai klasei paliekama iki 100 000 eilučių. Rezultatas — 2,43 mln. eilučių, padalytų 70/15/15 į mokymo, validacijos ir testavimo aibes.

## Paleidimas

`.bat` failai sunumeruoti paleidimo eile.

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

`_aplinka.bat` numerio neturi — tai bendra dalis, kurią kviečia visi kiti. Ji aktyvuoja conda aplinką `iot-ids` ir nutraukia darbą, jei aktyvi kita aplinka.

⚠️ **`08_vertinti_test.bat` liečia testavimo aibę.** Protokolas leidžia vieną prėjimą per ją: visi sprendimai — modeliai, hiperparametrai, slenksčiai, pjūviai — priimami validacijos aibėje prieš tai. `10_klaidos.bat` ir `14_palyginimas.bat` testavimo aibės neatidaro; jie skaičiuoja iš jau išsaugotų failų.

Rankiniu būdu:

```powershell
conda activate iot-ids
python patikra.py                          # aplinkos patikra
python -m src.duomenys.ikelimas patikra    # duomenu patikra
python -m src.duomenys.ikelimas imtis      # imtis.parquet (vienas kartas)
python -m src.duomenys.etiketes            # etikeciu zodyno savipatikra
python -m src.modeliai.bazinis             # modeliu kontrakto patikra
```

Aplinka: Python 3.11, conda `iot-ids`, LaTeX per MiKTeX. Priklausomybės — `requirements.txt`; tikslios versijos — `requirements-lock.txt` (patikrinta švarioje aplinkoje: 95 paketai, be konfliktų).

## Repozitorijos turinys

| Aplankas | Kas jame |
|---|---|
| `ataskaita/` | LaTeX šaltinis, 7 skyriai, generuojamos lentelės ir paveikslai |
| `src/duomenys/` | Įkėlimas, dedublikavimas, požymiai, skaidymas, balansavimas |
| `src/modeliai/` | Keturi modeliai su vienoda sąsaja (`fit` / `predict` / `predict_proba` / `issaugoti` / `ikelti`) |
| `src/eksperimentai/` | Paleidiklis, metrikos, slenksčiai, klaidų analizė, lentelių ir paveikslų generavimas |
| `src/prototipas.py` | Streamlit demonstracija: srautas → požymiai → inferencija → signalas |
| `konfig/` | YAML konfigūracijos; kiekvienas eksperimentas turi savo failą |
| `rezultatai/` | `rezultatai.csv` su visomis metrikomis, darbiniai skaičiavimai |
| `duomenys/` | Rinkinio dokumentacija; patys duomenys ne Git'e |

Ataskaitos lentelės su skaičiais generuojamos iš `rezultatai.csv`, tad rankomis jų perrašinėti nereikia ir negalima.

### Kur ieškoti atsakymo

| Klausimas | Failas |
|---|---|
| Kur kas guli, ką paleisti, kokie spąstai | `STRUKTURA.md` |
| Kas ir kada padaryta, kodėl taip nuspręsta | `DARBO_ZURNALAS.md` |
| Duomenų rinkinys: požymiai, etiketės, spąstai | `duomenys/README.md` |
| Šaltinių anotacijos | `literatura/anotacijos.md` |

## Citavimas

Duomenų rinkinys cituojamas per originalų straipsnį:

> E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, A. A. Ghorbani. *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment.* Sensors 23(13):5941, 2023. DOI: [10.3390/s23135941](https://doi.org/10.3390/s23135941)
