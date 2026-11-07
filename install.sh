#!/bin/sh
# Kairos Dev Kit, macOS and Linux. Run from this folder:  sh install.sh
# Needs no admin rights (no sudo). Downloads nothing itself: kairos.py (next to this file) clones the repos.
here=$(cd "$(dirname "$0")" && pwd)
py=$(command -v python3 || command -v python) || { echo "Python is not installed. Install Python 3.10+ from python.org or your package manager, then run this again."; exit 1; }
[ -f "$here/kairos.py" ] || { echo "kairos.py is not next to this script. Put both in the same folder."; exit 1; }
echo "Using $py"
"$py" "$here/kairos.py" install || { echo "Something failed. Run:  $py kairos.py check   and send the output."; exit 1; }
echo "Done. Next:  $py kairos.py next"
