# GAMBIT navigation policy

The wide GAMBIT HOME image banner at the top of a page is the canonical link to `hub.html`.

Whenever a page includes that working `.gambit-home` banner link, omit any redundant sidebar `.pill.home` element that also points to `hub.html`. This applies even if the extra pill text says `Main Prop Page` rather than `Home`.

Keep the banner, Back, Card Build, ETR Value, Open Checks, and all links to distinct destinations. On a page without that banner, keep its Home navigation.

**Important for Cursor publishing:** enforce this rule inside the HTML templates and page generators before publishing every new slate; do not reintroduce duplicate Home pills on subsequent renders. Check the published artifact with `python3 tools/check_gambit_home_nav.py`.
