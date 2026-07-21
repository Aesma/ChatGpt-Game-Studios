---
name: create-architecture
description: "Authors a versioned DRAFT master architecture as a derived view of Accepted ADRs and confirmed design requirements. Supports new, resume, focus, and read-only audit profiles; preserves requirement provenance, records unresolved decisions without making them binding, and requires an independent current-hash architecture review plus a separate recorder before READY status."
---

## Invocation and execution

Invoke this workflow as `$create-architecture`.

Arguments:

`[profile: new | resume | focus | audit] [focus-area: layers | ownership | data-flow | api-boundaries | decision-ledger | requirements] [--review full | lean | solo]`

If no profile is supplied, inspect `docs/architecture/architecture.md`:

- Missing file → recommend `new`.
- Existing file → recommend `resume`; never overwrite it implicitly.

`focus` requires one `focus-area`. `audit` is strictly read-only. Resolve review
mode once: explicit `--review`, then `production/review-mode.txt`, otherwise
`lean`.

Before the first write, use any existing bounded task authorization. Otherwise,
preview the complete changeset (including the architecture skeleton and session
checkpoint) and obtain one explicit approval. Once authorized, persist approved
sections without asking again for each write. Ask again only if file scope expands.

This workflow may delegate authoring research to `technical-director`, but the
authoring agent and every authoring subagent are members of the **author side**.
They cannot review, approve, sign, or promote their own artifact.

# Create Architecture

This workflow authors `docs/architecture/architecture.md`. The artifact is a
versioned architecture view, not a second source of technical truth.

## Non-negotiable authority model

1. **Accepted ADRs own binding technical decisions.** Engine/API choices, module
   ownership, cross-module contracts, data-flow mechanisms, threading models,
   persistence formats, and similar choices are binding only when an Accepted ADR
   owns them.
2. **The master architecture is derived.** It aggregates the current results of
   Accepted ADRs and links each binding statement to its ADR ID, status, and source
   hash. It may also contain clearly marked non-binding proposals and decision gaps.
3. **A proposal is not permission to implement.** A section lacking an Accepted
   ADR uses a stable `DECISION-*` ID, is labeled `NON-BINDING PROPOSAL`, and names
   the ADR needed to resolve it.
4. **The author never self-signs.** User approval authorizes content and file
   mutation; it does not constitute technical review or READY status.
5. **READY is recorded, not authored.** A fresh independent `$architecture-review`
   must review the exact current artifact hash. A recorder who is neither author
   nor reviewer may promote the document only after validating the record and all
   other READY conditions.

## Status and verdict vocabulary

Architecture artifact status is exactly one of:

- `DRAFT` — usable for discussion; not an implementation authority.
- `PARTIAL` — interrupted, input-incomplete, or review-incomplete draft.
- `READY` — independently reviewed at the current hash and derived only from
  Accepted ADRs for every binding/blocking decision.

Independent review verdict is exactly one of `PASS`, `CONCERNS`, or `FAIL`.
Only `PASS` is eligible for READY. The author must never write an approval,
technical-director sign-off, or equivalent endorsement into the architecture.

## Profile contract

| Profile | Preconditions | Allowed architecture mutation | Review behavior |
|---|---|---|---|
| `new` | Architecture file does not exist | Create the complete skeleton, then fill authorized sections incrementally | Review the completed DRAFT according to review mode |
| `resume` | Existing DRAFT/PARTIAL file | Fill incomplete sections and update explicitly selected stale derived content; preserve all other bytes | Review only after the requested draft scope is complete |
| `focus` | Existing file and one focus area | Change only the selected section plus Document Status/provenance fields required by that change | Review the resulting whole-file hash if promotion is requested |
| `audit` | Existing file | None: no architecture, review record, ADR, catalog, or session-state writes | Report findings inline; never change status |

If a profile precondition fails, stop and offer valid profiles. Do not silently
convert profiles or rewrite an existing document.

---

## Phase 0: Establish the run boundary

1. Resolve the profile, focus area, review mode, target path, and current target
   hash (or `ABSENT`).
2. Enumerate the inputs needed for the selected profile. Do not treat every file
   in a directory as approved merely because it exists.
3. For `resume` and `focus`, read the existing document completely and record its
   starting hash. Identify the exact sections eligible for mutation.
4. For `audit`, declare the run read-only and skip all later write steps.
5. Present the complete proposed changeset once when authorization is not already
   present.

If the target changes after its starting hash is recorded, stop with `PARTIAL —
CONCURRENT CHANGE`; do not overwrite the newer content.

---

## Phase 1: Build an approved input manifest

Read the pinned engine version and only the design/engine sources needed by the
selected profile. For every design input, record:

| Field | Required value |
|---|---|
| Path | Repository-relative path |
| Approval state | `APPROVED`, `PROVISIONAL`, or `UNKNOWN` from explicit artifact evidence |
| Source revision | Source-declared revision when present |
| SHA-256 | Hash of the exact bytes consumed |
| Scope | Sections used by this run |

