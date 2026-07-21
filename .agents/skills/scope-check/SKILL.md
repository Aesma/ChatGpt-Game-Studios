---
name: scope-check
description: "Read-only comparison of one explicit immutable scope baseline with one current scope manifest, using stable scope IDs and evidence coverage without deciding product cuts or re-baselining."
---

# Scope Check

## Invocation and contract

Invoke one read-only command:

```text
$scope-check compare --baseline <path> --current <path>
$scope-check inspect --baseline <path> --current <path> [--evidence <manifest-path>]
$scope-check discover
```

- `compare` is the normal operation and returns the canonical delta report.
- `inspect` adds bounded implementation, estimate, dependency, test, or change-record
  evidence named by one evidence manifest. It does not infer scope from code.
- `discover` only lists exact active-state candidate paths and their hashes. It does
  not choose a pair or produce a scope verdict.

Both `--baseline` and `--current` are required for analysis. A path supplied without
its counterpart, a feature name, sprint nickname, story nickname, or no arguments is
not resolved by fuzzy matching. Return `INPUT REQUIRED` with the exact invocation
needed. If active state exposes exactly one apparent pair, show it as a suggestion and
ask the user to confirm both paths; do not analyze it in the same invocation.

This skill is strictly read-only. It does not create or edit plans, stories, scope
manifests, decisions, estimates, reports, Git state, or session state. It invokes no
director gate and delegates no product decision.

## Non-negotiable rules

1. **Explicit immutable comparison** — identify the baseline and current artifact by
   canonical repository-relative path, byte length, SHA-256, schema/version, and their
   declared parent scope. Capture the baseline approval/version and its source commit
   or recorded timestamp. Re-read and re-hash both before the final result.
2. **Stable identity, not item count** — compare stable `Scope ID` values and semantic
   content hashes. Never derive scope health, effort growth, or a verdict from raw item
   counts, checklist row counts, files, commits, TODOs, or percentages of those counts.
   Splitting or merging presentation rows cannot change scope by itself.
3. **Evidence before metrics** — effort, schedule, quality, and integration statements
   require declared evidence with matching scope IDs and hashes. Missing evidence is
   `UNVERIFIED`; it is never guessed from prose, commit authors, or model judgment.
4. **Advisory, not decisional** — report additions, removals, semantic modifications,
   coverage gaps, and neutral response options. Never label an item `Cut`, `Keep`,
   `Defer`, justified, approved, or re-baselined without a cited decision/change
   record. The user or designated producer owns the choice.
5. **No implicit baseline** — active milestone/sprint state may suggest paths only.
   Multiple matches, missing approval/version, a changed baseline hash, or an
   ambiguous parent relationship blocks comparison.
6. **No code-derived scope** — code, Git history, TODO/FIXME, issue text, or build
   output can prove implementation activity only. None creates or changes approved
   product scope.
7. **Bounded reads** — read only the two scope artifacts and the exact supporting
   paths/commits listed in the optional evidence manifest, subject to the budgets
   below. Never scan the repository for “related” files.
8. **Immutable re-checks** — re-running against the same baseline hash compares to the
   same baseline. A new baseline requires an independently recorded product decision;
   this skill neither creates nor applies it.

## Authority and ownership boundaries

| Concern | Owner | This skill may do |
|---|---|---|
| Detect scope delta | `scope-check` | Read and classify exact evidence |
| Estimate effort | `$estimate` or recorded estimator | Consume a bound estimate receipt |
| Choose cut/keep/defer or timeline tradeoff | User/designated producer | Present neutral options and request a choice |
| Approve a scope change | User/designated product owner | Cite an existing decision/change record |
| Apply sprint or milestone changes | `$sprint-plan update` or owning planner | Provide a read-only handoff after a decision |
| Re-baseline | Product owner and owning planner | Compare a later approved baseline as a new version |

Agent roles, model recommendations, conversational approval of the report, and a
`NO SCOPE DELTA` result grant no mutation or product authority.

## Required artifact contracts

### Baseline scope artifact

The baseline must provide or be accompanied by:

- artifact kind and schema/version;
- canonical path, byte length, SHA-256;
- stable baseline ID and baseline version;
- approval state, approver/decision owner, approval record path/hash, and timestamp;
- source commit or immutable content revision;
- parent scope ID and timebox/release identity;
- complete ordered scope entries with unique stable `Scope ID`, title, description,
  acceptance boundary, and status at approval time;
- explicit exclusions/non-goals;
- declared completeness marker.

If approval, version, stable IDs, uniqueness, parent identity, or completeness is
missing, return `INSUFFICIENT EVIDENCE`. Do not synthesize IDs from titles or row
positions.

### Current scope manifest

The current artifact must provide:

- artifact kind and schema/version;
- canonical path, byte length, SHA-256 and current revision/commit if recorded;
- current manifest ID and declared baseline ID/version/hash;
- same parent scope and timebox/release identity as the baseline;
- complete ordered scope entries with unique stable `Scope ID`, title, description,
  acceptance boundary, state, and any linked change-record ID;
