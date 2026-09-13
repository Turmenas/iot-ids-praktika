@echo off
rem ====================================================================
rem  Sprendimo slenkstis: FPR biudzeto laikymasis be permokymo.
rem
rem  Naudoja jau apmokytus modelius (rezultatai\apmokyti). Trunka
rem  kelias minutes. I rezultatai.csv NERASO - isveda atskiras kreives.
rem
rem  ATMINTIS: Random Forest su max_depth=null uzima daugiau nei 3,9 GB.
rem  Jei procesas nutrukus be pranesimo, paleiskite dalimis:
rem      python -m src.eksperimentai.slenkstis --modeliai gradientinis mlp
rem      python -m src.eksperimentai.slenkstis --modeliai random_forest
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.eksperimentai.slenkstis --biudzetas 0.01
if errorlevel 1 goto :klaida

echo.
echo Rezultatai:
echo   rezultatai\darbiniai\slenkscio_kreives.csv
echo   rezultatai\darbiniai\slenkscio_taskai.csv
echo   ataskaita\lenteles\slenkstis.tex
echo.
echo TOLIAU:  07_prototipas.bat (demonstracija) arba 08_vertinti_test.bat
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nepavyko. Jei be pranesimo - greiciausiai truko atminties;
echo          zr. pastaba sio failo virsuje.
echo.

:pabaiga
pause
