# Skill Test Spec: $scope-check

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

## Skill Summary

`$scope-check` is a strictly read-only comparator for one exact immutable approved
baseline and one exact current scope manifest. Inputs use `path@revision`; versioned
schemas and stable Scope IDs produce deterministic semantic deltas; independent
decision records determine whether additions/removals/modifications are allowed;
separate evidence receipts support effort/schedule/quality/integration statements.

Canonical results are `ERROR`, `INPUT REQUIRED`, `INSUFFICIENT EVIDENCE`,
`PARTIAL`, `NO SCOPE DELTA`, and `SCOPE DELTA FOUND`. None grants product,
schedule, quality, planning, gate, mutation, or re-baseline authority.

---

## Static Assertions

- [ ] Frontmatter contains exactly `name: scope-check` and a non-empty description
- [ ] `compare` and `inspect` require baseline/current
      `path`; inspect also requires one exact evidence
      identity
- [ ] `discover` and no-argument behavior cannot choose or compare active scope
- [ ] Baseline/current contracts require exact schema/artifact IDs/versions,
      revisions, parent/timebox, completeness, stable Scope IDs, and compatible
      normalization schema
- [ ] Baseline approval binds exact bytes to authorized product-owner authority,
      timestamp, and immutable signature/record revision
- [ ] Current scope comes only from the current manifest; Git/code/TODO/issue/
      build evidence cannot create scope or approval
- [ ] Delta and allowed classifications are exact enumerations with deterministic
      tables
- [ ] Stable Delta ID excludes source revisions, title, row/line, timestamps, decision,
      risk, and impact state
- [ ] Change decision, risk acceptance, and re-baseline use separate versioned
      authority schemas and never substitute for one another
- [ ] Fixed numeric bounds cover artifact bytes/entries/semantic bytes,
      allowlisted paths/bytes/commits, decisions/risks/receipts, dependency edges,
      test mappings, and revalidate batches
- [ ] Effort interval, schedule, quality, and integration algorithms are explicit;
      no item-count percentage, intuitive Low/Medium/High, or overall risk score
- [ ] Result precedence uses exactly the six canonical values
- [ ] Output is `cgs.review-evidence/v1` plus `cgs.scope-check/v2`, exact-revision
      bound, `NOT_PERSISTED`, gate-ineligible, and READ_ONLY
- [ ] Skill never recommends/chooses/applies Cut/Keep/Defer, invokes another
      workflow, mutates planning/Git/session state, or silently re-baselines
- [ ] Metadata fully describes immutable pair, stable IDs, bounded evidence,
      change/risk separation, and read-only behavior without truncation

---

## Director Gate Checks

None. Scope comparison is read-only and has no product decision authority. No
agent, planner, producer, estimator, or gate is invoked.

---

## Test Cases

### Case 1: Exact equal semantics produce NO SCOPE DELTA

Fixture: Exact baseline/current path@revision inputs have compatible schemas, current
links the exact approved baseline, stable IDs/semantic revisions are identical, and
only ordering/Markdown formatting differs.

Assertions:

- [ ] Exact paths, byte lengths, revision, IDs, versions, revisions, parent/timebox,
      approval, completeness, and normalizer are reported
- [ ] Presentation changes create no delta
- [ ] Result is `NO SCOPE DELTA`
- [ ] Result explicitly grants no schedule/quality/product permission

---

### Case 2: Bare baseline path never identifies immutable bytes

Input: `$scope-check compare --baseline plans/m3.md --current plans/current.md`

Assertions:

- [ ] Returns `ERROR` for invalid exact identity syntax
- [ ] Does not revision/select the bare path and continue implicitly
- [ ] No similarly named/newer baseline is considered
- [ ] No comparison verdict is emitted

---

### Case 3: Validate, approval, and ambiguity fail closed

Variants: invocation revision mismatch; two approval records; missing approver
authority; baseline internal ID/version differs; current references another
baseline revision; identical aliased pair paths.

Assertions:

- [ ] Syntax/path alias failures are `ERROR`
- [ ] Identity/approval/linkage failures are `INSUFFICIENT EVIDENCE`
- [ ] No file is chosen by similarity, modification time, or active label
- [ ] Actual/expected identities and safe remediation are exact

---

### Case 4: Story/epic/sprint input needs explicit companion manifest

Fixture: A story points to one exact companion current manifest and approved epic
baseline; a similarly named milestone also exists.

Assertions:

- [ ] Only exact path@revision links are followed
- [ ] Parent/timebox and baseline identities must match
- [ ] Similar milestone is ignored
- [ ] Missing/ambiguous companion link is `INSUFFICIENT EVIDENCE`

