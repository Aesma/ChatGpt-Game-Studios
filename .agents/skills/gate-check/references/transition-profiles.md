# Gate Check — Versioned Transition Profiles

This file is the normative checklist, bounded-scope, and producer-adapter registry
for `$gate-check`. Profile IDs and check IDs are stable public identifiers. Read
only the selected profile plus the common rules; never merge checks from another
transition or silently add project-wide scans.

## Common profile rules

All paths are repository-relative. `EXPLICIT` means the caller or an authoritative
manifest must identify one exact path/ID. `MANIFEST` means expand only entries
declared by the named current manifest. `FIXED` means the literal path. A missing
blocking fixed/manifest entry is `FAIL`; an absent or ambiguous explicit identity
is `NOT_EVALUATED` and makes coverage partial.

Every profile excludes `.git/**`, `skill-fix-work/**`, vendor/third-party/import/
cache/generated directories, historical superseded reports, templates, examples,
and build outputs not named by the selected candidate. Globs are discovery aids,
not evidence-selection policies.

Unless a row says otherwise, every `BLOCKING` check has
`coverage_required: true` and every `ADVISORY` check has
`coverage_required: false`. The common director checks use their mode-dependent
coverage rule from `evaluation-contract.md`.

Each profile uses the deterministic contract in `evaluation-contract.md`. The
budgets below are hard ceilings, not targets. Context bytes count full-content and
structured extracts returned to the model. revision bytes count exact local byte reads
used only for revision tracking. A profile may finish below its ceiling; it may not sample
beyond a ceiling and infer PASS.

## Producer adapter registry

Use only adapters referenced by a selected check.

