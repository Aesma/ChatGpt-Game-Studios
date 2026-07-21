---
name: milestone-review
description: "Produces an evidence-backed milestone review from a stable milestone ID, reports unknown or stale inputs explicitly, and keeps objective readiness separate from the user's risk-acceptance decision."
---

# Milestone Review

Invoke as `$milestone-review [milestone-id|current] [--review full|lean|solo]`.

This workflow is read-only until the final, explicitly bounded report write. It never
changes a milestone, sprint, tracker, bug, test, performance, risk, scope, or session
state artifact.

## Non-negotiable safety contract

1. Never select a milestone by modification time, creation time, filename sort order,
   or a guess from prose.
2. Never invent, estimate, interpolate, or silently carry forward a progress or quality
   value. Every number must cite a verified source and formula; otherwise render the
   value as `UNKNOWN`.
3. Missing, empty, malformed, stale, out-of-scope, hash-mismatched, or
   revision-conflicting required evidence makes the evidence set `PARTIAL` and forbids
   an `evidence_verdict` of `GO`.
4. Keep `evidence_verdict`, `delivery_status`, `quality_status`, `risk_status`,
   `user_decision`, and `artifact_write_status` as separate fields. A user decision
   can record accepted risk but can never rewrite any evidence-derived field.
5. Producer review is advisory and read-only. It cannot modify source artifacts, the
   evidence-only draft, or the computed metrics.
6. Scope cuts are candidates until the user makes a separately recorded product
   decision. This workflow does not cut, defer, reprioritize, or edit scope.
7. Never overwrite a prior review. A path collision is `BLOCKED`, not permission to
   replace the existing artifact.

## Status vocabulary

Use exactly these independent fields in the report and final response:

| Field | Allowed values | Meaning |
|---|---|---|
| `delivery_status` | `COMPLETE`, `INCOMPLETE`, `UNKNOWN` | Whether milestone success criteria and required scope are complete |
| `quality_status` | `PASS`, `FAIL`, `UNKNOWN` | Whether every declared quality threshold is met |
| `risk_status` | `ON_TRACK`, `AT_RISK`, `OFF_TRACK`, `NOT_REVIEWED`, `UNKNOWN` | PR-MILESTONE result, skip state, or failed review |
| `evidence_status` | `COMPLETE`, `PARTIAL` | Whether all required evidence is verified and current |
| `evidence_verdict` | `GO`, `CONDITIONAL_GO`, `NO_GO`, `PARTIAL` | Objective, evidence-derived readiness |
| `user_decision` | `PROCEED`, `PROCEED_WITH_ACCEPTED_RISK`, `HOLD`, `NOT_RECORDED` | Governance choice made after the objective verdict |
| `artifact_write_status` | `COMPLETE`, `BLOCKED`, `ERROR`, `NOT_REQUESTED` | Result of the authorized report write only |

Saving a report sets only `artifact_write_status: COMPLETE`; it does not mean the
milestone is complete or ready.

## Phase 0: Parse once

Validate arguments before reading project data.

- The milestone selector defaults to `current`.
- A supplied milestone ID must match `^[a-z0-9][a-z0-9-]*$`. Reject path separators,
  traversal, globs, and ambiguous aliases.
- Resolve review mode once for the run: explicit `--review` value, otherwise the
  trimmed value in `production/review-mode.txt`, otherwise `lean`. Only `full`,
  `lean`, and `solo` are valid.
- Store the resolved selector and review mode. Do not parse or change them again later.

Invalid arguments produce `artifact_write_status: BLOCKED`; invoke no gate and write
nothing.

## Phase 1: Resolve one stable milestone ID

### Explicit selector

For an explicit ID, the authoritative file is
`production/milestones/<milestone-id>.md`. The filename is the stable ID. If the file
contains a milestone ID field, it must equal the filename.

### `current` selector

Read both of these authority files when present:

- `production/session-state/active.md`
- `production/milestones/index.md`

From each present file, accept only one explicit `Active Milestone ID:
<milestone-id>` or `active_milestone_id: <milestone-id>` field. Collect all declared
values.

Resolution succeeds only when:

- at least one authority file declares exactly one valid ID;
- no authority file declares more than one active ID; and
- all present declarations agree on the same ID.

Missing declarations, duplicate declarations, conflicts, malformed IDs, or a
declaration whose milestone file does not exist produce `BLOCKED`. Report the
authority paths and conflicting values, invoke no gate, and write nothing. Never fall
back to timestamps or ask the user to choose from a timestamp-derived list.

After resolution, read the milestone file. An absent, empty, or malformed file is
`BLOCKED`. Record the resolved ID and resolution source in the evidence ledger.

## Phase 2: Load and verify the evidence manifest

Read the fixed manifest
`production/milestones/evidence/<milestone-id>.yaml`. It must identify the same
milestone and declare the target build or checkpoint under review.

Required manifest entries are:

- milestone definition path, revision, and SHA-256;
- tracker path, revision, and SHA-256;
- the exact ordered milestone sprint IDs plus one sprint report path, revision, and
  SHA-256 for each ID;
