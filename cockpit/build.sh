#!/usr/bin/env bash
# Build the Kairos Cockpit: read PR state into the records, then render the page with the Kairos theme.
#
#   RECORDS=~/src/relay-kit-private ./build.sh [--mark amber|blue] [--out DIR] [--no-fetch]
#
# Needs relay-kit (pip install, or RELAYKIT="python3 /path/to/relay-kit/tools/cli.py") and, unless
# --no-fetch, the gh CLI signed in (or GITHUB_TOKEN). Writes:
#   - RECORDS/governance/pr-state.jsonl  (appended by relay-kit prs; commit it to the records or not)
#   - OUT/index.html, OUT/cockpit.json    (default ~/.kairos/cockpit; never inside this repository)
#   - OUT/../theme-<mark>.json            (generated from the records' design tokens)
# Nothing is written to this repository and nothing is published.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARK=amber OUT="${OUT:-$HOME/.kairos/cockpit}" FETCH=1
while [ $# -gt 0 ]; do
  case "$1" in
    --mark) MARK="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --no-fetch) FETCH=0; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
: "${RECORDS:?set RECORDS to your local clone of the private records}"
RELAYKIT="${RELAYKIT:-relay-kit}"
TOKENS="$RECORDS/kairos/design/tokens-v0.1-proposed.json"
# Resolve OUT to an absolute physical path (symlinks followed) before anything is written, and refuse it,
# or the folder the theme goes in, inside this repository.
phys() {
  local p="$1" rest=""
  case "$p" in /*) ;; *) p="$PWD/$p" ;; esac
  while [ ! -e "$p" ]; do rest="/$(basename "$p")$rest"; p="$(dirname "$p")"; done
  printf '%s%s\n' "$(cd -P "$p" && pwd -P)" "$rest"
}
REPO="$(cd -P "$HERE/.." && pwd -P)"
OUT="$(phys "$OUT")"
for d in "$OUT" "$(dirname "$OUT")"; do
  case "$d/" in "$REPO/"*) echo "refused: $d is inside the KAIROS repository; the Cockpit output is never committed" >&2; exit 2 ;; esac
done
if [ "$FETCH" = 1 ]; then
  args=()
  while IFS= read -r r || [ -n "$r" ]; do
    r="${r%$'\r'}"; r="${r%%#*}"; r="$(printf '%s' "$r" | tr -d '[:space:]')"
    [ -n "$r" ] && args+=(--repo "$r")
  done < "$HERE/repos.txt"
  [ "${#args[@]}" -gt 0 ] || { echo "refused: no repositories in repos.txt" >&2; exit 2; }
  $RELAYKIT prs --root "$RECORDS" "${args[@]}" || echo "note: some repositories failed; see the fetch line in pr-state.jsonl" >&2
fi
THEME="$(dirname "$OUT")/theme-$MARK.json"
mkdir -p "$(dirname "$OUT")"
python3 "$HERE/theme_from_tokens.py" --tokens "$TOKENS" --mark "$MARK" --out "$THEME"
$RELAYKIT cockpit --root "$RECORDS" --out "$OUT" --brand Kairos --theme "$THEME" --landing prs
echo "open $OUT/index.html"
