---
name: brainstorm
description: "Collaboratively authors or safely revises one game concept through user-owned decisions, section-scoped compare-and-set writes, bounded checkpoints, and a deterministic concept gate DAG."
---

# Brainstorm

This workflow facilitates product decisions; it does not make them for the user. It
creates or revises one game concept, records provenance and open questions, and stops.
It does not implement a game, choose an engine, publish market claims, produce a
formal schedule, or invoke a system-GDD review profile.

## Invocation

Accept exactly one mode:

~~~text
$brainstorm new --session-id <id> [--hint <text>] [--review full|lean|solo]
$brainstorm resume --concept design/gdd/game-concept.md --session-id <id> [--review full|lean|solo]
$brainstorm resume --checkpoint <checkpoint-path> --session-id <id> [--review full|lean|solo]
$brainstorm revise --concept design/gdd/game-concept.md --sections <stable-id[,stable-id...]> --session-id <id> [--review full|lean|solo]
~~~

Reject unknown/duplicate flags, missing values, unsafe paths, unsupported modes, and
review values outside `full`, `lean`, or `solo`. Session IDs are stable slugs or UUIDs,
not dates alone. Default review mode is `lean` only when `--review` is absent; never
read a newest session, latest concept, inferred review-mode file, or modification
time to choose state.

`new` requires the canonical concept target to be absent. If it exists, stop and show
the `resume`/`revise` forms. Existing-concept `resume` and `revise` require the
exact canonical path and its current raw-byte SHA-256. Checkpoint `resume` requires
one exact immutable checkpoint and revalidates whether its source concept was ABSENT
or hash-bound. Supply exactly one of `--concept` or `--checkpoint`; never silently
turn one mode into another.

## Authority, ownership, and write boundary

The user is the decision owner for concept selection, core fantasy, player experience,
core loop, pillars, anti-pillars, visual anchor, audience, platform intent, MVP, scope
tradeoffs, accepted concerns, and unresolved questions. Agents propose and review;
they never lock a product decision.

The brainstorm controller is the only writer of:

~~~text
production/brainstorm/<session-id>/session-manifest.md
production/brainstorm/<session-id>/checkpoints/<sequence>-<decision-id>.md
design/gdd/game-concept.md
~~~

No gate agent writes these files. This workflow never writes
`design/gdd/game-pillars.md`, an art bible, engine settings, production state, or any
other project artifact.

Use two explicit file boundaries:

1. **Checkpoint boundary** — after target validation, preview the exact session
   manifest/checkpoint root and obtain one bounded CREATE authorization unless the
   invocation already authorizes those exact files. This authority covers only
   immutable session/checkpoint files, not the concept.
2. **Concept boundary** — after the final section validation, show the complete
   concept CREATE or section-scoped MODIFY diff and obtain one authorization for
   that exact byte change. Product decisions collected earlier are not file
   authorization, and checkpoint approval is not concept-write approval.

Do not re-prompt per checkpoint or per section inside an unchanged authorized
boundary. A new path, newly selected section, changed source hash, or material scope
expansion requires a revised boundary. No approval authorizes implementation,
external research, publication, or downstream workflow execution.

