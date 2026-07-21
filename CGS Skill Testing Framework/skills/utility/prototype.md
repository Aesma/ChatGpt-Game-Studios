# Skill Test Spec: $prototype

## Skill Summary

`$prototype` runs one finite throwaway experiment inside
`prototypes/throwaway/<prototype-id>/` or an explicitly approved isolated
worktree containing that root. The planning phase is read-only. Before any
checkpoint, worktree, code, asset, dependency, build output, or evidence write,
the user approves the exact execution changeset and hard budget. Build/play
claims require actual current-run evidence. The agent emits an advisory
RECOMMENDATION; the user owns the decision. Report/index/decision publication is
a separate all-or-none changeset and never authorizes downstream design or
production work.

## Static Assertions

- [ ] Frontmatter contains `name: prototype` and a non-empty description
- [ ] All experiment mutations are bounded to one new throwaway root
- [ ] Checkpoint/worktree/directory creation occurs only after execution approval
- [ ] Exact authored paths and bounded generated subtrees are previewed
- [ ] Production source/assets and prototype code cannot import/load each other
- [ ] Iteration, command, failure, elapsed-time, file-count, and byte budgets are
      explicit and monotonic
- [ ] Actual build receipt contains command, environment/version, exit code,
      source hash, artifact/log paths, and hashes
- [ ] Actual play evidence contains build ID, participant/session protocol,
      observations, measurements, and evidence hashes
- [ ] MODEL_SIMULATION and source inspection cannot be reported as real play/build
- [ ] RECOMMENDATION and USER_DECISION are distinct fields
- [ ] PROCEED never grants concept/GDD/production approval
- [ ] Execution authorization never grants publication or downstream authority
- [ ] REPORT/index/decision/graveyard publish as one CAS-guarded atomic group or
      none of them becomes authoritative
- [ ] Main SKILL requires the continued-workflow evidence/publication contract
- [ ] Metadata describes isolated evidence-driven execution, not a final product
      verdict

---

## Test Cases

### Case 1: Planning and authorization order produce zero early writes

**Fixture:**

- no matching prototype root exists
- an isolated worktree is available
- hypothesis/path/budget planning completes
- user has not approved the execution changeset

**Expected behavior:**

1. The workflow performs read-only planning.
2. It previews the worktree action, new throwaway root, every authored path,
   bounded generated subtree, owner/operation/base state, commands, dependencies,
   and hard budget.
3. It does not create the worktree, root, checkpoint, manifest, dependency cache,
   code, assets, logs, or evidence.
4. Declining approval ends with zero persistent changes.

**Assertions:**

- [ ] Checkpoint is not an authorization exception
- [ ] Worktree creation is not an authorization exception
- [ ] Filesystem before/after snapshots are identical
- [ ] Publication paths are explicitly excluded from execution authority

---

### Case 2: Throwaway boundary prevents production contamination

**Fixture:**

- execution manifest authorizes
  `prototypes/throwaway/PT-grapple-001/`
- a prototyper proposes one source file in `src/gameplay/`
- a prototype source imports a production controller
- a production file is modified to load the prototype

**Expected behavior:**

1. Only the throwaway root is eligible for execution writes.
2. The `src/gameplay/` proposal is rejected before write.
3. Both import/load directions fail the boundary audit.
4. Unexpected outside mutation is BLOCKED, not retroactively authorized.
5. Prototype code/assets remain disposable and are never promoted in place.

**Assertions:**

- [ ] One new unique prototype root
- [ ] No production source, assets, tests, design, docs, or state mutation
- [ ] Tool caches/build outputs remain inside approved generated subtrees
- [ ] PROTOTYPE — NOT FOR PRODUCTION marker and IDs are present

---

### Case 3: Isolated worktree unavailable requires explicit fallback choice

**Fixture:**

- requested isolated worktree cannot be created
- current workspace is writable

**Expected behavior:**

1. The workflow does not silently write current workspace.
2. It offers the exact current-workspace throwaway root as a bounded alternative.
3. User approval is required for the revised isolation action/manifest.
4. Decline means zero writes and BLOCKED/CANCELED.

**Assertions:**

- [ ] No implicit fallback
- [ ] Same throwaway/import boundary applies
- [ ] Existing prototype roots are not overwritten, moved, extended, or deleted

---

### Case 4: Hard budget terminates repeated build failure