- explicit removals or supersessions rather than silently deleting identities;
- declared completeness marker.

A story, epic, sprint, milestone, or feature file is valid only if it satisfies this
manifest contract or points to a unique companion manifest that does. A story may be
compared with its explicitly referenced approved parent epic baseline; the parent path
may not be inferred by filename similarity.

### Optional evidence manifest

The evidence manifest is an allowlist, not a discovery hint. It contains:

- its own path/hash/schema/version and the exact baseline/current hashes it covers;
- exact supporting paths with purpose and expected hash;
- exact Git commit IDs/range, if implementation evidence is needed;
- estimate, dependency, test, and change-record receipts keyed by stable Scope ID;
- total path, byte, and commit budgets.

Defaults: at most 40 supporting paths, 2 MiB total text, and 100 commits. Exceeding a
budget returns `PARTIAL` with the unexamined entries. Do not silently truncate and do
not expand the allowlist.

## Canonical delta schema

Each finding has one stable `Delta ID`, deterministically derived from the baseline
ID/version/hash, current manifest hash, Scope ID, and delta type:

```yaml
Delta ID: SCP-DELTA-<digest-prefix>
Scope ID: <stable-id>
Delta Type: ADDED | REMOVED | MODIFIED | UNCHANGED | UNMAPPED | CONFLICT
Baseline:
  Path: <path-or-NONE>
  Artifact SHA-256: <hash>
  Entry SHA-256: <hash-or-NONE>
Current:
  Path: <path-or-NONE>
  Artifact SHA-256: <hash>
  Entry SHA-256: <hash-or-NONE>
Change Record: <path/hash/status or NONE>
Decision State: APPROVED_CHANGE | PROPOSED_CHANGE | NO_RECORD | CONFLICTING_RECORD
Effort Evidence: VERIFIED | UNVERIFIED | NOT_APPLICABLE
Risk Evidence: VERIFIED | PARTIAL | UNVERIFIED | NOT_APPLICABLE
Notes: <evidence-grounded summary>
```

Classification is set-based and hash-based:

- ID only in current: `ADDED`;
- ID only in baseline: `REMOVED`;
- ID in both with different normalized semantic-entry hashes: `MODIFIED`;
- ID and semantic hash equal: `UNCHANGED`;
- missing/non-unique ID: `UNMAPPED`;
- incompatible parent/baseline/change records: `CONFLICT`.

Titles and ordering are display fields, never identity. A pure row split/merge may be
recognized as presentation-only only when stable IDs and normalized semantic content
prove equivalence; otherwise classify it `UNMAPPED`, not as an effort percentage.

## Evidence coverage and optional metrics

Report coverage before impact:

```text
Scope identity coverage = valid unique current Scope IDs / declared current entries
Change-record coverage = changed IDs with matching records / changed IDs
Effort coverage = changed IDs with compatible estimate receipts / changed IDs
Risk coverage = changed IDs with dependency/test evidence / changed IDs
```

Coverage ratios describe evidence availability only; they are not scope-health scores.
If a denominator is zero, show `NOT APPLICABLE`, not 100%.

Effort delta may be calculated only when every compared changed entry has estimates
from the same calibrated unit, method, confidence policy, and baseline/current scope
hashes. Report absolute values and uncertainty interval. Otherwise output:
`Effort Delta: UNVERIFIED — incompatible or incomplete estimate evidence`.

Risk dimensions use only these deterministic evidence tests:

- `Schedule`: verified estimate delta plus documented capacity/timebox receipt;
- `Quality`: changed acceptance boundary plus matching regression/test-plan coverage;
- `Integration`: changed dependency/interface set plus matching dependency evidence.

For each dimension output `SUPPORTED`, `PARTIAL`, `UNVERIFIED`, or `NOT APPLICABLE`
with receipt paths/hashes. Do not translate these into Low/Medium/High by intuition.

## Canonical result states

Derive exactly one result:

| Result | Conditions |
|---|---|
| `ERROR` | Invalid syntax, path escape, duplicate input, unreadable artifact, or multiple/fuzzy resolution |
| `INPUT REQUIRED` | `discover`, no arguments, or one required input missing; no comparison performed |
| `INSUFFICIENT EVIDENCE` | Baseline/current identity, approval, stable IDs, parent link, version, hash, or completeness is missing/stale/conflicting |
| `PARTIAL` | Core artifacts are valid but an allowed evidence path is unavailable, hash-mismatched, or beyond declared budget |
| `NO SCOPE DELTA` | Complete identity coverage; exact baseline linkage; no `ADDED`, `REMOVED`, `MODIFIED`, `UNMAPPED`, or `CONFLICT` findings |
| `SCOPE DELTA FOUND` | Complete identity coverage and at least one evidence-backed `ADDED`, `REMOVED`, or `MODIFIED` finding |

