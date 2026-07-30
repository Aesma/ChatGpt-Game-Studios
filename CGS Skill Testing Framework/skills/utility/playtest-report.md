# Skill Test Spec: `$playtest-report`

## Skill Summary

`$playtest-report` contract `cgs.playtest-report/v2` is a strictly read-only,
four-mode workflow. It creates protocol candidates, validates immutable recorded
session bundles, derives source-bound report candidates, and verifies separately
recorded canonical reports. Raw evidence, observation, inference, director
review, report recording, and gate authority remain distinct.

A template or ingest assessment never counts as a playtest. A finalized report
candidate is not yet gate-eligible. Only a complete, unchanged
`production/playtests/<session-id>/report.md` plus an independent valid recorder
receipt can return `RECORDED COMPLETED — GATE ELIGIBLE`.

---

## Required test instrumentation

Run behavioral cases in an isolated disposable repository fixture. Record:

1. recursive path/type/revision snapshots before and after invocation;
2. every filesystem mutation attempt by the workflow, adapters, and reviewer;
3. every file read, canonical path, exact byte count, and read order;
4. every adapter ID/version/package revision, argv, runtime, exit status, raw/output
   revision, receipt, and sandbox denial;
5. every delegated role, input/report revision, wait count/duration, completion state,
   and returned review bytes;
6. exact response, report candidate, canonical payload, evidence, omission proof,
   and verification bytes; and
7. deterministic clock and UUID sources for stable-revision tests.

The mutation guard passes only when before/after snapshots are byte-identical and
the mutation-attempt ledger is empty. External fixture setup may create recorder
artifacts before invocation, but this skill must not. If instrumentation cannot
observe a required fact, mark the assertion `UNTESTED`, not PASS. Do not update
catalog result fields from static inspection or an uninstrumented run.

---

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] Contract version is exactly `cgs.playtest-report/v2`
- [ ] Metadata says immutable/read-only session analysis and independent recorder
- [ ] Exact template, ingest, finalize, and verify-recording grammars are explicit
- [ ] Legacy/invalid/missing/outside/directory/symlink/unknown inputs fail closed
- [ ] Protocol, session, evidence bundle, observation, metric/statistics, adapter,
  report, and recorder-receipt schemas are versioned
- [ ] Protocol is frozen before session start and binds hypothesis/AC, build,
  sample, consent, metric, statistics, and deviation rules
- [ ] Build/source/platform/input/accessibility and participant/consent/retention
  identity are mandatory and immutable
- [ ] Raw receipts, observations, derived findings, director review, report, and
  recorder receipt are separate artifact types
- [ ] Fixed bytes/files/participants/observations/metrics/findings/context/rows/
  adapter-time limits cannot be raised by input
- [ ] Explicit context traversal and exact bug-registry lookup are bounded
- [ ] Participant aggregation preserves n/N, missing/excluded/withdrawn counts,
  segments, majority, minority, and accessibility context
- [ ] Metric type, unit, aggregation unit, denominator, missingness, sample floor,
  summary statistics, and uncertainty are deterministic
- [ ] Stable finding IDs exclude paths, excerpts, PII, values, severity,
  confidence, priority, time, report/build revision, and review
- [ ] Impact, evidence confidence, and product priority remain separate axes
- [ ] Complete candidate evidence is not gate-eligible before recorder receipt
- [ ] Recording verification rejects directory counts, duplicate sessions,
  changed bytes/build/profile, partial reports, and noncanonical paths
- [ ] Optional director review is bounded, separate, and cannot alter analysis or
  fabricate approval
- [ ] All modes are zero-write and never chain to bug/design/backlog/gate workflows

---

## Canonical fixture

Unless overridden, use protocol `PROTO-COMBAT-01` version `2.1.0`, session
`PT-combat-001`, build `BUILD-220` with artifact revision `B`, commit `C`, and
platform profile `PLAT-PC-60` at revision `P`. The protocol predates session start,
names hypothesis `HYP-COMBAT-01` and AC `AC-COMBAT-017`, preregisters metrics,
segments, sample floors, accessibility dimensions, consent scopes, and direct
design-context revisions.

