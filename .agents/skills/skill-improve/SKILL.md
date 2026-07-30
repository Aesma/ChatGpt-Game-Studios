---
name: skill-improve
description: "Improve one Codex skill through an independently frozen oracle, isolated candidate staging, reproducible verification, and revision-guarded application that never weakens its own tests or overwrites concurrent edits."
---

# Skill Improve

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

`skill-improve` is a multi-task improvement protocol. It freezes acceptance
evidence before candidate authoring, stages proposed bytes outside the target,
verifies them independently, and applies them only after compare-and-set checks.

It never lets a candidate edit the spec, catalog, rubric, runner, or acceptance
lock used to judge that candidate. It never restores saved file contents over the
workspace.

## Invocation and modes

Use one explicit mode:

```text
$skill-improve freeze --run-id <stable-id> --skill <skill-name> --acceptance <exact-manifest-path> [--prior-lock <path> --oracle-change <receipt-path>]
$skill-improve stage --run-id <stable-id> --lock <exact-oracle-lock-path> --candidate-id <stable-id>
$skill-improve verify --lock <exact-oracle-lock-path> --candidate <exact-candidate-manifest-path> --verification-id <stable-id>
$skill-improve apply --lock <exact-oracle-lock-path> --candidate <exact-candidate-manifest-path> --verification <exact-receipt-path> --application-id <stable-id>
$skill-improve recover --application <exact-failed-application-receipt-path> --direction <forward|reverse> --recovery-id <stable-id>
$skill-improve status --run-id <stable-id> --run-manifest <exact-path>
```

Every mode is a separate task. Require distinct task IDs for oracle owner,
candidate author, verifier, and integrator. A recovery owner must not be the
failed application task. Reject missing, ambiguous, glob, directory-only,
"latest", modification-time, or external paths.

Canonical immutable run evidence lives under:

```text
.codex/skill-improve-runs/<run-id>/
  oracle-lock.md
  candidates/<candidate-id>/
    candidate-manifest.md
    files/<repository-relative-target-paths>
    forward.patch
    inverse.patch
    diff-receipt.md
  verifications/<verification-id>.md
  applications/<application-id>.md
  recoveries/<recovery-id>.md
```

Reject an existing output path. Never overwrite run evidence.

## Contract Manifest

```yaml
schema: cgs-skill-contract/v1
skill: skill-improve
modes:
  freeze: {target: one_skill, mutates_live_target: false}
  stage: {target: one_skill, mutates_live_target: false}
  verify: {target: one_candidate, mutates_live_target: false}
  apply: {target: one_verified_candidate, mutates_live_target: true}
  recover: {target: one_failed_application, mutates_live_target: true}
  status: {target: one_run, mutates_live_target: false}
reads:
  - .agents/skills/**/SKILL.md
  - .agents/skills/**/agents/openai.yaml
  - .codex/agents/**/*.toml
  - CGS Skill Testing Framework/catalog.yaml
  - CGS Skill Testing Framework/quality-rubric.md
  - CGS Skill Testing Framework/skills/**/*.md
  - .agents/skills/skill-test/rules-v1.yaml
  - .agents/skills/skill-test/validator-manifest-v1.yaml
  - CGS Skill Testing Framework/results/skill-test/**/*.yaml
writes:
  oracle_lock:
    path_pattern: ".codex/skill-improve-runs/{run-id}/oracle-lock.md"
  candidate_evidence:
    path_pattern: ".codex/skill-improve-runs/{run-id}/candidates/{candidate-id}/**"
  verification:
    path_pattern: ".codex/skill-improve-runs/{run-id}/verifications/{verification-id}.md"
  application:
    path_pattern: ".codex/skill-improve-runs/{run-id}/applications/{application-id}.md"
  recovery:
    path_pattern: ".codex/skill-improve-runs/{run-id}/recoveries/{recovery-id}.md"
  live_target:
    when: apply_or_recover_after_all_gates
    path_pattern: ".agents/skills/{skill-name}/**"
never_writes:
  - registered behavioral spec
  - testing catalog or rubric
  - skill-test rules, runner, manifest, or receipts
  - acceptance manifest or oracle lock after creation
  - callers, callees, shared schemas, or unrelated skills
authorization: one_complete_changeset_before_each_mode_first_write
operation_states: [FROZEN, STAGED, VERIFIED, APPLIED, PARTIAL_APPLICATION, RECOVERED, BLOCKED, ERROR]
test_states: [PASS, FAIL, PARTIAL, NOT_RUN, STALE, NOT_APPLICABLE]
evidence_classifications: [IMPROVEMENT, NO_CHANGE_REQUIRED, NO_IMPROVEMENT, TEST_NOISE, ENVIRONMENT_CHANGED, REGRESSION, INCONCLUSIVE]
```

