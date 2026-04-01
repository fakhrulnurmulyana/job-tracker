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

def _safe_del(self):
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = _safe_del

class StealthScraper:
    def __init__(self, version_main =145):
        self.version_main = version_main

    def _fetch_html_one(self, url:str) -> str:
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
        return [
            self._fetch_html_one(url=link)
            for link in links
        ]
