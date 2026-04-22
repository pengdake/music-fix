import sys
import os
from loguru import logger


from loguru import logger
import sys
import json

def setup_logger():
    logger.remove()

    def formatter(record):
        return json.dumps({
            "@timestamp": record["time"].isoformat(),
            "log.level": record["level"].name,
            "message": record["message"],
            "log.logger": record["name"],
            "process.thread.name": record["thread"].name,
            "process.pid": record["process"].id,
            "source.file": record["file"].path,
            "source.line": record["line"],
        }, ensure_ascii=False)

    logger.add(
        sys.stdout,
        level="INFO",
        format=formatter,
        backtrace=False,
        diagnose=False,
    )

    return logger