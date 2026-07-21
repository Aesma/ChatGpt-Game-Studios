# Skill Test Spec: $brainstorm

## Purpose

Verify that `$brainstorm` collaborates on one game concept without routing it through
a system-GDD reviewer, overwriting unselected existing content, looping indefinitely,
or contradicting its sequential full-mode gate DAG.

## Fixtures

Fixtures provide exact bytes and SHA-256 values for the concept, applicable
instructions, session/checkpoints, section manifest, decision records, draft
snapshots and gate receipts. Tests observe all file operations, delegation order,
timeouts and prompts. No fixture relies on newest-file selection or conversation-only
resume state.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches the directory.
- [ ] Invocation explicitly supports `new`, `resume`, and `revise`.
- [ ] New mode refuses to replace an existing concept.
- [ ] Resume/revise captures source raw hash, section ownership/status, selected IDs, and custom sections.
- [ ] Non-selected existing sections remain byte-for-byte preserved.
- [ ] Final MODIFY is compare-and-set against the original raw hash and selected section set.
- [ ] Checkpoint authorization and final concept authorization are separate exact changesets.
- [ ] Product decisions remain user-owned and are distinct from file authorization.
- [ ] Full mode runs exactly `CD-PILLARS -> AD-CONCEPT-VISUAL -> TD-FEASIBILITY -> PR-SCOPE`.
- [ ] The four gate nodes are never dispatched in parallel.
- [ ] REJECT has no override path and prevents final concept write.
- [ ] CONCERNS remains CONCERNS and may continue only through documented advisory acceptance.
- [ ] TIMEOUT/BLOCKED/ERROR/partial gate evidence stops dependents and prevents final write.
- [ ] Upstream section changes stale and rerun dependent gate receipts.
- [ ] Lean/solo mark all four nodes `NOT_RUN_BY_MODE`; solo spawns none.
- [ ] User and gate revision loops have bounded rounds, Keep checkpoint and Stop exits.
- [ ] Checkpoints are immutable, predecessor/hash-bound and resume idempotently.
- [ ] Unsourced market/platform claims are hypothesis/unknown.
- [ ] Engine choice is recorded as preference or deferred, never recommended here.
- [ ] Timeline/content values are user assumptions/budgets or sourced, not model facts.
- [ ] Concept-specific review validates substantive sections, provenance, assumptions and open questions.
- [ ] No system-design/GDD review invocation exists.
- [ ] Final output recommends at most one next action and never invokes it.
- [ ] Metadata describes collaborative new/resume/revise behavior.

## Case 1: New concept happy path

**Input**

~~~text
$brainstorm new --session-id bs-001 --review lean
~~~

The canonical concept is absent. The user authorizes checkpoint files, selects one of
three concepts, locks decisions within bounded rounds, and authorizes the exact final
CREATE.

**Expected**

- all required sections and decision provenance are substantive or explicitly open;
- four gates are `NOT_RUN_BY_MODE`;
- concept-specific review is `CONCEPT READY` or documented advisory concerns only;
- atomic write/read-back succeeds and returns the output SHA-256;
- no other project file changes;
- exactly one state-driven next action is suggested.

## Case 2: New refuses overwrite

The canonical concept already exists.

**Expected**

New mode returns `BLOCKED`, displays resume/revise forms, spawns no agents, and writes
neither concept nor checkpoint.

## Case 3: Resume selects only open sections

Existing concept contains locked identity/pillars, open MVP/risks, and custom lore.
The user selects MVP and risks.

**Expected**

Only those two section IDs become selected. Identity, pillars, provenance not involved
in the current decision, and custom lore retain exact source bytes. The diff lists
preserved ranges and the final CAS uses the original file hash.

## Case 4: Revise rejects scope expansion

Invoke revise with `--sections CONCEPT-CORE-LOOP`, then attempt to rewrite pillars.

**Expected**

The pillar edit is excluded and reported as a revised-boundary request. No write occurs
until a new selected set and exact diff are authorized.

## Case 5: Concurrent source change

After final preview but before write, another actor changes one unselected byte.

**Expected**

CAS fails, `Document State: CONFLICT`, no overwrite, source and draft are preserved,
and the next action is merge in a new session.

## Case 6: Custom and unknown sections

Existing concept contains two user-authored headings not in the stable schema.

**Expected**

Both receive preservation IDs and remain user-owned. Resume does not drop, reorder, or
normalize them unless explicitly selected under a revised manifest.

## Case 7: Full gate DAG order

**Input**

~~~text
$brainstorm new --session-id bs-full --review full
~~~

