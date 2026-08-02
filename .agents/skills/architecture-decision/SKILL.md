---
name: architecture-decision
description: "Creates an Architecture Decision Record (ADR) documenting a significant technical decision, its context, alternatives considered, and consequences. Every major technical choice should have an ADR."
---

## Invocation and execution

Invoke this workflow as `$architecture-decision`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[title] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


When this skill is invoked:

## 0. Parse Arguments — Detect Retrofit Mode

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

**If the argument starts with `retrofit` followed by a file path**
(e.g., `$architecture-decision retrofit docs/architecture/adr-0001-event-system.md`):

Before entering retrofit mode, require exactly one normalized path to an existing
project-local Markdown file matching `docs/architecture/adr-*.md`. Reject missing,
multiple, directory, non-Markdown, project-external, and non-ADR paths without
writing or producing a retrofit draft.

Enter **retrofit mode**:

1. Read the existing ADR file and `.codex/docs/templates/architecture-decision-record.md` completely.
2. Compare the ADR against the complete template in template order: title, Status,
   Date, Last Verified, Decision Makers, Summary, Engine Compatibility, ADR
   Dependencies, Context, Decision, Alternatives Considered, Consequences, Risks,
   Performance Implications, Migration Plan, Validation Criteria, GDD Requirements
   Addressed, and Related. For each item distinguish valid content, missing content,
   placeholder content, and illegal values. Missing required Title, Status, Context,
   Decision, or Consequences is BLOCKING; do not treat a present placeholder as valid.
3. Present to the user:
   ```
   ## Retrofit: [ADR title]
   File: [path]

   Valid content that will be preserved:
   ✓ [section]: [current non-placeholder value]

   Repairs shown in template order:
   ✗ [missing section] — [severity]
   ✗ [placeholder section] — replace placeholder with confirmed content
   ✗ Status: [illegal value] — replace with a valid lifecycle value
   ```
4. Ask: "Should the revised draft include these [N] template repairs? Valid existing content will remain unchanged."
5. If the user includes them in scope:
   - For **Status**: ask the user — "What is the current status of this decision?"
     Options: "Proposed", "Accepted", "Superseded". If Superseded, capture the replacement ADR separately in Related.
   - For **ADR Dependencies**: ask — "Does this decision depend on any other ADR?
     Does it enable or block any other ADR or epic?" Accept "None" for each field.
   - For **Engine Compatibility**: read the engine reference docs (same as Step 1 below)
     and ask the user to confirm the domain. Then generate the table with verified data.
   - For **GDD Requirements Addressed**: ask — "Which GDD systems motivated this decision?
     What specific requirement in each GDD does this ADR address?"
   - Build one complete revised draft in the exact template order. Insert missing
     sections at their template positions and replace only placeholders or illegal
     values; preserve every valid existing section verbatim.
6. Preview the complete revised ADR and obtain the normal single changeset approval
   before writing it. Do not append all repairs to the end of the file.
7. Suggest: "Run `$architecture-review` to re-validate coverage now that this ADR
   has its Status and Dependencies fields."

If NOT in retrofit mode, proceed to Step 1 below (normal ADR authoring).

**No-argument guard**: If no argument was provided (title is empty), ask before
running Phase 0:

> "What technical decision are you documenting? Please provide a short title
> (e.g., `event-system-architecture`, `physics-engine-choice`)."

Use the user's response as the title, then proceed to Step 1.

---

## 1. Load Engine Context (ALWAYS FIRST)

Before doing anything else, establish the engine environment:

1. Read `docs/engine-reference/[engine]/VERSION.md` to get:
   - Engine name and version
   - LLM knowledge cutoff date
   - Post-cutoff version risk levels (LOW / MEDIUM / HIGH)

2. Identify the **domain** of this architecture decision from the title or
   user description. Common domains: Physics, Rendering, UI, Audio, Navigation,
   Animation, Networking, Core, Input, Scripting.

