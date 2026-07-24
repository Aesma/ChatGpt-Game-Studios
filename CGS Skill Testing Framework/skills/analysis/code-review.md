# Skill Test Spec: $code-review

## Skill Summary

`$code-review` performs a strictly read-only, hash-bound review of explicit
project source targets. It builds a bounded target manifest, loads the complete
root-to-target rule chain, admits only explicit current ADR evidence, distinguishes
tool-verified facts from unverified judgment, routes at most three deduplicated
reviewers through current engine configuration, and returns
`cgs.review-evidence/v1` with a `cgs.code-review/v2` extension.

Finding severities are `BLOCKING`, `WARNING`, and `INFO`. Verdict precedence is:

1. invalid input/nonexistent valid manifest -> `ERROR` with null verdict;
2. incomplete mandatory coverage -> `PARTIAL`;
3. complete coverage plus blocking finding -> `NEEDS CHANGES`;
4. complete coverage plus warning but no blocker -> `CONCERNS`;
5. complete coverage with only info or no findings -> `APPROVED`.

The skill writes nothing, never treats silence as clean evidence, and never
invokes or offers a bypass into story completion.

---

## Static Assertions

- [ ] Frontmatter contains exactly `name: code-review` and a non-empty
      description
- [ ] Invocation requires one to eight repeatable `--target` options and permits
      at most one `--story`
- [ ] Positional, glob, absolute/out-of-root, duplicate, binary, and invalid story
      inputs have explicit error behavior
- [ ] Numeric bounds exist for target roots/files/depth/bytes, rule sources,
      ADRs, analysis receipts, reviewers/attempts/deadline, and snapshot chunks
- [ ] The rule chain is loaded root-to-target independently for every file and
      reports precedence/conflicts
- [ ] No universal complexity, method-length, DI/interface, or SOLID threshold is
      imposed without an exact applicable rule source
- [ ] Rule modality maps deterministically to `BLOCKING`, `WARNING`, `INFO`, or
      unresolved/partial
- [ ] AST/linter, build graph, profiler/runtime, build, and test claims require
      compatible current receipts and otherwise remain `UNVERIFIED`
- [ ] Commit messages are clues only and never create ADR compliance bindings
- [ ] Reviewer planning uses exact configured Engine Specialists/type routing,
      deduplicates roles, caps total reviewers at three, and defines timeout/
      overflow/invalid-response partial behavior
- [ ] Findings have stable fingerprints/IDs and exact target/rule hashes
- [ ] Output schema is `cgs.review-evidence/v1` plus `cgs.code-review/v2`
- [ ] Direct output is `NOT_PERSISTED`, gate-ineligible, and strictly zero-write
- [ ] Metadata has an untruncated description and names explicit targets,
      rule-sourced coverage, exact hashes, bounded specialists, and read-only use
- [ ] No next-step text suggests bypassing review or equates it with story done

---

## Director Gate Checks

None. `lead-programmer`, configured engine specialists, and story-scoped
`qa-tester` are bounded evidence reviewers, not director gates. They cannot edit
targets or decide the verdict.

---

## Test Cases

### Case 1: Strict single-file invocation forms an exact manifest

Fixture: `src/gameplay/health_component.gd` is a readable eligible source file.

Input: `$code-review --target src/gameplay/health_component.gd`

Assertions:

- [ ] Input normalizes to `cgs.code-review-input/v1`
- [ ] Manifest contains the canonical path, type, size, origin, and complete
      SHA-256
- [ ] Target-manifest hash binds the sorted canonical row
- [ ] Final record re-hashes the same exact target bytes

---

### Case 2: Repeatable targets and one explicit story

Fixture: Two source targets and one current story with stable story ID/type/scope.

Input: `$code-review --target src/a.gd --target src/b.gd --story production/epics/e/story-001.md`

Assertions:

- [ ] Both targets are retained and sorted; the story is context, not a target
- [ ] Story scope, requirements, QA applicability, and explicit ADR IDs are parsed
- [ ] The story is read-only and not marked complete
- [ ] A second `--story` is rejected

---

