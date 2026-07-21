---
name: help
description: Provide one evidence-backed next-step recommendation from a complete current project-stage packet without inferring stages, treating artifact presence, user claims, and detector output as gate approval.
---

# Studio Help

Provide concise, read-only orientation without allowing an artifact, status string, user claim, or stage diagnosis to substitute for a required approval or gate receipt.

This workflow recommends one primary next action. It never writes files, invokes a skill, spawns a reviewer, changes project state, or decides that a gate passed.

## Invocation

`$help [question-or-recent-activity]`

The optional argument is context only. Statements such as “I finished design-review” are claims to investigate, not completion evidence.

## Hard boundaries

1. **Read-only:** do not create, edit, migrate, approve, or register anything.
2. **One primary action:** return one safest next action, with secondary context only when useful.
3. **No local stage inference:** do not inspect artifact counts, source-file counts, directory names, `stage.txt`, sprint status, or user prose to derive a phase.
4. **Detector is not a gate:** `project_stage_detection/v2` provides diagnostic stage context only. Its stage, confidence, status, evidence, or recommendation never counts as workflow approval.
5. **Existence is not completion:** a matching file or status record is never `VERIFIED_PASS` by itself.
6. **Claims are not receipts:** user prose and session notes remain `CLAIMED` until current evidence verifies them.
7. **No unsafe advance:** never recommend a later required step or phase when an earlier required prerequisite is not `VERIFIED_PASS` under its catalog-declared completion policy.

## Consume project stage only from project_stage_detection/v2

The sole source of phase selection is one complete, current packet conforming to the producer-owned `project_stage_detection/v2` schema.

Do not copy, summarize into executable rules, or reconstruct the detector’s phase heuristics. Validate against the producer schema itself; do not maintain a local list of required packet fields.

### Complete packet

A packet is complete only when:

- its schema identifier is exactly `project_stage_detection/v2`;
- validation against that schema succeeds with no missing, truncated, omitted, or partial required section;
- it identifies the project and packet;
- it contains the detector’s stage result, confidence, evidence, conflicts, unknowns, and read-error sections required by the schema;
- it contains a snapshot/source manifest with content hashes or explicit absence markers;
- it identifies the workflow-catalog version/hash used by the detector;
- its completion marker is the schema-defined complete value.

Do not consume individual fields from an invalid or partial packet. A producer verdict named `PASS`, `COMPLETE`, or similar does not relax schema validation.

### Current packet

A schema-valid packet is current only when:

- its project identity matches the current project;
- every path in its declared source manifest can be checked;
- each current content hash or absence state matches the packet;
- the current workflow catalog matches the packet’s declared catalog identity/hash;
- no required source check has an access error;
- no newer valid packet for the same project/snapshot lineage supersedes it.

Timestamp age alone neither proves nor disproves currentness. Any source drift, catalog drift, project mismatch, supersession, or uncheckable required source makes the packet `STALE` or `UNKNOWN`.

Use the validated packet’s stage result exactly as produced. If its conflict/unknown/read-error sections say stage selection is unresolved, do not choose a normal phase step; issue a diagnostic recommendation.

### Packet failure behavior

- Missing packet: `STAGE_CONTEXT_MISSING`.
- Wrong schema or incomplete packet: `STAGE_PACKET_INVALID`.
- Source/catalog drift: `STAGE_PACKET_STALE`.
- Unresolved stage conflict or required read error: `STAGE_CONTEXT_CONFLICT`.

For all four, do not fall back to local heuristics. Recommend obtaining or refreshing the diagnostic packet, but do not run `project-stage-detect` automatically.

## Workflow catalog use

Read the workflow catalog whose identity/hash is bound to the current packet. Use it only for:

- ordered steps in the packet-selected phase;
- required/optional/repeatable flags;
- command or manual-action labels;
- the completion policy and receipt schema declared for each step;
- prerequisite relationships and phase-transition rules.

Do not use catalog artifact globs as proof of completion. They may locate evidence, but a match begins at `PRESENT_UNVERIFIED`.

If the catalog is unavailable, malformed, hash-mismatched, or lacks a completion policy needed for a required step, return a diagnostic recommendation. Do not invent a policy.

## Evidence states

Classify every relevant prerequisite into exactly one progress state while retaining all evidence records:

| State | Meaning | May satisfy a required prerequisite? |
|---|---|---|
| `VERIFIED_PASS` | A current evidence bundle satisfies the catalog-declared completion policy; every required approval/gate receipt has verdict `PASS` and matches current sources/artifacts | Yes |
| `CLAIMED` | User, session note, or unverified status source says the work is done | No |
| `PRESENT_UNVERIFIED` | An artifact or record exists, but no valid current completion evidence proves it | No |
| `STALE` | Receipt or artifact was valid for different source, artifact, catalog, or run hashes | No |
| `BLOCKED` | Current authoritative receipt says `BLOCKED`, `FAIL`, `REJECTED`, or equivalent non-pass | No |
| `MISSING` | Required artifact/evidence/receipt is absent | No |
| `CONTRADICTORY` | Current evidence sources disagree in a way that affects completion | No |
| `UNKNOWN` | Required evidence could not be read or interpreted safely | No |

Never display `CLAIMED`, `PRESENT_UNVERIFIED`, or a detector conclusion with a completed/checkmark symbol.

### Deterministic precedence

For one prerequisite:

