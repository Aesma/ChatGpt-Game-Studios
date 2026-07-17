#!/usr/bin/env bash
# Codex PostCompact hook: restore repository-scoped session guidance.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
cd "$(repo_root)" || exit 0

ACTIVE="production/session-state/active.md"

MESSAGE="=== Context Restored After Compaction ==="

if [ -f "$ACTIVE" ]; then
  SIZE=$(wc -l < "$ACTIVE" 2>/dev/null || echo "?")
  MESSAGE="$MESSAGE
Session state file exists: $ACTIVE ($SIZE lines)
IMPORTANT: Read this file now to restore your working context.
It contains: current task, decisions made, files in progress, open questions."
else
  MESSAGE="$MESSAGE
No session state file found at $ACTIVE.
If work was interrupted, check production/session-logs/ for the last session audit."
fi

emit_continue_json "$MESSAGE"
