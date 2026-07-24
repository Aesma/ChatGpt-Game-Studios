---
name: qa-plan
description: "Generate a version-bound QA plan for a sprint, feature, or story. Reads stories and their GDD/ADR sources, maps stable acceptance-criterion IDs to stable test IDs, and writes one independent plan without editing stories or session state."
---

## Invocation and execution

Invoke only as:

```text template
$qa-plan --scope-manifest <project-relative-path>
```

Reject missing/duplicate/unknown flags, positional sprint/feature/story values,
unresolved bracket tokens, and the legacy `$qa-plan [epic-slug]` catalog form before
any project write. Do not reinterpret an epic slug as a feature or search term. Route
catalog-call migration to the catalog owner; this workflow never edits the catalog.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

## Contract manifest

```yaml template
schema: cgs-qa-plan-workflow-contract/v1
input_schema: cgs-qa-plan-scope/v1
output_schema: cgs-qa-plan/v2
owned_output: production/qa/plans/<plan-id>.md
test_id_ownership_schema: cgs-test-id-ownership-snapshot/v1
hash_algorithm: sha256
states: [CURRENT, PARTIAL, STALE, UNKNOWN, BLOCKED]
never_writes:
  - story-gdd-adr-or-requirement-authority
  - build-or-test-evidence
  - test-id-ownership-snapshot
  - production/session-state/
  - workflow-catalog
```

One QA-plan owner reads and writes the artifact. Planning assistance may produce
read-only proposals, but only that owner assembles the final source/requirement/
dependency matrix, previews the exact bytes, and performs the compare-and-set write.

# QA Plan

This skill generates a structured, version-bound QA plan for a sprint, feature,
or individual story. It tells developers what to automate, what to verify
manually, what belongs in the smoke scope, and when playtest evidence is
required.

Run this before implementation begins. A plan produced from incomplete inputs
may still be saved as a planning artifact, but it is `PARTIAL` and cannot satisfy
a downstream quality gate. A plan whose captured source bytes later change is
effectively `STALE` and cannot satisfy a gate until regenerated.

Report independent axes:

| Axis | Values |
|---|---|
| Plan State | CURRENT, PARTIAL |
| Effective State | CURRENT, STALE, UNKNOWN |
| Scope Coverage | COMPLETE, PARTIAL |
| Build Binding | BOUND, PRE_IMPLEMENTATION, REQUIRED_MISSING |
| Test ID Ownership | OWNED, PROPOSED, CONFLICT |
| Evidence Level | PLANNED, IMPLEMENTED, DISCOVERED, EXECUTED, VERIFIED, UNKNOWN |
| Persistence | WRITTEN, UNCHANGED, DECLINED, FAILED |
| Gate Evidence | NO |

The hard planning ceilings are 512 stories, 4,096 authority/source files, 64 MiB
input bytes, 16,384 requirement spans, 32,768 dependency edges, 32,768 plan items,
16 MiB candidate output, and 120 seconds wall time. A scope manifest may lower but not
raise them. Any limit or unreadable prefix produces an explicit omitted/unprocessed
ledger and `Scope Coverage: PARTIAL`; no truncated plan is COMPLETE.

**Owned output:** `production/qa/plans/<plan-id>.md`

The plan ID is a stable canonical slug or UUID supplied by the scope manifest and must
not be a date alone. The path is immutable: require it absent, or byte-identical to
the approved candidate for a verified no-op. A changed existing plan is a conflict;
regeneration uses a new plan/revision ID and may declare `Supersedes Plan ID` without
mutating the old artifact.

## Artifact ownership and write boundary

`$qa-plan` owns only the independent QA plan file named above.

- Story files, GDDs, ADRs, registries, sprint files, and architecture manifests
  are read-only inputs.
- Never add, replace, or back-fill a story's `## QA Test Cases` section. The
  story-owning workflow is responsible for merging plan IDs or links into a
  story.
- Never create or modify `production/session-state/active.md`, a checkpoint,
  sprint status, or any other state file.
