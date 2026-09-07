@echo off
rem ====================================================================
rem  Bendra aplinkos paruosimo dalis. Kvieciama is visu kitu .bat failu.
rem  Atskirai paleisti nereikia.
rem
rem  GRYNAS ASCII. Lietuviskos raides cmd.exe lange virsta siuksliu,
rem  todel cia ju nera samoningai (ta pati taisykle kaip build.ps1).
rem ====================================================================

rem Projekto saknis - ten, kur guli sis failas.
cd /d "%~dp0"

rem Vartotojo lygio paketai (%APPDATA%\Python\PythonXXX\site-packages)
rem uzdengia conda aplinkos paketus. Butent del to 2026-09-07 pasirode
rem "NumPy 1.x cannot be run in NumPy 2.x". Isjungiame is anksto.
set PYTHONNOUSERSITE=1
set PYTHONIOENCODING=utf-8

rem TensorFlow informaciniai pranesimai - tik ispejimai ir klaidos.
set TF_CPP_MIN_LOG_LEVEL=2

rem --- Aplinkos aktyvavimas: bandomi trys iprasti keliai ---
call conda activate iot-ids >nul 2>&1
if not "%CONDA_DEFAULT_ENV%"=="iot-ids" (
    call "C:\ProgramData\anaconda3\Scripts\activate.bat" iot-ids >nul 2>&1
)
if not "%CONDA_DEFAULT_ENV%"=="iot-ids" (
    call "%USERPROFILE%\anaconda3\Scripts\activate.bat" iot-ids >nul 2>&1
)
if not "%CONDA_DEFAULT_ENV%"=="iot-ids" (
    call "%LOCALAPPDATA%\anaconda3\Scripts\activate.bat" iot-ids >nul 2>&1
)

rem Aktyvavimo skriptai gali pakeisti darbini aplanka - grazinam savaji,
rem kitaip "python -m src..." nerastu paketo.
cd /d "%~dp0"

rem --- Patikra: aktyvavimas galejo "pavykti" ir neaktyvaves ---
rem Tikrinamas ne CONDA_DEFAULT_ENV, o tikrasis interpretatoriaus kelias:
rem butent jis lemia, kurie paketai bus importuoti.
set APLINKA=
for /f "delims=" %%i in ('python -c "import sys,os;print(os.path.basename(sys.prefix))" 2^>nul') do set APLINKA=%%i

if "%APLINKA%"=="" (
    echo.
    echo [KLAIDA] Python nerastas.
    echo          Atidarykite "Anaconda Prompt" ir paleiskite is ten.
    echo.
    exit /b 1
)

if not "%APLINKA%"=="iot-ids" (
    echo.
    echo [KLAIDA] Aktyvi aplinka yra "%APLINKA%", o reikia "iot-ids".
    echo.
    echo          Paleidus is "base" aplinkos rezultatai butu gauti
    echo          aplinkoje, kurios requirements-lock.txt neaprazo.
    echo.
    echo          Sprendimas:  conda activate iot-ids
    echo          Jei aplinkos nera:
    echo             conda create -n iot-ids python=3.11
    echo             conda activate iot-ids
    echo             pip install -r requirements.txt
    echo.
    exit /b 1
)

exit /b 0
