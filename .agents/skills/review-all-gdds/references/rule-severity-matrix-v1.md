# Cross-GDD Review Ruleset v1

This file is normative for `$review-all-gdds`.

```yaml
ruleset_id: cgs.cross-gdd-rules/v1
shard_limits:
  max_system_gdds: 8
  max_typed_edges: 32
  max_exact_input_bytes: 196608
scenario_limits:
  max_selected: 5
```

Limits apply to the exact file bytes assigned to one worker, excluding the
small protocol prompt. Never split one GDD into independently judged fragments.
If one required GDD exceeds `max_exact_input_bytes`, record that document and
its checks as unchecked and return `PARTIAL`. Limits may be lowered before a
run when the available context is smaller, but never raised ad hoc. Record the
effective values in the report.

## Finding record and identity

Every finding uses this machine representation:

```yaml
id: XGDD-<rule-slug>-<first-12-fingerprint-hex>
fingerprint_sha256: <lowercase SHA-256>
rule_id: <ID from this file>
evidence_class: DETERMINISTIC | HYPOTHESIS | COVERAGE
severity: BLOCKER | WARNING | ADVISORY | INFO | COVERAGE_GAP
disposition: OPEN | ADVISORY | RESOLVED_IN_INPUT
summary: <bounded factual summary>
targets:
  - system_id: <stable system ID or null>
    path: <canonical repository-relative path>
    sha256: <exact evidence hash>
    section: <heading or line location>
producer_finding_ids: []
assumptions: []
counterexamples: []
validation_plan: <required for hypotheses, otherwise null>
accepted_risk_record_ids: []
```

The fingerprint is SHA-256 over canonical JSON containing `rule_id`, sorted
normalized target system IDs, and sorted evidence tuples of path, hash, and
section. Wording, worker identity, run date, and severity are excluded. A
reworded finding therefore retains identity; different evidence bytes do not.

`OPEN` means the current input still demonstrates a deterministic issue.
`ADVISORY` is used only for hypotheses or information that cannot block.
`RESOLVED_IN_INPUT` may be retained from a prior/imported record only when its
acceptance condition is demonstrably satisfied by current hashed input. Risk
acceptance is never a finding disposition and never changes severity or
verdict; verified records are referenced separately.

## Deterministic proof boundary

A deterministic blocker requires all of the following unless a rule below is
more restrictive:

1. all cited product artifacts are `APPROVED_CURRENT` and their exact hashes are
   in this run's manifest;
2. subject identity, applicability, scope, and units are unambiguous;
3. the cited statements are normative, not examples, history, or speculation;
4. the statements cannot both be true under the same conditions and no scoped
   exception resolves them; and
5. the violation is reproducible from the cited bytes without choosing product
   intent.

If required identity, scope, unit, input, or evidence is unknown, use
`COVERAGE_GAP` and force `PARTIAL`; do not convert uncertainty into a blocker.
If the evidence is complete but a product decision is needed and the rules do
not prove mutual exclusion, use `WARNING`.

## Rule-to-severity matrix

| Rule ID | Trigger | Severity and disposition |
|---|---|---|
| `RAG.CONSISTENCY.RULE_CONTRADICTION` | Two current normative rules govern the same subject, scope, and conditions and are mutually exclusive | `BLOCKER / OPEN` when every deterministic proof condition holds; otherwise `COVERAGE_GAP` for missing evidence or `WARNING` for a complete but non-exclusive decision conflict |
| `RAG.CONSISTENCY.ACCEPTANCE_CONTRADICTION` | Two current acceptance criteria cannot both pass for the same scenario | `BLOCKER / OPEN` under the deterministic proof boundary |
| `RAG.CONSISTENCY.OWNERSHIP_CONFLICT` | Two current artifacts each claim exclusive ownership of the same product value or transition | `BLOCKER / OPEN` only when both claims are explicit and exclusive; overlapping or unclear responsibility is `WARNING / OPEN` |
| `RAG.CONSISTENCY.DEPENDENCY_TARGET_MISSING` | An authoritative outgoing dependency points to no current or explicitly planned stable system ID | `WARNING / OPEN`; it is not a blocker without an approved invariant that requires the target now |
| `RAG.CONSISTENCY.DEPENDENCY_DECLARATION_MISMATCH` | A GDD's outgoing dependency declaration disagrees with its systems-index edge | `WARNING / OPEN`; never require a reverse handwritten declaration |
| `RAG.CONSISTENCY.STALE_REFERENCE` | A current document names a removed, renamed, or superseded target and no explicit replacement resolves it | `WARNING / OPEN` |
| `RAG.CONSISTENCY.FORMULA_INTERFACE_INCOMPATIBLE` | A typed upstream output and downstream input have compatible units but provably disjoint allowed domains, or their composition violates an approved threshold | `BLOCKER / OPEN` only for a reproducible approved invariant or acceptance failure; otherwise `WARNING / OPEN` plus `NEEDS_MEASUREMENT` |
| `RAG.CONSISTENCY.VALUE_OR_FORMULA_MISMATCH` | Imported consistency evidence shows overlapping values or formulas differ but cannot prove the stronger rules above | `WARNING / OPEN`; ambiguous units or scope are `COVERAGE_GAP` |
| `RAG.CONSISTENCY.MISSING_CLAIM` | A required current claim or declared target has no supporting definition | `WARNING / OPEN` when coverage is complete; otherwise `COVERAGE_GAP` |
| `RAG.INVARIANT.EXPLICIT_VIOLATION` | Current evidence reproducibly violates an explicit approved pillar, anti-pillar, invariant, or quantitative threshold | `BLOCKER / OPEN`; quote the invariant and conflicting rule, and prove both are current and co-applicable |
| `RAG.SCENARIO.EXPLICIT_CONTRADICTION` | A sampled scenario reaches two mutually exclusive current transition/order/output rules | `BLOCKER / OPEN` in `full` or `since-last-review` only, under the deterministic proof boundary |
| `RAG.SCENARIO.UNDEFINED_COMBINED_STATE` | A sampled multi-system state lacks a declared activation order, handoff, unit, range, or combined-state resolution | `WARNING / OPEN`, never automatically a blocker |
| `RAG.THEORY.PROGRESSION_COMPETITION` | Multiple loops may compete for the same progression role | `ADVISORY / ADVISORY` |
| `RAG.THEORY.ATTENTION_LOAD` | Concurrent decisions may exceed the intended audience's attention budget | `ADVISORY / ADVISORY` |
| `RAG.THEORY.POTENTIAL_DOMINANT_STRATEGY` | An option may dominate under stated assumptions | `ADVISORY / ADVISORY` |
| `RAG.THEORY.ECONOMY_RISK` | Source/sink structure may create surplus, scarcity, or feedback risk | `ADVISORY / ADVISORY` |
| `RAG.THEORY.DIFFICULTY_CURVE_RISK` | Scaling curves may diverge under stated assumptions | `ADVISORY / ADVISORY` |
| `RAG.THEORY.PILLAR_OR_FANTASY_RISK` | Alignment or fantasy coherence is interpretive and not an explicit invariant violation | `ADVISORY / ADVISORY` |
| `RAG.COVERAGE.INPUT_INELIGIBLE` | A required GDD lacks exact-hash independent approval | `COVERAGE_GAP`; force `PARTIAL` |
| `RAG.COVERAGE.CONSISTENCY_EVIDENCE` | Required consistency evidence is absent, stale, malformed, partial, or scope-incomplete | `COVERAGE_GAP`; force `PARTIAL` |
| `RAG.COVERAGE.WORKER_OR_SHARD` | A planned worker/check/shard errors, exceeds budget, mismatches hashes, or remains unchecked | `COVERAGE_GAP`; force `PARTIAL` |
| `RAG.COVERAGE.EVIDENCE_CONFLICT` | Results with the same fingerprint disagree on facts, severity, disposition, or evidence hashes | `COVERAGE_GAP`; retain both provenances and force `PARTIAL` |

