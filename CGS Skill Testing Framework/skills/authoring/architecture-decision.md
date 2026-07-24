# Skill Test Spec: $architecture-decision

## Skill Summary

`$architecture-decision` authors or safely retrofits exactly one ADR for one
cohesive technical decision from `cgs.architecture-decision-request/v2`. It uses
collision-safe allocation, `architecture-decision-profile-schema-v2`,
`cgs.adr-content-profile/v2`, bounded source evidence, user-selected comparable
alternatives, dependency/replacement graph validation, section checkpoints/CAS,
and external authoring receipt/review/lifecycle records.

The authoring target remains Proposed (or honest Unknown legacy retrofit).
Authoring completeness, Workflow READY_FOR_REVIEW, independent review
recommendation, and lifecycle Accepted are separate states.

## Static Assertions

- [ ] ADR-S001: Frontmatter contains only matching name and non-empty description
- [ ] ADR-S002: Invocation requires one cgs.architecture-decision-request/v2 manifest; no-arg stops before reads/allocation/writes
- [ ] ADR-S003: Author schema hashes exact SKILL bytes, NUL, and required continuation bytes
- [ ] ADR-S004: Request and ADR define exactly one decision key/domain/question/in-scope set
- [ ] ADR-S005: Compound decisions split unless current source hashes prove inseparability
- [ ] ADR-S006: New ADR consumes cgs.adr-id-allocation/v1 canonical UUID/exact path receipt and never scans next number
- [ ] ADR-S007: Target ABSENT CAS owns uniqueness; allocation/path collision stops without overwrite/reallocation
- [ ] ADR-S008: Semantic fingerprint checks bounded ADR summaries and offers cancel/revise/supersede/disjoint-scope/stop to user
- [ ] ADR-S009: One mutation authorization covers exact target sections and deterministic checkpoint/receipt creates
- [ ] ADR-S010: Only target ADR and create-only checkpoint/authoring-receipt records are writable
- [ ] ADR-S011: Profile v2 has stable section IDs plus independent content/evidence/workflow/assertion/status axes
- [ ] ADR-S012: New/revise/supersede proposal is Proposed; retrofit missing status is only Proposed or Unknown
- [ ] ADR-S013: Existing Accepted/Deprecated/Superseded ADR is immutable to authoring skill
- [ ] ADR-S014: External status state machine and cgs.adr-lifecycle-record/v1 define allowed CAS transitions
- [ ] ADR-S015: Supersession/scoped-exception links bind exact predecessor ID/path/hash/status/scope and remain acyclic
- [ ] ADR-S016: Context order is deterministic with hard 16-file/524288-byte limits and mutable-target-baseline
- [ ] ADR-S017: Context overflow may append one authorized PARTIAL checkpoint and leaves target unchanged
- [ ] ADR-S018: Every requirement/constraint/source records stable ID/owner/path-or-URL/locator/hash/version/date/coverage
- [ ] ADR-S019: Engine references record pinned version/domain/risk/cutoff/claim/hash/date and VERIFIED/PARTIAL/UNVERIFIED/STALE
- [ ] ADR-S020: Unclear dependency/API/verification/migration/performance/ordering is UNKNOWN blocker, never assumed None
- [ ] ADR-S021: Pre-write graph resolves IDs/status/hash and detects self/duplicate/dependency/replacement cycles
- [ ] ADR-S022: At least two viable alternatives use identical criteria, evidence coverage, reversibility, consequences, and risks
- [ ] ADR-S023: Actual user/named authority selects alternative/tradeoffs/supersession/scope; author/consultant never selects
- [ ] ADR-S024: Shared four decision classes plus ADRDEC/ADRCON/ADRALT provenance are stable/truthful
- [ ] ADR-S025: Skeleton-first section authoring uses cgs.architecture-decision-checkpoint/v2 predecessor CAS and exact resume
- [ ] ADR-S026: cgs.adr-content-profile/v2 assertions validate all mandatory sections; headings/placeholders are insufficient
- [ ] ADR-S027: Numeric performance/effort claims require sourced units/method/hash/date or HYPOTHESIS/UNKNOWN plus validation
- [ ] ADR-S028: Consultations cap one/role, two/run, two concurrent, one 60-second attempt, no retry/nesting; solo is zero
- [ ] ADR-S029: cgs.adr-consultation-result/v1 types partial/timeout/failed/side-effect/late handling and never changes Status
- [ ] ADR-S030: ADRAPR binds exact body, decisions/constraints/alternatives, assertions, graph/findings, context, baseline, authorization
- [ ] ADR-S031: Every target write uses Target/Section/Context/Authorization/Writer CAS
- [ ] ADR-S032: ADRREV binds before/after target/section, decisions/approval/sources/graph/authorization/actual writer
- [ ] ADR-S033: cgs.adr-authoring-receipt/v1 remains external and binds complete final authoring evidence without hash cycle
- [ ] ADR-S034: Receipt/checkpoint failure preserves content completeness but returns workflow PARTIAL with no review handoff
- [ ] ADR-S035: READY emits only cgs.architecture-review-request/v2 for a fresh read-only independent review task
- [ ] ADR-S036: cgs.architecture-review/v2 recommendation is not lifecycle status or acceptance
- [ ] ADR-S037: Only separate lifecycle recorder may CAS status/links and emit cgs.adr-lifecycle-record/v1/registry projection
- [ ] ADR-S038: GDD/registry/control/story/readiness/review/lifecycle/other ADR/code files remain unchanged; events are non-mutating
- [ ] ADR-S039: Metadata names single-decision collision-safe Proposed ADR, request v2, bounded evidence, CAS/receipt/review lifecycle
- [ ] ADR-S040: Spec has complete numbered cases/cross-checks/ADR-001..014 coverage and stages no catalog result changes

