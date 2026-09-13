@echo off
rem ====================================================================
rem  Random Forest
rem  Atskaitos lygis, prie kurio matuojamas prieaugis. Greiciausias.
rem
rem  Trys seed'ai (42, 43, 44) - protokolo 17 punktas.
rem  Rezultatai kaupiami rezultatai\rezultatai.csv po kiekvieno paleidimo.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

echo.
echo Pradzia: %DATE% %TIME%
echo.
python -m src.eksperimentai.paleisti konfig\random_forest.yaml --seed 42 43 44
if errorlevel 1 goto :klaida

echo.
echo Pabaiga: %DATE% %TIME%
echo Lenteles:  python -m src.eksperimentai.i_latex
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Mokymas nutruko. Ankstesni seed'ai jau irasyti i CSV.
echo.

:pabaiga
pause
