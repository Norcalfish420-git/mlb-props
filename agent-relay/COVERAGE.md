# Audit coverage

Generated 2026-10-20T15:13:46Z by `sports-rig:scripts/rig_relay_coverage.py`. Relay head: `cab25d7`. Do not edit by hand.

A verdict comes only from ChatGPT replies recorded from desk-handoff PR #1 with their comment
id and payload hash. Cursor test counts are shown for context and never set the verdict.

| Tool | Verdict | Current SHAs | Last confirmed by ChatGPT | Scope | Reviews | Open (C/H/M/L/I) | Accepted risk | Cursor tests |
|---|---|---|---|---|---|---|---|---|
| NFL props board (one prop per player, RC6 research gate, T-60 recheck) | NOT_REVIEWED | NFL-Player-Prop-Tool@a7d1bfd, sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| NFL double-up Showdown (v1.6 engine, ranked handoff, NFL_CASH_CORE_FIRST/1.0, real_engine wrapper) | REVIEW_PENDING | NFL-Player-Prop-Tool@5d41ae4, sports-rig@3a9c0ae | never | - | REV-20261020-007 | 0/0/0/0/0 | 0 | 3 run, 3 failed |
| CFB Showdown bundle intake and preview (ChatGPT picks; Cursor validates structure only) | NOT_REVIEWED | CFB-Player-Prop-Tool@fcdcac3 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| CFB props desk | NOT_REVIEWED | CFB-Player-Prop-Tool@fcdcac3 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Horse desk (check_horses, entries pages, eligibility screen) | NOT_REVIEWED | horse-desk@85bf764 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Pre-publish QC gate and leak scan (rig_qc.run_qc / assert_publishable) | REVIEW_PENDING | sports-rig@3a9c0ae | never | - | REV-20261020-007 | 0/0/0/0/0 | 0 | 3 run, 3 failed |
| Ledgers A-H index, decision record, source registry, rules view | NOT_REVIEWED | sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Research skeleton, facts, lessons, headless author and challenger | NOT_REVIEWED | sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Hub publisher and site pages | NOT_REVIEWED | NFL-Player-Prop-Tool@8e51f24 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| desk-handoff bridge relay (ChatGPT-owned transport; Cursor runs a pinned copy) | NOT_REVIEWED | desk-handoff@a67fb46 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| This audit bridge (agent-relay protocol, review tool, coverage generator) | STALE_SINCE_REVIEW | mlb-props@cab25d7, sports-rig@7ad9566 | mlb-props@74afc07, sports-rig@7ad9566 | CODE/COMPLETE | REV-20261020-001, REV-20261020-002, REV-20261020-003, REV-20261020-004, REV-20261020-005, REV-20261020-006 | 0/0/0/0/0 | 0 | 2 run, 0 failed |

Verdicts: NOT_REVIEWED, REVIEW_PENDING, REVIEWED_OPEN_FINDINGS, REVIEWED_ACCEPTED_RISK, REVIEWED_SCOPE_LIMITED, STALE_SINCE_REVIEW, REVIEWED_CLEAN_AT_SHA.
