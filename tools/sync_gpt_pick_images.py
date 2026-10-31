#!/usr/bin/env python3
"""Place ChatGPT pick images on hub pages the same way every time.

Usage examples:
  python3 tools/sync_gpt_pick_images.py \\
    --zip ~/Downloads/Florida_vs_Georgia_GAMBIT_Showdown_Images_2026-10-31.zip \\
    --page showdown/2026-10-31_UF_UGA.html

  python3 tools/sync_gpt_pick_images.py --reapply-missing
  python3 tools/sync_gpt_pick_images.py --check

Does not touch horses pages. Does not invent lineups. Asset bytes stay as
provided (PNG kept as PNG; JPEG kept as JPEG) unless --jpeg is set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gpt-picks"
RECEIPT = ROOT / "handoffs" / "GPT_IMAGE_SYNC_RECEIPT.json"
TZ = ZoneInfo("America/Chicago")

CSS_MARKER = ".gpt-picks-block{"
CSS_BLOCK = """\
.gpt-picks-block{margin:0 0 1.25rem;padding:0 0 1rem;border-bottom:1px solid var(--cell);}
.gpt-picks-block h3{display:block;width:max-content;max-width:100%;font-size:1.7rem;font-weight:800;letter-spacing:.04em;line-height:1.1;margin:0 0 .7rem;padding:0 0 .28rem;border-bottom:3px solid #c8c8c8;background:linear-gradient(180deg,#fff 8%,#d5d5d5 52%,#8f8f8f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;}
h3.cursor-picks-title{display:block;width:max-content;max-width:100%;font-size:1.7rem;font-weight:800;letter-spacing:.04em;line-height:1.1;margin:1.15rem 0 .7rem;padding:0 0 .28rem;border-bottom:3px solid #e6c35c;background:linear-gradient(180deg,#fff8d6 8%,#f0d56a 48%,#c49214 100%);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;}
html.light .gpt-picks-block h3{border-bottom-color:#5e5e5e;background:linear-gradient(180deg,#4a4a4a,#1f1f1f);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;}
html.light h3.cursor-picks-title{border-bottom-color:#8a6410;background:linear-gradient(180deg,#a67c12,#5c4308);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;}
.gpt-pick-image{margin:0 0 .85rem;}
.gpt-pick-image img{display:block;width:100%;height:auto;border-radius:.65rem;border:1px solid var(--cell);}
h4.cursor-choice{margin:.85rem 0 .45rem;font-size:1.05rem;font-weight:800;letter-spacing:.03em;}
"""
PRINT_CSS = (
    "  .gpt-picks-block h3,h3.cursor-picks-title{color:#111 !important;"
    "-webkit-text-fill-color:#111 !important;background:none !important;"
    "border-bottom-color:#111 !important;}"
)

HORSE_RE = re.compile(r"(^|/)horses(/|\.html)", re.I)
SHOWDOWN_STEM = re.compile(r"^(\d{4}-\d{2}-\d{2})_([A-Z0-9]+_[A-Z0-9]+)$")
DATE_STEM = re.compile(r"^(\d{4}-\d{2}-\d{2})$")
CLASSIC_SLUG = "CFB_CLASSIC"
CHOICE_CSS = "h4.cursor-choice{margin:.85rem 0 .45rem;font-size:1.05rem;font-weight:800;letter-spacing:.03em;}\n"
CHOICE_ASSET = re.compile(
    r"^(\d{4}-\d{2}-\d{2})_([A-Z0-9]+_[A-Z0-9]+)-choice(\d+)-chatgpt\.(jpe?g|png)$",
    re.I,
)
SINGLE_ASSET = re.compile(
    r"^(\d{4}-\d{2}-\d{2})_([A-Z0-9]+_[A-Z0-9]+)(?:-(showdown|props))?-chatgpt\.(jpe?g|png)$",
    re.I,
)
ZIP_PRIMARY = re.compile(
    r"^(?:PRIMARY_)?CFB_DK_SHOWDOWN_(\d{4}-\d{2}-\d{2})_([A-Za-z0-9]+)-([A-Za-z0-9]+)\.(png|jpe?g)$",
    re.I,
)
ZIP_CHOICE = re.compile(
    r"^CHOICE_(\d+)_CFB_DK_SHOWDOWN_(\d{4}-\d{2}-\d{2})_([A-Za-z0-9]+)-([A-Za-z0-9]+)\.(png|jpe?g)$",
    re.I,
)
COMPOSITE_RE = re.compile(r"Choices_1-3|Choices1-3|_all[-_]?choices", re.I)


@dataclass
class ChoiceImage:
    number: int
    path: Path
    sha256: str = ""
    asset_name: str = ""


@dataclass
class SyncJob:
    hub_page: Path  # relative to ROOT
    key: str
    choices: list[ChoiceImage] = field(default_factory=list)
    alt_label: str = ""
    placement: str = "Card Build tab, ChatGPT picks before Cursor picks"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def asset_rel(name: str) -> str:
    return f"assets/gpt-picks/{name}"


def img_src_for_page(page: Path, asset_name: str) -> str:
    depth = len(page.parts) - 1
    return ("../" * depth) + f"assets/gpt-picks/{asset_name}"


def ensure_not_horses(page: Path) -> None:
    rel = page.as_posix()
    if HORSE_RE.search(rel):
        raise SystemExit(f"refused: ChatGPT pick images are not placed on horse pages ({rel})")


def parse_showdown_page(page: Path) -> tuple[str, str] | None:
    m = SHOWDOWN_STEM.match(page.stem)
    if m:
        return m.group(1), m.group(2)
    m = DATE_STEM.match(page.stem)
    if m and page.parts[:1] == ("classic",):
        return m.group(1), CLASSIC_SLUG
    return None


def default_key(date: str, slug: str) -> str:
    if slug == CLASSIC_SLUG:
        return f"CFB|DK|CLASSIC|{date}|PRIMARY"
    return f"CFB|DK|SHOWDOWN|{date}|{slug}|PRIMARY"


def title_label(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def ensure_css(html: str) -> str:
    out = html
    if CSS_MARKER not in out:
        if "</style>" not in out:
            raise ValueError("page has no </style>; cannot inject GPT CSS")
        out = out.replace("</style>", CSS_BLOCK + "</style>", 1)
    if "h4.cursor-choice{" not in out and "</style>" in out:
        out = out.replace("</style>", CHOICE_CSS + "</style>", 1)
    if PRINT_CSS not in out and "@media print" in out:
        out = re.sub(
            r"(@media print\{)",
            r"\1\n" + PRINT_CSS + "\n",
            out,
            count=1,
        )
    return out


def build_section(job: SyncJob, page: Path) -> str:
    if not job.choices:
        raise ValueError("no choice images")
    primary = next((c for c in job.choices if c.number == 1), job.choices[0])
    parts = [
        f'<section class="gpt-picks-block" data-primary-key="{job.key}" '
        f'data-sha256="{primary.sha256}"><h3>ChatGPT picks</h3>'
    ]
    multi = len(job.choices) > 1
    for choice in sorted(job.choices, key=lambda c: c.number):
        if multi:
            parts.append(f'<h4 class="cursor-choice">Choice #{choice.number}</h4>')
        alt = job.alt_label or title_label("")
        if not alt:
            alt = f"ChatGPT Choice #{choice.number}"
        else:
            alt = f"ChatGPT Choice #{choice.number} — {alt}"
        src = img_src_for_page(page, choice.asset_name)
        parts.append(
            f'<figure class="gpt-pick-image"><img src="{src}" alt="{_esc(alt)}"/></figure>'
        )
    parts.append("</section>")
    parts.append('<h3 class="cursor-picks-title">Cursor picks</h3>')
    return "".join(parts)


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def strip_existing_gpt_block(html: str) -> str:
    """Remove prior ChatGPT picks section and a following Cursor picks title."""
    out = re.sub(
        r'<section class="gpt-picks-block"[^>]*>.*?</section>\s*'
        r'(?:<h3 class="cursor-picks-title">Cursor picks</h3>\s*)?',
        "",
        html,
        count=1,
        flags=re.S,
    )
    # Legacy single figure without section wrapper.
    out = re.sub(
        r'<figure class="gpt-pick-image"[^>]*>.*?</figure>\s*',
        "",
        out,
        count=1,
        flags=re.S,
    )
    return out


def inject_showdown_card_build(html: str, section: str) -> str:
    html = strip_existing_gpt_block(html)
    # After Card Build heading + optional sub blurb.
    pattern = re.compile(
        r'(<div class="card-build"><h2>Card Build</h2>)'
        r'(?:<p class="sub">.*?</p>)?',
        re.S,
    )
    m = pattern.search(html)
    if not m:
        raise ValueError("Card Build anchor not found")
    return html[: m.end()] + section + html[m.end() :]


def inject_top_props(html: str, section: str) -> str:
    html = strip_existing_gpt_block(html)
    for needle in (
        "<h3>TOP PROPS — week board</h3>",
        "<h3>THE PACK</h3>",
        "<h2>Cards</h2>",
        '<article class="panel-cards">',
    ):
        if needle in html:
            return html.replace(needle, needle + section, 1)
    raise ValueError("TOP PROPS / THE PACK / Cards anchor not found")


def page_embedded_sha(html: str) -> str | None:
    m = re.search(
        r'<section class="gpt-picks-block"[^>]*data-sha256="([0-9a-f]{64})"',
        html,
        re.I,
    )
    return m.group(1).lower() if m else None


def convert_to_jpeg(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in {".jpg", ".jpeg"} and src.resolve() != dest.resolve():
        shutil.copy2(src, dest)
        return
    if src.suffix.lower() in {".jpg", ".jpeg"} and src.resolve() == dest.resolve():
        return
    cmd = ["sips", "-s", "format", "jpeg", str(src), "--out", str(dest)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not dest.is_file():
        raise SystemExit(f"sips jpeg convert failed for {src}: {proc.stderr or proc.stdout}")


def stage_choice(
    src: Path,
    asset_name: str,
    *,
    as_jpeg: bool,
) -> ChoiceImage:
    ASSETS.mkdir(parents=True, exist_ok=True)
    dest = ASSETS / asset_name
    if as_jpeg and not asset_name.lower().endswith((".jpg", ".jpeg")):
        raise ValueError(f"jpeg staging requires .jpg name, got {asset_name}")
    if as_jpeg:
        convert_to_jpeg(src, dest)
    else:
        if src.resolve() != dest.resolve():
            shutil.copy2(src, dest)
    digest = sha256_file(dest)
    number = 1
    m = CHOICE_ASSET.match(asset_name)
    if m:
        number = int(m.group(3))
    return ChoiceImage(number=number, path=dest, sha256=digest, asset_name=asset_name)


def discover_zip_choices(zip_path: Path, extract_dir: Path) -> tuple[str, str, list[Path]]:
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)
    files = [p for p in extract_dir.rglob("*") if p.is_file() and not p.name.startswith(".")]
    date = slug = None
    by_num: dict[int, Path] = {}
    for path in files:
        name = path.name
        if COMPOSITE_RE.search(name):
            continue
        m = ZIP_CHOICE.match(name)
        if m:
            num = int(m.group(1))
            date, a, b = m.group(2), m.group(3).upper(), m.group(4).upper()
            slug = f"{a}_{b}"
            by_num[num] = path
            continue
        m = ZIP_PRIMARY.match(name)
        if m:
            date, a, b = m.group(1), m.group(2).upper(), m.group(3).upper()
            slug = f"{a}_{b}"
            by_num[1] = path
            continue
        # Alternate: PRIMARY_... already matched; also accept UF_UGA in filename.
        m2 = re.search(
            r"(PRIMARY|CHOICE[_-]?(\d+)).*?(\d{4}-\d{2}-\d{2}).*?([A-Za-z0-9]+)[_-]([A-Za-z0-9]+)",
            name,
            re.I,
        )
        if m2 and name.lower().endswith((".png", ".jpg", ".jpeg")):
            date = m2.group(3)
            slug = f"{m2.group(4).upper()}_{m2.group(5).upper()}"
            num = 1 if m2.group(1).upper().startswith("PRIMARY") else int(m2.group(2))
            by_num[num] = path
    if not date or not slug or not by_num:
        raise SystemExit(
            f"could not parse CFB Showdown choice images from zip {zip_path.name}; "
            f"files={sorted(p.name for p in files)}"
        )
    return date, slug, [by_num[n] for n in sorted(by_num)]


def job_from_zip(
    zip_path: Path,
    *,
    page: Path | None,
    as_jpeg: bool,
) -> SyncJob:
    with tempfile.TemporaryDirectory(prefix="gpt-picks-") as tmp:
        date, slug, paths = discover_zip_choices(zip_path, Path(tmp))
        hub = page or Path(f"showdown/{date}_{slug}.html")
        ensure_not_horses(hub)
        full = ROOT / hub
        if not full.is_file():
            raise SystemExit(f"hub page missing: {hub}")
        html = full.read_text(encoding="utf-8")
        label = title_label(html)
        # Drop date/prefix noise for alt text.
        label = re.sub(r"^CFB Showdown\s+\d{4}-\d{2}-\d{2}\s*[·\-]\s*", "", label).strip()
        choices: list[ChoiceImage] = []
        # Map extracted paths by sorted order → choice numbers from names when possible.
        numbered: list[tuple[int, Path]] = []
        for path in paths:
            m = ZIP_CHOICE.match(path.name)
            if m:
                numbered.append((int(m.group(1)), path))
            elif ZIP_PRIMARY.match(path.name) or path.name.upper().startswith("PRIMARY"):
                numbered.append((1, path))
            else:
                numbered.append((len(numbered) + 1, path))
        numbered.sort(key=lambda t: t[0])
        for num, src in numbered:
            ext = "jpg" if as_jpeg else src.suffix.lower().lstrip(".")
            if ext == "jpeg":
                ext = "jpg"
            asset_name = f"{date}_{slug}-choice{num}-chatgpt.{ext}"
            # Copy out of temp before TemporaryDirectory deletes it.
            stable = Path(tempfile.gettempdir()) / f"gpt-stage-{asset_name}"
            shutil.copy2(src, stable)
            choices.append(stage_choice(stable, asset_name, as_jpeg=as_jpeg))
            try:
                stable.unlink()
            except OSError:
                pass
        key = f"CFB|DK|SHOWDOWN|{date}|{slug}|PRIMARY"
        return SyncJob(
            hub_page=hub,
            key=key,
            choices=choices,
            alt_label=label or f"{slug.replace('_', ' at ')}, {date}",
        )


def _prefer_ext(existing: Path | None, candidate: Path) -> Path:
    """Prefer PNG over JPEG when both encodings exist for the same slot."""
    if existing is None:
        return candidate
    if candidate.suffix.lower() == ".png" and existing.suffix.lower() != ".png":
        return candidate
    return existing


def jobs_from_existing_assets(page: Path) -> SyncJob | None:
    ensure_not_horses(page)
    parsed = parse_showdown_page(page)
    if not parsed:
        return None
    date, slug = parsed
    by_num: dict[int, Path] = {}
    for path in sorted(ASSETS.glob(f"{date}_{slug}-choice*-chatgpt.*")):
        m = CHOICE_ASSET.match(path.name)
        if not m:
            continue
        num = int(m.group(3))
        by_num[num] = _prefer_ext(by_num.get(num), path)
    found: list[ChoiceImage] = []
    for num in sorted(by_num):
        path = by_num[num]
        found.append(
            ChoiceImage(
                number=num,
                path=path,
                sha256=sha256_file(path),
                asset_name=path.name,
            )
        )
    if not found:
        single = None
        for path in sorted(ASSETS.glob(f"{date}_{slug}*chatgpt.*")):
            if CHOICE_ASSET.match(path.name):
                continue
            if SINGLE_ASSET.match(path.name) or path.name.startswith(f"{date}_{slug}"):
                single = _prefer_ext(single, path)
        if single:
            found = [
                ChoiceImage(
                    number=1,
                    path=single,
                    sha256=sha256_file(single),
                    asset_name=single.name,
                )
            ]
    if not found:
        return None
    html = (ROOT / page).read_text(encoding="utf-8")
    label = title_label(html)
    label = re.sub(r"^CFB Showdown\s+\d{4}-\d{2}-\d{2}\s*[·\-]\s*", "", label).strip()
    return SyncJob(
        hub_page=page,
        key=default_key(date, slug),
        choices=found,
        alt_label=label or f"{slug.replace('_', ' at ')}, {date}",
    )


def apply_job(job: SyncJob, *, force: bool = False) -> dict:
    ensure_not_horses(job.hub_page)
    path = ROOT / job.hub_page
    if not path.is_file():
        raise SystemExit(f"hub page missing: {job.hub_page}")
    before = path.read_text(encoding="utf-8")
    primary = next((c for c in job.choices if c.number == 1), job.choices[0])
    embedded = page_embedded_sha(before)
    all_on_page = all(
        img_src_for_page(job.hub_page, c.asset_name) in before for c in job.choices
    )
    if embedded and embedded == primary.sha256 and 'class="gpt-picks-block"' in before and all_on_page:
        return {
            "key": job.key,
            "hub_page": job.hub_page.as_posix(),
            "asset": asset_rel(primary.asset_name),
            "sha256": primary.sha256,
            "action": "unchanged",
            "placement": job.placement,
        }
    if embedded and embedded != primary.sha256 and not force:
        # Newer replace is allowed when caller passes force (user-supplied zip/images).
        # Without force, refuse only when reapply would overwrite a different live hash
        # with asset bytes that differ — still OK to restore missing block with same hash.
        if 'class="gpt-picks-block"' in before:
            raise SystemExit(
                f"refused: page {job.hub_page} has data-sha256={embedded[:12]}… but "
                f"incoming primary is {primary.sha256[:12]}…; pass --force to replace"
            )
    section = build_section(job, job.hub_page)
    html = ensure_css(before)
    lane = job.hub_page.parts[0] if job.hub_page.parts else ""
    if lane == "showdown" or "card-build" in html:
        html = inject_showdown_card_build(html, section)
    elif lane in {"nfl", "cfb", "classic"}:
        try:
            html = inject_top_props(html, section)
        except ValueError:
            html = inject_showdown_card_build(html, section)
    else:
        html = inject_showdown_card_build(html, section)
    path.write_text(html, encoding="utf-8")
    action = "updated" if embedded else "added"
    if 'class="gpt-picks-block"' not in before:
        action = "restored" if any(
            (ASSETS / c.asset_name).is_file() for c in job.choices
        ) and embedded is None else "added"
    cards = []
    for choice in sorted(job.choices, key=lambda c: c.number):
        variant = "PRIMARY" if choice.number == 1 else f"CHOICE{choice.number}"
        key = job.key.rsplit("|", 1)[0] + "|" + variant
        cards.append(
            {
                "key": key,
                "hub_page": job.hub_page.as_posix(),
                "asset": asset_rel(choice.asset_name),
                "sha256": choice.sha256,
                "action": action,
                "placement": job.placement,
            }
        )
    return {
        "key": job.key,
        "hub_page": job.hub_page.as_posix(),
        "asset": asset_rel(primary.asset_name),
        "sha256": primary.sha256,
        "action": action,
        "placement": job.placement,
        "cards": cards,
    }


def update_receipt(entries: list[dict], *, source: str, published: bool = False) -> None:
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    doc: dict
    if RECEIPT.is_file():
        try:
            doc = json.loads(RECEIPT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            doc = {}
    else:
        doc = {}
    cards = list(doc.get("cards") or [])
    by_key = {c.get("key"): i for i, c in enumerate(cards) if c.get("key")}
    flat: list[dict] = []
    for entry in entries:
        if entry.get("cards"):
            flat.extend(entry["cards"])
        else:
            flat.append({k: entry[k] for k in ("key", "hub_page", "asset", "sha256", "action", "placement") if k in entry})
    for card in flat:
        key = card.get("key")
        if key in by_key:
            cards[by_key[key]] = card
        else:
            by_key[key] = len(cards)
            cards.append(card)
    now = datetime.now(TZ).isoformat(timespec="seconds")
    primary = flat[0] if flat else {}
    doc.update(
        {
            "checked_at": now,
            "source": source,
            "cards": cards,
            "published": published,
            "hub_page": primary.get("hub_page"),
            "asset": primary.get("asset"),
            "sha256": primary.get("sha256"),
            "tool": "tools/sync_gpt_pick_images.py",
        }
    )
    RECEIPT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def reapply_missing() -> list[dict]:
    results = []
    showdown = ROOT / "showdown"
    if not showdown.is_dir():
        return results
    for page in sorted(showdown.glob("*.html")):
        rel = page.relative_to(ROOT)
        html = page.read_text(encoding="utf-8")
        if 'class="gpt-picks-block"' in html:
            continue
        job = jobs_from_existing_assets(rel)
        if not job:
            continue
        results.append(apply_job(job, force=False))
    return results


def check_drift() -> int:
    """Return number of showdown pages that have assets but no gpt-picks-block."""
    bad = 0
    for page in sorted((ROOT / "showdown").glob("*.html")):
        rel = page.relative_to(ROOT)
        job = jobs_from_existing_assets(rel)
        if not job:
            continue
        html = page.read_text(encoding="utf-8")
        if 'class="gpt-picks-block"' not in html:
            print(f"MISSING_BLOCK {rel} assets={[c.asset_name for c in job.choices]}")
            bad += 1
            continue
        embedded = page_embedded_sha(html)
        primary = next((c for c in job.choices if c.number == 1), job.choices[0])
        if embedded != primary.sha256:
            print(f"HASH_DRIFT {rel} page={embedded} asset={primary.sha256}")
            bad += 1
    return bad


def apply_after_rebuild(page: Path) -> dict | None:
    """Hook for prospective_showdown_hub: restore GPT block if assets exist."""
    rel = page if not page.is_absolute() else page.relative_to(ROOT)
    job = jobs_from_existing_assets(rel)
    if not job:
        return None
    return apply_job(job, force=False)


def main(argv: list[str] | None = None) -> int:
    global ROOT, ASSETS, RECEIPT
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=None)
    p.add_argument("--zip", type=Path, help="ChatGPT Showdown image zip")
    p.add_argument("--page", type=Path, help="Hub page relative to site root")
    p.add_argument("--image", type=Path, action="append", default=[], help="One or more image files")
    p.add_argument("--choice", type=int, action="append", default=[], help="Choice numbers matching --image order")
    p.add_argument("--key", type=str, help="data-primary-key override")
    p.add_argument("--mirror", type=Path, action="append", default=[], help="Mirror page (e.g. classic/index.html) that gets the same block")
    p.add_argument("--jpeg", action="store_true", help="Convert staged assets to JPEG via sips")
    p.add_argument("--force", action="store_true", help="Replace a different on-page data-sha256")
    p.add_argument("--reapply-missing", action="store_true", help="Restore GPT blocks from existing assets")
    p.add_argument("--check", action="store_true", help="Report pages with assets but no GPT block")
    p.add_argument("--receipt-source", type=str, default="local_sync")
    opts = p.parse_args(argv)

    ROOT = (opts.root or Path(__file__).resolve().parents[1]).resolve()
    ASSETS = ROOT / "assets" / "gpt-picks"
    RECEIPT = ROOT / "handoffs" / "GPT_IMAGE_SYNC_RECEIPT.json"

    if opts.check:
        bad = check_drift()
        print(f"check_drift={bad}")
        return 1 if bad else 0

    results: list[dict] = []
    if opts.reapply_missing:
        results.extend(reapply_missing())

    if opts.zip:
        job = job_from_zip(opts.zip, page=opts.page, as_jpeg=opts.jpeg)
        results.append(apply_job(job, force=True))  # user-supplied zip always replaces

    if opts.image:
        if not opts.page:
            raise SystemExit("--page is required with --image")
        page = opts.page
        ensure_not_horses(page)
        parsed = parse_showdown_page(page)
        if not parsed:
            raise SystemExit(f"cannot derive slate from page stem: {page}")
        date, slug = parsed
        nums = opts.choice or list(range(1, len(opts.image) + 1))
        if len(nums) != len(opts.image):
            raise SystemExit("--choice count must match --image count")
        choices = []
        for num, img in zip(nums, opts.image):
            ext = "jpg" if opts.jpeg else img.suffix.lower().lstrip(".")
            if ext == "jpeg":
                ext = "jpg"
            name = f"{date}_{slug}-choice{num}-chatgpt.{ext}"
            choices.append(stage_choice(img, name, as_jpeg=opts.jpeg))
        html = (ROOT / page).read_text(encoding="utf-8")
        label = title_label(html)
        label = re.sub(r"^CFB Showdown\s+\d{4}-\d{2}-\d{2}\s*[·\-]\s*", "", label).strip()
        key = opts.key or default_key(date, slug)
        job = SyncJob(hub_page=page, key=key, choices=choices, alt_label=label)
        result = apply_job(job, force=opts.force or True)
        for mirror in opts.mirror:
            ensure_not_horses(mirror)
            if mirror.parent != page.parent:
                raise SystemExit(f"--mirror must sit beside --page: {mirror}")
            apply_job(SyncJob(hub_page=mirror, key=key, choices=choices, alt_label=label), force=True)
            for card in [result, *result.get("cards", [])]:
                card["hub_page_mirror"] = mirror.as_posix()
        results.append(result)

    if not results and not opts.check:
        raise SystemExit("nothing to do; pass --zip, --image, --reapply-missing, or --check")

    if results:
        update_receipt(results, source=opts.receipt_source, published=False)
        for r in results:
            print(f"{r['action']} {r['hub_page']} sha256={r['sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
