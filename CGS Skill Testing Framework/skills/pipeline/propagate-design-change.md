# Skill Spec: `$propagate-design-change`

> **Category**: pipeline
> **Priority**: high
> **Spec revision**: P1 PDC-004..PDC-008
> **Spec written**: 2026-07-22

## Skill Summary

`$propagate-design-change` compares one exact current GDD against one explicit
immutable baseline, assigns stable IDs to requirement deltas, traverses stable TR
and dependency edges through downstream planning/work artifacts, and publishes an
immutable owner-routed impact event root plus create-only receipts. It does not
modify GDD, TR, ADR, architecture, epic, story, sprint, implementation, test, or
owner artifacts. Partial coverage, active work, reviewer failure, fanout limits,
and unresolved owners remain explicit and cannot converge by approval alone.

---

## Static Assertions

- [ ] **PDC-S001** — YAML frontmatter contains only `name` and non-empty `description`; the name is `propagate-design-change`.
- [ ] **PDC-S002** — Invocation requires one `cgs.propagate-design-change-request/v2` manifest; no argument causes zero repository reads, agent calls, approvals, authorizations, or writes.
- [ ] **PDC-S003** — The request binds current GDD ID/path/hash and an immutable baseline kind, locator, resolved ID, path, and hash.
- [ ] **PDC-S004** — `HEAD:<path>`, mutable branch labels without resolved object IDs, mtime, and guessed “previous version” are invalid baselines.
- [ ] **PDC-S005** — Rename evidence is explicit and hash-bound; zero or multiple rename candidates are BLOCKED.
- [ ] **PDC-S006** — `change_id` is deterministically derived from stable GDD ID and exact baseline/current locator/path/hash fields.
- [ ] **PDC-S007** — `cgs.design-change-baseline/v2` records locators, resolved IDs, approval evidence, paths, byte counts, hashes, rename proof, workspace state, diff range, and change ID.
- [ ] **PDC-S008** — `cgs.design-change-diff/v2` provides stable delta IDs and exact before/after locators, excerpt/section digests, requirement/TR identities, semantic kind, and source hashes.
- [ ] **PDC-S009** — Missing, duplicate, or ambiguous requirement/TR identity creates a stable finding and remains open; no placeholder or renumbered TR is invented.
- [ ] **PDC-S010** — Source acquisition is index-first and capped at 48 files, 2,097,152 bytes, 256 nodes, 512 edges, and 100 impacts.
- [ ] **PDC-S011** — `cgs.pdc-source-manifest/v2` records exact path/layer/identity/authority/owner/bytes/hash/parse state/edges/omission evidence.
- [ ] **PDC-S012** — Coverage state is exactly `SCANNED | KNOWN_EMPTY | PARTIAL`; required missing/unparseable TR, dependency, ownership, active-work, or inventory evidence is PARTIAL.
- [ ] **PDC-S013** — Fanout overflow stops at a deterministic boundary, reports omitted identities, and creates ordered continuation shards without silently truncating.
- [ ] **PDC-S014** — Stable TR IDs are the primary join and direct path/ADR/epic/story references remain diagnostic edges.
- [ ] **PDC-S015** — Reverse traversal includes ADR/module dependencies, epics, stories, sprint/work, owners, and reverse dependency fanout.
- [ ] **PDC-S016** — Every delta has closure `IMPACTS_FOUND | NO_IMPACT_PROVEN | OPEN_COVERAGE`; no-impact requires complete TR and dependency closure.
- [ ] **PDC-S017** — `impact_id` is deterministically derived from change, delta, artifact type/ID, and impact kind; title, array position, and mutable prose are not identity.
- [ ] **PDC-S018** — `finding_id` is deterministically derived from change, finding kind, subject, and evidence fingerprint; `cgs.design-change-finding/v2` records status, evidence, owner, acceptance, and resolution.
- [ ] **PDC-S019** — `cgs.design-change-impact/v2` records change/delta/impact/artifact IDs, current artifact hash, exact evidence edges, classification, `status`, owner route, resolution, and findings.
- [ ] **PDC-S020** — Impact `status` is `OPEN | COORDINATION_REQUIRED | ROUTED | DEFERRED | RESOLVED` with explicit allowed transitions; RESOLVED is terminal for the change ID.
- [ ] **PDC-S021** — RESOLVED requires a current external `cgs.owner-design-change-resolution/v1` receipt binding owner workflow, impact, pre/post hashes, action, and verification.
- [ ] **PDC-S022** — Active or status-conflicted work becomes `ACTIVE_WORK_RISK` and `COORDINATION_REQUIRED`, recording owner, updated-at, status source/hash, artifact hash, and work identity.
- [ ] **PDC-S023** — Active work remains frozen until a matching external `cgs.active-work-coordination-receipt/v1`; generic approval cannot unfreeze it.
- [ ] **PDC-S024** — `cgs.owner-routed-design-change-plan/v2` groups impacts by authoritative owner and binds owner workflow, artifact snapshot, action, acceptance condition, dependencies, and required receipts.
- [ ] **PDC-S025** — Missing/conflicting/inferred owner evidence creates a finding and prevents ROUTED.
- [ ] **PDC-S026** — The complete impact matrix precedes decisions; interaction is capped at 25 rows per batch and four batches per run, with no per-ADR loop.
- [ ] **PDC-S027** — The canonical report path is exactly `production/change-impact/<change_id>.md` and `cgs.design-change-impact-report/v2` is create-only and immutable.
- [ ] **PDC-S028** — Later evidence is append-only through a linear create-only receipt chain under `production/change-impact/receipts/<change_id>/`.
- [ ] **PDC-S029** — Full mode uses one independent `TD-CHANGE-IMPACT` reviewer attempt capped at 60 seconds; reviewer differs from author and report writer.
- [ ] **PDC-S030** — Reviewer timeout/failure/partial/side-effect/identity collision yields PARTIAL and cannot be replaced by self-review or inferred approval.
- [ ] **PDC-S031** — At most one targeted analysis revision and one re-review are permitted; continued failure cannot trigger a third review or loop-until-pass.
- [ ] **PDC-S032** — Lean and solo record skipped review honestly; solo invokes zero agents and skipped is not APPROVE.
- [ ] **PDC-S033** — `cgs.pdc-report-plan-approval/v2` binds exact baseline/current, diff, manifest, graph, impact plan, review, report root, chain head, receipt, and owner decision hashes.
- [ ] **PDC-S034** — Plan approval does not authorize a write; one later mutation authorization is limited to the immutable report and one receipt.
- [ ] **PDC-S035** — Baseline/current/source, impact/owner evidence, immutable target/chain, approval/authorization, and role CAS all pass before the first write.
- [ ] **PDC-S036** — Any pre-write CAS mismatch causes zero writes and invalidates stale approval/authorization.
- [ ] **PDC-S037** — The report creates and verifies first, the receipt creates and verifies last, and the workflow never claims multi-file atomicity or destructive rollback.
- [ ] **PDC-S038** — `cgs.pdc-result-receipt/v2` binds event-root/predecessor hashes, analysis evidence, approvals, roles, transitions, owner/coordination receipts, open IDs, and continuation shards.
- [ ] **PDC-S039** — ANALYSIS_COMPLETE is distinct from CONVERGED; convergence requires every delta/dependency/impact/finding/coordination/owner resolution closed under a fresh same-pair rescan.
- [ ] **PDC-S040** — The only writable artifacts are the exact immutable impact report and one authorized create-only receipt; no downstream owner artifact is automatically written or workflow invoked.
- [ ] **PDC-S041** — An old Accepted ADR remains unchanged until a concrete accepted replacement and its owner workflow handle any transition; placeholders are forbidden.
- [ ] **PDC-S042** — `agents/openai.yaml` describes stable owner-routed impact analysis and does not imply direct downstream mutation.

