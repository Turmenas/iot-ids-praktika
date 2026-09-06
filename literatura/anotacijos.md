# Literatūros anotacijos — 1 užduotis

**Sudaryta:** 2026 m. rugsėjo 1 d., 13:40
**Failo vieta repozitorijoje:** `literatura/anotacijos.md`
**Atitinkamas BibTeX:** `ataskaita/saltiniai.bib` (11 įrašų)

> Darbinės pastabos. **Į ataskaitą nekeliauja.**
> Kiekvienam šaltiniui: kas tai · kas jame naudinga · kur konkrečiai panaudosiu · ką reikia žinoti.

---

## Sprendimas dėl šaltinių kiekio

Pradiniame plane 1 skyriui numatyta 15–25 šaltiniai. **Sumažinta iki 11.** Pagrindimas:

- 25 šaltiniai viename 4–5 psl. skyriuje reikštų ~5 citavimus puslapyje — tai jau ne analizė, o sąrašas. Recenzentui matosi iš karto.
- Realiai naudingų, recenzuotų ir **konkrečių** (su atakų mechanika, požymiais ar metrikomis) darbų šia tema nėra 25 — pusę sąrašo sudarytų persidengiančios apžvalgos.
- Visos ataskaitos bibliografija natūraliai užaugs iki ~22–28 įrašų: 2 užduotis prideda DI metodų šaltinius, 3 užduotis — palyginimo taškus. **15–25 buvo teisingas skaičius visam darbui, ne vienam skyriui.**

**Taikyti atrankos kriterijai:** recenzuota arba aukšto rango konferencija · IoT kontekstas, ne bendras tinklų saugumas · yra konkretika, ne vien konceptai · **kiekvienas šaltinis turi bent vieną poskyrį, kuriame be jo neapsieitum** (šis kriterijus išmetė ~6 kandidatus).

**Metaduomenys patikrinti** per Crossref ir OpenAlex API bei leidėjų puslapius — ne per Google Scholar. Visi DOI galioja 2026-09-01.

---

## A. Taksonomijos karkasas

### `krishna2021taxonomy` — Krishna et al. (2021), *Sustainability* 13(16):9463

**Kas tai:** apžvalga, kuri IoT grėsmes klasifikuoja pagal architektūros sluoksnius.

**Kas naudinga:** vienintelis iš atrinktų, kuris **aiškiai pateikia tris atskaitos modelius** — trijų sluoksnių (suvokimo / tinklo / programų), penkių (papildomai paslaugų ir operacijų) ir septynių sluoksnių — ir kiekvienam priskiria atakų pavyzdžius. Suvokimo sluoksniui: informacijos klastojimas, MITM, trikdymas (jamming); tinklo/šliuzo: fizinės, programinės, kriptoanalizės ir šoninio kanalo atakos; programų/debesies: SQL injekcijos, DDoS, silpna autentifikacija, užpakalinės durys.

**Kur panaudosiu:** **1.1 poskyris** — pagrindimas, kodėl darbe naudojamas trijų, o ne penkių ar septynių sluoksnių modelis. Be šio šaltinio pasirinkimas atrodytų savavališkas.

**Ką žinoti:** seniausias iš teorinių šaltinių (2021), todėl **naudojamas tik architektūros modeliui**, ne konkrečioms atakoms — jos imamos iš naujesnių. Architektūros atskaitos modeliai per 5 metus nepasensta, atakų sąrašai pasensta.

---

### `sasi2024attacks` — Sasi, Lashkari, Lu, Xiong, Iqbal (2024), *Journal of Information and Intelligence* 2(6):455–513

**Kas tai:** 59 psl. apimties apžvalga — pagrindinis 1 skyriaus šaltinis.

**Kas naudinga:** išsamiausias atrinktų atakų katalogas su siūlomomis atsakomosiomis priemonėmis. Klasifikuoja **keliomis dimensijomis vienu metu**: atakos sritis, grėsmės kategorija, vykdymo būdas, programinis paviršius, ryšio protokolas, įrenginio charakteristikos, užpuoliko pozicija, žalos lygis.

**Kur panaudosiu:** **1.2 poskyris** — atakų sąrašas ir jų aprašai, `tab:atakos` eilučių pagrindas.

**Ką žinoti — svarbu:** ši apžvalga **nesiremia trijų sluoksnių modeliu.** Jos dimensijos kitos. Tai reiškia, kad atakas į sluoksnius **skirstau aš**, remdamasis `krishna2021taxonomy` modeliu, o Sasi et al. naudoju kaip atakų šaltinį. Ataskaitoje tai reikia parašyti tiesiai — priešingu atveju atrodys, tarsi cituočiau klasifikaciją, kurios šaltinyje nėra.

