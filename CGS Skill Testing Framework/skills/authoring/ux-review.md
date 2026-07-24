# Skill Test Spec: $ux-review

## Skill Summary

`$ux-review` is a zero-write, profile-aware quality gate for the three artifact
types authored by `$ux-design`: `ux-spec`, `hud-design`, and
`interaction-pattern-library`. It derives the current author schema from exact
source bytes, routes by artifact metadata, validates semantic content rather than
heading presence, resolves hash-bound platform/accessibility/requirement evidence,
and returns `cgs.review-evidence/v1` with a `cgs.ux-review/v2` extension.

Quality verdicts are `APPROVED`, `NEEDS REVISION`, `MAJOR REVISION NEEDED`, and
`PARTIAL`. Invalid invocation/identity returns `ERROR`; incompatible author
schema returns `MIGRATION REQUIRED`; neither has a quality verdict. Every direct
output remains `NOT_PERSISTED` and ineligible as gate evidence.

---

## Static Assertions

- [ ] Frontmatter contains exactly `name: ux-review` and a non-empty description
- [ ] `SKILL.md` reads both current `$ux-design` author sources and derives the
      NUL-delimited SHA-256 author-schema identity
- [ ] Builds `cgs.ux-author-contract-manifest/v1` from the author's exact
      declarations and source hashes; target schema/profile/content values must
      match that manifest
- [ ] Reviewer support is fail-closed and currently accepts exactly
      `ux-profile-schema-v2` plus `cgs.ux-content-profile/v2`; legacy v1 or an
      author/target hash mismatch returns `MIGRATION REQUIRED` with null verdict
- [ ] `review-rules-v1.md` defines `cgs.review-evidence/v1`,
      `cgs.ux-review/v2`, `cgs.ux-review-batch/v1`, and
      `cgs.ux-review-worker/v1`
- [ ] All three artifact profiles use stable author-schema section IDs and
      semantic assertions
- [ ] Content states are exactly `VALID`, `EMPTY`, `PLACEHOLDER`, `INVALID`,
      `MISSING`, `NOT_APPLICABLE`, and `UNEVALUATED`
- [ ] Platform, accessibility, context, requirement, pattern/data, and optional
      performance sources require exact path/hash or stable-ID provenance
- [ ] Selector, context, requirement, reviewer, and mutation-snapshot limits are
      numeric and fail to `PARTIAL` rather than silently truncating
- [ ] Finding fingerprints exclude target hashes, line numbers, prose wording,
      and timestamps, enabling stable convergence
- [ ] Accepted risk cannot yield `APPROVED`
- [ ] No workflow step writes a project file or calls a recorder
- [ ] Metadata display name, description, and default prompt describe the current
      zero-write, hash-bound behavior without truncation

---

## Director Gate Checks

None. Standard review is local. Expert depth permits one bounded `ux-designer`
consultation, but the lead owns all mechanical checks, finding normalization, and
the verdict. The consultation may not write or approve.

---

## Test Cases

### Case 1: Complete current screen specification passes semantic checks

Fixture: A current `ux-spec` declares `ux-profile-schema-v2`,
`cgs.ux-content-profile/v2`, and the exact computed
`ux-design-author-sha256:<author_schema_hash>`; every `UXS-01`..`UXS-14`
assertion is populated with valid stable IDs, current context/platform/
accessibility/authoring-receipt hashes, a committed tier, and complete requirement
coverage.

Input: `$ux-review design/ux/inventory.md`

Assertions:

- [ ] Routes from `Artifact Type: ux-spec` to `screen-spec`
- [ ] Uses exact current author-contract manifest, author-schema,
      profile-version, and content-profile identities
- [ ] Every header and profile assertion is `VALID`
- [ ] Returns `APPROVED` in a complete `cgs.review-evidence/v1` envelope
- [ ] Returns `gate_evidence_status: NOT_PERSISTED` and
      `gate_evidence_eligible: false`
- [ ] Makes no file writes

---

### Case 2: Headings with empty or placeholder bodies fail

Fixture: A current `ux-spec` contains every required heading, but `UXS-06` has a
blank table, `UXS-10` contains `TBD`, and `UXS-13` repeats template examples.

Assertions:

- [ ] States are `EMPTY`, `PLACEHOLDER`, and `PLACEHOLDER` respectively
- [ ] No failed section is marked `VALID` merely because its heading exists
- [ ] Findings name stable check keys and exact evidence locations
- [ ] Verdict is `NEEDS REVISION` or stronger according to the severity matrix

