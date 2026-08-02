# Skill Test Spec: $security-audit

## Skill Summary

`$security-audit` audits the game for security risks including save data
integrity, network communication, anti-cheat exposure, and data privacy. It
reads source files in `src/` for security patterns and checks whether sensitive
data is handled correctly. No director gates are invoked. The skill does not
write files (findings report only). Verdicts: SECURE, CONCERNS, or
VULNERABILITIES FOUND.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: SECURE, CONCERNS, VULNERABILITIES FOUND
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff (what to do with findings)

---

## Director Gate Checks

None. Security audit is a read-only advisory skill; no gates are invoked.

---

## Test Cases

### Case 1: Happy Path — Save data validated, no hardcoded credentials

**Fixture:**
- `src/core/save_system.gd` safely parses save data, bounds-checks gameplay
  values, confines paths, and does not grant server-backed entitlements locally
- No hardcoded API keys, passwords, or credentials in any `src/` file
- No version numbers or internal build IDs exposed in client-facing output

**Input:** `$security-audit`

**Expected behavior:**
1. Skill scans `src/` for security patterns: encryption usage, hardcoded credentials, exposed internals
2. All checks pass: save input is safely parsed/validated, no credentials found,
   no exposed internals
3. Findings report shows all checks PASS
4. Verdict is SECURE

**Assertions:**
- [ ] Skill checks save parsing, bounds, paths, and applicable trust boundaries;
      encryption alone is neither required nor sufficient
- [ ] Skill scans for hardcoded credentials (API keys, passwords, tokens)
- [ ] Skill checks for version/build numbers exposed to players
- [ ] All checks shown in findings report
- [ ] Verdict is SECURE when all checks pass

---

### Case 2: Vulnerabilities Found — Unsafe save trust boundary

**Fixture:**
- `src/core/save_system.gd` parses plain JSON, accepts an unbounded paid-currency
  value, and applies it to a server-backed account without authoritative validation

**Input:** `$security-audit`

**Expected behavior:**
1. Skill scans `src/` and traces the save value to the privileged account update
2. The missing bounds and authoritative validation are reported with call-site evidence
3. Plain JSON is not independently reported as a vulnerability
4. Verdict is VULNERABILITIES FOUND
5. Skill recommends validation at the trust boundary without inventing a new
   checksum, signature, or encryption mechanism

**Assertions:**
- [ ] The unsafe privileged data flow is flagged with file and approximate line
- [ ] Plain JSON / lack of encryption is not independently treated as a finding
- [ ] Remediation suggestion is given for each vulnerability
- [ ] Verdict is VULNERABILITIES FOUND when any vulnerability is detected
- [ ] No files are written or modified

---

### Case 3: Online Features Without Authentication — CONCERNS

**Fixture:**
- `src/networking/lobby.gd` exists with functions: `join_lobby()`, `send_chat()`
- No authentication check is found before `send_chat()` — players can call it without being verified
- Game has online multiplayer features (inferred from file presence)

**Input:** `$security-audit`

**Expected behavior:**
1. Skill scans `src/networking/` — detects online feature code
2. Skill checks for authentication guard before network calls — finds none on `send_chat()`
3. Flags: "Online feature without authentication check — CONCERNS"
4. Verdict is CONCERNS (not VULNERABILITIES FOUND, as this is a missing control, not an exploit)

**Assertions:**
- [ ] Skill detects online features by scanning for networking source files
- [ ] Missing authentication checks before network operations are flagged
- [ ] Verdict is CONCERNS (advisory severity) for missing authentication guards
- [ ] Output recommends adding authentication before network calls

---

### Case 4: Edge Case — No Source Files to Analyze

**Fixture:**
- `src/` directory does not exist or is completely empty

**Input:** `$security-audit`

**Expected behavior:**
1. Skill attempts to scan `src/` — no files found
2. Skill outputs an error: "No source files found in `src/` — nothing to audit"
3. No findings report is generated
4. No verdict is emitted

**Assertions:**
- [ ] Skill does not crash when `src/` is empty or absent
- [ ] Output clearly states that no source files were found
- [ ] No verdict is emitted (there is nothing to assess)
- [ ] Skill suggests verifying the `src/` directory path

---

### Case 5: Gate Compliance — No gate; security-engineer invoked separately

**Fixture:**
- Source files exist; 1 CONCERNS-level finding detected (debug logging enabled in release build)
- `review-mode.txt` contains `full`

**Input:** `$security-audit`

**Expected behavior:**
1. Skill scans source; finds debug logging active in release path
2. No director gate is invoked regardless of review mode
3. Verdict is CONCERNS
4. Output notes: "For formal security review, consider engaging a security-engineer agent"
5. Findings are presented as a read-only report; no files written

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Security-engineer consultation is suggested (not mandated)
- [ ] No files are written
- [ ] Verdict is CONCERNS for advisory-level security findings

---

## Protocol Compliance

- [ ] Reads source files in `src/` before auditing
- [ ] Checks save data encryption, hardcoded credentials, exposed internals, auth guards
- [ ] Provides remediation recommendations for each finding
- [ ] Does not write any files (read-only skill)
- [ ] No director gates are invoked
- [ ] Verdict is one of: SECURE, CONCERNS, VULNERABILITIES FOUND

---

## Coverage Notes

- Anti-cheat analysis (client-side value validation, server authority) is not
  explicitly tested here; it follows the CONCERNS or VULNERABILITIES pattern
  depending on severity.
- Data privacy compliance (GDPR, COPPA) is out of scope for this spec; those
  require legal review beyond code scanning.

## P0 Contract Coverage

- [ ] Editable data-driven configuration is checked for trust-boundary validation
  and is not itself a cheat finding.
- [ ] Suspected secret values are never read from denied files or reproduced in
  conversation, delegation, or reports; only redacted location/type evidence appears.
- [ ] An unavailable security role falls back to the same checklist. Failed or
  partial delegation marks incomplete coverage and cannot yield CLEAR TO SHIP.
- [ ] CRITICAL/HIGH means DO NOT SHIP; CLEAR TO SHIP requires complete evidence
  for every selected category; otherwise the result is ASSESSMENT INCOMPLETE.
