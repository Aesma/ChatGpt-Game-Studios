# Skill Test Spec: test-setup

> **Spec ID**: test-setup-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: testing
> **Priority**: high
> **Spec written**: 2026-07-22

## Skill Summary

test-setup audits, scaffolds, verifies, or performs ID-keyed repair of
engine-specific test infrastructure. It binds an owner-approved structured engine
manifest, repository policy, canonical layout manifest, argv-only execution
manifest, reviewed dependency lock, deterministic pass/failure canaries, and
current revision-bound local and CI receipts.

Owned writes are limited to authorized managed test infrastructure, the managed
cgs-tests workflow job, and immutable evidence below
production/qa/evidence/test-setup. Audit is read-only. Instruction files, engine
and repository authorities, project descriptors, shared QA/gate contracts,
unmanaged workflow jobs, and human-authored tests are non-writes.

Workflow statuses are COMPLETE, PARTIAL, BLOCKED, and ERROR. A missing,
unreadable, timed-out, unsupported, stale, unverifiable, or partially covered
required check is never PASS. Gate eligibility requires every verification rung
through CI_VERIFIED for the same current revisions.

---

## Static Assertions

- [ ] **[TSU-SA-001]** Frontmatter contains exactly non-empty name and description,
  and name is test-setup.
- [ ] **[TSU-SA-002]** A normative cgs-test-setup-contract/v1 declares modes,
  authorities, owned outputs, non-writes, receipt schema, and revision format.
- [ ] **[TSU-SA-003]** Audit is read-only and no mode auto-invokes a gate, skill,
  commit, or publication.
- [ ] **[TSU-SA-004]** Existing infrastructure is parsed semantically; path
  existence cannot establish validity.
- [ ] **[TSU-SA-005]** Repair operations are stable-ID keyed, revision-preconditioned,
  diff-bound, backed up, compare-and-set, and preserve unmanaged content.
- [ ] **[TSU-SA-006]** The full root-to-target AGENTS chain is versioned and closest
  applicable rules control every target.
- [ ] **[TSU-SA-007]** Manual evidence routes only to production/qa/evidence and
  never to tests/evidence.
- [ ] **[TSU-SA-008]** One versioned layout manifest owns unit, integration,
  performance, playtest, setup-canary, and evidence-route declarations.
- [ ] **[TSU-SA-008A]** The three downstream manifests expose exactly `cgs-test-layout/v1`, `cgs-test-validator-manifest/v1`, and `cgs-test-execution-manifest/v1` through matching `artifact_type`, integer `manifest_version: 1`, and `schema`; every consumer binding includes canonical path and raw revision.
- [ ] **[TSU-SA-008B]** Legacy producer identities `cgs-test-layout-manifest` and `cgs-test-setup-validator-manifest` are rejected rather than aliased.
- [ ] **[TSU-SA-009]** Structured engine authority agrees with actual descriptor,
  version, language, project root, and module or assembly identity.
- [ ] **[TSU-SA-010]** Repository policy owns trunk/default/PR branches, paths,
  cache, timeout, concurrency, runner labels, and least privilege.
- [ ] **[TSU-SA-011]** CI validation targets the exact cgs-tests job and exact
  manifest-bound argv, not workflow or job-name presence.
- [ ] **[TSU-SA-012]** Verification advances monotonically from audit through
  static, discovery, canary, failure sensitivity, determinism, and trusted CI.
- [ ] **[TSU-SA-013]** Static validators, runners, parsers, manifests, sources,
  logs, and receipts carry exact version and raw revision bindings.
- [ ] **[TSU-SA-014]** Deterministic controls are frozen before execution and pass
  semantic projections must match without post-result retries.
- [ ] **[TSU-SA-015]** Partial, unavailable, timeout, unsupported, stale, or
  invalid evidence forces Gate Eligible NO.
- [ ] **[TSU-SA-016]** Every third-party action has a reviewed source, immutable
  full commit SHA, license/security disposition, and review-receipt revision.