3. Read the corresponding module reference if it exists:
   `docs/engine-reference/[engine]/modules/[domain].md`

4. Read `docs/engine-reference/[engine]/breaking-changes.md` — flag any
   changes in the relevant domain that post-date the LLM's training cutoff.

5. Read `docs/engine-reference/[engine]/deprecated-apis.md` — flag any APIs
   in the relevant domain that should not be used.

6. **Display a knowledge gap warning** before proceeding if the domain carries
   MEDIUM or HIGH risk:

   ```
   ⚠️  ENGINE KNOWLEDGE GAP WARNING
   Engine: [name + version]
   Domain: [domain]
   Risk Level: HIGH — This version is post-LLM-cutoff.

   Key changes verified from engine-reference docs:
   - [Change 1 relevant to this domain]
   - [Change 2]

   This ADR will be cross-referenced against the engine reference library.
   Proceed with verified information only — do NOT rely solely on training data.
   ```

   If no engine has been configured yet, stop this run with: "No engine is
   configured. Run `$setup-engine` first, or provide the engine and confirm that
   its existing `docs/engine-reference/[engine]/VERSION.md` can be located."
   Continue only after that existing reference is readable; never label
   unverified compatibility information as verified.

---

## 2. Determine the next ADR number

Before allocating a number, scan existing ADR titles, domains, Summary sections,
and related-decision links for the same decision. If a likely duplicate exists,
show it and let the user update that ADR or explicitly supersede it; do not
silently allocate a second ADR for the same decision.

If a new ADR is still required, scan `docs/architecture/` for existing ADRs to
find the next number. Treat this as a provisional filename until the write-time
recheck in Step 6.

---

## 3. Gather context

Read related code, existing ADRs, and relevant GDDs from `design/gdd/`.

### 3a: Architecture Registry Check (BLOCKING gate)

Read `docs/registry/architecture.yaml`. If it is missing, unreadable YAML, or
lacks the expected existing sections, stop this blocking check and explain the
exact problem. If the user explicitly skips the registry check, continue only
with a visible `Registry constraints not checked` limitation and never call the
blocking check passed.

Extract entries relevant to this ADR's domain and decision (search by system
name, domain keyword, or state being touched).

Present any relevant stances to the user **before** the collaborative design
begins, as locked constraints:

```
## Existing Architectural Stances (must not contradict)

State Ownership:
  player_health → owned by health-system (ADR-0001)
  Interface: HealthComponent.current_health (read-only float)
  → If this ADR reads or writes player health, it must use this interface.

Interface Contracts:
  damage_delivery → signal pattern (ADR-0003)
  Signal: damage_dealt(amount, target, is_crit)
  → If this ADR delivers or receives damage events, it must use this signal.

Forbidden Patterns:
  ✗ autoload_singleton_coupling (ADR-0001)
  ✗ direct_cross_system_state_write (ADR-0000)
  → The proposed approach must not use these patterns.
```

If the user's proposed decision would contradict any registered stance, surface
the conflict immediately:

> "⚠️ Conflict: This ADR proposes [X], but ADR-[NNNN] established that [Y] is
> the accepted pattern for this purpose. Proceeding without resolving this will
> produce contradictory ADRs and inconsistent stories.
> Options: (1) Align with the existing stance, (2) Supersede ADR-[NNNN] with
> an explicit replacement, (3) Explain why this case is an exception."

Do not proceed to Step 4 (collaborative design) until any conflict is resolved
or explicitly accepted as an intentional exception.

---

## 4. Guide the decision collaboratively

Before asking anything, derive the skill's best guesses from the context already
gathered (GDDs read, engine reference loaded, existing ADRs scanned). Then present
a **confirm/adjust** prompt by asking the user directly — not open-ended questions.

