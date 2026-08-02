---
name: asset-audit
description: "Audits game assets for compliance with naming conventions, file size budgets, format standards, and pipeline requirements. Identifies orphaned assets, missing references, and standard violations."
---

## Invocation and execution

Invoke this workflow as `$asset-audit`.

Arguments: `[all|art|audio|vfx|shaders|data]`. Empty input defaults to `all`.
Normalize the category to lowercase. On any other value, stop before scanning
and list the accepted values.


## Phase 1: Read Standards

For every target asset, read the complete applicable standards chain:

1. `design/art/art-bible.md`, section `Asset Standards`, when present.
2. `docs/technical-preferences.md`, when present.
3. Every `AGENTS.md` from the repository root down to the asset's parent
   directory. The closest directory rule wins when rules conflict.

The examples in Phase 3 are defaults only when none of those project sources
defines the check. Never use a default to override a closer `AGENTS.md`, the art
bible, or technical preferences.

---

## Phase 2: Scan Asset Directories

For `all`, recursively scan every existing file under `assets/`, including
root-level files and existing categories not in the common list. For a named
category, scan only its corresponding existing directory:

- `art` → `assets/art/**/*`
- `audio` → `assets/audio/**/*`
- `vfx` → `assets/vfx/**/*`
- `shaders` → `assets/shaders/**/*`
- `data` → `assets/data/**/*`

Do not create a missing directory. Record missing directories, unreadable paths,
unsupported files, and an empty result as distinct scope outcomes. Zero assets
or a scan error is not a successful compliance result.

---

## Phase 3: Run Compliance Checks

For every applicable check, record one of `PASS`, `FAIL`, or `NOT CHECKED` plus
the evidence used. If a binary property cannot be read, a file cannot be parsed,
or a referenced schema does not exist, record `NOT CHECKED` and the reason; never
infer that the asset passed.

**Default naming examples (only when no project rule applies):**
- Art: `[category]_[name]_[variant]_[size].[ext]`
- Audio: `[category]_[context]_[name]_[variant].[ext]`
- All files must be lowercase with underscores

**File standards:**
- Textures: Power-of-two dimensions, correct format (PNG for UI, compressed for 3D), within size budget
- Audio: Correct sample rate, format (OGG for SFX, OGG/MP3 for music), within duration limits
- Data: Valid JSON/YAML, schema-compliant

**Unresolved-reference candidates:** Search existing source code, scenes,
prefabs/resources, data files, manifests, and asset specs for each asset's project
path, engine URI, and stable resource identifier. If no direct reference is found,
report `NO REFERENCE FOUND`; do not call the asset deletable because dynamic or
editor-bound references may not be searchable.

**Missing assets:** Extract references from the same repositories and normalize
engine URIs, project-relative paths, separators, and case rules to a project path
before testing existence. Ignore known imported/derived paths. Put references
that cannot be resolved in `NOT CHECKED` rather than reporting them as missing;
never report one normalized path as both missing and unreferenced.

---

## Phase 4: Output Audit Report

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]

## Check Evidence
| File | Check | Expected | Actual | Result |
|------|-------|----------|--------|--------|

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Assets With No Reference Found
| File | Evidence Searched | Result | Recommendation |
|------|-------------------|--------|----------------|

## Missing Assets (normalized reference points to absent file)
| Reference Location | Expected Path | Normalization Evidence | Result |
|-------------------|---------------|------------------------|--------|

## Unverified References
| Reference Location | Original Reference | Reason |
|-------------------|--------------------|--------|

## Recommendations
[Prioritized list of fixes]

## Verdict: [COMPLIANT / WARNINGS / NON-COMPLIANT]
```

`COMPLIANT` is allowed only when every applicable check was actually performed
and passed. Any `NOT CHECKED`, empty scan, unsupported file, or recoverable scan
error forces at least `WARNINGS`; a failed blocking format or normalized missing
reference produces `NON-COMPLIANT`. These three verdicts are the only overall
health classification; do not emit a second CLEAN/MINOR/NEEDS enum.

This skill is read-only — it produces a report but does not write files.

---

## Phase 5: Next Steps

- Fix naming violations using the patterns defined in AGENTS.md.
- Delete confirmed orphaned assets after manual review.
- Run `$content-audit` to cross-check asset counts against GDD-specified requirements.
