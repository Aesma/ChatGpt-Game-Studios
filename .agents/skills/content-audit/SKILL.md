---
name: content-audit
description: "Read-only comparison of stable GDD content IDs with build-inclusion evidence, with fail-closed coverage and deterministic verdicts."
---

## Invocation and execution

Invoke this workflow as $content-audit.

Arguments: [system-id | --summary | no argument]. No argument audits every system represented by the authoritative content inventory. A system-id scopes the comparison to one stable system ID. The --summary flag changes presentation only.

This workflow is a strictly read-only analyzer. It may read project artifacts and return results in conversation, but it must not create, edit, delete, rename, stage, commit, or publish any file. It must not offer a report-writing branch, request write approval, invoke a director gate, or invoke another project skill.

Use the target snapshot captured in Phase 1 throughout one run. If an observed source changes during the run, mark that source STALE and return PARTIAL rather than mixing snapshots.

---

## Phase 1 — Establish scope and requirement coverage

1. Resolve the requested system-id against design/gdd/systems-index.md when it exists. Reject ambiguous names with result ERROR. For a full audit, enumerate all authoritative system and content-inventory sources.
2. Read every in-scope GDD or structured Content Inventory in full. Do not select files through keyword, filename, summary-section, or regular-expression pre-scans.
3. For every source, record:
   - stable path or artifact ID
   - content hash
   - read status: READ, MISSING, UNREADABLE, INVALID, or STALE
   - requirement IDs contributed by that source
4. Normalize each auditable requirement into this shape:

    requirement_id
    system_id
    content_type
    display_name
    criticality: CRITICAL or ORDINARY
    required_variant_policy
    source_artifact
    source_locator
    source_hash

5. Use a stable content ID supplied by the authoritative inventory or GDD. Names may be display labels but are not identity.
6. A bare numeric statement without stable IDs is UNIDENTIFIED_REQUIREMENTS. Preserve the stated quantity and source as a coverage gap; do not invent names or IDs and do not use it to prove completeness.
7. Model localized, difficulty, platform, and cosmetic variants under their logical requirement ID according to required_variant_policy. Do not count variants as separate logical items unless the authoritative specification explicitly gives them separate IDs.
8. If any in-scope requirement source is missing, unreadable, invalid, stale, ambiguous, or only count-based, requirement_coverage is INCOMPLETE.

If no authoritative content specifications exist, return PARTIAL with the gap NO_AUTHORITATIVE_REQUIREMENTS. Do not infer planned content from asset folders.

---

## Phase 2 — Load implementation evidence

For every normalized requirement ID, seek authoritative inclusion evidence from a versioned content/build manifest or an engine adapter that proves inclusion in the target build.

A valid inclusion record contains:

    requirement_id
    logical_content_id
    target_id
    build_or_manifest_id
    included: true or false
    source_artifact
    source_locator
    source_hash
    adapter_or_schema_version

The evidence must match the target snapshot and the logical ID/variant policy. Classify each requirement as:

- SHIPPED_VERIFIED — valid current evidence proves all required content and variants are included in the target build.
- MISSING — current authoritative evidence explicitly shows the required logical item is absent or excluded.
- PRESENT_UNVERIFIED — a matching file, folder, resource, editor object, test fixture, or source definition exists, but current build inclusion is not proven.
- EVIDENCE_CONFLICT — authoritative records disagree, use an unknown schema, refer to a different target, or refer to stale hashes.

File paths, filenames, directory names, glob totals, source-code matches, asset counts, and editor/test fixtures are advisory observations only. They never establish SHIPPED_VERIFIED, never reduce the missing set, never raise confidence, and never permit COMPLETE. Editor-only and test-only content is excluded unless the authoritative target manifest explicitly includes it as shipped content.

If the target manifest is absent, unreadable, invalid, stale, unsupported, or does not cover every in-scope requirement ID, implementation_coverage is INCOMPLETE. Preserve any verified or known-missing findings, but do not fill gaps with file counts.

Format, naming, file-size, and pipeline compliance belong to asset-audit. Content-audit does not rescan or decide those rules. It may display a current, hash-bound asset-audit finding as external evidence, with its owner and provenance, but that evidence does not substitute for build inclusion.

---

## Phase 3 — Compare stable sets and determine verdict

