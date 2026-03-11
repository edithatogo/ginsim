import sys

from loguru import logger


def setup_logging(level: str = "INFO", log_file: str = "outputs/logs/run.log"):
    """
    Configures loguru logging with a standard research-grade format.
    """
    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
    )

    # File handler
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="10 MB",
    )

    return logger

# Default setup
setup_logging()