---

## Behavioral Cases

### Case 1: no argument has zero side effects

**Input:**

    $architecture-decision

**Expected behavior:** print exact manifest-path usage and stop before repository
discovery, ID allocation, context, consultation, authorization, or write.

**Assertions:**

- [ ] ADR-C01-A: Usage names cgs.architecture-decision-request/v2
- [ ] ADR-C01-B: Zero filesystem/context/delegation side effects
- [ ] ADR-C01-C: No Proposed/review/Accepted result is fabricated

---

### Case 2: collision-safe new ADR creates complete skeleton

**Fixture:** valid allocation receipt with canonical UUID/display sequence/slug/
exact path/nonce/hash; target ABSENT; one decision scope; mutation boundary current.

**Expected behavior:** no directory numbering scan; ABSENT Target CAS creates full
profile skeleton with Status Proposed and every stable section ID; checkpoint
captures allocation/scope/fingerprint/state axes.

**Assertions:**

- [ ] ADR-C02-A: Allocation receipt/path/UUID are mutually consistent
- [ ] ADR-C02-B: Display sequence is not identity
- [ ] ADR-C02-C: Only target/checkpoint paths change

---

### Case 3: allocation or path collision fails closed

**Fixture variants:** allocation path already exists; receipt path differs from
target; allocation hash/nonce reused; another writer creates target before CAS.

**Expected behavior:** validation/Target CAS returns BLOCKED conflict, never
overwrites/reuses/scans next number or silently selects another path in run.

**Assertions:**

- [ ] ADR-C03-A: Existing ADR bytes remain unchanged
- [ ] ADR-C03-B: Allocation owner/new request is the one recovery
- [ ] ADR-C03-C: No duplicate canonical ADR ID/path is emitted

---

### Case 4: semantic duplicate detection is user-routed

**Fixture variants:** same decision fingerprint under different title; near match
to Proposed; overlap with Accepted; objectively disjoint component scope.

**Expected behavior:** bounded summary evidence is shown. User chooses cancel,
revise Proposed in new request, supersede Accepted, prove disjoint scope, or stop.
Author never creates/title-renames duplicate or chooses route.

**Assertions:**

- [ ] ADR-C04-A: Fingerprint uses domain/key/question/sorted in-scope IDs
- [ ] ADR-C04-B: Existing path/status/hash is explicit
- [ ] ADR-C04-C: Accepted target is not edited by duplicate handling

---

### Case 5: compound decision is split unless inseparable

**Fixture variants:** networking transport and save format with different owners/
rollback; renderer/API pair with current proof they cannot vary independently.

**Expected behavior:** first becomes separate ADR/TECH handoffs and one selected
decision; second may remain bundled only with source IDs/hashes and shared
alternatives/acceptance/rollback lifecycle.

