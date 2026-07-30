# Skill Test Spec: `$onboard`

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

## Skill Summary

`$onboard` returns a bounded, visibility-filtered, source-cited repository
orientation in conversation. It is read-only in every path, requires root
AGENTS.md, applies the complete applicable nested-instruction chain, denies
sensitive sources before access, uses deterministic content/Git budgets, keeps
repository roles separate from human organization, and reports ONBOARDING READY,
ONBOARDING PARTIAL, or ONBOARDING ERROR.

Optional stage and project-recommendation context comes only from explicitly
supplied current canonical detector/help evidence. Onboard never invokes or
reimplements either producer.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name
      matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains ONBOARDING READY, ONBOARDING PARTIAL, and ONBOARDING ERROR
- [ ] Explicitly forbids ONBOARDING COMPLETE
- [ ] Every path is strictly read-only; save, authorization, output-path
      invention, mutation, delegation, and downstream invocation are forbidden
- [ ] `--save` is rejected and persistence is a separately scoped document task
- [ ] Root AGENTS.md is mandatory and read before secondary project context
- [ ] Every opened/recommended path loads its physical root-to-parent AGENTS chain
      first and closest applicable rules win conflicts
- [ ] Defines enumeration-entry, opened-file, per-file-byte, total-byte, depth,
      and explicit Git-range commit budgets
- [ ] Visibility and sensitive-data denial occur before stat/open/revision
- [ ] Sensitive omission never reveals identifying path/filename/metadata details
- [ ] Repository roles are separate from human title, manager, reporting line,
      access, assignment, and decision authority
- [ ] Git requires explicit from_ref/to_ref, redacts personal/private metadata,
      and never infers momentum/productivity/velocity/performance
- [ ] Missing/invalid root instructions return ERROR without partial narrative
- [ ] Every fact has path/artifact, locator, revision, source state, instruction chain,
      visibility, and DIRECT/UNKNOWN confidence
- [ ] Canonical stage source is exactly `cgs.project-stage-detection/v2`; no local
      stage algorithm exists
- [ ] Optional help recommendation validates matching packet/catalog identity and
      remains external/unexecuted
- [ ] Emits `onboarding_context/v2`, source manifest identity, one non-mutating
      next action, and no-execution markers

---

## Director Gate Checks

None. Onboard is read-only and invokes no director, subagent, gate, detector,
help workflow, recorder, or downstream project skill.

---

## Test Cases

### Case 1: Complete bounded repository orientation

**Fixture:**

- Root AGENTS.md and every applicable nested instruction are current/readable
- Exact repository role ID resolves from an authoritative index
- Relevant project indexes and representative sources fit all budgets
- No sensitive or visibility-denied source affects requested scope
- Optional canonical stage packet and matching help envelope are CURRENT
- Every recommended file is readable, unchanged, and governed by a complete chain

**Input:**

`$onboard gameplay-programmer --visibility internal` with explicit stage/help evidence

**Expected behavior:**

1. Resolves repository role without inferring human organization.
2. Validates stage/help identities without invoking their producers.
3. Builds only DIRECT facts with source and instruction-chain citations.
4. Returns one non-mutating orientation action.
5. Returns ONBOARDING READY.

**Assertions:**

- [ ] Budget and source-manifest identities are present
- [ ] Stage/help data retain diagnostic/external labels
- [ ] All project facts and recommended files are traceable
- [ ] Files Written is none and Auto Executed is false

---

### Case 2: P0 regression — default invocation is zero mutation

**Fixture:** A configured repository has sufficient safe onboarding sources; no
persistence option is supplied.

**Input:** `$onboard`

**Expected behavior:** Returns GENERAL orientation in conversation with READY or
PARTIAL according to relevant coverage, no changeset, no authorization prompt,
no output path, and no file creation.

**Assertions:**

- [ ] No implicit onboarding filename or directory is invented
- [ ] No save option is offered
- [ ] Mutation and invocation spies remain zero

---