**Papildomas privalumas:** Lashkari ir Lu yra ir CICIoT2023 straipsnio bendraautoriai (Kanados kibernetinio saugumo institutas, UNB). Taksonomija ir duomenų rinkinys — iš tos pačios mokyklos, todėl terminija sutampa. Tai palengvina `tab:aprepis` sudarymą.

**Metų niuansas:** paskelbta internete 2023-12-22, bet leidinio numeris — 2024 m. **Cituojame 2024** (leidėjo oficiali data).

---

### `fei2023systematic` — Fei, Ohno, Sampalli (2023), *ACM Computing Surveys* 56(5):1–40

**Kas tai:** sisteminė 171 publikacijos apžvalga aukščiausio rango apžvalgų žurnale.

**Kas naudinga:** IoT architektūros šablonai ir tipinės savybės, funkciniai saugumo reikalavimai ir **susiję standartai** — dimensija, kurios kituose atrinktuose šaltiniuose nėra.

**Kur panaudosiu:** **1.1 ir 1.5 poskyriai** — IoT specifikos argumentai (ribotas resursas, protokolų įvairovė, nevienalytis elgesio profilis) ir nuoroda į standartus. Taip pat metodologinis svoris: viena ACM CSUR nuoroda vertingesnė už penkias iš nežinomų leidinių.

**Ką žinoti:** kaip ir Sasi et al., **sluoksnių modelio kaip organizavimo ašies nenaudoja**. Imu iš jo reikalavimus ir apribojimus, ne klasifikaciją.

---

## B. Konkretūs sluoksniai ir atakos

### `prajapati2025rpl` — Prajapati et al. (2025), *Computers and Electrical Engineering* 123:110071

**Kas tai:** RPL maršrutizavimo atakų apžvalga — tinklo sluoksnio gylis.

**Kas naudinga:** RPL yra **IoT specifinis** maršrutizavimo protokolas (RFC 6550), ir jo atakos (rango, sinkhole, wormhole, DIS potvynis, versijos numerio) neturi atitikmens klasikiniuose IT tinkluose. Būtent tai pagrindžia teiginį „įprastas IDS IoT netinka" konkrečiai, o ne bendrai.

**Kur panaudosiu:** **1.2.2 poskyris** (tinklo sluoksnis) ir **1.5** — argumentas dėl protokolų specifikos.

**Ką žinoti — svarbu `tab:aprepis` lentelei:** **CICIoT2023 RPL atakų neturi.** Jos lieka taksonomijoje, bet nepatenka į modeliuojamą aibę. Tai viena stipriausių eilučių spragų aptarime: parodo, kad taksonomija sudaryta iš literatūros, o ne atbulai iš duomenų rinkinio etikečių.

---

### `antonakakis2017mirai` — Antonakakis et al. (2017), *USENIX Security 17*, p. 1093–1110

**Kas tai:** kanoninė Mirai botneto analizė. 19 autorių, tarp jų Georgia Tech, Michigan, Google, Cloudflare, Akamai.

**Kas naudinga:** ne aprašomoji, o **išmatuota** analizė — plitimo mechanika (Telnet prievadai 23/2323, žodyno ataka su ~60 numatytųjų kredencialų), skenavimo elgsena (be būsenos SYN skenavimas su pseudoatsitiktiniais taikiniais) ir DDoS pajėgumas. Tai tiesiogiai virsta **matomais tinklo požymiais**: SYN vėliavėlių dalis, unikalių paskirties adresų skaičius per langą, jungčių į 23/2323 prievadus dažnis, srauto asimetrija.

**Kur panaudosiu:** **1.2.3 poskyris** ir `tab:atakos` eilutės „Mirai / botnetų verbavimas" požymių stulpelis.

**Ką žinoti:** 2017 m. — sąmoningai, tai pirminis šaltinis. Klasika čia pateisinama; teiginį, kad Mirai variantai aktualūs iki šiol, atremiu į `neto2023ciciot` (CICIoT2023 turi atskirą **Mirai kategoriją**, sukurtą 2023 m.).

---

### `meidan2018nbaiot` — Meidan et al. (2018), *IEEE Pervasive Computing* 17(3):12–22

**Kas tai:** N-BaIoT — realaus Mirai ir BASHLITE srauto iš 9 komercinių IoT įrenginių rinkinys ir aptikimas giliaisiais autokoderiais.

