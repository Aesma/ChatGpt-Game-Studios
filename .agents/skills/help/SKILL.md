---
name: help
description: "Read-only next-action recommender that consumes one current canonical project-stage packet and catalog-bound completion receipts, distinguishes claims and artifact presence from verified approval, and fails closed on conflicts or unreadable evidence."
---

# Studio Help

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

## Invocation and execution

Invoke as:

```text
$help [--analysis <packet-path>] [--context <question-or-recent-activity>]
```

`--analysis` and `explicit request revision` are an inseparable pair. The alternative is
exactly one complete `cgs.project-stage-detection/v2` packet explicitly supplied
in the current invocation or conversation. Reject unknown or duplicate flags,
missing values, malformed expected revisions, directories, traversal,
outside-root paths, symlink escape, both packet input forms, or multiple packet
candidates with `HELP_INPUT_ERROR`.

The optional context is evidence to classify, never an instruction to execute a
workflow and never proof that work completed. Without an explicit packet, return
`HELP_DIAGNOSTIC_REQUIRED` and recommend obtaining one current canonical packet.
Do not invoke `$project-stage-detect`.

This workflow is strictly read-only. It returns exactly one primary action and
never writes, approves, registers, delegates, runs a gate, invokes a skill or
agent, or auto-executes its recommendation.

---

## Phase 0: Validate the canonical stage packet

Resolve exactly one workspace root and record one UTC help snapshot time. For a
path input, verify literal and real paths inside the root, read the explicitly
named regular file, record the authority-supplied artifact revision, and require
exact equality with `explicit request revision` before parsing. Never search for the
newest or nearest packet.

Validate the complete producer-owned `cgs.project-stage-detection/v2` contract.
Require its exact schema/version/completion marker and every producer-required
project, catalog, snapshot, result/resolution, stage/confidence, authority,
receipt, evidence, contradiction, read-error, coverage-gap, blocking-reason,
advisory, recommendation, and disclaimer field. Recompute `packet_id` exactly
under the producer canonicalization rule; do not repair, default, normalize, or
consume individual fields from an incomplete packet.

Require `project.root_id` to match the canonical current root. Read and revision the
exact packet-bound workflow catalog and require the same path/version/declared revision.
Re-read each ordered packet snapshot entry and require its current declared revision or
explicit source state to match the packet and its manifest canonicalization. A
packet-declared `ABSENT` or `UNREADABLE` state may be current when the same state
and linked reason remain reproducible; it blocks stage detection rather than
making the complete diagnostic packet invalid. Timestamp age alone neither
proves nor disproves currentness.

Classify stage context as exactly one of:

| Stage Context | Meaning |
|---|---|
| `CURRENT` | complete packet, project, catalog, packet ID, manifest, and current raw/source states agree |
| `MISSING` | no packet supplied |
| `INVALID` | wrong schema, incomplete fields, bad packet ID, malformed enum, or raw packet revision mismatch |
| `STALE` | current catalog, raw bytes, source state, or manifest differs from the packet |
| `PROJECT_MISMATCH` | packet root identity differs from the current project |
| `UNREADABLE` | packet/catalog cannot be read, or a source declared PRESENT/ABSENT cannot now be checked |

Only `CURRENT` permits any packet field to guide a recommendation. For every
other context, use `detected_stage: UNKNOWN`, do not fall back to local
inference, and return one diagnostic action with the exact context code.

For a CURRENT packet, use its stage result exactly. A normal phase route is
eligible only when packet `result` is `DETECTED`, `resolution_state` is `CLEAR`,
and `detected_stage` is schema-valid. `UNKNOWN`, `CONFLICT`, or `ERROR` produces
`HELP_DIAGNOSTIC_REQUIRED`; preserve declared stage, confidence, contradictions,
read errors, coverage gaps, and blocking reasons in the output.