---

### Case 5: Current manifest is the only current-scope authority

Fixture: Current manifest has stable IDs A/B; Git contains feature C, code contains
D, and issue tracker/TODO mentions E.

Assertions:

- [ ] Current scope set is exactly A/B
- [ ] C/D/E do not become additions/removals/modifications
- [ ] Compare mode does not scan Git/code/issues/TODOs
- [ ] Evidence cannot silently amend current scope

---

### Case 6: Allowlisted Git/code evidence proves activity only

Fixture: Inspect evidence manifest allowlists exact commit and code paths/revisions
for delta A.

Assertions:

- [ ] Evidence is labeled implementation activity
- [ ] Commit author is not a product decision owner
- [ ] Activity cannot create Scope ID, approval, justification, estimate, or risk
      acceptance
- [ ] Non-allowlisted neighboring history/files are not read

---

### Case 7: Silent deletion is conflict, not an inferred removal

Fixture: Baseline contains Scope ID X; current omits X and has no explicit removal
row or decision link.

Assertions:

- [ ] X is `CONFLICT`, not a clean `REMOVED`
- [ ] No intent/owner is inferred
- [ ] Complete result is blocked by `INSUFFICIENT EVIDENCE`
- [ ] Adding an exact explicit removal row permits deterministic removal analysis

---

### Case 8: Approved change requires an exact final decision record

Fixture: Inspect evidence allowlists one final `cgs.scope-change-decision/v1`
record for addition A, binding
operation, Scope/Delta IDs, exact pair/entry revisions, parent/timebox, authorized
owner/authority, rationale, timestamp, signature, and no conflict.

Assertions:

- [ ] Authority is `APPROVED_CHANGE`
- [ ] Allowed classification is `ALLOWED_ADDITION`
- [ ] Authorized delta still yields `SCOPE DELTA FOUND`
- [ ] Approval does not prove low effort/risk or re-baseline

---

### Case 9: Prose and implementer identity cannot justify change

Variants: Git author plus prose; issue assignee; file owner; agent recommendation;
chat acknowledgment; external linked decision unavailable to compare; owner
without authority record; proposed decision.

Assertions:

- [ ] States include `NO_RECORD`, `UNVERIFIED_RECORD`, `UNAUTHORIZED_RECORD`, or
      `PROPOSED_CHANGE` as applicable
- [ ] None is `APPROVED_CHANGE`
- [ ] Added/removed/modified classification remains unapproved
- [ ] No person/justification is inferred from Git metadata

---

### Case 10: Allowed-state matrix is exhaustive

Fixtures cover unchanged, approved/unapproved added, approved/unapproved removed,
approved/unapproved modified, unmapped/conflict, and conflicting decision records.

Assertions:

- [ ] Results map exactly to ALLOWED_UNCHANGED/ADDITION/REMOVAL/MODIFICATION,
      UNAPPROVED_ADDITION/REMOVAL/MODIFICATION, or CONFLICT
- [ ] Authority and delta type remain separately visible
- [ ] Risk state never changes this mapping
- [ ] Same immutable inputs reproduce identical classifications

---

### Case 11: Accepted scope change and accepted risk are separate

Fixture: Delta A has approved change but no risk record; delta B has valid accepted
schedule risk but no approved change.

Assertions:

- [ ] A is allowed with risk state NO_RECORD
- [ ] B remains an unapproved scope change despite risk reference
- [ ] Risk reference changes no impact evidence state
- [ ] Comparator creates/applies neither record

---

### Case 12: Invalid risk acceptance is rejected

Variants: expired, unsigned, wrong Delta/Scope ID, wrong pair/evidence revision,
unverifiable owner authority, self-authored model/agent record, missing controls.

Assertions:

- [ ] Each has a deterministic invalid reason
- [ ] Delta/authority/allowed/impact/result remain unchanged
- [ ] Audit never renews or signs a record
- [ ] Ordinary acknowledgment is not accepted risk

---

### Case 13: Effort delta uses compatible interval arithmetic

Fixture: All changed IDs have exact pair-bound estimates in the same calibrated
unit/method/confidence policy; variant mixes units and omits one estimate.

Assertions:

- [ ] Complete variant computes `[C_low-B_high, C_high-B_low]` and aggregates
      compatible intervals only
- [ ] Mixed/incomplete variant is `Effort Delta: UNVERIFIED`
- [ ] No conversion, item-count proxy, or percentage growth is emitted
- [ ] Effort changes no delta/authority/result state

