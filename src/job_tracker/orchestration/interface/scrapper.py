from typing import List, Protocol

class StealthScrapper(Protocol):
    def fetch_html(self, links: List[str]) -> List[str]:
        ...
