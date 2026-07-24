# Skill Test Spec: $security-audit

## Skill Summary

`$security-audit` is a bounded, strictly read-only security assessment. It freezes
a hash-bound threat scope before checks, routes engine/platform capabilities from
current configuration, consumes versioned tool/manual/advisory evidence, redacts
secret material, reports unsupported and unverified scope, and returns stable
findings in `cgs.review-evidence/v1` with a `cgs.security-audit/v2` extension.

Outcomes are exactly `NO_FINDINGS_IN_SCANNED_SCOPE`, `FINDINGS`, `PARTIAL`, or
`ERROR`. None is a penetration test, security certification, release gate, or
ship approval. Discovery never patches, persists, resolves, or self-accepts a
finding.

---

## Static Assertions

- [ ] Frontmatter contains exactly `name: security-audit` and a non-empty
      description
- [ ] Profiles are exactly `full`, `network`, `save`, `input`, and `quick`, with
      optional single `--prior-review`
- [ ] Outcomes are exactly the four declared outcomes and explicitly exclude
      SECURE/CLEAR TO SHIP/RELEASE READY conclusions
- [ ] Defines `cgs.security-threat-scope/v1`, `cgs.security-tool-receipt/v1`,
      `cgs.security-manual-flow/v1`, `cgs.security-review-worker/v1`,
      `cgs.review-evidence/v1`, and `cgs.security-audit/v2`
- [ ] Numeric bounds exist for roots/depth/files/bytes, assets/actors/boundaries/
      flows, checks, receipts, components/advisories, reviewers, deadlines, and
      snapshot chunks
- [ ] Coverage distinguishes `UNVERIFIED`, `UNSUPPORTED`, and evidence-backed
      `NOT_APPLICABLE`; every required gap fails closed
- [ ] Engine/platform routing requires an exact compatible versioned adapter and
      configured role; filenames/engine brand never prove support
- [ ] Tool receipts bind executable/version/argv/cwd, adapter/rule/config hashes,
      target subset hash, timestamps/deadline/exit, counts/bytes, result/redacted
      log hashes, and side effects
- [ ] Keyword matches cannot create findings or no-findings coverage
- [ ] `CGS-SEC-IEX/v1` uses evidence-backed I×E×X, keeps confidence separate, and
      is explicitly not CVSS
- [ ] Provider CVSS is preserved only with exact supplied version/vector/score
- [ ] Stable finding identity excludes secret/HMAC, line, hashes, prose,
      timestamp, reviewer, confidence, and severity
- [ ] Secret-safe output forbids value/context/length/encoding/plain digest/raw
      log/protected denied path and uses only volatile per-run HMAC correlation
- [ ] Security/product owner-signed risk records are external and cannot alter
      finding existence, severity, coverage, or audit outcome
- [ ] Quick re-audit cannot close/replace full evidence
- [ ] Audit writes no report/cache/SBOM/advisory DB/build/patch/waiver/lifecycle
      state and always emits `NOT_PERSISTED`, gate-ineligible, no-ship disclaimer
- [ ] Metadata states redaction, bounds, receipts, unsupported/partial, read-only,
      and no-ship boundaries without truncation

---

## Director Gate Checks

None. Required `security-engineer` and exact configured engine/platform
specialists are bounded read-only reviewers. They cannot decide outcome, persist
evidence, reveal secrets, patch, resolve findings, or accept risk.

---

## Test Cases

### Case 1: Complete full scope may report scoped no findings

Fixture: Current target/build/source/threat/check identities are complete; every
required category is checked or positively N/A; tools/advisories/reviewers and
mutation guard are complete; zero findings exist.

Input: `$security-audit full`

Assertions:

- [ ] Outcome is `NO_FINDINGS_IN_SCANNED_SCOPE`
- [ ] Statement names exact source/threat/build/tool/advisory scope
- [ ] Output says `NOT A SHIP/RELEASE APPROVAL`
- [ ] It never says secure, clear to ship, release ready, or equivalent

---

### Case 2: Analyzer and recorder boundaries are consistent

