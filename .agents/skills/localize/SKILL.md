---
name: localize
description: Run a bounded, owner-separated localization catalog and locale-package workflow with stable keys, strict plural/placeholder schemas, privacy-safe human receipts, version and existence conflict check imports/exports, and build-bound pseudo-localization or runtime evidence.
---

# Localize

Coordinate source catalog, translation package, review, freeze, and evidence records without treating templates, populated text, static scans, pseudolocalization, or QA plans as completed localization or release proof.

## Invocation

```text
$localize <subcommand> --request <request-path>
```

Supported subcommands are:

- `scan`
- `catalog-diff`
- `catalog-apply`
- `export`
- `import`
- `validate`
- `status`
- `brief`
- `cultural-review`
- `vo-scan | vo-script | vo-validate | vo-integrate`
- `rtl-check`
- `freeze-call | freeze-lift | freeze-status`
- `qa-plan`
- `evidence-review`

Request path/revision are required exactly once. With none or an invalid subcommand, show usage and stop before reading project sources, delegating, contacting anyone, or writing. Reject moving aliases, directories, traversal, symlink/junction/reparse escape, unknown/repeated flags, unsupported schema, and expected/actual revision mismatch.

The request conforms to `cgs.localization-request/v2` and declares one subcommand, exact normalized locales, canonical localization-manifest path/revision, exact source/context/package/evidence inventory, format/parser/schema expectations, bounded key/locale/file/byte/time budgets, output paths/bases/owners/writers, privacy/consent policy, and explicit non-writes.

Do not infer source locale, target locale, table path, format, build, reviewer, translator, approver, vendor, or authority.

### Exact team-narrative input adapter

`cgs.localization-request/v2` contains exactly one `narrative_handoff` object:

```yaml
narrative_handoff:
  status: PRESENT | NONE
  adapter: cgs.narrative-localization-handoff-v2-adapter/v1 | null
  path: <canonical project-relative path or null>
  revision: <exact raw handoff revision or null>
  handoff_id: <exact NLOC-* ID or null>
  content_id: <exact team-narrative content ID or null>
  run_id: <exact team-narrative run ID or null>
  authority_id: <exact caller authority or null>
```

`NONE` requires every other field to be `null`. Any source-inventory entry whose
declared origin is `TEAM_NARRATIVE` requires `PRESENT`; the adapter may not be
selected from a path, filename, prose, or matching field names. `PRESENT` requires
the exact schema/adapter shown above and a regular canonical file at the supplied
path whose declared revision matches before any narrative source, catalog, package, or
output is read.

The adapter accepts only `cgs.narrative-localization-handoff/v2` with the literal
producer fields defined by `$team-narrative`. Validate without aliases or defaults:

1. revalidate `payload_revision` with exactly `payload_revision` and derived
   `handoff_id` omitted, re-derive `handoff_id`, and revalidate the exact handoff
   declared revision; require
   path `production/narrative/team-narrative/<content_id>/<run_id>/handoffs/localization-<64-lowercase-payload-identifier>.yaml`;
2. require request `content_id`, `run_id`, and `authority_id` to equal the handoff;
   require handoff request/contract authority IDs to equal each other;
3. re-read the `cgs.localization-handoff-contract/v1` and recipient-availability
   evidence at their exact paths/revisions; require recipient workflow `localize`,
   request schema `cgs.localization-request/v2`, and this adapter ID;
4. re-read every declared canon source, reproduce `canon_baseline_revision`, and
   reject an added, omitted, reordered, or stale canon row;
5. re-read the exact `cgs.narrative-final-artifact-manifest/v2`, require its raw
   revision and `final_artifact_set_revision`, and require `story_artifacts` to equal its
   ID/path/schema/raw-revision rows exactly;
6. re-read `cgs.narrative-context-manifest/v2` and every source binding, reproduce
   its current source set, and allow no undeclared narrative source;
7. re-read `cgs.narrative-string-constraint-manifest/v2`, reproduce the ordered
   string-ID identifier, and require those IDs to be the exact narrative key scope;
