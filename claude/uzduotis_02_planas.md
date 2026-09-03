# 2 UŽDUOTIS — DI ir mašininio mokymosi metodų taikymo galimybės

**Tikslų planas**
**Sudaryta:** 2026 m. rugsėjo 2 d., 09:45 · **Patikslinta:** 11:20 po duomenų patikros
**Vykdymas:** rugsėjo 2 d. (viena diena — suspaustas variantas; pradiniame plane buvo rugs. 4 ir 7 d.)
**Rezultatas:** `ataskaita/skyriai/02_di_metodai.tex` (~5–6 psl.), +6–8 įrašai `ataskaita/saltiniai.bib`, papildytos `literatura/anotacijos.md`

---

## 0. Būklė prieš pradedant

| Dalykas | Būklė | Poveikis šiai užduočiai |
|---|---|---|
| 1 užduotis | ✅ Baigta rugs. 1 d. | Duoda vertinimo rėmą — `tab:reikalavimai` ir `tab:aptikimas` |
| CICIoT2023 antraštė | ✅ **Patikrinta 11:20** | ⚠️ **39 požymiai, ne 46.** Radiniai — `claude/ciciot2023_pozymiai.md`. Keičia 2.7 ir 2.9 turinį |
| `saltiniai.bib` | 11 įrašų | Po šios užduoties turi būti 17–19 |
| 1 skyriaus apimtis | 9 psl. vietoj 4–5 | Sprendimas dėl normos — perkeliamas į rugs. 8 d. |
| Antriniai rinkiniai | ❌ **Atmesti 2026-09-02** | T6 iš plano išimtas; jo vietą užima nutekėjimo gynybos klausimas (6 skyrius) |

> **Kas pasikeitė po 11:20 patikros.** Rizika „veidrodžio stulpeliai skiriasi nuo dokumentacijos" įvyko: pašalinti `flow_duration`, `Srate`, `Drate`, `urg_count`, `Magnitue`, `Radius`, `Covariance`, `Weight`; `Duration` pervadintas į `Time_To_Live`; pridėtas `IGMP`. Papildomai rasta **keturios tikslios funkcinės priklausomybės** (`Variance`=`Std`², `Rate`=1/`IAT`, `Tot size`=`AVG`, `Tot sum`=`AVG`×`Number`), todėl efektyvus požymių skaičius ~35. **Tai ne kliūtis 2 užduočiai, o jos medžiaga** — žr. 4 ir 5 skyrius.

---

## 1. Kodėl ši užduotis svarbi (ne „metodų sąrašas")

Šis skyrius atrodo kaip enciklopedinė apžvalga, bet iš tikrųjų jis yra **3 užduoties įvestis ir 6 užduoties atskaitos taškas**. Konkrečiai:

- Metodų matrica su balais **yra** sprendimų matricos žaliava. Jei 2 skyrius baigsis sąrašu be vertinimo, rugsėjo 8 d. teks tą darbą daryti iš naujo — o tai vienintelė diena, kurios negalima praleisti.
- Susijusių darbų lentelė (šaltinis → rinkinys → metodas → metrika) yra **vienintelis būdas** 6 užduotyje pasakyti, ar mano 0,89 macro-F1 yra geras rezultatas. Be jos savo skaičius lyginsiu su niekuo.
- Praktinių apribojimų analizė (delsa, atmintis) **atmeta dalį metodų dar prieš juos realizuojant.** Tai sutaupo 4 užduoties dienas — pigiau atmesti metodą skaitant straipsnį nei po dviejų dienų mokymo.

Vertinimo kriterijus: *ar iš šio skyriaus rugsėjo 8 d. galima pereiti tiesiai prie balų suvedimo, nieko neskaitant iš naujo.*

**Svarbiausia:** kriterijai **nekuriami iš naujo.** 1 užduoties `tab:reikalavimai` juos jau išvedė iš IoT savybių. 2 skyrius tik pritaiko juos metodams. Tai reikia parašyti aiškiai pirmoje pastraipoje — kitaip atrodys, kad kriterijai parinkti po to, kai jau žinomas norimas atsakymas.

---

## 2. Konkretūs tikslai

