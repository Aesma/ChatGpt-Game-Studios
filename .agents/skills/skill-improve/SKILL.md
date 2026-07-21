---
name: skill-improve
description: "Improve one Codex skill through an independently frozen oracle, isolated candidate staging, reproducible verification, and hash-guarded application that never weakens its own tests or overwrites concurrent edits."
---

# Skill Improve

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
  verifications/<verification-id>.md
  applications/<application-id>.md
  recoveries/<recovery-id>.md
```

Reject an existing output path. Never overwrite run evidence.

## Role and mutation boundaries

- **Oracle owner / freeze:** may create only `oracle-lock.md` after independent
  acceptance approval and baseline evidence collection.
- **Candidate author / stage:** may create only a new candidate directory. It
  does not modify the live target or any oracle artifact.
- **Independent verifier / verify:** may create only a new verification receipt.
  It does not modify the candidate, live target, or oracle.
- **Integrator / apply:** may modify only exact live target paths listed in the
  verified candidate and create one application receipt, after all CAS checks.
- **Recovery owner / recover:** may apply only the recorded forward or inverse
  patch to paths whose current hashes match that patch's expected preimages, and
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
- `Verdict`: `ORACLE_FROZEN`, `CANDIDATE_STAGED`,
  `VERIFIED_IMPROVEMENT`, `NO_CHANGE_REQUIRED`, `REJECTED`, `APPLIED`,
  `BLOCKED`, or `ERROR`.
- `Persistence`: `NOT_REQUESTED`, `VERIFIED`, or `FAILED`.

A lower warning/failure count is not a verdict. `VERIFIED_IMPROVEMENT` requires
the complete severity- and scenario-based rule in Phase 6.

## Phase 1: Resolve the exact target and impact surface

Require `<skill-name>` to match one exact folder under `.agents/skills/`. Resolve
the target with repository-relative paths and reject symlinks escaping the
project. Inventory all target-local files and compute raw SHA-256 hashes.

Resolve the authoritative catalog entry, registered spec, category rubric,
runner/tool implementation and version, applicable templates, and the exact
acceptance manifest. Build a read-only impact graph containing:

- direct callers that name this skill or consume its outputs;
- direct callees/tools/skills the target invokes;
- shared schemas, paths, status enums, and artifact contracts;
- metadata/UI entry points; and
- owners that must review any impacted external contract.

Record exact paths, stable IDs, and hashes. An unresolved or over-budget impact
surface makes the oracle PARTIAL and prevents application. Do not let the
candidate author decide that an external contract is "not directly affected."

## Phase 2: Freeze the oracle before candidate work

`freeze` requires an independently approved
`skill-improve-acceptance-manifest` containing:

- artifact/schema version, run and target IDs, oracle-owner task ID;
- user objective and stable acceptance-scenario IDs;
- severity taxonomy and non-negotiable safety/authorization requirements;
- required static, category, behavioral, runtime, side-effect, timeout,
  recovery, and concurrency scenarios;
- exact commands/argv, runner/tool versions and hashes, environment,
  fixtures/seeds, expected outputs, and result parsers;
- allowed candidate mutation scope and forbidden oracle paths;
- impact-graph file/byte budget and required owners; and
- approval identity/timestamp plus manifest SHA-256.

Before any candidate exists, execute every required baseline suite against the
live target. Each execution receipt must record command/argv, working directory,
tool/version/hash, environment, start/end timestamps, exit code, stdout/stderr
and result paths/hashes, scenario-level outcomes, and producer/task identity.
A missing command, exit code, timestamp, tool hash, or result hash is `NOT_RUN`,
not PASS. A timeout, unavailable runner, incomplete suite, or unresolved impact
graph makes `Test Status: PARTIAL/NOT_RUN` and `Apply Eligible: NO`.

Assign stable finding/requirement IDs and severities. Freeze exact hashes for:

- every live target-local file;
- acceptance manifest and user objective;
- registered spec, catalog entry, category rubric, templates, runner/tool;
- required fixture/scenario set and baseline execution receipts;
- impact graph and shared contract set; and
- normalized baseline findings.

Use this header:

```markdown
Artifact Type: skill-improve-oracle-lock
Schema Version: 1
Run ID: <stable-id>
Target Skill: <name>
Oracle Owner Task ID: <task-id>
Target Source Set SHA-256: <sha256:...>
Acceptance Manifest Path/SHA-256: <path/hash>
Spec Path/SHA-256: <path/hash>
Catalog Path/Entry SHA-256: <path/hash>
Rubric Path/SHA-256: <path/hash>
Runner/Tool Identity/SHA-256: <values>
Scenario Set SHA-256: <sha256:...>
Baseline Receipt Set SHA-256: <sha256:...>
Impact Graph SHA-256: <sha256:...>
Oracle Status: FROZEN
Test Status: PASS | FAIL | PARTIAL | NOT_RUN
Apply Eligible: NO
Created At UTC: <RFC3339>
```

Preview the exact one-file CREATE and non-writes. After authorization, re-hash all
sources, write the lock atomically, re-read it, and report its SHA-256. A changed
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

- prior lock path/hash and target identity;
- old and new oracle paths/hashes;
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

`stage` revalidates the exact oracle-lock hash and every current oracle/source
hash. If the live target changed since freeze, return
`BLOCKED — CONCURRENT TARGET CHANGE; NEW ORACLE REQUIRED` before writing.

Diagnose against stable baseline findings, the user objective, and impact graph.
Do not rewrite passing material for style or broaden to external contracts.

Present:

- targeted stable finding/requirement IDs;
- exact target-local CREATE/MODIFY/DELETE paths;
- before/after excerpts or binary-safe hash description;
- expected scenario changes and severity effect;
- explicit oracle/shared/external non-writes;
- risks and recovery strategy.

Deletion requires explicit path-level authorization and cannot remove required
metadata or oracle-observed behavior merely to make a test disappear.

After bounded authorization, create only the candidate mirror and manifests.
Never edit live target bytes. The candidate manifest must bind:

- run/candidate/target IDs and candidate-author task ID;
- oracle-lock path/hash and frozen target source-set hash;
- exact candidate file path/base hash/candidate hash/action table;
- canonical forward patch with per-file preimage/postimage hashes;
- canonical inverse patch that applies only candidate hash -> base hash;
- targeted findings, expected results, impact graph, and non-writes;
- candidate aggregate SHA-256 and creation timestamp; and
- `Candidate Status: STAGED`, `Mutation Status: STAGED_ONLY`.

Verify candidate files and both patches by applying them in disposable copies, not
the live target. Reject existing paths or inconsistent patches.

If the proposed fix requires oracle/shared changes, do not create a misleading
partial candidate. Return BLOCKED and the separate owner handoff.

## Phase 5: Verify independently against the frozen oracle

`verify` requires a verifier task ID different from the oracle owner, candidate
author, and any oracle-change owner. Re-hash the lock, candidate manifest/files/
patches, every frozen oracle artifact, runner, fixture, and current live base.

If any hash changed, return STALE/BLOCKED. Do not update the lock to match.

Run every frozen required suite against the isolated candidate mirror. The runner
must accept an exact candidate manifest/root and must not resolve the live skill
by name. If the runner cannot test the candidate without installing or replacing
the live target, report `Test Status: NOT_RUN` and `Apply Eligible: NO`. Do not
temporarily swap live files.

Record the same full execution receipt fields as baseline, plus candidate
aggregate hash. Preserve stable requirement/finding IDs and produce a matrix:

| Requirement/Scenario ID | Severity | Baseline | Candidate | Delta | Evidence Receipt |
|---|---|---|---|---|---|

For changed oracle runs, include separate Old Oracle and New Oracle columns plus
the approved waiver receipt for every intentionally removed legacy requirement.

No test result may be PASS when its command, exit code, timestamps, runner hash,
environment, output hashes, or required assertions are missing.

## Phase 6: Determine improvement without score gaming

Return `VERIFIED_IMPROVEMENT` only when all are true:

1. every frozen required suite and scenario executed conclusively;
2. every user-objective acceptance scenario passes;
3. every targeted blocker/finding is RESOLVED with evidence;
4. no new P0/P1, safety, authorization, side-effect, concurrency, timeout, or
   recovery regression exists;
5. every non-targeted frozen requirement is unchanged or improved;
6. impact-graph contracts remain compatible or have separate owner approval;
7. oracle/spec/catalog/rubric/runner hashes are unchanged from the lock, or the
   valid dual-oracle protocol was used;
8. all candidate paths remain inside the authorized target-local scope; and
9. verification receipt persistence succeeds and re-reads correctly.

Reject a candidate when any non-waived old-oracle requirement regresses, even if
the new suite is green. A new P0 or P1 cannot be offset by any number of resolved
P2/P3 warnings. Counts, pass percentages, or aggregate scores are supporting data
only.

Map results:

- all improvement predicates true -> VERIFIED / PASS / Apply Eligible YES /
  `VERIFIED_IMPROVEMENT`;
- full conclusive evidence but no targeted behavioral improvement ->
  REJECTED / FAIL / Apply Eligible NO / `NO_CHANGE_REQUIRED` or `REJECTED`;
- any missing/partial/nonconclusive execution -> STAGED / PARTIAL or NOT_RUN /
  Apply Eligible NO / `BLOCKED`;
- any stale oracle/base/candidate -> STALE / STALE / Apply Eligible NO /
  `BLOCKED`.

Persist one immutable verification receipt with all hashes, commands, results,
severity comparison, dual-oracle matrix when applicable, impact review, verdict,
and verifier task ID. This receipt does not change the live target.

## Phase 7: Apply with all-file compare-and-set

`apply` requires a fresh integrator task ID distinct from oracle owner, candidate
author, and verifier. Revalidate the exact oracle lock, candidate, VERIFIED
verification receipt, runner/oracle hashes, impact approvals, and every live
target path.

Before any live write:

1. every current live target hash must equal its candidate base/preimage hash;
2. every candidate file hash and forward/inverse patch hash must match;
3. every oracle/shared artifact hash must equal the frozen lock;
4. candidate Test Status must be PASS and Apply Eligible YES;
5. target path set must exactly equal the authorized mutation set; and
6. all target paths and run evidence destinations must be unused or have the
   expected explicit pre-state.

Any mismatch returns `BLOCKED — CONCURRENT CHANGE` and writes nothing. Never
overwrite, merge around, or "restore" the changed file.

Preview the exact target mutation set and application-receipt CREATE. Obtain one
bounded authorization unless already explicitly granted for that exact set.
Prepare all postimage bytes in same-filesystem temporary paths and verify them
before publication. Publish as one transaction where supported and re-read every
target.

The application receipt records base/candidate/applied hashes per file, forward/
inverse patch hashes, oracle/candidate/verification hashes, integrator task ID,
timestamps, transaction steps, observed final hashes, and result
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
2. record exact current hashes and classify every path as BASE, CANDIDATE, or
   DIVERGED;
3. create or complete a failed application receipt without overwriting an
   existing receipt;
4. return `PARTIAL_APPLICATION / BLOCKED — RECOVERY REQUIRED`; and
5. require a separate `recover` invocation.

`recover` reads the failed receipt and requested recorded patch direction:

- forward expects each affected path at its recorded base/preimage hash and moves
  it to the candidate/postimage hash;
- reverse expects each affected path at its exact candidate/postimage hash and
  applies the inverse patch to the base hash.

Perform an all-file CAS preflight before any recovery write. If any path is
DIVERGED, changed after failure, missing unexpectedly, or does not match the
chosen direction's preimage, return `BLOCKED — CONCURRENT RECOVERY CHANGE` and
write nothing. Preserve external edits.

Preview and authorize the exact recovery paths plus new receipt. Apply only the
recorded patch, re-read all files, and persist the recovery receipt. Never recover
by replacing a file with saved original full text. A conflict requires human
three-way resolution in a separately authorized task.

A later regression discovered after a successful application is not an automatic
rollback. Start a new improvement run from current bytes or use an explicitly
authorized, hash-guarded patch workflow.

## Phase 9: Status and handoff

`status` validates the exact run manifest and all referenced immutable artifacts.
It is read-only and never chooses the newest candidate, verification, application,
or recovery by mtime.

Every mode reports exact paths/hashes, roles/task IDs, oracle and impact identity,
execution receipts, stable requirements/findings, severity deltas, mutation
boundary, all status axes, and next owner.

Do not chain automatically into `skill-test`, another improvement run, catalog
updates, caller/schema edits, commits, or publication. Missing execution evidence
is NOT_RUN, not success. No director gate applies.
