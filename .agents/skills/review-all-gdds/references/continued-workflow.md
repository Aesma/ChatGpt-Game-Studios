# Review All GDDs — Required workflow continuation

This file contains the remaining required phases. The frozen public contract,
mode matrix, and `cgs.cross-gdd-rules/v1` ruleset in the main `SKILL.md` govern
every step.

## Phase 4: Risk-scored cross-system scenario sample

Run this phase only when the mode matrix marks it `REQUIRED`. In `consistency`
mode it is `NOT_APPLICABLE`: do not generate candidates, spawn a scenario
worker, or emit experiential observations.

### 4a. Generate the complete candidate ledger

Use the typed event, state, dependency, resource, formula, and ownership graph
to generate, fingerprint, score, sort, and select candidates exactly as defined
by `cgs.cross-gdd-rules/v1`. Do not begin walkthroughs before the complete
candidate ledger exists.

Record for every candidate:

- stable scenario ID and normalized trigger;
- ordered system IDs and typed edges;
- evidence paths, sections, and hashes;
- each risk-score component and total score; and
- selection state: `SELECTED` or `UNSELECTED_SAMPLE_SCOPE`.

Select the deterministic top five, or every candidate when fewer than five
exist. Normal unselected candidates are declared sampling scope rather than
hidden coverage. If candidate generation, normalization, or scoring is
incomplete, list the missing graph scope and force `PARTIAL`.

### 4b. Walk every selected scenario

Assign selected scenarios to bounded workers using the standard
`cgs.cross-gdd-worker/v1` result. A worker receives only the scenario's graph
slice and exact-hash GDD inputs within the shard limits. For each scenario,
trace:

1. trigger and preconditions;
2. activation order and state transitions;
3. data/resource flow, ownership handoffs, units, and ranges;
4. player-visible or audible outcome; and
5. declared failure or recovery behavior.

Every claim cites stable system IDs, canonical paths, sections, and exact input
hashes. Verify the worker hash echo and account for every selected scenario. A
worker error, hash mismatch, budget overflow, or unchecked selected scenario is
a required coverage gap and forces `PARTIAL`.

### 4c. Classify only under the active mode

In `full` and `since-last-review`, apply the scenario rules from the matrix:

- `RAG.SCENARIO.EXPLICIT_CONTRADICTION` may be a blocker only when every
  deterministic proof condition holds;
- `RAG.SCENARIO.UNDEFINED_COMBINED_STATE` is a warning; and
- inferred balance, load, pacing, or strategy effects are advisory hypotheses.

In `design-theory`, deterministic consistency classification is forbidden.
Return only `HYPOTHESIS / ADVISORY` or `INFO`, with assumptions, a plausible
counterexample, and a validation plan. If a possible contradiction is noticed,
record it as an out-of-mode follow-up candidate without severity; do not inspect
it further or use it to change the verdict.

---

## Phase 5: Build one machine-consumable review report

The report has one authoritative machine block followed by human-readable
projections. The block is a fenced `gate-evidence` document so existing gate
consumers can parse the generic envelope; producer-specific data lives under
the versioned extension. Do not create a sidecar.

