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
#:
#: `aibe` (val / test) pridetas 2026-09-09, pries pirma 5 uzduoties
#: paleidima. Be jo `test` eilute butu uzemusi `val` eilutes vieta (zr.
#: RAKTAS pastaba) ir 21 turimas `val` rezultatas butu dinges TYLIAI.
SCHEMA = [
    "modelis", "formuluote", "seed", "aibe",
    "macro_f1", "weighted_f1", "accuracy", "pr_auc", "roc_auc", "mcc", "fpr",
    "mokymo_laikas_s", "inferencija_us", "modelio_dydis_mb",
    "konfig", "data",
]

#: Aibes, kuriomis modelis gali buti vertinamas.
AIBES = ("val", "test")


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
           dydis_mb: float, konfig: str, aibe: str) -> dict:
    """Suformuoja VIENA rezultatai.csv eilute pagal SCHEMA.

    `aibe` yra butinas pozicinis argumentas sazmoningai: numatytoji
    reiksme "val" butu leidusi test paleidimui tyliai issisaugoti kaip
    val. Argumentas be numatytosios reiksmes verzia kviecianti koda
    apsispresti.
    """
    if aibe not in AIBES:
        raise ValueError(f"Nezinoma aibe {aibe!r}. Yra: {AIBES}")
    r = {
        "modelis": modelis,
        "formuluote": formuluote,
        "seed": seed,
        "aibe": aibe,
        # Ikeliant modeli mokymo laikas imamas is metaduomenu ir gali ju
        # neturėti (seni failai). Nulis butu melas, todel None.
        "mokymo_laikas_s": (None if mokymo_laikas_s is None
                            else round(mokymo_laikas_s, 1)),
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


#: Kas vienareiksmiskai apibrezia paleidima. Ta pati penkeriuka du kartus
#: reiskia PAKARTOJIMA, ne nauja rezultata.
#:
#: ⚠️ `aibe` cia yra BUTINA. Be jos `--vertinimas test` paleidimas su tuo
#: paciu konfigu ir seed'u butu perrases atitinkama `val` eilute - be
#: klaidos, be ispejimo, ir `rezultatai.tex` butu rodes test skaicius po
#: isnasa apie val. Tai tos pacios rusies klaida kaip `Duration` = TTL:
#: dalykas, kurio supainiojimas nepasirodo kaip klaida.
RAKTAS = ["modelis", "formuluote", "seed", "konfig", "aibe"]


def prideti(eil: dict, kelias) -> None:
    """Iraso eilute i rezultatai.csv. Pakartotinis paleidimas PAKEICIA.

    Paprastas prirasymas (`mode="a"`) atrode saugus, bet 2026-09-07
    paleidus mokyti_viska.bat antra karta faile atsirado 24 eilutes
    vietoj 12. Kokybes metrikos nuo to nenukentetu (jos tapacios), bet
    isnasa "vidurkis is 3 paleidimu" butu melas, o laiko rodikliu sklaida
    skaiciuojama is 6 matavimu po 2 tam paciam seed'ui.

    Todel eilute su tuo paciu RAKTU perrasoma: failas idempotentiskas ir
    ji galima saugiai regeneruoti bet kada.
    """
    from pathlib import Path
    kelias = Path(kelias)
    kelias.parent.mkdir(parents=True, exist_ok=True)
    nauja = pd.DataFrame([eil], columns=SCHEMA)

    if kelias.exists() and kelias.stat().st_size > 0:
        sena = pd.read_csv(kelias)
        # Failas is laiku pries `aibe` stulpeli: visos jo eilutes yra val,
        # nes test aibe iki 2026-09-09 nebuvo atidaryta nei karto
        # (protokolo 19 punktas). Migracija cia, o ne atskirame skripte,
        # kad senas failas negaletu tyliai susikirsti su nauju raktu.
        if "aibe" not in sena.columns:
            print("  [i] rezultatai.csv be `aibe` stulpelio - "
                  "esamos eilutes zymimos kaip val")
            sena.insert(3, "aibe", "val")
        kauke = ~(sena[RAKTAS].astype(str)
                  .eq(nauja[RAKTAS].astype(str).iloc[0]).all(axis=1))
        nauja = pd.concat([sena[kauke], nauja], ignore_index=True)[SCHEMA]

    nauja.to_csv(kelias, index=False)