The evidence bundle contains validated pseudonymous participants, active consent
receipts, immutable raw receipts, a `cgs.playtest-observation-ledger/v1`, and
transformation receipts. Placeholder revisions are replaced with valid non-empty stable value values.

---

## Case 1: Strict invocation and path validation

### Fixture

Provide valid source artifacts plus missing files, directories, outside paths,
symlinks, junction escapes, URLs, globs, unrelated sessions, and latest-looking
files.

### Input

Run missing mode/options, extra positional arguments, duplicate/unknown options,
values beginning with `--`, mode-forbidden options, invalid review values, valid
four-mode commands, and legacy `new`/`analyze` commands.

### Expected writes

None.

### Expected behavior

Valid commands canonicalize each explicit path once. Invalid input returns
`ERROR` with token/path and reason. Legacy modes return exact replacement
guidance. No session, build, context, report, receipt, or latest artifact is
inferred; no completed/evidence/gate output is emitted.

### Assertions

- [ ] Exact grammar matches the skill contract
- [ ] Directory and missing path never become an empty session
- [ ] Invalid review value fails before session artifacts are read
- [ ] Unrelated files are never read
- [ ] Mutation guard passes

## Case 2: Template is a protocol candidate, never a session

### Fixture

Use no source, a complete source protocol, and a blank/placeholder-heavy source.

### Input

Run `template --protocol-id PROTO-COMBAT-01` with and without `--source`.

### Expected writes

None; no `_protocols` or session path is created.

### Expected behavior

The response is `cgs.playtest-protocol/v2` and `TEMPLATE READY`. Blank fields stay
explicit. Protocol content includes hypotheses/ACs, build/profile constraints,
recruitment, consent/retention/accessibility, tasks, metrics, sample/stopping/
analysis/deviation rules. It never reports completed session or gate evidence.

### Assertions

- [ ] Template lacks session completion and gate candidacy
- [ ] Each metric has stable type/unit/denominator/sample/statistics rules
- [ ] Participant placeholders are pseudonymous and scoped by consent
- [ ] No report or evidence record is emitted
- [ ] Mutation guard passes

## Case 3: Protocol immutability and retrospective registration

### Fixture

Create variants where protocol finalization precedes session, follows session,
revision changes after collection, declares a material deviation, or omits that
deviation.

### Input

Run ingest and finalize against each variant.

### Expected writes

None.

### Expected behavior

Only the pre-session exact-revision protocol supports preregistered claims. A later or
changed protocol is `RETROSPECTIVE PROTOCOL`; observations remain describable but
gate candidacy is forbidden. Declared deviations identify affected metrics;
undeclared material deviation makes finalization partial.

### Assertions

- [ ] Protocol ID/version/path/revision and finalization UTC are verified
- [ ] Post-hoc thresholds are never treated as preregistered
- [ ] Deviation IDs/reasons/times/metrics/approver are retained
- [ ] Retrospective status cannot be hidden by a complete bundle
- [ ] Mutation guard passes

## Case 4: Session, build, and platform identity is immutable

### Fixture

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

### Input

Run finalize for every variant.

### Expected writes

None.

### Expected behavior

Each mismatch is `PARTIAL — SESSION IDENTITY` when safe local evidence remains or
`ERROR` when primary identity is unusable. No report candidate, completed status,
or gate evidence exists. Current Git/host/time/build never fills a gap.

### Assertions

- [ ] Exact missing/mismatched field and affected evidence are listed
- [ ] Date-only and reused session IDs are rejected
- [ ] New build or bundle requires a distinct session identity
- [ ] Intended path is exactly `production/playtests/<session-id>/report.md`
- [ ] Mutation guard passes

## Case 5: Participant consent, privacy, withdrawal, and retention

### Fixture

Provide active consent, missing receipt, expired scope, quote-only scope with
telemetry, withdrawal, duplicate pseudonym, PII in normalized observations,
restricted unredacted raw object, valid redaction receipt, and retention expiry.

### Input

Run ingest/finalize independently.

### Expected writes

None.

### Expected behavior

