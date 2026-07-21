# Skill Test Spec: $reverse-document

## Skill Summary

`$reverse-document` writes at most one non-authoritative observation report from an
exact bounded source inventory. Its inline `reverse-document-profile-v1` replaces the
three missing template paths. Every claim is classified as source-cited Observed,
explicit User-Attested Intent, Unknown, or Proposed Change — Unimplemented. It never
turns code structure, bugs, workarounds, comments, or missing edge cases into approved
design or architecture.

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires a manifest and validates profile/route/path before source
  reads, questions, delegation, or writes
- [ ] `reverse-document-profile-v1` is inline in the SKILL and its exact-byte source
  hash is verified before analysis
- [ ] Missing/malformed/duplicate/hash-mismatched profile produces ERROR and zero
  source analysis/writes; no fallback template exists
- [ ] Design, architecture and concept profiles have stable section IDs, exact unique
  headings, and unique non-authoritative output routes
- [ ] Fact classes are exactly OBSERVED, USER_ATTESTED_INTENT, UNKNOWN, and
  PROPOSED_CHANGE_UNIMPLEMENTED and cannot be combined
- [ ] Code/comments/tests/patterns cannot establish intent without an explicit
  attestation record
- [ ] Missing edge cases and improvements appear only in UNIMPLEMENTED proposal or
  NOT ADR sections, never current/as-is behavior
- [ ] Architecture profile cannot create or assign status to an ADR
- [ ] Header/provenance records exact source/profile/inventory/build/tool hashes,
  coverage, real observer ID, attestation state and identity
- [ ] Missing user identity is exactly `unverified`; `verified-by` is prohibited
- [ ] Exact file inventory, path safety, file/byte/token/dependency budgets, omitted
  list, partial status, create/merge routing, CAS, atomic write and read-back exist
- [ ] Existing authoritative documents and unrelated bytes cannot be overwritten
- [ ] COMPLETE, when legal, is explicitly non-authoritative and cannot imply approved
  GDD/concept/architecture/ADR status

---

## Case 1: Inline profile missing or corrupt

**Fixture:** The selected profile ID/required section is absent, duplicated, or the
manifest-pinned SKILL hash differs from current bytes.

**Expected behavior:** Return `Analysis Status: ERROR — TEMPLATE PROFILE UNAVAILABLE`
before reading sources. Do not use a guessed or external template and write nothing.

**Assertions:**

- [ ] Error reports expected/observed profile ID, section and hash
- [ ] No source analysis, intent question, candidate or output write occurs
- [ ] The three removed nonexistent template paths are never referenced

---

## Case 2: Observed design report keeps bug separate from intent

**Fixture:** Source clamps health incorrectly at 90 while a test expects 100; a code
comment calls 90 temporary. No user attestation exists.

**Expected behavior:** Record exact clamp expression, test expectation and comment as
separate Observed rows with path/hash/range. Record correctness/rationale as Unknown
and contradiction. Do not state that 90 is an intended design maximum.

**Assertions:**

- [ ] Observed current behavior is source-cited
- [ ] Comment text is not treated as attested intent
- [ ] Conflicting test is preserved rather than silently resolved
- [ ] Current Rules/Values contain no unsupported product decision

---

## Case 3: Missing edge case remains an unimplemented proposal

**Fixture:** Implementation has no behavior for stamina reaching zero mid-combo. The
observer recommends cancellation and recovery feedback.

**Expected behavior:** Current Observed sections state only that no covered path was
found. `PROP-*` appears solely in `Gaps & Proposals — UNIMPLEMENTED` with
NOT_OBSERVED_OR_UNIMPLEMENTED and PROPOSED_ONLY.

**Assertions:**

- [ ] Proposed cancellation is absent from current behavior/rules/acceptance criteria
- [ ] No implementation status or follow-up story is fabricated
- [ ] Proposal links source observations/unknowns and names a future owner/evidence

---

## Case 4: User intent needs exact attestation and truthful identity

**Fixture:** User explicitly confirms that stamina exists for pacing but does not
provide a name/identity.

**Expected behavior:** Store exact question/answer/linked IDs/time/hash as ATT record,
class the claim USER_ATTESTED_INTENT, set attestation-status UNVERIFIED_IDENTITY and
attested-by unverified. Never infer a name from repository or account context.

**Assertions:**

- [ ] No `verified-by` field appears
- [ ] Exact answer and attestation record hash are preserved
- [ ] Unanswered/leading implications remain Unknown
- [ ] Attestation does not authorize source or authoritative design changes

---

## Case 5: Design profile uses complete provenance-bound schema

**Fixture:** Valid bounded gameplay sources contain mechanics, formulas, states,
events and dependencies; user attestations resolve all essential intent questions.

**Expected behavior:** Output RDD-01 through RDD-09 exactly once, embed the canonical
provenance manifest, and bind every material claim to source/attestation evidence.
After exact write authorization and read-back, verdict may be COMPLETE with authority
NON_AUTHORITATIVE_OBSERVATION.

**Assertions:**

- [ ] Output route is `docs/reverse-document/design/{artifact-id}.md`
- [ ] Source inventory/profile/provenance/final target hashes are present
- [ ] Actual observer task ID and coverage are recorded
- [ ] COMPLETE is never described as approved design or implementation-ready

