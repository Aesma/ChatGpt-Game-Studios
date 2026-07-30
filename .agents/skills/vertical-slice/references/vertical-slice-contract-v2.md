# Vertical Slice Contract v2

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs.

This is the normative private contract for `$vertical-slice`. `MUST`, `MUST NOT`,
`SHOULD`, and `MAY` are normative. If this reference and the skill disagree, the
workflow returns `INPUT_ERROR` without writing.

## 1. Canonical identity and serialization

- Validate declared identity, schema, version, and revision before use.; render `<explicit-revision>`.
- Canonical structured values use UTF-8, LF, Unicode NFC, sorted map keys, declared
  array order, decimal numbers without exponent notation, and RFC 3339 UTC times.
- Validate an ordered set as revision over `byte_length ":" raw_bytes` records.
- `ABSENT` is a create precondition requiring no entry at the canonical path.
- Paths are project-relative `/` paths after real-path containment, Unicode NFC,
  case-collision, alias, traversal, drive/URI, and symlink checks.
- IDs and revisions are evidence only when their defining schema and raw bytes validate.

Stable IDs use:

```text
VSR-<20-lower-hex>      request
VS-H-<stable-slug>      hypothesis
VS-RUN-<20-lower-hex>  slice run
VS-SYS-<stable-slug>    scoped system row
VS-AC-<stable-slug>     scoped acceptance row
VS-ST-<stable-slug>     implementation story
VS-B-<stable-slug>      implementation batch
VS-BUG-<20-lower-hex>  bug/failure
VS-C-<stable-slug>      proceed criterion
VS-K-<stable-slug>      kill predicate
VS-PT-<stable-slug>     playtest session
VS-VU-<stable-slug>     velocity unit
VS-EVAL-<20-lower-hex> evaluation
VSF-<20-lower-hex>      finding
```

A finding ID revisions schema, hypothesis ID, classification, source/stable-row ID,
normalized observation key, owner, and resolution condition. It excludes prose,
line numbers, timestamps, and current declared revisions. Current evidence remains in the
finding body.

## 2. Fixed limits

Requests MAY set stricter limits but never exceed:

```yaml
max_request_bytes: 262144
max_manifest_bytes: 1048576
max_sources: 512
max_total_source_bytes: 134217728
max_systems: 64
max_acceptance_criteria: 256
max_dependency_edges: 512
max_stories: 32
max_batches: 64
max_commands_per_batch: 32
max_mutation_paths_per_batch: 128
max_findings: 256
max_sessions: 128
max_session_raw_artifacts: 16
max_single_raw_artifact_bytes: 1073741824
max_total_raw_artifact_bytes: 8589934592
max_velocity_units: 256
max_network_cells: 32
max_report_bytes: 2097152
```

Over-limit evidence is explicit `OVER_LIMIT`, not truncated or sampled. Planning
is BLOCKED when required scope exceeds limits. Evaluation is PARTIAL/INCONCLUSIVE
when required evidence cannot be evaluated within the frozen limits.

## 3. Invocation request schemas

### Plan request

`cgs.vertical-slice-plan-request/v2` contains:

```yaml
schema: cgs.vertical-slice-plan-request/v2
request_id: VSR-<20-lower-hex>
project:
  id: <stable-project-id>
  root_identity: <repository/worktree-identity>
  expected_stage: PRE_PRODUCTION
run:
  run_id: VS-RUN-<20-lower-hex>
  hypothesis_id: VS-H-<stable-slug>
  attempt: 01 | 02
prerequisites:
  path: <project-relative-path>
  expected_revision: <explicit-revision>
  schema: cgs.vertical-slice-prerequisites/v2
scope_proposal:
  path: <project-relative-path>
  expected_revision: <explicit-revision>
  schema: cgs.vertical-slice-scope-proposal/v2
hypothesis_history:
  registry_path: <project-relative-path>
  registry_expected_revision: <explicit-revision>
  registry_revision: <nonnegative-integer>
  registry_head: <explicit-revision>
attempt_reservation:
  receipt_path: <project-relative-path>
  receipt_expected_revision: <explicit-revision>
  schema: cgs.vertical-slice-attempt-reservation/v2
prior_report:
  path: <project-relative-path> | NONE
  expected_revision: <explicit-revision> | NONE
output:
  plan_path: production/validation/vertical-slices/<hypothesis>/attempt-<NN>/<run>/plan.md
  expected_state: ABSENT
plan_author_task_id: <stable-task-id>
limits: <section-2-values-or-stricter>
generated_at: <RFC-3339-UTC>
```

