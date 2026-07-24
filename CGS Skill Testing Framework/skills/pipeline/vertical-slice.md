# Skill Test Spec: $vertical-slice

## Skill Summary

`$vertical-slice` plans or independently evaluates one exact vertical-slice run.
It requires complete versioned prerequisite/scope evidence, finite story/batch/
checkpoint budgets, immutable multi-session playtest records, reproducible
velocity arithmetic, applicable network-condition evidence, and a deterministic
verdict bound to one candidate build. It never implements the slice or advances
the project stage.

This spec defines expected static and scenario checks for the staged P1 candidate.
It does not claim that a runner executed them. Framework catalog `last_*` result
fields remain unchanged until a real harness records evidence.

## Contract Files

```text
.agents/skills/vertical-slice/SKILL.md
.agents/skills/vertical-slice/agents/openai.yaml
.agents/skills/vertical-slice/references/vertical-slice-contract-v2.md
CGS Skill Testing Framework/skills/pipeline/vertical-slice.md
```

## Static Assertions

### Structure and invocation

- [ ] VS-S001: Frontmatter contains only `name` and non-empty `description`;
      `name` is `vertical-slice`.
- [ ] VS-S002: Invocation accepts only exact hash-bound request/report paths for
      explicit `plan`, `evaluate`, and read-only `status` modes.
- [ ] VS-S003: No-argument, positional, glob, directory, absolute, traversal,
      symlink-escape, case-ambiguous, latest, mtime, and session-inferred scope is
      rejected before mutation.
- [ ] VS-S004: The private v2 contract is read completely and fixed limits are
      applied before source resolution.
- [ ] VS-S005: Owned writes are only one create-only plan or one create-only
      evaluation report; status and all other artifacts are non-writes.
- [ ] VS-S006: Exact candidates receive one bounded approval and full CAS/readback
      verification; existing output paths are never overwritten.

### P0 regression protections

- [ ] VS-S007: One hypothesis permits attempt 01 and one targeted attempt 02 only.
- [ ] VS-S008: Attempt-02 requires an exact current attempt-01 PIVOT report with
      the same hypothesis-definition hash and stable findings.
- [ ] VS-S008A: A CAS-backed hypothesis-history reservation makes each
      hypothesis/attempt unique across run IDs; implementation requires an exact
      plan-finalization receipt.
- [ ] VS-S009: Evidence and Workflow axes are deterministic and cannot be upgraded
      by creative advice, another agent, or product-owner decision.
- [ ] VS-S010: Product owner may conservatively downgrade but cannot upgrade.
- [ ] VS-S011: Plan, implementation, build, capture, evidence assembly, creative
      concerns, evaluation, and recording use distinct task/owner boundaries.
- [ ] VS-S012: Every implementation batch is separately authorized inside an
      isolated worktree; no multi-week conversational changeset exists.
- [ ] VS-S013: Report/evidence bind exact plan, prerequisite, hypothesis, scope,
      source commit/tree, candidate/build, engine/platform, batch, session,
      network, velocity, decision-matrix, and workflow-contract hashes.
- [ ] VS-S014: Any later code/content/configuration/build/evidence/contract change
      makes a report stale and gate-ineligible.
- [ ] VS-S015: Gate eligibility needs verified persisted CURRENT
      COMPLETE/PROCEED/PROCEED/PROCEED and exact candidate/report hashes.

### VS-005 — prerequisite completeness and status

- [ ] VS-S016: Plan consumes exactly `cgs.vertical-slice-prerequisites/v2`.
- [ ] VS-S017: Every required source role has fixed cardinality and admitted
      lifecycle status; adapters are version/hash bound.
- [ ] VS-S018: Each source row binds stable ID, canonical path, raw hash, schema,
      exact fields/locators, applicability, and authority.
- [ ] VS-S019: Required missing/unreadable/invalid/stale/unapproved/unsupported/
      over-limit sources produce stable findings and block with zero writes.
