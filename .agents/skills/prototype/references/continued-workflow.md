# Prototype continuation: evidence, routing, pivot lineage, and recoverable decisions

This file is mandatory after an authorized prototype run reaches the continuation boundary. Re-read it completely. Execution authority does not authorize report/index/decision/pivot/graveyard publication, cleanup not already approved, a new prototype, or any downstream design/production workflow.

## 7. Validate the immutable run packet

Read and hash only the current exact:

- `PROTOTYPE-MANIFEST.yaml` and its execution-authorization hash;
- the exact skill-source and this continuation-contract path/SHA-256 values previewed for the run;
- full `CHECKPOINT.yaml` hash chain;
- final `RUN-RECEIPT.yaml` using `cgs.prototype-run-receipt/v1`;
- source, dependency manifest/lock, toolchain, build-config, generated-output, and dirty-worktree manifests;
- build/play/skip/consent/redaction receipts and raw evidence referenced by the run receipt;
- hypothesis, thresholds, budgets, optional parent pivot, and cleanup state.

Validate that every referenced path/hash/build/source/run ID agrees, including this continuation contract. Exclude withdrawn or unredacted consent-restricted evidence. Reject a receipt that cites missing, stale, differently hashed, unsupported, or unauthorized evidence. Contract drift is `BLOCKED`; do not combine execution rules from one version with publication rules from another.

If the receipt packet is invalid, return `PARTIAL` or `BLOCKED`; recommendation is `INCONCLUSIVE`, no user decision is solicited from the invalid recommendation, and no final project-state publication occurs.

All debrief, recommendation, decision, index, pivot, and graveyard facts must link the exact run-receipt path/SHA-256. A draft or model narrative is not a source of fact.

## 8. Evidence analysis and advisory recommendation

Update only the already execution-authorized in-root `REPORT-DRAFT.md` and `PUBLICATION-PROPOSAL.yaml`. Mark them:

> NON-AUTHORITATIVE DRAFT — NOT A PRODUCT DECISION

Use these exact sections:

```markdown
## Experiment and receipt identity
[prototype/run/hypothesis/parent-pivot/run-receipt/source/lock/toolchain/build hashes]

## Observed facts
[direct current-run observations only]

## Participant reports
[consent-safe attributed/pseudonymous reports]

## Build results
[build receipts, commands, versions, artifacts/log hashes]

## Play results
[play receipts, consent/redaction, protocol and measurements]

## Typed skips and unsupported scope
[skip IDs/taxonomy/effects; never passes]

## Not run / not observed / withdrawn
[explicit evidence gaps]

## Model inferences
[interpretation separated from facts/reports]

## Recommendation
RECOMMENDATION: PROCEED | PIVOT | KILL | INCONCLUSIVE
Confidence basis: <evidence quality, not a generic probability>
Evidence supporting: [...]
Evidence against/limits: [...]
```

Do not include an unsupported numeric success probability. A probability may appear only with the exact applicable dataset path/hash, sample/outcome definition/count, period, uncertainty, and applicability limits.

Recommendation rules:

- `PROCEED` only when current usable receipts satisfy the predeclared threshold for the exact hypothesis. It means continue discovery/design consideration, not product approval.
- `PIVOT` only when current evidence identifies a specific testable change and a new falsifiable threshold while preserving known evidence.
- `KILL` is advisory only when usable evidence strongly contradicts the hypothesis. Iteration or pivot count never forces it.
- `INCONCLUSIVE` when an essential build/play/consent/dependency step is skipped, evidence is stale/withdrawn, the mode cannot measure the signal, a receipt is invalid, or budget ended without trustworthy evidence.

A build PASS without current consent-safe real play cannot support fun/player-feel PROCEED. `USER_ACCEPTED_RISK` never upgrades missing evidence. `MODEL_SIMULATION` cannot support human behavior claims.

An optional reviewer may produce `ADVISORY_REVIEW`; it cannot rewrite receipts/drafts, select a direction, publish state, or override the user.

## 9. Present user-owned routing choices

Show the evidence matrix, typed skips, unsupported scope, privacy limitations, recommendation, and consequences. Ask the user to select one:

- `PROCEED` — consider the evidence in the correct separately authorized concept/design step;
- `PIVOT` — define a new linked hypothesis for a new separately authorized prototype;
- `KILL` — stop/shelve this exploration non-destructively, with a recoverable record;
- `DEFER` — retain evidence with no direction;
- `MORE_EVIDENCE` — plan a separate bounded run; never extend this run automatically.

Do not write `USER_DECISION` until the user gives an explicit selection for the exact prototype/run/receipt. Silence, elapsed time, risk acceptance, recommendation text, reviewer opinion, third pivot, or task completion is not a decision.

Record the exact response, displayed options, prototype/run/receipt identity, timestamp, and canonical decision-record SHA-256. A user selection still writes no file and invokes nothing.

## 10. Correct design routing — PROTO-P1-006

Never route PROCEED directly to `design-review design/gdd/game-concept.md`. `design-review` reviews a qualifying system GDD; it is not the concept-freeze or concept-authoring gate.

Determine at most one advisory next route from explicit current artifacts/receipts, without recreating stage heuristics:

| Verified current state | Advisory owner/route | Required boundary |
|---|---|---|
| concept absent, draft, disputed, or not explicitly approved/frozen | concept owner / `brainstorm`-class concept authoring or revision | user decides concept content; prototype evidence is supporting input only |
| concept explicitly approved/frozen but systems index not reviewed | systems-mapping owner / `map-systems`-class decomposition | exact approved concept and separate authorization |
| reviewed systems index names a system without a complete GDD | system-design owner / `design-system`-class authoring | exact system scope and separate authorization |
| complete system GDD exists and is the explicit review target | design-review owner / `design-review <exact-system-gdd>` | current GDD hash and separate review task |
| technical feasibility only, no product/design decision | relevant technical owner | a bounded technical handoff, not concept/GDD approval |

If current-state evidence is missing/ambiguous, recommend resolving that evidence rather than guessing a stage. Never invoke the route automatically. PROCEED does not freeze a concept, approve a GDD, choose architecture, create epics/stories/sprints, or authorize production code/assets.

## 11. Pivot lineage — PROTO-P1-007

An explicit PIVOT selection does not authorize another run. Render one `cgs.prototype-pivot/v1` record in the publication proposal with:

- `pivot_id`, parent prototype/run/hypothesis IDs, exact run-receipt path/hash, and parent source/build/play identities;
- the exact prior threshold result and failure/inconclusive evidence IDs;
- facts that remain valid and exact evidence hashes;
- assumptions invalidated or still Unknown;
- one named changed variable/assumption, or an explicit minimal set with interaction rationale;
- new falsifiable hypothesis, success/failure/inconclusive criteria, and mode capability;
- changed scope and exclusions;
- required dependency/toolchain/privacy changes;
- proposed new hard budget and isolation mode;
- duplication check explaining how the new experiment differs from prior attempts;
- `authorization_state: NOT_AUTHORIZED` and `next_run_id: NOT_CREATED`.

The immutable pivot record is published only in the all-or-none group. A future `$prototype --pivot` must validate its exact path/hash, parent receipt, and lineage before planning. It must create new IDs/root/budget/changeset and carry forward evidence by hash, never by copied narrative. Invalid/missing lineage returns `ERROR` or asks for correction; do not repeat an unbound experiment.

## 12. Explicit recoverable KILL — PROTO-P1-009

`RECOMMENDATION: KILL` is not a decision. If the user initially chooses KILL, present a confirmation bound to the exact prototype/run/receipt that states:

- this stops/shelves the exploration only;
- no source, prototype, evidence, report, branch, or worktree is deleted by the KILL decision;
- what evidence and useful findings will be retained;
- the exact graveyard/index status proposed;
- how a later `REOPENED` event restores active exploration without erasing history;
- publication requires separate exact authorization.

Only an unambiguous affirmative response to that confirmation creates `USER_DECISION: KILL`. Record the prompt/response hash and set decision state `USER_KILLED_RECOVERABLE`. Ambiguous/no response leaves `PENDING`; write no graveyard event.

