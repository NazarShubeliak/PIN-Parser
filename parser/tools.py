"""
Simpli tools 

Includes:
- Clear Folder
- Find PDF document
"""
import os
from pathlib import Path
from typing import List
from parser.config import logger


def clear_folder(folder_path: Path) -> None:
    """
    Delete all files in folder 

    Args:
        folder_path (Path): path to folder.
    """
    for filename in os.listdir(folder_path):
        file_path = folder_path / filename
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {e}")

def find_document(folder_path: Path) -> List[str]:
    """
    Get document path from folder

    Args:
        folder_path (Path): Path to folder
    
    Returns:
        List[str]: List of all documents
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") and not filename.endswith("Mail_AG.pdf"):
            document_path = folder_path / filename
            logger.info(f"In folder: {folder_path} find {filename} documents")
            return document_path

