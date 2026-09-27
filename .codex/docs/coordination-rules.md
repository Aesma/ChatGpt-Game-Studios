# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Runtime Inheritance

Skills and role definitions do not pin a model or reasoning effort. All 49 roles
inherit the parent Codex session. Role instructions may describe the depth and
kind of work required, but must not encode provider model names, model tiers, or
per-role reasoning overrides.

## Codex Subagents

Codex subagents are the single supported delegation model for this repository.
Roles are auto-discovered from `.codex/agents/**/*.toml`; `.codex/config.toml`
sets global agent limits rather than registering individual roles. Skills may ask the current agent to delegate to a
named role; if that role is unavailable, the current agent follows the same role
responsibilities and reports the fallback.

Use parallel subagents when workstreams are independent and have non-overlapping
write ownership. Use sequential delegation when one result is an input to another.
Subagents inherit the parent task's effective sandbox and permission context.
See the [official subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Parallel Task Protocol

When an orchestration skill spawns multiple independent agents:

1. Start all independent Codex subagent delegations before waiting for a result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately — do not silently skip
4. Always produce a partial report if some agents complete and others block