- Never perform an unlisted or silent write. If a requested write is outside the
  owned output, explain the ownership boundary and leave that file unchanged.
- A plan may reference stable story, AC, and test IDs; the reference does not
  transfer ownership of the story to this workflow.

The complete changeset preview for this workflow therefore contains exactly one
candidate artifact: the immutable QA plan path. If no plan write is approved, the
changeset is empty.

---

## Phase 1: Parse and resolve scope

Resolve the literal scope-manifest path and real path inside the project. Reject a
directory, symlink escape, malformed/duplicate-key document, unsupported schema,
unsafe ID, ambiguous canonical path, or digest that is not lowercase SHA-256.
Read exact bytes once and require `cgs-qa-plan-scope/v1` with:

- stable plan ID, scope ID, scope kind `SPRINT`, `FEATURE`, or `STORY`, human name,
  and optional superseded plan ID;
- one authoritative scope source path/hash: active sprint manifest, epic/feature
  manifest, or exact story; never newest-file, mtime, title, substring, or glob-match
  selection;
- an ordered list of stable story IDs and exact story paths/hashes;
- expected GDD, ADR, control/requirement and dependency authority paths/hashes for
  each story/AC;
- build binding: either exact candidate-manifest path/hash, build ID/artifact
  path/hash, source commit, platform/configuration; or the literal state
  `PRE_IMPLEMENTATION` with owner and reason;
- exact `cgs-test-id-ownership-snapshot/v1` path/hash and snapshot owner/revision;
- optional existing test/evidence receipt paths/hashes used only to classify evidence
  levels;
- budgets for maximum stories, authorities, files, input bytes, extracted requirement
  spans, dependency edges, plan items, output bytes, and wall time, all at or below
  workflow maxima; and
- expected output path `production/qa/plans/<plan-id>.md` and precondition `ABSENT`.

Canonicalize IDs and paths with Unicode NFC, forward slashes, and case-folded
comparison keys while preserving raw spelling for evidence. Reject canonical duplicate
story IDs/paths, unsafe plan IDs, a mismatched output path, reused plan ID, or scope
source/story membership disagreement.

Sort stories by stable story ID then canonical path for deterministic loading. Admit
only whole story authority closures that fit every budget. Preserve a complete ledger
of selected, loaded, missing, unreadable, invalid, omitted, and unprocessed sources,
bytes, requirement spans, dependency edges, and plan items. Never scan outside the
manifest or silently truncate. Missing/unreadable expected stories remain ledger rows,
make `Plan State: PARTIAL`, `Effective State: UNKNOWN`, and prohibit using the plan as
a complete downstream planning/gate input.

---

## Phase 2: Load versioned inputs

### 2.1 Hash raw source bytes

For every source, read the raw file bytes once, compute SHA-256 over those exact
bytes, and parse content from the same bytes. Format every digest as
`sha256:<64 lowercase hexadecimal characters>`. Never hash normalized text,
copied excerpts, a user-supplied digest, or reconstructed content.

Record each source as `loaded`, `missing`, `unreadable`, or `invalid`. Capture:

- every in-scope story file, in full;
- every GDD referenced by an in-scope story, in full for hashing, even when only
  Acceptance Criteria, Formulas, and Edge Cases are used to build tests;
- every ADR referenced by an in-scope story, in full for hashing, even when only
  selected sections are used;
- the exact scope-defining sprint/epic/story authority;
- only the scope-manifest-declared systems index, control/requirement manifest,
  dependency authority, build candidate/receipt, ID-ownership snapshot, and evidence
  receipt paths/hashes.

The manifest must contain a source record for every story/GDD/ADR path expected
by scope, including a non-loaded status when no digest can be computed. Missing,
unreadable, invalid, or ambiguously referenced story/GDD/ADR input makes the plan
`PARTIAL`; never invent a digest or silently omit the path.

