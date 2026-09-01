"""
CICIoT2023 duomenu ikelimas: patikra, stratifikuota imtis, Parquet.

Kodel reikia imties: pilnas rinkinys yra ~46,7 mln. eiluciu / 13 GB.
Su pandas i RAM netilps, o 2,5 savaites projektui to ir nereikia.

Paleidimas (is projekto saknies, aktyvavus iot-ids aplinka):

    python -m src.duomenys.ikelimas patikra     # ar veidrodis tinkamas
    python -m src.duomenys.ikelimas imtis       # sukurti imti -> Parquet
    python -m src.duomenys.ikelimas             # abu is eiles

Rezultatas: duomenys/processed/ciciot2023_imtis.parquet
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# ─── Nustatymai ──────────────────────────────────────────────────────

SAKNIS = Path(__file__).resolve().parents[2]
RAW = SAKNIS / "duomenys" / "raw"
PROCESSED = SAKNIS / "duomenys" / "processed"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"

SABLONAS = "Merged*.csv"      # shadman1028 veidrodzio failu pavadinimai
ETIKETE = "label"

FRAKCIJA = 0.05               # 5 % nuo kiekvienos klases
MIN_EILUCIU = 5_000           # bet ne maziau nei tiek retoms klasems
GABALAS = 500_000             # kiek eiluciu skaityti vienu metu
SEED = 42


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

    df = pd.read_csv(failai[0], nrows=200_000)

    print(f"Stulpeliu: {df.shape[1]}  (tiketasi ~47)")
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

    # Disbalanso santykis: tikrame CICIoT2023 jis turi buti didziulis
    santykis = kiekiai.max() / kiekiai.min()
    print(f"\nDisbalanso santykis (max/min): {santykis:,.0f}")
    if santykis < 50:
        print("  [!] ITARTINA: klases per tolygios - galimai pritaikytas SMOTE")
    else:
        print("  [OK] Stiprus disbalansas - toks ir turi buti")

    # Skaitiniu pozymiu skale
    skaitiniai = df.select_dtypes("number")
    if not skaitiniai.empty:
        maks = skaitiniai.max().max()
        print(f"\nDidziausia skaitine reiksme: {maks:,.2f}")
        if maks <= 1.0:
            print("  [!] ITARTINA: pozymiai [0,1] rezyje - galimai jau normalizuota")
        else:
            print("  [OK] Pozymiai neapdoroti")


# ─── 2. Klasiu skaiciavimas (pirmas prejimas) ────────────────────────

def _klasiu_kiekiai(failai: list[Path]) -> pd.Series:
    """
    Suskaiciuoja klasiu pasiskirstyma visame rinkinyje.

    Skaitomas TIK `label` stulpelis (usecols) - todel 13 GB perziura
    uztrunka minutes, o ne desimtis minuciu, ir netelpa i RAM problemos nera.
    """
    print("1/2  Skaiciuojamos klases (skaitomas tik 'label' stulpelis)...")
    dalys = []
    for i, f in enumerate(failai, 1):
        s = pd.read_csv(f, usecols=[ETIKETE])[ETIKETE]
        dalys.append(s.value_counts())
        print(f"     [{i}/{len(failai)}] {f.name}")
    return pd.concat(dalys).groupby(level=0).sum().sort_values(ascending=False)


# ─── 3. Imtis (antras prejimas) ──────────────────────────────────────

def imtis() -> None:
    failai = _failai()
    kiekiai = _klasiu_kiekiai(failai)

    print(f"\nIs viso eiluciu: {kiekiai.sum():,}")
    print(f"Klasiu: {len(kiekiai)}\n")

    # Kiek imti is kiekvienos klases: FRAKCIJA, bet retoms - ne maziau MIN_EILUCIU
    tikslai = {}
    for etikete, n in kiekiai.items():
        tikslai[etikete] = min(n, max(int(n * FRAKCIJA), min(MIN_EILUCIU, n)))

    # Kiekvienai klasei sava frakcija - kad retos klases nedingtu
    frakcijos = {e: tikslai[e] / kiekiai[e] for e in kiekiai.index}

    print("2/2  Renkama imtis...")
    dalys = []
    for i, f in enumerate(failai, 1):
        for gabalas in pd.read_csv(f, chunksize=GABALAS):
            for etikete, grupe in gabalas.groupby(ETIKETE, observed=True):
                fr = frakcijos.get(etikete, FRAKCIJA)
                if fr >= 1.0:
                    dalys.append(grupe)
                else:
                    n = max(1, int(len(grupe) * fr))
                    dalys.append(grupe.sample(n=n, random_state=SEED))
        print(f"     [{i}/{len(failai)}] {f.name}")

    rezultatas = pd.concat(dalys, ignore_index=True)

    # Issaugojimas
    PROCESSED.mkdir(parents=True, exist_ok=True)
    kelias = PROCESSED / "ciciot2023_imtis.parquet"
    rezultatas.to_parquet(kelias, index=False)

    # Ataskaita
    galutiniai = rezultatas[ETIKETE].value_counts()
    DARBINIAI.mkdir(parents=True, exist_ok=True)
    suvestine = pd.DataFrame({
        "pilnas_rinkinys": kiekiai,
        "imtis": galutiniai,
    }).fillna(0).astype(int)
    suvestine["dalis_proc"] = (suvestine["imtis"] / suvestine["pilnas_rinkinys"] * 100).round(2)
    suvestine.to_csv(DARBINIAI / "imties_pasiskirstymas.csv")

    dydis_mb = kelias.stat().st_size / 1024 / 1024
    print(f"\nIssaugota: {kelias}")
    print(f"  Eiluciu:   {len(rezultatas):,}  (is {kiekiai.sum():,})")
    print(f"  Stulpeliu: {rezultatas.shape[1]}")
    print(f"  Dydis:     {dydis_mb:.1f} MB")
    print(f"\nPasiskirstymas: {DARBINIAI / 'imties_pasiskirstymas.csv'}")

    # Perspejimas del per retu klasiu
    retos = galutiniai[galutiniai < 100]
    if not retos.empty:
        print("\n[!] Sios klases turi < 100 pavyzdziu - ju metrikos bus triuksmas:")
        print(retos.to_string())
        print("    Sprendimas: didinti MIN_EILUCIU arba jungti klases i kategorijas.")


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
