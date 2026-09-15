# -*- coding: utf-8 -*-
"""Pozymiu svarba is apmokyto XGBoost modelio (6 uzduotis).

Paleidimas:
    python -m src.eksperimentai.pozymiu_svarba

Isvestis:
    ataskaita/lenteles/pozymiai.tex   tab:pozymiai


KODEL GAIN, O NE SHAP
---------------------
SHAP reikstu dar viena prejima per duomenis, o `mohale2025xai` kaip tik ir
ivardija ju skaiciavimo kaina. Vidutinis informacijos prieaugis (gain)
skaiciuojamas is PACIO modelio - duomenu neatidarant is viso, todel jis
nepriestarauja 5 uzduoties taisyklei, kad `test` liecama viena karta.

Ka gain pasako: kiek vidutiniskai sumazejo nuostolio funkcija, kai medis
skaide pagal ta pozymi. Ko nepasako: kryptes (ar didele reiksme reiskia
ataka) ir saveiku tarp pozymiu. Todel lentele skaitoma kaip "kuo modelis
remiasi", o ne kaip "kas sukelia ataka".
"""
from __future__ import annotations

from pathlib import Path

SAKNIS = Path(__file__).resolve().parents[2]
MODELIS = (SAKNIS / "rezultatai" / "apmokyti"
           / "gradientinis_derintas_8kat_seed42.joblib")
LENTELES = SAKNIS / "ataskaita" / "lenteles"

#: Kiek eiluciu i lentele. Visos 36 i puslapi netilptu ir nieko nepridetu.
VIRSUS = 10

#: Mazos dispersijos pozymiai, sauguoti SAMONINGAI (4 uzduotis).
#: Jei kuris nors ju pateks i virsu, tai bus tiesioginis to sprendimo
#: patvirtinimas; jei ne - lygiai taip pat verta pasakyti.
SAUGOMI = ["ece_flag_number", "cwr_flag_number", "Telnet", "SMTP",
           "IRC", "IGMP"]

#: Trumpi paaiskinimai - ka pozymis matuoja 10/100 paketu lange.
KA_MATUOJA = {
    "Time_To_Live": "paketo TTL, kiek tarpinių mazgų praėjo",
    "Rate": "paketų dažnis lange",
    "IAT": "vidutinis tarpas tarp paketų",
    "Number": "paketų skaičius lange",
    "Tot size": "vidutinis paketo dydis",
    "AVG": "vidutinis paketo dydis",
    "Std": "paketų dydžio standartinis nuokrypis",
    "Variance": "paketų dydžio dispersija",
    "Min": "mažiausias paketo dydis",
    "Max": "didžiausias paketo dydis",
    "Header_Length": "antraštės ilgis",
    "Protocol Type": "protokolo kodas",
    "Duration": "TTL (senas pavadinimas)",
    "syn_flag_number": "SYN vėliavėlių dalis",
    "ack_flag_number": "ACK vėliavėlių dalis",
    "fin_flag_number": "FIN vėliavėlių dalis",
    "rst_flag_number": "RST vėliavėlių dalis",
    "psh_flag_number": "PSH vėliavėlių dalis",
    "syn_count": "SYN paketų skaičius",
    "ack_count": "ACK paketų skaičius",
    "fin_count": "FIN paketų skaičius",
    "rst_count": "RST paketų skaičius",
    "HTTP": "HTTP srauto dalis",
    "HTTPS": "HTTPS srauto dalis",
    "DNS": "DNS srauto dalis",
    "TCP": "TCP srauto dalis",
    "UDP": "UDP srauto dalis",
    "ICMP": "ICMP srauto dalis",
    "ARP": "ARP srauto dalis",
    "SSH": "SSH srauto dalis",
    "DHCP": "DHCP srauto dalis",
    "Tot sum": "bendras baitų kiekis lange",
    "Magnitue": "dydžio magnitudė",
    "Covariance": "kovariacija",
    "Weight": "svoris",
    "Radius": "spindulys",
}


def _sk(x: float, n: int = 1) -> str:
    return f"{x:.{n}f}".replace(".", ",")


