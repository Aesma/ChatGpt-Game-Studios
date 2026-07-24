# UX Design — Required workflow continuation

This continuation is part of the ux-design author schema. Follow it only after
the main workflow has validated the v2 request, inventoried the target,
authorized one mutation boundary, loaded bounded current context, and created or
migrated the exact profile skeleton.

## Phase 5: Decision provenance and section transactions

Process only authorized stable section IDs in profile order unless the request
records a dependency-safe alternative. Each section uses:

    Context -> Decision Classification -> Questions -> Options -> Decision
    -> Draft -> Semantic Preflight -> Product Approval
    -> Transactional CAS -> Atomic Write -> Revision Record -> Checkpoint

Product approval confirms exact content inside the already authorized boundary.
Never request filesystem permission again while paths, sections, limits, owners,
and operation stay unchanged.

### Decision records

Every material statement traces to one stable record:

    id: UXDEC-<artifact-id>-<section-id>-<NNN>
    section_id: <stable ID>
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    authority: <user/product owner/source owner/derivation>
    source:
      path: <exact path or null>
      artifact_or_requirement_id: <stable ID or null>
      locator: <section/row/field or null>
      sha256: <raw hash or null>
    options: []
    selected: <outcome or routed question>
    inputs: []
    derivation: null
    assumptions: []
    provisional: true | false
    rationale: <reason>
    status: accepted | routed | blocked
    decided_at_utc: <RFC3339 seconds Z>

- product-choice is selected only by the named decision owner after two or
  three meaningful options/tradeoffs;
- evidence-backed-hard-constraint requires a current owner source and cannot be
  overridden in this artifact;
- derived-design-constraint preserves inputs/reasoning and user acceptance when
  it affects a product outcome;
- technical-handoff routes implementation/API/storage/test/architecture
  questions outside the UX artifact.

Platform/input/accessibility facts are hard constraints only when exact profile
IDs/versions/hashes validate. A temporary answer is provisional derived content,
creates an OPEN blocking finding, and cannot make a section CURRENT.

Consultants propose evidence only. They are never product decision owner, target
author, checkpoint recorder, accessibility-tier owner, global-library owner, or
review approver.

### Semantic preflight and approval

Draft only the current section from accepted decision records and current
evidence. Mark provisional statements and finding IDs visibly.

Before product approval:

1. run every applicable cgs.ux-content-profile/v2 assertion in Phase 6;
2. confirm every material choice/constraint maps to decision IDs;
3. confirm platform/accessibility/requirement/pattern/navigation references use
   exact stable IDs and current hashes;
4. reject implementation/QA/review material and content owned by another
   artifact;
5. detect duplicate component/element/pattern/event/finding/AC IDs;
6. compare all named owners/interfaces with bounded source evidence; and
7. record assertion failures and dependency findings before presenting approval.

If preflight changes the draft, show the full new body and rerun it. Earlier
approval never applies to changed bytes.

Ask approve exact body, revise, or stop. If stopped, preserve only
APPROVED_NOT_WRITTEN evidence when exact draft bytes and all bound hashes are in
the checkpoint; otherwise keep PENDING. Exceeding maximum three revision rounds
returns PARTIAL with one unresolved decision/finding.

### Transactional CAS, revision record, and checkpoint

Immediately before target write:

Treat the checks below as one five-part compare-and-set gate: **Target CAS**,
**Section CAS**, **Context CAS**, **Authorization CAS**, and **Writer CAS**. Every
part must pass against the authorized baseline in the same transaction attempt.

1. re-hash current target and selected section body;
2. re-hash every external context source used by the section plus the
   context-manifest digest; the mutable target is checked only by target/section
   CAS and is not treated as external context evidence;
3. revalidate authorization hash, writer identity, scope, approved draft bytes,
   and expected operation;
4. reject duplicate/ambiguous section anchors; and
5. confirm all out-of-scope byte ranges equal the checkpoint baseline/current
   hashes.

Mismatch returns ERROR — CONCURRENT TARGET CHANGE or
ERROR — CONTEXT EVIDENCE CHANGED with no transaction write.

