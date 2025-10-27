import re
from typing import List, Tuple, Dict
from pathlib import Path
import pdfplumber
from pdfplumber.page import Page
from parser.config import logger


def run_parser(filepath: Path) -> Tuple[float, float, float]:
    """
    Parses a PIN invoice PDF and returns totals for German, NON-EU, and EU regions.

    Args:
        filepath (Path): Path to the PDF file.

    Returns:
        Tuple[float, float, float]: Totals for German, NON-EU, and EU.
    """

    # Step 1: Read PDF file
    with pdfplumber.open(filepath) as pdf:
        try:
            # Step 2: Get table and total with Europe and NON-Europe
            table_str, total_eu = parse_europe_and_non_europe(pdf.pages)
            logger.debug("Get table and total with Europe and NON-Europe")

            # Step 3: Get total sum
            total = parse_total_sum(pdf.pages)
            logger.debug("Get total for all country")

            # Step 4: Group Europe with NON-Europe
            group = group_europe_and_non_europe(table_str)
            logger.debug("Create dict with Europe and NON-Europe data")

            # Step 5: Doing calculate
            german = total - total_eu
            non_europe = group["NON-EU"]["total"]
            europe = group["EU"]["total"]
            logger.debug("Get all necessary data")

            # Step 6: Return value
            return german, non_europe, europe
        except Exception as e:
            logger.warning(f"Failed to find all rows in {filepath}: {e}", exc_info=True)


def group_europe_and_non_europe(table: str) -> List[Dict[str, float]]:
    """
    Group Europe and NON-Europe

    Args:
        table (str): table like str from PDF

    Returns:
        Dict[Dict[str, float]]: return group value

    Example:
        "EU": {
            "items": ...
            "total": ...
        },
        "NON-EU": {
            "items": ...
            "total": ...
        }
    """

    def parse_table(table: str) -> list[Dict[str, float]]:
        """Parse table"""
        items = table.split("\n")
        parse = []
        for line in items:
            part = line.strip().split()
            if len(part) >= 7:
                parse.append(
                    {
                        "description": part[-5],
                        "price": float(part[-2].replace(".", "").replace(",", ".")),
                    }
                )
        return parse

    def sum_total(items: List[Dict[str, float]]) -> float:
        """Summ all value"""
        result = sum(i["price"] for i in items)
        return round(result, 2)

    eu_items = []
    non_eu_items = []
    items = parse_table(table)

    for item in items:
        if "NON-EU" in item["description"].upper():
            non_eu_items.append(item)
        else:
            eu_items.append(item)

    return {
        "EU": {"itmes": eu_items, "total": sum_total(eu_items)},
        "NON-EU": {"items": non_eu_items, "total": sum_total(non_eu_items)},
    }


def parse_europe_and_non_europe(pages: list[Page]) -> Tuple[str, float]:
    """
    Parsing table with Europe and NON-Europe data

    Args:
        pages (list[Page]): List of all pages

    Returns:
        Tuple[str, float]: Return table like 'str' and total sum
    """
    word = "Europasendungen"
    for page in pages:
        text = page.extract_text()
        if word in text:
            logger.info(f"Check if word: '{word}' in page")
            match = re.search(
                r"\d+\s+Europasendungen(.*?)\d+\s+Summe Europasendungen\s+([\d,.]+)",
                text,
                re.DOTALL,
            )
            if match:
                table_str = match.group(1).strip()
                total = match.group(2).replace(".", ",").replace(",", ".")
                logger.debug("Find table with total value")
                return table_str, float(total)
            else:
                logger.warning("Not found table")


def parse_total_sum(pages: List[Page]) -> float:
    """
    Get total sum for German, NON-Europe, Europe

    Args:
        pages (List[Page]): List of all pages

    Returns:
        float: total sum of all regions
    """
    word = "Endsumme"
    for page in pages:
        text = page.extract_text()
        if word in text:
            match = re.search(r"Endsumme\s+EUR\s+([\d\.,]+)", text)
            if match:
                value = match.group(1).replace(".", "").replace(",", ".")
                logger.debug(f"Find word:{word} in pages")
                return float(value)
