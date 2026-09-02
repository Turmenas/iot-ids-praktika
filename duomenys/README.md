# Duomenys

**Atnaujinta:** 2026-09-02 — ✅ **patikrinta realiame faile**, ne dokumentacijoje

Šis failas aprašo naudojamą duomenų rinkinį: šaltinį, licenciją, atsisiuntimą, požymius, etiketes ir spąstus. Kategorijų žodynas gyvena ne čia, o kode — `src/duomenys/etiketes.py`.

> **Patikros istorija.** 2026-09-01 versija buvo sudaryta iš straipsnio ir CIC puslapio, **neatidarius failo**, ir buvo klaidinga 8 stulpeliuose, eilučių skaičiuje ir etikečių registre. 2026-09-02 visi šio failo skaičiai gauti paleidus patikrą ant 63 CSV failų (45 mln. eilučių). Kur teiginys remiasi imtimi, o ne visu rinkiniu, tai pasakyta.

---

## Šaltinis

**CICIoT2023**, Kaggle leidimas „official IoT flow feature dataset".

| | |
|---|---|
| **Originalas** | Canadian Institute for Cybersecurity, University of New Brunswick |
| **Atsisiųsta iš** | `shadman1028/cic-iot2023-official-iot-flow-feature-dataset` |
| **Nuoroda** | https://www.kaggle.com/datasets/shadman1028/cic-iot2023-official-iot-flow-feature-dataset |
| **Oficiali CIC nuoroda** | https://www.unb.ca/cic/datasets/iotdataset-2023.html |
| **Vieta** | `duomenys/raw/archive/Merged01.csv` … `Merged63.csv` |
| **Dydis** | **8,7 GB**, 63 failai, **45 019 243 eilutės** |
| **Stulpelių** | **40** = 39 požymiai + `Label` |

**Cituojamas originalus straipsnis, ne veidrodis:**

> E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, A. A. Ghorbani. *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment.* Sensors 23(13):5941, 2023. DOI: 10.3390/s23135941

BibTeX raktas: `neto2023ciciot` (`ataskaita/saltiniai.bib`).

> ⚠️ **Ataskaitoje privaloma pasakyti, kad naudojamas ne kanoninis požymių rinkinys.** Straipsnis aprašo 46 požymius, darbe naudojami 39. Formuluotė — skyriuje „Kuo šis leidimas skiriasi".

**Licencija:** platinamas mokslo ir mokymo tikslams; naudojant privaloma cituoti originalų straipsnį.

## Atsisiuntimas

```bash
kaggle datasets download -d shadman1028/cic-iot2023-official-iot-flow-feature-dataset \
    --unzip -p duomenys/raw/
```

`duomenys/raw/` yra `.gitignore` — į repozitoriją nekeliama.

---

## Kuo šis leidimas skiriasi nuo oficialaus ⚠️

Oficialus CIC sąrašas — 46 požymiai. Šiame faile — **39**. Pašalinti **išvestiniai ir krypties** požymiai.

### Pašalinta (8)

| Požymis | Ką reiškė | Atkuriamas? |
|---|---|---|
| `flow_duration` | Srauto trukmė | **Ne.** Vienintelis tikras praradimas |
| `Srate` | Išsiunčiamų paketų dažnis | Ne — nėra krypties skirties |
| `Drate` | Gaunamų paketų dažnis | Ne — bet originale beveik visur 0 |
| `urg_count` | Paketų su URG vėliavėle | Ne |
| `Magnitue` | √(gaun. ilgių vid. + siunč. ilgių vid.) | Ne — reikia krypties |
| `Radius` | √(gaun. disp. + siunč. disp.) | Ne — reikia krypties |
| `Covariance` | cov(gaunamų, siunčiamų ilgių) | Ne — reikia krypties |
| `Weight` | gaun. paketų sk. × siunč. paketų sk. | Ne — reikia krypties |

### Pervadinta (1)

| Buvo | Tapo | Komentaras |
|---|---|---|
| `Duration` | **`Time_To_Live`** | ✅ Oficialiame rinkinyje `Duration` reiškė TTL — klastingiausias spąstas. Čia pavadinimas sąžiningas, **spąsto nebėra** |

### Pridėta (1)

`IGMP` — protokolo indikatorius.

**Suvestinė:** 46 − 8 + 1 = **39**.

### Ką tai kainuoja darbui

