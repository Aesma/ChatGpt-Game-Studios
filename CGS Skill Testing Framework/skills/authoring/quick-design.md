# Skill Test Spec: $quick-design

## Skill Summary

$quick-design creates one immutable cgs.quick-design-proposal/v2 artifact for an
evidence-proven low-structural-risk delta against explicit target, indexed owner,
sections, and current revisions, or for an isolated prototype hypothesis. It never
edits authoritative design/data/index/story/application/review/lifecycle/code/
test artifacts. Application, independent review, lifecycle recording, and
implementation are separate.

Production eligibility exists only in read-only status mode when an explicitly
supplied cgs.quick-design-lifecycle/v2 APPLIED record, application v1 receipt,
current GDD, and independent review evidence v1 all revalidate.

---

## Static Assertions

- [ ] QDS-S001: Frontmatter contains only name and non-empty description; name is quick-design
- [ ] QDS-S002: propose and read-only status forms are distinct
- [ ] QDS-S003: Production propose requires exact target, target ID, and one-or-more exact sections; it accepts no caller-supplied base token
- [ ] QDS-S003A: Stable section ID is SYS-id#canonical-heading-key and normalization collisions fail
- [ ] QDS-S004: Experiment form forbids production target/base arguments
- [ ] QDS-S005: Proposal ID is change-id@version and path is design/quick-specs/change-id/version/proposal.md
- [ ] QDS-S006: Created At UTC is RFC3339 seconds Z; path uniqueness never depends on date
- [ ] QDS-S007: Existing path uses atomic CREATE_IF_ABSENT and cannot be overwritten
- [ ] QDS-S008: Revisions require fresh version, exact predecessor, and current rebased evidence
- [ ] QDS-S009: Risk uses cgs.quick-design-risk/v2 with fixed IDs, YES/NO/UNKNOWN, owner, evidence, derivation, and reference ID
- [ ] QDS-S010: User label/effort cannot override a current risk fact
- [ ] QDS-S011: Any YES redirects and any UNKNOWN blocks before proposal creation
- [ ] QDS-S012: New system/owner/index row always redirects
- [ ] QDS-S013: Outside-range tuning redirects with owner/range/propagation handoff
- [ ] QDS-S014: QD-COSMETIC is restricted to presentation inside an existing indexed owner
- [ ] QDS-S015: QD-TUNING, QD-COSMETIC, QD-LOCAL, EXPERIMENT_ONLY have fact-derived review rules
- [ ] QDS-S016: Product, hard-evidence, derived, and technical decision classes match design-system P1
- [ ] QDS-S017: Every material delta references stable decision IDs and exact section revisions
- [ ] QDS-S018: Proposal contract is cgs.quick-design-proposal/v2 with exactly seven required sections
- [ ] QDS-S019: The only propose write is proposal.md; all authoritative and downstream artifacts are non-writes
- [ ] QDS-S020: Transaction preflight re-reads target, sections, index, dependencies, owner evidence, predecessor, and risk reference ID
- [ ] QDS-S021: Application evidence contract cgs.design-application/v1 binds pre/post revisions, delta IDs, patch/ranges, task, and payload
- [ ] QDS-S022: Re-review passes prior report plus application receipt as revision evidence
- [ ] QDS-S022A: Prior re-review report contract is cgs.design-review/v2
- [ ] QDS-S023: Review evidence contract cgs.review-evidence/v1 is independent/current/depth-bound
- [ ] QDS-S024: Lifecycle contract cgs.quick-design-lifecycle/v2 is append-only and explicit-path
- [ ] QDS-S025: APPLIED proposal is never reapplied; follow-up requires new superseding version
- [ ] QDS-S026: COMPLETE/PARTIAL/BLOCKED/REDIRECTED/ERROR have explicit precedence
- [ ] QDS-S027: Unsupported or unparseable input never returns COMPLETE or PROPOSAL_CREATED
- [ ] QDS-S028: Six status axes remain independent
- [ ] QDS-S029: Production story uses updated GDD plus current APPLIED record, proposal as rationale only
- [ ] QDS-S030: Metadata describes evidence-gated proposal boundary and no implementation readiness