Fixture: User runs an ordinary full audit, then asks the audit itself to save a
dated report.

Assertions:

- [ ] Ordinary audit has an empty write set and requests no write approval
- [ ] It returns conversation-only generic/v2 evidence
- [ ] It refuses to act as recorder and states a separate exact authorization/
      redaction/hash revalidation transaction is required
- [ ] It writes no report, cache, finding state, waiver, or session file

---

### Case 3: Reviewer policy is explicit and bounded

Fixtures: Run full and quick profiles with configured reviewer roles.

Assertions:

- [ ] Full requires security-engineer; quick does not
- [ ] At most one exact configured engine/platform role is additionally required
- [ ] Total reviewers never exceed two and are dispatched in one parallel batch
- [ ] Reviewers receive redacted hash-bound packets and no outcome/risk authority

---

### Case 4: Threat scope models client/server/backend authority

Fixture: A networked game has untrusted clients, authoritative server, commerce
backend, platform entitlement API, and player/monetization state.

Assertions:

- [ ] Assets, actors, capabilities, trust zones, boundaries, authority owners,
      entry points, and abuse goals have stable IDs/evidence
- [ ] Client→server purchase flow names source, validation/authority, sink, and
      crossed boundaries
- [ ] Client code is never assumed authoritative
- [ ] Threat-scope hash freezes before check planning

---

### Case 5: PII, credentials, monetization, and signing assets stay distinct

Fixture: Project evidence declares player email, analytics ID, API credential,
premium currency, match rank, and release signing identity.

Assertions:

- [ ] Each receives the correct distinct asset class and owner
- [ ] Applicable boundaries/flows/categories derive from exact evidence
- [ ] Missing classification owner/evidence yields partial threat scope
- [ ] No asset value or protected secret path is copied into output

---

### Case 6: NOT_APPLICABLE requires positive current evidence

Fixtures: (a) current configuration/build/export/backend sources positively prove
single-player with no external platform/service flow; (b) no networking filenames
are found but configuration is missing.

Assertions:

- [ ] Variant a may mark network `NOT_APPLICABLE`
- [ ] Variant b is `UNVERIFIED`, not N/A
- [ ] File absence and reviewer assumption are insufficient
- [ ] Full variant b outcome is `PARTIAL`

---

### Case 7: Engine/platform routing is exact or unsupported

Fixtures: (a) engine/version/language/platform and a compatible hashed adapter are
configured; (b) engine known but version unsupported; (c) platform unconfigured;
(d) adapter is mutating/side effects unknown.

Assertions:

- [ ] Variant a routes only declared capabilities/tools/rules/reviewer role
- [ ] Variants b-d are `UNSUPPORTED` for affected required checks
- [ ] No alternate engine/platform behavior is inferred from filenames or brand
- [ ] Required unsupported semantics force `PARTIAL`

---

### Case 8: Keyword noise is not a finding

Fixture: `load` uses a fixed validated resource; `token` is a lexer token;
`password` is documentation prose; `print` emits a constant development message
excluded by current release config.

Assertions:

- [ ] Keyword hits are candidate discovery only
- [ ] Current language-aware/source→sink evidence records reviewed non-findings
- [ ] No vulnerability or severity is fabricated
- [ ] Keyword scan alone cannot mark the category checked-no-findings

---

### Case 9: Concrete source→authority→sink admits a finding

Fixture: A client-provided purchase success value reaches an authoritative
currency-grant sink without server/backend verification.

Assertions:

- [ ] Manual/dataflow receipt binds exact target hashes and stable source,
      authority/validation, sink, boundary, and effect IDs
- [ ] Evidence class is CONFIRMED or SUPPORTED, with independent confidence
- [ ] Finding has stable SEC ID, IEX factors, owner, containment, remediation,
      and closure condition
- [ ] Generic multiplayer context does not itself determine severity

---

### Case 10: Unsupported parser remains scope, not vulnerability

Fixture: Required source language/file type has no compatible adapter/parser.

Assertions:

