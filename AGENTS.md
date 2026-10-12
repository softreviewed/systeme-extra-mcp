# Install guide for AI assistants

A user gave you this repository link and wants Systeme.io Extra MCP ready to use. Follow these steps in order. Ask the user only where a step says so.

## 0. Ground rules

- Never ask the user to paste their API key into the chat. They type it into a secret prompt (Docker route) or into their own config file (direct route).
- Never print, log or commit the key.
- Add this server next to the user's existing MCP servers. Never replace or delete other entries in a config file; make a backup copy first.
- Make no account changes during setup. Verify with `help` and one read only.

## 1. Pick the route

| Check | Route |
|---|---|
| `docker mcp gateway run --help` works | **A. Docker Gateway** (key stays in Docker's secret store) |
| Otherwise, Python 3.11 or newer is installed (`python --version` or `python3 --version`) | **B. Direct Python** (key goes in the client config file) |
| Neither | Ask the user to install Python 3.11+ (simplest) or Docker Desktop, then restart from step 1 |

## 2. Get the code

```sh
git clone https://github.com/softreviewed/systeme-extra-mcp.git
cd systeme-extra-mcp
```

Use a permanent folder (for example the user's home folder), not a temp folder. Note its absolute path as `REPO`.

## 3A. Docker Gateway route

```sh
docker build -t mcp-systeme-extra:v2 .
```

Copy `docker-catalog.yaml` to `~/.docker/mcp/catalogs/systeme-extra.yaml` (Windows: `%USERPROFILE%\.docker\mcp\catalogs\systeme-extra.yaml`). If that file already exists, back it up first, then overwrite it.

Check: `docker mcp gateway run --catalog systeme-extra.yaml --servers systeme-extra --dry-run` lists 22 tools.

Ask the user to store their key themselves. Windows PowerShell:

```powershell
$k = Read-Host "Systeme.io public API key" -AsSecureString; [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($k)) | docker mcp secret set systeme.api_key
```

macOS / Linux: `read -rs K && printf %s "$K" | docker mcp secret set systeme.api_key; unset K`

Client entry: command `docker`, args `["mcp", "gateway", "run", "--catalog", "systeme-extra.yaml", "--servers", "systeme-extra"]`. Templates: `examples/clients/*.json` and `examples/clients/codex.toml`.

## 3B. Direct Python route

```sh
python -m venv .venv
```

- Windows: `.venv\Scripts\python -m pip install -r requirements-lock.txt`; the Python path is `REPO\.venv\Scripts\python.exe`
- macOS / Linux: `.venv/bin/python -m pip install -r requirements-lock.txt`; the Python path is `REPO/.venv/bin/python`

Client entry: command = that absolute Python path, args = `["REPO/server.py"]` (absolute), env `SYSTEME_API_KEY`. Templates: `examples/clients/direct/`. In JSON on Windows, write paths with forward slashes or doubled backslashes.

Write the entry with `"YOUR_PUBLIC_API_KEY"` as the value, then tell the user which file to open and ask them to replace that placeholder with their key and save.

## 4. Where each client keeps its config

| Client | File or command |
|---|---|
| Claude Desktop | Windows `%APPDATA%\Claude\claude_desktop_config.json`; macOS `~/Library/Application Support/Claude/claude_desktop_config.json` (key `mcpServers`) |
| Claude Code | `claude mcp add --transport stdio --scope user systeme-extra -- <command> <args...>`; for route B add `--env SYSTEME_API_KEY=...` only if the user types it themselves, or edit `~/.claude.json` |
| Codex | `~/.codex/config.toml` (`[mcp_servers.systeme_extra]`) |
| Cursor | `~/.cursor/mcp.json` (key `mcpServers`, `"type": "stdio"`) |
| Google Antigravity | `~/.gemini/config/mcp_config.json` (key `mcpServers`) |
| Other stdio clients | Same command, args and env |

After editing, the user must fully restart the client app.

## 5. The key: which one

The user needs a **Public API key**: Systeme.io → Settings → MCP & API keys → **Public API keys** → Create. The **MCP key** on the same page is for the official Systeme.io MCP and is rejected here with HTTP 401 "Invalid API Key."

## 6. Verify

1. Call `systeme_extra_tags` with `action: "help"`. Expect a list of actions and `configured: true`.
2. Call `systeme_extra_tags` with `action: "list"`. Expect `ok: true`, status 200.
3. Tell the user it is ready, and give two example requests from the README.

| Problem | Fix |
|---|---|
| `configured: false` | Key not stored or placeholder not replaced; restart the client after fixing |
| 401 "Invalid API Key." | Wrong key type (MCP key) or deleted key; create a Public API key |
| No tools shown | Wrong path in config, or client not restarted |
| `ModuleNotFoundError` | Command is not the `.venv` Python; use the absolute venv path |

## 7. Using it

Every write needs a preview (`dry_run: true`) shown to the user, their clear yes, then the same call with `confirm: true`. Actions marked `high_impact` in `help` (sending newsletters, deleting, cancelling subscriptions, overwriting pages) deserve extra care. Full action list: `docs/feature-reference.md`.
