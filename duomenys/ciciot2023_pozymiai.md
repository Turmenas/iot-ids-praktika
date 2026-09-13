# CICIoT2023 požymiai — patikrintas sąrašas

**Sudaryta:** 2026 m. rugsėjo 1 d.
**Šaltiniai:** originalaus straipsnio 4 lentelė (Neto et al., *Sensors* 23(13):5941) ir realaus `MERGED_CSV` failo antraštė.

> Šis failas — darbinė nuoroda 1, 4 ir 5 užduotims. Į ataskaitą tiesiogiai nekeliauja, bet iš jo rašomas 4 skyriaus požymių aprašas.

---

## Kiek požymių: 46, ne 47

Neatitikimas, dėl kurio internete cituojama tai 46, tai 47, išspręstas:

| Šaltinis | Kiek | Ką skaičiuoja |
|---|---|---|
| Straipsnio 4 lentelė | 47 | 46 požymiai **+ `ts` (laiko žyma)** |
| `MERGED_CSV` antraštė | 47 stulpeliai | 46 požymiai **+ `label`** |

**`ts` į paskelbtus CSV failus nepateko.** Todėl: **46 požymiai + `label`**. Ataskaitoje rašyti „46 požymiai", nurodant, kad straipsnio lentelėje jų 47, nes įtraukta laiko žyma, kurios paskelbtoje versijoje nėra.

---

## Pilnas stulpelių sąrašas (CSV eilės tvarka)

| # | Stulpelis | Reikšmė |
|---|---|---|
| 1 | `flow_duration` | Srauto trukmė |
| 2 | `Header_Length` | Antraštės ilgis |
| 3 | `Protocol Type` | IP, UDP, TCP, IGMP, ICMP, Unknown (sveikieji skaičiai) |
| 4 | `Duration` | **Time-to-live (TTL)** — ne trukmė |
| 5 | `Rate` | Paketų siuntimo dažnis sraute |
| 6 | `Srate` | Išsiunčiamų paketų dažnis |
| 7 | `Drate` | Gaunamų paketų dažnis |
| 8 | `fin_flag_number` | FIN vėliavėlės reikšmė |
| 9 | `syn_flag_number` | SYN vėliavėlės reikšmė |
| 10 | `rst_flag_number` | RST vėliavėlės reikšmė |
| 11 | `psh_flag_number` | PSH vėliavėlės reikšmė |
| 12 | `ack_flag_number` | ACK vėliavėlės reikšmė |
| 13 | `ece_flag_number` | ECE vėliavėlės reikšmė |
| 14 | `cwr_flag_number` | CWR vėliavėlės reikšmė |
| 15 | `ack_count` | Paketų su ACK skaičius sraute |
| 16 | `syn_count` | Paketų su SYN skaičius sraute |
| 17 | `fin_count` | Paketų su FIN skaičius sraute |
| 18 | `urg_count` | Paketų su URG skaičius sraute |
| 19 | `rst_count` | Paketų su RST skaičius sraute |
| 20 | `HTTP` | Ar programų sluoksnio protokolas yra HTTP |
| 21 | `HTTPS` | Ar HTTPS |
| 22 | `DNS` | Ar DNS |
| 23 | `Telnet` | Ar Telnet |
| 24 | `SMTP` | Ar SMTP |
| 25 | `SSH` | Ar SSH |
| 26 | `IRC` | Ar IRC |
| 27 | `TCP` | Ar transporto sluoksnio protokolas yra TCP |
| 28 | `UDP` | Ar UDP |
| 29 | `DHCP` | Ar DHCP |
| 30 | `ARP` | Ar kanalo sluoksnio protokolas yra ARP |
| 31 | `ICMP` | Ar tinklo sluoksnio protokolas yra ICMP |
| 32 | `IPv` | Ar IP |
| 33 | `LLC` | Ar LLC |
| 34 | `Tot sum` | Paketų ilgių **suma** sraute |
| 35 | `Min` | Mažiausias paketo ilgis sraute |
| 36 | `Max` | Didžiausias paketo ilgis sraute |
| 37 | `AVG` | Vidutinis paketo ilgis sraute |
| 38 | `Std` | Paketo ilgio standartinis nuokrypis |
| 39 | `Tot size` | **Vieno paketo** ilgis |
| 40 | `IAT` | Laiko skirtumas su ankstesniu paketu |
| 41 | `Number` | Paketų skaičius sraute |
| 42 | `Magnitue` | √(gaunamų paketų ilgių vid. + siunčiamų paketų ilgių vid.) |
| 43 | `Radius` | √(gaunamų ilgių dispersija + siunčiamų ilgių dispersija) |
| 44 | `Covariance` | Gaunamų ir siunčiamų paketų ilgių kovariacija |
| 45 | `Variance` | Gaunamų ilgių dispersija / siunčiamų ilgių dispersija |
| 46 | `Weight` | Gaunamų paketų sk. × siunčiamų paketų sk. |
| 47 | `label` | Atakos klasė (33 atakos + `BenignTraffic`) |

