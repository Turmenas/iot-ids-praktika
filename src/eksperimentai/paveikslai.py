# -*- coding: utf-8 -*-
"""Ataskaitos paveikslai. Generuojama, ne piesiama ranka.

Paleidimas:
    python -m src.eksperimentai.paveikslai

Isvestis:
    ataskaita/paveikslai/architektura.pdf   sprendimo grandine (4 skyrius)
    ataskaita/paveikslai/kreives.pdf        FPR ir aptikimo kompromisas
    ataskaita/paveikslai/kategorijos.pdf    aptikimas pagal kategorijas

Sumaisymo matrica generuojama atskirai - `src/eksperimentai/klaidos.py`.


KODEL PILKA, O NE SPALVOTA
--------------------------
Ataskaita spausdinama. Todel tapatybe niekada neneša VIEN atspalvis:
kiekviena kreive turi ir savo linijos stiliu, ir uzrasa salia jos galo,
o stulpeliai skiriasi ir uzpildu (vienas istisinis, kitas brūkšniuotas).
Spalvotai perziurint informacijos nedaugeja - ir nesumazeja atspausdinus.


KODEL ROC IR PR KREIVIU NERA
----------------------------
Joms reiktu issaugotu prognoziu tikimybiu, o `paleisti.py` ju nesaugo
(5 uzduoties T0 spraga). Nubraizyti jas reikstu dar viena prejima per
`test` aibe del informacijos, kuri jau yra lenteleje skaiciais
(ROC-AUC, PR-AUC). Prejimas per test yra brangesnis uz paveiksla,
todel jo nedarome, o priezastis uzrasoma.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
PAVEIKSLAI = SAKNIS / "ataskaita" / "paveikslai"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"

#: FPR biudzetas is 1 skyriaus: 1 % reiskia ~1000 signalu per para.
BIUDZETAS_PROC = 1.0

#: Fiksuota eile ir stilius. Eile NEKAITALIOJAMA tarp paveikslu, kad
#: tas pats modelis visur atrodytu vienodai.
STILIUS = {
    "XGBoost (suderintas)":       {"c": "#111111", "ls": "-",  "v": "XGBoost"},
    "Random Forest (suderintas)": {"c": "#555555", "ls": "--", "v": "Random Forest"},
    "MLP (suderintas)":           {"c": "#888888", "ls": "-.", "v": "MLP"},
}
AUTOKODERIS = {"c": "#111111", "ls": ":", "v": "Autokoderis"}


def architektura() -> Path:
    """Sprendimo grandine: mokymas atskirtas nuo diegimo.

    Svarbiausia, ka schema turi parodyti: slenkstis tau ateina is
    VALIDACIJOS aibes, o ne is diegimo srauto - kitaip sistema
    kalibruotusi ant savo pacios duomenu.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 52); ax.axis("off")

    def deze(x, y, w, h, tekstas, pilkas=False, brūkšninis=False):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
            linewidth=1.1, edgecolor="#333333",
            facecolor="#eeeeee" if pilkas else "white",
            linestyle="--" if brūkšninis else "-"))
        ax.text(x + w / 2, y + h / 2, tekstas, ha="center", va="center",
                fontsize=7.4, linespacing=1.35)

    def rodykle(x1, y1, x2, y2, brūkšninė=False):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9,
            linewidth=0.9, color="#333333",
            linestyle="--" if brūkšninė else "-"))

    # ── Diegimas: krastinis sliuzas ──
    ax.text(1, 47.5, "DIEGIMAS — kraštinis šliuzas", fontsize=8,
            fontweight="bold", color="#222222")
    d = [("Srauto\nlangas", 10.5), ("36\npožymiai", 10.5),
         ("Normali-\nzavimas*", 10.5), ("Modelis", 10.5),
         ("Atakos\nįvertis", 10.5), ("Slenkstis\n$\\tau$", 10.5),
         ("Pavojaus\nsignalas", 12)]
    x = 1
    centrai = []
    for tekstas, w in d:
        deze(x, 33, w, 11, tekstas, pilkas=(tekstas == "Slenkstis\n$\\tau$"),
             brūkšninis=(tekstas == "Normali-\nzavimas*"))
        centrai.append((x, w))
        x += w + 2.5
    for i in range(len(centrai) - 1):
        x0, w0 = centrai[i]
        rodykle(x0 + w0, 38.5, centrai[i + 1][0], 38.5)

    # ── Mokymas: ne sliuze ──
    ax.text(1, 24.5, "MOKYMAS — atskirai, ne šliuze", fontsize=8,
            fontweight="bold", color="#222222")
    m = [("CICIoT2023\n45,0 mln.", 13), ("Valymas ir\ndublikatai", 13),
         ("Imtis\n2,43 mln.", 12), ("Skaidymas\n70/15/15", 12),
         ("Mokymas\n(train)", 12), ("Kalibravimas\n(val)", 13)]
    x = 1
    centrai_m = []
    for tekstas, w in m:
        deze(x, 8, w, 11, tekstas, pilkas=(tekstas == "Kalibravimas\n(val)"))
        centrai_m.append((x, w))
        x += w + 2.5
    for i in range(len(centrai_m) - 1):
        x0, w0 = centrai_m[i]
        rodykle(x0 + w0, 13.5, centrai_m[i + 1][0], 13.5)

    # ── Kas keliauja i sliuza ──
    rodykle(centrai_m[4][0] + centrai_m[4][1] / 2, 19,
            centrai[3][0] + centrai[3][1] / 2, 33, brūkšninė=True)
    rodykle(centrai_m[5][0] + centrai_m[5][1] / 2, 19,
            centrai[5][0] + centrai[5][1] / 2, 33, brūkšninė=True)

    ax.text(99, 2.5, "* tik neuroniniams modeliams; medžių ansambliams "
                     "normalizavimo nereikia",
            fontsize=6.3, ha="right", color="#555555")
    fig.tight_layout(pad=0.3)
    PAVEIKSLAI.mkdir(parents=True, exist_ok=True)
    kelias = PAVEIKSLAI / "architektura.pdf"
    # CreationDate isjungiama: kitaip kiekvienas paleidimas duoda kitokius
    # baitus, ir Git rodo pakeitima ten, kur turinys nepakito.
    fig.savefig(kelias, bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)
    return kelias