- [ ] **[TSU-SA-017]** COMPLETE requires nonzero discovery, pass, intentional
  conclusive fail, isolated equal post-probe pass, and current trusted CI proof.
- [ ] **[TSU-SA-018]** cgs-test-setup-receipt/v2 binds every authority, manifest,
  dependency, source, tool, execution, log, diff, and freshness result.

---

## Test Cases

### Case 1 [TSU-C01]: Existing paths receive semantic audit and bounded repair

#### Fixture

- The tests tree and tests workflow already exist.
- The execution manifest points at a stale runner revision.
- The managed cgs-tests job omits receipt upload.
- Human jobs and human-authored tests are present.

#### Input

- Mode is audit first, followed by separately authorized repair.
- Exact engine, repository-policy, dependency-lock, and run identities are supplied.

#### Expected reads

- Every managed artifact in full, its schema, references, stable IDs, and declared revision.
- Existing cgs-tests YAML subtree and all unmanaged sibling identities.
- Applicable validators and their pinned versions and revisions.

#### Expected writes

- Audit writes nothing.
- Repair writes only authorized managed fields plus immutable audit, repair-plan,
  preimage backup, exact diff, changed-files, and repair receipt artifacts.

#### Expected non-writes

- Unmanaged workflow jobs, human tests, instruction files, shared QA contracts,
  and unrelated files.

#### Expected behavior

- Path existence never yields VALID.
- Each expected artifact gets a semantic outcome and validator evidence.
- Repair operations carry stable ID, bounded pointer or anchor, base revision,
  before/after value revisions, patch revision, and all-file compare-and-set.
- A preimage mismatch writes no managed target.

#### Assertions

- [ ] Stale runner semantics are reported despite every path existing.
- [ ] Legacy force behaves exactly as bounded repair.
- [ ] Backups are recovery evidence and never overwrite divergent current bytes.
- [ ] Partial audit coverage prevents repair and gate eligibility.

#### Case Verdict

PASS when audit is complete and repair preserves unmanaged bytes with verified
preimage, diff, postimage, and read-back revisions; otherwise PARTIAL, BLOCKED, or
FAIL with Gate Eligible NO.

---

### Case 2 [TSU-C02]: Closest instruction chain controls every target

#### Fixture

- Root AGENTS and a nearer tests AGENTS define different naming details.
- A workflow target and multiple test-source target directories are planned.
- One variant makes a target-parent instruction unreadable.

#### Input

- Audit or scaffold with the complete proposed target list.

#### Expected reads

- The repository-root-to-parent instruction chain for every proposed target.
- Raw bytes and revision of each selected instruction file.

#### Expected writes

- On complete coverage, only the authorized scaffold and evidence.
- On unreadable applicable instructions, no write beneath the affected subtree.

#### Expected non-writes

- All AGENTS files and other instruction authorities.

#### Expected behavior

- Precedence is resolved separately per target and the closest rule wins.
- Effective naming, evidence, isolation, cleanup, and engine rules record their
  source path and revision.
- The current repository naming example is not used as a fallback elsewhere.

#### Assertions

- [ ] Generated names follow the closest tests rule.
- [ ] Selected, loaded, unreadable, and omitted instruction paths are explicit.
- [ ] An unreadable applicable rule yields Audit Coverage PARTIAL.
- [ ] No write occurs before instruction resolution completes.

#### Case Verdict

PASS only with a complete revision-bound chain and correct per-target precedence;
otherwise BLOCKED with Gate Eligible NO.

---

### Case 3 [TSU-C03]: Evidence routing has one canonical owner

#### Fixture

- Coding policy routes evidence to production/qa/evidence.
- An existing README routes visual evidence to tests/evidence.
- The proposed layout manifest declares the canonical route.

#### Input

- Audit or repair of test infrastructure.

#### Expected reads

- Instruction chain, coding policy, current layout manifest, README, execution
  manifest, and relevant consumer references.

