---
name: team-ui
description: "Orchestrates an approved UX spec into a uniquely owned, bounded UI implementation and verifies the final build hash with independent evidence before completion."
---

## Invocation and scope

Invoke only as:

~~~text
$team-ui --manifest {ui-feature-request-path} [--resume {checkpoint-path}]
~~~

The manifest is mandatory. Before reading any project artifact, reject no argument, unknown or duplicate flags, missing values, directories, unsafe IDs, path traversal, and unsupported schema. With no argument, show this usage and stop with no reads, delegates, writes, or verdict.

Require Artifact Type: ui-feature-request, Schema Version: 1 and:

- stable screen ID, run ID, and create or revise operation;
- exact UX-spec target path and expected absent/base-file SHA-256;
- ordered context paths/hashes plus file/byte budgets;
- platform, input, resolution/aspect, locale, accessibility, colorblind, motion, text-scale, and device targets;
- exact engine/technical-preferences path/hash or Engine Status: UNCONFIGURED;
- interaction-pattern library path/hash or explicit ABSENT;
- art-bible, accessibility-requirements, player-journey, relevant GDD requirement, visual-budget, and platform-manifest paths/hashes;
- target source/output roots and applicable AGENTS.md paths/hashes;
- named artifact owners;
- maximum revision/fix rounds, per-task timeout, phase deadline, and maximum concurrent reviewers;
- exact orchestration record root.

Screen and run IDs are stable slugs or UUIDs, not dates alone. Resolve real paths and reject symlinks escaping the project root. Re-hash exact bytes; do not discover all relevant GDDs or newest artifacts. Enforce the declared context budget and list omitted context.

## State, authority, and review-mode rules

Resolve optional consultation mode exactly once from the manifest: full, lean, or solo. It never weakens a mandatory quality gate.

- full may add optional director consultations whose output is advisory and hash-bound;
- lean skips optional consultations but retains every mandatory independent review;
- solo may author a design/prototype in the current agent, but cannot satisfy independent-review quorum or produce production COMPLETE.

Use these pipeline results:

- SPEC_APPROVED: current UX spec has persisted current-hash approval, but no verified production implementation;
- ACCEPTED_RISK_SPEC_NOT_APPROVED: user accepted named open findings; only prototype/backlog planning is allowed;
- NEEDS_REVISION: current spec or implementation has open blocking findings;
- IMPLEMENTATION_VERIFIED: final implementation/build hash passed all mandatory evidence;
- PARTIAL: a required task timed out, errored, or returned incomplete evidence;
- BLOCKED: identity, prerequisite, authorization, ownership, convergence, engine, mutation, or persistence prevents the next legal transition.

Verdict: COMPLETE is allowed only with Pipeline Result: IMPLEMENTATION_VERIFIED. All other results use Verdict: PARTIAL or BLOCKED as applicable. Accepted risk never changes a review verdict, never makes approval evidence eligible, and never authorizes production implementation.

## Artifact ownership and mutation domains

This pipeline is not read-only: named writer tasks may write only the exact operations declared in the currently authorized phase manifest. All reviewer tasks are read-only.

Assign one writer to each path before any write:

| Artifact domain | Unique writer | Other roles |
|---|---|---|
| UX spec | ux-author task | all reviewers read-only |
| UX-review recorder envelopes, phase/implementation manifests, checkpoints, final result | coordinator-recorder | agents return conversation records only |
| Visual spec and asset manifest | art-author task | art reviewer is a different read-only task |
| Engine implementation plan | engine-plan author | engine reviewer is a different read-only task |
| Feature-local pattern proposal | ux-author task | ui-programmer read-only |
| Global interaction-pattern library | external UX-library owner, outside this run | ui-programmer and coordinator never write |
| ADR/global UI framework/navigation/binding | architecture owner, outside this run | team-ui emits proposal only |
| Implementation files listed by manifest | one ui-programmer writer | all review tasks read-only |
| Build/test logs and evidence | declared runner/evidence recorder paths | reviewers read-only |

No agent may delegate further, change another owner's file, or share a write target. The ui-programmer must not create, edit, append, or normalize design/ux/interaction-patterns.md. A new or changed global pattern becomes a feature-local proposal with stable ID UXP-{screen-id}-{slug}; only the external UX-library owner may approve and merge it in a separately authorized task. A feature may reference an approved spec's local proposal, but must not describe it as a global reusable pattern. Cross-screen behavior blocks implementation until the library/ADR owner resolves it.

