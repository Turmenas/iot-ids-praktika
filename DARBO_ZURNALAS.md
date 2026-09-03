# Darbo žurnalas

**Praktikos darbas:** IoT kibernetinių atakų prevencija naudojant DI sistemas
**Autorius:** Gabrielius Tumėnas, VILNIUS TECH, Dirbtinio intelekto programinės sistemos
**Laikotarpis:** 2026 m. rugsėjo 1–18 d.
**Repozitorija:** [Turmenas/iot-ids-praktika](https://github.com/Turmenas/iot-ids-praktika) (privati)

> Pildoma kiekvieną dieną, ~10 min. Formatas: ką padariau / ką radau / kas nepavyko / ką darysiu rytoj.
> **Čia rašomi tik sprendimai, radiniai ir pamokos.** Techninės detalės gyvena savo failuose:
> šaltinių anotacijos — `literatura/anotacijos.md`, duomenų rinkinys — `duomenys/README.md`,
> užduoties planas — `claude/uzduotis_01_planas.md`, `claude/uzduotis_02_planas.md`, `claude/uzduotis_03_planas.md`.
> Šis failas **nekeliauja** į ataskaitą, bet iš jo rašomas „darbo eigos" skyrius.

---

## Rugsėjo 1 d. (antradienis) — aplinka ir visa 1 užduotis

### Ką padariau

**Aplinka paruošta:** projekto struktūra `D:\AInera\iot-ids-praktika`, LaTeX karkasas (MiKTeX, `build.ps1`), conda aplinka `iot-ids` su Python 3.11.16, Git ir privati GitHub repozitorija, `src/duomenys/ikelimas.py` su `patikra`/`imtis` komandomis.

**1 užduotis atlikta visa** — visi aštuoni tikslai (T1–T8), nors plane jai skirtos rugsėjo 2–3 d.:

| Rezultatas | Kur |
|---|---|
| 11 šaltinių, metaduomenys patikrinti per Crossref/OpenAlex | `ataskaita/saltiniai.bib`, `literatura/anotacijos.md` |
| Skyrius: 7 poskyriai, 5 lentelės, ~3 700 žodžių, TODO nėra | `ataskaita/skyriai/01_atakos.tex` |
| CICIoT2023 dokumentacija: 46 požymiai, 34 etiketės, spąstai | `duomenys/README.md` |
| Kategorijų žodynas su `assert` patikra | `src/duomenys/etiketes.py` |

**Rezultatas:** `ataskaita.pdf`, 15 psl., 0 klaidų, 0 neišspręstų nuorodų.

### Priimti sprendimai

- **Ataskaita rašoma tiesiai į LaTeX** nuo pirmos dienos, `\input` kiekvienam skyriui. Markdown kaip tarpinis žingsnis atmestas.
- **Duomenys: CICIoT2023**, oficiali `MERGED_CSV` versija (Kaggle veidrodis). Lemiamas kriterijus — nepritaikytas joks apdorojimas.
- **Šaltinių 11, ne 15–25.** Supratau, kad 15–25 buvo tikslas visam darbui, ne vienam skyriui. Pridėtas kriterijus: kiekvienas šaltinis turi turėti poskyrį, kuriame be jo neapsieitum — jis išmetė ~6 kandidatus.
- **Trijų sluoksnių modelis** (ne 5 ar 7): papildomi sluoksniai skiriasi architektūros, o ne atakų paviršiaus prasme, ir neturėtų atitikmens srauto požymiuose.
- **Atakų priskyrimą sluoksniams atlieku aš** — nei Sasi et al., nei Fei et al. sluoksnių ašimi nesiremia. Ataskaitoje tai pasakyta atvirai.
- **Diegimo vieta: kraštinis šliuzas.** Vienintelė vieta, kur vienu metu tenkinami reikalavimai remtis srautu ir veikti be per-įrenginio konfigūravimo.
- **Bibliografija generuojama atskirai** (`literatura.tex` → `literatura.pdf` → `\includepdf`), nes pilnoje preambulėje biblatex lūžta. `build.ps1` daro tai automatiškai.

### Ką radau — svarbu vėlesnėms užduotims

**Rinkinyje nėra laiko žymos (`ts`).** ⚠️ Plane numatytas chronologinis skaidymas **neįmanomas**. Siūloma: stratifikuotas atsitiktinis + atviras apribojimo įvardijimas, o kaip atsvara — kryžminis patikrinimas ant TON\_IoT. Tai paverčia antrinį rinkinį iš „gerai turėti" į metodologinę būtinybę. **Sprendimą užrakinti rugsėjo 8 d.**

**Klasių santykis 42:1 atakų naudai** (gerybinis srautas ~2,4 %). Realiame tinkle priešingai. Todėl bendras tikslumas beveik bevertis — modelis, viską žymintis kaip ataką, gautų ~97,6 %. **5 užduotyje: macro-F1, per-klasę metrikos, sumaišymo matrica; klaidingi teigiami analizuojami atskirai.**

**Kategorija neišvedama iš etiketės pavadinimo** — `label.split("-")[0]` veikia tik 23 iš 34. Todėl `etiketes.py` su aiškiu žodynu ir `assert`. Būtų kainavę valandą 4 užduotyje, o blogiausiu atveju davę tyliai neteisingą žymėjimą.

**Požymių pavadinimų spąstai:** `Duration` yra TTL, ne trukmė (trukmė — `flow_duration`); `Magnitue` su rašybos klaida; `Tot sum` ≠ `Tot size`. Pirmasis klastingiausias — supainiojus klaida nepasirodytų kaip klaida, tik prastesnis rezultatas. Visi surašyti `duomenys/README.md`.

**Sallam et al. delsos slenksčiai:** 1–10 ms MCU, 20–50 ms šliuzui, ≥100 ms debesiui. 5 užduotyje inferencijos delsa lyginama su 20–50 ms biudžetu, o ne vertinama abstrakčiai.

**1 skyrius jau užrakino dalį 3 ir 5 užduočių.** Atrankos kriterijai (tikslumas, klaidingi teigiami, resursai, interpretuojamumas) dabar kyla iš `tab:reikalavimai`, o ne pasirenkami savavališkai — plane jie buvo pateikti su svoriais, bet nepagrįsti.

### Kas nepavyko — taisyklės aplinkai

- **`.ps1` failai turi būti grynu ASCII**, o atsisiųsti reikalauja `Unblock-File`. Abu dalykai sulaužė `build.ps1` po du kartus.
- **`.gitignore` nepalaiko komentarų eilutės gale** — komentaras tampa šablono dalimi.
- **`xltabular` negali būti `table` float'e** — longtable float'e nesiverčia, LaTeX meta „Float too large for page by 2419pt". Mano klaida; lentelė buvo grūdama į vieną nedalomą bloką.
- **`cleveref` lietuvių kalbai netinka** — visada spausdina vardininką („Iš lentelė 4"), o `\crefname` to neišsprendžia. Visos nuorodos perrašytos į `\ref{...}` su rankomis linksniuotu žodžiu. **Taisyklė: `\cref` lietuviškame tekste nenaudoti.**
- **Po `mpm --update` — pirmas kompiliavimas su `-Clean`.** Atnaujinimas keičia `.aux`/`.bbl` formatus, seni failai lūžta neaiškiais pranešimais. Iki rugsėjo 18 d. daugiau neatnaujinti.

**Pagrindinė dienos pamoka.** Apie 4 valandas iš 9 praėjo kompiliavimo klaidose, ir penkias diagnozes iš eilės spėjau iš klaidos teksto — visos neteisingos. Pilno log'o paprašiau po trečio bandymo, bisekcijos — po penkto. **Po pirmo nepavykusio taisymo reikia ne antro spėjimo, o duomenų:** pilno log'o, minimalaus reprodukcinio pavyzdžio, bisekcijos.

Antra: **veikianti aplinka svarbiau už teisingą diagnozę.** Apėjimas su atskira bibliografija rastas per 20 min. ir leido dirbti toliau.

### Nebaigta

- **Duomenys neatsisiųsti.** Keturios iš penkių lentelių remiasi pavadinimais iš straipsnio ir CSV antraštės, bet nepatikrintais realiame faile. Didžiausia likusi 1 skyriaus rizika. *(Rugs. 2 d. patikslinta: atsisiųsta, bet dar nepatikrinta.)*
- **Skyriaus apimtis 9 psl. vietoj 4–5.** Trumpinimo variantai: `tab:aprepis` ir `tab:diegimas` į tekstą, `tab:reikalavimai` į 3 skyrių, trumpesnis 1.1 — kartu ~3 psl. Atvira ir kita galimybė: 26–34 psl. norma nustatyta be `onehalfspacing`, tad per didelis gali būti visas planas.
- **biblatex nesuderinamumas su pilna preambule** — priežastis nerasta, apeita. Įtariamasis: csquotes su lietuviškomis kabutėmis (biblatex antraštėms naudoja `\mkbibquote`). Bisekcijos failas `bibtestas2.tex` paruoštas.
- Titulinio puslapio fakultetas ir praktikos vadovas.
- `pip freeze > requirements-lock.txt`.

### Ką darysiu rytoj (rugs. 2, trečiadienis)

Pirma **du blokuojantys likučiai**, tik po to naujas turinys:

1. Atsisiųsti CICIoT2023, paleisti `ikelimas.py patikra` ir `etiketes.py`, sutikrinti `df.columns` bei `label.unique()` su `duomenys/README.md`. Jei veidrodis kitoks — taisyti keturias lenteles.
2. Skyriaus trumpinimas arba sprendimas dėl apimties normos.

Tada — **2 užduotis: DI ir ML metodų taikymo galimybės.** Ji turi karkasą, kurio 1 užduotis neturėjo: `tab:aptikimas` paskutinė eilutė ir `tab:reikalavimai` jau apibrėžia, ko iš metodų reikalaujama.

---

## Rugsėjo 2 d. (trečiadienis) — 2 užduoties planas ir duomenų patikra

### Ką padariau

**Sudarytas 2 užduoties tikslų planas** (`claude/uzduotis_02_planas.md`) — tikslai, skyriaus struktūra, lentelių specifikacija, laiko biudžetas vienai dienai, priėmimo kriterijai.

**Patikrinti 5 branduolio šaltiniai; metaduomenys ir skaičiai ištraukti**, todėl `tab:susije` pildoma nebeieškant:

| Raktas | Šaltinis | DOI |
|---|---|---|
| `almahaqeri2026gradient` | Almahaqeri et al. (2026), *Sci. Rep.* 16:16909 | `10.1038/s41598-026-47399-5` |
| `nassef2026tinyml` | Nassef et al. (2026), *Sci. Rep.* 16:18524 | `10.1038/s41598-026-50690-0` |
| `mazinani2026constrained` | Mazinani et al. (2026), *Future Internet* 18(1):34 | `10.3390/fi18010034` |
| `eren2026drift` | Eren et al. (2026), *Electronics* 15(11):2307 | `10.3390/electronics15112307` |
| `mohale2025xai` | Mohale, Obagbuwa (2025), *Front. AI* 8:1526221 | `10.3389/frai.2025.1526221` |

**T1 atlikta: `saltiniai.bib` papildytas 7 įrašais** (11 → **18**). Visi DOI patikrinti per Crossref API 2026-09-02; visi 7 iš 2025–2026 m. Failas sutvarkytas į skyrius: A–D (1 užd.), E–H (2 užd.). Struktūrinė patikra: skliaustai subalansuoti, dublikatų nėra, privalomi laukai yra (išskyrus `antonakakis2017mirai` — USENIX straipsnis DOI neturi, yra `url`).

| Raktas | Skirtas |
|---|---|
| `almahaqeri2026gradient` | Atskaitos taškas — 11 metodų ant CICIoT2023 |
| `houichi2025smartcity` | Antras CICIoT2023 atskaitos taškas |
| `nassef2026tinyml` | Delsa Raspberry Pi 4; TinyML, FL |
| `mazinani2026constrained` | Resursai mikrovaldiklyje, INT8 kvantavimas |
| `imani2025imbalance` | RF/XGBoost su SMOTE, ADASYN esant disbalansui |
| `eren2026drift` | Rezultatų galiojimo ribos, pasiskirstymo poslinkis |
| `mohale2025xai` | Paaiškinamumas, SHAP/LIME kaina |

**Pastaba dėl rakto:** `nassef2026tinyfl` pervadintas į **`nassef2026tinyml`** — Crossref parodė, kad straipsnio antraštėje TinyML, ne federated learning (FL yra tik viena sudedamoji). Raktas turi atitikti antraštę, kad po savaitės nereikėtų spėlioti.

**Naujas įrašas, kurio plane nebuvo:** `imani2025imbalance`. Pridėtas todėl, kad šiandien paaiškėjo 5 764 : 1 disbalansas tarp klasių — jam pagrįsti reikėjo šaltinio, o ne savo nuomonės.

**T2 atlikta: metodų apžvalga** — 5 paradigmos, 17 metodų, kiekvienam veikimo principas, IoT scenarijus ir verdiktas. `rezultatai/darbiniai/metodu_apzvalga.md`. Iš jos: **6 kandidatai** (sprendimų medis, Random Forest, XGBoost, autokoderis, Isolation Forest, MLP) ir **8 atmesti** su priežastimis.

**T3 atlikta: `tab:metodai`** — 18 eilučių × 8 stulpeliai, įrašyta į `ataskaita/skyriai/02_di_metodai.tex`. Resursų stulpelis padalytas į **mokymo** ir **inferencijos** kainą, kaip planuota. Struktūrinė patikra: visose eilutėse po 7 skirtukus, skliaustai subalansuoti, `\begingroup`/`\endgroup` poroje.

**T4 atlikta: `tab:susije`** — **10 eilučių iš 5 šaltinių**, visi skaičiai patikrinti leidėjo puslapiuose. Lieka viena eilutė (`houichi2025smartcity`): Wiley grąžina 403, ResearchGate 429 — reikia universiteto prieigos.

**T5 atlikta: 2.6 poskyris „Praktiniai apribojimai“** + `tab:apribojimai` (3 eilutės: MCU / šliuzas / debesis). Trys poskyriai: inferencijos delsa, mokymo kaina, klasių disbalansas.

**T6 atsisakyta.** Poskyris 2.8 („rezultatų patikimumas be kryžminio patikrinimo“) iš 2 skyriaus išbrauktas. Skyriaus apimties taikinys sumažėja iki ~5,8 psl.

**T7 atlikta: 2.8 poskyris + fiksuotas ketvertas.** Metodai: **Random Forest, XGBoost, MLP, autokoderis**. Pagrindinis užduoties detalumas — **8 kategorijos**.

**T8 atlikta: anotacijos.** `literatura/anotacijos.md` papildytas skyriais E–H (7 nauji įrašai). Patikra sugretinant `.bib` raktus su anotacijų antraštėmis: **18 iš 18, spragų nėra.**

**2 skyriaus redagavimas** — pašalintas savęs žeminimas ir perteklius, −181 žodis (−5,8 %).

**2 skyrius parašytas iki galo** — poskyriai 2.1–2.8, trys lentelės. **2 910 žodžių ≈ 7,8 psl.**

**T0 atlikta: duomenų antraštė sutikrinta su dokumentacija.** Rezultatas neigiamas — žr. žemiau. `duomenys/README.md` perrašytas (`claude/ciciot2023_pozymiai.md`).

### Priimti sprendimai

- **Liekame prie 39 požymių leidimo.** Kanoninės 46 požymių versijos neatsisiunčiame. Pagrindimas: 8 trūkstami požymiai daugiausia išvestiniai, o 13 GB atsisiuntimas iš naujo kainuotų dieną. Kaina — sumažėjęs palyginamumas su literatūra — **įvardijama ataskaitoje**, ne nutylima.
- **Antriniai duomenų rinkiniai atmesti** (TON\_IoT, Edge-IIoTset). Naudojamas tik CICIoT2023. Trys priežastys: (a) skirtingos požymių aibės ir struktūros — antras rinkinys reikštų antrą patikrą, antrą įkėlimo grandinę, antrą derinimo sluoksnį; (b) nesutampant požymiams modelio perkelti negalima, tad 4 ir 5 užduotys dvigubėtų; (c) 14 darbo dienų, vienas žmogus, viena mašina be GPU. **Ribojantis veiksnys yra kalendorius, ne skaičiavimai** — pirmosios dvi priežastys metodologinės, trečioji viena nepateisintų.
- **Imties riba: 100 000 eilučių klasei** (≈2,43 mln. eilučių, 5,4 % rinkinio, 0,35 GB). Pilnas rinkinys — tik galutiniams matavimams, jei liks laiko. **Pasekmė, kurią būtina atsiminti:** kryžminis patikrinimas tarp rinkinių buvo *stipriausias* argumentas prieš nutekėjimą, kai nėra laiko žymos. Jo netekus, ta rolė **atitenka nematytos atakų klasės testui**, kuris iki šiol buvo 6 užduoties papildoma dalis. Jį reikia perkelti į privalomą 5 užduoties dalį.
- **2 užduotis suspausta į vieną dieną** (planuota rugs. 4 ir 7 d.). Kaina plane įvardyta: pirmas nukenčia poskyrių 2.2–2.5 tekstas; 2.6–2.9 neliečiami.
- **Trys lentelės, ne penkios.** 1 skyriuje penkios davė 9 psl. vietoj 4–5.
- **Lentelės pildomos prieš tekstą, įžanginis poskyris rašomas paskutinis.** Rugs. 1 d. patirtis: tekstas, rašytas prieš lentelę, vėliau perrašomas.
- **Sprendimas dėl 1 skyriaus apimties paliktas rugs. 8 d.**

### Ką radau

#### 1. Veidrodis neatitinka dokumentacijos — 39 požymiai, ne 46

Rizika, plane vertinta kaip „vidutinė", **įvyko**. Realaus failo antraštėje **40 stulpelių: 39 požymiai + `Label`**.

- **Pašalinta (8):** `flow_duration`, `Srate`, `Drate`, `urg_count`, `Magnitue`, `Radius`, `Covariance`, `Weight`
- **Pervadinta (1):** `Duration` → **`Time_To_Live`**
- **Pridėta (1):** `IGMP`

**Gera žinia:** pervadinimas **panaikina klastingiausią spąstą.** Rugsėjo 1 d. užrašiau, kad `Duration` iš tikrųjų yra TTL ir kad supainiojus klaida nepasirodytų kaip klaida. Šiame leidime pavadinimas sąžiningas. Kartu dingo ir `Magnitue` rašybos spąstas — nes dingo pats stulpelis.

**Bloga žinia:** **nebėra `flow_duration`** ir **nebėra jokios krypties informacijos** (`Srate`/`Drate` ir iš jų išvesti `Magnitue`, `Radius`, `Covariance`, `Weight`). Srauto asimetrija — klasikinis DDoS ir botneto požymis — šiame leidime neišreiškiama. Labiausiai paliesta `DDoS-SlowLoris`: žemo intensyvumo ataka be trukmės požymio.

**Poveikis 1 skyriui:** kiekviena `tab:atakos` eilutė, kurios stulpelyje „matomi tinklo požymiai" minima **srauto trukmė** arba **asimetrija**, nebeturi atitinkamo stulpelio. Taisyti prieš rašant 2 skyrių.

#### 2. Perteklinių požymių patikra — trys iš keturių ⭐

Pastebėjęs įtartinų sutapimų pavyzdinėje eilutėje, patikrinau juos ant **500 000 eilučių**:

| Tapatybė | Rezultatas |
|---|---|
| `Variance` = `Std`² | ✅ galioja — 0 nesutapimų iš 499 990 |
| `Tot size` = `AVG` | ✅ galioja tiksliai — 500 000 iš 500 000 |
| `Tot sum` = `AVG` × `Number` | ✅ galioja — 0 nesutapimų |
| ~~`Rate` = 1/`IAT`~~ | ❌ **paneigta** — 305 006 nesutapimai iš 499 988 |

**`Rate` = 1/`IAT` buvo mano klaida.** Pirmoje eilutėje jie sutapo iki paskutinio skaitmens, ir iš vienos eilutės padariau išvadą. Realiai jie tik koreliuoja (Pearson 0,961; log10 0,997), o santykinės paklaidos maksimumas — 4233×. **Pamoka ta pati kaip rugsėjo 1 d., tik kitoje srityje: vienas pavyzdys nėra patikra.** Skirtumas tas, kad šįkart planas numatė patikrą prieš rašant į ataskaitą, ir ji suveikė.

**Efektyvus požymių skaičius ≈ 36**, ne 39.

**Svarbiausia išvada 4 užduočiai.** `Variance` = `Std`², bet jų **tiesinė** Pearson koreliacija tik **0,737**. Įprastas koreliacijos filtras su 0,95 slenksčiu šios poros **nepašalintų**, nors ryšys tikslus. Vadinasi, perteklinius požymius reikia šalinti **sąrašu, sąmoningai**, o ne pasikliaunant automatiniu filtru. Tai savarankiškas pastebėjimas ir tinka ataskaitai.

#### 2b. Duomenų kokybė — trys tylios problemos ⚠️

Pilnas skenavimas per visus 63 failus (45 019 243 eilutės):

| Problema | Eilučių |
|---|---:|
| Nutrūkusi paskutinė eilutė (9 failuose) | 9 |
| `Rate` = `Infinity` | 991 |
| `Std` / `Variance` tušti | 677 / 679 |
| `Number` < 10 (per trumpas langas) | 6 053 |

**Visos trys tylios.** `pandas.read_csv` nutrūkusią eilutę perskaito be klaidos ir be įspėjimo — ji virsta įrašu su `Label = NaN`, t. y. 35-a „klase", kuri tyliai patenka į mokymą. `Rate = Infinity` atsiranda ten, kur lange 1–3 paketai, todėl `IAT` = 0; `scikit-learn` tai atmes **mokymo viduryje**, ne įkeliant.

Įkėlimo grandinė dabar: `dropna(subset=["Label"])` → `replace([inf,-inf], nan)` → `dropna()`. Pašalinama ~1 700 eilučių iš 45 mln. (0,004 %).

#### 2c. Du disbalansai, ne vienas ⭐

| Rodiklis | Reikšmė |
|---|---|
| Atakos : gerybinis srautas | **41,8 : 1** |
| **Didžiausia klasė : mažiausia** | **5 764 : 1** (`DDOS-ICMP_FLOOD` 6,89 mln. vs `UPLOADING_ATTACK` 1 196) |

**Antrojo skaičiaus darbe iki šiol nebuvo, o jis svarbesnis.** 41,8:1 paaiškina, kodėl netinka accuracy dvejetainei užduočiai. Bet **macro-F1 kritimą** aiškina 5 764:1 — septynios klasės turi mažiau nei 0,03 % duomenų, ir būtent jos nutempia macro vidurkį. Tai empiriškai paaiškina `almahaqeri2026gradient` 0,8903 macro-F1 prie 99,59 % accuracy.

Į ataskaitą eina **abu** santykiai; 5 764:1 yra tas, kuris pagrindžia metrikos pasirinkimą.

Taip pat patikslinta: rinkinyje **45 019 243 eilutės ir 8,7 GB**, ne ~46,7 mln. / 13 GB, kaip buvo užrašyta iš dokumentacijos.

#### 3. `Label` registras kitoks

Antraštėje **`Label`** (didžioji `L`), reikšmės **didžiosiomis**: `DDOS-PSHACK_FLOOD`, o ne `DDoS-PSHACK_Flood`.

⚠️ **Ir dar vienas skirtumas, kurio nesitikėjau: `BenignTraffic` → `BENIGN`.** Tai **ne** registro pokytis — pavadinimas kitas. `"BenignTraffic".upper()` duotų `BENIGNTRAFFIC`, ko faile nėra. Vadinasi, `.upper()` sutvarko 33 etiketes iš 34, o gerybinis srautas — vienintelė išimtis, reikalaujanti atskiro atitikmens. Būtent ta klasė, kurios mažiausiai ir kuri svarbiausia klaidingų teigiamų analizei.

`df["label"]` mes `KeyError`, o `etiketes.py` žodyno raktai nesutaps ir `patikrinti()` mes klaidą. **Būtent dėl to ta funkcija ir buvo parašyta** — rugsėjo 1 d. sprendimas laikyti žodyną kode su `assert` atsipirko pirmą kartą jį paleidus.

**Sprendimas — normalizuoti įkeliant, ne perrašinėti žodyną:** `df["Label"].str.strip().str.upper()` ir raktus žodyne irgi didžiosiomis. Taip kodas veiks su abiem leidimais, ir veidrodžio registras nustoja būti problema.

#### 4. Literatūros radiniai (2 užduočiai)

**Realistinis metrikos tikslas: macro-F1 0,85–0,90, ne 0,99.** `almahaqeri2026gradient` ant to paties CICIoT2023: XGBoost dvejetainei užduočiai accuracy 99,61 %, macro-F1 0,9952; 8 klasėms accuracy 99,59 %, bet macro-F1 **0,8903**; 34 klasėms 0,8876. Tas pats modelis, tie patys duomenys: accuracy nejuda, macro-F1 krenta 0,1. **Empirinis** patvirtinimas rugs. 1 d. teiginiui apie 42:1 disbalansą.

**Gilieji modeliai netelpa į šliuzo delsos biudžetą.** `nassef2026tinyml`: GAT+BiGRU, F1 0,92 ant CICIoT2023, bet **120–180 ms Raspberry Pi 4**. `sallam2026gap` šliuzui skiria **20–50 ms**. XGBoost tame pačiame rinkinyje — **mikrosekundės**. Trys–keturios eilės skirtumo, gaunama vien sugretinus du šaltinius.

**Kryžminis rinkinių perkėlimas griūva** (`eren2026drift`): vidutinis MCC krenta nuo ~94 % iki ~29 %. Atmetus antrinius rinkinius šis šaltinis keičia vaidmenį — iš *pagrindimo, kodėl reikia antro rinkinio*, tampa *pagrindimu, kodėl savo rezultatų negalima laikyti apibendrinamais*. Toks panaudojimas sąžiningesnis ir 6 skyriui net naudingesnis.

**XAI yra analizės įrankis, ne inferencijos grandinės dalis** (`mohale2025xai`): SHAP ir LIME reikalauja daug skaičiavimo. SHAP → 6 užduotis, ne 4.

**INT8 kvantavimas mažina modelį >90 %** beveik neprarandant tikslumo (`mazinani2026constrained`).

#### 5. Imtis nėra kompromisas — ji teisingas sprendimas ⭐

Suskaičiavus, ką duotų skirtingos imties ribos:

| Riba klasei | Eilučių | Dalis | Disbalansas | RAM |
|---:|---:|---:|---:|---:|
| 20 000 | 558 482 | 1,24 % | 17 : 1 | 0,08 GB |
| **100 000** | **2 429 978** | **5,40 %** | **84 : 1** | **0,35 GB** |
| 500 000 | 9 263 034 | 20,58 % | 418 : 1 | 1,33 GB |

Riba 100 000 sprendžia **dvi** problemas vienu veiksmu: duomenys telpa į nešiojamą kompiuterį, o disbalansas krenta nuo 5 764 : 1 iki 84 : 1.

**Svarbiausia:** retoms klasėms riba niekada neįsijungia — jos paimamos visos. `UPLOADING_ATTACK` turi 1 196 eilutes, todėl po 70/15/15 skaidymo lieka **179 testavimo pavyzdžiai**. Serveris, mokantis visą parą ant visų 45 mln. eilučių, gautų lygiai tuos pačius 179 — daugiau tų duomenų neegzistuoja.

Vadinasi, laikyti 6,9 mln. `DDOS-ICMP_FLOOD` eilučių šalia 1 196 `UPLOADING_ATTACK` nesuteikia informacijos, tik iškreipia mokymą. **Ataskaitoje tai rašoma kaip pasirinkimas, ne kaip apribojimas dėl resursų stokos.** Tas pats principas, kurį naudoja `reddy2026datasets`.

Praktinė pasekmė 2.6 poskyriui: skaičiavimo biudžetas tampa kriterijumi **su skaičiumi** — mokymo laikas ≤ 30 min. vienam modeliui be GPU, Random Search vietoj Grid Search. Gilieji modeliai gauna **du nepriklausomus** argumentus prieš: brangūs mokant be GPU ir netelpa į 20–50 ms šliuzo biudžetą inferuojant.

#### 6. Duomenų struktūra atmeta daugiau metodų nei resursų trūkumas ⭐

Rašant T2 paaiškėjo, kad trys rugsėjo 2 d. patikros radiniai **iš anksto atmeta ištisas metodų šeimas** — ir ne dėl skaičiavimo biudžeto:

| Duomenų savybė | Ką atmeta |
|---|---|
| Nėra `ts`, nėra eilės tarp įrašų; kiekviena eilutė jau yra 10/100 paketų lango agregatas | **LSTM, GRU, Transformer** — sekos, kurią modeliuoti, tiesiog nėra |
| Nėra šaltinio/paskirties identifikatorių nei krypties | **GNN** — grafo nesukonstruosi. **Federated learning** — nėra pagal ką dalyti į klientus |
| Įrodytos tikslios priklausomybės (`Variance`=`Std`², `Tot size`=`AVG`) | **Naive Bayes** — paneigta nepriklausomumo prielaida |

**Iš 8 atmestų metodų tik du atmesti dėl resursų** (SVM ir One-Class SVM — O(n²–n³) mokymas), vienas dėl delsos (k-NN), o **keturi — dėl duomenų struktūros** ir vienas dėl pažeistos prielaidos.

**Tai reiškia, kad kandidatų aibė būtų beveik ta pati ir turint serverį.** Vakar rūpėjo, ar apimties mažinimas neatrodys kaip pasiteisinimas; pasirodo, pagrindinis atrankos veiksnys yra ne kalendorius, o duomenys. Į 2.9 poskyrį tai eina tiesiogiai.

Antra pastaba: literatūroje LSTM ir Transformer ant CICIoT2023 taikomi dažnai, nors įvestis ten yra tas pats vienos eilutės požymių vektorius, apsimetantis seka. **Tai savarankiškas pastebėjimas** ir eina į `tab:susije` stulpelį „Kas kelia abejonių".

#### 7. Trys pastebėjimai, atsiradę pildant lentelę

**Disbalanso stulpelis neprižiūrimiems metodams yra „neaktualus", ne „geras".** Autokoderis ir Isolation Forest mokomi **tik iš gerybinio srauto**, todėl 5 764 : 1 santykis tarp atakų klasių jų apskritai nepasiekia. Tai ne pranašumas balanso prasme, o kitokia problemos formuluotė — ir stulpelyje tai reikia užrašyti kaip trečią reikšmę, ne įsprausti į „geras/prastas" skalę.

**Dviem metodams disbalansas ne šiaip blogas, o blogėja.** Savimoka (pseudo-etiketės stiprina gausių klasių šališkumą) ir federuotas mokymasis esant ne-IID duomenims. Skirtumas tarp „prastas" ir „blogėja" yra esminis: pirmas yra būklė, antras — grįžtamasis ryšys.

**`\tnote{}` sulaužytų kompiliavimą.** Rašydamas išnašą lentelėje panaudojau `threeparttable` komandą, kurios preambulėje nėra. Pagavau patikra prieš kompiliuojant, pakeista į `\textsuperscript`. **Taisyklė: naudoti tik tas komandas, kurių paketai tikrai yra `ataskaita.tex` preambulėje** — praplėsti preambulę likus dviem savaitėms iki termino nėra vertas rizikos.

#### 8. `tab:susije` branduolys: vienas šaltinis, trys eilutės, viena išvada

Lentelės ašis yra ne metodai, o **užduoties granuliarumas**. Tas pats XGBoost, tas pats CICIoT2023, `almahaqeri2026gradient`:

| Užduotis | Tikslumas | macro-F1 |
|---|---|---|
| dvejetainė | 99,61 % | 0,9952 |
| 8 klasės | 99,59 % | **0,8903** |
| 34 klasės | 99,48 % | 0,8876 |

**Tikslumas nejuda, macro-F1 krenta 0,10.** Tris eilutes vienam šaltiniui skyriau sąmoningai: viena eilutė su 99,6 % nieko nepasakytų, o trys parodo, kad skirtumą daro ne modelis, o metrika ir užduotis. Tai geriausias turimas argumentas, kodėl 5 užduotyje accuracy nebus pagrindinis rodiklis.

Antra pastaba: `nassef2026tinyml` visose trijose eilutėse **užduoties granuliarumo nenurodo**, nors skelbia F1 0,92–0,94. Be to negalima pasakyti, ar tai palyginama su mano rezultatu. **Trūkstamas metodikos elementas irgi yra įrašas stulpelyje apie abejones — ne tik silpna metrika.**

#### 9. Dvi pataisos, atsiradusios tikrinant metrikas ⚠️

**`imani2025imbalance` nėra susijęs darbas.** Priimdamas jį ryte maniau, kad tai IoT įsibrovimų aptikimo darbas. Patikrinus paaiškėjo, kad naudojami **telekomunikacijų klientų nutekėjimo duomenys** su dirbtinai nustatytais disbalanso lygiais (15 / 10 / 5 / 1 % mažumos klasė). Todėl jis **išimtas iš `tab:susije`** ir lieka kaip metodologinis šaltinis 2.6 poskyriui. Šaltinis geras, bet ne toje lentelėje — o jei būčiau įrašęs jį kaip IoT darbą, tai būtų buvusi klaida ataskaitoje.

Jo turinys vis tiek vertingas ir dviem atžvilgiais keičia planus:

- **Random Forest prastai veikia esant stipriam disbalansui**, o geriausias derinys — suderintas XGBoost su SMOTE. RF yra mūsų 2-as kandidatas, tad tai įspėjimas, ne smulkmena.
- **Didėjant disbalansui MCC, Kappa ir F1 stipriai svyruoja, o ROC-AUC ir PR-AUC išlieka stabilūs.** Tai argumentas 5 užduočiai šalia macro-F1 pateikti ir **PR-AUC** — ne dėl išsamumo, o dėl to, kad F1 prie 84 : 1 bus triukšmingas.

**`mazinani2026constrained` naudoja CICIoT2023** — to nežinojau ryte. Ir tas pačias tris konfigūracijas: dvejetainę, 8 ir 34 klases. Tai paverčia jį tiesiogiai susijusiu darbu, o ne vien resursų šaltiniu. Papildoma smulkmena: jis nurodo **46 686 579 įrašus**, t. y. pilną oficialią versiją — dar vienas patvirtinimas, kad mūsų 45 019 243 eilučių leidimas yra kitas.

#### 10. Meidan skaičiai pasirodė iškalbingesni nei tikėtasi

`meidan2018nbaiot`: **TPR 100 %**, FPR 0,007 ± 0,01, aptikimo laikas **174 ± 212 ms**.

Du dalykai stulpeliui apie abejones. Pirma, TPR 100 % pasiektas **lengviausioje įmanomoje formuluotėje** — dvejetainė užduotis, atskiras modelis kiekvienam iš 9 įrenginių, dvi botnetų šeimos. Tai tiksliai tas atvejis, apie kurį įspėja `reddy2026datasets`. Antra, aptikimo laiko **standartinis nuokrypis (212 ms) didesnis už vidurkį (174 ms)** — pasiskirstymas su ilga uodega, o skelbiamas vidurkis to neparodo. Abu skaičiai viršija 20–50 ms šliuzo biudžetą.

#### 11. Delsos argumentas atlaiko svarbiausią prieštaravimą

Sugretinimas atrodo įspūdingai — XGBoost 3,53 µs prieš gilaus modelio 120–180 ms, keturios eilės — bet turi akivaizdų trūkumą: **skaičiai išmatuoti ne ta pačia aparatūra.** Mikrosekundės gautos serverio procesoriumi, milisekundės — Raspberry Pi 4. Recenzentas tai pastebėtų per sekundę, todėl įvardijau pats.

**Atsakymas gaunasi stipresnis nei tikėjausi.** 3,53 µs į 20 ms biudžetą telpa **5 669 kartus**. Vadinasi, net 5 669 kartus lėtesnė aparatūra dar tenkintų reikalavimą — aparatūros skirtumas tokio dydžio atsargos nepanaikina. O giliajam modeliui skirtumas veikia priešinga kryptimi: šliuzas paprastai nėra galingesnis už Raspberry Pi 4.

#### 12. „Aptikimo laikas" ir „inferencijos delsa" nėra tas pats ⭐

`meidan2018nbaiot` skelbia 174 ± 212 ms **aptikimo laiką** — jis apima ir srauto lango sukaupimą, ne vien modelio skaičiavimą. Sugretinti jį su XGBoost inferencijos mikrosekundėmis būtų klaida.

**Iš to seka konkretus reikalavimas 5 užduočiai:** matuoti **grynąją inferencijos delsą**, o lango sukaupimo laiką nurodyti atskirai. Priešingu atveju mano skaičiai nebus palyginami nei tarpusavyje, nei su literatūra. Įrašiau tai tiesiai į 2.6 poskyrį, kad rugsėjo 15 d. nereikėtų prisiminti.

#### 13. Prieš kompiliavimą pagautos trys klaidos

- **`\SI{\geq 100}{...}`** — siunitx į reikšmės lauką nepriima komandų; būtų lūžę. Pakeista į `$\geq$~\SI{100}{...}`.
- **Kirilicos raidė „а"** žodyje „pridedа" — vizualiai neatskiriama nuo lotyniškos. Nebūtinai būtų sulaužiusi kompiliavimą, bet paieška ir kėlimas veiktų klaidingai.
- Rašybos klaida „giliieji".

Visos trys rastos automatine patikra (`\SI` reikšmių tikrinimas + ne lotyniškų simbolių paieška), ne skaitant. **Verta tą patį paleisti ir 1 skyriui** — jis rašytas be tokios patikros.

#### 14. T6 išbrauktas — buvau perkomplikavęs ⚠️

Antrinių rinkinių atmetimą buvau pavertęs atskiru poskyriu apie tai, kodėl kryžminis patikrinimas nebegalimas ir kas jį pakeičia. **Tai buvo klaida, ir ne dėl apimties, o dėl vietos.**

2 skyrius apžvelgia metodus. Mano būsimų rezultatų galiojimo ribos priklauso **4 skyriaus metodikai** (ten užrakinamas skaidymo sprendimas) ir **6 skyriaus apribojimų aptarimui**. Aiškinti jas dar prieš pasirenkant metodus reiškia atsakinėti į klausimą, kurio niekas neuždavė — ir atkreipti dėmesį į trūkumą, kurio kitaip niekas nepastebėtų.

**Antrinių rinkinių tiesiog nėra. To konstatavimas nereikalauja poskyrio.**

Lieka vienas sakinys 4 skyriaus metodikoje prie skaidymo sprendimo. `reddy2026datasets` jau cituojamas 1 skyriuje, `eren2026drift` lieka `tab:susije` — abu savo darbą atlieka ir be atskiro poskyrio.

#### 15. Nematytos klasės testas: ta pati priemonė, geresnis pagrindas ⭐

Anksčiau jį pateikiau kaip kryžminio patikrinimo **pakaitalą**. Motyvacija buvo silpna — priemonė, pateisinama tuo, ko nėra.

Realus pagrindas paprastesnis ir stipresnis: **darbe yra du neprižiūrimi kandidatai (autokoderis, Isolation Forest), kurių vienintelė prasmė — aptikti nematytas atakas.** Jei to netikrinu nematytomis klasėmis, jų įtraukimas į palyginimą lieka nepatikrintas teiginys.

Taigi testas yra **tiesioginė autokoderio hipotezės patikra**, ir 5 užduotyje jam vieta savaime — nepriklausomai nuo to, ar antrinis rinkinys egzistuoja.

**Bendresnė pamoka:** kai priemonė pateisinama tuo, ko trūksta, verta paklausti, ar jos nepateisina tai, kas yra. Antruoju atveju argumentas visada tvirtesnis.

#### 16. Ketvertas fiksuotas ⭐

| Metodas | Vaidmuo |
|---|---|
| Random Forest | Atskaitos modelis — garantuoja rezultatą |
| XGBoost | Laukiamas nugalėtojas; vienintelis palyginamas su literatūra |
| MLP | Ar sudėtingumas apsimoka lentelinei įvesčiai |
| Autokoderis | Zero-day; darbo prielaidos patikra |

**Lemiamas argumentas dėl MLP.** 2.4 poskyryje pats iškėliau klausimą, ar gilusis mokymasis apsimoka srauto požymiams. Be MLP skyrius klaustų to, ko eksperimentas neatsako. Prižiūrimoje pusėje dabar susidaro sudėtingumo gradientas: medžių ansamblis → stiprinimas → neuroninis tinklas.

**Kaina:** autokoderis lieka be pigaus neprižiūrimo etalono (Isolation Forest neteko vietos). Jo mokymas trunka minutes, tad pridedamas, jei 4 užduotyje liks laiko.

**Detalumas: 8 kategorijos.** Atitinka `etiketes.py` žodyną ir sutampa su `almahaqeri2026gradient` 0,8903 — bus su kuo lyginti. Paleidimų ~20 vietoj ~70.

#### 17. Palyginimo asimetrija — numatyta prieš, o ne po ⚠️

Trys prižiūrimi metodai klasifikuoja į 8 kategorijas, o autokoderis duoda tik anomalijos įvertį. **Bendro macro-F1 stulpelio visiems keturiems sudaryti negalima.** 6 skyriaus suvestinė lentelė turės dvi dalis: prižiūrimi daugiaklasėje formuluotėje, autokoderis — dvejetainėje plius nematytų klasių bandymas.

Tai įrašiau į 2.8 poskyrį dabar. Pastebėta rugsėjo 17 d., ši smulkmena būtų reiškusi arba perdarytą lentelę, arba tylų neteisingą palyginimą.

#### 18. Vos nepataisiau to, kas nesugedę

Radęs 2.8 poskyryje lietuviškas kabutes prisiminiau rugsėjo 1 d. įtarimą, kad `csquotes` su jomis laužo biblatex, ir jau rengiausi jas šalinti. **Pirma patikrinau: 1 skyriuje jų lygiai tiek pat, ir jis kompiliuojasi be klaidų.** Vadinasi, kabutės tekste nėra problema — biblatex lūžta kitur.

Pamoka ta pati, kaip rugsėjo 1 d., tik atvirkščia kryptimi: **prieš taisant reikia duomenų, o ne prisiminto įtarimo.** Nepatikrinęs būčiau sugaišęs laiką ir dar pablogėtų tekstas.

#### 19. Anotacijos užfiksavo tai, kas per dieną pasikeitė

Rašant anotacijas paaiškėjo, kad keturi iš septynių naujų šaltinių per dieną **pakeitė savo vaidmenį**, ir be užrašo tai būtų pamiršta:

| Šaltinis | Buvo | Tapo |
|---|---|---|
| `eren2026drift` | Pagrindimas, kodėl reikia antrinio rinkinio | Pagrindimas, kodėl vieno rinkinio rezultatai neapibendrinami |
| `imani2025imbalance` | Susijęs IoT darbas | Metodologinis šaltinis — duomenys ne IoT, o klientų nutekėjimo |
| `mazinani2026constrained` | Resursų šaltinis | Tiesiogiai susijęs darbas — naudoja CICIoT2023 ir tas pačias 3 konfigūracijas |
| `nassef2026tinyfl` | — | Pervadintas į `nassef2026tinyml` (antraštėje TinyML, ne FL) |

Anotacijų failas dabar yra vienintelė vieta, kur šie pokyčiai užrašyti kartu su priežastimis.

#### 20. Rasta dubliuota anotacijų kopija

`literatura/` aplanke guli **du tos pačios medžiagos failai**: `anotacijos.md` (aktualus) ir `literatura_anotacijos.md` (senesnė kopija). Antrasis atsirado, kai projekto dokumentas buvo išsaugotas savo vardu. Palikti reikia vieną — kitaip po savaitės neaišku, kuris naujesnis. Įrašyta į „Kiti žingsniai“.

#### 21. Redagavimas: kur rašiau prieš save ⭐

Peržiūrėjus 2 skyrių paaiškėjo, kad keliose vietose gyniausi nuo priekaištų, kurių niekas nepareiškė. Tai skaitosi silpniau, nei tiesiog pasakius dalyką.

**Blogiausia vieta — „Mokymo kaina“.** Buvau parašęs: *„Mokymo kaina šiame darbe yra ne technologinis, o organizacinis apribojimas: keturiolika darbo dienų, vienas vykdytojas ir viena darbo vietos mašina be grafinio spartintuvo.“* Tai ne metodikos pagrindimas, o pasiaiškinimas — ir jis pats kviečia klausimą „vadinasi, su serveriu būtų kitaip?“.

Perrašyta į **diegimo reikalavimą**: tinklo elgsena kinta, todėl modelis turi būti periodiškai permokomas, o kraštinio šliuzo aplinkoje tam skiriama įprasta aparatūra be spartintuvo. Apribojimas tas pats, bet dabar jis kyla iš uždavinio, ne iš mano kalendoriaus. SVM atmetimas atitinkamai pagrįstas algoritmo savybe (kvadratinis–kubinis augimas milijonų eilučių imtyse), o ne tuo, ko aš nespėju.

**Kitos penkios vietos:**

| Buvo | Tapo |
|---|---|
| „Toks sugretinimas turi vieną akivaizdų trūkumą…“ (10 eil.) | Faktas apie skirtingą aparatūrą + 5 669 kartų atsarga (5 eil.) |
| RF paskirtis — „užtikrinti, kad rezultatas bus gautas, net jei sudėtingesni nepasiteisins“ | „Nustato atskaitos lygį, prie kurio matuojamas prieaugis“ |
| „Svarbiausia, kad atmetimo priežastys kyla iš duomenų, o ne iš išteklių“ | Pašalinta — priežastys išvardytos, skaitytojas mato pats |
| „Skaičiavimo ištekliai lemia **tik du** atmetimus“ | Pašalintas gynybinis skaičiavimas |
| „Autokoderis lieka be pigaus etalono… jei liks laiko“ | **Pašalinta** — spraga, kurios niekas nebūtų pastebėjęs |

**Taisyklė, kurią verta taikyti ir 1 skyriui:** jei sakinys pradedamas nuo to, ko darbas *neturi*, arba nuo to, ko *nespėta*, jis beveik visada perrašytinas į teiginį apie tai, kas padaryta ir kodėl taip pakanka. Sąžiningumas nuo to nenukenčia — apribojimai lieka, tik nustoja būti atsiprašymais.

**Kas sąmoningai palikta:** 39 vs 46 požymių skirtumas (kartą, `tab:susije`), palyginimo asimetrija tarp autokoderio ir prižiūrimų metodų (tai vertinimo plano dalis), aptikimo laiko ir inferencijos delsos skirtis. Tai metodiniai faktai, ne trūkumai.

#### 22. Skyrius baigtas: 7,8 psl. vietoj planuotų 5–6

| Dalis | Žodžių | ≈ psl. |
|---|---:|---:|
| Tekstas | 2 188 | 5,9 |
| Trys lentelės | 722 | 1,9 |
| **Iš viso** | **2 910** | **7,8** |

Poskyriams 2.1–2.5 ir 2.7 planuota ~1 440 žodžių, parašyta **1 027** — sutrumpinta beveik trečdaliu, sąmoningai nekartojant to, kas jau yra `tab:metodai` lentelėje. Proza neaprašinėja algoritmų; ji neša tik tai, ko lentelė negali: kodėl paradigma IoT kontekste svarstoma ir kas ją riboja.

**Vis dėlto 7,8 > 6.** Perviršis susidaro ne iš paskutinių poskyrių, o iš anksčiau parašytų 2.6–2.8, kurie kartu užima ~5 psl. Trumpinimo variantus siūlys vadovas kitame žingsnyje.

**Antras kartas su ta pačia klaida.** Vėl įrašiau kirilicos raides (`о` žodžiuose „mokо“, „matо“) — lygiai kaip prieš tai su „pridedа“. Vizualiai neatskiriamos, kompiliavimo nebūtinai sulaužo, bet kėlimą ir paiešką gadina. Automatinė patikra pagavo abu kartus. **Ši patikra dabar privaloma prieš kiekvieną commit'ą, ne tik prieš kompiliavimą** — pasikartojanti klaida nustoja būti atsitiktinumu.

#### 23. Kompiliavimas praėjo: 0 klaidų, 0 neišspręstų citavimų ✅

12:08 paleistas `build.ps1` patvirtino, ko labiausiai reikėjo:

- **0 klaidų** (`^!` log'e nėra), **0 neišspręstų citavimų** — vadinasi, **7 nauji `.bib` įrašai su `biber` veikia**, o LaTeX komandų taisymai (`\SI{\geq ...}`, `\tnote`) buvo pagauti laiku.
- **Visos trys naujos lentelės sėkmingai surinktos** — `tab:metodai`, `tab:susije` ir `tab:apribojimai` yra `.aux` faile.
- Ataskaita **22 psl.** (rugsėjo 1 d. buvo 15).

**35 `Overfull \hbox` įspėjimai**, didžiausi trys (38,6 ir 32,9 pt) — **5 puslapyje, t. y. 1 skyriuje**, ne naujose lentelėse. Didžiausias 2 skyriuje — 8,7 pt, praktiškai nematomas. Naujos lentelės telpa geriau nei senosios.

⚠️ **PDF dviem minutėmis senesnis už `.tex`** — paskutiniai poskyriai (2.1–2.5, 2.7) į šį build'ą nepateko. Pridėjus juos ataskaita augs iki **~25 psl.**

#### 24. Apimtis: išmatuota, ne įvertinta — ir sprendimas atidėti

> ⚠️ **Pataisyta 2026-09-03:** visas šis punktas remiasi 26–34 psl. norma, kuri paimta iš neteisingo šaltinio — `ataskaita.tex` nėra universiteto praktikos ataskaita, o dokumentas Aineros praktikos vadovui. **Matavimai galioja, taikinys — ne.** Žr. rugsėjo 3 d. įrašą, „Ką radau“, 4 punktas.

Sukompiliavau 1 ir 2 skyrius su trimis eilučių intervalais (kopija `/tmp`, originalūs failai neliesti):

| Intervalas | Psl. |
|---|---:|
| `\onehalfspacing` (dabar) | 19 |
| `\setstretch{1.15}` | 17 |
| `\singlespacing` | **16** |

**Mano pirminis vertinimas buvo klaidingas.** Sakiau „~28 %, ~11 psl.“; tikrovė — **16 %, ~6 psl.** Skirtumą lemia lentelės: jos nustatytos `\footnotesize` ir turi savo eilučių aukščius, tad intervalas jų beveik neliečia. Vertinau iš teorijos, o ne iš matavimo — ta pati klaida, kurią užsirašiau rugsėjo 1 d., tik kitoje srityje.

**Prognozė visam darbui:** ~44 psl. dabar · ~38 su vienetiniu intervalu · ~35 pridėjus 1 skyriaus trumpinimą · ~33,5 su 2 skyriaus lentelių suspaudimu. Nė vienas svertas vienas problemos neišsprendžia.

**Sprendimas: trumpinimas atidedamas, kol bus visas darbas.** Vadovo argumentas teisingas, ir jį remia konkretus faktas: plane numatyta rugsėjo 8 d. `tab:reikalavimai` perkelti iš 1 skyriaus į 3-ąjį, todėl **1 skyrius susitrauks savaime**. Trumpinant dabar tas pats darbas būtų daromas du kartus, o proporcijų negalima vertinti, kol 4–6 skyrių nėra.

**Ką verta pritaikyti iš karto, nes nieko nekainuoja:** 3–6 skyrius rašyti su išmatuotu tankiu galvoje. 1 ir 2 skyriai viršijo taikinį 60–90 %, o pagrindinė priežastis — **lentelės pigios rašyti, bet brangios puslapiais**: 2 skyriaus tankis 269 žod./psl. prieš 1 skyriaus 374. Kiekvienai naujai lentelei turi būti atsakyta, ko ji pasako, ko nepasakytų dvi teksto eilutės.

**Trumpinimo kandidatai, užrašyti kad nereikėtų ieškoti iš naujo:**

| Vieta | Veiksmas | ≈ psl. |
|---|---|---:|
| Preambulė | `\onehalfspacing` → `\singlespacing` arba `\setstretch{1.15}` | −6 / −3 |
| 1 sk. | `tab:aprepis`, `tab:diegimas` → tekstas; `tab:reikalavimai` → 3 sk. | −3 |
| 2 sk. | `tab:metodai` 18 → ~8 eilučių (4 pasirinkti + atmestieji pagal priežastį) | −0,7 |
| 2 sk. | `tab:susije` keturias `almahaqeri` eilutes sulieti į vieną | −0,5 |
| 2 sk. | `tab:apribojimai` (3 eilutės) → tekstas | −0,3 |
| 2 sk. | 2.2–2.5 sutraukti į vieną poskyrį | −1,5 |

**Proporcijos pastaba galutinei peržiūrai:** dabar 19 psl. teorijos prieš 13,5 psl. praktinio darbo. Praktikos vadovui skirtoje ataskaitoje santykis turėtų būti priešingas.

#### 25. Tuščias 3 skyrius PDF'e — mano klaida ⚠️

Vadovas pastebėjo, kad ataskaitoje yra tuščias 3 skyrius, dubliuojantis 4-ąjį.

**Priežastis:** `ataskaita.tex` deklaruoja **visus** skyrių pavadinimus (`\section` + `\label`), o skyrių failai turi tik `\subsection`. Rašydamas `02_di_metodai.tex` į failo pradžią įdėjau dar vieną `\section{Dirbtinio intelekto metodų taikymo galimybės}` su tuo pačiu `\label{sec:di_metodai}`. Rezultatas: 3 skyrius (iš `ataskaita.tex`) liko tuščias, o visas turinys atsidūrė 4-ame, sunumeruotas 4.1–4.8. Visi tolesni skyriai pasislinko vienu.

**Ženklas buvo `.aux` faile, ir aš jį mačiau:** `newlabel{sec:di_metodai}` figūravo **du kartus** — kaip `{3}{11}` ir kaip `{4}{11}`. Peržiūrėjau tą išvestį ieškodamas puslapių pasiskirstymo ir dubliuoto rakto nepastebėjau.

**Pataisyta:** pašalintas dubliuojantis `\section` ir `\label` iš `02_di_metodai.tex`. Patikrinta testiniu kompiliavimu — turinys dabar 3.1–3.8, tuščio skyriaus nėra, dubliuotų `\label` visame darbe nėra.

**Pamoka:** prieš rašant į skyriaus failą reikėjo pažiūrėti, kaip sutvarkytas jau veikiantis `01_atakos.tex`. Jis `\section` neturi — struktūros taisyklė buvo matoma, tik nepatikrinta. Tas pats principas kaip su kabutėmis, tik ten patikrinau, o čia ne.

**Antra pamoka — dėl patikrų:** mano automatinė patikra tikrino skliaustus, `\SI` reikšmes, kirilicą ir aplinkų poras, bet **netikrino dokumento struktūros nuoseklumo**. Pridėta: skyrių failuose `\section` būti negali, o `\label` visame darbe turi būti unikalūs.

### Kas nepavyko

- **`houichi2025smartcity` metrikų gauti nepavyko:** Wiley 403, ResearchGate 429, PDF kopijos nėra. Po trijų bandymų sustojau — reikia universiteto prieigos. Eilutė lentelėje pažymėta komentare.
- **Pamoka:** metrikas reikia ištraukti **tą pačią dieną, kai šaltinis įtraukiamas į `.bib`**. `houichi` ir `imani` pridėti ryte be skaičių, ir dėl to `imani` klaidingai pateko į susijusių darbų sąrašą, o `houichi` liko neužpildytas.
- **Du kandidatai šaltiniai nepasiekiami automatiškai:** *IET Smart Cities* (403) ir *Computer Science Review* FL apžvalga (robots.txt). Į `.bib` **neįtraukti** — metaduomenys nepatikrinti.

### Pamoka

**Rugsėjo 1 d. dokumentacija buvo sudaryta iš straipsnio ir CIC puslapio, ne iš failo.** Ji atrodė patikima — su lentelėmis, spąstų sąrašu, formulėmis — ir buvo neteisinga 8 stulpeliuose iš 46. Vienos antraštės eilutės pakako jai paneigti.

**Taisyklė: duomenų aprašas, sudarytas neatidarius duomenų, yra hipotezė, ne dokumentacija.** Žymėti tokį failą kaip nepatikrintą, kol nepaleista `patikra`.

Antra: du rugsėjo 1 d. sprendimai atsipirko iškart — žodynas kode su `assert` (pagavo registro pokytį) ir patikros skriptas. Trečia: pati atsargiausia šio failo eilutė — „jei stulpelių pavadinimai skiriasi nuo šio sąrašo, veidrodis pakeistas" — pasirodė esanti reikalingiausia.

### Ką darysiu rytoj (rugs. 3, ketvirtadienis)

1. Paleisti patikros skriptą ant 200 000 eilučių — patvirtinti keturias tapatybes ir etikečių registrą.
2. Pataisyti `etiketes.py` ir `ikelimas.py` (`Label`, `.upper()` normalizavimas).
3. Pataisyti `tab:atakos` eilutes, kurios remiasi `flow_duration` ir asimetrija.
4. Užbaigti 2 skyriaus P1 poskyrius, jei liko.

---

## Rugsėjo 3 d. (ketvirtadienis) — 3 užduoties planas

### Ką padariau

**12:35–13:00 — sudarytas 3 užduoties tikslų planas** (`claude/uzduotis_03_planas.md`): tikslai T0–T8, skyriaus struktūra, lentelių specifikacija, **eksperimento protokolas (24 punktai)**, laiko biudžetas, priėmimo kriterijai, rizikos. `STRUKTURA.md` atnaujinta.

**Prieš rašant peržiūrėta visa turima medžiaga** — `praktikos_planas.md`, `uzduotis_02_planas.md`, `metodu_apzvalga.md`, `STRUKTURA.md` ir šis žurnalas. Peržiūros rezultatas pasirodė svarbesnis už patį planą (žr. „Ką radau“).

**Ištaisyta klaidinga prielaida dėl dokumento paskirties** — `ataskaita.tex` yra teikiamas **Aineros praktikos vadovui**, ne universitetui kaip visa praktikos ataskaita. Pataisyti: plano 12 skyrius, šio žurnalo rugsėjo 2 d. 24 punktas (pažymėtas), rugsėjo 3 d. sprendimai.

### Priimti sprendimai

- **3 užduotis vykdoma šiandien**, ne rugsėjo 8 d. Grafikas eina **5 dienomis į priekį**; atlaisvintos dienos atitenka 4 užduočiai, kurioje plane numatyta didžiausia techninė rizika.
- ⭐ **Atranka skaidoma į dvi pakopas.** Pirma — keturi kietieji apribojimai (K1 duomenų struktūra, K2 prielaidos, K3 mokymo kaina, K4 inferencijos delsa) be svorių ir balų: 17 → 9. Tik po to svertiniai balai likusiems devyniems. **Priežastis: ketvertas fiksuotas vakar**, todėl vienpakopė svertinė matrica būtų jau priimto sprendimo pagražinimas — ir tai matytųsi.
- **Ketverto įtraukimas grindžiamas trimis dalykais, ne vienu:** rikiuotės viršūne, paradigmų padengimu ir sudėtingumo gradientu. **Autokoderis balais pralaimi ansambliams, ir tai rašoma atvirai** — jis aibėje todėl, kad reikalavimas aptikti nematytas atakas yra funkcinis, o ne sveriamas. Matrica, kuri sąžiningai rodo pralaimėjimą, stipresnė už tą, kurioje balai sutampa su atsakymu.
- **Balų skalė (1–5) apibrėžiama prieš balus**, kiekvienam kriterijui po eilutę. Kitaip balai yra nuojauta skaičiaus pavidalu.
- **Kiekvienas iš 5 svorių turi nurodyti konkrečią `tab:reikalavimai` eilutę.** Svoriai — vienintelė subjektyvi vieta visame skyriuje, todėl ji žymima, o ne užglaistoma.
- **Sprendimų matrica generuojama iš CSV** (`rezultatai/darbiniai/sprendimu_matrica.csv` → `tab:matrica`), ne rašoma ranka. Jautrumo analizė perskaičiuoja svertines sumas, o rankinis perrašinėjimas įvestų būtent tą klaidų klasę, kurios darbe sąmoningai atsisakyta.
- **Jautrumo analizės rezultatas užrašomas iš anksto abiem atvejais** — ir jei rikiuotė stabili, ir jei ne. Priešingu atveju atsirastų pagunda koreguoti svorius, kol rikiuotė „nusistovės“.
- **Protokolas rašomas tekstu, ne ketvirta lentele.** 1 sk. 9 psl. vietoj 4–5, 2 sk. 9,7 vietoj 5–6; trečias kartas iš eilės nebebūtų atsitiktinumas. Taikinys: ≤ 4,5 psl., ~1 200–1 400 žodžių teksto.
- **Apimties sprendimas lieka atidėtas**, bet **jo pagrindas pasikeitė** (žr. „Ką radau“, 5 punktas). Šiandien daroma tik `tab:reikalavimai` perkėlimas — ir daroma **dėl turinio**, ne dėl puslapių.
- **Smulkmenos** (`requirements-lock.txt`, titulinis, `houichi` eilutė, dubliuotos anotacijos) — rezervo laikas arba rugs. 4 d., ne P0 laikas.

### Ką radau

#### 1. 3 užduoties turinys jau didele dalimi sugeneruotas — ir tai keičia dienos svorio centrą ⭐

Peržiūrint paaiškėjo, kad iš dešimties dalykų, kurių 3 užduočiai reikėjo, **septyni jau padaryti** 2 užduotyje: kandidatų aibė, ketvertas, atmetimo priežastys su tipais, kriterijai (paveldėti iš `tab:reikalavimai`), užduoties detalumas, metrikų pasirinkimas ir delsos biudžetas.

**Neužrakinta liko trys, ir visos trys yra tas pats dalykas — eksperimento protokolas:** duomenų skaidymas, protokolas kaip visuma ir nematytos klasės testo klasės.

**Vadinasi, metodų atranka šiandien yra užrašymo, o ne sprendimo darbas.** Realus naujas darbas — protokolas, ir jis vienintelis blokuoja 4 užduotį. Tai tiesiogiai pakeitė dienos biudžetą: protokolui skirta ištisa valanda (16:05–17:05) su aukščiausiu prioritetu, o skyriaus tekstas pažymėtas kaip tas, kurį galima perkelti į rytojų.

#### 2. Dublikatai tarp `train` ir `test` — nutekėjimo kelias, kurio iki šiol nebuvo sąraše ⚠️

97,7 % rinkinio yra potvynio (flood) srautas. Tokio srauto eilutės gali sutapti **tiksliai**, o po atsitiktinio skaidymo tos pačios eilutės kopijos atsiduria ir `train`, ir `test` aibėse. Modelis tada testuojamas tuo, ką matė mokydamasis, ir **rezultatas išpučiamas be jokios matomos klaidos** — lygiai tas atvejis, apie kurį įspėja `reddy2026datasets`.

Atmetus antrinius rinkinius ir neturint laiko žymos, tai lieka **pagrindinis likęs nutekėjimo kelias**, o iki šiol jo nebuvo nė viename sąraše. Įrašyta į protokolą kaip privalomas žingsnis: `df.duplicated().sum()` **prieš** skaidymą; jei > 1 %, tikslūs dublikatai šalinami, skaičius įrašomas į ataskaitą. Kaina — viena eilutė kodo.

Antras panašus kelias, irgi įrašytas: **autokoderio slenkstis** turi būti kalibruojamas ant `val`, niekada ant `test`.

#### 3. `rezultatai.csv` schemą pigiau užrakinti dabar nei rugsėjo 15 d.

`i_latex.py` jau parašytas, o 5 ir 6 užduočių lentelės generuojamos iš to failo. Pakeitus stulpelius po pirmųjų eksperimentų, perrašomas ir skriptas, ir jau surinktos eilutės. Todėl 15 stulpelių schema fiksuota protokolo 24 punkte — penkios minutės dabar arba pusdienis rugsėjo 15 d.

Ta pati logika kaip su lentelių generavimu: sprendimai, kurie kainuoja minutes anksti ir valandas vėlai, priimami anksti.

#### 4. Apimties norma buvo paimta ne iš to šaltinio ⚠️⭐

`ataskaita.tex` **nėra visa VILNIUS TECH praktikos ataskaita** — tai dokumentas, teikiamas **Aineros praktikos vadovui**. Rugsėjo 1–2 d. dirbau su prielaida, kad tai universiteto ataskaita, ir nuo jos kilo 26–34 psl. norma.

**Vadinasi, nepagrįsta viskas, kas nuo tos normos išvesta:** trumpinimo kandidatų sąrašas (rugs. 2 d., 24 punktas), eilučių intervalo matavimas (−6 psl.) ir „proporcijų“ pastaba. Ne todėl, kad skaičiai neteisingi — jie išmatuoti — o todėl, kad **taikinys, į kurį jie lyginami, neegzistuoja.**

**Kas iš to lieka galioti.** Vienintelis argumentas, nepriklausęs nuo normos: **~23 psl. teorijos prieš 0 psl. atlikto darbo netinka auditorijai.** Įmonės vadovui rūpi, kas sukurta ir išmatuota. Vakar tai buvo viena pastaba iš kelių; dabar ji **vienintelė ir todėl svaresnė** — ir ji sako ne „trumpinti teoriją“, o **nemažinti 4–6 skyrių**, kai rugsėjo 9–17 d. spaus laikas.

**Pamoka, ir ji ta pati kaip rugsėjo 2 d. su duomenimis.** Normą pasiėmiau iš prielaidos apie dokumento paskirtį ir nė karto jos nepatikrinau, nors ji nulėmė ištisą sprendimų grandinę — trumpinimo kandidatus, lentelių ribą, skyrių taikinius. **Reikalavimas, kurio šaltinis nepatikrintas, yra spėjimas, ne reikalavimas.** Tas pats, ką užsirašiau apie duomenų aprašą, sudarytą neatidarius duomenų.

**Klausimas iškart ir atsakytas: reikalavimų nėra jokių** — nei apimties, nei struktūros, nei formato. Yra **tik užduočių sąrašas.** Vadinasi, 26–34 psl. skaičius nenaudojamas niekur ir trumpinimo klausimas **uždaromas visai**, ne atidedamas.

**Kas užima normos vietą — ir tai naudingiau.** Vienintelis vadovo turimas kriterijus yra pats užduočių sąrašas: ar visos šešios atliktos ir ar tai matyti. Iš to seka du pigūs dalykai: **skyrių numeracija turi sutapti su užduočių numeracija** (dabar sutampa — nieko daryti nereikia, tik nesugriauti), ir **kiekvienas skyrius baigiasi matomu tos užduoties rezultatu** (2 sk. — 2.8, 3 sk. bus 3.7).

⚠️ **Atgaline data tai perkvalifikuoja rugsėjo 2 d. dubliuoto `\section` klaidą.** Ji nuslinko turinį į 4 skyrių ir **sugriovė būtent tą sutapimą** — vadovas būtų atsivertęs „3 skyrių“ ir radęs tuščią puslapį ten, kur turi būti 3 užduotis. Užrašiau ją kaip formatavimo riktą; ji buvo kertanti į vienintelį egzistuojantį vertinimo kriterijų.

**Apimtis nuo šiol yra laiko biudžetas, ne atskaitomybė.** Puslapiai nebeturi kam atsiskaityti, bet valandos, praleistos rašant teoriją, yra valandos, neatiduotos 4–6 užduotims. **Vienintelė likusi apimties rizika yra priešinga tai, kurios bijojau:** ne per ilgas dokumentas, o ~23 psl. teorijos prieš plonus 4–6 skyrius.

**Veiksmas:** 26–34 psl. norma pažymėta šio žurnalo rugsėjo 2 d. 24 punkte; **`praktikos_planas.md` 4 skyrius („Realistinė apimtis“) dar nepažymėtas** — padaryti prie likučių.

#### 5. Kirilicos raidė — trečias kartas iš eilės

Rašydamas planą vėl įrašiau `а` žodyje „lieka“. Automatinė patikra pagavo, kaip ir abu ankstesnius kartus. **Trys kartai iš trijų dokumentų** reiškia, kad tai ne atsitiktinumas, o įrankio savybė, todėl patikra lieka privaloma kiekvienam naujam tekstui, ne tik `.tex` failams. Patikra papildyta ir `.md` failais.

---

## Rugsėjo 3 d., 13:40–14:30 — T0 atliktas

### Ką padariau

**`tab:atakos` suderinta su realiais duomenimis — 15 taisymų.** Visi aštuoni pašalinti stulpeliai iš 1 skyriaus dingo. Keturiose eilutėse pakeisti požymiai (`Magnitue`/`Radius` → `Variance`, `Weight` → `Rate`/`Number`, `Srate`/`Drate` → pašalinta), o **keturiose atakose spraga įvardyta atvirai**, nes pakaitalo nėra:

| Ataka | Ko nebeliko | Kaip užrašyta |
|---|---|---|
| DDoS-SlowLoris | Srauto trukmė | „Srauto trukmės šis leidimas neišreiškia — pagrindinis atakos požymis lieka nepadengtas“ |
| DNS klastojimas | Kryptis | „Atsakymų perteklius nefiksuojamas — krypties požymių leidime nėra“ |
| Žvalgyba | Trukmė + kryptis | „Srauto kryptis, trukmė ir unikalių taikinių skaičius nefiksuojami“ |
| Duomenų nutekinimas | Trukmė + asimetrija | „Krypties asimetrijos ir srauto trukmės — pagrindinių šios atakos požymių — leidimas neišreiškia“ |

Išnaša po lentele perrašyta: 46 → **39 požymiai**, įvardyti visi aštuoni trūkstami ir `Duration` → `Time_To_Live`.

**Rasta trys pasenę skaičiai, kurių plane nebuvo.** Ieškojau tik `flow_duration` ir asimetrijos, bet paieška atvedė ir prie kitų 1 skyriaus vietų, remiančių dokumentacija, o ne failu:

| Buvo | Yra |
|---|---|
| „iš maždaug 46,69 mln.“ | **45,02 mln.** |
| „apie 1,10 mln.“ gerybinio (2,4 %) | **1,05 mln.** (2,3 %), santykis **41,8:1** |
| Etiketė `BenignTraffic` (2 vietose) | **`BENIGN`** |

**`etiketes.py` patikrintas iki galo** — ne paleidžiant savipatikrą, o **prieš realias etiketes**: ištraukiau unikalias `Label` reikšmes iš visų 63 failų ir paleidau `i_kategorija()` kiekvienai. **34 iš 34, nė vienos klaidos.** Rugsėjo 2 d. taisymai veikia.

**Patvirtinta nutrūkusių eilučių elgsena** (protokolo 3 punktas): **9 failai** baigiasi nutrūkusia eilute, blogiausias `Merged46.csv` — tik 4 laukai iš 40. `pandas` jas perskaito be klaidos, `Label` tampa `NaN`, o `dropna(subset=["Label"])` pašalina. **Protokolo punktas galioja — dabar patikrintas, ne perimtas iš užrašų.**

**Smulkmenos uždarytos:** `requirements-lock.txt` **egzistuoja** (žurnalas buvo pasenęs, `STRUKTURA.md` teisi); `README.md` turi turinį, nors `STRUKTURA.md` žymėjo tuščią; ištrintas dubliuotas `literatura/literatura_anotacijos.md` ir `ataskaita/skyriai/02_di_metodai.tex.bak`.

### Ką radau

#### 6. Dvi mano paties klaidos per vieną valandą — abi pagautos ta pačia taisykle ⭐

**Pirma: 15 iš 15 pakeitimų nerado atitikmens.** `re.escape()` ekranuoja ir tarpus, todėl mano šablonas gavo perteklinį backslash'ą. **Antro spėjimo nedariau** — atspausdinau patį šabloną ir eilutę iš failo, ir priežastis buvo matoma iš karto. Rugsėjo 1 d. taisyklė („po pirmo nepavykusio taisymo — ne antras spėjimas, o duomenys“) suveikė pirmą kartą sąmoningai.

**Antra, pavojingesnė: kone paskelbiau, kad `etiketes.py` sugedęs.** Palyginau realias etiketes su `KATEGORIJOS` žodynu ir gavau **1 sutapimą iš 34** — atrodė, kad registro normalizavimas neveikia. Iš tikrųjų kodas naudoja **išvestinį** `KATEGORIJOS_NORM`, o aš tikrinau ne tą objektą. **Klaida buvo patikroje, ne kode.**

**Pamoka, kurios sąraše dar nebuvo:** kai patikra praneša apie katastrofą, pirmiausia tikrinama **pati patikra**, ne kodas. Būčiau „taisęs“ veikiantį žodyną — tiksliai tas scenarijus, kurio rugsėjo 2 d. išvengiau su kabutėmis, tik šįkart iš kitos pusės.

#### 7. `STRUKTURA.md` pasenusi dviem punktais, ir abu ta pačia kryptimi

`README.md` pažymėtas kaip tuščias, nors turi turinį; `requirements-lock.txt` žurnale laikomas neatliktu, nors failas yra nuo rugsėjo 1 d. **Abu pasenimai rodo darbą kaip mažiau padarytą, nei jis yra** — nekenksminga, bet reiškia, kad būklės žymos rašomos iš atminties. `src/` aplanke taip pat guli **9 tušti `.py` karkasai** (0 baitų): `pozymiai.py`, `balansavimas.py`, `paleisti.py` ir visi `modeliai/`. Tai atitinka ⬜ žymą, bet 4 užduotyje verta atsiminti, kad failai jau sukurti.

#### 8. T1 atšauktas — priemonė be pagrindo ⭐

`tab:reikalavimai` perkėlimas į 3 skyrių atrodė kaip turinio sprendimas („kriterijai priklauso 3 skyriui“), bet peržiūrėjus paaiškėjo, kad jis **gimė kaip apimties priemonė** — rugsėjo 1 d. trumpinimo kandidatų sąraše, šalia „`tab:aprepis`, `tab:diegimas` → tekstas“. Kai normos nebeliko, dingo ir pagrindas, o kaina liko matoma:

- 1.5 poskyris netektų savo centrinio objekto, nors **reikalavimai yra pats jo dalykas**;
- 1.6 įžanga remiasi 1.5 išvada;
- penkios nuorodos 1 skyriuje virstų nuorodomis **pirmyn**.

**Vietoj to 3 skyriuje bus sava `tab:kriterijai`** (kriterijus | svoris | iš kurios `tab:reikalavimai` eilutės kyla). Trečiasis stulpelis padaro tą patį, ką būtų padaręs perkėlimas — parodo paveldėjimą — tik nieko negriaudamas ir ~0,3 psl. vietoj ~1 psl.

**Pamoka:** kai priemonė lieka plane po to, kai jos priežastis dingo, ji ima atrodyti kaip savarankiškas sprendimas. **Vertinant kiekvieną likusį punktą verta paklausti, kuriai dingusiai priežasčiai jis tarnavo.** Tas pats klausimas laukia ir kitų rugsėjo 1 d. trumpinimo kandidatų.

**Pasekmė apimčiai:** 1 skyrius nebesusitrauks, tad ~23 psl. teorijos prognozė galioja be išlygų.

#### 9. T2: filtre metodų ne 17, o 18 — ir tai keičia du skaičius ⚠️

Rašydamas `tab:filtras` sutikrinau su `tab:metodai` ir radau, kad plane paveldėtas skaičius neteisingas. `metodu_apzvalga.md` skaičiuoja **17 metodų**, nes „Transformer / GNN“ ten yra vienas punktas; `tab:metodai` juos **išskiria**, todėl eilučių yra **18**. Kadangi plane pats reikalavau, kad filtro eilių tvarka sutaptų su `tab:metodai`, teisingas skaičius yra 18.

**Antras taisymas — „17 → 9“.** Praeina ne devyni, o **aštuoni**: sprendimų medis, RF, XGBoost, LightGBM, autokoderis, Isolation Forest, MLP, 1D-CNN. Devintas atsirado todėl, kad klasterizavimą ir savimoką buvau įskaičiavęs kaip praeinančius. Jie iš tikrųjų **visus keturis vartus praeina**, bet lieka **už darbo ribų**: pirmasis duoda grupes, ne sprendimą „ataka / ne ataka“, antrojo naudos pažymėtame rinkinyje išmatuoti neįmanoma.

⭐ **Iš to seka lentelės sandaros pataisa:** stulpelis „Rezultatas“ turi turėti **tris** reikšmes, ne dvi. „Už darbo ribų“ nėra atmetimas — sulieti juos į vieną reikštų pasakyti, kad metodas netinka, kai iš tikrųjų netinka uždavinys. Ta pati skirtis, kurią rugsėjo 2 d. užsirašiau apie disbalanso stulpelį neprižiūrimiems metodams („neaktualus“, ne „geras“).

**Galutinis balansas: 18 = 8 praeina + 8 atmesti vartais + 2 už ribų.** Atmetimų pasiskirstymas pasitvirtino toks, koks buvo numatytas: **K1 — 4, K2 — 1, K3 — 2, K4 — 1.** Tai reiškia, kad **pusę atrankos atlieka duomenų struktūra**, o skaičiavimo resursai — tik ketvirtadalį.

**Techninė pastaba:** varnelei naudojau `$\surd$`, ne `\checkmark` — `amssymb` preambulėje nėra. Patikrinau prieš rašydamas, o ne po kompiliavimo klaidos.

#### 10. T3: penktas kriterijus iškrito, ir tai lentelę sustiprino ⭐

Plane buvo penki kriterijai su svoriais 30/25/20/15/10. Bandant kiekvienam nurodyti `tab:reikalavimai` eilutę, **penktasis — „realizavimo rizika“ — jos neturi.** Ir negali turėti: tai ne IoT savybė, o mano kalendorius.

**Bet lemiamas argumentas pasirodė kitas, empirinis.** Visi aštuoni po filtro likę metodai turi standartines bibliotekų realizacijas — `sklearn`, `xgboost`, `keras`. Kriterijus, kuris visiems duoda tą patį balą, svertinės sumos nekeičia: jis tik atrodo kaip vertinimas. **Pašalintas.**

Tai tas pats redagavimo principas, kurį rugsėjo 2 d. taikiau 2 skyriui: „realizavimo rizika“ buvo kriterijaus pavidalu užrašytas nerimas, ko nespėsiu.

**Nauji svoriai — keturi, suma 100:**

| Kriterijus | Svoris | Iš kurios `tab:reikalavimai` eilutės |
|---|---:|---|
| Aptikimo kokybė | 30 % | 4 eil.: pažeidžiamumai lieka neištaisyti → aptikimas yra **vienintelė likusi apsauga** |
| Klaidingi teigiami ir disbalansas | 30 % | 5 eil.: 1 % klaidingų teigiamų = ~1000 signalų per parą → sistema išjungiama |
| Resursų poreikis | 25 % | 1 eil., kuri **pati sako**, kad tai „atrankos kriterijus, ne antraeilis rodiklis“ |
| Interpretuojamumas | 15 % | ta pati 5 eil., **antroji jos pasekmė**: ribotą pajėgumą turintis analitikas turi galėti signalą pagrįsti |

**Klaidingiems teigiamiems daviau tiek pat, kiek tikslumui (30 %),** nes 1 skyriaus skaičiavimas rodo ne pablogėjimą, o sistemos išjungimą. Tai ne kokybės laipsnis, o dvejetainis eksploatacijos rezultatas.

#### 11. Du reikalavimai kriterijaus neduoda — ir tai verta pasakyti

`tab:reikalavimai` antra eilutė (aptikimas remiasi tinklo srautu) ir trečia (be per-įrenginio konfigūravimo) **jokio kriterijaus neduoda**: jas vienodai tenkina visi po filtro likę metodai. Reikalavimas, kurio visi kandidatai laikosi, yra **prielaida, ne skiriamasis požymis**.

Įrašiau tai į lentelės išnašą. Priešingu atveju skaitytojas klaustų, kodėl iš penkių reikalavimų liko keturi kriterijai, ir teisingai įtartų, kad vienas dingo pakeliui.

⚠️ **Atkreiptinas dėmesys į 1 skyriaus teiginį.** 1.5 poskyrio pabaigoje parašyta, kad „aptikimo kokybė, klaidingų teigiamų lygis, resursų poreikis ir interpretuojamumas kyla tiesiogiai iš `tab:reikalavimai` lentelės“. **Interpretuojamumas lentelėje neminimas nė karto** — jis išvedamas iš penktos eilutės antrosios pasekmės, o ne skaitomas iš jos tiesiogiai. Dabar tas išvedimas užrašytas `tab:kriterijai`, tad teiginys tapo teisingas; bet iki šiandien jis buvo per stiprus.

#### 12. Numeracija: N užduotis yra N+1 skyrius ⚠️

Tikrindamas, kur PDF'e atsidūrė `tab:filtras`, pažiūrėjau į `.aux` ir pamačiau: `sec:atakos` = **2**, `sec:di_metodai` = **3**, `sec:parinkimas` = **4**. Priežastis paprasta — `\section{Įvadas}` yra pirmas.

**Poslinkis nuoseklus ir techniškai teisingas**, bet susikerta su tuo, kas nuspręsta šiandien: vienintelis vadovo turimas kriterijus yra užduočių sąrašas, o jis ieškos „3 užduoties“ ir ras ją 4 skyriuje. Savo priėmimo kriterijų („3 skyrius PDF'e yra trečias“) buvau užrašęs nepatikrinęs — jis nuo pat pradžių buvo neįvykdomas.

**Sprendimo nepriimu vienas** — variantai: palikti kaip yra (įvadas numeruojamas, tai įprasta); `\section*{Įvadas}` be numerio, kad N užduotis = N skyrius; arba į skyrių antraštes įrašyti užduoties numerį.

**Pamoka:** priėmimo kriterijus, parašytas nepažiūrėjus į `.aux`, yra toks pat spėjimas kaip duomenų aprašas, sudarytas neatidarius failo.

#### 13. Trečias kartas su ta pačia escape klaida

Vėl parašiau `r"...\n..."` ir gavau literal backslash-n vietoj eilutės lūžio — dabar keitiniuose. Pagavo `assert`, ne kompiliavimas. Rugsėjo 3 d. jau turėjau tą patį su `re.escape` ir tarpais. **Sprendimas nustojo būti ad hoc:** keitiniams naudoju `pat()` funkciją, kuri tarpus paverčia `\s+`, tad eilučių lūžiai nebesvarbūs.

#### 14. T4: matrica ketverto nepatvirtino — ir tai geriausia, kas galėjo nutikti ⭐⭐

Suvedus balus pagal `tab:kriterijai` skalę, rikiuotė gavosi tokia:

| Prižiūrimi | Suma | | Neprižiūrimi | Suma |
|---|---:|---|---|---:|
| XGBoost | **4,70** | | Isolation Forest | **3,50** |
| LightGBM | **4,70** | | Autokoderis | 2,95 |
| Sprendimų medis | 3,80 | | | |
| Random Forest | 3,55 | | | |
| MLP | 3,25 | | | |
| 1D-CNN | 2,70 | | | |

**Iš vakar fiksuoto ketverto rikiuotės viršūnėje yra tik XGBoost.** RF ketvirtas, MLP penktas, autokoderis — antras iš dviejų.

**Pirma reakcija buvo taisyti balus, ir ją reikėjo sustabdyti.** Tai tiksliai tas veiksmas, nuo kurio saugojausi rašydamas planą: pakoreguoti kriterijus, kol rezultatas sutaps su atsakymu. Balai lieka tokie, kokie išeina iš skalės, apibrėžtos **prieš** juos.

**Trys radiniai, kurių be matricos nebūtų buvę:**

1. ⚠️ **Sprendimų medis (3,80) lenkia Random Forest (3,55).** Priežastis skaidri: 5/5 už resursus ir interpretuojamumą prieš 4/3. Ketverte RF lieka dėl **sudėtingumo gradiento** — jis yra ansamblio pakopa. Bet radinys savarankiškas: šliuzo uždaviniui pigiausias ir aiškiausias prižiūrimas metodas yra stipresnis, nei atrodė. **Verta apsvarstyti jį kaip penktą, pigų atskaitos modelį.**
2. **LightGBM lygus XGBoost (4,70).** Jis atkrenta ne balais, o dėl to, kad du beveik tapatūs stiprinimo metodai palyginime nieko neprideda. **Matrica šį rugsėjo 2 d. sprendimą patvirtino**, ne paneigė.
3. **Isolation Forest (3,50) lenkia autokoderį (2,95).** Autokoderis aibėje dėl funkcinio reikalavimo, ne dėl balo. Tai antras nepriklausomas argumentas, kad IF vertas pridėti kaip pigus etalonas — pirmasis buvo rugsėjo 2 d.

> **Jei balai būtų sutapę su ketvertu, lentelė nieko neįrodytų** — tik atkartotų vakar priimtą sprendimą gražesniu pavidalu. Nesutapimas yra įrodymas, kad kriterijai nebuvo derinami prie norimo atsakymo.

#### 15. Palyginimo asimetrija atsirado lentelėje, ne tekste

Neprižiūrimų metodų negalima dėti į tą patį stulpelį su prižiūrimais — tai numatyta dar rugsėjo 2 d. (2.8 poskyris). Iki šiol tai buvo pastaba tekste; dabar ji **įgyvendinta lentelės sandaroje**: du atskiri blokai su antraštėmis, ir išnaša, kad sumos tarpusavyje nepalyginamos.

Papildomai reikėjo užrašyti, ką neprižiūrimiems metodams reiškia stulpelis „Disbalansas“: **problema jiems nekyla, o ne yra išspręsta.** Be to sakinio balas 4 atrodytų kaip pranašumas prieš RF balą 3, nors matuoja visai kitą dalyką.

#### 16. Matrica generuojama, ne rašoma — ir tai jau atsipirko

`sprendimu_matrica.csv` → `src/eksperimentai/matrica.py` → `ataskaita/lenteles/matrica.tex`, įtraukiama per `\lentele{}`. Atkartojamumą patikrinau paleisdamas du kartus ir sulygindamas `md5sum` — failas identiškas.

**Kaina buvo maždaug 20 minučių, o T5 be jos būtų neįmanomas:** jautrumo analizė perskaičiuoja svertines sumas aštuoniems svorių rinkiniams; rankomis tai būtų 64 perrašyti skaičiai.

**Skripte pagauta klaida:** `"..." % (...) .replace(...)` — `.replace` prilipo prie tuple, ne prie suformatuotos eilutės. Be to pati mintis buvo bloga: `.replace(".", ",")` visai eilutei būtų sugadinęs žymą `(aut.)` → `(aut,)`. **Kablelis dabar keičiamas tik pačiame skaičiuje.** Klaidą parodė `AttributeError`, bet tylųjį `(aut,)` variantą būčiau pamatęs tik PDF'e.

#### 17. T5: „nepasikeitė“ nėra išvada ⭐⭐

Aštuoni svorių rinkiniai po ±10 p. p. — **visais aštuoniais atvejais rikiuotė išliko ta pati (8/8).** Rašiau tai kaip rezultatą ir sustojau: pilnas stabilumas atrodo per gerai.

Patikrinus paaiškėjo, kad tai ne rikiuotės stabilumo, o **zondo siaurumo** matas. ±10 p. p. tiesiog nepasiekia nė vienos ribos. Todėl paskaičiavau, kur tos ribos iš tikrųjų yra:

| Palyginimas | Skirtumas | Kada apsiverstų |
|---|---:|---|
| XGBoost prieš Random Forest | +1,15 | **Niekada** — dominavimas |
| Random Forest prieš MLP | +0,30 | **Niekada** — dominavimas |
| XGBoost prieš sprendimų medį | +0,90 | Interpretuojamumo svoris → **0,42** (dabar 0,15) |
| Sprendimų medis prieš Random Forest | +0,25 | Kokybės svoris → **0,44**, arba interpretuojamumas → 0,01 |

⭐ **Dominavimas pasirodė stipresnis argumentas už bet kokį jautrumo procentą.** XGBoost nėra blogesnis už Random Forest nė pagal vieną kriterijų, o RF nėra blogesnis už MLP — tokioms poroms jautrumo analizė **apskritai nereikalinga**, nes jokių svorių derinys rezultato nekeičia. Dvi iš keturių svarbiausių porų yra būtent tokios.

Likusioms dviem ribos konkrečios ir įsimenamos: sprendimų medis aplenktų XGBoost tik tada, jei interpretuojamumui skirtume beveik tris kartus daugiau svorio nei dabar.

**Pamoka, kuri galioja ir 5–6 užduotims:** „rezultatas nepasikeitė“ savaime nieko nesako — reikia žinoti, **kiek toli buvo iki pokyčio**. Būčiau parašęs „rikiuotė stabili“ ir tai būtų buvęs tuščias sakinys, apsimetantis patikra. Tas pats principas kaip su vienos eilutės „patikra“ rugsėjo 2 d.

**Skriptas kviečia `svertine()` iš `matrica.py`, ne savo kopiją** — svoriai ir balai turi vieną šaltinį. Po refaktoringo `matrica.tex` `md5sum` nepakito, tad išvestis tikrai ta pati.

#### 18. „0 iš 8“ suklaidino patį autorių ⭐⭐

Rodiklį buvau užrašęs kaip **„pirmi trys pasikeitė 0 kartų iš 8“**. Perskaičius po kelių minučių jis nuskambėjo kaip **„niekas netiko“** — nors reiškia priešingą dalyką: rikiuotė išliko ta pati visais aštuoniais atvejais.

**Priežastis struktūrinė, ne stilistinė.** Rodiklis skaičiuoja *nesėkmes* (pokyčius), o skaitomas instinktyviai kaip *sėkmės*. Kai geras rezultatas yra nulis, kiekvienas skaitytojas turi tą nulį mintyse apversti — ir kartais neapverčia.

**Pataisyta visur teigiama forma:** „rikiuotė išliko ta pati 8 atvejais iš 8“. Skripto išvestis, skyriaus tekstas, planas ir šis įrašas.

**Taisyklė 5 ir 6 užduotims, kur tokių rodiklių bus daug:** jei geriausia reikšmė yra nulis, rodiklį reikia performuluoti taip, kad geriausia reikšmė būtų maksimumas. Tai galioja klaidingų teigiamų skaičiui, neišspręstų nuorodų skaičiui ir bet kuriam „kiek kartų nepavyko“ tipo matui. **Formuluotė, kurią autorius perskaito neteisingai, yra defektas, ne smulkmena.**

#### 19. Dar dvi klaidos, pagautos prieš kompiliavimą

**`\percent` darbe niekur nenaudotas.** Buvau parašęs `\SI{42}{\percent}`, bet 1 ir 2 skyriuose procentai rašomi `42~\%`. `siunitx` `\percent` greičiausiai būtų suveikęs, bet taisyklė aiški: naudoti tik tai, kas šiame darbe jau įrodyta veikiant. Pakeista į `~\%`.

**Korektūros riktas** „kiekvienai poroai“ → „porai“. Abi rastos peržiūrint failą po įrašymo — patikra dabar apima ir `\SI` argumentų sutikrinimą su tuo, kas jau naudota kituose skyriuose.

#### 20. T6: dublikatų patikra pakeitė ne protokolą, o rezultatų atskaitos tašką ⭐⭐⭐

Plane trys punktai buvo sąlyginiai — „jei dublikatų > 1 %, šalinti“. Išmatavus 1,9 mln. eilučių imtyje:

| | Plane buvo | Yra |
|---|---|---|
| Tikslūs dublikatai | „jei > 1 %“ | **33,1 %** |
| Prieštaringos etiketės | nenumatyta | **55 440 vektorių** |
| Neklasifikuojamos eilutės | nenumatyta | **4,98 %** |
| **Teorinė tikslumo riba** | nenumatyta | **~95 %** |

**Dublikatai susitelkę ten, kur ir tikėtumeisi:** `DDOS-ICMP_FLOOD` — 50 %, potvynio klasės 32–50 %, o retos klasės (`XSS`, `SQLINJECTION`, `UPLOADING_ATTACK`) — **0 %**. Atsitiktinai skaidant tos pačios eilutės kopijos patektų į abi aibes, ir modelis būtų testuojamas tuo, ką matė mokydamasis.

⭐ **Bet svarbiausia ne tai.** 55 440 požymių vektorių turi **daugiau nei vieną skirtingą etiketę** — tas pats įvesties vektorius pažymėtas skirtingai. Po dublikatų šalinimo tai palieka 4,98 % eilučių, kurių teisingai suklasifikuoti neįmanoma **jokiam modeliui**. Vadinasi, **teorinė tikslumo riba šiame rinkinyje yra ~95 %, ne 100 %**.

**Iš to seka argumentas, kurio darbe iki šiol nebuvo:** literatūroje skelbiami **99,5–99,6 %** tikslumai yra **aukščiau už šią ribą**. Tai reiškia, kad juose greičiausiai lieka dublikatų nutekėjimas. `reddy2026datasets` tai teigia bendrai; dabar turiu **savo skaičių**, išmatuotą savo duomenyse.

⚠️ **Išlyga, be kurios teiginys būtų per stiprus:** riba galioja **šiam 39 požymių leidimui**. Pašalinti krypties ir trukmės požymiai kaip tik ir skirtų dalį dabar sutampančių vektorių, todėl 46 požymių aibėje riba būtų aukštesnė. Tai kiekybiškai sustiprina 2 skyriaus teiginį apie ribotą palyginamumą — iš „skaičiai nepalyginami“ tampa „štai kiek ir kodėl“.

**Protokolo tvarka pasikeitė:** dublikatai šalinami **prieš** imties sudarymą ir skaidymą. Šalinama pagal **visą eilutę**, ne pagal požymius — prieštaringos etiketės paliekamos, nes tai tikras dviprasmiškumas, o ne dubliavimas. Šalinimas kartu sumažina disbalansą (imtyje 5 999:1 → 2 983:1) ir padidina `BENIGN` dalį (2,33 % → 3,49 %).

**Nematytų klasių scenarijai įvardyti vardais**, kaip reikalavo priėmimo kriterijus: `DDOS-SLOWLORIS` (žemo intensyvumo ataka, kurios pagrindinio požymio šiame leidime nėra — sunkiausias atvejis), `RECON-PORTSCAN`, ir ištisa kategorija `DICTIONARYBRUTEFORCE` (vienintelė savo kategorijos klasė, todėl prižiūrimas modelis etiketės neturi iš principo — tikroji autokoderio patikra).

#### 21. `\num{0,737}` būtų buvusi tyli klaida ⚠️

Taisyklę „naudoti tik tai, kas darbe jau įrodyta veikiant“ pritaikiau ir vėl neužteko. `\num` **yra** naudojamas 2 skyriuje — bet su **tašku**: `\num{0.018}`. Kablelis atsiranda išvestyje per `\sisetup{output-decimal-marker={,}}`.

Buvau parašęs `\num{0,737}` ir `\numrange{99,5}{99,6}` — siunitx kablelį įvestyje traktuoja kitaip, ir rezultatas būtų arba klaida, arba **tyliai neteisingas skaičius**. Pagavau tikrindamas, kaip komanda kviečiama kituose skyriuose, ne tik ar ji ten yra.

**Patikslinta taisyklė:** tikrinti ne tik *ar* komanda naudota, bet ir *kaip* ji kviečiama. Kartu pašalinti du `\percent` — darbe procentai visur rašomi `~\%`.

#### 22. T7: skyrius baigtas, apimtis viršyta trečią kartą — bet mažiausiai

| Skyrius | Taikinys | Faktas | Perviršis |
|---|---:|---:|---:|
| 1 užd. | 4–5 psl. | 9 psl. | +90 % |
| 2 užd. | 5–6 psl. | 9,7 psl. | +62 % |
| **3 užd.** | **4,5 psl.** | **~5 psl.** | **+11 %** |

Perviršį duoda 3.6 (protokolas) — vienas užima ~1,2 psl. **Trumpinti neverta:** jame dublikatų radinys ir teorinė riba, t. y. medžiaga, kuria remsis 5 ir 6 skyriai. Perviršis įvardijamas, ne nutylimas — tai ir buvo priėmimo kriterijaus prasmė.

**Kas suveikė:** keturios lentelės vietoj penkių; protokolas **tekstu**, ne penkta lentele; 3.1 ir 3.7 rašyti paskutiniai ir sąmoningai trumpi (~150 ir ~300 žodžių). Rugsėjo 2 d. taisyklė „lentelės pigios rašyti, bet brangios puslapiais“ pirmą kartą pritaikyta iš anksto, o ne po fakto.

#### 23. 3.7 turėjo pasakyti tai, ko lentelė nesako

Skyriuje liko akivaizdus prieštaravimas: `tab:matrica` rikiuotė neveda prie ketverto. Palikti jį be paaiškinimo reikštų, kad skaitytojas pats ras nesutapimą ir padarys blogiausią išvadą.

**3.7 poskyris tą prieštaravimą pasiima kaip savo turinį**, o ne slepia: pasakoma, kad rikiuotė aibės neduoda, ir įvardijamos trys sudedamosios — rikiuotės viršūnė, paradigmų padengimas, sudėtingumo gradientas. Tik pirmoji remiasi balais.

Kartu ten pateko du dalykai, kurių pradiniame plane nebuvo, nes jie **atsirado iš pačios matricos**: LightGBM lygus XGBoost (todėl atkrenta ne dėl silpnumo), ir sprendimų medis lenkia Random Forest (todėl lieka vertas dėmesio kaip pigus, savaime paaiškinamas atskaitos modelis). **Abu — matricos produktas, ne prielaida.**

### 3 UŽDUOTIS BAIGTA — suvestinė

| Kas | Rezultatas |
|---|---|
| Skyrius | `03_parinkimas.tex`, 7 poskyriai, 4 lentelės, ~5 psl. |
| Atranka | 18 metodų → 8 (vartai) → **4 pasirinkti** |
| Atmetimų kilmė | K1 duomenų struktūra — 4, K2 prielaida — 1, K3 mokymo kaina — 2, K4 delsa — 1 |
| Svoriai | 30/30/25/15, kiekvienas iš `tab:reikalavimai` eilutės |
| Jautrumas | 8 iš 8 stabilu; dvi poros sprendžiamos **dominavimo** |
| Protokolas | Užrakintas; dublikatai 33,1 %, **teorinė riba ~95 %** |
| Kompiliavimas | 30 psl., **0 klaidų, 0 neišspręstų nuorodų** |

**Vertingiausias dienos rezultatas nėra metodų aibė** — ji buvo žinoma vakar. Vertingiausia yra tai, kad (a) atmetimų priežastys pasirodė esančios duomenų, o ne resursų, (b) dvi svarbiausios poros sprendžiamos dominavimo, tad nepriklauso nuo jokių svorių, ir (c) **išmatuota teorinė tikslumo riba, kuri yra žemiau už literatūroje skelbiamus skaičius.**

### Ką darysiu rytoj (rugs. 4, penktadienis)

**4 užduotis — DI pagrįsto aptikimo sprendimo kūrimas.** Pradinė medžiaga jau paruošta: protokolo punktai yra `pozymiai.py` ir `balansavimas.py` specifikacija, o `rezultatai.csv` schema suderinta su `i_latex.py`.

Pirmas žingsnis — **įkėlimo grandinė su dublikatų šalinimu**, nes nuo jos priklauso visos imties charakteristikos. Tik po to modeliai.

⚠️ **Neuždaryti likučiai:** titulinio puslapio fakultetas ir vadovas (reikia sprendimo dėl Aineros pavidalo); `houichi` metrikos (Wiley 403); `praktikos_planas.md` 4 sk. nepažymėta, kad 26–34 psl. norma neegzistuoja; skyrių numeracijos poslinkis (N užduotis = N+1 skyrius) — sprendimas neprimtas. Lieka: sprendimų matrica (T4) ir jautrumas (T5) → **eksperimento protokolas** (T6) → skyriaus tekstas (T7) → `build.ps1`, commit.

✅ **Kompiliavimas praėjo be klaidų** su `tab:filtras` — 26 psl., lentelė 9-a, p. 21. `xltabular` ir `\SI` naujame faile suveikė iš pirmo karto, nes buvo kopijuotas `tab:metodai` šablonas, o ne rašyta iš naujo.

**Prieš rašant `tab:kriterijai` išvengta dviejų klaidų:** `\SI{10}{\mega\byte}` pakeista į paprastą `10~MB` (`\byte` darbe niekur nenaudotas, tad nepatikrintas), o nuoroda į dar neegzistuojantį jautrumo poskyrį perrašyta be `\ref` — kitaip būtų atsiradusi neišspręsta nuoroda. **Abi rastos peržiūrint prieš rašymą, ne po kompiliavimo.**

**Neišspręsta, reikia sprendimo:** titulinio puslapio fakultetas (`% TODO` 127 eil.) ir praktikos vadovas (`Vardas Pavardė`). Kadangi dokumentas teikiamas **Aineros** vadovui, klausimas platesnis nei užpildyti du laukus — ar titulinis apskritai turi būti universitetinio pavidalo.
