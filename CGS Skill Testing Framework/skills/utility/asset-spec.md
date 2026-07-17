# Skill Test Spec: $asset-spec

## Skill Summary

`$asset-spec` generates per-asset visual specification documents from design
requirements. It reads the relevant GDD, art bible, and design system to produce
a structured asset spec sheet that defines: dimensions, animation states (if
applicable), color palette reference, style notes, technical constraints
(format, file size budget), and deliverable checklist.

Spec sheets are written to `assets/specs/[asset-name]-spec.md` after a "May I apply the proposed changeset?"
4. File written on approval; verdict is COMPLETE

**Assertions:**
- [ ] All 6 spec components are present (dimensions, animations, palette, style, tech, checklist)
- [ ] Color palette reference links to art bible (not duplicated)
- [ ] Animation states are drawn from GDD (not invented)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. File written with placeholders and dependency flag; verdict is COMPLETE with advisory

**Assertions:**
- [ ] DEPENDENCY GAP is flagged for the missing art bible
- [ ] Spec is still generated (not blocked)
- [ ] Style notes contain placeholder markers, not invented styles
- [ ] Verdict is COMPLETE with advisory note

---

### Case 3: Asset Spec Already Exists — Offers to Update

**Fixture:**
- `assets/specs/goblin-enemy-spec.md` already exists
- GDD has been updated since the spec was written (new attack animation added)

**Input:** `$asset-spec goblin-enemy`

**Expected behavior:**
1. Skill detects existing spec file
2. Skill reports: "Asset spec already exists for goblin-enemy — checking for updates"
3. Skill diffs GDD against existing spec and identifies: new "charge-attack" animation
   state added in GDD but not in spec
4. Skill presents the diff: "1 new animation state found — offering to update spec"
5. Skill asks "May I apply the proposed changeset?" (not overwrite)
6. Spec is updated; verdict is COMPLETE

**Assertions:**
- [ ] Existing spec is detected and "update" path is offered
- [ ] Diff between GDD and existing spec is shown
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User can approve all 3 or skip individual assets
4. All approved specs are written; verdict is COMPLETE

**Assertions:**
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] User can decline one asset without blocking the others
- [ ] All 3 spec files are written for approved assets
- [ ] Verdict is COMPLETE when all approved specs are written

---

### Case 5: Director Gate Check — No gate; asset-spec is a design utility

**Fixture:**
- GDD and art bible exist

**Input:** `$asset-spec goblin-enemy`

**Expected behavior:**
1. Skill generates and writes the asset spec
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Reads GDD, art bible, and design system before generating spec
- [ ] Includes all 6 spec components (dimensions, animations, palette, style, tech, checklist)
- [ ] Flags missing dependencies (art bible, GDD) with DEPENDENCY GAP notes
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Handles multiple assets with individual write confirmations
- [ ] Verdict is COMPLETE when all approved specs are written

---

## Coverage Notes

- Audio asset specs (sound effects, music) follow the same structure with
  different fields (duration, sample rate, looping) and are not separately tested.
- UI asset specs (icons, button states) follow the same flow with interaction
  state requirements aligned to the UX spec.
- The case where GDD is also missing (neither GDD nor art bible exists) is not
  separately tested; spec would be generated with both dependency gaps flagged.
