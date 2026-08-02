---
name: code-review
description: "Performs an architectural and quality code review on a specified file or set of files. Checks for coding standard compliance, architectural pattern adherence, SOLID principles, testability, and performance concerns."
---

## Invocation and execution

Invoke this workflow as `$code-review`.

Arguments: `[one-or-more-source-paths] [optional-story-path]`. At least one target
is required. Accept only existing project-local text source files, or a bounded
project-local directory after confirming its recursive file set is manageable.
Reject empty/missing/external/binary/generated targets. A final Markdown path is
a story only when it is under the existing production epic/story hierarchy and
contains the expected story identity; otherwise treat it as invalid input.

Delegate substantive work to the `lead-programmer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


## Phase 1: Load Target Files

Read every target file in full. For each target, read every applicable
`AGENTS.md` from the repository root through the target's parent directory.
Apply the closest rule when instructions conflict, and list the actual standards
files used in the final report.

---

## Phase 2: Identify Engine Specialists

Read `docs/technical-preferences.md`, section `## Engine Specialists`. Note:

- The **Primary** specialist (used for architecture and broad engine concerns)
- The **Language/Code Specialist** (used when reviewing the project's primary language files)
- The **Shader Specialist** (used when reviewing shader files)
- The **UI Specialist** (used when reviewing UI code)

If the section reads `[TO BE CONFIGURED]`, no engine is pinned — skip engine specialist steps.

---

## Phase 3: ADR Compliance Check

**Argument:** `$code-review [file(s)]` may optionally include a story file path as the last argument (e.g., `$code-review src/combat/attack.gd production/epics/combat/story-001.md`). If a story path is provided, read it to extract the governing ADR reference.

Search for ADR references in, in priority order:
1. The story file (if provided as argument)
2. Header comments at the top of the implementation files
3. Commit messages referencing these files (`git log --oneline -- [file]`)

Recognize the repository's actual four-digit IDs and case-insensitive paths,
including `ADR-0001` and `docs/architecture/adr-0001-*.md`.

If no ADR references are found, determine whether the targets introduce or
implement a project system governed by the existing coding standards. For a new
system that requires an ADR, report a missing-required-ADR architecture concern.
For an ordinary local file without that evidence, state `No ADR reference found`
without inventing a violation.

For each referenced ADR, require the file to exist and be readable, then extract
Status, Decision, and Consequences. Distinguish Accepted, Proposed, Superseded,
missing, and unreadable references in ADR Compliance. Proposed/missing/unreadable
is an architecture concern whose verdict severity follows the actual project
rule and implementation risk; only contradiction of an Accepted decision is an
architectural violation.

Then classify any deviation:

- **ARCHITECTURAL VIOLATION** (BLOCKING): Uses a pattern explicitly rejected in the ADR
- **ADR DRIFT** (WARNING): Meaningfully diverges from the chosen approach without using a forbidden pattern
- **MINOR DEVIATION** (INFO): Small difference from ADR guidance that doesn't affect overall architecture

---

## Phase 4: Standards Compliance

Identify the system category (engine, gameplay, AI, networking, UI, tools).
Compliance findings may come only from the applicable AGENTS chain, coding
standards, technical preferences, or an Accepted ADR. Evaluate documented rules.
The following are review prompts, not automatic blockers unless an applicable
project source states them: complexity under 10, method length under 40, universal
interfaces, dependency injection, data-driven configuration, and SOLID. Cite the
source beside every required compliance finding; otherwise place it in Suggestions.

---

## Phase 5: Architecture and SOLID

**Architecture:**
- [ ] Correct dependency direction (engine <- gameplay, not reverse)
- [ ] No circular dependencies between modules
- [ ] Proper layer separation (UI does not own game state)
- [ ] Events/signals used for cross-system communication
- [ ] Consistent with formal rules and with observed patterns in the target's own
      module/direct dependencies. Keep observations separate from requirements;
      do not scan the entire repository or promote a small sample into a standard.

**SOLID:**
- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open/Closed: Extendable without modification
- [ ] Liskov Substitution: Subtypes substitutable for base types
- [ ] Interface Segregation: No fat interfaces
- [ ] Dependency Inversion: Depends on abstractions, not concretions

---

## Phase 6: Game-Specific Concerns

- [ ] Frame-rate independence (delta time usage)
- [ ] No allocations in hot paths (update loops)
- [ ] Proper null/empty state handling
- [ ] Thread safety where required
- [ ] Resource cleanup (no leaks)

---

## Phase 7: Specialist Reviews (Parallel)

Deduplicate applicable roles, rank them by target risk, and run them in bounded
parallel batches that respect current subagent capacity and leave space for the
primary task. If a role fails, times out, or is unavailable, list it and the reason;
do not fabricate its result or imply the review was complete.

### Engine Specialists

If an engine is configured, determine which specialist applies to each file and spawn in parallel:

- Primary language files (`.gd`, `.cs`, `.cpp`) → Language/Code Specialist
- Shader files (`.gdshader`, `.hlsl`, shader graph) → Shader Specialist
- UI screen/structured prompt code → UI Specialist
- Cross-cutting or unclear → Primary Specialist

Also spawn the **Primary Specialist** for any file touching engine architecture (scene structure, node hierarchy, lifecycle hooks).

### QA Testability Review

Only when a supplied story is valid and contains readable `## QA Test Cases` and
`## Acceptance Criteria`, spawn `qa-tester` through Codex subagent delegation in parallel with the engine specialists. Pass:
- The implementation files being reviewed
- The story's `## QA Test Cases` section (the pre-written test specs from qa-lead)
- The story's `## Acceptance Criteria`

Ask the qa-tester to evaluate:
- [ ] Are all test hooks and interfaces exposed (not hidden behind private/internal access)?
- [ ] Do the QA test cases from the story's `## QA Test Cases` section map to testable code paths?
- [ ] Are any acceptance criteria untestable as implemented (e.g., hardcoded values, no seam for injection)?
- [ ] Does the implementation introduce any new edge cases not covered by the existing QA test cases?
- [ ] Are there any observable side effects that should have a test but don't?

If no valid story or either required QA section is missing, skip qa-tester and
mark Testability `NOT EVALUATED — story QA context unavailable`; do not pass empty
context.

For Visual/Feel and UI stories: qa-tester reviews whether the manual verification steps in `## QA Test Cases` are achievable with the implementation as written — e.g., "is the state the manual checker needs to reach actually reachable?"

Collect all specialist findings before producing output.

---

## Phase 8: Output Review

```
## Code Review: [File/System Name]

### Engine Specialist Findings: [N/A — no engine configured / CLEAN / ISSUES FOUND]
[Findings from engine specialist(s), or "No engine configured." if skipped]

### Testability: [N/A — Visual/Feel or Config story / TESTABLE / GAPS / BLOCKING]
[qa-tester findings: test hooks, coverage gaps, untestable paths, new edge cases]
[If BLOCKING: implementation must expose [X] before tests in ## QA Test Cases can run]

### ADR Compliance: [NO ADR FOUND / ACCEPTED / PROPOSED / SUPERSEDED / MISSING / UNREADABLE / DRIFT / VIOLATION]
[List each ADR checked, status/result, and any deviations with evidence and severity]

### Standards Compliance: [X/6 passing]
[List failures with line references]

### Architecture: [CLEAN / MINOR ISSUES / VIOLATIONS FOUND]
[List specific architectural concerns]

### SOLID: [COMPLIANT / ISSUES FOUND]
[List specific violations]

### Game-Specific Concerns
[List game development specific issues]

### Positive Observations
[What is done well -- always include this section]

### Required Changes
[Must-fix items before approval — ARCHITECTURAL VIOLATIONs always appear here]

### Suggestions
[Nice-to-have improvements]

### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

Verdict mapping is deterministic:
- `CHANGES REQUIRED`: any blocker, ADR violation, or required acceptance
  criterion that the implementation makes untestable.
- `APPROVED WITH SUGGESTIONS`: no required change, but at least one advisory finding.
- `APPROVED`: no findings that require a change or suggestion.

This skill is read-only — no files are written.

---

## Phase 9: Next Steps

Ask the user directly:
- Prompt: "Code review complete — verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]. How would you like to proceed?"
- Options (adjust based on verdict):
  - If APPROVED:
    - `[A] Run $story-done to mark the story complete`
    - `[B] Stop here`
  - If CHANGES REQUIRED:
    - `[A] Fix the issues and re-run $code-review`
    - `[B] Stop here`
  - If APPROVED WITH SUGGESTIONS:
    - `[A] Review the suggestions`
    - `[B] Stop here`

If an ARCHITECTURAL VIOLATION is found:
- If the violation contradicts an **existing ADR**: fix the implementation to comply with `docs/architecture/[adr-file].md`. If the design has legitimately changed, run `$architecture-decision` to formally *revise* the existing ADR — do not create a competing one.
- If a required ADR is missing, call it a missing decision or architecture concern,
  not a violation of a document that does not exist. Run `$architecture-decision`
  only when the applicable project standard actually requires that decision.
