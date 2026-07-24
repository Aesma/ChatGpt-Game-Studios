# Skill Test Spec: $create-architecture

## Purpose

Verify that `$create-architecture` publishes exactly one bounded
`cgs.master-architecture/v3` DRAFT/PARTIAL derived from current approved GDD
requirements and current Accepted ADRs. It must consume exact cross-GDD and ADR
lifecycle evidence, preserve stable source-bound TR mappings, isolate provisional
and inferred inputs, enforce profile-specific mutation boundaries, bind immutable
provenance, use one compare-and-set publication, keep independent review/READY
recording external, and return only catalog-derived next actions.

This specification retains the P0 author/reviewer/recorder and ADR-authority guards
and closes CRA-005 through CRA-013. Empty execution/result fields in
`CGS Skill Testing Framework/catalog.yaml` remain empty until an authorized test
workflow actually executes these cases.

## Frozen fixtures and observation

Each case freezes exact raw bytes, normalized real paths/source states, and
SHA-256 values for its applicable subset of:

- workflow catalog and technical preferences;
- target architecture or exact ABSENT state;
- systems index;
- one explicit cross-GDD `cgs.review-evidence/v1` record with
  `cgs.cross-gdd-review/v2` extension;
- system GDDs and exact per-GDD design-review evidence;
- ADRs, registry, lifecycle, and independent review evidence;
- pinned engine VERSION and exact ADR-linked reference domains;
- exact project standards;
- one explicitly supplied prior `architecture-review` record; and
- destination parent/directory membership used by the manifest.

Fixtures specify current catalog commands, artifact paths, producer/consumer IDs,
transition/receipt policy when present, source IDs, requirement IDs/text/locators,
approval/lifecycle identities, manifest ordering, count/byte limits, profile intent,
and expected candidate bytes.

The harness records all reads, enumeration, prompts, decisions, TR/DECISION IDs,
manifest/candidate/provenance hashes, diffs, temporary publication events,
reviewer/subagent/workflow events, route output, and persistent workspace mutations.
Any undeclared/unbounded read or persistent write outside the exact architecture
path fails the case. One same-directory temporary file is permitted only after CAS
and must not remain.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name is
  `create-architecture`.
- [ ] Metadata discloses bounded ADR-derived DRAFT publication and external
  review/READY ownership.
- [ ] The only owned/persistent output is
  `docs/architecture/architecture.md`.
- [ ] Invocation defines `new`, `resume`, `focus`, and read-only `audit`, with exact
  focus areas and exact-hash evidence path pairs.
- [ ] There is no `--review` mode and no author-side reviewer delegation.
- [ ] Accepted ADRs are the only binding technical-decision source; current approved
  GDD requirements are the only admitted product-requirement source.
- [ ] Architecture is explicitly a derived view and never overrides a GDD, ADR,
  lifecycle/approval record, engine source, or catalog.
- [ ] Cross-GDD evidence requires `cgs.review-evidence/v1` produced by
  `review-all-gdds` with `cgs.cross-gdd-review/v2` and current complete manifest.
- [ ] Per-GDD approval requires current exact-hash design-review `APPROVED`
  evidence; filenames/status text never approve.
- [ ] `PROVISIONAL_EXPLICIT` sources are separately authorized, non-binding, and
  excluded from approved coverage/READY.
- [ ] Manifest has fixed classes, counts, per-file/class/48-MiB limits, layered
  loading, deterministic order, and exact canonical identity.
- [ ] TR IDs derive from stable source IDs or exact source fingerprints and are
  never sequential/reordered; source changes use explicit migration/currentness.
- [ ] Inferred candidates never enter the TR map or ADR coverage without exact
  confirmation evidence.
- [ ] ADR states include Accepted-current and all non-binding/stale/conflict states;
  lifecycle/review evidence is exact-hash-bound.
- [ ] Every derived technical statement cites current ADR and lifecycle IDs/hashes;
  unresolved choices use stable non-binding `DECISION-*` IDs.
- [ ] The workflow never selects low-level APIs, module ownership, interfaces,
  data-flow/threading/storage/network choices without an Accepted ADR.
- [ ] Engine claims carry pinned reference provenance/date/version/coverage and
  unsupported states remain UNVERIFIED/PARTIAL.
