# Code-review rules v1

This file is normative for `code-review`.

## Contract identity

- Rules schema: `cgs.code-review-rules/v1`
- Review extension: `cgs.code-review/v2`
- Generic envelope: `cgs.review-evidence/v1`
- Reviewer packet: `cgs.code-review-worker/v1`
- Analysis receipt: `cgs.code-analysis-receipt/v1`

Compute `skill_bundle_sha256` over exact `SKILL.md` bytes, one NUL byte,
exact `continued-workflow.md` bytes, one NUL byte, then exact
`review-rules-v1.md` bytes. Expose it as the producer version.

## Fixed limits

| Limit | Value |
|---|---:|
| Explicit target roots | 8 |
| Eligible target files | 64 |
| Directory traversal depth below each target | 12 |
| Exact bytes per target file | 524288 |
| Exact bytes across target manifest | 4194304 |
| Applicable rule sources | 32 |
| Explicit ADRs | 16 |
| Analysis receipts | 32 |
| Required reviewers including lead | 3 |
| Dispatch attempts per reviewer | 2 |
| Total collection deadline per reviewer | 120 seconds |
| Paths per mutation-snapshot chunk | 256 |

Crossing a limit never authorizes truncation. Preserve all discoverable manifest
identities, record overflow as unchecked, and return `PARTIAL`. If a direct input
cannot form any valid manifest, return input `ERROR` with null verdict.

## Strict input model

Normalize input as:

```yaml
schema: cgs.code-review-input/v1
targets: [<one to eight literal project-relative paths>]
story: <one literal project-relative .md path or null>
```

Reject:

- absent `--target`, positional targets, or target values beginning with `-`;
- more than eight targets, more than one story, duplicate canonical targets;
- absolute/UNC/device paths, `..` escape, glob metacharacters, NUL/control bytes;
- missing paths, symlink/junction escape, or non-regular/non-directory targets;
- a direct binary, generated, vendored, cache, build-output, document, asset, or
  otherwise ineligible non-source file;
- a story outside the project, without a stable story identity, or without the
  minimum current story schema needed to interpret its scope.

Eligible source classification comes from current project/engine configuration
and owner-approved target rules. Portable textual code/script/header/shader/build
definition types may be recognized for manifest formation, but recognition does
not impose language standards or select an engine specialist. Binary engine
assets are ineligible unless an exact owner-approved textual inspection adapter
exists and records a compatible analysis receipt.

## Bounded target manifest

Every row uses:

```yaml
path: <canonical project-relative path>
origin_target: <canonical input target>
entry_type: regular-file | symlink | junction | directory | other
source_type: <configured language/type or unknown>
size_bytes: <integer or null>
sha256: <complete lowercase SHA-256 or null>
eligibility: ELIGIBLE | EXCLUDED | ERROR | UNCHECKED
reason: <stable reason code>
```

Sort by Unicode-normalized, slash-separated canonical path. Reject case-folded
duplicates on case-insensitive filesystems. Always exclude version-control
internals. Exclude generated/vendor/cache/build files only with current
owner-approved path rules, a committed generation marker, or a source declaration
that proves the classification; store that evidence path/hash. A directory name
alone is insufficient.

Hash the canonical sorted manifest rows to produce `target_manifest_hash`.
The reviewed set is the first 64 eligible sorted rows that also fit the per-file
and total-byte limits. Keep every remaining known row as `UNCHECKED` with
`FILE_LIMIT`, `FILE_BYTES_LIMIT`, `TOTAL_BYTES_LIMIT`, or `DEPTH_LIMIT`. An
enumeration error, unreadable eligible file, or undiscovered subtree makes
manifest coverage incomplete.

## Rule-source chain and precedence

For every target file independently, record:

1. repository-root `AGENTS.md`;
2. every nested `AGENTS.md` from root toward the target parent;
3. directly referenced coding/technical/project standards whose subjects apply;
4. the exact optional story requirements scoped to the target;
5. each explicit current Accepted ADR scoped to the target; and
6. exact configured analyzer/linter rule sets used by evidence tools.

Runtime system/developer/user instructions still govern execution but are not
forged into project review findings.

Each source row contains path, SHA-256, source type, declared scope, target paths,
precedence basis, and currentness. A closest nested `AGENTS.md` overrides an
ancestor only where the repository contract grants closest-file precedence.
Story/ADR specificity does not silently override repository standards. An exact
source must state an exception or supersession; otherwise contradictory
normative requirements are `RULE_CONFLICT`, an `UNVERIFIED` check, and `PARTIAL`.

Do not share a leaf rule file between sibling target subtrees unless its declared
scope includes both. Missing/unreadable applicable sources, broken direct links,
unknown scope, or unresolved precedence are coverage gaps.

## Rule ledger and severity

Create one stable rule row per applicable normative requirement:

```yaml
rule_id: <explicit stable ID or deterministic generated key>
source_path: <canonical path>
source_sha256: <hash>
source_location: <heading/key/line evidence>
normative_text_hash: <hash>
targets: [<paths>]
applicability: APPLICABLE | NOT_APPLICABLE | UNKNOWN
applicability_evidence: <exact source and rationale>
normative_level: MUST | MUST_NOT | SHOULD | SHOULD_NOT | MAY | UNSPECIFIED
severity: BLOCKING | WARNING | INFO | UNRESOLVED
evidence_method: SOURCE | AST | LINTER | BUILD_GRAPH | PROFILER | RUNTIME |
                 SPECIALIST | COMPOSITE
check_state: VERIFIED_PASS | VERIFIED_FAIL | NOT_APPLICABLE | UNVERIFIED
```

Prefer an explicit source rule ID. Otherwise generate a stable key from canonical
source path, stable heading/key, and normalized normative sentence. Store the
current source hash separately.

Severity is derived, never guessed:

| Authoritative source semantics | Severity |
|---|---|
| explicit `MUST`, mandatory, required, blocking gate, or `MUST NOT`/forbidden | `BLOCKING` |
| explicit `SHOULD`/`SHOULD NOT`, warning, or non-blocking required review concern | `WARNING` |
| explicit `MAY`, preference, suggestion, or optional guidance | `INFO` |
| no reliable modality or conflicting authority | `UNRESOLVED` |

`UNRESOLVED` severity cannot yield a blocking/warning verdict; the check is
`UNVERIFIED` and forces `PARTIAL`. A reviewer may report unsupported improvement
advice only as `INFO` with `rule_id: REVIEWER-ADVICE`; it is not a rule pass/fail.

The following framework-owned ADR classifications are deterministic:

- an implementation uses a pattern an Accepted ADR explicitly rejects or forbids
  -> `BLOCKING` / `ADR-FORBIDDEN-PATTERN`;
- implementation meaningfully diverges from an Accepted chosen approach without
  using an explicitly forbidden pattern -> `WARNING` / `ADR-DRIFT`;
- a small, non-semantic difference from optional guidance -> `INFO` /
  `ADR-MINOR-DEVIATION`;
- an explicit readable non-Accepted ADR -> `WARNING` /
  `ADR-NOT-ACCEPTED`, while its Decision is not compliance authority.

## Applicability and N/A

`NOT_APPLICABLE` requires all of:

- the rule source permits conditional applicability;
- exact target language/type/symbol/scope evidence excludes the condition;
- the evidence path and hash are current; and
- the rationale is specific enough to reproduce.

Engine/language rules cannot be N/A merely because engine configuration is
missing. Missing configuration produces `UNKNOWN` applicability or
`ROUTING_UNCONFIGURED`, hence `UNVERIFIED` and `PARTIAL` when the target exposes
engine-specific code.

## Analysis evidence

Direct source inspection may verify local textual/syntactic facts only when the
fact does not require semantic expansion. Examples include presence of an exact
public doc comment or a direct forbidden token whose rule defines that pattern.

Use these minimum evidence methods:

| Claim | Minimum compatible evidence |
|---|---|
| cyclomatic/cognitive complexity | parser/AST or configured linter rule |
| call/dependency cycles | current build, module, or symbol dependency graph |
| dynamic dispatch/type substitution | compatible language semantic model |
| hot-path allocation | configured static analyzer or current profiler trace |
| runtime performance/frame budget | current profiler/test receipt for exact platform/scenario |
| thread safety/races | compatible analyzer plus synchronization model, or current runtime evidence |
| compile/build correctness | existing current build receipt |
| test pass/coverage | existing current test-evidence receipt; code review does not execute tests |

An analysis receipt is usable only with this shape:

```yaml
schema: cgs.code-analysis-receipt/v1
receipt_id: <stable ID>
tool: <name>
tool_version: <exact version>
configuration_path: <path or null>
configuration_sha256: <hash or null>
input_artifacts: [{path, sha256}]
capabilities: [<claim classes actually supported>]
invocation: <exact read-only invocation or recorded external run identity>
result_path: <path or embedded>
result_sha256: <hash>
executed_at: <ISO-8601 UTC or null>
status: PASS | FAIL | PARTIAL | ERROR
```

Input/hash mismatch, incompatible tool/language/version/configuration, ambiguous
capability, missing result, timeout, partial receipt, or unproven read-only
invocation makes the dependent rule `UNVERIFIED`. Never infer a clean AST, graph,
allocation, runtime, build, or test result from natural-language inspection.

## ADR evidence

Each explicit ADR row contains:

```yaml
adr_id: <stable ID>
declared_by: [{path, sha256, location}]
resolved_path: <canonical path or null>
sha256: <hash or null>
status: Accepted | Proposed | Superseded | Deprecated | Rejected | Unknown
decision_present: <boolean>
consequences_present: <boolean>
scope_targets: [<paths>]
evidence_state: EVALUATED | ADR_NOT_EVALUATED | MISSING | AMBIGUOUS |
                STALE | INVALID
```

Only one exact current `Accepted` record with Decision and Consequences may be
`EVALUATED`. Multiple IDs are all evaluated independently. A superseding ADR must
be followed only through its explicit stable link. A commit subject/body, branch
name, filename resemblance, repository age, or recent-touch heuristic is a clue,
not declaration or compliance evidence.

When an applicable current source requires ADR governance but the explicit set is
empty, record `ADR_NOT_EVALUATED` as a coverage gap. A source-backed explicit N/A
is allowed only when the applicable rules state that this target class needs no
ADR.

## Engine-specialist and reviewer routing

Read and hash `.codex/docs/technical-preferences.md` or the current configured
equivalent. Extract engine identity, language, named specialists, extension/type
routing rows, and declared fallback notes. Do not invent mappings.

Build reviewer candidates:

1. `lead-programmer` — always required for an otherwise valid manifest;
2. exact configured language/code, shader, UI, native/plugin, or other specialist
   for the target rows mapped to it;
3. configured Primary for broad engine lifecycle/architecture targets or only an
   explicitly permitted missing-row fallback; and
4. `qa-tester` only when the exact story type/scope makes code testability or
   manual-verification reachability an applicable review responsibility.

Deduplicate by canonical role. Merge assigned target/rule sets and reasons.
Never add Primary twice when it is also a specific configured role. If engine
configuration is `[TO BE CONFIGURED]`, generic code may proceed without an engine
reviewer, but an engine-specific target/rule has `ROUTING_UNCONFIGURED` and
incomplete coverage.

Sort candidates deterministically:

1. lead;
2. roles explicitly required by the story or applicable rule source;
3. narrow configured extension/type mappings, by canonical role ID;
4. configured Primary fallback/general architecture;
5. optional advisory candidates.

Dispatch the first three required candidates in one parallel batch. Required
candidates beyond the cap are `NOT_DISPATCHED_LIMIT` and force `PARTIAL`.
Optional advisory candidates beyond the cap are `NOT_APPLICABLE` and do not.

Each reviewer has at most two attempts within one 120-second total deadline. A
retry is allowed only for transient no-response and cannot reset the deadline.
Accepted status vocabulary:

```text
DONE | DONE_LOCAL_FALLBACK | NOT_APPLICABLE | NOT_DISPATCHED_LIMIT |
UNAVAILABLE | DECLINED | BLOCKED | TIMEOUT | ERROR | INVALID_RESPONSE
```

Only `DONE`, a valid lead-only `DONE_LOCAL_FALLBACK`, and evidence-backed
`NOT_APPLICABLE` complete required reviewer coverage.

Reviewer request:

```yaml
schema: cgs.code-review-worker/v1
run_id: <run ID>
role: <canonical role>
target_manifest_hash: <hash>
targets: [{path, sha256}]
assigned_rule_ids: [<IDs>]
rule_sources: [{path, sha256}]
adr_evidence: [{adr_id, path, sha256, status}]
constraints: {read_only: true, may_decide_verdict: false, may_write: false}
```

Usable response:

```yaml
schema: cgs.code-review-worker/v1
status: DONE
role: <same role>
target_manifest_hash: <same hash>
target_hashes: [{path, sha256}]
evaluations: [{rule_id, target_path, check_state, evidence, rationale}]
candidate_findings: [{rule_id, target_path, stable_subject, defect_class,
                      proposed_severity, evidence, rationale}]
```

The lead validates schema, scope, hashes, evidence, and rule severity. Reviewer
output cannot turn an `UNVERIFIED` mechanical check into verified evidence unless
the rule explicitly accepts specialist judgment as its evidence method.

## Stable finding contract

Finding states are `OPEN`, `ACCEPTED_RISK`, `RESOLVED`, or `SUPERSEDED`; a fresh
review normally emits current `OPEN` and separately referenced accepted risks.

Fingerprint material is:

```text
canonical target path + stable symbol/subject + stable rule ID + normalized
defect class
```

Exclude target/rule hashes, line numbers, prose wording, timestamps, run/reviewer
IDs, and severity from the fingerprint. Finding ID is:

```text
CRF-<sanitized-rule-id>-<first-12-of-SHA256(fingerprint)>
```

Each finding contains:

```yaml
finding_id: <stable ID>
fingerprint: <full SHA-256>
state: OPEN | ACCEPTED_RISK | RESOLVED | SUPERSEDED
severity: BLOCKING | WARNING | INFO
rule: {id, source_path, source_sha256, source_location}
target: {path, sha256, stable_subject, evidence_location}
check_state: VERIFIED_FAIL | UNVERIFIED
defect_class: <stable class>
observation: <evidence-bound statement>
consequence: <source-bound impact>
owner: code | architecture | security | performance | test-evidence | other
remediation: <bounded action>
```

