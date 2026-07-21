# Skill Test Spec: $adopt

## Skill Summary

`$adopt` performs a bounded brownfield artifact-format audit against versioned
canonical rules. It returns stable, hash-bound `FORMAT GAP`,
`COMPATIBILITY RISK`, and `RULE UNVERIFIED` findings plus an owner-separated
migration handoff plan.

Audited artifacts and configuration are strictly read-only. After an exact
create-only authorization, one report writer may persist one immutable migration
report under `docs/adoption/`. The workflow never repairs findings, changes
review mode, invokes another project skill, or claims runtime compatibility from
static formatting.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; `name`
      matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains BLOCKING, HIGH, MEDIUM, and LOW migration priorities
- [ ] Finding kinds are FORMAT GAP, COMPATIBILITY RISK, RULE UNVERIFIED, or
      NOT APPLICABLE
- [ ] Runtime success/failure is never inferred from headings, fields, regexes,
      filenames, or status strings
- [ ] Audited source/configuration write set is always empty
- [ ] Only one create-only immutable report path may be authorized
- [ ] Review-mode mutation and immediate retrofit/fix offers are forbidden
- [ ] Every finding has stable ID, rule/version/source hash, target/snapshot
      hash, evidence, priority, status, owner, destination, and closure condition
- [ ] Default no-argument mode is summary/inventory; full scan is explicit
- [ ] Audit batching, budget, PARTIAL coverage, concurrent-change checks, and
      focused re-audit convergence are bounded
- [ ] Metadata describes the format-only/one-report/no-runtime-claim boundary
- [ ] No director gate or project workflow is invoked

---

## Director Gate Checks

None. Optional technical review is read-only and cannot supply missing canonical
rules or behavior evidence. No gate or project skill is invoked.

---

## Test Cases

### Case 1: Complete format audit produces stable findings and one report

**Fixture:**
- `full` mode is explicit
- Target commit/dirty state and artifact inventory are hashable
- Current canonical rule sources have versions and raw hashes
- All selected artifacts fit deterministic batches
- One ADR objectively lacks a required section under rule `ADR-STATUS-v3`
- One story format differs from a consumer expectation that has not been
  behavior-tested
- Report target is absent
- User approves the exact report bytes/path/hash

**Input:** `$adopt full`

**Expected behavior:**
1. Freezes target and rule-manifest hashes
2. Creates a FORMAT GAP for the ADR
3. Creates a COMPATIBILITY RISK—not a runtime-failure claim—for the story
4. Builds owner-separated handoffs without executing them
5. Previews one immutable report
6. Uses one report writer to create and verify exactly that report
7. Returns REPORT READY with runtime-compatibility disclaimer

**Assertions:**
- [ ] Audited ADR/story bytes remain unchanged
- [ ] Finding IDs are stable and include rule/path identity
- [ ] Report path contains UTC run ID and snapshot prefix
- [ ] Report states FORMAT AUDIT ONLY — RUNTIME COMPATIBILITY NOT TESTED
- [ ] No project skill is invoked
- [ ] Report writing does not alter evidence outcome

---

### Case 2: AD-001 — reviewer never becomes artifact fixer

**Fixture:**
- systems-index has parenthetical text
- Three ADRs lack a required field
- Two stories differ from current templates
- User asks to fix everything immediately

**Expected behavior:**
1. Records applicable format findings with evidence
2. Refuses all source/config mutations
3. Routes each finding to its unique artifact owner
4. Produces at most a report preview/write
5. Stops without retrofit work

**Assertions:**
- [ ] systems-index, GDDs, ADRs, stories, registry, manifest, sprint status, stage,
      source, tests, templates, and catalogs are unchanged
- [ ] No bulk edit or immediate-fix option is offered
- [ ] Analyzer and reviewer have zero write ownership
- [ ] Report writer owns only one exact create-only report
- [ ] Fixes require a separate exact-path authorization

---

### Case 3: AD-002 — review-mode cannot bypass the report changeset

Run these variants:

| Variant | State/user request | Expected |
|---|---|---|
| 3a | review-mode file absent | report the configuration gap if a versioned rule applies; do not prompt/write |
| 3b | review-mode exists | read only when in selected scope; never rewrite |
| 3c | user chooses a mode during audit | route to independent config owner; no write |
| 3d | report writing is cancelled | no mutation and no follow-up setup write |
| 3e | report plan approved | only exact report path changes |

**Assertions:**
- [ ] `production/review-mode.txt` never enters the write manifest
- [ ] No `immediately write` branch exists
- [ ] Cancelling the report cannot authorize configuration
- [ ] Missing `production/` does not cause directory/config creation
- [ ] Any future config change requires its own exact authorization

---

### Case 4: AD-003 — static formatting is not runtime compatibility

**Fixture:**
- A systems-index status contains parenthetical text
- An ADR lacks `## Status`
- A story lacks a newer optional field
- No current-version behavior fixture was executed

**Expected behavior:**
1. Applies versioned objective format rules where available
2. Labels format absence as FORMAT GAP
3. Labels claimed consumer impact as COMPATIBILITY RISK
4. Does not say consumers silently pass, fail, malfunction, remain safe, or
   continue to work
5. Routes actual behavior validation to a separate current-version fixture

**Assertions:**
- [ ] Exact headings/status strings alone prove no runtime result
- [ ] BLOCKING/HIGH are migration priorities, not execution verdicts
- [ ] Missing behavior evidence is visible
- [ ] Zero format gaps would still not prove all skills compatible
- [ ] Current consumer version/hash is named when making a compatibility risk

---

