from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from wireguard_tunnel_service.core.config import AppSettings
from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.state_store import StateEvent, StateStore
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController


class MainWindow(QMainWindow):
    def __init__(
        self,
        settings: AppSettings,
        state_store: StateStore,
        available_tunnels: list[str],
        on_settings_updated: Callable[[AppSettings], None],
        on_refresh_tunnels: Callable[[], list[str]],
        on_tunnel_selected: Callable[[str], None] | None = None,
        on_status_changed: Callable[[str, str, int | None, int | None], None] | None = None,
    ) -> None:
        super().__init__()
        self._settings = settings
        self._state_store = state_store
        self._allow_close = False
        self._tray_enabled = False
        self._on_settings_updated = on_settings_updated
        self._on_refresh_tunnels = on_refresh_tunnels
        self._on_tunnel_selected = on_tunnel_selected
        self._on_status_changed = on_status_changed
        self._current_status = "unknown"
        self._current_reason = "-"
        self._current_rx_bytes: int | None = None
        self._current_tx_bytes: int | None = None

        self.setWindowTitle("WireGuard Tunnel Service")
        self.resize(980, 720)

        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.addWidget(self._build_status_group())
        root_layout.addWidget(self._build_config_group())
        root_layout.addLayout(self._build_action_bar())
        root_layout.addWidget(self._build_history_table())
        self.setCentralWidget(central)

        self._set_tunnels(available_tunnels)
        self._load_form_from_settings()

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(2000)
        self._refresh_timer.timeout.connect(self.refresh_view)
        self._refresh_timer.start()

        self._traffic_timer = QTimer(self)
        self._traffic_timer.setInterval(500)
        self._traffic_timer.timeout.connect(self._poll_transfer_counters)
        self._traffic_timer.start()
        self.refresh_view()

    def set_tray_enabled(self, enabled: bool) -> None:
        self._tray_enabled = enabled

    def request_exit(self) -> None:
        self._allow_close = True
        self.close()

    def current_status_snapshot(self) -> tuple[str, str, int | None, int | None]:
        return (
            self._current_status,
            self._current_reason,
            self._current_rx_bytes,
            self._current_tx_bytes,
        )

    def refresh_view(self) -> None:
        events = self._state_store.list_events(limit=200)
        self._fill_history(events)
        self._update_status(events)

    def manual_health_check(self) -> None:
        checker = self._new_checker()
        snapshot = checker.check_once()
        detail = _sanitize_value(snapshot.reason_detail)
        rx_raw = str(snapshot.rx_bytes) if snapshot.rx_bytes is not None else "-"
        tx_raw = str(snapshot.tx_bytes) if snapshot.tx_bytes is not None else "-"
        self._state_store.append_event(
            "manual_health_check",
            (
                f"status={snapshot.status.value};reason={snapshot.reason}"
                f";detail={detail};rx_bytes={rx_raw};tx_bytes={tx_raw}"
            ),
        )
        self.refresh_view()

    def manual_reconnect(self) -> None:
        controller = self._new_controller()
        ok = controller.reconnect()
        if ok:
            self._state_store.append_event("manual_reconnect_success", "code=ok;detail=-")
            self.refresh_view()
            return

        reconnect_error = controller.last_reconnect_error()
        error_code = (
            reconnect_error.code if reconnect_error is not None else "manual_reconnect_failed"
        )
        error_detail = reconnect_error.detail if reconnect_error is not None else "-"
        sanitized_detail = _sanitize_value(error_detail)
        self._state_store.append_event(
            "manual_reconnect_failure",
            f"code={error_code};detail={sanitized_detail}",
        )
        self.refresh_view()
        QMessageBox.warning(
            self,
            "Reconnect Failed",
            f"code: {error_code}\n\ndetail: {error_detail}",
        )

    def manual_connect(self) -> None:
        controller = self._new_controller()
        ok = controller.connect()
        if ok:
            self._state_store.append_event("manual_connect_success", "code=ok;detail=-")
            self.refresh_view()
            return

        connect_error = controller.last_reconnect_error()
        error_code = connect_error.code if connect_error is not None else "manual_connect_failed"
        error_detail = connect_error.detail if connect_error is not None else "-"
        self._state_store.append_event(
            "manual_connect_failure",
            f"code={error_code};detail={_sanitize_value(error_detail)}",
        )
        self.refresh_view()
        QMessageBox.warning(
            self,
            "Connect Failed",
            f"code: {error_code}\n\ndetail: {error_detail}",
        )

    def manual_disconnect(self) -> None:
        controller = self._new_controller()
        ok = controller.disconnect()
        if ok:
            self._state_store.append_event("manual_disconnect_success", "code=ok;detail=-")
            self.refresh_view()
            return

        disconnect_error = controller.last_reconnect_error()
        error_code = (
            disconnect_error.code if disconnect_error is not None else "manual_disconnect_failed"
        )
        error_detail = disconnect_error.detail if disconnect_error is not None else "-"
        self._state_store.append_event(
            "manual_disconnect_failure",
            f"code={error_code};detail={_sanitize_value(error_detail)}",
        )
        self.refresh_view()
        QMessageBox.warning(
            self,
            "Disconnect Failed",
            f"code: {error_code}\n\ndetail: {error_detail}",
        )

    def apply_settings(self) -> None:
        tunnel_name = self._tunnel_combo.currentText().strip()
        if not tunnel_name:
            QMessageBox.warning(self, "Invalid Config", "Please select a WireGuard tunnel.")
            return

        healthcheck_url = self._url_edit.text().strip()
        if not healthcheck_url:
            QMessageBox.warning(self, "Invalid Config", "Please enter a health check URL.")
            return

        new_wireguard = replace(
            self._settings.wireguard,
            tunnel_name=tunnel_name,
            service_name=None,
            healthcheck_url=healthcheck_url,
            healthcheck_timeout_sec=self._url_timeout_spin.value(),
        )
        new_monitor = replace(
            self._settings.monitor,
            check_interval_sec=self._check_interval_spin.value(),
            max_retries=self._max_retries_spin.value(),
            retry_interval_sec=self._retry_interval_spin.value(),
            cooldown_sec=self._cooldown_spin.value(),
            probe_failures_before_disconnect=self._probe_failures_spin.value(),
        )
        new_settings = replace(
            self._settings,
            wireguard=new_wireguard,
            monitor=new_monitor,
        )
        try:
            self._on_settings_updated(new_settings)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Apply Failed", str(exc))
            return

        self._settings = new_settings
        self._state_store.append_event(
            "config_updated",
            (
                f"tunnel_name={new_settings.wireguard.tunnel_name};"
                f"healthcheck_url={_sanitize_value(new_settings.wireguard.healthcheck_url)};"
                f"probe_failures_before_disconnect="
                f"{new_settings.monitor.probe_failures_before_disconnect}"
            ),
        )
        self.refresh_view()
        QMessageBox.information(self, "Config Applied", "Settings updated and monitor restarted.")

    def refresh_tunnels(self) -> None:
        try:
            tunnels = self._on_refresh_tunnels()
        except PermissionError as exc:
            QMessageBox.warning(self, "Permission Required", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, "Refresh Failed", str(exc))
            return
        self._set_tunnels(tunnels)

    def open_log_directory(self) -> None:
        log_dir = Path(self._settings.logging.directory)
        log_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(str(log_dir))

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._allow_close:
            event.accept()
            return

        if self._tray_enabled:
            event.ignore()
            self.hide()
            return

        event.accept()

    def _build_status_group(self) -> QGroupBox:
        self._tunnel_label = QLabel("-")
        self._status_label = QLabel("unknown")
        self._reason_label = QLabel("-")
        self._detail_label = QLabel("-")
        self._rx_label = QLabel("-")
        self._tx_label = QLabel("-")
        self._last_check_label = QLabel("-")

        group = QGroupBox("Current Status")
        layout = QGridLayout(group)
        layout.addWidget(QLabel("Tunnel"), 0, 0)
        layout.addWidget(self._tunnel_label, 0, 1)
        layout.addWidget(QLabel("Status"), 1, 0)
        layout.addWidget(self._status_label, 1, 1)
        layout.addWidget(QLabel("Reason"), 2, 0)
        layout.addWidget(self._reason_label, 2, 1)
        layout.addWidget(QLabel("Detail"), 3, 0)
        layout.addWidget(self._detail_label, 3, 1)
        layout.addWidget(QLabel("Received"), 4, 0)
        layout.addWidget(self._rx_label, 4, 1)
        layout.addWidget(QLabel("Sent"), 5, 0)
        layout.addWidget(self._tx_label, 5, 1)
        layout.addWidget(QLabel("Last Check"), 6, 0)
        layout.addWidget(self._last_check_label, 6, 1)
        return group

    def _build_config_group(self) -> QGroupBox:
        group = QGroupBox("Tunnel And Monitor Config")
        layout = QGridLayout(group)

        self._tunnel_combo = QComboBox()
        self._tunnel_combo.setEditable(True)
        self._tunnel_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self._tunnel_combo.setPlaceholderText("Select or type tunnel name, e.g. shenyang231")
        self._tunnel_combo.currentTextChanged.connect(self._remember_tunnel_selection)
        refresh_btn = QPushButton("Refresh Tunnels")
        refresh_btn.clicked.connect(self.refresh_tunnels)

        self._url_edit = QLineEdit()
        self._url_edit.setPlaceholderText("https://www.cloudflare.com/cdn-cgi/trace")

        self._url_timeout_spin = _new_spinbox(1, 120)
        self._check_interval_spin = _new_spinbox(3, 3600)
        self._max_retries_spin = _new_spinbox(1, 20)
        self._retry_interval_spin = _new_spinbox(1, 600)
        self._cooldown_spin = _new_spinbox(0, 3600)
        self._probe_failures_spin = _new_spinbox(1, 20)

        apply_btn = QPushButton("Apply Config")
        apply_btn.clicked.connect(self.apply_settings)

        layout.addWidget(QLabel("Tunnel"), 0, 0)
        layout.addWidget(self._tunnel_combo, 0, 1)
        layout.addWidget(refresh_btn, 0, 2)

        layout.addWidget(QLabel("Healthcheck URL"), 1, 0)
        layout.addWidget(self._url_edit, 1, 1, 1, 2)

        layout.addWidget(QLabel("URL Timeout (s)"), 2, 0)
        layout.addWidget(self._url_timeout_spin, 2, 1)

        layout.addWidget(QLabel("Check Interval (s)"), 3, 0)
        layout.addWidget(self._check_interval_spin, 3, 1)

        layout.addWidget(QLabel("Max Retries"), 3, 2)
        layout.addWidget(self._max_retries_spin, 3, 3)

        layout.addWidget(QLabel("Retry Interval (s)"), 4, 0)
        layout.addWidget(self._retry_interval_spin, 4, 1)

        layout.addWidget(QLabel("Cooldown (s)"), 4, 2)
        layout.addWidget(self._cooldown_spin, 4, 3)

        layout.addWidget(QLabel("Probe Failures Before Disconnect"), 5, 0)
        layout.addWidget(self._probe_failures_spin, 5, 1)

        layout.addWidget(apply_btn, 6, 3)
        return group

    def _build_action_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        check_btn = QPushButton("Check Now")
        check_btn.clicked.connect(self.manual_health_check)
        layout.addWidget(check_btn)

        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(self.manual_connect)
        layout.addWidget(connect_btn)

        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.clicked.connect(self.manual_disconnect)
        layout.addWidget(disconnect_btn)

        log_btn = QPushButton("Open Logs")
        log_btn.clicked.connect(self.open_log_directory)
        layout.addWidget(log_btn)

        layout.addStretch(1)
        return layout

    def _build_history_table(self) -> QTableWidget:
        self._history_table = QTableWidget(0, 3)
        self._history_table.setHorizontalHeaderLabels(["Time", "Event", "Payload"])
        self._history_table.horizontalHeader().setStretchLastSection(True)
        self._history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        return self._history_table

    def _fill_history(self, events: list[StateEvent]) -> None:
        self._history_table.setRowCount(len(events))
        for idx, event in enumerate(events):
            self._history_table.setItem(idx, 0, QTableWidgetItem(event.occurred_at))
            self._history_table.setItem(idx, 1, QTableWidgetItem(event.event_type))
            self._history_table.setItem(idx, 2, QTableWidgetItem(event.reason))

    def _update_status(self, events: list[StateEvent]) -> None:
        status_reason = "-"
        status_detail = "-"
        status_value = "unknown"
        event_rx_bytes: int | None = None
        event_tx_bytes: int | None = None
        last_time = "-"

        for event in events:
            if event.event_type not in {"health_check", "manual_health_check"}:
                continue
            payload = _parse_payload(event.reason)
            status_value = payload.get("status", status_value)
            status_reason = payload.get("reason", status_reason)
            status_detail = payload.get("detail", status_detail)
            event_rx_bytes = _parse_optional_int(payload.get("rx_bytes"))
            event_tx_bytes = _parse_optional_int(payload.get("tx_bytes"))
            last_time = event.occurred_at
            break

        if status_value == "disconnected":
            self._current_rx_bytes = None
            self._current_tx_bytes = None
        else:
            if self._current_rx_bytes is None and event_rx_bytes is not None:
                self._current_rx_bytes = event_rx_bytes
            if self._current_tx_bytes is None and event_tx_bytes is not None:
                self._current_tx_bytes = event_tx_bytes

        self._status_label.setText(status_value)
        self._reason_label.setText(status_reason)
        self._detail_label.setText(status_detail)
        self._rx_label.setText(_format_traffic_value(self._current_rx_bytes))
        self._tx_label.setText(_format_traffic_value(self._current_tx_bytes))
        self._last_check_label.setText(last_time)
        self._tunnel_label.setText(self._settings.wireguard.tunnel_name or "-")
        self._current_status = status_value
        self._current_reason = status_reason
        if self._on_status_changed is not None:
            self._on_status_changed(
                status_value,
                status_reason,
                self._current_rx_bytes,
                self._current_tx_bytes,
            )

    def _poll_transfer_counters(self) -> None:
        tunnel_name = (
            self._tunnel_combo.currentText().strip() or self._settings.wireguard.tunnel_name
        )
        if not tunnel_name:
            return

        controller = self._new_controller()
        transfer = controller.transfer_bytes(timeout_sec=1)
        if transfer is None:
            return

        rx_bytes, tx_bytes = transfer
        self._current_rx_bytes = rx_bytes
        self._current_tx_bytes = tx_bytes
        self._rx_label.setText(_format_traffic_value(rx_bytes))
        self._tx_label.setText(_format_traffic_value(tx_bytes))
        if self._on_status_changed is not None:
            self._on_status_changed(
                self._current_status,
                self._current_reason,
                rx_bytes,
                tx_bytes,
            )

    def _load_form_from_settings(self) -> None:
        self._url_edit.setText(self._settings.wireguard.healthcheck_url)
        self._url_timeout_spin.setValue(self._settings.wireguard.healthcheck_timeout_sec)
        self._check_interval_spin.setValue(self._settings.monitor.check_interval_sec)
        self._max_retries_spin.setValue(self._settings.monitor.max_retries)
        self._retry_interval_spin.setValue(self._settings.monitor.retry_interval_sec)
        self._cooldown_spin.setValue(self._settings.monitor.cooldown_sec)
        self._probe_failures_spin.setValue(self._settings.monitor.probe_failures_before_disconnect)

    def _set_tunnels(self, tunnels: list[str]) -> None:
        current = self._tunnel_combo.currentText().strip() or self._settings.wireguard.tunnel_name
        options = sorted({item.strip() for item in tunnels if item.strip()})
        if self._settings.wireguard.tunnel_name.strip():
            options.append(self._settings.wireguard.tunnel_name.strip())
            options = sorted(set(options))
        self._tunnel_combo.clear()
        self._tunnel_combo.addItems(options)
        idx = self._tunnel_combo.findText(current)
        if idx >= 0:
            self._tunnel_combo.setCurrentIndex(idx)
        elif current:
            self._tunnel_combo.setCurrentText(current)

    def _new_checker(self) -> HealthChecker:
        controller = self._new_controller()
        return HealthChecker(
            controller=controller,
            healthcheck_url=self._settings.wireguard.healthcheck_url,
            healthcheck_timeout_sec=self._settings.wireguard.healthcheck_timeout_sec,
        )

    def _new_controller(self) -> WireGuardController:
        tunnel_name = (
            self._tunnel_combo.currentText().strip() or self._settings.wireguard.tunnel_name
        )
        return WireGuardController(
            tunnel_name=tunnel_name,
            service_name=None,
        )

    def _remember_tunnel_selection(self, text: str) -> None:
        tunnel_name = text.strip()
        if not tunnel_name:
            return
        if tunnel_name == self._settings.wireguard.tunnel_name:
            return
        self._settings = replace(
            self._settings,
            wireguard=replace(self._settings.wireguard, tunnel_name=tunnel_name),
        )
        if self._on_tunnel_selected is not None:
            self._on_tunnel_selected(tunnel_name)


def _parse_payload(raw: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in raw.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _new_spinbox(minimum: int, maximum: int) -> QSpinBox:
    spin = QSpinBox()
    spin.setRange(minimum, maximum)
    return spin


def _sanitize_value(value: str | None) -> str:
    if not value:
        return "-"
    return value.replace(";", ",").replace("\n", " ")


def _format_traffic_bytes(raw: str | None) -> str:
    if raw is None:
        return "-"
    value = raw.strip()
    if not value or value == "-":
        return "-"
    if not value.isdigit():
        return value

    amount = int(value)
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    index = 0
    display = float(amount)
    while display >= 1024 and index < len(units) - 1:
        display /= 1024
        index += 1
    if index == 0:
        return f"{int(display)} {units[index]}"
    return f"{display:.2f} {units[index]}"


def _format_traffic_value(value: int | None) -> str:
    if value is None:
        return "-"
    return _format_traffic_bytes(str(value))


def _parse_optional_int(raw: str | None) -> int | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value or value == "-" or not value.isdigit():
        return None
    return int(value)
