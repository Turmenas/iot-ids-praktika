# T2 — DI ir MM metodų apžvalga pagal mokymosi paradigmą

**Sudaryta:** 2026-09-02
**Statusas:** darbinis failas. Iš jo pildoma `tab:metodai` (T3) ir rašomi poskyriai 2.2–2.5. **Į ataskaitą nekeliauja.**
**Aprėptis:** 5 paradigmos, 17 metodų. Kiekvienam: veikimo principas · IoT scenarijus · verdiktas šiam darbui.

> **Vertinimo rėmas paveldimas, ne kuriamas.** Kriterijai kyla iš 1 užduoties `tab:reikalavimai`; čia jie tik pritaikomi metodams. Kiekvienas vertinimas pažymėtas arba citata, arba **(aut.)** — mano vertinimas.

---

## 0. Kas keitėsi po rugsėjo 2 d. duomenų patikros ⚠️

Trys patikros radiniai **iš anksto atmeta** ištisas metodų šeimas — ne dėl resursų, o dėl **duomenų prigimties**. Tai svarbiausia šio poskyrio dalis, nes ji sutaupo 4 užduoties dienas.

| Duomenų savybė | Ką ji atmeta |
|---|---|
| **Nėra laiko žymos, nėra eilės tarp įrašų.** Kiekviena eilutė — jau agreguotas 10 arba 100 paketų lango apibendrinimas | **LSTM, GRU, Transformer.** Nėra sekos, kurią būtų galima modeliuoti |
| **Nėra šaltinio/paskirties identifikatorių** (nei IP, nei MAC, nei krypties) | **GNN** — grafo sukonstruoti neįmanoma. **Federated learning** — nėra pagal ką dalyti duomenis į klientus |
| **Įrodytos tikslios priklausomybės tarp požymių** (`Variance`=`Std`², `Tot size`=`AVG`, `Tot sum`=`AVG`×`Number`) | **Naive Bayes** — pažeidžiama pati požymių nepriklausomumo prielaida |

> **(aut.)** Tai stipresni argumentai už resursų trūkumą. Literatūroje LSTM ir Transformer ant CICIoT2023 taikomi dažnai, bet įvestis ten yra tas pats vienos eilutės požymių vektorius, apsimetantis seka. **Įvardyti tai yra savarankiškas indėlis**, o ne apimties mažinimas — ir tai patenka į 2.4 poskyrį bei `tab:susije` stulpelį „Kas kelia abejonių".

---

## 1. Prižiūrimas mokymasis (7 metodai)

Reikalauja pažymėtų duomenų. Turime 45 mln. pažymėtų eilučių, 34 klases — **paradigma tinka visiškai**.

### 1.1 Sprendimų medis (CART)

- **Principas:** rekursyvus požymių erdvės skaidymas pagal priemaišos kriterijų (Gini, entropija).
- **IoT scenarijus:** aiškinamas bazinis modelis; taisyklės perkeliamos į šliuzą kaip `if-else`.
- **Vertinimas:** interpretuojamumas **savaiminis** — vienintelis metodas, kurio sprendimą galima parodyti SOC analitikui be papildomų įrankių. Linkęs persimokyti. **(aut.)**
- **Verdiktas:** ✅ **į kandidatus** — interpretuojamumo apatinė riba ir sveiko proto patikra.

### 1.2 Random Forest

- **Principas:** medžių ansamblis su bootstrap imtimis ir atsitiktiniu požymių poaibiu; balsavimas.
- **IoT scenarijus:** patikimas bazinis daugiaklasis klasifikatorius kraštiniame šliuze.
- **Vertinimas:** atsparus persimokymui ir triukšmui; `class_weight` sprendžia disbalansą be duomenų dubliavimo `\cite{imani2025imbalance}`. Modelio dydis auga su medžių skaičiumi — atmintis šliuze ribojanti. **(aut.)**
- **Verdiktas:** ✅ **į kandidatus** — plane numatytas kaip rezultatą garantuojantis modelis.

### 1.3 XGBoost

