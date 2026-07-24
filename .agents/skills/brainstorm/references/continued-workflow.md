# Brainstorm — Required workflow continuation

This file is normative. It begins only after the main skill validated
`cgs.brainstorm-request/v2`, inventoried exact target/sections, established one
mutation boundary, loaded bounded ideation context, and initialized the
`cgs.brainstorm-checkpoint/v2` chain.

## Phase 4: Bounded discovery, ideation, and user-owned selection

### Common decision provenance

Every material concept statement references a stable
`BRSDEC-<concept-id>-<NNN>` record using the shared authoring classes:

| Class | Authority and treatment |
|---|---|
| `product-choice` | Named product owner selects an experience/fantasy/loop/pillar/visual/audience/platform-intent/MVP/scope/risk/deferral option after tradeoffs. |
| `evidence-backed-hard-constraint` | Current owned evidence directly constrains the concept; record stable owner/path-or-URL/locator/hash/observed date and do not ask the user to vote it away. |
| `derived-design-constraint` | Author derives a concept implication from accepted choices/current evidence; show derivation/assumptions and require product-owner acceptance. |
| `technical-handoff` | Engine/platform feasibility, architecture, formal estimate, implementation, test, or production question is routed to its external owner and stays out of authoritative concept truth. |

Record:

    id: BRSDEC-<concept-id>-<NNN>
    section_ids: []
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    owner: <actual user/named owner/source owner>
    recorder_task_id: <actual author task>
    question: <bounded decision/question>
    options: [{id, value, tradeoffs, evidence_refs}]
    selected: <option / hard constraint / routed destination>
    rationale: <owner rationale or derivation>
    source_refs: [{id, owner, path_or_url, locator, sha256, observed_at}]
    assumptions: []
    dependent_assertion_ids: []
    status: ACCEPTED | PROVISIONAL | ROUTED | SUPERSEDED
    accepted_at_utc: <RFC3339 seconds Z | null>

Never label author/gate/model output as a user decision. Never store sensitive
personal preference details that are unnecessary to the concept.

### Discovery brief convergence

Ask conversational questions about desired experience, memorable play, taste,
avoided genres, resources, constraints, and non-negotiables. Preserve free-text
escape paths.

Synthesize one Creative Brief. At every convergence prompt present:

1. Accept;
2. Revise one named dimension;
3. Keep current draft/checkpoint and stop; or
4. Stop without changing target.

Allow at most two brief revision rounds in one run. A third revision request
appends a safe checkpoint and returns `STOPPED — REVISION_LIMIT`, preserving the
draft and one exact resume step. Never loop until acceptance.

### Ideation rounds and selection

Generate two to four proposals per round, default three, and at most two rounds.
Each proposal is structurally comparable and contains:

- stable proposal ID, working title, ten-second pitch, core verb/fantasy/hook;
- primary player experience and smallest testable loop;
- qualitative scope tier, biggest uncertainty, and strongest anti-goal;
- audience/market statement labeled current evidence, user assumption, model
  hypothesis, or unknown; and
- explicit differences/tradeoffs rather than superficial reskins.

The product owner may select one, combine named elements, request one fresh
bounded round, keep checkpoint/stop, or stop. Combination identifies exact source
proposal elements and creates a new selected-proposal ID; the author never
silently blends or chooses. After the second rejected round, checkpoint and stop.

Persist `BRSIDEA` proposal hashes and the `BRSDEC` selection with alternatives and
rationale. Selection is product approval of direction, not file authorization,
concept completeness, independent review, or formal approval.

## Phase 5: Develop the selected concept and label evidence

For every selected section follow:

    Bounded Context -> Decision Classification -> Question -> Options
    -> User Decision -> Draft -> Assertion Preflight -> Exact-Body Approval

At each decision family offer Accept, Revise one named part, Keep checkpoint and
stop, or Stop. Permit at most two revisions for that family in the run. Exhaustion
appends checkpoint and returns STOPPED; it never implies acceptance.

Develop:

- moment-to-moment action/feel, five-minute choice/reward cycle, session loop/
  stopping point, and progression/long-term completion;
