# Team UI request and record contracts

This file is normative for `$team-ui`. Revisions are explicit schema values associated with stable IDs and canonical paths. All project paths are canonical, project-relative, forward-slash paths with no `.` or `..` segment. Enumerations are case-sensitive.

## Request schema: `cgs.team-ui-request/v2`

The manifest is UTF-8 YAML with these required fields:

~~~yaml
schema: cgs.team-ui-request/v2
screen_id: inventory
run_id: inventory-pass-1
operation: CREATE
project_root: <canonical absolute project root>
ux_spec:
  path: design/ux/inventory.md
  expected: ABSENT
context_budget:
  max_files: 32
  max_total_bytes: 524288
  max_file_bytes: 131072
context:
  - path: design/gdd/inventory.md
    revision: <explicit revision>
    bytes: <exact non-negative integer>
    purpose: REQ_SOURCE
    required: true
requirements: [TR-UI-001]
targets:
  platforms: [windows]
  inputs: [keyboard-mouse, gamepad]
  resolutions: [1920x1080]
  aspects: [16:9]
  locales: [en-US]
  text_scales: [1.0]
  accessibility_modes: [reduced-motion, colorblind]
  devices: [desktop-reference]
engine:
  status: CONFIGURED
  identity: Godot
  version: <exact version>
  version_source_path: <declared context path>
  version_source_revision: <explicit revision>
technical_preferences: {path: <declared path>, revision: <explicit revision>}
interaction_patterns: {status: PRESENT, path: <declared path>, revision: <explicit revision>}
art_bible:
  path: <declared path>
  revision: <explicit revision>
  authoring_receipt: {path: <declared path>, revision: <explicit revision>}
  review:
    schema: cgs.art-bible-review/v1
    path: <declared immutable record path>
    revision: <explicit revision>
    gate: AD-ART-BIBLE
    verdict: APPROVE
accessibility_requirements: {path: <declared path>, revision: <explicit revision>}
player_journey: {path: <declared path>, revision: <explicit revision>}
visual_budget: {path: <declared path>, revision: <explicit revision>}
platform_manifest: {path: <declared path>, revision: <explicit revision>}
localization:
  manifest:
    schema: cgs.localization-manifest/v2
    path: <canonical project-relative path>
    revision: <explicit revision>
  catalog:
    schema: cgs.localization-catalog/v2
    path: <exact manifest source_table.path>
    revision: <explicit revision>
    source_locale: <canonical BCP-47 tag>
    source_table_revision: <same exact raw catalog revision>
    keyset_revision: <canonical current keyset reference ID>
    catalog_identity_revision: <current derived catalog identity>
  package_requirement: REQUIRED | NOT_REQUIRED
  packages:
    - schema: cgs.localization-package/v1
      path: <canonical project-relative package path>
      revision: <exact raw package revision>
      locale: <canonical target locale>
      page: <stable page/range identity>
      source_table_revision: <same current catalog declared revision>
      keyset_revision: <same current keyset reference ID>
      catalog_identity_revision: <same current catalog identity>
      package_payload_revision: <recomputed internal package reference ID>
instruction_chain:
  - {path: AGENTS.md, revision: <explicit revision>}
  - {path: src/AGENTS.md, revision: <explicit revision>}
  - {path: src/ui/AGENTS.md, revision: <explicit revision>}
owners:
  ux_author: <stable identity>
  art_author: <stable identity>
  engine_plan_author: <stable identity>
  ui_programmer: <stable identity>
  evidence_runner: <stable identity>
  ux_reviewer: <different stable identity>
  art_reviewer: <different stable identity>
  accessibility_reviewer: <different stable identity>
  engine_qa_reviewer: <different stable identity>
  coordinator_recorder: <stable identity>
consultation_mode: lean
resume_checkpoint: null
authorization:
  design: PROPOSED
  design_support: NOT_REQUESTED
  implementation: NOT_REQUESTED
limits:
  ux_revision_rounds: 2
  implementation_fix_rounds: 2
  max_parallel_tasks: 3
  attempt_timeout_seconds: 600
  phase_timeout_seconds: 1800
  max_readonly_attempts: 2
~~~

For `REVISE`, `ux_spec.expected` is the exact base revision. For `CREATE`, it is `ABSENT`, and the target must not exist. `screen_id` and `run_id` match `^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$`; no date-only run ID is allowed. `operation` is `CREATE` or `REVISE`.

The canonical UX target is exactly `design/ux/<screen_id>.md`. The manifest path must equal it after normalization. `project_root` must resolve to the active project root. Each referenced artifact must also appear exactly once in `context`, except the request itself and future output paths.

