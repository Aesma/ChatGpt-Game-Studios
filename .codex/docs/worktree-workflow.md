# Worktree Collaboration

Use this shared protocol for any workflow running in a linked worktree or
handing committed branch results to another chat. Existing skills keep their
arguments, business artifacts, review modes, and user design decisions.

## Starting a task

The user chooses how many independent chats to open and their tasks. In the
Codex new-chat interface they select Worktree and a starting branch; Codex
prepares the checkout. This framework does not automatically create chats,
switch existing chats, send messages, or turn ordinary local work into worktree
work. Explicit requests to create a chat/worktree may use the available app
tools; prefer managed worktrees and inspect existing attachments before creating
another. Always operate in the returned absolute workspace path.

At task start, read the actual Git top level, branch (or `HEAD` when detached),
full HEAD commit, working-tree status, and any unfinished Git operation. Show
these together with the task and its intended files. Resolve paths relative to
this checkout, including from subdirectories. A `.git` file is valid for linked
worktrees; never assume it is a directory. Read each applicable AGENTS.md.

Record the task's initial commit as its fixed base in the task-start summary
and retain it in the handoff. A reused checkout needs its prior changes and
ongoing work accounted for before starting another task. Existing uncommitted
or untracked files are not automatically part of this task. If source context
is missing, disclose it; do not invent decisions from another chat. Dependencies
may be developed in parallel only under the original skill's explicit contract
or accepted assumptions; record those assumptions in the handoff.

## Branch-local business work

Continue using `$design-system`, `$dev-story`, and other existing skills.
Each task may update all business files in its authorized changeset, including
its own copies of project-wide files:

| Project file | Shared meaning |
|---|---|
| `design/gdd/systems-index.md` | Systems, GDD links, dependencies, design progress |
| `design/registry/entities.yaml` | Cross-system entities, items, formulas, constants |
| `production/sprint-status.yaml` | Story progress within a sprint |

These are separate physical files in each checkout. Conflicting edits are
reconciled when branches are integrated, not by imposing a global single writer.
Other shared artifacts are identified from the actual changes. Subagents inside
one checkout still need non-overlapping write ownership.

Keep existing business statuses. `$dev-story` leaves its story In Progress;
`$story-done` can close it after the normal evidence and authorization checks.
Every report applies only to the checkout and revision actually inspected.
Include `Scope: <branch> @ <full HEAD>; clean | uncommitted changes` in status,
review, and gate results. If Git is unavailable, report scope as unknown.
Uncommitted changes mean the result is not evidence for HEAD alone.

An authoring verdict or a branch's Complete/done status is not proof that a
combined target version passes. Do not infer live progress in other chats from
this checkout's snapshot. A phase gate may update only this checkout under its
existing rules; integration does not automatically advance the target's stage.

Compare candidate and target `production/stage.txt` explicitly before promotion.
A source's stage change needs separate transition authorization and combined
gate evidence; otherwise preserve the target stage within the authorized
candidate corrections, or block promotion when that correction is not authorized.

## Handoff from a writing task

When a linked-worktree task finishes or is handed off, append this concise
record to the original skill's result. Do not add a preparation skill or require
a shared task database. Keep detailed decisions in their existing artifacts.

```text
Task: <name and invoked skill>
Worktree / branch: <absolute path> / <branch>
Base commit: <fixed task-start SHA>
Delivery commit: <full SHA, or PENDING COMMIT>
Working tree: <clean, or list remaining tracked/untracked changes>
Delivered files: <actual paths and purpose, including shared artifacts>
Accepted decisions: <decision and supporting artifact section>
Dependencies / contracts: <versions, assumptions, interfaces, units>
Verification: <actual commands/review context, results and evidence scope>
Unverified / unresolved: <missing checks, user decisions, blockers>
Integration verification: PENDING
```

The user carries this summary to an independent integration chat. Git carries
the files; no copying of full documents or automatic cross-chat messaging is
required. Only claim committed files are delivered when they are in the stated
commit. Dirty work can be reported but remains pending delivery. A read-only
review may hand off evidence for an existing revision without creating a commit.

Before delivering from detached HEAD, create a unique `codex/<task>` branch
under the authorized task scope. Commits still require the user's instruction;
an implementation request alone does not authorize committing. Stage only
task-owned files after reviewing their diff. Preserve unrelated work.
If an old base was never recorded, disclose that gap and confirm the intended
comparison baseline rather than fabricate the task-start SHA.

Pin the full delivery SHA. Subsequent branch edits require a new delivery record
and updated verification. Older evidence does not automatically cover them.
The next action for committed parallel results is `$integrate-worktrees` in an
independent chat, alongside any still-required original review or story closure.

## Integration and promotion

Use `$integrate-worktrees <source-ref...> --into <target-branch>`; add
`--check-only` for a read-only preflight. The integration skill owns this sequence:

1. Inspect handoffs and Git history; pin each delivery and target commit, scope,
   dependencies, overlap and required checks. Existing Git authorization is
   retained; obtain one bounded authorization only if still missing.
2. Create or reuse a dedicated integration worktree on a `codex/integrate-*`
   branch based on the target. Merge pinned sources in dependency order. Finish
   each merge before starting another; all merge/fix commits stay here.
3. Preserve valid additions on both sides; reconcile shared entries, IDs,
   references and counts. Escalate contradictory product decisions to the user.
   Successful Git auto-merge is not a semantic verdict.
4. Validate the combined result with the applicable existing reviews/tests.
   Record the exact candidate revision and outstanding human evidence. On
   failure, preserve the candidate and report partial results; do not promote.
5. Recheck target state. If it advanced, merge its current revision into the
   candidate and revalidate affected evidence. Promote only by fast-forward
   into a clean, idle target checkout, then verify its final SHA.

The skill records an ignored integration journal at
`production/integration-runs/<batch>.json` for interrupted integration runs. Resume from
its pinned revisions and actual Git state; do not merge moving branch tips or
skip checks merely because an ancestor was already merged. Promotion requires
all mandatory evidence for the final candidate. Push, publication, branch
deletion and worktree cleanup are separate user instructions.