- intended autonomy, competence, relatedness, emotion, promise, and motivation;
- three to five pillars with definitions and concrete decision tests;
- at least three anti-pillars naming the protected pillar/boundary;
- audience intent/exclusions, platform intent, visual anchor, MVP uncertainty
  test, fallback/MVP/full scope tiers, risks, assumptions, and open questions.

Pillars in the concept are authoritative for this artifact. Linked pillar files
remain read-only derived references and are never synchronized here.

### Market and audience evidence

Use one label per market/audience/comparable/demand/price/trend claim:

- `SOURCED_CURRENT`: `cgs.brainstorm-research-receipt/v1` includes URL/source,
  publisher, claim locator, published/updated date when available, observed-at
  UTC, relevant bounded claim, snapshot/content hash, and researcher identity;
- `USER_ASSUMPTION`: actual product owner supplied the assumption;
- `MODEL_HYPOTHESIS`: creative hypothesis only, explicitly not validation; or
- `UNKNOWN`: evidence unavailable/insufficient/conflicting.

`research_mode: none` never researches. `receipts-only` trusts no claim beyond
the exact current declared receipt. `authorized-current` may perform only the
authorized bounded research questions and must persist receipts before use.
Missing/stale/conflicting source evidence becomes hypothesis/unknown or a finding;
never fabricate citations, audience size, comparable success, demand, policy,
price, or trend facts.

### Platform and engine ownership

Record user platform intent, performance/distribution constraints, team
experience, and user engine preference. A preference remains a product preference,
not a technical recommendation. Without current owned evidence, platform support/
policy/certification statements are UNKNOWN.

Write `Engine Decision: DEFERRED TO SETUP-ENGINE` unless an already accepted
external engine-selection receipt is supplied. Brainstorm never recommends,
selects, installs, or configures an engine. Feasibility questions use
`technical-handoff` with exact destination/needed evidence.

### Timeline, capacity, content, and estimate ownership

Label every duration/date/team-capacity/content-count/cost statement:

- `USER BUDGET` or `USER ASSUMPTION` with actual owner;
- `SOURCED ESTIMATE` only from exact current `cgs.estimate-evidence/v1` path/hash,
  scope/profile/units/assumptions, estimator identity, and confidence; or
- `UNKNOWN`.

Model intuition never becomes an X–Y month range, delivery date, staffing promise,
or content commitment. Route formal estimation to the estimate owner after the
concept; do not invoke it here. MVP/scope tiers may use qualitative bounds while
assumptions remain explicit.

## Phase 6: cgs.game-concept-content-profile/v2 assertions

Each assertion records stable ID, applicability, PASS/FAIL, evidence/decision IDs,
owner, and failure reason. Heading presence or non-placeholder prose is never
sufficient.

### Core identity and experience

- `GCC-CORE-01`: title/pitch/fantasy/hook form one distinguishable identity;
- `GCC-CORE-02`: pitch is concise and names player action/value, not marketing fact;
- `GCC-EXP-01`: emotion, promise, motivation, and intended agency are explicit;
- `GCC-EXP-02`: experience claims trace to product-owner decisions.

### Loop, pillars, and boundaries

- `GCC-LOOP-01`: moment, short, session, and progression loops each name action,
  feedback/reward, choice, transition, and stopping/continuation condition;
- `GCC-LOOP-02`: smallest testable loop exposes the core uncertainty;
- `GCC-PIL-01`: three to five nonduplicate pillars have definitions and observable
  decision tests;
- `GCC-PIL-02`: at least three anti-pillars state prohibited direction and protected
  pillar/value;
- `GCC-PIL-03`: linked pillar conflicts have owner/finding; no dual-write.

### Audience, visual, and platform

- `GCC-AUD-01`: primary/secondary audience intent and exclusions are explicit;
- `GCC-AUD-02`: every market/audience fact has a permitted evidence label/current
  receipt or is hypothesis/unknown;
- `GCC-VIS-01`: visual anchor has stable ID, one rule, principles, color/mood/shape
  intent, prohibited imitation, and source decision;
