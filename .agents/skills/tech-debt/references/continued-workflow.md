# Tech-Debt Continued Workflow

Execute these phases in order. All phases are read-only. Stop immediately on the
specified terminal condition; do not invoke another skill or the independent
recorder.

## Phase 0 — Parse invocation

1. Parse the exact grammar in `SKILL.md`.
2. Reject unknown/missing/repeated options, positional values, invalid hashes,
   invalid UUIDs, unsafe paths, and illegal combinations as `USAGE_ERROR`.
3. Resolve the canonical project root without scanning outside it.
4. Load the two normative contract files completely.

If grammar or contract loading fails, return the error envelope and stop.

## Phase 1 — Freeze input identity

1. Resolve every input to one canonical project-relative path.
2. Read exact bytes once, compute SHA-256, and compare the declared hash.
3. Validate schema, project relationship, timestamps/expiry when applicable, and
   internal hashes.
4. For `ABSENT:<path>`, prove exact absence before proceeding.
5. Record target commit/ref and dirty state when available; never clean or alter
   the working tree.

A scope/manual/baseline identity failure is `INPUT_ERROR`. A present register
identity/schema/chain failure is `REGISTER_ERROR`. Stop on either.

## Phase 2 — Capture before snapshot

Build a streaming read-only snapshot over the bounded input paths: path, type,
size, mtime where available, and SHA-256 for each readable regular file. Include
the register path even when absent. Record denied/unreadable entries. The allowed
write set is empty.

## Phase 3 — Validate and replay the register

1. Validate v3 header/codec and full content hash.
2. Verify global sequence/hash chain, per-debt chains, UUID uniqueness, payload
   hashes, fingerprint/alias ownership, and lifecycle transitions.
3. Materialize items and indices by replay; retain a view hash.
4. For absence, use the mode-specific empty/partial behavior.
5. For recognized legacy schema, return `REGISTER_ERROR` subtype
   `MIGRATION_REQUIRED` and a read-only migration proposal; stop.

Never repair or partially trust an invalid register.

## Phase 4A — Scan

1. Validate `cgs.tech-debt-scan-scope/v1` and apply hard caps.
2. Classify every included/excluded/unverified path with evidence.
3. Resolve exact rule and analyzer registry entries. A missing compatible analyzer
   creates an `UNSUPPORTED` receipt row; do not substitute another technique.
4. Invoke only declared read-only commands with exact target subsets and limits.
5. Normalize every result to `cgs.tech-debt-analyzer-receipt/v1`.
6. Convert results to candidate states. Marker/size/keyword hits remain
   `HEURISTIC_CANDIDATE`; complexity/clone require successful capable analyzers.
7. Compute `td-fp-v2` only when all identity fields are canonical.
8. Deduplicate against the replayed primary/alias index and within the run.
9. If the user explicitly selects owner-triaged rows, construct but do not persist
   one exact change proposal.
10. Select the scan outcome by the precedence in `SKILL.md`.

## Phase 4B — Add

1. If no manual record exists, return `INPUT_REQUIRED` with the exact
   `cgs.tech-debt-manual-candidate/v1` schema and stop.
2. Validate required fields, path/source identities, evidence hashes, scale values,
   and prohibited lifecycle/priority/schedule assertions.
3. Compute `manual@2` / `td-fp-v2` when possible.
4. Deduplicate against all primary fingerprints and aliases.
5. Return `ADD_DUPLICATE_FOUND` for a match or `ADD_PREVIEW_READY` for a new,
   owner-selected candidate. A proposal may contain `CREATE_REGISTER`, `CREATED`,
   `OBSERVED`, or a separately selected triage event as allowed by the contract.
6. Do not reserve a human acceptance/resolution/priority decision that was not
   separately supplied with its required authority evidence.

## Phase 4C — Prioritize

1. Select current `OPEN` and `ACCEPTED` rows only.
2. Resolve the latest valid estimate event and evidence for each input.
3. Mark incomplete/invalid values `UNSCORED`; do not infer or convert them.
4. Calculate exact rational scores and deterministic tie-break traces.
5. Produce a transient, hash-bound `ADVISORY_ONLY` view; do not modify or sort the
   register bytes.
6. Return `PRIORITY_VIEW_READY` only when all requested rows are scored; otherwise
   `PRIORITY_VIEW_PARTIAL` with exact gaps.

## Phase 4D — Report

1. Produce point-in-time lifecycle/category/verification counts and data gaps.
2. Validate the optional baseline as an exact ancestor.
3. Traverse exact event intervals for change metrics.
4. Compute timestamp/sprint aging only from declared stable evidence.
5. Mark absent/incomparable evidence `UNKNOWN`; never infer zero or a trend.
6. Return `REPORT_READY` only for complete requested fields; otherwise
   `REPORT_PARTIAL`.

## Phase 5 — Capture after snapshot

Repeat the Phase 2 snapshot and compare it to the before snapshot.

- Register change or a changed analyzed input invalidates the relevant result.
- Preserve evidence of concurrent change without reverting, deleting, or blaming.
- A register identity change is `REGISTER_ERROR` subtype `STALE_REGISTER`.
- Other required input changes force the applicable partial outcome; if no stable
  meaningful evidence remains, return `INPUT_ERROR`.

The skill itself must never appear as a writer.

## Phase 6 — Validate proposal and result

1. Recompute candidate, view, report, proposal, and envelope hashes.
2. Ensure all IDs are unique within the proposal and absent from the base index.
3. Verify every event transition, authority requirement, predecessor, payload
   hash, order, proposed head/revision/hash, and append-only proof.
4. Mark the proposal `NOT_PERSISTED` and `NOT_AUTHORIZATION`.
5. State gaps, unsupported checks, stale key, and mutation evidence.
6. Confirm outcome vocabulary is exact and does not imply mutation or quality.

If proposal validation fails, omit it and return the applicable error/partial
outcome. Never repair it by silently changing authorized content.

## Phase 7 — Return and stop

Return one `cgs.tech-debt-analysis/v2` envelope. Include enough deterministic data
for an independent verifier to recompute all hashes and classifications. End with:

```text
register_mutated: false
proposal_persisted: false
decision_authority_exercised: false
recorder_invoked: false
```

If the user wants persistence, explain that a separate recorder transaction needs
fresh exact authorization over the proposal hash. Do not perform that transaction
inside this skill.
