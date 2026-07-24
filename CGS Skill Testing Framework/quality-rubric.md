# Skill Quality Rubric v2

Schema: `cgs-skill-quality-rubric/v2`<br>
Applies to: `$skill-test` static, behavioral, category, and compatibility evaluation

## Evidence model

Quality has separate axes. A result MUST NOT collapse them into one “works” claim.

| Axis ID | Axis | Valid evidence | Invalid shortcut |
|---|---|---|---|
| QR-STRUCT | Structural conformance | exact candidate/spec bytes validated against `cgs-skill-spec/v2` | presence of a spec file |
| QR-SEMANTIC | Semantic consistency | stable contradiction checks and exact clause references | keyword occurrence alone |
| QR-STATIC | Instruction-level behavior | stable static assertions against bounded bytes | claiming runtime success |
| QR-RUNTIME | Runtime behavior | current execution receipt, inputs, environment, outputs, logs, and hashes | prose, simulation, or stale run |
| QR-SIDEFX | Side effects | pre/post state manifests for files and external systems | “read-only” wording alone |
| QR-RECOVERY | Timeout/recovery | bounded timeout/interruption/rollback/idempotency executions | a recovery paragraph alone |
| QR-COMPAT | Contract compatibility | caller/callee/shared-schema matrix with exact versions and hashes | checking the callee in isolation |

Each assertion verdict is `PASS`, `FAIL`, `WARN`, `NOT_RUN`, or `NOT_APPLICABLE`. `PASS` requires the evidence type declared by its axis. `NOT_RUN` is not PASS. Any required assertion with missing, stale, ambiguous, oversized, or unreadable evidence is `FAIL` or the skill's declared fail-closed verdict.

## Universal gates

Every skill is evaluated by these stable IDs before category metrics:

| Metric | PASS criteria |
|---|---|
| QR-U01 — Spec schema | Dedicated spec declares `cgs-skill-spec/v2`, unique Spec ID, category, priority, date, summary modes/owned outputs/non-writes/verdicts, and all required sections. |
| QR-U02 — Case structure | Cases are numbered contiguously from 1, have unique stable Case IDs, and each contains Fixture, Input, Expected reads, Expected writes, Expected non-writes, Expected behavior, stable Assertions, and Case Verdict. |
| QR-U03 — Interface reality | Every advertised command/mode/flag has a real handling path or fail-closed usage behavior; no inert interface exists. |
| QR-U04 — Ownership | Producer, reviewer, recorder, and canonical owner boundaries are explicit; no role self-approves or crosses write ownership. |
| QR-U05 — Typed evidence | Exact schema versions, paths, raw hashes, identities, currentness, supersession, and coverage are required where evidence is consumed. |
| QR-U06 — Bounded operation | Reads, waits, recursion, retries, writes, and external actions have limits and declared consequences. |
| QR-U07 — Transaction safety | Mutating paths specify authorization, compare-and-swap/preimage checks, atomicity, rollback, idempotency, and persisted receipt as applicable. |
| QR-U08 — Verdict honesty | Static, runtime, side-effect, and recovery conclusions stay separate; aggregation cannot upgrade unknown or not-run evidence. |
| QR-U09 — Traceability | Every audit/requirement ID maps to a concrete SKILL clause and at least one dedicated-spec case assertion. |
| QR-U10 — Compatibility | Changed producers/consumers/shared schemas/metadata/specs are enumerated, and exact output/input versions agree. |

## Category metrics

Category metrics supplement, never replace, universal gates. A skill is evaluated only against its declared category and explicit capabilities.

### `gate`

| Metric | PASS criteria |
|---|---|
| QR-G01 — Read-only gate | Gate analysis cannot write canonical stage or source artifacts. |
| QR-G02 — Stage authority | Versioned stage authority, transition, gate profile, target commit/ref, dirty state, current evidence, and recorder receipt are exact and hash-bound. |
| QR-G03 — Mode scope | Only declared consumers implement review mode. For `gate-check`, all four phase gates run in full and lean; solo contributes `N/A`. |
| QR-G04 — No skipped safeguards | Mode never skips required QA, accessibility, security, evidence validation, separation, or non-waivable blockers. |
| QR-G05 — No auto-advance | Eligibility is distinct from separately authorized stage advancement by the unique recorder. |

### `review` and `analysis`

| Metric | PASS criteria |
|---|---|
| QR-A01 — Read-only reviewer | Review/analysis does not mutate reviewed sources or authoritative state. |
| QR-A02 — Bound findings | Findings have stable IDs, severity, exact source locations/hashes, and reproducible evidence. |
| QR-A03 — Independent persistence | When durable evidence is needed, a distinct recorder persists unchanged result bytes and a hash-bound receipt. |
| QR-A04 — Coverage honesty | Coverage, exclusions, unreadable inputs, and unsupported environments remain explicit. |
| QR-A05 — No remediation inference | Findings or suggested patches do not claim applied/verified status without a separate authorized execution. |

### `authoring`

