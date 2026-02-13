import logging
from typing import List
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def _strip_html(html: str) -> str:
    """
    Remove HTML tags and return clean text.
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
    Process multiple HTML strings and return cleaned lowercase text.
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