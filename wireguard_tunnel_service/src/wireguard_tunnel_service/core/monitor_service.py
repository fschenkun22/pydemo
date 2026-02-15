from __future__ import annotations

import logging
import threading
import time

from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.models import TunnelStatus
from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy
from wireguard_tunnel_service.core.state_store import StateStore
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController


class MonitorService:
    def __init__(
        self,
        checker: HealthChecker,
        controller: WireGuardController,
        policy: ReconnectPolicy,
        state_store: StateStore,
        check_interval_sec: int,
        probe_failures_before_disconnect: int = 3,
    ) -> None:
        self._checker = checker
        self._controller = controller
        self._policy = policy
        self._state_store = state_store
        self._check_interval_sec = check_interval_sec
        self._probe_failures_before_disconnect = max(1, probe_failures_before_disconnect)
        self._logger = logging.getLogger(__name__)

    def run(
        self,
        iterations: int | None = None,
        stop_event: threading.Event | None = None,
    ) -> None:
        failed_reconnect_attempts = 0
        failed_connectivity_checks = 0
        completed = 0

        while iterations is None or completed < iterations:
            if stop_event is not None and stop_event.is_set():
                break

            connectivity_ok, connectivity_detail = self._checker.probe_connectivity()
            if not connectivity_ok:
                failed_connectivity_checks += 1
                self._logger.warning(
                    "Connectivity probe failed. consecutive=%s threshold=%s detail=%s",
                    failed_connectivity_checks,
                    self._probe_failures_before_disconnect,
                    connectivity_detail,
                )
                self._state_store.append_event(
                    "connectivity_probe_failed",
                    (
                        f"consecutive={failed_connectivity_checks};"
                        f"threshold={self._probe_failures_before_disconnect};"
                        f"detail={self._sanitize_reason(connectivity_detail)}"
                    ),
                )
                if failed_connectivity_checks >= self._probe_failures_before_disconnect:
                    self._handle_no_connectivity(connectivity_detail)
                    failed_reconnect_attempts = 0
                    failed_connectivity_checks = 0
                completed += 1
                if iterations is None or completed < iterations:
                    if not self._wait(self._check_interval_sec, stop_event):
                        break
                continue
            failed_connectivity_checks = 0

            snapshot = self._checker.check_once(skip_connectivity_probe=True)
            reason_detail = self._sanitize_reason(snapshot.reason_detail)
            rx_raw = str(snapshot.rx_bytes) if snapshot.rx_bytes is not None else "-"
            tx_raw = str(snapshot.tx_bytes) if snapshot.tx_bytes is not None else "-"
            self._state_store.append_event(
                "health_check",
                (
                    f"status={snapshot.status.value};reason={snapshot.reason}"
                    f";detail={reason_detail};rx_bytes={rx_raw};tx_bytes={tx_raw}"
                ),
            )
            self._logger.info(
                "health_check status=%s reason=%s detail=%s rx_bytes=%s tx_bytes=%s",
                snapshot.status.value,
                snapshot.reason,
                snapshot.reason_detail,
                rx_raw,
                tx_raw,
            )

            if snapshot.status is not TunnelStatus.HEALTHY:
                failed_reconnect_attempts = self._handle_reconnect(
                    failed_reconnect_attempts,
                    stop_event=stop_event,
                )
            else:
                failed_reconnect_attempts = 0

            completed += 1
            if iterations is None or completed < iterations:
                if not self._wait(self._check_interval_sec, stop_event):
                    break

    def _handle_no_connectivity(self, detail: str) -> None:
        safe_detail = self._sanitize_reason(detail)
        self._state_store.append_event(
            "health_check",
            f"status=disconnected;reason=no_internet;detail={safe_detail}",
        )
        running = self._controller.is_service_running()
        if running:
            disconnected = self._controller.disconnect()
            if disconnected:
                self._logger.warning(
                    "Internet probe failed. Tunnel disconnected for local recovery. detail=%s",
                    detail,
                )
                self._state_store.append_event(
                    "tunnel_disconnected_no_internet",
                    f"detail={safe_detail}",
                )
            else:
                disconnect_error = self._controller.last_reconnect_error()
                code = (
                    disconnect_error.code
                    if disconnect_error is not None
                    else "disconnect_unknown_failure"
                )
                error_detail = (
                    disconnect_error.detail
                    if disconnect_error is not None
                    else "No disconnect error detail."
                )
                self._logger.error(
                    "Internet probe failed and tunnel disconnect failed. code=%s detail=%s",
                    code,
                    error_detail,
                )
                self._state_store.append_event(
                    "disconnect_failure_no_internet",
                    f"code={code};detail={self._sanitize_reason(error_detail)}",
                )
        else:
            self._state_store.append_event(
                "no_internet_waiting",
                f"detail={safe_detail}",
            )

    def _handle_reconnect(
        self,
        failed_reconnect_attempts: int,
        stop_event: threading.Event | None,
    ) -> int:
        if not self._policy.has_remaining_retry(failed_reconnect_attempts):
            self._logger.error(
                "Reconnect retries exhausted. Entering cooldown for %s sec.",
                self._policy.cooldown_sec,
            )
            self._state_store.append_event(
                "reconnect_cooldown",
                f"duration_sec={self._policy.cooldown_sec}",
            )
            if not self._wait(self._policy.cooldown_sec, stop_event):
                return failed_reconnect_attempts
            return 0

        attempt = failed_reconnect_attempts + 1
        backoff_sec = self._policy.next_backoff_sec(attempt)
        self._logger.warning(
            "Tunnel disconnected. reconnect_attempt=%s backoff_sec=%s",
            attempt,
            backoff_sec,
        )
        self._state_store.append_event(
            "reconnect_attempt",
            f"attempt={attempt};backoff_sec={backoff_sec}",
        )
        if not self._wait(backoff_sec, stop_event):
            return failed_reconnect_attempts

        reconnected = self._controller.reconnect()
        if reconnected:
            self._logger.info("Reconnect succeeded. attempt=%s", attempt)
            self._state_store.append_event("reconnect_success", f"attempt={attempt}")
            return 0

        reconnect_error = self._controller.last_reconnect_error()
        error_code = (
            reconnect_error.code if reconnect_error is not None else "reconnect_unknown_failure"
        )
        error_detail = self._sanitize_reason(
            reconnect_error.detail if reconnect_error is not None else "No reconnect error detail.",
        )
        self._logger.error(
            "Reconnect failed. attempt=%s code=%s detail=%s",
            attempt,
            error_code,
            reconnect_error.detail if reconnect_error is not None else None,
        )
        self._state_store.append_event(
            "reconnect_failure",
            f"attempt={attempt};code={error_code};detail={error_detail}",
        )
        return failed_reconnect_attempts + 1

    @staticmethod
    def _wait(duration_sec: int, stop_event: threading.Event | None) -> bool:
        if duration_sec <= 0:
            return True
        if stop_event is None:
            time.sleep(duration_sec)
            return True
        return not stop_event.wait(timeout=duration_sec)

    @staticmethod
    def _sanitize_reason(reason: str | None) -> str:
        if reason is None or not reason:
            return "-"
        return reason.replace(";", ",").replace("\n", " ")