| Nr. | Tikslas | Išmatuojamas rezultatas |
|---|---|---|
| **T0** | ~~Patikrinti CICIoT2023 realiame faile~~ | ✅ **Atlikta 11:20.** Neatitikimai rasti ir surašyti; `duomenys/README.md` perrašytas |
| **T1** | ~~Papildyti šaltinių bazę DI metodų darbais~~ | ✅ **Atlikta.** 11 → **18** įrašų; 7 nauji, visi 2025–2026, visi DOI patikrinti per Crossref |
| **T2** | ~~Apžvelgti metodus pagal mokymosi paradigmą~~ | ✅ **Atlikta.** 5 paradigmos, **17 metodų**, 7 citavimai → `rezultatai/darbiniai/metodu_apzvalga.md` |
| **T3** | ~~Įvertinti metodus 1 užduoties kriterijais~~ | ✅ **Atlikta.** `tab:metodai`: **18 eilučių × 8 stulpeliai**, 21 šaltinio žyma, tuščių langelių nėra |
| **T4** | Sudaryti susijusių darbų lentelę | ✅ **Iš esmės atlikta.** **10 eilučių iš 5 šaltinių.** Lieka 1 (`houichi`) — leidėjas blokuoja, reikia universiteto prieigos |
| **T5** | ~~Sugretinti skelbiamą delsą su 1 užduoties biudžetu~~ | ✅ **Atlikta.** 2.6 poskyris + `tab:apribojimai`; sugretinimas su skaičiais ir atviru aparatūros nepalyginamumo įvardijimu |
| ~~T6~~ | ~~Nutekėjimo gynyba be antrinio rinkinio~~ | ❌ **Atsisakyta** — žr. 6 skyrių. Klausimas priklauso 4 ir 6 skyriams, ne 2 |
| **T7** | ~~Suformuluoti kandidatų aibę~~ | ✅ **Atlikta.** Fiksuoti **4 metodai**: Random Forest, XGBoost, MLP, autokoderis. Pagrindinis detalumas — 8 kategorijos |
| **T8** | ~~Anotuoti naujus šaltinius~~ | ✅ **Atlikta.** Skyriai E–H, 7 nauji įrašai; **visi 18 `.bib` raktų turi anotaciją**, spragų nėra |

**Ne šios užduoties tikslai:** galutinė atranka su svoriais (→ 3 užd.), duomenų paruošimas (→ 4 užd.), joks kodas modeliams (→ 4 užd.). Jei kyla noras parašyti `random_forest.py` — tai ženklas, kad skyrius baigtas ir laikas eiti į žurnalą.

---

## 3. Skyriaus `02_di_metodai.tex` struktūra

```
2. DI ir mašininio mokymosi metodų taikymo galimybės
   2.1. Vertinimo rėmas ir apžvalgos ašis                    (~0,5 psl.)
        - kriterijai paveldimi iš tab:reikalavimai, ne kuriami
        - kodėl ašis yra mokymosi paradigma, o ne algoritmų šeima
   2.2. Prižiūrimas mokymasis                                (~1,0 psl.)
        - sprendimų medžiai ir ansambliai (RF, XGBoost, LightGBM)
        - SVM, k-NN, MLP — trumpai, su atmetimo argumentais
   2.3. Neprižiūrimas mokymasis ir anomalijų aptikimas       (~0,75 psl.)
        - Isolation Forest, One-Class SVM, autokoderis
        - kodėl tai vienintelis kelias prie zero-day
   2.4. Gilusis mokymasis                                    (~1,0 psl.)
        - 1D-CNN, LSTM/GRU, Transformer, GNN
        - kritinis klausimas: ar sudėtingumas apsimoka srauto požymiams?
   2.5. Papildomos kryptys: paskirstytas mokymasis ir XAI     (~0,6 psl.)
        --> Lentelė tab:metodai (po 2.5, apima 2.2-2.5)
   2.6. Praktiniai apribojimai IoT aplinkoje                 (~0,9 psl.)
        - resursai, inferencijos delsa, klasių disbalansas, mokymo kaina
        - delsos sugretinimas su 20-50 ms biudžetu [T5 — skiriamasis bruožas]
   2.7. Susiję darbai ir skelbiami rezultatai                (~0,85 psl.)
        --> Lentelė tab:susije + pastraipa apie rezultatų patikimumą
        --> pastraipa apie 39 vs 46 pozymius: kodel palyginimas ribotas
   2.8. Apibendrinimas: kandidatų aibė 3 skyriui             (~0,3 psl.)
```

**Iš viso ~5,8 psl.** *(po 2.8 išbraukimo; buvo 6,2)* — viršutinė plano riba. Tai sąmoningas pasirinkimas: geriau planuoti 6 ir gauti 6, nei planuoti 5 ir gauti 9, kaip nutiko 1 skyriuje.

> **Apimties stabdis.** Jei 15:00 tekstas jau viršija 6 psl., o 2.6–2.9 dar neparašyti — pjaunama 2.2 (SVM/k-NN/MLP suliejami į vieną pastraipą) ir 2.4 (Transformer ir GNN — po vieną sakinį su citavimu). **Poskyriai 2.6–2.9 neliečiami: juose yra visa tai, ko negalima atkurti iš literatūros be papildomo darbo.**

---

## 4. Lentelių specifikacija (stulpeliai fiksuojami dabar, prieš rašant)

**Trys lentelės, ne penkios.** 1 skyriuje penkios lentelės davė 9 psl. Čia riba — trys, iš kurių dvi pagrindinės.

### `tab:metodai` — metodų vertinimo matrica (T3) ⭐

| Stulpelis | Turinys | Pastaba |
|---|---|---|
| Metodas | Pavadinimas + santrumpa | |
| Paradigma | Prižiūrimas / neprižiūrimas / gilusis / paskirstytas | |
| Aptinka nematytas atakas | Taip / Ribotai / Ne | |
| Resursų poreikis | Mažas / vidutinis / didelis — **su mokymo ir inferencijos skirtimi** | |
| Interpretuojamumas | Savaiminis / per XAI / juodoji dėžė | |
| Atsparumas disbalansui | Vertinimas + ar reikia balansavimo | 42:1 santykis — ne teorinis klausimas |
| Šaltinis | `\cite{}` arba **„(aut.)"**, jei tai mano vertinimas | ⭐ žr. taisyklę |

