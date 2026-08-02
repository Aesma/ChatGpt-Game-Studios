# Skill Test Spec: $design-system

## Skill Summary

`$design-system` authors one GDD incrementally. Before its first write it
authorizes the GDD plus conditional registry, systems-index, and active-session
edits. Per-section content approval occurs inside that file boundary. Full mode
uses the configured specialists and runs CD-GDD-ALIGN once after the complete
GDD; lean and solo skip those per-skill delegations.

---

## Static Assertions

- [ ] Any existing target path enters resume/retrofit instead of skeleton creation
- [ ] Selected incomplete non-placeholder bodies may be replaced precisely
- [ ] Initial changeset names all four possible existing target files
- [ ] CD-GDD-ALIGN runs once post-GDD in full only
- [ ] External review cannot be assumed to have returned in the authoring task

---

## Test Cases

### Case 1: Happy Path — new GDD with one complete authorization

**Assertions:**
- [ ] Before the skeleton write, the preview names GDD, registry, systems index, and active.md with conditional operations
- [ ] The skeleton is the first GDD write
- [ ] Later approved sections do not trigger repeated file authorization
- [ ] An unlisted file pauses the run for an expanded changeset
- [ ] Full mode runs CD-GDD-ALIGN once after the complete GDD

---

### Case 2: Retrofit an incomplete non-placeholder section

**Fixture:**
- Existing GDD has a short but non-placeholder Formulas body
- User selects only Formulas for replacement

**Assertions:**
- [ ] Existing full Formulas body is shown before selection
- [ ] The replacement draft targets only the Formulas section body
- [ ] Every unselected section remains byte-for-byte unchanged
- [ ] The existing file is not rebuilt from a skeleton

---

### Case 3: Plain system-name invocation finds an existing GDD

**Assertions:**
- [ ] Existing target detection does not require an explicit retrofit keyword
- [ ] The run enters resume/retrofit automatically
- [ ] No existing GDD is overwritten by a new skeleton

---

### Case 4: Lean and solo remain executable without specialists

**Assertions:**
- [ ] Every MANDATORY/Do-NOT specialist instruction is conditional on resolved mode
- [ ] Lean and solo draft in the current agent and display the applicable skip note
- [ ] D/H risk labels do not override the shared review mode
- [ ] CD-GDD-ALIGN is skipped in lean and solo

---

### Case 5: Full-mode post-GDD CD-GDD-ALIGN

**Assertions:**
- [ ] Gate runs once only after the complete GDD exists
- [ ] The gate does not run per section
- [ ] The complete GDD and pillar context are passed to the gate
- [ ] Unresolved gate results prevent a false completed review claim

---

### Case 6: Fresh-task design review is not imported implicitly

**Assertions:**
- [ ] Authoring completion writes systems-index status as Designed
- [ ] The task does not infer Approved or In Review from an unreachable external result
- [ ] A later caller with verifiable review output owns that status change

---

## Protocol Compliance

- [ ] Incremental section writes stay within one authorized file set
- [ ] Resume/retrofit never destroys unrelated existing content
- [ ] Full/lean/solo delegation behavior matches the shared mode contract
- [ ] Final systems-index status reflects only evidence available in this run