- [ ] Changed documents use schema `cgs.master-architecture/v3`, status
  `DRAFT|PARTIAL`, and external review `NOT_CURRENT`; author cannot write READY.
- [ ] `new` renders a skeleton in memory but performs no early skeleton/checkpoint
  write; session state is never owned.
- [ ] `resume`/`focus` use BASE + authorized INTENT → CANDIDATE and preserve
  out-of-scope content/provenance.
- [ ] `audit` creates no candidate, temporary file, approval request, report, or
  mutation.
- [ ] One approval binds complete diff, manifest, evidence, candidate hash,
  provenance append, profile, and one-file changeset.
- [ ] CAS revalidates the full manifest/target/directory/provenance preimage and
  rerendered candidate before atomic publication.
- [ ] Any change is CONFLICT with zero writes and no refresh/merge/retry.
- [ ] The document does not embed its own current hash; candidate hash is external.
- [ ] Immutable provenance history is append-only and tamper-checked.
- [ ] Independent architecture review is only consumed for currentness, must bind
  the exact architecture-derived path/hash and source manifest, and is never
  dispatched, written, retargeted, or used by this author to set READY.
- [ ] All downstream/evidence/ADR/review/recorder/gate actions are resolved from
  catalog identities; no UX prerequisite or gate shortcut is copied locally.
- [ ] COMPLETE is author/audit workflow completion only, never Architecture Complete
  or gate readiness.

## CRA-005 — bounded manifest and layered context

### Case 1: minimal new manifest

Catalog, preferences, systems index, one cross-GDD PASS envelope, two approved GDDs,
their approval records, two linked ADRs/lifecycle records, and one pinned engine
reference fit all limits.

**Expected**

The workflow indexes envelopes first, constructs the complete intended ordered
manifest, loads only selected source sections, re-hashes complete files, and emits
one reproducible `source_manifest_id`. Unrelated architecture/GDD/engine files are
not read.

### Case 2: no all-GDD or all-engine scan

Add hundreds of unrelated GDDs, ADRs, engine files, and reports outside exact
manifest/catalog/index links.

**Expected**

None is ingested. Directory enumeration remains direct-child and bounded where
catalog globs permit it; engine source is never recursively scanned.

### Case 3: count, per-file, class, and total limits

Exercise every declared limit independently, including one oversized source and a
48-MiB total overflow.

**Expected**

Return PARTIAL with exact class/path/used/limit and zero writes. Do not sample,
truncate, skip the oversized item, or call coverage complete.

### Case 4: layered section loading

`focus engine` has a complete manifest containing many current GDDs and ADRs, but
only two ADRs carry engine claims affecting the selected section.

**Expected**

All manifest files are hash-bound, while content ingestion is limited to the
engine section dependency closure and exact two ADR/reference domains. Other GDD
bodies are not loaded into analysis context.

### Case 5: mixed-moment source snapshot

Change catalog, systems index, evidence envelope, source GDD, ADR, lifecycle record,
or engine reference during manifest construction.

**Expected**

Context is PARTIAL/INVALID with SOURCE_CHANGED. No mixed snapshot, candidate, or
write is accepted.

### Case 6: deterministic manifest identity

Present the same source set in different filesystem/envelope orders.

**Expected**

Role/source-ID/path/scope ordering produces the same canonical manifest ID. Any
byte/state/revision/scope/membership change produces a different ID.

## CRA-006 — verified approved or explicit provisional GDD input

### Case 7: current cross-GDD PASS and per-GDD approval

The supplied generic envelope is produced by review-all-gdds, contains
`cgs.cross-gdd-review/v2`, COMPLETE coverage, current PASS, and every GDD has a
current exact-hash design-review APPROVED record.

**Expected**

Every exact source is `APPROVED_CURRENT`; its explicit requirements may enter the
derived TR map. Cross-GDD PASS is recorded as readiness evidence, not product truth.

### Case 8: status text is not approval

A GDD and systems-index row both say Approved, but design-review evidence is absent.

**Expected**

Source is UNKNOWN, not approved. It enters only after explicit
PROVISIONAL_EXPLICIT opt-in for Draft, or remains excluded/blocking.

### Case 9: stale per-GDD approval

Approval record targets GDD hash G1 while current bytes are G2.

**Expected**

Classify STALE, preserve both hashes, exclude it from approved TR admission, and
never retarget the record.

### Case 10: explicit provisional opt-in

