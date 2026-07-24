# Skill Test Spec: $design-system

## Skill Summary

$design-system authors or performs a bounded revision of exactly one system GDD.
It has four explicit invocation modes: new, resume, fill-gaps, and
revise-section. The author may mutate only the target GDD and its per-target
checkpoint. It never updates the entity registry or systems index, creates
approval evidence, embeds a sign-off, or marks its own output Approved.

The GDD contains player-visible rules and product-facing interface requirements.
Implementation, engine, architecture, QA-procedure, and review material is
routed out. Formal review is one independent whole-artifact review after
authoring stops.

The author validates system GDDs against content profile system-gdd/v2 and uses
only design-system-checkpoint/v3 for resumable continuity. The v3 checkpoint
binds origin mode, authorized scope, target and section baselines, bounded
context, registry evidence, decisions, consultations, and review invalidation.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only name and non-empty description; name is design-system
- [ ] Arguments define new, resume, fill-gaps, and revise-section
- [ ] retrofit resolves explicitly to fill-gaps or revise-section
- [ ] Maximum write set is exactly target GDD plus per-target checkpoint
- [ ] Writes to index, registry, review records, ADRs, and engine documents are forbidden
- [ ] Author never writes Approved or invalid status Designed
- [ ] Legal index states are exactly Not Started, In Design, In Review, Approved, Implemented
- [ ] No inline or per-section formal review gate exists
- [ ] Fresh-task whole-artifact review handoff is target-hash-bound
- [ ] Implementation/ADR material is forbidden in GDD and routed to ADR/TECH
- [ ] Every section write has semantic and transactional preflight
- [ ] Complete changeset is authorized once before first write
- [ ] Content approval never expands filesystem or section scope
- [ ] Content profile is system-gdd/v2
- [ ] Resumable checkpoint schema is design-system-checkpoint/v3
- [ ] A v1/v2 checkpoint fails closed for resume
- [ ] All eight required sections have content-level assertions
- [ ] Context ordering, 12-file cap, 524288-byte cap, manifest, and overflow behavior are explicit
- [ ] Registry claim classes and legacy-unverified behavior are explicit
- [ ] Transactional preflight re-hashes target, registry, and cited evidence
- [ ] Consultation is capped at one per section, three per run, one 60-second attempt
- [ ] Consultation result states are complete, partial, timeout, failed, skipped
- [ ] requirement, applicability, content_state, and workflow_state are distinct
- [ ] Optional absence and bounded not-applicable semantics are explicit
- [ ] Supported optional names are Visual/Audio Requirements, UI Requirements, and Open Questions
- [ ] Decision records define exactly four authority classes
- [ ] Resume preserves origin mode, authorized scope, and baseline hashes
- [ ] Content mutation invalidates prior review-handoff hashes
- [ ] Author handoff binds target SHA, content profile, and context-manifest digest

---

## Behavioral Cases

### Case 1: new mode writes only GDD and checkpoint

**Fixture:**

- game-concept.md and systems-index.md exist.
- movement target/checkpoint do not exist.
- registry and index hashes are recorded.

**Input:**

    $design-system movement --mode new

**Expected behavior:**

1. The skill presents target, checkpoint, eight sections, and no other writes.
2. After authorization it loads bounded context and creates an eight-section
   skeleton with Status In Design and Document Schema system-gdd/v2.
3. Every section follows decision, draft, semantic preflight, approval,
   transactional preflight, atomic write, and checkpoint update.
4. Whole-artifact validation changes only Status to In Review and records target
   plus context-manifest hashes.
5. It returns an independent-review handoff and stops.

**Assertions:**

- [ ] Only target GDD and checkpoint changed
- [ ] systems-index.md and entities.yaml are unchanged
- [ ] No review, sign-off, ADR, or engine document was created
- [ ] Each canonical required section occurs exactly once
- [ ] Status is In Review, never Approved
- [ ] Checkpoint target hash equals final GDD hash
- [ ] No inline review gate ran

---

### Case 2: fill-gaps preserves substantive sections

**Fixture:**

- Existing GDD has substantive Overview, Detailed Rules, and Dependencies.
- Formulas/Edge Cases are placeholders; Acceptance Criteria is missing.
- All other required sections are substantive.
- Baseline body hashes are recorded.

**Input:**

    $design-system design/gdd/combat.md --mode fill-gaps

**Expected behavior:**

1. All required sections are inventoried before authorization.
2. Scope is exactly Formulas, Edge Cases, Acceptance Criteria.
3. Weak but substantive content is not treated as a gap.
4. Only scoped gaps are authored.
5. Out-of-scope bodies remain byte-for-byte unchanged.

