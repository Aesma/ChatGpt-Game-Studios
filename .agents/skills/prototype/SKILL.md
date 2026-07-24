---
name: prototype
description: Run one finite throwaway experiment inside an approved isolated root, with pinned dependency/build identity, hash-bound run evidence, consent-safe observations, advisory recommendations, and user-owned recoverable decisions.
---

# Prototype

Run one disposable experiment against one falsifiable hypothesis. This workflow is not a design approval, production implementation, phase gate, portfolio decision, or authority to invoke downstream work.

## Invocation

```text
$prototype <concept-or-question> [--path html|engine|paper] [--spike]
           [--pivot <pivot-record-path> --expect-pivot <sha256:...>]
```

A concept or concrete experimental question is required. With none, show usage and stop without reading project files, delegating, creating a worktree/directory/checkpoint, or writing.

`--pivot` and `--expect-pivot` are an inseparable pair. They select one exact immutable `cgs.prototype-pivot/v1` record; moving aliases such as `latest` are invalid. A pivot continuation receives a new prototype/run/hypothesis ID, root, budget, and authorization.

An implementer may execute the approved experiment. It receives authority only for the exact execution manifest; it cannot expand scope, approve evidence, choose a product direction, publish project state, or invoke another workflow.

## Separate authority boundaries

There are three independent decisions:

1. **Execution authorization** permits the exact isolated worktree/root action, authored paths, generated subtrees, commands, dependencies, evidence, run receipt, and chosen cleanup/retention action.
2. **User routing decision** records `PROCEED`, `PIVOT`, `KILL`, `DEFER`, or `MORE_EVIDENCE` after evidence is shown. It changes no file by itself.
3. **Publication authorization** permits one exact all-or-none publication group after a user decision.

Content approval, risk acceptance, consent, execution approval, user routing choice, publication approval, cleanup authorization, and downstream work are never interchangeable.

Before execution authorization there are zero persistent writes, including no checkpoint, worktree, temp directory, dependency download/install, cache, generated project, lockfile, log, or evidence file.

## Non-negotiable invariants

- All experiment writes stay within one new approved throwaway root or its explicitly approved isolated worktree/temp root.
- Existing user/worktree changes are inventoried but never reverted, overwritten, staged, committed, moved, or cleaned.
- Prototype and production code/assets cannot import, link, load, generate into, or write each other in either direction.
- All dependency, cache, temp, user-data, build, and generated-output locations are exact descendants of the approved isolation root.
- Every iteration, command, consecutive failure, elapsed time, file count, and byte budget is hard, monotonic, and finite.
- Build/play claims require current-run receipts bound to exact source, dependency-lock, toolchain, command, artifact, and evidence hashes.
- Every skipped step uses the typed skip taxonomy; a skip is never a pass.
- Recommendations are advisory. Only an explicit user response can create a routing decision.
- Report/index/decision/pivot/graveyard publication is all-or-none or remains non-authoritative.
- KILL is non-destructive, explicitly confirmed, recoverable, and never forced by pivot/iteration count.
- No mode-selection success probability is asserted without a named, applicable measured dataset.

## Phase 0 — Read-only experiment definition

Define exactly one falsifiable hypothesis:

> If participant/system X performs action Y under condition Z, measured signal M will meet threshold T.

Record a stable hypothesis ID, riskiest assumption, one mechanic/question, measurable success/failure/inconclusive thresholds, evidence the selected mode cannot establish, and excluded scope. Narrow unfalsifiable prompts such as “is it fun?” before continuing.

Read only the minimum exact project context required to avoid conflicts and choose a mode. Existing concepts, GDDs, source, assets, prototypes, and project status are context, not write authorization.

### Evidence-capability mode selection — PROTO-P1-001

Choose using capability and limitation evidence, never an unsupported success percentage:

