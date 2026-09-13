# -*- coding: utf-8 -*-
"""
Klaidu analize: per-klase metrikos ir sumaisymo struktura.

Paleidimas:
    python -m src.eksperimentai.klaidos
    python -m src.eksperimentai.klaidos --aibe val

Isvestis:
    rezultatai/darbiniai/perklasiu_<aibe>.csv    per-klase P/R/F1 + n
    ataskaita/lenteles/perklase.tex              lentele su n stulpeliu
    ataskaita/paveikslai/sumaisymas.pdf          geriausio modelio matrica


TEST AIBE CIA NEATIDAROMA
-------------------------
Viskas skaiciuojama is jau issaugotu sumaisymo matricu
(`sumaisymas_*_<aibe>.csv`), kurias sukure `paleisti.py`. Modeliai
neikeliami, prognozes neperskaiciuojamos, `imtis.parquet` neatidaroma.

Tai ne optimizacija, o 5 uzduoties taisykle: `test` liecama vienu
prejimu, o kiekvienas paskesnis pjuvis daromas is to, kas tada issaugota.


KODEL `n` STULPELIS BUTINAS
---------------------------
`UPLOADING_ATTACK` klase turi 179 test pavyzdzius; vienas kitoks
sprendimas keicia atkurima 0,6 p. p. Retos klases lemia macro-F1, todel
ju neapibreztumas yra PAGRINDINIO rodiklio neapibreztumas. Skaicius be
`n` atrodo tvirtesnis, nei yra.


ARGMAX, NE OPERACINIS TASKAS
----------------------------
Issaugotos matricos yra ties argmax. Ties FPR biudzetu per-klase pjuvis
skaiciuojamas atskirai (zr. `slenkstis.py`) - cia jo NERA, ir lenteles
isnasa tai pasako, kad skaitytojas nesugretintu su 5.2 skyriaus
skaiciais, gautais kitame taske.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"
LENTELES = SAKNIS / "ataskaita" / "lenteles"
PAVEIKSLAI = SAKNIS / "ataskaita" / "paveikslai"

GERYBINE = "Benign"

#: Konfigo kamienas -> vardas ataskaitoje. Ta pati eile kaip i_latex.py.
VARDAI = {
    "gradientinis_derintas": "XGBoost",
    "random_forest_derintas": "Random Forest",
    "mlp_derintas": "MLP",
    "autoencoder": "Autokoderis",
    "gradientinis": "XGBoost (bazinis)",
    "random_forest": "Random Forest (bazinis)",
    "mlp": "MLP (bazinis)",
}
EILE = ["XGBoost", "Random Forest", "MLP", "Autokoderis"]


def _isrinkti(vardas: str) -> tuple[str, int] | None:
    """`sumaisymas_<konfigas>_<formuluote>_seed<N>[_<aibe>].csv` -> (konfigas, seed)."""
    m = re.match(r"sumaisymas_(.+?)_(8kat|dvejetaine|34klases)_seed(\d+)"
                 r"(?:_(val|test))?$", vardas)
    return (m.group(1), int(m.group(3))) if m else None


def ikelti_matricas(aibe: str) -> dict[tuple[str, int], pd.DataFrame]:
    """Visos issaugotos nurodytos aibes matricos.

    `val` matricos issaugotos BE priesagos (jos sukurtos pries 2026-09-09,
    kai aibe i varda dar nebuvo iraSyta), `test` - su `_test`. Todel
    atranka pagal varda, o ne pagal vieninga sablona.
    """
    priesaga = "_test" if aibe == "test" else ""
    rasta = {}
    for f in sorted(DARBINIAI.glob("sumaisymas_*.csv")):
        vardas = f.stem
        if aibe == "test" and not vardas.endswith("_test"):
            continue
        if aibe == "val" and vardas.endswith("_test"):
            continue
        r = _isrinkti(vardas)
        if r is None:
            continue
        rasta[r] = pd.read_csv(f, index_col=0)
    if not rasta:
        raise SystemExit(f"Nerasta nei vienos `{aibe}` sumaisymo matricos "
                         f"aplanke {DARBINIAI}")
    return rasta


def perklase(M: pd.DataFrame) -> pd.DataFrame:
    """Precision / recall / F1 / n is sumaisymo matricos.

    Eilutes - tikra klase, stulpeliai - prognoze (taip rasa
    `metrikos.sumaisymo_matrica`).
    """
    A = M.to_numpy(dtype=float)
    tp = np.diag(A)
    n = A.sum(axis=1)                 # tikru pavyzdziu
    prognozuota = A.sum(axis=0)

    with np.errstate(divide="ignore", invalid="ignore"):
        prec = np.where(prognozuota > 0, tp / prognozuota, 0.0)
        rec = np.where(n > 0, tp / n, 0.0)
        f1 = np.where(prec + rec > 0, 2 * prec * rec / (prec + rec), 0.0)

    return pd.DataFrame({"klase": M.index, "n": n.astype(int),
                         "precision": prec, "recall": rec, "f1": f1})


def suvestine(matricos: dict) -> pd.DataFrame:
    """Per-klase metrikos, suvidurkintos per seed'us."""
    eil = []
    for (konfigas, seed), M in matricos.items():
        p = perklase(M)
        p.insert(0, "modelis", VARDAI.get(konfigas, konfigas))
        p.insert(1, "seed", seed)
        eil.append(p)
    d = pd.concat(eil, ignore_index=True)

    g = d.groupby(["modelis", "klase"], sort=False)
    a = g[["precision", "recall", "f1"]].mean()
    a["std_f1"] = g["f1"].std(ddof=1)
    a["n"] = g["n"].first()
    a["seedu"] = g["seed"].nunique()
    a = a.reset_index()
    a["_m"] = a.modelis.apply(lambda v: EILE.index(v) if v in EILE else 99)
    return a.sort_values(["_m", "n"], ascending=[True, False]).drop(columns="_m")


