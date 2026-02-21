import logging

from who_am_i.core.config import LoggingConfig

LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}


def setup_logging(config: LoggingConfig) -> None:
    level = LEVEL_MAP.get(config.level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format=config.format,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
