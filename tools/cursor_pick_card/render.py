#!/usr/bin/env python3
"""Render a Cursor Showdown lineup JSON (or hub HTML table) to a PNG card."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template.html"


def _money(n: int | float) -> str:
    return f"${int(n):,}"


def _row_html(row: dict) -> str:
    slot = (row.get("slot") or "FLEX").strip()
    is_cpt = slot.lower().startswith("capt") or slot.upper() == "CPT"
    cls = "row cpt" if is_cpt else "row"
    slot_label = "CPT" if is_cpt else "FLEX"
    player = html.escape(str(row.get("player", "")))
    team = html.escape(str(row.get("team", "")))
    pos = html.escape(str(row.get("pos", "")))
    sal = _money(row.get("salary", 0))
    return (
        f'<div class="{cls}">'
        f'<div class="slot">{html.escape(slot_label)}</div>'
        f"<div><div class=\"name\">{player}</div>"
        f'<div class="meta">{team} · {pos}</div></div>'
        f'<div class="salary">{sal}</div></div>'
    )


def payload_to_html(data: dict) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    rows = "".join(_row_html(r) for r in data.get("rows") or [])
    total = data.get("total_spent")
    remaining = data.get("remaining")
    if total is None and data.get("rows"):
        total = sum(int(r.get("salary") or 0) for r in data["rows"])
    if remaining is None and total is not None:
        remaining = 50000 - int(total)
    replacements = {
        "{{BADGE}}": html.escape(data.get("badge") or "CURSOR LINEUP"),
        "{{TITLE}}": html.escape(data.get("title") or "Showdown lineup"),
        "{{SUBTITLE}}": html.escape(data.get("subtitle") or ""),
        "{{ROWS}}": rows,
        "{{TOTAL}}": _money(total or 0),
        "{{REMAINING}}": _money(remaining or 0),
        "{{FOOTER}}": html.escape(data.get("footer") or ""),
    }
    out = tpl
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def parse_choice_table(page_html: str, choice: int) -> dict:
    """Extract one Choice #N table from a CFB Showdown hub page."""
    choice = max(1, choice)
    pat = rf"<h3>Choice #{choice}[^<]*</h3>.*?<table[^>]*>.*?</table>"
    m = re.search(pat, page_html, flags=re.I | re.S)
    if not m:
        raise SystemExit(f"No Choice #{choice} table found in HTML")
    block = m.group(0)
    title_m = re.search(r"<title>([^<]+)</title>", page_html, re.I)
    title = title_m.group(1).strip() if title_m else "Showdown lineup"
    rows: list[dict] = []
    for tr in re.findall(r"<tr>(.*?)</tr>", block, flags=re.S)[1:]:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        if len(cells) < 5:
            continue
        clean = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        sal = re.sub(r"[^0-9]", "", clean[4])
        rows.append(
            {
                "slot": clean[0],
                "player": clean[1],
                "team": clean[2],
                "pos": clean[3],
                "salary": int(sal or 0),
            }
        )
    if not rows:
        raise SystemExit("Table had no data rows")
    spent = sum(r["salary"] for r in rows)
    return {
        "title": title.split("·")[-1].strip() if "·" in title else title,
        "subtitle": title,
        "badge": f"CURSOR · CHOICE #{choice}",
        "rows": rows,
        "total_spent": spent,
        "remaining": 50000 - spent,
        "footer": "Rendered from hub table · verify against HTML",
    }


def render_png(html_doc: str, out_path: Path, viewport_width: int = 720) -> None:
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": 900})
        page.set_content(html_doc, wait_until="networkidle")
        card = page.locator("#card")
        card.screenshot(path=str(out_path), type="png")
        browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", type=Path, help="Lineup JSON payload")
    ap.add_argument("--html", type=Path, help="Hub page HTML to parse")
    ap.add_argument("--choice", type=int, default=1, help="Choice index with --html")
    ap.add_argument("--out", type=Path, required=True, help="Output PNG path")
    args = ap.parse_args()

    if args.json:
        data = json.loads(args.json.read_text(encoding="utf-8"))
    elif args.html:
        data = parse_choice_table(args.html.read_text(encoding="utf-8"), args.choice)
    else:
        ap.error("Provide --json or --html")

    doc = payload_to_html(data)
    render_png(doc, args.out)
    print(json.dumps({"ok": True, "out": str(args.out), "rows": len(data.get("rows") or [])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
