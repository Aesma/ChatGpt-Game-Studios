---
name: hotfix
description: "Emergency fix workflow that bypasses normal sprint processes with a full audit trail. Creates hotfix branch, tracks approvals, and ensures the fix is backported correctly."
---

## Invocation and execution

Invoke this workflow as `$hotfix`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[bug-id or description]`. Treat bracketed values as optional unless the workflow says otherwise.


> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$hotfix`. Do not auto-invoke based on context matching.

## Phase 1: Assess Severity

Read the bug description or ID. Assess severity using these criteria:

- **S1 (Critical)**: Game unplayable, data loss, security vulnerability
- **S2 (Major)**: Significant feature broken, workaround exists
- **S3 or lower**: Minor issue — normal bug fix workflow applies

Confirm by asking the user directly:
- Prompt: "I've assessed this as **[assessed severity]** — [brief rationale]. Confirm severity to proceed:"
- Options:
  - `[A] S1 (Critical) — game unplayable, data loss, or security issue`
  - `[B] S2 (Major) — significant feature broken, workaround exists`
  - `[C] S3 or lower — redirect to normal bug fix workflow`

If [C]: stop. Verdict: **REDIRECTED** — use the normal bug fix workflow for S3 and below.

---

## Phase 2: Draft Hotfix Record In Memory

Draft the hotfix record:

```markdown
## Hotfix: [Short Description]
Date: [Date]
Severity: [S1/S2]
Reporter: [Who found it]
Status: IN PROGRESS

### Problem
[Clear description of what is broken and the player impact]

### Root Cause
[To be filled during investigation]

### Fix
[To be filled during implementation]

### Testing
[What was tested and how]

### Approvals
- [ ] Fix reviewed by lead-programmer
- [ ] Regression test passed (qa-tester)
- [ ] Release approved (producer)

### Rollback Plan
[How to revert if the fix causes new issues]
```

Keep this record in memory. Do not create or update any workspace file in this phase. The record joins the complete changeset only after Phase 3 has established the confirmed hotfix branch (or the user has explicitly accepted a non-Git current workspace) and Phase 4 has identified every code, test, record, and bug-file edit.

---

## Phase 3: Create Hotfix Branch

Check whether this is a git repository:

Run `git rev-parse --is-inside-work-tree` as a read-only repository check. Do not write any file before this check and the branch decision are complete.

If this is not a Git repository, state: "Not a Git repository; the hotfix can only be implemented in the current workspace." Ask the user to confirm current-workspace implementation before continuing. If they decline, output **HOTFIX BLOCKED** and stop.

If the check passes, ask the user directly before creating the branch:
- Prompt: "Ready to create hotfix branch 'hotfix/[short-name]' from [base-ref]?"
- Options:
  - `[A] Yes — create branch`
  - `[B] Use a different base ref — I'll specify it`
  - `[C] Skip — I'll create the branch myself`

Only run `git checkout -b hotfix/[short-name] [base-ref]` if user selects [A]. If [B], ask the user for the base ref, then run the command with that ref. If [C], do not proceed to workspace writes until the user confirms that the already-selected branch/workspace is the intended hotfix target; a declined confirmation ends with **HOTFIX BLOCKED**.

---

## Phase 4: Investigate and Implement

Focus on the minimal change that resolves the issue. Do NOT refactor, clean up, or add features alongside the hotfix.

Before authorization, perform only read-only root-cause investigation and caller discovery. Then present one complete changeset containing the hotfix record, all code and tests, and the uniquely resolved existing bug file when one exists. Only after that changeset is authorized may any of those files be written. If investigation expands the file set, stop and re-preview the expanded set.

Validate the fix by running targeted tests for the affected system. Check for regressions in adjacent systems.

Update the hotfix record with root cause, fix details, and test results.

---

## Phase 5: Collect Approvals

Use the Codex subagent delegation to request sign-off in parallel:

- `subagent_type: lead-programmer` — Review the fix for correctness and side effects
- `subagent_type: qa-tester` — Run targeted regression tests on the affected system
Both reviews must return APPROVE before proceeding. If either returns CONCERNS or REJECT, output **HOTFIX BLOCKED** and do not deploy. Consult `producer` only when deployment timing requires a product decision and the user authorizes that consultation; it is not a fixed code-correctness gate. Do not invoke a director gate or automatically escalate to `technical-director` inside this time-sensitive workflow.

---

## Phase 5b: QA Re-Entry Gate

After approvals, determine the QA scope required before deploying the hotfix. Spawn `qa-lead` through Codex subagent delegation with:
- The hotfix description and affected system
- The regression test results from Phase 5
- A list of all systems that touch the changed files (search to find callers)

Ask qa-lead: **Is a full smoke check sufficient, or does this fix require a targeted team-qa pass?**

Apply the verdict:
- **Smoke check sufficient** — run `$smoke-check` against the hotfix build. If PASS, proceed to Phase 6.
- **Targeted QA pass required** — run `$team-qa [affected-system]` scoped to the changed system only. If QA returns APPROVED or APPROVED WITH CONDITIONS, proceed to Phase 6.
- **Full QA required** — S1 fixes that touch core systems may require a full `$team-qa sprint`. This delays deployment but prevents a bad patch.

Do not skip this gate. A hotfix that breaks something else is worse than the original bug.

---

## Phase 6: Update Bug Status and Deploy

Update the original bug file if one exists:

```markdown
## Fix Record
**Fixed in**: hotfix/[branch-name] — [commit hash or description]
**Fixed date**: [date]
**Status**: Fixed — Pending Verification
```

Set `**Status**: Fixed — Pending Verification` in the bug file header.

Resolve and show the actual release and development branch targets. After verification, report **ready for merge**, not deployed or complete. Merging is an external side effect and requires explicit user authorization. Merge the hotfix into both targets; if either target is missing, skipped, conflicts, or the command fails, output **HOTFIX BLOCKED** and do not claim that backporting finished.

Only after both merges succeed, output a deployment summary:

```
## Hotfix Ready to Deploy: [short-name]

**Severity**: [S1/S2]
**Root cause**: [one line]
**Fix**: [one line]
**QA gate**: [Smoke check PASS / Team-QA APPROVED]
**Approvals**: lead-programmer ✓ / qa-tester ✓
**Rollback plan**: [from Phase 2 record]

Merge to: release branch AND development branch
Status: merged to both targets; awaiting confirmed deployment
Next: confirm the target build is deployed, then run $bug-report verify [BUG-ID]
```

### Rules
- Hotfixes must be the MINIMUM change to fix the issue — no cleanup, no refactoring
- Every hotfix must have a rollback plan documented before deployment
- Hotfix branches merge to BOTH the release branch AND the development branch
- All hotfixes require a post-incident review within 48 hours
- This workflow invokes no director gate; if scope is no longer suitable for a hotfix, stop with **HOTFIX BLOCKED** and return the decision to the user.

---

## Phase 7: Post-Deploy Verification

Enter this phase only after the user explicitly confirms that the build containing both successful merges has been deployed. Without that confirmation, stop at the ready/awaiting-deployment state: do not verify, close the bug, schedule a review, or output **HOTFIX COMPLETE**.

After confirmed deployment, run `$bug-report verify [BUG-ID]` to confirm the fix resolved the issue in the deployed build.

If VERIFIED FIXED: run `$bug-report close [BUG-ID]` to formally close it, then output **HOTFIX COMPLETE**.
If STILL PRESENT or verification/close fails: output **HOTFIX BLOCKED**; keep or re-open the bug and assess rollback.

Schedule a post-incident review within 48 hours using `$retrospective hotfix`.

Ask the user directly:
- Prompt: "Hotfix complete. What's the next step?"
- Options:
  - `[A] Run $smoke-check to verify the fix`
  - `[B] Run $patch-notes to document this hotfix`
  - `[C] Stop here`
