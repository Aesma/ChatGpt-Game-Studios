# Skill Spec: $team-ui

> **Category**: team
> **Priority**: medium
> **Spec written**: 2026-07-23

## Skill summary

`$team-ui` consumes one bounded `cgs.team-ui-request/v2` manifest. It authors and independently reviews one current_revision UX specification, creates separately owned visual/asset/engine support, freezes a separately authorized implementation manifest, permits one UI writer, captures real runtime evidence through a distinct runner, and requires four independent final review streams on the same post-fix build/source-set revision. The workflow contains controlled writes; reviewers are always read-only.

This specification is an executable-behavior contract, not evidence that a test was run.

## Static assertions

- [ ] **TUI-S001** — YAML frontmatter contains only `name` and non-empty `description`; `name` is `team-ui`.
- [ ] **TUI-S002** — No-argument validation precedes every project read, delegate, write, result, and verdict.
- [ ] **TUI-S003** — Invocation accepts only `--manifest` and optional `--resume`, rejecting unknown/duplicate/missing/positional input.
- [ ] **TUI-S004** — The request schema is exactly `cgs.team-ui-request/v2` and canonical IDs/paths are deterministic.
- [ ] **TUI-S005** — The only delegation interface is `cgs.team-ui-task/v2`; `$ux-design`, `$ux-review`, and interface fallback are forbidden.
- [ ] **TUI-S006** — `consultation_mode` defaults to `lean`; `review_mode` is invalid; modes never reduce mandatory gates.
- [ ] **TUI-S007** — `solo` cannot start production implementation or return `COMPLETE`.
- [ ] **TUI-S008** — `COMPLETE` maps only from `IMPLEMENTATION_VERIFIED`; all other pipeline results have deterministic `PARTIAL` or `BLOCKED` verdicts.
- [ ] **TUI-S009** — Accepted risk cannot change UX verdict, authorize production support/implementation, or return `COMPLETE`.
- [ ] **TUI-S010** — UX revisions and implementation fix rounds are each capped at two and preserve stable finding IDs.
- [ ] **TUI-S011** — Every write path has one owner; every reviewer is read-only; no role can spawn children.
- [ ] **TUI-S012** — UI programmer cannot write UX, visual/asset/engine, ADR, global-pattern, game-state, or unlisted paths.
- [ ] **TUI-S013** — Global pattern, visual/art-bible, and cross-screen architecture changes route to their external UX-library, art-bible, or architecture owner.
- [ ] **TUI-S014** — Design, design-support, and implementation boundaries cannot pre-authorize unknown later paths.
- [ ] **TUI-S015** — Every operation binds type, canonical path, expected base/absence, owner, candidate/diff revision, and byte cap.
- [ ] **TUI-S016** — UX, visual spec, asset manifest, engine plan, implementation manifest, checkpoints, reviews, evidence, and result have canonical paths.
- [ ] **TUI-S017** — `UNCONFIGURED` engine permits approved UX or a separately authorized engine-neutral nonproduction proposal only.
- [ ] **TUI-S018** — Production requires exact configured engine/version and current engine plan; no generic UI implementation is invented.
- [ ] **TUI-S019** — Visual spec and asset manifest are persisted, revision-bound, and owned by the art author; engine plan has a separate owner.
- [ ] **TUI-S020** — UX reviewer differs from UX author, art reviewer differs from art author, and all final reviewers differ from writer, runner, authors, and each other.
- [ ] **TUI-S020A** — The UX author writes only the current `ux-design` `ux-spec` tuple (`ux-profile-schema-v2`, `cgs.ux-content-profile/v2`, `ux-design-author-<revision>`) with exact UXS-01..14 structure; no team-ui-local schema may occupy `design/ux/<screen-id>.md`.
- [ ] **TUI-S020B** — The UX reviewer returns an exact `cgs.review-evidence/v1` envelope plus `cgs.ux-review/v2`; the coordinator persists only an immutable `cgs.team-ui-ux-review-recording/v1` wrapper and never upgrades the embedded NOT_PERSISTED/gate-ineligible fields.
- [ ] **TUI-S020C** — Production support and implementation require a current independent immutable `cgs.art-bible-review/v1` with gate AD-ART-BIBLE and verdict APPROVE binding the exact art-bible target, authoring receipt, AB-1/nine-section, dependency/context revision, and role separation; path/revision or content COMPLETE alone is insufficient.
- [ ] **TUI-S020D** — Every request binds exact current `cgs.localization-manifest/v2` and `cgs.localization-catalog/v2` path/declared revision plus recomputed source-table, keyset, catalog, source-locale, and target-locale identities.
- [ ] **TUI-S020E** — `package_requirement` is explicit; REQUIRED consumes only exact current `cgs.localization-package/v1` rows bound to the same catalog/source/keyset and locale/page, while NOT_REQUIRED requires an empty package set and no package dependency.
- [ ] **TUI-S020F** — Missing, stale, malformed, parser-mismatched, locale-incomplete, or package-incomplete localization inputs fail before checkpoint/task dispatch and remain read-only throughout team-ui.
- [ ] **TUI-S021** — Runtime evidence runner differs from the UI programmer and every reviewer and writes only declared raw evidence paths.
- [ ] **TUI-S022** — Runtime evidence records actual adapter/argv/config, engine/version, final identities, exit/timing, observations, and raw log revisions.
- [ ] **TUI-S023** — Plan, mock receipt, file existence, old receipt, reviewer prose, `UNKNOWN`, and `NOT_RUN` cannot satisfy runtime evidence.
- [ ] **TUI-S024** — Evidence matrix covers target input/focus, resolution/aspect/safe-zone, locale/expansion, every text scale/reflow, contrast/non-color/colorblind, motion, audio/events/game-state, frame/main-thread, allocation/lifecycle/leak, and engine rules.
- [ ] **TUI-S025** — Applicable `src/ui/AGENTS.md` constraints are versioned and become mandatory checks.
- [ ] **TUI-S026** — Project context hard caps are 32 files, 524288 total bytes, and 131072 bytes per file; manifest can only lower them.
- [ ] **TUI-S027** — Target cardinalities, implementation/evidence operations, evidence rows, and recorder artifacts have fixed hard caps.
- [ ] **TUI-S028** — Context is exact-path/revision/purpose only; discovery of newest or “all relevant” artifacts and silent truncation are forbidden.
- [ ] **TUI-S029** — A coverage profile is version/revision-bound and covers every target value; absent profile requires full bounded cross product or blocks.
- [ ] **TUI-S030** — At most three tasks are live; attempt cap is 900 seconds, phase cap is 1800 seconds, and one eligible retry is the maximum.
- [ ] **TUI-S031** — Writer retry requires proven pre-attempt project state; runner retry uses new authorized outputs; third attempts are forbidden.
- [ ] **TUI-S032** — Timed-out/cancelled attempt tokens are revoked and every late response is quarantined and gate-ineligible.
- [ ] **TUI-S033** — Unknown cancellation or mutation state produces `PARTIAL`/`BLOCKED`, not a retry or success assumption.
- [ ] **TUI-S034** — Checkpoints are immutable, sequenced, previous-receipt-ID-linked, bounded, atomically/read-back persisted, and written after every state-changing event.
- [ ] **TUI-S035** — Resume verifies checkpoint chain and every dependent identity, preserves counters/findings, and restarts from the earliest safe state.
- [ ] **TUI-S036** — A checkpoint cannot authorize an operation absent from its recorded manifest; stale artifacts stay preserved but ineligible.
- [ ] **TUI-S037** — Final review uses four mandatory streams on one frozen build/source/evidence identity and deterministic two-wave scheduling when concurrency is three.
- [ ] **TUI-S038** — Timeout, malformed output, missing stream, wrong target, late output, or incomplete check coverage yields `PARTIAL` and no quorum.
- [ ] **TUI-S039** — Every implementation fix creates a new build/source/evidence identity and stales all prior final reviews.
- [ ] **TUI-S040** — Re-review after a fix includes all prior open checks plus the complete regression matrix.
- [ ] **TUI-S041** — Mandatory accessibility, nested UI, engine, evidence, and ownership blockers are non-waivable.
- [ ] **TUI-S042** — Unexpected writes halt without silently reverting user work.
- [ ] **TUI-S043** — Skill and spec both describe controlled writes and exact mutation allowlists; neither calls the whole pipeline read-only.
- [ ] **TUI-S044** — Final result records revisions, authorization, attempts/cancellations/quarantine, findings, mutations, build/evidence/reviews, and persistence.
- [ ] **TUI-S045** — Final output emits exactly one state-derived next action and does not auto-invoke another workflow.
- [ ] **TUI-S046** — Metadata describes bounded-UX-to-independently-verified-UI behavior and names the v2 request manifest.
- [ ] **TUI-S047** — Both relative reference links resolve inside the candidate skill package.
- [ ] **TUI-S048** — P1 closure matrix contains exactly `TUI-007` through `TUI-017`, once each.

