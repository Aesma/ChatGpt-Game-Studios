---
name: art-bible
description: "Author a versioned nine-section Art Bible through explicit user decisions and skeleton-first persistence. Partial drafts never receive whole-document approval; asset production remains blocked until an independent art-director review record approves the current complete artifact hash."
---

## Invocation and execution

Invoke this workflow as `$art-bible [--scope full|core|asset-standards|resume] [--review full|lean|solo]`.

Before the first file change, present the complete exact changeset with every
path, operation, owner, and current SHA-256/ABSENT state. Use existing bounded
authorization only when it already covers that exact set. Otherwise obtain one
approval. A new path or operation requires a revised preview and new approval;
section decisions never broaden file authorization.

# Art Bible

This workflow authors `design/art/art-bible.md`. It may create/update a separate
authoring state file and, when eligible and exactly authorized, an immutable
review record. It never creates production assets or implementation files.

The author and whole-document reviewer must be separate identities. The reviewer
must be a fresh `art-director` Codex subagent that did not author, draft, revise,
or approve sections in this run. The reviewer may read the artifact and write
only its exact immutable review-record path; it never edits the Art Bible.

## Production safety invariant

Asset specification, generation, import, implementation, outsourcing, and
production are **BLOCKED** unless all are true:

1. the Art Bible uses schema `AB-1`;
2. all nine required sections are `COMPLETE`;
3. an independent `art-director` returned `APPROVE` through `AD-ART-BIBLE`;
4. the immutable review record names the current raw-byte Art Bible SHA-256; and
5. the current raw-byte hash still equals that approved hash.

User acceptance of risk, a section review, a partial scope completion, a
`CONCERNS` verdict, or a status written inside the Art Bible cannot replace this
gate.

---

## Canonical schema AB-1

Section identity is the stable ID, never the display title.

| ID | Display title | Required coverage |
|---|---|---|
| `AB-01` | Visual Identity Statement | one-line rule, principles, pillar tests |
| `AB-02` | Mood, Lighting & Atmosphere | state-based emotion, lighting, atmosphere |
| `AB-03` | Shape, Composition & Silhouette | character/environment/UI geometry and readability |
| `AB-04` | Color System & Accessibility | palette roles, semantics, area rules, backup cues |
| `AB-05` | Typography & Iconography | hierarchy, type personality, icons, legibility |
| `AB-06` | Character Art Direction | archetypes, silhouettes, pose/expression, camera/LOD |
| `AB-07` | Environment & Level Art Direction | architecture, materials, density, storytelling |
| `AB-08` | UI/HUD & VFX Visual Language | HUD presentation, motion, effects, readability |
| `AB-09` | Asset Standards, References & Prohibitions | budgets, formats, naming, references, avoid rules |

The document header contains:

```markdown
# Art Bible

> Schema: AB-1
> Artifact Status: DRAFT | PARTIAL | COMPLETE
> Production Use: BLOCKED — independent current-hash approval required
```

Do not write `APPROVED`, a reviewer signature, or an approval date into this
header. Whole-document approval lives only in external review evidence.

Section state is tracked externally as one of:

- `EMPTY` — skeleton only;
- `INCOMPLETE` — some required fields exist;
- `COMPLETE` — every AB-1 assertion is satisfied and user approved its decisions;
- `INVALID` — contradictory or malformed content;
- `STALE` — dependencies or constraints changed.

`SECTION REVIEWED` is review metadata, not whole-document approval.

---

## Phase 0: Resolve mode and bounded context

Resolve review mode once:

1. explicit `--review full|lean|solo`;
2. otherwise the configured project review mode;
3. otherwise `lean`.

Mode behavior:

- `full` — after a complete draft, use one fresh independent `art-director` for
  `AD-ART-BIBLE`.
- `lean` — no whole-document director review; document may become COMPLETE but
  remains UNREVIEWED and production-blocked.
- `solo` — spawn no director agents. Author locally with the user; document may
  become COMPLETE but remains UNREVIEWED and production-blocked.

Authoring is not sign-off. No identity that drafted or revised a section may be
selected as the whole reviewer.

