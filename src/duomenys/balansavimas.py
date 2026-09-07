# -*- coding: utf-8 -*-
"""
Klasiu disbalanso sprendimas.

IGYVENDINA PROTOKOLO 5.5 (claude/uzduotis_03_planas.md, 10-11 punktai):
  pirmas variantas - klasiu svoriai (duomenys nedubliuojami);
  SMOTE - TIK kaip abliacija vienam modeliui ir TIK ant mokymo aibes.

Paleidimas:
    python -m src.duomenys.balansavimas      # patikra ant tikros imties


KODEL SVORIAI, O NE SMOTE
-------------------------
Trys nepriklausomi argumentai:

1. Svoriai nedubliuoja duomenu: mokymo laikas nesikeicia, o imtis
   lieka ta pati, kuria aprasome ataskaitoje.
2. `imani2025imbalance`: geriausias derinys yra SUDERINTAS XGBoost su
   SMOTE - t. y. SMOTE vertas patikrinti, bet ne dauginti is keturiu.
3. SMOTE interpoliuoja tarp artimiausiu kaimynu, o dviprasmiskose
   srityse tai dviprasmiskuma sustiprintu. (Patikslinta 2026-09-06:
   pasalinus dublikatus tokiu eiluciu tera 0,43 %, todel sis argumentas
   yra silpnas - lieka pirmi du.)


ATSTUMAS NUO PROTOKOLO, KURI BUTINA IVARDYTI
--------------------------------------------
Protokolo 10 punktas XGBoost'ui numato `scale_pos_weight`. Tas parametras
veikia TIK dvejetaineje uzduotyje - daugiaklasei jis ignoruojamas. 8
kategoriju formuluotei ekvivalentas yra `sample_weight`, perduodamas
`fit()` metu. Todel cia grazinamas eiluciu svoriu masyvas, o
`scale_pos_weight` naudojamas tik dvejetaineje formuluoteje.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]


# ─── 1. Klasiu svoriai — numatytasis budas ───────────────────────────

def klasiu_svoriai(y_train) -> dict:
    """
    `class_weight="balanced"` ekvivalentas: n / (k * n_klases).

    Grazinamas zodynas, o ne eilute "balanced", kad svoriai butu MATOMI
    ir patektu i eksperimento konfiguracija - kitaip ju reiksmiu
    ataskaitoje nurodyti nebutu is kur.
    """
    from sklearn.utils.class_weight import compute_class_weight
    klases = np.unique(y_train)
    sv = compute_class_weight("balanced", classes=klases, y=np.asarray(y_train))
    return dict(zip(klases, sv))


def eiluciu_svoriai(y_train) -> np.ndarray:
    """
    Eiluciu svoriai XGBoost `fit(sample_weight=...)` metodui.

    Butent sis budas, o ne `scale_pos_weight`, veikia daugiaklaseje
    uzduotyje (zr. modulio dokumentacija).
    """
    sv = klasiu_svoriai(y_train)
    return np.asarray(pd.Series(np.asarray(y_train)).map(sv), dtype="float64")


def scale_pos_weight(y_train, teigiama) -> float:
    """Dvejetainei formuluotei: neigiamu ir teigiamu santykis."""
    y = np.asarray(y_train)
    t = int((y == teigiama).sum())
    if t == 0:
        raise ValueError(f"Mokymo aibeje nera klases {teigiama!r}")
    return float((len(y) - t) / t)


# ─── 2. SMOTE — tik abliacijai ───────────────────────────────────────

#: Gerybinis srautas NIEKADA nesintetinamas - zr. `smote` dokumentacija.
NESINTETINAMOS = frozenset({"Benign", "BENIGN"})


def smote(X_train, y_train, riba_dalis: float = 0.10, seed: int = 42):
    """
    SMOTE TIK mokymo aibei ir TIK ataku klasems. Grazina (X_bal, y_bal).

    `riba_dalis` - iki kokios gausiausios klases dalies keliamos retos
    klases. Numatyta 0,10, o ne pilnas subalansavimas, nes:
      pilnas subalansavimas 8 kategoriju uzduotyje reikstu 8 x 735 000 =
      5,9 mln. eiluciu (~1,7 GB) ir mokymo laika, virsijanti 30 min.
      biudzeta vienam modeliui. Abliacijos tikslas - patikrinti, ar
      sintetiniai pavyzdziai padeda, o ne pasiekti lygias klases.

    Pilnam subalansavimui: riba_dalis=1.0.

    GERYBINIS SRAUTAS NESINTETINAMAS. Dvi priezastys:
      1. Klaidingu teigiamu analize (5 uzduotis) turi remtis TIKRU
         gerybiniu srautu. Interpoliuoti pavyzdziai iskreiptu butent ta
         rodikli, kuriam skirti 30 % atrankos svorio.
      2. Autokoderio prielaida yra svarus gerybinio srauto profilis.
         Sintetinis gerybinis srautas ta prielaida pazeistu.
    """
    from imblearn.over_sampling import SMOTE

    y = pd.Series(np.asarray(y_train))
    kiekiai = y.value_counts()
    tikslas = int(kiekiai.max() * riba_dalis)

    strategija = {k: max(v, tikslas) for k, v in kiekiai.items()
                  if v < tikslas and k not in NESINTETINAMOS}
    if not strategija:
        raise ValueError(
            f"Nera klasiu, maziesniu uz {tikslas:,} - SMOTE nieko nekeistu.")

    # SMOTE interpoliuoja tarp k artimiausiu kaimynu: klase turi turėti
    # bent k+1 nari. Maziausia klase mokymo aibeje - 837, tad 5 saugu.
    maziausia = int(kiekiai.min())
    k = min(5, maziausia - 1)
    if k < 1:
        raise ValueError(f"Maziausia klase turi {maziausia} eilutes - SMOTE negalimas")

    X_bal, y_bal = SMOTE(sampling_strategy=strategija, k_neighbors=k,
                         random_state=seed).fit_resample(X_train, y)
    return X_bal, y_bal


# ─── 3. Apsauga nuo nutekejimo ───────────────────────────────────────

def patikrinti_tik_train(idx_naudota: np.ndarray, idx_train: np.ndarray) -> None:
    """
    Meta klaida, jei balansuojama ne mokymo aibe.

    Protokolo 11 punktas uzrasytas kaip TAISYKLE, ne ketinimas. Taisykle,
    kurios niekas netikrina, yra ketinimas.
    """
    if not np.isin(idx_naudota, idx_train).all():
        kiek = int((~np.isin(idx_naudota, idx_train)).sum())
        raise ValueError(
            f"Balansavimas taikomas {kiek:,} eilutems uz mokymo aibes ribu. "
            "SMOTE ir klasiu svoriai taikomi TIK train (protokolo 11 punktas).")


# ─── Patikra ─────────────────────────────────────────────────────────

def _patikra() -> None:
    from src.duomenys import pozymiai, skaidymas

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, y_et, y_kat = pozymiai.atrinkti(df, tikrinti=False)

    y_train = y_kat.to_numpy()[idx["train"]]
    print(f"Mokymo aibe: {len(y_train):,} eilutes, {len(np.unique(y_train))} kategorijos\n")

    sv = klasiu_svoriai(y_train)
    kiekiai = pd.Series(y_train).value_counts()
    print(f"{'kategorija':12s} {'eiluciu':>10s} {'svoris':>8s}")
    for k in sorted(sv, key=lambda k: -kiekiai[k]):
        print(f"{k:12s} {kiekiai[k]:>10,} {sv[k]:>8.3f}")

    print(f"\nSvoriu santykis (max/min): {max(sv.values())/min(sv.values()):.1f}")
    es = eiluciu_svoriai(y_train)
    print(f"Eiluciu svoriu masyvas: {es.shape}, suma {es.sum():,.0f} "
          f"(laukta ~{len(y_train):,})")

    print("\nSMOTE abliacija (riba_dalis=0,10):")
    tikslas = int(kiekiai.max() * 0.10)
    kelia = {k: v for k, v in kiekiai.items()
             if v < tikslas and k not in NESINTETINAMOS}
    praleista = [k for k, v in kiekiai.items()
                 if v < tikslas and k in NESINTETINAMOS]
    print(f"  Tikslas retoms klasems: {tikslas:,} eiluciu")
    print(f"  Keliamos {len(kelia)} kategorijos: {sorted(kelia)}")
    if praleista:
        print(f"  Sąmoningai NEkeliamos: {sorted(praleista)} "
              f"(gerybinis srautas nesintetinamas)")
    po = sum(tikslas if (v < tikslas and k not in NESINTETINAMOS) else v
             for k, v in kiekiai.items())
    print(f"  Eiluciu po SMOTE: {po:,} (+{po - len(y_train):,})")
    print(f"  Pilnas subalansavimas duotu: {kiekiai.max() * len(kiekiai):,} "
          f"- todel ne jis")

    # Apsauga veikia?
    try:
        patikrinti_tik_train(idx["test"][:5], idx["train"])
        print("\n[KLAIDA] Apsauga nesuveike!")
    except ValueError:
        print("\n[OK] Apsauga nuo balansavimo ne ant train suveikia")


if __name__ == "__main__":
    _patikra()