- [ ] VS-S020: “Key GDDs,” filename/prose matches, and user assurances cannot
      substitute for source-role completeness.

### VS-006 — stable scope closure

- [ ] VS-S021: Scope begins from an explicit hash-bound product-owner proposal
      containing stable system/requirement/AC/dependency IDs.
- [ ] VS-S022: Required closure is computed from authoritative slice-required
      markers, start→challenge→resolution, dependency edges, criteria, and
      applicable network/UX/accessibility rows.
- [ ] VS-S023: Every required node/edge appears exactly once; unknown, duplicate,
      orphan, or omitted rows block.
- [ ] VS-S024: `scope_sha256` binds the complete ordered scope and prerequisite
      hashes; approval binds that scope hash.
- [ ] VS-S025: Scope changes require a new plan and cannot be absorbed by a batch.

### VS-007 — finite implementation/checkpoint budget

- [ ] VS-S026: Every story has one initial and at most one remediation batch.
- [ ] VS-S027: Every stable bug/finding has at most one remediation attempt.
- [ ] VS-S028: Each batch has numeric command/time/path/byte limits and exact stop
      predicates; “until playable” is invalid.
- [ ] VS-S029: Required scope/compile/build/AC/budget/receipt checkpoints are
      explicit and the first non-PASS immediately stops mutation.
- [ ] VS-S030: A failed checkpoint produces PARTIAL/BLOCKED evidence; no same-task
      fix loop, relabel, third batch, main-workspace fallback, auto-merge, or
      auto-delete is permitted.

### VS-008 — minimum immutable session matrix

- [ ] VS-S031: CORE_LOOP requires at least three completed full-loop sessions and
      three distinct human testers.
- [ ] VS-S032: At least two testers are independent of producing/evaluating owners
      and at least one is unfamiliar with the slice.
- [ ] VS-S033: Every session receipt binds pseudonymous tester/session, exact
      candidate/build, environment, UTC times/events, raw path/hash, producer/
      observer identities, and attestation.
- [ ] VS-S034: Duplicate, abandoned, wrong-build, stale, unattested, owner-
      conflicted, summary-only, chat-only, or unhashed evidence cannot count.
- [ ] VS-S035: Insufficient cardinality/cells/raw capture makes Workflow PARTIAL,
      Evidence INCONCLUSIVE unless a verified preapproved kill predicate controls,
      and Gate Eligible NO; a different non-kill failure cannot manufacture a
      sampled conclusion.

### VS-009 — observed velocity

- [ ] VS-S036: Scope-unit IDs/types/weights/completion predicates and feasibility
      threshold are frozen before implementation.
- [ ] VS-S037: Ledger rows contain non-overlapping UTC active/blocked intervals,
      owner/story/batch/finding, pre/post tree, build, and completed unit IDs.
- [ ] VS-S038: Completed weight, active/elapsed/blocked time, active/calendar
      throughput, and blocked ratio use the exact v2 formulas.
- [ ] VS-S039: Missing/overlapping time, mutable weights, unproven completion,
      absent tree/build, zero denominator, or unexplained exclusion is UNKNOWN.
- [ ] VS-S040: Estimates, day labels, issue status, commit counts, and prose are
      never velocity observations.

### VS-010 — network profile

- [ ] VS-S041: Network applicability is derived from selected systems/GDD/AC/
      fantasy/criteria and cannot be waived by a local N/A declaration.
- [ ] VS-S042: Applicable plans freeze topology, authority, peers, target/adverse
      latency/jitter/loss/bandwidth, duration, simulator/tool/config, telemetry,
      sessions, and thresholds.
- [ ] VS-S043: Minimum target evidence is two completed target-condition sessions
      with at least two real peers controlled by distinct humans.
- [ ] VS-S044: Simulator evidence records executable/version/config plus observed
      injection telemetry; requested settings alone are UNKNOWN.