For every writer operation, record operation type, exact path, expected base hash or ABSENT, writer task ID, approved content/diff hash, and maximum bytes. Immediately before and after writing, re-hash inputs/base, enumerate changed paths, and compare them with the active allowlist. An outside-path mutation halts the pipeline; report it without silently reverting user work.

## Authorization boundaries

There is no single up-front authorization for the unknown full pipeline.

1. Read-only planning and in-memory/scratch drafting happen before project writes.
2. Design authorization covers only exact UX-spec, bounded revision, review-envelope, and checkpoint paths. It may authorize at most two revisions of the same spec path, and only changes mapped to stable open finding IDs plus an explicitly approved product decision.
3. After current-hash UX approval, visual and engine authors draft candidate bytes without project writes. Preview their exact artifact paths/operations and obtain bounded design-support authorization.
4. Only after approved design-support artifacts exist may the coordinator generate the precise implementation manifest. Preview exact implementation paths, operations, base hashes, unique writer, evidence paths, and explicit non-writes; obtain a separate implementation authorization.
5. New files, changed paths, global-pattern/ADR edits, or output expansion require a new manifest and authorization. Nested roles never request per-file approval and never broaden the orchestrator's boundary.

An explicit user request can authorize a listed boundary when it names the exact operations. It cannot authorize implementation paths that have not yet been planned and enumerated.

## Phase 0: Create or resume bounded orchestration state

Read every applicable AGENTS.md from project root through each declared output, including src/ui/AGENTS.md when it governs implementation. Hash and record the precedence chain. Require its scalable-text, colorblind, accessibility, localization, input, performance, and never-block-game-thread constraints in later checks.

Use immutable checkpoints:

~~~text
production/ui/team-ui/{screen-id}/{run-id}/checkpoints/{sequence}-{phase}.yaml
production/ui/team-ui/{screen-id}/{run-id}/result.md
~~~

Each checkpoint contains request/context/instruction hashes, phase state, exact authorized mutation manifest/hash, artifact/output hashes, task IDs/status/deadlines, decisions, stable open/closed finding IDs, target build/source hash, operation ledger, and next legal transition. The coordinator-recorder is the only writer.

A resume path must be exact and hash-verified. Re-hash every checkpoint input/output. If any changed, mark the dependent phase STALE and resume from the earliest affected read-only planning point; never reuse a stale approval or review. A checkpoint cannot authorize a write absent from its recorded manifest.

## Phase 1: Bounded UX authoring

Load only declared context. Missing accessibility requirements, target platforms/inputs, or required author schema is a blocking design gap; do not guess.

The ux-author drafts the exact create/revise candidate in scratch using the current UX author profile. It must include stable screen identity, requirement links, flow/states, navigation, input variants, localization, text scaling/reflow, colorblind/non-color cues, reduced motion, data/event ownership, accessibility, acceptance criteria, and pattern references/proposals.

If the global pattern library is absent, do not create it in this run. Use explicit feature-local proposals or block cross-screen patterns. No implementation role may backfill it.

Preview and authorize the bounded design changeset, then let only the ux-author write the UX spec. Verify exact bytes, target path, base hash, and absence of outside mutations. Write a checkpoint.

## Phase 2: Independent hash-bound UX review with finite convergence

Run the staged ux-review P0 read-only protocol in a fresh reviewer task that is not the author task. Require:

- review_record_schema: ux-review-record-v1;
- review_policy: ux-review-p0-v1;
- review_status: COMPLETE;
- exact target path/SHA-256 and current author-schema hash;
- stable UXF finding IDs and required-check coverage;
- deterministic verdict and approval_status;
- gate_evidence_eligible true only for APPROVED.

The reviewer returns a conversation record with gate_evidence_status: NOT_PERSISTED. The coordinator-recorder re-hashes the unchanged target and persists an immutable envelope at:

~~~text
production/qa/evidence/ui/{screen-id}/{run-id}/ux-review-round-{n}.yaml
~~~

The envelope contains Artifact Type: team-ui-ux-review-evidence, Schema Version: 1, exact embedded review-record bytes/hash, target path/hash, recorder identity/time, Persistence: WRITTEN, and read-back hash. Never edit the embedded record or change NOT_PERSISTED inside it.