**Assertions:**

- [ ] Only baseline missing, empty, or placeholder-only required sections are eligible
- [ ] Baseline substantive body hashes are unchanged
- [ ] No optional section is auto-created
- [ ] Whole-artifact handoff occurs only when all sections validate

---

### Case 3: revise-section changes exactly one selected section

**Fixture:**

- Existing complete GDD has substantive Formulas.
- Target and Formulas body hashes are recorded.

**Input:**

    $design-system design/gdd/combat.md --mode revise-section --section "Formulas"

**Expected behavior:**

1. Current Formulas body/hash are shown.
2. User makes and approves a new product decision.
3. Preflight verifies target, evidence, and selected baseline.
4. Exactly Formulas changes; other bodies are preserved.
5. Prior review is invalidated and status eventually becomes In Review only
   after whole-artifact validation.

**Assertions:**

- [ ] revise-section requires one supported canonical section
- [ ] No unselected section changes
- [ ] Prior approval evidence is not copied
- [ ] Index is not updated
- [ ] Review remains whole-artifact

---

### Case 4: resume requires v3 and matching bound evidence

**Fixture:**

- Variant A has matching target and v3 checkpoint with Edge Cases
  approved-not-written.
- Variant B target changed after checkpoint.
- Variant C uses a v1/v2 checkpoint.

**Input:**

    $design-system design/gdd/combat.md --mode resume

**Expected behavior:**

- A resumes exact stored content under original mode/scope.
- B returns ERROR — STALE CHECKPOINT with zero writes.
- C returns ERROR — UNSUPPORTED CHECKPOINT SCHEMA with zero writes.

**Assertions:**

- [ ] Written substantive sections are not re-discussed
- [ ] Conversation memory is not approval evidence
- [ ] Missing checkpoint makes resume unavailable
- [ ] invocation_mode is resume while origin_mode remains unchanged

---

### Case 5: technology content is routed out

**Fixture:**

- User asks whether Detailed Rules should use an engine singleton, event bus, or
  replicated component.
- Product-visible rule can be specified without that choice.

**Expected behavior:**

1. ADR/engine implementation text is not loaded into the GDD.
2. Checkpoint receives technical-handoff destination ADR/TECH with evidence and
   decision-needed or constraint-to-verify.
3. Draft contains only player-visible rule and design interface.
4. If uncertainty blocks product rule, section is blocked.

**Assertions:**

- [ ] No API/class/schema/storage/sync choice appears in GDD
- [ ] Technical content appears only in authorized checkpoint
- [ ] No technical sidecar is created
- [ ] Blocking uncertainty cannot be called complete

---

### Case 6: author cannot self-approve or cross-write

**Fixture:**

- All required sections pass.
- systems-index row is In Design.
- Registry contains matching and candidate facts.

**Expected behavior:**

1. Author may set only GDD status to In Review.
2. Registry candidates become checkpoint handoffs only.
3. Index and registry remain unchanged.
4. No review/sign-off evidence is written.
5. Author outputs target hash and fresh-task review command, then stops.

**Assertions:**

- [ ] Author writes are GDD plus checkpoint only
- [ ] No Designed or APPROVED author claim appears
- [ ] Checkpoint requests review but contains no verdict

---

### Case 7: recorder accepts only current independent approval

**Fixture:**

- A: independent persisted APPROVED report/receipt matches current target.
- B: target changed after review.
- C: report is same-task, advisory, partial, needs revision, major revision, or
  missing immutable receipt.
- Recorder has expected index pre-state.

**Expected behavior:**

- A may compare-and-set external index status Approved.
- B returns STALE REVIEW and changes nothing.
- C cannot authorize Approved.
- Index pre-state mismatch returns CONCURRENT INDEX CHANGE.

**Assertions:**

- [ ] Approval evidence includes exact target/hash
- [ ] Recorder re-hashes immediately before mutation
- [ ] Only external recorder may set Approved
- [ ] Stale/partial/advisory/non-APPROVED/missing-receipt evidence changes nothing

---

### Case 8: content approval and filesystem authorization differ

**Fixture:**

- User authorized exact target, checkpoint, and section scope.
- Drafting proposes an extra file or section.

**Expected behavior:**

1. Current content approval applies only inside existing scope.
2. Extra file/section is not written.
3. Expansion requires a revised complete changeset authorization.
4. Declined content remains pending/blocked and stops.

**Assertions:**

- [ ] No redundant per-section filesystem permission is requested
- [ ] No content is written without approval
- [ ] Scope expansion is blocked until authorized
- [ ] Empty/unapproved content is not complete

