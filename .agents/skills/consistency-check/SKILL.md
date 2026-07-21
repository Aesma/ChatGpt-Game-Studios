---
name: consistency-check
description: "Read-only cross-GDD consistency audit that compares competing claims, ownership, formulas, and dependencies, with optional registry context, and returns PASS, FINDINGS, PARTIAL, or ERROR."
---

# Consistency Check

Audit cross-document design consistency without changing the project. Compare
claims in all in-scope GDDs directly. If `design/registry/entities.yaml` exists,
use it as an additional claim source and coverage aid, never as automatic proof
that one product value is correct.

## Invocation and contract

Invoke as `$consistency-check [full | since-last-review | entity:<id> | item:<id>]`.
No argument is equivalent to `full`.

This workflow is strictly read-only:

- It may enumerate, search, and read project files and inspect read-only Git
  history when a mode requires a baseline.
- It must not create, edit, append, rename, or delete any file.
- It must not update GDDs, the entity registry, consistency logs, reports, or
  session state.
- It must not run another skill, spawn a director gate, or silently delegate a
  remediation.
- Its only deliverable is the complete report returned to the caller.

If the caller later wants a finding resolved or persisted, that is a separate
owner-led task with its own explicit scope. Do not perform that work during this
scan.

Verdict contract: `PASS | FINDINGS | PARTIAL | ERROR`.

The final verdict is exactly one of:

- `PASS` — coverage is complete and there are no actionable consistency
  findings.
- `FINDINGS` — coverage is complete and one or more actionable conflicts or
  dependency gaps exist.
- `PARTIAL` — the scan produced useful results, but at least one material input
  or required check could not be completed. `PARTIAL` takes precedence over
  `FINDINGS`; preserve any findings already proven.
- `ERROR` — the scan cannot establish a meaningful audit scope or cannot inspect
  any in-scope GDD.

Dependency gaps are a finding category, not a separate verdict.

---

## Phase 1: Validate scope and inventory inputs

1. Parse the optional argument.
   - `full`: compare every system GDD.
   - `since-last-review`: compare the complete GDD corpus, but report only
     findings for which at least one side changed after the last review
     baseline.
   - `entity:<id>`: compare claims about one normalized entity identifier across
     the complete GDD corpus.
   - `item:<id>`: compare claims about one normalized item identifier across the
     complete GDD corpus.
2. Reject an empty identifier, more than one mode, or an unrecognized argument
   with `ERROR`. Show the accepted syntax and stop.
3. Enumerate `design/gdd/*.md`. Exclude generated cross-review reports and the
   non-system overview files `game-concept.md`, `systems-index.md`, and
   `game-pillars.md`.
4. If no system GDD exists, return `ERROR` with:
   `No system GDDs found in design/gdd/. Create or identify the GDDs to audit.`
5. Record every in-scope path before comparison. For the default and `full`
   modes, every discovered system GDD is in scope.
6. For `since-last-review`, locate the baseline using read-only Git history for
   the most recent `design/gdd/gdd-cross-review-*.md` artifact. If a reproducible
   baseline cannot be established, continue with a full scan, disclose the
   fallback, and force `PARTIAL`.
7. Attempt to read `design/registry/entities.yaml` when present.
   - Missing or empty registry: continue with direct GDD-to-GDD comparison and
     report registry coverage as unavailable. Never stop with “nothing to
     check,” and never infer consistency from registry absence.
   - Malformed or unreadable registry: continue with direct comparison, record
     the failed coverage channel, and force `PARTIAL`.
   - Valid registry: index its entries as attributed claims. A `source` field is
     provenance supplied by the registry, not authority and not user approval.

Report the selected mode, GDD inventory, exclusions, registry status, and any
baseline fallback before reporting findings.

---

## Phase 2: Build a direct claim index

Read each in-scope GDD in full once before issuing a verdict. A read failure for
one or more GDDs forces `PARTIAL`; failure to read every in-scope GDD is `ERROR`.

Index only claims supported by identifiable text. Each indexed claim records:

- subject identifier and aliases stated in the document;
- claim category: `VALUE`, `FORMULA`, `OWNERSHIP`, `DEPENDENCY`, or `REFERENCE`;
- attribute or relationship name;
- raw value or expression and a normalized representation when normalization is
  unambiguous;
- unit and scope or applicability conditions;
- evidence location: file, heading, line or line range, and a short excerpt;
- stated owner, decision reference, or change rationale when present.

Also index registry entries in the same neutral claim form when the registry is
available. Label them `registry claim`; do not relabel them as canonical values.

Do not turn nearby examples, historical values, prose speculation, or unrelated
numbers into product claims. If identity, unit, scope, or meaning is ambiguous,
record an advisory `UNVERIFIABLE` note instead of inventing a comparison. An
ordinary reference that makes no value claim is not itself a conflict.

