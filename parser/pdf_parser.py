import re
from typing import List, Tuple, Dict
from pathlib import Path
import pdfplumber
from pdfplumber.page import Page
from parser.config import logger


def parse_pdf(filepath: Path) -> Tuple[float, float, float]:
    """
    Parses a single PDF and returns totals for GERMAN, NON-EUROPE, EU

    Args:
        filepath (Path): path to file.

    Returns:
        Tuple[float, float, float]: GERMAN, NON-EUROPE, EUROPE totals
    """
    with pdfplumber.open(filepath) as pdf:
        try:
            block, total_EU = parse_europasendungen(pdf.pages)
            total = parse_total(pdf.pages)
            grouped = group_items(parse_block(block))

            german = total - total_EU
            non_europe = grouped["NON-EU"]["total"]
            europe = grouped["EU"]["total"]

            logger.info(
                f"Parsed {filepath.name}: GERMAN={german}, NON-EU={non_europe}, EUROPE={europe}"
            )
            return german, non_europe, europe
        except Exception as e:
            logger.warning(f"Failed to parse {filepath.name}: {e}")


def parse_total(pages: List[Page]) -> float:
    """
    Extracts the total invoice amount from the PDF pages.

    Args:
        pages (List[Page]): List of PDF page.

    Return:
        float: Total amount in EUR
    """
    logger.info("Try find 'Endsumme' in PDF")
    for page in pages:
        word = "Endsumme"
        text = page.extract_text()
        if word in text:
            match = re.search(r"Endsumme\s+EUR\s+([\d\.,]+)", text)
            if match:
                value = match.group(1).replace(".", "").replace(",", ".")
                return float(value)
    else:
        logger.warning("'Endsumme' not found in PDF")


def parse_europasendungen(pages: List[Page]) -> Tuple[str, float]:
    """
    Extracts Europasendungen block and its total form PDF.

    Args:
        pages (List[Page]): List of PDF page.

    Return:
        Tuple[str, float]: Text block and total amount.
    """
    word = "Europasendungen"
    for page in pages:
        text = page.extract_text()
        if word in text:
            match = re.search(
                r"\d+\s+Europasendungen(.*?)\d+\s+Summe Europasendungen\s+([\d,.]+)",
                text,
                re.DOTALL,
            )
            if match:
                block = match.group(1).strip()
                total = match.group(2).replace(".", "").replace(",", ".")
                logger.debug(
                    f"""
                    Block: {block},
                    Total: {total}
                """
                )
                return block, float(total)


def parse_block(block: str) -> List[Dict[str, float]]:
    """
    Parses Europasendungen block into structured items.

    Args:
        block (str): block of table

    Returns:
        List[Dict[str, float]]: List of items with description and price.
    """
    items = block.split("\n")
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


def group_items(
    items: List[Dict[str, float]],
) -> Dict[str, Dict[str, float | List[Dict[str, float]]]]:
    """
    Group items into EU and NON-EU categories.

    Args:
        itesm (List[Dict[str, float]]): EU and NON-EU block

    Return:
        Dict[str, Dict]: Grouped items and their totals
    """
    eu_items = []
    non_eu_items = []
    items = parse_block(block=items)

    for item in items:
        if "NON-EU" in item["description"].upper():
            non_eu_items.append(item)
        else:
            eu_items.append(item)

    # total = lambda group: round(sum(i["price"] for i in group), 2)

    return {
        "EU": {"itmes": eu_items, "total": total(eu_items)},
        "NON-EU": {"items": non_eu_items, "total": total(non_eu_items)},
    }


def total(group: List[Dict[str, float]]) -> float:
    """
    Calculates the total price of all items in the group

    Args:
        group (List[Dict[str, float]]): List of items with 'price' field

    Returns:
        float: Rounded total price
    """
    return round(sum(i["price"] for i in group), 2)