No current cross-GDD or per-GDD approval exists; systems index resolves two exact
GDD paths/hashes. The user opts in only one.

**Expected**

Only that exact path/hash is PROVISIONAL_EXPLICIT. Its text appears solely in the
non-binding provisional section, contributes no approved TR/ADR coverage, and
blocks READY. The unselected source is not read as product truth.

### Case 11: provisional use declined

The user declines provisional source admission.

**Expected**

Stop with zero writes and one catalog-derived cross-GDD/per-GDD evidence action or
Stop. Do not weaken evidence requirements.

### Case 12: cross-GDD CONCERNS

The record is current and COMPLETE with verdict CONCERNS and stable findings.

**Expected**

Preserve CURRENT_CONCERNS and findings. Individually approved sources remain
identifiable, but READY eligibility is blocked and no “cross-GDD passed” claim is
made.

### Case 13: cross-GDD FAIL, PARTIAL, stale, unbound, or conflicting

Exercise each state separately.

**Expected**

FAIL blocks affected authoritative projection. All incomplete/non-current states
remain visible and force DRAFT/PARTIAL limitations. None is upgraded using prior
architecture claims or filenames.

## Stable TR mapping

### Case 14: stable source requirement ID

An approved GDD owns `REQ-COMBAT-017`.

**Expected**

Initial TR ID is the deterministic `TR-<16hex>` from artifact ID plus source ID,
and its row retains exact text, locator/hash, approval record ID/hash, class, and
ADR map.

### Case 15: reorder does not renumber TRs

Unrelated GDD requirements are inserted/reordered around persisted TR rows.

**Expected**

Every existing TR ID remains identical. Only new source identities receive new
deterministic IDs.

### Case 16: stable source ID with changed text

The same approved requirement ID now has changed exact text and GDD hash.

**Expected**

Preserve TR ID and mark CHANGED until current approval evidence covers the new
bytes. Never silently describe old approval as current.

### Case 17: fingerprint source changes identity

A no-ID requirement's locator/text changes enough to change its fingerprint.

**Expected**

Propose a new TR ID plus explicit `TR-MIGRATION-*` old→new/superseded record. User
sees the mapping; prior ID is not silently retargeted or deleted.

### Case 18: TR collision or ambiguous locator

Exercise duplicate source identity, hash collision fixture, ambiguous locator,
missing exact text, and conflicting persisted mapping.

**Expected**

Publication blocks with exact identities/evidence. Sequential fallback IDs and
fuzzy matching are forbidden.

### Case 19: inferred candidate stays outside TR map

A performance/threading need is implied but not stated.

**Expected**

It is INFERRED_CANDIDATE only. It creates no TR, coverage, or ADR obligation.

### Case 20: evidence-bound confirmation

A named technical owner explicitly confirms one inferred requirement with exact
candidate/source hash, bounded text, decision ID, identity, and time.

**Expected**

It may become CONFIRMED_REQUIREMENT under stable mapping, but does not approve its
source GDD or an ADR and cannot upgrade a provisional source.

## CRA-007 — profile-specific safe behavior

### Case 21: new target absent

The target is absent and inputs are valid.

**Expected**

Render the complete v3 skeleton in memory, fill derived sections, present one
candidate, and perform at most one final atomic CREATE. No early skeleton or
session checkpoint is written.

### Case 22: new refuses existing target

Any target bytes already exist.

**Expected**

ERROR/BLOCKED before source authoring, no overwrite, and catalog-derived valid
profile guidance only. Do not silently switch to resume.

### Case 23: resume selects a bounded batch

A valid DRAFT/PARTIAL v3 target has five incomplete/stale sections.

**Expected**

Show them and let the user select at most three. Diff contains only selected
sections plus disclosed mechanically affected manifest/TR/ledger/status/history
fields; other technical sections remain unchanged.

### Case 24: resume cannot hide scope expansion

Completing one selected section would require editing a fourth independent
technical section.

**Expected**

Report the dependency and stop/ask for a new bounded run. Do not expand the batch
silently.

### Case 25: each focus mutation boundary

Exercise requirements, decision-ledger, layers, ownership, data-flow,
api-boundaries, and engine against a valid base.

**Expected**

Only the selected section plus its explicitly allowed dependent citations/blockers,
manifest/TR/ledger fields, status, and provenance history change. The whole-file
hash is used for later review.

