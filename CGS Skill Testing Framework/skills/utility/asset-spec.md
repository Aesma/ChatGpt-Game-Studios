# Skill Test Spec: $asset-spec

## Skill Summary

`$asset-spec` accepts `system:<name>`, `level:<name>`,
`character:<name>`, and `entity:<name>`. It generates one target-level spec
at `design/assets/specs/[target]-assets.md` and updates
`design/assets/asset-manifest.md`. The art bible is a hard prerequisite.

---

## Static Assertions

- [ ] All four target types are declared by both invocation and parser
- [ ] The authoritative spec path is `design/assets/specs/[target]-assets.md`
- [ ] No `assets/specs/[asset]-spec.md` output contract appears
- [ ] Missing art bible stops with no spec or manifest write
- [ ] Spec and manifest are previewed together before one authorization

---

## Case 1: Entity input is executable

**Input:** `$asset-spec entity:goblin`

**Assertions:**

- [ ] Target type parses as entity and name as goblin
- [ ] Entity source lookup is used
- [ ] The workflow does not reject its own inventory recommendation

---

## Case 2: Canonical output path

**Input:** `$asset-spec system:combat`

**Assertions:**

- [ ] All approved asset blocks are compiled into
      `design/assets/specs/combat-assets.md`
- [ ] Manifest rows point to that same target-level spec
- [ ] No per-asset files under `assets/specs/` are created

---

## Case 3: Missing art bible blocks production specs

**Fixture:** `design/art/art-bible.md` is absent.

**Assertions:**

- [ ] The user is directed to `$art-bible`
- [ ] No placeholder visual rules are invented
- [ ] Neither the target spec nor manifest changes
- [ ] The run does not report a production-ready COMPLETE result

---

## Case 4: Spec and manifest share one atomic approval

**Fixture:** Both target spec and manifest edits are ready.

**Assertions:**

- [ ] The complete spec content and exact manifest diff are shown together
- [ ] Both paths appear in the first and only changeset preview
- [ ] Approval writes both continuously without a second prompt
- [ ] Declining leaves both files unchanged
- [ ] The spec is never written before the manifest edit is discovered or shown

---

## Protocol Compliance

- [ ] Director gates are not introduced; configured specialist behavior remains unchanged
- [ ] Existing ASSET fields and manifest schema remain unchanged
- [ ] The workflow adds no second output hierarchy or placeholder dependency mode