def svarba() -> list[tuple[str, float]]:
    import joblib

    if not MODELIS.exists():
        raise SystemExit(f"nerastas modelis: {MODELIS}")
    d = joblib.load(MODELIS)
    b = d["modelis"].get_booster()

    # feature_names_in_ yra numpy masyvas - `or []` ties juo luztu.
    v = getattr(d["modelis"], "feature_names_in_", None)
    vardai = [] if v is None else list(v)
    g = b.get_score(importance_type="gain")

    # Booster raktai buna arba tikri vardai, arba f0, f1, ... - abu atvejai
    # tvarkomi cia, kad lentele niekada nerodytu "f17".
    def vardas(k: str) -> str:
        if k.startswith("f") and k[1:].isdigit() and vardai:
            return vardai[int(k[1:])]
        return k

    is_viso = sum(g.values())
    e = [(vardas(k), v / is_viso * 100) for k, v in g.items()]
    return sorted(e, key=lambda t: -t[1])


def lentele(e: list[tuple[str, float]]) -> str:
    virsus = e[:VIRSUS]
    dalis = sum(v for _, v in virsus)
    penki = sum(v for _, v in e[:5])
    saugomu = [(k, v) for k, v in e if k in SAUGOMI]
    saugomu_dalis = sum(v for _, v in saugomu)

    eilutes = [
        f"{i + 1} & \\texttt{{{k.replace('_', chr(92) + '_')}}} & "
        f"{KA_MATUOJA.get(k, '---')} & {_sk(v)}~\\% \\\\"
        for i, (k, v) in enumerate(virsus)
    ]

    isnasa = (
        r"Vidutinis informacijos prieaugis (gain), normalizuotas iki "
        r"visų " + str(len(e)) + r" naudotų požymių sumos; XGBoost, "
        r"aštuonių kategorijų formuluotė, pradinis dydis 42. Skaičiuojama iš "
        r"paties modelio, o duomenų aibė neatidaroma. Penki pirmieji "
        r"požymiai surenka " + _sk(penki) + r"~\%, o visi dešimt surenka " +
        _sk(dalis) + r"~\% viso prieaugio. Šeši sąmoningai palikti mažos "
        r"dispersijos požymiai kartu surenka " + _sk(saugomu_dalis, 1) +
        r"~\%. Gain nerodo krypties. Jis pasako, kuo modelis remiasi, o ne "
        r"kokia požymio reikšmė reiškia ataką."
    )

    return "\n".join([
        "% Pozymiu svarba (gain) - 6 uzduotis",
        "% GENERUOJAMA is rezultatai/apmokyti/*.joblib",
        "% Ranka NELIESTI - paleisti: python -m src.eksperimentai.pozymiu_svarba",
        r"\begingroup",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{5pt}",
        r"\begin{tabularx}{\textwidth}{@{}>{\raggedleft\arraybackslash}p{0.7cm}"
        r">{\raggedright\arraybackslash}p{3.4cm}"
        r">{\raggedright\arraybackslash}X"
        r">{\centering\arraybackslash}p{2.2cm}@{}}",
        r"\toprule",
        r"\textbf{Nr.} & \textbf{Požymis} & \textbf{Ką matuoja} & "
        r"\textbf{Prieaugio dalis} \\",
        r"\midrule",
        *eilutes,
        r"\bottomrule",
        r"\end{tabularx}",
        r"\vspace{2pt}",
        r"\raggedright\scriptsize " + isnasa,
        r"\endgroup",
        "",
    ])


def main() -> None:
    e = svarba()
    LENTELES.mkdir(parents=True, exist_ok=True)
    (LENTELES / "pozymiai.tex").write_text(lentele(e), encoding="utf-8")
    print(f"[OK] {(LENTELES / 'pozymiai.tex').relative_to(SAKNIS)}")
    print(f"     naudota pozymiu: {len(e)}")
    for i, (k, v) in enumerate(e[:15]):
        zyma = "  <- saugomas" if k in SAUGOMI else ""
        print(f"  {i + 1:2d}. {k:20s} {v:5.2f} %{zyma}")
    print(f"\n  saugomi kartu: "
          f"{sum(v for k, v in e if k in SAUGOMI):.2f} %")


if __name__ == "__main__":
    main()
