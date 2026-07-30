# Setup Engine continuation: installation, health, refresh, upgrade, and recovery

This continuation is mandatory and revision-bound. Revalidate its previewed revision before use. It never treats a version declaration, downloaded file, source scan, or old receipt as proof of a working engine.

## 3. Download and installation transaction

Inspect only exact authorized installation paths/search roots. Discovery finds candidates but does not verify them. If no matching installation exists, build an install plan from the exact selected official release/download/checksum/signature claims.

Before any network artifact download, package-manager operation, installer, archive extraction, privilege elevation, PATH/registry/environment mutation, SDK/template/module install, overwrite, uninstall, or cleanup, show an exact external-install manifest and obtain installation authorization. Include:

- product/edition/version/channel/platform/architecture and official claim IDs/revisions;
- initial/final URL, frozen allowlist rule, permitted redirect chain, artifact filename/size, official checksum/signature source and expected identity;
- exact command/argv or installer options, working directory, destination, privileges, environment changes, cache/temp/quarantine/log paths;
- byte/time/retry limits, partial-download policy, retained artifacts, rollback/recovery and cleanup actions;
- runner/recorder identity and explicit non-actions.

Do not use interactive/default installer choices that are absent from the manifest. Download first to the exact authorized quarantine path; read its declared revision and byte length; validate the official checksum/signature before extraction/execution. An unexpected redirect/host, missing/mismatched checksum, invalid signature, different size/name/platform/architecture, new privilege request, or destination drift is BLOCKED.

Every attempt emits `cgs.engine-download-install-receipt/v1` with official claims/allowlist, request/response/redirect identity, bytes received/expected, partial-file revision, ETag/Last-Modified/range support, checksum/signature result, command/exit/time, changed machine state, logs/revisions, destination inventory, rollback status, and terminal state.

Download/install success alone is not `INSTALLATION_VERIFIED`. Declined authority returns PARTIAL and an exact plan. Never overwrite/uninstall another installation or change global defaults without an exact destructive manifest and separate approval.

## 4. Executable and toolchain health receipt — ENGINE-P1-005

Use one exact candidate executable, never the first binary on PATH. Resolve its
real path without following an unauthorized escape. Record requested/resolved path,
file type/size/mtime, explicit installation revision, platform code signature/
notarization/certificate when available, owner/permissions, installation root, and
source install receipt.

Use declared identities:

```text
installation_id = ENGINST-<engine>-<normalized-version>-<installation-sequence>
health_run_id = ENGHEALTH-<installation-id>-<utc-run-id>
```

Execute the manifest-declared version command using exact executable/argv, working directory, sanitized environment allowlist, and timeout. Capture start/end UTC, runner identity, OS/architecture, exit/signal/timeout, exact stdout/stderr bytes/revisions, parser ID/version, parsed product/edition/semantic and build version/channel/build ID, and comparison to official claim/decision/download identity.

Run every required SDK/compiler/runtime/package manager/export-template/module command similarly. Each tool entry records real executable path/revision, exact version output/revision, lock/manifest path/revision, required vs actual version, command receipt, health state, and incompatibility reason. Directory presence never proves health.

Run a bounded non-mutating project-load/health command with the exact engine binary. If import/cache/project rewrites are unavoidable, use only an authorized isolated copy/cache and enumerate every mutation. Record project/config/source revision, plugin/package/native extension/export-template/module manifests, import/serialization warnings, command result/log revision, and generated-output manifest.

Emit immutable `cgs.engine-health-receipt/v1` containing all identities above, official-claim/research/decision/install revisions, framework-consistency receipt/revision, command receipts, and status:

- `HEALTHY` — every required current command/lock/module/project check matches;
- `DEGRADED` — optional capability absent while required configure scope remains valid and limitation is explicit;
- `UNHEALTHY` — required mismatch/failure;
- `NOT_RUN` — current execution evidence missing;
- `STALE` — binary/toolchain/project/config bytes changed after receipt.

