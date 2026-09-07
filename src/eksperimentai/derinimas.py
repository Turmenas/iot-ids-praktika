# -*- coding: utf-8 -*-
"""
Hiperparametru derinimas atsitiktine paieska (protokolo 18 punktas).

Paleidimas:
    python -m src.eksperimentai.derinimas random_forest
    python -m src.eksperimentai.derinimas gradientinis --bandymai 25
    python -m src.eksperimentai.derinimas mlp --imtis 300000

Rezultatas:
    rezultatai/darbiniai/derinimas_<modelis>.csv   visi bandymai


PROTOKOLO 18 PUNKTAS
--------------------
"Random Search, 20-30 bandymu, tik ant val. Biudzetas <= 30 min. vienam
modeliui be GPU." Iki 2026-09-07 paleista su numatytosiomis reiksmemis,
t. y. sis punktas buvo NEIVYKDYTAS.

KODEL PAIESKA ANT IMTIES
------------------------
Pilnas Random Forest mokymas trunka ~127 s, XGBoost ~203 s. Dvidesimt
bandymu butu 42-68 min. vienam modeliui - virs biudzeto. Todel paieska
vykdoma ant mokymo aibes DALIES (numatyta 400 000 eiluciu), o geriausia
rasta konfiguracija paskui permokoma ant visos aibes iprastu paleidimu.

Rikiuote tarp konfiguraciju imtyje ir pilnoje aibeje nebutinai sutampa,
todel tai APYTIKSLE paieska, ne tikslus optimizavimas. Tai ivardijama
ataskaitoje.

KODEL DYDIS FIKSUOJAMAS SALIA macro-F1
--------------------------------------
Random Forest su max_depth=None uzima 558 MB diske ir daugiau nei 3,9 GB
atmintyje - krastiniam sliuzui tai diskvalifikuojanti riba. Todel kiekvienam
bandymui fiksuojamas ir modelio dydis: rinktis reikia ne tik pagal macro-F1.

TEST AIBE CIA NEATIDAROMA.
"""

from __future__ import annotations

import argparse
import gc
import time
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"

TINKLELIAI: dict[str, dict] = {
    "random_forest": {
        "n_estimators":     [100, 200, 300],
        "max_depth":        [10, 15, 20, 25, 30, None],
        "min_samples_leaf": [1, 2, 5, 10],
        "max_features":     ["sqrt", "log2", 0.3],
    },
    "gradientinis": {
        "n_estimators":     [200, 400, 600, 800],
        "max_depth":        [4, 6, 8, 10],
        "learning_rate":    [0.05, 0.1, 0.2],
        "subsample":        [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
        "min_child_weight": [1, 5, 10],
    },
    "mlp": {
        "sluoksniai":    [[64], [128, 64], [256, 128], [128, 64, 32]],
        "dropout":       [0.0, 0.2, 0.3],
        "learning_rate": [0.0005, 0.001, 0.003],
        "batch_size":    [2048, 4096],
        "epochos":       [20],
    },
}


def _imti(tinklelis: dict, rng) -> dict:
    return {k: v[rng.integers(len(v))] for k, v in tinklelis.items()}


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("modelis", choices=list(TINKLELIAI))
    a.add_argument("--bandymai", type=int, default=20)
    a.add_argument("--imtis", type=int, default=400_000)
    a.add_argument("--seed", type=int, default=42)
    n = a.parse_args()

    import joblib
    from sklearn.metrics import f1_score

    from src.duomenys import pozymiai, skaidymas
    from src.modeliai import bazinis

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, _, y_kat = pozymiai.atrinkti(df, tikrinti=False)
    del df; gc.collect()

    rng = np.random.default_rng(n.seed)
    i_tr = idx["train"]
    if n.imtis and n.imtis < len(i_tr):
        i_tr = np.sort(rng.choice(i_tr, n.imtis, replace=False))

    y = y_kat.to_numpy()
    X_tr, y_tr = X.iloc[i_tr], y[i_tr]
    X_val, y_val = X.iloc[idx["val"]], y[idx["val"]]
    del X, y_kat; gc.collect()

    Klase = bazinis.gauti(n.modelis)
    print(f"{n.modelis}: {n.bandymai} bandymu · mokymas ant {len(X_tr):,} "
          f"eiluciu · vertinimas ant {len(X_val):,}\n")

    if Klase.reikia_skales:
        skale = pozymiai.Skale().fit(X_tr)
        X_tr_m, X_val_m = skale.transform(X_tr), skale.transform(X_val)
    else:
        X_tr_m, X_val_m = X_tr, X_val

    laikinas = DARBINIAI / f"_derinimas_{n.modelis}.joblib"
    eil, geriausias = [], None
    t0 = time.perf_counter()

    for b in range(1, n.bandymai + 1):
        p = _imti(TINKLELIAI[n.modelis], rng)
        try:
            m = Klase(p, seed=n.seed).fit(X_tr_m, y_tr, X_val_m, y_val)
            pred = m.predict(X_val_m)
            f1 = f1_score(y_val, pred, average="macro", zero_division=0)
            m.issaugoti(laikinas)
            dydis = m.dydis_mb(laikinas)
        except Exception as e:                 # bloga konfiguracija - ne stabdis
            print(f"  [{b:2d}/{n.bandymai}] KLAIDA: {type(e).__name__}: {e}")
            continue

        eil.append({"bandymas": b, "macro_f1": round(f1, 5),
                    "dydis_mb": round(dydis, 2),
                    "mokymo_laikas_s": round(m.mokymo_laikas_s, 1),
                    **{k: str(v) for k, v in p.items()}})
        zyma = ""
        if geriausias is None or f1 > geriausias["macro_f1"]:
            geriausias, zyma = eil[-1], "  <- geriausias"
        print(f"  [{b:2d}/{n.bandymai}] macro-F1 {f1:.4f} · {dydis:7.2f} MB · "
              f"{m.mokymo_laikas_s:5.1f} s{zyma}")
        del m; gc.collect()

    for p in (laikinas, laikinas.with_suffix(".json"), laikinas.with_suffix(".keras")):
        p.unlink(missing_ok=True)

    d = pd.DataFrame(eil).sort_values("macro_f1", ascending=False)
    DARBINIAI.mkdir(parents=True, exist_ok=True)
    kelias = DARBINIAI / f"derinimas_{n.modelis}.csv"
    d.to_csv(kelias, index=False)

    print(f"\nTruko {(time.perf_counter()-t0)/60:.1f} min. -> "
          f"{kelias.relative_to(SAKNIS)}")
    print(f"\nGeriausi penki (macro-F1 / dydis):")
    print(d.head(5).to_string(index=False))

    # Maziausias modelis, atsiliekantis ne daugiau kaip 1 % nuo geriausio:
    # dydis yra atrankos kriterijus, ne antraeilis rodiklis.
    riba = d.macro_f1.max() * 0.99
    k = d[d.macro_f1 >= riba].nsmallest(1, "dydis_mb")
    if not k.empty and k.iloc[0].bandymas != d.iloc[0].bandymas:
        print(f"\nAlternatyva: maziausias modelis, atsiliekantis <1 % "
              f"(macro-F1 {k.iloc[0].macro_f1:.4f}, {k.iloc[0].dydis_mb:.2f} MB "
              f"vietoj {d.iloc[0].dydis_mb:.2f} MB)")
        print(k.to_string(index=False))


if __name__ == "__main__":
    main()
