# Skill Spec: `$team-narrative`

> **Category**: team
> **Priority**: medium
> **Spec revision**: P1 TN-004..TN-014
> **Spec written**: 2026-07-23

## Skill Summary

`$team-narrative` validates a bounded canon graph, records explicit product canon
decisions, freezes a verified canon baseline, collects mode-bounded read-only
brief/dialogue/art/level proposals, and renders every final artifact byte before
content approval and mutation authorization. Unique owners write disjoint paths;
localization review uses actual UX/string sources; immutable checkpoints support
idempotent recovery; and a fresh narrative-specific reviewer binds the final
artifact-set revision. Partial, late, unreviewed, or localization-blocked work never
becomes COMPLETE or a downstream localization handoff.

---

## P1 Closure Matrix

| P1 ID | Audit issue | Required closure |
|---|---|---|
| TN-004 | TNR-006 unknown first changeset | Complete candidate path/preimage/revision/owner manifest before approval |
| TN-005 | TNR-007 dangling review mode | Exact full/lean/solo role substitutions and quality ceilings |
| TN-006 | TNR-008 unbounded “full context” | Hard file/byte/node/edge/depth/entity budgets and fail-closed graph |
| TN-007 | TNR-009 evidence-free COMPLETE | Final paths/revisions/owners, zero blockers, authorization, localization, checkpoint, and review receipt |
| TN-008 | TNR-010 missing PARTIAL state | Typed PARTIAL/BLOCKED readiness and handoff prohibitions |
| TN-009 | TNR-011 no attempt control | Deadlines, one no-write retry, cancellation, revoked tokens, late quarantine |
| TN-010 | TNR-012 no resumable state | Append-only checkpoint chain and revision/CAS-validated idempotent resume |
| TN-011 | TNR-013 unilateral canon finalization | Product decision, separate promotion approval/authorization, registry receipt, freeze revision |
| TN-012 | TNR-014 invented 120-character gate | Per-surface authoritative UX/string constraints; UNKNOWN assumptions cannot pass |
| TN-013 | TNR-015 role drift | One role/phase matrix aligned across SKILL, metadata, and spec |
| TN-014 | TNR-016 unverified localize syntax | Versioned handoff contract and exact ready manifest; no automatic invocation |

---

## Static Assertions

