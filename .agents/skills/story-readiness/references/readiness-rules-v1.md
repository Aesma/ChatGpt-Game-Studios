# Story Readiness Rules v1

This file is normative for `$story-readiness`. **Must**, **must not**, **required**,
and **exactly** are contractual.

## 1. Canonical serialization and identity

Raw source identity is lowercase SHA-256 over exact file bytes. Display it as
`sha256:<64-lowercase-hex>`. Do not hash normalized/copy-pasted text in place of
raw bytes. Structured analysis records use canonical JSON: UTF-8, Unicode NFC
strings, LF within strings, lexicographically ordered object keys, array order
preserved where declared significant, no insignificant whitespace, and decimal
integers without leading zeroes.

Canonical project-relative paths use `/`, repository-canonical casing, and no
absolute root, drive, URI, traversal, glob, or external symlink target. A path
resolving to zero or multiple case-equivalent entries is invalid.

Stable story IDs must be explicitly declared and unique within every loaded
story/sprint/scope set. Do not derive IDs from filenames, titles, array ordinal,
or line number.

### cgs.story/v2 producer adapter

Production stories are parsed through exactly one explicit adapter. The only
gate-eligible adapter in this ruleset is:

```text
adapter_id: cgs.story-v2-readiness-adapter/v1
producer_schema: cgs.story/v2
producer_skill: .agents/skills/create-stories/SKILL.md@sha256:69064777acf168b7419a1d087d8b8aa28c22a1bc951f750be46a9109d73062af
producer_contract: .agents/skills/create-stories/references/story-authoring-contract.md@sha256:bec6a68249474f16c21085983e684aa71a467d886191f3c1b01e5064f8780102
producer_bundle_sha256: sha256:1f27d98b62b1ceb2be4c54f6d52a053502f54989a67cf8b801dd11afc924b97f
producer_bundle_preimage: exact SKILL bytes || 0x00 || exact contract bytes
```

The adapter must independently recompute both raw hashes and the bundle hash and
bind them in the readiness context. Any absence or mismatch is `UNSUPPORTED` with
`MIGRATION_REQUIRED`; a remembered or caller-supplied hash is not evidence. The
adapter accepts only one unambiguous exact
`Schema: cgs.story/v2` marker. Missing, duplicate, legacy, mixed, or future schema
markers set the story source status to `UNSUPPORTED`; `SR-C001` is `FAIL` when a
stable story identity can still be reported and `BLOCKED` otherwise. The result
must name `MIGRATION_REQUIRED` as the resolution condition. It must not guess a
schema from headings, paths, fields, or old IDs.

The adapter consumes these producer-owned identity fields exactly once:

```text
Story ID: STORY-<16 lowercase hex>
Story Slot: SNNN
Epic ID: <stable ID>
Canonical Path: production/epics/<epic-slug>/story-NNN-<display-slug>.md
Revision: <positive monotonic integer>
Source Manifest ID: sha256:<64 lowercase hex>
Story Core SHA-256: sha256:<64 lowercase hex>
Story Status: AUTHOR_COMPLETE | NEEDS_WORK | BLOCKED | RETIRED
Readiness Verdict: NOT_EVALUATED
Readiness Evidence: NONE_CURRENT
```

The internal path, epic slug, story numeric path slot, and `Story Slot` must agree.
Only `AUTHOR_COMPLETE` can become readiness `READY`; producer `NEEDS_WORK` fails
the applicable checks, and producer `BLOCKED`/`RETIRED` blocks implementation.
Producer status never substitutes for this independent readiness verdict.

The adapter validates the complete `Source Manifest and Currentness Matrix` and
reconstructs the producer manifest identity using its specified canonical ordered
source/target-manifest algorithm: UTF-8/LF canonical JSON, lexicographic object
keys, and arrays sorted by role, stable ID, canonical path, and scope. Every
required row binds role, stable source ID, canonical path, current raw hash or
exact ABSENT state, schema/revision/status/currentness, scope, and the stable
locators used by the story. The reconstructed identity must equal `Source Manifest
ID`; every loaded source byte/state/path/revision/membership/role/scope/evidence
value must equal its row. Missing, duplicate, ambiguous, extra-authoritative,
unsupported, non-current, or mismatched rows fail closed. A copied digest without
the complete current matrix cannot pass.

