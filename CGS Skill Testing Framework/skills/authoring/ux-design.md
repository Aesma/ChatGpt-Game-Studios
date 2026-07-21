# Skill Test Spec: $ux-design

## Skill Summary

`$ux-design` authors exactly one versioned `ux-spec`, `hud-design`, or
`interaction-pattern-library` artifact from a bounded manifest. `SKILL.md` plus its
required continuation are the common schema source for authoring, retrofit, and the
independent reviewer. Stable artifact/screen/section IDs, one exact mutation
authorization, atomic single-owner writes, explicit dependency status, and current
hash evidence prevent authoring from being mistaken for approval or implementation
readiness.

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires a manifest and validates arguments before repository reads,
  delegation, decisions, writes, or verdict
- [ ] Author schema hash is SHA-256 of exact `SKILL.md`, one NUL byte, and exact
  `references/continued-workflow.md`
- [ ] Profiles are versioned as `ux-profile-schema-v1` and every required section has
  a stable ID and exact H2 heading
- [ ] Exact headings match the current staged `ux-review` mappings for `ux-spec`,
  `hud-design`, and `interaction-pattern-library`
- [ ] Artifact header includes Artifact Type, hash-based Schema Version, Profile
  Version, stable Artifact/Screen IDs, actual Author Task ID, status, platform,
  accessibility, requirements, and context-manifest hash
- [ ] One exact task mutation authorization covers target/checkpoint paths and
  authorized section IDs; per-section product approval never re-prompts for file
  permission
- [ ] `ux-spec` and `hud-design` never mutate the global pattern library; canonical
  pattern changes require the external UX-library owner and a dedicated library run
- [ ] This workflow consumes but never creates or owns the accessibility foundation
- [ ] Missing concept/GDD owner/accessibility tier/platform/navigation/global-pattern
  dependencies prevent `READY_FOR_REVIEW`
- [ ] Authoring statuses are `DRAFT`, `PARTIAL`, and `READY_FOR_REVIEW`; authoring never
  emits `COMPLETE`, `APPROVED`, or `IMPLEMENTATION READY`
- [ ] Handoff requires a fresh independent reviewer on exact current hashes and never
  starts review or production implementation
- [ ] Context, consultation, checkpoint, timeout, retry, late-result, resume, path,
  ownership, and hash-drift boundaries are explicit

---

## Case 1: Fresh screen spec uses the common versioned schema

**Fixture:** A valid create manifest names stable screen ID `inventory`, an absent
target, exact context paths/hashes, owned GDD requirement IDs, platform/accessibility
profiles, budgets, authorities, writer identities, and checkpoint root.

**Input:** `$ux-design --manifest production/requests/ux-inventory.yaml`

**Expected behavior:**

1. The workflow computes the author schema hash from the two author sources.
2. It builds a scratch skeleton containing UXS-01 through UXS-14 and the exact required
   headings, plus the complete machine-readable header.
3. It previews one exact target/checkpoint mutation manifest and obtains authorization.
4. The unique UX-author writes the skeleton, then processes each section through
   context, decision, draft, product approval, atomic write, and checkpoint.
5. No per-section file authorization is requested.
6. Cross-reference checks pass; exact bytes are read back and hashed.
7. Result is `READY_FOR_REVIEW`, not complete or approved, with one next action for a
   fresh independent review of the exact target hash.

**Assertions:**

- [ ] Stable Artifact ID and Screen ID survive every checkpoint
- [ ] Schema Version equals `ux-design-author-sha256:{computed hash}`
- [ ] All exact ux-spec headings and nested layout headings are present once
- [ ] Actual author identity is recorded; user/consultants are not falsely co-authored
- [ ] No visual, review, accessibility-foundation, global-pattern, or implementation
  artifact is written

---

## Case 2: HUD and pattern profiles use their own exact schemas

**Fixture:** Two independent manifests target `design/ux/hud.md` and
`design/ux/interaction-patterns.md` in separate runs.

**Expected behavior:** HUD uses HUD-01 through HUD-08 and stable screen ID `hud`.
Pattern-library mode uses PAT-01 through PAT-05, identifies the external UX-library
owner, and is the sole authorized target in that run.

