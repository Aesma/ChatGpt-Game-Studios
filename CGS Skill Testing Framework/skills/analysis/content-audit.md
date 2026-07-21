# Skill Test Spec: $content-audit

## Skill Summary

$content-audit is a strictly read-only analyzer. It compares stable content requirement IDs from authoritative GDD inventories with current target build-inclusion evidence. It never treats files or directory counts as shipped content. Its deterministic verdicts are COMPLETE, GAPS FOUND, MISSING CRITICAL CONTENT, and PARTIAL. It returns schema content_audit/v2 in conversation and never writes a report or invokes another workflow.

---

## Static Assertions (Structural)

Verified automatically by $skill-test static; no fixture is required.

- [ ] YAML frontmatter contains only name and a non-empty description; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains COMPLETE, GAPS FOUND, MISSING CRITICAL CONTENT, and PARTIAL
- [ ] Declares the analyzer strictly read-only and forbids report writes, mutation approval prompts, director gates, and downstream skill invocation
- [ ] Requires full reading of all in-scope authoritative requirement sources rather than keyword pre-selection
- [ ] Requires stable requirement IDs and current target build-inclusion evidence
- [ ] Classifies bare file or folder presence as PRESENT_UNVERIFIED
- [ ] Forbids file counts, glob totals, and editor/test fixtures from proving shipped content or COMPLETE
- [ ] Defines a deterministic fail-closed verdict order
- [ ] Emits content_audit/v2 with source hashes, coverage, explicit ID sets, and per-ID evidence
- [ ] Keeps format and pipeline compliance under the asset-audit owner
- [ ] Routes quick-design only by structural risk, never by gap size or work-hour estimates
- [ ] States that a quick-design result is a proposal and becomes authoritative only after a separate approved application updates the canonical artifact
- [ ] Has one role-owned next-action handoff and does not invoke it

---

## Director Gate Checks

None. Content-audit is read-only and never invokes director gates, regardless of review mode.

---

## Test Cases

### Case 1: Complete only with IDs and build evidence

Fixture:

- The authoritative inventory defines enemy.grunt, enemy.sniper, enemy.tank, and enemy.boss.
- A current versioned target manifest contains included=true records for all four IDs and required variants.
- All requirement and manifest sources are readable, valid, hash-bound, and unchanged during the run.

Input: $content-audit

Expected behavior:

1. All four requirements are normalized by stable ID.
2. All four enter shipped_verified_ids.
3. missing_ids, present_unverified_ids, and conflict_ids are empty.
4. Both coverage dimensions are COMPLETE.
5. Verdict is COMPLETE.

Assertions:

- [ ] COMPLETE requires every specified ID to be SHIPPED_VERIFIED
- [ ] Each row cites requirement and implementation source hashes
- [ ] The result is returned only in conversation
- [ ] No file is written and no other skill is invoked

---

### Case 2: P0 regression — fixed COMPLETE cannot mask a gap

Fixture:

- Complete requirement and implementation coverage exists.
- enemy.grunt and enemy.sniper are included.
- ordinary requirement enemy.boss is explicitly absent from the current target manifest.

Input: $content-audit

Expected behavior:

1. enemy.boss appears in missing_ids and in the row table by name and ID.
2. The two included IDs appear in shipped_verified_ids.
3. Verdict is GAPS FOUND, not COMPLETE.

Assertions:

- [ ] A non-empty ordinary missing set deterministically produces GAPS FOUND
- [ ] The output never prints a fixed COMPLETE verdict
- [ ] The known missing ID is not hidden behind aggregate totals

---

### Case 3: P0 regression — critical gap

Fixture:

- Complete coverage exists.
- level.final_boss_arena is tagged CRITICAL and is explicitly excluded by the current target manifest.
- No other IDs are missing.

Input: $content-audit

Expected behavior:

1. level.final_boss_arena appears in missing_ids with CRITICAL provenance.
2. Verdict is MISSING CRITICAL CONTENT.

Assertions:

- [ ] Authoritative criticality controls the critical verdict
- [ ] Gap count, percentage, or estimated work does not control priority
- [ ] Verdict is not COMPLETE or ordinary GAPS FOUND

---

### Case 4: P0 regression — files are not shipped evidence

Fixture:

- GDD IDs are enemy.grunt, enemy.sniper, enemy.tank, and enemy.boss.
- Matching folders and source resources exist for all four.
- The current build/content manifest is missing.

Input: $content-audit

Expected behavior:

1. Matching files may be listed only under advisory_observations.
2. All matching IDs are PRESENT_UNVERIFIED, not SHIPPED_VERIFIED.
3. implementation coverage is INCOMPLETE.
4. Verdict is PARTIAL, never COMPLETE.

Assertions:

- [ ] Four matching folders do not produce Found=4 as verified content
- [ ] File presence cannot reduce the missing or unverified set
- [ ] Missing authoritative inclusion evidence fails closed to PARTIAL
- [ ] Editor-only or test-only resources are not counted as shipped

---

### Case 5: Named set difference

Fixture:

- The inventory specifies item.potion, item.key, and item.map.
- The current manifest verifies item.potion and item.key and explicitly marks item.map absent.
- Coverage is otherwise complete.

Input: $content-audit items

Expected behavior:

1. The stable system ID is resolved without ambiguity.
2. item.map is listed explicitly in missing_ids.
3. Verdict is GAPS FOUND.

Assertions:

- [ ] Missing identity is produced by set difference, not inferred from a numeric delta
- [ ] Rows are sorted deterministically
- [ ] Display labels do not replace stable identity

---

