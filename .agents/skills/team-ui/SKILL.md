---
name: team-ui
description: "Authors and independently approves bounded UX, then orchestrates one owned UI implementation with final-build evidence and deterministic recovery."
---

# Team UI

## Invocation

Use exactly:

~~~text
$team-ui --manifest <ui-request-path> [--resume <checkpoint-path>]
~~~

Parse the command before reading any project file. With no argument, print the usage line and stop with no project reads, agents, writes, checkpoint, pipeline result, or verdict. Reject unknown or duplicate flags, missing values, directories, ambiguous relative paths, unsafe IDs, path traversal, and any positional argument.

The manifest must conform to `cgs.team-ui-request/v2` in [request-and-record-contracts.md](references/request-and-record-contracts.md). That reference is normative for identifiers, canonical paths, context and cardinality limits, records, statuses, and verdicts. [execution-and-recovery.md](references/execution-and-recovery.md) is normative for task attempts, cancellation, checkpoints, mutation reconciliation, resume, and final review. A conflict between this file and either reference is `BLOCKED: CONTRACT_CONFLICT`; do not choose an interpretation.

The sole internal delegation interface is the typed `cgs.team-ui-task/v2` direct-task packet. Do not invoke `$ux-design`, `$ux-review`, or another project workflow, and do not choose between a subskill and an ad-hoc prompt. The packet nevertheless adapts the current owner contracts exactly: UX-author output is the current `ux-design` `ux-spec` artifact contract, and UX-reviewer output is `cgs.review-evidence/v1` with a `cgs.ux-review/v2` extension. Every author, planner, writer, runner, and reviewer receives the same packet schema with a role-specific output schema. An unavailable required role produces `PARTIAL`; it is not replaced by a different interface.

## Bounded request and context

Validate the request bytes and schema before following project paths. Revalidate every declared file from exact bytes and reject a mismatch. Resolve paths under the canonical project root, reject escaping symlinks and duplicate normalized paths, and never search for the newest, likely, or “all relevant” artifact.

The request declares a purpose for each context entry and exact requirement IDs. It also binds the exact current `cgs.localization-manifest/v2`, its `cgs.localization-catalog/v2` source-table path/declared revision and derived source-table/keyset/catalog identities, plus every conditionally implementation-required `cgs.localization-package/v1` path/raw/payload revision and locale/page identity. Project context is capped at 32 files, 524288 aggregate bytes, and 131072 bytes per file. Lower manifest limits are honored; higher limits are invalid. The target matrix is also bounded as specified by the normative reference. Do not silently truncate a required input. If a required input would exceed a cap, stop `BLOCKED: CONTEXT_LIMIT`; list only path, declared purpose, exact byte count, and revision for accepted and rejected entries.

Derive the finite instruction candidates only by joining `AGENTS.md` to the project root and each parent directory of every canonical output or proposed implementation operation. Probe those exact paths, require every existing file to appear in request context, count it against the hard budget, and record the ordered precedence chain. Do not recursively search for instructions. When implementation falls under `src/ui/AGENTS.md`, its localization, keyboard/mouse and gamepad, skippable motion, audio-event routing, no game-state ownership, no game-thread blocking, scalable-text, colorblind, and min/max-resolution rules become mandatory evidence checks.

## State and consultation modes

The optional `consultation_mode` is resolved once and checkpointed. Its default is `lean`. The field `review_mode` is invalid.

- `full` may add read-only advisory director consultations. Advisory output never supplies gate evidence.
- `lean` omits optional consultations and keeps every mandatory author, runner, and reviewer.
- `solo` may produce a scratch design or separately authorized nonproduction prototype proposal, but it cannot satisfy independence and can never start production implementation or return `COMPLETE`.

Mandatory gates and the four final review streams do not vary by mode. Use only the pipeline results and verdict mapping in the normative contract. `COMPLETE` is legal only for `IMPLEMENTATION_VERIFIED`; accepted risk, an approved spec, file existence, reviewer prose, or partial evidence never implies implementation completion.

## Authority, independence, and write ownership

This workflow contains controlled project writes, but all roles are read-only unless this table names them as the one writer for an active, authorized manifest:

| Domain | Sole writer | Independence and non-writes |
|---|---|---|
| UX spec and feature-local pattern proposals | UX author task | UX reviewer is a distinct task and read-only |
| UX-review, final-review, and runner receipt envelopes; phase manifests; checkpoints; final result | coordinator-recorder | never changes embedded role output |
| Visual spec and asset manifest | art author task | art reviewer is a distinct task and read-only |
| Global visual language, tokens, or art-bible policy | external art-bible owner, outside this run | team-ui may report a proposal, never apply it |
| Engine plan | engine-plan author task | engine reviewer is a distinct task and read-only |
| Global interaction-pattern library | external UX-library owner, outside this run | every team-ui role is read-only |
| ADR or cross-screen framework/navigation/binding policy | external architecture owner, outside this run | team-ui may report a proposal, never apply it |
| Authorized implementation source paths | one UI programmer task for the whole run | authors, runner, and reviewers are read-only |
| Declared runtime logs and raw evidence paths | one evidence-runner task | runner cannot edit design or source |

