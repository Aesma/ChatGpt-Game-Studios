# Contract Specification: `adopt`

## Purpose

This specification validates the `adopt` skill as a bounded, evidence-honest brownfield format audit. The skill may report format gaps, compatibility risks, stable re-audit deltas, and owner-separated handoffs. It may not migrate audited artifacts or claim runtime compatibility.

## Contract identity

- Skill under test: `.agents/skills/adopt/SKILL.md`
- Metadata under test: `.agents/skills/adopt/agents/openai.yaml`
- Primary report schema: `cgs.adopt-report/v1`
- Finding schema: `cgs.adopt-finding/v1`
- Handoff schema: `cgs.adopt-handoff/v1`
- Closure receipt schema: `cgs.adopt-closure-receipt/v1`
- Only accepted stage packet: `cgs.project-stage-detection/v2`

## Invocation matrix

| Invocation | Required behavior |
|---|---|
| `$adopt` | identical to `summary`; no artifact bodies or per-artifact findings |
| `$adopt summary` | canonical inventory, registry/parser coverage, budgets, cost/page preview |
| `$adopt full` | all registered classes, subject to hard ceilings and deterministic paging |
| `$adopt gdds|adrs|stories|infra` | only the selected registered artifact class |
| `--batch N` | one deterministic page anchored to snapshot and registry revisions |
| `--analysis P` | accept only the exact validated `cgs.project-stage-detection/v2` packet |
| `--prior-report P` | focused re-audit anchored to one exact immutable report |

One option in either path/revision pair without the other must produce `ERROR`. Moving aliases such as `latest` must be rejected.

## Required invariants

### A. Mutation and authority

1. Audited artifacts, indexes, registries, packets, prior reports, receipts, and tests remain read-only.
2. The only allowed write is one newly created immutable `docs/adoption/<run_id>.md` report after byte-exact preview and explicit user authorization.
3. Existing reports are never overwritten or amended; a path collision produces `ERROR` and requires a new preview.
4. Report-write approval never authorizes migrations, handoffs, commits, pushes, or publication.
5. The skill never invokes a downstream workflow automatically and always records `auto_executed: false`.

### B. Canonical stage ownership — AD-004

1. Stage context may come only from a version-pinned packet with schema `cgs.project-stage-detection/v2`.
2. Packet validation includes project-root identity, workflow-catalog version/revision, target-snapshot compatibility, and structural completeness.
3. Without a valid packet, stage is `UNKNOWN` or `UNVERIFIED`; the skill does not recreate stage analysis.
4. The skill must not read `production/stage.txt` as stage authority or infer stage from directories, artifact existence, Git history, labels, or prose.
5. Stage context is diagnostic and cannot convert a failed/unsupported rule into a pass.

### C. Versioned format and rule provenance

1. The canonical registry is discovered only through the project-declared catalog/index, never by newest-file or heading heuristics.
2. Registry/index sources used in a decision carry path, schema/version, and declared revision.
3. Artifact format version, parser version, rule ID/version, and registry version/revision are separate fields.
4. Rules specify supported schema IDs/versions/media/encoding, deterministic adapter, objective check, evidence contract, priority, owner, destination schemas, and closure receipt.
5. Missing, ambiguous, unversioned, duplicated, or revision-mismatched rules produce `RULE_UNVERIFIED` and cap the result at `PARTIAL`; substitute rules are not invented.
6. Unsupported versions are not coerced into a nearby supported version.

### D. Bounded discovery — AD-005 and AD-011

1. No-argument mode is `summary` and reads zero artifact bodies.
2. `full` must be explicit.
3. Discovery operates through canonical indexed entries; unbounded recursive content scanning is forbidden.
4. Default ceilings are testable: 256 enumerated entries, depth 6, 20 bodies/batch, 256 KiB/file, 250 KiB parsed/batch, 1 MiB artifact bytes/run, and 4 batches/run.
5. Ordering is deterministic by artifact class, stable artifact identity, and normalized path.
6. A ceiling stops before the next read and emits omitted counts/classes and resume tuple `(snapshot_revision, mode, next_ordinal, registry_revision)`. An initial/summary audit returns `PARTIAL`; a focused re-audit uses the stricter `BLOCKED` convergence terminal.
7. A summary contains counts, known sizes, support declarations, estimated pages/cost, ceilings, expected omissions, and `artifact_bodies_read: 0`.
8. Summary cannot emit per-artifact verdicts or `NO FORMAT GAPS IN SCANNED SCOPE`.