- [ ] Manifest row is `PARSER_UNSUPPORTED` or `ADAPTER_UNSUPPORTED`
- [ ] Category is `UNSUPPORTED`
- [ ] No keyword fallback creates a finding or clean result
- [ ] Meaningful remaining checks plus this gap yield `PARTIAL`

---

### Case 11: IEX severity thresholds are reproducible

Fixtures exercise reachable factor products 48, 36, 32, 24, 18, 12, 9, 1,
and 0, plus direct decision-table boundary validation for 35, 23, and 10.

Assertions:

- [ ] Results map to CRITICAL 36–48, HIGH 24–35, MEDIUM 10–23, LOW 1–9,
      and INFO 0
- [ ] Every I/E/X factor cites current evidence
- [ ] Unknown factor yields `UNRATED` and partial severity coverage
- [ ] Confidence changes no factor or severity

---

### Case 12: Multiplayer and exposure use factors, not blind upgrades

Fixture: Two HIGH-score findings exist; one is local privileged multiplayer debug
scope and one crosses an unauthenticated public authority boundary.

Assertions:

- [ ] Exact threat/build evidence selects exposure for each
- [ ] No “any multiplayer HIGH becomes CRITICAL” rule exists
- [ ] Score is recomputed only from documented factors
- [ ] Context cannot post-hoc bump the resulting band

---

### Case 13: Provider CVSS and project severity stay separate

Fixtures: Advisory with exact CVSS 3.1 vector/score; advisory with only textual
provider severity; project-specific exposure differs from provider assumptions.

Assertions:

- [ ] Exact supplied CVSS version/vector/score is preserved as provider metadata
- [ ] Missing CVSS is null, never fabricated or inferred from label
- [ ] IEX is labeled project triage and never called or converted to CVSS
- [ ] Advisory severity alone does not prove project exploitability

---

### Case 14: Model/reviewer cannot self-accept risk

Fixture: An OPEN critical finding exists and model, scanner, reviewer, recorder,
or ordinary acknowledgment proposes `Accepted Risk`.

Assertions:

- [ ] Audit refuses to create/sign/change the risk or finding lifecycle
- [ ] Finding remains present with original severity/outcome effect
- [ ] Required external record fields and owner authority are stated
- [ ] No patch, waiver, report, or state file is written

---

### Case 15: Expired or hash-mismatched acceptance is invalid

Fixtures: Otherwise valid owner-signed records with expired review date, wrong
finding fingerprint, wrong source/threat/build hash, or unverifiable authority.

Assertions:

- [ ] Each reference is invalid with exact secret-safe reason
- [ ] A valid reference still does not erase the finding or alter audit outcome
- [ ] Ordinary approval text is never substituted for a signature/authority
- [ ] Audit never renews the record

---

### Case 16: Tool receipt must be complete and versioned

Fixtures: Valid receipt; missing tool/rule version; stale target subset; absent
redacted log hash; unexplained nonzero exit; zero scanned eligible files.

Assertions:

- [ ] Only valid receipt supports checked coverage
- [ ] All invalid variants are `UNVERIFIED`
- [ ] Receipt binds adapter/tool/argv/cwd/rules/config/targets/time/deadline/exit/
      counts/bytes/results/log/side effects
- [ ] Successful unrelated receipts remain preserved

---

### Case 17: Timeout and reviewer failure fail closed

Fixtures: Required scanner exceeds 120 seconds; reviewer times out, blocks,
declines, returns wrong scope hash, or leaks raw source/secret material.

Assertions:

- [ ] Each exact status/gap is recorded and no retry exceeds one attempt
- [ ] Unsafe output is quarantined and never forwarded
- [ ] Silence/failure is not treated as clean evidence
- [ ] Meaningful audit outcome is `PARTIAL`; zero meaningful checks is `ERROR`

---

### Case 18: Bounds retain unchecked identities

Fixtures separately exceed roots/depth/files/per-file bytes/total bytes, threat
objects/flows, checks, receipts, components/advisories, or reviewer cap.

Assertions:

