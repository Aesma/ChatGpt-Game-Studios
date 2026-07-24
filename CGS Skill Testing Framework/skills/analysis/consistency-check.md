# Skill Test Spec: `$consistency-check`

## Skill summary

`$consistency-check` contract `cgs.consistency-check/v2` is a strictly read-only,
hash-bound cross-GDD scanner. It locks the complete system-GDD manifest, builds
typed claim/owner/dependency indexes once, compares only semantically compatible
claims, emits stable findings under `cgs.consistency-claims/v1`, and returns one
`cgs.consistency-report/v1` evidence envelope.

The registry is optional attributed input, never product authority. Missing,
empty, invalid, or unreadable registry data never stops direct-GDD scanning and
never permits `PASS`; it produces `PARTIAL`. The scanner never chooses product
truth or writes GDDs, the systems index, registry, logs, reports, evidence files,
lifecycle state, or session state.

Final verdicts are exactly `PASS | FINDINGS | PARTIAL | ERROR`. Dependency gaps
are finding categories. `PARTIAL` takes precedence over proven findings.

---

## Required runtime instrumentation

Behavioral tests run in an isolated disposable repository. The harness records:

1. recursive path/type/SHA-256 snapshots before and after invocation;
2. every attempted filesystem mutation;
3. every enumerated, hashed, semantically read, skipped, and failed file with
   exact byte count and read count;
4. Git command availability and exact read-only outputs used;
5. the locked manifest and every active limit/counter;
6. the normalized claim, owner, dependency, coverage, finding, and evidence data;
7. exact report bytes returned to the caller; and
8. every agent/skill invocation attempt.

Mutation guard passes only when snapshots are identical and the mutation-attempt
ledger is empty. Prose claims are not evidence. An unobservable assertion is
`UNTESTED`, never PASS. Do not update `catalog.yaml` results from static review or
an uninstrumented run.

---

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`
- [ ] Description says read-only, cross-GDD, and hash-bound; metadata remains an
  accurate read-only cross-GDD entry point
- [ ] Contract/ruleset IDs are `cgs.consistency-check/v2` and
  `cgs.consistency-claims/v1`
- [ ] Accepted grammar has one mode and requires one explicit baseline path only
  for `since-last-review`
- [ ] Workflow is zero-write and has no director, specialist, remediation, or
  chained-skill branch
- [ ] Verdict set and precedence are exactly ERROR, PARTIAL, FINDINGS, PASS
- [ ] Missing/empty registry explicitly performs direct scan and cannot PASS
- [ ] Complete exact-hash manifest and fixed file/byte/entry/claim limits exist
- [ ] Typed claim, owner-map, directed dependency, coverage, and finding schemas
  are explicit
- [ ] Semantic comparison requires stable identity, type, scope, normative status,
  and compatible units
- [ ] Stable finding fingerprint excludes wording, values, paths, hashes,
  severity, status, reviewer, and time
- [ ] Every actionable finding contains two-sided or declaration-plus-manifest
  evidence, owner, target hashes, status, and acceptance
- [ ] Git/baseline/read/YAML/search/normalization/budget/hash failures have
  fail-closed PARTIAL or ERROR behavior
- [ ] Machine evidence uses generic `cgs.review-evidence/v1` plus extension
  `cgs.consistency-report/v1`
- [ ] Report is returned only; no ambiguous optional report path or write exists
- [ ] Consumer-compatible categories are exactly documented

---

## Case 1: Strict invocation and exact targeted identity

Run independently:

| Input | Expected |
|---|---|
| `$consistency-check` | valid full mode |
| `$consistency-check full` | valid full mode |
| `$consistency-check entity:sword` | valid exact entity mode |
| `$consistency-check item:iron-sword` | valid exact item mode |
| `$consistency-check since-last-review baseline:reviews/csc.md` | valid incremental grammar |
| `$consistency-check unknown` | invalid invocation ERROR |
| `$consistency-check full item:sword` | duplicate/multiple mode ERROR |
| `$consistency-check entity:` | empty ID ERROR |
| `$consistency-check entity:IronSword` | non-kebab ID ERROR |
| `$consistency-check since-last-review` | missing baseline ERROR |
| `$consistency-check full baseline:old.md` | forbidden baseline ERROR |
| `$consistency-check since-last-review baseline:a.md baseline:b.md` | duplicate baseline ERROR |
| `$consistency-check since-last-review baseline:../outside.md` | outside path ERROR |
| `$consistency-check since-last-review baseline:https://example.invalid/x` | URL ERROR |

