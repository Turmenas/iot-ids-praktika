@echo off
rem ====================================================================
rem  T5: nematytu ataku klasiu testas (protokolo 22-23 punktai).
rem
rem  Trys PERMOKYMAI: XGBoost be DDOS-SLOWLORIS, be RECON-PORTSCAN,
rem  be DICTIONARYBRUTEFORCE. Kiekvienam tau parenkamas ant VAL ir
rem  taikomas TEST - tau ant test neperrenkamas niekada.
rem
rem  AUTOKODERIS NEPERMOKOMAS: jis mokomas tik is BENIGN, todel visos
rem  33 ataku klases jam ir taip nematytos. Permokymas be vienos ju
rem  duotu ta pati modeli.
rem
rem  SVORIAI imami is PILNOS mokymo aibes: kitaip permokytas modelis
rem  skirtusi nuo bazinio dviem dalykais - trukstama klase IR kitokiu
rem  balansavimu. Patikrinta: Benign svoris kitaip pakiltu 3,80 -> 5,00.
rem
rem  Trunka ~10 min. (trys mokymai po ~2 min. GPU + prognozes).
rem
rem  Isvestis:
rem      rezultatai\darbiniai\nematytos_test.csv
rem      rezultatai\darbiniai\perklasiu_tau_test.csv
rem      ataskaita\lenteles\nematytos.tex
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

if not exist "rezultatai\apmokyti\gradientinis_derintas_8kat_seed42.joblib" goto :nera_modelio

rem --- Kontrakto patikra PRIES duomenu ikelima ---
rem  2026-09-09: Gradientinis._ikelti buvo dinges, ir klaida pasirode
rem  tik po to, kai jau buvo ikeltas 2,4 mln. eiluciu parquet.
rem  Trukstamas metodas patikrinamas per sekunde, todel tikrinamas cia.
python -m src.modeliai.bazinis
if errorlevel 1 goto :kontraktas

echo.
echo Pradzia: %DATE% %TIME%
python -m src.eksperimentai.nematytos
if errorlevel 1 goto :klaida
echo.
echo Pabaiga: %DATE% %TIME%

echo.
echo TOLIAU:  12_formuluotes.bat   (T6 - dvejetaine ir 34 klasiu)
echo          T7 - patikimumo patikros
goto :pabaiga

:kontraktas
echo.
echo [KLAIDA] Modelio kontraktas nepilnas - zr. sarasa virsuje.
echo          Duomenys neikeliami, kol to nera.
echo.
goto :pabaiga

:nera_modelio
echo.
echo [KLAIDA] Nerastas bazinis modelis:
echo          rezultatai\apmokyti\gradientinis_derintas_8kat_seed42.joblib
echo          Pirma:  04_mokyti_derintus.bat
echo.
goto :pabaiga

:klaida
echo.
echo [KLAIDA] Nutruko. Jei be pranesimo - greiciausiai truko atminties.
echo          Paleiskite po viena klase:
echo             python -m src.eksperimentai.nematytos --klases DDOS-SLOWLORIS
echo.

:pabaiga
pause
