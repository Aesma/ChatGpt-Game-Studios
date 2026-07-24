---
name: vertical-slice
description: "Plan and independently evaluate one hash-bound vertical-slice hypothesis using complete prerequisite/scope manifests, finite implementation budgets, immutable build/playtest/velocity evidence, network-aware thresholds, and a deterministic non-overridable verdict."
---

# Vertical Slice

Test whether one representative core loop meets approved experience, technical,
quality, network, and production-feasibility thresholds. Planning, implementation,
build production, playtest capture, evidence assembly, creative advice, formal
evaluation, and recording are separate bounded tasks. This workflow never treats
a multi-week implementation as one conversational changeset.

Read [vertical-slice-contract-v2.md](references/vertical-slice-contract-v2.md)
completely before resolving input. It defines canonical schemas, identity,
limits, prerequisite/status rules, scope closure, batch/checkpoint budgets,
session minima, velocity arithmetic, network profiles, verdict derivation,
currentness, and persistence. Missing, unreadable, or inconsistent contract bytes
return `INPUT_ERROR` with zero writes.

## Invocation and owned writes

Accept exactly one mode:

```text
$vertical-slice plan --request <project-relative-plan-request>@sha256:<64-lower-hex>
$vertical-slice evaluate --request <project-relative-evaluation-request>@sha256:<64-lower-hex> [--persist]
$vertical-slice status --report <project-relative-report>@sha256:<64-lower-hex>
```

Reject no-argument calls, positional inputs, duplicate/unknown flags, malformed
hashes, absolute/unsafe/case-ambiguous paths, globs, directories, symlink escape,
and selectors such as `latest`, mtime, active session, or “current slice.” Paths
use project-relative canonical `/` form and Unicode NFC. Hash exact raw bytes with
SHA-256.

The skill owns only:

- one create-only `plan.md` named by a valid plan request; or
- one create-only `reports/<evaluation-id>.md` named by an authorized
  `evaluate --persist` request.

`status` is strictly read-only. The workflow never writes slice code, worktrees,
branches, build/candidate/batch receipts, raw playtest captures, session receipts,
velocity ledgers, evidence manifests, creative concerns, an index, stage/session
state, gate records, pivot notes, or graveyard entries. Existing owned output
paths are conflicts and are never overwritten.

## Independent status axes

Always report:

```text
Workflow Status: COMPLETE | PARTIAL | BLOCKED | ERROR
Evidence Verdict: PROCEED | PIVOT | KILL | INCONCLUSIVE
Product Decision: PROCEED | PIVOT | KILL | NEW_HYPOTHESIS_REQUIRED | AWAITING
Final Verdict: PROCEED | PIVOT | KILL | BLOCKED_PRODUCT_DECISION_REQUIRED
Currentness: CURRENT | STALE | INVALID
Gate Eligible: YES | NO
Persistence: NOT_REQUESTED | DECLINED | VERIFIED | FAILED
```

Workflow completion is not evidence success. Gate eligibility requires one
read-back-verified, persisted, CURRENT report with Workflow Status COMPLETE and
all three verdict axes PROCEED. No PARTIAL, INCONCLUSIVE, stale, unpersisted, or
advisory-only result advances Pre-Production.

## Phase 0 — Freeze request, workflow, and mutation boundary

1. Hash this skill, the private contract, catalog-declared dedicated spec, exact
   request, and project root/worktree identity.
2. Validate `cgs.vertical-slice-plan-request/v2` or
   `cgs.vertical-slice-evaluation-request/v2` exactly and apply fixed limits.
3. Build the complete ordered source/target manifest. Record path, schema/status,
   raw hash or `ABSENT`, stable IDs, exact fields used, and authority.
4. Capture before-mutation state for every allowed target. Do not recursively
   discover scope or infer missing input.

Request validity authorizes analysis only. Persistence still requires one exact
candidate preview and bounded authorization immediately before a write.

## PLAN mode

### Phase 1 — Validate the prerequisite manifest (VS-005)

Read only the exact `cgs.vertical-slice-prerequisites/v2` manifest and its bounded
source rows. Require project/stage/root/worktree identity, source commit/tree,
engine/version, target platform/configuration, generated-at UTC, manifest hash,
and exactly one row for every required source role defined by the private
contract.

Re-read every row and verify canonical path, unique stable ID, schema, exact
lifecycle status, raw hash, required fields/locators, and cross-source identity.
The project stage must be exactly `PRE_PRODUCTION`. The required sources include
game concept/pillars, systems index, every in-scope system GDD, architecture,
control manifest, every governing ADR, current TR registry/entries when used,
UX/accessibility requirements, engine version, and prior prototype/validation
evidence used to set thresholds.

