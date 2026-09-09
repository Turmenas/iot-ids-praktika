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


def _eigos_iskvietimas(is_viso: int, vardas: str):
    """XGBoost eigos juosta.

    Klase kuriama funkcijoje, bet PATI funkcija yra modulio lygyje: vietine
    klase (`_fit` viduje) nepasiduoda `pickle`, ir modelio issaugojimas
    luzta. Kartu `issaugoti` atsieja iskvietimus - kitaip i faila keliautu
    ir laikmaciai.
    """
    import time

    import xgboost as xgb

    from src.eksperimentai import eiga

    class _Eiga(xgb.callback.TrainingCallback):
        def __init__(self):
            self.is_viso = int(is_viso)
            self.zingsnis = max(1, self.is_viso // 20)
            self.t0 = time.perf_counter()

        def after_iteration(self, model, epoch, evals_log):
            n = epoch + 1
            if n % self.zingsnis == 0 or n == self.is_viso:
                eiga.juosta(n, self.is_viso, vardas, "medziu", self.t0)
            return False              # False = testi mokyma

    return _Eiga()


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
        "device": "cuda",          # GPU; be jos automatiskai grizta i "cpu"
        "n_jobs": -1,
    }

    @staticmethod
    def _irenginys(noretas: str) -> str:
        """Grazina "cuda" tik jei GPU tikrai pasiekiamas, kitaip "cpu".

        Tyliai grizti i CPU geriau nei luzti: tas pats konfigas turi veikti
        ir masinoje su GPU, ir be jos. Bet grizimas ISPAUSDINAMAS - kitaip
        nesuprastum, kodel mokymas staiga trunka desimt kartu ilgiau.
        """
        if noretas != "cuda":
            return noretas
        try:
            import xgboost as xgb
            if xgb.build_info().get("USE_CUDA"):
                return "cuda"
            print("  [!] XGBoost sukompiliuotas be CUDA - naudojamas CPU")
        except Exception as e:
            print(f"  [!] GPU patikra nepavyko ({e}) - naudojamas CPU")
        return "cpu"

        # Pastaba: `USE_CUDA` sako tik tiek, kad biblioteka SUKOMPILIUOTA su
        # CUDA - ne kad GPU yra. Jei jo nera, XGBoost pats grizta i CPU ir
        # apie tai perspeja ("No visible GPU is found"). Tos zinutes uztenka,
        # todel cia GPU buvimas netikrinamas paleidziant bandomaji mokyma.

    def _fit(self, X_train, y_train, X_val=None, y_val=None) -> None:
        from sklearn.preprocessing import LabelEncoder
        from xgboost import XGBClassifier

        from src.duomenys import balansavimas

        self._kodavimas = LabelEncoder().fit(y_train)
        self.klases_ = self._kodavimas.classes_
        y = self._kodavimas.transform(y_train)

        p = {**self.NUMATYTA, **self.konfig}
        p["device"] = self._irenginys(p.get("device", "cpu"))

        self._modelis = XGBClassifier(
            random_state=self.seed, eval_metric="mlogloss",
            callbacks=[_eigos_iskvietimas(p["n_estimators"], self.vardas)], **p)
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
        # Eigos iskvietimas turi laikmati ir isvesties busena - i issaugota
        # modeli jam ne vieta, o `pickle` jo vis tiek nepriimtu.
        self._modelis.callbacks = None
        joblib.dump({"modelis": self._modelis, "kodavimas": self._kodavimas},
                    kelias, compress=3)

    def _ikelti(self, kelias: Path) -> None:
        import joblib
        d = joblib.load(kelias)
        self._modelis = d["modelis"]
        self._kodavimas = d["kodavimas"]
        self.klases_ = self._kodavimas.classes_
        # Sliuze GPU nera, o modelis galejo buti apmokytas su `device=cuda`.
        # Delsa, matuota GPU, yra 6,5 karto mazesne uz CPU (2026-09-08),
        # todel ikeliant grazinama i ta aparatura, kuri bus diegimo vietoje.
        try:
            self._modelis.set_params(device="cpu")
        except Exception:
            pass
