from __future__ import annotations

from dataclasses import dataclass

from wireguard_tunnel_service.core.health_checker import HealthChecker
from wireguard_tunnel_service.core.models import TunnelStatus
from wireguard_tunnel_service.core.wireguard_controller import ControllerError


@dataclass
class FakeController:
    service_running: bool
    service_error: ControllerError | None = None

    def is_service_running(self) -> bool:
        return self.service_running

    def last_service_error(self) -> ControllerError | None:
        return self.service_error


def test_health_checker_marks_disconnected_when_service_not_running() -> None:
    controller = FakeController(
        service_running=False,
        service_error=ControllerError(code="service_not_found", detail="returncode=1060"),
    )
    checker = HealthChecker(controller)
    snapshot = checker.check_once()
    assert snapshot.status is TunnelStatus.DISCONNECTED
    assert snapshot.reason == "service_not_found"


def test_health_checker_marks_disconnected_when_url_probe_failed(monkeypatch) -> None:
    controller = FakeController(service_running=True)
    checker = HealthChecker(
        controller,
        healthcheck_url="https://example.com",
        healthcheck_timeout_sec=3,
    )
    monkeypatch.setattr(
        checker,
        "_probe_url",
        lambda url, timeout_sec: (False, "url_error=timed out"),
    )

    snapshot = checker.check_once()
    assert snapshot.status is TunnelStatus.DISCONNECTED
    assert snapshot.reason == "url_probe_failed"


def test_health_checker_marks_healthy_when_all_checks_pass(monkeypatch) -> None:
    controller = FakeController(service_running=True)
    checker = HealthChecker(
        controller,
        healthcheck_url="https://example.com",
        healthcheck_timeout_sec=3,
    )
    monkeypatch.setattr(
        checker,
        "_probe_url",
        lambda url, timeout_sec: (True, "http_status=200"),
    )

    snapshot = checker.check_once()
    assert snapshot.status is TunnelStatus.HEALTHY
    assert snapshot.reason == "ok"


def test_probe_connectivity_returns_disabled_when_url_empty() -> None:
    controller = FakeController(service_running=True)
    checker = HealthChecker(controller, healthcheck_url="")
    ok, detail = checker.probe_connectivity()
    assert ok
    assert detail == "probe_disabled"


def test_probe_connectivity_normalizes_bare_host(monkeypatch) -> None:
    controller = FakeController(service_running=True)
    checker = HealthChecker(controller, healthcheck_url="baidu.com")

    captured: dict[str, str] = {}

    def fake_probe(url: str, timeout_sec: int) -> tuple[bool, str]:
        captured["url"] = url
        return True, "http_status=200"

    monkeypatch.setattr(checker, "_probe_url", fake_probe)
    ok, _ = checker.probe_connectivity()
    assert ok
    assert captured["url"] == "https://baidu.com"
