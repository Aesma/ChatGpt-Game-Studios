---
name: scope-check
description: Compares one exact immutable approved scope baseline with one exact current scope manifest using stable Scope IDs, deterministic delta and authority classifications, bounded evidence, and strictly read-only hash-bound results.
---

# Scope Check

Compare two explicit scope artifacts without choosing product scope or changing
any plan. Stable Scope IDs and schema-declared semantic hashes determine deltas;
owner-authorized records determine whether a delta is allowed; compatible receipts
determine impact support. These are separate questions.

## Invocation

Use one exact command:

```text
$scope-check compare
  --baseline <project-relative-path>@sha256:<64-lowercase-hex>
  --current <project-relative-path>@sha256:<64-lowercase-hex>

$scope-check inspect
  --baseline <project-relative-path>@sha256:<64-lowercase-hex>
  --current <project-relative-path>@sha256:<64-lowercase-hex>
  --evidence <project-relative-path>@sha256:<64-lowercase-hex>

$scope-check discover
```

- `compare` reads the immutable pair plus only their exact mandatory
  approval/authority/normalization identity records.
- `inspect` additionally reads only paths and exact revisions allowlisted by one
  immutable evidence manifest.
- `discover` reads canonical active-state pointers only, lists exact candidate
  `path@sha256` identities, and returns `INPUT REQUIRED`. It never chooses or
  compares candidates.

Reject missing/repeated/unknown options, positional artifacts, bare paths without
hashes, non-SHA-256 identities, absolute/out-of-project/traversing paths, escaping
links, identical/aliased pair members, unsupported artifact types/schemas, and
fuzzy names. No arguments or one missing pair member returns `INPUT REQUIRED`;
invalid or ambiguous resolution returns `ERROR`. Never infer by title, feature,
sprint nickname, similar filename, modification time, or newest active artifact.

## Read-only boundary

The allowed write set is empty. Do not edit or create baselines, current manifests,
stories, epics, sprints, milestones, evidence, decisions, estimates, reports,
session state, Git state, or re-baseline records. Do not invoke gates, planners,
estimators, producers, or follow-up workflows. Do not scan the repository for
related scope, code, TODOs, commits, or issue text.

Read [scope-rules-v1.md](references/scope-rules-v1.md) completely. It defines the
artifact schemas, stable identities, semantic normalization, classifications,
bounded evidence, authority records, impact algorithms, canonical results, and
output evidence.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. Missing, unreadable, or inconsistent contract files
are `ERROR`; no comparison verdict is produced.

## Freeze exact artifact identities

Read exactly the supplied baseline/current paths. Before parsing, record canonical
project-relative path, byte length, complete SHA-256, schema ID/version, artifact
ID/version, source revision, parent scope/timebox, and completeness. The actual
hash must equal the invocation hash.

The baseline must be immutable and approved: it cites one current immutable
approval record with authorized product owner, authority source, decision,
timestamp, signature/record hash, and exact baseline ID/version/hash. The current
manifest must declare that same baseline ID/version/path/hash and the same parent
scope/timebox. Multiple records, stale hashes, missing approval/authority, or a
different baseline link returns `INSUFFICIENT EVIDENCE`.

Never substitute newer bytes at the same path. A later baseline version is a
different comparison identity and requires a separately authorized immutable
re-baseline record; this skill neither creates nor applies it.

## Load stable scope entries

Both artifacts must declare complete unique stable `Scope ID` entries under a
supported versioned schema. Do not synthesize IDs from titles, row positions,
file paths, commits, or prose similarity. Normalize only semantic fields explicitly
named by that schema, including scope boundary and acceptance semantics; exclude
presentation ordering/formatting. Hash the canonical semantic payload per entry.

Presentation row splits/merges do not create deltas when stable IDs and semantic
hashes remain identical. Duplicate/missing IDs, unsupported normalization, hidden
deletions, conflicting parent identities, or incomplete manifests produce
`UNMAPPED`/`CONFLICT` evidence and block a complete result.

Current product scope comes only from the current manifest. Code, Git history,
TODO/FIXME, issue text, build output, or implementation status may be allowlisted
as implementation evidence but can never add/remove/modify scope, prove approval,
or identify the product decision owner.

## Compute deterministic stable-ID deltas

Compare stable ID sets and semantic hashes:

```text
ADDED | REMOVED | MODIFIED | UNCHANGED | UNMAPPED | CONFLICT
```

For each ID emit one stable `SCP-DELTA-*` record. Its fingerprint uses baseline
ID/version, parent scope, Scope ID, and delta type; it excludes baseline/current
byte hashes, title, row/line, timestamp, or report wording. Store exact baseline/
current artifact and entry hashes separately for reproducibility and staleness.

Classify authority separately:

```text
APPROVED_CHANGE | PROPOSED_CHANGE | NO_RECORD | UNVERIFIED_RECORD |
UNAUTHORIZED_RECORD | STALE_RECORD | HASH_MISMATCH |
CONFLICTING_RECORD | NOT_APPLICABLE
```

Then derive the allowed-state classification defined by the rules file:

```text
ALLOWED_UNCHANGED | ALLOWED_ADDITION | ALLOWED_REMOVAL |
ALLOWED_MODIFICATION | UNAPPROVED_ADDITION | UNAPPROVED_REMOVAL |
UNAPPROVED_MODIFICATION | CONFLICT
```