**Kas naudinga:** **tiltas tarp 1 ir 4 skyriaus.** Parodo pilną grandinę: ataka → statistiniai srauto požymiai (paketų dydžio ir tarppaketinio intervalo statistikos slenkančiuose languose, agreguotos pagal šaltinio IP, IP+MAC ir kanalą) → neprižiūrimas modelis → aptikimas. Būtent tokia požymių inžinerija bus atkartojama 4 užduotyje.

**Kur panaudosiu:** **1.2.3** (botnetų požymiai) ir **1.4** — argumentas, kad anomalijomis grįstas aptikimas veikia be atakų pavyzdžių. Vėliau — 2 užduoties autokoderio poskyryje ir 3 užduoties pagrindime.

**Ką žinoti:** N-BaIoT apima **tik botnetus**. Kaip antrinį rinkinį kryžminiam patikrinimui jis per siauras — TON\_IoT arba Edge-IIoTset lieka geresni kandidatai (sprendžiama rugs. 7 d.).

---

## C. Aptikimo metodai ir diegimo vieta

### `komal2026idsreview` — Komal, Li (2026), *Sensors* 26(11):3405

**Kas tai:** naujausia išsami IoT IDS apžvalga.

**Kas naudinga:** daugiamatė IDS taksonomija — **parašais grįsti, anomalijomis grįsti** (statistiniai, ML, giliojo mokymosi, skatinamojo mokymosi porūšiai) ir **hibridiniai**. Tai tiksliai `tab:aptikimas` eilučių struktūra. Aptaria diegimo lygius: įrenginys su TinyML → rūko (fog) tarpinis apdorojimas → debesis. Peržiūri ir senus rinkinius (DARPA 1998, KDDCUP 99, NSL-KDD), ir modernius (Bot-IoT, TON\_IoT, CICIoT2023) su jų ribotumais.

**Kur panaudosiu:** **1.4 poskyris** ir `tab:aptikimas` karkasas; **1.6** — diegimo vietos.

**Tiesioginis citavimas:** teiginys, kad parašais grįstas IDS „negali aptikti zero-day atakų ar besikeičiančių grėsmių", o anomalijomis grįstas tai gali, bet **didesnių klaidingų teigiamų kaina** ribotų resursų aplinkoje. Tai centrinis 1 skyriaus argumentas, vedantis į 2 skyrių.

---

### `sallam2026gap` — Sallam, El Barachi, Li (2026), *IoT* 7(1):16

**Kas tai:** 32 IoT IDS pasiūlymų analizė pagal 10 eksploatacinių kriterijų + spragų analizė.

**Kas naudinga — geriausias skaitmenų šaltinis 1.6 poskyriui:** konkretūs realaus laiko delsos slenksčiai pagal diegimo vietą — **1–10 ms MCU lygmeniui, 20–50 ms šliuzui, ≥100 ms debesiui**. Tai paverčia „edge vs cloud" diskusiją iš bendrų samprotavimų į skaičius.

**Kur panaudosiu:** **1.6 poskyris** (diegimo vietų palyginimo lentelė) ir **5 užduotis** — šie slenksčiai tampa atskaitos taškais, prie kurių lyginsiu savo modelių išmatuotą inferencijos delsą. Be jų 5 užduoties „delsa 3,2 ms" yra skaičius be konteksto.

**Kritinė išvada:** iš 32 tirtų darbų **29 remiasi tik neprisijungus naudojamais (offline) duomenų rinkiniais**, nė vienas nedemonstravo mastelio testų realiomis daugiamazgėmis sąlygomis. Tai kartu ir mano darbo apribojimų pripažinimas (aš irgi dirbu su offline CICIoT2023), ir pagrindimas, kodėl matuoju inferencijos delsą — tai bent dalinis atsakas į šią spragą.

---

### `alwhbi2024encrypted` — Alwhbi, Zou, Alharbi (2024), *Sensors* 24(11):3509

**Kas tai:** šifruoto tinklo srauto analizė ir klasifikavimas mašininiu mokymusi.

**Kas naudinga:** pagrindžia **visą darbo prielaidą.** Šifravimas panaikina gilios paketų analizės (DPI) ir parašais grįsto aptikimo galimybę — naudingoji apkrova nepasiekiama. Bet **srauto lygmens metaduomenys išlieka:** paketų dydžiai, tarpatvykimo laikai, kryptis, antraščių laukai, TCP/UDP vėliavėlės, prievadai, statistinės savybės.

