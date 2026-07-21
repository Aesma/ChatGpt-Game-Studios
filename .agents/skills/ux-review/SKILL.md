---
name: ux-review
description: "Read-only, profile-aware validation of UX artifacts with deterministic verdicts and hash-bound review records."
---

## Invocation and execution

Invoke this workflow as `$ux-review`.

Arguments: `[file-path or 'all' or 'hud' or 'patterns']`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `ux-designer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.

## P0 review protocol (authoritative)

This protocol overrides every conflicting routing rule, checklist, output template,
verdict definition, and advisory statement later in this file. The later material
is legacy detail and may only be used when it agrees with this protocol. This
skill remains READ-ONLY: it never creates, edits, or persists a file.

### 1. Load the author's versioned profiles

Before selecting a review profile, read these author sources in full:

- .agents/skills/ux-design/SKILL.md
- .agents/skills/ux-design/references/continued-workflow.md

They are the schema source of truth. Compute author_schema_hash as SHA-256 over
the exact bytes of the first file, one NUL byte, and the exact bytes of the
second file. The active schema_version is
ux-design-author-sha256:<author_schema_hash>. Load the matching fenced skeleton
and only the requirements or minimums stated for that mode in the author
sources. Do not invent a parallel reviewer schema.

The current author profiles are:

- ux-spec: Purpose & Player Need; Player Context on Arrival; Navigation
  Position; Entry & Exit Points; Layout Specification; States & Variants;
  Interaction Map; Events Fired; Transitions & Animations; Data Requirements;
  Accessibility; Localization Considerations; Acceptance Criteria; Open Questions.
- hud-design: HUD Philosophy; Information Architecture; Layout Zones; HUD
  Elements; Dynamic Behaviors; Platform & Input Variants; Accessibility; Open
  Questions.
- interaction-pattern-library: Overview; Pattern Catalog; Patterns; Gaps &
  Patterns Needed; Open Questions.

If an author source is missing or unreadable, the requested profile is absent,
an explicit schema version is unsupported, or these documented mappings no
longer agree with the author sources, return ERROR / MIGRATION REQUIRED with
verdict: null. Report expected and observed values. Never apply a stale or
best-fit checklist. In particular, do not require HUD States, Visual Budget,
Tuning Knobs, Feedback & Notification, Animation Standards, or Sound Standards
unless a future author profile requires them.

### 2. Resolve artifact identity before routing

Read each candidate before choosing a profile. Resolve artifact_type,
schema_version, and routing_basis in this precedence order:

1. Explicit blockquote fields Artifact Type and Schema Version, when both exist.
2. The exact current-author Template marker, which is a machine-readable legacy
   compatibility alias:
   - Template: UX Spec maps to ux-spec.
   - Template: HUD Design maps to hud-design.
   - Template: Interaction Pattern Library maps to
     interaction-pattern-library.
   A Template marker uses the current author-schema hash as schema_version.
3. Filename is fallback evidence only. When recognized metadata is absent,
   propose the inferred type and obtain user confirmation before reviewing.
   Record routing_basis: user-confirmed-filename-fallback. Before confirmation,
   do not run a checklist and do not issue a quality verdict.

The hud and patterns arguments select candidate paths only; they do not force a
profile. If explicit metadata conflicts with the Template marker, or an alias
selects a document of another type, return ERROR / MIGRATION REQUIRED with no
quality verdict.

Review reports and unknown documents are ineligible. A review-record declaration,
a top-level UX Review or Review Record heading, or a path below a review/reports
directory identifies a review report. In all mode, list ineligible paths under
skipped with reason review-report or unknown-artifact-type and do not review
them. A specifically requested ineligible file returns an error with no verdict.

### 3. Normalize findings and calculate the verdict

Evaluate every required top-level section and every requirement or minimum for
the selected author profile. Never apply another profile's checklist. Normalize
each failure with stable fields:

- id: UXF-<profile>-<stable-check-key>
- check_id: <profile>.<stable-check-key>
- severity: MAJOR, BLOCKING, or ADVISORY
- path and section
- observed evidence and expected author requirement
- specific remediation

Reuse the same ID for the same check on re-review. Assign severity by rule:

- MAJOR: a foundation section is absent. Foundations are Purpose & Player Need
  or Interaction Map for ux-spec; HUD Philosophy, Information Architecture, or
  HUD Elements for hud-design; Pattern Catalog or Patterns for the interaction
  pattern library.
- BLOCKING: any other author-required section, nested structure, or stated
  minimum fails.
- ADVISORY: an improvement not required by the author profile.

Apply this verdict algorithm exactly, in order:

1. Routing or schema failure: ERROR / MIGRATION REQUIRED; verdict: null.
2. Any required check not evaluated: ERROR; verdict: null.
3. One or more MAJOR findings: MAJOR REVISION NEEDED.
4. Otherwise, one or more BLOCKING findings: NEEDS REVISION.
5. Otherwise: APPROVED. Advisory findings may remain only when every required
   check passed.

Do not choose a verdict by overall impression. Report passed/total required-check
coverage and counts for every severity.

### 4. Return a hash-bound review record

Hash the exact target bytes at review start and immediately before output. A
change between those hashes returns ERROR with reason
target-changed-during-review and verdict: null. Every result must include this
complete structured record:

    review_record_schema: ux-review-record-v1
    review_policy: ux-review-p0-v1
    review_status: COMPLETE | ERROR
    reviewed_at_utc: <ISO-8601 UTC>
    target_path: <repository-relative path>
    target_sha256: <hash of exact reviewed bytes>
    artifact_type: ux-spec | hud-design | interaction-pattern-library | null
    routing_basis: explicit-metadata | template-marker |
      user-confirmed-filename-fallback | null
    profile_id: <artifact_type>@<schema_version> | null
    schema_version: <version | null>
    author_schema_hash: <hash | null>
    required_checks_passed: <integer>
    required_checks_total: <integer>
    finding_counts: { major: <integer>, blocking: <integer>, advisory: <integer> }
    verdict: APPROVED | NEEDS REVISION | MAJOR REVISION NEEDED | null
    approval_status: APPROVED | NOT_APPROVED
    accepted_risk: false
    gate_evidence_eligible: <true only for COMPLETE plus APPROVED>
    gate_evidence_status: NOT_PERSISTED
    stale_when: sha256(current target bytes) != target_sha256
    findings: []
    skipped: []
    error: null

For all mode, return one record per eligible artifact; never combine target
hashes into one approval. Any artifact edit makes its old record stale.

This skill returns a conversation record only and never claims it is persisted.
A separate, explicitly authorized recorder may persist the record only after
rechecking target_sha256. A gate consumer must reject an unpersisted or stale
record, every non-APPROVED verdict, and approval_status: NOT_APPROVED.

### 5. Accepted risk is not approval

A user may proceed despite a non-approved result, but the original verdict does
not change. Add decision_status: ACCEPTED_RISK, accepted_risk: true,
approval_status: NOT_APPROVED, gate_evidence_eligible: false, the accepting user
and UTC timestamp, and every accepted open finding ID. Never describe this state
as approved, implementation-ready, reviewed-and-passed, or sufficient hard
evidence.

---


## Overview

Validates UX design documents before they enter the implementation pipeline.
Acts as the quality gate between UX Design and Visual Design/Implementation in
the `$team-ui` pipeline.

**Run this skill:**
- After completing a UX spec with `$ux-design`
- Before handing off to `ui-programmer` or `art-director`
- Before the Pre-Production to Production gate check (which requires key screens
  to have reviewed UX specs)
- After major revisions to a UX spec

**Verdict levels:**
- **APPROVED** — every required author-profile check passed for the exact
  `target_sha256`. This conversation result is not persisted evidence and does
  not itself authorize implementation or handoff.
- **NEEDS REVISION** — specific gaps found; fix before handoff but not a full redesign
- **MAJOR REVISION NEEDED** — fundamental issues with scope, player need, or
  completeness; needs significant rework

---

## Phase 1: Parse Arguments

- **Specific file path** (e.g., `$ux-review design/ux/inventory.md`): validate
  that one document
- **`all`**: find all files in `design/ux/` and validate each
- **`hud`**: validate `design/ux/hud.md` specifically
- **`patterns`**: validate `design/ux/interaction-patterns.md` specifically
- **No argument**: ask the user which spec to validate

For `all`, output a summary table first (file | verdict | primary issue) then
full detail for each.

---

## Phase 2: Load Cross-Reference Context

Before validating any spec, load:

1. **Input & Platform config**: Read `.codex/docs/technical-preferences.md` and
   extract `## Input & Platform`. This is the authoritative source for which input
   methods the game supports — use it to drive the Input Method Coverage checks in
   Phase 3A, not the spec's own header. If unconfigured, fall back to the spec header.
