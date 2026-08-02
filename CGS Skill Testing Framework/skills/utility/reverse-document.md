# Skill Test Spec: $reverse-document

## Skill Summary

`$reverse-document` generates design or architecture documentation from existing
source code. It reads the specified source file(s), infers design intent from
class structure, method names, constants, and comments, and produces either a
GDD skeleton (for gameplay systems) or an architecture overview (for technical
systems). The output is a best-effort inference — magic numbers and undocumented
logic may result in a PARTIAL verdict.

The skill asks "May I apply the proposed changeset?" before creating the document.
No director gates apply. Verdicts: COMPLETE (clean inference), PARTIAL (some
fields are ambiguous and need human review).

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, PARTIAL
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
7. File written; verdict is COMPLETE

**Assertions:**
- [ ] All 8 required GDD sections are present in the output
- [ ] `max_health = 100` appears as a Tuning Knob
- [ ] Clamping formula is captured in the Formulas section
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. File written with PARTIAL markers; verdict is PARTIAL

**Assertions:**
- [ ] AMBIGUOUS VALUE annotations appear for magic numbers
- [ ] Sections needing human review are marked explicitly
- [ ] Verdict is PARTIAL (not COMPLETE)
- [ ] File is still written — PARTIAL is not a blocking failure

---

### Case 3: Multiple Interdependent Files — Cross-System Overview Produced

**Fixture:**
- User provides 2 source files: `combat_system.gd` and `damage_resolver.gd`
- The files reference each other (combat calls damage_resolver)

**Input:** `$reverse-document src/gameplay/combat_system.gd src/gameplay/damage_resolver.gd`

**Expected behavior:**
1. Skill reads both files and detects the dependency relationship
2. Skill produces a cross-system architecture overview (not individual GDDs)
3. Overview describes: Combat System → Damage Resolver interaction, shared
   interfaces, data flow between the two
4. Skill asks "May I apply the proposed changeset?"
5. Overview written after approval; verdict is COMPLETE (or PARTIAL if ambiguous)

**Assertions:**
- [ ] Both files are analyzed together (not as two separate docs)
- [ ] Cross-system dependency is documented in the output
- [ ] Output file is written to `docs/architecture/` (not `design/gdd/`)
- [ ] Verdict is COMPLETE or PARTIAL

---

### Case 4: Source File Not Found — Error

**Fixture:**
- `src/gameplay/inventory_system.gd` does not exist

**Input:** `$reverse-document src/gameplay/inventory_system.gd`

**Expected behavior:**
1. Skill attempts to read the specified file — not found
2. Skill outputs: "Source file not found: src/gameplay/inventory_system.gd"
3. Skill suggests checking the path or running `$map-systems` to identify
   the correct source file
4. No document is created

**Assertions:**
- [ ] Error message names the missing file with the full path
- [ ] Alternative suggestion (check path or `$map-systems`) is provided
- [ ] No file modification occurs
- [ ] No verdict is issued (error state)

---

### Case 5: Director Gate Check — No gate; reverse-document is a utility

**Fixture:**
- Well-structured source file exists

**Input:** `$reverse-document src/gameplay/health_system.gd`

**Expected behavior:**
1. Skill generates and writes the design doc
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE or PARTIAL — no gate verdict involved

---

## Protocol Compliance

- [ ] Reads source file(s) before generating any content
- [ ] Produces all 8 required GDD sections when target is a gameplay system
- [ ] Annotates ambiguous values with AMBIGUOUS VALUE markers
- [ ] Produces cross-system overview (not individual GDDs) for multiple files
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE (clean inference) or PARTIAL (ambiguous fields)

---

## Coverage Notes

- Architecture overview format (for technical/infrastructure systems) differs
  from GDD format; the inferred output type is determined by the nature of the
  source file (gameplay logic → GDD; engine/infra code → architecture doc).
- The case where a source file is readable but contains only auto-generated
  boilerplate with no meaningful logic is not tested; skill would likely produce
  a near-empty skeleton with a PARTIAL verdict.
- C# and Blueprint source files follow the same inference pattern as GDScript;
  language-specific differences are handled in the skill body.

## P0 Contract Coverage

- [ ] Inputs must resolve to an existing project-contained file/directory;
  generated output, binaries, denied/sensitive files, and empty valid input stop
  with zero writes.
- [ ] Design, architecture, and concept use the existing full `.codex/docs/templates/`
  paths; a missing template stops instead of producing a guessed structure.
- [ ] Observed implementation, user-stated intent, and gaps are distinct;
  intended behavior is never marked implemented without code/test evidence.
- [ ] A newly created design GDD updates the uniquely matching systems-index row
  in the same changeset, and an existing output target is never overwritten silently.

## P1 Contract Coverage

- [ ] Invocation requires one explicit type and one file/directory path; a
  directory may contain multiple files, but multiple positional paths fail usage.
- [ ] `design` produces a complete reverse-documented system GDD.
- [ ] Missing Verified By, Creator, Decision Makers, or author identity remains
  pending/unknown instead of being invented.
- [ ] Unconfirmed ADR alternatives are possible/unknown and never presented as
  historical decisions or reasons not chosen.
- [ ] Prototype outcome, effort, reuse, tester feedback, and quotes require an
  existing record or explicit user input; otherwise they are N/A.
- [ ] The entire output file is previewed before authorization.
- [ ] Follow-up commands are listed after write and never executed in this workflow.
