---
name: reverse-document
description: "Generate design or architecture documents from existing implementation. Works backwards from code/prototypes to create missing planning docs."
---

## Invocation and execution

Invoke this workflow as `$reverse-document`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `<type> <path> (e.g., 'design src/gameplay/combat' or 'architecture src/core')`. Treat bracketed values as optional unless the workflow says otherwise.


# Reverse Documentation

This skill analyzes existing implementation and generates appropriate design or
architecture documentation. Use it for an undocumented feature, inherited
codebase, prototype formalization, or the rationale behind existing code.

---

## Workflow

## Phase 1: Parse Arguments

**Required format**: `$reverse-document <type> <single-path>`

**Type options**:
- `design` → Generate a complete reverse-documented system GDD
- `architecture` → Generate an Architecture Decision Record (ADR)
- `concept` → Generate a concept document from a prototype

Reject a missing/unknown type, missing path, or more than one path with the
usage string above. One directory path may contain multiple relevant files; do
not accept multiple positional paths.

The resolved input must be one existing file or directory contained within the
project. Reject project-external paths. Within a directory, read only text source
or configuration files directly relevant to the selected type and applicable
AGENTS instructions. Skip generated output, binaries, and sensitive or denied
files. If no valid text input remains, stop with zero writes.

**Examples**:
```text
$reverse-document design src/gameplay/magic-system
$reverse-document architecture src/core/entity-component
$reverse-document concept prototypes/vehicle-combat
```

## Phase 2: Analyze Implementation

**For design docs (GDD):**
- Identify mechanics, rules, formulas, values, states, dependencies, and handled edge cases.

Detailed extraction:
- Identify mechanics, rules, and formulas.
- Extract gameplay values such as damage, cooldowns, and ranges.
- Find state machines, ability systems, and progression.
- Detect edge cases handled in code.
- Map dependencies and system interactions.

**For architecture docs (ADR):**
- Identify implemented patterns, technical constraints, dependencies, coupling,
  trade-offs, and performance characteristics.
- Do not turn a plausible alternative into decision history. Alternatives not
  evidenced by a contemporaneous artifact or explicitly confirmed by the user
  are labeled `Unknown` or `Possible alternative`; `why not chosen` remains
  `Unknown — not recorded`.

Detailed extraction:
- Identify patterns such as ECS, singleton, observer, or service locator.
- Map technical decisions in threading and serialization.
- Map dependencies and coupling.
- Assess evidenced performance characteristics.
- Record constraints and observed trade-offs.

**For concept docs (prototype analysis):**
- Identify the implemented core mechanic and technical feasibility evidence.
- Load prototype outcome, effort/duration, reuse percentage, tester feedback,
  and quotes only from an existing record or explicit user input. Otherwise use
  `N/A — source unavailable`; never invent a quote, tester count, percentage,
  outcome, or effort estimate.

Detailed extraction:
- Identify the core mechanic and emergent gameplay patterns.
- Note what existing records say worked or did not work.
- Capture technical feasibility evidence.
- Separate observed feel from intended player fantasy.

## Phase 3: Ask Clarifying Questions

Do not merely describe code; ask about intent. Clarifications are recorded as
user-stated intent and do not replace observed behavior.

**Design questions** may ask whether a resource supports pacing, whether a
mechanic is core, or whether discovered scaling is intentional.

Example prompts:
- "I see a resource that depletes during this activity. Is the intent pacing,
  strategic resource management, or something else?"
- "The mechanic appears central in code. Is it a core pillar or supporting feature?"
- "This value scales exponentially. Is that intentional, or a gap to a desired curve?"

**Architecture questions** may ask why an observed pattern was chosen, but do
not present unrecorded alternatives as choices previously considered.

Example prompts:
- "The implementation uses a service locator. What rationale, if any, was
  recorded for that choice?"
- "Manual memory management appears here. Is there a confirmed performance
  constraint, or is the rationale unknown?"

**Concept questions** may ask about intended pillars, emergent behavior, or
whether existing playtest/effort records exist.

Example prompts:
- "The prototype emphasizes stealth over combat. Is that the intended pillar?"
- "Is there an existing playtest or time-tracking record I should use, or
  should those fields remain N/A?"

## Phase 4: Present Findings

Before drafting, show discovered mechanics, formulas, architecture, prototype
evidence, and unclear intent areas with source paths. Wait for clarification.

Use a findings presentation such as:

```text
I've analyzed [path].

MECHANICS IMPLEMENTED:
- [mechanic] with [evidenced property]

FORMULAS DISCOVERED:
- [output] = [formula]

UNCLEAR INTENT AREAS:
1. [resource/system question]
2. [pillar question]
3. [observed-versus-intended value question]
```

## Phase 5: Draft Document Using Template

