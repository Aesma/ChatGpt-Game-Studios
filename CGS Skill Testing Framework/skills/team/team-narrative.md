# Skill Test Spec: $team-narrative

## Skill Summary

Coordinates narrative delivery through a strict sequence: validate a manifest and
bounded canon graph, resolve explicit canon decisions, freeze a canon-baseline hash,
collect bounded read-only proposals, assign one writer per artifact, perform
localization review, authorize exact writes, read back final hashes, and obtain a
fresh independent narrative review. Only a current, fully evidenced and localization-
ready artifact set may receive `COMPLETE`.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; `name`
  matches the skill directory
- [ ] Invocation requires `--manifest` and validates arguments before reads,
  delegation, decisions, or writes
- [ ] No-argument behavior has zero reads, delegates, prompts, or writes
- [ ] Canon validation and an explicit decision precede writer, art-director, and
  level-designer proposal launch
- [ ] A verified canon-baseline hash is the hard gate for downstream proposals
- [ ] Proposal agents are read-only, bounded to maximum concurrency 3, have deadlines,
  at most one no-write retry, revoked attempt tokens, and late-result quarantine
- [ ] Every destination path has exactly one writer; shared records have one recorder
  and sequential base-hash guarded writes
- [ ] Canon promotion and narrative-content writes have separate exact mutation
  manifests and separate authorization boundaries
- [ ] Localization review uses real declared UX/string constraints, never a universal
  fixed line limit
- [ ] `NOT LOCALIZATION READY` can never produce `COMPLETE` or a downstream handoff
- [ ] Final review is fresh, independent, read-only, and tied to the current final
  artifact-set hash; post-review changes require rehash and scoped re-review
- [ ] Narrative review profile covers canon, voice, arc, trigger contract, mystery
  truths, localization, content rating, and reference integrity
- [ ] The workflow does not invoke or recommend a system-GDD review workflow
- [ ] Immutable checkpoints and hash-validated resume behavior are specified
- [ ] Terminal verdicts include `COMPLETE`, `PARTIAL`, and `BLOCKED`
- [ ] Final output requires artifact paths, hashes, owners, authorization evidence,
  localization evidence, reviewer identity, blockers, checkpoint, and one next action

---

## Case 1: Happy path — canon-safe delivery

**Fixture:**

- A valid request manifest declares content/run IDs, create/revise operation, canon
  sources, destination paths, base hashes, owners, UX/string constraints, policies,
  authorities, budgets, and deadlines
- Canon sources and the proposed brief agree
- All proposal, localization, write, read-back, and independent review tasks succeed

**Input:**

`$team-narrative --manifest production/requests/ironveil-intro.yaml`

**Expected behavior:**

1. Request and bounded dependency graph are validated and hashed.
2. `world-builder` and `narrative-director` return read-only canon inspection and
   brief proposals.
3. Canon authority confirms the source-backed decision; the verified sorted canon
   manifest produces `CANON_FROZEN` and a baseline hash.
4. Writer, art-director, and level-designer proposal tasks are issued together with
   the same baseline hash and make no writes.
5. Ownership and exact content mutation manifests are authorized.
6. Localization review passes against declared real constraints.
7. Unique owners write only their disjoint authorized paths; all files are read back
   and hashed into the final artifact-set hash.
8. A fresh non-author reviewer passes the narrative profile against those hashes.
9. Result is `Verdict: COMPLETE` with all required evidence and exactly one next
   action; no production implementation starts.

**Assertions:**

- [ ] Writer/art/level proposals start only after `CANON_FROZEN`
- [ ] Proposal agents have no write authority
- [ ] Every final path has exactly one owner and a verified final hash
- [ ] Reviewer identity differs from every author/editor/recorder identity
- [ ] Review evidence records the current final artifact-set hash
- [ ] Localization status is `LOCALIZATION READY`
- [ ] No engine code, asset, translation, or trigger implementation is produced

---

## Case 2: Canon contradiction blocks downstream proposals

**Fixture:** Canon says Ironveil was founded 200 years ago; the brief proposes 50.

**Expected behavior:**

1. World-builder reports a stable `NCF-*` finding with both paths/hashes and impact.
2. Coordinator presents source-backed options to the canon authority.
3. Writer, art-director, and level-designer are not launched while unresolved.
4. Choosing a canon change does not itself authorize a write; a canon-only mutation
   manifest and separate promotion authorization are required.
