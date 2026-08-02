---
name: team-release
description: "Orchestrate the release team: coordinates release-manager, qa-lead, devops-engineer, and producer to execute a release from candidate to deployment."
---

## Invocation and execution

Invoke this workflow as `$team-release`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[version number or 'next'] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.

**Argument check:** If no version number is provided:
1. Read `production/session-state/active.md` and the most recent file in `production/milestones/` (if they exist) to infer the target version.
2. If a version is found: report "No version argument provided — inferred [version] from milestone data. Proceeding." Then confirm by asking the user directly: "Releasing [version]. Is this correct?"
3. If no version is discoverable: ask the user directly to ask "What version number should be released? (e.g., v1.0.0)" and wait for user input before proceeding. Do NOT default to a hardcoded version string.

When this skill is invoked, orchestrate the release team through a structured pipeline.

**Decision Points:** At each phase transition, ask the user directly to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Phase 0: Resolve Review Mode

1. If `--review [mode]` was passed as an argument, use that mode.
2. Else read `production/review-mode.txt` — use whatever is written there.
3. Else default to `lean`.

Modes:
- `full` — spawn all director and lead gates as described
- `lean` — skip director gates unless they are PHASE-GATE type (CD-PHASE-GATE, TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE)
- `solo` — skip all director gate spawning entirely; run the skill without any agent gates

Store the resolved mode for use in all subsequent phases.

