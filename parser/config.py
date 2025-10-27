import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variable from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# General Setting
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false")
DOWNLOAD_DIR: Path = BASE_DIR / os.getenv("DOWNLOAD_DIR", "pin_doc")

# GetMyInvoice API
GMI_API_TOKEN: str = os.getenv("GMI_API_TOKEN", "")
GMI_ACCOUNT_ID: str = os.getenv("GMI_ACCOUNT_ID", "")
GMI_URL: str = os.getenv("GMI_URL", "https://api.getmyinvoices.com/accounts/v3/documents")

# API Header
HEADER: dict = {
    "X-API-KEY": GMI_API_TOKEN,
    "Accept": "application/json",
    "User-Agent": f"pin-fetcher/1.0 {GMI_ACCOUNT_ID}",
    "x-application": "Desktop-App"
}

# Date Format
DATE_FORMAT = "%Y-%m-%d"

# Google Sheet
GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "Order Overview")
GOOGLE_SHEET_WORKSHEET_NAME: str = os.getenv("GOOGLE_SHEET_WORKSHEET_NAME", "PIN Invoices")
GOOGLE_TOKEN: str = os.getenv("GOOGLE_TOKEN", "token.json")

# Logging
LOG_DIR: Path = BASE_DIR / "logs"
LOG_LEVEL: str = os.getenv("LOG_LEVEL")
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE: Path = LOG_DIR / "pin_parser.log"

# Logging Setting
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logging.getLogger("pdfminer").setLevel(logging.WARNING)
logger = logging.getLogger("pin_parser")
