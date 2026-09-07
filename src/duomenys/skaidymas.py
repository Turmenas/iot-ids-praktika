# -*- coding: utf-8 -*-
"""
Duomenu skaidymas 70 / 15 / 15 ir nutekejimo patikros.

IGYVENDINA PROTOKOLO 5.4 (claude/uzduotis_03_planas.md, 7-9 punktai):
  stratifikuotas atsitiktinis skaidymas, fiksuotas SEED, indeksai
  ISSAUGOMI ir ikeliami, o ne perskaiciuojami kiekvieno paleidimo metu.

Paleidimas:
    python -m src.duomenys.skaidymas          # sukurti ir issaugoti
    python -m src.duomenys.skaidymas patikra  # tik patikrinti esama

Rezultatas: duomenys/processed/skaidymas.npz


KODEL STRATIFIKUOJAMA PAGAL 34 ETIKETES, O NE 8 KATEGORIJAS
-----------------------------------------------------------
Pagrindine uzduoties formuluote yra 8 kategorijos, todel butu natūralu
stratifikuoti pagal jas. Bet kategorija yra etiketes funkcija, tad
stratifikavimas pagal etikete automatiskai islaiko ir kategoriju
proporcijas - o atvirksciai negalioja. Stratifikuojant pagal kategorija
retos klases (UPLOADING_ATTACK - 1 196 eilutes) galetu pasiskirstyti
netolygiai savo kategorijos viduje.

KODEL CHRONOLOGINIS SKAIDYMAS NEIMANOMAS
----------------------------------------
Rinkinyje nera laiko zymos. Todel rezultatai nieko nesako apie modelio
elgsena laikui begant - tai ivardijama ataskaitoje kaip apribojimas.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
PROCESSED = SAKNIS / "duomenys" / "processed"
IMTIS = PROCESSED / "imtis.parquet"
SKAIDYMAS = PROCESSED / "skaidymas.npz"
ETIKETE = "Label"

SEED = 42
DALYS = {"train": 0.70, "val": 0.15, "test": 0.15}


def sukurti(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Stratifikuotas 70/15/15. Grazina {aibe: pozicinis indeksu masyvas}."""
    from sklearn.model_selection import train_test_split

    y = df[ETIKETE].to_numpy()
    visi = np.arange(len(df))

    likutis, test = train_test_split(
        visi, test_size=DALYS["test"], random_state=SEED, stratify=y)
    # val dalis skaiciuojama nuo LIKUCIO, kad galutine dalis butu 0,15 nuo viso
    val_dalis = DALYS["val"] / (DALYS["train"] + DALYS["val"])
    train, val = train_test_split(
        likutis, test_size=val_dalis, random_state=SEED, stratify=y[likutis])

    return {"train": np.sort(train), "val": np.sort(val), "test": np.sort(test)}


def ikelti() -> dict[str, np.ndarray]:
    if not SKAIDYMAS.exists():
        raise SystemExit(
            f"Nerastas {SKAIDYMAS} - pirma: python -m src.duomenys.skaidymas")
    with np.load(SKAIDYMAS) as z:
        return {k: z[k] for k in ("train", "val", "test")}


# ─── Patikros ────────────────────────────────────────────────────────

def patikrinti(df: pd.DataFrame, idx: dict[str, np.ndarray]) -> None:
    """
    Keturios patikros. Kiekviena atitinka konkrecia nutekejimo rizika.
    Nepraeita patikra meta klaida - be jos rezultatai butu bereiksmiai.
    """
    n = len(df)
    tr, va, te = idx["train"], idx["val"], idx["test"]

    # 1. Aibes nesikerta
    for a, b, vardas in ((tr, va, "train/val"), (tr, te, "train/test"),
                         (va, te, "val/test")):
        bendri = np.intersect1d(a, b)
        assert len(bendri) == 0, f"{vardas}: {len(bendri):,} bendru indeksu"

    # 2. Aibes padengia viska
    assert len(tr) + len(va) + len(te) == n, "Skaidymas nepadengia visu eiluciu"
    assert len(np.unique(np.concatenate([tr, va, te]))) == n, "Indeksai kartojasi"

    # 3. Nera vienodu EILUCIU tarp train ir test.
    #    Imtis jau be dublikatu, bet tai pagrindine protokolo apsauga,
    #    todel tikrinama tiesiogiai, o ne laikoma savaime suprantama.
    h = pd.util.hash_pandas_object(df, index=False).to_numpy()
    bendros = np.intersect1d(h[tr], h[te])
    assert len(bendros) == 0, (
        f"{len(bendros):,} vienodu eiluciu tarp train ir test - NUTEKEJIMAS")

    # 4. Kiekviena klase atstovaujama visose aibese
    for vardas, i in idx.items():
        truksta = set(df[ETIKETE].unique()) - set(df[ETIKETE].to_numpy()[i])
        assert not truksta, f"{vardas}: truksta klasiu {sorted(truksta)}"


def suvestine(df: pd.DataFrame, idx: dict[str, np.ndarray]) -> pd.DataFrame:
    """Klasiu pasiskirstymas aibese + nuokrypis nuo bendros proporcijos."""
    y = df[ETIKETE]
    bendra = y.value_counts(normalize=True)
    e = []
    for klase in bendra.index:
        r = {"klase": klase, "is_viso": int((y == klase).sum())}
        for vardas, i in idx.items():
            r[vardas] = int((y.to_numpy()[i] == klase).sum())
        dalis = r["train"] / max(len(idx["train"]), 1)
        r["nuokrypis_pp"] = round((dalis - bendra[klase]) * 100, 4)
        e.append(r)
    return pd.DataFrame(e)


def main(komanda: str = "sukurti") -> None:
    df = pd.read_parquet(IMTIS)

    if komanda == "patikra":
        idx = ikelti()
        print(f"Ikelta: train {len(idx['train']):,} · val {len(idx['val']):,} "
              f"· test {len(idx['test']):,}")
    else:
        if SKAIDYMAS.exists():
            print(f"[!] {SKAIDYMAS.name} jau yra. Protokolo 8 punktas: "
                  f"skaidymas sudaromas VIENA karta.")
            print("    Kad perkurtumete, istrinkite faila ranka.")
            return
        idx = sukurti(df)
        PROCESSED.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(SKAIDYMAS, seed=SEED, **idx)
        print(f"Issaugota: {SKAIDYMAS.relative_to(SAKNIS)}")

    patikrinti(df, idx)
    print("\n[OK] Keturios patikros praejo:")
    print("     aibes nesikerta · padengia viska · nera vienodu eiluciu "
          "tarp train ir test · visos klases visose aibese")

    print(f"\n{'aibe':6s} {'eiluciu':>10s} {'dalis':>8s}")
    for vardas, i in idx.items():
        print(f"{vardas:6s} {len(i):>10,} {len(i)/len(df)*100:>7.2f} %")

    s = suvestine(df, idx)
    print(f"\nDidziausias klases proporcijos nuokrypis train aibeje: "
          f"{s['nuokrypis_pp'].abs().max():.4f} p. p.")
    print("\nRetos klases (maziausios penkios):")
    print(s.nsmallest(5, "is_viso")[
        ["klase", "is_viso", "train", "val", "test"]].to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sukurti")
