from loguru import logger
import sys

def setup_logger():
    logger.remove()  # Remove default logger
    format = "{time} - {level} - {name} - {function} - {line} - {message} - {extra}"
    logger.add(sys.stdout, level="INFO", format=format, serialize=True, backtrace=True, diagnose=True)
    return logger