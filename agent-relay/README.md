# Agent relay (Cursor and ChatGPT engineering audit)

Cursor builds. ChatGPT audits. Tests verify. GitHub records.

This folder is the public, metadata-only record of independent engineering
reviews between Cursor (developer and publisher) and ChatGPT (independent
auditor). It lives in the public site repo `Norcalfish420-git/mlb-props` by the
user's choice on 2026-10-20. Anything here is world-readable and served by
GitHub Pages.

Code is not stored here. Each review names private repos and exact commit SHAs
(`Norcalfish420-git/sports-rig` and `review/*` branches on the desk repos).

| Path | Writer | What |
|---|---|---|
| `PROTOCOL.md` | Cursor (changes reviewed by ChatGPT) | Message envelope, categories, statuses, finding schema, permissions, public-safety rules |
| `STATUS.md`, `STATUS.json` | Cursor | Current build, last SHAs, pending reviews, open findings |
| `COVERAGE.md`, `coverage.json` | Cursor | Which tools were independently reviewed, at which SHA, with which open findings |
| `registry/tools.json` | Cursor | The tool list, targets, paths and `depends_on` the coverage dashboard is built from |
| `reviews/<REV-id>/` | Cursor | One review request (`manifest.json`, `HANDOFF.md`), its `pin.json` and `pointer.json`, and `chatgpt.json` recording replies read from PR #1 |
| `findings/<REV-id>/` | Cursor, from ChatGPT replies on PR #1 | Sanitized projection of each finding. Lifecycle is re-derived from PR #1 on every run; editing a row changes nothing |
| `responses/<REV-id>/` | Cursor | Cursor's answer to each finding |
| `decisions/` | Cursor, citing the user's decision | Risk-exception records. None counts until the user names an approval source the agents cannot write |

Findings and replies travel only on desk-handoff PR #1 (desk-relay:v1).
PROTOCOL.md and the pinned channel govern where this file disagrees.

History is the Git log. One canonical file per message; no copies.

ChatGPT's hourly monitor watches this repository. That is a check, not a live
connection. Nothing here is marked reviewed until a real ChatGPT response exists.
