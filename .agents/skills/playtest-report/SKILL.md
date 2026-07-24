---
name: playtest-report
description: "Validates immutable playtest sessions and returns traceable build-bound report candidates while keeping raw evidence, observations, inferences, review, recording, and gate authority separate."
---

## Read-only contract and invocation

Invoke exactly one mode:

```text
$playtest-report template --protocol-id <protocol-id> [--source <protocol-source>]
$playtest-report ingest --session <session-manifest> --bundle <evidence-bundle>
$playtest-report finalize --session <session-manifest> --bundle <evidence-bundle>
  [--review full|lean|solo]
$playtest-report verify-recording --report <canonical-report> --receipt <recorder-receipt>
```

Contract version: `cgs.playtest-report/v2`.

Omitting `--review` in `finalize` deterministically means `lean`; no settings or
session-state file is read to choose review depth.

This skill is strictly read-only in every mode. It may return a protocol,
ingestion assessment, final report candidate, optional director-review candidate,
or recording-verification result in conversation. It never creates a session,
copies or edits raw evidence, authors an observation ledger, writes a report or
review, changes consent, updates a bug/GDD/backlog/gate artifact, launches a
playtest, or invokes another workflow. A separately authorized recorder owns
artifact persistence and produces immutable receipts.

Reject missing or extra positional arguments, duplicate or unknown options,
option values beginning with `--`, mode-forbidden options, invalid review values,
URLs, globs, directories where files are required, symlinks, outside-repository
paths, and junction escapes. Do not infer a session, protocol, build, bundle,
report, receipt, context document, review mode from project state, or “latest”
artifact. Legacy
`new` and `analyze` forms return `ERROR — LEGACY MODE UNSUPPORTED` with the exact
replacement command and no artifact.

Input failure returns `ERROR`, names the failed input/check, emits no completed
status, report candidate, evidence record, or gate state, and stops.

---

## Phase 0: Freeze instructions, schemas, and fixed bounds

Resolve the repository root and canonicalize every supplied path before reading
content. Load every applicable `AGENTS.md` from the repository root to each
selected file in root-to-target order and list them in the output. Hash exact raw
bytes for every selected protocol, manifest, registry, policy, bundle, ledger,
context, report, and receipt. Recompute all hashes immediately before output. If
any selected byte changes, return `ERROR — INPUT CHANGED DURING ANALYSIS` without
a final report, evidence record, or gate state.

Supported schemas are:

- `cgs.playtest-protocol/v2` for preregistered questions, hypotheses, metrics,
  samples, consent requirements, and analysis rules;
- `cgs.playtest-session/v2` for immutable session/build/participant identity;
- `cgs.playtest-evidence-bundle/v1` for raw receipts, observation ledger, and
  transformation receipts;
- `cgs.playtest-observation-ledger/v1` for source-bound observations;
- `cgs.playtest-metric-registry/v1` and
  `cgs.playtest-statistics-policy/v1` for units, denominators, aggregation,
  missingness, and uncertainty;
- `cgs.playtest-evidence-adapter-registry/v1` and
  `cgs.playtest-adapter-receipt/v1` for non-native evidence formats;
- `cgs.playtest-report/v2` for final report payloads; and
- `cgs.playtest-report-recorder-receipt/v1` for independently persisted reports.

The request may select less work but cannot raise these fixed limits:

| Resource | Fixed maximum |
|---|---:|
| Protocol, session manifest, registry, policy, or receipt manifest | 1 MiB each |
| Participants | 512 |
| Raw evidence objects | 1,024 |
| Bytes per raw object | 512 MiB |
| Aggregate selected raw bytes | 2 GiB |
| Observation rows | 100,000 |
| Attachment references | 10,000 |
| Metrics | 1,024 |
| Stable findings | 4,096 |
| Explicit design-context files | 8 |
| Explicit design-context bytes | 256 KiB |
| Canonical bug-registry bytes | 1 MiB |
| Rows rendered per report section | 500 |
| One adapter execution | 30 seconds |
| All adapter executions | 300 seconds |
| One adapter receipt | 1 MiB |

