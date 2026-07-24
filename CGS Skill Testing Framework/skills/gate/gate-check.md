# Skill Test Spec: `$gate-check`

## Skill summary and oracle

`$gate-check` is a strictly read-only assessment of one catalog-authorized,
adjacent phase transition. It validates a versioned authority record, evaluates
one bounded versioned profile, normalizes current hash-bound evidence, treats the
director panel as advisory, and emits `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`
plus `cgs.gate-record/v2`. It never advances stage. Plain
`production/stage.txt` is legacy observation only.

The behavioral oracle is the complete package:

- `.agents/skills/gate-check/SKILL.md`
- `.agents/skills/gate-check/references/evaluation-contract.md`
- `.agents/skills/gate-check/references/transition-profiles.md`
- `.agents/skills/gate-check/references/continued-workflow.md`

Evaluate all four files. A test that reads only the entry file is incomplete.

---

## Static assertions

- [ ] Frontmatter contains only required `name` and non-empty `description`.
- [ ] Public invocation declares all six exact transition IDs and rejects phase
      shorthand, unknown/repeated single-use options, and non-adjacent edges.
- [ ] Catalog-backed versioned authority is required before profile work.
- [ ] Plain `production/stage.txt` is explicitly `LEGACY_DECLARATION` and cannot
      select or validate a stage.
- [ ] `ERROR` is separate from gate verdict and emits no gate record.
- [ ] Gate verdict vocabulary is exactly PASS, CONCERNS, FAIL, PARTIAL.
- [ ] Deterministic precedence covers confirmed blocker, incomplete coverage,
      advisory-only, and all-pass paths.
- [ ] A confirmed blocking failure remains FAIL when coverage is also partial.
- [ ] Six profile IDs have stable check IDs, fixed scope rules, and numeric hard
      limits for manifest/files/context/hash/actions/time.
- [ ] Native producer adapters preserve native verdict and currentness.
- [ ] Producer adapters allowlist exact current envelope/extension or native
      schema versions and fail closed on unknown versions without legacy fallback.
- [ ] `cgs.gate-attestation/v1` binds question/operator/time/profile/scope/subject.
- [ ] Directors are advisory; NOT READY cannot directly create FAIL.
- [ ] Enabled director timeout/block/error/malformed/stale prevents PASS and
      yields PARTIAL absent a confirmed blocker.
- [ ] Solo skips only directors and keeps every deterministic/evidence rule.
- [ ] Output is `cgs.gate-record/v2` with authority, scope budgets, checks,
      coverage, panel, attestations, verification, and `stage_mutated: false`.
- [ ] Accepted risk uses separate `cgs.advance-request/v2` and never alters gate
      verdict/eligibility/coverage.
- [ ] No instruction writes project files or records director outcome in a source
      document/session-state file.

---

## Fixture contract

Every executable case freezes:

- repository identity/ref/dirty state and a before-tree path/hash snapshot;
- shared catalog hash with versioned stage schema, graph, owner, canonical
  authority path, receipt/freshness policy;
- valid authority record path/hash/prior chain/receipt for the tested origin;
- selected profile ID and complete bounded input manifest;
- explicitly named producer records and all dependency hashes;
- review mode and director fixture results; and
- after-tree snapshot plus authority/history/stage-file bytes.

Fixtures never identify evidence by mtime or `latest`. Hash changes create a new
fixture identity. Unless a case says otherwise, all profile checks pass, coverage
is complete, directors return READY in lean/full, and mutation guard passes.

---

## Table A: Invocation and authority validation

Run each row independently and assert no artifact/profile/director work occurs on
ERROR.

