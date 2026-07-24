# Skill Test Spec: $review-all-gdds

## Skill Summary

`$review-all-gdds` performs a report-only holistic review of the current,
hash-bound and independently approved system-GDD manifest. It imports current
deterministic `$consistency-check` evidence, constructs a typed graph, processes
design-holism work in bounded deterministic shards, walks a risk-ranked scenario
sample, and emits a generic `cgs.review-evidence/v1` record with a
`cgs.cross-gdd-review/v2` extension.

The run verdict is exactly `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`. Invalid
invocation and fewer than two reviewable GDDs return `ERROR` without a run
verdict. Conversation output is the default. The only permitted mutation is one
new, explicitly authorized immutable report; the skill never mutates GDDs,
systems index, registry, session state, lifecycle, approval, sign-off, or
accepted-risk records.

`cgs.cross-gdd-rules/v1` owns shard limits, finding identity, deterministic
severity, scenario selection, and verdict precedence. Design theory remains
advisory unless separate current evidence proves the explicit-invariant rule.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name
      matches the skill directory
- [ ] Main file links and requires the complete versioned ruleset and workflow
      continuation
- [ ] Declares exactly the run verdicts PASS / CONCERNS / FAIL / PARTIAL and
      distinguishes invocation ERROR without a verdict
- [ ] Declares conversation output by default and permits at most one new,
      explicitly authorized immutable report
- [ ] Explicitly forbids mutations to GDDs, systems index, registry, session
      state, lifecycle, approval, sign-off, accepted-risk records, and existing
      reports
- [ ] Defines strict argument grammar and a four-mode phase matrix with REQUIRED,
      FORBIDDEN, and NOT_APPLICABLE semantics
- [ ] Builds canonical system identity from stable systems-index IDs and treats
      `Depends On IDs` as one authoritative directed edge
- [ ] Requires exact-hash independent design-review approval evidence for every
      MVP GDD and forces provisional/stale/unbound input to PARTIAL
- [ ] Builds project/run/source identities, complete path/hash manifest,
      ruleset ID/hash, skill-bundle hash, manifest digest, stale key, planned
      checks, and planned shards
- [ ] Uses explicit baseline evidence and baseline/current graph union for
      bidirectional transitive incremental impact closure
- [ ] Never selects incremental scope using filesystem mtime, filename recency,
      or Git name-only output
- [ ] Imports a current `cgs.consistency-report/v1` and never directly treats the
      entity registry as product truth or populates it
- [ ] Declares numeric GDD/edge/byte shard bounds and exposes any overflow as
      unchecked coverage plus PARTIAL
- [ ] Defines `cgs.cross-gdd-worker/v1`, exact hash echoes, deterministic merge,
      stable finding fingerprints, deduplication, and evidence-conflict handling
- [ ] Enumerates all scenario candidates before deterministic top-five selection
      and reports selected plus unselected candidates
- [ ] Includes a versioned rule-to-severity matrix in which missing dependency
      and undefined combined state are warnings, theory is advisory, and
      critical unknowns force PARTIAL
- [ ] Emits one embedded fenced `gate-evidence` block compatible with
      `cgs.review-evidence/v1`, with a `cgs.cross-gdd-review/v2` extension,
      complete coverage/findings, accepted-risk references, and stale key
- [ ] Persists, when authorized, only
      `design/gdd/gdd-cross-review-<UTC>-<manifest-prefix>.md`
- [ ] Defines one separate handoff and `Stop here`

---

## Director Gate Checks

No director gates. Workers produce bounded evidence for the coordinator; they
never replace the deterministic ruleset or emit the overall verdict.

---

## Test Cases

### Case 1: Clean approved, fully covered full review

**Fixture:** A valid systems index contains three MVP systems with stable IDs and
directed dependencies. Every GDD has current exact-hash independent APPROVED
design-review evidence. A current complete `cgs.consistency-report/v1` returns
PASS for the same artifact set. All GDDs fit one bounded shard, scenario
candidate generation completes, and no warning or hypothesis remains.

**Input:** `$review-all-gdds full consistency-report:design/gdd/consistency/current.md`

**Assertions:**

- [ ] Review set includes all three MVP stable IDs and no unrelated Markdown
- [ ] Approval currentness and consistency-report record ID are verified
- [ ] Every required check/shard/scenario has DONE coverage
- [ ] Consistency-evidence validation and independent theory shards may run in
      parallel but merge deterministically before scenario selection
