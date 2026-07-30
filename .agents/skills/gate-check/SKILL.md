---
name: gate-check
description: "Validate one catalog-authorized adjacent phase transition with a bounded, revision-bound, read-only assessment. Produces PASS, CONCERNS, FAIL, or PARTIAL without changing project stage."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Phase Gate Validation

## Invocation and immutable boundary

Invoke this workflow as `$gate-check`.

```text
$gate-check [transition-id] [--review full|lean|solo]
            [--authority-record <repository-relative-path>]
            [--evidence <repository-relative-path-or-record-id>]...
```

The transition ID is optional only for selection from a validated catalog-backed
stage authority record. `--evidence` is intentionally repeatable; every other
option and the transition positional are single-use. Reject unknown options,
missing option values, repeated single-use options, more than one positional,
invalid review mode, outside-root/traversal/symlink-escape paths, and phase-name
shorthand with `ERROR` before reading transition artifacts.

`$gate-check` is strictly read-only. It MUST NOT create, edit, delete, rename,
persist, sign, approve, or repair any project file, including stage authority,
`production/stage.txt`, evidence, attestations, reports, transition history, or
session state. It may emit records in conversation. Only a separate explicitly
authorized stage-advancement workflow may commit a transition.

The workflow returns one of:

- invocation/state `ERROR` with no gate record; or
- gate verdict `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL` plus an immutable
  conversational `cgs.gate-record/v2`.

An owner may separately request `PROCEED_WITH_ACCEPTED_RISK`; that request never
changes the verdict or advances stage.

## Supported transition/profile registry

These are the six supported transition IDs and their profile IDs. The shared
catalog's versioned stage graph remains authoritative and must declare the same
edge before this skill can evaluate it.

| Transition ID | Required authority stage | Candidate stage | Profile ID |
|---|---|---|---|
| `concept-to-systems-design` | `Concept` | `Systems Design` | `gate.concept-to-systems-design/v2` |
| `systems-design-to-technical-setup` | `Systems Design` | `Technical Setup` | `gate.systems-design-to-technical-setup/v2` |
| `technical-setup-to-pre-production` | `Technical Setup` | `Pre-Production` | `gate.technical-setup-to-pre-production/v2` |
| `pre-production-to-production` | `Pre-Production` | `Production` | `gate.pre-production-to-production/v2` |
| `production-to-polish` | `Production` | `Polish` | `gate.production-to-polish/v2` |
| `polish-to-release` | `Polish` | `Release` | `gate.polish-to-release/v2` |

Never accept `concept`, `production`, another phase name, an inferred edge, a
skip, a backward edge, or a non-adjacent ID. A mismatch between this registry and
the shared catalog is `ERROR — TRANSITION SCHEMA CONFLICT`, not permission to pick
one copy.

---

## Phase 0: Freeze the read-only run identity

Resolve exactly one repository root. Read all applicable `AGENTS.md` files for
the root and every admitted input. Capture:

- invocation tokens after parsing;
- run ID and UTC start timestamp;
- source revision/ref and dirty state when available;
- shared catalog path/revision and declared stage-schema/profile versions;
- repository path/size/revision snapshot needed by the mutation guard; and
- explicit evidence identities supplied by the caller.

If the root is ambiguous, unsafe, or changes identity during preflight, return
`ERROR` and stop. Do not write a checkpoint.

## Phase 1: Validate catalog-backed stage authority

Read [references/evaluation-contract.md](references/evaluation-contract.md) in
full. Apply its **Versioned stage authority input** rules before profile work.

1. Read the shared workflow catalog and locate its versioned stage schema,
   allowed transition graph, authority owner rules, canonical authority-record
   location, gate-receipt policy, and freshness policy.
2. If `--authority-record` was supplied, require it to resolve to the catalog's
   canonical record for this project; it cannot override the catalog.
3. Validate the authority record's schema, owner, current stage, transition-from,
   timestamp, source snapshot, previous-record chain, and required gate receipt.
4. re-read all referenced authority/receipt inputs and enforce the catalog's
   freshness/dirty-state policy.
5. Read plain `production/stage.txt`, when present, only as a
   `LEGACY_DECLARATION`: record path/revision/value and any contradiction. Never use
   it to select or validate a stage.

If the catalog lacks this contract, the record is missing/invalid/stale, the
chain or receipt fails, or authority sources conflict, return:

```yaml
schema: cgs.gate-error/v1
result: ERROR
reason_code: STAGE_AUTHORITY_UNVERIFIED | TRANSITION_SCHEMA_CONFLICT | AUTHORITY_CONFLICT
transition_id: <requested-or-null>
authority_record: <path-or-null>
catalog_revision: <revision>
stage_mutated: false
```

Do not emit a gate record or continue to artifacts.

### Select and confirm one edge

- With a transition argument, require exact registry/catalog match and authority
  stage equal to the edge origin. A repeated, backward, skipped, already-completed,
  or mismatched edge is `ERROR`.
- Without a transition argument, select the single catalog edge whose origin is
  the validated authority stage, show exact ID/origin/candidate plus authority
  path/revision, and ask for confirmation. Rejection stops without a gate record.
  Zero or multiple outgoing edges is `ERROR`; `Release` has no outgoing edge.

Record `selection_mode: EXPLICIT | AUTHORITY_AUTO_CONFIRMED`, confirmation status,
authority record path/revision, catalog graph version, and exact edge in the run state.

### Resolve review mode once

Use explicit `--review`; otherwise read `production/review-mode.txt`; otherwise
default to `lean`. The file must contain exactly `full`, `lean`, or `solo` after
trimming. Invalid content is `ERROR`, not a silent fallback. Freeze the mode for
the run. Review mode changes only director dispatch; it never changes profile
scope, deterministic checks, evidence thresholds, or verdict precedence.

---

## Phase 2: Load one versioned profile and bounded manifest

Read [references/transition-profiles.md](references/transition-profiles.md) in
full, then select exactly the profile mapped above. Verify the selected profile's
ID, transition, origin, and candidate agree with the validated catalog edge.
Mismatch or missing profile is `ERROR`.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Track the selected profile's hard ceilings for:

- manifest entries;
- full-content file count;
- context bytes;
- bytes versioned;
- tool actions; and
- elapsed assessment time.

Stop admitting inputs before a ceiling. Never use newest-file selection, broad
repository scans, sampling, artifact-count heuristics, or unlisted equivalence.
Budget overflow, ambiguous evidence, unreadable required scope, or concurrent
change is a named coverage gap and prevents PASS under the evaluation contract.

`docs/consistency-failures.md` is not scanned globally. Read only stable finding
IDs explicitly referenced by a selected profile input/evidence record, and admit
those exact rows to the manifest.

---

## Phase 3: Evaluate and normalize every profile check

Evaluate every selected check exactly once and return the complete normalized
check schema from `evaluation-contract.md`.

### Deterministic checks

- Verify exact predicates; do not use file existence as proof of substantive
  content, approval, execution, playability, coverage, or quality.
- Use structured extraction/search for large files when the profile permits it;
  cite exact path/revision/field or section for expected and observed values.
- Run configured read-only test commands only when the selected profile names an
  exact execution manifest/runner and the action remains inside its budgets.
  Never synthesize a runner or infer PASS from source files or a zero exit code
  without the required receipt.
- Check applicability predicates explicitly. `NOT_APPLICABLE` without evidence is
  `NOT_EVALUATED`.

### Prior-result checks

Use only the profile's producer adapter. Revalidate native schema, persistence,
identity, complete dependency manifest, exact current revisions, coverage, producer
verdict, and profile threshold. Preserve native and normalized verdicts.

A `cgs.review-evidence/v1` wrapper is acceptable only when the adapter allows it
and its exact current extension/payload is available and independently valid.
Native durable records require the exact adapter-listed schema/version and every
listed companion receipt. Unknown schema versions fail closed; never synthesize
an envelope, recorder receipt, persistence state, or legacy adapter. Do not accept:

- document-internal self-signoff;
- a report selected by glob/mtime;
- conversation-only output where persistence is required;
- a legacy verdict string or filename;
- aggregate revisions that omit required per-input revisions; or
- accepted risk/director opinion as approval.

Missing bindings are `UNBOUND`; changed/mismatched/expired bindings are `STALE`.
Both fail a blocking check.

### Canonical evidence invariants

When the selected adapter applies, enforce all of its native requirements,
including these non-substitutable rules:

- playtest sessions count only unique canonical completed gate-eligible reports;
- regression requires selection plus an exact build-bound runner receipt;
- performance requires a complete current `cgs.review-evidence/v1` plus
  `cgs.performance-report/v1` and `cgs.performance-budget/v2` chain, together
  with an independent `cgs.performance-report-recorder-receipt/v1` proving the
  canonical create-only target, exact bytes, atomic conflict check/read-back, RECORDED persistence,
  and `gate_evidence_eligible: true`; the analyzer's `persistence: NONE`
  candidate alone is not gate evidence;
