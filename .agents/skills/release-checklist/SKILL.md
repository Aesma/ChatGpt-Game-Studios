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

Resolve the requested release or milestone from an explicit argument or an existing
active release/milestone reference. This workflow covers internal readiness only:
release-scope stories, bugs, QA/build evidence, and changelog status. Platform
certification, store metadata, distribution, and launch operations belong to the
existing `$launch-checklist` workflow and are not duplicated here.

---

## Phase 2: Load Existing Evidence

Read the current release or milestone artifact and load:

- every story explicitly included in the release scope and its current status;
- open bug reports from the project's existing QA bug location, including severity;
- the latest QA plan/sign-off, smoke or regression evidence, and applicable test results;
- existing build/CI evidence for the release scope;
- the changelog entry for the target release.

Do not infer PASS from an empty checkbox or a missing artifact. Record every missing,
out-of-scope, or unreadable source as **NOT VERIFIED** and cite the expected path.

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

| Check | Evidence | Result |
|-------|----------|--------|
| QA sign-off | [path or NOT VERIFIED] | [PASS/FAIL/NOT VERIFIED] |
| Build/CI | [path or NOT VERIFIED] | [PASS/FAIL/NOT VERIFIED] |

## Changelog

| Target | Evidence | Result |
|--------|----------|--------|
| [version] | [path or NOT VERIFIED] | [PASS/NOT VERIFIED] |

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
