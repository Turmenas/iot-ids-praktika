# -*- coding: utf-8 -*-
"""
Rezultatu patikimumo patikros — 5 uzduoties T7.

Paleidimas:
    python -m src.eksperimentai.patikimumas
    python -m src.eksperimentai.patikimumas --su-duomenimis   (prideda 2 patikra)

Isvestis:
    rezultatai/darbiniai/patikimumas_test.md
    ataskaita/lenteles/patikimumas.tex


KODEL SIS MODULIS, O NE SARASAS ATASKAITOJE
-------------------------------------------
Priemimo kriterijus, pazymetas atliktu nepaleidus komandos, yra spejimas
apie savo paties darba (2026-09-06 pamoka). Penkios patikros yra
tiksliai tokio tipo teiginiai, todel jos skaiciuojamos, o ne surasomos.


TRYS BUSENOS, NE DVI
--------------------
    PRAEJO    tikrinamas dalykas galioja
    RADINYS   negalioja, bet tai REZULTATAS, ne klaida - rasoma i ataskaita
    NEPRAEJO  kazkas negerai su pacia grandine

4-oji patikra (ar val operacinis taskas persikelia i test) is anksto
numatyta kaip galinti duoti RADINI: plane uzrasyta, kad jos rezultatas
rasomas, koks bebutu.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SAKNIS = Path(__file__).resolve().parents[2]
REZULTATAI = SAKNIS / "rezultatai" / "rezultatai.csv"
DARBINIAI = SAKNIS / "rezultatai" / "darbiniai"
LENTELES = SAKNIS / "ataskaita" / "lenteles"

#: Teorine tikslumo riba, ismatuota darbineje imtyje (imties_ataskaita.md).
#: 0,43 % eiluciu turi priestaringas etiketes, todel geriausias imanomas
#: klasifikatorius klysta bent tiek.
TEORINE_RIBA = 0.9978

BIUDZETAS = 0.01
GERYBINE = "Benign"

PRAEJO, RADINYS, NEPRAEJO = "PRAEJO", "RADINYS", "NEPRAEJO"


def _b(busena: str) -> str:
    return {PRAEJO: "[OK ]", RADINYS: "[RAD]", NEPRAEJO: "[!!!]"}[busena]


# ─── 1. Ar test aibe kam nors turejo itakos ──────────────────────────

def patikra_1(rez: pd.DataFrame) -> dict:
    """tau nepersirinktas ant test; kiekviena test eilute turi val pora.

    Du nepriklausomi rodmenys. Pirmasis tikrina slenksti tiesiogiai:
    jei `slenkscio_taskai_test.csv` tau sutampa su val reiksmemis iki
    paskutinio skaitmens, jis buvo NUSKAITYTAS, o ne parinktas is naujo.
    Antrasis tikrina eiliskuma: test eilute be val poros reikstu, kad
    modelis buvo vertintas test aibeje anksciau nei val.
    """
    pastabos, busena = [], PRAEJO

    v_k, t_k = DARBINIAI / "slenkscio_taskai.csv", DARBINIAI / "slenkscio_taskai_test.csv"
    if v_k.exists() and t_k.exists():
        v = pd.read_csv(v_k); t = pd.read_csv(t_k)
        v = v[v.taskas == "slenkstis"].set_index("modelis")["tau"]
        t = t[t.taskas == "slenkstis"].set_index("modelis")["tau"]
        bendri = sorted(set(v.index) & set(t.index))
        nesutampa = [m for m in bendri if abs(float(v[m]) - float(t[m])) > 1e-12]
        pastabos.append(f"tau sutampa {len(bendri) - len(nesutampa)}/{len(bendri)} modeliu")
        if nesutampa:
            busena = NEPRAEJO
            pastabos.append(f"PERRINKTAS ant test: {nesutampa}")
    else:
        busena = NEPRAEJO
        pastabos.append("slenkscio tasku failu nera")

    raktas = ["modelis", "formuluote", "seed", "konfig"]
    val = set(map(tuple, rez[rez.aibe == "val"][raktas].astype(str).to_numpy()))
    tst = set(map(tuple, rez[rez.aibe == "test"][raktas].astype(str).to_numpy()))
    be_poros = sorted(tst - val)
    pastabos.append(f"test eiluciu su val pora: {len(tst) - len(be_poros)}/{len(tst)}")
    if be_poros:
        busena = NEPRAEJO
        pastabos.append(f"be val poros: {be_poros[:3]}")

    return {"nr": 1, "pavadinimas": "test neitakojo jokio sprendimo",
            "busena": busena, "pastabos": pastabos}


# ─── 2. Ar train ir test nesikerta ───────────────────────────────────

def patikra_2() -> dict:
    """Du atskiri matavimai: dublikatu garantija ir modelio ivesties erdve.

    2a  39 stulpeliai (kaip salinti dublikatai) - PROTOKOLO GARANTIJA
    2b  36 pozymiai + etikete (kaip mato modelis) - stipresne savybe

    ⚠️ 2026-09-09 ISMATUOTA: 2a = 0, 2b = 30 eiluciu (0,0082 % test aibes).

    Priezastis tiksli. Dublikatai salinti VISOS 39 stulpeliu eilutes
    pagrindu, o modeliai mokosi is 36 pozymiu: `Variance`, `Tot size` ir
    `Tot sum` pasalinti kaip pertekliniai. Eilutes, kurios 39 stulpeliu
    pavidalu skiriasi paskutiniu slankiojo kablelio bitu, po pozymiu
    salinimo tampa tapacios:

        Variance  train 1,9797979797979728
                  test  1,9797979797979723

    Salinimas savo darba atliko teisingai; spraga turejo VEIKSMU TVARKA -
    dedublikavimas prieš pozymiu atranka, o ne po jos.

    Tai patikslina ir 2026-09-07 radini: `Variance` = `Std`^2 tikrinta su
    `rtol=1e-9`, ir vieno bito skirtumai ta patikra praeina teisingai -
    rysys tikrai tikslus. Bet dublikatu salinimas lygino TIKSLIAI.

    Poveikis rezultatams: <= 0,0082 p. p., t. y. po ketvirto skaitmens.
    Todel imtis neperdaroma; apribojimas ivardijamas ir ismatuojamas.
    """
    from src.duomenys import pozymiai, skaidymas
    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, y_et, _ = pozymiai.atrinkti(df, tikrinti=False)

    def maisos(d, i):
        return set(pd.util.hash_pandas_object(d.iloc[i], index=False).to_numpy())

    tr, te = idx["train"], idx["test"]
    p39 = maisos(df, tr) & maisos(df, te)
    su_et = X.assign(_et=y_et.to_numpy())
    p36 = maisos(su_et, tr) & maisos(su_et, te)
    del df

    dalis = len(p36) / len(te) * 100
    if p39:
        busena = NEPRAEJO          # pati garantija pazeista
    elif p36:
        busena = RADINYS           # tvarkos spraga, ismatuota
    else:
        busena = PRAEJO

    return {"nr": 2, "pavadinimas": "train ir test nesikerta",
            "busena": busena,
            "pastabos": [
                f"2a  39 stulpeliu (dedublikavimo erdve): {len(p39):,} "
                f"- protokolo garantija",
                f"2b  36 pozymiu + etikete (modelio ivestis): {len(p36):,} "
                f"= {dalis:.4f} % test aibes",
                "priezastis: dedublikuota PRIES pozymiu salinima; vieno bito "
                "skirtumai pasalintuose stulpeliuose po to isnyksta"]}


# ─── 3. Ar rezultatas neperzengia teorines ribos ─────────────────────

def patikra_3(rez: pd.DataFrame) -> dict:
    """Joks tikslumas neperzengia 99,78 %.

    Aukstesnis rezultatas butu ne pasiekimas, o nutekejimo pozymis:
    riba ismatuota siuose paciuose duomenyse.
    """
    t = rez[rez.aibe == "test"]
    virs = t[t.accuracy > TEORINE_RIBA]
    didz = t.loc[t.accuracy.idxmax()]
    return {"nr": 3, "pavadinimas": f"tikslumas neperzengia {TEORINE_RIBA*100:.2f} %",
            "busena": PRAEJO if virs.empty else NEPRAEJO,
            "pastabos": [f"didziausias: {didz.accuracy:.4f} "
                         f"({didz.modelis}, {didz.formuluote})",
                         f"atsarga iki ribos: {(TEORINE_RIBA - didz.accuracy)*100:.2f} p. p."]}


# ─── 4. Ar operacinis taskas persikelia is val i test ────────────────

def patikra_4() -> dict:
    """val tau taikomas test: ar FPR islieka biudzete.

    Vienintele patikra, kurios rezultato nezinojau is anksto. `parinkti`
    renka MAZIAUSIA tau, tenkinanti biudzeta, todel pagal konstrukcija
    atsiduria prie pat krasto - atsargos nera.
    """
    v_k, t_k = DARBINIAI / "slenkscio_taskai.csv", DARBINIAI / "slenkscio_taskai_test.csv"
    if not (v_k.exists() and t_k.exists()):
        return {"nr": 4, "pavadinimas": "operacinis taskas persikelia",
                "busena": NEPRAEJO, "pastabos": ["slenkscio tasku failu nera"],
                "eilutes": []}

    v = pd.read_csv(v_k); t = pd.read_csv(t_k)
    v = v[v.taskas == "slenkstis"].set_index("modelis")
    t = t[t.taskas == "slenkstis"].set_index("modelis")

    eil, virsija = [], []
    # I ataskaita eina tik suderintos konfiguracijos: 6.1 poskyris sako,
    # kad vertinami keturi modeliai suderintomis konfiguracijomis, o
    # bazines cia patekdavo tik todel, kad guli tame paciame CSV.
    for m in sorted(set(v.index) & set(t.index)):
        if "bazinis" in m:
            continue
        fv, ft = float(v.loc[m, "fpr"]), float(t.loc[m, "fpr"])
        eil.append({"modelis": m, "tau": float(v.loc[m, "tau"]),
                    "fpr_val": fv, "fpr_test": ft,
                    "santykis": ft / fv if fv else np.nan,
                    "telpa": ft <= BIUDZETAS})
        if ft > BIUDZETAS:
            virsija.append(f"{m} ({ft*100:.2f} %)")

    e = pd.DataFrame(eil)
    return {"nr": 4, "pavadinimas": "operacinis taskas persikelia i test",
            "busena": PRAEJO if not virsija else RADINYS,
            "pastabos": [f"FPR santykis test/val: {e.santykis.min():.2f}-"
                         f"{e.santykis.max():.2f}x",
                         (f"biudzeta virsija: {', '.join(virsija)}" if virsija
                          else f"visi telpa i {BIUDZETAS*100:g} %")],
            "eilutes": eil}


# ─── 5. Ar lenteles skaiciai atitinka modeliu isvesti ────────────────

def patikra_5(rez: pd.DataFrame) -> dict:
    """Metrikos perskaiciuojamos IS SUMAISYMO MATRICU ir lyginamos su CSV.

    Tai stipresne atkartojamumo patikra nei antras paleidimas: ji eina
    NEPRIKLAUSOMU keliu. `rezultatai.csv` skaiciai gauti is
    `sklearn.metrics`, o cia - is issaugotos matricos. Sutapimas reiskia,
    kad lenteleje esantys skaiciai tikrai yra tie, kuriuos modelis davė.
    """
    from src.eksperimentai.klaidos import VARDAI, ikelti_matricas, perklase

    matricos = ikelti_matricas("test")
    t = rez[(rez.aibe == "test")].copy()

    eil = []
    for (konfigas, seed), M in matricos.items():
        vardas = VARDAI.get(konfigas)
        r = t[(t.modelis == vardas) & (t.seed == seed)
              & (t.konfig.str.contains(f"/{konfigas}.yaml", regex=False))]
        if r.empty:
            continue
        r = r.iloc[0]
        p = perklase(M)
        A = M.to_numpy(dtype=float)
        eil.append({
            "zyma": f"{konfigas}_seed{seed}",
            "macro_f1_csv": float(r.macro_f1),
            "macro_f1_matrica": float(p.f1.mean()),
            "acc_csv": float(r.accuracy),
            "acc_matrica": float(np.diag(A).sum() / A.sum()),
        })

    e = pd.DataFrame(eil)
    if e.empty:
        return {"nr": 5, "pavadinimas": "metrikos atkuriamos",
                "busena": NEPRAEJO, "pastabos": ["nerasta sugretinamu eiluciu"]}
    e["d_f1"] = (e.macro_f1_csv - e.macro_f1_matrica).abs()
    e["d_acc"] = (e.acc_csv - e.acc_matrica).abs()
    riba = 1e-4          # CSV apvalinamas iki 5 skaitmenu
    bloga = e[(e.d_f1 > riba) | (e.d_acc > riba)]
    return {"nr": 5, "pavadinimas": "metrikos atkuriamos nepriklausomu keliu",
            "busena": PRAEJO if bloga.empty else NEPRAEJO,
            "pastabos": [f"sugretinta {len(e)} paleidimu",
                         f"didziausias skirtumas: macro-F1 {e.d_f1.max():.2e}, "
                         f"tikslumas {e.d_acc.max():.2e}"]}


# ─── Isvestis ────────────────────────────────────────────────────────

def _sk(x, n=2):
    return "---" if pd.isna(x) else f"{x:.{n}f}".replace(".", ",")


def _lentele(p4: dict) -> str:
    """4-oji patikra yra vienintele su skaiciais - ji ir eina i ataskaita."""
    sk = [r"% GENERUOJAMA - paleisti: python -m src.eksperimentai.patikimumas",
          r"\begingroup", r"\footnotesize", r"\setlength{\tabcolsep}{5pt}",
          r"\begin{tabularx}{\textwidth}{@{}"
          r">{\raggedright\arraybackslash}X"
          + r">{\centering\arraybackslash}p{2.0cm}" * 4 + r"@{}}",
          r"\toprule",
          r"\textbf{Modelis} & \textbf{$\tau$ (iš val)} & \textbf{FPR val} "
          r"& \textbf{FPR test} & \textbf{Santykis} \\",
          r"\midrule"]
    for e in p4.get("eilutes", []):
        zyma = "" if e["telpa"] else r"\,$^{*}$"
        sk.append(r"%s & %s & %s~\%% & %s~\%%%s & %s$\times$ \\" % (
            e["modelis"], _sk(e["tau"], 4), _sk(e["fpr_val"] * 100),
            _sk(e["fpr_test"] * 100), zyma, _sk(e["santykis"])))
    sk += [r"\bottomrule", r"\end{tabularx}",
           r"\vspace{2pt}",
           r"\raggedright\scriptsize $\tau$ parinktas validacijos aibėje ir "
           r"testavimo aibėje netaikomas iš naujo. "
           r"$^{*}$~viršija 1~\% biudžetą: taisyklė renka mažiausią "
           r"$\tau$, tenkinantį biudžetą validacijos aibėje, todėl pagal "
           r"konstrukciją atsiduria prie pat ribos ir atsargos neturi.",
           r"\endgroup"]
    return "\n".join(sk) + "\n"


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("--su-duomenimis", action="store_true", dest="su_duomenimis",
                   help="prideti 2 patikra (reikia imtis.parquet)")
    n = a.parse_args()

    rez = pd.read_csv(REZULTATAI)
    print(f"rezultatai.csv: {len(rez)} eilutes "
          f"({dict(rez.aibe.value_counts())})\n")

    p = [patikra_1(rez)]
    if n.su_duomenimis:
        p.append(patikra_2())
    p += [patikra_3(rez), patikra_4(), patikra_5(rez)]

    for x in p:
        print(f"{_b(x['busena'])} {x['nr']}. {x['pavadinimas']}")
        for s in x["pastabos"]:
            print(f"       {s}")

    if not n.su_duomenimis:
        print("\n[ ? ] 2. train ir test nesikerta - PRALEISTA")
        print("       paleisti su --su-duomenimis")

    DARBINIAI.mkdir(parents=True, exist_ok=True)
    LENTELES.mkdir(parents=True, exist_ok=True)
    eil = ["# Rezultatu patikimumo patikros", "",
           f"Sugeneruota: `python -m src.eksperimentai.patikimumas`", "",
           "| Nr. | Patikra | Busena | Pastabos |", "|---|---|---|---|"]
    for x in p:
        eil.append(f"| {x['nr']} | {x['pavadinimas']} | **{x['busena']}** | "
                   + " · ".join(x["pastabos"]) + " |")
    if not n.su_duomenimis:
        eil.append("| 2 | train ir test nesikerta | PRALEISTA | "
                   "paleisti su `--su-duomenimis` |")
    (DARBINIAI / "patikimumas_test.md").write_text("\n".join(eil) + "\n",
                                                   encoding="utf-8")
    p4 = next(x for x in p if x["nr"] == 4)
    (LENTELES / "patikimumas.tex").write_text(_lentele(p4), encoding="utf-8")

    blogi = [x for x in p if x["busena"] == NEPRAEJO]
    rad = [x for x in p if x["busena"] == RADINYS]
    print(f"\n{'='*60}")
    print(f"{len(p) - len(blogi) - len(rad)} praejo · {len(rad)} radinys · "
          f"{len(blogi)} nepraejo")
    print(f"     {(DARBINIAI / 'patikimumas_test.md').relative_to(SAKNIS)}")
    print(f"     {(LENTELES / 'patikimumas.tex').relative_to(SAKNIS)}")
    raise SystemExit(1 if blogi else 0)


if __name__ == "__main__":
    main()
