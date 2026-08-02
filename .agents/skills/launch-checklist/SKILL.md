---
name: launch-checklist
description: "Complete launch readiness validation covering every department: code, content, store, marketing, community, infrastructure, legal, and go/no-go sign-offs."
---

## Invocation and execution

Invoke this workflow as `$launch-checklist`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[launch-date or 'dry-run']`. Treat bracketed values as optional unless the workflow says otherwise.


> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$launch-checklist`. Do not auto-invoke based on context matching.

## Phase 1: Parse Arguments

Require exactly one argument: `dry-run` or a valid explicit calendar date in `YYYY-MM-DD`. If missing, ask for it. Reject invalid dates and dates earlier than today, report the reason, and stop without guessing or writing.

Dry-run generates the full evidence-annotated preview and canonical verdict but creates no sign-off, never requests changeset authorization, and skips Phase 5 writing. Its output must say `not persisted — not valid sign-off evidence`.

---

## Phase 2: Gather Project Context

- Read `AGENTS.md` and existing engine/build configuration for tech stack, target platforms, and team structure
- Resolve configured target platforms and whether online/multiplayer capability is enabled. Evaluate only applicable checkbox items. Append `not applicable because ...` or `manual confirmation required — configuration undecided` on the existing checkbox line or in existing ordinary explanatory areas; add no applicability field or column
- Read the latest milestone in `production/milestones/`
- Read the most recent earlier-dated launch checklist matching `production/launch/launch-checklist-[date].md`, if one exists
- Read any existing release checklist in `production/releases/`
- Read the content calendar in `design/live-ops/content-calendar.md` if it exists
- Read already-existing build, test, performance, bug, security, localization, certification, legal, store, infrastructure, operations, and community artifacts that directly correspond to checklist sections

A missing repository artifact proves only that repository evidence is unavailable; it does not prove completion or failure of an external fact. Keep such items for human confirmation.

---

## Phase 3: Scan Codebase Health

- Count `TODO`, `FIXME`, `HACK` comments only in production source and build configuration. Exclude documentation, test fixtures, templates, generated/vendor files, and the checklist itself; list the matched paths and accept exceptions only from existing documentation
- Check for any `console.log`, `print()`, or debug output left in production code
- Check for placeholder assets (search for `placeholder`, `temp_`, `WIP_`)
- Check for hardcoded test/dev values (localhost, suspected credentials, debug flags), but report only the file path and safe category such as `suspected development value/credential`. Never copy a credential or secret value into the conversation or checklist

---

## Phase 4: Generate the Launch Checklist

Preserve the checklist structure below. Mark compiler warnings, tests, leak/soak status, and similar execution claims only from checks executed in this run or a recent existing evidence artifact that directly records the result. An absent/empty file is not a pass; append `manual confirmation required` or use existing Conditional Items when no evidence exists.

For each existing checkbox, append only a short ordinary-text note such as `— evidenced by [existing path]`, `— manual confirmation required`, or `— not applicable because [reason]`. Do not add fields, columns, tables, or sections. If a claim cannot be represented accurately in the existing checkbox text, ordinary explanations, Blocking Items, or Conditional Items, remove the unsupported claim. Never check an item solely because no contrary evidence was found.

