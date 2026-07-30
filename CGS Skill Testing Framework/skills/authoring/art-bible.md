# Skill Test Spec: $art-bible

## Skill Summary

`$art-bible` authors or safely revises exactly one nine-section AB-1 Art Bible
from `cgs.art-bible-request/v2`. It uses `art-bible-profile-schema-v2`,
`cgs.art-bible-content-profile/v2`, bounded current evidence, explicit decision/
approval/revision provenance, five-part CAS, append-only checkpoint v2 records,
and an external `cgs.art-bible-authoring-receipt/v1`.

Artifact completeness, authoring workflow outcome, independent review, and
production eligibility are separate states. This authoring workflow does not
invoke review or asset production.

## Canonical AB-1 section IDs

1. `AB-01` Visual Identity Statement
2. `AB-02` Mood, Lighting & Atmosphere
3. `AB-03` Shape, Composition & Silhouette
4. `AB-04` Color System & Accessibility
5. `AB-05` Typography & Iconography
6. `AB-06` Character Art Direction
7. `AB-07` Environment & Level Art Direction
8. `AB-08` UI/HUD & VFX Visual Language
9. `AB-09` Asset Standards, References & Prohibitions

Titles are display text. Stable IDs define identity, range, migration, assertions,
decisions, approvals, revisions, and receipts.

## Static Assertions

- [ ] ARB-S001: Frontmatter contains only matching `name` and non-empty `description`
- [ ] ARB-S002: Invocation requires one cgs.art-bible-request/v2 manifest; no-arg stops before repository reads
- [ ] ARB-S003: Author schema revisions exact SKILL bytes, NUL, and required continuation bytes
- [ ] ARB-S004: Profile/content contracts are art-bible-profile-schema-v2 and cgs.art-bible-content-profile/v2
- [ ] ARB-S005: AB-01 through AB-09 occur exactly once and titles are not identity
- [ ] ARB-S006: Target header has stable artifact/receipt IDs but no APPROVED, reviewer signature, receipt path, or receipt revision
- [ ] ARB-S007: Content/evidence/workflow/assertion/section-status axes are independent
- [ ] ARB-S008: review_mode and consultation_mode are separate contracts
- [ ] ARB-S009: solo forces consultation none and spawns zero subagents/directors
- [ ] ARB-S010: One mutation authorization covers exact target/checkpoint/sections; content approval does not reauthorize
- [ ] ARB-S011: Context order is deterministic with hard 16-file/524288-byte limits
- [ ] ARB-S012: Context overflow can append only one authorized PARTIAL checkpoint and leaves target unchanged
- [ ] ARB-S013: Concept approval requires artifact/record identity and matching current revisions
- [ ] ARB-S014: Missing/stale/unapproved concept is DRAFT_ONLY and blocks COMPLETE/review handoff
- [ ] ARB-S015: Four authoring decision classes have stable ABDEC records
- [ ] ARB-S016: User/source/author/consultant identities are recorded truthfully
- [ ] ARB-S017: Every substantive visual choice follows Question/Options/Decision/Draft/Approval
- [ ] ARB-S018: ABAPR binds exact approved body, decisions, assertions, context, target baseline, and authorization
- [ ] ARB-S019: Every section uses deterministic content assertions; non-placeholder text is insufficient
- [ ] ARB-S020: fill-gaps/revise-sections/migrate-schema have distinct lossless mutation semantics
- [ ] ARB-S021: Hard evidence constrains automatically; product visual tradeoffs require owner choice; conflicting hard sources block
- [ ] ARB-S022: Missing engine/platform profile makes AB-09 PROVISIONAL/INCOMPLETE and later change makes dependencies STALE
- [ ] ARB-S023: Dependency findings use cgs.art-bible-dependency-finding/v1 stable business key/owner/resolution state
- [ ] ARB-S024: Consultation is one/section, three/run, two concurrent, one 60-second attempt, no retry/nesting, typed failure/quarantine
- [ ] ARB-S025: Every target write uses Target/Section/Context/Authorization/Writer CAS
- [ ] ARB-S026: ABREV binds before/after target/section revisions, decisions, approval, sources, authorization, and actual writer
- [ ] ARB-S027: Checkpoints use cgs.art-bible-checkpoint/v2 append-only predecessor CAS
- [ ] ARB-S028: cgs.art-bible-authoring-receipt/v1 is external authoring evidence without target/receipt revision cycle
- [ ] ARB-S029: Receipt/checkpoint failure preserves target content status but returns workflow PARTIAL with no review handoff
- [ ] ARB-S030: Selected-scope completion and nine-section artifact COMPLETE are separate
- [ ] ARB-S031: Eligible full mode emits only a revision-bound handoff to a fresh independent art-director AD-ART-BIBLE task
- [ ] ARB-S032: Authoring never invokes review, writes a review record, self-approves, or uses creative-director
- [ ] ARB-S033: Production eligibility requires external cgs.art-bible-review/v1 APPROVE matching current target/receipt/context and separation
- [ ] ARB-S034: Close uses exact workflow-catalog row/artifact/status/receipt evidence, never arbitrary GDD glob/existence
- [ ] ARB-S035: Metadata names AB-1, request v2, bounded evidence, CAS/receipt, and independent handoff consistently
- [ ] ARB-S036: Shared catalogs, assets, engine setup, implementation, and production remain non-writes

