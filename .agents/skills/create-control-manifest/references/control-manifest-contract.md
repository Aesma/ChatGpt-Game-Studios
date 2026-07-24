# Control Manifest — Source, Rule, Version, and Transaction Contract

This contract is normative for `$create-control-manifest`. It defines the bounded
source closure, Accepted-ADR/TR admission, source-faithful rule schema, stable
identity, deterministic deduplication/conflict handling, monotonic versions,
rule-level update semantics, immutable provenance, and the only permitted
compare-and-set transaction.

## 1. Authority and owned artifact

The only persistent output owned by this author workflow is:

```text
docs/architecture/control-manifest.md
```

Atomic publication may use one same-directory temporary file after successful CAS;
it must be consumed or removed and is never an artifact.

The control manifest is a derived programmer view, never a policy source:

| Information | Authoritative source | Manifest treatment |
|---|---|---|
| Product requirement/scope | Current approved GDD requirement | Stable TR reference only |
| Binding technical rule | Current Accepted ADR and lifecycle record | Source-faithful derived rule |
| Global project preference | Current technical-preferences source | Derived rule at exact source strength/scope |
| Engine deprecation/constraint | Pinned current engine reference | Derived fact with provenance/coverage |
| Proposed/rejected/superseded ADR | ADR/lifecycle source | Exclusion or unknown/conflict evidence, never rule authority |
| Architecture layout/traceability | Current `cgs.master-architecture/v3` view | Input index/cross-check only, never rule authority |
| Manifest review verdict | Independent catalog-declared reviewer | External evidence only |
| `ACTIVE` status | Separate catalog-declared recorder | Never written by this author |

The workflow never writes or repairs architecture, GDD, ADR, lifecycle/review
evidence, registry, technical preferences, engine references, story/epic, gate,
catalog, test, session-state, status pointer, or review record.

## 2. Bounded input manifest

Freeze one repository-root identity and one UTC snapshot. Record normalized
project-relative path, real-path/root result, role, stable source ID, consumed
scope, source/lifecycle state, revision, exact raw-byte SHA-256, or explicit
`ABSENT`/`UNREADABLE` marker.

Hard ceilings:

| Class | Allowed source | Count | Per file | Class bytes |
|---|---|---:|---:|---:|
| Workflow catalog | `.codex/docs/workflow-catalog.yaml` | 1 | 512 KiB | 512 KiB |
| Target/base manifest | `docs/architecture/control-manifest.md` or ABSENT | 1 | 2 MiB | 2 MiB |
| Master architecture | `docs/architecture/architecture.md` | 1 | 2 MiB | 2 MiB |
| Architecture review evidence | one explicit path/inline `cgs.review-evidence/v1` | 1 | 2 MiB | 2 MiB |
| Architecture registry | `docs/registry/architecture.yaml` when present | 1 | 1 MiB | 1 MiB |
| Accepted ADR | exact paths from current architecture/registry/catalog closure | 64 | 512 KiB | 16 MiB |
| ADR lifecycle/review evidence | exact links from ADR/registry | 64 | 256 KiB | 8 MiB |
| Technical preferences | `.codex/docs/technical-preferences.md` | 1 | 256 KiB | 256 KiB |
| Engine VERSION/reference | pinned VERSION plus exact referenced constraint domains | 32 | 512 KiB | 8 MiB |
| Project standards | exact catalog/ADR-linked paths | 16 | 256 KiB | 2 MiB |
| Prior control-manifest review | one explicit currentness candidate | 1 | 2 MiB | 2 MiB |

Total bytes read must not exceed 40 MiB. Enumerate only direct children under a
catalog-declared artifact glob, sorted by normalized path. Never recurse, follow a
symlink outside the root, choose evidence by newest/nearest/number, or scan an
engine source tree.

Use layered loading:

1. parse catalog, architecture header/manifest/TR/decision indexes, registry, and
   supplied evidence envelopes;
2. construct the complete intended path/record manifest;
3. validate exact source/lifecycle hashes without loading unrelated bodies;
4. parse only normative/alternative/performance/compatibility sections of admitted
   ADRs plus exact technical-preference/engine constraint sections; and
5. re-hash every complete source before approval and CAS.

Hashing a file does not authorize full-context ingestion. Oversize, unreadable,
ambiguous, changed-during-snapshot, count/class/total overflow, or an uncompleted
required source yields `PARTIAL` with exact reason such as
`CONTEXT_BUDGET_EXCEEDED`, `SOURCE_CHANGED`, or `SOURCE_UNREADABLE`. Never sample
and publish an apparently complete/Active manifest.

