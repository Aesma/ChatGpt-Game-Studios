# Security-audit continued workflow

Execute these phases in order. Preserve successful independent evidence when one
phase is partial, but never use it to hide a required gap.

## Phase 1: Parse profile and prior evidence

1. Parse one optional profile enum and one optional `--prior-review` path.
2. Default absent profile to `full`; reject ambiguity before scanning.
3. Resolve one canonical repository root without following links outside it.
4. Validate prior record path containment, immutable bytes, generic/extension
   schema, canonical record ID, persistence identity, project relation, profile,
   hashes, and stable findings.

Invalid invocation/root/prior identity is `ERROR` with null verdict. Do not guess
the profile, workspace, last audit, or prior record.

## Phase 2: Establish read-only target identity

Freeze the empty allowed-write set. Run only a proven read-only VCS identity
command, if available, and capture a complete tool receipt. Record commit/ref,
dirty/untracked state, executable/version/argv/cwd, timestamps, exit, and redacted
log hash. Do not infer clean state from an absent status line.

Create a sorted streaming project snapshot of path, size, and complete SHA-256.
Process at most 256 paths in memory per chunk, hash chunks, and fold them into
`before_root`. Exclude only version-control internals and exact owner-approved
ephemeral paths. Do not read policy-denied secret/environment paths; record a
category-level permission gap without exposing their name/value.

Incomplete target identity/snapshot makes coverage partial when a meaningful
scope remains, otherwise `ERROR`.

## Phase 3: Load configuration and freeze threat scope

Read/hash applicable root-to-target AGENTS rules, technical preferences, engine
version evidence, configured source roots, target platforms, export/build presets,
online/backend/platform services, mod/plugin declarations, data classifications,
and owner-approved security adapter registry.

Build `cgs.security-threat-scope/v1` before planning checks:

1. classify protected assets and owners;
2. identify actors/capabilities/access preconditions;
3. identify trust/authority/validation zones and boundaries;
4. enumerate entry points and concrete source→validator/authority→sink flows;
5. map abuse goals to assets/boundaries;
6. assign every profile category `APPLICABLE`, evidence-backed
   `NOT_APPLICABLE`, `UNKNOWN`, or `UNSUPPORTED`;
7. preserve assumptions and unresolved questions; and
8. canonicalize/hash the frozen record.

Do not use file absence as N/A. A positively configured single-player build may
exclude network only when current engine/platform/backend/export evidence also
excludes external platform/service flows. Unknown engine/platform identity makes
affected categories partial rather than generic.

## Phase 4: Build bounded manifests and check plan

Enumerate only configured/authorized source, config, build, package, component,
and supplied artifact roots. Do not follow escaping links. Keep inclusion,
exclusion, unsupported, denied-category, unreadable, parser, oversize, and limit
states as explicit rows.

Apply all fixed bounds. Hash complete canonical rows for the source scope, build
config, and component inventory. If no meaningful evidence target exists, stop
with `ERROR`.

For every required applicable category, map each target subset to an exact check
ID, adapter, evidence method, tool/rule/config version constraints, deadline, and
expected zero side effects. Keep unsupported/missing methods in the plan. Hash
the complete plan before executing anything.

## Phase 5: Route engine/platform evidence and reviewers

Match adapters on exact engine/version/language/type/platform/category. Reject
unknown/mutating adapters. An unmatched required plan row is `UNSUPPORTED`; never
substitute a scanner for another language/ecosystem or infer platform semantics.

Build the reviewer plan:

- require `security-engineer` for all profiles except `quick`;
- add at most one exact configured engine/platform role only when a planned
  manual-semantics row requires it;
- deduplicate roles and assignments;
- cap the complete candidate list at two required reviewers; required overflow
  is partial.

Dispatch required roles in one parallel batch using redacted worker packets. Each
has one attempt and a 120-second deadline. A pre-dispatch unavailable
`security-engineer` may use the repository-authorized current-agent fallback only
when all assigned manual receipts are actually produced. Do not fall back after
timeout/block/error or impersonate engine/platform roles.

Validate worker schema, profile, source-manifest/threat-scope hashes, assignments,
receipt completeness, and secret safety. Any unsafe output is quarantined and
never forwarded.

## Phase 6: Execute eligible checks

For each planned check in stable order:

1. revalidate adapter/tool/rule/config and target-subset hashes;
2. prove the invocation has no writes, cache, update, build, download, or network
   side effect under current authority;
3. skip unsafe/unsupported invocation and record its precise coverage state;
4. execute within 120 seconds without retry;
5. capture all `cgs.security-tool-receipt/v1` fields;
6. parse results with the same versioned adapter;
7. normalize secret-safe evidence and discard/quarantine unsafe raw material; and
8. update counts without silently dropping parser failures.

Keyword search is candidate discovery only. A vulnerable data/authority path
requires a compatible dataflow result or a complete manual-flow receipt. Manual
review must identify exact hashed targets and stable source/validator/sink/
boundary symbols without quoting secret-bearing source.

Tool missing/version unknown, stale rulepack, timeout, unexplained exit, partial
parse, unsupported file, zero scanned eligible targets, unsafe output, or observed
mutation is not a pass. Mark the plan row `UNVERIFIED` or `UNSUPPORTED`.

