from typing import List, Protocol

class StealthScraper(Protocol):
    """Contract for stealth HTML fetching strategies.

    Defines the interface for scraper implementations that retrieve raw
    HTML from a list of URLs while minimizing bot-detection risk.

    Implementations are responsible for browser lifecycle management,
    anti-detection configuration, and error handling per request.

    Example:
        >>> class MyScaper:
        ...     def fetch_html(self, links: List[str]) -> List[str]:
        ...         return [requests.get(l).text for l in links]
        >>> scraper: StealthScraper = MyScraper()
    """
    def fetch_html(self, links: List[str]) -> List[str]:
        """Fetch raw HTML from a list of URLs.

        Args:
            links (List[str]): Ordered list of fully-qualified URLs to fetch.

        Returns:
            List[str]: List of raw HTML strings in the same order as
                ``links``.

        Raises:
            Exception: Propagates any exception raised during fetching
                for the failing URL.

        Example:
            >>> scraper.fetch_html(["https://example.com"])
            ['<!DOCTYPE html>...']
        """
        ...