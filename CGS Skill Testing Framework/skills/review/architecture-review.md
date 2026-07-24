# Skill Test Spec: $architecture-review

## Skill Summary

`$architecture-review` is a bounded, hash-bound, read-only architecture
traceability gate. It reviews only explicit owner-approved requirements, current
ADR decisions, exact Requirement → ADR → Story → Test Run links, pinned engine
evidence, and profile-permitted independent reviewer results against one
complete target manifest.

Its gate verdict is exactly `PASS`, `BLOCKED`, or `PARTIAL`. Invalid invocation
or absence of a meaningful primary target returns `ERROR` without a gate
verdict. The skill emits an embedded `cgs.review-evidence/v1` envelope with a
`cgs.architecture-review/v2` extension.

The workflow changes zero files by default. With exact approval it may create
one new immutable report. It never edits GDDs, requirements, ADRs,
`architecture.md`, registries, indexes, stories, tests, test runs, systems
status, logs, sign-off, accepted-risk records, or session state. It does not
perform an eight-section architecture-document review.

`cgs.architecture-review-rules/v1` owns authority, mode isolation, shard limits,
reviewer profiles, input/empty-set states, stable findings, blocker proof, and
verdict precedence.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and non-empty `description`; name
      matches the skill directory
- [ ] Public modes are exactly `full`, `coverage`, `consistency`, `engine`,
      `single-gdd`, and `rtm`
- [ ] `single-gdd` accepts exactly one canonical `path:` or stable `id:` selector
      and forbids fuzzy/title/name lookup
- [ ] Gate verdict vocabulary is exactly PASS / BLOCKED / PARTIAL; invalid
      invocation returns ERROR with no verdict
- [ ] Default write set is empty and the only optional write is one exact new
      explicitly approved immutable report
- [ ] Explicitly prohibits changes to GDD/TR/ADR, architecture, registries,
      systems/traceability indexes, stories/tests/runs, statuses, logs, sign-off,
      accepted risk, and session state
- [ ] Explicitly forbids using or proposing `Needs Revision` as a systems-index
      status
- [ ] Defines streaming before/after path/size/SHA-256 mutation guard batches
- [ ] Requires a complete canonical target manifest, ruleset hash,
      skill-bundle hash, target manifest hash, and stale key
- [ ] Defines numeric artifact/index/edge/byte/snapshot/reviewer limits and
      exposes every planned shard/check plus unchecked scope
- [ ] Replaces ADR all-pairs comparison with explicit typed-key candidate groups
      and directed dependency graph checks
- [ ] Defines a strict six-mode phase/input/reviewer matrix with FORBIDDEN and
      NOT_APPLICABLE behavior
- [ ] Requires owner, approval, timestamp, immutable text, source path/hash,
      lifecycle, and exact ID before admitting a requirement
- [ ] Classifies inferred prose as CANDIDATE_REQUIREMENT and never allocates IDs
- [ ] Requires exact IDs for ADR/story/test links and classifies implicit links
      as UNVERIFIED_LINK
- [ ] Treats test-source existence as DISCOVERED_NOT_EXECUTED and only current
      authoritative EXECUTED_PASS as passing evidence
- [ ] Defines one source authority for product rules, requirement lifecycle,
      ADR decisions, derived views, implementation links, runs, and engine facts
- [ ] Defines reviewer statuses DONE / DECLINED / TIMEOUT / ERROR /
      NOT_APPLICABLE, caps reviewers at two, and makes required failure prevent
      PASS
- [ ] Defines applicability/presence/currentness ledgers with explicit
      PRESENT/MISSING/NOT_APPLICABLE semantics
- [ ] Defines a versioned blocker matrix where unknown, stale, partial, or
      unchecked evidence cannot PASS and cannot be guessed into a blocker
- [ ] Emits fenced `cgs.review-evidence/v1` plus
      `cgs.architecture-review/v2`, stable finding IDs/dispositions, complete
      coverage, reviewer ledger, risk references, and canonical record ID