All gates pass.

**Expected**

CD receives pillar/core hashes first. AD starts only after CD disposition and consumes
confirmed pillar hashes. TD starts only after visual-anchor choice. PR starts only
after TD and scope-tier inputs exist. At most one gate node is active; receipts bind
the exact draft snapshot. Final write occurs only after PR and concept review.

## Case 8: Parallel gate attempt is rejected

Attempt to dispatch AD, TD, or PR while CD is active or unresolved.

**Expected**

The controller refuses the dispatch, records the dependency violation, and preserves
the sequential DAG. No downstream receipt is accepted.

## Case 9: Lean mode

All four gates are `NOT_RUN_BY_MODE`; no gate agents spawn. The user-owned concept
review and write boundary still apply. No misleading “PASS” is emitted.

## Case 10: Solo mode

Behavior matches lean gate omission, and no director/producer agent is spawned.
Checkpoint and concept persistence rules remain unchanged.

## Case 11: REJECT cannot be overridden

CD returns REJECT for missing creative pillars.

**Expected**

The rejection receipt and feedback are shown. Final concept is not written. Options
are revise the affected sections and rerun CD within the bounded attempts, checkpoint
and stop, or stop. There is no override/proceed option.

## Case 12: CONCERNS remains visible

TD returns CONCERNS on a policy-advisory uncertainty.

**Expected**

The user may revise, checkpoint/stop, or document the concern with rationale, impact,
owner and review point. Status remains CONCERNS and the concept review can return only
`CONCEPT WITH DOCUMENTED CONCERNS`, not silently PASS.

If policy marks the concern blocking, dependent gates and final write do not proceed.

## Case 13: Gate timeout/partial result

AD times out after CD PASS; a late AD result references an older draft hash.

**Expected**

Workflow is PARTIAL, TD/PR do not run, final concept is not written, checkpoint names
deadline/attempt/missing evidence, and the late receipt is stale. One retry maximum
applies.

## Case 14: Upstream revision invalidates downstream evidence

After all full-mode gates pass, the user changes a pillar.

**Expected**

CD and all downstream gate receipts become STALE. They rerun in order; old receipts
cannot support final review or writing.

## Case 15: Bounded user revision

The user requests three successive pillar revisions.

**Expected**

Only two occur in this session. The third request writes the authorized checkpoint
and returns `STOPPED`, preserving the draft and next permitted section.

## Case 16: Concept generation bound

The user rejects every option twice and asks for more.

**Expected**

At most two concept rounds are generated. The workflow checkpoints and stops rather
than continuing indefinitely. A user may request two to four concepts per round;
default is three.

## Case 17: Evidence labels

No external research receipts exist. The draft discusses market size, comparable
success, console support, schedule and content counts.

**Expected**

Market/platform statements are `MODEL HYPOTHESIS` or `UNKNOWN`; schedule/content are
`USER ASSUMPTION`, `USER BUDGET`, or `UNKNOWN`. No citation, current platform fact,
formal estimate or engine recommendation is fabricated.

## Case 18: Concept-specific completeness review

Draft has every heading but one placeholder, one unsupported market fact, missing
decision provenance, and a blocking open question.

**Expected**

`CONCEPT INCOMPLETE`; heading existence does not count as completeness and final write
is not offered until the blocking defects are resolved or explicitly retained as
allowed open questions.

## Case 19: Checkpoint and idempotent resume

Interrupt after visual-anchor selection.

**Expected**

Resume uses the exact checkpoint path, verifies the predecessor chain, ABSENT-or-hash
source state, selected set, decision IDs, draft snapshot and gate receipts, then
continues at feasibility. It does not replay concept
selection, overwrite a checkpoint, or choose the newest session.

## Case 20: Atomic write and state-driven stop

A section-scoped resume passes review and receives exact concept authorization.

**Expected**

The workflow re-hashes source/instructions/preserved sections, atomically writes,
reads back, validates section IDs/provenance/preservation, and returns the final hash.
It suggests one relevant next action or Stop and invokes nothing else.

## Protocol compliance

- [ ] All concept, pillar, visual and scope choices belong to the user.
- [ ] Resume/revise never replace unselected authoritative content.
- [ ] The full gate DAG and test order are identical and deterministic.
- [ ] Reject, partial and stale evidence cannot support a final write.
- [ ] Checkpoints and loops make long sessions bounded and resumable.
- [ ] Market/engine/schedule claims retain evidence/owner boundaries.
- [ ] The concept review profile is specific to concept content.
- [ ] Persistence is exact, atomic and compare-and-set.
