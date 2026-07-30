---
name: team-live-ops
description: "Orchestrate one bounded, ethics-gated live-ops planning run with dependency-safe proposals, protected experiment protocols, stable review findings, immutable recovery checkpoints, and single-owner artifacts that never imply production readiness."
---

# Team Live Ops

Produce planning artifacts for one exact season or event. This workflow does not
implement content, change economy/store configuration, launch an experiment, schedule
operations, publish messages, deploy a build, update a release, or prove production
readiness. `PLAN COMPLETE` means only that the approved planning artifacts were recorded
and verified.

## Invocation and strict request

Invoke only as:

`$team-live-ops --request <path> --request-revision <revision>`

Require both flags exactly once. Reject unknown/duplicate fields, missing values,
directories where files are required, globs, `latest`, mtime selection, unsafe IDs,
absolute or escaping paths, symlinks, unsupported schemas and request_revision drift. Stop
before project reads, delegation, output or writes on invocation failure.

The request is strict `cgs.team-live-ops-request/v2` and declares one operation:

- `PLAN` — read-only proposal generation and review candidate assembly;
- `REVISE` — one bounded revision round against exact open finding IDs;
- `REVIEW` — one independent read-only live-ops review;
- `RECORD` — sequentially create one exact approved artifact manifest;
- `STATUS` — read-only checkpoint/manifest verification; or
- `RESUME` — continue from one exact immutable checkpoint.

The request binds stable run/season IDs, mode `full|lean|solo`, create/revise intent,
exact `cgs.live-ops-context-manifest/v2`, season-ID reservation/registry observation,
ethics policy, review policy, producer registry and instruction-chain paths/revisions;
expected predecessor checkpoint; fixed file/byte/dependency/proposal/agent/response/time
budgets; exact operation outputs; and mutation authority/expiry when recording.

Never infer season number, name, existing revision, policy, mode, registry entry,
context, artifact path, checkpoint or reviewer. A date/title alone is not an ID. A
changed season, policy, context, foundation, artifact manifest or decision creates a new
identity and invalidates dependent approval.

## Plan-only authority and shared non-writes

Keep read-only planning, controller checkpoint/artifact CREATE, implementation,
experiment execution, store/economy mutation, external publication, scheduling,
deployment, shared index update and release-state update as separate authorities.
Approval at one layer grants none of the others.

Never write game assets, content source, localization, economy/store configuration,
telemetry code, experiment services, test evidence, platform calendars, issue/sprint/
milestone/release state, external channels or a shared season index. A shared index or
metadata update belongs to its named owner through a later separate CAS operation; a
season recorder cannot silently add it to this run.

Every proposal and review agent has `mutation_authority: NONE`. Only a later RECORD
operation may create the exact approved artifact bytes. No planning result authorizes
implementation, QA, launch, deployment or publication.

## Ethics gate inherited by every phase

A readable, revision-bound ethics policy is required for payment/premium currency,
randomized rewards, artificial scarcity or time pressure, behavioral targeting,
sensitive experimentation/telemetry, or an audience that includes or may include
minors. Missing/unreadable required policy returns `BLOCKED — POLICY REQUIRED`.

Only a demonstrably free, non-random, non-pressure, non-sensitive, non-minor-specific
event may continue without policy, and only as `DRAFT / ETHICS NOT REVIEWED`. It is
never PLAN COMPLETE or eligible for implementation/production handoff.

Policy violations can only be revised away or remain `NON-COMPLIANT / BLOCKED`. Do not
offer conversational waiver or rationale override. An external risk-acceptance artifact
is context only; it does not clear the policy finding, establish compliance or permit
PLAN COMPLETE in this workflow.

Review the whole behavior design: economy/randomness, retention, experiments,
telemetry/privacy, communication, audience/minors, time windows, regions/platforms,
accessibility and cancellation/exit/refund. Never prescribe FOMO, coercive streak loss,
loss-aversion pressure, false scarcity, misleading urgency or dark patterns. Copy uses
transparent dates/time zones, value, eligibility, cost/odds, limitations and exit paths.

Use the read-only live-ops review defined here. Never invoke `$design-review` for a
season/event plan.

## Modes and truthful fallbacks — TLO-012

Mode affects proposal staffing only; ethics, independence, evidence, approval, writer,
revision and verdict rules never change.

- `full`: delegate live-ops-designer, economy-designer, analytics-engineer,
  community-manager, narrative-director and writer within the live-slot budget.
- `lean`: delegate live-ops-designer, economy-designer, analytics-engineer and
  community-manager. The controller may draft narrative framing and content/copy brief
  sequentially, labeled `controller-fallback`, never as named-agent output.
