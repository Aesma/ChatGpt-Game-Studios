---
name: setup-engine
description: "Research, select, verify, configure, refresh, or upgrade a game engine using official-source snapshots, real executable receipts, and strictly authorized atomic project changes."
---

# Setup Engine

Establish a reproducible engine identity. A version string in a document, an existing
file, a downloaded installer, or a user preference is not proof that the project is
configured or upgraded.

## Invocation contract

Invoke only as:

`$setup-engine --manifest {engine-request-path} [--resume {checkpoint-path}]`

Validate arguments before repository reads, network access, external execution,
delegation, decisions, or writes. With no manifest, print this usage line and stop
with no side effects and no verdict. Reject unknown/duplicate flags, missing values,
directories, unsafe IDs, path traversal, and unsupported schemas.

The manifest requires:

- `Artifact Type: engine-request` and `Schema Version: 1`;
- stable request/run IDs and mode `research`, `decision`, `configure`, `refresh`, or
  `upgrade`;
- requested engine, edition/channel, version or version constraint, language/toolchain,
  target platforms, region, organization/revenue context relevant to licensing, and
  project root;
- exact official-source policy, retrieval deadline, source snapshot root, and
  network authorization state;
- for configure/upgrade: expected executable path or installation search roots,
  installation ID if known, executable hash if pinned, supported version-output
  command, required SDK/toolchain commands, and project validation/build/test commands;
- exact project configuration paths, owners, expected base hashes or `ABSENT`,
  candidate/receipt/checkpoint paths, size limits, and explicit non-writes;
- named product decision authority, external installation authority, project mutation
  authority, owner approval for each authoritative file, execution runner, unique
  writers, transaction recorder, and evidence recorder;
- per-command timeout, phase deadline, maximum parallel read-only probes, retry limit,
  rollback policy, and resume checkpoint root;
- for upgrade: verified current active installation receipt, isolated candidate
  workspace, target installation, migration/build/regression matrices, and separate
  activation authority.

Normalize real paths. Reject binaries, installers, candidate workspaces, or outputs
that escape the authorized roots through symlinks or junctions. IDs are stable slugs
or UUIDs, never dates alone.

## State model and completion language

Research, selection, installation, execution verification, and project configuration
are distinct states:

- `RESEARCH_EVIDENCE_READY`: official-source snapshot is complete enough for a
  decision; no engine has been selected, installed, or configured by this state;
- `DECISION_RECORDED`: the named authority selected an evidenced candidate; no
  installation or project mutation is implied;
- `INSTALLATION_VERIFIED`: the exact executable and required toolchain produced valid
  current receipts; project configuration is still unchanged;
- `CONFIGURED`: verified installation identity and project declarations agree, the
  full transaction committed, configuration visibility was independently tested,
  and final receipts are current;
- `REFERENCE_REFRESHED`: authorized reference evidence changed while active engine
  identity remained unchanged;
- `UPGRADE_PLANNED`: target research/audit exists, but no active version changed;
- `UPGRADE_VERIFIED`: target installation, isolated migration, import/serialization,
  build, regression, and activation transaction all passed on final hashes;
- `PARTIAL`: safe evidence exists, but required work/evidence is incomplete;
- `BLOCKED`: authority, official evidence, identity, execution, ownership, CAS,
  rollback, or validation prevents the next legal transition.

`Verdict: COMPLETE` is legal only for requested mode `configure` with state
`CONFIGURED`, or mode `upgrade` with state `UPGRADE_VERIFIED`. Research, decision,
and refresh report their named state without `COMPLETE`. A documentation-only version
edit, file existence, source scan, download success, or user risk acceptance can
never produce `CONFIGURED`, `UPGRADE_VERIFIED`, or `COMPLETE`.

Do not use unqualified claims such as `latest`, `supported`, `free`, `verified`,
`configured`, or `upgraded`. Bind each claim to evidence scope, engine edition/version,
support channel, date, region, and receipt hash.

## Official-source evidence policy

Every mutable external fact must come from a first-party, versioned source. Examples
of eligible publishers are the engine vendor's release archive, documentation,
download manifest/checksum/signature service, platform-support matrix, lifecycle
policy, and legal/license terms. An official publisher's release repository is
eligible only when ownership is verified. Search snippets, aggregators, forums,
blogs, generated summaries, model memory, and user recollection are discovery hints,
not evidence.

For each claim record:

- stable claim ID and claim type;
- engine product, edition, exact version/channel, platform/architecture, locale and
  applicable region;
- canonical official URL, page/document version, publisher, publication/effective
  date, retrieved-at UTC, and exact quoted field or normalized finding;
- content SHA-256 or response-body hash when retrievable, plus ETag/Last-Modified;
- support/lifecycle state, download artifact identity, official checksum/signature
  location, license/royalty context and thresholds when relevant;
- conflicts, unavailable fields, and confidence `CONFIRMED` or `UNRESOLVED`.

Preserve citations and prior snapshot hashes when refreshing. Never silently replace
an official statement with another scope or date. Two conflicting official sources,
an inaccessible mandatory source, missing checksum/signature policy, or unclear
license/platform applicability is `BLOCKED` for any dependent decision. Present the
conflict; do not choose by recency alone.

