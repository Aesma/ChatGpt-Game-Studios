# Skill Spec: `$create-epics`

> **Category**: pipeline
> **Priority**: high
> **Spec revision**: P1 CE-003..CE-007
> **Spec written**: 2026-07-22

## Skill Summary

`$create-epics` reads the current Approved system set from the systems index,
binds it to current architecture modules and valid Accepted ADR evidence, and
plans exactly one canonical epic for each architecture module in scope. Multiple
systems mapped to one module are aggregated into that one epic; a system that
spans modules requires explicit responsibility slices. Each candidate is bound
to a bounded source manifest, current TR dispositions, deterministic dependency
order, exact preimage and candidate hashes, and an external result receipt.

The workflow is read-only until a planning owner approves the exact plan and the
user separately authorizes one complete mutation changeset. A full-mode producer
gate has one initial review and at most one targeted revision/re-review. Source,
target, identity, approval, authorization, writer, and recorder CAS gates run
before the first write. The skill never creates stories.

---

## Static Assertions

- [ ] **CE-S001** — YAML frontmatter contains only `name` and non-empty `description`; `name` is exactly `create-epics`.
- [ ] **CE-S002** — The request contract is `cgs.create-epics-request/v2` and a no-argument invocation causes zero filesystem, agent, approval, or authorization effects.
- [ ] **CE-S003** — The request identifies exact scope and hashes for the systems index, GDDs, architecture, control manifest, TR registry, ADR evidence, epic index, and existing epic targets.
- [ ] **CE-S004** — Source acquisition is capped at 32 files and 1,048,576 exact bytes, with an explicit BLOCKED outcome on overflow.
- [ ] **CE-S005** — The source inventory is represented by `cgs.epic-source-manifest/v2`, including normalized path, role, exact byte count, SHA-256, source identity, and selected/current evidence.
- [ ] **CE-S006** — `design/gdd/systems-index.md` is the sole system-enumeration authority; globs, headings, names, architecture, and epic files cannot add systems.
- [ ] **CE-S007** — Only exact `Approved` rows are eligible, the legal status vocabulary is `Not Started | In Design | In Review | Approved | Implemented`, and `Designed` is malformed rather than eligible.
- [ ] **CE-S008** — The indexed identity, exact GDD path, layer, status, and current-selection evidence must be complete and agree with the full-read GDD.
- [ ] **CE-S009** — Current GDD, architecture, control-manifest, TR-registry, and ADR source versions are selected through explicit current/version/hash evidence; directory order and newest-looking names are not authority.
- [ ] **CE-S010** — Binding architecture requires the declared architecture target hash and an Accepted ADR with matching target hash, independent review hash, authoring receipt, and `cgs.adr-lifecycle-record/v1` evidence.
- [ ] **CE-S011** — The workflow first constructs `module_id -> {system_ids[]}` with module name, owner, architecture locator/hash, Accepted ADRs, layer, dependencies, and deterministic `order_key`.
- [ ] **CE-S012** — The invariant is exactly one epic per architecture module; system-per-epic and mixed cardinality modes are forbidden.
- [ ] **CE-S013** — Multiple selected systems mapped to one module are aggregated into one epic whose `system_ids[]` contains every included system.
- [ ] **CE-S014** — A system spanning multiple modules requires explicit, non-overlapping responsibility slices and TR mappings for every module; ambiguity is BLOCKED.
- [ ] **CE-S015** — Canonical identity is `EPIC-MODULE:<module_id>` and remains stable across source-version changes.
- [ ] **CE-S016** — Every architecture-relevant TR receives exactly one disposition: `ADR_ACCEPTED`, `ADR_NA`, `ADR_REQUIRED_GAP`, or `UNKNOWN`.
- [ ] **CE-S017** — `ADR_NA` requires one reason code from `PRODUCT_ONLY | CONTENT_ONLY | PRESENTATION_ONLY | NO_ARCHITECTURE_EFFECT`, plus owner and auditable evidence.
- [ ] **CE-S018** — `ADR_REQUIRED_GAP` and `UNKNOWN` generate stable `cgs.epic-traceability-finding/v1` records and force the affected epic to `Blocked`.
- [ ] **CE-S019** — `TR-???`, unaudited `N/A`, invented ADR IDs, or missing mappings are prohibited from candidate epics.
- [ ] **CE-S020** — Epic dependencies come from the module graph, use canonical module IDs, and are checked for missing nodes, self-edges, and cycles before approval.
- [ ] **CE-S021** — Candidate ordering is deterministic topological order with ties broken by `order_key` and then `module_id`.
- [ ] **CE-S022** — Each `cgs.epic-plan/v2` epic records source-manifest ID/hash and the exact hashes/versions of its GDD, architecture, control manifest, TR registry, and ADR evidence.
- [ ] **CE-S023** — Any source-binding change makes a previously managed epic stale even if its prose appears unchanged; stale compatible artifacts classify `stale-update`.
- [ ] **CE-S024** — Existing targets and index rows classify only as `create`, `no-op`, `update`, `stale-update`, or `conflict`, with conflict-safe behavior inherited from CE-002.
- [ ] **CE-S025** — `no-op` requires exact candidate bytes, current source binding, stable identity, and a unique compatible index mapping.
- [ ] **CE-S026** — Full mode runs one read-only `PR-EPIC` producer review after planning and inventory, with one attempt capped at 60 seconds.
- [ ] **CE-S027** — `cgs.epic-producer-result/v1` records review status, disposition, source/plan/candidate hashes, stable finding IDs, omissions, and reviewer identity.
- [ ] **CE-S028** — Producer partial, timeout, failure, or side-effect returns PARTIAL with zero writes; it cannot be retried, replaced, or inferred as a pass.
- [ ] **CE-S029** — Producer concerns allow only accepted non-blocking advisory findings with rationale/owner/review point or one targeted revision followed by one re-review; continued blocking yields `BLOCKED — SCOPE DECISION REQUIRED`.
- [ ] **CE-S030** — Lean and solo modes record the producer gate as skipped; solo mode invokes zero agents, and skipped is never represented as `REALISTIC`.
- [ ] **CE-S031** — `cgs.epic-plan-approval/v1` binds the exact source, module map, dependency graph, producer result, targets, index, hashes, receipt path, owner, and decision.
- [ ] **CE-S032** — Planning approval does not authorize filesystem mutation; one later explicit mutation authorization binds the complete changeset, writer, recorder, and non-write scope.
- [ ] **CE-S033** — Source, target-set, identity, approval/authorization, and role CAS gates all pass in one pre-write preflight; any mismatch causes zero writes.
- [ ] **CE-S034** — Changed epics write and verify in dependency order, the index writes after epics, and a create-only external receipt writes last.
- [ ] **CE-S035** — The workflow never claims multi-file atomicity or rollback; any post-write failure yields PARTIAL and exact applied/not-applied evidence.
- [ ] **CE-S036** — `cgs.create-epics-result-receipt/v1` binds source, plan, approval, authorization, producer result, writer/recorder, target/index preimages, candidates, observations, findings, and COMPLETE/PARTIAL status.
- [ ] **CE-S037** — Epic/index content does not embed the result receipt path or hash, avoiding self-referential hashes; it may store a stable receipt ID.
- [ ] **CE-S038** — COMPLETE, COMPLETE—NO_CHANGES_REQUIRED, PARTIAL, BLOCKED, DECLINED, and STOPPED outcomes have distinct evidence and mutation semantics.
- [ ] **CE-S039** — The workflow never creates stories, edits story indexes, or invokes `$create-stories`; it offers exactly one bounded next action.
- [ ] **CE-S040** — `agents/openai.yaml` accurately describes one source-bound epic per architecture module and does not imply automatic or approval-free writes.