---

### Case 3: Unsupported N/A does not satisfy a conditional assertion

Fixture: `UXS-06` says loading, error, and locked states are `N/A` without a
source ID/hash or rationale; the current platform/profile evidence makes an error
state applicable.

Assertions:

- [ ] Each unsupported N/A is `INVALID`, not `NOT_APPLICABLE`
- [ ] The error-state omission creates a `BLOCKING` finding
- [ ] A source-backed excluded input variant can independently be
      `NOT_APPLICABLE`
- [ ] The record preserves the N/A evidence object or null for every assertion

---

### Case 4: Platform label is never an authority fallback

Fixture: The header says `Platform Target: PC`, but `Platform Profile` is
`MISSING`. The remaining content is complete.

Assertions:

- [ ] Does not infer controls, viewport, safe zone, or input variants from `PC`
- [ ] Dependency ledger records the platform profile as `MISSING`
- [ ] Affected assertions are `UNEVALUATED`
- [ ] Verdict is `PARTIAL`, never `APPROVED`

---

### Case 5: Stale platform profile is partial

Fixture: `Platform Profile` declares `profiles/pc.md@<hash-a>`, but exact bytes
hash to `<hash-b>`.

Assertions:

- [ ] Ledger stores expected and actual hashes and status `STALE`
- [ ] No spec header, filename, or remembered defaults replace the source
- [ ] Verdict is `PARTIAL`
- [ ] Remediation asks for a current exact platform-profile reference

---

### Case 6: Missing accessibility tier cannot be compliant or approved

Fixture: Accessibility foundation bytes/hash are current but the declared tier
is absent, empty, or not defined by that source.

Assertions:

- [ ] Ledger records the tier failure as a dependency gap
- [ ] `UXS-11` or `HUD-07` is not `VALID`
- [ ] Output never labels accessibility `COMPLIANT`
- [ ] Verdict is `PARTIAL` and approval status is `NOT_APPROVED`

---

### Case 7: Requirement coverage uses stable IDs and a symmetric denominator

Fixture: The target declares `UIR-10`; the current bounded manifest additionally
scopes approved `UIR-11` to the same Screen ID. The target header lists `UIR-10`,
but only a concrete interaction implements `UIR-11`.

Assertions:

- [ ] Denominator is `{UIR-10, UIR-11}` with exact source provenance
- [ ] A header mention alone does not mark `UIR-10` covered
- [ ] `UIR-11` is traced to its semantic implementation location
- [ ] Coverage rows report `DECLARED_NOT_TRACED` and `COVERED` respectively
- [ ] No GDD filename or heading is treated as a requirement ID

---

### Case 8: Incomplete requirement scope yields partial, not false 100 percent

Fixture: The context-manifest hash is stale and the target declares no
requirements.

Assertions:

- [ ] `denominator_complete: false`
- [ ] `coverage_ratio: null`, not `1` or `100%`
- [ ] The stale context manifest appears in the dependency ledger
- [ ] Verdict is `PARTIAL`

---

### Case 9: Bounded all mode returns per-file records

Fixture: `design/ux/` contains three eligible artifacts, two excluded reports,
and one unknown note, all under fixed limits.

Input: `$ux-review all`

Assertions:

- [ ] Manifest is sorted and hash-bound
- [ ] Reports and unknown types are excluded with explicit reasons
- [ ] Each eligible artifact has its own generic envelope and independent verdict
- [ ] Batch result uses `cgs.ux-review-batch/v1` and has no aggregate approval
- [ ] No target verdict approves another target

---

### Case 10: Batch overflow is explicit and partial

Fixture: The sorted manifest contains ten eligible artifacts.

Input: `$ux-review all`

Assertions:

- [ ] Exactly the first eight sorted eligible targets are evaluated
- [ ] The two remaining entries retain path/hash/type in `unchecked`
- [ ] Each unchecked reason is `LIMIT_REACHED`
- [ ] Batch status is `PARTIAL`
- [ ] Reviewed target records remain independently usable as non-persisted review
      results

---

### Case 11: Standard depth is local and deterministic

Fixture: A valid current HUD artifact.

Input: `$ux-review design/ux/hud.md --review-depth standard`

Assertions:

- [ ] Consultation is `NOT_REQUESTED` with reviewer count zero
- [ ] Mechanical profile, hash, dependency, and coverage checks execute locally
- [ ] The run can be complete without delegation
- [ ] No reviewer is permitted to override a mechanical failure

---

### Case 12: Required expert consultation failure is partial

Fixture: A current pattern library; the one expert reviewer declines, times out,
errors, returns malformed output, or returns a mismatched target hash.

Input: `$ux-review design/ux/interaction-patterns.md --review-depth expert`

Assertions:

- [ ] At most one reviewer is dispatched
- [ ] Exact failure state is recorded in consultation evidence
- [ ] Locally confirmed findings remain in the record
- [ ] Verdict is `PARTIAL`, never silently downgraded to standard
- [ ] Reviewer performs no writes and emits no verdict

---

### Case 13: Perceived responsiveness is not a fabricated X-ms budget

Fixture: A UX spec defines acknowledgement, progress, cancellation, recovery, and
error feedback, but cites no numeric performance requirement.

Assertions:

- [ ] UX feedback assertions are evaluated normally
- [ ] Reviewer introduces no universal millisecond threshold
- [ ] Absence of an uncited numeric budget is not by itself a finding
- [ ] A numeric claim is evaluated only with exact technical source ID/path/hash,
      platform, hardware class, scenario, metric, and threshold

---

### Case 14: Required runtime evidence gap is routed honestly

Fixture: An acceptance criterion cites a stable performance requirement, but its
source hash is stale.

Assertions:

- [ ] Adds `NEEDS-PERFORMANCE-EVIDENCE`
- [ ] Marks the affected assertion `UNEVALUATED`
- [ ] Verdict is `PARTIAL`
- [ ] Does not claim to have profiled or measured runtime behavior

---

### Case 15: Prior open finding keeps its stable identity

Fixture: A valid prior persisted v2 record contains an open finding. Current
bytes change unrelated prose while the same defect remains.

Input: `$ux-review design/ux/inventory.md --prior-review <record>`

Assertions:

- [ ] Prior record ID, target identity/hash, and author-schema identity validate
- [ ] Prior author-contract manifest hash and profile/content versions match the
      current review contract
- [ ] Prior open finding is evaluated before new checks
- [ ] Fingerprint and finding ID remain unchanged
- [ ] Disposition is `OPEN`; changed target hash does not create a new ID

---

### Case 16: Resolved and regressed findings are explicit

Fixture: Exact prior/current diff evidence shows one prior defect fixed and a
previously resolved defect reintroduced in a changed stable section.

Assertions:

- [ ] Fixed finding is `RESOLVED`
- [ ] Reintroduced matching fingerprint is `REGRESSED`
- [ ] Changed section and dependency cross-references are regression-checked
- [ ] No finding closes because wording or line numbers changed

---

### Case 17: Missing convergence evidence is partial

Fixtures: Separately test a malformed/unrelated prior envelope and a valid prior
envelope whose exact prior bytes/diff cannot be reproduced.

Assertions:

- [ ] Malformed or unrelated evidence returns input `ERROR` with null verdict
- [ ] Missing exact diff evidence yields `PARTIAL`
- [ ] Observable findings are preserved
- [ ] Output does not claim convergence from prose summaries

---

### Case 18: Deterministic verdict precedence

Fixtures: Current artifacts with (a) no required failures, (b) a blocking
finding, (c) a major finding, (d) an unevaluated required assertion, and (e) an
unsupported author schema.

Assertions:

- [ ] Results are respectively `APPROVED`, `NEEDS REVISION`,
      `MAJOR REVISION NEEDED`, `PARTIAL`, and `MIGRATION REQUIRED`/null
- [ ] Accepted-risk major or blocking findings remain open for verdict purposes
- [ ] `APPROVED` requires complete dependencies, denominator, assertions,
      consultation, convergence when requested, and mutation guard

---

### Case 19: Mutation guard remains read-only

Fixtures: Run once with identical bounded before/after streaming tree roots, once
with an external in-scope file change during review, and once with incomplete
snapshot coverage.

Assertions:

- [ ] Results are `UNCHANGED`, `CHANGED`, and `INCOMPLETE` respectively
- [ ] `CHANGED` and `INCOMPLETE` force `PARTIAL`
- [ ] Snapshot processing uses chunks of at most 256 paths
- [ ] Reviewer reports changes but never repairs, reverts, or writes them