def _issaugoti(fig, vardas: str) -> Path:
    """Issaugo PDF be datos - kitaip Git rodo pakeitima ten, kur jo nera."""
    import matplotlib.pyplot as plt
    PAVEIKSLAI.mkdir(parents=True, exist_ok=True)
    kelias = PAVEIKSLAI / vardas
    fig.savefig(kelias, bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)
    return kelias


def kreives() -> Path:
    """Klaidingu teigiamu ir aptikimo kompromisas (validacijos aibe).

    KODEL VALIDACIJOS, O NE TESTAVIMO AIBE
    Paveikslas rodo, KAIP parenkamas operacinis taskas, o jis pagal
    protokola parenkamas validacijos aibeje. Braizyti test kreive ir
    ant jos zymeti val taska reikstu sumaisyti dvi aibes viename
    paveiksle.

    KODEL DU SKYDELIAI
    Pirmoji versija turejo viena. Trys priziurimi modeliai skiriasi
    ~3 procentiniais punktais, o autokoderis - desimtimis, todel
    bendroje 0-100 % aseje visos trys kreives suguldavo viena ant kitos
    ir Random Forest dingdavo po XGBoost linija. Tai atrode kaip klaida,
    nors buvo mastelio problema.

    Sprendimas - ne kitokia asis tam paciam skydeliui (du masteliai
    viename paveiksle klaidina), o du skydeliai su ta pacia x asimi:
    kairysis rodo, kad autokoderis yra kitos rusies, desinysis - kaip
    priziurimi skiriasi tarpusavyje.

    KODEL LOGARITMINE X ASIS
    Svarbus rezis yra 0,1-10 %, o tiesineje aseje visas biudzeto
    klausimas suspaustu i kraštine skiltį.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    k = pd.read_csv(DARBINIAI / "slenkscio_kreives.csv")
    t = pd.read_csv(DARBINIAI / "slenkscio_taskai.csv")
    t = t[t.taskas == "slenkstis"].set_index("modelis")
    ak = pd.read_csv(DARBINIAI / "autokoderio_slenkstis.csv")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))

    def priziurimi(ax, su_zymomis: bool):
        for vardas, s in STILIUS.items():
            g = k[k.modelis == vardas].sort_values("fpr")
            g = g[g.fpr > 0]
            if g.empty:
                continue
            ax.plot(g.fpr * 100, g.ataku_aptikta * 100, s["ls"], color=s["c"],
                    linewidth=1.6, label=s["v"], zorder=3)
            if su_zymomis and vardas in t.index:
                e = t.loc[vardas]
                ax.plot(e.fpr * 100, e.ataku_aptikta * 100, "o", color=s["c"],
                        markersize=6.5, markeredgecolor="white",
                        markeredgewidth=1.2, zorder=5)

    def tvarka(ax):
        ax.set_xscale("log")
        ax.set_xlim(0.06, 60)
        ax.axvline(BIUDZETAS_PROC, color="#999999", linewidth=1.0,
                   linestyle=(0, (4, 3)), zorder=1)
        ax.tick_params(labelsize=7.5)
        ax.grid(True, linewidth=0.5, color="#dddddd", zorder=0)
        ax.set_axisbelow(True)
        for r in ("top", "right"):
            ax.spines[r].set_visible(False)
        for r in ("left", "bottom"):
            ax.spines[r].set_color("#999999")

    # ─── Kairysis: visi keturi ───
    priziurimi(a1, su_zymomis=False)
    a1.plot(ak.FPR_proc, ak.ataku_aptikta_proc, AUTOKODERIS["ls"],
            color=AUTOKODERIS["c"], linewidth=1.6, marker="s", markersize=4.5,
            label=AUTOKODERIS["v"], zorder=3)
    tvarka(a1)
    a1.set_ylim(0, 103)
    a1.set_ylabel("Aptikta atakų, %", fontsize=8.5)
    a1.set_title("Visi modeliai", fontsize=8.5, pad=6)
    # Uzrasas i KAIRE nuo linijos: desineje ji uzguleja autokoderio kreive
    # (pastebeta perziurint sugeneruota paveiksla, ne rasant koda).
    a1.text(BIUDZETAS_PROC * 0.85, 62, "biudžetas\n1 %", fontsize=7,
            color="#555555", ha="right")
    a1.legend(fontsize=7.2, frameon=False, loc="lower right")

    # ─── Desinysis: priziurimi is arti ───
    priziurimi(a2, su_zymomis=True)
    tvarka(a2)
    a2.set_ylim(78, 100)
    a2.set_title("Prižiūrimi modeliai iš arti", fontsize=8.5, pad=6)
    a2.text(BIUDZETAS_PROC * 1.25, 83.0, "operaciniai\ntaškai", fontsize=7,
            color="#555555")

    fig.supxlabel("Klaidingi teigiami, % gerybinio srauto (logaritminė ašis)",
                  fontsize=8.5, y=0.02)
    fig.tight_layout(pad=0.5, rect=(0, 0.04, 1, 1))
    return _issaugoti(fig, "kreives.pdf")


def kategorijos() -> Path:
    """Aptikimas pagal kategorijas ties FPR biudzetu (testavimo aibe).

    KODEL `Benign` EILUTES NERA
    Jai tas pats stulpelis reikstu klaidingus teigiamus, o ne aptikima -
    du skirtingi dalykai vienoje aseje. Jos reiksme nurodoma parasu.

    Sio paveikslo darbas - parodyti, kad bendras "aptinka 88 %" yra
    svertinis vidurkis: per kategorijas rezis 37-100 %.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    p = pd.read_csv(DARBINIAI / "perklasiu_tau_test.csv")
    x = p[p.modelis == "XGBoost"].set_index("kategorija")
    a = p[p.modelis == "Autokoderis"].set_index("kategorija")

    fpr_x = x.loc["Benign", "pazymeta_ataka"] * 100 if "Benign" in x.index else float("nan")
    fpr_a = a.loc["Benign", "pazymeta_ataka"] * 100 if "Benign" in a.index else float("nan")
    x = x.drop(index="Benign", errors="ignore").sort_values("pazymeta_ataka")

    kat = list(x.index)
    y = np.arange(len(kat))
    h = 0.36

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.barh(y + h / 2 + 0.01, x.pazymeta_ataka * 100, height=h,
            color="#555555", edgecolor="white", linewidth=0.8, label="XGBoost")
    ak = [a.loc[k_, "pazymeta_ataka"] * 100 if k_ in a.index else 0 for k_ in kat]
    ax.barh(y - h / 2 - 0.01, ak, height=h, facecolor="white",
            edgecolor="#555555", linewidth=0.9, hatch="////", label="Autokoderis")

    for i, (v, w) in enumerate(zip(x.pazymeta_ataka * 100, ak)):
        ax.text(v + 1.2, i + h / 2 + 0.01, f"{v:.0f}".replace(".", ",") + " %",
                va="center", fontsize=7, color="#333333")
        ax.text(w + 1.2, i - h / 2 - 0.01, f"{w:.0f}".replace(".", ",") + " %",
                va="center", fontsize=7, color="#777777")

    ax.set_yticks(y, [f"{k_}\n$n$ = {int(x.loc[k_, 'n']):,}".replace(",", "\u2009")
                      for k_ in kat], fontsize=7.5)
    ax.set_xlim(0, 118)
    ax.set_xlabel("Pažymėta kaip ataka, %", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.grid(True, axis="x", linewidth=0.5, color="#dddddd", zorder=0)
    ax.set_axisbelow(True)
    for k_ in ("top", "right", "left"):
        ax.spines[k_].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    ax.text(1.0, -0.20, f"Gerybinis srautas (klaidingi teigiami): "
                        f"XGBoost {fpr_x:.2f} %, autokoderis {fpr_a:.2f} %"
                        .replace(".", ","),
            transform=ax.transAxes, ha="right", fontsize=7, color="#555555")
    fig.tight_layout(pad=0.4)
    return _issaugoti(fig, "kategorijos.pdf")


if __name__ == "__main__":
    for f in (architektura, kreives, kategorijos):
        k = f()
        print(f"[OK] {k.relative_to(SAKNIS)}  ({k.stat().st_size/1024:.0f} kB)")
