# Skill Test Spec: qa-plan

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

> **Spec ID**: qa-plan-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: high
> **Spec written**: 2026-07-22

## Skill Summary

qa-plan consumes one cgs-qa-plan-scope/v1 manifest and creates one immutable
cgs-qa-plan/v2 at production/qa/plans using its stable plan ID. Scope is resolved
only from stable sprint, feature or story authority IDs and exact paths/revisions.
No newest-file, title substring, path substring, mtime or legacy positional
selection is allowed.

The plan binds exact scope, story, GDD, ADR, control, raw requirement-span,
candidate/build, Test ID ownership, dependency and available evidence revisions. It
maps every AC to one coverage item and one or more method-specific Test IDs,
observable/risk tags, dependencies, evidence levels and gaps. Partial, stale or
unknown state is explicit and never complete gate input. The plan itself always
declares Gate Evidence: NO.

The only owned write is the immutable QA plan. Stories, requirements, build and
test evidence, ID-ownership snapshots, session state, workflow catalog and all
other files remain non-writes.

---

## Static Assertions

- [ ] **[QP-SA-001]** Frontmatter has exactly non-empty name and description and
  name is qa-plan.
- [ ] **[QP-SA-002]** cgs-qa-plan-workflow-contract/v1 declares v1 scope input,
  v2 immutable output, ownership snapshot, states, revisions and non-writes.
- [ ] **[QP-SA-003]** Only the exact scope-manifest invocation is accepted; all
  positional, bracketed and legacy epic-slug forms fail before writes.
- [ ] **[QP-SA-004]** Scope uses stable manifest IDs and exact paths/revisions, never
  newest, mtime, title, substring or unbounded glob selection.
- [ ] **[QP-SA-005]** Every expected missing, unreadable, invalid, omitted and
  unprocessed story remains in the ledger and makes coverage partial.
- [ ] **[QP-SA-006]** Hard budgets cover stories, files, bytes, requirement
  spans, dependency edges, plan items, output bytes and wall time.
- [ ] **[QP-SA-007]** Story declared type is preserved and contradictions produce
  QP-TYPE-MISMATCH without story mutation.
- [ ] **[QP-SA-008]** Every AC may have multiple observable/risk tags and methods;
  no single primary classification exists.
- [ ] **[QP-SA-009]** Test methods derive from observable, risk, confidence,
  feasible automation, dependency and build evidence rather than story type.
- [ ] **[QP-SA-010]** Visual and configuration ACs may require automation,
  integration, benchmark, capture or manual evidence according to observables.
- [ ] **[QP-SA-011]** Playtest items use only completed
  canonical `cgs.playtest-report/v2` reports plus independent current
  `cgs.playtest-report-recorder-receipt/v1` under production/playtests.
- [ ] **[QP-SA-012]** Approval exposes every candidate byte through a full
  artifact/diff and revision-bound lossless chunks; summary-only approval is invalid.
- [ ] **[QP-SA-013]** Every story, GDD, ADR, control and scope authority carries
  exact raw-file revision.
- [ ] **[QP-SA-014]** Every requirement binding carries owner, file revision, exact
  raw byte span, span revision and parser/tool identity.
- [ ] **[QP-SA-015]** Build binding is BOUND, PRE_IMPLEMENTATION or
  REQUIRED_MISSING with exact identity and fail-closed effects.
- [ ] **[QP-SA-016]** Test ID ownership prevents duplicate owners, cross-AC
  mapping, reuse of tombstones and concurrent snapshot drift.
- [ ] **[QP-SA-017]** Dependency and coverage matrices preserve missing
  endpoints, unknown owners, cycles, evidence levels and gaps.
- [ ] **[QP-SA-018]** Evidence levels never promote through missing, partial,
  stale, unsupported or unreadable receipts.
- [ ] **[QP-SA-019]** Plan IDs are immutable; publication requires target absent
  or identical and uses exclusive compare-and-set plus read-back.
- [ ] **[QP-SA-020]** qa-plan never writes stories, session state, requirements,
  evidence, ownership registry, workflow catalog or checkpoints.

---

## Test Cases

### Case 1 [QP-C01]: Stable scope manifest replaces latest and substring selection

#### Fixture

- Several sprint files have different mtimes.
- Two features share similar title text and story paths.
- One cgs-qa-plan-scope/v1 names stable plan/scope IDs, exact active sprint or
  feature authority path/revision and ordered stable story path/revision rows.