---

## Review Gate Checks

- **Full mode**: `TD-CHANGE-IMPACT` receives exact hash-bound analysis after
  candidate render and before plan approval. One initial review and at most one
  targeted revision/re-review are allowed.
- **Lean mode**: no reviewer call; typed result says skipped/lean with an omission
  reason.
- **Solo mode**: zero agent calls; typed result says skipped/solo with an omission
  reason.
- Technical review is advisory quality evidence, not owner resolution, plan
  approval, mutation authorization, or receipt recording.
- No reviewer disposition can upgrade baseline failure, PARTIAL coverage,
  ambiguous ownership, active-work coordination, or an invalid receipt chain.

---

## Behavioral Test Cases

### Case 1: No-argument invocation is inert

**Fixture**: Multiple changed GDDs exist.

**Input**: `$propagate-design-change`

**Expected behavior**:

1. The skill prints the manifest-path usage.
2. It does not discover candidate GDDs, read project state, call a reviewer,
   request approval, or write.

**Assertions**:

- [ ] No GDD is selected implicitly.
- [ ] No project file is read or changed.
- [ ] No agent call occurs.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Explicit git baseline and dirty current bytes remain reproducible

**Fixture**:

- The request resolves caller token `BASE` to immutable commit/blob ID `OID`.
- The baseline path/hash and dirty workspace current path/hash are known.

