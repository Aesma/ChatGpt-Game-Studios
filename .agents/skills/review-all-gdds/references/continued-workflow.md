# Review All GDDs — Required workflow continuation

This file contains required phases of `$review-all-gdds`. Read it in full when
the main `SKILL.md` reaches its Required continuation section, then execute the
phases in order. The frozen public contract in `SKILL.md` governs every phase.

## Phase 4: Cross-System Scenario Walkthrough

Walk through the game from the player's perspective to find problems that only
appear at the interaction boundary between multiple systems. This phase is part
of the declared review coverage; it is not a third verdict vocabulary or a
license to edit source documents.

### 4a: Identify Key Multi-System Moments

Scan the hashed input manifest and identify the 3–5 most important player-facing
moments where multiple systems activate simultaneously. Look specifically for:

- **Combat + Economy overlap:** rewards, spending, death, and respawn state
- **Progression + Difficulty overlap:** level changes, unlocks, and scaling
- **Narrative + Gameplay overlap:** choices, state changes, and interruptions
- **3+ system chains:** an event flowing through three or more systems

List each selected scenario and why it was selected. Also state that this is a
sample, not exhaustive scenario coverage.

### 4b: Walk Through Each Scenario

For each scenario, step through:

1. **Trigger** — the player action or game event
2. **Activation order** — the systems and their sequence
3. **Data flow** — outputs, inputs, units, and ranges
4. **Player experience** — visible or audible outcomes
5. **Failure modes** — race conditions, feedback loops, broken transitions,
   contradictory messaging, compounding spikes, reward conflicts, or undefined
   combined behavior

Every claim must cite canonical input paths, sections, and the manifest hashes
used. A missing combined-state rule is a coverage gap or concern; it is not
automatically proof that runtime behavior is broken.

### 4c: Classify Scenario Evidence

- **BLOCKER:** only a reproducible contradiction or violation of an explicit
  anti-pillar, owner-approved invariant, or owner-approved threshold. Cite the
  exact conflicting rules and hashed inputs.
- **WARNING:** a non-blocking deterministic gap or compatibility concern.
- **HYPOTHESIS / ADVISORY:** an inferred experience, balance, load, or strategy
  risk. Include assumptions, a counterexample, and a validation plan.
- **INFO:** ordering or messaging notes without demonstrated conflict.

If required scenarios cannot be completed, record the unchecked scope and use
the overall verdict `PARTIAL`. Do not turn uncertainty into a blocker.

---

## Phase 5: Build the Review Report

The report must use the following evidence envelope and sections:

```yaml
schema: cgs.cross-gdd-review/v1
run_id: [UTC timestamp]-[manifest digest prefix]
project_id: [canonical repository root + repository identity]
generated_at_utc: [ISO-8601]
mode: [full | consistency | design-theory | since-last-review]
verdict: [PASS | CONCERNS | FAIL | PARTIAL]
source_revision:
  commit: [commit ID or null]
  input_state: [clean | dirty | includes-untracked-inputs]
manifest_sha256: [SHA-256 of ordered input manifest]
coverage_status: [COMPLETE | PARTIAL]
supersedes_run_id: [run ID or null]
```

### Input Manifest

| Canonical input path | SHA-256 | Role |
|---|---|---|
| [path] | [hash] | [system-gdd / pillars / systems-index / registry / other] |

### Coverage

| Required phase/check | Status | Checked scope | Unchecked scope / reason |
|---|---|---|---|
| [check] | DONE / PARTIAL / ERROR / NOT_APPLICABLE | [paths/rules] | [none or gap] |

### Consistency Issues

Separate deterministic blockers from non-blocking warnings. Each issue must cite
the exact paths, sections, rules, and hashes involved.

### Game Design Hypotheses

Every theory item is labeled `HYPOTHESIS / ADVISORY` and contains evidence,
assumptions, a plausible counterexample or compensating mechanic, and a
validation plan. A theory item may move to Blocking only when it demonstrates a
current, reproducible violation of an explicit anti-pillar, owner-approved
invariant, or owner-approved threshold in the manifest.

### Cross-System Scenario Issues