1. **Palyginamumas su literatūra sumažėja.** Beveik visi skelbiami CICIoT2023 rezultatai remiasi 46 požymiais; jų požymių atranka „46 → 23" čia neatkartojama, o dalis dažnai aukštai reitinguojamų požymių (`Magnitue`, `Covariance`, `Weight`) neegzistuoja. → eina į `tab:susije` stulpelį „Kas kelia abejonių" ir į 6 skyrių.
2. **`flow_duration` praradimas paliečia `tab:atakos`.** Kiekviena eilutė, kurios „matomi tinklo požymiai" mini srauto trukmę, nebeturi stulpelio. Pakaitalai: `Number`, `IAT`, `Rate`. Jautriausia — `DDOS-SLOWLORIS`.
3. **Krypties informacijos nebėra.** Srauto asimetrija — klasikinis DDoS ir botneto požymis — neišreiškiama.
4. **`Duration`/TTL spąstas dingo** — vienintelis teigiamas pokytis, ir reikšmingas.

---

## Pilnas stulpelių sąrašas (realaus failo eilės tvarka)

| # | Stulpelis | Reikšmė |
|---|---|---|
| 1 | `Header_Length` | Antraštės ilgis (vidurkis lange) |
| 2 | `Protocol Type` | Skaitinis protokolo kodas |
| 3 | `Time_To_Live` | **TTL** — buvęs `Duration` |
| 4 | `Rate` | Paketų dažnis sraute |
| 5–11 | `fin_flag_number`, `syn_flag_number`, `rst_flag_number`, `psh_flag_number`, `ack_flag_number`, `ece_flag_number`, `cwr_flag_number` | TCP vėliavėlės dalis lange (0–1) |
| 12–15 | `ack_count`, `syn_count`, `fin_count`, `rst_count` | Paketų su ta vėliavėle skaičius. ⚠️ `urg_count` **nebėra** |
| 16–22 | `HTTP`, `HTTPS`, `DNS`, `Telnet`, `SMTP`, `SSH`, `IRC` | Programų sluoksnio protokolas |
| 23–25 | `TCP`, `UDP`, `DHCP` | Transporto ir konfigūravimo protokolai |
| 26–30 | `ARP`, `ICMP`, **`IGMP`**, `IPv`, `LLC` | Kanalo ir tinklo sluoksnio protokolai |
| 31 | `Tot sum` | Paketų ilgių suma lange |
| 32–35 | `Min`, `Max`, `AVG`, `Std` | Paketo **ilgio** statistikos |
| 36 | `Tot size` | **= `AVG`** (žr. spąstus) |
| 37 | `IAT` | Vidutinis tarppaketinis intervalas (s) |
| 38 | `Number` | Paketų skaičius lange — **100** (94,95 %) arba **10** (4,92 %) |
| 39 | `Variance` | **= `Std`²** (žr. spąstus) |
| 40 | **`Label`** | Klasė. ⚠️ **Didžioji `L`** |

---

## ⚠️ Perteklinių požymių patikra (500 000 eilučių, `Merged01.csv`)

| Tapatybė | Rezultatas |
|---|---|
| **`Variance` = `Std`²** | ✅ **Galioja** — 0 nesutapimų iš 499 990 |
| **`Tot size` = `AVG`** | ✅ **Galioja tiksliai** — 500 000 iš 500 000, bitas į bitą |
| **`Tot sum` = `AVG` × `Number`** | ✅ **Galioja** — 0 nesutapimų iš 500 000 |
| ~~`Rate` = 1 / `IAT`~~ | ❌ **NEGALIOJA.** 305 006 nesutapimai iš 499 988 (61 %) |

**Dėl `Rate` ir `IAT`.** Pirmoje eilutėje jie sutapo iki paskutinio skaitmens, bet tai buvo atsitiktinumas. Realiai jie **labai stipriai koreliuoja, bet nėra tapatūs**: Pearson 0,961 (žali), 0,997 (log10); santykinės paklaidos mediana 0,017 %, bet 95-asis procentilis 8 %, o maksimumas 4233×. Vadinasi, **vieną iš jų šalinti galima, bet dėl koliniarumo, o ne dėl tapatumo** — ir tai reikia pasakyti būtent taip.

**Efektyvus požymių skaičius ≈ 36**, ne 39: `Variance`, `Tot size` ir `Tot sum` neneša naujos informacijos.

### ⭐ Kodėl to nepakanka koreliacijos filtrui

`Variance` = `Std`², bet jų **tiesinė** Pearson koreliacija tik **0,737**. Įprastas koreliacija grįstas požymių atrankos filtras (slenkstis 0,95) šios poros **nepašalins**, nors ryšys yra tikslus ir funkcinis.

> **Išvada 4 užduočiai:** perteklinius požymius šalinu **sąrašu, sąmoningai ir aprašydamas**, o ne pasikliaudamas automatiniu koreliacijos filtru. Šis pastebėjimas yra savarankiškas ir tinka ataskaitai.