---

## Director Gate Checks

- **Full mode**: `PR-EPIC` runs after source-bound candidates and conflict-free
  inventory, before plan approval and mutation authorization. One initial review
  plus at most one targeted revision/re-review is allowed.
- **Lean mode**: no producer call; the typed result records `status: skipped`,
  `mode: lean`, and an omission reason.
- **Solo mode**: zero agent calls; the typed result records `status: skipped`,
  `mode: solo`, and an omission reason.
- Producer advice is not plan approval, mutation authorization, writer identity,
  or recorder evidence.
- Conflict, invalid source binding, ambiguous module responsibility, ADR/TR gap,
  or dependency cycle blocks before mutation regardless of producer disposition.

---

## Behavioral Test Cases

### Case 1: No-argument invocation has zero effects

**Fixture**: Invoke `$create-epics` with no request payload.

**Expected behavior**:

1. The skill explains the required `cgs.create-epics-request/v2` fields.
2. It does not read project artifacts, call a producer, request approval or
   authorization, or write a file.

**Assertions**:

- [ ] No project path is accessed or mutated.
- [ ] No agent is called.
- [ ] The terminal result is not COMPLETE.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Systems index is the only enumeration authority

**Fixture**:

- `SYS-COMBAT` is an exact `Approved` row with a current GDD path.
- An unindexed experimental GDD has a compelling summary and architecture terms.
- Scope is `all`.