2. The accessibility tier committed to in `design/accessibility-requirements.md`
   (if it exists)
3. The interaction pattern library at `design/ux/interaction-patterns.md` (if
   it exists)
4. The GDDs referenced in the spec's header (read their UI Requirements sections)
5. The player journey map at `design/player-journey.md` (if it exists) for
   context-arrival validation

---

## Phase 3A: UX Spec Validation Checklist

Run all checks against a `ux-spec.md`-based document.

### Completeness (required sections)

- [ ] Document header present with Status, Author, Platform Target
- [ ] Purpose & Player Need — has a player-perspective need statement (not
  developer-perspective)
- [ ] Player Context on Arrival — describes player's state and prior activity
- [ ] Navigation Position — shows where screen sits in hierarchy
- [ ] Entry & Exit Points — all entry sources and exit destinations documented
- [ ] Layout Specification — zones defined, component inventory table present
- [ ] States & Variants — at minimum: loading, empty/populated, and error states
  documented
- [ ] Interaction Map — covers all target input methods (check platform target
  in header)
- [ ] Data Requirements — every displayed data element has a source system and owner
- [ ] Events Fired — every player action has a corresponding event or null
  explanation
- [ ] Transitions & Animations — at least enter/exit transitions specified
- [ ] Accessibility Requirements — screen-level requirements present
- [ ] Localization Considerations — max character counts for text elements
- [ ] Acceptance Criteria — at least 5 specific testable criteria

