# -*- coding: utf-8 -*-
"""
Eksperimento paleidimas: konfigas -> mokymas -> metrikos -> rezultatai.csv

Paleidimas:
    python -m src.eksperimentai.paleisti konfig/random_forest.yaml
    python -m src.eksperimentai.paleisti konfig/random_forest.yaml --seed 43
    python -m src.eksperimentai.paleisti konfig/*.yaml --seed 42 43 44

    # greita patikra pries tikra paleidima (imtis is mokymo aibes):
    python -m src.eksperimentai.paleisti konfig/random_forest.yaml --imtis 50000

    # 5 UZDUOTIS ir tik ji - modeliai jau apmokyti, todel NEPERMOKOMI:
    python -m src.eksperimentai.paleisti konfig/gradientinis_derintas.yaml \
        --seed 42 43 44 --vertinimas test --tik-vertinti


AIBE YRA REZULTATO DALIS, NE PALEIDIMO NUSTATYMAS
-------------------------------------------------
`rezultatai.csv` eilute apibreziama penkeriuka (modelis, formuluote,
seed, konfig, AIBE). Iki 2026-09-09 aibes rakte nebuvo, todel `test`
paleidimas butu perrases atitinkama `val` eilute - tyliai, be klaidos.


TEST AIBE NELIECIAMA IKI 5 UZDUOTIES
------------------------------------
Protokolo 19 punktas. Numatytoji vertinimo aibe yra `val`; `test`
ikeliama TIK su aiskia `--vertinimas test` veliava. Taisykle, kurios
niekas netikrina, yra ketinimas, todel test aibe cia is viso
neatidaroma be tos veliavos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from src.duomenys import balansavimas, pozymiai, skaidymas
from src.eksperimentai import metrikos
from src.modeliai import bazinis

SAKNIS = Path(__file__).resolve().parents[2]
REZULTATAI = SAKNIS / "rezultatai" / "rezultatai.csv"
APMOKYTI = SAKNIS / "rezultatai" / "apmokyti"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"

FORMULUOTES = ("8kat", "dvejetaine", "34klases")


def _y(y_et: pd.Series, y_kat: pd.Series, formuluote: str) -> np.ndarray:
    if formuluote == "8kat":
        return y_kat.to_numpy()
    if formuluote == "34klases":
        return y_et.to_numpy()
    if formuluote == "dvejetaine":
        return np.where(y_kat.to_numpy() == metrikos.GERYBINE,
                        metrikos.GERYBINE, "Ataka")
    raise ValueError(f"Nezinoma formuluote {formuluote!r}. Yra: {FORMULUOTES}")


def paleisti(konfig_kelias: Path, seed: int, vertinimas: str = "val",
             imties_riba: int | None = None,
             tik_vertinti: bool = False) -> dict:
    konfig = yaml.safe_load(Path(konfig_kelias).read_text(encoding="utf-8"))
    raktas = konfig["modelis"]
    formuluote = konfig.get("formuluote", "8kat")

    print(f"\n{'='*64}\n{konfig_kelias.name} · {raktas} · {formuluote} · seed {seed}"
          f" · {vertinimas}\n{'='*64}")

    zyma = f"{Path(konfig_kelias).stem}_{formuluote}_seed{seed}"
    aplankas = APMOKYTI / "_patikra" if imties_riba else APMOKYTI
    kelias = aplankas / f"{zyma}.joblib"

    if tik_vertinti and not kelias.exists():
        raise SystemExit(f"Nerasta {kelias} - `--tik-vertinti` reikalauja "
                         f"jau apmokyto modelio.")

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, y_et, y_kat = pozymiai.atrinkti(df, tikrinti=False)
    y = _y(y_et, y_kat, formuluote)

    i_train = idx["train"]
    if imties_riba:                       # tik greitai patikrai
        rng = np.random.default_rng(seed)
        i_train = np.sort(rng.choice(i_train, min(imties_riba, len(i_train)),
                                     replace=False))
        print(f"[!] PATIKROS rezimas: mokymo aibe apkarpyta iki {len(i_train):,}")

    if vertinimas == "test":
        print("[!] Naudojama TEST aibe (5 uzduotis)")
    i_vert = idx[vertinimas]

    X_vert, y_vert = X.iloc[i_vert], y[i_vert]

    Klase = bazinis.gauti(raktas)
    modelis = Klase(konfig.get("hiperparametrai", {}), seed=seed)

    skale_kelias = kelias.with_suffix(".skale.joblib")

    if tik_vertinti:
        # Mokymo aibe cia neikeliama: ji reikalinga tik skalei, o ta
        # issaugota salia modelio. Prie 1,7 mln. x 36 tai ~490 MB, kuriu
        # neuzimant Random Forest turi realia galimybe issitekti.
        print(f"[i] Modelis NEPERMOKOMAS - ikeliamas {kelias.name}")
        modelis = Klase.ikelti(kelias)
        skale = None
        if modelis.reikia_skales:
            if skale_kelias.exists():
                skale = pozymiai.Skale.ikelti(skale_kelias)
            else:
                # StandardScaler deterministinis, tad perskaiciuota is tos
                # pacios mokymo aibes skale yra tapati. Bet tai pasakoma
                # garsiai: tylus perskaiciavimas paslepia, kad modelis
                # issaugotas be savo normalizavimo parametru.
                print("  [!] Skale su modeliu neissaugota - "
                      "perskaiciuojama is train")
                skale = pozymiai.Skale().fit(X.iloc[idx["train"]])
        X_vert_m = skale.transform(X_vert) if skale is not None else X_vert
        print(f"{vertinimas} {len(X_vert):,} eilutes · "
              f"mokymo laikas is metaduomenu: {modelis.mokymo_laikas_s}")
    else:
        X_train, y_train = X.iloc[i_train], y[i_train]
        X_val, y_val = X.iloc[idx["val"]], y[idx["val"]]

        print(f"train {len(X_train):,} · {vertinimas} {len(X_vert):,} · "
              f"{len(np.unique(y_train))} klases")

        # ─── Normalizavimas: fit TIK ant mokymo aibes ───
        skale = None
        if modelis.reikia_skales:
            skale = pozymiai.Skale().fit(X_train)
            X_train_m = skale.transform(X_train)
            X_vert_m = skale.transform(X_vert)
            X_val_m = skale.transform(X_val)
        else:
            X_train_m, X_vert_m, X_val_m = X_train, X_vert, X_val

        # ─── SMOTE abliacija: TIK train, TIK jei konfigas praso ───
        if konfig.get("smote"):
            balansavimas.patikrinti_tik_train(i_train, idx["train"])
            pries = len(X_train_m)
            X_train_m, y_train = balansavimas.smote(
                X_train_m, y_train, riba_dalis=konfig.get("smote_riba", 0.10),
                seed=seed)
            print(f"SMOTE: {pries:,} -> {len(X_train_m):,}")

        print("Mokoma...")
        modelis.fit(X_train_m, y_train, X_val_m, y_val)
        print(f"  mokymo laikas {modelis.mokymo_laikas_s:.1f} s")

    y_pred = modelis.predict(X_vert_m)
    proba = modelis.predict_proba(X_vert_m)

    m = metrikos.suskaiciuoti(y_vert, y_pred, proba, modelis.klases_,
                              modelis.priziurimas)

    # Delsa matuojama ant mazesnes imties - matuojamas laikas irasui, ne visai aibei
    n = min(20_000, len(X_vert_m))
    delsa = modelis.inferencijos_delsa_us(
        X_vert_m[:n] if isinstance(X_vert_m, np.ndarray) else X_vert_m.iloc[:n])

    # Konfigo vardas BUTINAS zymoje: be jo `mokyti_derintus.bat` uzrase
    # bazinius modelius tais paciais failais, ir palyginimo "pries/po"
    # nebeliko - liko tik metrikos rezultatai.csv.
    # Patikros rezimo modeliai i tikra aplanka nepatenka: greta tikruju
    # gulintis nuo 50 000 eiluciu apmokytas failas tuo paciu vardu yra
    # klaida, kurios veliau nebeatskirsi.
    if not tik_vertinti:
        kelias = modelis.issaugoti(kelias)
        if skale is not None:
            # Be skales issaugotas MLP ar autokoderis yra neveikiantis
            # artefaktas: ivesties normalizavimo parametrai prarasti.
            skale.issaugoti(skale_kelias)
    dydis = modelis.dydis_mb(kelias)

    if not imties_riba:
        # ⚠️ Aibe zymoje BUTINA: be jos test sumaisymo matrica butu
        # perrasiusi val matrica tuo paciu vardu. Ta pati klaida, kuri
        # 2026-09-08 istrynė bazinius modelius, tik pagauta pries, ne po.
        metrikos.sumaisymo_matrica(y_vert, y_pred, modelis.klases_).to_csv(
            DARBINIAI / f"sumaisymas_{zyma}_{vertinimas}.csv")

    eil = metrikos.eilute(modelis.vardas, formuluote, seed, m,
                          modelis.mokymo_laikas_s, delsa, dydis,
                          str(Path(konfig_kelias).as_posix()), vertinimas)
    if not imties_riba:
        metrikos.prideti(eil, REZULTATAI)

    print(f"\n  macro-F1 {m['macro_f1']:.4f} · PR-AUC {m['pr_auc']:.4f} · "
          f"MCC {m['mcc']:.4f}")
    print(f"  tikslumas {m['accuracy']:.4f} · FPR {m['fpr']:.5f}")
    print(f"  delsa {delsa:.2f} us/irasui · dydis {dydis:.2f} MB")
    if imties_riba:
        print("\n[!] PATIKROS rezimas - i rezultatai.csv NERASOMA")
    return eil


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("konfigai", nargs="+", type=Path)
    a.add_argument("--seed", nargs="+", type=int, default=[42])
    a.add_argument("--vertinimas", choices=("val", "test"), default="val")
    a.add_argument("--imtis", type=int, default=None,
                   help="apkarpyti mokymo aibe - TIK greitai patikrai")
    a.add_argument("--tik-vertinti", action="store_true", dest="tik_vertinti",
                   help="neikelti mokymo aibes ir nepermokyti: ikelti "
                        "issaugota modeli ir tik ji ivertinti")
    n = a.parse_args()

    if n.tik_vertinti and n.imtis:
        raise SystemExit("--tik-vertinti ir --imtis viena kito neisskiria: "
                         "pirmasis nemoko, antrasis keicia mokymo aibe.")

    if n.vertinimas == "test":
        print("\n" + "=" * 64)
        print("TEST AIBE. Eilutes rasomos su `aibe=test`;")
        print("`aibe=val` eilutes NELIECIAMOS (metrikos.RAKTAS).")
        print("Slenkstis tau NEPERRENKAMAS - jis imamas is val.")
        print("=" * 64)

    import time
    darbai = [(k, s) for k in n.konfigai for s in n.seed]
    t0 = time.perf_counter()

    for i, (k, s) in enumerate(darbai, 1):
        praejo = time.perf_counter() - t0
        liko = (f"  praejo {praejo/60:.1f} min, liko ~"
                f"{praejo/(i-1)*(len(darbai)-i+1)/60:.0f} min" if i > 1 else "")
        print(f"\n>>> PALEIDIMAS {i}/{len(darbai)}{liko}")
        try:
            paleisti(k, s, n.vertinimas, n.imtis, n.tik_vertinti)
        except Exception as e:
            print(f"\n[KLAIDA] {k.name} seed {s}: {type(e).__name__}: {e}")
            raise

    if not n.imtis:
        print(f"\nRezultatai: {REZULTATAI.relative_to(SAKNIS)}")
        print("Lenteles: python -m src.eksperimentai.i_latex")


if __name__ == "__main__":
    main()
