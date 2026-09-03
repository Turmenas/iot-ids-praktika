# -*- coding: utf-8 -*-
"""Svoriu jautrumo analize (3 uzduotis, T5).

Klausimas: ar rikiuote priklauso nuo to, kad tikslumui daviau 30 %, o ne 25 %?

DVI DALYS:
  A. Plane numatytas zondas: kiekvienam kriterijui +/-10 p. p., likusieji
     perskirstomi proporcingai -> 8 rinkiniai. Fiksuojama, kiek kartu
     keiciasi pirmi trys prizurimi metodai.
  B. Kadangi A dalis nieko nepakeite, ieskoma TIKROS ribos: (1) ar pora
     apskritai gali apsiversti (dominavimas), (2) jei taip — kokio svorio
     tam reiketu. Tai stipresnis teiginys uz "±10 p. p. nieko nekeicia":
     dominavimo atveju rezultatas nepriklauso nuo JOKIU svoriu.

Rezultatas irasomas toks, koks yra — ir jei patvirtina rikiuote, ir jei ne.

Paleidimas:
    python -m src.eksperimentai.jautrumas
"""
from __future__ import annotations

from pathlib import Path

from src.eksperimentai.matrica import SVORIAI, ikelti, svertine

SAKNIS = Path(__file__).resolve().parents[2]
ISVESTIS = SAKNIS / "ataskaita" / "lenteles" / "jautrumas.tex"
POKYTIS = 0.10

VARDAI = {
    "kokybe": "aptikimo kokybės",
    "disbalansas": "klaidingų teigiamų",
    "resursai": "resursų poreikio",
    "interpretuojamumas": "interpretuojamumo",
}
TRUMPAI = {"Sprendimų medis (CART)": "Sprendimų medis",
           "Daugiasluoksnis perceptronas": "MLP"}

# Poros, kurios ataskaitai idomios: kiekviena kelia konkretu klausima.
POROS = [
    ("XGBoost", "Random Forest"),
    ("Random Forest", "Daugiasluoksnis perceptronas"),
    ("XGBoost", "Sprendimų medis (CART)"),
    ("Sprendimų medis (CART)", "Random Forest"),
]


def trumpai(v: str) -> str:
    return TRUMPAI.get(v, v)


def perskirstyti(kriterijus: str, naujas: float) -> dict[str, float]:
    """Vienam kriterijui nustatomas naujas svoris; likusieji proporcingai."""
    assert 0.0 < naujas < 1.0, f"{kriterijus}: svoris {naujas} uz ribu"
    kiti = {k: v for k, v in SVORIAI.items() if k != kriterijus}
    mastelis = (1.0 - naujas) / sum(kiti.values())
    w = {kriterijus: naujas}
    w.update({k: v * mastelis for k, v in kiti.items()})
    assert abs(sum(w.values()) - 1.0) < 1e-9
    return w


def rikiuote(eilutes, w):
    poros = [(e["metodas"], round(svertine(e, w), 4)) for e in eilutes]
    poros.sort(key=lambda p: (-p[1], p[0]))
    return poros


def dominuoja(a: dict, b: dict) -> bool:
    """A dominuoja B: ne blogesnis pagal VISUS kriterijus ir bent vienu geresnis."""
    return (all(a[k] >= b[k] for k in SVORIAI)
            and any(a[k] > b[k] for k in SVORIAI))


def kritinis_svoris(a: dict, b: dict) -> list[tuple[str, float]]:
    """Kokio svorio reiketu, kad pora apsiverstu. Grazina [(kriterijus, riba)]."""
    dabar = svertine(a) - svertine(b)
    ribos = []
    for k in SVORIAI:
        for i in range(1, 100):
            w = perskirstyti(k, i / 100)
            if (dabar > 0) != (svertine(a, w) - svertine(b, w) > 0):
                ribos.append((k, i / 100))
                break
    return ribos


def main() -> None:
    visi = ikelti()
    priz = [e for e in visi if e["blokas"] == "prizurimi"]
    d = {e["metodas"]: e for e in priz}

    # --- A dalis: +/-10 p. p. ---
    baze_top3 = [m for m, _ in rikiuote(priz, SVORIAI)[:3]]
    print("BAZINE rikiuote (pirmi trys):", " > ".join(trumpai(m) for m in baze_top3))
    pokyciai = 0
    for k in SVORIAI:
        for delta in (POKYTIS, -POKYTIS):
            w = perskirstyti(k, SVORIAI[k] + delta)
            top3 = [m for m, _ in rikiuote(priz, w)[:3]]
            pokyciai += top3 != baze_top3
    print(f"A dalis: pirmi trys pasikeite {pokyciai} kartus is 8\n")

    # --- B dalis: tikros ribos ---
    isvados = []
    for a, b in POROS:
        skirtumas = svertine(d[a]) - svertine(d[b])
        if dominuoja(d[a], d[b]):
            atsakymas = "dominavimas"
            ribos = []
        else:
            ribos = kritinis_svoris(d[a], d[b])
            atsakymas = "riba" if ribos else "neapsiverstu"
        isvados.append({"a": a, "b": b, "skirtumas": skirtumas,
                        "tipas": atsakymas, "ribos": ribos})
        print(f"{trumpai(a):18s} vs {trumpai(b):18s} {skirtumas:+.2f}  {atsakymas}"
              + ("  " + ", ".join(f"{VARDAI[k]} -> {r:.2f}" for k, r in ribos) if ribos else ""))

    ISVESTIS.write_text(i_latex(isvados, pokyciai), encoding="utf-8")
    print(f"\n[OK] -> {ISVESTIS.relative_to(SAKNIS)}")


def i_latex(isvados, pokyciai) -> str:
    sk = [r"% GENERUOJAMA: python -m src.eksperimentai.jautrumas",
          r"% Ranka NELIESTI.",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{4pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}p{5.4cm}"
          r">{\centering\arraybackslash}p{1.6cm}"
          r">{\raggedright\arraybackslash}X@{}}",
          r"\toprule",
          r"\textbf{Palyginimas} & \textbf{Skirtumas} "
          r"& \textbf{Kada apsiverstų} \\",
          r"\midrule"]
    for iv in isvados:
        if iv["tipas"] == "dominavimas":
            paaiskinimas = (r"\textbf{Niekada.} Pirmasis ne blogesnis pagal "
                            r"visus keturis kriterijus, todėl jokie svoriai "
                            r"rezultato nekeičia")
        elif iv["ribos"]:
            dalys = [r"%s svoris turėtų pasiekti %s (dabar %s)"
                     % (VARDAI[k], ("%.2f" % r).replace(".", ","),
                        ("%.2f" % SVORIAI[k]).replace(".", ","))
                     for k, r in iv["ribos"]]
            paaiskinimas = "; ".join(dalys)
        else:
            paaiskinimas = "Neapsiverstų nė prie vieno svorio"
        sk.append(r"%s prieš %s & %s & %s \\" % (
            trumpai(iv["a"]), trumpai(iv["b"]),
            ("%+.2f" % iv["skirtumas"]).replace(".", ",").replace("+", "$+$"),
            paaiskinimas))
        sk.append(r"\addlinespace[2pt]")
    sk += [r"\bottomrule", r"\end{tabularx}", r"\endgroup"]
    return "\n".join(sk) + "\n"


if __name__ == "__main__":
    main()