#### Expected writes

- Authorized managed README/layout fields and immutable repair evidence only.

#### Expected non-writes

- QA plans, review skills, gate skills, and external consumer contracts.

#### Expected behavior

- tests/evidence is classified CONFLICTING.
- Manual evidence and setup automation evidence resolve from one versioned layout
  manifest path and revision.
- Conflicting external consumers produce an owner handoff rather than an inferred
  local rewrite.

#### Assertions

- [ ] No generated text routes visual or UI proof under tests.
- [ ] README and execution manifest bind the exact layout-manifest revision.
- [ ] Shared consumers are never silently edited.
- [ ] Conflicting routes prevent COMPLETE.

#### Case Verdict

PASS when every managed route derives from the current layout manifest and no
forbidden route remains; otherwise BLOCKED or INCOMPLETE.

---

### Case 4 [TSU-C04]: Layout and implementation share one versioned manifest

#### Fixture

- Required directory IDs are unit, integration, performance, playtest, and
  setup-canary.
- An old tree contains unit, integration, smoke, and evidence directories.
- Empty directories have no tracked manifest or README.

#### Input

- Scaffold or repair with an approved layout manifest.

#### Expected reads

- Existing tree, README, layout manifest, execution manifest, and consumer
  references within scope.

#### Expected writes

- Nonempty managed records for each required directory and the exact current
  layout manifest.

#### Expected non-writes

- Human test sources and legacy directories not explicitly authorized for change.

#### Expected behavior

- The implementation derives directory creation and reporting from stable layout
  IDs rather than duplicated prose.
- Legacy smoke and evidence directories do not satisfy performance or playtest.
- Playtest contains adapters or fixtures, not manual evidence.

#### Assertions

- [ ] Every required directory ID resolves to one contained path.
- [ ] Changed-path claims match actual tracked files.
- [ ] The execution manifest binds the layout-manifest revision.
- [ ] No empty-path or directory-existence claim implies completion.

#### Case Verdict

PASS when one current layout manifest governs the complete tracked layout;
otherwise INCOMPLETE with Gate Eligible NO.

---

### Case 5 [TSU-C05]: Structured engine authority must match project reality

#### Fixture

- A cgs-test-setup-engine-manifest/v1 identifies engine, aliases, exact version,
  language, project root, descriptor revision, and module or assembly.
- Actual project descriptor and version authority are available.
- Variants contain an alias not listed, a second project root, or a version,
  language, descriptor_revision, or module mismatch.

#### Input

- Any mode with the exact engine-manifest path.

#### Expected reads

- Engine manifest, technical preferences, engine version authority, project
  descriptor, package/runtime data, and runner/framework configuration.

#### Expected writes

- Audit evidence only when identity conflicts.
- No scaffold or workflow activation for a conflicted identity.

#### Expected non-writes

- Engine manifest, project descriptor, version authority, and package manifests.

#### Expected behavior

- Only enumerated aliases normalize.
- Project root containment and descriptor declared revision are verified.
- Free-text engine labels cannot establish identity.
- Every conflict is explicit and fail-closed.

#### Assertions

- [ ] No engine, language, version, project name, module, or assembly is guessed.
- [ ] Multiple roots and symlink escapes are rejected.
- [ ] Exact framework and adapter compatibility is checked.
- [ ] Identity conflict yields BLOCKED.

#### Case Verdict

PASS for one fully consistent structured identity; otherwise BLOCKED with no
target write.

---

### Case 6 [TSU-C06]: Repository policy controls reviewable CI behavior

#### Fixture

- A cgs-test-setup-repository-policy/v1 supplies default/trunk/PR branch policy,
  path filters, cache inputs and restore scope, timeout, concurrency, runner
  labels, and permissions.
- Variants omit a field, disagree with verified VCS default branch, or contain a
  hard-coded main branch.

#### Input

- Scaffold, audit, verify, or repair of active CI.

#### Expected reads

