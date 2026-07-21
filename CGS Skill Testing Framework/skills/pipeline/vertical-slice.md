# Skill Test Spec: $vertical-slice

## Skill Summary

`$vertical-slice` freezes an immutable, hash-bound validation plan or independently
evaluates exact build, playtest, network, and velocity evidence. Planning,
implementation batches, evidence capture, creative concerns, formal evaluation,
and recording are separate tasks. One stable hypothesis permits attempt 01 and at
most one targeted attempt 02. Deterministic evidence cannot be upgraded by a
director or user.

---

## Static Assertions

- [ ] VS-S001: YAML frontmatter contains only `name` and non-empty
  `description`; `name` is `vertical-slice`.
- [ ] VS-S002: Invocation exposes explicit `plan`, `evaluate`, and read-only
  `status` modes.
- [ ] VS-S003: Canonical artifacts live under
  `production/validation/vertical-slices/<hypothesis-id>/attempt-<NN>/<slice-run-id>/`.
- [ ] VS-S004: The skill writes only immutable `plan.md` or one new
  `reports/<evaluation-id>.md`; existing paths are rejected.
- [ ] VS-S005: Plan, build, playtest capture, evidence manifest, evaluation,
  creative concerns, and recording have separate task/owner boundaries.
- [ ] VS-S006: A hypothesis allows only attempts 01 and 02; attempt 02 requires
  the same stable hypothesis definition and exact current attempt-01 PIVOT report.
- [ ] VS-S007: Attempt-02 failure yields KILL or
  `BLOCKED — PRODUCT DECISION REQUIRED`, never an automatic third attempt.
- [ ] VS-S008: Every implementation story is a separately authorized bounded
  worktree batch with exact mutation scope and at most one remediation batch.
- [ ] VS-S009: Lack of an isolated worktree blocks implementation; the main
  workspace is never an approved fallback.
- [ ] VS-S010: Build, candidate, report, source commit/tree, engine/version,
  platform/configuration, playtest sessions, and velocity evidence are
  hash-bound.
- [ ] VS-S011: Chat playtest answers and summaries without immutable raw evidence
  cannot satisfy a criterion.
- [ ] VS-S012: Missing sessions, unknown velocity, stale build, partial receipts,
  and required network gaps prevent PROCEED.
- [ ] VS-S013: Evidence verdict precedence is deterministic and cannot be changed
  by a user, director, reviewer, or agent.
- [ ] VS-S014: Creative concerns are advisory, can recommend only a downgrade,
  and cannot override PIVOT/KILL or objective thresholds.
- [ ] VS-S015: Workflow Status, Evidence Verdict, Product Decision, Final Verdict,
  Currentness, Gate Eligible, and Persistence are independent axes.
- [ ] VS-S016: Gate eligibility requires a persisted CURRENT report with
  COMPLETE/PROCEED/PROCEED/PROCEED across the required axes.
- [ ] VS-S017: Status requires an externally recorded expected report SHA-256;
  any report-byte or post-build source/code/content/configuration/build/evidence
  mutation makes an earlier report STALE and gate-ineligible.
- [ ] VS-S018: Metadata describes a multi-task bounded validation workflow rather
  than a one-prompt implementation loop.

---

### Case 1: Plan freezes exact scope without authorizing implementation

**Fixture:**

- A valid prerequisite manifest binds current approved GDDs, accepted ADRs,
  architecture/control manifest, systems index, concept, UX specification,
  engine version, source commit/tree, and platform.
- Stable core-loop system/AC IDs and objective thresholds are available.
- Attempt 01 plan path is unused.

**Input:**

`$vertical-slice plan --run-id vs-run-001 --hypothesis-id VS-H-core-loop --attempt 01 --prerequisites production/validation/manifests/vs-prereq-001.md`

**Expected writes:**

- Exactly
  `production/validation/vertical-slices/VS-H-core-loop/attempt-01/vs-run-001/plan.md`
  after bounded authorization.

**Expected non-writes:**

- No slice code, current-workspace file, worktree, build/evidence receipt,
  playtest artifact, report, session state, prototype index, stage, pivot note,
  graveyard, or Production artifact.

**Expected behavior:**

1. Re-hashes every prerequisite and freezes stable hypothesis/scope hashes.
2. Defines exact story rows, criteria/kill rules, session/network matrix, velocity
   units, decision matrix, and attempt budget.
3. Marks `Plan Status: FROZEN` and `Implementation Authorized: NO`.
4. Reports that each implementation batch needs a fresh task, isolated worktree,
   exact mutation manifest, and separate authorization.
5. Persists atomically and reports the verified plan hash.

