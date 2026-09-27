# Git operations and recovery

Read before preparing, resuming or promoting a batch. Run Git with explicit
worktree paths and argument arrays, without a shell built from user refs.
Resolve refs to full commit SHAs before merge commands.

## Read-only helper

```text
python .agents/skills/integrate-worktrees/scripts/inspect_worktrees.py \
  --repo <checkout> --into <local-branch> \
  --source <ref> [--source <ref> ...] \
  [--pin <ref> <full-delivered-SHA> ...] [--candidate <integration-checkout>]
```

`--pin` takes two values and is repeatable; only a full commit ID is accepted.
It is never replaced by a newer tip. The explicitly handed-over SHA remains
authoritative even when the source branch was rebased and its current tip is a
sibling; report `ref_moved` and keep the fixed delivery. A deleted source label
may likewise identify a resolvable pinned delivery with an explicit warning.
Pins must be real commits with target-related history; malformed refs, invalid
pins and unrelated target history block. The helper never fetches missing objects.

JSON `schema_version: 1` has `repository`, `target`, `sources`, `candidate`,
`worktrees`, `duplicates`, `warnings`, `blockers` and `ok`. Sources include
`ref_sha`, chosen `sha`, `pinned`, `merge_base`, `changed_files`,
`already_merged_target` and `already_merged_candidate`. Candidate is null when
not supplied. Target and worktree branches use canonical `refs/heads/` names;
source labels preserve input. `already_merged` means ancestry, not proof that
a later revert preserved behavior. Exit 0 means no detected Git blockers;
1 means a blocker; 2 means bad arguments. Read JSON even after a nonzero exit.

The stdlib Python helper writes no files and invokes Git without shell expansion.
It cannot certify human approval, other-chat inactivity, semantic consistency or
runtime behavior. Detect target movement by comparing fresh `target.sha` with
the journal, not by assuming the first inspection stays current.

## Location and branch safety

1. Inspect `list_artifacts` before allocating. Reuse only a free integration
   worktree in the same common repository whose journal and branch match the
   batch. A name alone is not proof it is free or safe.
2. Otherwise call app `create_worktree` with `allowAsync: true`, an integration
   name and the pinned target SHA as `ref`. If pending, check its operation
   status at reasonable intervals. Registration failure with a returned path
   is not permission to create a duplicate; inspect that checkout first.
3. Use the returned absolute workspace. If HEAD is detached, create a unique
   `codex/integrate-<batch>` branch there with `git switch -c <name> <target-SHA>`.
   Never rename, reset or replace an existing branch to force reuse.
4. Verify common Git directory, HEAD, named branch, clean state and operations.
   Its branch differs from all source branches and target. A new candidate starts
   exactly at pinned target SHA; a resumed candidate must contain the journal's
   original target SHA as an ancestor.
5. Shell `git worktree add` is a fallback only when app capability is unavailable
   or the user explicitly chose CLI management. Include its exact path/branch
   in the authorized preview. A slow pending operation or failed registration
   does not mean the capability is unavailable.

Never use forced checkout, hard reset, forced branch updates, stash, worktree
removal or branch deletion to pass preflight. Operate on the target at its
actual clean/inactive checkout, not via `update-ref` from the candidate. If no
target checkout exists, obtain an appropriate app-managed checkout (or authorized
CLI fallback), verify it is free, then switch that checkout to the existing
target branch for `merge --ff-only`. Never switch a development checkout away
from its task. No step authorizes another task's active work to be interrupted.

## Local journal

After the one operation authorization, create a unique batch file in the
coordinator's ignored `production/integration-runs/`. Check the
exact path with `git check-ignore` and `git ls-files`: an ignored pattern does
not make an already tracked file local. Do not fix ignore rules implicitly.
`--check-only` never writes a journal or checkpoint.

Store at least this structure, using actual values rather than placeholders:

```json
{
  "schema_version": 1,
  "batch": "unique-id",
  "common_git_dir": "absolute-directory",
  "coordinator_root": "absolute-checkout",
  "target": {"ref": "main", "initial_sha": "full-sha", "observed_sha": "full-sha"},
  "sources": [
    {"ref": "task/a", "sha": "full-sha", "task_base_sha": null, "outcome": "pending", "merge_commit": null}
  ],
  "candidate": {"path": null, "branch": null, "head": null},
  "phase": "prepared",
  "pending_merge": null,
  "decisions": [],
  "evidence": [],
  "promotion": null
}
```