For a new run, `resume_checkpoint` is `null`. When `--resume <checkpoint-path>` is present, it is `{path: <the same canonical checkpoint path>, revision: <explicit revision>}`. The flag and manifest field must either both be present or both be absent. The coordinator requires `resume_checkpoint.path` to equal the flag and verifies checkpoint bytes against `resume_checkpoint.revision` before trusting any checkpoint field.

Engine status is `CONFIGURED` or `UNCONFIGURED`. When unconfigured, `identity`, `version`, version source, technical preferences, and production engine work are ineligible; use explicit `null` values rather than guessed placeholders. Interaction patterns use `PRESENT` with path/revision or `ABSENT` with both path/revision `null`.

Required named context purposes are `REQ_SOURCE`, `ART_BIBLE`, `ART_BIBLE_AUTHORING_RECEIPT`, `ART_BIBLE_REVIEW`, `ACCESSIBILITY`, `PLAYER_JOURNEY`, `VISUAL_BUDGET`, `PLATFORM_MANIFEST`, `LOCALIZATION_MANIFEST`, `LOCALIZATION_CATALOG`, `LOCALIZATION_PACKAGE`, `ENGINE_VERSION`, `TECHNICAL_PREFERENCES`, `INTERACTION_PATTERNS`, and `INSTRUCTION`. `LOCALIZATION_PACKAGE` is required only for each package item declared below. The art-bible review must be an independent immutable current `cgs.art-bible-review/v1` record with gate `AD-ART-BIBLE` and verdict `APPROVE`; it binds the exact target path/revision, verified authoring-receipt ID/path/revision, AB-1 and all nine section revisions, current dependency and context-manifest revision, author identities, and reviewer separation. `CONCERNS`, `REJECT`, missing/stale/malformed review or receipt evidence, wrong role, identity overlap, or changed target/context is production-ineligible. For each canonical output and implementation operation, enumerate only root-to-parent directories and probe the exact `<directory>/AGENTS.md` candidate; every existing instruction is a required `INSTRUCTION` entry and counts toward the budget. A context entry may serve more than one explicitly listed purpose but is counted once. No wildcard, directory, URL, generated listing, “latest”, or optional discovery directive is valid.

The localization tuple is mandatory and read-only. Revalidate and strictly parse the
exact `cgs.localization-manifest/v2`; require its `catalog_schema` to be exactly
`cgs.localization-catalog/v2` and `source_table.path` to equal `catalog.path`.
Revalidate the catalog/source table with the manifest-declared deterministic
format/schema/parser, recompute `source_table_revision`, the canonical current
`keyset_revision`, and `catalog_identity_revision` using the `$localize` v2 formulas,
and require all request values to match. `source_locale` must equal the manifest,
and every bounded `targets.locales` entry must equal the source locale or one exact
manifest `target_locales` key. Path/name/time/latest evidence never proves
currentness.

`package_requirement: NOT_REQUIRED` requires `packages: []` and prohibits every
task from reading or relying on a package. `REQUIRED` is mandatory whenever the
authorized implementation/support plan consumes a localization package; each
required locale/page has exactly one package row and context entry. Every package
must be exact `cgs.localization-package/v1`, Revalidate at its declared path, reproduce
its internal package payload revision by omitting exactly `package_payload_revision` and
derived `package_id`, re-derive `package_id` as `LOCPKG-` plus the first 20
lowercase reference ID characters, and bind the same current source-table, keyset,
catalog identity, locale, stable key page, plural/placeholder policies, owner, and
privacy attestations. Missing/extra/duplicate/stale/malformed package rows or an
identity mismatch are invalid. None of these inputs grants team-ui authority to
write the manifest, catalog, package, target translations, or locale ledgers.

### Hard bounds

The request and every derived task obey all of these hard caps:

| Dimension | Maximum |
|---|---:|
| project context files | 32 |
| aggregate project context bytes | 524288 |
| one context file | 131072 bytes |
| stable requirement IDs | 128 |
| platforms | 8 |
| input profiles | 12 |
| resolutions | 24 |
| aspect ratios | 16 |
| locales | 32 |
| text scales | 8 |
| accessibility modes | 16 |
| devices/configurations | 24 |
| referenced pattern IDs | 64 |
| implementation source operations | 128 |
| evidence output operations | 128 |
| evidence matrix rows | 1024 |
| one recorder artifact | 524288 bytes |

Lists must be non-empty where the project declares support. Duplicates after case-appropriate normalization are invalid. The cross product need not be executed blindly: a versioned, declared coverage profile may select pairwise rows, but every value must occur in at least one row and every nested mandatory rule must have a row. The profile path/revision and selection algorithm/version become evidence inputs. If no approved profile exists, require the full bounded cross product or stop `BLOCKED: COVERAGE_PROFILE_REQUIRED` before implementation authorization.

The manifest may lower but never raise caps. Exceeding a hard cap is invalid; truncation is forbidden. Exact byte count means the number of bytes read before decoding.

