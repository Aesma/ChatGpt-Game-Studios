---
name: review-all-gdds
description: "Report-only, hash-bound holistic review of an approved system-GDD manifest. Uses bounded graph shards, imports current deterministic consistency evidence, records sampled design hypotheses, and returns PASS, CONCERNS, FAIL, or PARTIAL."
---

## Invocation and execution

Invoke this workflow as `$review-all-gdds`.

This workflow is report-only. Render the complete report in conversation by
default. If the user asks to persist it, present the exact, unique report path
as the complete proposed changeset and obtain explicit approval before that one
write. Never modify a GDD, `systems-index.md`, the entity registry, session
state, lifecycle status, sign-off, accepted-risk record, approval record, or an
existing review report. Remediation and lifecycle transitions belong to
separate owner-authorized workflows.

Accepted argument grammar:

```text
[full | consistency | design-theory | since-last-review]
[baseline:<repo-relative-report-path-or-run-id>]
[consistency-report:<repo-relative-report-path>]
```

No mode is equivalent to `full`. `baseline:` is required only for
`since-last-review` and is forbidden in other modes. `consistency-report:` is
the explicit evidence input for every mode that runs the consistency phase; if
it is omitted, the invocation remains valid but required evidence is missing
and the run must return `PARTIAL`. Arguments may appear in any order, but each
kind may appear at most once.

# Review All GDDs

This skill reviews relationships across the current system-GDD set. It does not
repeat a per-document `$design-review`, choose product truth, populate the
entity registry, or author fixes.

Run it after all MVP system GDDs have independent approval evidence for their
current hashes and before architecture begins. It may preserve useful findings
from provisional inputs, but provisional, stale, or incomplete input evidence
forces `PARTIAL` and can never authorize architecture.

## Frozen public contract

- **Run verdicts:** exactly `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`.
- **Invocation failure:** invalid arguments or fewer than two reviewable system
  GDDs return `ERROR` with no review verdict and no report write.
- **Report-only boundary:** conversation output is the default. The only
  permitted mutation is one new, explicitly authorized immutable report.
- **Evidence identity:** every report binds project identity, mode, source
  revision, canonical input paths, exact-byte SHA-256 hashes, ruleset version,
  run ID, planned shards, and coverage.
- **Staleness:** any added, removed, renamed, or changed artifact in the bound
  manifest, or a different ruleset version, invalidates the report's
  `stale_key`. A stale report is not gate evidence.
- **Incomplete work:** a provisional input, missing approval record, stale or
  missing consistency report, worker error, unchecked required shard, input
  budget overflow, hash mismatch, or unresolved merge conflict produces
  `PARTIAL`; it can never produce `PASS` or `FAIL`.
- **Blocking boundary:** design-theory observations are
  `HYPOTHESIS / ADVISORY`. Only a rule in the versioned severity matrix applied
  to reproducible current evidence can block.
- **Accepted risk:** `FAIL` is never relabeled. A separate owner-signed,
  hash-bound `ACCEPTED_RISK` record may be referenced, but the reviewer neither
  creates it nor changes the run verdict.
- **No hidden corpus:** every included and excluded system ID, supporting input,
  shard, check, and scenario candidate is represented in the report.

Before analysis, read
[`references/rule-severity-matrix-v1.md`](references/rule-severity-matrix-v1.md)
in full. Its ruleset ID, shard limits, risk scoring, finding schema, and verdict
precedence are normative for this workflow.

## Mode phase matrix

| Phase | `full` | `consistency` | `design-theory` | `since-last-review` |
|---|---|---|---|---|
| Validate approved current manifest | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| Validate/import consistency report | REQUIRED | REQUIRED | FORBIDDEN | REQUIRED |
| Bounded design-theory shards | REQUIRED | FORBIDDEN | REQUIRED | REQUIRED on impact closure |
| Risk-scored scenario sample | REQUIRED | FORBIDDEN | REQUIRED, advisory output only | REQUIRED on impact closure |
| Optional immutable report write | ALLOWED | ALLOWED | ALLOWED | ALLOWED |

