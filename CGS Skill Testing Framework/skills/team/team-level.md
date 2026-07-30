# Skill Test Spec: $team-level

## Candidate status

`NOT EXECUTED` — this P1 candidate reconstructs the full test structure and
defines assertions only. It does not claim static/spec/category execution,
subagent behavior, writes, review, QA evidence, design approval, or catalog
`last_*` results.

## Skill summary

`$team-level` designs or revises one level specification. It validates one level
ID before reads, ignores generic review mode, builds bounded context/adjacency
manifests, coordinates deterministic read-only jobs with deadlines and partial
states, routes every proposal to one destination, and gives one authorized writer
the exact level/checkpoint paths. Independent accessibility and level-review
evidence precede QA planning against the final current source revision. COMPLETE is
an explicit version-bound evidence matrix, not file production.

The only workflow verdicts are:

```text
COMPLETE — DESIGN APPROVED
PARTIAL — NOT APPROVED
ACCEPTED RISK / NOT APPROVED
BLOCKED — PRODUCT DECISION REQUIRED
```

## Contract sources

- `.agents/skills/team-level/SKILL.md`
- `.agents/skills/team-level/references/team-level-contract-v1.md`
- `.agents/skills/team-level/references/continued-workflow.md`
- `.agents/skills/team-level/agents/openai.yaml`

All candidate-local relative links must resolve inside the candidate package.
The shared catalog remains outside this candidate write boundary.

## Authoritative P1 traceability

| Audit ID | Required closure | Structural/behavioral coverage |
|---|---|---|
| `TLD-006` | Missing/invalid single target fails before reads/delegation/verdict | Static 4; Cases 2–3 |
| `TLD-007` | Ask only product/risk/final-write/final-acceptance decisions, not routine transitions | Static 5; Cases 4–5 |
| `TLD-008` | Review mode is removed; no solo/director contradiction or hidden quality downgrade | Static 6; Case 6 |
| `TLD-009` | Bounded context manifest, one-hop dependencies, excerpt/revision prompts, no verbatim context | Static 7–8; Cases 7–8 |
| `TLD-010` | Job deadline/state/timeout and coherent PARTIAL behavior are deterministic | Static 9–10; Cases 9–10 |
| `TLD-011` | COMPLETE binds target revision, blockers, dependencies, jobs, independent review, QA, acceptance, checkpoint | Static 11; Cases 11–12 |
| `TLD-012` | QA runs only after final integrated/reviewed current level revision and becomes stale on change | Static 12; Cases 13–14 |
| `TLD-013` | Adjacency uses stable directional interfaces and planned/authored/broken/conflict states with reverse validation | Static 13; Cases 15–16 |
| `TLD-014` | Every phase has checkpoint state; version-bound resume is idempotent and avoids duplicate work | Static 14; Cases 17–19 |
| `TLD-015` | Spec structure is complete and catalog remains blank until real evidence | Static 15–16; Case 20 |

Exactly these ten IDs are authoritative P1 scope. P0 preservation cases are
regressions, not additional P1 findings.

---

## Static assertions

1. [ ] Frontmatter contains only `name` and non-empty `description`; name equals
   `team-level`.
2. [ ] Both private relative references exist and are fully linked.
3. [ ] All four exact workflow verdicts are present; file production and risk
   acceptance are explicitly insufficient for COMPLETE.
4. [ ] Invocation requires exactly one safe level ID before any project read or
   delegation; invalid input emits no verdict.
5. [ ] User prompts are limited to enumerated operation/context/product/risk/
   blocker/write/final-acceptance decisions; routine transitions auto-continue.
6. [ ] Review mode is explicitly inapplicable, its file is unread, and full/lean/
   solo cannot remove, substitute, or downgrade required roles/evidence.
7. [ ] Context limits cover files, aggregate/excerpt/prompt bytes, explicit first-
   level references, and one-hop adjacency; over-limit required choices are shown
   rather than silently truncated.
8. [ ] Job prompts use manifest identity, selected excerpt revisions, and structured
   predecessor records, never all source documents or outputs verbatim.
9. [ ] Every job has stable ID, role, required flag, input/output revisions/schema,
   deadline, one bounded follow-up, status, result payload/revision, and dependency
   IDs; concurrency/jobs/result sizes are bounded.
10. [ ] Required timeout/invalid/missing result prevents COMPLETE, preserves valid
    independent results, and returns coherent PARTIAL only with an exact resume
    point.
11. [ ] `TL-COMPLETE/v1` lists all twelve predicates including target revision, agent
    completion, blockers, dependency state, independent current-revision review,
    current-revision QA, user acceptance, writer identity, and COMPLETE checkpoint.