- Repository-policy bytes/revision, verifiable VCS branch reference when available,
  dependency lock, workflow, and execution manifest.

#### Expected writes

- Only an authorized managed cgs-tests subtree and immutable evidence.

#### Expected non-writes

- Repository policy, VCS configuration, other workflow jobs, and branch settings.

#### Expected behavior

- CI generation derives every governed field from the policy.
- Cache keys bind engine/framework/dependency/tool revisions; restored bytes are
  Revalidate before use.
- Missing or conflicting policy leaves active CI unmodified and SETUP_PENDING.

#### Assertions

- [ ] No branch, path-filter, cache, timeout, or permission default is invented.
- [ ] Cache hit never proves dependency validity.
- [ ] Least privilege and concurrency are semantically checked.
- [ ] Policy mismatch prevents CI VERIFIED.

#### Case Verdict

PASS when active CI exactly matches a current policy revision; SETUP_PENDING or
INVALID otherwise.

---

### Case 7 [TSU-C07]: Exact managed CI job is parsed and patched without collateral edits

#### Fixture

- A workflow contains cgs-tests, lint, and package jobs.
- Another workflow contains a job named test.
- cgs-tests uses a wrong runner argv and stale execution-manifest revision.

#### Input

- Audit followed by an authorized ID-keyed repair.

#### Expected reads

- Complete parsed workflow trees, exact cgs-tests node, manifests, dependency
  review receipts, and current runner argv/revision.

#### Expected writes

- Managed cgs-tests fields and immutable repair artifacts only.

#### Expected non-writes

- lint, package, other workflows, comments where parser round-trip supports them,
  and all unrelated tests.

#### Expected behavior

- Presence of a workflow or generic test job provides no evidence.
- The exact job ID, event policy, manifest revision, argv array, logs, receipts,
  secrets, actions, timeout, cache, and runner prerequisites are validated.
- Repair uses a structured pointer and all-file compare-and-set.

#### Assertions

- [ ] Wrong argv is found even if the workflow is syntactically valid.
- [ ] Human job semantics remain unchanged.
- [ ] Old setup and CI receipts become stale after workflow change.
- [ ] Whole-workflow replacement is prohibited.

#### Case Verdict

PASS when exact-job semantics and preservation revisions verify; otherwise FAIL,
PARTIAL, or BLOCKED.

---

### Case 8 [TSU-C08]: Verification ladder is explicit and fail-closed

#### Fixture

- Scaffold files can be created.
- Variants make a static validator unavailable, discovery time out, one parser
  unsupported, canary execution partial, or CI receipt remote log unavailable.

#### Input

- Scaffold or verify.

#### Expected reads

- Contract, all authority and manifest revision, pinned validator manifest,
  execution receipts, logs, and CI receipt dependencies.

#### Expected writes

- Immutable evidence for checks that actually ran and the final setup report when
  persistence is authorized.

#### Expected non-writes

- Fabricated receipts, inferred results, newest-file substitutions, and any
  downstream gate state.

#### Expected behavior

- The level advances only through AUDITED, CREATED, STATIC_VALIDATED,
  DISCOVERY_VERIFIED, CANARY_PASS, FAILURE_SENSITIVE, and CI_VERIFIED.
- A higher observed result cannot fill a missing lower rung.
- Unavailable, timeout, unsupported, omitted, partial, stale, invalid, or
  unverified evidence maps to PARTIAL or NOT_RUN and Gate Eligible NO.

#### Assertions

- [ ] File creation stops at CREATED.
- [ ] Static parser success does not prove discovery.
- [ ] Local green cannot prove trusted CI.
- [ ] No incomplete branch emits COMPLETE or VERIFIED setup.

#### Case Verdict

PASS when the reported rung equals the last conclusively proven rung; any
overclaim is FAIL.

---

### Case 9 [TSU-C09]: Dependencies and actions require immutable reviewed provenance

#### Fixture

