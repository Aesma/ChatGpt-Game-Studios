---
name: code-review
description: Performs a strictly read-only, revision-bound review of explicit project source targets against their complete applicable rule chain, Accepted ADR evidence, deterministic analysis receipts, and bounded specialist coverage.
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Code Review

Review exact project source targets without modifying them. Build a bounded,
revision-bound manifest; load the complete rule chain for every target; distinguish
verified analysis from judgment; and return stable findings in a generic review
evidence envelope. This workflow neither fixes code nor completes a story.

## Invocation

Use this grammar exactly:

```text
$code-review --target <project-relative-file-or-directory>
             [--target <project-relative-file-or-directory> ...]
             [--story <project-relative-story.md>]
```

- `--target` is required and may appear at most eight times.
- `--story` is optional and may appear exactly once.
- Paths must be literal, project-relative paths. Reject absolute paths, empty
  values, wildcards/globs, duplicate canonical paths, unresolved traversal,
  symlink/junction escape, and paths outside the project root.
- A direct file must be an eligible textual source artifact. A directory is
  resolved recursively through the bounded manifest procedure.
- The story must be a readable project story with stable identity. It is context,
  not a hidden target and not permission to edit or complete the story.

No arguments, positional paths, unknown options, duplicate `--story`, invalid
types, and a target set that resolves to no eligible source are input `ERROR`s.
Return usage, the exact rejected input, and remediation; emit no quality verdict.

## Read-only boundary

The allowed write set is empty. Do not edit source, tests, rules, ADRs, stories,
metadata, reports, registries, status, logs, or session state. Do not install
tools, generate projects, compile, build, run tests, profile, or execute a command
that can create caches or outputs. A parser, linter, or graph analyzer may run
only when its configured invocation is proven read-only and its exact receipt is
captured. Otherwise consume an existing current receipt or mark the check
`UNVERIFIED`.

Take the before/after streaming mutation snapshots defined in the continued
workflow. Any changed or incompletely covered in-scope project state forces
`PARTIAL`; report it but never repair or revert it.

## Contract sources

Read [review-rules-v1.md](references/review-rules-v1.md) completely. It defines
the bounded manifest, rule/evidence states, severity mapping, ADR admission,
engine-specialist routing, reviewer limits, stable findings, verdict precedence,
and output schemas.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. Missing, unreadable, or inconsistent contract files
are an `ERROR` with no quality verdict.

## Build the exact target manifest

Canonicalize every target under the repository root. For directories, enumerate
eligible regular source files deterministically without following links outside
root. Apply exclusions only when Git internals or current owner-approved project
rules/markers classify content as generated, vendored, cached, or build output.
Do not exclude a path merely because its directory name resembles `vendor` or
`generated`.

For every candidate record normalized path, type classification, size, complete
revision, origin target, eligibility, and exclusion reason. Sort by normalized
path and revision the complete manifest. The fixed bounds are in the rules reference.
Every eligible file beyond a limit remains visible as `UNCHECKED`; an unreadable
or unchecked eligible file makes coverage `PARTIAL`. A direct ineligible file is
an input error rather than a silent exclusion.

re-read every target immediately before evidence rendering. If bytes no longer
match the reviewed revision, mark `TARGET_CHANGED_DURING_REVIEW` and return
`PARTIAL`.

## Load the complete rule chain

For each target, discover `AGENTS.md` from repository root through every target
parent. Read the entire chain and record each declared revision in root-to-leaf order; the closest
applicable file wins only where the project guidance explicitly grants that
precedence. Follow directly linked standards when their subject applies, including
coding standards and configured technical preferences. Record every source path,
revision, scope, precedence, stable rule ID, normative wording, and severity.

Do not use one target's nested rules for another target. Do not replace the chain
with remembered repository conventions. If an applicable rule source cannot be
read, precedence is ambiguous, or two authorities conflict without an explicit
override, record a rule coverage gap and return `PARTIAL`.

Checks come from current rule sources, Accepted ADRs, and the optional story's
explicit requirements. Do not impose universal thresholds such as complexity
`< 10`, method length `40`, mandatory interfaces, dependency injection, or SOLID
labels unless an applicable exact source states them. A language/engine-specific
rule is `N/A` only with exact applicability evidence. Unsupported N/A is
`UNVERIFIED`.

## Bind ADR evidence explicitly

Build the ADR candidate set only from explicit stable ADR IDs and paths in:

1. the exact `--story` artifact;
2. target source metadata/header references; and
3. an owner-approved bounded implementation manifest referenced by those inputs.

Commit messages may be recorded as non-authoritative discovery clues, but never
create an ADR binding, establish scope, or prove compliance. Do not search old
commits to choose among renamed, stale, duplicate, or multiple ADRs.

