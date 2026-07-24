# Skill Test Spec: $ux-design

## Skill Summary

$ux-design authors exactly one versioned ux-spec, hud-design, or
interaction-pattern-library artifact from cgs.ux-design-request/v2. The author
uses ux-profile-schema-v2, cgs.ux-content-profile/v2, bounded current evidence,
decision/revision provenance, compare-and-set writes, immutable checkpoint v2
records, and a final cgs.ux-authoring-receipt/v1.

The target plus authorized checkpoint root are the only writes. Authoring stops
at DRAFT, PARTIAL, BLOCKED, ERROR, or READY_FOR_REVIEW and never represents
independent approval or implementation readiness.

---

## Static Assertions

- [ ] UXD-S001: Frontmatter contains only matching name and non-empty description
- [ ] UXD-S002: Invocation requires exact manifest; no-arg stops before repository read
- [ ] UXD-S003: Request contract is cgs.ux-design-request/v2
- [ ] UXD-S004: Author schema hashes exact SKILL, NUL, and continuation bytes
- [ ] UXD-S005: Profile version is ux-profile-schema-v2
- [ ] UXD-S006: Content profile is cgs.ux-content-profile/v2
- [ ] UXD-S007: ux-spec, HUD, and pattern profiles have stable IDs and exact headings
- [ ] UXD-S008: Artifact header records profile/content/author schema and stable artifact/screen IDs
- [ ] UXD-S009: Header records platform profile ID, version, SHA-256, input IDs, and stable receipt ID without receipt hash self-reference
- [ ] UXD-S010: Temporary platform answers are PROVISIONAL and cannot produce READY
- [ ] UXD-S011: Modes are create/fill-gaps/revise-sections/migrate-schema
- [ ] UXD-S012: Section content/evidence/workflow/assertion state axes are separate
- [ ] UXD-S013: fill-gaps cannot rewrite substantive content
- [ ] UXD-S014: revise-sections may explicitly revise substantive CURRENT/STALE content
- [ ] UXD-S015: Migration preserves hashes and blocks on unmappable fragments
- [ ] UXD-S016: One mutation authorization covers exact target/checkpoint/sections
- [ ] UXD-S017: Per-section product approval never reauthorizes files
- [ ] UXD-S018: Context selection order is fixed with hard 16-file/524288-byte limits
- [ ] UXD-S019: Context overflow may write only authorized PARTIAL checkpoint and not target
- [ ] UXD-S020: Four decision classes match other P1 authoring contracts
- [ ] UXD-S021: Revision records bind before/after target/section/source/authorization hashes
- [ ] UXD-S022: Every target write uses target, section, context, authorization, writer CAS
- [ ] UXD-S023: Platform/accessibility/global pattern owners remain external
- [ ] UXD-S024: Cross-reference findings use cgs.ux-dependency-finding/v1 stable state
- [ ] UXD-S025: BLOCKING WAIVED remains unresolved and prevents READY
- [ ] UXD-S026: Acceptance criteria reference requirement/decision IDs without copying product rules
- [ ] UXD-S027: Consultation is one/section, three/run, two concurrent, one 60-second attempt, no retry/delegation
- [ ] UXD-S028: Checkpoints use cgs.ux-design-checkpoint/v2 append-only predecessor CAS
- [ ] UXD-S029: Final receipt is cgs.ux-authoring-receipt/v1 and is not approval
- [ ] UXD-S030: Author statuses exclude COMPLETE, APPROVED, IMPLEMENTATION READY
- [ ] UXD-S031: Fresh independent review handoff binds target/schema/context/receipt hashes
- [ ] UXD-S032: Metadata names UX consistently and describes all three profile boundaries

---

## Behavioral Cases

### Case 1: no argument has zero side effects

**Input:**

    $ux-design

**Expected behavior:** print exact manifest usage and stop.

**Assertions:**

- [ ] UXD-C01-A: No repository file/context is read
- [ ] UXD-C01-B: No decision, authorization, delegation, checkpoint, or verdict
- [ ] UXD-C01-C: Artifact/profile/target is not guessed

---

### Case 2: fresh screen uses profile/content v2

**Fixture:** valid create request names screen inventory, absent exact target,
owned requirement IDs, current platform/accessibility profiles, one-hop
navigation, budgets, identities, mutation boundary, and checkpoint root.

**Expected behavior:**

1. CLI/request/target/profile identity validates before context questions.
2. UXS-01..14 skeleton and complete header are planned.
3. One mutation authorization covers target/checkpoints/all required sections.
4. Stable ordered context fits hard budgets.
5. Sections use decisions, semantic preflight, approval, CAS, revision,
   checkpoint.
6. Content/cross-reference checks pass; final receipt revalidates.
7. READY_FOR_REVIEW handoff names exact target/receipt hashes.