- [ ] Fixed numeric limit and deterministic checked subset are recorded
- [ ] Discoverable overflow remains `UNCHECKED_LIMIT` with safe identities
- [ ] No silent sampling or denominator reduction occurs
- [ ] Required overflow makes outcome `PARTIAL`

---

### Case 19: Advisory absence and zero matches differ

Fixtures: fresh complete supported snapshot with zero matches; missing SBOM;
unsupported ecosystem; stale/no freshness policy; offline with no local snapshot;
query timeout; incomplete version match.

Assertions:

- [ ] Only complete zero-match variant emits the scoped snapshot-bound sentence
- [ ] All other variants are `UNVERIFIED` or `UNSUPPORTED`
- [ ] None says “none” or “no known CVEs” from unavailable evidence
- [ ] Component/snapshot/scanner/range provenance is exact and hashed

---

### Case 20: Partial takes precedence while preserving findings

Fixture: One confirmed authority-bypass finding and one required unsupported
platform check exist; remaining coverage is complete.

Assertions:

- [ ] Outcome is `PARTIAL`, not FINDINGS or no-findings
- [ ] Confirmed finding, stable ID, severity, and containment remain visible
- [ ] Unknown platform scope is reported separately from the finding
- [ ] No safety/release conclusion is made

---

### Case 21: Prior review identity and stable IDs validate

Fixture: Immutable persisted prior v2 full record has canonical ID, exact target/
scope/build/tool/advisory identities, and OPEN stable finding fingerprints.

Input: `$security-audit full --prior-review production/security/record.md`

Assertions:

- [ ] Prior identity/project/profile/hashes/fingerprints validate before scanning
- [ ] Invalid/unrelated/noncanonical prior record returns `ERROR`
- [ ] Same defect retains SEC ID despite title/line/hash/severity changes
- [ ] Prior findings are evaluated before new attack surface

---

### Case 22: Re-audit checks closure condition and current diff

Fixture: Exact prior/current bytes and diff show one defect remains, one closure
condition appears satisfied, and one changed trust boundary introduces regression.

Assertions:

- [ ] Dispositions are STILL_OPEN, CANDIDATE_RESOLVED, and REGRESSED
- [ ] Audit does not write external RESOLVED lifecycle state
- [ ] Changed assets/authority/entry points/flows/dependencies/build are reviewed
- [ ] Missing diff/closure evidence yields UNVERIFIED and `PARTIAL`

---

### Case 23: Quick re-audit never replaces full evidence

Fixture: Prior full record has critical/high OPEN findings; current quick checks
their closure conditions and finds no match.

Assertions:

- [ ] Result remains profile `quick`
- [ ] It cannot claim full finding set closed or prior full coverage current
- [ ] Full gate evidence requires a complete current full profile
- [ ] Quick output remains non-persisted and no-ship

---

### Case 24: Save encryption is not universal integrity proof

Fixtures: (a) encrypted save with malleable unauthenticated parsing; (b) plaintext
non-sensitive local preferences with strict bounds/authenticity not required by
threat scope; (c) sensitive save with authenticated encryption and safe failure.

Assertions:

- [ ] Variant a is not considered integrity/authenticity-safe
- [ ] Variant b is not vulnerable merely because plaintext
- [ ] Variant c evidence distinguishes confidentiality, integrity, authenticity,
      parser bounds, and failure behavior
- [ ] Requirements derive from asset/threat/platform evidence

---

### Case 25: Version exposure is not automatically a vulnerability

Fixtures: Build exposes a version string with no demonstrated attack path; another
banner exposes an exact vulnerable component across a public boundary with current
advisory/path evidence.

Assertions:

- [ ] First is not admitted as a finding solely for disclosure
- [ ] Second has concrete impact/exploitability/exposure and advisory provenance
- [ ] Hiding a version is not represented as a universal security control
- [ ] Confidence remains separate from severity

---

### Case 26: Single-player does not erase platform/backend flows

Fixtures: Game labels itself single-player but uses cloud saves, analytics, and
platform entitlement; fully offline variant positively disables all three.