Only `APPROVED` inputs may support READY. `PROVISIONAL` or `UNKNOWN` inputs may be
used for a DRAFT, but must be listed as blockers. Never infer approval from a
filename, directory, or conversational description.

Read the relevant engine reference provenance: engine/version, reference date,
coverage, and missing or stale domains. An unsupported engine claim remains
`UNVERIFIED` and cannot be represented as confirmed.

### Technical requirement classification

Extract requirements into two separate collections:

#### A. Requirements baseline

The baseline contains only:

- `EXPLICIT_REQUIREMENT`: a normative statement present in an approved source; or
- `CONFIRMED_REQUIREMENT`: a former inference explicitly confirmed by the user or
  named technical owner during this run.

Each row must preserve:

| Requirement ID | Class | Requirement | Source path | Source locator | Source excerpt | Source SHA-256 | Confirmation evidence | Domain |
|---|---|---|---|---|---|---|---|---|

Prefer a source-owned requirement ID. If none exists, derive a stable ID from the
source path, locator, and normalized statement fingerprint; do not renumber other
requirements when a source is edited.

#### B. Inferred candidates

Anything implied rather than stated is an `INFERRED_CANDIDATE`. Keep candidates in
a visibly separate table with rationale and source provenance. Candidates:

- do not enter the baseline;
- do not count toward coverage;
- do not create binding ADR obligations;
- do not appear as facts in the architecture; and
- become baseline requirements only after explicit confirmation is recorded.

Present each candidate requiring a product or technical choice with 2–3 meaningful
options and tradeoffs. If confirmation is unavailable, leave it as a candidate and
continue only as DRAFT/PARTIAL. Never call the extracted set "complete" merely
because all available files were scanned.

---

## Phase 2: Build the ADR-derived decision ledger

Read the in-scope ADR headers and relevant decision sections. For each ADR record:

| ADR ID | Title | Status | ADR SHA-256 | Requirements | Architecture sections | Binding? |
|---|---|---|---|---|---|---|

- `Accepted` → binding and eligible to populate the derived architecture view.
- `Proposed`, `Superseded`, `Rejected`, missing, or ambiguous → not binding.

Detect stale links by comparing stored ADR hashes with current bytes. Never resolve
a conflict by choosing a winner in the architecture document. Create or retain a
`DECISION-*` gap describing the conflict and route resolution to
`$architecture-decision`.

For every planned statement in Layers, Module Ownership, Data Flow, or API
Boundaries, classify it before writing:

- `DERIVED — ADR-NNNN@<hash>` for an Accepted ADR result; or
- `NON-BINDING PROPOSAL — DECISION-<stable-id>` when no Accepted ADR owns it.

The second classification cannot be presented as a contract programmers may
implement against.

---

## Phase 3: Create or validate the skeleton

In `new`, create the complete skeleton immediately after changeset authorization,
before inserting section content. In `resume` or `focus`, validate that the required
headers exist; add missing headers only when they are inside the authorized mutation
scope. The skeleton is:

```markdown
# [Game Name] — Master Architecture

## Document Status
- Schema Version: 2
- Artifact Revision: 1
- Status: DRAFT
- Artifact Hash: PENDING UNTIL WRITE
- Input Manifest Hash: [hash]
- Last Independent Review: NONE

## Input Manifest

## Technical Requirements Baseline

## Inferred Candidates (Non-Binding)

## Decision Ledger

## System Layer Map

## Module Ownership

## Data Flow

## API Boundaries

## Engine Knowledge and Verification

## Required ADRs

## Architecture Principles

## Open Questions and Blockers

## Revision History
```

After the skeleton write, compute its hash and checkpoint
`production/session-state/active.md` with profile, target, current status, completed
sections, next section, input manifest hash, and open blockers. Session state is a
recovery aid and never a review or approval record.

---

## Phase 4: Author sections incrementally

For each in-scope section:

1. Load only the manifest entries, baseline requirements, and ADR ledger rows needed
   for that section.
2. Show the proposed section. Binding lines cite Accepted ADR IDs/hashes. Unresolved
   choices show a `DECISION-*` ID, 2–3 options with tradeoffs, and the owner needed
   to decide.
3. Obtain the user's content decision. This is a design decision, not another file
   authorization.
4. Recheck the target hash, write only that section, recompute the hash, and update
   the recovery checkpoint.

Section-specific rules:

- **System Layer Map:** derive layer placements from Accepted ADRs; otherwise show
  a non-binding proposed placement.
- **Module Ownership:** only an Accepted ADR may establish exclusive ownership,
  exposed state, or dependency direction.
- **Data Flow:** only an Accepted ADR may establish the communication mechanism,
  thread boundary, initialization order, or persistence authority.
- **API Boundaries:** only an Accepted ADR may establish public interfaces or
  engine-specific types/signatures. Pseudocode without such an ADR is illustrative
  and labeled non-binding.
- **Required ADRs:** list decision gaps and the baseline requirement IDs they block;
  do not pre-decide the ADR outcome in its title or proposed architecture text.

