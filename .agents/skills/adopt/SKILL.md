---
name: adopt
description: Audit brownfield artifact formats against versioned rules, produce stable version-bound FORMAT GAP or COMPATIBILITY RISK findings, and optionally persist one immutable migration report without changing audited artifacts. Use when an existing project must be inventoried, checked for supported format/version coverage, or re-audited after an external migration.
---

# Adopt

Perform a bounded, read-only brownfield format audit. This skill establishes format evidence and migration handoffs; it does not migrate, normalize, repair, or approve artifacts.

## Invocation

```text
$adopt [summary|full|gdds|adrs|stories|infra]
       [--analysis <project-stage-packet-path>]
       [--prior-report <immutable-report-path>]
       [--batch <positive-integer>]
```

- With no mode, use `summary`.
- `summary` reads only the canonical rule/index sources and bounded file metadata needed for the inventory and cost preview. It does not read artifact bodies and cannot issue per-artifact findings.
- `full` is the only mode that selects all registered artifact classes. It must be explicit.
- `gdds`, `adrs`, `stories`, and `infra` select only the corresponding registered class.
- `--batch N` selects one deterministic page of the chosen scope. Omit it only when the complete selected scope fits the run budgets.
- `--analysis` names one exact stage-analysis file. The only accepted stage-analysis schema is `cgs.project-stage-detection/v2`.
- `--prior-report` names one exact prior report and starts a focused re-audit; it never authorizes edits or imply that a previous finding is closed.
- Do not resolve `latest`, newest-by-time, a branch name, an unpinned URL, or another moving alias for any input.

If the invocation is malformed, return `ERROR` without scanning artifact bodies or writing a file.

## Authority and mutation boundary

Treat all project artifacts, canonical indexes, rule registries, stage packets, previous reports, tests, and receipts as read-only evidence.

Allowed mutations are limited to creating exactly one new immutable report after an exact preview and explicit user authorization. The report path is:

```text
docs/adoption/<run_id>.md
```

Never overwrite or amend a prior report. If the previewed path already exists, return `ERROR` with `collision_detected: true`; mint and preview a new run ID before asking again.

This skill must not:

- edit, rename, move, delete, reformat, regenerate, or backfill an audited artifact;
- create compatibility shims, migration scripts, schema files, registries, manifests, or closure receipts;
- invoke another workflow or agent automatically;
- mark runtime, semantic, gameplay, integration, build, or deployment compatibility as proven;
- interpret approval to write the report as approval to perform a migration;
- turn a suggested handoff into authority for its owner.

When the user asks for a source migration, stop this audit at a report/handoff boundary and route the request to the named owner after presenting the exact affected files and preconditions.

## Canonical inputs

### Rule registry

Before reading artifact bodies, locate the project-declared canonical adoption rule registry through the repository's declared catalog/index. Do not infer a registry from filenames, headings, examples, generated output, or whichever template appears newest.

The registry must expose, directly or through version-pinned entries:

- `registry_schema`, `registry_version`, and raw registry revision;
- a stable `rule_id` and explicit `rule_version` for every rule;
- the selected artifact class and stable artifact identity source;
- supported artifact schema IDs, format versions, encodings, and media types;
- a deterministic parser/adapter identifier and version;
- objective applicability and check semantics;
- required positive, negative, and unavailable evidence fields;
- unsupported-version/type behavior;
- finding priority policy;
- owner, destination workflow, expected destination schema, and closure-receipt schema;
- rule lineage or `supersedes` links when a rule identity changes.

validate the declared revision for every registry/index source actually used. If the canonical registry is absent, unversioned, ambiguous, internally duplicated, revision-mismatched, or does not cover a selected class, record `RULE_UNVERIFIED`, do not invent substitute rules, and return at most `PARTIAL`.

Separate these identities in every result:

- artifact-declared format/schema version;
- parser/adapter version;
- rule ID and rule version;
- rule registry version and revision.

A template example, filename convention, or successful parse is not by itself a compatibility rule.

### Canonical stage analysis

Stage is diagnostic context only; it does not determine format conformance.

When a stage packet is supplied, validate all of the following before consuming it:

