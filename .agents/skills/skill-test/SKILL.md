---
name: skill-test
description: "Validate skill packages through versioned structural rules, machine-readable semantic contracts, and preflighted behavioral specs. Optional immutable result receipts are hash-bound to every tested authority; invalid infrastructure, partial coverage, or stale dependencies can never be reported COMPLIANT."
---

# Skill Test

## Invocation and execution

Invoke this workflow as `$skill-test`.

Arguments:

- `static [skill-name | all] [--persist-receipt]`
- `spec [skill-name] [--persist-receipt]`
- `category [skill-name | all] [--persist-receipt]`
- `audit [--persist-receipt]`

Every mode also accepts optional read-only `--check-receipt [receipt-path]`.

If the mode or required target is missing or invalid, show these forms and stop
without writing.

Validation is read-only by default. Never execute the target skill. The only
optional write is one immutable, version-bound result receipt after a complete
one-file changeset preview and approval.

## Contract Manifest

```yaml
schema: cgs-skill-contract/v1
skill: skill-test
modes:
  static:
    targets: [one_skill, all_skills]
  spec:
    targets: [one_skill]
  category:
    targets: [one_skill, all_skills]
  audit:
    targets: [repository]
flags:
  persist_receipt:
    default: false
  check_receipt:
    default: false
    effect: read_only_freshness_validation
reads:
  - .agents/skills/**/SKILL.md
  - .agents/skills/**/agents/openai.yaml
  - .codex/agents/**/*.toml
  - CGS Skill Testing Framework/catalog.yaml
  - CGS Skill Testing Framework/quality-rubric.md
  - CGS Skill Testing Framework/skills/**/*.md
  - CGS Skill Testing Framework/agents/**/*.md
  - CGS Skill Testing Framework/templates/skill-test-spec.md
writes:
  - when: persist_receipt
    path: CGS Skill Testing Framework/results/skill-test/receipt-[receipt-id].yaml
never_writes:
  - CGS Skill Testing Framework/catalog.yaml
  - target skill packages
  - target specs or rubrics
authorization:
  kind: one_complete_changeset_before_first_write
operation_states: [ANALYZED, RECEIPT_WRITTEN, RECEIPT_UNCHANGED, RECEIPT_DECLINED, FAILED]
validation_verdicts: [COMPLIANT, WARNINGS, NON-COMPLIANT, PARTIAL_VALIDATION, TEST_INFRA_INVALID]
receipt_freshness: [CURRENT, STALE, INVALID, UNVERIFIED]
```

This manifest is normative and must agree with the prose. Any later instruction
that contradicts it is a semantic failure in this skill itself.

---

## Phase 1: Load and validate testing authorities

Read raw bytes once and compute
`sha256:<64 lowercase hexadecimal characters>` for each selected authority:

- target `SKILL.md`;
- target `agents/openai.yaml`;
- `CGS Skill Testing Framework/catalog.yaml` and the exact target entry;
- the catalog-registered behavioral spec, when required;
- `CGS Skill Testing Framework/quality-rubric.md` and the exact category section,
  when required;
- this validator `SKILL.md` and its versioned rule sections;
- any pinned external validator manifest/binary/script actually used;
- every fixture or repository input used for an assertion.

Parse content from those same bytes. Never hash normalized, copied, or
user-supplied text.

### Authority status

Record every authority as `loaded`, `missing`, `unreadable`, `invalid`, or
`omitted`. Missing, unreadable, invalid, or omitted required authority prevents
`COMPLIANT`.

Do not guess a spec path. The catalog `spec:` field is authoritative. Validate
the catalog entry before using it:

- canonical skill name matches the target;
- exactly one normalized entry exists;
- category and spec path are non-empty;
- referenced spec remains inside the framework root;
- legacy result fields are evidence references only, never testing authority.

### Pinned validator handling

Run an external quick validator only when a trusted tool manifest provides its
exact path, version, raw-byte hash, allowed argv, timeout, and output schema.
Record argv, version, exit code, duration, stdout/stderr hashes, and parsed
result in the receipt.

