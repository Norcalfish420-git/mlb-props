#!/bin/sh
# Render Cursor lineup table → PNG (uses tools/.venv-card-render).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/tools/.venv-card-render/bin/python"
exec "$PY" "$ROOT/tools/cursor_pick_card/render.py" "$@"