- `solo`: spawn no proposal agents. The controller may create a bounded draft with
  producer `controller-fallback`. Because it authored every domain, it cannot also
  supply independent re-review; the strongest result before an independent REVIEW
  operation is `PARTIAL / BLOCKED — INDEPENDENT REVIEW REQUIRED`.

If a required delegated producer is unavailable in full/lean, the controller may use
the documented fallback only for proposal drafting. It may not fabricate independent
policy, legal, privacy, platform, test or operational approval. Record every fallback
and its effect.

## Stable IDs, context and bounds — TLO-009/TLO-011

`cgs.live-ops-context-manifest/v2` is the only context authority. It declares stable
run/season/product IDs, create/revise mode, exact reserved season-ID receipt or existing
season identity, ordered first-order source dependencies, policy/review/registry paths
and revisions, target audiences/regions/platforms, and fixed budgets.

For CREATE, require a collision-free stable season-ID reservation/registry receipt from
its owner. For REVISE, require exact prior plan identity/revision and new revision identity.
Never scan a directory, derive the next number, rename on collision or overwrite an
existing season. Normalize IDs/paths and reject canonical duplicates.

Read only listed first-order dependencies and their explicitly declared revision-bound
dependencies: game concept, approved design sources, current economy rules, policy,
platform/region constraints and named prior plans. Default ceilings are 16 files,
768 KiB, dependency depth 2, 32 proposal objects, 4 concurrent workers, 64 KiB per
response and 20 minutes; a request may lower but not raise them.

Admit whole source dependency closures. Record selected, loaded, missing, unreadable,
invalid, omitted and unprocessed rows with bytes/depth/reason. Required omission,
budget exhaustion, stale revision or unsupported source yields `PARTIAL CONTEXT / BLOCKED`.
Never silently truncate or send full repository context to delegates. Each prompt gets
only the needed bounded subset plus exact revisions and returns a bounded schema payload.

## Proposal ownership and artifact writers — TLO-010

Proposal roles are read-only:

- live-ops-designer: scope, cadence, retention, dependencies, operations and rollback;
- economy-designer: rewards, pricing, currencies, randomness/protection and economy risk;
- analytics-engineer: telemetry and protected experiment protocol;
- community-manager: transparent communication strategy/calendar;
- narrative-director: theme, story framing and canon constraints; and
- writer: stable content inventory, naming/copy brief and draft examples.

RECORD uses exactly four disjoint immutable artifacts:

| Artifact/schema | Unique writer | Canonical target |
|---|---|---|
| `cgs.live-ops-season-plan/v2` | live-ops-designer as season recorder | `design/live-ops/seasons/{season-id}/{plan-identity-revision}/season-plan.md` |
| `cgs.live-ops-analytics-plan/v2` | analytics-engineer | `.../analytics-plan.md` |
| `cgs.live-ops-content-manifest/v2` | writer | `.../content-manifest.md` |
| `cgs.live-ops-communication-plan/v2` | community-manager | `.../communication-plan.md` |

The content manifest is not silently embedded in the season plan. It owns stable
content IDs, inventory, dependency path/revision/readiness, implementation owner, draft
copy references, localization/accessibility/platform targets and explicit
`NOT_IMPLEMENTED` state. The season plan references its path/revision.

Narrative-director and economy-designer never write final artifacts. Writers run
sequentially in manifest order and can write only their one exact target. One controller
recorder writes only the separately authorized immutable artifact manifest/checkpoint,
never a shared index. Writer identity does not permit changing another domain proposal.

## Dependency graph and frozen foundation — TLO-007

Order planning work:

1. exact scope/audience/risk and product decisions;
2. narrative frame and economy/reward proposal;
3. frozen `cgs.live-ops-foundation-schema/v2` with event, reward, currency,
   entitlement, content and telemetry identifiers plus exact proposal revisions;
4. independent analytics fields that do not depend on economy plus content/comms
   scaffolds that do not reference unfrozen identifiers;
5. after foundation freeze, all dependent telemetry, experiment, reward-copy,
   eligibility, pricing/odds and communication rows;
6. cross-domain review, revision, approval and recording.

Do not force Phase 4/5 work into false independence. Only dependency-free subsets may
run early. Every dependent proposal binds the exact foundation schema identity. A
foundation change invalidates those proposals, review and approval; freeze a new
identity and recompute dependents.

## Delegation, timeout and late results — TLO-013

Before each batch, read configured `max_threads`, enumerate every live root/child/nested
agent and compute:

`available_child_slots = max(0, max_threads - live_threads_including_controller)`