Only consent-compatible pseudonymous participant evidence is eligible. Missing,
expired, withdrawn, scope-incompatible, duplicate, restricted, or retention-
invalid evidence is excluded without reproducing sensitive content. A valid
redaction transformation binds source/redacted revisions.

### Assertions

- [ ] Names/emails/accounts/contact details never appear in normalized output
- [ ] Withdrawal removes all linked observations/metrics under the policy
- [ ] Consent policy/scope/receipt/revision and retention deadline are traceable
- [ ] Exclusion changes every affected denominator
- [ ] Insufficient required sample becomes partial and gate-ineligible

## Case 6: Raw evidence, observation, and inference remain distinct

### Fixture

Include quote, observed behavior, telemetry, facilitator note, ambiguous
attribution, source-range mismatch, altered raw bytes, and an observation row
containing inferred cause/priority.

### Input

Run ingest and finalize.

### Expected writes

None.

### Expected behavior

Valid observations retain type, raw object/receipt, exact range, verbatim/event
value, participant/context, and transform receipt. Ambiguity is `UNKNOWN`. revision/
range mismatches and inference in the ledger are partial/invalid; findings remain
a separate derived layer.

### Assertions

- [ ] Facilitator note is not a participant quote
- [ ] Observation text is never paraphrased or back-edited
- [ ] Cause, severity, priority, design intent, and solution are absent from raw
  observation fields
- [ ] Every inference later resolves to observation and raw receipt IDs
- [ ] Mutation guard passes

## Case 7: Evidence adapters are exact and partial parse fails closed

### Fixture

Use native ledger plus supported non-native formats, unsupported version, two
equally exact adapters, package-revision mismatch, invalid validator receipt,
timeout/nonzero, malformed/truncated data, receipt mismatch/oversize, and adapter
network/write/undeclared-read/child-process attempts.

### Input

Run ingest for each variant and one mixed valid/invalid bundle.

### Expected writes

None.

### Expected behavior

Only an exact validated adapter executes. Invalid primary bundle is `ERROR`;
mixed bundle is `PARTIAL — INGEST`, with local observations disclosed but no
findings/finalization/gate evidence.

### Assertions

- [ ] Adapter ID/version/revision, format/schema/platform, argv, times, raw/output
  revisions, receipt, and warnings are reported
- [ ] No loose text parsing repairs malformed or truncated sources
- [ ] Sandbox attempts fail closed and mutation guard passes
- [ ] Excluded object/observations and reasons are explicit
- [ ] Ingest never derives findings

## Case 8: Design context is explicit, direct, and bounded

### Fixture

Protocol names direct GDD/hypothesis/AC paths and revisions. Add unrelated documents,
second-level links, fuzzy names, missing/revision-changed sources, nine files, and a
selected set above 256 KiB.

### Input

Run finalize for each variant.

### Expected writes

None.

### Expected behavior

Only exact direct references are read in protocol order. Loaded/omitted paths,
bytes, revisions, and reasons are reported. Required missing/conflicting/over-budget
context yields `PARTIAL — CONTEXT`; observations remain facts, but no design-
intent finding or gate candidate is emitted.

### Assertions

- [ ] Unrelated and second-level documents are never read
- [ ] File-count and exact-byte budgets both apply
- [ ] Input cannot raise limits
- [ ] Design-intent inference cites exact loaded source identity
- [ ] Mutation guard passes

## Case 9: Multiple participants preserve majority, minority, and missingness

### Fixture

Five eligible participants: three report confusion, one reports no confusion,
and one gives no answer. Use two segments with a segment-level reversal and
different input/accessibility contexts.

### Input

Run finalize.

### Expected writes

None.

### Expected behavior

Report `3/4` answered participants supporting confusion, `1/4` minority, one
missing of five recruited/eligible, and each segment denominator. No-answer is
not silently added to either side; overall aggregation does not erase reversal.

### Assertions

- [ ] Recruited/consented/withdrawn/excluded/started/completed/usable/missing
  counts reconcile
- [ ] Each participant contributes according to declared aggregation unit
- [ ] Minority, missing, segment, device, and accessibility evidence remains
  visible
