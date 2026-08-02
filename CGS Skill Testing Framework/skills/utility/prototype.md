# Skill Test Spec: $prototype

## Skill Summary

`$prototype` manages a rapid prototyping workflow for validating a game mechanic
before committing to full production implementation. Prototypes are created in
`prototypes/[mechanic-name]/` and are intentionally disposable — coding standards
are relaxed (no ADR required, AC can be minimal, hardcoded values acceptable).
After implementation, the skill produces a findings document summarizing what
was learned and recommending next steps.

The skill asks "May I apply the proposed changeset?" before creating files. If a
prototype already exists, the skill offers to extend, replace, or archive. Full
concept mode uses CD-PLAYTEST to review the draft evidence; lean/solo and spike
mode do not. Verdicts: PROTOTYPE COMPLETE (prototype built and findings
documented) or PROTOTYPE ABANDONED (mechanic found to be unworkable).

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: PROTOTYPE COMPLETE, PROTOTYPE ABANDONED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
2. After approval: creates `prototypes/grapple-hook/` directory and basic
   implementation skeleton (main scene, player controller extension)
3. Skill implements a minimal grapple hook mechanic (intentionally rough — no
   polish, hardcoded values acceptable)
4. Skill produces `prototypes/grapple-hook/findings.md` with:
   - What was tested
   - What worked
   - What didn't work
   - Recommendation (proceed / abandon / revise concept)
5. Verdict is PROTOTYPE COMPLETE

**Assertions:**
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Implementation is isolated to `prototypes/` (not `src/`)
- [ ] `findings.md` is created with at minimum: tested/worked/didn't-work/recommendation
- [ ] Verdict is PROTOTYPE COMPLETE

---

### Case 2: Prototype Already Exists — Offers Extend, Replace, or Archive

**Fixture:**
- `prototypes/grapple-hook/` already exists from a previous prototype session
- It contains a basic implementation and a findings.md

**Input:** `$prototype grapple-hook`

**Expected behavior:**
1. Skill detects existing `prototypes/grapple-hook/` directory
2. Skill reports: "Prototype already exists for grapple-hook"
3. Skill presents 3 options:
   - Extend: add new features to the existing prototype
   - Replace: start fresh (asks "May I replace `prototypes/grapple-hook/`?")
   - Archive: move to `prototypes/archive/grapple-hook/` and start fresh
4. User selects; skill proceeds accordingly

**Assertions:**
- [ ] Existing prototype is detected and reported
- [ ] Exactly 3 options are presented (extend, replace, archive)
- [ ] Replace path includes a "May I replace" confirmation
- [ ] Archive path moves (not deletes) the existing prototype

---

### Case 3: Prototype Validates Mechanic — Recommends Proceeding to Production

**Fixture:**
- Prototype implementation complete
- Findings: grapple hook mechanic is fun and technically feasible

**Input:** `$prototype grapple-hook` (prototype session complete)

**Expected behavior:**
1. After prototype is built and tested, findings are summarized
2. Recommendation in findings.md: "Mechanic validated — recommend proceeding
   to `$design-system` for full specification"
3. Skill handoff message explicitly suggests `$design-system grapple-hook`
4. Verdict is PROTOTYPE COMPLETE

**Assertions:**
- [ ] `findings.md` contains an explicit recommendation
- [ ] Recommendation references `$design-system` when mechanic is validated
- [ ] Handoff message echoes the recommendation
- [ ] Verdict is PROTOTYPE COMPLETE (not PROTOTYPE ABANDONED)

---

### Case 4: Prototype Reveals Mechanic is Unworkable — PROTOTYPE ABANDONED

**Fixture:**
- Prototype implemented for "procedural-dialogue"
- After testing: the mechanic creates incoherent dialogue trees and is
  frustrating to play

**Input:** `$prototype procedural-dialogue`

**Expected behavior:**
1. Prototype is built
2. Findings document the failure: incoherent output, player confusion, technical complexity
3. Recommendation in findings.md: "Mechanic not viable — abandoning"
4. `findings.md` documents the specific reasons the mechanic failed
5. Skill suggests alternatives in the handoff (e.g., curated dialogue instead)
6. Verdict is PROTOTYPE ABANDONED

**Assertions:**
- [ ] Verdict is PROTOTYPE ABANDONED (not PROTOTYPE COMPLETE)
- [ ] `findings.md` documents specific failure reasons (not vague)
- [ ] Alternative approaches are suggested in the handoff
- [ ] Prototype files are retained (not deleted) for reference

---

### Case 5: Director Gate Check — Standard verdicts, user owns recommendation

**Fixture:**
- Mechanic concept provided

**Input:** `$prototype wall-jump`

**Expected behavior:**
1. Skill creates an in-memory report draft after real playtest observations
2. In full mode CD-PLAYTEST reviews the draft and returns only APPROVE/CONCERNS/REJECT
3. The gate cannot return or override PROCEED/PIVOT/KILL; concerns go back to the user
4. REPORT/index/outcome files are previewed and written only after review is resolved

**Assertions:**
- [ ] Full mode uses only the standard CD-PLAYTEST gate verdicts
- [ ] The user, not the director, owns the final PROCEED/PIVOT/KILL recommendation
- [ ] Lean/solo concept mode and spike mode do not invoke the gate

---

## Protocol Compliance

- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Creates all files under `prototypes/` (not `src/`)
- [ ] Produces `findings.md` with tested/worked/didn't-work/recommendation
- [ ] Notes that production coding standards are intentionally relaxed
- [ ] Offers extend/replace/archive when prototype already exists
- [ ] Verdict is PROTOTYPE COMPLETE or PROTOTYPE ABANDONED
- [ ] `--spike` loads the continuation and reaches Spike Mode before any concept-phase write
- [ ] HTML, Markdown, and engine files use legal format-specific prototype comments
- [ ] Session state and initial build files are previewed together before their first write
- [ ] The post-playtest REPORT/index/applicable outcome files form one second bounded write batch after CD review
- [ ] A simulated Paper walkthrough is labelled non-player evidence and cannot produce a player-experience recommendation without real tester observations

---

## Coverage Notes

- Prototype implementation quality (code style) is intentionally not tested —
  prototypes are throwaway artifacts and quality standards do not apply.
- The archiving mechanism is mentioned in Case 2 but the archive format is
  not assertion-tested in detail.
- Engine-specific prototype scaffolding (GDScript scenes vs. C# MonoBehaviour)
  follows the same flow with engine-appropriate file types.
