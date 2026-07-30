# Skill Test Spec: `$design-review`

## Skill Summary

`$design-review` contract `cgs.design-review/v2` is a strictly read-only quality
gate for exactly one system GDD at `design/gdd/<system-slug>.md`. It validates
substantive eight-section content, reviews only declared first-level interfaces,
emits stable destination-aware findings, applies mechanical gate precedence,
binds its report and approval to exact bytes, and stops after one pass.

It never revises a document, updates `systems-index.md`, writes a review log or
evidence artifact, creates any file, approves an unreviewed revision, or chains
into another workflow.

Formal verdicts are exactly `APPROVED`, `NEEDS REVISION`, and
`MAJOR REVISION NEEDED`. `PARTIAL REVIEW`,
`BLOCKED — PRODUCT DECISION REQUIRED`, and
`ADVISORY REVIEW — NOT APPROVAL` are non-approval gate states. `ERROR` is an
invocation or execution failure and is neither a gate state nor a verdict.

---

## Required test instrumentation

Behavioral cases must run in an isolated disposable repository fixture. The
harness must record, without relying on model claims:

1. a recursive project path/type/revision snapshot before invocation;
2. the same snapshot after invocation;
3. every filesystem mutation attempt made by the skill runtime;
4. every file read, including byte counts and read order;
5. every delegated role, start time, completion status, and returned finding
   count; and
6. the exact report bytes returned in conversation.

The mutation guard passes only when before/after snapshots are identical and the
mutation-attempt ledger is empty. A prose Boundary statement alone is not test
evidence. If the harness cannot capture any required observation, that assertion
is `UNTESTED`, not PASS. Do not update `catalog.yaml` result fields from static
inspection or an uninstrumented manual run.

---

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] Description and `agents/openai.yaml` say read-only and one system GDD
- [ ] Contract version is exactly `cgs.design-review/v2`
- [ ] Entire workflow, not one phase, is explicitly zero-write
- [ ] No write-authorization, inline-revision, index-update, review-log, artifact,
  skip-re-review approval, director verdict, or chained-workflow branch exists
- [ ] Default depth is `lean`; `full` has a deterministic high-risk admission test
- [ ] Supported target grammar, normalized path, exclusions, and paired
  re-review arguments are explicit
- [ ] Every applicable root-to-target `AGENTS.md` is read in full and listed
- [ ] Supporting context has both a file-count and exact-byte budget
- [ ] Eight sections have content-level assertions, canonical order, and bounded
  `Not applicable` semantics
- [ ] Finding Schema includes stable ID, evidence, severity, destination,
  decision kind, acceptance, first/current revision, status, resolution, regression
  state, and consecutive-open count
- [ ] Gate precedence is ordered and defines unresolved waived blockers
- [ ] Full review selects no more than three specialists and no senior synthesizer
- [ ] Specialist timeout, failure, overflow, late-result, and partial behavior is
  explicit
- [ ] Lean, full, and solo outputs have distinct coverage/verdict rules
- [ ] Evidence schema, canonicalization, target/report/record revisions, reviewer,
  timestamp, depth, independence, and producer version are explicit
- [ ] Cross-GDD and whole-set design-theory ownership is explicitly out of scope

---

## Case 1: Strict invocation and profile routing

Run each input independently:

| Input | Expected |
|---|---|
| `$design-review` | missing target ERROR |
| `$design-review a.md b.md` | multiple target ERROR |
| `$design-review design/gdd/nonexistent.md` | file-not-found ERROR |
| `$design-review design/gdd/` | directory ERROR |
| `$design-review README.md` | unsupported directory ERROR |
| `$design-review design/gdd/data.json` | non-Markdown ERROR |
| `$design-review ../outside.md` | outside-project ERROR |
| `$design-review design/gdd/link.md` where link is a symlink | symlink ERROR |
| `$design-review design/gdd/*.md` | glob ERROR |
| `$design-review https://example.invalid/gdd.md` | URL ERROR |
| `$design-review design/gdd/Game System.md` | non-kebab-case target ERROR |
| `$design-review design/gdd/game-concept.md` | unsupported profile ERROR |
| `$design-review design/gdd/systems-index.md` | excluded index ERROR |
| `$design-review design/gdd/reviews/combat-review.md` | review report ERROR |
| `$design-review design/narrative/story.md` | narrative profile ERROR |
| `$design-review design/levels/level-01.md` | level profile ERROR |
| `$design-review design/live-ops/season-01.md` | live-ops profile ERROR |
| `$design-review design/gdd/combat.md --depth exhaustive` | invalid depth ERROR |
| `$design-review design/gdd/combat.md --depth` | missing option value ERROR |
| `$design-review design/gdd/combat.md --depth lean --depth solo` | duplicate option ERROR |
| `$design-review design/gdd/combat.md --unknown x` | unknown option ERROR |
| `$design-review design/gdd/combat.md --prior-review old.md` | unpaired re-review option ERROR |
| `$design-review design/gdd/combat.md --revision-evidence diff.md` | unpaired re-review option ERROR |