---

### Case 9: content profile rejects non-empty incomplete bodies

**Fixture:**

- All eight headings exist.
- Overview lacks player encounter and lost-value.
- Formulas lacks units, ranges, and worked example.
- Edge Cases lacks exact outcomes.
- A second variant has an approved Formulas not-applicable rationale.

**Expected behavior:**

1. system-gdd/v2 records assertion failures in v3 inventory.
2. Heading/non-empty text alone does not make content substantive.
3. Incomplete artifact remains In Design and partial.
4. N/A passes only for an eligible section with approved reason and observable
   consequence.

**Assertions:**

- [ ] Eight sections have explicit content assertions
- [ ] Overview/Fantasy/Rules/Edge Cases/Acceptance cannot be N/A
- [ ] Formulas/Dependencies/Knobs use bounded N/A rules
- [ ] Failures name missing elements
- [ ] Any failure blocks In Review

---

### Case 10: context budget fails closed reproducibly

**Fixture:**

- Mandatory sources fit individually.
- Selected dependencies/pillars push total over 12 files or 524288 bytes.
- Changeset was authorized.

**Expected behavior:**

1. Candidates use stable documented order.
2. No file is partially loaded.
3. Checkpoint records loaded path/role/size/hash, omitted candidates, totals,
   and CONTEXT_BUDGET_EXCEEDED.
4. Status becomes partial and GDD remains unchanged.

**Assertions:**

- [ ] Identical inputs produce identical ordered manifests
- [ ] Both numeric limits are enforced
- [ ] Required context is not silently omitted
- [ ] Overflow writes at most authorized checkpoint
- [ ] No section drafting follows overflow

---

### Case 11: registry claims are classified before approval

**Fixture:**

- A: legacy registry has no source hash.
- B: current target-owned claim.
- C: current external-owner claim contradicts draft.
- D: registry changes after semantic preflight.

**Expected behavior:**

- A is legacy-unverified and cannot silently constrain product rule.
- B may create target-owned-change-candidate handoff after user decision.
- C blocks until owning GDD is resolved.
- D returns ERROR — CONTEXT CLAIM CHANGED before target write.

**Assertions:**

- [ ] Six claim classes are defined
- [ ] Semantic claim comparison precedes approval
- [ ] Conflict-driven draft change requires new approval
- [ ] Transaction preflight re-hashes registry/evidence
- [ ] Registry is never edited

---

### Case 12: consultation limits and partial states

**Fixture:**

- Run has used two consultations.
- Optional consultation times out.
- Required consultation returns partial.
- One section requests a second adviser.

**Expected behavior:**

1. One adviser/section and three/run are maximum.
2. Each gets one 60-second attempt, no retry/nested delegation.
3. Optional timeout continues only via explicit user fallback.
4. Required partial blocks section and makes checkpoint partial.

**Assertions:**

- [ ] Complete/partial/timeout/failed/skipped states exist
- [ ] Section, role, question, hashes, required, status, fallback are recorded
- [ ] Fourth run consultation and second section adviser are rejected
- [ ] Missing specialist output is not invented

---

### Case 13: required, optional, and N/A are unambiguous

**Fixture:**

- Eight required sections exist.
- UI Requirements is absent.
- Open Questions is placeholder-only.
- Dependencies has approved not-applicable rationale.

**Expected behavior:**

1. requirement, applicability, content state, workflow state, and failures are
   separate.
2. Optional absence is valid.
3. Present optional placeholder blocks artifact completion.
4. It can be changed only by explicit revise-section.

**Assertions:**

- [ ] Optional absence is not a gap
- [ ] N/A is substantive approved content, not token
- [ ] new/fill-gaps do not add optional sections
- [ ] Exactly three supported optional names exist

---

### Case 14: decision provenance prevents authority override

**Fixture:**

- A user product choice has alternatives.
- Hard constraint has current owner path/section/hash.
- A curve derives from accepted inputs.
- Engine storage choice appears.

**Expected behavior:**

1. User selects product choice.
2. Hard constraint cannot be overridden in target.
3. Derived record preserves inputs, derivation, assumptions, acceptance.
4. Storage choice routes to technical-handoff.

**Assertions:**

- [ ] Exactly four decision classes exist
- [ ] Hard constraint has path/section/hash
- [ ] Derived constraint preserves derivation
- [ ] Written section references decision IDs
- [ ] User preference cannot silently override external-owner evidence

---

### Case 15: resume preserves original mutation predicate

**Fixture:**

