from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QMenu, QStyle, QSystemTrayIcon, QWidget


def setup_system_tray(
    parent: QWidget,
    on_reconnect: Callable[[], None],
    on_quit: Callable[[], None],
) -> QSystemTrayIcon:
    tray = QSystemTrayIcon(parent)
    tray_icon = parent.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
    tray.setIcon(tray_icon)
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
    return tray


def set_tray_status(
    tray: QSystemTrayIcon,
    *,
    status: str,
    reason: str = "-",
) -> None:
    normalized = status.strip().lower()
    color = _status_color(normalized)
    tray.setIcon(_build_status_icon(color))
    tray.setToolTip(f"WireGuard Tunnel Service [{normalized}] reason={reason}")


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


def _status_color(status: str) -> str:
    if status == "healthy":
        return "#25b85a"
    if status == "degraded":
        return "#f1b90c"
    if status == "disconnected":
        return "#e05252"
    return "#8b95a7"


def _build_status_icon(color_hex: str) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setBrush(QColor(color_hex))
    painter.setPen(QPen(QColor("#1f2937"), 1))
    painter.drawEllipse(2, 2, 12, 12)
    painter.end()
    return QIcon(pixmap)
