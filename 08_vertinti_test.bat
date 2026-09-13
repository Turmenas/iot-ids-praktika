@echo off
rem ====================================================================
rem  5 UZDUOTIS: vienintelis prejimas per TEST aibe.
rem
rem  Modeliai NEPERMOKOMI - ikeliami is rezultatai\apmokyti
rem  (--tik-vertinti). Mokymo aibe neatidaroma, todel greita ir
rem  telpa i atminti.
rem
rem  I rezultatai.csv rasoma su aibe=test. Eilutes su aibe=val
rem  NELIECIAMOS: aibe yra metrikos.RAKTAS dalis nuo 2026-09-09.
rem
rem  Po sio:  09_slenkstis_test.bat            -> operaciniai taskai
rem           i_latex --aibe test           -> lenteles
rem
rem  GRYNAS ASCII. Lietuviskos raides cmd.exe lange virsta siuksliu.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

rem --- Ar CSV turi `aibe` stulpeli (T0 taisymas) ---
rem  Tikrinama antraste, ne eiluciu skaicius: be sio stulpelio nulis
rem  val eiluciu ir nesantis stulpelis atrodo vienodai.
findstr /b /c:"modelis,formuluote,seed,aibe," rezultatai\rezultatai.csv >nul 2>&1
if errorlevel 1 goto :nera_aibes

rem --- Uzrakinta pries paleidima (uzduotis_05_planas.md, 3 sk.) ---
echo.
echo ====================================================================
echo  TEST AIBE - vienas prejimas
echo ====================================================================
echo  Modeliai:    tik SUDERINTI konfigai (baziniai i test neina)
echo  Seed'ai:     42 43 44
echo  Formuluote:  8 kategorijos
echo  Slenkstis:   tau imamas is val, cia NEPERRENKAMAS
echo.
echo  Jei prireiks pjuvio, kurio siame sarase nera - jis pridedamas
echo  IVARDIJANT, kad pridetas po fakto.
echo ====================================================================
echo.

for /f %%i in ('findstr /c:",val," rezultatai\rezultatai.csv ^| find /c /v ""') do set VAL_PRIES=%%i
echo Pries paleidima: %VAL_PRIES% val eilutes
echo.
pause

echo.
echo Pradzia: %DATE% %TIME%
echo.

rem --- XGBoost, MLP, autokoderis: telpa i viena procesa ---
python -m src.eksperimentai.paleisti konfig\gradientinis_derintas.yaml konfig\mlp_derintas.yaml konfig\autoencoder.yaml --seed 42 43 44 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida

rem --- Random Forest: PO VIENA SEED'A ---
rem  Suderintas RF yra 670 MB faile ir kelis kartus daugiau atmintyje.
rem  Trys tokie viename procese yra ta pati riba, kuri 2026-09-08
rem  nuzude joblib.load (iseities kodas 137).
python -m src.eksperimentai.paleisti konfig\random_forest_derintas.yaml --seed 42 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida
python -m src.eksperimentai.paleisti konfig\random_forest_derintas.yaml --seed 43 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida
python -m src.eksperimentai.paleisti konfig\random_forest_derintas.yaml --seed 44 --vertinimas test --tik-vertinti
if errorlevel 1 goto :klaida

echo.
echo Pabaiga: %DATE% %TIME%

for /f %%i in ('findstr /c:",val," rezultatai\rezultatai.csv ^| find /c /v ""') do set VAL_PO=%%i
for /f %%i in ('findstr /c:",test," rezultatai\rezultatai.csv ^| find /c /v ""') do set TEST_PO=%%i

echo.
echo --------------------------------------------------------------------
echo  val eilutes:  %VAL_PRIES% -^> %VAL_PO%   (turi buti nepakitusios)
echo  test eilutes: %TEST_PO%             (laukiama 12)
echo --------------------------------------------------------------------

if not "%VAL_PRIES%"=="%VAL_PO%" goto :val_pakito

echo.
echo TOLIAU:
echo   09_slenkstis_test.bat    (tau is val -^> test; protokolo patikra Nr. 4)
echo   python -m src.eksperimentai.i_latex --aibe test --priesaga _test
goto :pabaiga

:nera_aibes
echo.
echo [KLAIDA] rezultatai.csv nerastas arba jame nera `aibe` stulpelio.
echo          Sis .bat reikalauja 2026-09-09 T0 taisymu.
echo          Patikra:  python -m src.eksperimentai.i_latex --aibe val
echo.
goto :pabaiga

:val_pakito
echo.
echo [!!!] VAL EILUCIU SKAICIUS PAKITO: %VAL_PRIES% -^> %VAL_PO%
echo.
echo       To buti negali - aibe yra RAKTAS dalis. Nekartokite paleidimo.
echo       Atstatykite is Git ir tikrinkite metrikos.RAKTAS:
echo           git checkout rezultatai/rezultatai.csv
echo.
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nutruko. Baigti paleidimai jau yra rezultatai.csv su aibe=test,
echo          todel pakartojus jie tiesiog perrasomi ta pacia reiksme.
echo          Jei nutruko be pranesimo - greiciausiai truko atminties;
echo          paleiskite Random Forest po viena seed'a rankomis.
echo.

:pabaiga
pause
