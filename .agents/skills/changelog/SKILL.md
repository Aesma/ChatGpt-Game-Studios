---
name: changelog
description: "Auto-generates a changelog from git commits, sprint data, and design documents. Produces both internal and player-facing versions."
---

## Invocation and execution

Invoke this workflow as `$changelog`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[version|sprint-number]`. Treat bracketed values as optional unless the workflow says otherwise.

Before starting, gather initial context read-only:

1. Run `git log --oneline -30`; if Git history is unavailable, continue with an empty history and say so.
2. Run `git tag --list --sort=-v:refname` and retain the first five results.


## Phase 1: Parse Arguments

Read the argument for the target version or sprint number. If a version is given, use the corresponding git tag. If a sprint number is given, use the sprint date range.

Verify the repository is initialized: run `git rev-parse --is-inside-work-tree` to confirm git is available. If not a git repo, inform the user and abort gracefully.

---

## Phase 2: Gather Change Data

Select the range that matches the requested target:

- For a specified release tag, use the previous release tag through that target
  tag (`[previous-tag]..[target-tag]`). Do not use `HEAD` for an older release.
- If the specified tag is the first release tag, use history ending at that tag.
- With no target version, use the latest release tag through `HEAD` for current
  unreleased changes.
- For sprint mode, use only that sprint's existing date range and closed stories.

If the requested target tag or sprint boundary cannot be found, stop rather than
substituting a different range.

```
git log --oneline [selected-start]..[selected-end]
```

If no tags exist, read the full log or a reasonable recent range (last 100 commits).

Read sprint reports from `production/sprints/` for the relevant period to understand planned work and context behind changes.

Read completed design documents from `design/gdd/` for any new features implemented during this period.

---

## Phase 3: Categorize Changes

Categorize every change into one of these categories:

- **New Features**: Entirely new gameplay systems, modes, or content
- **Improvements**: Enhancements to existing features, UX improvements, performance gains
- **Bug Fixes**: Corrections to broken behavior
- **Balance Changes**: Tuning of gameplay values, difficulty, economy
- **Known Issues**: Issues the team is aware of but have not yet resolved
- **Miscellaneous**: Changes that do not fit the above categories, or commits whose messages are too vague to classify confidently

For each commit, check whether the message contains a task ID or story reference
(e.g. `[STORY-123]`, `TR-`, `#NNN`, or similar). Count commits that lack any task reference
and include this count in the Phase 4 Metrics section as: `Commits without task reference: [N]`.

---

## Phase 4: Generate Internal Changelog

```markdown
# Internal Changelog: [Version]
Date: [Date]
Sprint(s): [Sprint numbers covered]
Commits: [Count]

## New Features
- [Feature Name] -- [Technical description, affected systems]
  - Design doc: [link if applicable]

## Improvements
- [Improvement] -- [What changed technically and why]

## Bug Fixes
- [BUG-ID] [Description of bug and root cause]
  - Fix: [What was changed]

## Balance Changes
- [What was tuned] -- [Old value -> New value] -- [Design intent]

## Technical Debt / Refactoring
- [What was cleaned up and why]

## Miscellaneous
- [Change that didn't fit other categories, or vague commit message]

## Known Issues
- [Issue description] -- [Severity] -- [ETA for fix if known]

## Metrics
- Total commits: [N]
- Commits without task reference: [N]
```

---

## Phase 5: Generate Player-Facing Changelog

```markdown
# What is New in [Version]

## New Features
- **[Feature Name]**: [Player-friendly description of what they can now do
  and why it is exciting. Focus on the experience, not the implementation.]

## Improvements
- **[What improved]**: [How this makes the game better for the player.
  Be specific but avoid jargon.]

## Bug Fixes
- Fixed an issue where [describe what the player experienced, not what was
  wrong in the code]
- Fixed [player-visible symptom]

## Balance Changes
- [What changed in player-understandable terms and the design intent.
  Example: "Healing potions now restore 50 HP (up from 30) -- we felt
  players needed more recovery options in late-game encounters."]

## Known Issues
- We are aware of [issue description in player terms] and are working on a
  fix. [Workaround if one exists.]

---
Thank you for playing! Your feedback helps us make the game better.
Report issues at [link].
```

---

## Phase 6: Output

Output both changelogs to the user. The internal changelog is the primary working document. The player-facing changelog is ready for community posting after review.

---

## Phase 7: Offer File Write

After presenting the changelogs, ask the user:

> "Should the proposed changeset include this changelog update in `docs/CHANGELOG.md`?
> [A] Yes, prepend this entry while preserving all existing history
> [B] No — I'll copy it manually"

- Check whether `docs/CHANGELOG.md` exists and read its current contents before
  asking so the preview proves that prior entries are preserved.
- If the user selects [A]: prepend the new internal changelog entry (newest first)
  while leaving every existing entry unchanged.
- If the user selects [B]: stop here without writing.

After a successful write: Verdict: **CHANGELOG WRITTEN** — changelog saved to `docs/CHANGELOG.md`.
If the user declines: Verdict: **COMPLETE** — changelog generated.

---

## Phase 7: Next Steps

- Use `$patch-notes [version]` to generate a styled, saved version for public release.
- Use `$release-checklist` before publishing the changelog externally.

### Guidelines

- Never expose internal code references, file paths, or developer names in the player-facing changelog
- Group related changes together rather than listing individual commits
- If a commit message is unclear, check the associated files and sprint data for context
- Balance changes should always include the design reasoning, not just the numbers
- Known issues should be honest — players appreciate transparency
- If the git history is messy (merge commits, reverts, fixup commits), clean up the narrative rather than listing every commit literally