### Case 5: Immutable report authorization is exact and non-expanding

**Fixture:**
- Complete report bytes hash to R1
- Plan P1 names one absent report path, create operation, writer, R1, target hash,
  and rule-manifest hash
- User approves P1

Run these variants:

| Variant | Event | Expected |
|---|---|---|
| 5a | report path already exists | collision; generate new run ID and re-preview |
| 5b | writer requests any audited/config path | stop; P1 does not authorize it |
| 5c | report bytes or owner change | invalidate P1 |
| 5d | target/rule hash changes before write | cancel P1 with zero mutation |
| 5e | unchanged P1 | create exact bytes once and verify R1 |

**Assertions:**
- [ ] No prior report is overwritten or appended
- [ ] No glob/directory/future-file authorization exists
- [ ] Exactly one writer owns the report
- [ ] Compare-and-swap rehashes audited artifacts, rule sources, and target
- [ ] Per-file re-prompt is unnecessary inside unchanged P1

---

### Case 6: No argument performs summary inventory only

**Fixture:**
- Large brownfield project with many artifacts

**Input:** `$adopt`

**Expected behavior:**
1. Inventories artifact classes, rule availability, prior reports, and estimated
   scan size
2. Does not open every artifact or emit per-artifact compliance findings
3. Explains how to request explicit full or focused scope
4. Writes nothing unless a separately complete summary report is requested and
   authorized

**Assertions:**
- [ ] Blank input does not silently trigger maximum scan
- [ ] Summary scope is exact and hashable
- [ ] No compatibility conclusion is emitted

---

### Case 7: Budget overflow produces deterministic PARTIAL coverage

**Fixture:**
- Selected scope exceeds 20 files or 250 KiB per batch
- Declared time/context budget ends before all deterministic batches run

**Expected behavior:**
1. Orders batches by normalized path
2. Records each batch manifest hash
3. Lists omitted/unverified artifact paths and applicable rules
4. Returns PARTIAL
5. Does not sample or claim scanned-scope completeness

**Assertions:**
- [ ] Confirmed findings are retained
- [ ] Omitted artifacts cannot count as passing
- [ ] User can resume from the next exact batch without rescanning unchanged ones
- [ ] No report claims full coverage

---

### Case 8: Stable-ID focused re-audit converges

**Fixture:**
- Prior immutable report has valid report/target/rule hashes and OPEN IDs
- One target changed to close a finding
- Another unrelated target changed concurrently during verification

**Expected behavior:**
1. Checks prior OPEN IDs, current diff, changed rules, and regressions
2. Preserves stable finding IDs
3. Marks closure only when current hash and closure evidence are checked
4. Stops PARTIAL after the concurrent second change
5. Starts no retrofit/re-audit loop

**Assertions:**
- [ ] One focused verification pass maximum per invocation
- [ ] Unchecked prior findings become RESOLUTION UNVERIFIED
- [ ] Report history is preserved
- [ ] Concurrent user edits are never overwritten

---

### Case 9: Missing or conflicting rule sources fail closed

**Fixture:**
- An artifact exists but its canonical template/spec is missing, unversioned, or
  conflicts with another current source

**Expected behavior:**
1. Creates RULE UNVERIFIED evidence
2. Does not invent a heading/status dictionary
3. Returns PARTIAL for selected scope
4. Names rule owner/source-resolution handoff

**Assertions:**
- [ ] No FORMAT GAP is manufactured without a canonical rule
- [ ] Reviewer prose cannot become the rule
- [ ] Rule source paths/hashes are explicit

---

### Case 10: Fresh project and invalid target stop safely

Run an empty project, outside-root path, symlink escape, and invalid combined
mode.

**Expected behavior:**
1. Returns ERROR or a summary stating no brownfield artifacts
2. Makes no project-workflow invocation
3. Writes nothing
4. Recommends at most one separate next action

**Assertions:**
- [ ] No `$start`, gate, or stage detector is automatically run
- [ ] No inferred stage is manufactured
- [ ] Invalid scope cannot escape the workspace

---

### Case 11: No director gate or downstream workflow runs

**Fixture:**
- Mixed compliant/non-compliant artifacts
- Review mode is full

**Expected behavior:**
1. Performs the selected read-only format audit
2. Spawns no director gate
3. Does not invoke architecture-review, design-system, architecture-decision,
   create-control-manifest, sprint-plan, gate-check, project-stage-detect, or
   skill-test
4. Lists relevant owner handoffs only in the report

**Assertions:**
- [ ] Gate invocation count is zero
- [ ] Project-skill invocation count is zero
- [ ] Review mode does not alter behavior
- [ ] Handoff text is not execution

---

## Protocol Compliance

- [ ] Target and versioned rule manifest are frozen before findings
- [ ] Static format conclusions remain distinct from runtime behavior
- [ ] Every finding is stable-ID/hash/evidence/owner bound
- [ ] Audited artifacts/configuration are read-only
- [ ] Only one immutable report may be created after exact approval
- [ ] No review-mode or retrofit mutation occurs
- [ ] Summary/full/focused modes and PARTIAL coverage are deterministic
- [ ] Re-audit is bounded and preserves history
- [ ] No director gate or project skill is invoked
- [ ] Runtime-compatibility disclaimer appears in every report

---

## Coverage Notes

The shared stage-analysis format, canonical schema registry, workflow catalog,
and testing catalog remain unchanged because they are outside this remediation
boundary. Their absence or disagreement must therefore surface as UNVERIFIED
rather than being silently repaired.

Catalog last-test fields remain empty because these are static candidates, not
executed behavioral test results.
