---
name: project-stage-detect
description: "Automatically analyze project state, detect stage, identify gaps, and recommend next steps based on existing artifacts. Use when user asks 'where are we in development', 'what stage are we in', 'full project audit'."
---

## Invocation and execution

Invoke this workflow as `$project-stage-detect`.

This workflow is read-only and advisory. It always returns the stage report in the conversation, never writes `production/stage.txt` or a project-stage report, and never asks for changeset authorization.

Arguments: `[optional: role filter like 'programmer' or 'designer']`. Treat bracketed values as optional unless the workflow says otherwise.


# Project Stage Detection

This skill scans your project to determine its current development stage, completeness
of artifacts, and gaps that need attention. It's especially useful when:
- Starting with an existing project
- Onboarding to a codebase
- Checking what's missing before a milestone
- Understanding "where are we?"

---

## Workflow

### 1. Scan Key Directories

Analyze project structure and content:

**Design Documentation** (`design/`):
- Count GDD files in `design/gdd/*.md`
- Check for game-concept.md, game-pillars.md, systems-index.md
- If systems-index.md exists, count total systems and designed systems only from explicit values in its existing `Status` column. Record unparseable rows as `unknown`; a GDD file's existence alone does not imply Approved
- Analyze completeness (Overview, Detailed Design, Edge Cases, etc.)
- Count narrative docs in `design/narrative/`
- Count level designs in `design/levels/`

**Source Code** (`src/`):
- Count only configured production-language source extensions, excluding generated, vendor, and test trees
- Identify major systems from production-source directories; file-count thresholds are weak supporting signals only and never determine a stage
- Check for core/, gameplay/, ai/, networking/, ui/ directories
- Estimate lines of code (rough scale)

**Production Artifacts** (`production/`):
- Check for active sprint plans
- Look for milestone definitions
- Find roadmap documents

**Prototypes** (`prototypes/`):
- Count prototype directories
- Read README/status content rather than treating file existence as documentation
- Report a prototype active/archived only from explicit content; without a marker, record `unknown`

**Architecture Docs** (`docs/architecture/`):
- Count ADRs (Architecture Decision Records)
- Check for overview/index documents

**Tests** (`tests/`):
- Count test files
- Read an existing coverage report when available; otherwise report test file counts and coverage as unknown

### 2. Classify Project Stage

Based on scanned artifacts, determine stage. Check `production/stage.txt` first. Accept only the seven exact stage values below, then still cross-check all artifact signals. For an invalid value, report it as unusable and infer without modifying the file. For a valid but materially contradictory value, report the conflict and limits in the existing rationale/summary text rather than silently treating it as proven. Otherwise auto-detect explicitly in **Release → Polish → Production → Pre-Production → Technical Setup → Systems Design → Concept** order. Stop at the first stage whose own indicators and all preceding-stage artifact signals are satisfied:

| Stage | Indicators |
|-------|-----------|
| **Concept** | No game concept doc, brainstorming phase |
| **Systems Design** | Game concept exists, systems index missing or incomplete |
| **Technical Setup** | Systems index exists, engine not configured |
| **Pre-Production** | Completed system-design evidence plus architecture or epic work has started, and the engine is configured |
| **Production** | Production implementation code aligns with an active sprint and epic, with preceding design/setup evidence present |
| **Polish** | Explicit only (set by `$gate-check` Production → Polish gate) |
| **Release** | Explicit only (set by `$gate-check` Polish → Release gate) |

`Engine configured` means Engine, Language, and Target Platform are all non-placeholder values and mutually consistent in existing configuration. Missing, placeholder, or contradictory values are not configured.

Engine configuration or a source-file count is only a supporting signal and can never advance a project by itself. When signals conflict, retain the lower stage that is fully evidenced and explain the missing prerequisite.

### 3. Collaborative Gap Identification

**DO NOT** just list missing files. Instead, **ask clarifying questions**:

- "I see combat code (`src/gameplay/combat/`) but no `design/gdd/combat-system.md`. Was this prototyped first, or should we reverse-document?"
- "You have 15 ADRs but no architecture overview. Should I create one to help new contributors?"
- "No sprint plans in `production/`. Are you tracking work elsewhere (Jira, Trello, etc.)?"
- "I found a game concept but no systems index. Have you decomposed the concept into individual systems yet, or should we run `$map-systems`?"
- "Prototypes directory has 3 projects with no READMEs. Were these experiments, or do they need documentation?"

### 4. Generate Stage Report

Use `.codex/docs/templates/project-stage-report.md` as the single structural authority. Do not reproduce or add a competing embedded template, confidence field, or PASS/CONCERNS/FAIL classification here. Put evidence limits and conflicting signals in the template's existing `Executive Summary` or `Stage Classification Rationale` prose, and use counts/present/missing/unknown unless an explicit denominator exists.

Before generating the final report, present the preliminary artifact findings and ask only the gap questions whose answers can materially change classification or recommendation. Wait for the answers; unanswered questions remain `unresolved` and are never assumed.

### 5. Role-Filtered Recommendations (Optional)

If the user provided a role argument, accept only `programmer`, `designer`, `producer`, or `general`. For any other value, ask for clarification or explicitly fall back to General and show the actual scope used; do not silently apply a guessed filter.

If user provided a valid role argument (e.g., `$project-stage-detect programmer`):

**Programmer**:
- Focus on architecture docs, test coverage, missing ADRs
- Code-to-docs gaps

**Designer**:
- Focus on GDD completeness, missing design sections
- Prototype documentation

**Producer**:
- Focus on sprint plans, milestone tracking, roadmap
- Cross-team coordination docs

**General** (no role):
- Holistic view of all gaps
- Highest-priority items across domains

### 6. Present the Read-Only Report

After resolving key gap questions, present the full stage analysis in the conversation. Unanswered questions remain explicitly unresolved. Do not offer or attempt to save `production/project-stage-report.md` or update `production/stage.txt`.

---

## Example Usage

```text
# General project analysis
$project-stage-detect

# Programmer-focused analysis
$project-stage-detect programmer

# Designer-focused analysis
$project-stage-detect designer
```

---

## Follow-Up Actions

After generating the report, suggest relevant next steps:

- **Concept exists but no systems index?** → `$map-systems` to decompose into systems
- **Missing design docs?** → `$reverse-document design src/[system]`
- **Missing architecture docs?** → `$architecture-decision` or `$reverse-document architecture`
- **Prototypes need documentation?** → `$reverse-document concept prototypes/[name]`
- **No sprint plan?** → `$sprint-plan`
- **Approaching milestone?** → `$milestone-review [milestone-name]` (or `current` only when existing state resolves it uniquely)

---

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **Question First**: Ask about gaps, don't assume
2. **Present Options**: "Should I create X, or is it tracked elsewhere?"
3. **User Decides**: Wait for direction
4. **Show Report**: Display the complete advisory report in the conversation

**Never** write files or request changeset authorization in this workflow.
