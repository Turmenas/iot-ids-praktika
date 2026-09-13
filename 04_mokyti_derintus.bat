@echo off
rem ====================================================================
rem  Permokymas su SUDERINTAIS hiperparametrais ant VISOS aibes.
rem
rem  Atskiri konfigai (*_derintas.yaml), kad baziniai rezultatai
rem  rezultatai.csv liktu - ataskaitai reikia palyginimo pries/po.
rem
rem  Po sio: 06_slenkstis.bat, tada i_latex.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

echo.
echo Pradzia: %DATE% %TIME%
python -m src.eksperimentai.paleisti konfig\random_forest_derintas.yaml konfig\gradientinis_derintas.yaml konfig\mlp_derintas.yaml --seed 42 43 44
if errorlevel 1 goto :klaida

echo.
echo Pabaiga: %DATE% %TIME%
echo.
echo TOLIAU:  06_slenkstis.bat   (operaciniai taskai suderintiems modeliams)
echo          python -m src.eksperimentai.i_latex
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nutruko. Baigti paleidimai jau yra rezultatai.csv.
echo.

:pabaiga
pause
