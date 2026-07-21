# Skill Test Spec: $ux-review

## Skill Summary

$ux-review is a read-only, profile-aware reviewer for the three artifact types
authored by $ux-design: screen/flow UX specs, HUD designs, and interaction
pattern libraries. It loads the current author sources, versions them with a
SHA-256 hash, routes from document identity rather than filename, calculates a
deterministic verdict, and returns a target-hash-bound structured record.

Quality verdicts are APPROVED, NEEDS REVISION, or MAJOR REVISION NEEDED.
Routing or schema failures return ERROR / MIGRATION REQUIRED with no quality
verdict. Accepted risk remains NOT_APPROVED and cannot satisfy a hard gate.

The skill never writes project files. Its returned record says
gate_evidence_status: NOT_PERSISTED; persistence belongs to a separate,
explicitly authorized recorder.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name
      matches the skill directory
- [ ] Reads both .agents/skills/ux-design/SKILL.md and
      .agents/skills/ux-design/references/continued-workflow.md
- [ ] Defines matching profiles for ux-spec, hud-design, and
      interaction-pattern-library
- [ ] Defines ERROR / MIGRATION REQUIRED separately from all quality verdicts
- [ ] Defines an exact severity-to-verdict algorithm
- [ ] Defines ux-review-record-v1 with target SHA-256, author-schema hash,
      findings, verdict, approval status, and persistence status
- [ ] Remains read-only
- [ ] Contains no statement that a conversation-only APPROVED verdict is
      implementation-ready or directly authorizes a visual/implementation handoff

---

## Director Gate Checks

None. $ux-review performs the UX review. It does not invoke another director
gate and does not claim its conversation-only output is persisted gate evidence.

---

## Test Cases

### Case 1: Current screen/flow author profile routes and passes

Fixture: A populated design/ux/inventory.md created from the current $ux-design
UX Spec skeleton. It contains the exact Template: UX Spec marker, every required
top-level/nested section, and every stated author minimum.

Input: $ux-review design/ux/inventory.md

Assertions:

- [ ] Routes to artifact_type: ux-spec from routing_basis: template-marker
- [ ] schema_version starts with ux-design-author-sha256:
- [ ] Checks the author skeleton, not the obsolete User Flows / Interaction
      States / Accessibility Notes schema
- [ ] Returns APPROVED when all author-required checks pass
- [ ] Returns a COMPLETE ux-review-record-v1 with the exact target SHA-256
- [ ] Keeps gate_evidence_status: NOT_PERSISTED and does not authorize handoff
- [ ] Makes no file writes

---

### Case 2: Current HUD profile does not require reviewer-only sections

Fixture: A complete current $ux-design HUD artifact with the Template: HUD
Design marker and populated HUD Philosophy, Information Architecture, Layout
Zones, HUD Elements, Dynamic Behaviors, Platform & Input Variants,
Accessibility, and Open Questions sections. It intentionally has no HUD States,
Visual Budget, Tuning Knobs, or Feedback & Notification sections.

Input: $ux-review hud

Assertions:

- [ ] The alias selects the path but the document marker selects hud-design
- [ ] The four reviewer-only sections above are not required
- [ ] The artifact can receive APPROVED when all current author requirements pass
- [ ] The record is hash-bound and gate_evidence_status is NOT_PERSISTED

---

### Case 3: Current interaction-pattern profile routes independently

Fixture: A complete current $ux-design interaction pattern library with the
exact Interaction Pattern Library marker, current top-level sections, and all
author-defined fields for every pattern.

Input: $ux-review patterns

Assertions:

- [ ] Routes to interaction-pattern-library
- [ ] Requires the current author profile rather than a fixed widget list
- [ ] Can return APPROVED without Animation Standards or Sound Standards tables

---

### Case 4: Explicit schema mismatch is not a quality verdict

Fixture: A UX spec declares Artifact Type: ux-spec and an unsupported explicit
Schema Version.

Input: $ux-review design/ux/inventory.md

Assertions:

- [ ] Returns ERROR / MIGRATION REQUIRED
- [ ] Reports the unsupported and current schema versions
- [ ] Record has review_status: ERROR, verdict: null, and
      approval_status: NOT_APPROVED
- [ ] No profile checklist or quality verdict is issued

---

### Case 5: Filename is fallback evidence only

Fixture: design/ux/hud.md has neither explicit artifact metadata nor a
recognized Template marker.

Input: $ux-review design/ux/hud.md

Assertions:

- [ ] Does not automatically apply the HUD profile from the filename
- [ ] Proposes the inferred type and asks for confirmation
- [ ] Issues no verdict before confirmation
- [ ] After confirmation, records user-confirmed-filename-fallback

---

### Case 6: Conflicting identity and report exclusion

Fixtures:

- design/ux/hud.md declares Template: UX Spec
- design/ux/reports/hud-review.md declares a review record
- design/ux/notes.md has no recognized identity

Inputs: $ux-review hud and $ux-review all

Assertions:

- [ ] The hud alias conflict returns ERROR / MIGRATION REQUIRED with no verdict
- [ ] all excludes the review record with reason review-report
- [ ] all excludes the notes file with reason unknown-artifact-type
- [ ] Neither excluded file receives a UX checklist or verdict

---

### Case 7: Deterministic severity-to-verdict mapping

Fixtures: Four otherwise schema-compatible artifacts: no required failures; one
failed non-foundation requirement; one absent profile foundation section; and
one required check left unevaluated.

Assertions:

- [ ] No required failures returns APPROVED
- [ ] A BLOCKING finding returns NEEDS REVISION
- [ ] A MAJOR finding returns MAJOR REVISION NEEDED
- [ ] An unevaluated required check returns ERROR with verdict: null
- [ ] Findings use stable UXF-<profile>-<check-key> IDs and cite target sections

---

### Case 8: Hash binding and staleness

Fixture: Review a valid artifact, capture target_sha256, then change one byte in
the target.

Assertions:

- [ ] The record contains the exact reviewed hash
- [ ] The changed target no longer matches target_sha256
- [ ] The stale_when rule invalidates the old record
- [ ] Gate consumers are instructed to reject the stale record
- [ ] Bytes changing during review cause ERROR with no verdict

---

### Case 9: Accepted risk never becomes approval

Fixture: A review returns NEEDS REVISION with open blocking finding IDs, and the
user chooses to proceed.

Assertions:

- [ ] Original verdict remains NEEDS REVISION
- [ ] Decision status is ACCEPTED_RISK
- [ ] approval_status remains NOT_APPROVED
- [ ] gate_evidence_eligible is false
- [ ] Output never calls the artifact approved or implementation-ready

---

### Case 10: File not found

Fixture: design/ux/inventory-screen.md does not exist.

Input: $ux-review design/ux/inventory-screen.md

Assertions:

- [ ] Error names the missing path
- [ ] Suggests $ux-design inventory-screen
- [ ] No checklist and no quality verdict are issued
- [ ] No file is written

---

## Protocol Compliance

- [ ] Uses the matching current $ux-design author profile for all three types
- [ ] Never routes solely from a path without confirmation
- [ ] Never reviews reports or unknown document types
- [ ] Schema mismatch produces ERROR / MIGRATION REQUIRED, not a quality verdict
- [ ] Every complete result is target-hash-bound
- [ ] Verdict follows the documented algorithm exactly
- [ ] Accepted risk remains NOT_APPROVED
- [ ] No files are written
- [ ] Revision handoff points to the matching $ux-design mode; implementation
      handoff requires separately persisted, current-hash evidence and is never
      authorized by this conversation-only reviewer

---

## Coverage Notes

- Persistent recording and gate consumption are external integration concerns;
  this spec verifies that $ux-review returns a persistable record and never
  falsely labels it persisted.
- Bounded all execution, missing dependency/partial semantics, prior-finding
  convergence, and generated schema fixtures remain follow-up coverage outside
  this P0 remediation.
