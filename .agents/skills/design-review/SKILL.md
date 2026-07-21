---
name: design-review
description: "Performs a strictly read-only quality-gate review of one system GDD and returns one hash-bound report without editing files."
---

## Read-only contract and invocation

Invoke this workflow as `$design-review`.

This skill is a strictly read-only quality gate in every phase. It returns one
review report and stops. Never modify the target or any other file, request write
authorization, revise the GDD, update `systems-index.md`, append a review log,
create an artifact, or chain into another workflow.

Run formal review in a task independent from authoring or revision. If this task
has authored or revised the target, or has already reviewed it once, return
`ERROR — INDEPENDENT REVIEW REQUIRED` without a verdict and stop. Revision must
occur in a separate authoring task, and re-review in another fresh task. Any
formal approval applies only to the reviewed document hash. `Accepted Risk` is
always `Accepted Risk / Not Approved`.

Arguments:

```text
<path-to-system-gdd> [--depth full|lean|solo] [--prior-review <path>]
```

The target path is required. Default `--depth` is `lean`.

- `full`: primary review plus relevant specialist review.
- `lean`: primary review only.
- `solo`: embedded read-only analysis; emit
  `ADVISORY REVIEW — NOT APPROVAL` and never a formal verdict.
- `--prior-review`: read-only prior report used to retain finding IDs during
  re-review. The caller must also supply revision-diff evidence.

`--depth` is independent of global review mode. Do not read
`production/review-mode.txt`, spawn a director gate, or let a director override
this skill's gate rules.

## Phase 0: Validate the target

Validate exactly one target before reading it. It must exist as a regular Markdown
file whose direct parent is `design/gdd/`, in the form
`design/gdd/<system-slug>.md`.

Explicitly reject `game-concept.md`, `systems-index.md`, review reports/logs,
templates, files in any other directory, and concept, narrative, level, UX, art,
audio, live-ops, season, or other document profiles. Also reject missing or
multiple paths, directories, non-Markdown files, paths outside the project,
symlinks resolving outside the project, and invalid depth values.

For invalid or unsupported input, return a clear `ERROR` naming the input and
reason, do not apply the system-GDD rubric, emit no verdict, and stop. Never infer
a document profile or force the eight-section rubric onto a non-system document.

---

## Phase 1: Load bounded read-only context

Read the validated target in full. Load every applicable `AGENTS.md` from the
repository root through `design/gdd/`, in that order, with the nearest file taking
precedence. List the loaded instruction files in the report.

Read only bounded supporting context:

- `design/gdd/systems-index.md`, if present, for declared dependency identity;
- first-level dependency documents explicitly named by the target; and
- pillar or lore documents directly linked by the target.

Do not load documents merely because they seem related. Do not scan all GDDs or
all narrative files.

Compute and report the target's SHA-256 content hash before analysis. The review
and any approval apply only to those exact bytes. If the target changes during the
review, return `ERROR — TARGET CHANGED DURING REVIEW` without a verdict and stop.

Only a supplied `--prior-review` containing the prior target hash and stable
findings establishes re-review state. Validate it as a readable project file.
Missing, unreadable, or malformed re-review evidence returns `ERROR` without a
verdict. Legacy summary-only review logs do not establish finding identity.

For declared dependencies, classify each as `exists`,
`planned-not-authored`, `unknown`, or `broken-link`. A planned document is not
automatically a broken reference.

---

## Phase 2: Completeness Check

Evaluate against the Design Document Standard checklist:

- [ ] Has Overview section (one-paragraph summary)
- [ ] Has Player Fantasy section (intended feeling)
- [ ] Has Detailed Rules section (unambiguous mechanics)
- [ ] Has Formulas section (all math defined with variables)
- [ ] Has Edge Cases section (unusual situations handled)
- [ ] Has Dependencies section (other systems listed)
- [ ] Has Tuning Knobs section (configurable values identified)
- [ ] Has Acceptance Criteria section (testable success conditions)

---

## Phase 3: Consistency and Implementability

**Internal consistency:**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability:**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?

**Cross-system consistency:**
- Does this conflict with any existing mechanic?
- Does this create unintended interactions with other systems?
- Is this consistent with the game's established tone and pillars?

---

## Phase 3b: Normalize findings

Every reported issue must use this schema:

```yaml
id: DRV-<CATEGORY>-<NNN>
severity: blocker | advisory | note
category: completeness | consistency | implementability | dependency | player-fantasy
source: primary-reviewer | <specialist-name>
evidence:
  file: design/gdd/<system-slug>.md
  section: <heading or line location>
  quote_or_fact: <short evidence>
problem: <specific defect>
destination: GDD | ADR/TECH | QA | BACKLOG | REVIEW_ONLY
required_change: <minimum change needed, or "none" for a note>
acceptance: <objective condition that closes this finding>
status: OPEN | RESOLVED | WAIVED
introduced_by_revision: true | false
```

