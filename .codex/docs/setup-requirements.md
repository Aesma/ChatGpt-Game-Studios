# Setup Requirements

This template requires a few tools to be installed for full functionality.
All hooks fail gracefully if tools are missing — nothing will break, but
you'll lose validation features.

## Required

| Tool | Purpose | Install |
| ---- | ---- | ---- |
| **Git** | Version control, branch management | [git-scm.com](https://git-scm.com/) |
| **Codex** | Coding agent CLI | `npm install -g @openai/codex` ([official Codex docs](https://learn.chatgpt.com/docs/codex)) |

## Recommended

| Tool | Used By | Purpose | Install |
| ---- | ---- | ---- | ---- |
| **jq** | Hook scripts | JSON parsing in commit, push, asset, and subagent hooks | See below |
| **Python 3** | Validation scripts | JSON validation and portable helper scripts | [python.org](https://www.python.org/) |
| **Bash** | Shell hooks | Runs the migrated `.codex/hooks/*.sh` scripts | Included with Git for Windows |

### Installing jq

**Windows** (any of these):
```
winget install jqlang.jq
choco install jq
scoop install jq
```

**macOS**:
```
brew install jq
```

**Linux**:
```
sudo apt install jq     # Debian/Ubuntu
sudo dnf install jq     # Fedora
sudo pacman -S jq       # Arch
```

## Platform Notes

### Windows
- Git for Windows includes **Git Bash**, which provides the `bash` command used
  by shell hooks registered in `.codex/hooks.json`
- Ensure Git Bash is on your PATH (default if installed via the Git installer)
- Hook commands use `bash .codex/hooks/[name].sh`; confirm `bash.exe` is
  discoverable from the environment that starts Codex

### macOS / Linux
- Bash is available natively
- Install `jq` via your package manager for full hook support

## Verifying Your Setup

Run these commands to check prerequisites:

```bash
git --version          # Should show git version
codex --version        # Should show the installed Codex CLI version
bash --version         # Should show bash version
jq --version           # Should show jq version (optional)
python3 --version      # Should show python version (optional)
```

## What Happens Without Optional Tools

| Missing Tool | Effect |
| ---- | ---- |
| **jq** | Hooks fall back to Python for structured JSON extraction; commit, push, asset, and agent-audit checks continue. |
| **Python 3** | Hooks use `jq` when available; Python-only JSON validation and the quote-aware supplemental command parser are unavailable. |
| **Both** | A limited `sed` fallback preserves simple command/path extraction and basic checks, but structured parsing and JSON validation are reduced. The sandbox and execpolicy still apply. |

## Recommended IDE

Codex can run through the [CLI](https://learn.chatgpt.com/docs/codex/cli), the
[IDE extension](https://learn.chatgpt.com/docs/codex/ide), or the ChatGPT desktop
app. The repository behavior comes from the same `AGENTS.md`, skills, trusted
project config, and hook files across supported local surfaces.
