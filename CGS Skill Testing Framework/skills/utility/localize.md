# Contract Specification: `localize`

## Purpose

Validate `localize` as an owner-separated, hash-bound source-catalog, locale-package, freeze, review, and runtime-evidence workflow. Templates, populated values, machine drafts, static checks, pseudolocalization, and QA plans never become completed localization or release proof.

## Contract identities

- Request: `cgs.localization-request/v2`
- Manifest: `cgs.localization-manifest/v2`
- Catalog: `cgs.localization-catalog/v2`
- Locale package: `cgs.localization-package/v1`
- Translation delivery: `cgs.translation-delivery/v1`
- Locale review: `cgs.locale-review/v1`
- Consent/privacy: `cgs.localization-consent/v1`
- Change request: `cgs.localization-change-request/v1`
- Evidence manifest: `cgs.localization-evidence-manifest/v2`
- Narrative adapter: `cgs.narrative-localization-handoff-v2-adapter/v1` over
  `cgs.narrative-localization-handoff/v2`
- Skill: `.agents/skills/localize/SKILL.md`
- Metadata: `.agents/skills/localize/agents/openai.yaml`

## Invocation and modes

```text
$localize <subcommand> --request <path> --expect-request <sha256:...>
```

Supported subcommands: scan; catalog-diff/apply; export/import; validate/status; brief/cultural-review; vo-scan/script/validate/integrate; rtl-check; freeze-call/lift/status; qa-plan; evidence-review.

No/invalid mode or missing/mismatched request returns usage/error with zero project-source reads, delegation, external contact, or writes. Locales, paths, formats, source language, build, owners, and authority are never inferred.

## P0 invariants retained

1. QA_PLAN_READY is planning only; it cannot return PASS/ship/runtime evidence.
2. ACTIVE freeze binds manifest/catalog/source/keyset/per-key hashes and rejects catalog mutation before write unless a complete owner change request lifts it.
3. Cultural/legal/rating/platform/territory/market candidates require their human owner and cannot be closed by the model/localization lead.
4. Modes have one declared side-effect/verdict contract; no LOCALIZATION_COMPLETE, bare COMPLETE, or generic PASS exists.
5. Templates/source copies/MT drafts/unreviewed values/file existence do not count completed.
6. Every write uses exact path/owner/writer/base/candidate authorization, CAS, read-back, and rollback.

## P1 requirements

### A. Strict canonical formats and identity hashes — LOC-005

1. `cgs.localization-manifest/v2` declares project/source locale, catalog schema, exact table path/format/schema/parser/version, key policy, placeholder syntax/parser/version, plural rule source/version/hash, and each target locale path/format/schema/owners/fallback chain.
2. JSON/CSV/PO/XLIFF use strict deterministic parsers. Unsupported schema/parser or malformed file reports exact file/record/line/column/parser and writes nothing for that locale.
3. Manifest/source table raw hashes, canonical keyset hash, per-key source hash, catalog identity, locale identity, and translation revision identity are distinct and reproducibly derived.
4. Every import/export/review/build/evidence claim names exact manifest/catalog/source/keyset/per-key/locale/translation/freeze identities.
5. Any missing/mismatch becomes STALE/PARTIAL, never inferred.

### B. Stable keys, plurals and placeholders — LOC-005

1. Keys are stable semantic IDs under versioned regex/length/case/NFC/namespace policy; uniqueness uses the declared case policy.
2. Key IDs are not derived from mutable source text/line. Deprecated keys are never recycled.
3. Rename requires old/new IDs, `supersedes_key`, owner change request, affected locale hashes and migration/retranslation scope.
4. Source text revision changes per-key hash; retaining key requires source-owner meaning-continuity confirmation.
5. Orphans are DEPRECATION_CANDIDATE and history cannot be silently deleted.
6. Source/target messages parse to the declared AST; validation covers placeholder name/type/multiplicity, escaping/nesting, select variables and plural branches.
7. Required plural categories come only from versioned locale rules/hash. Missing/extra-invalid/renamed/type-changed placeholders or malformed plural/select syntax block import and cannot auto-fix.

### C. Static layout signals require runtime evidence — LOC-006/009

