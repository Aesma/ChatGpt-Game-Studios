# Skill Test Spec: $test-flakiness

## Skill Summary

`$test-flakiness` analyzes an explicit run-set manifest. It may optionally write
one hash-named analysis report under `production/qa/flakiness/`, but it never
modifies tests, CI, runner configuration, run receipts, or
`tests/regression-suite.md`.

Flakiness statistics are computed only inside homogeneous cohorts with the same
commit, build, test binary, runner/config, engine, platform, environment, seed,
and order identity. Only independent clean-process runs count.

The workflow reports operation and evidence separately. Report persistence is
not quarantine approval or application.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; the name
  matches the skill directory.
- [ ] At least two phase headings exist.
- [ ] Input requires `run-set: manifest-path`; a single legacy log is not a valid
  run set.
- [ ] Homogeneous cohort identity includes commit, build, binary, config,
  platform/environment, and seed.
- [ ] Fewer than two independent runs yields `INSUFFICIENT EVIDENCE`.
- [ ] Three runs with one failure is `SUSPECTED FLAKY`, never immediate
  quarantine.
- [ ] Confirmation and quarantine eligibility have explicit minimum samples.
- [ ] Quarantine requires owner, expiry, issue, replacement/risk, approval, and
  rollback fields.
- [ ] The skill cannot write `tests/regression-suite.md`, test source, or CI.
- [ ] Metadata says quarantine remains external.
- [ ] Operation and evidence verdicts are independent.

---

## Case 1: Different commit or config is heterogeneous evidence

### Fixture

- `run-set-a.yaml` references four valid result receipts for the same stable test
  ID.
- Commit/config A has two PASS results.
- Commit/config B has two FAIL results.
- Every receipt has a valid raw-byte hash and complete identity.
- Record pre-run bytes for all files.

### Input

`$test-flakiness run-set: run-set-a.yaml`

### Expected writes

- None.

### Expected non-writes

- Run set, receipts, tests, CI, regression manifest, and QA files remain
  byte-for-byte unchanged.

### Expected behavior and verdict

1. Runs are separated into two cohort keys.
2. Outcomes are not aggregated into one rate.
3. The test is not called flaky.
4. Operation is `ANALYZED`; evidence is `HETEROGENEOUS EVIDENCE`.
5. No quarantine proposal is eligible.

### Assertions

- [ ] Commit/build/config differences are named.
- [ ] No combined PASS/FAIL denominator exists.
- [ ] No `CONFIRMED FLAKY` or quarantine recommendation appears.

---

## Case 2: One independent run is insufficient

### Fixture

- A valid run-set manifest contains one independent, clean-process PASS or FAIL
  receipt for `TC-combat-S001-AC01`.
- All identity and hash fields are valid.

### Input

`$test-flakiness run-set: one-run.yaml`

### Expected writes

- None.

### Expected non-writes

- Entire fixture tree remains byte-for-byte unchanged.

### Expected behavior and verdict

1. No flakiness rate is computed.
2. Operation is `ANALYZED`.
3. Evidence is `INSUFFICIENT EVIDENCE`.
4. The result requests at least one more homogeneous independent run and does
   not suggest quarantine.

### Assertions

- [ ] A single PASS is not “no flakiness.”
- [ ] A single FAIL is not “flaky.”
- [ ] No quarantine state beyond absent/ineligible is emitted.

---

## Case 3: Legacy single CI log is not a run set

### Fixture

- `ci-output.log` contains one PASS and one retry FAIL line, but no run-set
  manifest and no independent run identity.
- The file may repeat the same test name several times.

### Input

`$test-flakiness ci-output.log`

### Expected writes

- None.

### Expected non-writes

- Log, tests, CI, and regression manifest remain unchanged.

### Expected behavior and verdict

1. The legacy input is rejected as a run-set source.
2. Repeated lines/retries are not counted as independent runs.
3. Operation is `ANALYZED`; evidence is `INSUFFICIENT EVIDENCE`.
4. Guidance names the required run-set identity fields.

### Assertions

- [ ] A single file is not assumed to contain independent runs.
- [ ] No failure rate or flaky classification is calculated.
- [ ] No persistence authorization is requested without `--persist`.

---

## Case 4: Three runs with one failure is suspected only

### Fixture

- One complete homogeneous cohort has three independent clean-process runs:
  two PASS and one FAIL.
- Stable test identity and all receipt hashes validate.

### Input

`$test-flakiness run-set: three-runs.yaml --persist`

The user declines report persistence.

### Expected writes

- None.

### Expected non-writes

- Run set, receipts, report path, regression manifest, tests, and CI remain
  unchanged.

### Expected behavior and verdict

1. Counts and the Wilson interval are reported.
2. Evidence is `SUSPECTED FLAKY`, not `CONFIRMED FLAKY`.
3. Quarantine is `INELIGIBLE` regardless of the 33.3 percent point estimate.
4. Operation is `REPORT_DECLINED`; the analysis remains valid and complete.

### Assertions

- [ ] Sparse sample size controls the verdict.
- [ ] A high point rate cannot bypass minimum counts.
- [ ] Declining persistence does not become analysis `BLOCKED`.

---

## Case 5: Controlled homogeneous reproduction confirms flakiness

### Fixture

- A controlled reproduction manifest identifies ten independent isolated runs
  with one identical complete cohort key.
