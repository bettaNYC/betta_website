#!/bin/zsh
# Weekly wrapper for the Strava → website sync (called by launchd).
# Regenerates training-data.js from the latest export and pushes if it changed.
# Run it by hand any time with:  ./run-sport-update.sh

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"
REPO="/Users/elisabettarappo/Projects/betta_website"
PY="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

cd "$REPO" || exit 1
echo "──────── $(date '+%Y-%m-%d %H:%M:%S') ────────"
"$PY" "$REPO/update-sport-data.py" --commit
echo "exit: $?"
