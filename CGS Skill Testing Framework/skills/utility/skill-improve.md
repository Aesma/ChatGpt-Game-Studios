# Skill Test Spec: $skill-improve

## Skill Summary

`$skill-improve` is a multi-task protocol: an independent owner freezes an
acceptance oracle, an author stages target-local candidate bytes outside the live
skill, a separate verifier evaluates the candidate against the frozen oracle, and
a separate integrator applies only a verified candidate using all-file CAS.
Candidate changes cannot edit their own spec/catalog/rubric/runner. Recovery uses
recorded hash-guarded patches and never restores saved full contents.

No test in this specification executes `$skill-improve` or `$skill-test` during
static acceptance.

---

## Static Assertions

- [ ] SI-S001: Frontmatter contains only `name` and non-empty `description`;
  `name` is `skill-improve`.
- [ ] SI-S002: Invocation exposes explicit `freeze`, `stage`, `verify`,
  `apply`, `recover`, and read-only `status` modes.
- [ ] SI-S003: Oracle owner, candidate author, verifier, integrator, and recovery
  owner have explicit task-separation rules.
- [ ] SI-S004: Oracle lock is created before candidate work and freezes target,
  acceptance, spec, catalog, rubric, runner, scenarios, receipts, and impact
  hashes.
- [ ] SI-S005: Candidate mutation scope is target-local and explicitly excludes
  spec, catalog, rubric, runner, templates, acceptance/oracle, callers/callees,
  shared schemas/docs, and other skills.
- [ ] SI-S006: Legitimate oracle changes require an independent owner receipt,
  a new lock, old/new oracle identity, and dual-oracle results.
- [ ] SI-S007: A green new oracle cannot hide a non-waived old safety or
  authorization regression.
- [ ] SI-S008: Verification requires candidate-aware isolated execution and full
  command/exit/time/tool/environment/output evidence; otherwise NOT_RUN.
- [ ] SI-S009: Improvement is severity/scenario based; counts, percentages, and
  aggregate scores cannot offset new P0/P1 or safety regressions.
- [ ] SI-S010: Candidate staging never edits live target files.
- [ ] SI-S011: Apply performs all-file preflight CAS against frozen base hashes
  and blocks all writes on any concurrent change.
- [ ] SI-S012: Recovery uses canonical forward/inverse patches whose preimages
  must match; it never restores saved full file contents.
- [ ] SI-S013: A DIVERGED or post-failure changed file blocks recovery and
  preserves the external edit.
- [ ] SI-S014: Successful application is not automatically rolled back after a
  later regression.
- [ ] SI-S015: Workflow, oracle, candidate, test, eligibility, mutation,
  persistence, and verdict axes are explicit.
- [ ] SI-S016: Immutable run artifacts have stable IDs, exact paths/hashes, and
  are never selected by latest/mtime.
- [ ] SI-S017: Catalog result recording and shared-contract changes are separate
  owner responsibilities after application.
- [ ] SI-S018: Metadata describes frozen-oracle staging and CAS application
  without a truncated score-loop description.

---

### Case 1: Oracle is frozen before candidate authoring

**Fixture:**

- Exact target skill, metadata, registered spec/catalog/rubric, runner, fixtures,
  acceptance manifest, and impact graph are readable.
- Baseline suites produce complete execution receipts.
- No oracle-lock path exists.
- Oracle-owner task is independent from later author/verifier/integrator tasks.

**Input:**

`$skill-improve freeze --run-id SI-run-001 --skill sample-skill --acceptance production/skill-acceptance/sample-001.md`

**Expected writes:**

- Exactly `.codex/skill-improve-runs/SI-run-001/oracle-lock.md` after bounded
  authorization.

**Expected non-writes:**

- Target skill/metadata, registered spec, catalog, rubric, runner, templates,
  candidate files, shared schemas, and callers/callees.

**Expected behavior:**

1. Resolves exact target/oracle/impact paths and hashes.
2. Runs all required baseline scenarios and verifies complete receipts.
3. Assigns stable requirement/finding IDs and severities.
4. Writes/re-reads one immutable lock with `Oracle Status: FROZEN`.
5. Does not claim baseline green means no improvement is needed when runtime or
   impact coverage is incomplete.

**Assertions:**

