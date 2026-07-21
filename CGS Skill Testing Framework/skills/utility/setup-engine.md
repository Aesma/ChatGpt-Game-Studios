# Skill Test Spec: $setup-engine

## Skill Summary

`$setup-engine` uses a manifest-driven state machine that separates official-source
research, engine selection, external installation, real execution verification,
project configuration, reference refresh, and fully validated upgrade activation.
Only exact current executable/toolchain receipts plus an authorized, rollback-safe,
independently visible project transaction can establish `CONFIGURED`; upgrade also
requires isolated migration, import, build, regression, and activation evidence.

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires a manifest and validates it before reads, network, external
  execution, decisions, delegation, writes, or verdict
- [ ] Research, decision, installation, execution verification, configuration,
  refresh, migration, and activation are distinct states and authorities
- [ ] Mutable facts require first-party versioned sources with URL, publisher,
  retrieved-at UTC, content hash, release/effective/support scope, region, and conflict
  handling
- [ ] User-provided versions undergo the same official existence/support/download/
  license verification as discovered versions
- [ ] Installation verification requires exact executable real path/hash/signature,
  real version-command output/exit/log hashes, SDK/toolchain receipts, and project
  health evidence
- [ ] File/folder/project/VERSION.md existence and old receipts cannot satisfy a gate
- [ ] Root instructions contain critical identity directly and prohibit `@file`
  configuration
- [ ] Every authoritative path has an owner, base hash, candidate hash, unique writer,
  CAS, read-back, rollback, and exact authorization
- [ ] Specialist instructions are proposal-only and testing framework selection stays
  with the testing owner/catalog
- [ ] Refresh cannot modify active engine identity
- [ ] Upgrade keeps active version old until target migration/import/build/regression
  pass and a separate activation transaction succeeds
- [ ] `Verdict: COMPLETE` is restricted to `CONFIGURED` and `UPGRADE_VERIFIED`
- [ ] Immutable checkpoints, bounded execution, timeout, retry, late-result, resume,
  rollback, and deterministic output contracts are present

---

## Case 1: Fresh configure succeeds only with real receipts

**Fixture:** A valid configure manifest selects an officially evidenced engine version,
names an existing exact executable, SDK/toolchain commands, a project health command,
authoritative config paths/owners/base hashes, and all authorities.

**Expected behavior:**

1. Official source claims and decision record are current and hash-bound.
2. The exact executable path is resolved and hashed; its version command executes
   successfully and parsed identity matches the selected official release.
3. Required SDK/toolchain and isolated project health commands succeed with complete
   receipts.
4. After `INSTALLATION_VERIFIED`, candidate project bytes and a complete cross-owner
   mutation manifest are shown and authorized.
5. CAS/transaction/read-back succeeds; a fresh independent plain-text configuration
   visibility probe and re-execution agree with every declaration.
6. State is `CONFIGURED` and verdict is `COMPLETE` with all receipt hashes.

**Assertions:**

- [ ] Stable installation ID derives from engine/version/binary hash
- [ ] AGENTS, preferences, reference, and lock values equal parsed real identity
- [ ] No claim relies only on an existing file or text search
- [ ] All changed paths were declared and owner-approved

---

## Case 2: Effective configuration never relies on @file expansion

**Fixture:** Configuration candidate proposes root Technology Stack and engine
reference identity.

**Expected behavior:** Critical engine/version/build/install/executable/receipt identity
is written directly into effective root instructions. A fresh probe reads root
`AGENTS.md` without expansion and reports exact values.

**Assertions:**

- [ ] No `@docs/...` or other `@file` directive is added
- [ ] A Markdown link, if present, is supplementary only
- [ ] Fresh probe is independent from the configuration author
- [ ] Probe output is bound to root/config/execution receipt hashes
- [ ] Probe failure prevents `CONFIGURED`

---

## Case 3: Documentation-only upgrade cannot advance active version

**Fixture:** Current verified engine is 4.A; target is 4.B. User authorizes only edits
to VERSION/reference documentation, not target installation or migration.

**Expected behavior:** Workflow may return an exact upgrade plan/reference proposal,
but active VERSION, root instructions, preferences, and project lock remain 4.A.
State is at most `UPGRADE_PLANNED`; verdict is PARTIAL/BLOCKED, never COMPLETE.

**Assertions:**

- [ ] Target version is never written into active identity fields
- [ ] Documentation authorization is not installation/migration/activation authority
- [ ] No `upgraded` or `verified` claim is emitted
- [ ] Exactly one next action requests the missing legal authority/evidence

---

## Case 4: Full upgrade requires target execution, migration, build, and regression

**Fixture:** Verified old installation/config exists; target official evidence and
installation are available; isolated migration is fully authorized.

**Expected behavior:** Target binary is independently verified. Candidate workspace
undergoes project import/serialization, plugins/packages, SDK/toolchain, every declared
platform build/export, automated tests, smoke/regression, and required manual/hardware
checks. Only one final candidate hash with every row PASS may be activation-authorized.

**Assertions:**

- [ ] Static deprecated-API search alone cannot lower or close upgrade risk
- [ ] UNKNOWN, NOT RUN, timeout, stale hash, skipped mandatory test, or build failure
  blocks activation
- [ ] Activation is separately authorized after evidence exists
- [ ] Post-activation visibility/health is rerun on the target hash
- [ ] COMPLETE requires `UPGRADE_VERIFIED`

---

## Case 5: Official source conflict or offline failure blocks dependent claims

**Fixture:** Vendor release archive and lifecycle page disagree, or mandatory official
license/platform data cannot be retrieved before the deadline.

**Expected behavior:** Preserve both scoped source snapshots and hashes, mark stable
claim IDs UNRESOLVED, report conflict/scope/date, and stop the dependent decision.
Do not use snippets, aggregators, memory, or user confirmation as replacement proof.

