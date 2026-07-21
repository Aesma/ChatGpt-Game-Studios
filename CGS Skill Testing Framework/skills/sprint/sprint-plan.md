# Skill Test Spec: `$sprint-plan`

## Skill Summary

`$sprint-plan` creates or updates a sprint using only existing registered story
files whose source status is exactly `Ready` and whose final read-only
`$story-readiness` result is `READY` for the exact current story-byte hash. It
checks QA-plan state and PR-SPRINT before one complete changeset authorization,
then writes the Markdown plan and YAML tracker as one verified pair. The legacy
`status` argument redirects to `$sprint-status` and terminates with zero gates
and zero writes.

Verdicts: `COMPLETE`, `COMPLETE — no changes required`, or `BLOCKED`.

---

## Static assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name
  matches the skill directory.
- [ ] Arguments expose `new|update`; the legacy word `status` appears only in an
  explicit redirect/terminal compatibility branch.
- [ ] The `status` branch says `STOP` and asserts zero gates and zero writes
  before review-mode or planning-context resolution.
- [ ] CLI review override has first priority and is resolved exactly once.
- [ ] Missing review-mode configuration defaults in memory and is never written
  by this workflow.
- [ ] Candidate work comes from `production/epics/*/EPIC.md` story rows and
  matching existing story files, never from a GDD feature scan.
- [ ] A new candidate requires both exact source status `Ready` and final
  readiness verdict `READY` bound to a SHA-256 of exact current story bytes.
- [ ] `Needs Work`, `Blocked`, aliases, historical verdicts, and changed hashes
  are ineligible.
- [ ] QA-plan findings and warnings resolve before PR-SPRINT, preview, approval,
  and write.
- [ ] Both final files are rendered and shown in one complete changeset preview
  after all findings and gate-driven revisions.
- [ ] No final target write occurs before one authorization of the exact final
  pair.
- [ ] Successful completion requires exact post-write hash verification of both
  the plan and tracker; partial write never yields COMPLETE.
- [ ] Contains verdict keywords `COMPLETE` and `BLOCKED` and at least two phase
  headings.

---

## Case 1: Happy path — registered and currently READY stories

**Fixture**

- Current milestone and capacity exist.
- `production/epics/movement/EPIC.md` has two managed story rows with status
  `Ready`.
- Each row resolves uniquely to a matching sibling `story-NNN-*.md`; story
  header identity/status/layer/type agree.
- Read-only story-readiness returns final `READY` for each exact file hash.
- A QA plan for sprint 003 exists.
- Review mode is `lean`.
- Both sprint targets have known preimages.

**Input:** `$sprint-plan new`

**Expected behavior**

1. Builds the immutable story registry and readiness/hash evidence.
2. Selects existing work by dependency/layer/priority within capacity.
3. Renders plan and tracker with identical work-item sets.
4. Adds the QA-plan path before the producer checkpoint.
5. Notes `[PR-SPRINT] skipped — Lean mode`.
6. Shows the exact two-file changeset once; user authorizes it.
7. Rechecks story and target hashes, writes the pair transactionally, and
   verifies both final hashes.

**Assertions**

- [ ] Every task points to an existing canonical story path.
- [ ] Tracker IDs are derived only from the existing epic slug/story number.
- [ ] Every new item has `source_status: Ready`, `readiness_verdict: READY`, a
  matching `source_sha256`, and initial tracker status `ready-for-dev`.
- [ ] Priority does not change lifecycle status.
- [ ] No GDD-derived task or copied acceptance criterion appears.
- [ ] Verdict is COMPLETE only after both final files verify.

---

## Case 2: SP-001 — empty or non-ready backlog fails closed

Run each variant independently:

| Variant | Fixture | Expected result |
|---|---|---|
| 2a | No EPIC story rows/files exist; a GDD contains a feature tagged ready | BLOCKED; recommend `$create-stories`; no invented task |
| 2b | Story row/file status is `Needs Work` | Excluded; never selected |
| 2c | Story row/file status is `Blocked` | Excluded; never selected |
| 2d | Header says `Ready`, final readiness is `NEEDS WORK` or `BLOCKED` | Excluded; header does not override gate |
| 2e | EPIC row and file identity/status disagree | BLOCKED when scope is ambiguous or requested |
| 2f | Story bytes change after final READY is computed | Stale result rejected; recheck required before selection |

**Assertions**

- [ ] GDD prose is never promoted to a sprint work item.
- [ ] No producer gate or write occurs when a new sprint has no eligible READY
  candidate.
- [ ] Exact current story SHA-256 binds selection and survives into both drafts.
- [ ] A user cannot waive `NEEDS WORK` or `BLOCKED` into the sprint.

---

## Case 3: SP-002 — missing QA plan is resolved before write

**Fixture**

- Eligible READY stories exist.
- No QA plan identifies the proposed sprint.
- Review mode is `full`; PR-SPRINT would otherwise be available.

### Variant A: pause for QA planning

User selects `Pause and run $qa-plan sprint first`.

- [ ] Verdict is BLOCKED before PR-SPRINT and before changeset authorization.
- [ ] Neither sprint target is written.
- [ ] No "sprint written" or COMPLETE message appears.

### Variant B: accept missing-QA warning

User selects `Continue with an explicit missing-QA warning`.

