# Architecture Decision — Required workflow continuation

This file is normative. It begins only after the main skill validated
`cgs.architecture-decision-request/v2`, one-decision scope, collision-safe target,
bounded current context, engine/dependency coverage, one mutation boundary, and
the `cgs.architecture-decision-checkpoint/v2` chain.

## Phase 4: Constraint, alternative, and user-decision provenance

Use the shared authoring decision classes for every material ADR claim:

| Class | Authority and treatment |
|---|---|
| `product-choice` | Actual user/named technical decision authority selects the proposed alternative, scope, tradeoffs, scoped exception, or supersession intent after comparable options. |
| `evidence-backed-hard-constraint` | Current owned requirement/engine/platform/security/legal/compatibility evidence directly constrains alternatives; preserve source identity/hash and do not ask the user to vote it away. |
| `derived-design-constraint` | Author derives an architectural implication from accepted choice/current hard evidence; show derivation/assumptions and require decision-owner acceptance. |
| `technical-handoff` | Separate architecture/implementation/measurement/design-owner question is routed out and cannot become ADR truth until current owner evidence returns. |

Record stable decisions:

    id: ADRDEC-<adr-uuid>-<NNN>
    section_ids: []
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    owner: <actual user/named authority/source owner>
    recorder_task_id: <actual author task>
    question: <one bounded question>
    options: [{id, value, tradeoffs, evidence_refs}]
    selected: <alternative/constraint/handoff>
    rationale: <owner rationale or derivation>
    source_refs: [{id, owner, path_or_url, locator, sha256, observed_at}]
    assumptions: []
    dependent_assertion_ids: []
    status: ACCEPTED | PROVISIONAL | ROUTED | SUPERSEDED
    accepted_at_utc: <RFC3339 seconds Z | null>

Never claim consultant/author/model choice as the user's. Product choice and
derived constraint require actual decision-owner acceptance. Hard constraints
require current source evidence. Routed handoff remains unresolved.

### Constraint ledger

Every constraint has stable ID and:

    id: ADRCON-<adr-uuid>-<NNN>
    kind: functional | performance | platform | engine | security |
      compatibility | schedule | resource | legal | product
    authority: hard-source | user-bound | derived | hypothesis | unknown
    statement: <one testable constraint or unknown>
    owner: <source/decision owner>
    source_refs: [{id, path_or_url, locator, sha256, version, observed_at}]
    applicability: <scope predicate>
    verification: <method/evidence needed>
    status: VERIFIED | PARTIAL | UNVERIFIED | STALE | UNKNOWN | CONFLICTING

Never write `None` because a constraint/dependency is unclear. Use UNKNOWN with
owner, effect, and evidence needed. Conflicting hard constraints block selection
until their owners resolve precedence; the author cannot choose.

### Comparable alternatives

Present at least two viable alternatives and include status quo/no-action when it
is a meaningful option. Use stable `ADRALT-<adr-uuid>-<NNN>` IDs. Evaluate every
alternative against the same ordered criteria:

- how it answers the exact decision question and stays in scope;
- satisfaction/violation/unknown for each constraint/requirement ID;
- architecture/components/data/control flow and key interface effect;
- compatibility/migration/rollback/reversibility;
- performance/resource/security/operational consequences;
- implementation complexity only as qualitative or sourced estimate;
- evidence coverage, assumptions, uncertainties, and validation needed; and
- positive/negative/neutral consequences and risks.

Do not create a straw alternative or use unsourced numbers to make one win.
Missing evidence appears identically in comparison and remains UNKNOWN.

Ask the actual decision authority to select an alternative, request one named
change, keep checkpoint/stop, or stop. Allow at most two alternative/decision
revision rounds in the run. A third request checkpoints and returns STOPPED; it
never silently selects/recommends a winner.

Selection creates one `product-choice` ADRDEC and records rejected alternatives
with factual rejection reason. It establishes the proposed technical decision,
not lifecycle acceptance, file authorization, review, implementation authority,
or registry/story readiness.

## Phase 5: cgs.adr-content-profile/v2 assertions

Every assertion has stable ID, applicability, PASS/FAIL, evidence/decision IDs,
owner, and failure reason. Heading/non-placeholder length is never sufficient.

