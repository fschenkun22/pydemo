from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReconnectPolicy:
    max_retries: int = 3
    base_interval_sec: int = 10
    cooldown_sec: int = 300

    def next_backoff_sec(self, attempt: int) -> int:
        if attempt < 1:
            raise ValueError("attempt must be >= 1")
        return int(self.base_interval_sec * (2 ** (attempt - 1)))

    def has_remaining_retry(self, failed_attempts: int) -> bool:
        return failed_attempts < self.max_retries
