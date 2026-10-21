# REV-20261021-002

Re-verification of AUDIT-20261021-001-001 and AUDIT-20261021-001-002. Not a release approval. Not a certification of the sports system.

Target: `Norcalfish420-git/sports-rig` main `27dacd56d0d7fd221240ce6a9b2ad8982b15555e`. The code change is commit `8b34a2cbd65f6de6eb52b3dc90df9fc6ce666573`. The later commit on main only adds the training record and `AGENTS.md`.

## What changed

`lineups_from_decision` still takes the comparison winner as the primary. The other two seats are filled in lineup-identity order, not formation order. Their label is `alternative_unranked` and their rank is null. `_fill_pivots` cannot create a primary. A page says "Pivot N" only when a row is already marked ranked. Nothing in this commit writes that mark. `ranked_handoff.create` is the function that will own an explicit pivot rank, and only for a reviewer-owned list. It is not called on the PRELIMINARY path.

`copy_blocks()` builds one plain-text block per lineup. The page puts that text in each `pre` and in the copy-all block. The copy buttons read those nodes. A missing number is the word unknown. An open check keeps the condition. A local path or address in that condition is replaced before it is shown.

`lineup_ids` no longer fills an empty rank with a position number.

## Tests

81 focused tests passed, including `PivotRankingTests` and `CopyOutputTests`. The full suite was 428 run, 427 passed, 1 failed. The failure is `DESK-HANDOFF-CONTRACT-V1.3`: the desk checkout has uncommitted edits in `CONTRACT.md`, so the file hash is not the pinned hash. This commit does not change that file.

## Ask

Confirm formation order cannot change a published rank, and that the page text and the copy text cannot diverge. Leave the tools registry targets where they are until that confirmation.
