# UX review continued workflow

This procedure operationalizes the normative rules without expanding authority or
write scope.

## 1. Preflight and mutation baseline

1. Parse the strict invocation before discovering files.
2. Establish project root from the repository/workspace context. Do not traverse
   outside it and do not follow symbolic links or junctions out of root.
3. Create a streaming, sorted mutation snapshot for all regular project files
   except version-control internals, declared cache/build/output directories, and
   other exclusions already defined by an owner-approved project manifest. revision
   path, size, and file revision. Process at most 256 paths in memory per chunk and
   fold chunk revisions into one root revision. The empty allowed-write set is explicit.
4. If the baseline cannot cover an in-scope path, record the exact gap. The run
   can continue for diagnostic findings but must be `PARTIAL`.
5. Read and revision the current `ux-design` main and continuation sources and the
   UX-review rules. Validate the explicit author-schema and bundle versions. Parse exactly one
   author-declared profile version, content profile, schema construction, routing
   matrix, and stable section sets; build/revision
   `cgs.ux-author-contract-manifest/v1` and record
   `author_contract_manifest_version`.
6. Apply the rules-file support gate before candidate scoring. Continue only when
   the declared tuple is supported and the assertion matrix covers every author
   profile/section. Otherwise return `MIGRATION REQUIRED` with null verdict and
   expected/observed author identities.

The snapshot is a read-only mutation guard, not an invitation to scan file
contents for design authority.

## 2. Build an explicit candidate manifest

For an exact target, normalize the project-relative path, prove it remains inside
the project root, and add that one file to the manifest.

For `all`, `hud`, or `patterns`, enumerate regular Markdown files directly under
`design/ux/` and its declared author-owned artifact subdirectories. Do not follow
links, search the whole repository, or infer authority from arbitrary files.
For each candidate, read only enough header bytes to determine:

- normalized path and revision;
- `Artifact Type`, if parseable;
- `Schema Version`, `Profile Version`, `Content Profile`, `Artifact ID`, and
  `Authoring Receipt ID`, if parseable;
- eligibility or exclusion reason.

Sort by normalized path. Exclude `cgs.review-evidence/*`, UX-review output,
archives, templates, manifests, reports, and files with an unsupported or unknown
artifact type. List exclusions; do not silently treat them as passed.

Apply selector filtering after metadata routing:

- `all`: all three supported artifact types;
- `hud`: only `hud-design`;
- `patterns`: only `interaction-pattern-library`.

The traditional filenames `design/ux/hud.md` and
`design/ux/interaction-patterns.md` may locate candidates but cannot override
their metadata. revision the sorted complete manifest rows. Review at most eight
eligible targets. Every remaining eligible row is `UNCHECKED / LIMIT_REACHED` and
forces batch `PARTIAL`.

## 3. Validate identity and route

For each selected target:

1. validate its declared revision and parse the required author header.
2. Validate type, author schema version, supported author-declared profile
   version/content profile, stable Artifact ID, and applicable Screen ID. Require
   READY_FOR_REVIEW to resolve its stable external authoring receipt ID to a
   current path/revision from the supplied handoff or bounded context evidence.
3. Choose the review profile from the artifact type matrix.
4. Treat a conflicting template marker or filename as evidence of invalid
   identity, not as a new route. If both metadata and marker are absent for one
   exact target, a conventional filename may only propose a type; pause for
   explicit confirmation, emit no verdict before it, and record
   `user-confirmed-filename-fallback` afterward. Never do this per file in a
   batch. Confirmation does not repair missing schema/profile/stable identity.
5. If identity cannot be established, return a target error with null verdict.
   Continue other batch targets independently.

Do not score a legacy artifact against the current checklist. This includes a
target declaring unsupported legacy `ux-profile-schema-v1`, an author/target content-profile
mismatch, or a Schema Version that does not equal the computed current author
revision. Return `MIGRATION REQUIRED` with the actual/expected author contract and
manifest identities.

## 4. Resolve bounded context

Resolve the target's exact `Context Manifest revision`. The manifest defines the
only authority records eligible for dependency and requirement resolution. Read
records by exact path and verify every declared revision before use.

Use this order:

1. context manifest;
2. platform profile;
3. accessibility foundation and committed tier;
4. applicable owner-approved requirement sources;
5. referenced pattern/data contracts;
6. exact performance/technical sources, only when the target makes a source-bound
   runtime claim.

