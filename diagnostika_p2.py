# -*- coding: utf-8 -*-
"""
Vienkartine diagnostika: is kur atsirado 30 vienodu eiluciu tarp train ir test.

Paleidimas (is projekto saknies):
    python diagnostika_p2.py

Klausimas vienas: ar tos 30 eiluciu yra TIKSLIOS kopijos ir 39 stulpeliu
pavidalu. Nuo atsakymo priklauso, kur klaida:

    Taip, tikslios kopijos      -> dublikatu salinimas praleido eilutes;
                                   klaida `ikelimas.py`, ne skaidyme.
    Ne, skiriasi pasalintuose   -> prielaida, kad `Variance`, `Tot size` ir
    stulpeliuose                   `Tot sum` yra tikslios likusiuju funkcijos,
                                   kazkur negalioja.
    Ne, skiriasi likusiuose     -> maisu susidurimas patikroje (labai mazai
                                   tiketina: ~1e-7 prie 2 mln. eiluciu).
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.duomenys import pozymiai, skaidymas

SAKNIS = Path(__file__).resolve().parent


def main() -> None:
    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, y_et, y_kat = pozymiai.atrinkti(df, tikrinti=False)

    def su_etikete(i):
        return X.iloc[i].assign(_et=y_et.to_numpy()[i])

    tr, te = idx["train"], idx["test"]
    h_tr = pd.util.hash_pandas_object(su_etikete(tr), index=False).to_numpy()
    h_te = pd.util.hash_pandas_object(su_etikete(te), index=False).to_numpy()

    bendros = np.intersect1d(h_tr, h_te)
    print(f"Vienodu (pozymiai + etikete) maisu: {len(bendros)}")
    if len(bendros) == 0:
        print("Nera ko tirti.")
        return

    i_tr = tr[np.isin(h_tr, bendros)]
    i_te = te[np.isin(h_te, bendros)]
    print(f"train eiluciu: {len(i_tr)} · test eiluciu: {len(i_te)}\n")

    # ─── Kokios klases ───
    print("Etiketes:")
    for et, n in pd.Series(y_et.to_numpy()[i_te]).value_counts().items():
        print(f"  {et:28s} {n}")
    print("\nKategorijos:")
    for k, n in pd.Series(y_kat.to_numpy()[i_te]).value_counts().items():
        print(f"  {k:12s} {n}")

    # ─── Ar sutampa VISI stulpeliai, ne tik 36 pozymiai ───
    visi = [c for c in df.columns]
    d_tr = df.iloc[i_tr][visi].reset_index(drop=True)
    d_te = df.iloc[i_te][visi].reset_index(drop=True)

    hv_tr = set(pd.util.hash_pandas_object(d_tr, index=False).to_numpy())
    hv_te = set(pd.util.hash_pandas_object(d_te, index=False).to_numpy())
    pilnai = hv_tr & hv_te
    print(f"\nVisu {len(visi)} stulpeliu sutapimu: {len(pilnai)}")

    if pilnai:
        print("  -> TIKSLIOS KOPIJOS. Dublikatu salinimas praleido siuos.")
    else:
        print("  -> NE tikslios kopijos: skiriasi stulpeliai, kuriu 36 pozymiu")
        print("     aibeje nera. Tikrinam, kurie:")
        pal = [c for c in visi if c not in X.columns and c != "Label"]
        print(f"     tikrinami: {pal}")

    # ─── Pirmoji pora is arti ───
    pirmoji = bendros[0]
    a = df.iloc[tr[h_tr == pirmoji][0]]
    b = df.iloc[te[h_te == pirmoji][0]]
    skiriasi = [c for c in visi
                if not (pd.isna(a[c]) and pd.isna(b[c])) and a[c] != b[c]]
    print(f"\nPirmoji pora - besiskiriantys stulpeliai: {skiriasi or 'NE VIENO'}")
    if skiriasi:
        for c in skiriasi:
            print(f"    {c}: train {a[c]!r}  test {b[c]!r}")

    # ─── Kiek tai sveria ───
    print(f"\nDalis test aibeje: {len(i_te)}/{len(te)} = "
          f"{len(i_te)/len(te)*100:.4f} %")
    print(f"Itaka tikslumui, jei visos butu isimintos: "
          f"<= {len(i_te)/len(te)*100:.4f} p. p.")

    Path("rezultatai/darbiniai").mkdir(parents=True, exist_ok=True)
    df.iloc[np.concatenate([i_tr, i_te])].assign(
        _aibe=["train"] * len(i_tr) + ["test"] * len(i_te)
    ).to_csv("rezultatai/darbiniai/p2_sutapimai.csv", index=False)
    print("\nIssaugota: rezultatai/darbiniai/p2_sutapimai.csv")


if __name__ == "__main__":
    main()
