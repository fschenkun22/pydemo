from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from wireguard_tunnel_service.core.models import HealthSnapshot, TunnelStatus
from wireguard_tunnel_service.core.monitor_service import MonitorService
from wireguard_tunnel_service.core.reconnect_policy import ReconnectPolicy
from wireguard_tunnel_service.core.wireguard_controller import ControllerError


@dataclass
class FakeChecker:
    snapshot: HealthSnapshot
    connectivity_ok: bool = True
    connectivity_detail: str = "http_status=200"

    def check_once(self, skip_connectivity_probe: bool = False) -> HealthSnapshot:
        return self.snapshot

    def probe_connectivity(self) -> tuple[bool, str]:
        return (self.connectivity_ok, self.connectivity_detail)


@dataclass
class FakeController:
    reconnect_result: bool
    reconnect_calls: int = 0
    disconnect_result: bool = True
    disconnect_calls: int = 0
    service_running: bool = False

    def reconnect(self) -> bool:
        self.reconnect_calls += 1
        return self.reconnect_result

    def disconnect(self) -> bool:
        self.disconnect_calls += 1
        self.service_running = False
        return self.disconnect_result

    def is_service_running(self) -> bool:
        return self.service_running

    def last_reconnect_error(self) -> ControllerError | None:
        return ControllerError(code="connect_start_failed", detail="mocked reconnect failure")


@dataclass
class FakeStateStore:
    events: list[tuple[str, str]]

    def append_event(self, event_type: str, reason: str) -> None:
        self.events.append((event_type, reason))


def test_monitor_service_records_reconnect_success(monkeypatch) -> None:
    monkeypatch.setattr("wireguard_tunnel_service.core.monitor_service.time.sleep", lambda _: None)

    snapshot = HealthSnapshot(
        status=TunnelStatus.DISCONNECTED,
        checked_at=datetime.now(UTC),
        reason="service_not_running",
    )
    checker = FakeChecker(snapshot=snapshot, connectivity_ok=True)
    controller = FakeController(reconnect_result=True)
    store = FakeStateStore(events=[])
    service = MonitorService(
        checker=checker,
        controller=controller,
        policy=ReconnectPolicy(max_retries=3, base_interval_sec=1, cooldown_sec=1),
        state_store=store,
        check_interval_sec=1,
        probe_failures_before_disconnect=1,
    )

    service.run(iterations=1)

    assert controller.reconnect_calls == 1
    assert any(event[0] == "reconnect_success" for event in store.events)


def test_monitor_service_records_reconnect_failure(monkeypatch) -> None:
    monkeypatch.setattr("wireguard_tunnel_service.core.monitor_service.time.sleep", lambda _: None)

    snapshot = HealthSnapshot(
        status=TunnelStatus.DISCONNECTED,
        checked_at=datetime.now(UTC),
        reason="service_not_running",
    )
    checker = FakeChecker(snapshot=snapshot, connectivity_ok=True)
    controller = FakeController(reconnect_result=False)
    store = FakeStateStore(events=[])
    service = MonitorService(
        checker=checker,
        controller=controller,
        policy=ReconnectPolicy(max_retries=3, base_interval_sec=1, cooldown_sec=1),
        state_store=store,
        check_interval_sec=1,
        probe_failures_before_disconnect=1,
    )

    service.run(iterations=1)

    assert controller.reconnect_calls == 1
    assert any(event[0] == "reconnect_failure" for event in store.events)


def test_monitor_service_reconnects_on_degraded_status(monkeypatch) -> None:
    monkeypatch.setattr("wireguard_tunnel_service.core.monitor_service.time.sleep", lambda _: None)

    snapshot = HealthSnapshot(
        status=TunnelStatus.DEGRADED,
        checked_at=datetime.now(UTC),
        reason="url_probe_failed",
    )
    checker = FakeChecker(snapshot=snapshot, connectivity_ok=True)
    controller = FakeController(reconnect_result=True)
    store = FakeStateStore(events=[])
    service = MonitorService(
        checker=checker,
        controller=controller,
        policy=ReconnectPolicy(max_retries=3, base_interval_sec=1, cooldown_sec=1),
        state_store=store,
        check_interval_sec=1,
        probe_failures_before_disconnect=1,
    )

    service.run(iterations=1)
    assert controller.reconnect_calls == 1


def test_monitor_service_disconnects_when_internet_unreachable(monkeypatch) -> None:
    monkeypatch.setattr("wireguard_tunnel_service.core.monitor_service.time.sleep", lambda _: None)

    snapshot = HealthSnapshot(
        status=TunnelStatus.HEALTHY,
        checked_at=datetime.now(UTC),
        reason="ok",
    )
    checker = FakeChecker(
        snapshot=snapshot,
        connectivity_ok=False,
        connectivity_detail="url_error=timed out",
    )
    controller = FakeController(reconnect_result=True, service_running=True)
    store = FakeStateStore(events=[])
    service = MonitorService(
        checker=checker,
        controller=controller,
        policy=ReconnectPolicy(max_retries=3, base_interval_sec=1, cooldown_sec=1),
        state_store=store,
        check_interval_sec=1,
        probe_failures_before_disconnect=1,
    )

    service.run(iterations=1)
    assert controller.disconnect_calls == 1
    assert controller.reconnect_calls == 0
    assert any(event[0] == "tunnel_disconnected_no_internet" for event in store.events)


def test_monitor_service_waits_for_threshold_before_disconnect(monkeypatch) -> None:
    monkeypatch.setattr("wireguard_tunnel_service.core.monitor_service.time.sleep", lambda _: None)

    snapshot = HealthSnapshot(
        status=TunnelStatus.HEALTHY,
        checked_at=datetime.now(UTC),
        reason="ok",
    )
    checker = FakeChecker(
        snapshot=snapshot,
        connectivity_ok=False,
        connectivity_detail="url_error=timed out",
    )
    controller = FakeController(reconnect_result=True, service_running=True)
    store = FakeStateStore(events=[])
    service = MonitorService(
        checker=checker,
        controller=controller,
        policy=ReconnectPolicy(max_retries=3, base_interval_sec=1, cooldown_sec=1),
        state_store=store,
        check_interval_sec=1,
        probe_failures_before_disconnect=3,
    )

    service.run(iterations=2)
    assert controller.disconnect_calls == 0
    assert any(event[0] == "connectivity_probe_failed" for event in store.events)

