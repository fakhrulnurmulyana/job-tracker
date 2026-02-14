import logging
from typing import List
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def _strip_html(html: str) -> str:
    """
    Remove HTML tags and return cleaned plain text.

    This function parses the input HTML string using BeautifulSoup
    and extracts readable text content while preserving word spacing.

    Args:
        html (str): Raw HTML content.

    Returns:
        str: Cleaned text with HTML tags removed.

    Raises:
        ValueError: If html is None.
        Exception: If HTML parsing fails.
    """
    logger.debug("Starting HTML stripping process.")

    if html is None:
        logger.error("Received None as html input.")
        raise ValueError("html must not be empty")

    try:
        result = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        logger.debug("HTML stripping successful. Output length=%s", len(result))
        return result

    except Exception:
        logger.exception("Failed while stripping HTML.")
        raise


def batch_strip_html(batch_html: List[str], data_length: int) -> List[str]:
    """
    Clean multiple HTML strings in batch mode.

    This function validates that the input batch length matches
    the expected data length before processing. Each HTML string
    is stripped and converted to lowercase.

    Args:
        batch_html (List[str]): List of raw HTML strings.
        data_length (int): Expected number of HTML items.

    Returns:
        List[str]: List of cleaned and lowercase text strings.

    Raises:
        ValueError: If batch_html length does not match data_length.
        Exception: If any individual HTML cleaning fails.
    """
    batch_html_length =len(batch_html)

    if batch_html_length != data_length:
      expected = data_length
      actual = batch_html_length

      logger.error(
          "Cleaning text failed — mismatch length (expected=%d, actual=%d)",
          expected,
          actual,
      )

      raise ValueError(
          f"Batch HTML length mismatch (expected={expected}, actual={actual})"
      )

    logger.info("Starting batch HTML cleaning. Total items=%s", data_length)

    results: List[str] = []

    for idx, html in enumerate(batch_html):
        logger.debug("Processing item index=%s", idx)

        try:
            result = _strip_html(html=html).lower()
            results.append(result)

        except Exception:
            logger.exception("Failed processing item index=%s", idx)
            raise

    logger.info(
        "Batch HTML cleaning completed successfully. Processed=%s items",
        len(results),
    )

    return results