The proposed graveyard event conforms to `cgs.prototype-graveyard-event/v1` and includes event ID, state `USER_KILLED_RECOVERABLE`, prototype/run/hypothesis/run-receipt/source/build/play hashes, explicit confirmation record/hash, reason, what worked, reusable evidence, retained paths, privacy/retention limits, reopen prerequisites, and `destructive_cleanup_authorized: false`.

Reopening requires a future explicit user confirmation for the exact event/hash and a separately authorized publication transaction. It appends a `REOPENED` event linked to the KILL event; it never deletes or rewrites history and never automatically launches a prototype.

## 13. Separately authorize atomic publication

Publication is optional. After a valid explicit user decision, render the complete group in memory:

- final immutable `REPORT.md` under the throwaway root;
- `DECISION.md` under the throwaway root;
- one exact create/update in `prototypes/index.md`;
- for PIVOT, one immutable `PIVOT-NOTE.md` containing `cgs.prototype-pivot/v1`;
- for confirmed KILL, one exact append/event in `prototypes/GRAVEYARD.md`;
- exact transaction/staging paths required for all-or-none commit.

Every member contains the same transaction ID, prototype/run/hypothesis IDs, exact run-receipt/source/lock/toolchain/build/play hashes, typed skips, privacy-safe evidence state, recommendation, explicit user decision/record hash, decision scope `EXPERIMENT ROUTING ONLY — NOT PRODUCT APPROVAL`, and pivot/reopen semantics when applicable.

Preview every path, operation, owner, base hash/ABSENT, complete content, transaction mechanics, rollback/recovery behavior, and explicit non-writes. Ask for publication authorization. Execution authorization, consent, content approval, recommendation, and user decision are insufficient filesystem authority.

Before commit:

1. revalidate every target base hash/absence and exact original-worktree dirty manifest;
2. revalidate run receipt and all source/lock/toolchain/build/play/skip/consent hashes;
3. stage complete candidates only in authorized transaction paths;
4. validate transaction ID, decision, lineage, privacy, and cross-file hashes;
5. prove the group can apply atomically or roll back without exposing a half-authoritative state.

If any condition fails, modify no final report/index/decision/pivot/graveyard target; retain the non-authoritative in-root draft/proposal only if already authorized; return `PARTIAL — PUBLICATION_NOT_COMMITTED` with recovery conflicts. Never write REPORT first and index later. Reviewers cannot alter the user decision.

After commit, read back all members and verify transaction/hashes. Otherwise return `BLOCKED — PUBLICATION_INCONSISTENT` and do not represent the group as authoritative.

## 14. Cleanup and final outcome

Cleanup follows only the exact execution-approved policy. KILL does not authorize it. Before approved cleanup, verify target is the new run-specific isolation root/worktree, evidence required by the run/publication receipts is retained at authorized locations, original worktree is unchanged outside expected Git metadata, and no pre-existing/user data is inside the target.

If cleanup cannot be proven safe, do not delete; return `cleanup_state: CLEANUP_REQUIRED` with exact paths. If it succeeds, emit `cgs.prototype-cleanup-receipt/v1` with target, pre-delete manifest hash, authorization hash, operation/result, preserved evidence hashes, and original-worktree postcheck. Briefly report what was removed and recoverability.

Report independently:

```yaml
run_status: COMPLETE | PARTIAL | BLOCKED | CANCELED
build_status: PASS | FAIL | TIMED_OUT | NOT_RUN
play_status: OBSERVED | NOT_RUN | STALE | WITHDRAWN
recommendation: PROCEED | PIVOT | KILL | INCONCLUSIVE
user_decision: PROCEED | PIVOT | KILL | DEFER | MORE_EVIDENCE | PENDING
decision_record_sha256: ... | NOT_CREATED
run_receipt_sha256: ...
publication: COMMITTED | NOT_REQUESTED | NOT_AUTHORIZED | CONFLICTED
cleanup_state: RETAINED | CLEANED | CLEANUP_REQUIRED
product_approval: NOT_GRANTED
auto_executed_downstream: false
```

`run_status: COMPLETE` means only that the bounded experiment/evidence protocol finished. Return at most one legal next action and never execute it.
