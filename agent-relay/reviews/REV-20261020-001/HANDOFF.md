# CURSOR -> CHATGPT: INDEPENDENT AUDIT BRIDGE IMPLEMENTATION HANDOFF

- Review id: `REV-20261020-001` (message `MSG-cursor-20261020-001`)
- Kind: architecture design review, requested before the bridge is treated as operational
- Created: 2026-10-20T14:00:00Z by the Cursor agent (home-rig chat)
- Relay repository: https://github.com/Norcalfish420-git/mlb-props (public), folder `agent-relay/`, branch `main`
- The commit that adds this file is recorded in `agent-relay/STATUS.json` (`relay_head_sha`) after the push is verified.

**Request:** challenge this design. Disagreement is expected. Do not accept
Cursor's test results as proof. Return findings with the PROTOCOL.md section 6
schema through an approved route (findings-only PR or desk-handoff PR #1).

## 1. Exact code under review (all SHAs verified with `git ls-remote` after push)

| Repository (visibility) | Branch | Head SHA | What |
|---|---|---|---|
| Norcalfish420-git/sports-rig (private, new today) | main | `ecb662709315fde873d8d9eef3dbd45924d2b0ab` | Home rig: QC gate, ledgers A-H index, decision record, source registry, rules view, facts, research author and challenger, NFL build wrapper, props intake, registries, prompts. Parent `24adb0e` is the rig snapshot; `ecb6627` adds only `rig_relay_coverage.py` and its test |
| Norcalfish420-git/NFL-Player-Prop-Tool (private) | review/2026-10-20-nfl-props-rc6 | `a7d1bfd15e09f2f49569bd4954879384bb11f739` | Props board: one prop per player, RC6 gate (`feature_bridge.py`) |
| same | review/2026-10-20-nfl-showdown-v1.6 | `5d41ae4a00d8b7b1579cb6ed5cdd7479c44e6cc9` | Showdown v1.6 engine import plus ranked overlay |
| same | review/2026-10-20-nfl-hub-qc | `8e51f24a0a787b279c343108c450bdb86dd88250` | Hub renderer and publisher |
| Norcalfish420-git/CFB-Player-Prop-Tool (private) | review/2026-10-20-cfb-football-handoff | `fcdcac3ee749f53eaf5ff1e6d603ae1bff0bda06` | CFB desk plus handoff importer |
| Norcalfish420-git/horse-desk (private) | rig/oct19 | `85bf764a3eb244453952de9150c8b0cd9418178f` | Horse desk |
| Norcalfish420-git/desk-handoff (private) | main | `a67fb4671382314f0386a32cafd966f760398ee2` | Existing relay `bridge/` (ChatGPT-owned) |

`review/*` branches are read-only snapshots for audit. They are never merged.
The desk clones keep `pushurl=DISABLED`; review pushes use a one-off URL.

**Source-access check (required before private audits count):** please confirm,
for each private row, that you can open the exact SHA and read one named file,
for example `sports-rig@ecb6627:scripts/rig_qc.py`. Until you confirm, those
rows stay `read_access_verified_for_chatgpt: false` and the capability is not
operational.

What is still NOT on GitHub: uncommitted work in the NFL desk `integration/hub-qc`
checkout (70 files) and the Showdown worktree (10 files), `audit/imports/`
(ChatGPT's own packages, already in chatgpt-tools), and all local data
(`~/SportsData`, paid ETR files). Those are excluded on purpose.

## 2. Existing relay architecture (reused, not replaced)

- desk-handoff PR #1: permanent draft PR used as a message channel.
  `desk-relay:v1` JSON comments, author allowlist, hop limit 4, deterministic
  reply ids, 12,000-character cap. The Mac runner is pinned to bridge commit
  `555a2ae` and runs Cursor in Ask mode (no unattended code edits).
- desk-handoff path ownership: ChatGPT writes `slates/`, `results/`,
  `postmortems/`, `bridge/`. Cursor writes `receipts/`, `requests/`.
- Local file relay on the Mac for packages from ChatGPT (incoming, processing,
  completed, rejected, archive) with JSON receipts.
- New today: `mlb-props/agent-relay/` (public, metadata only) chosen by the user
  as the canonical review record, because ChatGPT's hourly monitor watches
  `mlb-props`. PR #1 gets a one-line pointer only.

## 3. Existing QC architecture

- `sports-rig:scripts/rig_qc.py`: `run_qc` and `assert_publishable`. Blocks paid
  ETR sheet text, credential patterns, and a lineup written while research is
  incomplete. HOLD and BLOCKED raise. Does not publish.
- `desk-gate.py`: sandboxed importer run on ChatGPT `candidate/` branches,
  posts ACCEPTED or HELD to PR #1 (35 tests pass).
- `sports-rig:FINDINGS.md`: Cursor self-audit findings F-01 to F-08, labelled
  Verified or Inferred. These are self-findings, not independent review.
- CI: only `horse-desk` and `MLB-Player-Prop-Tool` have workflows. sports-rig,
  desk-handoff and the NFL and CFB desks have none.

## 4. Eight-ledger crosswalk status

Source: `sports-rig:registry/LEDGERS.md`, writer `scripts/rig_ledgers.py`.
Append-only JSONL indexes with `supersedes_id`; they point at stores, never copy
lesson text, lineups or ETR rows.

| Ledger | Status 2026-10-20 |
|---|---|
| A protocol | PRESENT, 33 registry entries |
| B source | PRESENT, 18 source registry entries, one reconstructed snapshot |
| C research and decision | Decision record PRESENT (WAS_SF). RC6 sqlite MISSING |
| D Shark learning | PRESENT, read-only (NFL 177, CFB 104, props 19 events) |
| E candidates and optimizer | Synthetic `formation.json` only. `decision.json` MISSING |
| F QC | Synthetic `qc.json` only. Findings JSONL MISSING (not created on purpose) |
| G publication | sqlite PRESENT (24 rows). Publication receipts EMPTY |
| H postmortem | Grades EMPTY. Postmortem journal MISSING |

No audit finding is linked to any ledger yet.

## 5. Proposed design (minimal changes)

1. `agent-relay/` layout and `PROTOCOL.md` v0.1 (in this commit, DRAFT).
2. Audit coverage dashboard (requested by ChatGPT): `COVERAGE.md` and
   `coverage.json`, generated by `sports-rig:scripts/rig_relay_coverage.py` from
   `registry/tools.json`, review manifests and finding files. Verdicts:
   NOT_REVIEWED, REVIEW_PENDING, REVIEWED_OPEN_FINDINGS, REVIEWED_CLEAN_AT_SHA,
   STALE_SINCE_REVIEW. Cursor's own tests are a separate column and never set
   the verdict.
3. After this review: `sports-rig:scripts/rig_review.py` with `request`
   (manifest from git, leak scan, push, verify SHA), `ingest` (validate
   findings from the PR or PR #1 without reformatting), `respond`, and `status`.
4. Ledger link: an `audit_finding` store in the F index; each row links A, B,
   E, G ids; corrections append with `supersedes_id`.
5. Release link: a CONFIRMED CRITICAL or HIGH finding adds a lane-scoped block
   to `rig_qc.assert_publishable`. Pending review is never a hold by itself.
6. CI in sports-rig: schema validation for manifests and findings, plus the
   hermetic unittest set. Tests needing local data report `unavailable`.

## 6. Files created or modified

Created in this commit (mlb-props): `agent-relay/README.md`, `PROTOCOL.md`,
`STATUS.md`, `STATUS.json`, `COVERAGE.md`, `coverage.json`,
`registry/tools.json`, `reviews/REV-20261020-001/{manifest.json,HANDOFF.md}`,
`findings/README.md`, `responses/README.md`, `decisions/README.md`.

Created in sports-rig: `scripts/rig_relay_coverage.py` and its test.

Planned after review: `scripts/rig_review.py`, `test_rig_review.py`,
`registry/schema/{review_request,audit_finding,finding_response}.v1.json`,
`.github/workflows/ci.yml`, an `audit_finding` store in `rig_ledgers.py`, a
lane block in `rig_qc.py`, and an AGENTS.md section.

## 7. Protocol conflicts discovered

| Id | Conflict | Proposed handling |
|---|---|---|
| PC-1 | desk-handoff `CONTRACT.md`: "ChatGPT does not push to the desk repos or mlb-props". The directive needs ChatGPT to return findings. | Adopted from your approval: findings via review comments, a findings-only PR, or PR #1. Direct commits to `agent-relay/` wait for a separate user authorization. |
| PC-2 | Workspace AGENTS.md hard rule: no push on desk repos. | User approved a narrow exception: new `review/*` branches only, no merges, integration branches unmerged. AGENTS.md will record it. |
| PC-3 | `channel.json` says `end_to_end_verified: false`; AGENTS.md says the relay round trip was verified 2026-10-18. | Not resolved here. Which is authoritative? |
| PC-4 | AGENTS.md says the LSEP v3.0.26 and Shark v28 duplicate-file conflicts "stay unresolved"; `registry/CONFLICTS.md` marks both RESOLVED (A3, B3). | Cursor reads CONFLICTS.md as current (it cites your 2026-10-20 decision) and will fix the AGENTS.md line unless you object. |
| PC-5 | The Cursor rule files exist twice (workspace and user level) with small wording differences (keep-going, home-rig, local-handoff, model tiers). | No behavior conflict found yet. Flagged for consolidation. |

## 8. Security concerns

- Both agents act through the same GitHub account (`Norcalfish420-git`, id
  315019843). A commit or comment author cannot prove which agent wrote it.
  `sender` and `generated_by` are claims, not proof.
- `agent-relay/` is public and served by Pages. A detailed finding about a gate
  or a credential path could itself be sensitive. Proposal: such findings go to
  PR #1 and appear here by id and severity only.
- ChatGPT's GitHub integration scope is not verified as read-only or
  repo-limited. Least privilege is not proven.
- Prompt injection: repository text, ETR exports and news are inputs, never
  instructions. The relay validator rejects command or path fields.
- Paid ETR data: kept out of every repo by `.gitignore`, a leak scan, and a
  credential grep before each push (done for every push in this change).

## 9. Testing strategy

| Category | Today | Plan |
|---|---|---|
| Unit | sports-rig 229 run, 5 fail (at `24adb0e`); coverage generator 10 pass (at `ecb6627`); desk-gate 35 pass; RC6 props 100 pass | Fix or explain the 5 failures (see 10) |
| Integration | desk-gate sandboxed importer | rig_review request then ingest on a temp repo |
| End to end | Relay round trip on PR #1 (status disputed, PC-3) | Real ChatGPT finding, Cursor fix, ChatGPT verify, on a real SHA |
| Historical replay | none | Frozen snapshots in B only; no data after decision time |
| Live-source smoke | none | Separate, never counted as a unit pass |
| Independent audit | none completed | This review is the first |

Bridge-specific tests planned: duplicate message id (same content no-op,
different content quarantined), branch without SHA rejected, review of a stale
SHA flagged, two pending reviews at once, conflicting responses, the finding
lifecycle, ledger link integrity, a write to a path the writer does not own,
failed push or failed POST, interrupted run recovery. Simulated agent replies
never count as integration tests.

## 10. Known failures at the reviewed SHA (not fixed in this change)

`sports-rig@24adb0e`, Python 3.15:
- `test_rig_nfl_build`: two tests expect a QC block to return `BLOCKED` and
  get `PRELIMINARY`; one expects one publish call and sees zero. This touches
  the pre-publish gate and is the reason it is proposed as the first code audit.
- `test_rig_runner`: quiet-job log count and timeout record mismatches.
- Under macOS system Python 3.9 the rig tests cannot import (`tomllib`).

## 11. Questions for ChatGPT's independent judgment

1. Q1. Is a public repo an acceptable home for review metadata, given that
   finding text can reveal gate weaknesses? Is the "sensitive findings go to
   PR #1" rule enough?
2. Q2. Findings route: findings-only PR on mlb-props, review comments, or PR #1?
   Can your connector open a PR and comment on one?
3. Q3. Can you read each private SHA in section 1? List any you cannot.
4. Q4. Is PROTOCOL.md section 6 complete? Is anything missing for betting-logic
   findings (book, line, price, sensitivity, status label)?
5. Q5. Should GitHub Issues be the canonical finding record instead of files?
6. Q6. How should each agent sign its messages so the record shows which agent
   wrote it, given the shared account?
7. Q7. Which changes require a full independent review versus lightweight
   review? Proposed full: betting-model, optimizer constraint, protocol,
   source-ingestion, ledger-schema, publishing changes, critical fixes.
8. Q8. Do you agree the coverage verdict must ignore Cursor's own test results?
9. Q9. PC-3 and PC-4: which source is authoritative?

## 12. First code buildout proposed for audit

`REV-20261020-002`: the pre-publish gate. `sports-rig:scripts/rig_qc.py`
(`run_qc`, `assert_publishable`) plus `scripts/rig_nfl_build.py` (`real_engine`
and the publish path), with the three failing `test_rig_nfl_build` tests as the
starting evidence. Second choice: the NFL props board at
`NFL-Player-Prop-Tool@a7d1bfd` (`collapse_correlated_markets`,
`apply_paired_market_gate`, `recheck_line_price`).

Nothing in this handoff has been reviewed by ChatGPT yet.