**Assertions:**

- [ ] UXD-C02-A: All IDs/headings/assertions occur exactly once
- [ ] UXD-C02-B: Actual author identity differs from decision provenance
- [ ] UXD-C02-C: Only target/checkpoint records are written
- [ ] UXD-C02-D: No per-section file permission prompt

---

### Case 3: HUD and pattern profiles remain distinct

**Fixture:** separate valid requests target hud.md and
interaction-patterns.md.

**Expected behavior:**

- HUD uses HUD-01..08, stable screen hud, declared platform/input variants.
- Pattern uses PAT-01..05, external library owner, UXP-GLOBAL IDs.
- One run never writes both targets.

**Assertions:**

- [ ] UXD-C03-A: ux-spec headings are not imposed on HUD/pattern
- [ ] UXD-C03-B: Screen/HUD cannot merge global pattern
- [ ] UXD-C03-C: Dedicated pattern run uses pattern-entry CAS

---

### Case 4: fill-gaps and revise-sections use content/evidence state

**Fixture:** UXS-01/03 are SUBSTANTIVE/CURRENT; UXS-06 PLACEHOLDER;
UXS-11 SUBSTANTIVE/STALE; UXS-12 MISSING.

**Expected behavior:**

- fill-gaps can select UXS-06/12 only.
- revise-sections may select explicit UXS-11 and update its source evidence.
- Unselected bodies remain byte-identical.
- Validation uses assertion results and evidence hashes, not placeholder text
  alone.

**Assertions:**

- [ ] UXD-C04-A: Complete sections can be revised explicitly
- [ ] UXD-C04-B: fill-gaps cannot use weakness as rewrite permission
- [ ] UXD-C04-C: VALID/STALE semantics are current-source-bound

---

### Case 5: legacy migration is deterministic and lossless

**Fixture:** legacy headings include substantive content, one duplicate mapping,
and one unmappable fragment.

**Expected behavior:**

1. migrate-schema records old heading/content hashes and stable-ID mappings.
2. Approved moves preserve exact bytes where not edited.
3. Duplicate/unmappable content becomes blocking decision/finding.
4. No silent drop, duplication, or automatic rewrite.

**Assertions:**

- [ ] UXD-C05-A: Schema mismatch on resume requires migration
- [ ] UXD-C05-B: Unresolved fragment prevents READY
- [ ] UXD-C05-C: Migration revisions retain before/after provenance

---

### Case 6: bounded context order and overflow are reproducible

**Fixture:** declared required context would exceed 16 files or 524288 bytes
after one-hop neighbors.

**Expected behavior:**

1. Candidate order follows instructions, target, platform, accessibility,
   requirements, neighbors, patterns, journey, art.
2. No second-hop/fuzzy/global scan or partial file read.
3. Authorized checkpoint records loaded/omitted path/role/IDs/bytes/hash/reason
   and CONTEXT_BUDGET_EXCEEDED.
4. Target remains unchanged and result PARTIAL.

**Assertions:**

- [ ] UXD-C06-A: Same inputs produce same manifest digest
- [ ] UXD-C06-B: Manifest-requested budget cannot exceed hard cap
- [ ] UXD-C06-C: Required omission is never silently accepted

---

### Case 7: target resolves before context and questions

**Fixture:** variants use invalid manifest schema, ambiguous target identity,
wrong mode/existence, and valid manifest.

**Expected behavior:**

- Invalid inputs stop before broader context or questions.
- Valid request inventories target/profile/scope, obtains one authorization,
  loads bounded context, then asks first product question.

**Assertions:**

- [ ] UXD-C07-A: "Read all before asking" is not used
- [ ] UXD-C07-B: No-arg and invalid manifest behavior are deterministic
- [ ] UXD-C07-C: Target/profile cannot be inferred from context

---

### Case 8: author, decision, and revision provenance are truthful

**Fixture:** user chooses layout option; platform profile imposes hard safe zone;
focus order is derived; engine widget question appears; consultant advises.

**Expected behavior:**

1. Product/hard/derived/technical UXDEC records carry real authority/evidence.
2. User is decision owner but not falsely named target author.
3. Consultant is evidence source only.
4. UXREV binds decision IDs and before/after target/section/source hashes to
   actual writer.

**Assertions:**

- [ ] UXD-C08-A: Every material draft statement has decision provenance
- [ ] UXD-C08-B: Derived reasoning/assumptions remain reproducible
- [ ] UXD-C08-C: Technical question is routed outside artifact

---

### Case 9: platform/input profile is persistent or provisional

**Fixture:** A has current platform profile ID/version/path/hash; B has MISSING
profile and user gives temporary controller/resolution answer.

**Expected behavior:**