### Case 3: P0 regression — persistence request never guesses a path

**Fixture:** Plausible onboarding filenames already exist in several directories.

**Input:** `$onboard artist --save`

**Expected behavior:** Identifies unsupported persistence, explains the separate
explicit-path/collision-policy requirement, and stops without inspecting output
candidates or asking authorization.

---

### Case 4: ON-003 — complete nested instruction chain governs every target

Run these variants:

| Variant | Fixture | Expected |
|---|---|---|
| 4a | Root and nested design/AGENTS.md conflict on visibility/convention | Closest design rule wins that subject; non-conflicting root rules remain |
| 4b | Two nested levels apply to one recommended file | Root→parent chain order and revisions are reported |
| 4c | Applicable nested AGENTS.md is unreadable/invalid | Governed target is not opened/recommended; PARTIAL + UNKNOWN_INSTRUCTION_CHAIN |
| 4d | Nested rule denies a source root recommended by an index | Denial occurs before target stat/open/revision |
| 4e | Candidate real path escapes through symlink | Candidate rejected; no outside-root read |

**Assertions:**

- [ ] Instruction files are read before governed target content
- [ ] Root AGENTS.md is not reused as the only rule source
- [ ] Override records name subject, ancestor source, closest source, and decision
- [ ] A permissive ancestor never bypasses a restrictive closest rule
- [ ] Every recommended file cites its effective chain

---

### Case 5: ON-004 — repository and enumeration scans are deterministically bounded

**Fixture:** `src`, `design`, `tests`, `production`, `assets`, and agent trees contain
thousands of files; authoritative indexes fit the default budget, while extra
role-relevant candidates exceed one limit at a time.

Run limits for 256 enumerated entries, 64 opened content files, 256 KiB per file,
1 MiB total bytes, and depth 6.

**Expected behavior:**

1. Applies configured limits or all exact defaults before enumeration/read.
2. Uses manifest/index order then normalized path tie-break.
3. Never full-reads a large directory or partially reads an oversized file.
4. Records consumption and generic OMITTED_BUDGET topics/reasons.
5. Returns PARTIAL when omission affects requested/role-relevant coverage.

**Assertions:**

- [ ] Enumeration itself is budgeted
- [ ] Per-file and total bytes are both enforced
- [ ] No silent truncation, limit increase, or guessed omitted summary
- [ ] Omitted content cannot support DIRECT facts

---

### Case 6: ON-005 — sensitive and private material is denied before access

**Fixture:** Safe indexes reference environment variants, credentials, tokens,
private keys, personnel/payroll records, private correspondence, raw exploit/
incident/anti-cheat reports, and safe architecture sources.

**Expected behavior:**

1. Applies visibility/deny rules before stat/open/revision/content ingestion.
2. Sensitive candidates never enter content reads or revision output.
3. Output uses only generic OMITTED_SENSITIVE/OMITTED_VISIBILITY codes.
4. No path, basename, extension, existence detail, size, timestamp, owner, revision,
   secret-shaped value, or exploit detail identifies the omitted item.
5. Denied sources are never recommended.

**Assertions:**

- [ ] Spy proves denied files were not opened, not merely redacted later
- [ ] Supplied stage/help evidence referencing sensitive paths is omitted safely
- [ ] User request and internal visibility cannot override a repository/environment denial
- [ ] Safe facts remain usable; status is PARTIAL only when requested scope is affected

---

### Case 7: ON-006 — repository roles are not human organization

**Fixture:** A role/agent definition describes review ownership and workflow
responsibilities; no visibility-allowed human organizational mapping exists.

**Input:** `$onboard qa-lead`

**Expected behavior:**

- Summarizes repository workflow responsibilities with citations.
- Reports job title, manager, reporting line, employment/team status, access,
  assignment authority, and decision authority as UNKNOWN.
- Does not infer organization from reviewer labels, agent prompts, role name, or
  CODEOWNERS-like routing.

**Assertions:**