**Kur panaudosiu:** **1.5 poskyris** (IoT specifika — šifruotas srautas) ir, svarbiausia, **1.2 lentelės metodologinis pagrindimas**: būtent todėl stulpelyje „matomi tinklo požymiai" rašomi srauto statistikos dydžiai, o ne naudingosios apkrovos turinys. Ir būtent todėl CICIoT2023 srauto požymiai (~46) yra tinkama įvestis.

---

## D. Duomenų rinkinys ir metodologinė apsauga

### `neto2023ciciot` — Neto et al. (2023), *Sensors* 23(13):5941

**Kas tai:** originalus CICIoT2023 straipsnis. **Citavimas privalomas — ne Kaggle veidrodis.**

**Kas naudinga:** 105 realūs IoT įrenginiai, **33 atakų tipai, 7 kategorijos** (DDoS, DoS, Recon, Web-based, Brute force, Spoofing, Mirai). Požymiai išgaunami iš paketų sekos tarp dviejų mazgų (DPKT biblioteka).

**Kur panaudosiu:** **1.3 poskyris** — `tab:aprepis` (7 kategorijos → mano taksonomijos sluoksniai) ir spragų pastraipa. Toliau — 4 užduoties duomenų aprašas.

**Ką patikrinti rašant:** tikslų požymių skaičių imti iš straipsnio 4 lentelės, o ne iš antrinių šaltinių — internete cituojama tai 46, tai 47 (skirtumas — ar `label` skaičiuojamas kaip požymis). Skaičių patvirtinti paleidus `python -m src.duomenys.ikelimas patikra` ir palyginti su straipsniu.

---

### `reddy2026datasets` — Reddy, Kumar (2026), *Frontiers in Big Data* 9:1878260

**Kas tai:** į duomenų rinkinius orientuota IoT/IIoT IDS apžvalga — 40+ rinkinių keturiose kategorijose, įskaitant CICIoT2023.

**Kas naudinga:** įvardija **vertinimo šališkumus**, dėl kurių skelbiami 99 %+ tikslumai yra dirbtiniai: klasių disbalansas, rinkinių paprastumas, pasikartojantys atakų šablonai, sintetinio srauto dominavimas, laiko nutekėjimas. Modeliai išmoksta statistinius rinkinio artefaktus, o ne kenkėjišką elgseną. Rekomenduoja srauto realistiškumą, laiko tęstinumą ir **kryžminį validavimą tarp rinkinių** vietoj neapdoroto tikslumo.

**Kur panaudosiu:** **1.7 apibendrinimas** — sakinys, kad aukštas skaičius pats savaime nieko nereiškia; toliau **4 užduotis** (chronologinis skaidymas, balansavimas tik ant train) ir **5 užduotis** (rezultatų patikimumo patikra).

**Kodėl vertinga strategiškai:** šis šaltinis leidžia savo santykinai kuklius rezultatus pateikti kaip **sąmoningą metodologinį pasirinkimą**, o ne trūkumą. Jei mano F1 bus 0,94, o literatūroje skelbiama 0,99 — turiu recenzuotą šaltinį, paaiškinantį skirtumą.

---

---

# 2 UŽDUOTIS — DI ir MM metodai

**Papildyta:** 2026 m. rugsėjo 2 d. · 7 nauji įrašai (11 → 18)
Visi DOI patikrinti per Crossref API; metrikos — leidėjų puslapiuose tą pačią dieną.

---

## E. Atskaitos taškai: mašininis mokymasis ant CICIoT2023

### `almahaqeri2026gradient` — Almahaqeri et al. (2026), *Scientific Reports* 16(1):16909

**Kas tai:** vienuolikos metodų palyginimas ant CICIoT2023 su gradientinio stiprinimo akcentu (XGBoost, LightGBM, CatBoost, NGBoost, ExtraTrees, RF, sprendimų medis, tiesinė SVM, logistinė regresija, AdaBoost, Gaussian NB).

**Kas naudinga — svarbiausias skaičių šaltinis visam darbui:**

| Užduotis | Metodas | Tikslumas | macro-F1 | Inferencija |
|---|---|---|---|---|
| dvejetainė | XGBoost | 99,61 % | 0,9952 | 0,355 µs |
| dvejetainė | LightGBM | 99,53 % | 0,9944 | 0,719 µs |
| 8 klasės | XGBoost | 99,59 % | **0,8903** | 1,046 µs |
| 34 klasės | XGBoost | 99,48 % | 0,8876 | 3,528 µs |

Požymių atranka 46 → 23 sumažino inferenciją 30–51 %, mokymą 33–40 %.