**Expected behavior**:

1. Only `SYS-COMBAT` enters the selected system set.
2. The experimental GDD may not add, replace, or supplement a system.
3. The manifest records the exact indexed GDD path and hash.

**Assertions**:

- [ ] No glob, heading search, or filename guess changes enumeration.
- [ ] The unindexed document is absent from selected systems and target epics.
- [ ] Selection evidence is current and explicit.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: `Designed` and malformed status fail closed

**Fixture**: A requested row uses `Designed`; another uses legal but ineligible
`In Review`; no writes have occurred.

**Expected behavior**:

1. `Designed` is reported as malformed because it is outside the legal status
   vocabulary.
2. `In Review` is legal but ineligible.
3. Requested scope that cannot be enumerated completely ends BLOCKED with zero
   writes.

**Assertions**:

- [ ] Only exact `Approved` is eligible.
- [ ] No alias, fallback, or inferred status is used.
- [ ] The defect identifies the exact row and source hash.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Two systems in one module produce one epic

**Fixture**:

- `SYS-INPUT` and `SYS-CAMERA` are current Approved systems.
- Current binding architecture maps both to `MOD-PLAYER-INTERACTION`.
- The module has valid current Accepted ADR evidence.

**Expected behavior**:

1. The module map has one key, `MOD-PLAYER-INTERACTION`, with both system IDs.
2. Exactly one `EPIC-MODULE:MOD-PLAYER-INTERACTION` candidate is rendered.
3. The epic aggregates both systems and their TR rows without duplicating module
   ownership or creating system epics.

**Assertions**:

- [ ] Candidate epic count is one, not two.
- [ ] `system_ids[]` contains both stable IDs exactly once.
- [ ] The index has one row for the canonical module epic.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: One system may span modules only through explicit slices

**Fixture**: `SYS-COMBAT` maps to `MOD-COMBAT-RUNTIME` and
`MOD-COMBAT-PRESENTATION`.

**Variant A**: Each module has a non-overlapping responsibility slice and exact
TR mapping.
**Variant B**: The architecture says only “combat belongs to both modules.”

**Expected behavior**:

1. Variant A creates two module candidates, each with its exact slice and TRs.
2. Variant B produces a stable mapping finding and BLOCKED with zero writes.
3. The skill never chooses one module heuristically or creates a third
   system-level epic.

**Assertions**:

- [ ] Cardinality remains one epic per module in both variants.
- [ ] Responsibility slices are explicit, complete, and non-overlapping.
- [ ] Ambiguity cannot be waived by generic user authorization.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Accepted ADR must be current and evidence-complete

**Fixture**:

- Architecture cites `ADR-0012` as Accepted.
- Variant A has matching target hash, independent review hash, authoring receipt,
  and lifecycle record.
- Variant B lacks the lifecycle record or targets an older architecture hash.

**Expected behavior**:

1. Variant A may bind the module and records all evidence hashes.
2. Variant B is non-binding and ends BLOCKED with the exact missing or mismatched
   evidence.
3. A filename or prose label `Accepted` cannot replace lifecycle evidence.

**Assertions**:

- [ ] ADR validity is hash-bound to the current architecture target.
- [ ] User approval cannot promote Proposed or stale ADR evidence.
- [ ] No affected epic becomes Ready under Variant B.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: TR dispositions route gaps downstream

**Fixture**: One module has four architecture-relevant requirements:

- `TR-101` maps to a valid Accepted ADR.
- `TR-102` is product-only with owner and evidence.
- `TR-103` requires an architecture decision that does not exist.
- `TR-104` has indeterminate applicability.