- [ ] Uses unique fractional-UTC + manifest report identity and forbids mtime,
      filename date, directory order, or vague latest selection
- [ ] ACCEPTED_RISK remains separate and cannot convert a verdict
- [ ] Ends with one destination-owner handoff, `Stop here`, and no invoked
      workflow

---

## Gate Ownership

No reviewer or delegated role owns the gate verdict. Reviewers return bounded
`cgs.architecture-review-worker/v1` evidence only. The coordinator applies the
versioned matrix mechanically after validating all hashes and coverage.

---

## Contract Cases

### Case 1: Happy-path bounded full review

Fixture:

- Current manifest contains explicit approved requirements, current ADRs,
  pinned engine references, and contract-required stories/tests/runs
- Every exact link is present and current
- Required test runs are authoritative EXECUTED_PASS
- Typed conflict/dependency groups are clean
- Technical-director and lead-programmer both return DONE on the same manifest
- All files fit bounded shards and mutation guard passes

Input: `$architecture-review full`

Assertions:

- [ ] Every input class, path/hash, index record, edge, shard, check, and reviewer
      is accounted
- [ ] Only explicit approved requirements enter the baseline
- [ ] Verdict is PASS and no legacy verdict appears
- [ ] Machine envelope and human projection agree
- [ ] No file changes by default

### Case 2: Mutation guard and optional report write

Fixture: Exercise conversational review, one exactly approved new report path,
an existing report path, and an unauthorized source/index/session change.

Assertions:

- [ ] Conversational review permits zero changed paths
- [ ] Approved save creates only
      `docs/architecture/reviews/architecture-review-<fractional-UTC>-<manifest12>-<uuid8>.md`
- [ ] Existing target is refused without overwrite/append/rename
- [ ] Saved bytes are re-read and record/manifest/file hashes are verified
- [ ] Unauthorized changed paths are all named and produce BLOCKED
- [ ] Reviewer never hides, repairs, normalizes, or reverts a mutation

### Case 3: Inferred prose is not a requirement

Fixture: A GDD sentence implies a technical constraint but lacks stable ID,
source-bound lifecycle, current owner approval, or explicit classification.

Assertions:

- [ ] Sentence is excluded from admitted baseline
- [ ] Stable CANDIDATE_REQUIREMENT finding cites exact path/hash/location and
      missing fields
- [ ] No ID is allocated/reused and registry remains byte-identical
- [ ] Verdict is PARTIAL when no independent blocker exists

### Case 4: Implicit ADR link and discovered test are unverified

Fixture: ADR discusses the same topic without the exact requirement ID; story
names a test path; test source exists; no authoritative current run exists.

Input: `$architecture-review rtm`

Assertions:

- [ ] ADR is UNVERIFIED_LINK, not VERIFIED_COVERED
- [ ] Test is DISCOVERED_NOT_EXECUTED, not EXECUTED_PASS
- [ ] Derived index or filename cannot fill either link
- [ ] Verdict is PARTIAL, never PASS

### Case 5: Test-run evidence truth table

Use otherwise current RTM fixtures:

- exact current passing run → EXECUTED_PASS and may contribute to PASS;
- old test/revision/manifest/link-set pass → STALE_RUN and PARTIAL;
- current authoritative fail → EXECUTED_FAIL and BLOCKED;
- test source without run → DISCOVERED_NOT_EXECUTED and PARTIAL;
- explicitly approved not-required evidence → NOT_APPLICABLE.

Assertions:

- [ ] Run ID, result, timestamp, exact test hash, linked IDs, and target revision
      or manifest are mandatory
- [ ] Absence never becomes NOT_APPLICABLE without explicit current contract
- [ ] Only EXECUTED_PASS counts as passing

### Case 6: Prior-report staleness and accepted risk