Load no more than 16 context artifacts or 262144 exact context bytes per target.
Do not use repository-wide filename/header searches to fill a gap. Store every
resolution in the dependency ledger. Any missing, stale, contradictory, or
overflowed required dependency causes `PARTIAL`.

## 5. Establish the requirement denominator

Parse stable IDs declared by the target and stable owner-approved UI/UX IDs whose
manifest scope matches the target's stable identity. Reject free-form titles,
headers, filenames, and unapproved proposals as denominator evidence.

Normalize at most 128 IDs and preserve provenance. If more apply, keep the full
sorted ID list in `overflow` without loading their bodies, mark the denominator
incomplete, and return `PARTIAL`. Otherwise map every ID to concrete target
locations and semantic coverage states. Also flag target behavior not supported
by a current stable source.

## 6. Apply content assertions

Evaluate common header checks and then every check in the selected profile. Use
the content-state algorithm in the rules file; heading presence is only the
starting point. Verify table rows, identifiers, states, transitions, source
links, acceptance criteria, and conditional N/A evidence.

For perceived-response claims, inspect acknowledgement, progress, feedback,
recovery, and state communication. Do not introduce a numeric latency limit.
When a cited technical performance requirement exists, verify its current source
and dimensions; do not run a profiler or claim runtime verification.

Create normalized stable findings immediately after each failed assertion.
Mechanical failures cannot be overridden by prose judgment or consultation.

## 7. Run the optional expert consultation

At standard depth, set `NOT_REQUESTED` and continue. At expert depth:

1. Prepare the single bounded worker packet from the exact target, resolved
   evidence, profile, and subjective check keys.
2. Dispatch at most one `ux-designer` reviewer with read-only/no-verdict
   constraints.
3. Validate the returned worker schema and target revision.
4. Independently normalize supported candidate findings and compare evaluations
   with local evidence.

A decline, timeout, error, malformed response, target mismatch, or unresolved
substantive evidence conflict forces `PARTIAL`. Do not retry with more reviewers
or silently downgrade to standard depth.

## 8. Reconcile a prior review

When a valid prior record is supplied:

1. Verify the envelope, extension, canonical record ID, artifact identity, prior
   target revision, author schema revision, author contract manifest revision, profile/content
   versions, and persisted evidence path. A prior different author contract is a
   migration boundary, not convergence evidence.
2. Obtain reproducible exact diff evidence between prior and current target bytes.
3. Re-evaluate every prior open or accepted-risk identity first.
4. Evaluate changed stable sections and their current dependency/requirement
   cross-references for regressions.
5. Apply stable ID reuse and explicit dispositions from the rules file.
6. Only then run remaining current assertions for new defects.

If the prior bytes/diff cannot be reproduced, preserve all observable findings
but mark convergence incomplete and the run `PARTIAL`. An invalid or unrelated
prior envelope is an input `ERROR`, not a license to start a fresh review while
pretending convergence occurred.

## 9. Finalize verdict and evidence

Confirm that every required assertion has exactly one state; every artifact and
dependency used has path and revision; the denominator is explicit; and all
consultation/convergence states are recorded. Apply the deterministic verdict
precedence from `SKILL.md`.

Construct the generic envelope and UX extension. Calculate `record_id` from a
canonical serialization with `record_id` omitted. Recalculate it once after all
fields are frozen. For batch mode, produce each target envelope independently,
then produce the manifest-bound batch summary. Do not compute an aggregate
approval verdict.

## 10. Close the mutation guard

Repeat the streaming project snapshot with the same root, exclusions, ordering,
and chunk size. Compare before and after roots.

- Equal roots -> `UNCHANGED`.
- Different roots -> `CHANGED`, list changed paths from bounded chunk comparison,
  force `PARTIAL`, and state that the run is not gate evidence.
- Incomplete snapshot -> `INCOMPLETE` and force `PARTIAL`.

The reviewer never repairs or reverts a change. It reports the evidence only.

## 11. Render the conversation response

Lead with target identity and verdict/run status. Then show:

1. target/profile/content/author-contract/schema/revision and support status;
2. dependency and denominator completeness;
3. findings ordered `MAJOR`, `BLOCKING`, then `ADVISORY`;
4. assertion-state summary and any `UNEVALUATED` checks;
5. consultation and convergence status;
6. mutation-guard result;
7. the complete machine-readable envelope(s) and batch summary where applicable;
8. explicit `NOT_PERSISTED` / `gate_evidence_eligible: false` notice.

Do not say that a draft is approved when the verdict is partial, do not hide
unchecked batch entries, and do not present accepted risk as closure.
