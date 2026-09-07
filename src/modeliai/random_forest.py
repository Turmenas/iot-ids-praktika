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
        from sklearn.ensemble import RandomForestClassifier

        p = {**self.NUMATYTA, **self.konfig}
        # Klasiu svoriai - protokolo 10 punktas. Duomenys nedubliuojami.
        p.setdefault("class_weight", "balanced")
        self._modelis = RandomForestClassifier(random_state=self.seed, **p)
        self._modelis.fit(X_train, y_train)
        self.klases_ = self._modelis.classes_

    def predict(self, X) -> np.ndarray:
        return self._modelis.predict(X)

    def predict_proba(self, X) -> np.ndarray:
        return self._modelis.predict_proba(X)

    def _issaugoti(self, kelias: Path) -> None:
        import joblib
        joblib.dump(self._modelis, kelias, compress=3)