For every story AC and supporting GDD/ADR/control requirement, record a stable
Requirement Binding ID, owning artifact/owner, exact raw file hash, parser/tool
identity/version/hash, byte-span start/end, and SHA-256 over the exact raw span bytes.
The span hash supports precise change review but never replaces the full-file hash.
If a parser cannot produce an unambiguous raw byte span, keep the path in the ledger,
set requirement status `UNKNOWN`, and make the plan `PARTIAL`.

Validate build binding independently. `BOUND` requires the candidate manifest and
local artifact or trusted build receipt to rehash, with exact build ID, artifact hash,
source commit, platform, and configuration. `PRE_IMPLEMENTATION` is allowed only when
the scope authority says no build should exist yet; every plan item remains Evidence
Level `PLANNED`, and the plan itself is never execution evidence. A required but
missing/mismatched build is `REQUIRED_MISSING` and makes the plan `PARTIAL/UNKNOWN`.

### 2.2 Extract story requirements

For each loaded story extract:

- story title, stable story number/ID, epic slug, and declared `Type:`;
- every acceptance criterion and its exact stable AC ID;
- implementation/evidence paths, engine notes, estimate, and dependencies;
- every referenced GDD and ADR path;
- any existing QA specification ID already associated with an AC.

Stable story acceptance criteria use the create-stories contract, for example
`AC-S001-01`. An AC ID belongs to the story owner. This skill must preserve it
exactly and must never add, guess, renumber, recycle, or write one into a story.

For each story:

1. Require every acceptance criterion to have one unique stable AC ID.
2. Reject duplicate AC IDs within the scope.
3. Record missing, malformed, duplicate, or ambiguous IDs as coverage gaps.
4. Make the plan `PARTIAL` when any in-scope criterion lacks an unambiguous
   stable AC ID. Include the criterion text and story path in the gap report.

Read the test-ID ownership snapshot as a read-only authority. Each existing Test ID
must bind exactly one stable AC ID, owner plan ID, lifecycle state, source plan
path/hash, and non-reuse tombstone when retired. New deterministic IDs are `PROPOSED`
and owned by this plan ID only after the immutable plan is published. Reject any Test
ID mapped to another AC, multiple owners, recycled tombstone, conflicting plan, or
snapshot hash/revision drift. Record `Ownership Status: OWNED`, `PROPOSED`, or
`CONFLICT`; a conflict makes the plan `PARTIAL` and prevents COMPLETE.

### 2.3 Load bounded supporting context

From loaded GDDs use the Acceptance Criteria, Formulas, and Edge Cases sections.
If Edge Cases is absent, record that edge-case coverage is inferred from the
GDD acceptance criteria and story ACs. Use the control manifest only for
applicable test guardrails. Do not turn a source excerpt into a substitute for
the full-file source hash.

Build one dependency graph over stories, ACs, production systems, configuration,
required test fixtures/environments, Test IDs, and expected evidence artifacts. Every
edge records source authority/path/hash and relation type. Detect missing endpoints,
unknown owners, duplicate edges, and cycles that make execution order ambiguous.
Preserve all gaps in a dependency/coverage matrix; do not infer an edge from similar
names or scan an unbounded control manifest.

---

## Phase 3: Classify test methods and assign stable test IDs

Preserve a story's declared type as `Declared Type`; never silently correct it. For
each AC independently derive zero or more observable/risk tags from explicit source
evidence: state/formula, boundary/error, cross-system/persistence, UI interaction/
accessibility, visual/rendering, feel/judgment, configuration/data, performance,
security/safety, recovery, or compatibility. Record source Requirement Binding IDs.

If the declared type conflicts with the AC observables/risks, emit finding
`QP-TYPE-MISMATCH` with declared type, derived tags, source evidence, and story owner.
Keep the declared type unchanged and plan all supported methods. If no valid type is
declared, label a proposed type `inferred`, add a gap, and make the plan `PARTIAL`.