`FORBIDDEN` phases must not read their phase-specific inputs, spawn workers, or
emit findings. Report them as `NOT_APPLICABLE`; that status is not incomplete
coverage. `since-last-review` uses the `full` phase set over a validated impact
closure. Unknown modes, multiple modes, duplicate argument kinds, a misplaced
`baseline:`, or extra text return `ERROR — INVALID INVOCATION`, show the exact
grammar, emit no verdict, and stop with zero mutations.

---

## Phase 1: Build the bounded current input manifest

### 1a. Resolve canonical system identity

Read `design/gdd/systems-index.md` first. Its `System ID` is persistent identity
and its `Depends On IDs` column is the single authoritative directed dependency
edge: `A depends on B` means `A -> B`. Reverse dependents are always derived by
graph traversal and are never required as handwritten declarations in B.

Build the review set from:

1. every MVP row, whether its document is present or missing; and
2. every non-MVP row whose lifecycle status is `Approved` and whose Design Doc
   resolves to a direct child `design/gdd/<slug>.md`.

Record every other row as an exclusion with its system ID and reason. Do not
discover additional authoritative systems from arbitrary Markdown files. If the
systems index is missing or malformed, inventory direct-child candidate GDDs as
`PROVISIONAL_DISCOVERY`, disclose that canonical scope is unavailable, and
force `PARTIAL` if at least two candidates can be reviewed.

Exclude `game-concept.md`, `game-pillars.md`, `systems-index.md`, templates,
review reports, generated logs, and files outside the direct `design/gdd/`
directory. A duplicate system ID, normalization collision, path shared by two
IDs, unresolved required MVP path, or dependency target absent from both the
current and explicitly planned system rows is a manifest finding or coverage
gap under the ruleset; never silently repair identity.

If fewer than two system GDD files are reviewable, return:

> `ERROR — Cross-GDD review requires at least two reviewable system GDDs.`

Emit no run verdict, spawn no workers, write nothing, and stop.

### 1b. Validate current approval evidence

For every review-set GDD, compute SHA-256 over its exact bytes and locate an
independent `design-review` evidence record using an explicit link when one is
present, otherwise an unambiguous project-local `cgs.review-evidence/v1` record
whose producer is `design-review` and whose artifact path and hash exactly
match. Validate the record hash before using it.

Record, per system:

- system ID, priority, declared lifecycle status, canonical path, and GDD hash;
- approval record path, record hash, producer verdict, and reviewed artifact
  hash; and
- eligibility: `APPROVED_CURRENT`, `PROVISIONAL`, `STALE`, `UNBOUND`, or
  `MISSING`.

Only an independent `APPROVED` verdict bound to the exact current GDD bytes is
`APPROVED_CURRENT`. Filename, status text, directory placement, conversation
memory, or a GDD's own sign-off is not approval evidence. Conflicting records
are `UNBOUND`. Analyze readable provisional documents only to preserve useful
evidence, mark their limitations, and force the overall verdict to `PARTIAL`.

### 1c. Build a compact typed graph before full reads

Hash supporting inputs actually used: game concept, pillars, systems index,
approval records, and the supplied consistency report. Do **not** read
`design/registry/entities.yaml` directly. Registry validation and comparison
belong to `$consistency-check`; this workflow consumes its bound result.

From the systems index and bounded extraction of each GDD's `Summary`,
`Dependencies`, `Cross-References`, `States and Transitions`, `Formulas`, and
`Acceptance Criteria` sections, build a compact typed graph:

- nodes: stable system IDs and declared events/resources/formulas/invariants;
- edges: authoritative dependency, data dependency, state trigger, rule
  dependency, ownership handoff, and formula input/output;
- edge evidence: path, section, exact hash, units/ranges when declared; and
- unresolved tokens: aliases, targets, units, or scopes that could not be
  normalized without guessing.