---

## Behavioral Cases

### Case 1: no argument has zero side effects

**Input:**

    $art-bible

**Expected behavior:** print exact manifest-path usage and stop before repository
discovery, target/context reads, delegation, authorization, or writes.

**Assertions:**

- [ ] ARB-C01-A: Usage identifies cgs.art-bible-request/v2
- [ ] ARB-C01-B: Zero repository reads/writes and zero agents
- [ ] ARB-C01-C: No artifact/workflow/review verdict is fabricated

---

### Case 2: fresh core scope writes full skeleton first

**Fixture:** valid create request; target ABSENT; current approved concept; scope
core AB-01..AB-04; exact target/checkpoint boundary authorized.

**Expected behavior:** bounded context succeeds; first target write contains
header and exactly AB-01..AB-09; unselected bodies are neutral placeholders;
substantive bodies follow approved decisions later.

**Assertions:**

- [ ] ARB-C02-A: Skeleton precedes substantive content
- [ ] ARB-C02-B: Exactly nine unique IDs and all state axes initialized
- [ ] ARB-C02-C: Final selected scope may complete but artifact is PARTIAL
- [ ] ARB-C02-D: Production blocked and no review handoff

---

### Case 3: selected scope completion is not whole completeness

**Fixture variants:** only core completes; only AB-09 completes; resume completes
all selected IDs while another AB-1 section is incomplete/stale.

**Expected behavior:** `selected_scope_complete: true`; artifact PARTIAL; no
whole-artifact review/approval/production claim.

**Assertions:**

- [ ] ARB-C03-A: Unselected states remain visible
- [ ] ARB-C03-B: SECTION_REVIEWED does not promote artifact status
- [ ] ARB-C03-C: No cgs.art-bible-review/v1 or production handoff is created

---

### Case 4: review and consultation modes are independent

**Fixture variants:** full+none; lean+bounded; solo with requested bounded.

**Expected behavior:** full+none uses zero authoring consultants and may later
emit review handoff; lean may consult within caps but never emits formal review
handoff; solo forces none and spawns zero agents/directors.

**Assertions:**

- [ ] ARB-C04-A: Review mode never silently enables section delegation
- [ ] ARB-C04-B: Consultant never consumes future reviewer identity
- [ ] ARB-C04-C: Solo has local user-driven fallback and zero agents

---

### Case 5: every substantive section choice has truthful provenance

**Fixture:** authoring AB-02, AB-05, and AB-07 includes mood, type personality,
and environment-density choices plus one sourced accessibility constraint.

**Expected behavior:** each product choice receives options/tradeoffs and actual
owner selection; hard evidence is recorded as source-owned; derived implications
are shown and accepted; exact final bodies receive ABAPR approval.

**Assertions:**

- [ ] ARB-C05-A: ABDEC classes and identities are truthful
- [ ] ARB-C05-B: Consultant/model output is never mislabeled user choice
- [ ] ARB-C05-C: Changed body invalidates earlier approval
- [ ] ARB-C05-D: Section write references accepted decisions and approval

---

### Case 6: retrofit completeness uses content assertions

**Fixture variants:** long but contradictory AB-04; non-placeholder AB-05 missing
legibility; old AB-09 budgets with changed platform; valid current AB-06.

**Expected behavior:** assertions derive INVALID/INCOMPLETE/STALE/COMPLETE rather
than preserving any non-placeholder body as complete; fill-gaps cannot overwrite
substantive bodies; revision requires explicit scope.

**Assertions:**

- [ ] ARB-C06-A: Assertion IDs/evidence/failures are recorded
- [ ] ARB-C06-B: Contradiction is INVALID and changed evidence is STALE
- [ ] ARB-C06-C: Only valid/current/approved body can be COMPLETE

---

### Case 7: concept file existence is not approval

**Fixture variants:** concept exists with no approval record; approval revision names
old concept bytes; current immutable approval matches artifact ID/revision.

**Expected behavior:** first two create stable BLOCKING concept findings and permit
only DRAFT/PARTIAL authoring; third may satisfy concept dependency after full
identity/revision validation.

**Assertions:**