For every row:

- [ ] Output names the rejected input and exact reason
- [ ] No target content rubric is applied
- [ ] No completeness score, gate state, formal verdict, or evidence record exists
- [ ] Mutation guard passes

For a valid mixed-separator input that canonicalizes to the target:

- [ ] Reported target is repository-relative and uses forward slashes
- [ ] Exactly one positional target and each option value are consumed once

---

## Case 2: Root-to-target instructions and substantive sections

Fixture includes distinct rules in root `AGENTS.md`, `design/AGENTS.md`, and
`design/gdd/AGENTS.md`, including one nearest-file override. The target has all
eight headings but these defects:

- headings are out of canonical order;
- `Overview` is placeholder-only;
- `Formulas` omits units, ranges, rounding/clamp behavior, and an example;
- `Edge Cases` says only “handle gracefully”;
- `Dependencies` uses display-name-only fuzzy references;
- `Tuning Knobs` omits safe ranges and gameplay effects; and
- `Acceptance Criteria` says only “works correctly” and “feels good”.

Assertions:

- [ ] All three instruction files are read in full, in root-to-target order
- [ ] Nearest applicable instruction wins and loaded paths appear in that order
- [ ] Heading presence alone does not pass a section
- [ ] Out-of-order heading is a blocker with exact evidence
- [ ] Each listed content defect fails its corresponding substantive assertion
- [ ] Completeness score equals substantive PASS count, not eight headings
- [ ] Three or more substantively missing sections cause
  `MAJOR REVISION NEEDED`, not merely `NEEDS REVISION`

Run bounded `Not applicable` variants:

- [ ] Specific, non-contradictory rationale passes only for `Formulas`,
  `Dependencies`, or `Tuning Knobs`
- [ ] Bare `N/A`, unsupported rationale, or N/A in any other required section
  fails substantive content
- [ ] Mutation guard passes for all variants

---

## Case 3: Mechanical severity and gate precedence

Run these independent variants:

| Condition | Expected gate/verdict behavior |
|---|---|
| Invalid input | ERROR; no gate, verdict, evidence |
| Solo with otherwise approvable content | ADVISORY REVIEW — NOT APPROVAL; no Verdict heading |
| Required context omitted by budget | PARTIAL REVIEW; no formal verdict |
| Full specialist times out | PARTIAL REVIEW; no formal verdict |
| Same blocker reaches two consecutive re-reviews | BLOCKED — PRODUCT DECISION REQUIRED; no formal verdict |
| Zero unresolved blockers, advisories remain | APPROVED |
| One local, explicit, non-product blocker | NEEDS REVISION |
| Player fantasy conflicts with rule model | MAJOR REVISION NEEDED |
| Any open `product-decision` blocker | MAJOR REVISION NEEDED |
| At least three substantive sections missing | MAJOR REVISION NEEDED |
| Blocker is WAIVED/accepted risk | remains unresolved; never APPROVED |

Assertions:

- [ ] First matching precedence rule wins when multiple conditions coexist
- [ ] PARTIAL takes precedence over an otherwise approvable finding set
- [ ] Advisory and note findings never prevent APPROVED
- [ ] BACKLOG and REVIEW_ONLY findings are never blockers
- [ ] No specialist, director, or user risk acceptance overrides the mapping
- [ ] Only the three formal verdict values render `### Verdict`

---

## Case 4: Automated mutation guard and canonical evidence

Fixture is one complete, internally consistent GDD with zero blockers, a systems
index, dependency documents, and an existing reviews directory. Invoke default
lean review.

Assertions:

- [ ] Profile, normalized target, exact target revision, system/artifact ID,
  contract version, review run UUID, UTC timestamp, depth, and independence exist
- [ ] Context Manifest reports paths, exact byte totals, fixed budgets, and no
  unexplained omissions
- [ ] Target is versioned from raw bytes before analysis and immediately before output
- [ ] Before/after recursive project snapshots are byte-identical
- [ ] Mutation-attempt ledger is empty
- [ ] No source, index, review, evidence, session-state, or other file is created,
  edited, renamed, or deleted
- [ ] Gate and formal verdict are APPROVED
- [ ] Output contains one fence labeled `gate-evidence` with schema
  `cgs.review-evidence/v1`
