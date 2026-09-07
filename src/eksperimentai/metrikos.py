# -*- coding: utf-8 -*-
"""
Metriku skaiciavimas — protokolo 5.7 (14-16 punktai).

KODEL NE ACCURACY
-----------------
Pagrindine metrika yra macro-F1. Bendras tikslumas skaiciuojamas ir
pateikiamas, bet TIK palyginimui su literatura: prie 41,8:1 santykio
modelis, viska zymintis kaip ataka, gautu ~97,6 %.

KAIP APIBREZIAMAS FPR DAUGIAKLASEJE UZDUOTYJE
---------------------------------------------
`fpr` = dalis TIKRO gerybinio srauto eiluciu, priskirtu bet kuriai atakos
kategorijai. Tai vienintelis apibrezimas, atitinkantis 1 skyriaus
skaiciavima ("1 % klaidingu teigiamu = ~1000 signalu per para"), ir
butent jam atrankoje skirta 30 % svorio.

Alternatyva - vidutinis per-klase FPR - butu didesnis ir grazesnis
skaicius, bet nieko nesakytu apie SOC analitiko krūvį.
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

GERYBINE = "Benign"

#: Protokolo 24 punkto schema. Eiluciu tvarka fiksuota.
SCHEMA = [
    "modelis", "formuluote", "seed",
    "macro_f1", "weighted_f1", "accuracy", "pr_auc", "roc_auc", "mcc", "fpr",
    "mokymo_laikas_s", "inferencija_us", "modelio_dydis_mb",
    "konfig", "data",
]


def _rikiavimo_ivertis(proba: np.ndarray, klases, priziurimas: bool):
    """
    Suvienodina priziurimu ir nepriziurimu modeliu iverti PR/ROC-AUC.

    Priziurimiems: (n, k) matrica. Nepriziurimiems: (n,) atkurimo paklaida.
    Bendras yra tik rikiavimas - butent jo ir reikia AUC metrikoms.
    """
    if not priziurimas:
        return np.asarray(proba).ravel()
    return np.asarray(proba)


def suskaiciuoti(y_true, y_pred, proba=None, klases=None,
                 priziurimas: bool = True) -> dict:
    """Kokybes metrikos. Grazina zodyna su SCHEMA laukais (be meta duomenu)."""
    from sklearn.metrics import (accuracy_score, average_precision_score,
                                 f1_score, matthews_corrcoef, roc_auc_score)

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    r = {
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "accuracy": accuracy_score(y_true, y_pred),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "pr_auc": np.nan,
        "roc_auc": np.nan,
        "fpr": np.nan,
    }

    # ─── FPR: tikras gerybinis srautas, priskirtas atakai ───
    gerybines = y_true == GERYBINE
    if gerybines.any():
        r["fpr"] = float((y_pred[gerybines] != GERYBINE).mean())

    # ─── AUC metrikos ───
    if proba is not None:
        try:
            s = _rikiavimo_ivertis(proba, klases, priziurimas)
            if priziurimas and s.ndim == 2:
                from sklearn.preprocessing import label_binarize
                Y = label_binarize(y_true, classes=list(klases))
                if Y.shape[1] == 1:            # dvejetaine uzduotis
                    Y = np.hstack([1 - Y, Y])
                r["pr_auc"] = average_precision_score(Y, s, average="macro")
                r["roc_auc"] = roc_auc_score(Y, s, average="macro",
                                             multi_class="ovr")
            else:                              # nepriziurimas: ivertis (n,)
                teigiama = (y_true != GERYBINE).astype(int)
                r["pr_auc"] = average_precision_score(teigiama, s)
                r["roc_auc"] = roc_auc_score(teigiama, s)
        except ValueError as e:
            print(f"  [!] AUC neskaiciuojama: {e}")

    return r


def sumaisymo_matrica(y_true, y_pred, klases) -> pd.DataFrame:
    """Sumaisymo matrica su vardais — 5 uzduoties paveikslams."""
    from sklearn.metrics import confusion_matrix
    m = confusion_matrix(y_true, y_pred, labels=list(klases))
    return pd.DataFrame(m, index=list(klases), columns=list(klases))


def eilute(modelis, formuluote: str, seed: int, metrikos: dict,
           mokymo_laikas_s: float, inferencija_us: float,
           dydis_mb: float, konfig: str) -> dict:
    """Suformuoja VIENA rezultatai.csv eilute pagal SCHEMA."""
    r = {
        "modelis": modelis,
        "formuluote": formuluote,
        "seed": seed,
        "mokymo_laikas_s": round(mokymo_laikas_s, 1),
        "inferencija_us": round(inferencija_us, 3),
        "modelio_dydis_mb": round(dydis_mb, 2),
        "konfig": konfig,
        "data": date.today().isoformat(),
        **{k: (None if v is None or (isinstance(v, float) and np.isnan(v))
               else round(float(v), 5)) for k, v in metrikos.items()},
    }
    truksta = [s for s in SCHEMA if s not in r]
    if truksta:
        raise ValueError(f"Eiluteje truksta SCHEMA lauku: {truksta}")
    return {k: r[k] for k in SCHEMA}


def prideti(eil: dict, kelias) -> None:
    """Prideda eilute i rezultatai.csv, issaugant SCHEMA tvarka."""
    from pathlib import Path
    kelias = Path(kelias)
    kelias.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([eil], columns=SCHEMA)
    yra = kelias.exists() and kelias.stat().st_size > 0
    df.to_csv(kelias, mode="a" if yra else "w", header=not yra, index=False)