Recompute `Story Core SHA-256` from the producer-defined canonical story source/
scope/slice/AC/dependency payload, excluding QA specifications, advisory review,
final-readiness fields, revision history, generated time, and all hashes. Compare
the result byte-for-byte with the declared value. The adapter must not invent a
different core projection or trust the label without recomputation.

`Manifest Version`, `Manifest Hash`, `## Source Snapshot`,
`AC-<story-id>-<three-digits>`, and `TEST-<story-id>-<three-digits>` are not
`cgs.story/v2` producer requirements. Their absence cannot fail a v2 story; their
presence cannot satisfy or override Source Manifest, Story Core, currentness,
AC, or Test checks. Legacy layouts are not silently coerced through this adapter.

## 2. Fixed limits and scope manifest

Hard caps per run:

| Resource | Maximum |
|---|---:|
| Stories evaluated per page | 32 |
| Stories declared by one all-scope manifest | 2,048 |
| Total source files read per page | 1,024 |
| Total source bytes per page | 67,108,864 |
| Bytes per story/GDD/ADR/plan/control source | 2,097,152 |
| Reference depth | 8 |
| GDD/TR/ADR/control references per story | 128 |
| Acceptance criteria per story | 100 |
| Test IDs per story | 256 |
| Dependencies per story | 64 |
| Asset references per story | 128 |
| QA packets/reviewer results per page | 32 |
| Findings per story | 256 |
| Paths displayed per gap class | 128 |

`cgs.story-readiness-scope/v1` contains schema, project ID, canonical root,
target commit/ref and dirty-state receipt, ordered entries of stable story ID,
canonical path, raw SHA-256 and byte size, generated-at UTC, generator identity,
and normalized manifest hash. Duplicate ID/path, missing hash, path outside
`production/epics/`, target mismatch, or a source byte mismatch is `INPUT_ERROR`.

The deterministic continuation cursor contains schema, project/target ID, scope
manifest hash, next zero-based ordinal, completed ordered result-key hash,
ruleset/checker hash, current-context snapshot hash, issued-at, and cursor hash.
A mismatch returns `INPUT_ERROR`; never reuse completed rows under a changed
cursor context.

Specific-story and sprint scopes use the same limits. Over-limit required input
makes only the affected story `evaluation_state: PARTIAL` unless scope identity
cannot be resolved at all. Never silently sample, truncate findings, or issue a
whole-scope count from a page.

## 3. Source status and current-context snapshot

Every attempted source entry is:

```text
LOADED_VALID | ABSENT | UNREADABLE | INVALID | HASH_MISMATCH |
STALE | UNSUPPORTED | OVER_LIMIT
```

`cgs.story-readiness-context/v1` contains project/target/dirty identity, story
identity, selected story adapter ID and producer SKILL/contract/bundle hashes,
review mode/source,
production-control applicability, ordered source
entries, sprint evidence where applicable, fixed-limit usage, created-at UTC,
checker/ruleset identity, normalized snapshot hash, and stale key.

Each source entry contains role, path, raw hash/bytes or absence, schema/parser
version, status, used fields/sections with stable locators, internal identity,
relationship to the story, and limitation. The snapshot includes:

- story file;
- complete producer Source Manifest and Currentness Matrix plus every row source;
- systems index and exact system row;
- exact system GDD and requirement row(s);
- TR registry and referenced TR rows;
- control manifest and applicable rule locators;
- every governing ADR;
- every dependency story and asset path/producer story;
- every imported QA plan and all of its captured sources;
- technical preferences and the configured engine-version reference when engine
  or performance checks apply;
- review-mode source; and
- sprint tracker adapter/schema/raw hash/revision/event/unique ACTIVE declaration,
  selected `plan_file` raw hash/revision/story set, plan stories, and session,
  project-stage, and current-milestone corroboration for sprint scope.

`production/session-state/active.md` is supporting current-context evidence only.
It cannot override an explicit story, requested sprint ID, tracker, plan, story
bytes, or a source-of-truth hash.