- [ ] Evidence includes exact artifact path/revision, reviewer, run ID, depth,
  independence, timestamp, all finding IDs, unresolved blocker IDs, canonical
  report payload revision, and producer `design-review@cgs.design-review/v2`
- [ ] revalidating declared canonical report-payload revision matches
- [ ] Stable record ID matches the business scope and review run ID
- [ ] Changing one report byte invalidates `report_payload_revision` or record ID
- [ ] Changing one target byte makes the evidence stale
- [ ] A consumer cannot treat stale or malformed evidence as approval

Mutation guard and canonical revision assertions are mandatory runtime assertions,
not static string checks.

---

## Case 5: Finding normalization, destinations, and decision ownership

Fixture contains:

- one ambiguous player-visible stacking rule;
- duplicate descriptions of the same defect reported by two sources;
- a replication/data-layout concern;
- a missing QA test matrix;
- a polish idea;
- review rationale; and
- one product choice with two plausible outcomes not decided by the GDD.

Assertions:

- [ ] Every finding contains the complete v2 Finding Schema
- [ ] Same category/root cause/evidence/destination/acceptance is deduplicated to
  one stable ID while preserving all sources
- [ ] Different root causes are never merged merely to reduce count
- [ ] Ambiguous player-visible rule routes to GDD
- [ ] Architecture/data/synchronization implementation routes to ADR/TECH
- [ ] Test matrix/data/observability/automation routes to QA
- [ ] Non-blocking polish routes to BACKLOG
- [ ] Review rationale routes to REVIEW_ONLY
- [ ] API/class/schema/test-step/review material is never routed into GDD
- [ ] Technical and QA roles use GDD only for evidenced missing/contradictory
  authoritative player-visible content
- [ ] Product choice is `decision_kind: product-decision`, is a blocker, and its
  required change states the decision question/constraints without selecting or
  drafting an answer
- [ ] Editorial and uniquely derived changes are distinguished from product choice
- [ ] Stable IDs follow canonical section, evidence-line, normalized-problem order

---

## Case 6: Stable re-review evidence and finite convergence

First review produces two blockers and one advisory. Persist the exact report
externally as a fixture; the skill itself must not write it. In a fresh authoring
task, create immutable revision evidence binding prior/current target revisions,
changed ranges or patch, and authoring identity.

Validation variants:

- [ ] Supplying only prior review or only revision evidence returns ERROR
- [ ] Summary-only legacy review returns ERROR
- [ ] Prior report with duplicate/missing IDs or invalid record revision returns ERROR
- [ ] Revision evidence with wrong pre-read, post-revision, target, or missing change
  scope/author identity returns ERROR
- [ ] Both evidence files over 256 KiB are rejected

Valid first re-review assertions:

- [ ] Every prior finding is carried forward with exactly the same ID
- [ ] Fixed blocker becomes RESOLVED only with non-null current-revision resolution
  evidence satisfying its recorded acceptance condition
- [ ] Unfixed blocker remains OPEN and increments consecutive count from 0 to 1
- [ ] Unrelated prior advisory remains represented without open-ended re-review
- [ ] Review scope is prior unresolved blockers plus evidenced changed ranges and
  their directly affected interfaces
- [ ] Same defect regression reopens the existing ID; materially new regression
  continues after the highest ID in its category
- [ ] Newly noticed preference is advisory, not a blocker
- [ ] Gate is NEEDS REVISION and the skill stops after one pass

Convergence variants:

- [ ] Zero unresolved blockers with no regression yields APPROVED and stops
- [ ] Resolution resets consecutive-open count to zero
- [ ] Same blocker still open in the second consecutive re-review reaches count 2
  and yields BLOCKED — PRODUCT DECISION REQUIRED
- [ ] No variant starts revision or another review automatically
- [ ] Mutation guard passes throughout

---

## Case 7: Bounded context and coverage failure

Fixture target declares ten first-level dependencies, two direct pillar/lore
links, one implied-but-unlinked related GDD, and one dependency-of-a-dependency.
Construct file sizes so the eighth selected support file fits and the ninth would
exceed 256 KiB total.

Assertions:

- [ ] Target and all applicable AGENTS files are read fully and excluded from the
  supporting budget
- [ ] Systems index is selected first, then explicit dependency and direct-link
  files in target declaration order
- [ ] No implied related GDD or second-level dependency is read
- [ ] No more than eight support files or 256 KiB are read
- [ ] Selected files are read fully; no file is truncated
- [ ] Manifest names every loaded/omitted file and exact reason/byte total
- [ ] Lean/full returns PARTIAL REVIEW and cannot APPROVE
- [ ] Solo remains advisory and clearly reports incomplete coverage
- [ ] An unreadable explicitly required context file follows the same fail-closed
  coverage path

