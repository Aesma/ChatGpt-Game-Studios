from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import skill_test_rules as sut


PACKAGE = Path(__file__).resolve().parent


def load_rules() -> dict:
    return json.loads((PACKAGE / "rules-v1.yaml").read_text(encoding="utf-8"))


def write_skill(root: Path, package: str, name: str, body: str = "## Phase\n\nComplete.\n") -> None:
    skill_dir = root / ".agents" / "skills" / package
    (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "fixture"\n---\n\n# Fixture\n\n{body}', encoding="utf-8"
    )
    (skill_dir / "agents" / "openai.yaml").write_text("interface: {}\n", encoding="utf-8")


def write_catalog(root: Path, skills: list[tuple[str, str]], agents: list[str]) -> None:
    framework = root / "CGS Skill Testing Framework"
    framework.mkdir(parents=True, exist_ok=True)
    lines = ["version: 2", "skills:"]
    for name, spec in skills:
        lines.extend((f"  - name: {name}", f"    spec: {spec}"))
        path = root / spec
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {name}\n", encoding="utf-8")
    lines.append("agents:")
    for name in agents:
        lines.extend((f"  - name: {name}", f"    spec: CGS Skill Testing Framework/agents/{name}.md"))
    (framework / "catalog.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


class RuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.rules = load_rules()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_recursive_discovery_and_exclusions(self) -> None:
        write_skill(self.root, "group/nested", "nested")
        agent_root = self.root / ".codex" / "agents"
        (agent_root / "tier").mkdir(parents=True)
        (agent_root / "tier" / "worker.toml").write_text("description='x'\n", encoding="utf-8")
        (agent_root / "generators").mkdir()
        (agent_root / "generators" / "not-a-role.toml").write_text("x=1\n", encoding="utf-8")
        (agent_root / "helper.generated.toml").write_text("x=1\n", encoding="utf-8")

        skills = sut.discover(self.root, "skill", self.rules)
        agents = sut.discover(self.root, "agent", self.rules)

        self.assertEqual(skills["selected"], [".agents/skills/group/nested/SKILL.md"])
        self.assertEqual(agents["selected"], [".codex/agents/tier/worker.toml"])
        self.assertEqual(
            {row["rule_id"] for row in agents["excluded"]},
            {"DISC-X003-GENERATED-DIRECTORY", "DISC-A002-GENERATOR-TOML"},
        )

    def test_symlink_is_reported_and_never_followed(self) -> None:
        source = self.root / ".agents" / "skills" / "real"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("x", encoding="utf-8")
        link = self.root / ".agents" / "skills" / "linked"
        try:
            os.symlink(source, link, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        ledger = sut.discover(self.root, "skill", self.rules)
        self.assertEqual(len(ledger["selected"]), 1)
        self.assertTrue(any(row["rule_id"] == "DISC-X001-SYMLINK" for row in ledger["excluded"]))

    def test_duplicate_precedes_grammar_and_unicode_is_not_silently_fixed(self) -> None:
        policy = self.rules["name_policy"]
        records = [
            {"source": "a", "name": sut.canonical_name("Skill-A", policy)},
            {"source": "b", "name": sut.canonical_name("skill-a", policy)},
        ]
        duplicates = sut.duplicate_rows(records)
        self.assertEqual(duplicates[0]["key"], "skill-a")
        self.assertIn("NAME-003-NOT-CASEFOLDED", records[0]["name"]["errors"])
        self.assertIn("NAME-004-SURROUNDING-WHITESPACE", sut.canonical_name(" skill-a", policy)["errors"])
        self.assertIn("NAME-006-GRAMMAR", sut.canonical_name("cafe\u0301", policy)["errors"])

    def test_hardlink_path_alias_is_reported(self) -> None:
        one = self.root / "one"
        two = self.root / "two"
        one.write_text("same", encoding="utf-8")
        try:
            os.link(one, two)
        except OSError as exc:
            self.skipTest(f"hardlinks unavailable: {exc}")
        aliases = sut.path_alias_rows(self.root, ["one", "two"])
        self.assertEqual(aliases[0]["sources"], ["one", "two"])

    def test_placeholder_context_distinguishes_metavariable_template_and_active_sentinel(self) -> None:
        text = """## Arguments
`$demo <target> [--flag]`

## Output Template
```yaml
id: <generated-id>
```

## Active Contract
```yaml
id: <unresolved>
writes:
  path: outputs/[receipt-id].yaml
```
TODO wire this later.
"""
        findings = sut.markdown_findings(text, "SKILL.md", self.rules)
        by_rule = [(row["rule_id"], row["outcome"], row["token"]) for row in findings]
        self.assertIn(("PH-002-DECLARED-METAVARIABLE", "PASS", "<target>"), by_rule)
        self.assertIn(("PH-002-DECLARED-METAVARIABLE", "PASS", "[--flag]"), by_rule)
        self.assertIn(("PH-002-DECLARED-METAVARIABLE", "PASS", "<generated-id>"), by_rule)
        self.assertIn(("PH-003-TEMPLATE-SCOPE", "PASS", "<generated-id>"), by_rule)
        self.assertIn(("PH-004-ACTIVE-STRUCTURED", "FAIL", "<unresolved>"), by_rule)
        self.assertIn(("PH-002-DECLARED-METAVARIABLE", "PASS", "[receipt-id]"), by_rule)
        self.assertIn(("PH-001-ACTIVE-SENTINEL", "FAIL", "TODO"), by_rule)

    def test_legacy_context_exception_is_bounded(self) -> None:
        text = """## Migration
Historical `.claude/` path quoted for removal.

## Active Contract
Use `AskUserQuestion` now.
"""
        findings = sut.markdown_findings(text, "SKILL.md", self.rules)
        legacy = [(row["rule_id"], row["outcome"]) for row in findings if row["rule_id"].startswith("LEG-")]
        self.assertIn(("LEG-001-CLAUDE-PATH", "PASS"), legacy)
        self.assertIn(("LEG-003-CLAUDE-TOOL-TOKEN", "FAIL"), legacy)

    def test_budget_omission_is_partial_and_deterministic(self) -> None:
        write_skill(self.root, "a", "a")
        write_skill(self.root, "b", "b")
        self.rules["budgets"]["maximum_candidate_files"] = 1
        ledger = sut.discover(self.root, "skill", self.rules)
        sut.load_selected(self.root, ledger, self.rules)
        self.assertEqual([row["path"] for row in ledger["loaded"]], [".agents/skills/a/SKILL.md"])
        self.assertEqual([row["path"] for row in ledger["omitted"]], [".agents/skills/b/SKILL.md"])
        self.assertEqual(sut.aggregate(sut.ledger_outcomes(ledger))["validation"], "PARTIAL_VALIDATION")

    def test_static_all_scans_every_recursive_target(self) -> None:
        write_skill(self.root, "a", "a", "## Active\n\nComplete.\n")
        write_skill(self.root, "group/b", "b", "## Active\n\nTODO later.\n")
        result = sut.run_static(self.root, "all", self.rules)
        self.assertTrue(any(row["path"].endswith("group/b/SKILL.md") for row in result["findings"]))
        self.assertEqual(result["aggregation"]["validation"], "NON-COMPLIANT")

    def test_aggregation_truth_table_is_exhaustive_at_precedence_edges(self) -> None:
        vectors = [
            ([{"axis": "authority", "outcome": "INVALID"}, {"axis": "target", "outcome": "FAIL"}], "TEST_INFRA_INVALID"),
            ([{"axis": "target", "outcome": "FAIL"}, {"axis": "coverage", "outcome": "PARTIAL"}], "NON-COMPLIANT"),
            ([{"axis": "target", "outcome": "PASS"}, {"axis": "coverage", "outcome": "PARTIAL"}], "PARTIAL_VALIDATION"),
            ([{"axis": "target", "outcome": "WARN"}], "WARNINGS"),
            ([{"axis": "target", "outcome": "PASS"}], "COMPLIANT"),
            ([], "TEST_INFRA_INVALID"),
        ]
        for outcomes, expected in vectors:
            with self.subTest(expected=expected):
                self.assertEqual(sut.aggregate(outcomes)["validation"], expected)

    def test_manifest_hash_binding_and_mismatch(self) -> None:
        package = self.root / ".agents" / "skills" / "skill-test"
        package.mkdir(parents=True)
        shutil.copy2(PACKAGE / "skill_test_rules.py", package / "skill_test_rules.py")
        shutil.copy2(PACKAGE / "rules-v1.yaml", package / "rules-v1.yaml")
        manifest = {
            "schema": sut.MANIFEST_SCHEMA,
            "runner": {"path": ".agents/skills/skill-test/skill_test_rules.py", "version": "1.0.0", "sha256": sut.sha256_bytes((package / "skill_test_rules.py").read_bytes())},
            "rules": {"path": ".agents/skills/skill-test/rules-v1.yaml", "version": "1.0.0", "sha256": sut.sha256_bytes((package / "rules-v1.yaml").read_bytes())},
            "allowed_argv": [["--repo-root", "<path>", "--mode", "audit"]],
            "output_schema": sut.OUTPUT_SCHEMA,
            "interpreter": {"minimum_version": "3.11.0", "maximum_exclusive_version": "3.14.0"},
            "timeout_seconds": 30,
            "writes": [],
        }
        path = package / "validator-manifest-v1.yaml"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(sut.verify_manifest(self.root, path)["valid"])
        manifest["runner"]["sha256"] = "sha256:" + "0" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        result = sut.verify_manifest(self.root, path)
        self.assertFalse(result["valid"])
        self.assertIn("runner-hash", result["errors"])

    def test_allowed_argv_is_exact(self) -> None:
        self.assertTrue(sut.allowed_argv(["--repo-root", "C:/repo", "--mode", "audit"]))
        self.assertTrue(sut.allowed_argv(["--repo-root", "C:/repo", "--mode", "static", "--target", "demo"]))
        self.assertFalse(sut.allowed_argv(["--mode", "audit", "--repo-root", "C:/repo"]))
        self.assertFalse(sut.allowed_argv(["--repo-root", "C:/repo", "--mode", "audit", "--rules", "other"]))

    def test_audit_reports_exact_duplicate_and_set_diff(self) -> None:
        write_skill(self.root, "one", "skill-a")
        write_skill(self.root, "nested/two", "Skill-A")
        agent_root = self.root / ".codex" / "agents"
        agent_root.mkdir(parents=True)
        (agent_root / "worker.toml").write_text("description='x'\n", encoding="utf-8")
        write_catalog(
            self.root,
            [("skill-a", "CGS Skill Testing Framework/skills/skill-a.md")],
            ["other-agent"],
        )
        result = sut.run_audit(self.root, self.rules)
        self.assertEqual(result["sets"]["skills"]["duplicates"]["implementation"][0]["key"], "skill-a")
        self.assertEqual(result["sets"]["agents"]["missing_from_catalog"], ["worker"])
        self.assertEqual(result["sets"]["agents"]["extra_in_catalog"], ["other-agent"])
        self.assertEqual(result["aggregation"]["validation"], "NON-COMPLIANT")


if __name__ == "__main__":
    unittest.main()
