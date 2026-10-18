# NFL Showdown publishing contract (2026-10-18)

Applies to all future NFL Showdown handoffs from ChatGPT to Cursor/Git/hub.

## Required ranked outputs per matchup
1. **PRIMARY** — highest-confidence certified Showdown lineup.
2. **PIVOT_A** — highest-ranked alternative with an explicit rationale.
3. **PIVOT_B** — second-ranked alternative with an explicit rationale distinct from Pivot A.

Each lineup contains exactly one captain and five FLEX positions, with unique player identifiers, team, DK position, DK CPT/FLEX salary, full $50,000-cap validation, team split, ETR expected fantasy points where sourced, ownership if available, slate/date, and a concise game-script explanation. Include copy-ready six-player format, plus timestamps/source receipts for salaries, ETR, injuries, inactives, beat reports, news, and QC. A pivot must be a complete legal lineup, not a suggested swap. Explicitly distinguish ranked confidence from maximum upside.

## Publication gates
- ChatGPT selects and ranks; Cursor validates/renders/publishes only after user approval. Cursor does not re-pick or change ranks.
- Require Stage-1 opponent-defense captain audit, ETR value screening, two-FLEX pair audit, adversarial alternate-CPT/salary/team-split comparison, Shark ledger/lessons evaluation, status/inactive source timestamps, and final prelock verification. For cash/double-ups, default to both starting QBs and both dependable feature RBs when justified, and never force a punt captain.
- Any failed validation, missing actual player projection, incorrect salary, material lineup conflict, unverified status, or absent prelock check means **HOLD**. Do not publish a HOLD build as a betting-approved recommendation; display diagnostic status only.
- Archive the three finalists, excluded alternatives, evidence, rank justification, handoff schema version, source timestamps, and postmortem references. Never overwrite the reasoning record silently.

## Required handoff shape
```json
{
  "schema_version": "nfl-showdown-3-ranked-v1",
  "slate_id": "YYYY-MM-DD_AWAY_HOME",
  "status": "APPROVED | HOLD",
  "verified_at": "ISO8601 timezone-aware timestamp or null",
  "lineups": [
    {"rank": 1, "role": "PRIMARY", "captain": {}, "flex": [{},{},{},{},{}], "salary_used": null, "salary_remaining": null, "team_split": null, "projection": null, "rationale": "", "copy_text": ""},
    {"rank": 2, "role": "PIVOT_A", "captain": {}, "flex": [{},{},{},{},{}], "salary_used": null, "salary_remaining": null, "team_split": null, "projection": null, "rationale": "", "copy_text": ""},
    {"rank": 3, "role": "PIVOT_B", "captain": {}, "flex": [{},{},{},{},{}], "salary_used": null, "salary_remaining": null, "team_split": null, "projection": null, "rationale": "", "copy_text": ""}
  ],
  "qc_receipts": {}, "source_receipts": {}, "journal_ref": ""
}
```

## Hub display requirements
Matchup pages show PRIMARY first and pivots second and third, with separate **Copy lineup** actions and rationale, total salary, projected points (if actually sourced), and status for each. The index links each matchup and shows approval/HOLD status. Publish only verified data; don't fill gaps by inventing projections or player status.
