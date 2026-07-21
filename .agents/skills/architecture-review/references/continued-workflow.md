# Architecture Review — Required workflow continuation

This continuation is part of the public $architecture-review contract. It may
format and optionally save one immutable report; it must not repair or record
changes in any reviewed source.

## Phase 8: Build the immutable report

Produce a schema-versioned report with these fields in this order:

1. schema_version
2. report_id — unique UTC timestamp plus the first 12 characters of
   target_manifest_hash
3. generated_at_utc
4. mode and exact target scope
5. source_revision
6. target_manifest_hash
7. complete target manifest: source type, canonical project-relative path, and
   complete-file SHA-256 for every input
8. input-class status: PRESENT, MISSING, or NOT_APPLICABLE
9. reviewer status for each required reviewer: DONE, DECLINED, TIMEOUT, ERROR,
   or NOT_APPLICABLE, with the manifest hash reviewed
10. admitted owner-approved requirements and CANDIDATE_REQUIREMENT findings
11. exact requirement-to-ADR traceability states
12. story/test linkage and test-run evidence states when in scope
13. consistency, dependency, and engine findings
14. deterministic verdict: PASS, BLOCKED, or PARTIAL
15. blocking and incomplete-evidence reasons
16. mutation-guard result
17. stale key: the target_manifest_hash that a consumer must reproduce

Every finding must include a stable report-local finding ID, severity/category,
source path and source hash, exact evidence location, destination owner, status,
and an acceptance test. Findings are observations only; do not edit their
destination files.

The report must say that:
- implicit or prose-similar links are UNVERIFIED_LINK
- a discovered test file is DISCOVERED_NOT_EXECUTED
- only current EXECUTED_PASS is passing evidence
- ACCEPTED_RISK is a separate owner record and cannot change the verdict
- any manifest change makes this report STALE

## Phase 9: Present before any optional save

First present the complete report in conversation.

Default behavior is no file write. If the user has not asked to save the report,
return it in conversation and continue to the final mutation check.

If the user asks to save it:

1. Propose one exact new project-relative report path. Prefer
   docs/architecture/reviews/architecture-review-<UTC>-<manifest12>.md.
2. Confirm the path does not exist. Existing reports are immutable and may not be
   overwritten, appended to, renamed by this workflow, or selected by a vague
   latest rule.
3. Show the complete report content and list the report path as the complete
   changeset.
4. Obtain one explicit approval before the first file change.
5. Create only that report. Do not create missing parent policy/index files,
   update a latest pointer, or modify any other path.
6. Re-read the saved bytes, compute its SHA-256, and report that artifact hash in
   conversation. Do not place a self-referential artifact hash inside the report.

Authorization to save the report never authorizes edits to:

- docs/architecture/tr-registry.yaml
- any GDD, ADR, architecture.md, systems-index, or traceability index
- requirements-traceability.md
- consistency-failures.md or any review/reflexion log
- production/session-state
- stories, tests, test-run evidence, signoff, or accepted-risk records

## Phase 10: Final mutation guard

Immediately before returning:

1. Repeat the Phase 0 project snapshot.
2. Compare every project-relative path, size, and SHA-256 against the baseline.
3. Permit no differences when the report was conversational only.
4. When a report was explicitly authorized and saved, permit only the exact new
   report path. A pre-existing path or a second changed path is never permitted.
5. If any unauthorized difference exists, list all changed paths, set
   mutation_guard to FAILED, return BLOCKED, and stop. Do not hide, repair,
   revert, or normalize the change.
6. Otherwise set mutation_guard to PASSED.

The mutation check itself is read-only.

## Phase 11: Staleness and risk disposition

When evaluating a prior report, rebuild the manifest from its recorded exact
scope. Return CURRENT only when every path, source type, revision, and SHA-256
reproduces target_manifest_hash. Otherwise return STALE and list the differences.
A stale report cannot satisfy a gate.

If a separately owned ACCEPTED_RISK record is supplied, verify its report ID,
finding IDs, exact scope, target manifest hash, owner signature, signed timestamp,
and expiry. Report its validity separately as risk_disposition. Never rewrite the
review verdict and never create, sign, renew, or store the risk record.

## Phase 12: Handoff and stop

Return:

- report ID and target_manifest_hash
- artifact path/hash if a report was saved
- PASS, BLOCKED, or PARTIAL with the exact machine reason codes
- the single highest-priority finding and its destination owner
- one recommended fresh-task handoff

Do not invoke the handoff, modify a destination file, update session state, or
automatically rerun after another ADR. Stop after the handoff.
