#!/bin/bash
# Codex PostToolUse hook: validate asset files affected by apply_patch.
# Checks naming conventions for files in assets/ directory
#
# Exit behavior:
#   exit 0 = success or advisory warnings only (non-blocking)
#   exit 2 = report a build-breaking validation failure (the completed edit is not rolled back)
#
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
read_hook_input
PATHS=$(tool_paths)
select_hook_python

[ -z "$PATHS" ] && exit 0

WARNINGS=""   # Style/convention issues -- exit 0 with advisory message
ERRORS=""     # Build-breaking issues reported after the tool call

while IFS= read -r FILE_PATH; do
    FILE_PATH=${FILE_PATH//\\//}
    if ! echo "$FILE_PATH" | grep -qE '(^|/)assets/'; then
        continue
    fi

    FILENAME=$(basename "$FILE_PATH")
    RESOLVED_PATH=$(resolve_path "$FILE_PATH")

    # Naming issues are advisory.
    if echo "$FILENAME" | grep -qE '[A-Z[:space:]-]'; then
        WARNINGS="$WARNINGS\n  NAMING: $FILE_PATH must be lowercase with underscores (got: $FILENAME)"
    fi

    # Invalid JSON in assets/data is build-breaking.
    if echo "$FILE_PATH" | grep -qE '(^|/)assets/data/.*\.json$' && [ -f "$RESOLVED_PATH" ]; then
        if [ ${#HOOK_PYTHON_CMD[@]} -gt 0 ]; then
            "${HOOK_PYTHON_CMD[@]}" -m json.tool "$RESOLVED_PATH" >/dev/null 2>&1 || ERRORS="$ERRORS\n  FORMAT: $FILE_PATH is not valid JSON"
        fi
    fi
done <<< "$PATHS"

# Report errors and block if any build-breaking issues found
if [ -n "$ERRORS" ]; then
    echo -e "=== Asset Validation: ERRORS (Blocking) ===$ERRORS\n===========================================\nFix these errors before proceeding." >&2
    exit 2
fi

# Report warnings with the supported PostToolUse JSON feedback shape.
if [ -n "$WARNINGS" ]; then
    MESSAGE=$(printf "=== Asset Validation: Warnings ===%b\nWarnings are advisory. Fix before final commit." "$WARNINGS")
    emit_hook_context "PostToolUse" "$MESSAGE"
fi

exit 0
