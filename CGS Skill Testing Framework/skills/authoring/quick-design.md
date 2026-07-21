# Skill Test Spec: $quick-design

## Skill Summary

`$quick-design` creates one immutable design-change proposal for a structurally
low-risk delta against an exact current GDD hash. It does not use estimated effort
as a quality-gate shortcut and does not edit authoritative design, data, registry,
story, review, lifecycle, test, or implementation artifacts. Application,
independent hash-bound review, and lifecycle recording are separate tasks.
Production implementation eligibility exists only for an explicitly supplied,
valid, APPLIED and CURRENT lifecycle record.

---

## Static Assertions (Structural)

- [ ] QDS-S001: Frontmatter contains only `name` and non-empty `description`;
  `name` is `quick-design`.
- [ ] QDS-S002: Invocation exposes explicit `propose` and read-only `status`
  modes.
- [ ] QDS-S003: The canonical proposal path is exactly
  `design/quick-specs/<change-id>/<version>/proposal.md`.
- [ ] QDS-S004: Existing proposals are immutable; PATH EXISTS requires a new
  version and no in-place update.
- [ ] QDS-S005: Scope eligibility is determined by an evidence-backed structural
  risk table, not hours or days.
- [ ] QDS-S006: A new system/state owner, cross-system contract, player-facing
  core rule, formula-semantic change, outside-range tuning, or other listed
  structural risk redirects.
- [ ] QDS-S007: UNKNOWN risk evidence blocks rather than defaulting to low risk.
- [ ] QDS-S008: Proposal author, application author, independent reviewer, and
  lifecycle recorder have explicit, separated responsibilities.
- [ ] QDS-S009: The only `quick-design propose` write is `proposal.md`; GDD,
  data, index, story, review, lifecycle, source, and test files are non-writes.
- [ ] QDS-S010: User draft approval authorizes proposal content/write only and is
  explicitly not formal review or implementation approval.
- [ ] QDS-S011: Proposal schema includes stable change/version IDs, Status
  PROPOSED, exact target/base/section/source hashes, author task ID, risk
  evidence/profile, and Implementation Eligible NO.
- [ ] QDS-S012: Proposal sections are exactly Product Decision, Base Snapshot,
  Structural Risk Evidence, Proposed Delta, Observable Acceptance Conditions,
  Apply Review and Record Handoff, and Boundaries.
- [ ] QDS-S013: APPLIED requires an application receipt, unchanged updated GDD
  hash, formal independent APPROVED review at required depth, and a separate
  recorder.
- [ ] QDS-S014: PROPOSED, SUPERSEDED, stale, invalid, experiment-only,
  advisory-reviewed, and unrecorded proposals are not implementation-eligible.
- [ ] QDS-S015: Lifecycle records use explicit paths/hashes and append-only
  predecessor binding; no latest/mtime selection.
- [ ] QDS-S016: Workflow Status, Proposal Status, Currentness, Implementation
  Eligible, Persistence, and Verdict are independent axes.
- [ ] QDS-S017: A production story must reference the updated authoritative GDD
  path/hash and exact APPLIED record; the proposal is rationale only.
- [ ] QDS-S018: Metadata describes the hash-bound proposal boundary without
  claiming direct implementation readiness.

---

### Case 1: In-range tuning creates only a PROPOSED artifact

**Fixture:**

- `design/gdd/movement.md` is a valid current system GDD with stable system ID.
- Its Tuning Knobs section documents `jump_height` range 4.0–7.0 and current
  default 5.0.
- Exact current GDD and section hashes are known.
- Current systems-index ownership is unambiguous and hashable.
- All structural risk rows are proven NO.
- `design/quick-specs/QD-jump-height/v001/proposal.md` does not exist.

**Input:**

`$quick-design propose "change jump_height default to 6.0" --change-id QD-jump-height --version v001 --target design/gdd/movement.md --expect-base <current-sha256>`

**Expected writes:**

- Exactly `design/quick-specs/QD-jump-height/v001/proposal.md` after product
  content approval and bounded write authorization.

**Expected non-writes:**

- `design/gdd/movement.md`, `assets/data/**`,
  `design/gdd/systems-index.md`, stories, review/lifecycle records, `src/**`,
  `tests/**`, and session state.

**Expected behavior:**

1. Verifies the exact target and source hashes without choosing by relevance or
   mtime.
2. Shows all-NO structural risk evidence and selects `QD-TUNING`.
3. Requires formal later review depth `lean` or `full`.
4. Writes and re-reads one immutable proposal with `Status: PROPOSED`,
   `Implementation Eligible: NO`, and all seven required sections.
