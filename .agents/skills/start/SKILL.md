---
name: start
description: "Collect onboarding intent, consume one canonical stage packet, derive one evidence-safe catalog route, and optionally persist versioned non-authoritative preferences without changing project stage or configuration."
---

# Start

`$start` is a bounded onboarding and orientation workflow. It collects user
intent, consumes at most one canonical stage-detection packet, uses the versioned
workflow catalog as the only route/policy source, optionally persists one
non-authoritative preference document, recommends one action, and stops.

It never detects stage itself, treats artifact presence as completion, owns a
gate verdict, changes authoritative stage/review mode, selects an engine, invokes
another workflow, delegates, or auto-executes its recommendation.

## Invocation

```text
$start [--analysis <packet-path> --expect-analysis <sha256:...>] [--persist]
```

Instead of the path pair, the user may explicitly supply exactly one complete
`cgs.project-stage-detection/v2` packet in the current invocation or conversation.
Reject:

- unknown or duplicate flags, missing values, positional engine/project/stage
  names, malformed expected hashes, or repeated `--persist`;
- only one member of the analysis path/hash pair;
- directories, traversal, outside-root paths, or root-escaping symlinks;
- both path and inline packet forms; or
- zero/multiple packet candidates when the user claims to supply one.

Never search for a newest/nearest packet. Without `--persist`, the workflow is
fully read-only. `--persist` authorizes only the exact previewed preference
transaction after all validations and compare-and-set checks succeed.

## Authority and ownership boundaries

Treat these independently:

1. **Canonical stage packet** — diagnostic evidence produced by the separate
   stage detector. It may constrain routing only while complete and current; it
   never becomes gate or execution authority.
2. **Catalog route status** — this run's read-only classification of the exact
   packet-bound catalog prerequisites. It is not an authoritative status file.
3. **Onboarding preferences** — user intent that `$start` may initialize/update
   only at `production/onboarding/preferences.yaml`.
4. **Authoritative stage** — owned by the catalog-declared stage owner and
   transition contract. `$start` always reports `Stage Mutation: NONE`.
5. **Review-mode configuration** — observed only. A different preference may be
   recorded, but `$start` always reports `Review Mode Mutation: NONE`.
6. **Workflow execution** — a recommendation or accepted risk is not execution
   authorization. `$start` always reports `Auto Executed: false`.

Plain `production/stage.txt` is `LEGACY_DECLARATION` only. A user claim, file/
directory presence, detector confidence, preference, director/producer statement,
accepted risk, historical PASS, or status label never establishes stage, gate, or
required-step completion.

## Fixed inputs and only output

Read only these fixed files when present, plus one explicit packet and the bounded
catalog-declared route-evidence closure:

```text
.codex/docs/workflow-catalog.yaml
production/onboarding/preferences.yaml
production/stage.txt
production/review-mode.txt
```

The only owned file is:

```text
production/onboarding/preferences.yaml
```

Creating `production/` or `production/onboarding/` is a mutation and must appear
in the exact changeset preview. Never write stage, review mode, packet, route
status, catalog, receipt, report, session state, source, design, engine, or test
files.

