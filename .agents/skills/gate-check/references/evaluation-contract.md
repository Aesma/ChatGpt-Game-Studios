# Gate Check — Deterministic Evaluation Contract

This contract is normative for `$gate-check`. Read it in full after transition and
stage-authority validation and before evaluating a transition profile. If this file
conflicts with prose examples elsewhere in the skill, this file controls check
normalization, coverage, verdict calculation, director handling, and attestations.

## 1. Result domains

Keep invocation/state validation separate from gate assessment:

- `ERROR` is returned before assessment when invocation, workspace, transition,
  stage-authority, or profile selection is invalid. `ERROR` emits no gate record.
- Gate verdict is exactly `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`.
- Coverage is exactly `COMPLETE` or `PARTIAL` and is reported independently from
  the verdict.
- An accepted-risk decision is not a gate verdict and never changes one.

Every profile check has these fields:

```yaml
check_id: <stable ID from transition-profiles.md>
class: BLOCKING | ADVISORY
coverage_required: true | false
source: DETERMINISTIC | PRODUCER_RECORD | ATTESTATION | DIRECTOR
status: PASS | FAIL | ADVISORY | UNKNOWN | NOT_EVALUATED | NOT_APPLICABLE | UNBOUND | STALE
expected: <profile rule>
observed: <redacted exact observation>
artifact_sha256: [<current hashes>]
evidence_record_ids: [<validated IDs>]
attestation_ids: [<validated IDs>]
finding_ids: [<stable IDs>]
reason_code: <stable machine reason>
```

Do not collapse `expected`, `observed`, evidence identity, or producer-native
verdict into free-form prose. A check may have multiple findings, but it has one
normalized status.

### Status assignment

Apply these rules in order:

1. Profile says the check does not apply, and the stated applicability condition
   was evaluated: `NOT_APPLICABLE`.
2. A required prior-result record is missing or lacks a required identity,
   manifest, producer, verdict, timestamp, persistence, or hash field: `UNBOUND`.
3. A supplied record or attestation is expired, superseded, scope-mismatched,
   build-mismatched, or differs from current exact bytes: `STALE`.
4. The check was not run because required scope, input, tool result, director
   response, or manual answer is unavailable: `NOT_EVALUATED`.
5. The check ran but cannot determine whether its predicate is true: `UNKNOWN`.
6. A blocking predicate is conclusively false: `FAIL`.
7. An advisory predicate is conclusively false, or a current producer/director
   reports a nonblocking risk: `ADVISORY`.
8. The exact predicate is conclusively true: `PASS`.

`UNBOUND` and `STALE` on a `BLOCKING` check are confirmed blocking failures, not
mere coverage gaps. `UNKNOWN` and `NOT_EVALUATED` are incomplete certification.
Do not translate silence, an unchecked box, a filename, or overall impression to
`PASS`.

## 2. Deterministic gate decision table

Normalize all checks, freeze their results, then apply the first matching row:

| Precedence | Condition | Verdict | Coverage |
|---|---|---|---|
| 1 | Any `BLOCKING` check is `FAIL`, `UNBOUND`, or `STALE` | `FAIL` | `PARTIAL` if any required coverage is incomplete, otherwise `COMPLETE` |
| 2 | No confirmed blocking failure, but any check with `coverage_required: true` is `UNKNOWN` or `NOT_EVALUATED`, or the bounded manifest/panel is incomplete | `PARTIAL` | `PARTIAL` |
| 3 | Complete coverage, no blocking failure, and one or more `ADVISORY` checks are `ADVISORY` | `CONCERNS` | `COMPLETE` |
| 4 | Complete coverage, every applicable blocking check is `PASS`, and no advisory risk remains | `PASS` | `COMPLETE` |

Additional invariants:

- `NOT_APPLICABLE` is complete only when the profile's applicability predicate
  itself was evaluated and its evidence is recorded.
- An advisory failure never creates `FAIL` by itself.
- A confirmed blocking failure remains `FAIL` even when other required work is
  incomplete; also report `coverage: PARTIAL` and every coverage gap.
- More than one failure does not change precedence. Preserve every finding.
- Do not average checks, count a majority, or let one role override a check owned
  by another source.
- Re-run the table after Chain-of-Verification. Revisions may change normalized
  statuses only when the new evidence is cited.

## 3. Accepted risk and waivers

`PROCEED_WITH_ACCEPTED_RISK` is an owner request recorded after the immutable gate
record. It does not change check statuses, verdict, coverage, eligibility, or
producer verdicts.

A policy waiver is different from accepted risk. A waiver may satisfy a check
only when that exact transition profile names an authorized waiver schema and the
supplied current record includes authority, scope, finding IDs, artifact/build
hashes, signed timestamp, and expiry. No current P1 transition profile authorizes
a generic waiver. Therefore a conversational permission, director opinion, or
unchecked `waived` label never passes a blocking check.

## 4. Versioned stage authority input