Use `dispatch_slots = min(request_worker_limit, 4, available_child_slots)`. If config,
live count or request limit is missing/invalid, run serially. Nested delegation consumes
the same budget and is forbidden without an assigned slot.

Each assignment declares stable attempt ID, input/foundation revisions, allowed output,
`mutation_authority: NONE`, exclusive proposal slot, deadline, response limit,
cancel rule and retry budget of at most one. Gather a whole batch before dispatching
dependents.

Assignment state is `PENDING|SUCCEEDED|PARTIAL|BLOCKED|TIMEOUT|CANCELLED|STALE|ERROR|
LATE_IGNORED`. At deadline, interrupt and record timeout. Retry only before review freeze
with a new attempt ID, identical immutable inputs and explicit retry authority. A changed
input needs a new assignment/authority. Results arriving after cancellation, timeout,
supersession or review freeze are LATE_IGNORED and cannot write, replace a proposal,
change a finding or qualify the run.

Any required partial, timeout, cancellation, stale/error/late result yields
`PARTIAL / BLOCKED`, preserves successful independent proposals, prevents design
approval/recording/production handoff, and names the exact owner/resume action.

## Immutable checkpoints and idempotent recovery — TLO-014

Every milestone creates or proposes one immutable `cgs.live-ops-checkpoint/v2` at:

```text
design/live-ops/checkpoints/{season-id}/{run-id}/
  {sequence}-{checkpoint-identity-revision}.yaml
```

Each checkpoint binds request/context/policy/review/instruction/foundation/proposal/
finding/decision/artifact-manifest identities; predecessor path/revision; exact phase;
agent attempt states; budgets; review round; writer/preimage/postwrite states; approval;
verdict/readiness; persistence; and exactly one next operation. It is create-only and
never an increment-in-place file.

RESUME requires exact checkpoint path/revision and expected predecessor chain. Revalidate all
inputs, proposals, decisions and already written artifact bytes; verify target absence
and reconcile assignment/writer states. Do not replay successful assignments/writers.
Broken chain, stale bytes, ambiguous writer outcome, changed policy/foundation or target
collision blocks. Preserve old checkpoints and start a new identity/authorization for
changed work. STATUS performs the same checks read-only and never repairs state.

## Exact artifact manifest and recording authorization — TLO-009

After stable season ID, final proposals, findings and design decision exist, render
`cgs.live-ops-artifact-manifest/v2` with exact four targets, schema/identity, canonical
bytes/revision, unique writer, expected `ABSENT` or exact allowed revision preimage,
write order, parent identity, maximum bytes and explicit non-writes. The manifest binds
the consolidated proposal, policy/review, approval and instruction revisions.

Only now may RECORD request one exact changeset authorization. Earlier planning,
delegation or product approval cannot authorize unknown season numbers, filenames,
content, index updates or future paths. New/changed targets or bytes require a new
artifact manifest and authorization.

Immediately before each sequential writer, CAS every input/preimage/authority and
revalidate all prior postwrite revisions. Use atomic no-replace/create-new, flush, parse,
read back and revision. On drift, collision, partial/unknown writer result or mismatch, stop
remaining writers, list actual writes/revisions and return `PARTIAL WRITE / BLOCKED`.
Never claim rollback or unwritten artifacts.

## Protected experiment protocol — TLO-015

Every A/B, holdout, behavioral or offer experiment is a nested
`cgs.live-ops-experiment-protocol/v2` in the analytics plan and remains
`Experiment State: PLANNED_NOT_RUN`. It includes:

- stable experiment/version IDs, preregistration revision and falsifiable hypothesis;
- target audience, eligibility/exclusions, minors treatment, regions/platforms and
  assignment/randomization unit;
- control/treatments, minimum and maximum exposure, duration, sample-size/power method
  or approved rationale, holdout and contamination controls;
- one primary metric, guardrail metrics, decision thresholds, multiple-testing rule,
  stopping rules and inconclusive handling;
- adverse-impact/fairness segments and thresholds, accessibility and economy harms;
- exact event/foundation schema, data minimization, lawful basis/consent, retention/
  deletion, access roles and privacy/security review requirements;
- kill-switch mechanism/owner, monitoring cadence, rollback/compensation and incident
  communication; and
- independent ethics-review finding IDs/status and implementation/QA prerequisites.

Missing protection is a BLOCKER. Minimize exposure before statistical sufficiency,
never optimize coercion, and never infer that protocol approval means an experiment ran
or was safe. Launch requires separate implementation, privacy/security, QA, platform
and external-action authority outside this workflow.

## Live-ops review and bounded convergence — TLO-006

`cgs.live-ops-review/v2` is read-only and checks:

1. ethics/audience/minors/accessibility/manipulation;
2. economy/rewards/randomness/entitlement/rollback consequences;
3. retention and transparent communication;
4. experiments, telemetry, privacy, fairness and kill switch;
5. content dependency ownership/readiness/localization/platform/region; and
6. operations, timing, support/on-call, monitoring, incident thresholds,
   disable/rollback, cancellation/refund and approval dependencies.

Every finding has stable ID derived from domain/rule/proposal evidence identity,
severity `BLOCKER|CONCERN|NOTE`, domain, exact rule source/revision, evidence path/revision,
problem, testable revision, owner, state `OPEN|RESOLVED|NON_COMPLIANT`, introduced round
and last-reviewed round. Preserve the ID across revisions; do not renumber unchanged
findings.

For an OPEN blocker offer only revise or stop. Allow at most two revision rounds.
After each revision, freeze the diff/proposal revisions and use a reviewer who did not
author the implicated revision. Re-review only open findings plus deterministic
regression checks from the diff. If no independent reviewer is available, return
`PARTIAL / BLOCKED — INDEPENDENT REVIEW REQUIRED`. If any blocker remains after round 2,
return `BLOCKED — REVIEW DID NOT CONVERGE`. New findings need cited new/detected evidence;
do not create an unbounded subjective loop.

A policy violation resolves only when the design satisfies the cited rule. Risk
acceptance remains NON_COMPLIANT here.

## Design approval and readiness boundary — TLO-008

Present the consolidated proposal with exact season/risk, narrative, economy/foundation,
experiment, content, communication, review/findings, sources, artifact manifest and
writer identities. Obtain explicit design approval only when all required work
succeeded, required policy is current, independent review is complete and open blockers
are zero. Approval binds owner, UTC time, proposal/policy/review/artifact-manifest revision.
It means “record this plan,” never implement or deploy it.

Always include a production-readiness matrix with at least:

- content/asset implementation dependencies and owners;
- localization/accessibility/platform/region calendars and approvals;
- economy/store configuration implementation and rollback/disable mechanism;
- telemetry/experiment implementation, privacy/security approval and kill switch;
- QA/test/build evidence, support/on-call, monitoring, incident/cancellation/refund;
- exact status/evidence path/revision/owner/required next artifact for every row.

This workflow has no build-bound evidence and therefore always returns
`Production Readiness: NOT_EVALUATED` and `Production Handoff Eligible: NO`. Unknown or
planned rows cannot become ready. PLAN COMPLETE is determined only by exact plan revision, complete
required proposals/review, zero open blockers, accountable owners, design approval and
verified four-artifact recording; it never changes the readiness fields.

## Verdicts and shared integration — TLO-016

Use exactly one planning verdict:

- `PLAN COMPLETE` — planning-only conditions and four artifact receipts verified;
- `DRAFT / ETHICS NOT REVIEWED` — strictly low-risk policy-absent draft;
- `BLOCKED — POLICY REQUIRED`;
- `NON-COMPLIANT / BLOCKED`;
- `PARTIAL CONTEXT / BLOCKED`;
- `PARTIAL / BLOCKED`;
- `PARTIAL WRITE / BLOCKED`;
- `BLOCKED — REVIEW DID NOT CONVERGE`;
- `BLOCKED — AUTHORIZATION REQUIRED`; or
- `PARTIAL / BLOCKED — INDEPENDENT REVIEW REQUIRED`.

Never emit bare COMPLETE, PRODUCTION READY or READY TO DEPLOY.

Return `cgs.team-live-ops-result/v2` with every request/run/season/context/policy/
instruction/foundation/proposal/review/finding/decision/artifact/checkpoint identity;
mode/fallback/assignment/budget ledgers; exact verdict; Production Readiness
NOT_EVALUATED; Production Handoff Eligible NO; actual writes/revisions; explicit non-writes;
and one legal next action/owner or none.

Shared consumers must preserve the boundary:

- content/asset/localization workflows may use the approved content manifest only as a
  revision-bound design input; NOT_IMPLEMENTED is not asset or localization evidence;
- implementation planning may reference PLAN COMPLETE only after its own requirements,
  architecture and story-readiness gates; this workflow does not create a sprint;
- `$team-qa` consumes exact build/test evidence, never PLAN COMPLETE as QA PASS;
- `$release-checklist` may list these plans as source context but cannot normalize them
  as implementation, QA, platform, experiment or deployment PASS;
- `$team-release` cannot treat PLAN COMPLETE, design approval, experiment protocol or
  communication draft as GO or any deployment/publication authority.

Stop after the packet. Never invoke another workflow or update shared state.
