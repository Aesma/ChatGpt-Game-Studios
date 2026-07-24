---
name: ux-review
description: Read-only, profile-aware review of UX specifications, HUD designs, and interaction-pattern libraries. Uses the current ux-design author schema, hash-bound evidence, deterministic verdicts, bounded batch/reviewer execution, and stable finding convergence.
---

# UX Review

Review UX authoring artifacts without modifying them. The reviewer proves what it
read, applies the profile selected by artifact metadata, and returns a
conversation-only review record. It does not approve a filename, an unchecked
artifact, a stale dependency, or an accepted risk.

## Inputs

Use this strict grammar:

```text
$ux-review <target-path|all|hud|patterns>
           [--review-depth standard|expert]
           [--prior-review <record-path>]
```

- `target-path` is one exact local UX artifact.
- `all` selects every eligible UX artifact in the bounded project manifest.
- `hud` and `patterns` filter that manifest to the corresponding artifact type.
- `--review-depth standard` is the default and performs all checks locally.
- `--review-depth expert` additionally requires one bounded `ux-designer`
  consultation. It never transfers verdict ownership.
- `--prior-review` is valid only for one target and enables convergence review.

Reject unknown options, duplicate options, ambiguous paths, more than one target,
or a prior review with a batch selector. Return usage plus `ERROR`; do not guess.

## Non-negotiable boundaries

1. Be strictly read-only. Do not edit the target, dependencies, registries,
   reports, or project state. Do not persist the returned review record.
2. Read the current `ux-design` `SKILL.md` and its continuation reference before
   reviewing. Compute `author_schema_hash` as SHA-256 of the exact main bytes,
   one NUL byte, then the exact continuation bytes. Parse their normative author
   declarations and construct/hash `cgs.ux-author-contract-manifest/v1`; accept
   only a reviewer-supported declared profile/content/schema tuple and record
   `author_contract_manifest_sha256`.
3. Use artifact metadata to select the profile. Aliases select candidates only;
   a filename, directory name, or user label never overrides metadata.
4. Use exact local bytes and SHA-256 for every artifact or dependency used as
   evidence. A path without a matching hash is not current evidence.
5. Keep mechanical checks local. A consultation may add evidence or findings but
   cannot waive a failed assertion, redefine the schema, or emit the verdict.
6. `Accepted risk` is not approval. It remains a visible open finding with an
   owner, rationale, scope, and expiry or review trigger.
7. A conversation response is not persistable gate evidence. A separate recorder
   must revalidate all hashes before persistence.

## Load the review contract

Read [review-rules-v1.md](references/review-rules-v1.md) completely. It defines
the supported author-contract gate, profile matrix, content assertions,
dependency and coverage rules, finding identity, verdict algorithm, and output
schemas. If it is missing, unreadable, or inconsistent/incomplete for the current
author manifest, return `MIGRATION REQUIRED` with a null verdict.

Read [continued-workflow.md](references/continued-workflow.md) completely for
the bounded discovery, dependency resolution, optional reviewer, convergence,
mutation guard, and rendering procedure.

## Route each target

Resolve the exact file, read its bytes, and hash it. Parse these header fields:

- `Artifact Type`
- `Schema Version`
- `Profile Version`
- `Content Profile`
- `Artifact ID`
- `Screen ID` when the schema requires it
- `Status`
- `Platform Profile`
- `Accessibility Foundation`
- `Requirement IDs`
- `Context Manifest SHA-256`
- `Authoring Receipt ID`

Before profile routing, require the current author sources to declare one
coherent contract and require that exact declared tuple to be in the reviewer
support set. The currently supported tuple is `ux-profile-schema-v2`,
`cgs.ux-content-profile/v2`, and
`ux-design-author-sha256:<computed author_schema_hash>`. Then require the target
header to match all three values exactly. An unsupported declaration, missing or
conflicting author value, incomplete assertion-matrix coverage, unsupported legacy `ux-profile-schema-v1`,
or target hash/profile/content mismatch returns
`MIGRATION REQUIRED` with null verdict. Do not route or score content under a
fallback or mixed contract.

Route only by `Artifact Type` and the current author schema:

| Artifact Type | Review profile |
|---|---|
| `ux-spec` | `screen-spec` |
| `hud-design` | `hud` |
| `interaction-pattern-library` | `pattern-library` |

The exact author template marker may recover an absent type only when the
current author schema explicitly defines that marker. Record the recovery as a
finding. For one exact target only, a filename may propose a type after both
metadata and marker routing fail; ask the user to confirm the proposed type and
emit no verdict before confirmation. Record `user-confirmed-filename-fallback`
after confirmation. Confirmation cannot supply or override Schema Version,
Profile Version, Content Profile, Artifact ID, or any other missing evidence, so a legacy target
still normally returns `MIGRATION REQUIRED`. Batch selectors exclude such
unknown candidates instead of prompting. A conflicting, unknown, or obsolete
type/schema is `ERROR` or `MIGRATION REQUIRED`; its verdict is null. Exclude
prior review records and non-UX documents from selectors.

## Evaluate content, not headings

For every required assertion in the selected profile, record exactly one state:

```text
VALID | EMPTY | PLACEHOLDER | INVALID | MISSING |
NOT_APPLICABLE | UNEVALUATED
```

