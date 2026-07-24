# Behavioral Test Spec: tech-debt

## Skill Summary

`tech-debt` has four strictly read-only modes: `scan`, `add`, `prioritize`, and
`report`. It classifies heuristic/analyzer output as candidates, validates and
replays an append-only lifecycle register, computes advisory-only priority views,
and returns hash-bound proposals for a separate recorder. The skill never mutates
the register or invokes the recorder.

This specification is a repaired catalog candidate. It is **NOT EXECUTED** and
must not set catalog pass/tested fields until a real runner records immutable test
receipts against the exact candidate hashes.

## Contract Sources

- `.agents/skills/tech-debt/SKILL.md`
- `.agents/skills/tech-debt/references/debt-rules-v1.md`
- `.agents/skills/tech-debt/references/continued-workflow.md`
- `.agents/skills/tech-debt/agents/openai.yaml`

All paths above are relative to the formal candidate mirror root.

## Invocation and State Machine

| Mode | Required inputs | Read-only terminal states |
|---|---|---|
| `scan` | hashed scope manifest; hashed or exactly absent register | `SCAN_COMPLETE`, `NO_NEW_DEBT_FOUND`, `SCAN_PARTIAL`, errors |
| `add` | hashed/exactly absent register; optional hashed manual record | `INPUT_REQUIRED`, `ADD_PREVIEW_READY`, `ADD_DUPLICATE_FOUND`, errors |
| `prioritize` | hashed or exactly absent register | `PRIORITY_VIEW_READY`, `PRIORITY_VIEW_PARTIAL`, errors |
| `report` | hashed or exactly absent register; optional one baseline selector | `REPORT_READY`, `REPORT_PARTIAL`, errors |

Common parse/input terminal states are `USAGE_ERROR`, `INPUT_ERROR`, and
`REGISTER_ERROR`. The skill never emits `REGISTER_UPDATED`, `MUTATION_FAILED`,
`PASS`, `FAIL`, `COMPLETE`, or a severity/priority label as its state.

The independent recorder contract has separate states:
`RECORDER_COMMITTED`, `ALREADY_APPLIED`, `CAS_CONFLICT`, `UUID_COLLISION`,
`AUTHORIZATION_INVALID`, `PROPOSAL_INVALID`, and `RECORDER_FAILED`. These are not
skill outcomes.

## Deterministic Fixtures

Use isolated repositories with:

- canonical project UUID, fixed source snapshots, explicit dirty-state receipts,
  symlink fixtures, stable clocks, and deterministic hash calculations;
- valid/absent/legacy/malformed `cgs.tech-debt-register/v3` fixtures, including
  full event and payload hash chains;
- injectable UUIDv4 providers for proposal/recorder collision tests;
- `cgs.tech-debt-scan-scope/v1` manifests containing first-party source,
  generated output, vendor code, build/cache paths, tests, ambiguous paths, and
  exact hashes;
- fake versioned text, AST-complexity, and token-clone analyzers that record exact
  argv/subset/config/rulepack/side effects and can complete, timeout, fail, mutate,
  or return malformed output;
- failure-injectable independent recorder implementing lock, CAS, prepared-file,
  atomic replace/create, flush, post-read verification, and immutable receipts;
- immutable VCS rename receipts and sprint-history receipts; and
- before/after filesystem snapshot instrumentation.

Never invoke another project skill. Tests that exercise the independent recorder
call the recorder fixture directly, never through `$tech-debt`.

## Global Assertions

Every test asserts:

1. `$tech-debt` writes zero bytes and reports `register_mutated: false`,
   `proposal_persisted: false`, `decision_authority_exercised: false`, and
   `recorder_invoked: false`.
2. A candidate is not accepted debt and analyzer output never chooses lifecycle,
   product priority, or scheduling.
3. A fingerprint/alias has at most one owning debt UUID; existing event bytes and
   order never change.
4. Every claim is bound to exact target, register, rulepack/config/analyzer, and
   evidence hashes, or explicitly `UNVERIFIED`/`UNKNOWN`.
