# Skill Test Spec: $art-bible

## Skill Summary

`$art-bible` authors one versioned `AB-1` Art Bible through a skeleton-first,
section-by-section workflow. Exact file authorization precedes writes, while
each substantive visual decision still requires user approval. Finishing only a selected scope does not prove whole-artifact completeness; all
nine current sections must independently qualify before approval. Formal
approval requires all nine sections COMPLETE and one independent fresh
`art-director` review record bound to the current raw-byte artifact hash. The
reviewer never edits the Art Bible. Asset production and implementation remain
blocked without a current matching APPROVE record.

## Canonical AB-1 section IDs

1. `AB-01` Visual Identity Statement
2. `AB-02` Mood, Lighting & Atmosphere
3. `AB-03` Shape, Composition & Silhouette
4. `AB-04` Color System & Accessibility
5. `AB-05` Typography & Iconography
6. `AB-06` Character Art Direction
7. `AB-07` Environment & Level Art Direction
8. `AB-08` UI/HUD & VFX Visual Language
9. `AB-09` Asset Standards, References & Prohibitions

Titles are display text; stable IDs are identity.

## Static Assertions

- [ ] Frontmatter contains only `name` and non-empty `description`
- [ ] SKILL, metadata, and spec all name AB-1 skeleton-first authoring and
      independent current-hash approval
- [ ] Fresh creation writes all nine stable section headings before section bodies
- [ ] Artifact status is limited to DRAFT/PARTIAL/COMPLETE
- [ ] No APPROVED status or reviewer signature is written inside the Art Bible
- [ ] A PARTIAL artifact or scoped-set-only completion cannot invoke whole-artifact approval
- [ ] AD-ART-BIBLE uses `art-director`, never `creative-director`
- [ ] Whole reviewer identity is different from every author identity
- [ ] Review record is external, immutable, and contains artifact/section hashes
- [ ] Post-review artifact changes make approval stale
- [ ] Legacy/unknown schemas require an approved migration diff
- [ ] Exact file authorization does not expand through section decisions,
      delegation, review, or resume
- [ ] Asset production/implementation remains blocked until current-hash approval

---

## Test Cases

### Case 1: Fresh document creates full AB-1 skeleton first

**Fixture:**

- `design/art/art-bible.md` is absent
- concept context is available
- the exact Art Bible and state paths are authorized
- selected scope is core (AB-01 through AB-04)

**Expected behavior:**

1. The first Art Bible write creates the AB-1 header and all AB-01 through AB-09
   headings.
2. Every unselected section contains only a neutral not-authored marker.
3. The state file records all nine section IDs and hashes.
4. Section content is written only after the skeleton exists and the user
   approves that section's decisions.
5. Final artifact status is PARTIAL, not COMPLETE or APPROVED.

**Assertions:**

- [ ] Skeleton precedes all section bodies
- [ ] Exactly nine unique stable IDs
- [ ] AB-05 through AB-09 remain preserved placeholders
- [ ] Production Use remains BLOCKED
- [ ] No review record is created for the partial draft

---

### Case 2: Scoped completion cannot approve the whole artifact

**Fixture variants:**

- scope is AB-01 through AB-04;
- scope is AB-09 only;
- resume completes every selected section but other AB-1 sections are incomplete.

**Expected behavior:**

1. Selected sections may become COMPLETE.
2. Unselected incomplete sections remain visible in the status matrix.
3. Artifact status is PARTIAL.
4. AD-ART-BIBLE whole review is ineligible even in full mode.
5. No asset-production or implementation handoff is presented as legal.

**Assertions:**

- [ ] Scoped-set completion is not whole completeness
- [ ] SECTION REVIEWED does not promote artifact approval
- [ ] Verdict cannot be APPROVED
- [ ] Production remains blocked

---

### Case 3: Full current-hash review uses an independent art-director

**Fixture:**

- AB-1 document contains all nine valid COMPLETE sections
- current raw-byte artifact hash is known
- author identities are recorded
- review mode is full
- one exact absent immutable review-record path is authorized
- concept and technical constraints are current

**Expected behavior:**

1. A fresh `art-director` identity that is not an author runs AD-ART-BIBLE.
2. The reviewer independently reads all nine sections and recomputes the raw
   artifact hash before and after review.
