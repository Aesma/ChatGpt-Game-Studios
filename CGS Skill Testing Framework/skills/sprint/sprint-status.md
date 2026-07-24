# Skill Test Spec: $sprint-status

## Candidate status

`NOT EXECUTED` — this P1 candidate specification defines structural and
behavioral expectations only. It does not claim a static/spec/category pass,
fixture run, gate invocation, source mutation, or catalog `last_*` result.

## Skill summary

`$sprint-status` is a bounded read-only check for one stable sprint. It validates
plan/tracker/story identities and hashes, distinguishes UNKNOWN from explicit
NOT_STARTED, obtains staleness and weighting values from one project-owned
configuration, computes a priority-/estimate-/dependency-aware rough signal, and
returns one health enum independently from data quality. It never scans source
slugs for progress, writes files, requests authorization, or invokes gates.

Authoritative fields include:

```text
run_status
data_status
health_status
story_status
stale_status
schedule_signal
```

## Contract sources

- `.agents/skills/sprint-status/SKILL.md`
- `.agents/skills/sprint-status/references/sprint-status-rules-v1.md`
- `.agents/skills/sprint-status/references/continued-workflow.md`
- `.agents/skills/sprint-status/agents/openai.yaml`

Every candidate-local link must resolve inside the package. No shared catalog,
workflow, gate, or runtime artifact is part of this candidate changeset.

## Authoritative P1 traceability

| Audit ID | Required closure | Structural/behavioral coverage |
|---|---|---|
| `SS-003` | No lifecycle marker is UNKNOWN, not NOT_STARTED/backlog | Static 7; Cases 4, 15 |
| `SS-004` | One health enum; data conflict, critical blockage, and schedule lag remain separate | Static 3–4; Cases 5, 12, 13 |
| `SS-005` | Stale threshold comes from one project configuration and is displayed | Static 8–9; Cases 6, 7 |
| `SS-006` | Missing dates produce exact UNKNOWN health with missing fields | Static 10; Case 8 |
| `SS-007` | Source/asset filename or slug discovery cannot imply progress | Static 11; Case 9 |
| `SS-008` | Rough health signal accounts for Must Have priority, estimates, and blocking DAG | Static 12–14; Cases 10–14 |

Exactly these six IDs are authoritative P1 scope. P0 preservation and adjacent
bounded/provenance checks are regression support, not additional P1 findings.

---

## Static assertions

1. [ ] Frontmatter contains only `name` and non-empty `description`; name matches
   `sprint-status`.
2. [ ] The package links and fully defines private rules and continued workflow.
3. [ ] `health_status` has exactly `ON_TRACK|AT_RISK|BLOCKED|UNKNOWN`; `Behind`
   and `SPRINT COMPLETE` are forbidden health verdicts.
4. [ ] `data_status`, story BLOCKED, critical-path health BLOCKED, and schedule
   LAGGING are distinct named fields/derivations.
5. [ ] Explicit → tracker active ID → session active ID/reference → user prompt
   resolution is defined; mtime/filename/latest inference is forbidden.
6. [ ] Applicable tracker requires selected IDs, plan revision, raw story-set
   hash, update time, complete story coverage, and matching projections; conflict
   stops before counts and health.
7. [ ] Tracker-absent no-marker story is UNKNOWN, missing file is MISSING, and
   neither enters NOT_STARTED/backlog/work denominators or non-UNKNOWN health.
8. [ ] `production/config/sprint-status.yaml` and schema
   `cgs.sprint-status-config/v1` are the only stale/weight/health threshold source.
9. [ ] The output displays config revision/hash, stale value/day basis/timezone/
   calendar, priority weights, schedule threshold, Must-Have time trigger, and
   estimate unit.
10. [ ] Missing/invalid dates make `health_status: UNKNOWN` with exact field IDs;
    no combined list of possible verdicts is emitted.
11. [ ] `src/`, assets, build output, history, and filename slugs are explicitly
    excluded even as hints and cannot affect any metric or verdict.
