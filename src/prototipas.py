# -*- coding: utf-8 -*-
"""
Aptikimo sprendimo prototipas: srautas -> pozymiai -> inferencija -> signalas.

Paleidimas:
    streamlit run src/prototipas.py

KODEL SLENKSTIS, O NE ARGMAX
----------------------------
Prototipas naudoja ta pati sprendimo taska, kaip ir vertinimas: ataka
skelbiama tik jei bendra ataku tikimybe virsija tau. Prie argmax jis
demonstruotu 21-32 % klaidingu teigiamu - t. y. rodytu tai, ka pats
darbas vadina netinkamu eksploatacijai.

TEST AIBE CIA NENAUDOJAMA
-------------------------
Demonstracijai imamos VALIDACIJOS aibes eilutes. Test aibe lieka
neliesta iki 5 uzduoties (protokolo 19 punktas) - net demonstracijoje.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

SAKNIS = Path(__file__).resolve().parents[1]

# `streamlit run src/prototipas.py` nustato sys.path[0] i `src/`, ne i
# projekto sakni, todel `from src.duomenys import ...` nerandamas.
# Sakni pridedame PRIES bet kokius `src.` importus.
if str(SAKNIS) not in sys.path:
    sys.path.insert(0, str(SAKNIS))

import numpy as np
import pandas as pd
import streamlit as st
APMOKYTI = SAKNIS / "rezultatai" / "apmokyti"
TASKAI = SAKNIS / "rezultatai" / "darbiniai" / "slenkscio_taskai.csv"
GERYBINE = "Benign"

#: Modulio priesaga -> (vardas lenteleje, ar butinas normalizavimas)
TIPAI = {
    "random_forest": ("Random Forest", False),
    "gradientinis": ("XGBoost", False),
    "mlp": ("MLP", True),
    "autoencoder": ("Autokoderis", True),
}


def rasti_modelius(seed: int = 42) -> tuple[dict, list[str]]:
    """Suranda issaugotus modelius aplanke, o ne remiasi ikaltais vardais.

    Pirmoji versija vardus turejo ikaltus, todel permokius BAZINI MLP
    prototipas vis tiek rode klaida - jis ieskojo SUDERINTO. Dabar
    siulomi tik tie modeliai, kurie tikrai yra ir tikrai veiks.

    Grazina ({rodomas vardas: (zyma, tipo vardas)}, [praleistu paaiskinimai]).
    """
    rasti, praleisti = {}, []
    for f in sorted(APMOKYTI.glob(f"*_seed{seed}.joblib")):
        zyma = f.stem
        tipas = next((k for k in TIPAI if zyma.startswith(k)), None)
        if tipas is None:
            continue
        vardas, reikia_skales = TIPAI[tipas]
        konfigas = zyma.split("_8kat")[0].split("_dvejetaine")[0]
        rodomas = f"{vardas} ({'suderintas' if 'derintas' in konfigas else 'bazinis'})"

        if reikia_skales and not f.with_suffix(".skale.joblib").exists():
            praleisti.append(f"{rodomas} - issaugotas be skales, permokykite "
                             f"konfiguracija `konfig/{konfigas}.yaml`")
            continue
        rasti[rodomas] = (zyma, vardas)
    return rasti, praleisti


# ─── Ikelimas ────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Ikeliamas modelis...")
def ikelti_modeli(zyma: str):
    """Grazina (ivercio funkcija, klases, skale, priziurimas, slenkstis).

    Priziurimiems `ivercio funkcija` grazina (n, k) tikimybiu matrica;
    autokoderiui - (n,) atkurimo paklaida. Bendra tik tai, kad didesne
    reiksme reiskia didesne atakos tikimybe.
    """
    import joblib

    kelias = APMOKYTI / f"{zyma}.joblib"
    if not kelias.exists():
        st.error(f"Nerastas {kelias.name}. Pirma paleiskite mokyma.")
        st.stop()

    d = joblib.load(kelias)
    skale = None
    sk_kelias = kelias.with_suffix(".skale.joblib")
    if sk_kelias.exists():
        from src.duomenys.pozymiai import Skale
        skale = Skale.ikelti(sk_kelias)

    if zyma.startswith("random_forest"):
        return d.predict_proba, d.classes_, skale, True, None

    if zyma.startswith("gradientinis"):
        m = d["modelis"]
        try:                       # sliuze GPU nera - inferencija CPU
            m.set_params(device="cpu")
        except Exception:
            pass
        return m.predict_proba, d["kodavimas"].classes_, skale, True, None

    if zyma.startswith("mlp"):
        import tensorflow as tf
        keras = tf.keras.models.load_model(kelias.with_suffix(".keras"))
        return (lambda X: keras.predict(X, batch_size=4096, verbose=0),
                d["kodavimas"].classes_, skale, True, None)

    if zyma.startswith("autoencoder"):
        # Autokoderis klasiu neturi: jis grazina atkurimo paklaida, o
        # sprendima priima pagal slenksti, kalibruota ant VAL gerybinio
        # srauto (protokolo 21 punktas). Slenkstis issaugotas su modeliu -
        # cia jis NEPERSKAICIUOJAMAS, kitaip demonstracija kalibruotusi
        # ant savo pacios duomenu.
        import tensorflow as tf
        keras = tf.keras.models.load_model(kelias.with_suffix(".keras"))

        def paklaida(X):
            X = np.asarray(X)
            atkurta = keras.predict(X, batch_size=4096, verbose=0)
            return np.mean((X - atkurta) ** 2, axis=1)

        return (paklaida, np.array([GERYBINE, "Ataka"]), skale, False,
                float(d["slenkstis"]))

    raise KeyError(zyma)



@st.cache_data(show_spinner="Ikeliamas srautas...")
def ikelti_srauta(n: int, tolygi: bool = False, seed: int = 0):
    """VALIDACIJOS aibes atkarpa. Test aibe neliesta.

    `tolygi=False` - natūrali sudetis, kokia yra rinkinyje. Joje DDoS
    sudaro 43 % langu, nes riba 100 000 taikyta ETIKETEI, o DDoS turi
    12 etikeciu, kai BruteForce - viena. Tai tikra rinkinio savybe, ne
    prototipo trukumas.

    `tolygi=True` - po lygiai is kiekvienos kategorijos. Skirta TIK
    demonstracijai: taip matomi visi atakų tipai, o ne vien potvyniai.
    Metrikos tokiame sraute nera reprezentatyvios ir taip pazymetos.
    """
    from src.duomenys import pozymiai, skaidymas

    df = pd.read_parquet(pozymiai.IMTIS)
    idx = skaidymas.ikelti()
    X, _, y_kat = pozymiai.atrinkti(df, tikrinti=False)
    y = y_kat.to_numpy()
    rng = np.random.default_rng(seed)
    val = idx["val"]

    if not tolygi:
        imti = rng.permutation(val)[:n]
    else:
        kat = y[val]
        vienai = max(n // len(np.unique(kat)), 1)
        dalys = []
        for k in np.unique(kat):
            k_idx = val[kat == k]
            dalys.append(rng.permutation(k_idx)[:min(vienai, len(k_idx))])
        imti = rng.permutation(np.concatenate(dalys))

    return X.iloc[imti].reset_index(drop=True), y[imti]


def numatytas_tau(vardas: str) -> float:
    if TASKAI.exists():
        t = pd.read_csv(TASKAI)
        e = t[(t.modelis == vardas) & (t.taskas == "slenkstis")]
        if not e.empty:
            return float(e.tau.iloc[0])
    return 0.98


# ─── Sasaja ──────────────────────────────────────────────────────────

st.set_page_config(page_title="IoT atakų aptikimas", layout="wide")
st.title("IoT tinklo srauto atakų aptikimas")
st.caption("Prototipas · CICIoT2023 · sprendimo taškas parenkamas pagal "
           "klaidingų teigiamų biudžetą, ne pagal argmax")

with st.sidebar:
    st.header("Nustatymai")
    MODELIAI, praleisti = rasti_modelius()
    if not MODELIAI:
        st.error("Nerasta nė vieno tinkamo modelio. Paleiskite mokyti_viska.bat")
        st.stop()
    pasirinktas = st.selectbox("Modelis", list(MODELIAI))
    zyma, vardas = MODELIAI[pasirinktas]
    if praleisti:
        st.caption("Nerodomi: " + " · ".join(praleisti))

    priziurimas = not zyma.startswith("autoencoder")
    if priziurimas:
        tau = st.slider("Sprendimo slenkstis τ", 0.50, 0.9999,
                        numatytas_tau(vardas), 0.0001, format="%.4f",
                        help="Ataka skelbiama, kai bendra atakų tikimybė "
                             "viršija τ. Didesnis τ — mažiau klaidingų "
                             "signalų, bet ir mažiau aptiktų atakų.")
    else:
        tau = None
        st.info("Autokoderis klasių neturi: sprendimas priimamas pagal "
                "atkūrimo paklaidos slenkstį, kalibruotą ant validacijos "
                "aibės gerybinio srauto (99-asis procentilis). Slenkstis "
                "išsaugotas su modeliu ir čia neperskaičiuojamas.")
    sudetis = st.radio(
        "Srauto sudėtis", ["natūrali", "tolygi (demonstracijai)"],
        help="Natūralioje DDoS sudaro 43 % langų — riba 100 000 taikyta "
             "etiketei, o DDoS turi 12 etikečių. Tolygioje po lygiai iš "
             "kiekvienos kategorijos, kad matytųsi visi atakų tipai.")
    tolygi = sudetis.startswith("tolygi")
    n_eiluciu = st.select_slider("Srauto ilgis (langų)",
                                 [2000, 5000, 10000, 20000], value=5000)
    dydis = st.select_slider("Paketo dydis", [100, 250, 500, 1000], value=250)
    greitis = st.slider("Pauzė tarp paketų, s", 0.0, 0.5, 0.05, 0.05)
    startas = st.button("Paleisti srautą", type="primary", use_container_width=True)

proba_f, klases, skale, priziurimas, ae_slenkstis = ikelti_modeli(zyma)
X, y = ikelti_srauta(n_eiluciu, tolygi)
i_ben = list(klases).index(GERYBINE) if priziurimas else None

st.sidebar.metric("Gerybinio srauto dalis", f"{(y == GERYBINE).mean()*100:.1f} %")
if tolygi:
    st.sidebar.warning("Tolygus srautas skirtas tik demonstracijai — "
                       "klaidingų teigiamų ir aptikimo dalys jame "
                       "nereprezentatyvios.")

if not startas:
    st.info("Nustatykite parametrus ir spauskite **Paleisti srautą**. "
            "Naudojama validacijos aibė — testavimo aibė nepaliečiama.")
    st.stop()

# ─── Srauto apdorojimas ──────────────────────────────────────────────

k1, k2, k3, k4 = st.columns(4)
p_apdorota, p_signalai, p_fpr, p_delsa = (k1.empty(), k2.empty(),
                                          k3.empty(), k4.empty())
juosta = st.progress(0.0)
g1, g2 = st.columns([2, 1])
vieta_grafikas = g1.empty()
vieta_kategorijos = g2.empty()
st.subheader("Aptikimas pagal kategorijas")
vieta_kat_lentele = st.empty()
st.subheader("Paskutiniai pavojaus signalai")
vieta_lentele = st.empty()

istorija, signalai_sar = [], []
pagal_kategorija: dict[str, list[int]] = {}
n_sig = n_ger = n_ger_klaid = n_atak = n_atak_rasta = 0
delsos = []

for pradzia in range(0, len(X), dydis):
    dalis = X.iloc[pradzia:pradzia + dydis]
    tikra = y[pradzia:pradzia + dydis]

    ivestis = skale.transform(dalis) if skale is not None else dalis
    t0 = time.perf_counter()
    P = proba_f(ivestis)
    delsos.append((time.perf_counter() - t0) / len(dalis) * 1e6)

    if priziurimas:
        ataku_tik = 1 - np.asarray(P)[:, i_ben]
        P_be = np.asarray(P).copy()
        P_be[:, i_ben] = -1
        kategorija = np.asarray(klases)[P_be.argmax(axis=1)]
        signalas = ataku_tik > tau
    else:
        # Autokoderis: ivertis yra atkurimo paklaida, kategorijos nera.
        ataku_tik = np.asarray(P)
        kategorija = np.full(len(ataku_tik), "Ataka")
        signalas = ataku_tik > ae_slenkstis

    n_sig += int(signalas.sum())
    ger = tikra == GERYBINE
    n_ger += int(ger.sum())
    n_ger_klaid += int(signalas[ger].sum())
    n_atak += int((~ger).sum())
    n_atak_rasta += int(signalas[~ger].sum())

    for k in np.unique(tikra):
        jos = tikra == k
        r = pagal_kategorija.setdefault(k, [0, 0])
        r[0] += int(jos.sum())
        r[1] += int(signalas[jos].sum())

    istorija.append({"paketas": len(istorija) + 1,
                     "signalai": int(signalas.sum()),
                     "iš jų klaidingi": int(signalas[ger].sum())})

    for j in np.where(signalas)[0][-6:]:
        signalai_sar.append({
            "langas": pradzia + int(j),
            "kategorija": kategorija[j],
            "įvertis": round(float(ataku_tik[j]), 4),
            "tikroji": tikra[j],
            "teisinga": "taip" if tikra[j] != GERYBINE else "KLAIDINGAS",
        })

    p_apdorota.metric("Apdorota langų", f"{pradzia + len(dalis):,}".replace(",", " "))
    p_signalai.metric("Pavojaus signalų", f"{n_sig:,}".replace(",", " "))
    p_fpr.metric("Klaidingi teigiami",
                 f"{n_ger_klaid / max(n_ger, 1) * 100:.2f} %",
                 delta=f"aptikta {n_atak_rasta / max(n_atak, 1) * 100:.1f} %",
                 delta_color="off")
    p_delsa.metric("Inferencijos delsa", f"{np.mean(delsos):.1f} µs")
    juosta.progress(min((pradzia + len(dalis)) / len(X), 1.0))

    vieta_grafikas.line_chart(pd.DataFrame(istorija).set_index("paketas"),
                              height=260)
    kat = pd.Series([s["kategorija"] for s in signalai_sar]).value_counts()
    if not kat.empty:
        vieta_kategorijos.bar_chart(kat, height=260)
    kl = pd.DataFrame([
        {"kategorija": k, "langų sraute": v[0], "signalų": v[1],
         "aptikta, %": round(v[1] / v[0] * 100, 1) if v[0] else 0.0}
        for k, v in pagal_kategorija.items()])
    # Gerybiniam srautui "aptikta" reiskia KLAIDINGUS signalus - todel
    # rikiuojama taip, kad prasciausiai atpazistamos klases butu virsuje.
    kl["_r"] = np.where(kl.kategorija == GERYBINE, -1, kl["aptikta, %"])
    vieta_kat_lentele.dataframe(
        kl.sort_values("_r").drop(columns="_r"),
        use_container_width=True, hide_index=True)

    vieta_lentele.dataframe(pd.DataFrame(signalai_sar[-12:][::-1]),
                            use_container_width=True, hide_index=True)

    if greitis:
        time.sleep(greitis)

st.success(
    f"Baigta. Apdorota {len(X):,} langų · signalų {n_sig:,} · "
    f"klaidingi teigiami {n_ger_klaid / max(n_ger,1)*100:.2f} % · "
    f"aptikta {n_atak_rasta / max(n_atak,1)*100:.1f} % atakų · "
    f"vidutinė delsa {np.mean(delsos):.1f} µs "
    f"(šliuzo biudžetas 20–50 ms)".replace(",", " "))