## Canonical output paths

For one `<screen-id>/<run-id>`, only these coordinator-owned record families are valid:

~~~text
production/ui/team-ui/<screen-id>/<run-id>/checkpoints/<sequence>-<phase>.yaml
production/ui/team-ui/<screen-id>/<run-id>/reviews/ux-round-<n>.yaml
production/ui/team-ui/<screen-id>/<run-id>/reviews/final-<stream>-round-<n>.yaml
production/ui/team-ui/<screen-id>/<run-id>/evidence/build-round-<n>.yaml
production/ui/team-ui/<screen-id>/<run-id>/evidence/matrix-round-<n>.yaml
production/ui/team-ui/<screen-id>/<run-id>/implementation-manifest.yaml
production/ui/team-ui/<screen-id>/<run-id>/result.md
~~~

Temporary atomic-write siblings use the same directory and final filename plus `.tmp-<attempt-token>`. They must be listed in the active recorder allowlist and must be absent after successful replacement. Raw engine logs/build artifacts may use other exact paths only when the authorized implementation manifest names them, assigns their runner, and binds a byte cap.

Design-support paths are exactly:

~~~text
design/ui/<screen-id>/visual-spec.md
design/ui/<screen-id>/asset-manifest.yaml
design/ui/<screen-id>/engine-plan.md
~~~

## Direct-task packet: `cgs.team-ui-task/v2`

Every role task receives one frozen packet containing:

- `schema`, `screen_id`, `run_id`, `phase`, `task_id`, `attempt`, and unique `attempt_token`;
- `role` from `UX_AUTHOR`, `UX_REVIEWER`, `ART_AUTHOR`, `ENGINE_PLAN_AUTHOR`, `UI_PROGRAMMER`, `EVIDENCE_RUNNER`, `UX_CONFORMANCE_REVIEWER`, `ART_CONSISTENCY_REVIEWER`, `ACCESSIBILITY_REVIEWER`, or `ENGINE_QA_REVIEWER`;
- request path/revision, skill-contract revision, ordered instruction-chain paths/revisions, and current checkpoint path/revision;
- exact target build/source/artifact paths and revisions;
- the role’s ordered context subset with exact bytes and the inherited lower budgets;
- stable requirement/check/finding IDs in scope;
- exact allowed read roots, write operations, and explicit non-writes;
- output schema and maximum output bytes;
- start deadline, attempt deadline, phase deadline, and cancellation channel/token;
- `children_allowed: false` and `network_allowed` derived from the approved evidence adapter, otherwise false.

For `UX_AUTHOR`, the packet additionally carries exact current `ux-design` main and continuation paths/declared revision, their NUL-delimited `author_schema_revision`, and canonical `cgs.ux-author-contract-manifest/v1`. Its output schema is not team-ui-owned: it is the current `ux-spec` artifact tuple `ux-profile-schema-v2`, `cgs.ux-content-profile/v2`, `ux-design-author-<revision>`, including the exact header and ordered stable sections `UXS-01` through `UXS-14` defined by those source bytes. Any alternate schema at `design/ux/<screen-id>.md` is malformed.

For `UX_REVIEWER`, the packet additionally carries the exact current UX-review main, continuation, and rules paths/declared revision, the computed review bundle revision, the author-contract manifest, and the complete current assertion matrix. Its output schema is exactly `cgs.review-evidence/v1` with a `cgs.ux-review/v2` extension as defined by those review-contract bytes. The response must remain `gate_evidence_status: NOT_PERSISTED` and `gate_evidence_eligible: false`; direct-task transport does not change the owner contract.

The packet revision is recorded before dispatch. A role response must echo packet revision, task/attempt/token, target identities, status, covered check IDs, output revision, and mutation claim. A packet or response missing a required field is malformed and cannot satisfy a gate.

## UX and final-review records

The UX-review payload is the complete `cgs.review-evidence/v1` envelope with `cgs.ux-review/v2` extension, without field renaming, omission, or verdict translation. Its canonical record ID, producer bundle revision, target/dependency ledger, routing tuple, author-contract manifest revision, assertion and requirement coverage, findings/stable finding keys, consultation/convergence state, mutation guard, verdict, approval status, and non-persisted gate state must all validate under the current UX-review contract.

The coordinator-owned `cgs.team-ui-ux-review-recording/v1` wrapper contains the exact embedded envelope bytes/revision and generic record ID; exact review-contract source paths/revisions; target and author-contract identities; reviewer/recorder separation; wrapper path/revision; write/read-back timestamps; persistence outcome; and previous wrapper/checkpoint link. A wrapper is eligible for the team-ui UX gate only when the embedded result is current and `APPROVED`, every contract check passes, and persistence reads back exactly. The wrapper never rewrites embedded `gate_evidence_status: NOT_PERSISTED` or `gate_evidence_eligible: false`.

