---
name: start
description: "Collects onboarding intent and optional preferences, then recommends one catalog-derived next workflow without self-certifying project stage or bypassing missing concept evidence."
---

# Start

`start` is a read-mostly orientation workflow. It asks what the user wants, consumes
one optional externally persisted `project_stage_detection/v2` packet, records non-authoritative preferences
when requested, recommends one catalog entry, and stops.

It never scans artifact existence to declare work complete, updates authoritative
stage, invokes another workflow, creates project structure, selects an engine, or
runs a director gate.

## Invocation

Use:

~~~text
$start [--analysis <project-stage-detection-v2-path> --expect-analysis <sha256:...>] [--persist]
~~~

Reject unknown or duplicate flags, missing values, directories, unsafe paths, and
positional project/engine/stage names. `--analysis` and `--expect-analysis` are an
inseparable pair selecting exactly one externally recorded detector packet; do not
choose the newest report. Without `--persist`, the workflow is read-only.

## Authority boundaries

Treat these as independent:

1. **Observed state** — exact catalog, optional stage analysis, existing preference,
   and existing configuration bytes may be read and hashed.
2. **Onboarding preference** — `start` may CREATE or UPDATE only
   `production/onboarding/preferences.yaml` after exact changeset authorization.
3. **Authoritative project stage** — only the separate stage owner may update it
   after current evidence gates. `start` always reports
   `Authoritative Stage Mutation: NONE`.
4. **Workflow execution** — a recommendation is not execution authorization.
5. **Implementation/external actions** — no preference or onboarding decision
   authorizes source changes, engine setup, deployment, publication, or messaging.

A user decision, file existence, model inference, analysis proposal, old stage label,
review-mode preference, or accepted risk cannot be recorded as an authoritative gate
PASS. Approval to write preferences never carries to another file or workflow.

## Canonical inputs and output

Read only these fixed routing/configuration inputs when present:

~~~text
.codex/docs/workflow-catalog.yaml
production/onboarding/preferences.yaml
production/stage.txt
production/review-mode.txt
~~~

The only optional variable input is the literal `--analysis` path. The only owned
output is:

~~~text
production/onboarding/preferences.yaml
~~~

If `production/` or `production/onboarding/` is absent, directory creation is a
mutation and must appear in the changeset preview. Never write `production/stage.txt`
or `production/review-mode.txt`; existing values are observed configuration only.

