---
name: localize
description: "Runs an owner-separated, hash-bound localization catalog and evidence workflow without treating templates, static checks, or QA plans as completed translation or release proof."
---

# Localize

## Invocation

Invoke one explicit subcommand:

`$localize scan`  
`$localize extract`  
`$localize validate <locale|--all>`  
`$localize status`  
`$localize brief <locale>`  
`$localize cultural-review <locale-or-region>`  
`$localize vo-pipeline <scan|script|validate|integrate> <locale>`  
`$localize rtl-check <locale>`  
`$localize freeze <call|lift|status>`  
`$localize qa-plan <locale...>`  
`$localize qa <locale...>`  
`$localize evidence-review <evidence-manifest-path>`

`qa` is a compatibility alias for `qa-plan`. It creates a plan only and can never
return a locale QA pass.

If no subcommand or an invalid combination is provided, return usage and stop before
delegating, reading project files, or writing. Do not infer a locale, table path,
source language, build, reviewer, or approval.

## Non-negotiable contract

1. **Owner separation** — Source authors own source meaning and application content;
   the catalog recorder owns key/schema synchronization; a named human
   translator/vendor owns target-locale values; a locale-qualified reviewer owns
   language review; cultural, legal, ratings, and platform decisions remain with the
   corresponding human authority; QA testers own runtime execution receipts. No role
   may use another role's authority.
2. **No self-certification** — The localization lead coordinates the pipeline and may
   record catalog diffs or review evidence, but does not write actual translations,
   impersonate a native reviewer, or close its own cultural/legal/platform candidate.
   The translator for a locale revision cannot approve that same revision as its sole
   language reviewer.
3. **No placeholder completion** — An empty value, source-language copy, generated
   skeleton, machine-translation draft, unchecked non-empty value, or file existence
   is not a completed translation. Use `UNTRANSLATED`, `SOURCE_COPY_CANDIDATE`,
   `MT_DRAFT`, `TRANSLATED_UNREVIEWED`, `REVIEWED`, or `STALE` per key/revision.
4. **QA plan is not QA execution** — `qa` and `qa-plan` return only
   `QA PLAN READY`. They never return `PASS`, `PASS WITH CONDITIONS`, a ship decision,
   or test evidence. Runtime execution and evidence review are separate activities.
5. **Freeze is hash-bound** — `ACTIVE` freezes one schema version, source locale,
   source-table byte hash, keyset hash, and per-key hashes. While active, catalog
   mutation is rejected by default. A warning or appended list is not permission to
   change the source table.
6. **Human high-impact decisions** — Automated cultural review produces
   `REVIEW CANDIDATE` findings only. It cannot decide market suitability, disputed
   territory treatment, legal/regulatory compliance, age/content rating, platform
   certification, or locale shipping approval.
7. **Evidence is immutable and scoped** — Any runtime or review claim is bound to
   exact locale, build ID and build SHA-256, platform/configuration, source freeze
   snapshot/hash, source-table hash, target-translation hash, and relevant
   font/package/asset hashes. A mismatch or missing hash makes evidence `STALE` or
   `PARTIAL`, never successful.
8. **Authorization is exact** — Read-only modes require no changeset prompt. Before a
   write, list exact normalized repository-relative paths, operation, unique writer,
   and preimage SHA-256 or `ABSENT`. Existing bounded authorization applies only when
   it covers that manifest. It does not authorize new paths, source-content changes,
   translations, human sign-off, external vendor communication, release state, or
   another subcommand.
9. **Evidence honesty** — Never invent or infer a translation, reviewer identity,
   human attestation, policy/legal conclusion, file hash, build, test run, screenshot,
   vendor receipt, or write result. Use `UNKNOWN`, `UNAVAILABLE`, `NOT RUN`,
   `UNVERIFIED`, `PARTIAL`, or `null`.
10. **No generic completion** — Catalog synchronization, static validation, QA
    planning, and evidence review have distinct verdicts. Never output
    `LOCALIZATION COMPLETE` or bare `COMPLETE`.

## Authority and artifact matrix

