# Art Bible — Required workflow continuation

This file is normative. It begins only after the main skill validated
`cgs.art-bible-request/v2`, established one authorized mutation boundary, loaded
bounded current context, and created/migrated the full AB-1 skeleton safely.

## Phase 5: Decision provenance, approval, and section transaction

Process one selected stable section at a time:

    Context -> Decision Classification -> Question -> Options -> Decision
    -> Draft -> Semantic Preflight -> Exact-Body Approval
    -> Five-Part CAS -> Atomic Write -> Revision -> Checkpoint

Exact-body approval confirms content inside the authorized boundary. It does not
reauthorize files, establish independent review, or approve production.

### Decision classes and records

Every material statement used by a section references one or more stable
`ABDEC-<artifact-id>-<NNN>` records. Use the common authoring classes:

| Class | Authority and treatment |
|---|---|
| `product-choice` | Named product owner selects one option after meaningful tradeoffs; only this class can choose visual identity, mood, composition, palette role, typography personality, character/environment direction, HUD/VFX language, or production-facing preference. |
| `evidence-backed-hard-constraint` | Current owned source directly requires a platform/accessibility/engine/budget/legal constraint; preserve exact source ID/owner/path/locator/revision and do not ask the user to vote it away. |
| `derived-design-constraint` | Author derives a visual implication from accepted product choices/current hard evidence; show derivation/assumptions and require named product-owner acceptance before use. |
| `technical-handoff` | Implementation/architecture/pipeline/test question is routed to its external owner and remains outside the Art Bible product truth. |

Record:

    id: ABDEC-<artifact-id>-<NNN>
    section_id: AB-<NN>
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    owner: <actual identity or source owner>
    recorder_task_id: <actual author identity>
    question: <decision/question>
    options: [{id, value, tradeoffs, evidence_refs}]
    selected: <option ID / hard constraint / handoff>
    rationale: <owner rationale or derivation>
    source_refs: [{id, owner, path, locator, revision}]
    assumptions: []
    dependent_assertion_ids: []
    status: ACCEPTED | PROVISIONAL | ROUTED | SUPERSEDED
    accepted_at_utc: <RFC3339 seconds Z | null>

Never label a model/consultant inference as a user decision. Product choices and
derived constraints require actual named-owner acceptance. A hard constraint
requires current owned evidence. A handoff cannot become section truth until its
owner returns current evidence and it is reclassified.

For every unresolved product choice, present two or three materially different
options with visual benefit, readability/accessibility effect, production cost,
and reversibility. Ask the user to decide. Do not manufacture a default decision.

### Hard evidence versus visual tradeoffs

- A current platform/engine/accessibility/legal limit is a hard constraint and
  automatically bounds the draft.
- Conflicting hard sources produce a BLOCKING dependency finding; the author
  cannot choose which source wins.
- A product-facing art/readability, fidelity/performance, density/clarity, or
  distinctiveness/cost tradeoff is a product-choice with options for the user.
- A proposed visual interpretation of a hard budget is a derived constraint and
  still needs product-owner acceptance.
- AB-08 art-versus-UX conflicts name both owners/evidence and require user choice
  unless one side is a non-waivable accessibility constraint.
- AB-09 separates sourced hard budgets from visual production preferences.

### Semantic preflight and exact-body approval

Draft only the current section from accepted decisions and current evidence. Show
the complete proposed section body and a short provenance table.

Before approval:

1. run every applicable `cgs.art-bible-content-profile/v2` assertion;
2. confirm every material statement maps to accepted decision IDs;
3. confirm source paths/locators/revisions and owner boundaries are current;
4. reject copied product truth owned by concept/GDD/UX/accessibility/technical
   artifacts; reference their stable IDs instead;
5. identify contradictions, unresolved handoffs, provisional assumptions,
   unlicensed references, and implementation prescriptions;
6. re-read target, section baseline, used external context, authorization, and
   approved draft bytes; and
7. list dependency findings before asking for approval.