### Case 3: Invalid input never guesses a target

Fixtures: no arguments; a positional path; wildcard; duplicate canonical path;
absolute/out-of-root path; escaping link; missing path; binary asset; malformed
story; target directory with no eligible source.

Assertions:

- [ ] Each returns a bounded `ERROR` with the rejected input and remediation
- [ ] Current directory, Git changes, last story, and conversation context are not
      used as fallback targets
- [ ] Verdict is null and no review envelope is forged
- [ ] No file is written

---

### Case 4: Directory manifest exclusions require evidence

Fixture: A directory contains source, committed generated code with an exact
generation marker, owner-declared vendor content, and a folder merely named
`vendor` whose files are project-owned.

Assertions:

- [ ] Source files and project-owned `vendor`-named files remain eligible
- [ ] Generated/vendor exclusions cite exact rule/marker path and hash
- [ ] Directory name alone never excludes a file
- [ ] Excluded rows remain visible in the complete manifest

---

### Case 5: Manifest bounds preserve unchecked scope

Fixtures independently exceed file count, per-file bytes, total bytes, or depth.

Assertions:

- [ ] Reviewed subset follows deterministic sorted order and exact fixed bounds
- [ ] Every overflow row is retained as `UNCHECKED` with a stable reason
- [ ] Target coverage and verdict are `PARTIAL`
- [ ] No file is silently dropped or partially read as if complete

---

### Case 6: Complete root-to-leaf AGENTS chain controls one target

Fixture: Root, `src/AGENTS.md`, and `src/ui/AGENTS.md` define overlapping and
distinct rules; target is `src/ui/menu.gd`.

Assertions:

- [ ] All three files are read completely and exact-hash recorded root-to-leaf
- [ ] Nearest rule wins only under the documented closest-file precedence
- [ ] Rule ledger records path/hash/location/scope/precedence for every rule
- [ ] Broken applicable direct standards links force `PARTIAL`

---

### Case 7: Sibling nested rules never leak

Fixture: `src/ui/AGENTS.md` and `src/network/AGENTS.md` differ; one target exists
under each subtree.

Assertions:

- [ ] Each target has an independent rule chain
- [ ] UI-only rules do not apply to the network target and vice versa
- [ ] Shared ancestor rules retain their current exact hashes for both
- [ ] Coverage denominators are target-specific

---

### Case 8: Unresolved rule conflict is partial

Fixture: Two current authorities impose contradictory requirements with no exact
override/supersession declaration.

Assertions:

- [ ] Conflict is named `RULE_CONFLICT`
- [ ] Applicability/severity/check state is unresolved/`UNVERIFIED`
- [ ] Reviewer does not choose a preferred convention from personal judgment
- [ ] Verdict is `PARTIAL`

---

### Case 9: Generic hard-coded standards are absent

Fixture: Applicable sources define complexity ≤15 and permit a 70-line
hand-written parser method; they do not require interfaces or DI for pure value
objects.

Assertions:

- [ ] Reviewer does not impose complexity <10, 40-line methods, interfaces, DI,
      or generic SOLID labels
- [ ] Configured complexity rule is evaluated against ≤15 only
- [ ] Conditional method-length and value-object rules use evidence-backed N/A
- [ ] Unsupported N/A is `UNVERIFIED`, not a pass

---

### Case 10: Rule modality determines severity

Fixture: Current sources contain explicit MUST, SHOULD, MAY, and unqualified
ambiguous statements; all four are violated.

Assertions:

- [ ] Severities resolve respectively to `BLOCKING`, `WARNING`, `INFO`, and
      `UNRESOLVED`
- [ ] Ambiguous modality makes coverage partial instead of inventing severity
- [ ] Reviewer-proposed severity cannot override the rule ledger
- [ ] Stable rule IDs retain source path/hash/location

---

### Case 11: Complexity needs compatible AST or linter evidence

Fixtures: The same source/rule with (a) compatible current AST receipt,
(b) natural-language inspection only, and (c) stale-config receipt.

Assertions:

