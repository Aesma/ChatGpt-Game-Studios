# Skill Test Spec: $team-polish

## Purpose

Verify that `$team-polish` performs read-only assessment before authorization,
assigns every real mutation to one owner, serializes shared-resource integration,
remeasures the final integrated build, and refuses release readiness on partial,
stale, mismatched, unrun, or inaccessible evidence.

## Fixtures

Positive fixtures provide exact raw bytes and full
`sha256:<64 lowercase hexadecimal>` digests for:

- `polish-target-manifest`, baseline `build-candidate`, artifact, source snapshot,
  applicable AGENTS.md chain, budgets, requirements, QA plan, test manifest, known
  issues, runner commands, hardware inventory, and scope;
- assessment report, stable findings, immutable mutation manifest, authorization
  record, writer ledger, patch/integration/build receipts, checkpoints, and final
  `build-candidate`;
- final-build profile, memory, loading, audio, regression, edge, stress, soak,
  visual, scalability, and accessibility receipts.

Every external fact is represented by a verifiable current receipt. Negative
fixtures change one fact unless stated otherwise. Tests observe file hashes and
delegation order and assert that no undeclared mutation or external action occurs.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name matches the directory.
- [ ] Invocation has explicit `assess`, `implement`, `verify`, and `resume` modes and rejects inferred targets/latest files.
- [ ] `assess` does not fall through to implementation.
- [ ] All assessment delegates are explicitly read-only.
- [ ] No implementation agent or product mutation is allowed before a complete mutation manifest and exact authorization.
- [ ] Assessment persistence, product writes, build/test outputs, and repository/external actions are separate authority layers.
- [ ] File approval never authorizes commit, tag, push, deploy, publication, or stakeholder communication.
- [ ] The mutation manifest lists code, engine, scene/prefab/resource, config, shader/VFX, audio, tooling, test, build, cache, log, report, receipt, and checkpoint effects.
- [ ] Every mutation has stable patch/finding IDs, exact path, operation, base hash, unique writer, dependencies, generated outputs, validation, and rollback.
- [ ] Only disjoint paths may be written in parallel.
- [ ] Every shared scene/config/resource/event/mixer/manifest has one integrator and sequential base-hash validation.
- [ ] `performance-analyst` diagnoses and measures but never writes code.
- [ ] Engine review requires trace hash, engine path/module, boundary justification, and confidence threshold.
- [ ] `tools-programmer` has an explicit content/editor/build-tool trigger.
- [ ] New motion/flash/camera/audio-only/gameplay-feedback effects require an approved design/UX artifact and independent accessibility review.
- [ ] Reduced motion, intensity control, policy-defined flash thresholds, functional equivalent feedback, readability, and settings persistence are mandatory.
- [ ] A final immutable build candidate is created after all patch and shared-resource integration receipts.
- [ ] Final profiling and QA use the same final artifact hash; Phase 1 or per-patch metrics cannot issue readiness.
- [ ] Execution receipts include command, tool, duration, seed/workload, hardware/environment, build hash, timestamps, samples, result, and raw evidence hashes.
- [ ] `NOT_RUN`, partial, unknown, timeout, stale, missing, invalid, unavailable, or incomplete hardware evidence cannot be READY.
- [ ] Readiness uses a deterministic four-result algorithm and requires zero open release blockers.
- [ ] `READY FOR RELEASE` always includes `Release Authorization: NOT GRANTED`.
- [ ] The root counts toward `max_threads`; with `max_threads = 6`, at most five children run when no other agent is live.
- [ ] Exactly one role owns every output path; nested delegation consumes the same cap.
- [ ] Timeouts cancel writers, reconcile path hashes, quarantine late patches, and block reassignment until termination.
- [ ] Immutable checkpoints support hash-verified idempotent resume without replay.
- [ ] The workflow never invokes a downstream workflow or performs release/publication actions.

## Case 1: Read-only assessment before approval

**Input**

~~~text
$team-polish assess --manifest production/polish/combat-target.yaml --assessment-id combat-a1
~~~

All inputs are valid.

**Expected**

- bounded read-only assessment agents may run;
- no product, source, asset, config, test, build, report, or checkpoint file changes;
- stable findings and the proposed path-owner manifest are returned in conversation;
- `Persistence: NOT_REQUESTED`;
- `Implementation State: NOT_AUTHORIZED`.