For targeted `entity:` or `item:` modes, still inspect all system GDDs, then
filter the claim index to the requested normalized identifier. Zero matches are
a `FINDINGS` result with category `MISSING_CLAIM`, unless a material read or
normalization gap requires `PARTIAL`.

---

## Phase 3: Compare competing claims

Compare claims only when subject, attribute, unit, and applicability overlap.
Compare GDDs directly with one another; registry claims supplement that graph.

Create actionable findings for:

- `VALUE_MISMATCH`: comparable values differ.
- `FORMULA_MISMATCH`: formulas for the same output and applicability differ in
  variables, operators, coefficients, caps, or output range.
- `COMPETING_OWNERSHIP`: more than one document makes an exclusive ownership
  claim for the same entity, mechanic, or decision.
- `DEPENDENCY_GAP`: a required dependency names a system or artifact that does
  not exist in the audited corpus and is not explicitly marked planned.
- `STALE_REFERENCE`: a document points to a removed, renamed, or superseded
  artifact and the replacement cannot be resolved from explicit evidence.
- `MISSING_CLAIM`: a targeted identifier has no supported claim.

Assign severity from impact, not from which document supplied the claim:

- `HIGH`: mutually exclusive normative formulas, values, or ownership claims
  can change core behavior or block downstream architecture.
- `MEDIUM`: an unresolved required dependency, stale reference, or bounded value
  mismatch can invalidate a dependent system.
- `LOW`: the contradiction is real and actionable but isolated, optional, or
  unlikely to affect another system. Keep ambiguous evidence advisory instead
  of inflating it into a low-severity conflict.

Do not report a mismatch when values are equivalent after an unambiguous unit
conversion, when conditions are explicitly different, or when one passage is
clearly an example rather than a normative rule.

Every actionable finding must show at least two evidence sides when two claims
compete. A dependency or missing-claim finding instead shows the declaring
evidence plus the audited inventory that failed to resolve it. Never emit a bare
“conflict exists” statement.

### Product-truth boundary

The scanner reports claims; it does not select product truth.

- Never declare a registry claim correct merely because its entry has a
  `source` field.
- Never declare the named source GDD correct merely because the registry points
  to it.
- Never rewrite “GDD versus registry” as “stale registry” or “wrong GDD” without
  explicit, current decision evidence.
- Never choose a new number, formula, owner, or dependency for the user.
- When claims compete, use status `DECISION REQUIRED` and identify the artifact
  owner or user decision needed.
- If a current approved decision artifact explicitly selects a claim and the
  finding includes its evidence, the report may state which claims match that
  decision. It still must not modify any target.

Owner metadata and change rationale may guide the handoff, but neither is enough
to overwrite another claim without explicit decision evidence.

---

## Phase 4: Coverage and verdict

Build a coverage ledger with one row per discovered system GDD and one row for
the optional registry channel:

| Input | Status | Checks completed | Limitation |
|---|---|---|---|
| `path` | `READ / SKIPPED / FAILED` | values, formulas, ownership, dependencies | reason or `none` |

Material limitations include unreadable GDDs, malformed registry data when it
was present, an indeterminate incremental baseline, or a required comparison
that could not be normalized. A missing registry alone is not an error when the
complete GDD corpus was directly compared; disclose that registry-backed
coverage was unavailable.

Choose one verdict in this order:

1. `ERROR` if scope is invalid, no system GDD exists, or none can be read.
2. `PARTIAL` if any material coverage limitation remains.
3. `FINDINGS` if coverage is complete and at least one actionable finding exists.
4. `PASS` otherwise.

Do not issue `PASS` based only on a registry lookup, a subset of GDDs, or an
empty result from text search.

---

## Phase 5: Return the report and stop

Return the full report in the response using this structure:

```markdown
## Consistency Check Report
Date: [YYYY-MM-DD]
Mode: [mode]
GDDs discovered: [N]
GDDs read: [N]
Registry coverage: [available | missing | empty | invalid | unreadable]

### Coverage
[coverage ledger]

### Actionable findings
| # | Category | Severity | Subject | Claim A | Claim B / Missing target | Evidence | Status |
|---|---|---|---|---|---|---|---|
| 1 | FORMULA_MISMATCH | HIGH | damage | ... | ... | both file locations | DECISION REQUIRED |

If there are none: `No actionable consistency findings.`

### Advisory notes
[unverifiable or non-blocking observations, or `None.`]

### Decision handoff
[For each finding: owner/user decision needed and the exact competing claims.
Do not prescribe a winning product value without explicit decision evidence.]

Verdict: PASS | FINDINGS | PARTIAL | ERROR
```

The report is the output. Do not save it, append a log, update session state, or
offer an in-workflow write. End after one concise next-step handoff:

- `PASS`: the caller may proceed to the next already-planned review or
  architecture step.
- `FINDINGS`: the responsible artifact owner or user must choose among the shown
  claims in a separate remediation task.
- `PARTIAL`: restore the named coverage inputs, then rerun the audit.
- `ERROR`: correct the scope or create/identify auditable GDDs, then rerun.