| Case | Invocation/state | Expected result/reason |
|---|---|---|
| A01 | `$gate-check production` | ERROR / invalid phase shorthand |
| A02 | `$gate-check concept-to-production` | ERROR / unknown non-adjacent edge |
| A03 | two transition positionals | ERROR / repeated positional |
| A04 | `--review full --review solo` | ERROR / repeated single-use option |
| A05 | `--review fast` | ERROR / invalid option value |
| A06 | unknown option or missing option value | ERROR / invocation invalid |
| A07 | catalog lacks stage schema/graph/owner/receipt policy | ERROR / STAGE_AUTHORITY_UNVERIFIED |
| A08 | authority missing/malformed/stale/unauthorized/broken prior chain | ERROR / STAGE_AUTHORITY_UNVERIFIED |
| A09 | registry edge differs from catalog edge | ERROR / TRANSITION_SCHEMA_CONFLICT |
| A10 | explicit transition origin differs from authority stage | ERROR / stage mismatch |
| A11 | backward/repeated/already-completed transition | ERROR / stage mismatch |
| A12 | no ID and authority stage is Release | ERROR / no outgoing edge |
| A13 | no ID and graph has zero or multiple outgoing edges | ERROR / ambiguous graph |
| A14 | unsafe/outside-root/symlink-escape authority path | ERROR / unsafe path |
| A15 | invalid `production/review-mode.txt` without override | ERROR / invalid review mode |

Assertions for every row:

- [ ] Result uses `cgs.gate-error/v1` where the contract provides it.
- [ ] No `cgs.gate-record/v2`, attestation, advance request, or director dispatch.
- [ ] `stage_mutated: false`; repository snapshot is unchanged.

### Legacy declaration rows

| Case | Versioned authority | `stage.txt` | Expected |
|---|---|---|---|
| A16 | valid Systems Design | missing | authority selects Systems Design |
| A17 | valid Systems Design | `Systems Design` | record `AGREES_ADVISORY_ONLY`; authority still selects |
| A18 | valid Systems Design | `Production` | record `CONTRADICTS_AUTHORITY`; authority still selects |
| A19 | missing authority | valid-looking `Concept` | ERROR; legacy value cannot rescue authority |

### Auto-selection evidence

With no transition ID and one valid outgoing catalog edge:

- [ ] Show exact edge and authority path/hash before checks.
- [ ] Rejection stops with no gate record.
- [ ] Confirmation records `AUTHORITY_AUTO_CONFIRMED` and `true`.
- [ ] An explicitly supplied ID records `EXPLICIT` and null confirmation.

---

## Table B: Six transitions and review-mode invariance

For each row, run `solo`, `lean`, and `full` (18 passing-path fixtures):

| Transition ID | Authority stage | Candidate | Profile ID |
|---|---|---|---|
| `concept-to-systems-design` | Concept | Systems Design | `gate.concept-to-systems-design/v2` |
| `systems-design-to-technical-setup` | Systems Design | Technical Setup | `gate.systems-design-to-technical-setup/v2` |
| `technical-setup-to-pre-production` | Technical Setup | Pre-Production | `gate.technical-setup-to-pre-production/v2` |
| `pre-production-to-production` | Pre-Production | Production | `gate.pre-production-to-production/v2` |
| `production-to-polish` | Production | Polish | `gate.production-to-polish/v2` |
| `polish-to-release` | Polish | Release | `gate.polish-to-release/v2` |

Assertions:

- [ ] Profile identity and authority edge match before manifest work.
- [ ] Every profile check ID appears exactly once.
- [ ] Full/lean/solo use byte-identical deterministic scope/evidence inputs and
      normalized non-director check results.
- [ ] Solo emits four `NOT_APPLICABLE_BY_MODE` rows; no directors spawn.
- [ ] Lean/full emit four current COMPLETE READY rows in this passing fixture.
- [ ] Verdict PASS, coverage COMPLETE, disposition ELIGIBLE.
- [ ] v2 record says `stage_mutated: false`; tree/authority/history unchanged.

---

## Table C: Deterministic verdict precedence

