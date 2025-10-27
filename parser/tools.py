import os
from pathlib import Path
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