**Assertions:**

- [ ] ADR-C05-A: Out-of-scope questions have owner/destination
- [ ] ADR-C05-B: Interfaces/migration cannot smuggle a second decision
- [ ] ADR-C05-C: User confirms exact decision scope

---

### Case 6: bounded context overflow is reproducible

**Fixture:** required ADR/engine/requirement candidates exceed 16 files or 524288
exact bytes; one critical dependency would fall beyond cap.

**Expected behavior:** normative selection order/size-before-load applies; no
truncation/broad scan/silent omission; at most one authorized PARTIAL checkpoint;
target remains unchanged.

**Assertions:**

- [ ] ADR-C06-A: Same manifest yields same context digest
- [ ] ADR-C06-B: CONTEXT_BUDGET_EXCEEDED names loaded/omitted sources
- [ ] ADR-C06-C: Missing evidence is not converted to None

---

### Case 7: missing or stale engine evidence remains unverified

**Fixture variants:** engine unconfigured; module ref absent; stale hash/version;
post-cutoff API not covered; current pinned reference verifies claim.

**Expected behavior:** first four record UNVERIFIED/STALE/UNKNOWN with exact owner/
needed evidence and prevent READY; setup-engine handoff only. Last records VERIFIED
with path/locator/hash/version/date/observed-at/risk/claim.

**Assertions:**

- [ ] ADR-C07-A: No invented engine/version/API support
- [ ] ADR-C07-B: References Consulted is provenance, not path list alone
- [ ] ADR-C07-C: Safe Proposed/PARTIAL draft is honest about coverage

---

### Case 8: comparable alternatives and constraints stay user-owned

**Fixture:** two viable approaches, meaningful status quo, hard compatibility
constraint, derived implication, missing performance evidence, consultant favorite.

**Expected behavior:** all alternatives use same criteria; hard source constrains;
derived implication is shown; performance stays hypothesis/unknown; actual user/
authority selects ADRALT and tradeoffs. Consultant favorite has no authority.

**Assertions:**

- [ ] ADR-C08-A: No straw option or unsourced scoring
- [ ] ADR-C08-B: ADRDEC/ADRCON/ADRALT IDs and source hashes are complete
- [ ] ADR-C08-C: Selection is not lifecycle acceptance or file authority

---

### Case 9: section checkpoint and resume are exact/idempotent

**Fixture:** interruption after alternatives approval; variants include valid v2
chain, missing predecessor/fork, changed target/context, approved-not-written body.

**Expected behavior:** valid resume verifies chain/state and writes approved exact
body before new questions; drift/fork blocks without replay. Whole ADR is not
regenerated from conversation memory.

**Assertions:**

- [ ] ADR-C09-A: Skeleton/decisions/sections persist incrementally
- [ ] ADR-C09-B: Checkpoint records next legal transition and CAS baselines
- [ ] ADR-C09-C: Existing out-of-scope bytes are preserved

---

### Case 10: consultation modes and caps are deterministic

**Fixture variants:** solo; lean with engine specialist; full with engine specialist
and technical-director.

**Expected behavior:** solo zero agents; lean maximum one; full maximum two and may
run concurrently; each has one question/60s attempt/no retry/nesting; all outputs
ADVISORY and Status remains Proposed.

**Assertions:**

- [ ] ADR-C10-A: Reviewer/recorder identities are not used as consultants
- [ ] ADR-C10-B: Consultant cannot edit or select alternative
- [ ] ADR-C10-C: Positive advice cannot set Accepted

---

### Case 11: consultation failure preserves Proposed partial evidence

**Fixture variants:** required engine consultant timeout; TD partial/malformed;
consultant writes a file; late result for old draft; optional consultation skipped.

**Expected behavior:** typed result records status/deadline/input/output/omissions/
identity; failed required evidence becomes UNVERIFIED/PARTIAL, checkpoint, no
review handoff; side-effect/late output quarantined; no retry/fabrication.

**Assertions:**

- [ ] ADR-C11-A: Status never changes from Proposed
- [ ] ADR-C11-B: Optional missing input may be UNKNOWN only when no assertion needs it
- [ ] ADR-C11-C: Target is not directly patched from consultant output