```gate-evidence
schema: cgs.review-evidence/v1
record_id: sha256:<canonical-record-payload>
artifact_id: system-gdd-set:<project-id-digest>:<manifest-prefix>
artifacts:
  - path: <canonical repository-relative path>
    sha256: <lowercase SHA-256 of exact bytes>
    role: system-gdd | game-concept | pillars | systems-index | approval-evidence | consistency-evidence
    system_id: <stable system ID or null>
reviewer: review-all-gdds:<run-id>
verdict: PASS | CONCERNS | FAIL | PARTIAL
timestamp: <ISO-8601 UTC>
finding_ids: [<stable XGDD IDs>]
producer:
  tool: review-all-gdds
  version: sha256:<ordered main/continuation/ruleset bundle digest>
extension:
  schema: cgs.cross-gdd-review/v2
  run_id: <UTC timestamp>-<manifest prefix>
  project_id: <canonical root plus repository identity>
  requested_mode: full | consistency | design-theory | since-last-review
  effective_scope: full | impact-closure
  source_revision:
    commit: <commit ID or null>
    input_state: clean | dirty | includes-untracked-inputs
  ruleset_id: cgs.cross-gdd-rules/v1
  ruleset_sha256: <exact ruleset bytes hash>
  skill_bundle_sha256: <ordered main/continuation/ruleset bytes digest>
  manifest_sha256: <ordered manifest digest>
  stale_key: <project/ruleset/mode/sorted-artifact-set digest>
  coverage_status: COMPLETE | PARTIAL
  limits:
    max_system_gdds: <effective value>
    max_typed_edges: <effective value>
    max_exact_input_bytes: <effective value>
    max_selected_scenarios: <effective value>
  approval_summary:
    approved_current: <count>
    provisional: <count>
    stale: <count>
    unbound_or_missing: <count>
  baseline:
    requested: <path or run ID or null>
    validated_run_id: <run ID or null>
    effective_fallback: <none or reason>
    changed_system_ids: []
    impact_system_ids: []
  consistency_evidence:
    path: <path or null>
    sha256: <hash or null>
    producer_verdict: <PASS | FINDINGS | PARTIAL | ERROR | null>
    currentness: CURRENT | STALE | UNBOUND | MISSING | NOT_APPLICABLE
  coverage:
    - check_id: <stable check ID>
      shard_id: <stable shard ID or null>
      status: DONE | PARTIAL | ERROR | NOT_APPLICABLE
      checked_scope: []
      unchecked_scope: []
      reason: <none or bounded reason>
  scenarios:
    candidates_total: <count>
    selected_ids: []
    unselected:
      - id: <scenario ID>
        score: <integer>
        reason: UNSELECTED_SAMPLE_SCOPE
  findings:
    - id: <stable XGDD ID>
      fingerprint_sha256: <hash>
      rule_id: <versioned rule ID>
      evidence_class: DETERMINISTIC | HYPOTHESIS | COVERAGE
      severity: BLOCKER | WARNING | ADVISORY | INFO | COVERAGE_GAP
      disposition: OPEN | ADVISORY | RESOLVED_IN_INPUT
      summary: <bounded summary>
      targets: []
      producer_finding_ids: []
      assumptions: []
      counterexamples: []
      validation_plan: <text or null>
      accepted_risk_record_ids: []
  accepted_risk_refs:
    - record_id: <separate verified record ID>
      path: <path>
      sha256: <hash>
      finding_ids: []
      scope: <bounded scope>
      owner: <owner identity>
      signature: <verifiable signature/identity evidence>
      expires_at: <timestamp>
      status: CURRENT | EXPIRED | STALE | UNBOUND
```

### 5a. Canonical record identity

Compute `record_id` as SHA-256 over canonical JSON of the complete
`gate-evidence` object with `record_id` omitted. Sort object keys
lexicographically. Preserve array semantics, but first sort:

- `artifacts` by path, role, then system ID;
- `finding_ids` and all ID-only arrays lexicographically;
- `coverage` by check ID then shard ID; and
- `findings` by finding ID.

Use UTF-8, lowercase hexadecimal hashes, no insignificant whitespace, and JSON
`null` rather than omitted required fields. Recompute the digest after final
verdict and coverage are known. The human-readable projection is not part of
the canonical record payload.

### 5b. Accepted-risk references

Default `accepted_risk_refs` to an empty list. Include a reference only when a
separate record is project-local, owner-signed, names this exact run or finding
IDs, has bounded scope and expiry, and its exact hash and currentness can be
verified. Missing, expired, stale, or unbound records confer no exception.

Never create, sign, or repair a risk record. Never set a finding disposition to
accepted risk. A referenced risk does not change this review's finding,
severity, coverage, or verdict; only a downstream gate applies its own policy.

### 5c. Human-readable projection

After the machine block, render all of these sections from the same normalized
data:

1. **Run Identity** — project, run, requested mode, effective scope, source
   revision, ruleset, manifest digest, stale key, and verdict.
2. **Input and Approval Manifest** — every included/excluded system, exact hash,
   approval record/currentness, priority, and role.
3. **Incremental Scope** — baseline validation, deltas, graph-closure members,
   tombstones, or the exact full-fallback reason.
