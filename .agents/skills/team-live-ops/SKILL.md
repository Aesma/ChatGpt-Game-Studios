---
name: team-live-ops
description: "Orchestrates an ethics-gated, plan-only live-ops pipeline with bounded delegation, evidence-honest review, checkpoint recovery, and single-writer artifacts."
---

# Team Live Ops

## Invocation and scope

Invoke as `$team-live-ops [season name or event description] [--review full|lean|solo]`.

If no season name or event description is provided, return the documented usage and
stop before reading files, delegating, or writing:

> Usage: `$team-live-ops [season name or event description]` — Provide the name or
> description of the season or live event to plan.

This workflow produces planning artifacts only. It does not implement game content,
change economy or store configuration, publish communication, start an experiment,
schedule production, deploy a build, or claim production readiness. Proposed copy,
telemetry, rewards, and content remain unimplemented proposals even after
`PLAN COMPLETE`.

## Non-negotiable safety contract

1. **Policy gate** — A plan involving payment, premium currency, randomized rewards,
   artificial scarcity or time pressure, behavioral targeting, or an audience that
   includes or may include minors requires a readable
   `design/live-ops/ethics-policy.md`. If it is absent, return
   `BLOCKED — POLICY REQUIRED`. Only a demonstrably free event with no monetization,
   randomized rewards, pressure mechanic, sensitive experiment, or minor-specific
   risk may continue, and its strongest result is
   `DRAFT / ETHICS NOT REVIEWED`. It is never complete or production-ready.
2. **No conversational override** — A policy violation can only be revised away or
   remain `NON-COMPLIANT / BLOCKED`. Do not offer an in-conversation bypass or rationale-based waiver. An
   independently governed risk-acceptance artifact may be reported as context, but
   it does not make the plan policy-compliant, does not clear the finding, and cannot
   produce `PLAN COMPLETE` or a production handoff.
3. **Whole-plan ethics** — Review economy, reward randomness, retention, experiments,
   telemetry/privacy, communication, audience/minor protections, time windows,
   regional/platform constraints, cancellation/exit behavior, and accessibility.
   Never prescribe FOMO, loss-aversion pressure, misleading scarcity, or dark
   patterns. Communication proposals use transparent deadlines, player value,
   eligibility, costs, odds where relevant, and opt-out/exit information.
4. **Correct review profile** — Use the read-only `live-ops-review` profile defined in
   this workflow. Do not invoke `$design-review` for a season or event document.
   Review findings are not implementation or test evidence.
5. **Single writers** — Planning agents return proposals and have zero file mutation
   authority unless a later writer turn explicitly names their one artifact. Every
   path has exactly one writer, writers run sequentially, and no writer may edit
   another writer's path. Shared index/metadata and the checkpoint have one recorder.
6. **Incomplete work stays incomplete** — Any required agent failure, timeout,
   cancellation, stale result, partial context, open blocker, missing policy gate,
   failed preimage check, or partial write prevents `PLAN COMPLETE`.
7. **Evidence honesty** — Never invent a source hash, proposal hash, file write,
   policy rule, reviewer result, test result, telemetry result, or readiness claim.
   Use `NOT RUN`, `UNKNOWN`, `UNAVAILABLE`, `PARTIAL`, or `null` when evidence does
   not exist.
8. **Authorization is path-bounded** — Approval to plan is not approval to write,
   implement, publish, deploy, or modify shared state. Before the first file write,
   present one exact artifact manifest with paths, intended changes, unique writers,
   and current preimage hashes. Existing bounded authorization is sufficient only
   when it covers that exact manifest. New paths or broader changes require a new
   approval; subagent delegation never expands the boundary.
9. **Design before implementation** — No content implementation, final asset
   production, game/store configuration, experiment launch, publishing, sprint
   mutation, or deployment may begin before the consolidated design is reviewed and
   explicitly approved. This workflow stops after recording the approved plan.

## Review modes

`--review` controls delegation depth, not ethics or approval gates:

- `full` — delegate all six domain roles subject to the concurrency cap.
- `lean` — delegate live-ops-designer, economy-designer, analytics-engineer, and
  community-manager; the primary agent performs the narrative and copy-brief review
  sequentially and labels those sources `primary-agent`.
- `solo` — spawn no subagents. The primary agent performs every domain pass
  sequentially and never claims a named agent ran.

If the option is absent, use a valid value from `production/review-mode.txt` when
present; otherwise use `lean`. Reject unknown values. Every mode uses the same policy
gate, review rubric, evidence requirements, writer rules, and verdict rules.

## Roles and ownership

### Proposal roles — read-only

- **live-ops-designer** — scope, cadence, retention proposal, content dependencies,
  operational ownership, and rollback concept.
- **economy-designer** — reward/economy proposal, pricing, currency flow, randomness,
  bad-luck protection, and economy risk.
