# Contract Specification: `setup-engine`

## Purpose

Validate `setup-engine` as a manifest-driven state machine that separates official-source research, user engine decision, external installation, real executable/toolchain health, project configuration, reference refresh, isolated upgrade validation, activation, and recovery. Active declarations can never lead the exact verified environment.

## Contract identities

- Request: `cgs.engine-request/v2`
- Official claim: `cgs.engine-official-claim/v2`
- License claim: `cgs.engine-license-claim/v1`
- Official allowlist: `cgs.engine-official-allowlist/v1`
- Download/install receipt: `cgs.engine-download-install-receipt/v1`
- Engine health receipt: `cgs.engine-health-receipt/v1`
- Framework consistency: `cgs.engine-framework-consistency-receipt/v1`
- Project visibility: `cgs.engine-project-visibility-receipt/v1`
- Skill: `.agents/skills/setup-engine/SKILL.md`
- Continuation: `.agents/skills/setup-engine/references/continued-workflow.md`

## Invocation

```text
$setup-engine --manifest <path> --manifest-revision <revision>
              [--resume <path> --resume-revision <revision>]
```

Required/optional path_revision pairs are inseparable. No arguments prints usage with zero network, execution, delegation, decision, or write. Reject moving aliases, directories, traversal, symlink/junction/reparse escapes, schema/revision mismatch, and unknown/repeated flags.

## P0 invariants retained

1. Research, decision, installation, health verification, configuration, refresh, migration, activation, and recovery are distinct states and authorities.
2. Critical engine identity is directly visible in effective root instructions; `@file` expansion is never relied on.
3. Documentation-only version edits cannot advance active identity or claim upgrade.
4. Exact current binary/toolchain/project receipts plus an owner-approved CAS/rollback/read-back transaction are mandatory for CONFIGURED.
5. Upgrade requires target health, isolated import/serialization/migration/build/regression, separate activation, and post-activation health on one final revision.
6. Cross-owner transaction failure rolls back fully or enters RECOVERY_REQUIRED; split state is never complete.
7. COMPLETE is legal only for CONFIGURED or UPGRADE_VERIFIED.

## P1 requirements

### A. User version existence/support/download verification — ENGINE-P1-001

1. A user-entered version is a request, never evidence.
2. Exact product/edition/release/build/channel must exist in the first-party release archive/API.
3. Support/lifecycle status and horizon are evaluated as of retrieved-at for the exact channel.
4. Exact platform/architecture download artifact, official URL, size/name, checksum/signature policy, and license applicability are confirmed.
5. Unsupported/archived/unavailable/conflicted/unverifiable versions remain unresolved; the user authority chooses another evidenced candidate or stops.
6. Nearby version/channel/edition substitution is forbidden.

### B. Versioned official-source provenance — ENGINE-P1-002

1. Every mutable external fact conforms to `cgs.engine-official-claim/v2` and comes from a frozen eligible first-party source.
2. Claim records product/edition/version/build/channel/support/horizon, platform/architecture/locale/region, canonical URL, allowlist rule, publisher ownership, document/API version, publication/effective date, retrieved-at UTC, HTTP/final URL/redirects, ETag/Last-Modified, response revision, normalized finding, freshness, and conflicts.
3. Download claims additionally bind artifact identity/size, checksum algorithm/value and official checksum source/revision, or exact signature/certificate/notarization verification policy.
4. “Most recent” is scoped to one exact official archive snapshot/channel/platform/as-of time. Unqualified latest/supported/free/verified and fixed knowledge-cutoff prose are forbidden.
5. Search snippets, mirrors, package indexes, aggregators, blogs/forums, model memory, and recollection cannot establish claims.
6. Missing/mismatched checksum, invalid signature, ineligible redirect, artifact conflict, or unresolved support blocks install/dependent claims.
7. Vendor-nonpublished checksum state is explicit and only an organization policy can permit a named signature/notarization substitute.

### C. Upgrade risk needs comprehensive execution evidence — ENGINE-P1-003