---

## ⚠️ Duomenų kokybė: 9 sugadintos eilutės

**9 iš 63 failų baigiasi nutrūkusia eilute** (failas nutrūksta viduryje įrašo, be eilutės pabaigos):

`Merged42`, `Merged44`, `Merged46`, `Merged47`, `Merged48`, `Merged49`, `Merged50`, `Merged51`, `Merged52` — po vieną kiekviename.

**Pavojingiausia dalis: `pandas.read_csv` jas perskaito TYLIAI.** Jokios klaidos, jokio įspėjimo — nutrūkusi eilutė virsta įrašu su `NaN` reikšmėmis, tarp jų **`Label = NaN`**. `Merged42.csv` rasta 16 eilučių su bent vienu `NaN` (45 `NaN` iš viso).

**Privaloma įkėlimo grandinėje:**

```python
df = df.dropna(subset=["Label"])      # nutrukusios eilutes
df = df.dropna()                       # arba tikslingiau -- pagal pozymius
```

Be to `Label` stulpelyje atsiranda 35-a „klasė" — `NaN` — ir ji tyliai patenka į mokymą.

### Netaisyklingos skaitinės reikšmės (visas rinkinys, 45 019 243 eilutės)

| Problema | Eilučių | Dalis |
|---|---:|---:|
| `Rate` = **`Infinity`** | **991** | 0,0022 % |
| `Std` tuščias (`NaN`) | 677 | 0,0015 % |
| `Variance` tuščias (`NaN`) | 679 | 0,0015 % |
| `Number` < 10 (per trumpas langas) | 6 053 | 0,0134 % |
| Nutrūkusios eilutės | 9 | — |

**Priežastis viena.** Dalis langų turi vos 1–3 paketus. Tada `IAT` = 0, todėl `Rate` = `Infinity`; o iš vieno paketo neapskaičiuojamas nuokrypis, todėl `Std` ir `Variance` tušti. Baigtinis `Rate` maksimumas — 5 242 880.

**Kodėl tai svarbu.** `scikit-learn` atmeta `inf` su `ValueError: Input contains infinity or a value too large for dtype('float64')`. Tai nutiks **mokymo viduryje**, ne įkeliant — po to, kai jau bus praleistos minutės. XGBoost `NaN` toleruoja, `inf` — ne.

**Privaloma įkėlimo grandinėje:**

```python
import numpy as np
df = df.dropna(subset=["Label"])                  # 9 nutrukusios eilutes
df = df.replace([np.inf, -np.inf], np.nan)        # 991 Rate = Infinity
df = df.dropna()                                  # + 679 Std/Variance
```

Iš viso pašalinama ~1 700 eilučių iš 45 mln. (0,004 %) — nuostolis nereikšmingas, o alternatyva yra kritimas įpusėjus mokymui.

> **Atskirai apsvarstyti:** ar nešalinti visų `Number < 10` eilučių (6 053). Langas iš 1–3 paketų neneša tos pačios informacijos kaip iš 100, o `Number` pasiskirstymas dvimodis (100 — 94,95 %, 10 — 4,92 %). Sprendimas — 4 užduotyje, bet **sąmoningai ir aprašytas**.

---

## Etiketės

**34 klasės, patikrinta pilnu skenavimu per visus 63 failus.** Registras — **DIDŽIOSIOS raidės**.

> ⚠️ **Du skirtumai nuo dokumentacijos, ne vienas:**
> 1. Visos etiketės **didžiosiomis**: `DDOS-PSHACK_FLOOD`, ne `DDoS-PSHACK_Flood`.
> 2. **`BenignTraffic` → `BENIGN`.** Tai **ne** registro pokytis — pavadinimas kitas. `"BenignTraffic".upper()` duotų `BENIGNTRAFFIC`, ko faile **nėra**.
>
> Vadinasi, `.upper()` normalizavimas sutvarko **33 etiketes iš 34**, o `BENIGN` reikalauja atskiro atitikmens. Tai vienintelė tokia išimtis.

**Sprendimas `src/duomenys/etiketes.py`:**

```python
ALIASAI = {"BENIGNTRAFFIC": "BENIGN"}

def normalizuoti(s):
    s = s.str.strip().str.upper()
    return s.replace(ALIASAI)
```

Taip kodas veikia ir su šiuo, ir su kanoniniu leidimu.

### Klasių pasiskirstymas (visas rinkinys, 45 019 243 eilutės)