| Adapter ID | Native record and required state | PASSING | ADVISORY | FAILING | INCOMPLETE |
|---|---|---|---|---|---|
| `PA-DESIGN-REVIEW-1` | Persisted `cgs.review-evidence/v1` wrapping an independent full/lean `$design-review`; exact target path/revision and finding set | `APPROVED` | none | `NEEDS REVISION`, `MAJOR REVISION NEEDED`, `BLOCKED — PRODUCT DECISION REQUIRED`, `PARTIAL REVIEW` | missing/malformed payload, advisory-only/solo, error, unpersisted |
| `PA-CROSS-GDD-1` | Persisted/read-back `cgs.review-evidence/v1` envelope plus exact `cgs.cross-gdd-review/v2` extension; exact artifact rows, producer/ruleset/bundle/manifest revisions, `requested_mode: full`, `effective_scope: full`, complete current MVP manifest, and `coverage_status: COMPLETE` | envelope `verdict: PASS` with no unresolved deterministic blocker | none | `CONCERNS`, `FAIL`; producer `PARTIAL` is not a completed failure result | missing/malformed/unpersisted envelope or payload, `PARTIAL`, incomplete identity/coverage, or unsupported envelope/extension version |
| `PA-ARCH-REVIEW-1` | Persisted architecture-review report; exact current target manifest, all required reviewers complete, mutation guard passed | `PASS` | none | `BLOCKED`, `PARTIAL` | missing/malformed/unpersisted report or null/error verdict |
| `PA-UX-REVIEW-1` | Exact `cgs.review-evidence/v1` envelope plus `cgs.ux-review/v2` extension; exact target/dependency/author-contract/ruleset/bundle revisions, complete denominator and mutation guard. Current producer fixes `gate_evidence_status: NOT_PERSISTED` and `gate_evidence_eligible: false` | none under the current producer contract; no current durable recorder schema is authorized | none | `NEEDS REVISION`, `MAJOR REVISION NEEDED` | `APPROVED` or `PARTIAL` conversation candidate, null/error, NOT_PERSISTED, gate-ineligible, missing/malformed payload, or unsupported envelope/extension version |
| `PA-ART-BIBLE-1` | Complete `AB-1` plus independent external `AD-ART-BIBLE` record matching current artifact revision and independent reviewer | `APPROVE` | none | `CONCERNS`, `REJECT`, DRAFT/PARTIAL final state | missing/malformed/unpersisted record |
| `PA-VERTICAL-SLICE-1` | Explicit persisted `cgs.vertical-slice-evaluation-report/v2`; complete current workflow-contract, plan, prerequisite, hypothesis, attempt/history, scope, source, candidate/build, batch/session/raw/network/velocity, concern/decision, verdict-matrix, set-revision, and report-revision graph | `Workflow Status: COMPLETE`, Evidence/Product/Final all `PROCEED`, `Currentness: CURRENT`, `Persistence: VERIFIED`, `Gate Eligible: YES` | none | current `PIVOT`, `KILL`, or `BLOCKED_PRODUCT_DECISION_REQUIRED` final result | PARTIAL/INCONCLUSIVE/skipped, missing/malformed/unpersisted report, incomplete graph, or unsupported schema version; changed bindings normalize to STALE |
| `PA-SMOKE-1` | Persisted/read-back `cgs-smoke-check-receipt/v2`; sprint mode, exact workflow contract, run manifest, candidate/build/artifact/source, authority-index, effective QA-plan, selected-scope, runner, test, evidence-member, platform/configuration/device, and receipt revisions | `Observed Verdict: PASS`, `Persistence: VERIFIED`, `Handoff Eligible: YES`, complete current scope, no unresolved warning | none | `FAIL` | `INCOMPLETE`, quick `TARGETED CHECK PASSED`, warning-bearing result, missing/malformed/unpersisted receipt, or unsupported schema version |
| `PA-TEAM-QA-1` | Exact persisted/read-back `cgs.team-qa-signoff/v2` for current candidate/build/artifact, frozen evidence index, authorities, scope/denominator, result rows, findings/dispositions, review receipt, and report revision; paired axes use current vocabulary | `Workflow State: WORKFLOW_COMPLETED`, `QA Verdict: QA_APPROVED`, `Persistence: VERIFIED`, `Gate Eligible: YES` | none | `QA_NOT_APPROVED`, `QA_APPROVED_WITH_CONDITIONS` | `QA_INCOMPLETE`, non-completed workflow, unverified persistence, gate-ineligible, missing/malformed signoff, or unsupported schema version |
| `PA-PLAYTEST-1` | Canonical `cgs.playtest-report/v2` at `production/playtests/<session-id>/report.md` plus separate `cgs.playtest-report-recorder-receipt/v1`; reconstruct the candidate `cgs.review-evidence/v1` record ID and verify exact report, session/protocol/build/bundle/dependency, recorder, target, persisted-file, read-back, and separation revisions | `RECORDED COMPLETED — GATE ELIGIBLE`; unique canonical completed session ID | none | current conclusive failed gate predicate supplied by the selected check | FINALIZATION READY/REQUIRES RECORDER candidate alone, missing recorder, malformed/duplicate/ingest/template/legacy/partial report, dependency mismatch, or unsupported report/receipt version |
| `PA-REGRESSION-1` | Current selection manifest plus runner/CI receipt bound to exact selection revision/build; current QA/source/test/sensitivity/quarantine state | every required active stable test conclusively passes | none | any current required test fails | awaiting run, missing sensitivity, indeterminate, partial, stale |
| `PA-TEST-EVIDENCE-1` | Persisted/read-back `cgs-test-evidence-review-report/v2`; exact workflow contract, review/scope, stage/session/sprint, QA-plan, candidate/build/artifact/source, evidence-registry, input-set, finding-set, and report revisions | `Workflow Status: COMPLETE`, Structural `ADEQUATE`, Admissibility `ADMISSIBLE`, Execution `PASS/CURRENT/COMPLETE`, required scope `FULL`, `Closure Eligible: YES`, `Persistence: WRITTEN`, and one unique eligible current row per required stable AC/check | none | any required row with a conclusive FAIL or closure-ineligible final state caused by a conclusive failure | NOT_RUN/UNKNOWN/STALE/partial axes, missing row/binding, missing/malformed/unpersisted report, or unsupported schema version |
| `PA-PERFORMANCE-1` | Exact `cgs.review-evidence/v1` analyzer record with `artifact_kind: performance-runtime-report`, `coverage: COMPLETE`, and `gate_evidence_candidate: true`, bound to canonical `cgs.performance-report/v1`, producer `perf-profile@cgs.perf-profile/v2`, exact `cgs.performance-budget/v2`, and separate `cgs.performance-report-recorder-receipt/v1`. revalidate the candidate reference ID and record ID; verify exact request/source/build/platform/hardware/scenario/capture/profiler/exporter/adapter/registry/policy/budget/input/trace/baseline rows and revisions, canonical create-only report/receipt paths, independent identities, `write_result: CREATED`, matching returned/persisted/read-back bytes, and `read_back: VERIFIED`. Analyzer fields remain `persistence: NONE` and `recorder_receipt: NONE` | unchanged analyzer and receipt verdict `WITHIN BUDGET`; candidate and receipt target flags true; receipt `evidence_persistence: RECORDED`, `performance_targets_met: true`, `gate_evidence_eligible: true`; full current matrix | none | valid gate-eligible receipt preserving `CONCERNS` or `OVER BUDGET` and `performance_targets_met: false` | candidate alone even when WITHIN BUDGET, missing/invalid receipt, self-recording, wrong path/prior state/atomic conflict check/read-back/bytes/identity, static/plan-only, partial/error/measurement-required, incomplete matrix, missing/malformed payload, or unsupported envelope/payload/budget/receipt version; changed bindings normalize to STALE |
| `PA-RELEASE-COLLECTOR-1` | Exact persisted release-checklist report bound to current release manifest/policy/candidate/build/item evidence; `Gate Decision: NOT EVALUATED` | every HARD item PASS or authorized policy N/A | unresolved advisory items are evaluated by separate advisory check | any HARD FAIL, UNKNOWN, STALE, UNAVAILABLE, invalid N/A, partial, or revision mismatch | missing/malformed/unpersisted collector |
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

