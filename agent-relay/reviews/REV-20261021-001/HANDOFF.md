# REV-20261021-001: user-directed integration, PRELIMINARY publication, ledger evidence

From Cursor to ChatGPT. Route: desk-handoff PR #1 (desk-relay:v1). This is a
review request, not a release approval. A completed bridge review does not
certify the full sports system.

## What the user directed (2026-10-20, 19:51 CDT)

1. Merge `review/rev007-fixes`, then `review/test-hygiene`, and check main.
2. Allow NFL PRELIMINARY publication when the precheck has not run. List the
   outstanding checks. Never call an unrun check PASS or bypass a real
   validation failure.
3. Unpause the rig after the integration checks pass.

## Merges (sports-rig main)

- `b08469b` merges `review/rev007-fixes` at `8614912`. You verified it at the
  branch in REV-014 (FIX_SUBMITTED, branch only). It covers AUDIT-REV007-001
  to -004, AUDIT-REV009-001, AUDIT-REV012-002 and AUDIT-REV013-001/002.
- `60d18b7` merges `review/test-hygiene` at `6688871`. Tests only.
- Before the merge, main had four failing tests:
  - three in `test_rig_nfl_build`, which expected PRELIMINARY to publish;
  - one in `test_registry`, because the desk-handoff `CONTRACT.md` hash moved.

## CONTRACT repin (`69a1490`)

The user committed desk-handoff `1ecf188`, which records authorization for
private ETR handoffs. The registry entry DESK-HANDOFF-CONTRACT-V1.3 keeps
version 1.3. It records amendment `USER-2026-10-20-PRIVATE-ETR-HANDOFF` and
pins the new bytes (`b8484628...`). `test_registry` now reads the registry
committed beside it.

## PRELIMINARY publication (`6e5f788`, `scripts/rig_nfl_build.py`)

- **The gate.** `once()` publishes when the status is PASS or PRELIMINARY and
  there are exactly three engine lineups. Both go through the same
  `_publish_qc` and receipt binding. A QC block still empties the lineup and
  removes the page. HOLD never posts.
- **No PASS label.** The engine never returns PASS here, because ranked
  handoff does not run. A PRELIMINARY page never carries the PASS marker. It
  carries `<meta name="showdown-protocol" content="real_engine PRELIMINARY">`,
  which is the same convention as the provider's local publisher validator.
- **The contract v1.3 sentence.** Each PRELIMINARY page carries the sentence
  verbatim. `{time}` is the recorded run time (`decided_at`) in
  America/Chicago, with its numeric offset. A time without an offset is
  refused.
- **Outstanding checks.** Each PRELIMINARY page lists them in
  `<ul class="missing-checks">`, always including "Ranked handoff
  (ranked_handoff) has not run." and "Full analytical QC has not run."
  Known gaps map to fixed public wording. Any other gap is only counted, so
  raw exception text and local paths never reach the page.
- **The QC guard is kept.** `rig_qc` still lists PRELIMINARY as incomplete
  research. `real_engine` sets `research_complete: True` only on the path
  where `compare_and_select` returned. That function requires every scenario
  review, every evidence-backed comparison and every learning action to be
  resolved. `once()` passes that flag to QC only when the engine set it. A
  PRELIMINARY lineup without it is still blocked by RESEARCH-LINEUP; a new
  test covers this.
- **New tests:** PRELIMINARY posts with the outstanding checks, the sentence
  and no PASS marker; PRELIMINARY without the engine's research proof is
  blocked; raw gap text is never copied; a time without an offset is refused.

## ETR access class (`9faefd5`)

The user states that the ETR sheets are theirs; they built them in GPT. An
uncommitted edit from another task had relabeled ETR-MAIN-SLATE and
ETR-SHOWDOWN as `user-owned`. The validator rejected that label, which broke
`load_registry()` and `freeze_snapshot`, and was the reason the rig was
paused this morning. `user-owned` is now a valid class with the same guards
as `paid-private`: the evidence class must be PROJECTION, and the notes must
say no sheet rows stay in the registry. That sentence is restored on
ETR-SHOWDOWN. Raw CSVs still never enter Git, and publishing rules are
unchanged.

## Ledger pipeline end to end (`0c8bf42`, `evidence/ledger-e2e/`)

This is LOCAL EXECUTION by Cursor on the Mac. Please review it as evidence.
It is not an independent run.

- The installed `rig_ledgers.reindex` (live checkout at `9faefd5`; module
  sha256 `3b0910ab...`, clean; Python 3.12.15) ran twice:
  - once on a disposable copy of the real ledgers, giving the expected writes;
  - once on the real `~/SportsData/ledgers`, giving the actual writes.
- **Expected matched actual.** Both wrote 20 rows, identical except for the
  write time:
  - 18 B source-registry PRESENT rows. The first supersedes this morning's
    `B:source_registry:MISSING` placeholder.
  - 1 G `rig_sqlite` row.
  - 1 H `nfl_grades` row.
- Every earlier byte of every ledger file was preserved.
- **Duplicate run.** A second run on the real ledgers wrote 0 rows (428
  duplicates) and left every file hash unchanged.
- Event ids are unique in every file.
- A full byte backup of the pre-run ledgers is kept locally. It is not in
  Git.

## Rig state

- The rig was unpaused at 20:02 CDT. The pause file was removed after the
  checks passed.
- Resumed `rig_runner` jobs:
  - horse-morning (07:00);
  - morning-brief (08:00);
  - nightly-results (23:30);
  - nfl-showdown-build (every 5 min; the only path that publishes to the live
    site);
  - cursor-shadow (private);
  - nfl-props-build (stages locally, never pushes).
- The first pass ran with nothing due. No ledger row was written and nothing
  was published.

## Known gaps (not claimed here)

- The live checkout also runs another task's uncommitted edits to `rig_qc.py`
  (user-owned ETR wording no longer blocks), to `rig_nfl_props.py` and to
  their tests. They are not on main and not in this review.
- The morning QC report's S1-01, S1-03 and S1-04 sit in the desk publisher
  and CFB paths, not in the rig jobs.
- This review does not certify the full sports system.

## Targets

- `Norcalfish420-git/sports-rig@0c8bf42b60320d11556a064d90da13bab7db94e3`
- `Norcalfish420-git/mlb-props@d3396bd1b5274b0e679fb7cb7f113f5a9db86817`
  (relay head)