5. Outcome vocabulary matches the state machine and partial/error outcomes list
   every missing/invalid input.

## Test Cases

### TD-001 — Exact scan grammar succeeds

**Given** a valid hashed v1 scope manifest and matching v3 register identity.

**When** invoked as the documented `scan --scope ... --register ...` grammar with
the two options in either allowed order.

**Then** parsing succeeds, the normalized invocation is identical in meaning, and
no undeclared positional/default scope is used.

### TD-002 — Invalid invocation is an execution error

**Given** separate invocations with no mode, unknown mode, positional scope,
unknown/repeated option, missing value, malformed UUID/hash/path, both report
baseline options, or a mode-incompatible option.

**When** parsing occurs.

**Then** each returns `USAGE_ERROR`, performs no scan/register replay/proposal/
write, and never emits `FAIL` or a quality verdict.

### TD-003 — Input and register identity errors are distinct

**Given** (a) a scope/manual/baseline byte-hash mismatch and (b) a register byte-
hash mismatch.

**When** the corresponding mode freezes input identity.

**Then** (a) returns `INPUT_ERROR`, (b) returns `REGISTER_ERROR`, neither continues
with stale bytes, and neither writes.

### TD-004 — Missing register behavior is mode-complete

**Given** a valid `ABSENT:<canonical-path>` identity whose path is confirmed
absent.

**When** each mode is exercised.

**Then** scan uses an empty dedup index and exposes `REGISTER_ABSENT`; add may
return an exact `CREATE_REGISTER` proposal; prioritize returns a partial empty
view; report returns partial/`UNKNOWN` metrics; no mode creates the file.

### TD-005 — Malformed and legacy registers fail closed

**Given** separate malformed/hash-broken v3 and valid recognized v2 registers.

**When** any mode loads them.

**Then** the malformed fixture returns `REGISTER_ERROR`; v2 returns
`REGISTER_ERROR` subtype `MIGRATION_REQUIRED` plus a byte-hash-bound migration
proposal; neither is repaired, reinterpreted, or written.

### TD-006 — TODO/FIXME is only a heuristic candidate

**Given** first-party source with TODO, FIXME, and HACK markers and a complete
versioned text-scanner receipt.

**When** scan runs.

**Then** each normalized hit is `HEURISTIC_CANDIDATE`, states why it may be debt
and intentional, requires owner triage, and creates no debt/status/priority claim
or register event.

### TD-007 — Long file is not automatically debt

**Given** a first-party file above a declared size threshold with no structural
evidence of a maintainability defect.

**When** scan runs.

**Then** the result is only a size-rule `HEURISTIC_CANDIDATE`; observed size and
threshold remain evidence but are excluded from stable fingerprint identity.

### TD-008 — Exclusions require positive classification

**Given** generated, vendored, build, cache, third-party, and test-fixture paths,
some with owner-approved classification evidence and some named similarly without
evidence.

**When** scan builds coverage.

**Then** proven paths are visibly `EXCLUDED_PROVEN`; test fixtures are excluded
from generic size/clone rules; name-only cases are `UNVERIFIED`; no path is
silently omitted.

### TD-009 — Complexity requires a versioned capable analyzer

**Given** complexity requested for a supported language but no compatible AST/
control-flow adapter.

**When** scan runs.

**Then** it emits an `UNSUPPORTED` analyzer receipt, no complexity result or clean
claim, affected candidates/checks are `UNVERIFIED`, and outcome is `SCAN_PARTIAL`.

### TD-010 — Duplication cannot fall back to text similarity

**Given** clone detection requested while only keyword/text matching is available.

**When** scan runs.

**Then** duplication is `UNSUPPORTED`/`UNVERIFIED`, no clone candidate is
fabricated, text similarity is not treated as token/AST evidence, and the outcome
is `SCAN_PARTIAL`.

### TD-011 — Complete analyzer receipt is reproducible

**Given** a compatible fake AST analyzer with exact executable/adapter/rulepack/
config/subset identities and deterministic output.

**When** it completes within limits and mutation snapshot remains unchanged.

