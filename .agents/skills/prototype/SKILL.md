---
name: prototype
description: "Run one bounded throwaway experiment inside an isolated prototype root. Requires explicit write authorization before checkpoint/code/assets, records real build and play evidence, emits advisory recommendations only, and keeps downstream product decisions and publication separately authorized."
---

## Invocation and execution

Invoke:

```text
$prototype <concept-or-question> [--path html|engine|paper] [--spike]
```

A concept or concrete experimental question is required. If it is missing, show
usage and stop without reading project files, spawning agents, or writing.

Delegate implementation to `prototyper` when available. The orchestrator retains
responsibility for authorization, budget enforcement, evidence classification,
and the separation between recommendation and user decision.

# Prototype

This workflow runs one disposable experiment. It is not a design approval,
production implementation, phase gate, or product portfolio authority.

It has two independently authorized mutation boundaries:

1. **Execution changeset** — throwaway prototype code/assets, local checkpoint,
   build outputs, and raw evidence inside one isolated root.
2. **Publication changeset** — report, project index, and any user-selected
   decision record after evidence exists.

Authorization for one boundary never authorizes the other or any downstream
workflow.

## Non-negotiable invariants

- Before execution changeset approval: **zero persistent writes**, including no
  checkpoint, worktree, directory, dependency install, generated project, or
  evidence file.
- All experiment mutations stay under one approved
  `prototypes/throwaway/<prototype-id>/` root or an explicitly approved isolated
  worktree containing that same project-relative root.
- Prototype code/assets never write to or become imports of `src/`, `assets/`,
  production tests, design, docs, or production state.
- Build/play claims require actual current-run evidence. File existence, source
  inspection, a proposed command, a model simulation, or user intent is not proof
  that a prototype built or was played.
- The workflow may write `RECOMMENDATION: PROCEED/PIVOT/KILL/INCONCLUSIVE`. It
  may not write a final product decision without the user's explicit selection.
- `PROCEED` means only "the evidence supports further user-directed discovery or
  design." It does not approve a concept, GDD, architecture, asset production,
  sprint work, or production code.
- Every loop has a hard, monotonic budget and must terminate.
- Report, index, and user decision publish together or remain non-authoritative.

---

## Phase 0: Read-only experiment definition

Do not mutate files or create an isolated worktree in this phase.

Ask the user to define one falsifiable hypothesis:

> "If the participant does X under condition Y, observable signal Z will meet
> threshold T."

Record:

- one hypothesis ID;
- riskiest assumption;
- one mechanic/question;
- measurable success/failure/inconclusive criteria;
- observations that the chosen mode cannot establish;
- explicitly excluded scope.

Reject `is it fun?` or other unfalsifiable wording. Narrow the experiment before
continuing.

Read only the minimum project context needed to select an engine/mode and avoid
known conflicts. Existing project concepts, GDDs, source, and assets are context,
not write authorization.

### Choose evidence-appropriate path

- `html` — browser logic/clarity experiments; do not use browser-only evidence to
  validate timing-sensitive native feel.
- `engine` — native timing/physics/rendering experiments.
- `paper` — rules/decision experiments; cannot validate moment-to-moment digital
  feel.
- `spike` — technical feasibility question; does not make a product decision.

Do not state unsupported success percentages for any path.

---

## Phase 1: Allocate isolated throwaway identity

Create in memory:

```yaml
prototype_id: PT-<slug>-<run-id>
hypothesis_id: HYP-<run-id>-001
mode: html | engine | paper | spike
throwaway_root: prototypes/throwaway/<prototype_id>/
isolation: requested_worktree | current_workspace_bounded_root
source_snapshot:
  paths_and_sha256: [...]
```

Preferred isolation is an explicit isolated Git worktree. Creating it is a
persistent side effect and belongs to the execution changeset. If an isolated
worktree is unavailable, do not silently fall back: offer the current-workspace
throwaway root as a bounded alternative and obtain its explicit approval.

