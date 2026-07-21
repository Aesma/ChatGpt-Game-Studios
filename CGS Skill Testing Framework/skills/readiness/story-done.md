# Skill Test Spec: $story-done

## Skill Summary

$story-done is the sole In Review -> Complete gate. It consumes the staged
$dev-story plan/source/file/test-log handoff, independently revalidates the
$story-readiness provenance contract, binds manual evidence to the current
verification tree or build, and closes only when every required acceptance
criterion and every story-type evidence requirement has a current PASS result.

The P0 contract is fail-closed:

- static presence and keyword checks are findings, never behavioral evidence;
- one missing required criterion blocks closure;
- Visual/Feel, UI, Config/Data, Integration, and Logic evidence requirements are
  all blocking;
- manual evidence requires criterion, tree/build, steps, observation, tester,
  timestamp, and artifact bindings; and
- no user override may convert a required evidence gap into Complete.

---

## Static Assertions (Structural)

Verified by static inspection; no fixture is required.

- [ ] YAML frontmatter contains only name and a non-empty description; name
  matches the skill directory
- [ ] Declares story-done as the sole owner of the Complete transition and
  requires the selected story to be In Review
- [ ] Consumes dev-story plan_hash, source-context hashes, post-write file hashes,
  command/cwd/timestamps/exit code, and raw log SHA-256
- [ ] Computes a deterministic verification_tree_hash from the approved plan and
  current implementation, automated-test, config, and runtime-input hashes
- [ ] Revalidates active TR, Accepted ADR, Manifest Version, Manifest Hash, and
  Source Snapshot instead of trusting prose readiness
- [ ] Preserves STALE / ACCEPTED-RISK and validates the staged manifest waiver
  without relabeling it READY or CURRENT
- [ ] States that file/symbol/number/string searches are findings and cannot mark
  an acceptance criterion PASS, COVERED, or VERIFIED
- [ ] Defaults every acceptance criterion to required
- [ ] Requires every required criterion to be PASS and makes FAIL, UNTESTED,
  DEFERRED, and STALE blocking
- [ ] Allows optional/non-blocking only when declared before the approved
  dev-story plan and bound by unchanged source/profile hashes
- [ ] Makes the required evidence row blocking for every supported Story Type
- [ ] Manual evidence schema includes evidence ID, criterion ID, tested tree
  hash, steps, observed result, PASS, tester, timestamp, and artifact links
- [ ] Invalidates manual evidence after tree/build hash change
- [ ] COMPLETE WITH NOTES cannot contain a required evidence gap
- [ ] BLOCKED has no close-anyway or risk-acceptance override
- [ ] Presents one complete changeset and obtains at most one authorization for
  an unchanged write set

---

## Test Cases

### Case 1: Happy path — current provenance and automated evidence for every required AC

Fixture:

- Story is In Review and the sprint tracker agrees
- Story has two required Logic criteria with stable IDs AC-LIGHT-001 and
  AC-LIGHT-002
- Dev-story handoff contains a valid plan hash, current source hashes, exact
  source/test file post-write hashes, and criterion coverage
- Each criterion maps to a named unit test
- Each test record contains command, cwd, timestamps, exit 0, PASS, and a raw
  log SHA-256
- Current raw file hashes equal the handoff hashes
- Exact active TR, Accepted ADR, current Manifest Version/Hash, and Source
  Snapshot checks pass
- No blocking or advisory finding exists

Expected behavior:

1. Rehashes all handoff paths and authoritative sources
2. Computes verification_tree_hash
3. Marks both required criteria PASS using the direct automated results
4. Marks Logic type evidence PASS
5. Emits COMPLETE
6. Previews the closure write set once
7. After approval, records all hashes/evidence and moves the story/tracker to
   Complete/done

Assertions:

- [ ] COMPLETE is based on direct test results, not test-file existence
- [ ] Completion Record contains plan, tree, source, file, and log hashes
- [ ] The story is not mutated before the approved closable verdict
- [ ] No implementation path is modified during closure

---

### Case 2: SD-001 — file and function exist but behavior test fails

Fixture:

- Logic criterion says damage is clamped to zero
- The expected source file and clamp_damage function both exist
- Keyword search finds the expected function and numeric boundary
- The direct unit test exits 1 and records FAIL
- All unrelated checks pass