This manifest is normative. A candidate-local change cannot expand these writes
or remove a non-write, oracle requirement, role separation, or version and existence conflict check gate.

## Role and mutation boundaries

- **Oracle owner / freeze:** may create only `oracle-lock.md` after independent
  acceptance approval and baseline evidence collection.
- **Candidate author / stage:** may create only a new candidate directory. It
  does not modify the live target or any oracle artifact.
- **Independent verifier / verify:** may create only a new verification receipt.
  It does not modify the candidate, live target, or oracle.
- **Integrator / apply:** may modify only exact live target paths listed in the
  verified candidate and create one application receipt, after all version and existence conflict check checks.
- **Recovery owner / recover:** may apply only the recorded forward or inverse
  patch to paths whose current revisions match that patch's expected preimages, and
  create one recovery receipt.
- **Status:** read-only.

The candidate mutation set may contain exact files inside
`.agents/skills/<skill-name>/`, including `SKILL.md`,
`agents/openai.yaml`, and explicitly named local references/scripts/assets.
It may not contain:

- the registered behavioral spec;
- `CGS Skill Testing Framework/catalog.yaml` or quality rubric;
- test runner/framework code or templates;
- acceptance manifests or oracle locks;
- callers, callees, shared schemas, shared documentation, or unrelated skills.

If any of those must change, stop with `BLOCKED — SEPARATE OWNER CHANGE REQUIRED`.
A separate owner creates and approves that change, then a new oracle is frozen.
It is never bundled into the candidate being judged.

## Status axes

Always report:

- `Workflow Status`: `COMPLETE`, `PARTIAL`, `BLOCKED`, or `ERROR`.
- `Oracle Status`: `FROZEN`, `CHANGED`, `STALE`, `INVALID`, or
  `NOT_APPLICABLE`.
- `Candidate Status`: `NOT_CREATED`, `STAGED`, `VERIFIED`, `REJECTED`,
  `APPLIED`, or `STALE`.
- `Test Status`: `PASS`, `FAIL`, `PARTIAL`, `NOT_RUN`, `STALE`, or
  `NOT_APPLICABLE`.
- `Apply Eligible`: `YES` or `NO`.
- `Mutation Status`: `NONE`, `STAGED_ONLY`, `APPLIED`,
  `PARTIAL_APPLICATION`, or `RECOVERED`.
- `Evidence Classification`: `IMPROVEMENT`, `NO_CHANGE_REQUIRED`,
  `NO_IMPROVEMENT`, `TEST_NOISE`, `ENVIRONMENT_CHANGED`, `REGRESSION`, or
  `INCONCLUSIVE`.
- `Verdict`: `ORACLE_FROZEN`, `CANDIDATE_STAGED`,
  `VERIFIED_IMPROVEMENT`, `NO_CHANGE_REQUIRED`, `NO_IMPROVEMENT`,
  `TEST_NOISE`, `ENVIRONMENT_CHANGED`, `REGRESSION`, `REJECTED`, `APPLIED`,
  `BLOCKED`, or `ERROR`.
- `Persistence`: `NOT_REQUESTED`, `VERIFIED`, or `FAILED`.

A lower warning/failure count is not a verdict. `VERIFIED_IMPROVEMENT` requires
the complete severity- and scenario-based rule in Phase 6.

