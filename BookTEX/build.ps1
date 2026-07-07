# build.ps1 — kompilasi buku ke PDF B5 dengan Tectonic.
# Pakai:  ./build.ps1            (kompilasi main.tex -> main.pdf)
#         ./build.ps1 -Convert   (regenerasi .tex dari .qmd dulu, lalu kompilasi)
param([switch]$Convert)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Convert) {
    Write-Host "== Regenerasi fragmen LaTeX dari .qmd ==" -ForegroundColor Cyan
    python tools/convert.py
}

Write-Host "== Kompilasi main.tex dengan Tectonic ==" -ForegroundColor Cyan
tectonic main.tex

if (Test-Path main.pdf) {
    $mb = (Get-Item main.pdf).Length / 1MB
    Write-Host ("Selesai -> main.pdf ({0:N1} MiB)" -f $mb) -ForegroundColor Green
}
