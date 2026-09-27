# Skill Spec: `$integrate-worktrees`

> **Category**: pipeline
> **Priority**: high
> **Spec written**: 2026-09-27

## Skill Summary

Integrates explicitly delivered Git commits in a dedicated worktree and branch,
revalidates the combined result, and fast-forwards the target only after required
checks pass. The interface is `$integrate-worktrees <source-ref...> --into
<target-branch> [--check-only]`. Source branch names identify deliveries; a
handover's full commit SHA fixes the delivered version. Git preflight is distinct
from semantic review and from permission to mutate Git state.

## Static Assertions

- [ ] Frontmatter has exactly non-empty `name` and `description`; identity matches the directory
- [ ] UI metadata contains the exact `$integrate-worktrees` invocation and a complete description
- [ ] Workflow has actionable phases, explicit blocked/pending/success outcomes, and a final handoff
- [ ] Shared worktree protocol and handover format are referenced rather than reimplemented inconsistently
- [ ] `--check-only` and the bundled inspection helper are explicitly read-only
- [ ] Helper output cannot prove design consistency, test success, or user authorization

## Director Gate Checks

No new integration-specific director gate applies in full, lean, or solo mode.
Existing review, consistency, story, smoke, and QA workflows keep their own mode
rules. Integration neither approves a GDD automatically nor advances the project
stage. An authoring conversation does not become an independent reviewer merely
because it creates another directory or branch.

## Test Cases

### Case 1: Happy path — two deliveries, isolated integration, verified fast-forward

**Fixture:** Two task branches descend from one target commit. Both have exact
handover SHAs, approved decisions, and declared checks. A dedicated integration
worktree starts at the target commit. The bounded local Git operations are authorized.

**Expected behavior:** Inspect deliveries; merge their fixed SHAs in dependency
order; reconcile shared records; run required checks; recheck target state; use
fast-forward-only promotion; report delivered and resulting commits.

**Assertions:**
- [ ] Sources are merged in a dedicated integration checkout, not directly in the target checkout
- [ ] Current task ownership and all required file templates are preserved
- [ ] Target SHA is unchanged before validation completes
- [ ] Final target SHA is exactly the verified integration SHA
- [ ] Report distinguishes merged, verified, and promoted states

### Case 2: Read-only preflight and check-only

**Fixture:** Same deliveries; invoke `--check-only` from a subdirectory in a path
containing spaces. Snapshot refs, tracked content, index, worktree inventory, and
integration journals before the run.

**Assertions:**
- [ ] Output includes target snapshot, fixed source SHAs, overlaps, dependencies, risks, and required validation
- [ ] Refs, files, index, worktree inventory, and integration journals remain unchanged
- [ ] No worktree, branch, merge, commit, stash, fetch, or report file is created
- [ ] Refusal or unavailable Git is explicit, never a passing semantic verdict

### Case 3: Delivery pin survives source advancement

**Fixture:** A handover names commit A; its branch has since advanced to B.

**Assertions:**
- [ ] A remains the delivery; the branch movement is disclosed
- [ ] B-only changes are excluded without an explicit updated delivery
- [ ] Missing/invalid commit objects and pinned histories unrelated to the target block integration
- [ ] After a source ref is rewritten, a related valid delivery SHA still prevails; the ref mismatch is disclosed rather than silently replacing the pin
- [ ] Uncommitted source edits are disclosed as excluded; they are not silently staged or merged
- [ ] A task with no committed delivery stays pending rather than reporting merge-ready output

### Case 4: Dirty target, in-progress Git operation, and invalid environment

**Fixture:** Variants include dirty target/candidate, merge or rebase in progress,
missing refs, detached candidate, and a candidate from another repository.

**Assertions:**
- [ ] Unsafe target/candidate state blocks mutation with exact affected paths
- [ ] No automatic stash, reset, checkout override, abort, or cleanup occurs
- [ ] A detached task delivery requires a named task branch before final handover
- [ ] Unavailable managed worktree tooling is disclosed with a supported local fallback or concrete blocker
- [ ] The actual returned checkout path is used; no assumption that creating a worktree changes the calling chat's cwd

### Case 5: Mechanical conflicts retain both valid contributions

**Fixture:** Two GDD tasks change the same systems index, registry, and progress
table, including overlapping counts and separate new entities.

