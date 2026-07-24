# Behavioral Test Spec: `$help`

## Purpose

Verify that `$help` is a strictly read-only recommender that consumes one
complete current `cgs.project-stage-detection/v2` packet and its exact bound
workflow catalog, validates current completion receipts, exposes claims and
conflicts honestly, and returns exactly one safe primary action without running it.

## Fixtures

Each fixture supplies as applicable:

- one canonical detector packet with deterministic packet/project/catalog/
  snapshot identities and producer validation oracle;
- the exact packet-bound versioned workflow catalog;
- catalog-declared completion policies, prerequisite graph, evidence indexes,
  finite read budgets, and verification actions;
- artifacts, receipts, repeatable-run records, sprint/session claims, and user
  context;
- read/currentness/canonicalization spies; and
- write, skill invocation, agent spawn, gate decision, and execution spies.

Tests never run project-stage-detect or any recommended workflow.

---

## Global assertions

1. No write, approval, gate decision, agent spawn, skill invocation, recorder, or
   recommendation execution occurs.
2. Stage comes only from one complete CURRENT
   `cgs.project-stage-detection/v2` packet whose project/catalog/manifest identities
   validate.
3. The implementation contains no local stage heuristic, transition map, artifact
   precedence, or stage.txt fallback.
4. Detector output is always diagnostic and never a workflow completion receipt.
5. Only a complete current catalog-policy bundle classified `VERIFIED_PASS` may
   satisfy a required prerequisite.
6. Exactly one primary action is returned and all same-level conflicts affecting
   that action remain visible.
7. Every output includes stable packet/catalog/snapshot/recommendation identity,
   structured evidence buckets, `auto_executed: false`, and `files_written: none`.

---

## HELP-001 — Current canonical packet and verified prerequisites

**Given:**

- one complete CURRENT canonical packet with DETECTED/CLEAR stage context;
- one matching supported catalog;
- every prerequisite before step S has a complete current policy-compliant PASS
  bundle with matching receipt/run/source/artifact/catalog identities.

**When:** Help runs.

**Then:**

- stage is copied exactly from the packet and labelled diagnostic only;
- all preceding prerequisites are VERIFIED_PASS with receipt IDs and current hashes;
- S is the one primary action;
- outcome is HELP_RECOMMENDATION_READY;
- detector evidence is not reused as a completion receipt.

---

## HELP-002 — HELP-P1-001: stage has one canonical producer

Run these variants:

| Variant | Fixture | Expected |
|---|---|---|
| 2a | No packet; artifacts resemble Production | MISSING + HELP_DIAGNOSTIC_REQUIRED; obtain packet |
| 2b | Wrong schema, truncated packet, bad completion marker, or bad packet ID | INVALID; no packet field consumed |
| 2c | Project root mismatch | PROJECT_MISMATCH; no local route |
| 2d | Catalog or packet source drift | STALE; refresh/reconcile packet |
| 2e | CURRENT packet result UNKNOWN | copy detector blockers; diagnostic action only |
| 2f | CURRENT packet result CONFLICT | copy all contradictions; reconcile them |
| 2g | CURRENT packet result ERROR | copy diagnostic state; no normal phase route |
| 2h | CURRENT packet DETECTED/CLEAR disagrees with local-looking artifacts | packet stage remains canonical |

**Assertions:**

- [ ] Schema is exactly `cgs.project-stage-detection/v2`
- [ ] Packet ID, project root ID, catalog hash, entry states, and manifest hash are
      verified before stage use
- [ ] Reproducible packet-declared ABSENT/UNREADABLE entries may form a CURRENT
      diagnostic packet whose detector result remains blocked
- [ ] No phase is inferred from source counts, directory names, stage.txt, engine
      configuration, sprint state, or user prose
- [ ] Help never invokes the detector

---

## HELP-003 — HELP-P1-002: artifact existence is not completion

Run separate earliest-required-step fixtures containing:

- an empty template;
- a populated draft;
- an artifact matching a catalog glob without approval evidence;
- a document-internal `Status: Approved` string;
- a current authoritative FAIL/BLOCKED/REJECTED receipt;
- a historical PASS receipt whose source or artifact hash changed; and
- one complete current catalog-policy PASS bundle.

**Expected classification:**

| Evidence | State |
|---|---|
| Empty template / populated draft / glob match / internal status text | PRESENT_UNVERIFIED |
| Current negative receipt | BLOCKED |
| Old receipt with current hash drift | STALE |
| Complete current accepted PASS bundle | VERIFIED_PASS |

**Assertions:**

