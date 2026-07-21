# Skill Test Spec: $create-stories

## Skill Summary

`$create-stories` breaks a single epic into traceable story files. It reads
the EPIC.md, the corresponding GDD, governing ADRs, the control manifest, and the
TR registry. Each story gets structured frontmatter including: Title, Epic, Layer,
Priority, Status, TR-ID, ADR references, Acceptance Criteria, and Definition of
Done. Stories are classified by type (Logic / Integration / Visual/Feel / UI /
Config/Data) which determines the required test evidence path.

Status is computed per story and fails closed. A story with an unavailable,
unknown, malformed, non-active, or unresolved TR-ID is `Blocked`; a story with
missing or incomplete QA specifications is at least `Needs Work`. Placeholder
TR-IDs are forbidden. Logic and Integration stories are eligible for `Ready`
only when every acceptance criterion has a complete QA specification with a
stable test-case ID.

In `full` review mode, a QL-STORY-READY check returns a result per drafted story
before changeset authorization. In
`lean` or `solo` mode, QL-STORY-READY is skipped. The skill treats the complete
story batch as one bounded changeset and uses existing task authorization or one
confirmation before writing. Stories are written to
`production/epics/[layer]/story-[name].md`.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED, NEEDS WORK
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Has a next-step handoff at the end (`$story-readiness`, `$dev-story`)
- [ ] Documents story Status: Blocked when governing ADR is Proposed
- [ ] Documents QL-STORY-READY gate: active in full mode, skipped in lean/solo
- [ ] Forbids `TR-[system]-???` and all other placeholder TR values in previews
  and written stories
- [ ] Documents per-story `Blocked` handling plus a traceability gap report
  routed to `$architecture-review` when no exact active TR-ID exists
- [ ] Documents `Needs Work` when QA coverage is missing or incomplete
- [ ] Requires one stable, non-placeholder test-case ID per acceptance criterion
  before a Logic or Integration story can be `Ready`
- [ ] Assigns stable story-local AC IDs and matches QA specifications by those
  IDs rather than mutable criterion text or order
- [ ] Uses computed story status in the preview, story file, EPIC table, and
      completion summary; no template constant may override it
- [ ] Computes the SHA-256 of the exact current control-manifest bytes and writes
      the same hash to both `Manifest Hash` and `## Source Snapshot`
- [ ] Preserves `MUST`/`MUST NOT`/`SHOULD`/`SHOULD NOT`/`MAY` strength and keeps
      contextual rejections distinct from explicit prohibitions

---

## Director Gate Checks

In `full` mode: QL-STORY-READY check runs per story after creation. Stories that
fail the check are noted as NEEDS WORK before the "changeset authorization" ask.

In `lean` mode: QL-STORY-READY is skipped. Output notes:
"QL-STORY-READY skipped — lean mode" per story.

In `solo` mode: QL-STORY-READY is skipped with equivalent notes.

---

## Test Cases

### Case 1: Happy Path — Epic with 3 stories, all ADRs Accepted

**Fixture:**
- `production/epics/[layer]/EPIC-[name].md` exists with 3 GDD requirements
- Corresponding GDD exists with matching acceptance criteria
- All governing ADRs have `Status: Accepted`
- `docs/architecture/control-manifest.md` exists
- `docs/architecture/tr-registry.yaml` has TR-IDs for all 3 requirements
- Every registry entry used by a story has `status: active`
- Every acceptance criterion has a complete QA specification; Logic and
  Integration specifications use stable test-case IDs
- `production/session-state/review-mode.txt` contains `lean`

**Input:** `$create-stories [epic-name]`

**Expected behavior:**
1. Skill reads EPIC.md, GDD, governing ADRs, control manifest, and TR registry
2. Classifies each requirement into a story type (Logic / Integration / Visual/Feel / UI / Config/Data)
3. Drafts 3 story files with correct frontmatter schema
4. QL-STORY-READY is skipped (lean mode) — noted in output
5. Treat the complete described file set as one bounded changeset: use existing task authorization, or preview and confirm it once before the first write.
6. Writes all 3 story files after approval

**Assertions:**
- [ ] Each story's frontmatter contains: Title, Epic, Layer, Priority, Status, TR-ID, ADR reference, Acceptance Criteria, DoD
- [ ] Every written TR-ID is an exact active registry ID
- [ ] Every Logic/Integration AC maps to a stable test-case ID
- [ ] Every story contains the exact current manifest version, manifest SHA-256,
      and matching Source Snapshot entry
- [ ] Story control rules preserve source normative strength; an ordinary
      contextual rejection is not rendered as forbidden