Compute set differences by requirement_id:

- specified_ids — all normalized requirement IDs
- shipped_verified_ids — IDs classified SHIPPED_VERIFIED
- missing_ids — IDs classified MISSING
- present_unverified_ids — IDs classified PRESENT_UNVERIFIED
- conflict_ids — IDs classified EVIDENCE_CONFLICT

Counts may be derived from these explicit sets for display. Never infer identities from counts, add unmatched file totals to verified counts, or calculate completion percentages.

Use this fail-closed order:

1. result is ERROR when the requested scope cannot be resolved safely or the target itself is invalid.
2. verdict is PARTIAL when requirement_coverage or implementation_coverage is INCOMPLETE, any source is STALE, any ID is PRESENT_UNVERIFIED or EVIDENCE_CONFLICT, or the run cannot inspect all required evidence.
3. verdict is MISSING CRITICAL CONTENT when coverage is complete and one or more MISSING IDs are CRITICAL.
4. verdict is GAPS FOUND when coverage is complete, no critical ID is missing, and one or more ORDINARY IDs are MISSING.
5. verdict is COMPLETE only when coverage is complete, every specified ID is SHIPPED_VERIFIED, both missing sets are empty, and there are no conflicts, blockers, unidentified requirements, or unverified items.

Known critical or ordinary gaps remain visible even when PARTIAL takes precedence. The output must explain that PARTIAL means the audit cannot make an exhaustive verdict; it does not mean the known gaps are harmless.

Priority comes only from authoritative criticality and stable dependency edges. Do not derive priority from gap counts, percentages, directory totals, elapsed time, or estimated implementation effort.

---

## Phase 4 — Return the evidence packet

Return one conversation-only packet with schema content_audit/v2:

    schema_version: content_audit/v2
    result: OK or ERROR
    verdict: COMPLETE | GAPS FOUND | MISSING CRITICAL CONTENT | PARTIAL
    scope:
      requested_argument
      resolved_system_ids
      target_id
      snapshot_at
    coverage:
      requirements: COMPLETE | INCOMPLETE
      implementation: COMPLETE | INCOMPLETE
      sources: [{artifact, hash, status, contribution}]
      gaps: [{code, artifact, reason}]
    rows:
      - requirement_id
        system_id
        content_type
        display_name
        criticality
        implementation_state
        requirement_evidence
        implementation_evidence
        missing_reason
    sets:
      specified_ids
      shipped_verified_ids
      missing_ids
      present_unverified_ids
      conflict_ids
    advisory_observations
    external_asset_audit_evidence
    contradictions
    recommendation
    disclaimer

Each evidence reference includes a stable artifact/path, locator, hash, target ID where applicable, and classification reason. Sort rows by system_id, content_type, then requirement_id so repeated runs against the same snapshot are stable.

For --summary, return the same verdict and coverage fields plus the five ID sets; rows may be compacted but evidence must remain traceable. Summary mode is not allowed to weaken coverage rules.

The disclaimer must say that file presence is not proof of shipped content and that PARTIAL is not a completeness claim.

---

## Phase 5 — Handoff and stop

Return at most one next action, chosen by the evidence owner:

- Missing implementation with an adequate specification: recommend the production/backlog owner create or schedule implementation work. This is not a design change.
- Missing or ambiguous specification: recommend the design owner clarify the authoritative inventory.
- Asset compliance evidence: point to the asset-audit owner.
- Evidence coverage failure: point to the manifest, build, or engine-adapter owner.
- No gap: state that no follow-up is required.

Do not invoke the recommendation.

If specification repair may use quick-design, route to it only after evaluating structural risk. The route is eligible only when the proposed design change is local and does not alter shared contracts, schemas, save compatibility, networking, economy, progression, cross-system dependencies, canonical narrative, accessibility obligations, or release/platform commitments. Any such structural risk routes to the appropriate full design or architecture owner instead.

Never select quick-design because a gap is small, a count is low, the work seems short, or an hour estimate falls below a threshold. quick-design produces a proposal only. Its proposal is not authoritative content-audit evidence and does not close a gap until a separate, explicitly approved application step updates the canonical artifact and the next audit observes that applied artifact in a new snapshot.

Stop after returning the packet and recommendation. Never write an audit report or mutate project state.
