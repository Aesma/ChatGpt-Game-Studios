# Skill Test Spec: $ux-design

## Skill Summary

`$ux-design` is a guided, section-by-section UX spec authoring skill. It produces
user flow diagrams (described textually), interaction state definitions, wireframe
descriptions, and accessibility notes for a specified screen or HUD element. The
skill follows the skeleton-first pattern: it creates the file with all section
headers immediately, then fills each section through discussion and writes each
section to disk after user approval.

The skill has no inline director gates — `$ux-review` is the separate review step.
Treat the complete described file set as one bounded changeset: use existing task authorization, or preview and confirm it once before the first write.
already exists for the named screen, the skill offers to retrofit individual sections
rather than replace. Verdict is COMPLETE when all sections are written.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Screen/flow, HUD, and patterns modes instantiate the matching current `.codex/docs/templates/` file; no copied reduced skeleton is used
- [ ] Retrofit inventories headings from the same current template and never treats short real content as a placeholder
- [ ] Normal slugs are non-empty kebab-case segments inside `design/ux/` and cannot use separators, dot segments, absolute paths, `hud`, or `interaction-patterns`
- [ ] One authorization covers the UX target, session state, and known current-spec pattern-library edit; section approval is not a second write prompt
- [ ] Other specs are pattern sources only when persisted Approved/Implemented; a current-spec new pattern requires explicit user approval, the single library writer, and persistence before first review
4. All approved sections are written in sequence within the single bounded document changeset
5. After all sections are written, verdict is COMPLETE
6. Skill suggests running `$ux-review` as the next step

**Assertions:**
- [ ] Skeleton file is created first (with empty section bodies)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. Only that section is updated; other sections are preserved; verdict is COMPLETE

**Assertions:**
- [ ] Existing spec is detected and retrofit is offered
- [ ] User selects which section(s) to update
- [ ] Only the selected section is updated — other sections unchanged
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE

---

### Case 3: Dependency Gap — Spec references a system with no design doc

**Fixture:**
- User is authoring a UX spec for the inventory screen
- `design/gdd/inventory.md` does not exist

**Input:** `$ux-design inventory-screen`

**Expected behavior:**
1. Skill begins authoring the inventory screen UX spec
2. During the User Flows section, skill attempts to reference inventory system rules
3. Skill detects: "No GDD found for inventory system — UX spec has a DEPENDENCY GAP"
4. The dependency gap is flagged in the spec (noted inline: "DEPENDENCY GAP: inventory GDD")
5. Skill continues authoring with placeholder notes for the missing rules
6. Verdict is COMPLETE with advisory note about the dependency gap

**Assertions:**
- [ ] DEPENDENCY GAP label appears in the spec for the missing system doc
- [ ] Skill does NOT block on the missing GDD — it continues with placeholders
- [ ] Dependency gap is also noted in the skill output (not just in the file)
- [ ] Handoff suggests both `$ux-review` and writing the missing GDD

---

### Case 4: No Argument Provided — Usage error

**Fixture:**
- No argument provided with the skill invocation

**Input:** `$ux-design`

**Expected behavior:**
1. Skill detects no screen name or argument provided
2. Skill outputs a usage error: "Screen name required. Usage: `$ux-design [screen-name]`"
3. Skill provides examples: `$ux-design hud`, `$ux-design main-menu`, `$ux-design inventory`
4. No file is created; no "changeset authorization" is asked

**Assertions:**
- [ ] Usage error is clearly stated
- [ ] Example invocations are provided
- [ ] No file is created
- [ ] Skill does not attempt to proceed without an argument

---

### Case 5: Director Gate Check — No gate; ux-review is the separate review skill

**Fixture:**
- New screen spec with argument provided

**Input:** `$ux-design settings-menu`

**Expected behavior:**
1. Skill authors all sections of the settings menu UX spec
2. No director agents are spawned
3. No gate IDs appear in output during authoring

**Assertions:**
- [ ] No director gate is invoked during ux-design
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Creates skeleton file with all section headers before discussing content
- [ ] Discusses and drafts one section at a time
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Detects existing spec and offers retrofit path
- [ ] Ends with handoff to `$ux-review`
- [ ] Verdict is COMPLETE when all sections are written

---

## Coverage Notes

- Interaction state enumeration (normal/hover/focus/disabled/error) is a core
  requirement of each spec; the `$ux-review` skill checks for completeness.
- Wireframe descriptions are text-only (no images); image references may be
  added manually by a designer after the fact.
- Responsive layout concerns (different screen sizes) are noted as optional
  content and not assertion-tested here.