**Assertions:**

- [ ] No ux-spec-only heading is imposed on HUD or pattern artifacts
- [ ] HUD covers declared platform/input/resolution/text-scale variants
- [ ] Pattern catalog and entries share canonical `UXP-GLOBAL-*` IDs
- [ ] The three profile mappings exactly match the staged reviewer contract
- [ ] One run never creates both the HUD/screen and global pattern library

---

## Case 3: Retrofit fill-gaps preserves valid content

**Fixture:** Existing current-schema screen spec has valid UXS-01, UXS-03, and UXS-07,
placeholders in UXS-06 and UXS-11, and an absent UXS-12. Manifest mode is `fill-gaps`.

**Expected behavior:** Classify every stable section as VALID, STALE, PLACEHOLDER,
MISSING, or UNMAPPABLE. Authorize and change only UXS-06, UXS-11, and UXS-12. Preserve
all other bytes and verify base/after hashes.

**Assertions:**

- [ ] VALID sections are not rewritten or rediscussed
- [ ] Only authorized stable-ID regions change
- [ ] Current content is determined by IDs, schema/source hashes, and evidence—not
  merely non-placeholder text
- [ ] Result remains PARTIAL if a selected dependency is unresolved

---

## Case 4: Explicit revision and legacy schema migration

**Fixture:** A legacy document uses older headings and substantive content. The user
wants to revise one complete section while migrating.

**Expected behavior:** `revise-sections` permits an explicitly selected VALID/STALE
section. `migrate-schema` produces deterministic mappings, content hashes, moves, and
unresolved fragments. Ambiguous content requires a product decision and is never
silently dropped or duplicated.

**Assertions:**

- [ ] Retrofit is not limited to placeholders
- [ ] Old-to-stable-ID mapping is recorded
- [ ] Unselected legacy bytes are preserved
- [ ] UNMAPPABLE content prevents READY_FOR_REVIEW until resolved
- [ ] Schema change on resume routes to migration rather than stale continuation

---

## Case 5: One write authorization, many product approvals

**Fixture:** Exact target, checkpoints, stable section IDs, owner, base hash, and limits
are authorized once; the user later approves three section drafts.

**Expected behavior:** Each approval is recorded as a `UXDEC-*` product decision. The
same authorized writer applies the three atomic section writes without another
filesystem prompt. A newly proposed path or section stops for a revised manifest.

**Assertions:**

- [ ] Product approval is never represented as write authorization
- [ ] No per-section or per-file authorization prompt occurs inside the boundary
- [ ] Scope expansion does not inherit prior authority
- [ ] Every write has base/after hash and read-back evidence

---

## Case 6: Missing critical dependencies cannot be called ready

**Fixture:** Inventory screen lacks an owned inventory GDD requirement; accessibility
tier and platform/input profile are also missing.

**Expected behavior:** Emit stable owned dependency findings with evidence and
resolution actions. Safe approved sections may be written as DRAFT/PARTIAL, but the
artifact and verdict are PARTIAL. User risk acceptance keeps findings open.

**Assertions:**

- [ ] Missing GDD requirement owner, accessibility foundation/tier, and platform
  profile are blocking, not advisory
- [ ] No COMPLETE, READY_FOR_REVIEW, APPROVED, or implementation-ready claim appears
- [ ] The workflow does not invent product behavior, an accessibility tier, or input
  targets
- [ ] Exactly one next action resolves one named dependency

---

## Case 7: Accessibility and global-pattern ownership stay external

**Fixture:** A screen author invents a reusable drag/drop interaction while no
accessibility foundation or global pattern library exists.

**Expected behavior:** Record a feature-local `UXP-{screen-id}-{slug}` proposal in the
screen spec and an OPEN dependency for the external owners. Do not create either
global prerequisite and do not let a consultant claim ownership.

**Assertions:**

- [ ] Screen target is the only UX artifact written
- [ ] Accessibility specialist may assess but cannot select/write the tier
- [ ] UI programmer is read-only and cannot implement or backfill the library
- [ ] Cross-screen behavior stays blocked until the external UX-library owner merges
  an independently authorized canonical pattern

