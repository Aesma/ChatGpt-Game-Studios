# Skill Test Spec: $asset-audit

## Purpose

Verify that `$asset-audit` issues COMPLIANT only from complete executable-adapter,
rule, reference and external-status evidence for one immutable asset snapshot.
Unsupported, failed, stale or partial evidence must fail closed, and the workflow must
remain strictly read-only.

## Fixtures

Fixtures provide exact bytes and SHA-256 values for the audit manifest, inventory,
assets/import metadata, build/dependency manifests, adapter registry/executables and
receipts, rules/AGENTS/technical preferences/art direction, engine resolver, asset
manifest/specifications and expected canonical packet.

Tests snapshot every project file before/after and simulate adapter timeout, malformed
binary metadata, LFS pointers, dynamic references, budgets and concurrent source
changes.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches directory.
- [ ] Invocation requires exact manifest/run ID and validates category enum/path confinement.
- [ ] The workflow is project-read-only and never offers delete/rename/import/fix actions.
- [ ] Scope comes from one hash-bound inventory, not undeclared recursive discovery.
- [ ] Rules have stable IDs, source hashes/locators, domains, precedence, operators, severity and adapter requirements.
- [ ] Root-to-target AGENTS precedence, technical preferences and art-direction domains are deterministic.
- [ ] Cross-domain rule conflicts become UNVERIFIED rather than silent override.
- [ ] Every asset type requires a versioned executable adapter with argv, tool identity, timeout, structured schema and receipt.
- [ ] Missing/unsupported/failed/timed-out/parse-error adapter state is UNVERIFIED and coverage INCOMPLETE.
- [ ] Metadata is verified from binary/container/structured output, never extension alone.
- [ ] JSON/YAML data validation requires exact schema path/hash/version.
- [ ] Engine reference decisions require versioned resolver/build graph evidence.
- [ ] String-search absence cannot produce confirmed orphan; unsupported syntax cannot produce confirmed missing.
- [ ] POSSIBLY_ORPHANED/UNKNOWN makes reference coverage incomplete.
- [ ] Asset-spec statuses exactly include DRAFT, BLOCKED_NOT_FOR_PRODUCTION and READY_FOR_PRODUCTION.
- [ ] BLOCKED_NOT_FOR_PRODUCTION is a hard production blocker and cannot be upgraded by local PASS/risk acceptance.
- [ ] READY_FOR_PRODUCTION must be transaction/hash/validation-current and does not itself imply COMPLIANT.
- [ ] Asset compliance and GDD content completeness have separate owners.
- [ ] The output uses schema asset_audit/v2 and binds target/build/input/evidence hashes.
- [ ] Conversation output is not durable external evidence without an independently persisted receipt.
- [ ] Verdict aggregation is deterministic and incomplete coverage can never be COMPLIANT.
- [ ] Budgets and source drift produce visible PARTIAL coverage.
- [ ] Stable findings include rule/asset/evidence/adapter IDs and hashes.
- [ ] No director gate or downstream workflow is invoked.
- [ ] Metadata describes adapter-backed, read-only, fail-closed behavior.

## Case 1: Complete image adapter PASS

A PNG fixture has verified signature/header, exact dimensions/color/alpha/compression
and import metadata. The image adapter receipt and all HARD rules match.

**Expected**

Every row binds asset/rule/adapter hashes and PASS. If all other coverage dimensions
are complete and production state is current READY_FOR_PRODUCTION, COMPLIANT is
eligible.

## Case 2: Missing image adapter

The inventory contains a texture but the registry has no compatible image adapter.

**Expected**

Adapter state UNSUPPORTED, check UNVERIFIED, adapter coverage INCOMPLETE, verdict
PARTIAL. Filename `.png` and visual inspection cannot produce PASS or COMPLIANT.

## Case 3: Corrupt image metadata

The image adapter starts but reports a structured parse error.

**Expected**

PARSE_ERROR/UNVERIFIED/PARTIAL, not a format FAIL unless the adapter contract provides
a conclusive valid violation result.

## Case 4: Audio metadata

A receipt binds exact audio bytes and reports container/codec/sample rate/channels/
bit depth/duration. One HARD sample-rate rule fails.

**Expected**

NON-COMPLIANT with expected/actual/unit/rule source and receipt hash. Extension alone
is never evaluated.

## Case 5: Data schema validation

JSON and YAML fixtures use exact parser and schema path/hash/version.

**Expected**

Valid data may PASS. Missing schema, unsupported YAML feature, parser timeout or
truncated receipt is UNVERIFIED/PARTIAL. A conclusive schema validation failure is
NON-COMPLIANT.

## Case 6: Rule precedence

Root AGENTS provides a naming baseline, nested AGENTS overrides the same key,
technical preferences supplies texture budget, and art direction supplies palette.

**Expected**

The effective rows cite exact winning source hashes/locators. Domain-specific rules
coexist; overridden rules are listed. A technical/art contradiction becomes
RULE_CONFLICT/UNVERIFIED.

