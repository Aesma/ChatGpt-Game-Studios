---
name: design-review
description: "Performs a strictly read-only quality-gate review of one system GDD and returns one hash-bound report without editing files."
---

## Read-only contract and invocation

Invoke this workflow as `$design-review`.

Contract version: `cgs.design-review/v2`.

This skill is a strictly read-only quality gate in every phase. It returns one
review report and stops. Never modify the target or any other file, request write
authorization, revise the GDD, update `systems-index.md`, append a review log,
create an artifact, or chain into another workflow. The report may contain an
embedded evidence record, but this skill never persists that record.

Run formal review in a task independent from authoring or revision. If this task
has authored or revised the target, or has already reviewed it once, return
`ERROR — INDEPENDENT REVIEW REQUIRED` without a gate state, formal verdict, or
evidence record, then stop. Revision must occur in a separate authoring task, and
re-review in another fresh task. Any formal approval applies only to the reviewed
document hash. `Accepted Risk` is always `Accepted Risk / Not Approved`; a waived
blocker remains unresolved for approval.

Arguments:

```text
<path-to-system-gdd> [--depth full|lean|solo]
  [--prior-review <path> --revision-evidence <path>]
```

The target path is required. Default `--depth` is `lean`.

- `full`: primary review plus a bounded specialist batch; reserved for a GDD
  meeting the high-risk test in Phase 5.
- `lean`: primary review only and the default formal-review mode.
- `solo`: embedded read-only analysis; emit
  `ADVISORY REVIEW — NOT APPROVAL` and never a formal verdict.
- `--prior-review`: a complete prior `cgs.design-review/v2` report used to retain
  finding identity during re-review.
- `--revision-evidence`: immutable change evidence binding the prior target path
  and SHA-256 to the current target path and SHA-256, with changed line ranges or
  a patch and an authoring-task or application-receipt identity.

`--prior-review` and `--revision-evidence` are a required pair. Supplying only one
is invalid. Each option may occur at most once and must have exactly one value.
Reject extra positional arguments, duplicate or unknown options, option values
that begin with `--`, and invalid depth values. Do not infer omitted values.

`--depth` is independent of global review mode. Do not read
`production/review-mode.txt`, spawn a director gate, or let a director override
this skill's gate rules.

## Phase 0: Validate and normalize inputs

Resolve the repository root and canonicalize every supplied path before reading
its content. The target must resolve inside the repository as a non-symlink
regular Markdown file whose direct parent is exactly `design/gdd/`, in the form
`design/gdd/<system-slug>.md`. Normalize the reported path to repository-relative
forward-slash form. `<system-slug>` must be lowercase kebab-case.

Explicitly reject `game-concept.md`, `systems-index.md`, review reports/logs,
templates, files in any other directory, and concept, narrative, level, UX, art,
audio, live-ops, season, or other document profiles. Also reject missing or
multiple targets, directories, non-Markdown files, paths outside the repository,
symlinks, canonical paths escaping through junctions, globs, and URLs.

The prior report and revision evidence, when supplied, must each resolve to one
readable, project-local, non-symlink regular file no larger than 256 KiB. Require:

1. the prior report declares contract `cgs.design-review/v2`, the same normalized
   target path, a prior target SHA-256, a review run identity, and complete unique
   finding records;
2. its embedded `cgs.review-evidence/v1` record ID and canonical report-payload
   SHA-256 both recompute correctly, and its artifact path/hash equal the prior
   report's declared target path/hash;
3. revision evidence names the same target, the prior report's target SHA-256 as
   its pre-change hash, and the current raw-byte target SHA-256 as its post-change
   hash; and
4. revision evidence contains changed line ranges or exact patch content and a
   stable authoring-task or application-receipt identity.

Malformed, internally inconsistent, summary-only, current-hash-mismatched, or
unbound re-review evidence returns `ERROR — INVALID RE-REVIEW EVIDENCE` without a
gate state, formal verdict, or evidence record.

For any invalid or unsupported input, return a clear `ERROR` naming the rejected
input and reason, do not apply the system-GDD rubric, emit no completeness score,
gate state, formal verdict, or evidence record, and stop. Never infer a document
profile or force the eight-section rubric onto a non-system document.

---

## Phase 1: Load bounded read-only context

