# Skill Test Spec: $brainstorm

## Skill Summary

`$brainstorm` authors or safely revises exactly one GC-1 game concept from
`cgs.brainstorm-request/v2`. It uses `game-concept-profile-schema-v2`,
`cgs.game-concept-content-profile/v2`, bounded ideation/evidence, user-owned
decision and exact-body approval provenance, finite convergence, a deterministic
read-only advisory gate DAG, five-part CAS, append-only checkpoints, and an
external `cgs.brainstorm-authoring-receipt/v1`.

Content completeness, workflow readiness, independent concept review, and formal
concept approval are separate. The authoring workflow invokes neither review nor
downstream work.

## Static Assertions

- [ ] BRS-S001: Frontmatter contains only matching `name` and non-empty `description`
- [ ] BRS-S002: Invocation requires one cgs.brainstorm-request/v2 manifest; no-arg stops before repository reads
- [ ] BRS-S003: Author schema revisions exact SKILL bytes, NUL, and required continuation bytes
- [ ] BRS-S004: Operation is exactly new/resume/revise; review and research modes are independent
- [ ] BRS-S005: New requires ABSENT; resume/revise bind exact raw target/checkpoint revisions and never select latest
- [ ] BRS-S006: One mutation authorization covers exact target sections plus deterministic checkpoint/receipt creates
- [ ] BRS-S007: Product choices and exact-body approval remain user/named-owner decisions, not filesystem authority
- [ ] BRS-S008: GC-1/profile/content contracts define all canonical stable section IDs
- [ ] BRS-S009: Non-selected and unknown/custom sections receive preservation IDs and remain byte-identical
- [ ] BRS-S010: Content/evidence/workflow/assertion/section-status axes are separate and non-placeholder text is insufficient
- [ ] BRS-S011: Context selection is deterministic with hard 16-file/524288-byte limits and mutable-target-baseline treatment
- [ ] BRS-S012: Context overflow may append only one authorized PARTIAL checkpoint and leaves target unchanged
- [ ] BRS-S013: New mode creates the full neutral skeleton before substantive concept selection/body writes
- [ ] BRS-S014: Checkpoints use cgs.brainstorm-checkpoint/v2 append-only predecessor/create-if-absent CAS
- [ ] BRS-S015: Every convergence prompt offers Accept/Revise named part/Keep checkpoint and stop/Stop with two-round cap
- [ ] BRS-S016: Ideation generates two-to-four comparable concepts, default three, at most two rounds
- [ ] BRS-S017: Four shared decision classes have truthful stable BRSDEC provenance
- [ ] BRS-S018: User alone selects/combines concepts and all product-facing loop/pillar/visual/scope decisions
- [ ] BRS-S019: SOURCED_CURRENT market claims require cgs.brainstorm-research-receipt/v1 URL/date/claim/snapshot/researcher evidence
- [ ] BRS-S020: Missing/stale market/platform evidence remains USER_ASSUMPTION/MODEL_HYPOTHESIS/UNKNOWN, never fabricated fact
- [ ] BRS-S021: Engine choice is preference/external receipt/deferred to setup owner; brainstorm never recommends/configures it
- [ ] BRS-S022: Schedule/capacity/content/cost values are user-owned, exact cgs.estimate-evidence/v1, or UNKNOWN
- [ ] BRS-S023: Full advisory DAG is exactly CD-PILLARS -> AD-CONCEPT-VISUAL -> TD-FEASIBILITY -> PR-SCOPE and sequential
- [ ] BRS-S024: Each gate has one 60-second attempt, no retry/nesting, typed partial/timeout/failed/side-effect/quarantine result
- [ ] BRS-S025: CONCERNS remains visible, REJECT has no override, and partial/failure stops dependents/final substantive write
- [ ] BRS-S026: Lean marks all gates NOT_RUN_BY_MODE; solo additionally spawns zero subagents
- [ ] BRS-S027: BRSAPR binds exact selected bodies/full draft, decisions, assertions, gates, context, target baseline, and authorization
- [ ] BRS-S028: Final target write uses Target/Section/Context/Authorization/Writer CAS
- [ ] BRS-S029: BRSREV binds before/after target/section, decision, approval, source/gate, authorization, and writer revisions/IDs
- [ ] BRS-S030: cgs.brainstorm-authoring-receipt/v1 is external authoring evidence without target/receipt revision cycle
- [ ] BRS-S031: Receipt/checkpoint failure preserves content status but returns workflow PARTIAL with no review handoff
- [ ] BRS-S032: Target CONTENT_COMPLETE, Workflow READY_FOR_REVIEW, and external APPROVED are distinct
- [ ] BRS-S033: Review handoff is cgs.concept-review-request/v1 for fresh independent CONCEPT-CONTENT-v1 read-only review
- [ ] BRS-S034: Brainstorm never invokes design-review/system-GDD rubric, reviewer, or writes approval evidence
- [ ] BRS-S035: Only current separated cgs.concept-approval/v1 APPROVE matching target/receipt/context supports approval
- [ ] BRS-S036: Research, estimate, engine setup, pillars, art, architecture, code, assets, production state, and shared catalog are non-writes
- [ ] BRS-S037: Final output recommends at most one evidence-driven action or Stop and invokes nothing
- [ ] BRS-S038: Metadata names request v2, bounded user-owned authoring, finite checkpoints, CAS/receipt, and independent review
- [ ] BRS-S039: Spec contains complete numbered fixtures/assertions for new/resume/revise, convergence, DAG, evidence, CAS, receipt, and review
- [ ] BRS-S040: Candidate does not stage shared catalog/result changes or claim unexecuted `$skill-test`