---

## Case 8: No argument has zero side effects

**Input:** `$ux-design`

**Expected behavior:** Print the manifest usage line and stop.

**Assertions:**

- [ ] No repository files are read
- [ ] No user decision or authorization is requested
- [ ] No delegate is spawned and no file/checkpoint is written
- [ ] No artifact type, screen ID, or target is guessed

---

## Case 9: Collision, reserved path, and hash drift

**Fixture:** Inputs separately exercise an invalid/reserved screen ID, an occupied
create target, a revise base-hash mismatch, and a symlink escaping the repository.

**Expected behavior:** Validation rejects each before writing. Mid-section target drift
halts with PARTIAL/BLOCKED and preserves user work without silent overwrite/revert.

**Assertions:**

- [ ] Stable ID/path normalization is deterministic
- [ ] Create/revise modes cannot be inferred from target existence
- [ ] Every atomic write checks the immediately current base hash
- [ ] Outside-root resolution and outside-manifest mutations stop the run

---

## Case 10: Bounded context and consultation failure

**Fixture:** Declared context exceeds budget and an optional feasibility consultant
times out, then returns a late patch.

**Expected behavior:** Load only declared paths/requirement IDs/one-hop neighbors,
stop at budget, revoke timeout token, allow at most one proven-no-write retry, ignore
the late patch, and checkpoint PARTIAL state.

**Assertions:**

- [ ] HUD does not scan all GDDs and pattern mode does not scan all UX specs
- [ ] At most two consultants run concurrently
- [ ] Attempt and phase deadlines are at most 15 and 30 minutes
- [ ] Consultants are read-only and cannot delegate
- [ ] Late results cannot mutate the target or become current evidence

---

## Case 11: Resume validates exact state

**Fixture:** An interrupted run has approved UXS-01 through UXS-05. One context source
has changed; UXS-03 and UXS-04 depend on it.

**Expected behavior:** Validate checkpoint chain, author schema, authorization, target,
owners, decisions, and late-write absence. Mark only dependent sections stale and
resume at the earliest legal step; never replay writes.

**Assertions:**

- [ ] Unchanged approved sections stay intact
- [ ] Changed schema forces migration
- [ ] Authorization/target drift blocks resume
- [ ] Non-placeholder text alone is not proof of completion

---

## Case 12: Hash-bound independent review and implementation boundary

**Fixture:** Authoring reaches READY_FOR_REVIEW with target hash H1.

**Expected behavior:** Final output names H1, actual author task ID, author schema hash,
and one action to request a fresh reviewer whose task differs from the author. This
workflow does not invoke review or persist its record. If the target later changes to
H2, the H1 review is stale. Production work remains prohibited until a consumer
validates persisted current-hash approval and separately authorizes exact
implementation paths.

**Assertions:**

- [ ] Author never self-reviews or self-approves
- [ ] Review is target-hash and author-schema-hash bound
- [ ] Conversation approval is not claimed as persisted evidence
- [ ] No implementation role is spawned before current-hash approval and a separate
  implementation authorization

---

## Protocol Compliance

- [ ] Author, retrofit, tests, and staged reviewer share the two-file versioned schema
- [ ] Stable screen/section/pattern IDs govern identity and migration
- [ ] User owns product decisions; sources and true author provenance remain explicit
- [ ] One task authorization covers only exact target/checkpoint boundaries
- [ ] Critical dependency and cross-reference blockers prevent READY_FOR_REVIEW
- [ ] Global accessibility and pattern artifacts retain their external owners
- [ ] Atomic writes, immutable checkpoints, bounded context/consultation, timeout,
  recovery, and hashes are testable
- [ ] Authoring stops before review persistence, visual work, or implementation

---

## Coverage Notes

Cases 1–7 directly regress the four audited P0 failures: profile-schema drift,
repeated/mixed authorization, false prerequisite ownership, and unconditional
completion despite dependency gaps. Cases 8–12 cover the adjacent identity, path,
context, consultation, checkpoint, reviewer-independence, approval, and production
authorization paths that could otherwise bypass the P0 controls.