1. conflicting current authoritative receipts → `CONTRADICTORY`;
2. one current authoritative negative receipt with no conflicting current receipt → `BLOCKED`;
3. one valid current `PASS` evidence bundle with no conflict → `VERIFIED_PASS`;
4. only mismatched/outdated evidence → `STALE`;
5. no valid receipt plus a user/session/status assertion → `CLAIMED`;
6. no claim plus an artifact/status file that merely exists → `PRESENT_UNVERIFIED`;
7. confirmed absence → `MISSING`;
8. access, schema, or interpretation failure → `UNKNOWN`.

When multiple non-authoritative signals exist, list all of them; do not upgrade the state.

## Completion evidence

For a required step, validate the exact completion policy declared by the packet-bound catalog. When approval or a gate is required, `VERIFIED_PASS` requires a receipt that binds at least:

- receipt and run identity;
- catalog step and gate/approval identity;
- explicit `PASS` verdict;
- authorized approver/authority evidence required by policy;
- subject artifact identities and content hashes;
- input/source snapshot hashes;
- catalog identity/hash;
- issue time and any expiry/supersession data.

Re-hash current subject artifacts and declared sources. A receipt for an older revision, a different run, changed inputs, changed artifact bytes, or a rejected/blocked verdict cannot pass.

A detector packet is not a completion receipt even if it contains the same paths or says the project is in a later stage.

For repeatable work, use the latest non-superseded run receipt that matches the current inputs and requested scope. An arbitrary same-named file, previous run, or “last completed” prose is not sufficient.

Treat `sprint-status.yaml`, session state, active task notes, and user statements as contextual claims unless the catalog completion policy explicitly declares their schema and they satisfy its current receipt requirements.

## Recommendation algorithm

1. Validate one full current `project_stage_detection/v2` packet.
2. Validate and bind the exact workflow catalog referenced by that packet.
3. Read the packet-selected phase and its ordered catalog steps without performing phase inference.
4. Gather bounded evidence for relevant required prerequisites and the user’s question.
5. Classify each prerequisite using the evidence-state contract.
6. Surface all same-level prerequisite conflicts that affect the primary action.
7. Select the first required step that is not `VERIFIED_PASS`:
   - `CLAIMED` or `PRESENT_UNVERIFIED` → recommend the catalog-declared verification/review/receipt-producing action;
   - `STALE` → recommend revalidation on current hashes;
   - `BLOCKED` → recommend resolving the recorded blocker;
   - `CONTRADICTORY` or `UNKNOWN` → recommend a diagnostic/reconciliation action;
   - `MISSING` → recommend the catalog-declared creation or completion action.
8. Recommend a later required step only when every earlier required prerequisite is `VERIFIED_PASS`.
9. Optional actions may be mentioned as secondary context only when they do not imply bypassing the primary prerequisite.
10. Never say a phase gate passed. Recommend the catalog-declared gate check when appropriate; that separate workflow owns its verdict.

If there is no safe catalog-declared command, describe the required manual verification or diagnostic action rather than inventing a command.

## Structured output

Keep the human-facing answer short, but include this evidence envelope:

- `recommendation_id`: stable hash of packet ID, packet snapshot hash, catalog hash, primary step/action, and reason codes;
- `outcome`;
- `stage_source: project_stage_detection/v2`;
- packet ID/hash and snapshot time;
- catalog version/hash;
- detector stage result and confidence, labelled `DIAGNOSTIC_ONLY`;
- one primary action and why it is safe;
- affected prerequisite and its progress state;
- evidence grouped as `verified`, `claimed`, `present_unverified`, `stale`, `blocked`, `missing`, `contradictory`, and `unknown`;
- receipt/run IDs and current source/artifact hashes used;
- conflicts or missing information;
- explicit `auto_executed: false` and `files_written: none`.

Suggested concise form:

```text
Where you are: <packet stage> (diagnostic context, not gate approval)
Primary next action: <one command or manual action>
Why: <prerequisite state and decisive evidence>
Blocked from advancing: <earlier unverified prerequisite, if any>
Evidence snapshot: <packet/catalog/source identity>
```

Only `VERIFIED_PASS` items may appear under “Verified done.” Claims must be labelled “You reported,” present artifacts “Found but unverified,” and stale/blocked/conflicting evidence plainly named.

## Outcomes

- `HELP_RECOMMENDATION_READY` — one safe catalog-backed primary action was selected from a complete current packet.
- `HELP_DIAGNOSTIC_REQUIRED` — packet/catalog/evidence is missing, stale, invalid, conflicted, blocked, or unsafe to interpret; one diagnostic/reconciliation action is recommended.
- `HELP_NO_SAFE_RECOMMENDATION` — no catalog-declared safe action can be identified; explain the missing contract.
- `HELP_READ_ERROR` — required read failed and no safe diagnostic can be grounded.

No outcome means a gate passed. Do not use `COMPLETE` or `PASS` as the help workflow’s verdict.

## Read-only verification

Before responding, confirm:

- no file was written;
- no skill or agent was invoked;
- no local stage heuristic was used;
- the packet was complete and current, or the output is diagnostic;
- artifact existence and user claims did not become `VERIFIED_PASS`;
- every skipped ordered prerequisite was `VERIFIED_PASS` on current hashes;
- exactly one primary action is present;
- the detector was not represented as a gate or approval authority.
