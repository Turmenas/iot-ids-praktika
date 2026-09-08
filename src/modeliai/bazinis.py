# -*- coding: utf-8 -*-
"""
Bendras modeliu sasajos kontraktas.

KODEL VIENODA SASAJA
--------------------
Nuo sio kontrakto tiesiogiai priklauso, ar 6 uzduotis (metodu palyginimas)
bus vienas ciklas, ar keturios dienos ranku darbo. Todel jis fiksuojamas
PRIES pirma modeli, o ne derinamas prie ju.

AUTOKODERIO ISLYGA — numatyta is anksto, ne po fakto
----------------------------------------------------
Trys priziurimi modeliai klasifikuoja i 8 kategorijas, o autokoderis
duoda tik anomalijos iverti. Bendro macro-F1 stulpelio visiems keturiems
sudaryti negalima (numatyta 2 uzduotyje, 2.8 poskyryje).

Kontrakte tai isreiksta dviem dalykais:

  `priziurimas`   - pagal ji `paleisti.py` zino, kuriu metriku modeliui
                    skaiciuoti negalima. Be sio lauko klaida isliptu
                    eksperimentu ciklo VIDURYJE kaip ValueError.

  `predict_proba` - apibreziamas kaip "ivertis, kurio DIDESNE reiksme
                    reiskia didesne atakos tikimybe", o ne kaip tikimybiu
                    matrica. Priziurimiems tai (n, k) matrica; autokoderiui
                    (n,) atkurimo paklaida. Bendras yra tik rikiavimas,
                    ir butent jo reikia PR-AUC bei ROC-AUC skaiciavimui.
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class Modelis(ABC):
    """Visi keturi darbo modeliai realizuoja si kontrakta."""

    #: Vardas, patenkantis i rezultatai.csv stulpeli `modelis`.
    vardas: str = "?"

    #: Ar modelis mokomas su etiketemis. Autokoderiui - False.
    priziurimas: bool = True

    #: Ar modeliui butinas normalizavimas (pozymiai.Skale).
    #: Medziu ansambliams - ne; MLP ir autokoderiui - taip.
    reikia_skales: bool = False

    def __init__(self, konfig: dict | None = None, seed: int = 42) -> None:
        self.konfig = dict(konfig or {})
        self.seed = seed
        self.klases_: np.ndarray | None = None
        self.mokymo_laikas_s: float | None = None
        self._modelis = None

    # ─── Privalomi metodai ───────────────────────────────────────────

    @abstractmethod
    def _fit(self, X_train, y_train, X_val, y_val) -> None:
        """Tikrasis mokymas. Kvieciamas is `fit`, kuris matuoja laika."""

    @abstractmethod
    def predict(self, X) -> np.ndarray:
        """Klasiu etiketes (priziurimiems) arba 0/1 (autokoderiui)."""

    @abstractmethod
    def predict_proba(self, X) -> np.ndarray:
        """Ivertis: didesne reiksme = didesne atakos tikimybe.

        Priziurimiems - (n, k) tikimybiu matrica stulpeliu tvarka
        `self.klases_`. Autokoderiui - (n,) atkurimo paklaida.
        """

    @abstractmethod
    def _issaugoti(self, kelias: Path) -> None:
        """Issaugo pati modeli. Plėtinį parenka realizacija."""

    # ─── Bendra logika ───────────────────────────────────────────────

    def fit(self, X_train, y_train, X_val=None, y_val=None) -> "Modelis":
        """Mokymas su laiko matavimu.

        `X_val` naudojamas ankstyvam stabdymui arba slenkscio kalibravimui;
        modeliams, kuriems jo nereikia, jis tiesiog ignoruojamas. TEST aibe
        cia nepatenka niekada (protokolo 19 punktas).
        """
        t0 = time.perf_counter()
        self._fit(X_train, y_train, X_val, y_val)
        self.mokymo_laikas_s = time.perf_counter() - t0
        return self

    def inferencijos_delsa_us(self, X, kartojimai: int = 3) -> float:
        """
        Gryna inferencijos delsa mikrosekundemis vienam irasui.

        Matuojama ATSKIRAI nuo srauto lango sukaupimo laiko (2 uzduoties
        12 radinys): `meidan2018nbaiot` skelbia 174 ms "aptikimo laika",
        i kuri iskaitytas ir lango kaupimas, todel su sio skaiciaus
        gretinti negalima.

        Imamas MINIMUMAS is kartojimu, ne vidurkis: minimumas maziau
        jautrus atsitiktinei sistemos apkrovai.
        """
        laikai = []
        for _ in range(kartojimai):
            t0 = time.perf_counter()
            self.predict(X)
            laikai.append((time.perf_counter() - t0) / len(X) * 1e6)
        return min(laikai)

    def issaugoti(self, kelias: Path) -> Path:
        """Issaugo modeli ir salia jo - metaduomenis (protokolo atkartojamumas)."""
        kelias = Path(kelias)
        kelias.parent.mkdir(parents=True, exist_ok=True)
        self._issaugoti(kelias)
        kelias.with_suffix(".json").write_text(json.dumps({
            "modelis": self.vardas,
            "priziurimas": self.priziurimas,
            "seed": self.seed,
            "konfig": self.konfig,
            "klases": None if self.klases_ is None else list(map(str, self.klases_)),
            "mokymo_laikas_s": self.mokymo_laikas_s,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        return kelias

    def papildomi_failai(self, kelias: Path) -> list[Path]:
        """Failai, kuriuos `_issaugoti` sukuria SALIA pagrindinio.

        Keras modeliai saugomi atskirame `.keras` faile, todel be sio
        metodo `dydis_mb` grazintu tik apvalkalo dydi - 0,00 MB. Modelio
        dydis yra vienas is keturiu resursu kriterijaus rodikliu, tad
        tyliai neteisingas nulis butu blogiau uz jo nebuvima.
        """
        return []

    def dydis_mb(self, kelias: Path) -> float:
        """Modelio dydis diske, iskaitant papildomus failus."""
        kelias = Path(kelias)
        failai = [kelias] + [f for f in self.papildomi_failai(kelias) if f.exists()]
        return sum(f.stat().st_size for f in failai) / 1024 / 1024


# ─── Issaugotu modeliu paieska ──────────────────────────────────────

#: Failo priesaga -> (vardas ataskaitoje, ar butinas normalizavimas)
TIPAI: dict[str, tuple[str, bool]] = {
    "random_forest": ("Random Forest", False),
    "gradientinis": ("XGBoost", False),
    "mlp": ("MLP", True),
    "autoencoder": ("Autokoderis", True),
}


def rasti_issaugotus(aplankas, seed: int = 42) -> list[dict]:
    """Suranda issaugotus modelius aplanke.

    Vardai NIEKUR nekalami: `slenkstis.py` ir `prototipas.py` juos turejo
    ikaltus, ir po failu pervadinimo abu luzo - kiekvienas atskirai.
    Paieska yra viena, todel ir taisyti reikia vienoje vietoje.

    Grazina po zodyna: zyma · tipas · vardas · konfigas · variantas ·
    rodomas · reikia_skales · turi_skale.
    """
    from pathlib import Path as _P

    rasti = []
    for f in sorted(_P(aplankas).glob(f"*_seed{seed}.joblib")):
        if f.name.endswith(".skale.joblib"):
            continue
        zyma = f.stem
        tipas = next((k for k in TIPAI if zyma.startswith(k)), None)
        if tipas is None:
            continue
        vardas, reikia_skales = TIPAI[tipas]
        konfigas = zyma.split("_8kat")[0].split("_dvejetaine")[0]
        variantas = "suderintas" if "derintas" in konfigas else "bazinis"
        rasti.append({
            "zyma": zyma, "tipas": tipas, "vardas": vardas,
            "konfigas": konfigas, "variantas": variantas,
            "rodomas": f"{vardas} ({variantas})",
            "reikia_skales": reikia_skales,
            "turi_skale": f.with_suffix(".skale.joblib").exists(),
        })
    return rasti


# ─── Registras — paleisti.py ieško modelio pagal konfigo vardą ───────

def gauti(raktas: str) -> type[Modelis]:
    """Grazina modelio klase pagal `konfig/*.yaml` lauka `modelis`."""
    import importlib

    # Modulis ir klase, o ne jau importuoti objektai: kitaip vieno modelio
    # importas (pvz., TensorFlow) butu butinas ir paleidziant visai kita.
    registras = {
        "random_forest": ("random_forest", "RandomForest"),
        "gradientinis":  ("gradientinis", "Gradientinis"),
        "mlp":           ("mlp", "MLP"),
        "autoencoder":   ("autoencoder", "Autokoderis"),
    }
    if raktas not in registras:
        raise KeyError(f"Nezinomas modelis {raktas!r}. Yra: {sorted(registras)}")
    modulis, klase = registras[raktas]
    return getattr(importlib.import_module(f"src.modeliai.{modulis}"), klase)
