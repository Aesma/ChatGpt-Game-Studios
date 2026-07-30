---
name: team-polish
description: "Assesses and hardens one revision-bound feature through bounded role/context contracts, approved path-owned patches, single-owner integration, fixed-matrix final-build evidence, deterministic readiness, and resumable receipts."
---

# Team Polish

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

This workflow separates assessment, implementation, integration, and verification.
A performance observation, proposal, file-write approval, or readiness verdict is not
permission to implement, commit, push, deploy, publish, or communicate externally.

## Versioned protocol records

This workflow accepts only the named schema/version, canonical path, and raw-byte
revision for each record:

- `cgs.polish-target-manifest/v2`
- `cgs.polish-context-manifest/v1`
- `cgs.polish-assessment/v2`
- `cgs.polish-mutation-manifest/v2`
- `cgs.polish-agent-task/v1` and `cgs.polish-agent-result/v1`
- `cgs.polish-profile-request/v1` and `cgs.polish-profile-receipt/v1`
- `cgs.polish-test-matrix/v1` and `cgs.polish-execution-receipt/v1`
- `cgs.polish-run-manifest/v1`, `cgs.polish-checkpoint/v1`, and
  `cgs.polish-verification-report/v2`

Unknown versions, duplicate identities, ambiguous paths, malformed fields, or
recorded/current revision mismatches are blocking. Do not coerce a legacy/free-text
artifact into one of these contracts.

## Invocation

Accept exactly one mode:

~~~text
$team-polish assess --manifest {polish-target-manifest-path} --assessment-id {stable-id} [--persist]
$team-polish implement --assessment {assessment-path} --mutation-manifest {manifest-path} --implementation-id {stable-id}
$team-polish verify --candidate-manifest {candidate-path} --verification-id {stable-id} [--persist]
$team-polish resume --checkpoint {checkpoint-path}
~~~

Reject unknown or duplicate flags, missing values, directories, unsafe paths, and
positional feature names. IDs are stable slugs or UUIDs, not timestamps alone. Never
infer a target, newest build, latest assessment, hardware, budget, requirement,
mutation set, checkpoint, or evidence file. With no mode or required argument, print
the accepted forms and exit without spawning agents or writing files.

`--review`, `full`, `lean`, `solo`, and generic director/lead skip flags are
not accepted modes. Actual participation is resolved from the required-role matrix
and exact target policy below; presentation mode never changes evidence obligations.

One invocation stops at its mode boundary. `assess` never falls through to
implementation. `implement` never issues release authority or performs publication.
`verify` never fixes a failure automatically.

## Authority and mutation boundary

Use independent authority layers:

1. **Read-only assessment** may read, revision, profile, and inspect only declared inputs.
2. **Assessment persistence** may create only the previewed assessment, proposal,
   path-owner, and checkpoint files.
3. **Product implementation** may change only exact paths and operations in one
   immutable mutation manifest after explicit authorization of the complete set.
4. **Build/test outputs** may create only exact artifact, cache, log, receipt, and
   verification paths named by the authorized manifest.
5. **Repository/external actions** — branch, commit, tag, push, release object,
   upload, deploy, store submission, public or stakeholder message, and publication
   are outside this workflow and require separate authority elsewhere.

Approval at one layer never carries to another layer, another manifest revision, a new
path, changed operation, destructive action, build target, external action, or retry.
One prompt may authorize product paths and build/test outputs together only when it
labels both layers and enumerates every operation explicitly; neither layer is implied.
A phase-transition choice is not product-write approval. A `READY FOR RELEASE`
verdict is evidence only; it grants no release, deployment, or publication authority.

A bounded user request may already authorize exact files and operations. Otherwise,
immediately before implementation, display one complete changeset with every CREATE,
MODIFY, DELETE, MOVE, generated output, test artifact, and expected side effect, then
obtain one explicit approval. Do not ask again per file inside that unchanged
boundary. Any new or changed path, generated output, binary asset, config effect, or
destructive operation stops the run and requires a new assessment and authorization.
No implementation agent may be spawned and no product byte may change before this
boundary is satisfied.

