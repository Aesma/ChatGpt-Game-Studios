# Skill Test Spec: $design-system

## Skill Summary

$design-system authors or performs a bounded revision of exactly one system GDD.
It has four explicit modes: new, resume, fill-gaps, and revise-section. The
author may mutate only the target GDD and its per-target checkpoint. It never
updates the entity registry or systems index, creates approval evidence, embeds a
sign-off, or marks its own output Approved.

The GDD contains player-visible rules and product-facing interface requirements.
Implementation, engine, architecture, QA-procedure, and review material is routed
out of the GDD. Technical questions are captured only as typed ADR/TECH handoffs
in the authorized checkpoint.

Formal review is one independent whole-artifact review after authoring stops. A
separate recorder may set systems-index status Approved only when the formal
APPROVED report is independent, immutable, and bound to the current GDD SHA-256.

---

## Static Assertions (Structural)

Verified without a fixture.

- [ ] YAML frontmatter contains only name and a non-empty description; name is design-system
- [ ] Main workflow has at least two phase headings and requires the continuation
- [ ] Arguments define new, resume, fill-gaps, and revise-section
- [ ] retrofit is not an implicit mode; it resolves to fill-gaps or revise-section
- [ ] The maximum write set is exactly the target GDD plus one per-target checkpoint
- [ ] The workflow explicitly forbids writes to systems-index.md, entities.yaml, review records, sign-off records, ADRs, and engine documents
- [ ] The author never writes Approved and never writes the invalid status Designed
- [ ] Legal systems-index states are exactly Not Started, In Design, In Review, Approved, and Implemented
- [ ] The workflow has no inline or per-section CD-GDD-ALIGN gate
- [ ] The formal review handoff is a fresh-task whole-artifact review bound to target SHA-256
- [ ] Implementation and ADR material is forbidden in the GDD and routed to ADR/TECH handoffs
- [ ] Every section write uses a pre-write hash guard and mode-specific mutation predicate
- [ ] The complete changeset is authorized once before the first write; per-section prompts approve content, not new file scope
- [ ] Formal review outcome vocabulary includes APPROVED, NEEDS REVISION, MAJOR REVISION NEEDED, and PARTIAL REVIEW

---

## Behavioral Cases

### Case 1: New mode writes only the GDD and checkpoint

**Fixture:**

- design/gdd/game-concept.md exists
- design/gdd/systems-index.md lists movement as Not Started
- design/gdd/movement.md does not exist
- production/session-state/design-system-movement.yaml does not exist
- entity registry and systems index hashes are recorded before the run

**Input:**

    $design-system movement --mode new

**Expected behavior:**

1. The skill resolves design/gdd/movement.md and the matching checkpoint.
2. It presents those two paths, all eight required sections, and no other writes
   as one changeset.
3. After authorization it creates the eight-section skeleton with Status In Design.
4. Each section follows user decision, draft, content approval, preflight, atomic
   write, and checkpoint update.
5. After whole-artifact validation it changes only the GDD Status header to
   In Review and records the final GDD SHA-256 in the checkpoint.
6. It returns an independent-review handoff and stops.

**Assertions:**

- [ ] Only design/gdd/movement.md and its checkpoint changed
- [ ] systems-index.md and entities.yaml are byte-for-byte unchanged
- [ ] No review record, director sign-off, ADR, or engine document was created or changed
- [ ] The GDD has each of the eight canonical sections exactly once
- [ ] The GDD status is In Review, never Approved
- [ ] Checkpoint.review_handoff.target_sha256 equals the final GDD SHA-256
- [ ] No inline review gate ran

---

### Case 2: fill-gaps preserves substantive sections

**Fixture:**

- Existing system GDD has substantive Overview, Detailed Rules, and Dependencies
- Formulas and Edge Cases are placeholders
- Acceptance Criteria is missing
- Other required sections are substantive
- Baseline body hashes are recorded for every substantive section

**Input:**

    $design-system design/gdd/combat.md --mode fill-gaps

**Expected behavior:**

1. The skill classifies all eight sections before authorization.
2. It scopes only Formulas, Edge Cases, and Acceptance Criteria.
3. It refuses to treat merely weak but substantive content as a gap.
4. It authors and writes only the three scoped gaps.
5. Out-of-scope sections remain byte-for-byte unchanged.

**Assertions:**

- [ ] Only missing, empty, or placeholder-only required sections were eligible
- [ ] Every baseline substantive section body hash is unchanged
- [ ] No existing substantive section was rewritten
- [ ] The target and checkpoint are the only mutated files
- [ ] The whole artifact receives one review handoff only after all eight sections validate

---

### Case 3: revise-section intentionally replaces one substantive section

**Fixture:**

- Existing complete system GDD
- Formulas contains substantive content
- Current GDD SHA-256 and Formulas body hash are recorded

**Input:**

    $design-system design/gdd/combat.md --mode revise-section --section "Formulas"

**Expected behavior:**

1. The skill shows the current Formulas body and baseline hash.
2. The user makes a new product decision and approves the replacement draft.
3. Preflight verifies both current target hash and selected-section baseline.
4. Exactly the Formulas body changes; every other section body is preserved.
5. Any prior Approved header is changed to In Review because the artifact hash
   changed.
6. The new final hash is handed to a fresh whole-artifact review.

**Assertions:**

- [ ] revise-section requires exactly one canonical section
- [ ] A substantive selected section may be replaced
- [ ] No unselected section changes
- [ ] Prior approval is treated as stale and is not copied or embedded
- [ ] The author does not update systems-index status
- [ ] Review is whole-artifact, not a gate on only Formulas

---

### Case 4: resume requires a matching checkpoint hash