- **Principas:** gradientinis stiprinimas — medžiai mokomi nuosekliai, kiekvienas taiso ankstesnių liekamąją paklaidą.
- **IoT scenarijus:** didžiausio tikslumo prižiūrimas modelis lentelinei srauto statistikai.
- **Vertinimas:** **geriausias iš 11 metodų ant CICIoT2023** — accuracy 99,61 % (dvejetainė), macro-F1 0,8903 (8 klasės), inferencija 1,05 µs/įrašui `\cite{almahaqeri2026gradient}`. `scale_pos_weight` ir vidinis `NaN` tvarkymas.
- **Verdiktas:** ✅ **į kandidatus** — laukiamas nugalėtojas.

### 1.4 LightGBM

- **Principas:** gradientinis stiprinimas su lapais grįstu augimu ir histogramų diskretizavimu.
- **IoT scenarijus:** tas pats kaip XGBoost, bet greitesnis mokymas didelėse imtyse.
- **Vertinimas:** accuracy 99,53 %, macro-F1 0,9944 (dvejetainė), 0,72 µs/įrašui `\cite{almahaqeri2026gradient}` — praktiškai lygu XGBoost.
- **Verdiktas:** ⚠️ **atsarginis.** Du beveik tapatūs stiprinimo metodai vienoje palyginimo lentelėje nieko neprideda; imamas, tik jei XGBoost mokymas netilps į biudžetą. **(aut.)**

### 1.5 SVM su RBF branduoliu

- **Principas:** maksimalaus tarpo hiperplokštuma branduolio erdvėje.
- **IoT scenarijus:** stiprus klasifikatorius vidutinio dydžio imtims.
- **Vertinimas:** mokymo sudėtingumas tarp O(n²) ir O(n³). Prie 2,43 mln. eilučių tai **valandos ar paros be serverio**. **(aut.)**
- **Verdiktas:** ❌ **atmetama — mokymo kaina.** Vienintelis metodas, kurį atmeta būtent resursų apribojimas, ir tai pasakoma atvirai.

### 1.6 k-artimiausių kaimynų (k-NN)

- **Principas:** klasė pagal k artimiausių mokymo pavyzdžių daugumą; mokymo fazės nėra.
- **IoT scenarijus:** paprastas etalonas.
- **Vertinimas:** **inferencijos kaina auga su mokymo aibe** — prie 1,7 mln. train eilučių atstumų skaičiavimas kiekvienam paketų langui netelpa į 20–50 ms šliuzo biudžetą `\cite{sallam2026gap}`. Metodas, kurio kaina yra ten, kur jos labiausiai negalima turėti. **(aut.)**
- **Verdiktas:** ❌ **atmetama — inferencijos delsa.**

### 1.7 Naive Bayes

- **Principas:** Bajeso taisyklė su prielaida, kad požymiai sąlygiškai nepriklausomi.
- **IoT scenarijus:** itin pigus etalonas ribotų resursų įrenginiuose.
- **Vertinimas:** ⭐ **prielaida paneigta mūsų pačių duomenimis.** Patikra parodė **tikslias funkcines priklausomybes**: `Variance` = `Std`², `Tot size` = `AVG`, `Tot sum` = `AVG` × `Number`. Tai ne silpna koreliacija, o determinizmas. **(aut.)**
- **Verdiktas:** ❌ **atmetama — pažeista modelio prielaida.** Argumentas savas ir patikrinamas.

---

## 2. Neprižiūrimas mokymasis ir anomalijų aptikimas (4 metodai)

Nereikalauja atakų pavyzdžių — mokoma tik iš gerybinio srauto. **Vienintelis kelias prie zero-day.** Turime 1 051 373 `BENIGN` eilutes — mokymui su kaupu pakanka.

### 2.1 Autokoderis