---

### Case 12: dependency graph blocks unknown, cycle, and Proposed prerequisite

**Fixture variants:** unknown Depends On; A->B->A cycle; replacement cycle;
required prerequisite Proposed; current Accepted prerequisite; evidence-backed no
dependencies.

**Expected behavior:** unknown/cycles/proposed prerequisite produce blocking graph
finding and no READY/acceptance eligibility; Accepted resolves; `None` appears only
when bounded graph evidence proves no edge.

**Assertions:**

- [ ] ADR-C12-A: IDs/status/path/hash/lifecycle receipt resolve uniquely
- [ ] ADR-C12-B: Self/duplicate/enable-block contradictions are checked
- [ ] ADR-C12-C: No story/registry readiness is inferred

---

### Case 13: retrofit and lifecycle-managed statuses cannot self-sign

**Fixture variants:** missing legacy status; ambiguous evidence; existing Accepted,
Deprecated, or Superseded ADR; stale/malformed legacy section.

**Expected behavior:** missing status offers Proposed/Unknown only; ambiguous is
Unknown. Lifecycle-managed ADR is not mutated. Retrofit revises only explicitly
authorized missing/stale section with preservation/CAS and never validates old
acceptance.

**Assertions:**

- [ ] ADR-C13-A: Accepted/Deprecated/Superseded are not author choices
- [ ] ADR-C13-B: User/file approval cannot create lifecycle transition
- [ ] ADR-C13-C: Current target hash is used for fresh review handoff only when ready

---

### Case 14: supersede proposal and scoped exception preserve old authority

**Fixture variants:** proposed successor completely replaces Accepted ADR; partial
replacement; objectively disjoint exception; overlapping “intentional exception”.

**Expected behavior:** complete proposal records exact predecessor/receipt/scope/
retained obligations/migration; old ADR remains unchanged/authoritative. Partial
replacement blocks. Disjoint exception records predicate/owner/reason/precedence/
exit. Overlap requires supersede/align/stop.

**Assertions:**

- [ ] ADR-C14-A: Proposed successor does not write Superseded By to predecessor
- [ ] ADR-C14-B: Replacement links and graph are acyclic
- [ ] ADR-C14-C: Only lifecycle recorder may atomically link accepted successor

---

### Case 15: five-part CAS rejects target/section/context/authority/writer drift

**Fixture variants:** target changes; selected anchor/body changes; used source
changes; authorization changes; wrong writer attempts section patch.

**Expected behavior:** corresponding CAS facet fails immediately before write;
no target/checkpoint transaction; approved body and collaborator bytes preserved.

**Assertions:**

- [ ] ADR-C15-A: All five CAS facets execute for every section/final metadata write
- [ ] ADR-C15-B: ADRREV appears only after verified read-back
- [ ] ADR-C15-C: Error identifies one precise recovery

---

### Case 16: performance numbers require measurement provenance

**Fixture variants:** model predicts 2ms/50MB; user budget; profiler evidence with
units/method/environment/date/hash; estimate source mismatches scope.

**Expected behavior:** unsupported prediction is HYPOTHESIS/UNKNOWN with validation
plan; user budget labeled owner; current profiler evidence may be sourced; mismatch
is finding. No number is presented as measured/verified without provenance.

**Assertions:**

- [ ] ADR-C16-A: Metric/baseline/budget/units/source/method are distinct
- [ ] ADR-C16-B: Validation names owner/environment/sample/threshold/decision impact
- [ ] ADR-C16-C: Author does not invoke profiling/estimate/implementation

---

### Case 17: GDD, registry, other ADR, and story boundaries remain read-only

**Fixture variants:** technical name differs from GDD; product rule would change;
registry global conflict; Blocks names story; successor proposal names old ADR.

**Expected behavior:** ADR/TECH maps terms; GDD PRODUCT RULE blocks/design-owner
handoff; registry align/supersede/scoped exception candidate only; dependency event
is conditional; predecessor/story/registry/GDD remain byte-identical.

**Assertions:**

- [ ] ADR-C17-A: No “ADR + update GDD” or registry projection write
- [ ] ADR-C17-B: No Blocked->Ready story transition
- [ ] ADR-C17-C: Exact non-write hashes remain unchanged

---