## Director and mode gates

- `full`: optional, read-only director consultation may supplement decisions but never counts as evidence.
- `lean`: default; omits optional consultations and keeps every mandatory role and gate.
- `solo`: permits scratch/nonproduction proposal work only; independence and production completion are impossible.
- The mandatory final streams are UX conformance, art consistency, accessibility, and engine UI/QA-evidence validation for every production run.

## Behavioral cases

### Case 1 — Verified final build happy path

**Fixture:** Valid bounded v2 request; configured engine; current instructions and owner sources; independently approved UX; separately authorized support artifacts and implementation manifest; one writer; one distinct evidence runner; all four distinct review streams pass the same final build/source/evidence identities.

**Expected:** Every phase persists a current checkpoint, mutations remain inside the active manifest, evidence is actual execution evidence, and the result is `Pipeline Result: IMPLEMENTATION_VERIFIED` plus `Verdict: COMPLETE`.

**Assertions:** TUI-S008, S011-S025, S034-S045.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 2 — No argument exits before project access

**Fixture:** Invoke `$team-ui` without flags in any project state.

**Expected:** Print exact usage and stop. No project file is read, no role starts, no write occurs, and no pipeline result/verdict is emitted.

**Assertions:** TUI-S002, TUI-S003.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 3 — Canonical direct-task interface has no fallback