An addition/removal/modification is allowed only when one final immutable change
decision binds the exact delta/Scope ID, baseline/current hashes, parent/timebox,
authorized product owner, authority proof, rationale, timestamp, and signature.
A commit author, implementer, agent recommendation, conversation acknowledgment,
or prose justification is not decision authority.

## Treat accepted change and accepted risk separately

A valid approved scope-change decision authorizes the named delta; it does not
accept schedule, quality, or integration risk. A valid accepted-risk record may
acknowledge one evidence-bound impact dimension; it does not authorize the scope
delta, alter delta type, create a new baseline, or turn missing evidence into
support.

Risk acceptance must bind exact Delta IDs, baseline/current/evidence hashes,
dimension and exposure, authorized product/risk owner plus authority proof,
rationale, compensating controls, timestamp, signature, and expiry/review trigger.
Expired, unsigned, self-authored, authority-unverifiable, or hash/scope-mismatched
records are invalid. This skill cannot create, renew, sign, or apply either record.

## Attach only bounded explicit evidence

`inspect` validates one `cgs.scope-evidence-manifest/v1` bound to the exact pair.
It is a closed allowlist, not a discovery hint. Read only exact `path@sha256`
entries and exact Git commits/range named by it, subject to the fixed budgets in
the rules file. Never expand the list.

Evidence may describe implementation activity, change decisions/authority,
estimates/capacity, dependencies/interfaces, test/regression coverage, or accepted
risk. Every receipt must bind stable Scope/Delta IDs and exact baseline/current
hashes. Missing, stale, incompatible, unreadable, over-budget, or unexamined
declared evidence is explicit `UNVERIFIED` and makes `inspect` `PARTIAL`; preserve
valid core deltas.

## Derive impact evidence without intuition

Never compute scope health, bloat, severity, or effort from item/file/commit/TODO
counts or percentages. One large subsystem and ten text items remain incomparable
without compatible estimate receipts.

Effort delta requires one calibrated method/unit/confidence policy across every
changed ID, bound to both artifacts. Report absolute interval arithmetic only.
Schedule, quality, and integration use the fixed evidence algorithms in the rules
file and return only:

```text
SUPPORTED_NO_EXPOSURE | SUPPORTED_EXPOSURE | INDETERMINATE |
UNVERIFIED | NOT_APPLICABLE
```

Do not invent Low/Medium/High or an overall risk score. Impact states never change
delta type, authority classification, or the canonical comparison result.

## Enforce bounded completeness and input stability

Apply the baseline/current entry/byte and evidence path/byte/commit/receipt/edge/
test-map limits from the rules reference. Process input re-hashes in chunks no
larger than the re-hash batch limit. List every unchecked identity on scope
overflow and return `PARTIAL` after any meaningful core comparison. Never silently
truncate denominators.

Hash every consumed artifact before use and immediately before output. If
baseline/current bytes change, discard delta conclusions and return
`INSUFFICIENT EVIDENCE — INPUT CHANGED DURING CHECK`. If optional evidence changes,
preserve core deltas, invalidate dependent classifications/impact, and return
`PARTIAL`. The skill never repairs, reverts, or updates changed inputs.

## Apply deterministic result precedence

Use exactly one result:

```text
ERROR | INPUT REQUIRED | INSUFFICIENT EVIDENCE | PARTIAL |
NO SCOPE DELTA | SCOPE DELTA FOUND
```

1. Invalid syntax/path/alias/schema/unreadable artifact -> `ERROR`.
2. Discovery/no arguments/missing pair member -> `INPUT REQUIRED`; no comparison.
3. Invalid/stale/conflicting baseline/current identity, approval, linkage,
   completeness, stable IDs, normalization, or changed core bytes ->
   `INSUFFICIENT EVIDENCE`.
4. Core identity/diff meaningful but bounded core/evidence/re-hash coverage
   incomplete -> `PARTIAL`.
5. Complete core comparison with no ADDED/REMOVED/MODIFIED/UNMAPPED/CONFLICT ->
   `NO SCOPE DELTA`.
6. Complete core comparison with at least one ADDED/REMOVED/MODIFIED and no
   UNMAPPED/CONFLICT -> `SCOPE DELTA FOUND`.

`NO SCOPE DELTA` is not PASS, schedule/quality approval, implementation readiness,
or permission to proceed. `SCOPE DELTA FOUND` is descriptive; an authorized delta
still remains a delta.

## Return read-only evidence and stop

Return `cgs.review-evidence/v1` with a `cgs.scope-check/v2` extension as defined
in the rules reference. Include exact immutable artifact identities, normalization
schema/hash, stable sorted deltas, authorization/allowed/risk states, bounded
evidence coverage, impact calculations, unchecked scope, final re-hashes, result,
stale key, and input mutation guard.

Direct output is conversation-only:

```text
gate_evidence_status: NOT_PERSISTED
gate_evidence_eligible: false
operation: READ_ONLY
```

When deltas exist, present two or three neutral unranked response options tied to
affected Scope IDs, evidence unknowns, owner, and separate required decision/action.
Do not recommend, choose, label Cut/Keep/Defer, launch a workflow, apply a change,
or re-baseline. Stop after the report.
