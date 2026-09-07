# -*- coding: utf-8 -*-
"""Eigos juosta. Grynas ASCII - cmd.exe lange Unicode blokai virsta siuksliu."""

from __future__ import annotations

import sys
import time


def juosta(dabar: int, is_viso: int, priesdelis: str = "",
           vienetas: str = "", t0: float | None = None, plotis: int = 26) -> None:
    """Perrasoma vienos eilutes juosta. Baigus - naujos eilutes simbolis.

    Rodyti eiga butina ne del patogumo: 2026-09-07 suderintas Random Forest
    mokesi ~8 min. vienam seed'ui, ir be jokios isvesties nebuvo kaip
    atskirti letai einancio mokymo nuo uzkibusio.
    """
    is_viso = max(int(is_viso), 1)
    dalis = min(max(dabar / is_viso, 0.0), 1.0)
    pilna = int(dalis * plotis)
    laikas = ""
    if t0 is not None and dalis > 0.02:
        praejo = time.perf_counter() - t0
        laikas = f"  {praejo/60:5.1f} min - liko ~{(praejo/dalis - praejo)/60:4.1f} min"
    sys.stdout.write(
        f"\r  {priesdelis:<14s}[{'#'*pilna}{'-'*(plotis-pilna)}] {dalis*100:3.0f} % "
        f" {dabar}/{is_viso} {vienetas}{laikas}      ")
    sys.stdout.flush()
    if dabar >= is_viso:
        sys.stdout.write("\n")
        sys.stdout.flush()