| Observable or risk | Candidate methods |
|---|---|
| State/formula or boundary/error | Unit, property, negative, and boundary automation |
| Cross-system/persistence or compatibility | Integration, migration, round-trip, and recovery automation |
| UI interaction/accessibility | Interaction and accessibility automation; manual evidence only for remaining observable gaps |
| Visual/rendering | Deterministic capture/diff or benchmark when feasible; named manual review for irreducible judgment |
| Feel/judgment | Reproducible playtest protocol, completed session result, and named sign-off |
| Configuration/data | Schema/data validation plus observable integration or smoke check |
| Performance/security/safety/recovery | Benchmark, abuse/negative, failure-injection, and recovery methods tied to explicit thresholds |

Treat each AC independently. Choose methods from observable and risk evidence, required
confidence, feasible automation, platform/build needs, and dependency graph—not story
type alone. Visual checks may be automated; configuration behavior may require full
integration. A story or AC may use multiple labels and methods; never select or report
a single primary classification and never drop secondary coverage.

Assign exactly one stable Coverage Item ID per stable AC ID and one Test ID for each
selected method family:

- coverage row: `QAI-[epic-slug]-S[story-number]-AC[criterion-number]`;

- Logic/Integration automated test:
  `TC-[epic-slug]-S[story-number]-AC[criterion-number]`
- Visual/Feel or UI manual check:
  `MC-[epic-slug]-S[story-number]-AC[criterion-number]`
- Config/Data smoke/data check:
  `SC-[epic-slug]-S[story-number]-AC[criterion-number]`

The story number and criterion number come from the stable AC ID. Multiple methods use
their distinct prefixes for the same AC, for example one TC plus one MC; no arbitrary
primary is chosen. Preserve a valid ownership-snapshot ID for that AC/method family.
IDs remain stable when criterion wording/order changes and are never recycled for a
different AC. Duplicate IDs, owner conflicts, or ID/AC/method mismatch are gaps that
make the plan `PARTIAL`.

Each plan item records: story path/hash, requirement binding/span hashes, stable AC/
coverage/Test IDs, ID owner/status, declared type, all observable/risk tags, method,
dependencies, build binding, test/evidence path/schema, Given/When/Then or
Setup/Verify/Pass condition, edge cases, required sign-off, coverage status, and
Evidence Level.

Evidence Level is one of `PLANNED`, `IMPLEMENTED`, `DISCOVERED`, `EXECUTED`,
`VERIFIED`, or `UNKNOWN`. Promotion requires current exact source/manifest/build/log/
receipt hashes at each rung; a missing, partial, stale, unsupported, or unreadable
required receipt yields `UNKNOWN`, never an inferred higher level. A pre-implementation
item without expected execution evidence remains `PLANNED` and is not itself a gap.
The QA plan always declares `Gate Evidence: NO`; downstream gates need the current plan
plus separate current execution/manual evidence.

Show the classification and AC-to-test mapping table before the write preview.

---

## Phase 4: Generate the plan

Generate a complete document with this structure:

