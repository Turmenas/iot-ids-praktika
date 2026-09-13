@echo off
rem ====================================================================
rem  Operaciniai taskai TEST aibeje.
rem
rem  tau IMAMAS IS VAL (rezultatai\darbiniai\slenkscio_taskai.csv) ir
rem  cia NEPERRENKAMAS: parinkti() siame rezime net nekvieciamas.
rem  Perrinkimas ant test butu nutekejimas - protokolo 21 punktas.
rem
rem  Isvestis i ATSKIRUS failus, val rezultatai nepaliecami:
rem      rezultatai\darbiniai\slenkscio_taskai_test.csv
rem      ataskaita\lenteles\slenkstis_test.tex
rem
rem  Reikalauja, kad 06_slenkstis.bat (val) jau butu paleistas.
rem
rem  ATMINTIS: Random Forest netelpa kartu su kitais. Jei nutruko be
rem  pranesimo, paleiskite dalimis:
rem      python -m src.eksperimentai.slenkstis --taikyti test --modeliai gradientinis mlp
rem      python -m src.eksperimentai.slenkstis --taikyti test --modeliai random_forest
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

if not exist "rezultatai\darbiniai\slenkscio_taskai.csv" goto :nera_val

python -m src.eksperimentai.slenkstis --taikyti test --biudzetas 0.01
if errorlevel 1 goto :klaida

echo.
echo Rezultatai:
echo   rezultatai\darbiniai\slenkscio_taskai_test.csv
echo   ataskaita\lenteles\slenkstis_test.tex
echo.
echo PATIKRA Nr. 4: ar val tau persikelia i test.
echo   Jei test FPR virsija biudzeta daugiau nei 2x, skriptas apie tai
echo   pranesa. Tai RADINYS apie operacinio tasko perkeliamuma, ne klaida
echo   - rasoma i ataskaita, o tau NEPERRENKAMAS.
goto :pabaiga

:nera_val
echo.
echo [KLAIDA] Nerastas rezultatai\darbiniai\slenkscio_taskai.csv
echo          tau turi buti parinktas ant val PIRMA:  06_slenkstis.bat
echo.
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nepavyko. Jei be pranesimo - greiciausiai truko atminties;
echo          zr. pastaba sio failo virsuje.
echo.

:pabaiga
pause