| Case | Normalized condition | Expected verdict | Coverage | Table row |
|---|---|---|---|---|
| C01 | all applicable blocking PASS; no advisory | PASS | COMPLETE | 4 |
| C02 | all blocking PASS; one advisory ADVISORY | CONCERNS | COMPLETE | 3 |
| C03 | one blocking FAIL | FAIL | COMPLETE | 1 |
| C04 | one blocking UNBOUND | FAIL | COMPLETE | 1 |
| C05 | one blocking STALE | FAIL | COMPLETE | 1 |
| C06 | no blocker; required UNKNOWN | PARTIAL | PARTIAL | 2 |
| C07 | no blocker; required NOT_EVALUATED | PARTIAL | PARTIAL | 2 |
| C08 | blocking FAIL plus another required NOT_EVALUATED | FAIL | PARTIAL | 1 |
| C09 | applicable predicate not checked but marked N/A | PARTIAL | PARTIAL | 2 |
| C10 | verified NOT_APPLICABLE and all remaining pass | PASS | COMPLETE | 4 |
| C11 | multiple director concerns only | CONCERNS | COMPLETE | 3 |
| C12 | director NOT READY only | CONCERNS | COMPLETE | 3 |
| C13 | enabled director missing/timeout with no blocker | PARTIAL | PARTIAL | 2 |
| C14 | enabled director timeout plus blocker | FAIL | PARTIAL | 1 |

For all rows, recompute after Chain-of-Verification. The skill must not average,
majority-vote, or let accepted risk change the expected row.

---

## Table D: Director panel contract

| Mode/result | Expected normalized behavior |
|---|---|
| solo | no spawn; four N/A-by-mode; complete policy coverage |
| lean/full all READY | four PASS advisory-source checks; panel COMPLETE |
| lean/full one CONCERNS | advisory finding; overall at least CONCERNS |
| lean/full one NOT READY | advisory finding; cannot directly create FAIL |
| lean/full one TIMEOUT | one NOT_EVALUATED; panel PARTIAL; cannot PASS |
| lean/full BLOCKED/ERROR/MALFORMED/missing | same incomplete behavior as timeout |
| response for older manifest hash | STALE panel result; panel PARTIAL |
| response after 120-second deadline | exclude as late; TIMEOUT retained |

Assertions:

- [ ] Four dispatches are issued before waiting in lean/full.
- [ ] Each has exact transition/profile/manifest hash, one attempt, and deadline.
- [ ] No silent retry, local-agent substitution, persistence, or blocking-check
      override.
- [ ] Available director results remain visible in a partial panel.

---

## Table E: Bounded manifest and context

| Case | Fixture mutation | Expected |
|---|---|---|
| E01 | extra unrelated repository files | excluded; no scope/result change |
| E02 | generated/vendor/cache files match a discovery-like name | excluded |
| E03 | two unreferenced reports match a broad historical glob | neither selected; explicit identity still required |
| E04 | authoritative manifest has ambiguous/duplicate path identity | coverage gap; PARTIAL absent blocker |
| E05 | manifest-entry ceiling would be exceeded | stop before ceiling; BUDGET_EXCEEDED; PARTIAL |
| E06 | context-byte/full-file/hash/action/time ceiling would be exceeded | same; no sampling-to-PASS |
| E07 | required input unreadable or root-escaping symlink | coverage gap or ERROR per preflight; never PASS |
| E08 | input changes after manifest freeze | SNAPSHOT_CHANGED/STALE; recalculate once |
| E09 | authority changes during evaluation | ERROR / AUTHORITY_CHANGED_DURING_CHECK; no gate record |
| E10 | Production profile lacks explicit scope manifest | PARTIAL; no whole-repo fallback |
| E11 | Release profile lacks explicit release/policy/candidate identity | PARTIAL; no newest collector selection |

Verify the v2 record includes used/limit values for all six budgets and complete
included/excluded/unreadable/ambiguous sets.

---

## Table F: Manual attestation

Use a profile row that explicitly allows attestation (`CSD-M01` or `PPP-M01`).