- [ ] VS-S045: Localhost/0 ms covers non-network functionality only; missing target
      coverage is PARTIAL and cannot yield unconditional PROCEED.

## Test Cases

### Case 1: Valid plan freezes one complete bounded contract

**Fixture**

- Exact plan request/prerequisite/scope-proposal hashes validate.
- Every required source role is current with an admitted status.
- Authoritative graph has stable system/requirement/AC/dependency IDs and scope is
  closed for one start→challenge→resolution loop.
- Attempt 01 output is absent.

**Expected**

1. Compute hypothesis and scope hashes.
2. Render exact criteria, kill rules, finite story/batch/checkpoints, build
   contract, session/network matrix, velocity schema, verdict matrix, and owners.
3. Preview/authorize/create/readback-verify only `plan.md`.
4. Mark `implementation_authorized: false` and stop.

- [ ] VS-C01-A: No worktree/code/build/evidence/report/index/stage artifact changes.
- [ ] VS-C01-B: Output includes exact plan hash and all explicit non-writes.

### Case 2: VS-005 — missing prerequisite roles block

**Fixture:** prerequisites omit SYSTEMS_INDEX and CONTROL_MANIFEST; one GDD path is
missing and another has native status Draft without an admitted adapter.

**Expected:** emit stable findings naming every role/path/status/hash and owner;
return BLOCKED/INCONCLUSIVE with zero writes.

- [ ] VS-C02-A: Present sources do not hide missing roles.
- [ ] VS-C02-B: Draft is not silently normalized to Approved.
- [ ] VS-C02-C: No scope inference or plan candidate is produced.

### Case 3: VS-005 — duplicate, stale, or unsupported evidence matrix

| Variant | Observation | Expected |
|---|---|---|
| 3a | two GAME_CONCEPT rows | BLOCKED duplicate authority |
| 3b | source raw hash differs | BLOCKED HASH_MISMATCH |
| 3c | unknown schema/status | BLOCKED UNSUPPORTED |
| 3d | status adapter missing hash | BLOCKED INVALID |
| 3e | required accessibility source omitted without N/A authority | BLOCKED ABSENT |
| 3f | source count/bytes exceeds limit | BLOCKED OVER_LIMIT |

- [ ] VS-C03-A: Every failure remains path/role/ID/hash specific.
- [ ] VS-C03-B: User assurance cannot bypass any row.

### Case 4: VS-006 — stable scope closure passes

**Fixture:** proposal selects all authoritative slice-required systems, loop-path
dependencies, requirement/AC rows, applicable UX/accessibility/network bindings,
and exact stories. All IDs/edges are unique and traceable.

**Expected:** compute the least closure, prove set/edge equality, freeze ordered
`cgs.vertical-slice-scope/v2`, and bind user approval to its hash.

- [ ] VS-C04-A: “All core systems” is replaced by explicit stable IDs.
- [ ] VS-C04-B: Scope hash changes when any node, edge, quality, environment, or
      prerequisite hash changes.

### Case 5: VS-006 — “key GDD” omission is blocked

**Fixture:** proposal labels two GDDs “key,” but omits a slice-required inventory
system and one AC on the resolution path. Product prose says they are unnecessary.

**Expected:** report omitted node/edge/AC findings and stop. If removing them
changes the core fantasy, require a new hypothesis.

- [ ] VS-C05-A: Model/user cannot arbitrarily shrink authoritative closure.
- [ ] VS-C05-B: Implementation batch cannot later absorb the omitted system.

### Case 6: VS-007 — compile checkpoint failure stops initial batch

**Fixture:** an external batch owner has an exact authorized manifest. CP-SCOPE
passes; CP-COMPILE fails. Time/path budget remains.

**Expected:** stop mutation immediately, emit immutable PARTIAL/BLOCKED receipt,
and require a fresh targeted remediation task if its one budget remains.

