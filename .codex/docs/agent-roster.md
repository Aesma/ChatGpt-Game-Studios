# Agent Roster

The following agents are available. Each has a dedicated definition file in
`.codex/agents/`. Use the agent best suited to the task at hand. When a task
spans multiple domains, the coordinating agent (usually `producer` or the
domain lead) should delegate to specialists.

## Tier 1 -- Leadership Agents (high-complexity)
| Agent | Domain | When to Use |
|-------|--------|-------------|
| `creative-director` | High-level vision | Major creative decisions, pillar conflicts, tone/direction |
| `technical-director` | Technical vision | Architecture decisions, tech stack choices, performance strategy |
| `producer` | Production management | Sprint planning, milestone tracking, risk management, coordination |

## Tier 2 -- Department Lead Agents (standard-complexity)
| Agent | Domain | When to Use |
|-------|--------|-------------|
| `game-designer` | Game design | Mechanics, systems, progression, economy, balancing |
| `lead-programmer` | Code architecture | System design, code review, API design, refactoring |
| `art-director` | Visual direction | Style guides, art bible, asset standards, UI/UX direction |
| `audio-director` | Audio direction | Music direction, sound palette, audio implementation strategy |
| `narrative-director` | Story and writing | Story arcs, world-building, character design, dialogue strategy |
| `qa-lead` | Quality assurance | Test strategy, bug triage, release readiness, regression planning |
| `release-manager` | Release pipeline | Build management, versioning, changelogs, deployment, rollbacks |
| `localization-lead` | Internationalization | String externalization, translation pipeline, locale testing |

## Tier 3 -- Specialist Agents (standard-complexity or low-complexity)
| Agent | Domain | Model | When to Use |
|-------|--------|-------|-------------|
| `systems-designer` | Systems design | standard-complexity | Specific mechanic implementation, formula design, loops |
| `level-designer` | Level design | standard-complexity | Level layouts, pacing, encounter design, flow |
| `economy-designer` | Economy/balance | standard-complexity | Resource economies, loot tables, progression curves |
| `gameplay-programmer` | Gameplay code | standard-complexity | Feature implementation, gameplay systems code |
| `engine-programmer` | Engine systems | standard-complexity | Core engine, rendering, physics, memory management |
| `ai-programmer` | AI systems | standard-complexity | Behavior trees, pathfinding, NPC logic, state machines |
| `network-programmer` | Networking | standard-complexity | Netcode, replication, lag compensation, matchmaking |
| `tools-programmer` | Dev tools | standard-complexity | Editor extensions, pipeline tools, debug utilities |
| `ui-programmer` | UI implementation | standard-complexity | UI framework, screens, widgets, data binding |
| `technical-artist` | Tech art | standard-complexity | Shaders, VFX, optimization, art pipeline tools |
| `sound-designer` | Sound design | standard-complexity | SFX design docs, audio event lists, mixing notes |
| `writer` | Dialogue/lore | standard-complexity | Dialogue writing, lore entries, item descriptions |
| `world-builder` | World/lore design | standard-complexity | World rules, faction design, history, geography |
| `qa-tester` | Test execution | low-complexity | Writing test cases, bug reports, test checklists |
| `performance-analyst` | Performance | standard-complexity | Profiling, optimization recs, memory analysis |
| `devops-engineer` | Build/deploy | low-complexity | CI/CD, build scripts, version control workflow |
| `analytics-engineer` | Telemetry | standard-complexity | Event tracking, dashboards, A/B test design |
| `ux-designer` | UX flows | standard-complexity | User flows, wireframes, accessibility, input handling |
| `prototyper` | Rapid prototyping | standard-complexity | Throwaway prototypes, mechanic testing, feasibility validation |
| `security-engineer` | Security | standard-complexity | Anti-cheat, exploit prevention, save encryption, network security |
| `accessibility-specialist` | Accessibility | low-complexity | WCAG compliance, colorblind modes, remapping, text scaling |
| `live-ops-designer` | Live operations | standard-complexity | Seasons, events, battle passes, retention, live economy |
| `community-manager` | Community | low-complexity | Patch notes, player feedback, crisis comms, community health |

## Engine-Specific Agents (use the set matching your engine)

### Engine Leads

| Agent | Engine | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unreal-specialist` | Unreal Engine 5 | standard-complexity | Blueprint vs C++, GAS overview, UE subsystems, Unreal optimization |
| `unity-specialist` | Unity | standard-complexity | MonoBehaviour vs DOTS, Addressables, URP/HDRP, Unity optimization |
| `godot-specialist` | Godot 4 | standard-complexity | GDScript patterns, node/scene architecture, signals, Godot optimization |

### Unreal Engine Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `ue-gas-specialist` | Gameplay Ability System | standard-complexity | Abilities, gameplay effects, attribute sets, tags, prediction |
| `ue-blueprint-specialist` | Blueprint Architecture | standard-complexity | BP/C++ boundary, graph standards, naming, BP optimization |
| `ue-replication-specialist` | Networking/Replication | standard-complexity | Property replication, RPCs, prediction, relevancy, bandwidth |
| `ue-umg-specialist` | UMG/CommonUI | standard-complexity | Widget hierarchy, data binding, CommonUI input, UI performance |

### Unity Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unity-dots-specialist` | DOTS/ECS | standard-complexity | Entity Component System, Jobs, Burst compiler, hybrid renderer |
| `unity-shader-specialist` | Shaders/VFX | standard-complexity | Shader Graph, VFX Graph, URP/HDRP customization, post-processing |
| `unity-addressables-specialist` | Asset Management | standard-complexity | Addressable groups, async loading, memory, content delivery |
| `unity-ui-specialist` | UI Toolkit/UGUI | standard-complexity | UI Toolkit, UXML/USS, UGUI Canvas, data binding, cross-platform input |

### Godot Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `godot-gdscript-specialist` | GDScript | standard-complexity | Static typing, design patterns, signals, coroutines, GDScript performance |
| `godot-csharp-specialist` | C# / .NET | standard-complexity | .NET patterns, [Signal] delegates, async, nullable types, type-safe node access |
| `godot-shader-specialist` | Shaders/Rendering | standard-complexity | Godot shading language, visual shaders, particles, post-processing |
| `godot-gdextension-specialist` | GDExtension | standard-complexity | C++/Rust bindings, native performance, custom nodes, build systems |
