# Phase validation on the combined candidate

Use profiles matching the complete delivery scope and dependencies. This overlay
does not replace existing skill verdicts, story statuses or phase gates. Profiles
combine when a batch crosses domains; Git cannot certify product semantics.

Reconstruct each delivery's cumulative changes from its fixed task-base SHA to
its fixed delivery SHA, validate that history, and reconcile this with the
handover file scope. Add affected dependencies and all integration corrections.
Do not substitute the helper's target/source merge-base diff for the original
task scope. An already-ancestor source may have an empty helper `changed_files`
list even after the target reverted its behavior; ancestry skips duplicate Git
merges, never acceptance revalidation. Missing original base or scope must be
recovered from explicit handover/history or obtained from the user; otherwise
report NOT VERIFIED rather than infer zero checks.

Commit merges and fixes before validation; evidence names exact candidate HEAD.
Prefer read-only review output recorded in the ignored journal. Optional tracked
reports are not required. If an existing workflow writes approved corrections
or records, commit them and refresh affected evidence before promotion. An
unrun requirement is NOT VERIFIED.

## GDD and shared design facts

1. Inspect merged index/registry structure, duplicate identifiers, missing paths,
   ownership and counts. Source GDD sections establish design meaning; a registry
   record cannot override the approved source from which it was derived.
2. Run `$design-review` on every added/substantively changed system GDD and any
   GDD changed semantically during conflict resolution. Respect its `--depth` and
   required phases. It is read-only and never writes Approved/index/review logs.
3. Preserve author independence: `$design-system` requires design-review in a
   fresh independent chat. An integration chat that authored a source GDD cannot
   self-certify independence. Obtain an independent review of the exact candidate;
   missing evidence is NOT VERIFIED. A fresh independent integration chat may
   review. Do not simulate a review or substitute a subagent inheriting the
   full author conversation.
4. Recommend `$consistency-check` for registry values, formulas, ownership and
   dependencies, retaining its optional status in the original workflow. Not
   running it is not missing required integration evidence. Known conflicts,
   stale registry entries and missing evidence for applicable required checks
   still need resolution; an optional check does not waive known issues.
5. Keep `$review-all-gdds` at the original milestone: all MVP system GDDs are
   authored and individually approved, before advancing to Technical Setup.
   Determine readiness from the combined candidate's systems index and actual
   GDDs, not the number of existing documents or completion of this batch.
   Until that milestone, report the cross-GDD review as not yet due; do not run
   it or treat its absence as missing required evidence for this batch. At the
   milestone, run `$review-all-gdds full` on the actual index-listed set for
   rules, formula interfaces, shared resources, AC and player scenarios, subject
   to that skill's normal prerequisites. Do not invent PASS when a prerequisite
   is unmet, and keep phase advancement under the existing `$gate-check` rules.
6. If changed GDDs have downstream ADR/TR/Epic/Story references, use
   `$propagate-design-change` per changed GDD. Its normal comparison may show
   only the last path-changing commit: also inspect the cumulative target-base
   to candidate diff so a conflict-fix commit does not hide earlier delivery
   changes. Record both scopes. Resolve relevant stale decisions through their
   existing workflows, not by silently changing Accepted ADRs or active stories.

Design-review blockers, consistency conflicts/missing required evidence and
cross-review FAIL prevent VERIFIED. CONCERNS needs visible warnings and all
required user decisions satisfied; never relabel it PASS. Expert review approval
is not user approval of a new product decision. A completed GDD may integrate
once this batch's applicable required checks pass even while other MVP GDDs
remain unfinished. Record the deferred project-wide review separately; a
verified batch does not mean all GDDs or the Systems Design gate have passed.
An intentionally incomplete GDD included in this delivery retains its
draft/designed status and remains integration NOT VERIFIED until its applicable
checks can complete.

Two branches may have approved incompatible rules. Present both source sections,
shared baseline and downstream effects. Let the user choose retained rules or
revisions, then update every affected source and summary record and recheck.
Never select authority by merge order, branch name or whole-file ours/theirs.

## Source code and story delivery

