# Skill Test Spec: $qa-plan

## Skill Summary

`$qa-plan` reads a bounded sprint, feature, or story scope and writes one
independent QA plan. The plan binds every story, GDD, and ADR to a SHA-256 of its
exact raw bytes, maps story-owned stable AC IDs to stable test/check IDs, and
declares `CURRENT` or `PARTIAL` at generation. Consumers compute `STALE` by
rehashing sources. The skill never edits story files or session state.

The only owned write is
`production/qa/qa-plan-[scope-slug]-[date].md`. A result may say `written` only
after byte-for-byte read-back verification.

---

## Static Assertions (Structural)

- [ ] Playtest requirements name only canonical completed reports at
      `production/playtests/<session-id>/report.md`; templates, raw logs,
      reviews, incomplete sessions, legacy paths, and hash-invalid reports do
      not satisfy evidence.

Verified automatically by `$skill-test static`; no fixture is required.

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; the
  name matches the skill directory.
- [ ] At least two phase headings are present.
- [ ] The owned-output section names exactly the QA plan artifact family.
- [ ] The skill explicitly forbids story, session-state, checkpoint, and
  unlisted writes.
- [ ] The skill requires full raw-byte SHA-256 provenance for every story, GDD,
  and ADR.
- [ ] The skill defines `CURRENT`, `PARTIAL`, and effective `STALE` behavior.
- [ ] Stable AC, automated test, manual check, and config/smoke-check ID formats
  are defined.
- [ ] Result vocabulary includes `written`, `declined`, and `failed`, and
  `written` is conditioned on read-back verification.
- [ ] Verdict keywords `COMPLETE`, `PARTIAL`, and `BLOCKED` are present.

---

## Case 1: Approved plan write changes only the owned artifact

### Fixture

- `production/epics/combat/story-001-damage.md` contains stable AC IDs
  `AC-S001-01`, `AC-S001-02`, and `AC-S001-03`.
- The story references `design/gdd/combat.md` and
  `docs/architecture/adr-0001-damage.md`; both exist.
- `production/session-state/active.md` exists with known fixture bytes.
- Record exact pre-run bytes and SHA-256 for the story, session-state, GDD, ADR,
  and every other file outside `production/qa/`.
- The target QA plan does not exist.

### Input

`$qa-plan story: production/epics/combat/story-001-damage.md`

The user approves the displayed one-file changeset.

### Expected writes

- Create exactly
  `production/qa/qa-plan-story-001-damage-[date].md` with the approved bytes.

### Expected non-writes

- The story file remains byte-for-byte unchanged.
- `production/session-state/active.md` remains byte-for-byte unchanged.
- GDD, ADR, sprint, registry, and architecture files remain byte-for-byte
  unchanged.
- No checkpoint or unlisted artifact is created.

### Expected behavior and verdict

1. The preview lists exactly the plan file and the explicit non-writes.
2. The skill re-hashes required inputs immediately before writing.
3. The plan is read back and verified after writing.
4. The result ledger lists one `write-qa-plan` operation as `written` with the
   verified plan SHA-256.
5. Verdict is `COMPLETE` when the plan is `CURRENT`.

### Assertions

- [ ] Filesystem diff contains exactly the QA plan file.
- [ ] No story QA section is added or replaced.
- [ ] No session-state marker is appended.
- [ ] The reported plan digest equals the digest of written raw bytes.
- [ ] The response does not claim any non-written artifact was updated or
  checkpointed.

---

## Case 2: Legacy story-backfill-only request produces no false success

### Fixture

- One valid story with a `## QA Test Cases` section and known fixture bytes.
- No QA plan target exists.
- `production/session-state/active.md` is absent.

### Input

The user asks `$qa-plan` to perform only the legacy action “back-fill the story
QA section” and does not approve a QA plan write.

### Expected writes

- None.

### Expected non-writes

- The story is byte-for-byte unchanged.
- No QA plan is created.
- No session-state or checkpoint file is created.

### Expected behavior and verdict

1. The skill explains that story merging belongs to the story owner.
2. No backfill option is added to the proposed changeset.
3. The operation ledger does not contain a `written` result.
4. The response does not say “QA plan written,” created, registered, or
   checkpointed.
5. Verdict is `BLOCKED` because no valid owned operation was selected.

### Assertions

- [ ] Entire fixture tree is byte-for-byte unchanged.
- [ ] No output path is synthesized for an unselected branch.
- [ ] No plan success or checkpoint success is reported.

---

## Case 3: Manifest binds raw-byte hashes and stable IDs

### Fixture

- Epic slug `combat`, story number `001`, and story AC IDs `AC-S001-01` and
  `AC-S001-02`.
- The story type is `Logic` and references one GDD and two ADRs.
- All required inputs exist and are readable.
- Precompute SHA-256 from each file's exact raw bytes.

### Input

`$qa-plan story: production/epics/combat/story-001-damage.md`

The user approves the plan write.

### Expected writes

