---
name: security-audit
description: "Run a bounded, read-only, evidence-bound security assessment with redacted findings, explicit coverage gaps, traceable advisory data, and no ship-approval claim."
---

## Invocation and execution

Invoke this workflow as `$security-audit [full|network|save|input|quick]`.

No argument means `full`. Reject unknown, repeated, or combined profiles with
`ERROR` before scanning. The workflow is read-only: it may execute approved
non-mutating inspection/scanner commands, but it never writes a report, cache,
dependency, build output, remediation, or risk acceptance.

Valid outcomes are exactly:

- `NO_FINDINGS_IN_SCANNED_SCOPE`;
- `FINDINGS`;
- `PARTIAL`; or
- `ERROR`.

These outcomes are not a penetration test, proof of security, certification, or
release/ship approval.

---

## Phase 0: Establish authority and mutation boundary

Before scanning:

1. Resolve one workspace root and reject paths outside it, unresolved symlinks,
   traversal, or ambiguous roots.
2. Record the requested profile and its category matrix.
3. Read applicable `AGENTS.md` and security/tooling instructions.
4. Record current VCS identity using an actually executed read-only command:
   commit/ref, dirty-state evidence, command, working directory, tool/version,
   timestamps, exit code, and raw output hash. If VCS identity cannot be
   established, mark target identity `UNVERIFIED`.
5. Identify engine/language, target platforms, configured online/backend
   features, release build configuration, export/package presets, and relevant
   data classifications from explicit sources and raw hashes.
6. Snapshot a read-only pre-audit workspace manifest for mutation detection.

Do not install tools, update advisory databases, fetch dependencies, create
scanner caches in the workspace, build the project, or use network access unless
the user separately authorizes that side effect. Lack of permission or tooling
is a coverage gap, never evidence of absence.

All security-engineer or specialist delegations are read-only. Their prose is
not scan evidence. Every claim must trace to an executed command, a manually
reviewed source/sink path, or an immutable supplied artifact.

---

## Phase 1: Build a threat model and exact scope manifest

Define trust boundaries before choosing checks:

- client, authoritative server, backend/service, platform APIs, local storage,
  mod/plugin boundary, build/release pipeline, and third-party supply chain;
- assets/data classified as public, local-sensitive, credential, player/PII, or
  monetization/competitive state;
- attacker capabilities and applicable abuse goals; and
- source → validation/authority boundary → sink flows.

For each profile declare required categories:

| Profile | Required categories |
|---|---|
| full | save/serialization, network when configured, input, exposure/secrets, cheat/authority, dependency/supply chain, build/release |
| network | network authority/authentication/validation/rate limits, exposure/secrets, relevant dependencies and release config |
| save | save/serialization, path handling, integrity/authenticity, local secret/PII exposure |
| input | player/external input sources through validators to file/log/network/backend/dynamic-code sinks |
| quick | explicitly enumerated high-confidence checks only; never full/release evidence |

A category may be `NOT_APPLICABLE` only with positive evidence, such as a hashed
project configuration proving no online feature. File-name absence or an agent's
assumption is insufficient; otherwise use `UNVERIFIED`.

Enumerate the exact allowlisted files before scanning. Record normalized path,
raw hash, byte size, language/type, category, inclusion reason, and accessibility.
Exclude binary/generated/vendor paths only by explicit rule and list them.
Denied, unreadable, oversized, parser-unsupported, timeout, or outside-root files
remain coverage gaps. Never bypass a platform/project denial or read denied
secret/environment files; record only a category-level permission gap without
revealing a protected path or value. Never silently sample or substitute keyword hits for full
coverage.

Freeze:

- target commit/ref and dirty state;
- canonical source-scope manifest hash;
- relevant build/export configuration hashes;
- supplied binary/build hash, if one actually exists; and
- threat-model hash.

If no meaningful target identity or no eligible source/build evidence can be
established, return ERROR. If some checks can run but any required category,
build configuration, or in-scope file remains unverified, the maximum outcome is
PARTIAL.

---

## Phase 2: Execute evidence-producing checks

Use language-aware SAST, dependency/SBOM scanners, build-configuration
inspection, and manual source→validator→sink review appropriate to the declared
engine/language. A keyword search may locate candidates but cannot by itself
create a vulnerability finding or a no-findings claim.

Before each command, record:

