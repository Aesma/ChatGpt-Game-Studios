# Skill Test Spec: regression-suite

> **Spec ID**: regression-suite-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: high
> **Spec written**: 2026-07-22

## Skill Summary

regression-suite consumes one cgs-regression-scope/v1 and operates in explicit
report, update or audit mode. It owns only tests/regression-suite.md, a
cgs-regression-selection-manifest/v2. The manifest is a stable Test-ID selection
artifact, not test execution, business-test implementation or release proof.

Scope, QA plan, Test ID ownership, story/AC/Requirement Binding/Coverage Unit,
verified-fixed bug, target build, change impact, test source, sensitivity,
quarantine and optional execution evidence are exact path/revision-bound. Selection
uses deterministic coverage-unit set operations and a fixed lexicographic
priority key under declared hard budgets.

Update and audit use ID-keyed patches; retirement uses explicitly approved
non-reusable tombstones. Report is read-only. This workflow never executes tests
or writes build-bound receipts. Operation, scope, impact, selection, execution,
persistence and coverage states remain independent.

---

## Static Assertions

- [ ] **[RS-SA-001]** Frontmatter has exactly non-empty name and description and
  name is regression-suite.
- [ ] **[RS-SA-002]** cgs-regression-suite-workflow-contract/v1 declares exact
  subcommands, v1 scope, v2 selection, change impact, output and no execution.
- [ ] **[RS-SA-003]** Missing/unknown mode, positional scope, bracket token or
  implicit write request fails before writes.
- [ ] **[RS-SA-004]** Scope is exact manifest-bound and never scans all
  GDDs/stories/tests or selects latest files.
- [ ] **[RS-SA-005]** Hard budgets cover requirements, bugs, coverage units,
  impact edges, tests, sources, receipts, bytes, duration, output and wall time.
- [ ] **[RS-SA-006]** Bugs require VERIFIED_FIXED state, fix commit, pre/post
  verification receipt and exact fixed-build compatibility.
- [ ] **[RS-SA-007]** Coverage uses exact required-minus-mapped Coverage Unit ID
  sets; unmapped branches and boundaries are MISSING.
- [ ] **[RS-SA-008]** Scope, plan, requirement span, ownership, build, impact,
  test, sensitivity, quarantine, selection and execution revisions drive stale.
- [ ] **[RS-SA-009]** Calendar time, mtime, names, comments and prose never
  establish freshness, mapping, sensitivity or coverage.
- [ ] **[RS-SA-010]** Quarantine distinguishes REQUESTED, APPROVED, APPLIED and
  later runner-VERIFIED state with exact config/build/Test ID revisions.
- [ ] **[RS-SA-011]** Operation and coverage states are independent; critical
  gaps cannot be hidden by successful manifest persistence.
- [ ] **[RS-SA-012]** Report is read-only, has Persistence NOT_APPLICABLE and
  never says updated, audited, written or complete.
- [ ] **[RS-SA-013]** The registered spec uses cgs-skill-spec/v2 with contiguous
  complete cases and unique stable IDs.
- [ ] **[RS-SA-014]** Missing business tests are handed to the story/test-
  authoring owner, never test-helpers.
- [ ] **[RS-SA-015]** Change impact binds baseline/current revisions, exact changed
  IDs/symbols and sourced graph edges.
- [ ] **[RS-SA-016]** Prioritization is a fixed lexicographic key with mandatory
  critical selection and explicit budget omissions.
- [ ] **[RS-SA-017]** Selection header and entries bind manifest/revision/scope/
  plan/build/ownership/impact/requirement/test/sensitivity revisions.
- [ ] **[RS-SA-018]** Tombstones retain history, approval and ownership forever;
  Selection IDs are never removed, recycled or rebound.
- [ ] **[RS-SA-019]** Keyed publication revalidates every authority and entry,
  parses the candidate, and uses one-file CAS plus read-back.
- [ ] **[RS-SA-020]** Selection and execution are separate artifacts; any changed
  manifest has Execution NOT_RUN and Coverage AWAITING RUN.

---

## Test Cases

### Case 1 [RS-C01]: Exact bounded scope replaces repository-wide traversal

#### Fixture

- Repository contains multiple QA plans, stories, GDDs and tests.
- One cgs-regression-scope/v1 binds stable operation/scope/manifest/revision IDs,
  exact current qa-plan v2 path/revision, ownership snapshot, build, requirement
  units, bugs, change-impact and preimage manifest.