> **Taisyklė šaltinio stulpeliui.** Kiekvienas įvertinimas turi būti arba cituojamas, arba aiškiai pažymėtas kaip mano. Vertinimų lentelė be šio stulpelio yra nuomonė, apsimetanti apžvalga — ir tai pirmas dalykas, kurį pastebi recenzentas. Tas pats principas jau pritaikytas 1 skyriuje (atakų priskyrimas sluoksniams — mano).

**Eilutės (~12):** Random Forest · XGBoost · LightGBM · SVM · k-NN · MLP · Isolation Forest · One-Class SVM · Autokoderis · 1D-CNN · LSTM/GRU · Transformer · GNN · Federated learning *(kaip mokymo schema, ne algoritmas — pažymėti)*

**Formatas:** `tabularx` su `\small`, be `table` float'o, jei netelpa (žr. 1 užduoties `xltabular` pamoką).

### `tab:susije` — susiję darbai ir skelbiami rezultatai (T4) ⭐

| Stulpelis | Turinys |
|---|---|
| Šaltinis | `\cite{}` + metai |
| Duomenų rinkinys | CICIoT2023 / TON\_IoT / Edge-IIoTset / kt. |
| Metodas | |
| Užduotis | Dvejetainė / 8 klasės / 34 klasės — **būtina**, be to metrikos nepalyginamos |
| Skelbiama metrika | Tiksliai kaip straipsnyje (acc / F1 / macro-F1) |
| **Kas kelia abejonių** | 1 frazė ⭐ |

> **Paskutinis stulpelis yra visa lentelės vertė.** Be jo tai citatų sąrašas. Su juo — analizė. Pavyzdžiai, ką ten rašyti: „accuracy dvejetainei užduočiai, macro-F1 34 klasėms − 0,89"; „skaidymas neaprašytas"; „balansavimas taikytas prieš skaidymą".
>
> ⚠️ **Po 11:20 patikros atsiranda dar viena tipinė frazė:** „**46 požymių aibė — nepalyginama**". Kiekvienam CICIoT2023 darbui reikia patikrinti, kiek požymių jis naudojo. Beveik visi naudos 46; mano leidime jų 39, ir tarp trūkstamų yra tokie, kurie publikuotose svarbos grafikuose dažnai atsiduria viršuje (`Magnitue`, `Covariance`, `Weight`). **Tai ne smulkmena lentelės pastaboje — tai pagrindinis 6 skyriaus palyginimo apribojimas**, ir jį pasakyti reikia čia, o ne pabaigoje.

### `tab:apribojimai` — mažoji lentelė 2.6 poskyriui

Diegimo vieta (MCU / šliuzas / debesis) × delsos biudžetas × kurie metodai telpa. **3 eilutės, 4 stulpeliai.** Jei netelpa į pusę puslapio — verčiama tekstu.

---

## 5. Šaltiniai: patikrinti kandidatai

**Metaduomenys patikrinti 2026-09-02 leidėjų puslapiuose.** Skaičiai žemiau — jau ištraukti, todėl `tab:susije` pildoma nebeieškant.

### Privalomi (branduolys)

| Raktas | Šaltinis | DOI | Kam būtent |
|---|---|---|---|
| `almahaqeri2026gradient` | Almahaqeri et al. (2026), *Scientific Reports* 16:16909 | `10.1038/s41598-026-47399-5` | ⭐ **Pagrindinis atskaitos taškas.** 11 metodų ant CICIoT2023 |
| `nassef2026tinyml` | Nassef et al. (2026), *Scientific Reports* 16:18524 | `10.1038/s41598-026-50690-0` | ⭐ **Delsos realybės patikra** — gilusis modelis Raspberry Pi 4 |
| `mazinani2026constrained` | Mazinani, Antonucci, Davoli, Ferrari (2026), *Future Internet* 18(1):34 | `10.3390/fi18010034` | Resursų poreikis mikrovaldiklyje, kvantavimas |
| `eren2026drift` | Eren et al. (2026), *Electronics* 15(11):2307 | `10.3390/electronics15112307` | ⭐ **Antrinio rinkinio pagrindimas** (T6) |
| `mohale2025xai` | Mohale, Obagbuwa (2025), *Frontiers in AI* 8:1526221 | `10.3389/frai.2025.1526221` | Interpretuojamumo kriterijus, SHAP/LIME kaina |

### Ką iš jų imti — konkretūs skaičiai

**`almahaqeri2026gradient` — svarbiausia eilutė `tab:susije`:**

| Užduotis | Metodas | Accuracy | Macro-F1 | Inferencija |
|---|---|---|---|---|
| Dvejetainė | XGBoost | 99,61 % | 0,9952 | 0,355 µs/įrašui |
| Dvejetainė | LightGBM | 99,53 % | 0,9944 | 0,719 µs |
| 8 klasės | XGBoost | 99,59 % | **0,8903** | 1,046 µs |
| 34 klasės | XGBoost | 99,48 % | **0,8876** | 3,528 µs |

