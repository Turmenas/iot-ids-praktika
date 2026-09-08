# -*- coding: utf-8 -*-
"""Duomenu lenteles ataskaitai. Generuojama, ne rasoma ranka.

Paleidimas:
    python -m src.eksperimentai.lenteles

Isvestis: ataskaita/lenteles/imtis.tex
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
PASISKIRSTYMAS = SAKNIS / "rezultatai" / "darbiniai" / "imties_pasiskirstymas.csv"
ISVESTIS = SAKNIS / "ataskaita" / "lenteles" / "imtis.tex"

VARDAI = {
    "Benign": "Gerybinis srautas", "DDoS": "DDoS", "DoS": "DoS",
    "Recon": "Žvalgyba", "Spoofing": "Klastojimas", "Web": "Žiniatinklio",
    "BruteForce": "Grubi jėga", "Mirai": "Mirai",
}
EILE = ["DDoS", "DoS", "Recon", "Mirai", "Spoofing", "Benign", "Web", "BruteForce"]


def _sk(x, po=0):
    return f"{x:,.{po}f}".replace(",", " ").replace(".", ",").replace(" ", "\\,")


def main() -> None:
    from src.duomenys import etiketes

    d = pd.read_csv(PASISKIRSTYMAS)
    d["kategorija"] = d.klase.map(etiketes.KATEGORIJOS_NORM)
    g = d.groupby("kategorija").agg(
        etikeciu=("klase", "count"), pilnas=("pilnas_rinkinys", "sum"),
        unikaliu=("unikaliu", "sum"), imtyje=("imtyje", "sum")).loc[EILE]
    g["dubl"] = (1 - g.unikaliu / g.pilnas) * 100

    sk = [r"% GENERUOJAMA is rezultatai/darbiniai/imties_pasiskirstymas.csv",
          r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.lenteles",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          + r">{\raggedleft\arraybackslash}p{1.5cm}" * 2
          + r">{\raggedleft\arraybackslash}p{1.9cm}"
          + r">{\raggedleft\arraybackslash}p{1.9cm}"
          + r">{\raggedleft\arraybackslash}p{1.6cm}@{}}",
          r"\toprule",
          r"\textbf{Kategorija} & \textbf{Etikečių} & \textbf{Dubli\-katų} "
          r"& \textbf{Rinkinyje} & \textbf{Unikalių} & \textbf{Imtyje} \\",
          r"\midrule"]
    for k, e in g.iterrows():
        sk.append(r"%s & %d & %s~\%% & %s & %s & %s \\" % (
            VARDAI[k], e.etikeciu, _sk(e.dubl, 1), _sk(e.pilnas),
            _sk(e.unikaliu), _sk(e.imtyje)))
    sk += [r"\midrule",
           r"\textbf{Iš viso} & \textbf{%d} & \textbf{%s~\%%} & \textbf{%s} "
           r"& \textbf{%s} & \textbf{%s} \\" % (
               g.etikeciu.sum(), _sk((1 - g.unikaliu.sum()/g.pilnas.sum())*100, 1),
               _sk(g.pilnas.sum()), _sk(g.unikaliu.sum()), _sk(g.imtyje.sum())),
           r"\bottomrule", r"\end{tabularx}",
           r"\vspace{2pt}",
           r"\raggedright\scriptsize Riba \num{100000} taikyta \emph{etiketei}, "
           r"ne kategorijai, todėl DDoS su dvylika etikečių gauna daugiausia "
           r"vietų. Dublikatai šalinami prieš imties sudarymą.",
           r"\endgroup"]
    ISVESTIS.parent.mkdir(parents=True, exist_ok=True)
    ISVESTIS.write_text("\n".join(sk) + "\n", encoding="utf-8")
    print(f"[OK] {len(g)} kategorijos -> {ISVESTIS.relative_to(SAKNIS)}")
    print(g.assign(dubl=g.dubl.round(1)).to_string())


if __name__ == "__main__":
    main()