The target writer replaces exactly one stable-ID region atomically and reads
back bytes. Verify only that region plus authorized header fields changed.

Append revision provenance:

    id: UXREV-<artifact-id>-<section-id>-<NNN>
    mode: create | fill-gaps | revise-sections | migrate-schema
    section_id: <stable ID>
    before_target_sha256: <hash>
    after_target_sha256: <hash>
    before_section_sha256: <hash or ABSENT>
    after_section_sha256: <hash>
    decision_ids: []
    source_hashes: []
    authorization_sha256: <hash>
    writer_task_id: <actual identity>
    operation: insert | replace | move-without-edit
    timestamp_utc: <RFC3339 seconds Z>

Then append one cgs.ux-design-checkpoint/v2 record through checkpoint-recorder
create-if-absent CAS. If receipt/checkpoint persistence fails after a verified
target write, leave the content-derived artifact Status unchanged, report
Workflow Verdict PARTIAL and the exact unreceipted target hash, emit no review
handoff, and never replay the write.

## Phase 6: cgs.ux-content-profile/v2 assertions

Heading/ID presence, non-empty prose, and absence of placeholder tokens are
necessary but not sufficient. Record PASS/FAIL for every assertion ID.

### ux-spec assertions

- UXS-01 purpose-requirement: player goal/outcome plus current requirement IDs
  and owners.
- UXS-02 arrival-context: prior activity/action, player state, pressure/urgency,
  and journey evidence or OPEN owned gap.
- UXS-03 navigation-position: stable screen IDs for root/parent/current and all
  alternate access, each source-hash-bound.
- UXS-04 entry-exit: every edge has trigger, source/destination ID, carried
  state, irreversible effect, and neighbor evidence.
- UXS-05 layout: exact required H3s; hierarchy precedes zones; component
  inventory has stable ID/content/interactivity/pattern/viewport; schematics
  declare platform profile/viewports/scales and are non-authoritative.
- UXS-06 states: default plus every applicable loading/empty/populated/error/
  locked/platform state; a not-applicable state has source-backed rationale.
- UXS-07 interaction: every interactive component across every declared input,
  focus order, multimodal feedback, outcome, cancel/back, error/recovery.
- UXS-08 events: every player action maps to stable event/payload/owner or
  source-backed none; UX does not become game-state owner.
- UXS-09 transitions: enter/exit/state changes, duration/trigger/interrupt, and
  reduced-motion equivalent.
- UXS-10 data: stable source owner, read/write intent, trigger/rate, null/empty/
  stale/error behavior, privacy/sensitivity.
- UXS-11 accessibility: every obligation traces to external foundation
  ID/version/tier/hash and covers applicable input, reflow, non-color, focus,
  announcements, and reduced motion.
- UXS-12 localization: exact string owner/profile, expansion/reflow/truncation,
  plural/gender, date/number, placeholder, and targeted bidi constraints.
- UXS-13 acceptance: every item satisfies the reference-first schema below.
- UXS-14 questions: every open item uses dependency-finding contract v1 with
  severity/owner/evidence/status/destination/acceptance/next action.

### hud-design assertions

- HUD-01 philosophy: accepted density principle, requirement/decision IDs, and
  measurable implications/conflicts.
- HUD-02 information: every declared requirement maps to item/owner and Must
  Show/Contextual/On Demand/Hidden decision.
- HUD-03 zones: exact platform-profile ID/version/hash, safe-zone, aspect,
  resolution, viewport, text-scale, focal/split-screen assumptions.
- HUD-04 elements: stable IDs, data owner/form/update/visibility/priority,
  null/error behavior, states, and pattern IDs.
- HUD-05 behavior: applicable exploration/combat/dialogue/cutscene/pause
  transitions, priority/contention/queue, density, reduced motion.
- HUD-06 variants: every declared platform/device/input/resolution/aspect/
  text-scale target; unsupported target is OPEN blocking gap.
- HUD-07 accessibility: foundation ID/tier/hash, non-color cues, reflow,
  assistive exposure, attention, focus, motion.