```markdown
# Launch Checklist: [Game Title]
Target Launch: [Date or DRY RUN]
Generated: [Date]

---

## 1. Code Readiness

### Build Health
- [ ] Clean build on all target platforms
- [ ] Zero compiler warnings
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Performance benchmarks within targets
- [ ] No memory leaks (verified via extended soak test)
- [ ] Build size within platform limits
- [ ] Build version correctly set and tagged in source control

### Code Quality
- [ ] TODO count: [N] (zero required for launch, or documented exceptions)
- [ ] FIXME count: [N] (zero required)
- [ ] HACK count: [N] (each must have documented justification)
- [ ] No debug output in production code
- [ ] No hardcoded dev/test values
- [ ] All feature flags set to production values
- [ ] Error handling covers all critical paths
- [ ] Crash reporting integrated and verified

### Security
- [ ] No exposed API keys or credentials in source
- [ ] Save data encrypted
- [ ] Network communication secured (TLS/DTLS)
- [ ] Anti-cheat measures active (if multiplayer)
- [ ] Input validation on all server endpoints (if multiplayer)
- [ ] Privacy policy compliance verified

---

## 2. Content Readiness

### Assets
- [ ] All placeholder art replaced with final assets
- [ ] All placeholder audio replaced with final audio
- [ ] Audio mix finalized and approved by audio director
- [ ] All VFX polished and performance-verified
- [ ] No missing or broken asset references
- [ ] Asset naming conventions enforced

### Text and Localization
- [ ] All player-facing text proofread
- [ ] No hardcoded strings (all externalized for localization)
- [ ] All supported languages translated and verified
- [ ] Text fits UI in all languages (text fitting pass complete)
- [ ] Font coverage verified for all supported languages
- [ ] Credits complete, accurate, and up to date

### Game Content
- [ ] All levels/maps playable from start to finish
- [ ] Tutorial flow complete and tested with new players
- [ ] All achievements/trophies implemented and tested
- [ ] Save/load works correctly for all game states
- [ ] Difficulty settings balanced and tested
- [ ] End-game/credits sequence complete

---

## 3. Quality Assurance

### Testing
- [ ] Full regression test suite passed
- [ ] Zero S1 (Critical) bugs open
- [ ] Zero S2 (Major) bugs open (or documented exceptions)
- [ ] Soak test passed (8+ hours continuous play)
- [ ] Multiplayer stress test passed (if applicable)
- [ ] All critical user paths tested on every platform
- [ ] Edge cases tested (full storage, no network, suspend/resume)

### Platform Certification
- [ ] PC: Steam/Epic/GOG SDK requirements met
- [ ] Console: TRC/TCR/Lotcheck submission prepared
- [ ] Mobile: App Store/Play Store guidelines compliant
- [ ] Accessibility: minimum standards met (remapping, text scaling, colorblind)
- [ ] Age ratings obtained (ESRB, PEGI, regional)

### Performance
- [ ] Target FPS met on minimum spec hardware
- [ ] Load times within budget on all platforms
- [ ] Memory usage within budget on all platforms
- [ ] Network bandwidth within targets (if multiplayer)
- [ ] No frame hitches in critical gameplay moments

---

## 4. Store and Distribution

### Store Pages
- [ ] Store page copy finalized and proofread
- [ ] Screenshots current and per-platform resolution
- [ ] Trailers current and approved
- [ ] Key art and capsule images finalized
- [ ] System requirements accurate (PC)
- [ ] Pricing configured for all regions
- [ ] Pre-purchase/wishlist campaigns active (if applicable)

### Legal
- [ ] EULA finalized and approved by legal
- [ ] Privacy policy published and linked
- [ ] Third-party license attributions complete
- [ ] Music/audio licensing verified
- [ ] Trademark/IP clearance confirmed
- [ ] GDPR/CCPA compliance verified (data collection, consent, deletion)

---

## 5. Infrastructure

### Servers (if multiplayer/online)
- [ ] Production servers provisioned and load-tested
- [ ] Auto-scaling configured and tested
- [ ] Database backups configured
- [ ] CDN configured for content delivery
- [ ] DDoS protection active
- [ ] Monitoring and alerting configured

### Analytics and Monitoring
- [ ] Analytics pipeline verified and receiving data
- [ ] Crash reporting active and dashboard accessible
- [ ] Server monitoring dashboards live
- [ ] Key metrics tracked: DAU, session length, retention, crashes
- [ ] Alerts configured for critical thresholds

---

## 6. Community and Marketing

### Community Readiness
- [ ] Community guidelines published
- [ ] Moderation team briefed and tools ready
- [ ] Discord/forum/social channels set up
- [ ] FAQ and known issues page prepared
- [ ] Support email/ticketing system active

### Marketing
- [ ] Launch trailer published
- [ ] Press/influencer review keys distributed
- [ ] Social media launch posts scheduled
- [ ] Launch day blog post/dev update drafted
- [ ] Patch notes for launch version published

---

## 7. Operations

### Team Readiness
- [ ] On-call schedule set for first 72 hours post-launch
- [ ] Incident response playbook reviewed by team
- [ ] Rollback plan documented and tested
- [ ] Hotfix pipeline tested (can ship emergency fix within 4 hours)
- [ ] Communication plan for launch issues (who posts, where, how fast)

### Day-One Plan
- [ ] Day-one patch prepared (if needed)
- [ ] Server unlock/go-live procedure documented
- [ ] Launch monitoring dashboard bookmarked by all leads
- [ ] War room/channel established for launch day

---

## Go / No-Go Decision

**Overall Status**: [LAUNCH READY / LAUNCH BLOCKED / CONCERNS]

### Blocking Items
[List any items that must be resolved before launch]

### Conditional Items
[List items that have documented workarounds or accepted risk]

### Sign-Offs Required
- [ ] Creative Director — Content and experience quality
- [ ] Technical Director — Technical health and stability
- [ ] QA Lead — Quality and test coverage
- [ ] Producer — Schedule and overall readiness
- [ ] Release Manager — Build and deployment readiness
```

---

## Phase 5: Save Checklist

Compare the current result with the most recent earlier-dated file of the same kind, item by item, and summarize resolved, still-open, and newly identified issues without introducing a new history format.

Map the final result deterministically:
- Any incomplete required platform certification, required legal document, open S1, or hard failure of a target-platform build is **LAUNCH BLOCKED**.
- With no hard blocker, any unresolved manual confirmation or conditional item is **CONCERNS**.
- Only when every applicable item has evidence and no open issue remains is the result **LAUNCH READY**.

Use the same canonical value in Overall Status and the terminal verdict. Present the completed checklist and summary to the user (total items, blocking items count, conditional items count, departments with incomplete sections).

If in dry-run mode, stop after presenting the preview/verdict and the `not persisted — not valid sign-off evidence` warning. Do not preview a write, ask for authorization, or hand the result off as sign-off.

If not in dry-run mode, use the single path `production/launch/launch-checklist-[date].md`. If that date already exists, preview it as an update rather than silently overwriting it. Add that exact file to the complete changeset preview; do not write it until authorized. Once authorized, write it and report the same canonical verdict.

---

## Phase 6: Next Steps

For a successfully persisted non-dry-run report, output the exact `production/launch/launch-checklist-[date].md` path, its canonical verdict, and summaries from the existing Blocking Items and Conditional Items. A dry-run has no qualifying handoff.

- Pass that exact persisted path and verdict to `$gate-check` for a formal launch assessment.
- Pass that exact persisted path and verdict to `$team-release`; only persisted **LAUNCH READY** can serve as sign-off. **CONCERNS** remains NO-GO until issues are resolved and a new persisted report says LAUNCH READY; **LAUNCH BLOCKED** stops immediately.