## Phase 1: Resolve the exact target and impact surface

Require `<skill-name>` to match one exact folder under `.agents/skills/`. Resolve
the target with repository-relative paths and reject symlinks escaping the
project. Inventory all target-local files and record declared revisions.

Resolve the authoritative catalog entry, registered spec, category rubric,
runner/tool implementation and version, applicable templates, and the exact
acceptance manifest. Build a read-only impact graph containing:

- direct callers that name this skill or consume its outputs;
- direct callees/tools/skills the target invokes;
- shared schemas, paths, status enums, and artifact contracts;
- metadata/UI entry points; and
- owners that must review any impacted external contract.

Use the exact discovery/name/exclusion/budget rules from
`.agents/skills/skill-test/rules-v1.yaml` and first validate that file against
the pinned `validator-manifest-v1.yaml`. Record its declared revision and full
selected/loaded/failed/omitted/excluded ledger. Direct edges require path/line
evidence: exact `$skill-name` calls, declared artifact paths or schemas, shared
status/verdict tokens, catalog/spec references, or metadata entry points. Search
all selected skill packages, registered specs, catalog entries, and shared docs;
do not infer an edge only from similar prose.

Record exact paths, stable edge IDs, owners, source revisions, and the graph's
canonical revision. A missing/revision mismatched skill-test authority, unresolved edge,
unreadable prefix, exclusion, or over-budget surface makes the oracle PARTIAL and
prevents application. Do not let the candidate author decide that an external
contract is "not directly affected."

## Phase 2: Freeze the oracle before candidate work

`freeze` requires an independently approved
`skill-improve-acceptance-manifest` containing:

- artifact/schema version, run and target IDs, oracle-owner task ID;
- user objective and stable acceptance-scenario IDs;
- severity taxonomy and non-negotiable safety/authorization requirements;
- required static, category, behavioral, runtime, side-effect, timeout,
  recovery, and concurrency scenarios;
- exact commands/argv, runner/tool versions and revisions, environment,
  fixtures/seeds, expected outputs, and result parsers;
- allowed candidate mutation scope and forbidden oracle paths;
- impact-graph file/byte budget and required owners; and
- approval identity/timestamp plus manifest revision;
- exact current skill-test rules/validator-manifest revisions and required
  `cgs-skill-test-receipt/v2` paths; and
- an evidence-class declaration for every scenario: written-contract,
  runtime, side-effect, timeout, recovery, concurrency, or manual.

For every required skill-test receipt, validate schema and declared revision, revalidate
every recorded dependency, and require freshness `CURRENT`. Map its independent
validation exactly:

- `COMPLIANT` or `WARNINGS` may satisfy only mapped written-contract rows;
- `NON-COMPLIANT` is a conclusive baseline/candidate failure;
- `PARTIAL_VALIDATION` makes Test Status `PARTIAL`;
- `TEST_INFRA_INVALID`, receipt `INVALID`, `STALE`, or `UNVERIFIED`
  makes the mapped suite `NOT_RUN`.

Never convert a skill-test `COMPLIANT` receipt into runtime, authorization
ordering, tool side-effect, timeout, recovery, or concurrency proof. Freeze the
receipt path/revision, freshness trace, rules/manifest revisions, stable outcomes, and
aggregation trace. `freeze` does not create or refresh a skill-test receipt;
that is independent pre-existing evidence.

Before any candidate exists, execute every required baseline suite against the
live target. Each execution receipt must record command/argv, working directory,
tool/version/revision, environment, start/end timestamps, exit code, stdout/stderr
and result paths/revisions, scenario-level outcomes, and producer/task identity.
A missing command, exit code, timestamp, tool revision, or result revision is `NOT_RUN`,
not PASS. A timeout, unavailable runner, incomplete suite, or unresolved impact
graph makes `Test Status: PARTIAL/NOT_RUN` and `Apply Eligible: NO`.

Assign stable finding/requirement IDs and severities. Freeze exact revisions for:

- every live target-local file;
- acceptance manifest and user objective;
- registered spec, catalog entry, category rubric, templates, runner/tool;
- skill-test rules/manifest plus every consumed receipt and freshness trace;
- required fixture/scenario set and baseline execution receipts;
- impact graph and shared contract set; and
- normalized baseline findings.

Use this header:

```markdown template
Artifact Type: skill-improve-oracle-lock
Schema Version: 1
Run ID: <stable-id>
Target Skill: <name>
Oracle Owner Task ID: <task-id>
Target Source Set revision: <revision:...>
Acceptance Manifest Path/revision: <path/revision>
Spec Path/revision: <path/revision>
Catalog Path/Entry revision: <path/revision>
Rubric Path/revision: <path/revision>
Runner/Tool Identity/revision: <values>
Skill-Test Rules/Manifest revision: <values>
Skill-Test Receipt Set/Freshness revision: <values>
Scenario Set revision: <revision:...>
Baseline Receipt Set revision: <revision:...>
Impact Graph revision: <revision:...>
Oracle Status: FROZEN
Test Status: PASS | FAIL | PARTIAL | NOT_RUN
Apply Eligible: NO
Created At UTC: <RFC3339>
```

Preview the exact one-file CREATE and non-writes. After authorization, revalidate all
sources, write the lock atomically, re-read it, and report its revision. A changed
source blocks the lock. The oracle is immutable after creation.

Do not stop merely because the old suite is green. Compare the frozen spec and
scenarios with the user objective, safety constraints, runtime/side-effect
coverage, and impact graph. A green but incomplete oracle is PARTIAL, not evidence
that no improvement is needed.

## Phase 3: Handle legitimate oracle changes separately

A candidate never edits its own oracle. If the behavior contract genuinely needs
revision, the spec/catalog/rubric/runner owner must create an independent,
authorized, immutable `skill-improve-oracle-change-receipt` before a new freeze.

A new freeze that uses `--prior-lock` and `--oracle-change` must validate:

- prior lock path/revision and target identity;
- old and new oracle paths/revisions;
- stable requirement IDs added, removed, changed, or retained;
- rationale, responsible owner, approval identity/timestamp;
- explicit legacy requirements waived by the product/safety owner; and
- compatibility/impact review for every caller, callee, and shared schema.

The new lock must preserve both oracle identities. Candidate verification runs
the candidate against both old and new oracle suites and reports a dual-oracle
matrix. A green new suite does not erase an old-oracle regression. Any lost
safety/authorization requirement requires an explicit approved waiver; otherwise
the candidate is REJECTED.

The candidate author, verifier, or integrator cannot act as oracle-change owner.

## Phase 4: Stage a candidate without touching the target

`stage` revalidates the exact oracle-lock revision and every current oracle/source
revision. If the live target changed since freeze, return
`BLOCKED — CONCURRENT TARGET CHANGE; NEW ORACLE REQUIRED` before writing.

Diagnose against stable baseline findings, the user objective, and impact graph.
Do not rewrite passing material for style or broaden to external contracts.

Present:

- targeted stable finding/requirement IDs;
- exact target-local CREATE/MODIFY/DELETE paths;
- before/after excerpts or binary-safe revision description;
- expected scenario changes and severity effect;
- explicit oracle/shared/external non-writes;
- risks and recovery strategy.

Deletion requires explicit path-level authorization and cannot remove required
metadata or oracle-observed behavior merely to make a test disappear.

After bounded authorization, create only the candidate mirror and manifests.
Never edit live target bytes. The candidate manifest must bind:

- run/candidate/target IDs and candidate-author task ID;
- oracle-lock path/revision and frozen target source-set revision;
- exact candidate file path/base revision/candidate revision/action table;
- canonical forward patch with per-file approved prior state/applied state revisions;
- canonical inverse patch that applies only candidate revision -> base revision;
- immutable `diff-receipt.md` with every source path/raw base revision/action/raw
  candidate revision, full canonical diff revision, patch-tool/version/revision, diff options,
  newline/binary policy, and forward/inverse patch revisions;
