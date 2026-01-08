import logging
from pathlib import Path

import job_tracker.logging_config  

from job_tracker.settings import load_gemini_config
from job_tracker.services import GeminiClient
from job_tracker.core import JobNormalizer
from job_tracker.prompts.job_normalization import build_job_normalization_prompt
from job_tracker.infrastructure import FileWriter, EditorLauncher, PathResolver
from job_tracker.persistence import JobDocumentSaver

# Module-level logger for this entrypoint
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Application entrypoint that orchestrates the job normalization pipeline.
    """
    # Load and validate external configuration
    config = load_gemini_config()
    
    # Resolve base working directory
    base_path=Path.cwd()

    # Initialize infrastructure and service dependencies
    paths = PathResolver(base_path=base_path)
    file_writer = FileWriter()
    editor = EditorLauncher()
    saver = JobDocumentSaver()
    client = GeminiClient(api_key=config.api_key, model=config.model)
    normalizer = JobNormalizer(client=client)

    # Request user-defined file name for raw input
    file_name = input("Write name for the file: ").strip().lower()

    # Create and open raw input file for user editing
    raw_path = paths.raw_file(file_name)
    file_writer.write(raw_path)
    editor.open(raw_path)

    # Read user-provided job description
    content = raw_path.read_text(encoding="utf-8")

    # Abort early if input is empty and clean up created file
    if content is None or not content.strip():
        file_writer.delete(path=raw_path, base_path=base_path)
        logger.info(
            "Empty content detected; file has been removed: %s",
            raw_path,
        )
        return

    # Build prompt and normalize job description via LLM
    prompt = build_job_normalization_prompt(content)
    job_doc = normalizer.normalize(prompt)

    # Generate output file name based on normalized data
    output_name = f"{job_doc.job.title}_{job_doc.company.name}"
    output_path = paths.processed_file(output_name)

    # Persist normalized job document
    saver.save(job_doc, output_path)

    logger.info("Job normalization finished successfully")

if __name__ == "__main__":
    # Guarded execution to ensure proper logging on fatal errors
    try:
        main()
    except Exception:
        logger.critical("Job normalization pipeline failed")
        raise