### E. Unsupported and partial coverage

1. Each selected artifact has exactly one coverage state: `SUPPORTED_CHECKED`, `SUPPORTED_NOT_READ`, `UNSUPPORTED`, `UNREADABLE`, `RULE_UNVERIFIED`, or `NOT_APPLICABLE`.
2. Oversized/unreadable artifacts, unsupported formats/media/encodings, missing adapters, and parser failures are explicit coverage entries rather than silent omissions.
3. Any selected unsupported, unreadable, omitted, or rule-unverified item caps the result at `PARTIAL`.
4. Whole-project absence claims are forbidden when coverage is partial or focused.
5. Static `PASS` never proves runtime, semantic, integration, gameplay, build, or deployment compatibility.

### F. Canonical status/schema registry — AD-006

1. Status, rule applicability, parser support, priority, owner, destination schema, and closure semantics come from pinned canonical schemas/registry entries.
2. The skill does not maintain a second inline project-status/template dictionary or derive semantics from headings and examples.
3. Skill-defined audit outcomes and coverage states are orchestration protocol fields, not replacements for project artifact schemas.

### G. Stable finding and evidence model — AD-007

1. Every actionable/unresolved `FORMAT_GAP`, `COMPATIBILITY_RISK`, or `RULE_UNVERIFIED` record conforms to `cgs.adopt-finding/v1`.
2. The finding includes stable ID, kind, priority policy, rule ID/version/source revision, registry identity, artifact identity/path/version/parser, exact target revision, snapshot revision, evidence IDs/locators, coverage/confidence, lifecycle, owner, handoff, closure condition, and prior delta.
3. `finding_id` derives from `(artifact_class, stable_artifact_id_or_PATH_IDENTITY, rule_id, applicability_scope)` and excludes time, target revision, evidence wording, and rule version.
4. Evidence IDs bind finding ID, rule version, target revision, normalized locator, and observation kind.
5. New target bytes change evidence identity without destabilizing the logical finding ID.
6. Rule replacement follows declared lineage or creates a new finding with an explicit relationship.

### H. Focused re-audit closure — AD-008

1. Re-audit requires the exact prior report path/revision and validates schema, run ID, root, snapshots, registry, coverage, findings, and handoffs.
2. Scope is limited to prior unresolved findings, receipt targets, changed manifest entries, changed rules, and the registry-declared bounded regression set.
3. Re-audit makes one deterministic bounded pass and never loops until green.
4. Deltas are one of `UNCHANGED_OPEN`, `EVIDENCE_CHANGED_OPEN`, `CLOSED_IN_THIS_RUN`, `REGRESSION_IN_THIS_RUN`, `RESOLUTION_UNVERIFIED`, `NOT_RECHECKED_BUDGET`, or `NOT_RECHECKED_UNSUPPORTED`.
5. Closure requires both a valid closure receipt and a current rule pass against the new exact target revision.
6. Re-audit budget/one-pass exhaustion produces `BLOCKED` with partial coverage and a resume token. Invalid baseline, repeated snapshot change, or unsafe scope also produces `BLOCKED`.
7. Earlier immutable reports and lifecycle states are never edited.

### I. Immutable run identity and historical diff — AD-009

1. The report uses `ADOPT-RUN-<UTC-basic-milliseconds>-<snapshot8>-<registry8>-<mode>-bNN` and stores full revisions.
2. Report paths are unique run-ID paths, not date-only overwrite targets.
3. A re-audit includes prior report path/revision and finding-by-finding deltas.
4. Timestamps alone do not establish freshness or snapshot identity.
5. Target manifest revision, registry revision, and individual target revisions remain distinguishable.

### J. Typed handoff and failure terminal — AD-010