The throwaway root must be new and absent. Never overwrite, replace, extend,
archive, or delete an existing prototype under the current run's authorization.
Resume requires the matching checkpoint and hashes. A new experiment receives a
new prototype ID/root.

### Boundary contract

Every authored file path is exact. The execution preview also identifies bounded
tool-generated subtrees such as `runtime-cache/` and `build/` whose filenames are
controlled by the engine/build tool. Those subtrees:

- must be descendants of the approved throwaway root;
- may contain only ephemeral generated output;
- cannot contain authoritative reports or project state;
- are inventoried and hashed after every command; and
- never broaden writes outside the root.

All build/dependency commands set working directory, cache, temp, output, and
user-data locations inside the isolated environment. If a tool cannot be
contained, do not run it.

No prototype source may import, link, load, or write production source/assets.
Production code/assets must not import or load the prototype root. Validate both
directions before and after execution.

---

## Phase 2: Freeze hard execution budget

Present a finite budget before authorization. Defaults:

```yaml
budget:
  max_implementation_iterations: 3
  max_build_commands: 12
  max_consecutive_failures: 2
  max_elapsed:
    concept: 8h
    spike: 4h
  max_authored_files: <exact manifest count>
  max_persistent_bytes: <declared bound>
```

The budget is monotonic and stored in the checkpoint after approval. Each command
or iteration increments its counter before execution. Deadline uses an absolute
timestamp.

When any limit is reached:

1. stop all further implementation/build tool calls;
2. capture current evidence and unresolved errors;
3. write only already-authorized checkpoint/evidence paths;
4. return `PARTIAL — BUDGET EXHAUSTED` or `BLOCKED`;
5. do not increase the budget in-place.

Further work requires a new user decision, new budget, and separately authorized
run or revised execution changeset. "Until playable" is forbidden.

---

## Phase 3: Preview and authorize the execution changeset

The plan remains read-only. Synthesize every expected authored path, including:

- `PROTOTYPE-MANIFEST.yaml`;
- `CHECKPOINT.yaml`;
- exact prototype source/config files;
- exact placeholder assets;
- exact test/harness files;
- `EVIDENCE.yaml`;
- `REPORT-DRAFT.md` and `PUBLICATION-PROPOSAL.yaml`, both explicitly non-authoritative;
- exact raw log destinations when known;
- bounded ephemeral `build/` and `runtime-cache/` subtrees.

Preview:

```markdown
| Path/subtree | Kind | Operation | Owner | Base SHA-256/ABSENT | Purpose |
|---|---|---|---|---|---|
```

Also show:

- isolation/worktree action;
- hypothesis and success criteria;
- budget and deadline;
- exact commands planned;
- expected environment/dependency versions;
- excluded project paths;
- cleanup/retention choice;
- publication paths explicitly **not authorized**.

Ask once for approval of this exact execution changeset. An existing bounded task
authorization counts only if it names the same root, actions, paths/subtrees,
owners, and operations.

If the plan later needs a new authored path, subtree, dependency, worktree action,
or operation, stop before writing and request a revised execution changeset.
Code/asset authorization never implies report/index/decision or downstream
workflow authorization.

---

## Phase 4: Initialize after approval

Only after approval:

1. verify every authored target is ABSENT or matches its approved base hash;
2. create the isolated worktree/root;
3. create the boundary manifest and checkpoint;
4. write the minimum scaffold;
5. inventory the root and verify no outside path changed.

Every source file begins with the language-appropriate equivalent of:

```text
PROTOTYPE — NOT FOR PRODUCTION
Prototype ID: <id>
Hypothesis ID: <id>
Throwaway root: <path>
```

The manifest records allowed authored paths, generated subtrees, source snapshot,
dependencies, budget, and the prohibition on production imports.

The checkpoint records:

```yaml
prototype_id: ...
hypothesis_id: ...
phase: ...
root: ...
manifest_sha256: ...
source_hashes: ...
budget:
  limits: ...
  consumed: ...
  deadline: ...
commands:
  - id: ...
    status: PLANNED | RUNNING | COMPLETE | FAILED | TIMED_OUT | CANCELED
written_paths:
  - { path: ..., pre_sha256: ..., post_sha256: ... }
builds: []
play_sessions: []
next_safe_step: ...
```

