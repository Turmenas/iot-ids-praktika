# -*- coding: utf-8 -*-
"""Suvestine 6 uzduociai: palyginimas ties FPR biudzetu.

Paleidimas:
    python -m src.eksperimentai.suvestine

Isvestis:
    ataskaita/lenteles/suvestine.tex     tab:suvestine
    ataskaita/paveikslai/kompromisai.pdf pav:kompromisai


KODEL SIS SKRIPTAS NELIECIA `test` AIBES
----------------------------------------
6 uzduotis nedaro nauju matavimu. Viskas skaiciuojama is failu, kuriuos
paliko 5 uzduoties prejimas per `test`:

    rezultatai/rezultatai.csv                  kokybe, delsa, dydis
    rezultatai/darbiniai/slenkscio_taskai_test.csv  operaciniai taskai
    rezultatai/darbiniai/perklasiu_tau_test.csv     aptikimas ties tau

Modeliai neikeliami, imtis neatidaroma. Priemimo kriterijus: po sio
skripto `rezultatai.csv` turi likti nepakites.


KODEL LENTELE TURI DVI DALIS
----------------------------
Autokoderis sprendzia dvejetaini uzdavini, priziurimi - astuoniu
kategoriju. Bendro macro-F1 stulpelio visiems keturiems sudaryti
negalima, ir tai numatyta dar 2 uzduotyje (2.8 poskyris). Cia ta pati
asimetrija igyvendinama ketvirta karta: po teksto, sprendimu matricos
sandaros ir modeliu kontrakto kode.


KODEL TIK SUDERINTOS KONFIGURACIJOS
-----------------------------------
Protokolo 3.2 punktas: i `test` eina tik suderinti konfigai. Bazinis MLP
i slenkscio lentele pateko del to, kad `rasti_issaugotus()` skenuoja
aplanka - tai ivardyta 5 skyriuje. Suvestineje jo nera: palyginimas turi
lyginti tai, kas buvo planuota lyginti.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
CSV = SAKNIS / "rezultatai" / "rezultatai.csv"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"
LENTELES = SAKNIS / "ataskaita" / "lenteles"
PAVEIKSLAI = SAKNIS / "ataskaita" / "paveikslai"

#: FPR biudzetas is 1 skyriaus: 1 % reiskia ~1000 signalu per para.
BIUDZETAS = 0.01

#: Suderintu konfigu vardai slenkscio faile -> vardas lenteleje.
PRIZIURIMI = {
    "XGBoost (suderintas)": "XGBoost",
    "Random Forest (suderintas)": "Random Forest",
    "MLP (suderintas)": "MLP",
}
#: Konfigu keliai `rezultatai.csv` faile - resursu rodikliams.
KONFIGAI = {
    "XGBoost": "konfig/gradientinis_derintas.yaml",
    "Random Forest": "konfig/random_forest_derintas.yaml",
    "MLP": "konfig/mlp_derintas.yaml",
}
EILE = ["XGBoost", "Random Forest", "MLP"]


def _sk(x: float, n: int = 3) -> str:
    """Skaicius su kableliu - taip, kaip visose kitose lentelese."""
    return f"{x:.{n}f}".replace(".", ",")


def _proc(x: float, n: int = 1) -> str:
    return f"{x * 100:.{n}f}".replace(".", ",") + "~\\%"


def ikelti() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    r = pd.read_csv(CSV)
    r = r[r["aibe"] == "test"]
    if r.empty:
        raise SystemExit("rezultatai.csv neturi test eiluciu - "
                         "pirma paleisti vertinti_test.bat")
    t = pd.read_csv(DARBINIAI / "slenkscio_taskai_test.csv")
    k = pd.read_csv(DARBINIAI / "perklasiu_tau_test.csv")
    return r, t, k


def aptikimas_ties_tau(k: pd.DataFrame, modelis: str) -> float:
    """Bendras atakų aptikimas, susvertas pagal kategoriju dydzius.

    Gerybine kategorija praleidziama: jai tas pats stulpelis reikstu
    klaidingus teigiamus, ne aptikima.
    """
    d = k[(k["modelis"] == modelis) & (k["kategorija"] != "Benign")]
    return float((d["n"] * d["pazymeta_ataka"]).sum() / d["n"].sum())


def surinkti(r: pd.DataFrame, t: pd.DataFrame, k: pd.DataFrame) -> list[dict]:
    eilutes: list[dict] = []

    for vardas in EILE:
        raktas = [s for s, v in PRIZIURIMI.items() if v == vardas][0]
        s = t[t["modelis"] == raktas].set_index("taskas")
        res = r[(r["konfig"] == KONFIGAI[vardas]) & (r["formuluote"] == "8kat")]
        if s.empty or res.empty:
            raise SystemExit(f"trūksta duomenų modeliui {vardas}")
        eilutes.append({
            "blokas": "priziurimi",
            "modelis": vardas,
            "f1_tau": float(s.loc["slenkstis", "macro_f1"]),
            "fpr_tau": float(s.loc["slenkstis", "fpr"]),
            "aptikta_tau": float(s.loc["slenkstis", "ataku_aptikta"]),
            "f1_argmax": float(s.loc["argmax", "macro_f1"]),
            "fpr_argmax": float(s.loc["argmax", "fpr"]),
            "dydis": float(res["modelio_dydis_mb"].mean()),
            "delsa": float(res["inferencija_us"].mean()),
        })

    a = r[(r["modelis"] == "Autokoderis") & (r["formuluote"] == "dvejetaine")]
    if a.empty:
        raise SystemExit("trūksta autokoderio test eiluciu")
    eilutes.append({
        "blokas": "neprziurimi",
        "modelis": "Autokoderis",
        "f1_tau": float(a["macro_f1"].mean()),
        "fpr_tau": float(a["fpr"].mean()),
        "aptikta_tau": aptikimas_ties_tau(k, "Autokoderis"),
        "f1_argmax": None,          # argmax autokoderiui neapibrezta
        "fpr_argmax": None,
        "dydis": float(a["modelio_dydis_mb"].mean()),
        "delsa": float(a["inferencija_us"].mean()),
        "pr_auc": float(a["pr_auc"].mean()),
    })
    return eilutes


def lentele(eilutes: list[dict]) -> str:
    geriausias = max(e["f1_tau"] for e in eilutes if e["blokas"] == "priziurimi")

    def eilute(e: dict) -> str:
        f1 = _sk(e["f1_tau"])
        if e["blokas"] == "priziurimi" and abs(e["f1_tau"] - geriausias) < 1e-9:
            f1 = r"\textbf{%s}" % f1
        fpr = _proc(e["fpr_tau"], 2)
        if e["fpr_tau"] > BIUDZETAS:
            fpr += r"\textsuperscript{b}"
        argmax = _sk(e["f1_argmax"]) if e["f1_argmax"] is not None else "---"
        return (f"{e['modelis']} & {f1} & {fpr} & "
                f"{_proc(e['aptikta_tau'])} & {argmax} & "
                f"{_sk(e['dydis'], 2)} & {_sk(e['delsa'], 1)} \\\\")

    p = [e for e in eilutes if e["blokas"] == "priziurimi"]
    n = [e for e in eilutes if e["blokas"] != "priziurimi"]

    isnasa = (
        r"Testavimo aibė, suderintos konfigūracijos, vidurkis iš 3 paleidimų. "
        r"Slenkstis $\tau$ kiekvienam modeliui parinktas validacijos aibėje. "
        r"\textsuperscript{a}~Dviejų blokų reikšmės tarpusavyje "
        r"nepalyginamos: prižiūrimi modeliai sprendžia aštuonių kategorijų "
        r"uždavinį, autokoderis --- dvejetainį, todėl jam didžiausios "
        r"tikimybės taškas neapibrėžtas. "
        r"\textsuperscript{b}~Peržengia 1~\% biudžetą "
        r"(žr. \ref{sec:patikimumas} poskyrį). "
        r"Autokoderio PR-AUC --- " + _sk(n[0].get("pr_auc", float("nan"))) +
        r", t.~y. rikiavimas geras, nors sprendimas ties biudžetu --- ne."
    )

    return "\n".join([
        "% Suvestine: palyginimas ties FPR biudzetu (6 uzduotis)",
        "% GENERUOJAMA is rezultatai.csv + slenkscio_taskai_test.csv",
        "% Ranka NELIESTI - paleisti: python -m src.eksperimentai.suvestine",
        r"\begingroup",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}X"
        r">{\centering\arraybackslash}p{1.9cm}"
        r">{\centering\arraybackslash}p{1.7cm}"
        r">{\centering\arraybackslash}p{1.9cm}"
        r">{\centering\arraybackslash}p{1.9cm}"
        r">{\centering\arraybackslash}p{1.6cm}"
        r">{\centering\arraybackslash}p{1.6cm}@{}}",
        r"\toprule",
        r"\textbf{Modelis} & \textbf{macro-F1 ties $\tau$} & \textbf{FPR} & "
        r"\textbf{Atakų aptikta} & \textbf{macro-F1 ties argmax} & "
        r"\textbf{Dydis, MB} & \textbf{Delsa, $\mu$s} \\",
        r"\midrule",
        r"\multicolumn{7}{@{}l}{\emph{Prižiūrimi, aštuonios "
        r"kategorijos}\textsuperscript{a}} \\",
        *[eilute(e) for e in p],
        r"\addlinespace",
        r"\multicolumn{7}{@{}l}{\emph{Neprižiūrimas, dvejetainė "
        r"formuluotė}\textsuperscript{a}} \\",
        *[eilute(e) for e in n],
        r"\bottomrule",
        r"\end{tabularx}",
        r"\vspace{2pt}",
        r"\raggedright\scriptsize " + isnasa,
        r"\endgroup",
        "",
    ])


def paveikslas(eilutes: list[dict]) -> Path:
    """Du kompromisai viename paveiksle.

    Kaireje - kaina, sumoketa uz biudzeta: kiek macro-F1 prarandama
    perejus nuo argmax prie tau. Desineje - kokybe ties biudzetu pries
    modelio dydi, logaritmine asimi, nes dydziai skiriasi keturiomis
    eilemis.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p = [e for e in eilutes if e["blokas"] == "priziurimi"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))

    # --- kaire: argmax pries tau -------------------------------------
    x = range(len(p))
    plocis = 0.36
    ax1.bar([i - plocis / 2 for i in x], [e["f1_argmax"] for e in p],
            plocis, color="#bbbbbb", edgecolor="#111111",
            label="ties argmax")
    ax1.bar([i + plocis / 2 for i in x], [e["f1_tau"] for e in p],
            plocis, color="#444444", edgecolor="#111111", hatch="//",
            label=r"ties FPR biudžetu")
    for i, e in enumerate(p):
        krytis = (e["f1_argmax"] - e["f1_tau"]) / e["f1_argmax"]
        ax1.text(i, max(e["f1_argmax"], e["f1_tau"]) + 0.02,
                 f"−{krytis * 100:.1f} %", ha="center", fontsize=9)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels([e["modelis"] for e in p])
    ax1.set_ylabel("macro-F1")
    ax1.set_ylim(0, 1.0)
    ax1.set_title("Kaina, sumokėta už klaidingų teigiamų biudžetą",
                  fontsize=10)
    ax1.legend(frameon=False, fontsize=9, loc="upper center", ncol=2)
    ax1.grid(axis="y", color="#dddddd", lw=0.6)
    ax1.set_axisbelow(True)

    # --- desine: kokybe pries dydi -----------------------------------
    for e in eilutes:
        zyma = "o" if e["blokas"] == "priziurimi" else "^"
        ax2.scatter(e["dydis"], e["f1_tau"], s=70, marker=zyma,
                    color="#111111" if e["modelis"] == "XGBoost" else "#777777",
                    zorder=3)
        # XGBoost ir Random Forest kokybe beveik sutampa, o dydziu
        # skiriasi 14 kartu - uzrasai issiskirstomi ranka, kad nesikloti.
        poslinkis = {"Random Forest": ((0, -18), "center")}
        xy, lyg = poslinkis.get(e["modelis"], ((8, 6), "left"))
        ax2.annotate(e["modelis"], (e["dydis"], e["f1_tau"]),
                     textcoords="offset points", xytext=xy, ha=lyg,
                     fontsize=9)
    ax2.set_xscale("log")
    ax2.set_xlabel("Modelio dydis, MB (logaritminė skalė)")
    ax2.set_ylabel(r"macro-F1 ties $\tau$")
    ax2.set_ylim(0, 1.0)
    ax2.set_xlim(0.03, 1500)
    ax2.set_title("Kokybė ties biudžetu prieš modelio dydį", fontsize=10)
    ax2.grid(color="#dddddd", lw=0.6)
    ax2.set_axisbelow(True)

    fig.tight_layout()
    PAVEIKSLAI.mkdir(parents=True, exist_ok=True)
    kelias = PAVEIKSLAI / "kompromisai.pdf"
    fig.savefig(kelias, bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)
    return kelias


