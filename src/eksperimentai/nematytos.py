# -*- coding: utf-8 -*-
"""
Nematytu ataku klasiu testas — protokolo 22-23 punktai.

Paleidimas:
    python -m src.eksperimentai.nematytos
    python -m src.eksperimentai.nematytos --klases DDOS-SLOWLORIS --seed 42

Isvestis:
    rezultatai/darbiniai/nematytos_test.csv       pagrindine lentele
    rezultatai/darbiniai/perklasiu_tau_test.csv   per-kategorija ties tau
    ataskaita/lenteles/nematytos.tex


KODEL DVEJETAINIS KLAUSIMAS, O NE macro-F1
------------------------------------------
`DICTIONARYBRUTEFORCE` yra VIENINTELE savo kategorijos klase, todel ja
pasalinus is mokymo `BruteForce` kategorija istustėja ir permokytas
modelis turi 7 klases vietoj 8. macro-F1, vidurkinamas per skirtinga
klasiu skaiciu, su baziniu modeliu nepalyginamas.

Todel klausiama vieno dalyko: ar pasalintos klases eilutes TEST aibeje
pazymimos kaip ataka (bet kuri), ar praleidziamos.


KODEL AUTOKODERIS NEPERMOKOMAS
------------------------------
Jis mokomas TIK is `BENIGN` (protokolo 20 punktas), todel visos 33 ataku
klases jam ir taip nematytos. Permokymas be `DDOS-SLOWLORIS` duotu ta
pati modeli. Jo skaicius imamas is bazinio test paleidimo — tai ne
apejimas, o teisingas palyginimas.


KODEL SVORIAI IMAMI IS PILNOS AIBES
-----------------------------------
`class_weight="balanced"` perskaiciuotu likusiu klasiu svorius, ir
permokytas modelis skirtusi nuo bazinio DVIEM dalykais: trukstama klase
IR kitokiais svoriais. Tada testas matuotu du pokycius vienu metu.
Todel svoriai skaiciuojami is PILNOS mokymo aibes ir tik po to
uzdedami ant sumazintos.


TAU VISADA IS VAL
-----------------
Kiekvienas permokytas modelis yra KITAS modelis, todel jam tau
parenkamas is naujo — bet ant `val`, ne ant `test`. FPR skaiciuojamas
tik is gerybinio srauto, tad pasalinta atakos klase i ta parinkima
neiteina.
"""

from __future__ import annotations

import argparse
import gc
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
APMOKYTI = SAKNIS / "rezultatai" / "apmokyti"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"
LENTELES = SAKNIS / "ataskaita" / "lenteles"

GERYBINE = "Benign"

#: Protokolo 22 punktas — klases parinktos 2026-09-03, ne matant rezultatus.
KLASES = ("DDOS-SLOWLORIS", "RECON-PORTSCAN", "DICTIONARYBRUTEFORCE")

#: Kodel butent sios trys.
PAGRINDIMAS = {
    "DDOS-SLOWLORIS": "zemo intensyvumo ataka; pagrindinio pozymio "
                      "(srauto trukmes) sis leidimas neisreiskia",
    "RECON-PORTSCAN": "zvalgyba; kategorija, kuria modelis painioja su "
                      "gerybiniu srautu",
    "DICTIONARYBRUTEFORCE": "vienintele savo kategorijos klase, todel "
                            "priziurimas modelis etiketes neturi is principo",
}

BAZINIS_KONFIGAS = "gradientinis_derintas"
AUTOKODERIS = "autoencoder_dvejetaine"


def _duomenys():
    """(X, y_etikete, y_kategorija, idx). Parquet skaitomas viena karta."""
    from src.duomenys import pozymiai, skaidymas
    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, y_et, y_kat = pozymiai.atrinkti(df, tikrinti=False)
    del df
    gc.collect()
    return X, y_et.to_numpy(), y_kat.to_numpy(), idx


def _tau_ant_val(P, klases, y_val, biudzetas: float) -> float:
    """Maziausias tau, tenkinantis FPR <= biudzetas. Renkama TIK ant val."""
    from src.eksperimentai.slenkstis import kreive, parinkti
    return float(parinkti(kreive(P, klases, y_val), biudzetas).tau)


def _aptikimas(P, klases, tau: float) -> np.ndarray:
    """True ten, kur skelbiama bet kuri ataka."""
    from src.eksperimentai.slenkstis import _sprendimas
    return _sprendimas(P, klases, tau) != GERYBINE