For every adapter, missing required identity fields are `UNBOUND` and any current
path/revision/scope/build mismatch is `STALE`, regardless of the native verdict.
Adapter tables do not authorize persistence or creation of missing records.

The schema names and versions above are allowlists, not examples. If a producer
emits `cgs.review-evidence/v1`, require that exact envelope and its listed current
extension or payload schema together. If a producer emits a native durable v2
record, require that native schema and every listed companion receipt. Never
synthesize an envelope, recorder receipt, persistence state, renamed status, or
legacy adapter fallback. A missing or unknown envelope, extension, payload,
native-record, budget, or recorder-receipt version is `INCOMPLETE` (or `UNBOUND`
when required identity is absent) and cannot satisfy a blocking check.

---

## Profile `gate.concept-to-systems-design/v2`

### Identity and budgets

- Transition: `concept-to-systems-design`
- Authority origin/candidate: `Concept` -> `Systems Design`
- Budgets: 32 manifest entries; 8 full-content files; 1 MiB context bytes;
  128 MiB revision bytes; 48 tool actions; 180 seconds elapsed.

### Scope manifest

| Input | Discovery | Read mode |
|---|---|---|
| `design/gdd/game-concept.md` | FIXED | FULL_CONTENT |
| `design/gdd/game-pillars.md` | FIXED, optional when concept embeds pillars | FULL_CONTENT |
| concept owner attestation | EXPLICIT, created/validated in conversation | EXTERNAL_RECEIPT |
| concept prototype report | EXPLICIT from concept provenance, optional | STRUCTURED_EXTRACT |

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `CSD-A01` | BLOCKING | DETERMINISTIC | Current `game-concept.md` exists, is non-placeholder, and its exact revision is in scope. |
| `CSD-Q01` | BLOCKING | DETERMINISTIC | Concept has substantive identity/player promise, core loop, audience, pillars with tests/anti-pillars, MVP scope/risks, and no unresolved contradiction or placeholder. This is the concept profile; never call the system-GDD-only `$design-review` adapter. |
| `CSD-Q02` | BLOCKING | DETERMINISTIC | Visual Identity Anchor has a one-line visual rule and at least two supporting principles bound to a recorded decision. |
| `CSD-M01` | BLOCKING | ATTESTATION | `evidence_source: ATTESTATION_ALLOWED`; owner explicitly confirms the exact current concept revision and recorded decisions are the concept baseline for systems decomposition. Question version `CSD-M01/v1`; expires on concept/scope revision change. |
| `CSD-R01` | ADVISORY | DETERMINISTIC | If an explicitly referenced, revision-bound concept-prototype report exists, surface any current non-PROCEED risk. Absence is advisory, not blocking. |

---

## Profile `gate.systems-design-to-technical-setup/v2`

### Identity and budgets

- Transition: `systems-design-to-technical-setup`
- Authority origin/candidate: `Systems Design` -> `Technical Setup`
- Budgets: 256 manifest entries; 64 full-content files; 6 MiB context bytes;
  1 GiB revision bytes; 128 tool actions; 360 seconds elapsed.

### Scope manifest

