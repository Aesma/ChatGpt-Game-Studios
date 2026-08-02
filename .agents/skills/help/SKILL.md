---
name: help
description: "Analyzes what is done and the users query and offers advice on what to do next. Use if user says what should I do next or what do I do now or I'm stuck or I don't know what to do"
---

## Invocation and execution

Invoke this workflow as `$help`.

Arguments: `[optional: what you just finished, e.g. 'finished design-review' or 'stuck on ADRs']`. Treat bracketed values as optional unless the workflow says otherwise.

Before starting, gather this read-only project context without assuming a shell:

1. Read the first non-empty line of `production/stage.txt`, or use `not set` when absent.
2. Find the most recently modified Markdown file under `production/sprints/`, or use `none`.
3. Read the first five lines of `production/session-state/active.md`, or use `none`.


# Studio Help — What Do I Do Next?

This skill is read-only — it reports findings but writes no files.

This skill figures out exactly where you are in the game development pipeline and
tells you what comes next. It is **lightweight** — not a full audit. For a full
gap analysis, use `$project-stage-detect`.

---

## Step 1: Read the Catalog

Read `.codex/docs/workflow-catalog.yaml`. This is the authoritative list of all
phases, their steps (in order), whether each step is required or optional, and
the artifact globs that indicate completion.

---

## Step 1b: Find Skills Not in the Catalog

Only when the user supplied a help topic, or when the catalog has no relevant
match, find `.agents/skills/*/SKILL.md` and read frontmatter only. Do not scan
every skill on an ordinary catalog-driven "what next?" request.

Compare against the `command:` values in the catalog. Any skill whose name does
not appear as a catalog command is an **uncataloged skill** — still usable but not
part of the phase-gated workflow.

Collect these for the output in Step 7 — show them as a footer block:

```
### Also installed (not in workflow)
- `$skill-name` — [description from SKILL.md frontmatter]
- `$skill-name` — [description]
```

Only show this block if at least one uncataloged skill exists. Limit to the 10
most relevant based on the user's current phase (QA skills in production, team
skills in production/polish, etc.).

---

## Step 2: Determine Current Phase

Check in this order:

1. **Read `production/stage.txt`** — trim its first non-empty line and accept
   it as authoritative only when it is one of the seven existing values below.
   If the file is empty or contains another value, show a warning and continue
   to artifact inference instead of using an undefined phase key. Map valid
   values to:
   - "Concept" → `concept`
   - "Systems Design" → `systems-design`
   - "Technical Setup" → `technical-setup`
   - "Pre-Production" → `pre-production`
   - "Production" → `production`
   - "Polish" → `polish`
   - "Release" → `release`

2. **If stage.txt is missing**, infer phase from artifacts (most-advanced match wins):
   - `src/` has 10+ source files → `production`
   - real story files matching `production/epics/**/story-*.md` exist (exclude
     `EPIC.md` and any index) → `pre-production`
   - `docs/architecture/adr-*.md` exists → `technical-setup`
   - `design/gdd/systems-index.md` exists → `systems-design`
   - `design/gdd/game-concept.md` exists → `concept`
   - Nothing, while technical preferences still contain engine/language
     placeholders → `not configured`

For `not configured`, show a short catalog-driven overview of the full
workflow and make `$start` the primary recommendation. Infer Concept only when
a concept artifact or another concrete Concept signal exists.

---

## Step 3: Read Session Context

Read `production/session-state/active.md` if it exists. Extract:
- What was most recently worked on
- Any in-progress tasks or open questions
- Current epic/feature/task from STATUS block (if present)

This tells you what the user just finished or is stuck on — use it to personalize
the output.

---

## Step 4: Check Step Completion for the Current Phase

For each step in the current phase (from the catalog):

### Artifact-based checks

If the step has `artifact.glob`:
- Search matching files to check if files matching the pattern exist
- If `min_count` is specified, require that many matching files
- If `artifact.pattern` is specified, evaluate the pattern against the matched
  files according to that step's existing condition; `min_count` and pattern
  must both hold. A match in one file cannot stand in for every required file.
- **Complete** = every declared artifact condition is met
- **Incomplete** = artifact is missing or pattern not found

If the step has `artifact.note` (no file pattern):
- Mark as **MANUAL** — cannot auto-detect, will ask user

If the step has no `artifact` field:
- Mark as **UNKNOWN** — completion not trackable (e.g. repeatable implementation work)

### Special case: production phase — read `sprint-status.yaml`