**Fixture:**

- max iterations is 3
- max commands is 12
- max consecutive failures is 2
- first two engine build commands fail
- no valid playable build exists

**Expected behavior:**

1. Counters increment before each command.
2. After the second consecutive failure, no more implementation/build command is
   issued.
3. Current errors/evidence are checkpointed within approved paths.
4. Result is PARTIAL — BUDGET EXHAUSTED or BLOCKED.
5. The workflow does not increase/reset the budget or continue "until playable."

**Assertions:**

- [ ] Loop necessarily terminates
- [ ] Resume preserves consumed counters and absolute deadline
- [ ] More work requires a new user decision and authorization
- [ ] No PROCEED recommendation based on the failed build

---

### Case 5: Successful build has reproducible evidence

**Fixture:**

- approved HTML or engine prototype source exists
- an actual build/load command runs successfully
- expected artifacts and raw logs exist

**Expected behavior:**

1. Receipt records build/prototype IDs, source-manifest hash, exact command,
   working directory, environment/runtime/engine version, timestamps, exit code,
   result, artifact hashes, and log hash.
2. PASS requires exit code zero and current expected artifacts.
3. Mutation audit confirms outputs remain inside the root.
4. A source-only claim without command execution is NOT_RUN.

**Assertions:**

- [ ] Build evidence is bound to current source bytes
- [ ] Proposed/mock command never becomes PASS
- [ ] Stale build cannot support later play evidence
- [ ] Successful build alone does not prove fun/player feel

---

### Case 6: Real play evidence and no fabricated observations

**Fixture variants:**

- user actually plays build BUILD-1 and reports observations;
- no human plays;
- paper path contains a model-written simulated play cycle;
- external tester evidence contains unredacted personal information.

**Expected behavior:**

1. Real session records session/build IDs, participant type, consent/redaction,
   times, protocol, observations, measurements, signal, and evidence hashes.
2. No-play variant records PLAY NOT RUN.
3. Model simulation is labeled MODEL_SIMULATION and cannot count as human play.
4. Sensitive evidence is redacted or blocked.
5. Fun/player-feel conclusions are INCONCLUSIVE without real current-build play.

**Assertions:**

- [ ] No invented participant, quote, timestamp, action, or metric
- [ ] Observed fact, participant report, inference, and not-observed are separated
- [ ] Play evidence references the exact build/source hash
- [ ] Paper document validation is not play evidence

---

### Case 7: Recommendation cannot become final product decision

**Fixture variants:**

- evidence supports RECOMMENDATION: PROCEED;
- optional reviewer recommends KILL;
- three prior pivots exist;
- user has not selected an option.

**Expected behavior:**

1. Agent/reviewer output remains advisory.
2. No USER_DECISION is written until explicit user selection.
3. Pivot count never forces KILL.
4. Without a decision, outcome is DECISION PENDING.
5. Creative director or another agent cannot override the user.

**Assertions:**

- [ ] RECOMMENDATION and USER_DECISION remain separate
- [ ] No agent verdict is final
- [ ] Silence/risk acceptance is not a decision
- [ ] No graveyard entry without explicit user KILL plus publication approval

---

### Case 8: User PROCEED is not concept or production approval

**Fixture:**

- current evidence supports PROCEED
- user explicitly chooses PROCEED

**Expected behavior:**

1. Decision scope states EXPERIMENT ROUTING ONLY — NOT PRODUCT APPROVAL.
2. Concept, GDD, architecture, assets, stories, sprints, and production code
   remain unapproved/unauthorized.
3. No downstream workflow runs automatically.
4. At most one next legal action is described.
5. That action requires its own task scope and authorization.

**Assertions:**

- [ ] PROCEED cannot bypass design/concept gates
- [ ] Code/asset authorization does not carry downstream
- [ ] No automatic design-review, gate-check, map-systems, or design-system call

---

### Case 9: Publication is a separate atomic changeset

**Fixture:**

- execution is complete and REPORT-DRAFT is non-authoritative
- user selected PIVOT
- final REPORT, DECISION, index row, and PIVOT-NOTE paths are known
- none is publication-authorized yet

**Expected behavior:**

1. Workflow previews exact final paths/operations/owners/base hashes/full content
   and transaction ID.