- [ ] Only the final variant may satisfy the required prerequisite
- [ ] PRESENT_UNVERIFIED recommends the catalog verification/receipt action
- [ ] BLOCKED recommends resolving the recorded blocker
- [ ] STALE recommends revalidation on current hashes
- [ ] No non-verified state receives a checkmark or “completed” wording
- [ ] A detector stage or receipt is not substituted for the step receipt

---

## HELP-004 — HELP-P1-003: user prose remains CLAIMED

**Given:** The user says “I completed design-review,” “the gate passed,” or “we
finished the sprint,” but no matching complete current receipt exists.

**When:** Help runs.

**Then:**

- verbatim bounded statements are recorded with USER_CLAIM provenance and stable IDs;
- each affected prerequisite is CLAIMED unless higher-precedence current evidence
  makes it BLOCKED, CONTRADICTORY, VERIFIED_PASS, or STALE;
- output introduces the statement as “You reported”;
- primary action is the catalog verification/receipt-producing action;
- no later required step is recommended.

**And given:** A later valid current receipt independently verifies the same work.

**Then:** The receipt bundle, not the claim, produces VERIFIED_PASS; the claim
remains visible as claim provenance.

---

## HELP-005 — HELP-P1-004: sprint and session status are validated claims

Run `sprint-status.yaml`, session state, and task-note variants with:

1. no catalog-declared schema or completion role;
2. missing/unsupported schema version;
3. unknown status vocabulary;
4. missing/unauthorized owner;
5. stale updated-at, target, source, or catalog hash;
6. structurally valid current status record not accepted as a completion receipt; and
7. a catalog policy that explicitly accepts the record only as one member of a
   larger current receipt bundle.

**Expected behavior:**

- Variants 1 and 6 remain STATUS_CLAIM/CLAIMED or PRESENT_UNVERIFIED.
- Variants 2–5 are UNKNOWN, STALE, or PRESENT_UNVERIFIED with exact reasons.
- Variant 7 becomes VERIFIED_PASS only if every other required receipt, owner,
  target, source, artifact, freshness, and catalog condition also validates.

**Assertions:**

- [ ] A filename or `done` value never makes status authoritative
- [ ] Schema, version, owner, updated-at, vocabulary, target, and hashes are checked
- [ ] Status state cannot override a current negative or conflicting receipt
- [ ] The earliest affected verification action remains primary

---

## HELP-006 — HELP-P1-005: repeatable steps require exact current run receipts

**Fixture:**

- repeatable required step with prior runs R1 and R2;
- current request is R2 scope/input set;
- R1 has a PASS receipt and newer file mtime;
- R2 receipt variants are missing, stale, negative, superseded, conflicting, and
  complete-current-PASS.

**Expected behavior:**

- R1 is STALE for R2 regardless of filename or mtime;
- missing R2 is MISSING, stale R2 is STALE, negative R2 is BLOCKED, conflicting
  R2 receipts are CONTRADICTORY;
- only the non-superseded complete current R2 PASS bundle is VERIFIED_PASS;
- missing/non-pass R2 recommends the catalog-declared R2 receipt-producing,
  revalidation, resolution, or reconciliation action.

**Assertions:**

- [ ] Exact run ID, receipt ID, scope, inputs, source/artifact hashes, producer,
      verdict, timestamp, catalog hash, and lineage/supersession are validated
- [ ] No “latest,” “last completed,” directory order, or same-named artifact rule exists
- [ ] Receipt IDs and run IDs appear in structured output

---

## HELP-007 — HELP-P1-006: reads, schemas, and budgets fail closed

Run these variants:

| Fault | Evidence state / outcome |
|---|---|
| Packet/catalog cannot be read globally | HELP_READ_ERROR or HELP_DIAGNOSTIC_REQUIRED |
| Catalog policy required for routing is missing/malformed/unsupported | UNKNOWN; HELP_NO_SAFE_RECOMMENDATION or HELP_DIAGNOSTIC_REQUIRED |
| Required receipt/source/artifact cannot be read | UNKNOWN; exact coverage gap; no later step |
| Catalog evidence-read entry/byte limit would be crossed | UNKNOWN + READ_BUDGET_EXCEEDED |
| Evidence changes between initial read and final rehash | STALE |
| Candidate location is confirmed absent | MISSING, not UNKNOWN or PASS |
| Invalid invocation/root/path/hash/packet selection | HELP_INPUT_ERROR |

**Assertions:**

- [ ] Access error is not converted to absence, pass, or empty content
- [ ] No silent truncation or unbounded scan
- [ ] Raw path/hash/source state and exact reason remain visible
- [ ] A later required step is never recommended after UNKNOWN
- [ ] No command is invented when catalog policy is incomplete

---

## HELP-008 — HELP-P1-007: one action does not hide sibling conflicts

**Fixture:**

- the earliest required prerequisite has two conflicting current receipts and one
  stale supporting artifact;