- The stable test produces eight PASS and two FAIL outcomes.
- No result is a retry, aborted run, duplicate, or resumed attempt.
- All manifest/result hashes and stable identities validate.

### Input

`$test-flakiness run-set: controlled-repro.yaml`

### Expected writes

- None.

### Expected non-writes

- Tests, CI, receipts, regression manifest, and all evidence remain unchanged.

### Expected behavior and verdict

1. All ten runs enter one cohort and denominator.
2. Evidence is `CONFIRMED FLAKY`.
3. The controlled-reproduction path satisfies evidence eligibility for a
   quarantine proposal, but no quarantine is approved or applied.
4. Operation is `ANALYZED`.

### Assertions

- [ ] At least two PASS and two FAIL are present.
- [ ] Exact identity equality and independence are verified.
- [ ] Confirmation does not mutate any file or state.

---

## Case 6: Incomplete quarantine proposal is rejected

### Fixture

- Start with confirmed evidence from Case 5.
- A draft proposal omits owner, expiry, tracking issue, replacement coverage,
  player/release risk, or rollback criteria.

### Input

Request a quarantine recommendation for the confirmed test.

### Expected writes

- None.

### Expected non-writes

- No proposal application, test annotation, CI change, report update, or
  regression-manifest update occurs.

### Expected behavior and verdict

1. Every missing mandatory field is listed.
2. State is at most `CONFIRMED`.
3. Quarantine is `QUARANTINE INELIGIBLE`, not `PROPOSED`, `APPROVED`, or
   `APPLIED`.
4. “Make CI green” is rejected as a rationale.

### Assertions

- [ ] Owner, expiry, issue, replacement/risk, approval, and rollback are all
  mandatory.
- [ ] Confirmation alone cannot authorize quarantine.
- [ ] No generic pytest instruction is emitted for a non-Python engine.

---

## Case 7: Proposal, approval, application, and verification remain distinct

### Fixture

- A complete eligible proposal exists in a flakiness report.
- Variant A has no external approval or application receipt.
- Variant B has an approval record but no application receipt.
- Variant C has an application receipt with changed adapter/config hashes but no
  subsequent runner receipt.
- Variant D adds a runner receipt bound to the applied config hash and exact
  stable test ID, recording it as skipped/quarantined.
- `tests/regression-suite.md` bytes are recorded before the check.

### Input

`$test-flakiness status: production/qa/flakiness/flakiness-report-run-a.md`

### Expected writes

- None.

### Expected non-writes

- Regression manifest, tests, CI/config, reports, and receipts remain
  byte-for-byte unchanged.

### Expected behavior and verdict

1. Variant A reports `PROPOSED` only.
2. Variant B reports `APPROVED` only.
3. Variant C reports `APPLIED` only.
4. Variant D reports `VERIFIED`.
5. Only APPLIED/VERIFIED receipt paths and hashes are handed to the
   `$regression-suite` owner for a future keyed upsert.
6. This workflow never performs that upsert.

### Assertions

- [ ] State never advances without the exact external receipt.
- [ ] Approval and application are independent changesets.
- [ ] Regression manifest bytes remain unchanged.
- [ ] Expired proposals/applications require revalidation and cannot hide the
  test indefinitely.

---

## Case 8: Optional report write is isolated and concurrency-safe

### Fixture

- A complete analysis report is generated from a valid run set.
- Record raw bytes/hashes of the run-set manifest and every included receipt.
- The report target does not exist for the first variant.
- In a second variant, an existing target changes after preview.

### Input

`$test-flakiness run-set: run-set-a.yaml --persist`

The user approves the exact one-file report changeset.

### Expected writes

- First variant: write only
  `production/qa/flakiness/flakiness-report-[run-set-id]-[hash-prefix].md`.
- Second variant: no write after the target hash conflict.

### Expected non-writes

- `tests/regression-suite.md`, tests, CI, run set, receipts, and quarantine state
  remain unchanged in both variants.

### Expected behavior and verdict

1. Sources are rehashed immediately before writing.
2. First variant read-back verifies the report and returns
   `Operation: REPORT_WRITTEN` with its SHA-256.
3. Second variant preserves the concurrent edit and returns
   `Operation: FAILED`.
4. Evidence verdict is reported independently in both variants.
5. Neither variant claims quarantine application or regression-manifest update.

### Assertions

- [ ] The filesystem diff contains at most the one owned report.
- [ ] Written status requires byte-for-byte read-back.
- [ ] Concurrent user edits are not overwritten.
- [ ] Report persistence is not a quarantine gate.

---

## Protocol Compliance

- [ ] Statistics use only homogeneous independent runs.
- [ ] Invalid, retry, skipped, aborted, and partial records have explicit
  denominator rules.
- [ ] Single-run and legacy single-log inputs cannot diagnose flakiness.
- [ ] Sparse mixed outcomes remain suspected.
- [ ] Quarantine eligibility has sample and completeness gates.
- [ ] Quarantine state follows external approval/application/runner receipts.
- [ ] `tests/regression-suite.md` has exactly one owner and is never written here.
- [ ] Operation and evidence statuses remain independent.

---

## Coverage Notes

- The staged regression-suite contract consumes only exact APPLIED/VERIFIED
  quarantine receipt paths/hashes; a flakiness report alone is insufficient.
- Runner/application receipt production remains an external test/CI owner
  responsibility.
- The CGS catalog and workflow guides remain unchanged because this staging task
  does not own shared files.