- [ ] Verdict is PASS
- [ ] Embedded evidence contains the generic schema and v2 extension, complete
      artifacts, empty finding IDs, manifest digest, and stale key
- [ ] No file is written without exact-path authorization

### Case 2: Imported deterministic rule contradiction

**Fixture:** Current consistency evidence cites two exact-hash approved normative
rules for the same subject, unit, scope, and condition that cannot both be true,
with no exception.

**Input:** `$review-all-gdds consistency consistency-report:design/gdd/consistency/current.md`

**Assertions:**

- [ ] Producer finding ID is retained as provenance
- [ ] Finding maps to `RAG.CONSISTENCY.RULE_CONTRADICTION`
- [ ] Both current paths, hashes, sections, and conflicting rules are present
- [ ] Finding is BLOCKER / OPEN and verdict is FAIL
- [ ] Reviewer does not choose which GDD is authoritative or edit either file

### Case 3: Missing dependency target is non-blocking

**Fixture:** The systems index has an outgoing edge from system A to an unknown
system B. Coverage is otherwise complete and current.

**Assertions:**

- [ ] Finding uses `RAG.CONSISTENCY.DEPENDENCY_TARGET_MISSING`
- [ ] Severity is WARNING, not BLOCKER
- [ ] Verdict is CONCERNS
- [ ] No reverse declaration in B is requested

### Case 4: Fewer than two reviewable GDDs

**Fixture:** The canonical manifest resolves zero or one readable system GDD.

**Assertions:**

- [ ] Returns the minimum-input ERROR
- [ ] Emits no PASS / CONCERNS / FAIL / PARTIAL run verdict
- [ ] Spawns no workers and writes no report or project file

### Case 5: No director gate or hidden review mode

**Fixture:** Valid inputs plus unrelated `production/review-mode.txt` and
session-state files.

**Assertions:**

- [ ] No director gate is spawned
- [ ] Unrelated review-mode/session files are not read or modified
- [ ] Bounded workers cannot override finding severity or overall verdict

### Case 6: Unmeasured design-theory risk

**Fixture:** Six concurrent systems and a ranged/melee damage difference exist,
but there is no approved attention budget, dominance threshold, simulation,
telemetry, or playtest evidence.

**Input:** `$review-all-gdds design-theory`

**Assertions:**

- [ ] Each observation is HYPOTHESIS / ADVISORY
- [ ] Evidence, assumptions, counterexample, validation plan, and
      NEEDS_MEASUREMENT are present
- [ ] These observations cannot produce FAIL
- [ ] With complete coverage, verdict is CONCERNS
- [ ] Consistency report is neither required nor read in this mode

### Case 7: Worker, budget, or selected-scenario coverage failure

**Fixture:** One planned worker errors, returns mismatched hashes, omits a check,
or a selected scenario exceeds the byte limit.

**Assertions:**

- [ ] Available completed evidence is retained
- [ ] Exact worker, shard, check, input, and reason are unchecked coverage
- [ ] Finding uses `RAG.COVERAGE.WORKER_OR_SHARD`
- [ ] Verdict is PARTIAL even when another shard proves a blocker
- [ ] Output is never PASS or FAIL

### Case 8: Stale or ambiguous prior baseline

**Fixture:** A prior PASS exists, but its record is malformed, project-mismatched,
ruleset-mismatched, or a run ID resolves to multiple reports.

**Input:** `$review-all-gdds since-last-review baseline:<value> consistency-report:design/gdd/consistency/current.md`

**Assertions:**

- [ ] Baseline is not selected by mtime or newest filename
- [ ] Unsafe incremental scope falls back to full and states the exact reason
- [ ] Historical PASS is not gate evidence for current bytes
- [ ] Current report still binds the complete current artifact set

### Case 9: Mutation guard and optional immutable persistence

**Fixture:** A complete report is rendered. Exercise decline, exact-path
approval, and an already-existing target path.

**Assertions:**

- [ ] Decline produces zero mutations
- [ ] Approval creates only the exact new
      `design/gdd/gdd-cross-review-<UTC>-<manifest-prefix>.md`
- [ ] Saved block is read back and record/manifest/file hashes are verified
- [ ] Existing target is never overwritten and no replacement path is chosen
      without new approval
- [ ] No sidecar, source, index, registry, session, lifecycle, sign-off, or risk
      record is written

### Case 10: Accepted risk does not rewrite evidence

**Fixture:** A current FAIL review and a separate owner-signed accepted-risk
record naming its exact run and findings. Repeat with expired and stale records.

**Assertions:**

