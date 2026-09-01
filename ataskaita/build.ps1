# =====================================================================
#  Ataskaitos kompiliavimas (be latexmk / be Perl)
#
#  Paleidimas is ataskaita\ aplanko:
#      .\build.ps1
#
#  DEMESIO: sis failas TURI likti ASCII. PowerShell 5.1 skaito .ps1
#  kaip CP1252, jei nera BOM zymos, todel lietuviskos raides ir
#  simboliai like --- arba OK zenklai sulauzo sintakse.
# =====================================================================

$ErrorActionPreference = "Stop"
$pavadinimas = "ataskaita"

function Zingsnis($tekstas) {
    Write-Host ""
    Write-Host "=== $tekstas ===" -ForegroundColor Cyan
}

# --- Patikra, ar LaTeX apskritai yra --------------------------------
if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Host "KLAIDA: pdflatex nerastas." -ForegroundColor Red
    Write-Host "Idiekite MiKTeX:  winget install MiKTeX.MiKTeX" -ForegroundColor Yellow
    Write-Host "Po idiegimo perkraukite PowerShell." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "$pavadinimas.tex")) {
    Write-Host "KLAIDA: $pavadinimas.tex nerastas siame aplanke." -ForegroundColor Red
    Write-Host "Paleiskite skripta is ataskaita\ aplanko." -ForegroundColor Yellow
    exit 1
}

# --- 1/4 -------------------------------------------------------------
Zingsnis "1/4  pdflatex (pirmas praejimas)"
pdflatex -interaction=nonstopmode -halt-on-error "$pavadinimas.tex"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "KLAIDA kompiliuojant. Ieskokite eiluciu su '!' faile $pavadinimas.log" -ForegroundColor Red
    Write-Host "Greita perziura:  Select-String -Path $pavadinimas.log -Pattern '^!' -Context 0,3" -ForegroundColor DarkGray
    exit 1
}

# --- 2/4 -------------------------------------------------------------
Zingsnis "2/4  biber (literaturos sarasas)"
if (Get-Command biber -ErrorAction SilentlyContinue) {
    biber $pavadinimas
} else {
    Write-Host "biber nerastas - literaturos sarasas nebus sugeneruotas." -ForegroundColor Yellow
    Write-Host "MiKTeX Console -> Packages -> idiekite 'biber'." -ForegroundColor Yellow
}

# --- 3/4 ir 4/4 ------------------------------------------------------
Zingsnis "3/4  pdflatex (nuorodos)"
pdflatex -interaction=nonstopmode "$pavadinimas.tex" | Out-Null

Zingsnis "4/4  pdflatex (turinys ir kryzmines nuorodos)"
pdflatex -interaction=nonstopmode "$pavadinimas.tex" | Out-Null

# --- Rezultatas ------------------------------------------------------
Write-Host ""
if (Test-Path "$pavadinimas.pdf") {
    $dydis = [Math]::Round((Get-Item "$pavadinimas.pdf").Length / 1KB, 1)
    Write-Host "[OK] Paruosta: $pavadinimas.pdf ($dydis KB)" -ForegroundColor Green

    $log = Get-Content "$pavadinimas.log" -Raw -ErrorAction SilentlyContinue
    if ($log -match "undefined references") {
        Write-Host "[!] Yra neissprestu nuorodu - paleiskite dar karta." -ForegroundColor Yellow
    }
    if ($log -match "Citation .* undefined") {
        Write-Host "[!] Yra neissprestu citavimu - patikrinkite saltiniai.bib" -ForegroundColor Yellow
    }
} else {
    Write-Host "[X] PDF nesukurtas. Priezastis - $pavadinimas.log faile." -ForegroundColor Red
    exit 1
}