- Negative variants exceed a hard budget or contain omitted/unreadable closures.

#### Input

- Invoke report with the exact scope-manifest path.

#### Expected reads

- Scope manifest and only declared whole authority closures admitted in canonical
  stable-ID order.

#### Expected writes

- None in report mode.

#### Expected non-writes

- Selection manifest, QA plan, sources, tests, receipts and repository state.

#### Expected behavior

- Canonicalize and reject duplicate IDs/paths and scope disagreements.
- Never scan all project requirements/tests or choose by latest/mtime.
- Enforce requirements/bugs/tests/files/receipts/bytes/units/edges/duration/
  output/wall-time ceilings.
- Record selected, loaded, missing, unreadable, invalid, omitted and unprocessed
  rows with stable reasons.
- Any required omission makes Scope PARTIAL and cannot yield verified coverage.

#### Assertions

- [ ] Directory order cannot change the admitted set.
- [ ] No undeclared file becomes coverage evidence.
- [ ] Whole closures are admitted or omitted.
- [ ] Ledger counts reconcile to scope declaration.

#### Case Verdict

PASS for exact deterministic bounded scope and fail-closed partiality; unbounded
traversal is FAIL.

---

### Case 2 [RS-C02]: Closed or Fixed labels do not prove a verified repair

#### Fixture

- Bug variants are Closed, Fixed, merged, assigned, fix-commit-only,
  VERIFIED_FIXED with stale receipt, VERIFIED_FIXED on another build, and fully
  verified fixed on the target-compatible build.
- Target candidate/build identity is exact and current.

#### Input

- Evaluate bug eligibility and priority.

#### Expected reads

- Bug artifact, original reproduction, fix commit/source identity, verification
  receipt and build dependencies.

#### Expected writes

- Report rows only in report mode.

#### Expected non-writes

- Bugs, commits, builds, receipts, tests and selection manifest.

#### Expected behavior

- Only VERIFIED_FIXED with receipt proving original failure on pre-fix build and
  pass on fixed target-compatible build is eligible.
- Closed/Fixed prose, merge and commit alone remain UNKNOWN gaps.
- Receipt or build mismatch is STALE/UNKNOWN.
- Eligible verified-fixed critical bug enters the mandatory priority class.

#### Assertions

- [ ] Exact bug ID/source revision and reproduction ID are required.
- [ ] Fix commit does not replace build verification.
- [ ] Build artifact/source/platform/configuration compatibility is checked.
- [ ] Ineligible bug remains visible.

#### Case Verdict

PASS when only fully verified target-compatible repair is eligible; label-based
acceptance is FAIL.

---

### Case 3 [RS-C03]: AC branch and boundary coverage is exact set arithmetic

#### Fixture

- QA plan AC has root, two branch, three boundary and one recovery Coverage Unit
  IDs.
- Selected tests map a proper subset; another candidate uses only the AC root.
- All revisions and sensitivity evidence for mapped units are current.

#### Input

- Compute unit, AC and aggregate coverage.

#### Expected reads

- QA-plan coverage/dependency matrix, Test ID ownership, exact test mappings,
  sensitivity and optional execution receipt.

#### Expected writes

- None in report mode.

#### Expected non-writes

- QA plan, mappings, tests, selection and receipts.

#### Expected behavior

- Required set includes every root/branch/boundary/recovery ID.
- Mapped set is the exact union of selected Test ID claims.
- Required minus mapped units are MISSING and GAP.
- A proper verified subset never upgrades the AC.
- AC is VERIFIED only when every required unit has eligible sensitivity and
  current build-bound PASS.

#### Assertions

- [ ] No model judgment labels a partial subset covered.
- [ ] Missing unit IDs are listed exactly.
- [ ] Root-only mapping cannot cover branches/boundaries.
- [ ] Aggregate counts reconcile to required units.

#### Case Verdict

PASS for deterministic set difference and all-units aggregation; subjective
PARTIAL/COVERED classification is FAIL.

---

### Case 4 [RS-C04]: explicit revision, not age, drive stale state

#### Fixture

- Current plan, requirement spans, ownership, build, impact, test, sensitivity,
  quarantine, selection and execution sources are captured.
- Variants change one byte in each source while preserving names and timestamps.
- Another variant changes only calendar age while bytes stay identical.

#### Input

- Revalidate mappings and evidence.

#### Expected reads

- Every captured raw source and declared dependency.

#### Expected writes

- None in report mode.