```markdown template
# QA Plan: [scope name]

**Artifact Type**: cgs-qa-plan
**Schema Version**: 2
**Plan ID**: [stable plan ID]
**Generated**: [ISO-8601 timestamp]
**Generated by**: $qa-plan
**Scope ID / Kind**: [stable scope ID] / [SPRINT | FEATURE | STORY]
**Scope Manifest**: [path] / sha256:[digest]
**Engine**: [engine or Not configured]
**Plan State at Generation**: [CURRENT | PARTIAL]
**Effective State at Generation**: [CURRENT | UNKNOWN]
**Build Binding**: [BOUND | PRE_IMPLEMENTATION | REQUIRED_MISSING]
**Gate Evidence**: NO
**Supersedes Plan ID**: [stable ID or NONE]

## Plan Manifest

`manifest_version: 2`
`hash_algorithm: sha256`

### Scope and Budget Ledger

| Record ID | Kind | Stable ID | Path | Status | Bytes / Edges / Items | Reason Rule |
|---|---|---|---|---|---|---|

### Build Binding

| Status | Candidate Manifest + Hash | Build ID | Artifact + Hash | Source Commit | Platform / Configuration |
|---|---|---|---|---|---|

### Sources

| Role | Owner | Path | Status | SHA-256 | Omission/Unknown Reason |
|---|---|---|---|---|---|
| story | [owner] | [path] | loaded | sha256:[digest] | NONE |
| gdd | [owner] | [path] | loaded | sha256:[digest] | NONE |
| adr | [owner] | [path] | loaded | sha256:[digest] | NONE |

### Story Requirement Bindings

| Story ID | Story Path | Story Hash | GDD Paths + Hashes | ADR Paths + Hashes | Stable AC IDs | Coverage |
|---|---|---|---|---|---|---|
| [stable ID] | [path] | sha256:[digest] | [path + digest] | [path + digest] | [IDs] | complete/gaps |

### Exact Requirement Bindings

| Binding ID | AC/Requirement ID | Owner | Path | File Hash | Raw Byte Span | Span Hash | Status |
|---|---|---|---|---|---|---|---|

### Test ID Ownership

| Test ID | Stable AC ID | Method Family | Owner Plan ID | Ownership Status | Snapshot Revision + Hash |
|---|---|---|---|---|---|

### Dependency and Coverage Matrix

| Coverage Item ID | Story/AC | Requirement Bindings | Declared Type | Observable/Risk Tags | Test IDs + Methods | Dependencies | Build Binding | Evidence Level | Coverage Status/Gaps |
|---|---|---|---|---|---|---|---|---|---|

### Plan State Rules

- CURRENT: every required story/GDD/ADR loaded and every AC has one stable test/check ID.
- PARTIAL: a required source/hash/AC binding is missing, invalid, or ambiguous.
- STALE: any current source bytes no longer match the captured hash, or a captured source disappears.
- UNKNOWN: a required source, span, dependency, build, ownership, or evidence result cannot be conclusively classified.

## Coverage Gaps

- [None, or exact story/source/AC gap and owning workflow]

## Test Summary

| Story | Stable AC ID | Coverage Item ID | Stable Test/Check IDs | Observable/Risk Tags | Methods | Evidence Levels | Coverage |
|---|---|---|---|---|---|---|---|

## Automated Tests Required

### [Test ID] — [Story title] / [AC ID]
**Test file path**: [path]
- Given: [precondition]
- When: [action]
- Then: [observable assertion]
- Edge cases: [boundaries/failures]

## Manual QA Checklist

### [Check ID] — [Story title] / [AC ID]
**Evidence path**: [path]
**Sign-off owner**: [role]
- Setup: [reproducible setup]
- Verify: [observable behavior]
- Pass condition: [unambiguous result]

## Smoke Test Scope

1. [Critical path with stable test/check IDs]

## Playtest Requirements

Playtest evidence must use the current producer pair: canonical
`production/playtests/<session-id>/report.md` containing an exact
`cgs.playtest-report/v2` payload, plus an independent current
`cgs.playtest-report-recorder-receipt/v1`. A plan item may name the report path and
receipt path as expected evidence, but neither path alone advances Evidence Level.
Validate the report's exact raw hash and canonical payload, session status
`COMPLETED`, protocol/session/build/platform/source/requirement identities, candidate
`cgs.review-evidence/v1` record identity with
`artifact_kind: playtest-session-report-candidate`, and candidate gate state
`REQUIRES RECORDER`. Then validate receipt schema and raw hash, recorder
identity/version and separation, exact canonical target path, persisted-file hash,
write/read-back UTC and atomic result, candidate record ID, and every bound dependency
hash. Reconstruct the candidate record ID rather than trusting the receipt claim.
Only the complete current pair that would yield `RECORDED COMPLETED — GATE ELIGIBLE`
may advance the Evidence Level or count one distinct completed session. A template,
protocol, raw log, review, ingest-only session, legacy report/schema, partial report,
changed build/profile, duplicate session ID, missing receipt, or stale/mismatched pair
remains `UNKNOWN` or the prior lower evidence level. The QA plan itself remains
`Gate Evidence: NO` in all cases.

| Stable Check ID | Story | Goal | Evidence Path | Sign-off Owner |
|---|---|---|---|---|

## Definition of Done

- [ ] Effective plan state is CURRENT after source revalidation.
- [ ] Every stable AC ID has passing automated or approved manual evidence.
- [ ] Required smoke checks pass.
- [ ] Required evidence exists at the named canonical path.
- [ ] The plan remains Gate Evidence: NO; gates consume this plan plus current separate evidence.
```