Expected behavior:

1. Reports file/function/numeric search only as static findings
2. Marks the criterion FAIL
3. Emits BLOCKED
4. Makes no mutation and offers no completion override

Assertions:

- [ ] Function presence never becomes PASS or VERIFIED
- [ ] The failing behavioral test controls the criterion result
- [ ] COMPLETE WITH NOTES is not offered

---

### Case 3: SD-001 — search match without a test result

Fixture:

- All named implementation files exist
- Test filename and contents contain words similar to the acceptance criterion
- No command result, exit code, or log hash exists for that criterion
- Other criteria pass

Expected behavior:

1. Does not infer direct coverage from names or text similarity
2. Marks the criterion UNTESTED
3. Emits BLOCKED

Assertions:

- [ ] Filename/content similarity is a finding only
- [ ] COVERED is not treated as a passing test result
- [ ] Missing execution evidence blocks closure

---

### Case 4: SD-002 — one required criterion is untested

Fixture:

- Story has four required criteria
- Three have current direct PASS evidence
- One has no current automated or manual result
- The missing share is 25 percent
- All story-type and provenance checks otherwise pass

Expected behavior:

1. Marks the fourth criterion UNTESTED
2. Emits BLOCKED regardless of percentage
3. Does not write completion notes or status

Assertions:

- [ ] There is no 50-percent allowance
- [ ] One missing required criterion blocks
- [ ] COMPLETE WITH NOTES cannot contain the gap

---

### Case 5: SD-002 — predeclared optional criterion may be deferred

Fixture:

- Story has three required criteria and one optional/non-blocking criterion
- The optional classification existed before dev-story approval and is present
  in the unchanged hashed story/Definition-of-Done source and plan coverage
- All required criteria and blocking type evidence PASS
- Optional criterion is DEFERRED

Expected behavior:

1. Preserves required versus optional classification
2. Emits COMPLETE WITH NOTES
3. Names the optional deferred criterion in Completion Notes

Assertions:

- [ ] Optional classification is not created at closure time
- [ ] Runtime user preference cannot downgrade a required criterion
- [ ] Required criteria remain fully passing

---

### Case 6: SD-003 — missing story-type evidence matrix

Run each variant with all acceptance criteria otherwise mapped to some passing
evidence and all provenance checks passing.

| Variant | Story Type | Missing required evidence | Expected |
|---|---|---|---|
| 6a | Logic | passing unit-test evidence | BLOCKED |
| 6b | Integration | integration run or hash-bound end-to-end session | BLOCKED |
| 6c | Visual/Feel | manual session, screenshot/artifact, or required sign-off | BLOCKED |
| 6d | UI | walkthrough/interaction evidence or required sign-off | BLOCKED |
| 6e | Config/Data | smoke-check PASS bound to current tree | BLOCKED |
| 6f | absent/unknown | declared type and evidence contract | BLOCKED |

Assertions:

- [ ] No supported type downgrades missing evidence to advisory
- [ ] Config/Data is not treated as requiring no evidence
- [ ] Missing Story Type cannot close
- [ ] A gate skip does not bypass this matrix

---

### Case 7: SD-003 — evidence file exists but Visual/Feel or UI sign-off is pending

Fixture:

- Evidence document exists and references the story
- It contains current screenshots and a walkthrough
- One required sign-off remains unchecked or unsigned
- Required criteria otherwise pass

Expected behavior:

1. Reports the evidence artifact and pending sign-off
2. Marks story-type evidence BLOCKED
3. Makes no story/status mutation

Assertions:

- [ ] Evidence-file existence alone does not pass
- [ ] Pending sign-off is blocking, not advisory
- [ ] A conversational approval cannot replace the declared sign-off record

---

### Case 8: SD-004 — valid manual record bound to the current tree

Fixture:

- UI criterion AC-UI-003 is permitted to use manual evidence
- Evidence record contains EVID-UI-003, exact criterion ID, the current
  verification_tree_hash, reproducible steps, observed result, explicit PASS,
  tester handle, ISO-8601 timestamp, and artifact links
- Current implementation/evidence hashes match dev-story
- Required UI sign-off is complete

