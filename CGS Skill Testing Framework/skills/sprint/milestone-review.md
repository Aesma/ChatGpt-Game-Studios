# Skill Test Spec: $milestone-review

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

## Candidate status

`NOT EXECUTED` — this P1 remediation specification defines static and behavioral
expectations only. No case result, catalog `last_*` field, runtime pass, report
write, producer review, or project-stage decision is claimed by this document.

## Skill summary

`$milestone-review` resolves one stable milestone ID, validates a bounded
revision-bound evidence manifest, computes deterministic metrics, freezes an
evidence-only draft before optional producer review, derives independent
delivery/quality/risk/evidence/decision/write states, and optionally creates one
authorized immutable report. Scope changes and risk acceptance remain user-owned
governance decisions and never rewrite objective evidence.

The authoritative states are:

```text
run_status
delivery_status
quality_status
risk_status
evidence_status
evidence_verdict
decision_status
artifact_write_status
```

## Contract sources

- `.agents/skills/milestone-review/SKILL.md`
- `.agents/skills/milestone-review/references/milestone-review-rules-v1.md`
- `.agents/skills/milestone-review/references/continued-workflow.md`
- `.agents/skills/milestone-review/agents/openai.yaml`
- `.codex/docs/director-gates.md` section `PR-MILESTONE` for full-mode producer
  dispatch only

All candidate-local relative links must resolve inside the candidate package.
The shared director-gate file is a read-only external dependency and is not part
of this candidate changeset.

## Authoritative P1 traceability

| Audit ID | Required closure | Structural/behavioral coverage |
|---|---|---|
| `MR-004` | Replace conflicting verdict terms with layered status fields | Static 2; Cases 1, 10, 11, 12 |
| `MR-005` | Define exact absent/empty/malformed/inconsistent milestone handling | Static 4; Cases 4, 5 |
| `MR-006` | Keep Protect/Cut recommendations as evidence-backed candidates; final scope change is user-owned | Static 9; Cases 13, 14 |
| `MR-007` | Define feature progress and adjusted-day formulas, sources, unknowns, and confidence | Static 7–8; Cases 7, 8 |
| `MR-008` | Define immutable report path/version/run ID/source revisions and write protocol | Static 13–16; Cases 17–20 |
| `MR-009` | Freeze evidence-only draft before same-revision producer review, then assign verdict | Static 10–12; Cases 9–12 |

Exactly these six IDs are the P1 authority for this candidate. Adjacent
hardening assertions support their safe implementation but do not change the
audit count.

---

## Static assertions

Verified by static inspection; no fixture is required.

1. [ ] YAML frontmatter contains only `name` and non-empty `description`, and
   `name` equals `milestone-review`.
2. [ ] Exact non-overlapping vocabularies exist for `run_status`,
   `delivery_status`, `quality_status`, `risk_status`, `evidence_status`,
   `evidence_verdict`, `decision_status`, and `artifact_write_status`.
3. [ ] `current` resolves only from explicit stable active-milestone fields; mtime,
   creation time, filename order, and guessed “latest” selection are forbidden.
4. [ ] Absent, zero-byte, malformed/schema-conflicting, and internally
   inconsistent milestones have exact BLOCKED subtypes and cannot enter metric,
   draft, producer, verdict, decision, or write phases.
5. [ ] The evidence manifest binds declared revisions/revisions, exact target build,
   freshness, repository revision, exact sprint ID set, tracker, bugs, tests,
   performance, risk, and pillar/player-goal evidence.
6. [ ] Fixed file/row/aggregate limits and exact source states are defined;
   missing, empty, stale, mismatched, or over-limit required evidence becomes
   partial and never silently becomes zero.
7. [ ] Every metric record requires source refs/revisions, named formula, operands,
   denominator, unit/basis, result or `UNKNOWN`, confidence, and limitation.
8. [ ] AC completion, planned/completed units, sprint count, bug/test/performance,
   compatible velocity, and ceiling adjusted working days have deterministic
   formulas and explicit unknown conditions.
9. [ ] `PROTECT|SIMPLIFY|DEFER|CUT` outputs are stable
   `CANDIDATE_NOT_DECIDED` objects with evidence, effects, pillar/player impact,
   dependencies, alternative/tradeoff, owner, and separate user-decision schema.