8. re-read `cgs.narrative-localization-review/v2`; require verdict
   `LOCALIZATION_READY`, empty `blocking_finding_ids`, and empty
   `unknown_required_finding_ids`;
9. require both protected-content exclusion booleans `true`; and
10. require source locale, destination owner/recorder, expected output preimages,
    source/context inventory, and non-writes to equal the localization request and
    current `cgs.localization-manifest/v2` transaction scope.

The handoff supplies identity and bounded source authority only. It does not grant
catalog, package, translation, vendor-contact, import, release, or deployment
authority. Missing, malformed, stale, non-ready, authority-mismatched, scope-
expanded, or conversation-only/unpersisted handoff evidence returns
`BLOCKED: NARRATIVE_HANDOFF_INVALID` with zero source/catalog/package/translation
writes and no fallback to inferred fields.

## Authority and evidence boundaries

- Source content owners own source meaning.
- The catalog recorder owns mechanical key/schema synchronization, not source meaning.
- A named human translator/vendor owns one exact target-locale revision.
- A distinct locale-qualified reviewer owns language review of that revision. The translator cannot be its sole reviewer.
- Cultural, legal, territory, rating, platform, and shipping decisions remain with the corresponding human owner.
- QA testers own runtime execution receipts; evidence reviewers verify receipts but cannot manufacture execution.
- Import/export recorders apply exact owner-authorized bytes but cannot author translations or approvals.

One transaction has one writer per path. Proposal agents are read-only. Authorization for one subcommand/path/locale never authorizes another, external vendor communication, source meaning change, target translation creation, human sign-off, release state, or deployment.

Never invent translations, identities, consent, attestations, revisions, builds, screenshots, runtime results, vendor receipts, or writes. Use UNKNOWN/UNAVAILABLE/NOT_RUN/UNVERIFIED/PARTIAL.

## Canonical catalog and locale identities — LOC-005/007/013

The version-pinned localization manifest uses `cgs.localization-manifest/v2` and contains:

```yaml
project_id: <stable ID>
catalog_schema: cgs.localization-catalog/v2
source_locale: <canonical BCP-47 tag>
source_table: { path: ..., format: json|csv|po|xliff, schema_version: ..., parser_id: ..., parser_version: ... }
key_policy: { schema_version: ..., pattern: ..., max_bytes: ..., case_sensitive: ... }
placeholder_policy: { syntax: icu|printf|named, parser_id: ..., parser_version: ... }
plural_rules: { source_id: ..., version: ..., revision: ... }
target_locales:
  <BCP-47>:
    path: ...
    format: ...
    schema_version: ...
    translation_owner_id: <human/vendor ID or null>
    reviewer_owner_id: <distinct ID or null>
    fallback_chain: [...]
```

Strictly parse the manifest and every table with its declared deterministic parser/schema. Malformed or unsupported JSON/CSV/PO/XLIFF reports exact file/record/line/column/parser detail and causes zero writes for that locale transaction. Never guess/fallback to another parser or directory.

For every load, record the authoritative manifest path, stable business IDs, schema/version, and explicit revisions. Treat revisions as supplied metadata: never calculate them from file content.

```text
manifest_revision = <declared revision>
source_table_revision = <declared revision>
keyset_revision = <declared revision>
source_key_revision = <declared revision>
catalog_identity = <stable catalog ID>
locale_identity = <stable locale ID>
translation_revision = <declared translation revision>
```

A build/runtime/review/import/export claim must name the exact manifest, catalog, source table, keyset, per-key source revisions, locale identity, translation revision, freeze snapshot, and applicable build/asset revisions. Any mismatch is STALE/PARTIAL.

## Stable keys, placeholders, and plurals — LOC-005

Key IDs are stable semantic identifiers, not revisions of mutable source text or line numbers. Enforce the manifest's key regex/length/case policy, Unicode NFC, uniqueness under declared case policy, and reserved namespace rules.

