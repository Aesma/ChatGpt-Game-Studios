# Skill Test Spec: `$team-live-ops`

## Purpose

Verify the complete P1 remediation set TLO-006 through TLO-016. The workflow must
converge review deterministically, respect foundation dependencies, distinguish plan
completion from production readiness, authorize only an exact artifact manifest,
define a separate content artifact, bound all context and delegation, recover through
immutable checkpoints, and protect every proposed experiment.

This is a static and fixture-driven specification. It does not invoke the skill,
agents, implementation, tests, experiments, publication, release or deployment.

## Fixtures and harness rules

Positive fixtures contain exact raw bytes and full lowercase SHA-256 for:

- `cgs.team-live-ops-request/v2` and `cgs.live-ops-context-manifest/v2`;
- stable season-ID reservation or prior-plan revision identity;
- ethics/review policies, producer registry and applicable instruction chain;
- bounded concept, economy, platform/region and prior-plan dependencies;
- scope, narrative, economy and frozen foundation proposals;
- analytics/experiment, content and communication proposals;
- stable review findings, revisions, decisions and independent reviews;
- `cgs.live-ops-artifact-manifest/v2`, writer/preimage records and checkpoints; and
- actual `max_threads`, live-agent snapshots, assignment deadlines and outcomes.

Negative variants change exactly one fact unless stated otherwise. Tests assert no
undeclared file, shared index, implementation, experiment, store/economy, sprint,
release, deployment or external-channel mutation. Catalog test fields stay blank until
a separately authorized real execution produces receipts.

## Structural assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name is `team-live-ops`.
- [ ] Invocation is exactly `$team-live-ops --request <path> --expect-request <sha256>`.
- [ ] PLAN, REVISE, REVIEW, RECORD, STATUS and RESUME are explicit request operations.
- [ ] Missing required ethics policy or an unresolved policy violation cannot yield PLAN COMPLETE.
- [ ] Whole-plan review covers economy, retention, experiment, telemetry, communication, audience, content and operations.
- [ ] Findings use stable IDs and at most two independent revision/re-review rounds.
- [ ] Frozen foundation schema precedes every dependent analytics/content/comms field.
- [ ] PLAN COMPLETE always keeps Production Readiness NOT_EVALUATED and Production Handoff Eligible NO.
- [ ] Artifact manifest is rendered before RECORD authorization and binds exact bytes, writers and preimages.
- [ ] Content manifest is a distinct fourth artifact with one writer and NOT_IMPLEMENTED state.
- [ ] Context comes only from an exact manifest with hard file/byte/depth/object/agent/response/time budgets.
- [ ] Full, lean and solo modes have concrete staffing/fallback behavior but identical gates.
- [ ] Dispatch counts all live/nested agents and records deadlines, timeout, cancel, retry and late-result states.
- [ ] Checkpoints are immutable, predecessor-linked, hash-addressed and resumable without replay.
- [ ] Every experiment has preregistration, exposure/sample, metrics, privacy/fairness, stop, kill and rollback protections.
- [ ] Proposal/review agents are read-only and final artifact writers are unique, sequential and path-confined.
- [ ] Shared QA/release consumers cannot treat plan completion as test, release or action evidence.
- [ ] Terminal output is `cgs.team-live-ops-result/v2` with one legal next action.

## P1 traceability

| Audit ID | Primary case |
|---|---|
| TLO-006 | Case 1 |
| TLO-007 | Case 2 |
| TLO-008 | Case 3 |
| TLO-009 | Case 4 |
| TLO-010 | Case 5 |
| TLO-011 | Case 6 |
| TLO-012 | Case 7 |
| TLO-013 | Case 8 |
| TLO-014 | Case 9 |
| TLO-015 | Case 10 |
| TLO-016 | Case 11 |

## Case 1 — Stable findings and bounded independent re-review — TLO-006

Initial review produces two blockers. Revise one finding, leave the other unchanged,
then perform two review rounds. Test a revision reviewed by its own author and a late
subjective finding without new evidence.

**Expected**

- IDs derive from domain/rule/proposal evidence and persist across revisions;
- only finding state, reviewed round and exact evidence hash change;
- each revision diff is frozen and re-reviewed by a non-author;
- self-review without another eligible reviewer yields
  `PARTIAL / BLOCKED — INDEPENDENT REVIEW REQUIRED`;
- re-review covers open findings plus deterministic regressions caused by the diff;
- a new finding requires cited new/detected evidence;
- any blocker after round 2 yields `BLOCKED — REVIEW DID NOT CONVERGE`, with no loop,
  design approval, artifact recording or handoff.

