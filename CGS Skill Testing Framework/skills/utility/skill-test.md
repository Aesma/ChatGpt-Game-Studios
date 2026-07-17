# Skill Test Spec: `$skill-test`

> **Category**: utility
> **Priority**: critical
> **Spec written**: 2026-07-18

## Skill Summary

`$skill-test` validates migrated Codex skills in four modes:

- `static [name|all]` checks package structure and the seven project rules.
- `spec [name]` evaluates the catalog-registered behavioral spec.
- `category [name|all]` applies `CGS Skill Testing Framework/quality-rubric.md`.
- `audit` compares implementations, catalog entries, UI metadata, agent TOML,
  and recursively discovered specs by unique name.

The validation pass is read-only. Persisting a result is optional and follows the
single bounded-changeset policy.

---

## Static Assertions

- [ ] YAML frontmatter contains exactly non-empty `name` and `description`
- [ ] The documented invocation is `$skill-test`
- [ ] Modes are `static`, `spec`, `category`, and `audit`
- [ ] Skill implementations are discovered at `.agents/skills/*/SKILL.md`
- [ ] Agent definitions are discovered recursively at `.codex/agents/**/*.toml`
- [ ] Behavioral spec paths come from `CGS Skill Testing Framework/catalog.yaml`
- [ ] The rubric path is `CGS Skill Testing Framework/quality-rubric.md`
- [ ] Audit compares unique names and reports missing and orphaned entries; it does not pass from totals alone
- [ ] Optional result persistence uses existing bounded task authorization, or one complete changeset preview and confirmation before writing

---

## Test Cases

### Case 1: Static Mode — compliant installed skill

**Fixture:**

- `.agents/skills/gate-check/SKILL.md` exists
- Its `agents/openai.yaml` exists

**Input:** `$skill-test static gate-check`

**Expected behavior:**

1. Run the installed quick validator when available.
2. Check frontmatter, folder identity, actionable instructions, UI metadata,
   Codex compatibility, collaboration boundary, and handoff/link integrity.
3. Cite file and line evidence for every warning or failure.
4. Return `COMPLIANT`, `WARNINGS`, or `NON-COMPLIANT`.

**Assertions:**

- [ ] All seven checks are evaluated independently
- [ ] A missing optional validator is reported without skipping the project checks
- [ ] Project skills invoked as legacy slash commands are rejected
- [ ] No validation output is persisted automatically

---

### Case 2: Static Mode — inline invalid fixture

**Fixture:** Evaluate this inline package description; no fixture path is required:

- folder: `Example_Skill/`
- frontmatter: `name: different-name`, no `description`, extra `model` key
- UI prompt invokes `/different-name`
- workflow writes two files and demands a separate confirmation for each

**Input:** `$skill-test static Example_Skill`

**Expected behavior:**

1. Fail frontmatter, identity, UI metadata, Codex compatibility, and collaboration boundary.
2. Explain every failure with the supplied fixture evidence.
3. Do not invent a catalog entry or behavioral spec for the fixture.

**Assertions:**

- [ ] Extra skill frontmatter fields fail
- [ ] Folder/name mismatch fails
- [ ] Legacy slash invocation fails
- [ ] Per-file re-prompting fails the bounded changeset rule
- [ ] Overall verdict is `NON-COMPLIANT`

---

### Case 3: Spec Mode — registered behavioral spec

**Fixture:**

- `CGS Skill Testing Framework/catalog.yaml` contains `design-review`
- The catalog's registered `spec` path exists

**Input:** `$skill-test spec design-review`

**Expected behavior:**

1. Resolve the implementation and spec from the catalog.
2. Read the complete registered spec.
3. Mark every behavioral assertion `PASS`, `PARTIAL`, or `FAIL` with evidence.
4. Stop with a missing-artifact result if the implementation, catalog entry, or
   spec is absent; do not guess another path.

**Assertions:**

- [ ] The catalog is the authority for spec routing
- [ ] Every case and protocol assertion receives a result
- [ ] Missing artifacts are not silently skipped

---

### Case 4: Category Mode — rubric is data-driven

**Fixture:** `gate-check` is categorized as `gate` in the catalog.

**Input:** `$skill-test category gate-check`

**Expected behavior:**

1. Read the skill's category from the catalog.
2. Read the `gate` metrics from `CGS Skill Testing Framework/quality-rubric.md`.
3. Evaluate every applicable metric independently.

**Assertions:**

- [ ] Rubric metrics are read from the framework file rather than duplicated in the skill
- [ ] Non-applicable metrics are explained rather than treated as silent passes

---

### Case 5: Audit Mode — complete recursive coverage

**Fixture:** The migrated repository currently contains:

- 74 `.agents/skills/*/SKILL.md` implementations
- 74 unique skill catalog entries and 74 registered skill specs
- 49 `.codex/agents/**/*.toml` role definitions, excluding generator helpers
- 49 unique agent catalog entries and 49 registered agent specs

**Input:** `$skill-test audit`

**Expected behavior:**

1. Discover all four implementation/spec sets recursively where applicable.
2. Compare normalized unique names, not only counts.
3. Report unregistered implementations, missing specs, orphaned specs, missing
   UI metadata, duplicate names, and stale result dates.
4. Include `$studio-status` and `$vertical-slice` in ordinary skill coverage.

**Assertions:**

- [ ] Coverage is exactly 74 skills and 49 Codex roles for this baseline
- [ ] Skill implementation, catalog, and spec name sets are equal
- [ ] Agent TOML, catalog, and spec name sets are equal
- [ ] Duplicate names fail even when aggregate totals match
- [ ] The audit compares the complete recursively discovered name sets

---

## Protocol Compliance

- [ ] Validation is read-only until optional persistence is explicitly selected
- [ ] Persisted results and catalog updates are presented as one complete changeset
- [ ] Existing bounded task authorization is honored without repeated prompts
- [ ] Findings include evidence, verdict, and the next corrective action

---

## Coverage Notes

This spec validates the workflow contract and repository coverage invariants. It
does not execute every target skill. Live behavioral execution can be added as a
separate harness without weakening the static, category, spec-routing, or set-
equality checks above.
