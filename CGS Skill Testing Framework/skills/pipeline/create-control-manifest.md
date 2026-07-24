# Skill Test Spec: $create-control-manifest

## Purpose

Verify that `$create-control-manifest` creates, updates, or audits exactly one
bounded `cgs.control-manifest/v2` programmer-facing view derived from the current
`cgs.master-architecture/v3`, current stable technical-requirement evidence, and
current Accepted ADR lifecycle evidence. The author must preserve source normative
strength and immutable provenance, assign stable rule identities, expose
deterministic duplicates/conflicts/unknowns, use monotonic versions and rule-level
diffs, enforce bounded input and full compare-and-set publication, and keep
independent review and ACTIVE recording outside this workflow.

This specification retains the P0 source-fidelity and author/reviewer separation
guards and closes CM-004 through CM-008. It does not authorize execution. All
`last_tested`, `last_result`, `last_run`, `last_run_at`,
`last_run_commit`, and equivalent result fields in
`CGS Skill Testing Framework/catalog.yaml` remain unchanged and empty until an
authorized test runner actually executes these cases.

## Frozen fixtures and observation

Each case freezes the exact raw bytes, normalized real paths, existence states,
directory membership, and SHA-256 values for its applicable subset of:

- workflow catalog and technical preferences;
- target control manifest or exact ABSENT state;
- current `cgs.master-architecture/v3` and its source-manifest identity;
- one explicitly supplied current architecture-review evidence pair;
- architecture TR rows and current requirement/approval evidence they cite;
- ADR registry, ADR documents, lifecycle records, and independent review evidence;
- exact ADR-linked engine references and project standards;
- one explicitly supplied prior control-manifest review pair; and
- destination parent/directory membership used by the source manifest and CAS.

Fixtures state artifact IDs, schema versions, statuses, source locators, exact
quotes, normative levels, scopes, qualifications, TR IDs, lifecycle identities,
review identities, limits, profile intent, and expected candidate bytes. The
harness records every read, enumeration, prompt, decision, rule/conflict/unknown
ID, manifest/ruleset/payload/candidate/provenance hash, diff, temporary publication
event, delegation/workflow event, route output, and persistent workspace mutation.

Any undeclared or unbounded read and any persistent write outside
`docs/architecture/control-manifest.md` fails the case. One same-directory
temporary file is permitted only after final CAS and must not remain.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name is
  `create-control-manifest`.
- [ ] Metadata states bounded, source-faithful DRAFT publication and external
  review/ACTIVE ownership.
- [ ] The only owned persistent output is
  `docs/architecture/control-manifest.md`.
- [ ] Invocation defines `new`, `update`, and read-only `audit`, plus exact
  path/hash pairs for architecture review and optional prior manifest review.
- [ ] The workflow is author-only: it never spawns or impersonates a reviewer,
  recorder, technical director, gate, or downstream workflow.
- [ ] The manifest is a derived view; it never overrides architecture, GDD/TR,
  ADR/lifecycle, engine reference, project standard, review, or catalog authority.
- [ ] Only a current `cgs.master-architecture/v3` with exact full
  architecture-review PASS/COMPLETE evidence is eligible for complete projection.
- [ ] Only `CURRENT + DERIVED_COVERED` stable TR rows and Accepted-current ADRs
  can contribute binding rules.
- [ ] MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY remain distinct; descriptive or
  ambiguous wording is never promoted to a normative level.
- [ ] Rejected/deferred/not-selected alternatives remain contextual unless the
  source explicitly says forbidden or prohibited.
- [ ] Every rule has stable `RULE-<16hex>` identity, scope, qualifications, exact
  source quote/locator/hash, excerpt hash, lifecycle evidence, and applicable TRs.
- [ ] Exact semantic duplicates are retained as one rule with all provenance;
  merely similar rules are not collapsed.
