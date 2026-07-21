---
name: create-control-manifest
description: "After architecture is complete, produces a source-faithful control sheet for programmers that preserves MUST/SHOULD/MAY strength, keeps contextual rejections distinct from explicit prohibitions, and requires independent hash-bound review."
---

## Invocation and execution

Invoke this workflow as `$create-control-manifest`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[update — regenerate from current ADRs]`. Treat bracketed values as optional unless the workflow says otherwise.

The current agent is the extraction author. Do not delegate source parsing, rule
normalization, preview assembly, or manifest drafting to the reviewer. Record the
author's stable runtime instance identifier (for example, the Codex task name or
agent ID exposed by the runtime); never invent an identifier.

After the draft is stable, use a fresh `technical-director` Codex subagent instance
only as the independent, read-only reviewer described in Phase 4b. The reviewer
must not edit the extraction, draft, sources, or manifest. The author and reviewer
instance identifiers must differ. If either identifier is unavailable, the
identifiers match, or an independent reviewer cannot be created, do not self-sign
or publish an Active manifest; report Verdict: **BLOCKED** with the reason.


# Create Control Manifest

The Control Manifest is a flat, actionable rules sheet for programmers. It shows
what is mandatory, recommended, optional, explicitly prohibited, or merely a
contextual rejection — organized by architectural layer and extracted from all
Accepted ADRs, technical preferences, and engine reference docs. Where ADRs
explain *why*, the manifest preserves *what* they actually require or allow.

**Output:** `docs/architecture/control-manifest.md`

**When to run:** After `$architecture-review` passes and ADRs are in Accepted
status. Re-run whenever new ADRs are accepted or existing ADRs are revised.

---

## 1. Load All Inputs

### ADRs
- Find files matching `docs/architecture/adr-*.md` and read every file
- Filter to only Accepted ADRs (Status: Accepted) — skip Proposed, Deprecated,
  Superseded
- Note the ADR number and title for every rule sourced

### Technical Preferences
- Read `.codex/docs/technical-preferences.md`
- Extract: naming conventions, performance budgets, approved libraries/addons,
  forbidden patterns

### Engine Reference
- Read `docs/engine-reference/[engine]/VERSION.md` for engine + version
- Read `docs/engine-reference/[engine]/deprecated-apis.md` — these become
  forbidden API entries
- Read `docs/engine-reference/[engine]/current-best-practices.md` if it exists

Report: "Loaded [N] Accepted ADRs, engine: [name + version]."

---

## 2. Extract Rules from Each ADR

The current agent performs this extraction directly. Apply the following
deterministic normalization rules to every source; the source's normative strength
and scope are authoritative:

### Normative Rules (primarily from "Implementation Guidelines")

Preserve RFC 2119 strength rather than collapsing rules into a single required
bucket. Match the listed terms case-insensitively when they are used normatively;
do not treat an ordinary descriptive use of the same word as a normative rule:

| Source wording | Manifest level | Treatment |
|---|---|---|
| `MUST`, `REQUIRED`, `SHALL`, `required to`, or an explicit mandate | **MUST** | Mandatory rule |
| `MUST NOT` or `SHALL NOT` | **MUST NOT** | Mandatory negative rule; do not relabel it as a rejected alternative |
| `SHOULD` or `RECOMMENDED` | **SHOULD** | Recommendation; never rewrite as `MUST`, `required`, or `always` |
| `SHOULD NOT` or `NOT RECOMMENDED` | **SHOULD NOT** | Negative recommendation; never rewrite as forbidden |
| `MAY` or `OPTIONAL` | **MAY** | Permitted option; never rewrite as required |
| No explicit normative wording, or ambiguous wording | none | Do not create a normative rule; add an ambiguity review finding with the source location |

- Preserve the source scope and conditions verbatim enough that the rule cannot
  apply more broadly than the ADR states.
- Preserve the original meaning. Minimal grammatical normalization is allowed,
  but do not introduce stronger verbs or delete qualifications.
- If one sentence contains multiple levels, split it into separately leveled
  rules without changing their shared conditions.

### Forbidden Approaches and Contextual Rejections

- Put an alternative from "Alternatives Considered" into **Forbidden
  Approaches** only when the ADR explicitly calls that alternative `forbidden` or
  `prohibited`. Preserve the stated scope and conditions.
- A rejected, not-selected, deferred, or lower-ranked alternative is not a global
  prohibition. Record it under **Contextual Rejections** with the alternative,
  reason, ADR-local scope, and any conditions under which it could be reconsidered.
- Keep explicit anti-pattern language at its source strength. If the source does
  not explicitly say `forbidden` or `prohibited`, do not manufacture `never`.
- When wording is unclear about whether an item is prohibited, keep it out of the
  forbidden list and add an ambiguity review finding.

### Performance Guardrails (from "Performance Implications" section)
- Budget constraints: "max N ms per frame for this system"
- Memory limits: "this system must not exceed N MB"

### Engine API Constraints (from "Engine Compatibility" section)
- Post-cutoff APIs that require verification
- Verified behaviours that differ from default LLM assumptions
- API fields or methods that behave differently in the pinned engine version

### Layer Classification
Classify each rule by the architectural layer of the system it governs:
- **Foundation**: Scene management, event architecture, save/load, engine init
- **Core**: Core gameplay loops, main player systems, physics/collision
- **Feature**: Secondary systems, secondary mechanics, AI
- **Presentation**: Rendering, audio, UI, VFX, shaders

If an ADR spans multiple layers, duplicate the rule into each relevant layer only
when the ADR's own scope covers those layers. Duplicating a rule must not broaden
its scope or change its level.

---

## 3. Add Global Rules

Combine rules that apply to all layers:

### From technical-preferences.md:
- Naming conventions (classes, variables, signals/events, files, constants)
- Performance budgets (target framerate, frame budget, draw call limits, memory ceiling)

### From deprecated-apis.md:
- All deprecated APIs → Forbidden API entries

### From current-best-practices.md (if available):
- Preserve the source level for engine-recommended patterns. `SHOULD` remains
  **SHOULD**, `MAY` remains **MAY**, and non-normative guidance is not promoted to
  a required entry.

### From technical-preferences.md forbidden patterns:
- Copy any "Forbidden Patterns" entries directly

---

## 4. Present Rules Summary Before Writing

Before writing the manifest, present a summary to the user:

```
## Control Manifest Preview
Engine: [name + version]
ADRs covered: [list ADR numbers]
Total rules extracted:
  - Foundation layer: [N] MUST/MUST NOT, [S] SHOULD/SHOULD NOT, [O] MAY, [M] explicitly forbidden, [C] contextual rejections, [P] guardrails
  - Core layer: [N] MUST/MUST NOT, [S] SHOULD/SHOULD NOT, [O] MAY, [M] explicitly forbidden, [C] contextual rejections, [P] guardrails
  - Feature layer: ...
  - Presentation layer: ...
  - Global: [N] naming conventions, [M] forbidden APIs, [P] approved libraries