Also preserve fixed task-base SHAs, cumulative delivery file scopes, task verdicts,
dependencies, accepted decisions and authorization boundary. Record target and
candidate stage values, their checked SHAs, any targeted restoration and any
separately authorized combined-candidate phase transition. Evidence entries name command/manual method, scope,
checked SHA, actual result, observed time and outstanding conditions. Preserve
invalidated earlier evidence as history. Record fixes and target refreshes;
`initial_sha` and each source `sha` stay immutable. A new delivery needs an
explicitly amended/new batch and revalidation, not silent source advancement.

Update after each completed operation and before the next. Use a temporary file
in the same ignored directory and atomic replacement to avoid interrupted JSON.
If persistence fails, stop starting operations and report actual Git state.
Record the absolute journal location in the integration context. The journal
may lag a command; recovery always verifies Git rather than trusting labels.

## Serial merges

For each delivery in the previewed order:

1. Test pinned SHA ancestry of candidate HEAD. Already-ancestor sources are
   recorded and skipped, without fabricating another merge or semantic PASS.
2. Verify clean state and no active operation; record proposed pending SHA.
3. Run `git merge --no-ff --no-commit <full-SHA>` in the candidate worktree.
4. Inspect `MERGE_HEAD`, unmerged entries and the diff even on command success.
   Resolve only authorized paths and respect product decisions.
5. Ensure no unmerged entries remain, review the complete staged result, stage
   only intended paths and commit the completed merge before the next source.
6. Record actual HEAD, ancestry and conflict decisions in the journal.

Extra corrections are scoped commits on the candidate. Use literal commit
message arguments or a prepared message file, never shell interpolation of
user text. A commit failure leaves the operation pending, not completed.

## Interrupted and repeated runs

Match journals by common repository, target and exact ordered pinned delivery
set. One exact match resumes; multiple plausible matches need selection. Do not
reuse journals with different deliveries/targets silently. Inspect actual HEAD,
branch, dirty state, ancestry and Git operations first.

- With `MERGE_HEAD`, require exactly the recorded pending source SHA or target
  refresh SHA. Inspect and continue that same authorized merge. An unexpected
  or multiple merge head blocks. Never start another merge or auto-abort.
- A crash after commit but before journal update may leave a completed source
  marked pending. Confirm it from ancestry/history, record the actual commit
  and skip it. Unexplained HEAD movement blocks.
- Dirty state without the matching operation or documented authorized fix is
  not assumed to belong to the batch. Resolve its identity before any write.
- Rebase/cherry-pick/revert/bisect is not this merge workflow's recovery state;
  report and stop without completing or aborting it.
- If all deliveries are ancestors of target, do not repeat merges. Evidence
  must still cover the exact current target; otherwise inspect and revalidate.

Helper `candidate_operation`/`candidate_dirty` findings for a known interrupted
merge mean ordinary preflight failed. The explicit recovery checks above permit
resuming that exact authorized merge, not bypassing dirty checks generally.

## Promotion and drift

Require clean, committed candidate HEAD and current evidence bound to that SHA.
Compare fresh target SHA with journal `observed_sha`. For ordinary advancement,
pin the new SHA, merge it into candidate with `--no-ff --no-commit`, resolve,
commit and revalidate. If already an ancestor, verify and refresh the snapshot.
Recheck the refreshed target stage against candidate using the stage-state rules
in phase validation; a source or stale target stage must not be promoted silently.
If target history was rewritten rather than advanced, stop for user investigation.

Recheck target cleanliness, inactivity, operations, stage-state evidence and
ancestry. Current target
must be an ancestor of the verified candidate. Run only
`git merge --ff-only <verified-candidate-SHA>` at the target checkout. A race or
failed fast-forward returns to inspection and revalidation, never force/reset or
another merge strategy. Confirm final target equals the verified SHA. After a
crash following promotion, matching target and evidence allow recording the
already completed operation rather than repeating it.

Keep Git and verification results separate on failure. Missing evidence never
authorizes promotion. Do not remove worktrees/branches, push or publish.
