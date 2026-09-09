# -*- coding: utf-8 -*-
"""Eksperimentu rezultatai: CSV -> ataskaita/lenteles/*.tex (5 ir 6 uzduotys).

Skriptas paleidziamas po KIEKVIENO eksperimentu perleidimo. Skaiciai i
ataskaita niekada nerasomi ranka (zr. praktikos_planas.md, "Svarbiausias
triukas").

Paleidimas:
    python -m src.eksperimentai.i_latex

Ataskaitoje:
    \\lentele{rezultatai}     % pagrindines metrikos
    \\lentele{veikimas}       % delsa, mokymo laikas, modelio dydis


KODEL DVI LENTELES, O NE VIENA
------------------------------
Protokolo 24 punktas fiksuoja 15 stulpeliu. Jie i viena puslapio ploti
netelpa, o ir neturi: kokybes metrikos atsako i klausima "ar aptinka",
veikimo rodikliai - "ar telpa i sliuza". Tai du atskiri klausimai, ir 5
skyriuje jie aptariami atskirai.

KODEL AGREGAVIMAS
-----------------
CSV turi po eilute KIEKVIENAM paleidimui (protokolo 17 punktas: 3 seed'ai).
Lenteleje rodomas vidurkis +- standartinis nuokrypis. Sklaida yra ne
puosmena: protokolas skirtuma tarp modeliu laiko reiksmingu tik tada, kai
jis virsija paleidimu sklaida (dietterich1998tests).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
CSV = SAKNIS / "rezultatai" / "rezultatai.csv"
ISVESTIS = SAKNIS / "ataskaita" / "lenteles"

#: Protokolo 24 punkto schema. Trukstamas stulpelis = klaida, ne ispejimas.
SCHEMA: list[str] = [
    "modelis", "formuluote", "seed", "aibe",
    "macro_f1", "weighted_f1", "accuracy", "pr_auc", "roc_auc", "mcc", "fpr",
    "mokymo_laikas_s", "inferencija_us", "modelio_dydis_mb",
    "konfig", "data",
]

RAKTAI = ["modelis", "formuluote"]

#: Fiksuota eile - kad lenteles stulpeliu tvarka nesikeistu tarp paleidimu.
MODELIU_EILE = ["XGBoost", "Random Forest", "MLP", "Autokoderis",
                "Isolation Forest", "Sprendimu medis"]
FORMULUOCIU_EILE = ["8kat", "dvejetaine", "34klases"]

FORMULUOCIU_VARDAI = {
    "8kat": "8 kategorijos",
    "dvejetaine": "Dvejetainė",
    "34klases": "34 klasės",
}

#: (CSV stulpelis, antraste, skaitmenu po kablelio, ar didesnis geriau,
#:  ar ryskinti geriausia)
#:
#: Kokybes lenteleje ryskinama TIK macro-F1 - protokolo pagrindine metrika.
#: Tikslumo ryskinti negalima: tos pacios lenteles isnasa sako, kad prie
#: 41,8:1 santykio jis nera rodiklis, o ryskinimas teigtu priesinga.
KOKYBE = [
    ("macro_f1", r"macro-F1", 3, True, True),
    ("pr_auc", r"PR-AUC", 3, True, False),
    ("roc_auc", r"ROC-AUC", 3, True, False),
    ("mcc", r"MCC", 3, True, False),
    ("fpr", r"FPR", 4, False, False),
    ("accuracy", r"Tikslumas\textsuperscript{a}", 3, True, False),
]

VEIKIMAS = [
    ("mokymo_laikas_s", r"Mokymo laikas, s", 1, False, True),
    ("inferencija_us", r"Inferencija, $\mu$s", 2, False, True),
    ("modelio_dydis_mb", r"Dydis, MB", 2, False, True),
]


# ─── Pagalbines ──────────────────────────────────────────────────────

def _sk(x: float, n: int) -> str:
    """Skaicius lietuviskai: kablelis TIK skaiciuje, ne visoje eiluteje."""
    return f"{x:.{n}f}".replace(".", ",")


def _reiksme(vid: float, std: float, n_seed: int, sk_po: int) -> str:
    """Vidurkis su sklaida. "+- 0,000" nerodoma: rodomu tikslumu tai nulis,
    o nulinis nuokrypis lenteleje atrodo kaip informacija, kurios nera."""
    if n_seed < 2 or pd.isna(std) or round(std, sk_po) == 0:
        return _sk(vid, sk_po)
    return r"%s\,$\pm$\,%s" % (_sk(vid, sk_po), _sk(std, sk_po))


def _ekranuoti(t: str) -> str:
    return str(t).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def _rikiuoti(df: pd.DataFrame) -> pd.DataFrame:
    """Fiksuota eile; nezinomi modeliai/formuluotes - gale, abecele."""
    df = df.copy()
    df["_m"] = df["modelis"].apply(
        lambda v: MODELIU_EILE.index(v) if v in MODELIU_EILE else len(MODELIU_EILE))
    df["_f"] = df["formuluote"].apply(
        lambda v: FORMULUOCIU_EILE.index(v) if v in FORMULUOCIU_EILE
        else len(FORMULUOCIU_EILE))
    return (df.sort_values(["_f", "_m", "modelis", "formuluote"])
              .drop(columns=["_m", "_f"]).reset_index(drop=True))


# ─── Agregavimas ─────────────────────────────────────────────────────

def ikelti(kelias: Path | None = None) -> pd.DataFrame:
    # Kelias imamas kvietimo metu, o ne is numatytojo argumento: numatytasis
    # butu uzfiksuotas importo momentu ir testai negaletu jo pakeisti.
    kelias = Path(kelias) if kelias is not None else CSV

    if not kelias.exists() or kelias.stat().st_size == 0:
        raise SystemExit(
            f"{kelias} tuscias arba nerastas - pirma paleiskite eksperimentus:\n"
            f"  python -m src.eksperimentai.paleisti konfig/random_forest.yaml")

    df = pd.read_csv(kelias)
    if df.empty:
        raise SystemExit(f"{kelias} tuscias.")

    truksta = [s for s in SCHEMA if s not in df.columns]
    if truksta:
        raise SystemExit(
            f"CSV truksta stulpeliu: {truksta}\n"
            f"Laukiama protokolo 24 punkto schemos:\n  {', '.join(SCHEMA)}\n"
            f"Rasta:\n  {', '.join(df.columns)}"
        )
    return df


def atrinkti_aibe(df: pd.DataFrame, aibe: str) -> pd.DataFrame:
    """Palieka tik nurodytos vertinimo aibes eilutes.

    Tylaus numatytojo pasirinkimo cia nera sazmoningai: lentele su test
    skaiciais ir val isnasa (arba atvirksciai) yra tiksliai ta klaida,
    del kurios `aibe` stulpelis apskritai atsirado.
    """
    t = df[df["aibe"] == aibe]
    if t.empty:
        turimos = ", ".join(sorted(df["aibe"].dropna().unique())) or "nera"
        raise SystemExit(
            f"rezultatai.csv nera nei vienos `{aibe}` eilutes. "
            f"Turimos aibes: {turimos}")
    return t.reset_index(drop=True)


def agreguoti(df: pd.DataFrame) -> pd.DataFrame:
    """Vidurkis, standartinis nuokrypis ir seed'u skaicius kiekvienai porai."""
    skaitiniai = [s for s, *_ in KOKYBE + VEIKIMAS]

    # ⚠️ RAKTAI neapima `konfig`, todel bazinis ir suderintas to paties
    # modelio variantai patenka i TA PACIA grupe ir suvidurkinami. Skaicius
    # tada nera nei vieno is ju, o isnasa "is N paleidimu" rodo seed'u, ne
    # eiluciu skaiciu. Tylus vidurkis is dvieju skirtingu modeliu yra
    # blogiau uz jo nebuvima, todel cia jis pasakomas garsiai.
    for raktas, grupe in df.groupby(RAKTAI, sort=False):
        konfigai = sorted(grupe["konfig"].unique())
        if len(konfigai) > 1:
            print(f"  [!] {raktas}: {len(grupe)} eilutes is {len(konfigai)} "
                  f"konfiguraciju suvidurkinamos i viena: {konfigai}")
            print("      Lentele rodys vidurki tarp skirtingu modeliu. "
                  "Atrinkite viena konfiguracija arba praplėskite RAKTAI.")

    g = df.groupby(RAKTAI, sort=False)

    vid = g[skaitiniai].mean().add_suffix("__vid")
    std = g[skaitiniai].std(ddof=1).add_suffix("__std")
    n = g["seed"].nunique().rename("n_seed")

    return _rikiuoti(pd.concat([vid, std, n], axis=1).reset_index())


