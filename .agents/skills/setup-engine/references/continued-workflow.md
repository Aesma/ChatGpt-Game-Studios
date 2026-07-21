# Setup Engine — Required workflow continuation

This continuation is mandatory after research and decision. It never treats a file,
installer, version declaration, or static source scan as proof of a working engine.

## Phase 3: Plan or perform installation

First inspect only the exact authorized installation path/search roots. Discovery
records candidates but does not verify them. If no matching installation exists,
prepare an install plan from the selected official download/package evidence.

Before any download, package-manager call, installer execution, archive extraction,
PATH/registry/environment change, SDK installation, privilege elevation, or cleanup,
present the exact external-install manifest and obtain explicit installation
authorization. Include:

- official URL/package ID, exact version/edition/channel/platform/architecture;
- expected checksum or signature verification method and official source;
- commands/arguments, destination, privileges, environment mutations, maximum
  download/unpacked size, timeout, logs, rollback and retained artifacts;
- unique installer runner identity and explicit non-actions.

Use no interactive/default installer choices absent from the manifest. Verify the
download before execution. A missing/mismatched checksum, invalid signature,
unexpected privilege request, redirect to an ineligible domain, destination drift,
timeout, partial extraction, or installer failure is `BLOCKED`/`PARTIAL`. Do not
continue to project configuration.

Persist an install receipt only in an authorized evidence path. It records exact
artifact bytes/hash, signature result, command/exit code, destination, changed machine
state, logs/hashes, rollback result, and installed candidate paths. Download or
installer success alone does not yield `INSTALLATION_VERIFIED`.

If the user declines installation, return an exact plan and `PARTIAL`; do not claim
configuration. Never uninstall, overwrite another installation, or change global
defaults without separately naming and authorizing that destructive scope.

## Phase 4: Verify real engine identity

Use the exact candidate executable, never whichever binary appears first on PATH.
Before execution, resolve its real path and record file metadata, SHA-256, platform
signature when available, size, and modification time. Derive stable installation ID:

`ENGINST-{engine}-{normalized-version}-{binary-sha256-prefix}`.

Execute the manifest-declared version command with exact argv, working directory,
timeout, and environment allowlist. Capture:

- executable requested/resolved paths and binary SHA-256;
- command/argv, start/end UTC, working directory, OS/architecture, runner identity;
- sanitized environment allowlist hash;
- exit code/signal/timeout, exact stdout/stderr bytes and hashes;
- parsed engine product, edition, semantic/build version, channel, and build ID;
- comparison with decision, official download evidence, and expected version/hash.

Run required SDK/compiler/runtime/package commands similarly. Pin their versions and
hashes where the project language/build requires them. Do not infer toolchain health
from directory existence.

Then run a non-mutating or isolated project-load/health command with the exact binary.
If an engine necessarily imports or rewrites project files, use only the declared
isolated validation copy/cache and enumerate resulting mutations. Capture load/import
result, project identity/hash, required modules/export templates/packages/plugins,
serialization/import warnings, exit code, logs and hashes.

`INSTALLATION_VERIFIED` requires all declared commands to exit successfully, parsed
identity to match official evidence and selected version, binary hash/signature to
match policy, required toolchains/modules to be present, and receipts to be complete
and read back. A pre-existing VERSION.md, executable name, folder, project file, or
old receipt cannot satisfy the gate.

Timeout is capped by the manifest and never above 15 minutes per command or 30 minutes
for the phase. At most one retry is allowed with the same input hashes after proving
the prior attempt did not mutate authoritative project/machine state. Revoke late
attempt tokens; quarantine late logs or patches.

## Phase 5: Build candidate project configuration

Only after `INSTALLATION_VERIFIED`, construct all candidate project bytes in scratch.
The minimum authoritative identity is:

- engine product/edition and exact parsed version/build ID;
- stable installation ID, resolved executable path and binary SHA-256;
- execution-receipt path/SHA-256 and project-validation receipt path/SHA-256;
- required SDK/toolchain identities/hashes;
- project lock/config path/hash and supported platforms/language;
- research-manifest and decision-record hashes.