4. **Coverage and Shards** — every planned check/shard, worker status, checked
   and unchecked scope, and `NOT_APPLICABLE` mode rows.
5. **Deterministic Findings** — stable IDs, rule IDs, exact evidence, severity,
   disposition, producer IDs, and acceptance conditions.
6. **Game-Design Hypotheses** — evidence, assumptions, counterexamples,
   validation plans, and `NEEDS_MEASUREMENT` markers.
7. **Scenario Candidate Ledger and Walkthroughs** — total, score breakdown,
   selected results, and every unselected candidate/reason.
8. **Accepted-Risk References** — verified records or `None`; explicitly state
   that they do not rewrite the verdict.
9. **Staleness Contract** — exact recomputation rule and the statement that a
   stale record is not gate evidence.
10. **Verdict** — one formal run verdict and the mechanical reason.

The machine block and projection must agree exactly. Any mismatch discovered
before delivery is an evidence conflict and forces `PARTIAL` until corrected in
the same in-memory report.

---

## Phase 6: Compute the verdict mechanically

Apply the verdict precedence in `cgs.cross-gdd-rules/v1` only after all
required-mode checks, shards, workers, scenario candidates, and merges have a
coverage status.

- `PARTIAL` takes precedence over proven blockers. Preserve those blockers in
  the report, but do not present the lower-priority `FAIL` as the run verdict.
- With complete coverage, one `BLOCKER / OPEN` produces `FAIL`.
- With complete coverage and no blocker, any warning, advisory hypothesis, or
  validation item produces `CONCERNS`.
- `PASS` requires complete applicable coverage and no blocker, warning,
  advisory hypothesis, or unresolved validation item.

An invalid invocation or fewer than two reviewable GDDs ended before this phase
and has no run verdict.

---

## Phase 7: Deliver or persist only the report

Always render the complete report in conversation first.

If the user asks to persist it, preview exactly one new path and obtain explicit
approval before writing:

`design/gdd/gdd-cross-review-<UTC timestamp>-<manifest-prefix>.md`

The path must not exist. Refuse overwrite. Do not silently select a replacement
path after a collision; generate a new run/path proposal and obtain new
approval. A correction is a new immutable report whose extension names
`supersedes_run_id`; it never edits the prior report. After the authorized write,
read it back, parse the `gate-evidence` block, recompute `record_id`, manifest
digest, and saved file hash, then report verification.

Write no sidecar. Under every outcome, do not modify or create source GDDs,
systems index, registry, session state, lifecycle status, approval/sign-off,
accepted-risk records, or any other report. Declining persistence causes zero
file mutations.

---

## Phase 8: One handoff and stop

Offer exactly one separate next action, then include `Stop here`:

- `FAIL`: route the highest-priority deterministic finding ID to its artifact
  owner for a separate remediation and fresh approval/review.
- `PARTIAL`: restore the highest-priority named evidence or coverage gap, then
  rerun this workflow.
- `CONCERNS`: run the highest-priority validation plan or obtain the named owner
  decision; a downstream gate decides advancement policy.
- `PASS`: offer `$gate-check` or `$create-architecture` with the current
  `record_id`, run ID, and stale key.

The handoff is not permission to edit, advance stage, sign risk, or run another
workflow automatically.

## Error recovery protocol

If a worker is blocked, errors, returns mismatched hashes, exceeds a limit, or
omits required checks:

1. retain its raw status and reason;
2. mark the exact shard/check/input as unchecked;
3. continue only independent planned work;
4. merge all completed evidence without inventing coverage;
5. return `PARTIAL`; and
6. recommend one bounded evidence-restoration action.

Never retry by widening a shard, passing the whole corpus, suppressing the
failed check, or changing mode. Never produce `PASS` from incomplete work.

## Collaborative protocol

1. Hash and inventory before analysis.
2. Keep product decisions with the owner.
3. Keep deterministic evidence, hypotheses, and coverage gaps distinct.
4. Expose all selected and unselected scope.
5. Use one optional immutable report write only.
6. Preserve reviewer/recorder/author separation.
7. Stop after one evidence-based handoff.
