# GAMBIT report mobile layout

Report pages share `assets/gambit-responsive.css`. It moves side navigation above
the report below 720 CSS pixels, keeps cards inside the content column, and
scrolls wide tables and preformatted text within their own containers.
Existing NFL `board-chrome` pages retain their mobile player-card layout.

After generating or regenerating HTML, run from this repository:

```sh
python3 tools/apply_mobile_layout.py
python3 tools/apply_mobile_layout.py --check
```

The first command adds relative stylesheet links and accessible table wrappers
only where needed. It leaves authored text, data, images, and scripts intact;
repeated runs make no additional changes. The second command exits nonzero if
generated pages still need the layout pass. Keep both steps in the active local
publisher before its existing validation and GitHub Pages publication steps.

This repository contains published HTML, not the active Mac generator. The
helper is available here; installing it into that local generator is a separate
integration step. Do not replace the active local pipeline with an old baseline.

For layout QA, check 320px and 390px phone widths plus desktop, including every
radio-selected report view, searches, sorting, theme controls, and menu toggles.
Horizontal scrolling should belong to wide tables/charts, not the entire page.
The fixed-size image rendering template in `tools/cursor_pick_card` is excluded.