## Canonical immutable artifacts

Use:

~~~text
production/polish/{target-id}/assessments/{assessment-id}/assessment.md
production/polish/{target-id}/assessments/{assessment-id}/mutation-manifest.yaml
production/polish/{target-id}/implementations/{implementation-id}/run-manifest.md
production/polish/{target-id}/implementations/{implementation-id}/checkpoints/{checkpoint-id}.md
production/polish/{target-id}/implementations/{implementation-id}/candidate/build-candidate.yaml
production/polish/{target-id}/implementations/{implementation-id}/verification/{verification-id}/report.md
~~~

Never overwrite a prior artifact or select one by modification time. An existing
target is a collision and blocks. Persisted artifacts use atomic create, read-back,
internal-reference validation, and full revision reporting.


## Unique writer ledger

The persisted writer ledger assigns exactly one role to every output path:

| Output class | Unique writer |
|---|---|
| assessment aggregate, mutation manifest, run manifest, checkpoints and final aggregate report | team-polish controller |
| performance measurement receipts | performance-analyst |
| visual/audio/tools/engine assessment receipts | the named read-only assessor |
| approved disjoint product paths and patch receipt | mutation-manifest patch owner |
| shared scenes/config/resources/registries and integration receipt | manifest-named integrator |
| final build outputs, build receipt and build-candidate manifest | manifest-named build owner |
| regression/edge/stress/soak execution receipts | qa-tester |
| final accessibility review receipt | accessibility-specialist |

No delegate may write a controller, integrator, build-owner, or other delegate path.
If an owner is unavailable, the output remains missing/unknown; ownership is not
silently transferred. Generated outputs inherit the declared writer and count in
overlap checks.

### Required-role matrix

The target manifest and current policy classify each row as `REQUIRED`,
`CONDITIONAL`, or `NOT_APPLICABLE` before assessment. Missing or ambiguous
classification is blocking.

| Role | Trigger | Required output |
|---|---|---|
| performance-analyst | any performance, memory, loading, streaming, or audio budget row | read-only profile receipt and stable findings |
| qa-tester | every target | assessment coverage receipt and final fixed-matrix execution receipts |
| accessibility-specialist | every target with visual, motion, input-feedback, audio-cue, or settings impact | read-only assessment plus independent final-candidate review |
| technical-artist | render, VFX, shader, material, camera, scalability, or visual-readability scope | read-only assessment receipt |
| sound-designer | audio source/event/bus/mix/spatialization/streaming scope | read-only assessment receipt |
| tools-programmer | content-authoring, import/export, editor, build-tool, or automation scope | read-only tools-impact receipt and, if later authorized, an owned patch receipt |
| engine-programmer | trace-backed engine-boundary finding meets the policy confidence threshold | read-only diagnosis and, if later authorized, an owned patch receipt |

There is no ceremonial director/lead gate. Every `REQUIRED` row must produce a
current `Agent Status: PASS` receipt. `FAIL` maps to a conclusive blocker;
`UNKNOWN`, `TIMEOUT`, `ERROR`, `CANCELLED`, or skip maps to
`Workflow Status: PARTIAL` and `Readiness Verdict: INCOMPLETE`. A skipped row
is nonblocking only when the pre-run policy marks it `NOT_APPLICABLE` and records
the rule ID, reason, owner, policy path/revision, and affected scope. Conversation or
review mode cannot reclassify a row.

## Status and verdict vocabulary