- stable check ID and category;
- exact executable and argument vector, without secret values;
- working directory;
- scanner/tool version;
- rulepack/config path and raw hash;
- target paths and manifest subset hash;
- expected side effects and deadline.

After execution, record:

- start/end ISO-8601 timestamps;
- exit code or timeout;
- eligible, scanned, excluded, failed, and parser-unsupported file counts/bytes;
- raw stdout/stderr hash and separately redacted-output hash;
- produced scanner result/SBOM hash, if supplied without workspace mutation; and
- PASS/FAIL/PARTIAL/ERROR execution state.

A command that was not run, timed out, returned an unexplained nonzero exit,
scanned zero eligible files, used an unknown rulepack, mutated the workspace, or
lacks a log hash is not passing evidence. Mark its coverage `UNVERIFIED` and fail
closed.

Manual review evidence must name reviewer/role, exact files and raw hashes,
source and sink symbols/locations, validation or authority boundary inspected,
reasoning, timestamp, and confidence. Do not report generic keywords such as
`load`, `token`, or `print(` as vulnerabilities without a concrete data flow and
impact.

For build/runtime claims, inspect only an existing identified build or run an
explicitly authorized build/test command. Record the build command, exit code,
config/preset hashes, artifact hash, platform, and log hash. If no current build
evidence exists, label build/runtime behavior `UNVERIFIED`; source inspection
cannot prove release-build behavior.

Use a finite deadline per command and delegation. On timeout, stop that check,
record it, and continue only with independent checks. Never retry indefinitely.
A required timed-out check makes the overall outcome PARTIAL or ERROR.

---

## Phase 3: Dependency and advisory evidence

Create the component inventory only from actual hashed lockfiles, package
manifests, vendor metadata, or an SBOM produced by an executed tool. Each
component record needs name, exact version or digest, source path/hash, ecosystem,
and match confidence.

A CVE/advisory result is valid only when it records:

- scanner/provider and version;
- advisory database or snapshot identifier, timestamp, and immutable hash;
- exact query/scan command, timestamps, exit code, and log hash;
- component-to-advisory match key and version-range reasoning; and
- the project's explicit freshness policy and whether the snapshot satisfies it.
  If no freshness policy exists, advisory freshness is UNVERIFIED.

If there is no lockfile/SBOM, no supported ecosystem, no advisory snapshot,
stale or unhashable data, denied network, timeout, or incomplete component match,
set dependency vulnerability status to `UNVERIFIED`. Never write `none`,
`no known CVEs`, or equivalent from missing/untraceable evidence.

When a complete, supported, fresh snapshot returns no matches, state only:
`No advisories matched the inventoried components in [snapshot ID/hash] at
[time].` This is scoped historical evidence, not proof that dependencies are
safe.

---

## Phase 4: Secret-safe detection and reporting

Configure secret scanning so the command itself does not print matched values or
surrounding source lines. Never echo, quote, store, summarize, or place a secret
value in a prompt, finding, log excerpt, report, checkpoint, or tool argument.

For a suspected credential, record only:

- stable finding ID and secret type;
- normalized path and line/column;
- rule/scanner ID and source file raw hash;
- a truncated HMAC-SHA-256 fingerprint made with a per-run volatile key that is
  never printed or persisted;
- validation state and confidence; and
- required containment action.

Do not record matched length or reversible encodings. Hash raw scanner output in
memory before redaction; expose only the raw-log hash and a redacted log/result.
If a tool cannot provide secret-safe output, do not display/persist its raw
output and mark the evidence-handling check PARTIAL.

A likely real credential triggers an immediate recommendation to revoke/rotate
it, inspect repository history and downstream logs, and restrict further
distribution. This skill does not rotate, delete, rewrite history, or patch it.

---

## Phase 5: Normalize findings and coverage

A finding requires concrete evidence. Record:

- stable ID derived from rule ID plus normalized source/sink symbol and path
  fingerprint—not title text;
- target commit/dirty-state, source manifest hash, build hash when applicable,
  tool/rule/snapshot evidence IDs, and timestamp;
- category, affected trust boundary, source→sink or authority path;
- impact, exploitability, exposure, confidence, and reproducible severity;
- redacted locations and evidence;
- initial state `OPEN`; and
- recommended containment/remediation owner and testable closure condition.