- [ ] VS-C06-A: No build/fix/recompile loop occurs in the initial task.
- [ ] VS-C06-B: Failure receipt contains commands/exits/log hashes and actual paths.
- [ ] VS-C06-C: Vertical-slice planner/evaluator performs no implementation write.

### Case 7: VS-007 — remediation exhaustion and bug relabeling

**Fixture:** initial receipt has `VS-BUG-a`; the one remediation batch fails the
same semantic bug, then proposes `VS-BUG-b` with changed prose to retry.

**Expected:** stable finding identity detects the relabel; story budget is
exhausted; return PARTIAL/BLOCKED and route product/scope decision. No third batch.

- [ ] VS-C07-A: One finding receives at most one remediation attempt.
- [ ] VS-C07-B: Timestamp/prose/line drift cannot reset the budget.
- [ ] VS-C07-C: Worktree is retained unless the user separately decides otherwise.

### Case 8: VS-008 — minimum CORE_LOOP matrix passes

**Fixture:** three completed full-loop sessions bind one candidate build and three
distinct testers; two testers are independent of producer/evaluator roles and one
is unfamiliar. Every receipt has raw capture and attestation.

**Expected:** cardinality passes only after raw receipts/candidate identity and
independence are verified; criteria still use their frozen thresholds.

- [ ] VS-C08-A: One tester cannot count as multiple distinct testers.
- [ ] VS-C08-B: Passing minima are not described as population-wide proof.

### Case 9: VS-008 — insufficient or invalid session evidence matrix

| Variant | Evidence | Expected row |
|---|---|---|
| 9a | one completed session | NOT_RUN / insufficient cardinality |
| 9b | three receipts, same tester | INVALID duplicate cardinality |
| 9c | three testers, no unfamiliar tester | NOT_RUN required cohort |
| 9d | wrong build hash | INVALID |
| 9e | raw video path without hash | UNKNOWN |
| 9f | chat summary only | NOT_RUN |
| 9g | capture/evaluator owner conflict | INVALID |

**Expected:** Workflow PARTIAL, Gate Eligible NO, exact missing cells named;
Evidence INCONCLUSIVE unless a verified preapproved kill predicate applies.

- [ ] VS-C09-A: No self-report or summary backfill occurs.
- [ ] VS-C09-B: Invalid receipts remain visible in the denominator.

### Case 10: VS-009 — velocity arithmetic is reproducible

**Fixture:** completed immutable unit weights total 6; ACTIVE intervals total
18,000 seconds; BLOCKED totals 3,600; elapsed totals 28,800. All rows bind exact
tree/build IDs without overlap.

**Expected arithmetic**

```text
completed_weight = 6
active_hours = 5.000
elapsed_hours = 8.000
blocked_hours = 1.000
active_throughput = 1.200 units/hour
calendar_throughput = 0.750 units/hour
blocked_ratio = 0.167
```

- [ ] VS-C10-A: Operands and rounding are reported.
- [ ] VS-C10-B: The frozen plan selects the deciding throughput/threshold.

### Case 11: VS-009 — velocity UNKNOWN matrix

| Variant | Observation | Expected |
|---|---|---|
| 11a | day labels only | UNKNOWN |
| 11b | planned rather than actual hours | UNKNOWN |
| 11c | overlapping owner intervals | UNKNOWN |
| 11d | unit weight changed after build | STALE/INVALID |
| 11e | completed unit lacks AC evidence | UNKNOWN |
| 11f | pre/post tree or build ID absent | UNKNOWN |
| 11g | active denominator zero | UNKNOWN |

**Expected:** preserve other gameplay PASS rows, return PARTIAL/INCONCLUSIVE and
Gate Eligible NO; never calculate production rate from missing operands.

- [ ] VS-C11-A: Free-text velocity cannot become numeric evidence.
- [ ] VS-C11-B: Exclusions require exact preapproved reasons.

### Case 12: VS-010 — network N/A declaration conflicts with scope

