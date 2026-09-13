@echo off
rem ====================================================================
rem  Aptikimo sprendimo prototipas (T8).
rem  Atsidaro narsykleje. Sustabdyti - Ctrl+C siame lange.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Diegiamas streamlit...
    pip install streamlit
)

echo.
echo Prototipas atsidarys narsykleje. Uzdaryti - Ctrl+C.
echo.
streamlit run src\prototipas.py

:pabaiga
pause
