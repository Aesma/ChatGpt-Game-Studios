---
name: setup-engine
description: Research, select, verify, configure, refresh, or upgrade a game engine using hash-pinned official-source claims, real executable and toolchain health receipts, owner-safe transactions, and explicit partial/offline recovery states.
---

# Setup Engine

Establish a reproducible engine identity. A version declaration, existing directory, downloaded installer, static source scan, or user preference does not prove that an engine exists, is supported, is healthy, is configured, or was upgraded.

## Invocation

```text
$setup-engine --manifest <engine-request-path> --expect-manifest <sha256:...>
              [--resume <checkpoint-path> --expect-resume <sha256:...>]
```

Manifest path/hash are required together. Resume path/hash are optional but inseparable. Validate arguments before repository reads beyond the manifest, network access, execution, delegation, decisions, or writes. With no manifest, show usage and stop with zero side effects and no verdict. Reject unknown/repeated flags, moving aliases such as `latest`, directories, unsafe IDs, traversal, symlink/junction/reparse escapes, unsupported schema, and expected/actual hash mismatch.

The request conforms to `cgs.engine-request/v2` and contains:

- stable request/run/project IDs and mode `research | decision | configure | refresh | upgrade`;
- requested engine product/edition/channel and exact version or bounded version constraint;
- language, target platforms/architectures, locale, distribution region(s), organization/use/revenue context needed for license evaluation, and currency/date basis;
- exact first-party source allowlist, claim freshness windows, network/offline policy, source-snapshot root, retrieval deadline, and evidence budgets;
- expected executable path or bounded installation roots, expected binary hash/signature when pinned, exact version argv/parser, required SDK/compiler/runtime/package/export-template commands and locks, and project health/build/test commands;
- authoritative testing-configuration/catalog path and expected hash or explicit `UNCONFIGURED`;
- exact project/config/reference/evidence/checkpoint/receipt/transaction paths, owners, expected base hashes or ABSENT, writers, limits, and non-writes;
- product-decision, external install, command execution, project mutation, migration, activation, and recovery authorities as separate identities;
- timeout, retry, parallel-probe, rollback, offline, partial-download, and resume policy;
- for upgrade, current configured receipt, isolated candidate root, target installation, migration/import/build/regression matrix, and separate activation authority.

The manifest is a request and scope constraint, not proof of an external fact and not authorization for network, install, execution, mutation, upgrade, or recovery.

## State and completion model

Use exactly these primary states:

- `RESEARCH_EVIDENCE_READY` — sufficient current official-source evidence exists for a user decision; nothing selected/installed/configured;
- `DECISION_RECORDED` — the named user/product authority selected an evidenced candidate; no install/config authority;
- `INSTALLATION_VERIFIED` — exact binary and required toolchains passed current health receipts; project files unchanged;
- `CONFIGURED` — verified installation identity matches all committed project declarations, framework reference, visibility probe, and final receipts;
- `REFERENCE_REFRESHED` — reference evidence transaction committed without changing active engine/toolchain identity;
- `UPGRADE_PLANNED` — target research/audit exists while active identity remains unchanged;
- `UPGRADE_VERIFIED` — target installation, isolated migration/import/build/regression, activation, and post-activation health all passed on one final hash;
- `OFFLINE_EVIDENCE_ONLY` — only identified cached snapshots were usable; freshness/claim limits are explicit and no current-online claim is made;
- `PARTIAL` — safe evidence exists but required scope is incomplete;
- `BLOCKED` — authority, official evidence, identity, health, ownership, CAS, validation, or policy prevents the next transition;
- `RECOVERY_REQUIRED` — partial machine/project mutation or incomplete rollback must be resolved before any other transition.

Only `CONFIGURED` in configure mode and `UPGRADE_VERIFIED` in upgrade mode may return `Verdict: COMPLETE`. Research, decision, refresh, and offline states never return an unqualified COMPLETE. Documentation-only edits, a successful download, static search, a file's existence, or accepted risk cannot produce CONFIGURED/UPGRADE_VERIFIED.

Qualify every statement such as version available, supported, downloadable, licensed, configured, healthy, or upgraded with exact product/edition/version/channel/platform/region/as-of time and evidence/receipt hashes. Never emit an unqualified `latest`, `free`, `supported`, or `verified` claim.

## Official-source claim contract — ENGINE-P1-001/002

Every mutable external fact must come from an eligible first-party, versioned source in the request's frozen allowlist. Eligible source roles include official release archive/API, lifecycle/support policy, official download/artifact manifest, checksum/signature service, platform matrix, migration guide, and legal/license terms. Vendor-owned release repositories are eligible only with verified ownership.

