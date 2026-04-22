import sys
import os
from loguru import logger


def setup_logger():
    logger.remove()

    log_level = os.getenv("LOG_LEVEL", "INFO")
    env = os.getenv("ENV", "prod")

    logger.add(
        sys.stdout,
        level=log_level,
        serialize=True,
        enqueue=True,
        backtrace=env == "dev",
        diagnose=env == "dev",
    )

    return logger