**Assertions:**
- [ ] Both valid entries survive; counts, unique IDs, references, and dependencies are reconciled
- [ ] A whole-file ours/theirs choice never replaces content review
- [ ] Conflict fixes stay within the authorized integration changeset
- [ ] An interrupted merge preserves the integration state and target SHA

### Case 6: Clean Git merge can still contain design conflict

**Fixture:** Non-overlapping lines assign incompatible units or values to the
same cross-system concept. Git can merge without textual conflict.

**Assertions:**
- [ ] Independent review of delivered GDDs and shared-record reconciliation inspect the combined result, including the conflicting units or values
- [ ] Not running the optional consistency check does not waive a known design conflict
- [ ] User sees competing decisions and impact before a meaning-changing resolution
- [ ] Missing user decisions keep promotion pending; no timeout implies consent
- [ ] Downstream architecture/story impact is inspected where present
- [ ] Branch `Designed`, `Approved`, or `Complete` states do not automatically validate the combined result

### Case 7: Separate task tests pass; combined tests fail

**Fixture:** Branch A changes a caller expectation; branch B changes a callee
result. Their own checks pass, but their combination fails an integration check.

**Assertions:**
- [ ] Actual affected and integration commands run on the candidate revision
- [ ] Failure prevents target promotion and retains candidate evidence
- [ ] Programmer-owned repair and affected rechecks are required before promotion
- [ ] Missing mandatory automation or manual evidence is pending/blocked, never implied PASS
- [ ] Final report names the tested revision and commands/results

### Case 8: Target advances during integration

**Fixture:** After successful candidate checks, target gains another commit.

**Assertions:**
- [ ] Target snapshot is compared again immediately before promotion
- [ ] New target changes enter the integration branch before renewed validation
- [ ] Previous passing evidence is not reused as proof for the changed candidate
- [ ] Promotion uses fast-forward-only semantics; divergence cannot be forced
- [ ] Further target movement causes another inspect/revalidate cycle or a clear pending result
- [ ] Target refresh also repeats the target/candidate stage comparison; an earlier stage decision is not carried forward blindly

### Case 9: Duplicate and already-integrated delivery

**Fixture:** Same ref is listed twice, two refs point at the same commit, or a
delivery is already an ancestor of target/candidate. In the last variant, the
target later reverted a delivered behavior, so helper `changed_files` is empty
although the original handover's acceptance scope remains material.

**Assertions:**
- [ ] Duplicate refs/SHAs are reported and not applied twice
- [ ] Ancestor checks distinguish already in target from already in the integration candidate
- [ ] Repeated integration preserves valid existing work and does not fabricate fresh validation
- [ ] Declared dependency order is preserved for remaining deliveries
- [ ] Already-ancestor status skips only the duplicate merge, never semantic or acceptance revalidation
- [ ] Review scope is reconstructed from each fixed task-base-to-delivery diff and handover scope, plus affected dependencies and integration corrections
- [ ] Empty helper `changed_files` and a later target revert cannot shrink that scope or produce VERIFIED without the applicable checks
- [ ] Missing original task base or delivery scope stays NOT VERIFIED until established, rather than being inferred from current ancestry

### Case 10: Restart an interrupted integration from its journal

**Fixture:** An ignored journal at `production/integration-runs/<batch>.json`
records the batch's fixed sources, target snapshot, candidate branch/path and
pending checks. Restart after one successful merge or during the next recorded
merge. A variant crashes after a merge commit but before the journal update.

**Assertions:**
- [ ] The recorded batch journal can resume integration without an active.md identity requirement
- [ ] Candidate branch/path/HEAD, fixed sources, prior merges, target snapshot, and pending checks are reverified against actual Git state
- [ ] A matching recorded pending merge may resume; unexpected Git operations or unexplained candidate changes block new mutations
- [ ] A commit completed before the journal update is verified from Git ancestry/history and recorded without merging the source again
- [ ] The journal is ignored and untracked, never enters a merge commit, and is not created or modified by check-only

### Case 11: Authorization and completion boundaries

**Assertions:**
- [ ] Existing bounded user authorization is honored without per-file/per-merge prompts
- [ ] Missing authorization results in one complete local changeset proposal after preflight
- [ ] A design choice or material scope expansion is surfaced separately
- [ ] No automatic push, publish, branch deletion, worktree removal, or project-stage advancement
- [ ] Final report includes source/target/candidate SHAs, resolved conflicts, tests, pending work, and next action