**Fixture:** selected combat GDD and core fantasy require replicated two-peer
combat, but scope proposal declares network profile NOT_APPLICABLE.

**Expected:** derive applicability from authority, create blocker, and refuse the
plan until a complete network profile/matrix exists.

- [ ] VS-C12-A: Product/model prose cannot waive applicability.
- [ ] VS-C12-B: A new non-network fantasy requires a new hypothesis.

### Case 13: VS-010 — 0 ms-only network evidence cannot proceed

**Fixture:** applicable network profile requires target latency/jitter/loss and
two peer sessions. Only passing localhost 0 ms sessions exist.

**Expected:** credit non-network functional rows only; mark network target cells
NOT_RUN, Workflow PARTIAL, Evidence INCONCLUSIVE absent a verified preapproved
kill predicate, and Gate Eligible NO.

- [ ] VS-C13-A: Localhost play is not network-feel evidence.
- [ ] VS-C13-B: Report names exact missing peer/cell/telemetry receipts.

### Case 14: VS-010 — valid simulated network cells

**Fixture:** two target-condition sessions use two real peers controlled by
distinct humans. Receipts bind simulator executable/version/config hash and
observed latency/jitter/loss/bandwidth telemetry to the candidate build.

**Expected:** validate each frozen network threshold and result independently;
requested simulator settings alone are not used.

- [ ] VS-C14-A: Target and adverse cells stay separate.
- [ ] VS-C14-B: Raw telemetry hashes are part of the evidence set.

### Case 15: Missing sample coverage prevents a PIVOT generalization

**Fixture:** one verified non-kill criterion FAIL would otherwise establish PIVOT,
while a required network cell is missing.

**Expected:** Evidence Verdict INCONCLUSIVE; Workflow Status PARTIAL; Gate Eligible
NO; both the independent failed row and missing network cells remain in the
report. The failure may guide remediation but cannot replace the missing minimum
sample unless it is a preapproved kill predicate.

- [ ] VS-C15-A: A non-kill failure does not hide incomplete sample evidence.
- [ ] VS-C15-B: Workflow is not mislabeled COMPLETE.

### Case 16: Same hypothesis stops after one targeted rerun

**Fixture:** attempt 01 CURRENT report is PIVOT; attempt 02 preserves hypothesis
hash and targets findings; its result is again PIVOT; attempt 03 is requested.

**Expected:** attempt 02 permits only KILL or NEW_HYPOTHESIS_REQUIRED; attempt 03
writes nothing and requires a genuinely new hypothesis.

- [ ] VS-C16-A: Stable IDs and prior failure history cannot be reset.
- [ ] VS-C16-B: No automatic new plan/build task is started.
- [ ] VS-C16-C: A new run ID without a unique current reservation writes nothing.

### Case 17: Creative or product authority cannot upgrade

Run variants:

- Evidence PIVOT, creative concerns recommend PROCEED.
- Evidence PROCEED, product owner chooses PIVOT.
- Evidence KILL, product owner asks for PROCEED.

**Expected:** advice cannot change evidence; conservative PIVOT is preserved;
invalid KILL upgrade yields AWAITING/BLOCKED, never PROCEED.

- [ ] VS-C17-A: Evidence is derived before concerns are read.
- [ ] VS-C17-B: Director output has empty write set and advisory authority only.

### Case 18: Report becomes stale after source/build/evidence mutation

**Fixture:** persisted eligible report binds tree T1, candidate C1, build B1,
sessions S1, velocity V1, network N1. Change any one byte or rebuild same filename
to B2.

**Expected:** status rehashes the exact graph, returns STALE and Gate Eligible NO,
and writes nothing.

- [ ] VS-C18-A: Same filename/mtime does not preserve identity.
- [ ] VS-C18-B: Old PROCEED is never refreshed in place.

### Case 19: Wrong-build playtest is not candidate evidence

**Fixture:** plan/current candidate is C2/B2; otherwise-valid session and network
receipts bind C1/B1.

