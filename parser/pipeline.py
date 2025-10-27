
from parser.config import logger, DOWNLOAD_DIR
from parser.api_client import fetch_documents, download_all_documents
from parser.tools import clear_folder, find_document
from parser.pdf_parser import run_parser

def run_pipeline(start_date: str, end_date: str) -> None:
    """Run the full PIN parsing pipeline"""
    logger.info("Start PIN Parsing")

    # Step 1: Delete old documents
    clear_folder(DOWNLOAD_DIR)
    logger.info(f"Delete old documents")

    # Step 2: Find all documents 
    documents = fetch_documents(start_date, end_date)
    logger.info(f"Found {len(documents)} documents")

    # Step 3: Download all documents
    download_all_documents(documents, DOWNLOAD_DIR)
    logger.info(f"Download all documents to {DOWNLOAD_DIR}")

    # Step 4: Parsing document
    filename = find_document(DOWNLOAD_DIR)
    german, non_europe, europe = run_parser(filename) # German, NON-Europe, Europe