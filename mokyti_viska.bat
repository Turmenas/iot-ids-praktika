@echo off
rem ====================================================================
rem  Visi keturi modeliai x 3 seed'ai = 12 paleidimu.
rem
rem  NUOSEKLIAI, NE LYGIAGRECIAI - ir tai ne atsargumas, o butinybe:
rem    1) visi keturi rasytu i ta pati rezultatai.csv, o vienu metu
rem       rasantys procesai ji sugadintu;
rem    2) duomenu paruosimas pasiekia ~3,5 GB, tad keturi procesai
rem       pareikalautu ~14 GB.
rem
rem  Nutrukus nieko neprarandama: kiekvieno paleidimo eilute i CSV
rem  irasoma is karto.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

echo.
echo ==================================================================
echo  12 paleidimu (4 modeliai x 3 seed'ai)
echo  Pradzia: %DATE% %TIME%
echo ==================================================================

call :vienas random_forest  "1/4 Random Forest"
if errorlevel 1 goto :klaida
call :vienas gradientinis   "2/4 XGBoost"
if errorlevel 1 goto :klaida
call :vienas mlp            "3/4 MLP"
if errorlevel 1 goto :klaida
call :vienas autoencoder    "4/4 Autokoderis"
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  VISI 12 PALEIDIMU BAIGTI
echo  Pabaiga: %DATE% %TIME%
echo ==================================================================
echo.
echo Generuojamos ataskaitos lenteles...
python -m src.eksperimentai.i_latex
goto :pabaiga

:vienas
echo.
echo ------------------------------------------------------------------
echo  %~2   [%TIME%]
echo ------------------------------------------------------------------
python -m src.eksperimentai.paleisti konfig\%~1.yaml --seed 42 43 44
exit /b %errorlevel%

:klaida
echo.
echo [KLAIDA] Mokymas nutruko. Iki siol baigti paleidimai jau yra CSV.
echo          Likusius galima paleisti atskirai: mokyti_*.bat
echo.

:pabaiga
pause