- [ ] Valid reference is listed under `accepted_risk_refs` with exact hash,
      scope, owner/signature, and expiry
- [ ] Finding remains BLOCKER / OPEN and review remains FAIL
- [ ] Expired, stale, or unbound risk gives no exception
- [ ] Reviewer never creates/signs risk or uses ACCEPTED_RISK as disposition

### Case 11: Large corpus is deterministically bounded

**Fixture:** Twenty-five approved system GDDs across domains and 90 cross-system
edges; every individual GDD fits the byte limit.

**Assertions:**

- [ ] Coordinator produces deterministic domain-node and cross-domain-edge
      shards sorted by the specified keys
- [ ] No shard exceeds 8 GDDs, 32 edges, or 196608 exact input bytes
- [ ] No worker receives the complete 25-GDD corpus or full registry
- [ ] Workers run in bounded concurrency batches until every planned shard runs
- [ ] Coverage accounts for every node, edge, shard, and applicable check
- [ ] A single oversized GDD is unchecked and forces PARTIAL rather than a
      silently enlarged shard

### Case 12: Incremental rename, dirty bytes, and transitive reverse impact

**Fixture:** Baseline graph has A -> B -> C and D -> B. In current input, B keeps
its stable ID but is renamed and its dirty uncommitted bytes change. Another
untracked GDD E depends on C. The baseline and current graphs are both valid.

**Assertions:**

- [ ] B is classified as rename plus content change by stable ID
- [ ] Current dirty/untracked exact bytes participate without Git name-only
- [ ] Baseline/current graph union retains removed/renamed tombstones
- [ ] Fixed-point traversal includes outgoing and incoming transitive impacts,
      including A, C, D, and E where connected
- [ ] Changing pillars, concept, systems index, ruleset, or consistency scope
      forces explicit effective full scope

### Case 13: Worker result merge, deduplication, and conflict

**Fixture:** Two valid workers return the same normalized defect with the same
evidence in different wording. A second run returns the same fingerprint with
incompatible severity or evidence hashes.

**Assertions:**

- [ ] Worker outputs validate against `cgs.cross-gdd-worker/v1`
- [ ] Identical fingerprint is emitted once with all worker provenances
- [ ] Stable finding ID is independent of wording, worker, date, and severity
- [ ] Incompatible same-fingerprint results are retained as
      `RAG.COVERAGE.EVIDENCE_CONFLICT`
- [ ] Coordinator never chooses one conflict result; verdict is PARTIAL

### Case 14: Directed dependency has one authority

**Fixture:** Systems index declares A -> B. A declares its outgoing dependency;
B does not contain “depended on by A.” A second fixture makes A's declaration
disagree with the systems index.

**Assertions:**

- [ ] First fixture has no asymmetry finding and does not require B to duplicate
      the reverse edge
- [ ] Derived incoming adjacency identifies A as B's dependent
- [ ] Second fixture uses `DEPENDENCY_DECLARATION_MISMATCH` as WARNING
- [ ] Report never stores two authoritative copies of the same edge

### Case 15: Current approval is a real precondition

**Fixture:** Four MVP GDDs: one exact-hash approved, one with only index status
Approved, one with a stale approval hash, and one with conflicting approval
records.

**Assertions:**

- [ ] Only the first is APPROVED_CURRENT
- [ ] Others are PROVISIONAL, STALE, or UNBOUND with exact reasons
- [ ] Readable provisional documents may preserve evidence but force PARTIAL
- [ ] No historical record, status text, filename, or self-signoff proves
      approval
- [ ] Approval counts/currentness appear in machine and human reports

### Case 16: Consistency evidence owns registry validation

**Fixture:** Full mode first receives no consistency report, then a stale report,
then a current complete `cgs.consistency-report/v1` that used registry context.

**Assertions:**

- [ ] Missing and stale reports create
      `RAG.COVERAGE.CONSISTENCY_EVIDENCE` and PARTIAL
- [ ] Current report's path/hash/verdict and producer finding IDs are preserved
- [ ] Review never directly loads registry as truth, repopulates it, or decides
      whether registry/GDD wins
- [ ] Design-theory mode neither requires nor reads consistency evidence

### Case 17: Scenario population and deterministic sampling

**Fixture:** Typed graph produces eight candidates with risk ties and a mix of
invariant, persistence, resource, fan-out, formula, and multi-system factors.

**Assertions:**