#### Input

- Invoke with the exact scope-manifest path.

#### Expected reads

- Scope manifest, its one exact authority and only its declared story closures.

#### Expected writes

- At most the exact immutable plan path after full validation and authorization.

#### Expected non-writes

- Other sprint/feature/story files, status files, catalogs and session state.

#### Expected behavior

- Scope membership is resolved from stable IDs and exact declared paths/revisions.
- Mtime, newest file, title/path substring and unbounded glob results are ignored.
- Scope source and story membership disagreement is invalid.
- Canonical duplicate IDs/paths are rejected.

#### Assertions

- [ ] Reordering directory entries does not change scope.
- [ ] Similar feature names do not add stories.
- [ ] The exact scope authority revision is recorded.
- [ ] No undeclared story is read for planning.

#### Case Verdict

PASS when selection is invariant and exactly manifest-bound; any inferred scope
is FAIL.

---

### Case 2 [QP-C02]: Missing story remains explicit PARTIAL and UNKNOWN

#### Fixture

- Scope manifest declares three stable story rows.
- One story loads, one is missing and one is unreadable.
- Requirement authorities for the loaded story are valid.

#### Input

- Generate a planning candidate and authorize saving the partial artifact.

#### Expected reads

- Every declared path attempted within budget and the loaded story closure.

#### Expected writes

- One immutable partial plan only when explicitly authorized.

#### Expected non-writes

- Missing placeholders, synthetic story files, guessed revisions, Test ID registry
  and downstream gate state.

#### Expected behavior

- Missing and unreadable stories remain source and scope-ledger rows with exact
  statuses and reason IDs.
- Scope Coverage and Plan State are PARTIAL; Effective State is UNKNOWN.
- No identifier, AC, requirement span or Test ID is invented.
- Result never describes the plan as complete downstream planning or gate input.

#### Assertions

- [ ] All three declared story IDs reconcile in the ledger.
- [ ] Missing paths have no fabricated revision.
- [ ] Verdict is PARTIAL after a verified write.
- [ ] Gate Evidence remains NO.

#### Case Verdict

PASS for a transparent partial artifact and fail-closed result; COMPLETE is FAIL.

---

### Case 3 [QP-C03]: Planning budgets produce deterministic omitted coverage

#### Fixture

- Scope exceeds maximum stories, authority files, input bytes and dependency
  edges in different variants.
- Stories have stable IDs and complete closure-size metadata.
- Manifest budgets are equal to or below hard workflow maxima.

#### Input

- Generate repeatedly from identical bytes and budgets.

#### Expected reads

- Scope header and story closure metadata first, then only whole admitted closures
  sorted by stable story ID and canonical path.

#### Expected writes

- At most one explicitly authorized partial plan with a complete budget ledger.

#### Expected non-writes

- Omitted/unprocessed sources and any truncated partial story closure.

#### Expected behavior

- Budgets cover stories, authorities, files, input bytes, requirement spans,
  dependency edges, plan items, output bytes and wall time.
- Selected, loaded, missing, unreadable, invalid, omitted and unprocessed rows
  record consumed counts and reason IDs.
- Budget exhaustion omits every remaining whole closure in deterministic order.
- No scan occurs outside the manifest.

#### Assertions

- [ ] Same inputs produce the same ledger and candidate revision.
- [ ] Counts reconcile to every declared story and authority.
- [ ] No half-loaded closure becomes current.
- [ ] Scope Coverage is PARTIAL after any omission.

#### Case Verdict

PASS when bounded selection and omissions are reproducible and complete;
otherwise FAIL.

---

### Case 4 [QP-C04]: Declared story type mismatch is reported, not rewritten

#### Fixture

- A story declares Visual/Feel.
- One AC has an exact deterministic formula observable and boundary requirements.
- Another AC genuinely requires subjective feel evaluation.
- All requirement bindings have exact source spans and revisions.

#### Input

- Classify the story ACs.

#### Expected reads

- Story declared type and all AC/GDD/ADR requirement bindings.

#### Expected writes

- QA plan candidate only.

#### Expected non-writes

- Story Type field, story AC text, GDD and ADR.

#### Expected behavior

- Preserve Declared Type Visual/Feel.
- Derive state/formula and boundary/error tags for the deterministic AC and
  feel/judgment for the subjective AC.
- Emit QP-TYPE-MISMATCH for contradictory observables with source evidence and
  owner.
- Plan supported methods without silently replacing the declared type.