## Canonical status vocabulary

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Mode` | `new`, `resume`, `revise` |
| `Section Status` | `PRESERVED`, `SELECTED`, `OPEN`, `DRAFT`, `LOCKED`, `CONFLICT` |
| `Gate Status` | `PASS`, `CONCERNS`, `REJECT`, `TIMEOUT`, `BLOCKED`, `ERROR`, `NOT_RUN_BY_MODE` |
| `Concept Review` | `CONCEPT READY`, `CONCEPT WITH DOCUMENTED CONCERNS`, `CONCEPT INCOMPLETE`, `BLOCKED` |
| `Document State` | `NEW DRAFT`, `RESUME DRAFT`, `REVISION DRAFT`, `READY TO WRITE`, `WRITTEN`, `UNCHANGED`, `CONFLICT` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

A workflow can be complete while explicitly open questions remain, but it cannot be
`CONCEPT READY` when a required section is empty, placeholder-only, contradictory,
or falsely stated as fact.

## Phase 0: Validate target, source bytes, and instructions

Resolve literal and real paths. Reject dot segments, symlink escapes, directories,
malformed IDs, unsupported encodings, path aliases, and paths outside the project
root. Read raw bytes once and compute full lowercase SHA-256.

For `new`:

- require `design/gdd/game-concept.md` to be absent;
- set the source concept state to `ABSENT`;
- do not delete, rename, or replace an existing file.

For existing-concept `resume` or `revise`:

- require exact path `design/gdd/game-concept.md`;
- capture the source concept raw SHA-256 and newline/encoding convention;
- parse its section manifest, stable headings, user-authored/custom sections,
  decision provenance, open questions, and gate evidence;
- reject duplicate stable section IDs, malformed ownership, or ambiguous headings;
- inventory any linked pillar/visual artifacts as read-only references only.

For checkpoint `resume`, require the exact checkpoint path to belong to the supplied
session ID, verify the full predecessor chain, and restore its recorded mode, source
path/hash-or-ABSENT, selected section set, draft snapshot and next step. If the
checkpoint says ABSENT, the canonical concept must still be absent; otherwise it
must still match the recorded raw hash.

Read the applicable AGENTS.md chain for the concept and checkpoint targets and bind
its paths/hashes to the session manifest. If source bytes or instructions cannot be
established, return `BLOCKED` and write nothing.

## Phase 1: Create the section and ownership manifest

Use these stable concept section IDs:

| Stable ID | Product owner | Purpose |
|---|---|---|
| `CONCEPT-CORE-IDENTITY` | user | title, elevator pitch, core fantasy and hook |
| `CONCEPT-PLAYER-EXPERIENCE` | user | desired emotion, player promise, motivation |
| `CONCEPT-CORE-LOOP` | user | moment, short-session, session and progression loops |
| `CONCEPT-PILLARS` | user | 3–5 pillars with definitions and decision tests |
| `CONCEPT-ANTI-PILLARS` | user | at least 3 explicit boundaries |
| `CONCEPT-AUDIENCE` | user | primary/secondary audience and exclusions |
| `CONCEPT-VISUAL-ANCHOR` | user | stable visual anchor ID, rule and principles |
| `CONCEPT-PLATFORM-CONSTRAINTS` | user | target intent and observed constraints |
| `CONCEPT-MVP` | user | smallest hypothesis-testing build |
| `CONCEPT-SCOPE-TIERS` | user | MVP, fallback and full-vision boundaries |
| `CONCEPT-RISKS` | user | design, technical, production and evidence risks |
| `CONCEPT-ASSUMPTIONS` | user | market, schedule, content and resource assumptions |
| `CONCEPT-OPEN-QUESTIONS` | user | explicitly unresolved decisions |
| `CONCEPT-PROVENANCE` | controller | decision/gate/source records only |

For each section record current heading, owner, source byte range, preimage hash,
status, selected-for-change flag, dependencies, decision IDs, and linked evidence.
Unknown custom sections receive stable preservation IDs and remain user-owned.

Mode rules:

- `new`: all required sections begin `OPEN`.
- `resume`: show the complete table and ask the user which `OPEN`/`DRAFT` sections to
  continue. Existing `LOCKED` sections are `PRESERVED` unless explicitly selected.
- `revise`: only IDs named by `--sections` become `SELECTED`. Reject unknown or
  duplicate IDs rather than broadening scope.
- In all modes, non-selected existing sections and custom prose must remain byte-for-
  byte unchanged. A selected section's dependencies are read-only context; selecting
  one does not silently select its dependents.

If `game-pillars.md` or another linked artifact disagrees with concept pillars, record
a conflict and owner. Do not synchronize or dual-write it.

## Phase 2: Immutable checkpoints and bounded context

After checkpoint authorization, create the session manifest and immutable checkpoints
after discovery, concept selection, core loop, pillars, every gate node, scope
decision, section review, and final write attempt.

Each checkpoint contains:

- session/mode/review values and predecessor path/hash;
- source concept path/hash or ABSENT;
- complete section/ownership/status table and selected IDs;
- stable decision ID, user-selected option, alternatives, rationale summary, and
  timestamp, excluding sensitive personal details not needed by the concept;
- draft snapshot hash, gate inputs/receipts/statuses, hypotheses/assumptions, and open
  questions;
- revision round counts, timeout/partial state, authorized paths, and next permitted
  step.

Never overwrite checkpoints. `resume` re-hashes the predecessor chain and source
concept. Continue only the first incomplete idempotent step. A missing predecessor,
changed source, altered selected set, or checkpoint collision returns `CONFLICT`.

Keep prompts and delegate context bounded to the current section, dependent section
hashes, user decisions, and explicit evidence. Do not send an unrestricted transcript.

## Phase 3: Collaborative discovery and concept selection

Ask conversational questions about desired experience, memorable play, taste,
avoided genres, team/resources, and practical constraints. Preserve free-text escape
paths; do not force a product decision into preset options.

Synthesize a Creative Brief and ask the user to:

- accept it;
- revise one named dimension;
- keep the draft/checkpoint and stop.

Allow at most two revision rounds for this decision. If it does not converge, write
the authorized checkpoint and return `STOPPED`, not an infinite loop.

Generate two to four structurally complete concepts; default to three unless the user
requests another number in that range. Each has:

- working title and 10-second elevator pitch;
- core verb, fantasy, hook and primary player experience;
- smallest testable loop;
- qualitative scope label;
- audience/market statement explicitly classified as sourced evidence, user
  assumption, model hypothesis, or unknown;
- biggest unanswered risk.

Ask the user to select one, combine named elements, request one fresh bounded round,
keep the checkpoint, or stop. Generate at most two concept rounds total. Record the
decision and alternatives; never pressure or silently select.

## Phase 4: Core loop, pillars, and boundaries

Develop the selected concept collaboratively:

- 30-second action and feel;
- five-minute choice/reward cycle;
- session loop and stopping point;
- progression/long-term completion;
- autonomy, competence and relatedness;
- 3–5 pillars with one-sentence definitions and concrete decision tests;
- at least 3 anti-pillars explaining the protected pillar.

At each product decision offer Accept, Revise one named part, Keep draft/checkpoint,
and Stop. Limit each decision family to two revisions. A third requested revision
saves a checkpoint and stops for a fresh session.

Pillars are authoritative in the concept. Linked pillar documents are derived
references and are not updated here.

## Phase 5: Audience, platform, scope, and evidence labels

Audience and market statements use one evidence label:

- `SOURCED CURRENT`: path/URL, publisher, observed date, relevant claim and snapshot
  hash are present;
- `USER ASSUMPTION`: the user supplied it;
- `MODEL HYPOTHESIS`: creative comparison only, not a market fact;
- `UNKNOWN`: no support.

Without current sources, audience size, comparable success, demand, price, platform
policy, or trend statements remain hypothesis/unknown. Do not fabricate citations or
write model intuition as authoritative validation.

Record platform targets, performance needs, distribution constraints, team experience
and user engine preference. Do not recommend an engine or state current engine/
platform support as fact. Set `Engine Decision: DEFERRED TO TECHNICAL SETUP` unless
the user records an existing preference, which remains a preference rather than a
technical recommendation.

Timeline, team capacity, content counts, cost, and delivery dates must be labeled
`USER BUDGET`, `USER ASSUMPTION`, `SOURCED ESTIMATE`, or `UNKNOWN`. Do not generate a
formal schedule or precise content promise from model judgment. Prepare preliminary MVP and scope constraints from those labels. After technical
feedback in the gate DAG, the user locks or revises the final scope tiers before the
PR-SCOPE node.

## Phase 6: Deterministic review-mode gate DAG

The DAG is sequential and hash-bound:

~~~text
CD-PILLARS
  -> AD-CONCEPT-VISUAL
  -> TD-FEASIBILITY
  -> PR-SCOPE
~~~

Never dispatch these four nodes in parallel. Each node receives the exact draft
snapshot hash, relevant stable section hashes, decision IDs, prior required gate
receipt, a bounded question, deadline, and attempt number. Each returns an immutable
receipt with gate ID, role, input hashes, start/end, verdict, concerns/rejection,
omissions, and receipt hash.

Mode matrix:

- `full`: all four nodes run in order and each downstream node waits for the current
  upstream disposition.
- `lean`: all four are `NOT_RUN_BY_MODE`; user-owned product decisions and the
  concept-specific review still apply.
- `solo`: all four are `NOT_RUN_BY_MODE`; spawn no gate agents.

### Node inputs and dependencies

1. `CD-PILLARS` consumes the chosen concept, core fantasy/hook, pillars, design tests,
   and anti-pillars.
2. `AD-CONCEPT-VISUAL` runs only after CD disposition and consumes confirmed pillar
   hashes. It proposes bounded visual directions; the user selects or describes the
   visual anchor.
3. `TD-FEASIBILITY` runs only after the visual-anchor decision and consumes core-loop,
   platform-intent, visual, MVP-risk, and assumption hashes. It records feasibility
   evidence/unknowns but never chooses an engine.
4. `PR-SCOPE` runs only after technical disposition and consumes MVP, fallback/full
   tiers, user resource/timeline assumptions, and technical concerns. It recommends
   scope risks but never approves scope for the user.

If an upstream section changes, mark that node and all downstream receipts `STALE`
and rerun them in order when full-mode gates remain required.

### Verdict semantics

- `PASS`: proceed to the next dependency.
- `CONCERNS`: keep the gate status as CONCERNS. The user may revise the named input,
  keep a checkpoint and stop, or explicitly document the concern and continue when
  the gate policy classifies concerns as advisory. Record owner, rationale, impact
  and review point. This is not PASS or an override.
- `REJECT`: do not write the final concept. There is no override path. The user may
  revise the rejected node's source sections and rerun that node, or checkpoint and
  stop.
- `TIMEOUT`, `BLOCKED`, `ERROR`, missing or partial receipt: return `Workflow Status:
  PARTIAL`, do not invent a verdict, do not run dependent nodes, and do not write the
  final concept.

Allow at most one retry per node and at most two user revision rounds for a rejected
or concerned node. On exhaustion, checkpoint and stop. A late result for an older
draft hash is stale and cannot unblock the DAG.

## Phase 7: Concept-specific read-only review

Review the exact final draft snapshot against this concept profile:

1. core identity is concise and internally consistent;
2. player promise, loops and motivations explain the intended experience;
3. pillars have definitions/tests and anti-pillars bound scope;
4. visual anchor has a stable ID, rule, principles, color philosophy and source
   decision;
5. audience, platform, market, engine, schedule and content statements have evidence
   labels rather than unsupported facts;
6. MVP tests the core uncertainty and scope tiers distinguish fallback/full vision;
7. risks, open questions, decision provenance and gate states are explicit;
8. required stable sections contain substantive content or an explicit open question;
9. no unresolved contradiction, placeholder token, fabricated citation, or stale gate
   receipt remains.

This is a concept-specific content review, not a system-design/GDD review. It is
read-only and cannot approve product decisions.

Return:

- `CONCEPT READY` when every required section is substantive or explicitly open,
  all statements are correctly labeled, full-mode gates pass or contain valid
  documented advisory concerns, and no REJECT/partial/stale required gate exists;
- `CONCEPT WITH DOCUMENTED CONCERNS` when only user-accepted advisory concerns remain;
- `CONCEPT INCOMPLETE` for placeholders, missing provenance/evidence labels, open
  blocking questions, or skipped required full-mode evidence;
- `BLOCKED` for a full-mode REJECT, conflict, unsafe target, or changed source hash.

## Phase 8: Preview, compare-and-set, and write

Only `CONCEPT READY` or `CONCEPT WITH DOCUMENTED CONCERNS` may enter the
concept-write boundary. `CONCEPT INCOMPLETE` checkpoints and stops without offering
a final concept write.

Build the exact target bytes and show:

- source path/hash or ABSENT;
- selected section IDs and their before/after hashes;
- byte-for-byte preserved section/custom ranges;
- complete unified diff, output hash, and one CREATE or MODIFY operation;
- unresolved open questions, documented concerns, and concept-review result.

For `new`, immediately before write confirm the target is still absent. For
`resume`/`revise`, re-read the source and require its raw SHA-256 to equal the Phase 0
preimage. Also verify every non-selected section hash. Any mismatch returns
`Document State: CONFLICT`, writes nothing, preserves both drafts in conversation/
checkpoint, and asks the user to merge in a new session.

Obtain one authorization for the exact displayed concept bytes. Write atomically,
re-read bytes, re-parse stable section IDs/provenance, confirm preserved sections,
and return the final SHA-256. Never replace the whole existing concept from
conversation memory.

If the exact output equals the source, return `Document State: UNCHANGED` and do not
write. Declined/failed authorization returns `Persistence: DECLINED` or `FAILED` and
does not change product decisions or source bytes.

## Output and stop

Always return:

- mode/session/review and source/output concept hashes;
- section owner/status/change table;
- user decision IDs and open questions;
- gate DAG statuses/input/receipt hashes and stale/partial rows;
- concept review, document state, workflow status and persistence;
- exact checkpoint/concept paths and next permitted action.

Recommend at most one next action selected from the concept state:

- unresolved product question -> continue this exact session;
- unproven core loop -> validate the core mechanic;
- complete concept with engine undecided -> perform technical setup;
- otherwise -> decompose the concept into systems;
- or `Stop`.

Do not invoke the recommendation, print a long pipeline, or claim formal market,
engine, feasibility, schedule, art, or release approval.

Verdict is `COMPLETE` only after an authorized atomic write/read-back or an explicitly
accepted unchanged result. REJECT, conflict or unsafe target is `BLOCKED`; missing/
timeout/partial required evidence is `PARTIAL`; user stop or bounded-loop exhaustion
is `STOPPED`.