5. If no decision/authority is available, result is `BLOCKED` with a checkpoint and
   exactly one next action.

**Assertions:**

- [ ] No speculative dialogue, visual, or level proposal exists before canon freeze
- [ ] The coordinator never silently chooses canon
- [ ] Decision, promotion authorization, registry update, read-back, and baseline hash
  are separately evidenced
- [ ] Skipping the conflict cannot produce `COMPLETE`

---

## Case 3: Parallel proposals are read-only and uniquely routed

**Fixture:** Frozen canon is available; three proposals target dialogue, an art brief,
and a trigger contract. Two initially suggest editing the same summary file.

**Expected behavior:**

1. At most three proposal agents run concurrently and return only proposal payloads.
2. The coordinator rejects overlapping writer ownership.
3. One recorder is assigned to the shared summary, or the paths are split before
   authorization.
4. Exact disjoint path sets are recorded in the ownership manifest.
5. Writes occur only later, sequentially per path, with expected base-hash guards.

**Assertions:**

- [ ] Parallel delegates cannot patch content or operational files
- [ ] No normalized path has multiple writers
- [ ] A shared manifest/registry has exactly one recorder
- [ ] Unlisted or drifted writes stop the run

---

## Case 4: Independent final-hash review after polish

**Fixture:** Initial final review finds a voice defect; the dialogue owner fixes it.

**Expected behavior:**

1. Initial reviewer is fresh, independent, read-only, and reviews final hashes.
2. The owner's fix makes the first review stale.
3. Artifacts are read back and the artifact-set hash is recomputed.
4. A fresh scoped independent review covers the changed dialogue and dependents.
5. `COMPLETE` is possible only if the new review passes and references the new hash.

**Assertions:**

- [ ] An author never self-approves
- [ ] Review before the final write cannot satisfy the completion gate
- [ ] Post-polish changes always cause rehash and re-review
- [ ] Stale review evidence yields `PARTIAL` or `BLOCKED`, never `COMPLETE`

---

## Case 5: Blocking localization defect cannot be waived into COMPLETE

**Fixture:** `dialogue.ironveil.intro.003` hardcodes an English date and has no
locale-aware formatter contract.

**Expected behavior:**

1. Localization-lead returns blocking `LOC-*` evidence with string ID, source hash,
   violated contract, owner, and required destination.
2. Assigned dialogue owner may fix it only within the authorized manifest.
3. The changed string is rehashed and independently re-reviewed.
4. If the defect remains, status is `NOT LOCALIZATION READY` and verdict `PARTIAL`.
5. Even if the user accepts business risk, no `COMPLETE`, localization handoff, or
   implementation handoff is emitted.

**Assertions:**

- [ ] Blocking localization issues must be fixed and re-reviewed for completion
- [ ] Accepted risk is not equivalent to readiness
- [ ] The workflow never silently rewrites an unauthorized string
- [ ] Final output names the blocker and exactly one resolution action

---

## Case 6: Narrative review profile replaces system-GDD review

**Fixture:** All artifacts are written and localization-ready.

**Expected behavior:** A fresh read-only reviewer checks canon/hash/reference
integrity, voice, arc and pacing, trigger contracts, mystery truth-ID coverage and
access partition, localization constraints, cultural safety, and content rating.

**Assertions:**

- [ ] Findings use stable `NRF-*` IDs and include evidence path/hash, owner,
  destination, severity, and disposition
- [ ] No system-GDD review workflow is invoked or recommended
- [ ] Narrative evidence is bound to the final artifact-set hash
- [ ] Missing profile evidence prevents `COMPLETE`

---

## Case 7: No argument exits before side effects

**Input:** `$team-narrative`

**Expected behavior:** Print manifest-based usage and stop.

**Assertions:**

- [ ] No repository file is read
- [ ] No agent is spawned
- [ ] No user decision is requested
- [ ] No file or checkpoint is written
- [ ] Topic is not inferred from repository state

---

## Case 8: Timeout, cancellation, late result, and resume

**Fixture:** Art-director proposal exceeds its deadline and later returns a patch.

**Expected behavior:**