- [ ] **TN-S001** — YAML frontmatter contains only `name` and non-empty `description`; `name` is exactly `team-narrative`.
- [ ] **TN-S002** — Invocation requires `--manifest` and accepts only optional exact `--resume`; no manifest has zero reads, delegates, prompts, approvals, or writes.
- [ ] **TN-S003** — Request schema is `cgs.team-narrative-request/v2` with stable content/run IDs, create/revise mode, exact artifact IDs/paths, authorities, revisions, limits, deadlines, and evidence roots.
- [ ] **TN-S004** — Unsafe/aliased/escaped paths, duplicate IDs/destinations, conflicting writers, missing revise targets, occupied create targets, and raised limits fail before side effects.
- [ ] **TN-S005** — Canon validation and explicit product decisions precede every canon-dependent narrative-director, writer, art-director, and level-designer task.
- [ ] **TN-S006** — Only a verified `CANON_FROZEN` checkpoint with canonical sorted canon-baseline revision opens dependent proposal work.
- [ ] **TN-S007** — Parallel delegates are read-only, use exact context/revision/token/prohibited-path inputs, have no nested delegation, and cannot write operational records.
- [ ] **TN-S008** — Each normalized artifact path has one writer; shared registries/manifests have one sequential recorder; writer path sets are disjoint.
- [ ] **TN-S009** — `cgs.narrative-artifact-plan/v2` lists every artifact ID/type/path/operation/preimage/full candidate revision/owner/dependency/limit/non-write before content approval.
- [ ] **TN-S010** — Unknown suggested paths are excluded until a revised request, complete re-render, new plan approval, and new mutation authorization.
- [ ] **TN-S011** — Content-plan approval and mutation authorization are separate exact revision-bound records; neither canon decision nor proposal approval authorizes a write.
- [ ] **TN-S012** — `cgs.narrative-role-matrix/v2` enumerates phase, role, mode state, identity, scope, deadlines, retry, omission effect, and reviewer independence.
- [ ] **TN-S013** — Full mode explicitly includes world-builder, narrative-director author, conditional writer/art-director/level-designer, localization-lead, and fresh independent narrative reviewer.
- [ ] **TN-S014** — Lean mode specifies coordinator substitutions and makes requested omitted art/level artifacts PARTIAL; solo invokes zero agents, is planning-only, writes no canon/content, and cannot COMPLETE.
- [ ] **TN-S015** — Hard context maxima are 48 files, 2,097,152 bytes, 256 canon nodes, 512 edges, graph depth 8, 64 characters, 64 locations, 32 factions, 64 private truths, 500 strings, 128 triggers, and eight source groups.
- [ ] **TN-S016** — Sources are inventoried before full-read, never truncated, and graph traversal is limited to declared roots/direct stable-ID references with cycle/omission evidence.
- [ ] **TN-S017** — Canon evidence overflow/missing/ambiguity/cycle blocks freeze; optional non-canon overflow yields PARTIAL and excludes dependent artifacts from authorization.
- [ ] **TN-S018** — Operational evidence is create-only under one content/run root and includes context, roles, decisions, plans, ownership, checkpoints, reviews, and results.
- [ ] **TN-S019** — Stable NCF/NCP/LOC/NRF/TNC IDs and finding status/evidence/owner/destination/acceptance/resolution fields support deterministic reruns.
- [ ] **TN-S020** — Maximum active proposal agents is 3, attempt deadline 15 minutes, proposal phase deadline 30 minutes, total attempts 10, one retry, and no nested delegation.
- [ ] **TN-S021** — Retry is allowed only after proving the revoked attempt wrote nothing and uses a new token/input snapshot.
- [ ] **TN-S022** — Timeout/cancel/invalid/side-effect revokes the token, cancels dependents, scans prohibited/target preimages, and makes late output quarantined and unusable.
- [ ] **TN-S023** — Detected late writes are preserved as exact evidence, never auto-reverted, and prevent COMPLETE.
- [ ] **TN-S024** — `cgs.team-narrative-checkpoint/v2` is append-only, predecessor-revision chained, phase typed, and records inputs/outputs/decisions/authorizations/attempts/blockers/next phase.
- [ ] **TN-S025** — Resume binds exact checkpoint path/revision and revalidates chain, IDs, mode, sources, canon, targets, authorizations, tokens, and late writes before continuing.
- [ ] **TN-S026** — Resume never silently restarts/replays writes/reuses stale proposals or review; completed verified work is no-op and pending tasks receive new tokens.
- [ ] **TN-S027** — `cgs.canon-product-decision/v2` binds source-backed options, decision-maker, rationale, affected IDs/paths/revisions, and timestamp.
- [ ] **TN-S028** — `cgs.canon-promotion-plan/v2` renders all canon/registry candidate bytes and unique owners before separate plan approval and mutation authorization.
- [ ] **TN-S029** — Canon promotion uses source/target/registry/decision/authorization/role CAS, sequential unique writers, read-back, registry verification, and `cgs.canon-promotion-receipt/v2`.
- [ ] **TN-S030** — World-builder or coordinator cannot unilaterally finalize canon; no downstream proposal starts after partial/unreceipted promotion.
- [ ] **TN-S031** — `cgs.narrative-string-constraint-manifest/v2` binds every string to its actual UI surface/control/source revision, formatter grammar, locale profile, and content/spoiler policy.
- [ ] **TN-S032** — Universal 120-character limits and generic expansion percentages are prohibited substitutes; assumptions remain UNKNOWN with owner/test plan.
- [ ] **TN-S033** — Blocking or UNKNOWN required localization findings produce `NOT_LOCALIZATION_READY` and PARTIAL regardless of risk acceptance.
- [ ] **TN-S034** — `cgs.localization-handoff-contract/v1` is required to validate receiving schema/version, manifest/revision, source locale/string IDs, readiness receipt, spoiler exclusions, output ownership, and availability.
- [ ] **TN-S035** — `cgs.narrative-localization-handoff/v2` is read-only; missing/stale/incompatible/unavailable interface yields `LOCALIZATION_HANDOFF_UNVERIFIED`, no guessed `$localize extract`, and no automatic invocation.
- [ ] **TN-S035A** — The handoff exposes the exact `cgs.narrative-localization-handoff-v2-adapter/v1` tuple: current contract/authority, canon sources/baseline, final story-artifact manifest and rows, context/source revisions, string constraints/IDs, LOCALIZATION_READY review with empty blocking/unknown lists, protected-content exclusions, destination ownership/preimages, recipient availability, and explicit payload revision and stable handoff business ID plus UTC run ID.
- [ ] **TN-S036** — Source/canon, target/ownership, review/approval/role, checkpoint/token CAS all pass in one pre-write pass; mismatch means zero new content writes.
- [ ] **TN-S037** — Writes are unique-owner, exact-scope, dependency-ordered, per-path atomic where supported, and immediately read back; whole-set atomicity/rollback is not claimed.
- [ ] **TN-S038** — Partial writes produce exact applied/no-op/not-applied/conflict/unknown preimage/candidate/observed evidence and require fresh recovery authorization.
- [ ] **TN-S039** — Final artifact manifest is canonical/sorted and its revision is the only `final_artifact_set_revision` used by final review and completion.
- [ ] **TN-S040** — Final reviewer is fresh, read-only, identity-independent, and uses only the narrative-specific canon/voice/arc/trigger/truth/localization/rating/reference profile.
- [ ] **TN-S041** — Post-review fixes stale prior evidence, require re-read and fresh scoped dependent review, and allow at most two fix/re-review rounds.
- [ ] **TN-S042** — No system-GDD review workflow is invoked or recommended for narrative artifacts.
- [ ] **TN-S043** — `cgs.team-narrative-result/v2` records artifact paths/revisions/owners, canon/final revisions, approvals, authorization, checkpoint, localization/hand-off/reviewer evidence, attempts, blockers, and exactly one next action.
- [ ] **TN-S044** — COMPLETE requires current artifacts, revisions, unique owners, LOCALIZATION_READY, independent final-revision review, valid chains/receipts, zero blockers/stale/late evidence, and required handoff verification.
- [ ] **TN-S045** — PARTIAL and BLOCKED have explicit semantics/readiness labels and cannot enter localization, assets, or implementation.
- [ ] **TN-S046** — Metadata names bounded canon-safe narrative, narrative/dialogue/art/level/localization proposals, single-owner authorization, and independent final review without omitting implemented roles.

