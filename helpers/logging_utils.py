"""Logging helpers for notebook-friendly demos."""

from __future__ import annotations

import logging
from pathlib import Path


def setup_notebook_logging(
    name: str = "course.notebook",
    *,
    level: int = logging.INFO,
    log_file: str | Path | None = None,
) -> logging.Logger:
    """Create a console-first logger, optionally with a file handler."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(stream_handler)

        if log_file is not None:
            path = Path(log_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(path)
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
            logger.addHandler(file_handler)

    return logger