Canonicalize the ordered input manifest as JSON with lexicographic keys; arrays by
role, stable source ID, normalized path, and consumed scope; UTF-8/LF; no
insignificant whitespace. Its identity is:

```text
source_manifest_id: sha256:<canonical ordered input manifest>
```

Any path/byte/state/revision/scope/evidence/directory-membership change invalidates
the identity.

## 3. Current architecture, TR, and Accepted ADR admission

The architecture input must parse as `cgs.master-architecture/v3`. Validate its
source manifest identity, immutable provenance chain, current derived TR map, ADR
decision ledger, status, and exact raw hash. The architecture is an index/cross-
check; text found only there never becomes a control rule.

A usable architecture review input is envelope `cgs.review-evidence/v1`, producer
`architecture-review`, extension `cgs.architecture-review/v2`, full-mode verdict
`PASS`, coverage COMPLETE, current record identity, and a manifest containing:

- `docs/architecture/architecture.md` with role `architecture-derived` and exact
  current hash; and
- all source/ADR/TR evidence needed to reproduce or explicitly bind the
  architecture's source manifest.

Missing/different artifact, manifest, mode, scope, ruleset, or source makes review
evidence stale/unbound. An author may still construct a clearly PARTIAL Draft for
diagnosis when sources are safe, but cannot claim architecture readiness or
publish/route an Active manifest.

Admit one TR only when its architecture row is `CURRENT` and
`DERIVED_COVERED`, its exact source requirement/approval evidence is current, and
all referenced source IDs/hashes reproduce. `CHANGED`, `STALE`, `UNBOUND`,
`DECISION_GAP`, `SOURCE_BLOCKED`, provisional, or ambiguous TRs are blockers or
unknown evidence, never rule scope authority.

Admit one ADR as `ACCEPTED_CURRENT` only when:

- exact stable ADR ID/path/hash appear in the input manifest and architecture
  decision ledger;
- ADR declares Accepted;
- a current lifecycle record binds the exact ADR hash, Accepted transition,
  recorder identity/time, and independent review evidence;
- supersession/dependency chain is complete/current; and
- registry/architecture/lifecycle evidence has no conflict.

Other states are `PROPOSED`, `SUPERSEDED`, `REJECTED`, `STALE`, `UNBOUND`,
`CONFLICT`, or `UNKNOWN`. Preserve every exclusion/state/hash. Proposed or status-
text-only ADRs never contribute rules.

Each ADR-derived rule may reference only TR IDs explicitly addressed by the same
ADR and current architecture ledger. Missing/ambiguous TR linkage is `UNKNOWN` and
cannot be fabricated from similar wording.

## 4. Source-faithful rule schema

Every derived item uses `cgs.control-rule/v2`:

```text
rule_id: RULE-<16 lowercase hex>
kind: NORMATIVE | PROHIBITION | CONTEXTUAL_REJECTION | GUARDRAIL | ENGINE_CONSTRAINT
level: MUST | MUST_NOT | SHOULD | SHOULD_NOT | MAY | NONE
scope:
  layers: [Foundation | Core | Feature | Presentation | Polish | Global]
  system_ids: [<stable IDs>]
  phases: [<source-declared values>]
  conditions: <preserved source conditions or NONE>
exact_meaning: <minimal grammar normalization without semantic change>
source:
  source_kind: ADR | TECHNICAL_PREFERENCE | ENGINE_REFERENCE
  source_id: <stable ID>
  path: <normalized path>
  section: <exact section>
  locator: <stable locator>
  exact_excerpt: <bounded exact source wording>
  excerpt_sha256: <hash of exact excerpt bytes>
  source_sha256: <hash of complete source bytes>
  lifecycle_record_id: <ID or NOT_APPLICABLE>
  lifecycle_record_sha256: <hash or NOT_APPLICABLE>
tr_ids: [<sorted current TR IDs>]
derivation: DERIVED_CURRENT | SOURCE_STALE | SOURCE_BLOCKED | UNKNOWN
supersedes_rule_ids: [<stable IDs>]
```

Rule ID construction:

1. Prefer a source-owned stable rule/constraint ID, deriving `RULE-<16hex>` from
   `(source_kind, source_id, source_rule_id)`.
2. Otherwise derive it from `(source_kind, source_id, section, stable locator,
   exact normative clause, preserved scope, level)`.
3. Preserve every persisted ID while the same source rule identity/meaning/scope
   remains. Never assign by extraction order, layer table position, date, or count.

When source meaning/level/scope changes, create a new rule ID and explicit
supersedes link; never silently retarget the old ID. When only the source file hash
changes around an unchanged stable source-owned rule, preserve ID, update
provenance, and expose the source-hash change in the rule diff.