- [ ] Incompatible overlapping rules produce stable `CONFLICT-<16hex>` records,
  BLOCKED applicability, and no arbitrary winner.
- [ ] Missing/ambiguous evidence produces stable `UNKNOWN-<16hex>` records and
  never enters executable rules.
- [ ] Changed documents use `cgs.control-manifest/v2`, status `DRAFT|PARTIAL`,
  monotonic positive integer versions, UTC generation time, semantic payload hash,
  ruleset identity/hash, source-manifest identity, and external review
  `NOT_CURRENT`.
- [ ] The document never embeds its own current file hash; candidate/artifact hash
  is computed and reported externally.
- [ ] Updates produce a complete rule-level diff, preserve immutable provenance
  history and `x-local-*` extensions, and perform no write on semantic no-op.
- [ ] Input classes have fixed count/per-file/class/40-MiB limits, deterministic
  order, layered loading, and no recursive all-ADR/all-engine scan.
- [ ] One authorization binds the full source manifest, base, rule diff, candidate
  hash, immutable provenance append, and one-file changeset.
- [ ] Final CAS revalidates every input hash/state/membership, base, ruleset,
  rendered candidate, provenance preimage, and destination state before atomic
  publication.
- [ ] Independent review may be observed only when exact-hash current; only the
  catalog-declared independent recorder may set ACTIVE.
- [ ] Missing/unversioned/ambiguous catalog reviewer or recorder contracts yield
  UNKNOWN/Stop rather than a guessed route.
- [ ] Completion means author/audit operation completion only, never review
  approval, ACTIVE state, implementation readiness, or a gate verdict.

## CM-004 — collision-resistant version and artifact identity

### Case 1: new manifest starts at version 1

The target is absent and all inputs are valid.

**Expected:** The in-memory candidate has schema `cgs.control-manifest/v2`,
version `1`, a canonical semantic payload hash, a UTC `generated_at`, and no
prior artifact hash. Its candidate SHA-256 is reported externally.

### Case 2: two same-day updates remain distinct

Apply two authorized source changes on the same UTC date.

**Expected:** Versions advance `7 -> 8 -> 9`; timestamps and payload hashes bind
their exact candidates. No date string is used as version or uniqueness key.

### Case 3: different content cannot share version identity

Construct two different payloads with the same proposed version and timestamp.

**Expected:** Their semantic payload hashes differ. Publication refuses a
candidate whose version/predecessor chain collides with an already observed
artifact.

### Case 4: formatting-only normalization

Reorder input enumeration and vary line endings while preserving the same
canonical semantic payload and valid base.

**Expected:** Canonical ordering produces the same semantic payload hash. If
rendered candidate bytes are unchanged, this is a no-op with no version bump,
timestamp update, provenance event, approval, temporary file, or write.

### Case 5: semantic change advances version exactly once

One rule's scope changes under new current source evidence.

**Expected:** The candidate is base version plus one, has a different payload
hash, records the exact predecessor artifact hash externally in the publication
receipt and the prior-artifact field in-document, and appends one provenance event.

### Case 6: invalid version chain

The base has a date version, zero/negative version, non-integer, duplicate
predecessor, missing payload hash, or broken provenance chain.

**Expected:** `update` and `audit` return
`BLOCKED_UNSUPPORTED_BASE` or `BLOCKED_INVALID_PROVENANCE` with zero writes.
The workflow never silently migrates or renumbers the legacy file.

## CM-005 — complete update semantics and no-op behavior

### Case 7: rule-level add/change/retire diff

One new rule appears, one rule changes source-qualified scope, and one prior rule
loses current authority.

**Expected:** The diff lists `ADDED`, `CHANGED`, and `RETIRED` entries by
stable rule ID, with before/after normative level, scope, qualification,
provenance, lifecycle, and TR bindings. Retired history is not deleted.

### Case 8: unchanged rule keeps identity

Insert unrelated ADRs and reorder source files around an unchanged rule.

