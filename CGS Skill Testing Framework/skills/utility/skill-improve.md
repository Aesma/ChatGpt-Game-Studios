# Skill Improve Spec: `$skill-improve`

> **Spec ID**: skill-improve-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$skill-improve` exposes separate `freeze`, `stage`, `verify`, `apply`,
`recover`, and read-only `status` modes. Distinct oracle owner, candidate author,
verifier, integrator, and recovery-owner tasks preserve independence.

**Owned outputs:** immutable run evidence under
`.codex/skill-improve-runs/{run-id}/`; only a verified `apply` or hash-guarded
`recover` may mutate exact target-local paths under
`.agents/skills/{skill-name}/`.

**Non-writes:** registered spec, catalog, rubric, skill-test rules/runner/
manifest/receipts, frozen acceptance/oracle evidence, callers, callees, shared
schemas/docs, and unrelated skills.

**Workflow vocabulary:** `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR`.

**Test vocabulary:** `PASS`, `FAIL`, `PARTIAL`, `NOT_RUN`, `STALE`,
`NOT_APPLICABLE`.

**Evidence classification:** `IMPROVEMENT`, `NO_CHANGE_REQUIRED`,
`NO_IMPROVEMENT`, `TEST_NOISE`, `ENVIRONMENT_CHANGED`, `REGRESSION`,
`INCONCLUSIVE`.

**Verdicts:** `ORACLE_FROZEN`, `CANDIDATE_STAGED`, `VERIFIED_IMPROVEMENT`,
`NO_CHANGE_REQUIRED`, `NO_IMPROVEMENT`, `TEST_NOISE`,
`ENVIRONMENT_CHANGED`, `REGRESSION`, `REJECTED`, `APPLIED`, `BLOCKED`,
`ERROR`.

The candidate never edits its judge, testing never swaps candidate bytes into
the live package, and recovery never restores saved full contents.

---

## Static Assertions

- [ ] **[SI-SA-001]** Frontmatter has exactly non-empty `name` and
  `description`; name is `skill-improve`.
- [ ] **[SI-SA-002]** A normative `cgs-skill-contract/v1` manifest defines all
  modes, writes, non-writes, states, and evidence classifications.
- [ ] **[SI-SA-003]** Oracle, candidate, verifier, integrator, recovery, and
  oracle-change ownership are separate.
- [ ] **[SI-SA-004]** Candidate scope is target-local and excludes all testing
  authorities and shared contracts.
- [ ] **[SI-SA-005]** Skill-test receipts require v2 schema, dependency
  freshness `CURRENT`, and exact partial/invalid/stale mapping.
- [ ] **[SI-SA-006]** Written-contract evidence cannot prove runtime,
  authorization ordering, side effects, timeout, recovery, or concurrency.
- [ ] **[SI-SA-007]** Improvement uses stable scenarios and severity, never
  warning/failure counts alone.
- [ ] **[SI-SA-008]** Candidate/apply evidence binds raw source, candidate,
  patch, full diff, tool, environment, and observed hashes.
- [ ] **[SI-SA-009]** Apply and recovery use all-file CAS and never overwrite a
  diverged path.
- [ ] **[SI-SA-010]** Recovery evidence has an explicit location, retention
  rule, and manual conflict procedure.
- [ ] **[SI-SA-011]** No mode auto-chains into skill-test, catalog updates,
  another improvement run, commit, or publication.

---

## Test Cases

### Case 1 [SI-C01]: Freeze binds current skill-test and impact evidence

#### Fixture

- An independently approved acceptance manifest identifies the target,
  objective, severity taxonomy, scenarios, runner identities, and owners.
- Current `cgs-skill-test-rules/v1` and validator manifest hashes match.
- A supplied `cgs-skill-test-receipt/v2` rehashes to freshness `CURRENT`.
- Impact discovery completes within its frozen budget.

#### Input

`$skill-improve freeze --run-id SI-001 --skill sample-skill --acceptance manifests/SI-001.json`

#### Expected reads

- Target-local files, catalog entry, registered spec, rubric, templates,
  skill-test rules/manifest/receipt dependencies, acceptance manifest, runners,
  fixtures, and complete impact surface.

#### Expected writes

- Exactly `.codex/skill-improve-runs/SI-001/oracle-lock.md` after authorization.

#### Expected non-writes

- Target, spec, catalog, rubric, skill-test authorities/receipts, acceptance
  manifest, shared contracts, and candidate paths.

#### Expected behavior

1. Validates skill-test receipt schema, content hash, all dependencies, and
   freshness before treating it as evidence.
2. Records selected/loaded/failed/omitted/excluded impact ledger and stable
   caller/callee/schema edges with source lines.
3. Freezes source, authority, runner, environment, scenario, receipt, and graph
   hashes before candidate work.
4. Re-hashes before writing and read-backs the immutable lock.
5. Returns `ORACLE_FROZEN`, Apply Eligible `NO`.

#### Assertions

- [ ] **[SI-C01-A01]** No target or oracle bytes change.
- [ ] **[SI-C01-A02]** Receipt freshness is hash-based, not date-based.
- [ ] **[SI-C01-A03]** Every impact edge has evidence and an owner.
- [ ] **[SI-C01-A04]** Missing impact or receipt coverage is not hidden.

#### Case Verdict

`PASS` when one verified lock binds all current evidence; `PARTIAL` when a
required read/coverage ledger is incomplete; otherwise `FAIL`.

---

### Case 2 [SI-C02]: Green written-contract evidence does not prove runtime safety

#### Fixture

- Baseline skill-test receipt is `CURRENT` and validation is `COMPLIANT`.
- Acceptance requires runtime authorization ordering, tool side-effect,
  timeout, recovery, and concurrency scenarios.
- The runtime runner is unavailable.

#### Input

Run `freeze` for the target.

#### Expected reads

- Current skill-test receipt, acceptance scenarios, runner manifest, and
  environment/tool identity.

#### Expected writes

- At most one authorized oracle lock marked incomplete.

#### Expected non-writes

- Target, skill-test receipt, candidate, catalog, and shared artifacts.

#### Expected behavior

1. Maps COMPLIANT only to written-contract scenario rows.
2. Marks unavailable runtime rows `NOT_RUN`.
3. Returns Test Status `NOT_RUN` or `PARTIAL`, classification `INCONCLUSIVE`,
   Apply Eligible `NO`, and `BLOCKED`.
4. Does not stop analysis as `NO_CHANGE_REQUIRED` merely because static checks
   are green.

#### Assertions

- [ ] **[SI-C02-A01]** Evidence classes are not interchangeable.
- [ ] **[SI-C02-A02]** Missing runtime proof blocks application.
- [ ] **[SI-C02-A03]** Static green cannot erase an open safety objective.

#### Case Verdict

`PASS` when missing runtime evidence blocks eligibility; otherwise `FAIL`.

---

### Case 3 [SI-C03]: A new P0 cannot be traded for removed lower findings

#### Fixture

- Baseline has five P2/P3 findings with stable IDs.
- Candidate resolves all five but introduces one authorization P0.
- Every required suite executes conclusively under the frozen environment.

#### Input

Run independent `verify`.

#### Expected reads

- Frozen oracle, stable scenario/finding set, baseline receipts, candidate,
  candidate receipts, severity taxonomy, and impact approvals.

#### Expected writes

- One immutable rejection verification receipt after authorization.

#### Expected non-writes

- Live target, candidate, oracle, spec, catalog, rubric, and shared contracts.

#### Expected behavior

1. Compares stable IDs, severity, and scenarios rather than aggregate counts.
2. Reports five resolutions and the new P0 independently.
3. Classifies `REGRESSION`, Test Status `FAIL`, Apply Eligible `NO`, verdict
   `REGRESSION`/`REJECTED`.
4. Never reports `VERIFIED_IMPROVEMENT`.

#### Assertions

- [ ] **[SI-C03-A01]** Severity precedence is deterministic.
- [ ] **[SI-C03-A02]** New P0/P1 and safety failures are non-offsettable.
- [ ] **[SI-C03-A03]** Counts remain supporting data only.

#### Case Verdict

`PASS` when the new P0 rejects the candidate; otherwise `FAIL`.

---

### Case 4 [SI-C04]: Shared-contract impact requires every direct owner

#### Fixture

- Proposed target change alters a status token consumed by three skills, two
  specs, one shared schema, and metadata.
- One consumer lies below a nested skill directory.
- Impact budget is complete and current.

#### Input

Run `freeze`, then attempt `stage` with only target-local authorization.

#### Expected reads

- Canonically discovered skills/specs/catalog/shared docs, exact token/path
  references, metadata, and skill-test discovery rules.

#### Expected writes

- Oracle lock only if freeze completes; no misleading partial candidate.

#### Expected non-writes

- All consumers, specs, schema, metadata, target, catalog, and candidate path.

#### Expected behavior

1. Reports every direct edge with stable ID, path, line, hash, and owner.
2. Nested consumers are not omitted.
3. Returns `BLOCKED — SEPARATE OWNER CHANGE REQUIRED`.
4. Does not let the candidate author declare shared consumers unaffected.

#### Assertions

- [ ] **[SI-C04-A01]** Discovery uses the frozen canonical rules and ledger.
- [ ] **[SI-C04-A02]** Shared changes cannot hitchhike on target authorization.
- [ ] **[SI-C04-A03]** Partial impact coverage prevents application.

#### Case Verdict

`PASS` when all consumers are handed to separate owners and no shared write
occurs; otherwise `FAIL`.

---

### Case 5 [SI-C05]: Candidate and application receipts are reproducible

#### Fixture

- Frozen target has two files with known raw hashes.
- Authorized candidate modifies one and creates one target-local file.
- Patch/diff tool and environment identities are available.

#### Input

Run `stage`, conclusive `verify`, then `apply`.

#### Expected reads

- Every base/candidate file, oracle, runner/tool, environment, forward/inverse
  patch, diff receipt, verification, and current live preimage.

#### Expected writes

- Immutable candidate files, manifest, forward/inverse patches,
  `diff-receipt.md`, verification receipt, exact live target postimages, and one
  application receipt.

#### Expected non-writes

- Oracle, spec, catalog, rubric, skill-test artifacts, and unrelated paths.

#### Expected behavior

1. Diff receipt records every path/action/raw base and candidate hash, complete
   diff hash, options, newline/binary policy, tool version/hash, and patch hashes.
2. Execution receipts include argv, cwd, environment, timestamps, exit code,
   stdout/stderr/result hashes, stable outcomes, and producer identity.
3. Apply performs all-file CAS, writes verified postimages, then read-backs each
   raw hash.
4. Application receipt binds the exact diff and observed final state.

#### Assertions

- [ ] **[SI-C05-A01]** Every changed byte has source and postimage provenance.
- [ ] **[SI-C05-A02]** Missing execution fields cannot be PASS.
- [ ] **[SI-C05-A03]** Receipt hashes reproduce the exact candidate and apply.
- [ ] **[SI-C05-A04]** No complete-success claim precedes read-back.

#### Case Verdict

`PASS` only when all receipts and final hashes verify; otherwise `FAIL` or
`PARTIAL` when execution evidence is incomplete before live mutation.

---

### Case 6 [SI-C06]: Partial, stale, or unsupported skill-test evidence blocks

#### Fixture

Use variants where:

- skill-test returns `PARTIAL_VALIDATION`;
- receipt is `STALE`, `INVALID`, or `UNVERIFIED`;
- testing infrastructure is `TEST_INFRA_INVALID`; or
- the pinned skill-test argv cannot accept the isolated candidate root.

#### Input

Run `freeze` or `verify` for each variant.

#### Expected reads

- Exact skill-test receipt, all recorded dependencies, rules/manifest, allowed
  argv, candidate manifest/root, and aggregation trace.

#### Expected writes

- At most an immutable blocked/partial lock or verification receipt when
  separately authorized.

#### Expected non-writes

- Live target, candidate, skill-test artifacts, oracle authorities, and shared
  files.

#### Expected behavior

1. `PARTIAL_VALIDATION` maps to Test `PARTIAL` and Apply Eligible `NO`.
2. Invalid/stale/unverified receipt or invalid infrastructure maps to
   `NOT_RUN` and Apply Eligible `NO`.
3. Unsupported candidate-root execution is `NOT_RUN`; baseline live receipt is
   not substituted.
4. Classification is `INCONCLUSIVE`; verdict is `BLOCKED`.
5. No candidate is installed into the live package for testing.

#### Assertions

- [ ] **[SI-C06-A01]** Partial cannot become PASS.
- [ ] **[SI-C06-A02]** Fresh baseline evidence cannot certify candidate bytes.
- [ ] **[SI-C06-A03]** Tool unavailability and target failure remain distinct.
- [ ] **[SI-C06-A04]** Live-swap testing is forbidden.

#### Case Verdict

`PASS` when every incomplete variant blocks without a live write; otherwise
`FAIL`.

---

### Case 7 [SI-C07]: Recovery evidence is retained and conflicts route to humans

#### Fixture

- A two-file apply is interrupted after one postimage is published.
- Candidate mirror, forward/inverse patches, diff receipt, and failed
  application receipt exist under the immutable run root.
- Another task changes the published file to a divergent hash.
- Acceptance manifest omits `retain_until`.

#### Input

`$skill-improve recover --application <failed-receipt> --direction reverse --recovery-id REC-007`

#### Expected reads

- Failed receipt, current/base/candidate hashes, both patches, diff receipt,
  tool identity, retention policy, and exact recovery direction.

#### Expected writes

- No target write; optionally one immutable blocked recovery receipt.

#### Expected non-writes

- Diverged current file, base-only file, candidate evidence, old receipts, and
  unrelated paths.

#### Expected behavior

1. Classifies paths DIVERGED and BASE before mutation.
2. All-file recovery CAS stops the entire recovery.
3. Retention defaults to indefinite and no mode prunes evidence.
4. Handoff lists exact hashes, first conflict, patch/tool identity, and bounded
   human three-way/CAS/read-back steps.
5. Never instructs copying a backup or saved original over current bytes.

#### Assertions

- [ ] **[SI-C07-A01]** Recovery location and evidence are explicit.
- [ ] **[SI-C07-A02]** Retention cannot expire implicitly.
- [ ] **[SI-C07-A03]** Divergence preserves external work.
- [ ] **[SI-C07-A04]** Manual recovery remains hash-guarded and authorized.

#### Case Verdict

`PASS` when recovery blocks, retains evidence, and provides safe manual steps;
otherwise `FAIL`.

---

### Case 8 [SI-C08]: Evidence classification separates six non-improvement states

#### Fixture

Use frozen variants for:

- objective already satisfied with empty candidate;
- open defect unchanged by candidate;
- inconsistent bounded repeats with identical environment;
- changed environment identity;
- deterministic worsened requirement;
- missing required suite.

#### Input

Run independent `verify` for every variant.

#### Expected reads

- Frozen repeat policy, seeds/order/timeouts, environment and runner hashes,
  baseline/candidate scenario receipts, severities, and targeted findings.

#### Expected writes

- One immutable verification receipt per authorized variant.

#### Expected non-writes

- Live target, candidate, oracle, environment, spec, catalog, and shared files.

#### Expected behavior

1. Classifications are respectively `NO_CHANGE_REQUIRED`, `NO_IMPROVEMENT`,
   `TEST_NOISE`, `ENVIRONMENT_CHANGED`, `REGRESSION`, and `INCONCLUSIVE`.
2. Only the frozen repeat count is used; no after-the-fact rerun fishing.
3. Changed environment is not noise; deterministic worsening is not noise;
   unresolved defect is not no-change-required.
4. Every variant is Apply Eligible `NO`.

#### Assertions

- [ ] **[SI-C08-A01]** Each outcome has one deterministic classification.
- [ ] **[SI-C08-A02]** Classification evidence is persisted in the receipt.
- [ ] **[SI-C08-A03]** Noise and environment changes cannot approve a candidate.
- [ ] **[SI-C08-A04]** No ambiguous `NO_CHANGE_REQUIRED or REJECTED` remains.

#### Case Verdict

`PASS` only when all six variants classify exactly; otherwise `FAIL`.

---

### Case 9 [SI-C09]: Candidate cannot weaken its own oracle

#### Fixture

- Frozen oracle contains safety requirement `AUTH-007`.
- Proposal modifies target `SKILL.md` and tries to delete `AUTH-007` from the
  registered spec/catalog in the same candidate.
- The weakened new suite would otherwise be green.

#### Input

Run `stage` and attempt `verify`.

#### Expected reads

- Oracle lock, candidate proposal, mutation boundary, registered authorities,
  and impact graph.

#### Expected writes

- None for the mixed candidate; no live or oracle mutation.

#### Expected non-writes

- Target, candidate path, spec, catalog, rubric, runner, acceptance/oracle, and
  shared files.

#### Expected behavior

1. Detects out-of-scope oracle paths before staging.
2. Returns `BLOCKED — SEPARATE OWNER CHANGE REQUIRED`.
3. Keeps `AUTH-007` in both frozen authority and verification matrix.
4. Green weakened results have no acceptance authority.

#### Assertions

- [ ] **[SI-C09-A01]** Candidate and judge cannot share a changeset.
- [ ] **[SI-C09-A02]** Removing a constraint cannot self-certify improvement.
- [ ] **[SI-C09-A03]** Apply Eligible remains `NO`.

#### Case Verdict

`PASS` when the mixed proposal is blocked with zero writes; otherwise `FAIL`.

---

### Case 10 [SI-C10]: Concurrent target change blocks apply and recovery

#### Fixture

- Verified candidate expects live hash A.
- Another task changes the target to hash B before apply.
- Separate recovery variant expects candidate hash C but observes divergent D.

#### Input

Run `apply`, then independently evaluate the recovery variant.

#### Expected reads

- Every current path hash, candidate pre/postimage, oracle, verification,
  patches, application/recovery destination state, and transaction plan.

#### Expected writes

- None to live target; optional immutable blocked receipts only at authorized
  unused paths.

#### Expected non-writes

- B, D, all other target paths, oracle, candidate, and existing receipts.

#### Expected behavior

1. All-file CAS detects A != B before apply publication.
2. Recovery detects C != D before any inverse patch.
3. Preserves B and D exactly; never restores A or C from saved content.
4. Requires a new oracle or human hash-guarded recovery task.

#### Assertions

- [ ] **[SI-C10-A01]** One mismatch blocks the entire mutation set.
- [ ] **[SI-C10-A02]** Concurrent edits are never overwritten.
- [ ] **[SI-C10-A03]** Blocked receipts do not claim target mutation.

#### Case Verdict

`PASS` when both operations stop before live writes; otherwise `FAIL`.

---

### Case 11 [SI-C11]: Conclusive happy path stages, verifies, and applies once

#### Fixture

- Frozen oracle/impact graph and all skill-test/runtime evidence are complete
  and current.
- Candidate changes only approved target-local files.
- Every runner accepts the isolated candidate root.
- All targeted failures resolve, no frozen requirement regresses, environment
  is unchanged, and live preimages remain current.

#### Input

Run independent `stage`, `verify`, and `apply` tasks.

#### Expected reads

- Complete oracle, target, candidate, diff/patch, receipt, runner, environment,
  impact, approval, and current-live evidence.

#### Expected writes

- Immutable candidate evidence, verification receipt, exact live postimages,
  and one application receipt.

#### Expected non-writes

- Spec, catalog, rubric, skill-test authorities/receipts, acceptance/oracle,
  shared contracts, and unrelated files.

#### Expected behavior

1. Stage leaves live target unchanged.
2. Verify classifies `IMPROVEMENT`, Test `PASS`, Apply Eligible `YES`, verdict
   `VERIFIED_IMPROVEMENT`.
3. Apply revalidates all hashes and publishes only verified postimages.
4. Read-back yields Candidate `APPLIED`, Mutation `APPLIED`, verdict `APPLIED`.
5. Stops before catalog recording, another run, commit, or publication.

#### Assertions

- [ ] **[SI-C11-A01]** All role tasks are distinct.
- [ ] **[SI-C11-A02]** Every required scenario is conclusive.
- [ ] **[SI-C11-A03]** Applied bytes equal verified candidate hashes.
- [ ] **[SI-C11-A04]** No automatic chained workflow occurs.

#### Case Verdict

`PASS` only when the exact candidate is applied and read back once; otherwise
`FAIL`.

---

### Case 12 [SI-C12]: Legitimate oracle revision uses dual-oracle evidence

#### Fixture

- Independent authority owner supplies an approved immutable oracle-change
  receipt with old/new hashes and stable requirement mapping.
- New oracle intentionally changes one product behavior but retains all safety
  and authorization requirements.
- Candidate is staged only after a new lock is frozen.

#### Input

Freeze with `--prior-lock` and `--oracle-change`, then verify independently.

#### Expected reads

- Prior lock, change receipt, old/new authorities, waivers, owners, impact
  approvals, candidate, runners, and both scenario sets.

#### Expected writes

- New immutable lock, target-local candidate evidence, and verification receipt
  at distinct unused paths.

#### Expected non-writes

- Old/new authority files, prior lock, catalog, rubric, runner, and live target.

#### Expected behavior

1. Validates independent owner, rationale, hashes, stable ID mapping, impact,
   and explicit waiver for every removed requirement.
2. Runs candidate against both old and new frozen scenario sets.
3. Reports separate matrices and rejects any non-waived old safety regression.
4. Candidate never authors either oracle.

#### Assertions

- [ ] **[SI-C12-A01]** Old evidence remains visible after new oracle passes.
- [ ] **[SI-C12-A02]** Safety removal requires explicit authorized waiver.
- [ ] **[SI-C12-A03]** Dual-oracle status is hash-bound and reproducible.

#### Case Verdict

`PASS` when both oracle identities and results remain independently visible;
otherwise `FAIL`.

---

## Protocol Compliance

- [ ] **[SI-PC-001]** Each mode has one bounded write set and previews it before
  first mutation.
- [ ] **[SI-PC-002]** Oracle owner, candidate author, verifier, integrator, and
  recovery owner are independent tasks.
- [ ] **[SI-PC-003]** Skill-test partial/invalid/stale/unverified evidence never
  becomes PASS.
- [ ] **[SI-PC-004]** Written-contract evidence is not generalized to runtime or
  side effects.
- [ ] **[SI-PC-005]** Counts cannot offset severity, safety, or scenario
  regressions.
- [ ] **[SI-PC-006]** Impact graph coverage is deterministic and incomplete
  coverage blocks application.
- [ ] **[SI-PC-007]** Candidate testing never installs or swaps live files.
- [ ] **[SI-PC-008]** Every live apply/recovery path passes all-file CAS before
  the first write.
- [ ] **[SI-PC-009]** Recovery evidence is retained and no full-content restore
  is permitted.
- [ ] **[SI-PC-010]** No mode mutates spec/catalog/rubric/runner/shared contracts
  or auto-chains external actions.

---

## Coverage Notes

### Authoritative P1 finding trace

| Audit ID | SKILL clause | Case/assertion |
|---|---|---|
| `IMPROVE-P1-001` | Phase 6 severity-first improvement predicates | Case 3: `SI-C03-A01`–`SI-C03-A03` |
| `IMPROVE-P1-002` | Phase 2 oracle currentness; Phase 3 oracle revision | Cases 1/9: `SI-C01-A02`, `SI-C01-A04`, `SI-C09-A01`, `SI-C09-A02` |
| `IMPROVE-P1-003` | Phase 2 evidence limits; Phase 5 independent verification | Case 2: `SI-C02-A01`–`SI-C02-A03` |
| `IMPROVE-P1-004` | Phases 1–2 impact surface/graph | Case 4: `SI-C04-A01`–`SI-C04-A03` |
| `IMPROVE-P1-005` | Phases 5/7 reproducible receipts and read-back | Case 5: `SI-C05-A01`–`SI-C05-A04` |
| `IMPROVE-P1-006` | Status axes and Phases 5–6 partial/unavailable states | Case 6: `SI-C06-A01`–`SI-C06-A04` |
| `IMPROVE-P1-007` | Phase 8 recovery evidence and retention | Case 7: `SI-C07-A01`–`SI-C07-A04` |
| `IMPROVE-P1-008` | Phase 6 evidence classifications | Case 8: `SI-C08-A01`–`SI-C08-A04` |

These are the eight exact P1 IDs from the 2026-07-20 skill-improve audit. The
rows are written-contract coverage and do not assert execution.

This spec validates the written workflow contract and immutable evidence/CAS
protocol. It does not execute `$skill-improve` or `$skill-test`, supply the
currently missing candidate-root skill-test argv, prove filesystem transaction
support, or authorize cleanup of run evidence. Candidate-aware skill-test
support, catalog receipt-reference migration, and shared runner infrastructure
remain separately owned work.