| Mode | Can provide | Cannot establish by itself |
|---|---|---|
| `html` | browser-load, interaction logic, clarity and coarse timing evidence | native engine timing, target-platform performance, production rendering feel |
| `engine` | pinned-engine physics/timing/render/build evidence | fun or player value without actual participants/evidence |
| `paper` | rules, choices, comprehension and facilitator-observation evidence | digital moment-to-moment feel, engine feasibility or executable build status |
| `spike` | one technical feasibility measurement | product desirability or design approval |

If historical success-rate data is offered, record dataset path/hash, sample definition/count, period, measured outcome, confidence/uncertainty, and applicability to this exact hypothesis. Otherwise state `mode_success_probability: NOT_ESTABLISHED`. Never use an inherited, anecdotal, or generic numeric probability as mode guidance.

## Phase 1 — Freeze identity, source, toolchain, and worktree protection

Create in memory:

```yaml
prototype_id: PT-<slug>-<run-id>
run_id: PTRUN-<UTC-basic-milliseconds>-<source8>-<hypothesis8>
hypothesis_id: HYP-<run-id>-001
mode: html | engine | paper | spike
isolation_mode: git_worktree | isolated_temp_root | current_workspace_bounded_root
throwaway_root: <exact new absolute and repository-relative identity>
parent_pivot: NOT_SUPPLIED | { path: ..., sha256: ... }
```

Freeze an exact read-only preflight packet:

- repository root, VCS HEAD/commit when available, current branch, Git implementation/version, and submodule state;
- pre-existing dirty/untracked path inventory with raw path and content hash/size where readable, plus canonical dirty-manifest SHA-256;
- exact project context paths/SHA-256 used by the plan;
- this `SKILL.md` and `references/continued-workflow.md` exact paths/SHA-256 values;
- OS/architecture, engine/runtime/SDK/compiler/build-tool/package-manager names and exact versions;
- engine executable or runtime path/hash where available;
- dependency manifest path/hash, lockfile path/hash, registry/source identity, and offline/cache state;
- build configuration and environment-variable allowlist hash, with secrets redacted and never persisted;
- expected generated-output/caches/temp/user-data subtrees;
- prototype/production import-boundary rules and baseline hash.

Unknown or floating engine/runtime/dependency/build identity caps executable claims at `BLOCKED` or `INCONCLUSIVE`. Tags such as `latest`, unpinned package ranges, unlocked resolution, mutable URLs, and global user caches are not reproducible identities.

If dependencies are required, use an existing exact lockfile included by hash, or propose creating a prototype-local lockfile after execution approval from an exact dependency manifest and pinned source. Never modify a production lockfile or install globally. Dependency resolution without a stable lock/source receipt is `DEPENDENCY_UNAVAILABLE`; do not claim a reproducible build.

### Isolation and fallback — PROTO-P1-002/003

Preferred isolation is a detached or dedicated approved Git worktree at an exact new path and base commit. Creating/removing it and any Git metadata changes are persistent operations in the execution/cleanup manifests.

Before approval, perform read-only feasibility checks. If the requested worktree is unavailable, present exactly these safe choices and their tradeoffs:

1. `isolated_temp_root` — an exact new temp/sandbox path, an exact source-copy manifest, redirected caches/build outputs, and a declared retain-or-cleanup policy;
2. `current_workspace_bounded_root` — exact new `prototypes/throwaway/<prototype-id>/`, original-worktree dirty-manifest protection, and strict no-outside-root mutation monitoring;
3. `CANCEL` — zero writes.

Never silently fall back. The user must explicitly select the revised isolation mode, and the execution changeset must be regenerated and approved.

For any mode:

- the root must be absent and resolve outside existing user prototype roots;
- every parent path, symlink/junction/reparse point, and filesystem boundary is validated;
- commands run with exact working directory and redirected dependency/cache/temp/output/user-data locations;
- the original worktree dirty manifest is rechecked before and after every command;
- any unexpected original-tree change is `BLOCKED`, is never reverted automatically, and is reported with pre/post hashes and recovery guidance;
- an uncontainable tool is not run.