12. [ ] Weighted completion uses estimate × configured priority weight and
    reports operands, basis points, coverage, unit, config identity, and limits.
13. [ ] Dependency input is a validated DAG; deterministic remaining critical
    path, tie-node set, blocker/stale nodes, and downstream blocked estimate are
    computed from stable IDs.
14. [ ] Health first-match rules separate unknown prerequisites, critical-path
    blockers, off-path risks, staleness, schedule lag, and Must-Have exposure, and
    explicitly label the result a rough signal rather than forecast.
15. [ ] IN_REVIEW is unfinished and recovery checkpoints are validated evidence,
    never status/completion authority.
16. [ ] The workflow is read-only throughout, rehashes sources before return,
    invokes no gate/workflow, requests no authorization, and creates no attachment.
17. [ ] Source/story/edge/checkpoint/output bounds are fixed; pagination never
    changes full-set metrics.
18. [ ] Metadata describes read-only, revision-checked, explicit unknown/data-
    conflict behavior and does not conflate DATA_CONFLICT with health.

---

## Case 1: Fully verified sprint produces ON_TRACK

**Fixture:**

- Tracker and session both select `sprint-004`.
- Plan/tracker IDs, plan revision, story-set hash, update times, story projections,
  and checkpoint/review evidence verify.
- Plan dates/timezone, estimates, priorities, and acyclic dependencies are valid.
- Project configuration validates and all required story statuses/freshness are
  known; no blocker, stale critical node, configured lag, or late Must-Have risk
  rule matches.

**Expected:** `run_status: COMPLETE`, `data_status: VERIFIED`,
`health_status: ON_TRACK`, exact `SS-HEALTH-05` input tuple, source/config hashes,
and no project mutation.

---

## Case 2: Active stable ID beats newer mtime

**Fixture:** tracker is absent, session explicitly selects `sprint-004`, and
`sprint-099.md` is newer by mtime and sorts later by filename.

**Expected:** only `sprint-004` resolves; selection source/path/hash are shown;
mtime and filename order are not inspected as authority.

---

## Case 3: Applicable tracker mismatch is DATA_CONFLICT

Run variants for wrong sprint/active ID, plan revision, story-set hash, stale
tracker timestamp, missing/extra story, status disagreement, malformed field, and
source changing during the run.

**Expected:** exact `DATA CONFLICT — sprint health not assessed.`,
`data_status: DATA_CONFLICT`, `health_status: UNKNOWN`, expected/observed source
values, one recovery action, and no counts, completion, critical path, or derived
health.

---

## Case 4: No marker is UNKNOWN, never backlog

**Fixture:** no applicable tracker; one valid referenced story has no controlled
lifecycle marker, another explicitly says Not Started, and a third is Done.

**Expected:** statuses are UNKNOWN, NOT_STARTED, and DONE respectively. Known-
status coverage is `2/3`; explicit backlog count is one; UNKNOWN is separately
listed, excluded from all work denominators, and forces
`health_status: UNKNOWN`.

---

## Case 5: Health vocabulary is single and layered

Run snapshots representing clean progress, schedule lag, off-critical blocker,
critical-path blocker, missing prerequisite, and tracker conflict.

**Expected:** health is respectively ON_TRACK, AT_RISK, AT_RISK, BLOCKED,
UNKNOWN, and UNKNOWN. Schedule uses LAGGING; tracker conflict uses
`data_status: DATA_CONFLICT`. No `Behind`, combined possible-verdict string, or
SPRINT COMPLETE health value appears.

---

## Case 6: Staleness follows the exact project configuration

**Variants:**

- A: config says `stale_after_days: 2`, CALENDAR_DAYS; elapsed status age is 3.
- B: config says `stale_after_days: 4`, CALENDAR_DAYS; same age is 3.
- C: WORKING_DAYS calendar makes the elapsed value 2 while calendar elapsed is 4.