1. Character counts, estimated expansion, static source scan, font/atlas file presence, RTL flags and audio files are candidates only.
2. They cannot prove pixel fit, overflow, glyph coverage, shaping/bidi/mirroring, line breaks, IME/input, mixed script, pronunciation, timing, lip sync, loudness or playback.
3. Pseudolocalization records algorithm/version/seed/settings plus exact catalog/source/keyset and generated hashes and is always TEST_ONLY_NOT_TRANSLATION.
4. Runtime proof binds exact build ID/hash, platform/config, viewport/DPI/direction, locale/pseudo identity, catalog/source/keyset/translation/freeze/font/scene/test identities, tester/times/results and screenshot/video/log hashes.
5. Pseudo runtime cases cover expansion/overlap/truncation, variables/placeholders/plurals, glyph/font fallback, shaping/bidi/mirroring, line breaking, IME/input and accessibility.
6. Real language quality still requires a distinct locale-qualified reviewer.

### D. Explicit locales and bounded linked sources/batches — LOC-007

1. Every locale-aware mode receives exact canonical BCP-47 locales; no English/default/fallback inference.
2. Hard ceilings: 8 locales, 250 keys/locale page, 2 MiB per catalog/translation file, 16 linked context files/512 KiB total, 64 VO files/locale, 4 read-only locale workers, 10 minutes/worker and 30 minutes/subcommand.
3. Request values can only lower ceilings. Locales/keys sort deterministically.
4. Resume cursor binds catalog identity, locale identity, translation revision and next key ordinal.
5. Limit/timeout/partial worker returns PARTIAL with completed/failed/omitted locale/key/file identity/reason/cursor. No sample or cross-locale substitution.
6. Brief reads only bounded exact linked context and is PARTIAL on omission.

### E. VO nested scope and privacy — LOC-008

1. VO action, locale, character/speaker IDs, script/audio inventory, byte/duration metadata, owner, rights/consent and outputs are top-level request fields, not hidden nested defaults.
2. Directory scans and unbounded scripts/audio are forbidden; 64 files/locale ceiling applies.
3. VO script is a draft only. Presence cannot prove translation, performance, pronunciation, sync, loudness, rights or runtime playback.
4. Human voice evidence requires exact performer/contract/consent record with recording/use/territory/platform/term/credit/derivative/synthetic/AI permissions or prohibitions.
5. Missing/withdrawn/expired rights makes evidence unusable and blocks import/integration claims.

### F. Truthful human identity and translator/reviewer separation — LOC-010/012

1. Freeze approver, translator/vendor, reviewer, performer, tester and cultural/legal/platform owner identities are explicitly supplied stable IDs or `unknown`; inferred “user” is invalid.
2. `cgs.translation-delivery/v1` binds translator authority, exact locale/catalog/source/keyset/package/file/revision, key range, delivery time and machine-assistance disclosure.
3. `cgs.locale-review/v1` binds a distinct locale-qualified reviewer, exact revision/hash/key range, findings/decision/times and receipt hash.
4. Translator cannot be sole reviewer of its revision absent an explicit project policy proving an independently identified review boundary.
5. Catalog/evidence recorder/model cannot translate or self-create review. Corrections return to translator as a new revision.
6. Reviewer work is per locale/page under bounded workers, one attempt, no child delegation; partial/malformed/stale review never yields REVIEWED.

### G. Structured freeze lift/change impact — LOC-011

1. `cgs.localization-change-request/v1` binds owner/authority/reason, affected key IDs and frozen hashes, intended delta, impacted locale identity+translation hash set, retranslation/re-review scope, vendor notification proposal/receipt, privacy change, approval time/hash and expiry.
2. Missing affected keys, locale scope, owner, or required notification receipt blocks lift.
3. Lift changes only freeze state to LIFTED_FOR_CHANGE; catalog apply is separate.
4. Successful catalog apply recomputes identities and marks affected translations/reviews/QA evidence STALE.
5. Old freeze snapshots/history are immutable; refreeze creates a new snapshot.

### H. Bounded locale delegation and PARTIAL semantics — LOC-012