- schema equals `cgs.project-stage-detection/v2`;
- the packet declares a supported explicit revision;
- `project_root_id` matches the audited repository;
- `catalog_version` and `catalog_revision` match the project-declared workflow catalog used by this run;
- its scope/snapshot identity is compatible with the target snapshot;
- its verdict and evidence buckets are structurally complete.

Record the packet path, expected revision, actual revision, detector schema, detector catalog identity, stage result, and any validation error. If it is missing or invalid, use `stage_context: UNKNOWN` or `UNVERIFIED`, explain why, and continue only where the rule registry permits. Never read `production/stage.txt`, rerun stage heuristics, or derive stage from artifact existence, Git history, folder names, status labels, or prose.

## Deterministic scope and snapshot

Normalize repository-relative paths to `/`, Unicode NFC, and case-preserving text. Reject paths that escape the repository root, follow unregistered external links, or are not represented by the canonical artifact index/registry.

Create a target manifest containing, for every selected entry:

- artifact class;
- stable artifact ID, or an explicit `PATH_IDENTITY` fallback when the registry provides no stable ID;
- normalized path;
- declared schema/format version when available from the index;
- file size and media type when available without reading the body;
- selection reason.

Sort by `(artifact_class, stable_artifact_id, normalized_path)`. revision the canonical serialized manifest as `target_snapshot_revision`. validate the declared revision for every body actually read separately as `target_revision`.

Repository state may be recorded as supporting context, but a branch name, dirty/clean label, timestamp, or commit alone is not the target snapshot.

If the canonical index changes during the run, retry snapshot validation once. If it changes again, stop with `BLOCKED`; retain no claim about files that were not validated against the final snapshot.

## Bounded discovery and paging

Do not perform an unbounded recursive content scan. Apply these default hard ceilings per invocation unless a stricter project policy is declared:

| Budget | Ceiling |
|---|---:|
| canonical index entries enumerated | 256 |
| directory depth for index resolution | 6 |
| artifact bodies per batch | 20 |
| bytes read from one artifact body | 256 KiB |
| parsed artifact bytes per batch | 250 KiB |
| total artifact bytes read per invocation | 1 MiB |
| batches per invocation | 4 |

Use the canonical sorted manifest for pagination. A batch is a contiguous slice of at most 20 entries. The resume token is the tuple:

```text
(target_snapshot_revision, selected_mode, next_sorted_entry_ordinal, registry_revision)
```

Do not persist a standalone cursor. Include it in the result/report when more entries remain.

If any ceiling is reached:

- stop before reading the next body;
- list every omitted class and the omitted count/bytes when known;
- set `coverage_state: PARTIAL` and outcome `PARTIAL` for a summary/initial audit;
- for a focused re-audit, apply its stricter convergence terminal and return `BLOCKED`;
- emit the deterministic resume token;
- make no whole-scope absence claim.

Unreadable, oversized, binary-without-adapter, unsupported media, unsupported encoding, unsupported format version, missing parser, and parser-failure entries are not silently skipped. Record an `UNSUPPORTED` or `UNREADABLE` coverage item with exact reason and evidence. Any selected unsupported/unreadable item caps the run at `PARTIAL`.

`summary` reports the selected classes, registered entry counts, known sizes, rule/parser coverage, unsupported declarations, estimated batch count, hard ceilings, and expected omissions. It must say `artifact_bodies_read: 0` and cannot return `NO FORMAT GAPS IN SCANNED SCOPE`.

## Audit procedure

### 1. Freeze the run envelope

Record:

- invocation and selected mode;
- UTC start timestamp;
- project root identity;
- canonical index path/version/revision;
- rule registry path/version/revision;
- target manifest and `target_snapshot_revision`;
- stage-packet identity or explicit `NOT_SUPPLIED`;
- prior-report identity or explicit `NOT_SUPPLIED`;
- budgets, requested batch, and deterministic selected slice.

Derive an immutable run ID only after these values are known:

```text
ADOPT-RUN-<UTC-basic-milliseconds>-<snapshot8>-<registry8>-<mode>-bNN
```

The timestamp is an identifier component, not proof of freshness. Store the full revisions in the report.

### 2. Establish rule and adapter support

