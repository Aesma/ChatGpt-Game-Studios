#!/usr/bin/env bash
# Shared helpers for project-local Codex command hooks.

HOOK_INPUT=""
HOOK_PYTHON_CMD=()

read_hook_input() {
  HOOK_INPUT=$(cat)
}

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

select_hook_python() {
  HOOK_PYTHON_CMD=()
  if command -v python3 >/dev/null 2>&1 &&
      printf '{"ok":true}' | python3 -c 'import json, sys; assert json.load(sys.stdin)["ok"] is True' >/dev/null 2>&1; then
    HOOK_PYTHON_CMD=(python3)
  elif command -v python >/dev/null 2>&1 &&
      printf '{"ok":true}' | python -c 'import json, sys; assert json.load(sys.stdin)["ok"] is True' >/dev/null 2>&1; then
    HOOK_PYTHON_CMD=(python)
  elif command -v py >/dev/null 2>&1 &&
      printf '{"ok":true}' | py -3 -c 'import json, sys; assert json.load(sys.stdin)["ok"] is True' >/dev/null 2>&1; then
    HOOK_PYTHON_CMD=(py -3)
  fi
}

json_path() {
  local dotted_path="$1"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$HOOK_INPUT" | jq -r ".${dotted_path} // empty" 2>/dev/null
    return
  fi

  select_hook_python
  if [ ${#HOOK_PYTHON_CMD[@]} -gt 0 ]; then
    printf '%s' "$HOOK_INPUT" | "${HOOK_PYTHON_CMD[@]}" -c '
import json, sys
try:
    value = json.load(sys.stdin)
    for part in sys.argv[1].split("."):
        value = value.get(part) if isinstance(value, dict) else None
    if value is not None and not isinstance(value, (dict, list)):
        print(value)
except Exception:
    pass
' "$dotted_path" 2>/dev/null
    return
  fi

  local leaf="${dotted_path##*.}"
  printf '%s' "$HOOK_INPUT" |
    sed -n "s/.*\"${leaf}\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" |
    head -n 1
}

tool_command() {
  json_path "tool_input.command"
}

tool_paths() {
  select_hook_python
  if [ ${#HOOK_PYTHON_CMD[@]} -gt 0 ]; then
    printf '%s' "$HOOK_INPUT" | "${HOOK_PYTHON_CMD[@]}" -c '
import json, re, sys
try:
    data = json.load(sys.stdin)
except Exception:
    raise SystemExit(0)
tool_input = data.get("tool_input", {})
values, payloads = [], []
if isinstance(tool_input, str):
    payloads.append(tool_input)
elif isinstance(tool_input, dict):
    for key in ("file_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str): values.append(value)
    paths = tool_input.get("paths")
    if isinstance(paths, list): values.extend(v for v in paths if isinstance(v, str))
    for key in ("command", "patch", "input"):
        value = tool_input.get(key)
        if isinstance(value, str): payloads.append(value)
for payload in payloads:
    for line in payload.splitlines():
        match = re.match(r"^(?:\*\*\* (?:Add|Update|Delete) File:|\+\+\+ b/|--- a/)\s*(.+?)\s*$", line)
        if match and match.group(1) != "/dev/null": values.append(match.group(1))
seen = set()
for value in values:
    value = value.replace("\\", "/")
    if value not in seen:
        seen.add(value)
        print(value)
' 2>/dev/null
    return
  fi

  printf '%s\n' "$HOOK_INPUT" |
    sed -n -E 's/^.*(\*\*\* (Add|Update|Delete) File:|\+\+\+ b\/|--- a\/)[[:space:]]*([^"\\n]+).*$/\3/p'
}

resolve_path() {
  local value="${1//\\//}"
  case "$value" in
    /*|[A-Za-z]:/*) printf '%s\n' "$value" ;;
    *) printf '%s/%s\n' "$(repo_root)" "$value" ;;
  esac
}

json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\r'/\\r}
  value=${value//$'\n'/\\n}
  value=${value//$'\t'/\\t}
  printf '%s' "$value"
}

emit_continue_json() {
  local message="${1:-}"
  if [ -n "$message" ]; then
    printf '{"continue":true,"systemMessage":"%s"}\n' "$(json_escape "$message")"
  else
    printf '{"continue":true}\n'
  fi
}

emit_hook_context() {
  local event_name="$1"
  local message="$2"
  printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"%s","additionalContext":"%s"}}\n' \
    "$(json_escape "$message")" \
    "$(json_escape "$event_name")" \
    "$(json_escape "$message")"
}