3. The reviewer does not edit the Art Bible.
4. It creates only the authorized immutable review record.
5. An APPROVE record includes reviewer/author identities, separation proof,
   artifact path/hash, AB-1, COMPLETE status, section/dependency hashes,
   findings, and timestamp.
6. External state records APPROVED only when the current artifact hash still
   matches.

**Assertions:**

- [ ] Reviewer role is art-director, never creative-director
- [ ] Reviewer identity is absent from author IDs
- [ ] Review record is external and hash-bound
- [ ] Art Bible bytes are unchanged by review
- [ ] State approval is a mechanical projection of immutable reviewer evidence
- [ ] Asset production is allowed only after final hash revalidation

---

### Case 4: Self-review or wrong reviewer is invalid

**Fixture variants:**

- the proposed reviewer drafted AB-04;
- the reviewer is the current authoring orchestrator;
- `creative-director` is spawned with AD-ART-BIBLE;
- reviewer identity/provenance is missing.

**Expected behavior:**

1. Separation validation fails before a formal verdict is accepted.
2. Wrong-role or self-review output is advisory only.
3. No APPROVED state is recorded.
4. Production remains blocked.
5. A fresh independent art-director review is required.

**Assertions:**

- [ ] Author/reviewer identity is explicit
- [ ] Same identity cannot author and sign
- [ ] Gate prefix does not substitute for correct role
- [ ] User acceptance cannot waive independence into approval

---

### Case 5: Modification after approval makes review stale

**Fixture:**

- an immutable APPROVE record names artifact hash `H1`
- AB-07 is subsequently modified under an authorized authoring changeset
- current artifact hash is `H2` and differs from `H1`

**Expected behavior:**

1. Resume/current-hash verification detects the mismatch.
2. External review state becomes STALE.
3. The old immutable record is preserved, not edited.
4. Production is blocked.
5. A new complete review with a new exact record path is required.

**Assertions:**

- [ ] Filename or old status cannot preserve approval
- [ ] No approval line in the document is trusted
- [ ] Old record remains immutable historical evidence
- [ ] H2 cannot be approved by H1 evidence

---

### Case 6: Legacy schema requires explicit migration

**Fixture variants:**

- legacy headings match the old retrofit list;
- legacy headings match the old authoring list;
- a section combines UI, typography, and VFX;
- unknown/duplicate headings or IDs exist.

**Expected behavior:**

1. The existing file is read and hashed in full.
2. A read-only mapping table identifies every legacy byte range and proposed
   AB-1 destination.
3. Split/merge ambiguity and unmapped content are explicit.
4. Exact before/after migration diff is shown for user correction/approval.
5. No skeleton or new content overwrites the legacy file before authorization.
6. Migrated sections are re-evaluated; migration alone grants no completeness or
   approval.

**Assertions:**

- [ ] Titles are not treated as stable identity
- [ ] Every original byte is preserved or explicitly dispositioned
- [ ] Unresolved mapping is BLOCKED
- [ ] Unknown content is retained in a migration appendix
- [ ] No legacy approval carries forward without current-hash review

---

### Case 7: Selected-section retrofit preserves all other bytes

**Fixture:**

- current AB-1 file exists
- AB-06 is selected for revision
- other eight section ranges have known hashes
- prior whole review was APPROVED

**Expected behavior:**

1. The complete proposed AB-06 content is approved by the user.
2. Base artifact hash is checked immediately before write.
3. Only AB-06 and authorized external state change.
4. Other eight section hashes remain equal.
5. Prior whole approval becomes STALE.
6. Artifact may remain COMPLETE but production is blocked until re-review.

**Assertions:**

- [ ] Stable ID bounds the edit
- [ ] Concurrent base mismatch blocks the write
- [ ] Unselected content is byte-preserved
- [ ] Section revision never inherits old whole approval

---

### Case 8: Lean and solo modes cannot create formal approval

**Fixture variants:**

- complete AB-1 draft in lean mode;
- complete AB-1 draft in solo mode.

**Expected behavior:**

1. Lean skips whole-document director review and records COMPLETE — UNREVIEWED.
2. Solo spawns no director agents and records COMPLETE — UNREVIEWED.
3. Neither mode creates a formal APPROVE review record.
4. Production remains blocked.
5. Full independent review is the next legal approval step.

**Assertions:**