**Fixture:** Valid manifest, but the UX reviewer role is unavailable.

**Expected:** Coordinator issues only typed v2 direct-task packets. It does not invoke `$ux-review`, `$ux-design`, or switch to an ad-hoc same-agent review. Result is `PARTIAL` with the unavailable role as the sole next action.

**Assertions:** TUI-S005, TUI-S020, TUI-S038.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 4 — Consultation mode cannot change review quorum

**Fixture:** Run once with omitted mode, once with `full`, once with `lean`, once with `solo`, and once with invalid `review_mode`.

**Expected:** Omitted resolves to `lean`; `full` adds advisory work only; `lean` keeps all four streams; `solo` cannot enter production; `review_mode` is rejected during request validation.

**Assertions:** TUI-S006, TUI-S007, TUI-S037.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 5 — NEEDS REVISION and accepted risk cannot reach production

**Fixture:** Current UX review contains gamepad and contrast blockers; user accepts named risk.

**Expected:** Review bytes/verdict remain unchanged. Pipeline result is `ACCEPTED_RISK_SPEC_NOT_APPROVED`, verdict is `BLOCKED`, and production support/implementation does not start. A nonproduction proposal needs its own manifest.

**Assertions:** TUI-S008-S010.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 6 — UX convergence stops after two revisions

**Fixture:** One stable `UXF-NAVIGATION` blocker remains after author revision rounds 1 and 2.

**Expected:** Same finding ID and before/after diff evidence are preserved; full regression runs on each new revision; no third revision occurs; stop for one user decision.

**Assertions:** TUI-S010, TUI-S020, TUI-S035.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 7 — Programmer global-pattern mutation is refused

**Fixture:** Implementation needs a reusable cross-screen interaction and tries to update the global pattern library.

**Expected:** Programmer operation is outside its manifest and is refused/detected. A stable feature-local proposal may be owned by UX author, while cross-screen production blocks for external UX-library/ADR owner. No user change is reverted.

**Assertions:** TUI-S012, TUI-S013, TUI-S041, TUI-S042.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 8 — Later writes require later authorization

**Fixture:** UX candidate exists, but visual/engine/source/evidence operations have not been planned.

**Expected:** Design authorization cannot cover unknown support or implementation paths. Candidate bytes and exact operations precede design-support authorization; a persisted exact implementation manifest precedes implementation authorization and writer dispatch.

**Assertions:** TUI-S014-S016.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 9 — Unconfigured engine blocks production, not UX

**Fixture:** Valid design context with `engine.status: UNCONFIGURED`.

**Expected:** UX may reach current `SPEC_APPROVED`. At most a separately authorized engine-neutral nonproduction proposal is legal. No production engine plan, UI programmer, build claim, or `COMPLETE` occurs.

**Assertions:** TUI-S017, TUI-S018.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 10 — Visual, asset, and engine outputs are versioned and owned

**Fixture:** Approved UX with configured engine and separately authorized support paths.

**Expected:** Art author alone writes canonical visual spec/asset manifest; engine-plan author alone writes canonical engine plan; all bind source revision, requirements, targets, and owner-specific content. Reviewer tasks are distinct and read-only.

