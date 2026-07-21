---
name: story-done
description: "Fail-closed end-of-story completion review. Verifies every required acceptance criterion with current hash-bound automated or manual evidence, enforces story-type evidence, preserves readiness and dev-story provenance, and only then closes the story."
---

## Invocation and execution

Invoke this workflow as $story-done [story-file-path] [--review full|lean|solo].
The story path is optional only for story selection.

Before the first file mutation, present one complete changeset preview listing
every target path and intended change and obtain one explicit approval. Existing
bounded authorization may satisfy this requirement when it already names the
same complete write set. Any new path or material change invalidates the preview
and requires a revised approval. Never ask again per file inside an unchanged
approved changeset.

# Story Done

This workflow is the sole owner of the In Review -> Complete transition. It
consumes the provenance and test handoff produced by $dev-story, revalidates the
current story and implementation, and computes a fail-closed completion verdict.

A story is closable only when every required acceptance criterion has a concrete
PASS result on the current verification tree and every evidence requirement for
the declared story type is satisfied. File existence, symbol names, keyword
searches, numeric scans, and a conversational Yes are findings, not acceptance
evidence.

Outputs:

- COMPLETE, COMPLETE WITH NOTES, or BLOCKED;
- a per-criterion evidence table;
- a provenance and freshness report;
- on an approved closable verdict, the updated story and normal status/session
  projections; and
- the next ready story or sprint close-out sequence.

---

## Phase 0: Resolve mode and select the story

Resolve review mode once:

1. Use --review when supplied.
2. Otherwise read production/review-mode.txt.
3. Otherwise default to lean.

When a path is supplied, read exactly that file. With no path, check
production/session-state/active.md, then the newest current sprint file for an In
Review story. If more than one candidate exists, ask the user to select one. If
none exists, request a path.

Read the selected story in full before delegation or mutation. Record the SHA-256
of its raw bytes as story_baseline_hash. The expected lifecycle state is In
Review. A story in Ready, In Progress, Draft, Blocked, Complete, or an
unrecognized state is BLOCKED for closure. When production/sprint-status.yaml
exists, its story projection must identify the same story and be in_review;
otherwise report the mismatch as BLOCKED.

---

## Phase 1: Load and revalidate the implementation handoff

### 1.1 Required dev-story handoff

Read the implementation handoff recorded in the story by $dev-story. Accept
Markdown or structured YAML presentation, but require unambiguous values for:

- plan_hash in sha256:<64 lowercase hexadecimal> form;
- each implementation and test/evidence path and its post-write raw SHA-256;
- source-context paths and the raw SHA-256 values used for implementation;
- every test command, working directory, start/end timestamp, exit code, raw log
  SHA-256, and recorded PASS/FAIL/BLOCKED result;
- acceptance-criterion coverage from the approved plan;
- manifest provenance state, implemented_against_hash, the then-current manifest
  hash, and any manifest waiver ID; and
- dependency waiver IDs, when present.

Missing, malformed, ambiguous, or duplicate fields are BLOCKED. A prose claim
that tests passed is not a substitute for the handoff.

Hash every listed implementation and test/evidence file now. Each current hash
must equal its recorded post-write hash. A missing file or mismatch makes all
evidence depending on that file stale and blocks closure.

Compute verification_tree_hash as SHA-256 over canonical UTF-8 lines sorted by
normalized path:

    plan_hash=<plan_hash>
    <normalized implementation, automated-test, config, or runtime-input path>\tsha256:<current raw hash>

Exclude the story, status/session files, raw logs, screenshots, and the manual
evidence record itself; hash those evidence artifacts separately. This avoids a
self-referential evidence hash while binding the exact executable/tested inputs.
Use lowercase hexadecimal hashes and LF separators. Record the resulting
sha256:<64hex> value in the completion report and closure record. This value is
the current subject-tree binding for manual evidence.

### 1.2 Readiness and source provenance

Independently re-read and hash the sources required by the staged
$story-readiness/$dev-story contract:

- docs/architecture/tr-registry.yaml;
- docs/architecture/control-manifest.md;
- every governing ADR;
- every GDD or additional source named in the story or dev-story handoff; and
- any Definition-of-Done profile that changes the default evidence matrix.

