---
name: release-checklist
description: "Generate an internal release readiness checklist from release-scope stories, open bugs, QA evidence, build evidence, and changelog status."
---

## Invocation and execution

Invoke this workflow as `$release-checklist`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[release or milestone identifier]`. Treat bracketed values as optional unless the workflow says otherwise.


> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$release-checklist`. Do not auto-invoke based on context matching.

## Phase 1: Resolve Internal Release Scope

Resolve the requested release or milestone from an explicit argument or one
validated active release/milestone reference. Prefer the explicit argument. If
multiple active candidates exist, list them and ask the user to select one; do
not choose by filename or modification time.

Read the version from the resolved milestone or an existing release artifact.
If no version is recorded, ask the user for it and do not invent one.

This workflow covers internal readiness only: release-scope stories, bugs,
QA/build evidence, and changelog status. Platform certification, store metadata,
distribution, and launch operations belong to the existing `$launch-checklist`
workflow and are not parameters or branches of this workflow.

---

## Phase 2: Load Existing Evidence

Read the current release or milestone artifact and load:

- every story explicitly included in the release scope and its current status;
- open bug reports from the project's existing QA bug location, including severity;
- the latest QA plan/sign-off, smoke or regression evidence, and applicable test results;
- existing build/CI evidence for the release scope;
- the changelog entry for the target release;
- the most recent existing checklist with a different date, when present.

For each test/build result, capture its recorded result, timestamp, and covered
release scope. If one of those fields is absent, show it as `NOT VERIFIED`; a
file's existence alone is not a pass.

If the project already scans TODO/FIXME/HACK markers, limit that scan to project
source and content files and list their locations separately. Markers do not
inherit bug severity and are never promoted to CRITICAL/HIGH without a bug
artifact that says so.

Treat zero-warning builds, soak duration, target package size, and similar
thresholds as gates only when an existing project configuration or release plan
explicitly requires them. Otherwise label them `not configured` or `manual`.

Do not infer PASS from an empty checkbox or a missing artifact. Record every missing,
out-of-scope, or unreadable source as **NOT VERIFIED** and cite the expected path.

If a previous checklist exists, compare only like-for-like fields and report
resolved, newly introduced, and unchanged items. If none exists, label this run
as the first baseline. The current evidence, not the delta, determines verdict.

---

## Phase 3: Evaluate Blocking State

Assign `PASS`, `FAIL`, or `NOT VERIFIED` to each internal readiness item with a
source path. Apply these verdict rules deterministically:

- Any open CRITICAL/HIGH bug, incomplete release-scope story, or blocking QA
  failure results in **RELEASE BLOCKED**.
- If there are no blocking failures but any remaining evidence is advisory or
  NOT VERIFIED, the result is **CONCERNS**.
- **RELEASE READY** is allowed only when every blocking item has existing
  evidence showing it passed.

---

## Phase 4: Generate the Internal Checklist

Use this structure:

```markdown
# Internal Release Readiness: [Version]

**Generated**: [date]
**Release scope**: [artifact path]

## Release-Scope Stories

| Story | Status | Evidence | Result |
|-------|--------|----------|--------|
| [story] | [status] | [path or NOT VERIFIED] | [PASS/FAIL/NOT VERIFIED] |

## Open Bugs

| Bug | Severity | Status | Result |
|-----|----------|--------|--------|
| [bug] | [severity] | [status] | [PASS/FAIL] |

## QA and Build Evidence

| Check | Result / Timestamp / Scope | Evidence | Assessment |
|-------|----------------------------|----------|------------|
| QA sign-off | [status, time, scope] | [path or NOT VERIFIED] | [PASS/FAIL/NOT VERIFIED] |
| Build/CI | [status, time, scope] | [path or NOT VERIFIED] | [PASS/FAIL/NOT VERIFIED] |

## Changelog

| Target | Evidence | Result |
|--------|----------|--------|
| [version] | [path or NOT VERIFIED] | [PASS/NOT VERIFIED] |

## Delta From Previous Checklist

[Resolved/new/unchanged like-for-like items, or "First checklist baseline"]

## Verdict: [RELEASE READY / CONCERNS / RELEASE BLOCKED]

[Evidence-backed rationale and exact blocking/advisory items.]
```

---

## Phase 5: Save Checklist

Target `production/releases/release-checklist-[date].md`. Before proposing the
write, check whether the exact target already exists. If it exists, read it and
offer a targeted update or stop; never silently overwrite it.

Present the complete checklist and the exact create/update in the complete
changeset preview. Write only after that changeset is authorized.

---

## Phase 6: Handoff

Report the final internal verdict and saved path. For platform certification,
store, distribution, or launch preparation, provide `$launch-checklist` as the
separate existing handoff; do not execute it automatically.
