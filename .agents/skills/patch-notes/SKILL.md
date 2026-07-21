---
name: patch-notes
description: "Create traceable local patch-note drafts only from an exact approved candidate and its verified production deployment receipt; never publish."
---

## Invocation and execution

Invoke this workflow as $patch-notes.

Arguments: [release-id] [--style brief|detailed|full]. A release-id is required. Style changes presentation only and defaults to detailed.

This workflow may generate a local draft after its evidence requirements pass. It never deploys or publishes, never posts to a store, website, forum, email, chat, or social channel, and never treats local-write authorization as public-publish approval.

Before the first local file change, present one complete changeset containing the single canonical target, its expected content hash, and the intended write. Obtain one explicit authorization for that local write. Do not re-prompt file by file. If the boundary expands, stop and obtain a new authorization.

Do not invoke another project skill, a director gate, a deployment, or a publication workflow.

---

## Phase 1 — Validate release identity and exact candidate

1. Validate release-id against the project release-ID schema. Reject separators, traversal tokens, absolute paths, control characters, ambiguous aliases, and unversioned labels.
2. Load one approved change manifest for that exact release ID. Do not fall back to HEAD, the working tree, an inferred tag, an arbitrary Git range, or the newest changelog.
3. Require this manifest contract:

    schema_version
    release_id
    manifest_id
    manifest_hash
    approval_receipt_id
    approval_status: APPROVED
    from_ref
    to_ref
    candidate_digest
    target_platforms
    change_items

4. Require every change item to contain:

    change_id
    disposition: INCLUDE or EXCLUDE
    player_visible: true or false
    category
    approved_player_fact
    source_ids
    verification_ids
    sensitive_classification
    manifest_item_hash

5. Verify that from_ref and to_ref resolve exactly as declared, form the approved bounded range, and that to_ref/candidate_digest identify the candidate under review. A local HEAD may be observed only to detect mismatch; it must never widen the candidate.
6. Capture a single evidence snapshot with release ID, manifest hash, candidate digest, resolved refs, and source hashes. If any required field is missing, ambiguous, stale, unverifiable, or inconsistent, return BLOCKED before drafting prose.

Only INCLUDE items that are player_visible and belong to the exact approved manifest may enter the claim table. Changelogs, Git commits, sprint data, retrospectives, design documents, balance proposals, bug trackers, and QA records cannot add claims. Manifest-linked records may corroborate an approved_player_fact but may not expand or strengthen it.

---

## Phase 2 — Verify production deployment authority

Load one immutable deployment receipt from the configured production deployment authority. The receipt must contain:

    schema_version
    receipt_id
    receipt_hash
    release_id
    environment: production
    deployment_status: SUCCEEDED
    candidate_digest
    manifest_hash
    deployed_artifact_digest
    deployed_targets
    deployed_at
    issuer
    verification_status: VERIFIED

The receipt is valid only when release_id, candidate_digest, and manifest_hash exactly match Phase 1; the environment is production; status is SUCCEEDED; the receipt is verified by the configured authority; and every claimed target is included in deployed_targets.

A local hotfix branch, hotfix plan, hotfix approval, tag, merge, build success, QA pass, release-checklist result, release readiness, staging deployment, canary result, scheduled rollout, or user assertion is not proof of production deployment. These signals must never authorize released, deployed, live, available now, fixed, or shipped language.

If the production receipt is absent, unverified, non-production, unsuccessful, stale, for another target, or bound to another candidate or manifest, return BLOCKED with an evidence table. Do not generate player-facing release narrative, not even as a speculative draft. A claim is eligible only when both its exact approved candidate item and the matching production receipt are valid.

---

## Phase 3 — Build and review the claim table

Create one deterministic row per eligible change_id:

    claim_id
    change_id
    category
    exact_player_fact
    candidate_digest
    manifest_id
    manifest_item_hash
    source_ids
    verification_ids
    deployment_receipt_id
    deployment_receipt_hash
    deployed_targets
    sensitivity
    disclosure_state
    draft_text
    status