Resolve every explicit ADR ID to one exact current path and revision. Read status,
Decision, and Consequences. Only `Accepted` ADRs provide compliance rules. A
readable non-Accepted ADR is `ADR_NOT_EVALUATED` and may produce a source-bound
`WARNING`; it is never compliance evidence. A missing, unreadable, ambiguous,
stale, statusless, or structurally incomplete explicit ADR is a coverage gap and
forces `PARTIAL`. When current project rules require an ADR but no explicit ID is
available, record `ADR_NOT_EVALUATED`; never infer `COMPLIANT`.

## Evaluate with reproducible evidence

Create a rule ledger before checking code. Each applicable check has exactly one
state:

```text
VERIFIED_PASS | VERIFIED_FAIL | NOT_APPLICABLE | UNVERIFIED
```

`VERIFIED_PASS` and `VERIFIED_FAIL` require the evidence method mandated by the
rule. Direct source evidence can prove syntactic/local facts. Cyclomatic
complexity requires a compatible AST/linter receipt; dependency cycles require a
current build/module graph; hot-path allocation and runtime performance require
compatible analyzer/profiler evidence. Natural-language inspection alone cannot
verify those properties.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## Route bounded reviewers

Mechanical rule, revision, parser, graph, and receipt checks remain local. Build one
deduplicated reviewer plan from exact project configuration and target types:

- `lead-programmer` owns the integrated code-quality/architecture review;
- configured engine language, shader, UI, native/plugin, or primary specialists
  apply only through the current `Engine Specialists` and extension-routing
  configuration;
- `qa-tester` applies only when the explicit story schema makes testability or
  manual-verification reachability part of this review.

Do not invent an engine or specialist from a filename. If the engine is configured
but a needed routing row is empty, use the configured Primary only when the
project routing contract explicitly permits that fallback. Otherwise record
`ROUTING_UNCONFIGURED`.

Deduplicate roles before dispatch. At most three reviewers total may run in one
parallel batch, including the lead. Reviewer selection and overflow use the
deterministic table in the rules reference. Each receives the same manifest revision,
only its assigned target revisions/rules, a read-only boundary, and no verdict
authority. A required reviewer not dispatched because of the cap, or returning
unavailable/declined/blocked/timeout/error/malformed/target-mismatched evidence,
forces `PARTIAL`. Reviewer silence is never clean evidence.

If the lead role is unavailable, the current agent may perform that exact role
locally and record `DONE_LOCAL_FALLBACK`; no engine or QA role may be silently
substituted. Normalize every usable reviewer observation against a current rule
ID and target revision. Unsupported advice is `INFO`, not a blocking rule.

## Normalize stable findings

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

The stable key excludes target byte revisions, line numbers, wording, timestamps,
and reviewer identity, so an unchanged defect retains its ID across revisions.
revisions remain in the evidence record for staleness. Security, performance, and
test-execution observations are routed to their owning domains as candidate
findings; code review does not duplicate their approval gates.

## Coverage and verdict

Coverage is `COMPLETE` only when:

- every eligible target in the bounded manifest was read, versioned, and reviewed;
- every applicable rule source and precedence decision is current and resolved;
- every required rule check is verified pass/fail or evidence-backed N/A;
- required ADR scope is explicit and every explicit ADR was resolved/status
  checked, with every Accepted ADR evaluated;
- every required reviewer completed with usable target-bound evidence; and
- before/after mutation and final target-revision guards are complete and unchanged.

Apply this precedence exactly:

1. No valid manifest or invalid invocation -> `ERROR`, verdict null.
2. Any mandatory coverage gap -> `PARTIAL`.
3. Complete coverage plus any open `BLOCKING` finding -> `NEEDS CHANGES`.
4. Complete coverage, no blocking finding, and any open `WARNING` -> `CONCERNS`.
5. Complete coverage with only `INFO` findings or none -> `APPROVED`.

Accepted risk, user preference, or an incomplete reviewer never overrides this
table. `INFO` is advisory and does not block approval.

## Return and stop

Return one `cgs.review-evidence/v1` envelope with a `cgs.code-review/v2`
extension as defined in the rules reference. Include the complete target
manifest, exact target revisions, rule chains/ledger, ADR and tool evidence,
reviewer plan/results, coverage gaps, stable findings, mutation guard, verdict,
and stale key.

This skill never persists the record, so always state:

```text
gate_evidence_status: NOT_PERSISTED
gate_evidence_eligible: false
```

Deliver findings and stop. Do not invoke, recommend bypassing into, or represent
this review as `$story-done`. Story completion is an independent verification
that must evaluate its own current evidence. For `PARTIAL`, identify coverage to
restore; for `NEEDS CHANGES` or `CONCERNS`, list source-bound remediation; for
`APPROVED`, state only what this exact non-persisted code-review record proves.
