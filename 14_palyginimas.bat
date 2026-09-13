@echo off
rem ====================================================================
rem  6 UZDUOTIS - metodu efektyvumo palyginimas.
rem
rem  NAUJU MATAVIMU NEDARO. Nei modeliai mokomi, nei test aibe
rem  atidaroma: suvestine surenkama is rezultatai.csv ir slenkscio
rem  tasku, pozymiu svarba - is jau apmokyto XGBoost modelio.
rem
rem  Priemimo kriterijus: po sio paleidimo rezultatai\rezultatai.csv
rem  turi likti NEPAKITES (45 eilutes).
rem
rem  Isvestis:
rem      ataskaita\lenteles\suvestine.tex
rem      ataskaita\lenteles\pozymiai.tex
rem      ataskaita\paveikslai\kompromisai.pdf
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.eksperimentai.suvestine
if errorlevel 1 goto :klaida

echo.
python -m src.eksperimentai.pozymiu_svarba
if errorlevel 1 goto :klaida

echo.
echo TOLIAU:  cd ataskaita ^&^& .\build.ps1
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nepavyko. Ar 08_vertinti_test.bat ir 09_slenkstis_test.bat
echo          jau paleisti? Reikalingi failai:
echo            rezultatai\rezultatai.csv (su test eilutemis)
echo            rezultatai\darbiniai\slenkscio_taskai_test.csv
echo            rezultatai\darbiniai\perklasiu_tau_test.csv
echo            rezultatai\apmokyti\gradientinis_derintas_8kat_seed42.joblib
echo.

:pabaiga
pause
