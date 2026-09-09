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

#### 24. T8: šaltiniai užpildė spragą, ne skaičių ⭐

Pridėti du įrašai (18 → **20**), abu su Crossref patikrintais DOI:

| Raktas | Šaltinis | Kam |
|---|---|---|
| `chawla2002smote` | Chawla et al. (2002), *JAIR* 16:321–357 | SMOTE abliacija |
| `dietterich1998tests` | Dietterich (1998), *Neural Computation* 10(7) | Kodėl 3 paleidimų neužtenka |

⭐ **Dietterich atskleidė tikrą protokolo spragą.** Rašydamas 3.6 buvau užrašęs „pateikiamas vidurkis ir standartinis nuokrypis“ — ir viskas. **Nebuvo pasakyta, kaip skirtumas tarp modelių bus laikomas tikru.** Dietterich rodo, kad pakartotinio perskirstymo testai turi pervertintą I tipo klaidą, o t-testas ant trijų paleidimų yra kaip tik toks. Todėl protokole dabar užrašyta: skirtumas reikšmingas tik viršijęs paleidimų sklaidą, formalus testas neatliekamas.

**Be šaltinio šis punktas būtų likęs neužrakintas** — o T6 priėmimo kriterijus reikalavo, kad neužrakintų nebūtų. Vadinasi, T8 iš tikrųjų uždarė T6 skylę.

**Abu šaltiniai — 1998 ir 2002 m., seniausi visame darbe.** Sąmoningai: metodo aprašui cituojamas pirminis šaltinis, ne naujausias jį minintis darbas. `imani2025imbalance` lieka empiriniam SMOTE + XGBoost rezultatui.

**Demšar (2006) atmestas dviem priežastimis:** skirtas palyginimui per daug rinkinių (čia rinkinys vienas), ir JMLR straipsnis DOI neturi.

**Rašant anotaciją atsirado trečias argumentas dėl SMOTE.** Jis interpoliuoja tarp artimiausių kaimynų, o mūsų duomenyse 4,98 % eilučių turi prieštaringas etiketes — sintetiniai pavyzdžiai tokiose srityse dviprasmiškumą tik sustiprintų. Iki šiol SMOTE buvo abliacija dėl biudžeto ir dėl `imani2025imbalance`; dabar yra ir duomenų argumentas.

**Patikra:** 20 `.bib` raktų, dublikatų nėra, skliaustai subalansuoti, be DOI tik `antonakakis2017mirai` (USENIX, jo neturi). Anotacijos padengia **20 iš 20**.

#### 25. Vadovas: procesas ataskaitoje neturi ko veikti ⭐⭐⭐

Peržiūrėjęs 3 skyrių vadovas nurodė esminį dalyką: **darbe nerašoma apie savo klaidas, dvejones ir atmestas alternatyvas.** Toks turinys priklauso žurnalui.

**Rugsėjo 2 d. tą taisyklę pats užsirašiau** (įrašas „kur rašiau prieš save“) ir per dieną sulaužiau dešimtyje vietų. Pašalinta:

| Kur | Kas buvo | Kodėl blogai |
|---|---|---|
| 3.1 | „svertinė matrica, kurios rezultatas sutampa su iš anksto žinomu atsakymu, yra retorinė priemonė“ | Gynyba nuo priekaišto, kurio niekas nepareiškė — ir pati **pasiūlo** skaitytojui tokį įtarimą |
| 3.1 | „subjektyvumas lieka vieninteliame taške“ | Savęs komentavimas |
| 3.5 | „toks rezultatas nereiškia, kad rikiuotė teisinga — zondas buvo per siauras“ | Mano metodo savikritika; skaitytojui rūpi riba, ne mano zondas |
| 3.6 | „Priežastis metodinė: jei metrikos pasirenkamos matant rezultatus…“ | Pasiaiškinimas, kodėl elgiuosi sąžiningai |
| 3.6 | „Dublikatai — **svarbiausias šio protokolo punktas**“ | Aš sprendžiu, kas skaitytojui svarbiausia |
| 3.7 | „ir tai pasakytina atvirai“, „tai matyti iš lentelės“ | Retorika, ne turinys |
| `tab:kriterijai` | atmesto penkto kriterijaus apskaita | Skaitytojas apie jį nieko nežino |
| 3.6 | „apribojimas įvardijamas atvirai“ | Pagyrimas sau; dabar pasakyta per **pasekmę** — ko rezultatai negali parodyti |

**−109 žodžiai, ir skyrius nuo to sustiprėjo.** Apribojimai liko visi; dingo tik pasakojimas apie tai, kaip aš prie jų priėjau.

**Skirtis, kurią reikia laikyti galvoje 4–6 skyriuose:**

- **Į darbą** — kas išmatuota, kas pasirinkta, kokia to pasekmė rezultatams. Apribojimas rašomas kaip **duomenų ar metodo savybė**: „rinkinyje nėra laiko žymos, todėl rezultatai nieko nesako apie elgseną laikui bėgant“.
- **Į žurnalą** — kaip prie to priėjau, ką bandžiau, kur suklydau, kodėl persigalvojau.

⚠️ **Pataisytas ir per stiprus teiginys.** Buvau parašęs, kad literatūros 99,5–99,6 % „greičiausiai lieka dublikatų nutekėjimas“ — **neperskaitęs tų darbų metodikos**. Dabar: skaičiai yra aukščiau už ribą, o ar dublikatai buvo šalinami, iš straipsnių nematyti. Kartu pridėta, kad riba matuota 1,9 mln. eilučių imtyje ir bus tikslinama.

### 3 UŽDUOTIS BAIGTA — suvestinė

| Kas | Rezultatas |
|---|---|
| Skyrius | `03_parinkimas.tex`, 7 poskyriai, 4 lentelės, ~5 psl. |
| Atranka | 18 metodų → 8 (vartai) → **4 pasirinkti** |
| Atmetimų kilmė | K1 duomenų struktūra — 4, K2 prielaida — 1, K3 mokymo kaina — 2, K4 delsa — 1 |
| Svoriai | 30/30/25/15, kiekvienas iš `tab:reikalavimai` eilutės |
| Jautrumas | 8 iš 8 stabilu; dvi poros sprendžiamos **dominavimo** |
| Protokolas | Užrakintas; dublikatai 33,1 %, **teorinė riba ~95 %** |
| Šaltiniai | 18 → **20**, visi su patikrintu DOI, anotacijos 20/20 |
| Kompiliavimas | 30 psl., **0 klaidų, 0 neišspręstų nuorodų** |

**Vertingiausias dienos rezultatas nėra metodų aibė** — ji buvo žinoma vakar. Vertingiausia yra tai, kad (a) atmetimų priežastys pasirodė esančios duomenų, o ne resursų, (b) dvi svarbiausios poros sprendžiamos dominavimo, tad nepriklauso nuo jokių svorių, ir (c) **išmatuota teorinė tikslumo riba, kuri yra žemiau už literatūroje skelbiamus skaičius.**

#### 26. Trys žinomos 3 skyriaus silpnybės — perkeliamos, ne užmirštamos ⚠️

Skyrius atitinka abu planus, bet po kritinės peržiūros liko trys dalykai, kurių **planai nereikalavo** ir kurie todėl liktų neužrašyti. Jie nėra klaidos ataskaitoje — tai žinomos jos ribos.

**1. Tikrinau ne tą subjektyvumą.** Jautrumo analizė vertino **svorius** (4 skaičiai su pagrindimu), o ne **balus** (32 skaičiai be jo). Patikrinta: „dominavimas“ RF prieš MLP griūva nuo **vieno balo** pakeitimo — jie sutampa trijuose kriterijuose iš keturių ir skiriasi tik interpretuojamumu. Teiginys formaliai teisingas, bet silpnesnis, nei skamba.
→ *Veiksmas:* paleisti tą pačią procedūrą ±1 balui. Skriptas jau yra.

**2. `tab:matrica` „Šalt.“ stulpelis nurodo eilutę, ne balą.** 2 užduotyje pats užsirašiau taisyklę, kad kiekvienas įvertinimas turi turėti šaltinį arba `(aut.)`. Publikuotus CICIoT2023 skaičius turi tik XGBoost ir LightGBM; RF, medžio, MLP ir 1D-CNN kokybės balai yra mano vertinimai skaičiaus pavidalu.
→ *Veiksmas:* arba per-balo žymos, arba aiškiai pasakyti, kad balai yra autoriaus vertinimas pagal `tab:metodai`.

**3. Sprendimų medis prieš Random Forest — neišspręsta.** Matrica sako, kad medis geresnis (3,80 prieš 3,55). Ataskaitoje parašyta „vertas dėmesio“, ir tiek. Pagrindimas „sudėtingumo gradientas“ yra kriterijus, kurio niekas neišvedė iš `tab:reikalavimai` — ta pati yda, kurią pats įžvelgiau svoriuose.
→ *Veiksmas:* arba penktas metodas 4 užduotyje, arba pagrindimas, kuris remiasi kuo nors, o ne patogumu.

**Ketvirtas, techninis:** 62,6 pt overfull 24 psl. — lentelė kyšo ~2,2 cm už paraštės. Kompiliavimą praeina, bet spaudinyje matyti. Didžiausias visame darbe (anksčiau 38,6 pt 1 skyriuje).

### Ką darysiu rytoj (rugs. 4, penktadienis)

**4 užduotis — DI pagrįsto aptikimo sprendimo kūrimas.** Pradinė medžiaga jau paruošta: protokolo punktai yra `pozymiai.py` ir `balansavimas.py` specifikacija, o `rezultatai.csv` schema suderinta su `i_latex.py`.

Pirmas žingsnis — **įkėlimo grandinė su dublikatų šalinimu**, nes nuo jos priklauso visos imties charakteristikos. Tik po to modeliai.

⚠️ **Neuždaryti likučiai:** titulinio puslapio fakultetas ir vadovas (reikia sprendimo dėl Aineros pavidalo); `houichi` metrikos (Wiley 403); `praktikos_planas.md` 4 sk. nepažymėta, kad 26–34 psl. norma neegzistuoja; skyrių numeracijos poslinkis (N užduotis = N+1 skyrius) — sprendimas neprimtas. Lieka: sprendimų matrica (T4) ir jautrumas (T5) → **eksperimento protokolas** (T6) → skyriaus tekstas (T7) → `build.ps1`, commit.

✅ **Kompiliavimas praėjo be klaidų** su `tab:filtras` — 26 psl., lentelė 9-a, p. 21. `xltabular` ir `\SI` naujame faile suveikė iš pirmo karto, nes buvo kopijuotas `tab:metodai` šablonas, o ne rašyta iš naujo.

**Prieš rašant `tab:kriterijai` išvengta dviejų klaidų:** `\SI{10}{\mega\byte}` pakeista į paprastą `10~MB` (`\byte` darbe niekur nenaudotas, tad nepatikrintas), o nuoroda į dar neegzistuojantį jautrumo poskyrį perrašyta be `\ref` — kitaip būtų atsiradusi neišspręsta nuoroda. **Abi rastos peržiūrint prieš rašymą, ne po kompiliavimo.**

**Neišspręsta, reikia sprendimo:** titulinio puslapio fakultetas (`% TODO` 127 eil.) ir praktikos vadovas (`Vardas Pavardė`). Kadangi dokumentas teikiamas **Aineros** vadovui, klausimas platesnis nei užpildyti du laukus — ar titulinis apskritai turi būti universitetinio pavidalo.

---

## Rugsėjo 6 d. (sekmadienis) — 4 užduoties planas

### Ką padariau

**Peržiūrėta visa turima medžiaga** — projekto dokumentai (`praktikos_planas.md`, trys užduočių planai, šis žurnalas, `STRUKTURA.md`) **ir realus repozitorijos turinys**, ne tik būklės žymos.

**Sudarytas 4 užduoties tikslų planas** (`claude/uzduotis_04_planas.md`): tikslai T0–T9, dublikatų šalinimo algoritmas, modelių sąsajos kontraktas, skyriaus struktūra, trijų dienų laiko biudžetas, priėmimo kriterijai, rizikos.

**Rugsėjo 4–5 d. nedirbta** (paskutinis commit — `96ef95a`, rugs. 3 d.). Grafikas vis tiek 5 dienomis priekyje pradinio plano.

### Priimti sprendimai

