# Architecture Review — Required workflow continuation

This continuation is part of `$architecture-review`. The main contract and
`cgs.architecture-review-rules/v1` govern every phase. This file may format and,
after exact authorization, save one immutable report; it never repairs or
records changes in reviewed sources.

## Phase 8: Build one machine-consumable immutable report

The report begins with one authoritative fenced `gate-evidence` block. Its
generic envelope is consumable by gate tooling; architecture-specific evidence
is stored under a versioned extension. Do not create a sidecar.

```gate-evidence
schema: cgs.review-evidence/v1
record_id: sha256:<canonical-record-payload>
artifact_id: architecture-traceability:<project-digest>:<mode>:<manifest12>
artifacts:
  - path: <canonical project-relative path>
    sha256: <lowercase complete-file SHA-256>
    role: GDD | systems-index | requirement-registry | ADR | architecture-derived | engine-reference | project-standard | story | test-source | test-run
    source_id: <stable ID or null>
reviewer: architecture-review:<run-id>
verdict: PASS | BLOCKED | PARTIAL
timestamp: <ISO-8601 UTC with fractional seconds>
finding_ids: [<stable ARCH finding IDs>]
producer:
  tool: architecture-review
  version: sha256:<ordered main/continuation/ruleset bundle digest>
extension:
  schema: cgs.architecture-review/v2
  run_id: AR-<compact UTC fractional timestamp>-<manifest12>-<UUIDv4>
  project_id: <canonical repository root plus repository identity>
  mode: full | coverage | consistency | engine | single-gdd | rtm
  target:
    selector: <path:... | id:... | null>
    resolved_id: <stable ID or null>
    resolved_path: <canonical path or null>
  source_revision:
    commit: <commit ID or null>
    input_state: clean | dirty | includes-untracked-inputs
  ruleset_id: cgs.architecture-review-rules/v1
  ruleset_sha256: <exact ruleset bytes hash>
  skill_bundle_sha256: <ordered main/continuation/ruleset bytes digest>
  target_manifest_hash: <canonical ordered manifest digest>
  stale_key: <project/mode/target/ruleset/sorted-artifact-set digest>
  coverage_status: COMPLETE | PARTIAL
  limits:
    max_artifacts_per_shard: <effective value>
    max_index_records_per_shard: <effective value>
    max_typed_edges_per_shard: <effective value>
    max_exact_input_bytes_per_shard: <effective value>
    max_snapshot_paths_per_batch: <effective value>
    max_reviewers: <effective value>
  input_classes:
    - class: <input class>
      applicability: REQUIRED | OPTIONAL | NOT_APPLICABLE
      presence: PRESENT | MISSING | NOT_APPLICABLE
      currentness: CURRENT | STALE | UNREADABLE | UNKNOWN | NOT_APPLICABLE
      paths: []
      reason: <explicit evidence>
  manifest_entries:
    - path: <canonical path>
      sha256: <hash>
      source_type: <type>
      source_id: <ID or null>
      source_revision: <commit or WORKTREE>
      scope: []
      currentness: <state>
  coverage:
    - check_id: <stable check ID>
      shard_id: <stable shard ID or null>
      status: DONE | PARTIAL | ERROR | NOT_APPLICABLE
      checked_scope: []
      unchecked_scope: []
      reason: <none or bounded reason>
  reviewers:
    - role: <role>
      status: DONE | DECLINED | TIMEOUT | ERROR | NOT_APPLICABLE
      target_manifest_hash: <hash or null>
      completed_check_ids: []
      unchecked_scope: []
  requirement_baseline:
    admitted_ids: []
    candidate_finding_ids: []
    unverified_ids: []
  traceability:
    - requirement_id: <ID>
      adr_ids: []
      coverage_state: VERIFIED_COVERED | VERIFIED_GAP | UNVERIFIED_LINK
      story_ids: []
      test_ids: []
      test_run_ids: []
  test_evidence:
    - test_id: <ID>
      state: EXECUTED_PASS | EXECUTED_FAIL | STALE_RUN | DISCOVERED_NOT_EXECUTED | MISSING_EVIDENCE | NOT_APPLICABLE
      run_id: <ID or null>
      target_hash: <hash or null>
  findings:
    - id: <stable ARCH ID>
      fingerprint_sha256: <hash>
      rule_id: <versioned rule ID>
      evidence_class: DETERMINISTIC | INCOMPLETE | INFORMATIONAL
      severity: BLOCKER | INCOMPLETE | INFO
      disposition: OPEN | INFORMATIONAL | RESOLVED_IN_INPUT
      summary: <bounded statement>
      targets: []
      destination_owner: <owner>
      acceptance_test: <objective test>
      producer_finding_ids: []
      reviewer_roles: []
      accepted_risk_record_ids: []
  blocker_reason_codes: []
  incomplete_reason_codes: []
  mutation_guard:
    baseline: COMPLETE | INCOMPLETE
    final: PASSED | FAILED | INCOMPLETE
    unauthorized_paths: []
  accepted_risk_refs:
    - record_id: <separate record ID>
      path: <path>
      sha256: <hash>
      finding_ids: []
      scope: <exact scope>
      target_manifest_hash: <hash>
      owner: <identity>
      signature: <verifiable identity evidence>
      signed_at: <timestamp>
      expires_at: <timestamp>
      status: CURRENT | EXPIRED | STALE | UNBOUND
```

