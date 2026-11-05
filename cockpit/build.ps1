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
# Resolve a path to its real location: relative to PowerShell's current folder, with junctions and
# symlinks of the nearest existing parent followed.
function Resolve-Physical([string]$path) {
  $full = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
  $rest = ""
  $p = $full
  while (-not (Test-Path -LiteralPath $p)) {
    $rest = "\" + (Split-Path $p -Leaf) + $rest
    $p = Split-Path $p -Parent
  }
  $item = Get-Item -LiteralPath $p -Force
  $real = if ($item.LinkTarget) { $item.ResolvedTarget.FullName } else { $item.FullName }
  return ($real.TrimEnd("\") + $rest)
}
$repoRoot = (Resolve-Physical (Join-Path $here "..")).TrimEnd("\") + "\"
$outFull = Resolve-Physical $Out
foreach ($d in @($outFull, (Split-Path $outFull -Parent))) {
  if (($d.TrimEnd("\") + "\").StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "refused: $d is inside the KAIROS repository; the Cockpit output is never committed"
  }
}
$relaykit = if ($env:RELAYKIT) { $env:RELAYKIT -split ' ' } else { @("relay-kit") }
$exe, $pre = $relaykit[0], @($relaykit | Select-Object -Skip 1)
if (-not $NoFetch) {
  $repoArgs = @()
  foreach ($r in Get-Content (Join-Path $here "repos.txt")) {
    $r = ($r -replace "#.*$", "").Trim()
    if ($r) { $repoArgs += @("--repo", $r) }
  }
  if ($repoArgs.Count -eq 0) { throw "refused: no repositories in repos.txt" }
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