Read the game concept and any approval evidence that exists. Record their current
raw-byte hashes. A missing or unapproved concept permits only `DRAFT/PARTIAL`
authoring; it never permits production approval. Do not claim an upstream concept
is approved merely because its file exists.

Read technical preferences and engine/platform constraints when available.
Without configured platform/engine budgets, AB-09 asset standards must be marked
`PROVISIONAL` and therefore not COMPLETE.

---

## Phase 1: Detect schema and protect existing content

If `design/art/art-bible.md` does not exist, use fresh mode.

If it exists:

1. read it in full and hash its current raw bytes;
2. inspect the explicit schema marker and stable section IDs;
3. inventory every section and byte range;
4. compare external state/review evidence with current hashes;
5. never infer identity or completeness from a title alone.

### Current AB-1 document

For each `AB-01` through `AB-09`, evaluate all required coverage and report
`EMPTY/INCOMPLETE/COMPLETE/INVALID/STALE` with evidence. Preserve content outside
the selected section byte ranges.

If a prior review record's artifact hash differs from current bytes, mark review
`STALE` immediately and set Production Use to BLOCKED in the proposed next
authoring update. Never carry approval forward by title or filename.

### Legacy or unknown schema

A file without `Schema: AB-1`, with old headings, duplicate IDs, missing IDs, or
unknown headings is a migration candidate. Do not insert the new skeleton over it
and do not overwrite or discard legacy content.

Create a read-only migration proposal:

```markdown
| Legacy byte range/title | Proposed AB-1 ID(s) | Action | Ambiguity | Preserved source |
|---|---|---|---|---|
```

Old sections that combine or split new concerns may map to multiple AB-1 IDs.
Unknown content remains `UNMAPPED`. Show the exact before/after diff, including
where every original byte will go. Ask the user to approve or correct mappings.

Only after the exact migration paths and operation are authorized may the Art
Bible be rewritten to AB-1. If any mapping is unresolved, keep the document
legacy, report BLOCKED for approval, and make no migration write.

A migration never establishes section completeness or whole approval by itself.
Re-evaluate every migrated AB-1 section from content assertions.

---

## Phase 2: Select scope and authorize exact files

Ask which sections to author:

- `full` — all nine;
- `core` — AB-01 through AB-04;
- `asset-standards` — AB-09 only;
- `resume` — user selects from non-complete AB-1 sections.

Scope controls authoring work only. It does not redefine the required nine-section
schema and never makes a subset eligible for whole approval.

Ask for reference sources and record exactly which elements are useful and which
must not be copied. References never authorize imitation of a living artist or
unlicensed production use.

### Authoring changeset

Before the first write, preview exact rows:

```markdown
| Path | Operation | Owner | Base SHA-256/ABSENT | Purpose |
|---|---|---|---|---|
| design/art/art-bible.md | create/update | authoring-owner | ... | AB-1 skeleton and approved sections |
| production/session-state/art-bible.yaml | create/update | authoring-owner | ... | section/decision/hash checkpoint |
```

The review record is a separate side effect. If `full` mode and full scope make a
review likely, preallocate a unique review ID and exact path such as
`design/art/reviews/ABR-<run-id>.md` and include its `create` row with owner
`independent-art-director-reviewer`. Otherwise, when a later run becomes eligible,
preview and authorize that exact new record path before review. Never authorize a
review directory or wildcard.

File authorization and product approval are different:

- changeset approval authorizes exact writes to listed paths;
- each section's substantive visual decisions still require explicit user choice;
- a section choice within the authorized paths does not require another file
  permission prompt;
- a new path, owner, or operation does.

---

## Phase 3: Create or normalize the full skeleton first

After authorization, re-read every target and verify base hashes/absence. On a
mismatch, write nothing and report `BLOCKED — CONCURRENT CHANGE`.

For a fresh file, create the complete AB-1 header and all nine section headings
in one skeleton write before adding any section body. Unselected sections receive
a neutral `[Not authored]` marker. Create the state file in the same authorized
changeset.