## Case 7: Invalid input path or symlink

Manifest contains traversal, external symlink, duplicate normalized path or
asset-hash mismatch.

**Expected**

ERROR/BLOCKED before adapters run. No external or aliased asset is inspected.

## Case 8: Budget exhaustion

The exact inventory has 1,000 items but manifest caps inspection at 200.

**Expected**

The first deterministic 200 are evaluated, 800 IDs are listed uninspected, coverage
INCOMPLETE and verdict PARTIAL unless an inspected current hard FAIL yields
NON-COMPLIANT.

## Case 9: LFS pointer and unreadable asset

One inventory path contains only an LFS pointer and another is permission denied.

**Expected**

Both are UNVERIFIED with explicit state/owner; no adapter PASS is synthesized and
verdict cannot be COMPLIANT.

## Case 10: Complete engine reference graph

Current resolver/build evidence covers every declared mechanism and proves an asset
has no inbound edge or build inclusion.

**Expected**

Reference state may be UNREFERENCED_CONFIRMED. It becomes NON-COMPLIANT only when the
hash-bound policy classifies that state HARD; no deletion is performed/recommended
without separate manual/VCS/build review.

## Case 11: Dynamic UID/addressable reference

An asset has no source-code path string but a current UID/addressable/runtime-registry
edge exists.

**Expected**

REFERENCED. Text absence cannot downgrade it or create an orphan finding.

## Case 12: Incomplete dynamic coverage

No edge is found, but one dynamic loading registry was not inspected.

**Expected**

POSSIBLY_ORPHANED, reference coverage INCOMPLETE, verdict PARTIAL, not a confirmed
orphan.

## Case 13: Confirmed missing reference

The resolver parses an exact scene/resource location and normalized asset ID; complete
inventory/build evidence proves it absent.

**Expected**

MISSING_CONFIRMED with location/resolver hashes and NON-COMPLIANT.

## Case 14: Unsupported reference syntax

A data file uses a reference syntax absent from the resolver registry.

**Expected**

UNKNOWN/PARTIAL. It cannot become MISSING_CONFIRMED or be ignored.

## Case 15: Asset-spec blocked state

Manifest/spec pair has matching hashes/transaction but status
BLOCKED_NOT_FOR_PRODUCTION with a current blocker list.

**Expected**

Production eligibility remains BLOCKED_NOT_FOR_PRODUCTION and verdict
NON-COMPLIANT for a production target, even if every local adapter check passes.
User acceptance cannot upgrade it.

## Case 16: Asset-spec READY mismatch

Manifest says READY_FOR_PRODUCTION but spec has another transaction ID, stale source
hash, NOT_RUN validation or `production_eligible: false`.

**Expected**

Production eligibility UNKNOWN, external coverage INCOMPLETE and verdict PARTIAL.
The label alone is not trusted.

## Case 17: Fully verified asset-spec READY

Manifest/spec transaction/status/hashes agree, all validations are current PASS and
inferences confirmed.

**Expected**

Production eligibility may be READY_FOR_PRODUCTION but COMPLIANT still requires every
local HARD rule, adapter, reference and coverage dimension to pass.

## Case 18: Content-audit boundary

A content-completeness consumer receives the canonical packet for the same target.

**Expected**

Asset PASS does not become SHIPPED_VERIFIED, content inclusion does not become asset
compliance, and BLOCKED_NOT_FOR_PRODUCTION remains visible. Without an independently
persisted packet path/hash/producer receipt, the conversation packet is UNVERIFIED.

## Case 19: Strict read-only mutation guard

An adapter attempts to generate import cache or modify metadata; another run suggests
deleting a confirmed orphan.

**Expected**

The mutating adapter is NOT_RUN, hashes remain unchanged, deletion is not performed,
and audit verdict reflects incomplete coverage. No changeset prompt appears.

## Case 20: Deterministic verdict matrix

Assert first-match results:

- invalid manifest/target -> ERROR;
- current HARD failure, confirmed missing, policy-hard confirmed orphan, production
  DRAFT/BLOCKED_NOT_FOR_PRODUCTION -> NON-COMPLIANT;
- otherwise any unsupported/partial/stale/unknown/not-run/parse/timeout/coverage gap
  -> PARTIAL;
- otherwise advisory failures -> WARNINGS;
- otherwise complete current PASS/N-A coverage and verified production READY ->
  COMPLIANT.

Known failures and every coverage gap remain visible regardless of precedence.

## Protocol compliance

- [ ] Every result is bound to one immutable target snapshot.
- [ ] Unsupported adapters and parse failures cannot produce COMPLIANT.
- [ ] Reference integrity uses engine/build graph evidence.
- [ ] Asset-spec production state is consumed without upgrading it.
- [ ] Content completeness remains a separate concern.
- [ ] The workflow performs zero project mutation.
