#!/bin/bash
# Codex PreToolUse hook: validate git push commands.
# Warns on pushes to protected branches
# Exit 0 = allow, Exit 2 = block
#
# Codex input schema (PreToolUse for Bash):
# { "tool_name": "Bash", "tool_input": { "command": "git push origin main" } }

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
read_hook_input
COMMAND=$(tool_command)
cd "$(repo_root)" || exit 0

# Only process git push commands
if ! echo "$COMMAND" | grep -qE '^git[[:space:]]+push'; then
    exit 0
fi

if echo "$COMMAND" | grep -qE '(^|[[:space:]])(-f|--force|--force-with-lease)([=[:space:]]|$)'; then
    echo "BLOCKED: force-push variants are disabled by project policy." >&2
    exit 2
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
MATCHED_BRANCH=""

# Check if pushing to a protected branch
for branch in develop main master; do
    if [ "$CURRENT_BRANCH" = "$branch" ]; then
        MATCHED_BRANCH="$branch"
        break
    fi
    # Also check if pushing to a protected branch explicitly (quote branch name for safety)
    if echo "$COMMAND" | grep -qE "[[:space:]]${branch}([[:space:]]|$)"; then
        MATCHED_BRANCH="$branch"
        break
    fi
done

if [ -n "$MATCHED_BRANCH" ]; then
    MESSAGE="Push to protected branch '$MATCHED_BRANCH' detected. Ensure the build and unit tests pass and no S1/S2 bugs remain."
    emit_hook_context "PreToolUse" "$MESSAGE"
fi

exit 0