- [ ] SI-C01-A: Oracle predates every candidate.
- [ ] SI-C01-B: Acceptance scenarios and safety requirements are immutable.
- [ ] SI-C01-C: Missing execution fields produce NOT_RUN/PARTIAL.
- [ ] SI-C01-D: Only the lock file is written.

---

### Case 2: Candidate cannot weaken its own oracle

**Fixture:**

- Frozen oracle requires authorization assertion `AUTH-007`.
- Proposed candidate edits target SKILL.md and also tries to delete AUTH-007 from
  the behavioral spec/catalog.
- Under the weakened spec, all candidate tests would be green.

**Input:**

Run `stage` and `verify` with the proposal.

**Expected writes:**

- No candidate is created for the mixed mutation set, or a target-local candidate
  is rejected before eligibility.
- No live target or oracle file changes.

**Expected behavior:**

1. Detects spec/catalog paths outside candidate ownership.
2. Returns `BLOCKED — SEPARATE OWNER CHANGE REQUIRED`.
3. Does not execute a weakened self-authored oracle as proof.
4. Keeps AUTH-007 in the frozen oracle.
5. Apply Eligible remains NO even if a hypothetical new suite is green.

**Assertions:**

- [ ] SI-C02-A: Implementation and oracle cannot share a candidate changeset.
- [ ] SI-C02-B: Deleting a constraint cannot self-certify improvement.
- [ ] SI-C02-C: Spec/catalog remain byte-identical.
- [ ] SI-C02-D: Green weakened tests have no acceptance authority.

---

### Case 3: Legitimate spec revision uses dual-oracle verification

**Fixture:**

- Independent spec owner has an authorized immutable oracle-change receipt.
- New oracle intentionally changes one behavioral requirement and retains all
  safety/authorization requirements.
- Prior lock and old oracle bytes are available.
- Candidate is staged only after the new lock is frozen.

**Input:**

Freeze with `--prior-lock` and `--oracle-change`, then independently verify the
candidate.

**Expected writes:**

- New immutable oracle lock and later candidate/verification artifacts under
  distinct unused paths.
- No oracle file is edited by the candidate.

**Expected behavior:**

1. Validates old/new requirement IDs, hashes, rationale, owner, approvals, impact,
   and explicit waivers.
2. Runs candidate against both old and new oracle suites.
3. Reports separate old/new results.
4. Rejects any non-waived old safety/authorization regression.
5. Does not erase old-oracle evidence when the new suite passes.

**Assertions:**

- [ ] SI-C03-A: Oracle change ownership is independent.
- [ ] SI-C03-B: Dual-oracle results are visible.
- [ ] SI-C03-C: Legacy safety removal requires explicit owner waiver.
- [ ] SI-C03-D: Candidate never authors its judge.

---

### Case 4: Concurrent target edit blocks stage or apply without overwrite

**Fixture:**

- Lock records target SKILL hash A and metadata hash M.
- Another agent legitimately changes SKILL to hash B after freeze.
- Variant A attempts `stage`.
- Variant B uses an already verified A-based candidate and attempts `apply`.

**Input:**

Run both variants with exact lock/candidate paths.

**Expected writes:**

- None to live target.
- At most an immutable BLOCKED receipt at an authorized unused run-evidence path.

**Expected behavior:**

1. Re-reads current live hashes before every mutation phase.
2. Variant A returns `BLOCKED — CONCURRENT TARGET CHANGE; NEW ORACLE REQUIRED`.
3. Variant B fails all-file CAS with
   `BLOCKED — CONCURRENT CHANGE` before writing any path.
4. Preserves B exactly and does not restore A.
5. Requires a new oracle from current bytes.

**Assertions:**

- [ ] SI-C04-A: CAS compares raw current bytes to frozen preimages.
- [ ] SI-C04-B: One mismatch blocks the whole target mutation set.
- [ ] SI-C04-C: External edits are never overwritten.
- [ ] SI-C04-D: Saved originals are not used for recovery.

---

### Case 5: Recovery refuses to overwrite a post-failure external edit

**Fixture:**

- A two-file application was interrupted: SKILL is at candidate hash C while
  metadata remains at base hash M.
- Failed application receipt records exact forward/inverse patches and hashes.
- Another agent then edits SKILL from C to divergent hash D.
- Recovery requests `--direction reverse`.