10. [ ] `cgs.milestone-evidence-draft/v1` explicitly excludes producer, risk,
    verdict, decision, authorization, path, and write fields and is frozen/revision-
    displayed before review.
11. [ ] Full-mode producer review receives and must echo the exact milestone,
    target, `source_snapshot_revision`, and `evidence_draft_revision`; it has no write
    or scope-decision authority.
12. [ ] Producer timeout/unavailability/malformed/revision mismatch becomes
    `risk_status: UNKNOWN` and `evidence_verdict: PARTIAL`; lean/solo use exact
    `NOT_REVIEWED` skip receipts.
13. [ ] Report schema is `cgs.milestone-review-report/v2` and path is exactly
    `production/milestones/reviews/<milestone-id>/<run-id>.md`.
14. [ ] Run ID, canonical byte format, report/source/draft/producer/decision
    revisions, fixed section order, and no-overwrite collision rule are defined.
15. [ ] Exact candidate path/revision/size/source base set/singleton write set is
    previewed and authorized before the first project write.
16. [ ] Every authority/source is compare-and-set revalidated, target absence is
    rechecked, create uses atomic no-replace semantics, and post-write records/revision
    and source stability are verified.
17. [ ] Stable finding IDs and scope-candidate IDs exclude volatile prose,
    timestamps, reviewer, severity/status, and observed revisions/values.
18. [ ] The final run envelope reports all layered fields independently and
    explicitly states that it did not run tests, captures, fixes, transitions, or
    downstream workflows.

---

## Case 1: Complete evidence with full review produces layered GO

**Fixture:**

- Both authority files declare `milestone-03` and the milestone/manifest validate.
- Every required source row is unique, in bounds, current, version/revision/build
  matched, and mapped to every required criterion/threshold.
- Delivery checks and quality checks all pass.
- Full-mode producer returns valid `ON_TRACK` for the exact frozen revisions.
- No governance decision or report authorization is supplied.

**Input:** `$milestone-review current --review full`

**Expected:**

- `run_status: COMPLETE`, `delivery_status: COMPLETE`, `quality_status: PASS`,
  `risk_status: ON_TRACK`, `evidence_status: COMPLETE`, and
  `evidence_verdict: GO`.
- `decision_status: NOT_RECORDED` and
  `artifact_write_status: NOT_REQUESTED` remain independent.
- No file is written.

---

## Case 2: Stable current selection ignores newer mtime

**Fixture:** authority files agree on `milestone-03`; `milestone-99.md` has the
newest mtime and filename order would select another file.

**Input:** `$milestone-review current`

**Expected:** only `milestone-03` resolves, with both authority revisions recorded.
No timestamp or filename fallback appears.

---

## Case 3: Ambiguous current blocks before evidence

**Variants:** missing declarations; duplicate declaration in one authority;
session/index conflict; multiple files for the same unsafe/colliding ID.

**Expected:** `run_status: BLOCKED`, `artifact_write_status: BLOCKED`, exact
authority diagnostic, no evidence load, producer, draft, verdict, decision
prompt, or write.

---

## Case 4: Missing and empty milestone never enter the template

**Variants:** resolved target is absent; resolved target is a zero-byte regular
file.

**Expected:** subtype `MILESTONE_MISSING_OR_EMPTY` and a resolution diagnostic
only. There are no metric rows, zeros, source manifest, evidence draft, producer
packet, objective verdict, governance decision, report path, or mutation.

---

## Case 5: Malformed and inconsistent milestone never enter the template

**Variants:** parse failure; wrong schema; internal ID mismatch; duplicate scope
or sprint IDs; conflicting target builds/criteria.

**Expected:** `MILESTONE_INVALID` or `MILESTONE_INCONSISTENT` as applicable,
`run_status: BLOCKED`, and the same phase exclusion as Case 4.

---

## Case 6: Evidence gaps propagate without erasing verified facts

**Fixture:** tracker and sprint sources verify; bug registry is missing, tests are
empty, one performance revision mismatches, and an unrelated threshold conclusively
fails from verified evidence.

