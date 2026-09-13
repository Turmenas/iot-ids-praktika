@echo off
rem ====================================================================
rem  Inferencijos delsos permatavimas CPU (be permokymo).
rem
rem  XGBoost mokytas su device: cuda, todel jo delsa buvo matuota GPU -
rem  o krastinis sliuzas GPU neturi. Cia visi modeliai matuojami vienodai.
rem
rem  Atnaujina inferencija_us stulpeli rezultatai.csv. ~3 min.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.eksperimentai.delsa
if errorlevel 1 goto :klaida

echo.
echo Perkuriamos lenteles...   (TOLIAU: 06_slenkstis.bat)
python -m src.eksperimentai.i_latex
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nepavyko. Jei be pranesimo - truko atminties;
echo          paleiskite dalimis: python -m src.eksperimentai.delsa --modeliai gradientinis mlp
echo.

:pabaiga
pause