| Domain | Decision owner | Unique writer | May not do |
|---|---|---|---|
| source meaning in code/narrative/UI | source content owner | assigned developer/writer | claim target-locale quality |
| canonical source string table and schema | localization lead acting as catalog recorder | catalog recorder | change source meaning or target translation values |
| target-locale translation revision | named translator/vendor | that translation owner | approve its own revision as sole reviewer |
| locale language-quality review | locale-qualified human reviewer | review recorder only | silently edit translation or claim legal/platform authority |
| cultural suitability | local cultural consultant | review recorder only | make legal, rating, or market-release decisions |
| legal/regulatory or territory decision | named legal/compliance owner | governance recorder | delegate final decision to the model |
| platform/rating decision | named platform/rating owner | governance recorder | infer certification from static content |
| runtime localization QA | named QA tester | evidence recorder | claim translation authority |
| evidence integrity review | localization lead or QA evidence reviewer | optional evidence-report recorder | manufacture missing execution or sign-off |

An artifact has one writer per authorized transaction. Proposal agents are read-only.
When the localization-lead role is unavailable, the primary agent may perform its
catalog/coordination duties but must label the fallback and still cannot act as
translator, native reviewer, legal owner, platform owner, or QA tester.

## Canonical localization manifest

All table-aware modes read
`assets/data/strings/localization-manifest.yaml`. It declares:

```yaml
schema_version: <integer>
source_locale: <BCP-47 locale>
source_table:
  path: <repository-relative path>
  format: json | csv | po
  schema_version: <integer>
target_locales:
  <BCP-47 locale>:
    path: <repository-relative path>
    translation_owner_id: <stable human/vendor ID or null>
    reviewer_owner_id: <distinct stable reviewer ID or null>
fallback_chain: []
```

Normalize and validate every locale and path before reading. Paths must be
repository-relative, inside the workspace, unambiguous, and consistent with the
manifest. Unknown formats or schema versions are `BLOCKED — UNSUPPORTED SCHEMA`.
Malformed JSON/CSV/PO reports file, line/record, and parser detail and causes zero
writes.

`scan` may run without the manifest because it examines source only. Every other
table-aware mode requires the manifest. Do not default the source locale to English
and do not search alternate directories as a fallback.

For each successful load, record raw-byte SHA-256 for the manifest and every input.
Compute:

- `source_table_sha256` from exact source-table bytes;
- `keyset_sha256` from canonical sorted key IDs;
- per-key SHA-256 from canonical key ID, source value, context, placeholder schema,
  plural metadata, and source revision;
- `translation_sha256` from the exact target-locale file bytes.

Do not claim a hash for an unreadable or absent file.

## Subcommand side-effect and verdict table

| Subcommand | Side effect | Allowed verdicts |
|---|---|---|
| `scan` | read-only | `SCAN COMPLETE`, `SCAN PARTIAL`, `BLOCKED` |
| `extract` | may write only canonical source table through catalog recorder | `CATALOG DIFF READY`, `CATALOG UPDATED — TRANSLATIONS STALE`, `BLOCKED` |
| `validate` | read-only | `STATIC VALIDATION CLEAN`, `GAPS FOUND`, `PARTIAL`, `BLOCKED` |
| `status` | read-only | `STATUS READY`, `PARTIAL`, `BLOCKED` |
| `brief` | may write exact translator-brief path | `BRIEF READY`, `BLOCKED` |
| `cultural-review` | read-only unless an exact candidate-report path is authorized | `REVIEW CANDIDATES READY`, `NO CANDIDATES OBSERVED`, `PARTIAL` |
| `vo-pipeline scan/validate/integrate` | read-only | `VO STATIC REPORT READY`, `PARTIAL`, `BLOCKED` |
| `vo-pipeline script` | may write exact script paths | `VO SCRIPT DRAFT READY`, `BLOCKED` |
| `rtl-check` | read-only | `RTL STATIC CANDIDATES READY`, `PARTIAL` |
| `freeze call/lift` | may write only freeze record | `FREEZE ACTIVE`, `FREEZE LIFTED FOR CHANGE`, `BLOCKED` |
| `freeze status` | read-only | `FREEZE STATUS READY`, `BLOCKED` |
| `qa` / `qa-plan` | read-only unless exact plan-report paths are authorized | `QA PLAN READY`, `PARTIAL PLAN`, `BLOCKED` |
| `evidence-review` | read-only unless exact evidence-report paths are authorized | `QA EVIDENCE VERIFIED`, `QA EVIDENCE REJECTED`, `PARTIAL EVIDENCE`, `BLOCKED` |

No verdict in this table means release approval.

## Phase 0: Validate request, inputs, and authorization boundary

