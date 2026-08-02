# Skill Test Spec: $ux-review

## Skill Summary

`$ux-review` is a read-only review of three routed document types: a normal UX
spec, `design/ux/hud.md`, and `design/ux/interaction-patterns.md`. Each type is
validated against its current authoritative template. Verdicts are APPROVED,
NEEDS REVISION, or MAJOR REVISION NEEDED.

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] The reviewer reads the matching current `.codex/docs/templates/` file
- [ ] The workflow remains read-only
- [ ] Verdict mapping is deterministic and blocker locations are reported

## Cases

### Case 1: Normal UX spec

- A non-reserved `design/ux/*.md` file matches the ux-spec template header and all current required sections.
- It has no blockers; advisory notes may exist.
- Expected: routed to UX spec checklist and APPROVED.

### Case 2: HUD

- `design/ux/hud.md` contains the current HUD template's substantive sections.
- Expected: routed to HUD, including HUD-specific visual-budget and context content; not reviewed as a normal screen.

### Case 3: Pattern library

- `design/ux/interaction-patterns.md` follows the current pattern-library template.
- Expected: routed to pattern-library checks; not reviewed as UX/HUD.

### Case 4: `all` with unsupported Markdown

- The directory contains the three supported kinds plus a Markdown file with no UX-template header.
- Expected: supported files receive their routed review; unsupported file is listed separately with no verdict.

### Case 5: Accessibility authority

- Central `design/accessibility-requirements.md` is missing/placeholder, or its committed tier conflicts with the spec header.
- Expected: missing authority yields `tier unknown` and never COMPLIANT; a conflict is a blocker. Only Basic/Standard/Comprehensive/Exemplary are accepted.

### Case 6: Verdict mapping

- Zero blockers => APPROVED, regardless of advisory count.
- Localized fixable blockers => NEEDS REVISION.
- Missing Purpose/Player Need, contradictory main flow/input/data ownership, or multiple substantively missing core template sections => MAJOR REVISION NEEDED.

## Protocol Compliance

- [ ] `all` never applies one checklist to every Markdown file
- [ ] Completeness headings come from current templates, not a copied 4-section/5-state schema
- [ ] Unsupported files receive no verdict
- [ ] Central accessibility requirements win over the reviewed document
- [ ] Every non-APPROVED result lists concrete blocker locations and a revision handoff
- [ ] No files are written
