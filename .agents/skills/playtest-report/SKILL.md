---
name: playtest-report
description: "Creates playtest protocols, ingests immutable session evidence, and finalizes build-bound playtest reports whose derived findings remain traceable to raw observations."
---

## Invocation and contract

Invoke as:

- $playtest-report template [<protocol-id>] [--save-protocol]
- $playtest-report ingest <path-to-notes> --session-id <session-id>
- $playtest-report finalize <session-id>
- $playtest-report review <session-id>
- Optional for finalize or review: --review full|lean|solo

The legacy new mode is an alias for template. The legacy analyze <path> form is not a completion command: treat it as ingest <path> and require a session ID before any write.

Resolve review mode exactly once per invocation:

1. Use an explicit --review value when present.
2. Otherwise read production/review-mode.txt once.
3. Otherwise use lean.
4. Reject any value other than full, lean, or solo with ERROR before reading session artifacts or writing files.

An explicit bounded user request authorizes its in-scope writes. Otherwise, before the first file change, present one complete changeset containing every intended path and modification and obtain one explicit approval. Do not re-prompt within that boundary. Stop for new approval only if scope expands materially.

## Phase 1: Validate inputs and choose one mode

Treat the project root as the only trust boundary for project artifacts. Resolve literal paths, normalize separators, reject missing paths and directories, and resolve symlinks before use. For ingest, reject any source whose real path escapes the project root. Accept only UTF-8 text notes in .md, .txt, .csv, or .json form up to 10 MiB. On a validation failure:

- return Verdict: ERROR with the failed check and path;
- do not create or modify a protocol, session, report, review, or verdict artifact;
- never return COMPLETE.

Session IDs are stable, unique identifiers in the form PT-<slug-or-uuid>. They must not be dates alone. Reject path separators, dot segments, collisions with an existing session, and reuse of an ID for a different evidence receipt or build.

Use this canonical layout and no alternate result location:

~~~text
production/playtests/
  _protocols/<protocol-id>.md
  <session-id>/
    manifest.md
    raw/<receipt-id>.<source-extension>
    observations.md
    report.md
    reviews/creative-director.md
~~~

Artifact types are distinct:

- protocol: reusable questions or a blank collection template; never a session result;
- raw evidence: byte-for-byte copied source notes plus a receipt; immutable after ingest;
- observation ledger: verbatim excerpts attributed to participants and raw offsets; immutable after ingest;
- completed session result: report.md with Artifact Type: playtest-session-result and Status: COMPLETED;
- director review: a hash-bound assessment under reviews/; never part of the raw evidence or completed report.

Only a distinct <session-id>/report.md that passes every finalization rule in Phase 4 counts as one playtest session. Files under _protocols, raw, reviews, or any legacy/noncanonical location do not count.

## Phase 2A: Template mode

Create a collection protocol, not a report. Include fields for:

- protocol ID and hypothesis or acceptance-criterion IDs;
- planned build, source commit, platform/configuration, input method, and accessibility profile;
- per-participant consent/anonymous ID, segment, start/end timestamps, device/input, and accessibility needs;
- verbatim observations with source location, observed behavior, participant statement, and attachment reference;
- session facilitator notes and evidence receipt placeholders.

If --save-protocol is absent, present the protocol without writing it. If it is present, write only production/playtests/_protocols/<protocol-id>.md after the authorization rule above. End with:

- Artifact Type: playtest-protocol
- Status: TEMPLATE
- Verdict: TEMPLATE_READY
- Gate Eligible: NO

Never create a session directory, report.md, Status: COMPLETED, or Verdict: COMPLETE in template mode.

## Phase 2B: Ingest immutable evidence

Read the validated source bytes once and calculate SHA-256 before interpretation. Create a new session changeset containing:

1. manifest.md with Artifact Type: playtest-session-manifest, Schema Version: 1, Session ID, Status: IN_PROGRESS, protocol/hypothesis or acceptance-criterion IDs, build version, build hash, source commit, platform/configuration, start/end timestamps, participant count, participant anonymous IDs, consent/retention classification, source path, receipt ID, raw SHA-256, and intended report path;
2. raw/<receipt-id>.<extension>, copied byte-for-byte from the input and never overwritten;
3. observations.md containing only the immutable observation layer.

Each observation row must contain a stable Observation ID (OBS-...), participant anonymous ID, source receipt ID, exact source line/range or timestamp, a verbatim excerpt, device/input/accessibility context, and attachment references. Preserve tester language. Do not paraphrase, classify, infer cause, assign priority, or overwrite the source in this ledger. Mark ambiguous attribution as UNKNOWN rather than inventing it.

For multiple participants, preserve separate observation rows. Never merge minority feedback into a majority summary at ingest time.

Before writing, preview the complete three-file changeset. Write it transactionally: stage all candidates, verify their hashes and internal references, then publish all or none. Reject existing session paths. End with Status: IN_PROGRESS and Verdict: EVIDENCE_INGESTED. This mode is not gate eligible and never returns COMPLETE.

## Phase 3: Build derived findings for finalization

Finalize reads only the canonical manifest, copied raw evidence, and observation ledger for the requested session. Recalculate the raw evidence SHA-256 and compare it with both manifest.md and observations.md. Any mismatch, missing artifact, invalid reference, or changed byte is ERROR.

