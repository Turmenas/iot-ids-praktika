# -*- coding: utf-8 -*-
"""
Inferencijos delsos permatavimas CPU.

Paleidimas:
    python -m src.eksperimentai.delsa
    python -m src.eksperimentai.delsa --modeliai gradientinis mlp

Atnaujina `inferencija_us` stulpeli rezultatai.csv. Modeliai NEPERMOKOMI.


KODEL PERMATUOJAMA
------------------
XGBoost mokytas su `device: cuda`, todel issaugotas modelis lieka GPU
atmintyje ir prognozuoja GPU. Ismatuota 4,13 mikrosekundes - bet
KRASTINIS SLIUZAS GPU NETURI. Tai buvo 2 skyriaus prielaida, is kurios
kyla visas delsos biudzetas (20-50 ms).

GPU matuota delsa yra per optimistine, o kartu nesulyginama su Random
Forest ir MLP, kurie matuoti CPU. Todel visiems modeliams delsa
matuojama vienodai: CPU, tuo paciu paketo dydziu.

Matuojamas MINIMUMAS is trijų kartojimu - jis maziau jautrus atsitiktinei
sistemos apkrovai nei vidurkis.

⚠️ VISI MODELIAI MATUOJAMI VIENU PALEIDIMU, VIENOJE MASINOJE.
Delsa priklauso nuo aparatūros, todel dalies eiluciu permatavimas kitoje
masineje padarytu stulpeli nesulyginama - butent tai ir taisoma. Todel
paleidziama BE `--modeliai` filtro, nebent truksta atminties; tada
likusius reikia permatuoti toje pacioje masinoje.
"""

from __future__ import annotations

import argparse
import gc
import time
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
APMOKYTI = SAKNIS / "rezultatai" / "apmokyti"
REZULTATAI = SAKNIS / "rezultatai" / "rezultatai.csv"

EILUCIU = 20_000        # tiek pat, kiek matavo paleisti.py
KARTOJIMAI = 3


def _prognozuotojas(zyma: str, d, skale):
    """Grazina funkcija, kuri atlieka TA PATI darba kaip diegime."""
    if zyma.startswith("random_forest"):
        return d.predict
    if zyma.startswith("gradientinis"):
        m = d["modelis"]
        m.set_params(device="cpu")          # esme: inferencija CPU
        return m.predict
    if zyma.startswith(("mlp", "autoencoder")):
        import tensorflow as tf
        keras = tf.keras.models.load_model(
            (APMOKYTI / f"{zyma}.joblib").with_suffix(".keras"))
        return lambda X: keras.predict(X, batch_size=4096, verbose=0)
    raise KeyError(zyma)


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("--modeliai", nargs="+", default=None,
                   help="tik siu tipu modeliai (pvz. gradientinis mlp)")
    n = a.parse_args()

    import joblib

    from src.duomenys import pozymiai, skaidymas
    from src.modeliai.bazinis import rasti_issaugotus

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, _, _ = pozymiai.atrinkti(df, tikrinti=False)
    Xtr = X.iloc[idx["train"]]
    skale_bendra = pozymiai.Skale().fit(Xtr)      # atsargai, jei nebus issaugotos
    Xv = X.iloc[idx["val"]][:EILUCIU].copy()
    del df, X, Xtr
    gc.collect()

    rez = pd.read_csv(REZULTATAI)
    pakeista = []

    for seed in (42, 43, 44):
        for m in rasti_issaugotus(APMOKYTI, seed):
            if n.modeliai and m["tipas"] not in n.modeliai:
                continue
            kelias = APMOKYTI / f"{m['zyma']}.joblib"
            d = joblib.load(kelias)

            skale = None
            if m["reikia_skales"]:
                sk = kelias.with_suffix(".skale.joblib")
                skale = (pozymiai.Skale.ikelti(sk) if sk.exists()
                         else skale_bendra)
            ivestis = skale.transform(Xv) if skale is not None else Xv

            f = _prognozuotojas(m["zyma"], d, skale)
            laikai = []
            for _ in range(KARTOJIMAI):
                t0 = time.perf_counter()
                f(ivestis)
                laikai.append((time.perf_counter() - t0) / len(Xv) * 1e6)
            us = min(laikai)

            kauke = ((rez.modelis == m["vardas"]) &
                     (rez.seed == seed) &
                     (rez.konfig == f"konfig/{m['konfigas']}.yaml"))
            sena = rez.loc[kauke, "inferencija_us"]
            rez.loc[kauke, "inferencija_us"] = round(us, 3)
            pakeista.append({
                "modelis": m["rodomas"], "seed": seed,
                "buvo_us": None if sena.empty else float(sena.iloc[0]),
                "dabar_us": round(us, 3), "eiluciu": int(kauke.sum())})
            print(f"  {m['rodomas']:28s} seed {seed}  {us:8.2f} us"
                  + ("" if kauke.any() else "   [!] eilutes CSV nerasta"))
            del d, f
            gc.collect()

    rez.to_csv(REZULTATAI, index=False)
    p = pd.DataFrame(pakeista)
    print(f"\nAtnaujinta {int(p.eiluciu.sum())} eiluciu -> "
          f"{REZULTATAI.relative_to(SAKNIS)}")
    print("\nVidurkiai po permatavimo (CPU):")
    print(p.groupby("modelis")[["buvo_us", "dabar_us"]].mean().round(2).to_string())
    print(f"\nSliuzo biudzetas 20 000 us - visi telpa "
          f"{20000 / p.dabar_us.max():.0f}x ar daugiau.")


if __name__ == "__main__":
    main()
