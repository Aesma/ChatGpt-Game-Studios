# Skill Spec: $test-evidence-review

> **Spec ID**: test-evidence-review-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: analysis
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$test-evidence-review` consumes one revision-bound `cgs-test-evidence-review-manifest/v2`. It reviews typed evidence on independent structural-quality, admissibility, execution-result, execution-currency, completeness, and scope axes. Default operation is strictly read-only; `--persist` may create one immutable atomically verified report.

## Static Assertions

- **TER-STA-001**: Frontmatter contains only `name` and non-empty `description`; name is `test-evidence-review`.
- **TER-STA-002**: The only invocation takes one canonical review-manifest path plus optional `--persist`; no caller-supplied content token is accepted.
- **TER-STA-003**: Current scope is resolved from exact stage/session manifests, never latest modification time.
- **TER-STA-004**: Sprint scope requires exactly one matching active sprint identity.
- **TER-STA-005**: Every scope row binds Story, Requirement, AC, Coverage Unit, Test/Check, owner, method, and evidence IDs.
- **TER-STA-006**: Candidate, build receipt, artifact, source commit, platform, configuration, QA-plan, and source revisions are cross-bound.
- **TER-STA-007**: Requirement coverage is semantic and stable-ID-based, not inferred from names, comments, or tokens.
- **TER-STA-008**: Reviewer attestations bind verified identity, time, scope, build, evidence revisions, statement, result, and authorization source.
- **TER-STA-009**: Relevant source-set byte changes make dependent evidence stale.
- **TER-STA-010**: Missing, unavailable, partial, stale, and unknown states remain distinct.
- **TER-STA-011**: Workflow Status, Structural Quality, Admissibility, Execution Result/Currency/Completeness/Scope, Closure, and Persistence are independent.
- **TER-STA-012**: No second PASS/WARNINGS/FAIL or COMPLETE/CONCERNS verdict vocabulary exists.
- **TER-STA-013**: Canonical naming requires unambiguous system, scenario, and expected fields.
- **TER-STA-014**: Naming conformance is maintainability evidence only and cannot prove requirement coverage.
- **TER-STA-015**: Evidence types have explicit admissibility limits and minimum bindings.
- **TER-STA-016**: File presence proves only PRESENT and cannot prove content, approval, or execution.
- **TER-STA-017**: Assertion-token counts and assertion-per-function thresholds are prohibited.
- **TER-STA-018**: Manual/visual/log evidence requires content inspection plus exact artifact receipt.
- **TER-STA-019**: A current execution PASS never implies structural adequacy, and ADEQUATE never implies execution.
- **TER-STA-020**: Every declared AC emits exactly one result row even when evidence is unreadable.
- **TER-STA-021**: Findings use versioned rule IDs and deterministic revision stable keys.
- **TER-STA-022**: Default review lists zero write paths and is byte-for-byte read-only.
- **TER-STA-023**: Optional persistence owns exactly one scope-revision-addressed immutable report.
- **TER-STA-024**: Persisted report publication uses absent-target atomic conflict check and read-back verification.

## Protocol Assertions

- **TER-PRO-001**: revision raw input bytes before parsing and reject duplicate keys.
- **TER-PRO-002**: Reject direct test paths, globs, ambiguous names, unsafe paths, and newest-file discovery.
- **TER-PRO-003**: Never omit an AC row because an input is missing or unreadable.
- **TER-PRO-004**: Never let one evidence type prove an axis prohibited by its admissibility contract.
- **TER-PRO-005**: Never infer requirement coverage from a filename, comment, or token count.
- **TER-PRO-006**: Never fabricate, complete, or copy forward a reviewer attestation.
- **TER-PRO-007**: Never classify an unreadable declared artifact as product-level MISSING.
- **TER-PRO-008**: Never restore freshness from dates, sprint start, or modification time.
- **TER-PRO-009**: Never convert targeted, partial, stale, unpersisted, or nonconclusive execution into full closure.
- **TER-PRO-010**: Rerunning unchanged bytes produces identical finding IDs and order.
- **TER-PRO-011**: A declined or failed report write preserves observed review axes and findings.
- **TER-PRO-012**: Never edit tests, evidence, requirements, manifests, stage/session state, or shared catalog files.
- **TER-PRO-013**: Never invoke tests, downstream gates, directors, or remediation workflows.
- **TER-PRO-014**: Downstream consumers receive exact report path/revision and revalidate referenced authorities.
- **TER-PRO-015**: A conversation-only review is not a durable review receipt.

## Test Cases

### Case 1 — Unique active sprint comes from stage and session manifests

#### Fixture

Two sprint directories have recent timestamps. The revision-bound stage and active-session manifests identify exactly one active sprint `SPR-42`.

#### Input

Review a sprint-scoped `cgs-test-evidence-review-manifest/v2`.

#### Expected reads

Only the declared review, stage, session, QA-plan, candidate/build, scope-row, and evidence authorities.

#### Expected writes

None unless `--persist` is separately present and authorized.

#### Expected non-writes

No sprint state update, latest-directory marker, manifest repair, inferred sprint file, or report in default mode.

#### Expected behavior

The workflow selects `SPR-42` only after stage/session/QA identities and revisions agree. Multiple or conflicting active sprint declarations block the review.

#### Assertions

TER-STA-003, TER-STA-004, TER-PRO-001, TER-PRO-002.

#### Case Verdict

PASS when the unique declared sprint is used and timestamps are ignored; otherwise BLOCKED.

### Case 2 — Evidence manifest explicitly links story, AC, build, and revision

#### Fixture

One scope row contains Story, Requirement, AC, Coverage Unit, Test ID, expected observable, candidate/build, evidence IDs, paths, and revisions. A similarly named unbound test file also exists.

#### Input

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

#### Expected reads

The exact QA plan, requirement sources, candidate, build receipt, test metadata/source, and typed evidence declared by the row.

#### Expected writes

None.

#### Expected non-writes

No inferred mapping, discovered evidence row, generated stable ID, or authority edit.

#### Expected behavior

Only the exact stable-ID and revision-bound row enters the review. The similarly named file is irrelevant.

#### Assertions

TER-STA-005, TER-STA-006, TER-PRO-002, TER-PRO-005.

#### Case Verdict

PASS only when every binding agrees; ambiguity or revision mismatch blocks or stales the affected row.

### Case 3 — Names and assertion text cannot manufacture coverage

#### Fixture

A conformingly named test contains assert-like words in comments, strings, duplicate assertions, and an opaque helper. It lacks a semantic observable and failure-sensitivity proof for its AC.

#### Input

Review automated structural quality.

#### Expected reads

The exact test source, stable metadata, helper implementation/contract if declared, QA requirement row, and negative-control or mutation receipts.

#### Expected writes

None.

#### Expected non-writes

No assertion count, invented helper semantics, inferred AC mapping, generated mutation result, or quality PASS.

#### Expected behavior

Comments, names, tokens, repetitions, and opaque helpers do not prove coverage. The row is structurally INCOMPLETE with stable semantic and sensitivity findings.

#### Assertions

TER-STA-007, TER-STA-017, TER-PRO-005.

#### Case Verdict

INCOMPLETE structural quality; execution remains independently classified.

### Case 4 — Nonempty role label is not an attestation

#### Fixture

A manual artifact contains `qa-lead` in a sign-off field but has no verifier-supported identity, scope, build, artifact revisions, statement, timestamp, or authorization source.

#### Input

Validate the required reviewer attestation.

#### Expected reads

The artifact receipt, declared attestation record, attester registry or verification receipt, and exact reviewed evidence.

#### Expected writes

None.

#### Expected non-writes

No filled identity, inferred approval, copied prior signature, role impersonation, or closure approval.

#### Expected behavior

The role label is inadmissible as approval. The row gets an attestation finding and closure NO. The model does not sign.

#### Assertions

TER-STA-008, TER-PRO-006.

#### Case Verdict

INCOMPLETE or INADMISSIBLE with closure NO.

### Case 5 — Any relevant source-byte change makes dependent evidence stale

#### Fixture

A previously valid execution receipt and attestation bind an older helper source revision. The current helper bytes differ while timestamps appear recent.

#### Input

Revalidate currentness.

#### Expected reads

Every relevant-source-set member and its captured path/revision, plus the receipt and attestation bindings.

#### Expected writes

None.

#### Expected non-writes

No refreshed revision, carried-forward approval, date-based freshness override, or source rollback.

#### Expected behavior

The exact mismatch creates a stable stale finding. Execution Currency is STALE; affected structural/attestation fields cannot support closure.

#### Assertions

TER-STA-009, TER-PRO-008.

#### Case Verdict

STALE with closure NO.

### Case 6 — Read failure, partial receipt, and absent evidence stay distinct

#### Fixture

AC-A explicitly lacks a required artifact, AC-B declares an artifact that cannot be decoded, AC-C has a truncated execution receipt with some valid rows, and AC-D declares no current execution receipt.

#### Input

Review all four rows.

#### Expected reads

Every readable declared authority and bounded partial evidence.

#### Expected writes

None in default mode.

#### Expected non-writes

No omitted AC row, fabricated byte, zero-filled result, generalized MISSING label, or PASS.

#### Expected behavior

AC-A is MISSING, AC-B UNAVAILABLE, AC-C execution PARTIAL with currentness determined separately, and AC-D execution UNKNOWN/NONE. Workflow is PARTIAL where inspection could not complete.

#### Assertions

TER-STA-010, TER-STA-020, TER-PRO-003, TER-PRO-007.

#### Case Verdict

PASS only if all states remain distinct and closure is NO.

### Case 7 — Review vocabulary has independent axes and no second verdict

#### Fixture

A structurally adequate row has a current conclusive execution FAIL. Another row is structurally incomplete but has a current execution PASS.

#### Input

Aggregate both rows.

#### Expected reads

Per-row structural, admissibility, execution, currentness, completeness, scope, and finding states.

#### Expected writes

None.

#### Expected non-writes

No single overloaded Verdict, PASS WITH WARNINGS, COMPLETE/CONCERNS, or flattened worst label.

#### Expected behavior

The first preserves ADEQUATE plus FAIL; the second preserves INCOMPLETE plus PASS. Aggregate axes follow the deterministic decision table and closure is NO.

#### Assertions

TER-STA-011, TER-STA-012, TER-STA-019.

#### Case Verdict

PASS when no axis overwrites another.

### Case 8 — Canonical naming requires system, scenario, and expected fields

#### Fixture

Test A is valid under the exact naming schema. Test B omits system. Test C contains ambiguous underscores that the schema parser rejects. Test D has a valid name but no stable AC mapping.

#### Input

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

#### Expected reads

The exact naming-schema bytes and each declared test name/metadata.

#### Expected writes

None.

#### Expected non-writes

No heuristic splitting, invented system, AC binding, coverage proof, or source rename.

#### Expected behavior

A passes naming; B and C receive naming findings; D remains unproven structurally despite naming conformance.

#### Assertions

TER-STA-013, TER-STA-014, TER-PRO-005.

#### Case Verdict

PASS when naming remains an independent maintainability result.

### Case 9 — Registered spec and skill share one exact contract

#### Fixture

The candidate skill, metadata, and registered `cgs-skill-spec/v2`.

#### Input

Run static contract comparison.

#### Expected reads

All three candidate files.

#### Expected writes

None.

#### Expected non-writes

No live skill, shared catalog, test, evidence, report, or source modification.

#### Expected behavior

Invocation, manifest schemas, read set, optional one-report write set, authorization, independent result axes, read-only default, and persistence semantics match. Cases 1 through 15 are contiguous and contain every required subsection.

#### Assertions

TER-STA-001 through TER-STA-024; TER-PRO-001 through TER-PRO-015.

#### Case Verdict

PASS only when the registered contract is complete, aligned, and fail-closed.

### Case 10 — Structural adequacy without current execution remains unknown

#### Fixture

A test has exact stable mapping, observable semantics, helper traceability, and current failure-sensitivity evidence. No current-build execution receipt is declared.

#### Input

Review the row.

#### Expected reads

The exact structural sources and admissible sensitivity receipt.

#### Expected writes

None.

#### Expected non-writes

No execution receipt, execution PASS, full scope, closure approval, or fabricated run.

#### Expected behavior

Structural Quality is ADEQUATE; Execution Result and Currency are UNKNOWN; Completeness is NONE; Scope is NONE; closure is NO.

#### Assertions

TER-STA-019, TER-PRO-009, TER-PRO-013.

#### Case Verdict

ADEQUATE structural quality with execution UNKNOWN and closure NO.

### Case 11 — Evidence types cannot prove prohibited axes

#### Fixture

A QA plan selects a Test ID, a build receipt proves the artifact, a screenshot shows a UI state, and an execution receipt proves a current automated result.

#### Input

Evaluate each evidence item against the typed admissibility registry.

#### Expected reads

Every evidence contract, raw artifact/receipt, stable subject binding, and verifier.

#### Expected writes

None.

#### Expected non-writes

No QA-plan execution PASS, build-receipt test PASS, screenshot approval, or execution-receipt structural ADEQUATE inference.

#### Expected behavior

Each item proves only its allowed claims. Valid narrow evidence is LIMITED; prohibited cross-axis use is INADMISSIBLE.

#### Assertions

TER-STA-015, TER-STA-016, TER-PRO-004.

#### Case Verdict

PASS when all admissibility boundaries hold.

### Case 12 — Existing screenshot requires receipt and content inspection

#### Fixture

A screenshot file exists but its artifact receipt lacks build/platform/captor/AC mapping, and the viewer cannot decode its contents.

#### Input

Review the manual evidence row.

#### Expected reads

The bounded image bytes, artifact receipt, expected observable, build/environment authorities, and decoder availability.

#### Expected writes

None.

#### Expected non-writes

No screenshot PASS, invented metadata, approval, content description, or MISSING classification.

#### Expected behavior

Presence is PRESENT. Provenance is INCOMPLETE or INADMISSIBLE; content inspection is UNAVAILABLE; execution result remains UNKNOWN; closure is NO.

#### Assertions

TER-STA-016, TER-STA-018, TER-PRO-007.

#### Case Verdict

UNAVAILABLE/INCOMPLETE, never ADEQUATE or PASS.

### Case 13 — Stable findings are reproducible across unchanged runs

#### Fixture

Two reviews consume byte-identical manifests and evidence with the same three issues. A third review changes one observed source revision.

#### Input

Generate and sort findings for all reviews.

#### Expected reads

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

#### Expected writes

None.

#### Expected non-writes

No random finding ID, order based on discovery time, or reused stable key after an observed identity changes.

#### Expected behavior

The first two reviews produce identical IDs, stable keys, fields, and order. The changed source produces a different stale-finding stable key while unaffected findings remain stable.

#### Assertions

TER-STA-021, TER-PRO-010.

#### Case Verdict

PASS when determinism and change sensitivity both hold.

### Case 14 — Default read-only and optional immutable report are separate

#### Fixture

The same complete review is run once without `--persist`, once with persistence declined, once with authorized persistence, and once against an existing destination.

#### Input

Execute the four persistence variants.

#### Expected reads

The exact review/evidence authorities; for writes, all inputs again at atomic conflict check time plus target absence and read-back bytes.

#### Expected writes

Zero paths for default and decline; exactly one scope-revision-addressed report for authorized absent-target persistence; zero final writes on collision.

#### Expected non-writes

No test/evidence/requirement/stage/session/catalog mutation, overwrite, append, latest pointer, or changed observed findings after persistence failure.

#### Expected behavior

Results respectively report NOT_REQUESTED, DECLINED, WRITTEN after atomic conflict check/read-back, and FAILED on collision. Review axes/findings remain identical.

#### Assertions

TER-STA-022, TER-STA-023, TER-STA-024, TER-PRO-011, TER-PRO-012, TER-PRO-015.

#### Case Verdict

PASS when mutation boundaries and persistence independence are exact.

### Case 15 — Full admissible current evidence happy path

#### Fixture

One unique active scope, CURRENT QA plan, exact candidate/build, complete stable AC rows, adequate semantic tests, admissible manual content, verified attestations, and full-scope current execution receipts all revision-match. `--persist` is authorized and the target is absent.

#### Input

Review, aggregate, atomic conflict check-persist, and verify the report as a downstream consumer.

#### Expected reads

Every exact stage/session/QA/requirement/candidate/build/test/helper/evidence/attestation authority and the final report read-back bytes.

#### Expected writes

Exactly one immutable `cgs-test-evidence-review-report/v2` at its review-ID and scope-revision-addressed path.

#### Expected non-writes

No authority edits, test execution, approval generation, downstream workflow invocation, mutable latest pointer, or additional report member.

#### Expected behavior

Every AC emits one ADEQUATE/ADMISSIBLE/PASS/CURRENT/COMPLETE/FULL row with no blockers. Aggregate closure is YES; report atomic conflict check and read-back verify; the consumer re-reads the exact report and referenced authorities.

#### Assertions

TER-STA-001 through TER-STA-024; TER-PRO-001 through TER-PRO-015.

#### Case Verdict

PASS only when every axis, finding set, immutable persistence check, and downstream verification succeeds.



## P1 audit remediation trace

| Audit ID | SKILL clause | Executable specification hook | Negative assertion |
|---|---|---|---|
| TER-004 | Phase 1 | Case 1 / TER-STA-003, TER-STA-004, TER-PRO-001, TER-PRO-002 | Newest/mtime sprint selection cannot pass |
| TER-005 | Manifest + Phase 2 | Case 2 / TER-STA-005, TER-STA-006, TER-PRO-002, TER-PRO-005 | Unbound fixed paths or arbitrary smoke evidence cannot enter scope |
| TER-006 | Phase 4 | Case 3 / TER-STA-007, TER-STA-017, TER-PRO-005 | Names/comments/assert counts cannot manufacture coverage |
| TER-007 | Phase 7 | Case 4 / TER-STA-008, TER-PRO-006 | Nonempty role text or model-generated signature is invalid |
| TER-008 | Phase 2 | Case 5 / TER-STA-009, TER-PRO-008 | Dates never override changed relevant bytes |
| TER-009 | Phases 9–10 | Case 6 / TER-STA-010, TER-STA-020, TER-PRO-003, TER-PRO-007 | Unreadable/partial/unknown cannot be mislabeled product MISSING |
| TER-010 | Independent axes + Phase 10 | Case 7 / TER-STA-011, TER-STA-012, TER-STA-019 | COMPLETE/CONCERNS or PASS/WARNINGS/FAIL cannot replace the declared axes |
| TER-015 | Phase 5 | Case 8 / TER-STA-013, TER-STA-014, TER-PRO-005 | Unparseable system/scenario/expected creates only naming evidence |
| TER-016 | Purpose/invocation/Phases 11–12 | Case 9 / all TER-STA and TER-PRO assertions | Direct test-path/code-quality/alternate-verdict contract cannot pass alignment |

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
