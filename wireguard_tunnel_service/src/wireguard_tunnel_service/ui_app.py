from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

from wireguard_tunnel_service.core.config import AppSettings, load_settings, save_settings
from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy
from wireguard_tunnel_service.core.state_store import StateStore
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController
from wireguard_tunnel_service.infra.logging_config import configure_logging
from wireguard_tunnel_service.ui.main_window import MainWindow
from wireguard_tunnel_service.ui.monitor_worker import MonitorWorker
from wireguard_tunnel_service.ui.single_instance import (
    SingleInstanceServer,
    notify_existing_instance,
)
from wireguard_tunnel_service.ui.tray import set_tray_status, setup_system_tray


def _default_config_path() -> Path:
    return Path("config") / "settings.toml"


def _build_worker(settings: AppSettings, state_store: StateStore) -> MonitorWorker:
    tunnel_name = settings.wireguard.tunnel_name.strip()
    if not tunnel_name:
        raise ValueError("No tunnel selected.")

    monitor_controller = WireGuardController(
        tunnel_name=tunnel_name,
        service_name=settings.wireguard.service_name,
    )
    checker = HealthChecker(
        controller=monitor_controller,
        healthcheck_url=settings.wireguard.healthcheck_url,
        healthcheck_timeout_sec=settings.wireguard.healthcheck_timeout_sec,
    )
    policy = ReconnectPolicy(
        max_retries=settings.monitor.max_retries,
        base_interval_sec=settings.monitor.retry_interval_sec,
        cooldown_sec=settings.monitor.cooldown_sec,
    )
    return MonitorWorker(
        checker=checker,
        controller=monitor_controller,
        policy=policy,
        state_store=state_store,
        check_interval_sec=settings.monitor.check_interval_sec,
        probe_failures_before_disconnect=settings.monitor.probe_failures_before_disconnect,
    )


def main() -> int:
    single_instance_name = "wireguard_tunnel_service_ui_single_instance"
    if notify_existing_instance(single_instance_name):
        return 0

    config_path = _default_config_path()
    settings: AppSettings = load_settings(config_path)
    configure_logging(settings.logging)
    logger = logging.getLogger(__name__)

    state_store = StateStore(Path(settings.storage.db_path))
    state_store.initialize()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    worker: MonitorWorker | None = None
    tray: QSystemTrayIcon | None = None
    if settings.wireguard.tunnel_name.strip():
        worker = _build_worker(settings, state_store)
        worker.start()

    def refresh_tunnels() -> list[str]:
        discovered = WireGuardController.discover_tunnels()
        if (
            settings.wireguard.tunnel_name.strip()
            and settings.wireguard.tunnel_name not in discovered
        ):
            discovered.append(settings.wireguard.tunnel_name)
        return sorted(set(discovered))

    def apply_settings(updated: AppSettings) -> None:
        nonlocal settings, worker
        save_settings(config_path, updated)
        settings = updated

        if worker is not None:
            worker.stop()
            worker.wait(5000)
            worker = None

        if settings.wireguard.tunnel_name.strip():
            worker = _build_worker(settings, state_store)
            worker.start()
        logger.info(
            "Updated monitor config. tunnel=%s check_interval=%s retries=%s",
            settings.wireguard.tunnel_name,
            settings.monitor.check_interval_sec,
            settings.monitor.max_retries,
        )

    def on_status_changed(status: str, reason: str) -> None:
        if tray is None:
            return
        set_tray_status(tray, status=status, reason=reason)

    def activate_window() -> None:
        if window.isMinimized():
            window.setWindowState(window.windowState() & ~Qt.WindowState.WindowMinimized)
        window.show()
        window.raise_()
        window.activateWindow()

    startup_discovery_error: str | None = None
    try:
        initial_tunnels = refresh_tunnels()
    except PermissionError as exc:
        startup_discovery_error = str(exc)
        logger.warning("Tunnel discovery requires admin privileges. detail=%s", exc)
        initial_tunnels = []
        if settings.wireguard.tunnel_name.strip():
            initial_tunnels.append(settings.wireguard.tunnel_name.strip())

    window = MainWindow(
        settings=settings,
        state_store=state_store,
        available_tunnels=initial_tunnels,
        on_settings_updated=apply_settings,
        on_refresh_tunnels=refresh_tunnels,
        on_status_changed=on_status_changed,
    )
    single_instance = SingleInstanceServer(
        single_instance_name,
        on_activate=activate_window,
        parent=app,
    )
    listener_started = single_instance.start()
    if not listener_started and notify_existing_instance(single_instance_name):
        return 0
    if not listener_started:
        logger.warning("Single-instance listener could not start; duplicate launch may occur.")
    if startup_discovery_error is not None:
        QMessageBox.warning(
            window,
            "Permission Required",
            startup_discovery_error,
        )

    def on_quit() -> None:
        window.request_exit()
        app.quit()

    if QSystemTrayIcon.isSystemTrayAvailable():
        tray = setup_system_tray(
            parent=window,
            on_reconnect=window.manual_reconnect,
            on_quit=on_quit,
        )
        window.set_tray_enabled(True)
        status, reason = window.current_status_snapshot()
        set_tray_status(tray, status=status, reason=reason)
        tray.showMessage(
            "WireGuard Tunnel Service",
            "Service is running in system tray.",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )
    else:
        logger.warning("System tray is not available on this platform.")

    def cleanup() -> None:
        nonlocal worker
        if worker is not None:
            worker.stop()
            worker.wait(5000)

    app.aboutToQuit.connect(cleanup)
    activate_window()
    return int(app.exec())


if __name__ == "__main__":
    raise SystemExit(main())
