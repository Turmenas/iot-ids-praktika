@echo off
rem ====================================================================
rem  T6: dvejetaine ir 34 klasiu formuluotes - TIK palyginimui su
rem  literatura (almahaqeri2026gradient, tas pats CICIoT2023).
rem
rem  Tik geriausias priziurimas modelis (XGBoost, suderinti parametrai).
rem  Hiperparametrai TIE PATYS kaip 8 kategoriju uzduotyje: perderinti
rem  kiekvienai formuluotei reikstu lyginti su literatura kitokiu modeliu.
rem
rem  Du zingsniai kiekvienam konfigui:
rem      1) mokymas + vertinimas ant VAL  -> aibe=val eilutes
rem      2) --tik-vertinti ant TEST       -> aibe=test eilutes
rem  Modelis mokomas VIENA karta; antras zingsnis tik prognozuoja.
rem
rem  TRUKME: 34 klasiu uzduotis augina 800 x 34 = 27 200 medziu vietoj
rem  6 400, todel ji viena gali uztrukti ~25 min. trims seed'ams.
rem  Dvejetaine - greiciausia is visu.
rem
rem  PALYGINIMAS TIES ARGMAX, ne ties FPR biudzetu: literatura skelbia
rem  argmax skaicius, ir gretinti galima tik tame paciame taske. 5.2
rem  skyriaus lenteles lieka ties biudzetu.
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.modeliai.bazinis
if errorlevel 1 goto :kontraktas

echo.
echo Pradzia: %DATE% %TIME%
echo.

echo === 1/4  DVEJETAINE - mokymas ir val
python -m src.eksperimentai.paleisti konfig\gradientinis_dvejetaine.yaml --seed 42 43 44
if errorlevel 1 goto :klaida

echo.
echo === 2/4  DVEJETAINE - test (be permokymo)
python -m src.eksperimentai.paleisti konfig\gradientinis_dvejetaine.yaml --seed 42 43 44 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida

echo.
echo === 3/4  34 KLASES - mokymas ir val  (ilgiausias zingsnis)
python -m src.eksperimentai.paleisti konfig\gradientinis_34klases.yaml --seed 42 43 44
if errorlevel 1 goto :klaida

echo.
echo === 4/4  34 KLASES - test (be permokymo)
python -m src.eksperimentai.paleisti konfig\gradientinis_34klases.yaml --seed 42 43 44 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida

echo.
echo Pabaiga: %DATE% %TIME%

python -m src.eksperimentai.i_latex --aibe test --priesaga _test
if errorlevel 1 goto :klaida

echo.
echo TOLIAU:  13_patikimumas.bat   (T7 - patikimumo patikros)
goto :pabaiga

:kontraktas
echo.
echo [KLAIDA] Modelio kontraktas nepilnas - zr. sarasa virsuje.
echo.
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nutruko. Baigti paleidimai jau yra rezultatai.csv;
echo          pakartojus jie perrasomi ta pacia reiksme.
echo          Jei truko atminties - paleiskite po viena seed'a.
echo.

:pabaiga
pause