Missing, duplicate, unreadable, invalid, stale, unapproved, unsupported,
over-limit, or contradictory prerequisites produce stable `VSF-*` findings with
exact path/status/hash/owner/resolution. Return BLOCKED/INCONCLUSIVE with zero
writes. “Key GDDs,” a filename match, quoted prose, template text, or user
assurance cannot satisfy a source role.

### Phase 2 — Validate and freeze scope closure (VS-006)

Read the exact `cgs.vertical-slice-scope-proposal/v2` named by the request. It is
the product owner's explicit scope decision and contains:

- stable hypothesis/question/core-fantasy IDs;
- ordered selected system IDs and exact GDD/requirement/AC IDs;
- start, challenge, resolution, observable loop-completion predicate;
- explicit dependency edges and required asset/UX/network bindings;
- selected/non-selected rows with bounded reasons;
- non-goals, target quality, platform/configuration, and evidence profile; and
- product-owner identity, decision timestamp, and proposal hash.

Compute scope closure against current systems-index/GDD/TR/control evidence. Every
system/AC marked slice-required, every dependency needed for the start→challenge→
resolution path, and every requirement used by a proceed/kill predicate must
appear exactly once. An omitted required node, orphan AC, duplicate/unknown ID,
unresolved dependency, or untraceable “all core systems” statement is BLOCKED.
Changing the core fantasy to justify an omission requires a new hypothesis, not a
local scope edit.

Freeze `cgs.vertical-slice-scope/v2` inside the plan and compute `scope_sha256`
over ordered identity/edge/quality/environment/evidence rows and prerequisite
hashes. The persisted plan candidate is presented to the user in full; approval
binds this scope hash. A later scope change requires a new plan and cannot be
absorbed by an implementation batch.

### Phase 3 — Freeze hypothesis and attempt budget

One `VS-H-*` hypothesis permits exactly attempt `01` and one targeted attempt
`02`. Attempt 03 or higher is `BLOCKED_PRODUCT_DECISION_REQUIRED` with zero
writes.

Require one current `cgs.vertical-slice-attempt-reservation/v2` receipt from the
separate hypothesis-history recorder. It binds registry path/hash/revision/head,
hypothesis, attempt, run ID, request hash, prior report when applicable, unique
reservation ID, owner, and expiry. Attempt 01 requires no prior attempt in the
registry; attempt 02 requires exactly one finalized attempt-01 PIVOT and no prior
attempt-02 reservation/plan. Missing, expired, duplicate, conflicting, or stale
history/reservation evidence is BLOCKED. A new run ID cannot reset an attempt.

Compute `hypothesis_definition_sha256` from question, core fantasy, proceed
criteria, kill rules, measurement definitions, required evidence/network profile,
and decision-matrix contract. Attempt 02 requires the exact CURRENT persisted
attempt-01 PIVOT report and its raw hash; it preserves hypothesis definition,
threshold meanings, and measurement rules and targets only stable prior findings
plus explicit regressions. Changed meaning requires a new hypothesis ID/attempt
01. A second PIVOT cannot schedule another same-hypothesis run.

### Phase 4 — Define finite implementation/checkpoint budgets (VS-007)

Create exact story and batch rows; this remains planning evidence and does not
authorize implementation. Each story row names stable story/scope/AC/finding IDs,
dependencies, exact allowed roots and file-type boundaries, owner role, initial
batch ID, at most one remediation batch ID, build/check commands, fixed command/
wall-time/file/byte limits, required checkpoints, and stop predicates.

Each story permits:

- one separately authorized initial batch;
- at most one separately authorized targeted remediation batch; and
- at most one remediation attempt for each stable failure/bug ID.

Every implementation task must run in an isolated Git worktree and record its
path, branch, base commit/tree, owner, and retention policy. Before mutation, its
owner produces one exact mutation manifest and receives separate authorization.
The main workspace is not a fallback. A new path/system/AC/design rule, command or
time budget exhaustion, build failure, required checkpoint failure, missing
receipt, or unsuccessful remediation immediately ends that batch as PARTIAL or
BLOCKED. It cannot continue “until playable,” retry under a new bug label, or
silently start a third batch.

No implementation batch may start until a separate history-recorder receipt
proves that the exact persisted plan hash consumed the reservation under registry
CAS. This skill never invokes or simulates that recorder.

Each batch receipt is immutable, create-only, and records manifest/pre/post tree
hashes, actual path hashes, commands/exits/log hashes, timestamps, active/blocked
intervals, checkpoint rows, build/candidate IDs, completed scope units, findings,
and result. After all passing planned batches, a separate build owner produces one
final candidate manifest binding exact source/build/platform identity. Any later
source/content/configuration/build change creates a new candidate.

### Phase 5 — Freeze evidence contracts