- Never recycle a removed/deprecated key for a new meaning.
- A rename is a source-owner change request with old/new IDs, `supersedes_key`, affected locale revision set, and migration/retranslation scope; it is not an in-place identity mutation.
- Source text change increments source revision and source-key revision while retaining key ID only when source owner confirms meaning continuity.
- Orphan keys become `DEPRECATION_CANDIDATE`; deletion requires owner/change request and cannot silently erase translation history.

Parse every source/target message into the declared placeholder/message AST. Validate placeholder name/type/multiplicity, escaping/nesting, select variables, and required locale plural categories. Required categories come only from the versioned plural-rule source/revision; do not assume singular/plural or copy source-locale branches. Extra/missing/renamed/type-changed placeholders or malformed branch syntax are BLOCKED and cannot be auto-fixed during import.

Per key use exactly `UNTRANSLATED | SOURCE_COPY_CANDIDATE | MT_DRAFT | TRANSLATED_UNREVIEWED | REVIEWED | STALE`. Empty/template/source copy without exemption/machine draft/unreviewed values never count complete.

## Bounded locale batches and source context — LOC-007/008/012

Request budgets may lower but never raise these per-invocation ceilings:

| Resource | Hard ceiling |
|---|---:|
| target locales | 8 |
| keys per locale batch | 250 |
| catalog/translation bytes per file | 2 MiB |
| linked context files | 16 |
| linked context bytes total | 512 KiB |
| VO files per locale | 64 |
| read-only locale workers | 4 |
| worker time per locale | 10 minutes |
| total subcommand elapsed | 30 minutes |

Sort locales by canonical tag and keys by stable key ID. Each locale/key page is anchored to `(catalog_identity, locale_identity, translation_revision, next_key_ordinal)`. Stop before exceeding any ceiling.

Return PARTIAL with exact completed/failed/omitted locale/key/file counts, paths/revisions, reasons, and resume cursor. A missing/timeout/late/partial worker result affects only its locale but prevents all-scope success. Revoke timed-out tokens; ignore/quarantine late output. Never silently sample, infer a missing locale, or claim other locale evidence covers it.

VO subcommands require exact locale, character/speaker IDs, declared script/audio file inventory, byte/duration metadata ceilings, and consent/rights records where people/recordings are involved. No unbounded directory scan.

## Translation and review separation — LOC-010/012

Every imported translation package has a `cgs.translation-delivery/v1` receipt containing translator/vendor ID, authority/contract reference, exact locale/catalog/source/keyset/package/file revisions, covered key range, translation revision, delivery time, tool/machine-assistance disclosure, and consent/privacy reference.

Every language review uses `cgs.locale-review/v1` with a distinct locale-qualified reviewer ID, role/qualification evidence reference, exact translation revision/revision and key range, findings/decisions, start/end time, and receipt revision.

The same identity/organization may not be sole translator and sole reviewer for the same revision unless an explicit project policy allows an independently identified reviewer boundary; otherwise PARTIAL. The catalog recorder/evidence reviewer/model cannot substitute. Missing identity is `unknown`, never “user.” Reviewers do not silently edit translation bytes; corrections return to the translation owner as a new revision.

Reviewer work is split per locale/page, uses the same hard worker limits, no child delegation, and no automatic retry. Partial/malformed/stale review never marks keys REVIEWED.

## Privacy, consent, and external delivery — LOC-008/010/011

Before exporting content to or importing identity/feedback/VO from a translator, reviewer, vendor, performer, tester, or external service, require `cgs.localization-consent/v1` or an owner-approved contract/data-processing reference covering:

- participant/vendor ID and authority;
- exact data categories, purpose, locale/key/file scope, recipients and transfer region;
- source/context confidentiality class and excluded secrets/personal data;
- storage/access, retention/deletion, attribution/credit and publication rules;
- for voice, recording/use/territory/platform/term, performer credit, derivative/synthetic/AI-training permissions or prohibitions, and withdrawal limits;
- explicit consent/contract state and record revision.