#### Assertions

- [ ] Story bytes remain unchanged.
- [ ] Finding records declared type, derived tags and source bindings.
- [ ] Deterministic AC receives automation candidates.
- [ ] Subjective AC retains reproducible playtest requirements.

#### Case Verdict

PASS for preserved declaration plus explicit evidence-backed mismatch; silent
acceptance or mutation is FAIL.

---

### Case 5 [QP-C05]: Mixed ACs retain all labels and methods without a primary

#### Fixture

- One AC combines persistence round-trip, UI interaction, visual state and error
  recovery.
- Risk and dependency sources are complete.
- Automation is feasible for interaction/state while final visual judgment needs
  named manual evidence.

#### Input

- Build coverage rows and Test IDs.

#### Expected reads

- AC requirement bindings, dependencies, build state and ownership snapshot.

#### Expected writes

- Candidate coverage and Test ID rows within the plan only.

#### Expected non-writes

- Story, ownership snapshot, test sources and evidence artifacts.

#### Expected behavior

- The AC carries cross-system/persistence, UI interaction, visual/rendering and
  recovery tags.
- It gets all justified automated and manual methods with distinct stable Test
  IDs and one Coverage Item ID.
- No field names or selects a single primary type or method.
- Coverage gaps remain visible if any observable lacks a feasible method.

#### Assertions

- [ ] Secondary coverage is not dropped.
- [ ] Method-specific Test IDs have one AC and owner status.
- [ ] Manual evidence does not erase automation.
- [ ] No risk-score tie breaker selects a primary.

#### Case Verdict

PASS for complete multi-label coverage; any forced primary or dropped method is
FAIL.

---

### Case 6 [QP-C06]: Observable and risk determine method, not story type

#### Fixture

- Variant A is Visual but exposes deterministic render pixels.
- Variant B is Config/Data but controls a cross-system runtime behavior.
- Variant C is UI with automatable accessibility semantics and irreducible
  aesthetic review.
- Variant D has performance and recovery thresholds.

#### Input

- Classify methods for every AC.

#### Expected reads

- Exact requirement observables, thresholds, dependencies, platform/build needs
  and feasible automation constraints.

#### Expected writes

- Plan matrix only.

#### Expected non-writes

- Tests, captures, benchmark results, playtest reports and requirements.

#### Expected behavior

- A gets deterministic capture/diff or benchmark automation.
- B gets schema validation plus observable integration or smoke execution.
- C gets interaction/accessibility automation plus manual evidence only for the
  remaining aesthetic observable.
- D gets benchmark, failure-injection and recovery methods tied to thresholds.
- Story type remains a hint, not a decision rule.

#### Assertions

- [ ] Visual is not automatically manual-only.
- [ ] Config/Data is not reduced to spot-check.
- [ ] Every method cites observable/risk bindings.
- [ ] Unsupported method evidence becomes a gap, not an invention.

#### Case Verdict

PASS when methods follow evidence and feasibility; type-only classification is
FAIL.

---

### Case 7 [QP-C07]: Playtest evidence uses one completed-result contract

#### Fixture

- Plan item requires feel/judgment evidence.
- Candidate paths include a protocol, raw log, ingest-only session, director
  review, legacy session-log and canonical completed report.
- Completed report variants differ in schema, status, build/source revision,
  completed-result revision or sign-off.

#### Input

- Define expected evidence path/schema and classify supplied evidence level.

#### Expected reads

- Canonical playtest result and every declared dependency when evidence exists.

#### Expected writes

- Expected evidence contract in the plan only.

#### Expected non-writes

- Playtest protocol, session, report, review and legacy evidence paths.

#### Expected behavior

- Expected route is production/playtests under one session ID and report.md.
- Only the exact canonical `cgs.playtest-report/v2` report and matching independent
  `cgs.playtest-report-recorder-receipt/v1`, with session status COMPLETED and every
  report/candidate-record/recorder/dependency identity verified, may produce the
  `RECORDED COMPLETED — GATE ELIGIBLE` verification needed to promote evidence.
- Protocols, templates, raw logs, reviews, ingest-only and legacy paths do not
  satisfy a completed session.
- Partial/unreadable evidence yields Evidence Level UNKNOWN.

#### Assertions

- [ ] production/session-logs is never generated.
- [ ] Path alone does not establish completion.
- [ ] Build/source mismatch prevents promotion.
- [ ] qa-plan never writes the playtest artifact.