Write this short identity directly into the root `AGENTS.md` Technology Stack or its
existing effective fields. Never add an `@file` directive: this repository does not
expand it. A normal Markdown link may aid humans, but all agent-critical engine and
receipt identity must appear directly in effective instructions.

Update only the declared engine/language/build/asset fields in technical preferences
and project locks. Preserve unrelated preferences. Reference documents separate:

- `Active Engine Identity`, bound to real installation and receipts;
- `Available/Researched Versions`, bound to official source snapshots;
- dated license/platform/support claims with region/scope/source IDs;
- no LLM training-cutoff risk score and no unsupported `latest` claim.

Do not edit specialist agent descriptions. Route engine-specific work through direct
effective project configuration; owner-specific instruction improvements are
proposals only. Do not choose a testing framework or duplicate its name.

## Phase 6: Authorize and commit the project transaction

Present the complete project mutation manifest with every candidate hash, base hash,
owner approval, writer, record path, non-write, and rollback hash. Obtain one explicit
project-configuration authorization after all owners have approved. Installation or
decision consent cannot substitute for it.

Before commit:

1. re-hash executable, receipts, official evidence, instruction chain, all base files,
   and all candidate bytes;
2. validate that active version equals the parsed real engine version;
3. validate every destination's schema and cross-reference;
4. stage candidate and rollback bytes in the authorized transaction area;
5. prove every unique writer owns a disjoint path set.

Commit sequentially with compare-and-swap guards and atomic same-volume replacement
where supported. On any failure, stop and restore every already changed path from the
recorded exact rollback bytes, then read back and hash all restored paths. If rollback
is incomplete, return `BLOCKED — RECOVERY REQUIRED`, list exact divergent paths, and
never claim configuration. Do not silently discard unrelated concurrent user changes.

After a successful commit, enumerate all changed paths and reject any outside the
manifest. Read back every file and write a mutation receipt bound to the installation
and final project-config set hash.

## Phase 7: Prove configuration visibility and consistency

Spawn a fresh independent read-only probe that did not author the candidate files.
It must read root `AGENTS.md` as effective plain text without expanding `@file`, then
report the directly visible engine product/version/build ID, installation ID,
executable path/hash, receipt path/hash, language, build system, and project lock.

Independently re-run the exact executable version command and a bounded project health
command, then compare:

- fresh-probe identity;
- current executable binary hash and parsed version;
- execution/project-validation receipts;
- root instructions, technical preferences, engine reference, and project lock;
- final project-config set hash.

Persist the hash-bound visibility/consistency receipt through the evidence recorder.
`CONFIGURED` requires all values to agree, all files/receipts to be current and
read-back verified, no outside mutation, and rollback material recorded. File
existence, text search, or the author's own reread is insufficient.

## Phase 8: Refresh official reference evidence

`refresh` reads the currently verified active identity and only its declared official
sources. It preserves citations and previous snapshot hashes, retrieves new official
snapshots, records conflicts, and proposes exact reference/evidence changes.

Refresh must not change active engine/version, executable path/hash, project lock,
toolchain identity, root Technology Stack, source code, binaries, or machine state.
A newly available release is reported as a candidate, not activated. Authorized
reference writes use their own exact mutation manifest, owner, CAS, read-back, and
rollback. Success is `REFERENCE_REFRESHED`, not engine configured/upgraded.

Offline access, source conflict, missing official data, or retrieval timeout yields
`PARTIAL`/`BLOCKED` and retains the prior evidence unchanged. Never update only a
`Last verified` date when underlying evidence was not successfully retrieved.

## Phase 9: Upgrade plan, migration, validation, and activation

Upgrade begins from a current `CONFIGURED` receipt. Re-hash the active binary,
receipts, project config, project locks, plugins/packages, source/content set, build
inputs, and instruction chain. A stale or missing active identity blocks upgrade.

### 9.1 Research and verify target installation

Research the exact target with current official sources. Record lifecycle, supported
upgrade path, migration guides, platform/toolchain/plugin requirements, serialization
and import changes, and license applicability. Obtain a new product decision if target
facts or scope differ.

Install/download the target only through a separate target-install authorization and
verify it through Phase 4. The old active installation/configuration remains unchanged.
State is at most `UPGRADE_PLANNED`.

### 9.2 Audit and authorize isolated migration