**Expected:** ledger states `MISSING`, `EMPTY`, and `REVISION_MISMATCH`; dependent
metrics/checks are `UNKNOWN`; the verified failure remains `FAIL` and has its own
finding; `evidence_status: PARTIAL`, `quality_status: FAIL`, and first-rule
`evidence_verdict: PARTIAL`. Missing counts are not zero.

---

## Case 7: AC and planned-completed formulas are deterministic

**Fixture:** eight required AC IDs map uniquely; six are in verified controlled
terminal states. Milestone `progress_basis` is `acceptance_criteria`; a story-
point value also exists but is out of basis.

**Expected:** AC completion operands are `6/8` with display `75.00%`; planned and
completed units are `8` and `6`; the unrelated point value is not mixed. Metric
rows show exact source revisions, formula versions, basis, confidence, and limits.

**Unknown variants:** zero AC denominator, duplicate mapping, missing state map,
or missing required tracker source produces `UNKNOWN`, not `0%`.

---

## Case 8: Velocity and adjusted remaining working days are defined

**Fixture:** compatible verified completed sprints contain 18 completed units
over 9 elapsed working days; planned/completed milestone units are 25/18.

**Expected:** velocity is rational `18/9` units per working day and adjusted days
is `ceil(7/(18/9)) = 4`, labeled `ESTIMATE_BOUND` or `VERIFIED` according to the
declared inputs, never a promised date.

**Unknown variants:** mixed point/item bases, incomplete sprint, calendar-day
input, zero/negative velocity, missing planned units, or estimate basis not
declared produces `UNKNOWN` with limitation.

---

## Case 9: Evidence-only draft contains no post-review state

**Fixture:** evidence, metrics, findings, and scope candidates are available.

**Expected:** canonical draft bytes contain the allowlisted evidence fields and
no producer result, `risk_status`, `evidence_verdict`, `decision_status`,
governance record, write authorization, report path/revision, or
`artifact_write_status`. Draft records/revision/size are frozen and shown before any
review dispatch.

---

## Case 10: Producer must review the identical frozen draft

**Fixture:** full mode; producer returns `AT_RISK`, echoes exact milestone/target,
source snapshot and draft revisions, and supplies valid sourced risks with owners
and deadlines.

**Expected:** the original draft revision remains unchanged; receipt validates;
`risk_status: AT_RISK`; complete delivery/quality/evidence yields
`evidence_verdict: CONDITIONAL_GO`. Producer text cannot alter metric, scope, or
objective inputs.

---

## Case 11: Producer failure is explicit PARTIAL

**Variants:** timeout; unavailable delegation; over-limit/malformed response;
duplicate response; different milestone/build/source/draft revision; invented metric.

**Expected:** one stable reviewer gap, `risk_status: UNKNOWN`,
`evidence_verdict: PARTIAL`, original draft preserved, no silent retry, no GO.

---

## Case 12: Lean and solo have exact skip state

**Fixture:** complete evidence and passing delivery/quality; run separately in
`lean` and `solo`.

**Expected:** no producer dispatch; exact mode skip receipt;
`risk_status: NOT_REVIEWED`; objective verdict follows the documented matrix
without describing the skip as a producer opinion. All other layered fields are
reported independently.

---

## Case 13: Scope outputs remain undecided candidates

**Fixture:** evidence supports protecting a pillar-critical item and deferring a
dependency-isolated item; schedule effect for a proposed cut cannot be verified.

**Expected:** stable `PROTECT`/`DEFER`/`CUT` candidate records show evidence,
scope/criterion IDs, schedule derivation or `UNKNOWN`, pillar/player and
dependency/quality/risk impacts, alternatives/tradeoffs, owner, and
`CANDIDATE_NOT_DECIDED`. No tracker/milestone/scope changes occur and prose does
not imply commitment.

---

## Case 14: Only a valid user artifact decides scope

**Variants:** no scope-decision artifact; valid artifact bound to candidate revision;
artifact with stale candidate revision or missing user-owned rationale/owner.

**Expected:** no artifact leaves candidate undecided; valid artifact is quoted
without applying a mutation; stale/incomplete artifact becomes a gap and is not
applied. The review never invents decision maker, timestamp, rationale, accepted
impact, owner, or deadline.

---

## Case 15: Risk acceptance cannot rewrite objective evidence

