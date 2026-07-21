---
name: architecture-decision
description: "Creates one Proposed Architecture Decision Record (ADR) for a significant technical decision, with alternatives, consequences, traceability, and an independent acceptance handoff."
---

## Invocation and execution

Invoke this workflow as `$architecture-decision`.

Arguments: `[title] [--review full|lean|solo]` or
`retrofit <docs/architecture/adr-....md> [--review full|lean|solo]`.

Before the first file change, present the complete proposed changeset and obtain
one explicit approval unless the enclosing bounded task already authorizes that
exact changeset. This workflow has a strict single-writer boundary:

- It may write only the one target ADR named in the approved changeset.
- It must not edit GDDs, architecture registries, traceability registries,
  stories, epics, readiness state, review records, or lifecycle records.
- Advisory-review output is conversation evidence only; it is not acceptance
  evidence and cannot change an ADR to `Accepted`.
- If the requested outcome needs any other file changed, stop and hand that work
  to the owning workflow instead of expanding this changeset.

Resolve the review mode once:

1. Use an explicit `--review full|lean|solo` argument when supplied.
2. Otherwise read `production/review-mode.txt` when present.
3. Otherwise use `lean`.

The review mode controls pre-write advisory review only. It never controls ADR
lifecycle status.

## 0. Enforce the lifecycle boundary

An ADR authored by this workflow is always `Proposed`. This applies in every
review mode and even when every advisory reviewer approves.

This workflow must never:

- set, promote, or retrofit an ADR to `Accepted`;
- create an architecture-review record or pretend an advisory review is one;
- invoke a lifecycle recorder or materialize a lifecycle transition;
- treat user approval to write a file as approval of the technical decision.

A later transition from `Proposed` to `Accepted` is valid only when a separate
lifecycle recorder consumes an independent `$architecture-review` record that
binds its verdict to the current ADR bytes. At minimum, that handoff must contain:

| Field | Required value |
|---|---|
| `subject_path` | Exact ADR path |
| `subject_sha256` | SHA-256 of the ADR bytes reviewed |
| `verdict` | The accepting verdict defined by `$architecture-review` |
| `review_record_uri` | Stable reference to the independent review record |
| `reviewer_session_id` | Different authoring context from this workflow |
| `recorded_by` | Identity of the lifecycle recorder |
| `recorded_at` | Timestamp of the recorded transition |

If the ADR changes after review, its SHA-256 changes and the review is stale.
Only a fresh independent review of the new hash can support acceptance.

## 1. Parse the request

### No-argument guard

If no title or retrofit path was supplied, ask:

> What technical decision are you documenting? Please provide a short title
> such as `event-system-architecture` or `physics-engine-choice`.

### Retrofit mode

Enter retrofit mode only for `retrofit <path>`.

1. Read the target ADR completely.
2. If its existing `## Status` is `Accepted`, `Deprecated`, or
   `Superseded...`, stop. A lifecycle-managed record must be revised or
   superseded through its lifecycle owner; this author workflow must not mutate
   it.
3. Scan for these sections:
   - `## Status` — BLOCKING when absent
   - `## ADR Dependencies` — HIGH when absent
   - `## Engine Compatibility` — HIGH when absent
   - `## GDD Requirements Addressed` — MEDIUM when absent
4. Present the existing and missing sections and ask whether the single target
   ADR should be augmented. Existing sections remain unchanged.
5. When `Status` is missing, offer only:
   - `Proposed` — the legacy decision is still under consideration; or
   - `Unknown` — lifecycle evidence is unavailable or ambiguous.
   Never offer or infer `Accepted`, `Deprecated`, or `Superseded`.
6. Gather the missing dependency, engine, and GDD traceability information using
   the same read-only context steps as normal authoring.
7. Preview one changeset containing only the retrofit ADR. After authorization,
   append only the approved missing sections.
8. Report the resulting ADR path and SHA-256, then provide the independent
   review handoff in Section 9.

