# Imties ataskaita

**GENERUOJAMA** - `python -m src.duomenys.ikelimas imtis`. Ranka neliesti.
**Sudaryta:** 2026-09-06 19:11  |  **SEED:** 42  |  **Riba klasei:** 100 000

## 1. Valymas (protokolo 5.2)

| Zingsnis | Eiluciu |
|---|---:|
| Perskaityta is CSV | 45 019 243 |
| Pasalinta nutrukusiu (tuscias `Label`) | 9 |
| Pasalinta su `inf` / trukstamomis reiksmemis | 991 |
| **Po valymo** | **45 018 243** |

## 2. Dublikatai (protokolo 5.4, 9 punktas)

| Rodiklis | Reiksme |
|---|---:|
| Eiluciu po valymo | 45 018 243 |
| Unikaliu eiluciu | 21 004 674 |
| **Dublikatu dalis** | **53,34 %** |
| Klasiu, kuriose riba 100 000 neisijunge | 13 is 34 |

## 3. Imtis

| Rodiklis | Reiksme |
|---|---:|
| Eiluciu imtyje | 2 425 937 |
| Dalis viso rinkinio (po valymo) | 5,39 % |
| Klasiu | 34 |
| Disbalansas (max/min) | 84:1 |
| `BENIGN` eiluciu (autokoderio mokymo aibe) | 100 000 |
| Stulpeliu | 40 |

## 4. Teorine tikslumo riba (protokolo 5.4 tikslinimas)

| Rodiklis | Reiksme |
|---|---:|
| Unikaliu pozymiu vektoriu | 2 420 616 |
| Is ju priestaringu (>1 etikete) | 5 114 |
| Dviprasmisku eiluciu | 10 435 (0,43 %) |
| Neisvengiamu klaidu | 5 321 |
| **Teorine tikslumo riba** | **99,78 %** |

> Riba galioja SIAM 39 pozymiu leidimui ir siai imciai. Aukstesnis uz
> ja rezultatas reiskia nutekejima, o ne sekme.

## 5. Patikros

- [x] Surinktu eiluciu skaicius sutampa su atrinktu maisu (2 425 937)
- [x] Dublikatu imtyje nera: `duplicated().sum()` = 0
- [x] Trukstamu reiksmiu nera: `isna().sum().sum()` = 0

Pasiskirstymas pagal klases - `imties_pasiskirstymas.csv`.