- **Principas:** neuroninis tinklas mokomas atkurti įvestį per siaurą sluoksnį; anomalija = didelė atkūrimo paklaida.
- **IoT scenarijus:** mokoma tik iš gerybinio srauto; aptinka nematytas atakas be jų pavyzdžių.
- **Vertinimas:** pilna grandinė (ataka → srauto statistikos → neprižiūrimas modelis → aptikimas) demonstruota realiame IoT sraute `\cite{meidan2018nbaiot}`. Reikia slenksčio kalibravimo — papildomas laisvės laipsnis. **(aut.)**
- **Verdiktas:** ✅ **į kandidatus** — plane numatytas neprižiūrimas metodas.

### 2.2 Isolation Forest

- **Principas:** atsitiktiniai skaidymai; anomalijos atskiriamos per mažiau skaidymų nei normalūs taškai.
- **IoT scenarijus:** pigus neprižiūrimas etalonas šliuze.
- **Vertinimas:** tiesinis sudėtingumas, mažas modelis, be hiperparametrų derinimo. Silpnesnis už autokoderį sudėtingoms anomalijoms. **(aut.)**
- **Verdiktas:** ✅ **į kandidatus** — pigus etalonas, kuris parodo, ar autokoderio sudėtingumas apsimoka.

### 2.3 One-Class SVM

- **Principas:** riba, apgaubianti normalius duomenis branduolio erdvėje.
- **IoT scenarijus:** klasikinis anomalijų aptikimo metodas.
- **Vertinimas:** ta pati O(n²) problema kaip 1.5. **(aut.)**
- **Verdiktas:** ❌ **atmetama — mokymo kaina.** Isolation Forest užima tą pačią nišą pigiau.

### 2.4 Klasterizavimas (k-vidurkių, DBSCAN)

- **Principas:** grupavimas pagal tankį arba atstumą iki centro.
- **IoT scenarijus:** žvalgybinė analizė, nežinomų atakų grupių paieška.
- **Vertinimas:** duoda grupes, ne sprendimą „ataka / ne ataka"; vertinimas be etikečių sunkiai palyginamas su kitais metodais. **(aut.)**
- **Verdiktas:** ❌ **už darbo ribų** — paminima 2.3 poskyryje vienu sakiniu.

---

## 3. Pusiau prižiūrimas mokymasis (1 metodas)

### 3.1 Savimoka / pseudo-žymėjimas

- **Principas:** modelis mokomas iš mažos pažymėtos dalies, tada pats žymi nepažymėtus duomenis.
- **IoT scenarijus:** realus diegimas, kur srauto daug, o pažymėto — mažai. **Praktikoje tai dažniausias atvejis.**
- **Vertinimas:** mūsų rinkinys **pažymėtas visas**, todėl paradigma neduotų nieko, ką galėtume išmatuoti. **(aut.)**
- **Verdiktas:** ❌ **už darbo ribų**, bet **paminima kaip tolimesnių tyrimų kryptis** — realiame diegime ji svarbesnė nei bet kuris gilusis modelis.

---

## 4. Gilusis mokymasis (4 metodai)

⚠️ **Visa šeima susiduria su ta pačia kliūtimi:** įvestis yra 36 nepriklausomi lenteliniai požymiai be sekos, be topologijos ir be krypties (žr. 0 skyrių).

### 4.1 Daugiasluoksnis perceptronas (MLP)

- **Principas:** pilnai sujungti sluoksniai su netiesinėmis aktyvacijomis.
- **IoT scenarijus:** vienintelė gilaus mokymosi architektūra, **prasminga lentelinei įvesčiai** — nedaro prielaidų apie eilę ar kaimynystę. **(aut.)**
- **Vertinimas:** kartu su TCN geriausias tikslumo ir kainos kompromisas ribotame įrenginyje; INT8 kvantavimas mažina modelį >90 % beveik neprarandant tikslumo `\cite{mazinani2026constrained}`.
- **Verdiktas:** ✅ **į kandidatus** — sąžiningas gilaus mokymosi atstovas, patikrinantis, ar sudėtingumas apsimoka.

### 4.2 1D-CNN

