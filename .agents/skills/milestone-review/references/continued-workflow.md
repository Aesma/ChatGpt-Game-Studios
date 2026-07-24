# Continued Milestone Review Workflow

Execute these phases in order. This is an operational checklist, not permission
to widen the read or write scope. Preserve all verified partial evidence and
stop at the earliest phase whose stop condition applies.

## Phase 0 — Parse and freeze the request

1. Parse exactly one selector and one optional review mode.
2. Resolve the mode from explicit input, exact configuration, or the documented
   `lean` default.
3. Record normalized invocation, UTC start time, contract versions, fixed limits,
   and `allowed_project_write_set: []`.
4. Capture a bounded pre-run project snapshot for authority sources, expected
   inputs once known, and the future report path once derived.

Invalid syntax/configuration stops with `run_status: ERROR`. Read no milestone
evidence, dispatch no reviewer, and write nothing.

## Phase 1 — Resolve exactly one milestone

1. For an explicit ID, construct only its canonical milestone path.
2. For `current`, read both configured authority files when present and parse
   only the named stable-ID fields.
3. Require agreement, uniqueness, canonical path confinement, exactly one target
   regular file, and matching internal ID.
4. Record authority paths, revisions/hashes, declarations, and resolution rule.

Missing, ambiguous, conflicting, malformed, or unsafe resolution stops with
`run_status: BLOCKED` and `artifact_write_status: BLOCKED`. Do not enumerate a
recency-ranked alternative.

## Phase 2 — Validate the milestone before templating

1. Apply the milestone byte bound before parse.
2. Distinguish absent, zero-byte, malformed/schema-conflicting, and internally
   inconsistent inputs.
3. Validate target/build/date, exact sprint IDs, scope and criteria IDs, quality
   thresholds, progress basis, goal IDs, and manifest reference.
4. Record the exact subtype and safe source observation on failure.

Any Phase 2 failure emits only a resolution diagnostic. Do not construct a
metric shell with zeros/unknowns, evidence draft, producer packet, objective
verdict, governance prompt, report candidate, or write authorization request.

## Phase 3 — Lock the bounded evidence manifest

1. Read only the milestone-referenced manifest and apply its byte bound.
2. Validate its schema, milestone raw hash/revision, target, capture/freshness
   declarations, repository revision, unique source rows, and required joins.
3. Derive the exact expected source set from milestone scope, sprint IDs, and
   thresholds; never discover inputs by directory recency or all-report scans.
4. Apply row/file/aggregate bounds, canonical path confinement, raw hash,
   internal revision, build/hardware/scenario/unit/basis, uniqueness, and
   freshness checks.
5. Create one ordered ledger row for every expected or unexpected manifest row,
   record exact coverage, and compute `source_snapshot_sha256`.

Missing or invalid evidence does not abort useful analysis unless safe bounded
parsing is impossible. Mark it explicitly, propagate dependent unknowns, set
`evidence_status: PARTIAL`, and continue with independent verified sources.

## Phase 4 — Derive metrics, checks, findings, and candidates

1. Compute metric objects only from compatible `VERIFIED` rows using the named
   formula versions, operands, denominators, units/bases, and confidence states.
2. Evaluate every required scope/criterion and quality threshold as
   `PASS|FAIL|UNKNOWN`; then derive delivery and quality statuses.
3. Normalize every failure/gap/risk/warning into a stable finding.
4. Construct only evidence-backed scope candidates, all with
   `CANDIDATE_NOT_DECIDED`; validate and quote any separately supplied scope
   decision without mutating scope.
5. Preserve simultaneous facts: a conclusive failure and unrelated evidence gap
   are both reported.

Do not infer feature percentages, compatible velocity, schedules, quality
results, player impact, owners, or deadlines.

## Phase 5 — Freeze the evidence-only draft

1. Assemble `cgs.milestone-evidence-draft/v1` with only the allowed evidence
   fields.
2. Assert forbidden producer, risk, verdict, governance, path, authorization, and
   write fields are absent.
3. Canonically serialize once, freeze the exact bytes, and compute
   `evidence_draft_sha256`.