---

### Case 20: Missing target and invalid invocation are non-quality errors

Fixtures: Missing exact target; unknown flag; batch selector combined with
`--prior-review`; duplicate target.

Assertions:

- [ ] Each returns a bounded error object with exact code and remediation
- [ ] Verdict is null and no profile quality checklist is forged
- [ ] No file is written

---

### Case 21: Filename fallback requires explicit confirmation

Fixture: Exact target `design/ux/hud.md` has no Artifact Type and no exact current
author template marker.

Assertions:

- [ ] Filename only proposes `hud-design`; it does not route automatically
- [ ] Reviewer asks for explicit confirmation and emits no verdict beforehand
- [ ] Confirmed routing basis is `user-confirmed-filename-fallback`
- [ ] Confirmation does not invent missing Schema Version, Profile Version,
      Artifact ID, platform, accessibility, or requirement evidence
- [ ] The legacy artifact returns `MIGRATION REQUIRED` rather than a quality pass
- [ ] Batch selectors exclude the unknown artifact instead of prompting

---

### Case 22: Current author-declared v2 contract is supported

Fixture: Exact current P1 `$ux-design` main and continuation bytes declare one
coherent contract: Profile Version `ux-profile-schema-v2`, Content Profile
`cgs.ux-content-profile/v2`, all three artifact profile/section sets, and Schema
Version constructed from the NUL-delimited author hash. The target header matches
those computed values.

Assertions:

- [ ] Reviewer records raw main/continuation hashes, computed author schema hash,
      canonical author-contract manifest, and its hash
- [ ] Support status is `SUPPORTED` only after assertion-matrix coverage matches
      every declared stable section ID
- [ ] Target identity passes the compatibility gate before profile scoring
- [ ] No literal v1 expectation overrides the author declaration

---

### Case 23: Legacy, unsupported, or hash-mixed contracts fail closed

Fixtures: Separately test (a) unsupported legacy target Profile Version `ux-profile-schema-v1`,
(b) unsupported future author profile/content declarations, (c) matching v2
profile but stale `Schema Version` hash, (d) missing/duplicate author declaration,
(e) v2 author section added without a reviewer assertion, and (f) a prior review
bound to a different author-contract manifest.

Assertions:

- [ ] Every variant returns `MIGRATION REQUIRED` with null verdict before content
      scoring or expert consultation
- [ ] Output names expected/observed schema, profile, content, author source
      hashes, and manifest hash when computable
- [ ] No v1 fallback, arbitrary-manifest trust, remembered hash, mixed-contract
      scoring, or cross-schema convergence occurs
- [ ] The reviewer remains zero-write and gate-ineligible

---

## Protocol Compliance

- [ ] Routes from current artifact identity, then exact schema-defined marker;
      aliases select candidates and filename fallback requires user confirmation
- [ ] Author declarations, reviewer support, target schema/profile/content, and
      author hash must all agree before profile routing/content scoring
- [ ] Applies content-level assertions to all current profile sections
- [ ] Rejects empty, placeholder, invalid, missing, and unsupported-N/A content
- [ ] Treats missing/stale platform, accessibility tier, context, and denominator
      evidence as `PARTIAL`
- [ ] Uses stable requirement IDs and an explicit symmetric denominator
- [ ] Batches are capped, preserve unchecked rows, and never aggregate approval
- [ ] Standard review is local; expert review is one bounded non-authoritative
      consultation whose failure is visible
- [ ] Separates perceived UX response from source-bound runtime performance
- [ ] Reconciles prior findings through stable fingerprints and exact diff evidence
- [ ] Emits the complete generic envelope plus UX v2 extension
- [ ] Every direct result is `NOT_PERSISTED`, gate-ineligible, and zero-write

---

## Coverage Notes

- UXR-005: Cases 1-3 plus content-state static assertions.
- UXR-006: Cases 4-5.
- UXR-007: Case 6.
- UXR-008: Cases 7-8.
- UXR-009: Cases 9-10.
- UXR-010: Cases 11-12.
- UXR-011: Cases 13-14.
- UXR-012: Cases 15-17.
- UXR-013: Static assertions, Cases 18-20, and protocol compliance.

Persistence and downstream gate consumption remain external integrations. The
spec verifies that `$ux-review` returns a persistable shape without claiming that
the conversation-only record has been persisted or is gate-eligible.
