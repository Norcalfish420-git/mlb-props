# REV-20261021-003

Recovery retarget for independent review. Not a release approval. Not a certification.

## Targets

- `Norcalfish420-git/sports-rig` `review/release-recovery-20261021` `01ec53fb9b81792415ac0ca7b905a6001329aff5`
- `Norcalfish420-git/desk-handoff` `main` `fd07c610b3604f08faf23730538950a6340df3d4`
- `Norcalfish420-git/mlb-props` `review/release-recovery-20261021` `acdf8bf31d706bea12b48a9cfbf7b87cd22bb742`

`sports-rig` `main` remains `9a5d193a00a463fe5849c644473b5848464514d3`. The recovery commit is that main plus one registry change. It is not merged.

## What changed

Showdown, QC and ledgers were still registered at older commits. The registry now names the recovery commit above. That commit contains the Showdown publisher guards, the unranked-alternative copy fix, and a contract hash update.

The contract row `DESK-HANDOFF-CONTRACT-V1.3` now hashes the bytes of desk-handoff `fd07c610b3604f08faf23730538950a6340df3d4`. The earlier amendment `1ecf1884d1f953c357513beffcabc067ec06fa3b` stays in the amendment list.

The desk relay tool now names desk-handoff `main` at that same contract commit. Its bridge code did not change. New files under the bridge are handoff notes.

`REV-20261020-001` is still an invalid pin. It has no manifest or handoff content hashes. Those hashes were not invented and the old pin was not rewritten.

## What did not move

NFL props, the Showdown engine pin, the hub publisher pin, CFB, horses, research, and the audit-bridge sports-rig scripts stay on their previous registered commits. Those paths did not change, or the installed checkout is a different dirty branch that was left alone.

The disabled automation sandbox is `sports-rig` `review/release-recovery-automation` `43c1a565f02aa1429a7cbe8dc95d2ff338f453f0`. It is not a registered production target. It refuses to run without a dry-run flag and it has no PASS result.

## Tests

At the recovery commit, the sports-rig suite ran 438 tests and all passed. At the automation commit it ran 447, including 9 sandbox tests, and all passed. Horse tests at the registered horse commit ran 72 and all passed.

The old Showdown commit still fails the current ranking and publish tests. That reproduction is evidence. It is not the candidate.

## Ask

Re-verify the findings named in the manifest at the recovery commit, or keep them open. Do not treat a Cursor test pass as verification. Do not treat `REV-20261020-001` as repaired.