---

## Behavioral Test Cases

### Case 1: No manifest is inert

**Input**: `$team-narrative`

**Expected behavior**: Print exact manifest/resume usage and stop.

**Assertions**:

- [ ] No repository path is discovered or read.
- [ ] No delegate, user decision, approval, authorization, checkpoint, or write occurs.
- [ ] No topic/content ID is inferred.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Request identity and path safety fail closed

**Fixture variants**: duplicate content/artifact ID, unsafe path, two writers for one
normalized path, missing revise target, occupied create target, source/target alias,
or context limit above contract.

**Expected behavior**:

1. The exact invalid field/path/identity is reported before source loading.
2. No best-effort normalization or overwrite occurs.
3. Verdict is BLOCKED with one correction action.

**Assertions**:

- [ ] Create and revise semantics remain distinct.
- [ ] Symlink/junction escape is rejected.
- [ ] Zero files and agents are affected.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Canon contradiction blocks all dependent creators

**Fixture**: Canon says a city is 200 years old; the requested brief says 50.

**Expected behavior**:

1. Read-only canon validation returns a stable NCF finding with both source revisions.
2. The canon authority receives source-backed choices.
3. Narrative-director dependent brief, writer, art-director, and level-designer are
   not launched until a verified decision/promotion and CANON_FROZEN checkpoint.