**Assertions:**

- [ ] VS-C01-A: "All core systems" resolves to ordered stable IDs.
- [ ] VS-C01-B: The plan does not authorize code or evidence writes.
- [ ] VS-C01-C: Only one exact file is created.
- [ ] VS-C01-D: Plan/currentness hashes are auditable.

---

### Case 2: Missing or stale prerequisites block before worktree creation

**Fixture:**

- Systems index and control manifest are missing.
- One GDD is present but not approved.
- A recorded architecture hash differs from current bytes.

**Input:**

Run `plan` for attempt 01.

**Expected writes:**

- None.

**Expected non-writes:**

- No plan, worktree, implementation, session-state, evidence, or report artifact.

**Expected behavior:**

1. Names every missing, invalid-status, and stale prerequisite path/ID.
2. Returns `Workflow Status: BLOCKED`,
   `Evidence Verdict: INCONCLUSIVE`, `Product Decision: AWAITING`,
   `Final Verdict: BLOCKED — PRODUCT DECISION REQUIRED`, and
   `Gate Eligible: NO`.
3. Does not invent scope, architecture, or hashes.
4. Stops before implementation planning or delegation.

**Assertions:**

- [ ] VS-C02-A: Prerequisites fail closed.
- [ ] VS-C02-B: Missing evidence is not a warning-bearing pass.
- [ ] VS-C02-C: No implementation side effect occurs.

---

### Case 3: Same hypothesis stops after one targeted rerun

**Fixture:**

- Attempt 01 has an immutable CURRENT PIVOT report with hypothesis hash H and
  stable failures `VS-F-01` and `VS-F-02`.
- Attempt 02 reuses H and the original threshold meanings, targeting those
  failures plus regressions.
- Attempt 02's deterministic evidence again yields PIVOT.
- A request is then made for attempt 03.

**Input:**

Run attempt-02 plan/evaluation, then request attempt 03 using the same hypothesis
ID.

**Expected writes:**

- Attempt 02 may create its authorized plan and evaluation report.
- Attempt 03 writes nothing.

**Expected non-writes:**

- No third plan, reset counter, broadened rerun, or automatic code batch.

**Expected behavior:**

1. Validates the attempt-01 report path/hash and same hypothesis definition.
2. Limits attempt 02 to named failures and regressions.
3. Maps second PIVOT to allowed Product Decision KILL or
   NEW_HYPOTHESIS_REQUIRED.
4. If not KILL, returns
   `Final Verdict: BLOCKED — PRODUCT DECISION REQUIRED`.
5. Rejects attempt 03. A changed question/threshold requires a new hypothesis ID.

**Assertions:**

- [ ] VS-C03-A: Initial run plus one rerun is the absolute limit.
- [ ] VS-C03-B: Stable hypothesis and finding IDs survive the rerun.
- [ ] VS-C03-C: Failed history cannot be erased by changing labels.
- [ ] VS-C03-D: No same-hypothesis third attempt is possible.

---

### Case 4: Creative director cannot upgrade or override evidence/user decision

**Fixture:**

Use these variants:

- A required current criterion FAIL makes Evidence Verdict PIVOT, while creative
  concerns recommend PROCEED.
- Evidence Verdict PROCEED, creative concerns recommend PROCEED, but the product
  owner chooses PIVOT.
- Evidence Verdict KILL, while creative concerns recommend PIVOT.

Every concern receipt is otherwise valid and hash-bound.

**Input:**

Run `evaluate` with each exact creative-concerns receipt.

**Expected writes:**

- Optional immutable evaluation report reflecting the deterministic result and
  allowed product decision.

**Expected non-writes:**

- No evidence edit, threshold waiver, creative-authored verdict replacement,
  stage transition, or report rewrite.

**Expected behavior:**

1. Calculates Evidence Verdict before reading concerns.
2. Labels concerns advisory and rejects any attempted upgrade.
3. Preserves the user's conservative PIVOT/KILL choice.
4. Never changes PIVOT or KILL to PROCEED.
5. Reports the attempted conflict in the report without granting authority.

**Assertions:**

- [ ] VS-C04-A: Evidence verdict is mechanically derived.
- [ ] VS-C04-B: Creative authority cannot override objective failure.
- [ ] VS-C04-C: Creative authority cannot override user PIVOT/KILL.
- [ ] VS-C04-D: Report bytes are authored only by the evaluator.

---

### Case 5: Multi-week work is split into bounded worktree batches

**Fixture:**

- Frozen plan has stories `VS-S-01` and `VS-S-02`.
- Each has exact initial/remediation IDs and allowed paths.
- VS-S-01's initial batch discovers a necessary file outside its mutation
  manifest.
