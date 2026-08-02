# Skill Test Spec: $create-epics

## Skill Summary

`$create-epics` maps approved in-scope systems to architectural modules and
produces one EPIC per module plus the existing epic index. Scope comes from
`systems-index.md`; a Summary heading is optional. In full mode PR-EPIC reviews
complete inline drafts and planned paths before any write.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] Output path remains `production/epics/[epic-slug]/EPIC.md`
- [ ] Epic identity is an architecture module, not automatically one system
- [ ] Full gate receives complete inline drafts and planned edits before writes
- [ ] Uses one complete changeset authorization

---

## Test Cases

### Case 1: Approved standard GDD without Summary

**Fixture:**
- `systems-index.md` maps an Approved system to `combat.md`
- `combat.md` has Overview but no Summary
- Architecture maps the system to Combat Runtime

**Assertions:**
- [ ] The system is in scope because of the systems index
- [ ] Overview is read when Summary is absent
- [ ] The valid GDD is not reported as ineligible

---

### Case 2: Two systems share one module

**Fixture:**
- Two in-scope systems map to the same architecture module
- Their TR requirements are distinct

**Assertions:**
- [ ] Exactly one EPIC draft is produced for the module
- [ ] Both systems/GDDs are represented
- [ ] Requirements are allocated once and not duplicated wholesale
- [ ] No path or slug collision is produced

---

### Case 3: Untraced Foundation/Core requirement blocks readiness

**Fixture:**
- A Foundation or Core epic contains an untraced requirement

**Assertions:**
- [ ] No placeholder ADR coverage is invented
- [ ] The EPIC draft status is Blocked, not Ready
- [ ] The blocking requirement is visible in the requirement table and preview

---

### Case 4: PR-EPIC receives exact pre-write candidates

**Fixture:**
- Review mode resolves to full
- Two epic drafts and one index edit are planned

**Assertions:**
- [ ] PR-EPIC receives each complete inline draft, planned final path, and complete planned index edit
- [ ] Planned paths are not described as existing files
- [ ] No skeleton, temporary epic, index edit, or other file is written before the gate
- [ ] Gate verdict is resolved before the one changeset authorization

---

### Case 5: PR-EPIC returns CONCERNS

**Assertions:**
- [ ] Specific concerns are shown before authorization
- [ ] User may revise, accept concerns, or stop
- [ ] Revised complete drafts are re-reviewed before writing
- [ ] Epics are not auto-written while the gate is unresolved

---

## Protocol Compliance

- [ ] systems-index mapping and GDD status determine scope
- [ ] One module produces one epic
- [ ] Untraced Foundation/Core requirements cannot produce Ready
- [ ] PR-EPIC is a write-before gate over exact inline candidates
- [ ] The complete file set is authorized once
- [ ] Ends with the existing `$create-stories [epic-slug]` handoff
