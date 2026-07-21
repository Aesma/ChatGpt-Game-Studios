# Skill Test Spec: $create-architecture

## Skill Summary

`$create-architecture` authors `docs/architecture/architecture.md` as a versioned
`DRAFT` derived from confirmed requirements and Accepted ADRs. Accepted ADRs remain
the only owners of binding technical decisions. The architecture may expose
non-binding `DECISION-*` proposals, but it may not turn them into implementation
contracts.

The workflow supports `new`, `resume`, `focus`, and read-only `audit` profiles.
`new` is skeleton-first; `resume` and `focus` protect existing content. The author
cannot review, sign, approve, or promote its own output. READY requires a fresh
independent `$architecture-review` PASS for the exact current artifact hash and a
separate recorder.

In `full` review mode, the independent architecture review and independent
lead-programmer feasibility review are dispatched concurrently after the DRAFT hash
is frozen. In `lean`, only the architecture review is dispatched. In `solo`, no
independence is simulated and the artifact remains DRAFT.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; `name`
  matches the skill directory.
- [ ] Invocation declares all profiles: `new`, `resume`, `focus`, and `audit`.
- [ ] Architecture statuses are `DRAFT`, `PARTIAL`, and `READY`; review verdicts are
  `PASS`, `CONCERNS`, and `FAIL`.
- [ ] The skill explicitly forbids author self-review, author sign-off, and author
  promotion to READY.
- [ ] READY requires an independent review record bound to the current artifact hash
  and a recorder distinct from both author and reviewer.
- [ ] `EXPLICIT_REQUIREMENT`, `CONFIRMED_REQUIREMENT`, and `INFERRED_CANDIDATE` are
  defined as separate classes.
- [ ] Baseline rows require source path, locator/excerpt, and source SHA-256.
- [ ] The skill states that inferred candidates do not enter the baseline without
  confirmation evidence.
- [ ] Accepted ADRs are the sole source of binding technical decisions.
- [ ] Missing or non-Accepted ADR decisions are labeled `NON-BINDING PROPOSAL` with
  a `DECISION-*` ID.
- [ ] `new` creates a complete skeleton before section content.
- [ ] `focus` limits edits to the selected section and minimal status/provenance
  fields; `audit` permits no mutation.
- [ ] Existing bounded authorization is reused, or the complete changeset is
  approved once before the first write; no per-section file authorization prompts.
- [ ] Reviewer failure, timeout, blocked state, or hash mismatch cannot produce
  READY.
- [ ] A DRAFT/PARTIAL handoff never says `Architecture Complete`.

### Prohibited positive instructions

Static inspection must fail if the skill positively instructs the author to:

- perform a technical-director self-review;
- record its own approval/sign-off;
- treat user file approval as technical acceptance;
- claim an inferred requirement is part of the baseline before confirmation;
- make module, API, data-flow, threading, or persistence choices binding without an
  Accepted ADR; or
- mark the architecture READY without independent current-hash evidence.

Prohibition text explaining these guards is allowed and must not be flagged as a
violation.

---

## Behavioral Cases

### Case 1: New profile — skeleton first and provenance preserved

**Fixture**

- `docs/architecture/architecture.md` does not exist.
- Two approved GDDs contain explicit requirement IDs.
- One GDD statement merely suggests a possible threading need.
- The target engine reference exists.
- The complete changeset is authorized.

**Input:** `$create-architecture new --review lean`

**Expected behavior**

1. The skill builds an input manifest containing approval evidence and SHA-256 for
   each source.
2. It places explicit statements in the baseline with source locator/excerpt/hash.
3. It places the suggested threading need only in Inferred Candidates.
4. It creates the full architecture skeleton before adding section content.
5. It writes accepted sections incrementally under the existing authorization.

**Assertions**

- [ ] The first architecture write contains every required section header.
- [ ] No authored section content precedes the skeleton write.
- [ ] Explicit requirements retain their source-owned IDs.
- [ ] The threading inference is labeled `INFERRED_CANDIDATE` and absent from the
  baseline and coverage count.
- [ ] Each baseline row contains source path, locator/excerpt, and source hash.
- [ ] The output is DRAFT until independent review and recording complete.

---

### Case 2: Inferred candidate requires explicit confirmation

**Fixture**

- An approved combat GDD describes 200 enemies but states no threading model.
- The author infers that AI might need background processing.

**Input:** `$create-architecture new`

**Expected behavior**

