"""
Konvertuoja eksperimentų rezultatus (CSV) į LaTeX lentelę.

Paleidimas:
    python -m src.eksperimentai.i_latex

Ataskaitoje naudojama:
    \\lentele{rezultatai}      % = \\input{lenteles/rezultatai.tex}

Svarbu: šis skriptas paleidžiamas po KIEKVIENO eksperimentų perleidimo.
Skaičiai į ataskaitą niekada nerašomi ranka.
"""

from pathlib import Path
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
CSV = SAKNIS / "rezultatai" / "rezultatai.csv"
ISVESTIS = SAKNIS / "ataskaita" / "lenteles"

# CSV stulpelis -> kaip vadinsis lentelėje
STULPELIAI = {
    "modelis": "Modelis",
    "accuracy": "Tikslumas",
    "precision_macro": "Precision",
    "recall_macro": "Recall",
    "f1_macro": "F1",
    "fpr": "FPR",
    "inferencijos_ms": "Delsa (ms)",
}


def main() -> None:
    if not CSV.exists():
        raise SystemExit(f"Nerastas {CSV} — pirma paleiskite eksperimentus.")

    df = pd.read_csv(CSV)

    trukstami = set(STULPELIAI) - set(df.columns)
    if trukstami:
        raise SystemExit(f"CSV trūksta stulpelių: {sorted(trukstami)}")

    lentele = df[list(STULPELIAI)].rename(columns=STULPELIAI)

    ISVESTIS.mkdir(parents=True, exist_ok=True)
    kelias = ISVESTIS / "rezultatai.tex"

    lentele.to_latex(
        kelias,
        index=False,
        float_format="%.3f",
        escape=False,
        column_format="l" + "S" * (len(STULPELIAI) - 1),  # siunitx lygiavimas
        caption="DI metodų veikimo rodikliai CICIoT2023 duomenų rinkinyje",
        label="tab:rezultatai",
        position="H",
    )
    print(f"Įrašyta: {kelias}  ({len(lentele)} eilutės)")


if __name__ == "__main__":
    main()