Default `accepted_risk_refs` to `[]`. Include a risk reference only after its
separate exact record validates. It does not alter findings, reason codes,
coverage, or verdict.

### 8a. Canonical record identity

Compute `record_id` as SHA-256 over canonical JSON of the complete
`gate-evidence` object with `record_id` omitted. Sort object keys
lexicographically. Before serialization, sort:

- `artifacts` and `manifest_entries` by path, role/type, then source ID;
- ID-only arrays lexicographically;
- `input_classes` by class;
- `coverage` by check ID then shard ID;
- `reviewers` by role;
- `traceability` by requirement ID; and
- `findings` by stable finding ID.

Use UTF-8, lowercase hash hex, no insignificant whitespace, and explicit JSON
`null` for required empty values. Recompute after the final mutation-guard state
and verdict are known. The human projection and saved report file hash are not
part of the record payload.

### 8b. Human-readable projection

Render these sections from the same normalized data:

1. **Run Identity** — record/run IDs, mode, exact target, project/source
   revision, ruleset and producer hashes, target manifest hash, stale key, and
   verdict.
2. **Input-Class Ledger** — every class's applicability, presence, currentness,
   paths, and reason, including missing and not-applicable classes.
3. **Target Manifest** — every actual review input with type, stable ID, path,
   hash, revision, currentness, and consumed scope.
4. **Coverage and Shards** — every planned artifact/index/group/edge/check,
   shard limits, completed and unchecked scope, and mode-forbidden
   `NOT_APPLICABLE` rows.
5. **Reviewer Ledger** — exact profile, role status, manifest hash, checks, and
   unchecked scope.
6. **Requirement Baseline** — admitted IDs, candidate requirements, registry
   drift, unknown classification, and source-owner evidence.
7. **Traceability and Execution** — exact Requirement→ADR→Story→Test→Run states
   allowed by the mode.
8. **Consistency/Dependency/Engine Results** — only mode-applicable keyed checks
   with exact evidence.
9. **Findings** — stable IDs, rules, outcome, disposition, exact sources,
   destination owner, and acceptance tests.
10. **Accepted-Risk References** — verified records or `None`, with the explicit
    statement that they do not rewrite the verdict.
11. **Mutation Guard and Staleness** — baseline/final state, any unauthorized
    paths, and exact stale-key recomputation rule.
12. **Verdict** — one formal verdict plus blocker/incomplete reason codes.

The projection must exactly match the machine block. A mismatch discovered
before delivery is `AR.REVIEWER.EVIDENCE_CONFLICT`-class incomplete evidence and
prevents `PASS` until corrected in memory.

The report must state:

- implicit/prose-similar links are `UNVERIFIED_LINK`;
- test-source existence is `DISCOVERED_NOT_EXECUTED`;
- only current `EXECUTED_PASS` is passing evidence;
- derived architecture/index text never overrules source authority;
- accepted risk is separate and cannot change the verdict; and
- any manifest, mode, target, scope, or ruleset-hash change makes it `STALE`.

---

## Phase 9: Present before optional save

Present the complete machine block and projection in conversation first.

Default behavior is zero writes. If the user asks to save, propose exactly:

`docs/architecture/reviews/architecture-review-<compact-UTC-fractional>-<manifest12>-<uuid8>.md`

The compact timestamp is `YYYYMMDDTHHMMSSffffffZ`, using six fractional digits;
`uuid8` is the first eight lowercase hex characters of the run UUID. Preserve
the full UUID in the machine record. Confirm the path does not exist, show it as
the complete changeset, and obtain explicit approval before the first write.

Create only that report. Do not create/update a latest pointer, review index,
parent policy, registry, lifecycle record, traceability artifact, status, log,
sign-off, risk record, or session state. Re-read saved bytes, parse and
recompute `record_id` and `target_manifest_hash`, compute the saved file
SHA-256, and report all three. The file hash is returned in conversation, not
embedded self-referentially.

If the proposed path already exists, refuse overwrite/append/rename. Generate a
new run ID and path proposal only in a fresh approval exchange. Never select an
existing report by a vague “latest” rule.

---

## Phase 10: Final mutation guard and verdict finalization

Immediately before returning:

1. repeat the Phase 0 streaming tree snapshot using the same path batches;
2. compare every project-relative path, size, and SHA-256;
3. permit no difference for conversational output;
4. after authorized save, permit only the exact new report path;
5. list every unauthorized added/removed/changed path; and
6. set final guard state before canonicalizing the report record.

An actual unauthorized difference is `FAILED`, adds
`AR.MUTATION.UNAUTHORIZED_CHANGE`, and yields `BLOCKED`. Inability to complete
the comparison without proof of change is `INCOMPLETE` and yields `PARTIAL` when
no blocker exists. Never hide, repair, revert, or normalize a difference.

Because the conversational report was rendered before an optional save, update
the final machine block/projection in conversation with final guard state,
verdict, and record ID. If a saved pre-guard report no longer matches final
state, do not overwrite it: mark that saved artifact unusable/incomplete and
return the corrected final evidence only in conversation. A later persistence
attempt requires a new immutable run and authorization.

---

## Phase 11: Prior-report currentness and risk disposition

For an explicitly identified prior record, recompute its exact mode, target,
ruleset hash, input classes, manifest entries, target manifest hash, and stale
key. Return `CURRENT` only when all reproduce. Otherwise return `STALE` with the
exact differences. A stale report has no current gate value.

If a separate accepted-risk record is supplied, verify record/report/finding
IDs, file hash, target manifest, exact scope, owner/signature, signed timestamp,
and expiry. Report `CURRENT`, `EXPIRED`, `STALE`, or `UNBOUND` separately. Never
create, sign, renew, store, or use it to rewrite the review.

---

## Phase 12: One handoff and stop

Return:

- record ID, run ID, target manifest hash, and stale key;
- saved report path/file hash if one was successfully authorized and verified;
- `PASS`, `BLOCKED`, or `PARTIAL` with exact reason codes;
- the single highest-priority open finding and actual destination owner; and
- one fresh-task recommendation.

For `BLOCKED`, route one confirmed blocker. For `PARTIAL`, route the highest
priority missing/unknown/failed evidence item. For `PASS`, offer the consuming
gate with this exact current record. Do not invoke the handoff, update any
status/index/session record, or automatically rerun after another ADR. Include
`Stop here` and stop.

## Error recovery

If a shard or reviewer declines, times out, errors, mismatches hashes, exceeds a
limit, or omits a check:

1. preserve its raw status and evidence;
2. mark the exact artifact/group/edge/check as unchecked;
3. continue only independent planned work;
4. never widen a shard or substitute an unplanned reviewer;
5. preserve any independently proven blockers; and
6. compute `BLOCKED` for a proven blocker, otherwise `PARTIAL`.

Never produce `PASS` from incomplete work.
