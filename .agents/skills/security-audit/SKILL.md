---
name: security-audit
description: Runs a bounded, strictly read-only security assessment with a version-bound threat scope, redacted evidence, versioned tool receipts, explicit unsupported and partial coverage, stable findings, and no security or release-approval claim.
---

# Security Audit

Assess one project snapshot without changing it. Establish the threat scope before
choosing checks, bind every claim to exact target/tool/rule/advisory evidence,
redact secret material, and fail closed when coverage is missing or unsupported.
This is not a penetration test, security certification, or ship/release approval.

## Invocation

Use this grammar exactly:

```text
$security-audit [full|network|save|input|quick]
                [--prior-review <project-relative-record-path>]
```

- No profile argument means `full`.
- Exactly one profile is allowed.
- `--prior-review` is optional, may appear once, and enables a re-audit against
  one immutable prior `cgs.security-audit/v2` record.
- Reject unknown/repeated/combined profiles, unknown options, missing option
  values, absolute/out-of-project/traversing paths, ambiguous roots, and an
  invalid or unrelated prior record with `ERROR` before scanning.

Valid outcomes are exactly:

```text
NO_FINDINGS_IN_SCANNED_SCOPE | FINDINGS | PARTIAL | ERROR
```

Never emit `SECURE`, `CLEAR TO SHIP`, `RELEASE READY`, or equivalent as an
outcome. A zero finding count describes only the exact completed scanned scope.

## Zero-write and secret-safe boundary

The allowed write set is empty. Do not write a report, cache, dependency, lockfile,
SBOM, advisory database, build, patch, waiver, finding state, checkpoint, status,
or session log. Do not install/update tools, fetch advisory data, build, package,
run the game, rotate credentials, delete secrets, rewrite history, or request
write permission for an ordinary audit.

Execute only commands proven non-mutating under the exact configured invocation.
Network access and any command that may download, update, cache, generate, build,
or persist output require separate authority and therefore are not performed by
this audit. Consume current immutable evidence when it exists; otherwise report
`UNVERIFIED` or `UNSUPPORTED`.

Never read a denied secret/environment source. Never place a credential value,
source line, surrounding context, length, encoding, reversible representation,
tool argument containing a secret, or volatile HMAC key in a prompt, reviewer
packet, finding, log excerpt, evidence record, or conversation. Use only the
secret-safe fields defined in the rules reference.

## Load the audit contract

Read [audit-rules-v1.md](references/audit-rules-v1.md) completely. It defines
profiles, fixed limits, threat scope, coverage states, tool/manual receipts,
engine/platform routing, reviewer policy, severity/confidence, stable finding
identity, risk boundaries, outcomes, and the evidence schema.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. If either contract file is missing, unreadable, or
internally inconsistent, return `ERROR` without an audit outcome claim.

## Establish target identity and mutation evidence

Resolve one canonical repository root. Record current commit/ref and dirty state
only from a successful read-only VCS receipt with executable/version/argv/cwd,
timestamps, exit status, and redacted output revision. If VCS identity is unavailable
but a meaningful source/build scope can still be identified, target identity is
`UNVERIFIED` and the maximum outcome is `PARTIAL`; otherwise return `ERROR`.

Create the before/after streaming mutation snapshots from the continued workflow
with an empty allowed-write set. A changed or incomplete snapshot invalidates
affected evidence and yields `PARTIAL` or `ERROR`. Report only secret-safe changed
paths; do not repair, revert, clean, stage, or attribute concurrent changes
without evidence.

## Freeze the threat scope before checks

Build one `cgs.security-threat-scope/v1` record from exact project evidence. It
must identify:

- configured engine, language, engine version, target platforms, build/export
  profiles, online/backend/platform services, mods/plugins, and supply chain;
- protected assets classified as public, local-sensitive, credential, player/PII,
  monetization, competitive/authority, or release-signing state;
- external actors and attacker capabilities;
- client, authoritative server, backend/service, platform API, local storage,
  mod/plugin, build/release, and third-party trust boundaries when applicable;
- entry points, authority/validation boundaries, sinks, and source→validator→sink
  flows; and
- abuse goals, assumptions, evidence paths/revisions, category applicability, and
  unresolved questions.

The profile matrix selects required categories, but evidence selects
applicability. A category is `NOT_APPLICABLE` only when current positive
configuration and threat-scope evidence prove it is out of scope. Missing files,
unconfigured engine/platform, or reviewer assumption is not N/A; use
`UNVERIFIED` or `UNSUPPORTED`.

