import logging

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from job_tracker.core import batch_strip_html, LLMClient
from job_tracker.infrastructure import LoadingStatus, batch_file_namming
from job_tracker.schemas import JobDocumentSchema
from job_tracker.prompts import build_batch_job_normalization_prompt


logger = logging.getLogger(__name__)

class EditorLauncher(ABC):

    @abstractmethod
    def open(
        self, 
        path: Path, 
        editor: Optional[str] = None
    ) -> None:
        ...


class FileHandler(ABC):

    @abstractmethod
    def write(
        self,
        path: Path,
        content: Optional[str],
        overwrite: bool,
    ) -> None:
        ...
        
    @abstractmethod
    def write_batch(
        self,
        paths: List[Path],
        contents: List[str],
    )->None:
        ...

    @abstractmethod
    def consume(self, path: Path)->str:
        ...
        
    @abstractmethod
    def batch_consume(self, paths:List[Path])->List[str]:
        ...


class FileSplitter:

    @abstractmethod 
    def split(self, data:str)->tuple:
        ...
    

class JobDocumentSaver(ABC):

    @abstractmethod
    def batch_save(
        self, 
        docs: List[JobDocumentSchema], 
        paths: List[Path],
    )-> None:
        ...


class PathResolver(ABC):

    @abstractmethod
    def raw_file(
        self, 
        name: str, 
        suffix: str,
    ) -> Path:
        ...
    
    @abstractmethod
    def batch_cleaned_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        ...
    
    @abstractmethod
    def split_path(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        ...
    
    @abstractmethod
    def batch_finalized_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        ...

class JobNormalizer(ABC):

    @abstractmethod
    def batch_normalize(self, prompts:List[str])->List[JobDocumentSchema]:
        ...


class GeminiJobNormalizer(JobNormalizer):
    def __init__(self, client: LLMClient):
        self.client = client

    def normalize(self, prompt: str) -> JobDocumentSchema:
        ...



import logging
from typing import List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class JobPipelineService:
    def __init__(
        self,
        editor: EditorLauncher,
        file_handler: FileHandler,
        file_splitter: FileSplitter,
        paths: PathResolver,
        saver: JobDocumentSaver,
        normalizer: JobNormalizer,
    ) -> None:
        self.editor = editor
        self.file_handler = file_handler
        self.file_splitter = file_splitter
        self.paths = paths
        self.saver = saver
        self.normalizer = normalizer

        logger.debug("JobPipelineService initialized with dependencies.")


    def initiate_file(self, file_name: str) -> Path:
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


    def normalize(self, read_path: List[Path], data_length: int) -> None:
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

        outputs_name = batch_file_namming(job_docs)
        finalized_paths = self.paths.batch_finalized_file(
            names=outputs_name, 
            data_length=data_length
        )

        logger.debug("Final output paths resolved: %s", finalized_paths)

        self.saver.batch_save(docs=job_docs, paths=finalized_paths)
        logger.info("Finalized job documents saved successfully.")


    def process(self, file_name: str) -> None:
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