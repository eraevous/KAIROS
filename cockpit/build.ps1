# Build the Kairos Cockpit on Windows: read PR state into the records, then render with the Kairos theme.
#
#   $env:RECORDS = "C:\src\relay-kit-private"; .\build.ps1 [-Mark amber|blue] [-Out DIR] [-NoFetch]
#
# Same steps and outputs as build.sh. Output defaults to $HOME\.kairos\cockpit, never this repository.
param(
  [ValidateSet("amber", "blue")][string]$Mark = "amber",
  [string]$Out = (Join-Path $HOME ".kairos\cockpit"),
  [switch]$NoFetch
)
$ErrorActionPreference = "Stop"
if (-not $env:RECORDS) { throw "set `$env:RECORDS to your local clone of the private records" }
$here = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $here "..")).Path
$outFull = [System.IO.Path]::GetFullPath($Out)
if ($outFull.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "refused: -Out is inside the KAIROS repository; the Cockpit output is never committed"
}
$relaykit = if ($env:RELAYKIT) { $env:RELAYKIT -split ' ' } else { @("relay-kit") }
$exe, $pre = $relaykit[0], @($relaykit | Select-Object -Skip 1)
if (-not $NoFetch) {
  $repoArgs = @()
  foreach ($r in Get-Content (Join-Path $here "repos.txt")) {
    if ($r -and -not $r.StartsWith("#")) { $repoArgs += @("--repo", $r.Trim()) }
  }
  & $exe @pre prs --root $env:RECORDS @repoArgs
  if ($LASTEXITCODE -ne 0) { Write-Warning "some repositories failed; see the fetch line in pr-state.jsonl" }
}
$parent = Split-Path $outFull -Parent
New-Item -ItemType Directory -Force -Path $parent | Out-Null
$theme = Join-Path $parent "theme-$Mark.json"
python (Join-Path $here "theme_from_tokens.py") --tokens (Join-Path $env:RECORDS "kairos\design\tokens-v0.1-proposed.json") --mark $Mark --out $theme
if ($LASTEXITCODE -ne 0) { throw "theme generation failed" }
& $exe @pre cockpit --root $env:RECORDS --out $outFull --brand Kairos --theme $theme --landing prs
if ($LASTEXITCODE -ne 0) { throw "cockpit build failed" }
Write-Host "open $outFull\index.html"
