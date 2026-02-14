param(
    [string]$Entry = "src/wireguard_tunnel_service/main.py",
    [string]$Name = "wireguard-tunnel-service",
    [switch]$Windowed
)

$ErrorActionPreference = "Stop"

$args = @(
  "--noconfirm",
  "--clean",
  "--name", $Name,
  "--onedir"
)

if ($Windowed -or $Entry -like "*ui_app.py") {
  $args += "--windowed"
}

$args += $Entry

uv run pyinstaller @args
