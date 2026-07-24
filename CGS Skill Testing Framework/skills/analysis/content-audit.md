# Skill Test Spec: $content-audit

## Skill Summary

`$content-audit` is a strictly read-only, bounded analyzer. It reads every
in-scope requirement source in full, normalizes explicit stable content IDs,
compares them with current target/build inclusion records from a versioned
manifest or registered engine adapter, and returns one hash-bound
`cgs.review-evidence/v1` packet with a `cgs.content-audit-report/v1` extension.
It never treats files, folders, aggregate counts, editor objects, or test fixtures
as shipped content. Its deterministic verdicts are `COMPLETE`, `GAPS FOUND`,
`MISSING CRITICAL CONTENT`, and `PARTIAL`; `ERROR` is an execution result.

Contract under test: `cgs.content-audit/v3`.

---

## P1 Remediation Trace

| Audit item | Required behavior | Primary cases |
|---|---|---|
| CTA-003 | No keyword/filename preselection; bounded full-read source coverage | 2, 8, 13 |
| CTA-004 | Exact stable-ID set difference; count-only claims remain unidentified | 3 |
| CTA-005 | Asset format compliance remains owned by asset-audit | 6 |
| CTA-006 | Registered engine adapters cover declared native formats; unsupported input is PARTIAL | 4, 5, 8 |
| CTA-007 | Criticality and priority use stable IDs plus a typed dependency graph | 7 |
| CTA-008 | Per-source failure, limit, symlink, stale, and coverage paths fail closed | 8, 9, 12 |
| CTA-009 | Every mode returns only; persistence belongs to a separate recorder | 10 |
| CTA-010 | Static and behavioral assertions match the v3 contract; catalog result fields stay blank until execution | all |

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static`; no fixture is required.

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name
      matches the skill directory.
- [ ] Declares analyzer contract `cgs.content-audit/v3`, evidence envelope
      `cgs.review-evidence/v1`, and extension `cgs.content-audit-report/v1`.
- [ ] Has at least two phase headings.
- [ ] Invocation accepts exact `system:` and `target:` stable IDs plus optional
      presentation-only `--summary`, and rejects aliases, paths, globs, regexes,
      URLs, duplicates, ambiguity, and unknown arguments.
- [ ] Declares the analyzer strictly read-only and forbids writes, write approval,
      report-path selection, director gates, delegation, remediation, and
      downstream skill invocation.
- [ ] Requires all applicable `AGENTS.md` files and one frozen project/target
      snapshot.
- [ ] Requires deterministic candidate enumeration and full reads of every
      selected in-scope GDD; forbids keyword, filename, summary, regex, folder,
      and prior-report preselection.
- [ ] Defines fixed manifest, semantic byte, requirement, inclusion-record,
      dependency-edge, external-evidence, and advisory-observation limits.
- [ ] Rejects symlinks and outside-project paths, hashes exact raw bytes, includes
      excluded/failed candidates, and revalidates the locked manifest.
- [ ] Requires explicit stable requirement, logical-content, system, target,
      build, manifest, adapter, dependency, and finding IDs where applicable.
- [ ] Records count-only normative claims as `UNIDENTIFIED_REQUIREMENTS` and
      forbids invented identities or completion percentages.
- [ ] Uses `cgs.content-inclusion/v1` records from a direct manifest or registered,
      exact-version engine adapter rather than extension guessing.
- [ ] Defines `SHIPPED_VERIFIED`, `MISSING`, `PRESENT_UNVERIFIED`,
      `UNKNOWN_INCLUSION`, and `EVIDENCE_CONFLICT` exactly once per requirement.
- [ ] Forbids file counts, glob totals, editor objects, test fixtures, and file
      presence from proving shipped content or `COMPLETE`.
- [ ] Keeps format and pipeline compliance under the asset-audit owner and admits
      supplied asset-audit evidence only through a recomputed hash-bound contract.
- [ ] Uses a typed stable-ID dependency graph and forbids priority inference from
      free-form systems-index prose, counts, percentages, or effort estimates.
- [ ] Defines stable `CAU-...` finding fingerprints that exclude mutable wording,
      paths, line numbers, hashes, status, priority, run ID, and timestamps.
- [ ] Defines a per-channel/per-check coverage ledger and a deterministic
      fail-closed verdict precedence where any material coverage gap is `PARTIAL`.
- [ ] Keeps detailed manifest rows bounded while hashing the complete candidate
      identity sequence and recording exact overflow counts/digests.
- [ ] Preserves known critical and ordinary gaps when `PARTIAL` takes precedence.
- [ ] Emits all six exact ID sets and a hash-bound evidence packet; summary mode
      preserves all verdict, coverage, set, finding, and hash semantics.
- [ ] Routes at most one role-owned next action and does not invoke it.
- [ ] States that a quick-design result is proposal-only and cannot close a gap
      until separately applied to a canonical artifact and observed at a new hash.

---

## Director Gate Checks

None. Content-audit is a read-only analyzer and never invokes a director gate in
any mode or verdict path.

---

## Test Cases

### Case 1: Complete only from exact IDs and current build evidence

Fixture:

- The authoritative inventory declares stable IDs `enemy.grunt`,
  `enemy.sniper`, `enemy.tank`, and `enemy.boss` under stable system ID
  `combat-enemies`.
- The authoritative target is `win64-release` and build is `build-0042`.
- A current `cgs.content-inclusion/v1` manifest contains conflict-free
  `included: true` records for all four IDs and every required variant.
- All requirement, target, manifest, instruction, and dependency inputs are
  within limits, readable, valid, hash-bound, and unchanged.

Input: `$content-audit target:win64-release`

Expected behavior:

1. One exact-hash manifest is locked before semantic comparison.
2. All four IDs enter `specified_ids` and `shipped_verified_ids`.
3. The other four implementation-state sets are empty.
4. Every required coverage dimension is complete.
5. Verdict is `COMPLETE`.

Assertions:

- [ ] Every row cites requirement and inclusion artifact ID, locator, and SHA-256.
- [ ] `COMPLETE` requires every specified ID to be `SHIPPED_VERIFIED`.
- [ ] The evidence envelope and extension hashes recompute.
- [ ] No file is written and no other skill is invoked.

---

### Case 2: All in-scope GDDs are read without keyword preselection

Fixture:

- Three in-scope GDDs are regular files within all limits.
- The first uses the phrase “Content Inventory”.
- The second declares stable content IDs under a differently named structured
  table and contains none of the old search keywords.
- The third contains an explicit count-only normative content statement and no
  matching filename token.

Input: `$content-audit`

Expected behavior:

1. Candidate enumeration includes all three before their prose is interpreted.
2. All three are read in full exactly once.
3. The second contributes its stable IDs.
4. The third contributes an `UNIDENTIFIED_REQUIREMENTS` coverage gap.
5. Verdict is `PARTIAL`.

Assertions:

- [ ] No keyword, filename, summary, regex, asset-folder, or prior-report scan
      controls selection.
- [ ] Every source has a manifest and coverage row.
- [ ] Empty search results are never evidence that a source has no requirements.

---

### Case 3: Stable set difference and count-only claims

Fixture:

- The inventory specifies IDs `item.potion`, `item.key`, and `item.map`.
- The target manifest verifies the first two and explicitly excludes `item.map`.
- Another source states “five bonus items” but provides no stable IDs.
- Five matching folders exist.

Input: `$content-audit system:items`

Expected behavior:

1. `item.map` is the only exact ID in `missing_ids`.
2. The numeric statement is recorded with quantity, source locator, and hash as
   `UNIDENTIFIED_REQUIREMENTS`; no bonus-item IDs are invented.
3. Folder totals remain advisory and do not reduce a set.
4. Requirement coverage is incomplete and verdict is `PARTIAL`, while
   `known_missing_ids` preserves `item.map` and
   `known_gap_classification` is `GAPS FOUND`.

Assertions:

- [ ] Missing identity is produced only by exact set difference.
- [ ] Equal or unequal aggregate counts cannot prove completeness.
- [ ] No completion percentage is calculated.
- [ ] Display names never replace stable IDs.

---

### Case 4: Registered adapters handle declared engine-native data

Fixture:

- The target build uses an authoritative engine resource database containing
  packed scenes, prefab-like resources, addressable entries, and packed build
  assets.
- A registry entry binds the exact engine version, adapter ID/version, input
  schema, and `cgs.content-inclusion/v1` output schema.
- The adapter emits deterministic target/build inclusion records with full
  provenance for all required IDs.

Input: `$content-audit target:console-release`

Expected behavior:

1. The registered adapter is selected by exact metadata, not file extension.
2. Native resource kinds are judged from adapter output records.
3. Proven records may become `SHIPPED_VERIFIED`.
4. Adapter registry, schema, inputs, and output provenance appear in the manifest.

Assertions:

- [ ] Scene, prefab, resource database, addressable, and packed-asset support is
      adapter-declared rather than hard-coded or inferred.
- [ ] Adapter version and output schema are hash-bound.
- [ ] Filesystem presence alone is not an adapter result.

---

### Case 5: Unsupported or missing adapter cannot claim completeness

Fixture:

- Requirement IDs are valid and fully readable.
- Matching engine files exist.
- The engine version is outside every registered adapter range, and a packed
  resource kind has an unknown schema.

Input: `$content-audit`

Expected behavior:

1. The adapter and format channels are `UNSUPPORTED` with exact reasons.
2. Affected requirements are `PRESENT_UNVERIFIED` when exact advisory presence
   resolves, otherwise `UNKNOWN_INCLUSION`.
3. Implementation coverage is incomplete.
4. Verdict is `PARTIAL`, never `COMPLETE` or an inferred missing verdict.

Assertions:

- [ ] Unknown formats are not silently skipped.
- [ ] No extension-based fallback is used.
- [ ] Both unverified and unknown IDs remain explicit sets.

---

### Case 6: Asset compliance has one owner

Fixture:

- Valid build evidence includes `audio.jump` for the exact target.
- A supplied current asset-audit evidence envelope flags its codec as
  non-compliant and all envelope/artifact hashes recompute.
- A second supplied asset-audit record is stale.

Input: `$content-audit system:audio`

Expected behavior:

1. Content-audit does not read technical preferences or rescan asset format.
2. The current record is displayed under accepted external evidence with
   asset-audit ownership and provenance.
3. The stale record is rejected with its hash/target reason.
4. Build inclusion remains distinct from format compliance.

Assertions:

- [ ] Format, naming, file-size, import, and pipeline checks are not reimplemented.
- [ ] External evidence never substitutes for target-build inclusion.
- [ ] Missing external asset-audit evidence does not make core content coverage
      incomplete.
- [ ] The handoff may point to the asset-audit owner but never invokes it.

---

### Case 7: Stable dependency graph controls impact presentation

Fixture:

- A typed graph contains edge `dep.final-boss-arena` from stable ID
  `campaign.final-boss` to stable ID `level.final-boss-arena` with
  `kind: BUILD_BLOCKING`, `blocking: true`, and exact source provenance.
- The prerequisite is explicitly missing from the target manifest.
- Free-form systems-index prose separately calls another gap “urgent”.

Input: `$content-audit`

Expected behavior:

1. Both graph endpoints resolve by exact stable requirement ID.
2. Criticality and the typed blocking edge are preserved as `priority_basis`.
3. The free-form urgency adjective has no priority effect.
4. Dependency impact changes presentation only, not implementation state.

Assertions:

- [ ] Stable dependency IDs and source hashes are present.
- [ ] Unknown endpoints, malformed edges, or prohibited cycles are explicit
      dependency coverage gaps and force `PARTIAL`.
- [ ] Counts, percentages, elapsed time, and estimated effort never set priority.

---

### Case 8: Bounded failure and overflow ledger

Fixture:

- One GDD is unreadable, one is a symlink, one exceeds the per-source byte cap,
  and total eligible GDDs exceed the semantic-source cap.
- One manifest candidate normalizes outside the project root.
- Other bounded sources and inclusion rows are valid and include a known missing
  ordinary ID.

Input: `$content-audit`

Expected behavior:

1. The candidate ledger records `UNREADABLE`, `SYMLINK_REJECTED`, `OVER_LIMIT`,
   and `OUTSIDE_PROJECT` without following or silently dropping them.
2. The bounded prefix is selected in deterministic manifest order; the complete
   identity sequence and omitted sequence are hashed, and exact total/omitted
   counts plus first/last omitted sort keys are recorded.
3. Verified and known-missing evidence from unaffected inputs remains visible.
4. Verdict is `PARTIAL`; `known_gap_classification` remains `GAPS FOUND`.

Assertions:

- [ ] No cap is raised and no file is sampled or partially judged.
- [ ] Every detailed failure affects explicit coverage rows/checks, and candidate
      overflow has one aggregate `OVER_LIMIT` row naming all affected checks.
- [ ] A subset or sample cannot yield `COMPLETE`.
- [ ] No outside-project or symlink target is read.

---

### Case 9: Fail-closed verdict precedence preserves known gaps

Evaluate these subfixtures independently:

| Coverage | Missing state | Expected verdict |
|---|---|---|
| complete | one `CRITICAL` ID | `MISSING CRITICAL CONTENT` |
| complete | ordinary IDs only | `GAPS FOUND` |
| complete | no missing/unverified/unknown/conflict IDs | `COMPLETE` |
| incomplete | known critical and ordinary missing IDs | `PARTIAL` |
| incomplete | no known missing IDs | `PARTIAL` |

Assertions:

- [ ] The first matching precedence rule is used mechanically.
- [ ] `PARTIAL` reports `known_missing_ids`, `known_missing_critical_ids`, and
      `known_gap_classification` rather than hiding proven gaps.
- [ ] `PARTIAL` is explained as non-exhaustive, not harmless.
- [ ] An empty requirement set never yields `COMPLETE`.

---

### Case 10: Analyzer and recorder remain separate in every mode

Fixture:

- Gaps exist.
- A project preference requests full review reports on disk.
- Run full, scoped, target-specific, and `--summary` invocations.

Inputs:

```text
$content-audit
$content-audit system:items
$content-audit target:win64-release
$content-audit system:items target:win64-release --summary
```

Expected behavior:

1. Every mode returns one conversation-only packet.
2. No mode offers, selects, creates, or writes a report path.
3. Summary compacts only the human projection; manifest, coverage, verdict, six
   sets, known gaps, finding IDs, and hashes match the equivalent full run.
4. No approval prompt, director gate, delegation, edit, story creation, or
   downstream skill invocation occurs.

Assertions:

- [ ] Read-only mutation guard holds in all modes and verdict paths.
- [ ] Persistence is described only as a separately invoked recorder operating
      on the exact returned bytes.
- [ ] There is no instruction to rerun a mode to write a report.

---

### Case 11: Stable finding identity and hash-bound evidence

Fixture:

- Run A contains one ordinary missing ID with complete exact-hash evidence.
- Run B moves the source to a different canonical path and changes wording and
  line numbers without changing stable project, source artifact, target,
  requirement, dependency, or issue identity.
- Run C changes the logical requirement ID.

Input: `$content-audit target:win64-release`

Expected behavior:

1. Runs A and B produce the same `CAU-...` finding ID but distinct artifact
   hashes and manifest hashes.
2. Run C produces a different finding fingerprint and ID.
3. Extension, payload, envelope, manifest, and every artifact hash recompute.
4. Any incompatible evidence sharing a fingerprint is an evidence conflict and
   forces `PARTIAL`.

Assertions:

- [ ] Mutable paths, wording, line numbers, hashes, status, priority, run ID, and
      timestamps are excluded from finding identity.
- [ ] Stable project/artifact/requirement/target/dependency identities participate.
- [ ] A consumer can reject a packet after any artifact byte changes.

---

### Case 12: Snapshot mutation is visible and non-combinable

Fixture:

- The analyzer locks all inputs and derives several valid inclusion rows.
- One requirement source changes bytes before finalization and one new manifest
  candidate appears under a declared root.

Input: `$content-audit`

Expected behavior:

1. Re-enumeration finds the added candidate and re-hashing marks the changed
   source `STALE`.
2. Semantic conclusions from old bytes are discarded.
3. Unaffected evidence remains visible with coverage limitations.
4. Verdict is `PARTIAL`; the analyzer does not silently restart or mix snapshots.

Assertions:

- [ ] Modification time and Git status are not substitutes for raw-byte hashes.
- [ ] Added, removed, renamed, and changed inputs are all detectable manifest
      changes.
- [ ] A stale source can never contribute to `COMPLETE`.

---

### Case 13: No authoritative requirements after bounded full reads

Fixture:

- All in-scope GDD candidates are readable and within limits but contain no
  structured inventory, explicit stable content requirement ID, or exact
  cross-reference to one.
- Asset folders contain many plausible content files.

Input: `$content-audit`

Expected behavior:

1. Every in-scope GDD candidate is read in full rather than keyword-filtered.
2. The audit records `NO_AUTHORITATIVE_REQUIREMENTS`.
3. Asset files remain bounded advisory observations only.
4. Verdict is `PARTIAL`; no planned identity or gap table is invented.
5. The one next action belongs to the design owner and is not invoked.

Assertions:

- [ ] No requirement source or asset count is fabricated.
- [ ] Lack of authoritative content is a coverage gap, not an empty complete set.
- [ ] The packet remains read-only and hash-bound.

---

### Case 14: Duplicate IDs, wrong targets, and variant policy conflict

Fixture:

- Two authoritative sources assign the same requirement ID to different logical
  content IDs.
- One inclusion record targets another build.
- Two current exact-target records disagree on `included`.
- One logical item lacks a required accessibility variant.

Input: `$content-audit`

Expected behavior:

1. The duplicate semantic identity is `IDENTITY_CONFLICT`.
2. The wrong-target record is rejected and cannot prove inclusion.
3. The disagreeing exact-target records are `EVIDENCE_CONFLICT`.
4. The missing required variant prevents `SHIPPED_VERIFIED` and, when explicit
   current evidence proves absence, classifies the logical item `MISSING`.
5. Verdict is `PARTIAL` because identity/evidence coverage is conflicted, while
   the known missing variant remains visible.

Assertions:

- [ ] The analyzer never chooses newest, majority, or filename-preferred evidence.
- [ ] Variant files do not inflate logical item totals.
- [ ] Every normalized requirement has exactly one implementation state.

---

## Protocol Compliance

- [ ] Invocation, project identity, target identity, and applicable instructions
      are exact and hash-bound.
- [ ] The candidate inventory is deterministic, bounded, project-local, and
      complete about exclusions and failures.
- [ ] Every selected requirement source is read in full once without keyword or
      filename preselection.
- [ ] Stable requirement IDs, logical content IDs, variant policies, target/build
      IDs, manifest IDs, adapter IDs/versions, and dependency IDs are explicit.
- [ ] Direct manifest or registered adapter records conform to
      `cgs.content-inclusion/v1` and preserve exact provenance.
- [ ] All six ID sets are explicit and derived only from per-ID classifications.
- [ ] Counts and file presence are advisory only; no completion percentage exists.
- [ ] Asset-format compliance belongs to asset-audit and is never reimplemented.
- [ ] Coverage is represented per source/channel/check and every material gap
      deterministically prevents `COMPLETE`.
- [ ] `PARTIAL` preserves known critical and ordinary gaps.
- [ ] Stable finding IDs survive non-semantic source movement or wording changes.
- [ ] Evidence packet artifact, manifest, payload, and record hashes recompute.
- [ ] Full and summary modes are strictly read-only and invoke no gate, recorder,
      owner, or downstream workflow.
- [ ] Any execution `ERROR` returns no verdict or review-evidence envelope; a
      post-lock diagnostic may expose only the locked manifest and exact failure.
- [ ] Output conforms to `cgs.review-evidence/v1` plus
      `cgs.content-audit-report/v1` under `cgs.content-audit/v3`.

---

## Coverage Notes

Behavioral fixtures must expose immutable raw bytes, canonical project-relative
paths, stable artifact/requirement/system/target/build/dependency IDs, and exact
adapter/manifest schema versions so current, stale, unsupported, conflicting, and
wrong-target evidence are distinguishable. Tests that mutate a fixture must do so
only between the explicitly modeled manifest-lock and final-revalidation steps.

Report persistence belongs to a separate recorder contract and is intentionally
outside this analyzer specification. The catalog entry points to this file, and
its `last_*` result fields must remain blank until these cases are actually
executed by the authorized test workflow. Editing this spec alone is not a test
pass and must not create a catalog result claim.
