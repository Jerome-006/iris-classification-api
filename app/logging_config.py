import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import settings


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging,settings.LOG_LEVEL))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)