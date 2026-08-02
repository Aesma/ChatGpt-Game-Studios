---
name: team-live-ops
description: "Orchestrate the live-ops team for post-launch content planning: coordinates live-ops-designer, economy-designer, analytics-engineer, community-manager, writer, and narrative-director to design and plan a season, event, or live content update."
---

## Invocation and execution

Invoke this workflow as `$team-live-ops`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[season name or event description]`. Treat bracketed values as optional unless the workflow says otherwise.

**Argument check:** If no season name or event description is provided, output:
> "Usage: `$team-live-ops [season name or event description]` — Provide the name or description of the season or live event to plan."
Then stop immediately without spawning any subagents or reading any files.

When this skill is invoked with a valid argument, orchestrate the live-ops team through a structured planning pipeline.

**Decision Points:** Ask for user choice at three consequential points only:
Phase 1 season/event scope, Phase 3 economy/reward design, and Phase 7 final
consolidated plan. Other dependent phases continue within those accepted
choices without routine transition approvals.


## Team Composition
- **live-ops-designer** — Season structure, event cadence, retention mechanics, battle pass
- **economy-designer** — Live economy balance, store rotation, currency pricing, pity timers
- **analytics-engineer** — Success metrics, A/B test design, event tracking, dashboard specs
- **community-manager** — Player-facing announcements, event descriptions, seasonal messaging
- **narrative-director** — Seasonal narrative theme, story arc, world event framing
- **writer** — Event descriptions, reward item names, seasonal flavor text, announcement copy

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: live-ops-designer` — Season/event structure and retention mechanics
- `subagent_type: economy-designer` — Live economy balance and reward pricing
- `subagent_type: analytics-engineer` — Success metrics, A/B tests, event instrumentation
- `subagent_type: community-manager` — Player-facing communication and messaging
- `subagent_type: narrative-director` — Seasonal theme and narrative framing
- `subagent_type: writer` — All player-facing text: event descriptions, item names, copy

Always provide full context in each agent's prompt (game concept path, existing season docs, ethics policy path, current economy state). Launch independent agents in parallel where the pipeline allows it (Phases 3 and 4 can run simultaneously).

## Pipeline

Phases 1–6 are analysis-only. All six roles return drafts and plans in
conversation; none creates or edits output documents before the Phase 7 ethics
review and final approval.

### Phase 1: Season/Event Scoping
Delegate to **live-ops-designer**:
- Define the season or event: type (seasonal, limited-time event, challenge), duration, theme direction
- Outline the content list: what's new (modes, items, challenges, story beats)
- Define the retention hook: what brings players back daily/weekly during this season
- Identify resource budget: how much new content needs to be created vs. reused
- Output: season brief with scope, content list, and retention mechanic overview

Present material scope alternatives and obtain the Phase 1 scope decision before
continuing.

### Phase 2: Narrative Theme
Delegate to **narrative-director**:
- Read the season brief from Phase 1
- Design the seasonal narrative theme: how does this event connect to the game world?
- Define the central story hook players will discover during the event
- Identify which existing lore threads this season can advance
- Output: narrative framing document (theme, story hook, lore connections)

### Phase 3: Economy Design (parallel with Phase 2 if theme is clear)
Delegate to **economy-designer**:
- Read the season brief and existing economy rules from `design/live-ops/economy-rules.md`
- Design the reward track: free tier progression, premium tier value proposition
- Plan the in-season economy: seasonal currency, store rotation, pricing
- Define pity timer mechanics and bad-luck protection for any random elements
- Verify no pay-to-win items in premium track
- Output: economy design draft with reward tables, pricing, and currency flow

Present material reward/economy alternatives and obtain the Phase 3 product
decision before dependent content is finalized.

### Phase 4: Analytics and Success Metrics (parallel with Phase 3)
Delegate to **analytics-engineer**:
- Read the season brief
- Define success metrics: participation rate target, retention lift target, battle pass completion rate
- Design any A/B tests to run during the season (e.g., different reward cadences)
- Specify new telemetry events needed for this season's content
- Output: analytics plan with success criteria and instrumentation requirements

### Phase 5: Content Writing (parallel)
Delegate in parallel:
- **narrative-director** (if needed): Write any in-game narrative text (cutscene scripts, NPC dialogue, world event descriptions) for the season
- **writer**: Write all player-facing text — event names, reward item descriptions, challenge objective text, seasonal flavor text
- Both should read the narrative framing doc from Phase 2

