from __future__ import annotations

import locale
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

STATE_STOPPED = 1
STATE_RUNNING = 4


@dataclass(frozen=True, slots=True)
class ControllerError:
    code: str
    detail: str


class WireGuardController:
    """System adapter for tunnel status checks and reconnection operations."""

    def __init__(self, tunnel_name: str, service_name: str | None = None) -> None:
        self.tunnel_name = tunnel_name
        self.service_name = service_name or f"WireGuardTunnel${tunnel_name}"
        self._wireguard_executable = self._resolve_wireguard_executable()
        self._last_service_error: ControllerError | None = None
        self._last_reconnect_error: ControllerError | None = None

    def is_service_running(self) -> bool:
        state = self._query_service_state()
        return state == STATE_RUNNING

    def reconnect(self) -> bool:
        disconnected = self.disconnect()
        if not disconnected:
            return False
        return self.connect()

    def connect(self) -> bool:
        self._last_reconnect_error = None
        current_state = self._query_service_state()
        if current_state is None:
            if self._is_service_not_found():
                return self._install_tunnel_service()
            self._last_reconnect_error = self._service_to_reconnect_error(
                "connect_service_query_failed",
            )
            return False
        if current_state == STATE_RUNNING:
            return True

        start_result, start_error = self._run_command_safe(
            ["sc.exe", "start", self.service_name],
            context="service_start",
        )
        if start_error is not None:
            self._last_reconnect_error = ControllerError(
                code="connect_start_exec_failed",
                detail=start_error.detail,
            )
            return False
        assert start_result is not None
        if start_result.returncode != 0:
            self._last_reconnect_error = ControllerError(
                code="connect_start_failed",
                detail=self._render_command_failure(start_result),
            )
            return False
        if not self._wait_for_state(STATE_RUNNING, timeout_sec=20):
            if self._last_service_error is not None:
                self._last_reconnect_error = self._service_to_reconnect_error(
                    "connect_start_state_query_failed",
                )
            else:
                self._last_reconnect_error = ControllerError(
                    code="connect_start_timeout",
                    detail="Service did not reach running state in 20 seconds.",
                )
            return False
        return True

    def disconnect(self) -> bool:
        self._last_reconnect_error = None
        current_state = self._query_service_state()
        if current_state is None:
            if self._is_service_not_found():
                return True
            self._last_reconnect_error = self._service_to_reconnect_error(
                "disconnect_service_query_failed",
            )
            return False

        uninstall_result, uninstall_error = self._run_command_safe(
            [self._wireguard_executable, "/uninstalltunnelservice", self.tunnel_name],
            context="uninstall_tunnel_service",
        )
        if uninstall_error is not None:
            self._last_reconnect_error = ControllerError(
                code="disconnect_uninstall_exec_failed",
                detail=uninstall_error.detail,
            )
            return False
        assert uninstall_result is not None
        if (
            uninstall_result.returncode != 0
            and not self._is_service_missing_result(uninstall_result)
        ):
            self._last_reconnect_error = ControllerError(
                code="disconnect_uninstall_failed",
                detail=self._render_command_failure(uninstall_result),
            )
            return False

        if not self._wait_for_stopped_or_missing(timeout_sec=20):
            if self._last_service_error is not None:
                self._last_reconnect_error = self._service_to_reconnect_error(
                    "disconnect_uninstall_state_query_failed",
                )
            else:
                self._last_reconnect_error = ControllerError(
                    code="disconnect_uninstall_timeout",
                    detail="Tunnel service did not stop/uninstall in 20 seconds.",
                )
            return False
        return True

    def last_service_error(self) -> ControllerError | None:
        return self._last_service_error

    def last_reconnect_error(self) -> ControllerError | None:
        return self._last_reconnect_error

    @classmethod
    def discover_tunnels(cls) -> list[str]:
        config_dir = cls._resolve_configurations_dir()
        try:
            entries = cls._list_directory(config_dir)
        except FileNotFoundError:
            return []
        except PermissionError as exc:
            raise PermissionError(
                f"Cannot read WireGuard tunnel list from {config_dir}. "
                "Please run as Administrator.",
            ) from exc

        discovered: set[str] = set()
        for entry in entries:
            if not entry.is_file():
                continue
            if not entry.name.endswith(".conf.dpapi"):
                continue
            tunnel_name = entry.name.removesuffix(".conf.dpapi").strip()
            if tunnel_name:
                discovered.add(tunnel_name)
        return sorted(discovered)

    @staticmethod
    def _resolve_configurations_dir() -> Path:
        program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        return program_files / "WireGuard" / "Data" / "Configurations"

    @staticmethod
    def _list_directory(path: Path) -> list[Path]:
        return list(path.iterdir())

    @staticmethod
    def _resolve_wireguard_executable() -> str:
        discovered = shutil.which("wireguard.exe") or shutil.which("wireguard")
        if discovered:
            return discovered

        windows_default = Path(r"C:\Program Files\WireGuard\wireguard.exe")
        if windows_default.exists():
            return str(windows_default)

        return "wireguard.exe"

    def _query_service_state(self) -> int | None:
        result, run_error = self._run_command_safe(
            ["sc.exe", "query", self.service_name],
            context="service_query",
        )
        if run_error is not None:
            self._last_service_error = run_error
            return None
        assert result is not None

        if result.returncode != 0:
            error_code = (
                "service_not_found"
                if self._is_service_missing_result(result)
                else "service_query_failed"
            )
            self._last_service_error = ControllerError(
                code=error_code,
                detail=self._render_command_failure(result),
            )
            return None

        for line in result.stdout.splitlines():
            normalized = line.upper()
            if "STATE" not in normalized:
                continue
            match = re.search(r":\s+(\d+)\s+", line)
            if not match:
                continue
            self._last_service_error = None
            return int(match.group(1))

        self._last_service_error = ControllerError(
            code="service_state_parse_failed",
            detail="Could not parse service state from sc query output.",
        )
        return None

    def _wait_for_state(self, expected_state: int, timeout_sec: int) -> bool:
        deadline = time.time() + timeout_sec
        while time.time() <= deadline:
            current_state = self._query_service_state()
            if current_state == expected_state:
                return True
            time.sleep(1)
        return False

    def _wait_for_stopped_or_missing(self, timeout_sec: int) -> bool:
        deadline = time.time() + timeout_sec
        while time.time() <= deadline:
            current_state = self._query_service_state()
            if current_state == STATE_STOPPED:
                return True
            if current_state is None and self._is_service_not_found():
                return True
            time.sleep(1)
        return False

    def _install_tunnel_service(self) -> bool:
        config_path = self._resolve_configurations_dir() / f"{self.tunnel_name}.conf.dpapi"
        install_result, install_error = self._run_command_safe(
            [self._wireguard_executable, "/installtunnelservice", str(config_path)],
            context="install_tunnel_service",
        )
        if install_error is not None:
            self._last_reconnect_error = ControllerError(
                code="connect_install_exec_failed",
                detail=install_error.detail,
            )
            return False
        assert install_result is not None
        if install_result.returncode != 0:
            self._last_reconnect_error = ControllerError(
                code="connect_install_failed",
                detail=self._render_command_failure(install_result),
            )
            return False
        if not self._wait_for_state(STATE_RUNNING, timeout_sec=20):
            if self._last_service_error is not None:
                self._last_reconnect_error = self._service_to_reconnect_error(
                    "connect_install_state_query_failed",
                )
            else:
                self._last_reconnect_error = ControllerError(
                    code="connect_install_timeout",
                    detail="Tunnel service did not reach running state in 20 seconds.",
                )
            return False
        return True

    def _is_service_not_found(self) -> bool:
        return (
            self._last_service_error is not None
            and self._last_service_error.code == "service_not_found"
        )

    @staticmethod
    def _is_service_missing_result(result: subprocess.CompletedProcess[str]) -> bool:
        if result.returncode == 1060:
            return True
        output = f"{result.stdout}\n{result.stderr}".lower()
        markers = ("does not exist", "failed 1060", "openservice failed 1060")
        return any(marker in output for marker in markers)

    def _service_to_reconnect_error(self, fallback_code: str) -> ControllerError:
        if self._last_service_error is None:
            return ControllerError(code=fallback_code, detail="Service query returned no result.")
        return ControllerError(
            code=fallback_code,
            detail=f"{self._last_service_error.code}: {self._last_service_error.detail}",
        )

    @staticmethod
    def _render_command_failure(result: subprocess.CompletedProcess[str]) -> str:
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        fragments = [f"returncode={result.returncode}"]
        if stdout:
            fragments.append(f"stdout={stdout}")
        if stderr:
            fragments.append(f"stderr={stderr}")
        return " | ".join(fragments)

    def _run_command_safe(
        self,
        command: list[str],
        context: str,
    ) -> tuple[subprocess.CompletedProcess[str] | None, ControllerError | None]:
        try:
            return self._run_command(command), None
        except FileNotFoundError as exc:
            return None, ControllerError(
                code=f"{context}_command_not_found",
                detail=str(exc),
            )
        except subprocess.TimeoutExpired as exc:
            return None, ControllerError(
                code=f"{context}_command_timeout",
                detail=str(exc),
            )
        except OSError as exc:
            return None, ControllerError(
                code=f"{context}_os_error",
                detail=str(exc),
            )

    @staticmethod
    def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW
        completed = subprocess.run(
            command,
            capture_output=True,
            text=False,
            check=False,
            timeout=15,
            creationflags=creationflags,
        )
        return subprocess.CompletedProcess(
            args=completed.args,
            returncode=completed.returncode,
            stdout=WireGuardController._decode_output(completed.stdout),
            stderr=WireGuardController._decode_output(completed.stderr),
        )

    @staticmethod
    def _decode_output(data: bytes) -> str:
        if not data:
            return ""
        preferred = locale.getpreferredencoding(False) or "utf-8"
        encodings = [preferred, "utf-8", "gbk", "cp936"]
        tried: set[str] = set()
        for encoding in encodings:
            normalized = encoding.lower()
            if normalized in tried:
                continue
            tried.add(normalized)
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
        return data.decode(preferred, errors="replace")