Normative level is exact:

| Source normative meaning | Level |
|---|---|
| MUST, REQUIRED, SHALL, explicit mandatory positive | `MUST` |
| MUST NOT, SHALL NOT, explicit mandatory negative | `MUST_NOT` |
| SHOULD, RECOMMENDED | `SHOULD` |
| SHOULD NOT, NOT RECOMMENDED | `SHOULD_NOT` |
| MAY, OPTIONAL | `MAY` |
| no clear normative meaning | no normative rule; `UNKNOWN` finding |

Do not promote, weaken, reverse, drop qualifications, or broaden scope. A sentence
with several levels is split while preserving shared conditions/provenance.

An alternative enters `PROHIBITION` only when its authoritative source explicitly
says forbidden/prohibited with matching scope. Rejected, deferred, not-selected,
or lower-ranked alternatives are `CONTEXTUAL_REJECTION`, level NONE, with reason,
scope, and reconsideration conditions. They never become global `never` rules.

Technical preferences contribute only exact normative statements in their
declared scope. Engine references contribute deprecation/constraint facts only
when pinned version/reference coverage is current and explicit. Descriptive best
practice text is not promoted.

## 5. Deterministic deduplication, conflict, and unknown

Sort candidate rules by source kind, source ID, section/locator, then rule ID.

Deduplicate only when level, kind, normalized exact meaning, full scope/conditions,
TR IDs, and applicability are identical. The surviving rule ID is the
lexicographically smallest stable ID; retain every source record in sorted
`equivalent_sources`. Similar prose or shared keywords are not duplicates.

Lifecycle supersession is the only automatic precedence. A newer date, higher ADR
number, architecture order, narrower/broader scope, layer, or preferred source does
not silently win. A scoped exception overrides another rule only when current
Accepted evidence explicitly declares the relationship and exact overlap.

For two non-superseded rules whose scopes overlap and whose required/forbidden or
level/meaning outcomes cannot both hold, create:

```text
conflict_id: CONFLICT-<16 lowercase hex of sorted rule IDs + overlap scope>
state: BLOCKED
rule_ids: [<sorted IDs>]
overlap_scope: <exact intersection>
source_evidence: [<paths/sections/hashes>]
```

Do not choose a winner, merge incompatible meanings, downgrade a MUST, or let the
user waive source contradiction inside this derived workflow. Resolve it in the
authoritative ADR/lifecycle sources.

Malformed/ambiguous normative wording, missing scope/TR/source/lifecycle data, or
unverifiable engine coverage creates a stable
`UNKNOWN-<16hex(source identity + locator + reason)>` finding. UNKNOWN is omitted
from executable rules and blocks Active eligibility when the source could be
mandatory.

Any unresolved BLOCKED conflict or blocking UNKNOWN prevents a complete publish;
the author may emit PARTIAL only when its limitations and excluded rules are
explicit and downstream use is forbidden.

## 6. Canonical manifest, version, and payload identity

The exact UTF-8/LF document follows `cgs.control-manifest/v2` with sections:

1. Document Status and Authority Boundary;
2. Source Manifest and Current Architecture Review;
3. Version/Payload Identity;
4. ADR/TR Coverage Ledger;
5. Normative Rules by layer and Global;
6. Explicit Prohibitions;
7. Contextual Rejections;
8. Performance Guardrails;
9. Engine Constraints and Coverage;
10. Conflict/Unknown Findings;
11. Retired/Superseded Rules;
12. Local Extensions (Non-Authoritative); and
13. Immutable Revision/Provenance History.

Header fields include:

```text
Schema: cgs.control-manifest/v2
Status: DRAFT | PARTIAL | ACTIVE
Manifest Version: <positive monotonic integer>
Generated At: <UTC ISO-8601 with timezone>
Source Manifest ID: sha256:<input manifest>
Ruleset ID: cgs.control-extraction-rules/v2
Ruleset SHA-256: <exact extraction contract hash>
Payload SHA-256: sha256:<canonical semantic payload>
Prior Artifact SHA-256: <hash-or-ABSENT>
External Review: NOT_CURRENT | <record identity>
```

This author writes only DRAFT or PARTIAL and External Review NOT_CURRENT.

`Payload SHA-256` is computed over canonical JSON of all semantic source/coverage/
rule/conflict/unknown/retirement content plus manifest version, excluding generated
time, document status, external review/recorder fields, payload hash itself, and
human formatting. The exact artifact SHA-256 is computed externally after rendering
and never embedded as its own current hash.