`INSTALLATION_VERIFIED` requires HEALTHY (or manifest-permitted DEGRADED only for explicitly optional capabilities), matching binary/checksum/signature/version/support identity, complete required toolchain locks/receipts, valid project health, current framework state, read-back receipt revision, and zero outside mutation. File/folder/VERSION existence and prior stdout do not count.

Each command is at most 15 minutes; health phase at most 30 minutes. Permit one retry with identical input revision only after proving the prior attempt made no unauthorized mutation. Revoke tokens and quarantine late output.

## 5. Build directly effective project configuration

Only after INSTALLATION_VERIFIED, render candidates in scratch. Active identity includes product/edition, parsed exact version/build/channel, installation ID, resolved executable/revision/signature, engine-health/execution/project-validation receipt paths/revisions, SDK/toolchain locks/identities, project engine lock/config revision, framework catalog/config reference and consistency status, supported platforms/language, and research/decision revisions.

Write required short identity directly into the root AGENTS Technology Stack/effective fields. Never add an `@file` directive; links are supplementary only. Preserve unrelated technical preferences and config fields.

Engine reference separates:

- `Active Engine Identity` bound to real HEALTHY receipts;
- `Researched/Available Candidates` bound to official snapshots, not active;
- support/lifecycle claims with channel/as-of/retrieved-at/source revision;
- license/platform claims with exact region/date/version/currency/threshold applicability;
- offline/stale/unresolved limitations.

Do not edit role/specialist descriptions. Do not name/choose a testing framework; reference only the authoritative testing config identity or UNCONFIGURED state.

## 6. Cross-owner CAS transaction — ENGINE-P1-007

Before project writes, present one complete mutation manifest with every exact path, operation, owner approval, base revision/ABSENT, candidate bytes/revision, unique writer, maximum bytes, commit order, rollback bytes/revision, receipt path, and non-write. Obtain configuration authorization only after all owners approve.

Role/specialist files are outside the allowed mutation set. If owner proposals are emitted, they contain target owner, exact base revision, suggested candidate/revision, rationale, and `authorization_state: NOT_AUTHORIZED`; setup-engine does not apply them.

Immediately before commit:

1. Revalidate binary/health/framework receipts, official source/license manifests, skill/reference contract, and all bases/candidates;
2. verify active declaration equals parsed HEALTHY engine/toolchain identity;
3. validate schemas and cross-references;
4. ensure disjoint writer ownership;
5. stage exact candidate/rollback bytes in authorized same-volume transaction paths.

Use CAS and atomic replacement where supported. Precommit drift changes nothing and returns BLOCKED. On mid-commit failure, stop and restore every changed path from exact rollback bytes, then read back all restored revisions. Never overwrite/revert an unrelated concurrent edit.

If full rollback succeeds, emit `ROLLED_BACK` and retain a recovery receipt. If incomplete, return `RECOVERY_REQUIRED`, list exact expected/actual/divergent paths/revisions, freeze all configuration/refresh/upgrade work, and require an explicit recovery plan/authority. Never claim configured while split state exists.

After success, reject outside-manifest mutations, read back every file, and emit a mutation receipt bound to installation/health/framework and final project-config-set revision.

## 7. Independent visibility and framework consistency

Use a fresh independent read-only probe that did not author candidates. It reads root AGENTS as literal effective text without expanding `@file` and reports visible product/version/build/channel, installation ID, executable/revision, health receipt/revision, language/build system, project lock/config, and authoritative testing-config reference/revision.

Re-run exact version and bounded project-health commands, and when required run the authoritative testing catalog's discovery/canary command. Recompute `cgs.engine-framework-consistency-receipt/v1`; setup-engine never changes the selected framework.

Compare root instructions, technical preferences, engine reference, project lock/config, health receipt, binary/toolchain locks, framework config/receipt, and final config-set revision. Persist `cgs.engine-project-visibility-receipt/v1`.

CONFIGURED requires all required values to agree, current HEALTHY execution evidence, framework status MATCH or explicitly scoped UNCONFIGURED, read-back verified transaction, no outside mutation, and viable rollback/recovery receipts. Text search/file existence/author self-review is insufficient.

