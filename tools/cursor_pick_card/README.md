# Cursor pick card PNG renderer

Deterministic HTML → PNG for hub lineup tables. Uses the local venv (Playwright + Chromium). **Does not** use AI image generation; rows must come from engine JSON or parsed HTML tables.

## Setup (once per Mac)

```sh
python3 -m venv tools/.venv-card-render
tools/.venv-card-render/bin/pip install playwright
tools/.venv-card-render/bin/playwright install chromium
```

## Render

```sh
tools/.venv-card-render/bin/python tools/cursor_pick_card/render.py \
  --json tools/cursor_pick_card/examples/fau_unt_choice1.json \
  --out assets/cursor-picks/2026-10-29_FAU_UNT-cursor-choice1.png
```

Options:

- `--json PATH` — lineup payload (see `schema.json`)
- `--html PATH` — parse first six-row lineup table from a hub Showdown page
- `--choice N` — with `--html`, pick the Nth Choice block (1-based)
- `--out PATH` — PNG output (creates parent dirs)

Embed on hub pages under **Cursor picks** (separate from **ChatGPT picks** images).