> **Tai svarbiausias skaičius visame skyriuje.** Accuracy beveik nekinta (99,6 → 99,5), o macro-F1 krenta nuo 0,995 iki 0,888. Tas pats modelis, tie patys duomenys — skiriasi tik metrika ir užduotis. Tai **empirinis įrodymas** 1 užduoties teiginiui, kad esant 42:1 disbalansui accuracy bevertis, ir tuo pačiu realistiškas mano rezultatų tikslas: **0,85–0,90 macro-F1, ne 0,99.**
>
> Papildomai: požymių atranka 46 → 23 sumažino inferenciją 30–51 %, mokymą 33–40 %.
>
> ⚠️ **Bet tai 46 požymių aibė, ne mano 39.** Todėl šis skaičius **neperkeliamas** kaip mano tikslas — jis cituojamas su išlyga. Užtat jis paaiškina mano paties radinį: jei 46 → 23 beveik nepablogina rezultato, tai todėl, kad **dalis požymių yra tiksliai išvestiniai**. Mano faile tokių rasta keturi (`Variance`=`Std`², `Rate`=1/`IAT`, `Tot size`=`AVG`, `Tot sum`=`AVG`×`Number`) — nepriklausomas to paties reiškinio patvirtinimas. **Šį sugretinimą verta parašyti 2.7 poskyryje: jis yra mano, ne perpasakotas.**

**`nassef2026tinyml` — argumentas prieš gilųjį modelį šliuze:**

GAT + BiGRU + federated learning; F1 = 0,92 (CICIoT2023), 0,94 (Edge-IIoTset), 0,93 (RT-IoT2022). **Inferencija 120–180 ms Raspberry Pi 4.** Ryšio kaina su FL −20 % (10 mazgų).

> **Sugretinimas, kuris turi būti skyriuje juodu ant balto:** `sallam2026gap` (jau turimas iš 1 užduoties) nurodo šliuzo biudžetą **20–50 ms**. Šis modelis reikalauja **120–180 ms** — nuo 2,4 iki 9 kartų daugiau. Tuo pačiu XGBoost tame pačiame rinkinyje inferuoja per **mikrosekundes**. Skirtumas — trys–keturios eilės. Tai ne stilistinė pastaba, o **pagrindas 3 užduoties sprendimui**, ir jis atsiranda nemokamai, vien sugretinus du šaltinius.

**`eren2026drift` — kodėl antrinis rinkinys būtinas:**

Rinkiniai BoT-IoT, ToN-IoT, UNSW-NB15; pasiskirstymų nuokrypis matuotas KS, KL, JS ir Wasserstein atstumais. Cituojamas kryžminio perkėlimo rezultatas: **vidutinis MCC krenta nuo ~94 % iki ~29 %.** Išvada: stiprūs rezultatai viename rinkinyje nieko nesako apie kitą.

> Šis šaltinis paverčia antrinį rinkinį iš „gerai turėti" į metodologinę būtinybę — ir tai tinka tiksliai ten, kur turime problemą: be laiko žymos negalime daryti chronologinio skaidymo, taigi kryžminis patikrinimas lieka **vienintelis** rimtas argumentas prieš nutekėjimą.

**`mazinani2026constrained`:** LSTM, GRU, SimpleRNN, CNN, TCN, MLP ant STM32H7S78-DK; matuota MACC operacijomis, RAM ir inferencijos laiku (Cube.AI). Geriausias tikslumo ir kainos kompromisas — **MLP ir TCN**. INT8 kvantavimas: **modelis mažėja >90 % beveik neprarandant tikslumo.**

**`mohale2025xai`:** SHAP duoda nuoseklias globalias ir lokalias atributikas, LIME greitesnis ir lokalus. Abu **reikalauja daug skaičiavimo ir riboja realaus laiko naudojimą.** Tai reiškia: XAI mano darbe — **analizės įrankis 6 užduotyje, ne inferencijos grandinės dalis.**

### Kandidatai, kuriuos dar reikia patvirtinti (T1, jei trūksta iki 6)

| Tema | Kandidatas | Būklė |
|---|---|---|
| Federated learning apžvalga | *Computer Science Review* (2026) | ❌ **Neįtraukta.** Metaduomenų patvirtinti nepavyko, o FL vis tiek atmetamas dėl apimties; `nassef2026tinyml` FL padengia pakankamai |
| ML ant CICIoT2023 | Houichi, Jaidi, Bouhoula (2025), *IET Smart Cities* 7(1):e70014 | ✅ **Patvirtinta per Crossref, įtraukta** kaip `houichi2025smartcity` |
| Lengvasvoris 1D-CNN | *Frontiers in AI* (2026) | ❌ Neprireikė — 18 įrašų pakanka |
| **Klasių disbalansas** | Imani, Beikmohammadi, Arabnia (2025), *Technologies* 13(3):88 | ✅ **Pridėta plane nenumatyta** — 5 764:1 disbalansui pagrįsti reikia šaltinio |

> **Taisyklė:** nė vienas įrašas nepatenka į `.bib` be patikrinto DOI per Crossref arba leidėjo puslapį. 1 užduotyje šis principas išlaikytas — nelaužyti jo dabar dėl skaičiaus.

