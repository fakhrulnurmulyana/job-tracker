import logging
import os
from pathlib import Path

from dotenv import load_dotenv

import job_tracker.logging_config 

from job_tracker.settings import load_gemini_config
from job_tracker.services import GeminiClient
from job_tracker.core import JobNormalizer
from job_tracker.prompts.job_normalization import build_job_normalization_prompt
from job_tracker.infrastructure import FileWriter, EditorLauncher, PathResolver
from job_tracker.persistence import JobDocumentSaver

logger = logging.getLogger(__name__)

def main() -> None:
    config = load_gemini_config()
    
    base_path=Path.cwd()

    paths = PathResolver(base_path=base_path)
    file_writer = FileWriter()
    editor = EditorLauncher()
    saver = JobDocumentSaver()
    client = GeminiClient(api_key=config.api_key, model=config.model)
    normalizer = JobNormalizer(client=client)

    file_name = input("Write name for the file: ").strip().lower()

    raw_path = paths.raw_file(file_name)
    file_writer.write(raw_path)
    editor.open(raw_path)

    content = raw_path.read_text(encoding="utf-8")

    if content is None or not content.strip():
        file_writer.delete(path=raw_path, base_path=base_path)
        logger.info("")
        return

    prompt = build_job_normalization_prompt(content)
    job_doc = normalizer.normalize(prompt)

    output_name = f"{job_doc.job.title}_{job_doc.company.name}"
    output_path = paths.processed_file(output_name)

    saver.save(job_doc, output_path)

    logger.info("Job normalization finished successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.critical("Job normalization pipeline failed")
        raise