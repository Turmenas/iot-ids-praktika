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
        #: Is isores paduoti eiluciu svoriai; None = skaiciuoti is y_train.
        self.svoriai_ = None
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

    def _ikelti(self, kelias: Path) -> None:
        """Atstato modeli is failo, kuri sukure `_issaugoti`.

        Pora `_issaugoti` / `_ikelti` laikoma vienoje vietoje sazmoningai:
        ikelimo logika jau buvo isbarstyta po `slenkstis.py` ir
        `prototipas.py`, ir po failu pervadinimo luzo abiejose vietose
        atskirai. Trecia kopija `paleisti.py` butu pakartojusi ta pacia
        klaida, todel ikelimas gyvena ten pat, kur issaugojimas.
        """
        raise NotImplementedError(
            f"{type(self).__name__} neturi `_ikelti` - ikelti negalima.")

    # ─── Bendra logika ───────────────────────────────────────────────

    def fit(self, X_train, y_train, X_val=None, y_val=None,
            svoriai=None) -> "Modelis":
        """Mokymas su laiko matavimu.

        `X_val` naudojamas ankstyvam stabdymui arba slenkscio kalibravimui;
        modeliams, kuriems jo nereikia, jis tiesiog ignoruojamas. TEST aibe
        cia nepatenka niekada (protokolo 19 punktas).

        `svoriai` - eiluciu svoriai, PADUODAMI is isores. Numatytuoju
        atveju jie skaiciuojami is `y_train` (`class_weight="balanced"`
        ekvivalentas), bet nematytu klasiu teste to nepakanka: pasalinus
        viena klase, likusiu svoriai persiskaiciuotu, ir permokytas
        modelis skirtusi nuo bazinio DVIEM dalykais vienu metu. Tada
        testas matuotu ne klases nebuvima, o klases nebuvima plius
        kitokia balansavima.
        """
        self.svoriai_ = svoriai
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

    @classmethod
    def ikelti(cls, kelias: Path) -> "Modelis":
        """Ikelia issaugota modeli kartu su jo metaduomenimis.

        `mokymo_laikas_s` imamas is salia gulincio `.json`, o NE matuojamas
        is naujo: modelis cia nemokomas, tad bet koks cia isvestas skaicius
        butu ne mokymo laikas, o ikelimo laikas su mokymo laiko etikete.
        """
        kelias = Path(kelias)
        meta_kelias = kelias.with_suffix(".json")
        meta = (json.loads(meta_kelias.read_text(encoding="utf-8"))
                if meta_kelias.exists() else {})

        m = cls(meta.get("konfig", {}), seed=meta.get("seed", 42))
        m._ikelti(kelias)
        m.mokymo_laikas_s = meta.get("mokymo_laikas_s")
        if m.klases_ is None and meta.get("klases"):
            m.klases_ = np.array(meta["klases"])
        return m

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
    formuluote · rodomas · reikia_skales · turi_skale.
    """
    import re
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
        # Formuluote isrenkama is zymos: slenkscio logika apibrezta TIK
        # 8 kategoriju uzduociai (ji remiasi "Benign" stulpeliu), todel
        # kviecianti puse turi galeti atsirinkti. Be sio lauko 34 klasiu
        # modelis patektu i `slenkstis.py` ir luztu ties `.index("Benign")`.
        m_f = re.search(r"_(8kat|dvejetaine|34klases)_seed", zyma)
        formuluote = m_f.group(1) if m_f else "?"
        konfigas = zyma.split(f"_{formuluote}_seed")[0]
        variantas = "suderintas" if "derintas" in konfigas else "bazinis"
        rasti.append({
            "zyma": zyma, "tipas": tipas, "vardas": vardas,
            "konfigas": konfigas, "variantas": variantas,
            "formuluote": formuluote,
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


#: Registro raktai — kad patikra galetu pereiti visus, nekartodama saraso.
REGISTRO_RAKTAI = ("random_forest", "gradientinis", "mlp", "autoencoder")


def patikra() -> int:
    """Ar visos keturios klases realizuoja pilna kontrakta.

    Paleidimas:  python -m src.modeliai.bazinis

    KODEL SI PATIKRA EGZISTUOJA
    ---------------------------
    2026-09-09 `Gradientinis._ikelti` dingo is failo (buvo uzrasytas senesne
    kopija). Klaida pasirode tik po to, kai `nematytos.py` jau buvo ikeles
    2,4 mln. eiluciu parquet ir modeli - t. y. po pusantros minutes darbo,
    nors atsakymas buvo zinomas is karto. Trukstamas kontrakto metodas yra
    dalykas, kuri galima patikrinti per sekunde, todel jis ir tikrinamas.
    """
    blogi = []
    for raktas in REGISTRO_RAKTAI:
        try:
            cls = gauti(raktas)
        except Exception as e:                      # noqa: BLE001
            blogi.append(f"{raktas}: importas nepavyko ({type(e).__name__}: {e})")
            continue
        truksta = [m for m in ("_fit", "predict", "predict_proba",
                               "_issaugoti", "_ikelti")
                   if getattr(cls, m, None) is getattr(Modelis, m, None)]
        if truksta:
            blogi.append(f"{cls.__name__}: nerealizuoti {truksta}")
        else:
            print(f"  [OK] {cls.__name__:14s} kontraktas pilnas")
    for eil in blogi:
        print(f"  [BLOGAI] {eil}")
    print(f"\n{len(REGISTRO_RAKTAI) - len(blogi)} / {len(REGISTRO_RAKTAI)} "
          f"klasiu realizuoja pilna kontrakta")
    return 1 if blogi else 0


if __name__ == "__main__":
    import sys
    sys.exit(patikra())