Read the validated target in full. Load in full every applicable `AGENTS.md` from
the repository root through `design/gdd/`, in root-to-target order. Apply the
nearest file last when rules differ. List the loaded instruction files in that
same order in the report.

Compute SHA-256 over the target's exact raw bytes before analysis. Never hash
normalized, copied, or re-serialized content. Recompute it after all review work
and immediately before returning the report. If it differs, return
`ERROR — TARGET CHANGED DURING REVIEW` without a gate state, formal verdict, or
evidence record and stop.

Supporting context is limited to:

1. `design/gdd/systems-index.md`, when present, for stable system identity;
2. first-level dependency documents explicitly identified in the target's
   Dependencies section by stable System ID or direct repository-relative link;
3. pillar or lore documents directly linked by the target.

Never load a document merely because it seems related. Never scan all GDDs or
narrative files, follow a second-level dependency, or fuzzy-match a filename.
Select supporting files in the order above, then target declaration order. The
fixed supporting-context budget is eight files and 256 KiB of exact bytes total;
the target, applicable `AGENTS.md` files, prior report, and revision evidence are
outside that budget. Do not partially read a selected file.

If an explicitly required supporting file cannot be read or the declared context
exceeds either budget, list every loaded and omitted path and the exact reason,
set required coverage to incomplete, and produce `PARTIAL REVIEW` for `full` or
`lean`. In `solo`, keep the advisory state and disclose the coverage gap. Never
approve from truncated or silently omitted required context.

### Stable dependency classification

Parse `systems-index.md` by exact `System ID` and normalized `Design Doc` cells.
For each declared dependency, prefer an exact `SYS-<canonical-kebab-slug>` ID;
otherwise require an exact direct link. Never infer identity from display names
or approximate filenames. Classify exactly once:

- `exists`: one exact index row resolves to one current regular Markdown design
  doc, or one exact direct link resolves to that file;
- `planned-not-authored`: one exact index row exists with status `Not Started` or
  `In Design` and no authored Design Doc; this is advisory by itself;
- `unknown`: no exact stable ID or direct-link identity can be resolved; this is
  a blocker;
- `broken-link`: an explicit link is missing/outside the repository, an index row
  names a Design Doc that is missing, or the row and explicit link disagree; this
  is a blocker.

For an `exists` dependency, check only the declared interface and bidirectional
reference: the dependency doc must name the target's exact System ID, or its exact
normalized path when the target has no index ID. A missing reverse declaration is
a dependency blocker. A `planned-not-authored` dependency is not a blocker unless
the target claims an already-authoritative interface that cannot exist without
that document; report that distinct contradiction with evidence.

Report the target's uniquely matched System ID when available; otherwise use the
stable artifact ID `gdd:<system-slug>`. This skill observes identity and status but
never updates the systems index.

---

## Phase 2: Substantive eight-section gate

Require these eight canonical level-2 headings exactly once and in this order:

1. `Overview`
2. `Player Fantasy`
3. `Detailed Rules`
4. `Formulas`
5. `Edge Cases`
6. `Dependencies`
7. `Tuning Knobs`
8. `Acceptance Criteria`

A heading is not completion. A section is substantively missing when its heading
is absent or duplicated, its body is empty/placeholder-only, or its content fails
the minimum assertion below. Report out-of-order headings as a blocker, but count
substantive presence independently so the major-revision threshold is reproducible.

| Section | Minimum substantive assertion |
|---|---|
| Overview | One non-placeholder summary states the system purpose, player-visible scope, and explicit exclusions or boundary. |
| Player Fantasy | States the intended player feeling and the rule outcomes that are meant to produce it. |
| Detailed Rules | Defines triggers, eligibility, state transitions or ordering, outcomes, and ownership without requiring a programmer to guess a product rule. |
| Formulas | Defines every symbol, unit, expected or safe input/output range, clamp/rounding rule when applicable, and at least one worked example for each rule-critical formula. |
| Edge Cases | Names boundary, simultaneous, interruption, invalid-state, and failure cases that apply and gives an explicit outcome; “handle gracefully” is invalid. |
| Dependencies | Uses exact stable System IDs or direct links, states each interface/ownership direction, and supports bidirectional verification. |
| Tuning Knobs | Gives each configurable value's default or source, safe range, affected gameplay behavior, and formula/rationale linkage. |
| Acceptance Criteria | Gives independently pass/fail-verifiable conditions covering every core rule and rule-critical formula; “feels good”, “works correctly”, and “performs well” alone are invalid. |

