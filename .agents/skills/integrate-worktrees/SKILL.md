---
name: integrate-worktrees
description: "Integrate delivered commits from independent worktree chats into a target branch, reconcile shared documents, and verify the combined result before promotion. Use across design and implementation phases; check-only reports readiness without changing files or Git state."
---

## Invocation and execution

Invoke as `$integrate-worktrees <source-ref...> --into <target-branch> [--check-only]`.
Require at least one source and exactly one local target branch. Reject missing
values, duplicate control flags, and unknown flags before mutation. Source refs
identify deliveries, not a request to consume every future branch update.

Read `.codex/docs/worktree-workflow.md`. Independent chats keep using normal
skills and update their own registry, index, Sprint and shared files. Do not
impose a global single writer or create new development chats. This skill
coordinates one integration batch.

Read [Git operations and recovery](references/git-integration.md) before preparing
or resuming a batch, and [phase validation](references/phase-validation.md) when
classifying changed files. Keep the original task verdict distinct from
integration verification against a precise candidate commit.

## 1. Inspect and pin deliveries

Remain read-only. Obtain handovers from this conversation or explicitly provided
records: source ref and full delivered commit, task base, file scope, accepted
user decisions, dependencies, tests and unresolved issues. Do not imply access
to another chat's unprovided history. Gather missing context while independent
inspection continues.

Run `scripts/inspect_worktrees.py` with sources, target and supplied handover
SHAs as `--pin REF SHA`. Its JSON describes Git facts only. A successful exit
is not semantic review, a test result or authorization to merge.

- Without a handover SHA, resolve the source once and show that exact proposed
  SHA in the batch preview; pin it when the user accepts the delivery.
- If a branch moved after handover, retain the handed-over SHA and show the
  difference. Never substitute the newer branch tip silently, including after
  a rebase: the explicit delivery SHA remains authoritative when it is a valid
  commit with target-related history.
- Verify source commits have related repository history, target is a local
  branch, and relevant worktrees share the Git common directory. Inspect dirty
  state and active operations before planning any mutation.
- Report source uncommitted changes as excluded from the committed delivery.
  Do not commit or copy them automatically.
- Inspect existing batch journals and actual Git state before starting anew.
  Reuse an exact matching batch as described in the recovery reference.
- Deduplicate identical source SHAs and detect already integrated sources, but
  retain each delivery's original scope for review: fixed task-base-to-delivery
  changes plus dependencies and integration fixes. The helper's empty changed
  list for an ancestor is not proof that a later revert preserved its behavior.
  Missing original base/scope must be established or remain NOT VERIFIED.

Show pinned sources, target SHA, affected paths, likely semantic conflicts,
required validation, blockers and proposed integration location/branch. Git
cannot prove another chat stopped editing; establish target inactivity from
available task status and handover evidence before promotion.

### Check-only

With `--check-only`, stop after this read-only assessment. Do not create a
worktree, branch, journal, checkpoint, report, commit or merge; do not stage,
fetch, stash, resolve conflicts, run a mutating skill or promote the target.
Report `CHECK COMPLETE` or `BLOCKED`, and `Integration: NOT VERIFIED` unless
existing evidence covers the exact current combined commit. Separate source
tests do not verify a prospective merge.

## 2. Authorize and prepare

Preview one concrete operation/file set: integration branch and worktree,
ordered pinned sources, merge/fix commits, allowed conflict fixes, any targeted
candidate restoration of the target's stage value, ignored journal, validation
and final fast-forward target promotion. Reuse existing
explicit Git authorization that covers the batch; otherwise obtain it once
before mutation. Task completion alone does not authorize commits or merges.
Material scope expansion and new product decisions return to the user, without
repeating authorization for each file.

Prefer app-managed worktrees: inspect `list_artifacts`, reuse a suitable free
integration checkout, or call `create_worktree` with the explicit target SHA.
Use a unique `codex/integrate-*` branch there. Follow the recovery reference for
asynchronous creation and CLI fallback. Never integrate in a source checkout or
an actively used target checkout.

Prepare one journal in the coordinator checkout at
`production/integration-runs/<batch>.json`. Include that write
in the preview, verify the exact path is ignored and untracked, and record its
absolute location. Do not silently track the integration journal or create
competing journals in multiple checkouts. This journal records integration
operations; actual Git state remains authoritative. Write its prepared
record before worktree/branch creation, then record each returned operation ID,
path and branch before proceeding.

## 3. Integrate on the candidate branch

Process pinned sources serially with `git merge --no-ff --no-commit <full-SHA>`.
Resolve and review each source's result, then commit its completed merge before
starting another. Skip and record already-ancestor deliveries. Never start a
second merge while `MERGE_HEAD` exists.

Resolve shared files by meaning as well as syntax:

- Preserve independent valid registry/index/Sprint entries; check duplicate IDs,
  sources, values, units, dependencies, ownership and conflicting status changes.
- Recompute totals from combined records. Never choose whole-file ours/theirs
  or assume automatically merged counts are correct.
- Preserve accepted product decisions. Contradictions and replacements need a
  user decision showing both source sections and downstream effects.
- Branch task statuses remain evidence about their own revisions. Reconcile
  combined story/Sprint records against actual files and current evidence;
  merged `Complete`/`done` labels do not prove integration success.
- Compare target and candidate `production/stage.txt` after merging. Integration
  alone never authorizes carrying a source phase transition into the target.
  Follow the stage-state safeguards in phase validation; restore only the known
  target stage in the candidate under the previewed scope, or block promotion.

Record merge/fix commits, decisions and issues in the journal. Make authorized
corrections only on the integration branch. A blocker keeps the candidate
recoverable and leaves the target unchanged.

## 4. Verify the combined commit

Once all sources and corrections are committed and the candidate is clean,
pin HEAD and run applicable checks from the phase-validation reference. Cover
the union of changed domains; one profile never waives another. Record commands,
scopes, actual results, human sign-off and checked SHA in the local journal.
Subsequent content changes invalidate affected evidence.

Missing tools, unrun tests, stale evidence, unresolved decisions or missing
required human evidence produce `NOT VERIFIED` or `BLOCKED`, never promotion.
Do not change review mode or manufacture approval to finish the batch.

## 5. Promote and report

Re-inspect immediately before promotion. Require clean and inactive target,
clean candidate, no active Git operation, every pinned source reachable from
candidate HEAD, and valid evidence for that exact HEAD. If target advanced,
merge its new pinned tip into the integration branch, commit, reconcile and
reverify before promotion. Recompare its current stage with the candidate; an
older stage decision or evidence cannot cover this new target snapshot. See the
reference for rewritten history and races.

Promote only via `git merge --ff-only <verified-candidate-SHA>` at the target
checkout. Do not reset, force-update or detach another checkout to make this
succeed. If target has no checkout, use the reference's authorized checkout
procedure. Failed fast-forward returns to inspection, never a fallback merge
strategy. Confirm target equals the checked candidate and record promotion.

Report source refs/fixed SHAs, target/final SHA, candidate branch/path, original
task verdicts, separate `Integration: VERIFIED / NOT VERIFIED / BLOCKED` at the
checked commit, decisions, evidence, remaining issues and journal path. State
explicitly whether target promotion happened.

Never push, publish, archive/delete worktrees or branches, or clean up as a
consequence of success. Keep candidate and journal for review and recovery.
