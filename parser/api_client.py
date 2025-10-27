import os
from typing import List, Dict, Any
from pathlib import Path
import requests
from parser.config import GMI_URL, HEADER, logger


def download_all_documents(documents: List[Dict[str, Any]], folder_path: Path) -> None:
    """
    Download all documents from the provided list and saves the to folder

    Args:
        documents (List[Dict[str, Any]]): A list of document metadata dicitonaires from GetMyInvoice
        folder_path (Path): Path to directory where all documents will ba saved
    """

    logger.info("Start download documents")
    for doc in documents:
        try:
            download_document(doc, folder_path)
        except Exception as e:
            logger.error(f"Failed to download document {doc.get("documentUid")}: {e}")
            raise


def fetch_documents(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Fetch documents from GetMyInvoice API within a date range.

    Args:
        start_date (str): Start date in ISO format (YYYY-MM-DD)
        end_date (str): End date in ISO format (YYY-MM-DD)

    Returns:
        List[Dict[str, Any]]: A list of document metadata dictionaries. Each dictionary contains fields
        such as 'documentUid', 'companyName', 'filename', 'date', etc.
    """
    params = {
        "searchQuery": "PIN",  # знайде testpin, PIN AG, PIN Mail AG
        "archivedFilter": 1,  # будь-які документи, включно з архівними
        "documentTypeFilter": "INCOMING_INVOICE",  # або "all" якщо хочеш усе
        "startDateFilter": start_date,
        "endDateFilter": end_date,
        "perPage": 500,
        "pageNumber": 1,
        "includeThumbnailUrl": False,
        "loadLineItems": False,
    }
    logger.info(f"Fetching documents from {start_date} to {end_date}")
    res = requests.get(GMI_URL, headers=HEADER, params=params)
    return res.json()["records"]


def download_document(document: Dict[str, Any], folder_path: Path) -> None:
    """
    Download a documents by its ID and save it locally under the specified filename

    Args:
        document (str): One document in GetMyInvoice.
        folder_name (Path): Download directory
    """
    doc_id = document.get("documentUid", "unknown")
    company = document.get("companyName", "unknown").replace(" ", "_")
    filename = f"{doc_id}_{company}.pdf"
    file_path = folder_path / filename
    logger.info(f"Formated file: {filename}")

    url = f"{GMI_URL}/{doc_id}/file"
    logger.info(f"Formated url: {url}")
    response = requests.get(url, headers=HEADER, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info("Download file")
    else:
        logger.error(f"Error status code: {response.status_code}: {response.text}")
