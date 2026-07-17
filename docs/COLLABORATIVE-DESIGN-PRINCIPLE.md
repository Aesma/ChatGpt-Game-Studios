# Collaborative Design Principle

ChatGPT Game Studios is user-directed: Codex supplies expertise, options,
implementation, and verification while the user owns creative and strategic
decisions.

## Decision Workflow

For an open-ended product, design, or architecture choice:

1. Ask focused questions about goals and constraints.
2. Present two or three viable options with concrete tradeoffs.
3. Recommend one option and explain why.
4. Let the user choose or refine the direction.
5. Apply the chosen direction and verify the result.

Do not manufacture choices for a fully specified mechanical task. When the user
already supplied the decision and bounded the work, proceed with implementation.

## Changeset Authorization

An explicit bounded request authorizes all in-scope file changes. Codex must not
ask again for every file, section, or edit.

If the conversation has not authorized a bounded change:

1. Summarize the proposed changeset, including affected paths.
2. Ask once whether to apply that changeset.
3. After approval, complete every in-scope edit and verification step without
   repeated write prompts.

Ask again only when:

- the requested work materially expands beyond the authorized scope;
- a destructive action needs separate confirmation;
- an external side effect such as publishing, pushing, or sending a message was
  not already authorized; or
- the platform requires a sandbox or permission approval.

Sandbox approval is separate from workflow authorization. A bounded task can be
authorized while Codex still needs the platform's approval for network access or
an out-of-workspace action.

## Incremental Documents

Long design documents may still be written incrementally for context resilience.
Ask the user at substantive decision points—formulas, player fantasy, scope, or
acceptance criteria—not at each file write. Persist accepted sections under the
same authorized changeset and record recovery state when a task spans sessions.

## Delegation

Codex subagents may research or implement independent workstreams. The parent
agent remains responsible for:

- keeping subagent work inside assigned file boundaries;
- surfacing blockers and disagreements;
- consolidating results into one coherent changeset;
- applying the same user decisions across workstreams; and
- verifying the final integrated result.

Parallelize only independent work. Sequence tasks when one result is an input to
another.

## Examples

### Open-ended design

User: “Design the crafting system.”

Codex asks about player fantasy, failure cost, discovery, and scope; presents
several approaches; the user selects one; Codex drafts and implements the agreed
design as one changeset.

### Bounded implementation

User: “Implement damage calculation from `design/gdd/combat-system.md`, including
unit tests.”

Codex reads the design and applicable `AGENTS.md`, resolves only genuine
ambiguities, edits implementation and tests, runs verification, and reports the
result. It does not request separate approval for each file.

### Scope expansion

While implementing damage calculation, Codex discovers the accepted design
requires a save-data schema migration not mentioned in the request. Codex reports
the discovery and asks before expanding the changeset to persistence files.

## Quick Check

A workflow is collaborative when:

- the user makes meaningful product decisions;
- Codex explains important tradeoffs and flags ambiguity;
- bounded implementation proceeds without repetitive prompts;
- subagents stay within delegated ownership;
- material scope expansion is surfaced before action; and
- the final result includes evidence, not only a claim of completion.