- A later authorized remediation batch still fails its stop condition.

**Input:**

Consume the plan as independent implementation tasks.

**Expected writes:**

- Only separately authorized paths inside each task's isolated worktree and its
  exclusive receipt path.

**Expected non-writes:**

- No implicit new file, main-workspace fallback, unbounded daily checkpoint edit,
  third remediation, automatic merge, or worktree deletion.

**Expected behavior:**

1. The out-of-manifest need stops the initial batch rather than expanding scope.
2. A new exact authorization is required for the remediation batch.
3. After remediation failure, emits PARTIAL/BLOCKED receipt and stops.
4. Records branch, worktree, base/pre/post tree hashes, actual path hashes,
   commands/results, timing, and blocker IDs.
5. Planning/evaluation tasks do not perform these implementation writes.

**Assertions:**

- [ ] VS-C05-A: Every batch has an enumerable authorization boundary.
- [ ] VS-C05-B: Context duration cannot silently broaden the changeset.
- [ ] VS-C05-C: Story remediation is finite.
- [ ] VS-C05-D: Worktree ownership/retention is explicit.

---

### Case 6: Report is stale after source or build mutation

**Fixture:**

- A persisted PROCEED report binds source commit/tree T1, candidate C1, artifact
  hash B1, sessions S1–S3, and evidence manifest E1.
- Variant A changes one source/configuration byte after C1.
- Variant B rebuilds to the same filename with artifact hash B2.
- Variant C changes one raw playtest receipt.

**Input:**

`$vertical-slice status <exact-report-path> --expect-report <recorded-sha256>`

**Expected writes:**

- None.

**Expected non-writes:**

- No report refresh, artifact rollback, stage transition, index update, or new
  evidence.

**Expected behavior:**

1. Re-hashes the complete report graph.
2. Detects each changed identity even when filenames are unchanged.
3. Returns `Currentness: STALE` and `Gate Eligible: NO`.
4. Does not retain PROCEED eligibility from historical evidence.

**Assertions:**

- [ ] VS-C06-A: Verdict binds exact source and build bytes.
- [ ] VS-C06-B: Playtest evidence binds that same candidate.
- [ ] VS-C06-C: Successful rebuild does not preserve the old identity.
- [ ] VS-C06-D: Status mode is read-only.

---

### Case 7: Missing build or playtest evidence is first-class INCONCLUSIVE

**Fixture:**

Run variants with:

- final candidate build receipt missing;
- one planned session NOT_RUN;
- raw recording hash missing;
- wrong-build playtest receipt;
- evidence-manifest owner equal to evaluator; or
- an implementation receipt marked PARTIAL.

No verified required criterion has already failed.

**Input:**

Run `evaluate`.

**Expected writes:**

- Optional immutable PARTIAL/INCONCLUSIVE evaluation report.

**Expected non-writes:**

- No synthesized receipt, PASS inference, report upgrade, or stage transition.

**Expected behavior:**

1. Preserves every missing/invalid row in the denominator.
2. Returns `Workflow Status: PARTIAL`,
   `Evidence Verdict: INCONCLUSIVE`,
   `Final Verdict: BLOCKED — PRODUCT DECISION REQUIRED`, and
   `Gate Eligible: NO`.
3. Names exact evidence required to resume.
4. Treats chat claims as non-evidence.

**Assertions:**

- [ ] VS-C07-A: Missing evidence cannot produce PROCEED.
- [ ] VS-C07-B: Partial agents/builds/playtests remain visible.
- [ ] VS-C07-C: Evaluator independence is enforced.

---

### Case 8: Network core fantasy cannot pass on 0 ms-only evidence

**Fixture:**

- Core fantasy includes network combat feel.
- Plan requires two peers at target latency/jitter/loss cells.
- Local 0 ms sessions pass the non-network loop.
- No real-peer or simulated target-network receipt exists.

**Input:**

Run `evaluate`.

**Expected writes:**

- Optional immutable INCONCLUSIVE report.

**Expected non-writes:**

- No network PASS inference or unconditional PROCEED report.

**Expected behavior:**

1. Credits local evidence only to non-network criteria.
2. Marks required network cells NOT_RUN.
3. Returns PARTIAL/INCONCLUSIVE and Gate Eligible NO unless a verified failure
   already establishes PIVOT/KILL.
4. Names the exact peer/network matrix still required.

**Assertions:**

- [ ] VS-C08-A: 0 ms local play is not network-feel evidence.
- [ ] VS-C08-B: Network thresholds are frozen before tests.
- [ ] VS-C08-C: Missing network coverage blocks PROCEED.