Do not send external messages or files automatically. Generate a proposed package only after minimization/redaction. Never export credentials, private keys, tokens, `.env` data, unrelated personal data, unreleased secrets outside authorized scope, or unapproved participant identities. Pseudonymize identities in catalog/status artifacts.

Silence is no consent. Withdrawal/expired contract marks affected human/VO evidence `WITHDRAWN_OR_EXPIRED` and unusable; deletion/retention follows separate exact authority. An import with missing consent/contract/privacy receipt is BLOCKED.

## Subcommand contract

### `scan` — read-only

Inspect only exact request source roots/files for hardcoded player text, unsafe concatenation, positional placeholders, locale-insensitive date/number/currency, embedded image text, LTR assumptions, and plural/gender assumptions. Return path/revision/line/rule/confidence as static candidates, not runtime failure. No source/catalog edit.

### `catalog-diff` / `catalog-apply` — source catalog owner boundary

Catalog-diff strictly parses exact source references and catalog, computes deterministic new/changed/deprecation candidates, placeholder/plural/context metadata, affected key/locale revision sets, and source-owner requirements. It never changes source meaning or target translations.

Catalog-apply is allowed only with source-owner decisions, freeze LIFTED_FOR_CHANGE, exact change request, catalog-recorder ownership, and one version and existence conflict check mutation manifest. Recheck source/manifest/freeze/catalog bases immediately before write, write exact authorized bytes, read back, and record new identities. Drift writes nothing. A successful change marks affected translations/reviews/QA evidence STALE.

### `export` — immutable locale package

Export creates no translation. It renders an immutable `cgs.localization-package/v1` containing exact catalog/source/keyset/per-key/locale/plural/placeholder identities, stable key page, source text/context/glossary/do-not-translate attestations, privacy classification, owner, and package revision.

The package exposes these literal fields; consumers must not rename or infer them:

```yaml
schema: cgs.localization-package/v1
package_id: LOCPKG-<UTC-run-id>-<locale>-<page-id>
locale: <canonical BCP-47 target locale>
page: <stable page/range identity>
manifest: {schema: cgs.localization-manifest/v2, path: <canonical path>, revision: <explicit revision>}
catalog:
  schema: cgs.localization-catalog/v2
  path: <exact manifest source_table.path>
  source_table_revision: <exact raw catalog revision>
  keyset_revision: <canonical current keyset identifier>
  catalog_identity: <current derived catalog identity>
locale_identity: <current derived locale identity>
plural_policy_revision: <current plural policy identifier>
placeholder_policy_revision: <current placeholder policy identifier>
keys:
  - {key_id: <stable ID>, source_key_revision: <current per-key identifier>}
context_revision: <canonical exported context/glossary/do-not-translate identifier>
privacy_classification: <declared classification>
owner_id: <exact package owner>
package_payload_revision: <canonical payload identifier excluding package_payload_revision and package_id>
```

Serialize packages with the declared UTF-8 JSON rules: Unicode-code-point-sorted object keys, NFC strings, declared key-page array order, no insignificant whitespace, and no trailing newline. The package owner supplies a stable `package_id` and explicit `package_payload_revision`; neither is calculated from package bytes. Keep the declared file revision as separate metadata.

The catalog/export recorder is the sole writer. Preview exact package/manifest paths, bases/ABSENT, candidate revisions, locale/page, owner and non-writes. version and existence conflict check source/freeze/catalog/output before atomic create/update and read back. Export authority does not grant vendor contact or translation-file writes.

### `import` — per-locale owner/version and existence conflict check transaction

Import never changes source catalog or another locale. Validate immutable package revision, exact locale/catalog/source/keyset/per-key revisions, key coverage, stable IDs, placeholder/plural AST parity, translation delivery/owner/consent receipt, format/schema/parser, and current freeze.

For each locale, preview an independent atomic transaction containing exact target translation path and locale revision-ledger path, operations, translation owner approval, import recorder, base/candidate revisions, revision ID, package/delivery/review state, rollback bytes, and non-writes. version and existence conflict check every base/source/package immediately before commit; write both or neither, read back and validate. One locale conflict yields PARTIAL without changing other locale transactions or claiming batch completion. Import does not mark REVIEWED without a distinct matching review receipt.