### Case 6: Count-only specification cannot prove completeness

Fixture:

- A GDD says there must be five enemies but supplies no stable content IDs.
- Five matching enemy folders exist.
- A manifest lists five resources but cannot map them to requirements.

Input: $content-audit

Expected behavior:

1. The numeric statement is recorded as UNIDENTIFIED_REQUIREMENTS.
2. No names or requirement IDs are invented.
3. requirement coverage is INCOMPLETE.
4. Verdict is PARTIAL.

Assertions:

- [ ] Equal aggregate counts do not produce COMPLETE
- [ ] Unknown identities are a coverage gap
- [ ] No completion percentage is calculated

---

### Case 7: Duplicate variants are not logical duplicates

Fixture:

- The inventory defines one logical ID enemy.grunt with required locales and two difficulty variants.
- Several resource files exist for those variants.
- The manifest proves all required variants are included under enemy.grunt.

Input: $content-audit

Expected behavior:

1. specified_ids contains enemy.grunt once.
2. Variant evidence is evaluated under required_variant_policy.
3. shipped_verified_ids contains enemy.grunt once.

Assertions:

- [ ] Variant files do not inflate logical item totals
- [ ] The row preserves variant-policy evidence
- [ ] A missing required variant prevents SHIPPED_VERIFIED

---

### Case 8: Incomplete or conflicting sources

Fixture:

- One GDD is unreadable.
- Another source changes hash during the audit.
- A manifest record points to a different target build.

Input: $content-audit

Expected behavior:

1. Source statuses include UNREADABLE and STALE.
2. The wrong-target record is EVIDENCE_CONFLICT.
3. Known gaps remain visible.
4. Verdict is PARTIAL.

Assertions:

- [ ] The analyzer does not mix source snapshots
- [ ] Any critical coverage failure blocks COMPLETE
- [ ] PARTIAL is explained as non-exhaustive, not harmless

---

### Case 9: Asset compliance ownership boundary

Fixture:

- Valid build evidence includes audio.jump.
- A current asset-audit evidence packet flags its format as non-compliant.

Input: $content-audit audio

Expected behavior:

1. content-audit does not rescan technical preferences or decide format compliance.
2. The external finding is shown with asset-audit ownership and provenance.
3. Build inclusion remains distinct from format compliance.

Assertions:

- [ ] Format checks are not reimplemented here
- [ ] External evidence does not substitute for build inclusion
- [ ] The handoff points to the asset-audit owner without invoking it

---

### Case 10: Strict read-only behavior in every mode

Fixture:

- Gaps exist.
- review-mode.txt contains full.
- The input is first $content-audit and then $content-audit --summary.

Expected behavior:

1. Both modes return conversation-only packets.
2. Neither mode offers or writes production reports.
3. No approval prompt, director gate, asset edit, story creation, or downstream skill execution occurs.

Assertions:

- [ ] Mutation guard holds in full, scoped, and summary modes
- [ ] Summary mode preserves verdict and coverage semantics
- [ ] There is no instruction to rerun a mode to write a report

---

### Case 11: quick-design routing uses structural risk only

Fixture:

- Gap A is a missing implementation with an adequate specification.
- Gap B requires clarification of a local display label and changes no shared contract.
- Gap C is numerically small but changes save compatibility and progression schema.

Input: $content-audit

Expected behavior:

1. Gap A routes to the production/backlog owner, not quick-design.
2. Gap B may recommend quick-design because its structural-risk screen passes.
3. Gap C does not recommend quick-design because structural risk is present, despite its small size.
4. Any quick-design output is described as a proposal, not authoritative evidence.
5. The gap remains open until a separate approved application updates a canonical artifact and a new audit snapshot observes it.

Assertions:

- [ ] Routing never uses gap count, percentage, t-shirt size, or work-hour thresholds
- [ ] Missing implementation is not mislabeled as a design task
- [ ] quick-design is proposal-only
- [ ] Only independently applied canonical changes can affect a later audit
- [ ] The recommendation is not invoked automatically

---

### Case 12: No authoritative specification

Fixture:

- The GDD directory contains mechanics documents but no authoritative Content Inventory or stable requirement IDs.
- Asset directories contain many plausible content files.

Input: $content-audit

Expected behavior:

1. Every in-scope GDD is read rather than keyword-filtered.
2. The analyzer reports NO_AUTHORITATIVE_REQUIREMENTS.
3. Asset files are advisory only.
4. Verdict is PARTIAL.

Assertions:

- [ ] No gap table invents planned identities
- [ ] No file total is interpreted as specified or complete content
- [ ] The next action belongs to the design owner

---

## Protocol Compliance

- [ ] Reads all in-scope authoritative requirement sources and records source status/hash
- [ ] Uses stable requirement IDs and a target-specific manifest or engine-adapter inclusion record
- [ ] Lists specified, shipped-verified, missing, present-unverified, and conflict ID sets
- [ ] COMPLETE is impossible when coverage is incomplete or any ID is unverified, missing, or conflicting
- [ ] Critical and ordinary missing IDs map deterministically to their verdicts when coverage is complete
- [ ] File and directory counts are advisory only
- [ ] Analyzer remains read-only and invokes no director gate or downstream workflow
- [ ] quick-design routing follows structural risk and its proposal is non-authoritative until independently applied
- [ ] Output conforms to content_audit/v2

---

## Coverage Notes

The behavioral cases require fixtures with immutable hashes and target IDs so stale, wrong-target, and current evidence are distinguishable. Report persistence belongs to a separate recorder contract and is intentionally outside this analyzer specification. The catalog result must remain blank until these cases are actually executed.
