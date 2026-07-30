---
name: sprint-plan
description: "Create or update a sprint from registry-bound AUTHOR_COMPLETE stories with current persisted implementation-eligible readiness records, resolving carryover and deterministic dependency order before one revision-checked plan/tracker transaction."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


## Invocation and execution

Invoke this workflow as `$sprint-plan`.

Arguments: `[new|update] [--review full|lean|solo]`. With no mode, use `new`.
Treat bracketed values as optional unless the workflow says otherwise.

Before the first file change, present the complete proposed changeset, listing
every file and its exact proposed content or complete diff, and obtain one
explicit approval. After approval, make only those changes. If scope, candidate
bytes, findings, or target prior states change, stop, rebuild the complete preview,
and obtain new approval when the changeset changed materially.

This workflow owns only sprint planning. `$sprint-status` owns status reports.
It never creates or repairs epics, stories, GDD requirements, TR registry entries,
ADRs, readiness evidence, QA plans, or `production/review-mode.txt`.

---

## Phase 0: Parse arguments and enforce terminal branches

Parse arguments before reading project files or resolving review mode. Reject an
unknown mode, an unknown review value, or conflicting duplicate arguments with
**Verdict: BLOCKED** and zero gates and zero writes.

### Legacy `status` compatibility branch

If the first mode is the legacy value `status`:

1. Output: "`$sprint-plan status` is read-only status work and has moved to
   `$sprint-status`. Run `$sprint-status` instead."
2. Do not resolve review mode, load planning context, invoke readiness or director
   gates, prepare a changeset, create a directory, or write any file.
3. Assert `gate_count == 0` and `write_count == 0`.
4. **STOP.** This is a terminal branch and cannot enter any later phase.

For `new` and `update`, initialize an in-memory mutation ledger with
`gate_count = 0`, `producer_rerun_count = 0`, `write_count = 0`, and an empty
authorized path set. The ledger is diagnostic state only and is never persisted.

---

## Phase 1: Resolve review mode once, without configuration writes

Resolve one review mode and keep it unchanged for the whole run:

1. If `--review full|lean|solo` was passed, use it. Do not replace it with a
   value read from disk.
2. Otherwise, if `production/review-mode.txt` exists and contains exactly one of
   `full`, `lean`, or `solo`, use that value.
3. Otherwise, use `lean` for this run and report that the configuration is
   missing or invalid.

Never create or edit `production/review-mode.txt` during sprint planning. Setting
or repairing the persistent review mode is a separate, explicitly authorized
task. The review-mode file is never part of the sprint changeset, so declining a
sprint cannot leave a review-mode side effect.

Use the resolved mode when validating readiness-record currentness and for
PR-SPRINT. See `.codex/docs/director-gates.md` for gate semantics.

---

## Phase 2: Load authoritative planning inputs

All work in this phase is read-only.

### 2.1 Milestone, capacity, history, and stable sprint identity

Read:

- the current milestone from `production/milestones/`;
- `production/sprints/` and `production/sprint-status.yaml`, when present;
- `production/session-state/active.md`, when present;
- any versioned project-stage or current-milestone declaration that explicitly
  carries `active_sprint_id`;
- one current owner-issued capacity receipt with stable ID/path/revision/declared revision,
  exact estimate unit, total/reserved/released values, and estimates in that unit;
  and
- the latest relevant risk register entries under `production/risk-register/`.

Treat a missing `production/sprints/` directory as empty history for `new`.
Never choose a sprint from modification time, directory order, a phrase such as
"most recent", or the greatest number alone.

For `update`, collect every explicit `active_sprint_id` from the tracker, active
session, project-stage declaration, and current milestone. A valid identifier is
exactly `sprint-[NNN]`. Ignore a source only when it has no sprint declaration;
do not ignore a malformed declaration. The update is eligible only when all
present well-formed declarations resolve to exactly one identical stable ID,
exactly one canonical plan declares that `sprint_id`, and the tracker declares
both `sprint_id` and `active_sprint_id` equal to it. Zero IDs, conflicting IDs,
malformed IDs, duplicate plan matches, a missing tracker, or a missing matching
plan is **BLOCKED**. Report every selector source and value; ask for correction
instead of guessing.

