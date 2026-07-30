# Architecture Review Ruleset v1

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs.

This file is normative for `$architecture-review`.

```yaml
ruleset_id: cgs.architecture-review-rules/v1
limits:
  max_artifacts_per_shard: 12
  max_index_records_per_shard: 96
  max_typed_edges_per_shard: 48
  max_exact_input_bytes_per_shard: 262144
  max_snapshot_paths_per_batch: 256
  max_reviewers: 2
```

The byte limit is the sum of exact file bytes assigned to one evidence worker,
excluding the small protocol prompt. Never split one artifact into independently
judged semantic fragments. If one required artifact exceeds the byte limit,
record it and its checks as unchecked and return `PARTIAL` unless another
independently proven blocker yields `BLOCKED`. Limits may be lowered for a
smaller available context but never raised ad hoc. Record effective limits.

## Authority and conflict resolution

| Evidence kind | Sole authority | Derived/non-authoritative consumers |
|---|---|---|
| Player-visible product rule and its approval | Current exact-revision owner-approved GDD | Requirement registry, ADR, architecture, story, test |
| Stable technical requirement ID/lifecycle | Owner-approved requirement lifecycle record bound to immutable GDD source text/revision | Traceability and architecture indexes |
| Binding technical decision/lifecycle | Current usable ADR within approved requirement bounds | `architecture.md`, control/traceability indexes, stories |
| Stable system identity and lifecycle enum | Systems-index owner/recorder | GDDs, architecture, planning and review reports |
| Architecture aggregation | No independent authority; `architecture.md` is a derived view | Gate and implementation planning |
| Traceability/coverage index | No independent authority; derived from exact source links | Gate dashboards and reports |
| Implementation claim | Current story/change evidence explicitly linked to governing requirement/ADR | Derived trackers |
| Test execution result | Authoritative test-run evidence store for exact test and target revisions | Stories, reports, dashboards |
| Engine/API compatibility fact | Pinned project VERSION and directly applicable current reference revision | ADR/architecture prose |

Rules of precedence:

1. A derived artifact never fills a missing source link or overrides its source.
2. A lifecycle registry cannot alter GDD source text; mismatch is
   `REGISTRY_DRIFT` and incomplete evidence.
3. A systems index may resolve stable identity and recorded lifecycle only; it
   cannot create product rules, technical requirements, or ADR decisions.
4. An ADR owns a technical decision only inside the approved requirement
   boundary. A reproducible contradiction with that boundary is a blocker; an
   ambiguous boundary is incomplete evidence.
5. Story/test claims prove implementation or execution only through their own
   exact current evidence; they do not create a requirement or decision.
6. Pinned engine references settle compatibility facts only. They do not choose
   product scope or architecture policy.
7. Two current source authorities at the same layer that make mutually
   exclusive claims require the blocker proof below. Source-versus-derived drift
   never makes the derived claim authoritative.

## Strict mode and reviewer plan

| Mode | Required check families | Forbidden check families | Required reviewers |
|---|---|---|---|
| `full` | requirement admission, coverage, ADR consistency/dependencies, engine, contract-required RTM | none inside declared scope | technical-director, lead-programmer |
| `coverage` | requirement admission, Requirement→ADR coverage | ADR all-domain consistency, engine, story/test/run | none |
| `consistency` | keyed ADR conflicts, explicit dependencies, cycles, supersession | GDD requirement admission, engine, story/test/run | technical-director |
| `engine` | pinned engine/API/module compatibility | GDD requirement admission, general ADR conflicts, story/test/run | selected-engine specialist |
| `single-gdd` | target requirement admission and exact Requirement→ADR coverage | unrelated GDDs, general ADR conflicts, engine, story/test/run | none |
| `rtm` | requirement admission, coverage, exact Story→Test→Run chain required by contract | general ADR conflicts and engine review | lead-programmer, qa-lead |

No run uses more than two reviewers. Two required reviewers start concurrently
after the target manifest is frozen. A missing selected-engine identity or role
is reviewer/input incompleteness, not permission to substitute an unrelated
engine specialist.