1. The author records background processing as an inferred candidate.
2. The user is shown meaningful technical options and tradeoffs.
3. If the user does not confirm a requirement, the candidate remains non-binding.
4. If the user explicitly confirms it, the workflow records confirmation evidence
   and promotes it to `CONFIRMED_REQUIREMENT` with source provenance.

**Assertions**

- [ ] Scanning the GDD alone never makes the inference a baseline requirement.
- [ ] Unconfirmed inference creates no required ADR and no coverage gap.
- [ ] Confirmed promotion records who confirmed it and in which run/decision.
- [ ] The source excerpt/hash remain attached after confirmation.

---

### Case 3: ADR authority — architecture cannot become a second truth source

**Fixture**

- ADR-0004 is Accepted and owns save serialization.
- ADR-0007 is Proposed and suggests an event bus.
- No ADR owns the public combat API.

**Input:** `$create-architecture new`

**Expected behavior**

1. Save serialization is written as `DERIVED — ADR-0004@<hash>`.
2. The event bus is a non-binding proposal linked to a stable decision gap.
3. The combat API is illustrative or omitted and linked to a separate decision gap.
4. Proposed ADR and missing ADR dependencies block READY.

**Assertions**

- [ ] Only ADR-0004 contributes a binding statement.
- [ ] ADR-0007 is never described as the chosen event architecture.
- [ ] Public combat functions are not described as contracts programmers may
  implement against.
- [ ] Required ADR entries do not pre-decide the ADR outcome.
- [ ] Any stale ADR hash makes its derived statement stale/non-binding.

---

### Case 4: Full mode — independent reviews run concurrently

**Fixture**

- The author has finished a DRAFT and frozen canonical hash `H1`.
- Fresh independent architecture-review and lead-programmer contexts are available.
- Neither context participated in authoring.

**Input:** `$create-architecture resume --review full`

**Expected behavior**

1. The author does not evaluate or sign the artifact.
2. Independent `$architecture-review` and LP feasibility review are dispatched
   concurrently with path, `H1`, and the same input-manifest hash.
3. The workflow waits for both and treats LP feasibility as advisory.
4. The architecture reviewer writes an external hash-bound record.

**Assertions**

- [ ] Both delegations are issued before waiting for either result.
- [ ] Both reviewers receive exactly `H1`.
- [ ] The review record is outside `architecture.md` and contains reviewer identity,
  reviewed hash, manifest hash, method, verdict, and findings.
- [ ] No author approval/sign-off field is added to the architecture.
- [ ] LP feasibility cannot independently promote the artifact.

---

### Case 5: Separate recorder promotes only a current-hash PASS

**Fixture**

- Independent review record R1 has verdict PASS for canonical hash `H1`.
- Current architecture canonical hash is `H1`.
- All readiness inputs are approved and all blocking decisions have current Accepted
  ADRs.
- A recorder distinct from author and reviewer is available.

**Expected behavior**

1. The recorder validates identity separation, hash equality, input hashes, ADR
   statuses, blockers, and review verdict.
2. The recorder changes only status/review reference/revision history to READY.

**Assertions**

- [ ] READY is written by the recorder, never by the author or reviewer.
- [ ] The review record path and hash are recorded.
- [ ] Technical content is unchanged during promotion.
- [ ] User approval alone is insufficient for READY.

---

### Case 6: Hash change invalidates review

**Fixture**

- R1 is a PASS for `H1`.
- The architecture is edited after review and now hashes to `H2`.

**Expected behavior**

1. R1 is reported as stale.
2. Status remains or returns to DRAFT.
3. A fresh independent review of `H2` is required.

**Assertions**

- [ ] The recorder refuses READY using R1.
- [ ] Findings from R1 may be displayed but are not current promotion evidence.
- [ ] No automatic copy or retargeting of R1 to H2 occurs.

---

### Case 7: Reviewer failure or timeout cannot be replaced by self-review

**Fixture**

- A DRAFT exists at current hash `H1`.
- Independent architecture-review times out or returns BLOCKED.

**Input:** `$create-architecture resume --review lean`

**Expected behavior**

1. The skill reports the reviewer outcome and preserves the draft.
2. It marks the run PARTIAL when review was requested but incomplete.
3. It does not run author-side review as a fallback.

**Assertions**

- [ ] Status is not READY.
- [ ] No sign-off is added.
- [ ] The handoff identifies review as failed/blocked and names one recovery action.
- [ ] Existing authored content is preserved.

---

### Case 8: Lean and solo modes preserve independence