| Case | Attestation state | Expected check status |
|---|---|---|
| F01 | complete/current `YES` | PASS |
| F02 | complete/current `NO` on blocking row | FAIL |
| F03 | explicit `UNKNOWN` | UNKNOWN; overall PARTIAL absent blocker |
| F04 | unanswered/ambiguous prose | NOT_EVALUATED; PARTIAL |
| F05 | missing operator/time/question/profile/scope/subject hash | UNBOUND; FAIL |
| F06 | expired or subject/scope hash changed | STALE; FAIL |
| F07 | attestation supplied for objective test/performance/legal check | reject; required objective check remains unsatisfied |
| F08 | skill invents operator/signature or persists attestation | spec failure |

Assert the record preserves complete `cgs.gate-attestation/v1`, ID, exact question,
normalized answer, operator assurance, times, and subject hashes.

---

## Table G: Producer adapter thresholds

All passing rows also require exact current path/hash/build/scope, required
persistence, and complete native dependency fields. Missing binding -> UNBOUND;
hash/currentness mismatch -> STALE regardless of verdict.

| Adapter | Passing native state | Non-passing examples |
|---|---|---|
| PA-DESIGN-REVIEW-1 | independent full/lean APPROVED | solo/advisory, NEEDS/MAJOR/PARTIAL/error |
| PA-CROSS-GDD-1 | persisted `cgs.review-evidence/v1` + `cgs.cross-gdd-review/v2`; full/full PASS + COMPLETE coverage | CONCERNS, FAIL, PARTIAL, v1 extension, envelope-only |
| PA-ARCH-REVIEW-1 | PASS current manifest | BLOCKED, PARTIAL |
| PA-UX-REVIEW-1 | none under current `cgs.review-evidence/v1` + `cgs.ux-review/v2` producer contract | APPROVED with NOT_PERSISTED/false eligibility, NEEDS/MAJOR/PARTIAL/null/error, invented recorder |
| PA-ART-BIBLE-1 | external independent APPROVE exact complete AB-1 hash | internal self-signoff, CONCERNS/REJECT/PARTIAL |
| PA-VERTICAL-SLICE-1 | persisted/current `cgs.vertical-slice-evaluation-report/v2`; COMPLETE + Evidence/Product/Final PROCEED + VERIFIED/YES | schema 1, skipped/PARTIAL/INCONCLUSIVE/PIVOT/KILL/BLOCKED |
| PA-SMOKE-1 | persisted `cgs-smoke-check-receipt/v2`; sprint PASS + VERIFIED + Handoff Eligible YES, no warnings | schema 1, quick TARGETED CHECK PASSED, FAIL/INCOMPLETE/warnings |
| PA-TEAM-QA-1 | persisted `cgs.team-qa-signoff/v2`; WORKFLOW_COMPLETED + QA_APPROVED + VERIFIED/YES | old COMPLETE/APPROVED vocabulary, QA_APPROVED_WITH_CONDITIONS, QA_NOT_APPROVED, QA_INCOMPLETE |
| PA-PLAYTEST-1 | canonical unique `cgs.playtest-report/v2` + `cgs.playtest-report-recorder-receipt/v1`; RECORDED COMPLETED — GATE ELIGIBLE | candidate envelope alone, REQUIRES RECORDER, protocol/template/duplicate/legacy/stale |
| PA-REGRESSION-1 | selection + exact runner receipt; all required pass | selection only, awaiting, missing sensitivity, failure |
| PA-TEST-EVIDENCE-1 | persisted `cgs-test-evidence-review-report/v2`; COMPLETE/ADEQUATE/ADMISSIBLE/PASS/CURRENT/COMPLETE/FULL/Closure Eligible YES | schema 1, missing/unknown/stale/not-run/closure-ineligible row |
| PA-PERFORMANCE-1 | current `cgs.review-evidence/v1` + `cgs.performance-report/v1` + `cgs.performance-budget/v2` + independent `cgs.performance-report-recorder-receipt/v1`; full matrix, unchanged WITHIN BUDGET, candidate/target flags true, RECORDED, targets met true, gate eligible true, create-only CAS/read-back verified | analyzer candidate alone, missing/invalid receipt, CONCERNS/OVER BUDGET, false target flag, wrong canonical path/bytes/identity, self-recording, static/plan/partial |
| PA-RELEASE-COLLECTOR-1 | all HARD PASS/authorized N/A; NOT EVALUATED collector field | HARD FAIL/UNKNOWN/stale/invalid N/A |
| PA-LOCALIZATION-1 | exact non-persisted `cgs.review-evidence/v1` candidate from `localize/evidence-review@cgs.localize-evidence-review/v1` plus independent current `cgs.localization-evidence-review-recorder-receipt/v1`; exact path/raw-hash-bound `cgs.localization-evidence-manifest/v2` extension; `cgs.localization-request/v2`, `cgs.localization-manifest/v2`, declared `cgs.localization-catalog/v2` path/raw hash/`catalog_identity_sha256`, ordered `cgs.localization-package/v1` path/raw-hash/ID/payload and per-key/locale/translation/freeze/build/font/UI/runtime rows; native QA_EVIDENCE_VERIFIED for every required locale/page; canonical create-only `production/qa/evidence/localization/<localization_candidate_sha256>/reports/<record_id_sha256>.md` and `production/qa/evidence/localization/<localization_candidate_sha256>/receipts/<record_id_sha256>.yaml`; `expected_report_preimage: ABSENT`; `expected_receipt_preimage: ABSENT`; CREATED CAS; exact `persisted_report_sha256`/bytes; matching `read_back_sha256`; VERIFIED read-back; RECORDED persistence; unchanged verdict; and gate eligibility | generic candidate alone; QA_EVIDENCE_REJECTED/PARTIAL_EVIDENCE; UNKNOWN/NOT_RUN/STALE; missing locale/page or distinct recorder; missing/invalid receipt; self-recording; wrong/reused canonical target; failed/non-created CAS; changed verdict; missing ordered binding; mismatched path/hash/currentness/expiry; unsupported producer/envelope/extension/receipt/request/manifest/catalog/package version |

