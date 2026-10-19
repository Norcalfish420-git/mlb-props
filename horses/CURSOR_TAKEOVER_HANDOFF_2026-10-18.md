# Horse Tool — Cursor takeover handoff (2026-10-18)

## Ownership and scope
Cursor owns architecture, private source ingestion, ledger maintenance, public hub integration, source verification, and all future horse-racing publication. Do not regenerate or resend Oct 17 watchlists or Oct 18 provisional audit; those are already on the practice board. Preserve historical selections/decisions, immutable as-of evidence and postmortem lineage.

## Existing canonical artifacts (ChatGPT Library; NOT uploaded to public GitHub)
- `Horse_Racing_Master_Ledger.xlsx` (2026-10-12/13 snapshot)
- `Horse_Racing_Master_Ledger_Oct15_16_Prescout.xlsx` (more recent 2026-10-17 snapshot; prefer over base ledger but reconcile versions)
- `Horse_Racing_Source_Register_2026-10-11.json` (source and collection metadata; registry includes source records SRC-030–SRC-058)
- `Horse_Racing_AI_2023_Backtest_Buildout_Master_Plan_2026-10-14.md` (v2.1 research/buildout master plan)
These are held in the user's ChatGPT file Library, not in this repository. Request an authorized transfer of the exact files before claiming full code/ledger synchronization. Do not publicly upload workbooks or PP data before checking paid-data licensing, privacy, proprietary data, personal details, and raw odds.

## Source register (verified entries from ledger)
Entry template: https://tvg.equibase.com/static/entry/RaceCardIndex{TRACK}{MMDDYY}USA-EQB.html
Late-changes template: https://tvg.equibase.com/static/latechanges/html/latechanges{TRACK}-USA.html
The dated entry card does NOT prove final scratches, gate, surface or real-time pricing.

| Source ID | Name | URL | Use / restriction |
|---|---|---|---|
| SRC-030 | Keeneland entries | https://tvg.equibase.com/static/entry/RaceCardIndexKEE101126USA-EQB.html | public dated entries; scheduled not final |
| SRC-031 | Gulfstream entries | https://tvg.equibase.com/static/entry/RaceCardIndexGP101126USA-EQB.html | public dated entries; scheduled not final |
| SRC-032 | Santa Anita entries | https://tvg.equibase.com/static/entry/RaceCardIndexSA101126USA-EQB.html | public dated entries; scheduled not final |
| SRC-033 | Belmont entries | https://tvg.equibase.com/static/entry/RaceCardIndexBEL101126USA-EQB.html | public dated entries; scheduled not final |
| SRC-034 | KEE changes | https://tvg.equibase.com/static/latechanges/html/latechangesKEE-USA.html | public rolling page; verify displayed date/time |
| SRC-035 | GP changes | https://tvg.equibase.com/static/latechanges/html/latechangesGP-USA.html | public rolling page; verify displayed date/time |
| SRC-036 | SA changes | https://tvg.equibase.com/static/latechanges/html/latechangesSA-USA.html | public rolling page; verify displayed date/time |
| SRC-037 | BEL changes | https://tvg.equibase.com/static/latechanges/html/latechangesBEL-USA.html | public rolling page; verify displayed date/time |
| SRC-038 | Keeneland complimentary PP index | https://www.keeneland.com/racing/complimentary-pps | publicly browsable; date links, rights review |
| SRC-039 | KEE Oct 11 PP | https://www.keeneland.com/files/10-11-26-kee-official-ppspdf.pdf | complimentary PP; avoid raw redistribution |
| SRC-040 | NYRA Belmont entries | https://www.nyra.com/belmont/racing/entries/?day=2026-10-11&limit=entries | dated cross-check; quoted prices not authenticated pre-post |
| SRC-041 | Churchill calendar | https://www.churchilldowns.com/come-to-the-track/ | schedule; direct page previously 403 |
| SRC-042 | Pimlico redevelopment | https://www.pimlico.com/redevelopment/ | venue calendar/eligibility; no automatic Laurel substitution |
| SRC-043 | Saratoga calendar | https://www.nyra.com/saratoga/news/nyra-unveils-stakes-schedule-for-the-2026-saratoga-summer-meet/ | seasonal eligibility |
| SRC-044 | Del Mar calendar | https://www.dmtc.com/season | seasonal eligibility |
| SRC-045 | Oaklawn calendar | https://www.oaklawn.com/racing/calendar/ | seasonal eligibility |
| SRC-046 | Monmouth calendar | https://www.monmouthpark.com/event/opening-day-4/ | venue-specific calendar |
| SRC-047 | Keeneland commentary | https://www.keeneland.com/racing/expert-picks/100 | unstable commentary; lead, not proof |
| SRC-048 | Historical exacta probables | NOT CONFIGURED | ordered-pair/time/base/return missing; no verified free historical exacta feed |
| SRC-049 | GP/SA/BEL complete PP | NOT RETRIEVED | requires authorized dated programs |
| SRC-050 | Blind contamination log | conversation research log 2026-10-11 | quarantine races with results seen before freeze |
| SRC-051 | On-demand workflow | conversation instruction 2026-10-11 | run full venue inventory, preserve provenance |
| SRC-052 | DRF/1ST GP/SA program route | https://promos.drf.com/1stracingpps | login/coupon/checkout gate; no unauthorized acquisition |
| SRC-053 | NYRA free Equibase PP signup | https://fs2.formsite.com/nyra2016/EquibasePPs/index.html | signup/email entitlement; not previously submitted |
| SRC-054 | TwinSpires Pools and Probables | https://support.twinspires.com/hc/en-us/articles/22361024823437-How-do-I-find-the-Pools-and-Probables | live exacta display route; no historical quote matrix verified |
| SRC-055 | TVG Equibase Watch and Wager PPs | https://tvg.equibase.com/tvgByRaceSet.cfm | paid program; not purchased |
| SRC-056 | AmWager API documentation | https://wagerapi.amwager.com/swagger/ui/index | bearer token required (HTTP 401); no authorized quote feed captured |
| SRC-057 | KEE Oct 11 local PP artifact | https://www.keeneland.com/files/10-11-26-kee-official-ppspdf.pdf | 23-page downloaded card, not to be republished |
| SRC-058 | DRF dated card availability | https://www.drf.com/drp-program | login/access gate; no entitlement bypass |

