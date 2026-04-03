import logging

from typing import Protocol, List

logger = logging.getLogger(__name__)


class LinkSplitter(Protocol):
    """Protocol defining the interface for link-splitting strategies.

    Any class implementing this protocol must provide a ``split`` method
    that partitions a raw string of links into an ordered list of
    individual URL strings.

    Example:
        >>> class CommaSplitter:
        ...     def split(self, links: str) -> List[str]:
        ...         return [l.strip() for l in links.split(",")]
        >>> splitter: LinkSplitter = CommaSplitter()
    """
    def split(
        self, 
        links:str
    )->List[str]:
        """Split a raw string of links into a list of individual URLs.

        Args:
            links (str): Raw string containing one or more URLs,
                separated by an implementation-defined delimiter.

        Returns:
            List[str]: Ordered list of individual URL strings extracted
                from ``links``.

        Example:
            >>> splitter.split("https://a.com,https://b.com")
            ['https://a.com', 'https://b.com']
        """
        ...