#### Expected non-writes

- All source/evidence/selection artifacts.

#### Expected behavior

- Any dependency byte or identity mismatch makes affected mapping STALE.
- Stable names, IDs and timestamps do not override mismatch.
- Identical old bytes remain current if all identity/freshness rules otherwise
  pass.
- Unavailable/unsupported verifier produces UNKNOWN, not current.

#### Assertions

- [ ] No day-count drift heuristic is used.
- [ ] Requirement raw span and file revision both revalidate.
- [ ] Prior green execution cannot cure stale selection.
- [ ] Exact changed dependency is reported.

#### Case Verdict

PASS when byte/identity change alone drives stale and age alone does not;
otherwise FAIL.

---

### Case 5 [RS-C05]: Quarantine needs applied and later verified runner state

#### Fixture

- Stable Test ID has proposal, approval, application and later runner receipts in
  different combinations.
- Application receipt binds changed config revision and expiry.
- Runner variants use wrong config, build, selection or Test ID; another explicitly
  records the exact Test ID skipped under current applied config.

#### Input

- Classify quarantine and coverage.

#### Expected reads

- Proposal, approval, application, config, selection, target build and runner
  receipts plus expiry authority.

#### Expected writes

- Report rows only.

#### Expected non-writes

- Registry, CI/config, test, receipts and selection manifest.

#### Expected behavior

- Proposal/registry text is QUARANTINE_REQUESTED.
- Current application without later matching runner proof is
  QUARANTINE_APPLIED_UNVERIFIED.
- Only unexpired current application plus later exact runner skip is QUARANTINED.
- Quarantined test never counts as PASS or verified coverage.
- Expired/mismatched/unreadable evidence is STALE/UNKNOWN and release-blocking.

#### Assertions

- [ ] APPLIED is not inferred from proposal.
- [ ] VERIFIED is not inferred from intended skip.
- [ ] Exact applied config revision and Test ID are required.
- [ ] Quarantine cannot hide a critical gap.

#### Case Verdict

PASS for exact state-machine classification and no coverage promotion; otherwise
FAIL.

---

### Case 6 [RS-C06]: Manifest operation success cannot hide critical gaps

#### Fixture

- Audit has a valid keyed update.
- One P0 Coverage Unit is missing and one noncritical item awaits execution.
- Candidate publication succeeds and read-back verifies.

#### Input

- Audit and approve exact keyed changes.

#### Expected reads

- All current scope, selection and candidate patch authorities.

#### Expected writes

- Only tests/regression-suite.md keyed fields.

#### Expected non-writes

- Tests, plans, requirements, receipts, CI and release state.

#### Expected behavior

- Persistence is WRITTEN and Operation is AUDITED.
- Critical missing unit makes Coverage CRITICAL GAPS.
- Awaiting unit remains listed and Execution becomes NOT_RUN after manifest revision
  changes.
- No COMPLETE or release-ready statement appears.

#### Assertions

- [ ] Operation and coverage dimensions are both emitted.
- [ ] Successful write does not change missing unit state.
- [ ] Critical unit IDs are visible.
- [ ] Release decision remains external.

#### Case Verdict

PASS for AUDITED plus CRITICAL GAPS and NOT_RUN; translating write success into
coverage success is FAIL.

---

### Case 7 [RS-C07]: Explicit modes disclose side effects before work

#### Fixture

- Invocation variants include no mode, duplicate mode, unknown mode, positional
  plan path, report, update and audit with exact scope manifest.
- An execution receipt is passed to update in one negative variant.

#### Input

- Parse each invocation and mode contract.

#### Expected reads

- Invalid forms read no project scope.
- Valid forms read only their literal scope manifest first.

#### Expected writes

- Report: none.
- Update/audit: no write until exact keyed changeset authorization.

#### Expected non-writes

- All files for invalid forms and report mode.

#### Expected behavior

- No/duplicate/unknown/positional forms fail before writes.
- Report is read-only; update is keyed upsert; audit adds approved tombstone
  capability.
- Update rejects execution receipt because changed selection requires a later run.
- No mode is inferred from metadata/default prompt or conversation context.

#### Assertions

- [ ] Side-effect class is known from the subcommand.
- [ ] No parameterless write-mode prompt occurs.
- [ ] Report never asks for write approval.
- [ ] Invalid mode emits no updated claim.

#### Case Verdict

PASS when subcommand determines exact read/write behavior; ambiguity is FAIL.

---