- [ ] ARB-C07-A: Missing/stale evidence is reported DRAFT_ONLY
- [ ] ARB-C07-B: No COMPLETE/review handoff/production eligibility without current approval
- [ ] ARB-C07-C: File existence/status prose cannot substitute for approval record

---

### Case 8: bounded context order and overflow are reproducible

**Fixture:** declared candidates exceed 16 files or 524288 exact bytes; a required
concept/platform source would fall beyond the cap.

**Expected behavior:** selection uses normative order and pre-load sizes; required
source is not silently omitted; at most one authorized PARTIAL checkpoint records
loaded/omitted evidence; target stays unchanged.

**Assertions:**

- [ ] ARB-C08-A: Same manifest yields same ordered context revision
- [ ] ARB-C08-B: No truncation, broad GDD/art scan, or second-hop expansion
- [ ] ARB-C08-C: CONTEXT_BUDGET_EXCEEDED and no target write

---

### Case 9: consultation failure is bounded and resumable

**Fixture variants:** required technical-artist times out; optional UX consultant
returns partial; consultant edits a file; late output arrives after cancellation.

**Expected behavior:** one typed ABCON result records status/evidence/fallback;
no retry/nested delegation; required failure blocks its section and checkpoints;
side-effect/late output is quarantined.

**Assertions:**

- [ ] ARB-C09-A: Caps are one/section, three/run, two concurrent, one 60s attempt
- [ ] ARB-C09-B: Failure never fabricates section content/completeness
- [ ] ARB-C09-C: Checkpoint identifies exact next safe action

---

### Case 10: hard constraints and product tradeoffs have different owners

**Fixture:** AB-08 art treatment conflicts with UX readability; AB-09 preference
exceeds one current hard budget; two hard sources conflict.

**Expected behavior:** UX/art product tradeoff shows options for user decision;
hard budget constrains automatically; visual interpretation is derived and
accepted; conflicting hard sources block their owner resolution.

**Assertions:**

- [ ] ARB-C10-A: Model does not silently resolve product tradeoff
- [ ] ARB-C10-B: User cannot vote away sourced non-waivable hard evidence
- [ ] ARB-C10-C: Conflicting hard sources remain blocking, not model-selected

---

### Case 11: missing engine or platform keeps AB-09 provisional

**Fixture variants:** no configured engine/platform profile; temporary user budget
answer; profile later appears or changes.

**Expected behavior:** AB-09 evidence and relevant decisions are PROVISIONAL/
INCOMPLETE; temporary answer does not become production standard; new/changed
profile marks AB-09 and dependents STALE for re-preflight.

**Assertions:**

- [ ] ARB-C11-A: Profile IDs/versions/paths/revisions/owners are persisted when current
- [ ] ARB-C11-B: Artifact cannot become COMPLETE from provisional AB-09
- [ ] ARB-C11-C: setup/engine configuration is a handoff, not performed here

---

### Case 12: legacy schema migration is lossless and separate from authoring

**Fixture:** old/duplicate/unknown headings, one combined UI/Typography/VFX body,
and one unmapped paragraph.

**Expected behavior:** read-only mapping covers every source byte range/revision,
split/merge ambiguity, exact destination and preserved disposition; accepted
migration CAS writes structure only; unmapped content remains appendix and blocks
COMPLETE.

**Assertions:**

- [ ] ARB-C12-A: Titles never substitute for stable IDs
- [ ] ARB-C12-B: Every original byte is preserved or explicitly dispositioned
- [ ] ARB-C12-C: Migration alone grants no completeness/approval

---

### Case 13: five-part CAS rejects concurrent drift

**Fixture variants:** target changes after approval; selected section anchor/body
changes; used context changes; authorization changes; wrong writer attempts patch.

**Expected behavior:** corresponding Target/Section/Context/Authorization/Writer
CAS fails; target/checkpoint transaction is not written; collaborator bytes are
not overwritten.

**Assertions:**

- [ ] ARB-C13-A: All five CAS facets execute immediately before write
- [ ] ARB-C13-B: Approved draft cannot apply to changed baseline/context
- [ ] ARB-C13-C: Error identifies drift class and one legal recovery

---

### Case 14: receipt failure cannot create a review handoff

**Fixture:** final target reaches content-derived COMPLETE and reads back stably;
final checkpoint/authoring-receipt append then fails or verifies incorrectly.

**Expected behavior:** target content status remains COMPLETE; Workflow Verdict is
PARTIAL; exact unreceipted target revision is reported; no review handoff; target write
is not replayed/reverted.

**Assertions:**

- [ ] ARB-C14-A: Content status and workflow evidence remain separate
- [ ] ARB-C14-B: Receipt path/revision stays external and independently owned
- [ ] ARB-C14-C: Missing receipt remains production blocking

---

### Case 15: complete full-mode artifact emits correct independent handoff

