# Prototype — Required evidence and publication continuation

Read this file in full after the main prototype run reaches its Required
continuation. These phases do not inherit authority from the execution changeset
for project index, final report, decision state, graveyard, or downstream work.

## Phase 7: Evidence analysis and advisory recommendation

Re-read and hash:

- `PROTOTYPE-MANIFEST.yaml` and `CHECKPOINT.yaml`;
- current prototype source manifest;
- every build receipt/log;
- every real play/observation record;
- the hypothesis and thresholds;
- the remaining/consumed budget.

Reject stale evidence whose build/source hashes do not match the evaluated
prototype.

Create/update the already execution-authorized
`REPORT-DRAFT.md` and `PUBLICATION-PROPOSAL.yaml` inside the throwaway root. Mark
both:

> NON-AUTHORITATIVE DRAFT — NOT A PRODUCT DECISION

The draft separates:

```markdown
## Experiment identity
[prototype/hypothesis/build/source hashes]

## Observed facts
[only directly measured/observed evidence]

## Participant reports
[attributed and consent-safe]

## Build results
[commands, environment, exit codes, artifacts/log hashes]

## Play results
[session/build IDs, protocol, observations, measurements]

## Not run / not observed
[explicit gaps]

## Model inferences
[reasoning derived from evidence]

## Recommendation
RECOMMENDATION: PROCEED | PIVOT | KILL | INCONCLUSIVE
Confidence: [...]
Evidence supporting: [...]
Evidence against/limits: [...]
```

Recommendation rules:

- `PROCEED` only when current build/play evidence satisfies the predeclared
  threshold for the specific hypothesis.
- `PIVOT` when evidence identifies a testable change and preserves what worked.
- `KILL` is an advisory option only when evidence strongly contradicts the
  hypothesis; iteration count never forces it.
- `INCONCLUSIVE` when build/play was not run, evidence is stale, thresholds were
  not observed, the selected mode cannot test the claim, or the budget ended
  before a trustworthy result.

A successful build without real play cannot support a player-feel/fun PROCEED
recommendation. A model simulation cannot support human behavior claims.

No creative director or other agent has final authority. An optional reviewer may
comment on evidence, but its output is `ADVISORY_REVIEW` and cannot overwrite the
draft recommendation, create a final decision, or mutate report/index files.

## Phase 8: User decision

Present the evidence matrix, limitations, and advisory recommendation. Ask the
user to choose:

- `PROCEED` — continue to a separately authorized design/discovery step;
- `PIVOT` — define a revised hypothesis for a new separately authorized prototype;
- `KILL` — record that the user is stopping this line of exploration;
- `DEFER` — preserve evidence without selecting a direction;
- `REQUEST MORE EVIDENCE` — plan a new bounded run; do not extend this exhausted
  or completed run automatically.

Record nothing as `USER_DECISION` until the user explicitly selects it. Silence,
agent advice, risk acceptance, a third pivot, or a PROCEED recommendation is not
a decision.

Even after the user selects `PROCEED`:

- the concept and GDD remain unapproved;
- no architecture, production code, assets, epic, story, sprint, or phase gate is
  authorized;
- no downstream workflow may be invoked automatically;
- the decision means only that the user wants to continue.

A `PIVOT` choice does not authorize another prototype. The next run needs a new
prototype ID, hypothesis, hard budget, throwaway root, and execution changeset.

A `KILL` choice does not authorize deletion. Prototype evidence is retained.
Any graveyard entry must be explicit, recoverable, and part of the publication
changeset; it may later receive a user-authorized `REOPENED` record.

If the user does not decide, stop with `EXPERIMENT COMPLETE — DECISION PENDING`
or `PARTIAL/BLOCKED`. Do not publish authoritative decision state.

## Phase 9: Separately authorize atomic publication

Publication is optional. The execution changeset does not authorize it.

After an explicit user decision, render the complete publication group in memory:

- final `REPORT.md` under the throwaway root;
- `DECISION.md` under the throwaway root;
- one exact row/update in `prototypes/index.md`;
- for `PIVOT`, exact `PIVOT-NOTE.md` under the throwaway root;
- for `KILL`, exact entry in `prototypes/GRAVEYARD.md`;
- exact temporary/transaction paths required for an all-or-none commit.

Every artifact records the same:

- publication transaction ID;
- prototype/hypothesis/build IDs;
- source/build/play/evidence hashes;
- advisory recommendation;
- explicit user decision and timestamp;
- decision scope: `EXPERIMENT ROUTING ONLY — NOT PRODUCT APPROVAL`;
- recovery/reopen semantics where applicable.

Preview exact path, operation, owner, base hash/ABSENT, and full proposed content.
Ask for one publication changeset approval. Code/asset write approval, user
decision, or recommendation does not substitute for this filesystem approval.

### CAS and all-or-none rule

Before publication:

1. re-read every final target and verify previewed base hashes/absence;
2. verify execution evidence is unchanged;
3. stage every complete candidate in the exact authorized transaction paths;
4. validate cross-file transaction ID, decision, IDs, links, and hashes;
5. confirm the environment can apply the whole group atomically or can guarantee
   rollback without exposing a partially authoritative state.

If any check fails, or atomic/rollback safety is unavailable:

- do not modify any final report/index/decision/graveyard target;
- keep `REPORT-DRAFT.md` explicitly non-authoritative;
- write only the already-authorized in-root recovery/proposal state;
- return `PARTIAL — PUBLICATION NOT COMMITTED` with conflicts.

Never write REPORT then index later, and never revise REPORT after a reviewer
changes a recommendation. A reviewer cannot change the user's decision.

After commit, re-read all targets. Publication is valid only when every member
contains the same transaction ID and current evidence hashes. Otherwise report
`BLOCKED — PUBLICATION INCONSISTENT` and do not present the group as authoritative.

## Phase 10: Outcome and handoff separation

Report independently:

```yaml
run_status: COMPLETE | PARTIAL | BLOCKED | CANCELED
build_status: PASS | FAIL | TIMED_OUT | NOT_RUN
play_status: OBSERVED | NOT_RUN | STALE
recommendation: PROCEED | PIVOT | KILL | INCONCLUSIVE
user_decision: PROCEED | PIVOT | KILL | DEFER | MORE_EVIDENCE | PENDING
publication: COMMITTED | NOT_REQUESTED | NOT_AUTHORIZED | CONFLICTED
product_approval: NOT_GRANTED
```

`run_status: COMPLETE` means the bounded experiment and its evidence protocol
finished. It does not mean the concept or mechanic is approved.

Recommend at most one legal next action based on the user decision and current
project stage. Describe it but do not invoke it. Any next workflow, file change,
prototype run, graveyard reopening, or production implementation requires its
own scope and authorization.