- **analytics-engineer** — metrics, telemetry schema, experiment protocol, privacy,
  stop rules, and kill switch.
- **community-manager** — transparent communication strategy and calendar proposal.
- **narrative-director** — theme, story hook, and lore constraints.
- **writer** — content inventory, naming/copy brief, and clearly labeled draft
  examples; no publishing or final asset mutation.

All proposal turns are read-only. Prompts list allowed sources and explicitly say
`mutation_authority: NONE`.

### Artifact writers — sequential and exclusive

| Artifact | Unique writer | Allowed write domain |
|---|---|---|
| season plan | live-ops-designer acting as season recorder | the exact season-plan path only |
| analytics plan | analytics-engineer | the exact analytics-plan path only |
| communication plan | community-manager | the exact communication-plan path only |
| checkpoint and optional season index/metadata | live-ops-designer acting as season recorder | only the manifest-listed checkpoint/index paths |

The writer identity is a file-ownership role, not permission to change another
domain's approved proposal. The narrative-director, writer, and economy-designer
never write these artifacts. Writers do not run concurrently. Before each write,
verify every manifest preimage; after each successful write, compute the raw-byte
SHA-256 and record it. A failed or mismatched write stops later writers and returns
`PARTIAL WRITE / BLOCKED` without claiming rollback or completion.

## Bounded delegation protocol

Record `max_parallel_agents = min(3, available_runtime_slots - 1)` in the run
checkpoint. If available capacity is unknown, use 2. If it is zero, run sequentially.
Never exceed 3 concurrent delegated agents.

Each delegation has a stable attempt ID, explicit inputs and input hashes, allowed
outputs, `mutation_authority: NONE`, a deadline recorded before launch, and one of:
`PENDING`, `SUCCEEDED`, `BLOCKED`, `TIMEOUT`, `CANCELLED`, or `STALE`. Default
deadline is 180 seconds unless a bounded run manifest declares another value.

For an independent batch:

1. launch all eligible agents up to the concurrency cap before awaiting results;
2. wait in bounded intervals and surface progress at least once per minute;
3. at deadline, interrupt/cancel the attempt and mark `TIMEOUT`;
4. allow at most one user-approved retry with a new attempt ID;
5. preserve successful outputs and their SHA-256 hashes;
6. reject late results from a cancelled, timed-out, or superseded attempt;
7. do not start a dependent phase until every required predecessor is `SUCCEEDED`.

Any missing required output yields `PARTIAL / BLOCKED`. Return the completed proposal
set and exact gaps, save an authorized checkpoint when possible, and stop before
design approval, final artifacts, or production handoff.

## Checkpoint and recovery contract

Before work begins, derive one stable season ID and exact artifact paths. The
changeset manifest includes:

- `design/live-ops/checkpoints/<season-id>.yaml`;
- `design/live-ops/seasons/<season-id>.md`;
- `design/live-ops/seasons/<season-id>-analytics.md`;
- `design/live-ops/seasons/<season-id>-comms.md`; and
- an existing season index/metadata path only when the requested change explicitly
  includes it.

The checkpoint is written only if that exact path is authorized. Otherwise emit the
same checkpoint block in conversation and mark `checkpoint_persisted: false`; never
silently add it to the changeset.

Checkpoint fields are:

```yaml
season_id: <stable-id>
review_mode: full | lean | solo
phase: <last-completed-phase>
checkpoint_revision: <integer>
inputs:
  - path: <repository-relative-path>
    sha256: <raw-byte-hash-or-null>
policy:
  path: design/live-ops/ethics-policy.md
  state: PRESENT | MISSING | UNREADABLE
  sha256: <hash-or-null>
risk_profile:
  policy_required: true | false
  reasons: []
artifact_manifest:
  - path: <exact-path>
    writer: <unique-role>
    preimage_sha256: <hash-or-ABSENT>
    status: NOT_WRITTEN | WRITTEN | FAILED
    postwrite_sha256: <hash-or-null>
decisions: []
agent_attempts: []
proposal_hashes: {}
findings: []
design_approval:
  state: NOT_REQUESTED | APPROVED | REJECTED
  owner: <identity-or-null>
  timestamp_utc: <timestamp-or-null>
next_phase: <phase-or-STOP>
```

The season recorder increments the checkpoint revision and writes it sequentially.
Resume only when the season ID, artifact manifest, policy hash, all input hashes, and
approved decisions match. Any mismatch makes the checkpoint `STALE`; preserve it,
report changed fields, generate a new manifest/checkpoint revision, and obtain new
authorization before any new path or changed intended write. Never infer success from
an old conversation or checkpoint alone.

## Phase 0: Validate input and establish the run

1. Parse one season/event description and optional valid review mode.
2. Resolve or propose a stable season ID. Reject traversal, absolute paths, ambiguous
   IDs, or collisions. Do not invent a successful registry allocation.