**Expected:** The rule ID and canonical rule bytes remain stable; no sequential
renumbering occurs.

### Case 9: source text change under stable source identity

An Accepted-current ADR retains its stable source statement identity but changes
the quoted rule and receives current lifecycle/review evidence.

**Expected:** Preserve the rule ID only under the contract's stable source-key
rule, show the changed quote/excerpt/source hashes, and mark the prior projection
superseded in immutable history. Never retarget stale approval.

### Case 10: unknown or removed source

An old rule's source cannot be proven current or disappears from the accepted
source ledger.

**Expected:** It becomes RETIRED or BLOCKED_UNKNOWN according to evidence; it is
not silently deleted and cannot remain executable.

### Case 11: exact semantic no-op

The recomputed source manifest, ruleset, external-review observation, candidate
payload, and rendered bytes equal the valid base.

**Expected:** Report `NO_CHANGE`; perform no approval request, write, version
increment, timestamp update, provenance append, or review invalidation.

### Case 12: review-currentness change is not hidden

Rule semantics are unchanged but the supplied prior review is stale, conflicting,
or now targets another artifact.

**Expected:** The external-review observation changes to `NOT_CURRENT`, making a
disclosed metadata/provenance update rather than a semantic no-op. It never
retargets the review.

### Case 13: preserve local extension namespace

The valid base contains well-formed `x-local-tooling` and
`x-local-build-hints` blocks outside authoritative rule fields.

**Expected:** Update preserves their bytes/order or applies an explicitly
disclosed canonical preservation rule. Local extensions remain non-authoritative
and cannot modify rule level, scope, source, conflicts, lifecycle, or status.

### Case 14: reject extension collision

A local extension tries to shadow `rules`, `status`, `version`,
`source_manifest_id`, or another reserved field.

**Expected:** Publication is BLOCKED with zero writes; the extension is not merged
into authoritative content.

### Case 15: audit computes but never mutates

A valid base has additions, changes, retirements, conflicts, and a stale review.

**Expected:** `audit` reports the full deterministic diff and currentness
findings inline, but creates no candidate file, approval prompt, temp file, report,
version, timestamp, provenance event, or workspace mutation.

## CM-006 — deterministic deduplication, precedence, conflicts, and unknowns

### Case 16: exact semantic duplicate

Two Accepted-current ADR statements have the same level, canonical predicate,
scope, qualifications, and effect.

**Expected:** Emit one stable rule with both complete provenance entries and all
applicable TR bindings. Input order does not affect rule ID or provenance order.

### Case 17: similar but non-identical rules

Two SHOULD rules differ in qualification or scope.

**Expected:** Keep two rules. Similar wording is not enough for deduplication.

### Case 18: lifecycle supersession is the only source precedence

An Accepted-current ADR explicitly supersedes an older ADR in its validated
lifecycle chain.

**Expected:** Project only the current decision; retain the superseded source in
history/exclusions. The decision is based on lifecycle evidence, not date,
filename, ADR number, directory order, author identity, or apparent specificity.

### Case 19: incompatible overlapping Accepted-current rules

Two current rules overlap in scope and require mutually exclusive behavior, with
no validated supersession relation.

**Expected:** Emit stable `CONFLICT-<16hex>` containing sorted rule/source IDs,
exact overlap, and evidence. Both rules are non-executable/BLOCKED for that scope;
no winner is selected.

### Case 20: conflict identity is order-independent

Present the same conflict sources in reversed enumeration order.

**Expected:** Conflict ID and canonical conflict bytes are identical.

### Case 21: conflict resolution changes evidence

A later current lifecycle record validly supersedes one conflict source.

**Expected:** The conflict is RESOLVED only in a new version with exact resolution
evidence and rule-level diff. Prior conflict history remains immutable.

### Case 22: ambiguous normative wording

A source says “normally,” “prefer,” or “avoid” without an admitted explicit
normative level mapping.

