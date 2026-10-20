# Audit coverage

Generated 2026-10-20T14:38:52Z by `sports-rig:scripts/rig_relay_coverage.py`. Relay head: `0d2a395`. Do not edit by hand.

A verdict comes only from ChatGPT replies recorded from desk-handoff PR #1 with their comment
id and payload hash. Cursor test counts are shown for context and never set the verdict.

| Tool | Verdict | Current SHAs | Last confirmed by ChatGPT | Scope | Reviews | Open (C/H/M/L/I) | Accepted risk | Cursor tests |
|---|---|---|---|---|---|---|---|---|
| NFL props board (one prop per player, RC6 research gate, T-60 recheck) | NOT_REVIEWED | NFL-Player-Prop-Tool@a7d1bfd, sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| NFL double-up Showdown (v1.6 engine, ranked handoff, NFL_CASH_CORE_FIRST/1.0, real_engine wrapper) | NOT_REVIEWED | NFL-Player-Prop-Tool@5d41ae4, sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| CFB Showdown bundle intake and preview (ChatGPT picks; Cursor validates structure only) | NOT_REVIEWED | CFB-Player-Prop-Tool@fcdcac3 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| CFB props desk | NOT_REVIEWED | CFB-Player-Prop-Tool@fcdcac3 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Horse desk (check_horses, entries pages, eligibility screen) | NOT_REVIEWED | horse-desk@85bf764 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Pre-publish QC gate and leak scan (rig_qc.run_qc / assert_publishable) | NOT_REVIEWED | sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Ledgers A-H index, decision record, source registry, rules view | NOT_REVIEWED | sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Research skeleton, facts, lessons, headless author and challenger | NOT_REVIEWED | sports-rig@ecb6627 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| Hub publisher and site pages | NOT_REVIEWED | NFL-Player-Prop-Tool@8e51f24 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| desk-handoff bridge relay (ChatGPT-owned transport; Cursor runs a pinned copy) | NOT_REVIEWED | desk-handoff@a67fb46 | never | - | none | 0/0/0/0/0 | 0 | none recorded |
| This audit bridge (agent-relay protocol, review tool, coverage generator) | REVIEWED_OPEN_FINDINGS | mlb-props@0d2a395, sports-rig@a0e6321 | mlb-props@5822e0b, sports-rig@2b20f0a | CODE/PARTIAL | REV-20261020-001, REV-20261020-002, REV-20261020-003, REV-20261020-004 | 0/4/1/0/0 | 0 | 2 run, 0 failed |

Verdicts: NOT_REVIEWED, REVIEW_PENDING, REVIEWED_OPEN_FINDINGS, REVIEWED_ACCEPTED_RISK, REVIEWED_SCOPE_LIMITED, STALE_SINCE_REVIEW, REVIEWED_CLEAN_AT_SHA.