For `new`, the existing active tracker identifies the previous sprint only when
its stable IDs and matching plan agree. If history exists but previous-sprint
identity is ambiguous, stop before carryover selection. Derive the proposed new
number only after the authoritative previous identity and all existing declared
sprint IDs are known; collision with any existing plan is **BLOCKED**.

Capture the exact declared revision of every selector, plan, and tracker used.

### 2.2 Consume the canonical story registry and story artifacts

The only source of sprint work is a sibling `STORIES.md` current registry produced
by the story authoring workflow. Enumerate only
`production/epics/*/STORIES.md`; each consumed registry must declare exact schema
`cgs.story-registry/v2`, one stable epic identity, a positive monotonic registry
revision, prior/current payload revisions, and an internally consistent Current Story
Registry plus append-only identity/history ledgers. `EPIC.md` remains a read-only
source named by the registry; its former `## Stories` table is not a sprint
registry and its row status is never an eligibility predicate.

A current registry row is structurally valid only when all of the following hold:

- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
  priority, dependency IDs, and current author status are present and unique;
- the path is a direct-child `story-NNN-<slug>.md` regular file under the same
  canonical `production/epics/<epic-slug>/` root, with no traversal, symlink,
  case-fold, ID, slot, or path collision;
- the file declares exact schema `cgs.story/v2`, the same Story ID, slot, epic ID,
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- its exact declared revision and declared Story Core revision reproduce; and
- registry payload/ledger revisions and the referenced EPIC/create-stories receipt
  identities are current and internally consistent.

Use the registry's stable Story ID verbatim as tracker `story_id`; store the exact
canonical project-relative path separately. Never derive identity from epic slug,
story number, title, GDD prose, acceptance criterion, filename, or a planning-time
task. A rename, slot reuse, or conflicting path is an upstream identity event;
sprint-plan must not repair or silently rewrite it.

Malformed, stale, conflicting, duplicate, unsafe, or unresolvable registry/story
evidence is reported and excluded. Corrupt registry ownership or ledgers block the
affected epic. If a bad row is required by a dependency, requested update, active
tracker entry, or carryover decision, stop with **Verdict: BLOCKED**.

### 2.3 Require persisted implementation-eligible readiness

A valid registry row becomes an eligible new candidate only when:

1. the registry and exact `cgs.story/v2` artifact both say
   `Story Status: AUTHOR_COMPLETE`;
2. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
3. Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
4. that record has final verdict `READY`, complete evaluation state, persistence
   state `PERSISTED`, and `implementation_gate_eligible: true`;
5. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
6. immediate re-read/re-read of the story, `STORIES.md`, readiness record,
   recorder receipt, readiness registry, and every stale-key source reproduces all
   captured values. Any change makes the item ineligible until independently
   reevaluated and recorded.

Sprint-plan is only a consumer. It never invokes `$story-readiness`, simulates or
invokes `cgs.story-readiness-recorder/v1`, persists a record, upgrades a verdict,
or treats a conversational/candidate `READY` as implementation authorization.
A record candidate with `NOT_PERSISTED` or `implementation_gate_eligible: false`,
a bare verdict, missing receipt, stale source, mismatched review mode, or user risk
acceptance is insufficient.

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Non-AUTHOR_COMPLETE, non-READY, unpersisted, ineligible, or stale rows remain
visible as exact exclusions but cannot enter proposed additions. If no eligible
new candidate exists for `new`, output "No implementation-gate-eligible stories
in the existing registry", recommend `$create-stories` for authoring gaps and the
catalog-declared readiness evaluation plus independent recorder for readiness
gaps, then finish **BLOCKED** with zero producer gates and zero writes.

