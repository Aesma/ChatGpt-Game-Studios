---
name: quick-design
description: "Create an immutable, low-structural-risk design-change proposal against one exact GDD hash; authoritative application, independent review, lifecycle recording, and implementation authorization remain separate."
---

# Quick Design

`quick-design` is the lightweight authoring path for a small, structurally
low-risk change to an existing design. It creates one proposal. It never edits an
authoritative GDD, data file, registry, index, story, review, lifecycle record, or
implementation.

A quick proposal is rationale and requested delta, not a source of truth.
Production work consumes the updated authoritative GDD only after separate
application, independent current-hash review, and lifecycle recording.

## Invocation and modes

Use one explicit mode:

```text
$quick-design propose "<change>" --change-id <QD-stable-id> --version <vNNN> --target <exact-gdd-path> [--expect-base <sha256:...>] [--supersedes <exact-proposal-path>] [--experiment-only <exact-prototype-scope>]
$quick-design status <exact-proposal-path> [--record <exact-lifecycle-record-path>]
```

`propose` is the only writing mode. `status` is read-only. Reject missing or
ambiguous mode, change ID, version, or target. Do not infer "the most relevant"
GDD, use filename similarity, select the latest file, or use modification time.

`change-id` must match `QD-[a-z0-9][a-z0-9-]{2,63}`. `version` must match
`v[0-9]{3}`. The canonical path is:

`design/quick-specs/<change-id>/<version>/proposal.md`

A later proposal is a new immutable version. It must use a new version ID, bind
the current target bytes, and name the exact predecessor path and SHA-256 in
`Supersedes`. Never update or overwrite an existing proposal.

## Roles and authority boundary

Keep these responsibilities separate:

1. **Proposal author** — this `quick-design propose` task gathers the product
   decision and may create only `proposal.md`.
2. **Application author** — a later, separately authorized design-authoring task
   applies selected deltas to the authoritative GDD. Use the staged
   `design-system revise-section` contract for each affected section.
3. **Independent reviewer** — a fresh task runs staged `design-review` on the
   complete updated GDD. It edits nothing and its verdict is bound to the exact
   reviewed GDD hash.
4. **Lifecycle recorder** — another owner-authorized task validates the proposal,
   application, current GDD, independent review, and expected record pre-state,
   then may create an APPLIED or SUPERSEDED lifecycle record.

The reviewer task ID must differ from the proposal-author and application-author
task IDs. The recorder task ID must differ from all author and reviewer task IDs.
A subagent in the authoring task, the author in another role, a user chat approval,
or a solo/advisory review does not satisfy independence.

An explicit bounded request to create the proposal authorizes only the proposed
`proposal.md` path after its product content is approved. It does not authorize a
GDD/data/index/story/record edit, formal review, or implementation. If the user
asks to apply or implement during this invocation, stop after the proposal
handoff. Keep the proposal operation's axes unchanged and report a separate
`Downstream Action: BLOCKED — SEPARATE APPLICATION AND REVIEW REQUIRED`.

## Status axes

Always report these independently:

- `Workflow Status`: `COMPLETE`, `BLOCKED`, `REDIRECTED`, `PARTIAL`, or
  `ERROR`.
- `Proposal Status`: `DRAFT`, `PROPOSED`, `APPLIED`, `SUPERSEDED`, or
  `NOT_CREATED`.
- `Currentness`: `CURRENT`, `STALE`, `INVALID`, or `NOT_APPLICABLE`.
- `Implementation Eligible`: `YES` or `NO`.
- `Persistence`: `NOT_REQUESTED`, `DECLINED`, `VERIFIED`, or `FAILED`.
- `Verdict`: `PROPOSAL_CREATED`, `DRAFT_ONLY`, `STATUS_REPORTED`,
  `REDIRECTED`, `BLOCKED`, or `ERROR`.

`Workflow Status: COMPLETE` means the requested authoring or status operation
finished. It never means the design is approved or implementation-ready.
`Implementation Eligible: YES` is possible only in read-only `status` mode after
the full APPLIED-currentness rule below. The `propose` result is always NO.

## Phase 1: Resolve the exact authoritative base

For production changes, require one exact existing system-GDD path under
`design/gdd/`. Reject a directory, glob, multiple matches, `systems-index.md`,
review artifact, quick proposal, story, or data file as the authoritative target.
Read applicable `AGENTS.md` guidance and the target's raw bytes. Compute lowercase
`sha256:<64 hex>` and record it as `Base GDD SHA-256`.