For invalid rows, name the token and reason, show exact grammar, emit no
manifest-dependent verdict/evidence, and perform zero mutation. Targeted valid
modes still scan the complete corpus before exact stable-ID filtering; alias,
display-name, case-folded, substring, or fuzzy matches never satisfy the target.

---

## Case 2: Registry loss never creates false success

Fixture has four readable system GDDs with one direct formula conflict. Run with
missing, empty, malformed, unreadable, and valid non-empty registry variants.

- [ ] Every variant reads all four GDDs and preserves the direct conflict
- [ ] Missing/empty status differs from invalid/unreadable
- [ ] Registry `source` is provenance only
- [ ] First four variants return PARTIAL, never PASS or “nothing to check”
- [ ] Valid registry may permit FINDINGS when all other coverage is complete
- [ ] Registry is never repaired or rewritten
- [ ] Report lists exact registry path/hash or null, status, and indexed count

A no-conflict missing-registry variant still returns PARTIAL after completing the
direct scan.

---

## Case 3: Typed claims reject nearby-number and identity heuristics

Fixture contains two stable item IDs with the same display name, a normative
value, worked example, historical value, rejected alternative, case aliases, one
alias resolving to multiple IDs, and a reference with no value claim.

- [ ] Only explicit normative rule/schema/formula/ownership/dependency/AC content
  becomes a claim
- [ ] Display names never merge different stable IDs
- [ ] Example, history, rejected alternative, commentary, and estimate numbers
  are not normative claims
- [ ] Case-insensitive/fuzzy alias matching is forbidden
- [ ] Zero/multiple alias resolution becomes UNVERIFIABLE_IDENTITY
- [ ] Material identity ambiguity forces PARTIAL; incidental ambiguity is advisory
- [ ] Ordinary reference is not itself a conflict
- [ ] Each GDD is semantically read once, not once per registry entry

---

## Case 4: Unit and formula semantic comparison

Run: `1000 ms`/`1 s`, `100 cm`/`1 m`, `100 percent`/`1 ratio`, same
amount with different currency IDs, display-identical formulas with different
symbol units, formatting-different equivalent trees, coefficient/clamp/rounding
differences, and missing symbol semantics.

- [ ] Closed-table conversions use exact rational arithmetic and do not conflict
- [ ] Different resource IDs are not converted or merged
- [ ] Formatting differences do not conflict when typed trees are equal
- [ ] Coefficient/operator/cap/rounding/domain differences produce two-sided
  FORMULA_MISMATCH
- [ ] Missing rule-critical semantics is COVERAGE_GAP/PARTIAL, not guessed
- [ ] Non-listed dimensions never receive inferred conversion
- [ ] Raw/normalized/unit/scope/tree/evidence hashes are reported

---

## Case 5: Ownership and directed dependencies

Fixture includes stable IDs, exact Design Doc paths, outgoing `Depends On IDs`,
planned rows, display collisions, a missing target, claimed missing Design Doc,
exclusive/non-exclusive owners, and outgoing GDD dependencies.

- [ ] Two exclusive owners for the same stable subject/attribute produce
  COMPETING_OWNERSHIP with both sides
- [ ] Non-exclusive collaborators do not conflict
- [ ] Missing/vague owner stays UNVERIFIABLE_OWNER
- [ ] Index edge `A -> B` means A depends on B
- [ ] Reverse dependents are derived; B need not handwrite A
- [ ] Each dependency is exactly exists, planned-not-authored, missing-target,
  broken-reference, or declaration-mismatch
