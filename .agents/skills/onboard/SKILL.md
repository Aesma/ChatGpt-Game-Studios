---
name: onboard
description: "Produce a bounded, visibility-filtered, source-cited repository orientation in conversation, using applicable nested instructions and optional canonical stage/help evidence without reading sensitive sources or modifying files."
---

## Invocation and execution

Invoke as:

```text
$onboard [role-id|area-id] [--visibility public|internal]
  [--analysis <stage-packet-path> --expect-analysis <sha256:...>]
  [--recommendation <help-envelope-path> --expect-recommendation <sha256:...>]
```

The role or area is optional and defaults to `GENERAL`. Each path/hash pair is
inseparable. Instead of either pair, exactly one corresponding complete packet
may be supplied explicitly in the current invocation or conversation. Reject
unknown or duplicate flags, missing values, malformed hashes, directories,
traversal, outside-root paths, symlink escape, mixed path/inline forms, or
multiple candidates with `ONBOARDING ERROR` before project context is read.

Visibility defaults to the least-privileged onboarding scope configured by
repository policy; without a policy it is `public`. A requested visibility may
narrow access but never expand the caller's authorized scope.

This workflow is strictly read-only. It returns context in conversation only and
must not create, edit, overwrite, delete, rename, stage, commit, publish, save,
delegate, invoke a gate, or invoke another project skill. It never requests
changeset authorization, invents an output path, offers a save branch, or runs a
recommended action.

`--save` is unsupported. A persistence request requires a separate document task
with an explicit path and collision policy; stop without choosing or inspecting
candidate output paths.

---

## Phase 0: Establish repository authority or fail

Resolve exactly one canonical workspace root, capture one UTC `snapshot_at`, and
establish a repository identity before reading project context.

Read repository-root `AGENTS.md` first. It is required. If it is missing,
unreadable, malformed, outside visibility, or cannot be bound to the canonical
root, return `ONBOARDING ERROR`. Do not read secondary configuration, role,
stage, sprint, source, Git, or area files to construct a partial narrative and do
not substitute a parent, nested, cached, or generated instruction file.

An error envelope may identify only the root instruction class, source state,
generic diagnostic code, and one non-mutating remediation question. It must not
invent project summary, technology, role, stage, current work, hierarchy, or
recommended files.

Required root failure codes are `ROOT_INSTRUCTIONS_MISSING`,
`ROOT_INSTRUCTIONS_UNREADABLE`, `ROOT_INSTRUCTIONS_INVALID`,
`ROOT_INSTRUCTIONS_OUT_OF_SCOPE`, and `REPOSITORY_IDENTITY_UNVERIFIED`.

---

## Phase 1: Resolve repository scope, visibility, and fixed budgets

Normalize a supplied role or area only against stable repository IDs:

- an exact role ID must resolve to one repository role definition;
- an exact area ID must resolve to one authoritative project-area index;
- a free-text alias is valid only when an authoritative alias map resolves it to
  exactly one stable ID;
- ambiguous or nonexistent values return `ONBOARDING ERROR` with safe candidate
  IDs only; and
- ambiguity never broadens visibility or triggers role-specific reads.

Repository role definitions describe workflow responsibilities and collaboration
interfaces only. They do not establish a person's job title, manager, reporting
line, employment status, team membership, access entitlement, decision
authority, performance expectations, or who assigns work. Unless an explicit,
visibility-allowed organizational mapping directly states one of those facts,
report it as `UNKNOWN`. Never derive human hierarchy from agent prompts, role
names, reviewer labels, CODEOWNERS-like routing, or workflow ownership.

Apply visibility and deny policy before candidate enumeration, stat, open, hash,
summary, or recommendation. Then resolve a versioned repository onboarding budget
if configured. Otherwise use all of these fixed defaults:

- at most 256 enumerated directory entries;
- at most 64 opened content files;
- at most 256 KiB raw bytes per content file;
- at most 1 MiB total opened content bytes;
- at most depth 6 below approved roots; and
- at most 20 commits inside one explicit configured Git range.

Budget counters include instruction files and supplied external evidence packets
after root AGENTS.md. Check limits before each enumeration/read. Never partially
read a file, silently truncate a source set, replace omitted bytes with a model
summary, or increase a limit because the repository is large.

