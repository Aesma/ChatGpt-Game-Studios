# Behavioral Test Spec: tech-debt

## Purpose

Verify the four-mode `tech-debt` contract: idempotent fingerprinting, evidence-based advisory scoring, immutable event history, and explicitly authorized atomic mutations.

## Fixtures

Use isolated repositories with deterministic clocks, UUID providers, source hashes, analyzer versions, and a failure-injectable atomic register writer. The authoritative path is `docs/tech-debt-register.md`.

Tests do not invoke another project skill or mutate sprint plans.

## Global assertions

1. Scan findings remain `CANDIDATE` until user triage.
2. A fingerprint has at most one owning `CREATED` event.
3. Existing event bytes and order never change.
4. Prioritize and report modes are read-only.
5. A register mutation requires one exact preview, authorization, base-hash compare, atomic commit, and post-write verification.
6. Analyzer output never chooses acceptance, product priority, or sprint scheduling.
7. Skill, metadata, and this spec use the same mode and outcome vocabulary.

## TDB-001 — First scan records selected candidates

**Given:** A valid empty schema-v2 register and two verified findings with distinct fingerprints.

**When:** The user selects both candidates and authorizes the exact recorder preview.

**Then:**

- two collision-resistant debt IDs receive exactly one `CREATED` event each;
- the final register preserves its base prefix and appends events in previewed order;
- the verified outcome is `REGISTER_UPDATED`.

## TDB-002 — Identical rescan is idempotent

**Given:** Registered fingerprint F with an `OBSERVED` event for source revision R and evidence hash E.

**When:** The identical scope is scanned again at R/E.

**Then:**

- F resolves to its existing debt ID;
- no `CREATED` or `OBSERVED` event is proposed;
- the register is not written;
- outcome is `NO_NEW_DEBT_FOUND`.

## TDB-003 — New revision updates last-seen without duplicate debt

**Given:** Registered fingerprint F last observed at R1.

**When:** The same normalized evidence is present at R2.

**Then:**

- the same debt ID is retained;
- at most one `OBSERVED` event for R2 is proposed;
- after authorization, replayed `last_seen` is R2 and the `CREATED` count remains one.

## TDB-004 — Line movement does not change identity

**Given:** Rule, canonical path, stable symbol, and normalized evidence text are unchanged.

**When:** Only line and column numbers move.

**Then:** The fingerprint is unchanged because volatile locations are excluded.

## TDB-005 — Rename behavior is explicit

**Given:** A registered finding moves from one canonical path to another.

**When:** The new path is scanned.

**Then:**

- the raw fingerprint changes;
- proven repository rename evidence or explicit user confirmation may propose `FINGERPRINT_ALIAS` for the same debt ID;
- without that evidence, the item remains a new candidate and the old item is not auto-resolved.

## TDB-006 — Fingerprint normalization is deterministic

**Given:** Equivalent evidence with CRLF/LF, outer whitespace, horizontal whitespace, Unicode normalization, and `\\`/`/` path separator variations.

**When:** `td-fp-v1` normalization runs.

**Then:** Equivalent canonical inputs yield the same SHA-256 fingerprint, while a changed rule, path, symbol, or normalized text yields a different one.

## TDB-007 — Duplicate ownership blocks mutation

**Given:** Two debt IDs own the same primary fingerprint or alias.

**When:** Any mutating mode replays the register.

**Then:**

- outcome is `REGISTER_ERROR`;
- no new event or replacement file is written;
- the conflicting debt IDs and fingerprint are reported.

## TDB-008 — Fixed priority score and tie-breaks

**Given:**

- A: impact 4, frequency 2, effort 2;
- B: impact 3, frequency 4, effort 3;
- C: impact 2, frequency 2, effort 1.

**When:** Prioritize mode runs.

**Then:**

- each score is exactly 4 before display rounding;
- order is A, B, C by impact descending, then the remaining documented tie-breaks;
- the view shows every input, evidence, calculation, and tie-break;
- the register hash is unchanged.

## TDB-009 — Missing score inputs are never invented

**Given:** One item lacks numeric frequency and another has only legacy T-shirt effort.

**When:** Prioritize mode runs without a recorded calibration.

**Then:**

- both items are `UNSCORED`;
- neither receives an inferred number or ranked position among scored items;
- outcome is `PRIORITY_VIEW_PARTIAL`;
- the user/producer, not the analyzer, retains priority and scheduling authority.

## TDB-010 — Advisory ranking never rewrites history

**Given:** A register whose chronological debt entries differ from score order.