---

## Case 8: Stable dependency identity and exact classifications

Fixture systems index contains stable IDs, display-name collisions, exact Design
Doc paths, planned rows, and one row pointing at a missing file. Target declares
dependencies using a mix of exact IDs and exact direct links.

Assertions:

- [ ] Display-name or approximate filename is never used to resolve identity
- [ ] Exact unique ID/path with current file classifies `exists`
- [ ] Exact Not Started/In Design row with no authored doc classifies
  `planned-not-authored` and is advisory by itself
- [ ] Unresolvable non-linked identity classifies `unknown` and is a blocker
- [ ] Missing/outside explicit link, missing claimed Design Doc, or ID/link
  disagreement classifies `broken-link` and is a blocker
- [ ] Every dependency receives exactly one classification
- [ ] Existing dependency missing exact reverse target identity is a blocker
- [ ] Planned dependency becomes a distinct blocker only when target falsely
  claims an already-authoritative unavailable interface
- [ ] Report emits the unique target System ID or deterministic `gdd:<slug>`
  fallback without writing the index

---

## Case 9: Full-depth risk, fan-out, and failure semantics

Low-risk variant:

- [ ] `--depth full` on a GDD with no score-3 domain and fewer than two score-2
  domains returns `ERROR — FULL DEPTH NOT JUSTIFIED`
- [ ] No specialist starts and no gate/verdict/evidence is emitted
- [ ] Default invocation of the same GDD runs lean

High-risk variant contains six eligible domain candidates with score ties:

- [ ] Candidates are scored only from explicit target content
- [ ] Roles are deduplicated, score-1 roles discarded, sorted by score then fixed
  tie order, and capped at three
- [ ] Actual starts do not exceed available runtime slots excluding current task
- [ ] All selected roles start in one parallel batch
- [ ] No creative director or senior synthesizer starts
- [ ] Primary reviewer performs deterministic normalization/synthesis
- [ ] Each specialist receives bounded relevant context and the common schema
- [ ] Each completed specialist returns no more than five unique findings
- [ ] More than five materially distinct findings yields FINDING_OVERFLOW instead
  of silent truncation
- [ ] Technical/QA destination restrictions are enforced

Failure variants independently produce `blocked`, `timed-out`, `failed`,
`unavailable`, `finding-overflow`, and `late-discarded`:

- [ ] Blocked status is surfaced immediately while already running peers are
  collected to deadline
- [ ] Wait uses no more than three intervals of at most 60 seconds each unless the
  platform deadline is shorter
- [ ] Late work is interrupted/discarded and never silently merged
- [ ] Completed results are preserved and missing coverage is named
- [ ] Any non-completed selected specialist yields PARTIAL REVIEW and no Verdict
- [ ] Same-agent fallback is disclosed but does not satisfy independent full
  coverage
- [ ] Primary-review failure yields ERROR, not a fabricated partial report

---

## Case 10: Mode-correct output templates

Run otherwise identical approvable fixtures:

### Lean

- [ ] Coverage says `primary-reviewer: completed`
- [ ] Coverage says `specialists: not requested (lean)`
- [ ] No specialist or senior verdict placeholder appears
- [ ] Gate and `### Verdict: APPROVED` appear

### Full

- [ ] Every selected specialist and execution status appears
- [ ] All-completed coverage may produce formal APPROVED
- [ ] Any incomplete role produces PARTIAL and omits `### Verdict`

### Solo

- [ ] Coverage says primary advisory analysis and specialists not requested
- [ ] Gate is ADVISORY REVIEW — NOT APPROVAL
- [ ] `### Verdict` heading is absent
- [ ] Evidence record says `review_depth: solo` and
  `independence: advisory-only`, never formal approval

### Blocked/partial

- [ ] Both states omit `### Verdict`
- [ ] Evidence records preserve the exact non-approval state

All non-error reports include Context Manifest, Review Coverage, substantive
Completeness, Internal Consistency, Implementability and Declared Interfaces,
Findings, Convergence, Gate, Review Evidence, and Boundary.

---

## Case 11: Scope ownership and systems-index boundary

Fixture includes an undeclared conflict in another GDD, a whole-game dominant
strategy, one declared interface conflict, and a systems-index row currently
`In Review`.

Assertions:

- [ ] Only the declared interface conflict is reviewed
- [ ] Unlinked cross-GDD conflict and whole-game theory are not searched or
  reported as design-review blockers
- [ ] The skill neither invokes nor automatically recommends consistency-check or
  review-all-gdds