**Registry gap:** This available snapshot identifies SRC-030 through SRC-058, NOT SRC-001 through SRC-029. Locate earlier canonical source ledger/versions before fabricating those IDs. Ledger contains additional date-scoped `SRC-20261012-*` and `SRC-20261016-*` evidence records; treat these as separate run-specific IDs, not replacements for numbered base IDs.

**Exacta:** SRC-048 is the missing historical exacta-probables source; SRC-054 documents a live display route. No free historical exacta matrix is verified. Block exacta recommendations without authenticated ordered-pair quote, quote timestamp, stake base, joint probability, and rule threshold.

## Protocol / controls
- Latest verified ledger protocol: **v1.12**. No newer numbered rule IDs verified from these files.
- Full allowed-track inventory and exclusions; maiden race and maiden performance lines excluded. Sloppy races and off-turf changes require protocol-specific quarantine/exclusion.
- Trainer layoff >=90 days is negative except documented top-5 current-meet trainer exemption; verify actual outer post >=10 only at distance >=1 mile.
- Morning line is NOT a live quote; no actionable overlay without authentic timestamped price and well-calibrated probability.
- Keep `WATCHLIST`, `HOLD`, `PASS`, `approved_wager`, `settled_wager`, `verified_result`, and `ROI` strictly separate.
- Do not import outcome information into pre-race decisions; preserve immutable freeze time, as-of time, source ID, retrieved time, and data quality.
- Historical 2023 Equibase request pending in Oct 14 plan; verify receipt, license/terms before ingestion. Distinguish fixed pre-race selection tests from historical quote-dependent value tests; prevent future-result/final-odds leakage.
- Log every run and postmortem with learning/lineage; provisional postmortem is not a betting win.
- QC/precheck is informative and on demand, not a blocker to publishing clearly labeled provisional results.

## Existing output / handoff
- `horses/postmortems/2026-10-18.json` on `chatgpt`, provisional, no certified bets.
- `https://github.com/Norcalfish420-git/mlb-props/issues/1` has Cursor request and ledger response.
- Local-only practice pages: `http://127.0.0.1:8765/horses.html` and dated routes.
- Ledger reply request `cursor-c6a884573958433a93bdea6fc7f0a9b5` still awaits acknowledged response from Cursor.
- Architecture integration: isolate read-only data collectors, normalized canonical registry, immutable decision snapshots, scenario/ranking engine, eligibility and quote gates, results/postmortem grader, public export, and schema validation. Cursor decides deployment/merge. No secret/token in repository.

## Handoff completion definition
Import authorized original Library artifacts privately; reconstruct full source registry including missing SRC-001–029; reconcile versions; identify protocol diffs beyond v1.12 only from actual provenance; ingest verified results; expose Horses/Results pages; reply with commit SHA, published URL, grading state and explicit blockers.