If preflight changes the body, show it again. Approval never carries to changed
bytes. Store:

    id: ABAPR-<artifact-id>-<section-id>-<NNN>
    owner: <actual product-decision owner>
    section_id: <AB ID>
    approved_body_revision: <revision>
    decision_ids: []
    assertion_result_revision: <revision>
    context_manifest_revision: <revision>
    target_baseline_revision: <revision>
    authorization_revision: <revision>
    approved_at_utc: <RFC3339 seconds Z>

Approval denied or exhausted revision rounds leaves the section INCOMPLETE and
appends a PARTIAL checkpoint with the next unresolved decision; never infer yes.

### Five-part CAS, atomic patch, and revision provenance

Immediately before every target write, one transaction attempt must pass:

1. **Target CAS** — current raw target equals expected baseline/previous verified
   write revision;
2. **Section CAS** — selected stable-ID body equals its approved baseline and
   unique anchors remain unambiguous;
3. **Context CAS** — every external source used by the body and the ordered
   context-manifest revision still match; mutable target is excluded here;
4. **Authorization CAS** — manifest/revision/authority, exact operation/section/path,
   approved-body revision, and limits still match; and
5. **Writer CAS** — actual target writer identity equals the authorized identity.

Mismatch returns `ERROR — CONCURRENT TARGET CHANGE`,
`ERROR — CONTEXT EVIDENCE CHANGED`, or
`ERROR — AUTHORIZATION/WRITER CHANGED`, with no transaction write.

The target writer atomically replaces only the selected stable-ID body plus
authorized header fields, reads back bytes, and proves every out-of-scope byte
range unchanged. Then append:

    id: ABREV-<artifact-id>-<section-id>-<NNN>
    mode: create | fill-gaps | revise-sections | migrate-schema
    section_id: <AB ID>
    before_target_revision: <revision>
    after_target_revision: <revision>
    before_section_revision: <revision or ABSENT>
    after_section_revision: <revision>
    decision_ids: []
    approval_id: <ABAPR ID>
    source_revisions: []
    authorization_revision: <revision>
    writer_task_id: <actual identity>
    operation: insert | replace | move-without-edit
    timestamp_utc: <RFC3339 seconds Z>

Append its `cgs.art-bible-checkpoint/v2` through predecessor/create-if-absent
CAS. If checkpoint persistence fails after verified target bytes, preserve the
content, return Workflow Verdict PARTIAL, report the exact unreceipted target
revision, emit no review handoff, and never replay the target patch.

## Phase 6: cgs.art-bible-content-profile/v2 assertions

Each assertion has stable ID, applicability, PASS/FAIL, evidence references,
owner, and failure reason. Non-placeholder length is never sufficient.

### AB-01 Visual Identity Statement

- `AB1-01`: one concise identity rule states intended perception without naming
  a source artist/style to imitate;
- `AB1-02`: three to five distinct visual principles define positive behavior;
- `AB1-03`: each principle has at least one observable pass/fail pillar test;
- `AB1-04`: scope and deliberate exclusions/prohibitions are explicit; and
- `AB1-05`: rules trace to current concept/pillar evidence and ABDEC IDs.

### AB-02 Mood, Lighting & Atmosphere

- `AB2-01`: named gameplay/narrative states map to intended emotion;
- `AB2-02`: key/fill/contrast/value/readability behavior is specified per state;
- `AB2-03`: atmosphere/weather/time transitions include continuity limits;
- `AB2-04`: camera/readability/accessibility conflicts have owned resolution; and
- `AB2-05`: rules are testable references, not only adjective lists.

### AB-03 Shape, Composition & Silhouette

- `AB3-01`: character/environment/UI shape grammars and contrast are distinct;
- `AB3-02`: composition, focal hierarchy, negative space, and camera contexts are
  specified;
- `AB3-03`: critical silhouettes/readability have observable scale/distance tests;
- `AB3-04`: density and clutter limits name owned evidence/decisions; and
- `AB3-05`: exceptions and prohibited forms are explicit.

