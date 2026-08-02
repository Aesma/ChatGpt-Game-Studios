# Skill Test Spec: $team-live-ops

## Skill Summary

Orchestrates the live-ops team through a 7-phase planning pipeline to produce a
season or event plan. Coordinates live-ops-designer, economy-designer,
analytics-engineer, community-manager, narrative-director, and writer. Phases 3
and 4 (economy design and analytics) run simultaneously. Ends with a consolidated
season plan requiring user approval before handoff to production.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
10. Verdict: COMPLETE — season plan produced and handed off for production

**Assertions:**
- [ ] All 7 phases execute in order; Phase 3 and 4 are issued as parallel Codex subagent delegations
- [ ] Phase 7 consolidated summary includes all six sections (season brief, narrative framing, economy design, analytics plan, content inventory, communication calendar)
- [ ] Ethics review section in Phase 7 explicitly references `design/live-ops/ethics-policy.md`
- [ ] Three output documents written to `design/live-ops/seasons/` with correct naming convention
- [ ] File writes are delegated to sub-agents — orchestrator does not write directly
- [ ] Verdict: COMPLETE appears in final output
- [ ] Next steps reference `$sprint-plan` and `$team-release` and do not call the system-GDD-only `$design-review`
- [ ] Arguments expose no `--review`; all six core roles always run
- [ ] Phases 1–6 are analysis-only and write no output documents

---

### Case 2: Ethics Violation Found — Reward element violates ethics policy

**Fixture:**
- All standard live-ops fixtures present (economy-rules.md, ethics-policy.md)
- `design/live-ops/ethics-policy.md` explicitly prohibits loot boxes targeting players under 18
- economy-designer (Phase 3) proposes a "Mystery Chest" mechanic with randomized premium rewards and no pity timer

**Input:** `$team-live-ops "Season 3: Shadow Tournament"`

**Expected behavior:**
1. Phases 1–4 proceed normally; economy-designer proposes Mystery Chest mechanic
2. Phase 7: Orchestrator reviews Phase 3 output against ethics policy; identifies Mystery Chest as a violation of the "no untransparent random premium rewards" rule in the ethics policy
3. Ethics review section of the Phase 7 summary flags the violation explicitly: "ETHICS FLAG: Mystery Chest mechanic in Phase 3 economy design violates [policy rule]. Approval is blocked until this is resolved."
4. user-input request presented with resolution options before season plan approval is offered
5. Skill does NOT issue COMPLETE or write output documents until a revision clears the ethics violation