Imported consistency categories map as follows before the stronger proof rules
are evaluated:

| Producer category | Default review rule |
|---|---|
| `VALUE_MISMATCH`, `FORMULA_MISMATCH` | `RAG.CONSISTENCY.VALUE_OR_FORMULA_MISMATCH` |
| `COMPETING_OWNERSHIP` | `RAG.CONSISTENCY.OWNERSHIP_CONFLICT` |
| `DEPENDENCY_GAP` | `RAG.CONSISTENCY.DEPENDENCY_TARGET_MISSING` |
| `STALE_REFERENCE` | `RAG.CONSISTENCY.STALE_REFERENCE` |
| `MISSING_CLAIM` | `RAG.CONSISTENCY.MISSING_CLAIM` |

The producer's `HIGH`, `MEDIUM`, or `LOW` label is provenance, not this
workflow's severity. Escalation to a blocker requires the objective proof in
this matrix.

## Scenario candidate generation and risk score

Generate the complete candidate ledger before selection:

1. one candidate per explicitly declared multi-system event or state trigger;
2. one candidate per typed dependency/event path containing three or four
   systems; and
3. one candidate per resource or ownership handoff that crosses a system
   boundary.

Deduplicate by normalized trigger, ordered system IDs, and edge types. Candidate
ID is `SCN-` plus the first 12 hex characters of that canonical fingerprint.
Score each candidate additively:

- `+5` touches an explicit approved invariant or acceptance criterion;
- `+4` includes an undefined activation order or combined-state rule;
- `+4` includes irreversible state, death, save, load, or persistence;
- `+3` includes a resource or ownership handoff;
- `+3` has fan-out to at least three downstream systems;
- `+2` crosses a formula edge with units or ranges; and
- `+1` per system beyond two, capped at `+3`.

Sort by score descending, then candidate ID ascending. Select the first five or
all candidates when fewer exist. A tie never expands the limit; the stable ID
breaks it. Report total, selected, and unselected candidates with scores and
reasons. Normal unselected candidates are declared sampling scope, not missing
coverage. Failure to generate or score the complete candidate ledger is a
coverage gap and forces `PARTIAL`.

In `design-theory` mode, scenario observations may use only `ADVISORY` or
`INFO`. Do not run deterministic consistency classification in that mode. In
`full` and `since-last-review`, the deterministic scenario rules are available.

## Verdict precedence

Apply exactly this order after all required-mode coverage is merged:

1. invalid invocation or no meaningful two-GDD scope: `ERROR`, no run verdict;
2. any required `COVERAGE_GAP`, provisional input, unchecked scope, or evidence
   conflict: `PARTIAL`;
3. complete coverage with one or more `BLOCKER / OPEN` findings: `FAIL`;
4. complete coverage with no blockers and one or more `WARNING`, `ADVISORY`, or
   open validation items: `CONCERNS`;
5. complete coverage with none of the above: `PASS`.

Never let a warning produce `FAIL`, an advisory item produce `FAIL`, or a
blocking finding survive in `PASS`/`CONCERNS`. Preserve deterministic findings
inside a `PARTIAL` report without computing the lower-priority verdict.