- [ ] Planned-not-authored is non-actionable by itself
- [ ] Missing/broken/mismatch creates DEPENDENCY_GAP with subtype and complete
  declaration-plus-graph evidence
- [ ] Removed/renamed unresolved target creates STALE_REFERENCE
- [ ] Duplicate ID/path mappings force PARTIAL instead of guessed identity

---

## Case 6: Immutable incremental baseline

Create a valid persisted baseline with record ID, project/ruleset, source commit,
complete path/hash manifest, run ID, and stable findings. Change one value, rename
one GDD under the same system ID, add/remove GDDs, and leave one unchanged.

- [ ] Baseline is selected only from the explicit path
- [ ] Record/producer/schema/project/ruleset/manifest/findings are validated
- [ ] Mtime, creation date, filename recency, Git rename heuristic, and “latest”
  search are never used
- [ ] Added/removed/renamed/changed/unchanged use stable IDs and exact hashes
- [ ] Dirty/untracked inputs participate by exact bytes
- [ ] Complete current-corpus coverage remains in evidence
- [ ] Prior IDs are re-evaluated and preserved
- [ ] New findings require at least one changed claim side/target

Invalid, stale, ambiguous, or scope-incomplete baselines return
`ERROR — INVALID CONSISTENCY BASELINE`. Git unavailable after a valid manifest
permits useful hash comparison but forces PARTIAL.

---

## Case 7: Fixed manifest and semantic budgets

Independently exceed 256 manifest candidates, 32 analyzed GDDs, 196608 bytes for
one GDD, 1048576 total semantic bytes, 2048 registry entries, and 4096 claims.

- [ ] Complete deterministically enumerable inventory is retained within cap
- [ ] Each candidate has stable ID/null, path, hash/bytes, status, and reason
- [ ] Selection follows stable system ID then path
- [ ] Oversized GDD is never split into independently judged fragments
- [ ] Unchecked paths/checks are explicit
- [ ] No limit is raised and no sample is called complete
- [ ] Every overflow returns PARTIAL and preserves completed findings
- [ ] Artifacts cover the complete enumerable current review set

Mid-run add/remove/rename/content change returns
`ERROR — INPUT CHANGED DURING SCAN`, never mixed-byte evidence.

---

## Case 8: Stable finding identity and resolution

First run produces value, formula, ownership, and dependency findings. Persist a
baseline externally; edit values/wording/line positions, rename a path under the
same system ID, resolve two, and add one different logical conflict.

- [ ] ID format is `CSC-<category-slug>-<12 fingerprint hex>`
- [ ] Fingerprint uses category/subcategory, stable subject/attribute,
  source-system IDs, and stable claim IDs
- [ ] Value, wording, path, hash, severity, status, reviewer, and time do not
  change the same logical ID
- [ ] Different logical claim gets a different ID
- [ ] Duplicate fingerprint merges provenance; incompatible identity/evidence
  forces PARTIAL
- [ ] RESOLVED_IN_CURRENT requires current exact-hash acceptance evidence
- [ ] Findings contain sides, owners, target hashes, status, acceptance,
  resolution, first/last run IDs, and producer claim IDs
- [ ] Sort order is deterministic

---

## Case 9: Failure and PARTIAL precedence

Simulate Git unavailable, index missing/malformed, one/all unreadable GDDs,
registry parse failure, semantic index failure, material unnormalizable
identity/unit/formula, fingerprint evidence conflict, record construction failure,
and one HIGH finding plus one coverage failure.

- [ ] Each input/check has explicit status and per-check state
- [ ] Git/index/one-file/registry/normalization/evidence failures return PARTIAL
- [ ] Proven findings remain under PARTIAL
- [ ] PARTIAL takes precedence over FINDINGS
- [ ] All GDDs unreadable returns ERROR
- [ ] Record construction failure returns ERROR, not inconsistent evidence
- [ ] No failure widens scope or limits
- [ ] PASS is impossible with any material gap

