# Skill Test Spec: $team-qa

## Purpose

Verify the complete P1 remediation set TQA-007 through TQA-017. `$team-qa` must
resolve one exact scope and build, authorize only presently knowable writes, respect the
actual agent budget, freeze Phase 1–5 evidence before signoff, checkpoint every phase,
quarantine partial/late work, and expose unambiguous workflow and QA result axes.

This specification is static and fixture-driven. It does not execute `$team-qa`,
external tests, bug creation, release gates or deployment.

## Fixtures and harness rules

Positive fixtures contain exact raw bytes and full lowercase SHA-256 for:

- `cgs.team-qa-request/v2` and `cgs.team-qa-scope-manifest/v2`;
- stable sprint/scope/story/requirement/AC/Test IDs and ordered source hashes;
- candidate, build receipt, artifact, source and target matrix;
- P1 QA plan, smoke receipt, regression selection and runner receipts;
- manual, playtest and soak evidence where required;
- Phase 1–5 checkpoints and `cgs.team-qa-evidence-manifest/v2`;
- independent P1 test-evidence-review request/report; and
- configured `max_threads`, exact live-agent snapshots, assignments and deadlines.

Negative variants change exactly one fact unless stated otherwise. The harness asserts
no undeclared filesystem, Git, build, bug, session, catalog, release, deployment or
publication mutation. Catalog execution fields remain blank because document staging is
not a real test run.

## Structural assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name is `team-qa`.
- [ ] Invocation is exactly `$team-qa --request <path> --expect-request <sha256>`.
- [ ] The strict request exposes START, INGEST, FREEZE, FINALIZE, STATUS and RESUME.
- [ ] There are exactly six phases; Phase 6 consumes only frozen Phase 1–5 evidence plus independent review.
- [ ] Scope, candidate, build, QA plan, smoke, evidence, review and signoff use exact path/hash identities.
- [ ] Controller write, test/manual execution, bug creation, evidence review and release/deployment authorities remain separate.
- [ ] START cannot pre-authorize future evidence, bug or signoff paths.
- [ ] Concurrency counts controller and nested agents and never exceeds actual available slots.
- [ ] Assignments have exclusive paths, deadlines, bounded responses, at most one retry and late-result quarantine.
- [ ] Workflow State and QA Verdict are always paired; no bare COMPLETE is emitted.
- [ ] Generic session state is not written; canonical immutable checkpoints bind the unique run and build.
- [ ] No review-mode branch alters denominator, staffing, evidence or signoff semantics.
- [ ] Context loading obeys file/byte/story/receipt/depth/agent/response/time budgets and records omissions.
- [ ] QA plan consumption matches `cgs-qa-plan` Schema 2; it remains Gate Evidence NO.
- [ ] Smoke consumption matches `cgs-smoke-check-receipt/v2`; only persisted sprint PASS with handoff YES enters.
- [ ] Regression selection Schema 2 is not treated as test execution.
- [ ] Automated/manual/playtest/soak PASS requires current independently produced evidence.
- [ ] Evidence review checks all independent P1 axes, not Workflow COMPLETE alone.
- [ ] QA_APPROVED becomes Gate Eligible YES only after verified signoff persistence.
- [ ] Team-QA signoff is QA evidence, never release GO or deployment/publication authority.
- [ ] Terminal output is `cgs.team-qa-result/v2` with exactly one legal next operation.

## P1 traceability

| Audit ID | Primary case |
|---|---|
| TQA-007 | Case 1 |
| TQA-008 | Case 2 |
| TQA-009 | Case 3 |
| TQA-010 | Case 4 |
| TQA-011 | Case 5 |
| TQA-012 | Case 6 |
| TQA-013 | Case 7 |
| TQA-014 | Case 8 |
| TQA-015 | Case 9 |
| TQA-016 | Case 10 |
| TQA-017 | Case 11 |

## Case 1 — Unique stable scope, never glob or mtime — TQA-007

Provide exact scope `SPRINT-12` with one stable sprint manifest and ordered story
hashes. Test these variants independently: two matching sprint files; a directory or
glob instead of manifest; “latest sprint”; date-only scope/run ID; changed story hash;
duplicate canonical story path; and exact valid scope.

**Expected**

- only the exact valid `cgs.team-qa-scope-manifest/v2` proceeds;
- every ambiguous/multiple/unsafe/mismatched variant is
  `WORKFLOW_BLOCKED_AT_ENTRY / QA_INCOMPLETE / Gate Eligible NO`;
- no directory enumeration, mtime tie-break or automatic sprint choice occurs;
- scope ID, ordered membership and scope identity hash appear in every later artifact;
  and
- a changed scope/build requires a new QA run ID.

## Case 2 — Operation-scoped authorization for knowable writes — TQA-008