- `GCC-VIS-02`: visual anchor is a concept constraint, not an art-bible substitute;
- `GCC-PLAT-01`: platform intent is separated from current technical facts;
- `GCC-PLAT-02`: engine choice is preference/external receipt/deferred, never author
  recommendation.

### MVP, scope, risks, assumptions, and questions

- `GCC-MVP-01`: MVP is the smallest build/testing concept that tests one named core
  uncertainty and excludes nonessential content;
- `GCC-SCOPE-01`: fallback/MVP/full tiers have qualitative boundaries, dependencies,
  and user-owned tradeoffs;
- `GCC-RISK-01`: design, technical, production, market/evidence risks have owner,
  impact, signal, and mitigation/next evidence;
- `GCC-ASM-01`: market/platform/schedule/content/resource statements use permitted
  owner/evidence labels and units;
- `GCC-OPEN-01`: every open question has stable ID, owner, impact, blocking flag,
  evidence/decision needed, and review point; explicit `none` is permitted;
- `GCC-OPEN-02`: only explicitly deferred nonblocking questions may remain for
  CONTENT_COMPLETE; blocking questions prevent it.

### Provenance and whole-concept consistency

- `GCC-PROV-01`: every material product statement traces to accepted BRSDEC IDs;
- `GCC-PROV-02`: proposal/selection, exact-body approvals, sources, gates,
  revisions, and author identities are current and noncontradictory;
- `GCC-WHOLE-01`: identity/experience/loop/pillars/audience/visual/platform/MVP/
  scope/risks/assumptions/questions agree across sections;
- `GCC-WHOLE-02`: no placeholder, fabricated citation, unlabeled estimate,
  unsupported platform/engine fact, stale required gate, or copied external truth.

Unknown/custom section bytes are preserved and may receive advisory checks, but
cannot silently satisfy a missing canonical section.

## Phase 7: Deterministic bounded advisory gate DAG

These nodes are read-only consultations, not product owners, independent concept
review, approval, or target writers:

    CD-PILLARS -> AD-CONCEPT-VISUAL -> TD-FEASIBILITY -> PR-SCOPE

Never run nodes in parallel. One node is active at most. Full mode runs in order;
lean/solo record every node `NOT_RUN_BY_MODE` and spawn none.

Dependencies:

1. `CD-PILLARS` receives selected concept, identity, fantasy/hook, loop, pillars,
   tests, anti-pillars, decision IDs, and exact draft hashes.
2. `AD-CONCEPT-VISUAL` runs only after current CD disposition and receives pillar
   hashes. It proposes visual evidence/options; user owns anchor selection.
3. `TD-FEASIBILITY` runs only after current visual-anchor decision and receives
   loop/platform intent/visual/MVP/risk/assumption hashes. It records constraints,
   unknowns, and handoffs; never chooses engine/schedule/scope.
4. `PR-SCOPE` runs only after current TD disposition and after product-owner scope
   draft exists. It advises risks; user owns final tiers.

Each node gets one bounded question, exact current input hashes, required
predecessor receipt hash, one 60-second attempt, no retry, and no nested
delegation. Return `cgs.brainstorm-gate-result/v1`:

    id: BRSGATE-<run-id>-<node>
    node: CD-PILLARS | AD-CONCEPT-VISUAL | TD-FEASIBILITY | PR-SCOPE
    role: <declared role>
    input_target_or_draft_sha256: <hash>
    input_section_hashes: {}
    decision_ids: []
    predecessor_receipt_sha256: <hash or null>
    started_at_utc: <timestamp>
    deadline_seconds: 60
    status: complete | partial | timeout | failed | side-effect | skipped
    verdict: PASS | CONCERNS | REJECT | null
    findings: []
    omissions: []
    output_sha256: <canonical hash or null>
    reviewer_task_id: <actual identity or null>

Result semantics:

- PASS permits the next dependency but never approves a product choice.
- CONCERNS stays CONCERNS. If policy/evidence marks it advisory, the product owner
  may revise, checkpoint/stop, or record concern owner/rationale/impact/review
  point and continue. This is not PASS or override.
- REJECT blocks final substantive target write. The user may revise affected
  selected sections in a new bounded run or checkpoint/stop; no override.