Fixture: A report for H1 is identified by exact path/record ID; one target,
scope, mode, or ruleset hash changes to H2. Separately test current, expired,
stale, and unbound accepted-risk records.

Assertions:

- [ ] Any identity/scope/hash change marks prior report STALE
- [ ] Prior verdict and report bytes remain unchanged
- [ ] Risk validates report/finding IDs, exact scope/manifest, owner/signature,
      timestamp, and expiry separately
- [ ] Risk never changes BLOCKED/PARTIAL to PASS or closes a finding

### Case 7: Invalid invocation produces no verdict

Fixture: Unknown/duplicate/extra mode; missing/duplicate selector; title/fuzzy
target; absolute/traversal/external path; unknown/ambiguous stable ID.

Assertions:

- [ ] Exact invalid token/target and accepted grammar are returned
- [ ] Output is ERROR with no PASS/BLOCKED/PARTIAL
- [ ] No inventory expansion, worker, report, or mutation occurs

### Case 8: Architecture document template review remains separate

Fixture: Caller asks for approval solely because `architecture.md` has eight
sections.

Assertions:

- [ ] Section count is not architecture traceability evidence
- [ ] No APPROVED / NEEDS REVISION / MAJOR ISSUES verdict is emitted
- [ ] Derived architecture cannot override GDD/TR/ADR sources
- [ ] No file changes

### Case 9: Large target remains bounded (ARR-006)

Fixture: 40 GDD/TR/ADR/story/test artifacts, 300 index records, and 140 explicit
typed edges spanning multiple decision domains; every individual file fits the
byte limit.

Assertions:

- [ ] Artifacts/index records/groups/edges sort deterministically into shards
- [ ] No shard exceeds 12 artifacts, 96 records, 48 edges, or 262144 input bytes
- [ ] No worker receives the whole target; shards run in bounded batches
- [ ] Mutation tree hashes at most 256 paths per streaming batch without loading
      file content into review context
- [ ] Every intended artifact/record/group/edge/check maps to coverage
- [ ] Oversized single file or uncompleted shard yields PARTIAL with exact
      unchecked scope, not a widened limit

### Case 10: Strict mode isolation (ARR-007)

Run golden fixtures for each mode:

- `full`: coverage + keyed consistency/dependencies + engine + contract-required
  RTM; TD and LP reviewers
- `coverage`: requirement admission and Requirement→ADR only; no engine,
  conflicts, stories/tests/runs, or reviewers
- `consistency`: current ADR keyed conflicts/dependencies only; TD reviewer
- `engine`: explicit ADR engine claims and pinned references only; matching
  engine specialist
- `single-gdd`: exact target admission/coverage only; no neighboring/fuzzy
  expansion or reviewers
- `rtm`: coverage plus contract-required Story→Test→Run; LP and QA reviewers

Assertions:

- [ ] Forbidden phases do not discover/read/delegate/emit findings
- [ ] Forbidden rows are NOT_APPLICABLE, not missing coverage
- [ ] No mode silently expands to full
- [ ] Every reviewer plan matches exactly and never exceeds two

### Case 11: Systems lifecycle remains recorder-owned (ARR-008)

Fixture: Systems index contains valid enum states; another fixture contains an
invalid historical value. Review produces findings requiring follow-up.

Assertions:

- [ ] Systems index bytes remain identical in every outcome
- [ ] Reviewer never writes or proposes `Needs Revision`
- [ ] Finding names the actual recorder/owner and objective evidence required,
      not a lifecycle transition command
- [ ] Optional report remains the sole authorized write

### Case 12: Reviewer failure and contradiction protocol (ARR-009)

Fixture: For each required reviewer exercise DONE, DECLINED, TIMEOUT, ERROR,
wrong manifest, omitted check, and same-fingerprint contradictory evidence.

Assertions:

- [ ] Every result validates as `cgs.architecture-review-worker/v1`
- [ ] Two-role profiles start in parallel and all profiles cap at two
- [ ] Any required non-DONE/mismatch/unchecked result prevents PASS and produces
      PARTIAL absent an independent blocker
