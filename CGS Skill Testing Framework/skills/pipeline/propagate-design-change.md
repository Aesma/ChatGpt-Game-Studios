# Skill Test Spec: $propagate-design-change

## Skill Summary

`$propagate-design-change` handles reproducible GDD revision cascades. It
requires an explicit baseline or a retrievable last-approved GDD baseline,
records baseline/current hashes, and traces the complete reverse graph from GDD
requirements through the TR registry, ADRs, epics, stories, and sprint work. It
distinguishes a complete no-impact result from a partial scan. It never changes
an Accepted ADR to Superseded until a concrete Accepted replacement exists and
the old ADR plus registry projections can transition atomically.

### Case 1: Full downstream impact — TR, ADR, epic, stories, and sprint work

**Fixture:**

- `design/gdd/[system].md` differs from baseline commit `BASE`
- the baseline and current file bytes have known SHA-256 hashes
- `docs/architecture/tr-registry.yaml` maps the changed requirement to
  `TR-[system]-001`
- one Accepted ADR, one epic, and two stories reference that TR-ID
- `production/sprint-status.yaml` includes one of the stories
- all required directories and files can be inventoried and parsed

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. The skill resolves the exact baseline and current bytes and reports both
   hashes plus the diff range.
2. It scans all six required layers: GDD, TR registry, ADR, epic, story, and
   sprint/work.
3. It traverses `GDD -> TR -> ADR -> epic -> story -> sprint` and reports the
   one epic and both stories, retaining the evidence edges.
4. It presents coverage, the full impact report, and all cautions before any
   resolution or write.
5. Any proposed writes are included in one bounded changeset.

**Assertions:**

- [ ] Baseline locator/path/hash, current path/hash, and diff range are present
- [ ] Coverage table shows every required layer SCANNED or KNOWN EMPTY
- [ ] Impact report identifies the one epic and both affected stories
- [ ] TR and ADR edges leading to those artifacts are visible
- [ ] Sprint membership/status is included for the tracked story
- [ ] Uses existing bounded authorization or one complete changeset approval
- [ ] Analysis verdict is COMPLETE only after full coverage is proven

---

### Case 2: No impact requires complete scan coverage

**Fixture:**

- `design/gdd/[system].md` differs from a valid explicit baseline
- the TR registry parses and maps every changed requirement unambiguously
- no ADRs, stories, epics, or sprint work reference the changed TR-IDs or GDD
  path
- every required artifact location can be inventoried and parsed

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. The skill verifies and hashes the baseline and current GDD.
2. It scans every required reverse-graph layer.
3. It finds no downstream references.
4. It outputs: "No downstream impact found for [system].md — no artifacts
   reference the changed requirements."
5. No write operation or authorization prompt occurs.

**Assertions:**

- [ ] Verdict is NO IMPACT only after complete coverage is shown
- [ ] No write operations are performed
- [ ] The skill does not error when artifact collections are KNOWN EMPTY
- [ ] The skill does not confuse NO IMPACT with NO CHANGE

---

### Case 3: Partial layer scan cannot become NO IMPACT

**Fixture:**

- the baseline is valid and the GDD has a real diff
- ADR, epic, and story scans find no references
- `docs/architecture/tr-registry.yaml` is missing or unparseable, or one required
  story/sprint source cannot be read

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. The failed source and layer are listed in the coverage table.
2. The affected layer is PARTIAL.
3. The skill reports unresolved coverage and does not claim there are no
   downstream impacts.
4. No director verdict or successful writes upgrade the scan result.

**Assertions:**

- [ ] Verdict is PARTIAL
- [ ] Output does not contain a NO IMPACT or COMPLETE verdict
- [ ] Exact failed/unparsed sources are named
- [ ] Successfully scanned empty layers do not hide the failed layer

---

### Case 4: In-progress story warning

**Fixture:**

- an affected story references the changed TR-ID
- the story or `production/sprint-status.yaml` marks it `In Progress`

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. The skill identifies the active story through the reverse graph.
2. It emits: "CAUTION: [story-file] is currently In Progress in [source] — a
   developer may be working on this. Coordinate before updating."
3. The warning appears in the impact report and again before any changeset
   authorization.
4. The story is not silently modified.

**Assertions:**

- [ ] Active work has an elevated warning distinct from normal impact entries
- [ ] Story and sprint status sources are reconciled
- [ ] A disagreement is treated as active work and Needs Review
- [ ] Other artifacts do not inherit the warning

---

### Case 5: Unknown or ambiguous baseline fails closed

**Fixture variants:**

- no `--baseline` and no retrievable approved baseline record;
- an approved hash exists but baseline bytes cannot be retrieved;
- the current path is absent at the baseline and rename resolution is ambiguous;
- an approved record's expected hash does not match its bytes.