---

### Case 9: Unknown velocity prevents production-feasibility PROCEED

**Fixture:**

- Core loop and playtest criteria pass.
- Batch receipts contain day labels but omit actual start/end, active/blocked
  time, scope units, or commit/build IDs.
- No other criterion fails.

**Input:**

Run `evaluate`.

**Expected writes:**

- Optional immutable PARTIAL/INCONCLUSIVE report.

**Expected non-writes:**

- No conversion of estimates or prose into observed velocity.

**Expected behavior:**

1. Marks velocity criterion UNKNOWN.
2. Returns `Evidence Verdict: INCONCLUSIVE` and Gate Eligible NO.
3. Reports the missing fields and does not calculate a production rate.
4. Preserves gameplay PASS rows separately.

**Assertions:**

- [ ] VS-C09-A: Velocity uses actual time/scope evidence.
- [ ] VS-C09-B: Missing velocity does not disappear from the matrix.
- [ ] VS-C09-C: Gameplay success alone cannot prove production feasibility.

---

### Case 10: Fully current evidence produces gate-eligible PROCEED

**Fixture:**

- Exact plan and prerequisite graph are CURRENT.
- All bounded batch/build receipts pass and bind one final candidate.
- Planned playtest and network cells have valid immutable raw evidence for that
  candidate.
- Velocity ledger is complete.
- Every proceed criterion passes; no kill rule or required failure is true.
- Evidence-manifest/evaluator roles are independent.
- Optional creative concerns are hash-bound and do not identify evidence gaps.
- Product owner chooses PROCEED.
- Fresh evaluation path is authorized.

**Input:**

Run `evaluate --persist` with exact inputs.

**Expected writes:**

- Exactly one new
  `production/validation/vertical-slices/<hypothesis>/attempt-<NN>/<run>/reports/<evaluation-id>.md`,
  atomically verified.

**Expected non-writes:**

- No evidence, plan, code, index, stage, session-state, gate, or Production
  planning artifact.

**Expected behavior:**

1. Re-hashes the complete evidence graph immediately before persistence.
2. Derives `Workflow Status: COMPLETE`,
   `Evidence Verdict: PROCEED`, `Product Decision: PROCEED`,
   `Final Verdict: PROCEED`, and `Currentness: CURRENT`.
3. Returns `Gate Eligible: YES` only after the report is re-read and verified.
4. Reports exact report and candidate hashes.
5. Stops for a separate recorder/gate consumer.

**Assertions:**

- [ ] VS-C10-A: Every PROCEED predicate is satisfied simultaneously.
- [ ] VS-C10-B: Report identity matches the tested build and sessions.
- [ ] VS-C10-C: Persistence and verdict remain separate until verification.
- [ ] VS-C10-D: The skill does not advance the stage itself.

---

### Case 11: Declined or failed report persistence is not gate evidence

**Fixture:**

- The calculated evidence/final verdict is PROCEED.
- Variant A omits or declines `--persist`.
- Variant B authorizes persistence but the atomic write or byte verification
  fails.

**Input:**

Run both evaluation variants.

**Expected writes:**

- Variant A: none.
- Variant B: no verified canonical evaluation report.

**Expected non-writes:**

- No index, gate, stage, or substitute report.

**Expected behavior:**

1. Retains the calculated evidence and product verdict in conversation.
2. Variant A returns Persistence NOT_REQUESTED/DECLINED and Gate Eligible NO.
3. Variant B returns Persistence FAILED and Gate Eligible NO.
4. Neither claims a canonical persisted PROCEED receipt.

**Assertions:**

- [ ] VS-C11-A: Report persistence cannot be inferred.
- [ ] VS-C11-B: Unpersisted or failed output is never gate-eligible.
- [ ] VS-C11-C: No unrelated write compensates for failure.

---

## Cross-skill compatibility assertions

- [ ] VS-X001: A gate consumer accepts only an explicitly supplied CURRENT
  persisted PROCEED report and exact candidate/report hashes.
- [ ] VS-X002: Creative review produces concerns only; it never owns or replaces
  the evidence/product verdict.
- [ ] VS-X003: Prototype/index/pivot/graveyard recording remains a separate
  owner-authorized responsibility.
- [ ] VS-X004: Implementation stories and worktree batches are independently
  authorized; no vertical-slice plan is implementation authorization.
- [ ] VS-X005: Real playtest capture is immutable, session-identified, and bound
  to the exact final build.
- [ ] VS-X006: Skill, metadata, and this spec use the same modes, paths, attempt
  budget, evidence matrix, status axes, and gate rule.
