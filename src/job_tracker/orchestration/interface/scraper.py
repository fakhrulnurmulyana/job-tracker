from typing import List, Protocol

class StealthScraper(Protocol):
    def fetch_html(self, links: List[str]) -> List[str]:
        ...
