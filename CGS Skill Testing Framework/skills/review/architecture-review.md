# Skill Test Spec: $architecture-review

## Skill Summary

$architecture-review is a formal, hash-bound architecture and ADR traceability
gate. It reviews only explicit owner-approved requirements and exact
Requirement → ADR → Story → Test Run evidence against a complete target
manifest. Its verdict is exactly PASS, BLOCKED, or PARTIAL.

The skill is read-only by default. With explicit approval it may create one new
immutable review report at one exact path. It never modifies GDDs, ADRs,
requirements, registries, indexes, stories, tests, test results, logs, signoff,
accepted-risk records, or session state.

The skill does not perform the separate eight-section architecture-document
completeness review.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only name and a non-empty description; name
  matches the skill directory
- [ ] Public modes are exactly full, coverage, consistency, engine, single-gdd
  with a canonical project-relative path, and rtm
- [ ] Verdict vocabulary is exactly PASS, BLOCKED, and PARTIAL
- [ ] Invalid mode/target returns ERROR with no verdict
- [ ] Default allowed write set is empty
- [ ] The only optional write is one exact, new, explicitly approved immutable
  report path
- [ ] Explicitly prohibits changes to GDD/ADR/TR, registries, systems index,
  traceability index, session state, logs, signoff, stories, tests, test results,
  and accepted-risk records
- [ ] Defines before/after SHA-256 mutation guard
- [ ] Requires a complete target manifest and target_manifest_hash
- [ ] Requires owner identity, approval status/timestamp, source path, and
  matching source revision/hash before admitting a requirement
- [ ] Classifies inferred prose as CANDIDATE_REQUIREMENT and never allocates an ID
- [ ] Requires exact requirement IDs for ADR/story/test links
- [ ] Classifies implicit links as UNVERIFIED_LINK
- [ ] Treats test file existence as DISCOVERED_NOT_EXECUTED, not passing evidence
- [ ] Requires immutable run ID, result, timestamp, test hash, linked IDs, and
  matching source revision/manifest for EXECUTED_PASS
- [ ] Any manifest change makes a prior report STALE
- [ ] ACCEPTED_RISK remains separate and cannot convert a verdict to PASS
- [ ] Full mode uses technical-director and lead-programmer as parallel,
  read-only reviewers; reviewer failure prevents PASS
- [ ] Ends with one destination-owner handoff and stops without invoking it

---

## Contract Cases

### Case 1: Happy path — current explicit evidence returns PASS

Fixture:

- All target inputs are listed in a canonical manifest with complete-file SHA-256
- Every source GDD contains a stable requirement ID verbatim
- Each lifecycle record preserves immutable source text, matches the GDD
  path/hash, is active, and has owner identity, approval status, and timestamp
- Every requirement has an exact link from a current usable ADR
- Stories and tests, where required, name the exact requirement and ADR/story IDs
- Latest authoritative test-run records have immutable run IDs, EXECUTED_PASS,
  execution timestamps, matching test hashes, and the same source revision or
  target_manifest_hash
- Engine evidence matches the pinned VERSION.md
- No conflicts, dependency cycles, gaps, unknown evidence, or mutations exist
- In full mode, technical-director and lead-programmer both return DONE against
  the same target_manifest_hash

Input: $architecture-review full

Expected behavior:

1. The complete ordered manifest and target_manifest_hash are shown.
2. Only explicit owner-approved requirements enter the baseline.
3. Exact links and current run records are VERIFIED_COVERED / EXECUTED_PASS.
4. Both full-mode reviewers run in parallel and make no file changes.
5. The final mutation guard passes.
6. Verdict: PASS.

Assertions:

- [ ] PASS is emitted only after every mandatory condition succeeds
- [ ] Report includes the full path/hash manifest, not only file counts
- [ ] No project file changes
- [ ] No legacy verdict appears

### Case 2: Mutation guard — unauthorized change blocks the gate

Fixture:

- A baseline snapshot exists for every project file outside .git
- During review, any GDD, ADR, registry, systems index, traceability index,
  consistency log, signoff, or session-state file changes

Input: $architecture-review coverage

Expected behavior:

1. The final snapshot detects every added, deleted, or changed unauthorized path.
2. mutation_guard is FAILED and names each path.
3. Verdict: BLOCKED.
4. The reviewer does not hide, repair, or automatically revert the change.

Assertions:

- [ ] Any unauthorized mutation prevents PASS
- [ ] The reviewer never writes or reconciles truth sources
- [ ] Automatic rollback is not attempted

Optional report subcase:

- [ ] With explicit approval, exactly one new report path is allowed
- [ ] A pre-existing report path is rejected rather than overwritten/appended
- [ ] Any second changed path still returns BLOCKED
- [ ] Saved report bytes are re-read and their SHA-256 is returned

### Case 3: Inferred prose is not an approved requirement

Fixture:

- A GDD sentence implies a possible technical constraint
- It has no stable ID, matching source-bound lifecycle record, or explicit owner
  approval

Input: $architecture-review coverage

Expected behavior:

1. The sentence is excluded from the approved requirement baseline.
2. A CANDIDATE_REQUIREMENT finding records exact source evidence and missing
   approval/provenance.
3. No TR ID is allocated or reused.
4. No registry text, lifecycle, or status changes.
5. Verdict: PARTIAL when no separate blocker exists.

Assertions:

- [ ] Fuzzy/near/semantic text matching never creates coverage
- [ ] Candidate prose cannot become VERIFIED_COVERED
- [ ] Registry remains byte-identical

### Case 4: Implicit ADR and file existence are unverified

Fixture:

- An ADR discusses the same topic as a requirement but does not name its exact ID
- A story states a test path and the test file exists
- There is no authoritative current test-run record

Input: $architecture-review rtm

Expected behavior:

1. ADR evidence is UNVERIFIED_LINK, not VERIFIED_COVERED.
2. Test evidence is DISCOVERED_NOT_EXECUTED, not EXECUTED_PASS.
3. The chain is incomplete.
4. Verdict: PARTIAL when no confirmed blocker exists.

Assertions:

- [ ] A GDD/system-name mention is not an exact requirement link
- [ ] Implicit coverage never raises the coverage count
- [ ] Existing test files are never described as passing tests
- [ ] PARTIAL, not PASS, is emitted

### Case 5: Test-run evidence truth table

Use otherwise PASS-ready rtm fixtures.

Subcase A — current pass:

- Latest authoritative run matches test hash and target revision/hash and reports
  PASS.
- Expected: EXECUTED_PASS; it may contribute to PASS.

Subcase B — stale pass:

- A pass record exists but names an older source revision, target manifest, or
  test content hash.
- Expected: STALE_RUN and PARTIAL, never PASS.

Subcase C — current failure:

- Latest authoritative matching run reports FAIL.
- Expected: EXECUTED_FAIL and BLOCKED.

Subcase D — missing run:

- The test source exists but no authoritative run record exists.
- Expected: DISCOVERED_NOT_EXECUTED and PARTIAL.

Assertions:

- [ ] Only Subcase A counts as passing evidence
- [ ] Run ID, result, timestamp, test hash, linked IDs, and revision/hash are all
  required
- [ ] A stale or missing run never becomes covered through file existence

### Case 6: Hash staleness and accepted risk preserve verdict history

Fixture:

- A saved report records PASS or BLOCKED for target manifest hash H1
- One target input changes, producing H2
- Optionally, a separate owner-signed ACCEPTED_RISK record references selected
  findings for H1

Expected behavior:

1. Rebuilding the manifest produces H2 and marks the report STALE.
2. The old report has no current gate value.
3. The reviewer does not edit or relabel the old report.
4. ACCEPTED_RISK is validated separately by report ID, finding IDs, scope, hash,
   owner signature, timestamp, and expiry.
5. Accepted risk never converts BLOCKED/PARTIAL to PASS and is invalid for H2.

Assertions:

- [ ] Any input/scope/hash change invalidates current gate use
- [ ] No vague latest-report selection is used
- [ ] Risk disposition and gate verdict remain separate

### Case 7: Missing or ambiguous target produces no verdict

Fixture:

- single-gdd target is missing, outside the project, or a title matching multiple
  files; or the mode is unknown

Expected behavior:

1. The exact invalid input is named.
2. Output is ERROR.
3. No PASS, BLOCKED, or PARTIAL verdict is produced.
4. No report or project file is written.

### Case 8: Contract boundary — architecture document template review is separate

Fixture:

- Input asks this skill to approve architecture.md solely by counting eight
  required document sections

Expected behavior:

1. The skill explains that section-template grading is a separate
   architecture-document-review concern.
2. It does not emit APPROVED, NEEDS REVISION, or MAJOR REVISION NEEDED.
3. It does not reinterpret section presence as traceability PASS.
4. It makes no file changes.

---

## Protocol Compliance

- [ ] Conversational review changes zero files
- [ ] Optional save creates only one approved immutable report
- [ ] Complete manifest/hash precedes evidence conclusions
- [ ] Only explicit owner-approved IDs enter the baseline
- [ ] Exact links and actual current test-run evidence are mandatory
- [ ] Verdict precedence is confirmed blocker → BLOCKED; otherwise incomplete or
  unknown evidence → PARTIAL; otherwise complete current evidence → PASS
- [ ] Mutation guard runs immediately before return
- [ ] Accepted risk cannot rewrite verdicts
- [ ] One owner-directed handoff is returned and not invoked

---

## Coverage Notes

This specification intentionally replaces the former eight-section document
review and APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED vocabulary. A
separate architecture-document-review skill/spec is required if that workflow is
retained. Shared catalog entries and downstream gate callers must be migrated
separately; they are outside this skill-owned changeset.