- [ ] Identical fingerprints deduplicate with all provenance
- [ ] Contradictory same-fingerprint evidence becomes EVIDENCE_CONFLICT and
      PARTIAL, never majority vote
- [ ] Reviewer never emits/overrides the gate verdict

### Case 13: Deterministic blocker and PASS matrix (ARR-010)

Exercise independently:

- explicitly critical/Foundation/Core admitted requirement with no ADR → BLOCKED;
- unclassified/noncritical missing ADR → PARTIAL;
- current conflicting accepted ADRs or dependency cycle → BLOCKED;
- unknown dependency identity/applicability or stale ADR → PARTIAL;
- pinned evidence proves current engine incompatibility → BLOCKED;
- missing/stale engine reference → PARTIAL;
- current required EXECUTED_FAIL → BLOCKED;
- stale/missing required run → PARTIAL.

Assertions:

- [ ] Every blocker satisfies all current authority/scope/lifecycle/hash proof
      conditions
- [ ] Foundation/Core/required ADR is never inferred from prose
- [ ] Unknown/stale/unchecked evidence cannot PASS and cannot be guessed into a
      blocker
- [ ] Precedence is ERROR(no verdict) → confirmed BLOCKED → PARTIAL → PASS

### Case 14: Source authority and derived drift (ARR-011)

Fixture: Create GDD-vs-registry, GDD-vs-ADR, ADR-vs-architecture, ADR-vs-story,
test-source-vs-run, and ADR-vs-engine-reference disagreements.

Assertions:

- [ ] GDD owns product rule; registry drift does not rewrite either source
- [ ] ADR owns technical decision only within approved GDD/TR boundary
- [ ] Architecture/traceability indexes are derived and never fill source links
- [ ] Story is implementation evidence, not decision authority
- [ ] Test run owns execution result for exact target
- [ ] Pinned reference owns compatibility fact, not product/architecture choice
- [ ] Ambiguous cross-owner scope is PARTIAL; reproducible current contradiction
      uses blocker proof

### Case 15: Unique report identity and exact selection (ARR-012)

Fixture: Multiple reports are produced in one day and second; duplicate dates,
multiple matching record IDs, stale index entries, and changed inputs exist.

Assertions:

- [ ] Run/path use fractional UTC, manifest prefix, and one preserved UUID and
      cannot overwrite
- [ ] Prior evidence is selected only by exact path or unique exact record ID
- [ ] Review index resolution verifies indexed path/record hash/project/mode/
      target/manifest before use
- [ ] Filename date, mtime, directory order, and vague latest are forbidden
- [ ] Any target-manifest or stale-key change removes gate currency

### Case 16: Exact single-GDD identity (ARR-013)

Fixture: A canonical path and stable systems-index ID resolve to one GDD; other
fixtures use duplicate titles, duplicate/colliding IDs, ID/path disagreement,
missing target, and outside-project path.

Assertions:

- [ ] Canonical path and unique stable ID select the same exact target
- [ ] `id:` resolution hashes and records the systems index as an input; a path
      selector does not silently depend on an unrecorded index
- [ ] Title/system-name search is never performed
- [ ] Zero/multiple/collision/disagreement returns ERROR with no verdict
- [ ] Only IDs appearing verbatim in that target and ADRs explicitly naming them
      enter scope

### Case 17: Empty, missing, and NOT_APPLICABLE states (ARR-014)

Exercise every ruleset empty-set row.

Assertions:

- [ ] No primary mode target returns ERROR without a gate verdict
- [ ] Readable GDD but no admissible requirements returns PARTIAL
- [ ] Explicit critical gap returns BLOCKED; noncritical/unknown gap returns
      PARTIAL
- [ ] Consistency with fewer than two ADRs returns PARTIAL
- [ ] Engine without pinned required evidence returns PARTIAL
- [ ] Missing required RTM evidence returns PARTIAL; explicit not-required
      contract returns NOT_APPLICABLE