| Input | Discovery | Read mode |
|---|---|---|
| `design/gdd/systems-index.md` | FIXED | FULL_CONTENT |
| every MVP system GDD | MANIFEST: exact MVP entries in systems-index | FULL_CONTENT |
| individual GDD review records | EXPLICIT IDs/paths declared for each MVP GDD | STRUCTURED_EXTRACT |
| one cross-GDD report | EXPLICIT report ID/path whose manifest is the complete current MVP set | STRUCTURED_EXTRACT |

Do not scan every Markdown file under `design/gdd/`. The systems index owns the MVP
set. An unresolvable, duplicated, or path-ambiguous MVP entry is incomplete scope.

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `SDT-A01` | BLOCKING | DETERMINISTIC | Systems index exists, is substantive, enumerates a unique canonical path for every MVP system, and defines priority tiers. |
| `SDT-A02` | BLOCKING | DETERMINISTIC | Every enumerated MVP GDD exists and is substantive; no undeclared inferred substitute is admitted. |
| `SDT-E01` | BLOCKING | PRODUCER_RECORD | Every MVP GDD has current `PA-DESIGN-REVIEW-1` PASSING evidence for its exact revision. |
| `SDT-E02` | BLOCKING | PRODUCER_RECORD | One `PA-CROSS-GDD-1` record is current, covers the complete MVP set, and is PASSING. `CONCERNS` does not satisfy this required approval profile. |
| `SDT-Q01` | BLOCKING | DETERMINISTIC | Systems-index dependencies are bidirectionally consistent with the current GDD set and contain no broken/stale reference. |
| `SDT-Q02` | BLOCKING | DETERMINISTIC | All deterministic cross-GDD blocker IDs are resolved in current evidence; conversational acceptance is not resolution. |

---

## Profile `gate.technical-setup-to-pre-production/v2`

### Identity and budgets

- Transition: `technical-setup-to-pre-production`
- Authority origin/candidate: `Technical Setup` -> `Pre-Production`
- Budgets: 384 manifest entries; 80 full-content files; 8 MiB context bytes;
  2 GiB revision bytes; 168 tool actions; 480 seconds elapsed.

### Scope manifest

Use fixed `AGENTS.md`, `.codex/docs/technical-preferences.md`,
`design/art/art-bible.md`, `design/accessibility-requirements.md`,
`design/ux/interaction-patterns.md`, `docs/architecture/architecture.md`, and
`docs/architecture/requirements-traceability.md`. Admit ADRs only from the current
architecture/traceability manifest, engine references only for the configured
pinned engine, test roots plus one exact canary test declared by test setup, and
the configured CI test workflow. Admit one explicit current architecture-review
record. Do not recursively read all tests, engine docs, or ADR-like Markdown.

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `TSP-A01` | BLOCKING | DETERMINISTIC | Engine/language/version/build and asset pipeline are selected; no `[CHOOSE]` placeholder remains, and technical preferences define naming plus versioned performance budgets. |
| `TSP-A02` | BLOCKING | DETERMINISTIC | Art Bible has at least foundation Sections 1–4; accessibility tier and interaction-pattern library are explicit and substantive. |
| `TSP-A03` | BLOCKING | DETERMINISTIC | Master architecture, traceability index, and at least three Foundation ADRs for scene management, event architecture, and save/load are present in the authoritative architecture manifest. |
| `TSP-E01` | BLOCKING | PRODUCER_RECORD | `PA-ARCH-REVIEW-1` is current and PASSING for architecture, traceability, in-scope ADRs, owner-approved requirements, engine constraints, and required test evidence. |
| `TSP-Q01` | BLOCKING | DETERMINISTIC | No ADR dependency cycle; all in-scope ADRs share the pinned engine version, contain Engine Compatibility and GDD Requirements Addressed, and do not use cataloged deprecated APIs. |
| `TSP-Q02` | BLOCKING | DETERMINISTIC | Traceability has zero Foundation gaps and every HIGH RISK engine domain is addressed or represented as an explicit blocking open question. |
| `TSP-A04` | BLOCKING | DETERMINISTIC | Engine reference VERSION exists; unit/integration roots, exact canary test, and configured CI workflow exist and are non-placeholder. |
| `TSP-Q03` | BLOCKING | DETERMINISTIC | Execute the exact declared canary through the configured runner and require a current conclusive pass receipt; source presence or exit code alone is insufficient. |
| `TSP-R01` | ADVISORY | DETERMINISTIC | At least one current key-screen UX specification has begun; absence is surfaced as an advisory risk. |