Record configured/default limits, consumption, deterministic selection order,
excluded roots, `OMITTED_BUDGET` sources or topics, and the limit reason. Use
authoritative index order; break ties by normalized repository-relative path.
When budget omission affects requested or role-relevant coverage, status is
`ONBOARDING PARTIAL`.

---

## Phase 2: Deny sensitive content before access

Always deny these source classes before stat/open/hash/content ingestion:

- `.env` files and local environment variants;
- credentials, secrets, tokens, cookies, connection strings, certificates,
  private keys, key stores, recovery codes, and vault exports;
- personnel, payroll, salary, performance, disciplinary, applicant, medical,
  demographic, private-contact, or access-review records;
- private correspondence, direct messages, mailbox exports, and user-private notes;
- raw vulnerability, exploit, incident-forensics, anti-cheat bypass, malware,
  abuse, embargoed, and unreleased security reports;
- any path denied by repository instructions, active visibility policy, or the
  environment permission profile.

Use deny patterns and authoritative classifications without opening a candidate.
If an index, filename, supplied packet, or recommendation appears sensitive,
record only a generic redaction code such as `OMITTED_SENSITIVE` or
`OMITTED_VISIBILITY`. Do not reveal its path, basename, extension, existence,
size, timestamps, owner, hash, metadata, secret-shaped value, exploit detail, or
reason specific enough to identify the item.

Never recommend a denied source for reading. Redaction after ingestion is not
compliance. A user request for wider onboarding detail cannot override repository
or environment denials.

---

## Phase 3: Build the bounded authoritative source plan

After root instructions, build a deterministic source plan from visibility-
allowed authoritative indexes and manifests before opening area content. Prefer:

1. exact project/technology references named by root AGENTS.md;
2. the selected repository role definition or area index;
3. architecture, design, test, production, and asset indexes;
4. an active-work manifest or sprint pointer; and
5. optional explicitly supplied canonical stage/help evidence.

Do not recursively full-read `src`, `design`, `tests`, `production`, `assets`, Git
history, or agent directories. Bounded directory enumeration may locate indexed,
role-relevant representatives but may not establish completeness.

### Applicable instruction chains

Before opening any candidate content or recommending its path:

1. resolve the candidate's canonical real path inside the repository;
2. enumerate physical parents from root through the candidate's parent;
3. locate every applicable `AGENTS.md` in root-to-parent order within budget;
4. apply visibility/deny checks to each instruction source;
5. read and hash the full applicable chain before the target; and
6. combine rules by subject, with the closest applicable instruction overriding
   a conflicting ancestor rule while non-conflicting ancestor rules remain active.

Record chain order, instruction path/hash, governed target, overridden rule
source, effective rule, and resolution reason. Do not merely read root AGENTS.md
once and reuse it for every path.

If an applicable nested instruction file is unreadable, invalid, stale, denied,
or over budget, do not open or recommend the governed target. Record a safe
`OMITTED_POLICY`/`UNKNOWN_INSTRUCTION_CHAIN` coverage gap and return PARTIAL when
the target affects requested scope. Never bypass the closest rule using a more
permissive ancestor.

### Source records

For every planned source record:

- stable artifact ID and safe normalized path, unless redacted by policy;
- exact field/section locator;
- raw content SHA-256;
- first-read and final-rehash times;
- source state: `READ`, `MISSING`, `UNREADABLE`, `INVALID`, `STALE`,
  `OMITTED_BUDGET`, or `OMITTED_POLICY`;
- applicable instruction-chain IDs;
- visibility scope; and
- supported fact IDs.

Re-read and re-hash every readable source before returning. A changed source is
`STALE`; remove its claims from current prose and never combine it with earlier
bytes as one snapshot.

Use project facts only when a current readable source directly states them.
Placeholders such as `[CHOOSE]` or `TO BE CONFIGURED` are `UNKNOWN`. Planned work
is not implemented work; active work is not completed work; file presence is not
approval.

---

## Phase 4: Consume optional canonical stage and help evidence

Do not invoke `$project-stage-detect` or `$help` and do not reproduce either
algorithm.

### Stage evidence

When supplied, validate the complete producer-owned
`cgs.project-stage-detection/v2` packet, its raw expected hash for a path input,
canonical packet ID, project root ID, packet-bound catalog path/hash, snapshot
manifest, and every current raw hash or explicit source state. A reproducible
packet-declared ABSENT/UNREADABLE state may form a CURRENT diagnostic packet; it
blocks detection rather than packet consumption.