- bug registry path, revision, and SHA-256;
- test-results path, revision, target build, measurement basis, and SHA-256;
- one or more performance-report paths with revision, target build, target hardware,
  and SHA-256;
- risk-register path, revision, and SHA-256;
- repository revision and the explicitly bounded roots used for code-health counts;
- manifest capture time and any freshness policy declared by the milestone.

Verify every path is inside the repository, exists, is non-empty, and parses according
to its declared format. Compute SHA-256 over the raw bytes and compare it with the
manifest. Confirm declared artifact revisions match the artifact contents, all target
build identifiers agree, all milestone sprint IDs are covered exactly once, and no
extra sprint is silently included. A dirty working tree or repository revision that
does not match the manifest makes repository-derived counts unavailable.

Use one of these evidence states for every entry:
`VERIFIED`, `MISSING`, `EMPTY`, `MALFORMED`, `HASH_MISMATCH`,
`REVISION_CONFLICT`, `STALE`, `OUT_OF_SCOPE`, or `UNKNOWN`.

A freshness rule must be evidence-backed: compare hashes/revisions/build IDs and any
milestone-declared maximum age. Do not invent a default maximum age. If a required
freshness claim cannot be verified, mark it `UNKNOWN`.

Build an evidence ledger containing role, path, declared revision, observed revision,
declared SHA-256, observed SHA-256, build/scope, state, and reason. If any required
entry is not `VERIFIED`, set `evidence_status: PARTIAL`. Continue only to create an
honest partial analysis with affected values set to `UNKNOWN`; never fill gaps from
memory or inference.

Create `source_snapshot_sha256` by hashing UTF-8 canonical JSON for the ordered ledger
entries `(role, path, declared_revision, observed_revision, observed_sha256, state)`.
Sort first by role and then normalized repository-relative path. Record the
canonicalization rule in the report.

## Phase 3: Compute deterministic metrics

Compute only from `VERIFIED` evidence and show the source path, revision/hash, formula,
numerator, denominator, unit, result, and confidence for each metric.

- `feature_completion_percent` =
  `100 * completed required acceptance criteria / total required acceptance criteria`.
  Count only milestone-scoped criteria with a one-to-one tracker mapping. If mappings
  or the denominator are missing, the value is `UNKNOWN`.
- `sprints_completed` = count of manifest sprint IDs whose report has a verified
  terminal completion state; denominator = exact manifest sprint-ID count.
- Open S1/S2/S3 counts come only from the verified bug registry using its documented
  open-state and severity mapping.
- Test coverage is copied from the verified test result, including measurement basis
  such as line, branch, requirement, or critical-path coverage. Never convert between
  bases.
- Each performance result is compared only with the matching milestone threshold,
  target build, and target hardware.
- `planned_vs_completed` uses one basis consistently. Prefer story points only when
  every scoped item has points; otherwise use item count and label the basis.
- `velocity_per_working_day` =
  `sum(completed units) / sum(elapsed working days)` across verified completed sprint
  reports using the same unit basis.
- `adjusted_remaining_working_days` =
  `ceil(remaining units / velocity_per_working_day)`. It is `UNKNOWN` when remaining
  units, elapsed working days, unit consistency, or positive velocity is unavailable.
- TODO/FIXME/HACK counts are valid only for the manifest repository revision and
  bounded roots; otherwise they are `UNKNOWN`.

Do not convert `UNKNOWN` into zero. Do not present a percentage without its
denominator. List evidence gaps beside every affected conclusion.

### Scope candidates

The analysis may list evidence-backed protect, simplify, defer, or cut candidates.
Each candidate needs a stable candidate ID, source evidence, schedule benefit,
player/pillar impact, dependency impact, tradeoff, and owner to decide. Label every
entry `CANDIDATE — NOT DECIDED`. User decisions must cite a separate decision record
or be recorded later as `user_decision`; recommendations do not mutate milestone
scope.

## Phase 4: Build and review the evidence-only draft

Create an evidence-only draft in memory. It includes the evidence ledger, source
snapshot hash, metric derivations, delivery/quality facts, blockers, risks, and scope
candidates. It excludes `evidence_verdict` and `user_decision`.

Serialize the draft exactly as it will be passed to a reviewer and compute
`evidence_draft_sha256` over those UTF-8 bytes. Show the draft and hash to the user
before any producer gate or write.

Apply the review mode resolved in Phase 0:

- `solo`: do not spawn PR-MILESTONE; record
  `[PR-MILESTONE] skipped — Solo mode` and `risk_status: NOT_REVIEWED`.
- `lean`: do not spawn PR-MILESTONE because it is not a phase gate; record
  `[PR-MILESTONE] skipped — Lean mode` and `risk_status: NOT_REVIEWED`.
- `full`: spawn `producer` through Codex subagent delegation using gate
  **PR-MILESTONE** from `.codex/docs/director-gates.md`.