The user chooses `RETAIN`, `CLEAN_AFTER_RECEIPT`, or `CLEAN_LATER`. Cleanup is never implied by KILL or task completion. `CLEAN_AFTER_RECEIPT` must be an exact destructive operation explicitly included in the execution manifest, may target only the newly created isolation root/worktree, runs only after required receipts/evidence have been preserved at authorized destinations, and emits a cleanup receipt. Otherwise return `cleanup_state: RETAINED | CLEANUP_REQUIRED`. Never delete production or pre-existing user data.

## Phase 2 — Freeze hard execution budget and exact changeset

Default hard ceilings per run:

```yaml
max_implementation_iterations: 3
max_build_commands: 12
max_consecutive_failures: 2
max_elapsed: { concept: 8h, spike: 4h }
max_authored_files: <exact approved manifest count>
max_persistent_bytes: <explicit finite value>
max_dependency_resolutions: 1
max_play_sessions: 3
```

Requested limits may lower but never raise defaults without a new user decision and complete reauthorization before execution begins. Counters increment before a command/iteration/session; deadlines are absolute timestamps. Resume preserves consumed counters and deadline. “Until playable” is forbidden.

When any limit is reached, stop new implementation/build/play calls, retain current authorized evidence, write only already-authorized checkpoint/receipt paths, and return `PARTIAL — BUDGET_EXHAUSTED` or `BLOCKED`. No in-place budget extension.

The read-only execution preview enumerates:

- exact isolation/worktree/temp action and base identity;
- `PROTOTYPE-MANIFEST.yaml`, `CHECKPOINT.yaml`, `RUN-RECEIPT.yaml`, `EVIDENCE.yaml`, `REPORT-DRAFT.md`, and `PUBLICATION-PROPOSAL.yaml`;
- every authored source/config/harness/placeholder/consent-record path;
- prototype-local dependency manifest/lockfile, if applicable;
- exact raw logs and build/play receipts;
- bounded generated `build/`, `runtime-cache/`, package-cache, temp, and user-data subtrees;
- exact commands, dependency sources, toolchain/build identity, environment allowlist, budget, deadline, source/dirty snapshots, production non-writes, privacy plan, retention/cleanup choice;
- publication paths explicitly not authorized.

For each path/subtree show kind, operation, owner, base hash/ABSENT, byte ceiling, and purpose. Ask once for exact execution authorization. Any new path, subtree, dependency, command class, isolation/cleanup action, operation, or raised budget invalidates the approval and requires a new preview.

## Phase 3 — Initialize only after authorization

After approval, revalidate source, toolchain, lock, dirty-worktree, target absence, parent safety, and command identities. On mismatch write nothing and return `BLOCKED — PREFLIGHT_DRIFT`.

Then create the exact isolation/root, boundary manifest, checkpoint, minimum scaffold, and local dependency lock as approved. Every authored source begins with a `PROTOTYPE — NOT FOR PRODUCTION` marker plus prototype/run/hypothesis/root identities.

`PROTOTYPE-MANIFEST.yaml` records allowed authored paths, generated subtrees, imports, source snapshot, dirty-worktree baseline, dependency/toolchain/build identities, privacy rules, budget, and cleanup policy.

`CHECKPOINT.yaml` records prior-checkpoint hash, phase, counters/deadline, command states, written paths/pre/post hashes, builds, play sessions, skip records, consent records, and next safe step. Each update validates its previous hash. Drift stops the run; do not reset.

## Phase 4 — Bounded implementation, build identity, and run receipts

Implement only what is required for the single hypothesis. Before every command/write, verify root/manifest authority, original-worktree baseline, dependency lock/toolchain identity, relevant base hashes, and remaining budget; increment counters first. Afterwards inventory all mutations and rehash source, lockfile, build config, output, logs, checkpoint, and original worktree.

Unexpected or unlisted writes are `BLOCKED`. Never retroactively authorize them or automatically revert user files.