**Assertions:** TUI-S016, TUI-S019, TUI-S020.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 11 — Self-review cannot satisfy independence

**Fixture:** Same execution identity is assigned UX author and reviewer, or UI programmer and engine/QA reviewer.

**Expected:** Identity validation blocks dispatch or marks returned evidence ineligible. No mode, small team, or user risk acceptance waives this gate.

**Assertions:** TUI-S020, TUI-S021, TUI-S037, TUI-S041.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 12 — Reviewer prose is not runtime evidence

**Fixture:** Reviewers say keyboard, scaling, and performance pass, but no verified runner receipts or raw logs exist.

**Expected:** Rows are missing/`NOT_RUN`; result is `PARTIAL`, no quorum and no completion. Reviewer cannot create runtime observations.

**Assertions:** TUI-S021-S024, TUI-S038.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 13 — Nested UI rules require build-bound rows

**Fixture:** Basic navigation passes, but one committed text scale lacks reflow/no-clipping evidence and the main/game-thread profile is absent.

**Expected:** Both are blocking missing rows bound to the current build. Result cannot be `COMPLETE`; exact check IDs, owners, and next action are reported.

**Assertions:** TUI-S024, TUI-S025, TUI-S041.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 14 — Context and matrix hard caps fail closed

**Fixture:** Manifest requests 33 files, 524289 bytes, an oversize single file, an unbounded “all relevant GDDs” search, or target cardinality above a hard maximum.

**Expected:** Reject before delegation. No silent truncation, sampling, discovery, or user-supplied higher cap is accepted. Report bounded identities/byte counts only.

**Assertions:** TUI-S026-S029.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 15 — Timeout, retry, cancellation, and late output

**Fixture:** One mandatory reviewer exceeds its deadline, ignores cancellation, and returns after a same_revision narrowed retry has started.

**Expected:** First token is revoked; its output is quarantined and never parsed or counted; at most one eligible retry occurs; phase cap still applies. Missing eligible quorum returns `PARTIAL`.

**Assertions:** TUI-S030-S033, TUI-S038.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 16 — Writer timeout with uncertain mutation state is not retried

**Fixture:** UI writer times out after possibly changing one declared path; terminal mutation state cannot be proven.

**Expected:** Revoke token, reconcile paths, checkpoint `UNKNOWN`, and stop `PARTIAL: MUTATION_STATE_UNKNOWN`. No automatic retry and no success inference.

**Assertions:** TUI-S031-S035, TUI-S042.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 17 — Resume invalidates stale descendants

**Fixture:** Resume from a valid checkpoint after the visual spec revision changes; all UX inputs remain unchanged.

**Expected:** Verify the full chain, preserve counters/findings, retain stale history, invalidate implementation/build/evidence/reviews, and restart no later than support-candidate validation. Prior authorization cannot bless a changed base.

**Assertions:** TUI-S034-S036.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 18 — Cross-screen technical choice requires current owner decision

**Fixture:** Engine plan introduces a navigation/data-binding framework used by multiple screens, but no current Accepted ADR exists.

**Expected:** Team-ui reports the proposal and named architecture owner, does not write an ADR, blocks production implementation, and emits that one owner decision as next action.

**Assertions:** TUI-S013, TUI-S018, TUI-S041, TUI-S045.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 19 — Post-fix reviews bind only the final revision

**Fixture:** Build B1 has a blocking accessibility finding. Sole UI writer applies authorized fix round 1 and evidence runner produces B2.

**Expected:** Every B1 row/review becomes stale; B2 runs the prior open check plus full regression matrix; only four complete B2 streams and zero blockers can verify implementation.

**Assertions:** TUI-S037-S041.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 20 — Controlled-write contract and mutation breach

**Fixture:** Authorized UX/support/source/recorder writes occur, and an unrelated path changes during one writer attempt.

**Expected:** Skill/spec identify controlled writes and role allowlists. The unrelated mutation causes `BLOCKED: MUTATION_BREACH`; it is reported and not silently reverted. No later role legalizes it.

**Assertions:** TUI-S011-S015, TUI-S042, TUI-S043.

**Case Verdict:** PASS / FAIL / PARTIAL

### Case 21 — Localization manifest, catalog, and conditional packages are current