**Then** the v1 receipt contains all required command, capability, count, timing,
hash, and side-effect fields; supported results may be `EVIDENCE_SUPPORTED` but
remain candidates.

### TD-012 — Failed, stale, side-effecting, and over-limit analyzers stay unknown

**Given** separate timeout, nonzero exit, malformed output, target-change,
mutation-observed, unreadable-file, and hard-cap fixtures.

**When** scan runs.

**Then** affected receipts are not `COMPLETE`, successful independent evidence is
preserved, every gap is enumerated, and outcome is `SCAN_PARTIAL` (or
`INPUT_ERROR` if no stable meaningful evidence remains).

### TD-013 — Stable fingerprint ignores volatile movement

**Given** identical rule ID, canonical path, stable symbol, defect class, and
semantic evidence key at different line/column/byte offsets, source hashes,
timestamps, diagnostic wording, and analyzer versions.

**When** `td-fp-v2` is computed.

**Then** all variants produce the same lowercase SHA-256 and candidate ID.

### TD-014 — Semantic identity changes split fingerprints

**Given** pairs differing in stable rule ID, canonical path, qualified symbol,
defect class, or semantic evidence key.

**When** `td-fp-v2` length-delimited normalization runs.

**Then** each meaningful difference produces a different fingerprint, while NFC,
slash, and allowed whitespace equivalents do not.

### TD-015 — Rename alias requires evidence or user selection

**Given** a registered finding moved to a new path/symbol.

**When** scan sees the new raw fingerprint.

**Then** immutable VCS move evidence or an exact user-selected alias may produce a
`FINGERPRINT_ALIAS` proposal for the existing UUID; without it, the result remains
a new candidate and the old item is not auto-resolved.

### TD-016 — Identical rescan is idempotent

**Given** registered fingerprint F whose latest source/evidence identity is R/E.

**When** the identical scope is scanned again at R/E.

**Then** F maps to its existing debt UUID, no `CREATED`/`OBSERVED` event is
proposed, the register is unchanged, and complete analysis returns
`NO_NEW_DEBT_FOUND`.

### TD-017 — New source observation preserves debt identity

**Given** registered F last observed at R1/E1 and materially new evidence R2/E2
with the same stable fingerprint.

**When** the owner selects it after scan.

**Then** the proposal contains at most one `OBSERVED` for the existing debt UUID,
never another `CREATED`, and remains not persisted.

### TD-018 — Reappeared resolution does not auto-reopen

**Given** F materializes as `RESOLVED` and is observed again.

**When** scan runs.

**Then** it is `REAPPEARED` under the stable UUID, stays `RESOLVED`, and only a
separately selected/authorized `REOPENED` proposal could request an external
transition.

### TD-019 — Duplicate ownership makes the register invalid

**Given** two debt UUIDs own the same primary fingerprint/alias, or one UUID/event
ID has conflicting records.

**When** any mode replays the register.

**Then** outcome is `REGISTER_ERROR`, conflicts are identified, and no partial
view/proposal/write is emitted.

### TD-020 — Add without payload requests exact input

**Given** a valid add invocation without `--candidate`.

**When** add runs.

**Then** it returns `INPUT_REQUIRED` with the exact v1 manual-candidate fields and
does not synthesize description, paths, evidence, category, owner, or estimates.

### TD-021 — Manual add is candidate-only and deduplicated

**Given** valid manual fixtures that (a) produce a new `manual@2` fingerprint and
(b) match an existing fingerprint.

**When** add runs after owner selection.

**Then** (a) returns `ADD_PREVIEW_READY` with one unpersisted `CREATED` proposal;
(b) returns `ADD_DUPLICATE_FOUND` with the existing debt UUID and no duplicate;
`UNKNOWN`/`UNASSIGNED` values remain explicit.

### TD-022 — Manual input cannot self-accept or self-resolve

**Given** a manual record that declares initial `ACCEPTED`, `RESOLVED`,
`SUPERSEDED`, product priority, or sprint schedule without the separate required
authority evidence.

**When** add validates it.

**Then** outcome is `INPUT_ERROR`, no lifecycle/decision event is proposed, and
ordinary owner triage is not treated as acceptance authority.