## 8. Reference refresh with frozen source allowlist and CAS — ENGINE-P1-006

Refresh begins from an exact active identity/reference/research snapshot. Freeze `cgs.engine-official-allowlist/v1` containing exact HTTPS scheme, eligible publisher, exact host or safely delimited subdomain rule, permitted path/API template, source role, product/edition/channel/platform applicability, allowed redirects, retrieval byte/time limits, and ownership evidence.

Do not broaden the allowlist during retrieval. A newly discovered host/URL is an unresolved proposal requiring a new manifest/authority; it cannot support the current refresh. Reject downgrade to HTTP, deceptive suffix hosts, URL shorteners, mirror/CDN not explicitly authorized, authentication/token-bearing URLs, and cross-host redirects outside rules.

Retrieve each prior claim only from its frozen allowed source role. Preserve prior snapshot bytes/revisions/citations and create a superseding claim linked by previous claim/source revision; never rewrite history or drop a conflicting citation. Compare publication/effective/retrieved dates, ETag/explicit revision, scope, support channel, platform/region, checksum/signature, and license thresholds.

Before any reference/evidence write, show exact sources/results, conflict matrix, candidate/base/rollback revisions, owner/writer, and one reference-only transaction. CAS all reference and evidence bases immediately before commit; read back and verify schema, ID, and revision after. Refresh may not change active engine/version/build, executable/revision, installation/health/toolchain/framework identity, root Technology Stack, project lock, source, binary, or machine state.

An available new release is `CANDIDATE_ONLY`. A conflict, offline source, missing mandatory response, timeout, stale cached source, ineligible redirect, or CAS drift leaves prior reference unchanged and returns PARTIAL/BLOCKED/OFFLINE_EVIDENCE_ONLY. Never update a “last verified” date without successful eligible retrieval and persisted source revision. Successful reference-only transaction returns REFERENCE_REFRESHED, never configured/upgraded COMPLETE.

## 9. Upgrade coverage — ENGINE-P1-003

Upgrade starts only from current CONFIGURED/health/visibility receipts. Revalidate active binary, toolchain/framework receipts, project config/lock, plugins/packages/native extensions, source/assets/content/serialization inputs, build/test infrastructure, and instruction chain. Stale active identity blocks upgrade.

### 9.1 Research and verify target

Research exact target release/support/download/checksum/license/platform claims under current allowlist policy. Record official supported upgrade path and migration guides. Verify target installation through Sections 3–4 under separate authority. Old active identity remains unchanged; state at most UPGRADE_PLANNED.

### 9.2 Comprehensive isolated audit

Static deprecated-API search is one limited input and cannot produce a low-risk or compatibility conclusion. The audit matrix includes:

- source/API/compiler changes;
- project and asset/resource serialization/import/cache changes;
- plugins/packages/native extensions and their locks;
- SDK/compiler/runtime/export templates/modules;
- rendering/physics/audio/input/network defaults;
- platform manifests, signing/export/packaging;
- save/data/network compatibility;
- build/test infrastructure and authoritative framework consistency;
- manual/hardware/platform validation required by scope.

Every row has applicability predicate, owner, input revision, target version/toolchain, planned command/check, expected receipt, and mandatory/optional state. UNKNOWN, unsupported, missing owner, or no safe check remains unresolved and blocks activation when mandatory.

### 9.3 Isolated migration and validation

Render exact candidate-workspace migration manifest with source snapshot/tree revision, paths/operations/base/candidate revision, owners/writers, target executable/toolchain/framework identity, build/test commands, evidence paths, time/size limits, non-writes, disposal and rollback. Obtain separate migration authority before workspace creation/write. Never migrate active project in place.

On one final candidate revision, run target project load/import/serialization; each platform/config build/export; authoritative unit/integration/smoke/regression; plugin/package/native compatibility; and declared manual/hardware checks. Receipts bind command/runner/time, source/config revision, target installation/binary/toolchain/framework, platform/config, exit/result, logs/artifacts revisions, pass/fail/skipped/warnings.