# ─── LaTeX ───────────────────────────────────────────────────────────

def _lentele(a: pd.DataFrame, stulpeliai: list, antraste: str,
             isnasa: str = "") -> str:
    plotis = "1.9cm" if len(stulpeliai) > 4 else "2.6cm"
    sk = [
        r"% GENERUOJAMA is rezultatai/rezultatai.csv",
        r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.i_latex",
        r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabularx}{\textwidth}{@{}"
        r">{\raggedright\arraybackslash}X"
        r">{\raggedright\arraybackslash}p{2.1cm}"
        + (r">{\centering\arraybackslash}p{%s}" % plotis) * len(stulpeliai)
        + r"@{}}",
        r"\toprule",
        r"\textbf{Modelis} & \textbf{Formuluotė} & "
        + " & ".join(r"\textbf{%s}" % a_ for _, a_, *_ in stulpeliai) + r" \\",
        r"\midrule",
    ]

    # Geriausia reiksme kiekviename stulpelyje - tik tarp tos pacios formuluotes
    geriausi: dict[tuple, float] = {}
    for kodas, _, _, didesnis, ryskinti in stulpeliai:
        if not ryskinti:
            continue
        for f, grupe in a.groupby("formuluote", sort=False):
            # Vienos eilutes grupeje geriausio nera - ji tokia viena.
            if len(grupe) < 2:
                continue
            v = grupe[f"{kodas}__vid"]
            if v.notna().any():
                geriausi[(kodas, f)] = v.max() if didesnis else v.min()

    ankstesne = None
    for _, e in a.iterrows():
        if ankstesne is not None and e["formuluote"] != ankstesne:
            sk.append(r"\addlinespace")
        ankstesne = e["formuluote"]

        langeliai = []
        for kodas, _, sk_po, _, _ in stulpeliai:
            vid, std = e[f"{kodas}__vid"], e[f"{kodas}__std"]
            if pd.isna(vid):
                langeliai.append("---")
                continue
            t = _reiksme(vid, std, int(e["n_seed"]), sk_po)
            if abs(vid - geriausi.get((kodas, e["formuluote"]), float("nan"))) < 1e-12:
                t = r"\textbf{%s}" % t
            langeliai.append(t)

        sk.append("%s & %s & %s \\\\" % (
            _ekranuoti(e["modelis"]),
            FORMULUOCIU_VARDAI.get(e["formuluote"], _ekranuoti(e["formuluote"])),
            " & ".join(langeliai)))

    sk += [r"\bottomrule", r"\end{tabularx}"]
    if isnasa:
        sk.append(r"\vspace{2pt}")
        sk.append(r"\raggedright\scriptsize %s" % isnasa)
    sk.append(r"\endgroup")
    sk.insert(0, "%% %s" % antraste)
    return "\n".join(sk) + "\n"


