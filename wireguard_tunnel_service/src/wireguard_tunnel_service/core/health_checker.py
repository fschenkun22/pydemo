from __future__ import annotations

from datetime import UTC, datetime
from urllib import error, request
from urllib.parse import urlsplit

from wireguard_tunnel_service.core.models import HealthSnapshot, TunnelStatus
from wireguard_tunnel_service.core.wireguard_controller import WireGuardController


class HealthChecker:
    def __init__(
        self,
        controller: WireGuardController,
        healthcheck_url: str = "",
        healthcheck_timeout_sec: int = 8,
    ) -> None:
        self._controller = controller
        self._healthcheck_url = self._normalize_url(healthcheck_url)
        self._healthcheck_timeout_sec = healthcheck_timeout_sec

    def check_once(self, skip_connectivity_probe: bool = False) -> HealthSnapshot:
        now = datetime.now(UTC)

        if not self._controller.is_service_running():
            service_error = self._controller.last_service_error()
            return HealthSnapshot(
                status=TunnelStatus.DISCONNECTED,
                checked_at=now,
                reason=service_error.code if service_error is not None else "service_not_running",
                reason_detail=service_error.detail if service_error is not None else None,
            )

        transfer = self._controller.transfer_bytes()
        rx_bytes = transfer[0] if transfer is not None else None
        tx_bytes = transfer[1] if transfer is not None else None

        if self._healthcheck_url and not skip_connectivity_probe:
            probe_ok, detail = self.probe_connectivity()
            if not probe_ok:
                return HealthSnapshot(
                    status=TunnelStatus.DISCONNECTED,
                    checked_at=now,
                    reason="url_probe_failed",
                    reason_detail=detail,
                    rx_bytes=rx_bytes,
                    tx_bytes=tx_bytes,
                )

        return HealthSnapshot(
            status=TunnelStatus.HEALTHY,
            checked_at=now,
            reason="ok",
            rx_bytes=rx_bytes,
            tx_bytes=tx_bytes,
        )

    @staticmethod
    def _probe_url(url: str, timeout_sec: int) -> tuple[bool, str]:
        req = request.Request(
            url=url,
            headers={"User-Agent": "wireguard-tunnel-service/0.1"},
            method="GET",
        )
        try:
            with request.urlopen(req, timeout=timeout_sec) as resp:  # noqa: S310
                code = getattr(resp, "status", 200)
                if 200 <= code < 400:
                    return True, f"http_status={code}"
                return False, f"http_status={code}"
        except error.HTTPError as exc:
            return False, f"http_error={exc.code}"
        except error.URLError as exc:
            return False, f"url_error={exc.reason}"
        except ValueError as exc:
            return False, f"invalid_url={exc}"
        except TimeoutError:
            return False, "timeout"
        except Exception as exc:  # noqa: BLE001
            return False, f"probe_error={exc}"

    def probe_connectivity(self) -> tuple[bool, str]:
        if not self._healthcheck_url:
            return True, "probe_disabled"
        return self._probe_url(
            self._healthcheck_url,
            timeout_sec=self._healthcheck_timeout_sec,
        )

    @staticmethod
    def _normalize_url(url: str) -> str:
        normalized = url.strip()
        if not normalized:
            return ""
        parsed = urlsplit(normalized)
        if parsed.scheme:
            return normalized
        return f"https://{normalized}"