3. Load only bounded context: the game concept, explicit live-ops dependencies, the
   current economy rules, the ethics policy, and explicitly referenced prior season
   records. Default budget is 12 files and 512 KiB. Record every path and raw-byte
   SHA-256; if required context exceeds the budget, ask to narrow or expand it and
   return `PARTIAL CONTEXT / BLOCKED`.
4. Classify the policy-required risk triggers before delegation. Do not fabricate
   missing policy content.
5. Build the exact artifact manifest, unique-writer map, deadlines, concurrency cap,
   and checkpoint path. Obtain one changeset authorization before the first write.
   This authorization does not approve the design or any implementation.

If policy is required and the policy is missing or unreadable, checkpoint the block
when authorized and return `BLOCKED — POLICY REQUIRED` without spawning design or
production agents.

## Phase 1: Scope, audience, and risk proposal

Run the live-ops-designer proposal pass. It must return:

- event type, objective, audience and age assumptions;
- start/end window, regions and platforms;
- content inventory and explicit dependencies;
- daily/weekly engagement proposal without coercive pressure;
- monetization, currency, randomness, scarcity, and experiment flags;
- operational owners, support impact, rollback concept, and cancellation/exit path;
- unknowns and evidence sources.

Present genuine product choices to the user using Question → Options → Decision.
Record decision owner, UTC timestamp, selected option, and proposal hash. Routine
phase transitions do not require repeated approval.

A material scope, audience, monetization, randomness, or time-pressure change requires
reclassification against the policy gate and an artifact-manifest check.

## Phase 2: Narrative and economy foundation

After Phase 1 decisions are recorded:

1. obtain a narrative framing proposal from narrative-director, or the truthful
   primary-agent fallback defined by the mode;
2. obtain an economy proposal from economy-designer using the approved scope,
   audience, ethics policy hash, and current economy rules;
3. resolve product decisions for premium value, pricing, randomness, and progression;
4. freeze a shared event/economy schema with stable event, reward, currency,
   entitlement, and telemetry identifiers;
5. hash the approved foundation proposal.

Analytics, copy, or communication work that references economy/event fields cannot
start until this schema is frozen. If narrative or economy work is blocked or partial,
return `PARTIAL / BLOCKED`.

## Phase 3: Bounded parallel planning proposals

Only after the foundation hash is frozen, run the independent proposal workstreams,
up to the recorded concurrency cap:

- **analytics-engineer** — metrics and telemetry against the frozen identifiers;
  any experiment must state hypothesis, audience, sample/exposure limit, primary and
  guardrail metrics, stop rule, privacy/data-minimization rules, fairness check, and
  kill switch. Status is `PLANNED / NOT RUN`, never “validated.”
- **writer** — content inventory and copy brief against approved narrative/economy
  constraints. Examples remain `DRAFT / NOT PUBLISHED`.
- **community-manager** — transparent communication calendar covering eligibility,
  value, price/cost, randomized odds where relevant, dates/time zones, platform and
  region differences, reminders, known-issue/cancellation handling, and exit
  information. Never request coercive deadline pressure or misleading urgency.

All three return proposals only. Collect every eligible result before continuing. A
timeout or blocked required workstream yields `PARTIAL / BLOCKED` and prevents review
approval or final document writing.

## Phase 4: Read-only live-ops-review profile

Apply `live-ops-review` to the consolidated proposals. It is a document-type-specific,
read-only review and never edits source proposals or invokes `$design-review`.

Check these domains independently:

1. **Ethics and audience** — actual policy rules and policy hash; minors, accessibility,
   randomness, paid value, time pressure, opt-out, and manipulation risk.
2. **Economy integrity** — currency sources/sinks, pricing, entitlement, reward value,
   bad-luck protection, pay-to-win risk, and rollback consequences.
3. **Retention and communication** — transparent value and deadlines; no coercive
   streaks, loss-aversion traps, false scarcity, FOMO, or misleading copy.
4. **Experiments and telemetry** — frozen identifiers, consent/privacy, minimization,
   hypothesis, exposure, guardrails, stop rule, fairness, and kill switch.
5. **Content dependencies** — owner, source hash, readiness state, localization,
   accessibility, platform/region, and unresolved external dependency.
6. **Operations** — launch window, support/on-call owner, monitoring plan, incident
   thresholds, rollback/disable path, cancellation/refund handling, and regional or
   platform approval needs.

Use stable findings:

```yaml
id: TLO-<DOMAIN>-<NNN>
severity: BLOCKER | CONCERN | NOTE
domain: ethics | economy | retention | experiment | telemetry | comms | audience | content | operations
rule_source: <policy-path-and-rule-or-review-rubric>
evidence: <proposal-section-and-hash>
problem: <specific-observed-gap>
required_revision: <testable-change>
status: OPEN | RESOLVED | NON_COMPLIANT
revision_round: 0 | 1 | 2
```