**Derive assumptions first:**
- **Problem**: Infer from the title + GDD context what decision needs to be made
- **Alternatives**: Propose 2-3 concrete options from engine reference + GDD requirements
- **Dependencies**: Scan existing ADRs for upstream dependencies; assume None if unclear
- **GDD linkage**: Extract which GDD systems the title directly relates to
- **Status**: Always `Proposed` for new ADRs — never ask the user what the status is

**Scope of assumptions question group**: Assumptions cover only: problem framing, alternative approaches, upstream dependencies, GDD linkage, and status. Schema design questions (e.g., "How should spawn timing work?", "Should data be inline or external?") are NOT assumptions — they are design decisions belonging to a separate step after the assumptions are confirmed. Do not include schema design questions in the assumptions structured choice prompt.

**After assumptions are confirmed**, if the ADR involves schema or data design choices, use a separate grouped set of questions presented directly to the user to ask each design question independently before drafting.

**Present assumptions by asking the user directly:**

```
Here's what I'm assuming before drafting:

Problem: [one-sentence problem statement derived from context]
Alternatives I'll consider:
  A) [option derived from engine reference]
  B) [option derived from GDD requirements]
  C) [option from common patterns]
GDD systems driving this: [list derived from context]
Dependencies: [upstream ADRs if any, otherwise "None"]
Status: Proposed

[A] Proceed — draft with these assumptions
[B] Change the alternatives list
[C] Adjust the GDD linkage
[D] Add a performance budget constraint
[E] Something else needs changing first
```

Do not generate the ADR until the user confirms assumptions or provides corrections.

**After engine specialist and TD reviews return** (Step 5.5/5.6), if unresolved
decisions remain, present each one as a separate a direct question to the user with the proposed
options as choices plus a free-text escape:

```
Decision: [specific unresolved point]
[A] [option from specialist review]
[B] [alternative option]
[C] Different approach — I'll describe it
```

**ADR Dependencies** — derive from existing ADRs, then confirm:
- Does this decision depend on any other ADR not yet Accepted?
- Does it unlock or unblock any other ADR or epic?
- Does it block any specific epic from starting?

Record answers in the **ADR Dependencies** section. Write "None" for each field if no constraints apply.

---

## 5. Generate the ADR

Following this format:

```markdown
# ADR-[NNNN]: [Title]

## Status
[Proposed | Accepted | Superseded]

## Date
[Date of decision]

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | [e.g. Godot 4.6] |
| **Domain** | [Physics / Rendering / UI / Audio / Navigation / Animation / Networking / Core / Input] |
| **Knowledge Risk** | [LOW / MEDIUM / HIGH — from VERSION.md] |
| **References Consulted** | [List engine-reference docs read, e.g. `docs/engine-reference/godot/modules/physics.md`] |
| **Post-Cutoff APIs Used** | [Any APIs from post-LLM-cutoff versions this decision depends on, or "None"] |
| **Verification Required** | [Specific behaviours to test before shipping, or "None"] |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | [ADR-NNNN (must be Accepted before this can be implemented), or "None"] |
| **Enables** | [ADR-NNNN (this ADR unlocks that decision), or "None"] |
| **Blocks** | [Epic/Story name — cannot start until this ADR is Accepted, or "None"] |
| **Ordering Note** | [Any sequencing constraint that isn't captured above] |

## Context

### Problem Statement
[What problem are we solving? Why does this decision need to be made now?]

### Constraints
- [Technical constraints]
- [Timeline constraints]
- [Resource constraints]
- [Compatibility requirements]

### Requirements
- [Must support X]
- [Must perform within Y budget]
- [Must integrate with Z]

## Decision

[The specific technical decision made, described in enough detail for someone
to implement it.]

### Architecture Diagram
[ASCII diagram or description of the system architecture this creates]

### Key Interfaces
[API contracts or interface definitions this decision creates]

## Alternatives Considered

### Alternative 1: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

### Alternative 2: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

## Consequences

### Positive
- [Good outcomes of this decision]

### Negative
- [Trade-offs and costs accepted]

### Risks
- [Things that could go wrong]
- [Mitigation for each risk]

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| [system-name].md | [specific rule, formula, or performance constraint from that GDD] | [how this decision satisfies it] |

## Performance Implications
- **CPU**: [Expected impact]
- **Memory**: [Expected impact]
- **Load Time**: [Expected impact]
- **Network**: [Expected impact, if applicable]

## Migration Plan
[If this changes existing code, how do we get from here to there?]

## Validation Criteria
[How will we know this decision was correct? What metrics or tests?]

## Related Decisions
- [Links to related ADRs]
- [Links to related design documents]
```