---

## Behavioral Cases

### Case 1: no argument has zero side effects

**Input:**

    $brainstorm

**Expected behavior:** print exact manifest-path usage and stop before repository
discovery, reads, agents, authorization, or writes.

**Assertions:**

- [ ] BRS-C01-A: Usage names cgs.brainstorm-request/v2
- [ ] BRS-C01-B: Zero filesystem/context/research/delegation side effects
- [ ] BRS-C01-C: No content/workflow/review/approval result is fabricated

---

### Case 2: new creates complete neutral skeleton before ideation body

**Fixture:** valid new request, canonical target ABSENT, authorized target/checkpoint
boundary, bounded context valid.

**Expected behavior:** ABSENT CAS creates GC-1 header and every canonical stable-ID
heading with neutral placeholders; checkpoint records all state axes; no proposal
is silently selected or inserted.

**Assertions:**

- [ ] BRS-C02-A: Skeleton precedes substantive selected-concept content
- [ ] BRS-C02-B: Target Content Status DRAFT and receipt PENDING
- [ ] BRS-C02-C: Only target/checkpoint paths change

---

### Case 3: new refuses to replace an existing concept

**Fixture:** request operation new but canonical target exists at revision H1.

**Expected behavior:** validation returns BLOCKED before authorization/ideation/
checkpoint; target remains H1; exact resume/revise request correction is reported.

**Assertions:**

- [ ] BRS-C03-A: No delete/rename/overwrite or silent operation conversion
- [ ] BRS-C03-B: Zero gate/research agents and zero writes

---

### Case 4: resume selects open sections and preserves custom bytes

**Fixture:** current GC-1 has COMPLETE identity/pillars, OPEN MVP/risks, and two
custom user sections with known ranges/revisions. User selects MVP/risks.

**Expected behavior:** only selected IDs enter plan; complete and custom sections
remain PRESERVED; final diff/CAS proves exact byte equality outside selected/header
ranges.

**Assertions:**

- [ ] BRS-C04-A: Inventory records owners/states/revisions/provenance
- [ ] BRS-C04-B: Selecting a section does not select its dependencies
- [ ] BRS-C04-C: Custom prose is neither normalized nor dropped

---

### Case 5: revise rejects unapproved scope expansion

**Fixture:** revise authorizes only CONCEPT-CORE-LOOP; discussion proposes changing
pillars or a custom section.

**Expected behavior:** out-of-scope change is excluded and reported as a new
boundary request; current run proceeds only with loop or stops; no implicit write
authority is inferred from product discussion.

