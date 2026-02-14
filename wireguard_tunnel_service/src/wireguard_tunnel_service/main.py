from __future__ import annotations

import logging
from pathlib import Path

from wireguard_tunnel_service.core.config import AppSettings, load_settings
from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.monitor_service import MonitorService
from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy
from wireguard_tunnel_service.core.state_store import StateStore
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController
from wireguard_tunnel_service.infra.logging_config import configure_logging


def _default_config_path() -> Path:
    return Path("config") / "settings.toml"


def main() -> None:
    settings: AppSettings = load_settings(_default_config_path())
    configure_logging(settings.logging)
    logger = logging.getLogger(__name__)

    if not settings.wireguard.tunnel_name.strip():
        logger.error(
            "No tunnel configured. Please set wireguard.tunnel_name in config/settings.toml.",
        )
        return

    state_store = StateStore(Path(settings.storage.db_path))
    state_store.initialize()

    controller = WireGuardController(
        tunnel_name=settings.wireguard.tunnel_name,
        service_name=settings.wireguard.service_name,
    )
    checker = HealthChecker(
        controller=controller,
        healthcheck_url=settings.wireguard.healthcheck_url,
        healthcheck_timeout_sec=settings.wireguard.healthcheck_timeout_sec,
    )
    policy = ReconnectPolicy(
        max_retries=settings.monitor.max_retries,
        base_interval_sec=settings.monitor.retry_interval_sec,
        cooldown_sec=settings.monitor.cooldown_sec,
    )
    monitor = MonitorService(
        checker=checker,
        controller=controller,
        policy=policy,
        state_store=state_store,
        check_interval_sec=settings.monitor.check_interval_sec,
        probe_failures_before_disconnect=settings.monitor.probe_failures_before_disconnect,
    )

    logger.info(
        "Service started. tunnel=%s check_interval_sec=%s max_retries=%s",
        settings.wireguard.tunnel_name,
        settings.monitor.check_interval_sec,
        settings.monitor.max_retries,
    )
    try:
        monitor.run()
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