1. Parse exactly one subcommand and its required locale(s) or manifest path.
2. Canonicalize target locale tags without changing the manifest's identity mapping.
   Reject traversal, duplicate aliases, malformed tags, ambiguous files, directories,
   and paths outside the repository.
3. Load the localization manifest for table-aware modes, validate schema, and record
   its raw hash.
4. Load every required input completely. Record path, role, owner, raw-byte hash,
   parser result, and byte count.
5. If any required input is missing, unreadable, malformed, over a declared context
   budget, or inconsistent, return `PARTIAL` or `BLOCKED` and make no write.
6. For a mutating subcommand, build the complete write manifest before the first
   mutation. Obtain one authorization unless the current bounded request already
   covers exactly those paths and intended operations.
7. Before every authorized write, recheck all preimage hashes. After a successful
   write, report the actual raw-byte postimage hash. On mismatch, stop without
   overwriting.

File authorization never supplies a missing domain decision or owner attestation.

## Phase 1: Scan source — read-only

`scan` searches explicit project source roots for hardcoded player-facing strings,
unsafe concatenation, positional placeholders, locale-insensitive dates/numbers/
currency, embedded image text, LTR assumptions, and plural/gender assumptions.

Return file, line, observed code, rule, confidence, and source-file hash. Findings are
static candidates; they do not prove runtime rendering failure. Do not edit source,
source tables, or translation files.

## Phase 2: Extract and synchronize the source catalog

`extract` separates semantic source ownership from mechanical catalog recording:

1. Read localized references and their source-file hashes.
2. Strictly parse the canonical source table declared by the manifest.
3. Produce a deterministic diff of new, changed, and orphan candidates. Every new key
   includes context, source location, placeholders, plural metadata, and source owner.
4. Never invent source copy, change narrative/UI meaning, auto-translate, or edit a
   target-locale file.
5. Check the freeze record and its snapshot hashes before proposing any mutation.
6. Present the catalog diff, exact affected-key hash set, preimage hash, owner, and
   intended post-state.
7. Only the catalog recorder may apply an authorized source-table diff.

If freeze is `ACTIVE`, source-table bytes and key hashes must match the snapshot.
Reject every new or changed key with `BLOCKED — ACTIVE FREEZE`. Do not mutate and then
append a warning.

If an authorized catalog mutation succeeds, compute the new table/key hashes and mark:

- all evidence manifests bound to the old source-table hash as `STALE`; and
- every affected target-locale key as requiring translation or re-review.

Return `CATALOG UPDATED — TRANSLATIONS STALE`, not localization completion.

## Phase 3: Static translation validation and status

`validate` strictly parses the source table and each requested translation file.
Validate:

- missing or empty values;
- placeholder name/type/count parity;
- plural/select branches required by the locale;
- encoding and declared locale identity;
- source-revision and per-key source-hash bindings;
- orphaned target keys;
- `MT_DRAFT` or generated text markers;
- source-identical values lacking an explicit proper-noun/do-not-translate
  attestation;
- reviewer identity and reviewed translation hash, when claimed.

Character counts, source scanning, font file presence, or translation file existence
are static signals only. They cannot prove UI fit, glyph rendering, shaping, bidi,
line breaking, contextual naturalness, VO sync, or platform behavior.

Per key, use only:

- `UNTRANSLATED` — absent/empty/template value;
- `SOURCE_COPY_CANDIDATE` — equals source without a valid exemption;
- `MT_DRAFT` — machine/generated draft;
- `TRANSLATED_UNREVIEWED` — populated but no matching locale-review receipt;
- `REVIEWED` — distinct locale reviewer approved the exact translation hash;
- `STALE` — source/freeze/translation revision no longer matches.

`STATIC VALIDATION CLEAN` means only that parsers and static invariants passed. It is
not locale QA, runtime verification, cultural/legal approval, or release readiness.

`status` reports separate counts for populated, untranslated, stale,
translated-unreviewed, reviewed, and runtime-evidence-verified entries. Never combine
these into a single misleading “localized” percentage. An empty template or populated
unreviewed file cannot produce a completed-locale state.

This workflow may generate a proposed empty locale skeleton as a catalog transfer
artifact only when an exact path and `UNTRANSLATED TEMPLATE` status are authorized.
It never fills target values. Once delivered, only the named translation owner may
write target-locale values.

## Phase 4: Translator brief