---

## Behavioral Cases

### Case 1: in-range tuning creates one current PROPOSED artifact

**Fixture:**

- movement GDD is indexed exactly as SYS-movement.
- Tuning Knobs uniquely defines jump_height default 5.0, range 4.0–7.0, unit m.
- Target/index/section/dependency revisions are current.
- Risk rows QDR-001..009 are all NO.
- Canonical v001 path is absent.

**Input:**

    $quick-design propose "set jump_height to 6.0"
      --change-id QD-jump-height --version v001
      --target design/gdd/movement.md --target-id SYS-movement
      --section "Tuning Knobs"

**Expected behavior:**

1. Exact row, target, section, owner, and revisions are verified.
2. Risk contract/reference ID derives QD-TUNING; effort is non-gating.
3. Product owner selects 6.0 and QDD record binds source/range/decision.
4. Atomic create-if-absent writes one proposal v2 and verifies raw bytes.
5. Result is COMPLETE/PROPOSED/CURRENT/NO/VERIFIED/PROPOSAL_CREATED.

**Assertions:**

- [ ] QDS-C01-A: Only canonical proposal path is created
- [ ] QDS-C01-B: Proposal binds exact target/index/section/risk/decision evidence
- [ ] QDS-C01-C: Successful proposal remains implementation-ineligible

---

### Case 2: risk facts cannot be downgraded by label or effort

**Fixture:** variants add a state owner, cross-system timing contract,
player-facing core rule, formula semantic, or persistence/accessibility policy.
User calls each tiny, under one hour, cosmetic, or tuning.

**Expected behavior:**

1. Fixed risk row is YES with owner source and derivation.
2. User label and effort do not change result.
3. Workflow is REDIRECTED/NOT_CREATED/NOT_APPLICABLE/NO/NOT_REQUESTED/REDIRECTED.
4. No proposal/write authorization prompt occurs.

**Assertions:**

- [ ] QDS-C02-A: Structural facts, not classification preference, gate eligibility
- [ ] QDS-C02-B: Revised product idea triggers full risk re-evaluation
- [ ] QDS-C02-C: Redirect creates no shadow artifact

---

### Case 3: exact target, ID, and sections fail closed

**Fixture:** run variants with missing target ID, wrong index row, multiple rows,
fuzzy target request, absent/duplicate heading, unsupplied affected section,
unsupported document profile, directory, symlink, or non-UTF-readable bytes.

**Expected behavior:**

- Invalid/unsupported input returns ERROR/NOT_CREATED/INVALID.
- Missing or contradictory registration/ownership evidence returns BLOCKED with
  TARGET SYSTEM REGISTRATION REQUIRED or RISK EVIDENCE REQUIRED.
- No relevance search, filename matching, or most-recent selection occurs.

**Assertions:**

- [ ] QDS-C03-A: Target path and SYS ID resolve one exact index row
- [ ] QDS-C03-B: Every delta maps to a supplied unique section
- [ ] QDS-C03-C: Unsupported input cannot produce COMPLETE

---

### Case 4: same-day and concurrent proposal collisions cannot overwrite

**Fixture:**

- QD-dash-window/v001 already exists.
- Variant A requests v001 again.
- Variant B requests unused v002 with exact predecessor and current base.
- Variant C races another creator for the same unused v003 path.

**Expected behavior:**

- A returns PATH EXISTS; CHOOSE A NEW VERSION with zero modification.
- B verifies predecessor, uses Proposal ID QD-dash-window@v002, current base,
  RFC3339 UTC timestamp, and creates only v002.
- C atomic CREATE_IF_ABSENT has one winner; loser returns path-exists error.

**Assertions:**

- [ ] QDS-C04-A: Date never controls path uniqueness
- [ ] QDS-C04-B: Predecessor path/revision/version chain is explicit
- [ ] QDS-C04-C: Existing bytes are never updated in place

---

