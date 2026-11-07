# Kairos Dev Kit, Windows. Run from this folder:  powershell -ExecutionPolicy Bypass -File install.ps1
# Needs no admin rights. Downloads nothing itself: kairos.py (next to this file) clones the repos.
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Write-Host "Python is not installed. Get it from https://www.python.org/downloads/ (tick 'Add python.exe to PATH'), then run this again."; exit 1 }
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $here "kairos.py"))) { Write-Host "kairos.py is not next to this script. Put both in the same folder."; exit 1 }
Write-Host "Using $($py.Source)"
& python (Join-Path $here "kairos.py") install
if ($LASTEXITCODE -ne 0) { Write-Host "Something failed. Run:  python kairos.py check   and send the output."; exit $LASTEXITCODE }
Write-Host "Done. Next:  python kairos.py next"