### Case 18: authoring receipt failure cannot create review handoff

**Fixture:** target reaches content-derived CONTENT_COMPLETE and stable read-back,
but checkpoint/authoring receipt append fails or receipt verification mismatches.

**Expected behavior:** target completeness remains CONTENT_COMPLETE and Status
Proposed; Workflow PARTIAL; exact unreceipted hash; no review handoff; no replay/
revert.

**Assertions:**

- [ ] ADR-C18-A: Content completeness, workflow, review, lifecycle status separate
- [ ] ADR-C18-B: Receipt path/hash stays external without target cycle
- [ ] ADR-C18-C: Missing receipt cannot support acceptance/registry/readiness

---

### Case 19: independent review recommendation is not Accepted

**Fixture variants:** READY+receipt; self/wrong-schema/stale review; current
independent ACCEPT; REVISE/REJECT; recorder preimage mismatch; valid recorder CAS.

**Expected behavior:** author only emits cgs.architecture-review-request/v2 and
does not invoke review. Review is read-only/recommendation only. Only separate
recorder with current ACCEPT/receipt/eligibility/separation may CAS allowed status
and emit lifecycle record. All invalid variants remain Proposed.

**Assertions:**

- [ ] ADR-C19-A: Review and acceptance/lifecycle recorder are distinct identities/actions
- [ ] ADR-C19-B: Review record binds current ADR/receipt/context hashes
- [ ] ADR-C19-C: Status-only transition receipt binds pre/post hashes
- [ ] ADR-C19-D: Non-status change requires new receipt/review

---

### Case 20: staged P1 package and catalog claims are honest

**Fixture:** staged SKILL, continuation, metadata, and this spec; shared catalog row
still points to formal authoring spec with no executed-result updates.

**Expected behavior:** matrix contains ADR-S001..ADR-S040, Cases 1..20,
ADR-X001..ADR-X008, and explicit ADR-001..ADR-014 coverage. Candidate stages no
catalog change and does not call source checks an executed `$skill-test`.

**Assertions:**

- [ ] ADR-C20-A: Exclusive files agree on v2 contracts/state/review boundaries
- [ ] ADR-C20-B: Shared catalog remains untouched
- [ ] ADR-C20-C: Verification provenance is stated accurately

---

## Cross-skill compatibility

- [ ] ADR-X001: Four decision classes and exact-body approvals match authoring provenance contracts
- [ ] ADR-X002: Bounded context/canonical manifest/mutable-target-baseline match authoring contracts
- [ ] ADR-X003: Allocation receipt plus ABSENT CAS provides collision-safe unique ID/path
- [ ] ADR-X004: Section checkpoints/five-part CAS/revisions preserve collaborator and non-target bytes
- [ ] ADR-X005: Receipt failure separates content completeness from Workflow Verdict/review handoff
- [ ] ADR-X006: GDD/engine/registry/story/lifecycle owners remain external and read-only
- [ ] ADR-X007: Independent review consumes target+authoring receipt but cannot accept; recorder owns transition
- [ ] ADR-X008: Final output emits one uninvoked owner/evidence handoff or Stop

## Coverage Notes

- ADR-001..ADR-005 remain covered by Proposed/Unknown-only authoring, strict
  cross-write boundary, sequential lifecycle separation, and current-hash review.
- ADR-006: Cases 2/3 and ADR-S006/S007 implement collision-safe ID/path allocation.
- ADR-007: Case 4 and ADR-S008 implement semantic duplicate routing.
- ADR-008: Case 6 and ADR-S016/S017 bound context deterministically.
- ADR-009: Cases 7/12 and ADR-S020/S021 make UNKNOWN blocking and validate graph.
- ADR-010: Cases 10/11 and ADR-S028/S029 define consultation timeout/failure/partial.
- ADR-011: Case 7 and ADR-S018/S019 require reference provenance/coverage.
- ADR-012: Case 9 and ADR-S025/S026 provide section checkpoints/resume.
- ADR-013: Case 5 and ADR-S009/S010 use one authorization and single target boundary.
- ADR-014: Cases 12/14 and ADR-S015/S021 validate dependency/replacement cycles.
- Shared catalog/results and downstream consumers require separate ownership; this
  candidate does not modify them or claim an executed test run.