- targeted findings, expected results, impact graph, and non-writes;
- candidate aggregate revision and creation timestamp; and
- `Candidate Status: STAGED`, `Mutation Status: STAGED_ONLY`.

Verify candidate files and both patches by applying them in disposable copies, not
the live target. Reject existing paths or inconsistent patches.

If the proposed fix requires oracle/shared changes, do not create a misleading
partial candidate. Return BLOCKED and the separate owner handoff.

## Phase 5: Verify independently against the frozen oracle

`verify` requires a verifier task ID different from the oracle owner, candidate
author, and any oracle-change owner. revalidate the lock, candidate manifest/files/
patches, every frozen oracle artifact, runner, fixture, and current live base.

If any revision changed, return STALE/BLOCKED. Do not update the lock to match.

Run every frozen required suite against the isolated candidate mirror. The runner
must accept an exact candidate manifest/root and must not resolve the live skill
by name. Validate the runner's path/version/revision/allowed argv/output schema before
execution.

The current `skill-test` pinned manifest exposes live repository
`static|audit|manifest` argv only; it does not authorize a candidate root.
Therefore a live-target skill-test receipt cannot be reused as candidate proof,
and static/spec/category candidate rows remain `NOT_RUN` until an independently
owned, frozen candidate-aware runner contract exists. If any required runner
cannot test the candidate without installing or replacing the live target,
report `Test Status: NOT_RUN`, `Evidence Classification: INCONCLUSIVE`, and
`Apply Eligible: NO`. Do not temporarily swap live files.

Record the same full execution receipt fields as baseline, plus candidate
aggregate revision. Preserve stable requirement/finding IDs and produce a matrix:

| Requirement/Scenario ID | Severity | Baseline | Candidate | Delta | Evidence Receipt |
|---|---|---|---|---|---|

For changed oracle runs, include separate Old Oracle and New Oracle columns plus
the approved waiver receipt for every intentionally removed legacy requirement.

No test result may be PASS when its command, exit code, timestamps, runner revision,
environment, output revisions, or required assertions are missing.

## Phase 6: Determine improvement without score gaming

Return `VERIFIED_IMPROVEMENT` only when all are true:

1. every frozen required suite and scenario executed conclusively;
2. every user-objective acceptance scenario passes;
3. every targeted blocker/finding is RESOLVED with evidence;
4. no new P0/P1, safety, authorization, side-effect, concurrency, timeout, or
   recovery regression exists;
5. every non-targeted frozen requirement is unchanged or improved;
6. impact-graph contracts remain compatible or have separate owner approval;
7. oracle/spec/catalog/rubric/runner revisions are unchanged from the lock, or the
   valid dual-oracle protocol was used;
8. all candidate paths remain inside the authorized target-local scope; and
9. verification receipt persistence succeeds and re-reads correctly.

Reject a candidate when any non-waived old-oracle requirement regresses, even if
the new suite is green. A new P0 or P1 cannot be offset by any number of resolved
P2/P3 warnings. Counts, pass percentages, or aggregate scores are supporting data
only.

Classify the evidence before choosing a verdict:

| Classification | Exact condition | Result |
|---|---|---|
| `IMPROVEMENT` | all nine predicates pass and at least one targeted requirement moves failing -> passing | VERIFIED / PASS / Apply Eligible YES / `VERIFIED_IMPROVEMENT` |
| `NO_CHANGE_REQUIRED` | baseline already satisfies the user objective, no targeted finding is open, and the candidate is empty or byte-identical | REJECTED / PASS / Apply Eligible NO / `NO_CHANGE_REQUIRED` |
| `NO_IMPROVEMENT` | execution is conclusive but an open targeted finding is unchanged and no regression exists | REJECTED / FAIL / Apply Eligible NO / `NO_IMPROVEMENT` |
| `TEST_NOISE` | frozen runner, environment, inputs, and seeds are identical but the bounded repeat policy produces inconsistent outcomes | STAGED / PARTIAL / Apply Eligible NO / `TEST_NOISE` |
| `ENVIRONMENT_CHANGED` | environment/tool/dependency identity differs from the lock before comparison | STALE / STALE / Apply Eligible NO / `ENVIRONMENT_CHANGED` |
| `REGRESSION` | any non-waived frozen requirement worsens, including a new P0/P1 or safety failure | REJECTED / FAIL / Apply Eligible NO / `REGRESSION` |
| `INCONCLUSIVE` | any required suite is NOT_RUN/PARTIAL, receipt is non-current, impact is partial, or evidence fields are missing | STAGED / PARTIAL or NOT_RUN / Apply Eligible NO / `BLOCKED` |

