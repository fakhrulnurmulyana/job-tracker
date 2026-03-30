import logging
from pathlib import Path

import job_tracker.logging_config  

from job_tracker.settings import load_gemini_config
from job_tracker.services import GeminiClient
from job_tracker.core import JobNormalizer
from job_tracker.infrastructure import (
    FileHandler,
    FileSplitter,
    JobDocumentSaver,
    EditorLauncher,
    PathResolver,
    input_fname,
    StealthScrapper,
)
import undetected_chromedriver as uc 
from job_tracker.orchestration import JobPipelineService


logger = logging.getLogger(__name__)

def _safe_del(self):
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = _safe_del


def main() -> None:
    """
    Entry point for the job normalization pipeline.

    This function initializes all dependencies required for the
    JobPipelineService, including the Gemini client, normalizer,
    file handlers, and path resolver. It prompts the user for a
    file name and executes the full job pipeline.

    Steps:
        1. Load Gemini API configuration.
        2. Initialize LLM client (GeminiClient) and JobNormalizer.
        3. Set up file handling, splitting, and saving services.
        4. Prompt user for raw file name.
        5. Execute the JobPipelineService.process() method to
           perform full ETL, normalization, and saving of job documents.

    Raises:
        Exception: Propagates any unhandled exceptions during pipeline execution.
    """
    config = load_gemini_config()
    base_path = Path.cwd()

    client = GeminiClient(
        api_key=config.api_key,
        model=config.model,
    )

    normalizer = JobNormalizer(client=client)

    # move the paths so we can use it for scrapping
    paths = PathResolver(base_path=base_path)

    pipeline = JobPipelineService(
        editor=EditorLauncher(),
        file_handler=FileHandler(),
        file_splitter=FileSplitter(),
        paths=paths, # changing this
        saver=JobDocumentSaver(),
        normalizer=normalizer,
    )

    file_name = input_fname()

    # START INJECTION
    # ask for URL, if provided, scrape it into the file.
    glints_url = input("Enter Glints URL to scrape (leave empty to past manually) : ").strip()

    if glints_url:
        logger.info("URL Provided. Starting stealth scraper...")
        scraper = StealthScrapper()
        html_content = scraper.fetch_html(glints_url)

        # resolve where the pipeline expects the file to be
        raw_path = paths.raw_file(file_name)

        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Successfully scraped and saved to {raw_path}")

    # END INJECTION

    pipeline.process(file_name)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.critical("Unhandled exception in main entry point")
        exc_info=True,
        raise