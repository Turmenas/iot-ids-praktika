# -*- coding: utf-8 -*-
"""Autokoderis — nematytu (zero-day) ataku aptikimas.

VAIDMUO
-------
Sprendimu matricoje autokoderis pralaimi ansambliams (2,95 pries 4,70) ir
net Isolation Forest (3,50). Aibeje jis ne del balo: reikalavimas aptikti
NEMATYTAS atakas yra FUNKCINIS, o ne sveriamas - nė vienas priziurimas
metodas jo neivykdo jokiu svoriu deriniu.

Todel jo tikrasis testas yra ne si eilute lenteleje, o nematytu klasiu
scenarijai (5 uzduotis): DDOS-SLOWLORIS, RECON-PORTSCAN ir istisa
kategorija DICTIONARYBRUTEFORCE.

SLENKSTIS — ANTRAS PAGAL TIKIMYBE NUTEKEJIMO KELIAS
---------------------------------------------------
Protokolo 21 punktas: slenkstis kalibruojamas ant VAL gerybinio srauto,
NIEKADA ant test. Kalibravus ant test, modelis "zinotu" testavimo aibes
pasiskirstyma, ir rezultatas butu isspūstas be jokios matomos klaidos -
lygiai kaip su dublikatais.

Cia tai isreiksta kodu: `_fit` slenksti skaiciuoja tik is `X_val`, o jei
val aibes negauna, meta klaida vietoj tylaus atsarginio varianto.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from src.modeliai.bazinis import Modelis

GERYBINE = "Benign"


class Autokoderis(Modelis):
    vardas = "Autokoderis"
    priziurimas = False           # paleisti.py pagal ji zino, kuriu metriku neskaiciuoti
    reikia_skales = True

    NUMATYTA = {
        "sluoksniai": [24, 12],   # koduotojas; dekoderis - veidrodinis
        "batch_size": 4096,
        "epochos": 30,
        "kantrybe": 4,
        "learning_rate": 0.001,
        "procentilis": 99,        # slenkstis is val gerybinio srauto
    }

    # PROCENTILIS YRA KLAIDINGU TEIGIAMU RANKENELE, NE KONVENCIJA
    # ----------------------------------------------------------
    # Slenkstis, nustatytas kaip p-asis val gerybinio srauto procentilis,
    # PAGAL APIBREZIMA duoda (100 - p) % klaidingu teigiamu tam srautui.
    # Iprastas 95-asis procentilis reikstu 5 % - o 1 skyriuje suskaiciuota,
    # kad jau 1 % reiskia ~1000 signalu per para ir sistema issijungia.
    #
    # Todel numatytasis yra 99: jis atitinka ta pati biudzeta, kuriuo
    # remiasi atrankos kriterijai (klaidingiems teigiamiems skirta 30 %
    # svorio). Pasirinkti 95 reikstu is anksto sutikti su rodikliu, kuri
    # pats darbas vadina nepriimtinu.

    def _fit(self, X_train, y_train, X_val=None, y_val=None) -> None:
        import tensorflow as tf

        tf.keras.utils.set_random_seed(self.seed)
        p = {**self.NUMATYTA, **self.konfig}
        self.klases_ = np.array([GERYBINE, "Ataka"])

        X_train = np.asarray(X_train)
        y_train = np.asarray(y_train)

        # ─── Mokoma TIK is gerybinio srauto (protokolo 20 punktas) ───
        gerybines = y_train == GERYBINE
        if not gerybines.any():
            raise ValueError(
                f"Mokymo aibeje nera klases {GERYBINE!r}. Autokoderis mokomas "
                "tik is gerybinio srauto - patikrinkite konfigo `formuluote`.")
        X_ger = X_train[gerybines]
        print(f"  autokoderis mokomas is {len(X_ger):,} gerybinio srauto eiluciu "
              f"(is {len(X_train):,})")

        n = X_train.shape[1]
        sl = [tf.keras.layers.Input(shape=(n,))]
        for k in p["sluoksniai"]:
            sl.append(tf.keras.layers.Dense(k, activation="relu"))
        for k in reversed(p["sluoksniai"][:-1]):
            sl.append(tf.keras.layers.Dense(k, activation="relu"))
        sl.append(tf.keras.layers.Dense(n, activation="linear"))

        self._modelis = tf.keras.Sequential(sl)
        self._modelis.compile(
            optimizer=tf.keras.optimizers.Adam(p["learning_rate"]), loss="mse")

        # Ankstyvam stabdymui - TIK val gerybinis srautas. Atakos i mokyma
        # ar stabdyma nepatenka niekada.
        val_duomenys, kviet = None, []
        if X_val is not None and y_val is not None:
            X_val, y_val = np.asarray(X_val), np.asarray(y_val)
            vg = X_val[y_val == GERYBINE]
            if len(vg):
                val_duomenys = (vg, vg)
                kviet.append(tf.keras.callbacks.EarlyStopping(
                    monitor="val_loss", patience=p["kantrybe"],
                    restore_best_weights=True))

        self._modelis.fit(X_ger, X_ger, validation_data=val_duomenys,
                          epochs=p["epochos"], batch_size=p["batch_size"],
                          callbacks=kviet, verbose=2)

        # ─── Slenkstis: TIK is val gerybinio srauto ───
        if X_val is None or y_val is None:
            raise ValueError(
                "Slenksciui kalibruoti butina val aibe. Kalibravimas ant test "
                "yra nutekejimas (protokolo 21 punktas), o ant train - "
                "per optimistinis.")
        vg = np.asarray(X_val)[np.asarray(y_val) == GERYBINE]
        if not len(vg):
            raise ValueError(f"Val aibeje nera {GERYBINE!r} eiluciu.")
        self.slenkstis_ = float(np.percentile(self._paklaida(vg), p["procentilis"]))
        self.procentilis_ = p["procentilis"]
        print(f"  slenkstis {self.slenkstis_:.6f} "
              f"({p['procentilis']}-asis procentilis is {len(vg):,} val gerybiniu)")

    def _paklaida(self, X) -> np.ndarray:
        """Atkurimo paklaida (MSE) kiekvienai eilutei."""
        X = np.asarray(X)
        atkurta = self._modelis.predict(X, batch_size=4096, verbose=0)
        return np.mean((X - atkurta) ** 2, axis=1)

    def predict(self, X) -> np.ndarray:
        return np.where(self._paklaida(X) > self.slenkstis_, "Ataka", GERYBINE)

    def predict_proba(self, X) -> np.ndarray:
        """Atkurimo paklaida: didesne reiksme = didesne atakos tikimybe."""
        return self._paklaida(X)

    def _issaugoti(self, kelias: Path) -> None:
        import joblib
        k = kelias.with_suffix(".keras")
        self._modelis.save(k)
        joblib.dump({"slenkstis": self.slenkstis_,
                     "procentilis": self.procentilis_, "keras": k.name}, kelias)

    def papildomi_failai(self, kelias: Path) -> list[Path]:
        return [Path(kelias).with_suffix(".keras")]