- [ ] The exact warning is present in the Markdown draft and
  `qa_plan: MISSING` is present in the YAML draft before PR-SPRINT.
- [ ] PR-SPRINT reviews the warning-bearing draft.
- [ ] The complete warning-bearing two-file changeset is previewed before write.
- [ ] No warning or other content is appended after authorization or after the
  first final-target write.

---

## Case 4: SP-002 — gate revision cannot mutate an authorized draft

**Fixture**

- QA finding has already been incorporated.
- Full-mode PR-SPRINT returns `UNREALISTIC` or `CONCERNS`.

**Expected behavior**

1. No file has been written and no changeset has been authorized yet.
2. Scope/capacity decision is resolved.
3. Both plan and tracker are re-rendered from the same revised set.
4. Invalidated readiness/QA/gate checks rerun.
5. Only the final pair is previewed and authorized.

**Assertions**

- [ ] Gate input, final preview, and persisted pair describe the same work-item
  set and story hashes.
- [ ] An earlier draft or approval is never reused after a material revision.
- [ ] A malformed/failed full-mode gate blocks with zero final-target writes.

---

## Case 5: SP-003 — review override and missing configuration are side-effect free

### Variant A: CLI override wins

**Fixture:** invocation includes `--review full`; file contains `solo`.

- [ ] Resolved mode is `full` for readiness and PR-SPRINT.
- [ ] The file value does not overwrite the CLI value.
- [ ] `production/review-mode.txt` is not changed.

### Variant B: configuration is missing

**Fixture:** no review-mode file; invocation has no override.

- [ ] Mode defaults to `lean` in memory.
- [ ] No review-mode prompt or write occurs.
- [ ] If the user later declines the sprint changeset, the configuration remains
  absent and every project file remains unchanged.

### Variant C: invalid configuration

- [ ] Skill reports the invalid value, uses the documented in-memory default,
  and does not repair the file as part of sprint planning.

---

## Case 6: SP-004 — status is a hard read-only terminal branch

**Input:** `$sprint-plan status --review full`

**Expected behavior**

1. Argument parsing recognizes legacy `status` before review resolution.
2. Output directs the user to `$sprint-status`.
3. The branch executes `STOP`.

**Assertions**

- [ ] No review-mode, milestone, sprint, story, QA, or risk file is read for
  planning.
- [ ] No story-readiness, QL-STORY-READY, or PR-SPRINT gate runs.
- [ ] No changeset is prepared and no directory/file write occurs.
- [ ] Terminal evidence reports `gate_count = 0` and `write_count = 0`.
- [ ] Execution cannot fall through into new/update drafting phases.

---

## Case 7: atomic pair and stale-preimage protection

Run each variant independently after final authorization:

| Variant | Change before write | Expected result |
|---|---|---|
| 7a | Selected story hash changes | Write nothing; invalidate readiness and rebuild |
| 7b | Plan or tracker preimage changes | Write nothing; re-preview the complete pair |
| 7c | Temporary candidate hash mismatches | BLOCKED; final targets untouched |
| 7d | Second replacement or post-write verification fails | Restore both preimages; BLOCKED; report possible paths |
| 7e | Both final hashes match | COMPLETE with both hashes |

**Assertions**

- [ ] One-file success is never reported as sprint success.
- [ ] Compare-and-swap checks cover both targets and all selected story sources.
- [ ] COMPLETE is emitted only after exact final verification.

---

## Case 8: update preserves lifecycle and gates additions

**Fixture**

- Matching active plan/tracker pair exists.
- Existing work includes `in-progress`, `review`, and `blocked` items.
- User requests one new story whose source/final status is READY.

**Assertions**

- [ ] Existing lifecycle statuses are preserved.
- [ ] The new addition passes the same EPIC-row, source-status, readiness, and
  story-hash checks as a new-sprint candidate.
- [ ] Non-not-started items cannot be silently removed or reset.
- [ ] A missing/mismatched plan/tracker pair blocks instead of choosing the most
  recently modified sprint.

---

## Case 9: Plan and tracker share one revisioned story set

- [ ] Markdown and YAML contain the same stable sprint ID, plan revision,
      story-set hash, and timezone-qualified updated_at
- [ ] Story-set hash uses sorted `ID<TAB>path<TAB>current-raw-story-hash`
      records with LF/no trailing LF and changes when any story bytes change
- [ ] Plan revision covers QA findings, producer outcome, risks, capacity, and
      final scope without self-hashing its own field
- [ ] A post-preview revision/hash change invalidates authorization and both
      files remain an atomic pair

## Protocol compliance

- [ ] Story registry/readiness, QA check, and producer check are read-only.
- [ ] User scope choices are distinct from the one write authorization.
- [ ] Review-mode configuration is outside the authorized sprint path set.
- [ ] Final preview includes every path and exact content/diff in the pair.
- [ ] Status reporting is always handed off to `$sprint-status`.
- [ ] Next steps never offer `$dev-story` for a non-final-READY story.

---

## Coverage notes

- These cases cover P0 remediation contracts SP-001 through SP-004.
- Durable cross-run readiness receipts, an upstream explicit globally stable
  story-ID field, tracker single-writer/CAS migration across `$dev-story` and
  `$story-done`, shared persisted plan revision/story-set hash, and bounded
  producer finding IDs remain cross-skill follow-up work.
