#!/bin/bash
# Codex SubagentStop hook: log agent completion for an audit trail.
# Tracks when agents finish and their outcome
#
# Codex stdin uses agent_type for the custom subagent profile.
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=hook-lib.sh
source "$SCRIPT_DIR/hook-lib.sh"
read_hook_input
AGENT_NAME=$(json_path "agent_type")
[ -z "$AGENT_NAME" ] && AGENT_NAME="unknown"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG_DIR="$(repo_root)/production/session-logs"

if [ "${CGS_HOOK_DRY_RUN:-0}" != "1" ]; then
    mkdir -p "$SESSION_LOG_DIR" 2>/dev/null
    echo "$TIMESTAMP | Agent completed: $AGENT_NAME" >> "$SESSION_LOG_DIR/agent-audit.log" 2>/dev/null
fi

# SubagentStop accepts the common Codex JSON output shape.
emit_continue_json

exit 0
