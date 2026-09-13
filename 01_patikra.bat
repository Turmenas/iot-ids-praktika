@echo off
rem ====================================================================
rem  Aplinkos ir grandines patikra. Paleisti PRIES mokyma.
rem  Trunka ~1 min. I rezultatai.csv NERASO.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

echo.
echo ==================================================================
echo  1/4  Bibliotekos ir aplankai
echo ==================================================================
python patikra.py
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  2/4  Pozymiai: 39 -^> 36 ir tapatybiu patikra
echo ==================================================================
python -m src.duomenys.pozymiai
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  3/4  Skaidymas: nutekejimo patikros
echo ==================================================================
python -m src.duomenys.skaidymas patikra
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  4/4  Pilnas ciklas ant 50 000 eiluciu (i CSV neraso)
echo ==================================================================
python -m src.eksperimentai.paleisti konfig\random_forest.yaml --imtis 50000
if errorlevel 1 goto :klaida

echo.
echo ==================================================================
echo  VISOS PATIKROS PRAEJO - TOLIAU: 02_mokyti_viska.bat
echo ==================================================================
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Patikra nepraejo. Mokymo nepradeti, kol nepataisyta.
echo.

:pabaiga
pause