**Assertions**:

- [ ] No speculative dependent proposal is accepted.
- [ ] Coordinator/world-builder does not choose canon.
- [ ] Skipping the contradiction cannot produce COMPLETE.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: No-change canon freeze is reproducible

**Fixture**: Canon validation finds no required mutation and every declared canon
source/registry revision is current.

**Expected behavior**:

1. Product no-change decision and sorted canon manifest are recorded.
2. re-reading yields one deterministic canon-baseline revision.
3. CANON_FROZEN checkpoint binds the decision, manifest, and role/context revisions.

**Assertions**:

- [ ] No canon file is rewritten for activity.
- [ ] Any later canon revision drift stales downstream proposals.
- [ ] The freeze is not inferred from reviewer approval alone.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Canon promotion is a separately authorized product transaction

**Fixture**: A product decision creates a canon fact and registry ID.

**Expected behavior**:

1. Every fact/registry candidate byte, path, owner, preimage, revision, order, and
   non-write is rendered before promotion approval.
2. Canon authority approves content; mutation authority separately authorizes the
   exact set.
3. One canon writer and one registry recorder write sequentially under CAS/read-back.
4. A verified promotion receipt is required before CANON_FROZEN.

**Assertions**:

- [ ] World-builder cannot finalize canon.
- [ ] Registry has one recorder and matches artifact IDs/revisions.
- [ ] Partial/unreceipted promotion blocks dependent proposals.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Exact first content changeset is known before approval

**Fixture**: Frozen canon yields dialogue, lore, art-brief, and trigger proposals;
one proposal suggests an undeclared glossary.

**Expected behavior**:

1. Complete candidate bytes and revisions are rendered for every declared artifact.
2. The exact path/operation/preimage/candidate/owner/dependency matrix is shown.
3. Suggested glossary is excluded until a revised request/re-render/approval.
4. Only then may content-plan approval occur; writes still await authorization.

**Assertions**:

- [ ] No wildcard or future path is pre-approved.
- [ ] Concept approval writes nothing.
- [ ] Scope expansion invalidates old approval/authorization.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Parallel proposals are zero-write and uniquely routed

**Fixture**: Writer, art-director, and level-designer propose concurrently; two
suggest the same summary file.

**Expected behavior**:

1. At most three read-only attempts receive the same canon revision and disjoint slices.
2. Overlapping destination ownership is rejected or routed through one recorder.
3. Writes occur only later through unique authorized owners.

**Assertions**:

- [ ] Proposal agents write no project or operational file.
- [ ] Shared path has exactly one recorder.
- [ ] Every final path appears once in ownership manifest.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Full mode role matrix is complete

**Fixture**: Request includes dialogue, visual brief, trigger contract, localizable
strings, and final delivery.

**Expected behavior**:

1. Matrix marks world-builder, narrative-director author, writer, art-director,
   level-designer, localization-lead, and independent reviewer required.
2. Each role has identity, phase, read/write scope, deadline, retry, and omission
   effect.
3. Final reviewer differs from every author/editor/writer/recorder/approver.

**Assertions**:

- [ ] SKILL, metadata, and spec role list agree.
- [ ] No mode label exists without behavioral effect.
- [ ] Every delegate is read-only.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Lean mode has explicit quality ceilings

**Fixture variants**: dialogue-only request; request also includes visual/level
artifacts.

**Expected behavior**:

1. World-builder, localization-lead for strings, and independent reviewer remain
   required; coordinator substitutions are disclosed.
2. Dialogue-only may complete if all other gates pass.
3. Requested art/level artifacts lack their skipped specialists, remain excluded,
   and force PARTIAL.

**Assertions**:

- [ ] Skipped role is not recorded as passed.
- [ ] Omission names affected artifact IDs and next action.
- [ ] Mode cannot change mid-run silently.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Solo mode is planning-only

**Fixture**: A valid solo request includes localizable dialogue.

**Expected behavior**:

1. Zero agents are invoked.
2. Coordinator may produce bounded read-only draft evidence only.
3. No canon/content write occurs; status includes NOT_LOCALIZATION_READY and
   NOT_INDEPENDENTLY_REVIEWED; verdict is PARTIAL/BLOCKED.

**Assertions**:

- [ ] Solo can never COMPLETE.
- [ ] Solo cannot promote canon.
- [ ] Missing independent roles are explicitly recorded.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 11: Canon graph budgets and cycles are enforced

**Fixture variants**: file 49, byte 2,097,153, node 257, edge 513, depth 9, entity
count overflow, cycle, missing stable reference, and optional non-canon overflow.

**Expected behavior**:

1. Inventory/count occurs before over-limit full-read; no source is truncated.
2. Canon failure/overflow blocks freeze; optional non-canon overflow produces
   PARTIAL and excludes dependents.
3. Context manifest records exact boundary, omissions, graph, and revisions.

**Assertions**:

- [ ] Request cannot raise any hard maximum.
- [ ] Whole-repository recursion is not used.
- [ ] Partial graph never becomes CANON_FROZEN.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 12: Timeout, cancellation, retry, and late result are bounded

**Fixture**: Art-director exceeds 15 minutes, is canceled, then returns a patch.

**Expected behavior**:

1. Token is revoked, dependents canceled, and target/prohibited preimages checked.
2. One retry is allowed only after proving the old attempt wrote nothing; it uses a
   new token.
3. Late result is quarantined and never merged/written/reviewed.
4. Remaining failure yields PARTIAL checkpoint; no indefinite wait occurs.

**Assertions**:

- [ ] Proposal phase stops by 30 minutes and run has at most 10 delegate attempts.
- [ ] Late write evidence is preserved, not automatically reverted.
- [ ] Side-effecting attempt is never retried automatically.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 13: Resume is checkpoint-bound and idempotent

**Fixture**: A PARTIAL PROPOSALS_READY checkpoint has two valid proposals, one
revoked attempt, exact manifests, and one pending proposal.

**Expected behavior**:

1. Resume validates the complete linear checkpoint chain and every bound revision,
   identity, authorization, token, canon, target, and late-write state.
2. Valid completed proposals are no-op; only pending work receives a new token.
3. Drift/fork/gap/overwritten checkpoint blocks without silent restart.

**Assertions**:

- [ ] Completed writes are never replayed.
- [ ] Stale review/proposal cannot be reused.
- [ ] Next phase equals recorded `next_safe_phase` only when prerequisites hold.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 14: Actual UI/string constraints drive localization review

**Fixture**: Dialogue maps to two UI surfaces with distinct current pixel/line/
markup/formatter/locale profiles.

**Expected behavior**:

1. Constraint manifest binds each string/surface/control to actual source revision.
2. Review applies the correct surface-specific rules and locale profile.
3. Formatter, plurals, grammar, dates, concatenation, rating, and spoiler checks are
   evidence-bound.

**Assertions**:

- [ ] No universal 120-character rule appears.
- [ ] No generic expansion percentage substitutes for source evidence.
- [ ] Every passed string has stable ID and current constraint revision.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 15: Missing constraint may be a test assumption, never a hard gate

**Fixture**: A dialogue surface lacks authoritative UX/string constraints.

**Expected behavior**:

1. An assumption may record owner, rationale, provisional test, and validation plan.
2. Required constraint status remains UNKNOWN.
3. Localization status is NOT_LOCALIZATION_READY and verdict PARTIAL/BLOCKED until
   authoritative evidence replaces it and review reruns.

**Assertions**:

- [ ] Assumption is not represented as shipping truth.
- [ ] Risk acceptance cannot change readiness.
- [ ] COMPLETE and localization handoff are impossible.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 16: Blocking localization defect cannot be waived

**Fixture**: One string hardcodes an English date without formatter contract.

**Expected behavior**:

1. Stable blocking LOC finding binds string/artifact/source revisions and owner action.
2. Only unique owner may fix within authorized candidate set; changed bytes require
   re-read, localization re-review, and final scoped review.
3. If unresolved, result is PARTIAL + NOT_LOCALIZATION_READY even when risk is
   accepted.

**Assertions**:

- [ ] No COMPLETE/localization/implementation handoff is emitted.
- [ ] Business decision does not downgrade blocker severity.
- [ ] Unauthorized auto-fix is forbidden.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 17: Valid localization handoff is exact and read-only

**Fixture**: Current handoff contract accepts the final artifact-manifest schema;
LOCALIZATION_READY receipt has zero blockers and exact string IDs/source locale.

**Expected behavior**:

1. Handoff candidate binds contract version/revision, artifact manifest/revision,
   readiness evidence, string order, spoiler exclusions, and output ownership.
2. Exact canon sources/baseline, story-artifact rows, context/source bindings,
   caller authority, recipient availability, and payload revision all validate against explicit producer metadata.
3. The payload carries an explicit monotonic revision, while handoff_id is NLOC-<canon-id>-<artifact-set-id>-<UTC-run-id>; neither field is content-derived or self-referential.
4. Path-bound use requires read-back-verified durable string-constraint,
   final-artifact, and handoff records from the pre-authorized recorder.
5. It may be offered as one post-COMPLETE next action.
6. This workflow does not invoke localization.

**Assertions**:

- [ ] Private truth payload is excluded.
- [ ] No guessed command syntax is emitted.
- [ ] Handoff recipient availability is evidenced.
- [ ] Every adapter field and raw/canonical revision reproduces from current sources.
- [ ] Request and contract caller-authority identities are equal.
- [ ] Conversation-only or missing prerequisite manifests cannot be consumed as a
      path-bound localize input.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 18: Missing or incompatible localization interface blocks required handoff

**Fixture variants**: interface absent, stale revision, unsupported manifest version,
unavailable receiver, missing readiness field, or destination ownership conflict.

**Expected behavior**:

1. State is LOCALIZATION_HANDOFF_UNVERIFIED with exact failure evidence.
2. Required localization delivery makes verdict PARTIAL.
3. No `$localize extract`, invocation, or downstream write occurs.

**Assertions**:

- [ ] Interface is never inferred from skill name.
- [ ] Content readiness does not prove transport compatibility.
- [ ] Exactly one interface-resolution action is offered.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 19: Private mystery truth never enters handoff or public artifacts

**Fixture**: Public dialogue references a confidential mystery answer.

**Expected behavior**:

1. Answer exists only in authorized private canon artifact; public files use truth ID.
2. Read-back and review verify access/spoiler partition and truth coverage.
3. Localization handoff excludes protected answer and operational excerpts.

**Assertions**:

- [ ] Public leak is a blocker.
- [ ] Orphan truth ID prevents COMPLETE.
- [ ] Reviewer checks proposal/review/record payloads for leakage.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 20: Content approval, authorization, and CAS are distinct

**Fixture**: Exact plan is approved and authorized; before first write independently
change source, canon, target, owner, constraint, approval, checkpoint head, writer,
or attempt-token state.

**Expected behavior**:

1. One-pass CAS detects the exact mismatch.
2. Zero new content writes occur.
3. Changed plan/scope/bytes require fresh render, approval, and authorization.