Verify exact active TR-IDs, Accepted ADR status, the current raw manifest hash,
the story Manifest Version and Manifest Hash, and the Source Snapshot manifest
entry. A prior story-readiness report may be consumed as provenance only when its
recorded source hashes equal the current hashes; it never replaces this
revalidation.

For normal provenance, the story header and Source Snapshot must match the
current manifest, and the dev-story source-context hashes must still match all
current sources.

For a staged dev-story result labeled STALE / ACCEPTED-RISK, preserve that label
and validate the structured manifest waiver:

- waiver_id is present;
- implemented_against_hash equals the story's captured Manifest Hash and Source
  Snapshot hash;
- the waiver current_hash equals both the current manifest hash observed by
  dev-story and the manifest hash observed now; and
- every non-manifest readiness/source check passes.

A valid branch may continue but can produce at most COMPLETE WITH NOTES. It must
never be relabeled READY or CURRENT. A missing or inconsistent waiver, a second
manifest change, or any other source hash change is BLOCKED.

Do not refresh story provenance inside this workflow. Route stale normal
provenance back through the owning story update workflow, final
$story-readiness, and $dev-story.

---

## Phase 2: Resolve acceptance criteria and evidence

### 2.1 Required versus optional criteria

Read every acceptance criterion verbatim and retain its order. Every criterion
is required by default.

A criterion is optional/non-blocking only when the story explicitly declared it
that way before the approved dev-story plan, the plan coverage records the same
classification, and the declaration is covered by an unchanged hashed
Definition-of-Done profile or story source. A runtime request to defer, accept,
or downgrade a required criterion is invalid.

Use the story's explicit stable AC ID when present. Otherwise use
AC-<ordinal>@<plan_hash> as a run-local identifier bound to the approved plan's
exact criterion mapping. Do not match evidence by similar wording.

For each criterion record one of PASS, FAIL, UNTESTED, DEFERRED, or STALE.
COVERED is a mapping state, not a passing result.

### 2.2 Evidence that can produce PASS

A required criterion may PASS only from one or more current evidence records that
directly exercise its observable behavior.

Automated evidence must include:

- criterion ID and test/evidence ID;
- exact test locator or scenario;
- exact command and working directory;
- start and end timestamps;
- exit code 0;
- recorded result PASS;
- raw log SHA-256;
- the approved plan mapping; and
- current file hashes equal to the dev-story post-write hashes.

The dev-story handoff format described in Phase 1 is valid automated evidence
when all these values are present and unchanged. An unrun command, missing log
hash, nonzero exit, FAIL/BLOCKED result, or ambiguous criterion mapping cannot
PASS a criterion.

Manual evidence must be a record in the declared evidence artifact and include:

- evidence_id and exact criterion_id;
- tested_tree_hash equal to the current verification_tree_hash;
- optional build artifact path and raw build_hash, when a packaged build was
  tested;
- reproducible steps;
- observed result;
- explicit PASS result;
- tester identity or stable tester handle;
- ISO-8601 session timestamp; and
- artifact links sufficient for the declared story type.

A conversational Yes/No/Not tested answer, an unsigned checklist, or a sign-off
without steps and observations is not manual evidence. If the tree or build hash
changes, the record is STALE. Capture of a newly completed manual record may be
proposed as an evidence-file write, but it cannot count until all fields and
artifacts exist and its exact path is included in the approved changeset.

Static inspection may produce findings only:

- file or dependency existence;
- symbol, function, class, number, or string searches;
- hardcoded-value/localization scans; and
- name similarity between a criterion and a test.

Never use these findings alone to mark PASS, COVERED, or VERIFIED.

### 2.2a Optional test-evidence-review receipt

If a durable `$test-evidence-review` report is supplied, treat it only as a
hash-bound summary of the evidence below. Require its exact canonical report
path and hash, its exact review-manifest path/hash, and revalidate every captured
QA-plan, story/AC, candidate/build, test source, smoke/playtest/manual artifact,
attestation, and receipt hash. It can support closure only when all axes say:

- `Workflow Status: COMPLETE`;
- `Overall Evidence Quality: ADEQUATE`;
- `Overall Execution Status: PASS`;
- required `Execution Scope: FULL`;
- `Closure Eligible: YES`; and
- verified durable persistence with no stale binding.

`ADEQUATE` alone never means tests ran. `PASS` without adequate evidence, a
targeted execution scope, conversation-only output, missing review manifest, or
any `UNKNOWN`, `STALE`, `UNAVAILABLE`, `INCOMPLETE`, or hash mismatch blocks
closure. A supplied review does not waive the per-criterion checks in this
phase; direct evidence may be used instead when no review is supplied.

### 2.3 Blocking evidence matrix by story type

Apply the strict default matrix. A predeclared, hash-bound Definition-of-Done
profile may replace a row only when it was already part of the story and approved
dev-story plan; no closure-time simplification is allowed.

| Story Type | Blocking type evidence |
|---|---|
| Logic | Current passing automated unit-test evidence; every required logic criterion must map to a passing automated test unless the predeclared profile names another method. |
| Integration | Current passing integration-test evidence or a current hash-bound manual end-to-end session for every required integration criterion. |
| Visual/Feel | Current hash-bound manual session, required screenshots/artifacts, and all required sign-offs. |
| UI | Current hash-bound manual walkthrough with artifacts or a passing automated interaction test, plus any sign-off required by the declared profile. |
| Config/Data | Current passing smoke-check evidence bound to the changed data/tree. |

A missing or unknown Story Type is BLOCKED. Missing files, pending sign-offs,
missing artifacts, stale hashes, or evidence that does not directly cover every
required criterion are BLOCKED for every type. They are never advisory.

All required criteria must be PASS. A required FAIL, UNTESTED, DEFERRED, or
STALE criterion blocks closure even if only one criterion is affected. An
optional criterion may be DEFERRED only under its predeclared classification and
must appear in Completion Notes.

---

## Phase 3: Design, QA, and code-review findings

Compare the implementation and evidence against the current TR requirement, GDD
rules, Accepted ADRs, control-manifest constraints, and the approved file scope.

Static searches may help locate a possible deviation, but neither presence nor
absence of a keyword proves behavioral conformance. A design rule is satisfied
only by the criterion evidence assembled in Phase 2. Record hardcoded-value,
localization, dependency, and out-of-scope scans as findings.

Use the existing project review-mode contract for QL-TEST-COVERAGE and
LP-CODE-REVIEW:

- full invokes the applicable gates;
- lean and solo follow their configured skip/prompt behavior; and
- record exact gate results or skips.

Apply any existing blocking QA or code-review result as BLOCKED. Retain advisory
gate findings in Completion Notes. These gates cannot turn missing or stale
acceptance evidence into PASS and cannot override any Phase 1 or Phase 2 blocker.

---

## Phase 4: Compute and present the verdict

Compute the verdict deterministically before any write.

BLOCKED when any of the following is true:

- lifecycle/tracker preconditions fail;
- the dev-story handoff, plan hash, file hash, test-log evidence, or source hash
  is missing, malformed, or stale;
- normal readiness provenance is not current, or an accepted-risk waiver is
  invalid;
- Story Type is missing/unknown or its blocking type evidence is incomplete;
- any required criterion is FAIL, UNTESTED, DEFERRED, STALE, or lacks direct
  evidence; or
- a blocking deviation or gate result remains.

COMPLETE when every required criterion is PASS on the current verification tree,
all blocking type evidence passes, provenance is CURRENT, and no blocking or
advisory item remains.

COMPLETE WITH NOTES only when the complete conditions hold and all remaining
items are non-blocking by a pre-existing rule, such as a predeclared optional
criterion, a valid STALE / ACCEPTED-RISK manifest waiver, or an advisory review
finding. It never accommodates a required evidence gap.