- One QA plan file.

### Expected non-writes

- All source files and session state remain unchanged.

### Expected behavior and verdict

1. The manifest lists the story, GDD, and both ADR paths individually.
2. Every loaded source record contains the expected lowercase
   `sha256:<64-hex>` digest.
3. The story binding lists `AC-S001-01` and `AC-S001-02`.
4. Plan items use `TC-combat-S001-AC01` and `TC-combat-S001-AC02`.
5. No ID is derived from mutable criterion text or list order.
6. Plan state and verdict are `CURRENT` / `COMPLETE`.

### Assertions

- [ ] Every expected story/GDD/ADR digest matches raw fixture bytes.
- [ ] Every stable AC ID maps to exactly one unique stable test ID.
- [ ] Reordering AC text without changing IDs preserves test IDs when the plan
  is regenerated.
- [ ] The plan does not write IDs back into the story.

---

## Case 4: Source mutation makes the plan effectively STALE

### Fixture

- Start with the verified `CURRENT` plan from Case 3.
- Change one byte in `docs/architecture/adr-0001-damage.md` after plan creation.

### Input

Attempt to reuse the plan as downstream gate evidence.

### Expected writes

- None.

### Expected non-writes

- The QA plan and all sources remain unchanged during validation.

### Expected behavior and verdict

1. The consumer re-hashes every captured source before use.
2. The ADR digest mismatch makes effective state `STALE`, regardless of the
   stored generation label.
3. The plan is rejected as gate evidence and regeneration is required.

### Assertions

- [ ] Staleness is detected from bytes, not timestamps or copied text.
- [ ] No automatic story or plan mutation is used to represent `STALE`.
- [ ] Stable AC/test IDs remain available for regeneration but do not bypass
  staleness.

---

## Case 5: Missing source or stable AC ID writes only a declared PARTIAL plan

### Fixture

- A sprint references two stories.
- Story A is valid and has `AC-S001-01`.
- Story B either is missing or contains one acceptance criterion without a
  stable AC ID.
- All existing fixture files have recorded pre-run bytes.

### Input

`$qa-plan sprint`

The user approves writing the partial planning artifact.

### Expected writes

- One QA plan containing the missing source/AC record and exact gap.

### Expected non-writes

- Existing story and session-state bytes do not change.
- No missing story, AC ID, checkpoint, or placeholder hash is created.

### Expected behavior and verdict

1. The missing path remains in the source manifest with a non-loaded status and
   no invented digest, or the unbound criterion is listed by story path/text.
2. `Plan State at Generation` is `PARTIAL`.
3. The result ledger may report the verified plan as `written`, but the final
   verdict is `PARTIAL`, not `COMPLETE`.
4. The plan explicitly cannot satisfy a downstream gate.

### Assertions

- [ ] No `TR-...-???`, fake SHA-256, or guessed AC/test ID appears.
- [ ] `PARTIAL` is not presented as current or implementation-authorizing.
- [ ] Only the actual plan artifact is reported as written.

---

## Case 6: Pre-write source or target race aborts without a success claim

### Fixture

- A complete plan preview has been approved.
- After preview but before write, either a required source changes or an
  existing target plan's raw bytes change.
- Record all fixture bytes at the point of approval and after the simulated
  concurrent change.

### Input

Continue the approved write operation.

### Expected writes

- None by `$qa-plan` after the mismatch is detected.

### Expected non-writes

- The concurrently changed file is preserved.
- Stories and session state remain unchanged.

### Expected behavior and verdict

1. Immediate pre-write revalidation detects the digest mismatch.
2. The operation ledger reports `failed` with the conflicting path and expected
   versus observed digest.
3. No artifact is described as written, updated, registered, or checkpointed.
4. Verdict is `BLOCKED` pending a regenerated preview.

### Assertions

- [ ] Concurrent user edits are not overwritten.
- [ ] Read-back verification is never claimed when no write occurred.
- [ ] The response contains no synthesized success from the approved but
  aborted operation.

---

## Protocol Compliance

- [ ] One complete changeset authorization occurs before the first write.
- [ ] The changeset contains only the independent QA plan.
- [ ] Story and session-state non-writes are explicit and byte-verified in
  behavioral fixtures.
- [ ] Every required story/GDD/ADR is represented in provenance.
- [ ] Stable AC/test IDs are preserved across wording/order changes.
- [ ] `PARTIAL` and effective `STALE` plans are rejected as gate evidence.
- [ ] Result status reflects only selected, completed, read-back-verified work.

---

## Coverage Notes

- Workflow-catalog argument cleanup is outside these P0 cases; the catalog's
  legacy epic-slug example remains a separate contract migration.
- Downstream skills must implement the effective-state revalidation contract;
  this spec proves the producer contract and records downstream enforcement as
  a cross-skill dependency.
- Canonical playtest/smoke/evidence routing is validated by the owning downstream
  specs and is not used to weaken the plan ownership, provenance, or result
  assertions above.
