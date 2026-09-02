"""CICIoT2023 etikeciu ir kategoriju zodynas.

Vieta repozitorijoje: src/duomenys/etiketes.py

Kodel atskiras modulis, o ne label.split("-"):
    Kategorija NEISVEDAMA is etiketes pavadinimo. Skaidymas per "-"
    veikia tik 24 is 34 etikeciu:
      - 10 etikeciu neturi kategorijos priesdelio (SqlInjection, XSS,
        BrowserHijacking, CommandInjection, Backdoor_Malware,
        Uploading_Attack, VulnerabilityScan, DictionaryBruteForce,
        DNS_Spoofing, BenignTraffic)
      - MITM-ArpSpoofing turi priesdeli MITM, bet kategorija - Spoofing
      - VulnerabilityScan priklauso Recon, nors priesdelio neturi

Saltinis: Neto et al., Sensors 23(13):5941, 2023 (bib: neto2023ciciot).
Placiau: duomenys/README.md
"""

from __future__ import annotations

# --------------------------------------------------------------------
# Etikete -> kategorija. 33 atakos + BenignTraffic = 34 irasai.
# --------------------------------------------------------------------
KATEGORIJOS: dict[str, str] = {
    # --- DDoS (12) ---
    "DDoS-ACK_Fragmentation":   "DDoS",
    "DDoS-HTTP_Flood":          "DDoS",
    "DDoS-ICMP_Flood":          "DDoS",
    "DDoS-ICMP_Fragmentation":  "DDoS",
    "DDoS-PSHACK_Flood":        "DDoS",
    "DDoS-RSTFINFlood":         "DDoS",   # be pabraukimo pries Flood!
    "DDoS-SlowLoris":           "DDoS",   # klasikiskai tai DoS, bet rinkinyje DDoS
    "DDoS-SYN_Flood":           "DDoS",
    "DDoS-SynonymousIP_Flood":  "DDoS",
    "DDoS-TCP_Flood":           "DDoS",
    "DDoS-UDP_Flood":           "DDoS",
    "DDoS-UDP_Fragmentation":   "DDoS",
    # --- DoS (4) ---
    "DoS-HTTP_Flood":           "DoS",
    "DoS-SYN_Flood":            "DoS",
    "DoS-TCP_Flood":            "DoS",
    "DoS-UDP_Flood":            "DoS",
    # --- Recon (5) ---
    "Recon-HostDiscovery":      "Recon",
    "Recon-OSScan":             "Recon",
    "Recon-PingSweep":          "Recon",
    "Recon-PortScan":           "Recon",
    "VulnerabilityScan":        "Recon",  # be priesdelio!
    # --- Web-based (6) ---
    "Backdoor_Malware":         "Web",
    "BrowserHijacking":         "Web",
    "CommandInjection":         "Web",
    "SqlInjection":             "Web",
    "Uploading_Attack":         "Web",
    "XSS":                      "Web",
    # --- Brute force (1) ---
    "DictionaryBruteForce":     "BruteForce",
    # --- Spoofing (2) ---
    "DNS_Spoofing":             "Spoofing",
    "MITM-ArpSpoofing":         "Spoofing",  # priesdelis MITM, ne Spoofing!
    # --- Mirai (3) ---
    "Mirai-greeth_flood":       "Mirai",
    "Mirai-greip_flood":        "Mirai",
    "Mirai-udpplain":           "Mirai",
    # --- Gerybinis srautas ---
    "BenignTraffic":            "Benign",
}

GERYBINE = "BenignTraffic"

#: Kategoriju eile ataskaitos lentelems ir sumaisymo matricoms.
#: Fiksuota, kad skirtinguose eksperimentuose stulpeliai nesikeistu.
KATEGORIJU_EILE: list[str] = [
    "Benign", "DDoS", "DoS", "Recon", "Spoofing", "Web", "BruteForce", "Mirai",
]

#: Lietuviski pavadinimai LaTeX lentelems (src/eksperimentai/i_latex.py).
KATEGORIJU_VARDAI: dict[str, str] = {
    "Benign":     "Gerybinis srautas",
    "DDoS":       "Paskirstytos DDoS atakos",
    "DoS":        "DoS atakos",
    "Recon":      "Zvalgyba",
    "Spoofing":   "Klastojimas",
    "Web":        "Ziniatinklio atakos",
    "BruteForce": "Grubios jegos ataka",
    "Mirai":      "Mirai botnetas",
}

ATAKU_ETIKETES = frozenset(KATEGORIJOS) - {GERYBINE}


# --------------------------------------------------------------------
# Registro normalizavimas (2026-09-02)
# --------------------------------------------------------------------
# Naudojamame Kaggle leidime etiketes rasomos DIDZIOSIOMIS raidemis:
#   DDOS-PSHACK_FLOOD, o ne DDoS-PSHACK_Flood.
# Vienas atvejis yra ne registro, o PAVADINIMO skirtumas:
#   BenignTraffic -> BENIGN  (".upper()" duotu BENIGNTRAFFIC, ko faile NERA)
# Todel .upper() sutvarko 33 etiketes is 34, o BENIGN reikia atitikmens.
# Sis sluoksnis leidzia tam paciam kodui veikti su abiem leidimais.

ALIASAI: dict[str, str] = {
    "BENIGNTRAFFIC": "BENIGN",
}

#: Normalizuotas zodynas: RAKTAS DIDZIOSIOMIS -> kategorija.
KATEGORIJOS_NORM: dict[str, str] = {
    ALIASAI.get(e.upper(), e.upper()): k for e, k in KATEGORIJOS.items()
}

