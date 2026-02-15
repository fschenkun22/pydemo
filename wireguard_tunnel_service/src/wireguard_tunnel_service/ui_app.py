from __future__ import annotations

import ctypes
import logging
import sys
from dataclasses import replace
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


def _is_running_as_admin() -> bool:
    if sys.platform != "win32":
        return True
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:  # noqa: BLE001
        return False


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
    single_instance_name = "wireguard_tunnel_service_ui_single_instance_admin"

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    if not _is_running_as_admin():
        QMessageBox.critical(
            None,
            "Administrator Required",
            (
                "WireGuard Tunnel Service must run as Administrator.\n\n"
                "Please restart the program with administrator privileges."
            ),
        )
        return 1
    if notify_existing_instance(single_instance_name):
        return 0

    config_path = _default_config_path()
    settings: AppSettings = load_settings(config_path)
    configure_logging(settings.logging)
    logger = logging.getLogger(__name__)

    state_store = StateStore(Path(settings.storage.db_path))
    state_store.initialize()

    worker: MonitorWorker | None = None
    tray: QSystemTrayIcon | None = None

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

    def on_status_changed(
        status: str,
        reason: str,
        rx_bytes: int | None,
        tx_bytes: int | None,
    ) -> None:
        if tray is None:
            return
        set_tray_status(
            tray,
            status=status,
            reason=reason,
            rx_bytes=rx_bytes,
            tx_bytes=tx_bytes,
        )

    def on_tunnel_selected(tunnel_name: str) -> None:
        nonlocal settings
        name = tunnel_name.strip()
        if not name or name == settings.wireguard.tunnel_name:
            return
        settings = replace(
            settings,
            wireguard=replace(settings.wireguard, tunnel_name=name),
        )
        save_settings(config_path, settings)

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

    if not settings.wireguard.tunnel_name.strip() and initial_tunnels:
        picked = initial_tunnels[0]
        settings = replace(
            settings,
            wireguard=replace(settings.wireguard, tunnel_name=picked),
        )
        save_settings(config_path, settings)
        logger.info("Auto-selected startup tunnel=%s because config was empty.", picked)

    if settings.wireguard.tunnel_name.strip():
        worker = _build_worker(settings, state_store)
        worker.start()

    window = MainWindow(
        settings=settings,
        state_store=state_store,
        available_tunnels=initial_tunnels,
        on_settings_updated=apply_settings,
        on_refresh_tunnels=refresh_tunnels,
        on_tunnel_selected=on_tunnel_selected,
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
        status, reason, rx_bytes, tx_bytes = window.current_status_snapshot()
        set_tray_status(
            tray,
            status=status,
            reason=reason,
            rx_bytes=rx_bytes,
            tx_bytes=tx_bytes,
        )
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