- [ ] Solo spawns zero directors
- [ ] No skipped gate is misreported as approval
- [ ] User approval of sections is not art-director sign-off
- [ ] COMPLETE and APPROVED remain distinct states

---

### Case 9: Evidence and file authorization remain bounded

**Fixture:**

- initial partial authoring authorizes only Art Bible and state paths
- later the document becomes complete in a new full-mode run
- immutable review path was not in the original changeset
- review ID and exact absent path are now known

**Expected behavior:**

1. The initial authorization does not cover the new review record.
2. The workflow previews its exact create path, owner, and ABSENT state.
3. It obtains a new bounded approval before reviewer record creation.
4. Reviewer may write only that record and cannot edit the Art Bible/state.
5. A new/changed path, owner, or operation requires another revised preview.

**Assertions:**

- [ ] No wildcard review directory authorization
- [ ] Section-content approval does not grant filesystem scope
- [ ] Delegation/review/resume never broadens authorization
- [ ] Immutable evidence is never overwritten

---

### Case 10: Section decision and conflict evidence

**Fixture:**

- AB-08 art direction conflicts with UX readability
- AB-09 visual preference conflicts with a hard platform budget

**Expected behavior:**

1. Art-versus-UX product tradeoff is presented with both positions and options.
2. The user makes the visual/readability decision before section write.
3. A hard technical budget constrains AB-09 automatically.
4. Any remaining product-facing tradeoff requires a user choice.
5. Missing engine/platform budgets leave AB-09 PROVISIONAL/INCOMPLETE.

**Assertions:**

- [ ] Model does not silently resolve product tradeoffs
- [ ] Decision provenance is stored in external state
- [ ] Provisional asset standards cannot make the artifact COMPLETE
- [ ] No asset implementation is started

---

### Case 11: Concurrent change stops a section patch

**Fixture:**

- authorized base artifact hash is `H1`
- another actor changes an unselected section, producing `H2`
- current run is about to write AB-03

**Expected behavior:**

1. Immediate pre-write hash check finds H2.
2. No AB-03 or state write is applied.
3. The unexpected diff is shown.
4. Verdict is BLOCKED until the user resolves/re-authorizes current bytes.

**Assertions:**

- [ ] Compare-and-set check before every section write
- [ ] No overwrite of collaborator changes
- [ ] Prior authorization does not apply to a changed base hash

---

### Case 12: Review verdict CONCERNS or REJECT

**Fixture:**

- complete AB-1 current hash is reviewed independently
- AD-ART-BIBLE returns CONCERNS or REJECT

**Expected behavior:**

1. Immutable record preserves the actual verdict and findings.
2. External state is CONCERNS or REJECTED.
3. Art Bible receives no APPROVED/sign-off line.
4. User risk acceptance does not convert the record to APPROVE.
5. Production remains blocked.

**Assertions:**

- [ ] Review evidence is truthful
- [ ] Non-APPROVE verdict cannot enable production
- [ ] Revision makes a future review use a new hash and record

---

## Verdict and production matrix

| Artifact state | Review state | Production use |
|---|---|---|
| DRAFT | NOT_ELIGIBLE | BLOCKED |
| PARTIAL | NOT_ELIGIBLE | BLOCKED |
| COMPLETE | UNREVIEWED | BLOCKED |
| COMPLETE | CONCERNS/REJECTED/STALE | BLOCKED |
| COMPLETE | APPROVED for a different hash | BLOCKED |
| COMPLETE | APPROVED for current hash | Eligible, subject to other project gates |

## Protocol Compliance

- [ ] AB-1 IDs and required coverage match SKILL exactly
- [ ] Skeleton and state precede section bodies
- [ ] Every substantive section decision is user-approved
- [ ] Partial content never receives whole approval
- [ ] Reviewer is correct-role, fresh, independent, and artifact-read-only
- [ ] Review evidence is external, immutable, and current-hash-bound
- [ ] Any artifact mutation makes prior approval stale
- [ ] Legacy schema migration is explicit and lossless
- [ ] Exact authorization covers every written path and never expands implicitly
- [ ] No asset production/implementation before current-hash APPROVE

## Coverage Notes

- Shared `director-gates.md` currently lacks artifact-hash and reviewer-separation
  fields; this candidate strengthens the skill/spec contract without editing that
  shared file.
- Asset-consuming skills and workflow-guide/catalog language need separately
  authorized updates to enforce this production gate end-to-end.