**Fixture A:** Independent architecture reviewer is available.

**Input A:** `$create-architecture resume --review lean`

**Assertions A**

- [ ] Independent architecture-review runs.
- [ ] LP feasibility is skipped with a named lean-mode note.
- [ ] READY is still impossible without separate recorder promotion.

**Fixture B:** The author is the only available context.

**Input B:** `$create-architecture resume --review solo`

**Assertions B**

- [ ] No reviewer is simulated by the author.
- [ ] Output records that independent review was not run in solo mode.
- [ ] The architecture remains DRAFT.

---

### Case 9: Resume profile preserves completed sections

**Fixture**

- Existing DRAFT contains completed Layers and Ownership sections and an incomplete
  Data Flow section.
- Starting hash is `H0`.

**Input:** `$create-architecture resume`

**Expected behavior**

1. The workflow reads the existing document and identifies eligible incomplete or
   explicitly stale sections.
2. It updates Data Flow only, plus required status/provenance/history fields.
3. It checks `H0` before writing.

**Assertions**

- [ ] Layers and Ownership remain byte-for-byte unchanged.
- [ ] The existing file is not replaced with a new skeleton.
- [ ] A concurrent target change stops the write with PARTIAL status.

---

### Case 10: Focus profile has a narrow mutation boundary

**Fixture**

- Existing architecture has all sections populated.

**Input:** `$create-architecture focus data-flow`

**Expected behavior**

1. The skill reads the whole document for context.
2. It proposes and writes only Data Flow plus minimal disclosure fields.
3. If a newly discovered issue affects another section, it reports the issue and
   asks to expand scope instead of editing that section.

**Assertions**

- [ ] Every non-target technical section is byte-for-byte unchanged.
- [ ] No whole-document regeneration occurs.
- [ ] The resulting whole-file hash, not a section hash, is used for later review.

---

### Case 11: Audit profile is strictly read-only

**Fixture**

- Existing architecture, ADRs, and session state are present.

**Input:** `$create-architecture audit`

**Expected behavior**

1. The workflow reports requirement classification, ADR authority, provenance,
   status, hash, and review-record problems inline.
2. It performs no writes and never changes status.

**Assertions**

- [ ] Architecture bytes are unchanged.
- [ ] ADRs, review records, session state, and catalog are unchanged.
- [ ] No skeleton, checkpoint, review record, or remediation file is created.

---

### Case 12: Existing target protection in new profile

**Fixture**

- `docs/architecture/architecture.md` already exists.

**Input:** `$create-architecture new`

**Expected behavior**

1. The workflow refuses to overwrite the existing file.
2. It offers `resume`, `focus`, or `audit` without mutating anything.

**Assertions**

- [ ] Existing bytes are preserved.
- [ ] The workflow does not silently switch profiles.
- [ ] No status or session-state write occurs before a valid profile is selected and
  authorized.

---

### Case 13: Proposed ADR and open blocker prevent false completion

**Fixture**

- Independent review reports PASS for the current hash.
- A Foundation decision depends on Proposed ADR-0012.
- A blocking open question remains.

**Expected behavior**

1. The review PASS is retained as evidence for that hash.
2. The recorder refuses READY because non-review readiness conditions fail.
3. Handoff says DRAFT, lists both blockers, and gives one highest-priority next
   action.

**Assertions**

- [ ] Review PASS alone is not treated as architecture completion.
- [ ] Proposed ADR is specific by ID/status/hash.
- [ ] The handoff does not say `Architecture Complete` or claim gate readiness.

---

## Protocol Compliance

- [ ] Product/technical decisions use Question → Options → Decision → Draft →
  Approval, with 2–3 meaningful options when a choice is open.
- [ ] File authorization is changeset-scoped and not repeated per section.
- [ ] Incremental writes occur only inside the authorized profile mutation boundary.
- [ ] Every successful section write updates the recovery checkpoint.
- [ ] Review evidence is external, independent, and exact-hash-bound.
- [ ] Failure paths return DRAFT/PARTIAL and preserve recoverable state.
- [ ] Handoff emits one highest-priority next action and does not auto-run chained
  skills.

## Coverage Notes

This specification intentionally replaces the prior contract in which the author
could self-assess, lean/solo could imply completion without independent evidence,
Proposed ADRs did not block finalization, and profile behavior was unspecified.
Cross-skill acceptance still requires `$architecture-review` and `$gate-check` to
consume the same current-hash external review record contract.
