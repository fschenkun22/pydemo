from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from wireguard_tunnel_service.core.config import LoggingSettings


def configure_logging(settings: LoggingSettings) -> None:
    log_dir = Path(settings.directory)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / settings.filename

    root = logging.getLogger()
    root.setLevel(settings.level.upper())
    root.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(
        log_path,
        maxBytes=settings.max_bytes,
        backupCount=settings.backup_count,
        encoding="utf-8",
    )
    rotating_handler.setFormatter(formatter)

    root.addHandler(stream_handler)
    root.addHandler(rotating_handler)