- another same-level prerequisite has an affecting unknown owner receipt;
- several optional actions and later required steps also exist.

**When:** Help runs.

**Then:**

- exactly one reconciliation/diagnostic action is primary;
- all affecting same-level conflict/unknown prerequisite IDs, evidence IDs, and
  reason codes are displayed;
- the stale supporting artifact remains visible in its evidence bucket;
- optional actions are non-executable context only;
- no later required step is described as unblocked or “next.”

**Assertions:**

- [ ] Conflicting current receipts classify CONTRADICTORY, not pass or arbitrary precedence
- [ ] Primary-action brevity never removes sibling blockers
- [ ] recommendation_id includes every displayed same-level conflict ID

---

## HELP-009 — Later detected stage is not gate approval

**Given:** A CURRENT packet diagnoses a later phase, while a catalog prerequisite
or phase-transition dependency lacks a complete current PASS receipt.

**When:** Help builds the prerequisite closure.

**Then:**

- packet stage stays DIAGNOSTIC_ONLY;
- no missing gate or approval evidence is synthesized;
- the earliest verification/gate-receipt action is primary;
- later phase work is not recommended as safe next action.

**And given:** Detector evidence contains the word PASS.

**Then:** It remains detector evidence and never becomes a workflow completion receipt.

---

## HELP-010 — Deterministic evidence precedence

For one prerequisite, validate this exact precedence:

1. conflicting current authoritative receipts → CONTRADICTORY;
2. one current authoritative negative receipt with no conflict → BLOCKED;
3. one complete current PASS bundle with no conflict → VERIFIED_PASS;
4. only stale/superseded/mismatched evidence → STALE;
5. only claim/status assertion → CLAIMED;
6. only present artifact/status record → PRESENT_UNVERIFIED;
7. confirmed absence → MISSING;
8. access/schema/budget/interpretation failure → UNKNOWN.

Every evidence record remains visible after classification. Only VERIFIED_PASS
satisfies a required prerequisite.

---

## HELP-011 — Stable recommendation identity

**Given:** Identical packet ID, packet manifest hash, catalog hash, help evidence
snapshot hash, primary action, reason codes, and same-level conflict IDs.

**Then:** Two runs produce the same recommendation_id.

**And given:** Any identity input changes.

**Then:** recommendation_id changes.

The ID never depends on filesystem mtime, arbitrary directory order, or prose formatting.

---

## HELP-012 — Read-only and no automatic handoff

**Given:** Any valid, invalid, stale, missing, conflicting, or unreadable fixture;
the user asks help to run the recommendation, repair evidence, or save the result.

**Then:**

- write count, skill invocation count, agent spawn count, recorder count,
  gate-decision count, and external-action count are zero;
- output contains `auto_executed: false` and `files_written: none`;
- exactly one primary action remains text only;
- no changeset or write-authorization prompt appears.

---

## Structured output assertions

Every response contains:

- exact outcome enum and stable recommendation_id;
- help snapshot time and stage context;
- stage source exactly `cgs.project-stage-detection/v2`;
- packet ID/source/raw hash/project root/result/resolution/declared/detected stage/
  confidence/manifest hash;
- catalog path/version/hash;
- one primary action, affected prerequisite, state, and reason codes;
- all same-level conflicts;
- verified, claimed, present_unverified, stale, blocked, missing, contradictory,
  and unknown evidence buckets;
- receipt/run IDs and current hashes;
- packet contradictions, read errors, coverage gaps, and blocking reasons;
- `auto_executed: false`, `files_written: none`, and the advisory disclaimer.

Only VERIFIED_PASS appears as “Verified done.” Claims say “You reported,” and
present artifacts say “Found but unverified.”

---

## Static conformance checks

The candidate bundle passes only if:

- frontmatter contains only name and description;
- metadata names exact `cgs.project-stage-detection/v2`, current receipt evidence,
  one action, read-only behavior, and no execution;
- all HELP-P1-001 through HELP-P1-007 appear as explicit behavior cases;
- the skill forbids local stage heuristics and partial/stale packet consumption;
- packet currentness checks packet/project/catalog/manifest identity and explicit
  source states without rejecting a reproducible diagnostic UNKNOWN packet;
- artifact presence, internal status text, user/status claims, and detector output
  cannot become VERIFIED_PASS;
- sprint status validates schema/owner/time/vocabulary/hashes before any catalog-
  permitted use;
- repeatable work requires exact current run/scope/lineage receipt identity;
- negative, stale, conflicting, missing, over-limit, and unreadable evidence cannot advance;
- output exposes all earliest conflicts while returning one primary action;
- all paths remain read-only and no recommended workflow runs.

Catalog last-test fields remain empty until these cases are actually executed;
this specification is not itself current execution evidence.