**Assertions:**

- [ ] BRS-C05-A: Selected stable IDs remain exact
- [ ] BRS-C05-B: Product approval is not filesystem authorization
- [ ] BRS-C05-C: One unchanged boundary requires no repeated write prompts

---

### Case 6: five-part CAS protects concurrent edits

**Fixture variants:** target changes; selected body changes; custom/non-selected
range changes; used context changes; authorization changes; wrong writer acts.

**Expected behavior:** Target/Section/Context/Authorization/Writer CAS identifies
the drift before write; target/checkpoint transaction is not applied; both current
source and approved draft are preserved for a new merge/preflight.

**Assertions:**

- [ ] BRS-C06-A: All five facets execute immediately before write
- [ ] BRS-C06-B: Collaborator bytes are never overwritten
- [ ] BRS-C06-C: Stale exact-body approval cannot apply to new baseline/context

---

### Case 7: every user revision family terminates finitely

**Fixture variants:** third Creative Brief revision; third pillar revision; third
final-preflight revision; user selects Keep checkpoint/stop or Stop.

**Expected behavior:** at most two revisions occur per family; third request or
explicit exit appends one safe checkpoint when authorized and returns STOPPED with
the exact next transition; no acceptance is inferred.

**Assertions:**

- [ ] BRS-C07-A: Counter and decision family persist in checkpoint
- [ ] BRS-C07-B: Accept/Revise/Keep-stop/Stop are always available
- [ ] BRS-C07-C: Resume with same run cannot reset an exhausted counter

---

### Case 8: bounded ideation remains comparable and user-selected

**Fixture variants:** user requests two, default, or four proposals; rejects first
round; asks for third round; combines named elements.

**Expected behavior:** two-to-four structurally complete proposals, default three;
at most two rounds; combination records exact source elements and new ID; product
owner selects. Third round request checkpoints/stops.

**Assertions:**

- [ ] BRS-C08-A: Proposals differ materially, not superficial reskins
- [ ] BRS-C08-B: Author/gate never silently selects/blends
- [ ] BRS-C08-C: Selection records alternatives/rationale without sensitive detail

---

### Case 9: checkpoint chain provides exact idempotent resume

**Fixture:** interruption after visual-anchor choice with exact v2 checkpoint;
variants include missing predecessor, fork/collision, changed source, and late gate
write.

**Expected behavior:** valid chain restores draft/selected/preserved IDs, decisions,
counters, evidence/gates, target revision, and first incomplete transition. Invalid
variants stop without replay/newest-file selection.

**Assertions:**

- [ ] BRS-C09-A: Records are immutable and predecessor/revision-bound
- [ ] BRS-C09-B: APPROVED_NOT_WRITTEN exact body is resumed before new questions
- [ ] BRS-C09-C: Conversation memory cannot reconstruct checkpoint state

---

### Case 10: full gate DAG is sequential and revision-bound

**Fixture:** full mode, current content/decisions, all nodes complete PASS.

**Expected behavior:** CD -> AD -> user visual selection -> TD -> user scope draft ->
PR. One node active; every result binds exact input and predecessor receipt revisions.

**Assertions:**

- [ ] BRS-C10-A: Downstream dispatch before dependency is rejected
- [ ] BRS-C10-B: Gate outputs never make user product choices
- [ ] BRS-C10-C: Current PASS evidence may enter content preflight, not approval

---

### Case 11: lean and solo preserve gate omission honestly

**Fixture variants:** lean; solo with request attempting gate/research agents.

**Expected behavior:** all advisory gates record NOT_RUN_BY_MODE; lean spawns no
gates; solo spawns zero subagents and does not perform agent research. No skipped
node is labeled PASS.

**Assertions:**

- [ ] BRS-C11-A: Mode behavior matches SKILL/metadata/spec
- [ ] BRS-C11-B: Independent future review handoff is not an inline spawn
- [ ] BRS-C11-C: User-owned local authoring remains available

---

### Case 12: gate timeout, partial, side effect, and late output fail closed

**Fixture variants:** AD times out; TD partial/malformed; PR edits a file; late CD
result references old input revision.