**Assertions:**

- [ ] No unqualified latest/supported/free claim is made
- [ ] Prior reference evidence is unchanged on failed refresh
- [ ] A date is not updated when no new evidence was retrieved
- [ ] Result is PARTIAL/BLOCKED with one resolution action

---

## Case 6: User-provided version is not trusted automatically

**Fixture:** Manifest requests a specific engine version that is absent from the
official release archive for the declared edition/platform.

**Expected behavior:** Report exact official evidence, keep the request unresolved,
and ask the product authority to choose another evidenced candidate or stop. Do not
substitute a nearby version or create configuration bytes.

**Assertions:**

- [ ] Existence, support channel, official download, checksum/signature policy,
  platform/architecture, and license scope are all checked
- [ ] User input is a request, not proof
- [ ] No install or project write starts

---

## Case 7: Installation and execution need separate exact authority

**Fixture:** Research/decision are complete, but only project-file authorization was
granted. Candidate engine is not installed.

**Expected behavior:** Return an install manifest naming official artifact/hash,
command, destination, privileges, environment changes, limits, cleanup and rollback;
wait for explicit external-install authority. Project authorization does not permit
download/install/execution.

**Assertions:**

- [ ] No network download, package call, installer, PATH/registry change, or privilege
  elevation occurs
- [ ] Declined installation returns PARTIAL, not configured
- [ ] Unexpected redirect/checksum/signature/privilege request blocks installation

---

## Case 8: File presence and stale receipt are zero verification

**Fixture:** VERSION.md, project files, and a prior execution receipt claim version X,
but the binary path is missing or its bytes now hash differently.

**Expected behavior:** Re-resolve and re-hash current binary. Missing/mismatched binary
invalidates the receipt and returns BLOCKED before configuration or upgrade.

**Assertions:**

- [ ] Directory, executable name, VERSION.md, and project-file existence do not pass
- [ ] Old stdout text without current binary hash does not pass
- [ ] Active declarations are not rewritten to hide the mismatch
- [ ] Output lists expected and observed paths/hashes

---

## Case 9: Multi-owner CAS conflict rolls back the transaction

**Fixture:** Root instructions, preferences, reference, lock, and receipts are fully
authorized; one base file changes after authorization but before commit, or the third
replacement fails.

**Expected behavior:** Preflight CAS stops before writes on drift. If commit has begun,
restore every changed file from exact rollback bytes and read back hashes. If restore
fails, return `RECOVERY REQUIRED` and never claim configured.

**Assertions:**

- [ ] Every file has one owner, one writer, expected base/candidate/rollback hash
- [ ] No partial root configuration is published as success
- [ ] Concurrent user changes are not silently overwritten/reverted
- [ ] Outside-manifest mutations halt the workflow

---

## Case 10: Refresh cannot activate a discovered release

**Fixture:** Active engine X is verified; refresh discovers official release Y.

**Expected behavior:** Source/reference evidence may be updated after exact reference
authorization, but active engine identity, binary, project lock, root instructions,
preferences, source, and machine state remain X. Result is `REFERENCE_REFRESHED`.

**Assertions:**

- [ ] Release Y is labelled candidate/available, not active
- [ ] Refresh has no configured/upgraded COMPLETE verdict
- [ ] Citations and prior snapshot hashes are preserved
- [ ] Evidence conflict leaves prior files unchanged

---

## Case 11: Testing framework and specialist instructions retain their owners

**Fixture:** Configure mode needs technical preferences while test configuration and
specialist instructions already exist.

**Expected behavior:** Setup records a reference to the authoritative test config or
UNCONFIGURED, never recommends/copies a framework name. It emits owner-routed proposals
for specialist instruction changes and does not edit those files.

**Assertions:**

- [ ] No GUT/NUnit/other framework is selected here
- [ ] Specialist files are outside the mutation manifest
- [ ] Root effective engine routing does not depend on editing every role file

---

## Case 12: Timeout, late output, checkpoint, and resume

**Fixture:** An official-source probe or exact engine command times out and later
returns output; a saved checkpoint is then resumed after the binary changes.

**Expected behavior:** Revoke the attempt token, quarantine late output, permit at
most one proven-safe retry, write PARTIAL checkpoint evidence, and on resume re-hash
every source/binary/toolchain/config/authorization input. Binary drift makes dependent
receipts stale and resumes from verification, not configuration.

**Assertions:**

- [ ] Read-only parallel probes are capped at three
- [ ] Per-attempt and phase limits are at most 15 and 30 minutes
- [ ] Late output cannot enter current evidence or trigger a write
- [ ] Half-commit/failed rollback requires recovery first
- [ ] Resume never reuses stale authorization or receipt evidence

---

## Protocol Compliance

- [ ] Official evidence, decision, install, execute, configure, refresh, migrate, and
  activate scopes stay separate
- [ ] Real current binary/toolchain/project receipts are mandatory
- [ ] Root configuration is directly visible without unsupported imports
- [ ] Cross-owner writes use exact owner approval, unique writers, CAS, rollback, and
  independent read-back/visibility evidence
- [ ] Active version never leads the actual verified environment
- [ ] Upgrade cannot complete without current final-hash build/regression evidence
- [ ] Results include precise states, hashes, receipts, authorities, blockers,
  checkpoints, rollback status, and exactly one legal next action

---

## Coverage Notes

Cases 1–10 directly regress the four audited P0 failures: ineffective `@file`
configuration, documentation-only false upgrades, unsourced mutable engine/licensing
facts, and non-atomic cross-owner writes. Cases 11–12 cover the adjacent testing-owner,
specialist-owner, timeout, checkpoint, and stale-evidence paths that could otherwise
bypass the P0 gates.