| Klasė | Eilučių | Dalis |
|---|---:|---:|
| `DDOS-ICMP_FLOOD` | 6 893 259 | 15,312 % |
| `DDOS-UDP_FLOOD` | 5 181 027 | 11,509 % |
| `DDOS-TCP_FLOOD` | 4 306 086 | 9,565 % |
| `DDOS-PSHACK_FLOOD` | 3 920 372 | 8,708 % |
| `DDOS-SYN_FLOOD` | 3 886 130 | 8,632 % |
| `DDOS-RSTFINFLOOD` | 3 872 808 | 8,603 % |
| `DDOS-SYNONYMOUSIP_FLOOD` | 3 445 659 | 7,654 % |
| `DOS-UDP_FLOOD` | 3 177 323 | 7,058 % |
| `DOS-TCP_FLOOD` | 2 558 256 | 5,683 % |
| `DOS-SYN_FLOOD` | 1 942 176 | 4,314 % |
| **`BENIGN`** | **1 051 373** | **2,335 %** |
| `MIRAI-GREETH_FLOOD` | 949 381 | 2,109 % |
| `MIRAI-UDPPLAIN` | 852 695 | 1,894 % |
| `MIRAI-GREIP_FLOOD` | 719 655 | 1,599 % |
| `DDOS-ICMP_FRAGMENTATION` | 433 157 | 0,962 % |
| `VULNERABILITYSCAN` | 357 583 | 0,794 % |
| `MITM-ARPSPOOFING` | 294 469 | 0,654 % |
| `DDOS-UDP_FRAGMENTATION` | 274 909 | 0,611 % |
| `DDOS-ACK_FRAGMENTATION` | 272 793 | 0,606 % |
| `DNS_SPOOFING` | 171 468 | 0,381 % |
| `RECON-HOSTDISCOVERY` | 128 677 | 0,286 % |
| `RECON-OSSCAN` | 93 970 | 0,209 % |
| `RECON-PORTSCAN` | 78 730 | 0,175 % |
| `DOS-HTTP_FLOOD` | 68 799 | 0,153 % |
| `DDOS-HTTP_FLOOD` | 27 597 | 0,061 % |
| `DDOS-SLOWLORIS` | 22 400 | 0,050 % |
| `DICTIONARYBRUTEFORCE` | 12 522 | 0,028 % |
| `BROWSERHIJACKING` | 5 630 | 0,013 % |
| `COMMANDINJECTION` | 5 168 | 0,011 % |
| `SQLINJECTION` | 5 022 | 0,011 % |
| `XSS` | 3 705 | 0,008 % |
| `BACKDOOR_MALWARE` | 3 078 | 0,007 % |
| `RECON-PINGSWEEP` | 2 161 | 0,005 % |
| `UPLOADING_ATTACK` | 1 196 | 0,003 % |
| *(sugadintos)* | 9 | — |

### ⭐ Du disbalansai, ne vienas

| Rodiklis | Reikšmė |
|---|---|
| Atakos : gerybinis srautas | **41,8 : 1** |
| **Didžiausia klasė : mažiausia klasė** | **5 764 : 1** (`DDOS-ICMP_FLOOD` vs `UPLOADING_ATTACK`) |

**Antrasis skaičius svarbesnis, ir jo iki šiol darbe nebuvo.** 41,8:1 paaiškina, kodėl netinka bendras tikslumas dvejetainei užduočiai. Bet **macro-F1 kritimą** aiškina 5 764:1 — septynios klasės turi mažiau nei 0,03 % duomenų, ir būtent jos „nutempia" macro vidurkį žemyn.

> Tai empiriškai paaiškina `almahaqeri2026gradient` rezultatą ant to paties rinkinio: XGBoost accuracy 99,59 %, bet macro-F1 tik **0,8903** (8 klasės). **Į ataskaitą eina abu santykiai**, ir 5 764:1 yra tas, kuris pagrindžia metrikos pasirinkimą.

**Pasekmės:** į ataskaitą — macro-F1, per-klasę metrikos ir sumaišymo matrica, ne accuracy. Balansavimas (SMOTE / klasių svoriai) — **tik ant train**, niekada ant test.

### Kategorija NEIŠVEDAMA iš etiketės pavadinimo

`Label.split("-")[0]` veikia tik daliai etikečių:

- **Be priešdėlio:** `SQLINJECTION`, `XSS`, `BROWSERHIJACKING`, `COMMANDINJECTION`, `BACKDOOR_MALWARE`, `UPLOADING_ATTACK`, `VULNERABILITYSCAN`, `DICTIONARYBRUTEFORCE`, `DNS_SPOOFING`, `BENIGN`
- **`MITM-ARPSPOOFING`** priešdėlis `MITM`, kategorija **Spoofing**
- **`VULNERABILITYSCAN`** priklauso `Recon`, nors priešdėlio neturi

