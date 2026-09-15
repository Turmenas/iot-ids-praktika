# -*- coding: utf-8 -*-
"""
Sprendimo slenkstis priziurimiems modeliams: FPR biudzeto laikymasis.

Paleidimas:
    python -m src.eksperimentai.slenkstis
    python -m src.eksperimentai.slenkstis --biudzetas 0.01 --seed 42

Rezultatai:
    rezultatai/darbiniai/slenkscio_kreives.csv   visos kreives
    rezultatai/darbiniai/slenkscio_taskai.csv    parinkti operaciniai taskai
    ataskaita/lenteles/slenkstis.tex             lentele ataskaitai


KODEL SLENKSTIS, O NE ARGMAX
----------------------------
Prie argmax modelis skelbia ta klase, kurios tikimybe didziausia. Tai
netiesiogiai pasirenka operacini taska - ir, kaip pasirode 2026-09-07,
taska su 21-32 % klaidingu teigiamu, t. y. 21-32 kartus virs 1 skyriuje
apskaiciuoto biudzeto.

Taisykle cia aiski: ataka skelbiama tik jei BENDRA ataku tikimybe
virsija slenksti tau; kitu atveju - Benign. Modelis nepermokomas.

Tai NE naujas metodas ir NE protokolo pazeidimas: autokoderiui slenkstis
kalibruojamas ant val nuo pat pradziu (protokolo 21 punktas). Cia tas
pats principas taikomas visiems modeliams, kad palyginimas vyktu PRIE
VIENODO FPR, o ne prie atsitiktiniu argmax tasku.

Slenkstis renkamas TIK ant val.

`--taikyti test` (5 uzduotis) atidaro test aibe, bet tau IS FAILO
(`slenkscio_taskai.csv`) - naujo tau tame rezime neparenka niekas, nes
`parinkti()` ten net nekvieciamas. Isvestis rasoma i atskirus failus,
todel val taskai ir kreives lieka nepaliestos.
"""

from __future__ import annotations

import argparse
import gc
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
APMOKYTI = SAKNIS / "rezultatai" / "apmokyti"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"
LENTELES = SAKNIS / "ataskaita" / "lenteles"

GERYBINE = "Benign"

#: Priziurimu modeliu tipai. Konkretus failai randami aplanke - vardai
#: nekalami: ikalti jie luzo po failu pervadinimo, ir luzo DVIEJOSE
#: vietose atskirai (`slenkstis.py` ir `prototipas.py`).
TIPAI = ("random_forest", "gradientinis", "mlp")

#: Tankus tinklelis: tolygus tarp 0,5 ir 0,9, tada vis ariau prie 1.
TAU = np.unique(np.concatenate([
    np.linspace(0.5, 0.9, 9),
    1 - np.logspace(-1, -6, 26),
]))


def _duomenys(reikia_skales: bool, aibe: str = "val"):
    """Grazina (X, y, skale) nurodytai vertinimo aibei.

    Parquet skaitomas VIENA karta. Mokymo aibe (1,7 mln. x 36 = ~490 MB)
    reikalinga tik MLP normalizavimui, todel is jos isskaiciuojama skale
    (72 skaiciai) ir aibe iskart atleidziama. Laikant ja atmintyje viso
    ciklo metu, kiti modeliai nebetelpa.
    """
    from src.duomenys import pozymiai, skaidymas

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, _, y_kat = pozymiai.atrinkti(df, tikrinti=False)
    del df
    gc.collect()

    skale = None
    if reikia_skales:
        # StandardScaler deterministinis, tad perskaiciuota skale tapati
        # tai, kuri buvo naudota mokant (ji su modeliu neissaugota - zr.
        # modulio pabaigos pastaba).
        Xtr = X.iloc[idx["train"]]
        skale = pozymiai.Skale().fit(Xtr)
        del Xtr
        gc.collect()

    Xv, yv = X.iloc[idx[aibe]].copy(), y_kat.to_numpy()[idx[aibe]]
    del X, y_kat
    gc.collect()
    return Xv, yv, skale


def tikimybes(raktas: str, Xv, skale, zyma: str):
    """Ikelia issaugota modeli pagal zyma ir grazina (P, klases)."""
    import joblib

    kelias = APMOKYTI / f"{zyma}.joblib"
    if not kelias.exists():
        raise SystemExit(f"Nerasta {kelias} - pirma paleiskite mokyma.")

    d = joblib.load(kelias)

    if raktas == "random_forest":
        return d.predict_proba(Xv), d.classes_

    if raktas == "gradientinis":
        m = d["modelis"]
        try:                      # sliuze GPU nera - delsa matuojama CPU
            m.set_params(device="cpu")
        except Exception:
            pass
        return m.predict_proba(Xv), d["kodavimas"].classes_

    if raktas == "mlp":
        # ⚠️ Skale su modeliu NEISSAUGOTA, todel perskaiciuojama is train.
        # StandardScaler yra deterministinis, tad rezultatas tapatus - bet
        # diegimui to nepakanka (zr. modulio pastaba apacioje).
        import tensorflow as tf
        modelis = tf.keras.models.load_model(kelias.with_suffix(".keras"))
        return modelis.predict(skale.transform(Xv), batch_size=4096, verbose=0), \
               d["kodavimas"].classes_

    raise KeyError(raktas)


