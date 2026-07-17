# Skill Test Spec: $asset-audit

## Skill Summary

`$asset-audit` audits the `assets/` directory for naming convention compliance,
missing metadata, and format/size issues. It reads asset files against the
conventions and budgets defined in `technical-preferences.md`. No director gates
are invoked. The skill does not write outside the authorized changeset. Verdicts: COMPLIANT,
WARNINGS, or NON-COMPLIANT.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLIANT, WARNINGS, NON-COMPLIANT
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Technical artist consultation is suggested (not mandated)
- [ ] Findings table is presented before any write prompt
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

## Protocol Compliance

- [ ] Reads `technical-preferences.md` for naming conventions, formats, and size budgets
- [ ] Scans `assets/` directory recursively
- [ ] Audit table shows file name, check type, expected value, actual value, and result
- [ ] Does not modify any asset files
- [ ] No director gates are invoked
- [ ] Verdict is one of: COMPLIANT, WARNINGS, NON-COMPLIANT

---

## Coverage Notes

- Metadata checks (e.g., missing texture import settings in Godot `.import` files)
  are not explicitly tested here; they follow the same FORMAT ISSUE flagging pattern.
- The interaction between `$asset-audit` and `$content-audit` (both check GDD
  references vs. assets) is intentional overlap; `$asset-audit` focuses on
  compliance while `$content-audit` focuses on completeness.