- A checkpoint originated new.
- B originated fill-gaps with two baseline gaps.
- C originated revise-section with substantive selected baseline.
- All v3 hashes match.

**Expected behavior:**

- Each continues only original scope/predicate.
- B cannot replace baseline substantive content.
- C recovers exact approved draft despite substantive current baseline.

**Assertions:**

- [ ] origin_mode never becomes resume
- [ ] invocation_mode records resume
- [ ] Scope/baselines survive interruption
- [ ] Resume never broadens permission

---

### Case 16: revision invalidates prior review handoff

**Fixture:**

- Complete GDD/checkpoint has prior handoff target hash.
- One revise-section mutation is authorized.
- Variant B changes loaded context before final validation.

**Expected behavior:**

1. First mutation records review_handoff.invalidated_target_sha256 and
   invalidation_reason, clears active handoff, and demotes stale status to
   In Design.
2. New handoff appears only after artifact/current-context validation.
3. Handoff binds target hash, profile, manifest digest.
4. Variant B remains partial with no new review request.

**Assertions:**

- [ ] Prior evidence is not copied to changed bytes
- [ ] In Review is author status, not approval
- [ ] Stale target/context cannot authorize Approved
- [ ] Author does not fabricate immutable receipt

---

### Case 17: P1 verification evidence is current

**Fixture:**

- Implementation and spec contain the P1 contract.
- No catalog result is assumed current.

**Expected behavior:**

1. Static/spec/category axes map each assertion to current evidence.
2. Results record implementation/spec hashes.
3. Shared catalog writer registers only actual results in separate scope.
4. Unexecuted or stale fields remain visible.

**Assertions:**

- [ ] Three validation axes are separate
- [ ] Failures/unexecuted checks are not hidden
- [ ] This candidate does not mutate shared catalog
- [ ] Current hashes are required for registration

---

## Protocol Compliance

- [ ] Question -> Options -> Decision -> Draft -> Approval occurs per section
- [ ] Semantic preflight precedes approval
- [ ] Transactional preflight precedes every GDD mutation
- [ ] Modes have distinct mutation rules
- [ ] GDD and checkpoint are only writes
- [ ] GDD contains design truth only
- [ ] Author completion is at most In Review
- [ ] One independent whole-artifact review follows authoring
- [ ] Recorder approval is current-hash-bound and compare-and-set
- [ ] Workflow stops after review handoff
- [ ] system-gdd/v2 and checkpoint v3 state are deterministic
- [ ] Context, registry, and decisions are provenance-bound
- [ ] Consultation/overflow failure produces partial or blocked state
- [ ] Resume and review invalidation preserve stale-evidence safety

## Coverage Notes

### Authoritative P1 finding trace

| Audit ID | SKILL clause | Case/assertion |
|---|---|---|
| `DSG-005` | Section 2; continuation Section 5 | Case 9: `Eight sections have explicit content assertions`; `Any failure blocks In Review` |
| `DSG-006` | Section 3 bounded context | Case 10: `Both numeric limits are enforced`; `Required context is not silently omitted` |
| `DSG-007` | Section 3 registry claim classification | Case 11: `Six claim classes are defined`; `Registry is never edited` |
| `DSG-008` | Continuation Sections 4c–4d | Case 11: `Semantic claim comparison precedes approval`; `Transaction preflight re-hashes registry/evidence` |
| `DSG-009` | Continuation Section 6 | Case 12: `Complete/partial/timeout/failed/skipped states exist`; `Missing specialist output is not invented` |
| `DSG-010` | Section 2; continuation Section 5 optional material | Case 13: `Optional absence is not a gap`; `Exactly three supported optional names exist` |
| `DSG-011` | Continuation Section 4a | Case 14: `Exactly four decision classes exist`; `Derived constraint preserves derivation` |
| `DSG-012` | Section 1; continuation Section 9 | Cases 4/15: `Missing checkpoint makes resume unavailable`; `Resume never broadens permission` |
| `DSG-013` | Continuation Sections 4e and 8 | Case 16: `Prior evidence is not copied to changed bytes`; `Stale target/context cannot authorize Approved` |
| `DSG-014` | SKILL P1 audit traceability and required-spec boundary | Case 17: `Three validation axes are separate`; `Failures/unexecuted checks are not hidden`; `Current hashes are required for registration` |

This matrix traces every exact P1 ID from the 2026-07-20 design-system audit.
DSG-001 through DSG-004 are separately classified P0 findings. Slug collision
matrices and stable entity identifiers remain separate DSG-015/DSG-016 work and
are intentionally outside this P1 specification. The rows are written-contract
coverage, not executed test results.