Rules:

- Preserve the approved_player_fact. Rewrite for clarity and tone only when the meaning, scope, causality, platform coverage, numbers, and certainty do not change.
- Never infer implementation from a design document, intent from a retrospective, player impact from a technical refactor, or deployment from readiness evidence.
- Never turn fixed a null reference into fixed a player crash unless the approved fact and verification evidence explicitly establish that behavior.
- Preserve exact before/after values, platform qualifiers, rollout boundaries, and known limitations.
- Purely internal or EXCLUDE items remain in an exclusions table and never enter prose.
- Every sentence or bullet in the draft maps to one or more claim IDs. No untraced title, highlight, reason, availability promise, or known issue is allowed.
- Tone guides and templates may shape wording and layout but cannot introduce facts, promises, quotations, dates, links, or scope.

Sensitive classes include SECURITY, ANTI_CHEAT, PRIVACY, EXPLOIT, LEGAL, EMBARGOED, and any project-defined restricted class. Default to OMIT when a claim is sensitive. Include it only with a separate verified public-disclosure approval bound to the claim ID, candidate digest, approved text boundary, audience, and expiry. The model cannot self-approve disclosure.

Do not invent developer commentary, first-person team voice, quotations, motives, lessons, or opinions. Full style may include developer commentary only when supplied verbatim in an approved quote record containing speaker, exact text, claim IDs, candidate digest, public-use approval, and provenance. Otherwise omit the section and record NO_APPROVED_QUOTE.

Assign stable review findings for unsupported, overstated, sensitive, contradictory, or untraceable text. Perform at most one bounded revision against those same findings. Any unresolved blocker returns BLOCKED and no prose artifact is written.

---

## Phase 4 — Draft and optionally write one canonical artifact

When all evidence and review checks pass, present:

- the local draft
- the claim-to-source table
- excluded items with reasons
- sensitive omissions without exploitable detail
- manifest and production receipt identities/hashes
- the canonical target
- publication_state: NOT_AUTHORIZED

Use the selected style, but do not create empty or invented sections. Title, date, platform list, and links require explicit manifest or receipt evidence. The resulting document includes machine-readable provenance for release_id, candidate_digest, manifest_hash, and deployment_receipt_hash.

The only canonical local target is:

    production/releases/[validated-release-id]/patch-notes.md

Do not also write a docs copy. Any public-site or documentation representation must be a downstream generated projection that cites the canonical artifact hash.

If no local-write authorization is requested or granted, return status DRAFTED and stop. If the user explicitly authorizes the exact one-file changeset, write only the canonical artifact, verify its hash, return status WRITTEN, and stop.

DRAFTED and WRITTEN describe local artifact state only. Neither means publicly approved, publicly posted, or successfully published. This workflow must not perform any external publication action.

---

## Phase 5 — Return status and handoff

Return patch_notes/v2:

    schema_version: patch_notes/v2
    status: DRAFTED | WRITTEN | BLOCKED
    release_id
    candidate_digest
    manifest_id
    manifest_hash
    production_receipt_id
    production_receipt_hash
    deployed_targets
    claim_table
    exclusions
    sensitive_omissions
    review_findings
    canonical_target
    canonical_hash
    publication_state: NOT_AUTHORIZED
    blocker_codes
    next_owner

Use BLOCKED when exact candidate authority, production deployment authority, evidence coverage, sensitive disclosure, or final traceability is insufficient. Do not report COMPLETE.

Return at most one next-owner handoff. A local content reviewer may approve or reject the draft as a separate decision. Public publishing requires a separate explicit approval and a separate publishing workflow outside this skill. Never imply that a release checklist, hotfix readiness, community review, local write, or this status packet grants publication authority.

Stop after returning the packet. Do not invoke the handoff.
