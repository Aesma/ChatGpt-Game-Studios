# Skill Spec: `$[skill-name]`

> **Spec ID**: `skill-spec.[skill-name]/v2`<br>
> **Spec Schema**: `cgs-skill-spec/v2`<br>
> **Category**: `[gate | review | authoring | readiness | pipeline | analysis | team | sprint | utility]`<br>
> **Priority**: `[critical | high | medium | low]`<br>
> **Spec written**: `[YYYY-MM-DD]`

## Skill Summary

- **Purpose**: [one bounded paragraph]
- **Invocation modes**: [exact supported modes and CLI forms; write `none` when absent]
- **Owned outputs**: [exact paths/schemas this skill may create or mutate]
- **Non-writes**: [canonical artifacts, state, external systems, and directories it must not mutate]
- **Verdict vocabulary**: [exact terminal and intermediate verdicts]
- **Authority boundary**: [producer/reviewer/recorder separation and any separately authorized action]

## Static Assertions

Every assertion has a stable ID and is evaluated against exact candidate bytes.

- [ ] **STATIC-001 — Frontmatter**: YAML frontmatter contains only required `name` and non-empty `description`; name matches the directory.
- [ ] **STATIC-002 — Interface**: Every advertised invocation, mode, flag, input, and required argument has executable handling or a fail-closed usage path.
- [ ] **STATIC-003 — Ownership**: Owned writes and required non-writes are explicit and non-overlapping with upstream/downstream owners.
- [ ] **STATIC-004 — Schemas**: Every consumed and produced schema exists at its exact version; path/version/currentness fields are stated.
- [ ] **STATIC-005 — Verdicts**: Verdicts, aggregation, blocking consequences, and exit behavior are unambiguous.
- [ ] **STATIC-006 — Side effects**: Static/read-only phases, runtime mutations, external actions, and authorization boundaries are separately enumerated.
- [ ] **STATIC-007 — Timeout and recovery**: Bounded waits, timeout result, resume/checkpoint behavior, rollback, and idempotency are explicit where applicable.
- [ ] **STATIC-008 — Handoff**: Caller/callee/shared-schema compatibility and the recommended next step are explicit.
- [ ] **STATIC-009 — Traceability**: Every governing audit/requirement ID maps to a concrete clause and at least one case assertion.

## Semantic Contradiction Checks

- [ ] **SEM-001 — Interface consistency**: Summary, phases, examples, metadata, and test cases advertise the same interface.
- [ ] **SEM-002 — Authority consistency**: No read-only/reviewer/advisory role is also assigned canonical mutation or approval authority.
- [ ] **SEM-003 — Evidence consistency**: Presence, prose, filename, count, or “latest” selection is never treated as current typed evidence.
- [ ] **SEM-004 — Mode consistency**: Optional modes are implemented end to end; no shared document creates an implicit mode.
- [ ] **SEM-005 — Transaction consistency**: Preview, authorization, compare-and-swap, commit, rollback, and receipt claims agree.
- [ ] **SEM-006 — Dependency consistency**: Caller outputs exactly match callee inputs, including schema version, identity, versions, and verdicts.
- [ ] **SEM-007 — Static/runtime distinction**: Instruction text alone is not reported as proof that a runtime side effect, timeout, or recovery behavior occurred.

## Test Cases

Case numbers MUST be contiguous from 1. Case IDs MUST be stable and unique. Duplicate or missing required fields invalidate the spec.

### Case 1: Happy Path — [brief name]

**Case ID**: `CASE-[SKILL]-001`

**Fixture**:
- [exact repository/external state, paths, schemas, versions, identities]

**Input**:
- [exact invocation and manifest/request bytes]

**Expected reads**:
- [ordered, bounded reads and accepted schemas]

**Expected writes**:
- [exact path/schema/transaction, or `none`]

**Expected non-writes**:
- [explicit protected paths/state/external actions]

**Expected behavior**:
1. [deterministic step]
2. [deterministic step]

**Assertions**:
- [ ] **CASE-[SKILL]-001-A01**: [observable static or runtime assertion]
- [ ] **CASE-[SKILL]-001-A02**: [observable identity/currentness/authority assertion]

**Case Verdict**: `PASS | FAIL | BLOCKED | NOT_RUN`

### Case 2: Invalid or blocked input — [brief name]

**Case ID**: `CASE-[SKILL]-002`

**Fixture**:
- [missing, stale, malformed, oversized, unauthorized, or contradictory state]

**Input**:
- [exact invocation]

**Expected reads**:
- [bounded validation reads]

**Expected writes**:
- none

**Expected non-writes**:
- [all canonical and external state]

**Expected behavior**:
1. Detect the exact failure.
2. Return the declared fail-closed verdict without downstream execution.

**Assertions**:
- [ ] **CASE-[SKILL]-002-A01**: [correct failure/verdict]
- [ ] **CASE-[SKILL]-002-A02**: [zero unauthorized writes or actions]

**Case Verdict**: `PASS | FAIL | BLOCKED | NOT_RUN`

### Case 3: Boundary, timeout, or recovery — [brief name]

**Case ID**: `CASE-[SKILL]-003`

**Fixture**:
- [limit boundary, interruption, partial transaction, or mode-specific state]

**Input**:
- [exact invocation]

**Expected reads**:
- [bounded inputs/checkpoint/preimage]

**Expected writes**:
- [checkpoint/receipt/rollback output, or `none`]

**Expected non-writes**:
- [protected state]

**Expected behavior**:
1. [timeout, recovery, rollback, or deterministic boundary handling]

**Assertions**:
- [ ] **CASE-[SKILL]-003-A01**: [observable behavior]
- [ ] **CASE-[SKILL]-003-A02**: [idempotency/rollback/no partial success]

**Case Verdict**: `PASS | FAIL | BLOCKED | NOT_RUN`

## Protocol Compliance

- [ ] **PROTO-001 — Bounded authorization**: An explicit bounded request authorizes only the stated in-scope changes.
- [ ] **PROTO-002 — Single changeset decision**: Without prior authorization, the complete changeset is previewed once; no per-file re-prompt occurs.
- [ ] **PROTO-003 — Scope expansion**: Material expansion, destructive action, publication, or external mutation requires separate authority.
- [ ] **PROTO-004 — Evidence honesty**: Static conformance, simulated behavior, and current runtime execution are reported on separate axes.
- [ ] **PROTO-005 — Read limits**: Recursive discovery and referenced-artifact reads are bounded and fail closed.
- [ ] **PROTO-006 — Recovery**: Interrupted or failed mutation cannot leave an unreported partial authoritative state.
- [ ] **PROTO-007 — Compatibility**: Caller, callee, shared schema, metadata, and dedicated spec impact are analyzed together.
- [ ] **PROTO-008 — Handoff**: The terminal response exposes exact verdict, evidence gaps, outputs, versions, and one bounded next action.

## Coverage Notes

- **Static coverage**: [what exact text/schema assertions were evaluated]
- **Runtime coverage**: [what was truly executed; write `not executed` when absent]
- **Side-effect coverage**: [write/external-state probes and pre/post state]
- **Timeout/recovery coverage**: [tested scenarios or explicit gap]
- **Caller/callee/shared-schema coverage**: [exact affected contracts]
- **Known gaps**: [unsupported environments, untested branches, missing receipts]
- **Audit trace**: [audit/requirement ID → SKILL clause → case assertion IDs]
