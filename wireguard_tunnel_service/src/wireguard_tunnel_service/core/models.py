from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TunnelStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    status: TunnelStatus
    checked_at: datetime
    reason: str
    reason_detail: str | None = None
    rx_bytes: int | None = None
    tx_bytes: int | None = None
