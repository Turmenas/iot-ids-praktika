# 6 UŽDUOTIS — DI metodų efektyvumo palyginimas

**Tikslų planas**
**Sudaryta:** 2026 m. rugsėjo 9 d. vakare
**Vykdymas:** rugsėjo 10 d. (ketvirtadienis), po 5 užduoties T8–T9
**Rezultatas:** `ataskaita/skyriai/06_palyginimas.tex` (~4 psl.), viena generuojama suvestinė lentelė, 1–2 paveikslai

> ✅ **ĮVYKDYTA 2026-09-09 vakare**, anksčiau nei planuota. Ką pakeitė vykdymas — 11 skyriuje failo gale.

---

## 0. Esmė: ši užduotis yra rašymo, ne matavimo darbas ⭐

**Naujų eksperimentų nereikia. `test` aibė daugiau neliečiama.** Visi 6 užduočiai reikalingi skaičiai jau išmatuoti ir guli failuose:

| Ko reikia 6 skyriui | Kur jau yra | Kada gauta |
|---|---|---|
| Kokybės metrikos ties FPR biudžetu, 3 seed'ai | `slenkscio_taskai_test.csv` | 5 užd. T2 |
| Metrikos ties argmax | `rezultatai.csv` (18 `test` eilučių) | 5 užd. T2 |
| Veikimo rodikliai (delsa CPU, dydis, mokymo laikas) | `rezultatai.csv`, `veikimas.tex` | 4 užd., permatuota 09-08 |
| Per-klasę ir per-kategoriją aptikimas | `perklasiu_test.csv`, `klaidu_tipai_test.csv` | 5 užd. T4, T5 |
| Nematytų klasių testas (3 klasės × 4 stulpeliai) | 5 užd. T5 išvestis | 5 užd. T5 |
| Dvejetainė ir 34 klasių formuluotės | `rezultatai.csv` | 5 užd. T6 |
| Slenksčio kreivės (FPR ↔ aptikimas) | `xgboost_slenkstis.csv`, `autokoderio_slenkstis.csv` | 4 užd. |
| Prognozė, su kuria lyginama | `sprendimu_matrica.csv` (4,70 · 3,55 · 3,25) | 3 užd. |

**Vienintelis naujas skaičiavimas — SHAP (T5), ir jis P1.** Jis daromas ant `val`, ne `test`.

> **Iš to seka dienos taisyklė:** jei kuriam nors teiginiui prireikia skaičiaus, kurio nėra lentelėje aukščiau — pirma klausiama, ar teiginys būtinas, ir tik po to, ar dėl jo verta liesti duomenis. **Ne todėl, kad tingu, o todėl, kad `test` panaudota vieną kartą ir tas skaičius yra vienintelis sąžiningas.**

---

## 1. Kuo 6 skyrius skiriasi nuo 5-ojo ⭐

Rizika akivaizdi: abu skyriai apie tuos pačius keturis modelius ir tuos pačius skaičius. Jei skirtis nebus laikoma galvoje, 6 skyrius taps 5-ojo santrauka.

| 5 skyrius atsako | 6 skyrius atsako |
|---|---|
| **Kiek** kiekvienas modelis pasiekė | **Kuris** ir **kam** tinkamiausias |
| Ką rodo metrikos, klaidos, nematytos klasės | Kokie **kompromisai** tarp metodų ir kur jie lūžta |
| Ar rezultatai patikimi | Ar **prognozės pasitvirtino** ir ką tai sako apie metodiką |

**Praktinė išraiška:** 5 skyriuje lentelė pateikia modelį eilutėje ir metriką stulpelyje. 6 skyriuje eilutė yra **kompromiso ašis** (kokybė, klaidingi teigiami, dydis, apibendrinimas nematytoms klasėms), o turinys — kas kurioje ašyje laimi ir kokia to kaina. Ta pati medžiaga, kita ašis.

**Skyrius baigiasi rekomendacija.** Tai vienintelė vieta visame darbe, kur pasakoma, ką rinktis — ir vadovui tai bus svarbiausia pastraipa.

---

## 2. Tikslai

