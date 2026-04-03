import logging

from typing import List

logger = logging.getLogger(__name__)


class LinkSplitter:
    """Concrete implementation of link splitting by whitespace delimiter.

    Splits a raw string of URLs into individual entries by whitespace,
    stripping surrounding whitespace from each token and discarding
    any empty entries that result from consecutive delimiters.

    Example:
        >>> splitter = LinkSplitter()
        >>> splitter.split("https://a.com  https://b.com")
        ['https://a.com', 'https://b.com']
    """ 
    def split(self, links:str)->List[str]:
        """Split a whitespace-delimited string of URLs into a list.

        Tokenizes ``links`` on any whitespace (spaces, tabs, newlines),
        strips each token, and filters out empty strings. Returns an
        empty list if ``links`` is falsy.

        Args:
            links (str): Raw string containing one or more URLs separated
                by whitespace.

        Returns:
            List[str]: Ordered list of non-empty URL strings extracted
                from ``links``. Returns ``[]`` if ``links`` is empty or
                falsy.

        Example:
            >>> splitter = LinkSplitter()
            >>> splitter.split("https://a.com\\nhttps://b.com")
            ['https://a.com', 'https://b.com']
            >>> splitter.split("")
            []
        """
        logger.debug("Starting split links operation.")

        if not links:
            logger.warning("Received empty data for splitting.")
            return []

        logger.debug(
            "Splitting data by space (input size=%d chars)",
            len(links),
        )

        split_links = [
            job.strip()
            for job in links.split()
            if job.strip()
        ]

        logger.info("File successfully split into %d job segments.", len(split_links))
        logger.debug("File split operation completed.")
        
        return split_links