**Kur panaudosiu:** `tab:susije` keturios eilutės · 2.6 poskyris (disbalanso argumentas) · 2.8 (XGBoost pagrindimas) · **5 užduotis — realistinis tikslas macro-F1 0,85–0,90** · 6 užduotis (palyginimas).

**Ką žinoti — du dalykai:**

1. **Naudota pilna 46 požymių aibė**, o mūsų leidime jų 39. Tiesioginis palyginimas negalioja, ir tai turi būti pasakyta 6 skyriuje. Be to jų požymių atrankos rezultato (46 → 23) atkartoti neįmanoma — tarp trūkstamų yra `Magnitue`, `Covariance`, `Weight`.
2. **Tikslumo ir macro-F1 atotrūkis yra pagrindinė šio šaltinio vertė**, ne aukštas skaičius. Tas pats modelis, tie patys duomenys: tikslumas 99,61 → 99,59, o macro-F1 0,9952 → 0,8903. Tai empirinis įrodymas, kad esant 42:1 disbalansui bendras tikslumas bevertis.

---

### `houichi2025smartcity` — Houichi, Jaidi, Bouhoula (2025), *IET Smart Cities* 7(1):e70014

**Kas tai:** įsibrovimų aptikimo sistema išmaniojo miesto kontekste, mašininio mokymosi metodai ant CICIoT2023.

**Kas naudinga:** antras nepriklausomas atskaitos taškas tame pačiame rinkinyje. Du šaltiniai leidžia atskirti, kas yra rinkinio savybė, o kas vieno darbo rezultatas.

**Kur panaudosiu:** `tab:susije` — eilutė kol kas **neužpildyta**.

**Ką žinoti — ⚠️ NEBAIGTA:** metrikų gauti nepavyko. Wiley grąžina 403, ResearchGate 429, laisvos PDF kopijos nėra. **Reikia universiteto prieigos.** Užpildyti: metodų sąrašas, užduoties detalumas, tikslumas / F1, kaip tvarkytas disbalansas ir skaidymas. Kol neužpildyta, šaltinis `.bib` faile yra, bet lentelėje jo nėra.

---

## F. Resursai, delsa ir diegimas kraštiniame šliuze

### `nassef2026tinyml` — Nassef et al. (2026), *Scientific Reports* 16(1):18524

**Kas tai:** lengvasvorė ir energijai jautri IIoT įsibrovimų aptikimo sistema — grafų dėmesio tinklas su dvikrypčiu GRU, optimizuotas pilkojo vilko algoritmu, papildytas federuotu mokymusi.

**Kas naudinga:** F1 0,94 (Edge-IIoTset), **0,92 (CICIoT2023)**, 0,93 (RT-IoT2022). **Inferencija 120–180 ms Raspberry Pi 4.** Ryšio kaina su FL −20 % dešimties mazgų simuliacijoje.

**Kur panaudosiu:** ⭐ **2.6 poskyrio ašis.** Sugretinus su `sallam2026gap` 20–50 ms šliuzo biudžetu gaunama, kad modelis jį viršija 2,4–9 kartų, o XGBoost tame pačiame rinkinyje inferuoja per mikrosekundes. Keturios eilės skirtumo — ir tai **du nepriklausomi argumentai prieš giliuosius modelius** kartu su mokymo kaina be GPU. Taip pat `tab:susije` trys eilutės ir `tab:metodai` Transformer/GNN eilutės.

**Ką žinoti:**

- **Užduoties detalumo nenurodo**, nors skelbia F1. Todėl neįmanoma pasakyti, ar 0,92 palyginamas su mano rezultatu. Tai eina į `tab:susije` abejonių stulpelį — **trūkstamas metodikos elementas irgi yra abejonė**, ne tik silpna metrika.
- Rakto pavadinimas: iš pradžių buvo `nassef2026tinyfl`, pervadinta į **`nassef2026tinyml`**, nes antraštėje TinyML, o FL — tik viena sudedamoji.

---

### `mazinani2026constrained` — Mazinani, Antonucci, Davoli, Ferrari (2026), *Future Internet* 18(1):34

**Kas tai:** šešių gilaus mokymosi architektūrų (LSTM, GRU, SimpleRNN, CNN, TCN, MLP) veikimo įvertinimas **realiame ribotų išteklių įrenginyje** — STM32H7S78-DK plokštėje, per Cube.AI matuojant MACC operacijas, RAM ir inferencijos laiką.