On a first review, sort findings by rubric order, evidence location, then a
normalized problem key. Deduplicate the same underlying defect and assign
category-local three-digit IDs in that stable order. On re-review, preserve every
prior ID exactly. New regression IDs continue after the highest prior ID in their
category. Never renumber an existing finding because wording or status changed.

Use destinations as follows:

| Destination | Put here | Never put here |
|---|---|---|
| `GDD` | Player-visible rules, formulas, boundary behavior, tuning constraints, acceptance conditions | APIs, class structure, storage/resource schemas, test steps, review discussion |
| `ADR/TECH` | Architecture, data structures, synchronization, technical performance strategy | Player-experience rules |
| `QA` | Test matrices/data, observability, automation advice | The design decision itself |
| `BACKLOG` | Non-blocking enhancements | Current approval blockers |
| `REVIEW_ONLY` | Evidence, disagreement, review explanation | Any authoritative product rule |

A finding is a `blocker` only when objective evidence shows that the current
system GDD cannot be implemented or accepted without guessing a required product
rule, contains contradictory authoritative rules, has a broken explicit
interface, or omits substantive required content. Preferences and improvements
are advisory. `BACKLOG` and `REVIEW_ONLY` findings cannot block approval.

The review identifies destination and acceptance conditions only. It never writes
the routed content anywhere.

## Phase 3c: Specialist review (`full` only)

Skip delegation for `lean` and `solo`. Specialists are reviewers, not authors:
they must not edit files, revise the design, or make product decisions.

Give each specialist the target hash, applicable rubric, structural findings,
Finding Schema, destination rules, and this instruction:

> Validate the document against objective domain standards. Report only findings
> with specific evidence, an objective acceptance condition, and the correct
> destination. A preference or speculative enhancement is advisory, not a
> blocker. Do not edit any file or propose inserting technical, QA, or review
> material into the GDD.

Normalize and deduplicate specialist results before applying the verdict. No
creative director or other senior reviewer may replace the deterministic gate
decision.

---

## Phase 4: Re-review convergence

A re-review is a verification pass, not a new open-ended critique. Use the prior
report and supplied change evidence to:

1. re-evaluate only prior `OPEN` blockers and retain their IDs;
2. mark one `RESOLVED` only when its stated acceptance condition is met;
3. inspect the supplied revision diff for regressions caused by that revision;
4. add a blocker only when evidence proves it is revision-introduced or an
   objective P0/P1 defect omitted by the first review; and
5. keep newly noticed subjective improvements advisory.

Stop convergence when `open_blockers == 0`. Advisory and note findings do not
prevent approval. If the same blocker remains open through two consecutive
re-review rounds, output `BLOCKED — PRODUCT DECISION REQUIRED`, identify the
unresolved IDs, do not start another review or revision, and stop.

This skill performs at most one first-review or re-review pass in a task.

---

## Phase 5: Apply the gate and return one report

For an independent `full` or `lean` review, apply these rules mechanically:

- `APPROVED`: zero `OPEN` blockers; advisory and note findings may remain.
- `NEEDS REVISION`: one or more `OPEN` blockers can be resolved by bounded,
  explicit edits without changing the core product direction.
- `MAJOR REVISION NEEDED`: the core player fantasy conflicts with the rule model,
  a product decision is required, or at least three required sections are
  substantively missing.
- `PARTIAL REVIEW`: required review coverage failed; it can never produce
  `APPROVED`.

A reviewer or specialist cannot override these rules.

Use this output shape:

```markdown
## Design Review: <document title>

- Profile: system-gdd
- Target: design/gdd/<system-slug>.md
- Target SHA-256: <hash>
- Depth: full | lean | solo
- Review type: first review | re-review
- Applicable instructions: <loaded AGENTS.md files>
- Approval independence: independent | advisory-only

### Completeness: <X>/8 substantive sections
<section results>

### Internal Consistency
<results>

### Implementability and Declared Interfaces
<results and dependency classifications>

### Findings
<complete normalized finding records, including RESOLVED prior findings>

### Convergence
- Prior open blocker IDs: <IDs or none>
- Resolved this pass: <IDs or none>
- Open blockers: <count and IDs>
- Revision-introduced regressions: <IDs or none>

### Gate
<APPROVED | NEEDS REVISION | MAJOR REVISION NEEDED | PARTIAL REVIEW |
BLOCKED — PRODUCT DECISION REQUIRED | ADVISORY REVIEW — NOT APPROVAL>

### Verdict: <formal verdict when and only when one is permitted>

### Boundary
Read-only review complete. No source, index, review log, or other file was
modified. This report applies only to target SHA-256 <hash>.
```

After returning the report, stop. If revision is required, state only that the
user may start a separate authoring/revision task with selected finding IDs and
then run an independent re-review in another fresh task. Do not offer an inline
revision, a status/log update, a skip-review approval, or a chained next workflow.