**Fixture:** nine current COMPLETE sections; current approved concept/platform
evidence; zero blocking findings; verified authoring receipt; full mode.

**Expected behavior:** authoring stops with READY_FOR_REVIEW and a revision-bound
handoff for a fresh independent `art-director` `AD-ART-BIBLE` task. It does not
spawn reviewer or write review record. Wrong/self/author/consultant reviewer is
ineligible.

**Assertions:**

- [ ] ARB-C15-A: Handoff binds target/sections/context/receipt/provenance revisions
- [ ] ARB-C15-B: Reviewer identity separation is explicit
- [ ] ARB-C15-C: creative-director and inline self-review are prohibited
- [ ] ARB-C15-D: READY_FOR_REVIEW is not APPROVED or production eligible

---

### Case 16: external review remains revision-bound and immutable

**Fixture variants:** current valid external APPROVE; CONCERNS/REJECT; APPROVE for
old target revision; artifact/receipt/context changed after approval.

**Expected behavior:** only current matching APPROVE with role separation may make
production eligible; all other variants remain blocked; immutable old records are
preserved and never rewritten.

**Assertions:**

- [ ] ARB-C16-A: H2 cannot be approved by H1 evidence
- [ ] ARB-C16-B: User risk acceptance does not convert non-APPROVE verdict
- [ ] ARB-C16-C: Changed target requires new receipt and fresh review record

---

### Case 17: close uses catalog artifact evidence, not filename existence

**Fixture variants:** arbitrary `design/gdd/concept.md`; one unrelated GDD; exact
workflow-catalog row with stable prerequisite IDs/status/receipts; stale/ambiguous
catalog evidence.

**Expected behavior:** arbitrary files do not prove design-system done. Exact
current catalog evidence may yield one legal successor. Missing/stale/ambiguous
evidence returns `STOP — WORKFLOW STATUS UNKNOWN`; shared catalog is not edited.

**Assertions:**

- [ ] ARB-C17-A: No `design/gdd/*.md` existence heuristic
- [ ] ARB-C17-B: Next action cites exact catalog path/locator/revision and artifact IDs
- [ ] ARB-C17-C: Unknown state fails closed with one evidence gap

---

### Case 18: staged P1 package and catalog claims are honest

**Fixture:** staged SKILL, continuation, metadata, and this spec; live catalog row
still points to the formal spec path but has no executed-result fields.

**Expected behavior:** static matrix contains ARB-S001..ARB-S036, behavioral cases
1..18, cross-skill checks, and coverage ARB-001..ARB-013. Candidate does not stage
or claim catalog result updates without an executed authorized test workflow.

**Assertions:**

- [ ] ARB-C18-A: Exclusive files agree on v2 contracts and boundaries
- [ ] ARB-C18-B: Shared catalog remains untouched
- [ ] ARB-C18-C: Static/source verification is not mislabeled executed `$skill-test`

---

## Cross-skill compatibility

- [ ] ARB-X001: Four decision classes match staged authoring contracts
- [ ] ARB-X002: Context manifest/caps and mutable-target-baseline rules match authoring contracts
- [ ] ARB-X003: Content approval is exact-body evidence, never filesystem or review authority
- [ ] ARB-X004: Five-part CAS and ABREV provenance preserve collaborator changes
- [ ] ARB-X005: Checkpoint/receipt failure separates content status from Workflow Verdict
- [ ] ARB-X006: Concept/platform/UX/accessibility/technical owners remain external
- [ ] ARB-X007: Independent review consumes target plus authoring receipt; it is not invoked inline
- [ ] ARB-X008: Catalog-driven close is read-only and fails closed on stale/unknown evidence

## Coverage Notes

- ARB-001..ARB-004 remain covered by partial-versus-whole completeness, external
  correct-role review, skeleton-first persistence, and canonical stable IDs.
- ARB-005: Case 4 and ARB-S008/S009 separate review from consultation and preserve solo.
- ARB-006: Case 5 and ARB-S015..S018 require decisions and exact-body approval.
- ARB-007: Case 6 and ARB-S007/S019/S020 use content assertions and explicit states.
- ARB-008: Case 7 and ARB-S013/S014 validate revision-bound concept approval.
- ARB-009: Case 9 and ARB-S024 define caps, failure schema, checkpoint, and quarantine.
- ARB-010: Case 10 and ARB-S021 preserve owner-specific conflict decisions.
- ARB-011: Case 11 and ARB-S022 keep unconfigured standards provisional/stale.
- ARB-012: Case 17 and ARB-S034 require exact catalog evidence and fail closed.
- ARB-013: Cases 1..18, ARB-S001..S036, and ARB-X001..X008 replace drifted tests.
- Shared catalog/result fields and downstream consumers require separate ownership;
  this candidate intentionally does not modify them or claim an executed test run.
