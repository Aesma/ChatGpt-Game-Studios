---
name: bug-report
description: "Creates a structured bug report from a description, or analyzes code to identify potential bugs. Ensures every bug report has full reproduction steps, severity assessment, and context."
---

## Invocation and execution

Invoke this workflow as `$bug-report`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[description] | analyze [project-path] | verify [BUG-NNNN] | close [BUG-NNNN]`.
Treat bracketed values as optional unless the workflow says otherwise. Reject an
unknown mode; verify/close require exactly one syntactically valid BUG ID.


## Phase 1: Parse Arguments

Determine the mode from the argument:

- No keyword → **Description Mode**: generate a structured bug report from the provided description
- `analyze [path]` → **Analyze Mode**: read the target file(s) and identify potential bugs
- `verify [BUG-ID]` → **Verify Mode**: confirm a reported fix actually resolved the bug
- `close [BUG-ID]` → **Close Mode**: mark a verified bug as closed with resolution record

If no argument is provided, ask the user for a bug description before proceeding.

---

## Phase 2A: Description Mode

1. **Parse the description** for key information: what broke, when, how to
reproduce it, expected/actual result, Reporter, Build, Platform, Frequency, and
Environment. Ask only for required facts that are missing. If the user does not
know one, record `Unknown`; never infer a reporter, build, platform, or repro step.

2. **Search the codebase** by file name and contents to add context (affected system, likely files).

3. **Check duplicates before drafting**: scan `production/qa/bugs/` for similar
symptoms in the same system or title. Show likely matches and let the user add a
related note to one existing report or continue with a new report. Include any
selected existing-file edit in the same complete changeset; never silently file
a duplicate.

4. **Allocate an ID provisionally** by scanning existing BUG-NNNN filenames and
choosing the next sequence. Re-scan immediately before the first write; if the
ID is now occupied, update the filename, report ID, and preview rather than
overwriting.

5. **Draft the bug report**:

```markdown
# Bug Report

## Summary
**Title**: [Concise, descriptive title]
**ID**: BUG-[NNNN]
**Severity**: [S1-Critical / S2-Major / S3-Minor / S4-Trivial]
**Priority**: [P1-Immediate / P2-Next Sprint / P3-Backlog / P4-Wishlist]
**Status**: Open
**Reported**: [Date]
**Reporter**: [Name]

## Classification
- **Category**: [Gameplay / UI / Audio / Visual / Performance / Crash / Network]
- **System**: [Which game system is affected]
- **Frequency**: [Always / Often (>50%) / Sometimes (10-50%) / Rare (<10%)]
- **Regression**: [Yes/No/Unknown -- was this working before?]

## Environment
- **Build**: [Version or commit hash]
- **Platform**: [OS, hardware if relevant]
- **Scene/Level**: [Where in the game]
- **Game State**: [Relevant state -- inventory, quest progress, etc.]

## Reproduction Steps
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
- **Logs**: [Relevant log output if available]
- **Visual**: [Description of visual evidence]

## Related Issues
- [Links to related bugs or design documents]

## Notes
[Any additional context or observations]
```

---

## Phase 2B: Analyze Mode

1. **Validate and read the target**: accept one existing project-local text source
file or a bounded project-local directory. Reject missing, external, binary,
generated, ambiguous multi-target, or unreadable inputs before analysis.

2. **Identify potential bugs**: null references, off-by-one errors, race conditions, unhandled edge cases, resource leaks, incorrect state transitions. Every finding
must cite file/line evidence, explain a reachable trigger, and state uncertainty.

3. **Select filings with the user**: findings whose reachability or reproduction
is not supported remain conversational `Potential` items. Show the evidence and
ask which items should be filed. Only confirmed selections become reports; do not
automatically turn every static suspicion into a full reproducible bug.

---

## Phase 2C: Verify Mode

Resolve exactly one file matching `production/qa/bugs/[BUG-ID]-*.md` and read it. Extract the reproduction steps and expected result.

1. Treat code search only as supporting evidence; it never counts as reproducing
   or clearing a runtime bug.
2. If an executable automated reproduction or related test is available, run the
   documented reproduction and compare the observed result with Expected Result.
3. Run any related regression tests and record the actual command/result. If the
   reproduction cannot be executed, required tests cannot run, or results are
   inconclusive, the verdict must be CANNOT VERIFY.

Produce a verification verdict:

- **VERIFIED FIXED** — an actual executable reproduction no longer produces the bug and related tests pass
- **STILL PRESENT** — bug reproduces as described; fix did not resolve the issue
- **CANNOT VERIFY** — automated checks inconclusive; manual playtest required

Prepare the exact existing-file edit and include it in the complete changeset preview:
- VERIFIED FIXED: set the top-level Status to `Verified Fixed` and append the
  actual verification command/results.
- STILL PRESENT: keep or set top-level Status to `Open` and append the observed failure.
- CANNOT VERIFY: append the limitation only; do not change top-level Status.

Write only after the single authorization. If STILL PRESENT, suggest re-running
`$hotfix [BUG-ID]`. Then end the Verify run; do not enter Phase 3.

---

## Phase 2D: Close Mode

Resolve exactly one file matching `production/qa/bugs/[BUG-ID]-*.md` and read it. Confirm Status is `Verified Fixed` before closing. If status is anything else, stop: "Bug [ID] must be Verified Fixed before it can be closed. Run `$bug-report verify [BUG-ID]` first."

Append a closure record to the bug file:

```markdown
## Closure Record
**Closed**: [date]
**Resolution**: Fixed — [one-line description of what was changed]
**Fix commit / PR**: [if known]
**Verified by**: qa-tester
**Closed by**: [user]
**Regression test**: [test file path, or "Manual verification"]
**Status**: Closed
```

Update the top-level `**Status**: Open` field to `**Status**: Closed`.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

After closing, check `production/qa/bug-triage-*.md` — if the bug appears in an open triage report, note: "Bug [ID] is referenced in the triage report. Run `$bug-triage` to refresh the open bug count." Then end the Close run; do not enter Phase 3.

---

## Phase 3: Save Report (Description and Analyze modes only)

Verify and Close modes have already ended and must never enter this phase.

Present the completed bug report(s) to the user and show the exact target path:
`production/qa/bugs/BUG-NNNN-[slug].md`. The canonical literals are exactly
S1-Critical/S2-Major/S3-Minor/S4-Trivial and
P1-Immediate/P2-Next Sprint/P3-Backlog/P4-Wishlist; do not introduce another
severity or priority vocabulary.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Once the complete changeset is authorized, write the file, creating the directory if needed. Verdict: **COMPLETE** — bug report filed.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 4: Next Steps

After saving, suggest based on mode:

**After filing (Description/Analyze mode):**
- Run `$bug-triage` to prioritize alongside existing open bugs
- If S1 or S2: run `$hotfix [BUG-ID]` for emergency fix workflow

**After fixing the bug (developer confirms fix is in):**
- Run `$bug-report verify [BUG-ID]` — confirm the fix actually works before closing
- Never mark a bug closed without verification — a fix that doesn't verify is still Open

**After verify returns VERIFIED FIXED:**
- Run `$bug-report close [BUG-ID]` — write the closure record and update status
- Run `$bug-triage` to refresh the open bug count and remove it from the active list
