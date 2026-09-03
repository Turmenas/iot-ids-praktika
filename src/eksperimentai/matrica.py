# -*- coding: utf-8 -*-
"""Sprendimu matrica: CSV -> ataskaita/lenteles/matrica.tex (3 uzduotis, T4).

Lentele GENERUOJAMA, o ne rasoma ranka: jautrumo analize (T5) perskaiciuoja
svertines sumas, o rankinis perrasymas ivestu klaidu klase, kurios darbe
sazingai atsisakyta (zr. praktikos_planas.md, "Svarbiausias triukas").

Paleidimas:
    python -m src.eksperimentai.matrica
"""
from __future__ import annotations

import csv
from pathlib import Path

SAKNIS = Path(__file__).resolve().parents[2]
CSV = SAKNIS / "rezultatai" / "darbiniai" / "sprendimu_matrica.csv"
ISVESTIS = SAKNIS / "ataskaita" / "lenteles" / "matrica.tex"

# Svoriai — tab:kriterijai (T3). Suma privalo buti 1,00.
SVORIAI: dict[str, float] = {
    "kokybe": 0.30,
    "disbalansas": 0.30,
    "resursai": 0.25,
    "interpretuojamumas": 0.15,
}

BLOKAI = [
    ("prizurimi", r"\textit{Prižiūrimi --- 8 kategorijų klasifikavimas}"),
    ("neprizurimi", r"\textit{Neprižiūrimi --- dvejetainė anomalijų formuluotė}"),
]


def ikelti(kelias: Path = CSV) -> list[dict]:
    with open(kelias, encoding="utf-8", newline="") as f:
        eilutes = list(csv.DictReader(f))
    for e in eilutes:
        for k in SVORIAI:
            e[k] = int(e[k])
            assert 1 <= e[k] <= 5, f"{e['metodas']}: {k}={e[k]} nepatenka i 1-5"
    assert eilutes, "CSV tuscias"
    return eilutes


def svertine(e: dict) -> float:
    return sum(SVORIAI[k] * e[k] for k in SVORIAI)


def _saltinis(zyma: str) -> str:
    return zyma if zyma.startswith("(") else r"\cite{%s}" % zyma


def i_latex(eilutes: list[dict]) -> str:
    sk = [r"% GENERUOJAMA is rezultatai/darbiniai/sprendimu_matrica.csv",
          r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.matrica",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{4pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          r">{\centering\arraybackslash}p{1.15cm}"
          r">{\centering\arraybackslash}p{1.35cm}"
          r">{\centering\arraybackslash}p{1.15cm}"
          r">{\centering\arraybackslash}p{1.45cm}"
          r">{\centering\arraybackslash}p{1.25cm}"
          r">{\raggedright\arraybackslash}p{1.9cm}@{}}",
          r"\toprule",
          r"\textbf{Metodas} & \textbf{Kokybė} & \textbf{Disba\-lansas}"
          r" & \textbf{Resur\-sai} & \textbf{Interpre\-tuojamumas}"
          r" & \textbf{Svertinė suma} & \textbf{Šalt.} \\",
          r"\multicolumn{1}{@{}l}{\itshape svoris} & 0,30 & 0,30 & 0,25 & 0,15"
          r" & --- & \\",
          r"\midrule"]

    for i, (raktas, antraste) in enumerate(BLOKAI):
        bloko = [e for e in eilutes if e["blokas"] == raktas]
        bloko.sort(key=svertine, reverse=True)
        if i:
            sk.append(r"\addlinespace")
        sk.append(r"\multicolumn{7}{@{}l}{%s} \\" % antraste)
        sk.append(r"\addlinespace[2pt]")
        for e in bloko:
            suma = f"{svertine(e):.2f}".replace(".", ",")   # tik skaicius, ne visa eilute
            sk.append(
                r"%s & %d & %d & %d & %d & \textbf{%s} & %s \\"
                % (e["metodas"], e["kokybe"], e["disbalansas"], e["resursai"],
                   e["interpretuojamumas"], suma, _saltinis(e["saltinis"]))
            )

    sk += [r"\bottomrule", r"\end{tabularx}", r"\endgroup"]
    return "\n".join(sk) + "\n"


def main() -> None:
    eilutes = ikelti()
    assert abs(sum(SVORIAI.values()) - 1.0) < 1e-9, "Svoriu suma ne 1,00"
    ISVESTIS.parent.mkdir(parents=True, exist_ok=True)
    ISVESTIS.write_text(i_latex(eilutes), encoding="utf-8")

    print(f"[OK] {len(eilutes)} metodai -> {ISVESTIS.relative_to(SAKNIS)}")
    for raktas, _ in BLOKAI:
        bloko = sorted((e for e in eilutes if e["blokas"] == raktas),
                       key=svertine, reverse=True)
        print(f"\n  {raktas}:")
        for vieta, e in enumerate(bloko, 1):
            print(f"    {vieta}. {e['metodas']:32s} {svertine(e):.2f}")


if __name__ == "__main__":
    main()
