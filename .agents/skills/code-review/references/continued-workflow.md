# Code-review continued workflow

Execute these phases in order. The rules reference is normative when this file
only elaborates procedure.

## Phase 1: Parse and contain inputs

1. Parse only named `--target` and `--story` options.
2. Establish one canonical repository root and repository identity.
3. Normalize each literal path without resolving it outside root.
4. Reject globs, absolute/device/UNC paths, traversal escape, duplicates, links
   that escape root, invalid target node types, and an invalid story schema.
5. Record the normalized `cgs.code-review-input/v1` object.

Stop with input `ERROR` and null verdict if no target input can proceed. Do not
fall back to the current directory, changed Git files, last story, or conversation
memory.

## Phase 2: Establish the read-only mutation baseline

The allowed write set is empty. Produce a sorted streaming snapshot of all regular
project files except version-control internals and exact owner-approved ephemeral
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
Process at most 256 paths in memory per chunk; revision each chunk, then fold ordered
chunk revisions into `before_root`.

If an in-scope path cannot be enumerated or versioned, keep reviewing observable
evidence but record `MUTATION_BASELINE_INCOMPLETE`; final verdict must be
`PARTIAL`. The snapshot is mutation evidence, not permission to read excluded
credentials or other denied paths.

## Phase 3: Resolve the bounded target manifest

For each direct target:

- A regular file is classified directly.
- A directory is traversed in sorted order to depth 12.
- Do not follow a symlink/junction outside root.
- Apply generated/vendor/cache/build exclusions only with the evidence required
  by the rules reference.
- Record every encountered candidate row before applying file/byte bounds.

Sort and case-normalize for collision detection. revision all eligible files before
selection. Enforce 64 files, 524288 bytes per file, and 4194304 total exact bytes.
Preserve overflow and enumeration failures as manifest rows. If the manifest has
no eligible source file, return input `ERROR`; otherwise any unreadable/error/
unchecked eligible row makes target coverage partial.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## Phase 4: Load rules per target

For each eligible selected file independently:

1. Read/revision repository-root `AGENTS.md`.
2. Walk root-to-parent and read/revision every nested `AGENTS.md`.
3. Follow only direct subject-applicable standards links from that chain.
4. Read/revision current coding standards and technical preferences when linked or
   otherwise explicitly governed by the chain.
5. Parse the optional story's stable ID, type, acceptance criteria, QA scope,
   explicit target mapping, and explicit ADR IDs.
6. Resolve exact target-header/manifest ADR IDs.
7. Read configured analyzer rule sets only when a check uses them.

Build source and rule ledgers. Apply closest-AGENTS precedence only to overlapping
keys in its declared subtree. For every other conflict require explicit override/
supersession evidence. Do not fill unconfigured placeholders from general game
industry practice.

Classify each rule's target applicability, normative level, severity, and evidence
method before reading code for violations. Unsupported N/A, unresolved modality,
source overflow, broken link, conflict, or unknown scope is a coverage gap.

## Phase 5: Resolve explicit ADR evidence

Build one sorted, deduplicated ADR declaration list from exact story, source
header, and referenced owner-approved implementation-manifest locations. Keep
declaration provenance and target scope.

Resolve at most 16 stable IDs through their exact declared paths or current
authoritative index records. Do not choose by filename similarity or commit
recency. Record commit-message matches only under `non_authoritative_clues`; they
cannot add to the ADR set.

For each ADR, revision bytes and validate stable ID, unique resolution, status,
Decision, Consequences, scope, and supersession links. Admit only current
`Accepted` decisions to the rule ledger. A readable non-Accepted ADR receives
`ADR_NOT_EVALUATED`; missing/ambiguous/stale/invalid evidence is partial. If
governing project rules require an ADR but the explicit set is empty, record the
gap rather than declaring compliance.

## Phase 6: Evaluate deterministic evidence

Create every applicable rule check before evaluation. For each target/rule pair:

1. Select the required evidence method.
2. Verify current target and rule-source revisions.
3. Use direct source evidence only for local facts it can prove.
4. For AST, linter, graph, profiler, runtime, build, or test claims, find a current
   compatible `cgs.code-analysis-receipt/v1` or execute only a configured analyzer
   invocation proven to make no writes.
5. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
6. Set exactly one check state and retain exact evidence.

Never install a tool, generate an analysis project, compile, build, run tests, or
profile as part of this read-only workflow. Tool failure/timeout/incompatibility
is `UNVERIFIED`, not a code failure and not a pass. A required unverified check
makes coverage partial.