5.5. **Engine Specialist Validation** — Before saving, spawn the **primary engine specialist** through Codex subagent delegation to validate the drafted ADR:
   - Read `docs/technical-preferences.md` `Engine Specialists` section to get the primary specialist
   - If no engine is configured (`[TO BE CONFIGURED]`), skip this step
   - Spawn `subagent_type: [primary specialist]` with: the ADR's Engine Compatibility section, Decision section, Key Interfaces, and the engine reference docs path. Ask them to:
     1. Confirm the proposed approach is idiomatic for the pinned engine version
     2. Flag any APIs or patterns that are deprecated or changed post-training-cutoff
     3. Identify engine-specific risks or gotchas not captured in the current ADR draft
   - If the specialist identifies a **blocking issue** (wrong API, deprecated approach, engine version incompatibility): place the proposed Decision and Engine Compatibility changes in the visible draft, then confirm them with the user before proceeding
   - If the specialist finds **minor notes** only: place the proposed Risks text in the same visible draft and obtain the same user confirmation before treating it as accepted content
   - No specialist result, regardless of severity, may silently change a user-confirmed decision

**Review mode check** — apply before spawning TD-ADR:
- `solo` → skip. Note: "TD-ADR skipped — Solo mode." Proceed to Step 5.7 (GDD sync check).
- `lean` → skip (not a PHASE-GATE). Note: "TD-ADR skipped — Lean mode." Proceed to Step 5.7 (GDD sync check).
- `full` → spawn as normal.

5.6. **Technical Director Strategic Review** — After the engine specialist validation, spawn `technical-director` through Codex subagent delegation using gate **TD-ADR** (`.codex/docs/director-gates.md`):
   - Pass: the ADR file path (or draft content), engine version, domain, any existing ADRs in the same domain
   - The TD validates architectural coherence (is this decision consistent with the whole system?) — distinct from the engine specialist's API-level check
   - APPROVE: continue.
   - If CONCERNS: show every concern and ask the user whether to accept the risk, revise the draft, or stop. If revised, run TD-ADR again before proceeding.
   - If REJECT: stop with no writes. Return to the existing drafting step, revise, and run TD-ADR again; a rejected draft cannot enter the changeset preview.

5.7. **GDD Sync Check** — Before presenting the single changeset approval, scan all GDDs
referenced in the "GDD Requirements Addressed" section for naming inconsistencies
with the ADR's Key Interfaces and Decision sections (renamed signals, API methods,
or data types). If any are found, surface them as a **prominent warning block** and show, for
each GDD, the current text and exact proposed replacement text immediately before
the single changeset approval — not as a footnote. If exact edits cannot be
shown, the selectable changeset may include the ADR only, not a GDD edit:

```
⚠️ GDD SYNC REQUIRED
[gdd-filename].md uses names this ADR has renamed:
  [old_name] → [new_name_from_adr]
  [old_name_2] → [new_name_2_from_adr]
The GDD must be updated before or alongside writing this ADR to prevent
developers reading the GDD from implementing the wrong interface.
```

If no inconsistencies: skip this block silently.

5. **Prepare the complete changeset** — Record whether the user wants the ADR
alone or the ADR plus the displayed GDD synchronization edits. Do not write yet.
Continue to Step 6 so registry candidates and any story status edits are known
before the one changeset preview.

