# Team Narrative — Independent Review Profile

This profile is exclusively for narrative artifact sets. It is not a system GDD,
architecture, implementation, test, localization-production, or content-rating
approval workflow. The reviewer is read-only and cannot edit, approve product
canon, authorize fixes, or record the final result.

## Input contract

Require:

- `content_id`, `run_id`, operation, review round, and stable reviewer/attempt IDs;
- frozen canon-manifest path/hash and `canon_baseline_sha256`;
- final artifact manifest path/hash and `final_artifact_set_sha256`;
- exact artifact ID/type/path/byte-count/raw-hash/owner rows;
- context, role, artifact, ownership, string-constraint, localization-review,
  trigger-contract, spoiler/access, and content-rating evidence hashes;
- changed artifact and declared-dependent set for scoped re-review; and
- prior review/finding hashes when verifying fixes.

Reject missing/ambiguous identity, unhashed inputs, artifact bytes that do not
match the manifest, stale canon, incomplete declared dependents, reviewer identity
overlap, revoked attempt token, or an input set above the approved context budget.
Return PARTIAL/BLOCKED evidence; do not guess or approve a subset as the whole.

## Independence

The reviewer identity and attempt token differ from every author, proposal agent,
writer, editor, shared recorder, canon/product decision-maker, plan approver, and
mutation authority for the reviewed set. A fresh context is required. Reusing the
same role type is allowed only with a demonstrably new identity/token and no hidden
authoring context.

The reviewer may not delegate, write, patch, polish, update findings outside the
review candidate, or make product canon choices. A side effect invalidates the
review and produces PARTIAL.

## Required checks

### NR-CANON — Canon and provenance

- Every narrative claim that depends on canon resolves to a stable canon ID and
  current source path/locator/hash.
- Character, faction, location, chronology, terminology, and relationship claims
  agree with the frozen baseline.
- No unresolved NCF finding or unverified canon-promotion projection is hidden in
  prose.
- Private/public access classes and canon registry projections agree.

### NR-VOICE — Character voice and continuity

- Dialogue voice, vocabulary, register, knowledge boundaries, emotional state,
  relationship stance, and character arc agree with current profiles.
- Variants and barks preserve intent without collapsing distinct voices.
- Voice exceptions cite a source-backed narrative reason and owner.

### NR-ARC — Arc, causality, pacing, and player comprehension

- Each artifact has a declared narrative purpose and stable entry/exit state.
- Beats have coherent cause/effect, escalation, payoff, emotional progression, and
  optional/mandatory status.
- Reveals do not rely on missing prerequisites or expose protected truths early.
- Failure, revisit, alternate-order, and skipped-content behavior is explicit when
  the trigger contract allows it.

### NR-TRIGGER — Gameplay and level contract

- Trigger/discovery/pacing contracts name stable level/gameplay IDs, preconditions,
  event, audience, state transition, repeatability, priority, and fallback.
- Narrative documents specify observable contracts, not engine implementation.
- Every referenced gameplay/level source matches the declared current hash.
- Dependent artifact IDs are complete for scoped re-review.

### NR-TRUTH — Mystery and spoiler partition

- Each public mystery reference uses a stable truth ID.
- The protected answer exists only in an authorized private canon artifact and its
  access/spoiler class matches policy.
- No answer leaks through dialogue, art brief, trigger metadata, finding excerpt,
  operational record, or localization payload.
- Orphan truths and unresolved public references are blockers.

### NR-LOC — Localization readiness and real UI constraints

- Every localizable string has a stable ID, source-locale owner, and formatter/
  placeholder/plural/gender/grammar contract.
- Concatenation, dates, numbers, names, markup, and culturally sensitive concepts
  are represented through declared current systems.
- Each relevant surface uses its actual UI/string constraint source/hash and
  locale/test profile. Universal character limits or generic expansion percentages
  are not accepted substitutes.
- `UNKNOWN` required constraints and every blocking LOC finding prevent
  LOCALIZATION_READY and COMPLETE even if business risk is accepted.
- The localization handoff excludes private truths and binds the current final
  artifact manifest/readiness evidence.

### NR-RATING — Content rating and cultural safety

- Content matches intended audience, rating policy, warnings, regional restrictions,
  sensitive-topic guidance, and opt-out/alternate presentation requirements.
- A policy exception has explicit authority/evidence and cannot waive localization,
  canon, or access-control blockers.

### NR-REF — Identity, reference, and artifact integrity

- Artifact IDs, paths, schemas, owners, hashes, dependencies, string IDs, truth IDs,
  trigger IDs, and proposal IDs agree across all manifests.
- Every requested artifact is present exactly once and no unlisted artifact appears.
- Create/revise classification, candidate/final hash, and read-back evidence agree.
- Operational checkpoint/result chains are linear, current, and owned by one
  recorder.

## Finding and coverage schema

Emit `cgs.narrative-review-result/v2` with:

```yaml
schema: cgs.narrative-review-result/v2
review_id: <stable id>
content_id: <id>
run_id: <id>
round: <nonnegative integer>
reviewer_identity: <independent identity>
attempt_token: <active token>
canon_baseline_sha256: <sha256>
final_artifact_set_sha256: <sha256>
scope_artifact_ids: []
dependent_artifact_ids: []
coverage:
  NR-CANON: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-VOICE: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-ARC: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-TRIGGER: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-TRUTH: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-LOC: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-RATING: COMPLETE | PARTIAL | NOT_APPLICABLE
  NR-REF: COMPLETE | PARTIAL | NOT_APPLICABLE
findings: []
disposition: PASS | CONCERNS | FAIL | PARTIAL
reviewed_at: <RFC3339 timestamp>
```

Every finding uses stable `NRF-<profile-check>-<artifact-id>-<fingerprint>` and
contains severity `BLOCKER | CONCERN | ADVISORY`, status `OPEN | ROUTED |
RESOLVED`, artifact/string/truth/trigger IDs, exact evidence path/locator/hash,
owner, destination, acceptance condition, and resolution evidence.

`NOT_APPLICABLE` requires an auditable reason and cannot be used for a requested
artifact obligation. Any required PARTIAL check makes the whole disposition
PARTIAL. Any open BLOCKER makes it FAIL. CONCERNS may contain only non-blocking
findings and still require owner routing/review points.

## Staleness and re-review

The result is current only while both canon-baseline and final-artifact-set hashes
match. Any artifact, dependency, constraint, localization evidence, trigger source,
truth boundary, owner, or canon change invalidates the affected result.

After an authorized fix, recompute the entire final artifact-set hash and review
every changed artifact plus its declared dependents with a fresh independent
identity/token. Prior findings remain evidence and receive explicit transitions;
they are not deleted or silently renumbered.

At most two fix/re-review rounds follow the initial review. Remaining blocker,
partial coverage, stale input, or identity overlap prevents COMPLETE. The review
never invokes a system-GDD reviewer or another workflow.
