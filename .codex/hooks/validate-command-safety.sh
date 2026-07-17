#!/usr/bin/env bash
# Codex PreToolUse hook: enforce the project shell-command deny policy.
# This is the runtime permissions layer for Bash commands, not a compatibility
# shim for notification hooks. Exit 2 blocks the pending command.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
read_hook_input
COMMAND=$(tool_command)

[ -z "$COMMAND" ] && exit 0

select_hook_python
if [ ${#HOOK_PYTHON_CMD[@]} -eq 0 ]; then
  emit_hook_context "PreToolUse" "Command-safety parser unavailable because Python was not found; rely on the sandbox and execpolicy rules, and avoid destructive shell commands."
  exit 0
fi

printf '%s' "$COMMAND" | "${HOOK_PYTHON_CMD[@]}" -c '
import os
import re
import sys


def tokenize(source):
    """Tokenize shell text while treating separators inside quotes as data."""
    tokens = []
    buffer = []
    state = "normal"
    i = 0

    def flush():
        if buffer:
            tokens.append("".join(buffer))
            buffer.clear()

    while i < len(source):
        char = source[i]
        if state == "single":
            if char == "\x27":
                state = "normal"
            else:
                buffer.append(char)
            i += 1
            continue
        if state == "double":
            if char == "\"":
                state = "normal"
            elif char == "\\" and i + 1 < len(source):
                i += 1
                buffer.append(source[i])
            else:
                buffer.append(char)
            i += 1
            continue

        if char == "\x27":
            state = "single"
        elif char == "\"":
            state = "double"
        elif char == "\\" and i + 1 < len(source):
            i += 1
            buffer.append(source[i])
        elif char == "#" and not buffer:
            while i < len(source) and source[i] not in "\r\n":
                i += 1
            continue
        elif char in " \t\r":
            flush()
        elif char == "\n":
            flush()
            tokens.append(";")
        elif char in ";&|<>":
            flush()
            run = [char]
            while i + 1 < len(source) and source[i + 1] == char:
                i += 1
                run.append(char)
            tokens.append("".join(run))
        else:
            buffer.append(char)
        i += 1
    flush()
    return tokens


def segments(source):
    result = []
    current = []
    for token in tokenize(source):
        if token and all(char in ";&|" for char in token):
            if current:
                result.append(current)
                current = []
        else:
            current.append(token)
    if current:
        result.append(current)
    return result


def is_env_path(value):
    value = value.rstrip(",;)")
    return os.path.basename(value.replace("\\", "/")).lower().startswith(".env")


def executable_tokens(part):
    index = 0
    while index < len(part) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", part[index]):
        index += 1
    tokens = part[index:]
    while tokens and tokens[0].lower() in {"command", "builtin", "nohup"}:
        tokens = tokens[1:]
    if tokens and tokens[0].lower() == "env":
        tokens = tokens[1:]
        while tokens and (tokens[0].startswith("-") or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0])):
            tokens = tokens[1:]
    return tokens


def inspect(source, depth=0):
    if depth > 4:
        return None
    for part in segments(source):
        lower = [token.lower() for token in part]

        for index, token in enumerate(part[:-1]):
            if token in {">", ">>", "<", "<<"} and is_env_path(part[index + 1]):
                return "redirection involving a .env* file"

        command = executable_tokens(part)
        if not command:
            continue
        exe = os.path.basename(command[0].replace("\\", "/")).lower()
        args = command[1:]
        args_lower = [arg.lower() for arg in args]

        if exe in {"sudo", "sudo.exe"}:
            return "sudo elevation"

        if exe in {"rm", "rm.exe"}:
            flags = "".join(arg[1:] for arg in args if arg.startswith("-") and not arg.startswith("--"))
            if "r" in flags.lower() and "f" in flags.lower():
                return "recursive forced deletion"

        if exe in {"remove-item", "remove-item.exe"}:
            if "-recurse" in args_lower and "-force" in args_lower:
                return "recursive forced deletion"

        if exe in {"chmod", "chmod.exe"} and args and args[0] in {"777", "0777"}:
            return "world-writable chmod"

        if exe in {"cat", "cat.exe", "type", "type.exe", "get-content"}:
            if any(is_env_path(arg) for arg in args if not arg.startswith("-")):
                return "reading a .env* file through the shell"

        if exe in {"git", "git.exe"}:
            if "push" in args_lower:
                push_index = args_lower.index("push")
                push_args = args_lower[push_index + 1:]
                if any(arg in {"-f", "--force"} or arg.startswith("--force-with-lease") for arg in push_args):
                    return "force push"
            if "reset" in args_lower:
                reset_index = args_lower.index("reset")
                if "--hard" in args_lower[reset_index + 1:]:
                    return "hard git reset"
            if "clean" in args_lower:
                clean_index = args_lower.index("clean")
                clean_args = args_lower[clean_index + 1:]
                if any(arg.startswith("-") and "f" in arg.lower().lstrip("-") for arg in clean_args):
                    return "forced git clean"

        nested_markers = {
            "bash": {"-c", "-lc"},
            "bash.exe": {"-c", "-lc"},
            "sh": {"-c", "-lc"},
            "sh.exe": {"-c", "-lc"},
            "powershell": {"-command", "-c"},
            "powershell.exe": {"-command", "-c"},
            "pwsh": {"-command", "-c"},
            "pwsh.exe": {"-command", "-c"},
            "cmd": {"/c"},
            "cmd.exe": {"/c"},
        }
        if exe in nested_markers:
            for index, arg in enumerate(args_lower):
                if arg in nested_markers[exe] and index + 1 < len(args):
                    finding = inspect(args[index + 1], depth + 1)
                    if finding:
                        return finding
                    break
    return None


finding = inspect(sys.stdin.read())
if finding:
    print(f"BLOCKED: project command-safety policy rejected {finding}.", file=sys.stderr)
    raise SystemExit(2)
'
exit $?