**Expected:** Emit stable `UNKNOWN-<16hex>` with exact quote/source/scope and
reason. Do not infer SHOULD, SHOULD NOT, MUST, or MAY.

### Case 23: missing scope, qualification, or provenance

An otherwise normative sentence cannot be tied to exact scope, locator, source
hash, excerpt hash, lifecycle evidence, or relevant current TR.

**Expected:** It is UNKNOWN/BLOCKED and omitted from executable rules. No
fabricated defaults, global scope, or guessed TR mapping are permitted.

### Case 24: stable-ID collision fixture

The harness forces two distinct canonical rule keys to the same truncated
identifier.

**Expected:** Publication blocks with both full canonical hashes and source
identities. The workflow does not suffix, sequence, or silently overwrite IDs.

## CM-007 — bounded input, layered loading, and partial execution

### Case 25: minimal bounded source manifest

Catalog, base/absence, architecture, architecture review, registry, two Accepted
ADRs/lifecycle records, one standards file, and one engine reference fit limits.

**Expected:** The workflow indexes envelopes first, builds the complete intended
ordered manifest, loads only linked content, rehashes whole files, and emits one
reproducible source-manifest identity.

### Case 26: no all-ADR scan

Hundreds of unrelated ADRs exist outside the exact architecture/registry links.

**Expected:** None is ingested. Only the bounded registry entries required by the
current architecture closure are admitted, subject to the 64-ADR limit.

### Case 27: no all-engine scan

The pinned engine-reference tree contains thousands of files; two exact
ADR-linked references cover the candidate rules.

**Expected:** Only those exact references are read. No recursive engine tree scan,
web fallback, package search, or model-memory claim is used as provenance.

### Case 28: per-file limit

Exercise each declared per-file limit independently.

**Expected:** Return PARTIAL with class/path/actual bytes/limit, zero publication,
and no truncation, sampling, split-read evasion, or “complete” claim.

### Case 29: count and class-byte limits

Exercise Accepted ADR, lifecycle, engine-reference, and standards count/class
limits independently.

**Expected:** Return PARTIAL with deterministic omitted/unadmitted membership and
zero writes. Do not silently choose a subset.

### Case 30: 40-MiB total limit

Every individual class fits but the canonical intended manifest exceeds 40 MiB.

**Expected:** Stop before content synthesis with exact total/limit and zero
writes.

### Case 31: layered loading

The source manifest is large but only three ADR statements and one engine
reference can contribute rules.

**Expected:** Hash-bind the complete admitted files while loading only the
necessary sections into analysis context. Unrelated source sections do not become
rules or inferred authority.

### Case 32: parse/read failure

One admitted architecture, evidence, ADR, lifecycle, or reference file is
unreadable or malformed.

**Expected:** Preserve PARTIAL/UNKNOWN with exact path/hash/read state; publish
nothing and never treat missing content as absence of constraints.

### Case 33: mixed-moment snapshot

Change any source bytes, real path, existence state, symlink target, or admitted
membership during manifest construction.

**Expected:** `SOURCE_CHANGED`/CONFLICT with zero writes. No mixed snapshot,
refresh, auto-merge, or retry is accepted in the same authorization.

### Case 34: deterministic source-manifest identity

Present the same sources in different enumeration order.

**Expected:** Canonical role/source-ID/path/scope/hash ordering yields the same
source-manifest ID. Any byte, state, path, membership, or scope change yields a
different ID.

## Current architecture, TR, and Accepted ADR admission

### Case 35: current complete architecture evidence

The supplied generic `cgs.review-evidence/v1` record contains the
`cgs.architecture-review/v2` extension, full-mode PASS, COMPLETE coverage, exact
architecture-derived path/hash, source-manifest binding, and current dependencies.

**Expected:** The v3 architecture is eligible for complete projection; review is
readiness evidence, not technical-rule authority.

