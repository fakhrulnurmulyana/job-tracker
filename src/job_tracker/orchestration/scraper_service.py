import logging
from job_tracker.infrastructure import (
    StealthScrapper,
)

logger = logging.getLogger(__name__)

class ScraperOrchestrator:
    def __init__(self, scraper: StealthScrapper, paths):
        self.scraper = scraper
        self.paths = paths

    def scrape_and_save(self, url: str, file_name: str) -> str:
        logger.info(f"URL Provided. Starting stealth scraper for : {url}")

        html_content = self.scraper.fetch_html(url=url)
        raw_path = self.paths.raw_file(file_name)

        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        logger.info(f"Successfully scraped and saved to {raw_path}")

        return str(raw_path)