**Kas naudinga:** **MLP ir TCN duoda geriausią tikslumo ir kainos kompromisą.** Post-treniruotinis kvantavimas iki 8 bitų sveikųjų skaičių sumažina modelį **daugiau nei 90 %** beveik neprarandant tikslumo.

**Kur panaudosiu:** ⭐ **2.8 poskyris — pagrindinis MLP pasirinkimo argumentas.** Taip pat `tab:metodai` gilaus mokymosi eilutės, `tab:apribojimai` įrenginio eilutė, `tab:susije`.

**Ką žinoti — pasirodė artimesnis, nei atrodė iš pradžių:**

1. **Naudoja CICIoT2023** ir **tas pačias tris konfigūracijas** — dvejetainę, 8 ir 34 klases. Todėl tai tiesiogiai susijęs darbas, o ne vien resursų šaltinis.
2. Nurodo **46 686 579 įrašus**, t. y. pilną oficialią versiją — dar vienas patvirtinimas, kad mūsų 45 019 243 eilučių leidimas yra kitas.
3. **Skelbia suminį kompromiso balą, o ne metrikas kiekvienam modeliui.** Todėl tiesiogiai palyginti su savo skaičiais neįmanoma — tai `tab:susije` abejonių įrašas.

---

## G. Klasių disbalansas ir rezultatų galiojimas

### `imani2025imbalance` — Imani, Beikmohammadi, Arabnia (2025), *Technologies* 13(3):88

**Kas tai:** Random Forest ir XGBoost elgsenos analizė su SMOTE, ADASYN ir GNUS balansavimo metodais prie keturių disbalanso lygių (mažumos klasė 15 / 10 / 5 / 1 %).

**Kas naudinga:**

- **Suderintas XGBoost su SMOTE nuosekliai geriausias** visuose disbalanso lygiuose.
- ⚠️ **Random Forest esant stipriam disbalansui veikia prastai.** RF yra mūsų atskaitos modelis — tai įspėjimas, ne smulkmena.
- ADASYN vidutiniškai veiksmingas su XGBoost, prastas su RF; GNUS nenuoseklus.
- ⭐ **Didėjant disbalansui F1, Kappa ir MCC stipriai svyruoja, o ROC-AUC ir PR-AUC išlieka stabilūs.** Reikšmingumas patvirtintas Friedmano ir Nemenyi kriterijais (p < 0,05).

**Kur panaudosiu:** 2.6 poskyris (balansavimo pasirinkimas) · `tab:metodai` RF ir XGBoost eilutės · **5 užduotis — argumentas šalia macro-F1 pateikti ir PR-AUC**, nes prie 84:1 F1 bus triukšmingas.

**Ką žinoti — ⚠️ SVARBI PATAISA:** priimdamas šį šaltinį maniau, kad tai IoT įsibrovimų aptikimo darbas. **Nėra.** Naudojami **telekomunikacijų klientų nutekėjimo duomenys** su dirbtinai nustatytais disbalanso lygiais. Todėl jis **netinka `tab:susije` lentelei** ir naudojamas tik kaip metodologinis šaltinis. Įrašytas kaip IoT darbas, jis būtų buvęs klaida ataskaitoje.

---

### `eren2026drift` — Eren et al. (2026), *Electronics* 15(11):2307

**Kas tai:** pasiskirstymų poslinkio tarp IoT įsibrovimų rinkinių (BoT-IoT, ToN-IoT, UNSW-NB15) analizė, matuojant Kolmogorovo–Smirnovo, Kullbacko–Leiblerio, Jenseno–Šenono ir Wassersteino atstumais.

**Kas naudinga:** cituojamas kryžminio perkėlimo rezultatas — **vidutinis MCC krinta nuo ~94 % iki ~29 %.** Išvada: stiprūs rezultatai viename rinkinyje nieko nesako apie kitą, nes rinkiniai turi savitų požymių šališkumų.

**Kur panaudosiu:** `tab:susije` · **4 skyriaus metodika** — vienas sakinys prie skaidymo sprendimo · 6 skyrius (apribojimai).

**Ką žinoti — šaltinio vaidmuo pasikeitė:** iš pradžių jis buvo pagrindimas, *kodėl reikia antrinio rinkinio*. Atsisakius antrinių rinkinių jis tampa pagrindimu, *kodėl vieno rinkinio rezultatų negalima laikyti apibendrinamais*. **Antrasis panaudojimas sąžiningesnis ir 6 skyriui stipresnis** — vietoj silpno kryžminio patikrinimo ant nesutampančių požymių gaunamas aiškiai apibrėžtas galiojimo rėžis.