Expected behavior:

1. Validates every record field and exact criterion mapping
2. Confirms tested_tree_hash equals the current tree
3. Marks the criterion and UI type evidence PASS

Assertions:

- [ ] Manual evidence can PASS only with the full record
- [ ] Output includes evidence ID, tester, timestamp, and tree hash
- [ ] Artifact links are retained in the closure record

---

### Case 9: SD-004 — simple confirmation or incomplete manual record

Run variants with unrelated checks passing:

| Variant | Manual input | Expected criterion result |
|---|---|---|
| 9a | User answers Yes — passes | UNTESTED/BLOCKED |
| 9b | Record lacks tester | UNTESTED/BLOCKED |
| 9c | Record lacks timestamp | UNTESTED/BLOCKED |
| 9d | Record lacks steps or observation | UNTESTED/BLOCKED |
| 9e | Record lacks artifact links required by type | UNTESTED/BLOCKED |
| 9f | Record lacks tested tree/build hash | STALE/BLOCKED |
| 9g | Record says Not tested | UNTESTED/BLOCKED |

Assertions:

- [ ] No bare conversational confirmation counts as a manual test
- [ ] Every required identity/session/behavior/hash field is enforced
- [ ] None of the variants can produce COMPLETE WITH NOTES

---

### Case 10: SD-004 — source or build changes invalidate manual evidence

Fixture:

- A complete manual record passed tree hash A
- One implementation file changes after the session, producing current tree B
- Optionally, a recorded packaged build path now hashes differently
- Story remains In Review

Expected behavior:

1. Rehashes the current files/build
2. Reports tested A versus current B
3. Marks dependent manual evidence STALE
4. Emits BLOCKED and requests a new session on the current tree/build

Assertions:

- [ ] Timestamp recency cannot hide a hash mismatch
- [ ] Tester identity cannot override staleness
- [ ] No closure write occurs

---

### Case 11: Dev-story handoff compatibility and fail-closed freshness

Run each variant with acceptance behavior otherwise passing.

| Variant | Handoff condition | Expected |
|---|---|---|
| 11a | plan_hash missing/malformed | BLOCKED |
| 11b | implementation post-write hash differs now | BLOCKED |
| 11c | command/cwd present but log hash missing | BLOCKED |
| 11d | log hash exists but exit code missing | BLOCKED |
| 11e | source-context hash changed | BLOCKED |
| 11f | all required fields and current hashes match | Continue to criterion checks |

Assertions:

- [ ] Story-done consumes the staged field set rather than inventing an
  incompatible handoff
- [ ] A prose dev-story success summary is insufficient
- [ ] Handoff freshness is checked before evidence evaluation

---

### Case 12: Story-readiness and manifest provenance compatibility

Run three variants with all required AC/type evidence passing.

Variant 12a — current:

- Story header version/hash and Source Snapshot match the current raw manifest
- Dev-story source hashes match current sources
- Expected verdict can be COMPLETE

Variant 12b — staged structured accepted risk:

- Story captured hash A
- Dev-story waiver names implemented_against_hash A and current_hash B
- Current manifest still hashes to B
- All non-manifest readiness/source checks pass
- Expected verdict can be COMPLETE WITH NOTES, labeled STALE / ACCEPTED-RISK

Variant 12c — manifest changes again:

- Same waiver names B, but current manifest hashes to C
- Expected verdict is BLOCKED

Assertions:

- [ ] Prior readiness prose never replaces current revalidation
- [ ] Accepted-risk provenance is preserved, not relabeled READY/CURRENT
- [ ] The waiver cannot conceal any non-manifest readiness gap
- [ ] A second manifest change invalidates the branch

---

### Case 13: Story changed after dev-story

Fixture:

- Dev-story handoff was recorded for a particular story/plan
- Acceptance-criterion text or required/optional classification changed later
- Implementation files are unchanged

Expected behavior:

1. Detects story/plan or source inconsistency
2. Does not remap evidence by similar text
3. Emits BLOCKED and routes through revalidation/reimplementation as needed

Assertions:

- [ ] Run-local fallback AC IDs stay bound to the approved plan hash and exact criterion mapping
- [ ] Similar wording does not preserve evidence across a changed criterion
- [ ] Optional status cannot be retrofitted