Todėl žodynas laikomas kode: `src/duomenys/etiketes.py` su `patikrinti()` ir `assert`.

### Trys detalės filtrams

1. `DDOS-RSTFINFLOOD` — be pabraukimo prieš `FLOOD`, kitaip nei kitos `DDOS-*_FLOOD`.
2. `DDOS-SLOWLORIS` priskirtas DDoS, nors klasikiniu apibrėžimu tai mažo pralaidumo DoS. ⚠️ Be `flow_duration` ją aptikti sunkiausia, o duomenų tik 0,05 %.
3. Mirai kategorijoje **tik DDoS fazė** (`GREETH`, `GREIP`, `UDPPLAIN`) — verbavimo etiketės nėra.

---

## Spąstai (patikrinta 2026-09-02)

1. **`Label` didžiąja raide.** `df["label"]` mes `KeyError`.
2. **`BENIGN`, ne `BENIGNTRAFFIC`.** `.upper()` vienas nepakanka — reikia atitikmens.
3. **9 nutrūkusios eilutės, `pandas` jas skaito tyliai** → `dropna(subset=["Label"])` privalomas.
   **991 eilutė turi `Rate` = `Infinity`** → `replace([np.inf, -np.inf], np.nan)` privalomas, kitaip `scikit-learn` kris mokymo viduryje.
4. **`Variance` = `Std`²**, bet tiesinė koreliacija tik 0,737 — filtras nepagaus.
5. **`Tot size` = `AVG`**, ne „vieno paketo ilgis" kaip rašo CIC dokumentacija.
6. **`Tot sum` = `AVG` × `Number`** — perteklinis.
7. **`Rate` ≈ 1/`IAT`, bet NE tapatu** — koliniarūs, ne tapatūs.
8. **Pavadinimai su tarpais:** `Protocol Type`, `Tot sum`, `Tot size`. Kreiptis `df["Tot sum"]`, ne `df.Tot_sum`.
9. **`Std`, `Min`, `Max`, `AVG` — paketų ILGIŲ statistikos**, ne `IAT`.
10. **Krypties požymių nėra** — asimetrija neišreiškiama.

**Nebeaktualūs** *(buvo 2026-09-01 versijoje)*: `Duration`=TTL — pervadinta; `Magnitue` rašybos klaida — stulpelio nebėra; „`Tot sum` ≠ `Tot size`" — pakeista tikslesniu 5–6 punktu.

---

## Nėra laiko žymos — chronologinis skaidymas neįmanomas

`ts` stulpelio nėra (patikrinta).

**2026-09-02: antriniai rinkiniai atmesti.** Kryžminis patikrinimas tarp rinkinių — stipriausias argumentas prieš nutekėjimą — nebegalimas. Lieka:

| Variantas | Privalumas | Trūkumas |
|---|---|---|
| Stratifikuotas atsitiktinis + apribojimo įvardijimas | Sąžininga, atkartojama | Lieka pasikartojančių šablonų rizika |
| Skaidyti pagal `Merged*` failų eilę | Apytikslis laiko tęstinumas | Prielaida nepatvirtinta |
| **Nematytos atakų klasės testas** | Nereikia antro rinkinio; realistiškas zero-day matavimas | Netikrina pasiskirstymo poslinkio |

**Siūloma: 1 + 3.** Nematytos klasės testas tampa **pagrindine** apsauga nuo per optimistinio rezultato, todėl perkeliamas iš 6 užduoties į privalomą 5 užduoties dalį. **Užrakinti rugsėjo 8 d.**

---

## Patikros komandos

```bash
python -m src.duomenys.ikelimas patikra
python -m src.duomenys.etiketes
```

Rankinė patikra — `duomenys/raw/archive/`:

```python
import pandas as pd, numpy as np, glob
df = pd.read_csv(sorted(glob.glob("duomenys/raw/archive/*.csv"))[0], nrows=500_000)

assert len(df.columns) == 40 and "Label" in df.columns
print(np.allclose(df["Variance"], df["Std"]**2))          # True
print(np.allclose(df["Tot size"], df["AVG"]))             # True
print(np.allclose(df["Tot sum"], df["AVG"]*df["Number"])) # True
print(df["Label"].isna().sum())                           # nutrukusios eilutes
```

**Jei stulpelių ne 40 arba etikečių ne 34 — veidrodis pasikeitė: stabdyti ir perrašyti šį failą prieš tęsiant.**