### Quality Checks

**Player Need Clarity**
- [ ] Purpose is written from player perspective, not system/developer perspective
- [ ] Player goal on arrival is unambiguous ("The player arrives wanting to ___")
- [ ] The player context on arrival is specific (not just "they opened the
  inventory")

**Completeness of States**
- [ ] Error state is documented (not just happy path)
- [ ] Empty state is documented (no data scenario)
- [ ] Loading state is documented if the screen fetches async data
- [ ] Any state with a timer or auto-dismiss is documented with duration

**Input Method Coverage**
- [ ] If platform includes PC: keyboard-only navigation is fully specified
- [ ] If platform includes console/gamepad: d-pad navigation and face button
  mapping documented
- [ ] No interaction requires mouse-like precision on gamepad
- [ ] Focus order is defined (Question group order for keyboard, d-pad order for gamepad)

**Data Architecture**
- [ ] No data element has "UI" listed as the owner (UI must not own game state)
- [ ] Update frequency is specified for all real-time data (not just "realtime" —
  what triggers update?)
- [ ] Null handling is specified for all data elements (what shows when data is
  unavailable?)

**Accessibility**
- [ ] Accessibility tier from `accessibility-requirements.md` is matched or exceeded
- [ ] If Basic tier: no color-only information indicators
- [ ] If Standard tier+: focus order documented, text contrast ratios specified
- [ ] If Comprehensive tier+: screen reader announcements for key state changes
- [ ] Colorblind check: any color-coded elements have non-color alternatives

**GDD Alignment**
- [ ] Every GDD UI Requirement referenced in the header is addressed in this spec
- [ ] No UI element displays or modifies game state without a corresponding GDD
  requirement
- [ ] No GDD UI Requirement is missing from this spec (cross-check the referenced
  GDD sections)

**Pattern Library Consistency**
- [ ] All interactive components reference the pattern library (or note they are
  new patterns)
- [ ] No pattern behavior is re-specified from scratch if it already exists in
  the pattern library
- [ ] Any new patterns invented in this spec are flagged for addition to the
  pattern library

**Localization**
- [ ] Character limit warnings present for all text-heavy elements
- [ ] Any layout-critical text has been flagged for 40% expansion accommodation

**Acceptance Criteria Quality**
- [ ] Criteria are specific enough for a QA tester who hasn't seen the design docs
- [ ] Performance criterion present (screen opens within Xms)
- [ ] Resolution criterion present
- [ ] No criterion requires reading another document to evaluate

---

## Phase 3B: HUD Validation Checklist

Run all checks against a `hud-design.md`-based document.

### Completeness

- [ ] HUD Philosophy defined
- [ ] Information Architecture table covers ALL systems with UI Requirements in GDDs
- [ ] Layout Zones defined with safe zone margins for all target platforms
- [ ] Every HUD element has a full specification (zone, visibility trigger, data
  source, priority)
- [ ] HUD States by Gameplay Context covers at minimum: exploration, combat,
  dialogue/cutscene, paused
- [ ] Visual Budget defined (max simultaneous elements, max screen %)
- [ ] Platform Adaptation covers all target platforms
- [ ] Tuning Knobs present for player-adjustable elements

### Quality Checks

- [ ] No HUD element covers the center play area without a visibility rule to
  hide it
- [ ] Every information item that exists in any GDD is either in the HUD or
  explicitly categorized as "hidden/demand"
- [ ] All color-coded HUD elements have colorblind variants
- [ ] HUD elements in the Feedback & Notification section have queue/priority
  behavior defined
- [ ] Visual Budget compliance: total simultaneous elements is within budget

### GDD Alignment

- [ ] All systems in `design/gdd/systems-index.md` with UI category have
  representation in HUD (or justified absence)

---

## Phase 3C: Pattern Library Validation Checklist

- [ ] Pattern catalog index is current (matches actual patterns in document)
- [ ] All standard control patterns are specified: button variants, toggle,
  slider, dropdown, list, grid, modal, dialog, toast, tooltip, progress bar,
  input field, question group bar, scroll
- [ ] All game-specific patterns needed by current UX specs are present
- [ ] Each pattern has: When to Use, When NOT to Use, full state specification,
  accessibility spec, implementation notes
- [ ] Animation Standards table present
- [ ] Sound Standards table present
- [ ] No conflicting behaviors between patterns (e.g., "Back" behavior consistent
  across all navigation patterns)

---

## Phase 4: Output the Verdict

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & Player Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### GDD Alignment: [ALIGNED / GAPS FOUND]
- GDD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered GDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Review Status: COMPLETE / ERROR
### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED / null
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

[For APPROVED]: All required checks passed for the reported target hash. Return
the complete `ux-review-record-v1` with `gate_evidence_status: NOT_PERSISTED`.
Implementation or visual-design handoff requires a separate authorized consumer
to persist and revalidate current-hash evidence.

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run
`$ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas].
Recommend returning to `$ux-design` to rework [sections].
```

---

## Phase 5: Collaborative Protocol

This skill is READ-ONLY — it never edits or writes files. It reports findings only.

After delivering the verdict:
- For **APPROVED**: state that the conversation result remains `NOT_PERSISTED`;
  do not claim implementation readiness or recommend direct implementation
- For **NEEDS REVISION**: offer to help fix specific gaps ("Would you like me to
  help draft the missing error state?") — but do not auto-fix; wait for user
  instruction
- For **MAJOR REVISION NEEDED**: suggest returning to `$ux-design` with the
  specific sections to rework

The user controls whether to proceed, but the P0 review contract governs status.
Proceeding with open findings records ACCEPTED_RISK / NOT_APPROVED; it never
changes the original verdict or satisfies an approval gate.