**Fixture:** objective result is `NO_GO` because delivery is incomplete or the
producer is `OFF_TRACK`; the user supplies a complete risk-acceptance record.

**Expected:** `evidence_verdict: NO_GO` and its input tuple remain unchanged;
`decision_status: PROCEED_WITH_ACCEPTED_RISK` is separate. A requested bare
`PROCEED` is rejected for non-GO. Accepted stable IDs, decision maker/time,
rationale, owners, and deadlines are recorded only as governance evidence.

---

## Case 16: Stable finding IDs survive volatile changes

**Fixture:** rerun the same logical failed check with changed wording, line,
timestamp, source revision/value, classification, state, and reviewer; then run a
different check against the same scope item.

**Expected:** the first finding retains the same `MRF-<20hex>` ID and updated
evidence; the different check receives another ID. Full finding key inputs and
revisions are available for verification.

---

## Case 17: Immutable report identity and candidate preview

**Fixture:** one frozen UTC second and source snapshot; report target does not
exist; no authorization yet.

**Expected:** schema `cgs.milestone-review-report/v2`; path exactly
`production/milestones/reviews/<id>/<UTC>-<UTC-run-id>.md`; all source revisions/revisions,
draft/producer/decision/finding/candidate identities and layered derivations are
embedded; preview shows `CREATE_NEW`, exact report revision/bytes/source base set and
singleton write set. Project remains unchanged.

---

## Case 18: Existing target collision blocks without suffix

**Fixture:** the deterministic target path already exists with identical or
different bytes.

**Expected:** `artifact_write_status: BLOCKED`; existing file remains unchanged;
no overwrite, append, counter, alternate timestamp, suffix, rename, or delete.

---

## Case 19: Source changes after authorization invalidates transaction

**Fixture:** user authorizes exact candidate; an authority or source declared revision,
revision, join, or target absence changes before atomic create.

**Expected:** no report write; old candidate/path/authorization are stale. Any
future attempt requires a fresh evidence run, source/draft/report revisions, run ID,
path, preview, and authorization.

---

## Case 20: Atomic write and postverification stay independent of readiness

**Variants:** create succeeds and all postchecks pass; no-replace fails;
post-read bytes differ; source changes immediately after create.

**Expected:** only the fully verified variant yields
`artifact_write_status: COMPLETE`; failure/ambiguous variants yield honest
`BLOCKED` or `ERROR` observations without claiming success. Regardless of write
state, objective/decision fields do not change. Only the exact report path may be
created; no other project artifact is edited.

---

## Case 21: Invalid invocation is a zero-read, zero-write error

**Variants:** traversal selector, path separator, glob, duplicate selector,
unknown/repeated option, missing mode value, malformed configured review mode.

**Expected:** `run_status: ERROR`, no milestone evidence read, no reviewer, no
project write, and the documented invocation syntax.

---

## Case 22: Fixed bounds fail closed without truncated coverage

**Variants:** 65 sprint IDs; 513 source rows; one source or aggregate exceeds its
bound; producer result/report candidate exceeds its own bound.

**Expected:** the applicable `OVER_LIMIT`, blocked candidate, or explicit error
is reported. The skill never drops rows, analyzes “first N” as complete, or
claims a partially serialized report was written.

---

## Protocol compliance

- [ ] Review mode resolves once.
- [ ] Stable milestone selection precedes evidence loading.
- [ ] Invalid milestone branches precede metric-template construction.
- [ ] Exact bounded manifest precedes formulas.
- [ ] Evidence-only draft freezes before producer review.
- [ ] Producer review/skip precedes objective verdict derivation.
- [ ] Objective verdict precedes optional governance decision.
- [ ] Report candidate freezes before authorization.
- [ ] Source compare-and-set precedes atomic create.
- [ ] Final output reports the validation boundary and stops.

## Verification boundary

Static inspection can verify package structure, vocabulary, formulas, schemas,
relative links, trace IDs, path/write rules, and test definitions. It cannot
claim any fixture execution, producer dispatch, test/performance run, atomic-
filesystem behavior, user decision, report persistence, milestone transition,
or catalog result. Those remain `NOT EXECUTED` until an authorized runner records
immutable evidence separately.