- partial/timeout/failed/side-effect/malformed/missing result returns Workflow
  PARTIAL, quarantines output, stops dependents, checkpoints, and does not invent
  verdict/evidence or perform final substantive target write.
- late or wrong-input output is STALE and quarantined.

Any upstream section/decision change marks its node and downstream results STALE.
They cannot support content preflight/review handoff. A later run may rerun the DAG
from the first stale node under a fresh bounded request.

## Phase 8: Semantic preflight and exact-body product approval

Build exact final bytes for every selected section from accepted BRSDEC records,
permitted evidence labels, and current gate results. Do not copy product truth
owned by another artifact; reference its stable ID/owner/path/locator/hash.

Before approval:

1. run all applicable content assertions and whole-concept consistency;
2. verify every material statement's decision/source/label/owner;
3. verify gate DAG order, identities, current input/receipt hashes, and status;
4. list blocking versus explicitly deferred nonblocking open questions;
5. verify custom/non-selected byte preservation plan;
6. re-hash target, selected sections, external context, authorization, and exact
   draft bytes; and
7. list findings/unknowns/concerns without converting them to facts.

Show the complete proposed selected bodies plus full unified target diff and
preserved-range hashes. Ask product owner to Accept exact bodies, Revise one named
section, Keep checkpoint/stop, or Stop. Permit at most two final-preflight revision
rounds. Changed bytes invalidate prior approval.

Store:

    id: BRSAPR-<concept-id>-<NNN>
    owner: <actual product owner>
    selected_section_ids: []
    approved_body_sha256_by_section: {}
    complete_target_draft_sha256: <hash>
    decision_ids: []
    assertion_result_sha256: <hash>
    gate_result_ids_and_hashes: []
    context_manifest_sha256: <hash>
    target_baseline_sha256: <hash or ABSENT>
    authorization_sha256: <hash>
    approved_at_utc: <RFC3339 seconds Z>

Denial/Stop/round exhaustion appends checkpoint and leaves existing substantive
target bytes unchanged (new-mode skeleton may remain DRAFT).

## Phase 9: Five-part CAS, atomic section write, revision, and receipt

Immediately before final target write, one attempt must pass:

1. **Target CAS** — current raw target equals authorized skeleton/source baseline;
2. **Section CAS** — every selected section equals its approved preimage and every
   non-selected/custom range equals its preservation hash with unique anchors;
3. **Context CAS** — every external source used and ordered context digest match;
   mutable target is checked only by Target/Section CAS;
4. **Authorization CAS** — exact path/operation/selected set/limits, approval hash,
   and authorization identity/hash match; and
5. **Writer CAS** — actual target writer equals authorized identity.

Failure returns the precise `ERROR — CONCURRENT TARGET CHANGE`,
`ERROR — CONTEXT EVIDENCE CHANGED`, or
`ERROR — AUTHORIZATION/WRITER CHANGED`, with no target/checkpoint transaction.

If exact final bytes equal current bytes, perform no target write and record
`UNCHANGED` only when exact current bodies/approvals/assertions already match.

Otherwise atomically replace only selected stable-ID bodies plus authorized header
fields, read back, and prove all non-selected/custom ranges unchanged. Append one
revision per selected section:

    id: BRSREV-<concept-id>-<section-id>-<NNN>
    operation: new | resume | revise
    section_id: <stable ID>
    before_target_sha256: <hash>
    after_target_sha256: <hash>
    before_section_sha256: <hash or ABSENT>
    after_section_sha256: <hash>
    decision_ids: []
    approval_id: <BRSAPR ID>
    source_and_gate_hashes: []
    authorization_sha256: <hash>
    writer_task_id: <actual identity>
    timestamp_utc: <RFC3339 seconds Z>

Append final checkpoint by predecessor/create-if-absent CAS. Then, only after the
final content/header CAS and stable read-back hash, create
`cgs.brainstorm-authoring-receipt/v1` binding request/operation, pre/post target,
selected/preserved section hashes, decisions/approval/revisions, content/profile/
author schema, context digest, research/estimate/gate evidence, findings/open
questions, authorization, author/writer/recorder, checkpoint head, and target path.