Existing tracked items retained by `update`, or explicitly carried from the
previous sprint, are not new candidates. Preserve their lifecycle status, but
verify stable ID/path/current story bytes against `STORIES.md` and the originally
admitted readiness record/receipt. A changed source or identity blocks silent
carry/update; never reset an in-progress, review, done, or blocked item to ready.

### 2.4 GDD boundary

GDDs are read-only validation sources only through the exact current story and
persisted readiness record's source/stale-key closure. Never scan `design/gdd/` for "ready features",
turn GDD prose into sprint tasks, invent acceptance criteria, or add a work item
that has no valid existing registry row and story file.

### 2.5 Capture tracker recorder preconditions

`production/sprint-status.yaml` has one logical recorder. No workflow may replace
it directly. Sprint-plan calls the recorder contract for sprint creation and scope
changes; lifecycle workflows call the same contract only for their owned status
fields. The recorder requires an exact compare-and-swap tuple:

```text
expected_tracker_revision
expected_tracker_revision
expected_plan_revision
expected_story_set_revision
requested_field_owners
event_id
```

For an absent tracker, the expected state is `ABSENT` and the candidate
starts at `tracker_revision: 1`. For an existing tracker, require a positive
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
`plan_revision` and `story_set_revision` to match the selected plan before drafting.
The candidate increments the revision by exactly one. `event_id` is unique and
stable across retries. Reusing an event with different requested bytes, bypassing
the recorder, an unknown field owner, or any expected/current mismatch is
**BLOCKED**; it must never be resolved by last-writer-wins.

Sprint-plan owns sprint identity, dates, goal, selected story set, canonical
paths, priority, estimates, dependency order, and planning revisions. Lifecycle
workflows own only allowed status-transition fields. A recorder request that
crosses those field boundaries is **BLOCKED**.

---

## Phase 3: Resolve carryover, select scope, and render both drafts

### 3.1 New-sprint carryover is a mandatory decision table

Compare the authoritative previous plan with its applicable tracker. Every
planned item whose tracker lifecycle status is not `done` is open. Missing or
extra tracker rows, duplicate IDs, a stale tracker, or a story path that no longer
matches the registry is **BLOCKED** before asking for a carryover decision.

Show each open item with stable `story_id`, canonical path, origin sprint,
current status, estimate, dependencies, and blocker. Require exactly one explicit
decision per item:

- `carry`: include it in the new sprint, preserve its original `origin_sprint`,
  canonical path, current lifecycle status, and remaining-work estimate;
- `defer`: exclude it from the new tracker and record the deferral reason in the
  new plan's carryover decision table; or
- `cancel from sprint scope`: exclude it and record the reason, without changing
  the story artifact or claiming the underlying story is cancelled.

Blank, inferred, bulk-defaulted, or contradictory decisions are invalid. The
decision table is part of the frozen planning payload. A carried item is marked
`[CARRY]`; it is never reset to `ready_for_dev`. Defer/cancel decisions do not
authorize edits to the previous tracker or story.

### 3.2 Deterministic dependency/layer/priority/capacity selection

Validate the dependency graph over eligible candidates, carried items, and
already-done prerequisites. Each dependency must resolve to one stable story ID.
A missing dependency, self-edge, cycle, dependency on an excluded unresolved
story, or a dependent whose prerequisite would not be done or earlier in the
proposed sprint is **BLOCKED**; never break a cycle or dependency by priority.

Select and order work with this exact algorithm:

1. Seed the ordered set with carried items in dependency-valid order while
   preserving their lifecycle state and origin.
2. Build a topological frontier of eligible new candidates whose prerequisites
   are already done or already ordered.
3. Within each frontier choose lower layer rank first:
   `Foundation < Core < Feature < Presentation`.
4. Within equal layer choose project priority:
   `must_have < should_have < could_have`.
5. Break remaining ties by stable `story_id` code-point order.
6. Add a candidate only when its estimate fits remaining capacity in the one
   established capacity unit. Recompute the frontier after each addition.

