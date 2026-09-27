#!/usr/bin/env python3
"""Inspect worktree integration inputs without changing Git state.

Example:
    python inspect_worktrees.py --repo . --into main --source feature/a \
        --pin feature/a FULL_COMMIT_SHA --candidate ../integration

Stdout is one schema_version=1 JSON object, including usage failures and --help.
Exit 0 means no detected Git blockers, not semantic acceptance; 1 means blockers;
2 means invalid CLI usage. Only Git metadata, status, and changed path names are
read. No fetch, checkout, merge, commit, worktree creation, or file-body reads run.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


class UsageError(Exception):
    """An argument error that must be rendered as JSON."""


class JsonParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class GitError(Exception):
    def __init__(self, message: str, code: str = "git_command_failed") -> None:
        super().__init__(message)
        self.code = code


def new_report() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "repository": {"root": None, "common_dir": None},
        "target": {"ref": None, "sha": None, "worktrees": []},
        "sources": [],
        "candidate": None,
        "worktrees": [],
        "duplicates": [],
        "warnings": [],
        "blockers": [],
        "target_is_ancestor_of_candidate": None,
        "ok": False,
    }


def issue(report: dict[str, Any], bucket: str, code: str, message: str,
          **details: Any) -> None:
    report[bucket].append({"code": code, "message": message, **details})


def decode(value: bytes) -> str:
    return value.decode("utf-8", errors="surrogateescape")


def path_key(value: str) -> str:
    return os.path.normcase(str(Path(value).resolve()))


def git(directory: str, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    """Run only caller-specified read-only Git commands, without shell expansion."""
    env = os.environ.copy()
    # Prevent inherited repository/index overrides from defeating --repo / -C.
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                 "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        env.pop(name, None)
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", GIT_NO_REPLACE_OBJECTS="1")
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", directory, *args],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, env=env, timeout=60, check=False,
        )
    except FileNotFoundError as exc:
        raise GitError("Git is not installed or is unavailable on PATH.", "git_unavailable") from exc
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitError(f"Git inspection could not run: {exc}") from exc
    if check and result.returncode:
        raise GitError(decode(result.stderr).strip() or f"Git inspection exited {result.returncode}.")
    return result


def git_text(directory: str, *args: str) -> str:
    return decode(git(directory, *args).stdout).rstrip("\r\n")


def resolve_commit(directory: str, ref: str) -> str | None:
    result = git(directory, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}", check=False)
    if result.returncode == 0:
        return decode(result.stdout).strip().lower()
    return None


def symbolic_ref(directory: str, ref: str) -> str | None:
    result = git(directory, "rev-parse", "--symbolic-full-name", "--verify", "--end-of-options", ref,
                 check=False)
    value = decode(result.stdout).strip()
    return value if result.returncode == 0 and value.startswith("refs/") else None


def common_directory(directory: str) -> str:
    return str(Path(git_text(directory, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve())


def valid_source_text(ref: str) -> bool:
    return bool(ref) and not ref.startswith("-") and not any(c in ref for c in "\0\r\n")


def is_ancestor(directory: str, ancestor: str, descendant: str) -> bool:
    result = git(directory, "merge-base", "--is-ancestor", ancestor, descendant, check=False)
    if result.returncode not in (0, 1):
        raise GitError(decode(result.stderr).strip() or "Could not inspect commit ancestry.")
    return result.returncode == 0


def merge_base(directory: str, first: str, second: str) -> str | None:
    result = git(directory, "merge-base", first, second, check=False)
    if result.returncode == 1:
        return None
    if result.returncode:
        raise GitError(decode(result.stderr).strip() or "Could not inspect merge base.")
    return decode(result.stdout).strip()


def parse_worktrees(raw: bytes) -> list[dict[str, Any]]:
    """Parse -z records without splitting paths on whitespace or newlines."""
    records: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for field in raw.split(b"\0"):
        if not field:
            if current:
                records.append(current)
                current = {}
            continue
        key, separator, value = field.partition(b" ")
        current[decode(key)] = decode(value) if separator else True
    if current:
        records.append(current)
    return records


def operation_names(directory: str) -> list[str]:
    result: list[str] = []
    for name, markers in (
        ("merge", ("MERGE_HEAD",)),
        ("rebase", ("rebase-merge", "rebase-apply")),
        ("cherry-pick", ("CHERRY_PICK_HEAD",)),
        ("revert", ("REVERT_HEAD",)),
        ("bisect", ("BISECT_START", "BISECT_LOG")),
        ("sequencer", ("sequencer",)),
    ):
        for marker in markers:
            marker_path = git_text(directory, "rev-parse", "--path-format=absolute", "--git-path", marker)
            if Path(marker_path).exists():
                result.append(name)
                break
    return result


def inspect_worktree(record: dict[str, Any], common_dir: str) -> dict[str, Any]:
    value = {
        "path": record["worktree"], "head": record.get("HEAD"),
        "branch": record.get("branch"), "dirty": None, "status": "unavailable",
        "operations": [], "common_repo": False,
    }
    if record.get("bare"):
        value["error"] = "Bare repository entries do not have a working tree."
        return value
    try:
        root = git_text(value["path"], "rev-parse", "--show-toplevel")
        if path_key(root) != path_key(value["path"]):
            value["error"] = "Registered worktree path is not the actual worktree root."
            return value
        value["common_repo"] = path_key(common_directory(value["path"])) == path_key(common_dir)
        if not value["common_repo"]:
            value["error"] = "Registered worktree belongs to another common Git directory."
            return value
        value["head"] = resolve_commit(value["path"], "HEAD")
        value["branch"] = symbolic_ref(value["path"], "HEAD")
        value["operations"] = operation_names(value["path"])
        status = git(value["path"], "status", "--porcelain=v1", "-z", "--untracked-files=all",
                     "--ignore-submodules=none").stdout
        value["dirty"] = bool(status)
        value["status"] = "dirty" if status else "clean"
    except GitError as exc:
        value["error"] = str(exc)
    return value


def check_worktree_safety(report: dict[str, Any], worktree: dict[str, Any], role: str) -> None:
    if worktree["status"] == "unavailable":
        issue(report, "blockers", f"{role}_worktree_unavailable" if role == "target" else "invalid_candidate",
              f"The {role} worktree could not be inspected.", path=worktree["path"],
              detail=worktree.get("error"))
    if not worktree["common_repo"]:
        issue(report, "blockers", "target_worktree_mismatch" if role == "target" else "candidate_repo_mismatch",
              f"The {role} worktree does not belong to this repository.", path=worktree["path"])
    if worktree["dirty"]:
        issue(report, "blockers", f"{role}_dirty", f"The {role} worktree has tracked or untracked changes.",
              path=worktree["path"])
    if worktree["operations"]:
        issue(report, "blockers", f"{role}_operation", f"The {role} worktree has an unfinished Git operation.",
              path=worktree["path"], operations=worktree["operations"])


def inspect(args: argparse.Namespace, report: dict[str, Any]) -> None:
    directory = str(Path(args.repo).resolve())
    try:
        bare = git_text(directory, "rev-parse", "--is-bare-repository")
        if bare == "true":
            issue(report, "blockers", "unsupported_bare_repository", "Use a non-bare worktree for --repo.")
            return
        root = git_text(directory, "rev-parse", "--show-toplevel")
        common_dir = common_directory(directory)
    except GitError as exc:
        issue(report, "blockers", "git_unavailable" if exc.code == "git_unavailable" else "invalid_repository",
              str(exc), path=directory)
        return
    report["repository"] = {"root": str(Path(root).resolve()), "common_dir": common_dir}

    target_ref = args.into if args.into.startswith("refs/heads/") else "refs/heads/" + args.into
    report["target"]["ref"] = target_ref
    if (not valid_source_text(args.into) or
            (args.into.startswith("refs/") and not args.into.startswith("refs/heads/")) or
            git(directory, "check-ref-format", target_ref, check=False).returncode):
        issue(report, "blockers", "invalid_target", "--into must name a local branch.", ref=args.into)
    else:
        report["target"]["sha"] = resolve_commit(directory, target_ref)
        if not report["target"]["sha"]:
            issue(report, "blockers", "target_unresolved", "The target local branch does not resolve to a commit.",
                  ref=args.into)

    pins: dict[str, str] = {}
    bad_pins: set[str] = set()
    for ref, pin in args.pin:
        if ref not in args.source:
            issue(report, "blockers", "pin_without_source", "Each --pin must match a --source argument.", ref=ref)
            continue
        if not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", pin):
            issue(report, "blockers", "invalid_pin", "Pins must be full 40- or 64-character hexadecimal commit SHAs.",
                  ref=ref, pin=pin)
            bad_pins.add(ref)
            continue
        pin = pin.lower()
        if ref in pins and pins[ref] != pin:
            issue(report, "blockers", "conflicting_pins", "A source has conflicting pinned commits.", ref=ref)
            bad_pins.add(ref)
        else:
            pins[ref] = pin

    records = parse_worktrees(git(directory, "worktree", "list", "--porcelain", "-z").stdout)
    report["worktrees"] = [inspect_worktree(record, common_dir) for record in records]
    # Use registered branch identity too, so an unavailable target is not missed.
    target_paths = {record["worktree"] for record in records if record.get("branch") == target_ref}
    for worktree in report["worktrees"]:
        if worktree["path"] in target_paths or worktree["branch"] == target_ref:
            report["target"]["worktrees"].append(worktree["path"])
            check_worktree_safety(report, worktree, "target")
        elif worktree["status"] == "unavailable":
            issue(report, "warnings", "worktree_unavailable", "A registered worktree could not be inspected.",
                  path=worktree["path"], detail=worktree.get("error"))

    candidate_sha = None
    candidate_branch = None
    if args.candidate:
        candidate_path = str(Path(args.candidate).resolve())
        candidate = inspect_worktree({"worktree": candidate_path}, common_dir)
        report["candidate"] = {key: candidate[key] for key in ("path", "branch", "operations", "dirty")}
        report["candidate"]["sha"] = candidate["head"]
        check_worktree_safety(report, candidate, "candidate")
        if candidate["common_repo"] and candidate["status"] != "unavailable":
            candidate_sha, candidate_branch = candidate["head"], candidate["branch"]
            if not candidate_branch or not candidate_sha:
                issue(report, "blockers", "invalid_candidate", "The candidate must have a named branch and a commit.",
                      path=candidate_path)
            target_sha = report["target"]["sha"]
            if target_sha and candidate_sha:
                if not merge_base(directory, target_sha, candidate_sha):
                    issue(report, "blockers", "candidate_unrelated_history", "Candidate and target histories are unrelated.")
                report["target_is_ancestor_of_candidate"] = is_ancestor(directory, target_sha, candidate_sha)
        if candidate_branch == target_ref:
            issue(report, "blockers", "candidate_branch_conflict", "The candidate branch must differ from the target.",
                  ref=candidate_branch, conflicts_with="target")

    seen_refs: dict[str, dict[str, Any]] = {}
    seen_shas: dict[str, dict[str, Any]] = {}
    for ref in args.source:
        if ref in seen_refs:
            original = seen_refs[ref]
            report["duplicates"].append({"reason": "source_ref", "ref": ref, "duplicate_of": original["ref"],
                                         "sha": original["sha"]})
            continue
        source: dict[str, Any] = {
            "ref": ref, "ref_sha": None, "sha": None, "pinned": ref in pins or ref in bad_pins,
            "merge_base": None, "changed_files": [], "already_merged": False,
            "already_merged_target": False, "already_merged_candidate": None,
            "already_merged_into": [], "worktrees": [],
        }
        seen_refs[ref] = source
        if not valid_source_text(ref):
            issue(report, "blockers", "invalid_source", "Source references cannot be empty, option-like, or contain NUL/newlines.", ref=ref)
            report["sources"].append(source)
            continue
        source["ref_sha"] = resolve_commit(directory, ref)
        branch = symbolic_ref(directory, ref)
        if not source["ref_sha"]:
            if git(directory, "check-ref-format", "--allow-onelevel", ref, check=False).returncode:
                issue(report, "blockers", "invalid_source", "An unresolved source must be a valid Git reference name.", ref=ref)
                report["sources"].append(source)
                continue
        if candidate_branch and branch == candidate_branch:
            issue(report, "blockers", "candidate_branch_conflict", "The candidate branch must differ from every source branch.",
                  ref=candidate_branch, conflicts_with=ref)
        if ref in bad_pins:
            report["sources"].append(source)
            continue
        if ref in pins:
            resolved_pin = resolve_commit(directory, pins[ref])
            if resolved_pin != pins[ref]:
                issue(report, "blockers", "pin_not_commit", "The pinned object must itself be an available commit, not a tag or other object.",
                      ref=ref, pin=pins[ref])
            else:
                source["sha"] = resolved_pin
                if source["ref_sha"] and source["ref_sha"] != resolved_pin:
                    issue(report, "warnings", "ref_moved", "The source ref differs from the handover; inspection uses the pinned commit.",
                          ref=ref, ref_sha=source["ref_sha"], sha=resolved_pin)
                elif not source["ref_sha"]:
                    issue(report, "warnings", "source_ref_unresolved", "The source ref is unavailable; inspection uses the pinned commit.",
                          ref=ref, sha=resolved_pin)
        else:
            source["sha"] = source["ref_sha"]
            if not source["sha"]:
                issue(report, "blockers", "source_unresolved", "The source does not resolve to an available commit.", ref=ref)
        source_sha = source["sha"]
        for worktree in report["worktrees"]:
            matches = (branch and worktree["branch"] == branch) or (
                not branch and source_sha and worktree["head"] == source_sha)
            if matches:
                source["worktrees"].append(worktree["path"])
                if worktree["dirty"]:
                    issue(report, "warnings", "source_dirty", "Uncommitted source worktree changes are excluded from the delivery.",
                          ref=ref, path=worktree["path"])
                if worktree["operations"]:
                    issue(report, "warnings", "source_operation", "A source worktree has an unfinished Git operation; only the fixed commit is inspected.",
                          ref=ref, path=worktree["path"], operations=worktree["operations"])
        if source_sha and source_sha in seen_shas:
            report["duplicates"].append({"reason": "commit_sha", "ref": ref,
                                         "duplicate_of": seen_shas[source_sha]["ref"], "sha": source_sha})
            continue
        report["sources"].append(source)
        if not source_sha:
            continue
        seen_shas[source_sha] = source
        target_sha = report["target"]["sha"]
        if target_sha:
            source["merge_base"] = merge_base(directory, target_sha, source_sha)
            if not source["merge_base"]:
                issue(report, "blockers", "unrelated_history", "Source and target do not share a commit history.", ref=ref, sha=source_sha)
            else:
                paths = git(directory, "diff", "--name-only", "--no-renames", "-z", "--no-ext-diff", "--no-textconv",
                            source["merge_base"], source_sha, "--").stdout
                source["changed_files"] = [decode(path) for path in paths.split(b"\0") if path]
                source["already_merged_target"] = is_ancestor(directory, source_sha, target_sha)
                if source["already_merged_target"]:
                    source["already_merged_into"].append("target")
        if candidate_sha:
            source["already_merged_candidate"] = is_ancestor(directory, source_sha, candidate_sha)
            if source["already_merged_candidate"]:
                source["already_merged_into"].append("candidate")
        source["already_merged"] = (source["already_merged_candidate"] if candidate_sha
                                     else source["already_merged_target"])


def main(argv: list[str] | None = None) -> int:
    """Print exactly one JSON report and return the CLI status code."""
    report = new_report()
    parser = JsonParser(description=__doc__, add_help=False, allow_abbrev=False)
    parser.add_argument("--repo", required=True, help="Repository worktree path.")
    parser.add_argument("--into", required=True, help="Existing target local branch.")
    parser.add_argument("--source", action="append", required=True, help="Source commit reference; repeatable.")
    parser.add_argument("--pin", action="append", nargs=2, default=[], metavar=("REF", "FULL_SHA"))
    parser.add_argument("--candidate", help="Existing integration worktree root.")
    parser.add_argument("--help", "-h", action="store_true", help="Emit usage in JSON.")
    arguments = list(sys.argv[1:] if argv is None else argv)
    exit_code = 1
    try:
        if arguments in (["--help"], ["-h"]):
            report.update(ok=True, help=parser.format_help())
            exit_code = 0
        else:
            args = parser.parse_args(arguments)
            if args.help:
                report.update(ok=True, help=parser.format_help())
                exit_code = 0
            else:
                inspect(args, report)
                report["ok"] = not report["blockers"]
                exit_code = 0 if report["ok"] else 1
    except UsageError as exc:
        issue(report, "blockers", "usage_error", str(exc))
        report["usage"] = parser.format_usage().strip()
        exit_code = 2
    except GitError as exc:
        issue(report, "blockers", exc.code, str(exc))
    except (OSError, ValueError) as exc:
        issue(report, "blockers", "inspection_error", str(exc))
    # ASCII encoding keeps filenames lossless as JSON escapes even on Windows
    # consoles with a legacy output code page or non-UTF-8 path bytes on POSIX.
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