- [ ] Systems-index status remains exactly `In Review`
- [ ] No illegal `NEEDS REVISION` index status is proposed or written
- [ ] Report identifies target row/system ID when unique
- [ ] Missing/non-unique mapping is reported without guessing or index mutation
- [ ] Review report contains no scope estimate owned by producer/estimate
- [ ] Mutation guard passes

---

## Case 12: Independence, currentness, and closing boundary

Test independently:

1. review in the task that authored or revised the target;
2. second review in a task that already completed one review;
3. old APPROVED report after changing one target byte;
4. request to waive one blocker and mark Approved; and
5. valid NEEDS REVISION review.

Assertions:

- [ ] Variants 1 and 2 return `ERROR — INDEPENDENT REVIEW REQUIRED` without gate,
  verdict, or evidence record
- [ ] Variant 3 is stale after target path and declared-revision re-read
- [ ] Variant 4 remains `Accepted Risk / Not Approved`; waived blocker prevents
  APPROVED
- [ ] Formal approval is possible only for current bytes in an independent task
- [ ] Reviewer identity is stable and never fabricates an unavailable person/task
- [ ] Complete report precedes the single bounded next-step sentence
- [ ] Only follow-up is separate authoring/revision followed by a fresh re-review
  with both evidence arguments
- [ ] No inline revision, write authorization, tracking write, index/log update,
  skip-review approval, next system, or chained review workflow is offered
- [ ] Skill stops after one report

---

## Authoritative P1 closure matrix

| Audit ID | Static clause | Behavioral evidence |
|---|---|---|
| DR-006 | Mechanical severity and gate precedence | Case 3 assertions |
| DR-007 | Stable prior-finding identity and state | Case 6 assertions |
| DR-008 | Current target/report revision binding | Cases 6 and 12 assertions |
| DR-009 | Lean default and risk-gated full mode | Cases 1 and 9 assertions |
| DR-010 | Typed destinations and technical-content isolation | Cases 5 and 9 assertions |
| DR-011 | Substantive eight-section validation | Case 2 assertions |
| DR-012 | Strict invocation, path, and profile errors | Case 1 assertions |
| DR-013 | Root-to-target instruction precedence | Case 2 assertions |
| DR-014 | Bounded explicit context and coverage failure | Case 7 assertions |
| DR-015 | Deterministic capped specialist fan-out | Case 9 assertions |
| DR-016 | Deadline, failure, and PARTIAL semantics | Case 9 assertions |
| DR-017 | Mode-correct lean/full/solo templates | Case 10 assertions |
| DR-018 | Stable dependency classification | Case 8 assertions |
| DR-019 | Read-only systems-index boundary | Case 11 assertions |
| DR-020 | Product-decision ownership | Case 5 assertions |
| DR-021 | Single-GDD scope and external-owner routing | Case 11 assertions |
| DR-022 | Current spec/revision evidence and honest catalog state | Protocol compliance and catalog rule |

## Protocol compliance

- [ ] Entire workflow performs zero file writes and zero mutation attempts
- [ ] Unsupported or malformed input returns ERROR without gate/verdict/evidence
- [ ] Exactly one normalized system GDD and its exact declared revision are reviewed
- [ ] Root-to-target instructions are complete and ordered
- [ ] Completeness is substantive rather than heading-count-only
- [ ] Every finding has stable identity, evidence, destination, decision ownership,
  acceptance, status, resolution, and revision/currentness fields
- [ ] Gate precedence is deterministic and accepted risk never equals approval
- [ ] Re-review validates stable blockers and revision-scoped regressions only
- [ ] `unresolved_blockers == 0` is the approval convergence condition
- [ ] Same-task review/edit/review loops and author self-approval are impossible
- [ ] Context, fan-out, finding count, waits, and partial coverage are bounded
- [ ] Lean/solo never fabricate specialists or a senior verdict
- [ ] Cross-GDD/global theory and systems-index writes remain out of scope
- [ ] Report and evidence records are canonically revision-bound and independently
  attributable
- [ ] SKILL, metadata, and this spec share one contract

## Coverage notes and catalog rule

Cross-GDD consistency, whole-set design theory, non-system document profiles,
approval persistence, systems-index mutation, and lifecycle recording are owned by
other workflows and intentionally not executed here. This spec validates the
reviewer's emitted evidence envelope, not a separate recorder.

Do not fill `catalog.yaml` `last_static`, `last_spec`, or `last_category` fields
until the corresponding instrumented test actually runs. Record FAIL or UNTESTED
honestly when the runtime cannot observe mutation attempts, file reads,
delegations, timeouts, canonical revisions, or report bytes.