Production control is required when the story path is under `production/epics/`
or the story contains any of: `Schema: cgs.story/v2`, `Story ID:`, `Story Slot:`,
`Source Manifest ID:`, `Story Core SHA-256:`, `Story Status:`, `Layer:`, `Type:`,
`TR-`, `Governing ADR`, stable AC or Test IDs, or an implementation/evidence path.
Legacy `Status: Ready`, `Status: Ready for Dev`, `Manifest Version:`, or `Manifest
Hash:` also triggers production classification but does not select the v2 adapter.
This classification is made from story/path evidence before checking whether an
authority exists.

## 4. Exact sprint resolution

Sprint scope reads exact raw bytes of `production/sprint-status.yaml`, computes
and records its raw SHA-256, and selects exactly
`cgs.sprint-tracker-v2-readiness-adapter/v1` only when the top-level
`schema_version` is exactly `cgs.sprint-tracker/v2`. Unknown, absent, duplicate,
mixed, or legacy schema is `UNSUPPORTED`; return `RUN_BLOCKED` with
`MIGRATION_REQUIRED`. Never try another adapter heuristically. Legacy
`plan_path`/`plan_hash` aliases are not consumed by this branch and cannot satisfy
missing `plan_file`/`plan_sha256`.

The tracker must contain exactly one of each required field and pass this authority
tuple:

```text
tracker_revision: positive integer
event_id: stable nonblank ID
sprint_id: exact requested stable sprint ID
active_sprint_id: exactly equal sprint_id
sprint_state: ACTIVE
lifecycle_owner: stable nonblank authority/owner ID
lifecycle_recorder: cgs.sprint-tracker/v2
plan_file: one safe canonical project-relative regular-file path
plan_sha256: sha256:<64 lowercase hex> over exact raw plan bytes
plan_revision: exact cgs.sprint-plan/v2 planning-payload revision
story_set_hash: sha256:<64 lowercase hex>
updated_at: timezone-qualified instant
goal / start_date / end_date / IANA timezone / estimate_unit
capacity: exact receipt ID/path/positive revision/raw hash/unit and nonnegative
          total/committed/reserved/released/remaining operands
qa_plan: safe canonical path or MISSING
stories[]: unique, ordered, complete one-to-one coverage of the plan story set
```

Require exact tracker/plan equality for dates, goal, IANA timezone, estimate unit,
capacity receipt and operands, QA-plan binding, ordered story identity/path/
priority/estimate/dependencies, and all planning hashes. Recompute
`remaining = total - committed - reserved + released` and reject a unit or operand
mismatch. Each tracker story row must contain and match its exact producer tuple:
stable story ID/name/file/order/layer/priority/source priority, controlled lifecycle
status and update provenance, `story_schema: cgs.story/v2`, author status, story
revision, current raw `source_sha256`, `story_core_sha256`, persisted readiness
record/key/stale-key and recorder-receipt identities/hashes, exact
`implementation_gate_eligible`, origin sprint, owner, nonnegative estimate,
dependencies, blocker, and completed state. Missing/extra/duplicate/incomplete rows
or disagreement with current plan/story/record bytes is a scope-authority conflict.

There is exactly one ACTIVE sprint declaration in the tracker: the single
top-level `active_sprint_id` plus `sprint_state: ACTIVE` tuple. A duplicate
top-level key, second ACTIVE row/tuple, repeated active ID, or conflicting sprint
ID is invalid even when values are textually equal. Every present session-state,
project-stage, and current-milestone source may declare at most one ACTIVE sprint
ID and must equal the tracker; those sources corroborate but never override it.

Record `(tracker canonical path, raw SHA-256, tracker_revision, event_id,
lifecycle_owner, lifecycle_recorder)` in the current-context snapshot, readiness
key, stale key, and `expires_when`. Re-read and rehash the tracker in the after
snapshot; any raw-byte/revision/event/owner/recorder/ACTIVE-state change invalidates
the sprint set and every result derived from it.

Resolve only the canonical plan at `plan_file`; a filename discovered elsewhere is
not authority. Require its exact raw hash to equal `plan_sha256`, schema exactly
`cgs.sprint-plan/v2`, and internal sprint ID, `plan_revision`, and story-set hash to
equal tracker values. Recompute the story-set hash from every plan row as exact
UTF-8 records:

```text
<story-id> TAB <canonical-path-or-INLINE> TAB <raw-story-sha256-or-MISSING>
```

Sort records by story ID using code-point order, join with LF and no trailing LF,
compute lowercase SHA-256, and prefix `sha256:`. Inline work is not a story and is
excluded from readiness evaluation but remains in the hash. Duplicate/missing IDs,
incomplete/extra tracker story coverage, ambiguous/missing paths, missing/
nonpositive tracker revision, duplicate event/ACTIVE declaration, missing explicit
plan revision, stale tracker timestamp, tracker/plan/story raw hash mismatch, or
disagreement with a current session selector returns `RUN_BLOCKED`. Never choose a
newest file, consume `plan_path`/`plan_hash`, or resolve a conflict by timestamp.

Plan priority (`Must Have`, `Should Have`, or declared controlled value) is stored
on each story result and used only in the exact sprint warning. It never changes
readiness severity.

## 5. Stable check registry

Every result contains exactly one row for every applicable check below. `version`
is `1` and the check-definition hash is the SHA-256 of its normative row and named
sections in this file.

| Check ID | Deterministic responsibility |
|---|---|
| `SR-C001` | story exists, raw identity stable, explicit supported adapter/schema, producer identity fields, and unique stable story ID |
| `SR-C002` | production-control classification, context coverage, required source statuses |
| `SR-C003` | stable system/GDD path/hash/status/requirement join |
| `SR-C004` | registry availability and exact active TR→system/GDD/requirement join |
| `SR-C005` | governing ADR presence/hash/status and reasoned N/A where allowed |
| `SR-C006` | v2 Source Manifest ID/currentness/control rows and applicable current Rule-ID locators |
| `SR-C007` | self-contained, observable, type-appropriate acceptance criteria |
| `SR-C008` | stable AC/Test IDs, coverage cardinality, direct/imported QA provenance |
| `SR-C009` | type, estimate, scope boundaries, evidence section, engine/performance notes |
| `SR-C010` | dependency ID/path/kind/hash/status/resolution validation |
| `SR-C011` | asset reference classification and producer dependency join |
| `SR-C012` | unresolved design/architecture/question marker detection |
| `SR-C013` | relevant current technical/control/engine-context evidence and forbidden work |
| `SR-C014` | v2 tracker adapter/raw hash/revision/unique ACTIVE declaration and exact plan_file/raw plan_sha256/revision/story-set/membership/priority evidence, or explicit scope N/A |
| `SR-C015` | bounded before/after mutation and source-stability guard |
| `SR-C016` | QL-STORY-READY mode/packet/result binding and deterministic merge |

Check status is `PASS`, `FAIL`, `BLOCKED`, `NOT_APPLICABLE`, or `UNVERIFIED`.
Each row includes check ID/version/hash, applicability/reason, story/context hashes,
assertion inputs, evidence locators/hashes, result, finding IDs, and limitations.

Only these N/A cases are permitted:

- `SR-C003`, `SR-C004`, and `SR-C006`: non-production story with an explicit
  structured reason and positive current evidence that no production control
  applies;
- `SR-C005`: explicit `No ADR applies` plus bounded architecture-neutral reason;
- `SR-C011`: no declared/detected asset reference after complete scan;
- `SR-C013`: exact `N/A — no engine API involved` for a pure data/config story,
  while control/technical-preference evidence remains evaluated;
- `SR-C014`: non-sprint scope; and
- `SR-C016`: correctly skipped lean/solo mode.

Absence, unreadability, unsupported parsing, or an owner waiver is not positive
N/A evidence.

## 6. Stable finding schema

For each non-pass/warning, compute fingerprint version `srf-v1` by SHA-256 over
UTF-8 length-delimited fields (`decimal-byte-length:bytes`) in this order:

```text
srf-v1
check_id
stable story_id, or canonical path only when ID is unavailable
subject_kind
stable subject_id (AC/Test/TR/ADR/system/dependency/asset/control/sprint or <story>)
controlled defect_key
```

Finding ID is `SRF-` plus the first 20 lowercase fingerprint hex characters.
Exclude line/column, diagnostic prose, source byte hash, timestamp, reviewer,
severity/classification, check version, verdict, owner, and status. If the story
ID is absent/duplicate, mark identity `UNVERIFIED`; the path fallback cannot be
claimed stable across a rename.