GERYBINE_NORM = ALIASAI.get(GERYBINE.upper(), GERYBINE.upper())   # "BENIGN"


def normalizuoti(etikete: str) -> str:
    """Suvienodina vienos etiketes uzrasyma: apkarpo, i DIDZIASIAS, alias."""
    e = etikete.strip().upper()
    return ALIASAI.get(e, e)


def normalizuoti_stulpeli(s):
    """Ta pati pandas Series stulpeliui. Grazina nauja Series."""
    s = s.str.strip().str.upper()
    return s.replace(ALIASAI)


# --------------------------------------------------------------------
# Funkcijos
# --------------------------------------------------------------------
def i_kategorija(etikete: str) -> str:
    """Grazina etiketes kategorija. Meta KeyError, jei etikete nezinoma."""
    try:
        return KATEGORIJOS_NORM[normalizuoti(etikete)]
    except KeyError:
        raise KeyError(
            f"Nezinoma etikete: {etikete!r}. "
            f"Gali buti, kad veidrodis pakeistas. "
            f"Zr. duomenys/README.md"
        ) from None


def patikrinti(etiketes) -> None:
    """Patikrina, ar visos duotos etiketes yra zodyne.

    Kviesti IS KARTO po duomenu ikelimo. Jei veidrodis pakeistas ar
    atsisiusta kita versija, klaida pasirodys cia, o ne kaip tyliai
    dingusi klase modelio rezultatuose.
    """
    etiketes = {normalizuoti(e) for e in etiketes if isinstance(e, str)}
    nezinomos = etiketes - set(KATEGORIJOS_NORM)
    if nezinomos:
        raise ValueError(
            f"Rinkinyje yra {len(nezinomos)} nezinomu etikeciu: "
            f"{sorted(nezinomos)}. Patikrinkite duomenu saltini ir "
            f"atnaujinkite src/duomenys/etiketes.py bei duomenys/README.md."
        )

    truksta = set(KATEGORIJOS_NORM) - etiketes
    if truksta:
        print(f"[ISPEJIMAS] Rinkinyje NERA {len(truksta)} zinomu etikeciu: "
              f"{sorted(truksta)}")
        print("            Imtyje tai gali buti normalu; pilname rinkinyje - ne.")


def prideti_kategorija(df, is_stulpelio: str = "Label",
                       i_stulpeli: str = "kategorija"):
    """Prideda kategorijos stulpeli. Grazina ta pati DataFrame.

    Naudojimas:
        df = prideti_kategorija(df)
        df["kategorija"].value_counts()
    """
    # 9 is 63 CSV failu baigiasi nutrukusia eilute; pandas ja perskaito
    # TYLIAI kaip irasa su Label=NaN. Zr. duomenys/README.md.
    nan = df[is_stulpelio].isna().sum()
    if nan:
        print(f"[ISPEJIMAS] {nan} eilutes su tusciu {is_stulpelio!r} - salinamos "
              f"(nutrukusios CSV eilutes).")
        df = df.dropna(subset=[is_stulpelio]).copy()

    df[is_stulpelio] = normalizuoti_stulpeli(df[is_stulpelio])
    patikrinti(df[is_stulpelio].unique())
    df[i_stulpeli] = df[is_stulpelio].map(KATEGORIJOS_NORM)
    return df


# --------------------------------------------------------------------
# Vidine patikra: python -m src.duomenys.etiketes
# --------------------------------------------------------------------
def _pasitikrinti() -> None:
    laukiama = {
        "DDoS": 12, "DoS": 4, "Recon": 5, "Web": 6,
        "BruteForce": 1, "Spoofing": 2, "Mirai": 3, "Benign": 1,
    }
    faktas: dict[str, int] = {}
    for kat in KATEGORIJOS.values():
        faktas[kat] = faktas.get(kat, 0) + 1

    assert faktas == laukiama, f"Kategoriju kiekiai nesutampa: {faktas}"
    assert len(KATEGORIJOS) == 34, f"Turi buti 34 etiketes, yra {len(KATEGORIJOS)}"
    assert len(ATAKU_ETIKETES) == 33, "Turi buti 33 ataku etiketes"
    assert set(KATEGORIJU_EILE) == set(laukiama), "KATEGORIJU_EILE nesutampa"
    assert set(KATEGORIJU_VARDAI) == set(laukiama), "KATEGORIJU_VARDAI nesutampa"

    # Registro sluoksnis: realaus failo etiketes turi buti atpazistamos
    assert len(KATEGORIJOS_NORM) == 34, "Normalizuotas zodynas sutrumpejo"
    assert normalizuoti("BenignTraffic") == "BENIGN"
    assert i_kategorija("DDOS-PSHACK_FLOOD") == "DDoS"
    assert i_kategorija("DDoS-PSHACK_Flood") == "DDoS"
    assert i_kategorija("BENIGN") == "Benign"
    assert i_kategorija("  benign  ") == "Benign"

    # Irodymas, kodel reikia zodyno, o ne label.split("-")
    sutampa = sum(
        1 for e, k in KATEGORIJOS.items()
        if "-" in e and e.split("-")[0] == k
    )
    print(f"[OK] Etikeciu: {len(KATEGORIJOS)} (33 atakos + gerybinis)")
    print(f"[OK] Kategorijos: {dict(sorted(faktas.items()))}")
    print(f"[INFO] label.split('-') duotu teisinga kategorija tik "
          f"{sutampa}/{len(KATEGORIJOS)} atveju - todel reikia zodyno.")


if __name__ == "__main__":
    _pasitikrinti()
