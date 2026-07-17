# Skill Test Spec: $architecture-decision

## Skill Summary

`$architecture-decision` guides the user through section-by-section authoring of
a new Architecture Decision Record (ADR). Required sections are: Status, Context,
Decision, Consequences, Alternatives, and Related ADRs. The skill also stamps the
engine version reference from `docs/engine-reference/` into the ADR for traceability.

In `full` review mode, TD-ADR (technical-director) and LP-FEASIBILITY
(lead-programmer) gate agents spawn after the draft is complete. If both gates
return APPROVED, the ADR status is set to Accepted. In `lean` or `solo` mode,
both gates are skipped and the ADR is written with Status: Proposed. The skill
asks "May I apply the proposed changeset?" asked, approved
4. After all sections: TD-ADR and LP-FEASIBILITY gates spawn in parallel
5. Both gates return APPROVED
6. ADR Status is set to Accepted
7. Skill writes `docs/architecture/adr-NNN-rendering-approach.md`
8. `docs/architecture/tr-registry.yaml` updated if new TR-IDs are defined

**Assertions:**
- [ ] All 6 required sections are authored and written
- [ ] Engine version reference is stamped in the ADR
- [ ] TD-ADR and LP-FEASIBILITY spawn in parallel (not sequentially)
- [ ] ADR Status is Accepted when both gates return APPROVED in full mode
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User selects update or supersede
4. Skill does NOT silently create a duplicate ADR

**Assertions:**
- [ ] Skill detects the existing ADR before authoring begins
- [ ] User is offered update or supersede options — no silent duplicate
- [ ] If update: skill opens the existing ADR for section-by-section revision
- [ ] If supersede: new ADR references the superseded one in Related ADRs section

---

### Case 5: Director Gate — Status set correctly based on mode and gate outcome

**Fixture:**
- ADR draft is complete
- Two scenarios: (a) full mode, both gates APPROVED; (b) full mode, one gate CONCERNS

**Full mode, both APPROVED:**
- ADR Status is set to Accepted

**Assertions (both approved):**
- [ ] ADR frontmatter/header shows `Status: Accepted`
- [ ] Both TD-ADR and LP-FEASIBILITY appear as APPROVED in output

**Full mode, one gate returns CONCERNS:**
- ADR Status stays Proposed

**Assertions (CONCERNS):**
- [ ] ADR frontmatter/header shows `Status: Proposed`
- [ ] Concerns are listed in output
- [ ] Skill does NOT set Status: Accepted when any gate returns CONCERNS

**Lean/solo mode:**
- ADR Status is always Proposed regardless of content quality

**Assertions (lean/solo):**
- [ ] ADR Status is Proposed in lean mode
- [ ] ADR Status is Proposed in solo mode
- [ ] No gate output appears in lean or solo mode

---

## Protocol Compliance

- [ ] All 6 required sections authored before gate review
- [ ] Engine version stamped in ADR from `docs/engine-reference/`
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] TD-ADR and LP-FEASIBILITY spawn in parallel in full mode
- [ ] Skipped gates noted by name and mode in lean/solo output
- [ ] ADR Status: Accepted only when full mode AND both gates APPROVED
- [ ] Ends with next-step handoff: `$architecture-review` or `$create-control-manifest`

---

## Coverage Notes

- ADR numbering (auto-incrementing NNN) is not independently fixture-tested —
  the skill reads existing ADR filenames to assign the next number.
- Related ADRs section linking (supersedes / related-to) is tested structurally
  via Case 4 but not all link types are individually verified.
- The TR-registry update (when new TR-IDs are defined in the ADR) is part of the
  write phase — tested implicitly via Case 1.
