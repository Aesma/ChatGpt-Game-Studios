---
name: day-one-patch
description: "Prepare a day-one patch for a game launch. Scopes, prioritises, implements, and QA-gates a focused patch addressing known issues discovered after gold master but before or immediately after public launch. Treats the patch as a mini-sprint with its own QA gate and rollback plan."
---

## Invocation and execution

Invoke this workflow as `$day-one-patch`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[scope: known-bugs | cert-feedback | all]`. Treat bracketed values as optional unless the workflow says otherwise.


# Day-One Patch

Every shipped game has a day-one patch. Planning it before launch day prevents
chaos. This skill scopes the patch to only what is safe and necessary, gates it
through a lightweight QA pass, and ensures a rollback plan exists before anything
ships. It is a mini-sprint — not a hotfix, not a full sprint.

**When to run:**
- After the gold master build is locked (cert approved or launch candidate tagged)
- When known bugs exist that are too risky to address in the gold master
- When cert feedback requires minor fixes post-submission
- When a pre-launch playtest surfaces must-fix issues after the release gate passed

**Day-one patch scope rules:**
- Only P1/P2 bugs that are SAFE to fix quickly
- No new features — this is fix-only
- No refactoring — minimum viable change
- Any fix that requires more than 4 hours of dev time belongs in patch 1.1, not day-one

**Output:** `production/releases/day-one-patch-[version].md`

---

## Phase 1: Load Release Context

Read:
- `production/stage.txt` — confirm project is in Release or Polish
- Existing release/launch checklist and QA sign-off artifacts that cover the
  current build, when present; do not require a `production/gate-checks/`
  report because the gate workflow does not create one
- `production/qa/bugs/*.md` — load all bugs with Status: Open or Fixed — Pending Verification
- `production/sprints/` most recent — understand what shipped
- `production/security/security-audit-*.md` most recent — check for any open security items

If `production/stage.txt` is missing, invalid, or not `Release`/`Polish`,
display the current evidence and stop immediately. Do not spawn any role, write
any file, or emit "patch complete".

---

## Phase 2: Scope the Patch

### Step 2a — Classify open bugs for patch inclusion

For each open bug, evaluate:

| Criterion | Include in day-one? |
|-----------|-------------------|
| S1 or S2 severity | Yes — must include if safe to fix |
| P1 priority | Yes |
| Fix estimated < 4 hours | Yes |
| Fix requires architecture change | No — defer to 1.1 |
| Fix introduces new code paths | No — too risky |
| Fix is data/config only (no code change) | Yes — very low risk |
| Cert feedback requirement | Yes — required for platform approval |
| S3/S4 severity | Only if trivial config fix; otherwise defer |

### Step 2b — Exclude emergency issues

If any candidate is P0/CRITICAL, exclude it from ordinary day-one scope and stop
execution with an explicit handoff to the existing `$hotfix` workflow. Do not
treat it as a four-hour patch item.

### Step 2c — Present patch scope to user

Ask the user directly:
- Prompt: "Based on open bugs and cert feedback, here is the proposed day-one patch scope. Does this look right?"
- Show: table of included bugs (ID, severity, description, estimated effort)
- Show: table of deferred bugs (ID, severity, reason deferred)
- Options: `[A] Approve this scope` / `[B] Adjust — I want to add or remove items` / `[C] No day-one patch needed`

If [C]: output "No day-one patch required. Proceed to `$launch-checklist`." Stop.

### Step 2d — Check total scope

Sum estimated effort. If total exceeds 1 day of work:
> "⚠️ Patch scope is [N hours] — this exceeds a safe day-one window. Consider deferring lower-priority items to patch 1.1. A bloated day-one patch introduces more risk than it removes."

Ask the user directly to confirm proceeding or reduce scope.

---

## Phase 3: Read-Only Fix Location, Rollback Draft, and Authorization

Before any code is written:

1. Have lead-programmer inspect each approved bug read-only and identify the
   exact candidate source/config files, targeted test files, and intended minimal
   operation.
2. Have release-manager draft the rollback procedure read-only, including
   platform constraints, owner, and player communication.
3. Present one complete changeset containing the rollback-plan file, every
   identified source/config and test file, and the final day-one patch record.
   Obtain one authorization before any of those files is written.

If implementation later discovers an unlisted file, pause and expand the
changeset before touching it. Do not write the rollback plan as a separate early
authorization.

---

## Phase 4: Implement Fixes

For each bug in the approved and authorized scope, run the focused
implementation loop using only the files owned in Phase 3:

1. Spawn `lead-programmer` through Codex subagent delegation with:
   - The bug report (exact reproduction steps and root cause if known)
   - The constraint: minimum viable fix only, no cleanup
   - The affected files (from bug report Technical Context section)

2. The lead-programmer implements and runs targeted tests.

3. Spawn `qa-tester` through Codex subagent delegation to verify: does the bug reproduce after the fix?

For config/data-only fixes: make the change directly (no programmer agent needed). Confirm the value changed and re-run any relevant smoke test.

---

## Phase 5: Patch QA Gate

This is a lightweight QA pass — not a full `$team-qa`. The patch is already QA-approved from the release gate; we are only re-verifying the changed areas.

Spawn `qa-lead` through Codex subagent delegation with:
- List of all changed files
- List of bugs fixed (with verification status from Phase 4)
- The smoke check scope for the affected systems

Ask qa-lead to determine: **Is a targeted smoke check sufficient, or do any fixes touch systems that require a broader regression?**

Run the required QA scope:
- **Targeted smoke check** — run `$smoke-check quick` and pass the affected systems as hand-off context, not as a positional mode
- **Broader regression** — run targeted tests in `tests/unit/` and `tests/integration/` for affected systems

QA verdict must be PASS or PASS WITH WARNINGS before proceeding. On FAIL, stop
and list the failing fix plus every file it changed. Ask the user whether to fix
it within the already authorized boundary or revert that fix's specific edits.
Then rerun the existing targeted tests against the remaining combination. Until
the failed change is restored or fixed and verification passes, do not enter
Phase 6 and do not produce a PASS patch record.

---

## Phase 6: Generate Patch Record

```markdown
# Day-One Patch: [Game Name] v[version]

**Date prepared**: [date]
**Target release**: [launch date or "day of launch"]
**Base build**: [gold master tag or commit]
**Patch build**: [patch tag or commit]

---

## Patch Notes (Internal)

### Bugs Fixed
| BUG-ID | Severity | Description | Fix summary |
|--------|----------|-------------|-------------|
| BUG-NNN | S[1-4] | [description] | [one-line fix] |

### Deferred to 1.1
| BUG-ID | Severity | Description | Reason deferred |
|--------|----------|-------------|-----------------|
| BUG-NNN | S[1-4] | [description] | [reason] |

---

## QA Sign-Off

**QA scope**: [Targeted smoke / Broader regression]
**Verdict**: [PASS / PASS WITH WARNINGS]
**QA lead**: qa-lead agent
**Date**: [date]
**Warnings (if any)**: [list or "None"]

---

## Rollback Plan

See: `production/releases/rollback-plan-[version].md`

**Trigger condition**: If [N] or more S1 bugs are reported within [X] hours of launch, execute rollback.
**Rollback owner**: [user / producer]

---

## Approvals Required Before Deploy

- [ ] lead-programmer: all fixes reviewed
- [ ] qa-lead: QA gate PASS confirmed
- [ ] producer: deployment timing approved
- [ ] release-manager: platform submission confirmed

---

## Player-Facing Patch Notes

[Draft for community-manager to review before publishing]

[list player-facing changes in plain language]
```

Write this record only as the final operation already listed and authorized in
Phase 3. Do not request a second changeset authorization.

---

## Phase 7: Next Steps

After the patch record is written:

1. Run `$patch-notes` to generate the player-facing version of the patch notes
2. Run `$bug-report verify [BUG-ID]` for each fixed bug after the patch is live
3. Run `$bug-report close [BUG-ID]` for each verified fix
4. Schedule a post-launch review 48–72 hours after launch using `$retrospective launch`

**If any S1 bugs remain open after the patch:**
> "⚠️ S1 bugs remain open and were not patched. These are accepted risks. Document them in the rollback plan trigger conditions — if they occur at scale, rollback may be preferable to a follow-up patch."

Ask the user directly:
- Prompt: "Day-one patch complete. What's next?"
- Options:
  - `[A] Run $patch-notes — generate player-facing patch notes`
  - `[B] Run $bug-report to log any issues found post-deploy`
  - `[C] Stop here`

---

## Collaborative Protocol

- **Scope discipline is everything** — resist scope creep; every addition increases risk
- **Rollback plan first, always** — a patch without a rollback plan is irresponsible
- **Deferred is not forgotten** — every deferred bug gets a 1.1 ticket automatically
- **Player communication is part of the patch** — `$patch-notes` is a required output, not optional