#### Case Verdict

PASS for exact canonical routing and fail-closed evidence classification;
otherwise FAIL.

---

### Case 8 [QP-C08]: Approval covers every candidate byte, not a summary

#### Fixture

- A large plan exceeds one UI page.
- Candidate bytes, total length and full revision are known.
- One preview variant shows only summary plus selected sections.
- Another provides ordered lossless chunks with byte ranges and individual revisions
  whose concatenation equals the candidate revision.

#### Input

- Request authorization for the one-file plan changeset.

#### Expected reads

- Candidate bytes and preview/chunk manifest.

#### Expected writes

- None until every byte is inspectable and the exact revision is approved.
- After valid approval, only the plan may be written.

#### Expected non-writes

- Any artifact approved from truncated, collapsed, ellipsis or summary-only
  content.

#### Expected behavior

- Full direct artifact is valid.
- Pagination is valid only when every ordered byte range and chunk revision
  reconciles to total bytes and candidate revision.
- Summary, sampled matrix, collapsed middle and changed-section-only previews are
  insufficient.
- Approval binds exact output path, operation and candidate revision.

#### Assertions

- [ ] No omitted content hides a coverage or dependency row.
- [ ] Concatenated chunks reproduce exact candidate bytes.
- [ ] Candidate change after approval invalidates authorization.
- [ ] Preview includes explicit non-writes.

#### Case Verdict

PASS when only full revision-bound content authorizes the write; summary approval is
FAIL.

---

### Case 9 [QP-C09]: Legacy catalog and positional invocations fail before writes

#### Fixture

- Invocation variants include a bare epic slug, bracketed epic placeholder,
  sprint positional token, feature text, story path text, no argument, unknown
  flag and one exact scope-manifest flag.
- Catalog remains a protected non-write.

#### Input

- Parse each invocation variant.

#### Expected reads

- For invalid variants, no project discovery is required.
- For the valid variant, only the literal scope manifest begins validation.

#### Expected writes

- None during invocation validation.

#### Expected non-writes

- Workflow catalog, stories, plans and session state.

#### Expected behavior

- All legacy/positional/bracketed/missing/unknown variants fail with the supported
  invocation and catalog-owner migration handoff.
- No epic slug is reinterpreted as feature search.
- Only the exact scope-manifest form proceeds.

#### Assertions

- [ ] Invalid call fails before scope discovery and preview.
- [ ] Catalog is never patched by qa-plan.
- [ ] No newest or title-match fallback occurs.
- [ ] Error does not claim a plan was generated.

#### Case Verdict

PASS when the invocation schema is exact and fail-closed; otherwise FAIL.

---

### Case 10 [QP-C10]: Registered specification has executable structural boundaries

#### Fixture

- The registered qa-plan specification is parsed as cgs-skill-spec/v2.
- A negative copy removes one required case section or creates a case-number gap.
- Another negative copy duplicates a static or protocol ID.

#### Input

- Run spec preflight against each fixture.

#### Expected reads

- Exact registered spec bytes.

#### Expected writes

- None.

#### Expected non-writes

- Spec, skill, metadata and catalog.

#### Expected behavior

- Valid spec has stable header, contiguous numbered cases and unique IDs.
- Every case contains Fixture, Input, Expected reads, Expected writes, Expected
  non-writes, Expected behavior, Assertions and Case Verdict.
- Missing section, number gap or duplicate stable ID makes the spec invalid.
- Structural validity is not reported as behavioral execution.

#### Assertions

- [ ] Cases are independently runnable from explicit fixtures.
- [ ] Side effects and non-writes are testable.
- [ ] Verdict conditions are explicit.
- [ ] No catalog result is fabricated.

#### Case Verdict

PASS when valid and negative structures classify exactly; otherwise FAIL.

---

### Case 11 [QP-C11]: Story, build and requirement bytes bind evidence levels

#### Fixture

- Story/GDD/ADR/control files and exact AC/requirement spans are readable.
- Variant A binds a current candidate manifest and build artifact.
- Variant B is explicitly PRE_IMPLEMENTATION.
- Variant C requires a build but it is missing.
- Evidence variants include current and stale test source/discovery/execution
  receipts.

#### Input

- Generate source, build, requirement and evidence rows.

#### Expected reads

- Exact raw source files, parser/tool identity, build candidate/artifact or
  trusted receipt and all evidence dependencies.

#### Expected writes

- Plan rows only.