### Metadata, status, and scope

- `ADRC-META-01`: canonical UUID/allocation receipt/path/display sequence/slug are
  mutually consistent and target uniqueness CAS is current;
- `ADRC-META-02`: schema/content/author versions, authoring completeness, receipt
  ID, date, and actual decision makers are present;
- `ADRC-STATUS-01`: new/revise/supersede proposal says Proposed exactly once;
- `ADRC-STATUS-02`: retrofit Unknown/Proposed is honest and contains no inferred
  Accepted/Deprecated/Superseded lifecycle claim;
- `ADRC-SCOPE-01`: one interrogative decision question, one domain, stable in/out
  component IDs, and out-of-scope handoffs are explicit;
- `ADRC-SCOPE-02`: any bundle has current inseparability evidence; otherwise the
  ADR contains exactly one decision.

### Engine, source, dependency, and constraint evidence

- `ADRC-ENG-01`: pinned engine/version/domain/risk/cutoff and every consulted
  reference ID/owner/path/locator/hash/date/coverage state are explicit;
- `ADRC-ENG-02`: API claims are VERIFIED or honestly PARTIAL/UNVERIFIED/STALE/
  UNKNOWN with validation/handoff; no missing evidence is None;
- `ADRC-DEP-01`: Depends On/Enables/Blocks/order fields contain stable IDs or
  evidence-backed explicit None where the bounded graph proves no edge;
- `ADRC-DEP-02`: graph records unique resolution, current lifecycle status/hash,
  self/duplicate/cycle/replacement-cycle checks and acceptance eligibility;
- `ADRC-CON-01`: all constraints use ADRCON IDs, owners, applicability, source
  hashes, verification, and coverage state;
- `ADRC-CON-02`: every current product/technical requirement has stable ID/owner/
  path/locator/hash and separates preserved product rule from ADR realization.

### Alternatives and proposed decision

- `ADRC-ALT-01`: at least two viable stable alternatives (plus meaningful status
  quo when applicable) use the same ordered criteria;
- `ADRC-ALT-02`: pros/cons/risks/reversibility/migration/performance/evidence gaps
  are specific and no alternative is a straw option;
- `ADRC-DEC-01`: selected ADRALT ID, exact user/named-authority ADRDEC record,
  rationale, rejected alternatives, and accepted tradeoffs are explicit;
- `ADRC-DEC-02`: architecture/data/control flow/key interfaces implement only the
  selected in-scope decision and do not redefine product truth.

### Consequences, performance, migration, and validation

- `ADRC-CONS-01`: positive/negative/neutral consequences and risk owner/likelihood/
  impact/mitigation/trigger cover selected alternative;
- `ADRC-PERF-01`: every numeric baseline/budget/prediction has source ID/path/
  locator/hash/units/method/date; otherwise it is labeled HYPOTHESIS/UNKNOWN;
- `ADRC-PERF-02`: hypotheses include reproducible measurement/validation plan,
  owner, environment, metric, sample/threshold, and decision impact;
- `ADRC-MIG-01`: migration steps, compatibility boundary, owner, rollback,
  irreversible point, and failure recovery are explicit or evidence-backed N/A;
- `ADRC-VAL-01`: validation criteria are measurable, identify evidence/owner, and
  distinguish implementation verification from lifecycle acceptance.

### Traceability, replacement, and provenance

- `ADRC-TRACE-01`: every requirement maps source product rule to ADR-owned
  technical realization without copying/mutating GDD authority;
- `ADRC-REPL-01`: related/depends/supersedes/scoped-exception links use exact IDs/
  paths/hashes/current statuses and no replacement cycle;
- `ADRC-REPL-02`: supersede proposal covers replacement scope/retained obligations/
  migration/completeness and leaves predecessors unchanged/authoritative;
- `ADRC-PROV-01`: every material statement traces to ADRDEC/ADRCON/ADRALT/source
  IDs; actual author/consultant identities are truthful;
- `ADRC-PROV-02`: exact-body approvals, revisions, consultations, findings, graph,
  context and authorization hashes are current and noncontradictory.

