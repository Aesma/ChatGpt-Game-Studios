# Skill Test Spec: $balance-check

## Skill Summary

`$balance-check` reads balance data files (JSON or YAML in `assets/data/`) and
checks each value against the design formulas defined in GDDs under `design/gdd/`.
It produces a findings table with columns: Value → Formula → Deviation → Severity.
No director gates are invoked (read-only analysis). The skill may optionally write
a balance report but asks "May I apply the proposed changeset?"
7. If user says no: skill ends without writing

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Findings table is presented without writing anything automatically
- [ ] Optional report write is offered but not forced
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

## Protocol Compliance

- [ ] Reads both balance data files and GDD formulas before analysis
- [ ] Findings table shows Value, Formula, Deviation, and Severity columns
- [ ] Does not write any files without explicit user approval
- [ ] No director gates are invoked
- [ ] Verdict is one of: BALANCED, CONCERNS, OUT OF BALANCE
- [ ] BALANCED requires all applicable checks to be evaluated with no material deviation
- [ ] CONCERNS covers non-blocking deviations or unevaluated items; OUT OF BALANCE requires a cited critical deviation or degenerate strategy
- [ ] Fix mode previews every exact file, current value, proposed value, and edit before one authorization
- [ ] Fix mode never changes a newly discovered file outside the authorized changeset

---

## Coverage Notes

- The case where `assets/data/` is entirely empty is not tested; behavior
  follows the CONCERNS pattern with a message that no data files were found.
- Tolerance thresholds (±10%, ±20%) are implementation details of the skill;
  the tests verify that deviations are detected and classified, not the
  exact threshold values.