No role may spawn children, share a write target, edit another owner’s artifact, or expand its path list. The UI programmer must not create, edit, append, normalize, or rename the global interaction-pattern library. A new pattern is `UXP-<screen-id>-<slug>` in the feature UX spec and remains feature-local until the external owner accepts it. A cross-screen pattern blocks implementation until a current library entry or Accepted ADR is supplied.

Every write operation records `CREATE` or `UPDATE`, canonical path, expected `ABSENT` or base revision, writer task ID, approved candidate/diff revision, and maximum bytes. Check the complete mutation set immediately before and after each writer. An unexpected change is `BLOCKED: MUTATION_BREACH`; report it without reverting user work.

## Authorization boundaries

An initial request cannot authorize implementation paths that have not been planned.

1. Read-only intake, validation, and scratch drafting require no project mutation.
2. Design authorization can cover only the exact UX-spec operation, its two bounded revisions, the fixed recorder paths, and declared checkpoint temporary/final paths.
3. After current_revision UX approval, visual, asset, and engine candidates are drafted in scratch. Present their exact operations, base revisions, candidate revision, writers, byte caps, and non-writes for a separate design-support authorization.
4. After the support artifacts are current, build the exact implementation manifest. Present every source and evidence operation, base revision, sole writer/runner, byte cap, and explicit non-write for a separate implementation authorization.
5. A new path, changed operation, new owner, changed base revision, or wider output requires a new manifest and authorization. Nested tasks never request approval and never broaden the coordinator’s boundary.

An explicit user instruction can authorize an already enumerated boundary. Pausing for an authorization records `BLOCKED: AUTHORIZATION_REQUIRED` and the single exact next action; it does not fabricate approval.

## Phase 0 — Validate or resume

For a new run, validate the v2 request, canonical paths, revisions, target matrix, owners, configured engine status, and instruction chain. Validate the art-bible target and authoring receipt, then require one fresh independent immutable `cgs.art-bible-review/v1` whose gate is `AD-ART-BIBLE`, verdict is `APPROVE`, reviewer differs from every author/consultant/recorder, and bindings exactly match the current target, authoring receipt, AB-1/all nine section revisions, dependencies, and context bytes. Missing, stale, malformed, `CONCERNS`, `REJECT`, wrong-role, identity-overlap, or revision-mismatched evidence is `BLOCKED: ART_BIBLE_NOT_PRODUCTION_APPROVED`.

Before the first checkpoint, also apply the exact localization preflight from the
request contract: Revalidate/strictly parse the current v2 manifest and catalog,
recompute source-table/keyset/catalog identities, validate exact locale coverage,
and, when package requirement is REQUIRED, Revalidate/parse every exact v1 package
and reproduce its locale/page/payload/source/keyset/catalog bindings. Any absent,
duplicate, malformed, unsupported, stale, revision-mismatched, parser-mismatched,
locale-incomplete, or package-incomplete input is
`BLOCKED: LOCALIZATION_INPUT_NOT_CURRENT`; create no checkpoint and dispatch no
author, support, programmer, runner, or reviewer. Create the first checkpoint only
after both art and localization preflights succeed and its exact recorder paths
are authorized.

For `--resume`, accept only the canonical checkpoint path for the same screen/run and verify its exact revision, request revision, instruction-chain revision, prior checkpoint link, recorded artifacts, authorizations, mutations, task attempt tokens, and current source/build identities. Follow the invalidation and earliest-safe-transition rules in the recovery reference. A checkpoint can never authorize an unrecorded operation.

## Phase 1 — Author the bounded UX spec

Read the current `ux-design` `SKILL.md` and its declared `references/continued-workflow.md`. Record their declared contract versions and construct `cgs.ux-author-contract-manifest/v1`; and require the supported tuple `ux-profile-schema-v2`, `cgs.ux-content-profile/v2`, and `ux-design-author-<revision>`. Missing, mixed, or unsupported author-contract evidence is `BLOCKED: UX_AUTHOR_CONTRACT_INCOMPATIBLE` before a design write.

Send one UX author a `cgs.team-ui-task/v2` packet with the exact spec target, base identity, bounded context, current instruction revisions, the author-contract manifest and source revision, current localization manifest/catalog identities and package identities when required, the current `ux-spec` output schema, deadline, and no-child rule. The canonical UX target is:

~~~text
design/ux/<screen-id>.md
~~~