**When:** Prioritize mode displays the score order.

**Then:**

- no event is appended;
- no existing byte moves;
- the register hash remains identical;
- outcome is `PRIORITY_VIEW_READY` or `PRIORITY_VIEW_PARTIAL`.

## TDB-011 — Status change is append-only

**Given:** An `OPEN` debt item.

**When:** The user records an acceptance or resolution with reason and evidence.

**Then:**

- the original `CREATED` and earlier events remain byte-for-byte and in order;
- one authorized `ACCEPTED` or `RESOLVED` event is appended;
- replay derives the new status;
- no table or event log is resorted.

## TDB-012 — Concurrent revision conflict requires fresh consent

**Given:** A preview authorized against base hash H1.

**When:** Another writer changes the register to H2 before commit.

**Then:**

- compare-and-set rejects the stale mutation;
- no last-writer-wins overwrite occurs;
- proposed events are rebased and deduplicated;
- changed content/event IDs/hash are shown in a fresh preview requiring fresh authorization.

## TDB-013 — UUID collision never overwrites identity

**Given:** The UUID provider produces an ID already owned by another entry or event.

**When:** A mutation is drafted or revalidated.

**Then:**

- the collision is detected;
- a new ID is generated before preview, or the mutation stops;
- a collision after authorization invalidates authorization;
- no conflicting identity is committed.

## TDB-014 — Mutation failure preserves exact base

**Given:** An authorized proposal and an injected prepare, replace, or verification failure.

**When:** The recorder commits.

**Then:**

- the register is restored to its exact base hash, or remains absent for a failed create;
- outcome is `MUTATION_FAILED`;
- `REGISTER_UPDATED` is forbidden.

## TDB-015 — Missing and malformed register behavior

**Given:** In separate fixtures, the register is absent and the register has an unsupported schema.

**When:** Each mode runs.

**Then:**

- an absent register is treated as empty for scan analysis but is created only through an exact authorized preview;
- add may propose authorized creation;
- prioritize/report return a partial empty view or explicit absence without writing;
- malformed schema returns `REGISTER_ERROR` and is never silently repaired.

## TDB-016 — Heuristic and analyzer boundaries

**Given:** A TODO in first-party source, a 600-line generated file, vendored code, and an unavailable clone detector.

**When:** Scan mode runs.

**Then:**

- the TODO is a candidate, not automatically accepted debt;
- generated and vendored files are excluded with reasons;
- duplication is `UNVERIFIED` rather than fabricated;
- outcome is `SCAN_PARTIAL`;
- no register write occurs without selected findings and authorization.

## TDB-017 — Reappeared resolution requires triage

**Given:** A `RESOLVED` item whose fingerprint is observed again.

**When:** Scan mode runs.

**Then:**

- the existing debt ID is reported as `REAPPEARED`;
- no automatic status change occurs;
- reopening requires an authorized append-only transition event.

## TDB-018 — Manual add deduplicates

**Given:** Add-mode input normalizes to an existing `manual@1` fingerprint.

**When:** The user completes the input.

**Then:**

- no duplicate `CREATED` event is proposed;
- the existing debt ID is offered for observation or triage;
- unknown category, owner, or numeric estimates remain explicit `UNKNOWN`.

## TDB-019 — Report baseline and aging are evidence-bound

**Given:** A valid event cursor and stable sprint-transition events.

**When:** Report mode runs.

**Then:** Changes, trend, and three-sprint aging are computed from those records.

**And given:** No comparable baseline or sprint history.

**Then:** Trend and aging are `UNKNOWN`, not inferred.

## TDB-020 — Usage and outcome vocabulary

**Given:** No mode or an unknown mode.

**When:** Invocation is parsed.

**Then:**

- outcome is `USAGE_ERROR`;
- no scan, register read beyond what usage requires, or write occurs;
- `FAIL` is not used as a quality verdict.

## Static conformance checks

The candidate bundle passes only if:

- frontmatter contains only `name` and `description`;
- metadata names all four modes and the mutation boundary;
- `td-fp-v1` includes rule, path, symbol, and normalized text but excludes line numbers;
- identical source revision/evidence cannot add a second event;
- priority inputs, formula, rounding, unscored behavior, and all six tie-breaks are fixed;
- prioritize/report cannot mutate or reorder the register;
- status changes use append-only events;
- mutations require authorization, CAS, atomic replacement, and verification;
- the spec covers repeat scans, movement/rename, missing/bad register, conflicts, collisions, heuristics, unavailable analyzer, scoring, overrides, history, and aging.