**Fixture:**

- A target and design-system-checkpoint/v2 checkpoint exist
- Checkpoint marks Edge Cases approved-not-written
- Variant A: checkpoint.current_sha256 equals current target SHA-256
- Variant B: another task changed the target after the checkpoint

**Input:**

    $design-system design/gdd/combat.md --mode resume

**Expected behavior:**

- Variant A resumes at Edge Cases without re-discussing written sections.
- Variant B returns ERROR — STALE CHECKPOINT and writes nothing.

**Assertions:**

- [ ] resume never infers permission to rewrite a substantive written section
- [ ] Hash mismatch blocks both GDD and checkpoint mutation
- [ ] Conversation memory is not used as approval or hash evidence
- [ ] Missing checkpoint makes resume unavailable

---

### Case 5: technology content is routed out of the GDD

**Fixture:**

- During Detailed Rules the user asks whether the system should use an engine
  singleton, event bus, or replicated component
- The product-visible rule can be specified without choosing one

**Input:**

    Continue the Detailed Rules section

**Expected behavior:**

1. The skill does not load or quote ADR/engine implementation text into the GDD.
2. It records a checkpoint technical_handoffs entry with destination ADR/TECH,
   source evidence, and status decision-needed or constraint-to-verify.
3. It drafts only the player-visible rule and product-facing input/output behavior.
4. If the implementation uncertainty prevents a product decision, it marks the
   section blocked and stops.

**Assertions:**

- [ ] No API, class, resource schema, storage choice, synchronization mechanism, or ADR choice appears in the GDD
- [ ] Technical material appears only in the authorized checkpoint handoff
- [ ] No ADR or technical sidecar is created by the author
- [ ] The section is not falsely completed when a blocking product rule remains unresolved

---

### Case 6: author cannot self-approve or cross-write authorities

**Fixture:**

- All eight sections pass author whole-artifact validation
- systems-index row is currently In Design
- entity registry contains matching and new candidate facts

**Input:**

    Finish the design-system run

**Expected behavior:**

1. The author may set only the GDD header to In Review.
2. Registry candidates may be reported in conversation or checkpoint evidence,
   but the registry is not changed.
3. The systems index is not changed to In Review, Approved, or any other value.
4. No review/sign-off evidence is written by the author.
5. The author outputs the target SHA-256 and fresh-task design-review command,
   then stops.

**Assertions:**

- [ ] Author writes remain limited to GDD plus checkpoint
- [ ] Registry and index hashes remain unchanged
- [ ] No Designed status is emitted
- [ ] No APPROVED claim is emitted by the author
- [ ] The checkpoint states that review is required and does not contain a formal verdict

---

### Case 7: recorder accepts only current-hash independent approval

**Fixture:**

- Variant A: independent whole-artifact report has verdict APPROVED and target
  SHA-256 equals the current GDD SHA-256
- Variant B: report says APPROVED but target changed after review
- Variant C: report is same-task, solo/advisory, PARTIAL REVIEW,
  NEEDS REVISION, or MAJOR REVISION NEEDED
- Recorder has an expected systems-index pre-state

**Input:**

    Recorder consumes review evidence after the authoring workflow has stopped

**Expected behavior:**

- Variant A may create immutable review evidence and compare-and-set the target
  systems-index row to Approved.
- Variant B returns STALE REVIEW and changes nothing.
- Variant C cannot authorize Approved.
- Any index pre-state mismatch returns CONCURRENT INDEX CHANGE and changes nothing.

**Assertions:**

- [ ] Approval evidence includes exact target path and SHA-256
- [ ] Recorder re-hashes the current GDD immediately before mutation
- [ ] Recorder uses compare-and-set for the index row
- [ ] Only the external recorder may set Approved
- [ ] Stale, partial, advisory, same-task, or non-APPROVED evidence leaves index unchanged
- [ ] Legal status enumeration excludes Designed

---

### Case 8: section approval and filesystem authorization are distinct

**Fixture:**

- User has authorized the target GDD, checkpoint, and exact scoped sections
- During drafting the author proposes an additional file or an extra section

**Input:**

    Approve the current section draft

**Expected behavior:**

1. Approval authorizes only the current section content inside existing scope.
2. The extra file/section is not written.
3. A material scope expansion requires a revised complete changeset authorization.
4. Declining a section leaves it pending/blocked and stops without writing empty
   or placeholder content as complete.

**Assertions:**

- [ ] No per-section filesystem permission prompt is added inside unchanged scope
- [ ] Content is never written without section approval
- [ ] Scope expansion is blocked until newly authorized
- [ ] Empty or unapproved content is not written as complete

---

## Protocol Compliance

- [ ] Question -> Options -> User Decision -> Draft -> Content Approval occurs for every authored section
- [ ] Preflight precedes every GDD mutation
- [ ] new, resume, fill-gaps, and revise-section have mutually distinct mutation rules
- [ ] Target GDD and per-target checkpoint are the only author writes
- [ ] GDD contains design truth only; ADR/TECH and QA material are routed out
- [ ] Author completion status is at most In Review
- [ ] One independent whole-artifact review follows authoring; no inline/per-section approval gate
- [ ] Recorder approval is current-hash-bound and compare-and-set
- [ ] Workflow stops after the independent-review handoff

## Coverage Notes

This P0 contract covers DSG-001 through DSG-004. It includes only the context,
hash, and failure guards needed to make those P0 contracts coherent. Full
lower-priority coverage for content-quality scoring, byte budgets, slug-resolution
matrices, specialist fan-out and timeout policy, optional-section state, registry
claim ownership, and stable entity identifiers remains outside this spec.