def _sprendimas(P: np.ndarray, klases, tau: float) -> np.ndarray:
    """Ataka skelbiama tik jei bendra ataku tikimybe virsija tau."""
    i_ben = list(klases).index(GERYBINE)
    ataku_tik = 1 - P[:, i_ben]
    P_be_ben = P.copy()
    P_be_ben[:, i_ben] = -1          # geriausia ATAKOS klase
    argmax_ataka = np.asarray(klases)[P_be_ben.argmax(axis=1)]
    return np.where(ataku_tik > tau, argmax_ataka, GERYBINE)


def taskas(P: np.ndarray, klases, yv, tau: float) -> dict:
    """Vieno operacinio tasko rodikliai."""
    from sklearn.metrics import f1_score
    pred = _sprendimas(P, klases, tau)
    ben = yv == GERYBINE
    return {
        "tau": round(float(tau), 8),
        "fpr": float((pred[ben] != GERYBINE).mean()),
        "ataku_aptikta": float((pred[~ben] != GERYBINE).mean()),
        "macro_f1": f1_score(yv, pred, average="macro", zero_division=0),
        "tikslumas": float((pred == yv).mean()),
    }


def kreive(P: np.ndarray, klases, yv) -> pd.DataFrame:
    """FPR, atakų aptikimas ir macro-F1 kiekvienam tau."""
    return pd.DataFrame([taskas(P, klases, yv, t) for t in TAU])


def argmax_taskas(P, klases, yv) -> dict:
    """Dabartinis (argmax) taskas - atskaitos linija."""
    from sklearn.metrics import f1_score
    pred = np.asarray(klases)[P.argmax(axis=1)]
    ben = yv == GERYBINE
    return {
        "tau": np.nan,
        "fpr": float((pred[ben] != GERYBINE).mean()),
        "ataku_aptikta": float((pred[~ben] != GERYBINE).mean()),
        "macro_f1": f1_score(yv, pred, average="macro", zero_division=0),
        "tikslumas": float((pred == yv).mean()),
    }


def parinkti(k: pd.DataFrame, biudzetas: float) -> pd.Series:
    """Maziausias tau, tenkinantis FPR <= biudzetas.

    Maziausias, nes FPR mazeja augant tau: imant maziausia tinkama,
    aptikimas lieka didziausias is visu, kurie telpa i biudzeta.
    """
    tinka = k[k.fpr <= biudzetas]
    if tinka.empty:
        raise ValueError(f"Nei vienas tau netenkina FPR <= {biudzetas}")
    return tinka.loc[tinka.tau.idxmin()]


def _lentele(t: pd.DataFrame, aibe: str = "val") -> str:
    sk = [r"% GENERUOJAMA is rezultatai/darbiniai/slenkscio_taskai.csv",
          r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.slenkstis",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          + r">{\centering\arraybackslash}p{2.0cm}" * 4 + r"@{}}",
          r"\toprule",
          r"\textbf{Modelis} & \textbf{Sprendimo taškas} & \textbf{FPR} "
          r"& \textbf{Atakų aptikta} & \textbf{macro-F1} \\",
          r"\midrule"]
    def sk_(x, n=3):
        return "---" if pd.isna(x) else f"{x:.{n}f}".replace(".", ",")
    for modelis, g in t.groupby("modelis", sort=False):
        for i, (_, e) in enumerate(g.iterrows()):
            vardas = modelis if i == 0 else ""
            taskas = "argmax" if pd.isna(e.tau) else f"$\\tau$ = {sk_(e.tau, 4)}"
            sk.append(r"%s & %s & %s~\%% & %s~\%% & %s \\" % (
                vardas, taskas, sk_(e.fpr * 100, 2),
                sk_(e.ataku_aptikta * 100, 1), sk_(e.macro_f1)))
        sk.append(r"\addlinespace")
    sk[-1] = r"\bottomrule"
    isnasa = (r"Slenkstis parenkamas tik validacijos aibėje: "
              r"mažiausias $\tau$, tenkinantis klaidingų teigiamų biudžetą. "
              r"Modeliai nepermokomi.")
    if aibe == "test":
        # Isnasa privalo pasakyti, kad tau atkeliavo is kitos aibes. Be to
        # lentele atrodo taip, tarsi tau butu parinktas cia pat.
        isnasa = (r"Rodikliai išmatuoti \textbf{testavimo} aibėje. $\tau$ "
                  r"parinktas validacijos aibėje ir čia netaikomas iš "
                  r"naujo: perrinkimas testavimo aibėje būtų nutekėjimas. "
                  r"Modeliai nepermokomi.")
    sk += [r"\end{tabularx}",
           r"\vspace{2pt}",
           r"\raggedright\scriptsize " + isnasa,
           r"\endgroup"]
    return "\n".join(sk) + "\n"