If `--persist` is supplied, only the exact assessment/proposal/controller paths may
be created after their separate file-write authorization. Product mutation remains
unauthorized.

## Case 2: Complete side-effect disclosure

Assessment proposes a game-code optimization, engine fix, shared scene edit, render
setting, shader/material/VFX edits, new audio event/mixer data, tooling change,
regression fixture, build cache/output, and receipts.

**Expected**

Every effect appears in the mutation manifest with operation, base hash/ABSENT,
writer, dependencies, shared group/integrator, generated outputs, validation, and
rollback. Omit any one class and implementation blocks before authorization.

## Case 3: Approval precedes all implementation

Invoke `implement` with a current assessment and mutation manifest but no prior
bounded approval.

**Expected**

The workflow re-hashes all inputs, previews the exact complete changeset, and waits.
No implementation writer is spawned and no product byte changes. Declining produces
`Implementation State: NOT_AUTHORIZED`.

Approve the exact set in a variant. Only then may the writer ledger and patch
delegations begin. A new path or operation requires a revised assessment and new
authorization.

## Case 4: Disjoint writers and one shared integrator

Three patch owners have disjoint source, VFX, and audio paths. Two also propose
changes to one scene and one event registry.

**Expected**

- disjoint owned paths may run in a bounded parallel batch;
- neither contributor writes the shared scene or registry;
- one manifest-named integrator applies shared inputs sequentially;
- each step validates the current base hash and emits a receipt;
- alias, case-fold, generated-output, or ancestor/descendant overlap is detected.

If two writers are assigned the same canonical path, execution blocks before spawn.

## Case 5: Final integrated build invalidates local metrics

Performance patch profiling passes. A later VFX patch adds particles and an audio
patch adds streaming voices.

**Expected**

Per-patch metrics cannot support readiness. After all patches and shared integration,
one build owner creates a new build candidate. Unified performance, memory, loading,
audio and QA evidence is rerun against that exact final artifact hash.

If final GPU time or audio streaming exceeds budget, verdict is
`NEEDS MORE WORK` even though the performance patch's local metrics passed.

## Case 6: Hidden write outside manifest

A technical-artist changes a render setting not listed in its owner paths.

**Expected**

Inventory reconciliation detects the unexpected hash change, stops integration,
marks the patch failed, records the path/owner, and yields `NEEDS MORE WORK` or
`INCOMPLETE` according to evidence. The workflow does not silently absorb or revert
the change and cannot issue READY.

## Case 7: Performance analyst role boundary

A profiler finding identifies an allocation hotspot.

**Expected**

The performance analyst produces trace, metric, budget gap, path/module, confidence,
and proposed owner evidence only. A programmer is the mutation owner after approval.
A prompt asking the analyst to fix code fails the structural test.

## Case 8: Engine and tools conditional triggers

Variants:

1. profiler trace binds an engine module/path and confidence meets policy;
2. a vague claim says “probably engine”;
3. target manifest includes editor/import automation;
4. target has no tools involvement.

**Expected**

- engine-programmer read-only diagnosis/writer proposal is allowed only in variant 1;
- variant 2 remains UNKNOWN and does not authorize an engine patch;
- tools-programmer runs in variant 3 only;
- tools-programmer does not run in variant 4.

## Case 9: Gameplay-affecting visual effect lacks approval

A technical artist proposes new screen shake and camera motion without a current
approved design/UX requirement.

**Expected**

The proposal may be recorded but cannot enter the authorized mutation set. Neither
technical-artist nor user file approval substitutes for design approval. Verdict
cannot be READY while the required behavior remains unresolved.

## Case 10: Accessibility final-build gate

Provide a final build with screen shake, flashes, and an audio-only critical cue.

Positive variant has current receipts for reduced-motion/disable behavior, intensity
limits, policy-defined flash measurements, functional-equivalent visual/haptic cue,
aim/readability preservation, settings persistence, and an independent
accessibility-specialist review.

**Expected**

Only the positive variant can pass. Missing threshold policy, reduced-motion control,
equivalent cue, persistence, or current review produces `INCOMPLETE`; a measured
threshold/readability failure produces `NEEDS MORE WORK`.

## Case 11: Evidence receipt completeness

For a final profile or test receipt, omit one at a time: candidate/artifact hash,
command/argv, tool version, hardware/environment, configuration, seed/workload,
warm-up/duration, sample count, timestamps, result, budget hash, or raw log hash.