---

## Case 10: Hash-bound review-all consumer interface

Run a complete valid-registry scan, persist exact returned bytes with a separate
test recorder, and validate the producer contract without invoking the consumer.

- [ ] Machine block label/schema are `gate-evidence` and
  `cgs.review-evidence/v1`
- [ ] Producer is `consistency-check@cgs.consistency-check/v2`
- [ ] Extension/ruleset are `cgs.consistency-report/v1` and
  `cgs.consistency-claims/v1`
- [ ] Artifacts include every current GDD path/hash/system ID plus used support
- [ ] Extension includes run/project/revision, mode/target, manifest, stale key,
  skill hash, limits, baseline, registry, index digests, coverage, findings, notes
- [ ] Canonical JSON sort rules reproduce record ID
- [ ] Human projection and machine block agree
- [ ] Any changed GDD path/hash makes the report stale
- [ ] review-all can verify current set, coverage, IDs/evidence, and verdict
  without loading registry

---

## Case 11: Mutation, truth boundary, and report-only closing

Fixture includes GDDs, index, registry, existing failure log/reports/session state,
and competing claims with no current exact-hash decision evidence.

- [ ] Before/after recursive snapshots are identical
- [ ] Mutation-attempt ledger is empty
- [ ] No source/index/registry/log/report/evidence/lifecycle/session file changes
- [ ] No review mode read, agent/director spawn, or skill execution
- [ ] Provenance/filename/status/recency/order/severity/majority never chooses truth
- [ ] Conflicts use DECISION_REQUIRED and name owner/user decision
- [ ] RESOLVED_IN_CURRENT needs approved exact-hash decision evidence
- [ ] Scanner returns bytes only and never proposes a save path
- [ ] One verdict handoff is returned, then stop

---

## Authoritative P1 closure matrix

| Audit ID | Static clause | Behavioral evidence |
|---|---|---|
| CSC-004 | Registry absence cannot produce PASS | Case 2 assertions |
| CSC-005 | Typed semantic comparison replaces nearby-number heuristics | Cases 3 and 4 assertions |
| CSC-006 | Owner map and directed dependency checks | Case 5 assertions |
| CSC-007 | Immutable exact-hash incremental baseline | Case 6 assertions |
| CSC-008 | Fixed manifest and explicit semantic budgets | Case 7 assertions |
| CSC-009 | Stable finding identity and resolution | Case 8 assertions |
| CSC-010 | Failure, PARTIAL, and verdict precedence | Case 9 assertions |
| CSC-011 | Canonical conversation-only report and zero writes | Case 11 assertions |

## Protocol compliance

- [ ] Registry absence cannot create false success
- [ ] Complete corpus is manifested before comparison
- [ ] Only typed, stable-ID, normative, scope/unit-compatible claims are compared
- [ ] Owner and directed dependency checks are implemented
- [ ] Incremental baseline is explicit, immutable, hash-bound, reproducible
- [ ] Limits and unchecked scope are visible
- [ ] Stable findings contain dual evidence, owner, hashes, status, acceptance,
  and resolution evidence
- [ ] Material failure/uncertainty is PARTIAL and blocks PASS
- [ ] Verdict precedence is ERROR > PARTIAL > FINDINGS > PASS
- [ ] Report is canonical hash-bound `cgs.consistency-report/v1`
- [ ] Scanner chooses no product truth and performs zero writes
- [ ] SKILL, metadata, and spec describe one contract

## Coverage notes and catalog rule

Design theory, scenario sampling, per-GDD approval, authoring, registry repair,
remediation, report persistence, lifecycle transition, and gate policy are out of
scope. `review-all-gdds` consumes exact evidence but owns its own ruleset/verdict.

Do not fill catalog `last_static`, `last_spec`, or `last_category` until
instrumented tests run. Record FAIL or UNTESTED when mutation attempts, read
counts, hashes, typed indexes, Git failure, limits, or report bytes are unobserved.
