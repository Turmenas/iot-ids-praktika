# -*- coding: utf-8 -*-
"""
Pozymiu paruosimas: 39 -> 36 ir normalizavimas.

IGYVENDINA PROTOKOLO 5.3 (claude/uzduotis_03_planas.md):
  salinami TRYS tiksliai isvestiniai pozymiai, salinama SARASU,
  o ne automatiniu koreliacijos filtru.

Paleidimas:
    python -m src.duomenys.pozymiai        # patikra ant imtis.parquet


KODEL SARASU, O NE AUTOMATINIU FILTRU
-------------------------------------
Du nepriklausomi argumentai, abu ismatuoti siuose duomenyse:

1. KORELIACIJOS FILTRAS NEPAGAUTU. `Variance` = `Std`^2 yra TIKSLUS rysys,
   bet ju tiesine Pearson koreliacija tera 0,737. Iprastas 0,95 slenkstis
   sios poros nepasalintu, nors vienas stulpelis neneša nieko naujo.

2. MAZOS DISPERSIJOS FILTRAS PASALINTU NE TUOS. Sesi stulpeliai
   (`ece_flag_number`, `cwr_flag_number`, `Telnet`, `SMTP`, `IRC`, `IGMP`)
   daugiau nei 99,5 % eiluciu turi ta pacia reiksme, todel automatinis
   filtras juos ismestu. Bet ju vidurkiai 4-22 kartus didesni butent
   reciausiose klasese: `IRC` x21,8 ties BACKDOOR_MALWARE (IRC valdymo
   kanalas), `Telnet` ir `SMTP` ties RECON-* (prievadu skenavimas),
   `cwr_flag_number` x15,6 ties UPLOADING_ATTACK. Tai klases, kurios ir
   lemia macro-F1.

Todel salinama tik tai, kas irodyta tapatybe, ir tai daroma samoningai.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.duomenys import etiketes

SAKNIS = Path(__file__).resolve().parents[2]
IMTIS = SAKNIS / "duomenys" / "processed" / "imtis.parquet"
ETIKETE = "Label"

#: Stulpelis -> kodel salinamas. Tapatybes patikrintos 2026-09-06
#: darbineje imtyje (2 425 937 eilutes): nesutapimu 0.
SALINAMI: dict[str, str] = {
    "Variance": "= Std^2 (tikslus rysys; tiesine koreliacija tik 0,737)",
    "Tot sum":  "= AVG * Number",
    "Tot size": "= AVG (sutampa tiksliai); paliekamas AVG, nes jis "
                "tiesiogiai interpretuojamas kaip vidutinis paketo dydis",
}

#: Stulpeliai, kuriuos automatinis filtras pasalintu KLAIDINGAI.
#: Laikomi cia, kad butu aisku: jie palikti samoningai, o ne pramiegoti.
SAUGOMI: dict[str, str] = {
    "ece_flag_number": "x7,7 ties XSS ir MITM-ARPSPOOFING",
    "cwr_flag_number": "x15,6 ties UPLOADING_ATTACK",
    "Telnet":          "x9,6 ties RECON-HOSTDISCOVERY",
    "SMTP":            "x9,0 ties RECON-HOSTDISCOVERY",
    "IRC":             "x21,8 ties BACKDOOR_MALWARE (IRC valdymo kanalas)",
    "IGMP":            "x11,9 ties XSS",
}

LAUKIAMA_POZYMIU = 36


def pozymiu_stulpeliai(df: pd.DataFrame) -> list[str]:
    """36 pozymiai: viskas, kas nera Label ir nera SALINAMI saraše."""
    p = [c for c in df.columns if c != ETIKETE and c not in SALINAMI]
    if len(p) != LAUKIAMA_POZYMIU:
        raise ValueError(
            f"Tiketasi {LAUKIAMA_POZYMIU} pozymiu, gauta {len(p)}. "
            f"Trukstami SALINAMI: {sorted(set(SALINAMI) - set(df.columns))}"
        )
    return p


def patikrinti_tapatybes(df: pd.DataFrame, rtol: float = 1e-9) -> dict[str, int]:
    """
    Patikrina, ar salinimo pagrindas TEBEGALIOJA siuose duomenyse.

    Kvieciama kaskart pries salinant. Jei veidrodis ar imtis pasikeistu,
    salinimas taptu nepagristas - ir tai turi pasirodyti cia, o ne kaip
    prastesnis modelio rezultatas.
    """
    tapatybes = {
        "Variance = Std^2":       (df["Variance"], df["Std"] ** 2),
        "Tot size = AVG":         (df["Tot size"], df["AVG"]),
        "Tot sum = AVG * Number": (df["Tot sum"], df["AVG"] * df["Number"]),
    }
    rezultatas = {}
    for vardas, (a, b) in tapatybes.items():
        n = int((~np.isclose(a, b, rtol=rtol, atol=1e-9, equal_nan=True)).sum())
        rezultatas[vardas] = n
        if n:
            raise ValueError(
                f"Tapatybe '{vardas}' NEBEGALIOJA: {n:,} nesutapimu is {len(a):,}. "
                f"Salinimo pagrindas dingo - nesalinti aklai, patikrinti duomenis."
            )
    return rezultatas


def atrinkti(df: pd.DataFrame, tikrinti: bool = True):
    """
    Grazina (X, y_etikete, y_kategorija).

    X - 36 pozymiai; y_etikete - 34 klases; y_kategorija - 8 kategorijos
    (pagrindine uzduoties formuluote, protokolo 12 punktas).
    """
    if tikrinti:
        patikrinti_tapatybes(df)
    X = df[pozymiu_stulpeliai(df)].astype("float64")
    y = df[ETIKETE].astype(str)
    kat = y.map(etiketes.KATEGORIJOS_NORM)
    if kat.isna().any():
        bloga = sorted(y[kat.isna()].unique())
        raise ValueError(f"Etiketes be kategorijos: {bloga}")
    return X, y, kat


# ─── Normalizavimas — fit TIK ant train ──────────────────────────────

class Skale:
    """
    StandardScaler su apsauga nuo nutekejimo.

    `fit` leidziama tik viena karta ir tik su mokymo aibe. Antras kvietimas
    meta klaida - butent taip nutekejimas ir atsiranda: kai kas nors
    "perskaiciuoja" skale ant viso rinkinio, nes taip patogiau.

    Medziu ansambliams (RF, XGBoost) normalizavimo nereikia; ji butina
    MLP ir autokoderiui.
    """

    def __init__(self) -> None:
        from sklearn.preprocessing import StandardScaler
        self._s = StandardScaler()
        self.pritaikyta = False
        self.stulpeliai: list[str] | None = None

    def fit(self, X_train: pd.DataFrame) -> "Skale":
        if self.pritaikyta:
            raise RuntimeError(
                "Skale jau pritaikyta. Pakartotinis fit() beveik visada reiskia, "
                "kad ji pritaikoma ant val/test - o tai nutekejimas."
            )
        self._s.fit(X_train)
        self.stulpeliai = list(X_train.columns)
        self.pritaikyta = True
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        if not self.pritaikyta:
            raise RuntimeError("Pirma fit() ant MOKYMO aibes.")
        if list(X.columns) != self.stulpeliai:
            raise ValueError("Stulpeliu tvarka nesutampa su ta, ant kurios fit().")
        return self._s.transform(X)

    def issaugoti(self, kelias: Path) -> None:
        import joblib
        kelias.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"scaler": self._s, "stulpeliai": self.stulpeliai}, kelias)


# ─── Patikra ─────────────────────────────────────────────────────────

def _patikra() -> None:
    if not IMTIS.exists():
        raise SystemExit(f"Nerasta {IMTIS} - pirma: python -m src.duomenys.ikelimas imtis")

    df = pd.read_parquet(IMTIS)
    print(f"Imtis: {len(df):,} eiluciu, {df.shape[1]} stulpeliai\n")

    print("Tapatybes (salinimo pagrindas):")
    for vardas, n in patikrinti_tapatybes(df).items():
        print(f"  [OK] {vardas:24s} nesutapimu {n}")

    print(f"\nSalinami {len(SALINAMI)}:")
    for c, kodel in SALINAMI.items():
        print(f"  - {c:12s} {kodel}")

    print(f"\nSamoningai paliekami {len(SAUGOMI)} (mazos dispersijos filtras "
          f"juos ismestu):")
    for c, kodel in SAUGOMI.items():
        print(f"  + {c:18s} {kodel}")

    X, y, kat = atrinkti(df)
    print(f"\nX: {X.shape}  (laukta {LAUKIAMA_POZYMIU} pozymiu)")
    print(f"Etikeciu: {y.nunique()}   Kategoriju: {kat.nunique()}")
    print("\nKategoriju pasiskirstymas:")
    print(kat.value_counts().to_string())

    assert X.shape[1] == LAUKIAMA_POZYMIU
    assert not X.isna().any().any(), "X yra trukstamu reiksmiu"
    assert np.isfinite(X.to_numpy()).all(), "X yra begaliniu reiksmiu"
    print("\n[OK] Visos patikros praejo")


if __name__ == "__main__":
    _patikra()