Each checkpoint update verifies its previous hash. An unexplained hash change
stops the run.

---

## Phase 5: Bounded implementation and build

Implement only the minimum needed for the single hypothesis. Relaxed code quality
does not relax containment, authorization, dependency, privacy, or evidence
rules.

Before every write or command:

- re-check root containment and manifest authority;
- re-check relevant base hashes;
- increment the corresponding budget counter;
- record command ID and start state in the checkpoint.

After every write or command:

- inventory all root mutations;
- reject any outside/unlisted authored mutation;
- hash source, build output, logs, and checkpoint;
- record exit code and elapsed time;
- stop on budget limits.

A command that writes outside the isolated environment is canceled/blocked.
Unexpected outside mutations are BLOCKED and are never retroactively authorized.

### Build evidence

A build exists only when an actual command ran. Record:

```yaml
build_id: BUILD-...
prototype_id: ...
source_manifest_sha256: ...
command: ...
working_directory: ...
environment:
  os: ...
  engine_or_runtime: ...
  version: ...
started_at: ...
ended_at: ...
exit_code: ...
result: PASS | FAIL | TIMED_OUT | NOT_RUN
artifact_paths_and_sha256: [...]
log_path_and_sha256: ...
```

`PASS` requires exit code zero and the expected current artifacts. Source
inspection or an agent statement cannot replace it.

HTML must receive an actual syntax/load check; engine mode must invoke the pinned
engine/build/run validation appropriate to the scaffold; paper mode may validate
document structure but this is not play evidence.

If no build command can run, record `BUILD NOT RUN` and do not claim a playable
prototype.

### Iteration

Use at most the approved iterations and commands. Each revision states which
observed build/play failure it targets. Do not add polish or new mechanics.
Terminate on success criteria, hard failure, or budget exhaustion—whichever
occurs first.

---

## Phase 6: Real play/observation evidence

Do not claim playability from a successful build alone.

A play session requires an actual user/tester action. Capture:

```yaml
session_id: PLAY-...
build_id: ...
participant_type: user | external_tester | self_test | wizard_of_oz
consent_and_redaction: ...
started_at: ...
ended_at: ...
protocol: ...
observations:
  - timestamp_or_step: ...
    fact: ...
measurements: [...]
participant_quotes_or_paraphrases: [...]
hypothesis_signal: MET | NOT_MET | MIXED | NOT_OBSERVED
evidence_paths_and_sha256: [...]
```

Distinguish:

- `OBSERVED FACT` — directly seen/measured;
- `PARTICIPANT REPORT` — what a person reports;
- `MODEL INFERENCE` — interpretation;
- `NOT OBSERVED` — no valid evidence.

Do not invent participants, actions, quotes, timestamps, metrics, recordings, or
results. A model-written paper simulation is labeled `MODEL_SIMULATION` and
cannot count as human play or first-impression evidence.

If no real play occurs, record `PLAY NOT RUN`. The evidence may support technical
feasibility, but not player-feel or fun claims.

Collect only data the participant consented to share. Redact secrets and personal
information before persistent evidence. Unredacted sensitive evidence is BLOCKED.

After evidence capture, re-hash the build/source manifest. Stale play evidence
cannot support a changed build.

---

## Required continuation

Before report/recommendation/publication, read
[references/continued-workflow.md](references/continued-workflow.md) in full and
follow its evidence, user-decision, and atomic-publication rules.

## Resume safety

Resume only when checkpoint, manifest, source, budget, build, and evidence hashes
match current bytes. Never reset counters or deadline. Completed commands are not
re-run unless a new iteration is explicitly within the remaining budget.

A stale checkpoint, changed root, outside mutation, or exhausted budget returns
BLOCKED/PARTIAL. Resume never inherits authorization for publication or any
downstream workflow.