If the manifest/tool is absent, its hash mismatches, it times out, or output
cannot be parsed, record reduced coverage as `PARTIAL_VALIDATION`. Continue safe
built-in checks, but never silently return `COMPLIANT`.

---

## Phase 2: Preflight behavioral spec authority

Before evaluating any target behavior, validate the registered spec against
`cgs-skill-spec/v2`.

### 2.1 Required spec structure

A valid spec must contain:

- unique `Spec ID`, `Spec Schema: cgs-skill-spec/v2`, category, priority, and
  spec-written date;
- Skill Summary with explicit input modes, owned outputs, non-writes, and verdict
  vocabulary;
- uniquely identified static assertions;
- a contiguous numbered Case sequence starting at 1;
- for every Case:
  - unique stable Case ID and non-empty title;
  - Fixture;
  - Input;
  - Expected reads;
  - Expected writes;
  - Expected non-writes;
  - Expected behavior;
  - one or more assertions with unique stable assertion IDs;
  - explicit Case Verdict vocabulary;
- uniquely identified Protocol Compliance assertions;
- Coverage Notes.

Case and assertion IDs must be unique under Unicode NFC normalization and
case-folding. Missing headings, empty sections, stray numbered steps outside a
Case, duplicate IDs, unclosed fences, or a non-contiguous Case sequence make the
spec `INVALID SPEC`.

### 2.2 Semantic spec lint

Build a structured model of modes, reads, writes, non-writes, operations,
verdicts, and state transitions. Reject contradictions, including:

- summary says read-only but any Case expects a write;
- one mode both requires and forbids the same path mutation;
- a success verdict is expected after a declined, failed, or unselected write;
- Case verdicts use vocabulary absent from the summary;
- fixture data cannot produce the expected branch;
- an assertion conflicts with the expected behavior;
- protocol assertions contradict a Case;
- write authorization is required after a write has already occurred;
- two Cases assign incompatible meanings to the same state.

Report each lint issue with stable rule ID, spec path, line, and conflicting
statements.

### 2.3 Infrastructure verdict

- `VALID SPEC` — schema and semantic lint both pass.
- `INVALID SPEC` — any schema or contradiction failure.
- `PARTIAL SPEC VALIDATION` — a required parser/authority was unavailable or
  input could not be fully parsed.

For `spec` mode, `INVALID SPEC` or `PARTIAL SPEC VALIDATION` stops target
behavior evaluation. Return `Validation: TEST_INFRA_INVALID` and name the spec
defects. Never grade only the assertions that happened to survive parsing, and
never return target `COMPLIANT` from invalid testing authority.

---

## Phase 3: Versioned structural validation

Structural rules are mechanical. Use rule set
`cgs-skill-structure/v2` and report every rule independently:

- `STR-001 FRONTMATTER_SCHEMA` — exactly non-empty `name` and `description`.
- `STR-002 PACKAGE_IDENTITY` — canonical folder and frontmatter names match the
  lowercase letters/digits/hyphen grammar and length limit.
- `STR-003 REQUIRED_FILES` — `SKILL.md` and `agents/openai.yaml` exist and parse.
- `STR-004 UI_SCHEMA` — exact required UI keys and target invocation syntax.
- `STR-005 MARKDOWN_STRUCTURE` — headings/fences/links are mechanically valid.
- `STR-006 PATH_EXISTENCE` — non-future referenced repository paths resolve.
- `STR-007 INVOCATION_TOKEN` — project-skill calls use exact `$name` syntax.

Structural validation does not decide whether a declared write set, state
machine, approval rule, or verdict is truthful. Keywords such as “read-only,”
“ask once,” or “COMPLETE” are not semantic proof.

### Template-aware placeholder parsing

Parse Markdown/code-fence context:

- placeholders inside an explicitly labelled output/template/example fence are
  allowed when the surrounding instructions say they are substituted;
- unresolved placeholders in active YAML/TOML/JSON, executable commands,
  invocation schemas, or normative contract fields fail;
- migration examples and quoted historical evidence are not active
  instructions but must be labelled as such.