5. Returns `Workflow Status: COMPLETE`, `Proposal Status: PROPOSED`,
   `Currentness: CURRENT`, `Persistence: VERIFIED`, and
   `Verdict: PROPOSAL_CREATED`.
6. Stops before authoritative application, review, recording, or implementation.

**Assertions:**

- [ ] QDS-C01-A: No effort estimate participates in eligibility.
- [ ] QDS-C01-B: The proposal is bound to exact current target/section hashes.
- [ ] QDS-C01-C: Only the canonical proposal path is created.
- [ ] QDS-C01-D: A successful proposal is still implementation-ineligible.

---

### Case 2: Structural risk redirects regardless of effort or label

**Fixture:**

Run variants where the requested change:

- creates a new achievement system;
- adds a new combat state owner;
- changes a combat-to-inventory timing/ownership contract; or
- changes a player-facing progression core rule.

The user describes each as "tiny", estimates under one hour, or selects
"Tuning".

**Input:**

Run `propose` with an exact target and distinct unused IDs.

**Expected writes:**

- None.

**Expected non-writes:**

- No proposal, GDD, data, systems-index, review, lifecycle, story, or
  implementation file.

**Expected behavior:**

1. Records the objective risk fact as YES with evidence.
2. Does not allow label selection or estimated effort to override the fact.
3. Returns `Workflow Status: REDIRECTED`,
   `Proposal Status: NOT_CREATED`, `Implementation Eligible: NO`,
   `Verdict: REDIRECTED`, and next owner `$design-system`.
4. Stops before drafting or asking for proposal write authorization.

**Assertions:**

- [ ] QDS-C02-A: Every prohibited structural risk fails closed.
- [ ] QDS-C02-B: "New Small System" is never a quick profile.
- [ ] QDS-C02-C: User classification cannot downgrade evidence-backed risk.
- [ ] QDS-C02-D: Redirection creates no shadow proposal.

---

### Case 3: Proposal approval cannot authorize GDD edits or implementation

**Fixture:**

- A valid `QD-LOCAL` draft proposes a bounded rule clarification.
- The user approves the draft and says, "apply it to the GDD and implement it
  now."
- The current task is the proposal-author task.

**Input:**

Approve the proposed `proposal.md` changeset.

**Expected writes:**

- Only the authorized canonical `proposal.md`.

**Expected non-writes:**

- Target GDD/checkpoint, data, systems index, story, review receipt, lifecycle
  record, code, tests, or implementation artifacts.

**Expected behavior:**

1. Treats approval as product-content and one-file persistence approval only.
2. Creates the PROPOSED artifact, if persistence was authorized.
3. Keeps the proposal operation's axes accurate and returns
   `Downstream Action: BLOCKED — SEPARATE APPLICATION AND REVIEW REQUIRED`
   for the request to apply/implement.
4. Provides separate application-author, independent-reviewer, and recorder
   handoffs, then stops.
5. Does not invoke the next workflow in the same task.

**Assertions:**

- [ ] QDS-C03-A: Proposal author never edits authoritative GDD/data/index.
- [ ] QDS-C03-B: User draft approval is not a formal review receipt.
- [ ] QDS-C03-C: No implementation begins before APPLIED/current evidence.
- [ ] QDS-C03-D: Author-review-record responsibilities remain separated.

---

### Case 4: PROPOSED cannot become a shadow implementation source

**Fixture:**

- A valid immutable proposal exists with `Status: PROPOSED`.
- The authoritative GDD still has the proposal's base hash.
- No lifecycle record is supplied.
- A story cites only the proposal path as its GDD Reference.

**Input:**

`$quick-design status design/quick-specs/QD-parry-window/v001/proposal.md`

**Expected writes:**

- None.

**Expected non-writes:**

- No proposal/status rewrite, story repair, GDD application, review, record, or
  implementation.

**Expected behavior:**

1. Re-hashes the proposal and current GDD.
2. Returns `Proposal Status: PROPOSED`, `Currentness: CURRENT`,
   `Implementation Eligible: NO`, and `Verdict: STATUS_REPORTED`.
3. Reports that the story's authoritative reference is inadequate.
4. Requires an updated authoritative GDD plus exact APPLIED lifecycle record
   before implementation readiness can be evaluated.

**Assertions:**

- [ ] QDS-C04-A: PROPOSED never authorizes production implementation.
- [ ] QDS-C04-B: The proposal is rationale, not an authoritative GDD substitute.
- [ ] QDS-C04-C: Status mode is read-only.
- [ ] QDS-C04-D: Story handoff cannot bypass application/review/recording.

---

### Case 5: Stale base blocks before persistence

