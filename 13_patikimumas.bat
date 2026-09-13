@echo off
rem ====================================================================
rem  T7: rezultatu patikimumo patikros (penkios).
rem
rem  Skaiciuojamos, o ne surasomos: priemimo kriterijus, pazymetas
rem  atliktu nepaleidus komandos, yra spejimas apie savo darba.
rem
rem  TRYS BUSENOS:
rem    PRAEJO    tikrinamas dalykas galioja
rem    RADINYS   negalioja, bet tai REZULTATAS - rasoma i ataskaita
rem    NEPRAEJO  kazkas negerai su pacia grandine
rem
rem  4-oji patikra is anksto numatyta kaip galinti duoti RADINI:
rem  tau renkamas kaip MAZIAUSIAS, tenkinantis biudzeta ant val, todel
rem  pagal konstrukcija atsiduria prie pat ribos ir atsargos neturi.
rem
rem  --su-duomenimis prideda 2 patikra (train ir test nesikerta) -
rem  jai reikia imtis.parquet, todel trunka ~1 min. ilgiau.
rem
rem  Isvestis:
rem      rezultatai\darbiniai\patikimumas_test.md
rem      ataskaita\lenteles\patikimumas.tex
rem
rem  GRYNAS ASCII.
rem ====================================================================
call "%~dp0_aplinka.bat"
if errorlevel 1 goto :pabaiga

python -m src.eksperimentai.patikimumas --su-duomenimis
if errorlevel 1 goto :nepraejo

echo.
echo TOLIAU:  14_palyginimas.bat   (6 uzd. - suvestine ir pozymiu svarba)
goto :pabaiga

:nepraejo
echo.
echo [KLAIDA] Bent viena patikra NEPRAEJO - zr. sarasa virsuje.
echo          RADINYS nera klaida: jis rasomas i ataskaita.
echo          NEPRAEJO reiskia, kad negerai pati grandine.
echo.

:pabaiga
pause