- UX review requires durable gate evidence, while the current P1 producer's
  `NOT_PERSISTED` / `gate_evidence_eligible: false` candidate cannot pass;
- cross-GDD review requires the `cgs.review-evidence/v1` envelope together with
  `cgs.cross-gdd-review/v2`, full effective scope, and complete coverage;
- release-checklist remains a collector with `Gate Decision: NOT EVALUATED`;
- Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
- vertical slice requires one explicitly supplied current persisted
  `cgs.vertical-slice-evaluation-report/v2` PROCEED graph;
- smoke requires persisted `cgs-smoke-check-receipt/v2` sprint PASS with
  `Handoff Eligible: YES`;
- team QA requires persisted `cgs.team-qa-signoff/v2` with
  `WORKFLOW_COMPLETED`, `QA_APPROVED`, and `Gate Eligible: YES`;
- playtest requires `cgs.playtest-report/v2` plus an independently verified
  `cgs.playtest-report-recorder-receipt/v1`; and
- test-evidence review requires persisted
  `cgs-test-evidence-review-report/v2` with every current closure axis passing.

Do not weaken those requirements because another file or checklist says work was
completed.

---

## Phase 4: Collect permitted manual attestations

After all automatic checks, collect only unresolved rows whose selected profile
explicitly states `evidence_source: ATTESTATION_ALLOWED`. Ask all exact versioned
questions together and require `YES|NO|UNKNOWN`, accountable operator, observation
time, and subject identity.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

The attestation remains conversational. Do not save or sign it for the user.

---

## Phase 5: Run the bounded director advisory panel

Apply the **Director advisory panel** contract from `evaluation-contract.md`.

- `solo`: spawn nobody; record all four as `NOT_APPLICABLE_BY_MODE`.
- `lean` or `full`: issue all four delegations in parallel before waiting:
  `creative-director`/`CD-PHASE-GATE`,
  `technical-director`/`TD-PHASE-GATE`,
  `producer`/`PR-PHASE-GATE`, and
  `art-director`/`AD-PHASE-GATE`.

Pass only the exact transition/candidate, scope manifest revision, bounded artifact
summary, and domain context. Each gate gets one attempt and a 120-second deadline.
Preserve READY/CONCERNS/NOT READY as native advisory results. A director cannot
change a blocking check or force FAIL. Any enabled missing, timed-out, blocked,
errored, malformed, or stale result makes panel coverage incomplete and prevents
PASS; still produce the available partial panel.

Normalize the four results into common checks `DIR-C01`, `DIR-T01`, `DIR-P01`,
and `DIR-A01` after the selected profile check rows. In solo they are
NOT_APPLICABLE_BY_MODE and do not create a coverage gap.

Do not follow shared generic instructions to persist phase-gate outcomes. This
skill's read-only boundary controls.

---

## Phase 6: Calculate, challenge, and freeze the verdict

Apply the deterministic decision table in `evaluation-contract.md` without
averaging or subjective override:

1. confirmed blocking `FAIL|UNBOUND|STALE` -> `FAIL`;
2. otherwise required incomplete evaluation/scope/panel -> `PARTIAL`;
3. otherwise advisory risks -> `CONCERNS`;
4. otherwise -> `PASS`.

If a blocker and incomplete coverage coexist, preserve `FAIL` and set coverage
`PARTIAL`. Accepted risk does not participate.

Challenge the draft using the actual check set:

1. Re-read/re-run the two highest-risk PASS inputs within the existing budgets.
2. Re-scan normalized checks for accidental PASS from unknown/manual/unbound/
   stale/advisory evidence.
3. Verify every profile check ID appears exactly once.
4. re-read authority, scope manifest, and accepted evidence.
5. Reapply the decision table and record whether the verdict changed.

Do not generate a fixed number of generic questions or expand scope during this
step. Evidence discovered outside the profile is excluded and named, not admitted.

Run the mutation guard. If this workflow caused a filesystem mutation, report the
guard failure and do not claim a valid gate assessment. Do not revert anything.

## Required continuation

Read [references/continued-workflow.md](references/continued-workflow.md) in full.
It defines the v2 report, immutable gate/advance records, final revalidation, and
bounded handoff. Execute it in order and stop.