### Case 8 [RS-C08]: Registered specification matches the selection contract

#### Fixture

- Registered spec is parsed as cgs-skill-spec/v2.
- Negative variants remove a case Fixture, Expected non-writes or Case Verdict;
  create numbering gap; or duplicate stable IDs.

#### Input

- Run structural spec preflight.

#### Expected reads

- Exact spec bytes.

#### Expected writes

- None.

#### Expected non-writes

- Spec, skill, metadata, catalog and selection manifest.

#### Expected behavior

- Valid spec header, contiguous cases, required sections and unique static/
  protocol IDs pass.
- Missing section, numbering gap or duplicate ID fails.
- Artifact path, modes, operation/coverage axes and verdicts match the v2
  selection-manifest contract.
- Static structure is not reported as behavioral execution.

#### Assertions

- [ ] Every case has explicit fixture and side-effect boundary.
- [ ] No obsolete production/qa coverage-report output is expected.
- [ ] No FULL COVERAGE legacy verdict replaces current statuses.
- [ ] Catalog test results are not fabricated.

#### Case Verdict

PASS when valid and corrupted specs classify exactly; otherwise FAIL.

---

### Case 9 [RS-C09]: Missing business test goes to its authoring owner

#### Fixture

- One mandatory AC Coverage Unit has no candidate business test.
- Test-helpers is available but its contract only creates helper libraries.
- Story/QA plan names the implementation/test-authoring owner and required failure
  condition.

#### Input

- Produce remediation handoff.

#### Expected reads

- AC/requirement binding, owner, dependency and expected failure evidence.

#### Expected writes

- None in report mode; a gap entry only if separately authorized in audit/update.

#### Expected non-writes

- Test source, helper source, QA plan, story and downstream workflow state.

#### Expected behavior

- Handoff names stable AC/Coverage Unit/expected Test IDs, story/test-authoring
  owner, observable, failure condition and evidence needed.
- It never routes business-test creation to test-helpers.
- No test/helper workflow is auto-invoked.
- Gap remains critical or noncritical according to exact severity.

#### Assertions

- [ ] Helper validation is not business coverage.
- [ ] Handoff owner has authority to create the missing test.
- [ ] No source file is scaffolded by regression-suite.
- [ ] Coverage remains a gap until current evidence exists.

#### Case Verdict

PASS for correct owner/evidence handoff; recommending test-helpers as test author
is FAIL.

---

### Case 10 [RS-C10]: Report mode never impersonates an update

#### Fixture

- Current selection manifest and scope evidence exist.
- Record exact bytes/revision for the complete fixture tree.
- Report contains both gaps and current entries.

#### Input

- Invoke explicit report mode with exact scope and optional receipt.

#### Expected reads

- Current in-scope evidence only.

#### Expected writes

- None.

#### Expected non-writes

- Entire fixture tree remains byte-for-byte unchanged.

#### Expected behavior

- Operation REPORTED and Persistence NOT_APPLICABLE.
- Coverage reflects evidence independently.
- Changeset is empty; no write authorization requested.
- Output never says updated, audited, written, unchanged-write or COMPLETE.

#### Assertions

- [ ] Manifest before/after bytes are identical.
- [ ] No history/revision is added.
- [ ] Actual mode is visible.
- [ ] Coverage can be VERIFIED, gaps, stale, awaiting or indeterminate without
  changing operation.

#### Case Verdict

PASS for exact read-only result vocabulary; any updated claim or write is FAIL.

---

### Case 11 [RS-C11]: Change impact and priority are reproducible under budget

#### Fixture

- cgs-change-impact/v1 binds baseline/current commits, changed source revision,
  requirement/bug/unit IDs, production symbols and sourced dependency edges.
- Candidates span every obligation class, severity, distance and stable ID.
- Duration budget cannot admit all nonmandatory tests.
- Negative variants omit a changed edge or mandatory duration evidence.

#### Input

- Build selection repeatedly from identical scope and impact bytes.

#### Expected reads

- Exact impact manifest/dependencies, QA plan, bugs, Test IDs, duration sources
  and test/sensitivity evidence.

#### Expected writes

- Candidate manifest only until authorization.

#### Expected non-writes

- Impact, plan, tests, durations and execution evidence.

#### Expected behavior

- Validate impact schema/tool/baseline/current and edge source revision.
- Sort by fixed obligation class, P0-P3 severity, graph distance, Coverage Unit
  ID, Test ID and source path.
