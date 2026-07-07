# =============================================================================
# sync.ps1 — sinkronkan semua format buku. SUMBER UTAMA = LaTeX (BookTEX/*.tex).
#
# Arah utama (kamu menyunting .tex):
#   BookTEX/*.tex ──► tectonic         ──► PDF B5 (naskah final)
#                └──► reverse.py (.qmd) ──► quarto render ──► website (online resources)
#
# Pemakaian:
#   ./sync.ps1                 # dari .tex: build PDF + update .qmd + render website
#   ./sync.ps1 -PdfOnly        # cuma build PDF B5
#   ./sync.ps1 -SkipRender     # update .qmd tapi lewati 'quarto render' (cepat)
#   ./sync.ps1 -SkipWeb        # cuma PDF, jangan sentuh website
#   ./sync.ps1 -Status         # laporan status, tidak mengubah apa pun
#
# Arah balik (jarang; menarik konten DARI website ke .tex):
#   ./sync.ps1 -FromQmd        # .qmd ──► .tex  (bootstrap/impor). Hormati pengaman:
#                              #   lewati bab yang .tex-nya sudah disunting manual.
#   ./sync.ps1 -FromQmd -Force # paksa timpa .tex dari .qmd
# =============================================================================
param(
    [switch]$Status,       # cuma laporan status
    [switch]$PdfOnly,      # cuma build PDF (= SkipWeb)
    [switch]$SkipRender,   # reverse ke .qmd tapi jangan quarto render
    [switch]$SkipWeb,      # jangan update website sama sekali
    [switch]$SkipPdf,      # jangan build PDF
    [switch]$FromQmd,      # ARAH BALIK: qmd -> tex (forward/bootstrap)
    [switch]$Force         # paksa (--force) untuk -FromQmd
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
function Step($n, $msg) { Write-Host "`n[$n] $msg" -ForegroundColor Cyan }
function Skip($n, $msg) { Write-Host "`n[$n] (dilewati) $msg" -ForegroundColor DarkGray }

# --- Status: tidak mengubah apa pun -----------------------------------------
if ($Status) { python BookTEX/tools/convert.py --status; return }

# --- Arah balik: qmd -> tex (bootstrap/impor konten dari website) -----------
if ($FromQmd) {
    Step 1 "ARAH BALIK  website/chapters/*.qmd  ->  BookTEX/chapters/*.tex"
    if ($Force) { python BookTEX/tools/convert.py --force }
    else        { python BookTEX/tools/convert.py }
    Write-Host "`nSelesai (impor dari .qmd). Jalankan ./sync.ps1 untuk build PDF + website." -ForegroundColor Green
    return
}

if ($PdfOnly) { $SkipWeb = $true }

# --- 1) .tex -> PDF B5 -------------------------------------------------------
if (-not $SkipPdf) {
    Step 1 "BookTEX/main.tex  ->  PDF B5 (Tectonic)"
    Push-Location BookTEX
    try {
        tectonic main.tex
        if (Test-Path main.pdf) {
            $mb = (Get-Item main.pdf).Length / 1MB
            Write-Host ("    -> BookTEX/main.pdf ({0:N1} MiB)" -f $mb) -ForegroundColor Green
        }
    } finally { Pop-Location }
} else { Skip 1 "build PDF" }

# --- 2) .tex -> .qmd (reverse) ----------------------------------------------
if (-not $SkipWeb) {
    Step 2 "BookTEX/chapters/*.tex  ->  website/chapters/*.qmd (reverse-sync)"
    python BookTEX/tools/reverse.py
} else { Skip 2 "update website (.qmd)" }

# --- 3) .qmd -> website (quarto render) -------------------------------------
if (-not $SkipWeb -and -not $SkipRender) {
    Step 3 "quarto render  ->  website HTML/DOCX"
    Push-Location website
    try { quarto render } finally { Pop-Location }
} elseif (-not $SkipWeb) { Skip 3 "quarto render (pakai -SkipRender)" }

Write-Host "`nSinkronisasi selesai." -ForegroundColor Green
