#!/usr/bin/env python3
"""QC for duplicate Home navigation in published GAMBIT HTML pages."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent.parent
banner = re.compile(r'<a[^>]*class=["\'][^"\']*\bgambit-home\b[^"\']*["\'][^>]*href=["\'][^"\']*hub\.html["\']', re.I)
pill = re.compile(r'<a[^>]*class=["\'][^"\']*\bpill\s+home\b[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)
href = re.compile(r'href=["\']([^"\']+)["\']', re.I)
bad = []
for page in root.rglob('*.html'):
    source = page.read_text(encoding='utf-8', errors='replace')
    if not banner.search(source):
        continue
    for match in pill.finditer(source):
        link = href.search(match.group())
        if link and re.search(r'(?:^|/)hub\.html(?:[?#].*)?$', link.group(1), re.I):
            bad.append(str(page.relative_to(root)))
            break
if bad:
    print('Duplicate Hub home pills:', *bad, sep='\n  ')
    sys.exit(1)
print('PASS: GAMBIT HOME banner is the sole duplicate-free Hub link')