| Metric | PASS criteria |
|---|---|
| QR-AU01 — Decision ownership | Open design decisions follow Question → Options → Decision → Draft → Approval. |
| QR-AU02 — Stable partial state | Skeleton/checkpoint strategy preserves stable IDs and source hashes when interruption recovery is supported. |
| QR-AU03 — Retrofit safety | Existing target bytes are classified and changed only through an authorized bounded transaction. |
| QR-AU04 — Review separation | Author cannot be the independent reviewer/approval recorder of the same candidate. |
| QR-AU05 — Canonical receipt | Authoring success is bound to exact output bytes and an owning recorder receipt when required. |

### `readiness`

| Metric | PASS criteria |
|---|---|
| QR-RD01 — Dimensions | Independent requirement, architecture, implementation, test/QA, and lifecycle dimensions are reported separately as applicable. |
| QR-RD02 — Fail-closed aggregation | A blocking/unknown required dimension cannot be averaged away or upgraded by advisory evidence. |
| QR-RD03 — Immutable inputs | Readiness/closure cannot rewrite requirement cores or planning hashes owned upstream. |
| QR-RD04 — Lifecycle ownership | Canonical status changes occur only through the unique tracker/state recorder with CAS, rollback, and receipt. |
| QR-RD05 — Next route | Any next-work suggestion is derived from exact current tracker/catalog evidence and has no implicit mutation. |

### `pipeline`

| Metric | PASS criteria |
|---|---|
| QR-P01 — Source provenance | Every output is bound to exact approved upstream artifacts, requirements, decisions, and hashes. |
| QR-P02 — Stable identities | Output IDs, membership, ordering, and cross-links are deterministic and collision-checked. |
| QR-P03 — Bounded changeset | The complete authorized changeset has exact destinations, preimages, schemas, and rollback behavior. |
| QR-P04 — Consumer compatibility | Every produced schema/version/path exactly matches registered consumers; changed shared schemas trigger impact analysis. |
| QR-P05 — No presence completion | Downstream readiness is proven by typed current receipts, not files, prose, count, or “latest”. |

### `team`

| Metric | PASS criteria |
|---|---|
| QR-T01 — Bounded delegation | Agent roles, inputs, outputs, ownership, and non-writes are explicit; delegation is permitted by the controlling contract. |
| QR-T02 — Dependency scheduling | Independent work may run in parallel; dependent work waits for exact prerequisite results. |
| QR-T03 — Failure collection | All launched work reaches a terminal result or bounded timeout; failures are surfaced without silent substitution. |
| QR-T04 — Integration owner | Exactly one integration/recorder owner applies authorized writes; reviewers remain read-only. |
| QR-T05 — Workflow-specific scope | The team does only its declared work; e.g. `team-audio` is spec-only and later implementation/QA are separate. |

### `sprint`

| Metric | PASS criteria |
|---|---|
| QR-SP01 — Canonical planning identity | Plan revision/hash, story-set membership/hash, tracker schema, and active sprint identity are explicit and current. |
| QR-SP02 — Planning ownership | Only the planning owner changes plan/story-set hashes; lifecycle updates are tracker-only. |
| QR-SP03 — Advisory mode | PR-SPRINT/PR-MILESTONE runs only in full for the declared consumer; lean/solo skip it without skipping mandatory evidence. |
| QR-SP04 — Measured claims | Velocity, completion, capacity, and forecast claims cite reproducible source rows and formulas. |
| QR-SP05 — Recorder transaction | Canonical sprint/tracker changes use one owner, CAS, rollback, idempotency, and a persisted receipt. |

### `utility`

| Metric | PASS criteria |
|---|---|
| QR-UT01 — Capability declaration | The skill declares its actual read/write/external behavior and is not granted implicit gate or mode behavior. |
| QR-UT02 — Domain contract | Utility-specific schemas, verdicts, side effects, timeout/recovery, and handoffs are tested with stable IDs. |
| QR-UT03 — Safe fallback | Missing optional capability never causes an untracked substitute, fabricated evidence, or unauthorized action. |

## Compatibility impact record

A change to an invocation, verdict, path, schema, owner, completion rule, timeout, side effect, or recovery behavior requires a compatibility record with:

1. changed producer clauses and exact candidate hashes;
2. every direct caller and callee;
3. every shared schema/catalog/guide reference;
4. required metadata and dedicated-spec updates;
5. old/new field and verdict mapping;
6. negative tests for stale/old/ambiguous evidence;
7. runtime execution status and remaining unverified effects.

Framework catalog `last_*` fields are execution history. Static repair or spec authoring MUST leave them empty; only the owning verified-run recorder may update them.

## Overall verdict

- `COMPLIANT`: all required structural, semantic, category, and compatibility assertions pass; runtime-dependent claims are either currently proven or explicitly scoped out without being claimed.
- `CONCERNS`: no contradiction or safety failure, but optional or non-authorizing evidence is incomplete.
- `NONCOMPLIANT`: any required structure is missing, an interface is inert, ownership conflicts, old/new contracts disagree, a mandatory safeguard is skippable, or an unexecuted/static claim is presented as runtime proof.