def klaidu_tipai(M: pd.DataFrame) -> dict:
    """Klaidos skirstomos pagal EKSPLOATACINE kaina, ne pagal dydi.

    Trys tipai, ir jie nera lygiaverciai:

      klaidingi teigiami  Benign -> ataka.  Signalas be pagrindo. Butent
                          jiems atrankoje skirta 30 % svorio (1 skyrius:
                          1 % reiskia ~1000 signalu per para).
      praleistos atakos   ataka -> Benign.  Signalo nera; aptikimas
                          neivyko.
      tarp ataku          ataka A -> ataka B.  Signalas IVYKO, tik
                          kategorija ivardyta ne ta. Analitikas pavojaus
                          vis tiek gauna.

    Bendras tikslumas visus tris skaiciuoja vienodai, todel jis matuoja
    ne tai, kas svarbu eksploatacijai.
    """
    A = M.to_numpy(dtype=float)
    kl = list(M.index)
    if GERYBINE not in kl:
        return {}
    i = kl.index(GERYBINE)
    visa = A.sum()
    klaidos = visa - np.diag(A).sum()
    kt = A[i, :].sum() - A[i, i]
    pa = A[:, i].sum() - A[i, i]
    return {
        "eiluciu": int(visa),
        "klaidu": int(klaidos),
        "klaidu_dalis": klaidos / visa,
        "klaidingi_teigiami": int(kt),
        "praleistos_atakos": int(pa),
        "tarp_ataku": int(klaidos - kt - pa),
        "tarp_ataku_dalis": (klaidos - kt - pa) / klaidos if klaidos else 0.0,
    }


def didziausios_painiavos(M: pd.DataFrame, kiek: int = 5) -> pd.DataFrame:
    """Stambiausios atskiros (tikra -> prognozuota) poros."""
    A = M.to_numpy(dtype=float)
    kl = list(M.index)
    p = [(kl[i], kl[j], int(A[i, j]))
         for i in range(len(kl)) for j in range(len(kl)) if i != j]
    p.sort(key=lambda x: -x[2])
    return pd.DataFrame(p[:kiek], columns=["tikra", "prognozuota", "eiluciu"])


def gerybinio_srauto_likimas(M: pd.DataFrame) -> pd.DataFrame:
    """I ka virsta tikras gerybinis srautas. 1 uzduoties prognozes patikra."""
    e = M.loc[GERYBINE]
    return pd.DataFrame({"i_klase": e.index, "eiluciu": e.to_numpy(),
                         "dalis": e.to_numpy() / e.sum()})


# ─── LaTeX ───────────────────────────────────────────────────────────

def _sk(x, n=3):
    return "---" if pd.isna(x) else f"{x:.{n}f}".replace(".", ",")


