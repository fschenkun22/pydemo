from __future__ import annotations

from collections.abc import Callable
from time import monotonic

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QAction, QColor, QIcon, QLinearGradient, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QMenu, QSystemTrayIcon, QWidget

_ICON_CACHE: dict[str, QIcon] = {}
_TRAY_STATE: dict[int, dict[str, object]] = {}
_TRAY_TIMERS: dict[int, QTimer] = {}
_TRAY_OBJECTS: dict[int, QSystemTrayIcon] = {}

_ANIMATION_TICK_MS = 50
_MAX_PULSES_PER_EVENT = 6
_MAX_PULSE_QUEUE = 24
_NOISE_FLOOR_BYTES = 4 * 1024
_SMALL_FLOW_BYTES = 64 * 1024
_FAST_FLOW_BYTES = 512 * 1024
_MEDIUM_STEP_BYTES = 256 * 1024
_FAST_STEP_BYTES = 512 * 1024
_TX_START_DELAY_MS = 120


def setup_system_tray(
    parent: QWidget,
    on_reconnect: Callable[[], None],
    on_quit: Callable[[], None],
) -> QSystemTrayIcon:
    tray = QSystemTrayIcon(parent)
    tray.setIcon(_build_status_icon("unknown", rx_flash=False, tx_flash=False))
    tray.setToolTip("WireGuard Tunnel Service")

    menu = QMenu(parent)
    show_action = QAction("Show / Hide", parent)
    reconnect_action = QAction("Reconnect", parent)
    quit_action = QAction("Quit", parent)

    show_action.triggered.connect(lambda: _toggle_visibility(parent))
    reconnect_action.triggered.connect(on_reconnect)
    quit_action.triggered.connect(on_quit)

    menu.addAction(show_action)
    menu.addAction(reconnect_action)
    menu.addSeparator()
    menu.addAction(quit_action)
    tray.setContextMenu(menu)

    tray.activated.connect(
        lambda reason: _on_tray_activated(parent, reason),
    )
    tray.show()
    _ensure_tray_runtime(tray)
    return tray


def set_tray_status(
    tray: QSystemTrayIcon,
    *,
    status: str,
    reason: str = "-",
    rx_bytes: int | None = None,
    tx_bytes: int | None = None,
) -> None:
    normalized = status.strip().lower() or "unknown"
    state = _ensure_tray_runtime(tray)
    state["status"] = normalized
    state["reason"] = reason

    now_ms = monotonic() * 1000.0
    _update_lane_from_bytes(state, lane="rx", value=rx_bytes, now_ms=now_ms)
    _update_lane_from_bytes(state, lane="tx", value=tx_bytes, now_ms=now_ms)

    _refresh_tray_visuals(id(tray))


def _ensure_tray_runtime(tray: QSystemTrayIcon) -> dict[str, object]:
    tray_id = id(tray)
    _TRAY_OBJECTS[tray_id] = tray
    state = _TRAY_STATE.setdefault(
        tray_id,
        {
            "status": "unknown",
            "reason": "-",
            "last_rx": None,
            "last_tx": None,
            "rx_mode": 0,  # 0=idle, 1=on, 2=off
            "tx_mode": 0,  # 0=idle, 1=on, 2=off
            "rx_remaining": 0,
            "tx_remaining": 0,
            "rx_deadline_ms": 0.0,
            "tx_deadline_ms": 0.0,
            "rx_on_ms": 100,
            "tx_on_ms": 100,
            "rx_off_ms": 400,
            "tx_off_ms": 400,
        },
    )
    if tray_id not in _TRAY_TIMERS:
        timer = QTimer(tray)
        timer.setInterval(_ANIMATION_TICK_MS)
        timer.timeout.connect(lambda tray_id=tray_id: _animate_tray(tray_id))
        timer.start()
        _TRAY_TIMERS[tray_id] = timer
        tray.destroyed.connect(lambda _=None, tray_id=tray_id: _cleanup_tray(tray_id))
    return state


def _cleanup_tray(tray_id: int) -> None:
    timer = _TRAY_TIMERS.pop(tray_id, None)
    if timer is not None:
        timer.stop()
    _TRAY_OBJECTS.pop(tray_id, None)
    _TRAY_STATE.pop(tray_id, None)


def _update_lane_from_bytes(
    state: dict[str, object],
    *,
    lane: str,
    value: int | None,
    now_ms: float,
) -> None:
    if value is None:
        return
    last_key = f"last_{lane}"
    last_value = state[last_key]
    if isinstance(last_value, int):
        delta = value - last_value
        if delta > 0:
            pulses, on_ms, off_ms = _lane_profile(delta)
            _enqueue_lane_pulses(
                state,
                lane=lane,
                pulses=pulses,
                on_ms=on_ms,
                off_ms=off_ms,
                now_ms=now_ms,
            )
    state[last_key] = value


