# Skill Test Spec: $create-control-manifest

## Skill Summary

`$create-control-manifest` reads Accepted ADRs and the configured technical and
engine references, then generates `docs/architecture/control-manifest.md` as a
source-traceable programmer reference. Extraction must preserve the source's
normative level and scope: MUST/SHOULD/MAY and their negative forms are distinct,
and wording without a clear normative level is reported as an ambiguity rather
than promoted.

Rejected alternatives remain contextual unless their ADR explicitly calls them
`forbidden` or `prohibited`. The current agent owns parsing and drafting. A fresh,
independent `technical-director` instance performs a mandatory read-only integrity
review of an exact SHA-256-bound payload. This is not a configurable director
gate and does not read `production/review-mode.txt`.

The skill uses existing bounded task authorization, or previews the complete
changeset and asks once before the first write. It never self-signs, never lets a
reviewer mutate the draft, and never writes an Active manifest after an identity
or review-hash failure.

---

### Case 1: Normative strength is preserved

**Fixture:** Four Accepted ADRs contain these scoped statements:

- ADR-0001: "The save service MUST write through the persistence port."
- ADR-0002: "UI callers should batch cosmetic notifications."
- ADR-0003: "Feature modules MAY cache immutable lookup data."
- ADR-0004: "Gameplay code SHOULD NOT call the analytics adapter each frame."
- ADR-0004 also says: "The adapter is easy to access from gameplay code."

**Input:** `$create-control-manifest`

**Expected behavior:**

1. The skill emits separate MUST, SHOULD, MAY, and SHOULD NOT entries with the
   original scope and source.
2. It does not rewrite SHOULD, SHOULD NOT, or MAY as required, always, MUST, never,
   forbidden, or prohibited.
3. The descriptive adapter sentence is not emitted as a normative rule; it is
   listed as an ambiguity finding only if the extractor believes it may contain a
   constraint needing source clarification.

**Assertions:**

- [ ] ADR-0001 is level MUST.
- [ ] ADR-0002 is level SHOULD, not MUST.
- [ ] ADR-0003 is level MAY, not MUST or SHOULD.
- [ ] ADR-0004's negative recommendation is SHOULD NOT, not forbidden.
- [ ] No sentence without an explicit normative level is auto-promoted.
- [ ] Every emitted rule retains its ADR source, scope, and qualifications.

---

### Case 2: Rejected alternatives stay contextual

**Fixture:** One Accepted ADR contains these alternatives:

- "Redis was rejected for this milestone because operating it exceeds the current
  team budget; reconsider if a managed service is funded."
- "Direct database access from presentation code is prohibited in every build."
- "A second cache was not selected because the first cache meets current scale."

**Input:** `$create-control-manifest`

**Expected behavior:**

1. Redis and the second cache appear only in Contextual Rejections with their
   reasons, ADR-local scope, and reconsideration conditions.
2. Direct database access appears in Forbidden Approaches because the ADR itself
   explicitly says `prohibited` and supplies global scope.
3. The skill never manufactures `never`, `forbidden`, or `prohibited` wording for
   either ordinary rejected alternative.

**Assertions:**

- [ ] A rejected/not-selected/deferred alternative is not automatically forbidden.
- [ ] Only an explicitly `forbidden` or `prohibited` alternative enters the forbidden list.
- [ ] Contextual rejection reasons, scope, and conditions are retained.
- [ ] Ambiguous prohibition wording becomes a finding and is omitted from the forbidden list.

---

### Case 3: Accepted ADR filtering is visible

**Fixture:** `docs/architecture/` contains three Accepted ADRs, two Proposed ADRs,
one Deprecated ADR, and one Superseded ADR.

**Input:** `$create-control-manifest`

**Expected behavior:**

1. Only the three Accepted ADRs contribute rules.
2. All excluded ADRs are reported with their status before write approval.
3. Every included rule names its source ADR.

**Assertions:**

- [ ] Only the three Accepted ADRs appear as rule sources.
- [ ] Proposed, Deprecated, and Superseded ADRs are listed as exclusions.
- [ ] The user sees the exclusion list before approving the write.
- [ ] Excluded ADRs are not silently omitted.
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts.

---

### Case 4: Independent review is identity- and hash-bound

**Fixture:**

- The extraction author runtime identifier is `task/author-a`.
- The stable review payload hashes to SHA-256 `HASH-1`.
- A fresh read-only technical-director reviewer has identifier `task/reviewer-b`.

**Input:** `$create-control-manifest`

**Expected behavior:**

1. The current agent performs parsing, normalization, preview assembly, and
   manifest drafting without delegating them to the reviewer.
2. The payload contains the proposed manifest content excluding review metadata,
   a path-sorted source inventory and source hashes, the extracted rule list, all
   ambiguity findings, and the author identifier.
3. The reviewer receives that exact payload and `HASH-1`, performs no writes, and
   returns its identifier, received hash, verdict, findings, and no-mutation
   confirmation.
4. The author proceeds only when the reviewer identifier differs, the returned
   hash equals `HASH-1`, no mutation occurred, and the verdict is APPROVE.
5. If any reviewed rule, level, scope, source inventory, or finding changes, the
   skill computes a new hash and obtains a new review.

**Assertions:**

- [ ] Extraction and drafting are owned by the current author, not the technical-director reviewer.
- [ ] Reviewer identity is present and differs from author identity.
- [ ] Review approval is recorded against the exact Review Input SHA-256.
- [ ] Missing identity, matching identities, hash mismatch, reviewer mutation, or unavailable independent reviewer blocks an Active write.
- [ ] The current agent never substitutes itself as reviewer or fabricates an identifier.
- [ ] CONCERNS and REJECT require correction and re-review; user acceptance cannot waive source fidelity or independence.
- [ ] The check runs without reading review mode and is not skipped in solo or lean mode.

---

### Case 5: Edge case — manifest already exists

**Fixture:**

- `docs/architecture/control-manifest.md` already exists (version 1, dated last week).
- `docs/architecture/` contains Accepted ADRs, including some accepted since the
  existing manifest was generated.

**Input:** `$create-control-manifest`

**Expected behavior:**

1. The skill detects the existing manifest and reads its version number and date.
2. It offers to regenerate rather than overwriting automatically.
3. If the user confirms, it drafts the update and increments the version number.
4. It applies the same source-fidelity and independent-review checks to the update.
5. It writes only after the complete changeset is authorized and the current hash
   has an independent APPROVE.

**Assertions:**

- [ ] Skill reads and reports the existing manifest version before offering to regenerate.
- [ ] User is offered a regenerate/skip choice; the manifest is not auto-overwritten.
- [ ] Updated manifest has an incremented version number.
- [ ] No stale review hash can authorize changed content.
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts.
- [ ] Ends with next-step handoff: `$create-epics` or `$create-stories`.

---

## Coverage Notes

- Cases 1, 2, and 4 are the P0 semantic-fidelity and reviewer-independence gates.
- Exact table styling remains defined by the skill body; tests assert meaning,
  level, scope, source, identity, and hash rather than presentation trivia.
- Version incrementing remains covered by Case 5; its exact numbering format is
  not fixture-locked.
- Downstream story snapshot/hash staleness is a cross-skill integration concern
  and is not validated by this isolated skill spec.