Report independent fields:

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` |
| `Finding Status` | `OPEN`, `PATCHED`, `VERIFIED`, `FAILED`, `DEFERRED`, `UNKNOWN` |
| `Agent Status` | `PASS`, `FAIL`, `UNKNOWN`, `TIMEOUT`, `ERROR`, `CANCELLED` |
| `Evidence State` | `CURRENT`, `STALE`, `MISSING`, `NOT_RUN`, `PARTIAL`, `INVALID`, `UNAVAILABLE` |
| `Implementation State` | `NOT_AUTHORIZED`, `AUTHORIZED`, `IN_PROGRESS`, `INTEGRATING`, `BUILT`, `BLOCKED`, `CANCELLED`, `COMPLETE` |
| `Readiness Verdict` | `READY FOR RELEASE`, `NEEDS MORE WORK`, `INCOMPLETE`, `ERROR` |
| `Release Authorization` | always `NOT GRANTED` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

`COMPLETE` describes workflow execution, not release readiness. `READY FOR RELEASE`
is allowed only for one immutable final candidate revision with all required current
evidence. `NOT_RUN`, `PARTIAL`, `UNKNOWN`, `TIMEOUT`, stale evidence, or missing
required hardware can never be converted into PASS by prose or user optimism.

## Phase 0: Validate one target and baseline

Resolve literal and real paths. Reject dot segments, symlink escapes, malformed or
duplicate keys, unsupported schemas, paths outside the project root, and unbounded
directory scans. Read raw bytes once and record full explicit revision identifiers.

The polish target manifest must contain:

- `Artifact Type: polish-target-manifest`, schema version, stable target ID, product
  ID, target feature/area IDs, and exact in-scope/excluded roots;
- baseline build-candidate manifest path/revision, candidate/build IDs, artifact path/revision,
  source commit, engine/toolchain version, platform/configuration matrix, and dirty
  workspace state;
- exact performance-budget policy path/revision with target hardware profiles, frame/CPU/
  GPU/memory/loading/streaming/audio thresholds and required sample rules;
- exact design, art, audio, UX, and accessibility requirement paths/revisions applicable
  to the target;
- exact QA plan/test manifest paths/revisions, required regression/soak/stress matrix,
  seeds/workloads/durations, and hardware/environment inventory;
- exact context-manifest path/revision and exact fixed test-matrix path/revision;
- known-issue registry path/revision and canonical severity/blocker mapping;
- declared profiling/test commands or approved runner receipts;
- input file/byte limits, context budget, generated-output roots, report root, owner,
  generated-at timestamp, and applicable AGENTS.md path/revision chain.

revalidate the baseline candidate manifest and local artifact. A remote build requires a
trusted build receipt binding the same identity, artifact identifier, source commit,
platform/configuration, toolchain, issuer/job, timestamps, logs, and signature or
verification method.

A missing or ambiguous target, stale baseline, dirty unrecorded source, missing
budget, absent required requirements, revision mismatch, or unsupported platform yields
`Workflow Status: BLOCKED`, `Implementation State: NOT_AUTHORIZED`, no delegation,
and no writes.

### Bounded context contract

`cgs.polish-context-manifest/v1` is the only delegation context authority. It
contains target/baseline IDs and revisions, policy revision, deterministic role-specific
entries with normalized path/revision/byte length/purpose/required flag, and positive
integer `max_files`, `max_total_bytes`, and `max_single_file_bytes` ceilings.
Entries are ordered by required flag, artifact class, stable ID, then normalized
path. The controller validates sizes before reading bodies and records one context
identifier per agent task.

Never send the repository, a directory tree, unrestricted full context, inferred
related files, or conversation-only evidence. A missing required entry, revision drift,
file-count/byte overflow, unreadable file, or inability to honor a ceiling blocks
that task before delegation; do not truncate silently or substitute an unbound
summary.

## Phase 1: Read-only multidisciplinary assessment

All assessment delegates are read-only. Prompts explicitly prohibit product/source/
asset/config/test mutation and name only the relevant target IDs, budgets, baseline
identity, exact input paths/revisions, byte limits, expected receipt schema, and
deadline. Do not send unrestricted “full context”.

Dispatch as applicable:

- `performance-analyst`: measure and diagnose only; never fixes code. Produce stable
  performance findings with metrics, trace path/revision, suspected module/path,
  confidence, budget gap, reproduction command, hardware, and proposed owner.
- `technical-artist`: inspect existing VFX, shader, material, render settings, camera,
  and scalability behavior; propose changes without editing.
- `sound-designer`: inspect event coverage, mix, spatialization, streaming, dynamics,
  and accessibility interactions; propose changes without editing.
- `qa-tester`: identify regression, edge, soak, stress, and minimum-spec coverage
  required for every proposal; assessment does not claim tests ran unless a receipt
  proves it.
- `accessibility-specialist`: review motion, camera shake, flashes, contrast/readability,
  audio-only cues, input/aim clarity, intensity controls, and functional alternatives.
- `tools-programmer`: inspect only when the manifest shows content-authoring,
  import/export, editor, build-tool, or automation involvement.
- `engine-programmer`: read-only diagnosis only when a performance finding includes a
  profiler trace revision, engine module/path, boundary justification, and confidence
  meeting the policy threshold.

No implementation writer runs in this phase. An unavailable tool, runner, target
hardware, or delegate is visible as `NOT_RUN`, `UNAVAILABLE`, `TIMEOUT`, or
`UNKNOWN`; do not synthesize results.

### Performance capture interface

Do not invoke `$perf-profile` as a nested workflow. The performance analyst performs
the equivalent bounded read-only responsibility through one
`cgs.polish-profile-request/v1` that binds request/target/baseline candidate and
artifact IDs/revisions, budget and context-manifest revisions, exact platform/hardware,
tool/version, executable/argv/cwd, warm-up, duration, samples, workload/seed,
timeout, output paths, deadline, and producer.

The only accepted result is an immutable `cgs.polish-profile-receipt/v1` at the
request-declared path. It repeats all subject identities, records start/end,
termination/exit/result, metric units and percentiles, raw trace/log paths/revisions,
omissions, findings, and producer identity. A compatible receipt produced elsewhere
may be consumed only when its schema, request, candidate, hardware, command, and raw
revisions all match. Unsupported runner/tool/interface, missing receipt, timeout, or
revision mismatch is `NOT_RUN` or `INVALID` and cannot be replaced by a nested call
or prose summary.

### Bounded concurrency

Read `.codex/config.toml` and use its `max_threads`. The root orchestrator counts as
one live thread. Before each batch enumerate all live agents and compute:

~~~text
available_child_slots = max(0, max_threads - live_threads_including_orchestrator)
~~~

With this repository's `max_threads = 6` and only the root active, at most five child
agents may run. If configuration is absent or invalid, run serially. Count nested
delegation against the same cap; delegates may not spawn children without an assigned
nested slot. Dispatch only independent read-only assessments in a bounded batch,
gather all results, then release slots.

## Phase 2: Stable findings and complete mutation manifest

Normalize every result into a stable finding ID. Record category, source receipt
path/revision, baseline candidate/build/artifact/source/platform identity, measured
actual/budget, severity, confidence, affected requirements, proposed change, risks,
test impact, and status. Preserve failed, unavailable, and unknown findings rather
than omitting them.

The proposed immutable mutation manifest must enumerate every real side effect,
including:

- game and engine source code;
- scenes, prefabs, levels, resource graphs, serialized objects, and generated scenes;
- render settings, project configuration, streaming/resource-loading configuration;
- shaders, materials, textures, meshes, particles, VFX graphs and caches;
- audio source files, banks, events, buses, mixers, spatialization and streaming data;
- camera, screen shake, input-feedback and gameplay-readability settings;
- content/editor/build tools and automation;
- tests, fixtures, manifests, build artifacts, caches, logs, reports, receipts, and
  checkpoints.

For every operation require stable patch ID and finding IDs, literal/real path,
CREATE/MODIFY/DELETE/MOVE operation, raw baseline revision or explicit ABSENT state,
expected output type, unique writer role, dependencies, shared-resource group,
integrator when shared, generated outputs, validation commands, rollback/recovery
method, and rationale. DELETE/MOVE or an irreversible conversion is destructive and
requires separately explicit authorization.

Generate a case-folded canonical path inventory. Treat identical paths, symlink
aliases, generated outputs, and ancestor/descendant write scopes as overlapping.
Only non-overlapping write domains may be parallel. Every shared scene, prefab,
resource graph, render/project setting, event registry, mixer, manifest, or generated
bundle has one unique integrator. Other roles may write isolated proposal/patch
fragments only; they never edit that shared resource.

The assessment report and mutation manifest are proposals. If persisted, preview
their exact CREATE paths/bytes and obtain assessment-persistence authority; that does
not authorize any proposed product mutation.

## Phase 3: Design and accessibility gate before authorization

A technical artist, sound designer, programmer, or orchestrator may not invent new
gameplay-affecting polish.

A new or materially changed screen shake, camera motion, flash, strobe, vibration,
visual obstruction, audio-only cue, aim/input feedback, or intensity curve requires
a current approved design/UX requirement artifact binding the target, behavior,
maximum/default intensity, player control, platform scope, and exact reviewed
assets/config revisions. Missing or proposed requirements block that mutation; this
workflow does not approve design.

The mutation manifest must require:

- reduced-motion behavior and a user-facing disable/reduction control where motion is
  present;
- policy-defined intensity limits and safe defaults;
- measured flash frequency/luminance/area evidence against the exact accessibility
  policy threshold; if no threshold exists, evidence is `UNKNOWN`;
- functional-equivalent non-motion/non-flash/non-audio-only feedback;
- preservation of aiming, input timing, HUD/world readability, and critical cues;
- correct persistence and application of accessibility settings on every target
  platform/configuration;
- an independent final-build accessibility review by `accessibility-specialist`.

The accessibility specialist is a reviewer, not the writer of the effect. A design
approval does not replace final accessibility evidence, and an accessibility review
does not approve the design.

## Phase 4: Approve and execute path-owned patches

`implement` must revalidate the assessment, mutation manifest, baseline candidate,
requirements, policy, instructions, and every declared base path immediately before
presenting the changeset. Any drift invalidates the manifest.

After exact product-write authorization, create a run manifest and writer ledger.
The performance analyst remains a measurement owner, never a code writer. Assign
implementation to the domain owner named by the manifest, such as
`gameplay-programmer`, `engine-programmer`, `technical-artist`, `sound-designer`, or
`tools-programmer`.

Before every writer starts:

1. confirm its child slot and unique output paths;
2. confirm all path base revisions still match the mutation manifest;
3. provide only exact inputs/findings/requirements and a deadline;
4. prohibit edits outside its owned paths and prohibit commit/push/deploy/publish;
5. Record the patch ID and checkpoint predecessor.

Run only disjoint path owners in parallel. A writer returns a structured patch
receipt containing patch/finding IDs, owner, base and resulting revisions, exact changed
paths, commands/tools, timestamps, result, validation evidence, omissions, and
unexpected writes. Re-scan the declared inventory after each batch. Any unlisted path,
revision drift, overlapping write, failed validation, or owner violation blocks
integration. Do not silently revert or absorb it.

### Shared-resource integration

One manifest-named integrator applies shared changes sequentially after all input
patch receipts are complete. For each shared file, revalidate the current base, apply
one ordered patch, validate, record the new revision, then use that revision as the next
base. Contributors never write the shared file. The integrator owns the integration
receipt and is the only writer of shared resources and the candidate integration
manifest.

A merge conflict, base mismatch, partial input, or failed intermediate validation
stops integration. User approval of the mutation manifest permits only its exact
resolved behavior; conflict resolution that changes behavior or path scope needs a
revised manifest and new authorization.

## Phase 5: Timeout, cancellation, checkpoint, and resume

Every delegate consumes a create-only `cgs.polish-agent-task/v1` with stable
task/attempt ID, role, required-role row, context identifier, exact read/write paths,
expected result path/schema, deadline, timeout, cancel owner, and predecessor
checkpoint revision. It returns one immutable `cgs.polish-agent-result/v1` with the
same bindings, start/end timestamps, terminal status, output revisions, omissions,
unexpected writes, and producer identity.

Every delegation has a deadline, attempt number, one policy-bounded retry maximum,
and explicit cancel owner. On timeout:

1. mark the agent `TIMEOUT` and the patch/finding `UNKNOWN`;
2. cancel or interrupt the writer and wait for confirmed termination;
3. stop dependent dispatch and integration;
4. inventory and revision all owned and shared paths;
5. quarantine any late or partial output from integration;
6. write an immutable checkpoint and partial report.

Never reassign the same paths while the prior writer may still be active. Retry only
after termination and filesystem reconciliation prove a stable declared base. A retry
uses a new attempt ID, the same approved patch scope, and no broader permission. An
unknown late write, client interruption, or cancellation failure remains `BLOCKED`.

Write immutable checkpoints after assessment, authorization, every patch batch,
shared integration, candidate build, and verification. Each checkpoint contains
workflow/implementation state, predecessor path/revision, target and baseline identity,
mutation-manifest revision, authorization record revision, writer ledger, patch receipts,
current path revisions, build identity if available, agent attempts/status/deadlines,
evidence inventory, unresolved findings, and next permitted action.

Each checkpoint conforms to `cgs.polish-checkpoint/v1`, has one stable checkpoint
ID and create-only canonical path, and records completed step IDs, retry budget
consumed, quarantined-output revisions, context/test-matrix revisions, and the exact next
legal idempotent step. A path collision, forked predecessor, duplicate completion,
or missing terminal agent result is blocking. One policy-bounded retry means at
most one new attempt after the original attempt; no recursive or unbounded retry.

Retry count is at most one new attempt after the original attempt. Each checkpoint
records the next legal idempotent step.

`resume` revalidate the entire checkpoint chain, manifests, instructions, owned/shared
paths, and external build receipts. Continue only from the first incomplete
idempotent step. Any unexplained drift, active stale writer, altered authorization,
or missing predecessor blocks; never replay a completed patch or build based on
conversation memory.

Resume must never replay a completed patch, integration, build, or verification
step.

## Phase 6: Integrate and build the final candidate

After every authorized patch and shared integration receipt succeeds, the unique
build owner creates the exact manifest-declared build outputs. revalidate source,
integrated assets/config, tests, toolchain/container/configuration, and generated
inputs immediately before build.

The immutable final `build-candidate` must include:

- schema/type, target/assessment/implementation IDs;
- candidate ID, build ID, artifact path and revision, source commit or recorded
  workspace snapshot identifier, engine/toolchain/container/configuration revisions;
- platform/configuration matrix and target hardware profiles;
- baseline candidate/artifact revisions;
- mutation-manifest, authorization, writer-ledger, patch-receipt and integration-
  receipt paths/revisions;
- design/UX/accessibility requirement paths/revisions;
- QA plan/test manifest and budget-policy paths/revisions;
- reproducible build command/argv, runner/job, start/end timestamps, exit status,
  complete log revision, SBOM/signature/provenance where policy requires them;
- generated-output inventory and manifest owner.

A build failure, partial platform matrix, mismatched source, missing patch receipt, or
unrecorded generated input blocks verification. Any product/asset/config/test byte
change after the build creates a new candidate and invalidates all evidence.

## Phase 7: Re-measure and harden the same final build

`verify` accepts only the exact final candidate manifest. It may not use Phase 1
baseline measurements or per-patch profiler claims as final evidence. revalidate the
candidate, artifact, transitive manifests, requirements, budgets, QA plan, tests,
patch/integration receipts, and applicable instructions before dispatch.

Require the exact immutable `cgs.polish-test-matrix/v1` already captured by the
target, assessment, mutation, run, and candidate manifests. Each stable matrix row
contains category, required/optional classification from current policy, candidate
platform/configuration and hardware profile, executable/argv/cwd, tool/version,
environment revision, warm-up, duration, sample count, seed/workload, timeout, expected
output path, receipt schema, pass predicate, metric units, budget rule ID, and
evidence owner. Verify may neither add, drop, weaken, nor reclassify a row.

Run the policy-required matrix on the final artifact revision and target hardware/
environment:

- unified CPU/GPU/frame-time and frame-pacing profile;
- memory peak/growth/leak and allocation profile;
- loading, streaming, shader/asset warm-up and transition measurements;
- audio CPU/voice/streaming/latency/dropout/peak/mix measurements;
- functional regression, edge, stress, soak and minimum-spec tests;
- visual/scalability/readability review;
- independent accessibility review including reduced-motion, flash thresholds,
  intensity controls, settings persistence, and equivalent feedback.

Every execution receipt conforms to `cgs.polish-execution-receipt/v1` and requires
matrix/row ID and revision, artifact/candidate/build/source/platform/hardware identity,
command/argv and tool/version, configuration/environment revision, seed/workload,
warm-up and measurement duration, sample counts, start/end timestamps, termination,
exit/result status, metric units/percentiles, budget path/revision/rule and threshold
comparison, raw trace/log/capture paths and revisions, omissions, and producer identity.
The receipt path is the matrix-declared create-only destination.

A plan, assertion, filename, local checkbox, conversation statement, Phase 1 report,
or receipt for a different build cannot prove a final result. If required hardware or
runner is unavailable, record `NOT_RUN` or `UNAVAILABLE`; never substitute a less
strict platform unless policy explicitly authorizes it with current evidence.

QA runs only after final profiling evidence exists so it tests the same integrated
candidate and can include performance/accessibility findings. If policy permits
independent final-build measurements to run concurrently, their output paths must be
disjoint and the concurrency cap still applies. Final aggregation waits for all
required receipts.

A required matrix row with no valid current receipt is `NOT_RUN`, `PARTIAL`,
`UNKNOWN`, `TIMEOUT`, `INVALID`, or `UNAVAILABLE` as evidenced; all map to
`INCOMPLETE`. Only a row classified optional by the pre-run policy may remain
nonblocking, and its owner, reason, approval receipt, scope, and expiry remain in the
report.

## Phase 8: Deterministic readiness verdict

Evaluate every policy-required budget, test, blocker, design, and accessibility item
for the exact final candidate.

Apply this order:

1. invalid candidate identity, manifest, policy, or internal processing ->
   `Readiness Verdict: ERROR`;
2. any current conclusive budget violation, test failure, regression, open
   release-blocking finding, unapproved gameplay-affecting effect, accessibility
   failure, or unresolved unexpected write -> `NEEDS MORE WORK`;
3. otherwise, any required receipt/evidence is `NOT_RUN`, `PARTIAL`, `UNKNOWN`,
   `TIMEOUT`, `STALE`, `MISSING`, `INVALID`, or `UNAVAILABLE`, or required
   platform/hardware coverage is incomplete -> `INCOMPLETE`;
4. only when there are zero open release blockers and every required receipt is
   current, revision-matched, complete, and passing -> `READY FOR RELEASE`.

A current conclusive FAIL takes precedence over incomplete evidence in the overall
verdict while the report still lists every omitted/unknown input. User risk preference cannot rewrite
evidence. A deferred finding is nonblocking only when the exact policy classifies it
non-required and records owner, rationale, scope, expiry/review point, and current
approval receipt; it remains visible.

`READY FOR RELEASE` binds only the report's exact candidate/artifact identifier,
platform/configuration matrix, evidence snapshot identifier, and policy revision. It becomes
stale on any byte, requirement, budget, policy, test, or environment change. Always
return `Release Authorization: NOT GRANTED`.

## Phase 9: Persistence and handoff

For persisted assessment or verification, preview only the controller-owned CREATE
paths. Immediately before writing, revalidate every input and confirm targets are
absent. Write atomically, read back exact bytes, validate references/counts, and
return full revision. Declined or failed persistence creates no consumable report.

The final report includes:

- target/baseline/final candidate/build/artifact/source/platform/hardware identity;
- workflow, implementation, evidence, readiness, release-authorization and
  persistence states;
- ordered stable findings with status, severity, owner and evidence revisions;
- authorized mutation and writer ledger, patch/integration/build receipt revisions;
- before/final metrics against exact budget thresholds;
- complete test/accessibility matrix and execution evidence;
- partial, timeout, cancelled, unavailable, not-run, stale and unexpected-write rows;
- checkpoint chain and next permitted action;
- all remaining issues with quantified gap, severity, owner and remediation boundary.

This workflow stops after reporting. It does not invoke another workflow, create a
release artifact, update milestone/stage state, commit, tag, push, deploy, publish,
send a message, or schedule work. A downstream consumer must revalidate this report and
candidate and make its own separately authorized decision.