## Case 2 — Shared foundation before dependent parallel work — TLO-007

Provide independent high-level metric and content scaffolds, but no frozen reward,
currency, entitlement or telemetry identifiers. Then freeze foundation F1 and later
change one reward ID to create F2.

**Expected**

- dependency-free scaffolds may run before freeze;
- telemetry fields, experiment events, reward copy, eligibility, pricing/odds and
  communication rows wait for F1;
- eligible work runs only in dependency-safe batches and binds F1 hash;
- F2 invalidates all F1-dependent proposals, review and approval;
- no test forces analytics/economy or phase groups to be independent when data
  dependencies exist.

## Case 3 — PLAN COMPLETE is not production readiness — TLO-008

Complete, approve and hash-verify all planning artifacts while content, localization,
store configuration, telemetry, QA, platform approvals, rollback tooling and on-call
evidence remain unimplemented or unavailable.

**Expected**

- planning verdict may be `PLAN COMPLETE` only when all plan-specific hashes, owners,
  proposals, review, findings, approval and four writes verify;
- readiness matrix lists every implementation/QA/platform/operations dependency with
  status, owner and required evidence path/hash;
- output remains `Production Readiness: NOT_EVALUATED` and
  `Production Handoff Eligible: NO`;
- no PLAN COMPLETE, design approval or artifact count becomes PRODUCTION READY,
  implementation done, experiment run, QA pass or deployment authority;
- missing owner or open plan blocker prevents PLAN COMPLETE itself.

## Case 4 — Exact artifact manifest precedes write authority — TLO-009

Begin with a season title but no stable number/ID. Later provide a collision-free season
reservation and final proposal bytes. Test a collision, a changed communication byte,
an added shared index path and RECORD authorization issued before exact filenames exist.

**Expected**

- no next-number scan, guessed season ID or mtime selection occurs;
- only the exact reservation/existing revision identity determines paths;
- artifact manifest binds four exact targets, bytes/hashes, unique writers, write order,
  preimages, parents and non-writes before RECORD authority;
- early/unknown-path authorization is unusable;
- changed byte/path/index produces a new manifest and authority request;
- shared season index is never silently included or written.

## Case 5 — Content inventory and copy have an explicit artifact — TLO-010

Provide content items, implementation dependencies, draft names/copy, localization,
accessibility and platform targets. Attempt to place all content implicitly in the
season document or let narrative/economy writers edit it.

**Expected**

- exact `cgs.live-ops-content-manifest/v2` is the fourth artifact at its own path;
- it owns stable content IDs, dependency hashes/readiness, owners, draft-copy references,
  targets and `NOT_IMPLEMENTED` state;
- season plan references the content path/hash rather than silently absorbing it;
- writer is the unique content-manifest writer; narrative/economy roles remain
  proposal-only;
- content manifest is not implementation, localization, asset or publication evidence.

## Case 6 — Context manifest and hard resource bounds — TLO-011

The manifest declares 20 candidate sources but ceilings allow 16 files/768 KiB/depth 2.
One required dependency closure crosses a budget; an undeclared adjacent prior season
exists with a newer mtime.

**Expected**

- only explicitly listed first-order sources and declared hash-bound dependencies load;
- no directory scan or recent-file substitution occurs;
- whole closures are admitted deterministically and never partially truncated;
- selected/loaded/missing/unreadable/invalid/omitted/unprocessed rows plus byte/depth
  usage are reported;
- required omission yields `PARTIAL CONTEXT / BLOCKED`;
- delegate prompts receive bounded subsets and bounded responses, not full repository
  context;
- a request attempting to raise hard ceilings is rejected.

## Case 7 — Review modes have real behavior and truthful fallback — TLO-012

Run full, lean and solo with identical policy/context. Also make a required delegated
producer unavailable.

**Expected**

- full delegates six named proposal roles within actual slots;
- lean delegates four core roles and labels controller narrative/content proposals
  `controller-fallback`;
- solo spawns none, claims no agent output and cannot independently approve its own
  all-domain draft; it requires a later independent REVIEW;
- unavailable producer fallback is allowed only for proposal drafting and is recorded;
- no mode weakens ethics, evidence, review, writer, revision or verdict rules;
- modes cannot fabricate legal/privacy/platform/test/operational approval.

## Case 8 — Timeout, partial, cancel, retry and late result — TLO-013

With configured `max_threads = 6`, controller plus two other live agents, request four
workers. Analytics succeeds, content is partial, communications time out and narrative
is cancelled. A timed-out result arrives after review freeze.

