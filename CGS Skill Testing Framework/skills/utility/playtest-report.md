# Skill Spec: $playtest-report

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

$playtest-report creates collection protocols, ingests immutable participant evidence, and finalizes canonical build-bound session results. Protocols, raw evidence, observation ledgers, completed reports, and creative-director reviews are separate artifacts. Only a structurally valid production/playtests/<session-id>/report.md with Status: COMPLETED and Gate Eligible: YES counts as a playtest session.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is playtest-report
- [ ] The workflow defines template, ingest, finalize, and review modes plus invalid-mode behavior
- [ ] The only canonical completed result path is production/playtests/<session-id>/report.md
- [ ] Template and ingest modes explicitly prohibit Status: COMPLETED, Verdict: COMPLETE, and gate eligibility
- [ ] Raw evidence and observation ledgers are immutable and separate from derived reports and director reviews
- [ ] Every derived finding requires Observation IDs and the verified raw-evidence SHA-256
- [ ] Successful finalization requires build/source/platform/time/participant/hypothesis/evidence provenance
- [ ] The workflow follows bounded changeset authorization and transactional write rules
- [ ] The final section routes follow-up candidates without invoking or mutating downstream workflows

---

## Director Gate Checks

- **Full mode**: CD-PLAYTEST runs only after a canonical completed report is written and receives exact report bytes plus SHA-256; its separate review must echo that hash.
- **Lean mode**: CD-PLAYTEST is skipped and session completion is unchanged.
- **Solo mode**: CD-PLAYTEST is skipped and session completion is unchanged.
- **Failure behavior**: timeout, malformed output, or hash mismatch yields Session Verdict: COMPLETE plus Director Review Status: PARTIAL; it never fabricates APPROVE or rewrites evidence.

---

## Test Cases

### Case 1: Template is not a completed session

**Fixture**:
- Invocation: $playtest-report template onboarding-v2 --save-protocol
- The bounded request authorizes production/playtests/_protocols/onboarding-v2.md.

**Expected behavior**:
1. The skill produces only the protocol artifact.
2. It labels the artifact as playtest-protocol with Status: TEMPLATE.
3. It returns TEMPLATE_READY and Gate Eligible: NO.

**Assertions**:
- [ ] No session directory or report.md is created
- [ ] No Status: COMPLETED or Verdict: COMPLETE is emitted
- [ ] A gate scan cannot count the protocol as a session
- [ ] Protocol fields include per-participant accessibility and evidence placeholders

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Missing or out-of-bounds notes fail closed

**Fixture**:
- Invocation points to a missing file, directory, symlink escaping the project root, unsupported type, or file above 10 MiB.

**Expected behavior**:
1. The skill resolves and validates the literal real path before any write.
2. It reports the failed validation and Verdict: ERROR.
3. It creates no session, raw receipt, report, review, or completion verdict.

**Assertions**:
- [ ] No artifact is written
- [ ] No COMPLETE or gate-eligible status appears
- [ ] The rejected path and failed check are identified

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Finalize a traceable build-bound session

**Fixture**:
- Session PT-combat-001 has a complete manifest, immutable copied notes, and an observation ledger.
- Build version/hash, source commit, platform profile, hypothesis ID, participant IDs, timestamps, consent, and evidence receipt are present.
- At least one finding references valid Observation IDs and the raw SHA-256.

**Expected behavior**:
1. The skill re-hashes raw evidence and validates every observation source reference.
2. It creates the derived sections Feel and Accessibility, Bugs Observed, Design Feedback, Balance and Polish, Next Steps, and a traceability matrix.
3. It writes only production/playtests/PT-combat-001/report.md atomically.
4. It re-reads the result before emitting COMPLETE and a hash receipt.

**Assertions**:
- [ ] Header contains Artifact Type: playtest-session-result, Status: COMPLETED, and Gate Eligible: YES
- [ ] Every finding resolves to observation IDs and the same raw evidence hash
- [ ] Verbatim excerpts remain unchanged and interpretations are labelled DERIVED
- [ ] Manifest, ledger, raw evidence, and report hashes are reported
- [ ] This completed session counts exactly once

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Multiple participants preserve majority and minority evidence

**Fixture**:
- Five participants provide separate observations.
- Three report confusion, one reports no confusion, and one has no answer.
- Participants include different input devices and accessibility profiles.

**Expected behavior**:
1. Ingest preserves five participant rows and separate observation IDs.
2. Finalize reports 3/4 answered participants for confusion and preserves the 1/4 minority result.
3. The unanswered participant is not silently added to either opinion denominator.
4. Device, segment, and accessibility context remain attached.

**Assertions**:
- [ ] Aggregation shows n/N and names the denominator basis
- [ ] Minority and unanswered evidence remain visible
- [ ] No participant statement is merged or rewritten
- [ ] Accessibility results identify profile and input context

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Director timeout cannot alter evidence or fabricate approval

**Fixture**:
- PT-combat-001 is already completed and hash-valid.
- Review mode is full.
- CD-PLAYTEST times out or returns a mismatched report hash.

**Expected behavior**:
1. The completed report stays byte-identical.
2. No valid director review artifact or approval is invented.
3. The result reports Session Verdict: COMPLETE and Director Review Status: PARTIAL with the reason.

**Assertions**:
- [ ] report.md and observations.md hashes do not change
- [ ] No APPROVE verdict is emitted
- [ ] No director text is mixed into raw observations or the completed report
- [ ] Lean and solo variants skip the gate without changing session completion

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Missing finalization provenance is rejected

**Fixture**:
- A session lacks one or more of build hash, source commit, platform configuration, hypothesis/AC ID, participant ID, valid start/end time, answered observation, or evidence receipt.

**Expected behavior**:
1. The skill enumerates every missing or invalid required field.
2. It emits Verdict: ERROR.
3. It writes no report.md and never marks the manifest COMPLETED.

**Assertions**:
- [ ] Partial or placeholder data cannot become gate eligible
- [ ] No COMPLETE appears
- [ ] Existing raw evidence remains untouched

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Distinct session IDs and builds are enforced

**Fixture**:
- Three valid sessions are required for a gate.
- One candidate reuses an existing session ID for different notes; another is a date-only ID; two valid sessions share a build profile intentionally.

**Expected behavior**:
1. Reused and date-only IDs are rejected.
2. Valid IDs remain independently tied to their own receipt and report hashes.
3. Gate evidence can count only distinct, validated completed IDs and display their build/profile bindings.

**Assertions**:
- [ ] Three files or directories alone are insufficient without three distinct completed session IDs
- [ ] A protocol, review, raw note, legacy-path report, or IN_PROGRESS manifest is never counted
- [ ] Each counted result exposes build hash and platform profile
- [ ] Existing completed results are never overwritten

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Treats an explicit bounded user request as authorization for all in-scope changes
- [ ] If no bounded authorization exists, previews one complete changeset and asks once before the first write
- [ ] Does not re-prompt per file, section, or edit within the authorized boundary
- [ ] Requests new direction only for material scope expansion or separately gated destructive/external action
- [ ] Validates before write and publishes multi-file ingest changes all-or-none
- [ ] Never creates files outside production/playtests without separate authorization
- [ ] Ends with artifact paths, hashes, status, gate eligibility, director status, and a mode-appropriate verdict

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime testing should supply real path, symlink, hash-mutation, multi-participant, director-timeout, and duplicate-session fixtures. Downstream gate-check, qa-plan, soak-test, test-evidence-review, workflow-catalog, and workflow-guide consumers must independently adopt the same canonical result route and validation rule.