**Expected behavior**:

1. The exact dispositions are `ADR_ACCEPTED`, `ADR_NA`, `ADR_REQUIRED_GAP`, and
   `UNKNOWN`.
2. `TR-102` uses reason code `PRODUCT_ONLY` and retains owner/evidence.
3. Stable findings for `TR-103` and `TR-104` make the module epic `Blocked`.
4. The candidate contains no `TR-???`, bare `N/A`, or invented ADR.

**Assertions**:

- [ ] Every relevant TR has exactly one disposition.
- [ ] Downstream story eligibility is false while blocking findings remain.
- [ ] Findings remain stable across an unchanged rerun.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Source changes make a managed epic stale

**Fixture**:

- Existing managed epic prose equals the newly rendered prose.
- Its recorded TR-registry hash is older than the current selected registry.
- Identity and managed schema are otherwise compatible.

**Expected behavior**:

1. The skill detects the source-binding mismatch.
2. It classifies the target `stale-update`, not `no-op`.
3. The preview shows old/new source hashes and the deterministic candidate hash.

**Assertions**:

- [ ] Source currency is content-bound, not based on path or prose similarity.
- [ ] All relevant GDD/architecture/manifest/TR/ADR hashes are recorded.
- [ ] Story handoff is not offered from the stale preimage.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Dependency graph produces deterministic order

**Fixture**:

- `MOD-DATA` precedes `MOD-RUNTIME`; `MOD-RUNTIME` precedes `MOD-UI`.
- Two independent same-layer modules share an order rank.

**Expected behavior**:

1. All edges use canonical module IDs and validate against the module map.
2. The plan orders data, runtime, then UI.
3. Same-rank nodes use `order_key`, then `module_id` as deterministic ties.

**Assertions**:

- [ ] The order is stable across unchanged reruns.
- [ ] Epic dependencies and the index use the same canonical IDs.
- [ ] No hidden filesystem order influences output.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Missing dependency or cycle blocks all writes

**Fixture**: Variant A references an absent module. Variant B contains
`MOD-A -> MOD-B -> MOD-A`. A separate candidate would otherwise be valid.

**Expected behavior**:

1. The complete graph is validated before producer review or approval.
2. The exact missing node or cycle path becomes a stable finding.
3. The whole changeset is BLOCKED; the independent candidate is not written.

**Assertions**:

- [ ] No topological order is fabricated.
- [ ] No producer disposition can legitimize the graph.
- [ ] All files remain byte-identical.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 11: Exact current rerun is no-op

**Fixture**: Every managed epic and the index exactly match deterministic
candidates and current source bindings; there are no conflicts or skips needing
action.

**Expected behavior**:

1. Every target and the index classify `no-op` after fresh reads and hashes.
2. No mutation authorization or activity-only receipt is requested.
3. The workflow ends `COMPLETE — NO_CHANGES_REQUIRED`.

**Assertions**:

- [ ] No timestamp or receipt churn rewrites a current artifact.
- [ ] Unique module identity and index mapping are revalidated.
- [ ] Zero files are mutated.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 12: Compatible update and create use one changeset

**Fixture**:

- One existing managed module epic is compatible but differs from its candidate.
- A second module target is absent.
- The index is compatible and both candidates are conflict-free.

**Expected behavior**:

1. Targets classify `update` and `create`; complete content/diffs and hashes are
   shown.
2. The planning owner approves one exact plan.
3. One separate mutation authorization binds both epics, index, receipt, writer,
   recorder, and non-write scope.
4. After all CAS gates pass, the files write in dependency order, index next,
   receipt last, with read-back verification.

**Assertions**:

- [ ] No per-file authorization is requested.
- [ ] Planning approval alone causes no mutation.
- [ ] Only the exact authorized paths and bytes are written.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 13: Manual content or identity collision is conflict

**Fixture**:

- A canonical target contains an epic for a different module ID or has unknown
  manual content.
- Another module is a clean create.

**Expected behavior**:

1. The target classifies `conflict` with identities, schema evidence, and hash.
2. The complete changeset stops BLOCKED before producer review and authorization.
3. Nothing is overwritten, merged, renamed, deleted, or independently written.

**Assertions**:

