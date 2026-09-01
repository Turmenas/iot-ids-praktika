# =====================================================================
#  build.ps1 - ataskaitos kompiliavimas
#
#  SVARBU: failas turi likti GRYNU ASCII. PowerShell 5.1 be BOM zymos
#  skaito .ps1 kaip CP1252, todel lietuviskos raides ir Unicode
#  simboliai (- v x) sulauzo sintakse.
#
#  Naudojimas:
#     .\build.ps1            - iprastas kompiliavimas
#     .\build.ps1 -Clean     - pries tai istrina pagalbinius failus
#     .\build.ps1 -Greitas   - tik vienas pdflatex praejimas (be biber)
#
#  Kodel reikia -Clean: jei ankstesnis paleidimas nutruko su klaida,
#  .aux failas lieka nebaigtas (pvz. paskutine eilute "\new"), ir kitas
#  paleidimas luzta su "Undefined control sequence" dar NEPRIEJES prie
#  tavo teksto. Sis skriptas tai aptinka pats ir issivalo automatiskai.
# =====================================================================

param(
    [switch]$Clean,
    [switch]$Greitas
)

$Vardas = "ataskaita"
$Plesiniai = @("aux", "toc", "out", "bcf", "bbl", "blg", "run.xml",
               "lot", "lof", "idx", "ilg", "ind", "fls", "fdb_latexmk")

function Valyti {
    $n = 0
    foreach ($p in $Plesiniai) {
        $f = "$Vardas.$p"
        if (Test-Path $f) { Remove-Item $f -Force; $n++ }
    }
    Write-Host "  Istrinta pagalbiniu failu: $n" -ForegroundColor DarkGray
}

function AuxSugadintas {
    # Nebaigtas .aux paprastai baigiasi nepilna komanda.
    $f = "$Vardas.aux"
    if (-not (Test-Path $f)) { return $false }
    $eil = Get-Content $f -ErrorAction SilentlyContinue
    if ($eil.Count -eq 0) { return $false }
    $pask = ($eil[-1]).Trim()
    if ($pask -eq "") { return $false }
    # Sveikas .aux baigiasi uzdaryta komanda su } arba \gdef eilute
    if ($pask -notmatch "[}\)]$" -and $pask -match "^\\") { return $true }
    return $false
}

Write-Host ""
Write-Host "=== ataskaitos kompiliavimas ===" -ForegroundColor Cyan

# Jei MiKTeX nustatytas klausti pries diegdamas trukstamus paketus,
# pdflatex sustoja ir laukia atsakymo - atrodo kaip uzstrigimas.
# Vienkartinis nustatymas, kad diegtu automatiskai:
#     initexmf --set-config-value="[MPM]AutoInstall=1"
# Ir vienkartinis atnaujinimas:
#     mpm --update-db
#     mpm --update

if ($Clean) {
    Write-Host "-Clean: valau pries pradedant"
    Valyti
}
elseif (AuxSugadintas) {
    Write-Host "  Aptiktas nebaigtas .aux (ankstesnis paleidimas nutruko)." -ForegroundColor Yellow
    Valyti
}

# --- 0/5  literatura.pdf (atskira bibliografija) ---------------------
# Bibliografija generuojama atskirai, nes pilnoje ataskaita.tex
# preambuleje biblatex luzta. Rezultatas ijungiamas per \includepdf.
if (Test-Path "literatura.tex") {
    Write-Host ""
    Write-Host "=== 0/5  literatura.pdf (bibliografija) ===" -ForegroundColor Cyan
    if ($Clean) {
        foreach ($p in $Plesiniai) {
            $f = "literatura.$p"
            if (Test-Path $f) { Remove-Item $f -Force }
        }
    }
    & pdflatex -interaction=nonstopmode -halt-on-error "literatura.tex"
    if ($LASTEXITCODE -eq 0) { & biber literatura }
    if ($LASTEXITCODE -eq 0) {
        & pdflatex -interaction=nonstopmode -halt-on-error "literatura.tex"
    }
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path "literatura.pdf")) {
        Write-Host "  literatura.pdf nesugeneruotas. Zr. literatura.log" -ForegroundColor Red
        Write-Host "  Ataskaita bus kompiliuojama be bibliografijos." -ForegroundColor Yellow
    } else {
        Write-Host "  literatura.pdf paruostas." -ForegroundColor Green
    }
}