**Fixture:** The positive request binds a current `cgs.localization-manifest/v2`,
its exact `cgs.localization-catalog/v2` source-table bytes, recomputable source-
table/keyset/catalog identity, target-locale coverage, and all implementation-
required `cgs.localization-package/v1` locale/page rows. Negative variants change
one catalog revision, parser version, keyset revision, locale entry, package ID,
and payload revision. Each package uses a producer-assigned stable package ID; no
field is derived from payload bytes. Every negative variant stops
`BLOCKED: LOCALIZATION_INPUT_NOT_CURRENT` before the first checkpoint or task;
team-ui writes no localization artifact and never substitutes a nearby/latest
manifest, catalog, or package.

**Assertions:** TUI-S020D-S020F, TUI-S024, TUI-S028, TUI-S041.

**Case Verdict:** PASS / FAIL / PARTIAL

## P1 closure matrix

The audit’s authoritative P1 set contains exactly 11 items:

| Audit ID | Closure contract | Primary assertions/cases |
|---|---|---|
| `TUI-007` | No-argument and malformed invocation stop before project access or side effects. | S002-S004; Case 2 |
| `TUI-008` | One typed direct-task interface is mandatory; no subskill/ad-hoc fallback exists. | S005; Case 3 |
| `TUI-009` | Default lean/full/solo consultation semantics are explicit; mandatory quorum never varies. | S006-S007, S037; Case 4 |
| `TUI-010` | Unconfigured engine permits spec/nonproduction work only and blocks production implementation. | S017-S018; Case 9 |
| `TUI-011` | Visual spec, asset manifest, and engine plan have canonical persisted paths, revisions, and unique owners. | S016, S019; Case 10 |
| `TUI-012` | Reviewer identities are distinct from relevant authors/writer/runner and are read-only. | S011, S020-S021, S037; Case 11 |
| `TUI-013` | A distinct runner produces real build-bound receipts; reviewer prose and missing/NOT_RUN rows are ineligible. | S021-S024; Cases 12-13 |
| `TUI-014` | Scalable-text/reflow, localization identities, and game/main-thread constraints are mandatory current-build evidence. | S020D-S020F, S024-S025, S041; Cases 13 and 21 |
| `TUI-015` | Exact context/purpose/revisions and hard file/byte/cardinality/coverage bounds replace open-ended discovery. | S026-S029; Case 14 |
| `TUI-016` | Hard deadlines, concurrency, attempt limits, revocation/quarantine, immutable checkpoints, and revision-invalidating resume are deterministic. | S030-S036, S038; Cases 15-17 |
| `TUI-017` | Cross-screen engine/interaction/visual architecture is owned by external UX-library, art-bible, or architecture authorities and requires current accepted evidence. | S013, S018, S041, S045; Case 18 |

## P0 preservation checks

- `TUI-001`: accepted risk never upgrades `NEEDS_REVISION` or reaches production/complete (Case 5).
- `TUI-002`: stable UXF findings and two-revision convergence cap (Case 6).
- `TUI-003`: UI programmer cannot write the global interaction-pattern source (Case 7).
- `TUI-004`: every post-fix review is stale and full revalidation binds the new final revision (Case 19).
- `TUI-005`: later exact support/implementation boundaries require later authorization (Case 8).
- `TUI-006`: skill and spec agree the workflow has controlled writes, with role-specific allowlists (Case 20).

## Protocol compliance

- [ ] Exact request, context, instruction, target, owner, and artifact revision govern every transition.
- [ ] User authorization applies only to the complete enumerated boundary currently presented.
- [ ] No role can broaden scope, share ownership, self-review, spawn children, or substitute narrative for evidence.
- [ ] Timeout, cancellation, retry, mutation reconciliation, persistence, and resume are fail-closed.
- [ ] Mandatory evidence and accessibility/engine/nested constraints are non-waivable.
- [ ] Final `COMPLETE` is bound to one current post-fix implementation manifest, build, source set, evidence matrix, and four-stream review set.
- [ ] Result stops with exactly one legal next action and never chains another workflow.

## Coverage notes

Runtime fixtures should exercise byte-exact YAML validation, canonical path and symlink rejection, CREATE/REVISE base identities, every hard bound, instruction precedence, typed-packet validation, role identity collisions, separate authorization manifests, immutable envelope/read-back failure, reviewer and writer deadlines, cancellation without acknowledgement, late results, writer/runner mutation uncertainty, retry-specific evidence paths, checkpoint-chain corruption, each resume invalidation row, engine-unconfigured and missing-ADR branches, exact localization manifest/catalog/package currentness and fail-closed variants, all nested UI evidence rows, two-round convergence, and proof that every non-owned path remains byte-identical.
