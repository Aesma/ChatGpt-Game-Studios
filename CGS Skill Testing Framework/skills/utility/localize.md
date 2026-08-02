# Skill Test Spec: $localize

## Skill Summary

`$localize` manages the full localization pipeline: it extracts all player-facing
strings from source files, resolves one source-table format, and manages the
default JSON tables in `assets/data/strings/` when no project table exists. It
validates completeness across all locale files. For new languages, it creates
a locale file skeleton with all current strings as keys and empty values. For
existing locale files, it produces a diff showing additions, removals, and
changed keys.

The default translation files are `assets/data/strings/strings-[locale-code].json`;
an existing project format may be used only when it resolves to one source of
truth. Files are written after a "May I apply the proposed changeset?"
5. File written on approval; verdict is GAPS FOUND (file created but empty values)
6. Skill notes: "strings-fr.json created — send to translator to fill values"

**Assertions:**
- [ ] All string keys from `strings-en.json` are present in `strings-fr.json`
- [ ] All values in `strings-fr.json` are empty (not copied from English)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. File updated with new empty keys added, obsolete keys marked; verdict is GAPS FOUND

**Assertions:**
- [ ] New keys appear as empty in the updated file (not auto-translated)
- [ ] Removed keys are flagged as obsolete (not silently deleted)
- [ ] Changed source strings are flagged for translator review
- [ ] Verdict is GAPS FOUND (new empty keys exist)

---

### Case 3: String Missing in One Locale — GAPS FOUND With Missing Key List

**Fixture:**
- 3 locale files exist: `strings-en.json`, `strings-fr.json`, `strings-de.json`
- `strings-de.json` is missing 4 keys that exist in both source and French tables

**Input:** `$localize validate`

**Expected behavior:**
1. Skill reads all 3 locale files and cross-references keys
2. `strings-de.json` is missing 4 keys
3. Skill produces GAPS FOUND report listing the 4 missing keys by locale:
   "strings-de.json missing: [key1], [key2], [key3], [key4]"
4. Skill offers to add the missing keys as empty values to `strings-de.json`
5. After approval: file updated; verdict remains GAPS FOUND (values still empty)

**Assertions:**
- [ ] Missing keys are listed explicitly (not just a count)
- [ ] Missing keys are attributed to the specific locale file
- [ ] Verdict is GAPS FOUND (not LOCALIZATION COMPLETE)
- [ ] Missing keys are added as empty (not auto-translated from English)

---

### Case 4: Translation File Has Syntax Error — Error With Line Reference

**Fixture:**
- `assets/data/strings/strings-fr.json` has malformed JSON at line 47
  (missing quote closure)

**Input:** `$localize validate`

**Expected behavior:**
1. Skill reads `strings-fr.json` and encounters a parse error at line 47
2. Skill outputs: "Parse error in strings-fr.json at line 47: [error detail]"
3. Skill cannot diff or validate the file until the error is fixed
4. Skill does NOT attempt to overwrite or auto-fix the malformed file
5. Skill suggests fixing the file manually and re-running `$localize`

**Assertions:**
- [ ] Error message includes line number (line 47)
- [ ] Error detail describes the nature of the parse error
- [ ] Skill does NOT overwrite or modify the malformed file
- [ ] Manual fix + re-run is suggested as remediation

---

### Case 5: Director Gate Check — No gate; localization is a pipeline utility

**Fixture:**
- Source code with player-facing strings

**Input:** `$localize extract`

**Expected behavior:**
1. Skill extracts strings and manages locale files
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is LOCALIZATION COMPLETE or GAPS FOUND — no gate verdict

---

## P1 Regression Assertions

- [ ] Extract scans hardcoded player-visible text plus localized references and excludes logs/tests/editor-only copy
- [ ] New-entry context contains only confirmed UI/call-site facts; unknown limits/gender are explicit TODO/unknown and prevent COMPLETE
- [ ] Any source/locale/manifest parse error reports file/location, blocks diff/write, and preserves the original
- [ ] Cultural review requires locales; optional saved output uses one deterministic `production/localization/cultural-review-...` path
- [ ] VO manifests/scripts use deterministic `production/localization/` paths; validate/integrate stop on missing locale/directory/manifest
- [ ] VO Recorded requires a readable non-empty key/locale-matching file and never implies recording quality
- [ ] RTL check runs only for explicit RTL locales and one configured engine; unconfigured engine reports limited coverage
- [ ] Status counts freeze violations only from parseable Post-Freeze Changes entries, otherwise unknown
- [ ] Translation files are not auto-translated/overwritten; authorized empty keys, obsolete markers, and source updates are allowed
- [ ] At most one localization-lead delegation path is used per run; fallback cannot fabricate human QA/reviewer/sign-off

## Protocol Compliance

- [ ] Extracts strings from source before operating on locale files
- [ ] Creates new locale files with all keys as empty values (not auto-translated)
- [ ] Diffs existing locale files against current source strings
- [ ] Flags missing keys by locale and by key name
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is LOCALIZATION COMPLETE (all locales fully translated) or GAPS FOUND
- [ ] `brief`, `cultural-review`, `vo-pipeline`, `rtl-check`, `freeze`, and `qa` reject missing or unknown required arguments without writing
- [ ] Active-freeze extraction previews the source-table and freeze-status edits together before either write
- [ ] A QA plan without executed evidence has no PASS/PASS WITH CONDITIONS verdict and no producer sign-off

---

## Coverage Notes

- LOCALIZATION COMPLETE is only achievable when all locale files have all keys
  with non-empty values; new-language skeleton creation always results in GAPS FOUND.
- Existing engine-specific locale formats may be used only as the project's one
  resolved source of truth; JSON is the canonical fallback format in tests.
- The case where source strings change at a very high rate (continuous integration
  of new UI text) is not tested; the diff logic handles this case.