### Case 5: outside-range tuning redirects with decision ownership

**Fixture:** current range is 4.0–7.0 m, requested value is 9.0, and dependent
HUD presentation consumes the range.

**Expected behavior:**

1. QDR-008 is YES with knob/range/unit/owner/revision.
2. No quick proposal or range/data edit is created.
3. Conversation handoff names target ID/section/revision, requested value, product
   decision owner, dependent owner, and design-system revise-section.
4. Full authoring decides the new range and later propagation/review.

**Assertions:**

- [ ] QDS-C05-A: Rationale cannot extend range in quick path
- [ ] QDS-C05-B: quick-design does not choose new range
- [ ] QDS-C05-C: Dependent propagation is routed, not silently performed

---

### Case 6: production new system redirects; cosmetic stays under existing owner

**Fixture:**

- A requests a small standalone notification system requiring a new index row.
- B changes only hit-confirm text/color mapping in existing SYS-combat,
  preserving mechanics, accessibility policy, interfaces, state, and owner.
- C calls a new UI component cosmetic but it owns lifecycle state.

**Expected behavior:**

- A and C set applicable QDR rows YES and redirect with no proposal.
- B may derive QD-COSMETIC after all-NO evidence and requires lean-or-full review.
- Cosmetic proposal remains bound to existing combat GDD section/owner.

**Assertions:**

- [ ] QDS-C06-A: New Small System is not a profile
- [ ] QDS-C06-B: Cosmetic category never creates a hidden system owner
- [ ] QDS-C06-C: Accessibility-policy changes are not cosmetic

---

### Case 7: stale base, predecessor, or re-application requires rebase

**Fixture:**

- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- Target becomes B before write.
- Another variant has an APPLIED v001 against A and wants same delta on C.

**Expected behavior:**

1. Pre-create re-read detects A/B mismatch and writes nothing.
2. Returns ERROR, STALE, REBASE REQUIRED; never silently edits draft binding.
3. APPLIED v001 is not reapplied to C.
4. Follow-up requires v002, --supersedes exact v001 path/revision, base C, fresh
   decisions/risk/application/review/record.

**Assertions:**

- [ ] QDS-C07-A: atomic conflict check covers all source evidence
- [ ] QDS-C07-B: Conversation memory is not currentness evidence
- [ ] QDS-C07-C: Re-application cannot bypass new version review

---

### Case 8: decision ownership classes prevent silent override

**Fixture:**

- User selects one in-range tuning option.
- Current owner GDD establishes range as hard evidence.
- Observable threshold is derived from accepted inputs.
- Engine storage question appears.

**Expected behavior:**

1. Four QDD records use product-choice, evidence-backed-hard-constraint,
   derived-design-constraint, and technical-handoff correctly.
2. Hard evidence includes owner path/ID/locator/revision.
3. Derived record includes inputs/derivation/assumptions and acceptance.
4. Technical question is routed and absent from design delta.

**Assertions:**

- [ ] QDS-C08-A: User owns product outcome, not external fact classification
- [ ] QDS-C08-B: Delta IDs reference accepted decision IDs
- [ ] QDS-C08-C: Application author cannot choose a different outcome silently

---

### Case 9: partial, blocked, error, decline, and failed persistence are distinct

**Fixture:** variants stop with unresolved decision, lack risk evidence, provide
unsupported target, decline persistence, or fail atomic byte verification.

**Expected behavior:**

- Unresolved discussion: PARTIAL/DRAFT/(CURRENT or STALE)/NO/NOT_REQUESTED/DRAFT_ONLY.
- Missing risk evidence: BLOCKED/NOT_CREATED/NOT_APPLICABLE/NO/NOT_REQUESTED/BLOCKED.
- Unsupported input: ERROR/NOT_CREATED/INVALID/NO/NOT_REQUESTED/ERROR.
- Decline: COMPLETE/DRAFT/CURRENT/NO/DECLINED/DRAFT_ONLY.
- Persistence failure: ERROR/NOT_CREATED/INVALID/NO/FAILED/ERROR.

