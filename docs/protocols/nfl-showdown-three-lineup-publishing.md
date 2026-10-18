# NFL Showdown: three ranked lineups — required Git handoff

Version: 1.0
Effective: 2026-10-18
Authority: ChatGPT decides; Cursor validates, renders and publishes after user approval.

## Mandatory output per matchup
Exactly three **fully specified**, **DraftKings-legal** lineups, ordered:
1. `PRIMARY` — preferred cash/double-up build, highest-confidence lineup for stated contest type.
2. `PIVOT_A` — strongest distinct credible alternative.
3. `PIVOT_B` — second distinct alternative.

Each has CPT (one) and five FLEX, player IDs where sourced, team and position, salary paid by slot (including 1.5x CPT salary), combined salary <= $50,000, leftover, showdown team split, ETR projected score (when sourced), slate-specific risk and reason, game-script assumption, and conditional trigger for substitution. No duplicate player within a lineup; both teams must be represented; observe DK roster rules. Never silently fill data gaps.

## Decision gates
- Run the complete CFB/NFL Showdown protocol and historical lessons, opponent defensive audit, injury/lineup/news receipts, ETR projection/value review, salary validation, two-FLEX pair comparison, alternate CPT and construction challenge, and Shark QC.
- Default double-up objective is safe base points. Favor both starting QBs and both clear-workload RBs if game/salary/usage allow; exception must be documented. Do not use a punt CPT for cash. Pivots need not be more volatile merely to be different.
- Mark every lineup with `DRAFT | HOLD | APPROVED | INVALIDATED`. Do not publish `HOLD` as playable or call it final. Missing material projections, player or matchup status, salaries, unverified starter or new material news -> HOLD and quarantine prior builds.
- Cite ETR sheet as-of and source versions, DK salary source/as-of, local beat/official/Rotowire injury timestamp, time checked, kickoff and prelock re-check. Rerun if material update arrives. Do not invent projections or QC passes.
- A slate with fewer than 3 approved lineups is **not completed**. Preserve provisional candidates separately, clearly non-playable.

## Handoff structure
Path: `handoffs/nfl-showdown/YYYY-MM-DD_AWAY_HOME.json`
Suggested schema:
{
  "schema_version": "nfl_showdown_three_ranked_v1",
  "sport": "NFL",
  "slate_id": "YYYY-MM-DD_AWAY_HOME",
  "contest_type": "double_up",
  "status": "HOLD",
  "kickoff_local": null,
  "research_checked_at": null,
  "etr_source": {"version": null, "as_of": null},
  "dk_salary_source": {"url": null, "as_of": null},
  "qc": {"shark_ledger_loaded": false, "shark_lessons_evaluated": false,
         "two_slot_audit_passed": false, "injury_gate_passed": false,
         "salary_gate_passed": false, "prelock_gate_passed": false},
  "lineups": [
    {"rank": 1, "type": "PRIMARY", "status": "HOLD", "captain": null, "flex": [],
     "salary_used": null, "salary_left": null, "projected_points": null,
     "team_split": null, "game_script": null, "rationale": null, "pivot_trigger": null},
    {"rank": 2, "type": "PIVOT_A", "status": "HOLD", "captain": null, "flex": [],
     "salary_used": null, "salary_left": null, "projected_points": null,
     "team_split": null, "game_script": null, "rationale": null, "pivot_trigger": null},
    {"rank": 3, "type": "PIVOT_B", "status": "HOLD", "captain": null, "flex": [],
     "salary_used": null, "salary_left": null, "projected_points": null,
     "team_split": null, "game_script": null, "rationale": null, "pivot_trigger": null}
  ],
  "receipts": [],
  "decision_journal_ref": null,
  "postmortem_ref": null
}

## Cursor publishing contract
- Render rank #1 prominently as **Best Play** and ranks #2/#3 as **Pivot A/B**, each with a working **Copy lineup** control; show time/QC status, salary, split, projected points when sourced, reason and conditional switch.
- Preserve current hub styling and existing ETR-value tab. Insert a ranked-lineups display into the Card Build tab.
- Cursor cannot select/change players, rank, weights, projections or QC outcomes. Invalid input must stop publishing and return diagnostics to ChatGPT.
- Git stage on `chatgpt` branch as a handoff. Do **not** merge/push live pages on `main` without user approval. On approval, Cursor imports verified JSON, previews it, and publishes page plus hub index.
- Save immutable dated handoffs, decision journal, versions, and postmortem reference. Retain previous revisions via Git. Never overwrite approved selections without new version/reason.
- This requirement applies on **every future NFL Showdown Git/hub push**; use the same ranking pattern for CFB Showdown where applicable.