`Not applicable — <specific rationale>` is permitted only in `Formulas`,
`Dependencies`, or `Tuning Knobs`. It is substantive only when the rationale
demonstrates respectively that the system has no numeric transformation, no
external system interface, or no configurable value. A bare `N/A`, unsupported
claim, or contradiction elsewhere makes the section substantively missing.

For every section report: heading count, order result, substantive PASS/FAIL,
evidence location, and failed assertion. The completeness score is the number of
sections passing substantive content, not the number of headings.

---

## Phase 3: Internal consistency and implementability

Review only the target and its declared first-level interfaces.

**Internal consistency:**

- Do formulas and worked examples produce the described outcomes at ordinary and
  boundary values?
- Do detailed rules, tuning ranges, edge outcomes, and acceptance criteria agree?
- Does the rule model actually deliver the stated player fantasy?

**Implementability:**

- Can a programmer determine every player-visible rule without making a product
  decision?
- Are ownership, ordering, inputs, outputs, units, ranges, clamps, and invalid
  states explicit where applicable?
- Are implementation, performance, data, and QA observations routed outside the
  GDD unless they expose a missing player-visible rule?

**Declared-interface consistency:**

- Do only explicitly declared dependencies agree on identity, ownership, values,
  and bidirectional interaction?
- Do directly linked pillars or lore contradict an explicit target rule?

Do not search for conflicts across undeclared GDDs, perform whole-game design
theory, or audit global balance. Cross-GDD ownership belongs to
`$consistency-check`; whole-set design-theory ownership belongs to
`$review-all-gdds`. Do not invoke or automatically recommend either workflow.

---

