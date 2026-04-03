from pathlib import Path
from typing import List, Protocol

class PathResolver(Protocol):
    """Contract for resolving filesystem paths used across the application.

    Defines how different file categories (raw input, scraped, split,
    cleaned, finalized, and temporary finalized output) should be resolved
    into concrete :class:`~pathlib.Path` objects.

    Implementations are responsible for handling directory structure,
    filename normalization, and path safety.

    Example:
        >>> class MyResolver:
        ...     def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        ...         return Path("/data/raw") / f"{name}{suffix}"
        >>> resolver: PathResolver = MyResolver()
    """
    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the path for a raw input file.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Resolved path to the raw file.

        Example:
            >>> resolver.raw_file("document")
            PosixPath('/data/raw/document.txt')
        """
        ...
    
    def scrap_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the path for a scraped file.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Resolved path to the scraped file.

        Example:
            >>> resolver.scrap_file("page_01")
            PosixPath('/data/scraped/page_01.txt')
        """
        ...
    
    def split_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the path for a split file.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Resolved path to the split file.

        Example:
            >>> resolver.split_file("chunk_01")
            PosixPath('/data/splited/chunk_01.txt')
        """
        ...
    
    def clean_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the path for a cleaned file.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Resolved path to the cleaned file.

        Example:
            >>> resolver.clean_file("document_clean")
            PosixPath('/data/cleaned/document_clean.txt')
        """
        ...
    
    def finalized_file(
        self, 
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        """Resolve the path for a finalized output file.

        Args:
            name (str): File stem of the finalized file.
            input_fname (str): Name of the originating input file, used as a
                grouping subdirectory within the finalized directory.
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".json"``.

        Returns:
            Path: Resolved path to the finalized file.

        Example:
            >>> resolver.finalized_file("result", "document")
            PosixPath('/data/finalized/document/result.json')
        """
        ...
    
    def temp_finalized_file(
        self,
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        """Resolve the path for a temporary finalized file.

        Intended for intermediate or in-progress outputs that may be
        promoted or discarded before the pipeline completes.

        Args:
            name (str): File stem of the temporary finalized file.
            input_fname (str): Name of the originating input file, used as a
                grouping subdirectory within the finalized directory.
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".json"``.

        Returns:
            Path: Resolved path to the temporary finalized file.

        Example:
            >>> resolver.temp_finalized_file("result_tmp", "document")
            PosixPath('/data/finalized/document/result_tmp.json')
        """
        ...