- [ ] All eight candidates are fingerprinted and scored before selection
- [ ] Exactly five are selected by descending score then stable ID
- [ ] All three unselected candidates retain scores and
      `UNSELECTED_SAMPLE_SCOPE`
- [ ] Normal unselected scope does not force PARTIAL
- [ ] Missing candidate generation or scoring does force PARTIAL
- [ ] Design-theory scenario output is advisory/info only

### Case 18: Strict mode isolation and invalid arguments

**Fixture:** Exercise all four valid modes plus unknown mode, duplicate mode,
duplicate argument kind, baseline outside incremental mode, and extra text.

**Assertions:**

- [ ] Full runs manifest, consistency, theory, and scenario phases
- [ ] Consistency runs only manifest and consistency; theory/scenario are
      NOT_APPLICABLE and no related workers spawn
- [ ] Design-theory runs manifest, theory, and advisory scenario; consistency is
      NOT_APPLICABLE and its file is not read
- [ ] Since-last-review runs full phases over validated impact closure
- [ ] Every invalid invocation returns ERROR with no run verdict or mutation

### Case 19: Versioned severity and verdict matrix

**Fixture:** Independently exercise normative contradiction, acceptance
contradiction, exclusive/non-exclusive ownership, missing dependency, stale
reference, formula mismatch with and without units/approved threshold, undefined
combined state, theory heuristic, and critical unknown.

**Assertions:**

- [ ] Only matrix rules with all deterministic proof conditions yield BLOCKER
- [ ] Missing dependency, stale reference, and undefined combined state are
      WARNING
- [ ] Formula mismatch without complete unit/domain/invariant proof is WARNING
      or COVERAGE_GAP, never blocker by intuition
- [ ] Theory remains ADVISORY and critical unknown becomes COVERAGE_GAP
- [ ] Verdict precedence is ERROR(no run) -> PARTIAL -> FAIL -> CONCERNS -> PASS

### Case 20: Gate-evidence schema and staleness round trip

**Fixture:** Produce a report containing deterministic, advisory, coverage, and
accepted-risk-reference data; then mutate, rename, add, and remove artifacts one
at a time.

**Assertions:**

- [ ] First fenced block parses as `cgs.review-evidence/v1`
- [ ] Generic required fields include record ID, artifact ID, complete artifacts,
      reviewer, producer/version, verdict, timestamp, and stable finding IDs
- [ ] Extension parses as `cgs.cross-gdd-review/v2` and contains mode/scope,
      source revision, ruleset ID/hash, skill-bundle hash, manifest/stale hashes,
      limits, approval summary, baseline, consistency currentness, coverage,
      scenarios, complete findings, dispositions, and accepted-risk references
- [ ] Canonical record ID recomputes after omitting `record_id` and sorting the
      specified keys/arrays
- [ ] Human projection exactly matches machine data
- [ ] Every artifact-set change invalidates stale key; stale evidence cannot pass
      a gate

---

## Protocol Compliance

- [ ] Every applicable input and exclusion has stable identity and exact hash
- [ ] Every MVP input has explicit approval currentness
- [ ] Every required node, edge, check, shard, worker, and selected scenario has
      visible coverage
- [ ] Full reads are confined to bounded shards
- [ ] Imported deterministic findings and theory hypotheses remain separate
- [ ] No reverse dependency duplication is required
- [ ] No registry truth or mutation ownership is assumed
- [ ] Mode-forbidden phases do not read inputs or spawn workers
- [ ] Critical partial/unknown/conflicting evidence cannot PASS or FAIL
- [ ] Machine record and human projection agree
- [ ] Default execution is mutation-free; optional persistence creates one
      immutable report only
- [ ] Handoff is separate and the workflow stops

---

## Coverage Notes

- Cases 1–10 preserve and strengthen P0 report-only, verdict, theory, staleness,
  mutation, and accepted-risk behavior.
- Case 11 closes RAG-006 (bounded corpus and shard coverage).
- Case 12 closes RAG-007 (manifest diff and bidirectional transitive impact).
- Case 13 closes RAG-008 (worker protocol and deterministic merge).
- Case 14 closes RAG-009 (single authoritative directed edge).
- Case 15 closes RAG-010 (current approval precondition).
- Case 16 closes RAG-011 (consistency/registry ownership boundary).
- Case 17 closes RAG-012 (candidate population and risk-ranked sample).
- Case 18 closes RAG-013 (strict mode phase isolation).
- Case 19 closes RAG-014 (versioned severity/verdict matrix).
- Case 20 closes RAG-015 (machine-consumable gate and staleness interface).