- A header/sections reference exact profile and may validate.
- B stores provisional derived decision plus blocking finding and
  DEPENDENCY-GAP; dependent sections are PROVISIONAL, result PARTIAL.
- Temporary answer never masquerades as external platform truth.

**Assertions:**

- [ ] UXD-C09-A: Header includes platform ID/version/hash
- [ ] UXD-C09-B: Missing profile prevents READY
- [ ] UXD-C09-C: Input/resolution assumptions are not conversation-only

---

### Case 10: cross-reference gaps have stable owner/state

**Fixture:** navigation neighbor disagrees, pattern reference is stale, and one
requirement has no owner.

**Expected behavior:**

1. Findings use cgs.ux-dependency-finding/v1 deterministic fingerprints.
2. OPEN records include current evidence, expected/observed, owner,
   destination, acceptance, first/last hashes.
3. Only current resolution evidence may mark RESOLVED.
4. BLOCKING WAIVED remains unresolved; READY prohibited.

**Assertions:**

- [ ] UXD-C10-A: Counts alone are not finding evidence
- [ ] UXD-C10-B: External owner gap cannot be closed by user acceptance
- [ ] UXD-C10-C: IDs persist across re-evaluation

---

### Case 11: acceptance criteria reference sources without shadow truth

**Fixture:** inventory GDD owns requirement INV-042; UX acceptance needs verify
disabled action feedback.

**Expected behavior:**

1. UXAC references INV-042 owner/path/locator/hash and UXDEC IDs.
2. It states local screen precondition, input, observable UX response,
   platform/accessibility variants, evidence method, validation owner.
3. It does not copy/restate inventory product rule.
4. Stale/missing INV-042 blocks instead of inventing.

**Assertions:**

- [ ] UXD-C11-A: Local UX condition is executable with cited requirement loaded
- [ ] UXD-C11-B: AC does not redefine gameplay outcome
- [ ] UXD-C11-C: QA automation/implementation details stay outside

---

### Case 12: consultation cap, timeout, and fallback are deterministic

**Fixture:** optional adviser times out; required accessibility evidence returns
partial; a section requests second adviser; run requests fourth consultation;
late result attempts a patch.

**Expected behavior:**

1. Enforce one/section, three/run, two concurrent, one 60-second attempt.
2. No retry/nested delegation; late/side-effect output quarantined.
3. Optional failure continues only via explicit nondependent product decision.
4. Required non-complete blocks section, appends PARTIAL checkpoint, stops.

**Assertions:**

- [ ] UXD-C12-A: complete/partial/timeout/failed/side-effect/skipped are recorded
- [ ] UXD-C12-B: Input/output hashes and fallback are explicit
- [ ] UXD-C12-C: Consultant never writes/approves/owns foundation

---

### Case 13: one authorization covers many content approvals

**Fixture:** target/checkpoint/sections/writers/limits are authorized once; user
approves three drafts; fourth draft proposes new section/path.

**Expected behavior:**

- First three writes use existing authorization plus CAS, no file reprompt.
- Fourth stops for revised mutation manifest.
- Product approval is recorded as UXDEC, not filesystem authority.

**Assertions:**

- [ ] UXD-C13-A: Scope expansion never inherits prior authorization
- [ ] UXD-C13-B: Each write has read-back and revision/checkpoint evidence
- [ ] UXD-C13-C: Checkpoint path creation was in initial boundary

---

### Case 14: target/context CAS blocks concurrent drift

**Fixture:** target changes after approval in A; platform profile changes in B;
checkpoint sequence is concurrently occupied in C.

**Expected behavior:**

- A returns CONCURRENT TARGET CHANGE with no transaction.
- B returns CONTEXT EVIDENCE CHANGED; dependent section becomes stale.
- C create-if-absent checkpoint CAS fails and never overwrites predecessor.

**Assertions:**

- [ ] UXD-C14-A: Approved draft bytes do not bypass rehash
- [ ] UXD-C14-B: Out-of-scope bytes remain protected
- [ ] UXD-C14-C: Concurrent receipt/checkpoint record is append-only safe

---

### Case 15: resume validates exact checkpoint chain

**Fixture:** interrupted run has approved-not-written UXS-05; one unrelated
source changes in A, dependent source changes in B, target drifts in C.

**Expected behavior:**

- Exact current chain recovers only stored draft bytes.
- A leaves unrelated section current.
- B marks only dependents STALE and reruns decisions/preflight.
- C blocks; schema mismatch requires migrate-schema; old checkpoint errors.

**Assertions:**

- [ ] UXD-C15-A: No write replay
- [ ] UXD-C15-B: Conversation memory is not provenance
- [ ] UXD-C15-C: Next transition comes from verified checkpoint

---

### Case 16: missing critical dependencies cannot be ready

**Fixture:** owned GDD requirement, platform profile, and accessibility
foundation are missing.