`cgs.story-readiness-finding/v1` fields:

```text
finding_id / fingerprint_version / fingerprint
check_id / check_version / check_hash
story_id / canonical story path / story hash
subject_kind / subject_id / defect_key
classification              GAP | BLOCKER | WARNING
observation                  OPEN | STILL_OPEN | RESOLVED_CANDIDATE | WAIVER_PRESENT
owner_role                   exact responsible artifact owner, or UNASSIGNED
external_action              true | false
dependency_id                stable ID or NONE
evidence[]                   path/hash/stable locator/observed value
resolution_condition         deterministic pass condition
first_seen_record            exact prior record ID/hash or UNKNOWN
current_context_hash / detected_at / limitations
```

Classification is determined by the check rules, never by reviewer rhetoric.
`BLOCKER` means an external/current authority or hard prerequisite prevents
implementation. `GAP` means the story/evidence package must be corrected.
`WARNING` cannot hide a failed required check.

When a valid prior-record manifest is supplied, match fingerprints. A current
match is `STILL_OPEN`; a prior finding absent under complete equivalent/current
coverage is `RESOLVED_CANDIDATE`; a valid referenced waiver is
`WAIVER_PRESENT`. The analyzer never persists OPEN/RESOLVED/WAIVED lifecycle
state. Invalid/unrelated/stale prior evidence is ignored as lifecycle authority
and reported as a gap.

## 7. Story and source schema

A supported production story requires the exact `cgs.story/v2` adapter identity
fields from Section 1, title, type, layer, estimate, in-scope and out-of-scope
sections, complete Source Manifest and Currentness Matrix, stable system/GDD
binding, exact TR IDs, governing ADRs or permitted N/A, current control rows and
stable Rule-ID locators, acceptance criteria with v2 AC IDs, QA specifications
with v2 Test IDs, dependencies, asset dependencies, implementation/engine/
performance notes, unresolved-question section, and expected evidence paths.

Allowed story types and minimum AC counts:

| Type | Minimum ACs | Required evidence kind |
|---|---:|---|
| `Logic` | 3 | automated unit/property test |
| `Integration` | 3 | automated integration/controlled harness |
| `Visual/Feel` | 2 | named playtest protocol and evidence path |
| `UI` | 2 | automated interaction/accessibility where possible plus named visual/manual evidence |
| `Config/Data` | 1 | schema/data validation or deterministic smoke check |

Estimate is an explicit points/hours/team-calibrated size value, never inferred.
Gameplay-loop/rendering/physics work requires a numeric budget with unit/target or
`no performance impact expected` plus a falsifiable reason. Post-cutoff engine API
use requires an exact engine-version source and verification condition.

Unresolved `UNRESOLVED`, `TBD`, `TODO`, placeholder `???`, undecided alternatives,
or question markers in normative behavior/AC/implementation sections fail
`SR-C012`. A literal question mark inside a quoted string, URL, test data, or
resolved FAQ is not an unresolved marker; parser locators must distinguish it.

## 8. Approved GDD, TR, ADR, and control joins

### Systems index and GDD

The story's binding contains `system_id`, canonical `gdd_path`, raw `gdd_hash`,
and one or more stable `gdd_requirement_id` values/locators. The systems index
must contain exactly one row with the same system ID/path/hash and status exactly
`Approved`. The GDD must identify the same system, have `Status: Approved` when
its schema declares status, and contain each requirement ID exactly once.

Missing/unreadable/invalid index or GDD, duplicate system/requirement ID,
non-Approved status, or index/current GDD hash mismatch is `SR-C003 BLOCKED`.
Available valid authority plus a missing/malformed story binding is `SR-C003
FAIL`. A bare filename, quote without a stable requirement locator, or title match
does not pass.

### TR registry

The registry must parse as its declared schema and contain unique IDs. Each exact
story `TR-[system]-NNN` must exist once, have `status: active`, and map to the same
system ID, GDD path, and GDD requirement ID/text identity. `superseded-by` must not
coexist with active status.

