# Skill Test Spec: $adopt

## Skill Summary

`$adopt` audits an existing project's artifacts — GDDs, ADRs, stories, infrastructure
files, and `technical-preferences.md` — for format compliance with the template's
skill pipeline. It classifies every gap by severity (BLOCKING / HIGH / MEDIUM / LOW),
composes a numbered, ordered migration plan, and writes it to `docs/adoption-plan-[date].md`
after explicit user approval via `user-input request`.

This skill is distinct from `$project-stage-detect` (which checks what exists).
`$adopt` checks whether what exists will actually work with the template's skills.

No director gates apply. The skill does NOT invoke any director agents.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains severity tier keywords: BLOCKING, HIGH, MEDIUM, LOW
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
   - Options: "Run `$start`", "My artifacts are in a non-standard location", "Cancel"
4. Skill stops — does not proceed to audit regardless of user selection

**Assertions:**
- [ ] `user-input request` is used (not a plain text message) when no artifacts are found
- [ ] `$start` is presented as a named option
- [ ] Skill stops after the question — no audit phases run
- [ ] No adoption plan file is written

---

### Case 5: Director Gate Check — No gate; adopt is a utility audit skill

**Fixture:**
- Project with a mix of compliant and non-compliant GDDs

**Input:** `$adopt`

**Expected behavior:**
1. Skill completes full audit and produces migration plan
2. No director agents are spawned at any point
3. No gate IDs (CD-*, TD-*, AD-*, PR-*) appear in output
4. No `$gate-check` is invoked during the skill run

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Skill reaches plan-writing or cancellation without any gate verdict

---

## Protocol Compliance

- [ ] Emits "Scanning project artifacts..." before silent read phase
- [ ] Reads all artifacts silently before presenting any results
- [ ] Shows Adoption Audit Summary and Gap Preview before asking to write
- [ ] Uses `user-input request` before applying a not-yet-authorized changeset the adoption plan file
- [ ] Adoption plan written to `docs/adoption-plan-[date].md` — not to any other path
- [ ] Migration plan items ordered: BLOCKING first, HIGH second, MEDIUM third, LOW last
- [ ] Phase 7 always offers a single specific next action (not a generic list)
- [ ] Never regenerates existing artifacts — only fills gaps in what exists
- [ ] Does not invoke director gates at any point

---

## Coverage Notes

- The `gdds`, `adrs`, `stories`, and `infra` argument modes narrow the audit scope;
  each follows the same pattern as the full audit but limited to that artifact type.
  Not separately fixture-tested here.
- The systems-index.md parenthetical status value check (BLOCKING) is a special case
  that triggers an immediate fix offer before applying a not-yet-authorized changeset the plan; not separately tested.
- The review-mode.txt prompt (Phase 6b) runs after plan writing if `production/review-mode.txt`
  does not exist; not separately tested here.