**Fixture:**

- The invocation supplies expected base hash A.
- The target GDD is changed to hash B before the proposal write preflight.
- The draft and risk analysis were based on A.
- The output path is unused.

**Input:**

Approve the draft for persistence.

**Expected writes:**

- None.

**Expected non-writes:**

- No proposal, GDD, data, index, review, record, story, or source write.

**Expected behavior:**

1. Re-reads all authoritative inputs immediately before writing.
2. Detects the target/section hash mismatch.
3. Returns `Workflow Status: ERROR`, `Proposal Status: NOT_CREATED`,
   `Currentness: STALE`, `Implementation Eligible: NO`,
   `Persistence: NOT_REQUESTED`, and `Reason: STALE BASE — REBASE REQUIRED`.
4. Does not silently update the draft or bind it to B.

**Assertions:**

- [ ] QDS-C05-A: Compare-and-set currentness is enforced.
- [ ] QDS-C05-B: Conversation memory is not hash evidence.
- [ ] QDS-C05-C: Stale proposal bytes are never written as current.

---

### Case 6: Existing path is immutable; revision creates a new version

**Fixture:**

- `design/quick-specs/QD-dash-window/v001/proposal.md` exists.
- Variant A requests `v001` again.
- Variant B requests `v002`, supplies the current GDD hash, and names the exact
  v001 path/hash in `--supersedes`.
- The current risk gate passes for Variant B.

**Input:**

Run both variants.

**Expected writes:**

- Variant A: none.
- Variant B: exactly the fresh
  `design/quick-specs/QD-dash-window/v002/proposal.md` after authorization.

**Expected non-writes:**

- No edit or overwrite of v001 and no mutable current-status pointer.

**Expected behavior:**

1. Variant A returns `ERROR — PATH EXISTS; CHOOSE A NEW VERSION`.
2. Variant B verifies the predecessor and rebases all target hashes.
3. v002 records the exact v001 path/hash in `Supersedes`.
4. Neither variant selects a version by date or mtime.

**Assertions:**

- [ ] QDS-C06-A: Same-day or repeated invocation cannot overwrite a proposal.
- [ ] QDS-C06-B: New versions are collision-free and explicitly chained.
- [ ] QDS-C06-C: Existing-file behavior matches the canonical contract.

---

### Case 7: Outside-range tuning redirects to full design

**Fixture:**

- Current GDD documents a tuning range of 4.0–7.0.
- The proposal requests value 9.0.
- No new state or cross-system interaction exists.

**Input:**

Run `propose` for the value 9.0.

**Expected writes:**

- None.

**Expected non-writes:**

- No proposal, GDD range edit, data edit, or implementation.

**Expected behavior:**

1. Records `Places tuning value outside documented current range: YES`.
2. Returns REDIRECTED and names `$design-system` as the authoring owner.
3. Does not accept rationale text as permission to extend the range.
4. Requires the range change to receive full authoritative authoring and review.

**Assertions:**

- [ ] QDS-C07-A: Outside-range values cannot use `QD-TUNING`.
- [ ] QDS-C07-B: Quick-design never edits the range or data directly.
- [ ] QDS-C07-C: Structural fact, not effort, controls redirection.

---

### Case 8: Self-review, stale review, or weak review cannot establish APPLIED currentness

**Fixture:**

Use an APPLIED lifecycle-record candidate with one invalid variant at a time:

- reviewer task ID equals proposal-author or application-author task ID;
- recorder task ID equals an author/reviewer task ID;
- review is `solo` / `ADVISORY REVIEW — NOT APPROVAL`;
- `QD-LOCAL` review depth is only `lean`;
- review verdict is not APPROVED;
- review targets the old GDD hash; or
- current GDD bytes changed after the review.

**Input:**

`$quick-design status <proposal-path> --record <applied-record-path>`

**Expected writes:**

- None.

**Expected non-writes:**

- No repair, re-review, record rewrite, GDD rollback, or implementation.

**Expected behavior:**

1. Re-hashes every explicit artifact and validates task-role separation.
2. Preserves the record's stated lifecycle status for audit but reports
   `Currentness: INVALID` or `STALE`.
3. Returns `Implementation Eligible: NO`.
4. Names the exact failed predicate and required fresh owner/review/record action.

**Assertions:**

- [ ] QDS-C08-A: Author cannot self-approve or self-record.
- [ ] QDS-C08-B: Review approval is bound to the current GDD hash.
- [ ] QDS-C08-C: Risk-profile review depth is enforced.
- [ ] QDS-C08-D: Status validation never mutates evidence.

---