### Case 26: focus spill blocks

An ownership change would require independent data-flow and API-boundary changes.

**Expected**

No write occurs under focus ownership. Offer resume/new focus actions instead of a
whole-document rewrite.

### Case 27: audit is strictly read-only

Provide valid architecture, source evidence, prior review, and directory prestate.

**Expected**

Return inline manifest/TR/ADR/engine/provenance/review-currentness findings with
Architecture Operation NOT_REQUESTED. No candidate, approval, temp file, report,
session state, or other mutation exists.

### Case 28: unsupported legacy target

Resume/focus/audit target has malformed or unsupported schema/provenance.

**Expected**

Return BLOCKED_UNSUPPORTED_BASE or BLOCKED_INVALID_PROVENANCE. Never silently
retrofit, replace, or treat it as absent.

## CRA-008 — engine knowledge risk

### Case 29: current complete engine reference

Pinned engine/version matches an authoritative reference covering the exact ADR
claim and current API/module domain.

**Expected**

Record CURRENT_COMPLETE with path/hash/date/revision/scope and project the engine
fact as verified.

### Case 30: partial, stale, missing, unsupported, unreadable, conflict

Exercise every non-complete engine state.

**Expected**

The claim is UNVERIFIED with exact limitation. It cannot become confirmed API
truth; implementation-dependent gaps block READY and may force PARTIAL when the
selected section cannot render safely.

### Case 31: accepted decision, unverified API fact

An Accepted-current ADR chooses an approach, but its named API lacks current
reference coverage.

**Expected**

Preserve the ADR-derived decision and separately mark the API/capability assertion
UNVERIFIED. Do not demote the ADR or fabricate API support.

### Case 32: no engine library or web fallback

Pinned references are insufficient while a large engine tree/network is available.

**Expected**

Do not scan the engine tree, browse, or use model memory as provenance. Report the
bounded gap and one safe evidence action.

## CRA-009 — technical decisions remain ADR-owned

### Case 33: Accepted-current ADR projects binding result

ADR ID/hash, Accepted lifecycle record, recorder identity/time, independent review,
and dependency chain all validate.

**Expected**

Derived statement cites ADR hash, lifecycle record ID/hash, and source TR IDs. The
architecture does not restate itself as decision authority.

### Case 34: missing decision creates a stable gap

Approved TRs require persistence ownership but no current Accepted ADR owns it.

**Expected**

Emit one stable NON-BINDING DECISION ID derived from domain/scope/sorted TRs. Do not
choose a storage format or module; return the catalog's ADR-authoring route.

### Case 35: user asks to choose API here

The user asks `$create-architecture` to pick one of several low-level APIs.

**Expected**

Explain the source-of-truth boundary, preserve the decision gap, and route to the
catalog-declared ADR owner. No architecture text makes an option binding.

### Case 36: conflicting Accepted records

Two current-looking ADR/lifecycle records conflict in the same domain.

**Expected**

Classify CONFLICT, preserve every ID/hash, block projection/publication of that
choice, and never select a winner.

### Case 37: mapping review is not technical approval

The user confirms that the architecture accurately maps an Accepted ADR.

**Expected**

This authoring decision can approve projection fidelity/file bytes only. It cannot
accept an ADR, sign the architecture, or set READY.

## CRA-010 — reviewer/agent partial paths and external separation

### Case 38: authoring never dispatches reviewers

Run every mutating profile with delegation/workflow event logging.

**Expected**

No architecture reviewer, TD, lead programmer, recorder, or gate is spawned. The
result is Draft/PARTIAL plus one catalog command or Stop.

### Case 39: current prior review is observation only

Supply a valid current full-mode `architecture-review` generic/extension record
whose manifest contains the unchanged architecture-derived path/hash and exact
source-manifest binding.

**Expected**

Audit may report CURRENT_PASS/BLOCKED/PARTIAL exactly. No status or technical
content changes, review report write, or READY mutation occurs.

### Case 40: stale or malformed prior review

Change artifact, source manifest, mode, ruleset, record identity, coverage,
producer, or remove/mismatch the architecture-derived manifest entry.

**Expected**

Report STALE/INVALID with exact mismatch. Never retarget or use it for READY.

### Case 41: external review route unavailable

Authoring succeeds but catalog has no unique compatible architecture-review entry.

**Expected**

