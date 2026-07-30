# Gate Check — Required Workflow Continuation

This file is normative. Read it in full only after the main skill has completed
profile evaluation, director handling, deterministic verdict calculation,
Chain-of-Verification, and the initial mutation guard.

## Phase 7: Present the human-readable assessment

Present one compact report before the machine record:

```markdown
## Gate Check: <transition-id> — <current stage> → <candidate stage>

- Profile: <profile-id>
- Selection: <EXPLICIT | AUTHORITY_AUTO_CONFIRMED>
- Authority: <record path>@<revision> (schema <version>)
- Legacy stage declaration (`LEGACY_DECLARATION`): <NONE | value/path/revision; advisory only>
- Review mode: <full | lean | solo>
- Scope: <included count>; <excluded count>; <coverage gaps count>
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- Coverage: <COMPLETE | PARTIAL>

### Blocking checks
| Check ID | Status | Expected | Observed | Evidence/finding IDs |
|---|---|---|---|---|

### Advisory checks
| Check ID | Status | Risk | Evidence/finding IDs |
|---|---|---|---|

### Director advisory panel
| Gate ID | Status | Native verdict | Finding IDs |
|---|---|---|---|

### Coverage gaps
- <reason code, exact unchecked scope, destination owner>

### Verdict: <PASS | CONCERNS | FAIL | PARTIAL>
- Decision-table row: <1 | 2 | 3 | 4>
- Advancement disposition: <ELIGIBLE | NOT_ELIGIBLE>
- Chain-of-Verification: <verdict unchanged | old → new; evidence IDs>
- Stage mutated: false
```

List every selected profile check exactly once, followed by common director checks
`DIR-C01`, `DIR-T01`, `DIR-P01`, and `DIR-A01`. Never count `NOT_APPLICABLE` as a
pass, hide PARTIAL coverage behind a percentage, or describe CONCERNS/FAIL/PARTIAL
as passed. `ELIGIBLE` applies only to PASS; the other verdicts are
`NOT_ELIGIBLE`, regardless of accepted risk.

## Phase 8: Emit one immutable gate record

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

```yaml
schema: cgs.gate-record/v2
record_id: <stable allocated ID>
run_id: <stable run ID>
generated_at: <ISO-8601 timestamp with timezone>
gate:
  tool: gate-check
  version: cgs.gate-check/p1-v2
transition:
  transition_id: <exact ID>
  current_stage: <catalog-authority stage>
  candidate_next_stage: <catalog edge candidate>
  profile_id: <selected profile ID>
  selection_mode: EXPLICIT | AUTHORITY_AUTO_CONFIRMED
  auto_selection_confirmed: true | false | null
authority:
  catalog_path: <path>
  catalog_revision: <revision>
  stage_schema_version: <version>
  transition_graph_version: <version>
  record_path: <path>
  record_revision: <revision>
  owner: <validated owner>
  source_snapshot_revision: <revision>
  prior_record_revision: <revision-or-null-under-schema>
  receipt_id: <validated receipt ID or null under schema>
  receipt_revision: <revision or null under schema>
legacy_declaration:
  path: production/stage.txt | null
  revision: <revision-or-null>
  value: <value-or-null>
  relationship: ABSENT | AGREES_ADVISORY_ONLY | CONTRADICTS_AUTHORITY
snapshot:
  repository_id: <canonical identity>
  source_revision: <commit/ref-or-UNVERIFIED>
  dirty_state: <clean|dirty|UNVERIFIED>
  started_at: <ISO-8601>
  finalized_at: <ISO-8601>
review_mode: full | lean | solo
scope:
  manifest_<stable allocated ID>
  manifest_entries: <integer>
  included: [<path/role/revision/read-mode records>]
  excluded: [<path/rule/reason records>]
  unreadable: [<path/reason records>]
  ambiguous: [<identity/candidate records>]
  budget:
    manifest_entries: {used: <n>, limit: <n>}
    full_content_files: {used: <n>, limit: <n>}
    context_bytes: {used: <n>, limit: <n>}
    content_read_bytes: {used: <n>, limit: <n>}
    tool_actions: {used: <n>, limit: <n>}
    elapsed_seconds: {used: <n>, limit: <n>}
checks:
  - check_id: <stable profile check ID>
    class: BLOCKING | ADVISORY
    coverage_required: true | false
    source: DETERMINISTIC | PRODUCER_RECORD | ATTESTATION | DIRECTOR
    status: PASS | FAIL | ADVISORY | UNKNOWN | NOT_EVALUATED | NOT_APPLICABLE | UNBOUND | STALE
    expected: <profile predicate>
    observed: <redacted exact observation>
    artifact_revision: [<current revisions>]
    evidence_record_ids: [<IDs>]
    producer_adapter_id: <adapter ID or null>
    producer_native_verdict: <exact native value or null>
    attestation_ids: [<IDs>]
    finding_ids: [<stable IDs>]
    reason_code: <stable reason>
attestations:
  - <complete cgs.gate-attestation/v1 or empty>
director_panel:
  required_by_mode: true | false
  coverage: COMPLETE | PARTIAL
  results:
    - gate_id: <ID>
      agent_role: <role>
      attempt: 1
      scope_manifest_revision: <revision>
      started_at: <time-or-null>
      ended_at: <time-or-null>
      native_verdict: READY | CONCERNS | NOT_READY | null
      status: COMPLETE | TIMEOUT | BLOCKED | ERROR | MALFORMED | STALE | NOT_APPLICABLE_BY_MODE
      finding_ids: [<IDs>]
findings:
  - finding_id: <stable profile/run finding ID>
    check_id: <check ID>
    severity: BLOCKING | ADVISORY | COVERAGE_GAP
    status: OPEN | RESOLVED | ACCEPTED_RISK_REQUESTED
    evidence_location: <path/revision/field or panel result>
    destination_owner: <owner>
    acceptance_test: <specific test>
coverage:
  status: COMPLETE | PARTIAL
  gaps: [<reason code and exact unchecked scope>]
decision:
  table_row: 1 | 2 | 3 | 4
  verdict: PASS | CONCERNS | FAIL | PARTIAL
  advancement_disposition: ELIGIBLE | NOT_ELIGIBLE
verification:
  high_risk_rechecks: [<check/evidence/action/result>]
  check_set_complete: true
  final_reread_passed: true
  draft_verdict: <verdict>
  final_verdict: <verdict>
mutation_guard:
  status: PASSED
  observed_external_changes: [<paths-or-empty>]
stage_mutated: false
```