### AB-04 Color System & Accessibility

- `AB4-01`: palette roles are semantic and trace to stable decisions;
- `AB4-02`: dominance/accent/neutral/feedback area or contrast relationships are
  measurable;
- `AB4-03`: every critical color meaning has a non-color backup cue;
- `AB4-04`: accessibility requirements reference their external owner/ID/revision;
- `AB4-05`: lighting/post-process interactions and exceptions are covered.

### AB-05 Typography & Iconography

- `AB5-01`: type hierarchy, personality, weights/scales, and fallback behavior are
  defined without treating font names as the whole rule;
- `AB5-02`: measurable legibility and text-scale constraints cite current UX/
  accessibility evidence;
- `AB5-03`: icon grammar, stroke/fill/metaphor/state rules are defined;
- `AB5-04`: localization/dynamic text and input-glyph ownership are referenced;
- `AB5-05`: rights/licensing dependencies are owned and current.

### AB-06 Character Art Direction

- `AB6-01`: archetype/faction differentiation traces to owned product evidence;
- `AB6-02`: silhouette, proportion, costume/material, pose, and expression rules
  are defined;
- `AB6-03`: camera/distance/LOD/readability variants are explicit;
- `AB6-04`: customization/equipment intersections name external owners; and
- `AB6-05`: prohibited stereotypes, unsafe copying, and exception rules exist.

### AB-07 Environment & Level Art Direction

- `AB7-01`: architecture/material/biome grammars and faction/region differences
  trace to current owner evidence;
- `AB7-02`: density, landmark, traversal cue, and focal hierarchy rules exist;
- `AB7-03`: environmental storytelling elements distinguish required fact from
  art treatment;
- `AB7-04`: lighting/weather/destruction/state variants are covered; and
- `AB7-05`: level-design collision/navigation rules are referenced, not reowned.

### AB-08 UI/HUD & VFX Visual Language

- `AB8-01`: HUD/UI hierarchy, surfaces, motion, icon/color relationships reference
  current UX IDs/revisions;
- `AB8-02`: VFX grammar covers shape, timing, intensity, semantic family, and
  contention/readability limits;
- `AB8-03`: reduced-motion, photosensitivity, non-color, and text/readability
  obligations reference their external owners;
- `AB8-04`: art-versus-UX conflicts have explicit owner decisions/findings; and
- `AB8-05`: art treatment does not replace interaction or accessibility truth.

### AB-09 Asset Standards, References & Prohibitions

- `AB9-01`: engine/platform/profile IDs, versions, paths, and revisions are current;
- `AB9-02`: sourced hard budgets distinguish geometry, texture, shader, animation,
  VFX, UI, memory, and performance applicability;
- `AB9-03`: formats, color spaces, naming, variants, LOD/import/validation handoffs
  identify technical owners rather than invent implementation;
- `AB9-04`: reference entries name source, rights status, specific reusable
  element, required divergence, and legal-review need;
- `AB9-05`: prohibitions include living-artist imitation and unlicensed copying;
- `AB9-06`: missing engine/platform evidence makes section PROVISIONAL/INCOMPLETE,
  never production-standard COMPLETE.

`NOT_APPLICABLE` is permitted only for an individual assertion whose profile
explicitly allows it, with accepted `ABDEC` rationale and owner; no AB-1 section
itself is optional.

## Phase 7: Concept, platform, dependency, and cross-reference gate

### Concept evidence

Treat a concept file's existence as evidence of bytes only. Current approval
requires exact artifact ID/path/revision/status plus an immutable approval record
ID/path/revision/reviewer and a matching approved concept revision. Missing, stale,
unapproved, or self-reported evidence permits safe DRAFT/PARTIAL authoring but:

- creates an OPEN BLOCKING `concept-approval` finding;
- keeps dependent evidence PROVISIONAL/MISSING;
- prevents artifact COMPLETE, authoring review handoff, and production use; and
- must be reported honestly as `DRAFT_ONLY`, never “approved concept”.

### Platform/engine evidence

