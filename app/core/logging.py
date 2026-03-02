import logging
import sys


def configure_logging(debug: bool = False) -> None:
    """Configure root logging for the application.

    Sets a sane default formatter and routes output to stdout so containers capture logs.
    """
    level = logging.DEBUG if debug else logging.INFO
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Basic configuration
    logging.basicConfig(level=level, format=fmt, stream=sys.stdout)

    # Make sure uvicorn loggers use the same handlers/level when running under uvicorn
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # avoid duplicate handlers if they already exist
        if not logger.handlers:
            logger.handlers = logging.getLogger().handlers


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the provided name."""
    return logging.getLogger(name)