For CREATE, version is 1. For a valid UPDATE whose semantic payload/provenance
changes, version is `base version + 1`; it must be greater than every prior
provenance version. Same-day different content therefore has different version and
payload/artifact hashes. On exact no-op, preserve the base version/generated time,
write nothing, and append no event.

Each actual content update appends one immutable provenance event with event ID,
base/candidate versions, base hash, source manifest ID, payload hash, changed rule/
finding IDs, generated_at, and author-side task identity. Never edit/delete/reorder
prior events.

Local human content is allowed only under `Local Extensions (Non-Authoritative)`
with `x-local-*` stable IDs. Preserve it byte-for-byte/canonically across updates.
It cannot add/override/suppress/relevel a derived rule or satisfy conflict/unknown.
Unknown content outside supported schema/extension namespace is
`BLOCKED_INVALID_BASE`.

## 7. Rule-level update diff

For UPDATE construct:

```text
BASE + deterministic current SOURCES -> CANDIDATE
```

Show stable-ID sets:

- unchanged rules with unchanged provenance;
- provenance-only changes;
- added rules;
- removed-from-active rules moved to Retired/Superseded with reason/source state;
- changed level/scope/meaning represented as old retirement + new rule/supersedes;
- added/resolved/changed conflict and UNKNOWN IDs;
- changed ADR/TR/engine coverage;
- preserved local extensions and prior provenance; and
- version/payload/artifact hash delta.

Never silently delete a rule. A source no longer Accepted/current retires its rule
with exact reason; it does not remain Active and is not erased. A manual extension
is never merged into derived rule state.

If current canonical semantic payload, source manifest, formatted bytes, and base
provenance are identical, operation is `UNCHANGED`: no write, version bump,
generated-time change, review invalidation, or new history event.

## 8. Approval, CAS, and publication

Show the complete candidate/lossless representation, source manifest/limits,
architecture review currentness, ADR/TR ledger, every rule/finding/source, complete
rule-level diff, version/payload/candidate hash, immutable provenance append, local
extensions, and one-file changeset. Obtain one user approval bound to all exact
values. It is file authorization only, not source approval, independent review, or
Active recording.

The preview binds root identity, destination parent, catalog, base/absence,
architecture, architecture review, registry, every ADR/lifecycle/review record,
technical preferences, engine/version/reference, standards, enumerated directory
membership, ruleset bytes/hash, input manifest ID, BASE/provenance, candidate
semantic payload/version/bytes/hash, and decision IDs.

Immediately before mutation, re-read/re-hash the full closure, rebuild the ordered
manifest and deterministic extraction, reapply update diff, and require every bound
state/hash plus candidate payload/artifact hash to equal preview.

Any difference is `CONFLICT`: zero writes; exact old/new evidence; no merge,
refresh, retry, overwrite, re-review, or implicit acceptance.

After CAS:

1. write exact candidate bytes to one same-directory temporary file;
2. flush/close as supported;
3. atomically create/replace only the control manifest;
4. re-read and verify exact artifact bytes/hash;
5. reparse and validate v2 schema, version/payload, source ledger, stable rules,
   conflicts/unknowns, local extensions, immutable history, DRAFT/PARTIAL, and
   External Review NOT_CURRENT; and
6. confirm no other persistent path changed because of this workflow.

Report WRITTEN only after every verification succeeds. Pre-publication failure is
FAILED; publication/read-back/result uncertainty is PARTIAL with exact observed
state. Never claim COMPLETE/Active or repair/revert external concurrent changes.

## 9. Independent review and Active recorder separation

This author never delegates/impersonates a reviewer, writes review evidence, or
sets Active. It may consume one explicitly supplied prior control-manifest review
only to report currentness.

A usable review is generic `cgs.review-evidence/v1` from the unique catalog-declared
control-manifest reviewer, with catalog-declared extension/ruleset, exact current
manifest path/artifact hash, source manifest ID, payload hash, complete rule/conflict/
unknown coverage, current record identity, and passing verdict. A changed byte,
source, ruleset, profile, or scope makes it stale. Do not invent a review schema or
reviewer when catalog policy is absent.

Only a separate catalog-declared recorder may set ACTIVE after independently
validating current passing review, exact artifact/payload/source-manifest hashes,
complete Accepted ADR/current TR coverage, no BLOCKED/UNKNOWN source fidelity gap,
monotonic version/provenance chain, and its own CAS policy. The recorder may change
only status/review reference/recording event; it cannot rewrite derived rules.

This author returns exactly one catalog-derived source-resolution, review, recorder,
or downstream action—or `Stop`—and never executes it.