- [ ] Optional missing derived architecture/index is disclosed without penalty
- [ ] Every class records applicability, presence, currentness, and reason

### Case 18: Mode golden fixtures and catalog contract (ARR-015)

Maintain one passing, one partial/error, and where applicable one blocked fixture
for every public mode. Check implementation, metadata, this catalog-resolved
spec, report schemas, and path contract together.

Assertions:

- [ ] Catalog entry resolves exactly to this spec path
- [ ] Metadata names bounded hash-bound traceability, read-only surface, and
      PASS/BLOCKED/PARTIAL semantics
- [ ] Each mode's accepted syntax, allowed inputs, forbidden phases, reviewers,
      output schema, and verdict match across all owned files
- [ ] Golden fixtures cover mutation guard and exact trace/test evidence
- [ ] Catalog execution-result fields are updated only by the separate catalog
      test recorder, not by this reviewer

### Case 19: Machine review-evidence round trip

Fixture: Report includes present/missing/N/A classes, shards, reviewers,
candidate/unverified requirements, traceability, test states, blocker/incomplete
reasons, stable findings, and a risk reference.

Assertions:

- [ ] First fenced block parses as `cgs.review-evidence/v1`
- [ ] Generic fields contain canonical record ID, artifact ID, complete artifact
      set, reviewer, verdict, timestamp, finding IDs, and producer version
- [ ] Extension parses as `cgs.architecture-review/v2` with exact target,
      ruleset/skill hashes, manifest/stale identity, limits, classes, coverage,
      reviewers, baseline, traceability, test evidence, findings, reasons,
      mutation guard, and risk references
- [ ] Canonical record ID reproduces after omitting record_id and sorting the
      specified keys/arrays
- [ ] Stable finding ID changes only when rule/target/evidence identity changes
- [ ] Human projection equals machine evidence

### Case 20: Partial preservation with an independent blocker

Fixture: One bounded shard proves a current dependency cycle while another
shard times out and an optional derived index is missing.

Assertions:

- [ ] Proven blocker and incomplete scope are both preserved
- [ ] Verdict is BLOCKED because blocker proof is independent and complete
- [ ] Incomplete reason codes remain visible; they are not discarded
- [ ] If blocker evidence itself is incomplete, verdict is PARTIAL instead
- [ ] PASS is impossible in both variants

---

## Protocol Compliance

- [ ] Inventory is mode-bounded and all excluded classes are explicit
- [ ] Full reads and reviewer prompts obey artifact/record/edge/byte limits
- [ ] Exact source authority and current hashes precede conclusions
- [ ] Only explicit approved IDs enter the baseline
- [ ] Exact links and actual current run evidence are mandatory
- [ ] Reviewers are profile-driven, capped, read-only, and non-authoritative
- [ ] Confirmed blocker → BLOCKED; otherwise incomplete evidence → PARTIAL;
      otherwise complete current evidence → PASS
- [ ] Mutation guard runs in bounded batches immediately before return
- [ ] Generic evidence and extension are canonical, immutable, and stale-aware
- [ ] Default execution changes zero files; optional save creates only one report
- [ ] One owner-directed handoff is returned and not invoked

---

## Coverage Notes

- Cases 1–8 preserve P0 read-only, explicit requirement/link/run evidence,
  staleness, risk separation, mutation guard, and document-review boundary.
- Case 9 closes ARR-006.
- Case 10 closes ARR-007.
- Case 11 closes ARR-008.
- Case 12 closes ARR-009.
- Case 13 closes ARR-010.
- Case 14 closes ARR-011.
- Case 15 closes ARR-012.
- Case 16 closes ARR-013.
- Case 17 closes ARR-014.
- Case 18 closes ARR-015.
- Cases 19–20 harden machine-consumption and mixed blocker/partial behavior.