**Expected behavior**:

1. Baseline bytes come from `OID`; current bytes come from the workspace.
2. Both exact byte counts/hashes and the diff range are recorded.
3. The same pair reproduces the same change ID.

**Assertions**:

- [ ] Dirty current bytes are not replaced with HEAD.
- [ ] Caller token and resolved immutable ID are both present.
- [ ] Re-analysis does not advance either side of the pair.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Approved snapshot and explicit rename are hash-bound

**Fixture**:

- A retrievable approved snapshot identifies old path/hash and approval record.
- The current GDD has a new path and declared rename proof.

**Expected behavior**:

1. Approval record, snapshot bytes, old path, new path, and both hashes verify.
2. Rename evidence enters the baseline record and path-identity delta.
3. A mutable approval label without bytes is rejected.

**Assertions**:

- [ ] No filename similarity is used as authority.
- [ ] The change ID binds both paths.
- [ ] Ambiguous rename evidence is BLOCKED.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Unknown, mutable, or mismatched baseline fails closed

**Fixture variants**: missing baseline; implicit HEAD; unresolved branch label;
unretrievable approved bytes; hash mismatch; multiple rename candidates.

**Expected behavior**:

1. The exact baseline failure is reported.
2. The workflow stops BLOCKED before impact conclusions or report approval.
3. It emits neither NO_IMPACT nor ANALYSIS_COMPLETE.

**Assertions**:

- [ ] No guessed fallback is used.
- [ ] Zero writes occur.
- [ ] Candidate rename paths are shown when applicable.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Stable structured diff IDs survive rerun

**Fixture**: One stable requirement is modified, one added, and one removed under
the same exact baseline/current pair.

**Expected behavior**:

1. Three typed delta rows bind exact before/after locators and digests.
2. Stable requirement identities are preserved; absence/ambiguity becomes a
   finding rather than an invented ID.
3. An unchanged rerun produces identical change/delta IDs and diff hash.

**Assertions**:

- [ ] Conceptual summary alone is insufficient evidence.
- [ ] `TR-???` and automatic renumbering do not appear.
- [ ] A different current hash yields a new change ID.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: TR and dependency closure reaches every downstream owner

**Fixture**:

- Changed delta maps to one TR and ADR/module.
- The module has two reverse dependents, one epic, two stories, and active sprint
  membership across the branches.
- All inventories parse within limits.

**Expected behavior**:

1. Traversal retains TR, ADR, direct, and dependency evidence edges.
2. Every reached artifact has one stable artifact/impact identity while retaining
   all incoming paths.
3. Each branch ends in an owner route or explicit no-impact proof.

**Assertions**:

- [ ] Dependency fanout is not limited to direct TR references.
- [ ] Deduplication does not erase evidence paths.
- [ ] Every delta receives a closure row.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: NO_IMPACT requires complete closure

**Fixture**: A real diff has unambiguous TR identity and no downstream references;
every required inventory and dependency layer is SCANNED or KNOWN_EMPTY.

**Expected behavior**:

1. Every delta records `NO_IMPACT_PROVEN` with explicit edge-absence evidence.
2. The result may be NO_IMPACT only after full bounded coverage.
3. No downstream or activity-only write occurs without exact report approval.

**Assertions**:

- [ ] NO_CHANGE and NO_IMPACT remain distinct.
- [ ] KNOWN_EMPTY is backed by successful authoritative inventory.
- [ ] Empty subsets cannot conceal an unscanned branch.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Partial scan cannot close an impact

**Fixture**: The TR registry is missing, a dependency inventory fails parsing, or
one owner/active-work source cannot be read.

**Expected behavior**:

1. The exact layer/path/failure becomes PARTIAL and a stable finding.
2. Affected deltas remain `OPEN_COVERAGE`.
3. Reviewer approval, user approval, and empty scanned layers cannot upgrade the
   result.

**Assertions**:

- [ ] Output is PARTIAL, not NO_IMPACT/ANALYSIS_COMPLETE/CONVERGED.
- [ ] Omitted sources are named.
- [ ] No downstream mutation is proposed.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Stable impact and finding IDs support closure

**Fixture**: One artifact remains affected across two runs of the same change;
the second run includes a valid owner resolution receipt.

**Expected behavior**:

1. Both runs use the same change, delta, artifact, impact, and finding IDs.
2. The second receipt transitions the impact to RESOLVED and binds artifact
   pre/post hashes plus verification evidence.
3. The immutable root report is not rewritten.

**Assertions**:

- [ ] Mutable title or matrix position does not affect identity.
- [ ] Resolution cannot be inferred from current prose alone.
- [ ] RESOLVED is terminal for the change ID.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Canonical report is fixed, immutable, and conflict-safe

**Fixture variants**:

- Report target is ABSENT.
- A valid report already exists for the same change ID.
- A different or malformed report owns the canonical path.

**Expected behavior**:

1. ABSENT permits a candidate only at
   `production/change-impact/<change_id>.md`.
2. A valid existing report becomes the event root and is never rewritten.
3. Identity/schema/hash conflict is BLOCKED with zero writes.

**Assertions**:

- [ ] No alternate ad hoc report path is guessed.
- [ ] Rerun timestamps do not churn the root report.
- [ ] Generic approval cannot overwrite a conflict.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 11: Owner-routed plan never performs downstream writes

**Fixture**: Impacts affect the TR registry, one ADR, one epic, and two stories,
all with authoritative owners.

**Expected behavior**:

1. The route plan groups exact impacts by owner workflow and acceptance condition.
2. The planning owner may route or defer them in bounded batches.
3. Only report/receipt paths may enter mutation authorization; all affected
   artifacts remain read-only.

**Assertions**:

- [ ] No owner workflow is invoked automatically.
- [ ] “Route” is not represented as applied or resolved.
- [ ] No ADR supersedure or story status change occurs.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 12: Decision batching has a hard interaction boundary

**Fixture**: Seventy impacts are grouped across four owners.

**Expected behavior**:

1. The complete 70-row matrix is displayed before decisions.
2. Decisions are requested in at most three batches of 25/25/20, grouped by
   owner/action; there is no per-ADR prompt.
3. Unreviewed exceptions remain OPEN rather than silently accepted.

**Assertions**:

- [ ] No batch exceeds 25 rows.
- [ ] No run exceeds four decision interactions.
- [ ] The approved route plan binds every decision and omission.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 13: Fanout overflow yields deterministic PARTIAL continuation

**Fixture variants**: Discovery would require file 49, byte 2,097,153, node 257,
edge 513, or impact 101.

**Expected behavior**:

1. The file/node/edge/impact before the hard boundary is processed; the next is
   not partially read or silently dropped.
2. Coverage is PARTIAL and omitted identities are ordered into deterministic
   continuation shards.
3. A continuation binds the same change ID and prior receipt-chain head.

**Assertions**:

- [ ] Limit values cannot be raised by the request.
- [ ] Result is not no-impact or complete.
- [ ] Repeating unchanged evidence yields the same boundary/shards.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 14: In-progress story is frozen by exact coordination state

**Fixture**: An affected story or sprint tracker marks work In Progress and
provides owner, updated-at, status source/hash, artifact hash, and work ID.

**Expected behavior**:

1. The impact becomes ACTIVE_WORK_RISK / COORDINATION_REQUIRED.
2. An elevated warning precedes decisions and the route includes exact snapshot
   evidence.
3. Only a matching external active-work coordination receipt can permit the
   lifecycle to advance.

