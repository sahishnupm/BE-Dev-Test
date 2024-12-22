import logging
import sys
from pathlib import Path
from loguru import logger
from fastapi.logger import logger as fastapi_logger

# Add loguru to requirements.txt
def setup_logging():
    # Remove default handlers
    logging.getLogger().handlers = []
    fastapi_logger.handlers = []

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure loguru
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": "INFO",
            },
            {
                "sink": "logs/app.log",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                "rotation": "1 day",
                "retention": "7 days",
                "level": "DEBUG",
            },
        ],
    }

    logger.configure(**config)
    return logger 