- HUD-08 questions: dependency-finding contract v1.

### interaction-pattern-library assertions

- PAT-01 overview: external library owner, canonical scope, consumers,
  content/profile/schema/context hashes.
- PAT-02 catalog: unique UXP-GLOBAL IDs, versions, status, category, exact
  anchors, source proposal IDs, owner.
- PAT-03 patterns: one entry/catalog ID with states, declared inputs, focus,
  cancel/back, multimodal feedback, accessibility/localization, data/event
  boundaries, use/non-use, current references.
- PAT-04 gaps: unmerged local UXP-<screen-id>-<slug> IDs, source screen/hash,
  requested disposition, owner, blocking status.
- PAT-05 questions: dependency-finding contract v1.

Only the dedicated library target/owner may write global patterns. Each pattern
patch uses target/entry/context CAS. Collision, stale base, duplicate semantics,
or unowned cross-screen behavior blocks.

## Phase 7: Reference-first acceptance criteria

UXS-13 items use:

    id: UXAC-<artifact-id>-<NNN>
    requirement_refs:
      - id: <stable requirement ID>
        owner: <artifact owner>
        path: <exact source path>
        locator: <section/row>
        sha256: <raw hash>
    decision_refs: [<UXDEC IDs>]
    local_precondition: <screen/HUD state>
    action_or_input: <declared user/system input>
    expected_local_result: <observable UX response>
    platform_profile_ids: []
    accessibility_obligations: []
    evidence_method: <observable local check>
    validation_owner: <owner>

Reference the product rule by ID/locator/hash; do not copy/rephrase it as a
second authority. Include enough local precondition/input/result to execute the
UX check after loading the cited requirement. Missing/stale requirement evidence
creates a blocking finding; never invent or duplicate the product rule.

ACs may verify UI state, focus, feedback, navigation, presentation of owned
data, and platform/accessibility variants. They do not prescribe QA automation,
implementation structure, or redefine gameplay outcomes.

## Phase 8: Cross-reference and dependency finding gate

Run deterministic checks over exact context:

1. every applicable requirement is covered or has OPEN owned finding;
2. navigation edges agree by screen ID and neighbor hash;
3. global pattern references resolve at declared library hash and local
   proposals remain non-global;
4. accessibility obligations trace to current foundation/tier;
5. data UI defines applicable null/empty/stale/loading/error behavior;
6. platform/input/resolution/aspect/text-scale declarations are covered;
7. every profile section occurs once and passes all content assertions;
8. author/decision/revision provenance matches identities/hashes; and
9. every AC references current requirement and decision evidence.

Use contract cgs.ux-dependency-finding/v1:

    id: UXD-<artifact-id>-<check-id>-<fingerprint>
    severity: BLOCKING | ADVISORY
    category: requirement | navigation | pattern | accessibility | data |
      platform | schema | provenance | acceptance
    evidence:
      path: <exact path>
      artifact_or_requirement_id: <ID>
      locator: <section/row/field>
      sha256: <raw hash>
      observed: <fact>
    expected: <rule>
    owner: <resolution owner>
    destination: <artifact/workflow>
    acceptance: <objective close condition>
    first_seen_target_sha256: <hash>
    last_evaluated_target_sha256: <hash>
    status: OPEN | RESOLVED | WAIVED
    resolution: <current-hash evidence or null>

Fingerprint is deterministic over category, owner, source ID/locator, expected,
and observed normalized facts. Preserve IDs across re-evaluation. RESOLVED
requires current evidence meeting acceptance. BLOCKING WAIVED remains unresolved
and prevents readiness. A user cannot close an external-owner gap by acceptance.

Any unresolved BLOCKING/critical finding prevents READY_FOR_REVIEW. Advisory
findings may remain.

## Phase 9: Bounded consultations and failure results

Consultants are read-only advisers. Limits:

- at most one consultant per section;
- at most three consultations per run;
- at most two concurrently;
- one question and one 60-second attempt;
- no automatic retry or nested delegation;
- canceled/late result token is revoked and result quarantined.