`brief <locale>` requires a valid target locale and bounded explicit context: game
concept, tone, audience, glossary, source table, and directly linked narrative
sources. Record all hashes and stop with `PARTIAL` if required context is omitted.

The brief states the source snapshot, locale, schema, keyset hash, placeholder rules,
character-limit intent, glossary, do-not-translate attestations, delivery format, and
translation owner. Placeholder contacts remain `UNKNOWN` until a human supplies
them. The brief is not a translation and does not grant vendor communication or file
delivery permission.

Only the catalog/coordination recorder may write the exact authorized brief path.

## Phase 5: Cultural, regulatory, and platform review candidates

`cultural-review` may delegate read-only analysis to localization-lead, but its output
is a candidate register, not a market or compliance decision.

Each candidate records:

```yaml
id: L10N-CAND-<NNN>
locale_or_region: <exact scope>
category: culture | representation | territory | religion | legal | rating | platform
observed_content:
  path: <path>
  sha256: <hash>
  location: <line/key/asset>
risk_hypothesis: <why a human review may be needed>
required_owner: local-cultural-consultant | legal-compliance-owner | platform-rating-owner
status: NEEDS_HUMAN_REVIEW | RESOLVED | NOT_APPLICABLE
decision_receipt: <path-and-hash-or-null>
```

The model may prioritize review but does not declare content legally compliant,
certified, market-suitable, prohibited, or safe to ship. A candidate closes only when
the required human owner supplies identity, role/authority, exact locale/region,
content/source hashes, decision, rationale, UTC timestamp, and any expiry or
jurisdiction limit. A locale language reviewer cannot substitute for legal/platform
authority.

When authoritative current law, rating, platform, or territory evidence is absent,
return `NEEDS_HUMAN_REVIEW` or `UNKNOWN`. Do not fabricate rules from memory.

## Phase 6: VO and RTL static analysis

`vo-pipeline` always requires an explicit locale and bounded paths.

- `scan` identifies dialogue keys and candidate audio mappings.
- `script` produces recording-script drafts only; it does not synthesize, record,
  approve, or integrate audio.
- `validate` checks file/key/name/hash presence statically.
- `integrate` checks static references and file existence only.

Audio presence does not prove language accuracy, actor approval, pronunciation,
timing, lip sync, loudness, or in-build playback. Those require tester/studio receipts
bound to locale, build, source/translation hashes, audio asset hash, and test cases.

`rtl-check` produces static candidates for layout flags, string assembly, font assets,
and directional icons. It never labels runtime layout `PASS` or a static finding as a
final blocker. Actual fit, shaping, bidi, mirroring, glyph coverage, and mixed-script
behavior require build-bound screenshots/video/logs and locale-qualified review in
`evidence-review`.

## Phase 7: Hash-bound freeze state machine

The freeze record is `production/localization/freeze-status.yaml` with:

```yaml
schema_version: 1
state: UNFROZEN | ACTIVE | LIFTED_FOR_CHANGE
snapshot_id: <stable-id>
source_locale: <manifest source locale>
source_table_path: <exact path>
source_table_sha256: <raw-byte hash>
catalog_schema_version: <integer>
key_count: <integer>
keyset_sha256: <canonical sorted key hash>
key_hashes:
  <key>: <canonical per-key hash>
called_at_utc: <timestamp>
called_by:
  owner_id: <stable identity>
  authority: <source-freeze authority>
active_change_request: <id-or-null>
history: []
```

### Freeze call

Require a completely parsed source table and a stable, explicitly supplied approver
identity/authority. `Called by: user` or an inferred session identity is invalid.
Record the manifest/table/schema/key hashes and write the authorized record through
the freeze recorder. Re-read it and report its actual postwrite hash before returning
`FREEZE ACTIVE`.

If the current source bytes or per-key hashes later differ from the `ACTIVE` snapshot,
return `FREEZE VIOLATION / BLOCKED`. Do not update the snapshot automatically.

### Freeze lift

A lift requires an authorized change request:

```yaml
id: L10N-CR-<NNN>
owner_id: <stable source owner>
authority: <role/reference>
reason: <specific reason>
affected_keys:
  - key: <key>
    frozen_hash: <hash>
intended_change_hash: <hash-or-null>
retranslation_locales: []
vendor_notification_receipts:
  - locale: <locale>
    path: <receipt>
    sha256: <receipt-hash>
approved_at_utc: <timestamp>
```