---

### Case 14: Schedule exposure uses interval comparison

Fixtures: effort upper ≤ capacity lower; effort lower > capacity upper; intervals
overlap; stale/missing capacity; zero changed IDs.

Assertions:

- [ ] States are respectively SUPPORTED_NO_EXPOSURE, SUPPORTED_EXPOSURE,
      INDETERMINATE, UNVERIFIED, and NOT_APPLICABLE
- [ ] Units/method/pair/evidence revisions must match
- [ ] No Low/Medium/High or intuitive schedule score appears
- [ ] Accepted risk reference cannot change the state

---

### Case 15: Quality exposure uses changed acceptance denominator

Fixtures: every changed acceptance ID mapped/current; complete evidence proves one
missing mapping; complete conflicting sufficiency; incomplete denominator; no
acceptance change.

Assertions:

- [ ] States follow the five-state quality algorithm exactly
- [ ] Header/test-file existence alone is not coverage
- [ ] Denominator and mapping rows are stable-ID/revision-bound
- [ ] Zero denominator is NOT_APPLICABLE, not 100%

---

### Case 16: Integration exposure uses exact dependency/interface graphs

Fixtures: no changed edges; all changed edges have owner/contract/consumer/test;
complete evidence proves broken edge; graphs conflict; graph missing; no
dependency-bearing change.

Assertions:

- [ ] States follow the five-state integration algorithm exactly
- [ ] Commit/code prose does not substitute for graph/contract evidence
- [ ] Dependency edge budget/unchecked rows are explicit
- [ ] No combined overall risk rating is produced

---

### Case 17: No arguments and discover require confirmation

Fixture: Active state has one candidate pair, then multiple candidate pairs.

Assertions:

- [ ] No arguments returns `INPUT REQUIRED`
- [ ] `discover` lists exact path@revision identities only and returns INPUT REQUIRED
- [ ] Even one pair is not analyzed in the same invocation
- [ ] Multiple candidates are never ranked or auto-selected

---

### Case 18: Error, insufficient, and partial are distinct

Variants: invalid syntax/path/schema; stale/missing core approval/link/ID; valid
core pair with declared inspect evidence revision mismatch/unsupported/overflow.

Assertions:

- [ ] Results are respectively ERROR, INSUFFICIENT EVIDENCE, and PARTIAL
- [ ] Partial preserves valid stable core deltas
- [ ] Missing evidence cannot yield NO SCOPE DELTA
- [ ] Exact blocked conclusions and unchecked identities are shown

---

### Case 19: Evidence manifest is a closed exact allowlist

Fixture: Valid evidence manifest binds exact pair and includes exact path@revision/
purpose/source IDs plus exact Git IDs; neighboring relevant files also exist.

Assertions:

- [ ] Only allowlisted exact identities are read
- [ ] Globs/directories/fuzzy hints are invalid
- [ ] Neighboring files/history are ignored
- [ ] Git evidence remains implementation-only

---

### Case 20: Evidence budgets fail visibly

Variants exceed 40 paths, 2 MiB, 100 commits, 256 decisions/risks/receipts, or
4096 edges/test mappings.

Assertions:

- [ ] Effective limit is min(declared, fixed)
- [ ] Every discoverable overflow identity is `UNCHECKED_LIMIT`
- [ ] Inspect result is PARTIAL and dependent impacts are UNVERIFIED
- [ ] No denominator shrinks or read silently truncates

---

### Case 21: Core entry/byte overflow cannot look healthy

Fixtures exceed per-artifact bytes, 4096 Scope IDs, or semantic byte budget.

Assertions:

- [ ] Identity impossible to establish is INSUFFICIENT EVIDENCE
- [ ] Meaningful bounded subset plus unchecked entries is PARTIAL
- [ ] No complete NO SCOPE DELTA/SCOPE DELTA FOUND is emitted
- [ ] Every unchecked Scope ID/count is explicit

---

### Case 22: Repeated checks retain immutable baseline identity

Fixture: Run 1 uses baseline B/v3/H1 and current C1; later plan path bytes become
H2 without re-baseline; Run 2 still supplies exact H1 bytes; Run 3 supplies path
with H2 while current still cites H1.

Assertions:

- [ ] Run 2 reproduces comparison against B/v3/H1
- [ ] Run 3 is INSUFFICIENT EVIDENCE — BASELINE MISMATCH
- [ ] Edited/newer plan is never substituted
- [ ] Prior “improvement” or cuts do not alter baseline identity

---

### Case 23: Re-baseline requires a separate authorized record

