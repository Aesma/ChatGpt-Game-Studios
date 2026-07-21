---
name: bug-report
description: "Creates canonical bug reports and records evidence-gated verification and closure transitions without treating static inspection or manual checks as regression proof."
---

# Bug Report

## Invocation and execution

Invoke this workflow as `$bug-report`.

Before the first file change, present the complete proposed changeset, listing every
file and intended modification, and obtain one explicit approval. Existing bounded
task authorization satisfies this gate. After approval, make all changes within that
boundary continuously without asking again file by file. If the scope expands
materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[description] | analyze [path-to-file]`. Treat bracketed values as
optional unless the workflow says otherwise.

## Non-negotiable canonical contract

1. The only canonical bug registry is `production/qa/bugs/*.md`. A record's path is
   `production/qa/bugs/<BUG-ID>.md`, where the filename ID exactly matches the `ID`
   field. Do not read or write `production/bugs/`, a combined bugs file, a triage
   report, or any other artifact as a bug record.
2. Canonical records use `Schema Version: 1` and one stable ID matching
   `BUG-[0-9]{4,}`. Route verify and close operations only through that stable ID.
   If the expected record is absent, the filename and field disagree, or more than
   one canonical file contains the ID, stop without a business verdict or mutation
   and report the conflicting paths.
3. Canonical severity values are exactly `S1-Critical`, `S2-Major`, `S3-Minor`,
   and `S4-Trivial`. Do not silently convert legacy
   `CRITICAL/HIGH/MEDIUM/LOW` values. Priority and scheduling are separate owner
   decisions and are never inferred from severity by this workflow.
4. Canonical lifecycle statuses are exactly `Open`,
   `Fixed Pending Verification`, `Verified Fixed`, and `Closed`. Update the single
   top-level Status field and append the matching transition-history event in one
   proposed mutation.
5. Source search, diff inspection, or the presence of a test can establish only
   `FIX PRESENT / RUNTIME UNVERIFIED`. It can never establish
   `VERIFIED FIXED`.
6. `VERIFIED FIXED` requires both a target-build reproduction receipt and a passing,
   failure-sensitive automated regression-test receipt bound to the fix revision.
   Manual runtime observation may supply the reproduction receipt, but manual
   evidence never replaces the automated regression-test receipt.
7. `CLOSED` requires the current `Verified Fixed` transition and the same valid
   automated regression evidence. `Manual verification` is not an allowed value for
   `Regression test`. The repository test policy grants no regression-test waiver.
8. This workflow does not assign priority, schedule work, accept risk, or edit sprint,
   triage, hotfix, release, or test-plan records.

## Canonical state machine and owners

| From | To | Decision owner | Required evidence | This workflow's role |
|---|---|---|---|---|
| `Open` | `Fixed Pending Verification` | fix implementer / owning development workflow | fix commit or PR, affected build, and regression test ID/path | Consume the recorded transition; Verify Mode does not create it |
| `Fixed Pending Verification` | `Verified Fixed` | QA verifier | passing target-build reproduction receipt and passing automated regression receipt for the fix revision | Verify Mode may record after authorization |
| `Fixed Pending Verification` | `Open` | QA verifier | failing target-build reproduction or regression receipt | Verify Mode may record after authorization |
| `Verified Fixed` | `Closed` | authorized QA closure owner | current verification transition plus its passing automated regression receipt | Close Mode may record after authorization |

All other transitions are illegal. In particular, reject `Open → Verified Fixed`,
`Open → Closed`, `Fixed Pending Verification → Closed`, and every transition out of
`Closed`. The workflow records an owner's decision; it does not grant that authority.
Every accepted transition appends an immutable history entry containing old status,
new status, owner identity and role, UTC timestamp, reason, source receipt hashes,
and the bug-record preimage SHA-256.

## Phase 1: Parse arguments

Determine the mode from the argument:

- No keyword → **Description Mode**: generate a structured canonical bug report from
  the provided description.
- `analyze [path]` → **Analyze Mode**: read the target file(s) and identify potential
  bugs.
- `verify [BUG-ID]` → **Verify Mode**: evaluate evidence for a reported fix.
- `close [BUG-ID]` → **Close Mode**: record an authorized closure after all gates pass.

If no argument is provided, ask the user for a bug description before proceeding.

For Verify and Close, normalize no user-supplied path. Validate the ID, resolve only
`production/qa/bugs/<BUG-ID>.md`, confirm its raw-byte SHA-256, parse
`Schema Version`, `ID`, `Severity`, and `Status`, and reject ambiguity before doing
business work.

## Phase 2A: Description Mode

1. Parse the description for what broke, when, how to reproduce it, expected
   behavior, actual behavior, environment, and impact.
2. Search the codebase by file name and contents to add clearly labeled inferred
   context. Source search is not runtime evidence.
3. Draft the canonical report below. Allocate a stable project bug ID and use the
   same ID in the filename and body.
4. Set initial status only to `Open`. Description Mode cannot record a fixed,
   verified, or closed status.

```markdown
# Bug Report

**Schema Version**: 1
**ID**: BUG-[NNNN]
**Title**: [Concise, descriptive title]
**Severity**: [S1-Critical / S2-Major / S3-Minor / S4-Trivial]
**Priority**: [Observed value, or Unassigned]
**Status**: Open
**Reported**: [UTC timestamp]
**Reporter**: [Name]

## Classification
- **Category**: [Gameplay / UI / Audio / Visual / Performance / Crash / Network]
- **System**: [Which game system is affected]
- **Frequency**: [Always / Often (>50%) / Sometimes (10-50%) / Rare (<10%)]
- **Regression**: [Yes / No / Unknown]

## Environment
- **Build**: [Version or commit hash]
- **Platform**: [OS and relevant hardware]
- **Scene/Level**: [Where in the game]
- **Game State**: [Relevant state]

## Reproduction Steps
**Repro Case ID**: [Stable case ID]
**Preconditions**: [Required state before starting]

1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

**Expected Result**: [What should happen]
**Actual Result**: [What actually happens]

## Technical Context
- **Likely affected files**: [List of files based on codebase search]
- **Related systems**: [What other systems might be involved]
- **Possible root cause**: [If identifiable from the description]

## Evidence
- **Logs**: [Path and SHA-256, if available]
- **Visual**: [Path and SHA-256, if available]

## Fix Reference
- **Fix commit / PR**: [Not recorded until a fix owner supplies it]
- **Fix build**: [Not recorded until a fix owner supplies it]
- **Regression test ID/path**: [Not recorded until a fix owner supplies it]

## Verification Evidence
Not yet verified.

## Transition History
- [Reported timestamp] — record created with Status `Open` by [reporter]

## Related Issues
- [Links to related bugs or design documents]

## Notes
[Any additional context or observations]
```

The proposed destination is exactly
`production/qa/bugs/<BUG-ID>.md`. Never save the canonical report anywhere else.

## Phase 2B: Analyze Mode

1. Read only the explicitly specified project file(s).
2. Identify potential null references, off-by-one errors, race conditions, unhandled
   edge cases, resource leaks, or incorrect state transitions.
3. For each potential bug, draft the canonical report from Phase 2A with the trigger
   scenario and recommended fix recorded as hypotheses.
4. Source analysis alone does not reproduce a bug and does not create verification
   evidence. New records begin at `Open` and use the canonical path, schema, and
   severity enum.

## Phase 2C: Verify Mode

Load the one canonical record by stable ID and require current status
`Fixed Pending Verification`. If the status is `Open`, stop because no fix-owner
transition is ready to verify. If it is `Verified Fixed`, report the existing
transition without adding a second one. If it is `Closed`, stop; closed records are
immutable.

### Step 1: Static fix inspection

Inspect the referenced fix revision and related code path. Record changed paths and
source hashes. Static inspection can return only:

- `FIX PRESENT / RUNTIME UNVERIFIED`; or
- `FIX NOT FOUND / RUNTIME UNVERIFIED`.

If this is all the available evidence, return `CANNOT VERIFY`, propose no status
change, and state exactly which runtime or regression receipt is missing.

### Step 2: Target-build reproduction receipt

Re-run the record's exact `Repro Case ID` and numbered reproduction steps on the
target fix build. A receipt is valid only when it records all of:

- bug ID and repro case ID;
- build ID and fix commit SHA;
- platform and relevant configuration;
- runner identity, or manual observer identity and role;
- UTC start/end timestamps;
- each executed step, observed actual result, and expected result;
- outcome `PASS`, `FAIL`, or `RUNNER_ERROR`;
- immutable evidence path(s) and raw-byte SHA-256 hashes.

The build ID, fix commit, platform, and repro case must match the canonical record's
fix reference. Missing, stale, wrong-build, wrong-platform, or unreadable evidence
does not verify the fix.

### Step 3: Automated regression-test receipt

Require a regression test that is specifically failure-sensitive to the original
defect. A valid receipt records:

- regression test ID and repository-relative test path;
- fix commit SHA and target build/configuration;
- exact test invocation and completion timestamp;
- exit code and `PASS` result;
- assertion or fixture explaining why the test would fail on the original defect;
- immutable log path and raw-byte SHA-256.

The test ID/path must match the canonical Fix Reference, and the receipt must be from
the fix commit being verified. A related suite that does not exercise the original
failure is insufficient. A manual playtest, code review, screenshot, or prose claim
cannot serve as this receipt.

### Step 4: Verdict and transition

- When target-build reproduction is `PASS` and the automated regression receipt is
  `PASS`, return `VERIFIED FIXED` and propose one atomic mutation:
  set `Status: Verified Fixed`, append both receipts under Verification Evidence,
  and append the `Fixed Pending Verification → Verified Fixed` history event.
- When target-build reproduction or the failure-sensitive regression is `FAIL`,
  return `STILL PRESENT` and propose one atomic mutation: set `Status: Open`, retain
  the failure evidence, and append the
  `Fixed Pending Verification → Open` history event.
- When either required receipt is missing, stale, mismatched, unreadable, partial, or
  `RUNNER_ERROR`, return `CANNOT VERIFY` and make no status mutation.
- A static-only result always remains `FIX PRESENT / RUNTIME UNVERIFIED` (or
  `FIX NOT FOUND / RUNTIME UNVERIFIED`) and `CANNOT VERIFY`.

Do not write the proposed transition before the complete changeset is authorized.

## Phase 2D: Close Mode

Load the one canonical record by stable ID. Require current status
`Verified Fixed` and a valid `Fixed Pending Verification → Verified Fixed` history
event.

Revalidate that the transition references:

1. a passing target-build reproduction receipt matching the bug, repro case, fix
   build, fix commit, and platform; and
2. a passing, failure-sensitive automated regression receipt matching the regression
   test ID/path and fix commit.

The receipt files must still be readable and their raw-byte SHA-256 values must match.
If either receipt is missing, stale, mismatched, non-passing, or manual-only, stop
without mutation:

`Bug [ID] cannot be closed: current target-build verification and a passing automated
regression-test receipt are required.`

Require the authorized QA closure owner's identity and authority reference. Then
propose one atomic edit: set the top-level status to `Closed` and append:

```markdown
## Closure Record
**Closed**: [UTC timestamp]
**Resolution**: Fixed — [one-line description]
**Fix commit / PR**: [verified fix reference]
**Build verification receipt**: [path and SHA-256]
**Verified by**: [QA verifier identity]
**Closed by**: [authorized QA closure owner]
**Closure authority**: [role or decision reference]
**Regression test ID/path**: [automated test ID and path]
**Regression receipt**: [path and SHA-256]
**Status**: Closed
```

Append the `Verified Fixed → Closed` transition-history event in that same edit.
Manual verification may be supporting evidence but never replaces either required
receipt.

After closing, do not edit triage output. Note only that `$bug-triage` derives a
fresh read-only snapshot from canonical records.

## Phase 3: Present and save

Present the completed report or transition proposal and its exact canonical path.
List every proposed file change and obtain the one changeset authorization required
above unless existing bounded authorization already covers it.

For a new report, write only `production/qa/bugs/<BUG-ID>.md`. For Verify or Close,
write only the resolved canonical bug record, and only after every evidence and owner
gate passes. Preserve the preimage hash in the transition history.

If authorized and all gates pass, verdict: `COMPLETE`. If not authorized, verdict:
`BLOCKED — changeset not authorized`. Evidence failure uses the Verify/Close verdict,
not `COMPLETE`.

## Phase 4: Next steps

- After filing, suggest `$bug-triage` for a read-only priority/schedule snapshot.
- After a development owner records `Fixed Pending Verification` with a fix reference
  and regression test, suggest `$bug-report verify [BUG-ID]`.
- After `VERIFIED FIXED`, suggest `$bug-report close [BUG-ID]`.
- For an S1/S2 emergency candidate, `$hotfix plan <BUG-ID>` may be suggested but never invoked
  automatically.
- Never claim that triage, sprint, risk, release, or test records were changed by this
  workflow.