**Expected behavior:** one BRSGATE result records typed status, deadline, revisions,
omissions/output/quarantine; no retry/nesting; dependents/final substantive write
stop; Workflow PARTIAL checkpoint identifies one recovery.

**Assertions:**

- [ ] BRS-C12-A: One 60-second attempt per node and one active node
- [ ] BRS-C12-B: No fabricated verdict/evidence or merge of quarantined result
- [ ] BRS-C12-C: New run is required to rerun failed/stale node

---

### Case 13: CONCERNS, REJECT, and upstream revision retain semantics

**Fixture variants:** advisory TD CONCERNS; blocking concern; CD REJECT; pillar
changes after all nodes completed.

**Expected behavior:** advisory concern stays CONCERNS with owner/rationale/impact/
review point if user continues; blocking concern/REJECT prevents final substantive
write; no override. Pillar change stales CD and all downstream results.

**Assertions:**

- [ ] BRS-C13-A: User acceptance does not relabel concern PASS
- [ ] BRS-C13-B: REJECT has revise-new-run/checkpoint-stop only
- [ ] BRS-C13-C: Old input receipts cannot support preflight/handoff

---

### Case 14: market research has current-source boundaries

**Fixture variants:** research none; receipts-only with stale snapshot; authorized-
current receipt; no evidence for market size/comparable success/demand/price/trend.

**Expected behavior:** only valid current receipt supports SOURCED_CURRENT and
records URL/publisher/date/claim locator/observed time/snapshot/researcher. Other
claims become user assumption, model hypothesis, unknown, or finding.

**Assertions:**

- [ ] BRS-C14-A: No fabricated citation or market validation
- [ ] BRS-C14-B: Model hypothesis is visibly non-authoritative
- [ ] BRS-C14-C: Research never chooses concept or expands mutation scope

---

### Case 15: platform and engine claims stay with technical owner

**Fixture variants:** mobile/console intent without sources; user prefers Unity;
current external engine-selection receipt exists; TD proposes an engine.

**Expected behavior:** unsupported support/policy is UNKNOWN; preference remains
preference; current external receipt may be referenced; otherwise Engine Decision
is DEFERRED TO SETUP-ENGINE. TD recommendation becomes technical handoff only.

**Assertions:**

- [ ] BRS-C15-A: Brainstorm never recommends/selects/installs/configures engine
- [ ] BRS-C15-B: Current platform facts require owned source evidence
- [ ] BRS-C15-C: Setup-engine is at most one uninvoked next action

---

### Case 16: schedule and content quantities are not model estimates

**Fixture variants:** model suggests X-Y months; user supplies budget; exact current
cgs.estimate-evidence/v1 exists; stale estimate mismatches scope.

**Expected behavior:** model range is excluded/UNKNOWN; user data is labeled owner;
current estimate binds profile/scope/units/assumptions/estimator; stale mismatch is
finding. No formal schedule/content promise is authored from intuition.

**Assertions:**

- [ ] BRS-C16-A: USER BUDGET/USER ASSUMPTION/SOURCED ESTIMATE/UNKNOWN are distinct
- [ ] BRS-C16-B: Qualitative MVP bounds do not masquerade as calibrated estimate
- [ ] BRS-C16-C: Estimate workflow is not invoked

---

### Case 17: content completeness rejects empty template and blocking open work

**Fixture variants:** all headings but placeholder loop; unsupported market fact;
missing decision provenance; explicit nonblocking deferred question; blocking open
question; valid substantive profile.

**Expected behavior:** assertions derive INCOMPLETE/INVALID until defects resolve.
Permitted explicit nonblocking deferral may remain with owner/impact/evidence/
review point. Only valid full profile becomes CONTENT_COMPLETE.

**Assertions:**

- [ ] BRS-C17-A: Heading/non-placeholder text alone never passes
- [ ] BRS-C17-B: Every material statement traces to decisions/evidence labels
- [ ] BRS-C17-C: Blocking question prevents CONTENT_COMPLETE

---

### Case 18: authoring receipt failure cannot create review handoff