- The dependency lock lists framework, parser, launcher, and CI actions.
- Variants use a major tag, a full SHA without review, missing license or security
  disposition, a stale review-receipt revision, or changed transitive lock bytes.

#### Input

- Audit, scaffold, repair, or verify.

#### Expected reads

- Dependency lock, source identities, immutable SHAs or reference IDs, transitive locks,
  review receipt paths/revisions, and installed bytes.

#### Expected writes

- Audit findings or an authorized managed dependency-lock patch plus repair
  evidence; no external installation or review fabrication.

#### Expected non-writes

- External registries, licenses, review receipts, secrets, and runner provisioning.

#### Expected behavior

- Immutable identity and approval are independent required predicates.
- Every installed or restored dependency is Revalidate.
- Any dependency or review change invalidates prior setup and CI receipts.
- Missing external approval produces SETUP_PENDING.

#### Assertions

- [ ] Major tags fail immutable identity.
- [ ] Full commit SHA alone does not prove review.
- [ ] Reviewer identity, license, security/deprecation disposition, and receipt
  revision are present.
- [ ] Cache restore is checked against the lock.

#### Case Verdict

PASS only for reviewed immutable current provenance; otherwise SETUP_PENDING,
INVALID, or BLOCKED with Gate Eligible NO.

---

### Case 10 [TSU-C10]: Deterministic pass and intentional failure prove the runner

#### Fixture

- Version-matched adapter, runner, parser, canary sources, and execution manifest
  all revision_match.
- Stable pass and setup-only failure IDs each discover exactly once.
- Seed, order, locale, timezone, environment-name set, parallelism, timeout, and
  normalization are frozen before execution.

#### Input

- Verify using only pinned argv-array entries.

#### Expected reads

- Current candidate/build/layout/execution manifests, sources, runner, parser,
  deterministic controls, and dependency lock.

#### Expected writes

- Immutable pass, failure-probe, and post-probe logs and automated receipts.

#### Expected non-writes

- Ordinary suite selection, failure fixture state, shell scripts, and fallback
  runner commands.

#### Expected behavior

- Pass returns zero with one pass.
- Intentional assertion failure returns the declared conclusive nonzero failure.
- Isolated post-probe pass returns zero.
- First and last pass semantic projections match; timing fields are excluded from
  equality and no retry policy changes after observation.

#### Assertions

- [ ] Timeout, crash, parse error, zero discovery, or truncated output is not a
  conclusive intentional failure.
- [ ] Failure fixture is excluded from ordinary execution.
- [ ] Projection mismatch yields Determinism Status UNSTABLE.
- [ ] Missing deterministic controls yields PARTIAL, never VERIFIED.

#### Case Verdict

PASS only for conclusive PASS, FAIL, equal isolated PASS and Determinism VERIFIED;
otherwise INCOMPLETE with Gate Eligible NO.

---

### Case 11 [TSU-C11]: Engine-specific required artifacts are real and version matched

#### Fixture

- Variant A is Godot with a pinned addon and completion-aware wrapper.
- Variant B is Unity with pinned Test Framework and project assemblies.
- Variant C is Unreal with exact project, module, editor, automation filter, and
  self-hosted runner labels.
- Negative variants omit one required artifact or contain unresolved identity.

#### Input

- Scaffold or verify for exactly one structured engine identity.

#### Expected reads

- Engine authority, project descriptor, dependency lock and reviews, approved
  adapter template, runner/parser, and existing engine artifacts.

#### Expected writes

- Only the authorized version-matched engine artifacts and evidence.

#### Expected non-writes

- Project descriptor, external plugin installation, license acquisition, and
  runner provisioning.

#### Expected behavior

- Godot waits for suite completion and propagates exit class.
- Unity creates and parses both EditMode and PlayMode asmdefs, compiles, and
  discovers tests.
- Unreal resolves every project/module/editor/filter/runner value.
- Missing external prerequisites yield SETUP_PENDING, not wired CI.

#### Assertions

