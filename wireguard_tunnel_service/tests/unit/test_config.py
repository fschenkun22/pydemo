from pathlib import Path

from wireguard_tunnel_service.core.config import load_settings, save_settings


def test_load_settings_from_file(tmp_path: Path) -> None:
    config_path = tmp_path / "settings.toml"
    config_path.write_text(
        """
[wireguard]
tunnel_name = "wg-test"
service_name = "WireGuardTunnel$wg-test"
healthcheck_url = "https://example.com/health"
healthcheck_timeout_sec = 5

[monitor]
check_interval_sec = 5
max_retries = 2
probe_failures_before_disconnect = 4

[logging]
level = "DEBUG"

[storage]
db_path = "tmp/state.db"
""".strip(),
        encoding="utf-8",
    )

    settings = load_settings(config_path)
    assert settings.wireguard.tunnel_name == "wg-test"
    assert settings.wireguard.service_name == "WireGuardTunnel$wg-test"
    assert settings.wireguard.healthcheck_url == "https://example.com/health"
    assert settings.wireguard.healthcheck_timeout_sec == 5
    assert settings.monitor.check_interval_sec == 5
    assert settings.monitor.max_retries == 2
    assert settings.monitor.probe_failures_before_disconnect == 4
    assert settings.logging.level == "DEBUG"
    assert settings.storage.db_path == "tmp/state.db"


def test_load_settings_uses_defaults_when_missing_file(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "not-found.toml")
    assert settings.wireguard.tunnel_name == ""
    assert settings.wireguard.service_name is None
    assert settings.wireguard.healthcheck_url == "https://www.cloudflare.com/cdn-cgi/trace"
    assert settings.wireguard.healthcheck_timeout_sec == 8
    assert settings.monitor.max_retries == 3
    assert settings.monitor.probe_failures_before_disconnect == 3
    assert settings.logging.filename == "service.log"
    assert settings.storage.db_path == "data/state.db"


def test_save_settings_round_trip(tmp_path: Path) -> None:
    source = tmp_path / "source.toml"
    source.write_text(
        """
[wireguard]
tunnel_name = "wg-alpha"
service_name = ""
healthcheck_url = "https://example.org/ping"
healthcheck_timeout_sec = 7

[monitor]
check_interval_sec = 9
max_retries = 5
retry_interval_sec = 11
cooldown_sec = 40
probe_failures_before_disconnect = 6

[logging]
level = "INFO"
max_bytes = 123
backup_count = 2
directory = "logs"
filename = "app.log"

[storage]
db_path = "data/test.db"
""".strip(),
        encoding="utf-8",
    )
    settings = load_settings(source)
    target = tmp_path / "saved.toml"
    save_settings(target, settings)
    loaded = load_settings(target)

    assert loaded.wireguard.tunnel_name == "wg-alpha"
    assert loaded.wireguard.healthcheck_url == "https://example.org/ping"
    assert loaded.monitor.max_retries == 5
    assert loaded.monitor.probe_failures_before_disconnect == 6