For each proceed criterion and kill rule, define stable IDs, exact requirement/AC
owners, metric/unit/method, threshold/tolerance, required build/environment,
sample/cardinality, receipt type, evidence owner, and mappings for PASS, FAIL,
NOT_RUN, UNKNOWN, STALE, INVALID, and PARTIAL. Kill rules are objective and fixed
before evidence. They cannot be invented after results, and a playtest-derived
kill predicate is verified only after its own frozen minimum sample passes.

#### Minimum playtest matrix (VS-008)

Select a private-contract evidence profile and include every required cell. The
ordinary experiential profile requires at least three completed full-loop
sessions by three distinct pseudonymous human testers, at least two testers who
are not plan/implementation/build/capture/evaluation owners, and at least one
tester unfamiliar with the slice. Stronger GDD/product thresholds prevail.

Every planned cell names session ID/pattern, tester cohort/role, build/platform/
device/input/environment, start/end conditions, observation method, criteria,
required raw artifacts, and independence rules. Each immutable session receipt
binds one tester/session to the exact candidate/build and records UTC times,
steps/events, completion/blockers, raw path/hash, producer/observer identities,
and attestation. Duplicate testers/sessions, chat answers, summaries, recollected
observations, or unhashed media do not increase cardinality.

Missing testers, sessions, required cohorts/cells, raw captures, build bindings,
or attestations marks affected rows NOT_RUN/UNKNOWN/INVALID and guarantees
Workflow Status PARTIAL and Gate Eligible NO. This sample can validate only the
predeclared slice threshold; it cannot support an unbounded population claim.

#### Velocity ledger (VS-009)

Define stable scope-unit IDs, types, weights, completion predicates, and velocity
thresholds before implementation. Every batch records non-overlapping UTC work
intervals, active/blocked classification, owner, story/finding, pre/post tree,
build ID, completed unit IDs/weights, and exclusions.

The evaluator uses only the private-contract arithmetic: completed unit weight,
active hours, elapsed hours, blocked hours, active throughput, calendar
throughput, and blocked ratio. Estimate text, day labels, issue status, or planned
hours are not observations. Missing/overlapping time, changing unit weights,
unproven completion, absent tree/build identity, zero denominator, or unexplained
exclusions yields UNKNOWN and prevents PROCEED.

#### Network evidence profile (VS-010)

Derive network applicability from the selected systems, core fantasy, GDD/ACs,
and proceed/kill rules. The plan cannot declare `NOT_APPLICABLE` when any of those
requires multi-peer interaction or network feel.

When applicable, freeze peer topology/count, authority mode, target and adverse
latency/jitter/loss/bandwidth cells, warm-up/duration, simulator/tool/version/
configuration, telemetry, session count, and thresholds. Require at least two
real peers controlled by distinct human testers and at least two completed target-
condition sessions, using real conditions or a validated latency simulator. A
local 0 ms session may satisfy only non-network functional rows.

Missing/invalid target cells or peer/telemetry/simulator evidence marks network
rows NOT_RUN/UNKNOWN/INVALID, Workflow Status PARTIAL, and Gate Eligible NO. The
Evidence Verdict is INCONCLUSIVE unless a verified preapproved kill condition
independently establishes KILL; a different non-kill failure cannot replace the
missing network sample, and the result is never unconditional PROCEED.

### Phase 6 — Persist one immutable plan

Render `cgs.vertical-slice-plan/v2` at the request's exact create-only path. It
includes request/workflow/prerequisite identities, hypothesis history/reservation,
frozen scope, all thresholds, story/batch/checkpoint budgets, session/network
matrix, velocity schema, verdict matrix, owner/non-write contract, and plan hash.
It states `implementation_authorized: false`.

Show the full candidate and exact one-file changeset. Obtain one bounded
authorization unless the request already authorizes that exact path/candidate.
Immediately rehash every input and target; any change writes nothing. Create via
same-directory prepared file and atomic replace, flush, reread, validate, and
report the raw plan hash. Failed persistence does not freeze a plan. Stop; do not
implement, build, capture evidence, or evaluate in this task.

The next owner is the hypothesis-history recorder, which must independently CAS
append the exact plan hash and emit a reservation-finalization receipt. Until that
receipt exists, `implementation_authorized: false` remains effective.

## EVALUATE mode

### Phase 7 — Validate one exact evidence graph

The evaluation task identity must differ from every plan, implementation, build,
capture, evidence-manifest, and creative-concern owner. Read only the exact
`cgs.vertical-slice-evaluation-request/v2`, frozen plan, and
`cgs.vertical-slice-evidence-manifest/v2`. Recursively follow only their bounded
ordered manifests, enforce limits, and rehash every referenced raw byte.