1. Static deprecated-API search is one limited input and cannot prove low risk/compatibility.
2. Upgrade matrix covers source/compiler API, project/asset/resource serialization/import/cache, plugins/packages/native extensions, SDK/compiler/runtime/templates/modules, rendering/physics/audio/input/network defaults, platform/signing/export/packaging, save/data/network compatibility, build/test infrastructure/framework, and required manual/hardware/platform checks.
3. Every row has applicability, owner, input revision, target identity, command/check, expected receipt, and mandatory/optional state.
4. UNKNOWN, unsupported, NOT_RUN, timeout, stale revision, missing owner/receipt, skipped mandatory row, or failure blocks activation.
5. Migration uses an authorized isolated candidate; active project/version remain unchanged until every mandatory row PASS on one final candidate revision and a separate activation succeeds.

### D. Authoritative testing-framework consistency — ENGINE-P1-004

1. Setup-engine reads only the exact revision-pinned authoritative testing catalog/configuration or records UNCONFIGURED.
2. It never chooses, recommends, or copies a framework name from memory/engine preference.
3. Project config references stable testing-config ID/version/path/revision; health/test command comes from that source.
4. `cgs.engine-framework-consistency-receipt/v1` binds engine/language/project revisions, testing catalog/config schema/revision, framework ID/version, adapter/runner command receipt, discovery result, and status MATCH/UNCONFIGURED/CONFLICT/NOT_RUN.
5. CONFLICT blocks CONFIGURED/UPGRADE_VERIFIED. Required NOT_RUN blocks them. Explicitly out-of-scope UNCONFIGURED may allow engine configuration only with `test_readiness: NOT_CONFIGURED` visible.
6. Framework conflict is routed to its testing owner; setup-engine does not repair it.

### E. Executable/toolchain/project health receipt — ENGINE-P1-005

1. Candidate uses exact resolved executable path, file revision/size/mtime/permissions and signature identity; PATH-first discovery is insufficient.
2. Exact version argv runs with bounded working directory/environment/timeout; receipt captures time/runner/OS/architecture/exit/signal, stdout/stderr bytes/revisions, parser/version, parsed product/version/channel/build, and official-decision comparison.
3. Required SDK/compiler/runtime/package/template/module tools each have real path/revision/version output/lock/command health receipts.
4. Project-load/health uses the exact binary and exact project/config/source identity in non-mutating or isolated mode, recording import/serialization/plugin/package warnings and logs/mutations.
5. `health_run_id` binds installation/binary, version receipt, toolchain lock/receipt set, module/template/plugin manifest, and project-health receipt.
6. `cgs.engine-health-receipt/v1` is HEALTHY/DEGRADED/UNHEALTHY/NOT_RUN/STALE; only required-current health can yield INSTALLATION_VERIFIED.
7. File/folder/VERSION/old stdout/old receipt existence has zero verification value.

### F. Refresh allowlist, citation preservation, conflict and CAS — ENGINE-P1-006

1. `cgs.engine-official-allowlist/v1` freezes HTTPS scheme, publisher, exact host/safely delimited subdomain rule, path/API template, source role, applicability, redirects, retrieval budgets, and ownership evidence.
2. Refresh cannot broaden allowlist during retrieval. Newly discovered source is an unresolved proposal requiring a new manifest/authority.
3. HTTP downgrade, deceptive suffix, URL shortener, unauthorized mirror/CDN/auth URL, and out-of-rule redirect are rejected.
4. Prior source bytes/revisions/citations are preserved; new claims link superseded claim/source revision. Conflicts remain explicit and are not resolved by recency alone.
5. Refresh previews a reference-only transaction with owner/base/candidate/rollback revisions and CAS/read-back.
6. It cannot change active engine/binary/toolchain/framework/root/project lock/source/machine state. New releases are CANDIDATE_ONLY.
7. Offline/conflict/missing/timeout/stale/redirect/CAS failure leaves prior reference unchanged; last-verified dates never advance without successful eligible retrieval and persisted source revision.

### G. Per-file owner, snapshot, CAS and role protection — ENGINE-P1-007