The source table and story binding table are mandatory. `PARTIAL` plans retain
all known records and gaps; they must not disguise an absent hash as current.

### Effective-state revalidation contract

Before this plan is reused, imported into a story, or consumed by
`$smoke-check`, `$story-done`, `$regression-suite`, or another gate:

1. Read every captured scope/story/GDD/ADR/control/requirement/build/ownership/
   dependency/test/evidence source path and hash its current raw bytes.
2. Revalidate raw requirement spans, build identity/artifact, ownership revision,
   dependency edges, evidence receipt schemas and all referenced dependencies.
3. Compare current digests and source availability with the manifest.
4. Treat any mismatch, disappearance, or newly unreadable captured source as `STALE`,
   regardless of the stored `Plan State at Generation` label.
5. Treat an unavailable verifier/remote receipt, partial coverage, unsupported schema,
   or unresolved new dependency as `UNKNOWN`; never infer currentness.
6. Reject `PARTIAL`, `STALE`, and `UNKNOWN` as a complete planning/gate input.
   Regenerate the immutable plan from current sources under a new plan/revision ID.
7. Preserve valid stable AC and owned test/check IDs when regenerating; update hashes and
   requirement text from current sources.

This computed effective state avoids mutating the plan merely to mark it stale.

---

## Phase 5: Preview, authorize, write, and verify

### 5.1 Preview one complete changeset

Show the complete generated plan bytes or a lossless inspectable artifact/diff whose
manifest records total bytes, raw SHA-256, section order, and byte-range/hash for every
chunk. If display limits require pagination, present every chunk with no omitted or
ellipsis content before approval and verify the concatenated hash. A summary, sampled
matrix, collapsed middle, or changed-section list is not approval evidence.

Then show:

```text template
Proposed changeset
- CREATE production/qa/plans/<plan-id>.md (sha256:<candidate-digest>)

Explicit non-writes
- all in-scope story files
- production/session-state/active.md
- all GDD, ADR, sprint, registry, and architecture files
- build, evidence, and test-ID ownership artifacts
- workflow catalog
```

Require the target absent at preview. If it already exists and is byte-for-byte
identical to the candidate, preview a verified no-op; if bytes differ, return
`BLOCKED — IMMUTABLE PLAN ID CONFLICT` and require a new plan/revision ID. Never
preview or perform UPDATE of an existing plan. Ask once whether to apply the exact
one-file candidate bytes/hash or accept the exact verified no-op.

There is no story-backfill or session-state option. If the user asks for one,
explain that the story/checkpoint owner must perform it and do not include it in
this changeset.

### 5.2 Apply only the selected operation

If approved, immediately before writing:

- re-hash the scope manifest and every loaded scope/story/GDD/ADR/control/
  requirement-span/build/dependency/ownership/evidence source and abort if any digest,
  availability, ownership revision, or effective state changed since generation;
- require the immutable target still absent, or identical only for the previewed
  no-op; and
- stage only the plan file bytes/hash, exactly as previewed.

Create using an exclusive/compare-and-set publication primitive through a same-
filesystem staged file. If the target appears concurrently, compare raw hashes: report
`unchanged` only when identical; otherwise preserve it and block. After creation, read
the plan back as raw bytes, verify byte-for-byte equality with approved content, parse
all internal references, and report SHA-256. A write/read-back/internal-reference
failure is BLOCKED and never produces written status.

Do not create a checkpoint and do not append to session state after the write.

### 5.3 Report an operation ledger

Report each proposed operation independently:

| Operation | Artifact | Result | SHA-256 / Evidence |
|---|---|---|---|
| write-qa-plan | approved immutable plan path | written / unchanged / declined / failed | verified digest or exact reason |