- [ ] Participant statements are not merged or rewritten
- [ ] Mutation guard passes

## Case 10: Feel and accessibility retain profile-specific evidence

### Fixture

Use preregistered Feel and Accessibility metrics across keyboard, controller,
screen-reader, reduced-motion, high-contrast, remapped-input, and no-declared-
need participants. Include an accommodation not exercised in the session.

### Input

Run finalize.

### Expected writes

None.

### Expected behavior

Findings and metrics remain attached to participant segment, device/input,
accessibility profile/accommodation, task, observation IDs, and denominators.
Unexercised accommodations are `NOT OBSERVED`, not pass/fail.

### Assertions

- [ ] Feel and Accessibility have explicit report sections
- [ ] Accessibility need and accommodation are distinct
- [ ] No result is generalized to untested profiles/devices
- [ ] Design feedback and next-evidence handoffs remain present and traceable
- [ ] Mutation guard passes

## Case 11: Metrics, statistics, uncertainty, and sample floors

### Fixture

Create binary, categorical, ordinal, continuous, duration, and repeated-measure
metrics with independently calculated summaries. Add N=1 binary, missingness,
withdrawn participant, invalid unit, post-hoc threshold, insufficient segment,
and events incorrectly counted as participants.

### Input

Run finalize for each fixture.

### Expected writes

None.

### Expected behavior

Metrics follow frozen type/unit/aggregation/denominator/missingness/quantile and
uncertainty rules. Binary N>=2 includes Wilson 95%; ordinal/continuous summaries
follow policy; repeated measures aggregate within participant first. Insufficient
required sample is `PARTIAL — SAMPLE COVERAGE`; post-hoc analysis is EXPLORATORY.

### Assertions

- [ ] Every percentage includes n/N and denominator basis
- [ ] Full precision decides thresholds; display rounding cannot flip a result
- [ ] Confidence interval is not population proof
- [ ] Event count never becomes participant N
- [ ] Unregistered metric has no success/failure or gate claim

## Case 12: Fixed ingest limits and deterministic omission proof

### Fixture

Exercise each limit at limit minus one, limit, and limit plus one. Include a raw
object within byte limit whose normalized observations exceed 100,000, more than
500 rendered rows, and manifest attempts to raise limits.

### Input

Run ingest/finalize for each boundary fixture.

### Expected writes

None.

### Expected behavior

Pre-ingest structural/byte excess is `ERROR — REQUEST EXCEEDS FIXED BOUND`.
Post-normalization excess is `PARTIAL — BOUNDED INGEST` with candidate-set
reference ID, included/omitted counts, stable boundary key, and tail reference ID.

### Assertions

- [ ] Deterministic manifest/stable-ID order retains the same prefix
- [ ] Omitted tail is never sampled, summarized, or generalized
- [ ] No partial/truncated result finalizes or becomes gate candidate
- [ ] Selected manifests/registries/policies/receipts/context are read whole
- [ ] Mutation guard passes

## Case 13: Bug occurrence identity and registry routing

### Fixture

Provide two observation clusters with identical symptom stable key, an exact
matching canonical bug, an ambiguous near-match, missing registry, changed
registry revision, and no match.

### Input

Run finalize.

### Expected writes

None; bug registry and reports remain byte-identical.

### Expected behavior

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

### Assertions

- [ ] Occurrence identity includes session/build/platform/symptom/task/
  observation identity
- [ ] Fuzzy title/text never links a bug
- [ ] Multiple observations coalesce without losing evidence
- [ ] Candidate contains owner handoff, not a created bug
- [ ] Mutation guard passes

## Case 14: Stable findings separate impact, confidence, and priority

### Fixture

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

### Input

Finalize each fixture twice.

### Expected writes

None.

### Expected behavior

Noncanonical changes preserve `PTF-<category>-<non-empty stable value>`; canonical
changes alter it. Duplicates coalesce, evidence is retained, and ordering follows
authorized priority then impact/confidence/count/ID, or is labeled evidence-only.

### Assertions