1. Attempt is canceled, token revoked, and at most one retry occurs only after
   confirming the first attempt wrote nothing.
2. Late patch/result is ignored and quarantined.
3. Phase deadline prevents indefinite waiting; result is `PARTIAL` with a checkpoint.
4. Resume verifies checkpoint chain, current inputs, canon baseline, authority, and
   absence of late writes before continuing from the exact safe phase.

**Assertions:**

- [ ] Concurrency never exceeds 3, attempt deadline never exceeds 15 minutes, and
  phase deadline never exceeds 30 minutes
- [ ] No more than one no-write retry occurs
- [ ] Late output cannot mutate or enter the accepted proposal set
- [ ] Drift on resume yields `BLOCKED` rather than silent restart

---

## Case 9: Exact authorization boundaries

**Fixture:** Proposals are approved conceptually; requested content paths are not yet
authorized. A delegate also suggests a new glossary file.

**Expected behavior:**

1. Concept approval does not permit mutation.
2. Exact content mutation manifest lists operation, path, base hash, writer, proposal
   IDs, size limit, and non-writes.
3. Only named paths may be written after authority approval.
4. Suggested glossary path is excluded or requires a revised manifest and new
   authorization.

**Assertions:**

- [ ] Unknown future changes are never pre-authorized
- [ ] Canon-promotion authority and content-write authority are distinct
- [ ] No per-file prompts occur inside unchanged authorized scope
- [ ] Scope expansion stops before writing

---

## Case 10: Canon registry is a separately verified shared artifact

**Fixture:** A canon decision creates a new faction fact and registry ID.

**Expected behavior:** One canon writer edits the fact; one registry recorder updates
the shared registry sequentially; both verify base hashes, read back, validate
references, and contribute to the sorted canon-baseline hash.

**Assertions:**

- [ ] No two agents write the registry
- [ ] Product decision is recorded before promotion authorization
- [ ] Failed registry validation prevents `CANON_FROZEN`
- [ ] Downstream proposals do not start on partial canon promotion

---

## Case 11: Mystery truth and spoiler access boundary

**Fixture:** A public dialogue references a mystery whose true answer is confidential.

**Expected behavior:** The answer is written only to a declared private canon
artifact; public content uses its stable truth ID. Read-back validates access class,
truth coverage, references, and hashes.

**Assertions:**

- [ ] Protected truth text does not leak into public artifacts or proposal evidence
- [ ] Missing private truth artifact or orphan truth ID blocks completion
- [ ] Independent review includes the spoiler partition check

---

## Case 12: Missing real UI/string constraints

**Fixture:** Dialogue is proposed, but the request manifest declares no verifiable UX
or string-system constraint source.

**Expected behavior:** Affected constraints are `UNKNOWN`; the workflow does not
invent a 120-character limit; localization is not ready and verdict is `PARTIAL` or
`BLOCKED` with one action to supply the source.

**Assertions:**

- [ ] Generic language-expansion percentages do not replace actual constraints
- [ ] Unknown constraints cannot pass localization review
- [ ] `COMPLETE` is impossible until sources are supplied and review is rerun

---

## Protocol Compliance

- [ ] Canon is validated, decided, authorized when changed, and frozen before
  downstream creative proposals
- [ ] All parallel work is read-only, bounded, cancelable, retry-limited, and immune
  to late writes
- [ ] Every write has one owner, an exact authorization entry, a base-hash guard, and
  read-back evidence
- [ ] All final changes invalidate prior review until independent scoped re-review
- [ ] Localization blockers cannot be accepted into `COMPLETE`
- [ ] Operational records have a single coordinator recorder and immutable checkpoints
- [ ] `COMPLETE` requires current paths/hashes/owners/review and zero blockers
- [ ] `PARTIAL` preserves safe evidence; `BLOCKED` names the decision or dependency
- [ ] Output has exactly one status-driven next action and performs no downstream work

---

## Coverage Notes

Cases 2, 4, 5, and 6 directly regress the five audited P0 failures: canon-before-
parallel ordering, unique write ownership, independent final-hash review,
localization completion gating, and narrative-specific review routing. Cases 7–12
cover adjacent side-effect, authorization, bounded-concurrency, resume, registry,
spoiler, and real-constraint contracts so those P0 fixes cannot be bypassed through
another path.