Only a GDD's outgoing dependency declaration may be compared with the systems
index. Never require the target GDD to restate the reverse relationship.
`DEPENDENCY_TARGET_MISSING` and `DEPENDENCY_DECLARATION_MISMATCH` use separate
rules from the matrix; neither is called “asymmetry.”

Hashing a file and extracting named sections does not authorize an unbounded
whole-corpus prompt. Full document reads happen only inside the bounded shards
that need them. If a required section cannot be extracted or a file cannot fit
the single-shard byte limit, record the exact unchecked document/check and
force `PARTIAL`.

### 1d. Resolve incremental scope

For `since-last-review`, require the explicit `baseline:` value. A path must
resolve to one immutable report inside the project. A run ID may be resolved
only when exactly one report embeds that ID; zero or multiple matches are not a
trustworthy baseline. Validate the baseline's schema, record ID, project ID,
ruleset ID, manifest digest, stable system IDs, and complete path/hash set. Do
not use report modification time, Git `name-only`, or filename recency.

Compare baseline and current manifests by stable system ID and classify:

- added or removed system;
- same ID with a renamed path;
- same ID/path with changed exact-byte hash; or
- unchanged.

Build the union of the baseline and current typed graphs. Seed the impact set
with every added, removed, renamed, or changed system, then traverse both
outgoing and derived incoming edges transitively until a fixed point. Removed
nodes remain baseline tombstones so their former dependents are not lost.
Untracked and dirty current inputs participate through their current exact-byte
hashes like every other input.

If concept, pillars, systems index, ruleset, graph identity, or consistency
evidence scope changed, the effect is global: set `effective_scope: full` and
review the complete current set. If the baseline is absent, malformed,
ambiguous, or cannot reproduce its graph, disclose why incremental scope is
unsafe and fall back to `full`, not a guessed subset.

### 1e. Bind run identity and planned coverage

Create an ordered manifest and record:

- project ID: canonical repository root plus repository identity;
- run ID: UTC timestamp plus the first 12 characters of the ordered manifest
  digest;
- requested mode and effective scope;
- source revision: commit ID or null plus `clean`, `dirty`, or
  `includes-untracked-inputs`;
- every system/supporting path, stable ID/role, exact SHA-256, approval state,
  and baseline delta;
- ruleset ID, exact ruleset SHA-256, skill-bundle SHA-256 over the ordered main
  file, continuation, and ruleset bytes, and all active limits; and
- every required check and planned shard ID.

The `manifest_sha256` is the SHA-256 of the canonical ordered manifest. The
`stale_key` is the SHA-256 of canonical JSON containing project ID, ruleset ID,
exact ruleset hash, requested mode, and the sorted complete path/hash artifact
set. Never use a timestamp as either digest.

---

## Phase 2: Import deterministic consistency evidence

Run this phase only where the mode matrix says `REQUIRED`.

In `full` and `since-last-review`, consistency-evidence validation and the first
independent theory-shard batch may run in parallel after the Phase 1 manifest is
locked. They consume disjoint slices, use the same run ID and hashes, and must
both finish before scenario selection or verdict computation. Parallelism never
changes the deterministic merge order.

Validate the explicitly supplied `consistency-report:` as
`cgs.consistency-report/v1`. It must contain a valid record ID, the same project
ID, exact current path/hash coverage for the complete review set, a coverage
ledger, stable finding IDs, evidence locations, and verdict
`PASS | FINDINGS | PARTIAL | ERROR`. Recompute all referenced current hashes.
Registry content, when used by the producer, is evidence owned and validated by
that report; do not separately load or reinterpret the registry here.

- Missing, malformed, `PARTIAL`, `ERROR`, hash-mismatched, or scope-incomplete
  consistency evidence is a required coverage gap and forces this run to
  `PARTIAL`.
- `PASS` imports no deterministic findings.
- `FINDINGS` imports each supported finding, maps its category through the
  versioned rule matrix, and preserves the producer finding ID as provenance.
