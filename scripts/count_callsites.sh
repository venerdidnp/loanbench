#!/usr/bin/env bash
# Default scope is production + tests, not the repository or bin worktrees.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-python3}"
exec "$PY" "$ROOT/scripts/count_callsites.py" "$@"