**Expected**

The receipt is invalid/partial and readiness is `INCOMPLETE`. A plan, checkbox,
filename, Phase 1 measurement, or conversation claim cannot replace it.

## Case 12: Required test matrix not run

Variants include unavailable minimum-spec hardware, soak marked NOT RUN, truncated
stress output, timed-out regression, and a receipt for the baseline build.

**Expected**

Each produces `INCOMPLETE`, never READY. The report names the exact missing evidence,
candidate mismatch, owner, and next permitted action. User optimism or phase approval
cannot rewrite the state.

## Case 13: Deterministic verdict order

Assert:

- invalid candidate/policy/manifest -> `ERROR`;
- current conclusive budget violation/regression/release blocker/design/accessibility
  failure -> `NEEDS MORE WORK`;
- otherwise, required missing/partial/not-run/unknown/timeout/stale/invalid/unavailable
  evidence -> `INCOMPLETE`;
- only all current complete passing evidence and zero blockers ->
  `READY FOR RELEASE`.

A current conclusive FAIL has precedence over incomplete evidence in the overall
verdict while every omission remains visible. Every outcome reports `Release Authorization: NOT GRANTED`.

## Case 14: Bounded concurrency

Set `.codex/config.toml` to `max_threads = 6`. The root and two unrelated agents are
live; five assessment tasks exist.

**Expected**

Available child slots are three, so dispatch batches never exceed three. Nested
agents consume the same cap. Invalid/missing config falls back to serial. The
controller gathers each batch before its dependents.

## Case 15: Writer timeout and late patch

A shader writer times out, returns after cancellation, and writes one owned file.

**Expected**

The workflow marks `TIMEOUT`, cancels/interrupts, blocks dependent integration,
reconciles hashes, quarantines the late output, and never assigns that path while the
old writer may be active. Retry requires confirmed termination, stable base, a new
attempt ID, and the same approved scope.

## Case 16: Checkpoint and resume

Interrupt after shared integration and before build.

**Expected**

`resume` verifies every predecessor/checkpoint hash, target/baseline/mutation/
authorization identity, writer ledger, patch receipts, and current path hashes. It
continues from build without replaying completed patches. Drift, altered authority,
missing predecessor, or active stale writer blocks.

## Case 17: Build identity and post-build change

The final candidate records artifact/source/toolchain/platform/mutation/patch/
integration hashes and reproducible build receipt. Then an audio bank byte changes.

**Expected**

All prior final evidence becomes stale. The workflow creates no READY report until a
new candidate is built and the full required verification matrix reruns.

## Case 18: Release/publication boundary

The final verification returns `READY FOR RELEASE`.

**Expected**

`Release Authorization: NOT GRANTED`; no commit, tag, push, release record, deploy,
upload, store submission, public/stakeholder message, downstream workflow invocation,
stage update, or scheduling action occurs. Any downstream consumer must re-hash the
candidate/report and obtain separate authority.

## Case 19: Persisted report integrity

Authorize one exact verification report CREATE.

**Expected**

Immediately before write, every input is re-hashed and target absence is confirmed.
The report is atomically created, read back, internally validated, and returned with
its SHA-256. Decline or failure yields no consumable persisted report and no other
write.

## Case 20: Stable finding rerun

A later verified candidate closes two of five stable finding IDs.

**Expected**

The report compares exact finding IDs and source evidence hashes, marks only verified
closures, preserves unresolved/deferred/unknown findings, and checks diff regressions.
It never starts an open-ended polish loop or selects an earlier report by recency.

## Protocol compliance

- [ ] Phase 1 completes without product mutation before any implementation approval.
- [ ] The complete mutation manifest is stable and hash-bound before writers spawn.
- [ ] Parallel writes are disjoint and bounded; shared resources have one sequential integrator.
- [ ] The final integrated build is created before all release-readiness profiling and QA.
- [ ] Every required final receipt binds the same candidate/artifact hash.
- [ ] Partial, unavailable, unknown, stale, timeout and NOT RUN states are visible and non-ready.
- [ ] Gameplay-affecting polish cannot bypass approved design or accessibility evidence.
- [ ] Unique writer, timeout, cancellation, checkpoint and idempotent resume rules are enforced.
- [ ] No file authorization expands to release, deployment, publication, or messaging.
- [ ] Metadata describes assessment/implementation/verification rather than an unsafe parallel polish pass.
