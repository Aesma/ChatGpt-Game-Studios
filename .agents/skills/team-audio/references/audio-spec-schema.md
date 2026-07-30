# Team Audio — Audio Specification and Review Schema

This reference defines the only authoritative artifact produced by `$team-audio`:

    design/audio/audio-<artifact-id>.md

The document is a player-facing audio design contract. It is not a technical
architecture, performance budget, asset brief, QA plan/result, implementation
story, test file, or review transcript.

## 1. Managed schema

Use `cgs.audio-spec/v2` with deterministic UTF-8 LF, fixed heading order, no
trailing whitespace, and one final newline. Machine-readable provenance fields at
the top include:

- schema/version, artifact ID, title, create/revise operation, spec status;
- request, context-manifest, source snapshot, direction-decision, and destination-
  ledger revisions;
- engine validation `CURRENT | DEFERRED`, engine/version evidence revision or null,
  and exact revalidation trigger when deferred;
- stable proposal, accessibility finding, external dependency, and acceptance IDs;
- artifact owner, transaction writer, and last approved candidate ID; and
- explicit `IMPLEMENTATION NOT PRESENT`, `QA NOT RUN`, and `PLAYBACK NOT RUN`.

The spec does not embed its own final declared revision. The write plan/checkpoint/review/
acceptance evidence records that revision externally.

## 2. Required headings

### 1. Identity, Purpose, and Scope

- artifact ID, feature/area identity, intended audience/platform scope;
- source snapshot references by path/locator/revision;
- player experience purpose and explicit inclusions/exclusions; and
- create/revise history references without duplicating checkpoint prose.

### 2. Approved Sonic Direction

- selected product-decision ID and source-bound rationale;
- emotional tone, palette, texture, recognizability, and mix-priority intent;
- music/ambience/SFX/voice relationship at an abstract design level; and
- explicit feature-local assumptions when no current sound bible exists.

### 3. Audio Event Contracts

Every event row has stable event ID and:

- trigger/precondition and repeat/interruption behavior;
- priority/criticality and player-facing meaning/result;
- spatial/non-spatial behavior and required directional alternative;
- variation/repetition intent and abstract mix/ducking rule;
- caption/subtitle/source-identification requirement;
- required visual/tactile equivalent for critical information;
- sensitivity control or accessibility behavior;
- dependency/proposal/finding IDs; and
- testable design acceptance IDs.

Event IDs are unique across the loaded asset/event index evidence. Collision or
ambiguous ownership is a blocker, never solved by silent renumbering.

### 4. Adaptive Music and State Transitions

- stable state IDs, entry/exit conditions, priority and fallback;
- transition, interruption, resume/recovery, hysteresis, and silence behavior;
- player-facing intent and failure/edge-case expectations; and
- event/trigger/dependency/acceptance IDs.

Do not select middleware, name engine classes, or prescribe concrete bus graphs.

### 5. Mix and Cue-Conflict Rules

- abstract categories and player-information priority;
- ducking/masking/silence/overlap expectations in observable terms;
- behavior when multiple critical cues compete; and
- acceptance criteria for intelligibility and redundancy.

Memory, CPU, voice-count, bitrate, streaming, and platform thresholds belong in a
PERFORMANCE_BUDGET destination and are only referenced by proposal/dependency ID.

### 6. Accessibility Contract

- stable AXA findings with only RESOLVED state included as closure evidence;
- critical-feedback visual/tactile equivalents;
- captions/source identification/directional alternatives;
- volume, dynamic-range, sudden/loud/high-frequency sensitivity controls; and
- testable accessibility acceptance IDs.

Open BLOCKING findings make the candidate `PARTIAL — NOT APPROVED`. Non-blocking
accepted risk also keeps the workflow NOT APPROVED; risk details live in external
evidence and are referenced by ID.

### 7. Destination and Dependency Ledger

Reference every non-AUDIO_SPEC proposal exactly once by stable ID, destination,
owner, acceptance condition, dependency status, and evidence revision:

- AUDIO_ASSET_BRIEF;
- TECHNICAL_ADR_OR_SPEC;
- PERFORMANCE_BUDGET;
- QA_PLAN;
- BACKLOG_OR_STORY; and
- REVIEW_ONLY.

Do not copy their detailed content into the spec. Technical ADR dependencies record
Accepted/open/unknown state without inventing a decision.

### 8. Engine Validation State

When current, reference engine/version and validation proposal revisions and list only
player-facing consequences. When deferred, state `ENGINE VALIDATION DEFERRED`, the
configuration evidence revision, affected IDs, owner, and exact revalidation trigger.
Do not guess engine-specific implementation.

### 9. Design Acceptance Criteria

Every criterion has stable ID, observable player-facing outcome, event/state IDs,
accessibility equivalence where relevant, evidence owner, and dependency condition.
Criteria may specify what future implementation/QA must prove but never claim that
it has been proved.

### 10. Open Items, Readiness, and Provenance

- open product/dependency/finding IDs with owner and acceptance condition;
- engine state and implementation-readiness prohibition;
- context/direction/ledger/proposal revisions;
- current spec status; and
- planned QA proposal IDs separate from executed QA/playback evidence.

## 3. Prohibited content

The AUDIO SPEC must not contain:

- middleware choice or configuration;
- concrete engine node/component/class/API patterns;
- bus graph implementation, import settings, file paths for code, or source snippets;
- memory/CPU/streaming/voice-count budget tables;
- unit/integration test implementation or QA/playback PASS claims;
- detailed audio-asset production instructions or generated asset content;
- ADR prose, story/task bodies, or implementation sequencing; or
- verbatim agent/reviewer transcripts and “all team outputs” aggregation.

Finding prohibited content is a destination-hygiene blocker. Route it to the named
owner/destination and regenerate the spec candidate.

## 4. Independent audio-spec review

Use `cgs.audio-spec-review/v2`:

```yaml
schema: cgs.audio-spec-review/v2
review_id: <stable id>
artifact_id: <id>
reviewer_identity: <independent identity>
attempt_token: <active token>
spec_path: design/audio/audio-<artifact-id>.md
spec_revision: <revision>
context_manifest_revision: <revision>
destination_ledger_revision: <revision>
engine_state: CURRENT | DEFERRED
coverage:
  direction: COMPLETE | PARTIAL
  events: COMPLETE | PARTIAL
  accessibility: COMPLETE | PARTIAL
  mix_conflicts: COMPLETE | PARTIAL
  adaptive_states: COMPLETE | PARTIAL
  destination_hygiene: COMPLETE | PARTIAL
  dependencies_engine: COMPLETE | PARTIAL
  acceptance_criteria: COMPLETE | PARTIAL
findings: []
disposition: PASS | CONCERNS | FAIL | PARTIAL
reviewed_at: <RFC3339 timestamp>
```

Reviewer identity/token differs from author and transaction writer. The reviewer is
read-only and may not delegate, edit, approve product direction, authorize fixes,
or write the checkpoint.

Findings use `AR-<artifact-id>-<check>-<stable key>` and contain severity
`BLOCKING | CONCERN | ADVISORY`, status `OPEN | ROUTED | RESOLVED`, exact section/
event/acceptance locator and spec revision, required outcome, owner, destination, and
resolution evidence.

Any required PARTIAL coverage makes the whole review PARTIAL. Any open BLOCKING
finding makes it FAIL. CONCERNS may contain only non-blocking items with owner and
review point; accepting them yields `ACCEPTED RISK — NOT APPROVED`, not SPEC
COMPLETE.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## 5. Completion evidence distinction

`SPEC COMPLETE` proves only that:

- the exact spec path exists with the accepted current revision;
- required sections/schema/destination hygiene pass;
- context is complete, accessibility/review blockers are zero, and product choices
  are resolved;
- external technical/asset/budget/QA/backlog work is explicitly routed;
- current independent review and PLANNED QA proposal bind that revision; and
- product acceptance/checkpoint record the same evidence.

It never proves code exists, audio assets exist, a build ran, QA executed, playback
was heard, mix quality passed, accessibility was runtime-tested, or any downstream
artifact was written.