### Kokie 1 užduoties šaltiniai naudojami pakartotinai

`komal2026idsreview` (ML / gilaus / skatinamojo mokymosi porūšiai — 2.1 ašies pagrindimas) · `meidan2018nbaiot` (autokoderis — 2.3) · `sallam2026gap` (delsos biudžetai — 2.6) · `reddy2026datasets` (rezultatų šališkumas — 2.7) · `alwhbi2024encrypted` (kodėl srauto metaduomenys yra tinkama įvestis).

**Faktas:** 11 + 7 = **18 įrašų**; 3 užduotis pridės 2–3 → ~20. Tai patenka į 15–25 rėžį visam darbui.

---

## 6. ~~Rezultatų patikimumas be kryžminio patikrinimo~~ — ATSISAKYTA

**Sprendimas 2026-09-02:** poskyris 2.8 iš 2 skyriaus **išbraukiamas**, T6 nevykdomas.

**Priežastis — vieta, ne apimtis.** 2 skyrius apžvelgia metodus. Mano būsimų rezultatų galiojimo ribos priklauso metodikai (4 sk., kur užrakinamas skaidymo sprendimas) ir apribojimų aptarimui (6 sk.). Aiškinti jas dar prieš pasirenkant metodus reiškia atsakinėti į klausimą, kurio niekas neuždavė, ir atkreipti dėmesį į trūkumą.

**Antrinių duomenų rinkinių tiesiog nėra — to konstatavimas nereikalauja poskyrio.**

### Kas vis dėlto neturi dingti

Vienas sakinys **4 skyriaus metodikoje**, prie skaidymo sprendimo: rinkinyje nėra laiko žymos, todėl chronologinis skaidymas neįmanomas; naudojamas stratifikuotas atsitiktinis, o apribojimas įvardijamas atvirai. To pakanka — `reddy2026datasets` jau cituojamas 1 skyriuje, `eren2026drift` lieka `tab:susije`.

### Nematytos atakų klasės testas — lieka, bet kitu pagrindu

Anksčiau jį buvau pateikęs kaip kryžminio patikrinimo **pakaitalą**. Tai buvo silpna motyvacija. Realus pagrindas paprastesnis: **darbe yra neprižiūrimų kandidatų (autokoderis, Isolation Forest), kurių vienintelė prasmė — aptikti nematytas atakas.** Netikrinant to nematytomis klasėmis, jų įtraukimas lieka nepatikrintas teiginys.

Taigi testas yra ne kompensacija, o **tiesioginė autokoderio hipotezės patikra**, ir jam vieta 5 užduotyje savaime.

## 7. Laiko biudžetas — rugsėjo 2 d. (trečiadienis)

| Laikas | Darbas | Rezultatas | Prior. |
|---|---|---|---|
| ~~09:45–10:45~~ | ✅ **T0 atlikta.** Antraštė sutikrinta, `duomenys/README.md` perrašytas | 39 požymiai + `Label`; 4 tapatybės; registro pokytis | **P0** |
| **11:20–11:50** | **Patikros skriptas ant 200 000 eilučių** (`duomenys/README.md` kodas): patvirtinti keturias tapatybes ir etikečių registrą | Tapatybės patvirtintos arba paneigtos | **P0** |
| 11:50–12:30 | T1: 5 branduolio šaltinių `.bib` įrašai iš leidėjų „Export citation"; `build.ps1`, kad biber klaidos išaiškėtų iš karto | 16 įrašų, kompiliuojasi | P0 |
| *12:30–13:15* | *Pietūs* | | |
| 13:15–13:45 | **T4: `tab:susije` pildymas.** Skaičiai jau ištraukti (5 skyrius) — tai perkėlimo, ne skaitymo darbas | Lentelė užpildyta | **P0** |
| 13:45–14:45 | **T3: `tab:metodai`.** Pirma pildoma lentelė, tik paskui rašomas tekstas aplink ją | ~12 eilučių, šaltinio stulpelis be tuščių langelių | **P0** |
| 14:45–15:30 | Poskyriai 2.2–2.5 — tekstas aplink `tab:metodai` | ~3 psl. `.tex` | P1 |
| 15:30–16:15 | **T5: poskyris 2.6** — delsos sugretinimas (120–180 ms vs 20–50 ms vs µs) + `tab:apribojimai` | ~1 psl., skaičiai citatose | **P0** |
| 16:15–16:50 | Poskyris 2.7 — rezultatų patikimumas aplink `tab:susije` **+ 39 vs 46 pastraipa** | ~0,85 psl. | **P0** |
| 16:50–17:10 | T7: poskyris **2.8** — kandidatų aibė 3 skyriui, su atmetimo priežastimis | ~0,3 psl. | **P0** |
| 17:25–17:40 | Poskyris 2.1 — **rašomas paskutinis**, kai aiškus skyriaus turinys | ~0,5 psl. | P1 |
| 17:40–18:00 | T8: anotacijos · `build.ps1` · git commit + push · **žurnalo įrašas** | Kompiliuojasi be klaidų | P0 |