Normalize only authoring priority `must-have` to plan `must_have`,
`should-have` to `should_have`, and `nice-to-have` to `could_have`; record the
source spelling and mapping provenance. Any other spelling is **BLOCKED**. Unknown
or mixed estimate/capacity units make feasibility **BLOCKED**. An item
that does not fit remains an explicit capacity exclusion; do not skip a required
prerequisite and admit its dependent, split stories, alter estimates, or invent
work to fill unused capacity. Record the ordered candidate manifest and every
dependency/readiness/capacity exclusion.

### 3.3 Update sprint

Start only from the stable active plan/tracker pair resolved in Phase 2.1. Show
current items and statuses, then gather requested additions, removals,
reprioritization, or re-estimation. Every addition must pass Phase 2.3 and the
same graph/order/capacity algorithm in Phase 3.2. Preserve existing statuses.
Only not-started items (`backlog` or canonical `ready_for_dev`) may be removed or freely
reprioritized; otherwise ask the user to retain them or use the lifecycle owner.

### 3.4 Render the sprint plan

Render the complete Markdown candidate in memory:

````markdown
# Sprint [N] — [start_date] to [end_date]

## Machine-readable Plan Record

```yaml
schema_version: "cgs.sprint-plan/v2"
sprint_id: "sprint-[NNN]"
plan_revision: "[positive integer]"
story_set_revision: "[positive integer]"
tracker_revision: [positive integer]
updated_at: "[ISO-8601 instant with offset]"
goal: "[sprint goal]"
start_date: "[YYYY-MM-DD]"
end_date: "[YYYY-MM-DD]"
timezone: "[IANA timezone]"
estimate_unit: "[one exact project-supported unit]"
capacity:
  receipt_id: "[stable capacity receipt ID]"
  receipt_path: "[canonical project-relative path]"
  receipt_revision: [positive integer]
  receipt_revision: [positive integer]
  unit: "[same exact value as estimate_unit]"
  total: [non-negative integer]
  committed: [sum of selected story estimates]
  reserved: [non-negative integer]
  released: [non-negative integer]
  remaining: [total - committed - reserved + released]
stories:
  - story_id: "STORY-0123456789abcdef"
    file: "production/epics/[epic-slug]/story-[NNN]-[slug].md"
    registry_revision: [positive integer]
    registry_payload_revision: [positive integer]
    author_status: "AUTHOR_COMPLETE"
    story_revision: [positive integer]
    priority: "must_have"
    source_priority: "must-have"
    estimate: [non-negative integer]
    owner: "[owner or UNKNOWN]"
    dependencies: []
    source_revision: [positive integer]
    story_core_revision: [positive integer]
    readiness_record_id: "[stable record ID]"
    readiness_record_revision: [positive integer]
    readiness_receipt_id: "[stable recorder receipt ID]"
    readiness_receipt_revision: [positive integer]
    implementation_gate_eligible: true
```

## Sprint Goal
[One sentence tied to the current milestone]

## Capacity
- Unit: [the exact estimate_unit above]
- Total: [X]
- Committed: [C]
- Reserved / Buffer: [R]
- Released: [L]
- Remaining: [Total - Committed - Reserved + Released]

## Work Items
| Order | Story ID | Story | File | Layer | Priority | Owner | Estimate | Dependencies | Source revision |
|---:|---|---|---|---|---|---|---:|---|---|
| 1 | STORY-0123456789abcdef | [existing title] | `production/epics/[epic-slug]/story-[NNN]-[slug].md` | Foundation | must_have | [owner] | [integer] | [stable STORY-* IDs or None] | `<declared revision>` |

## Carryover Decisions
| Story ID | Origin Sprint | Current Status | Decision | Reason |
|---|---|---|---|---|

## Exclusions
| Story ID | Reason | Dependency / Capacity Evidence |
|---|---|---|