- [ ] Story types are correctly classified (at least one Logic type in fixture)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] QL-STORY-READY skip is noted in output
- [ ] All 3 story files are written with correct naming: `story-[name].md`
- [ ] Skill does NOT start implementation

---

### Case 2: Failure Path — No epic file found

**Fixture:**
- The epic path provided does not exist in `production/epics/`

**Input:** `$create-stories nonexistent-epic`

**Expected behavior:**
1. Skill attempts to read the EPIC.md file
2. File not found
3. Skill outputs a clear error with the path it searched
4. Skill suggests checking `production/epics/` or running `$create-epics` first
5. No story files are created

**Assertions:**
- [ ] Skill outputs a clear error naming the missing file path
- [ ] No story files are written
- [ ] Skill recommends the correct next action (`$create-epics`)
- [ ] Skill does NOT create stories without a valid EPIC.md

---

### Case 3: Blocked Story — ADR is Proposed

**Fixture:**
- EPIC.md exists with 2 requirements
- Requirement 1 is covered by an Accepted ADR
- Requirement 2 is covered by an ADR with `Status: Proposed`

**Input:** `$create-stories [epic-name]`

**Expected behavior:**
1. Skill reads the ADR for Requirement 2 and finds Status: Proposed
2. Story for Requirement 2 is drafted with `Status: Blocked`
3. Blocking note references the specific ADR: "BLOCKED: ADR-NNN is Proposed"
4. Story for Requirement 1 is drafted normally with `Status: Ready`
5. Both stories are shown in the draft — user asked "changeset authorization" for both

**Assertions:**
- [ ] Story 2 has `Status: Blocked` in its frontmatter
- [ ] Blocking note names the specific ADR number and recommends `$architecture-decision`
- [ ] Story 1 has `Status: Ready` — blocked status does not affect non-blocked stories
- [ ] Blocked status is shown in the draft preview before applying a not-yet-authorized changeset
- [ ] Both story files are written (blocked stories are still written — just flagged)
- [ ] The story template preserves each computed status in the file and EPIC table

---

### Case 4: Edge Case — No argument provided

**Fixture:**
- `production/epics/` directory exists with ≥2 epic subdirectories

**Input:** `$create-stories` (no argument)

**Expected behavior:**
1. Skill detects no argument is provided
2. Outputs a usage error: "No epic specified. Usage: $create-stories [epic-name]"
3. Skill lists available epics from `production/epics/`
4. No story files are created

**Assertions:**
- [ ] Skill outputs a usage error when no argument is given
- [ ] Skill lists available epics to help the user choose
- [ ] No story files are written
- [ ] Skill does NOT silently pick an epic without user input

---

### Case 5: Director Gate — Full mode runs QL-STORY-READY; stories failing noted as NEEDS WORK

**Fixture:**
- EPIC.md exists with 2 requirements
- Both governing ADRs are Accepted
- `production/session-state/review-mode.txt` contains `full`
- QL-STORY-READY check finds one story has ambiguous acceptance criteria

**Input:** `$create-stories [epic-name]`

**Expected behavior:**
1. Both stories are drafted
2. QL-STORY-READY check runs for each story
3. Story 1 passes QL-STORY-READY
4. Story 2 fails QL-STORY-READY — noted as NEEDS WORK with specific feedback
5. Both stories are shown to user with pass/fail status before "changeset authorization"
6. User can proceed (story written as-is with NEEDS WORK note) or revise first

**Assertions:**
- [ ] QL-STORY-READY results appear per story in the output
- [ ] Story 2 is flagged as NEEDS WORK with the specific failing criteria
- [ ] Story 1 shows as passing QL-STORY-READY
- [ ] User is given the choice to proceed or revise before applying a not-yet-authorized changeset
- [ ] Skill does NOT auto-block writing of stories that fail QL-STORY-READY without user input

---

### Case 6: CS-001 — QA coverage fail-closed matrix

Run each variant independently with a valid epic, active TR-IDs, Accepted ADRs,
and all unrelated checks passing.

| Variant | Fixture | Expected status |
|---|---|---|
| 6a | Logic story has no QA specification | Needs Work |
| 6b | Logic story has three ACs but only two specifications | Needs Work |
| 6c | Integration story has a specification for every AC, but one test-case ID is missing or placeholder | Needs Work |
| 6d | User chooses `Defer test specs` | Needs Work; uncovered AC IDs listed |
| 6e | Visual/Feel or UI story lacks a required manual check | Needs Work |
| 6f | Logic story has one complete specification and stable test-case ID per AC | Eligible for Ready |

**Expected behavior:**

1. Builds the QA coverage result per story and per acceptance criterion
2. Uses stable IDs in the form
   `TC-[epic-slug]-S[story-number]-AC[criterion-number]` for automated cases
   and preserves each story-local AC ID when wording or order changes