Additional drift assertions:

- [ ] Concept profile never invokes system-GDD-only `$design-review`.
- [ ] Cross-GDD CONCERNS does not become required approval PASS.
- [ ] Smoke `PASS WITH WARNINGS` is never invented or accepted.
- [ ] Team-QA APPROVED_WITH_CONDITIONS is not gate eligible.
- [ ] Native and normalized verdicts both appear in the v2 record.
- [ ] A generic wrapper cannot upgrade an ineligible native payload.
- [ ] Cross-GDD rejects `cgs.cross-gdd-review/v1` and envelope-only input.
- [ ] UX `APPROVED` with `NOT_PERSISTED`/false eligibility remains incomplete.
- [ ] Vertical-slice schema 1, smoke schema 1, old Team-QA vocabulary, and
      test-evidence schema 1 all fail closed.
- [ ] Playtest candidate output without its exact independent recorder receipt
      remains incomplete and is not counted as a session.
- [ ] Performance `WITHIN BUDGET` with analyzer `persistence: NONE` remains
      incomplete without exact `cgs.performance-report-recorder-receipt/v1`.
- [ ] Localization generic candidate alone cannot pass: require producer
      `localize/evidence-review@cgs.localize-evidence-review/v1`, exact
      `cgs.localization-evidence-manifest/v2` extension path/raw hash, and one
      independent `cgs.localization-evidence-review-recorder-receipt/v1`.
- [ ] Localization rejects v1/unknown request, evidence-manifest,
      localization-manifest or catalog schema and rejects v2/unknown locale
      packages; catalog path/raw hash/catalog identity, package path/hash and
      currentness are mandatory rather than inferred from a verdict string.