Section `NOT_APPLICABLE` is permitted only where an assertion explicitly allows
N/A and an accepted ADRDEC plus evidence explains why. Required sections cannot
be skipped.

## Phase 6: Bounded advisory consultations and failure results

Consultants are read-only advisers. They cannot select alternatives, resolve hard
source conflicts, edit files, approve content, accept/supersede/deprecate an ADR,
write review/lifecycle evidence, invoke other agents, or become independent
reviewer/recorder.

Mode contract:

- `solo`: zero consultants/subagents;
- `lean`: at most one configured primary engine specialist when engine evidence
  is applicable;
- `full`: at most the primary engine specialist and one technical-director; they
  may run concurrently because neither owns decisions/lifecycle;
- all modes remain Proposed.

Hard caps: one consultation per role, two per run, two concurrently, one bounded
question and one 60-second attempt, no retry, and no nested delegation. Revoke
tokens and quarantine canceled/late output.

Record `cgs.adr-consultation-result/v1`:

    id: ADRCONSLT-<run-id>-<NNN>
    role: <engine specialist | technical-director>
    question: <one bounded evidence question>
    required: true | false
    input_target_or_draft_sha256: <hash>
    input_source_hashes: []
    started_at_utc: <timestamp>
    deadline_seconds: 60
    status: complete | partial | timeout | failed | side-effect | skipped
    disposition: ADVISORY_SUPPORT | ADVISORY_CONCERNS | ADVISORY_REJECT | null
    findings: []
    omissions: []
    output_sha256: <canonical hash or null>
    consultant_task_id: <actual identity or null>

Consultation disposition never changes Status. Show each proposed draft change
with source evidence; the user/decision authority accepts, rejects, or revises it
through ADRDEC/exact-body approval. Consultant output never directly mutates the
draft.

Required partial/timeout/failed/side-effect/malformed/late result marks dependent
evidence UNVERIFIED, Authoring Completeness PARTIAL, appends checkpoint, emits no
review handoff, and stops that section. Optional failure may remain an explicit
UNKNOWN only when no required assertion depends on it. Never fabricate analysis
or retry in the same run.

## Phase 7: Findings and external-owner handoffs

Use `cgs.adr-dependency-finding/v1`:

    id: ADRF-<adr-uuid>-<check-id>-<fingerprint>
    severity: BLOCKING | ADVISORY
    category: duplicate | scope | requirement | engine | dependency | cycle |
      conflict | product-owner | performance | replacement | provenance
    evidence: {path_or_url, source_id, locator, sha256, observed}
    expected: <objective rule>
    owner: <resolution owner>
    destination: ADR/TECH | GDD PRODUCT RULE | ENGINE SETUP | ESTIMATE |
      LIFECYCLE | REGISTRY | STORY READINESS
    acceptance: <objective close condition>
    status: OPEN | RESOLVED | WAIVED
    resolution: <current-hash evidence or null>

Fingerprint deterministically covers category, owner, source ID/locator,
expected, and observed normalized facts. `BLOCKING WAIVED` remains unresolved and
prevents READY_FOR_REVIEW/acceptance eligibility.

Classify GDD differences:

- `ADR/TECH`: API/signal/method/data type/internal ownership naming stays in ADR;
  map it to GDD term and do not edit GDD.
- `GDD PRODUCT RULE`: player-visible/balance/content/UX rule change blocks affected
  decision and routes to design owner; do not edit/redefine the GDD.

Registry conflicts require align, complete supersede proposal, or objectively
disjoint scoped exception. Registry is read-only projection; emit candidate only.

From Blocks/Enables, emit a non-mutating
`dependency_may_be_unblocked` event with ADR path/hash, affected IDs, and
`eligibility: pending_accepted_lifecycle_record`. It never edits or labels a story
Ready; independent story-readiness validates all dependencies later.

## Phase 8: Section drafting, semantic preflight, approval, and CAS

Draft one stable section at a time from accepted ADRDEC records and current
ADRCON/ADRALT/source/graph evidence. For each unresolved product/technical choice,
present two or three meaningful options and let the user/authority decide.

Before exact-body approval:

1. run applicable content assertions and single-decision scope check;
2. verify every material claim's decision/constraint/alternative/source IDs;
3. revalidate duplicate fingerprint, dependency/replacement graph, owner
  boundaries, engine coverage, numeric evidence, and findings;
4. confirm no consultant prose silently became authoritative;
5. confirm no external artifact change is included;
6. re-hash target/section/context/authorization/draft bytes; and
7. show complete proposed section body plus provenance/failure table.

Store actual content approval:

    id: ADRAPR-<adr-uuid>-<section-id>-<NNN>
    owner: <actual user/named technical authority>
    section_id: <stable ID>
    approved_body_sha256: <hash>
    decision_constraint_alternative_ids: []
    assertion_result_sha256: <hash>
    graph_and_finding_sha256: <hash>
    context_manifest_sha256: <hash>
    target_and_section_baseline_sha256: <hashes>
    authorization_sha256: <hash>
    approved_at_utc: <RFC3339 seconds Z>

Approval denied or two revision rounds exhausted leaves section INCOMPLETE,
appends PARTIAL/STOPPED checkpoint, and never infers yes.

Immediately before each write, one attempt must pass:

1. **Target CAS** — current raw target equals expected baseline/last verified hash;
2. **Section CAS** — selected stable-ID body/unique anchors equal approved
   preimage and all out-of-scope ranges match;
3. **Context CAS** — every external source used plus ordered manifest digest match;
   mutable target is excluded here;
4. **Authorization CAS** — exact path/operation/section/limits, approval hash, and
   authorization identity/hash match; and
5. **Writer CAS** — actual target writer equals authorized identity.

Mismatch returns precise `ERROR — CONCURRENT TARGET CHANGE`,
`ERROR — CONTEXT EVIDENCE CHANGED`, or
`ERROR — AUTHORIZATION/WRITER CHANGED`, with no target/checkpoint transaction.

Atomically replace only one stable-ID body plus authorized metadata fields, read
back, and prove every out-of-scope byte unchanged. Append:

    id: ADRREV-<adr-uuid>-<section-id>-<NNN>
    operation: new | retrofit | revise-proposed | supersede-proposal
    section_id: <stable ID>
    before_target_sha256: <hash>
    after_target_sha256: <hash>
    before_section_sha256: <hash or ABSENT>
    after_section_sha256: <hash>
    decision_constraint_alternative_ids: []
    approval_id: <ADRAPR ID>
    source_and_graph_hashes: []
    authorization_sha256: <hash>
    writer_task_id: <actual identity>
    timestamp_utc: <RFC3339 seconds Z>

Then append checkpoint by predecessor/create-if-absent CAS. If checkpoint fails
after verified target bytes, preserve content, return Workflow Verdict PARTIAL,
report exact unreceipted target hash, emit no review handoff, and never replay.

## Phase 9: Whole-ADR validation and authoring receipt

Re-evaluate exact single-decision scope, fingerprint/duplicates, every section/
assertion/source/constraint/alternative/decision/approval/revision, engine
coverage, dependency/replacement graph, consultations/findings, lifecycle status,
target/context hashes, and preserved bytes.

Set target Authoring Completeness from content only:

- DRAFT: skeleton exists without a complete approved decision;
- PARTIAL: safe Proposed/Unknown content exists but required section/evidence/
  graph/decision/consultation/finding remains incomplete/invalid/stale/blocking;
- CONTENT_COMPLETE: all content assertions pass, exact one decision is selected,
  required evidence/graph are current, no blocking finding remains, and target
  bytes read back stably. Lifecycle Status remains Proposed (or honest Unknown
  retrofit).

Before final metadata write rerun five-part CAS. Then create final external
`cgs.adr-authoring-receipt/v1` only after stable final target bytes. It binds
allocation/request/operation, pre/post target/section hashes, profile/content/
author schema, context digest, scope/fingerprint, sources/constraints/alternatives/
decisions/approvals/revisions, graph/replacements, consultations/findings,
authorization, author/writer/recorder identities, checkpoint head, and target.

Receipt ID may appear in target; receipt path/hash may not. Receipt is authoring
evidence, not independent review, lifecycle acceptance, implementation, registry,
or readiness evidence.