- [ ] Canonical JSON and suffix independently recompute
- [ ] PII, values, severity/confidence/priority/time/review never enter ID
- [ ] Impact, evidence confidence, and priority remain independent fields
- [ ] Model cannot claim authoritative product priority
- [ ] Finding acceptance/next-evidence condition is falsifiable

## Case 15: Observation is not inference or unsupported cause

### Fixture

Provide participant quote, observed navigation failure, matching telemetry, and
loaded design intent. Add source correlation without a controlled study and a
separately identified controlled study.

### Input

Run finalize.

### Expected writes

None.

### Expected behavior

Raw/observation facts remain quoted/referenced separately. Design conflict is
labeled DERIVED and cites context. Correlation remains hypothesis; only the
controlled study can support a bounded causal claim. Proposed next steps are
owner handoffs, not executed changes.

### Assertions

- [ ] Every inference resolves to observation and raw receipt IDs
- [ ] No finding rewrites participant language
- [ ] Severity/priority is not inserted into observation layer
- [ ] Unsupported causal language is absent
- [ ] Mutation guard passes

## Case 16: Complete finalization yields candidate, not gate evidence

### Fixture

Use a complete canonical protocol/session/bundle/context/sample/finding dataset.
Also run one missing required field from each layer.

### Input

Run finalize in lean mode.

### Expected writes

None; canonical report path remains absent.

### Expected behavior

Complete data returns all 15 headings, canonical `cgs.playtest-report/v2`,
`FINALIZATION READY`, session status COMPLETED, intended path, and gate state
`REQUIRES RECORDER`. Missing-layer variants are exact PARTIAL/ERROR and
gate-ineligible.

### Assertions

- [ ] Report bytes and canonical payload exclude evidence/recorder receipt
- [ ] Exactly one complete `cgs.review-evidence/v1` record binds report bytes
- [ ] Record says persistence NONE, gate candidate true, gate eligible false
- [ ] Template/ingest/partial emits no completed evidence record
- [ ] Mutation guard passes

## Case 17: Independent recorder verification controls gate eligibility

### Fixture

Provide a recorder-persisted complete report at canonical path and exact receipt.
Add variants with absent receipt, wrong path, changed byte, changed build/profile/
bundle dependency, duplicate session ID, non-atomic/no-readback receipt, partial
report, legacy path, template, observation ledger, and director review.

### Input

Run verify-recording for each explicit report/receipt pair.

### Expected writes

None.

### Expected behavior

Only the exact complete pair returns `RECORDED COMPLETED — GATE ELIGIBLE`.
Everything else is `RECORDING INVALID — GATE INELIGIBLE` with reasons. No
artifact is repaired or replaced.

### Assertions

- [ ] Receipt binds recorder identity, candidate record, exact path/file/payload,
  session/protocol/build/bundle, atomic write, and read-back
- [ ] Recorder is independent from analysis run
- [ ] Directory/file count cannot substitute for validation
- [ ] Recorder cannot change report bytes to make them eligible
- [ ] Mutation guard passes

## Case 18: Director review is bounded and cannot alter session truth

### Fixture

Use complete finalization and full review variants: success echoing revision,
unavailable, timeout, malformed response, wrong revision, late response, and nested
delegation attempt. Also use lean and solo.

### Input

Run finalize with each review mode.

### Expected writes

None; no review file or report mutation.

### Expected behavior

At most one creative director receives the bounded candidate after calculation.
Success returns a separate `DIRECTOR INTERPRETATION` candidate. Failure is review
coverage PARTIAL, without fabricated approval or change to session completion,
metrics, findings, evidence, or gate state. Lean/solo skip.

### Assertions

- [ ] At most three 60-second waits; no retry/replacement/nested delegation
- [ ] Late/mismatched result is ignored
- [ ] Report/observation revisions remain identical in every variant
- [ ] Director verdict never authorizes a design change
- [ ] Mutation guard passes

## Case 19: Gate counts distinct verified sessions with build/profile binding

### Fixture

Provide three distinct verified sessions; duplicate one ID; reuse report bytes
under another filename; include protocols/raw/ledgers/reviews/legacy/partial
reports; and vary build/profile across valid sessions.

### Input