- [ ] Output never says who the contributor reports to
- [ ] Workflow owner is not presented as a human manager
- [ ] Missing organization/access facts remain UNKNOWN
- [ ] Next action is not framed as a manager expectation or assigned task

---

### Case 8: ON-007 — Git activity uses one explicit privacy-safe window

Run these variants:

| Variant | Fixture | Expected |
|---|---|---|
| 8a | No authoritative from_ref/to_ref | No Git read; activity UNKNOWN/OMITTED_POLICY |
| 8b | Valid explicit range with >20 commits | At most configured/default 20; PARTIAL if relevant remainder omitted |
| 8c | Invalid/unreadable refs or unredactable required content | No raw fallback; PARTIAL when relevant |
| 8d | Valid range contains names/emails/signatures/tickets/branches/raw messages | Personal/private fields absent; safe technical themes only |

**Assertions:**

- [ ] No “recent,” HEAD~N, date guess, current branch, all-branch, reflog, or full-history fallback
- [ ] Exact range purpose and commit budget are reported
- [ ] No author/committer identity or raw message is exposed
- [ ] Commit count/frequency/authorship never becomes momentum, productivity,
      velocity, staffing, ownership, performance, or contributor attribution

---

### Case 9: ON-008 — root AGENTS failure cannot produce partial onboarding

Run missing, unreadable, malformed, visibility-denied, outside-root, and
repository-identity-unverified root cases while secondary config/sprint/role
files exist.

**Expected behavior:**

1. Returns ONBOARDING ERROR with exact generic root failure code.
2. Reads no secondary project-context source.
3. Generates no onboarding narrative, technology, role, stage, current work,
   hierarchy, or recommended-file claim.
4. Returns at most one non-mutating remediation question.

**Assertions:**

- [ ] Secondary files never substitute for repository authority
- [ ] Root failure never becomes PARTIAL or READY
- [ ] Error path remains visibility-safe and read-only
- [ ] Parent/nested/cached/generated AGENTS.md is not substituted

---

### Case 10: Canonical stage evidence is optional and never recomputed

Run stage packet variants: CURRENT DETECTED/CLEAR, CURRENT UNKNOWN/BLOCKED with
reproducible ABSENT/UNREADABLE evidence, CURRENT CONFLICT, missing, invalid,
stale, project mismatch, unreadable, and policy-omitted.

**Expected behavior:**

- Only CURRENT packets supply declared/detected/result/resolution/confidence and
  packet/catalog/snapshot diagnostics.
- UNKNOWN/CONFLICT/ERROR remains visible and never becomes a phase.
- Missing/non-current stage is UNKNOWN/NOT_SUPPLIED and may make onboarding
  PARTIAL only when stage is relevant.
- No stage.txt/artifact/source-count/engine/ADR inference runs.

**Assertions:**

- [ ] Stage source is exactly `cgs.project-stage-detection/v2`
- [ ] Packet ID, root ID, catalog revision, manifest and current source states validate
- [ ] Detector packet remains diagnostic, not gate/access authority
- [ ] project-stage-detect invocation count is zero

---

### Case 11: Evidence-bound help recommendation is external and matched

Run recommendation variants: CURRENT and matching stage packet; missing; invalid
ID/schema fields; stale evidence; project mismatch; packet/catalog mismatch;
unreadable; policy-omitted; and envelope with omitted same-level conflicts.

**Expected behavior:**

- CURRENT requires recommendation ID, snapshot, stage source/context, matching
  packet/root/manifest/catalog IDs, exactly one action, complete conflict/evidence
  buckets, receipt/run IDs, diagnostics, no-execution markers, and current revisions.
- Non-current variants do not supply project recommendation facts.
- A valid project workflow action may be displayed separately but is never
  executed, treated as assignment, or automatically made onboarding next_action.
- It becomes the onboarding action only if independently non-mutating,
  visibility-allowed, repository-guided, source-current, and instruction-compliant.

**Assertions:**