If `--expect-base` is supplied, it must equal the computed hash. A mismatch
returns:

```text
Workflow Status: ERROR
Proposal Status: NOT_CREATED
Currentness: STALE
Implementation Eligible: NO
Persistence: NOT_REQUESTED
Verdict: ERROR
Reason: STALE BASE — REBASE REQUIRED
```

Read the target's stable artifact/system ID, Status, and exact affected section
headings. Compute a SHA-256 for each affected section's raw heading-bound range.
Duplicate or ambiguous headings, unreadable bytes, missing stable identity, or an
unresolved target section returns BLOCKED and writes nothing.

Read the exact current systems index and other authoritative dependency records
needed to prove ownership. Record their paths and SHA-256 hashes. If required
ownership/dependency evidence is missing, ambiguous, or contradictory, return
`BLOCKED — RISK EVIDENCE REQUIRED`. Do not interpret missing evidence as low risk.

Do not scan old quick specs as authority. When revising the same proposal, require
`--supersedes` and validate that exact predecessor's path, artifact type, change
ID, version, hash, and target identity. An invalid/stale predecessor blocks a new
version.

For an explicitly requested `--experiment-only` proposal, require an exact path or
stable ID under `prototypes/` and set `Target Use: EXPERIMENT_ONLY`. It may never
target production code, data, a production story, or a production GDD mutation,
and it can never become APPLIED or implementation-eligible.

## Phase 2: Run the structural risk gate

Do not estimate hours or days to decide eligibility. Effort may be recorded as
non-gating planning context only.

For every row below, record `YES`, `NO`, or `UNKNOWN` plus an exact evidence path,
section/ID, and source hash:

| Risk fact | Gate result |
|---|---|
| Adds a system or subsystem, or requires a new systems-index row | YES redirects |
| Adds a state, changes state ownership, or changes lifecycle ownership | YES redirects |
| Adds or changes a cross-system input/output, timing, ordering, or ownership contract | YES redirects |
| Adds or changes a player-facing core rule, pillar, MDA relationship, or progression/economy rule | YES redirects |
| Changes formula semantics rather than a documented value within its allowed range | YES redirects |
| Changes persistence, save compatibility, networking, security, accessibility policy, or platform contract | YES redirects |
| Requires multiple authoritative owners or conflicts with another current GDD | YES redirects |
| Places a tuning value outside its documented current range | YES redirects |
| Lacks evidence needed to answer any row | UNKNOWN blocks |

The product owner may change the proposed design so the facts change, but cannot
override a true fact by selecting a lower-risk label. Re-run the checklist against
the revised proposal and the same current source bytes.

If any row is YES, stop before drafting or writing:

```text
Workflow Status: REDIRECTED
Proposal Status: NOT_CREATED
Currentness: NOT_APPLICABLE
Implementation Eligible: NO
Persistence: NOT_REQUESTED
Verdict: REDIRECTED
Next owner: $design-system
```

If any row is UNKNOWN, use `BLOCKED / NOT_CREATED / Implementation Eligible: NO`
and name the missing evidence. Only all-NO evidence can enter the quick path.

## Phase 3: Assign the review profile

Choose the profile from facts, not preference or effort:

- `QD-TUNING` — changes only documented designer-controlled numeric defaults
  within their current allowed ranges; formula meaning, behavior, states, and
  interfaces are unchanged. Required independent review depth: `lean` or `full`.
- `QD-LOCAL` — clarifies or adjusts a bounded rule within one existing system and
  existing ownership/interface surfaces, while every Phase 2 risk fact remains
  NO. Required independent review depth: `full`.
- `EXPERIMENT_ONLY` — temporary prototype hypothesis with no production handoff.
  Formal approval and APPLIED status are not available.

`New Small System` is not a quick profile. A new system redirects regardless of
predicted implementation effort. A tuning value outside the current GDD range
also redirects; the range must first change through full authoring and review.

Show the completed risk table, evidence hashes, inferred profile, and required
review depth. Ask the user to decide whether to proceed with that fact-based
profile, revise the product change, or redirect. A label choice cannot alter the
evidence-derived gate result.

## Phase 4: Make the product decision

Follow `Question -> Options -> Decision -> Draft -> Approval` for every unresolved
product choice. Present two to four meaningful options with tradeoffs. The user,
not the author or reviewer, selects the rule/value and rationale.