1. Each finding has a `cgs.adopt-handoff/v1` record with stable ID, linked evidence, owner/workflow, exact preconditions, required input/output schemas, bounded destinations, non-goals, closure receipt contract, and failure behavior.
2. Every handoff starts `authorization_state: NOT_AUTHORIZED` and `auto_executed: false`.
3. Closure receipts identify the finding/handoff, old/new revisions, applied format/rule version, producer run, verification evidence, result, and failure reason.
4. Missing destination, unsupported downstream behavior, invalid/no receipt, or failed verification leaves the finding `OPEN` or `RESOLUTION_UNVERIFIED` and the plan `BLOCKED`/`PARTIAL`.
5. Assignment, a claimed edit, a newer file, or a zero exit status alone cannot close a finding.

## Outcome contract

Exactly one outcome is returned:

- `SUMMARY READY`
- `REPORT READY`
- `NO FORMAT GAPS IN SCANNED SCOPE`
- `PARTIAL`
- `BLOCKED`
- `ERROR`

Every outcome records run identity (or `NOT_MINTED`), mode/batch, index/registry/snapshot identity, stage and prior-report identities, budget consumption, bodies/bytes read, coverage/omissions/resume token, findings/handoffs or `none`, persisted report or `files_written: none`, `runtime_compatibility_proven: false`, and `auto_executed: false`.

## Persistence protocol

Before a write, the exact report bytes, destination, must-not-exist precondition, byte length, revision, and changeset `(create 1, modify 0, delete 0)` must be shown. Any changed bytes/path require a new preview and approval. Immediately before the write, all expected revisions, snapshot/index/registry identities, input paths, and destination absence are revalidated. Mismatch produces `BLOCKED` and no write. After an authorized create, the written revision is verified.

## Static test cases

### Positive

- Default invocation declares summary mode and zero artifact body reads.
- Explicit `full` includes all registered classes but stops at the total run ceiling with deterministic resume data.
- A valid version-pinned detector v2 packet is copied as stage context without secondary stage analysis.
- Same rule/artifact identity across two snapshots retains the finding ID while producing a new evidence ID.
- Focused re-audit closes a finding only when both a valid receipt and current exact-target pass exist.
- An authorized report creates one previously absent run-ID path and verifies its revision.

### Negative

- A stage declaration file or folder heuristic is treated as authoritative.
- Registry rules are inferred from a template/example or a newest file.
- Unsupported format is parsed with a nearby supported adapter and reported as pass.
- Full recursive scan has no entry, byte, depth, batch, or run ceiling.
- Summary mode reads artifact bodies or emits per-artifact findings.
- A finding ID contains a timestamp or target revision and therefore changes on every run.
- Re-audit loops until clean, silently drops prior open findings, or edits the earlier report.
- Handoff execution is implied by report-write approval.
- Existing date-named report is overwritten.
- Static pass claims runtime compatibility.

Any negative case is a contract failure.

## Audit remediation traceability

| Finding | Closure evidence in this contract |
|---|---|
| AD-004 | Section B consumes only `cgs.project-stage-detection/v2` and forbids local stage heuristics |
| AD-005 | Section D defines indexed pagination, per-file/batch/run ceilings, omissions, and resume tokens |
| AD-006 | Sections C/F require a pinned canonical registry and separate protocol states from project schemas |
| AD-007 | Section G defines stable finding/evidence identities and complete provenance |
| AD-008 | Section H defines exact-baseline, one-pass focused re-audit and the required max-limit `BLOCKED` terminal |
| AD-009 | Section I defines immutable run paths and mandatory historical delta binding |
| AD-010 | Section J defines typed handoffs, closure receipts, authorization boundary, and failure terminal |
| AD-011 | Invocation matrix and Section D make `summary` the zero-body default and require explicit `full` |

## Required disclaimer semantics

The result must state that it is a bounded static format audit of exact checked bytes under a pinned registry; unsupported, unreadable, omitted, and unverified scope is explicit; static pass does not prove runtime or downstream compatibility; and no audited artifact or downstream workflow was changed or executed.