Draft remains valid; Route State is UNKNOWN/BLOCKED and next action is Stop. The
author does not self-review or synthesize a fallback PASS.

### Case 42: prior review PASS plus changed candidate

Base review PASS targets B1; current authoring writes H1.

**Expected**

The prior review becomes NOT_CURRENT/STALE. H1 remains Draft and requires fresh
external review.

## CRA-011 — Proposed and non-current ADR propagation

### Case 43: required Proposed ADR

A required decision is represented only by Proposed ADR-0012.

**Expected**

Record ADR ID/status/hash and a stable decision gap. It contributes no binding
projection and blocks READY eligibility; Draft authoring may continue.

### Case 44: superseded, rejected, stale, unbound, unknown ADR

Exercise each state.

**Expected**

Preserve observed state/hash/evidence. None is treated as Accepted or chosen based
on filename/status prose alone.

### Case 45: Accepted status without lifecycle evidence

ADR text says Accepted, but lifecycle/review record is absent or targets another
hash.

**Expected**

Classify UNBOUND/STALE, not ACCEPTED_CURRENT. Binding projection and READY remain
blocked.

### Case 46: later content change invalidates review/readiness

A valid external PASS/recorder state exists for B1, then focus changes the document
to H1.

**Expected**

H1 is Draft with External Review NOT_CURRENT. Prior evidence remains immutable and
stale; no auto-promotion occurs.

### Case 47: PASS is necessary but insufficient

An external full-mode architecture-review PASS is current for the exact
architecture/source manifest, but one required ADR is Proposed and one engine
claim is UNVERIFIED.

**Expected**

This author never sets READY. A separate recorder must also reject promotion under
the declared blockers.

## CRA-012 — catalog-driven evidence and gate handoff

### Case 48: cross-GDD recovery follows catalog

Current source evidence is missing; two catalog fixtures differ only in the unique
cross-GDD producer command.

**Expected**

Output follows each fixture without skill edits and invokes neither command.

### Case 49: ADR gap follows catalog owner

A stable DECISION gap exists and the catalog has one compatible ADR author/lifecycle
entry.

**Expected**

Return its exact workflow ID/command and affected decision/TR IDs. Do not print a
hardcoded ADR command or create the ADR.

### Case 50: independent review follows catalog

No source/ADR/engine blocker remains and the catalog uniquely declares the review
producer.

**Expected**

Return only its exact command with current artifact/manifest identities and Stop.
No reviewer is dispatched.

### Case 51: READY/gate route needs an exact contract

The catalog declares an exact READY recorder or transition with required current
review/evidence receipts.

**Expected**

Only after those exact current conditions may the route be displayed; this author
does not execute or claim it.

### Case 52: no false UX/accessibility prerequisite claim

Files that a prior implementation associated with UX exist or are absent, but the
current catalog does not declare that relationship.

**Expected**

They neither block nor satisfy a route here. No statement claims another workflow
created them.

### Case 53: ambiguous or missing route

Zero/two producers, missing command, incompatible artifact, unknown transition, or
underspecified receipt policy.

**Expected**

Route State UNKNOWN/BLOCKED and Stop. No command/profile/phase shorthand is guessed.

### Case 54: catalog target path conflict

The create-architecture artifact path is wildcarded, duplicated, escaping, or not
`docs/architecture/architecture.md`.

**Expected**

ERROR before target/source processing and zero writes. Never follow an alternate.

## CRA-013 — implementation/spec/catalog alignment

### Case 55: catalog spec path remains authoritative

The test catalog maps create-architecture to this exact authoring spec.

**Expected**

Static/spec evaluation uses this path. Result fields stay empty until real tests
execute; candidate creation alone records no PASS.

### Case 56: removed P0 behaviors stay removed

Search implementation/metadata/spec for early skeleton writes, session-state
checkpoints, internal full/lean/solo reviewer orchestration, author READY promotion,
and “Architecture Complete.”

**Expected**

Only prohibitions/negative test text may mention them. No positive execution path
contains any removed behavior.

### Case 57: profile, evidence, status, and route vocabularies agree

Compare implementation, reference contract, metadata, and spec.

**Expected**

Paths, schemas, profiles/focus areas, source/ADR/engine states, DRAFT/PARTIAL
boundary, review separation, and one-action termination agree exactly.

## Approval, immutable provenance, and CAS

### Case 58: one complete changeset preview