6. **Update Architecture Registry**

Scan the complete ADR draft for new architectural stances that should be registered:
- State it claims ownership of
- Interface contracts it defines (signal signatures, method APIs)
- Performance budget it claims
- API choices it makes explicitly
- Patterns it bans (Consequences → Negative or explicit "do not use X")

Present candidates:
```
Registry candidates from this ADR:
  NEW state ownership:      player_stamina → stamina-system
  NEW interface contract:   stamina_depleted signal
  NEW performance budget:   stamina-system: 0.5ms/frame
  NEW forbidden pattern:    polling stamina each frame (use signal instead)
  EXISTING (referenced_by update only): player_health → already registered ✅
```

**Registry append logic**: When writing to `docs/registry/architecture.yaml`, do NOT assume sections are empty. The file may already have entries from previous ADRs written in this session. Before each Edit call:
1. Read the current state of `docs/registry/architecture.yaml`
2. Find the correct section (state_ownership, interfaces, forbidden_patterns, api_decisions)
3. Append the new entry AFTER the last existing entry in that section — do not try to replace a `[]` placeholder that may no longer exist
4. If the section has entries already, use the closing content of the last entry as the `old_string` anchor, and append the new entry after it

**BLOCKING — do not write to `docs/registry/architecture.yaml` without explicit user approval.**

Ask by asking the user directly:
- Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
  - Options: "Yes — update the registry", "Not yet — I want to review the candidates", "Skip registry update"

Before approval, scan for stories whose top-level Status is `Blocked` specifically
because of this ADR. Show each exact proposed `Blocked` → `Ready` edit and let the
user include or exclude it; never change unrelated blocked stories.

Immediately before presenting the complete changeset, re-scan
`docs/architecture/adr-*.md`. If the provisional number or filename is now occupied,
recalculate it, update every affected draft/reference, and re-present the changed
filename and content; never overwrite the occupied file.

Now present one complete changeset containing the full ADR draft and every selected
GDD, registry, and story edit. List every target file and exact modification. Obtain
one explicit approval, then apply all selected writes continuously. If approval is
withheld, none of these files changes.

If the registry update is included in the authorized changeset, append new entries.
When a stance changes, update the old entry to the existing single-value form
`status: superseded` and add the replacement as a new entry whose `adr` points to
ADR-[NNNN]. Do not emit the ambiguous YAML value `status: superseded_by: ...`.

---

## 6. Closing Next Steps

After the ADR is written (and registry optionally updated), close by asking the user directly.

Before generating the structured prompt:
1. Read `docs/registry/architecture.yaml` — check if any priority ADRs are still unwritten (look for ADRs flagged in technical-preferences.md or systems-index.md as prerequisites)
2. Check if all prerequisite ADRs are now written. If yes, include a "Start writing GDDs" option.
3. List ALL remaining priority ADRs as individual options — not just the next one or two.

Structured prompt format:
```
ADR-[NNNN] written and registry updated. What would you like to do next?
[1] Write [next-priority-adr-name] — [brief description from prerequisites list]
[2] Write [another-priority-adr] — [brief description]  (include ALL remaining ones)
[N] Start writing GDDs — run `$design-system [first-undesigned-system]` (only show if all prerequisite ADRs are written)
[N+1] Stop here for this session
```

If there are no remaining priority ADRs and no undesigned GDD systems, offer only "Stop here" and suggest running `$architecture-review` in a fresh session.

**Always include this fixed notice in the closing output (do NOT omit it):**

> To validate ADR coverage against your GDDs, open a **fresh Codex session**
> and run `$architecture-review`.
>
> **Never run `$architecture-review` in the same session as `$architecture-decision`.**
> The reviewing agent must be independent of the authoring context to give an unbiased
> assessment. Running it here would invalidate the review.