Receipt ID may appear in the target header; its path/hash cannot. The external
receipt binds already-final bytes and is authoring evidence, not concept review or
approval.

If checkpoint/receipt persistence fails after verified target bytes, leave
content-derived status intact, return Workflow Verdict PARTIAL, report exact
unreceipted target hash, emit no review handoff, and never replay/revert the write.

## Phase 10: Content result and independent read-only review handoff

Re-evaluate every canonical section, custom preservation, assertion, evidence
label, decision/approval/revision, gate result, finding/open question, target/
context hash, and receipt.

Set target Content Status from content only:

- DRAFT: skeleton/approved direction exists but no complete selected body;
- PARTIAL: safe content exists but whole profile has blocking incompleteness,
  invalid/stale evidence, unresolved required gates, or blocking questions;
- CONTENT_COMPLETE: all canonical sections pass, only permitted nonblocking
  deferrals remain, provenance is current, and target bytes are stable.

Set Workflow Verdict separately:

- DRAFT/PARTIAL target: PARTIAL or STOPPED, no review handoff;
- CONTENT_COMPLETE plus verified authoring receipt: READY_FOR_REVIEW and exact
  independent concept-review handoff;
- CONTENT_COMPLETE but receipt append/verification failed: PARTIAL, no handoff,
  exact unreceipted target hash;
- unsafe source/authorization/identity/drift: BLOCKED with last safe target;
- invalid request/corrupt evidence before safe work: ERROR, no false target state.

Handoff contract `cgs.concept-review-request/v1` names a fresh independent
concept-review task using profile `CONCEPT-CONTENT-v1` and default reviewer role
`creative-director`. It binds:

- target path/current SHA-256, GC-1/profile/content/author schema;
- all section/assertion hashes and custom preservation evidence;
- decisions/approval/revisions, research/estimate/gate results, findings/questions;
- context digest, authoring receipt ID/path/hash, and all author/gate/writer/
  recorder identities; and
- required immutable output `cgs.concept-approval/v1` with verdict APPROVE,
  CONCERNS, or REJECT.

Do not invoke the reviewer. It must be fresh, role-separated, target/receipt/
context read-only, recompute hashes, use the concept profile rather than a system-
GDD rubric, and create only a separately authorized immutable approval record.

Only a current matching APPROVE may establish concept approval. Any target/
context/receipt mutation makes old approval STALE and requires new authoring
receipt plus fresh review. Never overwrite immutable evidence.

## Phase 11: Resume, finite recovery, output, and stop

Resume validates exact request/checkpoint paths and full v2 predecessor/payload
chain, source ABSENT/hash, target/context, schema, authorization, identities,
selected/preserved sections, draft snapshot, decisions/approvals/revisions, gate/
research/estimate evidence, convergence counters, findings/questions, and absence
of late writes.

- all hashes current: continue first incomplete idempotent transition, prioritizing
  APPROVED_NOT_WRITTEN exact bodies;
- target/selected/preserved mismatch: CONFLICT/BLOCKED, zero write, show exact diff;
- external context changed: mark dependent sections/gates STALE, invalidate active
  receipt/review handoff, and require new preflight;
- checkpoint collision/fork: ERROR — CHECKPOINT CHAIN INVALID;
- author/profile mismatch: require explicit migration/restart; never replay;
- exhausted counter remains exhausted in this run; resume requires a new run ID.

Conversation memory never reconstructs source bytes, decisions, approval, gate
receipts, context, checkpoints, authoring receipt, or independent approval.

Final response lists operation/session/concept IDs, review/research modes,
convergence counters, source/output hashes, section state/change/preservation
table, decisions/approval/revisions, evidence labels and research/estimate/gate
receipts, findings/questions, authorization/roles, checkpoint/authoring-receipt
paths/hashes, content/workflow/approval states, non-writes, and exactly one next
action or Stop.

Choose at most one next action from current evidence: resume one named question,
validate the core mechanic, obtain one missing research/estimate/setup/review
evidence item, decompose an approved concept into systems, or Stop. Never invoke
it, print a pipeline, or claim market/engine/feasibility/schedule/art/release
approval.
