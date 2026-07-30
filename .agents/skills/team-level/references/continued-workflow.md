# Continued Team Level Workflow

Execute these phases in order. Routine read-only transitions continue without a
user prompt. Stop only at the declared input, product-decision, blocker,
authorization, timeout/partial, stale, or final-acceptance boundaries.

## Phase 0 — Validate invocation before all reads

1. Parse exactly one level ID and reject every invalid/extra token.
2. On failure, return usage with zero project reads, delegation, writes, or
   verdict.
3. Load private contracts; contradiction is ERROR before project evidence.
4. Record permanent concurrency, mutation, result-size, and review-loop bounds.

Do not read review mode. No role/evidence requirement varies by mode.

## Phase 1 — Resolve operation and target baselines

1. Resolve exact level/checkpoint paths and canonical confinement.
2. Inspect existence/type and declared revision or ABSENT.
3. Derive CREATE when absent; ask create/revise intent only when observed state is
   ambiguous; validate a matching checkpoint before RESUME.
4. Freeze operation/run identity and initialize in-memory checkpoint state zero.

CREATE collision, missing REVISE baseline, unsafe target, or stale RESUME state
stops. Do not reinterpret operation or overwrite.

## Phase 2 — Build bounded context and adjacency manifests

1. Read root/nearest instructions and only allowed explicit sources.
2. Apply file/byte/excerpt/depth limits before delegation.
3. Record every included/omitted row and exact excerpt revision/reason.
4. Ask the user only when required sources cannot fit; bind the explicit
   included/omitted selection.
5. Build one-hop directional adjacency records, reverse joins, cycles, and states.
6. Freeze context/adjacency revisions and checkpoint state.

Never silently truncate, recurse a cycle, infer from filenames, or auto-run an
adjacent level workflow.

## Phase 3 — Dispatch first read-only proposal batch

1. Derive applicable narrative/world/art jobs from the manifest.
2. Create stable job records with exact input revisions/schemas/sizes/deadlines.
3. Dispatch at most three live jobs; wait only until the common bounded batch
   completes or individual deadlines expire.
4. Validate result schema/size/source refs/revision and destination uniqueness.
5. Preserve valid independent results and checkpoint every job state/payload.

One narrowed follow-up may occur before the original deadline. Required timeout/
invalid result prevents COMPLETE; return PARTIAL with safe resume when coherent
core evidence exists, otherwise BLOCKED.

## Phase 4 — Author layout and integrate domain interfaces

1. Dispatch one read-only level author with LEVEL_SOURCE proposals only.
2. Validate its allowlisted level draft and freeze layout revision.
3. Dispatch applicable systems and location-art jobs against that exact revision in a
   bounded batch.
4. Route formulas/tuning to SYSTEM_GDD and production art detail to ART_BRIEF;
   retain only testable level-facing interfaces/constraints.
5. Surface exact cross-domain conflicts as product decisions; do not let reducer
   choose.
6. Validate/persist the next in-memory checkpoint state.

No transcript or external-destination payload is pasted into the level draft.

## Phase 5 — Accessibility review with one convergence opportunity

1. Run a fresh read-only reviewer on exact draft/requirement revisions.
2. Normalize stable findings and observation count.
3. With OPEN BLOCKING findings, ask for one exact author diff scope or stop.
4. If revision is chosen, run one separate read-only author job and one
   verification re-review limited to original IDs and diff regressions.
5. Stop if any original blocker remains open on observation two.
6. Accept only non-blocking risk with complete user-owned record and immediately
   finish `ACCEPTED RISK / NOT APPROVED`.

No blocker acknowledgment can unlock writing, QA, approval, or implementation.
Never run a third observation or broaden verification into unrelated redesign.

## Phase 6 — Route, reduce, decide, and freeze source bytes

1. Place every proposal/finding in the canonical one-destination ledger.
2. Verify reducer allowlist and forbidden-body exclusion.
3. Ask only remaining genuine product choices with stable alternatives/effects.
4. Render exact canonical level bytes and assign the owner-approved explicit `level_draft_revision`.
5. Record context, adjacency, proposal, decision, resolved-finding, dependency,
   blocker, and draft revisions in the next checkpoint snapshot.

Routine reduction needs no approval. No project write occurs yet.

## Phase 7 — Preview and execute the first bounded transaction

1. Select one permanent transaction writer.
2. Build/preview the complete two-path plan and deterministic plan revision.
3. Request one authorization bound to exact paths/operations/owner/baselines/
   source base/draft/checkpoint transitions.
4. revalidate all sources/targets; stale values cancel before mutation.
5. Writer performs only authorized level/checkpoint compare-and-set writes.
6. Reread bytes, verify revisions, and record actual write set.

On failure, prove full byte rollback or preserve/print honest PARTIAL recovery
state. Do not claim approval from file existence.

## Phase 8 — Run independent level review

1. Freeze current raw level revision after write/postverification.
2. Dispatch a fresh reviewer whose identity differs from every author/writer.
3. Apply only the `cgs.level-review/v1` profile and validate source/evidence revision.
4. On BLOCKING findings, allow one exact author diff under a replacement plan and
   authorization, then one limited verification re-review.
5. Any level-byte change stales all old review/QA evidence.
6. Reviewer timeout, collision, malformed output, missing evidence, or second
   open blocker prevents COMPLETE.

Never invoke `$design-review`, system-GDD section checks, or reviewer writes.

## Phase 9 — Generate QA proposal against final current revision

1. Require current accessibility and level-review zero-blocker state.
2. Dispatch read-only qa-tester with exact final level/review/finding revisions.
3. Validate bounded planned-case schema/coverage/result revision.
4. Mark cases PLANNED only; write no QA file and claim no execution/PASS.
5. Freeze the reducer; any later level change stales review and QA and returns to
   Phase 8 before fresh QA.

Missing/invalid/timed-out QA returns PARTIAL and an exact resume phase.

## Phase 10 — Final product acceptance and checkpoint transition

1. Evaluate all twelve `TL-COMPLETE/v1` predicates with evidence revisions.
2. If any predicate is false/unknown, do not ask for design acceptance; return
   the blocking decision or safe resume action.
3. Build exact final packet plus COMPLETE-checkpoint candidate path, baseline,
   bytes/revision, writer, compare-and-set condition, and finalization plan revision; ask
   once for combined product acceptance and write authorization.
4. Decline/deferral leaves NOT APPROVED.
5. revalidate all sources/targets and have the same writer persist only the exact
   newly authorized COMPLETE checkpoint candidate by compare-and-set; do not
   reuse the earlier source-write authorization for unknown future bytes.
6. Reread checkpoint/level bytes and re-evaluate the matrix.

Only then emit `COMPLETE — DESIGN APPROVED`. It is not implementation authority.

## Phase 11 — Resume idempotently

1. Validate checkpoint schema/sequence/run/operation/plan/source/target revisions and
   stored bounded job payload/result revisions.
2. Mark every mismatched dependent record STALE.
3. Re-enter the earliest stale/incomplete phase.
4. Reuse only exact valid completed jobs, writes, decisions, review observations,
   and QA proposal; do not duplicate them.
5. A prose-only prior success or missing payload is not reusable evidence.

## Phase 12 — Return and stop

Return one `cgs.team-level-run/v2` with all paths/revisions, manifests, destination
counts, jobs/deadlines/results, decisions, findings/rounds, review/QA identities,
write/checkpoint state, COMPLETE predicate matrix, safe resume, and exactly one
workflow verdict.

State the validation boundary: PLANNED QA is not executed evidence, static/review
prose does not implement the level, and this workflow wrote no external
destination. Stop without invoking another workflow.
