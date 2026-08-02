# Skill Test Spec: `$studio-status`

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-18

## Skill Summary

`$studio-status` is a read-only Codex replacement for the unsupported live terminal
status line. It reports the current production stage, active Epic → Feature → Task
breadcrumb, evidence used for inference, and the available recovery file without
installing a status line or modifying project state.

---

## Static Assertions

- [ ] YAML frontmatter contains `name: studio-status` and a non-empty `description`
- [ ] The documented invocation is `$studio-status`
- [ ] Explicitly states that the workflow is read-only
- [ ] Does not install, emulate, or configure a terminal status line
- [ ] Uses `.codex/docs/` and `AGENTS.md` paths only
- [ ] Defines deterministic stage precedence and a stable report format

---

## Director Gate Checks

None. Status reporting is advisory and must not delegate to director subagents or
advance the production stage.

---

## Test Cases

### Case 1: Explicit Stage and Complete Breadcrumb

**Fixture:**
- `production/stage.txt` contains `Production`
- `production/session-state/active.md` contains a valid STATUS block with Epic,
  Feature, and Task values

**Expected behavior:**
1. Use `Production` exactly from the explicit stage file.
2. Read only the marked STATUS block.
3. Report `Epic > Feature > Task` in that order.
4. Name `active.md` as the recovery source.

**Assertions:**
- [ ] Explicit stage takes precedence over inferred evidence
- [ ] Breadcrumb ordering is stable
- [ ] Text outside the STATUS markers is ignored
- [ ] No files are modified

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: No Stage File — infer the most advanced supported stage

**Fixture:**
- No `production/stage.txt`
- A game concept, systems index, configured engine preference, and two ADRs exist
- Fewer than ten recognized source files exist

**Expected behavior:**
1. Inspect all defined evidence rather than stopping at the first match.
2. Infer `Pre-Production`, the most advanced supported stage in the precedence list.
3. Report the ADR evidence used.
4. Omit the active breadcrumb because this is an earlier stage.

**Assertions:**
- [ ] Result is Pre-Production
- [ ] Evidence line identifies the ADRs
- [ ] No unsupported later stage is inferred
- [ ] No files are modified

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Source Threshold — infer Production

**Fixture:**
- No explicit stage file
- Exactly ten recognized source files exist recursively under `src/`
- Other stage evidence is absent

**Expected behavior:**
1. Count only the documented source extensions.
2. Infer `Production` at the inclusive threshold of ten.
3. Check `active.md` for an optional breadcrumb.

**Assertions:**
- [ ] Exactly ten recognized files satisfy the threshold
- [ ] Unrecognized extensions do not affect the count
- [ ] Missing active state is reported as `none recorded`, not as an error
- [ ] No files are modified

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Malformed or Contradictory State

**Fixture:**
- `production/stage.txt` contains `Launch Candidate`, which is not a documented stage
- `active.md` has an opening STATUS marker but no closing marker
- Source evidence otherwise suggests Production

**Expected behavior:**
1. Preserve and display the explicit value without silently normalizing it.
2. Warn that the stage is unrecognized and that evidence is contradictory.
3. Warn that the STATUS markers are malformed and do not extract an unbounded block.
4. Do not repair either file.

**Assertions:**
- [ ] Both anomalies are reported
- [ ] The explicit stage value remains visible
- [ ] No breadcrumb is fabricated
- [ ] No repair or write occurs

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Empty Project — stable Concept fallback

**Fixture:**
- No explicit stage, design artifacts, engine selection, ADRs, source files, or active state

**Expected behavior:**
1. Treat every missing optional path as absent evidence rather than an exception.
2. Report `Concept` with `Focus: none recorded` and `Recovery: none`.
3. Avoid subagent delegation and all writes.

**Assertions:**
- [ ] Empty workspaces produce Concept deterministically
- [ ] Output includes all four fields: Stage, Focus, Evidence, Recovery
- [ ] No director gate or subagent is invoked
- [ ] No file or terminal configuration is created

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Remains read-only in every branch
- [ ] Uses exact project evidence and calls out uncertainty
- [ ] Does not claim to be a continuously updating status line
- [ ] Returns a compact report without requiring user interaction
- [ ] Inference evidence is collected even when a non-empty explicit stage exists
- [ ] Inference can warn but never replaces the explicit Stage field
- [ ] active.md marker pairing is validated for every stage, including unrecognized values
- [ ] Breadcrumb fields are extracted only from a valid bounded block for Production/Polish/Release

---

## Coverage Notes

Later stages such as Polish and Release are reachable only from an explicit stage
file and are covered by the same precedence rule as Case 1. The coverage audit
must locate this spec recursively and compare it with the actual
`.agents/skills/studio-status/SKILL.md` file.