**Expected**

- available/dispatch slots are three and actual concurrency never exceeds three;
- nested delegates consume the same budget;
- every assignment records input hashes, exclusive slot, deadline, response limit,
  attempt and state;
- at most one retry occurs before freeze with identical inputs and new attempt ID;
- partial/timeout/cancelled required work yields `PARTIAL / BLOCKED` and prevents
  approval/recording/handoff while preserving successful proposals;
- late output is `LATE_IGNORED` and cannot overwrite or alter frozen state;
- invalid concurrency information falls back to serial execution.

## Case 9 — Immutable checkpoints and idempotent resume — TLO-014

Interrupt after foundation freeze, review and the second artifact write. Resume from
each exact checkpoint, then vary predecessor hash, policy byte, foundation identity,
writer outcome and next target existence.

**Expected**

- each checkpoint is a new hash-addressed create-only file with predecessor, all input/
  proposal/finding/decision/artifact identities, agent/writer states, budgets and one
  next operation;
- valid resume re-hashes the chain, reconciles writer state and never replays successful
  assignments/writes;
- drift/broken chain/ambiguous write/collision blocks and preserves old history;
- changed work uses a new identity and authorization;
- STATUS is read-only and never repairs or increments a checkpoint in place.

## Case 10 — Sensitive experiments require a protected protocol — TLO-015

Test an A/B offer with: no hypothesis; unbounded exposure; no sample method; only vanity
metrics; no privacy retention; minors without treatment; no fairness guard; no stop rule;
and no kill/rollback owner. Then provide a complete protocol.

**Expected**

- each missing protection produces a stable BLOCKER;
- complete `cgs.live-ops-experiment-protocol/v2` binds preregistration, hypothesis,
  audience/exclusions/assignment, control/treatment, min/max exposure, sample/power,
  primary/guardrail metrics, thresholds, multiple testing, stopping/inconclusive rules,
  fairness/accessibility/economy harms, event schema, minimization/lawful basis/
  retention/access, kill switch, rollback and incident communication;
- status remains `PLANNED_NOT_RUN` even after plan approval;
- review minimizes exposure and never optimizes coercion;
- launch still requires separate implementation, security/privacy, QA, platform and
  external-action authority.

## Case 11 — Complete spec, catalog boundary and shared integration — TLO-016

Run document-structure lint and shared-consumer fixtures.

### Structure expectations

- all eleven IDs TLO-006 through TLO-016 occur in SKILL and spec;
- exactly eleven primary cases contain fixtures/inputs and explicit expected behavior;
- Case 1 is complete rather than orphaned text after static assertions;
- schemas, verdicts, four artifacts, checkpoints and mode behavior agree across skill,
  metadata and spec;
- catalog result/timestamp fields remain blank without actual execution evidence.

### Shared-consumer variants

1. approved content manifest presented to asset/localization workflow;
2. PLAN COMPLETE presented to implementation planning;
3. PLAN COMPLETE presented as Team QA PASS;
4. PLAN COMPLETE/design approval/experiment protocol/comms draft presented to
   release-checklist or team-release as release/deploy/publish permission.

**Expected**

- variant 1 is hash-bound design input only and retains NOT_IMPLEMENTED;
- variant 2 still requires requirements, architecture, story-readiness and its own
  authorized implementation workflow;
- variant 3 is not build/test evidence and cannot affect QA verdict;
- release-checklist may treat plans as source context only, never implementation, QA,
  platform, experiment or deployment PASS;
- team-release cannot derive GO or any action authority from any planning artifact;
- live/shared/catalog/old-P0 files remain unchanged by staging this candidate.

## Required P0 regression matrix

Retain these safety properties from the prior candidate:

1. missing required policy blocks risky/monetized/minor/sensitive plans;
2. strictly low-risk policy-absent work remains DRAFT / ETHICS NOT REVIEWED;
3. policy violation has no conversational override and remains non-compliant;
4. ethics review covers retention/comms/experiment/telemetry, not economy alone;
5. live-ops-specific review is read-only and never calls design-review;
6. proposal agents have no mutation authority and artifact writers are unique/
   sequential/path-confined;
7. final recording requires independent review, exact design approval and exact write
   authority;
8. partial writes list actual mutations/hashes and never claim rollback;
9. no test, analytics, platform, localization, implementation, publication or release
   evidence is fabricated; and
10. every non-complete outcome recommends only the single action that addresses its
    blocker and invokes no downstream workflow.