Do not mark findings RESOLVED or ACCEPTED RISK in discovery. Remediation is a
separate, explicitly authorized implementation task. Risk acceptance is a
separate owner decision and must contain finding ID, exact target/scope hash,
approver identity/authority, rationale, compensating controls, expiry/review
date, and signature/audit reference. The model, analyzer, reviewer, or recorder
cannot self-accept risk.

Use a coverage matrix for every required category:

| State | Meaning |
|---|---|
| CHECKED_WITH_FINDINGS | required evidence executed and findings exist |
| CHECKED_NO_FINDINGS | required evidence executed and no findings in that exact scope |
| UNVERIFIED | missing/failed/stale/unsupported/unauthorized evidence |
| NOT_APPLICABLE | positive evidence proves category outside the threat model |

Determine overall outcome in this order:

1. `ERROR` — no meaningful scan ran, target/scope identity is invalid, or
   evidence integrity failed globally.
2. `PARTIAL` — at least one meaningful check ran but any required category,
   file, build/config, advisory source, command, or evidence field is UNVERIFIED;
   also report whether confirmed findings exist.
3. `FINDINGS` — required scope is complete and one or more findings exist.
4. `NO_FINDINGS_IN_SCANNED_SCOPE` — required scope is complete and no findings
   exist.

Never convert uncertainty into a vulnerability merely to be conservative.
Record it as a coverage gap.

---

## Phase 6: Return a redacted read-only evidence packet

Return in conversation only:

1. outcome plus `NOT A SHIP/RELEASE APPROVAL`;
2. target commit/ref, dirty state, source/build/threat-model hashes;
3. profile and exact included/excluded/failed scope;
4. coverage matrix;
5. executed command/manual-review evidence table;
6. redacted findings and stable IDs;
7. dependency/advisory snapshot evidence or UNVERIFIED reason;
8. build/runtime evidence or UNVERIFIED reason;
9. mutation check comparing pre/post workspace manifests;
10. remediation-owner handoffs and separate risk-decision requirements; and
11. exact re-audit scope.

Do not write `production/security/` or any other project file. Do not ask for a
write approval because this skill has no write set. If the user separately asks
to persist the packet, stop and route it to a recorder workflow with a new exact
path/content/hash authorization and secret-safe review. That recorder action is
outside this audit.

A post-audit workspace-manifest difference not explained by external concurrent
work is an evidence-integrity failure. Report ERROR or PARTIAL and list redacted
changed paths; never silently accept scanner side effects.

---

## Release and re-audit boundaries

This skill does not claim to be a required release-gate artifact because the
shared gate/catalog does not currently establish that contract. A quick profile
cannot satisfy a future full release-security requirement.

If the project later adopts a release-security gate, acceptable evidence must be
an immutable, independently recorded full-profile packet bound to the exact
commit, dirty state, source manifest, build artifact/configuration, tool/rule
versions, advisory snapshot, coverage matrix, and finding lifecycle records.
Open CRITICAL/HIGH findings must have independently auditable remediation or
owner-signed, unexpired acceptance records. This audit does not create either.

A re-audit receives prior stable finding IDs, their original evidence hashes,
the current target/scope hashes, and the exact diff. It verifies original
closure conditions plus new/changed attack surface. A quick re-audit remains
quick evidence and never upgrades or replaces a prior full profile.

---

## Handoff boundaries

For `FINDINGS` or `PARTIAL` with confirmed findings, provide containment and
remediation requirements but make no patch. A separate implementation workflow
must preview exact files/owners/operations/baseline hashes/tests, obtain explicit
authorization, implement, and produce test evidence.

For risk acceptance, route to the authorized security/product owner. Do not
suggest that an ordinary acknowledgment closes the finding.

For `NO_FINDINGS_IN_SCANNED_SCOPE`, recommend only the missing dynamic,
penetration, platform, or release evidence appropriate to the threat model.
Never say the game is safe or ready to ship.

---

## Non-negotiable rules

- Never output `SECURE` or `CLEAR TO SHIP` as an audit conclusion.
- Never claim a check, build, test, CVE query, or file scope ran without command
  and hash evidence.
- Never print or persist a secret value.
- Never invent `none` for unavailable advisory data.
- Never patch findings or self-accept risk in this workflow.
- Never write a report or mutate the workspace.
- Never let a quick scan substitute for full release evidence.
