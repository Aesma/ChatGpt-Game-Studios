---
name: qa-plan
description: "Generate a version-bound QA plan for a sprint, feature, or story. Reads stories and their GDD/ADR sources, maps stable acceptance-criterion IDs to stable test IDs, and writes one independent plan without editing stories or session state."
---

## Invocation and execution

Invoke this workflow as `$qa-plan`.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

Arguments: `[sprint | feature: system-name | story: path]`. Treat bracketed
values as optional unless the workflow says otherwise.

Delegate substantive planning work to the `qa-lead` Codex subagent role when it
is available. If that role is unavailable, follow the same responsibilities in
the current agent.

# QA Plan

This skill generates a structured, version-bound QA plan for a sprint, feature,
or individual story. It tells developers what to automate, what to verify
manually, what belongs in the smoke scope, and when playtest evidence is
required.

Run this before implementation begins. A plan produced from incomplete inputs
may still be saved as a planning artifact, but it is `PARTIAL` and cannot satisfy
a downstream quality gate. A plan whose captured source bytes later change is
effectively `STALE` and cannot satisfy a gate until regenerated.

**Owned output:** `production/qa/qa-plan-[scope-slug]-[date].md`

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
candidate artifact: the QA plan path. If no plan write is approved, the
changeset is empty.

---

## Phase 1: Parse and resolve scope

Determine scope from the argument:

- **`sprint`** — read the most recent file in `production/sprints/`. If
  `production/sprint-status.yaml` exists, use it as the primary story list and
  use the sprint plan for metadata. Record both source paths when both are read.
- **`feature: [system-name]`** — find files matching
  `production/epics/*/story-*.md`, filter to stories whose path or title contains
  the system name, and read the matching epic index file when present.
- **`story: [path]`** — validate and select exactly that story path.
- **No argument** — ask the user which supported scope to use: current sprint,
  a specific feature, or a specific story.

Normalize the resolved name to a filesystem-safe `scope-slug` for the output
path. Preserve the human-readable scope name separately. Report:
`Building QA plan for [N] referenced stories in [scope].`

Keep every referenced story path in the scope manifest. A missing or unreadable
story is not discarded: record its source status and make the plan `PARTIAL`.

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
- the scope-defining sprint/status/epic file;
- `design/gdd/systems-index.md` and
  `docs/architecture/control-manifest.md` when present.

The manifest must contain a source record for every story/GDD/ADR path expected
by scope, including a non-loaded status when no digest can be computed. Missing,
unreadable, invalid, or ambiguously referenced story/GDD/ADR input makes the plan
`PARTIAL`; never invent a digest or silently omit the path.

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

### 2.3 Load bounded supporting context

From loaded GDDs use the Acceptance Criteria, Formulas, and Edge Cases sections.
If Edge Cases is absent, record that edge-case coverage is inferred from the
GDD acceptance criteria and story ACs. Use the control manifest only for
applicable test guardrails. Do not turn a source excerpt into a substitute for
the full-file source hash.

---

## Phase 3: Classify test methods and assign stable test IDs

Preserve a story's declared type. If no valid type is declared, infer a proposed
type for planning, label it `inferred`, add a gap, and make the plan `PARTIAL`.

| Story Type | Typical method |
|---|---|
| **Logic** | Unit tests for formulas, rules, state transitions, and boundaries |
| **Integration** | Integration tests for cross-system events, persistence, or round-trips |
| **Visual/Feel** | Reproducible manual check, capture, benchmark, and named sign-off |
| **UI** | Interaction/accessibility automation where feasible plus observable walkthrough checks |
| **Config/Data** | Schema/data validation and an observable smoke check |

Treat each AC independently. A story may use more than one test method; never
drop secondary coverage merely to force one primary classification.

Assign exactly one stable plan item ID per stable AC ID:

- Logic/Integration automated test:
  `TC-[epic-slug]-S[story-number]-AC[criterion-number]`
- Visual/Feel or UI manual check:
  `MC-[epic-slug]-S[story-number]-AC[criterion-number]`
- Config/Data smoke/data check:
  `SC-[epic-slug]-S[story-number]-AC[criterion-number]`

The story number and criterion number must come from the stable AC ID. If the
story already contains a valid plan item ID for that same AC, preserve it. IDs
must remain stable when criterion wording or order changes and must never be
recycled for a different AC. Duplicate IDs or a mismatch between an ID and its
AC are gaps that make the plan `PARTIAL`.

Each plan item records: story path, stable AC ID, stable test/check ID, method,
test/evidence path, Given/When/Then or Setup/Verify/Pass condition, edge cases,
and required sign-off. Do not invent unsupported requirements; record an input
gap instead.

Show the classification and AC-to-test mapping table before the write preview.

---

## Phase 4: Generate the plan

Generate a complete document with this structure:

```markdown
# QA Plan: [scope name]

**Generated**: [ISO-8601 timestamp]
**Generated by**: $qa-plan
**Scope**: [scope]
**Engine**: [engine or Not configured]
**Plan State at Generation**: [CURRENT | PARTIAL]

## Plan Manifest

`manifest_version: 1`
`hash_algorithm: sha256`

### Sources

| Role | Path | Status | SHA-256 |
|---|---|---|---|
| story | [path] | loaded | sha256:[digest] |
| gdd | [path] | loaded | sha256:[digest] |
| adr | [path] | loaded | sha256:[digest] |

### Story Requirement Bindings

| Story ID | Story Path | Story Hash | GDD Paths + Hashes | ADR Paths + Hashes | Stable AC IDs | Coverage |
|---|---|---|---|---|---|---|
| [stable ID] | [path] | sha256:[digest] | [path + digest] | [path + digest] | [IDs] | complete/gaps |

### Plan State Rules

- CURRENT: every required story/GDD/ADR loaded and every AC has one stable test/check ID.
- PARTIAL: a required source/hash/AC binding is missing, invalid, or ambiguous.
- STALE: any current source bytes no longer match the captured hash, or a captured source disappears.

## Coverage Gaps

- [None, or exact story/source/AC gap and owning workflow]

## Test Summary

| Story | Stable AC ID | Stable Test/Check ID | Method | Automated | Manual |
|---|---|---|---|---|---|

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

Playtest evidence must use the canonical completed-result contract:
`production/playtests/<session-id>/report.md`. A plan item may name that path as
its expected evidence, but a template, protocol, raw log, review, ingest-only
session, legacy path, or report without `Status: COMPLETED`, `Gate Eligible:
YES`, and matching source hashes cannot satisfy the item or count as a session.

| Stable Check ID | Story | Goal | Evidence Path | Sign-off Owner |
|---|---|---|---|---|

## Definition of Done

- [ ] Effective plan state is CURRENT after source revalidation.
- [ ] Every stable AC ID has passing automated or approved manual evidence.
- [ ] Required smoke checks pass.
- [ ] Required evidence exists at the named canonical path.
```

The source table and story binding table are mandatory. `PARTIAL` plans retain
all known records and gaps; they must not disguise an absent hash as current.

### Effective-state revalidation contract

Before this plan is reused, imported into a story, or consumed by
`$smoke-check`, `$story-done`, `$regression-suite`, or another gate:

1. Read every captured source path and hash its current raw bytes.
2. Compare current digests and source availability with the manifest.
3. Treat any mismatch, disappearance, or newly unreadable source as `STALE`,
   regardless of the stored `Plan State at Generation` label.
4. Reject `PARTIAL` and `STALE` as gate evidence. Regenerate the plan from
   current sources.
5. Preserve stable AC and test/check IDs when regenerating; update hashes and
   requirement text from current sources.

This computed effective state avoids mutating the plan merely to mark it stale.

---

## Phase 5: Preview, authorize, write, and verify

### 5.1 Preview one complete changeset

Show the complete generated plan or an inspectable full artifact/diff. Then show:

```text
Proposed changeset
- CREATE or UPDATE production/qa/qa-plan-[scope-slug]-[date].md

Explicit non-writes
- all in-scope story files
- production/session-state/active.md
- all GDD, ADR, sprint, registry, and architecture files
```

If the target already exists, read and record its raw-byte SHA-256 for the
preview and describe the operation as `UPDATE`; do not describe it as a new
file. Ask once whether to apply this exact one-file changeset.

There is no story-backfill or session-state option. If the user asks for one,
explain that the story/checkpoint owner must perform it and do not include it in
this changeset.

### 5.2 Apply only the selected operation

If approved, immediately before writing:

- re-hash every loaded story/GDD/ADR and abort if any digest changed since plan
  generation;
- for an update, re-hash the target and abort if it differs from the previewed
  target hash;
- write only the plan file, exactly as previewed.

If an existing target is already byte-for-byte identical to the approved
content, do not rewrite it; verify it and report `unchanged`. Otherwise, after
writing, read the plan back as raw bytes and verify byte-for-byte equality with
the approved content. Compute and report the plan's SHA-256 in either case.

Do not create a checkpoint and do not append to session state after the write.

### 5.3 Report an operation ledger

Report each proposed operation independently:

| Operation | Artifact | Result | SHA-256 / Evidence |
|---|---|---|---|
| write-qa-plan | [path] | written / unchanged / declined / failed | [verified digest or reason] |

Use `written` only after the read-back verification succeeds. Never report a
path as written, created, updated, registered, or checkpointed when that action
was unselected, declined, aborted, or failed. Never synthesize success for a
legacy backfill-only request.

Final verdicts:

- **Verdict: COMPLETE** — the approved plan was verified `written` or verified
  `unchanged`, and its effective state at result time is `CURRENT`.
- **Verdict: PARTIAL** — the approved plan was verified written but has declared
  source or AC/test binding gaps; it is not gate evidence.
- **Verdict: BLOCKED** — approval was declined, a source/target changed before
  write, the write/read-back failed, or no valid owned operation was selected.

Only after a verified write may the response say:
`QA plan written to [path] (sha256:[digest]).`
For a verified no-op, say instead:
`QA plan already current at [path] (sha256:[digest]); no write performed.`

---

## Collaborative protocol

- Ask for scope only when it was not supplied, then use one complete changeset
  authorization before the first write.
- Keep source gaps visible; do not guess hashes, AC IDs, test IDs, formulas, or
  acceptance criteria.
- Keep story and checkpoint ownership explicit. Offer a handoff to the owning
  workflow, but never perform that write from `$qa-plan`.
- A user's acceptance of a risk does not make a `PARTIAL` or `STALE` plan
  current and does not authorize downstream implementation.
- Stop after the verified plan result and context-aware next steps.