## Result vocabularies

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Stage Packet State` | `CURRENT`, `MISSING`, `INVALID`, `STALE`, `PROJECT_MISMATCH`, `UNREADABLE` |
| `Stage Context` | `DETECTED_CLEAR`, `DIAGNOSTIC_BLOCKED`, `UNKNOWN` |
| `Route State` | `READY`, `AT_RISK`, `DIAGNOSTIC`, `UNKNOWN`, `BLOCKED`, `NO_ROUTE` |
| `Prerequisite State` | `VERIFIED_PASS`, `CLAIMED`, `PRESENT_UNVERIFIED`, `STALE`, `BLOCKED`, `MISSING`, `CONTRADICTORY`, `UNKNOWN` |
| `Preference Operation` | `INITIALIZE`, `UPDATE`, `UNCHANGED`, `NOT_REQUESTED`, `DECLINED`, `CONFLICT`, `FAILED`, `BLOCKED_INVALID_EXISTING` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

`COMPLETE` means only that the onboarding interaction returned a transparent route
or stop decision with an honest persistence state. It never means a concept,
engine, phase, gate, required step, or project is complete.

---

## Phase 0: Freeze root, catalog, and minimal observations

Resolve exactly one workspace root. Reject ambiguous roots and unsafe paths.
Set one UTC snapshot time. Read exact bytes once and compute lowercase SHA-256.

### Bind the workflow catalog

The only route, completion-policy, and transition-policy source is
`.codex/docs/workflow-catalog.yaml`. Require supported schema/version and unique
stable IDs for phases, ordered steps, prerequisites, transitions, completion
policies, verification actions, receipt schemas, artifact types, and risk policy.
Every routable step must declare:

- stable step ID, phase, order, command/manual action, and accepted/produced
  artifact types;
- required/optional/repeatable semantics and ordered prerequisite IDs;
- exact completion policy, accepted receipt schemas/native verdicts, owner,
  currentness/freshness, target/source/artifact hash and supersession rules;
- bounded evidence locations/indexes and read entry/per-entry/total-byte limits;
- verification/receipt-producing action for unverified evidence; and
- risk eligibility plus missing-prerequisite consequences when a later action may
  be recommended at risk.

Every phase transition must declare exact stable transition ID/from/to, gate
profile, required gate-record/receipt schema, PASS/coverage/eligibility threshold,
stage-owner handoff, and advancement action. Do not copy or reconstruct these
inside `$start`.

If any policy needed for the first relevant route is missing, malformed,
duplicated, unsupported, or hash-inconsistent, use `Route State: BLOCKED` or
`UNKNOWN` and name the missing contract. Do not guess a command, roadmap,
transition ID, completion rule, receipt, owner, scan limit, or review profile.

### Observe configuration without authority

Read `production/stage.txt` only as a legacy path/hash/value observation. It never
selects stage or skips a step. Read `production/review-mode.txt` only as observed
configuration and validate its value as full/lean/solo or INVALID. The user may
choose a different preference later; this workflow never changes the file.

Read existing onboarding preferences when present. Validate only under
[references/onboarding-preferences-contract.md](references/onboarding-preferences-contract.md).
An invalid/unsupported existing document produces
`BLOCKED_INVALID_EXISTING`; never treat it as absent or overwrite it.

---

## Phase 1: Consume exactly one canonical stage packet or remain unknown

The producer contract is `cgs.project-stage-detection/v2`. It is conversation-only
by default; therefore accept either one explicit inline packet or one explicitly
recorded path copy with expected raw hash. Do not require the detector itself to
persist a file.

### Validate source and complete schema

For a path packet, verify literal/real path inside root, regular file, exact raw
SHA-256 equality with `--expect-analysis`, then parse. For inline input, preserve
the exact supplied structured packet and recompute its `packet_id` using the
producer canonicalization rule.

Require every producer-owned field: schema/version/completion marker, packet ID,
project root ID, catalog path/version/hash, complete snapshot identity/limits/
manifest/ordered entries, result/resolution/stage/confidence, authority,
receipts, evidence, contradictions, read errors, coverage gaps, blocking reasons,
advisories, recommendation, and diagnostic disclaimer. Do not repair, default,
normalize, or consume selected fields from an incomplete packet.

Require project root ID and packet-bound catalog hash to match this run. Re-read
only the packet's ordered snapshot closure and reproduce every raw hash or
explicit ABSENT/UNREADABLE source state within the packet/catalog limits. Recompute
snapshot manifest and packet ID. Timestamp age alone proves nothing.

Classify packet state:

| State | Rule |
|---|---|
| `CURRENT` | complete packet/ID/root/catalog/snapshot and current source states agree |
| `MISSING` | no packet supplied |
| `INVALID` | wrong schema, missing field, malformed enum/ID, bad raw/path expectation |
| `STALE` | current catalog/source state/hash/manifest differs |
| `PROJECT_MISMATCH` | root identity differs |
| `UNREADABLE` | packet/catalog or reproducible source state cannot be read |

Only `CURRENT` permits packet fields to guide route selection. Even then,
`DETECTED_CLEAR` requires `result: DETECTED`, `resolution_state: CLEAR`, a valid
detected-stage enum, and no blocking contradiction/gap. `UNKNOWN`, `CONFLICT`, or
`ERROR` remains `DIAGNOSTIC_BLOCKED`. The packet is diagnostic and never satisfies
a workflow prerequisite or outgoing gate by itself.

Without a packet, use `Stage Packet State: MISSING` and `Stage Context: UNKNOWN`.
Do not scan artifacts or call/impersonate the detector. A fresh intent may still
receive an initial intent-compatible catalog route without a stage claim. Existing
work may receive only the catalog's typed detector/diagnostic action or UNKNOWN.

This workflow never invokes `$project-stage-detect` or another analyzer. It
consumes one producer packet and preserves its conclusions unchanged.

---

## Phase 2: Ask the onboarding intent and preference delta

Ask one focused start-state question:

- no idea;
- vague idea;
- clear but unformalized concept;
- existing work; or
- another described situation.

For existing work, state project context only from a CURRENT packet. Otherwise
say it is unknown; do not cite ad hoc file counts.

Collect only:

- bounded intent/idea hint;
- concept-formalization preference;
- review-mode preference `full|lean|solo|unspecified`;
- whether preferences should be persisted; and
- explicit missing-concept risk decision if a later risk-eligible route is
  requested.

Do not ask the user to select an engine, stage, gate verdict, or receipt state.
Show observed review mode beside the requested preference and say explicitly that
only the preference may change.

---

## Phase 3: Build one bounded catalog route-status view

This phase classifies route evidence; it does not detect stage or own project
status. Use current catalog bytes and one of two routing bases:

1. **Fresh intent without packet** — select only an initial catalog entry whose
   accepted input type and declared purpose match `open-ideation`, `idea-hint`, or
   `game-concept` authoring. Do not claim a phase or completed prerequisite.
2. **Existing work with CURRENT DETECTED_CLEAR packet** — use the exact detected
   phase and build only the ordered required-step plus outgoing-transition closure
   declared by the packet-bound catalog.

For MISSING/non-current/diagnostic-blocked packet with existing work, do not build
a later-phase closure. Select the catalog's typed packet-refresh/evidence-resolution
action when uniquely declared; otherwise Route State is UNKNOWN/BLOCKED.

### Bounded evidence closure

Starting from the routing basis, read only catalog-declared evidence locations for
the earliest required step that may be unsafe, including all same-level evidence
that can conflict. Honor catalog entry/per-entry/total-byte limits. Stop before a
limit and classify the affected prerequisite UNKNOWN with
`READ_BUDGET_EXCEEDED`; never sample and advance.

Record path, field, provenance, raw hash/source state, expected hash, receipt/run
ID, owner, timestamp, and reason codes. Re-read before output. A changed item is
STALE. Artifact globs may find bounded candidates only when catalog permits; a
match is `PRESENT_UNVERIFIED`, not completion.

Classify each prerequisite using this precedence:

1. conflicting current authoritative receipts -> `CONTRADICTORY`;
2. current catalog-defined negative receipt -> `BLOCKED`;
3. one complete current accepted PASS bundle with no conflict -> `VERIFIED_PASS`;
4. only mismatched/superseded/changed evidence -> `STALE`;
5. only user/session/status assertion -> `CLAIMED`;
6. merely present artifact/record -> `PRESENT_UNVERIFIED`;
7. confirmed absent requirement/evidence -> `MISSING`; and
8. unreadable/schema/budget/interpretation gap -> `UNKNOWN`.

Only `VERIFIED_PASS` satisfies a required prerequisite. A valid bundle must meet
the exact catalog completion policy and bind receipt schema/ID/run, step/policy
ID, accepted verdict, authorized owner, subject/input/source/target hashes,
catalog hash/version, time/freshness, and supersession lineage. Detector evidence,
stage labels, preferences, unchecked status, filenames, and claims never qualify.

For repeatable steps, require exact requested run/scope/input IDs and hashes;
never choose by filename or mtime.

### Gate transition dependency

When all ordered required steps in the CURRENT detected phase are VERIFIED_PASS,
evaluate the catalog's exact outgoing transition dependency. Never derive an ID
from phase names. A gate record can satisfy a transition prerequisite only when
the catalog accepts its exact schema and it is current for the same authority,
source/scope/artifact hashes, transition ID, and profile, with:

```text
schema: cgs.gate-record/v2
coverage.status: COMPLETE
decision.verdict: PASS
decision.advancement_disposition: ELIGIBLE
mutation_guard.status: PASSED
stage_mutated: false
```

`CONCERNS`, `FAIL`, `PARTIAL`, incomplete coverage, accepted risk, a director
opinion, a conversational permission, or a stale/unbound gate record is not PASS.
If the exact PASS record is current but advancement is a separate catalog step,
recommend that stage-owner/advancement action; `$start` never advances. If no
current PASS record exists, recommend the catalog's exact `$gate-check
<transition-id>` action only when it is the earliest unmet required transition
dependency. Never emit phase shorthand or skip a prior required step.

### Select one first safe action

Select exactly the first ordered required prerequisite that is not VERIFIED_PASS:

- CLAIMED/PRESENT_UNVERIFIED -> catalog verification/receipt-producing action;
- STALE -> catalog revalidation action;
- BLOCKED -> blocker-resolution action;
- CONTRADICTORY -> reconciliation action preserving all conflicts;
- UNKNOWN -> diagnostic action;
- MISSING -> declared creation/completion action.

Recommend a later step only when every earlier required prerequisite and
transition dependency is VERIFIED_PASS on the same snapshot. Do not guess sprint
planning or another later workflow because related files exist.

### Concept artifact routing

A game concept is not a system GDD. A concept review route is eligible only when
the catalog entry explicitly accepts `game-concept`, declares a concept-specific
profile, and its prerequisite policy is satisfied. A system-GDD-only
`design-review` route is always ineligible. If no typed concept route exists,
report a catalog gap and select concept authoring/diagnostic action or Stop.

### Missing-concept accepted risk

When a concept prerequisite is not VERIFIED_PASS and the user requests a later
technical action, a later route may be `AT_RISK` only when the current catalog
explicitly declares that action risk-eligible and supplies consequence/remediation
IDs. Explain the exact missing prerequisite states and offer formalize, explicitly
accept bounded risk, or Stop.

Explicit acceptance creates `accepted-risk/missing-concept` under the preference
schema, bound to decision owner/time, missing prerequisite IDs, selected catalog
step, consequence codes, expiry/review, remediation step, catalog hash, and packet
ID. Missing steps remain unsatisfied. Risk does not create VERIFIED_PASS, gate
PASS, stage approval, workflow execution, or write authority outside preferences.

---

## Phase 4: Build or update schema-valid preferences

Read [references/onboarding-preferences-contract.md](references/onboarding-preferences-contract.md)
in full. Apply `cgs.onboarding-preferences/v2` exactly.

- Target absent -> `INITIALIZE`.
- Valid schema-2 target -> `UPDATE`, preserving preference identity, created time,
  prior decision/risk history byte-for-byte and appending one decision event.
- Invalid/unsupported target -> `BLOCKED_INVALID_EXISTING`; no overwrite/migration.
- No requested persistence -> `NOT_REQUESTED`; keep proposal in conversation.

Record packet identity/state, catalog identity, observed legacy stage/review mode,
requested preferences, selected route/status, decision history, risk records, and
the fixed no-authority/no-auto-execution boundary. Do not record `Proposed Stage`
as if `$start` owned a stage decision; store only diagnostic packet stage/state.

For UPDATE, show the field-level old/new diff. Always show observed review-mode
value/hash next to requested review-mode preference and show that the actual config
will remain unchanged.

---

## Phase 5: Preview, authorize, CAS, and persist

For persistence, show the complete one-file changeset and proposed bytes/hash,
including every missing directory. An explicit bounded `--persist` request may
authorize that exact preview; otherwise obtain one approval. Never re-prompt per
directory or field.

Immediately before writing, follow the preference contract's compare-and-set:

- revalidate catalog, complete packet/current snapshot, route evidence closure,
  observed legacy stage/review mode, preference preimage/absence, and parent
  directory states;
- require every state/hash to equal the preview;
- on any difference return `CONFLICT`, write nothing, and do not merge/retry;
- after successful CAS, create only previewed directories, atomically publish one
  file, re-read exact bytes, verify output hash/schema/IDs/history/references; and
- confirm stage/review-mode bytes or source states were not changed by `$start`.

Declined persistence is `DECLINED`; write failure is `FAILED`. Neither hides the
route, limitation, proposed bytes, or authoritative files remaining unchanged.

---

## Phase 6: Return one transparent result and stop

Return:

- user start state, intent, decision ID/owner;
- catalog path/version/hash;
- stage packet source/path-or-inline, raw hash where applicable, packet ID,
  snapshot hash/state/result/resolution/stage/confidence;
- observed legacy-stage and review-mode path/hash/value with non-authority labels;
- ordered route-status rows through the first unmet required prerequisite,
  including evidence/receipt IDs and every same-level conflict;
- exact selected catalog step/command or manual action, affected prerequisite,
  route state and reason codes;
- accepted-risk record, if explicitly created;
- preference operation/path/preimage/output hash/persistence/conflicts;
- `Stage Mutation: NONE`, `Review Mode Mutation: NONE`, `Auto Executed: false`;
  and
- exactly one next action or `Stop`.

Do not print a copied multi-phase roadmap, auto-run the recommendation, imply a
later step is unblocked, or collapse the result to one success line that hides
MISSING/INVALID/STALE/CONFLICT/DECLINED/FAILED state.

Status mapping:

- invalid invocation/root -> `ERROR`;
- invalid catalog, invalid existing preferences, unsafe route conflict ->
  `BLOCKED`;
- missing/stale/invalid packet or incomplete route evidence preventing a safe
  returning-project route -> `PARTIAL`;
- user Stop or declined onboarding interaction -> `STOPPED`;
- transparent completed interaction with honest route and persistence state ->
  `COMPLETE`.

`COMPLETE` is onboarding completion only. Stop without invoking anything.