### Case 9: Valid APPLIED and CURRENT evidence is recognized read-only

**Fixture:**

- Proposal is valid and hash-bound.
- A separately authorized application receipt binds its proposal hash, applied
  delta IDs, and exact pre/post GDD hashes.
- Current GDD bytes equal the post-application hash.
- Independent formal review is APPROVED for that exact GDD path/hash and meets
  the profile's required depth.
- Reviewer and recorder task IDs are independent from all author task IDs.
- A valid append-only APPLIED record binds every artifact and expected pre-state.

**Input:**

`$quick-design status <proposal-path> --record <applied-record-path>`

**Expected writes:**

- None.

**Expected non-writes:**

- No story, GDD, lifecycle, review, code, or test changes.

**Expected behavior:**

1. Revalidates the complete hash graph.
2. Returns `Workflow Status: COMPLETE`, `Proposal Status: APPLIED`,
   `Currentness: CURRENT`, `Implementation Eligible: YES`, and
   `Verdict: STATUS_REPORTED`.
3. Clarifies that implementation still requires a separate current
   `story-readiness` decision.
4. Requires stories to reference the authoritative updated GDD path/hash and
   exact APPLIED record, not the proposal alone.

**Assertions:**

- [ ] QDS-C09-A: Every APPLIED predicate is simultaneously satisfied.
- [ ] QDS-C09-B: Eligibility recognition is read-only.
- [ ] QDS-C09-C: Quick-design does not chain into implementation.

---

### Case 10: Experiment-only proposal cannot enter production

**Fixture:**

- Exact prototype scope exists under `prototypes/`.
- A low-risk temporary hypothesis is requested with `--experiment-only`.
- No production GDD mutation is authorized.

**Input:**

Run `propose` with an unused canonical proposal path and exact prototype scope.

**Expected writes:**

- Only the authorized proposal with `Target Use: EXPERIMENT_ONLY`.

**Expected non-writes:**

- Production GDD/data/story/code, lifecycle APPLIED record, review approval, or
  production implementation.

**Expected behavior:**

1. Writes `Status: PROPOSED`, the exact `Prototype Scope`,
   `Risk Profile: EXPERIMENT_ONLY`, `Required Review Depth: NOT_APPLICABLE`, and
   `Implementation Eligible: NO`.
2. States that APPLIED status is unavailable.
3. Provides only a prototype-validation handoff, not `story-readiness` or
   `dev-story`.

**Assertions:**

- [ ] QDS-C10-A: Experiment-only is visibly non-production.
- [ ] QDS-C10-B: It cannot become APPLIED or implementation-eligible.
- [ ] QDS-C10-C: Production artifacts remain untouched.

---

### Case 11: Authorization decline or persistence failure does not claim creation

**Fixture:**

- Draft, target, and risk evidence are valid.
- Variant A declines the one-file write.
- Variant B authorizes it but atomic persistence or byte verification fails.

**Input:**

Complete `propose` through the persistence decision.

**Expected writes:**

- Variant A: none.
- Variant B: no verified canonical proposal; temporary staging is not a result.

**Expected non-writes:**

- All authoritative and implementation artifacts remain untouched.

**Expected behavior:**

1. Variant A returns `COMPLETE / DRAFT / DRAFT_ONLY`,
   `Persistence: DECLINED`, and `Implementation Eligible: NO`.
2. Variant B returns `ERROR / NOT_CREATED / ERROR`,
   `Persistence: FAILED`, and `Implementation Eligible: NO`.
3. Neither response claims `PROPOSAL_CREATED` or an existing canonical path.

**Assertions:**

- [ ] QDS-C11-A: Content approval and filesystem persistence remain distinct.
- [ ] QDS-C11-B: Failed verification cannot produce a success verdict.
- [ ] QDS-C11-C: No partial write expands the authorization boundary.

---

## Cross-skill compatibility assertions

- [ ] QDS-X001: GDD mutation is handed to staged `design-system
  revise-section` with a separate authorization and author-only mutation scope.
- [ ] QDS-X002: Formal approval uses a fresh staged `design-review` task and is
  bound to the exact whole-GDD hash.
- [ ] QDS-X003: Solo/advisory review never satisfies formal approval.
- [ ] QDS-X004: Production stories must satisfy staged `story-readiness` using
  current authoritative-source traceability; a PROPOSED quick artifact is not a
  GDD.
- [ ] QDS-X005: Dependent-artifact propagation, when needed, remains a separate
  owner-authorized workflow and is never performed by quick-design.
- [ ] QDS-X006: The spec and metadata use the same proposal path, schema,
  lifecycle states, verdicts, and non-write boundary as the skill.
