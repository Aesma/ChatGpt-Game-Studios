<p align="center">
  <h1 align="center">ChatGPT Game Studios</h1>
  <p align="center">
    Turn a single Codex task into a full game development studio.
    <br />
    49 Codex subagents. 74 skills. One coordinated game-development studio.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href=".codex/agents"><img src="https://img.shields.io/badge/subagents-49-blueviolet" alt="49 Codex Subagents"></a>
  <a href=".agents/skills"><img src="https://img.shields.io/badge/skills-74-green" alt="74 Skills"></a>
  <a href=".codex/hooks.json"><img src="https://img.shields.io/badge/hook%20handlers-12-orange" alt="12 Registered Hook Handlers"></a>
  <a href=".codex/docs/rules-reference.md"><img src="https://img.shields.io/badge/scoped%20rules-11-red" alt="11 Path-Scoped Rule Sets"></a>
  <a href="https://learn.chatgpt.com/docs/codex"><img src="https://img.shields.io/badge/built%20for-Codex-111111?logo=openai" alt="Built for Codex"></a>
</p>

---

## Why This Exists

Building a game solo with AI is powerful — but a single chat session has no structure. No one stops you from hardcoding magic numbers, skipping design docs, or writing spaghetti code. There's no QA pass, no design review, no one asking "does this actually fit the game's vision?"

**ChatGPT Game Studios** solves this by giving your AI session the structure of a real studio. Instead of one general-purpose assistant, you get 49 specialized agents organized into a studio hierarchy — directors who guard the vision, department leads who own their domains, and specialists who do the hands-on work. Each agent has defined responsibilities, escalation paths, and quality gates.

The result: you still make every decision, but now you have a team that asks the right questions, catches mistakes early, and keeps your project organized from first brainstorm to launch.

---

## Table of Contents

