from __future__ import annotations

import logging
import threading

from PySide6.QtCore import QThread

from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.monitor_service import MonitorService
from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy
from wireguard_tunnel_service.core.state_store import StateStore
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController


class MonitorWorker(QThread):
    def __init__(
        self,
        checker: HealthChecker,
        controller: WireGuardController,
        policy: ReconnectPolicy,
        state_store: StateStore,
        check_interval_sec: int,
        probe_failures_before_disconnect: int = 3,
    ) -> None:
        super().__init__()
        self._stop_event = threading.Event()
        self._monitor = MonitorService(
            checker=checker,
            controller=controller,
            policy=policy,
            state_store=state_store,
            check_interval_sec=check_interval_sec,
            probe_failures_before_disconnect=probe_failures_before_disconnect,
        )

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:  # noqa: D401
        try:
            self._monitor.run(stop_event=self._stop_event)
        except Exception:  # noqa: BLE001
            logging.getLogger(__name__).exception("Monitor worker crashed unexpectedly.")
