#!/bin/sh
# Claude Code Stop hook for an application repo. Exit 2 sends the agent back.
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd) || exit 2
if command -v python3 >/dev/null 2>&1; then
  py=python3
elif command -v python >/dev/null 2>&1; then
  py=python
else
  echo "Install Python 3. The Stop hook cannot finish a session without scripts/verify.py." >&2
  exit 2
fi
exec "$py" "$root/scripts/verify.py" "$root"