Missing/unreadable/invalid registry or duplicate/conflicting registry IDs is
`SR-C004 BLOCKED`. Missing/malformed/placeholder/unregistered/deprecated/
superseded story TR is `SR-C004 FAIL`; name a unique replacement when current
registry evidence provides one. Exact `Traceability: LEGACY-UNTRACED` is FAIL.

### ADRs

Each governing ADR path must exist, hash successfully, have one stable ADR ID,
and `Status: Accepted`. Missing/invalid/Proposed/Rejected/Superseded or duplicate
ADR identity is `SR-C005 BLOCKED`. N/A follows Section 5 and cannot cover an
unresolved architecture choice.

### Control manifest through the cgs.story/v2 currentness adapter

First require a valid recomputed `Source Manifest ID`, `Story Core SHA-256`, and
complete currentness matrix under Section 1. The matrix must include the exact
current `cgs.control-manifest/v2` artifact, its source-manifest/ruleset/payload/
revision and immutable provenance state, plus external review/ACTIVE receipt when
the control contract requires one. Story control-rule bindings name stable Rule
IDs, locators, normative level, bounded rule text/hash, source ADR, scope, and
conditions; each must resolve uniquely in the current control artifact and apply
consistently to story scope.

Missing/unreadable/invalid authority, required matrix row, currentness state,
receipt, Rule ID/locator, or any hash/identity mismatch is `SR-C006 FAIL` and
therefore at least `NEEDS_WORK`; unavailable authority that prevents a meaningful
join is `BLOCKED`. A v2 story does not require `Manifest Version`, `Manifest Hash`,
or `## Source Snapshot`. Dates, copied labels, `Manifest-Note`, risk acceptance,
and those legacy fields cannot pass or override the producer-owned join.

## 9. Acceptance criteria, Test IDs, and QA provenance

For `cgs.story/v2`, AC format is `AC-SNNN-CC`: `SNNN` must equal the exact
`Story Slot`, and `CC` is that story's two-digit criterion slot. Test format is
exactly one of:

```text
TC-<epic-slug>-SNNN-ACCC   Logic | Integration
MC-<epic-slug>-SNNN-ACCC   Visual/Feel | UI
SC-<epic-slug>-SNNN-ACCC   Config/Data
```

The test epic slug must equal the canonical story path's epic slug, its `SNNN`
must equal `Story Slot`, and `ACCC` must reference the same `CC` as exactly one
current `AC-SNNN-CC`. Every ID is explicit, unique, append-only within its producer
ledger, and never inferred from headings or order.

Each AC contains one observable assertion, conditions/input, expected result,
and evidence kind. An AC that says only “implement,” “support,” “works,” “looks
good,” or an unbounded subjective judgment fails. Visual/Feel subjective criteria
pass testability only with a named protocol, evaluator condition, observable
rubric, and evidence path.

Each current AC has exactly one type-correct Test/check row. A TC row contains
Given, When, Then, edge cases, observable assertion, and evidence path/schema; an
MC row contains setup, verification procedure, unambiguous pass condition,
evidence path/schema, and sign-off; an SC row contains setup/data fixture,
action/load, observable pass condition, and evidence path/schema. Every row also
binds its exact AC, direct/imported origin, and owner/source plan. A Test ID is
defined once and cannot map to multiple ACs. Duplicate/malformed/slot-mismatched
AC or Test IDs, uncovered ACs, orphan or multi-AC Tests, wrong type prefixes,
missing type-specific fields, or conflicting paths are `SR-C007/SR-C008 FAIL`.

Imported QA evidence additionally requires:

- exact canonical QA plan path and current raw `QA Plan Hash`;
- plan declared and independently recomputed effective state both `CURRENT`;
- all plan source paths present with exact captured raw hashes;
- exact story path and current story hash binding;
- exact declared and recomputed `Story Core SHA-256` plus producer Source Manifest
  ID binding;
- exact set equality between plan/story AC IDs;
- exact `ac_set_sha256` equality;
- globally unique imported Test definitions; and
- every Test ID mapping to exactly one declared AC with no orphan.

Missing/mismatched/PARTIAL/STALE/ambiguous evidence is `SR-C008 FAIL`. A directly
authored test table is not exempt from ordinary ID/cardinality/evidence checks.

