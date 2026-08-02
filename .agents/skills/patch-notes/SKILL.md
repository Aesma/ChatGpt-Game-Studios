---
name: patch-notes
description: "Generate player-facing patch notes from git history, sprint data, and internal changelogs. Translates developer language into clear, engaging player communication."
---

## Invocation and execution

Invoke this workflow as `$patch-notes`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[version] [--style brief|detailed|full]`. Treat bracketed values as optional unless the workflow says otherwise.

Use the `community-manager` Codex subagent role, when available, only for a read-only tone review of the in-memory draft. It has no write permission and is not a director gate. If unavailable, the current agent performs the same tone review and reports the fallback. User authorization still controls the final two-file write.


## Phase 1: Parse Arguments

- `version`: exactly one release version identifier (e.g., `1.2.0`). Reject path separators, traversal segments, whitespace-separated extra targets, and unknown flags with **BLOCKED** before constructing any path
- `--style`: output style — `brief` (bullet points), `detailed` (with context), `full` (with developer commentary). Default: `detailed`.

If no version is provided, ask the user before proceeding. Resolve exactly one release target for that version. Use a Git range only when both that target and its immediately preceding release ref are unique. If the target tag does not exist, label the result throughout as an **unreleased draft at current HEAD**. If the preceding ref is ambiguous, ask the user; never guess the range.

---

## Phase 2: Gather Change Data

- Use `production/releases/[version]/changelog.md` as the primary source when it exists
- Use the matching `docs/CHANGELOG.md` version entry only to supplement missing details
- Use `git log` only as a fallback over the uniquely resolved immediately-previous-release ref through the uniquely resolved target; current HEAD is permitted only for an explicitly labelled unreleased draft
- Read sprint retrospectives in `production/sprints/` for context
- Read any balance change documents in `design/balance/`
- Read bug fix records from QA if available

Deduplicate the collected entries by an explicit issue/change ID when available,
otherwise by the same normalized description. When sources disagree on scope,
values, or release status, show the conflict to the user and do not silently pick
one source. Primary-source precedence does not authorize concealing a conflict.

**If no changelog data is available** (neither `production/releases/[version]/changelog.md`
nor a `docs/CHANGELOG.md` entry for this version exists, and git log is empty or unavailable):

> "No changelog data found for [version]. Run `$changelog [version]` first to generate the
> internal changelog, then re-run `$patch-notes [version]`."

Verdict: **BLOCKED** — stop here without generating notes.

---

## Phase 2b: Detect Tone Guide and Template

**Tone guide detection** — before drafting notes, check for writing style guidance:

1. Check `docs/technical-preferences.md` for any "tone", "voice", or "style"
   fields or sections.
2. Check `docs/PATCH-NOTES-STYLE.md` if it exists.
3. Check `design/community/tone-guide.md` if it exists.
4. If any source contains tone/voice/style instructions, extract them and apply
   them to the language and framing of the generated notes.
5. If no tone guidance is found anywhere, default to:
   player-friendly, non-technical language; enthusiastic but not hyperbolic;
   focus on what the player experiences, not what the developer changed.

**Template detection** — check whether a patch notes template exists:

1. Check for a project-provided `docs/patch-notes-template.md`.
2. If found, read it and use it as the output structure for Phase 4
   instead of the built-in style templates (Brief / Detailed / Full). The template
   controls structure; the detected tone guide controls wording. Fill only sections
   supported by source data. Omit or leave clearly empty any unsupported template
   request and explain the gap rather than inventing content.
3. If not found, use the built-in style templates as defined in Phase 4.

---

## Phase 3: Categorize and Translate

Categorize all changes into player-facing categories:

- **New Content**: new features, maps, characters, items, modes
- **Gameplay Changes**: balance adjustments, mechanic changes, progression changes
- **Quality of Life**: UI improvements, convenience features, accessibility
- **Bug Fixes**: grouped by system (combat, UI, networking, etc.)
- **Performance**: optimization improvements players might notice
- **Known Issues**: include only issues explicitly listed for this release or supported by an existing open bug record. Include a workaround only when that source provides one; otherwise omit it

Translate developer language to player language without inventing effects:

- Use a player-observable result only when changelog, bug, or test evidence explicitly states it.
- Pure refactors, allocation changes, and other internal work are excluded by default.
- If an internal change may affect players but the evidence does not say how, list it under excluded/needs clarification for the user; do not supply a benefit.
- Preserve before/after balance values only when the source provides both. When one side is absent, use only the verifiable description and mark the missing side for confirmation; never calculate it.

---

## Phase 4: Generate Patch Notes

### Brief Style
```markdown
# Patch [Version] — [Title]

**New**
- [Feature 1]
- [Feature 2]

**Changes**
- [Balance/mechanic change with before → after values]

**Fixes**
- [Bug fix 1]
- [Bug fix 2]

**Known Issues**
- [Issue 1]
```

### Detailed Style
```markdown
# Patch [Version] — [Title]
*[Date]*

## Highlights
[1-2 sentence summary of the most exciting changes]

## New Content
### [Feature Name]
[2-3 sentences describing the feature and why players should be excited]

## Gameplay Changes
### Balance
| Change | Before | After | Reason |
| ---- | ---- | ---- | ---- |
| [Item/ability] | [old value] | [new value] | [brief rationale] |

### Mechanics
- **[Change]**: [explanation of what changed and why]

## Quality of Life
- [Improvement with context]

## Bug Fixes
### Combat
- Fixed [description of what players experienced]

### UI
- Fixed [description]

### Networking
- Fixed [description]

## Performance
- [Improvement players will notice]

## Known Issues
- [Issue and workaround if available]
```

### Full Style
Includes everything from Detailed. Add Developer Commentary only by editing commentary already present in a changelog, retrospective, or supplied by the user. Preserve its attribution. If no source exists, omit that section or leave an explicit user-fill placeholder; never invent first-person team statements, motives, tradeoffs, or quotations.

---

## Phase 5: Review Output

Check the generated notes for:

- No internal jargon (replace technical terms with player-friendly language)
- No references to internal systems, tickets, or sprint numbers
- Balance changes include before/after values
- Bug fixes describe the player experience, not the technical cause
- Tone matches the game's voice (adjust formality based on game style)

---

## Phase 6: Save Patch Notes

Present the completed patch notes to the user along with: a count of changes by category, and any internal changes that were excluded (for review).

If every collected entry is internal/non-player-facing, state clearly that there
are zero verified player-facing changes and ask the user to stop or save a short
factual notice. Do not populate sections with invented player value.

If the user refuses the changeset, state `draft generated, not saved`, output **BLOCKED**, and stop without either file.

The complete changeset must list both `docs/patch-notes/[version].md` and `production/releases/[version]/patch-notes.md`, with identical content. Do not write either until the two-file changeset is authorized. Attempt the two writes as one bounded save operation and verify both contents. If either write fails or differs, report the exact path and output **BLOCKED**; one successful copy is not completion.

---

## Phase 7: Next Steps

Verdict: **COMPLETE** only after both copies are saved and verified identical. Otherwise the verdict is **BLOCKED**.

- Run `$release-checklist` to verify all other release gates are met before publishing.
- If the in-workflow community-manager tone review was unavailable, note that a manual review may still be useful before publishing; do not imply another workflow write or bypass user authorization.
