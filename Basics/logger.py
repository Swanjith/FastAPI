import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path # file path
from config import settings # import log level settings

# Ensure logs directory exists
log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "app.log"

# Use settings.LOG_LEVEL from config
level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Root logger
logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(level)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Console handler (optional for development)
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler with rotation (1MB per file, keep 3 backups)
file_handler = RotatingFileHandler(
    filename=str(log_file),
    mode="a",
    maxBytes=1 * 1024 * 1024,  # 1 MB
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