- [ ] Localization candidate remains `persistence: NONE` and
      `recorder_receipt: NONE`; the receipt must prove distinct identities,
      canonical create-only report/receipt targets, both ABSENT preimages,
      `compare_and_set: CREATED`, exact returned-review hash/bytes,
      `read_back: VERIFIED`, unchanged native verdict,
      `evidence_persistence: RECORDED`, and `gate_evidence_eligible: true`.
- [ ] A current independent performance receipt with matching WITHIN BUDGET,
      `evidence_persistence: RECORDED`, `performance_targets_met: true`,
      `gate_evidence_eligible: true`, create-only CAS, and verified read-back can
      pass; CONCERNS/OVER BUDGET remain conclusive non-passing evidence.
- [ ] Unknown envelope, extension, payload, native-record, budget, and companion
      receipt versions normalize to INCOMPLETE/NOT_EVALUATED, never PASS.

---

## Table H: Accepted risk

Run once each from CONCERNS, FAIL, and PARTIAL.

- [ ] Gate record remains byte-for-byte unchanged and retains original verdict,
      coverage, disposition NOT_ELIGIBLE, findings, and record ID.
- [ ] No request is emitted without explicit operator and explicit finding/gap IDs.
- [ ] Complete request is `cgs.advance-request/v2`, includes gate/profile/
      authority/scope identities and `stage_mutated: false`.
- [ ] Omitted open finding/gap is reported as unaccepted.
- [ ] Request never claims PASS/ELIGIBLE or modifies authority/history/stage.
- [ ] PASS path emits no unnecessary accepted-risk request.

---

## Table I: Output/canonicalization and mutation guard

For PASS, CONCERNS, FAIL, PARTIAL, ERROR, and accepted-risk paths:

- [ ] Human report and machine record agree on every check/verdict/coverage field.
- [ ] `cgs.gate-record/v2` contains all required authority/scope/budget/check/
      attestation/panel/finding/verification/mutation fields.
- [ ] Check ordering follows the selected profile; every ID appears once.
- [ ] Canonical record hash excludes only `record_id`; one-byte change produces a
      different ID.
- [ ] Final authority/evidence/scope hashes are revalidated exactly once.
- [ ] Repository path/hash snapshot, authority/history, and `stage.txt` bytes are
      unchanged by the workflow.
- [ ] No report, attestation, gate record, advance request, checkpoint, session
      state, or director status is persisted.
- [ ] External concurrent changes are reported and never reverted.
- [ ] Any workflow-caused mutation fails the spec; no valid gate result is claimed.

---

## Transition-specific assertions

### Concept → Systems Design

- [ ] Uses the concept-specific deterministic profile, not the system-GDD rubric.
- [ ] Owner attestation binds the exact concept and scope hashes.
- [ ] Prototype absence is advisory only.

### Systems Design → Technical Setup

- [ ] MVP set comes only from current systems-index canonical entries.
- [ ] Every MVP GDD has current independent APPROVED review evidence.
- [ ] Cross-GDD report covers the complete current set and must be PASS.

### Technical Setup → Pre-Production

- [ ] ADR set is manifest-derived; cycle/version/deprecated/traceability checks are
      complete and architecture-review is current PASS.
- [ ] Declared canary has current execution evidence; source existence is not pass.

### Pre-Production → Production

- [ ] One explicit current persisted vertical-slice PROCEED graph is required.
- [ ] Art/UX approvals use their exact native adapters.
- [ ] Manual feel/playthrough attestation cannot replace vertical-slice/build
      evidence.

### Production → Polish

- [ ] Explicit production scope/candidate manifest prevents all-repository scans.
- [ ] Regression, clean smoke, exact APPROVED team QA, three canonical sessions,
      bug, performance, UX/accessibility checks all execute.

### Polish → Release

- [ ] Explicit release/policy/candidate matrix owns scope.
- [ ] Collector never self-approves; gate derives hard/advisory result.
- [ ] Exact QA/smoke/regression/performance/localization/bug/legal/package evidence
      is current for the candidate.

