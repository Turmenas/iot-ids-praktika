@echo off
rem ====================================================================
rem  Klaidu analize: per-klase metrikos ir sumaisymo struktura.
rem
rem  TEST AIBE CIA NEATIDAROMA. Viskas skaiciuojama is jau issaugotu
rem  sumaisymo matricu (rezultatai\darbiniai\sumaisymas_*_test.csv),
rem  kurias sukure 08_vertinti_test.bat. Modeliai neikeliami, todel
rem  greita ir atminties problemos nera.
rem
rem  Isvestis:
rem      rezultatai\darbiniai\perklasiu_test.csv
rem      rezultatai\darbiniai\klaidu_tipai_test.csv
rem      ataskaita\lenteles\perklase.tex
rem      ataskaita\lenteles\klaidu_tipai.tex
rem      ataskaita\paveikslai\sumaisymas.pdf
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.eksperimentai.klaidos --aibe test
if errorlevel 1 goto :klaida

echo.
echo TOLIAU:  11_nematytos.bat   (T5 - nematytu ataku klasiu testas)
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nepavyko. Ar 08_vertinti_test.bat jau paleistas?
echo          Reikalingi failai: rezultatai\darbiniai\sumaisymas_*_test.csv
echo.

:pabaiga
pause