Require exact agreement on run/hypothesis/attempt, history reservation and plan-
finalization receipt, hypothesis/scope/plan hashes, prerequisites, source commit/
tree, engine/version, platform/configuration, final candidate/build artifact,
batch receipt set, session/raw-evidence set, velocity ledger, network profile,
criteria, decision matrix, and owner separation. Preserve
missing, wrong-build, stale, malformed, duplicate, unsupported, over-limit, or
partial rows; never omit them to improve a verdict.

Recompute session cardinality/independence, velocity arithmetic, network coverage,
every criterion and kill predicate, and all set hashes. Agent summaries and
manifest labels are claims until the referenced evidence validates.

### Phase 8 — Derive non-overridable evidence and workflow results

Normalize required evidence rows to `PASS`, `FAIL`, `NOT_RUN`, `UNKNOWN`, `STALE`,
`INVALID`, or `PARTIAL`.

Evidence Verdict precedence is:

1. verified current preapproved kill predicate true → KILL;
2. otherwise any required minimum playtest or network cardinality/cell gap →
   INCONCLUSIVE, even when a different non-kill criterion failed;
3. otherwise any verified current required criterion FAIL → PIVOT;
4. otherwise any required row non-PASS or required evidence gap → INCONCLUSIVE;
5. otherwise every required row PASS → PROCEED.

Workflow Status is independently PARTIAL whenever any required row/input is
NOT_RUN, UNKNOWN, STALE, INVALID, missing, or partial—even when a verified kill
predicate controls the Evidence Verdict. Otherwise a completed evaluation is
COMPLETE.
A user, director, reviewer, or agent cannot change the Evidence Verdict or
Workflow Status derivation.

### Phase 9 — Advisory concerns and user product decision

Only after deterministic derivation may the evaluator read an optional immutable
`cgs.vertical-slice-creative-concerns/v2` receipt. It must bind the exact plan,
evidence, candidate/build, hypothesis/attempt, matrix, and recomputed verdict.
Concerns are advisory and may recommend only an allowed conservative downgrade.
They cannot edit evidence/report, waive a threshold/session/network gap, upgrade
to PROCEED, override user PIVOT/KILL, or declare a final result.

Ask the product owner for one decision within the contract matrix. The user may
downgrade evidence, never upgrade it. Attempt-02 PIVOT permits only KILL or
NEW_HYPOTHESIS_REQUIRED. KILL evidence cannot become PIVOT/PROCEED. INCONCLUSIVE
permits KILL or AWAITING. Without an allowed explicit decision, Final Verdict is
BLOCKED_PRODUCT_DECISION_REQUIRED.

### Phase 10 — Persist one immutable evaluation report

Render `cgs.vertical-slice-evaluation-report/v2` with every identity/set hash,
prerequisite/scope/build evidence, criterion rows, complete playtest matrix,
network coverage, velocity operands/arithmetic, missing/invalid evidence,
deterministic derivation, advisory concerns, user decision, attempt history,
currentness predicates, owned/non-write paths, and exact next owner.

`.codex/docs/templates/vertical-slice-report.md` is legacy presentation guidance,
not a schema or evidence source. Do not copy its placeholders, free-text velocity,
single-session counts, or recommendation field as proof.

If `--persist` is absent or declined, return the calculated result with Gate
Eligible NO and Persistence NOT_REQUESTED/DECLINED. If persistence is requested,
show the exact one-file CREATE and full candidate, obtain bounded authorization,
rehash the entire graph and output absence, then create/flush/reread/schema/hash
verify. Only a verified CURRENT COMPLETE/PROCEED/PROCEED/PROCEED report returns
Gate Eligible YES. A write failure returns Persistence FAILED and Gate Eligible
NO. Never update an index/stage/gate in compensation.

## STATUS mode — read-only currentness

Read the exact report bytes and verify the caller-supplied raw hash before parsing.
Rehash its complete bounded referenced graph. CURRENT requires every report, plan,
prerequisite, scope, source/tree, candidate/build, batch, session/raw artifact,
velocity, network, concerns, product decision, workflow contract, and decision-
matrix identity to match.

Any later code/content/configuration/build/evidence/contract mutation makes the
report STALE and Gate Eligible NO; the same filename or a successful rebuild does
not preserve identity. Write nothing and do not refresh the report.

## Final response and stop

Every mode returns `cgs.vertical-slice-run-result/v2` with normalized invocation,
workflow-contract hash, exact IDs/paths/hashes, prerequisite/scope coverage,
attempt/batch budget, evidence/velocity/network completeness, all status axes,
stable findings, mutation snapshot, and next separate owner.

Do not chain into implementation, playtest capture, creative review, report/index
recording, gate check, stage transition, or Production planning. Never claim that
a plan authorizes implementation, one chat playtest validates a general claim,
free-text day logs prove velocity, 0 ms local play proves network feel, or creative
authority replaces evidence.