## Team Composition
- **release-manager** — Release branch, versioning, changelog, deployment
- **qa-lead** — Test sign-off, regression suite, release quality gate
- **devops-engineer** — Build pipeline, artifacts, deployment automation
- **security-engineer** — Pre-release security audit (invoke if game has online/multiplayer features or player data)
- **analytics-engineer** — Verify telemetry events fire correctly and dashboards are live
- **community-manager** — Patch notes, launch announcement, player-facing messaging
- **producer** — Go/no-go decision, stakeholder communication, scheduling

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: release-manager` — Release branch, versioning, changelog, deployment
- `subagent_type: qa-lead` — Test sign-off, regression suite, release quality gate
- `subagent_type: devops-engineer` — Build pipeline, artifacts, deployment automation
- `subagent_type: security-engineer` — Security audit for online/multiplayer/data features
- `subagent_type: analytics-engineer` — Telemetry event verification and dashboard readiness
- `subagent_type: community-manager` — Patch notes and launch communication
- `subagent_type: producer` — Go/no-go decision, stakeholder communication
- `subagent_type: network-programmer` — Netcode stability sign-off (invoke if game has multiplayer)

Always provide full context in each agent's prompt (version number, milestone status, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Release Planning
Delegate to **producer**:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Set the target release date and communicate to team
- Output: release authorization with scope confirmation

### Phase 2: Release Candidate
Delegate to **release-manager**:
- Present the exact release branch and version-file changes at the existing Phase 2 decision point; obtain explicit authorization for branch creation and version changes. File changeset approval alone does not authorize Git operations.
- Cut release branch from the agreed commit
- Bump version numbers in all relevant files
- Generate the release checklist using `$release-checklist`
- Freeze the branch — no feature changes, bug fixes only
- Output: release branch name and checklist

### Phase 3: Quality Gate (parallel)
Delegate in parallel:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no S1/S2 bugs. Sign off on quality.
- **devops-engineer**: Build release artifacts for all target platforms. Verify builds are clean and reproducible. Run automated tests in CI.
- **security-engineer** *(if game has online features, multiplayer, or player data)*: Conduct pre-release security audit. Review authentication, anti-cheat, data privacy compliance. Sign off on security posture.
- **network-programmer** *(if game has multiplayer)*: Sign off on netcode stability. Verify lag compensation, reconnect handling, and bandwidth usage under load.

### Phase 4: Localization, Performance, and Analytics
Delegate (can run in parallel with Phase 3 if resources available):
- Verify all strings are translated (delegate to **localization-lead** if available)
- Run performance benchmarks against targets (delegate to **performance-analyst** if available)
- **analytics-engineer**: Verify all telemetry events fire correctly on release build. Confirm dashboards are receiving data. Check that critical funnels (onboarding, progression, monetization if applicable) are instrumented.
- Output: localization, performance, and analytics sign-off

### Phase 5: Go/No-Go
Delegate to **producer**:
- Consume the two persisted checklist reports matching the Phase 1 version/date/scope. Prefer exact paths returned by this run; otherwise accept only user-specified paths under `production/releases/release-checklist-[date].md` and `production/launch/launch-checklist-[date].md` whose bodies match the release scope. Never choose by modification time.
- Internal readiness passes only with `RELEASE READY`; `CONCERNS`, `RELEASE BLOCKED`, missing, malformed, or mismatched reports are NO-GO. External readiness passes only with a persisted `LAUNCH READY`; `CONCERNS`, `LAUNCH BLOCKED`, missing, malformed, mismatched, or dry-run-only output is NO-GO.
- Collect sign-off from qa-lead, release-manager, devops-engineer, security-engineer (if spawned), and network-programmer (if spawned). Use a technical-director result only when the internal release checklist explicitly cites an existing one; otherwise do not invent or require an undispatched sign-off.
- Evaluate any open issues — are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

**If producer declares NO-GO:**
- Surface the decision immediately: "PRODUCER: NO-GO — [rationale, e.g., S1 bug found in Phase 3]."
- Ask the user directly with options:
  - Fix the blocker and re-run the affected phase
  - Defer the release to a later date
  - Provide additional evidence and re-run the Phase 5 decision
- **Skip Phase 6 entirely** — do not tag, deploy to staging, deploy to production, or spawn community-manager.
- Produce a partial report summarizing Phases 1–5 and what was skipped (Phase 6) and why.
- Verdict: **BLOCKED** — release not deployed.

User rationale may supplement evidence, but it cannot change a checklist verdict or directly enter Phase 6. Re-run Phase 5 after the underlying persisted reports/sign-offs are corrected. Any checklist CONCERNS/BLOCKED result, build failure, missing required sign-off, S1/S2, security/privacy blocker, or multiplayer stability blocker deterministically remains NO-GO.

### Phase 6: Deployment (if GO)
Before any action, display the exact tag, staging target, and production target. Obtain explicit authorization separately for tag creation, staging deployment, and production deployment; the file changeset approval and Phase 2 branch/version authorization do not cover these operations.

Assign exclusive ownership and run sequentially:
- **release-manager** owns version/tag/changelog only and prepares the changelog plus tag plan; it does not deploy.
- **devops-engineer** owns build artifacts and deployments only. It deploys the handed-off artifact/version to staging and waits for an actual smoke result.
- Only an actual staging smoke PASS allows the release-manager to create the authorized tag and allows the devops-engineer to request/use explicit production authorization. FAIL or UNKNOWN returns BLOCKED and skips tag and production actions not yet performed.
- Exactly one devops-engineer deployment task may target production.
- Human team action: Monitor dashboards and error rates for 48 hours post-release. Schedule a follow-up retrospective using `$retrospective` at the 48-hour mark.

Delegate to **community-manager** in parallel only for drafts:
- Finalize patch notes using `$patch-notes [version]`
- Prepare launch announcement (store page updates, social media, community post)
- Draft known issues post if any S3+ issues shipped
- Output: unpublished player-facing release communication drafts. Do not publish during Phase 6.

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- **community-manager**: After production deployment is confirmed successful, publish player-facing communication only after a separate explicit `publish` instruction. Without it, leave drafts unpublished. A failed/BLOCKED deployment must not emit a success announcement.
- **analytics-engineer**: Confirm live dashboards are healthy; alert if any critical events are missing
- Schedule post-release retrospective if issues occurred

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (release checklists, changelogs, patch notes, deployment scripts) are
delegated to sub-agents and sub-skills. The orchestrator obtains one combined changeset authorization before delegation, and every delegate writes only inside that boundary without prompting again. This orchestrator does not write files directly.

This file authorization never authorizes branch creation, tagging, staging/production deployment, or external publishing; those use the explicit decisions in Phases 2, 6, and 7.

## Output

A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan.

Verdict: **COMPLETE** — release executed and deployed.
Verdict: **BLOCKED** — release halted; go/no-go was NO or a hard blocker is unresolved.

## Next Steps

- Monitor post-release dashboards for 48 hours.
- Run `$retrospective` if significant issues occurred during the release.
- Update `production/stage.txt` to `Live` after successful deployment.
