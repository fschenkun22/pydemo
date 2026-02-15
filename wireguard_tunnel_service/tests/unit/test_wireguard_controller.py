from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from wireguard_tunnel_service.core.wireguard_controller import (
    STATE_STOPPED,
    ControllerError,
    WireGuardController,
)


def _completed(
    returncode: int,
    stdout: str,
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["x"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_is_service_running_returns_true_for_running_state(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: _completed(0, "STATE              : 4  RUNNING"),
    )

    assert controller.is_service_running()


def test_transfer_bytes_parses_rx_tx(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: _completed(
            0,
            "\n".join(
                [
                    "peer-a\t100\t200",
                    "peer-b\t300\t400",
                ],
            ),
        ),
    )

    transfer = controller.transfer_bytes()
    assert transfer == (400, 600)


def test_transfer_bytes_sets_error_when_wg_not_found(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: (_ for _ in ()).throw(FileNotFoundError("wg.exe missing")),
    )

    assert controller.transfer_bytes() is None
    error = controller.last_transfer_error()
    assert error is not None
    assert error.code == "transfer_query_command_not_found"


def test_reconnect_starts_service_when_already_stopped(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(controller, "_query_service_state", lambda: STATE_STOPPED)
    monkeypatch.setattr(controller, "_wait_for_state", lambda expected_state, timeout_sec: True)
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: _completed(0, "OK"),
    )

    assert controller.reconnect()


def test_is_service_running_sets_service_error_when_service_missing(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: _completed(
            1060,
            "",
            "The specified service does not exist as an installed service.",
        ),
    )

    assert not controller.is_service_running()
    error = controller.last_service_error()
    assert error is not None
    assert error.code == "service_not_found"


def test_connect_failure_exposes_error_code(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")
    monkeypatch.setattr(controller, "_query_service_state", lambda: STATE_STOPPED)
    monkeypatch.setattr(
        controller,
        "_run_command",
        lambda command: _completed(5, "", "Access is denied."),
    )

    assert not controller.connect()
    error = controller.last_reconnect_error()
    assert error is not None
    assert error.code == "connect_start_failed"
    assert "returncode=5" in error.detail


def test_connect_installs_service_when_not_found(monkeypatch) -> None:
    controller = WireGuardController(tunnel_name="wg0")

    def fake_missing_state() -> int | None:
        controller._last_service_error = ControllerError(  # noqa: SLF001
            code="service_not_found",
            detail="returncode=1060",
        )
        return None

    monkeypatch.setattr(controller, "_query_service_state", fake_missing_state)
    monkeypatch.setattr(controller, "_install_tunnel_service", lambda: True)

    assert controller.connect()


def test_discover_tunnels_reads_configuration_names(tmp_path: Path, monkeypatch) -> None:
    config_dir = tmp_path / "Configurations"
    config_dir.mkdir()
    (config_dir / "office.conf.dpapi").write_text("", encoding="utf-8")
    (config_dir / "wg0.conf.dpapi").write_text("", encoding="utf-8")
    (config_dir / "notes.txt").write_text("", encoding="utf-8")

    monkeypatch.setattr(
        WireGuardController,
        "_resolve_configurations_dir",
        staticmethod(lambda: config_dir),
    )
    assert WireGuardController.discover_tunnels() == ["office", "wg0"]


def test_discover_tunnels_raises_when_permission_denied(monkeypatch) -> None:
    config_dir = Path(r"C:\Program Files\WireGuard\Data\Configurations")
    monkeypatch.setattr(
        WireGuardController,
        "_resolve_configurations_dir",
        staticmethod(lambda: config_dir),
    )

    def raise_permission_error(path: Path) -> list[Path]:
        raise PermissionError("Access is denied.")

    monkeypatch.setattr(
        WireGuardController,
        "_list_directory",
        staticmethod(raise_permission_error),
    )

    with pytest.raises(PermissionError, match="Please run as Administrator"):
        WireGuardController.discover_tunnels()
