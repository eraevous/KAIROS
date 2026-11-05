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
case "$(cd "$OUT" 2>/dev/null && pwd || echo "$OUT")" in
  "$(cd "$HERE/.." && pwd)"*) echo "refused: --out is inside the KAIROS repository; the Cockpit output is never committed" >&2; exit 2 ;;
esac
if [ "$FETCH" = 1 ]; then
  args=()
  while read -r r; do case "$r" in ''|\#*) ;; *) args+=(--repo "$r") ;; esac; done < "$HERE/repos.txt"
  $RELAYKIT prs --root "$RECORDS" "${args[@]}" || echo "note: some repositories failed; see the fetch line in pr-state.jsonl" >&2
fi
THEME="$(dirname "$OUT")/theme-$MARK.json"
mkdir -p "$(dirname "$OUT")"
python3 "$HERE/theme_from_tokens.py" --tokens "$TOKENS" --mark "$MARK" --out "$THEME"
$RELAYKIT cockpit --root "$RECORDS" --out "$OUT" --brand Kairos --theme "$THEME" --landing prs
echo "open $OUT/index.html"