revision the frozen normalized threat scope. If a required boundary, asset, authority,
entry point, or platform/engine identity cannot be established, preserve known
scope but return at most `PARTIAL`.

## Build bounded source, build, and component manifests

Enumerate only authorized project roots declared by current configuration and
applicable project rules. Record normalized path, type/language, size, revision,
category/reason, accessibility, and inclusion state for every candidate. Do not
follow links outside root. Exclude generated/vendor/binary/build content only with
current owner-approved classification evidence; keep each exclusion visible.

Apply the fixed file/depth/byte/component/check limits in the rules reference.
Denied, unreadable, oversized, parser-unsupported, adapter-unsupported, timed-out,
or over-limit required entries remain explicit coverage gaps. Never silently
sample, and never replace unsupported language/data-flow coverage with keyword
hits.

If no meaningful source, build, component, or target identity exists, return
`ERROR`. When at least one meaningful check runs but required scope is incomplete,
return `PARTIAL` even if confirmed findings exist.

## Route engine, platform, tools, and reviewers

Read and revision current technical preferences, engine-version reference, build/
export presets, platform declarations, and an owner-approved security adapter
registry when present. Route checks only through an adapter whose declared
engine/version/language/platform/category capabilities match the frozen threat
scope. Never infer a supported analyzer, platform behavior, server authority, or
secure-storage API from a filename or engine brand.

An absent/incompatible adapter is `UNSUPPORTED`, not N/A and not evidence of
safety. Engine/platform-specific manual checks use the exact configured Primary
or specialist routing only when its role and scope are declared. Do not invent a
Godot, Unity, Unreal, mobile, console, web, or backend specialist.

Deterministic scanning and coverage remain local. For `full`, `network`, `save`,
and `input`, one `security-engineer` review is required; a pre-dispatch unavailable
role may be performed locally under the repository's explicit fallback rule and
must emit the same target-bound manual-flow receipts. `quick` does not require a
reviewer. At most one configured engine/platform specialist may additionally be
required for unresolved platform semantics, for a total cap of two reviewers.

Dispatch required reviewers in one parallel batch with redacted, version-bound
packets and no raw secret/source context. Timeout, blocked, declined, error,
malformed output, target/threat-scope mismatch, unsafe output, or required role
overflow makes coverage `PARTIAL`. Reviewer prose is never scanner evidence and
cannot decide the outcome or accept risk.

## Require versioned evidence receipts

Every executed check uses `cgs.security-tool-receipt/v1`. Record executable,
tool/version, exact redacted argv, cwd, rulepack/config path and revision, adapter ID/
version, target subset revision, start/end time, deadline, exit/timeout, scanned/
excluded/unsupported counts and bytes, result revision, redacted log revision, and side
effect status.

Manual source→validator→sink review uses `cgs.security-manual-flow/v1` with exact
reviewer, target revisions, symbols/locations, trust/authority boundary, validation,
sink, reasoning, confidence, and timestamp. A keyword such as `load`, `token`,
`password`, `secret`, or `print` may identify a candidate but cannot create a
finding or no-findings claim without language-aware/source→sink evidence.

Unknown/missing tool or rule version, stale/incomplete input, incompatible
adapter, parser rejection, timeout, unexplained nonzero exit, zero eligible files,
unrevisionable result, unsafe secret output, or mutation yields `UNVERIFIED` or
`UNSUPPORTED`. Preserve successful independent evidence; never infer a pass.

Dependency advisories additionally require an exact versioned component inventory,
supported ecosystem matcher, immutable advisory snapshot ID/revision/timestamp,
freshness rule, version-range reasoning, and successful query receipt. Missing,
stale, offline, unsupported, or incomplete advisory evidence never becomes
“none” or “no known CVEs.”

## Normalize secret-safe stable findings

A finding must have concrete evidence, a stable identity/ID, exact target and
scope revisions, category and trust boundary, source→sink/authority path, confidence,
reproducible project severity, owner, containment, remediation, and a testable
closure condition. Findings begin `OPEN`.

Finding identity never includes a secret value/HMAC, title, prose wording, line
number, byte revision, timestamp, reviewer, confidence, or severity. Secret findings
use secret type plus a stable structural location. A per-run volatile HMAC may
correlate the same matched secret inside that run only; it is truncated, never
persisted as identity, and its key is destroyed without output.