Read design context only when the manifest explicitly names hypothesis, acceptance-criterion, or GDD IDs. Follow only those direct references. List missing or omitted context; do not silently broaden the scan.

Create interpretations separately from observations. Every finding must contain:

- Finding ID (FND-...) and Interpretation Type: DERIVED;
- one or more Observation IDs and the verified raw evidence SHA-256;
- category: Feel/Accessibility, Bug, Design Feedback, Balance, or Polish;
- observed frequency as n/N and participant segment, including majority and minority counts;
- impact, confidence, and evidence limitations;
- severity for observed impact, separate from product priority;
- proposed next step and owner candidate;
- for bugs, an occurrence ID and normalized fingerprint, plus a link to a matching canonical bug ID when one exists.

A derived finding may summarize or hypothesize, but it must not alter a verbatim excerpt or claim that an inference is an observed fact. A design-intent conflict is an interpretation tied to named design context, not a rewrite of the observation.

Produce these report sections:

1. Provenance and Completion Receipt
2. Session Profile and Participant Denominators
3. Feel and Accessibility
4. Bugs Observed
5. Design Feedback
6. Balance and Polish
7. Majority and Minority Signals
8. Next Steps
9. Finding Traceability Matrix

Top priorities must cite finding IDs. Rank impact, confidence, and frequency independently before proposing product priority.

## Phase 4: Finalize a completed session result

Finalization fails with Verdict: ERROR and writes no report.md unless all required fields are present and valid:

- unique Session ID and Schema Version;
- build version, build hash, source commit, platform/configuration, and input method;
- hypothesis or acceptance-criterion ID;
- tester/facilitator identifier and at least one consented or anonymous participant ID;
- start and end timestamps with end later than start;
- at least one answered, non-placeholder observation;
- evidence receipt ID, copied raw evidence, matching SHA-256, and observation-to-source locations;
- at least one derived finding whose Observation IDs resolve;
- explicit participant count and valid n/N denominators;
- canonical path production/playtests/<session-id>/report.md.

The completed report header must contain exactly these machine-readable fields:

~~~text
Artifact Type: playtest-session-result
Schema Version: 1
Session ID: <session-id>
Status: COMPLETED
Gate Eligible: YES
Build Version: <version>
Build Hash: <sha256-or-build-id>
Source Commit: <commit>
Platform Configuration: <platform/profile>
Hypothesis/AC IDs: <ids>
Started At: <ISO-8601>
Ended At: <ISO-8601>
Participant Count: <N>
Evidence Receipt ID: <receipt-id>
Raw Evidence SHA-256: <sha256>
Manifest SHA-256: <sha256>
Observation Ledger SHA-256: <sha256>
~~~

Compute the manifest and observation ledger hashes from the exact bytes used. Preview the complete report changeset, then write report.md atomically without modifying the raw evidence or observation ledger. Reject overwrite of an existing completed report; a new build or evidence set requires a new session ID.

Only after the canonical report is durably written and re-read with all checks passing, return:

- Session Status: COMPLETED
- Verdict: COMPLETE
- Gate Eligible: YES
- Canonical Result: production/playtests/<session-id>/report.md
- Completion Receipt: session ID plus report, manifest, ledger, and raw evidence hashes

A template, an ingest-only session, a malformed report, a duplicate session ID, or a legacy-path file can never produce this verdict.

## Phase 5: Optional creative-director review

Director review is derived commentary and cannot change session completion or evidence.

- solo: skip and report Director Review Status: SKIPPED_SOLO.
- lean: skip and report Director Review Status: SKIPPED_LEAN.
- full: after successful finalization, invoke the CD-PLAYTEST gate using the exact completed report bytes, report SHA-256, named game pillars/core fantasy if available, and the tested hypothesis. Require the response to echo the same report hash.

Write any valid response only to production/playtests/<session-id>/reviews/creative-director.md with:

- Artifact Type: playtest-director-review
- Session ID and immutable report SHA-256
- Review Status: COMPLETE
- Verdict: APPROVE, CONCERNS, or REJECT
- assessment and feedback explicitly labelled DIRECTOR INTERPRETATION

Never copy the verdict into report.md or rewrite observations. If the director is unavailable, times out, returns malformed output, or echoes a different hash, do not fabricate approval. Leave the completed session untouched and return Session Verdict: COMPLETE plus Director Review Status: PARTIAL and the failure reason. A director verdict never authorizes a design change.

The review command applies this phase to an already completed canonical report. It rejects missing, non-completed, stale, or hash-mismatched reports with ERROR.

## Phase 6: Action routing and next steps

Emit candidates only; do not invoke another workflow or mutate a bug, GDD, balance, or backlog artifact automatically.

- Bug findings: link an existing canonical bug when the fingerprint matches; otherwise propose a bug-report candidate with occurrence and finding IDs.
- Design findings: propose impact analysis against the named GDD/hypothesis before any design edit.
- Balance findings: propose verification against the named system and evidence.
- Polish findings: propose a backlog entry carrying session, finding, and observation IDs.

End every invocation with the mode, session/protocol ID when applicable, artifact paths, hashes produced, Status, Gate Eligible, director review status, and exactly one verdict appropriate to that mode. Do not call an incomplete artifact COMPLETE.