---

## Profile `gate.pre-production-to-production/v2`

### Identity and budgets

- Transition: `pre-production-to-production`
- Authority origin/candidate: `Pre-Production` -> `Production`
- Budgets: 512 manifest entries; 96 full-content files; 10 MiB context bytes;
  8 GiB revision bytes; 220 tool actions; 600 seconds elapsed.

### Scope manifest

The caller must explicitly identify one vertical-slice evaluation report. Expand
only its complete referenced plan/candidate/source/build/scope/evidence/playtest/
velocity/decision graph. Add the current systems-index MVP set, architecture and
traceability manifests, art-bible record, control manifest, one explicit first
sprint plan, epics/story paths named by that plan, and key-screen UX specs plus
their review records. Never locate a vertical slice, sprint, or review by mtime.

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `PPP-E01` | BLOCKING | PRODUCER_RECORD | `PA-VERTICAL-SLICE-1` is current and PASSING for the exact supplied report/build graph. |
| `PPP-A01` | BLOCKING | DETERMINISTIC | First sprint, control manifest, Foundation/Core epics, and referenced story paths exist and bind current GDD requirement IDs plus Accepted ADRs. |
| `PPP-A02` | BLOCKING | DETERMINISTIC | All MVP GDDs are complete; architecture has no unresolved Foundation/Core question; all Foundation/Core ADRs are Accepted and current. |
| `PPP-E02` | BLOCKING | PRODUCER_RECORD | Complete Art Bible has current `PA-ART-BIBLE-1` PASSING evidence; internal self-signoff is rejected. |
| `PPP-A03` | BLOCKING | DETERMINISTIC | Exact build named by vertical-slice evidence exists and matches candidate/source/platform/configuration identity. |
| `PPP-E03` | BLOCKING | PRODUCER_RECORD | Main menu, core gameplay HUD when applicable, and pause-menu specs each have current `PA-UX-REVIEW-1` PASSING evidence. |
| `PPP-Q01` | BLOCKING | DETERMINISTIC | UX specs cover MVP UI requirements, committed accessibility tier, and referenced interaction patterns. |
| `PPP-M01` | BLOCKING | ATTESTATION | `evidence_source: ATTESTATION_ALLOWED`; an accountable playtest owner confirms a human completed the exact build's start→challenge→resolution loop without developer guidance and the central interaction felt acceptable for production. Question version `PPP-M01/v1`; bind build/report/scope revisions and expire on any change. |
| `PPP-R01` | ADVISORY | PRODUCER_RECORD | At least one distinct `PA-PLAYTEST-1` session exists for the exact slice build. Absence is CONCERNS, not a substitute for `PPP-M01` or vertical-slice evidence. |

---

## Profile `gate.production-to-polish/v2`

### Identity and budgets

- Transition: `production-to-polish`
- Authority origin/candidate: `Production` -> `Polish`
- Budgets: 1024 manifest entries; 128 full-content files; 12 MiB context bytes;
  16 GiB revision bytes; 260 tool actions; 720 seconds elapsed.

### Scope manifest