Present:

    ## Story Done: [story ID] — [verdict]
    Story: [path]
    Story baseline: sha256:[hash]
    Dev plan: sha256:[hash]
    Verification tree: sha256:[hash]
    Manifest provenance: [CURRENT or STALE / ACCEPTED-RISK]
    Implemented against: sha256:[hash]
    Current manifest: sha256:[hash]

    ### Acceptance evidence
    | AC ID | Required | Evidence IDs | Method | Freshness | Result |
    |---|---:|---|---|---|---|
    | ... | yes/no | ... | automated/manual | current/stale | PASS/... |

    ### Story-type evidence
    - [required item] — [evidence ID/path/hash] — [PASS/BLOCKED]

    ### Sources and gates
    - [path/gate] — [hash/result]

    ### Findings and notes
    - [finding or None]

    ### Verdict
    [COMPLETE / COMPLETE WITH NOTES / BLOCKED]

If BLOCKED, make no file mutation, do not offer a completion override, and list
the exact evidence or revalidation needed. A user's acceptance of risk cannot
convert a required evidence blocker into a closable verdict.

---

## Phase 5: Record an approved closure

Only COMPLETE or COMPLETE WITH NOTES may enter this phase.

Present the complete write set once and ask whether to apply it. The ordinary
closure set is:

- the selected story;
- production/sprint-status.yaml, when it exists;
- production/session-state/active.md; and
- docs/tech-debt-register.md only when the user chooses to log existing advisory
  findings.

If a newly captured manual evidence record is part of the run, its exact evidence
path must also appear in this preview before any write.

Rehash every target immediately before the first write. If the story no longer
matches story_baseline_hash or any other target changed since preview, stop and
recompute the report and changeset.

When the sprint tracker exists, first validate its `sprint_id`,
`active_sprint_id`, `plan_revision`, `story_set_hash`, and `updated_at` with the
exact `$sprint-status` contract and capture its raw-byte preimage hash. An
invalid/conflicting tracker blocks closure. Preserve sprint identity and
`plan_revision`; never repair them by inference.

Update the story to Status: Complete, set Last Updated, and append an immutable
Completion Record containing:

- closure_transaction_id;
- completion timestamp;
- story_baseline_hash and plan_hash;
- verification_tree_hash;
- manifest provenance state, implemented_against_hash, current manifest hash,
  and waiver IDs;
- source-context hashes;
- every criterion ID, required/optional classification, result, and evidence ID;
- every automated command/cwd/exit/timestamp/log hash;
- every manual evidence record path, tested tree/build hash, tester, timestamp,
  and artifact links;
- story-type evidence result;
- QA/code-review result or skip; and
- final verdict and advisory notes.

Update the matching sprint tracker entry to done/completed and append the session
extract using the same closure_transaction_id. Do not modify implementation files
or rewrite source provenance. If a write fails, report exactly which projections
were and were not updated and do not claim closure succeeded.

Because the story bytes change to `Complete`, recompute tracker
`story_set_hash` from the complete current story set using sorted
`ID<TAB>path<TAB>raw-byte-hash` records and set a timezone-qualified
`updated_at` in the same closure transaction. Re-read the story, tracker, and
session projection; verify the shared transaction ID, tracker preimage CAS,
unchanged `plan_revision`, and recomputed story-set hash before reporting
closure.

Suggest a commit command, but never commit, push, or publish without a separate
user instruction.

---

## Phase 6: Surface the next story

After a successful closure, read the current sprint and surface up to three Must
Have or Should Have stories whose recorded state and dependency state make them
candidates. Recommend $story-readiness [path] before $dev-story.

When all Must Have stories are complete, present the existing sprint close-out
sequence: smoke check, team QA, retrospective, gate check after QA approval, and
the next sprint plan. Do not execute those workflows automatically.

---

## Non-negotiable rules

- Static presence or keyword checks never PASS an acceptance criterion.
- Every required criterion needs direct current PASS evidence.
- Every story type's declared evidence is blocking.
- Manual evidence is identity-, session-, artifact-, and tree/build-hash bound.
- Changed story/source/tree/build hashes make dependent evidence stale.
- A required gap can never be hidden in COMPLETE WITH NOTES.
- Accepted risk preserves its provenance label and never means READY/CURRENT.
- BLOCKED cannot be overridden into closure.
- Only this workflow may write Complete/Done for the story lifecycle.
