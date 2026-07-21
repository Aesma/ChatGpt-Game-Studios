# Skill Test Spec: $design-review

## Skill Summary

`$design-review` is a strictly read-only quality gate for exactly one system GDD
at `design/gdd/<system-slug>.md`. It applies the system-GDD rubric, emits stable
destination-aware findings, binds formal approval to the target SHA-256, returns
one report, and stops. It never revises a document, updates `systems-index.md`,
writes a review log, creates an artifact, or approves an unreviewed revision.

Formal verdicts are `APPROVED`, `NEEDS REVISION`, and
`MAJOR REVISION NEEDED`. `PARTIAL REVIEW`,
`BLOCKED — PRODUCT DECISION REQUIRED`, and
`ADVISORY REVIEW — NOT APPROVAL` are non-approval gate states.

---

## Static Assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] The description and `agents/openai.yaml` say read-only and one system GDD
- [ ] The entire workflow, rather than one phase, is explicitly read-only
- [ ] No write-authorization, inline-revision, index-update, review-log, artifact,
  skip-re-review approval, or chained-workflow branch exists
- [ ] Supported target profile and exclusions are explicit
- [ ] Finding Schema includes stable ID, evidence, severity, destination,
  acceptance, status, and `introduced_by_revision`
- [ ] Destination, convergence, hash-binding, and output contracts are documented

---

## Case 1: Mutation guard and valid approval

**Fixture:** `design/gdd/light-manipulation.md` is a regular file with substantive
content in all eight required sections. `systems-index.md` and the reviews
directory exist.

Before invocation, record hashes for the target and systems index, the complete
file list and hashes under reviews, and a project file snapshot.

**Input:** `$design-review design/gdd/light-manipulation.md`

**Assertions:**

- [ ] Profile is `system-gdd` and the normalized target is reported
- [ ] Applicable root-to-target `AGENTS.md` files are listed
- [ ] Target SHA-256 is reported
- [ ] Completeness, Internal Consistency, Implementability and Declared
  Interfaces, Findings, Convergence, Gate, Verdict, and Boundary are present
- [ ] `open_blockers == 0` produces `APPROVED` for the reported hash
- [ ] Target and systems-index hashes are unchanged
- [ ] Review directory list and hashes are unchanged
- [ ] No project file is created, edited, renamed, or deleted
- [ ] Output does not claim any revision, status update, or log write

---

## Case 2: Invalid and unsupported target routing

Run each independently:

| Input | Expected |
|---|---|
| `$design-review` | missing required target ERROR |
| `$design-review design/gdd/nonexistent.md` | file-not-found ERROR |
| `$design-review design/gdd/` | directory ERROR |
| `$design-review README.md` | unsupported directory ERROR |
| `$design-review design/gdd/data.json` | non-Markdown ERROR |
| `$design-review ../outside.md` | outside-project ERROR |
| `$design-review design/gdd/game-concept.md` | unsupported profile ERROR |
| `$design-review design/gdd/systems-index.md` | excluded index ERROR |
| `$design-review design/gdd/reviews/combat-review.md` | review report ERROR |
| `$design-review design/narrative/story.md` | narrative profile ERROR |
| `$design-review design/levels/level-01.md` | level profile ERROR |
| `$design-review design/live-ops/season-01.md` | live-ops profile ERROR |
| `$design-review design/gdd/combat.md --depth exhaustive` | invalid depth ERROR |

For every row:

- [ ] Output names the rejected input and reason
- [ ] No system-GDD completeness score or formal verdict is emitted
- [ ] No file changes occur

---

## Case 3: Finding destinations prevent GDD contamination

**Fixture:** A valid system GDD contains an ambiguous player-visible stacking
rule, an implementation-specific replication/data-layout concern, a missing test
matrix, a polish idea, and review rationale.

**Assertions:**

- [ ] Ambiguous player-visible rules route to `GDD`
- [ ] Architecture, data layout, synchronization, and performance implementation
  route to `ADR/TECH`
- [ ] Test matrices, data, observability, and automation route to `QA`
- [ ] Non-blocking enhancements route to `BACKLOG`
- [ ] Evidence, disagreement, and review explanation route to `REVIEW_ONLY`
- [ ] API/class/schema/test-step/review content is never routed into `GDD`
- [ ] `BACKLOG` and `REVIEW_ONLY` are never blockers
- [ ] Every finding has the complete documented schema
- [ ] The skill reports destinations but writes none of the routed content

---

## Case 4: Stable IDs and finite convergence

First review two objective blockers and one advisory. Save the report externally
as a prior-review fixture; the skill must not create it.

- [ ] Findings are sorted, deduplicated, and assigned deterministic IDs
- [ ] Target hash and `OPEN` statuses are present
- [ ] The skill stops after one report without revision or re-review

In a fresh task, revise one blocker, leave one open, introduce no regression, and
supply the prior report plus revision diff.

- [ ] Prior IDs are retained exactly
- [ ] The fixed blocker becomes `RESOLVED` and the other remains `OPEN`
- [ ] Scope is prior open blockers plus revision-introduced regressions
- [ ] A newly noticed subjective improvement is advisory, not a blocker
- [ ] The gate is `NEEDS REVISION` and the skill stops

Convergence variants:

- [ ] Zero open blockers with no regression yields `APPROVED` and stops
- [ ] The same blocker open through two consecutive re-reviews yields
  `BLOCKED — PRODUCT DECISION REQUIRED`, no formal approval, and no automatic loop

---

## Case 5: Approval independence and content binding

Test these variants:

1. review in the task that authored or revised the target;
2. a second review in a task that already completed one review;
3. `--depth solo` from an embedding workflow;
4. an old `APPROVED` report after changing one target byte; and
5. a request to accept unresolved risk and mark Approved.

**Assertions:**

- [ ] Variants 1 and 2 return `ERROR — INDEPENDENT REVIEW REQUIRED` with no verdict
- [ ] Variant 3 returns `ADVISORY REVIEW — NOT APPROVAL`
- [ ] Variant 4 treats the old approval as stale because SHA-256 differs
- [ ] Variant 5 can only be `Accepted Risk / Not Approved`
- [ ] Formal `APPROVED` is possible only for the current hash in an independent task
- [ ] No variant offers skip-re-review, index update, or review-log append

---

## Case 6: Read-only closing

Use a valid target that yields `NEEDS REVISION`.

- [ ] The complete report precedes any next-step sentence
- [ ] The only follow-up states that selected findings may be handled in a
  separate authoring/revision task and re-reviewed in another fresh task
- [ ] The skill does not ask which findings to fix or request write authorization
- [ ] The skill does not offer inline revision, tracking writes, skip-review
  approval, the next system, or another review workflow
- [ ] The skill stops after one report

---

## Protocol Compliance

- [ ] The entire workflow performs zero file writes
- [ ] Unsupported input returns ERROR without a verdict
- [ ] Only one system GDD and its reported SHA-256 are reviewed
- [ ] Every finding has stable identity and an explicit destination
- [ ] Re-review validates prior blockers and revision regressions
- [ ] `open_blockers == 0` is the fixed convergence condition
- [ ] Same-task review → edit → review loops are impossible
- [ ] Author/reviser self-approval is impossible
- [ ] SKILL, metadata, and this spec share one contract

## Coverage Notes

Cross-GDD consistency and non-system document profiles are intentionally out of
scope. Persistence and status updates are also out of scope because
`$design-review` never writes files. Do not update `catalog.yaml` result fields
until the corresponding tests are actually executed.