A missing policy is not a passed ethics review. A risk-acceptance artifact is not a
resolved policy finding. Review status is one of `REVIEW PASSED`,
`REVIEW CONCERNS`, `NON-COMPLIANT / BLOCKED`, or `PARTIAL REVIEW / BLOCKED`.
Review evidence proves only that planning documents were examined; it is not a game,
test, analytics, platform, legal, or deployment result.

## Phase 5: Bounded revision and re-review

For each `OPEN` blocker, offer only:

- revise the implicated proposal; or
- stop with `NON-COMPLIANT / BLOCKED` or `BLOCKED`.

Do not offer an in-conversation waiver. Preserve finding IDs across revision. Re-review
only open findings plus regressions caused by the revision diff. Allow at most two
revision rounds in one run. If a blocker remains after round 2, return
`BLOCKED — REVIEW DID NOT CONVERGE` and stop. New blockers require concrete evidence
that they were introduced by the revision or were objective policy violations; do
not create an endless subjective review loop.

A policy violation becomes `RESOLVED` only when the violating design is removed or
changed to satisfy the cited rule. An external risk decision remains
`NON_COMPLIANT` for this workflow.

## Phase 6: Consolidated design decision

Present one consolidated proposal containing:

- season brief and audience/risk profile;
- narrative framing;
- economy design and frozen schema;
- analytics/experiment plan marked `NOT RUN`;
- content inventory/copy brief marked `NOT IMPLEMENTED`;
- communication strategy marked `NOT PUBLISHED`;
- live-ops-review findings;
- operational, rollback, platform, region, localization, and accessibility gaps;
- source and proposal hashes;
- exact artifact manifest and writer map.

Request explicit design approval only when all required proposals succeeded, the
policy is present when required, the review is not partial, and open blockers equal
zero. The approval record includes decision owner, UTC timestamp, consolidated
proposal hash, policy hash, and exact artifact manifest hash.

Approval means “record this plan,” not “implement or deploy it.” If the user rejects
or changes the design, update decisions/checkpoint and return to the affected phase
within the two-round limit. Do not start implementation or final production work.

## Phase 7: Sequential artifact recording

Only after both exact changeset authorization and design approval:

1. revalidate every input and artifact preimage hash before any final-document write;
2. run the season-plan writer and verify its one allowed path and postwrite hash;
3. revalidate remaining preimages, then run the analytics-plan writer;
4. revalidate again, then run the communication-plan writer;
5. let the season recorder update an authorized index/metadata path, if any, last;
6. update the authorized checkpoint last with all postwrite hashes and statuses.

No writers run concurrently. A writer receives only the approved proposal sections
for its artifact and may not change design decisions. If any hash is stale or a writer
fails, stop later writes, list every actual mutation and hash, and return
`PARTIAL WRITE / BLOCKED`. Do not claim atomic rollback, recreate missing evidence,
or report unwritten files as written.

Required document headers include season ID, plan status, consolidated proposal hash,
policy path/hash/state, review status, design approval owner/timestamp, source hashes,
writer identity, and artifact postwrite hash reported alongside the artifact.

## Verdicts and handoff

Use exactly one:

- `PLAN COMPLETE` — policy gate satisfied, all required proposals and review complete,
  zero open blockers, design approved, all authorized planning artifacts written and
  hash-verified. This means planning is complete only.
- `DRAFT / ETHICS NOT REVIEWED` — missing policy is allowed only for the strictly
  free, non-random, non-pressure, non-sensitive low-risk profile. No production or
  implementation handoff.
- `BLOCKED — POLICY REQUIRED` — policy-required risk with missing/unreadable policy.
- `NON-COMPLIANT / BLOCKED` — one or more policy violations remain.
- `PARTIAL / BLOCKED` — required context or proposal/review work is incomplete.
- `PARTIAL WRITE / BLOCKED` — only some authorized artifacts were written.
- `BLOCKED — REVIEW DID NOT CONVERGE` — blockers remain after two revision rounds.
- `BLOCKED — AUTHORIZATION REQUIRED` — exact planning artifact writes are not
  authorized.

Never output bare `COMPLETE`, `PRODUCTION READY`, `READY TO DEPLOY`, or claims that
tests, implementation, platform approval, localization, telemetry, experiments, or
release steps succeeded without corresponding external evidence.

## Next step

For `PLAN COMPLETE` only, suggest one separate next action appropriate to the
remaining gap, normally `$sprint-plan` to schedule approved implementation work.
Do not invoke it. Do not call `$team-release` until separately produced
implementation, QA, platform, and deployment evidence exists.

For every draft, blocked, partial, or non-compliant result, recommend only the single
action that resolves the named blocker. Never route a season document to
`$design-review`.
