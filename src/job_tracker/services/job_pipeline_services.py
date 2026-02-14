import logging

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from job_tracker.core import batch_strip_html, LLMClient
from job_tracker.infrastructure import LoadingStatus, batch_file_naming
from job_tracker.schemas import JobDocumentSchema
from job_tracker.prompts import build_batch_job_normalization_prompt


logger = logging.getLogger(__name__)

class EditorLauncher(ABC):
    """
    Abstract base class for launching a system editor.

    Implementations should provide a method to open a file
    in a specified editor or fall back to system defaults.
    """

    @abstractmethod
    def open(
        self, 
        path: Path, 
        editor: Optional[str] = None
    ) -> None:
        """
        Open a file in an editor.

        Args:
            path (Path): Path to the file to open.
            editor (Optional[str]): Editor program to use. Defaults to system editor.

        Raises:
            NotImplementedError: If method is not implemented in subclass.
        """
        ...


class FileHandler(ABC):
    """
    Abstract base class for handling file operations.

    Implementations should support writing, reading, and batch processing of files.
    """

    @abstractmethod
    def write(
        self,
        path: Path,
        content: Optional[str],
        overwrite: bool,
    ) -> None:
        """
        Write content to a file.

        Args:
            path (Path): File path to write.
            content (Optional[str]): File content.
            overwrite (bool): Whether to overwrite if the file exists.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...
        
    @abstractmethod
    def write_batch(
        self,
        paths: List[Path],
        contents: List[str],
    )->None:
        """
        Write multiple files in batch.

        Args:
            paths (List[Path]): List of file paths.
            contents (List[str]): Corresponding file contents.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...

    @abstractmethod
    def consume(self, path: Path)->str:
        """
        Read and validate a single file.

        Args:
            path (Path): File path to read.

        Returns:
            str: File content.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...
        
    @abstractmethod
    def batch_consume(self, paths:List[Path])->List[str]:
        """
        Read and validate multiple files.

        Args:
            paths (List[Path]): List of file paths.

        Returns:
            List[str]: List of file contents.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...


class FileSplitter:
    """
    Handles splitting large text content into smaller segments.
    """

    @abstractmethod 
    def split(self, data:str)->tuple:
        """
        Split text data into smaller segments.

        Args:
            data (str): Raw text data to split.

        Returns:
            tuple: A tuple (list of split segments, number of segments).

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...
    

class JobDocumentSaver(ABC):
    """
    Abstract base class for saving job documents to disk.
    """

    @abstractmethod
    def batch_save(
        self, 
        docs: List[JobDocumentSchema], 
        paths: List[Path],
    )-> None:
        """
        Save multiple job documents in batch.

        Args:
            docs (List[JobDocumentSchema]): List of normalized job documents.
            paths (List[Path]): Corresponding output file paths.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...