#### Expected non-writes

- Sources, builds, test implementation and evidence.

#### Expected behavior

- Each requirement row records binding ID, owner, file revision, exact byte span and
  span revision.
- BOUND records candidate/build/artifact/source commit/platform/configuration.
- PRE_IMPLEMENTATION keeps items PLANNED and Gate Evidence NO.
- REQUIRED_MISSING makes plan PARTIAL and Effective State UNKNOWN.
- Evidence promotes only through IMPLEMENTED, DISCOVERED, EXECUTED and VERIFIED
  when each current exact revision receipt exists; otherwise UNKNOWN.

#### Assertions

- [ ] Span revision never replaces full-file revision.
- [ ] Build name/date cannot replace artifact revision.
- [ ] Stale receipt cannot promote evidence.
- [ ] Plan itself is never execution evidence.

#### Case Verdict

PASS for exact binding and promotion rules; guessed revision or level is FAIL.

---

### Case 12 [QP-C12]: Test ID ownership and dependency coverage are complete

#### Fixture

- Ownership snapshot contains owned IDs, one retired tombstone and version/revision.
- AC variants request a new deterministic ID, conflict with another AC, reuse a
  tombstone and map to multiple owners.
- Dependency graph includes valid edges, missing endpoint and ambiguous cycle.

#### Input

- Build ownership and dependency/coverage matrices.

#### Expected reads

- Ownership snapshot, source plan revisions, AC bindings and dependency authorities.

#### Expected writes

- PROPOSED/OWNED/conflict rows in the plan only.

#### Expected non-writes

- Ownership snapshot, prior plans, stories and dependency authorities.

#### Expected behavior

- Existing ID must map to one AC, method family and owner plan.
- New deterministic ID is PROPOSED and becomes plan-owned only after immutable
  publication.
- Conflict, multiple owner, cross-AC mapping or tombstone reuse makes plan
  PARTIAL and prevents COMPLETE.
- Every dependency edge records source/path/revision/relation; missing endpoints,
  unknown owners and ambiguous cycles remain coverage gaps.

#### Assertions

- [ ] Snapshot revision drift before publish blocks version and existence conflict check.
- [ ] IDs are never recycled.
- [ ] All ACs and dependencies reconcile in the matrix.
- [ ] No name similarity invents a dependency edge.

#### Case Verdict

PASS for unique ownership and complete gap-preserving graph; otherwise PARTIAL or
BLOCKED, never COMPLETE.

---

### Case 13 [QP-C13]: Immutable plan publication uses exclusive version and existence conflict check

#### Fixture

- Candidate bytes, path and full revision are approved.
- Every authority and ownership snapshot still matches preview.
- Target variants are absent, byte-identical, different, or appear concurrently.

#### Input

- Publish the approved immutable plan.

#### Expected reads

- Every captured authority and evidence dependency, target existence/bytes and
  staged candidate bytes.

#### Expected writes

- Absent variant creates exactly one plan.
- Identical variant performs no write and reports unchanged.
- Different/concurrent conflict writes nothing.

#### Expected non-writes

- Existing different plan, stories, ownership snapshot, state and all external
  work.

#### Expected behavior

- Immediately revalidate all sources, requirement spans, build, dependency,
  ownership and evidence state.
- Require target absent or approved identical no-op.
- Use same-filesystem staged exclusive create/compare-and-set.
- Read back and validate candidate bytes and internal references.
- Existing different bytes yield BLOCKED IMMUTABLE PLAN ID CONFLICT and require a
  new revision ID.

#### Assertions

- [ ] No UPDATE path exists.
- [ ] Concurrent user file is preserved.
- [ ] Written status requires byte-identical read-back.
- [ ] Superseding a plan never mutates the old plan.

#### Case Verdict

PASS for exact create/no-op/conflict behavior; overwrite or false success is FAIL.

---

### Case 14 [QP-C14]: Complete bounded plan is current but not gate evidence

#### Fixture

- Valid exact scope manifest fits all budgets.
- Every story and authority loads with exact revisions and unambiguous requirement
  spans.
- Build binding is BOUND or valid PRE_IMPLEMENTATION.
- ACs have complete observable/risk, methods, dependencies and unique Test ID
  ownership.
- Available evidence levels are classified from current receipts.
- Full candidate bytes are approved and version and existence conflict check publication/read-back succeeds.

#### Input

- Run the full planning transaction.

#### Expected reads