Reject a manifest or selected raw-byte set above its pre-ingest bound as
`ERROR — REQUEST EXCEEDS FIXED BOUND`. When valid, within-byte-bound evidence
expands beyond an observation, attachment, metric, finding, context, or rendering
limit, stop at manifest order then stable identity order. Record the complete
candidate-set digest, included/omitted counts, boundary key, and omitted-tail
digest and return `PARTIAL — BOUNDED INGEST`. Never sample or summarize the
omitted tail, finalize a complete report, or claim gate candidacy.

Do not partially read a selected protocol, session manifest, registry, policy,
receipt, or context document. Do not let a manifest raise a fixed limit.

---

## Phase 1: Produce or validate an immutable session protocol

`template` returns a `cgs.playtest-protocol/v2` candidate only. A valid protocol
has stable protocol ID, semantic version, author/owner, creation UTC, target
hypothesis and/or stable AC IDs, direct design-context identities/hashes,
planned build/profile constraints, recruitment segments, participant inclusion/
exclusion rules, consent scopes, retention policy, accessibility dimensions,
questions/tasks, preregistered metrics, minimum samples, stopping rule, analysis
rules, and deviation policy.

Each metric declares a stable metric ID; value type (`binary`, `categorical`,
`ordinal`, `continuous`, or `duration`); unit/scale; eligible observation types;
participant/session/repeated-measure aggregation unit; numerator and denominator;
missing/withdrawn/excluded handling; segment strata; direction; threshold or
explicit `NONE`; minimum usable N; and statistics/uncertainty rule. Do not invent
success thresholds from prose or observed data.

When `--source` is supplied, validate and normalize only that source; otherwise
return a blank collection protocol whose unanswered fields remain explicit. A
blank candidate is `TEMPLATE READY`, never a session, completed result, evidence,
or gate candidate. This skill does not persist it.

For `ingest` and `finalize`, the session manifest must reference an independently
recorded protocol by exact path, version, and raw-byte SHA-256. The protocol must
have been finalized no later than session start. A post-session or changed
protocol is `RETROSPECTIVE PROTOCOL`; observations may be described, but all
preregistered hypothesis/metric claims and gate candidacy are invalid. Declared
session deviations retain their own IDs, timestamps, reasons, affected tasks/
metrics, and approver; an undeclared material deviation makes finalization
partial.

---

## Phase 2: Validate immutable session, build, participant, and consent identity

Require one exact `cgs.playtest-session/v2` manifest with:

- stable session ID `PT-<lowercase-kebab-or-uuid>` that is not a date alone;
- protocol ID/version/path/hash and hypothesis/AC IDs with direct source hashes;
- build ID/version, artifact SHA-256, source commit, source-tree state, engine
  product/version, build configuration, content/data version, and build receipt;
- platform profile ID/version/hash, hardware/device class, OS/runtime/driver,
  locale, network profile or `NONE`, graphics/profile settings, input method and
  device, and accessibility configuration;
- facilitator and recorder role IDs, scheduled/start/end UTC, monotonic duration,
  location/remote profile, session sequence, and prior-session relationship or
  `NONE`;
- declared participant count and ordered pseudonymous participant IDs; and
- evidence-bundle path/hash, metric/statistics registries and hashes, consent and
  retention policy versions/hashes, and canonical intended report path
  `production/playtests/<session-id>/report.md`.

Every participant row independently declares pseudonymous participant ID,
recruitment segment, cohort attributes allowed by consent, session participation
start/end, device/input, accessibility needs/accommodations or `NONE`, consent
receipt ID/path/hash, consent-policy version/hash, scopes for notes/quotes/
telemetry/audio/video/attachments, retention deadline, withdrawal status/time,
and exclusion reason or `NONE`.

Names, emails, account identifiers, contact details, or unapproved sensitive
attributes are forbidden in normalized observations and reports. The external
recorder must redact them before this workflow and provide a transformation
receipt binding source and redacted hashes. Do not read an unredacted object when
the bundle labels it restricted. Missing, expired, scope-incompatible, or
withdrawn consent excludes that participant and every linked observation/metric.
List the pseudonymous ID and reason without reproducing restricted content.