def _enqueue_lane_pulses(
    state: dict[str, object],
    *,
    lane: str,
    pulses: int,
    on_ms: int,
    off_ms: int,
    now_ms: float,
) -> None:
    if pulses <= 0:
        return
    mode_key = f"{lane}_mode"
    remaining_key = f"{lane}_remaining"
    deadline_key = f"{lane}_deadline_ms"
    on_key = f"{lane}_on_ms"
    off_key = f"{lane}_off_ms"
    mode = int(state[mode_key])
    remaining = int(state[remaining_key])

    current_on = int(state[on_key])
    current_off = int(state[off_key])
    state[on_key] = min(current_on, on_ms)
    state[off_key] = min(current_off, off_ms)

    if mode == 0:
        if lane == "tx":
            # Slight phase offset to keep RX/TX visually separable.
            state[mode_key] = 2
            state[deadline_key] = now_ms + _TX_START_DELAY_MS
            state[remaining_key] = min(_MAX_PULSE_QUEUE, pulses)
        else:
            state[mode_key] = 1
            state[deadline_key] = now_ms + state[on_key]
            state[remaining_key] = min(_MAX_PULSE_QUEUE, max(0, pulses - 1))
        return

    state[remaining_key] = min(_MAX_PULSE_QUEUE, remaining + pulses)


def _animate_tray(tray_id: int) -> None:
    state = _TRAY_STATE.get(tray_id)
    if state is None:
        return
    if tray_id not in _TRAY_OBJECTS:
        _cleanup_tray(tray_id)
        return
    now_ms = monotonic() * 1000.0
    rx_changed = _step_lane(state, lane="rx", now_ms=now_ms)
    tx_changed = _step_lane(state, lane="tx", now_ms=now_ms)
    if rx_changed or tx_changed:
        _refresh_tray_visuals(tray_id)


def _step_lane(state: dict[str, object], *, lane: str, now_ms: float) -> bool:
    mode_key = f"{lane}_mode"
    remaining_key = f"{lane}_remaining"
    deadline_key = f"{lane}_deadline_ms"
    on_key = f"{lane}_on_ms"
    off_key = f"{lane}_off_ms"
    mode = int(state[mode_key])
    deadline = float(state[deadline_key])
    remaining = int(state[remaining_key])
    on_ms = int(state[on_key])
    off_ms = int(state[off_key])

    if mode == 0 or now_ms < deadline:
        return False

    if mode == 1:
        if remaining > 0:
            state[mode_key] = 2
            state[deadline_key] = now_ms + off_ms
        else:
            state[mode_key] = 0
            state[deadline_key] = 0.0
            state[on_key] = 100
            state[off_key] = 400
        return True

    state[mode_key] = 1
    state[remaining_key] = max(0, remaining - 1)
    state[deadline_key] = now_ms + on_ms
    return True


def _refresh_tray_visuals(tray_id: int) -> None:
    tray = _TRAY_OBJECTS.get(tray_id)
    state = _TRAY_STATE.get(tray_id)
    if tray is None or state is None:
        return

    status = str(state.get("status", "unknown")).strip().lower() or "unknown"
    reason = str(state.get("reason", "-"))
    rx_flash = int(state.get("rx_mode", 0)) == 1
    tx_flash = int(state.get("tx_mode", 0)) == 1
    tray.setIcon(_build_status_icon(status, rx_flash=rx_flash, tx_flash=tx_flash))

    rx_text = _format_bytes(_as_optional_int(state.get("last_rx")))
    tx_text = _format_bytes(_as_optional_int(state.get("last_tx")))
    tray.setToolTip(
        f"WireGuard Tunnel Service [{status}] reason={reason} | RX={rx_text} TX={tx_text}",
    )


def _as_optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def _toggle_visibility(parent: QWidget) -> None:
    if parent.isVisible():
        parent.hide()
        return
    parent.show()
    parent.raise_()
    parent.activateWindow()


def _on_tray_activated(parent: QWidget, reason: QSystemTrayIcon.ActivationReason) -> None:
    if reason is QSystemTrayIcon.ActivationReason.DoubleClick:
        _toggle_visibility(parent)


def _status_color(status: str) -> QColor:
    if status == "healthy":
        return QColor("#22c55e")
    if status == "degraded":
        return QColor("#f59e0b")
    if status == "disconnected":
        return QColor("#ef4444")
    return QColor("#94a3b8")


def _build_status_icon(status: str, *, rx_flash: bool, tx_flash: bool) -> QIcon:
    cache_key = f"{status}|{int(rx_flash)}|{int(tx_flash)}"
    cached = _ICON_CACHE.get(cache_key)
    if cached is not None:
        return cached

    icon = QIcon()
    for size in (16, 20, 24, 32):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        _paint_network_windows(
            painter,
            size,
            status=status,
            rx_flash=rx_flash,
            tx_flash=tx_flash,
        )
        painter.end()
        icon.addPixmap(pixmap)

    _ICON_CACHE[cache_key] = icon
    return icon