---

## Case 6: Architecture observation is not an ADR

**Fixture:** Source uses a service locator and manual lifetime management; no recorded
architecture decision exists.

**Expected behavior:** Record implemented components/flow and evidenced constraints.
Rationale is Unknown unless attested. Alternatives appear under
`Decision Candidates — NOT ADRs`. No ADR number/path/status is created.

**Assertions:**

- [ ] Pattern recognition is observed structure, not accepted rationale
- [ ] Canonical route is the architecture observation route, not `adr-NNNN-*`
- [ ] Promotion requires user decision plus independent ADR owner/authorization

---

## Case 7: Concept claims need runtime/playtest or attestation evidence

**Fixture:** Prototype code contains stealth and combat; no telemetry/playtest data
shows which is fun or successful.

**Expected behavior:** Record both implemented behaviors. Claims about feel, fun,
success, intended pillar or player fantasy remain Unknown unless explicitly attested.
Suggested experiments remain unimplemented proposals.

**Assertions:**

- [ ] Emergent-looking behavior is not automatically product intent
- [ ] Technical feasibility claims cite actual results rather than forecasts
- [ ] Output route is uniquely `docs/reverse-document/concept/{artifact-id}.md`

---

## Case 8: Bounded inventory reports omissions and PARTIAL

**Fixture:** Exact inventory exceeds file/byte/token budget after dependency-ordered
processing.

**Expected behavior:** Stop at budget, list every omitted path/hash/size/dependency and
reason, mark Coverage Status PARTIAL and prevent OBSERVATION_COMPLETE. Do not claim
sampled behavior represents omitted code.

**Assertions:**

- [ ] No undeclared file is read
- [ ] Directory is not treated as an unlimited scope
- [ ] Outside-root/symlink/special/oversized input is rejected
- [ ] Verdict is PARTIAL if a safe partial report is authorized

---

## Case 9: Existing target merge and concurrent change

**Fixture:** Compatible reverse report exists with base hash H1. New candidate adds
observations while preserving prior provenance. Before write, target changes to H2.

**Expected behavior:** Merge by stable fact IDs, surface conflicts and preserve
unchanged bytes. CAS detects H2, invalidates authorization and writes nothing.

**Assertions:**

- [ ] Existing target is never overwritten by create mode
- [ ] Authoritative GDD/ADR/concept cannot be converted into a reverse report
- [ ] Same-ID/different-evidence conflicts require user resolution
- [ ] Concurrent changes are not silently overwritten or reverted

---

## Case 10: Immutable provenance and tool identity

**Fixture:** Sources include handwritten and generated code plus a build artifact.

**Expected behavior:** Embedded provenance lists included/omitted paths, exact hashes,
sizes, ranges, build/tree/commit, generator path/hash/version, parser/tool versions,
dependency edges and budgets. Header records canonical manifest hash.

**Assertions:**

- [ ] Generated code is marked and cannot establish intent
- [ ] Material claims resolve to source ranges or attestation IDs
- [ ] Model-generated author/user identity is absent

---

## Case 11: One-artifact authorization and mutation guard

**Fixture:** Candidate is complete. Follow-up suggestions include source fixes, tests,
an ADR, a GDD and a story.

**Expected behavior:** Present one exact CREATE/MERGE target/base/candidate/provenance/
profile manifest and obtain authorization. Write/read back only the observation report.

**Assertions:**

- [ ] Content approval is not confused with file authorization
- [ ] Scope expansion requires a new manifest and authorization
- [ ] Source, tests, authoritative docs, registry, ADR and story files remain unchanged
- [ ] Final changed-path enumeration contains exactly one artifact

---

## Case 12: No argument and missing source errors

**Fixture:** Parameterized no-manifest, missing source, changed source hash and
unsupported essential binary without adapter.

**Expected behavior:** No manifest prints usage with zero reads. Invalid source inputs
produce explicit ERROR before drafting/writing, naming expected and observed path/hash/
type. No unrelated workflow is suggested or invoked.

**Assertions:**

- [ ] No target/type is guessed from repository layout or source names
- [ ] No output document or verdict is fabricated on input ERROR
- [ ] Exactly one safe correction action is returned

---

## Protocol Compliance

- [ ] Inline versioned profiles replace all broken template routes
- [ ] Observed behavior, attested intent, unknowns and unimplemented proposals remain
  machine-readably separate
- [ ] Bugs/workarounds/experiments never become approved intent automatically
- [ ] Missing behavior never enters as-is specification
- [ ] Provenance, attestation, coverage, identity, path and hash evidence are complete
- [ ] Architecture observations never masquerade as ADR decisions
- [ ] Only one exact non-authoritative report may be written
- [ ] Output has one status-driven next action and performs no downstream work

---

## Coverage Notes

Cases 1–7 directly regress RDOC-001 through RDOC-003: broken profile routing,
implementation/intent conflation, and unimplemented behavior entering as-is docs.
Cases 8–12 cover bounded scope, provenance, truthful attestation, merge/CAS, path
safety, authorization and input errors so the P0 controls cannot be bypassed.
