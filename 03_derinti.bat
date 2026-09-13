@echo off
rem ====================================================================
rem  Hiperparametru derinimas - protokolo 18 punktas.
rem
rem  Atsitiktine paieska ant mokymo aibes DALIES (400 000 eiluciu), kad
rem  tilptu i 30 min. vienam modeliui biudzeta. Geriausia rasta
rem  konfiguracija paskui iraso i konfig\*.yaml IR permokoma ant visos
rem  aibes iprastu paleidimu (mokyti_*.bat).
rem
rem  Is viso ~45-75 min. trims modeliams. Test aibe neatidaroma.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

echo.
echo Pradzia: %DATE% %TIME%

call :vienas random_forest "1/3 Random Forest"
if errorlevel 1 goto :klaida
call :vienas gradientinis  "2/3 XGBoost"
if errorlevel 1 goto :klaida
call :vienas mlp           "3/3 MLP"
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  DERINIMAS BAIGTAS: %DATE% %TIME%
echo ==================================================================
echo.
echo  Rezultatai: rezultatai\darbiniai\derinimas_*.csv
echo.
echo  TOLIAU: geriausias reiksmes irasyti i konfig\*_derintas.yaml, tada
echo          04_mokyti_derintus.bat - permokymas ant visos aibes
echo          ant VISOS aibes - 02_mokyti_viska.bat
goto :pabaiga

:vienas
echo.
echo ------------------------------------------------------------------
echo  %~2   [%TIME%]
echo ------------------------------------------------------------------
python -m src.eksperimentai.derinimas %~1 --bandymai 20 --imtis 400000
exit /b %errorlevel%

:klaida
echo.
echo [KLAIDA] Derinimas nutruko. Baigtu modeliu CSV jau issaugoti.
echo.

:pabaiga
pause