Ambiguity findings: [count and source locations]
Extraction author instance: [stable runtime identifier]
```

Ask the user directly:
- Prompt: "Does this rule summary look complete?"
- Options:
  - `[A] Yes — looks good, run the independent read-only review`
  - `[B] Correct source mapping — I found an extraction or source-strength error`
  - `[C] Review ambiguity findings — resolve them in the source ADR or leave them out`
  - `[D] Stop here — I need to review the ADRs first`

Any requested correction must trace to a loaded source. Do not add an unsourced
rule, omit a source-mandated rule, or change its normative level merely because a
user prefers different manifest wording; revise the authoritative source first.

---

## 4b. Independent Read-Only Technical Review

This is a mandatory integrity review, not a configurable director gate. Do not
read `production/review-mode.txt`, do not apply `solo`/`lean`/`full`, and do not
delegate any authoring work to the reviewer.

Before spawning the reviewer, build a deterministic review payload containing:

1. the complete proposed manifest content except the review-outcome metadata;
2. a path-sorted inventory of every included and excluded input with its SHA-256;
3. all ambiguity findings and the full extracted rule list; and
4. the extraction author's stable runtime instance identifier.

Serialize text as UTF-8 with LF line endings and paths in repository-relative
POSIX form, then compute the SHA-256 of the exact payload. Record this as the
**Review Input Hash**. Any rule, level, scope, source inventory, or finding change
creates a new payload and requires a new review.

Spawn a fresh `technical-director` Codex subagent instance as a read-only reviewer.
Pass the exact review payload and its hash. Require the reviewer to return:

- reviewer instance identifier;
- received review-input hash;
- **APPROVE**, **CONCERNS [list]**, or **REJECT [blockers]**;
- confirmation that no files or draft content were modified.

The reviewer checks whether:

- every `MUST`/`SHOULD`/`MAY` and negative form retains source strength and scope;
- only alternatives explicitly called `forbidden` or `prohibited` appear in
  Forbidden Approaches;
- ordinary rejected alternatives remain contextual and retain their reasons and
  conditions;
- no rule lacks a source and all ambiguity findings are visible; and
- performance guardrails are consistent with the source constraints.

Validate the response before applying it:

- The reviewer identifier must be present and differ from the author identifier.
- The received hash must exactly equal the current Review Input Hash.
- Missing identity, matching identity, hash mismatch, reviewer mutation, or an
  unavailable independent reviewer yields Verdict: **BLOCKED**. Do not self-review,
  do not accept a substituted identity, and do not write an Active manifest.
- **APPROVE** with valid identity and hash may proceed to Phase 5.
- **CONCERNS** must be resolved and re-reviewed. User acceptance cannot waive
  source-fidelity or reviewer-independence concerns.
- **REJECT** must be fixed and re-reviewed; do not write the manifest.

---

## 5. Write the Control Manifest

Ask the user directly:
- Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
- Options:
  - `[A] Yes — write to docs/architecture/control-manifest.md`
  - `[B] Show me the full draft first, then ask again`
  - `[C] Not yet — I want to make more changes`

Format:

```markdown
# Control Manifest