def _lentele(a: pd.DataFrame, aibe: str, modeliai: list[str]) -> str:
    sk = [r"% GENERUOJAMA is rezultatai/darbiniai/sumaisymas_*.csv",
          r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.klaidos",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          r">{\raggedleft\arraybackslash}p{1.6cm}"
          + r">{\centering\arraybackslash}p{1.9cm}" * 3 + r"@{}}",
          r"\toprule",
          r"\textbf{Kategorija} & \textbf{$n$} & \textbf{Tikslumas} "
          r"& \textbf{Atkūrimas} & \textbf{F1} \\",
          r"\midrule"]
    for m in modeliai:
        g = a[a.modelis == m]
        if g.empty:
            continue
        sk.append(r"\multicolumn{5}{@{}l}{\textbf{%s}} \\" % m)
        for _, e in g.iterrows():
            sk.append(r"\quad %s & %s & %s & %s & %s \\" % (
                e.klase, f"{int(e.n):,}".replace(",", "\\,"),
                _sk(e.precision), _sk(e.recall), _sk(e.f1)))
        sk.append(r"\addlinespace")
    sk[-1] = r"\bottomrule"
    kur = "testavimo" if aibe == "test" else "validacijos"
    sk += [r"\end{tabularx}",
           r"\vspace{2pt}",
           # ⚠️ Generuojamoje lenteleje NEGALI buti `\\ref` i etikete, kuri
           # apibrezta skyriaus faile: 2026-09-09 cia buvo `tab:rezultatai`,
           # o skyrius naudoja `tab:rezultatai_test`, ir PDF liko "??".
           # Generuojamas failas apie skyriaus etiketes nezino, todel jos
           # ivardijamos zodziais, ne nuoroda.
           r"\raggedright\scriptsize Rodikliai išmatuoti \textbf{%s} aibėje "
           r"ties \emph{argmax}, o ne ties klaidingų teigiamų biudžetu, todėl "
           r"su pagrindine aptikimo kokybės lentele tiesiogiai negretinami. "
           r"$n$ --- tikrų pavyzdžių skaičius; retose kategorijose vienas kitoks "
           r"sprendimas keičia atkūrimą per dešimtąsias procentinio punkto dalis." % kur,
           r"\endgroup"]
    return "\n".join(sk) + "\n"


def _tipu_lentele(t: pd.DataFrame, aibe: str) -> str:
    sk = [r"% GENERUOJAMA - paleisti: python -m src.eksperimentai.klaidos",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          + r">{\centering\arraybackslash}p{2.1cm}" * 4 + r"@{}}",
          r"\toprule",
          r"\textbf{Modelis} & \textbf{Klaidų iš viso} "
          r"& \textbf{Klaidingi teigiami} & \textbf{Praleistos atakos} "
          r"& \textbf{Tarp atakų} \\",
          r"\midrule"]
    for _, e in t.iterrows():
        sk.append(r"%s & %s~\%% & %s~\%% & %s~\%% & \textbf{%s~\%%} \\" % (
            e.modelis, _sk(e.klaidu_dalis * 100, 1),
            _sk(e.klaidingi_teigiami / e.klaidu * 100, 1),
            _sk(e.praleistos_atakos / e.klaidu * 100, 1),
            _sk(e.tarp_ataku_dalis * 100, 1)))
    kur = "testavimo" if aibe == "test" else "validacijos"
    sk += [r"\bottomrule", r"\end{tabularx}",
           r"\vspace{2pt}",
           r"\raggedright\scriptsize %s aibė, \emph{argmax}. Pirmasis stulpelis --- "
           r"klaidingai suklasifikuotų eilučių dalis; kiti trys --- tų klaidų "
           r"pasiskirstymas. \textbf{Tarp atakų} reiškia, kad pavojaus signalas "
           r"įvyko, o suklysta tik kategorija; eksploatacijai tai pigiausia "
           r"klaidos rūšis, nors bendras tikslumas ją skaičiuoja taip pat kaip "
           r"praleistą ataką." % kur,
           r"\endgroup"]
    return "\n".join(sk) + "\n"


# ─── Paveikslas ──────────────────────────────────────────────────────

