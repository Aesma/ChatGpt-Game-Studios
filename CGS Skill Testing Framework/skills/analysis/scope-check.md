# Skill Test Spec: $scope-check

## Skill Summary

`$scope-check` is a read-only comparator for one explicit immutable approved baseline
and one current scope manifest. It identifies additions, removals, and semantic
modifications using stable Scope IDs and content hashes. It may attach compatible
estimate, capacity, dependency, test, and decision evidence from one bounded allowlist
manifest. It never infers scope from code, uses raw item counts as a health score,
chooses Cut/Keep/Defer, mutates a plan, or re-baselines.

Canonical results are `ERROR`, `INPUT REQUIRED`, `INSUFFICIENT EVIDENCE`, `PARTIAL`,
`NO SCOPE DELTA`, and `SCOPE DELTA FOUND`.

## Static assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] Metadata describes an explicit, immutable, read-only comparison
- [ ] `compare` requires both `--baseline` and `--current`
- [ ] No feature-name, filename-similarity, or repository-scan baseline inference
- [ ] Scope classification uses stable IDs and semantic hashes
- [ ] Raw item counts and percentages cannot produce a result or impact claim
- [ ] Missing approval, baseline linkage, stable IDs, or completeness blocks
      `NO SCOPE DELTA`
- [ ] Product options are neutral and require a user/product-owner decision
- [ ] No file, Git, gate, delegation, workflow, or re-baseline mutation
- [ ] Canonical result vocabulary matches this specification exactly
- [ ] Report includes exact artifact paths, hashes, coverage, deltas, unknowns, and
      the read-only statement

## Director gate checks

None. This skill has no director gate and cannot obtain product-scope authority from
an agent recommendation.

## Test cases

### Case 1: Equal stable-ID semantics produce NO SCOPE DELTA

**Fixture**

- Approved baseline `B1/v3` has a trusted approval record, complete marker, parent
  scope `M3`, and Scope IDs `COMBAT-01`, `AI-02`, `LEVEL-03`.
- Current manifest declares the exact `B1/v3` hash, parent `M3`, completeness, and the
  same IDs and normalized semantic entry hashes.
- Current presentation order and heading formatting differ.

**Input**

`$scope-check compare --baseline <baseline> --current <current>`

**Expected**

- Both artifacts are reported with exact path, version, byte length, and SHA-256.
- Presentation-only changes do not create a delta.
- Result is `NO SCOPE DELTA`.
- The result explicitly does not mean schedule/quality approval.
- No files or state are changed.

### Case 2: One large addition and many tiny additions are not count-weighted

**Fixture**

- Variant A adds one new network subsystem Scope ID.
- Variant B adds ten small text Scope IDs.
- Neither variant has compatible estimate evidence.

**Expected**

- Both variants produce stable `ADDED` findings and `SCOPE DELTA FOUND`.
- No percent bloat, count-derived severity, or effort comparison is emitted.
- Both show `Effort Delta: UNVERIFIED`.
- The model does not claim ten text items are larger than one network subsystem.

### Case 3: Row split and merge preserve semantic scope

**Fixture**

- Baseline and current artifacts retain the same stable IDs and normalized semantic
  content, but render them as different checklist rows.

**Expected**

- Row count differences are display-only.
- No addition or removal is inferred from row count.
- Result is `NO SCOPE DELTA` when all other contract fields are complete.

### Case 4: Missing or ambiguous baseline blocks comparison

**Variants**

- no `--baseline`;
- two active-state baseline candidates;
- fuzzy feature nickname only;
- baseline lacks version or approval record;
- baseline bytes no longer match the current manifest's declared hash.

**Expected**

- Missing input returns `INPUT REQUIRED`; invalid/ambiguous resolution returns
  `ERROR`; identity or approval gaps return `INSUFFICIENT EVIDENCE`.
- No candidate is selected by similarity or modification time.
- No scope-health or delta verdict is produced.

### Case 5: No-argument invocation only discovers candidates

**Fixture**

- Active state points to exactly one milestone baseline and one sprint manifest.

**Input**

`$scope-check`

**Expected**

- The skill may display the exact suggested paths and hashes.
- It returns `INPUT REQUIRED` and asks the user to confirm both.
- It does not analyze or silently choose them in that invocation.

### Case 6: Story comparison requires an explicit parent baseline

**Fixture**

- Current story manifest explicitly references approved epic baseline path/hash `E7`.
- A similarly named milestone also exists.

**Input**

`$scope-check compare --baseline <E7> --current <story>`

**Expected**

- The story is checked against exactly `E7`, not the similarly named milestone.
- Parent and baseline hashes must match.
- A missing explicit parent link returns `INSUFFICIENT EVIDENCE`.

### Case 7: Git, code and TODO evidence cannot create scope

**Fixture**

