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

## Kiti žingsniai

- [ ] Įkelti `saltiniai.bib` į `ataskaita/` ir paleisti `build.ps1` — patikrinti, ar `biber` praeina be klaidų
- [ ] Perskaityti pilnai: `sasi2024attacks` (2 sk. — taksonomija) ir `komal2026idsreview` (IDS tipų skyrius). Likusiems — santrauka, išvados, lentelės
- [ ] Pildant `tab:atakos`: kiekvienai eilutei tikrinti, ar požymių stulpelis susisieja su CICIoT2023 stulpeliu
- [ ] `neto2023ciciot` 4 lentelė — nusirašyti tikslų požymių sąrašą, jis reikalingas ir `tab:aprepis`, ir 4 užduočiai