- [ ] Onboard does not recompute a different project action
- [ ] Packet/catalog mismatches fail closed
- [ ] Hidden same-level conflicts invalidate the envelope
- [ ] help and recommended-workflow invocation counts are zero

---

### Case 12: Ambiguous repository role fails before role-specific reads

**Fixture:** Alias `artist` maps to both technical-artist and art-director.

**Input:** `$onboard artist`

**Expected behavior:** Returns safe candidate IDs, ONBOARDING ERROR, reads no
role-specific area content, does not broaden visibility, and invents no human hierarchy.

---

### Case 13: Optional coverage missing, stale, placeholder, or contradictory

**Fixture:** Root and role identity are valid; active-work pointer is missing;
architecture changes during the run; technology contains CHOOSE placeholders;
two current safe indexes contradict one another.

**Expected behavior:**

- Current work and placeholder technology are UNKNOWN.
- Stale source facts are removed from current prose.
- Contradictions cite stable safe source records.
- Known facts remain DIRECT and cited.
- Status is ONBOARDING PARTIAL with exact affected dimensions.

**Assertions:**

- [ ] Missing/placeholder data is not inferred from file extensions or conventions
- [ ] Mixed snapshots are not presented as current
- [ ] PARTIAL never hides omitted, stale, or contradictory coverage

---

### Case 14: Safe next action is non-mutating and source-supported

**Fixture:** One current visibility-allowed architecture overview is explicitly
recommended by repository guidance and has a complete instruction chain. No task
assignment or project workflow is authorized.

**Expected behavior:** Recommends reading that one verified file with path/revision/
chain, or asking one source-identified artifact owner a bounded question. Does
not recommend implementation, initialization, sprint/design work, or a denied/
stale/unverified file merely because another artifact is absent.

---

### Case 15: Every outcome remains strictly read-only

**Fixture:** READY, PARTIAL, ERROR, invalid invocation, save request, missing
upstream evidence, budget overflow, sensitive candidates, and user request to run
the next action.

**Expected behavior:**

- write, authorization, detector/help/skill invocation, agent spawn, gate,
  recorder, commit, publish, and external-action counts are zero;
- packet says `files_written: none` and `auto_executed: false`;
- at most one orientation action remains text only.

---

## Status decision assertions

- `ONBOARDING ERROR`: root authority/identity invalid; role/area or invocation
  invalid; policy prevents required root/identity coverage.
- `ONBOARDING PARTIAL`: root and identity valid but requested/relevant optional
  coverage is missing, unreadable, stale, contradictory, UNKNOWN,
  OMITTED_BUDGET, or OMITTED_POLICY.
- `ONBOARDING READY`: all requested/relevant bounded coverage is current/direct,
  recommended paths have full chains, and no unresolved UNKNOWN could mislead.
- `ONBOARDING COMPLETE` never appears.

READY grants no access, authority, assignment, approval, or promise of complete
undocumented knowledge.

---

## Protocol Compliance

- [ ] Default, error, partial, and ready paths are read-only
- [ ] Root AGENTS.md gates all secondary context
- [ ] Nested instruction chains precede governed reads/recommendations
- [ ] Enumeration/content/Git collection obeys explicit budgets
- [ ] Visibility and sensitive denial precede stat/open/revision
- [ ] Every DIRECT fact has stable provenance and current snapshot state
- [ ] Repository roles never become human organization
- [ ] Git is explicit-range, privacy-safe, and non-evaluative
- [ ] Canonical stage/help evidence is optional, matched, current, and unexecuted
- [ ] READY/PARTIAL/ERROR are deterministic
- [ ] Output conforms to onboarding_context/v2
- [ ] No director, subagent, gate, detector, help, recorder, write, or downstream workflow runs

---

## Coverage Notes

Fixtures must prove denied sources were never statted/opened/versioned and that
applicable instruction files were read before targets. Absence from final prose
alone is insufficient. Catalog test-result fields remain blank until these cases
are actually executed; authoring this spec is not test evidence.