- Run real project tests/build checks from repository guidance and story QA
  cases for changed implementation/config/interfaces. Exercise the affected
  integration boundary, not only isolated handover tests. Record actual commands,
  results and checked SHA.
- Use `$code-review` for combined implementation and governing GDD/ADRs. Respect
  its actual verdict and configuration; do not weaken global review mode.
- Recheck affected story AC, evidence and deviations using `$story-done`'s
  verification requirements. Already Complete stories receive read-only
  revalidation, not another closing run. Do not duplicate Completion Notes or
  timestamps. Failed revalidation blocks integration and follows existing
  explicit correction/reopen decisions; never reopen silently or trust stale Done.
- A genuinely unfinished story may use normal `$story-done` closure as a separate
  authorized operation with all prerequisites. Commit its approved output and
  refresh affected evidence before promotion.
- Required UI, Visual/Feel and playtest evidence must cover combined behavior and
  have required human sign-off. Source-only sign-off is insufficient when the
  integration changed that behavior. Missing/stale human evidence is NOT VERIFIED.
- At Sprint QA handoff, retain `$smoke-check sprint` then `$team-qa sprint` and
  their evidence gates. Do not force full Sprint closure for a small batch, or
  claim a verified batch means Sprint QA passed.

## Other stages

Reuse existing domain checks against final artifacts: `$architecture-review`
for GDD/ADR/TR relationships, `$ux-review` for UX specs, `$asset-audit` for asset
standards and existing project checks for other outputs. Read their scopes and
prerequisites; never send unsupported artifacts to a check. A missing mandatory
check is missing evidence. If no established check covers a material domain,
define acceptance evidence with the user before claiming VERIFIED rather than
inventing a new domain gate.

## Stage state and phase-transition authority

`$gate-check` remains the phase-advancement workflow. A source branch may already
contain its own gate-driven `production/stage.txt` update; merging that file
would change the target stage even if this skill never writes it directly.

Record the target's stage at the pinned target SHA before merging. Compare it
with the candidate after all source merges/fixes and again after every target
refresh and immediately before promotion. Read the actual stage field using
its existing first-nonempty-line convention; do not infer stage from filenames
or a source's completion label. Preserve evidence of both values in the journal.

Ordinary integration authorization does not authorize a phase transition:

- For an understood stage difference, restore the current target's exact stage
  value in the candidate only if that targeted field edit was included in the
  integration preview. Preserve unrelated file content and source branches;
  commit the correction and revalidate affected evidence.
- If that restoration was not authorized, or either changed field is missing,
  malformed, ambiguous or cannot be safely edited, block promotion and request
  the specific interpretation/correction. Do not whole-file copy, invent a
  stage, delete an unfamiliar file or silently accept the source value. If both
  target and candidate lack stage state, record no transition rather than create it.
- A stage change may remain only with separate explicit authorization for that
  transition on the combined candidate and complete applicable `$gate-check`
  evidence for that combined revision. Branch-local gate results cannot satisfy
  this condition. Perform the gate's normal decisions and requirements, commit
  the authorized stage result, then refresh integration evidence against final
  candidate HEAD before promotion. Do not advance unrelated tasks.

If the target moves, refresh its stage from the new pinned target SHA and repeat
this comparison and any transition gate/evidence checks. Never restore an older
target stage over a newly authorized target transition. Without these checks,
report NOT VERIFIED/BLOCKED; do not claim that integration preserved the stage.

## Evidence and labels

Keep original task verdicts as evidence about their original revisions. Add a
separate integration label:

- **VERIFIED at SHA**: every applicable required check ran on final candidate;
  no blocker or unresolved decision remains; policy-allowed advisory conditions
  are explicit. Only this state may promote.
- **NOT VERIFIED at SHA**: evidence is missing, stale, partial or not run. Name
  the exact missing checks/human evidence; leave target unchanged.
- **BLOCKED at SHA**: failing test/review, unresolved product decision or invalid
  Git/input state prevents verification. Retain candidate and journal.

Candidate edits and target refreshes invalidate affected evidence. Re-run those
checks on the new exact commit; when impact cannot be bounded, rerun all batch
checks. Never relabel a source PASS as candidate PASS.