4. Show milestone/target, source snapshot, draft hash/size, evidence coverage,
   and limitations before any producer review.

Do not mutate and rehash the draft to accommodate reviewer feedback. A changed
source requires a new analysis run, not a patched same-run draft.

## Phase 6 — Perform or skip producer review

1. In `full`, send the exact frozen draft bytes/hash and source snapshot through
   `PR-MILESTONE`; give the reviewer no write or scope-decision authority.
2. In `lean` or `solo`, create the exact mode skip receipt and do not dispatch.
3. Validate one producer response against schema, size, milestone/target, both
   hashes, reviewer/timestamps, stable risks, evidence refs, and result hash.
4. Treat timeout, unavailability, malformed/multiple/mismatched response, or
   invented metrics as an explicit reviewer gap with `risk_status: UNKNOWN`.

Never silently retry a reviewer with changed input or treat non-response as
`ON_TRACK`/`NOT_REVIEWED`.

## Phase 7 — Compute layered statuses and objective verdict

1. Reuse the already derived delivery and quality states.
2. Set risk status from the validated receipt/skip only.
3. Apply the first matching objective verdict rule and record its rule ID/input
   tuple.
4. Keep `decision_status: NOT_RECORDED` and
   `artifact_write_status: NOT_REQUESTED` at this point.

Evidence partiality or required full-review failure forces `PARTIAL`. A user has
not yet made a decision, and no report transaction has occurred.

## Phase 8 — Record an optional user governance decision

1. Present objective status, source gaps, stable risks/findings, scope candidates,
   tradeoffs, and allowed decision values.
2. Validate a supplied governance record and all required user-owned identity,
   time, rationale, accepted IDs, owners, and deadlines.
3. Bind the record to exact source/draft/producer/objective hashes.
4. Reject incompatible `PROCEED`; otherwise record the user value without
   changing any objective field.

No reply or incomplete fields means `decision_status: NOT_RECORDED`; never infer
acceptance from a request to review or write the report.

## Phase 9 — Build the final immutable report candidate

1. Freeze one UTC second and derive the deterministic run ID/path.
2. Construct the full report in the required section order and canonical format.
3. Verify all embedded revisions/hashes, derivation inputs, stable IDs, and
   layered states against the frozen objects.
4. Compute exact `report_candidate_sha256` and byte count.
5. Require the canonical target path is absent; a collision blocks the write.

The report candidate may exist in memory/scratch, but `report_persisted` remains
false and the project write set remains empty.

## Phase 10 — Preview and authorize

Preview:

```text
operation: CREATE_NEW
report_path: <canonical path>
report_candidate_sha256: <sha256>
report_candidate_bytes: <integer>
source_base_set: <ordered revisions and hashes>
allowed_project_write_set: [<same report path>]
```

Use prior task authorization only if it explicitly covers that exact immutable
candidate transaction. Otherwise request one authorization. Refusal or absent
authorization leaves the project unchanged and sets
`artifact_write_status: BLOCKED`.

## Phase 11 — Compare-and-set and atomic create

1. Re-resolve every authority/source path and recheck exact bytes, hashes,
   revisions, joins, and target absence.
2. If any value changed, invalidate candidate/path/authorization and return a
   stale result; do not write.
3. Prepare exact bytes in the target directory and use atomic create-new/no-
   replace semantics for the one authorized path.
4. Reread and verify exact target bytes/hash and revalidate all sources.
5. Report `artifact_write_status: COMPLETE` only after successful postchecks.

Never overwrite, append, invent a collision suffix, widen the write set, or
repair another file. On ambiguous failure, report what can be verified and do
not claim the report exists correctly.

## Phase 12 — Return one run envelope and stop

Return `cgs.milestone-review-run/v2` containing normalized request, contract and
limit versions, milestone/authority identities, source/draft/producer/decision/
report hashes, coverage, metrics, checks, findings, scope candidates/decisions,
layered status fields with derivation, mutation snapshots, exact report receipt
or null, and stale key.

Explicitly state the validation boundary: source inspection and deterministic
derivation do not execute tests, performance captures, fixes, milestone
transitions, recommendations, or downstream workflows. Stop.
