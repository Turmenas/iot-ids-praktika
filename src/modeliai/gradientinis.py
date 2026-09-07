# -*- coding: utf-8 -*-
"""XGBoost — sprendimu matricos virsune (4,70) ir vienintelis modelis,
kurio rezultata galima tiesiogiai gretinti su literatura.

FAILO VARDAS
------------
Modulis vadinasi `gradientinis`, o ne `xgboost`: failas `xgboost.py`
sitame pakete uzdengtu pacia biblioteka `import xgboost`, ir klaida
pasirodytu kaip nesuprantamas ImportError.

DISBALANSAS
-----------
Protokolo 10 punktas numate `scale_pos_weight`, taciau tas parametras
veikia TIK dvejetaineje uzduotyje - daugiaklasei jis ignoruojamas be
jokio ispejimo. Pagrindine formuluote yra 8 kategorijos, todel cia
naudojamas `sample_weight` (balansavimas.eiluciu_svoriai).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.modeliai.bazinis import Modelis


class Gradientinis(Modelis):
    vardas = "XGBoost"
    priziurimas = True
    reikia_skales = False

    NUMATYTA = {
        "n_estimators": 300,
        "max_depth": 8,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "tree_method": "hist",     # butinas milijonu eiluciu imtims
        "n_jobs": -1,
    }

    def _fit(self, X_train, y_train, X_val=None, y_val=None) -> None:
        from sklearn.preprocessing import LabelEncoder
        from xgboost import XGBClassifier

        from src.duomenys import balansavimas

        self._kodavimas = LabelEncoder().fit(y_train)
        self.klases_ = self._kodavimas.classes_
        y = self._kodavimas.transform(y_train)

        p = {**self.NUMATYTA, **self.konfig}
        self._modelis = XGBClassifier(random_state=self.seed,
                                      eval_metric="mlogloss", **p)
        # Disbalansas: eiluciu svoriai, ne scale_pos_weight (zr. dokumentacija)
        self._modelis.fit(X_train, y,
                          sample_weight=balansavimas.eiluciu_svoriai(y_train),
                          verbose=False)

    def predict(self, X) -> np.ndarray:
        return self._kodavimas.inverse_transform(self._modelis.predict(X))

    def predict_proba(self, X) -> np.ndarray:
        return self._modelis.predict_proba(X)

    def _issaugoti(self, kelias: Path) -> None:
        import joblib
        joblib.dump({"modelis": self._modelis, "kodavimas": self._kodavimas},
                    kelias, compress=3)