`NOT_RUN`, `UNKNOWN`, skip of mandatory coverage, timeout, failure, stale revision, unsupported serializer/plugin/platform, or missing receipt blocks activation. Static absence of deprecated APIs never overrides these states.

### 9.4 Activate last

Only every mandatory row PASS on the same final revision permits an activation preview. It atomically applies candidate diff plus root instructions, preferences, reference identity, locks/config, framework reference, receipts/checkpoints. Obtain separate activation authority after evidence exists.

Commit under Section 6, then repeat Section 7 and required post-activation health/build/smoke checks. Only current evidence yields UPGRADE_VERIFIED/COMPLETE. Any failure retains/restores old active declarations and returns UPGRADE_PLANNED/PARTIAL/BLOCKED/RECOVERY_REQUIRED; never advance version documents alone.

## 10. Offline, partial download, timeout, and recovery — ENGINE-P1-009

### Offline research

When network is unavailable or denied, use only exact cached official snapshots named by path/revision and validate their original URL/publisher/document version/retrieved-at/freshness deadline. Mark each `OFFLINE_CACHED` or `STALE`. Do not say current/latest and do not silently fall back to memory/nonofficial sources.

If cached evidence satisfies the request's freshness/applicability policy, return OFFLINE_EVIDENCE_ONLY with explicit claim ceiling. Missing/expired mandatory release/support/checksum/license/platform evidence blocks decision/install/refresh. Offline refresh writes nothing and preserves dates/revisions.

### Partial download/install

A partial artifact stays in the authorized quarantine path and is never extracted/executed. Receipt records bytes expected/received, partial revision, ETag/Last-Modified, range support, URL/allowlist, timeout/error, destination state, and whether safe resume is vendor/protocol supported.

Recovery offers exact options: resume only with same artifact identity/ETag/range/checksum policy; restart into a new authorized quarantine file; retain for diagnosis; or delete via separate exact cleanup authorization. Do not append when identity changed, execute partial bytes, or call partial install verified.

### Checkpoint and terminal recovery

After each research, decision, download/install attempt, health check, candidate generation, authorization, transaction step, visibility check, refresh, migration wave, activation, rollback, and recovery, create an immutable authorized checkpoint with all input/output revision, authorities, attempt tokens, state, mutations, rollback material/status, blockers, and exact next legal transition.

On resume validate the entire checkpoint chain, request/mode/IDs, contract revisions, allowlist/source freshness, binary/toolchain/framework/project identities, bases/candidates, authorities, partial artifacts, late outputs, and rollback state. Resume only at the recorded transition. Drift invalidates dependent receipts and authorization.

A failed/half transaction or rollback enters RECOVERY_REQUIRED. Before new research/config/refresh/upgrade, present exact divergences and a recovery manifest with owner, operation, expected current revision, desired restore/complete revision, evidence preservation, rollback and verification; obtain recovery authorization. Never guess, delete partial state, or continue configuration around it.

## 11. Deterministic output

Every result includes request/run/mode, exact state/verdict, selected/active identities, official claim/license/allowlist/research revisions, installation/binary/toolchain/framework/health/project/config identities, command and receipt paths/revisions, owner/authority IDs, mutation/rollback/recovery/partial-artifact states, upgrade coverage matrix, checkpoint revision, limitations, and exactly one legal next action.

Completion gates:

- configure → CONFIGURED plus current official/license evidence, HEALTHY execution/toolchain/project receipts, framework consistency, authorized transaction, independent visibility, matching revisions;
- upgrade → UPGRADE_VERIFIED plus target official/health receipts, complete final_revision migration/import/build/regression matrix, authorized activation, post-activation visibility/health;
- safe incomplete evidence → PARTIAL or OFFLINE_EVIDENCE_ONLY;
- authority/evidence/identity/policy/CAS failure → BLOCKED;
- half mutation or failed rollback → RECOVERY_REQUIRED.

Do not auto-start another workflow, install an unapproved component, mutate outside an exact transaction, commit, push, or publish.