The acceptance manifest fixes repeat count, seed, order, timeout, and noise
classifier before baseline execution. Never invent reruns after seeing a failure.
A changed environment is not test noise; a deterministic worse outcome is a
regression; and an unresolved baseline defect is not `NO_CHANGE_REQUIRED`.

Persist one immutable verification receipt with all revisions, commands, results,
severity comparison, dual-oracle matrix when applicable, impact review,
evidence classification with decision trace, exact diff-receipt revision, verdict,
and verifier task ID. This receipt does not change the live target.

## Phase 7: Apply with all-file compare-and-set

`apply` requires a fresh integrator task ID distinct from oracle owner, candidate
author, and verifier. Revalidate the exact oracle lock, candidate, VERIFIED
verification receipt, runner/oracle revisions, impact approvals, and every live
target path.

Before any live write:

1. every current live target revision must equal its candidate base/approved prior state revision;
2. every candidate file revision and forward/inverse patch revision must match;
3. every oracle/shared artifact revision must equal the frozen lock;
4. candidate Test Status must be PASS and Apply Eligible YES;
5. target path set must exactly equal the authorized mutation set; and
6. all target paths and run evidence destinations must be unused or have the
   expected explicit pre-state.

Any mismatch returns `BLOCKED — CONCURRENT CHANGE` and writes nothing. Never
overwrite, merge around, or "restore" the changed file.

Preview the exact target mutation set and application-receipt CREATE. Obtain one
bounded authorization unless already explicitly granted for that exact set.
Prepare all applied state bytes in same-filesystem temporary paths and verify them
before publication. Publish as one transaction where supported and re-read every
target.

The application receipt records base/candidate/applied declared revisions per file, the
complete diff-receipt and forward/inverse patch revisions, patch-tool/version/revision,
oracle/candidate/verification revisions, integrator task ID, environment identity,
timestamps, transaction steps, observed final revisions, and result
`APPLIED`, `PARTIAL_APPLICATION`, or `FAILED`.

Only exact verified postimages plus a verified receipt return:

```text
Workflow Status: COMPLETE
Oracle Status: FROZEN
Candidate Status: APPLIED
Test Status: PASS
Apply Eligible: NO
Mutation Status: APPLIED
Verdict: APPLIED
Persistence: VERIFIED
```

Application consumes eligibility; it does not imply that catalog run-evidence
fields were recorded. That is a separate recorder responsibility.

## Phase 8: Safe failure and recovery

Never restore saved original contents, use repository-wide reset, or blindly copy
a baseline snapshot over current files.

If application is interrupted or verification finds mixed base/candidate states:

1. stop all writes;
2. Record exact current revisions and classify every path as BASE, CANDIDATE, or
   DIVERGED;
3. create or complete a failed application receipt without overwriting an
   existing receipt;
4. return `PARTIAL_APPLICATION / BLOCKED — RECOVERY REQUIRED`; and
5. require a separate `recover` invocation.

`recover` reads the failed receipt and requested recorded patch direction:

- forward expects each affected path at its recorded base/approved prior state revision and moves
  it to the candidate/applied state revision;
- reverse expects each affected path at its exact candidate/applied state revision and
  applies the inverse patch to the base revision.

Perform an all-file version and existence conflict check preflight before any recovery write. If any path is
DIVERGED, changed after failure, missing unexpectedly, or does not match the
chosen direction's approved prior state, return `BLOCKED — CONCURRENT RECOVERY CHANGE` and
write nothing. Preserve external edits.