Search results, snippets, mirrors, aggregators, package indexes not controlled by the vendor, forums, blogs, model memory, user recollection, and copied prior prose are discovery hints only. They cannot establish a claim.

Each `cgs.engine-official-claim/v2` record contains:

- stable claim ID/type and claim schema version;
- engine product/edition, exact normalized release version/build ID, release channel, lifecycle/support status and support horizon as of `retrieved_at`;
- platform/architecture, locale, applicable region, and claim applicability predicate;
- canonical official URL, allowlist rule ID, publisher/ownership evidence, document/API version, publication/effective date, and `retrieved_at` UTC;
- HTTP/result status, final URL and redirect chain, ETag/Last-Modified, response/content SHA-256, and preserved normalized finding;
- for download claims, exact artifact name/bytes/platform/architecture, official download URL, checksum algorithm/value and separately sourced official checksum URL/hash, or signature/certificate/notarization identity and validation policy;
- support channel and whether the artifact is preview/beta/RC/stable/LTS/archived/unsupported;
- license claim IDs when relevant;
- freshness deadline, conflicts, unavailable fields, and status `CONFIRMED | UNRESOLVED | STALE | OFFLINE_CACHED`.

“Most recent” can only mean the maximal release under the exact official archive snapshot and channel/platform predicate at `retrieved_at`; retain the archive URL/content hash and do not call it timeless/latest. Fixed training/knowledge-cutoff prose is forbidden.

A user-supplied version is a requested candidate, not evidence. Confirm exact release existence, edition/channel, support status/horizon, official download asset, platform/architecture, artifact checksum/signature, and applicable license terms. If unavailable, unsupported, archived, conflicted, or unverifiable, show the official evidence and ask the user authority to select an evidenced option or stop. Never silently substitute a nearby version/channel/edition.

Missing/mismatched checksum, invalid/untrusted signature, artifact identity conflict, ineligible redirect, or unresolved support state blocks download/install and all dependent claims. If a vendor publishes no checksum, record `CHECKSUM_NOT_PUBLISHED` with source evidence; only a manifest-declared organization policy may allow a specific signature/notarization alternative, and the exception remains explicit in every receipt.

## License/platform claim contract — ENGINE-P1-008

License, royalty, seat, revenue, funding, distribution, console/platform availability, and service-fee claims use `cgs.engine-license-claim/v1` and record:

- exact engine product/edition/version/channel and license/terms document title/version/URL/hash;
- publisher, publication/effective date, retrieved-at UTC, applicable region/jurisdiction and locale;
- organization/use category, seat/headcount basis, commercial/noncommercial/education context, distribution platform, and target platform;
- threshold amount, currency, measurement period, gross/net/funding/revenue basis, exclusions, royalty/fee rate and base, and tax treatment exactly as stated when applicable;
- user-provided applicability facts/attestation hash, with sensitive exact revenue minimized to an adequate band when possible;
- status `CONFIRMED_APPLICABLE | CONFIRMED_NOT_APPLICABLE | UNRESOLVED | NOT_PROVIDED`, conflicts, and next review date.

Never infer organization revenue, location, legal entity, platform eligibility, or license applicability. `NOT_PROVIDED`/ambiguous region/date/threshold is unresolved. Present factual source-bound information, not legal advice. A user risk acceptance cannot turn missing legal applicability into confirmed eligibility.

## Evidence and receipt root

Authorized immutable evidence belongs under:

```text
production/engine/setup-engine/<request-id>/<run-id>/
```

The sole evidence recorder owns exact paths for:

- `sources/<sequence>-<source-id>.json` and response bodies where permitted;
- `official-allowlist.json`, `research-manifest.json`, `license-manifest.json`, and `decision.json`;
- `receipts/download-install.json`, `receipts/engine-health.json`, `receipts/framework-consistency.json`, `receipts/project-visibility.json`, and upgrade receipts;
- `mutation-manifest.json`, `mutation-receipt.json`, rollback/recovery receipts;
- immutable checkpoints and `result.json`.

Every record uses canonical serialization, schema version, request/run/installation IDs, producer/tool version, source/input/output hashes, authority IDs, UTC time, and status. Read back every persisted record and retain its SHA-256. An existing filename, old receipt, timestamp, or status word is not current evidence.

Hash this `SKILL.md` and `references/continued-workflow.md` in the initial packet. Revalidate both before the continuation; mixed contract versions are BLOCKED.

## Phase 1 — Read-only research

Research is read-only with respect to the project and machine. Network access occurs only when explicitly authorized by the request/authority; installer/package downloads are not research.

