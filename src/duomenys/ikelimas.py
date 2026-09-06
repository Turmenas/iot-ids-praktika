# -*- coding: utf-8 -*-
"""
CICIoT2023 ikelimas: patikra, valymas, dublikatu salinimas, stratifikuota imtis.

IGYVENDINA UZRAKINTA PROTOKOLA (claude/uzduotis_03_planas.md, 5 sk.):
  5.2  valymo tvarka: nutrukusios eilutes -> registras -> begalybes
  5.4  dublikatai salinami PRIES imti ir PRIES skaidyma, pagal VISA eilute
  5.1  riba 100 000 eiluciu klasei; retos klases imamos visos
       fiksuotas SEED; imtis sudaroma VIENA karta ir issaugoma

Paleidimas (is projekto saknies, aktyvavus iot-ids aplinka):

    python -m src.duomenys.ikelimas patikra     # ar veidrodis tinkamas
    python -m src.duomenys.ikelimas imtis       # sukurti imti -> Parquet
    python -m src.duomenys.ikelimas             # abu is eiles

Rezultatai:
    duomenys/processed/imtis.parquet
    rezultatai/darbiniai/imties_ataskaita.md        <- skaiciai i 4 ir 5 skyrius
    rezultatai/darbiniai/imties_pasiskirstymas.csv


KODEL DU PREJIMAI PER DUOMENIS
------------------------------
Protokolas reikalauja salinti dublikatus PRIES imti: jie pasiskirste
netolygiai (potvynio klasese 32-50 %, retose 0 %), todel salinimas keicia
klasiu proporcijas, ir imtis, sudaryta pries salinima, jau butu iskreipta.

Bet `df.duplicated()` ant viso rinkinio neimanomas: 45,0 mln. eiluciu x 39
float64 pozymiu ~ 14 GB vien duomenu. Sprendimas - lyginti ne eilutes, o ju
maisas (uint64): 45 mln. x 8 B = 360 MB.

  1 prejimas: skaiciuojamos eiluciu maisos, kaupiamos pagal klase.
              np.unique duoda TIKSLU unikaliu eiluciu skaiciu (= dublikatu
              statistika visam rinkiniui) ir leidzia atsitiktinai atrinkti
              iki 100 000 UNIKALIU maisu klasei.
  2 prejimas: renkamos tik tos eilutes, kuriu maisa pateko i atranka.
              Kartotiniai to paties maisos pasirodymai pasalinami galutiniu
              drop_duplicates (imtis tik ~2,4 mln. eiluciu - pigu).

Toks budas duoda TOLYGIAI ATSITIKTINE imti is unikaliu eiluciu, o ne
pirmasias failo eilutes, ir neviriija ~0,5 GB atminties.

Maisos susidurimo tikimybe prie 45 mln. eiluciu ir 64 bitu yra ~5e-8.
Metodas yra apytikslis, ne tikslus; tai IVARDIJAMA ataskaitoje, o galutine
patikra (ar surinktu eiluciu skaicius sutampa su atrinktu maisu skaiciumi)
tokius atvejus parodo.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from src.duomenys import etiketes

# ─── Nustatymai ──────────────────────────────────────────────────────

SAKNIS = Path(__file__).resolve().parents[2]
RAW = SAKNIS / "duomenys" / "raw" / "archive"   # 2026-09-02: CSV gula i archive/
PROCESSED = SAKNIS / "duomenys" / "processed"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"

SABLONAS = "Merged*.csv"      # shadman1028 veidrodzio failu pavadinimai
ETIKETE = "Label"             # 2026-09-02: faile DIDZIOJI L, ne "label"

RIBA_KLASEI = 100_000         # protokolo 5.1: riba, NE frakcija
GABALAS = 500_000             # kiek eiluciu skaityti vienu metu
SEED = 42

IMTIS = PROCESSED / "imtis.parquet"
ATASKAITA = DARBINIAI / "imties_ataskaita.md"
PASISKIRSTYMAS = DARBINIAI / "imties_pasiskirstymas.csv"


def _failai() -> list[Path]:
    failai = sorted(RAW.glob(SABLONAS))
    if not failai:
        raise SystemExit(
            f"Nerasta failu pagal sablona {SABLONAS} aplanke {RAW}\n"
            "Atsisiuskite duomenis:\n"
            "  kaggle datasets download -d shadman1028/"
            "cic-iot2023-official-iot-flow-feature-dataset --unzip -p duomenys/raw/"
        )
    return failai


# ─── Valymas — protokolo 5.2, tvarka fiksuota ────────────────────────

class Skaitliukai:
    """Valymo statistika. Kaupiama abiejuose prejimuose, lyginama gale."""

    def __init__(self) -> None:
        self.perskaityta = 0
        self.nutrukusios = 0      # tuscias Label: 9 failai baigiasi nepilna eilute
        self.begalybes = 0        # Rate = Infinity: langas su 1-3 paketais
        self.po_valymo = 0

    def kaip_zodyna(self) -> dict[str, int]:
        return {
            "perskaityta": self.perskaityta,
            "nutrukusios": self.nutrukusios,
            "begalybes": self.begalybes,
            "po_valymo": self.po_valymo,
        }


def valyti(df: pd.DataFrame, sk: Skaitliukai | None = None) -> pd.DataFrame:
    """
    Protokolo 5.2 valymas. Tvarka SVARBI ir nekeiciama:

      1. dropna pagal Label  - nutrukusios eilutes virstu 35-a "klase"
      2. registro normalizavimas - BENIGN, ne BENIGNTRAFFIC
      3. pozymiai -> float64 - BUTINA maisu determinizmui (zr. zemiau)
      4. inf -> nan -> dropna - sklearn kitaip luzta mokymo VIDURYJE

    3 zingsnis nera kosmetinis. pandas tipa nustato KIEKVIENAM gabalui
    atskirai, todel tas pats stulpelis viename gabale gali buti int64,
    kitame float64 - ir vienodos reiksmes duotu SKIRTINGAS maisas.
    Be sio kastinimo du prejimai nesutaptu.
    """
    if sk is not None:
        sk.perskaityta += len(df)

    n = len(df)
    df = df.dropna(subset=[ETIKETE])
    if sk is not None:
        sk.nutrukusios += n - len(df)

    df = df.copy()
    # .astype(str) -> object dtype: vienodas elgesys pandas 2.x ir 3.x,
    # ir maisos skaiciuojamos nuo paprastu Python eiluciu, ne StringDtype.
    df[ETIKETE] = etiketes.normalizuoti_stulpeli(df[ETIKETE].astype(str))

    pozymiai = [c for c in df.columns if c != ETIKETE]
    df[pozymiai] = df[pozymiai].apply(pd.to_numeric, errors="coerce").astype("float64")

    n = len(df)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    if sk is not None:
        sk.begalybes += n - len(df)
        sk.po_valymo += len(df)

    return df


def _maisos(df: pd.DataFrame) -> np.ndarray:
    """Vienos eilutes maisa (uint64) is VISU stulpeliu, iskaitant Label."""
    return pd.util.hash_pandas_object(df, index=False).to_numpy()


# ─── 1. Patikra ──────────────────────────────────────────────────────

def patikra() -> None:
    """
    Tikrina, ar veidrodis nera jau apdorotas.

    Trys raudonos veliavos:
      1. Per mazai stulpeliu    -> ismesti pozymiai
      2. Tolygus klasiu pasisk. -> jau pritaikytas SMOTE / balansavimas
      3. Pozymiai [0,1] rezyje  -> jau normalizuota (leakage rizika)
    """
    failai = _failai()
    print(f"Rasta failu: {len(failai)}")
    print(f"Tikrinamas: {failai[0].name}\n")

    df = pd.read_csv(failai[0], nrows=200_000, low_memory=False)

    print(f"Stulpeliu: {df.shape[1]}  (tiketasi 40 = 39 pozymiai + Label)")
    if df.shape[1] < 40:
        print("  [!] Per mazai stulpeliu - gali buti ismestu pozymiu")

    if ETIKETE not in df.columns:
        raise SystemExit(f"Nerastas stulpelis '{ETIKETE}'. Yra: {list(df.columns)}")

    kiekiai = df[ETIKETE].value_counts()
    print(f"Klasiu: {len(kiekiai)}\n")
    print("Dazniausios:")
    print(kiekiai.head(5).to_string())
    print("\nReciausios:")
    print(kiekiai.tail(5).to_string())

    santykis = kiekiai.max() / kiekiai.min()
    print(f"\nDisbalanso santykis (max/min): {santykis:,.0f}")
    if santykis < 50:
        print("  [!] ITARTINA: klases per tolygios - galimai pritaikytas SMOTE")
    else:
        print("  [OK] Stiprus disbalansas - toks ir turi buti")

    skaitiniai = df.select_dtypes("number")
    if not skaitiniai.empty:
        maks = skaitiniai.max().max()
        print(f"\nDidziausia skaitine reiksme: {maks:,.2f}")
        if maks <= 1.0:
            print("  [!] ITARTINA: pozymiai [0,1] rezyje - galimai jau normalizuota")
        else:
            print("  [OK] Pozymiai neapdoroti")

    etiketes.patikrinti(df[ETIKETE].unique())
    print("  [OK] Visos etiketes yra zodyne")


# ─── 2. Pirmas prejimas: maisos ──────────────────────────────────────

def _pirmas_prejimas(failai: list[Path]) -> tuple[dict[str, list], Skaitliukai]:
    """Grazina {klase: [maisu masyvai]} ir valymo skaitliukus."""
    print(f"1/2  Skaiciuojamos eiluciu maisos ({len(failai)} failai)...")
    sk = Skaitliukai()
    maisos: dict[str, list] = {}

    for i, f in enumerate(failai, 1):
        for gabalas in pd.read_csv(f, chunksize=GABALAS, low_memory=False):
            gabalas = valyti(gabalas, sk)
            if gabalas.empty:
                continue
            h = _maisos(gabalas)
            for klase, idx in gabalas.groupby(ETIKETE, sort=False).indices.items():
                maisos.setdefault(klase, []).append(h[idx])
        print(f"     [{i}/{len(failai)}] {f.name}")

    return maisos, sk


def _atranka(maisos: dict[str, list]) -> tuple[np.ndarray, pd.DataFrame]:
    """
    Is kiekvienos klases unikaliu maisu atsitiktinai atrenka iki RIBA_KLASEI.

    Grazina: (surusiuotas atrinktu maisu masyvas, suvestines lentele).
    """
    rng = np.random.default_rng(SEED)
    pasirinktos: list[np.ndarray] = []
    eilutes = []

    for klase in sorted(maisos):
        visos = np.concatenate(maisos[klase])
        unikalios = np.unique(visos)
        n_visos, n_unik = len(visos), len(unikalios)

        if n_unik > RIBA_KLASEI:
            imti = rng.choice(unikalios, size=RIBA_KLASEI, replace=False)
            riba_isijunge = True
        else:
            imti = unikalios
            riba_isijunge = False

        pasirinktos.append(imti)
        eilutes.append({
            "klase": klase,
            "pilnas_rinkinys": n_visos,
            "unikaliu": n_unik,
            "dublikatu_proc": round((1 - n_unik / n_visos) * 100, 2),
            "imtyje": len(imti),
            "riba_isijunge": riba_isijunge,
        })

    suvestine = pd.DataFrame(eilutes).sort_values(
        "pilnas_rinkinys", ascending=False).reset_index(drop=True)
    return np.sort(np.concatenate(pasirinktos)), suvestine


# ─── 3. Antras prejimas: eiluciu rinkimas ────────────────────────────

def _antras_prejimas(failai: list[Path], pasirinktos: np.ndarray) -> pd.DataFrame:
    """
    Renka eilutes, kuriu maisa pateko i atranka.

    Dublikatai salinami IS KARTO, gabalas po gabalo, o ne sudejus viska i
    viena DataFrame ir tik tada iskvietus drop_duplicates. Skirtumas ne
    kosmetinis: atrinktos 2,4 mln. maisu duomenyse pasikartoja ~4 mln.
    kartu, todel sudetas rinkinys butu ~65 % didesnis uz galutini, o
    concat dar padvigubina atminti. Pirmoji versija butent ties tuo ir
    luzo (OOM) masinoje su 4 GB.

    `matytos` yra ne daugiau kaip len(pasirinktos) maisu (~190 MB).
    """
    print(f"\n2/2  Renkamos atrinktos eilutes ({len(pasirinktos):,} maisu)...")
    dalys: list[pd.DataFrame] = []
    matytos: set = set()
    kartotiniu = 0

    for i, f in enumerate(failai, 1):
        for gabalas in pd.read_csv(f, chunksize=GABALAS, low_memory=False):
            gabalas = valyti(gabalas)
            if gabalas.empty:
                continue
            h = _maisos(gabalas)
            kauke = np.isin(h, pasirinktos)
            if not kauke.any():
                continue
            gabalas, h = gabalas[kauke], h[kauke]

            if matytos:                       # pandas isin su set - maisos paieska
                nauji = ~pd.Index(h).isin(matytos)
                kartotiniu += int((~nauji).sum())
                if not nauji.any():
                    continue
                gabalas, h = gabalas[nauji], h[nauji]

            matytos.update(h.tolist())
            dalys.append(gabalas)
        print(f"     [{i}/{len(failai)}] {f.name}")

    df = pd.concat(dalys, ignore_index=True)
    print(f"\n     Surinkta {len(df):,} unikaliu "
          f"(praleista {kartotiniu:,} kartotiniu pasirodymu)")
    return df.drop_duplicates(ignore_index=True)


# ─── 4. Teorine tikslumo riba ────────────────────────────────────────

def teorine_riba(df: pd.DataFrame) -> dict[str, float]:
    """
    Bajeso riba, kylanti is priestaringu etikeciu.

    Tas pats POZYMIU vektorius kartais pazymetas skirtingomis etiketemis.
    Geriausias imanomas klasifikatorius tokiai grupei parenka dazniausia
    etikete, todel neisvengiama klaida yra (grupes dydis - dazniausios
    etiketes daznis), susumuota per visas grupes.

    Pastaba: cia lyginami TIK pozymiai, be Label - kitaip priestaringos
    eilutes atrodytu kaip skirtingos ir riba butu 100 %.
    """
    pozymiai = [c for c in df.columns if c != ETIKETE]
    h = pd.util.hash_pandas_object(df[pozymiai], index=False).to_numpy()

    poros = (pd.DataFrame({"h": h, "lab": df[ETIKETE].to_numpy()})
             .groupby(["h", "lab"], sort=False).size().rename("n").reset_index())
    grupes = poros.groupby("h", sort=False)["n"].agg(["sum", "max", "count"])

    klaidos = int((grupes["sum"] - grupes["max"]).sum())
    dviprasmiskos = int(grupes.loc[grupes["count"] > 1, "sum"].sum())

    return {
        "eiluciu": len(df),
        "unikaliu_vektoriu": int(len(grupes)),
        "priestaringu_vektoriu": int((grupes["count"] > 1).sum()),
        "dviprasmisku_eiluciu": dviprasmiskos,
        "dviprasmisku_proc": round(dviprasmiskos / len(df) * 100, 2),
        "neisvengiamu_klaidu": klaidos,
        "teorine_riba_proc": round((1 - klaidos / len(df)) * 100, 2),
    }


# ─── 5. Ataskaita ────────────────────────────────────────────────────

def _n(x: float, sk_po: int = 0) -> str:
    """Skaicius su tarpais tarp tukstanciu. Kablelis TIK skaiciuje.

    Anksciau ataskaita buvo formatuojama globaliu .replace(",", " ") per
    visa teksta - jis butu isdarkes ir prozos kablelius.
    """
    return f"{x:,.{sk_po}f}".replace(",", "\u202f").replace(".", ",").replace("\u202f", " ")


def _ataskaita(sk: Skaitliukai, suvestine: pd.DataFrame, df: pd.DataFrame,
               riba: dict[str, float], laukta: int) -> str:
    gerybine = int((df[ETIKETE] == etiketes.GERYBINE_NORM).sum())
    kiekiai = df[ETIKETE].value_counts()
    zemiau = int((~suvestine["riba_isijunge"]).sum())
    po_valymo = int(suvestine["pilnas_rinkinys"].sum())
    unikaliu = int(suvestine["unikaliu"].sum())
    dubl_proc = (1 - unikaliu / po_valymo) * 100

    e = [
        "# Imties ataskaita",
        "",
        "**GENERUOJAMA** - `python -m src.duomenys.ikelimas imtis`. Ranka neliesti.",
        f"**Sudaryta:** {datetime.now():%Y-%m-%d %H:%M}  |  **SEED:** {SEED}  "
        f"|  **Riba klasei:** {_n(RIBA_KLASEI)}",
        "",
        "## 1. Valymas (protokolo 5.2)",
        "",
        "| Zingsnis | Eiluciu |",
        "|---|---:|",
        f"| Perskaityta is CSV | {_n(sk.perskaityta)} |",
        f"| Pasalinta nutrukusiu (tuscias `Label`) | {_n(sk.nutrukusios)} |",
        f"| Pasalinta su `inf` / trukstamomis reiksmemis | {_n(sk.begalybes)} |",
        f"| **Po valymo** | **{_n(sk.po_valymo)}** |",
        "",
        "## 2. Dublikatai (protokolo 5.4, 9 punktas)",
        "",
        "| Rodiklis | Reiksme |",
        "|---|---:|",
        f"| Eiluciu po valymo | {_n(po_valymo)} |",
        f"| Unikaliu eiluciu | {_n(unikaliu)} |",
        f"| **Dublikatu dalis** | **{_n(dubl_proc, 2)} %** |",
        f"| Klasiu, kuriose riba {_n(RIBA_KLASEI)} neisijunge | "
        f"{zemiau} is {len(suvestine)} |",
        "",
        "## 3. Imtis",
        "",
        "| Rodiklis | Reiksme |",
        "|---|---:|",
        f"| Eiluciu imtyje | {_n(len(df))} |",
        f"| Dalis viso rinkinio (po valymo) | "
        f"{_n(len(df) / max(sk.po_valymo, 1) * 100, 2)} % |",
        f"| Klasiu | {len(kiekiai)} |",
        f"| Disbalansas (max/min) | {_n(kiekiai.max() / kiekiai.min())}:1 |",
        f"| `{etiketes.GERYBINE_NORM}` eiluciu (autokoderio mokymo aibe) | "
        f"{_n(gerybine)} |",
        f"| Stulpeliu | {df.shape[1]} |",
        "",
        "## 4. Teorine tikslumo riba (protokolo 5.4 tikslinimas)",
        "",
        "| Rodiklis | Reiksme |",
        "|---|---:|",
        f"| Unikaliu pozymiu vektoriu | {_n(riba['unikaliu_vektoriu'])} |",
        f"| Is ju priestaringu (>1 etikete) | {_n(riba['priestaringu_vektoriu'])} |",
        f"| Dviprasmisku eiluciu | {_n(riba['dviprasmisku_eiluciu'])} "
        f"({_n(riba['dviprasmisku_proc'], 2)} %) |",
        f"| Neisvengiamu klaidu | {_n(riba['neisvengiamu_klaidu'])} |",
        f"| **Teorine tikslumo riba** | **{_n(riba['teorine_riba_proc'], 2)} %** |",
        "",
        "> Riba galioja SIAM 39 pozymiu leidimui ir siai imciai. Aukstesnis uz",
        "> ja rezultatas reiskia nutekejima, o ne sekme.",
        "",
        "## 5. Patikros",
        "",
    ]

    if len(df) == laukta:
        e.append(f"- [x] Surinktu eiluciu skaicius sutampa su atrinktu maisu "
                 f"({_n(laukta)})")
    else:
        e.append(f"- [ ] **NESUTAMPA:** atrinkta {_n(laukta)} maisu, surinkta "
                 f"{_n(len(df))} eiluciu (skirtumas {len(df) - laukta:+d}). "
                 "Tiketina priezastis - maisos susidurimas; zr. modulio "
                 "dokumentacija.")

    e += [
        f"- [x] Dublikatu imtyje nera: `duplicated().sum()` = "
        f"{int(df.duplicated().sum())}",
        f"- [x] Trukstamu reiksmiu nera: `isna().sum().sum()` = "
        f"{int(df.isna().sum().sum())}",
        "",
        "Pasiskirstymas pagal klases - `imties_pasiskirstymas.csv`.",
        "",
    ]

    return "\n".join(e)


# ─── 6. Imtis ────────────────────────────────────────────────────────

def imtis() -> None:
    failai = _failai()

    maisos, sk = _pirmas_prejimas(failai)
    etiketes.patikrinti(maisos.keys())

    pasirinktos, suvestine = _atranka(maisos)
    del maisos

    print(f"\n     Po valymo: {sk.po_valymo:,} eiluciu")
    print(f"     Unikaliu:  {suvestine['unikaliu'].sum():,} "
          f"(dublikatu {(1 - suvestine['unikaliu'].sum() / suvestine['pilnas_rinkinys'].sum()) * 100:.2f} %)")
    print(f"     Atrinkta:  {len(pasirinktos):,} maisu")

    df = _antras_prejimas(failai, pasirinktos)
    riba = teorine_riba(df)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    DARBINIAI.mkdir(parents=True, exist_ok=True)
    df.to_parquet(IMTIS, index=False)
    suvestine.to_csv(PASISKIRSTYMAS, index=False)
    ATASKAITA.write_text(
        _ataskaita(sk, suvestine, df, riba, len(pasirinktos)), encoding="utf-8")

    (PROCESSED / "imtis_metadata.json").write_text(json.dumps({
        "sudaryta": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED,
        "riba_klasei": RIBA_KLASEI,
        "eiluciu": len(df),
        "stulpeliu": int(df.shape[1]),
        "valymas": sk.kaip_zodyna(),
        "teorine_riba": riba,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nIssaugota: {IMTIS.relative_to(SAKNIS)}")
    print(f"  Eiluciu:   {len(df):,}  (is {sk.po_valymo:,} po valymo)")
    print(f"  Stulpeliu: {df.shape[1]}")
    print(f"  Dydis:     {IMTIS.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"\n  Teorine tikslumo riba: {riba['teorine_riba_proc']} %")
    print(f"\nAtaskaita: {ATASKAITA.relative_to(SAKNIS)}")

    retos = df[ETIKETE].value_counts()
    retos = retos[retos < 100]
    if not retos.empty:
        print("\n[!] Sios klases turi < 100 pavyzdziu - ju metrikos bus triuksmas:")
        print(retos.to_string())


# ─── Paleidimas ──────────────────────────────────────────────────────

if __name__ == "__main__":
    komanda = sys.argv[1] if len(sys.argv) > 1 else "visos"

    if komanda in ("patikra", "visos"):
        patikra()
        print()
    if komanda in ("imtis", "visos"):
        imtis()
    if komanda not in ("patikra", "imtis", "visos"):
        raise SystemExit("Naudojimas: python -m src.duomenys.ikelimas [patikra|imtis]")