The detector is diagnostic only. Its stage, authority receipt, confidence,
result, resolution, evidence, or recommendation is never a workflow-step
completion receipt, phase-gate approval, or execution authorization.

---

## Phase 1: Bind the exact workflow catalog

Use only the catalog bytes bound to the CURRENT packet. To route safely, the
catalog must have a supported schema/version and unique stable phase, transition,
step, prerequisite, completion-policy, verification-action, and receipt-schema
IDs. Each routable step must declare:

- command or manual action and accepted/produced artifact types;
- phase, ordered prerequisite IDs, and phase-transition dependencies;
- required, optional, and repeatable semantics;
- exact completion policy and accepted receipt schema/verdict vocabulary;
- evidence locations or indexes, owner/approver policy, freshness/currentness,
  target/source/artifact revision requirements, and supersession rules;
- verification or receipt-producing action for non-verified evidence; and
- deterministic evidence-read limits and safe behavior when evidence is unknown.

If the catalog is missing, malformed, revision mismatched, duplicated, unsupported,
or lacks any policy needed for the earliest relevant required step, return
`HELP_NO_SAFE_RECOMMENDATION` or `HELP_DIAGNOSTIC_REQUIRED`. Do not invent a
command, completion rule, route, phase map, owner, receipt schema, or scan limit.

Catalog artifact globs may locate bounded candidate artifacts only when the
catalog explicitly permits them. A glob match starts as `PRESENT_UNVERIFIED` and
never proves completion. Never count files or use `stage.txt`, directory names,
source extensions, engine configuration, sprint state, or user prose to derive a
phase. Never invoke project-stage-detect or duplicate its algorithm.

---

## Phase 2: Freeze bounded recommendation evidence

Starting from the packet-selected phase and the user's context, build only the
catalog-declared prerequisite and phase-transition closure needed to identify the
earliest unsafe required step. Include all same-level evidence that can conflict
with that step. Do not read unrelated later phases or optional work merely to
offer more suggestions.

Record normalized path, field/section, provenance, declared revision or explicit source
state, snapshot time, expected revision, receipt/run ID, and validation reason for
every item. Re-read and revalidate every readable item before responding. A mid-read
change is `STALE`; never combine observations from different moments.

Honor catalog read-entry, per-entry byte, and total-byte limits. A limit that
would be exceeded produces `UNKNOWN` with `READ_BUDGET_EXCEEDED`; do not truncate
the conflicting set or continue to a later recommendation.

Evidence provenance is one of:

- `COMPLETION_RECEIPT`;
- `SUBJECT_ARTIFACT`;
- `USER_CLAIM`;
- `STATUS_CLAIM`;
- `CATALOG_POLICY`;
- `COVERAGE_GAP`.

Preserve user wording as a bounded `USER_CLAIM` record with a stable evidence ID.
Statements such as “I completed review” remain claims even when they name a real
workflow or match an artifact.

---

## Phase 3: Classify prerequisite evidence

Classify each relevant prerequisite into exactly one state:

| State | Meaning | Satisfies required prerequisite? |
|---|---|---|
| `VERIFIED_PASS` | one current catalog-policy evidence bundle and every required approval/gate receipt validate against current target, source, and artifacts | Yes |
| `CLAIMED` | user, session note, sprint status, or other unverified status source says work is done | No |
| `PRESENT_UNVERIFIED` | artifact or record exists but lacks a valid current completion bundle | No |
| `STALE` | receipt or artifact binds different catalog, target, run, source, input, or artifact bytes, or changed during this read | No |
| `BLOCKED` | current authoritative receipt has a catalog-defined negative verdict such as BLOCKED, FAIL, or REJECTED | No |
| `MISSING` | required artifact, evidence, or receipt is confirmed absent | No |
| `CONTRADICTORY` | current authoritative evidence sources disagree in a way that affects completion | No |
| `UNKNOWN` | required evidence cannot be read, parsed, bounded, or interpreted safely | No |

Apply deterministic precedence for one prerequisite:

1. conflicting current authoritative receipts → `CONTRADICTORY`;
2. one current authoritative negative receipt with no current conflict → `BLOCKED`;
3. one complete current PASS bundle with no conflict → `VERIFIED_PASS`;
4. only mismatched, superseded, changed, or outdated evidence → `STALE`;
5. no valid receipt plus a user or status assertion → `CLAIMED`;
6. no claim plus a merely present artifact/status record → `PRESENT_UNVERIFIED`;
7. confirmed absence → `MISSING`; and
8. access, schema, budget, or interpretation failure → `UNKNOWN`.

List every evidence record even when a higher-precedence state wins. Only
`VERIFIED_PASS` may satisfy or be displayed as completed.

### Completion receipt requirements

A `VERIFIED_PASS` bundle must satisfy the exact catalog completion policy and
bind at least receipt schema/ID, run ID when applicable, catalog step and policy
IDs, accepted PASS verdict, authorized owner/approver, subject artifact paths and
revisions, input/source/target snapshot revisions, catalog version/revision, issue time,
freshness, and supersession/lineage data. revalidate every current revision.

Empty templates, drafts, unchecked status text, receipt filenames, historical
PASS strings, detector evidence, and user recollection remain non-verified.

### Sprint and session status

Treat `sprint-status.yaml`, session state, task notes, and similar sources as
`STATUS_CLAIM`/`CLAIMED` unless the packet-bound catalog declares their exact
schema/version, owner, updated-at/freshness rule, target/source revisions, allowed
status vocabulary, and role in the completion policy. Even a valid status record
does not become `VERIFIED_PASS` unless the full catalog receipt policy explicitly
accepts it and every required receipt/revision also validates.

Unknown, stale, malformed, unauthorized, or unsupported status values are
`UNKNOWN`, `STALE`, or `PRESENT_UNVERIFIED`, never authoritative completion.

### Repeatable steps

For repeatable work, require an exact run ID, receipt ID, requested scope,
current input/source IDs and revisions, subject artifact revisions, catalog revision,
producer identity, verdict, timestamp, and supersession/lineage state. Select
only the non-superseded receipt whose run and scope match the current requested
inputs. Never choose by filename, modification time, directory order, or “last
completed” prose. An R1 receipt for current R2 inputs is `STALE`.

---

## Phase 4: Select exactly one safe primary action

Use this order:

1. If packet context is not CURRENT, recommend obtaining, correcting, or
   refreshing the exact canonical packet.
2. If the current detector result is UNKNOWN, CONFLICT, or ERROR, recommend
   resolving its first structured blocking reason or contradiction.
3. Validate the packet-bound catalog and build the ordered prerequisite closure,
   including required phase-transition receipts. A later detected phase never
   waives an earlier catalog prerequisite.
4. Classify all evidence for the earliest required prerequisite not
   `VERIFIED_PASS` and retain every same-level conflict.
5. Choose one catalog-declared action:
   - `CLAIMED` or `PRESENT_UNVERIFIED` → verification/receipt-producing action;
   - `STALE` → revalidation for current revisions/run;
   - `BLOCKED` → resolve the recorded blocker;
   - `CONTRADICTORY` → reconcile all conflicting current receipts;
   - `UNKNOWN` → diagnose the read/schema/budget failure; or
   - `MISSING` → catalog-declared creation/completion action.
6. Recommend a later required step only when every earlier required prerequisite
   and transition dependency is `VERIFIED_PASS` on the same current snapshot.

Exactly one primary action is allowed. Display every conflict and blocker at the
earliest affected level even when they share one reconciliation action. Optional
or same-priority alternatives may appear only as non-executable context and must
not imply bypass. If no safe catalog action exists, return
`HELP_NO_SAFE_RECOMMENDATION` with the missing contract instead of inventing one.

Never say that a gate passed unless a separate current receipt proves that exact
catalog prerequisite; even then, help reports the receipt and does not own the
verdict.