- An imported severity label alone never proves a blocker. The matrix's
  objective preconditions must be present in the imported evidence; otherwise
  classify the item as a warning or coverage gap as specified there.

In incremental mode, the consistency report must still bind the complete
current review set. Report only imported findings with at least one target in
the impact closure, but retain full-report identity as provenance. This phase
never reruns registry comparison, fills the registry, selects a winning value,
or modifies the consistency report.

---

## Phase 3: Run bounded design-holism shards

Run this phase only where the mode matrix says `REQUIRED`.

### 3a. Plan deterministic shards

Use the compact typed graph to produce:

1. domain node shards, grouping related systems without exceeding any ruleset
   limit; and
2. cross-domain edge shards covering every typed edge whose endpoints do not
   occur together in a domain shard.

Sort systems by normalized domain then stable system ID, and edges by edge type,
source ID, target ID, then evidence path. Fill shards greedily in that order.
Every in-scope node and edge must map to at least one planned shard. No worker
receives the whole corpus unless the complete corpus itself fits one bounded
shard. Pass only the shard's paths, exact hashes, compact graph slice, applicable
checks, pillars/invariants needed by that slice, run ID, and ruleset excerpt.
Do not pass the entity registry, unrelated engine details, or an unbounded
conversation transcript.

If one GDD alone exceeds the byte limit, a required edge cannot be placed, or
available context cannot complete a planned shard, mark it unchecked and force
`PARTIAL`; do not silently widen the limit or claim corpus-wide coverage.

### 3b. Analyze theory as hypotheses

Within each shard, inspect progression-loop interaction, attention demands,
strategy trade-offs, economic sources/sinks, difficulty curves, pillar
alignment, and player-fantasy coherence. Full-read only the GDDs assigned to
that shard and verify their hashes before and after analysis.

Each theory item is `HYPOTHESIS / ADVISORY` and must contain exact evidence,
assumptions, a plausible counterexample or compensating mechanic, a validation
plan, and `NEEDS_MEASUREMENT` when measurement is absent. It cannot become a
blocker merely because a common heuristic was exceeded. An explicit approved
invariant violation uses the separate deterministic invariant rule and all of
its proof requirements.

### 3c. Require the standard worker result

Every delegated analysis returns exactly one result shaped as:

```yaml
schema: cgs.cross-gdd-worker/v1
run_id: <run ID>
worker_id: <stable worker ID>
phase: theory | scenario | evidence-validation
shard_id: <planned shard ID>
status: DONE | PARTIAL | ERROR
input_manifest:
  - path: <canonical path>
    sha256: <exact hash used>
checks:
  - check_id: <ruleset check ID>
    status: DONE | PARTIAL | ERROR | NOT_APPLICABLE
unchecked_scope: []
findings: []
```

Workers never emit the overall review verdict. Run independent shards in
parallel up to the available concurrency, then continue in deterministic
batches; do not omit a shard because all workers cannot start simultaneously.
The coordinator validates every echoed hash and accounts for the Cartesian set
of planned shard/check pairs.

### 3d. Merge deterministically

Normalize every finding using the ruleset. Its fingerprint is SHA-256 over
`rule_id + normalized targets + sorted evidence path/hash/section tuples`; its
stable ID derives from that fingerprint. Sort merged results by phase, rule ID,
severity rank, fingerprint, then source worker ID.

Deduplicate identical fingerprints while retaining every producer/worker
provenance. If the same fingerprint carries incompatible facts, severity,
disposition, or evidence hashes, do not choose one result: record an
`EVIDENCE_CONFLICT`, list both results as unresolved, and force `PARTIAL`.
Missing workers, mismatched hashes, missing planned checks, or non-empty
unchecked required scope also force `PARTIAL` while preserving completed
evidence.

---

## Required continuation

Before continuing, read
[`references/continued-workflow.md`](references/continued-workflow.md) in full.
It defines risk-scored scenario sampling, machine-consumable report output,
verdict computation, optional persistence, and the final handoff. Execute those
phases in order under the frozen contract and mode matrix above.