1. At most 4 read-only locale workers, 10 minutes each, 30 minutes total, exact locale/page assignment, no child delegation and no automatic retry.
2. Worker receives exact input hashes and schema, returns complete response with attempt token/status/hash.
3. Timeout/missing/late/partial/malformed result is locale PARTIAL; late token is revoked/quarantined.
4. One worker cannot cover multiple undeclared locales or attest human translation/review/QA.
5. Other locale results remain independently reportable but the batch cannot claim full coverage.

### I. Immutable build/source/locale gate handoff — LOC-013

1. Evidence review accepts only `cgs.localization-evidence-manifest/v2`, not a bare report path.
2. It recomputes locale/build/platform, manifest/freeze/catalog/source/keyset/per-key/translation/font/VO/scene/test/evidence hashes, freshness and required coverage.
3. Every receipt names tester identity/times/actual result/outcome/raw evidence; language review and cultural/legal/platform owner receipts remain distinct.
4. Results are QA_EVIDENCE_VERIFIED/REJECTED/PARTIAL_EVIDENCE per exact locale/build/page.
5. Verified means evidence integrity/coverage only, not release/legal/platform/market approval.
6. Only a conclusive complete review emits a non-persisted `cgs.review-evidence/v1`
   candidate from literal producer
   `localize/evidence-review@cgs.localize-evidence-review/v1`; its exact extension
   is the path/raw-hash-bound `cgs.localization-evidence-manifest/v2`, its
   `artifact_sha256` equals that raw hash, and its persistence/receipt remain NONE.
7. Durable gate evidence additionally requires an independent current
   `cgs.localization-evidence-review-recorder-receipt/v1` proving exact returned
   review bytes, generic record ID, extension path/hash, request/manifest/catalog/
   package/per-key/locale/translation/freeze/build/font/UI/runtime identities,
   complete current unexpired coverage, canonical create-only targets, ABSENT
   preimages, CAS creation and verified read-back.
8. A receipt may preserve either conclusive native verdict, but may not alter it;
   eligibility is admissibility, not a positive localization or release verdict.
   Missing/stale/not-run/mismatched/partial evidence cannot be promoted.

### J. Exact team-narrative input adapter — LOC-007/010/013

1. `cgs.localization-request/v2` declares `narrative_handoff.status` as exactly
   PRESENT or NONE; TEAM_NARRATIVE source rows require PRESENT.
2. PRESENT consumes only `cgs.narrative-localization-handoff/v2` through
   `cgs.narrative-localization-handoff-v2-adapter/v1`, pinned by exact path/raw
   hash/handoff/content/run/authority IDs. No alias or heuristic selection exists.
3. The adapter revalidates current contract/availability, equal caller authority,
   canon source rows/baseline, final story-artifact manifest/rows, context/source
   bindings, string constraints/order, LOCALIZATION_READY review with zero
   blocker/unknown IDs, exclusions, destination ownership/preimages, and payload.
4. Invalid, stale, unpersisted, scope-expanded, or non-ready evidence is
   `BLOCKED: NARRATIVE_HANDOFF_INVALID` before source or output writes.

## Parent-requested owner/CAS and privacy contracts

### Import/export owner and CAS

Export creates an immutable source package only; it never creates translation or contacts a vendor. Exact `cgs.localization-package/v1` fields bind package ID, locale/page, manifest path/raw hash, catalog path/raw hash, source-table/keyset/catalog/locale/plural/placeholder identities, ordered per-key source hashes, context/glossary/do-not-translate digest, privacy, owner, canonical payload hash, and separate raw-file hash. The canonical payload omits exactly `package_payload_sha256` and derived `package_id`; the latter is re-derived from the digest, so no placeholder/self-referential ID participates. Exact package paths/bases/candidates are owner-authorized and CAS/read-back verified.

Import operates per locale and never mutates source/another locale. It validates package/delivery/consent, current source/key/locale identities, stable IDs, placeholder/plural AST and owner. Target translation plus revision ledger commit atomically with exact owner/writer/base/candidate/rollback/CAS. One locale conflict produces PARTIAL and cannot affect others. REVIEWED requires a distinct matching review receipt.

Catalog apply is owned by the catalog recorder and requires source-owner decisions plus lifted freeze/change request. It cannot write target translations. Every midcommit failure rolls back; failed rollback is RECOVERY_REQUIRED and blocks new localization writes.

### Consent/privacy