def paveikslas(M: pd.DataFrame, vardas: str, aibe: str) -> Path:
    """Sumaisymo matrica, normalizuota PER EILUTE (t. y. atkurimas).

    Normalizuojama per eilute, o ne absoliuciais skaiciais: prie 84:1
    disbalanso absoliuti matrica rodytu tik tai, kad DDoS klasiu daug.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    A = M.to_numpy(dtype=float)
    N = A / np.clip(A.sum(axis=1, keepdims=True), 1, None)
    klases = list(M.index)

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.imshow(N, cmap="Greys", vmin=0, vmax=1)

    ax.set_xticks(range(len(klases)), klases, rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(klases)), klases, fontsize=7.5)
    ax.set_xlabel("Prognozuota kategorija", fontsize=8.5)
    ax.set_ylabel("Tikra kategorija", fontsize=8.5)

    for i in range(len(klases)):
        for j in range(len(klases)):
            if N[i, j] < 0.005:
                continue
            ax.text(j, i, f"{N[i, j]*100:.0f}".replace(".", ","),
                    ha="center", va="center", fontsize=7,
                    color="white" if N[i, j] > 0.55 else "#222222")

    ax.set_title(f"{vardas} — {aibe} aibė, atkūrimas kategorijoje (\\%)"
                 .replace("\\%", "%"), fontsize=9, pad=8)
    fig.tight_layout(pad=0.4)
    PAVEIKSLAI.mkdir(parents=True, exist_ok=True)
    kelias = PAVEIKSLAI / "sumaisymas.pdf"
    # CreationDate isjungiama - kitaip Git rodo pakeitima ten, kur turinys
    # nepakito (ta pati taisykle kaip paveikslai.py).
    fig.savefig(kelias, bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)
    return kelias


def main() -> None:
    a_arg = argparse.ArgumentParser()
    a_arg.add_argument("--aibe", choices=("val", "test"), default="test")
    a_arg.add_argument("--paveikslui", default="XGBoost",
                       help="kurio modelio matrica pieziama")
    n = a_arg.parse_args()

    matricos = ikelti_matricas(n.aibe)
    print(f"Rasta {len(matricos)} {n.aibe} matricos: "
          f"{sorted({k for k, _ in matricos})}")

    a = suvestine(matricos)
    DARBINIAI.mkdir(parents=True, exist_ok=True)
    a.to_csv(DARBINIAI / f"perklasiu_{n.aibe}.csv", index=False)

    # Lentele - tik daugiaklasiai modeliai: autokoderis turi dvi "klases"
    # (Benign / Ataka), ir jo eilutes toje pacioje lenteleje reikstu
    # palyginima, kurio nera (palyginimo asimetrija, 2.8 poskyris).
    modeliai = [m for m in EILE if m in set(a.modelis) and m != "Autokoderis"]
    LENTELES.mkdir(parents=True, exist_ok=True)
    (LENTELES / "perklase.tex").write_text(
        _lentele(a, n.aibe, modeliai), encoding="utf-8")

    # ─── Klaidu tipai pagal eksploatacine kaina ───
    tipai = []
    for konfigas, vardas in [(k, v) for k, v in VARDAI.items() if v in modeliai]:
        M = matricos.get((konfigas, 42))
        if M is None:
            continue
        t = klaidu_tipai(M)
        if t:
            tipai.append({"modelis": vardas, **t})
    if tipai:
        t = pd.DataFrame(tipai)
        t.to_csv(DARBINIAI / f"klaidu_tipai_{n.aibe}.csv", index=False)
        (LENTELES / "klaidu_tipai.tex").write_text(
            _tipu_lentele(t, n.aibe), encoding="utf-8")
        print(f"\nKlaidu tipai ({n.aibe}, argmax, seed 42):")
        for _, e in t.iterrows():
            print(f"  {e.modelis:16s} klaidu {e.klaidu:7,} ({e.klaidu_dalis*100:.1f} %)"
                  f" | klaid. teig. {e.klaidingi_teigiami/e.klaidu*100:4.1f} %"
                  f" | praleista {e.praleistos_atakos/e.klaidu*100:4.1f} %"
                  f" | TARP ATAKU {e.tarp_ataku_dalis*100:4.1f} %")

    # ─── Gerybinio srauto likimas: 1 uzduoties prognozes patikra ───
    print(f"\nGerybinio srauto likimas ({n.aibe}, argmax, seed 42):")
    for konfigas, vardas in [(k, v) for k, v in VARDAI.items()
                             if v in modeliai]:
        M = matricos.get((konfigas, 42))
        if M is None or GERYBINE not in M.index:
            continue
        g = gerybinio_srauto_likimas(M).sort_values("dalis", ascending=False)
        virsus = "  ".join(f"{r.i_klase} {r.dalis*100:.1f}%"
                           for _, r in g.head(3).iterrows())
        print(f"  {vardas:16s} {virsus}")

    # ─── Paveikslas ───
    kelias = None
    for konfigas, vardas in VARDAI.items():
        if vardas == n.paveikslui and (konfigas, 42) in matricos:
            kelias = paveikslas(matricos[(konfigas, 42)], vardas, n.aibe)
            break

    print(f"\n[OK] {len(a)} eilutes -> "
          f"{(DARBINIAI / f'perklasiu_{n.aibe}.csv').relative_to(SAKNIS)}")
    print(f"     {(LENTELES / 'perklase.tex').relative_to(SAKNIS)}")
    if kelias:
        print(f"     {kelias.relative_to(SAKNIS)}")
    else:
        print(f"     [!] paveikslas nepiestas - nerastas {n.paveikslui} seed 42")


if __name__ == "__main__":
    main()
