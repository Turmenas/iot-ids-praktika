# 4 UŽDUOTIS — DI pagrįsto aptikimo sprendimo kūrimas

**Vykdymas:** rugsėjo 7–9 d. · **Atnaujinta:** 2026-09-07 vakare — išbraukta tai, kas atlikta
**Detalės apie atliktus darbus — `DARBO_ZURNALAS.md`.** Čia lieka tik tai, kas dar nepadaryta.

---

## 1. Būklė

| | |
|---|---|
| ✅ **T0–T7** | Įkėlimo grandinė · 36 požymiai · skaidymas · balansavimas · keturi modeliai · paleidiklis · **12 paleidimų atlikta** |
| ✅ **Derinimas** | Atliktas: 20 bandymų × 3 modeliai. Suderinti konfigai — `konfig/*_derintas.yaml` |
| 🔄 **Permokymas** | `mokyti_derintus.bat` — **dar nepaleistas** |
| ✅ **T8** | Prototipas — `prototipas.bat`. MLP jame pareikalaus permokymo (skalė) |
| ✅ **T9** | `04_sprendimas.tex` — 7 poskyriai, 3 lentelės, 2 paveikslai. **Sukompiliuota: 37 psl., 0 klaidų** |

**Turimi rezultatai** (val aibė, ties FPR ≤ 1 %): XGBoost **0,639** · Random Forest 0,604 · MLP 0,546 · autokoderis 0,220 *(FPR 1 %, aptinka 11,8 %)*.

---

## 2. Kas liko

### 2.1. Permokymas su suderintais parametrais — `mokyti_derintus.bat`

Derinimas atliktas; lieka permokyti ant **visos** aibės ir gauti operacinius taškus.

**Eiliškumas:** `mokyti_derintus.bat` → `slenkstis.bat` → `python -m src.eksperimentai.i_latex`

⚠️ Paieškos skaičiai gauti ant 400 000 eilučių, tad su dabartiniais (1,7 mln.) tiesiogiai nepalyginami — permokymas tai ir išsprendžia.

### 2.2. T8 — prototipas su vizualizacija

Srautas → požymiai → inferencija → signalas, Streamlit.

⚠️ **Blokuojantis dalykas: skalė neišsaugoma su modeliu.** `paleisti.py` sukuria `Skale`, bet jos neįrašo. MLP ir autokoderis be jos yra neveikiantys artefaktai. **Taisyti prieš prototipą.**

Prototipas turi naudoti **slenkstį**, ne argmax — kitaip demonstruotų 21–32 % klaidingų teigiamų.

**P1 prioritetas:** po 11:30 stabdomas, koks bebūtų — skyrius svarbiau.

### 2.3. T9 — `04_sprendimas.tex`

```
4.1. Sprendimo architektura                    (~0,7 psl.)
     --> pav: srautas -> pozymiai -> modelis -> signalas
4.2. Duomenu paruosimas                        (~1,2 psl.)
     --> tab:imtis; dublikatai 53,3 %; teorine riba 99,78 %
4.3. Pozymiai: 39 -> 36                        (~0,6 psl.)
     - kodel ne koreliacijos ir ne dispersijos filtras
4.4. Modeliu realizacija ir bendra sasaja      (~1,0 psl.)
     - kontraktas; autokoderio islyga
4.5. Klasiu disbalansas ir sprendimo slenkstis (~0,7 psl.)
     --> tab:slenkstis (jau sugeneruota)
4.6. Eksperimentu infrastruktura ir prototipas (~1,0 psl.)
     --> pav: prototipo ekrano nuotrauka
4.7. Apibendrinimas                            (~0,3 psl.)
```

**Apimties taikinys nemažinamas** — vienintelė likusi apimties rizika yra ~23 psl. teorijos prieš plonus 4–6 skyrius.

⚠️ **Pirmi paveikslai visame darbe.** `\includegraphics` niekur nenaudotas, tad nepatikrintas — pirmas paveikslas dedamas anksti, ne skyriaus pabaigoje.

---

## 3. Neuždaryti priėmimo kriterijai

- [ ] Hiperparametrai suderinti (protokolo 18 p.); geriausios reikšmės konfigūracijose
- [ ] Skalė išsaugoma su modeliu
- [ ] `\includegraphics` veikia; PDF kompiliuojasi be klaidų
- [ ] 4.7 poskyryje matomas užduoties rezultatas
- [ ] Automatinė patikra: kirilica · `\SI`/`\num` argumentai · `\section` skyriaus faile · dubliuoti `\label`

---

## 4. Likusios rizikos

| Rizika | Veiksmas |
|---|---|
| Derinimas nepagerina rezultatų | **Rašoma, kaip yra.** Numatytosios reikšmės tada yra rezultatas, ne aplaidumas |
| Prototipas suvalgo skyriaus laiką | T8 yra P1; po 11:30 stabdomas |
| Random Forest netelpa į atmintį | Derinimas turi pasiūlyti mažesnę konfigūraciją (`max_depth`) |
| Skyrius išplinta | Perviršis čia **nėra** problema — problema būtų priešinga |

---

## 5. Likučiai — rezervo laikas

- [ ] ⚠️ **Titulinio puslapio fakultetas ir vadovas** — atviras nuo rugs. 1 d., reikia sprendimo
- [ ] `houichi2025smartcity` metrikos (Wiley 403) — **terminas praėjo**; eilutė iš `tab:susije` išimtina
- [ ] `praktikos_planas.md` — pažymėti, kad 26–34 psl. norma neegzistuoja *(failo repozitorijoje nėra, tik Claude projekte)*
- [ ] Ištrinti: `ataskaita/bibtestas.tex` · `saltiniai.bib.bak` · `etiketes.py.bak` · `ikelimas.py.bak` · `src/modeliai/cnn.py`
- [ ] `duomenys/raw/archive.zip` — **~2,3 GB** atgaunama; CSV jau išpakuoti
- [ ] `ataskaita/skyriai/ciciot2023_pozymiai.md` — ne skyrius, perkelti į `duomenys/`
- [ ] `claude/` aplanke tik trys planai; `uzduotis_01_planas.md`, `praktikos_planas.md`, `kontekstas.md` tebėra tik Claude projekte

---

## 6. Kas keliauja į 5 užduotį

- **`test` aibė iki tol neliesta** — `paleisti.py` jos neįkelia be `--vertinimas test`
- **Palyginimas tik prie suderinto FPR**, ne prie argmax: argmax taškas pakeitė rikiuotę, tad tai metodinė klaida, ne smulkmena
- **Slenkstis parenkamas ant `val`**, taikomas `test` — perrinkti ant `test` būtų nutekėjimas
- **Nematytų klasių testas** — `DDOS-SLOWLORIS`, `RECON-PORTSCAN`, `DICTIONARYBRUTEFORCE`. Privaloma dalis
- **Dvejetainė ir 34 klasių formuluotės** — tik geriausiam prižiūrimam modeliui, palyginimui su `almahaqeri2026gradient`
- **Realistinis taikinys** — macro-F1 0,85–0,90 nepasiektas: turime 0,64 ties FPR biudžetu. Skirtumas paaiškinamas dublikatų šalinimu, ir tai rašoma atvirai
- **SHAP → 6 užduotis**
