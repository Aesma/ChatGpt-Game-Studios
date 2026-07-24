# Asset Audit Continued Workflow

Execute these phases in order. All phases are project-read-only. Stop at the first
terminal execution error and never invoke another project workflow.

## Phase 0 — Parse and load contracts

1. Parse the closed invocation grammar.
2. Resolve one canonical project root and one project-relative regular manifest.
3. Read the main SKILL and both private references completely.
4. Reject unsafe/ambiguous/unsupported input as `ERROR — INVALID INVOCATION`.
5. Capture a pre-read mutation snapshot for manifest/instruction locations.

On failure, return usage/non-evidence diagnostics only and stop.

## Phase 1 — Validate and lock one audit manifest

1. Read manifest raw bytes once; enforce the 1 MiB cap and compute SHA-256.
2. Parse `cgs.asset-audit-manifest/v1` with duplicate-key detection.
3. Resolve literal/real paths without following symlinks/junctions.
4. Validate unique stable target/build/artifact/platform/configuration and every
   declared source path/hash/schema/relationship.
5. Load inventory plus its versioned completeness receipt and verify all stable
   asset IDs/paths/hashes/types/import/LFS/provenance/license fields.
6. Reject scope identity/path/hash/schema conflicts before adapters run.

Never infer latest/current inputs or recursively discover undeclared asset roots.

## Phase 2 — Build bounded manifests and one-pass indexes

1. Apply fixed limits; manifest values may only lower them.
2. Sort and hash the complete candidate identity stream.
3. Retain bounded rows and exact overflow counts, boundary keys, and omitted
   sequence digests.
4. Build inventory, rule, adapter, provenance, license, production, and reference
   indexes once.
5. Emit aggregate OVER_LIMIT coverage for uninspected entries; do not sample or
   partially judge them.

Any overflow prevents COMPLIANT unless a conclusive HARD failure already controls
NON-COMPLIANT; the gap still remains visible.

## Phase 3 — Resolve effective rules

1. Load root-to-target applicable `AGENTS.md` paths/hashes.
2. Load technical preferences, art direction, provenance/license policy, and
   explicitly advisory fallbacks.
3. Normalize stable rule records and apply same-key instruction precedence.
4. Keep distinct domains co-applicable; detect unresolved contradictions.
5. Record effective, overridden, duplicate, and conflicting rules with provenance.

Missing/invalid/ambiguous required rules/operators/owners/sources/adapters make
coverage incomplete. Do not ask a specialist, use memory, or invent a default.

## Phase 4 — Validate adapter and resolver registries

1. Validate adapter/resolver IDs, versions, executable/parser/normalizer hashes,
   supported engines/platforms/types/schemas/operators/syntaxes, typed argv,
   sandbox/no-network policy, time/output caps, result schemas, and cleanup.
2. Confirm OS-level project-read-only isolation before any execution.
3. Mark incompatible/mutating/unsupported contracts NOT_RUN/UNSUPPORTED; do not
   substitute shell strings, extension guesses, visual judgment, or new parsers.
4. Construct the planned check matrix from selected assets/rules/channels.

## Phase 5 — Run typed checks once

For each deterministic selected asset/rule pair:

1. revalidate asset/import/rule/adapter/target hashes and signature;
2. run only the registered argv inside the declared read-only sandbox and bounds;
3. capture `cgs.asset-adapter-receipt/v1` plus before/after snapshots;
4. validate receipt binding/schema/result/log digests;
5. compare typed expected/actual values with the registered operator; and
6. emit PASS, conclusive FAIL, UNVERIFIED, or evidence-backed N/A.

Preserve independent current evidence after timeout/parse/unsupported gaps. Never
turn adapter failure into a rule failure or clean result.

## Phase 6 — Evaluate provenance and license policy

1. Validate exact `cgs.asset-provenance/v1` rows and acyclic derived-parent chains.
2. Validate exact `cgs.asset-license/v1` rows, approved policy/rule/adapter,
   target/territory/time/derivative/redistribution scope, and obligation evidence.
3. Distinguish conclusive prohibited/expired/unmet HARD obligations from unknown,
   missing, unsupported, or conflicting records.
4. State that policy results are evidence under the named policy, not legal advice.

Never infer origin/rights from path, URL, extension, project location, or memory.

## Phase 7 — Resolve engine references

1. Match exact engine/version/target to the registered resolver.
2. Verify every declared static/dynamic/native syntax and parser/normalizer.
3. Validate current build/dependency/inventory hashes.
4. Parse locations to normalized asset IDs and emit exact graph edges/receipts.
5. Prove mechanism coverage before classifying each asset/reference.
6. Apply REFERENCED, UNREFERENCED_CONFIRMED, POSSIBLY_ORPHANED,
   MISSING_CONFIRMED, or UNKNOWN exactly.

String search is advisory. Unsupported syntax/dynamic/packed coverage is UNKNOWN
or POSSIBLY_ORPHANED, not a confirmed orphan/missing asset. Never recommend or
perform automatic deletion.

## Phase 8 — Consume production state and preserve ownership

1. Rehash exact asset manifest/spec/transaction/validation inputs when applicable.
2. Accept READY_FOR_PRODUCTION only under its complete current contract.
3. Preserve DRAFT/BLOCKED_NOT_FOR_PRODUCTION as HARD production-target failures.
4. Mark missing/stale/mismatched state UNKNOWN/incomplete rather than upgrading it.
5. Keep content completeness outside scope; do not emit SHIPPED_VERIFIED or invoke
   content-audit.

## Phase 9 — Normalize findings and coverage

1. Build stable AAF fingerprints from stable logical IDs only.
2. Attach current evidence, severity from the effective rule, owner, limitation,
   status, and objective closure condition.
3. Deduplicate only identical full fingerprints; conflicting evidence forces a
   coverage conflict.
4. Emit one bounded coverage row for every required candidate/channel/check.
5. Require current positive evidence for NOT_APPLICABLE.

## Phase 10 — Revalidate immutable snapshot

1. Re-enumerate declared roots and rehash every locked project input.
2. Compare asset/import/cache mutation snapshots.
3. Mark added/removed/renamed/changed inputs STALE and discard affected old-byte
   conclusions without mixing snapshots.
4. If this run or an adapter actually mutated the project, return execution ERROR
   with no evidence envelope. Do not revert, repair, clean, or blame.

## Phase 11 — Aggregate deterministically

Apply the exact first-match table in `evidence-contracts-v1.md`: execution error,
current conclusive HARD failure, incomplete/unknown coverage, advisory failure,
then fully proven compliance. Preserve known findings and all gaps regardless of
which row controls.

`--summary` must retain identical machine target, input hashes, manifest/overflow,
rule precedence, coverage, state sets, finding IDs, limitations, verdict, and
payload/envelope hashes.

## Phase 12 — Construct and return evidence

1. Build canonical `cgs.asset-audit-report/v1` under `cgs.asset-audit/v3`.
2. Recompute every artifact, manifest, receipt, payload, and envelope hash.
3. Wrap it in `cgs.review-evidence/v1`; on any construction mismatch return
   `ERROR — EVIDENCE CONSTRUCTION FAILED` with no record.
4. Mark conversation output not durable/not persisted.
5. Return at most one owner-specific recommendation from current evidence.
6. State scope/content/license/mutation disclaimers and stop.

Every non-error result states `allowed_project_write_set: []`,
`report_persisted: false`, `recorder_invoked: false`, and
`mutation_authorized: false`.

Do not write a report, update catalog status, invoke a recorder/owner/specialist/
gate/downstream skill, or execute the recommendation.