### Case 12: Stage-specific evidence and serial compatibility

**Assertions:**
- [ ] GDD delivery retains independent design review, shared-record reconciliation and applicable downstream-impact checks; consistency-check stays optional and cross-GDD review waits until all MVP GDDs are authored and individually approved
- [ ] Code delivery runs affected/integration tests and existing review/story checks; sprint completion retains smoke/QA gates
- [ ] Other artifact types use their originating workflow's required checks; unknown requirements stay unverified
- [ ] Normal task skills retain their arguments and do not automatically create or switch worktrees
- [ ] A fresh integration conversation is required when author/reviewer independence applies

### Case 13: Source stage advancement does not silently promote the target

**Fixture:** Target `production/stage.txt` is Systems Design. A source delivery
contains its own gate-driven update to Technical Setup. The text merges cleanly,
but no phase transition for the combined candidate is authorized or evidenced.
Variants exclude the stage correction from the authorized changeset, explicitly
authorize a combined phase gate, or advance the target during integration.

**Assertions:**
- [ ] Target and candidate stage files are compared after merges even without a textual conflict
- [ ] By default the candidate retains the target's stage; a source branch's gate result does not authorize combined-stage advancement
- [ ] Restoring the target stage must be inside the previewed correction scope; otherwise promotion is BLOCKED until the boundary is resolved
- [ ] A changed candidate stage requires separate combined-phase-gate authorization and evidence satisfying the existing gate rules
- [ ] Ordinary integration verification or a source-only gate PASS cannot substitute for that authorization and evidence
- [ ] Target drift triggers a fresh stage comparison and corresponding candidate correction/gate checks before promotion

### Case 14: GDD batches retain the original review milestones

**Fixture:** Integrate one completed, independently reviewed GDD. The candidate
contains two individually approved MVP GDDs, while a third MVP GDD is unfinished.
Variants complete and individually approve the final MVP GDD, omit the optional
consistency check with all applicable required checks passing, or expose a known
design conflict as in Case 6.

**Assertions:**
- [ ] Readiness comes from the candidate's actual MVP GDDs and systems index, not the number of existing GDDs or completion of the delivered batch
- [ ] While any MVP GDD remains unfinished or lacks individual approval, review-all-gdds is not run and is reported as not yet due, not missing required batch evidence
- [ ] A completed single-GDD delivery may be verified and promoted after its applicable required checks pass even while other MVP GDDs remain unfinished
- [ ] Once all MVP GDDs are authored and individually approved, review-all-gdds full is required under its normal prerequisites before advancing to Technical Setup; unrelated unfinished non-MVP work does not postpone this milestone
- [ ] At that milestone, missing required cross-review evidence or a FAIL verdict prevents verified promotion; unmet skill prerequisites never become an invented PASS
- [ ] Not running consistency-check alone does not produce NOT VERIFIED or BLOCKED, or prevent promotion
- [ ] Known design conflicts, missing applicable required evidence and unresolved decisions still prevent verified promotion even when consistency-check is omitted
- [ ] Deferred review is reported separately from batch verification; integration does not approve unfinished GDDs, claim a project-wide review passed, or advance the project stage

## Protocol Compliance

- [ ] Reads handovers, Git history, applicable artifacts, and evidence before writes
- [ ] Preserves original artifact schemas and follows the common handover/integration-journal format
- [ ] Uses one bounded authorization for local integration writes and Git mutations
- [ ] Honors department ownership for fixes; product decisions stay with the user
- [ ] Has no implicit network, deployment, cleanup, or phase-advancement side effects
- [ ] Ends with a truthful result and concrete next action

## Coverage Notes

`tests/test_worktree_preflight.py` executes the actual read-only Git helper and
isolated Git worktree fixtures. Fixture merge/validation/promotion commands test
Git mechanics and failure invariants; they are not a live execution of the full
agent skill. Conversational decision handling, GDD semantic detection, independent
review, and configured downstream skill execution require live workflow evidence.
The reverted-delivery scope and phase-state fixtures above are written-contract
cases; the existing helper/Git fixture run does not claim to execute them.
Static `$skill-test spec` PASS means written-contract coverage only. Do not fill
catalog `last_*` fields with assumed or fabricated execution results.