**Assertions**:

- [ ] Approval alone never mutates.
- [ ] Authorization includes no unknown future path.
- [ ] Non-write paths remain unchanged.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 21: Mid-set write failure remains PARTIAL

**Fixture**: First artifact writes/verifies; second write fails; shared manifest has
not yet written.

**Expected behavior**:

1. Ordinary writes stop; no destructive rollback or atomic-set claim occurs.
2. Applied/no-op/not-applied/conflict/unknown states bind exact revisions.
3. Authorized PARTIAL checkpoint/result is attempted; receipt failure reports an
   unreceipted changed set.
4. Recovery requires fresh full inventory and authorization.

**Assertions**:

- [ ] Accepted proposal is not counted as delivered.
- [ ] Shared manifest does not claim failed prerequisites.
- [ ] COMPLETE is impossible.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 22: Independent review follows final polish revisions

**Fixture**: Initial review finds a voice blocker; owner applies authorized fix.

**Expected behavior**:

1. Reviewer is fresh/read-only/independent and binds current canon/final revisions.
2. Fix stales old review; complete artifact set is re-read.
3. Exact fix bytes enter a versioned plan with fresh approval/authorization unless
   current authorization already binds those exact bytes.
4. Fresh scoped review covers changed dialogue plus declared dependents.
5. At most two fix/re-review rounds occur; remaining blocker is PARTIAL/BLOCKED.

**Assertions**:

- [ ] Author cannot self-approve.
- [ ] Review before final write cannot satisfy completion.
- [ ] No third fix round or loop-until-pass occurs.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 23: Narrative profile replaces system-GDD review

**Fixture**: Final artifacts include dialogue, arc, trigger contract, private truth,
and localizable strings.

**Expected behavior**: Review covers NR-CANON, NR-VOICE, NR-ARC, NR-TRIGGER,
NR-TRUTH, NR-LOC, NR-RATING, and NR-REF against final revisions.

**Assertions**:

- [ ] Required PARTIAL profile check makes whole review PARTIAL.
- [ ] NRF findings bind artifact/evidence/owner/destination/acceptance/resolution.
- [ ] No system-GDD reviewer is invoked or recommended.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 24: COMPLETE has exact evidence; PARTIAL cannot masquerade

**Fixture variants**:

- Every required artifact, receipt, role, localization gate, review, checkpoint,
  revision, and handoff condition succeeds.
- One blocker, omitted role, late result, stale revision, unverified handoff, or failed
  evidence write remains.

**Expected behavior**:

1. First variant emits COMPLETE result with artifact path/revision/owner table, canon/
   final revisions, approvals, authorization, localization/handoff/reviewer evidence,
   zero blockers, and exactly one next action.
2. Second variant emits PARTIAL/BLOCKED with readiness labels and exact evidence.
3. Neither variant starts a downstream workflow.

**Assertions**:

- [ ] Process completion alone is insufficient.
- [ ] Result receipt is read back and current.
- [ ] PARTIAL cannot enter localization/assets/implementation.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 25: Staged package and catalog remain integration-honest

**Fixture**: Inspect the P1 candidate without invoking formal `$skill-test`.

**Expected behavior**:

1. Formal mirror contains SKILL, metadata, exclusive spec, and both private
   references.
2. Live skill/spec/metadata, old P0 staging, shared docs, and catalog remain
   byte-identical.
3. Catalog result fields remain empty until authorized formal evaluation.

**Assertions**:

- [ ] Every staged file has exact byte count and revision.
- [ ] No staged catalog/shared-doc edit exists.
- [ ] No project workflow was invoked.

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Cross-Artifact Checks

- [ ] **TN-X001** — Request content/run/artifact IDs and destination paths agree
  across context, roles, proposals, artifact/ownership plans, authorization,
  checkpoints, final manifest, reviews, handoff, and result.
