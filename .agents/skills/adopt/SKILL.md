---
name: adopt
description: "Audit brownfield artifact formats against versioned rules, produce stable hash-bound FORMAT GAP or COMPATIBILITY RISK findings, and write only one separately approved immutable migration report."
---

## Invocation and execution

Invoke this workflow as `$adopt [summary|full|gdds|adrs|stories|infra]`.

No argument means `summary`: inventory artifact classes, declared stage,
available rule sources, prior report IDs, and estimated full-scan size without
opening every artifact. `full` must be explicit. Reject unknown, repeated, or
combined modes with `ERROR`.

The audited GDDs, ADRs, indexes, stories, infrastructure, stage, and configuration
are strictly read-only. The only permitted mutation is one independent migration
report after exact authorization. This workflow never repairs an artifact,
changes `review-mode.txt`, runs a retrofit, or invokes another project skill.

Valid outcomes are:

- `REPORT READY`;
- `PARTIAL`;
- `NO FORMAT GAPS IN SCANNED SCOPE`; or
- `ERROR`.

None of these outcomes proves runtime compatibility.

---

## Phase 0: Freeze target, rules, and write boundary

Resolve one workspace root and one mode. Reject traversal, outside-root paths,
ambiguous roots, and symlink escape.

Record a target snapshot:

- VCS commit/ref and dirty state when available;
- normalized artifact inventory with raw path/hash/byte size/class;
- authoritative declared stage from `production/stage.txt`, if valid;
- current template/rule sources with version and raw hash; and
- current consumer skill/spec versions or hashes when explicitly available.

Do not infer a project stage from source/story/ADR counts. If no versioned
stage-analysis artifact or valid stage declaration exists, report stage
`UNVERIFIED`. This workflow never duplicates `$project-stage-detect` heuristics
or invokes that workflow.

Before scanning, declare the only possible write paths:

- normal artifact: an immutable report at
  `docs/adoption/adoption-audit-[UTC-run-id]-[snapshot8].md`;
- no source, configuration, checkpoint, cache, or auxiliary path.

The UTC run ID must include seconds and the first eight hex characters of the
target snapshot hash. If the exact report path already exists, treat it as a
collision, generate a new run ID, and rebuild the preview. Never overwrite or
append to a prior report.

All analyzers and reviewers are read-only. Choose exactly one report writer only
after the report bytes are complete. It owns the one exact path and nothing else.

---

## Phase 1: Build a versioned rule manifest

For the selected artifact classes, load only current canonical templates,
schemas, or behavioral specs that explicitly define required structure. Record
for every rule:

- stable rule ID and rule version;
- artifact class and exact applicability predicate;
- canonical source path, section, and raw hash;
- objective format check;
- evidence required to call the check present/missing/unknown;
- default migration priority and rationale; and
- owning artifact workflow.

A copied heading/status list inside this skill is not authoritative. If a
canonical source is missing, conflicting, unversioned, or unreadable, mark the
rule `UNVERIFIED` and do not manufacture a gap.

The report may distinguish:

- `FORMAT GAP` — objective current artifact bytes do not satisfy a versioned
  structural rule;
- `COMPATIBILITY RISK` — a format difference may affect a named consumer, but
  runtime behavior has not been fixture-tested;
- `RULE UNVERIFIED` — no trustworthy current rule can support a conclusion; and
- `NOT APPLICABLE` — the rule's explicit applicability predicate is false.

Never state that a skill silently passes, fails, malfunctions, is safe, or
continues to work from headings, field presence, regexes, filenames, or status
strings alone. Actual behavior belongs to a separately executed `$skill-test`
fixture against the current consumer version.

---

## Phase 2: Run a bounded read-only format audit

Use exact mode scopes:

| Mode | Artifact scope |
|---|---|
| summary | inventory and cost estimate only; no per-artifact compliance verdict |
| full | GDD, ADR, systems index, stories, infrastructure, and technical preferences |
| gdds | GDD artifacts only |
| adrs | ADR artifacts only |
| stories | story artifacts only |
| infra | infrastructure/configuration artifacts only |

Process at most 20 artifact files or 250 KiB of UTF-8 text per batch. Paginate
deterministically by normalized path. The full scan may use multiple explicit
batches, but it must record each batch manifest hash and stop at the declared
time/context budget. Never silently sample or omit.

For each artifact, record raw hash before reading, applicable rule IDs, objective
evidence locations, and parse result. Unreadable, concurrently changed,
oversized, parser-unsupported, permission-denied, or omitted files are coverage
gaps. If any selected-scope artifact or rule is unverified, the maximum outcome
is PARTIAL.

An optional technical-director reviewer may inspect the evidence and priorities,
but remains read-only. Reviewer prose cannot replace a canonical rule, artifact
hash, or behavioral fixture.

After scanning, rehash every read artifact. Any changed hash makes its findings
stale. Do not reread under the old snapshot, overwrite the concurrent edit, or
continue to a clean conclusion.

---

## Phase 3: Normalize stable findings

Every finding contains:

- stable ID:
  `ADOPT-[class]-[rule-id]-[normalized-path-fingerprint]`;
- kind: FORMAT GAP, COMPATIBILITY RISK, or RULE UNVERIFIED;
- migration priority: BLOCKING, HIGH, MEDIUM, or LOW;
- rule ID/version/source path/section/hash;
- artifact path, target raw hash, and target snapshot hash;
- exact redacted structural evidence;
- confidence and applicability;
- status `OPEN`;
- unique artifact owner;
- proposed destination workflow;
- testable closure condition; and
- behavior-validation requirement, when compatibility is only a risk.