- Git contains a leaderboard commit and code contains an achievement TODO.
- Neither has a Scope ID in the current manifest.

**Expected**

- `compare` does not scan them.
- If exact evidence paths/commits are allowlisted for `inspect`, they are labeled
  implementation evidence only.
- They do not become additions, approvals, or justification records.

### Case 8: Change justification requires a bound decision record

**Fixture variants**

- A: an addition has a change record binding Scope ID, baseline/current hashes,
  decision, owner, and timestamp.
- B: only the implementer's Git author and prose explanation exist.

**Expected**

- A is `APPROVED_CHANGE` only when every binding matches.
- B is `NO_RECORD`, not “justified”.
- Commit author is never treated as scope decision owner.

### Case 9: Product decision remains with user or designated owner

**Fixture**

- Three additions and one removal have complete evidence.
- No product decision selects a remedy.

**Expected**

- Result is `SCOPE DELTA FOUND`.
- Two or three unranked options show affected Scope IDs, known impacts, unknowns, and
  owner/action requirements.
- The skill does not recommend, rank, choose, apply, or label Cut/Keep/Defer.
- No planner or producer agent is invoked.

### Case 10: Effort and risk remain unverified without compatible receipts

**Fixture**

- Some changed IDs use hours, some use story points, and one has no estimate.
- There is no capacity receipt, test-plan coverage, or dependency evidence.

**Expected**

- No effort percentage is calculated.
- Effort delta is `UNVERIFIED`.
- Schedule, quality, and integration states are `UNVERIFIED` or `PARTIAL`, with exact
  missing fields listed.
- No intuitive Low/Medium/High rating appears.

### Case 11: Compatible evidence enables bounded impact reporting

**Fixture**

- All changed IDs have estimates using one calibrated unit/method and matching
  baseline/current hashes.
- Capacity, test-plan, and dependency receipts are complete and current.

**Expected**

- Absolute effort delta and uncertainty interval are reported.
- Impact dimensions are `SUPPORTED` with receipt paths/hashes.
- Impact evidence does not change delta types or make a product decision.

### Case 12: Evidence manifest enforces bounded context

**Variants**

- an allowlisted path hash mismatches;
- a supporting path is outside the allowlist;
- the path, byte, or commit budget is exceeded.

**Expected**

- The skill never expands the allowlist or scans for related files.
- Valid core deltas are preserved, but result is `PARTIAL` and affected impacts are
  `UNVERIFIED`.
- Unexamined entries and budget limits are explicit.

### Case 13: Immutable baseline survives repeat checks

**Fixture**

- Run 1 compares baseline hash `H1` with current `C1`.
- A planner file later changes to hash `H2` without an approved re-baseline decision.
- Run 2 still supplies `H1`; variant Run 3 supplies the changed path whose bytes are
  `H2` while current manifest still cites `H1`.

**Expected**

- Run 2 remains reproducible against immutable `H1` if bytes are available.
- Run 3 returns `INSUFFICIENT EVIDENCE — BASELINE MISMATCH`.
- The skill never treats the edited plan as an improved or replacement baseline.

### Case 14: Inputs changing during analysis invalidate conclusions

**Fixture**

- Baseline or current bytes change after initial hashing and before final reporting.

**Expected**

- Final re-hash detects the change.
- Result is `INSUFFICIENT EVIDENCE — INPUT CHANGED DURING CHECK`.
- All earlier conclusions are discarded and no partial healthy result is shown.

### Case 15: Delta findings are deterministic and reproducible

**Fixture**

- The same immutable baseline/current/evidence bytes are provided twice.

**Expected**

- Stable Delta IDs, sorted findings, coverage, optional metrics, and result are
  identical in both runs.
- Each finding contains both artifact hashes and its Scope ID/delta type.

## Protocol compliance

- [ ] Reads only explicit baseline/current artifacts and evidence-manifest allowlist
- [ ] Re-hashes every consumed artifact before reporting
- [ ] Never uses item counts or percentages as scope-health or effort metrics
- [ ] Missing evidence cannot yield `NO SCOPE DELTA`
- [ ] Never makes a product decision or silently re-baselines
- [ ] Never writes files, mutates Git, invokes gates, delegates, or launches follow-ups
- [ ] Result is exactly one canonical value from the shared result table

## Audit remediation coverage

- Cases 2–3 close SCP-001: heterogeneous items and presentation splits cannot drive
  magnitude or verdicts.
- Case 9 closes SCP-002: the skill presents neutral options and waits for the actual
  product owner.
- Cases 1 and 4–6 close SCP-003: inputs, default behavior, single-story mode, artifact
  identity, and result vocabulary share one contract with the skill and metadata.
- Cases 4–8 and 10–15 cover baseline routing, source evidence, justification, risk,
  bounded context, immutable re-checks, stable findings, and owner boundaries.