Before external translator/reviewer/vendor/performer/tester data transfer or human feedback/recording, require `cgs.localization-consent/v1` or approved contract/DPA reference covering exact subject/authority, data categories/purpose, locale/key/file scope, recipients/transfer region, confidentiality/exclusions, storage/access/retention/deletion, attribution/publication, and VO rights where applicable.

No automatic external messaging. Export is minimized/redacted and excludes credentials, `.env`, secrets, unrelated personal/confidential data, and unapproved identity. Silence is no consent. Withdrawal/expiry marks evidence WITHDRAWN_OR_EXPIRED; retention/deletion requires separate authority.

## Per-key status and mode verdicts

Per key: UNTRANSLATED, SOURCE_COPY_CANDIDATE, MT_DRAFT, TRANSLATED_UNREVIEWED, REVIEWED, or STALE.

Mode verdicts are limited to SCAN_COMPLETE/PARTIAL; CATALOG_DIFF_READY; CATALOG_UPDATED_TRANSLATIONS_STALE; EXPORT_READY; IMPORT_COMMITTED/IMPORT_PARTIAL/NOT_IMPORTED; STATIC_VALIDATION_CLEAN/GAPS_FOUND/PARTIAL; STATUS_READY; BRIEF_READY; REVIEW_CANDIDATES_READY; VO_STATIC_REPORT_READY/VO_SCRIPT_DRAFT_READY; RTL_STATIC_CANDIDATES_READY; FREEZE_ACTIVE/FREEZE_LIFTED_FOR_CHANGE/FREEZE_STATUS_READY; QA_PLAN_READY/PARTIAL_PLAN; QA_EVIDENCE_VERIFIED/REJECTED/PARTIAL_EVIDENCE; BLOCKED; RECOVERY_REQUIRED.

No verdict is release approval.

## Behavioral cases

### Case 1 — Malformed catalog

CSV has an unterminated field. Exact parser/line/column is reported; import/apply writes nothing. Another locale may report independently but batch is PARTIAL.

### Case 2 — Key rename and plural mismatch

Source key rename lacks supersedes/change request and target omits a required locale plural branch while renaming a placeholder type. Import is blocked; neither target nor ledger changes; no automatic repair occurs.

### Case 3 — Static width/font/RTL

Character count and font asset appear acceptable. No build screenshots/logs exist. Output is static candidate/NOT_RUN, never QA evidence verified.

### Case 4 — Bounded locale batch

Ten locales requested. Only deterministic first eight fit; omitted locales and resume cursor are reported, and all-scope status is PARTIAL.

### Case 5 — VO consent

Audio file exists but performer contract lacks synthetic/AI/territory terms and recording consent. VO remains blocked; presence cannot prove usable/integrated.

### Case 6 — Translator self-review

Same identity delivered and solely reviewed exact revision. Status is TRANSLATED_UNREVIEWED/PARTIAL until a distinct qualified review receipt exists.

### Case 7 — Freeze lift

Affected key/locale hash set is incomplete and one vendor receipt missing. Freeze remains ACTIVE and source bytes unchanged. Complete request lifts only state, then catalog apply uses separate CAS.

### Case 8 — Locale worker timeout

One of four workers times out and later responds. Its locale is PARTIAL; late output quarantined; other results remain scoped; no batch-wide success.

### Case 9 — Gate handoff mismatch

Evidence manifest references another build/source translation hash. Review rejects/stales exact receipts and passes no generic report path/status to gate.

### Case 10 — Export/import CAS

Export package source hash changes before write: no package. During import target translation changes after preview: locale transaction writes neither translation nor ledger; new preview/authorization required.

### Case 11 — P0 regression

QA plan cannot PASS; ACTIVE freeze blocks mutation; model cannot close cultural/legal issue; no LOCALIZATION_COMPLETE; read-only modes write nothing.

### Case 12 — Team-narrative handoff adapter is exact and current

A request declares TEAM_NARRATIVE source rows and a path/hash-pinned v2 handoff.
The positive fixture reproduces the contract/availability, authority, canon,
story-artifact, context/source, string/readiness, exclusion, destination, and
payload identities, computing the payload with exactly `payload_sha256` and
derived `handoff_id` omitted, and may proceed to the selected localize subcommand without
granting any extra write. Negative variants change one raw source hash, omit one
story row, reorder a string ID, use non-ready/UNKNOWN review evidence, mismatch
authority/output ownership, set an exclusion false, supply conversation-only
bytes, or use an unknown adapter. Every negative variant returns
`BLOCKED: NARRATIVE_HANDOFF_INVALID`, performs zero source/output writes, and
never guesses a replacement field.