The candidate must begin with the current `ux-design` header, including `Artifact Type: ux-spec`, `Schema Version: ux-design-author-<revision>`, `Profile Version: ux-profile-schema-v2`, and `Content Profile: cgs.ux-content-profile/v2`. It must contain the exact `UXS-01` through `UXS-14` stable section IDs and headings in author-contract order and satisfy every current `cgs.ux-content-profile/v2` assertion, including the exact required UXS-05 subheadings. It must bind stable requirement IDs and specify flow/state, deterministic focus and navigation, target inputs, resolutions/aspects/safe zones, locales and expansion, every text scale with reflow, non-color cues and colorblind modes, reduced/skippable motion, accessibility, data/event ownership, audio events, lifecycle, acceptance checks, and pattern references/proposals. A team-ui-specific schema or alternate artifact at this canonical path is forbidden.

If the global pattern library is absent, do not create it. A feature-local proposal is allowed; a cross-screen dependency blocks production. Preview and authorize the exact design mutation, then let only the UX author write. Revalidate and verify the whole mutation set before checkpointing.

## Phase 2 — Independently approve the current UX revision

Create a fresh UX reviewer task whose task ID and execution identity differ from the author. It is read-only and receives the exact UX bytes/revision, `cgs.ux-author-contract-manifest/v1`, current author and review-contract source revision, the complete current UX-review assertion matrix, bounded context, and the exact `cgs.review-evidence/v1` envelope with `cgs.ux-review/v2` extension output schema. The direct task applies that contract; it does not invent a team-ui review schema or invoke `$ux-review`.

The coordinator persists the returned bytes without editing them in an immutable envelope at:

~~~text
production/ui/team-ui/<screen-id>/<run-id>/reviews/ux-round-<n>.yaml
~~~

The reviewer result must retain `gate_evidence_status: NOT_PERSISTED` and `gate_evidence_eligible: false`. The coordinator may wrap the exact unchanged bytes only in `cgs.team-ui-ux-review-recording/v1`, after recomputing the generic record ID, extension fields, author-contract manifest, target and dependency revisions, reviewer independence, coverage, and mutation guard. The wrapper records its own path/revision, recorder identity/version, write/read-back timestamps and outcome; it never edits or upgrades the embedded record. Approval requires that read-back-verified wrapper, an embedded complete current generic envelope whose `cgs.ux-review/v2` extension has exact target/profile/content/author-contract identities, deterministic verdict `APPROVED`, `approval_status: APPROVED`, complete required assertion and requirement coverage, and zero open major or blocking findings. Finding IDs and stable finding keys use the exact UX-review algorithm (`UXF-<sanitized-artifact-id>-<check-key>-<stable finding key-prefix>`), not a team-ui-local ID scheme.

Initial review is round 0. Permit no more than two UX author revisions, rounds 1 and 2. Each revision maps open finding IDs to before/after evidence and an exact diff revision. Re-review checks every prior open finding and the full required regression set on the new revision. If the same blocker remains after revision 2, the review is incomplete, or required evidence is missing, stop `BLOCKED` or `PARTIAL` with one user decision.

Accepted risk never changes the review record. Record `ACCEPTED_RISK_SPEC_NOT_APPROVED`; only a separately authorized nonproduction backlog/prototype proposal is legal. Do not enter production support planning, implementation, or `COMPLETE`.

## Phase 3 — Produce owned visual, asset, and engine support

Proceed only from a persisted approval envelope for the current UX revision, the still-current independent `cgs.art-bible-review/v1` APPROVE evidence, and the still-current localization manifest/catalog/package tuple validated in Phase 0. Revalidate the art bible, authoring receipt, review record, localization inputs, context and dependencies immediately before support drafting; any drift blocks support and implementation. In bounded scratch tasks, produce candidates for:

~~~text
design/ui/<screen-id>/visual-spec.md
design/ui/<screen-id>/asset-manifest.yaml
design/ui/<screen-id>/engine-plan.md
~~~

The art author owns the first two. They bind UX; exact art-bible target, authoring-receipt and `cgs.art-bible-review/v1` revisions; accessibility, platform and visual-budget revisions; typography/text scales; contrast/non-color cues; spacing/reflow; motion; localization; resolutions/aspects; and stable asset IDs. The engine-plan author owns the third and binds exact engine/version, technical preferences, instruction chain, UX/visual/asset revisions, hierarchy, focus/navigation, input routing, data binding/events, localization, lifecycle, performance, cleanup, and test hooks.

If engine status is `UNCONFIGURED`, stop after `SPEC_APPROVED` or a separately authorized engine-neutral nonproduction prototype plan. Do not create a production engine plan, spawn a UI programmer, or claim implementation readiness.

