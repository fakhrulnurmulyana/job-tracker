import logging

from pathlib import Path
from typing import List

from job_tracker.core import batch_strip_html
from job_tracker.infrastructure import LoadingStatus
from job_tracker.orchestration.interface import (    
    EditorLauncher,
    FileHandler,
    LinkSplitter,
    JobDocumentSaver,
    JobNormalizer,
    PathResolver,
    StealthScrapper
)
from job_tracker.prompts import build_batch_job_normalization_prompt
from job_tracker.orchestration.job_processor import JobProcessor

logger = logging.getLogger(__name__)


class JobPipelineService:
    """
    End-to-end service for job extraction, cleaning, normalization, and persistence.
    """

    def __init__(
        self,
        editor: EditorLauncher,
        file_handler: FileHandler,
        link_splitter: LinkSplitter,
        paths: PathResolver,
        saver: JobDocumentSaver,
        normalizer: JobNormalizer,
        scrapper: StealthScrapper,
    ) -> None:
        """
        Initialize the JobPipelineService with all required dependencies.

        Args:
            editor (EditorLauncher): Editor launcher instance.
            file_handler (FileHandler): File read/write handler.
            file_splitter (FileSplitter): File splitter utility.
            paths (PathResolver): File path resolver.
            saver (JobDocumentSaver): Job document saver instance.
            normalizer (JobNormalizer): Job normalizer instance.
        """
        self.editor = editor
        self.file_handler = file_handler
        self.link_splitter = link_splitter
        self.paths = paths
        self.saver = saver
        self.normalizer = normalizer
        self.scrapper = scrapper

        logger.debug("JobPipelineService initialized with dependencies.")


    def initiate_file(self, file_name: str) -> Path:
        """
        Create and open a new raw file for job data entry.

        Args:
            file_name (str): Name of the raw file to create.

        Returns:
            Path: Path of the newly created raw file.
        """
        logger.info("Initiating raw file for '%s'", file_name)

        raw_path = self.paths.raw_file(file_name)
        logger.debug("Resolved raw path: %s", raw_path)

        self.file_handler.write(raw_path, content="", overwrite=False)
        logger.debug("Empty raw file created at %s", raw_path)

        self.editor.open(raw_path)
        logger.debug("Editor opened for file %s", raw_path)

        return raw_path
    
    def scrap_content(
        self,
        links,    
    )-> List[str]:
        return self.scrapper.fetch_html(links=links)

            
    def split_content(
        self,
        read_path: Path,
    ) -> List[str]:
        """
        Split raw job file into multiple segments.

        Args:
            read_path (Path): Path of the raw file to split.

        Returns:
            List[str]
        """

        logger.info("Splitting file: %s", read_path)

        content = self.file_handler.consume(read_path)
        logger.debug("File consumed successfully: %s", read_path)

        return self.link_splitter.split(links=content)

    def cleaned_content(
        self,
        contents: List[str],
    ) -> List[str]:
        """
        Clean HTML content from split files and write cleaned files.

        Args:
            contents (List[str]): data to clean.

        Returns:
            List[str]: List of cleaned data.
        """

        logger.info("Cleaning %d split files", len(contents))

        return batch_strip_html(batch_html=contents)

    def normalize_content(
        self, 
        contents: List[str],
        input_fname: str,
    ) -> None:
        """
        Normalize cleaned text contents into structured job documents.

        This method generates normalization prompts from preprocessed
        text data and executes the batch normalization pipeline using
        the configured normalizer. The resulting structured job
        documents are persisted through the configured saver component.

        Args:
            contents (List[str]):
                List of cleaned text contents to be normalized.
            input_fname (str):
                Base filename identifier used for output generation
                and saving processed documents.

        Returns:
            None

        Side Effects:
            - Generates normalization prompts.
            - Executes batch processing via ``job_processor``.
            - Saves normalized job documents to storage.

        Raises:
            Exception:
                Propagates exceptions raised during prompt generation
                or job processing.
        """
        logger.info("Starting normalization for %d cleaned files", len(contents))

        prompts = build_batch_job_normalization_prompt(
            raw_text_list=contents
        )
        logger.debug("Normalization prompts generated.")

        job_processor= JobProcessor(
            prompts=prompts,
            normalizer=self.normalizer, 
            paths=self.paths,
            saver=self.saver,
            handler=self.file_handler,
            input_fname=input_fname,
        )

        job_processor.process()
    
        logger.info("Finalized job documents saved successfully.")


    def process(
        self, 
        file_name: str, 
    ) -> None:
        """
        Execute the full job extraction pipeline: create, split, clean,
        normalize, and save job data, with loading status and error handling.

        Args:
            file_name (str): Base filename to process.

        Raises:
            KeyboardInterrupt: If the process is manually interrupted.
            Exception: If any step in the pipeline fails.
        """
        logger.info("Starting full job pipeline for file '%s'", file_name)

        api_loader = LoadingStatus(f"Normalizing text in file {file_name}.txt ")

        success = False

        try:
            raw_path = self.initiate_file(file_name=file_name)

            split_links = self.split_content(
                read_path=raw_path
            )

            html_content = self.scrap_content(
                links=split_links,    
            )

            self.file_handler.write(
                path=self.paths.scrap_file(name=file_name),
                content=str(html_content),
            )

            # cleaned_data = self.cleaned_content(
            #     contents=html_content,
            # )

            # self.file_handler.write(
            #     path=self.paths.clean_file(name=file_name),
            #     content=str(cleaned_data),
            # )

            api_loader.start()
            logger.debug("LoadingStatus started.")

            self.normalize_content(
                contents=html_content,
                input_fname=file_name,
            )

            success = True
            logger.info("Job pipeline completed successfully for '%s'", file_name)

        except KeyboardInterrupt:
            logger.warning("Process interrupted by user (Ctrl+C)")
            raise

        except Exception:
            logger.exception("Job normalization pipeline failed for '%s'", file_name)
            raise

        finally:
            if success:
                api_loader.true_stop()
                logger.debug("LoadingStatus stopped with success.")
            else:
                api_loader.false_stop()
                logger.debug("LoadingStatus stopped with failure.")