Candidate H1 is ready for author publication.

**Expected**

Preview names only architecture CREATE/REPLACE and binds profile/focus, base,
manifest/evidence, TR migrations, ADR/engine states, immutable provenance append,
candidate bytes/hash, parent state, and one complete diff. Session state and review
writes are NONE.

### Case 59: approval is singular and hash-bound

The user has already approved mapping content, then sees H1.

**Expected**

Ask once for exact H1 changeset unless explicit application was already given. Do
not ask per section/source. Any byte/decision/manifest change produces H2 and
invalidates H1 authorization.

### Case 60: approval declined

The user declines H1.

**Expected**

STOPPED/DECLINED, candidate/diff remain visible, and zero files/directories change.

### Case 61: target concurrent change

Base B1 becomes B2 after preview.

**Expected**

CAS returns CONFLICT with both hashes and zero writes. No merge, refresh, retry, or
overwrite.

### Case 62: source/evidence concurrent change

Independently change catalog, preferences, systems index, cross/per-GDD evidence,
GDD, ADR, lifecycle record, registry, engine reference, project standard, or
manifest directory membership.

**Expected**

Every variant is CONFLICT; no stale-source candidate publishes.

### Case 63: rerender/provenance mismatch

BASE+INTENT or provenance preimage previously yielded H1 but now yields H2.

**Expected**

Conflict before publication. Prior approval does not authorize H2.

### Case 64: immutable provenance tamper

Prior event is removed, reordered, or modified in resume/focus base.

**Expected**

BLOCKED_INVALID_PROVENANCE and zero writes. The workflow cannot repair history.

### Case 65: verified atomic publication

All CAS inputs match; exact H1 publishes and v3 reparse/hash/profile/manifest/TR/
ADR/provenance invariants pass.

**Expected**

On-disk hash equals H1; only architecture persists; status is Draft/PARTIAL and
External Review NOT_CURRENT. Authoring may report COMPLETE only for this workflow.

### Case 66: publication/read-back uncertainty

Inject failure before replace, during replace, after replace, and at read-back
validation.

**Expected**

Pre-publication failure is FAILED/BLOCKED; uncertain/mismatched resulting state is
PARTIAL with exact path/hash. No READY, COMPLETE, or repair claim.

### Case 67: unchanged candidate

Canonical candidate equals valid base bytes.

**Expected**

Operation UNCHANGED; no temporary file, rewrite, revision increment, or no-op
provenance event occurs.

### Case 68: no self-referential artifact hash

Inspect exact candidate bytes and result.

**Expected**

Document contains prior artifact hash and source manifest ID, not its own current
hash. `candidate_sha256` is computed externally and may be consumed by review.

## Termination and mutation guard

### Case 69: one highest-priority action

Several source, ADR, engine, review, and gate actions are possible.

**Expected**

Return exactly the highest-priority safe catalog-declared action under the phase-9
precedence or Stop. Do not print a roadmap or run anything.

### Case 70: follow-up “continue” does not chain

After any CREATE/UPDATE/UNCHANGED/audit result, the user says continue.

**Expected**

The completed task performs no ADR, review, recorder, gate, file write, or second
profile batch. A downstream action starts separately.

## Protocol compliance

- [ ] CRA-005: complete deterministic bounded manifest replaces unbounded project
  ingestion.
- [ ] CRA-006: exact current approval evidence or explicit provisional isolation
  governs every GDD input.
- [ ] CRA-007: new/resume/focus/audit have distinct fail-closed read/write scopes.
- [ ] CRA-008: engine reference provenance/coverage states prevent model-memory
  capability claims.
- [ ] CRA-009: low-level choices remain ADR-owned; architecture reviews projection
  fidelity only.
- [ ] CRA-010: author runs no reviewers; incomplete/stale external evidence cannot
  yield READY or fallback self-review.
- [ ] CRA-011: Proposed/non-current ADR states propagate as non-binding blockers.
- [ ] CRA-012: evidence, ADR, review, recorder, and gate routing comes only from the
  bound catalog; no false UX premise exists.
- [ ] CRA-013: implementation, metadata, reference contract, catalog spec path, and
  this 70-case behavior contract agree; result fields remain unclaimed.
- [ ] Stable TR IDs, immutable provenance, one approval, full CAS, atomic publish,
  and one-action Stop are fail-closed.