Record:

    id: UXCON-<run-id>-<NNN>
    section_id: <stable ID>
    role: <consultant role>
    question: <one bounded question>
    input_paths_sha256: []
    required: true | false
    started_at_utc: <timestamp>
    deadline_seconds: 60
    status: complete | partial | timeout | failed | side-effect | skipped
    output_sha256: <canonical result hash or null>
    evidence_summary: <bounded evidence or null>
    fallback: none | explicit-product-decision | section-blocked

Optional non-complete input may continue only when the product decision does not
depend on missing evidence and the owner explicitly decides; record fallback.
Required non-complete, malformed, side-effect, or late input marks dependent
section BLOCKED, artifact PARTIAL, appends checkpoint, and stops. Never invent
or merge quarantined output.

Consultants cannot choose layout/flow/density/input/interaction, define platform
or accessibility foundation, merge patterns, edit files, approve content, or
delegate.

## Phase 10: Checkpoint recovery and mode safety

On --resume validate exact request/checkpoint paths, v2 chain/payload hashes,
artifact/run/profile/content/author schema, authorization, target, context,
owners, section states/assertions, decisions/revisions, consultations, findings,
budgets, next transition, and absence of late writes.

- all hashes current: resume APPROVED_NOT_WRITTEN exact bytes first, otherwise
  next PENDING legal section;
- target mismatch: BLOCKED — TARGET/AUTHORIZATION DRIFT, zero write;
- context source mismatch: mark only dependent sections STALE and require new
  decision/preflight; do not replay;
- profile/content/author schema mismatch: switch to newly authorized
  migrate-schema;
- unsupported old checkpoint: ERROR — UNSUPPORTED CHECKPOINT SCHEMA;
- missing checkpoint: resume unavailable.

Non-placeholder text is not completion evidence. No conversation memory
reconstructs approval, provenance, receipt, or hashes.

## Phase 11: Final receipt, result, and independent-review handoff

Re-read target, re-run content/cross-reference gates, and re-hash every external
context-evidence entry (not the mutable-target-baseline entry). Append the final
cgs.ux-authoring-receipt/v1 checkpoint only after a final CAS writes the
content-derived artifact Status and stable receipt ID, then reads the final
target hash. The receipt is valid only when target,
section revisions, decision records, context digest, authorization, writer/
recorder identities, and finding set all recompute.

Set artifact Status from content/dependency state, then set Workflow Verdict:

- all required sections current/substantive, platform/accessibility/requirements
  current, zero unresolved BLOCKING findings, consultations complete/skipped
  legally, stable target:
  artifact Status READY_FOR_REVIEW;
- READY_FOR_REVIEW target plus verified receipt:
  Workflow Verdict READY_FOR_REVIEW and independent-review handoff;
- READY_FOR_REVIEW target but receipt append/verification failed:
  Workflow Verdict PARTIAL, no review handoff, report exact unreceipted target
  hash without reverting content;
- safe work preserved but content/evidence/dependency/consultation/migration is
  incomplete:
  artifact Status and Workflow Verdict PARTIAL;
- no safe transition due identity/authorization/owner/mandatory decision/target
  drift:
  preserve last safe status and Verdict BLOCKED;
- invalid/unsupported input or corrupt evidence before safe authoring:
  ERROR with no false artifact verdict.

Never emit COMPLETE, APPROVED, or IMPLEMENTATION READY.

Return artifact/run/screen IDs, profile/content/author schema hashes, actual
author/recorder identities, target pre/post/hash, context digest, section state/
assertions, decision/revision IDs, authorization hash, consultations, findings,
receipt ID/path/hash, non-writes, and exactly one next action.

READY_FOR_REVIEW next action is a fresh independent read-only UX review of exact
target and cgs.ux-authoring-receipt/v1 path/hash. Reviewer identity differs from
author/recorder and returns hash-bound current-schema evidence. This workflow
does not invoke review, persist review evidence, start visual production, or
implement UI.

PARTIAL/BLOCKED next action resolves one named dependency, decision,
authorization, drift, owner, migration, consultation, or receipt item.