- **4 užduotis vykdoma rugsėjo 7–9 d.** (pradiniame plane — rugs. 9–14). Trys dienos: duomenų grandinė · modeliai ir pirmas ciklas · prototipas ir skyrius.
- **Prototipas su vizualizacija įeina į užduotį** (Streamlit), bet **P1 prioritetu**: po rugs. 9 d. 11:30 jis stabdomas, koks bebūtų — skyrius svarbiau.
- **Skyrių numeracija paliekama kaip yra** — „Įvadas“ lieka 1 skyrius, todėl N užduotis = N+1 skyrius. Klausimas, atviras nuo rugs. 3 d., **uždarytas**. Kadangi vienintelis vadovo turimas kriterijus yra užduočių sąrašas, atitikimą turi užtikrinti kas kita nei numeriai — skyrių antraštės jau atkartoja užduočių formuluotes.
- **`i_latex.py` perrašomas, ne protokolas** (žr. žemiau). Kartu keičiasi jo vaidmuo: iš „CSV → lentelė“ į **agregavimo žingsnį** (vidurkis ± std per seed'us, dvi išvesties lentelės).
- **Dublikatai šalinami klasės viduje, srautu, per eilučių maišas** — protokolo reikalavimas „prieš imtį“ išlaikomas, bet be 14 GB atminties poreikio.
- **4 skyriaus apimties taikinys nemažinamas.** 1–3 skyriuose taikinys buvo stabdis; čia jis yra grindys. Vienintelė likusi apimties rizika yra ~23 psl. teorijos prieš plonus 4–6 skyrius.

### Ką radau

#### 1. Trys priėmimo kriterijai pažymėti atliktais neatidarius failo ⚠️⭐

Visi trys — tas pats klaidos tipas, kuris darbe kartojasi **ketvirtą kartą**: rugsėjo 2 d. tai buvo duomenų aprašas, sudarytas neatidarius duomenų; rugsėjo 3 d. — priėmimo kriterijus, parašytas nepažiūrėjus į `.aux`.

**`rezultatai.csv` schema su `i_latex.py` NĖRA suderinta.** Kriterijus teigia priešingai. Sutikrinus: sutampa **3 stulpeliai iš 15**. Skriptas laukia `f1_macro`, `precision_macro`, `recall_macro`, `inferencijos_ms`; protokolas fiksuoja `macro_f1`, `pr_auc`, `roc_auc`, `mcc`, `inferencija_us` ir dar aštuonis. Paleistas skriptas mestų `SystemExit`.

**`ikelimas.py` neįgyvendina užrakinto protokolo.** Kode `FRAKCIJA = 0.05`, `MIN_EILUCIU = 5000`; protokole — riba 100 000 eilučių klasei. Retoms klasėms sutampa, gausioms ne: proporcinga frakcija **disbalanso nemažina** (~288:1 vietoj 84:1), o būtent jo sumažinimas buvo pusė ribos pagrindimo. Kode taip pat nėra dublikatų šalinimo, `dropna`/`inf` tvarkymo ir skaidymo išsaugojimo — visa tai aprašyta protokole ir `duomenys/README.md`, bet neegzistuoja.

**Dublikatų matavimo skripto nėra.** 33,1 % ir ~95 % teorinė riba yra stipriausi darbo radiniai, kuriais remiasi trys skyriai, bet `rezultatai/darbiniai/` juos pagrindžiančio failo nėra — skaičiai gauti ad hoc ir **neatkartojami**.

> **Pamoka:** priėmimo kriterijus, pažymėtas atliktu nepaleidus komandos, yra **spėjimas apie savo paties darbą**. Nuo šiol kriterijus, kurio patikra yra viena komanda, žymimas tik po tos komandos.

#### 2. „Dublikatai prieš imtį“ ir RAM — konfliktas su sprendimu ⭐⭐

`df.duplicated()` ant 45,0 mln. eilučių × 39 `float64` požymių yra ~14 GB vien duomenų. Protokolo 9 punktas, kaip parašytas, nešiojamame kompiuteryje neįvykdomas.

Trys pastebėjimai jį panaikina: dublikatas visada yra **klasės viduje** (kitos klasės sutapimas yra prieštaringa etiketė, kurią protokolas liepia palikti); palyginti reikia **maišų**, ne eilučių (45 mln. × 8 B = 360 MB vietoj 14 GB); o klasėms, kurios po šalinimo vis tiek viršija 100 000 ribą, **tvarka „prieš/po“ duoda tą patį rezultatą**. Tvarka svarbi tik toms, kurios nukrenta žemiau ribos.

Lieka vienas nukrypimas, kurį reikia įvardyti: eilutės imamos failų tvarka, ne atsitiktinai iš viso rinkinio. Apsauga — surinkti iki 150 000 unikalių eilučių klasei ir atsitiktinai atrinkti 100 000.

#### 3. Autokoderis į vienodą kontraktą telpa tik su išlyga ⭐

Palyginimo asimetrija numatyta rugsėjo 2 d. (2.8 poskyris) ir įgyvendinta rugsėjo 3 d. matricos sandaroje. **Kode ji turi atsirasti trečią kartą:** `predict_proba` apibrėžiamas kaip „įvertis, kurio didesnė reikšmė reiškia didesnę atakos tikimybę“, ne kaip tikimybių matrica, o laukas `priziurimas = False` pasako `paleisti.py`, kad macro-F1 per 8 kategorijas šiam modeliui neskaičiuojamas. Jei to nebus kontrakte, tai išlįs rugsėjo 15 d. kaip `ValueError` viduryje ciklo.

#### 4. Smulkmena, kuri būtų kainavusi valandą diagnostikos

Failas `src/modeliai/xgboost.py` uždengtų biblioteką `import xgboost`. Pervadinta į `gradientinis.py` dar plane. `cnn.py` (0 B) nebeatitinka ketverto — ištrinti.

#### 5. Pirmi paveikslai visame darbe

`paveikslai/` tuščias, `\includegraphics` niekur nenaudotas, taigi **nepatikrintas**. Taisyklė „naudoti tik tai, kas darbe jau įrodyta veikiant“ čia neišvengiamai laužoma, todėl pirmas paveikslas dedamas rugsėjo 8 d., ne 9 d. — turint dieną atsargos.

### Vakare — T0 atliktas, nelaukiant pirmadienio ✅

Trys neatitikimai uždaryti tą pačią dieną, kai buvo rasti.

**`i_latex.py` perrašytas.** Priimtas sprendimas taisyti skriptą, ne protokolą: protokolas užrakintas ir kiekvienas jo stulpelis turi pagrindimą, o skriptas rašytas rugsėjo 1 d., kai nieko iš to dar nebuvo nuspręsta. Kartu pasikeitė jo vaidmuo — iš „CSV → lentelė" į **agregavimo žingsnį**: 15 stulpelių į puslapį netelpa, o CSV turi po eilutę kiekvienam seed'ui, todėl skriptas grupuoja pagal modelį ir formuluotę, skaičiuoja vidurkį ± standartinį nuokrypį ir išveda **dvi** lenteles — `rezultatai.tex` (kokybė) ir `veikimas.tex` (delsa, mokymo laikas, dydis).

**`ikelimas.py` perrašytas.** Įgyvendina protokolo 5.1–5.4: valymo tvarką, dublikatų šalinimą, ribą 100 000 klasei, teorinės ribos perskaičiavimą. Trečias neatitikimas — neatkartojamas dublikatų matavimas — **išnyko kaip atskira problema**: matavimas dabar yra pačios grandinės dalis ir kaskart išvedamas į `imties_ataskaita.md`.

### Ką radau rašydamas kodą

#### 6. Vieno prėjimo per duomenis nepakanka ⭐

Plane buvau numatęs vieną prėjimą su 1,5× atsarga (surinkti 150 000, atrinkti 100 000), kad kompensuočiau failų tvarkos šališkumą. Rašant paaiškėjo, kad tai apėjimas, o ne sprendimas: **kad imtis būtų tolygiai atsitiktinė iš unikalių eilučių, reikia iš anksto žinoti, kiek jų klasėje yra.**

Todėl pirmas prėjimas skaičiuoja maišas ir atrenka, antras renka eilutes. Kaina — dvigubas skaitymas; nauda — imtis **nepriklauso nuo eilučių tvarkos failuose**, todėl atsargos nebereikia ir nukrypimo nuo protokolo, kurį plane ketinau įvardyti ataskaitoje, nebelieka.

#### 7. `float64` kastinimas yra determinizmo sąlyga, ne kosmetika ⭐⭐

`pandas` tipą nustato **kiekvienam gabalui atskirai**, todėl tas pats stulpelis viename gabale gali būti `int64`, kitame `float64` — ir vienodos reikšmės duotų **skirtingas maišas**. Du prėjimai tada nesutaptų, o klaida pasirodytų ne kaip klaida, o kaip nepaaiškinamai maža imtis.

Tai tos pačios rūšies spąstai kaip `Duration` = TTL: dalykas, kurio supainiojimas nemeta klaidos. Patikrinta tiesiogiai — paleidus su gabalu 500 ir 137 rezultato `md5` sutampa.

#### 8. Tikslumo ryškinti negalima ⚠️

Pirma lentelės versija paryškindavo geriausią reikšmę **kiekviename** stulpelyje — įskaitant bendrą tikslumą, po kuriuo tos pačios lentelės išnaša sako, kad prie 41,8:1 santykio jis nėra rodiklis. Lentelė būtų prieštaravusi savo pačios išnašai.

**Ryškinama tik macro-F1** — protokolo pagrindinė metrika. Kartu pašalinta `± 0,000`: kai sklaida rodomu tikslumu lygi nuliui, ji nerodoma, nes nulinis nuokrypis atrodo kaip informacija, kurios nėra.

Abu radiniai atsirado **skaitant savo paties išvestį**, ne rašant kodą. Tai argumentas visada atspausdinti pavyzdinę lentelę, o ne pasitikėti, kad kodas teisingas.

#### 9. Teorinė riba skaičiuojama tiksliau nei rugsėjo 3 d. ⭐

Rugsėjo 3 d. ribą vertinau kaip „dviprasmiškų eilučių dalį" (4,98 % → ~95 %). Tai per grubu: jei vektorius pažymėtas 9 kartus `A` ir 1 kartą `B`, klasifikatorius suklysta **vieną** kartą iš dešimties, o ne dešimt.

Dabar skaičiuojama **Bajeso riba**: kiekvienai prieštaringai grupei geriausias įmanomas klasifikatorius parenka dažniausią etiketę, todėl neišvengiama klaida yra *(grupės dydis − dažniausios etiketės dažnis)*. Ataskaitoje pateikiami abu skaičiai, nes 3 skyriuje cituojamas pirmasis.

**Tikėtina pasekmė: patikslinta riba bus aukštesnė nei 95 %.** Jei taip, `03_parinkimas.tex` teiginys apie literatūros 99,5–99,6 % susilpnėja — ir tai reikės parašyti, o ne nutylėti.

#### 10. Kaip patikrinau — sintetinis rinkinys su nepriklausomu orakulu ⭐

Sukurtas 34 klasių sintetinis rinkinys su **iš anksto žinomu** atsakymu: suplanuoti dublikatai, viena `Rate = inf` eilutė, viena nutrūkusi eilutė failo gale, viena prieštaringų etikečių pora. Laukiami skaičiai apskaičiuoti **nenaudojant tikrinamo modulio**.

**13 patikrų iš 13 praėjo.** Svarbiausia iš jų — atkartojamumas prie skirtingų gabalo dydžių: būtent ji būtų pagavusi 7 punkto klaidą, jei kastinimo nebūčiau padaręs.

⚠️ **Ko patikra nepadengia:** tikrųjų 8,7 GB, `to_parquet` su tikru dydžiu ir atminties elgsenos prie 45 mln. eilučių. Paaiškės rytoj ryte.

> **Pamoka, uždaranti šios dienos ratą.** Ryte užsirašiau, kad priėmimo kriterijus, pažymėtas atliktu nepaleidus komandos, yra spėjimas apie savo paties darbą. Vakare tą taisyklę pritaikiau pirmą kartą sąmoningai: **niekas nepažymėta atliktu, kol nepaleista.** Tai kainavo apie valandą ir sugavo dvi klaidas, kurios kitaip būtų išlindusios rugsėjo 8 d. viduryje eksperimentų.

### Vėliau vakare — T1 taip pat atliktas ✅

Prieš paleidžiant rasta viena kliūtis: **`sprendimu_matrica.csv` nebuvo Git'e.** `.gitignore` turi `*.csv` su viena išimtimi (`rezultatai/rezultatai.csv`), todėl failas, kurį `STRUKTURA.md` vadina „vieninteliu balų šaltiniu", egzistavo tik šioje mašinoje. Švarioje kopijoje `tab:matrica` būtų neatkuriama, o „lentelės generuojamos, o ne rašomos ranka" principas nustotų galioti. Pridėta išimtis `!rezultatai/darbiniai/*.csv`.

**Įkėlimo grandinė paleista ant tikrų 63 failų.** Rezultatai — `rezultatai/darbiniai/imties_ataskaita.md`.

### Ką radau — T1

#### 11. Valymo skaitliukai sutapo su rugsėjo 2 d. radiniais tiksliai ⭐

| Rodiklis | Rugs. 2 d. | Rugs. 6 d. |
|---|---:|---:|
| Eilučių iš viso | 45 019 243 | **45 019 243** |
| Nutrūkusių eilučių | 9 | **9** |
| `Rate = Infinity` | 991 | **991** |

Tai nepriklausomas patvirtinimas, kad rugsėjo 2 d. skenavimas buvo teisingas. Vertinga ne dėl skaičių, o dėl to, kad pirmą kartą darbe **du nepriklausomi matavimai sutapo** — iki šiol kiekvienas patikslinimas ką nors paneigdavo.

#### 12. Dublikatų ne 33,1 %, o 53,3 % ⭐⭐

Rugsėjo 3 d. skaičius buvo iš 1,9 mln. eilučių imties. Visame rinkinyje — **53,34 %**: iš 45 018 243 eilučių unikalios tik 21 004 674.

**Argumentas dėl nutekėjimo nuo to sustiprėjo**: rinkinyje, kur kas antra eilutė yra kitos kopija, atsitiktinis skaidymas be dublikatų šalinimo garantuoja, kad dalis testavimo aibės modeliui jau matyta.

**Pasiskirstymas struktūrinis, ne atsitiktinis:**

| Klasių grupė | Dublikatų |
|---|---|
| Potvynio (`DDOS-ICMP_FLOOD`, `DDOS-RSTFINFLOOD`, …) | **41–72 %** |
| Mirai, MITM | 3,5–10 % |
| `BENIGN` | **0,38 %** |
| Retos atakų klasės (13 klasių) | vidutiniškai **0,49 %**; šešiose — **0 %** |

Iš to seka dalykas, kurio plane nebuvo: **dublikatų šalinimas pats savaime mažina disbalansą**, nes traukiasi būtent gausiausios klasės. Riba 100 000 tik užbaigia tai, ką pradeda šalinimas.

#### 13. Teorinė riba ne ~95 %, o 99,78 % ⚠️⚠️ — 3 skyrius pataisytas

Tai didžiausias šios dienos pokytis, ir jis **panaikina vieną 3 skyriaus argumentą**.

| | Rugs. 3 d. | Rugs. 6 d. |
|---|---|---|
| Ką matavau | dviprasmiškų eilučių dalį **su dublikatais** | Bajeso klaidą **be dublikatų** |
| Prieštaringi vektoriai | 55 440 | **5 114** |
| Dviprasmiškos eilutės | 4,98 % | **0,43 %** (10 435) |
| Riba | ~95 % | **99,78 %** |

**Dvi priežastys, ir abi mano.** Pirma, rugsėjo 3 d. skaičiavau dviprasmiškų eilučių dalį, o ne neišvengiamą klaidą: jei vektorius pažymėtas 9× `A` ir 1× `B`, klasifikatorius suklysta vieną kartą iš dešimties, o ne dešimt. Antra — ir tai svarbiau — **matavau prieš dublikatų šalinimą**. Dublikatai dviprasmiškumą pučia: vektorius, pasikartojantis 1000× kaip `A` ir 1000× kaip `B`, prieš šalinimą duoda 2000 „dviprasmiškų eilučių", o po jo — dvi eilutes ir vieną neišvengiamą klaidą.

⚠️ **Pasekmė: teiginys „literatūros 99,5–99,6 % yra aukščiau už teorinę ribą" nebegalioja.** 99,5–99,6 yra **žemiau** 99,78. Argumentas buvo stipriausias 6 skyriaus koziris, ir jo nebėra tokio, koks buvo.

**Kas lieka vietoj jo — ir tai švaresnis argumentas.** Palyginamumo problema kyla ne iš ribos, o iš dublikatų: mūsų imtis jų neturi, o ar cituojamuose darbuose jie buvo šalinami, iš straipsnių nematyti. Tai teiginys apie **eksperimento sąlygas**, o ne apie kitų autorių skaičių teisingumą — ir jam nereikia prielaidos, kurios negaliu patikrinti. 3.6 poskyris perrašytas būtent taip.

> **Pamoka.** Rugsėjo 3 d. užsirašiau, kad riba „išmatuota 1,9 mln. imtyje ir bus tikslinama". Išlyga buvo teisinga, bet jos neužteko: skaičius jau buvo panaudotas kaip argumento pagrindas. **Skaičių su išlyga „bus patikslintas" galima rašyti į protokolą, bet ne daryti jo argumento ašimi.**

#### 14. Modulis lūžo ties atmintimi — ir tai buvo tikra klaida, ne VM ypatybė ⭐

Antrame prėjime `imtis()` sudėdavo visas surinktas eilutes į vieną `DataFrame` ir tik tada kviesdavo `drop_duplicates`. Atrinktos 2,43 mln. maišų duomenyse pasirodo **3,99 mln. kartų**, todėl sudėtas rinkinys buvo 65 % didesnis už galutinį, o `concat` atmintį dar padvigubino. Procesas buvo nužudytas (OOM).

**Pataisyta modulyje, ne apėjime:** dublikatai dabar šalinami gabalas po gabalo, `dalys` sąraše visada tik unikalios eilutės. Praleista 1 164 221 kartotinių pasirodymų.

Tai klaida, kurios sintetinis testas **negalėjo** pagauti — 537 eilutės telpa bet kur. Ją parodė tik tikras rinkinys. **Iš to seka taisyklė: testas su mažais duomenimis tikrina teisingumą, bet ne mastelį; abu reikia tikrinti atskirai.**

Po pataisymo sintetinis testas paleistas iš naujo — **13 iš 13 tebepraeina.**

#### 15. Maišų susidūrimų nebuvo nė vieno

Surinkta **2 425 937** eilutės — lygiai tiek, kiek buvo atrinkta maišų. Modulio dokumentacijoje įvardyta ~5·10⁻⁸ susidūrimo tikimybė liko teorine. Patikra automatinė ir kartojasi kiekvieną paleidimą.

#### 16. Imtis atitiko prognozes tiksliau, nei tikėjausi

| Rodiklis | Planuota | Gauta |
|---|---|---|
| Eilučių | ~2 429 978 | **2 425 937** |
| Dalis rinkinio | 5,40 % | **5,39 %** |
| Disbalansas | 84:1 | **84:1** |
| `BENIGN` (autokoderio mokymo aibė) | ~100 000 | **100 000** |

**13 klasių iš 34 ribos nepasiekia** — joms imtis yra visa klasė po dublikatų šalinimo, ir daugiau tų duomenų neegzistuoja. Mažiausia — `UPLOADING_ATTACK`, 1 196 eilutės, po 70/15/15 liks **179 testavimo pavyzdžiai**.

⭐ **Vienas dalykas nematytų klasių testui:** `DDOS-SLOWLORIS` turi **0 % dublikatų** ir visas 22 399 eilutes. Sunkiausias scenarijus bent jau nėra apsunkintas dar ir duomenų trūkumu.

### Ką darysiu rytoj (rugs. 7, pirmadienis)

**T0 ir T1 atlikti, todėl diena prasideda nuo T2 — atlaisvinta ~4 val.**

⚠️ **Pirmas veiksmas — `cd ataskaita ; .\build.ps1`.** 3 skyrius pataisytas, bet Windows pusėje nekompiliuotas: Linux mašinoje nėra lietuviško babel ir `siunitx`. Struktūrinės patikros (kirilica, `\num` argumentai, skliaustai, `\section`) praeitos.

**T2 → T3 → T4.** Pirmas veiksmas — `ikelimas.py imtis` paleidimas ant tikrų 63 failų, fone; tuo metu rašomas požymių modulis. Dienos minimumas: `imtis.parquet` ir `skaidymas.npz` egzistuoja, realūs skaičiai užrašyti.

⚠️ **Atskiras 15:30–16:15 langas:** sutikrinti gautus skaičius su 3 skyriumi. Jei faktinis dublikatų procentas ar patikslinta teorinė riba skiriasi nuo užrašytų, `03_parinkimas.tex` taisomas **tą pačią dieną**.

---

## Rugsėjo 7 d. (pirmadienis) — T2, T3, T4

### Ką padariau

**Kompiliavimas patvirtintas:** `build.ps1` praėjo be klaidų, **31 psl.** Pataisytas 3 skyrius Windows pusėje veikia.

Trys moduliai, kurie iki šiol buvo 0 baitų: **`pozymiai.py`** (36 požymiai), **`skaidymas.py`** (70/15/15), **`balansavimas.py`** (klasių svoriai + SMOTE abliacija). Visi trys turi savipatikras ir paleisti ant tikros imties.

### Ką radau

#### 17. Tapatybės patikrintos darbinėje imtyje, ne tik žaliuose duomenyse ⭐

Rugsėjo 2 d. jos buvo tikrintos 500 000 eilučių. Dabar — visose 2 425 937:

| Tapatybė | Nesutapimų |
|---|---:|
| `Variance` = `Std`² | **0** |
| `Tot size` = `AVG` | **0** |
| `Tot sum` = `AVG` × `Number` | **0** |
| ~~`Rate` = 1/`IAT`~~ | **1 963 560 iš 2 425 937** (80,9 %) |

Šalinimo pagrindas galioja, o `Rate` lieka — kaip ir buvo nuspręsta. Patikra įrašyta į `pozymiai.py` ir kviečiama **kaskart prieš šalinant**: jei imtis ar veidrodis pasikeistų, šalinimas taptų nepagrįstas, ir tai turi pasirodyti kaip klaida, o ne kaip prastesnis modelio rezultatas.

#### 18. `Protocol Type` vos nepašalinau be pagrindo ⚠️

Atrodė akivaizdžiai perteklinis: rinkinyje jau yra `TCP`, `UDP`, `ICMP`, `IGMP` stulpeliai, tad protokolo kodas turėtų būti jų kartojimas. Patikrinau prieš šalindamas:

| | Sutapimas |
|---|---:|
| `Protocol Type` == 6 ↔ `TCP` == 1 | 69,78 % |
| `Protocol Type` == 17 ↔ `UDP` == 1 | 84,86 % |
| `Protocol Type` == 1 ↔ `ICMP` == 1 | 94,39 % |

**Ne tapatybė, o koreliacija.** Stulpelis neša savarankišką informaciją ir lieka. Ketvirtas kartas, kai patikra prieš veiksmą sustabdo klaidingą sprendimą — ir pirmas, kai ji apsaugojo nuo **duomenų praradimo**, o ne nuo klaidos tekste.

Kartu paaiškėjo smulkmena, kurios nežinojau: **nė vienas iš 39 stulpelių nėra dvejetainis.** „Vėliavėlių“ stulpeliai (`syn_flag_number` ir kt.) yra **dalys** 10/100 paketų lange, ne 0/1 požymiai. Tai keičia, kaip juos reikia skaityti 4 skyriuje.

#### 19. Mažos dispersijos filtras pašalintų būtent tuos požymius, kurie skiria retas klases ⭐⭐

Šeši stulpeliai daugiau nei 99,5 % eilučių turi tą pačią reikšmę: `ece_flag_number`, `cwr_flag_number`, `Telnet`, `SMTP`, `IRC`, `IGMP`. Automatinis filtras juos išmestų.

Patikrinau jų vidurkius pagal klases:

| Požymis | Kur didžiausias | Kiek kartų virš bendro vidurkio |
|---|---|---:|
| `IRC` | `BACKDOOR_MALWARE` | **×21,8** |
| `cwr_flag_number` | `UPLOADING_ATTACK` | ×15,6 |
| `IGMP` | `XSS` | ×11,9 |
| `Telnet` | `RECON-HOSTDISCOVERY` | ×9,6 |
| `SMTP` | `RECON-HOSTDISCOVERY` | ×9,0 |
| `ece_flag_number` | `XSS` | ×7,7 |

**Pasiskirstymas prasmingas, ne atsitiktinis.** `IRC` ties užpakalinių durų kenkėjiška programa yra klasikinis IRC valdymo kanalas; `Telnet` ir `SMTP` ties žvalgyba — prievadų skenavimas paliečia būtent tuos prievadus. Ir visos šešios klasės, kuriose požymiai sustiprėja, yra **rečiausios** — t. y. tos, kurios lemia macro-F1.

⚠️ **Sąžininga išlyga:** absoliučios reikšmės mažos (~0,001), tad tai silpni signalai, esantys ~0,1 % langų. Argumentas yra prieš **automatinį** šalinimą, o ne teiginys, kad šie požymiai daug duos.

Tai **antras nepriklausomas argumentas** ta pačia kryptimi kaip rugsėjo 2 d. koreliacijos radinys: pirmas rodo, kad filtras **nepašalina** to, ką turėtų; šis — kad **pašalina** tai, ko neturėtų. Abu eina į 4 skyrių, ir dabar poskyris apie požymius turi ką pasakyti be „pašalinome tris stulpelius“.

Šeši stulpeliai įrašyti į `pozymiai.py` kaip `SAUGOMI` su priežastimis — kad būtų aišku, jog jie palikti sąmoningai, o ne pramiegoti.

#### 20. Protokolo pataisa: `scale_pos_weight` daugiaklasėje užduotyje neveikia ⚠️

Protokolo 10 punktas XGBoost'ui numato `scale_pos_weight`. Rašant modulį paaiškėjo, kad **tas parametras veikia tik dvejetainėje užduotyje** — daugiaklasėje jis tiesiog ignoruojamas. Pagrindinė mūsų formuluotė yra 8 kategorijos.

Ekvivalentas — `sample_weight`, perduodamas `fit()` metu. Modulis grąžina eilučių svorių masyvą, o `scale_pos_weight` lieka tik dvejetainei formuluotei.

**Būtų buvusi tyli klaida:** XGBoost nemeta įspėjimo, modelis mokosi, o disbalansas lieka neatsvertas. Pasirodytų kaip nepaaiškinamai prastas macro-F1 — ir aš greičiausiai kaltinčiau duomenis, ne konfigūraciją.

#### 21. SMOTE būtų sintetinęs gerybinį srautą ⭐

Paleidus balansavimo patikrą pamačiau, kad prie ribos 10 % keliamos **trys** kategorijos: `BruteForce`, `Web` ir — `Benign`. Formaliai teisinga: gerybinis srautas 8 kategorijų užduotyje yra tokia pat klasė kaip kitos.

**Bet ne turinio prasme, ir dėl dviejų priežasčių.** Pirma, klaidingų teigiamų analizė (5 užduotis) turi remtis **tikru** gerybiniu srautu — interpoliuoti pavyzdžiai iškreiptų būtent tą rodiklį, kuriam atrankoje skirta 30 % svorio. Antra, autokoderio prielaida yra švarus gerybinio srauto profilis; sintetinis gerybinis srautas ją pažeistų.

Gerybinis srautas įrašytas į `NESINTETINAMOS` su abiem priežastimis. Keliamos dvi kategorijos, ne trys.

#### 22. Pilnas subalansavimas netelpa į biudžetą — riba 10 %

| Variantas | Eilučių po SMOTE |
|---|---:|
| Pilnas subalansavimas (8 × 734 996) | **5 879 968** (~1,7 GB) |
| Riba 10 % nuo gausiausios | **1 819 794** (+121 639) |

Pilnas subalansavimas viršytų 30 min. mokymo biudžetą vienam modeliui. **Abliacijos tikslas — patikrinti, ar sintetiniai pavyzdžiai padeda, o ne pasiekti lygias klases**, todėl riba 10 %. Įvardyta modulyje, kad rugsėjo 15 d. nereikėtų atkurti pagrindimo.

#### 23. Skaidymas pataikė į rugsėjo 2 d. prognozę tiksliai

| | |
|---|---|
| train / val / test | 1 698 155 / 363 891 / 363 891 (70,00 / 15,00 / 15,00 %) |
| Didžiausias klasės proporcijos nuokrypis | **0,0001 p. p.** |
| `UPLOADING_ATTACK` | 837 / 180 / **179** |

**179 testavimo pavyzdžiai** — lygiai tiek, kiek buvo suskaičiuota rugsėjo 2 d., dar neturint nei imties, nei skaidymo.

**Stratifikuojama pagal 34 etiketes, ne 8 kategorijas.** Kategorija yra etiketės funkcija, todėl stratifikavimas pagal etiketę automatiškai išlaiko ir kategorijų proporcijas — atvirkščiai negalioja: stratifikuojant pagal kategoriją retos klasės galėtų pasiskirstyti netolygiai savo kategorijos viduje.

**Keturios nutekėjimo patikros** įrašytos į modulį ir metamos kaip klaidos, ne įspėjimai: aibės nesikerta · padengia viską · **nėra vienodų eilučių tarp `train` ir `test`** · visos klasės visose aibėse. Trečioji imtyje be dublikatų yra savaime tenkinama, bet ji yra pagrindinė protokolo apsauga, todėl tikrinama tiesiogiai, o ne laikoma savaime suprantama.

> **Diena be nė vienos klaidos, kurią būtų pagavęs tik tikras paleidimas.** Visi keturi radiniai (`Protocol Type`, mažos dispersijos filtras, `scale_pos_weight`, SMOTE ant gerybinio srauto) rasti **prieš** veiksmą — tikrinant prielaidą, o ne taisant pasekmę. Tai pirmas kartas darbe, kai taisyklė „patikra prieš veiksmą“ suveikė keturis kartus iš eilės.

### Vėliau — T5 ir T6 atlikti tą pačią dieną

**Keturi modeliai su vienodu kontraktu ir eksperimentų paleidiklis.** Visi keturi patikrinti pilnu ciklu; mokymas perduotas paleisti Windows pusėje.

#### 24. Kontraktas fiksuotas prieš pirmą modelį — ir iškart atsipirko ⭐

`bazinis.py` parašytas **prieš** `random_forest.py`, kaip ir buvo suplanuota. Autokoderio išlyga įrašyta į kontraktą iš karto: laukas `priziurimas` ir `predict_proba`, apibrėžtas kaip „įvertis, kurio didesnė reikšmė reiškia didesnę atakos tikimybę“, o ne kaip tikimybių matrica.

Tai **trečias kartas**, kai ta pati palyginimo asimetrija įgyvendinama: rugsėjo 2 d. ji buvo pastaba tekste, rugsėjo 3 d. — matricos sandara, dabar — kodas. Kiekvieną kartą pigiau nei būtų buvę ją atrasti vėliau.

**Registras importuoja tik reikalingą modulį.** Pirma versija importavo visus keturis iš karto — tada `TensorFlow` būtų buvęs būtinas ir paleidžiant Random Forest. Pataisyta į `importlib` pagal raktą.

#### 25. Keturios klaidos, pagautos paleidžiant, ne skaitant

| Kas | Kaip pasirodė |
|---|---|
| `xgboost.py` uždengtų biblioteką | Numatyta plane; failas pavadintas `gradientinis.py` |
| **MLP dydis 0,00 MB** | Keras modelis guli atskirame `.keras` faile, o `dydis_mb` matavo tik apvalkalą |
| **MLP netilptų į biudžetą** | 30 epochų × batch 1024 ant 1,7 mln. → ~40 min. Pakeista į 20 × 4096 (13 s vietoj 42 s patikroje) |
| **Patikros modeliai gulė į tikrą aplanką** | Nuo 50 000 eilučių apmokytas failas tuo pačiu vardu greta tikrojo — vėliau nebeatskirtum. Dabar `_patikra/` |

Modelio dydis yra vienas iš keturių resursų kriterijaus rodiklių, tad **tyliai neteisingas nulis būtų buvęs blogiau už jo nebuvimą** — 6 skyriuje MLP atrodytų nemokamas.

#### 26. Autokoderio slenkstis yra klaidingų teigiamų rankenėlė, ne konvencija ⭐⭐

Numatytuoju buvau paėmęs 95-ąjį procentilį — įprastą pasirinkimą. Paleidus pamačiau `FPR = 0,05000` **lygiai**, ir tada supratau, kad tai ne sutapimas: slenkstis, nustatytas kaip *p*-asis gerybinio srauto procentilis, **pagal apibrėžimą** duoda (100−*p*) % klaidingų teigiamų.

Vadinasi, rinkdamasis 95 iš anksto sutinku su 5 % klaidingų teigiamų — o 1 skyriuje pats suskaičiavau, kad **jau 1 % reiškia ~1000 signalų per parą ir sistema išjungiama**. Numatytasis pakeistas į **99**, kad atitiktų tą patį biudžetą, kuriuo remiasi atrankos kriterijai (klaidingiems teigiamiems skirta 30 % svorio).

#### 27. Išmatuotas slenksčio kompromisas — ir jame yra skardis ⭐⭐⭐

Kadangi slenkstis pasirodė esąs sprendimas, o ne detalė, išmatavau jį per visą rėžį (val aibė, 348 891 ataka / 15 000 gerybinių, autokoderis mokytas iš visų 70 000 mokymo gerybinių):

| Procentilis | FPR | Atakų aptikta | macro-F1 |
|---:|---:|---:|---:|
| 90 | 10 % | **84,9 %** | 0,624 |
| 95 | 5 % | **80,9 %** | 0,596 |
| **99** | **1 %** | **11,8 %** | **0,150** |
| 99,5 | 0,5 % | 5,4 % | 0,093 |
| 99,9 | 0,1 % | 0,3 % | 0,042 |

⭐ **Tarp 95 ir 99 yra skardis:** klaidingiems teigiamiems krentant nuo 5 % iki 1 %, aptikimas griūva nuo 80,9 % iki 11,8 %. Ne laipsniškas pablogėjimas, o lūžis.

**Tai reikšmingiausias šios dienos rezultatas ir jis eina tiesiai į 5 ir 6 skyrius.** Autokoderis **rikiuoja gerai** — ROC-AUC 0,929, PR-AUC 0,995 prieš bazinį 0,959 — bet **negali pateikti naudingo aptikimo lygio to klaidingų teigiamų biudžeto viduje, kurį darbas pats laiko privalomu.** Tai stipresnis teiginys nei „autokoderis silpnesnis už XGBoost“: jis pasako, *kodėl*.

Kreivė išsaugota — `rezultatai/darbiniai/autokoderio_slenkstis.csv`.

#### 28. Maža imtis būtų davusi priešingą išvadą ⚠️⭐

Greita patikra ant 60 000 eilučių (iš jų tik 2 441 gerybinė) rodė PR-AUC **0,944** — **žemiau** bazinio 0,959 lygio, t. y. rikiavimas blogesnis už atsitiktinį. Būčiau užrašęs, kad autokoderio prielaida neveikia.

Pilna mokymo aibė (70 000 gerybinių) apvertė vaizdą: **PR-AUC 0,995**, o atkūrimo paklaidos mediana atakoms 0,376 prieš 0,028 gerybiniam srautui — atakos atkuriamos **blogiau**, kaip ir turi būti.

**Pamoka yra rugsėjo 6 d. taisyklės antra pusė.** Tada užsirašiau, kad mažų duomenų testas tikrina teisingumą, bet ne mastelį. Dabar paaiškėjo ir atvirkščiai: **mažų duomenų testas gali duoti neteisingą dalykinę išvadą.** Ciklo veikimą tikrinti maža imtimi galima; modelio prielaidą — ne.

#### 29. Ankstyvas rikiuotės ženklas atitinka sprendimų matricą

Ant tos pačios 50 000 eilučių patikros imties: **XGBoost 0,692 · Random Forest 0,666 · MLP 0,527**. Sprendimų matricos balai buvo 4,70 · 3,55 · 3,25 — **ta pati tvarka**.

⚠️ Tai 3 % mokymo duomenų ir vienas seed'as, todėl ne rezultatas, o ženklas. Bet jei pilnas paleidimas duotų kitą tvarką, tai būtų vertas dėmesio nesutapimas, ir gerai, kad turiu su kuo lyginti.

#### 30. Atminties riba pasirodė esanti reali

Duomenų paruošimas (parquet → 36 požymiai → normalizavimas) pasiekia **3,53 GB**. Mano pusėje tai riba, ir vienas pilnas autokoderio paleidimas dėl to nutrūko. Pati grandinė greita — 3,8 s — bet atmintis, o ne laikas, yra ribojantis veiksnys.

Įrašyta į paleidimo instrukciją: turint mažiau nei 8 GB, konfigus leisti po vieną.

#### 31. Pirmas paleidimas Windows pusėje — aplinkos spąstai suveikė ⚠️⭐

Patikros paleidimas praėjo, bet su dešimtimis `NumPy 1.x cannot be run in NumPy 2.4.3` įspėjimų. Rezultatas teisingas — **macro-F1 0,6657 prieš mano 0,6659** — bet priežastis verta dėmesio.

**Paleista `(base)`, ne `(iot-ids)`.** Tai tiksliai tas atvejis, kurį `STRUKTURA.md` spąstų lentelėje užsirašiau rugsėjo 3 d., tik pasirodė ne kaip `ModuleNotFoundError`, o kaip numpy versijų konfliktas — todėl iš pirmo žvilgsnio neatpažįstamas.

Klaidos pėdsakas rodo mišrią aplinką: `pandas` imamas iš `%APPDATA%\Python\Python312\site-packages`, o `numexpr` ir `bottleneck` — iš `C:\ProgramData\anaconda3`. Vartotojo lygio paketai uždengia anaconda base paketus, o jie sukompiliuoti su numpy 1.x. **`iot-ids` yra Python 3.11, todėl `Python312` aplankas jos nepasiekia** — aktyvavus aplinką problema dingsta savaime.

⚠️ **Kodėl tai ne kosmetika.** `pandas` tyliai išjungia `numexpr` ir `bottleneck` ir skaičiuoja lėčiau, bet teisingai. Tikroji rizika kita: **rezultatai būtų gauti aplinkoje, kurios `requirements-lock.txt` neaprašo.** Atkartojamumo teiginys ataskaitoje remiasi tuo failu, o `(base)` turi kitas versijas. Kol rezultatai nerašomi į `rezultatai.csv`, nieko neprarasta — patikros režimas kaip tik tam ir skirtas.

**Gera žinia:** dviejų platformų skaičiai sutapo iki trečio skaitmens (0,6657 / 0,6659), nors bibliotekų versijos skiriasi. Grandinė determinuota, o skirtumas — bibliotekų, ne kodo.

#### 32. `requirements-lock.txt` buvo neįkeliamas — UTF-16 ⚠️⭐

Tikrindamas, kokias versijas aprašo lock failas, radau, kad jis yra **UTF-16LE su BOM**. `pip install -r` tokio failo neperskaito.

Priežastis ta pati kaip su `.ps1` failais rugsėjo 1 d.: **PowerShell `>` peradresavimas rašo UTF-16**, ne UTF-8. Rugsėjo 1 d. `pip freeze > requirements-lock.txt` sukūrė failą, kuris atrodo teisingas, atsidaro redaktoriuje ir yra Git'e — bet savo vienintelės funkcijos neatlieka.

**Tai buvo tyli klaida devynias dienas.** Rugsėjo 3 d. dar pažymėjau punktą „`requirements-lock.txt` — jau atlikta 09-01“ kaip uždarytą; failo neatidariau. Penktas tos pačios rūšies atvejis: **byloja failo egzistavimas, ne turinys.**

Failas perrašytas į UTF-8 (79 paketai, turinys nepakeistas). Iš jo matyti, kad `iot-ids` turi tai, ko reikia: numpy 2.4.6, pandas 3.0.5, scikit-learn 1.9.0, xgboost 3.2.0, tensorflow 2.21.0 — t. y. aplinka tvarkinga, tik nebuvo aktyvuota.

**Taisyklė papildyta:** PowerShell'e failus rašyti su `| Out-File -Encoding utf8`, ne `>`.

#### 33. `.bat` paleidikliai — aplinkos klaida paverčiama neįmanoma ⭐

Septyni failai: `patikra.bat`, keturi `mokyti_*.bat` po vieną modeliui, `mokyti_viska.bat` ir bendra dalis `_aplinka.bat`.

**Svarbiausia juose ne patogumas, o `_aplinka.bat`.** Jis daro tris dalykus, kurių rankinis paleidimas nedaro:

1. **Aktyvuoja `iot-ids` ir patikrina, ar tikrai aktyvavo.** Tikrinamas ne `CONDA_DEFAULT_ENV`, o `os.path.basename(sys.prefix)` — tikrasis interpretatoriaus kelias, nes būtent jis lemia, kurie paketai importuojami. Jei aplinka ne ta, skriptas **nutraukia darbą** su paaiškinimu, o ne mokosi toliau.
2. **`PYTHONNOUSERSITE=1`** — išjungia `%APPDATA%\Python\Python312\site-packages`, t. y. pačią šiandieninio numpy konflikto priežastį, o ne jo simptomą.
3. Grąžina darbinį aplanką po aktyvavimo (aktyvavimo skriptai gali jį pakeisti) ir nutildo TensorFlow informacinius pranešimus.

**Mokymas nuoseklus, ne lygiagretus, ir tai ne atsargumas.** Du argumentai: keturi procesai rašytų į tą patį `rezultatai.csv` ir jį sugadintų, o duomenų paruošimas pasiekia ~3,5 GB, tad keturi vienu metu pareikalautų ~14 GB. Įrašyta į failo antraštę, kad po savaitės nekiltų pagunda „pagreitinti“.

**Ta pati ASCII taisyklė kaip `build.ps1`.** Failai gryname ASCII be lietuviškų raidžių ir su CRLF: cmd.exe lange lietuviškos raidės virsta šiukšlėmis, o LF eilutės laužo daugiaeiles `if`/`for` konstrukcijas. `.gitattributes` papildytas `*.bat text eol=crlf` — kitaip Git jas normalizuotų į LF ir failai suluoštų.

Patikrinta automatiškai: ASCII, CRLF, BOM nėra, kiekvienas `goto` turi atitinkamą etiketę.

⚠️ **Ko patikra nepadengia:** pačios `cmd.exe` semantikos — Linux pusėje jos paleisti negaliu. Pirmas tikras bandymas bus `patikra.bat`.

### T7 — visi 12 paleidimų atlikti ✅

| Modelis | macro-F1 | Tikslumas | PR-AUC | FPR | Mokymas | Delsa | Dydis |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Random Forest** | **0,721** ± 0,001 | 0,840 | 0,760 | **32,2 %** | 127 s | 7,20 µs | **558,5 MB** |
| XGBoost | 0,684 ± 0,000 | 0,810 | **0,784** | 21,4 % | 203 s | 6,04 µs | 7,78 MB |
| MLP | 0,617 ± 0,006 | 0,743 | 0,719 | 29,9 % | 50 s | 3,09 µs | 0,18 MB |
| Autokoderis | 0,220 ± 0,044 | 0,240 | **0,996** | **1,0 %** | 5 s | 3,81 µs | 0,06 MB |

### Ką radau

#### 34. Random Forest aplenkė XGBoost — ir tai tikras skirtumas ⭐⭐

macro-F1 **0,721 prieš 0,684**. Skirtumas 0,0375 yra **75 kartus didesnis už paleidimų sklaidą** (0,0005), tad pagal `dietterich1998tests` taisyklę jis tikras, o ne triukšmas.

**Tai apverčia dvi ankstesnes prognozes.** Sprendimų matrica davė XGBoost 4,70, o Random Forest 3,55; rugsėjo 7 d. patikra ant 50 000 eilučių rodė XGBoost 0,692 prieš RF 0,666 — ta pačia kryptimi kaip matrica. **Pilna aibė apvertė ženklą.**

Bet vienareikšmio nugalėtojo nėra, ir tai svarbiau už rikiuotę:

| Kriterijus | Laimi |
|---|---|
| macro-F1 | **Random Forest** (0,721 prieš 0,684) |
| PR-AUC ir ROC-AUC | **XGBoost** (0,784 / 0,983) |
| Klaidingi teigiami | **XGBoost** (21,4 % prieš 32,2 %) |
| Modelio dydis | **XGBoost** — 7,78 MB prieš **558,5 MB**, t. y. **72 kartus** |

XGBoost geriau **rikiuoja** (aukštesni AUC), Random Forest geriau **sprendžia** prie argmax. Tai skirtingi dalykai, ir 6 skyriuje juos reikia pasakyti atskirai.

⚠️ **Sprendimų matrica per dosniai įvertino RF resursus** (4 iš 5). 558 MB kraštiniame šliuze yra ne „šiek tiek daugiau“, o diskvalifikuojantis dydis. Priežastis mano konfigūracijoje: `max_depth: null`.

#### 35. Klaidingi teigiami — 21–32 kartus virš biudžeto ⚠️⚠️⚠️

**Tai rimčiausias radinys ir jis blokuoja išvadas.** 1 skyriuje suskaičiuota, kad 1 % klaidingų teigiamų reiškia ~1000 signalų per parą ir sistema išjungiama. Gauta:

| Modelis | FPR | Virš biudžeto |
|---|---:|---:|
| Random Forest | 32,2 % | **32×** |
| MLP | 29,9 % | 30× |
| XGBoost | 21,4 % | 21× |
| Autokoderis | 1,0 % | **telpa** (pagal konstrukciją) |

Trys prižiūrimi modeliai eksploatacijai netinka nė vienas. **Klaidingiems teigiamiems atrankoje skirta 30 % svorio — tiek pat, kiek aptikimo kokybei**, tad tai ne šalutinis rodiklis.

**Darbinė hipotezė — klasių svoriai.** `Web` gauna svorį 12,79, `BruteForce` 24,22, o `Benign` tik 3,03. Vadinasi, gerybinis srautas *santykinai* nusvertas 4–8 kartus: kai eilutė dviprasmiška, modeliui pigiau spėti retą ataką. Balansavimas, keliantis macro-F1, tuo pačiu griauna FPR.

**Hipotezė tikrinama abliacija** — tie patys modeliai be `class_weight`. Kaina ~17 min.

#### 36. Klaidingi teigiami turi vardą, ir jis buvo numatytas 1 užduotyje ⭐⭐⭐

Pažiūrėjus, į ką virsta 15 000 val gerybinių eilučių:

| Kur nukeliauja | Random Forest | XGBoost |
|---|---:|---:|
| Lieka `Benign` | 67,9 % | 78,8 % |
| → **`Recon`** | **28,0 %** | 9,3 % |
| → `Spoofing` | 3,2 % | 1,9 % |
| → `Web` / `BruteForce` | 0,9 % | 10,0 % |

**Beveik visi Random Forest klaidingi teigiami yra viena pora: gerybinis srautas ↔ žvalgyba.**

⭐ **Ir būtent tai buvo užrašyta rugsėjo 3 d.** `01_atakos.tex` eilutėje apie žvalgybą: *„Srauto kryptis, trukmė ir unikalių taikinių skaičius **nefiksuojami**“* — tai viena iš keturių atakų, kurioms 39 požymių leidimas neturi skiriamųjų požymių.

**Prognozė iš 1 užduoties pasitvirtino matavimu 5 užduotyje.** Duomenų apribojimas, įvardytas teorinėje dalyje, pasirodė kaip konkretus, išmatuojamas klaidų šablonas. Tai stipriausias darbo rezultatas: jis susieja 1 skyrių su 5-uoju ir parodo, kad teorinė dalis nebuvo dekoracija.

#### 37. Tikslumas 0,84 prieš literatūros 99,5 % — dublikatų argumentas įrodytas savo skaičiais ⭐⭐

`almahaqeri2026gradient` ant to paties CICIoT2023 skelbia 99,59 % tikslumą 8 kategorijoms. Mūsų geriausias — **0,840**.

Skirtumas **15,6 procentinio punkto**, ir pagrindinis kandidatas į priežastis yra tas pats, kurį išmatavau rugsėjo 6 d.: **pašalinti 53,3 % tikslių dublikatų.** Pašalinus pasikartojančias eilutes dingsta būtent tie pavyzdžiai, kuriuos modelis gali įsiminti.

⚠️ **Sąžiningos išlygos:** skiriasi ir požymių aibė (39 prieš 46), ir imtis. Todėl teigti galima tiek: *skirtumas yra tos pačios eilės, kaip ir pašalintų dublikatų dalis*, o ne kad jis vien jais paaiškinamas.

**Teorinė riba (99,78 %) nėra ribojanti** — nuo jos esame 15 punktų atstumu. Sunkumas tikras, ne artefaktas.

#### 38. Retos klasės ir yra macro-F1 stabdis

Random Forest per klases (atkūrimas / tikslumas):

| Kategorija | Atkūrimas | Tikslumas |
|---|---:|---:|
| Mirai | 99,8 % | 99,8 % |
| Spoofing · Recon | 86,9 % | 92,8 / 83,4 % |
| DoS · DDoS | 85,2 / 80,8 % | 60,9 / 93,9 % |
| `Benign` | 67,9 % | 58,7 % |
| **BruteForce** | **33,9 %** | 66,3 % |
| **Web** | **26,9 %** | 57,1 % |

`Web` ir `BruteForce` — mažiausios kategorijos (23 707 ir 12 520 eilučių) ir prasčiausiai atpažįstamos. Būtent jos nutempia macro vidurkį, kaip ir numatyta rugsėjo 2 d. aiškinant `almahaqeri2026gradient` 0,8903.

Antra pastaba: `Benign` tikslumas **58,7 %** — kas antra „gerybine“ pavadinta eilutė iš tikrųjų yra ataka. Problema abipusė, ne tik klaidingi teigiami.

#### 39. Delsos argumentas pasitvirtino su didele atsarga

3,09–7,20 µs vienam įrašui prieš 20–50 ms šliuzo biudžetą — **2 800–6 500 kartų atsargos**. 2 skyriaus teiginys, kad lentelinių modelių delsa nėra ribojantis veiksnys, patvirtintas savo matavimais, o ne vien literatūra.

Autokoderis atkartojo rugsėjo 7 d. slenksčio kreivę tiksliai: FPR lygiai 1,0 % ir macro-F1 0,220 (kreivė prognozavo 0,150 ties 11,8 % aptikimo). PR-AUC **0,996** prieš bazinį 0,959 — rikiuoja gerai, sprendžia blogai. Tas pats skardis, tik dabar pilnoje aibėje.

#### 40. Sprendimo slenkstis išsprendžia FPR problemą be permokymo ⭐⭐⭐

Prieš darant abliaciją paaiškėjo, kad klasių svoriai net nėra pagrindinis svertas. Prižiūrimi modeliai grąžina tikimybes, todėl **operacinį tašką galima rinktis po mokymo** — lygiai kaip autokoderiui.

Taisyklė: ataka skelbiama tik jei bendra atakų tikimybė viršija slenkstį *τ*; kitu atveju — `Benign`. XGBoost (seed 42, val aibė, **modelis nepermokytas**):

| *τ* | FPR | Atakų aptikta | macro-F1 |
|---:|---:|---:|---:|
| argmax *(dabartinis)* | 21,35 % | — | 0,684 |
| 0,90 | 4,86 % | 92,1 % | 0,664 |
| **0,99** | **0,17 %** | **86,0 %** | **0,620** |
| 0,999 | 0,01 % | 84,1 % | 0,574 |

⭐ **Ties *τ* = 0,99 klaidingi teigiami krenta 125 kartus (21,35 % → 0,17 %), o macro-F1 — tik 9 % (0,684 → 0,620).** Aptikimas lieka 86 %. Operacinis biudžetas iš 21 karto viršyto tampa 6 kartus atsargesnis už reikalaujamą.

**Tai keičia ir 6 skyriaus palyginimą.** Iki šiol modeliai lyginti prie argmax, kur jų FPR skiriasi 21–32 %. Palyginimas **prie vienodo FPR** yra vienintelis teisingas: autokoderis prie 1 % FPR aptinka 11,8 % atakų, XGBoost prie **0,17 %** — 86 %. Skirtumas ne laipsniškas, o kategoriškas, ir be slenksčio kreivės jis nebuvo matomas.

⚠️ **Metodinė pastaba:** slenkstis renkamas ant `val`, kaip ir autokoderio (protokolo 21 punktas). Tai ne protokolo pažeidimas, o to paties principo išplėtimas visiems modeliams — bet jį reikia įvardyti kaip sprendimo taisyklės dalį, ne kaip rezultatų gražinimą.

Kreivė: `rezultatai/darbiniai/xgboost_slenkstis.csv`.

#### 41. Gerybinio srauto turime 10,5 karto daugiau, nei panaudojome ⭐

`BENIGN` klasėje yra **1 047 308** unikalios eilutės, o imtyje — 100 000, nes suveikė riba. Tuo tarpu FPR ir `Benign` tikslumas (58,7 %) yra pagrindinės problemos.

**Tai vienintelė klasė, kuriai daugiau duomenų iš tikrųjų padėtų.** Potvynio klasėse taip pat liko po 1–1,9 mln. eilučių, bet jų pridėjimas tik didintų disbalansą ir neliestų nė vieno klaidų šaltinio. Ribos kėlimas **tik gerybiniam srautui** yra asimetriškas ir tiksliai nukreiptas.

⚠️ Tai **protokolo 1 punkto keitimas**, todėl daromas tik įvardijus priežastį ataskaitoje, o ne tyliai.

#### 42. Random Forest netelpa į atmintį — 558 MB buvo per švelnus skaičius ⚠️⭐

Rašant slenksčio modulį procesas nutrūko be pranešimo. Priežastis pasirodė svarbesnė už patį modulį: **`joblib.load` vien Random Forest modeliui nužudomas 3,9 GB mašinoje** (išėjimo kodas 137), net kai daugiau nieko neįkelta.

558 MB yra dydis **diske ir suspaustas** (`joblib compress=3`). Atmintyje modelis kelis kartus didesnis — daugiau nei 3,9 GB.

**Tai keičia resursų vertinimą kokybiškai, ne kiekybiškai.** Sprendimų matricoje Random Forest gavo 4 iš 5 už resursus, o kraštinio šliuzo klasės įrenginiai turi 1–8 GB. Modelis, kuriam vien įkelti reikia daugiau nei 4 GB, ten netelpa iš principo — tai ne „šiek tiek brangiau“, o diskvalifikacija. Priežastis mano konfigūracijoje: `max_depth: null`.

Iš to seka konkretus reikalavimas derinimui: **modelio dydis fiksuojamas šalia macro-F1 kiekvienam bandymui**, ir įrašyta taisyklė siūlyti mažiausią modelį, atsiliekantį mažiau nei 1 % nuo geriausio.

#### 43. Slenksčio kreivė patvirtinta antruoju matavimu

XGBoost, visa `val` aibė, modelis nepermokytas:

| Taškas | FPR | Atakų aptikta | macro-F1 |
|---|---:|---:|---:|
| argmax | 21,20 % | 97,0 % | 0,684 |
| **τ = 0,975** | **0,67 %** | **87,6 %** | **0,639** |

**FPR sumažėjo 32 kartus, macro-F1 — 6,5 %.** Biudžetas įvykdytas su atsarga, o aptikimas nukrito nuo 97,0 % iki 87,6 %.

⚠️ **Dvi ribos, kurių negalėjau patikrinti savo pusėje:** Random Forest netelpa į atmintį, o MLP `.keras` failas neįsikelia dėl Keras versijų skirtumo (`quantization_config` — failas išsaugotas naujesne versija). Abu turi veikti mašinoje, kurioje modeliai buvo apmokyti.

#### 44. Skalė neišsaugota su modeliu ⚠️

Rašant MLP kelią paaiškėjo, kad `paleisti.py` sukuria `Skale`, bet jos **neišsaugo**. Slenksčio moduliui tai neproblema — `StandardScaler` deterministinis, tad perskaičiuota iš tos pačios mokymo aibės skalė tapati.

Bet **diegimui to nepakanka:** išsaugotas MLP ar autokoderis be skalės yra neveikiantis artefaktas, nes įvesties normalizavimo parametrai prarasti. Tai tiesiogiai liečia 4 užduoties prototipą (T8). Įrašyta kaip taisytinas dalykas.

#### 45. Prie vienodo FPR rikiuotė apsiverčia atgal — ir sprendimų matrica buvo teisi ⭐⭐⭐

Slenksčio kreivės visiems trims prižiūrimiems modeliams (val aibė, modeliai nepermokyti):

| Modelis | argmax FPR | argmax macro-F1 | τ | FPR ties τ | Aptikta | macro-F1 ties τ | Kaina |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random Forest | 32,10 % | **0,7212** | 0,9842 | 0,77 % | 86,3 % | 0,6037 | **−16,3 %** |
| **XGBoost** | 21,20 % | 0,6835 | 0,9749 | 0,67 % | **87,6 %** | **0,6390** | **−6,5 %** |
| MLP | 29,13 % | 0,6096 | 0,9602 | 0,86 % | 83,9 % | 0,5455 | −10,5 % |

⭐ **Ties vienodu FPR nugalėtojas pasikeičia: XGBoost 0,639 prieš Random Forest 0,604.**

Vakar užrašiau, kad RF aplenkė XGBoost (0,721 prieš 0,684) ir kad tai apverčia sprendimų matricą. **Tai buvo argmax taško artefaktas.** RF pranašumas egzistavo tik prie 32 % klaidingų teigiamų, t. y. taške, kurio darbas pats nepriima. Įvedus reikalaujamą biudžetą, RF praranda 16,3 %, o XGBoost — 6,5 %.

**Mechanizmas paaiškinamas.** Random Forest tikimybė yra 100 medžių balsų dalis, tad ties 1,0 ji šokinėja žingsniu 0,01 — skiriamoji geba ten, kur jos labiausiai reikia, yra grubi. XGBoost grąžina tolydžias tikimybes, todėl aukštą slenkstį pasiekia tiksliau.

**Iš to seka trys dalykai:**

1. **Sprendimų matrica buvo teisi.** Ji davė XGBoost 4,70, RF 3,55; matavimas prie teisingo operacinio taško tai patvirtina. Vakarykštis „matrica apversta" atšaukiamas.
2. **XGBoost laimi pagal visus kriterijus vienu metu** — macro-F1 (0,639), PR-AUC, ROC-AUC, klaidingus teigiamus ir dydį (7,78 MB prieš 558 MB). Kompromiso nebėra.
3. **Palyginimas prie argmax yra metodinė klaida**, o ne smulkmena: jis pakeitė rikiuotę. 6 skyriuje modeliai lyginami **tik** prie suderinto FPR.

> **Pamoka.** Vakar iš skirtumo, 75 kartus viršijančio sklaidą, padariau išvadą apie metodų rikiuotę. Skirtumas buvo tikras — bet matavau ne tą tašką. **Statistinis reikšmingumas nieko nesako apie tai, ar matuojamas dydis yra tas, kurio reikia.**

#### 46. `rezultatai.csv` turėjo 24 eilutes vietoj 12 ⚠️

Paleidus `mokyti_viska.bat` antrą kartą kiekvienas paleidimas įsirašė dukart: `metrikos.prideti` prirašinėjo be jokios patikros.

Kokybės metrikoms tai nekenktų — jos tapačios — bet išnaša „vidurkis ± std iš **3** paleidimų" būtų melas, o laiko rodiklių sklaida skaičiuojama iš 6 matavimų po du tam pačiam seed'ui.

**Pataisyta: eilutė su tuo pačiu `(modelis, formuluotė, seed, konfigas)` dabar perrašoma**, tad failas idempotentiškas ir bet kada saugiai regeneruojamas.

⭐ **Šalutinis rezultatas vertingesnis už pačią klaidą.** Du nepriklausomi pilni paleidimai davė kokybės metrikas, sutampančias iki **1·10⁻⁵**. Skiriasi tik laiko rodikliai (mokymas iki 15 s, delsa iki 2,2 µs) — kaip ir turi būti. **Atkartojamumas patvirtintas matavimu**, ne prielaida apie fiksuotus seed'us.

#### 47. GPU padeda tik XGBoost

Turima RTX 4060. Patikrinta:

| Biblioteka | GPU | Pastaba |
|---|---|---|
| XGBoost 3.2 | ✅ | `device: cuda`; įrašyta į konfigą |
| TensorFlow 2.21 | ❌ | **Native Windows GPU nepalaiko nuo TF 2.11** — reikėtų WSL2 |

Antrasis apribojimas ne mūsų pasirinkimas — jį praneša pats TensorFlow. Praktinė pasekmė: derinimas pagreitės tik XGBoost, o MLP ir autokoderis lieka CPU. Jiems tai ne bėda — MLP mokosi 50 s.

`gradientinis.py` GPU nebuvimą tikrina ir **tyliai grįžta į CPU, bet apie tai praneša**: tas pats konfigas veikia abiejose mašinose, o dešimteriopai lėtesnis mokymas nelieka nepaaiškintas.

#### 48. Derinimas atliktas — XGBoost gauna daugiausia ⭐⭐

Po 20 bandymų kiekvienam modeliui (400 000 eilučių imtis):

| Modelis | Numatytoji *(pilna aibė)* | Geriausia paieškoje *(400 k)* | Dydis |
|---|---:|---:|---|
| Random Forest | 0,7213 · 558 MB | 0,7117 | **196 MB** |
| **XGBoost** | 0,6838 · 7,78 MB | **0,7137** | 27,8 MB |
| MLP | 0,6165 · 0,18 MB | 0,6274 | 0,52 MB |

⚠️ **Skaičiai tiesiogiai nepalyginami:** paieška vyko ant 400 000 eilučių, o numatytosios reikšmės išmatuotos ant 1,7 mln. Palyginimas galioja **tarp konfigūracijų paieškoje**, ne tarp stulpelių. Tikrąjį atsakymą duos permokymas ant visos aibės.

**Bet vienas dalykas iškalbingas jau dabar.** XGBoost su 400 000 eilučių ir suderintais parametrais (0,7137) lenkia save patį su 1,7 mln. eilučių ir numatytosiomis (0,6838). **Derinimas čia davė daugiau nei keturgubas duomenų kiekis** — tai atskiras pastebėjimas, vertas 4 skyriaus.

**Random Forest laimėjimas ne kokybėje, o dydyje: 196 MB vietoj 558 MB** prie beveik tos pačios macro-F1. `max_depth=30` ir `max_features=0.3` išsprendžia tai, ką vakar radau kaip diskvalifikuojantį apribojimą.

**XGBoost pasirinktas didesnis variantas** (800 medžių, 27,8 MB), o ne mažiausias per 1 % (200 medžių, 7,40 MB, macro-F1 0,7074): 27,8 MB telpa į šliuzo biudžetą be išlygų, o 0,9 % kokybės ten svarbiau nei 20 MB.

**Suderinti konfigai sukurti ATSKIRAIS failais** (`*_derintas.yaml`). Perrašius senuosius, `rezultatai.csv` idempotentiškas įrašymas pakeistų bazines eilutes ta pačia rakto pora — ir palyginimas „prieš/po“, kurio reikia ataskaitai, dingtų.

#### 49. Suderintas Random Forest lėtesnis ~3,7 karto — ir be eigos to nebuvo kaip suprasti ⭐

Permokymas atrodė užkibęs. Priežastis paprasta ir apskaičiuojama iš anksto: suderintas RF turi `max_features=0.3` (11 požymių skaidymui vietoj 6 prie `sqrt`) ir **200 medžių vietoj 100**. Kartu ≈ 3,7 karto daugiau darbo, t. y. ~8 min. vienam seed'ui vietoj 127 s.

**Bet tai išaiškėjo tik suskaičiavus.** Kol procesas nieko nerašė, „lėtas" ir „užkibęs" atrodė vienodai — o tai priverčia arba laukti neribotai, arba nutraukti gerą paleidimą.

**Pridėta eiga trimis lygiais:**

| Lygis | Kas rodoma |
|---|---|
| Visas paleidimas | `>>> PALEIDIMAS 4/9  praejo 12,3 min, liko ~18 min` |
| Random Forest | juosta pagal medžius, 20 žingsnių |
| XGBoost | juosta pagal medžius per `TrainingCallback` |
| MLP · autokoderis | Keras jau spausdina epochas |

⭐ **Random Forest juostai reikėjo mokyti dalimis, ir tai buvo patikrinta prieš darant.** `warm_start` su tuo pačiu `random_state` duoda **tapatų** mišką — skirtumas 2·10⁻¹⁶, t. y. slankiojo kablelio apvalinimas. Tikrinau prieš keisdamas mokymą: eigos juosta, keičianti rezultatus, būtų blogesnė už jos nebuvimą.

**Dvi klaidos, pagautos bandant:**

- **Eigos klasė funkcijos viduje nepasiduoda `pickle`** — modelio išsaugojimas lūžo `PicklingError`. Perkelta į modulio lygį, o `_issaugoti` dabar atsieja iškvietimus: išsaugotam modeliui laikmačiai nereikalingi.
- **`USE_CUDA` sako tik tiek, kad biblioteka sukompiliuota su CUDA** — ne kad GPU yra. Mano patikra būtų tylėjusi ten, kur GPU nėra. XGBoost pats grįžta į CPU su aiškiu pranešimu, tad patikros teiginys patikslintas, o ne sustiprintas.

#### 50. Derinimas pagerino visus tris — ties FPR biudžetu ⭐⭐

| Modelis | Bazinė ties biudžetu | Suderinta ties biudžetu | Pokytis |
|---|---:|---:|---:|
| **XGBoost** | 0,6390 | **0,6578** | +2,9 % |
| Random Forest | 0,6037 | 0,6423 | +6,4 % |
| MLP | 0,5455 | 0,5906 | +8,3 % |

**XGBoost lieka geriausias ties operaciniu tašku** — macro-F1 0,6578, aptinka 88,4 % atakų prie 0,94 % klaidingų teigiamų.

⭐ **Rikiuotės apsivertimas pasikartojo su suderintais modeliais.** Prie argmax pirmauja Random Forest (0,7235 prieš 0,7185), ties biudžetu — XGBoost (0,6578 prieš 0,6423). Tas pats reiškinys, tie patys modeliai, kitos hiperparametrų reikšmės. **Vadinasi, tai ne atsitiktinumas, o savybė**, ir 6 skyriuje ją galima teigti tvirtai.

**GPU davė realų pagreitį:** XGBoost mokymas 215,8 → 105,5 s, nors medžių 800 vietoj 300 ir gylis 10 vietoj 8 — vienam medžiui apie penkis kartus greičiau.

#### 51. Dydis, išmatuotas ant imties, į pilną aibę NEPERSIKELIA ⚠️⚠️

Derinimo paieška Random Forest'ui prognozavo **196 MB**. Permokius ant visos aibės gauta **637,9 MB** — 3,3 karto daugiau, ir **daugiau nei bazinės konfigūracijos 558 MB.**

Priežastis paprasta ir buvo numatoma: paieška ėjo ant 400 000 eilučių, o pilna mokymo aibė yra 1 698 155 — 4,25 karto daugiau. Prie `max_depth=30` medžiai nėra gylio ribojami tiek, kad lapai prisotintų: mazgų skaičius auga beveik tiesiškai su eilučių skaičiumi. Dydis padidėjo 3,3 karto — beveik tiek pat, kiek duomenys.

⚠️ **Vadinasi, Random Forest atminties problema NEIŠSPRĘSTA — ji šiek tiek pablogėjo.** Būtent dėl jos į paiešką ir įdėjau dydžio stulpelį, o tas stulpelis pasirodė neinformatyvus tam tikslui, kuriam buvo skirtas.

**Pamoka konkreti:** ant imties matuojama **kokybė** persikelia neblogai (rikiuotė pasitvirtino), bet **dydis nepersikelia**, nes jis priklauso nuo mokymo aibės dydžio, o ne tik nuo hiperparametrų. Dydį reikia arba matuoti pilnoje aibėje, arba ekstrapoliuoti pagal eilučių santykį.

**Ką iš tikrųjų mažintų:** `min_samples_leaf` (dabar 1). Prie 10 ar 20 mazgų skaičius kristų kartais, o ne procentais. `max_depth` prie 30 nebeveikia kaip riba.

XGBoost dydis irgi paaugo (27,8 → 45,0 MB), bet tik 1,6 karto: medžių skaičius fiksuotas, tad auga tik jų sudėtingumas. 45 MB į šliuzo biudžetą telpa.

#### 52. Apsirikau delsos kryptimi ⚠️

Vakar parašiau, kad GPU→CPU perėjimas išpūs XGBoost delsą. **Išmatuota priešingai: 7,58 → 4,13 µs**, t. y. beveik dvigubai greičiau. Prognozė vyksta GPU, ir tai atperka `DMatrix` sudarymą.

**Bet išvada dėl matavimo lieka ta pati — tik dėl priešingos priežasties.** 4,13 µs yra **per optimistinis** skaičius: jis gautas su GPU, o kraštinis šliuzas GPU neturi — tai buvo 2 skyriaus prielaida. Lyginti jį su Random Forest ir MLP, matuotais CPU, negalima nė viena kryptimi.

Taisymas tas pats: prieš delsos matavimą modelis perjungiamas į CPU. Skirtumas tas, kad tai ne „ištaisyti išpūstą skaičių", o **atsisakyti aparatūros, kurios diegimo vietoje nebus.**

#### 53. T8 — prototipas veikia; du blokuojantys dalykai pakeliui ⚠️

**`src/prototipas.py`** (Streamlit): srautas → požymiai → inferencija → signalas. Modelio pasirinkimas, **slenksčio slankiklis**, srauto atkūrimas paketais, gyvi rodikliai (apdorota langų, signalai, klaidingi teigiami, delsa), signalų grafikas, kategorijų pasiskirstymas ir paskutinių signalų lentelė su žyma, ar signalas teisingas.

**Prototipas naudoja slenkstį, ne argmax.** Prie argmax jis demonstruotų 21–32 % klaidingų teigiamų — t. y. rodytų būtent tai, ką darbas vadina netinkamu eksploatacijai. Numatytasis τ imamas iš `slenkscio_taskai.csv`, tad demonstracija ir vertinimas naudoja **tą patį** sprendimo tašką.

**Naudojama validacijos aibė.** Test aibė lieka neliesta net demonstracijoje.

**Patikra be sąsajos** (XGBoost, 5 000 langų): klaidingi teigiami **0,43 %**, aptikta **89,0 %** atakų — atitinka viso `val` skaičius (0,94 % / 88,4 %; skirtumą duoda 232 gerybinės eilutės imtyje).

⚠️ **Blokuojantis dalykas 1: modelių failų vardai neturėjo konfigo.** `zyma` buvo `<modelis>_<formuluotė>_seed<N>`, todėl `mokyti_derintus.bat` **užrašė bazinius modelius** tais pačiais failais. Patikrinau metaduomenis: visi išsaugoti modeliai yra suderintieji, bazinių nebeliko.

Praktinės žalos ataskaitai nėra — bazinių modelių metrikos yra `rezultatai.csv`, o jų pačių niekam nebereikia. Bet **slenksčio kreivės, kurias vakar laikiau bazinėmis, iš tikrųjų buvo skaičiuotos jau ant suderintų modelių** — tai paaiškina, kodėl skaičiai sutapo su „po derinimo" verte. Vardas dabar turi konfigo kamieną, o esami failai pervadinti.

⚠️ **Blokuojantis dalykas 2: skalė nebuvo saugoma.** Užrašiau tai rugsėjo 7 d. kaip taisytiną; prototipui tai tapo blokuojančiu. `paleisti.py` dabar išsaugo `.skale.joblib` šalia modelio, o `Skale.ikelti` ją grąžina. **XGBoost ir Random Forest normalizavimo nereikalauja, todėl prototipas veikia jau dabar; MLP pareikalaus permokymo** — jis apie tai praneša aiškia žinute, o ne lūžta.

**Delsa prototipe matuojama CPU** (`set_params(device="cpu")`) — kraštinis šliuzas GPU neturi. Tai ta pati pataisa, kurią numačiau, tik įgyvendinta ten, kur ji labiausiai matoma.

#### 54. „Visada dominuoja DDoS" — tai imties sudarymo pasekmė, ne prototipo yda ⭐

Prototipe, kad ir kokie nustatymai, signalų sąraše vyrauja DDoS. Priežastis matoma iš srauto sudėties:

| Kategorija | `val` langų | Dalis | **Etikečių** |
|---|---:|---:|---:|
| DDoS | 157 500 | **43,3 %** | **12** |
| Recon | 55 691 | 15,3 % | 5 |
| DoS | 55 266 | 15,2 % | 4 |
| Mirai | 45 000 | 12,4 % | 3 |
| Spoofing | 30 000 | 8,2 % | 2 |
| Benign | 15 000 | 4,1 % | 1 |
| Web | 3 556 | 1,0 % | 6 |
| BruteForce | 1 878 | 0,5 % | 1 |

⭐ **Riba 100 000 taikyta ETIKETEI, ne kategorijai.** DDoS turi 12 etikečių, tad gauna iki 1,2 mln. vietų, o `BruteForce` — viena etiketė ir 1 878 eilutės. Kategorijų disbalansas imtyje **84:1** yra tiesioginė to pasekmė.

**Tai nebuvo klaida** — protokolo 1 punktas ribą apibrėžė etiketei sąmoningai, kad retos etiketės nedingtų. Bet pasekmė kategorijų lygmeniu iki šiol niekur nebuvo užrašyta, nors būtent ji paaiškina, kodėl `Web` (6 etiketės, bet tik 3 556 eilutės) atpažįstamas prasčiausiai.

**Prototipe pridėti du dalykai, kurie tai paverčia informacija:**

1. **Srauto sudėties pasirinkimas** — natūrali (kaip rinkinyje) arba tolygi (po lygiai iš kategorijos). Tolygi skirta **tik demonstracijai** ir pažymėta įspėjimu: metrikos joje nereprezentatyvios. Patikrinta: natūralioje DDoS 44,3 %, tolygioje visos po 12,5 %.
2. **Aptikimo lentelė pagal kategorijas** — kiek langų sraute, kiek signalų, kokia aptikimo dalis, rikiuojant prasčiausiai atpažįstamas viršuje. Iki šiol prototipas rodė bendrą „aptikta 89 %", kuris slėpė tikrąją istoriją: Mirai 99,8 %, o `Web` 26,9 %.

#### 55. Įkalti failų vardai lūžo dviejose vietose atskirai ⚠️

Pervadinus modelius (`<konfigas>_<formuluotė>_seed<N>`) lūžo **ir** prototipas, **ir** `slenkstis.py` — abu turėjo vardus įkaltus, ir kiekvieną teko taisyti atskirai. Pirmą pataisiau nepastebėjęs antrojo.

**Paieška perkelta į vieną vietą** — `bazinis.rasti_issaugotus()`. Ji skenuoja aplanką ir apie kiekvieną modelį pasako: žymą, tipą, konfigą, variantą (bazinis / suderintas), ar reikia normalizavimo ir ar skalė išsaugota. Prototipas pagal tai atrenka tik veikiančius, `slenkstis.py` — visus prižiūrimus.

**Šalutinė nauda:** dabar randami ir baziniai, ir suderinti modeliai, tad slenksčio lentelė gauna abu variantus, o palyginimas „prieš/po" atsiranda savaime, be atskiro darbo.

**Pamoka paprasta ir sena:** dubliuotas sąrašas yra du sąrašai, kurie anksčiau ar vėliau išsiskiria. Vardų šaltinis turi būti vienas — geriausia pati failų sistema.

#### 56. Delsa permatuota CPU — XGBoost skirtumas 6,5 karto ⭐

| Modelis | Delsa, µs | Dydis, MB |
|---|---:|---:|
| Autokoderis | 2,78 | 0,06 |
| MLP (suderintas) | 3,00 | 0,52 |
| Random Forest (suderintas) | 10,91 | 637,9 |
| **XGBoost (suderintas)** | **27,42** *(buvo 4,2 su GPU)* | 45,0 |

Suderinto XGBoost delsa CPU **6,5 karto didesnė** nei matuota GPU. Visi keturi vis tiek telpa į 20–50 ms šliuzo biudžetą su trijų eilių atsarga, bet dabar skaičiai palyginami tarpusavyje ir atitinka diegimo aplinką.

⚠️ **Permatuodamas savo pusėje vos neįvedžiau naujo nesulyginamumo:** įrašiau VM išmatuotas reikšmes į `rezultatai.csv`, kur kitos eilutės matuotos kita mašina. Failą atstačiau iš Git, o į modulio dokumentaciją įrašiau taisyklę — **visi modeliai matuojami vienu paleidimu, vienoje mašinoje**. Ta pati nesulyginamumo yda, kurią taisiau, tik kitu pavidalu.

#### 57. T9 — 4 skyrius parašytas ✅

`04_sprendimas.tex`: 7 poskyriai, ~4,1 psl. teksto plius trys lentelės ir paveikslas.

**Pirmas paveikslas visame darbe** — `paveikslai/architektura.pdf`, generuojamas (`src/eksperimentai/paveikslai.py`), ne pieštas. Jame svarbiausia ne grandinė, o **mokymo atskyrimas nuo diegimo**: į šliuzą keliauja tik du artefaktai — apmokytas modelis ir slenkstis, o slenkstis ateina iš validacijos aibės. Sistema, kalibruojanti save pagal stebimą srautą, prisitaikytų prie atakos, jei ši truktų pakankamai ilgai.

**Nauja generuojama lentelė** `tab:imtis` (`src/eksperimentai/lenteles.py`) — kategorijos, etikečių skaičius, dublikatų dalis, unikalios eilutės ir imtis. Ji vienu žvilgsniu paaiškina tai, ką iki šiol reikėdavo aiškinti tekstu: DDoS turi 12 etikečių ir 62 % dublikatų, `BruteForce` — vieną etiketę ir 0 %.

⚠️ **Generuojamos lentelės `\label` neturi** — jį duoda skyrius, apgaubdamas `table` aplinka. Pastebėjau tikrindamas nuorodas, ne po kompiliavimo. Visos trys naudoja `tabularx`, todėl `table` float'e leistinos (`xltabular` ten negalima — 1 skyriaus spąstai).

**Skyriuje sąmoningai nėra proceso pasakojimo** — nei apie tai, kaip prie sprendimų priėjau, nei apie klaidas. Yra tik kas išmatuota, kas pasirinkta ir kokia to pasekmė. Rugsėjo 3 d. vadovo pastaba pritaikyta iš karto, o ne po redagavimo.

### Ką darysiu toliau

**Kompiliavimas** (`build.ps1`) — paveikslas ir trys lentelės Windows pusėje dar nebandyti. Po to 4 užduotis uždaryta; lieka 5 ir 6. Prieš 5 užduotį lieka trys taisymai: delsa CPU ir `paleisti.py` (prototipe jau padaryta) · `class_weight` aiškiu žodynu · Random Forest dydis per `min_samples_leaf`. Tada 4 skyrius turės ir bazinius, ir suderintus rezultatus prie suderinto FPR. Derinimas yra protokolo 18 punkto vykdymas, iki šiol neatliktas; paieška vyksta ant 400 000 eilučių imties, kad tilptų į 30 min. biudžetą, o geriausia konfigūracija permokoma ant visos aibės.

Pirmas žingsnis — **`bazinis.py` kontraktas, prieš pirmą modelį**. Nuo jo priklauso, ar 6 užduotis bus vienas ciklas. Autokoderio išlyga (`priziurimas = False`, `predict_proba` kaip anomalijos įvertis) turi būti kontrakte iš karto.

⚠️ **Nepamiršti:** `src/modeliai/cnn.py` ištrinti, `xgboost.py` **nekurti** — failas tokiu vardu uždengtų biblioteką; vardas `gradientinis.py`.

---

## Rugsėjo 8 d. (antradienis), vakare — 5 užduoties planas

### Ką padariau

**Sudarytas 5 užduoties tikslų planas** (`claude/uzduotis_05_planas.md`): tikslai T0–T9, vertinimo protokolas (12 punktų), nematytų klasių testo taisyklės, patikimumo patikros, dienos biudžetas rugsėjo 9 d., priėmimo kriterijai, rizikos.

**Prieš rašant peržiūrėta ne būklės žymos, o pati repozitorija** — `rezultatai/apmokyti/`, `rezultatai.csv`, `metrikos.py`, `paleisti.py`, `slenkstis.py`. Peržiūros rezultatas pasirodė svarbesnis už patį planą.

### Priimti sprendimai

- **5 užduotis vykdoma rugsėjo 9 d.**, ne 15–16 d. Grafikas eina **6 dienomis į priekį**.
- ⭐ **`test` aibė liečiama vienu prėjimu.** Visi sprendimai (τ, modeliai, pjūviai, lentelės, paveikslai) priimami ant `val` **prieš**; `test` duoda vieną rezultatų failą, iš kurio generuojama visa kita. Priežastis ta pati kaip 3 užduoties dviejų pakopų filtro: keturi atskiri „paleidimai ir pažiūrėjimai“ reikštų, kad kiekvienas paskesnis pjūvis pasirinktas jau matant ankstesnį rezultatą. Nutekėjimo formaliai nebūtų, **atrankos nutekėjimas būtų**.
- **Nematytų klasių testas vertinamas dvejetainiu klausimu**, ne macro-F1 — žr. „Ką radau“, 2 punktas.
- **Autokoderis nematytų klasių testui nepermokomas.** Jis mokomas tik iš `BENIGN`, todėl visos 33 atakų klasės jam ir taip nematytos; permokymas be `DDOS-SLOWLORIS` duotų tą patį modelį. Jo skaičius imamas iš bazinio `test` paleidimo per-klasę aptikimo dalies.
- **Nematytų klasių testo kaina — 3 permokymai, ne 6.** Tik geriausias prižiūrimas modelis, vienas seed'as.
- **Rezultato interpretacija užrašoma iš anksto abiem atvejais** (`test` ≈ `val` ir `test` ≠ `val`) — ta pati taisyklė kaip 3 užduoties jautrumo analizėje.
- **`test` FPR atitikimo patikra yra vienintelė, kurios rezultato nežinau iš anksto**, todėl ji vertingiausia iš penkių.

### Ką radau

#### 58. `test` paleidimas būtų tyliai sunaikinęs visus `val` rezultatus ⚠️⚠️⚠️

`metrikos.py`:

```
SCHEMA = [modelis, formuluote, seed, macro_f1, ..., konfig, data]
RAKTAS = [modelis, formuluote, seed, konfig]
```

Vertinimo aibės **nėra nei schemoje, nei rakte**. `prideti()` eilutę su tuo pačiu raktu perrašo — tai buvo teisingas rugsėjo 7 d. sprendimas prieš dublikatus (24 eilutės vietoj 12). Bet paleidus `--vertinimas test` su tuo pačiu konfigu ir seed'u **`test` eilutė užimtų `val` eilutės vietą**, ir visi 21 turimas `val` rezultatas dingtų.

**Blogiausia, kad tyliai.** Klaidos nebūtų, failas liktų tvarkingas, o `rezultatai.tex` rodytų `test` skaičius po išnaša apie `val`. Tai **šeštas** tos pačios rūšies atvejis darbe: dalykas, kurio supainiojimas nepasirodo kaip klaida.

**Ta pati problema mažesniu mastu:** `sumaisymas_{zyma}.csv` vardas irgi neturi aibės, tad `test` matricos perrašytų `val`. Lygiai tai, kas rugsėjo 8 d. atsitiko su modelių vardais, kai `mokyti_derintus.bat` užrašė bazinius modelius — tik dabar pagauta **prieš**, ne po.

#### 59. `--vertinimas test` permoko modelius, o ne tik vertina ⚠️

`paleisti()` visada kviečia `fit()` ir `issaugoti()`. Vadinasi, 12 „vertinimo“ paleidimų yra 12 permokymų: vien suderintas Random Forest (~8 min. vienam seed'ui) suvalgytų ~25 min., o modelių failai būtų be reikalo perrašyti.

`bazinis.rasti_issaugotus()` jau egzistuoja nuo rugsėjo 8 d. ryto — reikia tik `--tik-vertinti` veliavos. **Funkcija, parašyta kitam tikslui, sutaupys pusvalandį rytoj.**

#### 60. `slenkstis.py` `test` aibės neatidaro iš viso

Kode `idx["val"]` įkalta, o dokumentacijoje parašyta „test aibė čia neatidaroma“. Tai buvo **sąmoningas ir teisingas** 4 užduoties sprendimas. 5 užduočiai reikia režimo, kurio nėra: τ **skaitomas iš `slenkscio_taskai.csv`** ir taikomas `test`, o perskaičiavimo galimybės tame režime neturi būti iš viso — taisyklė, kurios niekas netikrina, yra ketinimas.

#### 61. Trys iš keturių būklės žymų nesutapo su failais ⭐

| Žyma | Tikrovė |
|---|---|
| `uzduotis_04_planas.md`: „Permokymas — **dar nepaleistas**“ | ✅ **Atliktas** rugs. 8 d. 06:07–06:47; `*_derintas_8kat_seed42..44` yra visiems trims |
| Žurnalas: RF suderintas **637,9 MB** | Faile **670 MB**; trys seed'ai ≈ **2 GB** |
| `STRUKTURA.md`: `metadata.json` — metaduomenys Git'e | Failas **tuščias** (`{"modeliai": {}}`); metaduomenys guli kiekvieno modelio `.json` šalia |

**Septintas kartas.** Rugsėjo 6 d. užsirašiau taisyklę „kriterijus, kurio patikra yra viena komanda, žymimas tik po tos komandos“. Šįkart ji pritaikyta **planuojant**, ne po fakto — visas plano 0 skyrius sudarytas iš `ls` ir `grep`, ne iš ankstesnių dokumentų. Kaina — apie 15 min.; nauda — trys blokuojantys dalykai, rasti prieš dieną, kurios negalima pakartoti.

#### 62. `DICTIONARYBRUTEFORCE` pašalinimas ištuština visą kategoriją ⭐⭐

Ji yra **vienintelė savo kategorijos klasė**. Vadinasi, permokytas be jos prižiūrimas modelis 8 kategorijų formuluotėje turės **7 klases**, ir jo macro-F1 su bazinio modelio macro-F1 **nepalyginamas** — vidurkinama per skirtingą klasių skaičių.

Būčiau tai pastebėjęs rugsėjo 9 d. viduryje eksperimento, ir tada rinktis būtų reikėję tarp perdarytos lentelės ir tylaus neteisingo palyginimo.

**Sprendimas: nematytų klasių testas vertinamas dvejetainiu klausimu** — ar pašalintos klasės eilutės pažymimos kaip ataka (bet kuri), ar praleidžiamos, prie to paties FPR biudžeto. macro-F1 ten nenaudojamas nė vienam modeliui.

⭐ **Kartu paaiškėjo, ko lentelėje trūko.** Trys stulpeliai (n · prižiūrimas be klasės · autokoderis) parodo tik tiek, ar klasė aptinkama. **Ketvirtasis — prižiūrimo modelio aptikimo dalis, kai klasė buvo mokyme** — parodo, *kiek kainuoja* jos nematyti. Būtent jis paverčia lentelę atsakymu į 2 skyriaus zero-day klausimą, o ne dar viena metrikų lentele.

### Ką darysiu rytoj (rugs. 9, trečiadienis)

**T0 pirmas ir be išimčių:** `aibe` stulpelis į `SCHEMA` ir `RAKTAS` · `zyma` su aibe · `--tik-vertinti` · `slenkstis --taikyti test`. ⚠️ **Prieš pirmą `test` paleidimą — `git commit` su esamu `rezultatai.csv`**, kad 21 `val` eilutė turėtų atsarginę kopiją, jei taisymas nesuveiktų.

Tik po to protokolo užrakinimas (T1) ir vienintelis prėjimas per `test` (T2).

---

## Rugsėjo 9 d. (trečiadienis) — T0: infrastruktūra `test` vertinimui

### Ką padariau

**Keturi taisymai, be kurių pirmas prėjimas per `test` būtų sunaikinęs `val` rezultatus.** Visi patikrinti paleidimu, ne peržiūra.

| Kas | Kur |
|---|---|
| `aibe` stulpelis į `SCHEMA` ir `RAKTAS`; migracija sename faile | `metrikos.py` |
| Aibė `sumaisymas_*.csv` varde; `--tik-vertinti` veliava | `paleisti.py` |
| `Modelis.ikelti()` + `_ikelti()` visiems keturiems modeliams | `bazinis.py` ir 4 modulai |
| `--taikyti test`: τ **skaitomas iš failo**, ne perrenkamas | `slenkstis.py` |
| `--aibe {val,test}` filtras; aibė įrašoma į lentelės išnašą | `i_latex.py` |
| `rezultatai.csv` migruotas: 21 eilutė gavo `aibe=val` | — |

**Sintetinis testas — 16 patikrų iš 16.** Tikrinama: `aibe` yra abiejose vietose; `eilute()` atmeta nežinomą aibę; senas failas be stulpelio migruojamas; **`test` eilutė neperrašo `val` eilutės**; pakartotinis `test` paleidimas lieka idempotentiškas; `atrinkti_aibe` tuščiai aibei meta klaidą; `mokymo_laikas_s = None` nevirsta nuliu.

### Ką radau

#### 63. Kontrolinis paleidimas patvirtino, kad grėsmė buvo reali, o ne teorinė ⭐⭐⭐

Prieš taisant paleidau **seną** `metrikos.prideti` su `test` eilute ant tikros `rezultatai.csv` kopijos:

```
pries: 21 eilutes
po   : 21 eilutes
XGBoost derintas seed42 macro_f1: buvo 0,71847 -> tapo 0,5
```

**Eilučių skaičius nepakito, klaidos nebuvo, o rezultatas dingo.** Tai ne prognozė ir ne atsargumas — tai išmatuotas faktas ant to paties failo, kuris būtų buvęs naudojamas rytoj.

**Verta atkreipti dėmesį, kad tai buvo teisingo sprendimo pasekmė.** Rugsėjo 7 d. idempotentiškas įrašymas buvo taisymas — jis pašalino 24 eilutes vietoj 12. Bet raktas, apibrėžtas be vertinimo aibės, tą patį mechanizmą pavertė naikinimo įrankiu, kai atsirado antra aibė. **Idempotentiškumas yra tiek pat saugus, kiek tikslus jo raktas.**

#### 64. `--vertinimas test` būtų buvęs 12 permokymų, ne 12 vertinimų

`paleisti()` visada kviečia `fit()` ir `issaugoti()`. Suderintas Random Forest mokosi ~8 min., tad vien jis būtų suvalgęs ~25 min., o modelių failai būtų perrašyti be reikalo.

`--tik-vertinti` įkelia išsaugotą modelį ir **mokymo aibės neatidaro visai**, kai skalė išsaugota — 1,7 mln. × 36 yra ~490 MB, kurių neužimant 670 MB Random Forest turi realią galimybę išsitekti. Mokymo laikas imamas iš metaduomenų; perskaičiuotas jis būtų ne mokymo, o įkėlimo laikas su mokymo laiko etikete.

#### 65. Įkėlimo logika gyveno trijose vietose, ir aš rengiausi pridėti ketvirtą ⭐

`slenkstis.py` ir `prototipas.py` kiekvienas turėjo savo `joblib.load` su modelio tipo šakojimu — būtent tai, dėl ko rugsėjo 8 d. abu lūžo atskirai po failų pervadinimo. Rašydamas `--tik-vertinti` pirmą minutę galvojau nukopijuoti tą patį trečią kartą.

**Vietoj to `_ikelti()` atsidūrė ten pat, kur `_issaugoti()`** — kiekvienoje modelio klasėje, o `Modelis.ikelti()` yra vienintelis įėjimo taškas. Pora, kurios pusės guli skirtinguose failuose, anksčiau ar vėliau išsiskiria.

Šalutinis rezultatas: `gradientinis._ikelti` **įkeldamas grąžina modelį į CPU**. Delsa GPU yra 6,5 karto mažesnė nei CPU, o šliuze GPU nėra — dabar to nebereikia atsiminti kiekvienoje matavimo vietoje atskirai.

#### 66. `i_latex` vidurkina bazinį ir suderintą modelį į vieną eilutę ⚠️⚠️

Rastas tikrinant migruotą CSV. `RAKTAI = ["modelis", "formuluote"]` neapima `konfig`, todėl:

| Lentelėje | Iš tikrųjų |
|---|---|
| XGBoost macro-F1 **0,7012** | vidurkis tarp bazinio 0,6838 ir suderinto 0,7185 — **nė vieno iš jų** |
| „vidurkis iš **3** paleidimų“ | suvidurkintos **6** eilutės; `n_seed` skaičiuoja seed'us, ne eilutes |

**Vadinasi, dabartinė `rezultatai.tex` 4 skyriuje rodo skaičius, kurių neturi nė vienas modelis.** Tai ta pati klasė kaip ir šios dienos pagrindinis radinys: teisingas mechanizmas su per siauru raktu.

**Nepataisiau — tai turinio sprendimas.** Praplėtus `RAKTAI` lentelė gautų po dvi eilutes kiekvienam modeliui, o 4 skyriaus tekstas rašytas prie dabartinės sandaros. Vietoj to `agreguoti()` dabar **garsiai praneša**, kai į vieną grupę patenka kelios konfigūracijos. **5 užduočiai grėsmės nėra**: į `test` eina tik suderinti konfigai (protokolo 3.2 punktas), tad po vieną konfigą modeliui.

#### 67. Lentelės išnaša dabar pati pasako, kuria aibe išmatuota ⭐

`val` ir `test` lentelės skiriasi tik skaičiais, o skaičių niekas neatpažįsta iš atminties. Todėl `i_latex --aibe` įrašo į išnašą „Rezultatai išmatuoti testavimo aibėje“, o `slenkstis --taikyti test` — dar ir tai, kad τ parinktas validacijos aibėje ir čia **netaikomas iš naujo**.

**Tai pigiausia šios dienos apsauga:** dokumentas, kuris pats pasako, iš kur jo skaičiai, negali būti tyliai supainiotas.

### Kas nepavyko

**Failų sistema per `device_bash` neprisijungė** (`no Plan9 drive shares mounted`), todėl kodas taisytas debesies konteineryje ir grąžintas per failų perkėlimą. Praktinė pasekmė viena: **pakeitimai nepatikrinti Windows pusėje su tikrais duomenimis ir modeliais.** Sintetinis testas tikrina logiką, ne integraciją — lygiai kaip rugsėjo 6 d., kai 537 eilučių testas praėjo, o tikras rinkinys parodė OOM.

### Ką darysiu toliau

1. ⚠️ **`git commit` prieš bet ką kitą** — `rezultatai.csv` su `aibe=val` turi turėti atsarginę kopiją.
2. `patikra.bat` ir `python -m src.eksperimentai.i_latex --aibe val` — patvirtinti, kad taisymai veikia su tikrais duomenimis. Laukiama: 21 val eilutė, trys įspėjimai dėl sumaišytų konfigūracijų.
3. Vienas modelis `--vertinimas test --tik-vertinti --seed 42` kaip **integracijos patikra**, ir tik po jos pilnas ciklas: `wc -l rezultatai.csv` prieš ir po turi duoti 21 → 22.
4. Tada T1 — protokolo užrakinimas prieš likusius 11 paleidimų.
