# =====================================================================
#  Antras sutvarkymo etapas: vietos diske atlaisvinimas (2026-09-13).
#
#  Pirmas etapas (sutvarkyti.ps1) salino mazus, nebereikalingus failus.
#  Sis salina didelius, kurie ataskaitai nebereikalingi, bet dalis ju
#  atkuriama tik permokant - todel kiekvienas irasas turi pastaba, KAIP
#  ji susigrazinti.
#
#  Ka salina:
#    archive.zip                   1,79 GB  63 CSV jau ispakuoti salia
#    random_forest_derintas_*      2,0 GB   3 x 670 MB; permokymas ~25 min
#    gradientinis_34klases_*       355 MB   3 x 118 MB; permokymas ~20 min
#    rezultatai\apmokyti\_patikra  dumu testo modeliai
#    __pycache__                   Python kesas
#    lenteles\rezultatai.tex       vienintele NENAUDOJAMA generuojama lentele
#
#  Ko NESALINA samoningai:
#    diagnostika_p2.py + p2_sutapimai.csv - juo ismatuotas 5.7 poskyryje
#    pateiktas skaicius (30 sutampanciu eiluciu).
#
#  GRYNAS ASCII. Paleisti is repozitorijos saknies:
#      .\sutvarkyti_diska.ps1 -Perziura     # tik parodo, kiek atlaisvintu
#      .\sutvarkyti_diska.ps1               # atlieka
# =====================================================================
param([switch]$Perziura)

# git raso i stderr ir tada, kai viskas gerai - klaidas tikriname per
# $LASTEXITCODE, ne per klaidu srauta (zr. sutvarkyti.ps1 pastaba).
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$sekami = @{}
foreach ($f in (git ls-files)) { $sekami[($f -replace "/", "\")] = $true }
if ($LASTEXITCODE -ne 0) {
    Write-Host '[KLAIDA] git ls-files nepavyko. Ar cia Git repozitorija?'
    exit 1
}

$viso = 0L

function Dydis($kelias) {
    if (Test-Path -LiteralPath $kelias -PathType Container) {
        $s = (Get-ChildItem -LiteralPath $kelias -Recurse -File -ErrorAction SilentlyContinue |
              Measure-Object -Property Length -Sum).Sum
        if ($null -eq $s) { return 0L } else { return [long]$s }
    }
    return [long](Get-Item -LiteralPath $kelias).Length
}

function MB($baitai) { return "{0,8:N1} MB" -f ($baitai / 1MB) }

function Salinti($kelias, $pastaba) {
    if (-not (Test-Path -LiteralPath $kelias)) {
        Write-Host ("  - nera:      {0}" -f $kelias)
        return
    }
    $d = Dydis $kelias
    $script:viso += $d
    if ($Perziura) {
        Write-Host ("  ? {0}  {1}" -f (MB $d), $kelias)
        if ($pastaba) { Write-Host ("               {0}" -f $pastaba) }
        return
    }
    if ($sekami.ContainsKey($kelias)) {
        git rm -q -f -r -- $kelias
        if ($LASTEXITCODE -ne 0) { Write-Host ("  ! git rm nepavyko: {0}" -f $kelias); return }
        Write-Host ("  x {0}  git rm:   {1}" -f (MB $d), $kelias)
    } else {
        Remove-Item -LiteralPath $kelias -Recurse -Force
        Write-Host ("  x {0}  istrinta: {1}" -f (MB $d), $kelias)
    }
}

Write-Host ""
Write-Host "=== 1. Zaliu duomenu archyvas ==="
Salinti "duomenys\raw\archive.zip" "atsisiuntimas is naujo - zr. README.md (kaggle datasets download)"

Write-Host ""
Write-Host "=== 2. Apmokyti modeliai, kuriu ataskaitai nebereikia ==="
foreach ($s in 42, 43, 44) {
    Salinti "rezultatai\apmokyti\random_forest_derintas_8kat_seed$s.joblib" "permokymas: 04_mokyti_derintus.bat"
    Salinti "rezultatai\apmokyti\random_forest_derintas_8kat_seed$s.json" $null
}
foreach ($s in 42, 43, 44) {
    Salinti "rezultatai\apmokyti\gradientinis_34klases_34klases_seed$s.joblib" "permokymas: 12_formuluotes.bat"
    Salinti "rezultatai\apmokyti\gradientinis_34klases_34klases_seed$s.json" $null
}
Salinti "rezultatai\apmokyti\_patikra" "atsikuria paleidus 01_patikra.bat"

Write-Host ""
Write-Host "=== 3. Kesas ir nenaudojami generuojami failai ==="
foreach ($k in (Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty FullName)) {
    Salinti ($k.Substring($PSScriptRoot.Length + 1)) $null
}
Salinti "ataskaita\lenteles\rezultatai.tex" "nenaudojama ne viename skyriuje; atsikuria per i_latex.py"

Write-Host ""
Write-Host ("Is viso: {0}" -f (MB $viso))
Write-Host ""
if ($Perziura) {
    Write-Host "Perziura - niekas nepakeista. Paleisti be -Perziura."
} else {
    git add -A
    Write-Host "Busena:"
    git status --short
    Write-Host ""
    Write-Host "TOLIAU:  git commit -m ""Pasalinti nebereikalingi dideli failai"""
}
Write-Host ""