**Assertions:**

- [ ] QDS-C09-A: No incomplete path emits PROPOSAL_CREATED
- [ ] QDS-C09-B: UNKNOWN never defaults to NO
- [ ] QDS-C09-C: Failure does not claim canonical artifact exists

---

### Case 10: proposal approval cannot authorize downstream writes

**Fixture:** valid draft is approved and user asks to apply, review, record, and
implement immediately.

**Expected behavior:**

1. Approval applies only to exact proposal content and CREATE_IF_ABSENT.
2. Only proposal may be written.
3. GDD/checkpoint/data/index/story/application/review/lifecycle/code/test remain
   non-writes.
4. Downstream action is blocked and independent owner handoffs are returned.

**Assertions:**

- [ ] QDS-C10-A: Proposal author cannot self-apply/review/record
- [ ] QDS-C10-B: Draft approval is not formal review
- [ ] QDS-C10-C: Workflow stops after handoff

---

### Case 11: proposal v2 schema is complete and non-authoritative

**Fixture:** verified QD-LOCAL draft with two explicitly supplied sections.

**Expected behavior:**

1. Header contains all v2 identity, UTC, base/index/risk/profile/non-eligibility
   fields.
2. Exactly seven required level-two sections exist.
3. Each QDDELTA maps one supplied section, decision IDs, owner, before/after,
   and unchanged invariants.
4. Literal statement says proposal does not replace authoritative GDD.

**Assertions:**

- [ ] QDS-C11-A: No GDD Update Required No escape exists
- [ ] QDS-C11-B: Proposal cannot instruct programmer to implement
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

---

### Case 12: application uses design-system ownership and receipt v1

**Fixture:** valid current proposal contains delta IDs for Formulas and Tuning
Knobs.

**Expected behavior:**

1. Separate application author revalidates proposal/base/section/evidence revisions.
2. Each section uses design-system revise-section with separate authorization,
   decision owner preserved, and no quick-design write expansion.
3. External immutable cgs.design-application/v1 receipt binds proposal,
   pre/post GDD revisions, delta IDs, exact ranges/patch, task, timestamp, payload.
4. Base mismatch requires new proposal version, not application improvisation.

**Assertions:**

- [ ] QDS-C12-A: Application matches design-system P1 section ownership
- [ ] QDS-C12-B: Receipt is revision evidence, not approval
- [ ] QDS-C12-C: Proposal author does not create receipt

---

### Case 13: review uses design-review P1 current evidence

**Fixture:**

- Updated GDD and application receipt exist.
- For re-review, prior design-review v2 report targets receipt prior-state.
- Variants use self-review, solo, partial, weak depth, stale target, malformed
  report/evidence payload, or valid independent approval.

**Expected behavior:**

- Re-review gets exact prior report plus application receipt revision evidence.
- Receipt post-revision equals current GDD and review target.
- Only formal independent APPROVED cgs.review-evidence/v1 at profile depth can
  support APPLIED.
- Invalid variants remain NO and are never repaired by status.

**Assertions:**

- [ ] QDS-C13-A: QD-LOCAL requires full review
- [ ] QDS-C13-B: Tuning/cosmetic accept lean or full formal review
- [ ] QDS-C13-C: Review report/evidence revisions recompute
- [ ] QDS-C13-D: Reviewer identity differs from both authors

---

### Case 14: PROPOSED remains rationale, not shadow truth

**Fixture:** valid PROPOSED file exists, base GDD remains current, no lifecycle
record, and a story cites only proposal path.

**Input:**

    $quick-design status <proposal>

**Expected behavior:**

1. Read-only status returns PROPOSED/CURRENT/NO/STATUS_REPORTED.
2. Story reference is inadequate: it needs updated authoritative GDD and current
   APPLIED record.
3. No repair/application/review/record/story edit occurs.

**Assertions:**

- [ ] QDS-C14-A: PROPOSED never authorizes production
- [ ] QDS-C14-B: Proposal is rationale only
- [ ] QDS-C14-C: Status is explicit-path and read-only

