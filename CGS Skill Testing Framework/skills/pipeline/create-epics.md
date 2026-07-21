# Skill Spec: `$create-epics`

> **Category**: pipeline
> **Priority**: high
> **Spec written**: 2026-07-21

## Skill Summary

`$create-epics` enumerates only Approved systems explicitly recorded in
`design/gdd/systems-index.md`, loads their exact GDD paths, maps them only to
binding architecture modules backed by Accepted ADRs, and proposes EPIC.md plus
index changes. Before any mutation it classifies existing artifacts as
`create`, `update`, `no-op`, or `conflict`; conflicts block the complete
changeset and authorized writes are guarded by preimage hashes. It never creates
stories.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; the name is `create-epics`.
- [ ] Two or more phase headings are present.
- [ ] The workflow has explicit `COMPLETE` and `BLOCKED` terminal states.
- [ ] Multi-file mutation uses existing bounded authorization or one complete changeset preview and approval.
- [ ] The workflow ends with the `$create-stories [epic-slug]` handoff.

---

## Director Gate Checks

- **Full mode**: PR-EPIC runs after epic definitions and conflict-free inventory, before write authorization.
- **Lean mode**: PR-EPIC is skipped and reported as `PR-EPIC skipped — Lean mode`.
- **Solo mode**: PR-EPIC is skipped and reported as `PR-EPIC skipped — Solo mode`.
- A conflict blocks before PR-EPIC; no gate may legitimize overwriting it.

---

## Test Cases

### Case 1: Happy Path — Overview-only Approved GDDs are included

**Fixture**:

- The Approved systems index contains stable IDs `SYS-INPUT` and `SYS-CAMERA`, exact GDD paths, unique layers, and valid order.
- Both GDDs have `## Overview` but no `## Summary`, and their recorded identity/status agrees with the index.
- Each system maps to a binding architecture module backed by a current Accepted ADR.
- No epic files or index exist; review mode is lean.

**Expected behavior**:

1. The skill reads the systems index first and builds a two-row run manifest.
2. Both Overview-only GDDs are full-read because their indexed rows are eligible.
3. Both targets and the new index are classified `create` and shown completely.
4. PR-EPIC is noted as skipped in lean mode.
5. After existing bounded authorization or one changeset approval, both epics and the index are written and hash-verified.

**Assertions**:

- [ ] Inclusion does not depend on a Summary heading.
- [ ] The exact indexed GDD paths are used; no guessed filename is used.
- [ ] Epic summaries and the complete changeset are shown before mutation.
- [ ] Only the frozen authorized files are written.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: CE-001 — Unindexed documents cannot enter the run

**Fixture**:

- `SYS-COMBAT` is an Approved indexed row whose GDD has only `## Overview`.
- `design/gdd/experimental-combat.md` is not indexed but contains a compelling `## Summary` and matching words.
- Invocation is `$create-epics all`.

**Expected behavior**:

1. The skill includes `SYS-COMBAT` from the index.
2. It does not use the unindexed file to select, replace, or supplement a system.
3. It reports the authoritative manifest before drafting.

**Assertions**:

- [ ] The Overview-only indexed GDD is included.
- [ ] The unindexed Summary-bearing file is absent from the manifest and changeset.
- [ ] No filesystem glob or heading search is treated as enumeration authority.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: CE-001 — Malformed or ineligible indexed row fails safely

**Fixture**:

- One requested row lacks a stable ID, uses status `Designed`, has a duplicate GDD path, or disagrees with the GDD status.
- No output writes have occurred.

**Expected behavior**:

1. The skill distinguishes legal-but-ineligible status from malformed status.
2. It reports the exact row defect and stops with BLOCKED when the requested scope cannot be enumerated completely.
3. It does not guess an ID, status alias, layer, or GDD path.

**Assertions**:

- [ ] Only exact `Approved` rows are eligible.
- [ ] `Designed` is not accepted as an alias.
- [ ] Ambiguous identity/path/layer data yields BLOCKED and zero writes.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Architecture proposal is not a binding module

**Fixture**:

- An Approved indexed system and GDD exist.
- Its only architecture placement is `NON-BINDING PROPOSAL — DECISION-EVENT-BUS`, sourced from Proposed ADR-0012.

**Expected behavior**:

1. The skill reports the proposal and ADR status.
2. It stops with `BLOCKED — accepted architecture decision required`.
3. It does not draft or write an epic against the proposed module.

**Assertions**:

- [ ] Only binding architecture statements backed by current Accepted ADRs may supply a module.
- [ ] User file authorization does not convert a proposal into a binding decision.
- [ ] No EPIC.md or index file is written.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: CE-002 — Exact rerun is a no-op

**Fixture**:

- The target EPIC.md bytes exactly equal the deterministic candidate.
- The index has one exact compatible row and no collisions.

**Expected behavior**:

1. The skill records current hashes and classifies the epic and index as `no-op`.
2. It lists the no-op result and performs no write or overwrite prompt.
3. It ends COMPLETE with `no changes required`.

**Assertions**:

- [ ] A repeat run does not rewrite timestamps or identical artifacts.
- [ ] No-op requires both exact candidate bytes and a unique exact index mapping.
- [ ] Zero files are mutated.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: CE-002 — Compatible update plus independent create

**Fixture**:

- One existing managed epic has the same stable identity, recognized generated schema, no unknown/manual content, and a unique compatible index row, but differs from the deterministic candidate.
- A second target is absent and has no collision.

**Expected behavior**:

1. The first target is classified `update`; its preimage hash and complete unified diff are shown with Update/Skip choices.
2. The second target is classified `create`; its complete content is shown.
3. After the user selects Update and the bounded changeset is authorized once, both targets and the index are rechecked, written, and verified.

**Assertions**:

- [ ] Existing EPIC files are inventoried before any write.
- [ ] A compatible update is never silently overwritten.
- [ ] The new system proceeds normally in the same conflict-free changeset.
- [ ] No per-file write authorization is requested.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: CE-002 — Manual or identity conflict blocks atomically

**Fixture**:

- A target slug already contains an epic for another system ID, or the target has an unknown manual section.
- A separate new target would otherwise be a valid create.

**Expected behavior**:

1. The colliding target is classified `conflict` with identities and hashes.
2. The entire changeset stops BLOCKED before PR-EPIC or authorization.
3. The skill does not overwrite, merge, rename, delete, or write the independent new target.

**Assertions**:

- [ ] Conflict cannot be downgraded to update by a generic approval.
- [ ] Manual/unknown content is preserved.
- [ ] All files remain byte-identical.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: CE-002 — Preimage changes after preview

**Fixture**:

- A conflict-free create/update changeset has been previewed and authorized.
- Before mutation, one target or the index changes bytes or appears/disappears.

**Expected behavior**:

1. The all-target preflight detects the hash/existence mismatch before the first write.
2. The skill writes nothing and reclassifies the complete changeset.
3. A resulting conflict is BLOCKED; a materially changed preview requires new authorization.

**Assertions**:

- [ ] All preimages are rechecked in one read-only pass before mutation.
- [ ] No partially stale changeset is applied.
- [ ] The mismatch and affected path are reported.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Director Gate — PR-EPIC returns CONCERNS

**Fixture**:

- Two Approved indexed systems have conflict-free create/update classifications.
- Review mode is full and PR-EPIC returns CONCERNS.

**Expected behavior**:

1. PR-EPIC runs after inventory and before write authorization.
2. The concerns are surfaced with revise, accept-and-proceed, and stop choices.
3. Revised drafts are re-rendered and reclassified before any changeset approval.
4. No files are written while concerns remain unresolved.

**Assertions**:

- [ ] CONCERNS are shown before mutation.
- [ ] The user has a clear revise/proceed/stop decision.
- [ ] Revised content receives a current inventory and preview.

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Treats an explicit bounded user request as authorization for all in-scope changes.
- [ ] Otherwise previews the complete create/update changeset and asks once before applying it.
- [ ] Does not re-prompt per file, section, or edit within the authorized changeset.
- [ ] Requests new authorization only for material scope/preview changes or separately gated side effects.
- [ ] Performs no mutation during index enumeration, artifact inventory, conflict handling, or gate review.
- [ ] Ends with `$create-stories [epic-slug]` for each created, updated, or current epic.

---

## Coverage Notes

- CE-001 is covered by Cases 1–3; CE-002 is covered by Cases 5–8.
- Case 4 preserves the create-architecture target contract: Proposed or otherwise non-binding architecture text cannot become an epic contract.
- CE-003 and later remediation items remain outside this P0 candidate. In particular, this spec does not resolve module-to-system cardinality, source-hash stale detection, ADR-gap routing, producer retry caps, or template extraction.
- Behavioral execution is still required to prove the written contract; this candidate does not update catalog result fields.