- **Principas:** konvoliucija slenkančiu langu; mokosi lokalių šablonų.
- **IoT scenarijus:** literatūroje populiaru srauto požymių vektorių traktuoti kaip 1D signalą.
- **Vertinimas:** ⚠️ **konvoliucija remiasi kaimynystės prasmingumu, o mūsų požymių eilė yra savavališka** — `HTTP` šalia `HTTPS` neturi tos pačios prasmės kaip gretimi signalo atskaitos taškai. Metodas veiktų, bet jo indukcinis šališkumas duomenims netinka. **(aut.)**
- **Verdiktas:** ⚠️ **rezervinis** — imamas tik jei MLP netikėtai nusileistų ansambliams ir liktų laiko.

### 4.3 LSTM / GRU

- **Principas:** rekurentiniai vartai, kaupiantys būseną per seką.
- **IoT scenarijus:** laiko priklausomybės sraute — C&C periodiškumas, lėtos atakos.
- **Vertinimas:** ❌ **sekos nėra.** Nėra `ts`, nėra eilės tarp įrašų, o kiekviena eilutė jau yra 10 arba 100 paketų lango agregatas. Seka jau „suvyniota" į požymius. **(aut.)**
- **Verdiktas:** ❌ **atmetama — duomenų struktūra.** Ne dėl resursų.

### 4.4 Transformer / GNN

- **Principas:** dėmesio mechanizmas per seką (Transformer); žinučių perdavimas grafe (GNN).
- **IoT scenarijus:** ilgos priklausomybės; tinklo topologija.
- **Vertinimas:** Transformer — ta pati sekos problema. GNN — **grafo sukonstruoti neįmanoma**, nes nėra nei mazgų identifikatorių, nei briaunų. Hibridinis GAT+BiGRU ant CICIoT2023 pasiekia F1 0,92, bet **120–180 ms Raspberry Pi 4** `\cite{nassef2026tinyml}` — nuo 2,4 iki 9 kartų virš 20–50 ms šliuzo biudžeto `\cite{sallam2026gap}`, kai XGBoost inferuoja per mikrosekundes.
- **Verdiktas:** ❌ **atmetama — duomenų struktūra ir delsa.** Du nepriklausomi argumentai.

---

## 5. Paskirstytas mokymasis (1 metodas)

### 5.1 Federated learning (FedAvg)

- **Principas:** modeliai mokomi lokaliai įrenginiuose, centralizuojami tik svoriai.
- **IoT scenarijus:** privatumas — srautas neišeina iš tinklo; svarbi ir realistiška kryptis.
- **Vertinimas:** ryšio kaina −20 % dešimties mazgų simuliacijoje `\cite{nassef2026tinyml}`. Bet **mūsų duomenyse nėra įrenginio identifikatoriaus**, todėl realistiško ne-IID padalijimo į klientus sukonstruoti neįmanoma — atsitiktinis padalijimas imituotų IID ir tirtų ne tą, ką reikia. **(aut.)**
- **Verdiktas:** ❌ **atmetama — duomenys neleidžia.** Apžvelgiama kaip kryptis, viena `tab:metodai` eilutė, ir pažymima, kad tai **mokymo schema, ne algoritmas**.

---

## 6. Skersinis sluoksnis: paaiškinamumas (ne paradigma)

**SHAP / LIME.** SHAP duoda nuoseklias globalias ir lokalias atributikas, LIME greitesnis ir lokalus; **abu reikalauja daug skaičiavimo ir riboja realaus laiko naudojimą** `\cite{mohale2025xai}`.

> **Sprendimas (aut.):** XAI šiame darbe yra **6 užduoties analizės įrankis, ne inferencijos grandinės dalis.** Todėl `tab:metodai` stulpelyje „Interpretuojamumas" skiriama „savaiminis" (medžiai) nuo „per XAI" (ansambliai, MLP) — antrasis reiškia papildomą kainą, kurios šliuze nemokame.

---

## 7. Rezultatas: KETURI fiksuoti metodai (T7, 2026-09-02)

**Sprendimas:** iš 6 kandidatų fiksuojami **4**. Pagrindinis užduoties detalumas — **8 kategorijos**.