---

### Case 15: valid APPLIED and CURRENT graph is recognized read-only

**Fixture:** proposal v2, application receipt v1, current post-GDD, independent
APPROVED review evidence v1 at required depth, lifecycle v2 record, identities,
revisions, and predecessor all revalidate.

**Expected behavior:**

1. Status validates complete explicit graph.
2. Returns APPLIED/CURRENT/Implementation Eligible YES/STATUS_REPORTED.
3. Still requires separate current story-readiness.
4. Any one stale/invalid predicate changes eligibility to NO without mutation.

**Assertions:**

- [ ] QDS-C15-A: All eligibility predicates are simultaneous
- [ ] QDS-C15-B: Recognition never writes evidence
- [ ] QDS-C15-C: quick-design never chains into implementation

---

### Case 16: experiment-only cannot enter production lifecycle

**Fixture:** exact prototype scope exists and unused proposal path is authorized.

**Expected behavior:**

1. Production target/id/section/base arguments are rejected in experiment form.
2. Valid experiment proposal has EXPERIMENT_ONLY, exact scope, review N/A, and
   eligibility NO.
3. APPLIED/lifecycle production handoff and story-readiness are unavailable.
4. No production artifact changes.

**Assertions:**

- [ ] QDS-C16-A: Experiment identity is exact and isolated
- [ ] QDS-C16-B: Experiment never becomes APPLIED
- [ ] QDS-C16-C: Only prototype-validation handoff is offered

---

### Case 17: P1 test evidence and catalog registration are honest

**Fixture:** current staged implementation, metadata, and this spec; shared
catalog last-result fields are not assumed current.

**Expected behavior:**

1. Static/spec/category evaluation maps every assertion to current file revisions.
2. Each axis reports PASS/FAIL/UNEXECUTED separately.
3. A separately owned shared catalog update occurs only after actual execution.
4. Empty/stale/copied fields are not test evidence.

**Assertions:**

- [ ] QDS-C17-A: Spec covers QDS-001 through QDS-012
- [ ] QDS-C17-B: This candidate does not edit shared catalog
- [ ] QDS-C17-C: Current implementation/metadata/spec revisions are required

---

## Cross-skill compatibility

- [ ] QDS-X001: Application uses staged design-system revise-section exact section ownership
- [ ] QDS-X002: Product/hard/derived/technical decision ownership matches design-system
- [ ] QDS-X003: Re-review evidence shape satisfies staged design-review v2 input requirements
- [ ] QDS-X004: Formal evidence uses staged design-review cgs.review-evidence/v1
- [ ] QDS-X005: Solo/advisory/partial review never approves
- [ ] QDS-X006: Proposal is rationale; story authority is current GDD plus APPLIED record
- [ ] QDS-X007: Propagation remains a separately owned workflow
- [ ] QDS-X008: Metadata/spec/skill agree on proposal/risk/application/lifecycle contracts and profiles

## Authoritative P1 closure matrix

| Audit ID | Static clause | Behavioral evidence |
|---|---|---|
| QDS-005 | Typed risk facts precede profile classification | Cases 1 and 2 assertions |
| QDS-006 | Exact target/system/section ownership | Cases 3 and 6 assertions |
| QDS-007 | Compare-and-create collision safety | Case 4 assertions |
| QDS-008 | Approved tuning-range enforcement | Case 5 assertions |
| QDS-009 | Production new-system redirect | Case 6 assertions |
| QDS-010 | Stale-base, predecessor, and re-application protocol | Cases 7 and 15 assertions |
| QDS-011 | Failure, partial, unsupported, decline, and persistence states | Case 9 assertions |
| QDS-012 | Current P1 spec evidence and honest catalog registration | Case 17 assertions |

## Coverage Notes

This contract covers QDS-001 through QDS-012. Filename normalization hardening,
project-specific implementation-value formats, dependent-owner tooling, and
downstream story policy refinements remain separate QDS-013..017 work except
where required to preserve the P1 authority boundary.

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