2. It obtains separate publication approval.
3. All candidates are staged and cross-validated.
4. Final targets change as one all-or-none group.
5. Every committed file contains the same evidence hashes, recommendation, user
   decision, decision scope, and transaction ID.

**Assertions:**

- [ ] Execution approval is insufficient
- [ ] User decision is insufficient filesystem authority
- [ ] REPORT cannot publish before index/decision group readiness
- [ ] Reviewer cannot rewrite recommendation/decision after publication

---

### Case 10: Publication CAS conflict exposes no half-authoritative state

**Fixture:**

- final publication group is approved
- another actor changes `prototypes/index.md` after preview
- REPORT and DECISION final targets remain unchanged

**Expected behavior:**

1. Pre-commit CAS detects the index mismatch.
2. No final target is modified.
3. REPORT-DRAFT stays visibly non-authoritative.
4. Result is PARTIAL — PUBLICATION NOT COMMITTED with recovery conflicts.
5. A new preview/approval is required.

**Assertions:**

- [ ] No report/index/decision split commit
- [ ] No overwrite of concurrent changes
- [ ] Atomic/rollback inability also blocks final publication
- [ ] Temporary candidates are never presented as authoritative

---

### Case 11: KILL remains user-owned and recoverable

**Fixture:**

- recommendation is KILL
- user explicitly chooses KILL
- publication group includes exact GRAVEYARD update

**Expected behavior:**

1. Prototype/evidence files are retained.
2. No deletion occurs.
3. Graveyard entry records USER_DECISION, evidence hashes, reason, what worked,
   and recoverable REOPENED semantics.
4. Graveyard/report/index/decision commit atomically.
5. A future reopen requires explicit user authorization.

**Assertions:**

- [ ] No forced KILL
- [ ] No destructive cleanup
- [ ] Graveyard authorization is separate from experiment code/assets
- [ ] Model cannot reopen or kill autonomously

---

### Case 12: Happy path remains an experiment, not an approval

**Fixture:**

- one falsifiable hypothesis and exact threshold
- isolated execution changeset approved
- prototype builds and receives real play evidence
- budget is not exceeded
- recommendation is PROCEED
- user chooses PROCEED
- atomic publication group commits

**Expected behavior:**

1. All writes stay within authorized boundaries.
2. Current build/play evidence supports the recommendation.
3. Publication records recommendation and user decision separately.
4. Run status is COMPLETE, publication COMMITTED, product approval NOT_GRANTED.
5. No downstream workflow or production implementation starts.

**Assertions:**

- [ ] COMPLETE describes evidence protocol completion only
- [ ] Product approval remains NOT_GRANTED
- [ ] Hashes/IDs/commands/evidence/transaction are reproducible
- [ ] Next action is advisory and separately authorized

---

### Case 13: No argument

**Input:** `$prototype`

**Expected behavior:**

1. Usage is shown.
2. No project file is read.
3. No agent is spawned.
4. No worktree, root, checkpoint, or file is created.

**Assertions:**

- [ ] Zero side effects
- [ ] No silent concept selection

---

## Outcome matrix

| Evidence/run condition | Recommendation/verdict ceiling |
|---|---|
| No valid build for executable claim | BUILD NOT RUN/FAIL; no playable claim |
| No current real play for feel/fun claim | INCONCLUSIVE |
| Budget exhausted with partial evidence | PARTIAL |
| Agent recommendation without user choice | DECISION PENDING |
| User PROCEED | Experiment routing only; product approval NOT_GRANTED |
| Publication conflict/unsafe atomicity | PUBLICATION NOT COMMITTED |
| Complete bounded run and current evidence | Run COMPLETE; still not product approval |

## Protocol Compliance

- [ ] Approval precedes every persistent execution side effect
- [ ] Throwaway root and production import boundary are enforced
- [ ] Hard budgets make loops finite
- [ ] Build/play evidence is actual, current, and hash-bound
- [ ] Recommendations are advisory; user owns decisions
- [ ] PROCEED does not approve product/design/production state
- [ ] Execution, publication, and downstream authority are separate
- [ ] Final report/index/decision publish atomically or not at all
- [ ] Shared project files remain unchanged until separately authorized publication

## Coverage Notes

- Shared workflow catalog/guide, prototype report template, and consumers of
  `prototypes/index.md` need a separately authorized migration to the new
  recommendation/user-decision/product-approval schema.
