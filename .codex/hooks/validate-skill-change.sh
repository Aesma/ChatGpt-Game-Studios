#!/bin/bash
# Codex PostToolUse hook: advise validation after skill changes.
# Handles apply_patch command payloads as well as file_path/path inputs.
#
# Exit behavior:
#   exit 0 = advisory only (non-blocking)
#
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
read_hook_input
PATHS=$(tool_paths)
ADVICE=""

while IFS= read -r FILE_PATH; do
    FILE_PATH=${FILE_PATH//\\//}
    if ! echo "$FILE_PATH" | grep -qE '(^|/)\.agents/skills/'; then
        continue
    fi

    SKILL_NAME=$(echo "$FILE_PATH" | sed -nE 's|^.*\.agents/skills/([^/]+).*$|\1|p')
    [ -z "$SKILL_NAME" ] && continue

    ADVICE="$ADVICE\nSkill modified: $SKILL_NAME. Use \$skill-test for a static check."
done <<< "$PATHS"

if [ -n "$ADVICE" ]; then
    MESSAGE=$(printf "Skill validation reminder:%b" "$ADVICE")
    emit_hook_context "PostToolUse" "$MESSAGE"
fi

exit 0