- [What's Included](#whats-included)
- [Studio Hierarchy](#studio-hierarchy)
- [Skills](#skills)
- [Getting Started](#getting-started)
- [Upgrading](#upgrading)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Design Philosophy](#design-philosophy)
- [Customization](#customization)
- [Platform Support](#platform-support)
- [Community](#community)
- [License](#license)

---

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Codex subagents** | 49 | Specialized roles across design, programming, art, audio, narrative, QA, and production |
| **Skills** | 74 | `$skill` workflows for every production phase, including `$studio-status` and `$vertical-slice` |
| **Hook handlers** | 12 | 11 source mappings plus one supplemental command-safety handler across 8 events; `hook-lib.sh` is an unregistered helper |
| **Rules** | 11 | Path-scoped coding standards enforced when editing gameplay, engine, AI, UI, network code, and more |
| **Templates** | 40 | Recursively discovered templates for GDDs, UX specs, ADRs, sprint plans, HUD design, accessibility, and more |

## Studio Hierarchy

Subagents are organized into three responsibility tiers, matching how real
studios operate. These tiers describe ownership and escalation, not model
selection. This repository ships no per-role model or reasoning override; all
49 roles inherit the parent Codex session.

```
Tier 1 — Directors
  creative-director    technical-director    producer

Tier 2 — Department Leads
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

Tier 3 — Specialists
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

### Engine Specialists

The template includes agent sets for all three major engines. Use the set that matches your project:

| Engine | Lead Agent | Sub-Specialists |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript, Shaders, GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS, Shaders/VFX, Addressables, UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS, Blueprints, Replication, UMG/CommonUI |

## Skills

Invoke any of the 74 skills with `$skill-name` in Codex:

**Onboarding & Navigation**
`$start` `$help` `$project-stage-detect` `$studio-status` `$setup-engine` `$adopt`

**Game Design**
`$brainstorm` `$map-systems` `$design-system` `$quick-design` `$review-all-gdds` `$propagate-design-change` `$vertical-slice`

**Art & Assets**
`$art-bible` `$asset-spec` `$asset-audit`

**UX & Interface Design**
`$ux-design` `$ux-review`

**Architecture**
`$create-architecture` `$architecture-decision` `$architecture-review` `$create-control-manifest`

**Stories & Sprints**
`$create-epics` `$create-stories` `$dev-story` `$sprint-plan` `$sprint-status` `$story-readiness` `$story-done` `$estimate`

**Reviews & Analysis**
`$design-review` `$code-review` `$balance-check` `$content-audit` `$scope-check` `$perf-profile` `$tech-debt` `$gate-check` `$consistency-check` `$security-audit`

**QA & Testing**
`$qa-plan` `$smoke-check` `$soak-test` `$regression-suite` `$test-setup` `$test-helpers` `$test-evidence-review` `$test-flakiness` `$skill-test` `$skill-improve`

**Production**
`$milestone-review` `$retrospective` `$bug-report` `$bug-triage` `$reverse-document` `$playtest-report`

**Release**
`$release-checklist` `$launch-checklist` `$changelog` `$patch-notes` `$hotfix` `$day-one-patch`

**Creative & Content**
`$prototype` `$onboard` `$localize`

**Team Orchestration** (coordinate multiple agents on a single feature)
`$team-combat` `$team-narrative` `$team-ui` `$team-release` `$team-polish` `$team-audio` `$team-level` `$team-live-ops` `$team-qa`

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- [Codex](https://learn.chatgpt.com/docs/codex) (`npm install -g @openai/codex` for the CLI)
- **Recommended**: [jq](https://jqlang.github.io/jq/) (for hook validation) and Python 3 (for JSON validation)

All hooks fail gracefully if optional tools are missing — nothing breaks, you just lose validation.

### Setup

1. **Clone or use as template**:
   ```bash
   git clone https://github.com/Aesma/ChatGpt-Game-Studios.git my-game
   cd my-game
   ```

2. **Open the repository in Codex** using the desktop app, IDE extension, or CLI:
   ```bash
   codex
   ```

3. **Trust and review project hooks** — after marking the repository trusted,
   run `/hooks`, inspect the commands loaded from `.codex/hooks.json`, and trust
   the current hook hash only when it matches the checked-in configuration.

4. **Invoke `$start`** — the system asks where you are (no idea, vague concept,
   clear design, existing work) and guides you to the right workflow. No assumptions.

   Or jump directly to a specific skill if you already know what you need:
   - `$brainstorm` — explore game ideas from scratch
   - `$setup-engine godot 4.6` — configure your engine if you already know
   - `$project-stage-detect` — analyze an existing project

## Upgrading

Already using an older version of this template? See [UPGRADING.md](UPGRADING.md)
for step-by-step migration instructions, a breakdown of what changed between
versions, and which files are safe to overwrite vs. which need a manual merge.

## Project Structure

```
AGENTS.md                           # Master configuration
.agents/
  skills/                           # 74 reusable SKILL.md workflows
.codex/
  config.toml                       # Runtime defaults, permissions, and agent limits
  hooks.json                        # 12 handlers across 8 lifecycle/validation events
  agents/                           # 49 Codex subagent TOML definitions
  hooks/                            # 12 handler scripts plus hook-lib.sh
  rules/                            # Sandbox-external command policy (execpolicy)
  guidance/agent-memory/            # Repository-only role guidance and memory
  docs/
    workflow-catalog.yaml           # 7-phase pipeline definition (read by $help)
    templates/                      # 40 document templates
CGS Skill Testing Framework/        # Behavioral specs and recursive coverage catalog
src/                                # Game source code
assets/                             # Art, audio, VFX, shaders, data files
design/                             # GDDs, narrative docs, level designs
docs/                               # Technical documentation and ADRs
tests/                              # Test suites (unit, integration, performance, playtest)
tools/                              # Build and pipeline tools
prototypes/                         # Throwaway prototypes (isolated from src/)
production/                         # Sprint plans, milestones, release tracking
```

The 11 path-scoped rule sets are nested `AGENTS.md` files in the directories
they govern; see [rules-reference.md](.codex/docs/rules-reference.md).

## How It Works

### Agent Coordination

Agents follow a structured delegation model:

1. **Vertical delegation** — directors delegate to leads, leads delegate to specialists
2. **Horizontal consultation** — same-tier agents can consult each other but can't make binding cross-domain decisions
3. **Conflict resolution** — disagreements escalate up to the shared parent (`creative-director` for design, `technical-director` for technical)
4. **Change propagation** — cross-department changes are coordinated by `producer`
5. **Domain boundaries** — agents don't modify files outside their domain without explicit delegation

### Collaborative, Not Autonomous

This is **not** an auto-pilot system. Open-ended product decisions use a
collaborative protocol:

1. **Ask** — agents ask questions before proposing solutions
2. **Present options** — agents show 2-4 options with pros/cons
3. **You decide** — the user always makes the call
4. **Draft** — subagents show the proposed direction or changeset
5. **Approve scope** — one bounded authorization covers all in-scope edits

Codex does not re-prompt for every file or edit in an explicitly authorized
bounded task. It asks again only when work materially expands scope or reaches a
separately gated destructive or external action. You stay in control while the
subagents provide structure and expertise.

### Automated Safety

For a trusted repository, `.codex/hooks.json` registers these project hooks:

| Hook | Trigger | What It Does |
|------|---------|--------------|
| `validate-command-safety.sh` | `PreToolUse` | Quote-aware inspection of every Bash command against the project deny policy |
| `validate-commit.sh` | `PreToolUse` | Applies staged design/JSON/hardcoding/TODO checks only to `git commit` |
| `validate-push.sh` | `PreToolUse` | Surfaces protected-branch push risk |
| `validate-assets.sh` | `PostToolUse` | Validates asset paths changed by `apply_patch`; feedback does not roll back the completed patch |
| `validate-skill-change.sh` | `PostToolUse` | Recommends `$skill-test` after `.agents/skills/` paths changed by `apply_patch` |
| `session-start.sh` | `SessionStart` | Loads branch, project stage, and recovery context |
| `detect-gaps.sh` | `SessionStart` | Detects fresh projects and missing documentation |
| `pre-compact.sh` | `PreCompact` | Saves recovery context before compaction |
| `post-compact.sh` | `PostCompact` | Restores the `active.md` recovery reminder |
| `log-agent.sh` | `SubagentStart` | Starts a subagent audit entry |
| `log-agent-stop.sh` | `SubagentStop` | Completes the audit entry |
| `session-stop.sh` | `Stop` | Records session and Git activity |

These are 11 source mappings plus one supplemental command-safety handler across
8 events. The source Notification hook is replaced by native `[tui]` desktop
notifications. `hook-lib.sh` is a shared helper and is not registered. See the
[hook reference](.codex/docs/hooks-reference.md) and
[official Codex hooks documentation](https://learn.chatgpt.com/docs/hooks).

Codex sandbox and approval behavior is configured through supported settings in
personal `~/.codex/config.toml` and trusted project `.codex/config.toml` layers.

### Path-Scoped Rules

Coding standards are automatically enforced based on file location:

| Path | Enforces |
|------|----------|
| `src/gameplay/**` | Data-driven values, delta time usage, no UI references |
| `src/core/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggability, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, security |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `design/gdd/**` | Required 8 sections, formula format, edge cases |
| `design/narrative/**` | Lore consistency, character voice, canon levels |
| `assets/data/**` | JSON validity, naming, schemas, and defaults |
| `assets/shaders/**` | Naming, performance budgets, variants, and portability |
| `tests/**` | Test naming, coverage requirements, fixture patterns |
| `prototypes/**` | Relaxed standards, README required, hypothesis documented |

## Design Philosophy

This template is grounded in professional game development practices:

- **MDA Framework** — Mechanics, Dynamics, Aesthetics analysis for game design
- **Self-Determination Theory** — Autonomy, Competence, Relatedness for player motivation
- **Flow State Design** — Challenge-skill balance for player engagement
- **Bartle Player Types** — Audience targeting and validation
- **Verification-Driven Development** — Tests first, then implementation

## Customization

This is a **template**, not a locked framework. Everything is meant to be customized:

- **Add/remove agents** — delete agent files you don't need, add new ones for your domains
- **Edit agent prompts** — tune agent behavior, add project-specific knowledge
- **Modify skills** — adjust workflows to match your team's process
- **Add rules** — create new path-scoped rules for your project's directory structure
- **Tune hooks** — adjust validation strictness, add new checks
- **Pick your engine** — use the Godot, Unity, or Unreal agent set (or none)
- **Set review intensity** — `full` (all director gates), `lean` (phase gates only), or `solo` (none). Set during `$start` or edit `production/review-mode.txt`. Override per-run with `--review solo` on any skill.

## Platform Support

Hook scripts use POSIX-compatible patterns (`grep -E`, not `grep -P`) and include
fallbacks for optional tools. Git Bash supplies `bash` on Windows; macOS and Linux
use their native shell environment. The hook registry also provides Windows command
forms. Cross-platform testing is ongoing; please report platform-specific breakage.

## Community

- **Repository** — [Aesma/ChatGpt-Game-Studios](https://github.com/Aesma/ChatGpt-Game-Studios)
- **Issues** — [Bug reports and feature requests](https://github.com/Aesma/ChatGpt-Game-Studios/issues)

*Built for Codex. Contributions are welcome through the repository's available
GitHub collaboration features.*

## License

MIT License. See [LICENSE](LICENSE) for terms and [NOTICE.md](NOTICE.md) for
upstream authorship and adaptation provenance.
