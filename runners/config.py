"""
Centralized configuration and logging setup for RUNNERS.
"""
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variable from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# General Setting
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false")

# Last Run History File
LAST_RUN_FILE_NAME = os.getenv("LAST_RUN_FILE", "last_run_file.txt")

# Logging
LOG_DIR: Path = BASE_DIR / "logs"
LOG_LEVEL: str = os.getenv("LOG_LEVEL")
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE: Path = LOG_DIR / "runners.log"

# Logging Setting
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("runners")