**Expected:** A is STALE; B and C are FRESH. Each row displays config
revision/hash, threshold, basis, timezone/calendar, timestamps, elapsed operand,
and strict-greater comparison. File mtime never participates.

---

## Case 7: Missing or invalid stale configuration has no hidden default

**Variants:** absent file; wrong schema; zero/negative threshold; invalid timezone;
WORKING_DAYS without a complete verified calendar; estimate-unit mismatch.

**Expected:** stable config-field findings, affected staleness/weighted values
UNKNOWN, `data_status: PARTIAL`, and `health_status: UNKNOWN`. Neither a two-day
nor four-day fallback appears.

---

## Case 8: Missing dates emit only UNKNOWN health

**Variants:** absent start date, absent end date, invalid/zero duration, missing
timezone, or incomplete working calendar.

**Expected:** available source/status coverage may still be shown, but date/time
operands and schedule signal are UNKNOWN; `health_status: UNKNOWN` names exact
missing field IDs and `SS-HEALTH-02`. It never prints a list such as “ON TRACK /
AT RISK / BLOCKED: unknown.”

---

## Case 9: Implementation-looking slug cannot change progress

**Fixture:** an UNKNOWN story ID/title has matching names in `src/`, assets, build
output, and git history; rerun with those files removed.

**Expected:** both outputs have identical story status, coverage, estimates,
critical path, schedule signal, health, and hashes for the allowed read set. No
slug search or Evidence Hint appears and none of those directories is read.

---

## Case 10: Estimate weighting differs from task count

**Fixture:** three stories share one estimate unit: two 1-unit DONE stories and
one 8-unit IN_PROGRESS story, with equal priority weights and complete known
inputs.

**Expected:** task-count completion may be displayed only as descriptive `2/3`;
weighted completion is `floor(10000*2/10)=2000` bps and drives schedule signal.
The skill does not substitute `6666` task-count bps for weighted progress.

---

## Case 11: Must Have priority changes weighted exposure

**Fixture:** configuration weights MUST_HAVE 3 and SHOULD_HAVE 1; an 8-unit
MUST_HAVE is IN_PROGRESS and an 8-unit SHOULD_HAVE is DONE.

**Expected:** weighted planned is `24+8=32`, weighted DONE is `8`, completion is
2500 bps, incomplete Must-Have estimate is 8 units, and config/unit operands are
shown. Reversing statuses produces the corresponding deterministic result.

---

## Case 12: Critical-path blocker yields BLOCKED health

**Fixture:** valid DAG `A -> B -> C` and independent `D`; remaining path A-B-C is
the maximum estimate path, B is verified BLOCKED, all prerequisites are known.

**Expected:** B is in the complete critical-node set;
`health_status: BLOCKED`, rule `SS-HEALTH-03`, critical path/tie rule and
dependency-blocked downstream estimate are shown. `data_status` remains VERIFIED
or PARTIAL according to source coverage, never DATA_CONFLICT merely due to B.

---

## Case 13: Off-critical blocker and critical stale story are AT_RISK

**Variants:** verified blocker exists only off the maximum path; or no blocker
exists but a configured-stale IN_PROGRESS story is on the critical path.

**Expected:** both yield `health_status: AT_RISK`, rule `SS-HEALTH-04`, with
stable story IDs and distinct reason fields. Neither is relabeled BLOCKED merely
for generic lateness.

---

## Case 14: Invalid estimates, priority, or DAG fail health closed

**Variants:** missing/negative/mixed-unit estimate, unknown priority, missing edge
endpoint, self-edge, duplicate edge, dependency cycle, or zero weighted
denominator.

**Expected:** exact affected operands are UNKNOWN with stable findings and
`health_status: UNKNOWN`; available independent counts remain clearly partial.
The workflow does not assign defaults, delete edges, or use task count instead.

---

## Case 15: UNKNOWN, MISSING, and explicit NOT_STARTED remain distinct