def permokyti_be_klases(X, y_kat, idx, etiketes_masyvas, klase: str,
                        konfig: dict, seed: int):
    """Permoko XGBoost be nurodytos etiketes. Grazina (modelis, klases)."""
    from src.modeliai import bazinis
    from src.duomenys import balansavimas

    i_tr = idx["train"]
    lieka = etiketes_masyvas[i_tr] != klase
    i_tr_maz = i_tr[lieka]

    # ⚠️ Svoriai — is PILNOS mokymo aibes (zr. modulio dokumentacija).
    sv = balansavimas.klasiu_svoriai(y_kat[i_tr])
    w = np.asarray(pd.Series(y_kat[i_tr_maz]).map(sv), dtype="float64")

    print(f"    train {len(i_tr):,} -> {len(i_tr_maz):,} "
          f"(pasalinta {len(i_tr) - len(i_tr_maz):,})")
    kat_liko = sorted(set(y_kat[i_tr_maz]))
    if len(kat_liko) < len(set(y_kat[i_tr])):
        dingo = sorted(set(y_kat[i_tr]) - set(kat_liko))
        print(f"    [!] ISTUSTEJO kategorija: {dingo} -> "
              f"{len(kat_liko)} klases vietoj {len(set(y_kat[i_tr]))}")

    Klase = bazinis.gauti("gradientinis")
    m = Klase(konfig.get("hiperparametrai", {}), seed=seed)
    m.fit(X.iloc[i_tr_maz], y_kat[i_tr_maz], svoriai=w)
    print(f"    mokymo laikas {m.mokymo_laikas_s:.1f} s")
    return m


def main() -> None:
    import yaml

    a = argparse.ArgumentParser()
    a.add_argument("--klases", nargs="+", default=list(KLASES))
    a.add_argument("--seed", type=int, default=42)
    a.add_argument("--biudzetas", type=float, default=0.01)
    n = a.parse_args()

    from src.modeliai import bazinis

    konfig = yaml.safe_load(
        (SAKNIS / "konfig" / f"{BAZINIS_KONFIGAS}.yaml").read_text(encoding="utf-8"))

    X, y_et, y_kat, idx = _duomenys()
    i_val, i_test = idx["val"], idx["test"]
    y_val, y_test = y_kat[i_val], y_kat[i_test]
    et_test = y_et[i_test]
    print(f"val {len(i_val):,} · test {len(i_test):,}")

    # ─── 1. Bazinis modelis: atskaitos stulpelis ir per-kategorija ties tau ───
    kelias = APMOKYTI / f"{BAZINIS_KONFIGAS}_8kat_seed{n.seed}.joblib"
    print(f"\nBazinis modelis: {kelias.name}")
    bazinis_m = bazinis.gauti("gradientinis").ikelti(kelias)
    P_val = bazinis_m.predict_proba(X.iloc[i_val])
    tau_baz = _tau_ant_val(P_val, bazinis_m.klases_, y_val, n.biudzetas)
    del P_val
    gc.collect()
    P_test = bazinis_m.predict_proba(X.iloc[i_test])
    apt_baz = _aptikimas(P_test, bazinis_m.klases_, tau_baz)
    fpr_baz = float(apt_baz[y_test == GERYBINE].mean())
    print(f"  tau {tau_baz:.4f} (is val) · test FPR {fpr_baz*100:.2f} %")

    # Per-kategorija ties tau — pjuvis, kurio T4 neturejo (jis ties argmax)
    pk = []
    for kat in sorted(set(y_test)):
        k = y_test == kat
        pk.append({"modelis": "XGBoost", "taskas": "slenkstis",
                   "kategorija": kat, "n": int(k.sum()),
                   "pazymeta_ataka": float(apt_baz[k].mean())})
    del P_test
    gc.collect()

    # ─── 2. Autokoderis: NEPERMOKOMAS ───
    ak_kelias = APMOKYTI / f"{AUTOKODERIS}_seed{n.seed}.joblib"
    apt_ak = None
    if ak_kelias.exists():
        from src.duomenys import pozymiai
        print(f"\nAutokoderis: {ak_kelias.name} (NEPERMOKOMAS)")
        ak = bazinis.gauti("autoencoder").ikelti(ak_kelias)
        sk_kelias = ak_kelias.with_suffix(".skale.joblib")
        skale = (pozymiai.Skale.ikelti(sk_kelias) if sk_kelias.exists()
                 else pozymiai.Skale().fit(X.iloc[idx["train"]]))
        apt_ak = ak.predict(skale.transform(X.iloc[i_test])) != GERYBINE
        print(f"  test FPR {float(apt_ak[y_test == GERYBINE].mean())*100:.2f} %")
        for kat in sorted(set(y_test)):
            k = y_test == kat
            pk.append({"modelis": "Autokoderis", "taskas": "slenkstis",
                       "kategorija": kat, "n": int(k.sum()),
                       "pazymeta_ataka": float(apt_ak[k].mean())})
        del ak
        gc.collect()

    DARBINIAI.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(pk).to_csv(DARBINIAI / "perklasiu_tau_test.csv", index=False)

    # ─── 3. Permokymai be klases ───
    eil = []
    for klase in n.klases:
        yra = et_test == klase
        if not yra.any():
            print(f"\n[!] {klase} test aibeje nerasta - praleidziama")
            continue
        print(f"\n=== {klase}  (test n = {int(yra.sum()):,})")
        m = permokyti_be_klases(X, y_kat, idx, y_et, klase, konfig, n.seed)

        Pv = m.predict_proba(X.iloc[i_val])
        tau = _tau_ant_val(Pv, m.klases_, y_val, n.biudzetas)
        del Pv
        gc.collect()

        Pt = m.predict_proba(X.iloc[i_test])
        apt = _aptikimas(Pt, m.klases_, tau)
        del Pt, m
        gc.collect()

        e = {
            "klase": klase,
            "n_test": int(yra.sum()),
            "tau": round(tau, 6),
            "fpr_test": float(apt[y_test == GERYBINE].mean()),
            "nematyta_priziurimas": float(apt[yra].mean()),
            "autokoderis": (None if apt_ak is None else float(apt_ak[yra].mean())),
            "matyta_priziurimas": float(apt_baz[yra].mean()),
            "pagrindimas": PAGRINDIMAS.get(klase, ""),
        }
        eil.append(e)
        print(f"    tau {tau:.4f} · FPR {e['fpr_test']*100:.2f} %")
        ak_tekstas = ("---" if e["autokoderis"] is None
                      else f"{e['autokoderis']*100:.1f} %")
        print(f"    aptikta: nematyta {e['nematyta_priziurimas']*100:.1f} %"
              f" | autokoderis {ak_tekstas}"
              f" | kai matyta {e['matyta_priziurimas']*100:.1f} %")

    t = pd.DataFrame(eil)
    t.to_csv(DARBINIAI / "nematytos_test.csv", index=False)
    LENTELES.mkdir(parents=True, exist_ok=True)
    (LENTELES / "nematytos.tex").write_text(_lentele(t), encoding="utf-8")

    print(f"\n[OK] {len(t)} klases -> "
          f"{(DARBINIAI / 'nematytos_test.csv').relative_to(SAKNIS)}")
    print(f"     {(DARBINIAI / 'perklasiu_tau_test.csv').relative_to(SAKNIS)}")
    print(f"     {(LENTELES / 'nematytos.tex').relative_to(SAKNIS)}")