1. Every authoritative file has one owner approval, expected base/ABSENT, candidate revision, unique writer, rollback bytes/revision, size/commit order, CAS, read-back, and transaction receipt.
2. Changed base/candidate, missing owner, writer overlap, or expanded path invalidates authorization.
3. Precommit drift writes nothing. Midcommit failure fully restores exact rollback bytes or enters RECOVERY_REQUIRED.
4. Concurrent unrelated edits are not silently overwritten or reverted.
5. Specialist/role instruction files are outside setup-engine's mutation set. Proposals are NOT_AUTHORIZED and carry owner/base/candidate revision only.
6. Any later role-file workflow must independently enforce per-file owner/snapshot/CAS/read-back; no batch wildcard ownership exists.

### H. License region/date/version/threshold context — ENGINE-P1-008

1. Every license/platform claim conforms to `cgs.engine-license-claim/v1` and binds product/edition/version/channel plus official terms title/version/URL/revision/publisher/publication/effective/retrieved dates.
2. It records applicable region/jurisdiction/locale, use/org/seat basis, commercial/education context, distribution/target platforms, threshold amount/currency/period/gross-net-funding basis/exclusions, royalty/fee rate/base, and tax treatment when applicable.
3. User applicability facts have an attestation revision; sensitive amounts are minimized to a sufficient band when possible.
4. Status is CONFIRMED_APPLICABLE/CONFIRMED_NOT_APPLICABLE/UNRESOLVED/NOT_PROVIDED with conflicts and next review date.
5. Organization revenue/location/legal entity/platform eligibility is never inferred. Missing region/date/currency/threshold context stays unresolved.
6. Output is source-bound information, not legal advice; risk acceptance cannot manufacture applicability.

### I. Offline, partial, timeout, checkpoint, and recovery — ENGINE-P1-009

1. Offline mode uses only exact cached official snapshots with original URL/publisher/version/retrieved-at/revision/freshness; states OFFLINE_CACHED or STALE and never claims current/latest.
2. Fresh enough cached evidence yields OFFLINE_EVIDENCE_ONLY with claim ceilings. Missing/expired mandatory evidence blocks dependent decision/install/refresh; offline refresh writes nothing.
3. Partial downloads stay quarantined and are never executed/extracted. Receipt binds expected/received bytes, partial revision, ETag/Last-Modified/range support, allowlist URL, error, and destination state.
4. Recovery options are identity-safe resume, new-file restart, retain, or separately authorized exact deletion. Changed identity cannot be appended/resumed.
5. Each attempt/phase is bounded; only one proven non-mutating retry; timed-out/late tokens are revoked/quarantined.
6. Immutable checkpoints exist after every transition and bind all sources/contracts/binaries/toolchains/framework/config/authority/partial-artifact/rollback identities.
7. Resume revalidates the chain and exact next legal transition. Drift invalidates evidence/authorization.
8. Half commit/failed rollback enters RECOVERY_REQUIRED and freezes other transitions until an owner-authorized recovery manifest restores/completes exact revisions and verifies them.

## State and authority assertions

States are exactly RESEARCH_EVIDENCE_READY, DECISION_RECORDED, INSTALLATION_VERIFIED, CONFIGURED, REFERENCE_REFRESHED, UPGRADE_PLANNED, UPGRADE_VERIFIED, OFFLINE_EVIDENCE_ONLY, PARTIAL, BLOCKED, and RECOVERY_REQUIRED.

Evidence persistence, product decision, external install, command execution, project configuration, refresh, isolated migration, activation, and recovery/cleanup authorities are separate and non-transitive.

Root effective configuration directly contains short critical engine/receipt identity and never relies on `@file`. Active reference distinguishes actual installation from researched candidates and date/region-scoped support/license claims.

## Behavioral cases

### Case 1 — User version unavailable

The requested release is absent for the declared edition/platform in the official archive. It remains UNRESOLVED; no nearby substitution/install/config candidate is created. User chooses another evidenced version or stops.

### Case 2 — Current official release claim

Archive/source records exact URL/publisher/document version/retrieved-at/explicit revision/channel/support horizon/artifact/checksum. “Most recent” is qualified to that snapshot. A missing checksum/signature blocks install.

### Case 3 — Static upgrade scan appears clean