Use `CGS-SEC-IEX/v1`, not an invented CVSS score, for project triage. Impact,
exploitability, and exposure have exact evidence-backed values; confidence is
separate and never raises severity. Multiplayer or public exposure changes only
the documented exposure factor and never blindly upgrades every HIGH finding to
CRITICAL. If any required factor is unsupported, severity is `UNRATED` and the
audit is `PARTIAL`.

For an external advisory, preserve the provider's exact CVSS version/vector/score
when supplied and label it advisory metadata. Do not fabricate missing CVSS,
convert the internal IEX score to CVSS, or treat advisory severity as proof of
project exploitability.

## Separate discovery, acceptance, persistence, and closure

This audit cannot patch, set `RESOLVED`, create an accepted-risk record, sign a
waiver, or persist its output. An existing risk acceptance affects neither
finding existence nor audit outcome unless an independent gate contract says how
to consume it. It is valid only with finding ID/identity, exact target/scope
revisions, authorized security/product owner, authority proof, rationale,
compensating controls, signed timestamp, expiry/review trigger, and audit
reference. The model, scanner, reviewer, recorder, or ordinary user acknowledgment
cannot self-accept risk.

Direct output is conversation-only `cgs.review-evidence/v1` with a
`cgs.security-audit/v2` extension. Always state:

```text
gate_evidence_status: NOT_PERSISTED
gate_evidence_eligible: false
NOT A SHIP/RELEASE APPROVAL
```

A separate recorder would need new exact authorization and must independently
revalidate redaction, record ID, target/scope/build/tool/advisory revisions, and
finding lifecycle. This workflow does not invoke it.

## Re-audit stable IDs and current attack surface

When `--prior-review` is supplied, validate its generic/extension schemas,
canonical record ID, immutable persistence identity, profile, target/scope revisions,
stable finding identities, evidence receipts, and relation to the current
project. Invalid or unrelated prior input is `ERROR`.

Evaluate every prior OPEN or owner-accepted-risk finding first against its exact
closure condition, then inspect the exact prior→current diff and changed trust/
authority/data flows for regressions and new attack surface. Reuse stable IDs for
unchanged identities and record `STILL_OPEN`, `CANDIDATE_RESOLVED`, `REGRESSED`,
`SUPERSEDED`, or `UNVERIFIED`. The auditor never mutates lifecycle state.

Missing prior bytes/diff/current evidence makes re-audit coverage `PARTIAL`.
A quick re-audit remains quick: it cannot close a full finding set, replace a
full current audit, or satisfy a future release-security gate. Only a full current
profile can produce full-profile evidence, still subject to separate persistence
and lifecycle authority.

## Coverage and outcome

Each required category is exactly one of:

```text
CHECKED_WITH_FINDINGS | CHECKED_NO_FINDINGS | NOT_APPLICABLE |
UNVERIFIED | UNSUPPORTED
```

Apply outcome precedence:

1. Invalid identity/scope or no meaningful check -> `ERROR`.
2. At least one meaningful check plus any required `UNVERIFIED`/`UNSUPPORTED`,
   unchecked file/flow/component, failed tool/reviewer, unsafe redaction, target
   change, or incomplete mutation/re-audit evidence -> `PARTIAL`.
3. Complete required scope plus one or more findings -> `FINDINGS`.
4. Complete required scope and zero findings ->
   `NO_FINDINGS_IN_SCANNED_SCOPE`.

Under `PARTIAL`, preserve confirmed findings and explicitly say which required
scope remains unknown. Never convert uncertainty into a vulnerability merely to
sound conservative.

## Return and stop

Return the complete envelope defined in the rules reference: target/build/source/
threat-scope revisions, bounded manifests, engine/platform/adapter routing, coverage,
tool and manual receipts, redacted stable findings, advisory evidence, reviewer
plan/results, risk references, re-audit dispositions, mutation guard, outcome,
and stale key.

For a suspected live credential, expose only secret type, normalized allowed path,
line/column, structural anchor, rule/tool ID, target revision, confidence, and volatile
truncated HMAC. Recommend immediate revoke/rotate, restricted distribution, and
authorized history/log inspection, but do not perform them.

Provide evidence-bound containment/remediation ownership and stop. Never write a
report, invoke remediation, self-accept risk, claim a finding closed, or present
this audit as release approval.