- `VALID` means the required semantic content is present, internally coherent,
  and supported by current evidence where the assertion requires evidence.
- `EMPTY` includes whitespace-only fields, blank table rows, or headings with no
  substantive body.
- `PLACEHOLDER` includes `TODO`, `TBD`, bracketed template text, example-only
  rows, or prose that merely restates the heading.
- `INVALID` means content exists but violates the assertion, uses an invalid ID,
  conflicts with evidence, or cites a stale/unresolved source.
- `MISSING` means the required field, section, row, or semantic element is absent.
- `NOT_APPLICABLE` is allowed only for an assertion marked conditional by the
  current schema and only with a current source ID/path/hash plus specific
  rationale. An unsupported `N/A` is `INVALID`.
- `UNEVALUATED` means the reviewer could not finish the assertion. It forces a
  partial result.

Section existence alone can never produce `VALID`. Apply the exact profile
assertions in the rules reference and any stricter current author-schema rule.
If the sources disagree, stop with `MIGRATION REQUIRED`; do not silently merge
incompatible schemas.

## Resolve dependencies and trace requirements

Build a dependency ledger before quality scoring. Validate each referenced path,
hash, stable ID, and declared version. In particular:

- Platform authority is the exact `Platform Profile` `path@hash` resolved through
  the bounded context manifest. `Platform Target` prose is not a fallback.
- Accessibility authority is the exact `Accessibility Foundation`
  `path@hash/tier`. The committed tier must exist and be readable.
- The requirement denominator is the union of current stable IDs declared in the
  artifact and current owner-approved in-scope requirement IDs for the same
  stable artifact/screen identity in the bounded context manifest.
- A GDD filename, heading, free-form title, or repository-wide search does not
  establish requirement coverage.
- A numeric runtime performance budget is checked only when an exact current
  performance or technical source ID defines its platform, hardware, scenario,
  and budget. UX review checks perceived responsiveness, feedback, recovery, and
  state communication; it never invents a universal millisecond threshold.

Missing, unreadable, stale, or contradictory required dependencies make the run
`PARTIAL`. Preserve confirmed findings, list every gap, and never emit
`APPROVED`. Requirements absent from the denominator or denominator entries not
covered by the artifact are findings. If the denominator itself cannot be
completed, the result is also `PARTIAL`.

## Review and converge

Perform deterministic mechanical checks locally. At `expert` depth, dispatch at
most one `ux-designer` reviewer using the worker schema in the rules reference.
Decline, timeout, malformed output, target-hash mismatch, or substantive evidence
conflict makes the run `PARTIAL`; local mechanical results remain authoritative.

When `--prior-review` is supplied, verify its generic and UX schemas, record ID,
target identity, prior target hash, author schema hash, author contract manifest
hash, profile/content versions, and finding fingerprints.
Evaluate every prior `OPEN` or accepted-risk finding first. Then inspect the exact
prior-to-current diff and current cross-references for revision-introduced
regressions. Reuse a stable finding ID when its fingerprint is unchanged. Record
`RESOLVED`, `OPEN`, `REGRESSED`, or `SUPERSEDED` explicitly. Never declare
convergence from a prose summary or an unrelated/stale record.

## Decide the result

Apply this precedence after all required assertions have a state:

1. Invalid invocation, unresolved target identity, unsupported artifact/schema,
   or invalid prior-record identity -> `ERROR` or `MIGRATION REQUIRED`; verdict
   is null.
2. Any required dependency, denominator, required consultation, mutation guard,
   or assertion evaluation incomplete -> `PARTIAL`.
3. Any open `MAJOR` finding -> `MAJOR REVISION NEEDED`.
4. Otherwise any open `BLOCKING` finding -> `NEEDS REVISION`.
5. Otherwise -> `APPROVED`; advisory findings may remain.

`APPROVED` requires all required assertions evaluated, every required dependency
current, complete requirement coverage, no unresolved evidence conflict, and no
open blocking or major finding. Accepted-risk references never change this rule.

## Return evidence

For one target, return one `cgs.review-evidence/v1` envelope with a
`cgs.ux-review/v2` extension exactly as defined in the rules reference. Include
the target hash, author schema hash, author contract manifest hash, profile,
profile/content versions and support status, complete
dependency and requirement ledgers, assertion states, stable findings,
consultation state, convergence data, verdict, and gate-evidence status.

For selectors, return one independent review envelope per checked target plus one
`cgs.ux-review-batch/v1` summary. The batch summary has a run status but no
aggregate approval verdict. A per-target verdict cannot approve another target.
If a limit is reached, list every unreviewed manifest entry as `UNCHECKED` and
mark the batch `PARTIAL`.

Always state:

```text
gate_evidence_status: NOT_PERSISTED
gate_evidence_eligible: false
```

because this skill never writes the record. A recorder may persist only after
rechecking the target, author schema, dependencies, and record ID against the
same exact bytes.

## Completion guarantee

A review is complete only when target discovery is bounded and explicit, every
eligible target has either its own complete record or an `UNCHECKED` entry, every
required assertion has one state, every evidence claim is hash-bound, prior open
findings are reconciled when requested, and the mutation guard proves that no
input or project file changed during the run.