For an authorized legacy migration, write the complete AB-1 structure while
preserving the user-approved mapping and all unmapped content in a clearly marked
migration appendix. Do not mix migration and newly invented section content in
the same write.

The state file records:

```yaml
schema: AB-1
run_id: ...
artifact_path: design/art/art-bible.md
artifact_sha256: ...
artifact_status: DRAFT | PARTIAL | COMPLETE
review_status: NOT_ELIGIBLE | UNREVIEWED | APPROVED | CONCERNS | REJECTED | STALE
approved_artifact_sha256: null
sections:
  AB-01:
    status: EMPTY | INCOMPLETE | COMPLETE | INVALID | STALE
    section_sha256: ...
    decision_ids: []
    author_id: ...
    section_review: UNREVIEWED | SECTION_REVIEWED
selected_scope: [...]
concept: { path: ..., sha256: ..., approval: ... }
constraints: { paths_and_hashes: [...] }
review_record: { id: ..., path: ..., sha256: null }
next_safe_step: ...
```

The raw Art Bible hash is stored only in external state/evidence. Do not insert
its hash into the Art Bible and create a self-referential value.

---

## Phase 4: Author selected sections

Process one selected section at a time. For every substantive visual decision:

1. ask a focused question;
2. provide two or three meaningful options with tradeoffs;
3. let the user decide;
4. draft only from approved concept constraints and that decision;
5. show the complete proposed section;
6. obtain explicit section-content approval;
7. verify the Art Bible base hash;
8. replace only that section's stable-ID byte range;
9. recompute Art Bible and section raw-byte hashes;
10. update the state checkpoint within the already authorized paths.

A user-approved product decision is evidence, not new filesystem authority.

The current agent is the author. It may consult `ux-designer` for AB-05/AB-08
and `technical-artist` for AB-09. Consultants return read-only proposals. In full
mode, reserve the future whole-document `art-director` reviewer identity; never
use that same identity to draft or revise sections.

If a consultant fails, times out, or returns partial content, record the section
`INCOMPLETE` and produce a partial report. Do not fabricate its analysis or mark
the section COMPLETE.

### Section-specific constraints

- AB-04 must define non-color backup cues for every semantic use that cannot rely
  on color alone.
- AB-05 must include measurable hierarchy/legibility rules, not only font names.
- AB-08 must surface art-versus-UX readability conflicts to the user; the model
  cannot silently choose a product tradeoff.
- AB-09 must distinguish hard technical budgets from art preferences. Hard
  configured constraints win automatically; product-facing visual tradeoffs
  require user choice. Without configured engine/platform budgets, it remains
  PROVISIONAL/INCOMPLETE.
- AB-09 references identify specific reusable elements and explicit divergence;
  they are not prompts to copy a source's general style.

After every write, verify that only the selected section and state file changed.
An unexpected byte change outside the approved range is BLOCKED; do not continue
or overwrite it.

---

## Phase 5: Compute artifact status

Re-evaluate all nine stable IDs, including unselected sections.

- `DRAFT` — skeleton exists and no section is complete.
- `PARTIAL` — at least one but fewer than nine sections is COMPLETE, or any
  section is INCOMPLETE/INVALID/STALE/PROVISIONAL.
- `COMPLETE` — all nine sections satisfy AB-1 assertions, all decisions are
  approved, and no section is invalid, stale, provisional, or unmapped.

A scoped run that finishes all selected sections remains PARTIAL unless every
AB-1 section is COMPLETE.

Update only `Artifact Status: DRAFT/PARTIAL/COMPLETE` and
`Production Use: BLOCKED — independent current-hash approval required` in the
Art Bible. Update external state with the resulting raw-byte artifact hash.
Never write whole-document APPROVED into the artifact.

A section-level check may record `SECTION REVIEWED` for its exact section hash,
but it cannot promote artifact review status.

---

## Phase 6: Independent whole-document review

Review is eligible only when:

- artifact status is COMPLETE;
- schema is exactly AB-1 with all nine unique IDs;
- no migration ambiguity, provisional constraint, or stale dependency remains;
- review mode is full;
- the exact immutable record path is authorized and still ABSENT; and
- the selected reviewer identity did not author, draft, revise, or approve any
  section.