- [ ] **TN-X002** — Canon source/registry revisions, product decision, promotion
  receipt, CANON_FROZEN checkpoint, all proposal inputs, final manifest, and review
  bind the same canon-baseline revision.
- [ ] **TN-X003** — Every artifact path maps to exactly one writer/owner and every
  candidate/final/preimage revision agrees across plan, authorization, write evidence,
  final manifest, review, and result.
- [ ] **TN-X004** — Role matrix, attempt records, checkpoint tokens, mode omissions,
  metadata role claims, and spec expectations agree exactly.
- [ ] **TN-X005** — String IDs, surfaces, actual constraint-source revisions,
  localization findings/readiness, final artifact manifest, and handoff candidate
  refer to the same ordered current string set.
- [ ] **TN-X006** — Private truth IDs/access classes agree across canon, public
  references, proposal evidence, review, and localization exclusions without answer
  leakage.
- [ ] **TN-X007** — Checkpoint/result predecessor revisions, sequences, phases,
  completed/pending work, target observations, and next safe phase form one linear
  immutable chain.
- [ ] **TN-X008** — Reviewer identity/token is disjoint from author/editor/writer/
  recorder/decision/approval identities and its canon/final revisions equal current
  read-back revisions.
- [ ] **TN-X009** — Every PARTIAL/BLOCKED condition appears in result readiness,
  open findings/blockers, checkpoint next phase, and exactly one next action; none
  appears as COMPLETE or a downstream handoff.
- [ ] **TN-X010** — The staged candidate contains no catalog/shared-document copy,
  and live/P0/catalog revisions equal their frozen pre-edit snapshots.

---

## Protocol Compliance

- [ ] Open canon/voice/arc/risk choices follow Question → Options → Decision →
  Draft → Approval; mechanical phase progression does not prompt repeatedly.
- [ ] Canon promotion and narrative content have separate exact approval and
  authorization records.
- [ ] No write occurs before complete path/owner/preimage/candidate inventory and
  all applicable CAS gates.
- [ ] Parallel work is proposal-only, bounded, cancelable, retry-limited, and immune
  to late-output adoption.
- [ ] Final changes always stale prior review until re-read and fresh independent
  scoped review.
- [ ] COMPLETE, PARTIAL, and BLOCKED remain evidence states, not user-preference
  labels.
- [ ] Exactly one legal next action is returned; no downstream workflow is invoked.

---

## Coverage Notes

- TN-004 / audit TNR-006: Cases 6–7, 20 and TN-S009..TN-S011.
- TN-005 / audit TNR-007: Cases 8–10 and TN-S012..TN-S014.
- TN-006 / audit TNR-008: Case 11 and TN-S015..TN-S017.
- TN-007 / audit TNR-009: Case 24 and TN-S039, TN-S043..TN-S044.
- TN-008 / audit TNR-010: Cases 12, 15–16, 18, 21, 24 and TN-S022..TN-S023,
  TN-S033, TN-S038, TN-S045.
- TN-009 / audit TNR-011: Case 12 and TN-S020..TN-S023.
- TN-010 / audit TNR-012: Case 13 and TN-S018, TN-S024..TN-S026.
- TN-011 / audit TNR-013: Cases 4–5 and TN-S027..TN-S030.
- TN-012 / audit TNR-014: Cases 14–16 and TN-S031..TN-S033.
- TN-013 / audit TNR-015: Cases 8–10, 25 and TN-S012..TN-S014, TN-S046.
- TN-014 / audit TNR-016: Cases 17–18 and TN-S034..TN-S035A.
- P0 canon ordering, unique ownership, independent post-polish review,
  localization-blocker gating, and narrative-specific review remain covered by
  Cases 3, 5, 7, 16, 22, and 23.
- Case 25 is staging-only. This candidate does not update shared catalog/docs and
  does not invoke formal `$skill-test`.
