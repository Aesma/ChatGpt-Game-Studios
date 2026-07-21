---
name: onboard
description: "Produce a bounded, source-cited, role-aware onboarding summary in conversation without reading sensitive sources or modifying files."
---

## Invocation and execution

Invoke this workflow as $onboard.

Arguments: [role-id | area-id] [--visibility public|internal]. The role or area is optional. Visibility defaults to the least-privileged scope configured for onboarding; if no policy exists, use public.

This workflow is strictly read-only. It returns onboarding context only in conversation and must not create, edit, overwrite, delete, rename, stage, commit, publish, or save any file. It must not request changeset authorization, invent an output path, offer a save branch, invoke a director gate, delegate to a subagent, or invoke another project skill.

The --save option is unsupported. If persistence is requested, explain that it requires a separately scoped document task with an explicit path and collision policy, then stop without writing.

---

## Phase 1 — Resolve identity, visibility, and budget

1. Capture one snapshot_at value and repository identity before reading project context.
2. Normalize a supplied role or area against stable repository IDs:
   - A role must resolve exactly to one configured repository role definition.
   - An area must resolve exactly to one indexed project area.
   - Free-text aliases are accepted only when an authoritative alias map resolves them uniquely.
   - Missing optional input means GENERAL.
   - Ambiguous or nonexistent input returns ONBOARDING ERROR with candidate IDs; do not guess.
3. Keep repository roles separate from real organizational positions. Agent or role definitions describe repository workflow responsibilities, not a person's job title, manager, reporting line, employment status, access entitlement, or decision authority. Report those organizational facts as UNKNOWN unless an explicit, in-scope organizational mapping provides them.
4. Apply the configured onboarding visibility policy before opening any content. A requested visibility may narrow access but cannot expand the caller's authorized scope.
5. Use the configured onboarding context budget when present. Otherwise use:
   - at most 64 content files
   - at most 1 MiB total content
   - at most depth 6 below approved roots
   - at most 20 Git commits from one explicit configured range
6. Record budget limits, consumption, excluded roots, omitted sources, and reasons. Never silently exceed a budget.

The following are always denied and must not be opened, quoted, summarized, hashed into the output, or recommended as reading:

- environment files and local environment variants
- credentials, secrets, tokens, cookies, certificates, private keys, and vault exports
- personnel, payroll, salary, performance, disciplinary, applicant, or private-contact records
- private correspondence and user-private notes
- raw security vulnerability, exploit, anti-cheat bypass, incident-forensics, and embargoed reports
- any path denied by repository instructions or the active visibility policy

If a discovered filename or index entry appears sensitive, record only a generic redacted omission code. Do not expose its path, filename, existence details, secret-shaped value, or metadata.

---

## Phase 2 — Load bounded authoritative context

1. Read the repository-root AGENTS.md first. It is required. If it is missing, unreadable, invalid, or outside the allowed visibility scope, return ONBOARDING ERROR and no onboarding narrative.
2. Build a deterministic source plan from authoritative indexes and manifests before reading area content. Prefer:
   - project and technology configuration explicitly referenced by root AGENTS.md
   - architecture, design, test, production, and asset indexes
   - the active sprint pointer or current-work manifest
   - the exact role definition or area index selected in Phase 1
3. Do not recursively full-read src, design, tests, production, assets, Git history, or agent directories. Directory enumeration may identify candidates within the depth budget, but only indexed, role-relevant representative files enter the content budget.
4. For every candidate file that may be read or recommended, load the applicable instruction chain from repository root through its parent directory. Apply the closest nested AGENTS.md rule when rules conflict. Record the rule source and effective constraint.
5. Read only visibility-allowed, budgeted sources. For each source record:
   - stable path or artifact ID
   - content hash
   - snapshot status: READ, MISSING, UNREADABLE, INVALID, STALE, OMITTED_BUDGET, or OMITTED_POLICY
   - applicable instruction sources
   - claims supported
