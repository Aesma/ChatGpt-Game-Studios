---
name: propagate-design-change
description: "When a GDD is revised, compares it against an explicit or approved reproducible baseline, traces affected TR registry entries, ADRs, epics, stories, and active sprint work, and guides a bounded resolution without creating a placeholder supersedure."
---

## Invocation and execution

Invoke this workflow as `$propagate-design-change`.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

Arguments:

```text
$propagate-design-change <path/to/changed-gdd.md> --baseline <git-ref-or-approved-baseline> [--baseline-path <old/path.md>]
```

The GDD path is required. `--baseline` may be omitted only when the project has a
last-approved GDD record that provides both an immutable content locator and its
approved SHA-256 hash. A hash without retrievable baseline bytes is not enough.

Delegate substantive work to the `technical-director` Codex subagent role when
it is available. If that role is unavailable, follow the same responsibilities
in the current agent.

# Propagate Design Change

A GDD revision can invalidate requirements, architecture, planning, and work
already in progress. This workflow proves which two GDD versions are compared,
builds the complete downstream reverse graph, and resolves affected artifacts
without leaving an Accepted ADR superseded by a replacement that does not yet
exist.

**Usage:**

```text
$propagate-design-change design/gdd/combat-system.md --baseline main~1
$propagate-design-change design/gdd/combat-system.md --baseline a1b2c3d --baseline-path design/gdd/combat.md
```

---

## 1. Validate Target and Reproducible Baseline

A GDD path is required. If it is missing, stop with:

> "No GDD specified. Usage: `$propagate-design-change design/gdd/[system].md --baseline <git-ref-or-approved-baseline>`"

List recently modified GDDs only as suggestions. Never select one for the user.

Verify that the current GDD exists and read it in full. If it does not exist,
stop with:

> "[path] not found. Check the path and try again."

Resolve the baseline before analyzing downstream impact:

1. Prefer the caller's `--baseline` value.
2. Otherwise, load the last-approved GDD record only if it identifies immutable
   baseline bytes (for example, a commit plus path or an immutable approved
   snapshot) and states the approved SHA-256 hash.
3. Read the baseline GDD bytes and verify their SHA-256 hash against the approved
   record when one is used.
4. Compute the SHA-256 hash of the current workspace GDD bytes. The current file
   may be dirty; the recorded hash, not an assumed commit state, identifies it.
5. Record the resolved baseline ref or approved snapshot locator, baseline path,
   current path, baseline hash, current hash, and diff range.

`HEAD:<path>` is not an implicit baseline. A baseline that is missing,
unresolvable, mutable, hash-mismatched, or unable to provide its content is
**BLOCKED**. Do not guess and do not report NO IMPACT.

### Rename handling

If the current path does not exist at the selected baseline:

- use `--baseline-path` when provided;
- otherwise resolve a unique rename between the selected baseline and current
  workspace by content/history evidence;
- if zero or multiple candidates remain, report the candidates and stop
  **BLOCKED**.

A file absent from a valid baseline is a new GDD, not a revision. Report
`NEW GDD — no previous requirement state to propagate` and stop without
claiming NO IMPACT.

If baseline and current hashes are identical, report `NO CHANGE` and perform no
writes.

---

## 2. Compute a Structured GDD Diff

Compare the exact baseline bytes with the exact current bytes identified in
Step 1. Read both in full. Identify:

- added, removed, and modified requirements;
- changed stable TR-ID references;
- changed rules, formulas, acceptance criteria, constraints, and tuning knobs;
- unchanged sections that provide context.

Produce:

```markdown
## Change Summary: [GDD filename]
Baseline locator: [ref/snapshot]
Baseline path: [path]
Baseline SHA-256: [hash]
Current path: [path]
Current SHA-256: [hash]
Diff range: [baseline locator + path] -> [workspace + path]

Changed requirements:
- [baseline evidence] -> [current evidence]

Unchanged sections:
- [section]
```

Every impact entry must cite a changed requirement or an explicit path-level
change. A conceptual summary never replaces the recorded hashes and locators.

---

## 3. Inventory Every Required Reverse-Graph Layer

Read the following required layers before declaring coverage complete:

| Layer | Required sources | Edges to extract |
|---|---|---|
| GDD | changed GDD and baseline bytes | GDD path/system to stable TR-ID |
| TR registry | `docs/architecture/tr-registry.yaml` | GDD/source to TR-ID; TR-ID status and requirement |
| ADR | every ADR under `docs/architecture/` | TR-ID/GDD to ADR; ADR status; supersedure links |
| Epic | `production/epics/*/EPIC.md` and `production/epics/index.md` when present | TR-ID/ADR/GDD to epic |
| Story | `production/epics/**/story-*.md` | TR-ID/ADR/epic to story; story status |
| Sprint/work | `production/sprint-status.yaml` and current plan files under `production/sprints/` when present | story path/ID to sprint and work status |