The record retains every UNBOUND, STALE, unknown, not-evaluated, advisory, panel,
and coverage finding. Do not store the record in the repository, update a latest
pointer, or call it a stage receipt. A stage-advancement workflow must independently
verify the record ID and currentness.

## Phase 9: Final currentness and mutation recheck

Immediately before returning:

1. Re-read the catalog and authority record and require their revisions to equal the
   record. If authority changed, discard the draft gate record and return
   `ERROR — AUTHORITY CHANGED DURING CHECK`; do not emit a stale record.
2. re-read every scope entry and accepted evidence/attestation dependency required
   by the profile. If any differs, update the affected status to STALE or the scope
   gap to SNAPSHOT_CHANGED, rerun the decision table and record ID, then recheck
   once. Do not loop.
3. Repeat the mutation guard. The only permitted changes are independently caused
   external changes already reported; this workflow itself must have changed
   nothing. If attribution is uncertain, report mutation guard FAILED and do not
   claim a valid assessment.
4. Confirm `stage_mutated: false` and that stage authority/history bytes are
   unchanged by this workflow.

Never repair concurrent changes, refresh evidence, or rerun a producer inside
this workflow.

## Phase 10: Optional accepted-risk request

PASS needs no risk request. After CONCERNS, FAIL, or PARTIAL, emit a request only
if the user explicitly identifies the accountable operator and accepts every
named finding/coverage gap they intend to carry. Do not infer acceptance from a
request to continue, a previous conversation, or a director response.

Keep the immutable gate record unchanged and emit:

```yaml
schema: cgs.advance-request/v2
request_id: <stable allocated ID>
transition_id: <exact transition ID>
profile_id: <profile ID>
gate_record_id: <cgs.gate-record/v2 ID>
gate_verdict: CONCERNS | FAIL | PARTIAL
gate_coverage: COMPLETE | PARTIAL
requested_disposition: PROCEED_WITH_ACCEPTED_RISK
operator: <explicit accountable user identity>
identity_assurance: USER_ASSERTED | VERIFIED
timestamp: <ISO-8601 with timezone>
authority_record_revision: <revision used by gate>
scope_manifest_revision: <revision used by gate>
accepted_finding_ids: [<explicit IDs>]
accepted_coverage_gap_ids: [<explicit IDs>]
evidence_record_ids: [<IDs from gate record>]
stage_mutated: false
```

An omitted open blocker/gap remains unaccepted and must be named. The request does
not make the gate eligible and is not authority to mutate. Only an independent,
explicitly authorized stage-advancement workflow may validate policy, compare-and-
set the current authority record, preserve verdict/risk fields, append history,
and atomically commit. If none exists, state that no advancement occurred.

## Phase 11: Bounded recovery rules

- Tool failure or budget exhaustion: keep completed checks, mark exact required
  scope NOT_EVALUATED, calculate FAIL-with-partial-coverage or PARTIAL, and stop.
- Director timeout/block/error/malformed/stale: preserve available results,
  panel coverage PARTIAL in lean/full, calculate deterministically, and stop.
- Unanswered/ambiguous attestation: retain UNKNOWN/NOT_EVALUATED; never ask in a
  loop or manufacture an identity.
- Late evidence or director response after the final manifest freeze: exclude it
  as late/stale. A new assessment requires a new run/record ID.
- Concurrent source change: perform the one final reclassification/recalculation
  described above, then stop. Never auto-retry the whole gate.
- Compaction/interruption before record emission: recover only from re-read
  immutable project inputs and explicit conversation records still available;
  if exact run state cannot be reconstructed, return PARTIAL without claiming the
  lost checks passed.

Always return a partial report when some bounded work completed. Never silently
skip, substitute a role, expand scope, or turn incomplete work into PASS.

## Phase 12: One next action and stop

End with at most one prioritized action plus `Stop here`; do not print a pipeline,
invoke a skill, spawn remediation, edit files, or rerun the gate.

- PASS: recommend a separately authorized stage-advancement workflow that consumes
  this exact current gate record, or Stop.
- CONCERNS: recommend resolving the highest-priority advisory finding, or Stop.
- FAIL: recommend resolving the highest-priority blocking finding according to its
  destination owner/acceptance test, or Stop.
- PARTIAL: recommend supplying/resolving the highest-priority coverage gap, or Stop.

State plainly: `Gate assessment complete; project stage was not changed.`