Otherwise skip formal review, report the specific reason, and keep production
blocked. A PARTIAL artifact never invokes AD-ART-BIBLE for whole approval. Scope
completion alone never establishes eligibility; a scoped or resume run may proceed
only when all nine current sections independently re-evaluate COMPLETE.

Spawn a fresh `art-director` through Codex subagent delegation using
`AD-ART-BIBLE`. Do not spawn `creative-director` for this gate.

Pass only review evidence:

- exact Art Bible path and current raw-byte SHA-256;
- AB-1 section manifest and section hashes;
- current concept/pillar/constraint paths and hashes;
- decision provenance;
- author identities; and
- explicit instruction to remain artifact-read-only and write only the authorized
  immutable review record.

The reviewer must:

1. independently re-read the complete Art Bible;
2. recompute the raw-byte hash before review;
3. verify all nine sections and cross-section consistency;
4. return `APPROVE`, `CONCERNS`, or `REJECT`;
5. re-hash the artifact before recording the verdict; and
6. emit no formal verdict if either hash differs from the supplied current hash.

The immutable record contains:

```yaml
review_id: ABR-...
gate: AD-ART-BIBLE
reviewer_role: art-director
reviewer_id: ...
author_ids: [...]
separation_verified: true
artifact_path: design/art/art-bible.md
artifact_sha256: sha256:...
schema: AB-1
artifact_status: COMPLETE
section_hashes: {...}
dependency_hashes: {...}
verdict: APPROVE | CONCERNS | REJECT
findings: [...]
reviewed_at: ...
```

The reviewer creates the record once and never edits the Art Bible. If the record
path already exists, generate a new review ID/path and obtain authorization; do
not overwrite immutable evidence.

Only `APPROVE` sets external state to `review_status: APPROVED` and
`approved_artifact_sha256: <current hash>`. After independently verifying the
immutable record and current artifact hash, the already-authorized authoring owner
may write this mechanical state projection; it cannot alter the reviewer verdict,
review record, or Art Bible. `CONCERNS` and `REJECT` remain
production-blocking. User acceptance of concerns does not convert the verdict.

Do not add a sign-off line to the Art Bible after review; that would change the
reviewed bytes. The external state and immutable record are the only approval
projection.

---

## Phase 7: Current-hash verification and close

Immediately before reporting approval or recommending asset work:

1. re-read and hash the Art Bible;
2. re-read and hash the immutable review record;
3. verify reviewer/author separation;
4. verify the record verdict is APPROVE;
5. verify its artifact hash equals current bytes;
6. verify schema/status/nine section hashes and dependencies remain current.

If any check fails, report `REVIEW STALE/INVALID — PRODUCTION BLOCKED` and update
the authorized state file to STALE when possible. Never claim the document is
approved from an older record.

Verdicts:

- `DRAFT` — skeleton only; production blocked.
- `PARTIAL` — incomplete scoped/full content; production blocked.
- `COMPLETE — UNREVIEWED` — nine sections complete without current approval;
  production blocked.
- `COMPLETE — CONCERNS/REJECTED` — reviewed but not approved; production blocked.
- `APPROVED` — independent APPROVE record matches the current complete hash;
  production may use this Art Bible subject to other project gates.
- `BLOCKED` — migration, conflict, evidence, authorization, or dependency prevents
  safe progress.

The final report lists exact artifact/state/review paths, current hashes, section
states, author/reviewer IDs, approval record, production-use decision, preserved
legacy content, and the next safe handoff. Do not automatically invoke asset
production or implementation workflows.

---

## Resume and authorization safety

On resume, read the Art Bible and state in full, recompute every hash, and compare
them with the checkpoint. Never trust state over current bytes.

- matching hashes → continue at `next_safe_step`;
- changed selected section → show diff and require user decision;
- changed unselected section or unknown bytes → BLOCKED;
- changed approved artifact → mark approval STALE before further claims;
- new output path → revised changeset preview and authorization.

Existing bounded authorization applies only to its exact paths/operations.
Delegation, review, resume, or user acceptance never expands it.