def main() -> None:
    r, t, k = ikelti()
    eilutes = surinkti(r, t, k)

    LENTELES.mkdir(parents=True, exist_ok=True)
    (LENTELES / "suvestine.tex").write_text(lentele(eilutes), encoding="utf-8")
    kelias = paveikslas(eilutes)

    print(f"[OK] {(LENTELES / 'suvestine.tex').relative_to(SAKNIS)}")
    print(f"[OK] {kelias.relative_to(SAKNIS)}")
    print()
    for e in eilutes:
        argmax = "---" if e["f1_argmax"] is None else f"{e['f1_argmax']:.4f}"
        print(f"  {e['modelis']:14s} F1(tau)={e['f1_tau']:.4f} "
              f"argmax={argmax} FPR={e['fpr_tau'] * 100:.2f}% "
              f"aptikta={e['aptikta_tau'] * 100:.1f}% "
              f"dydis={e['dydis']:.2f}MB delsa={e['delsa']:.1f}us")
    # Kontrole: XGBoost aptikimas is per-kategoriju pjuvio turi sutapti
    # su slenkscio failu. Nesutapimas reikstu, kad failai is skirtingu
    # paleidimu.
    x_kat = aptikimas_ties_tau(k, "XGBoost")
    x_sl = [e for e in eilutes if e["modelis"] == "XGBoost"][0]["aptikta_tau"]
    print(f"\n  kontrole: XGBoost aptikimas is kategoriju {x_kat:.4f} "
          f"vs is slenkscio failo {x_sl:.4f} "
          f"(skirtumas {abs(x_kat - x_sl):.5f})")


if __name__ == "__main__":
    main()