START has exact manifest/strategy/case paths but failures and future evidence IDs are
not yet known. Later, two evidence receipts and one unmatched finding arrive.

**Expected**

- START previews/creates only its exact known absent targets and checkpoint;
- START authority does not cover later evidence, freeze, signoff or bug paths;
- each INGEST, FREEZE and FINALIZE presents a new exact closed changeset only after its
  IDs and bytes are known;
- Team QA never writes `production/qa/bugs/**`; the exact occurrence/fingerprint/evidence
  is handed to one serialized bug-report owner under separate authority;
- expanded scope or changed output membership stops for a new request/authority;
- no prose claims that all future files were pre-authorized.

## Case 3 — Live-slot concurrency cap and exclusive batching — TQA-009

Set `max_threads = 6`, request worker limit 4, and test live totals one, three and six,
including nested agents. Provide ten story shards with distinct case destinations.

**Expected**

- dispatch slots are respectively four, three and zero;
- the controller and nested agents count; children may not spawn without assigned slot;
- invalid/missing config or live count falls back to serial execution;
- shards run in batches no larger than dispatch slots and each owns disjoint proposal
  paths;
- every batch is gathered and recorded before the next;
- no “one tester per story” unbounded dispatch occurs.

## Case 4 — Phase 6 consumes only frozen Phase 1–5 inputs — TQA-010

Prepare complete checkpoints 01–05 and one frozen evidence-manifest identity. Provide
qa-lead an input phrased as “Phases 4–6,” then the exact Phase 1–5 manifest/checkpoint.
Attempt to include the Phase 6 signoff candidate in its own inputs.

**Expected**

- ambiguous “Phases 4–6” and self-referential signoff input are rejected;
- qa-lead receives only the exact frozen Phase 1–5 evidence manifest/checkpoint and
  cannot change rows, counts or evidence;
- independent evidence review is a separate exact input;
- Phase 6 derives signoff deterministically without circular dependency;
- the spec and skill expose the same six-phase order.

## Case 5 — Workflow completion is never QA approval — TQA-011

Finalize three fully evaluated fixtures: all evidence passes, one current FAIL, and one
required NOT_RUN. Test a downstream parser that sees only the word COMPLETE.

**Expected**

- output always contains paired machine axes plus an unambiguous rendered outcome;
- the fixtures return respectively
  `WORKFLOW_COMPLETED / QA_APPROVED`,
  `WORKFLOW_COMPLETED / QA_NOT_APPROVED`, and
  `WORKFLOW_COMPLETED / QA_INCOMPLETE`;
- no standalone COMPLETE field may be consumed as quality success;
- Gate Eligible is YES only for verified persisted QA_APPROVED;
- the parser cannot infer pass from workflow completion.

## Case 6 — Unique run path and coherent checkpoint vocabulary — TQA-012

Start two runs on the same calendar date, test a date-only ID, and attempt to write
`production/session-state/active.md` using legacy PASS/FAIL/CONCERNS values. Provide one
valid UUID run with checkpoint/signoff hashes.

**Expected**

- date-only or colliding run IDs are rejected;
- no generic session-state file is read or written;
- only the canonical unique run root and `cgs.team-qa-checkpoint/v2` store recovery
  state;
- checkpoints/signoff use the same Workflow State, QA Verdict, Gate Eligible, phase
  and persistence enumerations;
- every checkpoint binds build, evidence-manifest and report/signoff hashes or explicit
  NONE, preventing path/date drift.

## Case 7 — Milestone checkpoints and exact resume — TQA-013

Interrupt after phases 1, 3 and 5. Resume each from its exact checkpoint. Then vary a
predecessor hash, candidate byte, evidence receipt and already-existing next target.

**Expected**

- phases 01–05 each have an immutable predecessor-linked checkpoint with inputs,
  outputs, status axes, assignment ledger, budget use and legal next operation;
- valid resume re-hashes the entire predecessor/input chain and continues only the
  recorded next operation without replaying complete work;
- changed/broken/ambiguous fixtures block and name the exact owner/action;
- existing target or CAS drift never overwrites and writes nothing further;
- STATUS validates the chain read-only and never repairs it.

## Case 8 — Timeout, partial, cancel, retry and late-write rules — TQA-014

Run four required assignments: one succeeds, one returns half a schema, one times out,
and one is cancelled. Let the timeout return after Phase 5 freeze. Also test a retry
whose candidate hash changed.

**Expected**

- assignment IDs, deadlines, response limits, attempts and exact outcomes are recorded;
- partial/timeout/cancelled work leaves required rows nonconclusive and QA_INCOMPLETE;
- at most one retry is allowed before freeze with identical inputs/path/budget/authority;
- changed retry inputs require new authority and cannot reuse the assignment;
- Phase 5 cancels outstanding work; late output is `LATE_IGNORED` and cannot write,
  amend or qualify the frozen run;
