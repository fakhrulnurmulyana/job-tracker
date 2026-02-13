import logging
from pathlib import Path

import job_tracker.logging_config  

from job_tracker.settings import load_gemini_config
from job_tracker.services import GeminiClient, JobPipelineService
from job_tracker.core import JobNormalizer
from job_tracker.infrastructure import (
    FileHandler,
    FileSplitter,
    EditorLauncher,
    PathResolver,
    silent_input,
)
from job_tracker.persistence import JobDocumentSaver


logger = logging.getLogger(__name__)


def main() -> None:
    config = load_gemini_config()
    base_path = Path.cwd()

    client = GeminiClient(
        api_key=config.api_key,
        model=config.model,
    )

    normalizer = JobNormalizer(client=client)

    pipeline = JobPipelineService(
        editor=EditorLauncher(),
        file_handler=FileHandler(),
        file_splitter=FileSplitter(),
        paths=PathResolver(base_path=base_path),
        saver=JobDocumentSaver(),
        normalizer=normalizer,
    )

    file_name = silent_input("Write name for the file: ")

    pipeline.process(file_name)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.critical("Unhandled exception in main entry point")
        exc_info=True,
        raise