Gate evaluation requires a current catalog-backed authority record. Validate the
shared catalog's stage schema and transition graph, then the record and its prior
chain. The authority packet used by this skill contains at least:

```yaml
schema_version: <catalog-declared version>
record_path: <repository-relative path>
record_sha256: <raw hash>
stage: <one of the seven exact stages>
owner: <catalog-authorized owner>
transition_from: <prior stage or null under schema>
updated_at: <ISO-8601 with timezone>
source_snapshot_hash: <hash>
previous_authority_record_sha256: <hash or schema-authorized null>
gate_receipt:
  required: true | false
  record_id: <ID or null>
  path: <path or null>
  sha256: <hash or null>
```

If the shared catalog lacks the schema/graph/owner/receipt rules, or the authority
record is missing, malformed, stale, unauthorized, or contradictory, return
`ERROR — STAGE AUTHORITY UNVERIFIED` before profile work. Do not invent a schema
inside this skill.

`production/stage.txt` may be read only as a `LEGACY_DECLARATION`. Record its path,
raw hash, and value as an advisory observation. It cannot select a transition,
increase confidence, satisfy the authority check, or override the versioned
record. A conflicting legacy value is reported as a contradiction but does not
replace the authority stage.

## 5. Bounded scope manifest

Build only the profile-defined manifest. A manifest row records canonical
repository-relative path, role, discovery rule, current raw SHA-256, size, and
read mode (`FULL_CONTENT`, `STRUCTURED_EXTRACT`, `HASH_ONLY`, or
`EXTERNAL_RECEIPT`). Reject traversal, outside-root paths, root-escaping symlinks,
generated/vendor/cache paths, and ambiguous repository roots.

Never select a report because it is newest, has a convenient filename, or is the
only glob match after silently ignoring others. A profile must identify a record
directly, derive it from an authoritative manifest, or report ambiguity as
incomplete coverage.

Each transition profile declares these hard budgets:

- maximum manifest entries;
- maximum files whose full contents enter model context;
- maximum extracted/full-content bytes entering model context;
- maximum exact bytes hashed locally;
- maximum tool actions; and
- maximum elapsed assessment time.

Track actual use in the gate record. Stop admitting new inputs before exceeding a
budget. `BUDGET_EXCEEDED`, unreadable required input, ambiguous candidate,
concurrent change, or unresolved scope conflict makes profile coverage partial
and yields `PARTIAL` unless a confirmed blocking failure already requires `FAIL`.
Do not sample and infer that unchecked scope passed.

Hashing and structured search may inspect bytes without placing those bytes in
conversation context, but they still count against the profile's hash/action/time
budgets. Exclude `.git/`, generated builds not explicitly named by a candidate,
vendor/third-party/import/cache directories, `skill-fix-work/`, and the testing
framework unless a profile explicitly names one of those paths as evidence.

Immediately before the verdict, re-hash the authority record, complete scope
manifest, and every accepted evidence record. A changed authority record makes
the run `ERROR — AUTHORITY CHANGED DURING CHECK` with no gate record. Another
changed required input is `SNAPSHOT_CHANGED`, incomplete coverage, and cannot
produce PASS. An evidence hash mismatch is `STALE` under the status rules above.

## 6. Producer-record adapters

A blocking prior result may be accepted in either form only when the selected
profile explicitly allowlists that exact form and version:

1. a complete `cgs.review-evidence/v1` envelope whose exact profile-listed
   extension or payload schema is independently available and revalidated; or
2. a profile-authorized native immutable producer record.

For either form, the profile defines exact schema/version, required persistence,
artifact/build manifest, native verdict mapping, and currentness rule. Preserve
both `producer_native_verdict` and normalized check status. A generic envelope
cannot upgrade an ineligible native verdict or omit native dependencies.

Do not wrap a native record synthetically and do not infer a legacy adapter from
a similar filename or verdict. For a generic producer, validate the envelope,
the exact current extension/payload schema and version, the canonical payload or
artifact hash, and any producer-authorized recorder receipt. For a native
producer, validate the exact native schema/version and every required companion
receipt. Unknown or missing envelope, extension, payload, native-record, budget,
or recorder-receipt versions fail closed as `INCOMPLETE`; missing identity is
`UNBOUND`, and a changed current binding is `STALE`.

Reject conversation-only records when the producer contract says they are not
persisted gate evidence. Reject a wrapper whose payload cannot be reproduced.
An envelope marked `persistence: NONE`, `gate_evidence_eligible: false`, or
otherwise candidate-only remains `INCOMPLETE` even when its candidate verdict is
favorable. A recorder can make it eligible only when the current producer or
profile defines the recorder's exact schema/version and the complete receipt
validates; the gate must not invent that contract.
Do not accept document-internal approval, legacy summary logs, `latest` pointers,
or an aggregate hash when the producer requires per-input hashes.

Native verdict normalization uses four outcomes:

- `PASSING`: profile threshold met -> blocking check `PASS`.
- `ADVISORY`: producer guarantees complete coverage and no blocker, while named
  nonblocking risks remain -> check `ADVISORY` only where the profile permits it.
