---
name: security-audit
description: "Audit the game for security vulnerabilities: save tampering, cheat vectors, network exploits, data exposure, and input validation gaps. Produces a prioritised security report with remediation guidance. Run before any public release or multiplayer launch."
---

## Invocation and execution

Invoke this workflow as `$security-audit`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[full | network | save | input | quick]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `security-engineer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# Security Audit

Security is not optional for any shipped game. Even single-player games have
save tampering vectors. Multiplayer games have cheat surfaces, data exposure
risks, and denial-of-service potential. This skill systematically audits the
codebase for the most common game security failures and produces a prioritised
remediation plan.

**Run this skill:**
- Before any public release (required for the Polish → Release gate)
- Before enabling any online/multiplayer feature
- After implementing any system that reads from disk or network
- When a security-related bug is reported

**Output:** `production/security/security-audit-[date].md`

---

## Phase 1: Parse Arguments and Scope

**Modes:**
- `full` — all categories (recommended before release)
- `network` — network/multiplayer only
- `save` — save file and serialization only
- `input` — input validation and injection only
- `quick` — only the following checks that can produce CRITICAL/HIGH findings:
  unsafe dynamic execution/deserialization or path use; hardcoded credentials;
  network authority/authentication/input-validation bypasses; privileged
  entitlement, currency, score, or progression trust violations; and an
  exact-version dependency match to a CRITICAL/HIGH official advisory
- No argument — run `full`

Read `docs/technical-preferences.md` to determine engine/language, target
platforms, and whether networking is in scope. If any scope field is
unconfigured, inspect existing source/config directory names and explicit APIs
only to build candidate scope, show the evidence, and ask the user to confirm.
Do not default the project to single-player or multiplayer.

Build a manifest of all existing project source and configuration directories
applicable to the selected mode. If none contains an auditable text file, stop
with "No auditable source or configuration files found for [scope]", write no
report, and issue no security verdict.

---

## Phase 2: Spawn Security Engineer

If the `security-engineer` role is available, delegate once and pass the mode,
engine/language, and source-directory manifest. Never pass a suspected secret's
value. If the role is unavailable, the current agent follows the same six-category
checklist. If delegation fails or times out, mark the affected categories as
partial coverage and do not produce CLEAR TO SHIP.

---

## Phase 3: Audit Categories

The security-engineer evaluates each of the following. Skip categories not
applicable to the confirmed project scope. Every search pattern below identifies
a candidate only. Inspect the call-site data flow, trust boundary, and applicable
release/debug build condition before creating a finding; a keyword hit by itself
is not evidence of a vulnerability.

### Category 1: Save File and Serialization Security
- Are save files validated before loading? (no blind deserialization)
- Are save file paths constructed from user input? (path traversal risk)
- Are save values parsed safely and bounds-checked before use?
- Do competitive, monetised, or server-backed entitlements get validated at the
  applicable authoritative trust boundary?
- Are there any eval() or dynamic code execution calls near save loading?

Candidate search patterns: `File.open`, `load`, `deserialize`, `JSON.parse`,
`from_json`, `read_file`. Trace the selected overload and the data reaching it
before classifying it.

### Category 2: Network and Multiplayer Security (skip if confirmed out of scope)
- Is game state authoritative on the server, or does the client dictate outcomes?
- Are incoming network packets validated for size, type, and value range?
- Are player positions and state changes validated server-side?
- Is there rate limiting on any network calls?
- Are authentication tokens handled correctly (never sent in plaintext)?
- Does the game expose any debug endpoints in release builds?

Candidate search patterns: `recv`, `receive`, `PacketPeer`, `socket`,
`NetworkedMultiplayerPeer`, `rpc`, `rpc_id`. Confirm each call-site flow.

### Category 3: Input Validation
- Are any player-supplied strings used in file paths? (path traversal)
- Are any player-supplied strings logged without sanitization? (log injection)
- Are numeric inputs (e.g., item quantities, character stats) bounds-checked before use?
- Are achievement/stat values checked before being written to any backend?

Candidate search patterns: `get_input`, `Input.get_`, `input_map`, and
user-facing text fields. Confirm whether the data reaches a sensitive sink.

### Category 4: Data Exposure
- Are any API keys, credentials, or secrets hardcoded in `src/` or `assets/`?
- Are debug symbols or verbose error messages included in release builds?
- Does the game log sensitive player data to disk or console?
- Are any internal file paths or system information exposed to players?

Search file contents for candidate identifiers such as `api_key`, `secret`,
`password`, `token`, and `private_key`, plus release-facing debug/logging calls.
Obey denied-path rules, including never reading forbidden environment files.
For a suspected secret, report only file, line, and identifier type with the
value redacted; never echo it in conversation, delegation, or a report. Generic
`DEBUG`, `print(`, or logging hits require a confirmed release path and sensitive
data flow before becoming a finding.

### Category 5: Cheat and Anti-Tamper Vectors
- Are external data-driven gameplay values validated for type/range at their
  trust boundary, without treating editable configuration itself as a flaw?
- Are critical progression or entitlement flags (e.g., "has paid for DLC")
  validated by the appropriate authoritative side?
- Is there any protection against memory editing tools (Cheat Engine, etc.) for multiplayer?
- Are leaderboard/score submissions validated before acceptance?

Note: Client-side anti-cheat is largely unenforceable. Focus on server-side validation for anything competitive or monetised.

### Category 6: Dependency and Supply Chain
- Are any third-party plugins or libraries used? List them.
- Do any plugins have known CVEs in the version being used?
- Are plugin sources verified (official marketplace, reviewed repository)?

Inspect `addons/`, `plugins/`, `third_party/`, and `vendor/` when present, and
list external dependencies with their exact recorded versions. A CVE conclusion
requires an exact version and an authoritative vendor/government advisory. If
the version is absent, official advisory access is unavailable, or the match is
ambiguous, mark the dependency `Not Assessed`; never write `none` by inference.

---

## Phase 4: Classify Findings

For each finding, assign severity from evidence of exploitability and impact,
not project type alone:

| Level | Definition |
|-------|-----------|
| **CRITICAL** | Remote code execution, data breach, or trivially-exploitable cheat that breaks multiplayer integrity |
| **HIGH** | Save tampering that bypasses progression, credential exposure, or server-side authority bypass |
| **MEDIUM** | Client-side cheat enablement, information disclosure, or input validation gap with limited impact |
| **LOW** | Defence-in-depth improvement — hardening that reduces attack surface but no direct exploit exists |

Every new finding starts `Open`. Use `Accepted Risk` only when an existing
artifact or the user explicitly supplies the acceptance decision and rationale;
the auditor cannot accept risk on the team's behalf. Use `Out of Scope` only
when the confirmed scope supports it. Do not mechanically promote every HIGH
finding to CRITICAL merely because multiplayer exists.

---

## Phase 5: Generate Report

```markdown
# Security Audit Report

**Date**: [date]
**Scope**: [full | network | save | input | quick]
**Engine**: [engine + version]
**Audited by**: [actual executor]
**Files scanned**: [N source files, N config files]

---

## Executive Summary

| Severity | Count | Must Fix Before Release |
|----------|-------|------------------------|
| CRITICAL | [N] | Yes — all |
| HIGH | [N] | Yes — all |
| MEDIUM | [N] | Recommended |
| LOW | [N] | Optional |

**Release recommendation**: [CLEAR TO SHIP / DO NOT SHIP / ASSESSMENT INCOMPLETE]

- Any CRITICAL or HIGH finding → DO NOT SHIP.
- Zero blockers and evidence for every selected category → CLEAR TO SHIP.
- Any selected category with partial/missing evidence → ASSESSMENT INCOMPLETE;
  list it under Data Limitations and do not issue CLEAR TO SHIP.

---

## CRITICAL Findings

### SEC-001: [Title]
**Category**: [Save / Network / Input / Data / Cheat / Dependency]
**File**: `[path]` line [N]
**Description**: [What the vulnerability is]
**Attack scenario**: [How a malicious user would exploit it]
**Remediation**: [Specific code change or pattern to apply]
**Effort**: [Low / Medium / High]
**Status**: Open

[repeat per finding]

---

## HIGH Findings

[same format]

---

## MEDIUM Findings

[same format]

---

## LOW Findings

[same format]

---

## Accepted Risk

[Only existing user/team decisions, with source and rationale; otherwise None]

---

## Dependency Inventory

| Plugin / Library | Version | Source | Advisory Assessment |
|-----------------|---------|--------|---------------------|
| [name] | [exact version or unknown] | [source] | [advisory ID / none found / Not Assessed] |

---

## Data Limitations

[Unconfigured scope, missing versions, unavailable official advisory checks,
partial delegation, or unreadable sources]

---

## Remediation Priority Order

1. [SEC-NNN] — [1-line description] — Est. effort: [Low/Medium/High]
2. ...

---

## Re-Audit Trigger

Run `$security-audit` again after remediating any CRITICAL or HIGH findings.
The Polish → Release gate requires this report with no open CRITICAL or HIGH items.
```

---

## Phase 6: Write Report

Present the report summary (executive summary + CRITICAL/HIGH findings only) in conversation.

Resolve `production/security/security-audit-[date].md` and read it if it already
exists. Offer a targeted update or stop; do not overwrite it or invent a new
version name. Show the complete report and exact create/update in the complete
changeset preview, then write only after the single changeset approval.

---

## Phase 7: Gate Integration

This report is a required artifact for the **Polish → Release gate**.

After remediating findings, re-run: `$security-audit quick` to confirm CRITICAL/HIGH items are resolved before running `$gate-check release`.

If CRITICAL findings exist:
> "⛔ CRITICAL security findings must be resolved before any public release. Do not proceed to `$launch-checklist` until these are addressed."

If no CRITICAL/HIGH findings and every selected category has complete evidence:
> "✅ No blocking security findings. Report written to `production/security/`. Include this path when running `$gate-check release`."

If any selected category is incomplete, report **ASSESSMENT INCOMPLETE** and the
missing coverage instead of a shipping clearance.

---

## Collaborative Protocol

- **Never assume a pattern is safe or unsafe from a keyword** — inspect the
  call-site data flow and build condition before classifying it
- **Accepted risk requires a team decision** — record only an explicit existing
  decision; do not create one during the audit
- **Use evidence-based severity** — multiplayer changes the threat model but
  does not automatically change every HIGH finding to CRITICAL
- **This is not a penetration test** — this audit covers common patterns; a real pentest by a human security professional is recommended before any competitive or monetised multiplayer launch