Preview and authorize the exact recovery paths plus new receipt. Apply only the
recorded patch, re-read all files, and persist the recovery receipt. Never recover
by replacing a file with saved original full text. A conflict requires human
three-way resolution in a separately authorized task.

The recovery evidence is retained under the immutable run root: candidate
postimages, `forward.patch`, `inverse.patch`, `diff-receipt.md`, failed
application receipt, and every recovery receipt. The acceptance manifest sets an
RFC3339 `retain_until`; absent a value, retention is indefinite. No mode deletes
or prunes evidence. Cleanup is a separate explicitly authorized task permitted
only after the retention deadline and a terminal APPLIED or RECOVERED receipt.

Manual recovery handoff lists exact current/base/candidate revisions, the first
diverged path, intended direction, patch/tool revisions, and these steps: preserve
current bytes, inspect a three-way diff outside this workflow, obtain path-level
authorization for a new patch, apply with all-file version and existence conflict check, re-read every file, and
write a new immutable recovery receipt. It never tells an operator to copy a
backup over the workspace.

A later regression discovered after a successful application is not an automatic
rollback. Classify it as `REGRESSION` evidence and start a new improvement run
from current bytes or use an explicitly authorized, revision-guarded patch workflow.

## Phase 9: Status and handoff

`status` validates the exact run manifest and all referenced immutable artifacts.
It is read-only and never chooses the newest candidate, verification, application,
or recovery by mtime.

Every mode reports exact paths/revisions, roles/task IDs, oracle and impact identity,
execution receipts, skill-test receipt freshness/partial mapping, stable
requirements/findings, severity deltas, evidence classification, retention and
manual-recovery status, mutation boundary, all status axes, and next owner.

Do not chain automatically into `skill-test`, another improvement run, catalog
updates, caller/schema edits, commits, or publication. Missing execution evidence
is NOT_RUN, not success. No director gate applies.

## P1 audit traceability

The IDs below are copied exactly from the authoritative 2026-07-20
`skill-improve` P1 audit table. Each row independently binds one finding to its
normative clause and dedicated-spec case/assertions. The table does not claim
that any case was executed.

| Audit ID | Normative clause | Dedicated spec evidence |
|---|---|---|
| `IMPROVE-P1-001` | Phase 6 severity-first, non-offsettable improvement predicates | Case 3 — `SI-C03-A01`, `SI-C03-A02`, `SI-C03-A03` |
| `IMPROVE-P1-002` | Phase 2 frozen oracle completeness/currentness and Phase 3 separate oracle revision | Cases 1 and 9 — `SI-C01-A02`, `SI-C01-A04`, `SI-C09-A01`, `SI-C09-A02` |
| `IMPROVE-P1-003` | Phase 2 evidence-capability limits and Phase 5 independent verification | Case 2 — `SI-C02-A01`, `SI-C02-A02`, `SI-C02-A03` |
| `IMPROVE-P1-004` | Phase 1 bounded impact surface and Phase 2 frozen impact graph | Case 4 — `SI-C04-A01`, `SI-C04-A02`, `SI-C04-A03` |
| `IMPROVE-P1-005` | Phases 5 and 7 revision/tool/diff/application receipts and read-back | Case 5 — `SI-C05-A01`, `SI-C05-A02`, `SI-C05-A03`, `SI-C05-A04` |
| `IMPROVE-P1-006` | Status axes plus Phases 5–6 fail-closed partial/unavailable classification | Case 6 — `SI-C06-A01`, `SI-C06-A02`, `SI-C06-A03`, `SI-C06-A04` |
| `IMPROVE-P1-007` | Phase 8 immutable recovery evidence, retention, and manual recovery | Case 7 — `SI-C07-A01`, `SI-C07-A02`, `SI-C07-A03`, `SI-C07-A04` |
| `IMPROVE-P1-008` | Phase 6 deterministic evidence classification | Case 8 — `SI-C08-A01`, `SI-C08-A02`, `SI-C08-A03`, `SI-C08-A04` |