Retrofit does not validate historical acceptance. If acceptance evidence cannot
be bound to the resulting current hash, the effective lifecycle state remains
`Proposed` or `Unknown`.

For normal authoring, continue below.

## 2. Load engine context

Before drafting:

1. Read `docs/engine-reference/[engine]/VERSION.md` for the pinned engine,
   version, knowledge cutoff, and risk levels.
2. Determine the decision domain from the title and user description.
3. Read the corresponding
   `docs/engine-reference/[engine]/modules/[domain].md` when present.
4. Read `breaking-changes.md` and `deprecated-apis.md` for the pinned engine.
5. Display a knowledge-gap warning before design work when the domain risk is
   MEDIUM or HIGH.

If no engine is configured, ask the user to run `$setup-engine` or identify the
engine. Do not invent a version.

## 3. Select the target and gather bounded context

1. Scan `docs/architecture/` and select the next display number.
2. Set exactly one target path:
   `docs/architecture/adr-[NNNN]-[slug].md`.
3. Read related code, relevant GDD requirements, and related ADRs.
4. Read `docs/registry/architecture.yaml` as an accepted-constraint projection
   only. This workflow never writes it.
5. Present the bounded source manifest used for the draft.

### Architecture conflict gate

Present relevant registered stances before collaborative design. If the proposal
conflicts with an accepted stance, continue only after the user chooses one of:

1. **Align** — make the proposal conform to the accepted stance.
2. **Explicit supersession proposal** — the new Proposed ADR names the old ADR
   and a complete replacement. The old stance remains authoritative until an
   independent review and lifecycle recorder accept and record the replacement.
3. **Scoped exception proposal** — record a non-overlapping scope, its boundary
   predicate, owner, reason, and exit condition in the ADR.

A scoped exception must not leave two global stances active. If the scope cannot
be made objectively disjoint, treat it as supersession or stop. “Intentional
exception” without an explicit boundary is not a valid resolution.

## 4. Guide the decision collaboratively

Derive and present a confirm/adjust proposal from the bounded context:

- problem statement;
- two or three concrete alternatives;
- relevant GDD requirements;
- upstream ADR dependencies;
- `Status: Proposed`.

Do not draft until the user confirms or corrects those assumptions. Ask schema
and data-design decisions separately after the assumptions are confirmed.

For dependencies, record:

- `Depends On`;
- `Enables`;
- `Blocks`;
- an ordering note.

## 5. Draft the Proposed ADR

Use this complete structure:

```markdown
# ADR-[NNNN]: [Title]

## Status
Proposed

## Date
[Draft date]

## Engine Compatibility

| Field | Value |
|---|---|
| Engine | [Pinned engine and version] |
| Domain | [Decision domain] |
| Knowledge Risk | [LOW / MEDIUM / HIGH] |
| References Consulted | [Engine-reference paths read] |
| Post-Cutoff APIs Used | [APIs or None] |
| Verification Required | [Specific checks or None] |

## ADR Dependencies

| Field | Value |
|---|---|
| Depends On | [ADR-NNNN or None] |
| Enables | [ADR-NNNN or None] |
| Blocks | [Epic/story identifier or None] |
| Ordering Note | [Constraint or None] |

## Context

### Problem Statement
[Why the decision is needed]

### Constraints
[Technical, schedule, resource, and compatibility constraints]

### Requirements
[Requirement IDs and source references]

## Decision
[The proposed technical decision]

### Architecture Diagram
[ASCII diagram or compact description]

### Key Interfaces
[Technical contracts introduced by the ADR]

## Alternatives Considered
[At least two alternatives with pros, cons, and rejection reasons]

## Consequences

### Positive
[Benefits]

### Negative
[Accepted trade-offs]

### Risks
[Risks and mitigations]

## GDD Requirements Addressed

| Source requirement | Product rule preserved | Technical realization |
|---|---|---|
| [stable source reference] | [player-facing rule] | [ADR-owned technical mapping] |

## Performance Implications
[Expected impacts and validation plan]

## Migration Plan
[Migration steps or None]

## Validation Criteria
[Tests, measurements, and acceptance evidence required]

## Related Decisions
[Related, proposed-supersession, or scoped-exception links]
```