Verify each explicit report/receipt, then evaluate the resulting identities as a
consumer fixture.

### Expected writes

None.

### Expected behavior

Exactly three distinct validated session IDs count. Duplicate/copy/non-result
artifacts do not. Each counted session exposes report, manifest, bundle, build
artifact, platform profile, protocol, and recorder revisions; no directory count is
used.

### Assertions

- [ ] Session uniqueness derives from validated identity, not path count
- [ ] Same build/profile across distinct sessions is allowed and disclosed
- [ ] Changed build/profile cannot reuse another session receipt
- [ ] Noncanonical artifacts count zero sessions
- [ ] Mutation guard passes

## Case 20: Zero-write and authority boundary across all modes

### Fixture

Include existing protocols, sessions, raw data, observations, reports, reviews,
bug registry, GDDs, backlog, gate records, and requests to save/update/create or
chain work.

### Input

Run every mode, including complete and partial variants, while requesting writes,
bug creation, design edits, priority decisions, gate updates, and report repair.

### Expected writes

None under all variants.

### Expected behavior

The skill returns one mode-appropriate candidate/assessment/verification and
stops. Unauthorized instructions cannot expand authority. Persistence, bug/GDD/
backlog changes, product priority, gate updates, and follow-up workflows remain
separate explicit work.

### Assertions

- [ ] Before/after repository snapshots are byte-identical
- [ ] Mutation-attempt ledger is empty for workflow/adapters/reviewer
- [ ] No write-authorization branch exists
- [ ] No workflow, issue, task, or external approval is started
- [ ] Metadata, skill, and spec describe the same zero-write boundary

---

## Audit finding traceability

| Audit finding | Closing contract clauses | Behavioral proof |
|---|---|---|
| PTR-004 | Exact four-mode grammar, strict path/options, legacy replacement, no inferred artifacts | Case 1 |
| PTR-005 | Only direct revision-bound hypothesis/GDD/AC context; eight-file/256-KiB bounds and omissions | Case 8 |
| PTR-006 | Independent participant rows, pseudonymous identities, n/N/segments, majority/minority/missing | Cases 5, 9 |
| PTR-007 | Versioned profile includes Feel, Accessibility, Design Feedback, metrics, and owner next steps | Cases 2, 10, 16 |
| PTR-008 | Stable occurrence/stable key, exact canonical bug lookup, unlinked candidate without writes | Case 13 |
| PTR-009 | Immutable build/source/platform/protocol/hypothesis/AC/raw/participant/consent identity and stale detection | Cases 3-6 |
| PTR-010 | Optional bounded director review is separate; failure is review PARTIAL without changing session completion | Case 18 |
| PTR-011 | Stable finding schema, evidence trace, n/N, limitations, impact/confidence/priority separation and deterministic order | Cases 14, 15 |

Additional parent-requested metric/statistics/sample, bounded ingest, stable
evidence, report finalization, gate eligibility, and recorder separation receive
positive and negative coverage in Cases 7, 11, 12, 16, 17, 19, and 20.

---

## Pass criteria

- [ ] Every static assertion passes
- [ ] Cases 1-20 pass with all required instrumentation
- [ ] Mutation guard passes for the workflow, adapters, and optional reviewer in
  every case
- [ ] All protocol/session/bundle/raw/observation/context/report/receipt revisions,
  stable finding/occurrence IDs, and omission reference IDs independently recompute
- [ ] PTR-004 through PTR-011 each have positive and negative/boundary proof
- [ ] No missing consent, provenance, declared revision, observation trace, required
  context, required sample, or bounded tail produces complete/gate evidence
- [ ] No raw/observation fact is rewritten as inference or unsupported cause
- [ ] No template, ingest assessment, candidate response, partial report,
  director review, noncanonical file, or directory count becomes gate-eligible
- [ ] Only independent recorder verification can produce actual gate eligibility
- [ ] Repeated deterministic fixtures produce identical metrics, findings,
  ordering, revisions, and omission proofs apart from controlled run metadata
- [ ] Live skill/spec/metadata, P0 staging, shared files, and catalog result fields
  remain unchanged by this candidate

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
