# -*- coding: utf-8 -*-
"""Daugiasluoksnis perceptronas — ar sudetingumas apsimoka lentelinei ivesciai.

VAIDMUO
-------
2 uzduoties 2.4 poskyris iskele klausima, ar gilaus mokymosi sudetingumas
apsimoka lenteliniams srauto pozymiams. Sprendimu matricoje MLP yra tik
penktas (3,25), bet aibeje jis ne del balo: be jo tas klausimas liktu
neatsakytas eksperimentu, o skyrius klaustu to, ko pats netikrina.

Tai NE seku modelis. LSTM, GRU ir Transformer atmesti K1 vartais: kiekviena
eilute jau yra 10/100 paketu lango agregatas, tad sekos, kuria modeliuoti,
tiesiog nera.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from src.modeliai.bazinis import Modelis


class MLP(Modelis):
    vardas = "MLP"
    priziurimas = True
    reikia_skales = True          # be normalizavimo neuroninis tinklas nesimoko

    NUMATYTA = {
        "sluoksniai": [128, 64],
        "dropout": 0.2,
        "batch_size": 4096,
        "epochos": 20,
        "kantrybe": 3,            # ankstyvas stabdymas pagal val nuostoli
        "learning_rate": 0.001,
    }

    def _fit(self, X_train, y_train, X_val=None, y_val=None) -> None:
        import tensorflow as tf
        from sklearn.preprocessing import LabelEncoder

        from src.duomenys import balansavimas

        tf.keras.utils.set_random_seed(self.seed)
        p = {**self.NUMATYTA, **self.konfig}

        self._kodavimas = LabelEncoder().fit(y_train)
        self.klases_ = self._kodavimas.classes_
        y = self._kodavimas.transform(y_train)

        sl = [tf.keras.layers.Input(shape=(X_train.shape[1],))]
        for n in p["sluoksniai"]:
            sl.append(tf.keras.layers.Dense(n, activation="relu"))
            if p["dropout"]:
                sl.append(tf.keras.layers.Dropout(p["dropout"]))
        sl.append(tf.keras.layers.Dense(len(self.klases_), activation="softmax"))

        self._modelis = tf.keras.Sequential(sl)
        self._modelis.compile(
            optimizer=tf.keras.optimizers.Adam(p["learning_rate"]),
            loss="sparse_categorical_crossentropy", metrics=["accuracy"])

        # Ankstyvas stabdymas pagal MUSU val aibe, ne pagal vidini skaidyma:
        # kitaip modelis butu stabdomas pagal mokymo aibes dali, ir val
        # nustotu buti nepriklausoma.
        kviet, val_duomenys = [], None
        if X_val is not None and y_val is not None:
            val_duomenys = (X_val, self._kodavimas.transform(y_val))
            kviet.append(tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=p["kantrybe"],
                restore_best_weights=True))

        # Disbalansas: klasiu svoriai, ne duomenu dubliavimas (protokolo 10 p.)
        sv = balansavimas.klasiu_svoriai(y_train)
        svoriai = {int(self._kodavimas.transform([k])[0]): float(v)
                   for k, v in sv.items()}

        self._modelis.fit(X_train, y, validation_data=val_duomenys,
                          epochs=p["epochos"], batch_size=p["batch_size"],
                          class_weight=svoriai, callbacks=kviet, verbose=2)

    def predict(self, X) -> np.ndarray:
        return self._kodavimas.inverse_transform(
            self.predict_proba(X).argmax(axis=1))

    def predict_proba(self, X) -> np.ndarray:
        return self._modelis.predict(X, batch_size=4096, verbose=0)

    def _issaugoti(self, kelias: Path) -> None:
        import joblib
        k = kelias.with_suffix(".keras")
        self._modelis.save(k)
        joblib.dump({"kodavimas": self._kodavimas, "keras": k.name}, kelias)

    def _ikelti(self, kelias: Path) -> None:
        import joblib
        import tensorflow as tf
        d = joblib.load(kelias)
        self._kodavimas = d["kodavimas"]
        self.klases_ = self._kodavimas.classes_
        # `compile=False`: ikeliant reikia tik inferencijos, o optimizatoriaus
        # busenos deserializavimas yra dazniausia Keras versiju nesutapimo
        # vieta. Tai NEISSPRENDZIA `quantization_config` klaidos, matytos
        # kitoje masinoje - ta kyla is sluoksniu, ne is kompiliavimo.
        self._modelis = tf.keras.models.load_model(
            Path(kelias).with_suffix(".keras"), compile=False)

    def papildomi_failai(self, kelias: Path) -> list[Path]:
        return [Path(kelias).with_suffix(".keras")]
