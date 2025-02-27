import logging
import os

LOGGING_LEVEL = getattr(logging, os.getenv("LOGGING_LEVEL", "INFO").upper(), logging.INFO)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger