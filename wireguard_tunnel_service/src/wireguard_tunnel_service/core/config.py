from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class WireGuardSettings:
    tunnel_name: str = ""
    service_name: str | None = None
    healthcheck_url: str = "https://www.cloudflare.com/cdn-cgi/trace"
    healthcheck_timeout_sec: int = 8
    ping_target: str = "10.0.0.1"
    enable_ping_check: bool = True


@dataclass(frozen=True, slots=True)
class MonitorSettings:
    check_interval_sec: int = 15
    max_retries: int = 3
    retry_interval_sec: int = 10
    cooldown_sec: int = 300
    probe_failures_before_disconnect: int = 3


@dataclass(frozen=True, slots=True)
class LoggingSettings:
    level: str = "INFO"
    max_bytes: int = 1_048_576
    backup_count: int = 5
    directory: str = "logs"
    filename: str = "service.log"


@dataclass(frozen=True, slots=True)
class StorageSettings:
    db_path: str = "data/state.db"


@dataclass(frozen=True, slots=True)
class AppSettings:
    wireguard: WireGuardSettings
    monitor: MonitorSettings
    logging: LoggingSettings
    storage: StorageSettings


def _as_table(raw: object) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    return {}


def load_settings(path: Path) -> AppSettings:
    if not path.exists():
        return AppSettings(
            wireguard=WireGuardSettings(),
            monitor=MonitorSettings(),
            logging=LoggingSettings(),
            storage=StorageSettings(),
        )

    with path.open("rb") as fp:
        data = tomllib.load(fp)

    wg = _as_table(data.get("wireguard"))
    monitor = _as_table(data.get("monitor"))
    log = _as_table(data.get("logging"))
    storage = _as_table(data.get("storage"))

    service_name_raw = str(wg.get("service_name", "")).strip()
    service_name = service_name_raw if service_name_raw else None

    return AppSettings(
        wireguard=WireGuardSettings(
            tunnel_name=str(wg.get("tunnel_name", "")).strip(),
            service_name=service_name,
            healthcheck_url=str(
                wg.get("healthcheck_url", "https://www.cloudflare.com/cdn-cgi/trace"),
            ),
            healthcheck_timeout_sec=int(wg.get("healthcheck_timeout_sec", 8)),
            ping_target=str(wg.get("ping_target", "10.0.0.1")),
            enable_ping_check=bool(wg.get("enable_ping_check", True)),
        ),
        monitor=MonitorSettings(
            check_interval_sec=int(monitor.get("check_interval_sec", 15)),
            max_retries=int(monitor.get("max_retries", 3)),
            retry_interval_sec=int(monitor.get("retry_interval_sec", 10)),
            cooldown_sec=int(monitor.get("cooldown_sec", 300)),
            probe_failures_before_disconnect=int(
                monitor.get("probe_failures_before_disconnect", 3),
            ),
        ),
        logging=LoggingSettings(
            level=str(log.get("level", "INFO")),
            max_bytes=int(log.get("max_bytes", 1_048_576)),
            backup_count=int(log.get("backup_count", 5)),
            directory=str(log.get("directory", "logs")),
            filename=str(log.get("filename", "service.log")),
        ),
        storage=StorageSettings(
            db_path=str(storage.get("db_path", "data/state.db")),
        ),
    )


def save_settings(path: Path, settings: AppSettings) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    service_name = settings.wireguard.service_name or ""
    content = (
        "[wireguard]\n"
        f'tunnel_name = "{settings.wireguard.tunnel_name}"\n'
        f'service_name = "{service_name}"\n'
        f'healthcheck_url = "{settings.wireguard.healthcheck_url}"\n'
        f"healthcheck_timeout_sec = {settings.wireguard.healthcheck_timeout_sec}\n"
        f'ping_target = "{settings.wireguard.ping_target}"\n'
        f"enable_ping_check = {_bool_literal(settings.wireguard.enable_ping_check)}\n"
        "\n"
        "[monitor]\n"
        f"check_interval_sec = {settings.monitor.check_interval_sec}\n"
        f"max_retries = {settings.monitor.max_retries}\n"
        f"retry_interval_sec = {settings.monitor.retry_interval_sec}\n"
        f"cooldown_sec = {settings.monitor.cooldown_sec}\n"
        f"probe_failures_before_disconnect = {settings.monitor.probe_failures_before_disconnect}\n"
        "\n"
        "[logging]\n"
        f'level = "{settings.logging.level}"\n'
        f"max_bytes = {settings.logging.max_bytes}\n"
        f"backup_count = {settings.logging.backup_count}\n"
        f'directory = "{settings.logging.directory}"\n'
        f'filename = "{settings.logging.filename}"\n'
        "\n"
        "[storage]\n"
        f'db_path = "{settings.storage.db_path}"\n'
    )
    path.write_text(content, encoding="utf-8")


def _bool_literal(value: bool) -> str:
    return "true" if value else "false"