`resume` must leave completed, current sections unchanged unless the user explicitly
selected them. `focus` must leave every non-target section byte-for-byte unchanged,
except the minimal Document Status, provenance, and Revision History fields required
to disclose the change. `audit` skips this phase.

---

## Phase 5: Finalize the author-side draft

Recompute coverage using baseline requirements only. Report separately:

- requirements linked to Accepted ADRs;
- requirements with unresolved `DECISION-*` gaps;
- confirmed requirements with no architecture mapping;
- inferred candidates awaiting confirmation;
- Proposed or stale ADR dependencies; and
- unverified engine claims.

Set author-side status:

- `PARTIAL` if the run was interrupted, an authorized section is unfinished, an
  input is missing, a concurrent change occurred, or a requested reviewer failed.
- otherwise `DRAFT`.

The author may never set `READY`. Compute the exact SHA-256 of the completed draft
bytes and expose it as `reviewed_artifact_hash` for the next phase. Because embedding
a file's own hash changes its bytes, the Document Status field stores the hash of
the canonical review payload defined as the UTF-8 document with the `Artifact Hash`
value replaced by `PENDING`; the external review record stores both that canonical
hash and the repository blob hash when available.

---

## Phase 6: Independent review and recording

`audit` skips this phase. Review work must use a fresh context that did not author
or edit the artifact.

### Review-mode behavior

- `full`: dispatch independent `$architecture-review` and `lead-programmer`
  feasibility review concurrently against the same immutable artifact hash. Wait
  for both; the LP result is advisory and cannot promote the artifact.
- `lean`: dispatch only independent `$architecture-review`. Record
  `LP feasibility skipped — lean mode`.
- `solo`: do not simulate independence in the current context. Record
  `Independent architecture review not run — solo mode`; leave the artifact DRAFT.

If independent delegation is unavailable, times out, becomes blocked, or reads a
different hash, report the exact condition and leave the artifact `PARTIAL` or
`DRAFT`. Never replace a missing independent review with author-side reasoning.

The independent reviewer, not the author, writes:

`docs/architecture/reviews/architecture-review-<canonical-hash-prefix>.md`

The record must contain reviewer identity/context, timestamp, architecture path,
canonical reviewed hash, repository blob hash when available, input manifest hash,
review method, `PASS|CONCERNS|FAIL`, findings, and any required remediation. A record
for any other hash is stale.

### Separate recorder promotion

A recorder who is neither author nor reviewer may change status to READY only when:

- the current canonical artifact hash exactly matches a fresh independent record;
- the independent verdict is `PASS`;
- every source needed for readiness is APPROVED at the recorded hash;
- every binding or blocking technical decision is owned by a current Accepted ADR;
- there are no blocking open questions, stale ADR links, or unverified binding
  engine claims; and
- any required full-mode feasibility result has completed without a blocking issue.

The recorder records only status, review-record path/hash, timestamp, and revision
history. The recorder does not rewrite technical content. Any later content change
returns the artifact to DRAFT and invalidates the old review record for promotion.

---

## Phase 7: Handoff

Never output `Architecture Complete` for a DRAFT or PARTIAL artifact. Report:

```markdown
## Architecture Draft Saved

- Path: `docs/architecture/architecture.md`
- Status: DRAFT | PARTIAL | READY
- Canonical artifact hash: [hash]
- Input manifest hash: [hash]
- Independent review: [current record path and verdict | NOT RUN | STALE | FAILED]
- Binding source: Accepted ADRs only

## Blocking Decisions

| Decision ID | Baseline requirements | Reason | Resolution owner |
|---|---|---|---|

## Highest-Priority Next Action

[One action only: confirm an inferred candidate, create/accept one ADR, run an
independent review, or address one review finding.]

## Gate Readiness

Do not claim a phase gate is ready from this workflow. State which evidence exists
and direct `$gate-check [stage]` to verify the catalog-defined artifacts. A current-
hash independent review record is required evidence; author text is not evidence.
```

Update session state after the last successful write. Do not automatically run a
chain of ADR workflows, a gate, or another skill.

---

## Failure and recovery rules

- Missing/unapproved source → preserve provenance, mark blocker, remain DRAFT/PARTIAL.
- Missing/stale engine reference → mark claims UNVERIFIED; never present them as
  confirmed API facts.
- Proposed ADR → show as non-binding and block READY when required.
- Reviewer unavailable/timeout/blocked → preserve draft and report review not
  completed; never self-review.
- Hash mismatch before a write → stop without overwriting and report concurrent
  change.
- Hash mismatch after review → mark the record stale and require a fresh review.
- Resume after interruption from the on-disk document and checkpoint; do not infer
  missing decisions from conversation memory.

## Static safety guards

- No author-side approval or sign-off fields.
- No inferred candidate in the requirements baseline without confirmation evidence.
- No binding architecture statement without a current Accepted ADR citation.
- No READY transition without an independent current-hash PASS record and separate
  recorder.
- No whole-document rewrite in `focus` or `audit`.
- No mutation of any kind in `audit`.
