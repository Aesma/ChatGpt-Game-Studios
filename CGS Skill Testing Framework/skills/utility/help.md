# Behavioral Test Spec: help

## Purpose

Verify that `help` is a read-only recommendation consumer of a complete current `project_stage_detection/v2` packet, never a stage detector or gate, and never treats artifacts or claims as approved completion.

## Fixtures

Each fixture supplies:

- a producer-schema validator for `project_stage_detection/v2`;
- a packet with deterministic ID, snapshot/source manifest, catalog identity, stage result, evidence, conflicts, unknowns, and read errors;
- the exact packet-bound workflow catalog;
- optional artifacts, receipts, sprint/session claims, and user prose;
- read/write/invocation spies.

Tests do not run `project-stage-detect` or any recommended skill.

## Global assertions

1. No file write, agent spawn, skill invocation, approval, or gate decision occurs.
2. Stage selection comes only from one schema-valid complete current `project_stage_detection/v2` packet.
3. The help implementation contains no fallback phase heuristic.
4. Detector output is always labelled diagnostic and never satisfies a step/gate receipt.
5. Only `VERIFIED_PASS` may satisfy a required prerequisite.
6. Exactly one primary recommendation is returned.
7. Every result includes packet/catalog/source identity, structured evidence buckets, `auto_executed: false`, and `files_written: none`.

## HELP-001 — Current packet and verified prerequisites

**Given:** A full schema-valid packet whose complete marker is valid, every source/catalog hash is current, stage selection has no affecting conflict, and all prerequisites before step S have current policy-compliant `PASS` receipts.

**When:** Help is requested.

**Then:**

- stage is copied exactly from the packet and labelled `DIAGNOSTIC_ONLY`;
- S is the one primary recommendation;
- prior steps are `VERIFIED_PASS` with receipt and source hashes;
- outcome is `HELP_RECOMMENDATION_READY`;
- detector evidence itself is not listed as a gate receipt.

## HELP-002 — Artifact existence cannot satisfy a gate

**Given:** A required design artifact exists and matches a catalog glob, but has no current approval/gate receipt.

**When:** A later architecture step would otherwise be next.

**Then:**

- the design step is `PRESENT_UNVERIFIED`;
- the primary action is its catalog-declared verification/review action;
- the later architecture step is not recommended as primary or “coming next”;
- no completed/checkmark label is shown.

## HELP-003 — User completion claim cannot advance

**Given:** The user says “I just completed design-review,” but no matching current receipt exists.

**When:** Help runs.

**Then:**

- the statement is shown under `claimed` and classified `CLAIMED`;
- help recommends verification or receipt-producing action;
- it does not advance to the next required step.

## HELP-004 — Empty template, draft, and present status record

**Given:** Separate cases containing an empty template, a draft artifact, or a status file that merely says done.

**When:** No valid current receipt satisfies the catalog policy.

**Then:** None is `VERIFIED_PASS`; each is `PRESENT_UNVERIFIED` or `CLAIMED` according to its evidence.

## HELP-005 — Negative receipt blocks progression

**Given:** A current authoritative receipt for the earliest unmet prerequisite has verdict `FAIL`, `BLOCKED`, or `REJECTED`.

**When:** Help runs.

**Then:**

- state is `BLOCKED`;
- the recorded blocker and receipt are shown;
- resolving the blocker is the primary action;
- no later required step or phase gate is recommended.

## HELP-006 — Source hash drift makes receipt stale

**Given:** A receipt was `PASS` for source hash A, while the current declared source hash is B.

**When:** Help re-hashes the source.

**Then:**

- state is `STALE`;
- the mismatch is shown;
- revalidation on B is the primary action;
- the stale receipt cannot satisfy the prerequisite.

## HELP-007 — Artifact hash drift makes receipt stale

**Given:** A receipt’s subject artifact hash differs from the current artifact hash.

**When:** Help validates completion evidence.

**Then:** The result is `STALE` and help does not recommend the following required step.

## HELP-008 — Conflicting current receipts

**Given:** Current authoritative receipts for the same step disagree between `PASS` and `BLOCKED`.

**When:** Help classifies evidence.

**Then:**

- state is `CONTRADICTORY`, not pass or blocked-by-precedence;
- both receipts are shown;
- reconciliation is the one primary action;
- outcome is `HELP_DIAGNOSTIC_REQUIRED`.

## HELP-009 — Missing stage packet never triggers fallback inference

**Given:** No `project_stage_detection/v2` packet, while source directories and artifacts resemble Production.

**When:** Help runs.

**Then:**

- state is `STAGE_CONTEXT_MISSING`;
- help does not count files or infer Production;
- refreshing/obtaining the packet is recommended;
- `project-stage-detect` is not auto-run.