### Build identity — PROTO-P1-002

Derive `source_manifest_sha256` from exact authored source/config/harness paths and hashes. Derive `build_identity_sha256` from the canonical tuple:

```text
(prototype_id, run_id, source_manifest_sha256, dependency_manifest_sha256,
 dependency_lock_sha256, toolchain_manifest_sha256, build_config_sha256,
 exact_command_and_arguments, environment_allowlist_sha256)
```

Every actual build emits `cgs.prototype-build-receipt/v1`:

```yaml
build_id: BUILD-<run-id>-NN
build_identity_sha256: ...
prototype_id: ...
run_id: ...
source_manifest_sha256: ...
dependency_manifest_sha256: ...
dependency_lock_sha256: ...
toolchain_manifest: [{ name: ..., version: ..., path_sha256: ... }]
build_config_sha256: ...
command: { executable: ..., args: [...], working_directory: ... }
environment_allowlist_sha256: ...
started_at: ...
ended_at: ...
exit_code: ...
result: PASS | FAIL | TIMED_OUT | CANCELED | NOT_RUN
artifacts: [{ path: ..., sha256: ..., bytes: ... }]
log: { path: ..., sha256: ... }
generated_manifest_sha256: ...
outside_root_mutations: []
```

PASS requires an actual command, exit code zero, expected current artifacts, matching hashes, and zero unapproved outside-root mutations. Source inspection, a proposed/mock command, cached artifact without identity match, or agent statement cannot substitute.

HTML needs an actual pinned syntax/load check; engine mode must invoke the pinned engine/build/run validation; paper mode may validate artifact structure but that is neither executable build nor human play evidence. If build cannot run, use a typed skip/NOT_RUN and make no playable claim.

Each revision links the build/play failure or threshold it addresses. Stop on threshold, hard failure, or budget exhaustion.

### Immutable run receipt — PROTO-P1-004

Every run maintains `RUN-RECEIPT.yaml` conforming to `cgs.prototype-run-receipt/v1`. It contains:

- prototype/run/hypothesis and optional parent-pivot identities;
- skill-source and mandatory continuation-contract paths/SHA-256 values;
- execution authorization manifest/hash and isolation/cleanup choice;
- source snapshot, dirty-worktree baseline/final, source-manifest, dependency manifest/lock, toolchain, build-config, environment, generated-output, and checkpoint hashes;
- every command ID/exact command/time/exit/result/log hash;
- every build receipt path/hash and build identity;
- every play/observation record path/hash and bound build/source identity;
- every skip record, consent record, redaction receipt, privacy/retention state, and evidence path/hash;
- budget limits/consumption/deadline and final run/build/play status;
- report-draft/publication-proposal hashes and cleanup receipt/state.

The receipt is finalized from exact current bytes at run end and becomes immutable. Debrief facts, recommendations, REPORT, DECISION, prototype index rows, pivot notes, and graveyard events must cite the exact run-receipt path/SHA-256 plus source/build/play hashes. If the receipt is missing, stale, internally inconsistent, or hash-mismatched, no fact may be published as current and the recommendation ceiling is `INCONCLUSIVE`.

## Phase 5 — Typed skips — PROTO-P1-005

Every planned-but-unexecuted or inapplicable step emits `cgs.prototype-skip/v1` with step ID, taxonomy, exact reason, evidence path/hash, actor/source, timestamp, scope, affected hypothesis signal/claim, recommendation ceiling, and recovery condition.

Allowed taxonomy:

- `NOT_APPLICABLE` — a predeclared applicability predicate is false;
- `USER_ACCEPTED_RISK` — the user explicitly accepts a named non-safety risk after seeing consequence/evidence;
- `ENVIRONMENT_BLOCKED` — actual current environment evidence prevents execution;
- `DEPENDENCY_UNAVAILABLE` — pinned dependency/lock/source cannot be resolved safely;
- `BUDGET_EXHAUSTED` — a monotonic limit has been reached;
- `CONSENT_WITHHELD` — required participant consent/data category was not granted or was withdrawn;
- `UNSUPPORTED_MODE` — selected mode cannot establish the requested signal;
- `NOT_REQUESTED` — optional step was outside the approved experiment;
- `FAILED_PRECONDITION` — required hash, identity, boundary, or freshness check failed.

