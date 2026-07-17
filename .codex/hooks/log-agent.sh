#!/bin/bash
# Codex SubagentStart hook: log agent invocations for an audit trail.
# Tracks which agents are being used and when
#
# Codex stdin includes session_id, turn_id, agent_id, agent_type, cwd,
# permission_mode, and hook_event_name.
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
    echo "$TIMESTAMP | Agent invoked: $AGENT_NAME" >> "$SESSION_LOG_DIR/agent-audit.log" 2>/dev/null
fi

exit 0