| # | Metodas | Paradigma | Vaidmuo eksperimente |
|---|---|---|---|
| 1 | **Random Forest** | Prižiūrimas | Atskaitos modelis — garantuoja rezultatą, jei sudėtingesni nepasiteisins |
| 2 | **XGBoost** | Prižiūrimas | Laukiamas nugalėtojas; vienintelis tiesiogiai palyginamas su literatūra |
| 3 | **MLP** | Gilusis | Atsako 2.4 klausimą: ar sudėtingumas apsimoka lentelinei įvesčiai |
| 4 | **Autokoderis** | Neprižiūrimas | Vienintelis kelias prie zero-day; tikrina darbo prielaidą |

**Kodėl būtent šie.** Prižiūrimoje pusėje susidaro sudėtingumo gradientas: medžių ansamblis → stiprinimas → neuroninis tinklas. Tai leidžia atsakyti klausimą, kurį 2.4 poskyris kelia, bet be MLP paliktų neatsakytą. Autokoderis yra ne palyginimo dalyvis įprasta prasme, o darbo prielaidos patikra.

**Pagrindinis detalumas — 8 kategorijos.** Atitinka `etiketes.py` žodyną ir sutampa su `almahaqeri2026gradient` skelbiamu macro-F1 0,8903. ~20 paleidimų vietoj ~70. Dvejetainė ir 34 klasių formuluotės — tik geriausiam modeliui.

### Neteko vietos, nors tinkami (4)

| Metodas | Kodėl neteko |
|---|---|
| Sprendimų medis | Beveik nesiskiria nuo Random Forest; interpretuojamumą padengia SHAP |
| LightGBM | Beveik tapatus XGBoost — du stiprinimo metodai lentelėje nieko neprideda |
| **Isolation Forest** | ⚠️ Būtų buvęs pigus etalonas autokoderiui. Mokymas trunka minutes — **pridėti, jei 4 užduotyje liks laiko** |
| 1D-CNN | Atkartotų MLP atstovaujamą paradigmą su prastesniu indukciniu šališkumu |

### Atmesta su esminėmis priežastimis (8)

| Metodas | Priežastis | Tipas |
|---|---|---|
| SVM (RBF) | O(n²–n³) mokymas prie 2,43 mln. eilučių | **Resursai** |
| One-Class SVM | Tas pats | **Resursai** |
| k-NN | Inferencijos kaina auga su train aibe | **Delsa** |
| Naive Bayes | Nepriklausomumo prielaida paneigta patikra | **Prielaida** |
| LSTM / GRU | Sekos duomenyse nėra | **Duomenų struktūra** |
| Transformer | Ta pati sekos problema + delsa | **Duomenų struktūra** |
| GNN | Nėra mazgų ir briaunų | **Duomenų struktūra** |
| Federated learning | Nėra įrenginio identifikatoriaus | **Duomenų struktūra** |

**Už darbo ribų (2):** klasterizavimas · savimoka *(→ tolimesnių tyrimų kryptis)*.

### ⭐ Tik du atmetimai iš aštuonių — dėl resursų

Keturi atmesti dėl duomenų struktūros, vienas dėl pažeistos prielaidos, vienas dėl delsos. **Vadinasi, ketvertas būtų beveik tas pats ir turint serverį** — tai eina į 2.8 poskyrį.

### ⚠️ Palyginimo asimetrija, kurią reikia numatyti dabar

Trys prižiūrimi metodai klasifikuoja į 8 kategorijas; autokoderis duoda tik anomalijos įvertį. **Bendro macro-F1 stulpelio visiems keturiems sudaryti negalima.** 6 skyriaus suvestinė lentelė turės dvi dalis: prižiūrimi daugiaklasėje formuluotėje, autokoderis — dvejetainėje plius nematytų klasių bandymas.

## 8. Kas keliauja į T3 (`tab:metodai`)

Lentelė pildoma iš šio failo mechaniškai. Stulpeliai — pagal plano 4 skyrių; **17 eilučių** (visi apžvelgti metodai, ne tik kandidatai), kad matytųsi ir atmetimo pagrindas. Stulpelis „Šaltinis" pildomas iš čia esančių `\cite{}` ir **(aut.)** žymų — tuščių langelių būti negali.