**Expected:** mark receipts INVALID, Workflow PARTIAL, Evidence INCONCLUSIVE absent
higher precedence, Gate Eligible NO.

- [ ] VS-C19-A: Report/candidate/session hashes form one identity chain.

### Case 20: Declined or failed report persistence

**Fixture:** calculated axes are COMPLETE/PROCEED/PROCEED/PROCEED. Variant A omits
`--persist`; variant B authorizes it but write/readback verification fails.

**Expected:** retain calculated conversation result; return Persistence
NOT_REQUESTED/DECLINED or FAILED and Gate Eligible NO; no substitute/index/stage
write occurs.

- [ ] VS-C20-A: Gate evidence requires verified persisted bytes.

### Case 21: Evaluator identity conflicts with an evidence producer

**Fixture:** evaluation task ID equals playtest-capture or evidence-manifest owner.

**Expected:** mark independence invalid and return BLOCKED or PARTIAL/
INCONCLUSIVE according to evaluability; never silently self-attest.

- [ ] VS-C21-A: Separating labels without distinct task identities is insufficient.

### Case 22: Legacy report template is presentation-only

**Fixture:** `.codex/docs/templates/vertical-slice-report.md` is filled with day
logs, one session, and a PROCEED recommendation but lacks v2 identity/evidence.

**Expected:** do not accept it as plan/evidence/report schema or gate proof.

- [ ] VS-C22-A: Placeholder/free-text sections do not satisfy v2 receipts.
- [ ] VS-C22-B: Template recommendation has no verdict authority.

### Case 23: Fully current evidence produces eligible PROCEED

**Fixture:** prerequisites/scope/plan/batches/candidate/build are current; minimum
and stronger session/network matrices pass; velocity operands pass the frozen
threshold; every required criterion PASS; no kill predicate; independent roles;
product owner PROCEED; report create is authorized and verified.

**Expected:** COMPLETE/PROCEED/PROCEED/PROCEED, CURRENT, Persistence VERIFIED,
Gate Eligible YES; exact report/candidate hashes returned; stop for separate gate.

- [ ] VS-C23-A: All eligibility predicates hold simultaneously.
- [ ] VS-C23-B: The skill does not invoke gate-check or update project stage.

## P1 Finding Coverage

| Finding | Contract remediation | Primary cases |
|---|---|---|
| VS-005 | versioned complete prerequisite manifest; fixed roles/cardinality/status/hash/adapters; stable blockers | 2–3 |
| VS-006 | explicit product scope proposal; authoritative graph closure; stable system/requirement/AC/edge IDs; frozen scope hash | 4–5 |
| VS-007 | numeric per-story/batch/finding budgets; required checkpoints; immediate PARTIAL/BLOCKED stop; no repair loop | 6–7 |
| VS-008 | three-session/tester minimum; independence/unfamiliar cohort; immutable build-bound raw receipts | 8–9, 19 |
| VS-009 | immutable weighted units/intervals; fixed formulas and thresholds; missing operands UNKNOWN | 10–11 |
| VS-010 | authority-derived applicability; real-peer target cells; simulator telemetry; 0 ms cannot PROCEED | 12–14 |

## Cross-skill and protocol assertions

- [ ] VS-X001: Catalog spec path remains
      `CGS Skill Testing Framework/skills/pipeline/vertical-slice.md`.
- [ ] VS-X002: A gate consumer receives only an exact CURRENT persisted eligible
      report/candidate hash pair; the workflow does not claim the gate migrated.
- [ ] VS-X003: Plan authorization never authorizes implementation batches.
- [ ] VS-X004: Batch/build/playtest/velocity/network/evidence artifacts remain
      separately owned and immutable.
- [ ] VS-X005: Metadata describes multi-task planning/evaluation, not one-prompt
      implementation.
- [ ] VS-X006: Static/spec validation does not populate catalog execution results.
