# Skill Test Spec: $architecture-decision

## Skill Summary

`$architecture-decision` authors or retrofits an ADR using the complete existing
ADR template. New decisions are always drafted as `Proposed`; acceptance is a
separate lifecycle transition. In `full` review mode TD-ADR runs after the draft.
The ADR, selected GDD synchronization edits, architecture registry candidates,
and selected blocked-story status edits are previewed together before one
changeset authorization.

**Assertions:**
- [ ] The complete existing ADR template is used for new and retrofit drafts
- [ ] Engine version reference is stamped in the ADR
- [ ] TD-ADR follows APPROVE / CONCERNS / REJECT handling from `director-gates.md`
- [ ] New ADR Status remains Proposed after gate approval; Deprecated is not a valid status
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] ADR, GDD, registry, and story edits are all included in that preview; excluded files remain unchanged
3. User selects update or supersede
4. Skill does NOT silently create a duplicate ADR

**Assertions:**
- [ ] Skill detects the existing ADR before authoring begins
- [ ] User is offered update or supersede options — no silent duplicate
- [ ] If update: skill opens the existing ADR for section-by-section revision
- [ ] If supersede: new ADR references the superseded one in Related ADRs section

---

### Case 5: Director Gate — Gate outcome controls whether the draft can be written

**Fixture:**
- ADR draft is complete
- Three scenarios: TD-ADR APPROVE, CONCERNS, and REJECT

**Full mode, APPROVE:**
- ADR Status remains Proposed and the complete changeset may be previewed

**Assertions (approved):**
- [ ] ADR header shows `Status: Proposed`
- [ ] TD-ADR appears as APPROVE in output

**Full mode, TD-ADR returns CONCERNS:**
- The user chooses accept risk, revise and re-review, or stop

**Assertions (CONCERNS):**
- [ ] ADR frontmatter/header shows `Status: Proposed`
- [ ] Concerns are listed in output
- [ ] Concerns are not silently folded into the draft

**Full mode, TD-ADR returns REJECT:**
- [ ] No file is written and no changeset approval is offered for the rejected draft
- [ ] The workflow returns to drafting and requires TD-ADR to run again

**Lean/solo mode:**
- ADR Status is Proposed; TD-ADR is skipped

**Assertions (lean/solo):**
- [ ] ADR Status is Proposed in lean mode
- [ ] ADR Status is Proposed in solo mode
- [ ] No gate output appears in lean or solo mode

---

## Protocol Compliance

- [ ] Complete template authored before gate review
- [ ] Engine version stamped in ADR from `docs/engine-reference/`
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] TD-ADR runs in full mode and is noted as skipped in lean/solo
- [ ] Status lifecycle is exactly Proposed → Accepted → Superseded
- [ ] Retrofit inserts missing sections at template positions and replaces placeholders/illegal values while preserving valid content
- [ ] Ends with next-step handoff: `$architecture-review` or `$create-control-manifest`

---

## Coverage Notes

- ADR numbering (auto-incrementing NNN) is not independently fixture-tested —
  the skill reads existing ADR filenames to assign the next number.
- Related ADRs section linking (supersedes / related-to) is tested structurally
  via Case 4 but not all link types are individually verified.
- Registry and story candidates are discovered before the single changeset
  approval; no post-write prompt or unconditional story update is permitted.