| Type | Template | Output Path |
|------|----------|-------------|
| `design` | `.codex/docs/templates/design-doc-from-implementation.md` | `design/gdd/[system-name].md` |
| `architecture` | `.codex/docs/templates/architecture-doc-from-code.md` | `docs/architecture/[decision-name].md` |
| `concept` | `.codex/docs/templates/concept-doc-from-prototype.md` | `prototypes/[name]/CONCEPT.md` or `design/concepts/[name].md` |

If the selected template is absent, stop; do not invent a replacement structure.

Draft rules:

- Put code/test-backed facts under **Observed implementation**.
- Put clarified future or desired behavior under **User-stated intent**.
- Put every difference under **Gap**; intent never rewrites observed state.
- Mark an Acceptance Criterion implemented only when code/test evidence proves it.
- When the user has not supplied `Verified By`, `Decision Makers`, `Creator`,
  or author identity, keep the template's `pending review` / `unknown` value.
- In an ADR, unconfirmed alternatives and rejection rationales remain possible
  or unknown rather than historical facts.
- In a concept document, unavailable outcome, effort, reuse, and playtest fields
  are `N/A — source unavailable`.

Flag follow-up work such as balance tuning or missing features, but keep it
outside observed implementation and do not apply it during this workflow.

## Phase 6: Show Draft and Request Approval

Show the entire proposed document, including metadata, appendices, incomplete
fields, and every section that will be written. Do not abbreviate the preview to
key sections. For a new design GDD, also show the complete proposed systems-index
row update. Let the user request draft changes before the one complete changeset
authorization.

Identify additions made from user clarification and sections marked incomplete,
but this summary supplements rather than replaces the full draft.

## Phase 7: Write Document with Metadata

Before requesting write authorization, resolve the exact output target and check
whether it exists. If it exists, read it and offer a targeted update or stop;
never overwrite it silently.

Use metadata without guessing identity:

```markdown
---
status: reverse-documented
source: [path/]
date: [today]
verified-by: [explicit user-provided identity or pending review]
---
```

For a new design GDD, also update the existing
`design/gdd/systems-index.md` corresponding row in the same changeset. If no
unique existing system row can be identified, stop and ask the user to select
an existing system rather than inventing a new system decision. Preview the
new/updated document and index edit together.

The written file retains the template's reverse-documentation notice and
evidence-boundary sections.

## Phase 8: Flag Follow-Up Work

After writing, list evidence gaps, document gaps, and relevant existing commands
such as `$balance-check`, `$architecture-decision`, or `$code-review`. End the
workflow after that list. Do not ask to tackle a follow-up immediately and do
not edit code, another GDD, or an ADR under this workflow's authorization.

Example handoff list:

```text
Written to: [resolved output path]

FOLLOW-UP RECOMMENDED (not executed):
1. $balance-check [document] — validate discovered formulas
2. $architecture-decision — document a still-unrecorded decision
3. Implement the listed observed-versus-intended gaps
```

---

## Template Selection Logic

| If analyzing... | Use template... | Because... |
|----------------|-----------------|------------|
| `src/gameplay/*` | design-doc-from-implementation.md | Gameplay mechanics → GDD |
| `src/core/*`, `src/ai/*` | architecture-doc-from-code.md | Core systems → ADR |
| `prototypes/*` | concept-doc-from-prototype.md | Experiments → concept doc |
| `src/networking/*` | architecture-doc-from-code.md | Technical systems → ADR |
| `src/ui/*` | design-doc-from-implementation.md | UI/UX → design spec |

---

## Example Session: Reverse-Document a System

```text
User: $reverse-document design src/gameplay/[system]

Agent: [Analyzes implementation and shows observed mechanics/formulas.]
       [Asks what the resource, mechanic, and discovered scaling were intended to do.]

User: The implemented exponential scaling should become linear.

Agent: [Shows the complete draft. The exponential rule remains Observed
       implementation, linear scaling is User-stated intent, and their
       difference is a Gap.]

User: Approves the complete changeset.

Agent: Writes the previewed document and lists later commands; no follow-up
       workflow runs automatically.
```

---

## Collaborative Protocol

1. **Analyze First**: Read code and understand implementation.
2. **Question Intent**: Ask about why, not only what.
3. **Present Findings**: Show discoveries and unclear areas.
4. **User Clarifies**: Separate intent from accidents.
5. **Draft Document**: Preserve reality, intent, and gaps separately.
6. **Show Full Draft**: Display all content that will be written.
7. **Get Approval**: Preview the complete files once, then write only the
   authorized changeset. Return **COMPLETE** after writing or **BLOCKED — user
   declined write** on decline.
8. **Flag Follow-Up**: Suggest related commands, do not auto-execute them.

**Never assume intent or identity. Never fabricate prototype evidence or
decision history.**