12. [ ] QA input is the final persisted/reviewed level revision; any later level byte
    change stales review and QA and no QA file/PASS evidence is produced here.
13. [ ] Adjacency records have stable directional IDs/endpoints/reverse refs and
    exactly `PLANNED|AUTHORED|UNRESOLVED|BROKEN_LINK|INTERFACE_CONFLICT`; file
    existence is insufficient.
14. [ ] `cgs.team-level-checkpoint/v2` is constructed after every phase, stores
    bounded job payloads/revisions and monotonic sequence, and resumes from the
    earliest stale dependency without duplicate dispatch/write/review/QA.
15. [ ] This spec has Candidate status, summary, sources, P1 trace, static
    assertions, director/profile section, complete numbered cases with fixtures/
    expected behavior/assertions, protocol compliance, and verification boundary.
16. [ ] Candidate remains `NOT EXECUTED`; it neither mutates shared catalog nor
    claims/populates any `last_*` field.
17. [ ] `$design-review` is forbidden for level documents; private
    `cgs.level-review/v1` is independent/read-only/current-version-bound.
18. [ ] BLOCKING findings are non-waivable, stable across one verification
    re-review, and stop after observation two if still open.
19. [ ] Every proposal/finding routes once; reducer allowlist excludes lore,
    production art, formulas/tuning, QA bodies, backlog, review transcripts, and
    raw outputs.
20. [ ] Exactly one transaction writer owns the two planned paths and all other
    roles are read-only.

## Review profile checks

No system-GDD director gate is invoked. The private `cgs.level-review/v1`
profile checks critical-path continuity, sequence breaks/softlocks/recovery,
pacing, bidirectional adjacency compatibility, navigation/wayfinding,
accessibility, and encounter interface/dependency boundaries. Reviewer identity
must differ from every author and the transaction writer.

---

## Case 1: Happy path reaches version-bound DESIGN APPROVED

**Fixture:**

- `forest-dungeon` is a valid absent target; CREATE is unambiguous.
- Required sources fit bounds; adjacency interfaces validate.
- Every applicable job completes before deadline with valid result revisions.
- Routing/reducer allowlists pass and accessibility has zero blockers.
- The user authorizes the exact two-path plan; writer verifies both writes.
- Independent level-review passes the current raw level revision.
- QA returns PLANNED cases bound to that same revision/review result.
- User accepts the exact final packet and authorizes its exact COMPLETE-
  checkpoint candidate; that separate compare-and-set verifies.

**Input:** `$team-level forest-dungeon`

**Expected behavior:** all twelve `TL-COMPLETE/v1` predicates are true and the
only verdict is `COMPLETE — DESIGN APPROVED`.

**Assertions:**

- [ ] Only level and checkpoint paths are mutated
- [ ] Every specialist/reviewer/QA job remains read-only
- [ ] Review, QA, acceptance, level, plan, context, and checkpoint revisions agree
- [ ] Final acceptance does not authorize implementation

---

## Case 2: Missing level ID stops before every project read

**Fixture:** arbitrary project content and agent availability.

**Input:** `$team-level`

**Expected behavior:** usage and safe examples; `run_status: ERROR`; no project
read, subagent, user prompt, write, or workflow verdict.

**Assertions:**

- [ ] No AGENTS/GDD/level/session file is read
- [ ] No target paths are inferred from an empty string
- [ ] No verdict is emitted

---

## Case 3: Invalid/extra target input is a zero-read error

**Variants:** traversal, path separator, drive/device prefix, Unicode lookalike,
whitespace, repeated/edge hyphen, wildcard/regex, and two positional IDs.

**Expected behavior:** same boundary as Case 2. Ambiguous normalization is
rejected instead of silently creating another slug.

**Assertions:**

- [ ] Project read and agent-dispatch counts are zero
- [ ] No invalid value reaches either target path
- [ ] No workflow verdict is emitted

---

## Case 4: Routine phase transitions never prompt

**Fixture:** valid deterministic happy path with no product conflict, context
overflow, blocker, write boundary, or final acceptance yet.

**Expected behavior:** target validation → context → proposals → author → systems/
art → accessibility → routing/reduction transitions automatically. No “approve
the summary/continue to next step?” question occurs.

**Assertions:**

- [ ] Routine prompt count is zero
- [ ] Read-only prerequisites still execute in order
- [ ] Absence of a routine confirmation is not recorded as approval

---

## Case 5: Every permitted question has a stable decision boundary

**Variants:** existing-target operation choice; context over-budget selection;
cross-domain product alternatives; non-blocking risk; blocker revision/stop;
write plan; changed-plan replacement; final packet acceptance.