Record stage evidence state as `CURRENT`, `MISSING`, `INVALID`, `STALE`,
`PROJECT_MISMATCH`, `UNREADABLE`, or `OMITTED_POLICY`. Only CURRENT supplies
stage fields. Copy declared stage, detected stage, result, resolution,
confidence, snapshot/catalog identity, contradictions, read errors, coverage
gaps, and blocking reasons exactly. Do not parse stage.txt, inspect artifacts, or
turn UNKNOWN/CONFLICT/ERROR into a phase. The packet remains diagnostic, not gate
or access authority.

### Help recommendation evidence

When supplied, validate the complete evidence-bound `$help` recommendation
envelope and raw expected hash for a path input. Require its recommendation ID,
help snapshot, stage context/source, packet identity, catalog identity, one
primary action, same-level conflicts, all evidence buckets, receipt/run IDs,
packet diagnostics, `auto_executed: false`, `files_written: none`, and disclaimer.

Require its stage source to be `cgs.project-stage-detection/v2`; packet ID,
project root ID, packet snapshot manifest hash, and catalog hash must match the
CURRENT supplied stage packet when both are present. Revalidate every exposed
current evidence hash and the recommendation identity under its producer rule.
Do not repair, recompute a different project action, or accept an envelope whose
same-level conflicts are omitted.

Record recommendation evidence as `CURRENT`, `MISSING`, `INVALID`, `STALE`,
`PROJECT_MISMATCH`, `PACKET_MISMATCH`, `UNREADABLE`, or `OMITTED_POLICY`.
A valid help action is an external project recommendation, not an onboarding
instruction, manager assignment, approval, or authorization.

The onboarding `next_action` remains one non-mutating orientation action directly
supported by repository guidance: read one verified visibility-allowed file or
ask one source-identified artifact owner a bounded question. A supplied help
action may be copied into a separate `project_recommendation` field, but it may
become onboarding `next_action` only when it is itself non-mutating, within
visibility, explicitly repository-guided, and all cited sources/instruction
chains validate. Never run it.

Without current stage/help evidence, report those dimensions `UNKNOWN` or
`NOT_SUPPLIED`; never infer replacements. Missing optional evidence makes status
PARTIAL only when that dimension is requested or relevant to the resolved scope.

---

## Phase 5: Read Git only through an explicit privacy-safe window

Read Git activity only when a visibility-allowed authoritative repository source
declares exact `from_ref`, `to_ref`, window purpose, and allowed technical fields.
Validate both refs and the bounded range before reading up to the configured
commit limit. Do not fall back to “recent,” `HEAD~N`, dates guessed by the model,
current branch history, all branches, reflogs, or repository lifetime.

Default output omits author/committer names, emails, signatures, usernames,
private ticket IDs, branch/tag names, raw commit messages, review comments, and
other personal/private metadata. Summarize only directly supported technical
themes from allowed paths and fields after redaction. Do not infer team momentum,
productivity, velocity, staffing, ownership, performance, or who did the work
from commit count, frequency, or authorship.

If no authorized range exists, set recent activity to `UNKNOWN` or
`OMITTED_POLICY`. If the range is invalid, unreadable, over budget, or contains
unredactable required content, omit it and return PARTIAL when activity is
relevant. Never expose raw commits as a fallback.

---

## Phase 6: Build facts before prose

Every fact record contains:

```text
fact_id
topic
statement
source_artifact_id
source_locator
source_sha256
source_snapshot_state
applicable_instruction_chain_ids
visibility
confidence: DIRECT | UNKNOWN
```

Only DIRECT facts from current readable sources may be stated as project facts.
UNKNOWN fields remain explicit; do not fill them with common game-development
assumptions or nearby artifacts.

Return sections only when supported:

1. Scope, visibility, snapshot, and budget
2. Project overview
3. Repository role or area
4. Technology and architecture
5. Effective standards and conventions
6. Canonical declared/detected stage and current work
7. Key directories and verified files
8. Dependencies and repository-owned interfaces
9. Common pitfalls explicitly documented by the project
10. External evidence-bound project recommendation, when current
11. Safe first orientation action
12. Questions for a source-identified artifact owner
13. Sources, instruction chains, omissions, redactions, and uncertainty