Read each discovered artifact in full. Direct GDD-path references and stable
TR-ID references are both edges; do not rely on filename matching alone.

For every layer, record one coverage state:

- `SCANNED` — every discovered source was read and parsed;
- `KNOWN EMPTY` — the expected directory/file inventory was checked and no
  source exists;
- `PARTIAL` — any source could not be listed, read, or parsed, or the required
  TR registry is absent.

A missing TR registry is always PARTIAL because stable requirement coverage
cannot be proven. Other absent artifact collections may be KNOWN EMPTY only
after their expected locations were successfully inventoried.

The scan coverage table must include expected location, discovered file count,
parsed file count, failures, and state. If any required layer is PARTIAL, the
workflow verdict can be only **PARTIAL** (or **BLOCKED** for a baseline failure);
it can never be COMPLETE or NO IMPACT.

---

## 4. Build and Traverse the Reverse Graph

Use stable, exact TR-IDs as the primary join key:

```text
changed GDD
  -> changed/removed/added TR registry entries
  -> ADRs
  -> epics
  -> stories
  -> sprint/current work
```

For each changed GDD requirement:

1. Match it to the baseline and current TR registry entry.
2. Preserve the stable TR-ID when the requirement identity is unchanged.
3. Mark removed, inactive, missing, duplicate, or ambiguous mappings as a
   traceability finding; never invent or renumber an ID.
4. Traverse all exact TR-ID edges through ADR, epic, story, and sprint layers.
5. Also follow direct GDD-path, ADR-ID, epic-path, and story-path edges so that a
   malformed intermediate reference is reported rather than silently dropping a
   downstream artifact.
6. Deduplicate artifacts reached through multiple paths while retaining every
   evidence edge.

For each affected artifact, record:

- artifact type, stable ID when present, and path;
- evidence edge(s) that reached it;
- baseline assumption and current requirement;
- current status;
- impact classification and recommended action.

Artifacts may be classified:

| Classification | Meaning |
|---|---|
| `Still Valid` | The changed requirement does not invalidate this artifact |
| `Needs Review` | Human judgment or traceability repair is required |
| `Likely Superseded` | The current requirement contradicts the artifact's assumption |

A graph with no affected nodes is NO IMPACT only when every required layer is
SCANNED or KNOWN EMPTY and every changed requirement has an unambiguous stable
TR mapping. Otherwise it is PARTIAL.

---

## 5. Elevate Work Already In Progress

Reconcile each affected story's own status with
`production/sprint-status.yaml` and the current sprint plan. If any source marks
the story `In Progress`, `In Review`, or an equivalent active-work state, place
this warning before resolution choices:

> "CAUTION: [story-file] is currently [status] in [source] — a developer may be working on this. Coordinate before updating."

If status sources disagree, report the conflict as Needs Review and treat the
story as active work. Never silently update an active story.

---

## 6. Present the Complete Impact Report

Present the report before asking for any resolution or write:

```markdown
## Design Change Impact Report

GDD: [current path]
Baseline: [locator and baseline path]
Baseline SHA-256: [hash]
Current SHA-256: [hash]
Diff range: [range]

### Scan coverage
| Layer | Expected source | Found | Parsed | State | Failures |
|---|---|---:|---:|---|---|

### Changed requirements
[structured diff with evidence]

### Reverse graph
[TR -> ADR -> epic -> story -> sprint paths]

### Active-work cautions
[elevated warnings]

### Affected artifacts
[Still Valid / Needs Review / Likely Superseded entries, grouped by type]

### Unresolved coverage or traceability
[findings, or None]
```

Use these analysis verdicts:

- **BLOCKED** — target or reproducible baseline could not be established.
- **NO CHANGE** — verified baseline and current hashes are equal.
- **PARTIAL** — a required layer or stable mapping could not be completely
  scanned or proven.
- **NO IMPACT** — a real diff exists, the full graph was scanned, and no
  downstream artifact is affected.
- **COMPLETE** — a real diff exists, full graph coverage is proven, and all
  impacts are reported. This describes analysis completeness, not permission to
  mutate files.

Never turn PARTIAL into NO IMPACT merely because the successfully scanned files
contain no references.

---

## 6b. Director Gate — Technical Impact Review

**Review mode check** — apply before spawning TD-CHANGE-IMPACT:

- `solo` → skip. Note: "TD-CHANGE-IMPACT skipped — Solo mode."
- `lean` → skip. Note: "TD-CHANGE-IMPACT skipped — Lean mode."
- `full` → spawn `technical-director` through Codex subagent delegation using
  gate **TD-CHANGE-IMPACT** (`.codex/docs/director-gates.md`).

Pass the hashes, diff range, scan coverage table, complete reverse graph, active
work cautions, classifications, and recommended actions.

Apply the verdict:

- **APPROVE** → proceed to resolution planning.
- **CONCERNS** → surface the flagged entries and ask whether to revise, accept
  with noted concerns, or discuss further.
- **REJECT** → do not proceed to resolution; revise the analysis.

A director review cannot upgrade BLOCKED or PARTIAL scan coverage.

---

## 7. Resolution Workflow

Resolve only artifacts already listed in the complete report. Ask the user for
the disposition of each Needs Review or Likely Superseded artifact, then present
one complete proposed changeset. Use existing bounded authorization when it
already covers that exact set; otherwise obtain one approval before the first
write. In-progress cautions remain visible in the preview.

General choices are:

- keep as-is with rationale;
- update in place with the exact proposed fields;
- defer as Needs Review;
- replace/supersede through the guarded ADR transition below.

### Guarded ADR supersedure

A Likely Superseded classification is a finding, not an ADR status. While a
replacement is being prepared, keep the current ADR's authoritative status
unchanged and record `Needs Review — replacement required` only in the impact
report.

Do not propose a supersedure write unless the replacement ADR:

1. exists at a concrete path and has a concrete ADR ID;
2. has authoritative `Status: Accepted`;
3. explicitly identifies the old ADR it replaces;
4. covers the affected active TR-IDs without placeholders; and
5. passes the project's normal ADR acceptance requirements.

After those conditions are proven, construct one atomic transition group:

- update the old ADR to `Superseded by ADR-NNNN`;
- update every affected traceability/ADR registry projection to the same concrete
  replacement ID; and
- preserve the replacement ADR as Accepted.

Record pre-write hashes for every transition-group file. Re-read and compare
those hashes immediately before applying. If any file changed, any required
projection is unavailable, or the environment cannot apply the entire group as
one all-or-nothing changeset, perform no transition writes and return BLOCKED
with the conflicting paths. Never write a placeholder replacement reference.

Updates to TR registry, epic, story, or sprint artifacts must likewise be shown
with exact paths and changes in the single bounded preview. A skipped artifact
remains an unresolved impact and prevents a resolution verdict of COMPLETE.

---

## 8. Apply and Verify the Authorized Changeset

When an exact changeset is authorized:

1. Re-read every target and verify its pre-write hash.
2. Apply only the authorized files.
3. For a guarded ADR transition, apply the whole transition group or none of it.
4. Re-read every written file and verify the intended references and statuses.
5. Re-run the reverse-graph analysis against the same baseline/current GDD
   hashes. Do not silently substitute a newer baseline.
6. Report applied, skipped, conflicted, and unresolved artifacts.

If analysis coverage was PARTIAL, writes do not upgrade the verdict. If any
authorized write conflicts or an atomic ADR transition cannot complete, return
BLOCKED or PARTIAL with evidence.

---

## 9. Output Change Impact Document

Include:

- baseline/current locators, paths, hashes, and diff range;
- structured change summary;
- scan coverage table;
- full reverse graph and active-work cautions;
- impact analysis and resolution decisions;
- applied/skipped/conflicted paths;
- remaining owner handoffs.

Add this document to the bounded changeset preview before writing it. If the user
declines the write, keep the on-screen analysis and report **BLOCKED — user
declined report write**. Do not modify authoritative artifacts merely to make
the report appear complete.

---

## 10. Follow-Up Actions

List concrete unresolved work:

- replacement ADR required but not yet Accepted;
- TR registry mapping requiring the registry owner;
- epic/story/sprint changes requiring their owning workflows;
- active-work coordination required before a story changes;
- PARTIAL scan sources that must be restored or parsed.

Recommend architecture review after accepted ADR transitions when broad
traceability changed. A future run must use the same recorded baseline/current
hash pair to verify the same change; do not claim verification by comparing
against an implicit newer version.

---

## Collaborative Protocol

1. Establish and hash the exact target and baseline before impact analysis.
2. Read every required reverse-graph layer and expose scan coverage.
3. Show the complete report and active-work cautions before resolution choices.
4. Preview the entire exact write set once; obtain at most one bounded approval.
5. Keep authoritative ADR status unchanged until a concrete Accepted replacement
   exists and the atomic transition group is ready.
6. Never report COMPLETE or NO IMPACT from a partial scan.