List scenarios walked, deterministic issues, advisory hypotheses, and unchecked
scenario scope.

### GDDs Referenced by Findings

This is evidence only. It does not authorize changing a GDD or its lifecycle
status.

| GDD | Finding summary | Evidence class | Severity |
|---|---|---|---|
| [path] | [summary] | Deterministic / Hypothesis | Blocking / Warning / Advisory |

### Staleness Contract

This report is current only while `project_id` and the complete canonical
path/SHA-256 manifest match the project. Any input addition, removal, rename, or
content-hash change makes it `STALE`. A stale report, including a stale
`PASS`, is not gate evidence and must not authorize architecture.

### Verdict: [PASS / CONCERNS / FAIL / PARTIAL]

- **PASS:** all required checks for the selected mode completed; no blocking or
  non-blocking issues remain.
- **CONCERNS:** all required checks completed; no blockers, but warnings or
  advisory hypotheses remain.
- **FAIL:** all required checks completed and one or more deterministic blocking
  violations remain.
- **PARTIAL:** required input or coverage is missing, a worker failed, hashes do
  not match, or evidence conflicts remain unresolved. `PARTIAL` must never be
  represented as `PASS`.

A `FAIL` verdict is immutable for this run. It cannot be waived, renamed, or
rewritten as `PASS`. If project governance permits proceeding, a separate
owner-signed `ACCEPTED_RISK` record must name the run ID, exact findings,
scope, owner identity/signature, and expiry. The reviewer never signs it for the
owner, and the separate record does not change this report's verdict.

---

## Phase 6: Deliver or Persist Only the Review Report

Always render the complete report in conversation first.

If the user asks to persist it, preview exactly one new path and obtain explicit
approval before writing. Use a unique immutable path such as:

`design/gdd/reviews/gdd-cross-review-[UTC timestamp]-[manifest-prefix].md`

The path must not already exist. Never overwrite or amend a prior report; a
correction creates a new report with `supersedes_run_id`. After approval,
write only that report and verify its saved manifest digest. If the user declines
or does not authorize the write, perform zero file mutations.

Under all outcomes, do **not** modify or create:

- any source GDD;
- `design/gdd/systems-index.md` or any lifecycle/status field;
- an entity registry or consistency baseline;
- `production/session-state/active.md` or any session/state file;
- sign-off, approval, waiver, or accepted-risk records.

Status transitions and accepted-risk records belong to independent,
owner-authorized recorders that consume the immutable review evidence.

---

## Phase 7: Handoff and Stop

Offer one separate next workflow; do not edit source content inside this review.

- `FAIL`: recommend the owner choose a remediation workflow for the highest
  priority deterministic blocker, then rerun this review.
- `PARTIAL`: recommend resolving the named evidence/coverage gap, then rerun.
- `CONCERNS`: recommend owner review or the validation plan for the highest
  priority concern; architecture may proceed only under the consuming gate's
  policy and with a current report.
- `PASS`: offer `$gate-check` or `$create-architecture` with the
  current run ID and manifest digest.

Always include `Stop here`. The handoff is a recommendation, not permission
for this reviewer to modify GDDs, indexes, session state, or governance records.

---

## Error Recovery Protocol

If any spawned agent is blocked, errors, returns mismatched hashes, or fails to
complete:

1. Surface the worker status and reason.
2. Record affected checks and inputs as unchecked.
3. Continue only where independent evidence permits.
4. Produce the available report with verdict `PARTIAL`.
5. Offer retry with narrower scope, resolve the blocker, or stop.

Never hide missing coverage and never produce `PASS` from partial work.

---

## Collaborative Protocol

1. **Read silently** — load and hash all inputs before presenting findings.
2. **Show everything** — present consistency, theory, scenario, and coverage
   evidence before asking whether to persist the report.
3. **Distinguish deterministic from advisory** — unmeasured theory is a
   hypothesis, not an architecture blocker.
4. **Do not make product decisions** — surface evidence and validation options.
5. **One optional write** — only an explicitly authorized new immutable report.
6. **No lifecycle or session mutation** — reviewer and recorder roles remain
   separate.
7. **Be specific** — every deterministic finding cites exact paths, sections,
   rules, and hashes.