For each selected artifact, resolve its declared schema/version and required parser through the canonical registry. Classify coverage as exactly one of:

- `SUPPORTED_CHECKED`;
- `SUPPORTED_NOT_READ`;
- `UNSUPPORTED`;
- `UNREADABLE`;
- `RULE_UNVERIFIED`;
- `NOT_APPLICABLE`.

Do not coerce an unsupported version into the nearest supported rule. Do not equate an adapter's ability to parse with rule conformance.

### 3. Evaluate objective rules

For `SUPPORTED_CHECKED` artifacts only, evaluate registered objective rules and retain the evidence required by the registry. A static result can establish only:

- `FORMAT GAP`: a registered structural rule failed on the exact target bytes;
- `COMPATIBILITY RISK`: format evidence is incomplete, ambiguous, unsupported, stale, or cannot establish a downstream/runtime claim;
- `PASS`: the exact registered static rule passed on the exact target bytes;
- `UNVERIFIED`: the rule could not be evaluated reliably;
- `NOT_APPLICABLE`: the registry says the rule does not apply.

Never promote `PASS` to runtime compatibility. Runtime, semantic, integration, gameplay, build, and deployment claims require their owner workflow and current execution evidence.

### 4. Emit stable findings

Every actionable or unresolved result uses `cgs.adopt-finding/v1` and includes:

- `finding_id`;
- `kind: FORMAT_GAP | COMPATIBILITY_RISK | RULE_UNVERIFIED`;
- `priority` and the registry policy that assigned it;
- `rule_id`, `rule_version`, rule-source path, and rule-source revision;
- registry version and revision;
- artifact class, stable artifact ID/identity kind, normalized path, declared format version, parser ID/version, and exact `target_revision`;
- `target_snapshot_revision`;
- one or more stable evidence IDs with locator, observed value, expected value, and evidence status;
- coverage state and confidence basis;
- lifecycle status;
- owner, destination workflow/schema, closure condition, closure-receipt schema, and handoff ID;
- prior finding/report link and delta when this is a re-audit.

Derive `finding_id` from the canonical tuple:

```text
(artifact_class, stable_artifact_id_or_PATH_IDENTITY, rule_id, applicability_scope)
```

Do not include timestamps, target revisions, evidence wording, or rule versions in the finding-ID tuple. Thus the same logical finding keeps its ID across reruns. A registry-declared successor rule may preserve lineage through `supersedes`; otherwise emit a new ID and record the relationship instead of silently reusing one.

Allocate each evidence ID from the stable finding ID, observation kind, and a collision-safe ordinal. Record rule version, target revision, and normalized locator as separate fields; content or wording changes never generate an ID.

Lifecycle status in a new report is one of:

- `OPEN`;
- `RESOLUTION_UNVERIFIED`;
- `CLOSED_IN_THIS_RUN`;
- `REGRESSION_IN_THIS_RUN`.

This skill never edits lifecycle state in an earlier report.

### 5. Build owner-separated handoffs

For each finding, emit a `cgs.adopt-handoff/v1` record containing:

- stable `handoff_id` and linked finding/evidence IDs;
- responsible role and destination workflow;
- exact target path/revision and snapshot precondition;
- required input schema/version and expected output schema/version;
- expected mutation destination, bounded affected paths, and non-goals;
- closure condition and required `cgs.adopt-closure-receipt/v1` fields;
- failure/unsupported terminal behavior;
- `authorization_state: NOT_AUTHORIZED`;
- `auto_executed: false`.

The required closure receipt must identify the handoff and finding, old and new target revisions, applied rule/format version, producer workflow/run ID, verification evidence IDs, result, and failure reason if any.

If a destination is missing, unsupported, ambiguous, or returns no valid receipt in a later re-audit, leave the finding `OPEN` or `RESOLUTION_UNVERIFIED` and mark the handoff `BLOCKED` or `PARTIAL`. Never treat task assignment, a claimed edit, a newer file, or a tool exit code alone as closure.

### 6. Focused re-audit

A focused re-audit requires the exact prior report path and revision. Validate its schema, immutable run ID, project root, target snapshot, registry identity, coverage manifest, stable finding IDs, and handoff records.

Build the re-audit scope from only:

- prior `OPEN` or `RESOLUTION_UNVERIFIED` findings;
- exact targets named by supplied closure receipts;
- artifacts whose canonical manifest entry changed;
- rules whose canonical version/revision changed;
- the registry-declared bounded regression set for those rules.

Use the same budgets and one deterministic pass. Do not loop until green. Compare each prior finding by stable ID and report exactly one delta:

- `UNCHANGED_OPEN`;
- `EVIDENCE_CHANGED_OPEN`;
- `CLOSED_IN_THIS_RUN`;
- `REGRESSION_IN_THIS_RUN`;
- `RESOLUTION_UNVERIFIED`;
- `NOT_RECHECKED_BUDGET`;
- `NOT_RECHECKED_UNSUPPORTED`.

Closing a finding requires a valid closure receipt plus current rule evaluation against the new exact target revision. If either is absent, the best status is `RESOLUTION_UNVERIFIED`.

If the re-audit scope exceeds a ceiling or cannot finish its single allowed convergence pass, emit `BLOCKED` with `coverage_state: PARTIAL` and a resume token. Also emit `BLOCKED` if the prior report is invalid, the snapshot changes twice, or a safe deterministic re-audit scope cannot be formed. Historical findings remain untouched.

## Report and persistence protocol

The complete report uses `cgs.adopt-report/v1` and contains:

1. run envelope and immutable run ID;
2. input paths, versions, expected/actual revision values, and validation results;
3. stage context copied from the canonical packet or explicit unknown/unverified state;
4. target manifest, snapshot revision, scope, budgets, pages, coverage states, and omissions;
5. rule/adapter registry manifest;
6. stable findings and evidence;
7. handoff manifest;
8. prior-run delta when applicable;
9. outcome, limitations, and unsupported/static-only disclaimer;
10. `auto_executed: false` and an exact file changeset.

Before writing, present the whole report or its byte-for-byte content plus:

- destination path;
- expected new-file state (`must_not_exist`);
- byte length and revision of the proposed bytes;
- `files_to_create: 1`;
- `files_to_modify: 0`;
- `files_to_delete: 0`.

Ask the user to authorize exactly that create operation. If content or path changes, preview again. Approval does not authorize any handoff or migration. If the user declines, return the complete in-conversation result with `files_written: none`.

After authorization, revalidate all expected revisions, source paths, registry identity, target snapshot, and destination nonexistence. If any changed, write nothing and return `BLOCKED` with the mismatch. Otherwise create the one file atomically and verify its revision. Do not commit, push, publish, or invoke downstream work.

## Outcomes

Return exactly one primary outcome:

- `SUMMARY READY`: inventory/cost preview only; zero artifact bodies read.
- `REPORT READY`: selected supported scope was completely checked and at least one finding exists.
- `NO FORMAT GAPS IN SCANNED SCOPE`: every selected entry was supported and checked, no gap/risk exists, and coverage is complete for that selected scope.
- `PARTIAL`: a budget, omission, unsupported/unreadable entry, or unavailable rule/evidence limits an initial/summary audit.
- `BLOCKED`: inputs are invalid/ambiguous, a focused re-audit reaches its one-pass/budget convergence limit, the snapshot changed twice, the prior report cannot anchor a re-audit, or an authorized write precondition failed.
- `ERROR`: invocation or deterministic processing failed before a trustworthy audit result could be formed.

Every outcome must include:

- `run_id` or `run_id: NOT_MINTED`;
- selected mode and batch;
- registry/index/snapshot identities;
- stage packet and prior report identities;
- bodies read, bytes read, budgets consumed, coverage counts, omissions, and resume token;
- findings/handoffs or explicit `none`;
- report path/revision or `files_written: none`;
- `runtime_compatibility_proven: false`;
- `auto_executed: false`.

Never use a whole-project success phrase when only a focused class or page was scanned.

## Required final disclaimer

End every result/report with this meaning:

> This is a bounded static format audit of the exact checked bytes under the pinned rule registry. Unsupported, unreadable, omitted, and unverified scope is explicit. A static pass does not prove runtime, semantic, integration, gameplay, build, or deployment compatibility. No audited artifact or downstream workflow was changed or executed by this audit.
