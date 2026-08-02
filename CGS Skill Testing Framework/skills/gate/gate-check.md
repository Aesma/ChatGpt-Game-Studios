# Skill Test Spec: $gate-check

## Skill Summary

`$gate-check` validates exactly one transition selected by a canonical
source-phase token, verifies it matches the current stage, and deterministically
aggregates Required, Recommended, quality, manual, and director evidence. Only
PASS or explicitly accepted non-blocking CONCERNS may advance
`production/stage.txt`; FAIL cannot be overridden into advancement.

---

## Static Assertions

- [ ] Canonical tokens are exactly concept, systems-design, technical-setup, pre-production, production, and polish
- [ ] Explicit invocations verify current stage before checks or writes
- [ ] PASS/CONCERNS/FAIL aggregation is deterministic
- [ ] Required lists contain only blocking items
- [ ] Concept gate does not call system-only `$design-review`
- [ ] FAIL/NOT READY/REJECT cannot write the next stage

---

## Test Cases

### Case 1: Six source-phase mappings

**Assertions:**
- [ ] `concept` maps only Concept to Systems Design
- [ ] `systems-design` maps only Systems Design to Technical Setup
- [ ] `technical-setup` maps only Technical Setup to Pre-Production
- [ ] `pre-production` maps only Pre-Production to Production
- [ ] `production` maps only Production to Polish
- [ ] `polish` maps only Polish to Release
- [ ] Unknown or target-phase-style aliases are rejected rather than inferred

---

### Case 2: Requested source does not match current stage

**Assertions:**
- [ ] Current-stage and requested-source evidence are both shown
- [ ] The gate checklist is not run
- [ ] `production/stage.txt` is not written or moved backward/forward
- [ ] No mismatch override path is offered

---

### Case 3: Deterministic verdict and manual evidence

**Assertions:**
- [ ] Any blocking Required absence, auto-FAIL, or NOT READY/REJECT produces FAIL
- [ ] With no blocker, missing Recommended or confirmed non-blocking quality concern produces CONCERNS
- [ ] PASS requires all blocking/quality checks and no unanswered blocking manual item
- [ ] An unanswered blocking manual question never defaults to PASS

---

### Case 4: Gate-specific P0 contracts

**Assertions:**
- [ ] Pre-Production vertical slice/inventory/playtest recommendations are not counted as Required
- [ ] Production QA plan appears once as Recommended while QA sign-off remains Required
- [ ] Concept quality is checked directly from concept content without invoking `$design-review`
- [ ] Systems Design requires substantive eight-section MVP GDD content plus systems-index status Approved
- [ ] No nonexistent individual design-review report is required as evidence

---

### Case 5: Director panel and advancement

**Assertions:**
- [ ] Full/lean run the existing four phase-gate directors in parallel; solo records skips and still runs artifact/quality checks
- [ ] Any NOT READY result makes the overall verdict FAIL
- [ ] FAIL may be acknowledged only while staying in the current stage
- [ ] CONCERNS may advance only after explicit acceptance and one stage-file changeset authorization
- [ ] PASS advances only after explicit confirmation and authorization

---

### Case 6: Detection, freshness, tests, and applicability

**Assertions:**
- [ ] Missing/invalid stage uses existing artifact heuristics; conflicting signals require confirmation
- [ ] Report scope/date/build/system linkage must cover the current gate
- [ ] Missing configured test command is MANUAL/CONCERNS; an actual failed run is FAIL
- [ ] Polish-to-Release N/A requires platform/language/store evidence and is not counted missing/passing
- [ ] Vertical Slice artifact and quality are counted once

---

### Case 7: Partial panel and manual challenge timing

**Assertions:**
- [ ] Failed/timed-out director is named and never fabricated as READY
- [ ] A required incomplete panel cannot PASS
- [ ] Chain challenge reuses collected manual answers
- [ ] A newly discovered blocking manual question is asked before final verdict; unanswered cannot PASS

---

## Protocol Compliance

- [ ] Complete checklist evidence precedes the verdict
- [ ] Six source tokens and current-stage validation prevent cross-level writes
- [ ] Stage changes are one bounded authorized edit
- [ ] Failure never manufactures or advances artifacts