For every recommended file, require current existence/readability, safe path/hash,
visibility allowance, and its complete effective root-to-parent instruction chain.
Do not recommend a denied, omitted, stale, or unverified path.

Tailor emphasis to the resolved repository role/area without hiding relevant
constraints. Never assign work, invent backlog tasks, claim a manager expects an
action, promise access, or state an undocumented organizational relationship.

---

## Phase 7: Determine status and return the packet

Return schema `onboarding_context/v2` with:

```yaml
schema_version: onboarding_context/v2
status: ONBOARDING READY | ONBOARDING PARTIAL | ONBOARDING ERROR
snapshot_at: <UTC>
repository_identity: <stable-id-or-UNVERIFIED>
resolved_scope: <GENERAL-or-role/area-id-or-UNRESOLVED>
visibility_scope: <effective-scope>
context_budget: <all limits>
budget_consumed: <entries/files/per-file-max/total-bytes/depth/commits>
coverage: <topic states and reason codes>
stage_evidence:
  state: CURRENT | MISSING | INVALID | STALE | PROJECT_MISMATCH | UNREADABLE | OMITTED_POLICY | NOT_SUPPLIED
  packet_id: <id-or-NONE>
  result: DETECTED | CONFLICT | UNKNOWN | ERROR | UNAVAILABLE
  resolution_state: CLEAR | BLOCKED | UNAVAILABLE
  declared_stage: <value-or-UNAVAILABLE>
  detected_stage: <stage-or-UNKNOWN>
  confidence: HIGH | MEDIUM | LOW
  snapshot_manifest_sha256: <sha256-or-UNVERIFIED>
  contradictions: [<ids>]
  blocking_reasons: [<codes>]
help_recommendation:
  state: CURRENT | MISSING | INVALID | STALE | PROJECT_MISMATCH | PACKET_MISMATCH | UNREADABLE | OMITTED_POLICY | NOT_SUPPLIED
  recommendation_id: <id-or-NONE>
  outcome: <help-outcome-or-UNAVAILABLE>
  primary_action: <external-action-or-UNAVAILABLE>
  same_level_conflicts: [<ids>]
facts: [<fact records>]
onboarding_summary: <source-cited sections>
recommended_files: [<path/hash/instruction-chain records>]
effective_instruction_chains: [<ordered rule records>]
source_manifest_sha256: <canonical-source-record-hash>
omitted_sources: [<generic safe records>]
redactions: [<generic codes>]
contradictions: [<stable records>]
stale_sources: [<safe records>]
project_recommendation: <external help action or NONE>
next_action: <one non-mutating orientation action or NONE>
files_written: none
auto_executed: false
disclaimer: REPOSITORY ORIENTATION ONLY — NOT ACCESS, AUTHORITY, ASSIGNMENT, OR APPROVAL
```

Apply this fail-closed order:

1. `ONBOARDING ERROR`: root AGENTS.md missing/unreadable/invalid/out of scope;
   repository identity unavailable; role/area ambiguous or invalid; invocation
   invalid; or policy prevents required root/identity coverage.
2. `ONBOARDING PARTIAL`: required root and identity are valid, but any requested
   or role-relevant optional dimension is missing, unreadable, stale,
   contradictory, budget-omitted, policy-omitted, or UNKNOWN.
3. `ONBOARDING READY`: required and relevant bounded coverage is current and
   direct, no omission affects scope, every recommended path has a complete
   effective instruction chain, and no unresolved UNKNOWN could mislead the user.

Never emit `ONBOARDING COMPLETE`. READY means only that this bounded orientation
snapshot is adequately sourced. It grants no access or authority and does not
assert that undocumented practices do not exist.

Return at most one non-mutating next action and stop. Never persist the packet.

## Non-negotiable rules

- Root AGENTS.md is mandatory and secondary sources never replace it.
- Applicable nested instructions are loaded before governed content.
- Visibility, deny policy, and budgets apply before access.
- Sensitive paths and metadata never enter output or recommended reading.
- Repository roles never become human hierarchy or authority.
- Git has no implicit recent-history fallback and no personal/performance output.
- Stage/help evidence is optional, explicit, current, and never recomputed locally.
- Every path is read-only and every handoff remains unexecuted.