Reviewer status is exactly `DONE`, `DECLINED`, `TIMEOUT`, `ERROR`, or
`NOT_APPLICABLE`. Required reviewers never use `NOT_APPLICABLE`. Any required
status other than `DONE`, a target-manifest mismatch, missing planned check, or
unchecked critical scope prevents `PASS`.

## Input-class and empty-set rules

Each class has independent `applicability`, `presence`, and `currentness`.
Allowed values are:

- applicability: `REQUIRED | OPTIONAL | NOT_APPLICABLE`;
- presence: `PRESENT | MISSING | NOT_APPLICABLE`;
- currentness: `CURRENT | STALE | UNREADABLE | UNKNOWN | NOT_APPLICABLE`.

`NOT_APPLICABLE` requires an explicit current scope or approved requirement
contract. Never derive it from an empty search.

Apply these empty-set outcomes:

| Condition | Outcome |
|---|---|
| No primary GDD/ADR target for the selected mode | Invocation `ERROR — NO REVIEWABLE ARCHITECTURE SCOPE`; no gate verdict |
| Readable GDDs but zero admitted requirements because IDs/approval/provenance are absent | `PARTIAL` with requirement-baseline incompleteness |
| Admitted explicitly critical/Foundation/Core requirement and zero usable ADR links | Confirmed `BLOCKED` coverage gap |
| Admitted noncritical requirement and zero usable ADR links | `PARTIAL` |
| `consistency` with fewer than two current ADRs | `PARTIAL`; comparisons are incomplete, not `NOT_APPLICABLE` |
| `engine` with missing pinned VERSION or required reference | `PARTIAL` |
| RTM class explicitly not required by every admitted contract | `NOT_APPLICABLE`; no penalty |
| Required story/test/run class absent or stale | `PARTIAL`, except a current `EXECUTED_FAIL` is `BLOCKED` |
| Optional derived architecture/index absent | `MISSING/OPTIONAL`; disclose, no penalty |

## Finding record and stable identity

```yaml
id: ARCH-<rule-slug>-<stable-source-id>-<sequence>
finding_key: <rule-id>:<stable-source-id>:<location-id>
rule_id: <ID from this file>
evidence_class: DETERMINISTIC | INCOMPLETE | INFORMATIONAL
severity: BLOCKER | INCOMPLETE | INFO
disposition: OPEN | INFORMATIONAL | RESOLVED_IN_INPUT
summary: <bounded factual statement>
targets:
  - source_id: <stable requirement/ADR/story/test ID or null>
    path: <canonical project-relative path>
    revision: <exact source revision>
    location: <field, heading, or line>
destination_owner: <actual authority owner>
acceptance_test: <objective evidence needed to close>
producer_finding_ids: []
reviewer_roles: []
accepted_risk_record_ids: []
```

Build the finding key from `rule_id`, sorted stable source IDs, and normalized location IDs. Exclude wording,
severity, reviewer, date, and run ID. The same business IDs retain identity across runs; changed evidence updates the explicit revision and state without changing the finding ID.

Risk acceptance is never a finding disposition. `RESOLVED_IN_INPUT` requires
current versioned evidence satisfying the recorded acceptance test. Reports may
retain imported resolved evidence but never mark an open item resolved from user
permission alone.

## Blocker proof boundary

Except mutation guard, every blocker requires:

1. all cited source artifacts are current, readable, and in the target manifest;
2. stable identity, authority, scope, lifecycle, and applicability are explicit;
3. cited claims are normative and co-applicable, not examples or inference;
4. the violation is reproducible from exact cited bytes; and
5. no explicit exception or valid supersession resolves it.

Unknown owner, criticality, layer, applicability, identity, lifecycle, scope,
unit, revision, or evidence is `INCOMPLETE` and prevents `PASS`; it does not prove
a blocker.

## Rule-to-outcome matrix