def _sk(x, n=1):
    return "---" if x is None or pd.isna(x) else f"{x:.{n}f}".replace(".", ",")


def _lentele(t: pd.DataFrame) -> str:
    sk = [r"% GENERUOJAMA is rezultatai/darbiniai/nematytos_test.csv",
          r"% Ranka NELIESTI - paleisti: python -m src.eksperimentai.nematytos",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          r">{\raggedleft\arraybackslash}p{1.3cm}"
          + r">{\centering\arraybackslash}p{2.1cm}" * 3 + r"@{}}",
          r"\toprule",
          r"\multirow{2}{*}{\textbf{Pašalinta klasė}} & \multirow{2}{*}{\textbf{$n$}} "
          r"& \multicolumn{3}{c}{\textbf{Aptikta (pažymėta kaip ataka)}} \\",
          r"\cmidrule(l){3-5}",
          r" & & \textbf{Prižiūrimas, klasės nematęs} & \textbf{Autokoderis} "
          r"& \textbf{Prižiūrimas, klasę matęs} \\",
          r"\midrule"]
    for _, e in t.iterrows():
        sk.append(r"\texttt{%s} & %s & %s~\%% & %s~\%% & %s~\%% \\" % (
            e.klase.replace("_", r"\_"),
            f"{int(e.n_test):,}".replace(",", "\\,"),
            _sk(e.nematyta_priziurimas * 100),
            _sk(None if pd.isna(e.autokoderis) else e.autokoderis * 100),
            _sk(e.matyta_priziurimas * 100)))
    sk += [r"\bottomrule", r"\end{tabularx}",
           r"\vspace{2pt}",
           r"\raggedright\scriptsize Testavimo aibė. Klausiama tik to, ar eilutė "
           r"pažymima kaip \emph{bet kuri} ataka: pašalinus "
           r"\texttt{DICTIONARYBRUTEFORCE} ištuštėja visa \texttt{BruteForce} "
           r"kategorija, todėl macro-F1 su baziniu modeliu būtų nepalyginamas. "
           r"Autokoderis \emph{nepermokomas} --- jis mokomas tik iš gerybinio "
           r"srauto, tad visos atakų klasės jam ir taip nematytos. Paskutinis "
           r"stulpelis rodo, kiek kainuoja klasės nematyti. Kiekvienam modeliui "
           r"$\tau$ parinktas validacijos aibėje.",
           r"\endgroup"]
    return "\n".join(sk) + "\n"


if __name__ == "__main__":
    main()