Use `written` only after the read-back verification succeeds. Never report a
path as written, created, updated, registered, or checkpointed when that action
was unselected, declined, aborted, or failed. Never synthesize success for a
legacy backfill-only request.

Final verdicts:

- **Verdict: COMPLETE** — the approved immutable plan was verified `written` or
  verified `unchanged`, its effective state is `CURRENT`, requirement/dependency and
  Test ID ownership matrices are complete, and no required build/evidence state is
  `UNKNOWN` or `REQUIRED_MISSING`.
- **Verdict: PARTIAL** — the approved plan was verified written but has declared
  source or AC/test binding gaps; it is not gate evidence.
- **Verdict: BLOCKED** — approval was declined, a source/target changed before
  write, immutable plan ID conflicted, the CAS/write/read-back failed, or no valid
  owned operation was selected.

Only after a verified write may the response say:
`QA plan written to [path] (sha256:[digest]).`
For a verified no-op, say instead:
`QA plan already current at [path] (sha256:[digest]); no write performed.`

---

## P1 audit traceability

Each exact ID from the authoritative 2026-07-20 P1 audit table has one row that
binds a normative clause to a concrete dedicated-spec case/assertion. These rows
do not claim that any case was executed.

| Audit ID | Normative clause | Dedicated spec evidence |
|---|---|---|
| `QP-004` | Phase 1 exact scope-manifest resolution | Case 1 — assertions `The exact scope authority hash is recorded` and `No undeclared story is read for planning` |
| `QP-005` | Phase 1 ledger/partial coverage and Phase 4 Plan State Rules | Case 2 — assertions `Missing paths have no fabricated hash`, `Verdict is PARTIAL`, and `Gate Evidence remains NO` |
| `QP-006` | Phase 1 hard budgets and Phase 2 bounded context | Case 3 — assertions `Counts reconcile to every declared story and authority`, `No half-loaded closure becomes current`, and `Scope Coverage is PARTIAL` |
| `QP-007` | Phase 2.2 preserve declared story type and record mismatch | Case 4 — assertions `Story bytes remain unchanged` and `Finding records declared type, derived tags and source bindings` |
| `QP-008` | Phase 3 multi-label coverage without a forced primary | Case 5 — assertions `Secondary coverage is not dropped` and `No risk-score tie breaker selects a primary` |
| `QP-009` | Phase 3 observable/risk-driven method selection | Case 6 — assertions `Every method cites observable/risk bindings` and `Unsupported method evidence becomes a gap` |
| `QP-010` | Phase 4 Playtest Requirements current report/recorder adapter | Case 7 — assertions `production/session-logs is never generated`, `Path alone does not establish completion`, and `qa-plan never writes the playtest artifact` |
| `QP-011` | Phase 5.1 complete lossless candidate preview/authorization | Case 8 — assertions `Concatenated chunks reproduce exact candidate bytes` and `Candidate change after approval invalidates authorization` |
| `QP-018` | Invocation and Phase 1 exact scope schema; legacy calls fail closed | Case 9 — assertions `Invalid call fails before scope discovery and preview` and `No newest or title-match fallback occurs` |
| `QP-019` | Contract manifest dedicated-spec requirement and this trace matrix | Case 10 — assertions `Cases are independently runnable from explicit fixtures`, `Side effects and non-writes are testable`, and `Verdict conditions are explicit` |

## Collaborative protocol

- Require the exact scope manifest. If it is absent, stop with the supported invocation
  and perform no discovery or write; never infer scope through a conversational choice.
  Use one complete changeset authorization before the first write.
- Keep source gaps visible; do not guess hashes, AC IDs, test IDs, formulas, or
  acceptance criteria.
- Keep story and checkpoint ownership explicit. Offer a handoff to the owning
  workflow, but never perform that write from `$qa-plan`.
- A user's acceptance of a risk does not make a `PARTIAL` or `STALE` plan
  current and does not authorize downstream implementation.
- Stop after the verified plan result and context-aware next steps.