#: Kaip aibe ivardijama lenteles isnasoje. Isnasa privalo pasakyti, kuria
#: aibe skaiciai ismatuoti - kitaip val lentele nuo test lenteles skiriasi
#: tik skaiciais, o tai nera skirtumas, kuri kas nors pastebetu.
AIBIU_VARDAI = {
    "val": "validacijos aibėje",
    "test": "testavimo aibėje",
}


def main() -> None:
    a_arg = argparse.ArgumentParser()
    a_arg.add_argument("--aibe", choices=("val", "test"), default="val",
                       help="kurios vertinimo aibes rezultatus generuoti")
    a_arg.add_argument("--priesaga", default="",
                       help="pridedama prie isvesties failu vardu, pvz. _test")
    n = a_arg.parse_args()

    df = atrinkti_aibe(ikelti(), n.aibe)
    a = agreguoti(df)

    n_seed = sorted(a["n_seed"].unique())
    sklaida = ("vidurkis $\\pm$ standartinis nuokrypis iš %s paleidimų"
               % "/".join(str(n) for n in n_seed)) if max(n_seed) > 1 else \
              "vienas paleidimas, sklaida nematuota"
    kur = "Rezultatai išmatuoti " + AIBIU_VARDAI[n.aibe] + ". "

    ISVESTIS.mkdir(parents=True, exist_ok=True)
    p = n.priesaga

    (ISVESTIS / f"rezultatai{p}.tex").write_text(_lentele(
        a, KOKYBE, "Aptikimo kokybe",
        isnasa=kur +
               r"\textsuperscript{a}~Bendras tikslumas pateikiamas \emph{tik} "
               r"palyginimui su literatūra: prie 41,8:1 santykio jis nėra "
               r"rodiklis. Reikšmės --- " + sklaida + "."), encoding="utf-8")

    (ISVESTIS / f"veikimas{p}.tex").write_text(_lentele(
        a, VEIKIMAS, "Veikimo rodikliai",
        isnasa=kur +
               r"Inferencijos delsa matuojama gryna, atskirai nuo srauto lango "
               r"sukaupimo laiko; kraštinio šliuzo biudžetas --- 20--50~ms. "
               r"Reikšmės --- " + sklaida + "."), encoding="utf-8")

    print(f"[OK] aibe={n.aibe} · {len(df)} paleidimai -> {len(a)} eilutes")
    for f in (f"rezultatai{p}.tex", f"veikimas{p}.tex"):
        print(f"     {(ISVESTIS / f).relative_to(SAKNIS)}")
    print()
    for _, e in a.iterrows():
        print(f"  {e['modelis']:18s} {e['formuluote']:12s} "
              f"n={int(e['n_seed'])}  macro-F1={e['macro_f1__vid']:.4f}")


if __name__ == "__main__":
    main()