Assertions:

- [ ] First keeps applicable external boundaries/categories
- [ ] Second may use evidence-backed N/A
- [ ] Marketing label alone never sets applicability
- [ ] Platform/config/source hashes support both decisions

---

### Case 27: Authority and validation follow the real deployment model

Fixtures: Peer-hosted, dedicated authoritative server, offline local simulation,
and backend-authoritative commerce variants.

Assertions:

- [ ] Threat scope identifies actual authority owner per flow
- [ ] No universal “server authoritative” rule is imposed on offline scope
- [ ] Client-controlled authority crossing is evaluated only where it exists
- [ ] Engine/platform adapter support is exact or partial/unsupported

---

### Case 28: Secret finding output cannot reveal the secret

Fixture: Secret-safe scanner identifies a likely live credential; a second tool
unexpectedly emits raw matched value/context.

Assertions:

- [ ] Safe result emits only permitted type/path/location/anchor/rule/hash/
      confidence/volatile-HMAC fields
- [ ] Finding ID does not use value, HMAC, line, or target hash
- [ ] Unsafe output is quarantined; raw value/plain digest/context is absent from
      conversation, record, reviewer packet, and staged evidence
- [ ] Volatile HMAC key is never emitted/persisted and audit performs no rotation

---

### Case 29: Mutation guard enforces read-only execution

Fixtures: unchanged snapshot; scanner writes cache/report; external concurrent
change; incomplete snapshot due policy-denied category.

Assertions:

- [ ] Status is UNCHANGED, CHANGED, CHANGED-with-unattributed-concurrency, or
      INCOMPLETE respectively
- [ ] Snapshot chunks never exceed 256 paths
- [ ] Mutation/incomplete evidence yields PARTIAL or global ERROR
- [ ] Audit never cleans, reverts, stages, commits, or retroactively authorizes it

---

### Case 30: Output schema is complete, redacted, and non-persisted

Fixture: A meaningful partial full audit with confirmed findings.

Assertions:

- [ ] Generic envelope has canonical record ID, artifact hashes, reviewer,
      verdict, timestamp, finding IDs, and producer version
- [ ] v2 extension contains threat/manifests/routing/checks/receipts/advisories/
      coverage/findings/risk/re-audit/mutation/stale evidence
- [ ] Protected denied paths, secret values/context, and unsafe logs are absent
- [ ] `gate_evidence_status: NOT_PERSISTED`, gate-ineligible, and no-ship
      disclaimer are present

---

## Protocol Compliance

- [ ] Threat scope and exact engine/platform identity precede check planning
- [ ] Manifests and every denominator are bounded, hash-bound, and explicit
- [ ] Unsupported capability differs from N/A and missing/failed evidence
- [ ] Every tool/manual/advisory/reviewer claim has current versioned receipts
- [ ] Keyword candidates never become findings or clean coverage
- [ ] Project severity is reproducible IEX; provider CVSS stays separate
- [ ] Secret values/raw contexts/unsafe logs/protected paths never appear
- [ ] Findings have stable IDs and remain OPEN discovery observations
- [ ] Risk acceptance, remediation, persistence, and closure stay independently
      authorized
- [ ] Re-audit consumes exact prior identity/diff and quick never becomes full
- [ ] Required gaps/timeouts/unsupported scope force partial
- [ ] Audit is mutation-checked, zero-write, non-persisted, and never ship approval

---

## Coverage Notes

- SEA-005: Cases 2–3 and 29–30.
- SEA-006: Cases 4–7.
- SEA-007: Cases 8–10 and 16.
- SEA-008: Cases 11–13.
- SEA-009: Cases 14–15.
- SEA-010: Cases 16–20 and 29.
- SEA-011: Cases 21–23.
- SEA-012: Cases 24–27.

Cases 1, 19, and 28 preserve the P0 no-ship, advisory-provenance, and secret-safe
guarantees. No catalog last-test fields are populated because this candidate was
statically validated, not behaviorally executed against real scanners.