Attempt 01 requires prior report NONE. Attempt 02 requires an exact prior report.
The request ID revisions the canonical request without ID/generated-at.

### Evaluation request

`cgs.vertical-slice-evaluation-request/v2` contains:

```yaml
schema: cgs.vertical-slice-evaluation-request/v2
request_id: VSR-<20-lower-hex>
project: <same-project-identity>
run_id: VS-RUN-<20-lower-hex>
hypothesis_id: VS-H-<stable-slug>
attempt: 01 | 02
plan:
  path: <exact-plan-path>
  expected_revision: <explicit-revision>
evidence_manifest:
  path: <project-relative-path>
  expected_revision: <explicit-revision>
  schema: cgs.vertical-slice-evidence-manifest/v2
creative_concerns:
  path: <project-relative-path> | NONE
  expected_revision: <explicit-revision> | NONE
output:
  report_path: <plan-root>/reports/<evaluation-id>.md
  expected_state: ABSENT
evaluation_id: VS-EVAL-<20-lower-hex>
evaluator_task_id: <stable-task-id>
limits: <section-2-values-or-stricter>
generated_at: <RFC-3339-UTC>
```

The evaluator task ID MUST differ from every producing/advisory task ID in the
evidence graph. `--persist` authorizes no write until exact candidate approval.

## 4. Prerequisite manifest (VS-005)

`cgs.vertical-slice-prerequisites/v2` contains project/stage/root identity, source
commit/tree, engine/version, platform/configuration, generated-at, revision algorithm,
an ordered Sources array, and a canonical source-set revision.

Every source row contains:

```text
source_role / stable_id / canonical_path / raw_revision / schema_or_format /
declared_status / exact fields-or-sections used / required / applicability proof
```

Required role and status rules:

| Source role | Cardinality | Admitted status |
|---|---:|---|
| `GAME_CONCEPT` | exactly 1 | `APPROVED` |
| `SYSTEMS_INDEX` | exactly 1 | `APPROVED` |
| `CORE_SYSTEM_GDD` | one per referenced core system | `APPROVED` |
| `ARCHITECTURE` | exactly 1 | `DRAFT_CURRENT` or `APPROVED` |
| `CONTROL_MANIFEST` | exactly 1 | `ACTIVE` |
| `GOVERNING_ADR` | every referenced/required ADR | `ACCEPTED` |
| `TR_REGISTRY` | exactly 1 when TR is used | `CURRENT` |
| `UX_SPEC` | every scope-required UX source | `APPROVED` |
| `ACCESSIBILITY_REQUIREMENTS` | exactly 1 or explicit schema-valid N/A authority | `APPROVED` |
| `ENGINE_VERSION` | exactly 1 | `VERIFIED` |
| `PRIOR_VALIDATION` | every threshold-setting source | `VERIFIED` |

Adapters MAY map a source's exact native token to a canonical status only when the
adapter ID/version/revision is declared in the manifest and supported by the workflow
contract. Unknown statuses do not pass.

The manifest MUST prove completeness from the systems index, GDD dependency
graph, ADR references, TR mappings, and scope proposal. A manifest cannot prove
its own completeness by omitting an authority. A source row is one of
`LOADED_VALID`, `ABSENT`, `UNREADABLE`, `INVALID`, `REVISION_MISMATCH`, `STALE`,
`UNSUPPORTED`, or `OVER_LIMIT`; only LOADED_VALID passes a required role.

