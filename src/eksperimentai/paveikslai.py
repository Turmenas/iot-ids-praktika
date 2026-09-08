# -*- coding: utf-8 -*-
"""Ataskaitos paveikslai. Generuojama, ne piesiama ranka.

Paleidimas:
    python -m src.eksperimentai.paveikslai

Isvestis: ataskaita/paveikslai/architektura.pdf
"""
from __future__ import annotations

from pathlib import Path

SAKNIS = Path(__file__).resolve().parents[2]
PAVEIKSLAI = SAKNIS / "ataskaita" / "paveikslai"


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


if __name__ == "__main__":
    k = architektura()
    print(f"[OK] {k.relative_to(SAKNIS)}  ({k.stat().st_size/1024:.0f} kB)")