## Phase 7: Evaluate dependencies and advisories

Build the inventory only from current hashed lockfiles/manifests/vendor metadata
or an already available secret-safe SBOM receipt. Do not generate/update a
lockfile/SBOM or fetch advisory data.

Use only a compatible local immutable advisory snapshot and successful query
receipt. Validate provider/scanner versions, snapshot ID/hash/time, owner-approved
freshness policy, component ecosystems/versions/digests, and range reasoning.

When evidence is incomplete, output `UNVERIFIED` or `UNSUPPORTED` and never “no
known CVEs.” When complete with zero matches, use only the scoped snapshot-bound
statement from the rules reference. Preserve provider-supplied CVSS metadata
without inventing or converting it.

## Phase 8: Admit and score findings safely

For each result/manual receipt:

1. discard generic keyword-only candidates from finding admission;
2. classify evidence as CONFIRMED, SUPPORTED, or CANDIDATE;
3. admit only CONFIRMED/SUPPORTED findings;
4. compute the stable fingerprint/SEC ID without hashes, line, title, secret,
   HMAC, confidence, severity, reviewer, or timestamp;
5. choose I/E/X factors from current threat/evidence rows and compute
   `CGS-SEC-IEX/v1`; use `UNRATED` when a factor is unsupported;
6. keep provider CVSS separate from project severity;
7. set lifecycle observation `OPEN`; and
8. record owner, containment, remediation, and testable closure condition.

For a likely live credential, emit only the permitted secret-safe fields and a
volatile-key truncated HMAC. Destroy the key without output. Recommend urgent
containment but do not rotate/delete/rewrite/patch.

Encryption satisfies confidentiality only when correctly evidenced; it does not
prove integrity/authenticity. Version/banner exposure is a finding only when a
concrete threat path, impact, exploitability, and exposure are established.
Multiplayer context selects evidence-backed I/E/X values; it causes no automatic
severity upgrade.

## Phase 9: Validate risk references without changing state

For every supplied risk-acceptance reference, validate all admission fields,
authority, signature, hashes/scope, controls, expiry/review trigger, and originating
audit. Mark invalid references as such without quoting secret contents.

Never create an acceptance record or change a finding. A valid unexpired reference
does not remove the finding or alter outcome/severity/coverage.

## Phase 10: Perform re-audit convergence

When prior review is valid:

1. obtain exact prior→current source/build/config/dependency diff evidence;
2. re-evaluate every prior OPEN/accepted-risk-referenced finding first;
3. verify its original closure condition with current target/tool/test evidence;
4. inspect changed assets, actors, boundaries, authority, entry points, flows,
   platforms, dependencies, build/export configuration, and adapter coverage;
5. reuse stable IDs for unchanged fingerprints; and
6. record only STILL_OPEN, CANDIDATE_RESOLVED, REGRESSED, SUPERSEDED, or
   UNVERIFIED observations.

Do not mutate lifecycle state. Missing diff/prior bytes/current closure evidence is
partial. A quick re-audit never closes or replaces full evidence; a complete full
current profile is required to assess the entire current scope.

## Phase 11: Calculate coverage and outcome

Finalize every category and coverage dimension. Report exact planned, covered,
unsupported, unverified, excluded, and unchecked counts/bytes plus secret-safe gap
IDs. A zero denominator is complete only with positive threat-scope evidence.

Apply outcome precedence:

1. invalid/global failure/no meaningful check -> `ERROR`;
2. any required gap after meaningful evidence -> `PARTIAL`;
3. complete coverage plus findings -> `FINDINGS`;
4. complete coverage and zero findings ->
   `NO_FINDINGS_IN_SCANNED_SCOPE`.

Preserve confirmed findings under `PARTIAL`. Do not turn uncertainty into a
finding or no-finding conclusion.

## Phase 12: Re-hash, close mutation guard, and render

Re-hash every evidence artifact. Any target/config/build/adapter/tool/rule/
advisory/prior-record mismatch invalidates dependent evidence and forces partial
or error.

Repeat the streaming snapshot with identical root/exclusions/chunking:

- equal roots -> `UNCHANGED`;
- unequal roots -> `CHANGED`, retain only secret-safe changed-path evidence and
  return at most `PARTIAL`;
- incomplete -> `INCOMPLETE` and return at most `PARTIAL`.

Never repair or clean mutations.

Freeze the complete generic envelope and extension, compute canonical `record_id`,
and validate all secret-safe fields. Return:

1. outcome and `NOT A SHIP/RELEASE APPROVAL`;
2. target/source/build/threat/check/stale hashes;
3. bounded manifests and engine/platform/adapter routing;
4. category/dimension coverage and exact gaps;
5. versioned tool/manual/reviewer/advisory evidence;
6. redacted stable findings and IEX factors;
7. risk-reference/re-audit observations;
8. mutation guard; and
9. complete machine-readable envelope with `NOT_PERSISTED` and gate-ineligible.

Stop. Do not write a report, run remediation, accept risk, claim resolution, or
make a release decision.