**Fixture:** atomic final target is CONTENT_COMPLETE and stable, but final
checkpoint/authoring receipt append fails or receipt verification mismatches.

**Expected behavior:** target content status remains CONTENT_COMPLETE; Workflow
Verdict PARTIAL; exact unreceipted target revision; no independent review handoff;
target is not replayed/reverted.

**Assertions:**

- [ ] BRS-C18-A: Content, workflow, and approval states remain separate
- [ ] BRS-C18-B: Receipt stays external without target/revision cycle
- [ ] BRS-C18-C: Missing receipt cannot support approval or downstream work

---

### Case 19: independent concept review and approval remain current-revision-bound

**Fixture variants:** CONTENT_COMPLETE+verified receipt; wrong system-GDD reviewer;
self-review; external APPROVE; CONCERNS/REJECT; target/context/receipt changed after
APPROVE.

**Expected behavior:** authoring only emits cgs.concept-review-request/v1 handoff to
fresh CONCEPT-CONTENT-v1 read-only role. Only current separated
cgs.concept-approval/v1 APPROVE supports approval. All invalid/stale/non-APPROVE
variants remain unapproved and immutable history is preserved.

**Assertions:**

- [ ] BRS-C19-A: No design-review invocation or system-GDD rubric
- [ ] BRS-C19-B: Handoff binds target/sections/context/receipt/provenance revisions
- [ ] BRS-C19-C: H2 cannot be approved by H1 evidence
- [ ] BRS-C19-D: Reviewer/approval record never edits the concept

---

### Case 20: staged P1 package and catalog claims are honest

**Fixture:** staged SKILL, continuation, metadata, and this spec; shared catalog row
still points to the formal utility spec and has no executed-result fields.

**Expected behavior:** matrix contains BRS-S001..BRS-S040, Cases 1..20,
BRS-X001..BRS-X008, and coverage through BRS-012. Candidate stages no catalog
change and does not call source checks an executed `$skill-test`.

**Assertions:**

- [ ] BRS-C20-A: Exclusive files agree on v2 contracts/status/review boundary
- [ ] BRS-C20-B: Shared catalog remains untouched
- [ ] BRS-C20-C: Verification provenance is stated accurately

---

## Cross-skill compatibility

- [ ] BRS-X001: Four decision classes and actual identities match authoring provenance contracts
- [ ] BRS-X002: Bounded context/canonical manifest/mutable-target-baseline match authoring contracts
- [ ] BRS-X003: Product/exact-body approval never expands mutation or review authority
- [ ] BRS-X004: Five-part CAS and BRSREV preserve collaborator/non-selected/custom bytes
- [ ] BRS-X005: Checkpoint/receipt failure separates content status from Workflow Verdict
- [ ] BRS-X006: Research, engine/platform, estimate, pillars/art, and implementation owners remain external
- [ ] BRS-X007: Independent review consumes target plus authoring receipt and never uses system-GDD review
- [ ] BRS-X008: Downstream action is a single uninvoked evidence-based handoff or Stop

## Coverage Notes

- BRS-001..BRS-003 remain covered by concept-specific external review,
  section-scoped source CAS/preservation, and the sequential advisory gate DAG.
- BRS-004: Case 7 and BRS-S015/S016 enforce finite exits/counters.
- BRS-005: Cases 2/9 and BRS-S013/S014 provide file-backed skeleton/checkpoints.
- BRS-006: Cases 10..13 and BRS-S023..S026 define timeout/failure/partial DAG.
- BRS-007: Case 14 and BRS-S019/S020 enforce research/source boundaries.
- BRS-008: Case 15 and BRS-S021 preserve engine/platform owner boundaries.
- BRS-009: Case 16 and BRS-S022 preserve estimate ownership/calibration.
- BRS-010: Case 5 and BRS-S006/S007 use one mutation authorization plus content approvals.
- BRS-011: Cases 1..20 and BRS-S039 replace damaged/drifted tests.
- BRS-012: Case 17 and BRS-S008/S010 define content-level completeness.
- Shared catalog/results and downstream consumers require separate ownership; this
  candidate does not modify them or claim an executed test run.
