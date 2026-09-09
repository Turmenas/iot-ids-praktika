# -*- coding: utf-8 -*-
"""Random Forest — ansamblio pakopa sudetingumo gradiente.

Vaidmuo (3 uzduoties 3.7): nustato atskaitos lygi, prie kurio matuojamas
sudetingesniu modeliu prieaugis. Sprendimu matricoje 3,55 balo.

Normalizavimo nereikia: medziai remiasi tvarka, ne mastu.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.modeliai.bazinis import Modelis


class RandomForest(Modelis):
    vardas = "Random Forest"
    priziurimas = True
    reikia_skales = False

    NUMATYTA = {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "n_jobs": -1,
    }

    def _fit(self, X_train, y_train, X_val=None, y_val=None) -> None:
        import time

        from sklearn.ensemble import RandomForestClassifier

        from src.eksperimentai import eiga

        p = {**self.NUMATYTA, **self.konfig}
        # Klasiu svoriai - protokolo 10 punktas. Duomenys nedubliuojami.
        p.setdefault("class_weight", "balanced")
        is_viso = int(p.pop("n_estimators"))

        # Medziai auginami dalimis TIK tam, kad matytusi eiga. Patikrinta:
        # warm_start su tuo paciu random_state duoda tapati miska (skirtumas
        # 2e-16), nes RNG srautas tesiasi - kiekvienas medis vis tiek
        # nepriklausomas.
        self._modelis = RandomForestClassifier(
            n_estimators=0, warm_start=True, random_state=self.seed, **p)

        zingsnis = max(1, is_viso // 20)
        t0, n = time.perf_counter(), 0
        while n < is_viso:
            n = min(n + zingsnis, is_viso)
            self._modelis.n_estimators = n
            self._modelis.fit(X_train, y_train)
            eiga.juosta(n, is_viso, self.vardas, "medziu", t0)

        self.klases_ = self._modelis.classes_

    def predict(self, X) -> np.ndarray:
        return self._modelis.predict(X)

    def predict_proba(self, X) -> np.ndarray:
        return self._modelis.predict_proba(X)

    def _issaugoti(self, kelias: Path) -> None:
        import joblib
        joblib.dump(self._modelis, kelias, compress=3)

    def _ikelti(self, kelias: Path) -> None:
        import joblib
        self._modelis = joblib.load(kelias)
        self.klases_ = self._modelis.classes_