Formal approval requires the persisted envelope, embedded COMPLETE + APPROVED, approval_status APPROVED, gate_evidence_eligible true, zero MAJOR/BLOCKING findings, complete required-check coverage, and a target hash equal to current UX-spec bytes.

### Revision limit

Initial review is round 0. Permit at most two author revision attempts, rounds 1 and 2.

- Reuse stable finding IDs for the same checks.
- Each author revision lists finding ID, before/after evidence, exact diff, and any regression-risk area.
- Re-review checks every previously OPEN finding plus a full required-check regression scan.
- Advisory expansion cannot create unbounded scope; new blocking findings must map to deterministic check IDs.
- The ux-author remains the only spec writer; reviewer and recorder remain read-only to the spec.

If the same MAJOR/BLOCKING finding remains open after two revisions, or the reviewer cannot complete, return BLOCKED or PARTIAL with USER DECISION. Legal choices are narrow/redefine the feature in a new request, stop, or record ACCEPTED_RISK_SPEC_NOT_APPROVED. Accepted risk may generate a backlog/prototype proposal only under a separate nonproduction path manifest; it cannot enter Phase 3, production implementation, or COMPLETE.

## Phase 3: Visual, asset, and engine proposals

Proceed only from a current persisted approved UX envelope.

In scratch, an art-author drafts:

- design/ui/{screen-id}/visual-spec.md;
- design/ui/{screen-id}/asset-manifest.yaml.

Bind both to UX-spec path/hash, art-bible/hash, accessibility/hash, platform/profile targets, color/contrast, typography/text scaling, spacing/reflow, motion, localization, supported resolutions/aspects, and stable asset IDs/specifications.

When engine status is configured, an engine-plan author drafts design/ui/{screen-id}/engine-plan.md bound to exact engine/version, technical preferences/hash, UX/visual hashes, applicable implementation AGENTS chain, UI hierarchy/navigation/data-binding/events, localization, lifecycle/performance, and test hooks. If a framework/navigation/binding choice affects multiple screens, emit an ADR proposal and block implementation until an accepted current ADR is supplied.

If engine status is UNCONFIGURED, stop after SPEC_APPROVED or a separately authorized engine-neutral prototype plan. Do not spawn ui-programmer, write production UI, or return COMPLETE.

Preview exact support artifacts and obtain design-support authorization. Unique authors write only their owned files; verify bytes and mutation allowlists. Checkpoint all hashes.

## Phase 4: Build and authorize the precise implementation manifest

Create an exact candidate manifest:

~~~text
Artifact Type: ui-implementation-manifest
Schema Version: 1
Screen ID: {screen-id}
Run ID: {run-id}
UX Spec Path/SHA-256: {path/hash}
UX Approval Envelope Path/SHA-256: {path/hash}
Visual Spec Path/SHA-256: {path/hash}
Asset Manifest Path/SHA-256: {path/hash}
Engine Plan Path/SHA-256: {path/hash}
Engine/Version: {identity}
Applicable AGENTS Chain SHA-256: {hash}
Writer Task ID: {single ui-programmer}
Operations: [{CREATE|UPDATE, exact path, expected base hash or ABSENT, max bytes}]
Evidence Outputs: [{exact paths}]
Explicit Non-Writes: [global pattern library, UX spec, visual/asset/engine plan, ADRs, game-state owners, session state]
~~~

Include localization tables only if exact owned operations and owner are authorized. UI never owns game state; it displays bound state and emits declared events.

Before authorization verify every input hash and that every path is necessary. Present full paths/operations/base hashes/owners/non-writes and obtain one implementation authorization. Persist and re-read the manifest before spawning the writer. No writer starts from a proposed, declined, stale, or partial manifest.

## Phase 5: Single-writer implementation and build evidence

Spawn exactly one ui-programmer writer with the authorized manifest and no delegation permission. It may write only listed implementation paths.

Require implementation to:

- follow the approved current UX, visual, asset, engine, pattern, and ADR inputs;
- support every platform-manifest input method rather than hardcoded assumptions;
- use localization keys for player-facing text;
- support declared text scales with reflow/no clipping;
- preserve non-color state cues and colorblind modes;
- respect reduced motion and skippable transitions;
- route UI audio through declared events;
- avoid direct game-state ownership/mutation;
- avoid blocking the game/main thread;
- expose deterministic navigation, lifecycle, accessibility, and performance test hooks.