Use only current authoritative design evidence. Route implementation selections,
engine APIs, class/module names, storage schemas, test procedures, and technical
architecture to named downstream owners; do not place them in the design delta.

For `QD-TUNING`, require the exact current knob name, default, range, unit,
affected observable behavior, proposed in-range value, and rationale. For
`QD-LOCAL`, require exact base rule locators, the requested product-level delta,
unchanged invariants, observable outcomes, and the owner of each affected
artifact. Acceptance conditions must be measurable; "feels right" alone becomes a
named playtest hypothesis with metric, observation method, and decision threshold.

## Phase 5: Draft one immutable proposal

Use this exact header:

```markdown
# Quick Design Change Proposal: <title>

Artifact Type: quick-design-change-proposal
Schema Version: 1
Change ID: <QD-stable-id>
Version: <vNNN>
Status: PROPOSED
Target Use: PRODUCTION_CHANGE | EXPERIMENT_ONLY
Prototype Scope: <exact prototypes path or stable ID | NOT_APPLICABLE>
Risk Profile: QD-TUNING | QD-LOCAL | EXPERIMENT_ONLY
Required Review Depth: lean | full | NOT_APPLICABLE
Proposal Author Task ID: <task-id>
Created At UTC: <RFC3339>
Target GDD Path: <exact path | NOT_APPLICABLE>
Target GDD Artifact/System ID: <stable ID | NOT_APPLICABLE>
Base GDD SHA-256: <sha256:... | NOT_APPLICABLE>
Systems Index Path/SHA-256: <exact path and hash | NOT_APPLICABLE>
Supersedes Path/SHA-256: <exact path and hash | NONE>
Currentness at Creation: CURRENT
Implementation Eligible: NO
```

Then include exactly these level-two sections:

1. `## Product Decision` — selected rule/value, rationale, authoritative owner,
   and explicit non-goals.
2. `## Base Snapshot` — ordered target section IDs/headings and hashes, short
   locators, source paths/hashes, and current authoritative statements. Quote only
   the minimum needed to identify the delta.
3. `## Structural Risk Evidence` — every Phase 2 row, YES/NO/UNKNOWN, evidence
   locator/hash, and derived profile.
4. `## Proposed Delta` — stable delta IDs, target section, product-level before/
   after meaning, unchanged invariants, and affected artifact owners. State:
   "This proposal does not replace the authoritative GDD."
5. `## Observable Acceptance Conditions` — stable AC/hypothesis IDs, observable
   conditions, metrics/thresholds where applicable, and validation owner.
6. `## Apply, Review, and Record Handoff` — base hash, ordered application
   targets, required `design-system revise-section` handoffs, required independent
   review depth, lifecycle-record requirements, and explicit implementation
   block.
7. `## Boundaries` — exact owned write plus GDD/data/index/story/review/record/
   implementation non-writes.

Do not include a `GDD Update Required? No` escape hatch. A production delta is
only a proposal until the authoritative GDD is updated and independently approved.
Do not tell a programmer to implement from the proposal.

## Phase 6: Approve and persist the proposal only

Show the full draft. Ask the user to approve the proposal content, revise it, or
redirect. Content approval means the draft expresses the product decision; it is
not formal design review or implementation approval.

Before the first write, present one bounded changeset:

```text
CREATE design/quick-specs/<change-id>/<version>/proposal.md
NON-WRITES design/gdd/**, assets/data/**, design/gdd/systems-index.md,
           production/**, src/**, tests/**, review artifacts,
           lifecycle records, session state
```

Use an already explicit bounded authorization when it covers this exact CREATE;
otherwise obtain one authorization. Do not re-prompt per section. Immediately
before writing, re-read and re-hash the target GDD, every affected section, the
systems index, dependency evidence, and predecessor proposal. Any change returns
`ERROR — STALE BASE — REBASE REQUIRED` and writes nothing.

Reject an existing canonical proposal path. Return `ERROR — PATH EXISTS; CHOOSE A
NEW VERSION` without modifying it. Never offer in-place update.

Write the one proposal atomically, re-read its bytes, verify the schema, source
hashes, status, and expected content, then report its SHA-256. A declined write
returns `COMPLETE / DRAFT / DRAFT_ONLY / Persistence: DECLINED`. A failed or
unverified write returns `ERROR / NOT_CREATED / ERROR / Persistence: FAILED`.
Only verified persistence returns:

```text
Workflow Status: COMPLETE
Proposal Status: PROPOSED
Currentness: CURRENT
Implementation Eligible: NO
Persistence: VERIFIED
Verdict: PROPOSAL_CREATED
```

## Phase 7: Separate application, review, and recording handoff

After verified proposal creation, stop with these independent next actions:

1. **Application:** in a separate task, the design author reads the exact proposal
   and revalidates its hash and Base GDD SHA-256. For each accepted delta, run
   `design-system revise-section` with its own exact changeset authorization.
   The application author writes only the authoritative GDD/checkpoint allowed by
   that workflow and produces an immutable application receipt containing
   proposal path/hash, pre/post GDD hashes, applied delta IDs, task ID, and
   timestamp.
2. **Review:** after the final GDD edit, a fresh independent task runs
   `design-review <exact-gdd-path> --depth <required-depth>`. `QD-TUNING` accepts
   formal `lean` or `full` approval; `QD-LOCAL` requires formal `full` approval.
   `solo` is advisory and never sufficient. The report must be immutable,
   independently attributable, and bound to the exact post-application GDD hash.
3. **Record:** a separate recorder re-hashes every input and expected record
   pre-state, then may append a lifecycle record. This skill does not perform that
   write.

An APPLIED lifecycle record uses a fresh exact path under:

`design/quick-specs/<change-id>/<version>/records/<record-id>.md`

It must contain artifact type `quick-design-lifecycle-record`, schema version 1,
`Status: APPLIED`, proposal path/hash, application receipt path/hash and task ID,
updated GDD path/hash, independent review receipt path/hash, verdict `APPROVED`,
review depth and independence, reviewer task ID, recorder task ID, exact previous
record path/hash or NONE, timestamp, and `Implementation Eligible: YES`.

A SUPERSEDED record uses the same binding fields, `Status: SUPERSEDED`, successor
proposal path/hash, recorder task ID, and `Implementation Eligible: NO`. Lifecycle
records are append-only. Select one by explicit path and hash, never mtime.
Conflicting records, reused task identities, missing hashes, or an unexpected
pre-state are invalid and authorize nothing.

Only the recorder may create lifecycle records. The proposal author, application
author, and reviewer must not self-record APPLIED or SUPERSEDED.

## Phase 8: Read-only status and implementation eligibility

`status` reads the exact proposal and optional exact lifecycle record. It never
searches for a newer version or record. Re-hash all referenced artifacts.

Without a lifecycle record, return `Proposal Status: PROPOSED`,
`Currentness: CURRENT` only if the target still equals Base GDD SHA-256, and
`Implementation Eligible: NO`.

For a supplied APPLIED record, `Implementation Eligible: YES` requires all of:

- proposal path/hash and change/version identity match;
- record schema, append-only predecessor binding, and role/task independence are
  valid;
- application receipt is valid and binds the proposal to exact pre/post GDD
  hashes and applied delta IDs;
- the current GDD raw-byte SHA-256 equals the applied post-GDD hash;
- the independent review receipt is immutable, formal, `APPROVED`, at or above
  the profile's required depth, and targets that same current GDD path/hash;
- no SUPERSEDED record is supplied for this proposal;
- all referenced paths and hashes revalidate now.

If any check fails, preserve the recorded lifecycle status but report
`Currentness: STALE` or `INVALID` and `Implementation Eligible: NO`. Never repair
or rewrite evidence in status mode.

For a valid SUPERSEDED record, return `Proposal Status: SUPERSEDED`,
`Currentness: CURRENT`, and `Implementation Eligible: NO` with the exact successor
path/hash.

A production story may cite the proposal as rationale, but its authoritative GDD
reference must identify the updated GDD path/hash and the exact current APPLIED
record path/hash. Story readiness or development must reject PROPOSED,
SUPERSEDED, stale, invalid, experiment-only, advisory-reviewed, or unrecorded
quick designs. Even APPLIED status does not authorize this skill to start
implementation; a separate current story-readiness decision is still required.

## Final response contract

Every invocation reports exact inspected/created paths and hashes, risk profile,
all status axes, non-writes, and a precise next owner.

Never end a newly created proposal with "ready for implementation." Use
"proposal created; separate authoritative application, independent review, and
recording required." Recommend `story-readiness` only after read-only status has
verified APPLIED and CURRENT; never chain into `dev-story`.