- [ ] No unresolved engine or project placeholder is active.
- [ ] README claims cannot replace actual files or execution.
- [ ] Unity discovery is greater than zero.
- [ ] No fallback engine command is synthesized.

#### Case Verdict

PASS for complete version-matched engine semantics; SETUP_PENDING or INCOMPLETE
otherwise.

---

### Case 12 [TSU-C12]: Receipt freshness is recomputed from every dependency

#### Fixture

- Local static, execution, setup, and CI receipts are supplied.
- Variants have missing schema or signature, prior layout revision, changed source,
  changed runner/parser/workflow/dependency review, unavailable remote log, or
  complete current bindings.

#### Input

- Audit or verify with explicit receipt paths.

#### Expected reads

- Raw receipt bytes and every declared local or trusted remote dependency.

#### Expected writes

- Freshness findings and, if authorized and otherwise valid, one immutable setup
  report.

#### Expected non-writes

- Existing receipts, remote artifacts, timestamps, badges, and prior run state.

#### Expected behavior

- Parse/signature failure is INVALID.
- Any dependency mismatch is STALE.
- Remote unavailable, timeout, unsupported verifier, or incomplete coverage is
  UNVERIFIED and partial.
- Only fully revalidated bytes are CURRENT.
- Latest name, time, badge, or local green never substitutes for current proof.

#### Assertions

- [ ] Receipt schema, producer/tool revision, dependency set, and receipt revision or
  signature are required.
- [ ] Every local dependency is Revalidate.
- [ ] Partial and stale receipts cannot advance the ladder.
- [ ] CI receipt binds deterministic controls and equal pass projections.

#### Case Verdict

PASS only when freshness classification exactly matches evidence; overclaiming
CURRENT is FAIL.

---

### Case 13 [TSU-C13]: Concurrent repair change fails without partial overwrite

#### Fixture

- An authorized repair plan spans multiple managed files.
- All preimage and backup revisions initially match.
- One path changes after preview and before apply.

#### Input

- Repair with the frozen operation IDs and patch revision.

#### Expected reads

- Current bytes for every path immediately before any write, repair plan,
  preimages, backup revisions, and exact diff.

#### Expected writes

- One immutable blocked receipt only.

#### Expected non-writes

- Every managed target path, divergent user bytes, and unrelated files.

#### Expected behavior

- All-file compare-and-set detects the changed path before the first write.
- The repair returns BLOCKED — CONCURRENT CHANGE.
- Recovery handoff describes a separately authorized three-way patch using
  current/base/candidate revision; it never recommends copying a backup over work.

#### Assertions

- [ ] Zero target files change.
- [ ] First divergent path and observed revision are recorded.
- [ ] Backup presence does not authorize restoration.
- [ ] Replanning requires a new repair identity and approval boundary.

#### Case Verdict

PASS when concurrency produces a no-write blocked result with preserved external
edits; any partial overwrite is FAIL.

---

### Case 14 [TSU-C14]: Fully current deterministic setup may become gate eligible

#### Fixture

- Instruction, engine, repository, layout, execution, dependency, source,
  validator, runner, parser, workflow, and receipt revision are current.
- Audit coverage is complete.
- Static validation and nonzero discovery pass.
- Pass, intentional conclusive failure, and equal isolated post-probe pass verify.
- Active cgs-tests CI matches policy and uses reviewed immutable actions.
- Trusted current CI receipt proves the same bytes and sequence.
- Durable report publish and read-back succeed.

#### Input

- Verify for one exact candidate, build, platform, configuration, and run ID.

#### Expected reads

- Every authority, manifest, implementation, log, receipt, signature, and
  dependency declared by cgs-test-setup-receipt/v2.

#### Expected writes

- One immutable all-or-none run directory and current setup report.

#### Expected non-writes

- Live game/test sources, policies, shared consumers, gates, commits, and remote
  systems.

#### Expected behavior