**Assertions**:

- [ ] Generic plan/write approval cannot unfreeze work.
- [ ] Conflicting status sources are treated as active.
- [ ] The story is never silently edited.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 15: Missing active-work or owner concurrency fields remain PARTIAL

**Fixture**: An active story lacks owner, updated-at, artifact hash, or has
conflicting owner sources.

**Expected behavior**:

1. Missing/conflicting fields create stable findings.
2. The impact remains COORDINATION_REQUIRED and cannot become ROUTED.
3. The run is PARTIAL with one owner-evidence next action.

**Assertions**:

- [ ] Owner is never inferred from filename or current operator.
- [ ] No downstream authorization is emitted.
- [ ] Approval cannot waive the gap.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 16: Full review is independent and hash-bound

**Fixture**: Valid full-mode analysis has distinct author, technical reviewer,
planning owner, writer, and recorder identities; reviewer returns APPROVE.

**Expected behavior**:

1. Exactly one review call receives all exact analysis/candidate hashes.
2. The typed result records independent identities and APPROVE.
3. Review causes no write and does not substitute for owner or plan approval.

**Assertions**:

- [ ] Reviewer differs from author and report writer.
- [ ] Review input hashes match the later approval.
- [ ] No nested reviewer delegation occurs.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 17: Reviewer failure or identity collision yields PARTIAL

**Fixture variants**: timeout, failed, partial, side-effect, reviewer equals
author, reviewer equals report writer, or output hashes do not match inputs.

**Expected behavior**:

1. The technical-review result remains incomplete and the run is PARTIAL.
2. No self-review, inferred approval, automatic retry, or downstream resolution
   write occurs.
3. A hash-bound PARTIAL report/receipt may be proposed only as evidence.

**Assertions**:

- [ ] Failure omissions/side effects are preserved.
- [ ] ANALYSIS_COMPLETE and CONVERGED are impossible.
- [ ] Lean/solo skipping is not used to disguise a failed full review.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 18: Review convergence has one revision ceiling

**Fixture**: Initial review returns CONCERNS; one targeted revision occurs.

**Variant A**: Re-review approves.
**Variant B**: Re-review still has blocking concerns.

**Expected behavior**:

1. All affected candidates and inventories are rehashed before the one re-review.
2. Variant A may proceed to plan approval.
3. Variant B stops PARTIAL/BLOCKED with stable findings; no third review or second
   revision occurs.

**Assertions**:

- [ ] Exactly two review calls maximum are observable.
- [ ] Revision addresses named stable finding IDs only.
- [ ] No loop-until-pass behavior exists.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 19: Plan approval, mutation authorization, and CAS remain separate

**Fixture**: A complete report/receipt preview is approved and later authorized;
before the first write, independently vary current GDD, source manifest, owner
receipt, report target, chain head, writer, or recorder.

**Expected behavior**:

1. The appropriate CAS gate detects each mismatch in a one-pass preflight.
2. Zero writes occur and stale approval/authorization is invalidated.
3. A fresh preview is required when current scope or bytes change.

**Assertions**:

- [ ] Plan approval alone writes nothing.
- [ ] Authorization contains only report/receipt targets.
- [ ] Every declared non-write category remains unchanged.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 20: Report succeeds but receipt fails honestly

**Fixture**: Initial report target is absent; report creation/read-back succeeds;
receipt creation or verification fails.

**Expected behavior**:

1. The immutable report is preserved and not rolled back or overwritten.
2. The result is PARTIAL with exact report/receipt expected and observed hashes.
3. A later authorized recovery receipt may attach to the report root.

**Assertions**:

- [ ] Multi-file atomicity is not claimed.
- [ ] No downstream write occurs during recovery.
- [ ] An unreceipted root cannot be called ANALYSIS_COMPLETE.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 21: Receipt folding proves or rejects convergence

**Fixture variants**:

- A linear chain supplies current owner resolutions for every impact and a fresh
  same-pair scan finds no new impacts.
- A chain forks, skips a sequence, contains an illegal transition, leaves one
  deferred impact, or uses a stale artifact postimage.

**Expected behavior**:

1. The valid variant folds to CONVERGED without rewriting the root report.
2. Invalid variants are BLOCKED or PARTIAL with exact receipt/impact evidence.
3. ANALYSIS_COMPLETE with ROUTED impacts is not mislabeled CONVERGED.

**Assertions**:

- [ ] Every delta/dependency branch closes.
- [ ] RESOLVED requires current owner receipt and postimage verification.
- [ ] New baseline/current bytes create a different change ID.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 22: Accepted ADR safety and staging integrity

**Fixture**:

- A changed requirement suggests an Accepted ADR may need replacement, but no
  concrete accepted replacement owner receipt exists.
- Inspect the P1 candidate without invoking formal `$skill-test`.

**Expected behavior**:

1. The impact is routed as Needs Review; the old ADR remains unchanged and no
   placeholder replacement is written.
2. The formal mirror contains SKILL, continuation reference, metadata, and this
   exclusive spec only.
3. Live files, old P0 staging, shared framework files, and catalog result fields
   remain unchanged.

**Assertions**:

- [ ] No authoritative downstream file is modified.
- [ ] Every staged file has a reported SHA-256 and exact byte count.
- [ ] No staged catalog exists.

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Cross-Artifact Checks

- [ ] **PDC-X001** — Baseline/current hashes in request, baseline record, diff,
  source manifest, report, approval, authorization, and receipts agree exactly.
- [ ] **PDC-X002** — Every delta ID maps to exact changed evidence and one closure
  row; every impact ID maps back to one change/delta/artifact/kind tuple.
- [ ] **PDC-X003** — TR/direct/dependency edges in the graph, impact evidence, owner
  route, and convergence closure agree without dropped branches.
- [ ] **PDC-X004** — Artifact ID/path/hash, owner source/hash, active-work snapshot,
  coordination receipt, and owner-resolution receipt bind the same artifact state.
- [ ] **PDC-X005** — Report path/change ID/root hash and every receipt predecessor,
  sequence, transition, and folded state form one linear immutable chain.
- [ ] **PDC-X006** — Technical-review input hashes, plan approval, mutation
  authorization, writer/recorder identities, and receipt evidence are distinct and
  mutually consistent.
- [ ] **PDC-X007** — Every omitted file/node/edge/impact appears in exactly one
  deterministic continuation shard and prevents a complete/converged verdict.
- [ ] **PDC-X008** — The authorized write inventory contains only the canonical
  report create and one receipt create; every GDD/TR/ADR/architecture/epic/story/
  sprint/implementation/test/owner artifact remains byte-identical.

---

## Protocol Compliance

- [ ] Open owner/scope decisions follow Question → Options → Decision → Draft →
  Approval within bounded interaction batches.
- [ ] Complete impact matrix precedes bulk decisions; no per-artifact approval
  loop occurs.
- [ ] Exact report-plan approval precedes and differs from one report-only
  mutation authorization.
- [ ] Scope, identity, route, source, candidate, chain, writer, or recorder drift
  invalidates stale approval/authorization.
- [ ] PARTIAL remains PARTIAL despite review/user approval or successful evidence
  writes.
- [ ] Owner-routed handoffs are recommendations with receipt requirements, never
  automatic workflow invocation or applied downstream changes.

---

## Coverage Notes

- PDC-001 remains covered by Cases 6–8 and PDC-S011..PDC-S016.
- PDC-002 remains covered by Cases 2–5 and PDC-S003..PDC-S009.
- PDC-003 remains covered by Cases 11 and 22 plus PDC-S040..PDC-S041.
- PDC-004 is covered by Cases 5, 8–9, and 21 plus PDC-S006..PDC-S009,
  PDC-S016..PDC-S021.
- PDC-005 is covered by Cases 10 and 20–21 plus PDC-S027..PDC-S028,
  PDC-S037..PDC-S039.
- PDC-006 is covered by Cases 11–13 plus PDC-S024..PDC-S026.
- PDC-007 is covered by Cases 14–15 and 19 plus PDC-S022..PDC-S025,
  PDC-S035..PDC-S036.
- PDC-008 is covered by Cases 16–18 plus PDC-S029..PDC-S032.
- Case 22 is a staging-only integrity check. The candidate deliberately does not
  update catalog result fields and does not invoke formal `$skill-test`.