Require one explicit current production/milestone scope manifest and candidate
build. Expand only its GDD requirement IDs, story paths, implementation paths,
test IDs, QA plan, regression selection/receipt, smoke receipt, team-QA report,
bug-registry snapshot, performance report/budget, playtest session IDs, UX paths,
and accessibility evidence. Do not recursively compare all `design/gdd/`, `src/`,
assets, or tests. A missing scope manifest is incomplete coverage, not permission
to scan the repository.

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `PTP-A01` | BLOCKING | DETERMINISTIC | Scope manifest is current/complete; every core mechanic requirement maps to current implementation and story evidence; candidate's main gameplay path is end-to-end playable. |
| `PTP-A02` | BLOCKING | DETERMINISTIC | Current QA plan covers the production scope and every required Logic/Integration story maps to declared test IDs/source. |
| `PTP-E01` | BLOCKING | PRODUCER_RECORD | `PA-REGRESSION-1` is current and PASSING for the exact candidate build. |
| `PTP-E02` | BLOCKING | PRODUCER_RECORD | `PA-SMOKE-1` is current and PASSING. `PASS WITH WARNINGS`, targeted/quick, or mere report existence is ineligible. |
| `PTP-E03` | BLOCKING | PRODUCER_RECORD | `PA-TEAM-QA-1` is current and PASSING. `APPROVED_WITH_CONDITIONS` is not gate eligible. |
| `PTP-E04` | BLOCKING | PRODUCER_RECORD | Three distinct current `PA-PLAYTEST-1` sessions cover new-player experience, mid-game systems, and difficulty curve for the candidate/build family. |
| `PTP-Q01` | BLOCKING | DETERMINISTIC | Current bug registry has no unresolved blocker/critical finding for the scope; every critical fun finding is resolved by current evidence. |
| `PTP-E05` | BLOCKING | PRODUCER_RECORD | `PA-PERFORMANCE-1` is current and PASSING for every required platform/scenario matrix row. |
| `PTP-Q02` | BLOCKING | DETERMINISTIC | Fun hypothesis is explicitly validated or revised; no recorded confusion loop above the approved threshold remains; difficulty evidence matches the current design target when applicable. |
| `PTP-Q03` | BLOCKING | DETERMINISTIC | Every implemented in-scope screen maps to a current UX spec/pattern and current accessibility verification for the committed tier. |

---

## Profile `gate.polish-to-release/v2`

### Identity and budgets

- Transition: `polish-to-release`
- Authority origin/candidate: `Polish` -> `Release`
- Budgets: 2048 manifest entries; 160 full-content files; 16 MiB context bytes;
  32 GiB revision bytes; 340 tool actions; 900 seconds elapsed.

### Scope manifest

Require explicit current release manifest, release policy, build-candidate
manifest, candidate/build IDs and revisions, platform/locale matrix, and exact
release-checklist collector report. Expand only records referenced by those
manifests: milestone/content inventory, QA plan/team-QA, smoke, regression/test
evidence, performance, bugs, localization, accessibility, legal/privacy/rating/
certification receipts, balance review, package receipts, store metadata,
changelog, and patch-note draft. Never scan all source/content or select newest
receipts.

### Checks

| Check ID | Class | Source | Predicate |
|---|---|---|---|
| `PTR-A01` | BLOCKING | DETERMINISTIC | Release/policy/candidate manifests are current, mutually bound, and enumerate the complete required feature/content/platform/locale scope. |
| `PTR-E01` | BLOCKING | PRODUCER_RECORD | `PA-RELEASE-COLLECTOR-1` has every HARD item passing/authorized N/A for the exact candidate; UNKNOWN or invalid N/A is not pass. |
| `PTR-R01` | ADVISORY | PRODUCER_RECORD | From the same validated `PA-RELEASE-COLLECTOR-1` record, emit every unresolved advisory-class item as a named concern after all hard items pass. |
| `PTR-E02` | BLOCKING | PRODUCER_RECORD | `PA-TEAM-QA-1` is current and PASSING for the exact release candidate/build. |
| `PTR-E03` | BLOCKING | PRODUCER_RECORD | `PA-SMOKE-1` and `PA-REGRESSION-1` are current and PASSING with full release scope. |
| `PTR-E04` | BLOCKING | PRODUCER_RECORD | `PA-TEST-EVIDENCE-1` is current and PASSING: all Must Have requirement/test rows have conclusive build-bound evidence and no required row is missing/unknown. |
| `PTR-E05` | BLOCKING | PRODUCER_RECORD | `PA-PERFORMANCE-1` is current and PASSING across every required target platform. |
| `PTR-Q01` | BLOCKING | DETERMINISTIC | Current bug registry contains no unresolved policy-blocking severity; any disposition/waiver is validated only under the release policy's exact authority. |
| `PTR-E06` | BLOCKING | PRODUCER_RECORD | `PA-LOCALIZATION-1` is current and PASSING for every required target locale. |
| `PTR-Q02` | BLOCKING | DETERMINISTIC | Accessibility, legal/privacy/ratings/certification, clean package, store metadata, changelog/patch-note, and required balance-review evidence are present, current, and satisfy release policy. |

## Completion rule

Evaluate every row in the selected profile. No profile is complete if a listed
check is omitted, a required manifest branch is sampled, an adapter record is
selected by recency, an applicability predicate is assumed, or budget accounting
is absent. Record exact skipped scope and use the decision table; never invent an
equivalent artifact or silently downgrade a blocking row.