def _tau_is_val(modeliai) -> dict[str, float]:
    """Operaciniai taskai, parinkti ant val. Perskaiciavimo cia NEBUNA.

    Tai vienintelis kelias, kuriuo tau patenka i test rezima. Jei val
    tasko failo nera, darbas nutraukiamas: perrinkti tau ant test butu
    nutekejimas, kuri protokolo 21 punktas ivardija kaip antra pagal
    tikimybe, ir jis butu nematomas rezultatuose.
    """
    kelias = DARBINIAI / "slenkscio_taskai.csv"
    if not kelias.exists():
        raise SystemExit(
            f"Nerasta {kelias}.\n"
            f"Pirma parinkite tau ant val:\n"
            f"  python -m src.eksperimentai.slenkstis")
    t = pd.read_csv(kelias)
    t = t[t.taskas == "slenkstis"]
    tau = dict(zip(t.modelis, t.tau))

    truksta = [m["rodomas"] for m in modeliai if m["rodomas"] not in tau]
    if truksta:
        raise SystemExit(
            f"slenkscio_taskai.csv nera tau siems modeliams: {truksta}\n"
            f"Turimi: {sorted(tau)}")
    return tau


def _taikyti_test(modeliai, n) -> None:
    """Taiko val tau test aibei. Naujas tau cia neparenkamas niekada.

    Isvestis rasoma i ATSKIRUS failus: val taskai ir kreives lieka
    nepaliestos. Tai ta pati taisykle, del kurios `rezultatai.csv` gavo
    `aibe` stulpeli - test rezultatas neturi uzimti val rezultato vietos.
    """
    tau = _tau_is_val(modeliai)

    Xv, yv, skale = _duomenys(
        reikia_skales=any(m["reikia_skales"] for m in modeliai), aibe="test")
    print(f"\nTEST {len(Xv):,} eilutes · "
          f"gerybiniu {int((yv == GERYBINE).sum()):,}")
    print("tau imamas IS VAL - cia neperrenkamas\n")

    eil = []
    for m in modeliai:
        vardas = m["rodomas"]
        P, klases = tikimybes(m["tipas"], Xv, skale, m["zyma"])
        am = argmax_taskas(P, klases, yv)
        pt = taskas(P, klases, yv, float(tau[vardas]))
        for zyma, e in (("argmax", am), ("slenkstis", pt)):
            eil.append({"modelis": vardas, "taskas": zyma, "aibe": "test",
                        **{x: e[x] for x in ("tau", "fpr", "ataku_aptikta",
                                             "macro_f1", "tikslumas")}})
        print(f"{vardas}")
        print(f"   argmax          FPR {am['fpr']*100:6.2f} %   aptikta "
              f"{am['ataku_aptikta']*100:5.1f} %   macro-F1 {am['macro_f1']:.4f}")
        print(f"   tau={pt['tau']:.4f} (val)  FPR {pt['fpr']*100:6.2f} %   "
              f"aptikta {pt['ataku_aptikta']*100:5.1f} %   "
              f"macro-F1 {pt['macro_f1']:.4f}")
        # Protokolo patikra Nr. 4: ar val operacinis taskas persikelia.
        # Rezultatas rasomas, koks bebutu - tai vienintele sios dienos
        # patikra, kurios rezultato nezinau is anksto.
        if pt["fpr"] > 2 * n.biudzetas:
            print(f"   [!] test FPR {pt['fpr']*100:.2f} % virsija biudzeta "
                  f"{n.biudzetas*100:g} % daugiau nei 2x - "
                  f"operacinis taskas NEPERSIKELE")
        del P
        gc.collect()

    DARBINIAI.mkdir(parents=True, exist_ok=True)
    LENTELES.mkdir(parents=True, exist_ok=True)
    t = pd.DataFrame(eil)
    t.to_csv(DARBINIAI / "slenkscio_taskai_test.csv", index=False)
    (LENTELES / "slenkstis_test.tex").write_text(
        _lentele(t, aibe="test"), encoding="utf-8")
    print("\nIssaugota: slenkscio_taskai_test.csv · lenteles/slenkstis_test.tex")
    print("val failai NEPALIESTI.")


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("--biudzetas", type=float, default=0.01)
    a.add_argument("--seed", type=int, default=42)
    a.add_argument("--modeliai", nargs="+", choices=list(TIPAI),
                   default=list(TIPAI),
                   help="tik sie modeliai; naudinga, kai Random Forest "
                        "netelpa i atminti")
    a.add_argument("--taikyti", choices=("val", "test"), default="val",
                   help="val: parinkti tau (numatytoji); "
                        "test: TAIKYTI val tau test aibei, neperrenkant")
    n = a.parse_args()

    from src.modeliai.bazinis import rasti_issaugotus
    # Tik 8 kategoriju formuluote: slenkscio taisykle remiasi "Benign"
    # stulpeliu tikimybiu matricoje, o 34 klasiu modelyje tokio stulpelio
    # nera - butu `ValueError` viduryje ciklo.
    modeliai = [m for m in rasti_issaugotus(APMOKYTI, n.seed)
                if m["tipas"] in n.modeliai and m.get("formuluote") == "8kat"]
    if not modeliai:
        raise SystemExit(f"Aplanke {APMOKYTI} nerasta modeliu su seed {n.seed}.")

    if n.taikyti == "test":
        return _taikyti_test(modeliai, n)

    Xv, yv, skale = _duomenys(
        reikia_skales=any(m["reikia_skales"] for m in modeliai))
    print(f"val {len(Xv):,} eilutes · gerybiniu {int((yv == GERYBINE).sum()):,}")
    print(f"FPR biudzetas: {n.biudzetas*100:g} %\n")

    kreives, taskai = [], []
    for m in modeliai:
        raktas, vardas = m["tipas"], m["rodomas"]
        P, klases = tikimybes(raktas, Xv, skale, m["zyma"])
        k = kreive(P, klases, yv)
        k.insert(0, "modelis", vardas)
        kreives.append(k)

        am = argmax_taskas(P, klases, yv)
        pt = parinkti(k, n.biudzetas)
        for zyma, e in (("argmax", am), ("slenkstis", pt)):
            taskai.append({"modelis": vardas, "taskas": zyma, **{
                x: (e[x] if isinstance(e, dict) else e[x])
                for x in ("tau", "fpr", "ataku_aptikta", "macro_f1", "tikslumas")}})

        print(f"{vardas}")
        print(f"   argmax      FPR {am['fpr']*100:6.2f} %   aptikta "
              f"{am['ataku_aptikta']*100:5.1f} %   macro-F1 {am['macro_f1']:.4f}")
        print(f"   tau={pt.tau:.4f}  FPR {pt.fpr*100:6.2f} %   aptikta "
              f"{pt.ataku_aptikta*100:5.1f} %   macro-F1 {pt.macro_f1:.4f}")
        print(f"   -> FPR sumazejo {am['fpr']/max(pt.fpr, 1e-9):.0f}x, "
              f"macro-F1 pakito {(pt.macro_f1-am['macro_f1'])/am['macro_f1']*100:+.1f} %\n")
        del P
        gc.collect()

    DARBINIAI.mkdir(parents=True, exist_ok=True)
    LENTELES.mkdir(parents=True, exist_ok=True)
    # Paleidus dalimis (--modeliai) ankstesniu modeliu eilutes islaikomos.
    def _sujungti(nauja: pd.DataFrame, kelias: Path) -> pd.DataFrame:
        if kelias.exists():
            sena = pd.read_csv(kelias)
            # Salinamos ir tos pacios eilutes senu vardu (be varianto
            # skliaustuose) - kitaip po pervadinimo lenteleje lieka dublikatai.
            baze = {m.split(" (")[0] for m in nauja.modelis.unique()}
            sena = sena[~sena.modelis.isin(nauja.modelis.unique())
                        & ~sena.modelis.isin(baze)]
            nauja = pd.concat([sena, nauja], ignore_index=True)
        eile = {m["rodomas"]: i for i, m in enumerate(modeliai)}
        nauja["_e"] = nauja.modelis.map(eile).fillna(99)
        return nauja.sort_values("_e", kind="stable").drop(columns="_e")

    _sujungti(pd.concat(kreives, ignore_index=True),
              DARBINIAI / "slenkscio_kreives.csv").to_csv(
        DARBINIAI / "slenkscio_kreives.csv", index=False)
    t = _sujungti(pd.DataFrame(taskai), DARBINIAI / "slenkscio_taskai.csv")
    t.to_csv(DARBINIAI / "slenkscio_taskai.csv", index=False)
    (LENTELES / "slenkstis.tex").write_text(_lentele(t), encoding="utf-8")
    print(f"Issaugota: slenkscio_kreives.csv · slenkscio_taskai.csv · "
          f"lenteles/slenkstis.tex")


if __name__ == "__main__":
    main()