---

### Case 14: QA/code-review result cannot override evidence blockers

Fixture:

- Full-mode QA says ADEQUATE and code review says APPROVED
- One required AC is UNTESTED or one manual record is STALE

Expected behavior:

1. Records gate results
2. Keeps the evidence blocker
3. Emits BLOCKED

Assertions:

- [ ] Director gates cannot manufacture PASS evidence
- [ ] User acceptance of review risk cannot close the story

---

### Case 15: No-argument selection is bounded to an In Review story

Fixture:

- active.md identifies one In Review story
- Another sprint story is In Progress

Expected behavior:

1. Selects and reads the In Review story
2. Does not attempt to close the In Progress story
3. Confirms ambiguity if multiple In Review stories exist

Assertions:

- [ ] Lifecycle precondition is checked before evidence
- [ ] Non-In-Review state is BLOCKED for closure

---

### Case 16: Optional test-evidence-review receipt keeps quality and execution separate

**Fixture**: Supply exact persisted review/report and manifest paths. Exercise
`ADEQUATE + UNKNOWN`, `ADEQUATE + PASS + TARGETED`, a stale source hash, and the
fully current `COMPLETE/ADEQUATE/PASS/FULL/Closure Eligible YES` combination.

**Expected**:

- [ ] `ADEQUATE` alone never proves execution or closure
- [ ] Targeted, unknown, stale, unavailable, incomplete, or hash-invalid review evidence blocks closure
- [ ] Every underlying QA/story/build/test/smoke/playtest/manual/attestation hash is revalidated
- [ ] A valid review remains a summary; per-criterion evidence checks still apply

### Case 17: Closure updates the revisioned tracker atomically

- [ ] Invalid sprint identity/revision/story-set hash blocks closure
- [ ] Complete story, done tracker, and session projection share one closure transaction ID
- [ ] Story-byte change recomputes sorted `ID<TAB>path<TAB>raw-hash` story_set_hash
- [ ] plan_revision remains unchanged and updated_at is timezone-qualified
- [ ] CAS/write/read-back failure cannot report closure success

## Verdict Matrix

| Condition | COMPLETE | COMPLETE WITH NOTES | BLOCKED |
|---|---:|---:|---:|
| Every required AC has current PASS evidence | required | required | false/missing |
| Story-type evidence complete | required | required | false/missing |
| Current file/source/tree bindings | required | required, except valid manifest accepted-risk branch | stale/invalid |
| Required AC deferred/untested/failed | never | never | yes |
| Optional predeclared AC deferred | no | allowed | no |
| Valid STALE / ACCEPTED-RISK manifest waiver | no | allowed | invalid/changed |
| Advisory review finding only | no | allowed | no |
| Blocking deviation/gate | no | no | yes |

There is no percentage threshold and no close-anyway branch.

---

## Protocol Compliance

- [ ] Reads the full story before delegation or mutation
- [ ] Uses raw SHA-256 bindings for story, source, implementation, evidence,
  tree/build, and test logs
- [ ] Does not treat file existence, static search, or names as behavior
- [ ] Lists every required AC with evidence IDs, freshness, and result
- [ ] Enforces type evidence as blocking for all five types
- [ ] Uses structured manual records, not direct confirmations
- [ ] Makes stale evidence blocking
- [ ] Presents the complete report before the one closure authorization
- [ ] Writes nothing for BLOCKED
- [ ] Never permits a required-gap override
- [ ] Preserves accepted-risk provenance in report and closure
- [ ] Does not commit, push, publish, or run follow-on workflows automatically

---

## Coverage Notes

These cases fully exercise SD-001, SD-002, SD-003, and SD-004 and their
no-bypass paths. They also cover compatibility with the staged dev-story
plan/source/post-write/test-log handoff and the staged story-readiness manifest
provenance model.

Still outside this P0 candidate:

- standardized cross-skill evidence-file and test-manifest schemas;
- mandatory QA GAPS handling and risk-based code-review policy;
- atomic multi-artifact closure with compare-and-swap recovery;
- a single shared stable ID registry for AC/Test/Evidence/Finding records; and
- catalog/workflow-guide/source-skill migration.