---

## H. Paaiškinamumas

### `mohale2025xai` — Mohale, Obagbuwa (2025), *Frontiers in Artificial Intelligence* 8:1526221

**Kas tai:** sisteminė paaiškinamo dirbtinio intelekto integravimo į įsibrovimų aptikimo sistemas apžvalga.

**Kas naudinga:** SHAP duoda nuoseklias globalias ir lokalias požymių atributikas; LIME greitesnis ir labiau lokalus, tinkamas pavieniams pranešimams audituoti. **Abu reikalauja daug skaičiavimo ir riboja naudojimą realiu laiku.** Interpretuojamumo ir tikslumo kompromisas išlieka neišspręstas.

**Kur panaudosiu:** 2.5 poskyris · ⭐ `tab:metodai` stulpelio „Interpretuojamumas“ skirstymo pagrindas: *savaiminis* (medžiai) vs *per XAI* (ansambliai, MLP) vs *juodoji dėžė*.

**Ką žinoti — sprendimas darbui:** kadangi SHAP ir LIME kainuoja skaičiavimo, **XAI šiame darbe yra 6 užduoties analizės įrankis, ne inferencijos grandinės dalis.** Skirtumas tarp „savaiminis“ ir „per XAI“ reiškia papildomą kainą, kurios kraštiniame šliuze nemokame.

---

## I. Eksperimento metodika (3 skyrius, 3.6 poskyris)

### `chawla2002smote` — Chawla, Bowyer, Hall, Kegelmeyer (2002), *Journal of Artificial Intelligence Research* 16:321–357

Pirminis SMOTE šaltinis: mažumos klasė papildoma **sintetiniais** pavyzdžiais, interpoliuojant tarp artimiausių tos klasės kaimynų, o ne dubliuojant esamas eilutes. Straipsnis rodo, kad toks papildymas kartu su gausios klasės mažinimu duoda geresnę ROC kreivę nei vien svorių keitimas.

**Kam reikalingas šiame darbe.** 3.6 poskyryje SMOTE numatytas kaip **abliacija vienam modeliui**, ne kaip pagrindinis balansavimo būdas — pagrindinis yra klasių svoriai, nes jie duomenų nedubliuoja. Cituojamas pirminis, o ne naujesnis šaltinis: metodo aprašui tinka originalas, o `imani2025imbalance` lieka empiriniam SMOTE ir XGBoost derinio rezultatui.

⚠️ **Svarbu mūsų duomenims:** SMOTE interpoliuoja tarp kaimynų, o dviprasmiškose srityse sintetiniai pavyzdžiai dviprasmiškumą sustiprintų. *(Patikslinta 2026-09-06: pašalinus dublikatus tokių eilučių darbinėje imtyje yra **0,43 %**, ne 4,98 %, todėl šis argumentas yra silpnas. Lieka du stiprūs: skaičiavimo biudžetas ir `imani2025imbalance` rezultatas, kad geriausias derinys yra suderintas XGBoost su SMOTE — t. y. vertas patikrinti, bet ne numatytasis.)*

### `dietterich1998tests` — Dietterich (1998), *Neural Computation* 10(7):1895–1923

Lygina penkis statistinius testus mokymosi algoritmams palyginti ir parodo, kad **pakartotinio perskirstymo (resampling) testai turi pervertintą I tipo klaidą** — skirtumai atrodo reikšmingi dažniau, nei yra iš tikrųjų, nes paleidimai nėra nepriklausomi.

**Kam reikalingas šiame darbe.** Tai tiesioginis pagrindas 3.6 poskyrio sprendimui: turint **tik tris pradinius dydžius**, t-testas ant jų būtų kaip tik toks testas, apie kurį Dietterich įspėja. Todėl protokole užrašyta, kad skirtumas laikomas reikšmingu tik tada, kai viršija paleidimų sklaidą, o formalus reikšmingumo testas neatliekamas.

> **Kodėl ne Demšar (2006).** Jo darbas skirtas palyginimui **per daug duomenų rinkinių**; čia rinkinys vienas, todėl tinka Dietterich formuluotė. Be to Demšar publikuotas JMLR ir DOI neturi, o taisyklė reikalauja patikrinto DOI.

**Abu šaltiniai — 1998 ir 2002 m.**, t. y. gerokai senesni už visus kitus. Tai sąmoninga: metodo aprašui cituojamas pirminis šaltinis, ne naujausias jį minintis darbas.

## Aprėpties patikra pagal poskyrius