## 10. Dependencies

Each dependency row declares unique stable `dependency_id`, canonical story path,
kind `hard` or `soft`, expected interface/deliverable, and resolution condition.
Read the current dependency story; require its internal ID to match, record raw
hash/status, and reject cycles inside the loaded dependency graph.

Hard is the default. Hard passes only for current `Complete` or `Done`. Missing,
unreadable, Draft, Blocked, Ready, or In Progress hard dependency is
`SR-C010 BLOCKED`, with `owner_role`, `external_action: true`, dependency ID,
current evidence, and exact resolution condition.

Soft passes only when the dependency exists, has a non-conflicting status, and the
story supplies a bounded fallback/interface proving implementation can proceed
without it. Missing/Draft/Blocked soft dependency or absent fallback is
`SR-C010 FAIL`; a soft row never bypasses a requirement that is functionally hard.
Free-text waiver/accepted risk does not change the check result.

## 11. Assets

Recognize declared asset rows and safe textual references containing `assets/` or
ending in `.png`, `.jpg`, `.jpeg`, `.svg`, `.wav`, `.ogg`, `.mp3`, `.glb`,
`.gltf`, `.tres`, `.tscn`, or `.res`. Deduplicate by canonical path.

| Classification | Exact condition | Readiness effect |
|---|---|---|
| `EXISTING` | canonical readable regular file exists | pass existence row |
| `PLANNED_WITH_STORY` | absent asset; unique dependency story explicitly produces exact path | hard/default producer incomplete -> BLOCKED; complete producer but absent -> BROKEN |
| `BROKEN` | absent with no valid producer, or completed producer missing deliverable | FAIL / NEEDS_WORK |
| `UNKNOWN` | unsafe/ambiguous/unreadable/unsupported/over-limit | UNVERIFIED, partial, never READY |

An explicit soft producer must satisfy Section 10 and the story must specify a
non-asset fallback; otherwise it is functionally hard. Asset quality is outside
this check.

## 12. QA packet and stable reviewer findings

In full mode, create one `cgs.story-readiness-qa-packet/v1` per story containing
packet ID/hash, story ID/path/hash/type, context snapshot hash, check-result-set
hash, verbatim AC IDs/text, Test mappings, GDD/TR requirement identity/text,
dependency matrix, base verdict, deterministic finding IDs, gate ID
`QL-STORY-READY`, and deadline.

One normalized `cgs.story-readiness-qa-result/v1` must echo packet/story/context/
check hashes, reviewer role/instance, start/end time, exact verdict, structured
issue rows, limitations, and result hash. Issue rows receive normal `srf-v1`
finding IDs under `SR-C016` using the AC/Test ID or `<story>` and a controlled QA
defect key.

Missing/duplicate/cross-story/malformed/hash-mismatched/timed-out/unavailable
results are `SR-C016 UNVERIFIED` and final `BLOCKED`. `ADEQUATE` passes only the
QA check; it cannot override deterministic gaps/blockers. `GAPS` is FAIL and at
least `NEEDS_WORK`; `INADEQUATE` is BLOCKED. No proceed-anyway/risk branch produces
READY.

Lean/solo explicitly produce `NOT_APPLICABLE` with review mode/source evidence.

## 13. Verdict and batch state

Run outcomes are exactly `RUN_COMPLETE`, `RUN_PARTIAL`, `RUN_BLOCKED`,
`USAGE_ERROR`, and `INPUT_ERROR`. Per-story verdicts are exactly `READY`,
`NEEDS_WORK`, and `BLOCKED`.

First derive base verdict from `SR-C001..SR-C015`:

1. any `BLOCKED` -> `BLOCKED`;
2. otherwise any required `FAIL`/`UNVERIFIED` -> `NEEDS_WORK`;
3. otherwise every applicable row PASS/permitted N/A -> `READY`.

Merge `SR-C016` by Section 12. A per-story result has `evaluation_state`
`COMPLETE`, `PARTIAL`, or `NOT_EVALUATED`. `READY` requires `COMPLETE` and a
complete before/after snapshot. A partial story with no blocker is `NEEDS_WORK`;
when identity/current authority cannot be established at all it is `BLOCKED`.