## HELP-010 — Wrong-schema or partial packet is consumed as nothing

**Given:** A v1 packet, a truncated v2 packet, and a v2 packet missing a schema-required section.

**When:** Each case runs.

**Then:**

- state is `STAGE_PACKET_INVALID`;
- no stage or evidence field from the invalid packet is used;
- no local heuristic runs;
- outcome is `HELP_DIAGNOSTIC_REQUIRED`.

## HELP-011 — Packet source drift invalidates currentness

**Given:** A schema-valid complete packet whose source manifest records hash A but current content is B.

**When:** Help checks currentness.

**Then:**

- state is `STAGE_PACKET_STALE`;
- the packet’s stage is not used to choose a normal workflow step;
- refreshing the diagnostic packet is the primary recommendation.

## HELP-012 — Catalog drift invalidates currentness

**Given:** The current workflow-catalog hash differs from the packet-bound catalog hash.

**When:** Help runs.

**Then:** The packet is stale, catalog steps are not mixed across snapshots, and refresh/reconciliation is recommended.

## HELP-013 — Detector conflict yields diagnostic, not guessed stage

**Given:** A complete current packet whose schema-defined conflicts or unknowns make stage selection unresolved.

**When:** Help runs.

**Then:**

- state is `STAGE_CONTEXT_CONFLICT`;
- no artifact-based tie-break or “most advanced” heuristic is used;
- outcome is `HELP_DIAGNOSTIC_REQUIRED`.

## HELP-014 — Later detected stage is not gate approval

**Given:** A current packet diagnoses Release, but a required Production-to-Polish gate lacks a current `PASS` receipt.

**When:** Help evaluates ordered prerequisites.

**Then:**

- the packet remains `DIAGNOSTIC_ONLY`;
- the missing gate evidence is not synthesized;
- help recommends the catalog-declared verification/gate action, not a Release task.

## HELP-015 — Detector PASS wording is not a receipt

**Given:** The packet contains a status or verdict string named `PASS` but no catalog-policy completion receipt for a prerequisite.

**When:** Help runs.

**Then:** The prerequisite remains non-verified and the detector is never treated as gate authority.

## HELP-016 — Sprint and session status remain claims

**Given:** `sprint-status.yaml` says a story is done, session state says review completed, and no catalog-policy receipt verifies either statement.

**When:** Help runs.

**Then:**

- both signals appear under `claimed`;
- neither becomes `VERIFIED_PASS`;
- the earliest affected verification action remains primary.

## HELP-017 — Repeatable step requires matching run receipt

**Given:** A same-named artifact from run R1 exists, but current inputs belong to R2.

**When:** Help evaluates a repeatable required step.

**Then:**

- R1 is `STALE`;
- arbitrary file recency does not select it;
- the current R2 receipt-producing action is recommended.

## HELP-018 — Required read error does not become absence or pass

**Given:** A required receipt or source cannot be read.

**When:** Help classifies evidence.

**Then:**

- state is `UNKNOWN`;
- the error is shown;
- outcome is `HELP_DIAGNOSTIC_REQUIRED` or `HELP_READ_ERROR`;
- later steps are not recommended.

## HELP-019 — Stable recommendation identity

**Given:** Identical packet ID, snapshot hash, catalog hash, primary action, and reason codes.

**When:** Help runs twice.

**Then:** `recommendation_id` is identical.

**And given:** Any identity input changes.

**Then:** `recommendation_id` changes.

## HELP-020 — One primary action and visible sibling conflicts

**Given:** Several optional actions and two evidence conflicts affect the earliest required prerequisite.

**When:** Help responds.

**Then:**

- exactly one primary action is present;
- both conflicts are visible;
- optional actions are secondary and do not imply bypass.

## HELP-021 — Read-only and no automatic handoff

**Given:** Any valid or invalid fixture.

**When:** Help finishes.

**Then:**

- write count, skill invocation count, agent spawn count, and gate-decision count are all zero;
- output contains `auto_executed: false` and `files_written: none`;
- a recommended command remains unexecuted.

## Static conformance checks

The candidate bundle passes only if:

- frontmatter contains only `name` and `description`;
- metadata names the exact `project_stage_detection/v2` contract, current `PASS` receipts, and read-only behavior;
- the skill forbids local stage heuristics and partial-packet field consumption;
- currentness checks project identity, every source hash/absence, catalog hash, required read errors, and supersession;
- the detector is explicitly diagnostic and not a gate or receipt;
- artifact presence, status files, session text, and user claims cannot become `VERIFIED_PASS`;
- negative, stale, conflicting, missing, and unreadable evidence cannot advance;
- output exposes one primary action, structured evidence, packet/catalog/snapshot identity, and no-execution markers;
- all paths remain read-only and no recommended workflow is run.