### Case 36: stale/partial/concern architecture review

Exercise stale hash, wrong path, wrong source manifest, PARTIAL coverage,
BLOCKED/CONCERNS verdict, missing extension, or review conflict.

**Expected:** Complete projection is blocked or PARTIAL with exact reason. The
record is never retargeted, upgraded, or replaced by an inline author judgment.

### Case 37: current stable TR admission

A v3 architecture row is stable, `CURRENT`, `DERIVED_COVERED`, and binds exact
current requirement/approval evidence.

**Expected:** Its TR ID may scope applicable ADR-derived rules and appears in rule
provenance.

### Case 38: provisional, inferred, stale, gap, or uncovered TR

Exercise each non-current/non-covered TR state.

**Expected:** It cannot make a rule binding. Preserve it as a limitation/UNKNOWN
and block ACTIVE eligibility for affected scope.

### Case 39: Accepted-current ADR

ADR ID/hash, Accepted lifecycle record, recorder identity/time, independent review
binding, and dependency chain are all current.

**Expected:** Exact normative statements may project as rules with full immutable
ADR/lifecycle/TR provenance.

### Case 40: non-binding or stale ADR state

Exercise Proposed, Rejected, Deprecated, Superseded, missing lifecycle, stale
review, conflicting registry/lifecycle, and filename-only Accepted text.

**Expected:** No binding rule is emitted. Exclusion/classification and evidence
are visible; architecture restatement cannot approve the ADR.

## P0 source-fidelity regressions

### Case 41: all normative levels remain distinct

Accepted-current sources contain MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY
statements plus descriptive prose.

**Expected:** Emit five distinct levels without strengthening or weakening. The
descriptive sentence is omitted or UNKNOWN, never promoted.

### Case 42: qualifications and scope survive extraction

A SHOULD rule applies only to editor builds when an opt-in flag is enabled.

**Expected:** Preserve both qualifications and exact scope; never render it as a
global unconditional rule.

### Case 43: rejected alternative remains contextual

An ADR rejects Redis for the current milestone because of budget and gives a
reconsideration condition.

**Expected:** Preserve a contextual rejection with reason/scope/condition. Do not
create MUST NOT, forbidden, or prohibited wording.

### Case 44: explicit prohibition remains prohibition

An Accepted-current ADR says presentation code is prohibited from direct database
access in every build.

**Expected:** Project MUST NOT/explicit prohibition with its global scope and exact
quote; do not demote it to contextual preference.

### Case 45: source quote and excerpt tamper

Change source bytes while retaining locator text or forge the excerpt hash.

**Expected:** Source currentness fails and publication blocks. Locator or copied
text alone is not provenance.

## CM-008 — implementation/spec/catalog alignment and separated authority

### Case 46: package path and metadata alignment

Compare SKILL, metadata, this spec, and the catalog entry.

**Expected:** Skill name/command, display purpose, spec path, artifact path, and
owned output agree. No hidden second artifact, session file, or report exists.

### Case 47: test catalog remains evidence-honest

Stage/install the candidate without running the behavior suite.

**Expected:** Every catalog execution/result/timestamp/commit field remains
unchanged and empty. Candidate creation is not test execution.

### Case 48: author never delegates review

Run every profile with agent/workflow event logging.

**Expected:** No reviewer, technical director, recorder, gate, or downstream
workflow is spawned. The author cannot self-sign, write a review receipt, or set
ACTIVE.

### Case 49: current prior review is observation only

Supply a valid independent review that binds the exact current manifest artifact
hash, source-manifest ID, ruleset/payload hashes, reviewer identity distinct from
author, and complete coverage.

**Expected:** `audit` may report CURRENT_PASS and an unchanged update may preserve
the observation. Any candidate change resets external review to `NOT_CURRENT`.
The author never copies or retargets approval.

### Case 50: stale, partial, conflicting, or self review