**Expected behavior:** each question names stable IDs, exact choices/effects and
default non-mutating outcome. No response is inferred. A material plan change
invalidates old authorization. Final product acceptance binds the exact final
checkpoint candidate and authorizes only that transition.

**Assertions:**

- [ ] Every prompt maps to one enumerated condition
- [ ] Product and write decisions remain distinct
- [ ] Unanswered prompts cause no mutation or acceptance

---

## Case 6: Review mode cannot alter behavior

**Fixture:** full, lean, solo, malformed, and absent review-mode files in separate
runs; one run also passes `--review solo`.

**Expected behavior:** files are never read and normal runs select the same
required roles/evidence. The option-bearing invocation is rejected before project
reads; solo cannot suppress an independent reviewer or create a self-review.

**Assertions:**

- [ ] Review-mode read count is zero
- [ ] Required-role matrix is identical across filesystem variants
- [ ] Unsupported review option fails before project evidence

---

## Case 7: Context budget and dependency depth fail closed

**Fixture:** 21 candidate files, more than 250 KiB raw text, oversized excerpts,
and a cycle across adjacent levels beyond one hop.

**Expected behavior:** exact included/omitted candidates and exceeded limits are
shown for user prioritization before delegation. Cycle is recorded once; no
recursive crawl or silent truncation occurs.

**Assertions:**

- [ ] No job starts before a bounded manifest freezes
- [ ] Adjacency depth never exceeds one hop
- [ ] User selection binds both included and omitted rows

---

## Case 8: Agent prompts receive excerpts and references, not full context

**Fixture:** a large lore document, system GDD, art bible and prior proposals;
prompt recorder captures every dispatched payload.

**Expected behavior:** each prompt remains within 96 KiB, binds context/excerpt/
predecessor revisions, and contains only task-relevant excerpts/structured records.
No full-project dump or accumulated verbatim transcript appears.

**Assertions:**

- [ ] Every excerpt has a source section and revision
- [ ] Prompt byte limit is enforced before dispatch
- [ ] Prior agent output is structured, not transcript concatenation

---

## Case 9: Deadline and failure state are deterministic

**Variants:** result before deadline; one narrowed follow-up; no result by exact
deadline; late result; malformed/over-limit result; duplicate differing results.

**Expected behavior:** COMPLETE, same-deadline follow-up, TIMED_OUT, recorded-late
but not complete, INVALID, and INVALID respectively. No deadline extension,
unbounded wait, forged result, or replacement loop occurs.

**Assertions:**

- [ ] One job ID/input revision persists through the permitted follow-up
- [ ] Late/duplicate output cannot become valid COMPLETE evidence
- [ ] At most three jobs are live and at most sixteen exist in the run

---

## Case 10: Core evidence can return PARTIAL without pretending COMPLETE

**Fixture:** context identity and coherent level draft exist; an applicable
required systems proposal times out while independent completed results remain
valid.

**Expected behavior:** preserve completed payloads/revisions, mark required job
TIMED_OUT, return `PARTIAL — NOT APPROVED`, and identify the exact checkpoint
resume phase. If no coherent draft exists, return BLOCKED instead.

**Assertions:**

- [ ] Valid independent results are not discarded or forged
- [ ] Required timeout always makes the COMPLETE predicate false
- [ ] Resume action identifies one earliest phase

---

## Case 11: COMPLETE matrix blocks every missing predicate

**Fixture:** run twelve variants, making exactly one `TL-COMPLETE/v1` predicate false or
unknown in each.

**Expected behavior:** none emits COMPLETE or asks final acceptance while a
precondition is missing. Output names predicate ID and evidence gap; once all are
true/current, the final packet may be accepted.

**Assertions:**

- [ ] All twelve predicates are individually observed
- [ ] False and unknown are both fail-closed
- [ ] Final acceptance is bound to the all-true matrix revision

---

## Case 12: A produced file or accepted risk is never approval

**Variants:** source write succeeds before review; non-blocking risk is accepted;
checkpoint says COMPLETE but current level revision differs.

**Expected behavior:** respectively PARTIAL, `ACCEPTED RISK / NOT APPROVED`, and
STALE/PARTIAL. None is `COMPLETE — DESIGN APPROVED`.

**Assertions:**

- [ ] File existence is not an approval predicate substitute
- [ ] Accepted risk cannot waive a blocking or COMPLETE predicate
- [ ] Checkpoint prose cannot override current raw bytes

---

## Case 13: QA is generated after final integrated source and review

