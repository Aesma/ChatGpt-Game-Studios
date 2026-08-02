# [Prototype Name] — Concept Document

---
**Status**: Reverse-Documented from Prototype
**Prototype Path**: `prototypes/[name]/`
**Date**: [YYYY-MM-DD]
**Creator**: [Explicitly provided name or "unknown — not recorded"]
**Outcome**: [Evidence-backed outcome or "N/A — source unavailable"]
---

> **⚠️ Reverse-Documentation Notice**
>
> This concept document was created **after** the prototype was built. It captures
> the core mechanic, learnings, and design insights discovered through prototyping.
> This is a formalization of experimental work, not a pre-planned design.

---

## Evidence Boundaries

- **Observed implementation:** Record only behavior, structure, and constraints directly evidenced by source code, assets, configuration, build output, or test results.
- **User-stated intent:** Label goals or intended behavior supplied by the user separately; intent is not evidence that a feature is implemented.
- **Gap:** Mark missing, contradictory, or unverified behavior explicitly instead of inferring it.
- **Prototype evidence:** Outcome, effort/duration, reuse percentages, tester counts, feedback, and quotes require an existing record or explicit user input. Otherwise write `N/A — source unavailable` and do not estimate.

Acceptance criteria may be marked implemented or passing only when supported by code, build, or test evidence.

---

## 1. Prototype Overview

**Original Hypothesis**:
[Existing record/user statement, or N/A — source unavailable]

**Approach**:
[Observed implementation approach]

**Duration**:
- Time spent: [Existing record/user value, or N/A — source unavailable]
- Complexity: [Evidence-backed assessment, or N/A — source unavailable]

**Outcome**:
- **Validated**: [Evidence-backed result, or N/A]
- **Needs Work**: [Evidence-backed result, or N/A]
- **Invalidated**: [Evidence-backed result, or N/A]

---

## 2. Core Mechanic

**What the Prototype Does**:
[Observed mechanic/system]

**How It Feels**:
- [Existing playtest/user feedback with source, or N/A — source unavailable]

**Player Fantasy**:
[User-stated intent or N/A — not supplied]

**Core Loop** (if evidenced):
```
[Action 1] → [Result 1] → [Action 2] → [Result 2]
```

**Emergent Behaviors**:
- [Observed/test-record behavior, or N/A]

---

## 3. What Worked

### Mechanic Successes

**[Success 1]**: [Evidence-backed result or N/A]
- **Why**: [Existing evidence/user reflection or unknown]
- **Keep for Production**: [Explicit decision or Not decided]

### Technical Successes

**[Technical win 1]**: [Observed result]
- **Lesson**: [User reflection/evidence or unknown]
- **Reusable**: [Measured/confirmed value or Not assessed]

---

## 4. What Didn't Work

### Mechanic Failures

**[Failure 1]**: [Evidence-backed result or N/A]
- **Why**: [Existing analysis/user reflection or unknown]
- **Could It Be Fixed**: [Explicit assessment or Not assessed]

### Technical Failures

**[Technical issue 1]**: [Observed issue or N/A]
- **Lesson**: [Existing/user-provided lesson or unknown]

---

## 5. What Needs Refinement

**[Element 1]**: [Evidence-backed gap]
- **Issue**: [Observed problem]
- **Path Forward**: [User-stated intent or Not decided]
- **Effort**: [Existing estimate/user input or N/A — source unavailable]

---

## 6. Key Learnings

### Design Insights

**[Insight 1]**: [Existing record/user reflection or N/A]
- **Implication**: [Confirmed implication or Not decided]

### Technical Insights

**[Insight 2]**: [Evidence-backed insight]
- **Implication**: [Confirmed implication or Not decided]

### Player Psychology Insights

**[Insight 3]**: [Playtest evidence/user reflection or N/A]
- **Implication**: [Confirmed implication or Not decided]

---

## 7. Production Readiness Assessment

**Should This Become a Full Feature?**: [Explicit decision or Not decided]

**If Yes — Production Requirements**:
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

**Estimated Production Effort**: [Existing estimate/user input or N/A — source unavailable]
- Prototype reusability: [Measured/confirmed percentage or N/A — source unavailable]
- From-scratch effort: [Existing estimate/user input or N/A — source unavailable]

**If No — Why Not?**:
- [Explicit reason or N/A]

**If Pivot — Suggested Direction**:
- [Explicit/user-provided direction or Not decided]

---

## 8. Design Pillars Alignment

| Pillar | Alignment | Notes |
|--------|-----------|-------|
| [Existing pillar] | [Evidence/user assessment or Not assessed] | [Source] |

**Overall Pillar Fit**: [Explicit assessment or Not assessed]

---

## 9. Next Steps

### Immediate (If Moving Forward)
1. **[Task 1]**: [description]
2. **[Task 2]**: [description]

### Before Production (If Needs More Work)
1. **[Task 1]**: [description]
2. **[Task 2]**: [description]

### If Abandoning
1. **[Task 1]**: [description]
2. **[Task 2]**: [description]

---

## 10. Technical Notes

**Prototype Implementation**:
- Language/Engine: [Observed]
- Architecture: [Observed]
- Shortcuts taken: [Observed or unknown]

**Reusable Code**:
- `[file/path 1]`: [Observed function; reusability Not assessed unless evidenced]

**Technical Debt**:
- [Observed debt]

---

## 11. Playtest Feedback

Populate this section only from an existing playtest/session record or explicit
user-provided feedback. Cite the source. If neither exists, write:

`N/A — no playtest record or user-provided feedback available.`

**Testers**: [Recorded count/type or N/A — source unavailable]

**Positive Feedback**:
- [Exact existing quote within applicable quotation limits + source, or N/A]

**Negative Feedback**:
- [Exact existing quote within applicable quotation limits + source, or N/A]

**Suggestions**:
- [Recorded suggestion + source, or N/A]

**Themes**:
- [Evidence-backed repeated theme, or N/A]

Never synthesize a quote, tester identity, tester count, or consensus theme.

---

## 12. Related Work

**Inspired By**:
- [User-provided/existing record, or N/A]

**Differs From**:
- [Evidence/user-provided difference, or N/A]

**Integrates With**:
- [Observed or intended system connection, labeled]

---

## 13. Open Questions

**Design Questions**:
1. [Undecided design question]
2. [Question requiring playtest/iteration]

**Technical Questions**:
3. [Technical unknown]
4. [Feasibility question]

---

## 14. Appendix: Prototype Assets

**Code**:
- Location: `prototypes/[name]/src/`
- Status: [Observed status or Not assessed]

**Art/Audio**:
- Location: `prototypes/[name]/assets/`
- Status: [Observed status or Not assessed]

**Documentation**:
- README: [Exists | Missing]
- Build instructions: [Exists | Missing]

---

## Version History

| Date | Author | Changes |
|------|--------|---------|
| [Date] | Codex (reverse-doc) | Initial concept doc from prototype analysis |
| [Date] | [Explicit author or unknown] | Clarified outcomes or added sourced playtest feedback |

---

**Final Recommendation**: [Explicit evidence-backed GO/NO-GO/PIVOT decision or Not decided]

**Rationale**: [Existing evidence/user rationale or N/A — source unavailable]

---

*This concept document was generated by `$reverse-document concept prototypes/[name]`*