## Phase 4: Normalize findings and apply severity

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
decision_kind: editorial | derived | product-decision
required_change: <minimum change or decision question; "none" only for a note>
acceptance: <objective condition that closes this finding>
first_seen_target_sha256: <64-lowercase-hex>
last_evaluated_target_sha256: <64-lowercase-hex>
status: OPEN | RESOLVED | WAIVED
resolution: null | <current-hash evidence proving acceptance is satisfied>
introduced_by_revision: true | false
consecutive_open_re_reviews: <non-negative integer>
```

On a first review, sort findings by canonical section order, evidence line, then a
lowercase whitespace-normalized problem key. Merge findings only when category,
root cause, evidence, destination, and acceptance condition are materially the
same; preserve all sources on the merged record. Assign category-local
three-digit IDs in that deterministic order.

On re-review, preserve every prior ID exactly. New regression IDs continue after
the highest prior ID in their category. Never renumber an existing finding because
wording, source, severity, or status changes. `RESOLVED` requires non-null
resolution evidence from the current hash showing the recorded acceptance
condition is satisfied. A blocker marked `WAIVED` remains unresolved and prevents
approval; accepted risk never converts it to `RESOLVED`.

Use destinations as follows:

| Destination | Put here | Never put here |
|---|---|---|
| `GDD` | Player-visible rules, formulas, boundary behavior, tuning constraints, acceptance conditions | APIs, class structure, storage/resource schemas, test steps, review discussion |
| `ADR/TECH` | Architecture, data structures, synchronization, technical performance strategy | Player-experience rules |
| `QA` | Test matrices/data, observability, automation advice | The design decision itself |
| `BACKLOG` | Non-blocking enhancements | Current approval blockers |
| `REVIEW_ONLY` | Evidence, disagreement, review explanation | Any authoritative product rule |

A finding is a `blocker` only when objective evidence shows that the current GDD
cannot be implemented or independently accepted without guessing a required
product rule, contains contradictory authoritative rules, has an unknown or
broken declared interface, or has a substantively missing required section.
Preferences, speculative enhancements, implementation choices that do not change
player-visible rules, and unmeasured design-theory opinions are advisory.
`BACKLOG` and `REVIEW_ONLY` findings can never be blockers.

For `decision_kind: product-decision`, `required_change` must state the unresolved
decision, constraints, and acceptance boundary without selecting an outcome or
drafting the authoritative rule. Such an open blocker triggers major revision.
Editorial findings may specify exact corrections that preserve meaning. Derived
findings may specify a consequence only when it follows uniquely from already
approved rules. The review identifies destinations and acceptance conditions; it
never applies routed content.

---

## Phase 5: Bounded specialist review (`full` only)

Skip delegation for `lean` and `solo`. Specialists are reviewers, not authors:
they must not edit files, revise the design, or make product decisions.

### High-risk admission and deterministic selection

Build candidates only from explicit target content:

| Domain signal | Candidate role | Fixed tie order |
|---|---|---:|
| Economy, rewards, pricing, drops, progression curves | `economy-designer` | 1 |
| Combat/balance equations, stacking, boundary-heavy system math | `systems-designer` | 2 |
| Multiplayer authority, prediction, replication, reconciliation | `network-programmer` | 3 |
| AI state, perception, targeting, navigation | `ai-programmer` | 4 |
| Player-facing interaction, accessibility, information presentation | `ux-designer` or `accessibility-specialist`, whichever exact concern is present | 5 |
| Explicit performance budget, scale limit, memory/frame-time risk | `performance-analyst` | 6 |
| Configured-engine constraint or version-sensitive engine interface | the configured primary engine specialist only | 7 |
| Complex testability, safety, or multi-state acceptance coverage | `qa-lead` | 8 |

Score each candidate: `3` for an explicit hard constraint, declared high risk, or
authoritative external interface; `2` for a rule-critical formula/state model or
core acceptance dependency; `1` for an incidental mention. Deduplicate roles and
discard score `1`. A GDD is high-risk only when at least one candidate scores `3`
or at least two distinct candidates score `2`. If `--depth full` is requested but
this test fails, return `ERROR — FULL DEPTH NOT JUSTIFIED`, recommend `lean`, emit
no gate state, formal verdict, or evidence record, and stop.

Sort by descending score then fixed tie order and select at most three roles. The
primary reviewer performs synthesis; never spawn a director or a separate senior
synthesizer. Determine currently available delegation slots and use no more than
the smaller of three, the selected-role count, and available slots excluding the
current task. Start all selected specialists in one parallel batch.

Give each specialist the target hash, applicable rubric, bounded relevant
context, structural findings, Finding Schema, destination rules, and this prompt:

> Validate only the assigned domain against objective standards. Return no more
> than five unique findings, ordered blockers before advisories. Every finding
> needs exact evidence, an objective acceptance condition, and the correct
> destination. Merge common root causes. If more than five materially distinct
> evidenced defects remain, return `FINDING_OVERFLOW` instead of hiding them. A
> preference is advisory. Do not edit files, make product decisions, or propose
> inserting technical, QA, or review material into the GDD.

Technical, engine, network, AI, and performance roles normally use `ADR/TECH` or
`QA`; they may use `GDD` only when their evidence proves a missing or contradictory
player-visible rule. `qa-lead` normally uses `QA`, but routes an untestable
authoritative acceptance condition to `GDD`. Design/economy roles may use `GDD`,
`BACKLOG`, or `REVIEW_ONLY` as the content requires.

### Timeout, failure, and partial coverage

Track each selected role as `completed`, `blocked`, `timed-out`, `failed`,
`unavailable`, `finding-overflow`, or `late-discarded`. Use the platform's shorter
deadline when one exists; otherwise wait in at most three bounded intervals of no
more than 60 seconds each. Surface `blocked` immediately, continue collecting
already running peers until their deadline, then interrupt or disregard remaining
late work. Never wait indefinitely or silently substitute invented findings.

The primary review must succeed to return a review report. If it cannot, return
`ERROR — PRIMARY REVIEW INCOMPLETE` with no gate state, verdict, or evidence. If
any selected specialist is not `completed`, preserve every completed result,
describe missing coverage, set required coverage incomplete, and return
`PARTIAL REVIEW`; it can never produce `APPROVED`. A same-agent fallback may be
shown as advisory context but does not count as completed independent specialist
coverage for `full`.

Normalize and deduplicate completed specialist findings before applying the gate.
No specialist or director may replace the deterministic gate decision.

---

## Phase 6: Re-review convergence

A re-review is a verification pass, not a new open-ended critique. Use the
validated prior report and revision evidence to:

1. carry every prior finding into the report and preserve its ID;
2. re-evaluate prior unresolved blockers against their recorded acceptance;
3. set `RESOLVED` only with non-null current-hash resolution evidence;
4. inspect only evidenced changed ranges plus the interfaces they directly affect
   for revision-introduced regression;
5. reopen an existing ID when the same accepted condition regressed, otherwise
   add a new ID only for a proven revision-introduced defect or an objective gate
   defect whose omission would make the prior approval mechanically false; and
6. keep newly noticed preferences or unrelated improvements advisory.

On the first review set `consecutive_open_re_reviews: 0`. Each re-review that
leaves the same blocker unresolved increments it by one; resolution resets it to
zero. Stop convergence when there are no `OPEN` or blocker-level `WAIVED`
findings. If any blocker reaches `consecutive_open_re_reviews: 2`, output
`BLOCKED — PRODUCT DECISION REQUIRED`, identify the IDs, emit no formal verdict,
do not start another review or revision, and stop.

This skill performs at most one first-review or re-review pass in a task.

---

## Phase 7: Apply gate precedence mechanically

Apply exactly the first matching rule:

1. Invalid input, failed independence, target mutation, malformed re-review
   evidence, or incomplete primary review: `ERROR`; no gate state, formal verdict,
   or evidence record.
2. `solo`: `ADVISORY REVIEW — NOT APPROVAL`; no formal verdict.
3. Incomplete required context or any incomplete selected specialist:
   `PARTIAL REVIEW`; no formal verdict.
4. Any blocker with `consecutive_open_re_reviews >= 2`:
   `BLOCKED — PRODUCT DECISION REQUIRED`; no formal verdict.
5. Zero unresolved blockers: formal verdict `APPROVED`.
6. Otherwise, if the player fantasy conflicts with the rule model, any open
   finding is `decision_kind: product-decision`, or at least three required
   sections are substantively missing: formal verdict `MAJOR REVISION NEEDED`.
7. Otherwise: formal verdict `NEEDS REVISION`.

An unresolved blocker is an `OPEN` blocker or blocker-level `WAIVED` finding.
Advisory and note findings do not prevent approval. A reviewer, specialist, user
risk acceptance, or director cannot override these rules.

---

## Phase 8: Return the mode-correct report and evidence

Generate one lowercase UUID review run ID and one exact UTC ISO-8601 timestamp
for the report. Use `codex-task:<review-run-id>` as reviewer identity unless the
runtime exposes a stronger stable task identity; never claim a person or task ID
that is unavailable.

All modes use this common body:

```markdown
## Design Review: <document title>