### Case 13 — Evidence envelope and independent recorder are exact

A complete current evidence manifest produces a `cgs.review-evidence/v1`
candidate whose producer, record ID, raw-manifest artifact hash, exact v2 extension
path/hash, COMPLETE coverage, unchanged conclusive native verdict, NONE
persistence and NONE recorder fields reproduce exactly. It is not durable gate
evidence alone. A distinct authorized recorder then creates the canonical report
and `cgs.localization-evidence-review-recorder-receipt/v1` paths from ABSENT,
recomputes all request/manifest/catalog/package/per-key/locale/translation/freeze/
build/font/UI/runtime bindings, and verifies the exact returned bytes by read-back;
only that chain is gate-eligible. Independent variants with PARTIAL_EVIDENCE,
stale/expired scope, wrong extension or package raw hash, changed native verdict,
self-recording identity, reused target, non-created CAS, or unknown read-back emit
no valid durable receipt and remain gate-ineligible.

### Case 14 — Package ID derivation is non-circular

Export canonicalizes the package with exactly `package_payload_sha256` and the
derived `package_id` omitted, computes the digest, derives `package_id` as
`LOCPKG-` plus the first 20 lowercase digest characters, serializes the completed
package, and separately hashes its raw file. A variant hashing a placeholder or
completed `package_id`, omitting only the digest field, or substituting the raw-file
hash is invalid and writes no package.

## Negative assertions

Any is a contract failure:

- parser fallback or write after parse error;
- key recycling, text-derived unstable key, unchecked placeholder/plural mismatch;
- static character/font/RTL/VO/pseudo evidence called runtime pass;
- implicit locale, unbounded context/VO/locale work, late worker accepted;
- translator self-review or inferred approver identity;
- freeze lift without affected key/locale/vendor/privacy scope;
- gate handoff by bare report path without locale/build/source hashes;
- external transfer/recording without consent/contract/minimization;
- import/export without owner/base/candidate CAS and read-back;
- auto vendor contact, downstream gate mutation, deployment, generic PASS/COMPLETE.
- TEAM_NARRATIVE source admission without the exact current persisted v2 handoff,
  equal authority, complete current hash sets, and LOCALIZATION_READY zero-blocker
  evidence.
- generic localization evidence without its exact current v2 extension, or a
  persistence claim without the independent recorder receipt, canonical
  create-only targets, CAS and verified read-back.

## Remediation traceability

| Finding | Closure evidence |
|---|---|
| LOC-005 | Sections A/B and import/export contracts define strict parser/schema, stable keys, plural/placeholder AST and zero-write failures |
| LOC-006 | Section C requires build-bound pseudo/UI/font evidence and limits static character checks to candidates |
| LOC-007 | Sections D/J and Case 12 require explicit locales, bounded linked sources, and exact path/hash-pinned narrative source admission |
| LOC-008 | Section E moves VO action/locale/character/files/limits/rights into the request schema |
| LOC-009 | Section C requires runtime visual matrix/receipts for RTL and pseudo-localization claims |
| LOC-010 | Sections F/J and Case 12 require explicit human/caller authority identities and forbid inferred `user` or handoff authority |
| LOC-011 | Section G defines affected-key/locale hashes, vendor receipts, privacy/retranslation scope and immutable freeze lineage |
| LOC-012 | Section H bounds per-locale workers/time/delegation and enforces PARTIAL for missing responses |
| LOC-013 | Sections I/J and Cases 12/13 bind immutable downstream evidence and exact current upstream narrative hashes; neither a bare report, unpersisted generic candidate, nor conversation-only handoff is durable gate evidence |

## Output

Every result records subcommand, locale/page scope, exact identities that exist, parser/budget/omission counts, owner/consent/privacy gaps, writes pre/post hashes or READ_ONLY_NO_CHANGES, partial cursor/recovery state, one legal next action, and `auto_executed: false`.
