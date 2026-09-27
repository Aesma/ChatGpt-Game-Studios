"""Integration tests for read-only preflight and isolated worktree Git mechanics.

Run with: python -m unittest discover -s tests -p test_worktree_preflight.py -v
Set CGS_FRAMEWORK_ROOT to validate a reviewable staged framework overlay.
All commits, branches, merges, and checkout edits occur in disposable fixtures.
The fixture integration sequences are not live executions of the agent skill.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


FRAMEWORK_ROOT = Path(os.environ.get("CGS_FRAMEWORK_ROOT",
                                    str(Path(__file__).resolve().parents[1])))
HELPER = (FRAMEWORK_ROOT / ".agents" / "skills" /
          "integrate-worktrees" / "scripts" / "inspect_worktrees.py")
GIT = shutil.which("git")


@unittest.skipUnless(GIT, "Git is required for worktree integration fixtures")
class WorktreePreflightTests(unittest.TestCase):
    """Verify the real helper against actual repositories, without user Git config."""

    def setUp(self):
        self.assertTrue(HELPER.is_file(), f"Required preflight helper missing: {HELPER}")
        self.temp = tempfile.TemporaryDirectory(prefix="cgs worktree qa ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "target checkout"
        self.repo.mkdir()
        self.env = dict(os.environ)
        for key in list(self.env):
            if key.startswith("GIT_"):
                del self.env[key]
        self.env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                         "GIT_TERMINAL_PROMPT": "0"})
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Worktree QA Fixture")
        self.git("config", "user.email", "worktree-qa@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.commit(self.repo, {"README.md": "fixture\n",
                               ".gitignore": "production/integration-runs/\n",
                               "feature_a.py": "ENABLED = False\n",
                               "feature_b.py": "ENABLED = False\n",
                               "check.py": "import feature_a, feature_b\n"
                               "assert not (feature_a.ENABLED and feature_b.ENABLED), "
                               "'incompatible combined features'\n"}, "fixture: baseline")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *args, cwd=None, check=True):
        result = subprocess.run([GIT, *args], cwd=cwd or self.repo, env=self.env,
                                text=True, encoding="utf-8", capture_output=True)
        if check and result.returncode:
            self.fail(f"Git {args} failed ({result.returncode}): {result.stderr}")
        return result

    def commit(self, checkout, files, message):
        for name, content in files.items():
            path = checkout / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        self.git("add", "--", *files, cwd=checkout)
        self.git("commit", "-m", message, cwd=checkout)
        return self.git("rev-parse", "HEAD", cwd=checkout).stdout.strip()

    def branch(self, name, start=None):
        checkout = self.root / name.replace("/", " ")
        self.git("worktree", "add", "-b", name, str(checkout), start or self.base)
        return checkout

    def deliver(self, name="task/a", files=None):
        checkout = self.branch(name)
        sha = self.commit(checkout, files or {"alpha.txt": "alpha\n"}, "fixture: delivery")
        return checkout, sha

    def inspect(self, sources=("task/a",), target="main", pins=(), candidate=None,
                repo=None, expected=0):
        command = [sys.executable, str(HELPER), "--repo", str(repo or self.repo),
                   "--into", target]
        for source in sources:
            command += ["--source", source]
        for ref, sha in pins:
            command += ["--pin", ref, sha]
        if candidate is not None:
            command += ["--candidate", str(candidate)]
        result = subprocess.run(command, env=self.env, text=True, encoding="utf-8",
                                capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["ok"], expected == 0)
        if expected == 1:
            self.assertTrue(data["blockers"], data)
        return data

    def snapshot(self):
        """Include integration journals, Git metadata/index/refs, and all fixture files."""
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def validate_fixture(self, checkout):
        return subprocess.run([sys.executable, "-B", "check.py"], cwd=checkout,
                              env=self.env, text=True, capture_output=True)

    def test_preflight_nested_linked_checkout_preserves_every_file(self):
        # Arrange: linked .git file, spaces, ignored integration journal, and nested cwd.
        checkout, sha = self.deliver()
        nested = checkout / "nested directory"
        nested.mkdir()
        journal = checkout / "production/integration-runs/batch-a.json"
        journal.parent.mkdir(parents=True)
        journal.write_text('{"batch": "a", "phase": "prepared"}\n', encoding="utf-8")
        self.assertTrue((checkout / ".git").is_file())
        before = self.snapshot()
        # Act: execute the real helper, which is always check-only.
        result = self.inspect(repo=nested)
        # Assert: exact pin, actual root, and no file or Git metadata mutation.
        self.assertEqual(result["target"]["sha"], self.base)
        self.assertEqual(result["sources"][0]["sha"], sha)
        self.assertEqual(Path(result["repository"]["root"]).resolve(), checkout.resolve())
        self.assertEqual(self.snapshot(), before)

    def test_preflight_missing_source_and_target_block_without_mutation(self):
        self.deliver()
        before = self.snapshot()
        self.inspect(sources=("missing-branch",), expected=1)
        self.inspect(target="missing-target", expected=1)
        self.assertEqual(self.snapshot(), before)

    def test_preflight_unrelated_source_blocks(self):
        self.deliver()
        other = self.root / "unrelated checkout"
        self.git("worktree", "add", "--detach", str(other), self.base)
        self.git("checkout", "--orphan", "unrelated", cwd=other)
        self.git("rm", "-rf", ".", cwd=other)
        self.commit(other, {"foreign.txt": "unrelated history\n"}, "fixture: unrelated")
        result = self.inspect(sources=("unrelated",), expected=1)
        self.assertTrue(result["blockers"])
        unrelated_sha = self.git("rev-parse", "unrelated").stdout.strip()
        self.inspect(pins=(("task/a", unrelated_sha),), expected=1)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)

    def test_preflight_delivery_pin_excludes_later_source_commit(self):
        checkout, delivered = self.deliver()
        later = self.commit(checkout, {"later.txt": "not delivered\n"}, "fixture: later")
        result = self.inspect(pins=(("task/a", delivered),))
        source = result["sources"][0]
        self.assertEqual(source["sha"], delivered)
        self.assertEqual(source["ref_sha"], later)
        self.assertTrue(source["pinned"])
        self.assertTrue(result["warnings"])
        self.assertIn("alpha.txt", source["changed_files"])
        self.assertNotIn("later.txt", source["changed_files"])
        candidate = self.branch("integration/pinned")
        self.git("merge", "--no-edit", source["sha"], cwd=candidate)
        self.assertTrue((candidate / "alpha.txt").exists())
        self.assertFalse((candidate / "later.txt").exists())
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)

    def test_preflight_delivery_pin_handles_missing_objects_and_rewritten_ref(self):
        self.deliver()
        _, other_sha = self.deliver("task/b", {"beta.txt": "beta\n"})
        self.inspect(pins=(("task/a", "f" * 40),), expected=1)
        result = self.inspect(pins=(("task/a", other_sha),))
        self.assertEqual(result["sources"][0]["sha"], other_sha)
        self.assertTrue(any(warning["code"] == "ref_moved"
                            for warning in result["warnings"]))

    def test_preflight_duplicate_ref_and_sha_are_reported_once(self):
        _, sha = self.deliver()
        self.git("branch", "task/alias", sha)
        result = self.inspect(sources=("task/a", "task/a", "task/alias"))
        self.assertEqual(len(result["sources"]), 1)
        self.assertTrue(result["duplicates"])
        self.assertEqual(result["sources"][0]["sha"], sha)

    def test_preflight_source_dirty_warns_but_excludes_uncommitted_work(self):
        checkout, sha = self.deliver()
        (checkout / "uncommitted.txt").write_text("not delivered\n", encoding="utf-8")
        before = self.snapshot()
        result = self.inspect(pins=(("task/a", sha),))
        self.assertTrue(result["warnings"])
        self.assertNotIn("uncommitted.txt", result["sources"][0]["changed_files"])
        self.assertEqual(self.snapshot(), before)

    def test_preflight_dirty_target_and_candidate_block_without_cleanup(self):
        self.deliver()
        candidate = self.branch("integration/dirty")
        (self.repo / "target-local.txt").write_text("keep target\n", encoding="utf-8")
        (candidate / "candidate-local.txt").write_text("keep candidate\n", encoding="utf-8")
        before = self.snapshot()
        result = self.inspect(candidate=candidate, expected=1)
        self.assertTrue(result["candidate"]["dirty"])
        self.assertEqual(self.snapshot(), before)

    def test_preflight_in_progress_conflict_blocks_and_preserves_target(self):
        self.deliver(files={"README.md": "source version\n"})
        candidate = self.branch("integration/conflict")
        self.commit(candidate, {"README.md": "candidate version\n"}, "fixture: conflict")
        conflict = self.git("merge", "--no-edit", "task/a", cwd=candidate, check=False)
        self.assertNotEqual(conflict.returncode, 0)
        before = self.snapshot()
        result = self.inspect(candidate=candidate, expected=1)
        self.assertTrue(result["candidate"]["operations"])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)

    def test_preflight_candidate_must_belong_to_same_repository(self):
        self.deliver()
        foreign = self.root / "other repository"
        foreign.mkdir()
        self.git("init", "-b", "foreign", cwd=foreign)
        self.inspect(candidate=foreign, expected=1)

    def test_preflight_detached_candidate_blocks_without_creating_branch(self):
        self.deliver()
        candidate = self.root / "detached candidate"
        self.git("worktree", "add", "--detach", str(candidate), self.base)
        before = self.snapshot()
        self.inspect(candidate=candidate, expected=1)
        self.assertEqual(self.snapshot(), before)

    def test_preflight_target_merge_operation_blocks_without_aborting(self):
        self.deliver(files={"README.md": "task version\n"})
        advanced = self.commit(self.repo, {"README.md": "target version\n"},
                               "fixture: target conflict")
        conflict = self.git("merge", "--no-edit", "task/a", check=False)
        self.assertNotEqual(conflict.returncode, 0)
        before = self.snapshot()
        self.inspect(expected=1)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), advanced)

    def test_preflight_already_merged_target_and_candidate_are_distinct(self):
        _, sha = self.deliver()
        candidate = self.branch("integration/repeat")
        self.git("merge", "--no-edit", sha, cwd=candidate)
        result = self.inspect(candidate=candidate)
        self.assertFalse(result["sources"][0]["already_merged_target"])
        self.assertTrue(result["sources"][0]["already_merged_candidate"])
        self.git("merge", "--ff-only", "integration/repeat")
        result = self.inspect(candidate=candidate)
        self.assertTrue(result["sources"][0]["already_merged_target"])

    def test_fixture_success_promotes_exact_verified_candidate(self):
        # Arrange independent deliveries and candidate, all in disposable fixture.
        _, alpha = self.deliver()
        _, beta = self.deliver("task/b", {"beta.txt": "beta\n"})
        candidate = self.branch("integration/success")
        report = self.inspect(sources=("task/a", "task/b"), candidate=candidate)
        self.assertEqual([s["sha"] for s in report["sources"]], [alpha, beta])
        # Act: emulate approved Git mechanics, then execute actual fixture checks.
        for source in report["sources"]:
            self.git("merge", "--no-edit", source["sha"], cwd=candidate)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)
        self.assertEqual((candidate / "alpha.txt").read_text(), "alpha\n")
        self.assertEqual((candidate / "beta.txt").read_text(), "beta\n")
        evidence = self.validate_fixture(candidate)
        self.assertEqual(evidence.returncode, 0, evidence.stderr)
        verified = self.git("rev-parse", "HEAD", cwd=candidate).stdout.strip()
        self.inspect(sources=("task/a", "task/b"), candidate=candidate)
        self.git("merge", "--ff-only", verified)
        # Assert exact validated commit promoted; original source refs unchanged.
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), verified)
        self.assertEqual(self.git("rev-parse", "task/a").stdout.strip(), alpha)
        self.assertEqual(self.git("rev-parse", "task/b").stdout.strip(), beta)

    def test_fixture_combined_failure_keeps_target_unchanged(self):
        a, _ = self.deliver(files={"feature_a.py": "ENABLED = True\n"})
        b, _ = self.deliver("task/b", {"feature_b.py": "ENABLED = True\n"})
        self.assertEqual(self.validate_fixture(a).returncode, 0)
        self.assertEqual(self.validate_fixture(b).returncode, 0)
        candidate = self.branch("integration/failure")
        self.git("merge", "--no-edit", "task/a", cwd=candidate)
        self.git("merge", "--no-edit", "task/b", cwd=candidate)
        # Git preflight succeeds but actual combined validation fails.
        self.inspect(sources=("task/a", "task/b"), candidate=candidate)
        evidence = self.validate_fixture(candidate)
        self.assertNotEqual(evidence.returncode, 0)
        self.assertIn("incompatible combined features", evidence.stderr)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), self.base)
        self.assertNotEqual(self.git("rev-parse", "HEAD", cwd=candidate).stdout.strip(),
                            self.base)

    def test_fixture_target_drift_requires_resync_before_fast_forward(self):
        _, sha = self.deliver()
        candidate = self.branch("integration/drift")
        self.git("merge", "--no-edit", sha, cwd=candidate)
        original = self.inspect(candidate=candidate)["target"]["sha"]
        self.assertEqual(self.validate_fixture(candidate).returncode, 0)
        advanced = self.commit(self.repo, {"target-new.txt": "new target work\n"},
                               "fixture: target advancement")
        current = self.inspect(candidate=candidate)["target"]["sha"]
        self.assertEqual(current, advanced)
        self.assertNotEqual(current, original)
        blocked = self.git("merge", "--ff-only", "integration/drift", check=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), advanced)
        # New target is integrated and evidence rerun for the resulting revision.
        self.git("merge", "--no-edit", current, cwd=candidate)
        self.assertEqual((candidate / "target-new.txt").read_text(), "new target work\n")
        self.assertEqual(self.validate_fixture(candidate).returncode, 0)
        verified = self.git("rev-parse", "HEAD", cwd=candidate).stdout.strip()
        self.git("merge", "--ff-only", verified)
        self.assertEqual(self.git("rev-parse", "main").stdout.strip(), verified)


if __name__ == "__main__":
    unittest.main()
