# =====================================================================
#  Vienkartinis repozitorijos sutvarkymas (2026-09-13).
#
#  Ka daro:
#    1. Istrina nebereikalingus failus (diagnostika, atsargines kopijos,
#       tuscias metadata.json, bibtestas.* apejimo diagnostika).
#    2. Perkelia ciciot2023_pozymiai.md is ataskaita\skyriai\ i duomenys\
#       - tai duomenu dokumentas, ne skyrius.
#    3. Istrina SENUS .bat vardus. Nauji, sunumeruoti pagal paleidimo
#       eile, jau ideti - zr. README.md.
#
#  Kas sekama Git'e, salinama per `git rm` (istorija lieka). Kas
#  nesekama - paprastu `Remove-Item`.
#
#  Skripta galima paleisti kelis kartus: jau sutvarkyti failai
#  praleidziami su zyma "nera".
#
#  PASTABA (2026-09-13): pirmoji versija naudojo
#  `git ls-files --error-unmatch` kiekvienam failui. Kai failo Git'e
#  nera, ta komanda raso i stderr, o su $ErrorActionPreference = "Stop"
#  PowerShell tai laiko klaida ir nutraukia darba po pirmo failo.
#  Todel sekamu failu sarasas dabar imamas VIENU `git ls-files`, o
#  klaidu srautas nebenaudojamas kaip salyga.
#
#  GRYNAS ASCII. Paleisti is repozitorijos saknies:
#      .\sutvarkyti.ps1
#  Perziura nieko nekeiciant:
#      .\sutvarkyti.ps1 -Perziura
# =====================================================================
param([switch]$Perziura)

# Natyvios komandos (git) raso i stderr ir tada, kai viskas gerai.
# Su "Stop" tai nutrauktu skripta, todel klaidas tikriname patys per
# $LASTEXITCODE.
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

# --- ka salinti ------------------------------------------------------
$salinti = @(
    # biblatex apejimo diagnostika - priezastis nerasta, apejimas veikia
    "ataskaita\bibtestas.tex",
    "ataskaita\bibtestas.aux",
    "ataskaita\bibtestas.bbl",
    "ataskaita\bibtestas.bcf",
    "ataskaita\bibtestas.blg",
    "ataskaita\bibtestas.log",
    "ataskaita\bibtestas.pdf",
    "ataskaita\bibtestas.run.xml",
    # atsargine kopija, likusi is 2 uzduoties
    "ataskaita\saltiniai.bib.bak",
    # neatitinka galutinio ketverto (RF, XGBoost, MLP, autokoderis)
    "src\modeliai\cnn.py",
    # klaidos pedsakas, pagautas 5 uzduotyje ir jau istaisytas
    "nematytos_klaida.txt",
    # tuscias: metaduomenys realiai guli kiekvieno modelio .json faile
    "rezultatai\apmokyti\metadata.json"
)

# --- senieji .bat vardai (nauji sunumeruoti jau ideti) ----------------
$seniBat = @(
    "patikra.bat", "mokyti_viska.bat", "mokyti_rf.bat", "mokyti_xgboost.bat",
    "mokyti_mlp.bat", "mokyti_autoencoder.bat", "derinti.bat",
    "mokyti_derintus.bat", "delsa.bat", "slenkstis.bat", "prototipas.bat",
    "vertinti_test.bat", "slenkstis_test.bat", "klaidos.bat", "nematytos.bat",
    "formuluotes.bat", "patikimumas.bat", "palyginimas.bat"
)

# --- perkelti --------------------------------------------------------
$perkelti = @(
    @{ is = "ataskaita\skyriai\ciciot2023_pozymiai.md"; i = "duomenys\ciciot2023_pozymiai.md" }
)

# --- sekamu failu sarasas: VIENAS git kvietimas ----------------------
$sekami = @{}
foreach ($f in (git ls-files)) {
    $sekami[($f -replace "/", "\")] = $true
}
if ($LASTEXITCODE -ne 0) {
    Write-Host '[KLAIDA] git ls-files nepavyko. Ar cia Git repozitorija?'
    exit 1
}
Write-Host ""
Write-Host "Git seka $($sekami.Count) failu."

function Sekamas($kelias) { return $sekami.ContainsKey($kelias) }

function Salinti($kelias) {
    if (-not (Test-Path $kelias)) { Write-Host "  - nera:      $kelias"; return }
    if ($Perziura) {
        $kaip = if (Sekamas $kelias) { "git rm" } else { "istrinti" }
        Write-Host ("  ? {0,-8} {1}" -f $kaip, $kelias)
        return
    }
    if (Sekamas $kelias) {
        git rm -q -f -- $kelias
        if ($LASTEXITCODE -ne 0) { Write-Host "  ! git rm nepavyko: $kelias"; return }
        Write-Host "  x git rm:    $kelias"
    } else {
        Remove-Item -Force -LiteralPath $kelias
        Write-Host "  x istrinta:  $kelias"
    }
}

Write-Host ""
Write-Host "=== 1. Nebereikalingi failai ==="
foreach ($f in $salinti) { Salinti $f }

Write-Host ""
Write-Host "=== 2. Perkeliami failai ==="
foreach ($p in $perkelti) {
    if (-not (Test-Path $p.is)) { Write-Host "  - nera:      $($p.is)"; continue }
    if (Test-Path $p.i) { Write-Host "  ! jau yra:   $($p.i) - praleista"; continue }
    if ($Perziura) { Write-Host "  ? perkeltu:  $($p.is) -> $($p.i)"; continue }
    if (Sekamas $p.is) {
        git mv -- $p.is $p.i
        if ($LASTEXITCODE -ne 0) { Write-Host "  ! git mv nepavyko: $($p.is)"; continue }
    } else {
        Move-Item -LiteralPath $p.is -Destination $p.i
    }
    Write-Host "  > perkelta:  $($p.is) -> $($p.i)"
}

Write-Host ""
Write-Host "=== 3. Senieji .bat vardai ==="
foreach ($f in $seniBat) { Salinti $f }

Write-Host ""
if ($Perziura) {
    Write-Host "Perziura - niekas nepakeista. Paleisti be -Perziura."
} else {
    git add -A
    Write-Host "Atlikta. Busena:"
    git status --short
    Write-Host ""
    Write-Host "TOLIAU:  git commit -m ""Sutvarkyti failai, .bat pervadinti pagal paleidimo eile"""
}
Write-Host ""