| Rule ID | Trigger | Outcome |
|---|---|---|
| `AR.MUTATION.UNAUTHORIZED_CHANGE` | Final guard proves an unauthorized path was added, removed, or changed | `BLOCKER / OPEN` |
| `AR.COVERAGE.CRITICAL_REQUIREMENT_GAP` | An admitted requirement explicitly marked critical/Foundation/Core has no exact current usable ADR link | `BLOCKER / OPEN` |
| `AR.CONSISTENCY.CONFLICTING_CURRENT_ADRS` | Two current usable ADRs make mutually exclusive decisions for the same explicit boundary/resource/interface | `BLOCKER / OPEN` under blocker proof |
| `AR.CONSISTENCY.DEPENDENCY_CYCLE` | Current usable ADR dependency graph has a reproducible directed cycle | `BLOCKER / OPEN` |
| `AR.CONSISTENCY.MISSING_REQUIRED_DEPENDENCY` | A current usable ADR explicitly requires an absent, rejected, stale, or unusable ADR before its decision can hold | `BLOCKER / OPEN` when mandatory/current is explicit; otherwise `INCOMPLETE` |
| `AR.ENGINE.INCOMPATIBLE_CURRENT_DECISION` | Current ADR decision explicitly requires an API/version/module prohibited by current pinned evidence | `BLOCKER / OPEN` under blocker proof |
| `AR.TEST.CURRENT_EXECUTED_FAIL` | Authoritative current run for required exact test/target reports failure | `BLOCKER / OPEN` |
| `AR.REQUIREMENT.CANDIDATE_OR_UNAPPROVED` | Prose lacks stable ID/current lifecycle/source binding/approval | `INCOMPLETE / OPEN`; never allocate an ID |
| `AR.REQUIREMENT.REGISTRY_DRIFT` | Registry source text/path/revision differs from current GDD evidence | `INCOMPLETE / OPEN`; GDD remains product authority |
| `AR.TRACE.UNVERIFIED_LINK` | Only implicit, fuzzy, filename, system-name, ambiguous, or stale relationship exists | `INCOMPLETE / OPEN` |
| `AR.COVERAGE.NONCRITICAL_REQUIREMENT_GAP` | Admitted requirement without explicit critical/Foundation/Core classification has no usable ADR | `INCOMPLETE / OPEN`; unknown criticality also remains incomplete |
| `AR.TEST.STALE_OR_MISSING_EXECUTION` | Required test evidence is stale, discovered-only, absent, ambiguous, or unreadable | `INCOMPLETE / OPEN` |
| `AR.ENGINE.UNKNOWN_REFERENCE` | Required pinned version/reference is missing, stale, unreadable, or does not cover the claim | `INCOMPLETE / OPEN` |
| `AR.INPUT.MISSING_OR_STALE` | Required input class is missing, stale, unreadable, or unknown | `INCOMPLETE / OPEN` |
| `AR.COVERAGE.BUDGET_OR_SHARD` | Artifact/index/edge/byte limit is exceeded or planned shard/check remains unchecked | `INCOMPLETE / OPEN` |
| `AR.REVIEWER.REQUIRED_FAILURE` | Required reviewer is not DONE on exact manifest/check set | `INCOMPLETE / OPEN` |
| `AR.REVIEWER.EVIDENCE_CONFLICT` | Same finding key has incompatible facts, outcome, or evidence revisions | `INCOMPLETE / OPEN`; retain all provenance |
| `AR.DERIVED.DRIFT` | Derived architecture/traceability/index content disagrees with current source authority | `INCOMPLETE / OPEN` only when the derived artifact is required by declared scope; otherwise `INFO / INFORMATIONAL` |

Legacy labels, imported reviewer severity, inferred Foundation/Core wording, or
the number of files never determine the gate outcome.

## Deterministic verdict precedence

After all mode-applicable checks have a state:

1. invalid invocation or no meaningful primary scope: `ERROR`, no gate verdict;
2. any confirmed `BLOCKER / OPEN`: `BLOCKED`, while preserving incomplete items;
3. otherwise any `INCOMPLETE / OPEN`, missing/stale required class, unchecked
   shard, reviewer failure, or mutation-guard incompleteness: `PARTIAL`;
4. otherwise: `PASS`.

`PASS` may contain only `INFO / INFORMATIONAL` findings. It requires final
mutation guard `PASSED`, complete current manifest, all applicable checks DONE,
all required exact links verified, current execution evidence where required,
and every required reviewer DONE on the same manifest.