**Input:**

`$skill-improve recover --application <failed-receipt> --direction reverse --recovery-id REC-005`

**Expected writes:**

- No target write and no overwritten external change.
- Optional immutable BLOCKED recovery receipt at its authorized path.

**Expected behavior:**

1. Classifies SKILL as DIVERGED and metadata as BASE.
2. Fails all-file recovery CAS before applying any inverse hunk.
3. Returns `BLOCKED — CONCURRENT RECOVERY CHANGE`.
4. Preserves D and M byte-for-byte.
5. Routes to explicit human three-way recovery; never copies saved original text.

**Assertions:**

- [ ] SI-C05-A: Recovery preimages are direction-specific.
- [ ] SI-C05-B: DIVERGED blocks all recovery writes.
- [ ] SI-C05-C: Concurrent work is preserved.
- [ ] SI-C05-D: No repository reset or snapshot restore occurs.

---

### Case 6: Happy path stages, verifies, and applies once

**Fixture:**

- Frozen oracle and impact graph are complete/current.
- Candidate changes only authorized target-local files.
- Candidate-aware runner tests the isolated mirror.
- Every targeted finding is resolved, all user acceptance scenarios pass, no
  non-targeted or safety regression exists, and verification receipt persists.
- Live target still matches every base hash.
- Integrator task is independent and exact apply path is authorized.

**Input:**

Run `stage`, independent `verify`, then independent `apply`.

**Expected writes:**

- Immutable candidate files/manifest/patches.
- Immutable verification receipt.
- On apply, exactly the authorized live target paths and one application receipt.

**Expected behavior:**

1. Candidate stage leaves live target unchanged.
2. Verification returns VERIFIED/PASS/Apply Eligible YES and
   `VERIFIED_IMPROVEMENT`.
3. Apply revalidates all hashes and publishes verified postimages.
4. Returns APPLIED/PASS/Mutation APPLIED/Verdict APPLIED.
5. Consumes apply eligibility and stops before catalog updates or another run.

**Assertions:**

- [ ] SI-C06-A: All task roles are independent.
- [ ] SI-C06-B: Every target path passes CAS before publication.
- [ ] SI-C06-C: Applied bytes equal verified candidate hashes.
- [ ] SI-C06-D: No automatic chained workflow occurs.

---

### Case 7: New P0 cannot be offset by many removed warnings

**Fixture:**

- Baseline has five P2/P3 warnings.
- Candidate resolves all five but introduces one authorization P0.
- Aggregate failure/warning count decreases.
- All execution receipts are conclusive.

**Input:**

Run `verify`.

**Expected writes:**

- Immutable rejection verification receipt only.

**Expected behavior:**

1. Compares stable requirement IDs and severity, not aggregate score.
2. Reports the five resolutions and new P0 separately.
3. Returns REJECTED/FAIL/Apply Eligible NO.
4. Does not label the candidate improved.

**Assertions:**

- [ ] SI-C07-A: Severity precedence is deterministic.
- [ ] SI-C07-B: New P0/P1 always blocks verified improvement.
- [ ] SI-C07-C: Score reduction is supporting data only.

---

### Case 8: Missing execution provenance is NOT_RUN

**Fixture:**

Use variants where a baseline or candidate receipt lacks command/argv, exit code,
timestamps, runner hash, environment, assertion results, or stdout/result hashes.

**Input:**

Run `freeze` or `verify`.

**Expected writes:**

- Optional immutable PARTIAL/NOT_RUN evidence receipt; no eligible candidate or
  live target mutation.

**Expected behavior:**

1. Names each missing execution field.
2. Returns Test Status NOT_RUN or PARTIAL and Apply Eligible NO.
3. Never converts an empty/zero-count result to PASS.
4. Does not continue to apply.

**Assertions:**

- [ ] SI-C08-A: Execution evidence is reproducible.
- [ ] SI-C08-B: Unavailable tests are first-class blockers.
- [ ] SI-C08-C: Static green text alone is insufficient.

---

### Case 9: Green legacy suite with coverage gaps does not end analysis early

**Fixture:**

- Existing static/category checks pass.
- Acceptance manifest requires runtime authorization ordering, timeout, recovery,
  and side-effect scenarios not covered by that suite.
