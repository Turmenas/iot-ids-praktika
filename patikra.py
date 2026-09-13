"""
Aplinkos patikra. Paleidimas:  python patikra.py

Tikrina, ar visos priklausomybes idiegtos ir ar projekto struktura vietoje.
"""

import sys
from pathlib import Path

print(f"Python: {sys.version.split()[0]}  ({sys.executable})")
print()

BIBLIOTEKOS = [
    "pandas", "numpy", "pyarrow", "sklearn", "xgboost", "lightgbm",
    "imblearn", "tensorflow", "shap", "matplotlib", "seaborn", "yaml",
]

#: Bibliotekos, be kuriu VISKAS, isskyrus viena zingsni, veikia.
#: Ju trukumas nera klaida, bet turi buti matomas: 2026-09-13 paaiskejo,
#: kad `requirements-lock.txt` (sudarytas rugs. 1 d.) streamlit neturi,
#: nors prototipas be jo nepasileidzia. Svari aplinka butu prasidejusi
#: nuo "viskas gerai" ir luzusi tik ties 07_prototipas.bat.
PAPILDOMOS = {
    "streamlit": "07_prototipas.bat (demonstracija)",
}

trukstamos = []
for pav in BIBLIOTEKOS:
    try:
        modulis = __import__(pav)
        versija = getattr(modulis, "__version__", "?")
        print(f"  [OK] {pav:<14} {versija}")
    except ImportError:
        print(f"  [--] {pav:<14} TRUKSTA")
        trukstamos.append(pav)

for pav, kam in PAPILDOMOS.items():
    try:
        modulis = __import__(pav)
        versija = getattr(modulis, "__version__", "?")
        print(f"  [OK] {pav:<14} {versija}")
    except ImportError:
        print(f"  [  ] {pav:<14} nera - reikalinga tik: {kam}")

print()

SAKNIS = Path(__file__).resolve().parent
APLANKAI = [
    "ataskaita/skyriai", "ataskaita/lenteles", "ataskaita/paveikslai",
    "src/modeliai", "src/duomenys", "src/eksperimentai",
    "duomenys/raw", "duomenys/processed", "konfig",
    "rezultatai/apmokyti", "rezultatai/darbiniai",
]

for a in APLANKAI:
    zyme = "OK" if (SAKNIS / a).is_dir() else "--"
    print(f"  [{zyme}] {a}")

print()
if trukstamos:
    print("Truksta bibliotieku:", ", ".join(trukstamos))
    print("Idiekite:  pip install -r requirements.txt")
    sys.exit(1)

print("Aplinka paruosta.")
