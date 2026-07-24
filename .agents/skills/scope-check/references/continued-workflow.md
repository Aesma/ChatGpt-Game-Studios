# Scope-check continued workflow

Execute these phases in order. Never expand the read set beyond exact pair and
validated evidence-manifest allowlist.

## Phase 1: Parse without guessing

1. Parse exactly `compare`, `inspect`, or `discover`.
2. Require exact `path@sha256:<hex>` pair for compare/inspect and one exact
   evidence identity for inspect.
3. Canonicalize project-relative paths, reject escapes/links/aliases/duplicates,
   and verify exact bytes before parsing.
4. Reject unknown/repeated options, positional names, bare paths, fuzzy IDs, and
   unsupported types/schemas.

No arguments or a missing pair member returns `INPUT REQUIRED`. `discover` reads
only canonical active-state pointer fields, hashes the exact suggested candidates,
lists all possibilities, and returns `INPUT REQUIRED`. It never compares in that
invocation or chooses among multiple candidates.

## Phase 2: Freeze pair identity and approval

Record before hashes for baseline/current. Enforce the per-artifact byte limit,
parse exact schema IDs, and validate:

- baseline ID/version/source revision/parent/timebox/completeness;
- exact immutable approval record and product-owner authority;
- current manifest ID/version/source revision/parent/timebox/completeness;
- current baseline reference matches supplied path/hash/ID/version;
- compatible normalization schema/adapter; and
- declared counts, unique stable Scope IDs, and explicit removals.

Follow only exact mandatory approval/authority/normalization `path@sha256`
references embedded in the pair, capped at eight records and 524288 total bytes.
These are core identity evidence, not a license to discover optional decisions.

Any actual/invocation hash mismatch, changed baseline at same path, missing or
ambiguous approval/authority, parent mismatch, alternate baseline link, duplicate
ID, unsupported normalizer, or incomplete core artifact is `INSUFFICIENT
EVIDENCE`. Never search for a replacement.

## Phase 3: Normalize and hash entries

Load only semantic fields declared by the shared normalization adapter. Canonicalize
and hash each Scope ID payload and acceptance boundary. Preserve source locations
and exact artifact hash.

Ignore presentation order/heading/row formatting. A split/merge is presentation
only when the same stable IDs normalize to the same semantic hashes. Never use
title similarity or model summaries to align entries.

Apply 4096-ID and semantic-byte bounds. Preserve over-limit IDs/counts as
`UNCHECKED_LIMIT`; when a meaningful subset was compared return `PARTIAL`, never a
complete no-delta result.

## Phase 4: Compute stable sorted deltas

Build union of stable IDs and classify every ID through the exact delta table.
Silent deletion is conflict. Compute stable fingerprint/Delta ID without artifact
hashes or presentation fields. Store both artifact/entry hashes and semantic
field-level differences separately.

Sort by stable Scope ID then delta type. Raw row/item/file/commit/TODO counts are
never effort, bloat, health, or verdict inputs.

## Phase 5: Classify authority and allowed state

For compare without evidence manifest, an embedded complete decision may be
validated; an external linked decision is `UNVERIFIED_RECORD` and is not opened.
For inspect, validate external decision/authority records only from the evidence
allowlist. Never search for them.

For each changed delta:

1. validate decision schema/state/operation;
2. match Scope and Delta IDs;
3. match exact baseline/current/entry hashes, parent, and timebox;
4. validate decision owner through exact authority record;
5. validate timestamp/signature/record digest/supersession;
6. detect contradictory finals; and
7. assign authority and allowed-state classes mechanically.

Do not treat Git author, implementer, file owner, issue assignee, agent, prose, or
conversation acknowledgment as authority or justification.

## Phase 6: Validate the bounded evidence manifest

For inspect, validate evidence manifest identity/schema/completeness and exact
pair bindings. Effective budgets are the smaller of its declarations and fixed
limits. Read only its exact path@hash rows and exact Git IDs/range. Do not follow
globs/directories or discover adjacent evidence.

Classify each row's purpose and attach it only to matching stable Scope/Delta IDs
and pair hashes. Git/code/TODO/build evidence may show implementation activity but
cannot create scope or approval.

Keep every unavailable/hash-mismatched/unsupported/over-budget row as unchecked.
Preserve core deltas and return `PARTIAL`; dependent authority/impact/risk states
become invalid or unverified.

## Phase 7: Calculate evidence-bound effort and impact

Validate estimates for all changed IDs against exact pair/entry hashes, calibrated
method/unit, and uncertainty policy. If complete, calculate absolute delta
intervals exactly; otherwise output unverified without conversion or percentage.

Calculate dimensions mechanically:

- Schedule: compare complete effort and capacity/timebox intervals.
- Quality: build the changed acceptance-boundary denominator and verify every
  current regression/test-plan mapping.
- Integration: compare exact dependency/interface graphs and owner/contract/
  consumer/integration evidence for changed edges.

Use only the five dimension states. Report all receipts and denominators. Do not
combine dimensions into a score/rating or let impact change delta/authority/result.

## Phase 8: Validate accepted-risk references

Read only exact allowlisted risk records. Validate state, Delta/Scope IDs,
dimension/exposure, pair/evidence hashes, owner authority, rationale, controls,
signature, timestamp, and expiry/review trigger.

List valid or invalid references beside the relevant impact state. Do not change
impact, delta, authority, allowed classification, or result. Never create, renew,
or apply an acceptance.

## Phase 9: Enforce immutable re-checks

Re-read every consumed artifact in batches no larger than 64 paths and recompute
hashes.

- Baseline/current change -> discard delta conclusions and return
  `INSUFFICIENT EVIDENCE — INPUT CHANGED DURING CHECK`.
- Approval/normalizer change -> invalidate core identity and return
  `INSUFFICIENT EVIDENCE`.
- Optional evidence/decision/risk/estimate/dependency/test change -> preserve
  core deltas, invalidate dependent fields, and return `PARTIAL`.
- Unreadable re-hash -> same severity as the affected role.

Do not modify, restore, copy, or re-baseline any input.

## Phase 10: Derive result and neutral options

Apply canonical result precedence exactly. An authorized changed ID remains
`SCOPE DELTA FOUND`; an unapproved change is classified but the comparator does
not decide its fate. Missing compare-only optional evidence does not hide the
delta. Declared inspect evidence gaps produce `PARTIAL`.

When complete deltas exist, produce two or three neutral unranked options, for
example:

1. keep the immutable approved baseline and separately remove/revert named
   unapproved current deltas;
2. retain named deltas and request compatible impact evidence plus an authorized
   product decision; or
3. place named IDs into a separately approved future baseline/timebox.

List exact Scope/Delta IDs, known impact, unknowns, decision owner/action, and
separate required transaction. Do not recommend/rank/select an option, label
Cut/Keep/Defer, invoke another workflow, or mutate scope.

## Phase 11: Render read-only evidence

Freeze the generic envelope and `cgs.scope-check/v2` extension. Canonicalize and
calculate `record_id` with the field omitted. Include:

- exact pair, approval, normalizer, and evidence identities;
- stable sorted deltas and both-side hashes;
- authority, allowed, risk, effort, and impact states;
- core/evidence coverage and every unchecked identity;
- input before/after hashes, comparison/stale keys, result, and neutral options;
- `NOT_PERSISTED`, gate-ineligible, and `READ_ONLY` boundary.

End with exact baseline/current path@hash identities and state that no file, Git
state, product decision, planning artifact, or baseline changed. Stop without
delegation or follow-up execution.