### `validate` / `status` — read-only

Validate parser/schema, stable keys/lifecycle, missing/empty values, exact placeholder/plural/select parity, encoding/locale identity, source revision/per-key binding, orphan keys, MT/source-copy markers, owner/delivery/review receipts, and stale identities.

Status reports separate untranslated/source-copy/MT/unreviewed/reviewed/stale/runtime-verified counts per exact locale revision/page. Never produce one misleading localized percentage.

### `brief` / `cultural-review`

Brief uses at most the bounded linked context and outputs no translation. Cultural review produces version-bound REVIEW_CANDIDATE records only. Local cultural/legal/rating/platform human owners close their own records; the model cannot declare compliance, suitability, certification, or ship readiness.

### VO and RTL static modes — LOC-008/009

VO scan/script/validate/integrate operates on exact locale/character/file inventory. Script output is DRAFT, not recording/translation/performer approval. File presence cannot prove pronunciation, timing, lip sync, loudness, consent, rights, or in-build playback.

RTL-check produces static candidates for directional assembly, layout flags, fonts and icons. Character counts, estimated expansion, font-file/atlas presence, or source scan cannot prove pixel fit, glyph coverage, shaping, bidi, mirroring, line break, input/IME, or mixed-script behavior.

### Freeze state machine — LOC-010/011

ACTIVE freeze binds exact manifest/catalog schema/source locale/source table/keyset/per-key revisions. Freeze-call requires explicit approver ID/authority; inferred identity or “user” is invalid. ACTIVE rejects catalog/source mutation before write.

Freeze-lift requires `cgs.localization-change-request/v1` with owner/authority, reason, affected key IDs and frozen revisions, intended delta revision, impacted/retranslation locale identity+translation revision set, vendor notification proposal/receipt per affected external owner, privacy scope change, approval time/revision, and expiry. It only changes freeze state to LIFTED_FOR_CHANGE; catalog change occurs separately. Old snapshots/history remain immutable.

### `qa-plan` — plan only

Produce exact per-locale/page cases and expected evidence. Successful verdict is only QA_PLAN_READY; incomplete batches are PARTIAL_PLAN. Never execute a build, create screenshots, review language, or return PASS.

### Pseudolocalization and runtime evidence — LOC-006/009/013

Pseudolocalization is a generated test locale, never human translation. A pseudo artifact records algorithm/version/seed, expansion/bidi/diacritic/bracketing settings, exact catalog/source/keyset revisions, transformed key revisions, generated file revision, and `TEST_ONLY_NOT_TRANSLATION`.

Static pseudo generation or validation cannot prove UI/font behavior. Runtime evidence must be bound to exact build ID/revision, platform/configuration, viewport/DPI/input direction, locale/pseudo identity, manifest/freeze/catalog/source/keyset/translation revisions, font package/atlas revision, UI scene/screen ID, test-case ID, tester identity, timestamps, actual result, and screenshot/video/log revisions.

Pseudo-loc runtime cases cover truncation/overflow/overlap, variable expansion, placeholders/plurals, glyph coverage, shaping/bidi/mirroring, line breaking, input/IME, accessibility, and font fallback. Real locale language quality still needs the distinct human reviewer.

`evidence-review` consumes only `cgs.localization-evidence-manifest/v2`, revalidate all revisions/freshness/coverage, and returns QA_EVIDENCE_VERIFIED, QA_EVIDENCE_REJECTED, or PARTIAL_EVIDENCE per locale/build/page. Verified means receipt integrity/coverage only, not release/legal/platform/market approval. Downstream gates receive the immutable manifest path/revision, locale/build/catalog/source/translation identities, coverage, and expiry; never a bare report path.

For a conclusive complete evidence review only, emit one non-persisted generic record
whose producer is literally
`localize/evidence-review@cgs.localize-evidence-review/v1`:

```yaml
schema: cgs.review-evidence/v1
record_id: <stable business ID>
artifact_kind: localization-runtime-evidence-manifest
artifact_identity: <request_id>/<build_id>/<locale_page_set_id>
artifact_revision: <exact raw cgs.localization-evidence-manifest/v2 revision>
producer: localize/evidence-review@cgs.localize-evidence-review/v1
run_id: <UUIDv4>
generated_at_utc: <RFC3339 UTC>
coverage: COMPLETE
verdict: QA_EVIDENCE_VERIFIED | QA_EVIDENCE_REJECTED
extension:
  schema: cgs.localization-evidence-manifest/v2
  path: <canonical project-relative evidence-manifest path>
  revision: <same exact raw manifest revision>
persistence: NONE
gate_evidence_candidate: true
recorder_receipt: NONE
```

Canonicalize the record as UTF-8 JSON with Unicode-code-point-sorted object keys,
NFC strings, preserved array order, JSON number grammar, no insignificant
whitespace and no trailing newline. `artifact_revision` and `extension.revision`
are equal declared file revisions, not a canonical-payload substitute. Emit no generic
record for `PARTIAL_EVIDENCE`, an incomplete locale/page set, unknown/stale/not-run
evidence, or an error. The generic record is a read-only candidate: its persistence
and receipt fields remain `NONE` forever, and it is not durable gate evidence by
itself.

### Independent localization evidence recorder contract

Only a separately authorized recorder may make the exact complete returned review
durable. The compatible receipt is
`cgs.localization-evidence-review-recorder-receipt/v1`. The recorder must receive
the exact returned review bytes, revalidate the embedded generic `record_id`, re-read
the exact extension, and repeat the underlying bounded rows rather than relying on
set identifiers alone. Evidence reviewer and recorder identities must differ.

Allocate `localization_run_id` as a unique RFC 4122 UUIDv4 at recorder start. Bind that run ID to the exact request, manifest, catalog, package, key, locale/page, freeze, build, runtime-evidence, expiry, verdict, extension, and generic record identifiers listed below. Never derive the run ID or another business ID from artifact content. Use it in these exact create-only paths:

```text
production/qa/evidence/localization/<run_id>/reports/<record_id>.md
production/qa/evidence/localization/<run_id>/receipts/<record_id>.yaml
```

The receipt is canonical UTF-8 YAML and contains at least these literal fields:

```yaml
schema: cgs.localization-evidence-review-recorder-receipt/v1
receipt_id: <stable business ID>
recorder: {identity: <independent ID>, version: <version>, implementation_revision: <revision>}
producer: localize/evidence-review@cgs.localize-evidence-review/v1
source:
  review_raw_revision: <exact returned review revision>
  review_bytes: <positive integer>
  evidence_schema: cgs.review-evidence/v1
  evidence_record_id: <revision>
  extension_schema: cgs.localization-evidence-manifest/v2
  extension_path: <canonical project-relative path>
  extension_revision: <exact raw manifest revision>
  reviewer_persistence: NONE
  reviewer_recorder_receipt: NONE
identity:
  localization_run_id: <revision>
  request: {schema: cgs.localization-request/v2, id: <ID>, path: <canonical path>, revision: <revision>}
  localization_manifest: {schema: cgs.localization-manifest/v2, path: <canonical path>, revision: <revision>}
  catalog: {schema: cgs.localization-catalog/v2, path: <canonical path>, file_revision: <revision>, catalog_identity: <revision>, source_table_revision: <revision>, keyset_revision: <revision>}
  packages:
    - {schema: cgs.localization-package/v1, path: <canonical path>, file_revision: <revision>, package_id: <LOCPKG-*>, package_payload_revision: <revision>, locale: <BCP-47>, page: <stable page/range>}
  per_key_source_revisions: [{key_id: <stable ID>, source_key_revision: <revision>}]
  locale_pages:
    - {locale: <BCP-47>, page: <stable page/range>, locale_identity: <revision>, translation_revision: <revision>, native_verdict: QA_EVIDENCE_VERIFIED | QA_EVIDENCE_REJECTED}
  freeze: {snapshot_id: <ID>, revision: <revision>}
  build: {id: <ID>, artifact_revision: <revision>, platform: <ID>, configuration: <ID>}
  runtime_set_revision: <ordered font/UI/test/raw-evidence row identifier>
  expires_at_utc: <RFC3339 UTC>
target:
  report_path: production/qa/evidence/localization/<run_id>/reports/<record_id>.md
  receipt_path: production/qa/evidence/localization/<run_id>/receipts/<record_id>.yaml
  expected_report_preimage: ABSENT
  expected_receipt_preimage: ABSENT
  persisted_report_revision: <same returned review revision>
  persisted_report_bytes: <same byte count>
write:
  compare_and_set: CREATED
  read_back: VERIFIED
  read_back_revision: <same returned review revision>
decision:
  coverage: COMPLETE
  verdict: QA_EVIDENCE_VERIFIED | QA_EVIDENCE_REJECTED
  evidence_persistence: RECORDED
  gate_evidence_eligible: true
```