**Metodinė pastaba dėl tvarkos.** Lentelės pildomos **prieš** tekstą (11:45, 13:15), o įžanginis poskyris rašomas **paskutinis** (17:20). Rugsėjo 1 d. patirtis rodo, kad tekstas, rašomas prieš lentelę, vėliau perrašomas — ir tai kainuoja daugiau nei atrodo. Ta pati logika, kaip su generuojamomis rezultatų lentelėmis.

**Dienos pabaigos kriterijus (minimalus):** `tab:metodai` ir `tab:susije` užpildytos, 2.6–2.8 parašyti, PDF kompiliuojasi, duomenų radiniai įrašyti į žurnalą. Visa kita — P1 ir gali persikelti į rugsėjo 3 d. rytą.

> **Ko į šią dieną NEKELTI.** Patikra atvėrė tris kodo darbus: `Label` didžioji raidė, `.upper()` normalizavimas `etiketes.py`, ir `tab:atakos` eilutės, remiančios `flow_duration` bei asimetrija. **Visi trys — rugsėjo 3 d. rytas, ne šiandien.** Jie neblokuoja 2 skyriaus rašymo, o įsileisti kodo taisymus į rašymo dieną yra tiesiausias kelias pakartoti rugsėjo 1 d. scenarijų, kai 4 val. iš 9 praėjo klaidose.

> **Suspausto varianto kaina — pasakoma atvirai.** Pradiniame plane šiai užduočiai buvo dvi dienos (rugs. 4 ir 7). Suspaudus į vieną, pirmas nukenčia **poskyrių 2.2–2.5 tekstas** — jis gali likti konspektyvus. Tai priimtina: 3 užduočiai reikia lentelių ir sprendimų, ne prozos. **Neturi nukentėti 2.6–2.8.** Jei 16:00 matyti, kad nespėjama, P1 poskyriai paliekami juodraštiniai ir baigiami rugsėjo 3 d. ryte — rezervo yra, nes visas grafikas eina diena į priekį.

---

## 8. Priėmimo kriterijai

- [x] **T0:** antraštė sutikrinta; neatitikimai surašyti; `duomenys/README.md` perrašytas *(atlikta 11:20)*
- [ ] Keturios tapatybės patvirtintos ant ≥200 000 eilučių — **arba** pažymėtos kaip nepatvirtintos ir į ataskaitą **neįrašytos**
- [ ] Etikečių registras patikrintas `df["Label"].unique()`
- [x] `02_di_metodai.tex` kompiliuojasi be klaidų · TODO žymų nėra · **9,7 psl.** — viršija taikinį, **trumpinimas atidėtas iki viso darbo** (sprendimas 2026-09-02)
- [x] `tab:metodai` — **18 eilučių**, nė vieno tuščio langelio stulpelyje „Šalt.“ *(T3)*
- [ ] `tab:susije` — ≥7 eilutės; kiekvienoje užpildyti „Užduotis" ir „Kas kelia abejonių"
- [x] Skaitinis delsos sugretinimas atliktas *(T5)*: 3,53 µs telpa **5 669 kartus** į 20 ms biudžetą; gilusis modelis jį viršija 2,4–9 kartų
- [ ] `tab:susije` kiekvienoje CICIoT2023 eilutėje nurodyta, **kiek požymių** darbas naudojo
- [ ] Požymių aibės apribojimas (39 iš 46) įvardytas 2.7 poskyryje; galiojimo ribos dėl skaidymo — **4 skyriaus metodikoje**, ne čia
- [x] Kandidatų aibė 3 užduočiai suformuluota (**6 metodai**); kiekvienas iš **8 atmestų** turi priežastį *(T2)*
- [ ] `saltiniai.bib` — 16–19 įrašų, visi su patikrintu DOI, `biber` be klaidų
- [x] `literatura/anotacijos.md` padengia **visus 18** `.bib` įrašų — patikrinta sugretinant raktus *(T8)*
- [ ] Nė vienas metodų vertinimas nepateiktas kaip faktas be šaltinio arba be „(aut.)" žymos
- [ ] `git push`; `DARBO_ZURNALAS.md` papildytas; `STRUKTURA.md` atnaujinta (`02_di_metodai.tex` ⬜ → ✅)

---

## 9. Rizikos ir jų valdymas