### Phase 6: Player Communication Plan
Delegate to **community-manager**:
- Read the season brief, economy design, and narrative framing
- Draft the season launch announcement (tone, key highlights, platform-specific versions)
- Plan the communication cadence: pre-launch teaser, launch day post, mid-season reminder, final week FOMO push
- Draft known-issues section placeholder for day-1 patch notes
- Output: communication calendar with draft copy for each touchpoint

### Phase 7: Review and Sign-off
Collect outputs from all phases and present a consolidated season plan:
- Season brief (Phase 1)
- Narrative framing (Phase 2)
- Economy design and reward tables (Phase 3)
- Analytics plan and success metrics (Phase 4)
- Written content inventory (Phase 5)
- Communication calendar (Phase 6)

Present a summary to the user with:
- **Content scope**: what is being created
- **Economy health check**: does the reward track feel fair and non-predatory?
- **Analytics readiness**: are success criteria defined and instrumented?
- **Ethics review**: check the Phase 3 economy design against `design/live-ops/ethics-policy.md`
  - If the file does not exist: flag "ETHICS REVIEW SKIPPED: `design/live-ops/ethics-policy.md` not found. Economy design was not reviewed against an ethics policy. Recommend creating one before production begins." Include this flag in the season design output document. Add to next steps: create `design/live-ops/ethics-policy.md`.
  - If the file exists and a violation is found: flag "ETHICS FLAG: [element] in Phase 3 economy design violates [policy rule]. Approval is blocked until this is resolved." Do NOT issue a COMPLETE verdict or write output documents. Ask the user directly to revise economy design or cancel. If the user revises, re-spawn economy-designer and repeat Phase 7 ethics review. Cancel ends BLOCKED. An explicit policy violation cannot be overridden or waived.
- **Open questions**: decisions still needed before production begins

If a policy violation is found, offer only: revise the economy design and re-run
the same ethics check, or cancel with **BLOCKED**. There is no override/waiver
path for an explicit policy violation.

Resolve the exact paths defined below and show the proposed number/slug before
asking the user to approve the consolidated season plan. Issue COMPLETE only
after approval, one complete three-file changeset authorization, successful
writes, and no unresolved ethics violation. If a violation is unresolved, end
**BLOCKED** with zero output files.

## Output Documents

Before Phase 7 approval, resolve `[N]` and `[name]`. If the input explicitly
contains `Season N`, use N. Otherwise scan existing files under
`design/live-ops/seasons/`, take one greater than the highest valid season
number, and show that proposed number to the user. Normalize the name to a
filesystem-safe lowercase hyphenated slug. If any target path already exists,
stop and ask whether the user intends an explicit update; never overwrite it
silently.

All documents save to `design/live-ops/` with these exact resolved paths:
- `seasons/S[N]_[slug].md` — Season design document (from Phase 1-3)
- `seasons/S[N]_[slug]_analytics.md` — Analytics plan (from Phase 4)
- `seasons/S[N]_[slug]_comms.md` — Communication calendar (from Phase 6)

After ethics clearance and final plan approval, list these three paths and exact
intended contents in the one changeset. Then delegate non-overlapping ownership:
- `live-ops-designer` alone writes the season document
- `analytics-engineer` alone writes the analytics document
- `community-manager` alone writes the communications document

Each writer incorporates the other approved conversational outputs but edits
only its assigned path.

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

If a BLOCKED state is unresolvable, end with Verdict: **BLOCKED** instead of COMPLETE.

## File Write Protocol

Phases 1–6 perform no writes. Only after Phase 7 ethics clearance, the final
product decision, collision checks, and one complete three-file changeset
approval may writing agents be delegated. live-ops-designer, analytics-engineer,
and community-manager each own exactly one approved path as listed above. The
orchestrator does not write files directly.

## Output

A summary covering: season theme and scope, economy design highlights, success metrics, content list, communication plan, and any open decisions needing user input before production.

Verdict: **COMPLETE** — season plan produced and handed off for production.

## Next Steps

- Validate the season document against its own approved goals, cadence, economy, and content constraints; do not pass it to the system-GDD-only `$design-review`.
- Run `$sprint-plan` to schedule content creation work for the season.
- Run `$team-release` when the season content is ready to deploy.