- Every scope, source, build, ownership, dependency and available evidence
  authority declared by the scope manifest.

#### Expected writes

- One immutable production/qa/plans plan file.

#### Expected non-writes

- Stories, requirements, builds, tests, evidence, ownership snapshot, session
  state, catalog, checkpoints and downstream workflows.

#### Expected behavior

- Plan State, Effective State and Scope Coverage are CURRENT/CURRENT/COMPLETE.
- Dependency and coverage matrices reconcile every AC and Test ID.
- Persistence is WRITTEN or verified UNCHANGED.
- Verdict is COMPLETE.
- Gate Evidence remains NO; downstream gates require current separate evidence.
- No downstream workflow is invoked.

#### Assertions

- [ ] Artifact schema and all v2 mandatory sections exist.
- [ ] Plan declared revision equals reported and read-back revision.
- [ ] All non-writes remain byte-identical.
- [ ] Any partial/stale/unknown predicate prevents COMPLETE.

#### Case Verdict

PASS only for the complete current immutable planning result; otherwise fail
closed.

---

## Protocol Compliance

- [ ] **[QP-PC-001]** Exact scope-manifest invocation validates before discovery
  or writes.
- [ ] **[QP-PC-002]** Scope selection, IDs, canonical paths and hard budgets are
  deterministic and manifest-bound.
- [ ] **[QP-PC-003]** Every source and raw requirement span is revision-bound with an
  explicit owner and parser/tool.
- [ ] **[QP-PC-004]** Build and evidence states distinguish bound,
  pre-implementation, required-missing, current, partial, stale and unknown.
- [ ] **[QP-PC-005]** Story declared type is preserved while AC observables and
  risks independently drive multi-method planning.
- [ ] **[QP-PC-006]** Test ID ownership is unique, non-recycled and revalidated at
  publication.
- [ ] **[QP-PC-007]** Dependency and coverage gaps remain explicit and cannot be
  score-filled or inferred by name.
- [ ] **[QP-PC-008]** Full lossless candidate bytes and revision are inspectable
  before one-file authorization.
- [ ] **[QP-PC-009]** Partial, stale and unknown plans are not complete
  downstream inputs and Gate Evidence is always NO.
- [ ] **[QP-PC-010]** Publication is immutable, exclusive version and existence conflict check and read-back
  verified.
- [ ] **[QP-PC-011]** Result ledger reports only selected and verified operations.
- [ ] **[QP-PC-012]** No story/state/catalog/authority/evidence/downstream write or
  workflow invocation occurs.

## Coverage Notes

### Authoritative P1 finding trace

| Audit ID | SKILL clause | Case/assertion |
|---|---|---|
| `QP-004` | Phase 1 exact scope resolution | Case 1: exact scope authority revision; no undeclared story read |
| `QP-005` | Phase 1 partial ledger; Phase 4 Plan State Rules | Case 2: no fabricated revision; PARTIAL verdict; Gate Evidence NO |
| `QP-006` | Phase 1 budgets; Phase 2 bounded context | Case 3: reconciled counts; no half-loaded CURRENT; PARTIAL coverage |
| `QP-007` | Phase 2.2 declared-type preservation | Case 4: story unchanged; mismatch finding retains declared/derived/source data |
| `QP-008` | Phase 3 multi-label coverage | Case 5: secondary coverage retained; no primary tie-breaker |
| `QP-009` | Phase 3 observable/risk-driven methods | Case 6: method bindings; unsupported evidence remains a gap |
| `QP-010` | Phase 4 Playtest Requirements | Case 7: no session-logs write; path alone insufficient; no playtest write |
| `QP-011` | Phase 5.1 lossless preview/approval | Case 8: chunks reproduce candidate; post-approval change invalidates authorization |
| `QP-018` | Invocation and Phase 1 exact scope schema | Case 9: invalid call fails before discovery; no newest/title fallback |
| `QP-019` | Contract manifest and SKILL trace matrix | Case 10: runnable fixtures; testable writes/non-writes; explicit verdicts |

The matrix above replaces range-only coverage with one independently inspectable
row for every exact P1 ID in the 2026-07-20 qa-plan audit.

Cases 11 through 14 cover the requested exact story/build/requirement revisions,
Test ID ownership, evidence levels, dependency/coverage matrix, partial/unknown
semantics and immutable version and existence conflict check publication. This specification is a written
behavioral contract; it does not claim that a plan fixture or downstream evidence
was executed.