After writing, enforce the mutation allowlist and record exact source hashes. Produce a candidate build receipt binding source commit/tree hash, engine/version, platform/config, implementation-manifest hash, UI source-set hash, build ID/artifact hash, compile result, warnings, logs/hashes, and test adapter identity. Compile/run failure, missing engine, outside mutation, or incomplete receipt is BLOCKED/PARTIAL, never implementation complete.

## Phase 6: Bounded independent review, fixes, and final revalidation

Mandatory review evidence is independent of review mode. Authors/writer cannot review their own domain. Reviewers are read-only.

Run at most max_parallel_reviewers, capped at 3. Agents may not spawn children. Use stable task IDs and two waves as needed:

- independent UX-conformance reviewer;
- independent art-consistency reviewer;
- accessibility specialist;
- engine UI specialist plus QA evidence validation.

Every task receives exact implementation manifest, final candidate build/source hashes, only its bounded context, stable check IDs, deadline, and output schema. Default timeout is the manifest value, capped at 15 minutes; allow one retry with the same target hash and narrower scope. Cap total review phase at 30 minutes. Timeout, error, missing stream, target-hash mismatch, or malformed output yields PARTIAL and cannot satisfy quorum.

Each finding has stable ID UIF-{stream}-{check-id}, severity BLOCKING or ADVISORY, exact target build/source hash, observed evidence, expected requirement, owner, and remediation.

Required evidence matrix includes all declared:

- keyboard/gamepad/touch/assistive input and focus restoration;
- minimum/maximum resolution, every supported aspect ratio, safe zones;
- locales, text expansion, every committed text scale and reflow;
- contrast, non-color cues, colorblind modes;
- reduced motion/skippable transitions;
- UI event/audio routing and no direct game-state mutation;
- frame time, main/game-thread stalls, allocation/lifecycle/leak checks;
- engine-specific navigation/data binding/lifecycle rules.

Evidence rows bind check ID, build ID/hash, source-set hash, platform/device/config, observer/runner, timestamp, method, result, artifact/log path/hash. Missing/UNKNOWN/NOT RUN/stale evidence is blocking.

### Fix and re-review loop

The same ui-programmer is the only fix writer. Permit at most two fix rounds.

1. Apply only approved BLOCKING finding IDs within the existing implementation manifest. New paths require new authorization.
2. Rebuild and produce a new build/source-set hash.
3. Treat every old review as stale.
4. Re-run all previously open checks plus the full regression matrix against the new final hash.
5. Persist immutable reviewer envelopes/checkpoints bound to that hash.

If the same blocker remains after two fix rounds, any required stream lacks COMPLETE evidence, or a writer changes a non-owned file, return BLOCKED/PARTIAL. Risk acceptance cannot close a mandatory blocker.

## Phase 7: Deterministic completion and stop

Verdict: COMPLETE and Pipeline Result: IMPLEMENTATION_VERIFIED require all of:

- current persisted UX approval envelope for exact final UX-spec hash;
- verified visual/asset/engine/ADR inputs and implementation manifest;
- authorized mutation ledger with no outside writes;
- final build and source-set hashes after the last fix;
- all four mandatory review streams COMPLETE and bound to that final hash;
- evidence matrix complete with zero open BLOCKING findings;
- accessibility, input, resolution/aspect, locale/text scaling, colorblind, motion, engine, cleanup, and main-thread checks conclusive;
- every artifact/checkpoint/result written and read-back verified;
- global interaction-pattern library unchanged by programmer.

Otherwise return the precise Pipeline Result and Verdict: PARTIAL or BLOCKED. Do not describe visual/spec/implementation work as complete when its current-hash evidence is missing.

The final result at production/ui/team-ui/{screen-id}/{run-id}/result.md records every artifact/path/hash, authorization manifest/hash, task status/deadline, finding transition, build/source-set hash, evidence row, mutation, checkpoint, persistence result, and the single legal next action.

State-driven next action examples: revise one named UX finding, obtain engine configuration/ADR, authorize the exact implementation manifest, repair one named blocker, rerun one timed-out review, or hand the verified result to the story owner. Do not auto-invoke another workflow.