**Input:** `$propagate-design-change design/gdd/[system].md`

**Expected behavior:**

1. The skill explains which baseline requirement failed.
2. It does not substitute `HEAD` or another guessed revision.
3. It stops before downstream impact conclusions.
4. It records BLOCKED rather than new-file/no-impact.

**Assertions:**

- [ ] Verdict is BLOCKED
- [ ] No NO IMPACT or COMPLETE verdict is emitted
- [ ] No files are changed
- [ ] Candidate rename paths are shown when rename resolution is ambiguous

---

### Case 6: Dirty workspace and rename remain reproducible

**Fixture:**

- `--baseline BASE --baseline-path design/gdd/old-name.md` resolves baseline
  bytes
- the current renamed GDD has uncommitted edits
- expected SHA-256 hashes for both byte sequences are known

**Input:** `$propagate-design-change design/gdd/new-name.md --baseline BASE --baseline-path design/gdd/old-name.md`

**Expected behavior:**

1. The skill reads the old baseline path and current workspace path.
2. It hashes the exact bytes from each source.
3. It reports the rename and diff range without requiring the current file to be
   committed.
4. Re-analysis pins the same hash pair.

**Assertions:**

- [ ] Both paths and both expected hashes are reported
- [ ] Dirty current content is analyzed rather than silently replaced by HEAD
- [ ] Re-analysis does not advance the baseline
- [ ] No guessed rename is used

---

### Case 7: Replacement ADR must be Accepted before supersedure

**Fixture variants:**

- the old ADR is Accepted and no replacement exists;
- a replacement exists but is Proposed;
- an Accepted replacement exists, explicitly supersedes the old ADR, and covers
  the affected active TR-IDs.

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. With no replacement or a non-Accepted replacement, the old ADR remains
   Accepted and the report records "Needs Review — replacement required."
2. No placeholder replacement ID is written anywhere.
3. With a qualifying Accepted replacement, the skill previews one atomic group
   containing the old ADR and every affected registry/traceability projection.
4. A hash conflict or inability to apply the whole group results in zero
   transition writes and BLOCKED.

**Assertions:**

- [ ] Old ADR status is unchanged until the replacement is Accepted
- [ ] No placeholder or future ADR ID is used
- [ ] Accepted replacement has an explicit supersedes link and required TR coverage
- [ ] Old ADR and registry projections change together or not at all
- [ ] Post-write verification names the concrete replacement ID everywhere

---

### Case 8: Edge case — no argument provided

**Fixture:** multiple GDDs exist in `design/gdd/`.

**Input:** `$propagate-design-change`

**Expected behavior:**

1. The skill outputs: "No GDD specified. Usage:
   $propagate-design-change design/gdd/[system].md --baseline
   <git-ref-or-approved-baseline>"
2. It may list recently modified GDDs as suggestions.
3. It does not silently select a target or perform analysis.

**Assertions:**

- [ ] Usage error includes the target path and baseline requirement
- [ ] No impact analysis is performed
- [ ] No GDD is selected without user input

---

### Case 9: Director gate — no gate spawned regardless of review mode

**Fixture:**

- a GDD has a valid baseline and downstream references
- `production/session-state/review-mode.txt` exists with `full`

**Input:** `$propagate-design-change design/gdd/[system].md --baseline BASE`

**Expected behavior:**

1. The skill reads the GDD and traces downstream references.
2. It does not read `production/session-state/review-mode.txt`.
3. No director gate agents are spawned.
4. The impact report is produced with the full P0 evidence.

**Assertions:**

- [ ] No director gate agents are spawned
- [ ] Review mode is not read
- [ ] Output contains no gate or gate-skipped entries
- [ ] Review mode has no effect on the P0 evidence

---

## Protocol Compliance

- [ ] Exact baseline/current paths, locators, hashes, and diff range are recorded
- [ ] Explicit baseline or retrievable approved baseline is required
- [ ] GDD, TR registry, ADR, epic, story, and sprint/work layers are inventoried
- [ ] Direct path edges supplement stable TR-ID traversal
- [ ] PARTIAL never becomes NO IMPACT or COMPLETE
- [ ] Active stories are elevated before authorization
- [ ] No authoritative ADR supersedure precedes a concrete Accepted replacement
- [ ] ADR plus registry transition is atomic and hash-guarded
- [ ] One bounded authorization covers the complete exact write set

---

## Coverage Notes

- Stable impact IDs, immutable report paths, resolution lifecycle fields, scan
  budgets, and owner-lock coordination are outside these P0 cases.
- The pre-existing implementation/spec director-gate mismatch is outside these P0
  cases and remains a separate remediation.