---

## Spąstai, į kuriuos lengva įkliūti

**1. `Duration` yra TTL, ne trukmė.** Srauto trukmė — `flow_duration`. Pavadinimai klaidina, o abu stulpeliai yra skaitiniai ir abu „veikia" modelyje, todėl klaida nepasirodys kaip klaida — tik kaip prastesnis rezultatas ir neteisingas paaiškinimas ataskaitoje.

**2. `Magnitue` — su rašybos klaida.** Rinkinyje būtent `Magnitue`, be `d`. Kode rašyti taip, kaip yra; ataskaitos tekste galima minėti „magnitude", pažymint, kad rinkinyje pavadinimas su korektūros klaida.

**3. `Tot sum` ≠ `Tot size`.** `Tot sum` — visų paketų ilgių suma sraute; `Tot size` — vieno paketo ilgis. Painiojant gaunami visiškai skirtingi dydžiai.

**4. Pavadinimų stilius nevienodas.** Dalis su pabraukimais (`flow_duration`, `Header_Length`, `ack_count`), dalis su **tarpais** (`Protocol Type`, `Tot sum`, `Tot size`). Kode kreipiantis `df["Tot sum"]`, ne `df.Tot_sum`. Verta iš karto normalizuoti:

```python
df.columns = df.columns.str.strip().str.replace(" ", "_")
```

— bet tada ataskaitoje pavadinimus rašyti originalius, o normalizavimą paminėti metodikoje.

**5. `Std`, `Min`, `Max`, `AVG` yra paketų ILGIŲ statistikos**, ne `IAT` statistikos. `IAT` sklaidos stulpelio nėra — jei jos reikia (pvz., C&C periodiškumui aptikti), ją reikia išvesti patiems slenkančiame lange.

**6. `Protocol Type` enumeracija ribota:** IP, UDP, TCP, IGMP, ICMP, Unknown. GRE, kuriuo remiasi Mirai `GREIP`/`GREETH` potvyniai, patenka į `Unknown`.

---

## Ko rinkinyje NĖRA — ir ką tai reiškia

**Nėra IP ir MAC adresų, prievadų numerių, srauto identifikatorių.** Kiekviena eilutė yra paketų sekos požymiai be dalyvių tapatybės. Pasekmės:

- Neįmanomi požymiai, reikalaujantys agregavimo per srautus: unikalių taikinių skaičius skenavimo metu, tapatybių skaičius iš vieno šaltinio (Sybil), jungčių į konkretų prievadą dažnis.
- Protokolų žymos (`Telnet`, `SSH`, `HTTP`) yra vienintelis pakaitalas prievadų analizei.
- Įrenginio tapatybės pokytis (klonavimas) neaptinkamas iš principo.

**Nėra laiko žymos (`ts`).** ⚠️ **Tai keičia 4 užduoties planą.**

Plane numatyta „duomenų padalijimas chronologinis, ne atsitiktinis — kitaip gaunamas temporal leakage". **Be `ts` stulpelio chronologinis padalijimas paskelbtoje versijoje neįmanomas.** Galimi variantai, sprendžiami rugsėjo 8–9 d.:

| Variantas | Privalumas | Trūkumas |
|---|---|---|
| Skaidyti pagal `part-*` failų eilę | Failai generuoti nuosekliai, todėl apytiksliai atitinka laiko tvarką | Prielaida nepatvirtinta dokumentacijoje |
| Stratifikuotas atsitiktinis skaidymas + aiškus apribojimo įvardijimas | Sąžininga, atkartojama | Lieka pasikartojančių šablonų nutekėjimo rizika |
| Grįžti prie originalių PCAP arba per-atakos CSV iš CIC serverio | Laiko dimensija atkuriama | Daug papildomo darbo, netelpa į grafiką |
| Kryžminis patikrinimas ant kito rinkinio (TON\_IoT) | Stipriausias argumentas prieš nutekėjimą | Reikia antro rinkinio paruošimo |

**Rekomendacija:** 2 variantas + 4 variantas. Atsitiktinis stratifikuotas skaidymas su atviru apribojimo įvardijimu, o kaip atsvara — kryžminis patikrinimas ant TON\_IoT. Tai tiksliai atitinka `reddy2026datasets` rekomendaciją (cross-dataset validation vietoj neapdoroto tikslumo) ir 1 varianto nepatvirtintą prielaidą paverčia nereikalinga.

---

## Patikra po atsisiuntimo

```python
import pandas as pd
df = pd.read_csv("duomenys/raw/Merged01.csv", nrows=200_000)

print(len(df.columns))                    # laukiama 47 (46 + label)
print(list(df.columns))                   # sutikrinti su lentele aukščiau
print("ts" in df.columns)                 # laukiama False
print(df["label"].value_counts())         # turi būti STIPRIAI nesubalansuota
print(df[["Duration", "flow_duration"]].describe().T)   # skirtingos skalės?
print(df["Drate"].describe())             # ar ne visur 0 — zinoma problema
```

Jei stulpelių pavadinimai skiriasi nuo šio sąrašo — **veidrodis pakeistas**, ir `tab:atakos` požymių stulpelį reikia taisyti prieš rašant tekstą.

---

# Etiketės: 33 atakos + gerybinis srautas

`label` stulpelyje yra **34 reikšmės** — 33 atakų tipai ir `BenignTraffic`.

## Pilnas sąrašas pagal kategorijas

**DDoS (12)**
`DDoS-ACK_Fragmentation` · `DDoS-HTTP_Flood` · `DDoS-ICMP_Flood` · `DDoS-ICMP_Fragmentation` · `DDoS-PSHACK_Flood` · `DDoS-RSTFINFlood` · `DDoS-SlowLoris` · `DDoS-SYN_Flood` · `DDoS-SynonymousIP_Flood` · `DDoS-TCP_Flood` · `DDoS-UDP_Flood` · `DDoS-UDP_Fragmentation`

**DoS (4)**
`DoS-HTTP_Flood` · `DoS-SYN_Flood` · `DoS-TCP_Flood` · `DoS-UDP_Flood`

**Recon (5)**
`Recon-HostDiscovery` · `Recon-OSScan` · `Recon-PingSweep` · `Recon-PortScan` · `VulnerabilityScan`

**Web-based (6)**
`Backdoor_Malware` · `BrowserHijacking` · `CommandInjection` · `SqlInjection` · `Uploading_Attack` · `XSS`

**Brute force (1)**
`DictionaryBruteForce`

**Spoofing (2)**
`DNS_Spoofing` · `MITM-ArpSpoofing`

**Mirai (3)**
`Mirai-greeth_flood` · `Mirai-greip_flood` · `Mirai-udpplain`

**Gerybinis**
`BenignTraffic`

## ⚠️ Kategorijos NEIŠVEDAMOS iš etiketės pavadinimo

Akivaizdus sprendimas — `label.split("-")[0]` — **veikia tik 24 iš 34 etikečių**. Nepavyksta:

- **10 etikečių neturi kategorijos priešdėlio:** `SqlInjection`, `XSS`, `BrowserHijacking`, `CommandInjection`, `Backdoor_Malware`, `Uploading_Attack`, `VulnerabilityScan`, `DictionaryBruteForce`, `DNS_Spoofing`, `BenignTraffic`
- **`MITM-ArpSpoofing`** turi priešdėlį `MITM`, bet kategorija yra **Spoofing** — skaidymas duotų neegzistuojančią klasę
- **`VulnerabilityScan`** priklauso `Recon` kategorijai, nors priešdėlio `Recon-` neturi (kitos keturios turi)

Todėl 8 klasių (7 kategorijos + gerybinis) žymėjimui **būtinas aiškus žodynas**, ne eilučių apdorojimas:

```python
KATEGORIJOS = {
    # DDoS (12)
    "DDoS-ACK_Fragmentation": "DDoS",   "DDoS-HTTP_Flood": "DDoS",
    "DDoS-ICMP_Flood": "DDoS",          "DDoS-ICMP_Fragmentation": "DDoS",
    "DDoS-PSHACK_Flood": "DDoS",        "DDoS-RSTFINFlood": "DDoS",
    "DDoS-SlowLoris": "DDoS",           "DDoS-SYN_Flood": "DDoS",
    "DDoS-SynonymousIP_Flood": "DDoS",  "DDoS-TCP_Flood": "DDoS",
    "DDoS-UDP_Flood": "DDoS",           "DDoS-UDP_Fragmentation": "DDoS",
    # DoS (4)
    "DoS-HTTP_Flood": "DoS",            "DoS-SYN_Flood": "DoS",
    "DoS-TCP_Flood": "DoS",             "DoS-UDP_Flood": "DoS",
    # Recon (5)
    "Recon-HostDiscovery": "Recon",     "Recon-OSScan": "Recon",
    "Recon-PingSweep": "Recon",         "Recon-PortScan": "Recon",
    "VulnerabilityScan": "Recon",
    # Web-based (6)
    "Backdoor_Malware": "Web",          "BrowserHijacking": "Web",
    "CommandInjection": "Web",          "SqlInjection": "Web",
    "Uploading_Attack": "Web",          "XSS": "Web",
    # Brute force (1)
    "DictionaryBruteForce": "BruteForce",
    # Spoofing (2)
    "DNS_Spoofing": "Spoofing",         "MITM-ArpSpoofing": "Spoofing",
    # Mirai (3)
    "Mirai-greeth_flood": "Mirai",      "Mirai-greip_flood": "Mirai",
    "Mirai-udpplain": "Mirai",
    # Gerybinis
    "BenignTraffic": "Benign",
}

# Patikra po ikelimo — privaloma
trukstamos = set(df["label"].unique()) - set(KATEGORIJOS)
assert not trukstamos, f"Nezinomos etiketes: {trukstamos}"
```

`assert` čia svarbus: jei veidrodis turi kitokį rašybos variantą, klaida pasirodys iš karto, o ne kaip tyliai dingusi klasė.

## Klasių pasiskirstymas

| | Eilučių | Dalis |
|---|---|---|
| `BenignTraffic` | ~1 098 195 | ~2,4 % |
| Visos atakos | ~45 588 385 | ~97,6 % |
| **Iš viso** | **~46 686 580** | |

Atakų ir gerybinio srauto santykis **~42:1** — realiame tinkle jis priešingas. Tai reiškia, kad:

- **Bendras tikslumas (accuracy) šiame rinkinyje beveik bevertis.** Modelis, viską žymintis kaip ataką, gautų ~97,6 %.
- Klaidingai teigiamų (FPR) rodiklis atrodys dirbtinai geras, nes gerybinių pavyzdžių, kuriuose galima suklysti, yra mažai.
- Į ataskaitą turi eiti **macro-F1, per-klasę metrikos ir sumaišymo matrica**, o ne accuracy.

Šie skaičiai patys keliauja į 1.3 poskyrį (`tab:aprepis` aptarimas) ir 5 skyriaus metodiką.

## Trys detalės, kurias verta žinoti iš anksto

1. **`DDoS-RSTFINFlood`** — be pabraukimo prieš `Flood`, skirtingai nei visos kitos `DDoS-*_Flood` etiketės. Klasikinė vieta apsirikti rašant filtrą.
2. **`DDoS-SlowLoris`** priskirtas DDoS kategorijai, nors SlowLoris klasikiniu apibrėžimu yra mažo pralaidumo DoS ataka. Ataskaitoje verta tai paminėti, kad neatrodytų kaip mano klaida.
3. **Mirai kategorijoje yra tik DDoS fazė** (`greeth`, `greip`, `udpplain`) — **verbavimo fazės (Telnet žodyno atakos) atskiros etiketės nėra**. Artimiausias atitikmuo — `DictionaryBruteForce`, bet jis nesusietas su Mirai. Todėl `tab:atakos` eilutė „Mirai tipo botneto verbavimas" pažymėta `dal.`, ne `taip`.