Run outcomes follow `SKILL.md`. Batch summary lists counts by final verdict,
partial/not-evaluated count, exact processed ordinal range, and continuation.
Never discard completed story results because another story fails.

## 14. Record candidate

`cgs.story-readiness-record-candidate/v1` contains:

```text
record_candidate_id / candidate_hash
readiness_key               deterministic stable snapshot/result key
story_id / path / raw hash
story_adapter_id / producer_skill_hash / producer_contract_hash / producer_bundle_hash
source_manifest_id / story_core_sha256
checked_at                  RFC 3339 UTC
checker_id / version / executable-or-contract hash
ruleset ID/version/hash
review mode/source hash
context snapshot and ordered source identities/hashes
ordered SR-C001..SR-C016 rows and check-result-set hash
stable findings and finding-set hash
base verdict / QA result / final verdict / evaluation state
expires_when                exact source/checker/rules/reviewer change predicates
stale_key
persistence_status          NOT_PERSISTED
implementation_gate_eligible false
record_mutated              false
recorder_invoked            false
```

Compute `readiness_key` from length-delimited schema, story ID/hash, adapter ID and
producer SKILL/contract/bundle hashes, Source Manifest ID/Story Core hash, context hash,
check-result-set hash, QA-result hash or exact skip token, checker/ruleset hashes,
and final verdict; exclude checked-at. Candidate hash includes the complete
canonical record including checked-at. Candidate ID is `SRR-CAND-` plus the first
20 candidate-hash hex characters.

`expires_when` must name every story/source/adapter/producer-SKILL/contract/bundle/
reviewer/checker/ruleset identity used.
Any raw hash, status, join, source availability, sprint identity, review mode, or
contract change makes the candidate stale. A prior/current result cannot be
reused by path/verdict alone.

## 15. Independent recorder protocol

`cgs.story-readiness-recorder/v1` is a separate writer that this skill never
calls. A conforming recorder accepts one exact candidate hash, an owner-declared
readiness-registry target/schema, base registry hash/revision/head or exact
absence, and fresh authorization bound to operation/final hash/expiry.

Under exclusive lock/CAS it must:

1. reread candidate bytes and independently rehash every source in the stale key;
2. revalidate all source schemas/joins, check rows, finding IDs, QA result, verdict,
   checker/ruleset allowlist, record hash, and authorization;
3. reject stale sources/result as `STALE_CANDIDATE` without writing;
4. detect an exact already-persisted record by candidate/readiness key and return
   `ALREADY_RECORDED` without duplication;
5. compare exact registry base path/ID/hash/revision/head and return
   `CAS_CONFLICT` without writing when changed;
6. prepare an append-only event/record with collision-resistant IDs, flush a
   same-directory prepared file, atomically replace/create, and post-read verify
   prefix/order, chain, UUID/key uniqueness, revision/head, and final hash; and
7. emit an immutable `cgs.story-readiness-recorder-receipt/v1` with source/
   candidate/base/final identities, authorization, lock/CAS/atomicity evidence,
   timestamps, result, and receipt hash.

Recorder results are exactly `RECORDED`, `ALREADY_RECORDED`, `STALE_CANDIDATE`,
`CAS_CONFLICT`, `AUTHORIZATION_INVALID`, `CANDIDATE_INVALID`, or
`RECORDER_FAILED`. On any result except the first two, target bytes/absence remain
unchanged. Conflict/staleness requires a fresh analysis candidate and new
authorization; no hidden retry or last-writer-wins is allowed.

Only an exact persisted `READY` record plus valid receipt may set
`implementation_gate_eligible: true`, and only while every stale-key source still
matches. The recorder cannot upgrade a `NEEDS_WORK`, `BLOCKED`, or partial record.

## 16. Run envelope

`cgs.story-readiness-run/v2` contains schema, normalized invocation, run ID/hash,
scope/sprint manifest and context identities, review mode, start/end time, limits/
usage, processed range and continuation, ordered per-story results, coverage/
gaps, before/after mutation snapshots, run outcome, and these fixed assertions:

```text
allowed_write_set: []
record_mutated: false
recorder_invoked: false
implementation_started: false
```

The result is evidence, not a file mutation, sprint decision, or implementation
authorization.