- [ ] Generic approval cannot downgrade conflict to update.
- [ ] Existing content remains byte-identical.
- [ ] The clean create is not applied as a partial plan.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 14: CAS detects source, target, index, or role drift

**Fixture**: A plan is approved and a changeset authorized. Before the first
write, independently vary one of: source bytes, target preimage, index preimage,
receipt existence, canonical identity, approval binding, writer, or recorder.

**Expected behavior**:

1. The one-pass preflight detects the mismatch before mutation.
2. Zero files are written.
3. The workflow reports the exact gate/path/hash/identity and reclassifies or
   requires fresh approval/authorization as applicable.

**Assertions**:

- [ ] All authorized paths are checked, not only changed epic paths.
- [ ] Receipt existence is compared to `ABSENT`.
- [ ] No stale plan is partially applied.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 15: Full producer gate converges within one revision

**Fixture**:

- Initial `PR-EPIC` returns `CONCERNS` with stable nontrivial findings.
- The planning owner chooses one targeted revision.
- Re-review returns `REALISTIC`.

**Expected behavior**:

1. The initial review occurs after full plan/inventory and before approval.
2. Only named finding fields are revised.
3. All candidate bytes, target inventory, source-manifest digest, and plan digest
   are regenerated before the single re-review.
4. The current producer result is included in later plan approval.

**Assertions**:

- [ ] Exactly two producer calls occur: initial review and one re-review.
- [ ] Stable finding IDs connect review, revision, and disposition.
- [ ] No files are written during review or revision.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 16: Producer non-convergence and incomplete review fail closed

**Fixture**:

- Variant A remains `UNREALISTIC` or has blocking concerns after the one
  targeted revision.
- Variant B returns timeout, failed, partial, or side-effect on any required
  full-mode review.

**Expected behavior**:

1. Variant A ends `BLOCKED — SCOPE DECISION REQUIRED` with stable findings and
   one owner decision.
2. Variant B ends PARTIAL, preserves omissions/side-effect evidence, and makes
   no writes.
3. There is no third review, retry loop, nested delegation, or inferred pass.

**Assertions**:

- [ ] Review cap is mechanically observable.
- [ ] Blocking producer findings cannot be accepted as advisory.
- [ ] Producer status and disposition remain distinct typed fields.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 17: Lean and solo modes remain evidence-honest

**Fixture**: Run the same valid plan once in lean mode and once in solo mode.

**Expected behavior**:

1. Neither mode calls `PR-EPIC`; solo mode invokes zero agents total.
2. Each typed producer result records `skipped`, the exact mode, and reason.
3. Both runs still execute local mapping, traceability, dependency, approval,
   authorization, CAS, write, and verification gates as applicable.

**Assertions**:

- [ ] Skipped is never encoded as REALISTIC or complete producer evidence.
- [ ] Mode does not relax source or mutation safety.
- [ ] The final result discloses the omitted independent review.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 18: Mid-changeset failure produces exact PARTIAL evidence

**Fixture**: Two epic updates are authorized. The first writes and verifies; the
second write or verification fails.

**Expected behavior**:

1. The workflow stops ordinary writes and does not claim rollback or atomicity.
2. If safely possible, it writes the already-authorized create-only PARTIAL
   receipt with exact applied/not-applied and expected/observed hashes.
3. If the receipt also fails, it reports an unreceipted changed set and remains
   PARTIAL.

**Assertions**:

- [ ] No destructive rollback is attempted.
- [ ] Index is not written if prerequisite epics did not all succeed.
- [ ] COMPLETE is impossible without a verified COMPLETE receipt.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 19: Receipt is external and hash-cycle free

**Fixture**: A valid authorized create succeeds for one epic and the index.

**Expected behavior**:

1. The receipt is created last at the authorized absent path.
2. It binds source, plan, approval, authorization, producer, writer/recorder,
   targets, index, findings, timestamp, and observed hashes.
3. Epic and index bytes do not embed the receipt path or receipt hash.

**Assertions**:

- [ ] The receipt schema is `cgs.create-epics-result-receipt/v1`.
- [ ] Receipt read-back and SHA-256 verification occur before COMPLETE.
- [ ] The receipt cannot authorize its own creation or a repair.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 20: Downstream handoff is one exact next action

**Fixture**: Variant A has one Ready epic and one higher-priority epic Blocked by
an ADR gap. Variant B has one Ready epic and no unresolved blocker.