The underlying ordered package, per-key, locale/page, font/UI/runtime and raw
evidence rows remain mandatory even when their set identifiers are present. The
receipt is valid only if both targets were absent, version and existence conflict check created both exact targets,
read-back verified the returned bytes, every binding is current and unexpired,
coverage is complete, and the decision verdict is unchanged. Eligibility means
the record is admissible for a conclusive positive or negative gate decision; it
does not turn `QA_EVIDENCE_REJECTED` into success. A mismatched path/revision/version,
self-recording identity, reused target, partial scope, changed verdict, failed version and existence conflict check,
or unknown read-back makes the receipt invalid and gate-ineligible.

## Import/export write and recovery protocol — LOC-005/011/013

Every mutating subcommand shows one exact operation manifest before the first write: normalized paths, locale/page, owner approval, unique writer, base/ABSENT, candidate revision, size, source/package identities, rollback bytes/revision, and non-writes. Authorization is exact and non-transitive.

Recheck all preimages and identity revisions immediately before write. Use atomic replacement/group commit with rollback. On conflict, write nothing for that locale; on midcommit failure, restore exact bases and verify. Failed rollback returns RECOVERY_REQUIRED with divergent paths/revisions and blocks further localization writes. Never overwrite concurrent edits or auto-resolve a translator/catalog conflict.

## Verdicts and output

Use mode-specific verdicts only: SCAN_COMPLETE/PARTIAL; CATALOG_DIFF_READY; CATALOG_UPDATED_TRANSLATIONS_STALE; EXPORT_READY; IMPORT_COMMITTED/IMPORT_PARTIAL/NOT_IMPORTED; STATIC_VALIDATION_CLEAN/GAPS_FOUND/PARTIAL; STATUS_READY; BRIEF_READY; REVIEW_CANDIDATES_READY; VO_STATIC_REPORT_READY/VO_SCRIPT_DRAFT_READY; RTL_STATIC_CANDIDATES_READY; FREEZE_ACTIVE/FREEZE_LIFTED_FOR_CHANGE/FREEZE_STATUS_READY; QA_PLAN_READY/PARTIAL_PLAN; QA_EVIDENCE_VERIFIED/REJECTED/PARTIAL_EVIDENCE; BLOCKED; RECOVERY_REQUIRED.

Never output LOCALIZATION_COMPLETE, bare COMPLETE, generic PASS, or release approval.

Every result includes subcommand, exact locale/page scope, manifest/catalog/source/keyset/per-key/locale/translation/freeze/package/build/evidence identities that actually exist, parser/loads/budgets/omissions, owners/consent/privacy gaps, exact writes pre/post revisions or READ_ONLY_NO_CHANGES, partial/resume state, and one legal next action. Do not auto-run another mode, contact a vendor, alter translations outside import, close human review, update release gates, or deploy.