No deprecated APIs are found but a plugin, serialized asset and export template are incompatible. Upgrade stays UPGRADE_PLANNED because comprehensive mandatory rows fail; active declarations remain old.

### Case 4 — Framework drift

Project/test catalog names one framework/config while an old setup recommendation names another. Receipt is CONFLICT; setup-engine changes neither and routes the exact conflict to testing owner. CONFIGURED is blocked if test readiness is required.

### Case 5 — Binary/toolchain identity mismatch

VERSION claims X but exact binary version output/revision or compiler lock differs. Health is UNHEALTHY/STALE; no project identity changes hide the mismatch.

### Case 6 — Refresh redirect and concurrent edit

Official page redirects outside allowlist and reference base changes after preview. Retrieval is rejected; CAS writes nothing; prior citations/dates/revisions remain unchanged.

### Case 7 — Role-file batch proposal

Configure wants to update multiple specialist descriptions. All are excluded from mutation. Per-owner revision-bound proposals may be returned but are NOT_AUTHORIZED and not applied.

### Case 8 — License threshold ambiguity

Terms differ by region/revenue period and user supplies no region/band. Claim is NOT_PROVIDED/UNRESOLVED; no unqualified free/royalty conclusion is made and install decision cannot rely on applicability.

### Case 9 — Offline and partial download recovery

Cached lifecycle evidence is stale and a prior artifact is partially downloaded. Result is OFFLINE_EVIDENCE_ONLY/BLOCKED; partial bytes remain quarantined. Resume requires identical ETag/artifact/checksum/range identity or a separately authorized restart/delete.

### Case 10 — P0 regression

Documentation-only target version edit cannot upgrade. Root configuration never adds @file. Multi-owner CAS failure rolls back or enters RECOVERY_REQUIRED. Only real current receipts and independent visibility can yield CONFIGURED/UPGRADE_VERIFIED.

## Negative assertions

Any of these is a contract failure:

- trusting a user version or claiming latest/support without official retrieved-at evidence;
- downloading/executing an artifact without exact eligible URL and checksum/signature validation;
- low-risk/compatible conclusion from static source search alone;
- hardcoding or selecting a testing framework;
- health based on directory/file/version-document existence;
- refresh from an arbitrary web result, dropped prior citation, missing CAS, or active-version mutation;
- wildcard/bulk role-file edit without per-file owner/snapshot/CAS;
- license claim without version/region/effective date/currency/threshold basis;
- treating offline cache or partial download as current/installed;
- continuing past RECOVERY_REQUIRED or reusing stale authorization;
- COMPLETE outside CONFIGURED/UPGRADE_VERIFIED.

## Remediation traceability

| Finding | Closure evidence |
|---|---|
| ENGINE-P1-001 | Section A verifies requested version existence/support/download/checksum/license and forbids substitution |
| ENGINE-P1-002 | Section B defines complete first-party version/support/checksum/retrieved-at claim provenance |
| ENGINE-P1-003 | Section C requires broad final_revision migration/import/build/regression coverage beyond static API search |
| ENGINE-P1-004 | Section D uses the authoritative testing config and emits a framework consistency receipt without choosing a framework |
| ENGINE-P1-005 | Section E defines real binary/version/toolchain/project-health identity and receipt gates |
| ENGINE-P1-006 | Section F freezes the source allowlist, preserves citations/conflicts, and uses reference-only CAS |
| ENGINE-P1-007 | Section G enforces per-file owner/snapshot/writer/CAS/rollback and excludes role files |
| ENGINE-P1-008 | Section H binds license/platform claims to region/date/version/currency/threshold context |
| ENGINE-P1-009 | Section I defines offline/partial/timeout/checkpoint/resume/RECOVERY_REQUIRED terminals |

## Deterministic output

Every result reports request/run/mode, precise state/verdict, selected/active identities, official/license/allowlist revisions, installation/binary/toolchain/framework/health/config identities, receipts, owners/authorities, transaction/rollback/recovery/partial-artifact status, upgrade matrix, checkpoint, limitations, and exactly one legal next action. It invokes no downstream workflow and performs no unapproved commit/push/publish.