Persist current platform and engine profile IDs, versions, paths, revisions, owners,
and applicable budget locators in the checkpoint and AB-09 evidence refs.
Temporary user answers may be PROVISIONAL derived constraints but cannot replace
owned profiles. Missing profiles make AB-09 PROVISIONAL/INCOMPLETE. When a profile
appears or changes, mark AB-09 and dependent sections STALE before further claims.

### Dependency finding contract

Use `cgs.art-bible-dependency-finding/v1`:

    id: ARBF-<artifact-id>-<check-id>-<stable business key>
    severity: BLOCKING | ADVISORY
    category: concept-approval | platform-engine | accessibility | ux |
      product-owner | technical-owner | rights | schema | provenance | catalog
    evidence: {path, artifact_or_requirement_id, locator, revision, observed}
    expected: <objective rule>
    owner: <resolution owner>
    destination: <artifact/workflow>
    acceptance: <objective close condition>
    first_seen_target_revision: <revision>
    last_evaluated_target_revision: <revision>
    status: OPEN | RESOLVED | WAIVED
    resolution: <current-revision evidence or null>

stable business key deterministically covers category, owner, source ID/locator,
expected, and normalized observed facts. Preserve IDs across reevaluation.
RESOLVED requires current evidence satisfying acceptance. `BLOCKING WAIVED`
remains unresolved and prevents COMPLETE/review handoff/production eligibility;
user risk acceptance cannot close an external-owner gap.

Run cross-section checks for concept/pillar consistency, palette/lighting/
typography/icon/VFX semantics, character/environment/UI shape distinction,
accessibility and UX ownership, engine/platform/budget applicability, references/
rights/prohibitions, decision/approval/revision provenance, and exact nine-section
cardinality. Record every failure as an assertion or finding before status.

## Phase 8: Bounded consultations and failure handling

Consultation and review are different. Consultants are read-only advisers and
cannot approve content, make product choices, edit files, invoke other agents, or
become the future independent reviewer.

In `solo` or `consultation_mode: none`, spawn zero consultants/directors. In
`bounded` mode:

- at most one consultant per section;
- at most three consultations per run;
- at most two concurrently;
- one bounded question and one 60-second attempt;
- no automatic retry or nested delegation; and
- canceled/late result token is revoked and output quarantined.

Record:

    id: ABCON-<run-id>-<NNN>
    section_id: <AB ID>
    role: ux-designer | technical-artist | accessibility-specialist | other-declared
    question: <one evidence question>
    input_paths_revision: []
    required: true | false
    started_at_utc: <timestamp>
    deadline_seconds: 60
    status: complete | partial | timeout | failed | side-effect | skipped
    output_revision: <canonical revision or null>
    evidence_summary: <bounded evidence or null>
    fallback: none | explicit-product-decision | section-blocked

Optional non-complete consultation may continue only when the missing input is
not required evidence and the product owner explicitly decides a remaining
product choice; record fallback. Required non-complete, malformed, side-effect,
or late input marks the dependent section BLOCKED/INCOMPLETE, appends a PARTIAL
checkpoint, and stops that section. Never fabricate or merge quarantined output.

## Phase 9: Artifact completeness, final CAS, and authoring receipt

Re-evaluate all nine sections, assertions, current concept approval, external
context revisions, findings, decisions, approvals, revisions, migration disposition,
and platform/engine state. Distinguish:

- `selected_scope_complete`: every selected section reached WRITTEN and its body
  approval/assertions are current; and
- `artifact_complete`: all nine unique AB-1 sections satisfy the COMPLETE contract.

Selected scope may be complete while artifact status remains PARTIAL.

Before final status/header write, rerun the five-part CAS and prove only authorized
header fields change. Read back final target and append the final
`cgs.art-bible-authoring-receipt/v1` only after stable final bytes exist. Receipt
verification revalidates declared target, all section/revision/decision/approval revisions,
context revision, authorization, roles, findings, and final checkpoint predecessor.