- Admit mandatory critical/fixed-bug tests first, then whole tests under every
  budget.
- Record full sort key, duration source/revision and omission reason.
- Missing mandatory test/impact/severity/duration yields PARTIAL/UNKNOWN and
  CRITICAL GAPS.

#### Assertions

- [ ] Repeated candidates have identical order/revision.
- [ ] No model score or prose priority is used.
- [ ] Mandatory item is never silently demoted.
- [ ] Omitted list reconciles all candidates.

#### Case Verdict

PASS for deterministic selection and fail-closed mandatory gaps; otherwise FAIL.

---

### Case 12 [RS-C12]: Tombstone and keyed CAS preserve ownership and history

#### Fixture

- Selection manifest has managed entries with owner, rationale, comments, custom
  fields and history.
- One entry needs machine-field update; one retirement is approved with prior
  entry revision; one retirement lacks approval.
- Concurrent variant changes manifest or ownership snapshot after preview.

#### Input

- Audit, preview and authorize exact per-ID candidate.

#### Expected reads

- Manifest/header/entries, every proposed source, ownership snapshot and
  tombstone approval.

#### Expected writes

- Clean variant changes only approved keyed fields/tombstone plus one revision and
  history events.
- Concurrent/conflict variant writes nothing.

#### Expected non-writes

- Human/unknown fields, unapproved retirement, concurrent bytes and all external
  authorities.

#### Expected behavior

- Tombstone retains prior identity/history and permanent non-reuse marker.
- Replacement uses new Selection ID with supersedes link.
- Complete candidate is parsed for unique IDs/references and exact revision.
- Revalidate all authorities and entry preimages, then one-file CAS.
- Read-back verifies exact candidate and preservation.

#### Assertions

- [ ] No physical deletion or ID recycling occurs.
- [ ] Unapproved tombstone remains byte-identical.
- [ ] Any preflight drift aborts all keyed changes.
- [ ] Persistence failure cannot report update.

#### Case Verdict

PASS for exact keyed/tombstone CAS and preservation; overwrite or history loss is
FAIL.

---

### Case 13 [RS-C13]: Selection change and execution are separate transactions

#### Fixture

- Existing execution receipt is current for old manifest/build.
- Update changes one selection entry and manifest revision.
- No runner invocation occurs in this workflow.
- A later external runner receipt binds the new exact manifest and target build.

#### Input

- Update, then separately report against the later receipt.

#### Expected reads

- Update reads no receipt for post-write coverage.
- Later report reads exact new selection and external execution receipt.

#### Expected writes

- Update writes only keyed selection manifest.
- Report writes nothing.

#### Expected non-writes

- Runner config, test results, receipt, build and release state.

#### Expected behavior

- Immediately after changed update: Operation UPDATED, Execution NOT_RUN and
  Coverage AWAITING RUN.
- Selection manifest alone cannot create PASS.
- Later report accepts receipt only when selection/build/plan/ownership/
  requirement/test/parser/log revisions and every active Test ID match.
- regression-suite never invokes or waits for the runner.

#### Assertions

- [ ] Old receipt becomes stale after manifest change.
- [ ] No circular execution result is embedded in selection entries.
- [ ] External runner owns the receipt.
- [ ] Release decision remains outside this workflow.

#### Case Verdict

PASS for strict transaction separation and later exact receipt consumption;
otherwise FAIL.

---

### Case 14 [RS-C14]: Complete current selection report can verify coverage only with execution

#### Fixture

- Scope, qa-plan v2, ownership, build, requirements, change impact, bugs, tests,
  sensitivity, quarantine and selection revisions are current and complete.
- All required units map to eligible active tests.
- Matching external runner receipt binds exact current manifest/build and every
  active Test ID passes.
- Report mode is used.

#### Input

- Report with exact scope and execution receipt.

#### Expected reads

- Every declared current authority and receipt dependency.

#### Expected writes

- None.

#### Expected non-writes

- Selection, tests, plans, receipts, CI/build/release/catalog and session state.

#### Expected behavior

- Scope, Impact, Selection and Execution are CURRENT.
- Operation REPORTED and Persistence NOT_APPLICABLE.
- Required-minus-mapped set is empty and all units are VERIFIED.
- Coverage is VERIFIED COVERAGE.
- No release PASS or COMPLETE is emitted.
- Exact selection and execution paths/revisions are handed to the external gate.

#### Assertions