Static deprecated-API search is one input only; it never proves low risk. The audit
must also cover project/asset serialization, import/cache changes, plugins/packages,
native extensions, SDK/compiler/runtime, build/export templates, rendering/physics
defaults, platform manifests, save/data compatibility, and build/test infrastructure.

Build an exact migration manifest for an isolated candidate workspace. Include source
snapshot/tree hash, operations, unique owners/writers, expected base hashes, candidate
workspace/output paths, build/test commands, evidence paths, non-writes, time/size
limits, and disposal/rollback plan. Obtain owner approvals and separate migration
authorization before creating or changing that workspace. Never migrate the active
project in place under a planning authorization.

### 9.3 Execute migration and real validation

Only named writers apply authorized candidate changes. Enforce CAS and mutation
allowlists. Using the exact target executable/hash, run in the isolated candidate:

1. project load/import and resource/serialization validation;
2. compile/build/export for every declared platform/configuration;
3. required automated unit/integration/smoke/regression suites from the authoritative
   project test configuration;
4. plugin/package/native-extension compatibility checks;
5. declared manual or hardware validation, or mark it `NOT RUN` and block activation.

Each receipt binds command/runner/time, candidate source/config hash, target
installation ID/binary hash, platform/config, exit code, exact logs/hashes, produced
build/artifact hash, tests passed/failed/skipped, and warnings. `UNKNOWN`, `NOT RUN`,
timeout, failure, missing receipt, or stale hash blocks activation.

### 9.4 Authorize activation last

Only after every migration/build/regression row passes on the same final candidate
hash may the workflow prepare an activation transaction. It includes applying the
approved candidate diff plus root instructions, technical preferences, reference
identity, project locks, receipts, and checkpoints as one cross-owner transaction.
Show exact operations/base/candidate/rollback hashes and obtain separate activation
authorization.

Commit with Phase 6 CAS/rollback rules. Then repeat Phase 7 visibility and consistency
checks using the target binary and run the required post-activation health/build/smoke
checks. Only fully current evidence yields `UPGRADE_VERIFIED` and
`Verdict: COMPLETE`.

If any target install, migration, import, build, regression, activation, visibility,
or rollback step fails, the active version declarations must remain old or be fully
restored. Return `UPGRADE_PLANNED`, `PARTIAL`, or `BLOCKED`; never update VERSION.md
to the target as if active and never describe the project as upgraded.

## Phase 10: Recovery and resume

Write an immutable checkpoint after research, decision, installation, execution,
candidate generation, authorization, transaction, visibility, each upgrade validation
wave, and activation. Record input/output hashes, state, authorities, owners/writers,
attempt tokens, mutations, rollback material/status, receipts, blockers, and the exact
next legal transition.

On `--resume`, validate the checkpoint chain, request/mode/engine/install IDs,
official-source freshness policy, binary/toolchain hashes, active/candidate project
hashes, authorizations, ownership, transaction state, rollback state, and late writes.
Resume only at the recorded transition. Drift makes dependent evidence stale; a
half-committed or failed rollback requires recovery before any new work.

## Phase 11: Deterministic output

Every result includes request/run/mode, precise state, selected and active engine
identities, installation IDs, executable paths/hashes, parsed version outputs,
official claim/source hashes, receipt paths/hashes, project-config set hash, owner and
authorization IDs, mutation/rollback status, build/regression matrix when applicable,
blockers, checkpoint path/hash, and exactly one legal next action.

Completion gates:

- configure: `CONFIGURED` plus current official evidence, real execution/project
  receipts, successful authorized transaction, fresh visibility probe, and consistent
  final hashes → `Verdict: COMPLETE`;
- upgrade: `UPGRADE_VERIFIED` plus target receipts, final candidate migration/import/
  build/regression evidence, authorized activation, post-activation visibility and
  health evidence → `Verdict: COMPLETE`;
- incomplete but preserved safe evidence → `Verdict: PARTIAL`;
- authority/evidence/identity/CAS/rollback failure prevents progress →
  `Verdict: BLOCKED`.

Research, decision, and refresh return their explicit named states and stop without a
configuration completion verdict. Do not auto-start another workflow, install an
unapproved component, change source code outside an authorized migration, commit,
push, or publish.