Report the exact context classification. Do not fail a legal authoring template
merely because placeholder tokens exist.

---

## Phase 4: Semantic contract validation

Require a parseable `cgs-skill-contract/v1` manifest in every target skill.
Absence, duplicate fields, invalid paths/states, or an unparseable manifest is
`SEMANTIC CONTRACT INVALID` and prevents `COMPLIANT`.

Use versioned semantic rules:

- `SEM-001 MODE_CONTRACT` — prose invocation/modes match the manifest.
- `SEM-002 WRITE_SET` — every imperative write/edit/create/delete instruction in
  every phase targets a declared write; no declared non-write is mutated.
- `SEM-003 AUTHORIZATION_ORDER` — each write branch is authorized before its
  first mutation; read-only branches never ask for write approval.
- `SEM-004 RESULT_TRUTH` — success/updated/written claims require the matching
  selected operation and post-write verification.
- `SEM-005 STATE_MACHINE` — every status transition has one unambiguous trigger;
  failed, declined, unselected, stale, or partial branches cannot reach success.
- `SEM-006 VERDICT_TRUTH_TABLE` — prose verdicts equal the manifest vocabulary
  and deterministic aggregation rules.
- `SEM-007 CALL_CONTRACT` — each called workflow/agent names the owner, allowed
  side effect, input, output, and failure behavior.
- `SEM-008 OWNERSHIP` — no artifact has two writers inside the described
  workflow.
- `SEM-009 TEMPLATE_CONTEXT` — examples/templates cannot be mistaken for
  executable or normative state.
- `SEM-010 INTERNAL_CONTRADICTION` — scan all sections, not only top
  boilerplate, for mutually exclusive instructions.

For each rule, cite both the structured field and every supporting or
contradicting prose location. A top-level compliance sentence cannot cancel a
later silent write or false-success branch.

A target whose contract is invalid or whose semantic rule fails is
`NON-COMPLIANT` even when all structural rules pass.

---

## Phase 5: Mode execution

### 5.1 Static mode

For one target or all recursively discovered skills:

1. Load/hashes per Phase 1.
2. Run structural rules from Phase 3.
3. Run semantic contract rules from Phase 4.
4. Report Structural and Semantic results separately.

`static all` discovers recursively at `.agents/skills/**/SKILL.md`. Do not follow
directory symlinks. Exclude hidden/generated directories only through explicit
versioned exclusion rule IDs and report every excluded path.

### 5.2 Spec mode

1. Resolve the exact catalog-registered spec.
2. Run Phase 2 preflight.
3. Only for `VALID SPEC`, evaluate every Case and Protocol assertion.
4. Record `PASS`, `WARN`, `FAIL`, `INVALID`, or `PARTIAL` per stable assertion ID
   with direct evidence.
5. Record selected fixtures and exact hashes. Inline fixture blocks are hashed
   as exact spec byte ranges; filesystem fixtures are hashed from raw bytes.
6. Do not execute the target skill; evaluate its written contract and declared
   behavior against the fixture.

### 5.3 Category mode

Validate catalog and rubric structure before use. Read the category from the
unique catalog entry and the exact rubric section from current raw bytes.
Evaluate every metric independently. Contradictory, missing, or unparseable
rubric authority returns `TEST_INFRA_INVALID`, not a target pass.

### 5.4 Audit mode

Use one canonical discovery/normalization implementation for every set:

- skills: recursive `.agents/skills/**/SKILL.md`;
- skill metadata: sibling `agents/openai.yaml`;
- agents: recursive `.codex/agents/**/*.toml`, excluding generator helpers by
  explicit rule;
- catalog entries;
- registered skill and agent specs.

Canonical names use Unicode NFC, case-folding, and the lowercase
letters/digits/hyphen grammar. Detect duplicates before set comparison. Compare
exact normalized sets; totals alone never pass.

Report selected, loaded, failed, omitted, and excluded paths plus byte/file/time
budgets. Any required read failure, unvalidated exclusion, timeout, or budget
omission yields `PARTIAL_VALIDATION`. Derive current totals from the selected
sets; never require hard-coded historical counts.