- [ ] Report remains byte-preserving.
- [ ] Sensitivity and ordinary execution are both required.
- [ ] Any partial/stale/unknown predicate prevents verified coverage.
- [ ] Selection success is not release success.

#### Case Verdict

PASS only for exact all-current report evidence; otherwise fail closed.

---

## Protocol Compliance

- [ ] **[RS-PC-001]** Exact explicit mode and scope manifest validate before
  project discovery or writes.
- [ ] **[RS-PC-002]** Stable scope, plan, build, ownership, requirement, impact,
  bug, test and receipt identities are raw-revision-bound.
- [ ] **[RS-PC-003]** Budget admission and prioritization are deterministic and
  fully ledgered.
- [ ] **[RS-PC-004]** Coverage is exact Coverage Unit set arithmetic with no
  filename/prose inference.
- [ ] **[RS-PC-005]** Verified-fixed bugs and quarantines require their complete
  independent receipt chains.
- [ ] **[RS-PC-006]** PARTIAL, STALE and UNKNOWN states remain explicit and never
  become current or verified.
- [ ] **[RS-PC-007]** Report performs zero writes and mode-specific operation
  vocabulary is truthful.
- [ ] **[RS-PC-008]** Update/audit use keyed field patches only and preserve all
  human/unknown bytes.
- [ ] **[RS-PC-009]** Tombstones require exact approval, preserve history and
  reserve IDs forever.
- [ ] **[RS-PC-010]** Publication uses complete candidate validation, authority
  Revalidate, one-file CAS and read-back.
- [ ] **[RS-PC-011]** Runner/build receipt ownership and execution remain separate
  from selection maintenance.
- [ ] **[RS-PC-012]** No test/helper/CI/build/release/catalog/session workflow is
  authored, mutated or invoked.

## Coverage Notes

### Authoritative P1 audit traceability

| Audit ID | Implemented clause | Concrete case and assertion cells |
|---|---|---|
| `RS-004` | `SKILL.md` Phase 1.2 QA-plan scope/provenance and contract-manifest budgets | `RS-C01`; “No undeclared file becomes coverage evidence”; “Ledger counts reconcile to scope declaration” |
| `RS-005` | `SKILL.md` Phase 1.3 verified bug requirements | `RS-C02`; “Fix commit does not replace build verification”; “Build artifact/source/platform/configuration compatibility is checked” |
| `RS-006` | `SKILL.md` Phase 2 stable inventory and Coverage computation exact set arithmetic | `RS-C03`; “No model judgment labels a partial subset covered”; “Missing unit IDs are listed exactly” |
| `RS-007` | `SKILL.md` Phase 1.4 explicit revision impact plus Phase 2 source revision freshness | `RS-C04`; “No day-count drift heuristic is used”; “Requirement raw span and file revision both revalidate” |
| `RS-008` | `SKILL.md` Phase 1.5 quarantine registry/receipt validation | `RS-C05`; “APPLIED is not inferred from proposal”; “VERIFIED is not inferred from intended skip”; “Exact applied config revision and Test ID are required” |
| `RS-009` | `SKILL.md` Phase 3 coverage verdict separated from Phase 5 operation result | `RS-C06`; “Operation and coverage dimensions are both emitted”; “Successful write does not change missing unit state” |
| `RS-010` | `SKILL.md` Phase 1.1 explicit mode and Phase 5.2 authorization boundary | `RS-C07`; “Side-effect class is known from the subcommand”; “No parameterless write-mode prompt occurs”; “Report never asks for write approval” |
| `RS-016` | Dedicated spec fixture/side-effect contract, current selection artifact, and verdict vocabulary | `RS-C08`; “Every case has explicit fixture and side-effect boundary”; “No obsolete production/qa coverage-report output is expected”; “No FULL COVERAGE legacy verdict replaces current statuses” |
| `RS-017` | `SKILL.md` Phase 5.1 remediation handoff preserves test-authoring ownership and forbids helper substitution | `RS-C09`; “Helper validation is not business coverage”; “Handoff owner has authority to create the missing test” |
| `RS-018` | `SKILL.md` Phase 5.3 mode-specific operation protocol | `RS-C10`; “Manifest before/after bytes are identical”; “No history/revision is added”; “Actual mode is visible” |

`RS-C11` tests deterministic change impact/priority, `RS-C12` tests tombstone and
keyed CAS preservation, `RS-C13` tests selection/execution separation, and
`RS-C14` tests complete current coverage with exact execution. This is a written
contract, not an executed runner or release result.