Missing owner, affected-key hashes, retranslation scope, or required vendor receipt
blocks the lift. An authorized lift changes state to `LIFTED_FOR_CHANGE`; it does not
mutate the source table. After the catalog change, call freeze again to create a new
snapshot. The old snapshot and history remain immutable.

## Phase 8: QA planning only

`qa` and `qa-plan` create a per-locale execution plan. Split locales explicitly and
cap one plan at eight target locales; larger sets require separate batches. A missing
locale input is an error.

For every locale, the plan records:

- plan ID and plan document hash when written;
- exact locale and translation owner/reviewer IDs;
- intended build ID/hash/platform/configuration, or `UNKNOWN / NOT BUILT`;
- manifest, freeze snapshot, source table, keyset, translation, font/package, VO, and
  relevant asset hashes, using `null` when unavailable;
- test cases for functional strings, UI overflow, pseudolocalization, placeholders,
  plural/date/number/currency, input/IME, RTL/shaping where relevant, contextual
  language review, cultural candidates, VO/subtitle timing, accessibility,
  localization, and platform-specific text;
- required tester identity, evidence types, and expected results.

A plan may identify blockers or missing inputs, but it never executes a build, takes a
screenshot, reviews a translation as a native speaker, or returns `PASS`. Its only
successful verdict is `QA PLAN READY`. When any locale plan is incomplete, return
`PARTIAL PLAN` with per-locale gaps; do not fill them with guesses.

## Phase 9: Independent execution receipts and evidence review

QA execution happens outside `qa-plan` under a named QA tester and, for language
quality, a distinct locale-qualified reviewer. This workflow may review supplied
receipts through `evidence-review`; it does not manufacture or retroactively complete
them.

A runtime receipt contains:

```yaml
receipt_id: <stable-id>
test_case_id: <plan-case-id>
locale: <exact BCP-47 locale>
build_id: <build-id>
build_sha256: <build-hash>
platform: <platform-and-configuration>
manifest_sha256: <localization-manifest-hash>
freeze_snapshot_id: <snapshot-id>
freeze_record_sha256: <freeze-hash>
source_table_sha256: <source-hash>
keyset_sha256: <keyset-hash>
translation_path: <exact path>
translation_sha256: <translation-hash>
font_package_sha256: <hash-or-null>
vo_asset_set_sha256: <hash-or-null>
tester:
  owner_id: <stable identity>
  role: <QA role>
started_at_utc: <timestamp>
finished_at_utc: <timestamp>
actual_result: <observed result>
outcome: PASS | FAIL | BLOCKED | NOT_RUN
evidence:
  - path: <screenshot-video-log-path>
    sha256: <raw-byte-hash>
```

`evidence-review` verifies every receipt against one immutable evidence manifest and
recomputes all readable hashes. It also requires:

- a locale-qualified reviewer receipt for the exact translation hash;
- resolution receipts from the required human owner for every in-scope cultural,
  legal, rating, or platform candidate;
- complete required test-case coverage for the exact locale/build/platform;
- no `NOT_RUN`, `BLOCKED`, stale, unreadable, or mismatched required receipt.

Per locale, return only:

- `QA EVIDENCE VERIFIED` — all required receipts and owner decisions match;
- `QA EVIDENCE REJECTED` — at least one supplied receipt fails validation or records a
  failed test;
- `PARTIAL EVIDENCE` — required evidence is absent, unreadable, not run, blocked, or
  stale.

`QA EVIDENCE VERIFIED` confirms receipt integrity and coverage for that immutable
locale/build/source snapshot. It is not a release, legal, platform, or market
approval. Never convert it to `PASS` merely for compatibility with another skill.

## Phase 10: Output and next action

Return:

1. subcommand, operation status, mutation status, and exact scope;
2. source locale and requested target locales;
3. manifest/schema/freeze/source/keyset/translation/build hashes that actually exist;
4. input load counters, parse errors, stale reasons, and omitted evidence;
5. owner identities and missing-owner gaps;
6. exact writes with preimage/postimage hashes, or `READ_ONLY_NO_CHANGES`;
7. the subcommand-specific verdict from the contract table;
8. one next action that resolves the current gap.

Never auto-run another localization mode, contact a vendor, alter a translation,
close a human review candidate, update a release gate, or invoke deployment. Any
downstream gate must consume an immutable evidence manifest and independently verify
locale, build, source, translation, freeze, receipt hashes, freshness, and coverage.