- Verification Level is CI_VERIFIED.
- Audit Coverage and Static Validation are complete and PASS.
- Determinism Status is VERIFIED and Receipt Freshness is CURRENT.
- Setup Status is VERIFIED, Verdict COMPLETE, and Gate Eligible YES.
- Downstream workflows are not invoked.

#### Assertions

- [ ] Report header contains all v2 machine-readable fields.
- [ ] Changed, unchanged, unmanaged, rejected, backup, diff, and receipt revision
  are internally consistent.
- [ ] A report persistence or read-back failure removes gate eligibility.
- [ ] Every negative variant stops at the last proven rung.

#### Case Verdict

PASS only for the exact all-current happy path; otherwise fail closed with Gate
Eligible NO.

---

## Protocol Compliance

- [ ] **[TSU-PC-001]** Exact mode, IDs, authority paths, candidate, and options are
  validated before reads with side effects.
- [ ] **[TSU-PC-002]** Bounded authorization covers exact writes and argv arrays.
- [ ] **[TSU-PC-003]** Audit performs no write and no process execution.
- [ ] **[TSU-PC-004]** Instruction, engine, repository, dependency, layout, and
  execution authorities are raw-revision-bound.
- [ ] **[TSU-PC-005]** Semantic validator coverage is complete or explicitly
  PARTIAL and fail-closed.
- [ ] **[TSU-PC-006]** Multi-file repair uses all-file compare-and-set, backup,
  full diff, read-back, and immutable receipt.
- [ ] **[TSU-PC-007]** Runner execution uses pinned argv arrays without shell
  interpolation or fallback commands.
- [ ] **[TSU-PC-008]** Secrets are allowlisted by name and values are redacted and
  never persisted.
- [ ] **[TSU-PC-009]** Timeout terminates the full process tree and cannot count
  as a conclusive failure probe.
- [ ] **[TSU-PC-010]** Deterministic controls and semantic projections are frozen
  before observation and never score-gamed with ad hoc retries.
- [ ] **[TSU-PC-011]** Current receipt status is derived by dependency Revalidate and
  signature verification, not name, date, badge, or mtime.
- [ ] **[TSU-PC-012]** No catalog, shared QA contract, downstream skill, gate,
  commit, push, or publication is mutated or invoked.

## Coverage Notes

### Authoritative P1 finding trace

| Audit ID | SKILL clause | Case/assertion |
|---|---|---|
| `TSU-005` | Phase 2 semantic audit/repair | Case 1: stale semantics despite paths; partial coverage blocks repair/gate |
| `TSU-006` | Phases 1/3 instruction authority and naming | Case 2: closest tests rule; unreadable rule yields PARTIAL |
| `TSU-007` | Contract evidence route; Phase 3 layout | Case 3: no visual/UI proof under tests; no shared-consumer edit |
| `TSU-008` | Phase 3 versioned manifest contract | Case 4: directory IDs resolve once; execution manifest binds layout revision |
| `TSU-009` | Phase 1 engine/project authority | Case 5: no identity guessing; conflicts BLOCKED |
| `TSU-010` | Phase 1 repository policy; Phase 5 CI | Case 6: no invented CI defaults; policy mismatch blocks VERIFIED |
| `TSU-011` | Phase 5 exact managed job patch | Case 7: wrong argv detected; whole-workflow replacement prohibited |
| `TSU-012` | Verification states; Phases 4/6/8 ladder | Case 8: parser is not discovery; incomplete never COMPLETE/VERIFIED |
| `TSU-013` | Phase 5 dependency/action provenance | Case 9: major tags not immutable; commit SHA alone not reviewed |

The matrix above replaces range-only coverage with one independent row for every
exact P1 ID in the 2026-07-20 test-setup audit.

Cases 10 through 14
preserve the P0 canary, engine, receipt, concurrency, and complete-path guarantees
while making determinism, partial validation, freshness, and all-file repair
fail-closed. Candidate-root execution requires a separately pinned runner contract;
this written specification alone does not claim engine, CI, or runtime execution.
