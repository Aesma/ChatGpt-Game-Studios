#!/usr/bin/env python3
"""Deterministic read-only supplement for the skill-test P1 rules."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path
from typing import Any, Iterable

OUTPUT_SCHEMA = "cgs-skill-test-runner-output/v1"
RULES_SCHEMA = "cgs-skill-test-rules/v1"
MANIFEST_SCHEMA = "cgs-skill-test-validator-manifest/v1"
RUNNER_VERSION = "1.0.0"


def read_json_yaml(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level value must be an object")
    return value, raw


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def path_key(value: str) -> str:
    return unicodedata.normalize("NFC", value.replace("\\", "/")).casefold()


def canonical_name(raw: Any, policy: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, str):
        return {"raw": raw, "key": None, "valid": False, "errors": ["NAME-001-NOT-STRING"]}
    key = unicodedata.normalize("NFC", raw).casefold()
    errors: list[str] = []
    if raw != unicodedata.normalize("NFC", raw):
        errors.append("NAME-002-NOT-NFC")
    if raw != raw.casefold():
        errors.append("NAME-003-NOT-CASEFOLDED")
    if raw != raw.strip():
        errors.append("NAME-004-SURROUNDING-WHITESPACE")
    if len(raw) > int(policy["maximum_codepoints"]):
        errors.append("NAME-005-TOO-LONG")
    if not re.fullmatch(str(policy["grammar"]), raw):
        errors.append("NAME-006-GRAMMAR")
    if policy.get("forbid_consecutive_hyphens") and "--" in raw:
        errors.append("NAME-007-CONSECUTIVE-HYPHENS")
    return {"raw": raw, "key": key, "valid": not errors, "errors": errors}


def duplicate_rows(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        key = record.get("name", {}).get("key")
        if key is not None:
            grouped.setdefault(key, []).append(record)
    return [
        {"key": key, "sources": sorted((row["source"] for row in rows), key=path_key)}
        for key, rows in sorted(grouped.items())
        if len(rows) > 1
    ]


def path_alias_rows(repo_root: Path, sources: Iterable[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[str]] = {}
    for source in sources:
        try:
            path = repo_root / source
            stat = path.stat()
            identity: tuple[Any, ...]
            if stat.st_ino:
                identity = ("inode", stat.st_dev, stat.st_ino)
            else:
                identity = ("realpath", path_key(path.resolve(strict=True).as_posix()))
            grouped.setdefault(identity, []).append(source)
        except OSError:
            continue
    return [
        {"identity": ":".join(map(str, identity)), "sources": sorted(paths, key=path_key)}
        for identity, paths in sorted(grouped.items())
        if len(paths) > 1
    ]


def _excluded_directory(name: str, discovery: dict[str, Any]) -> tuple[str, str] | None:
    for rule in discovery["rules"]:
        if rule["kind"] == "directory_segment_exact" and name in rule["values"]:
            return rule["id"], rule["reason"]
        if rule["kind"] == "directory_segment_regex" and re.fullmatch(rule["pattern"], name):
            return rule["id"], rule["reason"]
    return None


def discover(repo_root: Path, kind: str, rules: dict[str, Any]) -> dict[str, Any]:
    discovery = rules["discovery"]
    root = repo_root / discovery[f"{kind}_root"]
    started = time.monotonic()
    ledger: dict[str, Any] = {
        "root": repo_relative(root, repo_root),
        "selected": [],
        "loaded": [],
        "failed": [],
        "omitted": [],
        "excluded": [],
        "complete_enumeration": True,
    }
    if not root.is_dir():
        ledger["failed"].append({"path": repo_relative(root, repo_root), "reason": "missing-root"})
        ledger["complete_enumeration"] = False
        return ledger
    stack = [root]
    symlink_rule = next(rule for rule in discovery["rules"] if rule["kind"] == "symlink")
    agent_generator = next(
        rule for rule in discovery["rules"] if rule["kind"] == "agent_basename_regex"
    )
    while stack:
        if time.monotonic() - started > float(rules["budgets"]["maximum_wall_seconds"]):
            ledger["failed"].append(
                {"path": repo_relative(stack[-1], repo_root), "reason": "enumeration-timeout-unknown-descendants"}
            )
            ledger["complete_enumeration"] = False
            break
        directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: path_key(item.name))
        except OSError as exc:
            ledger["failed"].append(
                {"path": repo_relative(directory, repo_root), "reason": f"unreadable-prefix:{exc.__class__.__name__}"}
            )
            ledger["complete_enumeration"] = False
            continue
        for entry in entries:
            path = Path(entry.path)
            rel = repo_relative(path, repo_root)
            try:
                if entry.is_symlink():
                    try:
                        target = path.resolve(strict=False).as_posix()
                    except OSError:
                        target = "UNRESOLVED"
                    ledger["excluded"].append(
                        {"path": rel, "rule_id": symlink_rule["id"], "reason": symlink_rule["reason"], "resolved_target": target}
                    )
                    continue
                if entry.is_dir(follow_symlinks=False):
                    excluded = _excluded_directory(entry.name, discovery)
                    if excluded:
                        ledger["excluded"].append(
                            {"path": rel, "rule_id": excluded[0], "reason": excluded[1]}
                        )
                    else:
                        stack.append(path)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                if kind == "skill" and entry.name == discovery["skill_file"]:
                    ledger["selected"].append(rel)
                elif kind == "agent" and entry.name.endswith(discovery["agent_suffix"]):
                    if re.fullmatch(agent_generator["pattern"], entry.name):
                        ledger["excluded"].append(
                            {"path": rel, "rule_id": agent_generator["id"], "reason": agent_generator["reason"]}
                        )
                    else:
                        ledger["selected"].append(rel)
            except OSError as exc:
                ledger["failed"].append({"path": rel, "reason": f"lstat-error:{exc.__class__.__name__}"})
                ledger["complete_enumeration"] = False
    ledger["selected"].sort(key=path_key)
    ledger["excluded"].sort(key=lambda row: path_key(row["path"]))
    ledger["failed"].sort(key=lambda row: path_key(row["path"]))
    return ledger


def load_selected(repo_root: Path, ledger: dict[str, Any], rules: dict[str, Any]) -> dict[str, bytes]:
    budgets = rules["budgets"]
    accepted: list[tuple[str, Path]] = []
    total_bytes = 0
    for index, rel in enumerate(ledger["selected"]):
        path = repo_root / rel
        if index >= int(budgets["maximum_candidate_files"]):
            ledger["omitted"].append({"path": rel, "reason": "maximum-candidate-files"})
            continue
        try:
            size = path.stat().st_size
        except OSError as exc:
            ledger["failed"].append({"path": rel, "reason": f"stat-error:{exc.__class__.__name__}"})
            continue
        if size > int(budgets["maximum_file_bytes"]):
            ledger["omitted"].append({"path": rel, "reason": "maximum-file-bytes", "bytes": size})
            continue
        if total_bytes + size > int(budgets["maximum_total_bytes"]):
            ledger["omitted"].append({"path": rel, "reason": "maximum-total-bytes", "bytes": size})
            continue
        total_bytes += size
        accepted.append((rel, path))

    loaded: dict[str, bytes] = {}
    started = time.monotonic()
    workers = max(1, int(budgets["maximum_concurrency"]))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [(rel, pool.submit(path.read_bytes)) for rel, path in accepted]
        for rel, future in futures:
            remaining = float(budgets["maximum_wall_seconds"]) - (time.monotonic() - started)
            timeout = min(float(budgets["maximum_per_file_seconds"]), max(0.0, remaining))
            try:
                data = future.result(timeout=timeout)
                loaded[rel] = data
                ledger["loaded"].append({"path": rel, "bytes": len(data)})
            except FutureTimeout:
                ledger["failed"].append({"path": rel, "reason": "read-timeout"})
            except OSError as exc:
                ledger["failed"].append({"path": rel, "reason": f"read-error:{exc.__class__.__name__}"})
    for key in ("loaded", "failed", "omitted"):
        ledger[key].sort(key=lambda row: path_key(row["path"]))
    ledger["budget"] = dict(budgets)
    ledger["selected_bytes_admitted"] = total_bytes
    return loaded


def parse_frontmatter_name(data: bytes) -> Any:
    text = data.decode("utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("frontmatter-missing")
    name_match = re.search(r"(?m)^name:\s*(?:\"([^\"]*)\"|'([^']*)'|([^#\r\n]*?))\s*$", match.group(1))
    if not name_match:
        raise ValueError("frontmatter-name-missing")
    return next(value for value in name_match.groups() if value is not None)


def markdown_findings(text: str, rel: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    placeholder = rules["placeholder_rules"]
    template_labels = tuple(label.casefold() for label in placeholder["template_labels"])
    allowed_legacy = tuple(label.casefold() for label in rules["legacy_allowed_contexts"]["heading_or_fence_labels"])
    structured = set(placeholder["structured_fence_languages"])
    findings: list[dict[str, Any]] = []
    heading = ""
    in_fence = False
    fence_info = ""
    in_frontmatter = False
    for number, line in enumerate(text.splitlines(), 1):
        if number == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            continue
        heading_match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading_match and not in_fence:
            heading = heading_match.group(1).casefold()
        fence_match = re.match(r"^\s*(```+|~~~+)\s*(.*?)\s*$", line)
        if fence_match:
            if in_fence:
                in_fence = False
                fence_info = ""
            else:
                in_fence = True
                fence_info = (fence_match.group(2) or "").casefold()
            continue
        context = " ".join(part for part in (heading, fence_info) if part)
        template_scope = any(label in context for label in template_labels)
        legacy_exception = any(label in context for label in allowed_legacy)
        fence_language = fence_info.split()[0] if fence_info else ""
        structured_active = in_fence and fence_language in structured and not template_scope
        for pattern in placeholder["sentinel_patterns"]:
            for match in re.finditer(pattern, line):
                outcome = "PASS" if template_scope else "FAIL"
                findings.append(_finding("PH-001-ACTIVE-SENTINEL", outcome, rel, number, match.group(0), context))
                if template_scope:
                    findings.append(_finding("PH-003-TEMPLATE-SCOPE", "PASS", rel, number, match.group(0), context))
        for pattern in placeholder["metavariable_patterns"]:
            for match in re.finditer(pattern, line):
                inline_code = any(
                    start <= match.start() and match.end() <= end
                    for start, end in ((item.start() + 1, item.end() - 1) for item in re.finditer(r"`[^`]*`", line))
                )
                structured_path_pattern = bool(
                    structured_active
                    and "/" in line
                    and re.match(r"^\s*(?:path|paths|reads|writes|never_writes|output|input)[a-z_]*\s*:", line)
                )
                if structured_active and not structured_path_pattern:
                    rule_id, outcome = "PH-004-ACTIVE-STRUCTURED", "FAIL"
                elif template_scope or inline_code or structured_path_pattern:
                    rule_id, outcome = "PH-002-DECLARED-METAVARIABLE", "PASS"
                else:
                    rule_id, outcome = "PH-002-DECLARED-METAVARIABLE", "FAIL"
                findings.append(_finding(rule_id, outcome, rel, number, match.group(0), context))
                if template_scope:
                    findings.append(_finding("PH-003-TEMPLATE-SCOPE", "PASS", rel, number, match.group(0), context))
        for legacy in rules["legacy_rules"]:
            if legacy["id"] == "LEG-002-CLAUDE-FRONTMATTER" and not in_frontmatter:
                continue
            for pattern in legacy["patterns"]:
                match = re.search(pattern, line)
                if match:
                    outcome = "PASS" if legacy_exception else legacy["severity"]
                    findings.append(_finding(legacy["id"], outcome, rel, number, match.group(0), context))
    return findings


def _finding(rule_id: str, outcome: str, path: str, line: int, token: str, context: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "axis": "target",
        "outcome": outcome,
        "path": path,
        "line": line,
        "token": token,
        "context": context or "active-prose",
    }


def aggregate(outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    trace: list[str] = []
    if not outcomes:
        return {"validation": "TEST_INFRA_INVALID", "trace": ["empty-required-rule-set"]}
    if any(row["axis"] == "authority" and row["outcome"] == "INVALID" for row in outcomes):
        trace.append("required-authority-invalid")
        return {"validation": "TEST_INFRA_INVALID", "trace": trace}
    if any(row["axis"] == "target" and row["outcome"] in {"FAIL", "INVALID"} for row in outcomes):
        trace.append("conclusive-target-fail")
        if any(row["outcome"] == "PARTIAL" for row in outcomes):
            trace.append("partial-axis-retained-but-lower-priority")
        return {"validation": "NON-COMPLIANT", "trace": trace}
    if any(row["outcome"] == "PARTIAL" for row in outcomes):
        return {"validation": "PARTIAL_VALIDATION", "trace": ["coverage-partial"]}
    if any(row["outcome"] == "WARN" for row in outcomes):
        return {"validation": "WARNINGS", "trace": ["complete-coverage-with-warning"]}
    if all(row["outcome"] == "PASS" for row in outcomes):
        return {"validation": "COMPLIANT", "trace": ["all-required-pass"]}
    return {"validation": "TEST_INFRA_INVALID", "trace": ["unknown-outcome-vector"]}


def ledger_outcomes(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    if ledger["failed"] or ledger["omitted"] or not ledger["complete_enumeration"]:
        return [{"rule_id": "DISC-LEDGER", "axis": "coverage", "outcome": "PARTIAL"}]
    return [{"rule_id": "DISC-LEDGER", "axis": "coverage", "outcome": "PASS"}]


def parse_catalog(data: bytes, policy: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {"skills": [], "agents": []}
    section: str | None = None
    current: dict[str, Any] | None = None
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        top = re.match(r"^(skills|agents):\s*$", line)
        if top:
            section = top.group(1)
            current = None
            continue
        item = re.match(r"^  - name:\s*(.*?)\s*$", line)
        if section and item:
            raw = item.group(1).strip('"\'')
            current = {"source": f"CGS Skill Testing Framework/catalog.yaml:{number}", "name": canonical_name(raw, policy)}
            result[section].append(current)
            continue
        spec = re.match(r"^    spec:\s*(.*?)\s*$", line)
        if current is not None and spec:
            current["spec"] = spec.group(1).strip('"\'')
    return result


def verify_manifest(repo_root: Path, manifest_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest, _ = read_json_yaml(manifest_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return {"valid": False, "errors": [f"manifest-load:{exc.__class__.__name__}"]}
    if manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append("manifest-schema")
    if manifest.get("version") != RUNNER_VERSION:
        errors.append("manifest-version")
    for field in ("runner", "rules"):
        item = manifest.get(field)
        if not isinstance(item, dict):
            errors.append(f"{field}-record")
            continue
        try:
            path = (repo_root / item["path"]).resolve(strict=True)
            path.relative_to(repo_root.resolve(strict=True))
            if not path.is_file():
                errors.append(f"{field}-path")
            if item.get("version") != RUNNER_VERSION:
                errors.append(f"{field}-version")
            if field == "rules":
                parsed, _ = read_json_yaml(path)
                if parsed.get("schema") != RULES_SCHEMA or parsed.get("version") != item.get("version"):
                    errors.append("rules-schema-version")
        except (KeyError, OSError, ValueError):
            errors.append(f"{field}-path")
    allowed = manifest.get("allowed_argv")
    if not isinstance(allowed, list) or not allowed:
        errors.append("allowed-argv")
    output = manifest.get("output_schema")
    if output != OUTPUT_SCHEMA:
        errors.append("output-schema")
    interpreter = manifest.get("interpreter")
    if not isinstance(interpreter, dict):
        errors.append("interpreter-record")
    else:
        current = tuple(sys.version_info[:3])
        minimum = tuple(int(part) for part in interpreter.get("minimum_version", "0.0.0").split("."))
        maximum = tuple(int(part) for part in interpreter.get("maximum_exclusive_version", "0.0.0").split("."))
        if not (minimum <= current < maximum):
            errors.append("interpreter-version")
    if not isinstance(manifest.get("timeout_seconds"), (int, float)) or manifest["timeout_seconds"] <= 0:
        errors.append("timeout")
    if manifest.get("writes") != []:
        errors.append("writes-not-empty")
    return {"valid": not errors, "errors": errors, "manifest": manifest}


def run_static(repo_root: Path, target: str, rules: dict[str, Any]) -> dict[str, Any]:
    ledger = discover(repo_root, "skill", rules)
    loaded = load_selected(repo_root, ledger, rules)
    policy = rules["name_policy"]
    records: list[dict[str, Any]] = []
    outcomes = ledger_outcomes(ledger)
    findings: list[dict[str, Any]] = []
    for rel, data in loaded.items():
        try:
            raw = parse_frontmatter_name(data)
            records.append({"source": rel, "name": canonical_name(raw, policy), "data": data})
        except (UnicodeError, ValueError) as exc:
            findings.append({"rule_id": "NAME-001-FRONTMATTER", "axis": "target", "outcome": "FAIL", "path": rel, "message": str(exc)})
    if target == "all":
        duplicates = duplicate_rows(records)
        if duplicates:
            findings.append({"rule_id": "NAME-008-DUPLICATE", "axis": "target", "outcome": "FAIL", "duplicates": duplicates})
        matches = records
    else:
        target_key = canonical_name(target, policy)["key"]
        matches = [row for row in records if row["name"]["key"] == target_key]
        if len(matches) != 1:
            findings.append({"rule_id": "NAME-009-TARGET-RESOLUTION", "axis": "target", "outcome": "FAIL", "message": f"expected one target, found {len(matches)}"})
            matches = []
    for row in matches:
        if not row["name"]["valid"]:
            findings.append({"rule_id": "NAME-VALIDATION", "axis": "target", "outcome": "FAIL", "path": row["source"], "message": row["name"]["errors"]})
        findings.extend(markdown_findings(row["data"].decode("utf-8"), row["source"], rules))
    outcomes.extend({"rule_id": row["rule_id"], "axis": row["axis"], "outcome": row["outcome"]} for row in findings)
    if not findings:
        outcomes.append({"rule_id": "P1-RULES", "axis": "target", "outcome": "PASS"})
    return {"ledger": ledger, "findings": findings, "aggregation": aggregate(outcomes)}


def run_audit(repo_root: Path, rules: dict[str, Any]) -> dict[str, Any]:
    policy = rules["name_policy"]
    skill_ledger = discover(repo_root, "skill", rules)
    agent_ledger = discover(repo_root, "agent", rules)
    skill_data = load_selected(repo_root, skill_ledger, rules)
    agent_data = load_selected(repo_root, agent_ledger, rules)
    outcomes = ledger_outcomes(skill_ledger) + ledger_outcomes(agent_ledger)
    findings: list[dict[str, Any]] = []
    implementations: dict[str, list[dict[str, Any]]] = {"skills": [], "agents": []}
    for rel, data in skill_data.items():
        try:
            implementations["skills"].append({"source": rel, "name": canonical_name(parse_frontmatter_name(data), policy)})
        except (UnicodeError, ValueError) as exc:
            findings.append({"rule_id": "NAME-001-FRONTMATTER", "axis": "target", "outcome": "FAIL", "path": rel, "message": str(exc)})
    for rel in agent_data:
        implementations["agents"].append({"source": rel, "name": canonical_name(Path(rel).stem, policy)})
    catalog_path = repo_root / "CGS Skill Testing Framework/catalog.yaml"
    try:
        catalog = parse_catalog(catalog_path.read_bytes(), policy)
    except (OSError, UnicodeError) as exc:
        catalog = {"skills": [], "agents": []}
        outcomes.append({"rule_id": "CATALOG-LOAD", "axis": "authority", "outcome": "INVALID"})
        findings.append({"rule_id": "CATALOG-LOAD", "axis": "authority", "outcome": "INVALID", "message": str(exc)})
    sets: dict[str, Any] = {}
    for section in ("skills", "agents"):
        impl_dups = duplicate_rows(implementations[section])
        catalog_dups = duplicate_rows(catalog[section])
        aliases = path_alias_rows(repo_root, (row["source"] for row in implementations[section]))
        impl_keys = {row["name"]["key"] for row in implementations[section] if row["name"]["valid"]}
        catalog_keys = {row["name"]["key"] for row in catalog[section] if row["name"]["valid"]}
        invalid = [row for row in implementations[section] + catalog[section] if not row["name"]["valid"]]
        missing_specs = []
        missing_metadata = []
        for row in catalog[section]:
            spec = row.get("spec")
            if not spec or not (repo_root / spec).is_file():
                missing_specs.append({"name": row["name"]["raw"], "spec": spec})
        if section == "skills":
            for row in implementations[section]:
                metadata = (repo_root / row["source"]).parent / rules["discovery"]["skill_metadata"]
                if not metadata.is_file():
                    missing_metadata.append(repo_relative(metadata, repo_root))
        sets[section] = {
            "implementation": sorted(impl_keys),
            "catalog": sorted(catalog_keys),
            "missing_from_catalog": sorted(impl_keys - catalog_keys),
            "extra_in_catalog": sorted(catalog_keys - impl_keys),
            "duplicates": {"implementation": impl_dups, "catalog": catalog_dups},
            "path_alias": aliases,
            "invalid_names": [{"source": row["source"], "errors": row["name"]["errors"]} for row in invalid],
            "missing_metadata_or_spec": sorted(missing_metadata, key=path_key) + missing_specs,
        }
        failed = any((impl_dups, catalog_dups, aliases, impl_keys - catalog_keys, catalog_keys - impl_keys, invalid, missing_specs, missing_metadata))
        outcomes.append({"rule_id": f"AUDIT-{section.upper()}-SETS", "axis": "target", "outcome": "FAIL" if failed else "PASS"})
    aggregation = aggregate(outcomes)
    return {"ledger": {"skills": skill_ledger, "agents": agent_ledger}, "sets": sets, "findings": findings, "aggregation": aggregation}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--mode", required=True, choices=("static", "audit", "manifest"))
    parser.add_argument("--target")
    return parser


def allowed_argv(argv: list[str]) -> bool:
    if len(argv) == 4:
        return argv[0] == "--repo-root" and argv[2:4] in (["--mode", "audit"], ["--mode", "manifest"])
    if len(argv) == 6:
        return (
            argv[0] == "--repo-root"
            and argv[2:4] == ["--mode", "static"]
            and argv[4] == "--target"
            and bool(argv[5])
        )
    return False


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if not allowed_argv(raw_argv):
        raise ValueError("argv is not an allowed manifest template")
    args = build_parser().parse_args(raw_argv)
    repo_root = Path(args.repo_root).resolve(strict=True)
    manifest_path = repo_root / ".agents/skills/skill-test/validator-manifest-v1.yaml"
    manifest_result = verify_manifest(repo_root, manifest_path)
    if args.mode == "manifest":
        payload = {"schema": OUTPUT_SCHEMA, "mode": "manifest", "manifest_validation": manifest_result}
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return 0
    rules, _ = read_json_yaml(repo_root / ".agents/skills/skill-test/rules-v1.yaml")
    if rules.get("schema") != RULES_SCHEMA:
        raise ValueError("rules schema mismatch")
    if args.mode == "static":
        if not args.target:
            raise ValueError("--target is required for static mode")
        result = run_static(repo_root, args.target, rules)
    else:
        result = run_audit(repo_root, rules)
    if not manifest_result["valid"]:
        result["manifest_validation"] = manifest_result
        current = result["aggregation"]
        if current["validation"] not in {"TEST_INFRA_INVALID", "NON-COMPLIANT"}:
            result["aggregation"] = {
                "validation": "PARTIAL_VALIDATION",
                "trace": current["trace"] + ["VAL-001-PINNED-RUNNER"],
            }
    payload = {
        "schema": OUTPUT_SCHEMA,
        "mode": args.mode,
        "rules": {"schema": rules["schema"], "version": rules["version"], "path": ".agents/skills/skill-test/rules-v1.yaml"},
        **result,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # fail closed with machine-readable stderr
        print(json.dumps({"schema": OUTPUT_SCHEMA, "error": exc.__class__.__name__, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(2)