- Contract: cgs.design-review/v2
- Review Run ID: <lowercase UUID>
- Reviewed At: <UTC ISO-8601>
- Profile: system-gdd
- Target: design/gdd/<system-slug>.md
- Target System ID: <SYS-id or gdd:system-slug>
- Target SHA-256: <64-lowercase-hex>
- Requested/Effective Depth: <depth>/<depth>
- Review Type: first review | re-review
- Applicable Instructions: <root-to-target list>
- Approval Independence: independent | advisory-only

### Context Manifest
<loaded paths, exact byte totals, budget, omitted paths and reasons>

### Review Coverage
<primary and specialist status records; never invent a specialist for lean/solo>

### Completeness: <X>/8 substantive sections
<heading count, order, substantive result, evidence, failed assertions>

### Internal Consistency
<results>

### Implementability and Declared Interfaces
<results and exact dependency classifications>

### Findings
<complete normalized finding records, including prior RESOLVED findings>

### Convergence
- Prior unresolved blocker IDs: <IDs or none>
- Resolved this pass: <IDs or none>
- Unresolved blockers: <count and IDs>
- Revision-introduced regressions: <IDs or none>
- Maximum consecutive open re-reviews: <integer>

### Gate
<gate state or formal verdict selected by Phase 7>
```

Mode-specific rules:

- `lean`: coverage is `primary-reviewer: completed` and
  `specialists: not requested (lean)`. Include `### Verdict` only when Phase 7
  permits one formal verdict.
- `full`: list every selected specialist and status. Include `### Verdict` only
  when every selected specialist completed and Phase 7 permits a formal verdict.