If framework, navigation, binding, or interaction policy affects multiple screens, require a current Accepted ADR and, for patterns, a current approved library entry. If visual language, tokens, typography policy, or another art-bible rule changes globally, require a current approved art-bible amendment and its external owner. Route the gap to the named architecture, UX-library, or art-bible owner and stop `BLOCKED: OWNER_DECISION_REQUIRED`; team-ui does not write any of those sources of truth.

After design-support authorization, only the named authors write their paths. Verify bytes, revisions, ownership, and the full mutation set, then checkpoint.

## Phase 4 — Freeze the implementation manifest

The coordinator creates and persists `cgs.ui-implementation-manifest/v2` at the canonical path in the normative reference. It binds the approved UX envelope, visual spec, asset manifest, engine plan, current art-bible target/authoring-receipt/independent APPROVE record, Accepted ADRs/pattern entries, engine/version, instruction chain, one UI-programmer task ID, exact source operations, exact evidence outputs, evidence-runner ID, byte caps, and explicit non-writes.

UI displays bound game state and emits declared commands/events; it never owns or directly mutates game state. The localization manifest, catalog/source table, packages, target translations, and locale ledgers are read-only inputs and explicit non-writes throughout team-ui. UI source may reference only the validated stable keys; changing localization bytes requires a separate owner-authorized workflow and is never a team-ui implementation operation.

Verify all input and base revisions, present the full implementation boundary, obtain one implementation authorization, then persist and read back the manifest. Do not start a writer from a proposed, declined, stale, incomplete, or unpersisted manifest.

## Phase 5 — Single-writer implementation and real build evidence

Start exactly one UI programmer with the authorized manifest and no delegation. It writes only listed source paths and must implement all approved inputs, platform-manifest input methods, localization keys, focus restoration, text-scale reflow/no clipping, non-color cues/colorblind modes, reduced/skippable motion, audio events, declared commands, lifecycle/cleanup, and deterministic accessibility/performance test hooks. It must not block the main/game thread.

After the writer returns, reconcile the complete mutation set and record the exact UI source-set revision. Then start the distinct evidence runner against that immutable source set. The runner executes the declared engine/build/test adapters and writes only declared raw logs/receipts. It must produce actual command/adapter identity, argv/config, engine/version, source commit/tree and source-set revisions, build ID/artifact revision, exit status, timestamps, duration, warnings, main/game-thread stalls, and log revisions. A plan, mock receipt, file-existence check, or reviewer assertion is not runtime evidence.

Compile/run failure, missing engine, unverified adapter, stale source, unknown runner state, missing log, or malformed receipt yields `PARTIAL` or `BLOCKED`, never implementation completion.

## Phase 6 — Independent final review, fixes, and revalidation

Run these four mandatory read-only streams against the same immutable candidate build/source-set revision:

1. UX conformance;
2. art consistency;
3. accessibility;
4. engine UI and QA-evidence validation.

The UX and art reviewers differ from their respective authors. No reviewer may be the UI programmer, evidence runner, or another mandatory stream for this run. The evidence runner supplies observations but never reviews or approves them. Use stable `UIF-<stream>-<check-id>` findings and the full build-bound evidence matrix in the normative contract.

Scheduling, concurrency, deadlines, retry eligibility, cancellation, partial results, and late-output quarantine follow the recovery reference. Any missing/malformed/timed-out stream, incomplete matrix row, target mismatch, `UNKNOWN`, `NOT_RUN`, or stale receipt prevents quorum and yields `PARTIAL`.

The same UI programmer is the only fix writer. Permit at most two fix rounds and only for approved blocking finding IDs within the existing operation paths. New paths require a new authorized manifest. After every fix, rebuild, produce a new build/source-set revision, stale all prior reviews and evidence not bound to the new revision, and rerun every prior open check plus the complete regression matrix. A mandatory blocker cannot be waived.

## Phase 7 — Deterministic result and stop

Return `Pipeline Result: IMPLEMENTATION_VERIFIED` and `Verdict: COMPLETE` only when all completion predicates in the normative contract are true on the post-fix final revision. This includes current persisted UX approval, current support artifacts and accepted owner decisions, authorized mutation ledger with no breach, successful real build/run receipts, all four complete independent review streams, the complete evidence matrix, zero open blockers, and read-back-verified checkpoints/result.

Otherwise use the exact pipeline result and `PARTIAL`/`BLOCKED` mapping. The final result records every input/output path and revision, authorization and manifest identity, task/attempt status, cancellations and quarantined outputs, finding transitions, build/source-set identity, evidence rows, mutation ledger, checkpoints, and persistence status.

Emit exactly one state-derived next action, such as revising one named UX finding, obtaining engine configuration or an Accepted ADR, authorizing one frozen manifest, reconciling one uncertain mutation, repairing one named blocker, or retrying one eligible same_revision task. Never auto-invoke another workflow.
