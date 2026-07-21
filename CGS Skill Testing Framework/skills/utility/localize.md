# Skill Spec: `$localize`

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$localize` is an owner-separated localization catalog and evidence workflow. It
distinguishes source authorship, source-table recording, human translation,
locale-qualified review, cultural/legal/platform decisions, runtime QA execution, and
evidence integrity review. Every table, freeze, translation, and runtime claim is
bound to exact schema, locale, source, translation, build, and evidence hashes.
Templates, non-empty files, machine drafts, static checks, and QA plans never count as
completed localization or release proof.

---

## Static Assertions

- [ ] YAML frontmatter contains only required `name` and non-empty `description`;
      name matches the skill directory
- [ ] Metadata names owner separation, freeze control, QA planning, and hash-bound
      evidence review
- [ ] Has at least two phase headings
- [ ] Requires an explicit subcommand and locale where applicable
- [ ] `qa` is only an alias for `qa-plan` and returns `QA PLAN READY`, never a locale
      QA `PASS`
- [ ] Defines a separate `evidence-review` mode
- [ ] Freeze `ACTIVE` records schema version, source locale, source-table hash,
      keyset hash, and per-key hashes
- [ ] Active freeze rejects source-table mutation by default
- [ ] Freeze lift requires owner, authority, affected-key hashes, retranslation scope,
      and vendor notification receipts
- [ ] Cultural analysis returns `REVIEW CANDIDATE` and requires the appropriate human
      owner to close it
- [ ] The model cannot decide legal compliance, content ratings, platform
      certification, market suitability, or locale shipping
- [ ] Source author, catalog recorder, translator, locale reviewer, cultural/legal/
      platform owner, QA tester, and evidence reviewer are distinct authorities
- [ ] A translator cannot be the sole reviewer of the same translation revision
- [ ] Empty values, templates, source copies, machine drafts, and unreviewed values
      cannot count as complete
- [ ] Source locale and paths come from a versioned localization manifest, not a
      hardcoded English/default-directory assumption
- [ ] QA/runtime evidence requires exact locale, build ID/hash, platform,
      manifest/freeze/source/keyset/translation hashes, tester identity, timestamps,
      actual result, outcome, and raw evidence hashes
- [ ] Missing, mismatched, unreadable, or stale evidence cannot verify
- [ ] Read-only modes make no writes and request no changeset authorization
- [ ] Every write uses exact paths, unique writer, preimage hash, bounded
      authorization, and postimage hash
- [ ] No mode outputs `LOCALIZATION COMPLETE` or bare `COMPLETE`
- [ ] Spec covers every documented subcommand and side-effect contract

---

## Director Gate Checks

None. Localization uses domain and human authority boundaries rather than creative or
technical director gates. Product, cultural, legal, rating, platform, QA, and release
owners retain their own decisions; `localization-lead` cannot substitute for them.

---

## Test Cases

### Case 1: QA mode produces a plan, not a pass

**Fixture:**

- Manifest, freeze snapshot, source table, and `fr-FR` translation exist.
- No target build or execution receipts exist.

**Input:** `$localize qa fr-FR`

**Expected behavior:**

1. `qa` resolves to `qa-plan`.
2. The output names locale `fr-FR` and records unknown build/evidence as
   `UNKNOWN / NOT BUILT` and `NOT RUN`.
3. It creates a per-locale test plan covering functional, visual, language, cultural,
   accessibility, RTL/IME where relevant, VO, and platform cases.
4. Verdict is `QA PLAN READY`.
5. No locale `PASS`, conditional pass, ship decision, or fabricated receipt appears.

**Assertions:**

- [ ] Plan creation and execution are explicitly separate
- [ ] A plan may be written only to an authorized exact path
- [ ] Missing build/evidence stays missing
- [ ] Gate/release status is unchanged

---

### Case 2: Freeze call records an immutable source snapshot

**Fixture:**

- Localization manifest declares source locale `ja-JP` and a valid JSON source table.
- Table schema and all keys parse successfully.
- A stable freeze approver ID and authority are supplied.
- Exact freeze-record path is authorized.

**Input:** `$localize freeze call`

**Expected behavior:**

- The record contains schema version, `ja-JP`, exact source-table path and byte hash,
  table schema, key count, sorted keyset hash, every per-key hash, snapshot ID,
  approver identity/authority, UTC timestamp, and history.
- The postwrite file is re-read and its raw-byte hash reported.
- Verdict is `FREEZE ACTIVE`.

**Assertions:**

- [ ] Source locale is not assumed to be English
- [ ] `Called by: user` is not accepted as identity evidence
- [ ] No translation, source code, or source table is modified
- [ ] Missing approver or hash prevents activation

---

### Case 3: Active freeze rejects extraction changes

**Fixture:**

- Freeze state is `ACTIVE` and all frozen hashes match.
- Source scan discovers one new key.
- No authorized localization change request/lift exists.

**Input:** `$localize extract`

**Expected behavior:**

- The deterministic diff identifies the new key.
- The source table remains byte-identical.
- No target translation file changes.
- Verdict is `BLOCKED — ACTIVE FREEZE`.
- No warning-only mutation or post-freeze append occurs.

**Assertions:**

- [ ] Freeze blocks before write
- [ ] Existing planning/file authorization does not bypass freeze authority
- [ ] No translation evidence is fabricated

---

### Case 4: Freeze lift requires complete change governance

**Fixture:**

- Freeze is `ACTIVE`.
- A proposed lift omits vendor notification receipt for one affected shipping locale.

**Input:** `$localize freeze lift`

**Expected behavior:**

- The workflow lists the missing locale receipt and rejects the lift.
- Freeze remains `ACTIVE` and source bytes stay unchanged.
- With complete owner, authority, affected-key hashes, retranslation scope, and
  receipts, only the freeze record changes to `LIFTED_FOR_CHANGE`.
- The lift itself never mutates the source table.

**Assertions:**

- [ ] Every affected key is bound to its frozen hash
- [ ] All impacted locales appear in retranslation scope
- [ ] Refreezing after the catalog change creates a new snapshot rather than rewriting
      old history

---

### Case 5: Cultural analysis produces candidates for human owners

**Fixture:**

- Content includes a disputed map, religious imagery, and possible platform-rating
  concern for one region.
- No current legal/platform or local-cultural decision receipt exists.

**Input:** `$localize cultural-review zh-Hant-TW`

**Expected behavior:**

- Stable candidate IDs cite exact content paths/hashes and observed locations.
- Risk hypotheses are labeled as candidates.
- Cultural content routes to a local cultural consultant; territory/legal issues
  route to legal/compliance; rating issues route to platform/rating owner.
- Status remains `NEEDS_HUMAN_REVIEW`.
- Output makes no compliance, certification, rating, market, or ship conclusion.

**Assertions:**

- [ ] Localization-lead cannot close the candidates
- [ ] A locale language reviewer cannot substitute for legal/platform authority
- [ ] Missing current authoritative evidence remains `UNKNOWN`
- [ ] Verdict is `REVIEW CANDIDATES READY` or `PARTIAL`, not completion

---

### Case 6: Templates and unreviewed translations remain incomplete

**Fixture:**

- `fr-FR` contains one empty value, one source-identical value without exemption, one
  machine draft, and one populated human translation without a reviewer receipt.

**Input:** `$localize validate fr-FR`

**Expected behavior:**

- Keys are respectively `UNTRANSLATED`, `SOURCE_COPY_CANDIDATE`, `MT_DRAFT`, and
  `TRANSLATED_UNREVIEWED`.
- None count as reviewed or runtime-evidence-verified.
- Verdict is `GAPS FOUND`.
- Validation is read-only.

**Assertions:**

- [ ] Non-empty file existence does not imply completion
- [ ] English/source text is never copied into target values as a completed translation
- [ ] The skill never writes actual translations
- [ ] No `LOCALIZATION COMPLETE` appears

---

### Case 7: Translation and review ownership cannot collapse

**Fixture:**

- Translator `vendor-A` delivered exact `de-DE` translation hash `T1`.
- The only review receipt is signed by the same `vendor-A` identity.
- No independent locale-qualified reviewer exists.

**Input:** `$localize evidence-review production/localization/evidence/de-DE.yaml`

**Expected behavior:**

- Translation ownership is recognized, but language review is missing/invalid.
- Result is `PARTIAL EVIDENCE`.
- The skill does not invent a reviewer or re-label the translator.
- A distinct reviewer receipt for exact hash `T1` is required.

**Assertions:**

- [ ] Catalog recorder does not sign as translator
- [ ] Translator cannot be sole reviewer of its own revision
- [ ] Evidence reviewer cannot self-create missing language sign-off

---

### Case 8: Exact locale/build/hash evidence can be verified

**Fixture:**

- Immutable evidence manifest specifies `ar-SA`, build ID/hash, platform/config,
  localization manifest hash, active freeze record/snapshot, source/keyset hashes,
  translation hash, font package hash, and required test cases.
- Named QA tester receipts contain timestamps, actual results, outcomes, and
  screenshot/video/log hashes.
- A distinct locale-qualified reviewer approves the exact translation hash.
- Required cultural/legal/platform candidates have matching human-owner receipts.
- Every file is readable and recomputed hashes match.

**Input:** `$localize evidence-review <manifest-path>`

**Expected behavior:**

- Every receipt is checked against the immutable manifest and recomputed bytes.
- Required coverage is complete for exactly `ar-SA` and the named build/platform.
- Result is `QA EVIDENCE VERIFIED`.
- Output states this is evidence-integrity verification, not a release, legal,
  platform, market, or shipping approval.

**Assertions:**

- [ ] No evidence from another locale/build/revision is reused
- [ ] Tester and locale-reviewer roles remain distinct
- [ ] Gate/release files are not modified
- [ ] Result is never converted to generic `PASS`

---

### Case 9: Hash or build mismatch makes evidence stale/partial

**Variants:**

- A: source table changed after the freeze snapshot;
- B: translation hash differs from the reviewer receipt;
- C: screenshot is from another build;
- D: required test case is `NOT_RUN`;
- E: evidence path is unreadable.

**Expected behavior:**

- A supplied invalid/failing receipt yields `QA EVIDENCE REJECTED`.
- Missing, unreadable, not-run, or incomplete required evidence yields
  `PARTIAL EVIDENCE`.
- Exact mismatch fields and expected/actual hashes are reported.
- No success verdict or file mutation occurs.

**Assertions:**

- [ ] Source-table changes invalidate old evidence manifests
- [ ] Locale and build identity are mandatory
- [ ] Missing hashes are `null`/`UNAVAILABLE`, never guessed

---

### Case 10: Malformed table produces precise zero-write failure

**Fixture:**

- Manifest declares CSV translation `fr-FR`.
- CSV contains an unterminated quote at line 47.

**Input:** `$localize validate fr-FR`

**Expected behavior:**

- Error names file, line 47, and parser detail.
- Diff/validation stops for that file.
- Translation and every other file retain their preimage hashes.
- Result is `BLOCKED` or `PARTIAL` depending on requested locale scope.

**Assertions:**

- [ ] No auto-fix or overwrite
- [ ] Loaded and failed locale counts are exact
- [ ] Other requested locales may be reported, but incomplete scope cannot be called
      clean or verified

---

### Case 11: Extract changes catalog only and invalidates dependent revisions

**Fixture:**

- Freeze is `LIFTED_FOR_CHANGE` under a complete change request.
- Catalog recorder has an authorized deterministic diff.
- Target translation files exist for three locales.

**Input:** `$localize extract`

**Expected behavior:**

- Only the canonical source table is written by the catalog recorder.
- Target-locale files remain byte-identical.
- New source/keyset/per-key hashes are computed.
- Old evidence manifests become `STALE` and affected keys require retranslation or
  re-review in each impacted locale.
- Verdict is `CATALOG UPDATED — TRANSLATIONS STALE`.

**Assertions:**

- [ ] Source meaning is not changed by extraction
- [ ] Catalog authorization does not grant translation writes
- [ ] Actual preimage/postimage hashes are reported

---

### Case 12: RTL and VO static checks do not claim runtime success

**Fixture:**

- Arabic font assets and RTL flags exist statically.
- VO files are present and named correctly.
- No build-bound runtime receipts exist.

**Input:** `$localize rtl-check ar-SA` and separately
`$localize vo-pipeline validate ar-SA`

**Expected behavior:**

- RTL returns static candidates/report only.
- VO returns static presence/reference report only.
- Neither claims shaping, bidi, glyph coverage, mirroring, lip sync, timing, playback,
  pronunciation, or language quality passed.
- Runtime evidence remains `NOT RUN`.

**Assertions:**

- [ ] Static file presence is not build evidence
- [ ] Runtime verification requires exact locale/build/source/translation/asset hashes
- [ ] Both modes are read-only

---

### Case 13: Authorization remains mode-, path-, and owner-bounded

**Fixture:**

- User authorized one translator-brief path.
- During briefing, a new target translation file, cultural report, and freeze change
  are suggested.

**Input:** `$localize brief es-MX`

**Expected behavior:**

- Only the exact brief may be written by its named recorder.
- Translation, cultural report, and freeze paths remain untouched.
- The workflow asks for a revised manifest before any added path or operation.
- File authorization does not provide translator/reviewer/legal/vendor authority.

**Assertions:**

- [ ] Read-only findings do not silently become writes
- [ ] Subagent delegation cannot broaden authority
- [ ] No external vendor message is sent

---

### Case 14: Every subcommand has one declared side-effect contract

**Variants:**

- `scan`; `extract`; `validate`; `status`; `brief`; `cultural-review`;
  each `vo-pipeline` action; `rtl-check`; each `freeze` action; `qa-plan`/`qa`;
  `evidence-review`; invalid/no subcommand.

**Expected behavior:**

- Each valid command returns only a verdict declared in the side-effect table.
- Read-only modes make zero writes and request no write authorization.
- Mutating modes show exact path/writer/preimage manifest before writing.
- Invalid/no subcommand reads/writes nothing and returns usage.
- No mode returns `LOCALIZATION COMPLETE` or bare `COMPLETE`.

**Assertions:**

- [ ] Mode parser and spec match the SKILL invocation list
- [ ] All target-locale modes require explicit locale
- [ ] No fallback directory or hardcoded source locale is used
- [ ] No director gate is invoked

---

## Protocol Compliance

- [ ] Treats existing bounded authorization as sufficient only for the exact listed
      paths and operations
- [ ] Otherwise asks once for the complete mutation manifest before the first write
- [ ] Does not re-prompt per file within an unchanged authorized manifest
- [ ] Requests new authority for new paths, translation ownership, human review,
      vendor contact, release changes, or another subcommand
- [ ] Rechecks preimages before writes and reports actual postimage hashes
- [ ] Preserves source/catalog/translation/review/testing/release ownership
- [ ] Reports partial locale loads and missing evidence explicitly
- [ ] Recommends one next action and invokes nothing automatically

---

## Coverage Notes

Case 1 covers LOC-001; Cases 2–4 cover LOC-002; Case 5 covers LOC-003; the rewritten mode matrix and Case 14 cover LOC-004. Cases 6–13 cover the required owner,
placeholder, hash, locale, build-evidence, and authorization boundaries. Case 14
prevents future mode/spec drift. These are behavioral expectations only: this
remediation performed static validation and did not execute `$localize`, contact a
translator, run a build, review a locale, modify catalog results, or produce QA
evidence.