| Rizika | Ženklas | Veiksmas |
|---|---|---|
| ~~Duomenų patikra atveria daug neatitikimų~~ | **Įvyko** | Neatitikimai surašyti, `duomenys/README.md` perrašytas. **`tab:atakos` taisymas — rugs. 3 d. rytą**, ne šiandien: 2 užduotis svarbesnė už 1 skyriaus poliravimą |
| **Tapatybės nepasitvirtina ant viso rinkinio** | 11:50 `np.allclose` grąžina `False` | Nerašyti jų į ataskaitą kaip fakto. Pataisyti `duomenys/README.md` ir tęsti — 2 skyriaus turinys nuo to nepriklauso |
| **Skyrius išplinta kaip 1-asis** | 15:00 tekstas >6 psl., 2.6 neparašytas | Apimties stabdis iš 3 skyriaus: pjaunami 2.2 ir 2.4, ne 2.6–2.9 |
| **Užstrigimas skaitant naujus straipsnius** | 12:30 `tab:susije` tuščia | **Skaičiai jau ištraukti** (5 skyrius). Straipsniai atidaromi tik patikrinti citatai, ne skaityti nuo pradžių |
| **Metodų matrica virsta nuomone** | „Šaltinis" stulpelyje tuščia | Priėmimo kriterijus to neleidžia. Jei vertinimo nepavyksta pagrįsti — rašoma „(aut.)", ir tai sąžininga |
| **Federated learning išplinta** | 2.5 užima >0,6 psl. | FL mano darbe **nerealizuojamas** — jis apžvelgiamas kaip kryptis ir 3 užduotyje atmetamas dėl apimties. Vienas paragrafas + viena `tab:metodai` eilutė |
| **Skelbiami rezultatai nepalyginami** | Straipsniai naudoja skirtingas užduotis ir metrikas | Būtent todėl `tab:susije` turi stulpelį „Užduotis". **Nepalyginamumas yra radinys**, ne kliūtis — jis įrašomas į 2.7 |
| **Suspausta diena** | Nespėjama iki 18:00 | P1 poskyriai perkeliami į rugs. 3 d. rytą. Grafikas eina diena į priekį — rezervas yra |
| **Aplinkos problemos** | Kompiliavimo klaida | 1 užduoties taisyklė: **po pirmo nepavykusio taisymo — ne antras spėjimas, o duomenys** (pilnas log'as, `-Clean`, bisekcija) |

---

## 10. Kas keliauja į 3 užduotį (rugs. 8 d.)

Užsirašyti skyriaus pabaigoje, kad rugsėjo 8 d. nereikėtų atkurti:

- **Ketvertas jau fiksuotas** (RF, XGBoost, MLP, autokoderis) — rugs. 8 d. lieka priskirti svorius ir pagrįsti, o ne rinktis iš naujo
- **Pagrindinis detalumas: 8 kategorijos** (~20 paleidimų vietoj ~70)
- ⚠️ **Palyginimo asimetrija:** autokoderio negalima dėti į tą patį macro-F1 stulpelį — 6 sk. lentelė turės dvi dalis
- **Delsos ribojimas:** gilieji modeliai netelpa į 20–50 ms šliuzo biudžetą, jei nekvantuojami. Tai iš anksto pasveria kriterijų „resursų poreikis"
- **Realistinis metrikos tikslas:** macro-F1 0,85–0,90, ne 0,99 — atskaitos taškas iš `almahaqeri2026gradient`
- **Požymių atrankos argumentas:** 46 → 23 požymiai duoda 30–51 % greitesnę inferenciją beveik neprarandant tikslumo → svarstyti 4 užduotyje
- **Efektyvus požymių skaičius ~35, ne 39** — keturios tapatybės pašalinamos sąmoningai, prieš bet kokią automatinę atranką
- **Nematytos atakų klasės testas perkeliamas į privalomą 5 užduoties dalį** — atmetus antrinius rinkinius, jis yra pagrindinė apsauga nuo per optimistinio rezultato. Rugs. 8 d. tai turi būti eksperimento protokolo dalis, ne 6 užduoties priedas
- **INT8 kvantavimas** (`mazinani2026constrained`) — jei gilusis modelis pateks į atranką, tai jo pateisinimo sąlyga

---

## 11. Sutvarkyti pakeliui (smulkūs likučiai)

Ne šios užduoties dalis, bet pigu padaryti tarp darbų:

- [ ] `pip freeze > requirements-lock.txt`
- [ ] Titulinio puslapio fakultetas ir praktikos vadovas

**Perkelta į rugsėjo 3 d. rytą** *(atsirado po 11:20 patikros)*:

- [ ] `src/duomenys/ikelimas.py` ir `etiketes.py`: `label` → `Label`, registro normalizavimas `.str.upper()`
- [ ] `ataskaita/skyriai/01_atakos.tex`: `tab:atakos` eilutės, kurių „matomi tinklo požymiai" mini srauto trukmę arba asimetriją — pakeisti į `Number` / `IAT` / `Rate` arba pažymėti kaip nepadengtus duomenimis
- [ ] `duomenys/README.md` skyrius „Keturios tikslios priklausomybės" — patikslinti pagal 200 000 eilučių rezultatą
- [ ] Sprendimas dėl 1 skyriaus apimties — **paliekamas rugs. 8 d.**, kai bus žinomas realus 2 ir 3 skyrių dydis. Šiandien jo nespręsti (viena diena, du sprendimai — žr. 6 skyrių)

---

## 12. Apimties biudžetas: 2,5 savaitės, vienas žmogus, be serverio ⭐

**Sprendimas (2026-09-02):** darbe naudojamas **tik CICIoT2023**. Antriniai rinkiniai (TON\_IoT, Edge-IIoTset) atmesti.

**Pagrindimas — trys nepriklausomos priežastys:**

1. **Skirtingos požymių aibės ir struktūros.** Kiekvienas rinkinys turi savo antraštę, savo etikečių schemą ir savo kodavimą. Kaip tik parodė rugsėjo 2 d. patikra, net **to paties** rinkinio kitas leidimas skiriasi 8 stulpeliais, etikečių registru ir pavadinimu. Antras rinkinys reikštų antrą tokią patikrą, antrą įkėlimo grandinę ir antrą požymių derinimo sluoksnį.
2. **Kiekvienam rinkiniui reikėtų atskirų modelių.** Nesutampant požymiams, modelio perkelti negalima — reikia mokyti iš naujo ant bendro poaibio. Tai daugina 4 ir 5 užduotis iš dviejų.
3. **Resursai.** 14 darbo dienų, vienas žmogus, viena darbo vietos mašina be GPU (TensorFlow Windows'e GPU nebepalaiko nuo 2.11). Tai ne komanda su serveriu, mokančiu modelius visą parą.

> **Ribojantis veiksnys yra kalendorius, ne skaičiavimai** — ir tai reikia pasakyti tiesiai. Pirmoji ir antroji priežastys yra metodologinės; trečioji viena nepateisintų apimties mažinimo, bet kartu su jomis sudaro nuoseklų argumentą.

### Kiek duomenų iš tikrųjų reikia

Patikra parodė, kad **45 mln. eilučių nėra privalumas** — 97,7 % jų yra potvynio (flood) srautas, o retos klasės yra tokios, kokios yra, ir daugiau jų nebus.

| Riba klasei | Eilučių | Dalis rinkinio | Disbalansas | ~RAM (float32) |
|---:|---:|---:|---:|---:|
| 20 000 | 558 482 | 1,24 % | 17 : 1 | 0,08 GB |
| **100 000** | **2 429 978** | **5,40 %** | **84 : 1** | **0,35 GB** |
| 500 000 | 9 263 034 | 20,58 % | 418 : 1 | 1,33 GB |

**Rekomendacija: riba 100 000 eilučių klasei.** Gaunama 2,43 mln. eilučių — 0,35 GB atmintyje, telpa į bet kurį nešiojamą kompiuterį, Random Forest mokosi minutėmis, ne valandomis. **Ir tuo pačiu disbalansas krenta nuo 5 764 : 1 iki 84 : 1**, t. y. imtis sprendžia dvi problemas vienu veiksmu.

### ⭐ Argumentas, kuris pakeičia apribojimą į metodologiją

Retos klasės **paimamos visos** — jų riba niekada neįsijungia:

| Klasė | Viso | train | val | test |
|---|---:|---:|---:|---:|
| `UPLOADING_ATTACK` | 1 196 | 837 | 179 | **179** |
| `RECON-PINGSWEEP` | 2 161 | 1 512 | 324 | 324 |
| `BACKDOOR_MALWARE` | 3 078 | 2 154 | 461 | 461 |
| `XSS` | 3 705 | 2 593 | 555 | 555 |

**Mažiausia klasė duoda 179 testavimo pavyzdžius, ir jokie skaičiavimo resursai to nepakeis.** Serveris, mokantis visą parą ant visų 45 mln. eilučių, gautų lygiai tuos pačius 179 — nes daugiau `UPLOADING_ATTACK` duomenų tiesiog neegzistuoja.

> Vadinasi, **imtis nėra kompromisas dėl resursų stokos — ji yra teisingas sprendimas.** Laikyti 6,9 mln. `DDOS-ICMP_FLOOD` eilučių šalia 1 196 `UPLOADING_ATTACK` eilučių nesuteikia informacijos, tik iškreipia mokymą ir metrikas. **Taip tai ir rašoma ataskaitoje: pasirinkimas, o ne apribojimas** — tas pats retorinis principas, kurį jau naudoja `reddy2026datasets` (įvardytas trūkumas vertingesnis už nutylėtą aukštą skaičių).

### Ką tai reiškia metodų atrankai (2.6 poskyris)

Skaičiavimo biudžetas tampa **vertinimo kriterijumi su skaičiumi**, ne bendra pastaba:

- **Mokymo laikas ≤ 30 min. vienam modeliui** be GPU. Metodas, kurio vienas apmokymas trunka ilgiau, netelpa į 14 dienų su 3–5 kartojimais.
- **Hiperparametrų paieška ribota** — Random Search su 20–30 bandymų, ne Grid Search.
- **Gilieji modeliai vertinami dvigubai atsargiau:** be GPU jie brangūs mokant, o `nassef2026tinyml` rodo, kad ir inferuojant netelpa į 20–50 ms šliuzo biudžetą (120–180 ms Raspberry Pi 4). **Du nepriklausomi argumentai prieš tą patį metodą.**
- Į `tab:metodai` stulpelį „Resursų poreikis" įrašoma **mokymo ir inferencijos skirtis** — būtent dėl to jis ir buvo suplanuotas atskirai.

### Kas iš to seka 5 užduočiai

Nematytos atakų klasės testas (6 skyrius) **į šį biudžetą telpa**: jis kainuoja ne N papildomų mokymų, o **2–3** — po vieną kiekvienai išimtai klasei, ir tik geriausiam modeliui. Tai vienintelė likusi apsauga nuo per optimistinio rezultato, ir ji pigi. **Jos nemažinti.**