def _paint_network_windows(
    painter: QPainter,
    size: int,
    *,
    status: str,
    rx_flash: bool,
    tx_flash: bool,
) -> None:
    status_color = _status_color(status)
    intensity = _status_intensity(status)

    margin = size * 0.04
    outer = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)
    outer_radius = max(2.0, size * 0.22)
    shell_gradient = QLinearGradient(outer.topLeft(), outer.bottomLeft())
    shell_gradient.setColorAt(0.0, QColor("#232a35"))
    shell_gradient.setColorAt(1.0, QColor("#10151d"))
    painter.setBrush(shell_gradient)
    painter.setPen(QPen(QColor(255, 255, 255, 50), max(1.0, size * 0.045)))
    painter.drawRoundedRect(outer, outer_radius, outer_radius)

    inner = outer.adjusted(size * 0.06, size * 0.08, -size * 0.06, -size * 0.16)
    gap = max(1.0, size * 0.05)
    pane_w = (inner.width() - gap) / 2.0
    left = QRectF(inner.x(), inner.y(), pane_w, inner.height())
    right = QRectF(inner.x() + pane_w + gap, inner.y(), pane_w, inner.height())

    rx_color = QColor("#3B82F6")
    tx_color = QColor("#F59E0B")
    _paint_window_pane(
        painter,
        left,
        flash=rx_flash,
        base_color=rx_color,
        intensity=intensity,
    )
    _paint_window_pane(
        painter,
        right,
        flash=tx_flash,
        base_color=tx_color,
        intensity=intensity,
    )

    bar_h = max(1.6, size * 0.12)
    bar = QRectF(
        outer.x() + outer.width() * 0.08,
        outer.y() + outer.height() - bar_h - size * 0.07,
        outer.width() * 0.84,
        bar_h,
    )
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(_blend(QColor("#111827"), status_color, 0.85))
    painter.drawRoundedRect(bar, bar_h * 0.6, bar_h * 0.6)


def _paint_window_pane(
    painter: QPainter,
    pane: QRectF,
    *,
    flash: bool,
    base_color: QColor,
    intensity: float,
) -> None:
    if flash:
        top = _blend(base_color, QColor("#FFFFFF"), 0.42)
        bottom = _blend(base_color, QColor("#0B1220"), 0.15)
        edge = QColor(255, 255, 255, 90)
    else:
        top = _blend(QColor("#1F2937"), base_color, 0.04 * intensity)
        bottom = _blend(QColor("#0F172A"), base_color, 0.02 * intensity)
        edge = QColor(255, 255, 255, 35)

    gradient = QLinearGradient(pane.topLeft(), pane.bottomLeft())
    gradient.setColorAt(0.0, top)
    gradient.setColorAt(1.0, bottom)

    painter.setBrush(gradient)
    painter.setPen(QPen(edge, max(1.0, pane.width() * 0.08)))
    radius = max(1.8, pane.width() * 0.28)
    painter.drawRoundedRect(pane, radius, radius)

    painter.setPen(Qt.PenStyle.NoPen)
    if flash:
        inset = pane.adjusted(
            pane.width() * 0.16,
            pane.height() * 0.12,
            -pane.width() * 0.16,
            -pane.height() * 0.58,
        )
        painter.setBrush(QColor(255, 255, 255, 170))
        painter.drawRoundedRect(inset, inset.height() * 0.45, inset.height() * 0.45)
    else:
        indicator = pane.adjusted(
            pane.width() * 0.18,
            pane.height() * 0.76,
            -pane.width() * 0.18,
            -pane.height() * 0.10,
        )
        painter.setBrush(QColor(base_color.red(), base_color.green(), base_color.blue(), 72))
        painter.drawRoundedRect(indicator, indicator.height() * 0.5, indicator.height() * 0.5)


def _blend(c1: QColor, c2: QColor, ratio: float) -> QColor:
    r = max(0.0, min(1.0, ratio))
    red = int(c1.red() * (1.0 - r) + c2.red() * r)
    green = int(c1.green() * (1.0 - r) + c2.green() * r)
    blue = int(c1.blue() * (1.0 - r) + c2.blue() * r)
    return QColor(red, green, blue)


def _status_intensity(status: str) -> float:
    if status == "healthy":
        return 1.0
    if status == "degraded":
        return 0.88
    if status == "disconnected":
        return 0.56
    return 0.72


def _lane_profile(delta_bytes: int) -> tuple[int, int, int]:
    if delta_bytes < _NOISE_FLOOR_BYTES:
        return 0, 100, 400

    if delta_bytes < _SMALL_FLOW_BYTES:
        return 1, 80, 700

    if delta_bytes < _FAST_FLOW_BYTES:
        extra = delta_bytes // _MEDIUM_STEP_BYTES
        pulses = min(_MAX_PULSES_PER_EVENT, 1 + int(extra))
        return pulses, 100, 350

    extra = delta_bytes // _FAST_STEP_BYTES
    pulses = min(_MAX_PULSES_PER_EVENT, 2 + int(extra))
    return pulses, 90, 120


def _format_bytes(value: int | None) -> str:
    if value is None:
        return "-"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    amount = float(value)
    idx = 0
    while amount >= 1024 and idx < len(units) - 1:
        amount /= 1024
        idx += 1
    if idx == 0:
        return f"{int(amount)} {units[idx]}"
    return f"{amount:.2f} {units[idx]}"