When the current phase is `production`, check for `production/sprint-status.yaml`
before doing any pattern-based story checks. If it exists, read it directly. If
it is absent, use the already discovered latest sprint Markdown as a read-only
fallback and report its sprint number plus resolvable active/ready/done/blocked
story counts:

- Canonical `status: in_progress` → surface as "currently active"
- Canonical `status: ready` → surface as "next up"
- Canonical `status: done` → count as complete
- Canonical `status: blocked` → surface as blocker with the `blocker` field
- For read-only backward compatibility, normalize legacy hyphenated or
  space/title-case spellings to those values; never write them back

This gives precise per-story status without Markdown scanning. Skip the pattern
artifact check for the `implement` and `story-done` steps — the YAML is authoritative.

### Special case: `repeatable: true` (non-production)

For repeatable steps outside production (e.g. "System GDDs"), the artifact
check tells you whether *any* work has been done, not whether it's finished.
Label these differently — show what's been detected, then note it may be ongoing.

---

## Step 5: Find Position and Identify Next Steps

From the completion data, determine:

1. Walk required steps in catalog order and stop progression at the first
   incomplete required step. This is the **Current blocker**.
2. The **Last confirmed complete step** is the last contiguous required step
   before that blocker. Later artifacts may be shown as `present but blocked by
   earlier step`; they never move the workflow position past the blocker.
3. **Optional opportunities** — incomplete *optional* steps that can be done
   before or alongside the blocker
4. **Upcoming required steps** — required steps after the current blocker
   (show as "coming up" so user can plan ahead)

Classify a user argument before using it:
- Treat it as a completion claim only when it contains explicit
  finished/completed semantics and the named token exactly matches a catalog
  command or step ID.
- Treat all other arguments (for example `testing`) as help topics and filter
  catalog/installed descriptions without advancing project state.

A completion claim may confirm a MANUAL/UNKNOWN item. It may not override a
required step whose catalog entry names a concrete artifact: if that artifact is
absent, keep it as the blocker and explain the evidence mismatch.

---

## Step 6: Check for In-Progress Work

If `active.md` shows an active task or epic:
- Surface it prominently at the top: "It looks like you were working on [X]"
- Suggest continuing it or confirm if it's done

---

## Step 7: Present Output

Keep it **short and direct**. This is a quick orientation, not a report.

```
## Where You Are: [Phase Label]

**In progress:** [from active.md, if any]

### ✓ Done
- [completed step name]
- [completed step name]

### → Next up (REQUIRED)
**[Step name]** — [description]
Command: `[$command]`

### ~ Also available (OPTIONAL)
- **[Step name]** — [description] → `$command`
- **[Step name]** — [description] → `$command`

### Coming up after that
- [Next required step name] (`$command`)
- [Next required step name] (`$command`)

---
Approaching **[next phase]** gate → run `$gate-check` when ready.
```

**Formatting rules:**
- `✓` for confirmed complete
- `→` for the current required next step (only one — the first blocker)
- `~` for optional steps available now
- Show commands inline as backtick code
- If a step has no command (e.g. "Implement Stories"), explain what to do instead of inventing a command
- For a MANUAL step that affects the first blocker, ask: "I can't tell if [step]
is done — has it been completed?" Until answered, present guidance as
provisional and do not emit a completion verdict.

Limit next-skill recommendations to one primary and at most two secondary
choices. The uncataloged footer and coming-up context are not additional
recommendations.

Verdict: **HELP COMPLETE** — next steps identified.

---

## Step 8: Gate Warning (if close)

After the current phase's steps, check if the user is likely approaching a gate:
- If all required steps in the current phase are complete (or nearly complete),
  add: "You're close to the **[Current] → [Next]** gate. Run `$gate-check` when ready."
- If multiple required steps remain, skip the gate warning — it's not relevant yet.

---

## Step 9: Escalation Paths

After the recommendations, if the user seems stuck or confused, add:

```
---
Need more detail?
- `$project-stage-detect` — full gap analysis with all missing artifacts listed
- `$gate-check` — formal readiness check for your next phase
- `$start` — re-orient from scratch
```

Only show this if the user's input suggested confusion (e.g. "I don't know", "stuck",
"lost", "not sure"). Don't show it for simple "what's next?" queries.

---

## Collaborative Protocol

- **Never auto-run the next skill.** Recommend it, let the user invoke it.
- **Ask about MANUAL steps** rather than assuming complete or incomplete.
- **Match the user's tone** — if they sound stressed ("I'm totally lost"), be
  reassuring and give one action, not a list of six.
- **One primary recommendation** — the user should leave knowing exactly one thing
  to do next. Optional steps and "coming up" are secondary context.