An accepted risk must cite a separate current owner/authority/scope/rationale/
expiry record. It does not change severity, coverage, or verdict.

Security/performance/test-execution candidate observations retain stable finding
IDs but are explicitly owner-routed. They do not claim those domain gates passed
and do not invoke their workflows.

## Coverage ledger

Coverage dimensions are:

```yaml
targets: {status: COMPLETE | PARTIAL, reviewed, eligible, unchecked: []}
rule_sources: {status: COMPLETE | PARTIAL, resolved, applicable, gaps: []}
checks: {status: COMPLETE | PARTIAL, verified_or_na, applicable, unverified: []}
adr_evidence: {status: COMPLETE | PARTIAL | NOT_APPLICABLE,
               evaluated, explicit, gaps: []}
reviewers: {status: COMPLETE | PARTIAL, completed, required, gaps: []}
mutation_guard: {status: COMPLETE | PARTIAL, before_root, after_root, changed: []}
```

Overall coverage is complete only when every required dimension is complete or
evidence-backed not applicable. Empty-set states require proof:

- zero target files is input `ERROR`;
- zero applicable rules is `PARTIAL`, not a clean review;
- zero ADRs is complete only with explicit source-backed N/A;
- zero engine specialists is complete only when no configured/applicable engine
  routing is required;
- zero findings with complete coverage may be approved.

## Verdict table

| Condition, in precedence order | Verdict |
|---|---|
| input cannot form a valid non-empty manifest | null (`ERROR`) |
| any required coverage dimension partial | `PARTIAL` |
| complete coverage and at least one open `BLOCKING` | `NEEDS CHANGES` |
| complete coverage, no blocking, at least one open `WARNING` | `CONCERNS` |
| complete coverage with only `INFO` or no findings | `APPROVED` |

`PARTIAL` takes precedence even when a confirmed blocking finding is already
known. Preserve the finding; do not claim a complete severity verdict.

## Review-evidence output

Return this exact shape for a valid manifest:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<canonical normalized payload with record_id omitted>
artifact_id: code-review:<first-16-of-target-manifest-hash>
artifacts:
  - path: <canonical project-relative path>
    sha256: <complete lowercase SHA-256>
    role: target | story | AGENTS | project-standard | ADR | analyzer-config |
          analysis-receipt
    source_id: <stable ID or null>
reviewer: code-review:<run-id>
verdict: APPROVED | CONCERNS | NEEDS CHANGES | PARTIAL
timestamp: <ISO-8601 UTC with fractional seconds>
finding_ids: [<stable CRF IDs>]
producer:
  tool: code-review
  version: sha256:<skill_bundle_sha256>
extension:
  schema: cgs.code-review/v2
  run_id: CR-<compact UTC>-<manifest12>-<UUIDv4>
  project_id: <canonical repository identity>
  source_revision: {commit: <commit or null>, input_state: clean | dirty | includes-untracked-inputs}
  target_manifest_hash: <hash>
  stale_key: <digest of project/manifest/rules/ADRs/tool receipts/reviewer contract>
  input: {targets: [<paths>], story: <path or null>}
  limits: <all effective fixed limits>
  target_manifest: [<all rows, including excluded/error/unchecked>]
  rule_sources: [<complete source rows>]
  rule_ledger: [<complete rule rows>]
  adr_evidence: [<complete ADR rows>]
  analysis_evidence: [<complete receipt/capability rows>]
  reviewer_plan: [<candidate, reason, assignments, required, disposition>]
  reviewer_results: [<validated results/failures>]
  coverage: <complete coverage ledger>
  findings: [<complete stable finding objects>]
  accepted_risk_refs: [<exact records>]
  partial_reasons: [<stable reason codes and evidence>]
  mutation_guard:
    before_root: <streaming tree hash>
    after_root: <streaming tree hash>
    status: UNCHANGED | CHANGED | INCOMPLETE
    changed_paths: [<bounded evidence>]
  approval_status: APPROVED | NOT_APPROVED
  gate_evidence_status: NOT_PERSISTED
  gate_evidence_eligible: false
```

Every target file and every artifact used as evidence appears in `artifacts` with
its exact current hash. `record_id` is calculated only after the record is frozen.
Any artifact/rule/ADR/receipt/reviewer-contract/target-manifest hash change makes
the record stale. Direct skill output is always non-persisted and gate-ineligible.

For input `ERROR`, return a bounded error object with schema, error code, rejected
input, project-root containment evidence, and remediation. Set `verdict: null`;
do not forge a review envelope or finding coverage.