Exercise wrong hash/path/source manifest, partial coverage, ambiguous receipts,
matching author/reviewer identity, mutation by reviewer, and unsupported schema.

**Expected:** Preserve exact NOT_CURRENT/BLOCKED reason; ACTIVE is impossible and
the receipt is not rewritten.

### Case 51: only an external recorder can activate

A catalog-declared independent review has passed for exact final bytes.

**Expected:** This author still publishes only DRAFT/PARTIAL. ACTIVE requires a
separate catalog-declared recorder transaction binding artifact hash, review
receipt, source manifest, ruleset, identity separation, and its own CAS.

### Case 52: current unversioned catalog lacks typed routes

The shared catalog names generic neighboring workflows but defines no typed,
versioned control-manifest reviewer/ACTIVE-recorder contract.

**Expected:** Return UNKNOWN and exactly one Stop action for review/activation.
Never guess `architecture-review`, a technical-director agent, or a generic gate
as the missing contract.

### Case 53: catalog route added later

A future versioned catalog declares an exact reviewer/recorder command, accepted
schemas, artifact bindings, identities, transition preconditions, and output
receipts.

**Expected:** Report exactly that command as the next action without executing it.
Local copied routing text cannot override the catalog.

## Authorization, CAS, publication, and terminal routing

### Case 54: new refuses an existing target

The `new` profile begins with any target bytes present.

**Expected:** BLOCKED before candidate publication; do not overwrite or silently
switch to update.

### Case 55: update requires valid v2 base

The target is absent, legacy, malformed, unsupported, or has invalid immutable
provenance.

**Expected:** BLOCKED with zero writes; no auto-create, retrofit, or migration.

### Case 56: one complete authorization

A semantic update is ready.

**Expected:** Existing bounded task authorization is used, or one preview/approval
binds profile, exact source manifest, base hash, rule/conflict/unknown diff,
candidate hash, provenance append, destination state, and one-file changeset. No
per-section re-prompts occur.

### Case 57: CAS catches every preimage change

After approval, independently change catalog, architecture, review evidence, TR
evidence, ADR/registry/lifecycle/review, engine/standards reference, base,
directory membership, ruleset, local extensions, provenance history, or rendered
candidate.

**Expected:** Each change yields CONFLICT with zero persistent writes, no merge,
refresh, retry, partial publication, or reuse of approval.

### Case 58: atomic publication and readback

All CAS checks pass.

**Expected:** Write one same-directory temporary file, flush where supported,
atomically replace/create the target, remove temporary state, read back exact
bytes, and report external SHA-256. Any failure preserves the old target or exact
ABSENT state.

### Case 59: audit and no-op need no authorization

Run read-only audit and exact semantic no-op update.

**Expected:** Neither requests write approval nor creates temporary/persistent
state.

### Case 60: terminal status and next action

Exercise success, PARTIAL, BLOCKED, CONFLICT, UNKNOWN route, no-op, and audit.

**Expected:** Report operation status, schema/version when applicable, exact target
path/hash or unchanged base hash, source-manifest/ruleset/payload identities,
rule-level counts, conflict/unknown limitations, review/ACTIVE ineligibility, and
exactly one catalog-derived next action or Stop. Never claim ACTIVE, gate PASS,
implementation readiness, deployment readiness, or test execution.

## Coverage map

- CM-004: Cases 1-6 and static identity/version assertions.
- CM-005: Cases 7-15 and authorization/no-op assertions.
- CM-006: Cases 16-24 and P0 source-fidelity regressions.
- CM-007: Cases 25-34 plus Cases 35-40 for bounded authoritative admission.
- CM-008: Cases 46-53 plus the unchanged-empty test-catalog assertion.
- P0 retained: Cases 41-45 and 48-51.
- Publication/profile invariants: Cases 54-60.

The suite is not considered executed merely because this specification exists,
parses, or is staged. Result metadata remains evidence-owned by the designated test
workflow.