Set Workflow Verdict separately:

- DRAFT/PARTIAL target: PARTIAL/STOPPED, no review handoff;
- CONTENT_COMPLETE target plus verified receipt: READY_FOR_REVIEW and independent
  architecture-review handoff;
- CONTENT_COMPLETE target but receipt append/verification fails: PARTIAL, no
  handoff, exact unreceipted target hash, no replay/revert;
- unsafe target/context/authorization/identity: BLOCKED with last safe bytes;
- invalid request/corrupt evidence before safe work: ERROR, no false target state.

Never report Accepted, registry projected, implementation ready, or story Ready.

## Phase 10: Independent review and lifecycle-recorder separation

For READY_FOR_REVIEW, emit `cgs.architecture-review-request/v2` for a fresh
independent architecture-review task. Do not invoke it. Bind:

- exact ADR ID/path/current SHA-256 and profile/content/author schema;
- single-decision scope/fingerprint, all section/assertion hashes;
- allocation, sources/constraints/requirements/engine coverage;
- alternatives/user decision/approvals/revisions, consequences/performance/
  migration/validation;
- dependency/replacement graph, consultations/findings;
- context digest, authoring receipt ID/path/hash, and all author/consultant/writer/
  recorder identities; and
- instruction to remain ADR/receipt/context read-only and emit immutable
  `cgs.architecture-review/v2` only.

Review recommendation (`ACCEPT`, `REVISE`, or `REJECT`) is not lifecycle status.
Reviewer must be fresh/independent, recompute target/receipt/context hashes, and
cannot edit ADR/registry/story/lifecycle state.

Only a separate lifecycle recorder may consume current independent `ACCEPT`,
verified authoring receipt, Proposed target preimage, dependency/replacement
eligibility, and identity separation. It performs exact CAS transition and emits
`cgs.adr-lifecycle-record/v1` binding review record/hash, status-only pre/post
target hashes, recorder identity, timestamp, and any atomic predecessor/successor
links. It alone may derive registry projection under registry-owner policy.

Missing/stale/self/wrong-schema review, non-ACCEPT recommendation, changed ADR/
receipt/context, Proposed/Unknown dependency, cycle, incomplete replacement, or
recorder identity conflict prevents acceptance. User acceptance cannot bypass it.

Any non-status target change after review requires a new authoring receipt and
fresh review. Preserve immutable old review/lifecycle records.

## Phase 11: Resume, recovery, output, and stop

Resume validates exact request/checkpoint paths and full v2 predecessor/payload
chain, allocation/target/context/schema, authorization/roles, scope/fingerprint,
section axes/assertions, sources/constraints/graph, alternatives/decisions/
approvals/revisions, consultations/findings, replacement/lifecycle evidence,
limits, next transition, and absence of late writes.

- all current: resume APPROVED_NOT_WRITTEN exact body first, otherwise next PENDING
  section;
- target/path/allocation mismatch: BLOCKED — TARGET/ALLOCATION DRIFT, zero write;
- external source/graph change: mark dependent sections STALE, invalidate active
  receipt/review handoff, and require new preflight;
- accepted/deprecated/superseded target: lifecycle-owner handoff, zero author edit;
- checkpoint collision/fork: ERROR — CHECKPOINT CHAIN INVALID;
- author/profile mismatch: explicit migration/new request; never replay.

Conversation memory never reconstructs source hashes, decisions, approval,
checkpoint, receipt, review, lifecycle state, or acceptance.

Final response lists run/ADR/allocation IDs, exact path/operation, scope/fingerprint,
target pre/post/hash, section axes/assertions, sources/coverage, constraints/
alternatives/decision/approval/revisions, graph/replacement links, consultations/
findings/handoffs, authorization/roles, checkpoint/receipt paths/hashes,
Authoring Completeness, Workflow Verdict, lifecycle status, explicit non-writes,
and exactly one next action or Stop.

Choose at most one evidence-based action: resolve one named blocker, resume one
section, obtain missing engine/dependency evidence, request fresh architecture
review, hand an accepted review to lifecycle recorder, or Stop. Never invoke it
or enumerate a pipeline.