## Implementation Eligibility Evidence
| Story ID | Author Status | Story revision / Core revision | Readiness Record ID / revision | Recorder Receipt ID / revision | Eligible |
|---|---|---|---|---|---|

## QA Plan
[path and coverage note, or the exact missing-QA warning from Phase 4]

## Producer Findings
| Finding ID | Verdict | Evidence | Disposition |
|---|---|---|---|

## Risks
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|

## Definition of Done for this Sprint
- [ ] Every delivered work item satisfies its story acceptance criteria
- [ ] Required automated tests or manual evidence pass
- [ ] QA plan requirements and smoke checks pass
- [ ] QA sign-off has no unresolved S1 or S2 defect
- [ ] Required design deviations and reviews are recorded
````

The `cgs.sprint-plan/v2` record is the normative machine-readable plan. Every
human table is a derived view and must agree with it exactly. The plan references
existing stories; it does not copy, rewrite, or extend their acceptance criteria.

### 3.5 Render the tracker through the recorder contract

Render `production/sprint-status.yaml` in memory from the same ordered work-item
set. Keep priority separate from lifecycle status. Every newly selected candidate
starts as `ready_for_dev`; preserve retained and carried statuses together with
their exact status-update timestamp/provenance.

```yaml
# Generated through the sprint tracker recorder; direct replacement is forbidden.
schema_version: "cgs.sprint-tracker/v2"
tracker_revision: [positive integer]
event_id: "sprint-plan/[sprint-id]/[stable operation id]"
sprint_id: "sprint-[NNN]"
active_sprint_id: "sprint-[NNN]"
sprint_state: "ACTIVE"
lifecycle_owner: "[stable authority/owner ID]"
lifecycle_recorder: "cgs.sprint-tracker/v2"
plan_file: "production/sprints/sprint-[NNN].md"
plan_revision: [positive integer]
plan_revision: "[positive integer]"
story_set_revision: "[positive integer]"
updated_at: "[ISO-8601 timestamp with timezone]"
goal: "[sprint goal]"
start_date: "[YYYY-MM-DD]"
end_date: "[YYYY-MM-DD]"
timezone: "[IANA timezone]"
estimate_unit: "[same exact unit as plan]"
capacity:
  receipt_id: "[same stable capacity receipt ID as plan]"
  receipt_path: "[same canonical project-relative path as plan]"
  receipt_revision: [same positive integer as plan]
  receipt_revision: [same positive integer as plan receipt]
  unit: "[same exact value as plan estimate_unit]"
  total: [same non-negative integer as plan]
  committed: [same selected-estimate sum as plan]
  reserved: [same non-negative integer as plan]
  released: [same non-negative integer as plan]
  remaining: [same recomputed value as plan]
qa_plan: "[canonical path or MISSING]"

stories:
  - story_id: "STORY-0123456789abcdef"
    name: "[existing story title]"
    file: "production/epics/[epic-slug]/story-[NNN]-[slug].md"
    order: 1
    layer: "[Foundation|Core|Feature|Presentation]"
    priority: "must_have"
    source_priority: "must-have"
    status: "ready_for_dev"
    status_updated_at: "[same activation instant as top-level updated_at]"
    status_update_provenance:
      event_id: "sprint-plan/[sprint-id]/[stable operation id]"
      recorder: "cgs.sprint-tracker/v2"
      reason: "initial sprint admission"
      prior_status: "ABSENT"
      source_story_revision: [positive integer]
    story_schema: "cgs.story/v2"
    author_status: "AUTHOR_COMPLETE"
    story_revision: [positive integer]
    source_revision: [positive integer]
    story_core_revision: [positive integer]
    readiness_verdict: "READY"
    readiness_review_mode: "[full|lean|solo]"
    readiness_record_id: "[stable record ID]"
    readiness_record_revision: [positive integer]
    readiness_key: "[stable readiness key]"
    readiness_stale_key: "[current stale key]"
    readiness_receipt_id: "[stable recorder receipt ID]"
    readiness_receipt_revision: [positive integer]
    implementation_gate_eligible: true
    origin_sprint: ""
    owner: ""
    estimate: [non-negative integer]
    dependencies: []
    blocker: ""
    completed: ""
```

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