Normalize confirmed failures into stable findings. Derive severity from the rule
ledger. Keep unsupported reviewer-style improvements separate as `INFO` advice.

## Phase 7: Plan bounded reviewers

Read the exact Engine Specialists and extension/type routing configuration. Map
each target to configured roles; do not infer Godot, Unity, Unreal, language, UI,
shader, or native routing from generic filenames when the configuration does not
say so.

Build candidates for the lead, exact configured engine specialists, Primary only
where its configured scope/fallback permits, and story-required QA testability.
Merge duplicate roles and their assigned files/rules. Sort with the rules table.
Record every candidate before applying the three-reviewer cap.

Dispatch up to three required roles once in parallel with exact worker packets.
Allow at most one retry for a transient no-response inside the same 120-second
total per-role deadline. Do not wait indefinitely. A required overflow role is
`NOT_DISPATCHED_LIMIT`; unavailable, decline, block, timeout, error, malformed
schema, out-of-scope evidence, or manifest/target revision mismatch is recorded by
exact status and makes reviewer coverage partial.

When `lead-programmer` is unavailable, the current agent may complete that exact
integrated responsibility and record `DONE_LOCAL_FALLBACK`. Do not use this to
impersonate a configured engine or QA specialist. Reviewer findings remain
candidate observations until locally mapped to a current rule and target revision.

## Phase 8: Normalize ownership and findings

For each verified failure or source-accepted specialist judgment:

1. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
2. Establish stable symbol/subject, rule ID/path/revision, and normalized defect class.
3. Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
4. Derive severity from the rule ledger or use `INFO / REVIEWER-ADVICE`.
5. Cite exact evidence location without including the line in the stable key.
6. State source-bound consequence, owner, and bounded remediation.

Code-quality and Accepted-ADR conformity stay with code/architecture ownership.
Potential vulnerability, runtime performance, or executed-test-evidence issues
are explicitly routed as candidates to their domain owners; do not claim those
gates, invoke their workflows, or duplicate their approvals.

Do not manufacture Positive Observations. Include a positive observation only
when exact target/rule evidence supports it, and never let praise offset a
finding or coverage gap.

## Phase 9: Calculate coverage and verdict

Finalize all six coverage dimensions from the rules reference. Every applicable
check must be verified pass/fail or evidence-backed N/A. Report numerator,
denominator, and every named gap for targets, sources, checks, ADRs, and reviewers.
Do not treat a zero denominator as complete without explicit empty-set evidence.

Apply verdict precedence mechanically:

1. invalid/nonexistent empty manifest -> input `ERROR`, null verdict;
2. any coverage gap -> `PARTIAL`;
3. otherwise open blocking -> `NEEDS CHANGES`;
4. otherwise open warning -> `CONCERNS`;
5. otherwise -> `APPROVED`.

Preserve confirmed blocking/warning findings under `PARTIAL`; incompleteness takes
precedence because the review cannot certify its total severity.

## Phase 10: re-read and close mutation guard

Re-read every reviewed target and evidence artifact and record its declared revision. A mismatch is
`TARGET_CHANGED_DURING_REVIEW` or `EVIDENCE_CHANGED_DURING_REVIEW`, invalidates
dependent claims, and forces `PARTIAL`.

Repeat the streaming project snapshot using identical root, exclusions, ordering,
and 256-path chunking:

- equal roots -> `UNCHANGED`;
- unequal roots -> `CHANGED`, record bounded changed-path evidence and force
  `PARTIAL`;
- incomplete snapshot -> `INCOMPLETE` and force `PARTIAL`.

Do not repair, revert, stage, or otherwise alter a changed file.

## Phase 11: Render one evidence record

Freeze the complete generic envelope and `cgs.code-review/v2` extension. Include
all target/evidence artifact revisions, the complete manifest including exclusions
and unchecked rows, rule sources and checks, ADRs, tool receipts, reviewer plan/
results, coverage, findings, mutation guard, and stale key.

Calculate `record_id` from canonical normalized payload bytes with `record_id`
omitted. Validate it once after all fields are frozen. State that direct output is
`NOT_PERSISTED` and gate-ineligible.

Present:

1. manifest identity/revision and verdict;
2. coverage summary and every gap;
3. findings ordered `BLOCKING`, `WARNING`, `INFO`;
4. rule, ADR, analysis, reviewer, and mutation evidence;
5. the complete machine-readable envelope;
6. bounded remediation tied to source rules.

Stop after delivering findings. Do not offer a review override, invoke
`story-done`, mark a story complete, or imply that a partial/concerning review is
completion evidence.