---

## Phase 6: Deterministic aggregation

Per-rule outcomes are `PASS`, `WARN`, `FAIL`, `INVALID`, or `PARTIAL`. Aggregate
with this fixed priority:

1. Required testing authority `INVALID` → `TEST_INFRA_INVALID`.
2. Any target `FAIL` with valid infrastructure → `NON-COMPLIANT`.
3. Any `PARTIAL`, required validator loss, unreadable input, or omitted target
   with no stricter outcome → `PARTIAL_VALIDATION`.
4. Any `WARN` with all required coverage complete → `WARNINGS`.
5. `COMPLIANT` only when every required rule/assertion is `PASS` and all
   authority, validator, fixture, and discovery coverage is complete.

Never turn `INVALID`, `PARTIAL`, missing data, or an empty assertion set into
`COMPLIANT`.

Report two axes:

- `Operation: ANALYZED` until an optional receipt is verified written.
- `Validation: COMPLIANT | WARNINGS | NON-COMPLIANT | PARTIAL_VALIDATION |
  TEST_INFRA_INVALID`.

---

## Phase 7: Optional immutable receipt

### 7.1 Receipt schema

With `--persist-receipt`, generate
`cgs-skill-test-receipt/v2` containing:

- receipt ID, schema, timestamp, mode, target/scope, operation, validation;
- target `SKILL.md` path/hash;
- target `agents/openai.yaml` path/hash;
- catalog path/hash and exact target-entry byte-range hash;
- spec path/hash and `VALID SPEC` preflight result, or explicit N/A;
- rubric path/hash and category-section byte-range hash, or explicit N/A;
- validator skill path/hash, ruleset IDs/versions/hashes;
- external validator manifest/tool/version/hash/argv/exit/log hashes, or the
  explicit coverage reduction;
- fixture snapshot: every selected inline block/file path plus raw-byte/range
  hash;
- discovery selected/loaded/failed/omitted/excluded sets;
- every stable rule/assertion ID, outcome, evidence path/line, and message;
- aggregation trace;
- receipt content hash computed over the canonical receipt payload before its
  outer hash field.

The receipt is immutable. If its path already exists with different bytes, fail;
never overwrite or “refresh” it.

### 7.2 Freshness

When `--check-receipt [receipt-path]` is supplied, read that exact receipt.
Before displaying or referencing a persisted result, re-hash every dependency
recorded in the receipt. Any mismatch, disappearance, validator version change,
fixture change, or selected-set change makes freshness `STALE`. Missing or
malformed receipt data is `INVALID`; absent receipt is `UNVERIFIED`.

A stale, invalid, or unverified receipt cannot be displayed as current
`COMPLIANT`.

### 7.3 Write protocol

Show the complete receipt and exact one-file changeset, obtain one approval,
then immediately re-hash every dependency. Abort on any change. Write only the
new receipt, read it back byte-for-byte, and report its raw SHA-256.

- verified write → `Operation: RECEIPT_WRITTEN`;
- identical existing immutable receipt → `RECEIPT_UNCHANGED`;
- declined → `RECEIPT_DECLINED` while the in-conversation validation remains;
- conflict/write/read-back failure → `FAILED`.

### 7.4 Catalog safety

This version never writes `CGS Skill Testing Framework/catalog.yaml` and never
populates or repurposes legacy `last_*` date/result fields.

A future catalog schema may reference only an existing verified receipt ID and
receipt hash. Until that schema is independently migrated and validated, report
the missing reference capability; do not fabricate dates, PASS strings, receipt
IDs, hashes, or last-test results.

---

## Collaborative protocol

- Validate the testing authority before judging the target.
- Separate structural syntax, semantic truth, behavioral assertions, category
  metrics, and infrastructure health in every report.
- Cite exact rule/assertion IDs and file/line evidence.
- Never repair a target during validation; hand findings to its owning workflow.
- Never run the target skill as part of written-contract validation.
- Never persist by default and never update catalog `last_*` fields.
- End with the strict validation verdict, receipt freshness when applicable, and
  the smallest owner-specific remediation.