### TD-023 — Register v3 replays required lifecycle fields

**Given** valid event chains exercising `CREATED`, `TRIAGED_OPEN`, `ACCEPTED`,
`REOPENED`, `RESOLVED`, and `SUPERSEDED` with required owners, reasons,
timestamps, hashes, authority, controls, evidence, and successors.

**When** prioritize/report replay them.

**Then** materialized statuses are exactly `OPEN`, `ACCEPTED`, `RESOLVED`, or
`SUPERSEDED`, fields retain provenance, and historical event bytes/order remain
unchanged.

### TD-024 — Invalid lifecycle or missing rationale fails closed

**Given** separate fixtures with `CREATED -> REOPENED`, a transition after
terminal `SUPERSEDED`, acceptance without reason/review trigger, resolution
without evidence/authority, broken predecessor, or bad payload/event hash.

**When** any mode replays the register.

**Then** each returns `REGISTER_ERROR`; no status is guessed and no repair,
proposal, or write occurs.

### TD-025 — Fixed priority score and deterministic ties

**Given** A=(impact 4, frequency 2, effort 2), B=(3,4,3), and C=(2,2,1), all with
valid evidence and equal exact score 4.

**When** prioritize runs.

**Then** order is A, B, C by impact and remaining documented tie-breaks; exact
rationals are retained, three decimals displayed, every source event/evidence and
tie-break is shown, and the register hash is unchanged.

### TD-026 — Missing score inputs remain unscored

**Given** one item lacks frequency, one has only an uncalibrated T-shirt effort,
and one value is out of range.

**When** prioritize runs.

**Then** all are `UNSCORED`, no conversion/inference occurs, they are listed
lexically outside scored rows, outcome is `PRIORITY_VIEW_PARTIAL`, and the view is
`ADVISORY_ONLY`.

### TD-027 — Priority view never reorders or records decisions

**Given** chronological register order different from advisory score order and a
user preference different from both.

**When** prioritize displays the view.

**Then** register bytes/hash/order are identical, no priority/schedule event is
appended, and an external decision can appear only in a new exact proposal after
separate user/producer selection.

### TD-028 — Report baseline is an exact ancestor

**Given** a valid event UUID and a valid ancestor register hash in separate runs.

**When** report runs.

**Then** it computes exact created/observed/accepted/reopened/resolved/superseded
transitions over the interval and records the cursor/hash in a read-only report.

### TD-029 — Missing or incomparable report evidence stays unknown

**Given** no baseline, a sibling/unrelated baseline, and missing sprint history in
separate fixtures.

**When** report runs.

**Then** no baseline yields point-in-time counts with change/trend `UNKNOWN` and a
partial outcome when requested; sibling/unrelated input returns `INPUT_ERROR`;
three-sprint aging is `UNKNOWN` without stable transition evidence.

### TD-030 — Analyzer and recorder are operationally separate

**Given** a selected candidate and valid change proposal.

**When** `$tech-debt` completes in any mode.

**Then** it does not call the recorder fixture, acquire its write lock, create a
prepared file, or mutate the register; proposal markers are `NOT_PERSISTED` and
`NOT_AUTHORIZATION` and a future write requires fresh exact authorization.

### TD-031 — CAS conflict requires new proposal and consent

**Given** an independently authorized proposal for base tuple H1/R1/E1 and another
writer advances the register to H2/R2/E2.

**When** the recorder fixture receives the stale proposal.

**Then** it returns `CAS_CONFLICT`, writes nothing, performs no last-writer-wins or
hidden retry, and any retry path is replay → new proposal/hash → new authorization
→ new transaction.

### TD-032 — UUID collision invalidates authorization

**Given** a reserved event/debt UUID absent at proposal time but present at recorder
CAS validation.

**When** the recorder fixture validates uniqueness.

**Then** it returns `UUID_COLLISION`, does not regenerate under old authorization,
writes nothing, and regeneration requires a new proposal and authorization.

### TD-033 — Exact replay is idempotent, not duplicate append