After QA findings, producer findings/dispositions, carryover decisions, and all
scope values are resolved, assign the next positive `plan_revision` through the
single recorder. The plan and tracker must agree on sprint identity, dates, goal,
capacity, ordered work items, provenance, source record IDs/revisions, carryover,
exclusions, QA state, risks, findings, and tracker revision. Use one exact
`updated_at` in both files. Re-render both drafts before preview; any later
material change requires a new preview and authorization.

---

## Phase 4: Resolve QA-plan findings before authorization

Still without writing, search `production/qa/` for the canonical QA plan for the
stable sprint ID or one unambiguous QA plan that declares that ID.

- If found, read it, record its canonical path and coverage in both drafts, and
  proceed.
- If absent or ambiguous, surface the finding and ask:
  - `[A] Pause and run $qa-plan sprint first (Recommended)`
  - `[B] Continue with an explicit missing-QA warning`

If `[A]`, discard the write candidate and finish **BLOCKED — QA plan required
before sprint activation** with zero writes. If `[B]`, add this exact block to
the Markdown draft before any producer gate or changeset preview:

```markdown
> ⚠️ **No QA Plan**: This sprint is being activated without a QA plan. Run
> `$qa-plan sprint` before implementation. Production → Polish QA sign-off is
> blocked until a sprint QA plan exists.
```

Also set tracker `qa_plan: "MISSING"`. The choice is part of scope resolution,
not permission to write. No QA finding or warning may be appended after approval
or after either target is written.

---

## Phase 5: Bounded producer feasibility gate before authorization

The gate input is the full current Markdown/YAML draft, including stable sprint
selectors, deterministic order, readiness revisions, carryover decisions, exclusions,
recorder preconditions, and QA finding.

- `solo`: do not spawn; report `[PR-SPRINT] skipped — Solo mode`.
- `lean`: do not spawn; report `[PR-SPRINT] skipped — Lean mode`.
- `full`: spawn `producer` through Codex subagent delegation using **PR-SPRINT**
  from `.codex/docs/director-gates.md`, increment `gate_count`, and await it.

Require every producer finding to have a stable ID `PR-SPRINT-[NNN]`, verdict,
specific evidence, affected story IDs or capacity field, and one requested
disposition. Reject a missing, malformed, duplicate, or evidence-free finding as
**BLOCKED**. Preserve the same finding ID when the same concern appears on rerun;
never renumber findings to make an unresolved concern appear new or resolved.

On the first result:

- `REALISTIC`: proceed with all finding IDs/dispositions recorded.
- `CONCERNS`: show each finding. The user may explicitly accept every concern as
  risk, stop, or authorize one directed scope/capacity revision.
- `UNREALISTIC`: do not write. The user may stop or authorize one directed
  scope/capacity revision addressing the identified findings.
- Missing, failed, malformed, or unrecognized verdict: finish **BLOCKED**.

At most one directed revision and one PR-SPRINT rerun are allowed. Before the
rerun, increment `producer_rerun_count` to 1, revalidate every affected story,
dependency, capacity, carryover, and QA condition, then re-render both drafts.
Pass the prior finding IDs and their dispositions to the rerun. The rerun must
return `REALISTIC`; `CONCERNS`, `UNREALISTIC`, malformed output, a second revision
request, or `producer_rerun_count > 1` is **BLOCKED** with zero final-target
writes. This workflow never loops until a favorable verdict.

Gate output, accepted first-pass concerns, and stable finding dispositions must
all appear in the drafts before the final changeset is frozen.

---

## Phase 6: Freeze, preview, authorize, and atomically record

### 6.1 Freeze and preview

Freeze the exact UTF-8 bytes for:

- `production/sprints/sprint-[NNN].md`; and
- `production/sprint-status.yaml`.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
each frozen candidate. For an existing tracker also show the exact recorder atomic conflict check
tuple from Phase 2.5. Present one complete changeset preview containing both
paths, prior states, candidate revisions, and complete new content or complete unified
diff. State that no other file, including `production/review-mode.txt`, changes.

Obtain one explicit authorization for this exact pair. If declined, write
nothing and finish **BLOCKED — changeset not authorized**. Authorization of an
earlier draft does not authorize a later warning, finding, story revision, recorder
revision, or scope change.

### 6.2 Compare-and-swap preconditions

Immediately before the first mutation, perform one read-only preflight:

- every selected/carryover story still exists at its canonical path, remains the
  same current `cgs.story-registry/v2` row and `cgs.story/v2` artifact, and matches
  the previewed raw/core revisions;
- every readiness record, recorder receipt, readiness-registry revision/head, and
  stale-key source remains current and still proves
  `implementation_gate_eligible: true`;
- the capacity receipt still has the previewed ID/path/revision/declared revision/unit and
  operands, and its remaining-capacity equation still reproduces;
- every active sprint selector still has its previewed revision and value;
- both plan/tracker targets still match their previewed prior states or remain absent;
- the current tracker still matches the expected tracker revision, declared revision,
  plan revision, and story-set revision;
- the `event_id` is unused or is an exact idempotent replay of the same bytes; and
- the plan/tracker candidates still have identical ordered work-item sets.
- both candidates still declare their exact schema versions and identical
  `start_date`, `end_date`, `timezone`, `estimate_unit`, `ACTIVE` identity, and
  capacity receipt/operand values.

If any precondition changed, write nothing. Return to the relevant read-only
phase, rebuild both drafts, re-run invalidated checks, and re-preview. Materially
different bytes require new authorization. Never overwrite a newer tracker.

### 6.3 Atomic plan write and single-recorder tracker commit

Treat the plan and recorder commit as one transaction:

1. Create same-directory temporary siblings containing only the authorized
   candidate bytes; increment `write_count` only for authorized transaction writes.
2. Re-read temporary files and verify their revisions against the preview.
3. Recheck all prior states and the recorder atomic conflict check tuple once more.
4. Replace the plan and commit the tracker through the one recorder while keeping
   both captured prior states until both operations verify.
5. If replacement, recorder commit, or verification fails, restore both prior states
   (or remove only a newly created target), report every path that may have
   changed, and finish **BLOCKED**. Never report one-file success as COMPLETE.
6. Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Do not write either final target before QA resolution, the bounded producer gate,
complete preview, and authorization have all resolved.

---

## Phase 7: Verdict and handoff

Emit **Verdict: COMPLETE** only after both authorized final files exist and pass
exact revision/identity/revision verification. Report final revisions, previous and new
tracker revisions, recorder event ID, producer rerun count, and counts of selected,
carried, deferred, cancelled-from-scope, and excluded work items.

Then suggest only applicable next steps:

- `$qa-plan sprint` first when `qa_plan: MISSING`;
- the catalog-declared readiness evaluation, followed by separately authorized
  readiness recording, when an AUTHOR_COMPLETE story lacks current persisted
  implementation eligibility;
- `$dev-story [story-path]` only for a still-current
  `implementation_gate_eligible: true` work item; and
- `$sprint-status` for all status reporting.

Other terminal results are explicit:

- **Verdict: BLOCKED** — no current persisted implementation-gate-eligible
  candidate, invalid registry/story/readiness identity,
  unresolved carryover, dependency/capacity failure, ambiguous active sprint,
  recorder conflict, unresolved producer rerun, QA blocker, changed precondition,
  declined authorization, or failed atomic verification.
- **Verdict: COMPLETE — no changes required** — `update` renders byte-identical
  plan/tracker state and verifies both current files; no write occurs.

In every terminal branch, report `gate_count`, `producer_rerun_count`,
`write_count`, and all paths written. The legacy `status` branch always reports
zero gates and zero writes.
