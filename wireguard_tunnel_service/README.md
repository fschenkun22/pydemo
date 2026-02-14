# wireguard-tunnel-service

WireGuard tunnel health check service for Windows.

## Prerequisites
- Python 3.12
- `uv` 0.6+
- WireGuard for Windows

## Quick Start
```powershell
uv sync --group dev
uv run wireguard-tunnel-service
```

`wireguard-tunnel-service` is a long-running process. Stop it with `Ctrl+C`.

## Desktop UI
```powershell
uv sync --group dev
uv run wireguard-tunnel-ui
```

The desktop mode runs in the system tray. Closing the window minimizes to tray.
At startup it discovers WireGuard tunnels and lets you choose one in the UI.
You can update health-check URL, check interval, retry count, retry interval, and cooldown.
If discovery is empty, type your tunnel name directly in the tunnel input (for example `shenyang231`).
Monitor policy: if internet probe fails, the app disconnects the tunnel first; when internet is reachable again, it retries tunnel connect according to retry settings.

## Quality Commands
```powershell
uv run ruff check .
uv run mypy src
uv run pytest
```

## Build EXE
```powershell
uv sync --group dev
./scripts/build.ps1
```

## Project Layout
```text
src/wireguard_tunnel_service/
  core/        # domain and service logic
  infra/       # IO adapters (logging, db, command integration)
  ui/          # desktop UI and tray
config/
  settings.toml
tests/
  unit/
  integration/
scripts/
  build.ps1
```

## Runtime Data
- Logs: `logs/service.log`
- State history DB: `data/state.db`