Free-text “skip” is invalid. `NOT_APPLICABLE` requires the exact predicate and evidence. `USER_ACCEPTED_RISK` requires a hash-bound explicit user response and cannot waive containment, privacy, authorization, destructive-action, identity, or evidence-integrity rules. Environment/dependency claims need current receipts. A skip never becomes PASS, MET, OBSERVED, or evidence of absence. Essential build/play/consent skips cap affected recommendations at `INCONCLUSIVE`.

## Phase 6 — Consent-safe play and observation — PROTO-P1-008

Before soliciting or collecting participant feedback, recording, screen/audio/video capture, telemetry, logs tied to a person, direct quotes, or contact identifiers, present a privacy/consent plan:

- experiment purpose and participant type;
- exact data categories and collection methods;
- whether screen/audio/video/telemetry recording occurs;
- storage paths, access/recipients, retention period, and cleanup/deletion owner;
- quote/paraphrase/anonymization policy;
- voluntary nature, ability to decline/withdraw, and consequences of withdrawal;
- known sensitive/secret data exclusions.

Record an explicit consent response per participant/data category in `cgs.prototype-consent/v1`, hash it, and bind evidence to it. Silence is no consent. Consent for feedback is not consent for recording, quoting, publication, or identity disclosure. Do not recruit or record minors/vulnerable participants without an applicable owner-approved policy and required guardian/organizational consent; otherwise use `CONSENT_WITHHELD`.

Do not persist secrets, credentials, access tokens, private keys, or unnecessary direct identifiers. Minimize collection; assign participant IDs; redact/pseudonymize before persistent evidence. Raw unredacted personal/sensitive evidence is quarantined inside an approved restricted in-root path or not written, is never published/indexed, and makes the affected evidence `BLOCKED` until an authorized redaction receipt exists. Do not expose sensitive values in tool output or reports.

Withdrawal stops further collection and marks linked evidence `WITHDRAWN_NOT_USABLE`. Deletion/retention follows the consent plan and requires exact authority; do not silently delete or continue using it.

An actual play/observation record conforms to `cgs.prototype-play-receipt/v1` and contains session/build/run/source identity, participant pseudonymous type/ID, consent record/hash, timing/protocol, observed facts, participant reports, measurements, evidence hashes, redaction state, and hypothesis signal. Separate `OBSERVED_FACT`, `PARTICIPANT_REPORT`, `MODEL_INFERENCE`, and `NOT_OBSERVED`. Never invent a participant, action, quote, timestamp, metric, recording, or result.

No real play yields `PLAY_NOT_RUN` plus a typed skip. A model/paper simulation is `MODEL_SIMULATION` and cannot support human behavior, first-impression, fun, or feel claims. Rehash build/source after capture; stale evidence cannot support a changed build.

## Required continuation

Before producing the final advisory recommendation, pivot lineage, user decision, design-route advice, publication proposal, or cleanup result, revalidate the previewed SHA-256 and read [references/continued-workflow.md](references/continued-workflow.md) completely. That reference is a hash-bound part of this skill contract. Drift returns `BLOCKED` and requires a new preview; never continue under mixed contract versions.

## Resume and interruption

Resume only when execution manifest, checkpoint chain, run receipt, source/lock/toolchain/build/evidence/consent hashes, dirty-worktree baseline, budget counters/deadline, root, and optional parent pivot all match. Completed commands are not rerun unless explicitly allowed by remaining budget.

Drift, an exhausted budget, outside mutation, stale consent, or stale pivot lineage returns `BLOCKED`/`PARTIAL`. Resume inherits neither publication nor downstream authority.
