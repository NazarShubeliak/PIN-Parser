"""
Main pipeline orchestration.

Coordinates the full flow:
1. Fetch documents
2. Parse PDFs
3. Aggregate totals
4. Push to Google Sheets

Can be triggered manually or automatically.
"""
from parser.config import logger, DOWNLOAD_DIR, GOOGLE_SHEET_NAME, GOOGLE_SHEET_WORKSHEET_NAME
from parser.api_client import fetch_documents, download_all_documents
from parser.tools import clear_folder, find_document
from parser.pdf_parser import run_parser
from parser.sheet import SheetService

def run_pipeline(start_date: str, end_date: str) -> None:
    """Run the full PIN parsing pipeline"""
    logger.info("Start PIN Parsing")

    # Step 1: Delete old documents
    clear_folder(DOWNLOAD_DIR)
    logger.info(f"Delete old documents")

    # Step 2: Find all documents 
    documents = fetch_documents(start_date, end_date)
    logger.info(f"Found {len(documents)} documents")

    # Step 3: Download documents
    download_all_documents(documents, DOWNLOAD_DIR)
    logger.info(f"Download all documents to {DOWNLOAD_DIR}")

    # Step 4: Parsing document
    filename = find_document(DOWNLOAD_DIR)
    german, non_europe, europe = run_parser(filename) # German, NON-Europe, Europe

    # Step 5: Add data to Google Sheet
    sheet_service = SheetService(GOOGLE_SHEET_NAME)
    sheet_service.append_rows(GOOGLE_SHEET_WORKSHEET_NAME, [german, non_europe, europe])
