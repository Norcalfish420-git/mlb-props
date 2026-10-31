#!/usr/bin/env python3
"""Unit tests for sync_gpt_pick_images (no network, no git)."""
from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

import sync_gpt_pick_images as sync


MINI_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02"
    b"\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
    b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


class SyncGptPickImagesTests(unittest.TestCase):
    def test_refuse_horses(self):
        with self.assertRaises(SystemExit):
            sync.ensure_not_horses(Path("horses/2026-10-31.html"))

    def test_inject_card_build_idempotent(self):
        html = (
            "<html><head><style>body{color:red;}</style></head><body>"
            '<div class="card-build"><h2>Card Build</h2>'
            "<h3>Choice #1 · Recommended</h3><p>x</p></div></body></html>"
        )
        html = sync.ensure_css(html)
        section = (
            '<section class="gpt-picks-block" data-primary-key="K" data-sha256="'
            + ("a" * 64)
            + '"><h3>ChatGPT picks</h3>'
            '<h4 class="cursor-choice">Choice #1</h4>'
            '<figure class="gpt-pick-image"><img src="../assets/gpt-picks/x.png" alt="a"/></figure>'
            "</section>"
            '<h3 class="cursor-picks-title">Cursor picks</h3>'
        )
        once = sync.inject_showdown_card_build(html, section)
        twice = sync.inject_showdown_card_build(once, section)
        self.assertEqual(once.count('<section class="gpt-picks-block"'), 1)
        self.assertEqual(twice.count('<section class="gpt-picks-block"'), 1)
        self.assertEqual(twice.count('<h3 class="cursor-picks-title">Cursor picks</h3>'), 1)
        self.assertIn("Choice #1 · Recommended", twice)
        self.assertLess(twice.index("ChatGPT picks"), twice.index("Cursor picks"))
        self.assertLess(twice.index("Cursor picks"), twice.index("Choice #1 · Recommended"))

    def test_zip_parse_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "site"
            showdown = root / "showdown"
            showdown.mkdir(parents=True)
            assets = root / "assets" / "gpt-picks"
            assets.mkdir(parents=True)
            (root / "handoffs").mkdir()
            page = showdown / "2026-10-31_UF_UGA.html"
            page.write_text(
                "<!DOCTYPE html><html><head><title>CFB Showdown 2026-10-31 · Florida @ Georgia"
                "</title><style>body{}</style></head><body>"
                '<div class="card-build"><h2>Card Build</h2>'
                "<h3>Choice #1 · Recommended</h3></div></body></html>",
                encoding="utf-8",
            )
            zpath = Path(tmp) / "pack.zip"
            with zipfile.ZipFile(zpath, "w") as zf:
                zf.writestr(
                    "PRIMARY_CFB_DK_SHOWDOWN_2026-10-31_UF-UGA.png", MINI_PNG
                )
                zf.writestr(
                    "CHOICE_2_CFB_DK_SHOWDOWN_2026-10-31_UF-UGA.png", MINI_PNG + b"\x00"
                )
                zf.writestr(
                    "CHOICE_3_CFB_DK_SHOWDOWN_2026-10-31_UF-UGA.png", MINI_PNG + b"\x01"
                )
                zf.writestr(
                    "CFB_Showdown_2026-10-31_UF_UGA_Choices_1-3.png", MINI_PNG
                )
            sync.ROOT = root
            sync.ASSETS = assets
            sync.RECEIPT = root / "handoffs" / "GPT_IMAGE_SYNC_RECEIPT.json"
            job = sync.job_from_zip(zpath, page=Path("showdown/2026-10-31_UF_UGA.html"), as_jpeg=False)
            self.assertEqual(len(job.choices), 3)
            result = sync.apply_job(job, force=True)
            self.assertIn(result["action"], {"added", "updated", "restored"})
            text = page.read_text(encoding="utf-8")
            self.assertIn("gpt-picks-block", text)
            self.assertIn("choice1-chatgpt.png", text)
            self.assertIn("choice2-chatgpt.png", text)
            self.assertIn("choice3-chatgpt.png", text)
            self.assertIn("Cursor picks", text)
            # Rebuild wipe simulation + reapply
            page.write_text(
                "<!DOCTYPE html><html><head><title>CFB Showdown 2026-10-31 · Florida @ Georgia"
                "</title><style>body{}</style></head><body>"
                '<div class="card-build"><h2>Card Build</h2>'
                "<h3>Choice #1 · Recommended</h3></div></body></html>",
                encoding="utf-8",
            )
            restored = sync.apply_after_rebuild(Path("showdown/2026-10-31_UF_UGA.html"))
            self.assertIsNotNone(restored)
            self.assertIn("gpt-picks-block", page.read_text(encoding="utf-8"))

    def test_classic_date_page_multi_choice_with_mirror(self):
        self.assertEqual(
            sync.parse_showdown_page(Path("classic/2026-10-31.html")),
            ("2026-10-31", "CFB_CLASSIC"),
        )
        self.assertIsNone(sync.parse_showdown_page(Path("nfl/2026-10-31.html")))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "classic").mkdir()
            html = (
                "<html><head><style>.gpt-picks-block{x}</style></head><body>"
                '<article class="panel-cards"><section class="gpt-picks-block" '
                'data-primary-key="OLD" data-sha256="' + ("b" * 64) + '"><h3>ChatGPT picks</h3>'
                "</section>\n<h3 class=\"cursor-picks-title\">Cursor picks</h3>\n<p>t</p></article>"
                "</body></html>"
            )
            for name in ("2026-10-31.html", "index.html"):
                (root / "classic" / name).write_text(html, encoding="utf-8")
            imgs = []
            for n in (1, 2):
                img = root / f"in{n}.png"
                img.write_bytes(MINI_PNG + bytes([n]))
                imgs.append(img)
            argv = ["--root", str(root), "--page", "classic/2026-10-31.html",
                    "--mirror", "classic/index.html"]
            self.assertEqual(sync.main(argv + ["--image", str(imgs[0])]), 0)
            for img in imgs:
                argv += ["--image", str(img)]
            self.assertEqual(sync.main(argv), 0)
            for name in ("2026-10-31.html", "index.html"):
                out = (root / "classic" / name).read_text(encoding="utf-8")
                self.assertIn('data-primary-key="CFB|DK|CLASSIC|2026-10-31|PRIMARY"', out)
                self.assertIn('<h4 class="cursor-choice">Choice #2</h4>', out)
                self.assertIn("2026-10-31_CFB_CLASSIC-choice2-chatgpt.png", out)
                self.assertIn("h4.cursor-choice{", out)
                self.assertEqual(out.count("gpt-picks-block\""), 1)
                self.assertEqual(out.count("Cursor picks"), 1)
                self.assertNotIn("OLD", out)
            import json
            receipt = json.loads((root / "handoffs" / "GPT_IMAGE_SYNC_RECEIPT.json").read_text())
            keys = {c["key"] for c in receipt["cards"]}
            self.assertIn("CFB|DK|CLASSIC|2026-10-31|CHOICE2", keys)


if __name__ == "__main__":
    unittest.main()