| Nr. | Tikslas | Išmatuojamas rezultatas | Prior. |
|---|---|---|---|
| **T1** | **Suvestinė lentelė** — dvi dalys (prižiūrimi 8 kategorijose · autokoderis dvejetainėje), **ties FPR biudžetu** | `tab:suvestine`, **generuojama** iš CSV | **P0** |
| **T2** | **Kompromisų analizė** — kokybė vs. dydis, kokybė vs. klaidingi teigiami, argmax vs. biudžetas | 6.3 tekstas + `pav:kompromisai` | **P0** |
| **T3** | **Prognozių patikra** — sprendimų matrica prieš matavimą; kur pataikė, kur ne | 6.4, ~0,5 psl. | **P0** |
| **T4** | **Zero-day verdiktas** — autokoderio hipotezė: pasiteisino ar ne | 6.5, remiasi 5 užd. T5 | **P0** |
| **T5** | Požymių svarba (SHAP, `mohale2025xai`) — ant `val`, XGBoost | `pav:shap` arba lentelė | P1 |
| **T6** | **Rekomendacija** — kuris metodas kuriam scenarijui | 6.7, ~0,4 psl. | **P0** |
| **T7** | Parašyti `06_palyginimas.tex` | 7 poskyriai, ~4 psl., 0 klaidų | **P0** |

**Ne šios užduoties tikslai:** nauji eksperimentai, permokymas, Isolation Forest, `test` aibės pjūviai, kurių dar nėra. Įvadas (`00_ivadas.tex`) ir išvados (`07_isvados.tex`) — rugsėjo 11 d. užbaigimo darbas, ne 6 užduotis.

---

## 3. Kas jau užrakinta — nekvestionuojama ⭐

Šie sprendimai priimti anksčiau ir 6 skyriuje tik taikomi:

1. **Lyginama ties suderintu FPR biudžetu (≤ 1 %), ne ties argmax.** Argmax rikiuotė kitokia (RF pirmauja) ir tai **savarankiškas radinys**, pateikiamas kaip toks — bet pagrindinė lentelė yra biudžeto lentelė. *(4 užd. 45 radinys, patvirtinta `test` aibėje 5 užd. 69 radinys.)*
2. **Suvestinė lentelė turi dvi dalis.** Autokoderis neduoda 8 kategorijų sprendimo, tad bendro macro-F1 stulpelio visiems keturiems nėra. *(Numatyta 2 užd. 2.8, įgyvendinta 3 užd. matricoje ir 4 užd. kode — 6 skyriuje ketvirtą kartą.)*
3. **Skirtumas tikras tik viršijęs paleidimų sklaidą** (`dietterich1998tests`); formalus testas neatliekamas ir kodėl — vienu sakiniu.
4. **Į skyrių — kas išmatuota, kas pasirinkta, kokia to pasekmė.** Kaip prie to priėjau, ką bandžiau, kur suklydau — į žurnalą. *(Vadovo taisyklė, rugs. 3 d.)*
5. **Apimtis yra grindys, ne stabdis.** Vienintelė likusi apimties rizika — ~23 psl. teorijos prieš plonus 4–6 skyrius.

---

## 4. Skyriaus struktūra

```
6. DI metodu efektyvumo palyginimas
   6.1. Palyginimo pagrindas                        (~0,3 psl.)
        - kodel ties FPR biudzetu, ne ties argmax
        - kodel lentele turi dvi dalis
   6.2. Suvestine                                   (~0,8 psl.)
        --> tab:suvestine (generuojama)
   6.3. Kompromisai                                 (~1,0 psl.)
        --> pav:kompromisai
        - kokybe vs. dydis: XGBoost 45 MB pries RF 670 MB
        - kokybe vs. klaidingi teigiami: rikiuotes apsivertimas
        - priziurimas vs. neprziurimas
   6.4. Prognozes ir matavimas                      (~0,5 psl.)
        - sprendimu matrica 4,70 / 3,55 / 3,25 pries matavima
        - kur prognoze neatlaike: RF resursu balas
   6.5. Nematytos atakos: hipotezes verdiktas       (~0,7 psl.)
        --> tab:nematytos (is 5 uzd.)
   6.6. Pozymiu svarba                              (~0,4 psl.)  [P1]
   6.7. Rekomendacija                               (~0,4 psl.)
```

**Iš viso ~4,1 psl.**

---

## 5. Kas turi būti 6.7 rekomendacijoje ⭐

Tai vienintelis poskyris, kurio turinio dar nėra nė viename faile. Jį verta apmąstyti prieš rašant kitus, nes jis pasako, kam viskas buvo.

Rekomendacija turi būti **sąlyginė, ne viena**:

| Scenarijus | Ką siūlyti | Kuo remiantis |
|---|---|---|
| Kraštinis šliuzas, 1 % klaidingų teigiamų biudžetas | **XGBoost su slenksčiu 0,975** | Geriausias ties biudžetu; 45 MB; telpa į delsą su trijų eilių atsarga |
| Griežtai ribota atmintis | XGBoost mažesnė konfigūracija (200 medžių, 7,4 MB) | Derinimo paieška: −0,9 % kokybės, −20 MB |
| Random Forest | **Nerekomenduojamas** | 670 MB, `joblib.load` nužudomas 3,9 GB mašinoje; ties biudžetu pralaimi |
| Autokoderis kaip vienintelis metodas | **Nerekomenduojamas** | Ties 1 % FPR aptinka ~12 % atakų; nematytoms klasėms pralaimi prižiūrimam |
| Autokoderis kaip papildoma pakopa | Svarstytinas | PR-AUC 0,996 — **rikiuoja gerai, sprendžia blogai** |

⚠️ **Kartu turi būti pasakyta, ko rekomendacija neapima:** vieno rinkinio rezultatai neapibendrinami (`eren2026drift`), o zero-day teiginys galioja **naujai tos pačios šeimos klasei**, ne naujai atakos rūšiai (5 užd. 74 radinio išlyga).

---

## 6. Trys dalykai, kurių 5 skyriuje nebuvo vietos, o 6-ame yra ⭐

Nesugalvoti — jie liko atviri po 5 užduoties ir natūraliai priklauso palyginimui:

1. **Random Forest `test` aibėje peržengė biudžetą (1,02 %).** 5 skyriuje tai patikros Nr. 4 radinys. 6 skyriuje tai **argumentas prieš RF** ir kartu bendresnis teiginys: *τ*, parinktas ties pačiu biudžeto kraštu, į nepriklausomą aibę persikelia be atsargos.
2. **Detalumo kaina.** 8 kategorijos prieš 34 klases: modelis 2,5× didesnis, mokymas 3,6× ilgesnis, delsa 3,0× didesnė, o macro-F1 **mažesnis**. Tai kompromiso ašis, kurios 5 skyrius neanalizuoja — jis tik pateikia skaičius palyginimui su literatūra.
3. **Aptikimas per kategorijas svyruoja 37–100 %.** Bendras „88,4 %" yra svertinis vidurkis, kurį lemia DDoS. Palyginimo skyriuje tai reiškia, kad **modelių rikiuotė pagal vieną skaičių slepia, kad visi trys prasčiausiai atpažįsta tas pačias tris kategorijas** — o tai jau ne modelio, o duomenų savybė.

---

## 7. Laiko biudžetas — rugsėjo 10 d.

| Laikas | Darbas | Prior. |
|---|---|---|
| — | *(pirma užbaigti 5 užd. T8 ir T9)* | **P0** |
| 1,0 val. | **T1:** suvestinės lentelės skriptas (`src/eksperimentai/suvestine.py`) → `tab:suvestine` | **P0** |
| 0,7 val. | **T2:** `pav:kompromisai` — kokybė ties biudžetu prieš modelio dydį (log ašis) | **P0** |
| 1,5 val. | **T7:** 6.2–6.5 tekstas aplink lenteles | **P0** |
| 0,5 val. | **T6:** 6.7 rekomendacija | **P0** |
| 0,5 val. | **T5:** SHAP, jei liko laiko | P1 |
| 0,3 val. | 6.1 — rašomas paskutinis | P1 |
| 0,4 val. | `build.ps1` · patikros · commit · `DARBO_ZURNALAS.md` · `STRUKTURA.md` | **P0** |

**Dienos minimumas:** `tab:suvestine` generuojama, 6.2–6.5 ir 6.7 parašyti, PDF kompiliuojasi.

---

## 8. Priėmimo kriterijai

- [x] **Nė vieno naujo `test` paleidimo.** `rezultatai.csv` po dienos turi tas pačias 45 eilutes — *patikrinta `md5sum` prieš ir po*
- [x] `tab:suvestine` **generuojama** skriptu, ne rašoma ranka; dvi dalys su išnaša, kad sumos tarpusavyje nepalyginamos
- [x] Pagrindinis palyginimas — **ties FPR biudžetu**; argmax rikiuotė pateikta atskirai ir įvardyta kaip radinys
- [x] 6.4 pasako **ir tai, kur prognozė neatlaikė** (RF resursų balas 4/5 prieš 638 MB), ne tik kur pataikė
- [x] 6.5 pasako **verdiktą** — autokoderio hipotezė nepasitvirtino — su išlyga apie tos pačios šeimos klases
- [x] **6.7 yra sąlyginė rekomendacija**, ne vienas pavadinimas; įvardyta, ko ji neapima
- [x] Skyriuje **nėra proceso pasakojimo** — nei klaidų, nei dvejonių, nei „kaip priėjau"
- [x] Automatinė patikra: kirilica 0 · `\SI`/`\num` argumentai sutikrinti · `\section` skyriaus faile 0 · dubliuotų `\label` nėra
- [x] Kompiliuojasi: **0 klaidų, 0 neišspręstų nuorodų** *(konteineryje, be `biblatex`; Windows pusėje dar netikrinta)*
- [x] `DARBO_ZURNALAS.md` · `STRUKTURA.md` · commit