## 5. Scope proposal and closure (VS-006)

`cgs.vertical-slice-scope-proposal/v2` contains product-owner identity/decision,
hypothesis/question/core-fantasy IDs, loop start/challenge/resolution IDs, selected
system/requirement/AC rows, dependency edges, asset/UX/network bindings, target
quality, environment/evidence profile, explicit non-goals, proposed stories, and
proposal revision.

Normalize the authoritative graph:

```text
systems index system -> Approved GDD requirement -> active TR/control rule ->
Accepted ADR/dependency -> stable AC -> proposed story/evidence criterion
```

Compute required closure as the least fixed point from:

1. every system/requirement marked `vertical_slice_required` or equivalent exact
   contract field;
2. the declared start/challenge/resolution path;
3. every dependency needed to execute that path at target quality;
4. every system/AC named by proceed/kill criteria; and
5. every network/UX/accessibility requirement made applicable by 1–4.

Every closure node and edge MUST appear once in the selected scope. Selected rows
outside closure need a bounded product reason; they cannot alter the hypothesis.
A required omitted row is a blocker. When authorities lack stable IDs or a
machine-identifiable slice-required predicate, return BLOCKED and route the exact
gap to its design owner; never choose “key” sources heuristically.

`cgs.vertical-slice-scope/v2` freezes ordered system/requirement/AC/edge/story/
quality/environment/evidence rows and prerequisite revisions. `scope_revision` covers
the complete canonical scope. Approval records user identity, UTC time, proposal
revision, scope revision, plan candidate revision, and literal decision.

## 6. Hypothesis and attempt state

`hypothesis_definition_revision` revisions schema/contract version, stable hypothesis
ID, question, core fantasy, proceed criteria, kill predicates, measurement
definitions, network applicability/profile, and decision matrix.

Attempt rules:

| Attempt | Admission |
|---|---|
| `01` | no prior report; first run for hypothesis |
| `02` | exact CURRENT persisted attempt-01 PIVOT report; same definition revision; targeted prior findings plus regressions only |
| any other | invalid, zero writes |

`cgs.vertical-slice-hypothesis-history/v2` is an append-only registry whose rows
bind hypothesis, attempt, run, request, reservation, plan/report revisions, evidence/
final verdict, lifecycle, revision, prior head, event ID, and event revision. A
separate recorder owns it.

Before plan mode, require `cgs.vertical-slice-attempt-reservation/v2` containing:

```text
reservation ID / registry path+ID+base revision+revision+head / hypothesis+attempt /
run+request revisions / prior report identity or NONE / reserved-at+expires-at UTC /
recorder identity / exclusive-lock+version and existence conflict check result / receipt revision
```

The recorder may reserve an attempt only when current history contains no plan or
live reservation for that hypothesis/attempt and the preceding-attempt rules pass.
Plan mode revalidates registry/receipt/expiry immediately before persistence.
After the plan is verified, a separate recorder version and existence conflict check-appends its exact revision and
emits `cgs.vertical-slice-attempt-finalization/v2`. Implementation batch manifests
MUST include that finalization receipt/revision. An unfinalized plan authorizes no
implementation. A different run ID, expired abandoned reservation, filename, or
missing registry row cannot reset history.

An attempt-02 PIVOT/KILL/INCONCLUSIVE result cannot generate another same-
hypothesis plan. Product decision is KILL or NEW_HYPOTHESIS_REQUIRED/AWAITING as
allowed by section 12.

## 7. Story, batch, finding, and checkpoint budgets (VS-007)

Every planned `cgs.vertical-slice-story/v2` row contains story ID, owned outcome,
scope/system/AC IDs, input revisions, dependency IDs, allowed path roots/file types,
owner role, initial/remediation batch IDs, commands, limits, checkpoint schedule,
scope units, and stop predicates.

Hard maxima:

```text
initial batches per story: 1
remediation batches per story: 1
remediation attempts per stable bug/finding ID: 1
same-task build/fix cycles after a failed checkpoint: 0
unplanned mutation paths: 0
```

Each batch request defines stricter numeric command, mutation-path, candidate-byte,
wall-time, and tool-call budgets. A missing numeric budget is invalid; “until
done/playable” is not a number.

Required checkpoint IDs are:

```text
CP-SCOPE       actual paths/changes remain inside manifest and scope
CP-COMPILE     compile/import/schema validation commands complete
CP-BUILD       expected build artifact and receipt validate
CP-AC          assigned AC/Test rows have current evidence
CP-BUDGET      command/time/path/byte limits remain
CP-RECEIPT     immutable batch receipt can be produced
```

Each checkpoint result is PASS, FAIL, BLOCKED, NOT_RUN, or UNKNOWN. The first
non-PASS required checkpoint stops mutation and yields a PARTIAL/BLOCKED receipt.
No in-task repair loop follows. A remediation batch is a fresh task with exact
authorization and may target only stable failures from the initial receipt plus
explicit regression checks. A new failure outside planned remediation scope stops
and routes to product/scope ownership.

`cgs.vertical-slice-batch-receipt/v2` binds run/plan/scope/story/batch, task,
worktree/branch/base/pre/post commit/tree, mutation manifest, planned/actual path
revisions, commands/exits/raw logs, start/end/active/blocked intervals, checkpoint
rows, build/candidate, scope units, findings, result, and receipt revision. It is
immutable and create-only.

## 8. Minimum playtest evidence (VS-008)

Evidence profiles are cumulative:

| Profile | Absolute minimum |
|---|---|
| `CORE_LOOP` | 3 completed full-loop sessions; 3 distinct human testers; at least 2 testers independent of plan/implementation/build/capture/evaluation owners; at least 1 tester unfamiliar with the slice |
| `NETWORK_CORE` | all CORE_LOOP minima plus section-10 target-network cells |
| `CUSTOM_STRONGER` | all applicable minima plus stronger approved GDD/product rows |

One tester/session may satisfy several criterion rows but counts once toward each
distinct-cardinality set. Duplicate/replayed/abandoned sessions do not increase
completed cardinality. The plan may demand more but never less.

Each `cgs.vertical-slice-playtest-session/v2` receipt contains session/tester IDs,
pseudonymous tester cohort/role and independence flags, exact candidate/build/
source/engine/platform/device/input/environment identities, UTC start/end,
full-loop start/challenge/resolution events, per-criterion observations,
completion/blockers, raw artifact path/revision/size/media type, producer/observer
task IDs, consent/redaction classification, attestation, and receipt revision.

Raw evidence is immutable and create-only. A transcript/summary/self-report may be
an observation only when its raw record is bound. Conversation cannot backfill a
missing event, tester, timestamp, build, or declared revision. Wrong-build, stale, duplicate,
unattested, owner-conflicted, missing, or truncated receipts are INVALID/UNKNOWN.

The fixed minima support only the frozen slice threshold and are not statistical
proof of market-wide preference. Any broader claim requires a separately approved
sampling design.

## 9. Velocity evidence and arithmetic (VS-009)

Before implementation, define each `VS-VU-*` with immutable type, positive
rational weight, completion predicate, owner AC/check, and evidence locator.
Changing type/weight/predicate invalidates the plan rather than “re-estimating”
observed velocity.

Each work interval has start/end UTC, classification ACTIVE or BLOCKED, owner,
story/batch/finding IDs, and no overlap with another interval for that owner.
Intervals with end <= start, overlap, missing classification, or implausible
unexplained duration are invalid.

Compute using exact seconds, then display hours to three decimals:

```text
completed_weight = sum(weight of units whose completion predicates validate)
active_seconds = sum(valid ACTIVE interval seconds)
blocked_seconds = sum(valid BLOCKED interval seconds)
elapsed_seconds = final_candidate_receipt_end - first_valid_implementation_start
active_throughput = completed_weight / (active_seconds / 3600)
calendar_throughput = completed_weight / (elapsed_seconds / 3600)
blocked_ratio = blocked_seconds / (active_seconds + blocked_seconds)
```

The plan defines which throughput and threshold decide feasibility and whether
confidence/tolerance rules apply. A zero denominator, missing unit/interval/tree/
build identity, overlapping intervals, unexplained exclusions, or inconsistent
completion makes the velocity criterion UNKNOWN. Estimates, day logs, issue
status, commits alone, and prose are never operands.

## 10. Network profile and evidence (VS-010)

Network applicability is the OR of exact selected system/GDD/AC/core-fantasy/
criterion fields requiring multiple peers, replication, latency-sensitive
interaction, matchmaking, authority transfer, or network feel. An applicable
profile cannot be waived or set N/A by prose.

`cgs.vertical-slice-network-profile/v2` freezes:

```text
topology / authority model / minimum peers >= 2 / distinct human controllers /
target platform / baseline cell / target latency-jitter-loss-bandwidth cells /
at least one adverse cell / warm-up / duration / session count /
simulator-or-real-network method+version+config revision / telemetry fields /
criterion thresholds / PASS-FAIL-invalid mappings
```

Minimum target evidence is two completed target-condition sessions with at least
two real peers controlled by distinct humans. A validated simulator is allowed
only when its executable/version/config revision and observed injection telemetry are
recorded. Requested settings without observed telemetry are UNKNOWN. Localhost/
loopback/0 ms evidence can prove non-network functionality only.

Every network receipt binds exact session/candidate/build, peer IDs/roles,
topology, injection configuration, observed latency/jitter/loss/bandwidth samples,
clock/time basis, events, raw telemetry path/revision, and result. Missing required
cell/peer/session/telemetry/tool identity makes the network criterion NOT_RUN,
UNKNOWN, or INVALID and Workflow Status PARTIAL. Evidence Verdict cannot be
PROCEED.

## 11. Evidence manifest and evaluation

`cgs.vertical-slice-evidence-manifest/v2` is owned by a task distinct from the
evaluator and contains exact run/hypothesis/attempt/history reservation+plan
finalization/plan/scope/prerequisite,
source/candidate/build, engine/platform, ordered batch/session/raw/velocity/network
rows, criterion/kill observations, known gaps, producer identities, set revisions,
generated-at, and manifest revision.

The evaluator independently revalidate and validates the entire bounded graph. A
manifest row never validates itself. Required row statuses are PASS, FAIL,
NOT_RUN, UNKNOWN, STALE, INVALID, or PARTIAL.

A kill predicate is “verified” only when its preapproved build/environment,
method, threshold, sample/cardinality, receipt, and currentness contract all pass.
One session cannot establish a playtest-derived kill rule whose frozen sample is
larger.

Derive Evidence Verdict:

1. any verified current preapproved kill predicate true -> KILL;
2. else any required minimum playtest or network cardinality/cell gap ->
   INCONCLUSIVE, even when another non-kill row is FAIL;
3. else any verified current required criterion FAIL -> PIVOT;
4. else any required row is not PASS -> INCONCLUSIVE;
5. else PROCEED.

Independently derive Workflow Status:

- PARTIAL if any required input/row is NOT_RUN, UNKNOWN, STALE, INVALID, missing,
  over-limit, or partial;
- BLOCKED if identity/scope cannot resolve or no meaningful evaluation is possible;
- ERROR for workflow-contract/runtime failure with no meaningful result; or
- COMPLETE when the bounded evaluation ran and no required input is incomplete.

Report every non-PASS row even when a verified KILL controls Evidence Verdict.
Neither creative concerns nor product decision changes these axes.

## 12. Creative concerns and product decision