`NO SCOPE DELTA` means only “these two immutable artifacts have the same approved
scope semantics.” It is not `PASS`, schedule approval, quality approval, or permission
to proceed. `SCOPE DELTA FOUND` is descriptive; it does not declare “creep” or choose a
remedy. Any `UNMAPPED` or `CONFLICT` forces `INSUFFICIENT EVIDENCE`.

## Phase 0: Validate invocation without mutation

1. Parse the exact command and reject unknown flags or repeated inputs.
2. Canonicalize paths and require them to remain inside the repository.
3. Reject identical baseline/current paths and symbolic/path aliases that resolve to
   the same artifact.
4. For `discover`, inspect only canonical active-state pointers and list their exact
   candidate paths/hashes. Return `INPUT REQUIRED`; do not select or analyze.
5. Confirm no output path, write, Git mutation, agent delegation, or gate is requested.

## Phase 1: Load and freeze the comparison pair

Read each input completely within the declared two-artifact budget. Record canonical
path, byte length and SHA-256 before parsing. Validate both contracts, baseline
approval/version/hash, current-to-baseline link, parent identity, and uniqueness of
all Scope IDs.

If the current artifact cites a different baseline hash/version than the supplied
baseline, return `INSUFFICIENT EVIDENCE — BASELINE MISMATCH`. Never substitute a
newer or similarly named plan.

## Phase 2: Compute stable-ID deltas

Normalize only schema-declared semantic fields; preserve source bytes and record the
normalization rules. Build the ID set-difference and entry hashes. Emit one canonical
finding per Scope ID in stable sort order.

Do not scan code, Git, TODOs, design files, or neighboring plans. Do not count rows as
effort. Do not infer who requested or justified a change.

## Phase 3: Attach bounded evidence

If `--evidence` is supplied, validate its own hash/bindings and enforce its allowlist
and budgets. A change is `APPROVED_CHANGE` only when a matching record binds the
Scope ID, baseline/current hashes, decision, owner, and timestamp. A commit author or
implementer is not a decision owner.

Attach compatible estimate, capacity, dependency, and test receipts. Mark every
missing, stale, mismatched, or incompatible field explicitly. Evidence never changes
the delta type; it changes coverage and impact support only.

## Phase 4: Derive the result and neutral options

Re-read and re-hash every consumed artifact. If any hash changed, return
`INSUFFICIENT EVIDENCE — INPUT CHANGED DURING CHECK`.

Derive one result from the table above. When a scope delta exists, show two or three
neutral product options without choosing one:

1. keep the approved baseline and remove/revert the proposed current delta;
2. retain the delta and request compatible estimate/capacity evidence plus an explicit
   product decision;
3. move identified Scope IDs to a separately approved future scope, if applicable.

For each option list affected Scope IDs, known impacts, unknown evidence, owner, and
the independent workflow/action that would be required. Use `Decision Required`; do
not write “recommended”, rank the options, or start another workflow.

## Phase 5: Report and stop

Output:

```markdown
# Scope Check

Result: <canonical result>
Operation: READ_ONLY

## Compared artifacts
| Role | ID/version | Path | SHA-256 | Approval/completeness |

## Coverage
| Dimension | Value | Evidence |

## Scope deltas
| Delta ID | Scope ID | Type | Decision state | Effort evidence | Risk evidence |

## Impact evidence
- Effort Delta: <value/range or UNVERIFIED>
- Schedule: <state and receipts>
- Quality: <state and receipts>
- Integration: <state and receipts>

## Decision options
<none when no delta; otherwise two or three unranked options>

## Unknowns and blocked conclusions
<explicit list>
```

End with the exact baseline/current paths and hashes so a later run can reproduce the
comparison. State that no file, Git state, decision, or baseline was changed.

## Failure and stale-evidence behavior

- Missing or ambiguous path: `ERROR`; show candidates only when exact active pointers
  named them, never from fuzzy search.
- Missing baseline approval/version/stable IDs/completeness: `INSUFFICIENT EVIDENCE`.
- Current manifest points to another baseline: `INSUFFICIENT EVIDENCE`.
- Unsupported file type/schema: `ERROR`.
- Missing supporting evidence: preserve valid deltas, return `PARTIAL`, and mark the
  affected impact conclusions `UNVERIFIED`.
- Changed bytes during execution: discard conclusions and return
  `INSUFFICIENT EVIDENCE — INPUT CHANGED DURING CHECK`.
- Existing decision record proposes re-baselining: report it; do not treat the
  baseline as changed until a separately approved immutable baseline exists.

## Final invariants

- No raw item-count or percentage verdict.
- No inferred baseline, change justification, owner, estimate, or risk rating.
- No automatic Cut/Keep/Defer choice.
- No mutation, delegation, gate, or follow-on workflow execution.
- Missing evidence never becomes `NO SCOPE DELTA`.
- Re-running with identical immutable inputs produces identical deltas and result.