**Fixture:** one no-marker existing story, one absent referenced story, and one
explicit backlog story, all Must Have with estimates.

**Expected:** statuses UNKNOWN, MISSING, NOT_STARTED; backlog count one; missing/
unknown counts one each; weighted and incomplete-Must-Have denominators are not
claimed complete; health UNKNOWN. No unavailable story becomes zero work.

---

## Case 16: Historical sprint excludes another active tracker

**Fixture:** explicit `sprint-003`; well-formed tracker/session select
`sprint-004`; sprint-003 plan/story fallback is valid.

**Expected:** tracker is `NOT_APPLICABLE — different active sprint`, never used
for sprint-003 statuses. Fallback provenance and PARTIAL data status are shown.
An omitted/current selector with conflicting active declarations instead yields
DATA_CONFLICT.

---

## Case 17: IN_REVIEW is unfinished

**Fixture:** story/tracker normalize to IN_REVIEW and plan/post-write/test/log
hashes verify with exit code zero and no unresolved checkpoint.

**Expected:** IN_REVIEW is distinct, contributes zero DONE estimate, and prevents
an all-work-done claim. Missing/malformed/failing review evidence is
DATA_CONFLICT, not automatic IN_PROGRESS or DONE.

---

## Case 18: Recovery checkpoint is evidence, not authority

**Variants:** valid unresolved PARTIAL checkpoint with both projections
IN_PROGRESS; hash/identity mismatch; unresolved checkpoint while IN_REVIEW;
claimed restored failure whose baseline hashes do not match current bytes.

**Expected:** only the first returns RECOVERY_CHECKPOINT while remaining
IN_PROGRESS. Every contradiction is DATA_CONFLICT with no health derivation.
Nothing is marked complete from a checkpoint.

---

## Case 19: Source changes before return invalidate derived state

**Fixture:** a selector, plan, tracker, story, checkpoint, configuration, or
calendar hash changes after analysis but before final response.

**Expected:** discard derived counts and health; return DATA_CONFLICT with exact
expected/observed raw hashes. Do not repair, revert, or report the stale snapshot
as current.

---

## Case 20: Read-only and gate-independent in every review mode

**Fixture:** full, lean, and solo review-mode files exist in separate variants.

**Expected:** those files are not read; no gate/subagent/workflow is invoked; no
authorization prompt, write, attachment, tracker update, or scope proposal occurs.
Before/after source hashes and the empty write set are reported.

---

## Case 21: Large sprint output is bounded without metric truncation

**Fixture:** 100 fully validated stories and 35 attention findings, within input
bounds.

**Expected:** all 100 stories contribute to metrics; primary summary stays at or
below 50 lines; first 20 deterministically sorted attention rows show `20/35` and
cursor; no attachment is created. A continuation page changes display only.

---

## Case 22: Invalid invocation is a zero-evidence-read error

**Variants:** two selectors, traversal, separator, wildcard, or malformed ID.

**Expected:** `run_status: ERROR`, documented usage, no sprint evidence, no gate,
no authorization, and no write.

---

## Protocol compliance

- [ ] Stable selection precedes plan/story reading.
- [ ] Plan/story-set identity precedes tracker authority.
- [ ] Tracker conflict stops before counts/health.
- [ ] Explicit UNKNOWN classification precedes weighted calculations.
- [ ] Project configuration precedes staleness and health.
- [ ] Estimate/priority/DAG signals precede one first-match health result.
- [ ] Full-source rehash precedes final return.
- [ ] Final output reports one recommendation at most and stops.

## Verification boundary

Static inspection can verify package structure, enums, formulas, config source,
phase order, source exclusions, relative links, P1 trace IDs, and fixture
definitions. It cannot claim runtime fixture execution, tracker/checkpoint truth,
calendar arithmetic in a real project, gate behavior, source immutability during
an actual run, or any delivery forecast. All such behavior remains
`NOT EXECUTED` until separately tested with immutable evidence.