**Expected behavior**:

1. Variant A offers exactly one action to resolve the named ADR blocker and does
   not offer story creation.
2. Variant B may offer exactly one Ready-epic handoff; it names one epic and binds epic path/hash, source-manifest
   digest, module/system IDs, TR rows, findings, and dependency/order evidence.
3. A Blocked epic remains ineligible; no story skill is invoked in either
   variant.

**Assertions**:

- [ ] The response does not emit a generic create-stories command for every epic.
- [ ] Story files and story indexes remain unchanged.
- [ ] The one next action is concrete and evidence-bound.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 21: Staged package is complete and catalog-honest

**Fixture**: Inspect the P1 candidate directory without invoking `$skill-test`.

**Expected behavior**:

1. The formal path mirror contains `SKILL.md`,
   `references/continued-workflow.md`, `agents/openai.yaml`, and this exclusive
   specification.
2. No live skill, old P0 staging file, shared framework file, or catalog entry is
   changed.
3. Catalog result fields remain untouched until authorized formal evaluation.

**Assertions**:

- [ ] Every staged file has a reported SHA-256 and exact byte count.
- [ ] Live pre-edit snapshot hashes/bytes still match.
- [ ] No staged catalog file exists.

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Cross-Artifact Checks

- [ ] **CE-X001** — Every selected systems-index ID appears in at least one
  explicit module responsibility slice, and no unselected ID enters an epic.
- [ ] **CE-X002** — Every in-scope module has exactly one canonical epic ID/path,
  and every canonical epic ID/path maps back to exactly one module.
- [ ] **CE-X003** — Epic `system_ids[]`, module-map membership, TR responsibility
  slices, and epic-index membership agree exactly.
- [ ] **CE-X004** — Epic source hashes equal source-manifest hashes and the
  approval, authorization, and receipt bind the same source-manifest digest.
- [ ] **CE-X005** — Architecture target hashes and Accepted ADR lifecycle target
  hashes agree for every binding module.
- [ ] **CE-X006** — Dependency edges, topological order, epic dependency fields,
  write order, and index order use the same canonical module identities.
- [ ] **CE-X007** — Producer result, plan approval, mutation authorization, writer,
  recorder, and receipt are independently attributable and cannot substitute for
  one another.
- [ ] **CE-X008** — Candidate hashes, authorized hashes, read-back hashes, index
  hash, and receipt observations agree for COMPLETE; any discrepancy is PARTIAL
  or BLOCKED, never COMPLETE.

---

## Protocol Compliance

- [ ] Question → Options → Decision → Draft → Approval is preserved for
  open-ended module-scope or producer-concern decisions.
- [ ] Exact planning approval precedes and remains distinct from one bounded
  mutation authorization.
- [ ] New or changed scope, bytes, targets, identities, or hashes invalidates the
  applicable approval/authorization instead of being silently absorbed.
- [ ] No mutation occurs during enumeration, source selection, mapping,
  traceability, dependency validation, inventory, producer review, approval, or
  CAS failure handling.
- [ ] Authorized writes are limited to selected epics, the epic index, and one
  external result receipt; GDD, architecture, ADR, TR, control-manifest, and
  story sources are read-only.
- [ ] Partial application is reported honestly with exact path/hash evidence and
  never relabeled COMPLETE.

---

## Coverage Notes

- CE-001 remains covered by Cases 2–3 and static assertions CE-S006..CE-S009.
- CE-002 remains covered by Cases 11–14 and static assertions CE-S024..CE-S025,
  CE-S032..CE-S035.
- CE-003 is covered by Cases 4–5 and CE-S011..CE-S015.
- CE-004 is covered by Case 3 and CE-S007..CE-S008.
- CE-005 is covered by Cases 6–7 and CE-S010, CE-S016..CE-S019.
- CE-006 is covered by Case 8 and CE-S005, CE-S009, CE-S022..CE-S023.
- CE-007 is covered by Cases 15–17 and CE-S026..CE-S030.
- Cases 18–20 validate recorder, partial-result, and downstream safety needed to
  make the P1 contract executable without overstating atomicity or completion.
- Case 21 is a staging-only integrity check. This candidate deliberately does not
  update catalog result fields and does not invoke formal `$skill-test`.
