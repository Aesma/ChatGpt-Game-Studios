# Skill Test Spec: $architecture-decision

## Skill Summary

`$architecture-decision` authors or retrofits exactly one Architecture Decision
Record and leaves it `Proposed` (or `Unknown` for a legacy retrofit whose
lifecycle evidence is unavailable). Review mode controls advisory review only.
No advisory result, user write approval, or retrofit answer may produce
`Accepted`.

Acceptance is a separate lifecycle operation: an independent
`$architecture-review` record must bind its verdict to the current ADR SHA-256,
and a separate recorder must validate that record before recording the
transition and deriving registry state.

The skill has a strict mutation boundary. It may write only the target ADR. GDDs,
architecture/traceability registries, stories, readiness state, review records,
and lifecycle records remain unchanged.

## Required ADR content

A newly authored ADR contains:

- Status (`Proposed`);
- Date;
- Engine Compatibility;
- ADR Dependencies;
- Context;
- Decision and Key Interfaces;
- Alternatives Considered;
- Consequences and Risks;
- GDD Requirements Addressed;
- Performance Implications;
- Migration Plan;
- Validation Criteria;
- Related Decisions.

## Fixtures

Each case snapshots these protected paths before invocation:

- `design/gdd/**`;
- `docs/registry/**`;
- story and epic files;
- review and lifecycle records;
- every ADR except the selected target.

After invocation, compare content hashes. Only the authorized target ADR may
change.

## Case 1: New ADR remains Proposed after positive full-mode advice

**Given**

- A configured engine and relevant engine-reference files.
- `--review full`.
- Engine specialist and technical-director advisory reviews both return
  positive findings.
- The user authorizes the one-file ADR changeset.

**Expected**

1. The skill drafts all required sections.
2. Advisory reviews are labeled `ADVISORY`.
3. The target ADR is written with `## Status` followed by `Proposed`.
4. Output reports the target path and current SHA-256.
5. No acceptance or lifecycle record is created.

**Assertions**

- [ ] Positive advisory results do not set `Accepted`.
- [ ] No `$architecture-review` is spawned in the authoring context.
- [ ] No recorder is invoked.
- [ ] Only the target ADR hash changes.

## Case 2: Retrofit cannot self-sign acceptance

**Given**

- A legacy ADR with no `## Status` section.
- No independent hash-bound review record.
- The user invokes `retrofit <path>`.

**Expected**

- The only status choices are `Proposed` and `Unknown`.
- The skill never offers, infers, or writes `Accepted`.
- Missing authorized sections may be appended to the target ADR only.
- Output instructs the user to obtain a fresh independent review of the
  resulting current hash.

**Assertions**

- [ ] `Accepted`, `Deprecated`, and `Superseded` are not retrofit choices.
- [ ] Ambiguous evidence produces `Unknown`, not `Accepted`.
- [ ] Existing `Accepted`, `Deprecated`, or `Superseded` ADRs cause a lifecycle
  handoff and are not mutated.
- [ ] Only the retrofit target hash may change.

## Case 3: Technical naming mismatch stays out of GDD

**Given**

- A GDD uses a product term that differs from the proposed signal, method, or
  data type name.
- The player-facing product rule is unchanged.

**Expected**

- The finding destination is `ADR/TECH`.
- The ADR records the technical interface and maps it to the GDD term.
- The GDD remains byte-for-byte unchanged.
- The one-file changeset preview contains only the ADR.

**Assertions**

- [ ] Technical names are not back-propagated into GDDs.
- [ ] “ADR + update GDD” is not offered.
- [ ] GDD hashes remain unchanged.

## Case 4: Product-rule differences go to the design owner

**Given**

- The proposed technical approach requires a player-visible or balance rule to
  change.

**Expected**

- The finding destination is `GDD PRODUCT RULE`.
- Finalization of the affected choice stops.
- The skill hands the finding to the design owner or
  `$propagate-design-change`.
- No GDD is edited by this workflow.

**Assertions**

- [ ] Product ownership is explicit.
- [ ] The ADR does not silently redefine the product rule.
- [ ] GDD hashes remain unchanged.

## Case 5: Registry conflict requires supersession or a scoped exception

**Given**

- `docs/registry/architecture.yaml` contains an accepted global stance that
  conflicts with the proposal.

**Expected**

- The registry is read as a constraint projection.
- The user must align, propose explicit supersession, or define an objectively
  disjoint scoped exception.
- A free-form “intentional exception” without scope is rejected.
- A Proposed supersession does not deactivate the accepted stance.
- No registry file is edited.

**Assertions**

- [ ] Two contradictory global stances cannot remain active.
- [ ] Supersession remains proposed until independent acceptance and recording.
- [ ] Scoped exception includes boundary predicate, owner, reason, and exit
  condition.
- [ ] Registry hashes remain unchanged.

## Case 6: Blocked stories are never promoted by the ADR author

**Given**

- The ADR `Blocks` or `Enables` field names a blocked story.

**Expected**

- The story file is unchanged.
- Output emits `event: dependency_may_be_unblocked` with ADR path, current
  SHA-256, affected item, and
  `eligibility: pending_accepted_lifecycle_record`.
- Output directs readiness evaluation to `$story-readiness`.

**Assertions**

- [ ] No `Status: Blocked` to `Status: Ready` edit occurs.
- [ ] The event is labeled non-mutating and conditional.
- [ ] Story hashes remain unchanged.

## Case 7: Acceptance evidence must be independent and current-hash-bound

**Given**

- The ADR has been written.
- Scenario A supplies no architecture-review record.
- Scenario B supplies a review record for an older ADR hash.
- Scenario C supplies a current-hash review record, but the reviewer session is
  the authoring session.

**Expected**

- In every scenario the author workflow leaves the ADR `Proposed`.
- It reports missing, stale, or non-independent evidence.
- It directs a separate recorder to validate a fresh independent review; it does
  not perform the transition itself.

**Assertions**

- [ ] Missing review evidence cannot accept.
- [ ] A stale hash cannot accept.
- [ ] Same-context review cannot accept.
- [ ] The author never writes lifecycle state or review records.

## Review-mode contract

- `solo`: no advisory agents.
- `lean`: configured primary engine specialist only.
- `full`: configured primary engine specialist and technical-director;
  both are advisory and may run in parallel.
- Any approval, concern, rejection, timeout, or failure leaves the ADR
  `Proposed`.

## Protocol compliance

- [ ] The exact one-file changeset is authorized once before the first write.
- [ ] The target ADR is the only permitted mutation.
- [ ] New ADR status is always `Proposed`.
- [ ] Retrofit status is only `Proposed` or `Unknown`.
- [ ] GDD findings use `ADR/TECH` or `GDD PRODUCT RULE` destinations.
- [ ] Registry conflicts require alignment, explicit supersession, or a scoped
  exception.
- [ ] Registries and stories are never written.
- [ ] Output includes target SHA-256 and the independent review/recorder handoff.
- [ ] Output does not claim that a blocked dependency is Ready.

## Coverage notes

The following are deliberately outside this P0 contract and require separate
coverage when their owning remediations land: collision-safe ADR ID allocation,
semantic duplicate detection, bounded context manifests, dependency-cycle
validation, engine-reference freshness, resumable checkpoints, append-only
lifecycle history, and stable requirement IDs.