> **Engine**: [name + version]
> **Last Updated**: [date]
> **Manifest Version**: [date]
> **ADRs Covered**: [ADR-NNNN, ADR-MMMM, ...]
> **Status**: [Active — regenerate with `$create-control-manifest update` when ADRs change]
> **Extraction Author Instance**: [stable runtime identifier]
> **Independent Reviewer Instance**: [different stable runtime identifier]
> **Review Input SHA-256**: [hash approved by the reviewer]
> **Independent Review**: [APPROVE]

`Manifest Version` is the date this manifest was generated. Story files embed
this date when created. `$story-readiness` compares a story's embedded version
to this field to detect stories written against stale rules. Always matches
`Last Updated` — they are the same date, serving different consumers.

This manifest is a programmer's quick-reference extracted from all Accepted ADRs,
technical preferences, and engine reference docs. Rule levels preserve source
normative strength: **MUST/MUST NOT** are mandatory, **SHOULD/SHOULD NOT** are
recommendations, and **MAY** is optional. Contextual rejections explain why an
alternative was not selected but are not prohibitions. For the reasoning behind
each rule, see the referenced ADR.

---

## Foundation Layer Rules

*Applies to: scene management, event architecture, save/load, engine initialisation*

### Normative Rules
| Level | Rule and preserved conditions | Source |
|---|---|---|
| MUST | [mandatory rule] | [ADR-NNNN, section] |
| SHOULD | [recommendation] | [ADR-NNNN, section] |
| MAY | [optional pattern] | [ADR-NNNN, section] |

### Forbidden Approaches
- **[explicitly forbidden/prohibited approach]** — [preserved scope and reason] — source: [ADR-NNNN, section]

### Contextual Rejections
- **[alternative not selected]** — reason: [source reason]; scope: [ADR-local scope]; reconsider when: [conditions or "not stated"] — source: [ADR-NNNN, section]

### Performance Guardrails
- **[system]**: max [N]ms/frame — source: [ADR-NNNN]

---

## Core Layer Rules

*Applies to: core gameplay loop, main player systems, physics, collision*

### Normative Rules
...

### Forbidden Approaches
...

### Contextual Rejections
...

### Performance Guardrails
...

---

## Feature Layer Rules

*Applies to: secondary mechanics, AI systems, secondary features*

### Normative Rules
...

### Forbidden Approaches
...

### Contextual Rejections
...

---

## Presentation Layer Rules

*Applies to: rendering, audio, UI, VFX, shaders, animations*

### Normative Rules
...

### Forbidden Approaches
...

### Contextual Rejections
...

---

## Global Rules (All Layers)

### Naming Conventions
| Element | Convention | Example |
|---------|-----------|---------|
| Classes | [from technical-preferences] | [example] |
| Variables | [from technical-preferences] | [example] |
| Signals/Events | [from technical-preferences] | [example] |
| Files | [from technical-preferences] | [example] |
| Constants | [from technical-preferences] | [example] |

### Performance Budgets
| Target | Value |
|--------|-------|
| Framerate | [from technical-preferences] |
| Frame budget | [from technical-preferences] |
| Draw calls | [from technical-preferences] |
| Memory ceiling | [from technical-preferences] |

### Approved Libraries / Addons
- [library] — approved for [purpose]

### Forbidden APIs ([engine version])
These APIs are deprecated or unverified for [engine + version]:
- `[api name]` — deprecated since [version] / unverified post-cutoff
- Source: `docs/engine-reference/[engine]/deprecated-apis.md`

### Cross-Cutting Constraints
- **[MUST/SHOULD/MAY]** [constraint that the source applies everywhere]

### Ambiguity Findings (Not Manifest Rules)
- [source path and section] — [ambiguous statement and why no normative level was assigned]
```

---

## 6. Suggest Next Steps

After writing the manifest:

- If epics/stories don't exist yet: "Run `$create-epics layer: foundation` then `$create-stories [epic-slug]` — programmers
  can now use this manifest when writing story implementation notes."
- If this is a regeneration (manifest already existed): "Updated. Recommend
  notifying the team of changed rules — especially any new Forbidden entries."

---

## Collaborative Protocol

1. **Load silently** — read all inputs before presenting anything
2. **Show the summary first** — let the user see the scope before writing
3. **Single changeset approval** — include the manifest in the complete preview before creating or overwriting it. On write: Verdict: **COMPLETE** — control manifest written. On decline: Verdict: **BLOCKED** — user declined write.
4. **Source every rule** — never add a rule that doesn't trace to an ADR, a
   technical preference, or an engine reference doc
5. **No interpretation** — extract rules as stated in ADRs; do not paraphrase
   in ways that change meaning
6. **Preserve normative strength** — never promote `SHOULD` or `MAY` to `MUST`;
   ambiguous non-normative text becomes a review finding, not a rule
7. **Keep rejection contextual** — an alternative is forbidden only when the
   source explicitly calls it `forbidden` or `prohibited`
8. **No self-signing** — extraction and drafting belong to the current author;
   a distinct read-only reviewer approves the exact Review Input Hash