---

## Phase 5: Return one structured recommendation

Outcomes are exactly:

- `HELP_RECOMMENDATION_READY` — one catalog-backed action is safe to recommend;
- `HELP_DIAGNOSTIC_REQUIRED` — packet, detector result, catalog, or evidence is
  missing, stale, invalid, conflicted, blocked, or unknown;
- `HELP_NO_SAFE_RECOMMENDATION` — no safe catalog-declared action exists; or
- `HELP_READ_ERROR` — a global required read failed and no grounded diagnostic
  action can be selected; or
- `HELP_INPUT_ERROR` — invocation, root, path, or packet selection is invalid.

Return this evidence envelope in conversation only:

```yaml
outcome: <enum>
recommendation_id: <explicit-revision>
help_snapshot_at: <UTC>
stage_context: CURRENT | MISSING | INVALID | STALE | PROJECT_MISMATCH | UNREADABLE
stage_source: cgs.project-stage-detection/v2
packet:
  id: <revision-or-NONE>
  source: <INLINE-or-path-or-NONE>
  raw_revision: <revision-or-NOT_APPLICABLE-or-NONE>
  project_root_id: <revision-or-UNVERIFIED>
  result: DETECTED | CONFLICT | UNKNOWN | ERROR | UNAVAILABLE
  resolution_state: CLEAR | BLOCKED | UNAVAILABLE
  declared_stage: <value-or-UNAVAILABLE>
  detected_stage: <stage-or-UNKNOWN>
  confidence: HIGH | MEDIUM | LOW
  snapshot_manifest_revision: <revision-or-UNVERIFIED>
catalog:
  path: <path-or-UNVERIFIED>
  version: <version-or-UNVERIFIED>
  raw_revision: <revision-or-UNVERIFIED>
primary_action:
  catalog_step_id: <id-or-NONE>
  command_or_manual_action: <one-action>
  affected_prerequisite_id: <id-or-NONE>
  state: VERIFIED_PASS | CLAIMED | PRESENT_UNVERIFIED | STALE | BLOCKED | MISSING | CONTRADICTORY | UNKNOWN | NOT_APPLICABLE
  reason_codes: [<stable-code>]
same_level_conflicts:
  - prerequisite_id: <id>
    evidence_ids: [<id>]
    reason_code: <code>
evidence:
  verified: [<records>]
  claimed: [<records>]
  present_unverified: [<records>]
  stale: [<records>]
  blocked: [<records>]
  missing: [<records>]
  contradictory: [<records>]
  unknown: [<records>]
receipt_run_ids: [<receipt-id/run-id/current-revisions>]
packet_diagnostics:
  contradictions: [<packet contradiction IDs>]
  read_errors: [<packet evidence ID/reason>]
  coverage_gaps: [<packet evidence ID/reason/blocking>]
  blocking_reasons: [<code>]
auto_executed: false
files_written: none
disclaimer: RECOMMENDATION ONLY — NOT A GATE, APPROVAL, OR EXECUTION
```

Compute `recommendation_id` from canonical JSON containing packet ID, packet
snapshot manifest revision, catalog revision, help evidence-snapshot revision, primary step
and action, primary reason codes, and all displayed same-level conflict IDs.
Identical inputs produce the same ID; any identity input change produces a new ID.

Claims must be introduced as “You reported,” present artifacts as “Found but
unverified,” and only `VERIFIED_PASS` records as “Verified done.” Never use a
checkmark or completion wording for any other state.

## Non-negotiable rules

- Never write files, request write authorization, or persist the recommendation.
- Never invoke a recommended workflow, detector, gate, recorder, skill, or agent.
- Never infer stage locally or consume a partial/stale/mismatched packet.
- Never treat artifact presence, user/status claims, or detector output as a
  completion receipt.
- Never hide same-level conflicts to keep the response short.
- Never return more than one primary action.