User-provided versions receive the same verification. Confirm exact existence,
edition, support state, official download, platform/architecture, and applicable
license terms. If a requested version is unsupported or unavailable, report the
official evidence and ask for a product decision; do not silently substitute a
different version.

## Evidence artifacts

Use immutable records under:

`production/engine/setup-engine/{request-id}/{run-id}/`

The declared evidence/transaction recorder is the sole writer for:

- `sources/{sequence}-{source-id}.json` — exact official-source snapshot;
- `research-manifest.json` — claim/source matrix and its canonical hash;
- `decision.json` — selection and decision provenance;
- `receipts/install.json` — installer/package transaction, when installation occurs;
- `receipts/execution.json` — real binary and SDK/toolchain execution identity;
- `receipts/project-validation.json` — project load/import/smoke evidence;
- `receipts/build-regression.json` — upgrade build/test matrix;
- `mutation-manifest.json` and `mutation-receipt.json` — authorized project transaction;
- `checkpoints/{sequence}-{phase}.json` and `result.json`.

Records use canonical serialization and SHA-256, include their schema version, stable
request/run/installation IDs, producer identity, UTC time, input/output hashes,
authorization IDs, and status. Read back every persisted record and include its hash.
An existing filename or an unvalidated old receipt is not evidence.

## Phase 1: Read-only research

Research mode and the research portion of other modes are read-only with respect to
the project and machine. Network access follows the manifest's explicit policy. Do
not download or execute an installer during research.

1. Validate the engine, edition, version constraint, platforms, region, and licensing
   context that need evidence.
2. Retrieve only eligible official sources within the deadline and source budget.
3. Verify source ownership, preserve response hashes and timestamps, and construct
   the claim/source matrix.
4. Compare candidates using sourced capabilities, lifecycle, platform requirements,
   language/toolchain constraints, installation footprint, and applicable licensing.
   Do not embed a timeless engine recommendation matrix in this workflow.
5. Mark missing/conflicting facts `UNRESOLVED`. A comparison may show bounded options
   but cannot convert unresolved facts into confidence.

Optional parallel retrieval is capped at three read-only tasks. Each gets explicit
URLs, no child delegation, a unique attempt token, and a deadline capped at 15
minutes; the total research phase is capped at 30 minutes. Permit one retry only
after proving the prior attempt made no writes/downloads. Revoke timed-out tokens and
ignore/quarantine late results.

If the request authorizes persistence of research evidence, first present its exact
record paths, hashes, recorder, and limits for one research-record authorization.
Otherwise return the canonical evidence in conversation as
`RESEARCH_EVIDENCE_READY`. This authority does not permit installation or project
configuration.

## Phase 2: Product decision

Present only candidates supported by the current evidence snapshot. For each option,
show exact edition/version/channel, support horizon, platform/toolchain constraints,
license scope/date/region, unresolved facts, and source IDs. The user named as product
authority chooses; the workflow never forces a recommendation.

Record stable decision ID, selected installation candidate, research-manifest hash,
options, rationale, decision-maker identity, UTC time, and accepted unresolved risks.
Risk acceptance does not turn an unresolved mandatory fact into confirmed evidence
and cannot authorize installation or writes.

Persisting `decision.json` requires its own exact record authorization if not already
covered. A decision is not installation consent and not project mutation consent.
State becomes `DECISION_RECORDED` only after the persisted record, when requested, is
read back and hashed.

## Authorization boundaries and ownership

Never ask for one vague up-front approval covering unknown later work. Use separate,
non-transitive authorities:

1. optional evidence-record authorization;
2. product decision authority;
3. external download/install authorization, naming URL/package, checksum/signature,
   command/installer, exact destination, privileges, disk limit, environment changes,
   timeout, cleanup and rollback;
4. execution authorization for exact binary/toolchain/project commands and working
   directories when execution is not already explicitly authorized;
5. project configuration authorization only after `INSTALLATION_VERIFIED`, covering
   final candidate bytes for every exact file and receipt;
6. upgrade migration authorization for exact isolated candidate operations;
7. upgrade activation authorization only after all current target-hash regression
   evidence passes.

Each authoritative project file has one owner and one writer. Owner approval is
required for root `AGENTS.md`, technical preferences, engine reference, project lock,
and any other declared destination. Specialist/agent instruction files are outside
this workflow; emit owner-routed proposals rather than editing them. Testing framework
selection belongs to the testing configuration owner and its authoritative catalog;
do not copy or recommend a framework name here.

The project configuration mutation manifest lists every operation, normalized path,
owner approval ID, expected base hash or `ABSENT`, candidate content hash, unique
writer, maximum bytes, commit order, rollback bytes/hash, and explicit non-writes.
Any unknown path, missing owner, changed base hash, changed candidate, or expanded
scope requires a revised manifest and new authorization.

## Required continuation

Before installation, execution, configuration, refresh, or upgrade, read
`references/continued-workflow.md` in full. It defines real execution receipts,
configuration visibility, multi-owner transaction/rollback, refresh isolation,
upgrade migration/regression, checkpoint recovery, and terminal output.