**Given** a recorder retry whose exact proposed event IDs/hashes and final content
are already committed.

**When** the recorder fixture validates current state.

**Then** it returns `ALREADY_APPLIED` without a write. A merely equivalent event
with different IDs/hashes is a CAS/proposal conflict, not silently adopted.

### TD-034 — Atomic failure preserves base or absence

**Given** separately injected prepare, flush, atomic replace/create, and post-read
verification failures.

**When** the recorder fixture executes.

**Then** result is `RECORDER_FAILED`, the original register remains byte-identical
or exact absence remains, no partial event is visible, and the receipt identifies
the failed atomicity stage without claiming commit.

### TD-035 — Concurrent source/register change is disclosed

**Given** an analyzed file or register changes between before/after snapshots.

**When** the skill finalizes.

**Then** changed source evidence forces the applicable partial/error state;
changed register identity returns `REGISTER_ERROR` subtype `STALE_REGISTER`; the
skill does not revert, overwrite, or attribute the concurrent edit.

### TD-036 — Output and metadata stay synchronized

**Given** the candidate SKILL, references, metadata, and this specification.

**When** static conformance runs.

**Then** all four modes, exact outcome vocabularies, candidate-only heuristic
boundary, versioned analyzer receipts, v3 lifecycle states, read-only analyzer/
recorder separation, stable fingerprinting, CAS/UUID/atomicity rules, and
NOT-EXECUTED status agree without contradictory mutation claims.

## Static Conformance Checks

The candidate passes static conformance only if:

- frontmatter contains exactly `name` and `description` and metadata YAML parses;
- all Markdown links resolve inside the formal candidate mirror;
- public mode grammar and outcome tokens match in SKILL, workflow, metadata, and
  this spec;
- every public mode has an empty write set and no `REGISTER_UPDATED` outcome;
- marker/size rules cannot become debt and AST/clone checks require compatible
  versioned analyzer receipts;
- generated/vendor/test exclusions require positive evidence and remain visible;
- v3 schema contains status, owners, acceptance/resolution/supersession reasons,
  timestamps, evidence, payload/event hashes, UUIDs, and both chain dimensions;
- `td-fp-v2` is deterministic, length-delimited, and excludes volatile fields;
- replay detects duplicate ownership, invalid lifecycle, UUID collisions, and
  chain/hash corruption;
- priority formula, allowed values, exact ordering, unscored behavior, and all six
  tie-breaks are fixed and read-only;
- report baseline/sprint-aging behavior is evidence-bound;
- proposal schema binds exact base/final bytes and says not persisted/authorized;
- independent recorder contract requires authorization, exclusive CAS, UUID
  checks, atomic replacement/create, post-verification, and a fresh proposal plus
  fresh authorization after conflict; and
- no catalog test/pass field is changed by this unexecuted specification.

## Audit Traceability

| Audit item | Closing contract | Primary tests |
|---|---|---|
| TDB-004 | heuristic/owner-triage boundary; proven exclusions | TD-006–TD-008 |
| TDB-005 | versioned adapter/rulepack receipts; AST/clone capabilities; unsupported states | TD-009–TD-012 |
| TDB-006 | v3 event schema and explicit lifecycle/authority/reason/evidence | TD-023–TD-024 |
| TDB-007 | exact absent/legacy/malformed behavior; proposal-only creation/migration | TD-004–TD-005 |
| TDB-008 | strict grammar, schemas, and execution errors distinct from quality | TD-001–TD-003 |
| TDB-009 | zero-write four modes; independent recorder only | TD-030, TD-035–TD-036 |
| TDB-010 | repaired four-mode state-machine spec and synchronized vocabulary; test status remains NOT EXECUTED | TD-001–TD-036 |
| TDB-011 | stable UUID/fingerprint, CAS base tuple, no stale retry, atomic failure behavior | TD-013–TD-019, TD-031–TD-034 |

P0 protections remain covered: scan idempotence/dedup (TD-013–TD-019), fixed
evidence-based advisory scoring (TD-025–TD-027), and append-only history
(TD-023–TD-024, TD-027–TD-034).