---

## 9. Rizikos

| Rizika | Ženklas | Veiksmas |
|---|---|---|
| ⭐ **6 skyrius tampa 5-ojo santrauka** | Pastraipa, kurią galima perkelti į 5 skyrių nieko nepakeitus | 1 sk. skirtis: 5 sk. — kiek, 6 sk. — kuris ir kam. Kiekvienai pastraipai klausti, kurioje ji vieta |
| **Pagunda paleisti „dar vieną pjūvį"** | Naujas `--vertinimas test` paleidimas | 0 sk. taisyklė. `test` panaudota vieną kartą |
| Rekomendacija per švelni („priklauso nuo konteksto") | Nė vienas metodas neįvardytas | 5 sk. lentelė — sąlygos konkrečios, atsakymai irgi |
| SHAP suvalgo dieną | Praėjo valanda, grafiko nėra | P1. Po 40 min. stabdoma, poskyris 6.6 iškrenta |
| Skyrius per plonas (< 3 psl.) | — | Perviršis čia **nėra** problema |

---

## 10. Po 6 užduoties — rugsėjo 11 d. užbaigimas

Ne šios užduoties darbas, bet verta matyti, kas lieka:

- `00_ivadas.tex` ir `07_isvados.tex` — rašomi paskutiniai
- ⚠️ **Titulinio puslapio fakultetas ir vadovas** — atviras nuo rugs. 1 d., **reikia sprendimo**
- `README.md` paleidimo instrukcija, atkartojamumo patikra iš švarios aplinkos
- Smulkūs likučiai: `bibtestas*.tex` ir `cnn.py` ištrinti · `metadata.json` pildyti arba išbraukti iš `STRUKTURA.md` · `ciciot2023_pozymiai.md` perkelti į `duomenys/` · `houichi` eilutė iš `tab:susije`
- `claude/` — `uzduotis_01_planas.md`, `praktikos_planas.md`, `kontekstas.md` tebėra tik Claude projekte

**Grafikas eina 7 dienomis į priekį pradinio plano** (6 užd. buvo numatyta rugs. 17 d.).

---

## 11. Kuo vykdymas skyrėsi nuo plano *(įrašyta po fakto, 2026-09-09)*

Trys nukrypimai, visi į tą pačią pusę — pigiau ir anksčiau, nei planuota.

**1. SHAP pakeistas informacijos prieaugiu (gain).** Planas T5 numatė SHAP ant `val`. Vykdant paaiškėjo, kad gain skaičiuojamas **iš paties modelio**, todėl duomenų neatidaro visai — tai griežtesnis „vieno prėjimo" taisyklės laikymasis nei planuota, o ne nusileidimas. `mohale2025xai` cituojamas ten, kur pasakoma, ko gain **neduoda**: krypties ir sąveikų. Poskyris 6.6 iš P1 tapo P0, nes tai vienintelė vieta darbe, kur interpretuojamumo kriterijus (15 % svorio) apskritai matuojamas.

**2. Skyrius išėjo ~6 psl. vietoj ~4.** Perviršį duoda 6.3 (keturios kompromisų ašys) ir 6.7 (keturios sąlyginės rekomendacijos). Netrumpinta sąmoningai: nuo 4 skyriaus galioja taisyklė, kad apimtis yra grindys, o ne stabdis.

**3. Rasta ir ištaisyta neišspręsta nuoroda, kurios plane nebuvo.** Kompiliuojant visą darbą paaiškėjo, kad `lenteles/perklase.tex` nurodo `tab:rezultatai`, o skyrius naudoja `tab:rezultatai_test`. Kode klaidos nebuvo — `klaidos.py` jau pataisytas — bet lentelė buvo sugeneruota **prieš** tą taisymą. Pergeneravus: 0 neišspręstų nuorodų. Pamoka įrašyta į `STRUKTURA.md` spąstus: **pataisius generatorių reikia pergeneruoti išvestį.**

**Ko plane nebuvo, bet pasirodė vertinga:** suvestinės skripte įrašyta kontrolinė patikra — autokoderio aptikimas skaičiuojamas iš per-kategorijų pjūvio, o tuo pačiu būdu suskaičiuotas XGBoost aptikimas turi sutapti su slenksčio failu. Sutampa iki penkto skaitmens, tad abu failai tikrai iš to paties paleidimo.