class PathResolver(ABC):
    """
    Abstract base class for resolving application file paths.
    """

    @abstractmethod
    def raw_file(
        self, 
        name: str, 
        suffix: str,
    ) -> Path:
        """
        Resolve path for raw input file.

        Args:
            name (str): Base filename.
            suffix (str): File extension.

        Returns:
            Path: Resolved path.
        """
        ...
    
    @abstractmethod
    def batch_cleaned_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for batch cleaned files.

        Args:
            name (str): Base filename.
            data_length (int): Number of files to generate.
            suffix (str): File extension.

        Returns:
            List[Path]: List of resolved paths.
        """
        ...
    
    @abstractmethod
    def split_path(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for split files.

        Args:
            name (str): Base filename.
            data_length (int): Number of segments.
            suffix (str): File extension.

        Returns:
            List[Path]: List of resolved split file paths.
        """
        ...
    
    @abstractmethod
    def batch_finalized_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for finalized job documents.

        Args:
            name (str): Base filename(s).
            data_length (int): Number of files.
            suffix (str): File extension (usually .json).

        Returns:
            List[Path]: List of resolved paths.
        """
        ...

class JobNormalizer(ABC):
    """
    Abstract base class for job document normalization.
    """

    @abstractmethod
    def batch_normalize(self, prompts:List[str])->List[JobDocumentSchema]:
        """
        Normalize a batch of prompts into structured job documents.

        Args:
            prompts (List[str]): List of normalization prompts.

        Returns:
            List[JobDocumentSchema]: List of normalized job documents.
        """
        ...


class GeminiJobNormalizer(JobNormalizer):
    """
    LLM-based job normalizer using Gemini client.
    """

    def __init__(self, client: LLMClient):
        """
        Initialize GeminiJobNormalizer.

        Args:
            client (LLMClient): LLM client instance used for normalization.
        """
        self.client = client

    def normalize(self, prompt: str) -> JobDocumentSchema:
        """
        Normalize a single prompt into a JobDocumentSchema.

        Args:
            prompt (str): Text prompt for normalization.

        Returns:
            JobDocumentSchema: Normalized job document.
        """
        ...


class JobPipelineService:
    """
    End-to-end service for job extraction, cleaning, normalization, and persistence.
    """

    def __init__(
        self,
        editor: EditorLauncher,
        file_handler: FileHandler,
        file_splitter: FileSplitter,
        paths: PathResolver,
        saver: JobDocumentSaver,
        normalizer: JobNormalizer,
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
        self.file_splitter = file_splitter
        self.paths = paths
        self.saver = saver
        self.normalizer = normalizer

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


    def split_file(
        self,
        file_name: str,
        read_path: Path,
    ) -> Tuple[List[Path], int]:
        """
        Split raw job file into multiple segments.

        Args:
            file_name (str): Base filename for segments.
            read_path (Path): Path of the raw file to split.

        Returns:
            Tuple[List[Path], int]: List of split file paths and number of segments.
        """

        logger.info("Splitting file: %s", read_path)

        content = self.file_handler.consume(read_path)
        logger.debug("File consumed successfully: %s", read_path)

        split_data, length_data_split = self.file_splitter.split(data=content)
        logger.info("File split into %d segments", length_data_split)

        split_path = self.paths.split_path(
            name=file_name,
            data_length=length_data_split
        )
        logger.debug("Generated split paths: %s", split_path)

        self.file_handler.write_batch(
            paths=split_path,
            contents=split_data,
        )
        logger.debug("Split files written successfully.")

        return split_path, length_data_split

    def cleaned_file(
        self,
        file_name: List[str],
        read_path: List[Path],
        data_length: int,
    ) -> Tuple[List[Path], int]:
        """
        Clean HTML content from split files and write cleaned files.

        Args:
            file_name (List[str]): Base filenames for cleaned files.
            read_path (List[Path]): Paths of split files to clean.
            data_length (int): Number of files to process.

        Returns:
            Tuple[List[Path], int]: List of cleaned file paths and number of files.
        """

        logger.info("Cleaning %d split files", data_length)

        content = self.file_handler.batch_consume(read_path)
        logger.debug("Batch file consume completed.")

        cleaned_data = batch_strip_html(
            batch_html=content,
            data_length=data_length
        )
        logger.debug("HTML stripping completed.")

        cleaned_path = self.paths.batch_cleaned_file(
            name=file_name,
            data_length=data_length
        )
        logger.debug("Resolved cleaned file paths: %s", cleaned_path)

        self.file_handler.write_batch(
            paths=cleaned_path,
            contents=cleaned_data
        )
        logger.info("Cleaned files successfully written.")

        return cleaned_path, data_length


    def normalize(
        self, 
        read_path: List[Path], 
        data_length: int,
    ) -> None:
        """
        Normalize cleaned job files into structured JobDocumentSchema objects
        and persist the results to finalized paths.

        Args:
            read_path (List[Path]): Paths of cleaned files to normalize.
            data_length (int): Number of files to normalize.
        """
        logger.info("Starting normalization for %d cleaned files", data_length)

        content = self.file_handler.batch_consume(read_path)
        logger.debug("Batch consume completed for normalization.")

        prompts = build_batch_job_normalization_prompt(
            raw_text_list=content,
            data_length=data_length
        )
        logger.debug("Normalization prompts generated.")

        job_docs = self.normalizer.batch_normalize(
            prompts=prompts,
            data_length=data_length
        )
        logger.info("Batch normalization completed.")

        outputs_name = batch_file_naming(job_docs)
        finalized_paths = self.paths.batch_finalized_file(
            names=outputs_name, 
            data_length=data_length
        )

        logger.debug("Final output paths resolved: %s", finalized_paths)

        self.saver.batch_save(docs=job_docs, paths=finalized_paths)
        logger.info("Finalized job documents saved successfully.")


    def process(self, file_name: str) -> None:
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

            split_path, length_data_split = self.split_file(
                file_name=file_name,
                read_path=raw_path
            )

            cleaned_path, _ = self.cleaned_file(
                file_name=file_name,
                read_path=split_path,
                data_length=length_data_split,
            )

            api_loader.start()
            logger.debug("LoadingStatus started.")

            self.normalize(
                read_path=cleaned_path,
                data_length=length_data_split
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