**Fixture:** initial draft H0 is integrated/written as H1; accessibility closes;
independent level-review passes H1.

**Expected behavior:** qa-tester first dispatch occurs only after H1 persistence
and review PASS, and inputs bind H1 plus review/finding revisions. Cases are PLANNED;
no QA file, test execution, PASS, or coverage claim appears.

**Assertions:**

- [ ] QA dispatch sequence follows current-revision review PASS
- [ ] Every QA case references H1 sections/entities
- [ ] QA write and execution counts are zero

---

## Case 14: Post-QA source change stales review and QA

**Fixture:** review/QA bind H1; source changes to H2 before final acceptance.

**Expected behavior:** both evidence sets become STALE; COMPLETE is impossible;
workflow returns to fresh independent review of H2 and then fresh QA. Reducer
cannot silently patch H1 after QA freezes.

**Assertions:**

- [ ] H1 evidence is never applied to H2
- [ ] Review precedes regenerated QA
- [ ] Final packet cannot retain stale revisions

---

## Case 15: PLANNED and AUTHORED adjacency use explicit contracts

**Variants:** absent target with current roadmap interface/owner/reverse contract;
two authored levels with matching forward/reverse IDs/endpoints/direction/state.

**Expected behavior:** states PLANNED and AUTHORED respectively with stable
interface/source revisions. Filename presence or absence alone does not decide.

**Assertions:**

- [ ] PLANNED names roadmap declaration and owner
- [ ] AUTHORED validates both directions and revisions
- [ ] Stable interface identity excludes volatile prose

---

## Case 16: Broken and conflicting adjacency block approval

**Variants:** declared authored target missing; missing reverse reference;
direction mismatch; endpoint mismatch; traversal-state mismatch; revision
conflict; missing undecided declaration.

**Expected behavior:** BROKEN_LINK, BROKEN_LINK, INTERFACE_CONFLICT variants, and
UNRESOLVED. Required cases prevent COMPLETE, record owner/action, stop one-hop
traversal, and never auto-run another team-level workflow.

**Assertions:**

- [ ] Every state follows the deterministic interface matrix
- [ ] Required unresolved states make dependency predicate false
- [ ] Downstream workflow invocation count is zero

---

## Case 17: Every phase produces a monotonic checkpoint snapshot

**Fixture:** happy path through context, batches, author, accessibility, reducer,
write, review, QA, and final acceptance.

**Expected behavior:** in-memory/persisted snapshots increment `state_seq`, bind
phase/source/target/job/result/decision/finding revisions, and retain one exact safe
resume action. Pre-authorization snapshots cause zero project writes.

**Assertions:**

- [ ] Sequence is strictly monotonic with no duplicate accepted transition
- [ ] Stored job results include bounded payload and matching revision
- [ ] Only planned checkpoint transitions persist after authorization

---

## Case 18: Resume reuses exact completed work once

**Fixture:** valid persisted checkpoint with matching context/target revisions and
stored bounded COMPLETE job payloads/results; run stopped before level review.

**Expected behavior:** completed proposals/write/decisions are reused without
redispatch/rewrite; resume begins at review. Job IDs, observation count and write
receipts are not duplicated.

**Assertions:**

- [ ] Reused job input/payload/result revisions all verify
- [ ] Existing target bytes equal checkpoint current revision
- [ ] Dispatch and write counts remain unchanged for reused work

---

## Case 19: Stale checkpoint returns to earliest affected phase

**Variants:** changed context source; corrupted stored job payload; changed target
bytes; stale review revision; missing QA payload with matching claimed revision.

**Expected behavior:** dependent records become STALE and resume starts at
context/job/write/review/QA respectively. Prose-only claims are rejected and no
valid earlier independent result is unnecessarily rerun.

**Assertions:**

- [ ] Earliest stale dependency determines resume phase
- [ ] Independent still-valid records retain their revisions/status
- [ ] No prose-only or missing payload is reusable evidence

---

## Case 20: Rebuilt spec structure and catalog evidence boundary

**Fixture:** static parser inspects this candidate and shared catalog entry remains
with blank `last_*` values.

**Expected behavior:** all required top-level sections exist; Cases 1–25 are
unique/contiguous and contain Fixture, Expected behavior, and Assertions blocks;
P1 table contains exactly TLD-006..TLD-015. Candidate reports NOT EXECUTED and
does not edit/claim catalog results.

**Assertions:**

- [ ] Case headings are unique and contiguous
- [ ] Every case has all three required blocks
- [ ] Shared catalog bytes and blank result fields remain unchanged

---

## Case 21: Level document never enters system-GDD design review

**Fixture:** current level revision H1 exists and invocation recorder is active.