1. Validate product/edition/version constraint/channel/platform/architecture/region/license context.
2. Freeze the exact source allowlist and expected claim roles before retrieval.
3. Retrieve only allowlisted first-party HTTPS sources within deadline and byte/probe budgets.
4. Verify publisher ownership, redirect eligibility, source freshness, response hash, and claim applicability.
5. Build claim/source and conflict matrices; retain unavailable/partial/offline evidence explicitly.
6. Compare only evidence-backed capabilities, lifecycle/support horizon, platform/toolchain constraints, footprint, and contextual license terms.

Read-only retrieval permits at most three parallel probes, each with exact URLs, no child delegation, unique attempt token, and at most 15 minutes; total research at most 30 minutes. One retry is allowed only after proving the first attempt made no machine/project/download mutation. Timed-out/late tokens are revoked and results quarantined.

Source conflict is not resolved by recency alone. Preserve both claims/scopes/hashes and mark dependent facts UNRESOLVED. Missing mandatory release/support/download/checksum/license/platform evidence blocks dependent decision/install/configuration.

Persisting evidence needs exact evidence-record authorization. Otherwise return the canonical packet in conversation. Research authority never authorizes installation/execution/project changes.

## Phase 2 — User-owned engine decision

Present only evidenced candidates. Each option shows exact product/edition/version/channel, release/support horizon as of a date, download/checksum/signature status, platform/toolchain constraints, license region/date/threshold context, unresolved facts, and source IDs/hashes.

The named user/product authority chooses. The workflow may compare tradeoffs but cannot silently decide. Record decision ID, exact candidate, research/license manifest hashes, alternatives, verbatim choice/rationale, decision identity/source, timestamp, and accepted unresolved risks.

Risk acceptance cannot replace mandatory checksum/signature, legal applicability, executable/toolchain health, project validation, ownership, or CAS evidence. Decision persistence has a separate exact authorization and is not install/configuration consent.

## Authorization and owner boundaries

Use separate non-transitive authorities for:

1. optional evidence persistence;
2. user/product decision;
3. external download/install and machine changes;
4. exact engine/toolchain/project-health commands;
5. project configuration transaction after `INSTALLATION_VERIFIED`;
6. refresh reference-only transaction;
7. isolated upgrade migration;
8. activation after all validation passes;
9. rollback/recovery/destructive cleanup when required.

Every authoritative destination has one named owner and one unique writer. The transaction manifest records path, operation, owner approval ID, expected base hash/ABSENT, candidate hash, rollback bytes/hash, maximum bytes, commit order, and non-writes. Unknown owner/path, changed base/candidate, writer overlap, or expanded scope requires a new manifest/approval.

Root AGENTS, technical preferences, engine reference, project engine lock/config, testing configuration reference, and evidence receipts keep their distinct owners. Do not edit specialist/role instruction files; emit exact owner-routed proposals only. This avoids bulk role-description drift. If another authorized workflow later edits them, each file still requires its own owner, snapshot hash, candidate hash, CAS, read-back, and transaction receipt.

Testing framework selection belongs solely to the authoritative testing catalog/configuration owner. This skill never copies or recommends GUT, GdUnit4, NUnit, or any framework name from memory.

## Testing-framework consistency — ENGINE-P1-004

Read only the exact manifest-declared authoritative testing catalog/configuration and expected hash. Record `UNCONFIGURED` if none exists; do not invent a default.

Configuration/upgrade candidates reference the catalog entry by stable framework/config ID, version, path, and SHA-256. The project-health/test command must come from that exact configuration, not an inline engine-specific recommendation.

Emit `cgs.engine-framework-consistency-receipt/v1` with engine/language/project config hashes, testing catalog/config path/hash/schema, framework ID/version, adapter/runner command receipt, expected/actual discovery result, and status:

- `MATCH` — declarations and current execution receipt agree;
- `UNCONFIGURED` — no authoritative selection exists; engine setup may proceed only if tests are explicitly out of configure scope, while `test_readiness: NOT_CONFIGURED` remains visible;
- `CONFLICT` — duplicated/different framework declarations;
- `NOT_RUN` — current executable test/discovery check absent.

`CONFLICT` blocks CONFIGURED/UPGRADE_VERIFIED. `NOT_RUN` blocks those states when testing is required by the manifest/upgrade matrix. Setup-engine never resolves the conflict by choosing a framework; route it to the testing owner.

## Required continuation

Before download, installation, executable/toolchain health checks, configuration, refresh, upgrade, recovery, or deterministic output, revalidate the hash-pinned [references/continued-workflow.md](references/continued-workflow.md), read it completely, and apply it. It defines installation verification, health receipts, refresh allowlist/CAS, upgrade coverage, offline/partial terminals, rollback, checkpoints, and recovery.