**Expected behavior:**

- Stable blocking findings name owners/actions.
- Safe sections may produce DRAFT/PARTIAL only.
- User risk acceptance does not upgrade.
- Workflow creates no missing foundation/global artifact.

**Assertions:**

- [ ] UXD-C16-A: No COMPLETE/READY/APPROVED/implementation-ready claim
- [ ] UXD-C16-B: No platform/accessibility/product behavior is invented
- [ ] UXD-C16-C: One next action resolves one named gap

---

### Case 17: final receipt and independent review remain separate

**Fixture:** all assertions/current dependencies pass and final target hash H1
is stable.

**Expected behavior:**

1. Checkpoint recorder appends cgs.ux-authoring-receipt/v1 binding target
   pre/post, context, decisions/revisions/findings/schema/auth/writer identities.
2. Header names only stable receipt ID; response names external receipt path/hash
   and READY_FOR_REVIEW without a target/receipt self-reference cycle.
3. Fresh reviewer differs from author/recorder and consumes exact H1/schema/
   context/receipt.
4. Author does not review/persist review/start visual or implementation work.
5. If target becomes H2, H1 receipt/review is stale.

**Assertions:**

- [ ] UXD-C17-A: Receipt is authoring evidence, not approval
- [ ] UXD-C17-B: Receipt failure leaves content status intact but workflow PARTIAL, with no review handoff
- [ ] UXD-C17-C: Implementation still needs persisted current review evidence

---

### Case 18: P1 test evidence and catalog registration are honest

**Fixture:** current staged skill, continuation, metadata, and spec; shared
catalog results are not assumed current.

**Expected behavior:**

1. Static/spec/category axes map assertions to current file SHA-256 values.
2. PASS/FAIL/UNEXECUTED remain separate.
3. Shared catalog is updated only by its owner after real execution.
4. Stale/copied/empty fields are not evidence.

**Assertions:**

- [ ] UXD-C18-A: Spec covers UXD-001 through UXD-013
- [ ] UXD-C18-B: This candidate does not edit catalog
- [ ] UXD-C18-C: All four exclusive-file hashes are recorded for registration

---

## Cross-skill compatibility

- [ ] UXD-X001: Content/evidence/workflow state mirrors P1 authoring patterns
- [ ] UXD-X002: Decision classes/provenance match design-system and quick-design
- [ ] UXD-X003: Context manifest uses deterministic bounded selection/hash digest
- [ ] UXD-X004: Target/context/checkpoint writes use compare-and-set
- [ ] UXD-X005: Authoring receipt is immutable evidence but never review approval
- [ ] UXD-X006: Reviewer consumes current target/profile/schema/context/receipt
- [ ] UXD-X007: Accessibility and global library retain external owners
- [ ] UXD-X008: Skill/continuation/metadata/spec agree on v2 contracts and status

## Coverage Notes

### Authoritative P1 finding trace

| Audit ID | SKILL clause | Case/assertion |
|---|---|---|
| `UXD-005` | Phases 1 and 3 mode/content inventory and mutation planning | Case 4: `UXD-C04-A`, `UXD-C04-B`, `UXD-C04-C` |
| `UXD-006` | Phase 2 bounded context | Case 6: `UXD-C06-A`, `UXD-C06-B`, `UXD-C06-C` |
| `UXD-007` | Phase 0 before Phase 2 | Case 7: `UXD-C07-A`, `UXD-C07-B`, `UXD-C07-C` |
| `UXD-008` | Continuation Phase 5 | Case 8: `UXD-C08-A`, `UXD-C08-B`, `UXD-C08-C` |
| `UXD-009` | Required header and state axes | Case 9: `UXD-C09-A`, `UXD-C09-B`, `UXD-C09-C` |
| `UXD-010` | Continuation Phase 8 | Case 10: `UXD-C10-A`, `UXD-C10-B`, `UXD-C10-C` |
| `UXD-011` | Continuation Phase 7 | Case 11: `UXD-C11-A`, `UXD-C11-B`, `UXD-C11-C` |
| `UXD-012` | Continuation Phase 9 | Case 12: `UXD-C12-A`, `UXD-C12-B`, `UXD-C12-C` |
| `UXD-013` | Profile/content contracts, continuation, and SKILL trace matrix | Case 18: `UXD-C18-A`, `UXD-C18-B`, `UXD-C18-C` |

This matrix traces every exact P1 ID from the 2026-07-20 ux-design audit.
UXD-001 through UXD-004 are separately classified P0 findings. Further slug
collision matrices, pattern-entry concurrency mechanics, responsive schematic
tooling, foundation workflow ownership, and downstream review persistence remain
UXD-014..018 except where P1 authority/CAS boundaries require explicit
compatibility. These rows are written-contract coverage, not executed results.