## Status vocabulary

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Analysis State` | `CURRENT`, `PARTIAL`, `STALE`, `INVALID`, `UNAVAILABLE`, `NOT_SUPPLIED` |
| `Stage Authority` | `OBSERVED_ONLY`, `PROPOSED_ONLY`, `UNKNOWN` |
| `Route State` | `READY`, `AT_RISK`, `UNKNOWN`, `BLOCKED`, `NO_ROUTE` |
| `Preference Operation` | `CREATE`, `UPDATE`, `UNCHANGED`, `DECLINED`, `CONFLICT`, `FAILED`, `NOT_REQUESTED` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |
| `Authoritative Stage Mutation` | always `NONE` |

`COMPLETE` means the onboarding interaction produced a transparent recommendation or
stop decision. It never means that a development phase, gate, concept, engine, or
project setup is complete.

## Phase 0: Validate the catalog and minimal state

Resolve literal and real paths, reject symlink escapes and paths outside the project
root, read raw bytes once, and compute full lowercase SHA-256.

### Workflow catalog

Require `.codex/docs/workflow-catalog.yaml` to have a supported schema/version and
unique stable workflow IDs. Each routable entry must define:

- command/display name and artifact types it accepts/produces;
- required predecessor step IDs and evidence types;
- optional/required classification and phase;
- risk flags and whether it can be recommended when evidence is unknown;
- deprecation/replacement metadata when applicable.

The catalog is the only route source. Do not embed or reconstruct a multi-step
roadmap in this skill. If the catalog is missing, invalid, duplicated, or lacks the
needed typed route, set `Route State: BLOCKED` or `UNKNOWN`; do not guess a command.

### Existing preferences and observed configuration

If `production/onboarding/preferences.yaml` exists, read and validate its schema,
raw-byte hash, preference ID, user decision provenance, and catalog/analysis hashes.
A valid file makes persistence an `UPDATE`; absence makes it a `CREATE`. Invalid or
ambiguous existing preferences block writes rather than being overwritten.

Read existing stage/review-mode bytes only to show observed values and raw hashes.
A stage label without its owner/evidence receipt remains `OBSERVED_ONLY`. Do not use
it to skip required catalog steps. A current review-mode value is not immutable; the
user may record a different onboarding preference, but `start` does not apply it to
the authoritative configuration.

## Phase 1: Consume one versioned detection packet or remain unknown

When `--analysis` is supplied, first verify the exact packet bytes against
`--expect-analysis`, then require the complete `project_stage_detection/v2` contract:

- `result`, `detected_stage`, `declared_stage`, `confidence`, and `snapshot_at`;
- target commit, dirty state, and source snapshot hash;
- authority schema/version, record path/hash, owner, and transition source;
- required/valid receipt counts;
- the full ordered evidence list with stable ID, provenance, path, hash, and state;
- contradictions, coverage gaps, advisory observations, recommendation, and the
  `ADVISORY DETECTION ONLY — NOT A GATE OR TRANSITION` disclaimer.

Re-hash the packet and every declared path/receipt against the same snapshot. A
filename, directory, nonempty document, GDD/architecture/source existence, unchecked
status text, or newest artifact can never establish completion. `UNKNOWN`, `CONFLICT`,
`ERROR`, any non-current target, or any INVALID/STALE/UNVERIFIED evidence makes the
analysis unsafe for stage-based routing. Even `DETECTED` is advisory and never gate
or transition authority.

When no packet is supplied, use `Analysis State: NOT_SUPPLIED` and
`Stage Authority: UNKNOWN`. Ask the user's intent, but do not perform a duplicate
stage scan or impersonate a stage analyzer.

This workflow never invokes the detector automatically. If a current packet is required
for a safe route, select the catalog's typed stage-detection entry as the single
recommendation when available.

## Phase 2: Ask the user's onboarding intent

The first visible question asks where the user is starting:

- no idea yet;
- vague idea;
- clear but unformalized concept;
- existing work;
- describe another situation.

For existing work, report only facts from a `CURRENT` analysis receipt. Otherwise say
that project completeness is unknown; do not cite counts obtained from an ad hoc scan.

Collect only routing preferences needed for the next step:

- short free-text intent or idea hint;
- whether the user wants concept formalization before technical work;
- desired review preference: `full`, `lean`, `solo`, or `unspecified`;
- whether they want to record preferences;
- any explicit request to continue despite a missing required concept.

Do not ask the user to choose an engine here. Platform/engine decisions belong to
their typed catalog workflow and current evidence.

## Phase 3: Determine one catalog-derived route

Use the current catalog hash plus the stage analysis:

1. If analysis is CURRENT, locate its first unmet required step by stable workflow ID
   and confirm its evidence dependencies against the catalog.
2. If analysis is missing/partial/stale, recommend the typed stage-analysis entry
   when safe and available; otherwise return `Route State: UNKNOWN`.
3. For a fresh/no-idea intent, select the catalog entry whose declared purpose and
   accepted input type match open concept ideation.
4. For a vague/clear idea, select a concept-authoring or concept-specific review entry
   only when its artifact-type contract accepts `game-concept`.
5. For existing work, never jump to a later phase merely because files exist. Use the
   first unmet required step from current analysis.
6. Return one workflow ID/command, its catalog path/hash, input artifact type,
   prerequisites/evidence, and why it is the first safe next step.

### Artifact-type review routing

A game concept is not a system GDD. A review route is eligible only when the catalog
entry explicitly declares `accepts_artifact_type: game-concept` and a concept-specific
profile. A system-GDD-only rubric is ineligible. If no typed concept reviewer exists,
record a catalog gap and recommend concept authoring/analysis or stop; never send the
concept to a mismatched reviewer.

### Missing-concept risk

If a concept is a required predecessor but the user asks to jump to later technical
work, explain the missing evidence and offer:

- formalize the concept;
- continue with risk recorded;
- stop.

Continuing requires an explicit user decision and creates one immutable preference
record:

~~~text
Risk ID: accepted-risk/missing-concept
State: ACCEPTED_BY_USER
Missing Requirement IDs: <stable IDs>
Selected Workflow ID: <catalog ID>
Consequences: <bounded concrete list>
Decision Owner: user
Decision ID: <stable ID>
Accepted At: <ISO-8601>
Expires/Review At: <milestone or timestamp>
Remediation: <first missing concept step>
Catalog SHA-256: <digest>
Analysis SHA-256: <digest or NOT_SUPPLIED>
~~~

Set `Route State: AT_RISK`, not READY. Set every missing concept/gate item to
`UNSATISFIED`; never mark it complete, passed, waived, or stage-approved. If the user
does not explicitly accept, route to the missing concept step or stop.

Risk acceptance is a preference record only. It does not authorize the selected
workflow, implementation, stage advancement, or any file except the exact preferences
file.

## Phase 4: Build schema-valid onboarding preferences

The exact YAML document uses:

~~~text
Artifact Type: onboarding-preferences
Schema Version: 1
Preference ID: <stable UUID/slug>
Project Root ID: <normalized-root digest>
Catalog Path: .codex/docs/workflow-catalog.yaml
Catalog SHA-256: sha256:<64 lowercase hex>
Analysis Path: <path or NOT_SUPPLIED>
Analysis SHA-256: <digest or NOT_SUPPLIED>
Analysis State: <enum>
Observed Stage Path: <path or ABSENT>
Observed Stage SHA-256: <digest or ABSENT>
Observed Stage Value: <value or UNKNOWN>
Stage Authority: OBSERVED_ONLY | PROPOSED_ONLY | UNKNOWN
Proposed Stage: <analysis proposal or UNKNOWN>
Observed Review Mode Path: <path or ABSENT>
Observed Review Mode SHA-256: <digest or ABSENT>
Observed Review Mode: <value or UNKNOWN>
Review Mode Preference: full | lean | solo | unspecified
Self-Reported Start State: <stable enum>
Intent Summary: <bounded user text>
Selected Workflow ID: <catalog ID or NONE>
Selected Workflow Command: <catalog command or NONE>
Route State: READY | AT_RISK | UNKNOWN | BLOCKED | NO_ROUTE
Decision ID: <stable ID>
Decision Owner: user
Decision Timestamp: <ISO-8601>
Risk Records: <ordered records or NONE>
Authoritative Stage Mutation: NONE
~~~

For UPDATE, preserve unrelated existing preference fields and prior risk/decision
history. Append a new immutable decision event; do not rewrite history. Display a
field-level diff, old/new raw hash, catalog/analysis hashes, all directory/file
operations, and the fact that stage/review-mode files remain unchanged.

If the user chose not to persist, return `Preference Operation: NOT_REQUESTED` and
retain the recommendation in conversation only.

## Phase 5: Authorize, compare-and-set, and persist

For `--persist`, an explicit bounded request may authorize the exact preference
changes. Otherwise preview the complete changeset and obtain one approval.

Immediately before writing:

- re-hash catalog, analysis and every referenced receipt;
- re-read observed stage/review-mode for transparent drift reporting;
- for CREATE, confirm the target and directories have the previewed existence state;
- for UPDATE, require the existing preference raw SHA-256 to equal its preimage;
- revalidate route ID/command against the same catalog bytes.

Any relevant change returns `Preference Operation: CONFLICT`, `Workflow Status:
BLOCKED`, and writes nothing. Do not merge or overwrite concurrent preference edits.

Create missing directories only if previewed. Write the one preference file
atomically, re-read exact bytes, validate schema/enums/references/history, and return
its SHA-256. A directory or file write failure returns `FAILED`; it never implies
preferences or stage were applied.

Declined persistence returns `DECLINED` while still showing the route, analysis
limitations, proposed preferences and unchanged authoritative files.

## Phase 6: Output one recommendation and stop

Return a concise but complete result:

- user intent and decision ID;
- catalog path/hash and selected workflow ID/command;
- analysis path/hash/state and first unmet evidence;
- observed/proposed stage with authority label;
- route state and accepted-risk record if any;
- preference operation/path/preimage/output hash/persistence;
- unchanged stage/review-mode paths/hashes;
- `Authoritative Stage Mutation: NONE`;
- one next action or `Stop`.

Never auto-run the recommendation, print a copied multi-phase roadmap, guess a later
sprint, or reduce the result to a single line that hides conflicts/declined writes.

Verdict mapping:

- invalid catalog/schema/path -> `ERROR` or `BLOCKED`;
- partial/stale analysis that prevents safe routing -> `PARTIAL`;
- declined recommendation or user stop -> `STOPPED`;
- successful interaction with transparent READY/AT_RISK/UNKNOWN route and verified
  persistence state -> `COMPLETE`.

`COMPLETE` is onboarding completion only.
