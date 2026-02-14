from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StateEvent:
    event_type: str
    reason: str
    occurred_at: str


class StateStore:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def initialize(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS state_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    occurred_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def append_event(self, event_type: str, reason: str) -> None:
        occurred_at = datetime.now(UTC).isoformat()
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO state_events(event_type, reason, occurred_at) VALUES (?, ?, ?)",
                (event_type, reason, occurred_at),
            )
            conn.commit()

    def list_events(self, limit: int = 100) -> list[StateEvent]:
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT event_type, reason, occurred_at
                FROM state_events
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [StateEvent(event_type=row[0], reason=row[1], occurred_at=row[2]) for row in rows]