- admitting late evidence requires a new evidence identity and QA run.

## Case 9 — Review-mode removal and explicit role fallback — TQA-015

Supply legacy `full`, `lean` and `solo` flags; separately make qa-tester and qa-lead
unavailable while all execution evidence remains external.

**Expected**

- legacy review flags are rejected and cannot alter evidence scope, denominator,
  staffing or verdict;
- qa-tester absence permits local case drafting only, still NOT_RUN;
- qa-lead absence permits draft strategy/mechanical normalization only; a policy-
  required assessment stays missing and forces QA_INCOMPLETE;
- independent test-evidence-review can never be self-produced or waived;
- fallback cannot attest execution, manual observation, playtest, soak or platform facts.

## Case 10 — Bounded context with complete omission ledger — TQA-016

Provide 100 stories when the request allows 10 story shards and a byte limit that fits
nine complete story authority closures. Include one tenth story whose dependency closure
would cross the byte limit.

**Expected**

- only declared, deterministically ordered files are read; no full-directory scan occurs;
- nine whole closures load and the tenth is omitted intact, never partially truncated;
- selected/loaded/missing/unreadable/invalid/omitted/unprocessed rows and consumed
  file/byte/dependency budgets are reported;
- required omission makes workflow partial and QA_INCOMPLETE;
- each delegate receives one bounded shard and returns schema rows plus bounded summary,
  not the full corpus;
- raising a request budget above hard ceilings is rejected.

## Case 11 — Complete aligned specification and QA/release integration — TQA-017

Run static structure lint and the adjacent-contract matrix.

### QA-plan variants

1. exact `cgs-qa-plan` Schema 2 with generation/current states CURRENT, complete
   coverage, Build Binding BOUND and Gate Evidence NO;
2. Schema 1, PARTIAL/UNKNOWN, unbound build, gaps or stale source.

Only variant 1 may satisfy the plan authority; it never proves execution.

### Smoke variants

1. exact canonical `cgs-smoke-check-receipt/v2`, sprint PASS, Persistence VERIFIED,
   Handoff Eligible YES and matching selected-scope/member hashes;
2. quick/targeted pass, wrong build, partial, warning/unknown, unpersisted or handoff NO.

Only variant 1 passes entry.

### Regression, playtest, soak and review variants

- regression-selection-manifest Schema 2 without runner receipt remains NOT_RUN;
- playtest requires `cgs.playtest-report/v2` plus independent recorder receipt and
  `RECORDED COMPLETED — GATE ELIGIBLE`;
- soak requires exact `cgs-soak-result/v2` plus completion receipt, verified persistence,
  and explicit readiness/dimension evaluation; Handoff Eligible alone is not PASS;
- evidence review closure requires COMPLETE, ADEQUATE, ADMISSIBLE, PASS, CURRENT,
  COMPLETE execution, FULL scope, Closure Eligible YES and Persistence WRITTEN.

### Release handoff variants

1. verified QA_APPROVED signoff for the exact release candidate;
2. QA_NOT_APPROVED, QA_INCOMPLETE, unpersisted signoff or wrong candidate;
3. QA_APPROVED presented directly as release/deployment authority.

Variant 1 is QA evidence only. Release-checklist may normalize it through its exact
Schema 2 evidence index while retaining Gate Decision NOT_EVALUATED and all authorities
NONE. Team-release may consume it only through its exact release-gate request/receipt
policy binding. Variants 2–3 cannot pass the release QA gate or authorize an action.

**Static completion expected**

- all eleven IDs TQA-007 through TQA-017 occur in SKILL and spec;
- exactly eleven primary cases are present and each has explicit expected behavior;
- phases, status axes, canonical paths and schemas match across skill, metadata and spec;
- the formerly damaged Case 1 has a complete heading, fixture and expectations;
- live files, shared/catalog state and old P0 staging are untouched;
- catalog result/timestamp fields remain blank without real execution receipts.

## Required P0 regression matrix

The harness must retain these prior safety properties:

1. missing/unknown/stale/wrong-build smoke blocks at entry with no execution/signoff;
2. automated NOT_RUN/STALE/INVALID/UNKNOWN never becomes PASS;
3. manual PASS requires tester/device/time/per-step actuals/attestation/attachment hash;
4. required BLOCKED/NOT_RUN prevents QA_APPROVED and remains in denominator arithmetic;
5. Team QA never allocates numeric bug IDs or writes canonical bug files;
6. a current FAIL takes QA_NOT_APPROVED precedence while incomplete rows remain visible;
7. playtest/soak completion labels are not readiness PASS; and
8. only exact current complete evidence plus closure-eligible independent review and
   verified signoff persistence can yield QA_APPROVED / Gate Eligible YES.