- `FAILING`: producer confirms a blocker or an ineligible final state -> blocking
  check `FAIL`.
- `INCOMPLETE`: null/error/partial/timeout/missing coverage -> `NOT_EVALUATED`,
  unless missing binding or stale currentness requires `UNBOUND`/`STALE`.

## 7. Manual attestation contract

Ask a manual question only when its profile row says
`evidence_source: ATTESTATION_ALLOWED`. Objective review, test, performance,
build, legal, certification, localization, accessibility, or receipt predicates
cannot be replaced by attestation unless that exact profile explicitly says so.

Ask all eligible unresolved questions together. Require structured answers and
the accountable operator identity. Normalize each answer to `YES`, `NO`, or
`UNKNOWN`; do not interpret prose beyond an explicit answer.

```yaml
schema: cgs.gate-attestation/v1
attestation_id: sha256:<canonical payload excluding attestation_id>
check_id: <stable profile check ID>
question_version: <profile ID + question version>
question: <exact question>
answer: YES | NO | UNKNOWN
operator: <user-supplied accountable identity>
identity_assurance: USER_ASSERTED | VERIFIED
issued_at: <ISO-8601 with timezone>
observed_at: <ISO-8601 with timezone>
expires_at: <profile deadline or null when hash-bound only>
transition_id: <exact transition ID>
profile_id: <exact profile ID>
scope_manifest_sha256: <current manifest hash>
subjects:
  - path_or_id: <artifact/build/report identity>
    sha256: <current hash>
supporting_receipt_ids: [<IDs>]
```

Validation rules:

- Missing operator, time, question version, subject hash, or scope hash is
  `UNBOUND`.
- Expiry, profile/check mismatch, or subject/scope hash change is `STALE`.
- `YES` maps to `PASS`, `NO` maps to `FAIL` for a blocking question or
  `ADVISORY` for an advisory question, and `UNKNOWN` maps to `UNKNOWN`.
- An unanswered or ambiguously answered required question remains
  `NOT_EVALUATED`; it never becomes PASS.
- The skill may emit the attestation in conversation but remains read-only and
  must not persist or sign it for the user.

## 8. Director advisory panel

Director results are advisory observations. They never satisfy a blocking check,
upgrade evidence, waive a blocker, or directly force `FAIL`.

Use these four common stable check IDs after the selected profile checks:

- `DIR-C01` — CD-PHASE-GATE;
- `DIR-T01` — TD-PHASE-GATE;
- `DIR-P01` — PR-PHASE-GATE; and
- `DIR-A01` — AD-PHASE-GATE.

They are `class: ADVISORY`, `source: DIRECTOR`. Their
`coverage_required` is true in lean/full and false in solo.

For `lean` and `full`, dispatch the four profile-independent phase gates in
parallel with the exact transition ID, candidate stage, scope manifest hash,
bounded artifact summary, and domain-specific context. Each dispatch has one
attempt and a 120-second response deadline. Do not silently retry, substitute the
current agent, or accept a response for an older manifest.

Each result records:

```yaml
gate_id: CD-PHASE-GATE | TD-PHASE-GATE | PR-PHASE-GATE | AD-PHASE-GATE
agent_role: <expected role>
attempt: 1
scope_manifest_sha256: <hash>
started_at: <time>
ended_at: <time or null>
native_verdict: READY | CONCERNS | NOT_READY | null
status: COMPLETE | TIMEOUT | BLOCKED | ERROR | MALFORMED | STALE | NOT_APPLICABLE_BY_MODE
finding_ids: [<stable panel finding IDs>]
```

Normalize a complete `READY` to director check `PASS`. Normalize complete
`CONCERNS` and `NOT READY` to `ADVISORY`, preserving the native wording and
findings. Any enabled result that is TIMEOUT, BLOCKED, ERROR, MALFORMED, missing,
or STALE is `NOT_EVALUATED`; director-panel coverage is required in lean/full, so
the run cannot PASS and is PARTIAL absent a confirmed blocking failure.

For `solo`, spawn no directors. Emit all four as `NOT_APPLICABLE_BY_MODE`; panel
coverage is complete by policy. Solo changes no deterministic check, scope,
evidence threshold, or verdict-table rule.

The shared director-gate document may define prompts and role domains, but its
generic strictest-verdict or persistence guidance does not authorize this
read-only skill to let directors own the gate verdict or write outcomes to files.

## 9. Mutation guard

Capture a repository snapshot sufficient to detect file creation, deletion,
rename, or content change caused during the run. `$gate-check` itself must produce
no filesystem mutation in PASS, CONCERNS, FAIL, PARTIAL, ERROR, or accepted-risk
paths. External concurrent changes are reported; never revert or repair them.

If this workflow caused or authorized any mutation, set the mutation guard to
FAILED and do not claim a valid gate result. Conversational gate records,
attestations, and advance requests are not filesystem mutations.