The document must remain `Proposed` throughout this workflow.

## 6. Run advisory reviews

Advisory reviews improve the draft but cannot accept it.

- `solo`: do not spawn advisory reviewers.
- `lean`: when an engine is configured, ask the primary engine specialist to
  review engine/API compatibility.
- `full`: ask the primary engine specialist and `technical-director` to review
  the same draft. Their reviews may run in parallel because neither owns the
  lifecycle transition.

Label every result `ADVISORY`. For blocking technical findings, revise the draft
only after the user confirms the technical choice. For concerns, record risks or
unresolved validation work. A timeout, failure, concern, rejection, or approval
all leave `Status: Proposed`.

Do not spawn `$architecture-review` in this authoring context. The independent
review must occur after the ADR bytes are written and hashed, in a fresh context.

## 7. Classify GDD sync findings

Compare referenced GDD product rules with the ADR's proposed technical
realization. Report each discrepancy with exactly one destination:

| Destination | Meaning | Action in this workflow |
|---|---|---|
| `ADR/TECH` | API, signal, method, data type, internal ownership, or other implementation naming | Keep the technical name in the ADR and add a mapping to the GDD term. Do not edit the GDD. |
| `GDD PRODUCT RULE` | Player-visible behavior, balance rule, content rule, UX rule, or other product requirement would change | Stop finalization of the affected decision and hand it to the design owner or `$propagate-design-change`. Do not edit the GDD. |

A technical naming mismatch is not permission to rewrite a GDD. A product-rule
change is not valid until the design owner approves and records it in the design
source of truth. The ADR may cite only the currently approved product rule.

## 8. Preview and write one-file changeset

Present the complete changeset:

```text
Proposed changeset
- ADD or UPDATE: docs/architecture/adr-[NNNN]-[slug].md
  Purpose: one Proposed ADR with traceability and validation criteria

Explicitly unchanged
- design/gdd/**
- docs/registry/**
- production/**/stories/**
- review and lifecycle records
```

Obtain one approval unless that exact one-file changeset is already authorized.
If approval includes another file, refuse the expansion and provide an owner
handoff.

Immediately before writing, confirm the draft still says `Status: Proposed`.
Write only the target ADR. Compute and report its SHA-256 after the write.

From `Blocks` or `Enables`, emit a non-mutating event in the final output:

```yaml
event: dependency_may_be_unblocked
adr_path: docs/architecture/adr-[NNNN]-[slug].md
adr_sha256: [current hash]
eligibility: pending_accepted_lifecycle_record
affected_items:
  - [epic/story identifier]
```

This event is a review prompt, not a readiness transition. Never edit a blocked
story or claim it is `Ready`. `$story-readiness` remains responsible for checking
all dependencies, acceptance evidence, acceptance criteria, and tests.

Do not update any registry. You may report derived registry candidates as a
handoff, but only a lifecycle recorder may project them from an Accepted ADR.

## 9. Independent review and lifecycle handoff

After the write, report:

1. target path;
2. current SHA-256;
3. unresolved advisory findings;
4. `ADR/TECH` and `GDD PRODUCT RULE` handoffs;
5. registry projection candidates, clearly labeled “not written”;
6. dependency event, clearly labeled “no story status changed”.

Always include:

> Open a fresh Codex session and run `$architecture-review` against this ADR.
> The review record must name the ADR path and current SHA-256. This authoring
> session cannot accept the ADR. A separate lifecycle recorder must validate the
> independent review record before recording `Accepted` and deriving registry
> state.

Then offer one highest-priority next action or `Stop here`. Do not enumerate or
automatically start all remaining ADRs.