- `solo`: coverage is `primary-reviewer: advisory analysis` and
  `specialists: not requested (solo)`. Gate is advisory and the `### Verdict`
  heading must be absent.
- `PARTIAL REVIEW` and `BLOCKED — PRODUCT DECISION REQUIRED` never render a
  `### Verdict` heading.

For every non-error completed report, hash the canonical report body above plus
any permitted `### Verdict` section, excluding the evidence block and Boundary.
Canonicalization is UTF-8, LF line endings, no trailing whitespace, field order as
shown, and exactly one final newline. Then append a `### Review Evidence` section
containing this literal fenced record:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<SHA-256 of this canonical record payload excluding record_id>
artifact_id: <SYS-id or gdd:system-slug>
artifacts:
  - path: design/gdd/<system-slug>.md
    sha256: <64-lowercase-hex>
reviewer: <stable reviewer identity>
review_run_id: <lowercase UUID>
review_depth: full | lean | solo
independence: independent | advisory-only
verdict: <APPROVED | NEEDS REVISION | MAJOR REVISION NEEDED | PARTIAL REVIEW | BLOCKED — PRODUCT DECISION REQUIRED | ADVISORY REVIEW — NOT APPROVAL>
timestamp: <UTC ISO-8601>
finding_ids: [<all stable finding IDs, sorted as reported>]
unresolved_blocker_ids: [<IDs or empty>]
report_payload_sha256: <SHA-256 of canonical report body>
producer:
  tool: design-review
  version: cgs.design-review/v2
```

Label the output fence `gate-evidence`. Canonicalize the evidence record with
UTF-8, LF endings, no trailing whitespace, the displayed field order, and one
final newline. Exclude the `record_id` line when computing `record_id`. Recompute
both hashes once and fail with `ERROR — EVIDENCE CONSTRUCTION FAILED` rather than
emitting inconsistent evidence. Downstream consumers must recompute target,
report-payload, and record hashes; a changed target or report makes approval
stale.

Finish every non-error report with:

```markdown
### Boundary
Read-only review complete. No source, index, review log, evidence artifact, or
other file was modified. This report applies only to target SHA-256 <hash>.
```

After returning the report, stop. If revision is required, state only that the
user may start a separate authoring/revision task with selected finding IDs and
then run an independent re-review in another fresh task with both required
re-review evidence arguments. Do not offer inline revision, status/log/index
updates, skip-review approval, or another review workflow.

## Authoritative P1 traceability

This matrix is documentary trace evidence only; it does not add behavior or
broaden the read-only contract.

| Audit ID | Closing contract clause |
|---|---|
| DR-006 | Phases 4 and 7 define mechanical severity, verdict, and precedence. |
| DR-007 | Phase 6 re-evaluates stable prior finding IDs instead of summaries. |
| DR-008 | Phases 6 and 8 bind approval evidence to exact target/report hashes. |
| DR-009 | Invocation defaults to lean; Phase 5 admits full review only by explicit high-risk rules. |
| DR-010 | Phases 4 and 5 type finding destinations and keep technical advice outside the GDD. |
| DR-011 | Phase 2 validates substantive section content rather than heading presence. |
| DR-012 | Phase 0 defines strict single-target arguments, path/profile validation, and error exits. |
| DR-013 | Phase 1 loads the complete root-to-target instruction chain with nearest precedence. |
| DR-014 | Phase 1 freezes bounded explicit context and reports uncovered scope. |
| DR-015 | Phase 5 caps and deterministically selects specialist fan-out. |
| DR-016 | Phase 5 defines deadlines, failures, PARTIAL coverage, and no-approval precedence. |
| DR-017 | Phase 8 renders mode-specific lean/full/solo output without fabricated roles. |
| DR-018 | Phase 1 classifies stable dependency identities as authored, planned, unknown, or broken. |
| DR-019 | The read-only contract and Phase 8 prohibit systems-index mutation and illegal status writes. |
| DR-020 | Phase 4 routes product decisions to the user and forbids reviewer-owned product changes. |
| DR-021 | Phase 3 and the final boundary keep whole-set consistency and theory in their owning workflows. |
| DR-022 | Phase 8 exposes hash-bound evidence while the formal spec keeps catalog results unexecuted until tested. |
