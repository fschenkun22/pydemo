from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject
from PySide6.QtNetwork import QLocalServer, QLocalSocket


def notify_existing_instance(server_name: str, timeout_ms: int = 500) -> bool:
    socket = QLocalSocket()
    socket.connectToServer(server_name)
    if not socket.waitForConnected(timeout_ms):
        return False
    socket.write(b"activate")
    socket.flush()
    socket.waitForBytesWritten(timeout_ms)
    socket.disconnectFromServer()
    return True


class SingleInstanceServer(QObject):
    def __init__(
        self,
        server_name: str,
        on_activate: Callable[[], None],
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._server_name = server_name
        self._on_activate = on_activate
        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._handle_new_connection)

    def start(self) -> bool:
        return self._server.listen(self._server_name)

    def _handle_new_connection(self) -> None:
        while self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()
            if socket is None:
                continue
            if socket.bytesAvailable() == 0:
                socket.waitForReadyRead(100)
            _ = socket.readAll()
            self._on_activate()
            socket.disconnectFromServer()
            socket.deleteLater()