**Expected behavior:** private `cgs.level-review/v1` reviews H1 with correct level
criteria. `$design-review` invocation count is zero; missing Formula/Tuning/
Economy sections are not defects; reviewer cannot write.

**Assertions:**

- [ ] Reviewer identity differs from authors/writer
- [ ] Result binds H1 and exact level sections
- [ ] System-GDD review/gate invocation count is zero

---

## Case 22: Accessibility blocker cannot be acknowledged away

**Fixture:** `AX-forest-dungeon-*` BLOCKING finding identifies a color-only
critical-path cue.

**Expected behavior:** only exact author revision or stop is offered. QA, design
acceptance and implementation handoff remain forbidden while OPEN. A request to
“document and continue” returns `BLOCKED — PRODUCT DECISION REQUIRED`.

**Assertions:**

- [ ] BLOCKING has no accepted-risk record
- [ ] Open blocker count remains positive until verified closure
- [ ] No QA, acceptance, or implementation job starts while open

---

## Case 23: Destination routing and single-writer guard

**Fixture:** proposals contain dialogue, asset palette/VFX list, loot formula,
test cases, backlog item, review discussion, and spatial level constraints; an
expert attempts to write an art brief.

**Expected behavior:** every item routes once; only spatial allowlist enters level
source; external content is referenced, not pasted; expert write is rejected.
Only the permanent writer can touch the exact level/checkpoint paths.

**Assertions:**

- [ ] Routing ledger cardinality equals unique proposal/finding cardinality
- [ ] Forbidden bodies are absent from canonical level bytes
- [ ] External destination and specialist write sets are empty

---

## Case 24: Review convergence stops after observation two

**Fixture:** original accessibility or level-review blocker remains open after one
authorized scoped revision and verification re-review.

**Expected behavior:** original stable ID persists, diff regressions link to it,
second observation stops `BLOCKED — PRODUCT DECISION REQUIRED`, and no third
author/reviewer is dispatched.

**Assertions:**

- [ ] Original identity/ID is unchanged across observations
- [ ] Re-review scope contains only original IDs and diff regressions
- [ ] Observation count never exceeds two

---

## Case 25: Compare-and-set write and partial recovery are honest

**Variants:** source changes before first write; CREATE target collision; level
write succeeds but checkpoint fails; all changed bytes restore; changed bytes do
not restore.

**Expected behavior:** first two write nothing; checkpoint failure prints bounded
`RECOVERY CHECKPOINT NOT PERSISTED`; rollback is claimed only for byte-identical
verified restoration; otherwise actual revisions and PARTIAL state are preserved.
No unlisted path or replacement writer is used.

**Assertions:**

- [ ] Every write is covered by the exact plan revision and single owner
- [ ] Compare-and-set occurs immediately before mutation
- [ ] Partial/rollback claims match reread raw target bytes

---

## Protocol compliance

- [ ] Input validation precedes all project reads and delegation.
- [ ] Routine transitions continue without prompts.
- [ ] Context/adjacency manifests precede jobs.
- [ ] Every job is bounded, read-only, deadline-bound, and checkpointed.
- [ ] Accessibility review precedes source authorization.
- [ ] Destination routing/reducer allowlist precede source bytes.
- [ ] One complete authorization precedes first mutation.
- [ ] Independent current-revision level review precedes QA.
- [ ] Final current-revision QA precedes design acceptance.
- [ ] COMPLETE matrix and final compare-and-set precede the verdict.
- [ ] No implementation, external destination, test execution, or shared catalog
      mutation occurs.

## Verification boundary

Static inspection can verify structure, exact P1 trace, invocation/gate/mode
contracts, limits, schemas, state machines, ordering, relative links, write
boundaries, and defined cases. It cannot claim agent deadlines, concurrency,
filesystem compare-and-set/rollback, reviewer independence, QA generation,
catalog results, or DESIGN APPROVED behavior in a real run. All behavioral cases
remain `NOT EXECUTED` pending separate authorized testing with immutable receipts.

## Integration notes

- `cgs.level-review/v1` is a private inline profile in this candidate; there is
  no separately installed/shared `$level-review` skill here.
- Shared catalog `last_*` fields must remain blank until static/spec/category
  tests actually run and their immutable receipts are reviewed.
- Pre-authorization phase snapshots are in-memory only so unknown future bytes
  are not pre-authorized; rollout must not claim crash-resume durability until
  the first exact checkpoint candidate has been authorized and persisted.
- A rollout must copy the skill, both private references, metadata, and spec as
  one revision-reviewed unit; copying only `SKILL.md` leaves required links missing.