`cgs.team-ui-final-review/v2` includes stream, reviewer identity, exact implementation-manifest/build/source-set/evidence-matrix revisions, required check IDs, covered check IDs, status, and `UIF-<stream>-<check-id>` findings. Each finding records severity `BLOCKING|ADVISORY`, state `OPEN|CLOSED`, observed evidence row/log revision, expected requirement ID, owner, remediation, and first/last observed build revision.

The coordinator envelope includes the unmodified embedded response bytes/revision, packet revision, role status, target revisions, recorder identity, write/read-back timestamps, persistence status, final envelope revision, and previous envelope/checkpoint link. It cannot upgrade the embedded status.

## Runtime evidence matrix

Only an evidence runner distinct from the UI programmer and all reviewers may produce raw runtime receipts. Reviewers validate receipts; they do not create observations. Each `cgs.team-ui-evidence-row/v2` contains:

- stable check and requirement IDs;
- build ID/revision, UI source-set revision, implementation-manifest revision, engine/version, platform/device/config;
- input, resolution/aspect/safe-zone, locale/expansion, text scale, accessibility/colorblind/motion profile as applicable;
- runner identity, adapter name/version/revision, exact argv or structured invocation revision, start/end timestamp, duration, exit code;
- method and actual observation/metric, expected threshold, result `PASS|FAIL|UNKNOWN|NOT_RUN`;
- raw artifact/log canonical path, byte count, and revision.

Mandatory coverage includes focus traversal/restoration for every supported input; min/max resolutions and every aspect/safe zone; every locale or approved expansion profile; every committed text scale with reflow/no clipping; contrast, non-color cues and every colorblind mode; reduced motion and skippable transitions; audio-event routing; no direct game-state mutation; frame/main-thread stalls; allocation/lifecycle/leak cleanup; and engine-specific hierarchy/navigation/data-binding rules.

`UNKNOWN`, `NOT_RUN`, missing raw bytes, stale target identity, unverified adapter, or a reviewer-authored observation is blocking. Static analysis may satisfy only a check explicitly typed `STATIC`; it cannot substitute for a runtime-typed row.

## Implementation manifest: `cgs.ui-implementation-manifest/v2`

The persisted manifest includes screen/run IDs; request and instruction revisions; current UX spec and approval-envelope revisions; visual/asset/engine-plan revision; engine/version; exact art-bible target, authoring-receipt, and current independent `cgs.art-bible-review/v1` APPROVE record identities/revisions; exact current `cgs.localization-manifest/v2`, `cgs.localization-catalog/v2`, derived catalog/keyset/source-table identities and every conditionally required `cgs.localization-package/v1` path/revision/locale/page identity; current Accepted ADR and pattern-entry revisions; coverage-profile identity; one UI-programmer identity; one distinct evidence-runner identity; exact `CREATE|UPDATE` operations with expected base and max bytes; exact raw evidence/log operations; and explicit non-writes.

Explicit non-writes always include the UX spec, global pattern library, art bible/global visual-token sources, visual/asset/engine artifacts during implementation, ADRs, game-state owners, unrelated localization data, project configuration, and all paths absent from the manifest.

## Pipeline results and verdicts

Use this exhaustive mapping:

| Pipeline Result | Verdict | Meaning |
|---|---|---|
| `IMPLEMENTATION_VERIFIED` | `COMPLETE` | every completion predicate is current and conclusive |
| `PARTIAL` | `PARTIAL` | a required bounded task/evidence/persistence operation is incomplete or its final state is unknown |
| `SPEC_APPROVED` | `BLOCKED` | current UX is approved but production prerequisites or authorization remain |
| `ACCEPTED_RISK_SPEC_NOT_APPROVED` | `BLOCKED` | open UX findings were acknowledged; production remains forbidden |
| `NEEDS_REVISION` | `BLOCKED` | one or more current blocking findings require their named owner |
| `BLOCKED` | `BLOCKED` | identity, prerequisite, owner decision, authorization, convergence, mutation, or contract prevents progress |

Invalid invocation returns `ERROR` plus usage before project reads and emits no pipeline result or verdict.

`IMPLEMENTATION_VERIFIED` requires: current persisted UX approval; current support artifacts; exact current independent `cgs.art-bible-review/v1` APPROVE evidence still binding the art-bible target, authoring receipt, context and section/dependency revisions; revalidated current localization manifest/catalog identities and every conditionally required exact package; current Accepted cross-screen owner decisions; authorized read-back-verified implementation manifest; reconciled mutation ledger; successful real build receipt; full evidence matrix bound to the final build/source-set; all four distinct mandatory review streams `COMPLETE`; zero open blocking findings; no unknown/stale/NOT_RUN row; checkpoints/result read back; and the global pattern library and all localization inputs unchanged by team-ui.