The full-mode request must be read-only and include the resolved milestone ID and
target date, exact evidence-only draft bytes, `evidence_draft_sha256`,
`source_snapshot_sha256`, verified completion derivation, blocked story count,
verified velocity data or explicit `UNKNOWN`, and candidate scope tradeoffs. Tell the
producer not to write files or replace unknowns. Accept only `ON TRACK`, `AT RISK`, or
`OFF TRACK` bound to the same `evidence_draft_sha256`.

A timeout, delegation error, malformed result, hash mismatch, or reviewer use of
different inputs sets `risk_status: UNKNOWN` and forces `evidence_verdict: PARTIAL`.
Preserve the evidence-only draft and error evidence. Never silently rerun against
changed inputs.

## Phase 5: Derive the objective verdict

First derive:

- `delivery_status: COMPLETE` only when every milestone success criterion and required
  scope item is verified complete; `INCOMPLETE` when a verified item is incomplete or
  blocked; otherwise `UNKNOWN`.
- `quality_status: PASS` only when every declared quality threshold has verified,
  matching evidence and passes; `FAIL` when any verified required threshold fails;
  otherwise `UNKNOWN`.

Then derive `evidence_verdict` in this strict order:

1. `PARTIAL` if `evidence_status` is `PARTIAL`, delivery or quality is `UNKNOWN`, or a
   required full-mode producer review failed.
2. `NO_GO` if delivery is `INCOMPLETE`, quality is `FAIL`, a required blocker remains,
   or `risk_status` is `OFF_TRACK`.
3. `CONDITIONAL_GO` only when evidence is complete, delivery and quality pass, and
   `risk_status` is `AT_RISK`; list sourced, owned, deadline-bound conditions.
4. `GO` only when evidence is complete, delivery and quality pass, no required
   blocker remains, and risk is `ON_TRACK` or `NOT_REVIEWED`.

No user response can change these fields. In particular:

- `AT_RISK` remains `AT_RISK`;
- `OFF_TRACK` remains `OFF_TRACK`;
- `NO_GO` remains `NO_GO`;
- `PARTIAL` remains `PARTIAL`.

## Phase 6: Record a separate user decision

Show the complete objective status block, producer result or skip note, evidence gaps,
and tradeoffs. Then ask whether the user wants to record a governance decision.

Allowed records are:

- `PROCEED` only when `evidence_verdict: GO`;
- `PROCEED_WITH_ACCEPTED_RISK` for `CONDITIONAL_GO`, `NO_GO`, or `PARTIAL`;
- `HOLD`;
- `NOT_RECORDED` when the user does not decide.

Risk acceptance must record user-supplied decision maker, UTC timestamp, rationale,
accepted stable risk/gap IDs, and any follow-up owner/deadline. Never invent these
values. The report must state that accepted risk is not evidence of readiness and
does not promote, override, or relabel the objective verdict. Do not offer “override
to GO” or “frame as GO” options.

## Phase 7: Preview and write an immutable report

Use this immutable path:

`production/milestones/reviews/<milestone-id>/<run-id>.md`

Derive `run-id` as
`<UTC-YYYYMMDDTHHMMSSZ>-<first-12-of-source_snapshot_sha256>`. If that path already
exists, stop with `artifact_write_status: BLOCKED`; do not overwrite or invent a
suffix.

The report must include:

1. resolved milestone ID and authority source;
2. run ID, target build/checkpoint, review mode, and UTC generation time;
3. all independent status fields;
4. evidence ledger and every source hash/revision;
5. source snapshot and evidence-draft hashes with canonicalization rules;
6. metric formulas, operands, results, confidence, and `UNKNOWN` reasons;
7. delivery, quality, code-health, blocker, and risk findings with stable IDs;
8. producer result or exact skip/failure note bound to the draft hash;
9. scope candidates marked `CANDIDATE — NOT DECIDED`;
10. the separate user decision and risk-acceptance record;
11. actions with stable ID, evidence, owner, deadline, and status.

If the user already authorized this exact bounded report write, do not ask again.
Otherwise present the complete proposed changeset with the exact path and a summary
of the bytes to be written, then obtain one explicit approval before the first file
change. A materially expanded changeset requires a new preview and approval.

After approval, re-hash every source immediately before writing. If any source changed,
discard the candidate report, return to Phase 2, and obtain approval for the new
exact path/content. Write only the approved report. On success, compute and display
the saved report SHA-256 and set `artifact_write_status: COMPLETE`. On refusal, set
`BLOCKED`; on write or verification failure, set `ERROR`. Never report objective
readiness from write success.

## Final response

Return a compact status block with all independent status fields, resolved milestone
ID, report path or `null`, report SHA-256 or `null`, source snapshot hash, evidence
gaps, producer outcome/skip, and the recorded user decision. When no report was
written, say why and confirm that no source artifact changed.

Suggest `$gate-check` or `$sprint-plan` only as optional next actions. Do not invoke
them and do not claim they consumed this report without a separate, verified
interface contract.
