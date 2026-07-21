# Skill Test Spec: $team-level

## Skill Summary

`$team-level` designs or revises exactly one level. It coordinates bounded,
read-only domain specialists, routes every proposal to one destination, and
permits one transaction writer to write only the level source and its recovery
checkpoint. BLOCKING accessibility findings are non-waivable. An independent,
read-only, hash-bound `level-review` profile—not `$design-review`—must approve
the current level file before a COMPLETE verdict or implementation handoff.

The workflow may return `COMPLETE — DESIGN APPROVED`, `PARTIAL — NOT
APPROVED`, `ACCEPTED RISK / NOT APPROVED`, or `BLOCKED — PRODUCT DECISION
REQUIRED`. A file existing does not establish approval.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`;
      `name` matches the skill directory
- [ ] Has at least two numbered phase headings
- [ ] Contains the four exact workflow verdicts
- [ ] Explicitly forbids `$design-review` for level documents
- [ ] Defines a read-only level-review profile covering critical path, softlock,
      pacing, adjacency, navigation, accessibility, and encounter contracts
- [ ] BLOCKING accessibility findings have no waive/acknowledge-and-proceed path
- [ ] Initial finding IDs remain stable through at most one verification
      re-review; no recursive review/rewrite loop exists
- [ ] Every proposal has exactly one destination and verbatim aggregation is
      forbidden
- [ ] All specialists and reviewers are read-only; one transaction writer owns
      the exact level and checkpoint paths
- [ ] Approval is bound to exact paths, operations, owner, hashes, scope, and a
      deterministic plan hash
- [ ] Concurrency and agent deadlines are bounded
- [ ] Partial writes, timeouts, checkpoint fields, raw-hash resume checks, and
      rollback proof are explicit
- [ ] QA output is labeled planned; unexecuted tests or missing hashes are never
      reported as passing evidence
- [ ] Implementation is forbidden until the current level hash is independently
      reviewed and DESIGN APPROVED
- [ ] Metadata describes the single reviewed/hash-bound level-spec boundary

---

## Director Gate Checks

No system-GDD director gate is invoked. Level review is an independent,
read-only document-type profile inside this workflow. The author/transaction
writer cannot act as reviewer.

---

## Test Cases

### Case 1: Happy path — one destination-routed level reaches DESIGN APPROVED

**Fixture:**
- Input is `forest-dungeon`
- Game concept, pillars, art bible, accessibility requirements, relevant system
  GDD, and direct adjacency sources fit within the context budget
- The target level source and checkpoint are absent
- Narrative, world, art, layout, systems, and accessibility agents complete
  within their deadlines
- Accessibility returns zero BLOCKING findings
- User resolves all genuine product choices
- The exact two-path write plan is approved
- The transaction writer writes the approved draft and verifies its raw hash
- A fresh independent reviewer returns zero BLOCKING findings against that hash
- qa-tester returns a planned QA-case set bound to the same hash

**Input:** `$team-level forest-dungeon`

**Expected behavior:**
1. Builds and hashes a bounded context manifest
2. Runs only read-only specialists with at most three live agents
3. Routes every proposal to exactly one destination
4. Reduces only LEVEL SOURCE material into the draft
5. Previews and obtains one hash-bound write authorization
6. Uses one transaction writer for the exact level/checkpoint paths
7. Runs independent level-review against the verified current hash
8. Labels QA cases PLANNED and records no fabricated execution evidence
9. Requests final design acceptance as a product decision
10. Returns `COMPLETE — DESIGN APPROVED`

**Assertions:**
- [ ] Normal artifact set contains only
      `design/levels/forest-dungeon.md`
- [ ] Checkpoint is
      `production/session-state/team-level-forest-dungeon.yaml`
- [ ] Writer and reviewer are different agents
- [ ] Level-review and QA evidence bind to the final raw level hash
- [ ] No code, assets, tests, lore file, art brief, system GDD, or QA file is
      written
- [ ] No routine phase-transition approval is requested

---

### Case 2: TLD-001 — level docs never enter the system-GDD reviewer

**Fixture:**
- A valid level file is written and hashes to H1
- A tool spy records every workflow invocation and agent prompt

**Expected behavior:**
1. Runs the inline level-review profile with H1
2. Checks critical path, sequence breaks/softlocks, pacing, adjacency,
   navigation, accessibility, and encounter contracts
3. Keeps the reviewer read-only and independent from the writer
4. Does not invoke `$design-review` or apply system-GDD section requirements

**Assertions:**
- [ ] Invocation count for `$design-review` is zero
- [ ] Missing Formulas/Tuning/Economy sections are not level-review defects
- [ ] Review evidence names H1 and exact level sections
- [ ] A hash change makes H1 review evidence stale
- [ ] No reviewer writes the level source

---

### Case 3: TLD-002 — accessibility blockers cannot be acknowledged away

**Fixture:**
- Accessibility review returns `AX-forest-dungeon-001` as BLOCKING because the
  critical path distinguishes toxic water only by color

Run two variants:

| Variant | User choice | Expected |
|---|---|---|
| 3a | asks to document and continue | refuse continuation; remain BLOCKED |
| 3b | authorizes a bounded redesign | run one separate author revision and one verification re-review |

**Assertions:**
- [ ] No acknowledge/proceed option is offered for a BLOCKING finding
- [ ] QA planning, design approval, and implementation handoff do not occur
      while AX-forest-dungeon-001 is OPEN
- [ ] If the user stops, verdict is
      `BLOCKED — PRODUCT DECISION REQUIRED`
- [ ] Non-blocking accepted risk requires finding ID, bounded risk, owner,
      deadline, approved_by, and approved_at
- [ ] Any accepted-risk branch ends
      `ACCEPTED RISK / NOT APPROVED`, never COMPLETE

---

### Case 4: TLD-003 — review/revision converges or stops

**Fixture:**
- Initial review creates `AX-forest-dungeon-001`
- User approves an exact revision brief
- A separate author task changes only the approved scope
- Verification re-review observes the same blocker still open

**Expected behavior:**
1. Preserves the original finding ID and first-review evidence
2. Re-review checks only that ID plus regressions caused by the diff
3. Stops after the second observation
4. Returns `BLOCKED — PRODUCT DECISION REQUIRED`
5. Starts no third author or reviewer task

**Assertions:**
- [ ] Stable finding IDs are not regenerated per round
- [ ] Each author/reviewer task gets one bounded pass
- [ ] At most one verification re-review occurs
- [ ] New unrelated subjective scope cannot enter during verification
- [ ] No recursive review → rewrite → review loop exists

---

### Case 5: TLD-004 — destination routing prevents document contamination

**Fixture:**
- Agents return:
  - dialogue and faction history → NARRATIVE / LORE
  - asset inventory, palette, and VFX list → ART BRIEF
  - loot formula and enemy tuning → SYSTEM GDD
  - test cases → QA PLAN
  - critical path, landmark function, and encounter interface IDs → LEVEL SOURCE
  - review discussion → REVIEW ONLY

**Expected behavior:**
1. Records each proposal ID once in the routing ledger
2. Passes only LEVEL SOURCE fields to the reducer
3. Uses references for external destinations
4. Produces separate report handoffs without writing those destinations

**Assertions:**
- [ ] Level source contains no dialogue/lore prose, production asset list,
      system formula/tuning table, QA cases, or review transcript
- [ ] No `all outputs verbatim` instruction exists
- [ ] Duplicate facts are referenced, not pasted
- [ ] External destination files remain unchanged
- [ ] The level file remains the authority only for level rules

---

### Case 6: TLD-005 — mutation guard, unique writer, and fixed authorization

**Fixture:**
- All proposals are ready
- Exact plan P1 names the level path, checkpoint path, one transaction writer,
  create operations, ABSENT baselines, context/draft hashes, and write conditions
- User approves P1

Run these variants:

| Variant | Event | Expected |
|---|---|---|
| 6a | an expert attempts to write | reject the write; expert remains read-only |
| 6b | writer requests an art-brief path | stop; P1 does not authorize it |
| 6c | owner changes | invalidate P1 and require a complete new plan |
| 6d | target/source hash changes before mutation | cancel P1 with zero writes |
| 6e | unchanged P1 writes both exact targets | no per-file re-prompt |

**Assertions:**
- [ ] One and only one transaction writer owns both paths
- [ ] Every normal/recovery path is exact before approval
- [ ] Authorization does not expand by implication
- [ ] Unlisted narrative, art, system, QA, backlog, implementation, test, and
      asset paths cannot be written
- [ ] Compare-and-swap preflight uses raw SHA-256 hashes

---

### Case 7: Bounded concurrency, timeout, partial write, and checkpoint resume

Run these variants:

| Variant | Event | Expected |
|---|---|---|
| 7a | one required expert reaches its deadline | mark TIMED OUT; return PARTIAL, not COMPLETE |
| 7b | writer changes the level file and then fails; byte restoration is unsafe | preserve actual state, write PARTIAL checkpoint if possible, do not claim rollback |
| 7c | every changed byte is restored and hashes equal baselines | rollback may be reported |
| 7d | resume hashes match checkpoint | reuse only completed results whose input/output hashes match |
| 7e | resume hash differs | stop and revalidate; do not duplicate spawn or write |

**Assertions:**
- [ ] At most three agents are live
- [ ] At most one narrowed follow-up occurs before each deadline
- [ ] No indefinite wait or replacement loop occurs
- [ ] Checkpoint contains plan/context/source/baseline/current hashes, decisions,
      findings, agent states/deadlines, review round, write sets, and safe resume
- [ ] PARTIAL artifacts are never DESIGN APPROVED

---

### Case 8: Tests and evidence are never fabricated

**Fixture:**
- qa-tester proposes five cases but executes none
- Independent review completed successfully

**Expected behavior:**
1. Reports the five cases as PLANNED
2. Does not claim PASS, executed coverage, or playtest completion
3. Requires a real timestamp, exit/result, and raw log/evidence hash before
   labeling future evidence executed

**Assertions:**
- [ ] Agent prose alone is not test evidence
- [ ] Missing/timeout QA proposal prevents COMPLETE
- [ ] `$qa-plan` is a separate handoff and no QA file is written here
- [ ] No invented command, exit code, timestamp, or hash appears

---

### Case 9: Design approval and implementation are hash-gated

**Fixture:**
- Level-review approved file hash H1
- The level file is later changed and now hashes to H2

**Expected behavior:**
1. Marks H1 review and QA proposal stale
2. Does not retain DESIGN APPROVED for H2
3. Requires fresh independent evidence bound to H2
4. Does not invoke `$dev-story`, an implementation agent, or asset production

**Assertions:**
- [ ] A filename or prior approval cannot substitute for current hash evidence
- [ ] COMPLETE requires zero open blockers and matching checkpoint/evidence hash
- [ ] Implementation stories must capture the approved hash and pass their own
      readiness gate before a separate dev-story run
- [ ] Every non-COMPLETE verdict recommends only resolution/resume work

---

### Case 10: Missing or invalid target fails before project reads

**Fixture:**
- Any project state

Run empty input, path traversal, drive prefix, control character, and ambiguous
slug variants.

**Expected behavior:**
1. Prints the required argument and safe examples
2. Stops before project-file reads or delegation
3. Performs no write and emits no verdict

**Assertions:**
- [ ] No subagent is spawned
- [ ] No GDD, level, or session-state file is read
- [ ] Existing target is never overwritten under create mode
- [ ] Invalid IDs cannot escape `design/levels/`

---

### Case 11: Context and adjacency traversal remain bounded

**Fixture:**
- More than 20 candidate sources exist
- Two adjacent levels reference each other
- One authored neighbor disagrees on interface direction

**Expected behavior:**
1. Stops at one adjacency hop and records the cycle
2. Surfaces the context-budget choice instead of silently truncating
3. Classifies the neighbor `INTERFACE CONFLICT`
4. Does not auto-run another team-level workflow or invent the neighbor

**Assertions:**
- [ ] Maximum manifest is 20 files and 250 KiB unless the user explicitly
      narrows the selection
- [ ] Cycles do not recurse or crash
- [ ] File existence alone is not AUTHORED compatibility
- [ ] Interface conflict blocks approval until resolved

---

## Protocol Compliance

- [ ] User input is reserved for product decisions, accepted risk, final design
      acceptance, and exact write authorization
- [ ] Routine transitions do not re-prompt
- [ ] All expert/reviewer tasks are read-only
- [ ] Exactly one writer owns the two pre-approved paths
- [ ] All parallel batches respect the three-agent cap and deadlines
- [ ] BLOCKING findings are non-waivable
- [ ] Destination routing precedes reduction
- [ ] Level-review evidence is independent, read-only, and current-hash-bound
- [ ] Partial/timeout state is reconstructable from the checkpoint
- [ ] No test, review, hash, or completion evidence is fabricated
- [ ] No implementation begins before DESIGN APPROVED
- [ ] Verdict is one of the four declared states

---

## Coverage Notes

The catalog entry remains unchanged because shared catalog mutation is outside
this remediation boundary. No last-test fields are populated: these are static
candidate checks, not executed workflow results.

The inline level-review profile is intentionally specified here because there is
no separately authorized `level-review` skill in this changeset. Creating a
shared skill/profile and aligning other team workflows remain rollout tasks.
