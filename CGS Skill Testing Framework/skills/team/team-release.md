# Skill Test Spec: $team-release

## Skill Summary

Orchestrates the release team through a 7-phase pipeline from release candidate to
deployment and post-release monitoring. Coordinates release-manager, qa-lead,
devops-engineer, producer, security-engineer (optional, required for online/
multiplayer), network-programmer (optional, required for multiplayer),
analytics-engineer, and community-manager. Phase 3 agents run in parallel. Ends
with a go/no-go decision; deployment (Phase 6) is skipped if the producer calls
NO-GO. Closes with a post-release monitoring plan.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] File approval does not authorize branch, tag, staging, production, or publish side effects
- [ ] Phase 5 consumes scope-matched persisted release/launch checklist paths; only RELEASE READY plus persisted LAUNCH READY can GO
- [ ] Dry-run launch output, CONCERNS, BLOCKED, missing, malformed, or mismatched checklist evidence is NO-GO
- [ ] A written rationale cannot override NO-GO; corrected evidence must be re-evaluated
- [ ] release-manager exclusively owns version/tag/changelog and devops-engineer exclusively owns build/deploy
- [ ] Staging smoke must actually PASS before tag/production; FAIL or UNKNOWN blocks remaining irreversible actions
- [ ] Community work before deploy is draft-only; publishing requires successful production plus an explicit publish instruction
4. Proceeds as if `$team-release v1.1.0` was the input

**Expected behavior (variant B):**
1. Phase 1: No argument provided; reads available state files — no version discoverable
2. Uses user-input request: "What version number should be released? (e.g., v1.0.0)"
3. Waits for user input before proceeding

**Assertions:**
- [ ] Skill does NOT default to a hardcoded version string when no argument is provided
- [ ] Skill reads `production/session-state/active.md` and milestone files before asking (variant A)
- [ ] Inferred version is confirmed with the user via user-input request before proceeding (variant A)
- [ ] When no version is discoverable, user-input request is used — skill does not guess (variant B)
- [ ] Skill does NOT error out when milestone files are absent — it falls back to asking (variant B)

---

## Protocol Compliance

- [ ] `user-input request` used at each phase transition gate (post-Phase 1, post-Phase 2, post-Phase 3/4 if issues, post-Phase 5 go/no-go)
- [ ] Phase 3 agents are always issued as parallel Codex subagent delegations — qa-lead and devops-engineer are never sequential
- [ ] security-engineer is conditionally spawned based on game features — never silently skipped when features are present
- [ ] File Write Protocol: orchestrator never calls file edits directly — all writes are delegated to sub-agents or sub-skills
- [ ] Phase 6 Deployment is strictly conditional on a GO verdict from Phase 5 — never auto-triggered
- [ ] Tag, staging target, and production target are displayed and explicitly authorized by action class
- [ ] Error recovery: any BLOCKED agent is surfaced immediately before continuing to dependent phases
- [ ] Partial reports are always produced if any phase fails or the pipeline is halted (Case 2)
- [ ] Verdict: COMPLETE only when deployment completes; BLOCKED when go/no-go is NO or a hard blocker is unresolved
- [ ] Next steps always include 48-hour post-release monitoring, `$retrospective` recommendation, and `production/stage.txt` update to `Live`

---

## Coverage Notes

### P1 Regression Matrix

- [ ] `next` and omitted versions use explicit milestone targets; multiple candidates require user selection and malformed versions fail.
- [ ] Phase 1 confirms scope, source commit text, target platforms, version, and date before branch creation.
- [ ] No unused review mode can skip a production or sign-off role.
- [ ] Localization/performance applicability follows confirmed scope and budgets; applicable missing evidence is BLOCKED.
- [ ] No-telemetry scope is N/A; scoped but inaccessible telemetry is UNKNOWN/BLOCKED, never healthy by assumption.
- [ ] Required QA/devops/security/network/checklist work cannot use Skip to reach GO.
- [ ] COMPLETE covers deployed release and immediate actions only; the 48-hour human monitor remains a pending work item.

- Phase 7 post-release actions (release report, milestone tracking, community publishing, dashboard monitoring) are validated implicitly by Case 1. No separate edge case is required as Phase 7 is non-gated and does not have a blocking failure mode.
- The "devops-engineer build fails" path is not separately tested — it would surface as a BLOCKED result in Phase 3 and follow the standard error recovery protocol (surface → assess → user-input request options). This is validated structurally by the Static Assertions error recovery check.
- The parallel Phase 4 path (localization + performance + analytics simultaneously with Phase 3) is a documented option in the skill ("can run in parallel with Phase 3 if resources available"). Case 4 tests Phase 4 as a sequential gate; the parallel variant is left to the skill's implementation judgment.
- The `network-programmer` sign-off path for multiplayer is validated as part of Case 3 rather than a separate case, as it follows the same parallel-spawn pattern as security-engineer.
- NO-GO has no rationale-only escape hatch. Additional text can supply evidence, but Phase 5 must be re-run and all hard blockers remain deterministic NO-GO.

## P0 Behavioral Cases

- Checklist gate: a matching `RELEASE READY` file plus a persisted matching `LAUNCH READY` file and all required sign-offs may GO; every other checklist state, including launch dry-run chat output, is NO-GO.
- Staging failure: after authorized staging deploy, FAIL/UNKNOWN smoke produces BLOCKED; production and any not-yet-created tag are skipped.
- External authorization: approving release files does not create a branch/tag, deploy, or publish; each existing phase decision is required.
- Ownership: release-manager never deploys and devops-engineer never tags; one devops task owns production.
- Messaging: community-manager may draft during deployment, but cannot publish before successful production and an explicit `publish` instruction.