3. Records `QA Coverage: Missing` and exact uncovered AC IDs when incomplete
4. Applies `Needs Work` before preview and preserves it through every rendered
   output
5. Never treats deferral, accepted risk, or a QA placeholder as complete coverage

**Assertions:**

- [ ] Missing or partial QA coverage never produces `Ready`
- [ ] Every Logic/Integration AC must have exactly one complete specification
  with a stable non-placeholder ID before the story is eligible for `Ready`
- [ ] Blank fields and `TBD`, `TODO`, `???`, or "fill later" markers count as
  missing coverage
- [ ] QA deferral is allowed only as a written non-ready planning artifact
- [ ] Preview, story header, EPIC table, and completion summary show the same
  computed status
- [ ] A stricter pre-existing `Blocked` status is never downgraded to `Needs Work`

---

### Case 7: CS-002 — Stable TR traceability fail-closed matrix

Run each variant independently with complete QA coverage, Accepted ADRs, and all
unrelated checks passing.

| Variant | Fixture | Expected status |
|---|---|---|
| 7a | Registry missing, unreadable, or invalid | Blocked for every affected story |
| 7b | GDD requirement has no registry match | Blocked |
| 7c | Candidate ID is malformed or contains `???` | Blocked; placeholder not emitted |
| 7d | Candidate ID is absent from the registry | Blocked |
| 7e | Registry entry is deprecated, superseded, or otherwise non-active | Blocked |
| 7f | Story covers two requirements and only one resolves to an active ID | Blocked; unresolved requirement listed |
| 7g | Every covered requirement resolves to an exact active ID | TR check passes |

**Expected behavior:**

1. Parses the registry and records `loaded`, `missing`, `unreadable`, or
   `invalid`
2. Uses only exact IDs whose registry entry has `status: active`
3. Does not invent, guess, renumber, or write any placeholder TR-ID
4. Produces a per-story Traceability Gaps entry with the GDD path/section,
   requirement text, and failure reason
5. Routes the consolidated gap report to `$architecture-review`, the sole
   registry-authoring workflow, without editing the registry
6. Keeps unrelated fully traced stories independently eligible for `Ready`

**Assertions:**

- [ ] No preview or file contains `TR-[system]-???` or an equivalent placeholder
- [ ] Every unresolved or non-active requirement makes only its affected story
  `Blocked`
- [ ] Gap evidence is specific enough for `$architecture-review` to register or
  repair the requirement
- [ ] The skill remains a read-only consumer of the TR registry
- [ ] The batch may still write Blocked planning artifacts after changeset
  authorization, but never offers `$dev-story` for them

---

### Case 8: QA-plan provenance is revalidated before import

**Fixture**: Provide an explicit canonical QA-plan path whose captured story
hash or one captured GDD/ADR hash differs from the current raw bytes. Repeat
with declared `PARTIAL`, effective `STALE`, an AC-ID mismatch, and ambiguous
test/check IDs.

**Expected**:

- [ ] No plan is selected by mtime, title, slug, or a "latest" filename
- [ ] Every captured source is re-hashed before any specification is imported
- [ ] `PARTIAL`, `STALE`, hash mismatch, AC drift, and ambiguous IDs are rejected
- [ ] The affected story remains at least `Needs Work`; risk acceptance cannot pass it
- [ ] A valid import records plan path, plan hash, `CURRENT`, and imported IDs

## Protocol Compliance

- [ ] All context (EPIC, GDD, ADRs, manifest, TR registry) loaded before drafting stories
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Blocked stories flagged before write approval — not discovered after writing
- [ ] TR-IDs reference the registry — requirement text is not embedded inline in story files
- [ ] Missing QA coverage and unresolved traceability are visible before write
  authorization
- [ ] No output path converts `Blocked` or `Needs Work` back to `Ready`
- [ ] `$story-readiness` remains the authoritative implementation-readiness gate;
  `$dev-story` is offered only after its final READY verdict
- [ ] Control manifest rules quoted per-story from the manifest, not invented
- [ ] Control-manifest version/hash/source snapshot match the exact bytes read
- [ ] Control-manifest normative levels and contextual rejections are not
      collapsed into a Required/Forbidden binary
- [ ] Ends with next-step handoff: `$story-readiness` → `$dev-story`

---

## Coverage Notes

- Integration story test evidence (playtest doc alternative) follows the same
  approval pattern as Logic stories — not independently fixture-tested.
- Story ordering (foundational first, UI last) is validated implicitly via
  Case 1's multi-story fixture.
- The story sizing rule (splitting large requirement groups) is not tested here
  — it is addressed in the `$create-stories` skill's internal logic.