`cgs.vertical-slice-creative-concerns/v2` binds plan/evidence/candidate/build/
hypothesis/attempt/matrix/verdict revisions, advisory task ID, ordered concerns,
recommended conservative decision, allowed-write set empty, and receipt revision.
wrong revision, verdict-writing, mutating, or upgrading output is invalid and ignored
as authority.

Product decision matrix:

| Evidence / attempt | Allowed product decisions | Final result |
|---|---|---|
| PROCEED / 01 | PROCEED, PIVOT, KILL | same decision |
| PROCEED / 02 | PROCEED, KILL, NEW_HYPOTHESIS_REQUIRED | PROCEED, KILL, or BLOCKED_PRODUCT_DECISION_REQUIRED |
| PIVOT / 01 | PIVOT, KILL | same decision |
| PIVOT / 02 | KILL, NEW_HYPOTHESIS_REQUIRED | KILL or BLOCKED_PRODUCT_DECISION_REQUIRED |
| KILL / any | KILL, NEW_HYPOTHESIS_REQUIRED | KILL or BLOCKED_PRODUCT_DECISION_REQUIRED |
| INCONCLUSIVE / any | KILL, AWAITING | KILL or BLOCKED_PRODUCT_DECISION_REQUIRED |

The product owner may downgrade but not upgrade. A decision receipt records exact
user identity, evidence verdict, attempt, allowed matrix row, literal decision,
UTC time, and authorization context. Missing/invalid decisions become AWAITING.

## 13. Plan, report, persistence, and currentness

`cgs.vertical-slice-plan/v2` contains all validated prerequisite/scope/hypothesis/
attempt data, criteria/kill matrix, story/batch/checkpoint budgets, build contract,
session/network matrix, velocity schema, owner/non-write rules, authorization,
created-at, and canonical plan revision. It states `implementation_authorized: false`.

`cgs.vertical-slice-evaluation-report/v2` contains:

```text
evaluation/run/hypothesis/attempt / history reservation+plan finalization /
evaluator identity / workflow contract /
plan+prerequisite+hypothesis+scope / source commit+tree / candidate+build artifact /
engine+platform+configuration / batch receipt set / session+raw evidence set /
network profile+receipt set / velocity ledger+operands+arithmetic /
criterion+kill rows / all gaps+findings / creative concerns / product decision /
Workflow Status / Evidence Verdict / Product Decision / Final Verdict /
Currentness / Gate Eligible / Persistence / expires_when / created-at / report revision
```

Owned outputs are create-only. Before persistence, render complete bytes, show one
exact file CREATE, obtain candidate-bound authorization, revalidate every source and
ABSENT target, then write via same-directory prepared file, flush, atomic replace,
reread, schema/revision validate, and snapshot after-state. A failed/declined write
cannot yield VERIFIED persistence or Gate Eligible YES.

CURRENT requires exact matches for report, workflow contract, plan, prerequisite,
scope, all sources, commit/tree, candidate/build, engine/platform/configuration,
all batch/session/raw/network/velocity/concern/decision rows and set revisions, and
the verdict matrix. Any changed identity, explicit revision, or status makes STALE. Status mode
writes nothing.

Gate Eligible YES requires simultaneously:

```text
Workflow Status COMPLETE
Evidence Verdict PROCEED
Product Decision PROCEED
Final Verdict PROCEED
Currentness CURRENT
Persistence VERIFIED
exact current report and candidate/build revisions
```

All other combinations are NO. The report is evidence for a separate gate
consumer; it does not update project stage or invoke the gate.

## 14. Terminal result

`cgs.vertical-slice-run-result/v2` records normalized invocation, contract/request
revisions, mode, source coverage, findings, attempt/batch budget, prerequisite/scope/
session/velocity/network completeness, status axes, owned writes/non-writes,
before/after mutation snapshot, exact output revision or NONE, and next separate owner.

No mode invokes implementation, build, capture, creative, recording, or gate
workflows. A result never claims unexecuted tests, unobserved sessions, estimated
velocity, or untested network conditions as evidence.
