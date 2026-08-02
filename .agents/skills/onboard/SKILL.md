---
name: onboard
description: "Generates a contextual onboarding document for a new contributor or agent joining the project. Summarizes project state, architecture, conventions, and current priorities relevant to the specified role or area."
---

## Invocation and execution

Invoke this workflow as `$onboard`.

This workflow is read-only. It produces the onboarding document in the conversation, never writes a file, and never requests changeset authorization.

Arguments: `[role|area]`. Treat bracketed values as optional unless the workflow says otherwise.

With no argument, use **General** scope. With one argument, first match it to an
existing `.codex/agents/` role or an existing top-level project area. If it
matches neither, ask the user what they meant and stop; do not guess a role,
agent file, or directory.


## Phase 1: Load Project Context

Read root `AGENTS.md` for project overview and standards. If it is missing, stop: explain that project rules cannot be summarized safely, recommend `$start`, and do not output **ONBOARDING COMPLETE**.

Read `docs/technical-preferences.md`, `production/stage.txt` when present, the uniquely referenced active sprint (from existing session/stage/sprint state), and the relevant architecture overview. If no unique active sprint exists, report it as unknown rather than choosing the most recently modified file.

Read the relevant agent definition from `.codex/agents/` if a specific role is specified.
Use that definition's stated responsibilities and file ownership to select
relevant existing directories for any discipline, including art and audio. If
the definition supplies no reliable mapping, use General scope rather than
inventing a reporting line or directory.

---

## Phase 2: Scan Relevant Area

- For programmers: scan `src/` for architecture, patterns, key files
- For designers: scan `design/` for existing design documents
- For narrative: scan `design/narrative/` for world-building and story docs
- For QA: scan `tests/` for existing test coverage
- For production: scan `production/` for current sprint and milestone
- For any other matched role: scan only existing directories named by its agent
  responsibilities or file ownership; if none are named, retain General scope

For every target listed in `Key Files`, read the applicable `AGENTS.md` chain
from the repository root down to that file's directory. Cite the contributing
rule file paths in `Current Standards and Conventions`; root rules alone are not
enough when a nearer override applies.

Read recent changes (git log if available) to understand current momentum. In a
non-Git workspace, a repository with no commits, or when the command fails,
write `Recent activity unavailable` and continue from file state. Never invent
momentum.

---

## Phase 3: Generate Onboarding Document

```markdown
# Onboarding: [Role/Area]

## Project Summary
[2-3 sentence summary of what this game is and its current state]

## Your Role
[What this role does on this project and key responsibilities. State who this
role reports to only when an agent definition or project document explicitly
configures it; otherwise write `Reporting line: not configured`. ]

## Project Architecture
[Relevant architectural overview for this role]

### Key Directories
| Directory | Contents | Your Interaction |
|-----------|----------|-----------------|

### Key Files
| File | Purpose | Read Priority |
|------|---------|--------------|

## Current Standards and Conventions
[Summary of conventions relevant to this role from AGENTS.md and agent definition]

## Current State of Your Area
[What has been built, what is in progress, what is planned next]

## Current Sprint Context
[What the team is working on now and what is expected of this role]

## Key Dependencies
[What other roles/systems this role interacts with most]

## Common Pitfalls
[Things that trip up new contributors in this area]

## First Tasks
[Suggested first tasks to get oriented and productive. Recommend implementation
work only when it already exists in the active sprint, an open issue, or a
clearly evidenced project gap. With no such source, recommend reading and asking
the listed questions instead of creating new backlog work.]

1. [Read these documents first]
2. [Review this code/content]
3. [Start with this small task]

## Questions to Ask
[Questions the new contributor should ask to get fully oriented]
```

---

## Phase 4: Present Document

Present the complete onboarding document directly in the conversation. Do not create, update, or offer to save any file.

---

## Phase 5: Next Steps

Verdict: **ONBOARDING COMPLETE** — onboarding document generated from the sources above. This success verdict is only for a completed orientation; missing root AGENTS.md stops without it.

- Share the onboarding doc with the new contributor before their first session.
- Run `$sprint-status` to show the new contributor current progress.
- Run `$help` if the contributor needs guidance on what to work on next.