# --- 1/4 -------------------------------------------------------------
Write-Host ""
Write-Host "=== 1/4  pdflatex (pirmas praejimas) ===" -ForegroundColor Cyan
& pdflatex -interaction=nonstopmode -halt-on-error "$Vardas.tex"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Pirmas praejimas nepavyko. Valau ir bandau dar karta..." -ForegroundColor Yellow
    Valyti
    & pdflatex -interaction=nonstopmode -halt-on-error "$Vardas.tex"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "KLAIDA. Pirmos trys '!' eilutes is $Vardas.log:" -ForegroundColor Red
    Select-String -Path "$Vardas.log" -Pattern '^!' -Context 0,3 |
        Select-Object -First 3 | ForEach-Object { Write-Host $_ }
    exit 1
}

if ($Greitas) {
    Write-Host ""
    Write-Host "-Greitas: biber ir likusieji praejimai praleisti." -ForegroundColor DarkGray
    exit 0
}

# --- 2/4 -------------------------------------------------------------
Write-Host ""
Write-Host "=== 2/4  biber ===" -ForegroundColor Cyan
& biber $Vardas
if ($LASTEXITCODE -ne 0) {
    Write-Host "biber grazino klaida. Zr. $Vardas.blg" -ForegroundColor Red
    exit 1
}

# --- 3/4, 4/4 --------------------------------------------------------
Write-Host ""
Write-Host "=== 3/4  pdflatex ===" -ForegroundColor Cyan
& pdflatex -interaction=nonstopmode -halt-on-error "$Vardas.tex"

Write-Host "=== 4/4  pdflatex ===" -ForegroundColor Cyan
& pdflatex -interaction=nonstopmode -halt-on-error "$Vardas.tex"

# --- Suvestine -------------------------------------------------------
$log = Get-Content "$Vardas.log" -ErrorAction SilentlyContinue

$klaidos  = @($log | Select-String -Pattern '^!').Count
$undef    = @($log | Select-String -Pattern 'undefined').Count
$overfull = @($log | Select-String -Pattern 'Overfull').Count

$psl = "?"
$m = $log | Select-String -Pattern 'Output written on .* \((\d+) page'
if ($m) { $psl = $m.Matches[0].Groups[1].Value }

Write-Host ""
Write-Host "=== Suvestine ===" -ForegroundColor Cyan
Write-Host "  Puslapiu:            $psl"

if ($klaidos -gt 0) {
    Write-Host "  Klaidu (!):          $klaidos" -ForegroundColor Red
} else {
    Write-Host "  Klaidu (!):          0" -ForegroundColor Green
}

if ($undef -gt 0) {
    Write-Host "  Neissprestu nuorodu: $undef" -ForegroundColor Yellow
    Write-Host "    (jei tik ka pridejai nauju citavimu - paleisk dar karta)"
} else {
    Write-Host "  Neissprestu nuorodu: 0" -ForegroundColor Green
}

Write-Host "  Perpildytu eiluciu:  $overfull  (kosmetika)" -ForegroundColor DarkGray

if ($klaidos -gt 0) {
    Write-Host ""
    Write-Host "Klaidos:" -ForegroundColor Red
    Select-String -Path "$Vardas.log" -Pattern '^!' -Context 0,3 |
        Select-Object -First 5 | ForEach-Object { Write-Host $_ }
    exit 1
}

Write-Host ""
Write-Host "Baigta: $Vardas.pdf" -ForegroundColor Green
Write-Host ""
