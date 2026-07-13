# build.ps1 — kompilasi main.pdf dengan Tectonic.
# Pakai:  ./build.ps1
#
# Catatan: main-review.pdf (versi ringan untuk editor/kolega, gambar
# di-downsample ke 300dpi JPEG) tidak dibuat skrip ini -- itu proses
# terpisah yang menyalin seluruh sumber ke folder scratch, mengompres
# figures/, lalu build ulang. Lihat README.md.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== Kompilasi main.tex dengan Tectonic ==" -ForegroundColor Cyan
tectonic -X compile main.tex

if (Test-Path main.pdf) {
    $mb = (Get-Item main.pdf).Length / 1MB
    Write-Host ("Selesai -> main.pdf ({0:N1} MiB)" -f $mb) -ForegroundColor Green
}