- [ ] Compatible receipt produces `VERIFIED_PASS` or `VERIFIED_FAIL`
- [ ] Inspection-only and stale receipt produce `UNVERIFIED`
- [ ] Tool/version/configuration/input/result hashes are recorded
- [ ] Required unverified complexity makes verdict `PARTIAL`

---

### Case 12: Cycles and hot paths cannot be inferred from prose

Fixtures: A cycle rule without a current build graph and an allocation rule
without compatible analyzer/profiler evidence.

Assertions:

- [ ] Both checks are `UNVERIFIED`
- [ ] No dependency graph or hot-path cleanliness claim is made
- [ ] Candidate concerns may be INFO but do not replace required evidence
- [ ] Coverage and verdict are `PARTIAL`

---

### Case 13: Analysis receipt must bind exact capabilities and inputs

Fixture: A receipt has correct schema/tool version but omits one target hash and
claims a capability the tool configuration does not enable.

Assertions:

- [ ] Receipt is incompatible for the affected checks
- [ ] Other explicitly supported, correctly bound checks may remain verified
- [ ] Partial/error/timeout receipt never becomes a clean pass
- [ ] The review never installs tools, builds, tests, or profiles to fill gaps

---

### Case 14: Explicit Accepted ADR governs exact targets

Fixture: Story and source header both cite the same stable ADR ID/path. The unique
current ADR is `Accepted`, has Decision/Consequences, and applies to both target
hashes.

Assertions:

- [ ] Declarations deduplicate without losing provenance
- [ ] ADR ID/path/hash/status/scope are recorded
- [ ] Decision and Consequences become source-bound rule rows
- [ ] Compliance is evaluated only against that exact Accepted evidence

---

### Case 15: Commit message is never an ADR binding

Fixture: No story/source/manifest ADR reference exists, but an old commit message
mentions `ADR-009`.

Assertions:

- [ ] Commit match appears only under non-authoritative clues, if inspected
- [ ] `ADR-009` is not added to the governing ADR set
- [ ] No ADR compliance claim is made
- [ ] When current project rules require ADR governance, result is
      `ADR_NOT_EVALUATED` and `PARTIAL`

---

### Case 16: Proposed, stale, ambiguous, and multiple ADRs are honest

Fixtures: A readable Proposed ADR; a stale declared path/hash; duplicate files
with the same ID; and two unique current Accepted ADRs.

Assertions:

- [ ] Proposed is status-checked, not compliance evidence, and produces the
      source-bound warning/`CONCERNS` when all coverage is otherwise complete
- [ ] Stale and ambiguous evidence force `PARTIAL`
- [ ] Both unique Accepted ADRs are independently evaluated
- [ ] Supersession is followed only through an explicit stable link

---

### Case 17: Engine specialist routing uses exact configuration

Fixture: Technical preferences configure one language specialist and one shader
specialist; Primary is the same role as the language specialist. Targets include
configured language and shader file types.

Assertions:

- [ ] Preferences path/hash and matching routing rows are recorded
- [ ] Roles are mapped by configured target type, not filename guesswork
- [ ] Duplicate Primary/language role is merged with combined assignments
- [ ] No unrelated engine family or specialist is invented

---

### Case 18: Reviewer cap and overflow are deterministic

Fixture: After deduplication, lead plus three distinct source/story-required roles
remain.

Assertions:

- [ ] Candidate list and deterministic priority exist before capping
- [ ] At most three total roles are dispatched in one parallel batch
- [ ] Required overflow is `NOT_DISPATCHED_LIMIT`
- [ ] Reviewer coverage and verdict are `PARTIAL`

---

### Case 19: Timeout and invalid reviewer evidence are partial

Fixtures: Required reviewer times out beyond one 120-second total deadline; retry
exceeds two attempts; response has wrong manifest hash; response writes a file.

Assertions:

- [ ] Exact status is `TIMEOUT` or `INVALID_RESPONSE`
- [ ] Retry does not reset the deadline and attempt count never exceeds two
- [ ] Silence/hash mismatch is not inferred clean
- [ ] Mutation or required-reviewer failure forces `PARTIAL`

---