Set artifact status from content only, then Workflow Verdict separately:

- DRAFT/PARTIAL target: Workflow Verdict PARTIAL, no review handoff;
- COMPLETE target plus verified receipt and `review_mode: full`: Workflow Verdict
  READY_FOR_REVIEW and exact independent review handoff;
- COMPLETE target in lean/solo: Workflow Verdict COMPLETE_UNREVIEWED, no formal
  review handoff, production blocked;
- COMPLETE target but receipt persistence/verification failure: retain target
  status COMPLETE, Workflow Verdict PARTIAL, no review handoff, report exact
  unreceipted target revision;
- unsafe identity/authorization/owner/drift: preserve last safe content status,
  Workflow Verdict BLOCKED;
- invalid unsupported input/corrupt evidence before safe work: ERROR with no false
  artifact status.

Never report APPROVED or production eligible from authoring evidence.

## Phase 10: Independent review and approval-evidence handoff

For eligible full mode, return a conversation handoff for a fresh independent
`art-director` task using `AD-ART-BIBLE`. Do not spawn it. Bind:

- exact target path/current revision and AB-1/profile/author schema;
- all nine section revisions and assertion-result revision;
- concept/platform/engine/accessibility/UX/product evidence paths and revisions;
- context-manifest revision, decisions/approvals/revisions/findings;
- authoring receipt ID/path/revision and author/consultant/recorder identities; and
- required immutable review output contract `cgs.art-bible-review/v1`.

The future reviewer must be fresh, different from every author/consultant/
recorder, artifact-read-only, re-read before and after, review all nine sections,
and create one separately authorized immutable record with verdict `APPROVE`,
`CONCERNS`, or `REJECT`. It never edits the Art Bible or authoring receipt.

Only a separately verified `APPROVE` record matching current target, authoring
receipt, section/dependency revisions, role separation, and `AD-ART-BIBLE` may make
production use eligible. `CONCERNS`, `REJECT`, stale/missing receipt, wrong role,
self-review, changed target/context, or user risk acceptance remains blocked. A
changed target requires a new authoring receipt and fresh review record; never
overwrite immutable evidence.

## Phase 11: Resume, recovery, and catalog-driven close

On `resume`, validate exact request/checkpoint roots and full
`cgs.art-bible-checkpoint/v2` predecessor/payload chain, artifact/run/schema,
authorization, target/context, roles, section axes/assertions, decisions/
approvals/revisions, consultations/findings, budgets, and absence of late writes.

- all revisions current: resume APPROVED_NOT_WRITTEN exact bytes first, otherwise the
  next PENDING legal section;
- target mismatch: BLOCKED — TARGET/AUTHORIZATION DRIFT, zero write;
- external source mismatch: mark only dependent sections STALE, invalidate active
  receipt/review handoff, and require new decision/preflight;
- profile/author schema mismatch: require authorized migrate-schema;
- unsupported checkpoint: ERROR — UNSUPPORTED CHECKPOINT SCHEMA;
- missing checkpoint: resume unavailable.

Conversation memory never reconstructs approval, decision provenance, receipt,
review, or revisions.

Determine the next workflow only from the exact request-declared workflow-catalog
artifact/row/locator/revision and its explicit stable prerequisite artifact IDs,
statuses, and receipts. Do not treat `design/gdd/*.md`, a concept/index filename,
directory existence, or arbitrary documents as evidence that design-system is
done. If catalog evidence is missing, stale, ambiguous, or does not identify one
legal successor, return `STOP — WORKFLOW STATUS UNKNOWN` with one named evidence
gap. Never modify shared catalog/workflow files here.

Final result lists artifact/run IDs, operation/scope and both completion states,
profile/content/author schema, target pre/post/revision, context revision, concept/
platform evidence, section axes/assertions, decision/approval/revision IDs,
consultations/findings, authorization/writer/recorder identities, checkpoint and
receipt ID/path/revision, review-handoff eligibility, production-use decision,
preserved legacy content, non-writes, and exactly one evidence-backed next action.