| Poskyris | Šaltiniai | Būklė |
|---|---|---|
| 1.1 Architektūra ir atakų paviršius | `krishna2021taxonomy`, `fei2023systematic` | ✅ |
| 1.2.1 Suvokimo sluoksnis | `krishna2021taxonomy`, `sasi2024attacks` | ⚠️ silpniausia vieta |
| 1.2.2 Tinklo sluoksnis | `prajapati2025rpl`, `sasi2024attacks` | ✅ |
| 1.2.3 Programų sluoksnis | `antonakakis2017mirai`, `meidan2018nbaiot`, `sasi2024attacks` | ✅ |
| 1.3 Sąsaja su CICIoT2023 | `neto2023ciciot`, `reddy2026datasets` | ✅ |
| 1.4 Aptikimo metodai | `komal2026idsreview`, `meidan2018nbaiot` | ✅ |
| 1.5 IoT specifika | `fei2023systematic`, `alwhbi2024encrypted`, `prajapati2025rpl` | ✅ |
| 1.6 Diegimo vieta | `sallam2026gap`, `komal2026idsreview` | ✅ |
| 1.7 Apibendrinimas | `reddy2026datasets` | ✅ |

**Vienintelė spraga: suvokimo (percepcijos) sluoksnis.** Nėra specializuoto šaltinio fizinėms, šoninio kanalo ir jutiklių klastojimo atakoms.

**Sprendimas — sąmoningai nepildyti.** Priežastis: suvokimo sluoksnio atakos **nematomos tinklo srauto duomenyse**, todėl į CICIoT2023 nepatenka ir modeliuojamos nebus. Skirti joms atskirą šaltinį reikštų plėsti skyrių ten, kur praktinė dalis nesiekia. Poskyryje 1.2.1 jos aprašomos trumpai iš dviejų bendrųjų apžvalgų ir **iš karto įvardijamos kaip už darbo ribų**, o `tab:aprepis` tai parodo lentelės forma. Jei recenzentas paklaus — atsakymas paruoštas.

*Jei vis dėlto prireiktų 12-o šaltinio, kandidatas: PUF ir aparatinės saugos apžvalgos (Springer P2P Networking and Applications, 2025). Nepridėta, kol nėra poreikio.*

---

## Aprėpties patikra — 2 skyrius

| Poskyris | Šaltiniai | Būklė |
|---|---|---|
| 2.1 Vertinimo rėmas | `komal2026idsreview` *(iš 1 užd.)* | ✅ |
| 2.2 Prižiūrimas mokymasis | `almahaqeri2026gradient`, `imani2025imbalance` | ✅ |
| 2.3 Neprižiūrimas mokymasis | `meidan2018nbaiot` | ✅ |
| 2.4 Gilusis mokymasis | `mazinani2026constrained`, `nassef2026tinyml` | ✅ |
| 2.5 Paskirstytas mokymasis ir XAI | `nassef2026tinyml`, `mohale2025xai` | ✅ |
| 2.6 Praktiniai apribojimai | `sallam2026gap`, `nassef2026tinyml`, `imani2025imbalance` | ✅ |
| 2.7 Susiję darbai | `almahaqeri2026gradient`, `nassef2026tinyml`, `mazinani2026constrained`, `meidan2018nbaiot`, `eren2026drift` | ⚠️ `houichi` be metrikų |
| 2.8 Kandidatų aibė | `almahaqeri2026gradient`, `mazinani2026constrained`, `meidan2018nbaiot` | ✅ |

**Vienintelė spraga: `houichi2025smartcity` metrikos.** Sprendimas — bandyti per universiteto prieigą. Jei nepavyks, šaltinis lieka `.bib` faile kaip konteksto citata, o `tab:susije` remsis penkiais šaltiniais. Tai priimtina, bet ne pageidautina.

---

## Kiti žingsniai

- [ ] **`houichi2025smartcity`** — gauti metrikas per universiteto prieigą, užpildyti `tab:susije` eilutę
- [ ] Paleisti `.\build.ps1` — nuo rugsėjo 2 d. ryto pridėti **7 nauji `.bib` įrašai ir trys lentelės**, o `biber` su jais dar nebandytas
- [ ] ⚠️ Aplanke `literatura/` yra **du tos pačios anotacijų failo kopijos**: `anotacijos.md` (šis, aktualus) ir `literatura_anotacijos.md` (senesnė). Palikti vieną — ištrinti antrąją
- [ ] 3 užduotis pridės 2–3 šaltinius sprendimų matricos pagrindimui → ~20–21 įrašas