### Case 20: Lead fallback is narrow

Fixture: `lead-programmer` is unavailable and the current agent performs the
integrated lead responsibility; a configured shader specialist is unavailable.

Assertions:

- [ ] Lead is `DONE_LOCAL_FALLBACK` with completed assigned evidence
- [ ] Current agent does not impersonate the shader specialist
- [ ] Shader failure remains a reviewer coverage gap
- [ ] Verdict is `PARTIAL`

---

### Case 21: Verdict table is deterministic

Fixtures: (a) invalid empty manifest, (b) a required unverified check plus a known
blocker, (c) complete coverage plus blocker, (d) complete coverage plus warning,
(e) complete coverage with info only.

Assertions:

- [ ] Results are respectively null/`ERROR`, `PARTIAL`, `NEEDS CHANGES`,
      `CONCERNS`, and `APPROVED`
- [ ] Known findings remain visible under partial coverage
- [ ] `INFO` alone does not block approval
- [ ] Accepted risk cannot change severity, coverage, or verdict

---

### Case 22: Stable findings retain identity while hashes expose staleness

Fixture: A violation remains on the same stable symbol/rule after unrelated lines
and target bytes change; then the rule source bytes change.

Assertions:

- [ ] Fingerprint/CRF ID remains stable for the same defect
- [ ] Target and rule SHA-256 fields update independently
- [ ] Line numbers, wording, timestamps, reviewer, and severity are absent from
      fingerprint material
- [ ] Prior record stale key changes when target/rule/evidence inputs change

---

### Case 23: Mutation guard proves zero-write behavior

Fixtures: (a) unchanged before/after project roots, (b) in-scope file changes
during review, and (c) incomplete denied-path snapshot coverage.

Assertions:

- [ ] Status is respectively `UNCHANGED`, `CHANGED`, and `INCOMPLETE`
- [ ] Snapshot chunk size never exceeds 256 paths
- [ ] Changed/incomplete guard forces `PARTIAL`
- [ ] Reviewer never repairs, reverts, stages, or writes changed files

---

### Case 24: Code review never bypasses into story completion

Fixtures: Each of `APPROVED`, `CONCERNS`, `NEEDS CHANGES`, and `PARTIAL`.

Assertions:

- [ ] Output delivers source-bound findings/coverage/remediation and stops
- [ ] It does not invoke or offer “run story-done anyway”
- [ ] It does not mark a story complete or call the review completion evidence
- [ ] It states that story completion independently validates its own current
      evidence

---

## Protocol Compliance

- [ ] Exact named inputs produce one bounded hash-bound manifest
- [ ] Every target loads its complete applicable AGENTS/standards chain
- [ ] Rule applicability and severity come from current source evidence
- [ ] Complex semantic/runtime claims use compatible analysis evidence or remain
      `UNVERIFIED`
- [ ] ADR compliance uses explicit unique current Accepted ADRs only
- [ ] Engine and QA roles route through exact configuration/story scope,
      deduplicate, cap at three, and fail honestly to partial
- [ ] Coverage is reported for targets, rule sources, checks, ADRs, reviewers,
      and mutation guard before verdict
- [ ] Verdict uses exactly `APPROVED`, `CONCERNS`, `NEEDS CHANGES`, or `PARTIAL`
- [ ] Every finding is stable-ID and exact target/rule-hash bound
- [ ] Generic and code-specific evidence schemas are complete and non-persisted
- [ ] Skill edits nothing and never acts as or bypasses story completion

---

## Coverage Notes

- CDR-003: Cases 1-5.
- CDR-004: Cases 6-8.
- CDR-005: Cases 9-10.
- CDR-006: Cases 11-13.
- CDR-007: Cases 14-16.
- CDR-008: Cases 17-20.
- CDR-009: Case 21 plus rule-severity static assertions.
- CDR-010: Case 24.

Case 22 verifies the requested stable-finding and exact-hash contract; Case 23
verifies strict read-only mutation evidence. Persistence and downstream gate
consumption remain external: direct `$code-review` output is always
`NOT_PERSISTED` and gate-ineligible.