6. Use project facts only when a current readable source directly states them. Configuration placeholders are UNKNOWN, not configured values. A stage declaration is labeled DECLARED unless accompanied by the repository's current authoritative stage evidence. Planned work is not implemented work; an active sprint item is not completed work.
7. Read Git activity only when a repository source defines an explicit from_ref/to_ref or release/sprint window. Enforce the commit budget. Do not fall back to unbounded recent history or HEAD-relative guessing. Do not expose author names, emails, signatures, private ticket IDs, branch names, or raw commit messages. Summarize only source-supported technical themes after redaction.
8. If a selected source changes hash during the run, mark it STALE and do not combine its facts with the snapshot.

Core required coverage is root instructions plus the selected role/area identity. Project summary, technology, architecture, current stage, current work, testing, and recent activity are optional coverage dimensions. Missing or omitted optional dimensions remain explicitly UNKNOWN.

---

## Phase 3 — Build the cited onboarding summary

Build facts before prose. Each fact has:

    fact_id
    topic
    statement
    source_artifact
    source_locator
    source_hash
    snapshot_status
    visibility
    confidence: DIRECT or UNKNOWN

Only DIRECT facts may be stated as project facts. UNKNOWN fields remain labeled UNKNOWN; do not fill them with common game-development assumptions.

Return sections only when supported:

1. Scope and snapshot
2. Project overview
3. Repository role or area
4. Technology and architecture
5. Effective standards and conventions
6. Current declared stage and active work
7. Key directories and verified files
8. Dependencies and repository-owned interfaces
9. Common pitfalls explicitly documented by the project
10. Safe first orientation actions
11. Questions for the relevant owner
12. Sources, omitted coverage, and uncertainty

For every recommended file:

- verify that the file exists and is readable in the snapshot
- cite its path and hash
- report the applicable root-to-parent instruction chain
- do not recommend a policy-denied or visibility-excluded path

First orientation actions must be non-mutating and already authorized by repository guidance. Do not assign work, invent backlog tasks, claim a manager expects an action, or state that the contributor has access.

Tailor emphasis to the resolved repository role or area without hiding relevant constraints. A repository role can identify collaboration interfaces, but it cannot establish real team hierarchy or reporting relationships.

---

## Phase 4 — Determine status and return packet

Return schema onboarding_context/v2:

    schema_version: onboarding_context/v2
    status: ONBOARDING READY | ONBOARDING PARTIAL | ONBOARDING ERROR
    snapshot_at
    repository_identity
    resolved_scope
    visibility_scope
    context_budget
    budget_consumed
    coverage
    facts
    onboarding_summary
    recommended_files
    effective_instruction_chains
    omitted_sources
    redactions
    contradictions
    stale_sources
    next_action
    disclaimer

Use this fail-closed order:

1. ONBOARDING ERROR — root AGENTS.md is unavailable or invalid; role/area is ambiguous or invalid; repository identity cannot be established; or policy prevents required coverage.
2. ONBOARDING PARTIAL — required identity is valid, but any requested or relevant optional coverage dimension is missing, unreadable, stale, contradictory, policy-omitted, or budget-omitted.
3. ONBOARDING READY — required and relevant coverage is complete, every project fact is directly sourced, no source is stale or contradictory, no budget/policy omission affects the requested scope, and the summary contains no unresolved UNKNOWN that could mislead the contributor.

Never report a fixed ONBOARDING COMPLETE status. READY means the bounded snapshot is adequately sourced; it does not grant access, assign authority, or promise that the project has no undocumented practices.

Default and error paths remain strictly read-only and never request authorization.

---

## Phase 5 — Handoff and stop

Return at most one non-mutating next action supported by the observed repository guidance, such as reading one verified source or asking one identified artifact owner a question. Do not invoke the action or another skill.

If no safe, source-supported next action exists, say so. Do not suggest a project initialization, sprint, implementation, or design workflow merely because a file is absent.

Stop after returning the conversational packet. Never save an onboarding document.