**Assertions:**
- [ ] Phase 7 ethics review section explicitly names the violating element and the policy rule it breaks
- [ ] Skill does not auto-approve the season plan when an ethics violation is present
- [ ] user-input request offers only revise economy design or cancel
- [ ] Output documents are NOT written while the violation is unresolved
- [ ] If user chooses to revise: skill re-spawns economy-designer to produce a corrected design before returning to Phase 7 review
- [ ] Verdict: COMPLETE is only issued after the ethics flag is cleared
- [ ] An explicit policy violation cannot be overridden or waived

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$team-live-ops` (no argument)

**Expected behavior:**
1. Phase 1: No argument detected
2. Outputs: "Usage: `$team-live-ops [season name or event description]` — Provide the name or description of the season or live event to plan."
3. Skill exits immediately without spawning any subagents

**Assertions:**
- [ ] Skill does NOT guess a season name or fabricate a scope
- [ ] Error message includes the correct usage format documented in the skill body
- [ ] No Codex subagent delegations are issued before the argument check fails
- [ ] No files are read or written

---

### Case 4: Parallel Phase Validation — Phases 3 and 4 run simultaneously

**Fixture:**
- All standard live-ops fixtures present
- Phase 1 (season brief) and Phase 2 (narrative framing) already approved
- Phase 3 (economy-designer) and Phase 4 (analytics-engineer) inputs are independent of each other

**Input:** `$team-live-ops "Season 1: The First Thaw"` (observed at Phase 3/4 transition)

**Expected behavior:**
1. After Phase 2 is approved by the user, the orchestrator issues both Codex subagent delegations (economy-designer and analytics-engineer) before awaiting either result
2. Both agents receive the season brief as context; analytics-engineer does NOT wait for economy-designer output to begin
3. Economy-designer output and analytics-engineer output are collected together before Phase 5 begins
4. If one of the two parallel agents blocks, the other continues; a partial result is reported

**Assertions:**
- [ ] Both Codex subagent delegations for Phase 3 and Phase 4 are issued before either result is awaited — they are not sequential
- [ ] Analytics-engineer prompt does NOT include economy-designer output as a required input (the inputs are independent)
- [ ] If economy-designer blocks but analytics-engineer succeeds, analytics output is preserved and the block is surfaced via user-input request
- [ ] Phase 5 does not begin until BOTH Phase 3 and Phase 4 results are collected
- [ ] Skill documentation explicitly states "Phases 3 and 4 can run simultaneously"

---

### Case 5: Missing Ethics Policy — `design/live-ops/ethics-policy.md` does not exist

**Fixture:**
- `design/live-ops/economy-rules.md` exists
- `design/live-ops/ethics-policy.md` does NOT exist
- All other fixtures are present

**Input:** `$team-live-ops "Season 4: Desert Heat"`

**Expected behavior:**
1. Phases 1–4 proceed; economy-designer and analytics-engineer are given the ethics policy path but it is absent
2. Phase 7: Orchestrator attempts to run ethics review; detects that `design/live-ops/ethics-policy.md` is missing
3. Phase 7 summary includes a gap flag: "ETHICS REVIEW SKIPPED: `design/live-ops/ethics-policy.md` not found. Economy design was not reviewed against an ethics policy. Recommend creating one before production begins."
4. Skill still completes the season plan and reaches COMPLETE verdict, but the gap is prominently flagged in the output and in the season design document
5. Next steps include a recommendation to create the ethics policy document

**Assertions:**
- [ ] Skill does NOT error out when the ethics policy file is missing
- [ ] Skill does NOT fabricate ethics policy rules in the absence of the file
- [ ] Phase 7 summary explicitly notes that ethics review was skipped and why
- [ ] Verdict: COMPLETE is still reachable despite the missing file
- [ ] Gap flag appears in the season design output document (not just in conversation)
- [ ] Next steps recommend creating `design/live-ops/ethics-policy.md`

---

## Protocol Compliance

- [ ] User decisions occur at Phase 1 scope, Phase 3 economy/rewards, and Phase 7 consolidated approval; routine transitions do not re-prompt
- [ ] Phases 3 and 4 are always spawned in parallel, not sequentially
- [ ] File Write Protocol: orchestrator never calls file edits directly — all writes are delegated to sub-agents
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Ethics review in Phase 7 always references the ethics policy file path explicitly
- [ ] Error recovery: any BLOCKED agent is surfaced immediately with user-input request options (skip / retry / stop)
- [ ] Partial reports are produced if any phase blocks — work is never discarded
- [ ] Verdict: COMPLETE only after user approves the consolidated season plan; BLOCKED if any unresolved ethics violation exists
- [ ] Next steps include `$sprint-plan` and `$team-release`; no incompatible `$design-review` call appears
- [ ] Phase 7 ethics clearance happens before the only changeset authorization and all writes
- [ ] Unresolved policy violation means BLOCKED and zero output files
- [ ] Season number comes from explicit `Season N` or max existing valid N + 1
- [ ] Name is normalized to a safe slug and collisions never overwrite silently
- [ ] live-ops-designer, analytics-engineer, and community-manager each own one exact output path

---

### Case 6: Output identity and ownership are deterministic

**Fixture:** existing S01/S02 files; input does not contain an explicit season number.

**Assertions:**
- [ ] Proposed number is 3 and is shown before approval
- [ ] Unsafe name punctuation is normalized to a safe lowercase hyphenated slug
- [ ] Existing target collision stops or requires explicit update intent; no silent overwrite
- [ ] The final changeset lists exactly the season, analytics, and comms paths
- [ ] live-ops-designer writes season only, analytics-engineer analytics only, community-manager comms only

### Case 7: No early writes before ethics review

**Assertions:**
- [ ] Phase 1–6 agents return content in conversation only
- [ ] No output document exists before Phase 7 ethics clearance and final approval
- [ ] A violation followed by cancel yields BLOCKED and zero written files
- [ ] A revision must pass the same ethics check before the changeset can be authorized

### Case 8: Economy and analytics parallel drafts reconcile

**Assertions:**
- [ ] Phases 3 and 4 always launch together after Phase 2, never parallel with Phase 2
- [ ] After reward choice, analytics is checked against every final reward, price, currency, cadence, and random/pity event
- [ ] Missing instrumentation is an unresolved analytics gap

### Case 9: Missing policy/rules do not manufacture conclusions

**Assertions:**
- [ ] Missing economy-rules offers stop or a non-pricing provisional outline
- [ ] Provisional output never claims economy health was checked
- [ ] Missing ethics policy says not reviewed for economy and communications, not fair/non-predatory
- [ ] Production is called blocked only when an existing project rule says so
- [ ] Existing policy review includes urgency/FOMO communication copy

### Case 10: Required outputs and approvals remain distinct

**Assertions:**
- [ ] Phase 5 approved content/copy is included in the season document, with no fourth file
- [ ] Skipped/unresolved required season/economy/analytics/content/comms work yields partial BLOCKED and zero formal writes
- [ ] Product/content approval occurs before and is distinct from changeset authorization
- [ ] Existing matching documents are read and previewed as updates; a different-season collision stops

---

## Coverage Notes

- Phase 5 parallel spawning (narrative-director + writer) follows the same pattern as Phases 3/4 but is not separately tested here — it uses the same parallel Task protocol validated in Case 4.
- The "economy-rules.md absent" edge case is not separately tested — it would surface as a BLOCKED result from economy-designer and follow the standard error recovery path tested implicitly in Case 4.
- The full content writing pipeline (Phase 5 output validation) is validated implicitly by the Case 1 happy path consolidated summary check.
- Community manager communication calendar format (pre-launch, launch day, mid-season, final week) is validated implicitly by Case 1; no separate edge case is needed.
