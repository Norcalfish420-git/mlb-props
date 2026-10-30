#!/usr/bin/env python3
"""Apply shared responsive styles to generated reports without rewriting content.

Run after generating site HTML and before publishing. --check reports drift.
The card-rendering template under tools/ is deliberately excluded.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import json
import re

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SCROLL = {'table-scroll', 'gambit-table-scroll', 'season-log-wrap', 'scroll'}

class LayoutParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        for match in re.finditer('\n', source): self.lines.append(match.end())
        self.stack = []
        self.tables = []
        self.rail = False
        self.feed(source)

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        classes = set((attr.get('class') or '').split())
        self.rail |= 'rail' in classes
        start = self.position()
        wrap = tag == 'table' and not any(t == 'table' or c & SCROLL or 'bat-card' in c for t, c, _, _ in self.stack)
        if tag not in VOID: self.stack.append((tag, classes, start, wrap))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, _, start, wrap = self.stack[i]
                if wrap:
                    end = self.source.index('>', self.position()) + 1
                    self.tables.append((start, end))
                del self.stack[i:]
                break

def transform(source, relative_path):
    parser = LayoutParser(source)
    # New board-chrome NFL reports already render mobile player cards.
    if 'id="board-chrome"' in source: return source
    needs_styles = parser.rail or bool(parser.tables)
    if not needs_styles: return source
    out = source
    for start, end in sorted(parser.tables, reverse=True):
        out = out[:start] + '<div class="gambit-table-scroll" role="region" aria-label="Scrollable data table" tabindex="0">' + out[start:end] + '</div>' + out[end:]
    if 'data-gambit-responsive="1"' not in out:
        prefix = '../' * (len(relative_path.parts) - 1)
        link = '<link rel="stylesheet" data-gambit-responsive="1" href="' + prefix + 'assets/gambit-responsive.css?v=20261030"/>\n'
        if '</head>' not in out: raise ValueError(f'No head closing tag: {relative_path}')
        out = out.replace('</head>', link + '</head>', 1)
    return out

def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args.add_argument('--check', action='store_true')
    opts = args.parse_args()
    changed = []
    pages = 0
    for path in sorted(opts.root.rglob('*.html')):
        rel = path.relative_to(opts.root)
        if any(p.startswith('.') for p in rel.parts) or rel.parts[0] in {'tools', 'node_modules'}: continue
        pages += 1
        before = path.read_text()
        after = transform(before, rel)
        if after != before:
            changed.append(str(rel))
            if not opts.check: path.write_text(after)
    print(json.dumps({'pages_checked': pages, 'changed': len(changed), 'paths': changed}))
    return 1 if opts.check and changed else 0

if __name__ == '__main__': raise SystemExit(main())