- Required runtime runner is unavailable.

**Input:**

Run `freeze`.

**Expected writes:**

- Optional immutable oracle lock clearly marked PARTIAL/NOT_RUN.

**Expected behavior:**

1. Detects missing required runtime coverage despite green legacy results.
2. Returns Apply Eligible NO.
3. Does not say "no improvement needed" solely because old checks pass.
4. Names the missing scenarios and owner/tool needed.

**Assertions:**

- [ ] SI-C09-A: Oracle completeness is independent of baseline pass count.
- [ ] SI-C09-B: Runtime/tool-side effects require actual evidence.
- [ ] SI-C09-C: Partial oracle cannot approve a candidate.

---

### Case 10: Shared-schema impact remains a separate owner change

**Fixture:**

- Candidate proposal changes a status enum consumed by three direct callers and
  one shared schema.
- Impact graph identifies all consumers and owners.
- Only the target skill directory is authorized.

**Input:**

Run `stage`.

**Expected writes:**

- None, unless a target-local candidate excluding the incompatible contract
  change remains meaningful and independently authorized.

**Expected behavior:**

1. Lists every direct caller/schema/owner and hash.
2. Returns `BLOCKED — SEPARATE OWNER CHANGE REQUIRED` for the shared change.
3. Does not edit caller specs, catalog, or schemas.
4. Requires independent owner approval and a new oracle if the contract changes.

**Assertions:**

- [ ] SI-C10-A: Impact scope is not guessed by the candidate author.
- [ ] SI-C10-B: Shared changes cannot hitchhike on target authorization.
- [ ] SI-C10-C: Candidate is not partially staged as falsely complete.

---

### Case 11: Runner unable to test isolated candidate cannot swap live files

**Fixture:**

- Frozen runner resolves only `.agents/skills/<name>` and cannot accept a
  candidate manifest/root.
- Candidate is otherwise structurally valid.
- Replacing live target temporarily would make the runner work.

**Input:**

Run `verify`.

**Expected writes:**

- Verification receipt with NOT_RUN, if authorized.
- No live target swap or installation.

**Expected behavior:**

1. Refuses to replace live files for testing.
2. Returns Candidate STAGED, Test NOT_RUN, Apply Eligible NO, Verdict BLOCKED.
3. Names candidate-aware runner support as the required next action.
4. Leaves candidate and target hashes unchanged.

**Assertions:**

- [ ] SI-C11-A: Verification isolation is mandatory.
- [ ] SI-C11-B: Test convenience cannot cross mutation boundaries.
- [ ] SI-C11-C: NOT_RUN never becomes success.

---

### Case 12: Later regression after successful apply starts a new run

**Fixture:**

- Prior application completed and receipt verifies APPLIED.
- Later unrelated work changed the target.
- A newly discovered regression suggests returning to older behavior.

**Input:**

Request automatic rollback from the old run.

**Expected writes:**

- None.

**Expected behavior:**

1. Rejects automatic rollback after successful application.
2. Does not apply the old inverse patch to changed current bytes.
3. Requires a new improvement run from current hashes or a separate explicitly
   authorized patch workflow.
4. Preserves current work.

**Assertions:**

- [ ] SI-C12-A: Recovery is for recorded partial application, not later regret.
- [ ] SI-C12-B: Historical inverse patches have no authority over current bytes.
- [ ] SI-C12-C: External changes remain intact.

---

## Cross-skill compatibility assertions

- [ ] SI-X001: Candidate-aware `skill-test` execution must consume an exact
  candidate manifest/root and emit full execution receipts; absent support yields
  NOT_RUN.
- [ ] SI-X002: Catalog and behavioral-spec owners remain independent oracle
  owners and are never mutated by the candidate under test.
- [ ] SI-X003: Catalog run-evidence recording happens only after APPLIED and in a
  separate recorder task.
- [ ] SI-X004: Shared callers/callees/schemas receive explicit impact handoffs,
  not edits under target-skill authorization.
- [ ] SI-X005: Application/recovery uses explicit patches and CAS rather than
  repository reset or snapshot copying.
- [ ] SI-X006: Skill, metadata, and spec use the same modes, paths, roles, status
  axes, oracle rules, eligibility criteria, and recovery boundaries.
