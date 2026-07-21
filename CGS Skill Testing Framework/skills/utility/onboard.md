# Skill Test Spec: $onboard

## Skill Summary

$onboard returns a bounded, source-cited onboarding summary in conversation. It is strictly read-only in every path and never asks for changeset authorization or invents a save location. It resolves repository roles separately from human organizational authority, applies visibility and sensitive-data exclusions before reading, follows applicable nested AGENTS.md instructions, and reports ONBOARDING READY, ONBOARDING PARTIAL, or ONBOARDING ERROR.

---

## Static Assertions (Structural)

Verified automatically by $skill-test static; no fixture is required.

- [ ] YAML frontmatter contains only name and a non-empty description; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains ONBOARDING READY, ONBOARDING PARTIAL, and ONBOARDING ERROR
- [ ] Explicitly forbids a fixed ONBOARDING COMPLETE status
- [ ] Declares every path strictly read-only and forbids authorization prompts, save branches, output-path invention, and file mutation
- [ ] Rejects --save and explains that persistence belongs to a separately scoped document task
- [ ] Requires root AGENTS.md and loads the root-to-parent instruction chain for each recommended file
- [ ] Applies the closest nested AGENTS.md rule on conflict
- [ ] Defines file, byte, depth, and Git-window budgets plus omitted-source reporting
- [ ] Applies visibility and sensitive-data exclusions before opening content
- [ ] Keeps repository role definitions separate from real job titles, managers, access, and decision authority
- [ ] Requires source path, locator, hash, snapshot status, and confidence for every fact
- [ ] Does not use unbounded Git history or expose author identity/private metadata
- [ ] Emits onboarding_context/v2 and has a non-mutating next-action handoff
- [ ] Invokes no director gate, subagent, or downstream project skill

---

## Director Gate Checks

None. Onboard is read-only and invokes no director gate, subagent, or downstream workflow.

---

## Test Cases

### Case 1: Configured project with complete bounded evidence

Fixture:

- Root AGENTS.md is readable and valid.
- An exact role ID resolves from the repository role index.
- Current technology, architecture, stage evidence, active-work pointer, and test index are readable within budget.
- All recommended files are visibility-allowed and unchanged during the run.

Input: $onboard gameplay-programmer --visibility internal

Expected behavior:

1. The role resolves exactly as a repository role.
2. Facts cite source path, locator, hash, and snapshot status.
3. Recommended files include their applicable instruction chains.
4. No relevant coverage gap exists.
5. Status is ONBOARDING READY.

Assertions:

- [ ] The output distinguishes repository responsibilities from human reporting authority
- [ ] Every project fact is DIRECT and traceable
- [ ] No file is written
- [ ] No authorization prompt or downstream workflow appears

---

### Case 2: P0 regression — default invocation is zero mutation

Fixture:

- A configured repository has all onboarding sources.
- No persistence option is supplied.

Input: $onboard

Expected behavior:

1. The general onboarding summary is returned in conversation.
2. No changeset preview or authorization question appears.
3. No directory or file is created.
4. Status is READY or PARTIAL according to coverage.

Assertions:

- [ ] Default behavior is strictly read-only
- [ ] The workflow does not offer to save the result
- [ ] No implicit onboarding filename or directory is invented

---

### Case 3: P0 regression — persistence request cannot trigger path guessing

Fixture:

- A user asks for persistence without providing a separately scoped document task.
- Files with plausible onboarding names already exist in several directories.

Input: $onboard artist --save

Expected behavior:

1. The unsupported option is identified.
2. The workflow explains the separate explicit-path and collision-policy requirement.
3. It stops without choosing, creating, patching, or overwriting any path.
4. No authorization prompt appears.

Assertions:

- [ ] --save never writes
- [ ] Existing files are not inspected to choose an overwrite target
- [ ] No default path or filename is generated
- [ ] Mutation count remains zero

---

### Case 4: Root AGENTS.md missing

Fixture:

- Repository root AGENTS.md is absent.
- Other configuration and sprint files exist.

Input: $onboard

Expected behavior:

1. Root instruction coverage fails.
2. No project onboarding narrative is generated from secondary sources.
3. Status is ONBOARDING ERROR.
4. A source-specific remediation question is returned without invoking a workflow.

Assertions:

- [ ] Missing root instructions never produce READY or a fixed completion verdict
- [ ] Secondary files do not substitute for repository authority
- [ ] The result remains read-only

---

### Case 5: Nested instruction conflict

Fixture:

- Root AGENTS.md recommends general files.
- design/AGENTS.md restricts design material to a narrower visibility and overrides one convention.
- The resolved area is design.

Input: $onboard design

Expected behavior:

1. The root-to-design instruction chain is loaded.
2. The closest applicable rule wins.
3. Restricted files are omitted before content is opened.
4. The effective rule source is cited.

Assertions:

- [ ] Root rules are not applied in isolation
- [ ] Nested precedence is deterministic
- [ ] Recommended files comply with their nearest instructions

---

### Case 6: Large repository exceeds bounded context

Fixture:

- src and design contain thousands of files.
- Relevant authoritative indexes fit within the default budget.
- Additional role-relevant files exceed either the 64-file or 1-MiB limit.

Input: $onboard programmer

Expected behavior:

1. Indexes and deterministic representative files are read within budget.
2. Recursive full-read does not occur.
3. Excess sources are OMITTED_BUDGET with counts and topics.
4. Status is ONBOARDING PARTIAL when omitted coverage affects the role.

Assertions:

- [ ] File, byte, and depth budgets are reported
- [ ] No silent truncation occurs
- [ ] Omitted content is not summarized or guessed

---

### Case 7: Sensitive sources are excluded before reading

Fixture:

- Index entries mention an environment file, credentials, personnel records, and a raw exploit report.
- Safe architecture and sprint sources are also present.

Input: $onboard

Expected behavior:

1. Sensitive entries are filtered before opening.
2. The output records generic policy omission codes only.
3. No sensitive path, filename, metadata, value, or exploit detail appears.
4. Safe facts remain available, with PARTIAL when the omission affects requested scope.

Assertions:

- [ ] Redaction is not deferred until after content ingestion
- [ ] Secrets and personal data never enter the prompt or output
- [ ] Denied artifacts are never recommended

---

### Case 8: Repository role is not an organizational chart

Fixture:

- A repository role definition describes review responsibilities.
- No explicit human-team or reporting-line mapping exists.

Input: $onboard qa-lead

Expected behavior:

1. Repository workflow responsibilities are summarized with citations.
2. Manager, reporting line, employment role, and access entitlement are UNKNOWN.
3. No person or real team hierarchy is invented.

Assertions:

- [ ] Agent descriptions do not establish human authority
- [ ] The summary does not say who the contributor reports to
- [ ] Missing organizational facts remain UNKNOWN

---

### Case 9: Git activity requires an explicit bounded window

Fixture:

- The repository has a large Git history with names, emails, ticket IDs, and private branch names.
- No configured onboarding from_ref/to_ref window exists.

Input: $onboard

Expected behavior:

1. Git history is not scanned as recent activity.
2. The activity dimension is UNKNOWN or omitted with reason.
3. No author identity, email, branch, ticket, or raw message is exposed.
4. Status is PARTIAL only if activity is relevant to requested scope.

Assertions:

- [ ] The workflow does not fall back to HEAD-relative history
- [ ] Git data has a maximum 20-commit budget when a window is configured
- [ ] Personal and private metadata is redacted

---

### Case 10: Ambiguous free-text role

Fixture:

- The alias artist maps to both technical-artist and art-director.
- No exact role ID was supplied.

Input: $onboard artist

Expected behavior:

1. Both candidate IDs are returned without reading role-specific area content.
2. No role is guessed.
3. Status is ONBOARDING ERROR.
4. No file is written.

Assertions:

- [ ] Role selection is deterministic
- [ ] Ambiguity cannot silently broaden visibility
- [ ] No human reporting relationship is inferred

---

### Case 11: Optional coverage is missing or stale

Fixture:

- Root instructions and role identity are valid.
- The active sprint pointer is missing.
- The architecture index changes hash during the run.

Input: $onboard engine-programmer

Expected behavior:

1. Current work is UNKNOWN.
2. Architecture is marked STALE and excluded from prose.
3. Known facts remain cited.
4. Status is ONBOARDING PARTIAL.

Assertions:

- [ ] Missing optional sources do not become invented facts
- [ ] Mixed snapshots are not presented as current
- [ ] PARTIAL lists the exact coverage dimensions affected

---

### Case 12: Placeholder configuration is unknown

Fixture:

- Technology configuration contains placeholders such as CHOOSE or TO BE CONFIGURED.
- Root instructions are valid.

Input: $onboard

Expected behavior:

1. Engine and language are reported UNKNOWN.
2. The skill does not choose an engine or infer one from source extensions.
3. Status is ONBOARDING PARTIAL when technology is relevant.

Assertions:

- [ ] Placeholders are not treated as configured values
- [ ] File extensions do not silently determine project policy
- [ ] The summary stays source-cited and read-only

---

### Case 13: Safe next action is non-mutating

Fixture:

- A valid snapshot identifies one verified, visibility-allowed architecture overview as the highest-priority orientation source.
- No project task assignment is authorized.

Input: $onboard network-programmer

Expected behavior:

1. The output recommends reading that one verified file.
2. Its path, hash, and nested instruction chain are cited.
3. No implementation, sprint, initialization, design, or other skill is invoked.

Assertions:

- [ ] The action is supported by repository guidance
- [ ] The action does not mutate project state
- [ ] The workflow does not assign work or claim manager expectations

---

## Protocol Compliance

- [ ] Default, error, partial, and ready paths are strictly read-only
- [ ] No save option, output-path inference, or changeset authorization exists
- [ ] Role/area and visibility are resolved before context loading
- [ ] Root and applicable nested AGENTS.md instructions govern every recommended path
- [ ] Context collection obeys explicit file, byte, depth, and Git budgets
- [ ] Sensitive material is denied before reading and omitted without identifying detail
- [ ] Every project fact has stable provenance and snapshot status
- [ ] READY, PARTIAL, and ERROR are used deterministically
- [ ] Repository roles are not represented as human organizational authority
- [ ] No director gate, subagent, write, or downstream workflow is invoked
- [ ] Output conforms to onboarding_context/v2

---

## Coverage Notes

Behavioral fixtures must prove zero filesystem mutation and verify that denied sources were not opened, not merely absent from final prose. Catalog results remain blank until these cases are actually executed.