---

## Authoritative P1 audit traceability

Each row maps one authoritative audit ID to an implemented clause and concrete
test cells/assertions. The mappings are individual; no case range substitutes for
enumerated coverage.

| Audit ID | Implemented clause | Concrete case/assertion cells |
|---|---|---|
| `GTC-005` | `SKILL.md` Phase 6 deterministic precedence and `evaluation-contract.md` section 2 verdict function | Table C `C03` blocking FAIL; `C06` required UNKNOWN; `C08` FAIL plus partial coverage; `C10` verified N/A; `C11` advisory-only CONCERNS |
| `GTC-006` | `SKILL.md` Phase 5 bounded advisory panel and `evaluation-contract.md` section 8 panel contract | Table D `lean/full one NOT READY`; Table D `lean/full one TIMEOUT`; Table D `BLOCKED/ERROR/MALFORMED/missing`; Table C `C12`; `C13`; `C14`; assertion “No ... blocking-check override” |
| `GTC-007` | `SKILL.md` invocation modes and Phase 5 solo branch | Table B assertion “Full/lean/solo use byte-identical deterministic scope/evidence inputs”; Table B assertion “Solo emits four NOT_APPLICABLE_BY_MODE rows”; Table D `solo`; Table C `C03` remains blocking in every mode |
| `GTC-008` | `SKILL.md` invocation validation and Phase 1 catalog-backed authority/adjacency | Table A `A01`; `A02`; `A03`; `A08`; `A10`; `A11`; `A12`; `A13`; `A15` |
| `GTC-009` | `SKILL.md` Phase 2 bounded manifest and every versioned profile's numeric limits | Table E `E04`; `E05`; `E06`; `E10`; `E11`; assertion “no sampling-to-PASS” |
| `GTC-010` | `SKILL.md` Phase 4 and `evaluation-contract.md` section 7 `cgs.gate-attestation/v1` | Table F `F01`; `F03`; `F04`; `F05`; `F06`; `F07`; `F08` |
| `GTC-011` | `SKILL.md` prior-result checks, canonical evidence invariants, and `transition-profiles.md` exact adapter registry | Table G `PA-DESIGN-REVIEW-1`; `PA-CROSS-GDD-1`; `PA-UX-REVIEW-1`; `PA-LOCALIZATION-1`; localization envelope/extension, schema/path/hash/currentness and recorder assertions; assertion “Concept profile never invokes system-GDD-only design-review”; assertion “Cross-GDD CONCERNS does not become required approval PASS”; unknown-version fail-closed assertion |
| `GTC-012` | Complete four-file oracle, six versioned transition profiles, output mutation guard, and honest execution-result boundary | Table B `concept-to-systems-design`; `systems-design-to-technical-setup`; `technical-setup-to-pre-production`; `pre-production-to-production`; `production-to-polish`; `polish-to-release`; Table C `C02`; `C03`; `C06`; Table G `PA-VERTICAL-SLICE-1`; Table I mutation assertions; Execution-result integrity assertion |

---

## Recovery and stopping assertions

- [ ] Tool failure/budget exhaustion returns available report plus deterministic
      FAIL-with-partial-coverage or PARTIAL; never silently skips.
- [ ] Late responses/evidence do not mutate a frozen record; rerun needs new run ID.
- [ ] Recovery never expands scope, substitutes roles, repairs artifacts, or loops.
- [ ] Final response recommends at most one prioritized action plus Stop.
- [ ] No downstream skill/workflow is invoked automatically.
- [ ] Final statement says the project stage was not changed.

## Execution-result integrity

This specification defines intended behavior; it is not an execution receipt.
Do not update `CGS Skill Testing Framework/catalog.yaml` result fields until the
relevant static/spec/category runs actually execute and their immutable result
artifacts identify this exact package hash. Empty result fields remain honest
until then.