Variants: valid `cgs.scope-rebaseline/v1`; proposed record; edited plan; newer
modification time; prior scope-check result.

Assertions:

- [ ] Only valid record can support a future new baseline input/version
- [ ] Current run never creates/applies the record
- [ ] Other variants do not re-baseline
- [ ] Comparing new baseline is a new exact comparison identity

---

### Case 24: Input changes during check invalidate the right layer

Variants: baseline/current changes; approval/normalizer changes; optional estimate/
decision/risk/test evidence changes.

Assertions:

- [ ] Core change discards deltas and yields INSUFFICIENT EVIDENCE
- [ ] Approval/normalizer change invalidates core identity
- [ ] Optional evidence change preserves core deltas but yields PARTIAL
- [ ] revalidate processing uses batches of at most 64 paths without dropping inputs
- [ ] No changed input is repaired, restored, or adopted

---

### Case 25: Stable Delta IDs survive unrelated byte changes

Fixture: Same baseline ID/version, parent, Scope ID, and MODIFIED delta remains
while presentation/current revision/line/title/decision/risk/impact changes.

Assertions:

- [ ] finding key and Delta ID remain stable
- [ ] Exact artifact/entry revisions expose current staleness separately
- [ ] Changing delta type or baseline version creates a new identity
- [ ] Two identical immutable runs sort/output the same deltas

---

### Case 26: One large item, ten small items, and row splits are not magnitude

Fixture: One network subsystem addition; ten text additions; presentation-only
row split/merge; no compatible estimates.

Assertions:

- [ ] Each actual stable-ID change is classified without relative magnitude claim
- [ ] Row split/merge with equal stable semantic revisions is unchanged
- [ ] Effort remains UNVERIFIED
- [ ] No bloat/creep/item-count/file-count percentage verdict appears

---

### Case 27: Canonical result precedence is deterministic

Fixtures cover syntax error, discovery, stale core identity, partial evidence,
complete equal semantics, complete authorized delta, complete unapproved delta,
and unmapped/conflict.

Assertions:

- [ ] Results are ERROR, INPUT REQUIRED, INSUFFICIENT EVIDENCE, PARTIAL,
      NO SCOPE DELTA, SCOPE DELTA FOUND, SCOPE DELTA FOUND, and INSUFFICIENT
      EVIDENCE respectively
- [ ] Authorized versus unapproved classification never changes delta result
- [ ] Result vocabulary contains no PASS/FAIL/creep verdict
- [ ] Missing evidence never produces a healthy conclusion

---

### Case 28: Output is read-only evidence with neutral options

Fixture: Inspect finds approved addition, unapproved removal, valid and invalid
risk refs, partial impact evidence, and unchanged input revisions.

Assertions:

- [ ] Generic envelope and v2 extension contain exact identities, normalizer,
      deltas, authority/allowed/risk/impact, coverage, unchecked, revalidate,
      comparison/stale keys, result, and producer version
- [ ] `NOT_PERSISTED`, gate-ineligible, and READ_ONLY are explicit
- [ ] Two or three options are unranked and name Scope/Delta IDs, unknowns,
      decision owner/action, and separate transaction
- [ ] Skill never recommends/chooses Cut/Keep/Defer, delegates, writes, mutates
      Git/session/plans, or starts re-baselining

---

## Protocol Compliance

- [ ] Reads only exact immutable pair plus validated evidence allowlist
- [ ] Scope and semantic identity use stable IDs/versioned normalizer, not fuzzy
      text or counts
- [ ] Every delta binds both artifact/entry revisions while retaining stable identity
- [ ] Added/removed/modified and allowed/unapproved/conflict classifications are
      deterministic and separate
- [ ] Change, risk, and re-baseline authority are distinct and independently
      verified
- [ ] Impact statements use exact receipts and fixed algorithms or UNVERIFIED
- [ ] Budget/revalidate gaps are explicit and fail closed
- [ ] Result follows the canonical six-state precedence
- [ ] Output is revision-bound, non-persisted, gate-ineligible, and strictly read-only
- [ ] Product decisions and mutations remain with authorized external owners

---

## Coverage Notes

- SCP-004: Cases 1–4.
- SCP-005: Cases 5–7.
- SCP-006: Cases 8–10.
- SCP-007: Cases 11–16.
- SCP-008: Cases 17–18 and 27.
- SCP-009: Cases 19–21.
- SCP-010: Cases 22–24.

Cases 25–28 additionally verify stable findings, count-independent semantics,
deterministic results, exact revalidate, neutral ownership, and read-only evidence.
