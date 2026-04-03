import undetected_chromedriver as uc 
import time 

import logging
import gc
import warnings
warnings.filterwarnings(
    "ignore",
    message=".*handle is invalid"
)

from typing import List


logger = logging.getLogger(__name__)

def _safe_del(self) -> None:
    """Safely quit a Chrome driver instance without raising exceptions.

    Intended as a replacement for :pymeth:`uc.Chrome.__del__` to suppress
    errors that occur when the driver is garbage-collected after the browser
    process has already exited.

    Args:
        self: The :class:`uc.Chrome` instance being destroyed.

    Example:
        >>> uc.Chrome.__del__ = _safe_del
    """
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = _safe_del

class StealthScraper:
    """Stealth web scraper using undetected ChromeDriver.

    Wraps :mod:`undetected_chromedriver` to fetch raw HTML from URLs while
    minimizing bot-detection. Each request spawns a fresh browser instance
    that is unconditionally closed in a ``finally`` block.

    Attributes:
        version_main (int): Major Chrome version passed to
            :class:`uc.Chrome` for driver compatibility.

    Example:
        >>> scraper = StealthScraper(version_main=145)
        >>> html_pages = scraper.fetch_html(["https://example.com"])
    """
    def __init__(self, version_main =145) -> None:
        """Initialize StealthScraper with a target Chrome major version.

        Args:
            version_main (int, optional): Major version of the locally
                installed Chrome browser. Used by undetected-chromedriver to
                download a matching ChromeDriver binary. Defaults to ``145``.

        Example:
            >>> scraper = StealthScraper(version_main=145)
            >>> scraper.version_main
            145
        """
        self.version_main = version_main

    def _fetch_html_one(self, url:str) -> str:
        """Fetch raw HTML from a single URL using a disposable Chrome instance.

        Spawns a new :class:`uc.Chrome` browser, navigates to ``url``, waits
        for the page to fully render, then returns the page source. The
        browser is always closed in the ``finally`` block regardless of
        success or failure.

        Note:
            Headless mode is intentionally disabled; running headless can
            trigger Cloudflare bot-detection challenges.

        Args:
            url (str): Fully-qualified URL to fetch
                (e.g. ``"https://example.com"``).

        Returns:
            str: Raw HTML source of the rendered page.

        Raises:
            Exception: If the response contains bot-block indicators such as
                ``"Apologies"`` or ``"captcha"`` in the page source.

        Example:
            >>> scraper = StealthScraper()
            >>> html = scraper._fetch_html_one("https://example.com")
        """
        logger.info("Starting fetch : %s", url)
         
        options = uc.ChromeOptions()

        # better turn this option off, this is make the driver do not open browser tab, but it can lead to cloudflare error

        # options.add_argument("--headless") 

        driver = uc.Chrome(options=options, version_main = self.version_main)

        try:
            driver.get(url)
            time.sleep(15)
            html = driver.page_source

            if "Apologies" in html or "captcha" in html:
                logger.error("Block detected on %s", url)
                raise Exception("Blcok Detected!")
            
            logger.info("Fetch Success")
            return html
        
        finally:
            if driver is not None:

                try:
                    logger.debug("Closing Browser")
                    driver.quit()
                except Exception:
                    pass

                del driver
                gc.collect()

    def fetch_html(self, links: List[str]) -> List[str]:
        """Fetch raw HTML from a list of URLs sequentially.

        Calls :pymeth:`_fetch_html_one` for each URL in ``links`` and
        collects the results in order. Requests are made sequentially; if
        any single URL raises an exception the entire call propagates it.

        Args:
            links (List[str]): Ordered list of fully-qualified URLs to fetch.

        Returns:
            List[str]: List of raw HTML strings in the same order as
                ``links``.

        Raises:
            Exception: Propagates any exception raised by
                :pymeth:`_fetch_html_one` for the failing URL.

        Example:
            >>> scraper = StealthScraper()
            >>> pages = scraper.fetch_html([
            ...     "https://example.com",
            ...     "https://example.org",
            ... ])
            >>> len(pages)
            2
        """
        return [
            self._fetch_html_one(url=link)
            for link in links
        ]