Manifest identity is immutable. Missing/duplicate/conflicting participant IDs,
impossible timestamps, reused session ID for another build/bundle, build or
profile hash mismatch, missing consent, or changed protocol/build/bundle bytes
produces `PARTIAL — SESSION IDENTITY` when safe local evidence remains, otherwise
`ERROR`. Never substitute current Git, host, build, time, platform, or user prose.

---

## Phase 3: Validate raw evidence and the observation layer

The evidence bundle lists immutable raw objects, recorder receipts, observation
ledger, redaction/transcription/normalization receipts, attachments, and exact
hashes. Each raw receipt binds stable object ID, media/data type, source device,
capture start/end, participant IDs or `NONE`, session/build IDs, byte length,
SHA-256, recorder product/version/hash, and chain-of-custody timestamps. Raw
objects remain external and byte-identical; this skill never copies or edits them.

Native observation-ledger rows require:

- stable observation ID and type `PARTICIPANT_QUOTE`, `OBSERVED_BEHAVIOR`,
  `TELEMETRY_EVENT`, or `FACILITATOR_NOTE`;
- session ID, pseudonymous participant ID or `NONE`, task/question/metric IDs;
- raw object/receipt ID and exact byte/line/event/timecode range;
- verbatim excerpt or exact normalized event value;
- device/input/accessibility/segment context; and
- transformation receipt IDs for redaction, transcription, or normalization.

An observation records what was said, seen, or measured. It cannot contain cause,
design intent, severity, priority, sentiment added by the model, or a proposed
solution. Facilitator notes remain their own observation type and are not promoted
to participant statements. Validate source ranges and recompute every reachable
raw/transformed hash. Ambiguous attribution is `UNKNOWN`, never guessed.

For non-native formats, select exactly one adapter by evidence type, producer/
exporter version, schema/version, and platform profile. The registry entry must
bind adapter ID/version/package SHA-256, deterministic arguments, supported
matrix, `cgs.playtest-observation-ledger/v1` output, validator receipts, and a
sandbox prohibiting network, project writes, undeclared reads, and child-process
expansion. Validate `cgs.playtest-adapter-receipt/v1` tool/argv/time/status/raw/
output hashes and warnings. Unsupported, ambiguous, malformed, truncated,
timed-out, nonzero, hash-mismatched, or unvalidated transformation excludes that
object and makes coverage `PARTIAL — INGEST`; never parse by loose text matching.

`ingest` stops after returning identity, chain-of-custody, consent, observation,
adapter, and omission ledgers. It returns `INGEST VALIDATED` only for complete
coverage; otherwise a precise `PARTIAL`. It never produces findings, finalizes a
session, or becomes gate evidence.

---

## Phase 4: Load only explicit context and resolve bug occurrences

`finalize` may read only design sources directly named by exact path/hash and
stable GDD/hypothesis/AC ID in the frozen protocol/session. Follow no second-level
links, fuzzy names, or “related” documents. Select in protocol declaration order
within the eight-file/256-KiB budget. List loaded and omitted identities, exact
bytes, hashes, and reasons. Missing, changed, conflicting, or over-budget required
context yields `PARTIAL — CONTEXT`; raw/observation facts remain reportable, but
design-intent findings and gate candidacy are unavailable.

For every bug-like observation cluster, compute a stable occurrence ID and
normalized fingerprint from session ID, build artifact hash, platform-profile
ID, canonical symptom code, affected task/system ID, and observation IDs. Query
only the canonical bug registry explicitly identified and hash-bound by the
session manifest. Link an existing bug only on exact fingerprint or exact stable
bug ID. Ambiguous/missing registry evidence yields an unlinked `BUG REPORT
CANDIDATE`; never claim a duplicate, create a bug, or invoke another workflow.

---

## Phase 5: Calculate preregistered metrics and sample uncertainty

Compute each metric only from eligible observations and participants under its
frozen definition. Report total recruited, consented, withdrawn, excluded,
started, completed, answered/observed, usable N, and missing N, plus reasons.
Preserve every segment denominator and minority result; never merge participant
statements or let an overall majority erase a segment reversal.

Use these deterministic summaries unless the frozen statistics policy is more
restrictive:

- binary: count `n/N`, proportion, and two-sided 95% Wilson interval for `N >= 2`
  using `z = 1.959963984540054` and the same exact Wilson formula declared in the
  policy; below two, counts only;
- categorical: count and proportion for every category including `OTHER` and
  missing, with denominator basis;
- ordinal: usable N, minimum, p25, median, p75, and maximum using the policy's
  exact quantile algorithm; never treat scale distance as continuous implicitly;
- continuous/duration: usable N, unit, min/p25/median/p75/max, and mean/sample-SD
  only when preregistered and `N >= 2`;
- repeated measures: first aggregate within the declared participant/session
  unit, then across independent units; never count events as participants.

Keep raw precision for decisions and round only for display. Report metric
threshold, direction, minimum usable N, achieved N, missingness, exclusions,
segment coverage, and protocol deviations. A percentage never substitutes for
`n/N`; a confidence interval is sampling uncertainty, not general population
proof. Do not generalize beyond recruitment frame, platform/build/profile, or
observed sample.

Unregistered analyses are labeled `EXPLORATORY`, with exact derivation and no
success/failure or gate claim. A preregistered metric below minimum N, invalid
denominator, unhandled missingness, consent exclusion that breaks sample rules,
or absent required segment makes finalization `PARTIAL — SAMPLE COVERAGE`.

---

## Phase 6: Derive stable findings without rewriting facts

Every finding uses:

```yaml
id: PTF-<category-slug>-<12-lowercase-hex>
category: FEEL | ACCESSIBILITY | BUG | DESIGN | BALANCE | POLISH
interpretation_type: DERIVED
session_id: <stable ID>
protocol_id: <stable ID/version/hash>
hypothesis_or_ac_ids: [<stable IDs>]
metric_ids: [<stable IDs>]
observation_ids: [<stable IDs>]
raw_receipt_ids: [<stable IDs>]
participant_evidence:
  segment: <stable segment ID or ALL>
  n: <supporting participants>
  denominator: <eligible participants>
  minority_n: <contrary participants>
  missing_n: <count>
observed_fact: <source-faithful summary>
inference: <explicit interpretation or NONE>
impact: LOW | MEDIUM | HIGH | CRITICAL
evidence_confidence: LOW | MEDIUM | HIGH
product_priority_candidate: NONE | LOW | MEDIUM | HIGH
limitations: [<specific limitations>]
acceptance_or_next_evidence: <falsifiable condition>
owner_handoff: <role or NONE>
bug_occurrence_id: <stable ID or NONE>
linked_bug_id: <stable ID or NONE>
```

Impact describes observed player/session effect; evidence confidence describes
support quality; product priority is a proposal for a product owner. They never
substitute for each other, and the model cannot assign an authoritative product
priority. “Top” ordering is deterministic by explicit product priority when
provided by an authorized source, then impact, evidence confidence, affected
participant count, and finding ID. Otherwise call it an evidence ordering, not
product priority.

Compute the finding suffix from SHA-256 of UTF-8 canonical JSON containing only
repository identity, session ID, protocol ID/version, category, sorted
hypothesis/AC IDs, sorted metric IDs, sorted observation IDs, and bug occurrence
ID or `NONE`. Do not include paths, excerpts, participant names, counts,
percentages, interval values, impact, confidence, priority, status, timestamps,
current report/build hash, or reviewer result. Coalesce identical identities,
retain all evidence, and sort by category then finding ID.

Every inference cites resolvable observation and raw receipt IDs. Preserve exact
observation text separately; never back-edit raw or observation artifacts. A
design-intent conflict requires loaded exact design context and remains an
interpretation. Causal claims require a separately identified controlled study;
otherwise use hypothesis language.

---

## Phase 7: Finalize a report candidate and optional review

Finalization is complete only when all protocol/session/build/platform/
participant/consent/raw/observation/context/metric/finding requirements validate,
the session has at least one eligible participant and answered non-placeholder
observation, all required metrics meet sample rules, and no bounded omission or
material undeclared deviation exists.

Return a canonical `cgs.playtest-report/v2` payload with:

1. `Result and Gate State`
2. `Protocol, Session, Build, and Platform Identity`
3. `Participant, Consent, and Sample Ledger`
4. `Raw Evidence and Transformation Receipts`
5. `Observation Ledger References`
6. `Context Coverage`
7. `Preregistered Metrics and Statistics`
8. `Feel and Accessibility`
9. `Bug Occurrences and Registry Links`
10. `Design, Balance, and Polish Findings`
11. `Majority, Minority, Missing, and Segment Signals`
12. `Stable Finding Traceability`
13. `Limitations and Exploratory Analyses`
14. `Owner Handoffs`
15. `Evidence Record`

Canonicalize the machine payload as UTF-8 JSON with lexicographically sorted
object keys, preserved array order, JSON number grammar, and no insignificant
whitespace. Include all identities/hashes, limits, included/excluded evidence,
coverage ledgers, statistics, findings, omissions, producer
`playtest-report@cgs.playtest-report/v2`, UUIDv4 run ID, and RFC 3339 UTC time.
Report bytes are the exact rendered report plus embedded canonical payload, but
exclude the separate evidence record and any later recorder receipt.

Complete finalization returns `FINALIZATION READY`, session status `COMPLETED`,
canonical intended path `production/playtests/<session-id>/report.md`, and gate
state `REQUIRES RECORDER`. Partial finalization returns the exact `PARTIAL` state,
no completed session status, and gate state `INELIGIBLE`.

For complete finalization only, emit one fenced `analysis-evidence` record using
`cgs.review-evidence/v1`, bound to exact report bytes/hash, session/build/protocol/
bundle identities, finding IDs, producer, run/time, coverage COMPLETE, and:

```yaml
artifact_kind: playtest-session-report-candidate
session_status: COMPLETED
persistence: NONE
recorder_receipt: NONE
gate_evidence_candidate: true
gate_eligible: false
gate_reason: REQUIRES INDEPENDENT RECORDER
```

Template, ingest, error, retrospective protocol, partial, truncated, insufficient
sample, or context-incomplete output emits no completed evidence record and is
gate-ineligible.

When `--review full`, at most one creative-director may receive only the bounded
final report candidate/hash, named pillars, and tested hypotheses after all
deterministic calculations finish. Wait at most three times for 60 seconds each,
with no retry/replacement/nested delegation. A valid response echoes the report
hash and becomes a separate `cgs.playtest-director-review/v1` candidate labeled
`DIRECTOR INTERPRETATION`. It cannot alter observations, findings, metrics,
session completion, or gate state. Timeout/unavailable/malformed/hash mismatch
sets review status and coverage `PARTIAL` without fabricating approval or changing
complete session analysis. `lean` and `solo` skip review explicitly.

---

## Phase 8: Verify independent recording and stop

`verify-recording` accepts only the canonical path
`production/playtests/<session-id>/report.md` and one independent
`cgs.playtest-report-recorder-receipt/v1`. Validate report schema/payload/hash,
session/protocol/build/bundle identities, candidate evidence record ID, recorder
identity/version, exact target path, persisted-file SHA-256, write/read-back UTC,
atomic-write result, and recorder separation from this analysis run. Rehash every
dependency referenced by the report or require a recorder snapshot receipt that
binds the same exact hashes.

Reconstruct the candidate evidence record deterministically from the report
payload/run metadata and recompute its record ID; never trust the receipt's
claimed candidate record ID by itself.

Return `RECORDED COMPLETED — GATE ELIGIBLE` only when the report is complete,
unmodified, unique by session ID, on the canonical path, and every receipt/hash/
dependency validates. A directory count, filename, protocol, raw object,
observation ledger, review, candidate response, legacy-path report, duplicate
session ID, changed build/profile, missing receipt, or partial report never
counts. Gate consumers must count distinct verified session IDs and display each
build artifact and platform profile.

Verification is read-only and does not amend the report. Invalid recording
returns `RECORDING INVALID — GATE INELIGIBLE` with reasons and no replacement
artifact. The recorder cannot change report bytes, findings, metrics, verdict, or
evidence to make them eligible.

After any mode output, stop. Do not persist an artifact, create a bug, revise a
design, set product priority, approve a director interpretation, update a gate,
or chain into another workflow.