Priority orders migration work; it is not a claim about runtime behavior. Words
such as BLOCKING or HIGH must be accompanied by the exact versioned rule and
bounded consequence. Do not say the consumer actually fails unless an external
current-version fixture supplies that evidence.

Deduplicate by stable ID. A changed title, ordering, or report run does not create
a new ID when the rule and normalized artifact identity are unchanged.

---

## Phase 4: Build a migration handoff plan

Order OPEN findings by dependency, then migration priority. For each entry list:

- finding ID and evidence hash;
- owning artifact workflow/role;
- exact artifact path;
- bounded desired end state and closure check;
- prerequisites and dependency IDs;
- suggested separate workflow or manual owner action; and
- rough effort labeled as an estimate, not evidence.

This is a handoff manifest, not an implementation plan. It contains no write
authorization for audited artifacts and does not execute any listed command or
skill.

Route by authority:

- GDD gaps → the GDD's authoring/retrofit owner;
- ADR gaps → architecture-decision owner;
- story gaps → story authoring/readiness owner;
- systems index → systems-design/index owner;
- infrastructure/manifest/registry → its declared bootstrap owner;
- review-mode/configuration → an independently authorized configuration owner.

Do not offer to fix a status string, add ADR fields, generate stories, bootstrap
registries, set stage, or write review mode inside this run. Do not claim
existing stories will or will not work; route compatibility validation to an
explicit current-version fixture.

Any downstream handoff failure remains an OPEN dependency in the report. It
cannot mutate this audit outcome or trigger another workflow automatically.

---

## Phase 5: Focused re-audit and convergence

If a prior immutable adoption report is supplied, validate its report hash,
target snapshot, rule-manifest hash, and OPEN finding set.

A focused re-audit checks:

1. prior OPEN finding IDs against their exact closure conditions;
2. artifacts changed since the prior target snapshot;
3. rules changed since the prior rule-manifest snapshot; and
4. regressions introduced by the current diff.

Preserve stable IDs. Mark a prior finding `RESOLUTION UNVERIFIED` unless its
current artifact hash and closure evidence are actually checked. The audit
report itself never edits an external lifecycle record.

Allow one focused verification pass per invocation. If targets change again
during that pass, stop PARTIAL and require a new invocation. Never loop through
report → retrofit → report inside one task.

---

## Phase 6: Preview and write only the immutable report

First return a complete redacted preview containing:

- mode, run ID, target snapshot/hash, declared stage evidence;
- rule-manifest version/hash and consumer versions examined;
- batch/scope coverage and omitted/unverified items;
- every stable finding with kind, priority, evidence, owner, and status;
- migration handoff dependencies;
- prior-run delta when performing a focused re-audit;
- explicit disclaimer:
  `FORMAT AUDIT ONLY — RUNTIME COMPATIBILITY NOT TESTED`; and
- exact report bytes and raw SHA-256.

If the user wants persistence, present one changeset with the exact report path,
create operation, `ABSENT` baseline, single report writer, content hash, and
target/rule snapshot hashes. Ask once. Any path, owner, operation, content, target
snapshot, or rule-manifest change invalidates approval.

Immediately before writing, rehash every audited artifact, rule source, and the
report target. Any mismatch cancels the write. The report writer writes the exact
approved bytes once and verifies the post-write raw hash.

If the user cancels, return the preview and stop with no mutation. Do not ask
about review mode or offer an immediate fix afterward.

---

## Outcome rules

Return `ERROR` when no valid target/rule/scope identity can be established.

Return `PARTIAL` when any selected artifact/rule was omitted, changed,
unreadable, unparsed, permission-denied, or otherwise unverified. Include
confirmed findings separately; never call the project compatible.

Return `NO FORMAT GAPS IN SCANNED SCOPE` only when every selected artifact and
applicable versioned rule was checked and no FORMAT GAP or COMPATIBILITY RISK was
found. Still state that runtime compatibility was not tested.

Return `REPORT READY` when complete selected-scope evidence contains one or more
findings and the preview/report is ready. A report write is optional and does not
change the evidence outcome.

---

## Mutation and authorization boundaries

During ordinary analysis, the allowed write set is empty. After exact report
approval, it contains one create-only immutable report path.

Never modify:

- `design/gdd/systems-index.md` or any GDD;
- any ADR, story, registry, manifest, sprint/status, stage, or engine reference;
- `production/review-mode.txt` or another configuration;
- source, tests, assets, templates, skills, catalogs, or prior adoption reports.

Do not ask for broad directory, glob, retrofit, bulk-fix, or future-file
authorization. External fixes require a separate task with exact paths, unique
owners, operations, baseline hashes, tests, and explicit approval.

---

## Output

Report:

- one outcome;
- exact mode, scope/batch coverage, target and rule-manifest hashes;
- stable finding counts by kind and migration priority;
- omitted/unverified/concurrently changed items;
- immutable report path/hash or `NOT WRITTEN`;
- owner-separated migration handoffs; and
- the runtime-compatibility disclaimer.

Recommend at most one next action: the highest-priority artifact-owner handoff,
a current-version compatibility fixture, or completion of missing audit
coverage. Never execute it in this workflow.

---

## Non-negotiable rules

- Never repair an audited artifact or configuration.
- Never write or change review mode.
- Never infer runtime behavior from static format heuristics.
- Never overwrite an adoption report.
- Never let an analyzer/reviewer write.
- Never expand the approved one-file write boundary.
- Never run another project skill from this workflow.
