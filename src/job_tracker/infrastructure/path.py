from pathlib import Path

from typing import List

class PathResolver:
    """Centralized utility for resolving application file paths.

    Manages directory structure for raw, scraped, split, cleaned, and
    finalized data. Provides consistent path generation for individual
    files and ensures required directories are created on demand.

    Attributes:
        base_path (Path): Root directory for all application-generated files.
        data_path (Path): Subdirectory ``<base_path>/data``.
        raw_dir (Path): Directory for raw input files.
        scrap_dir (Path): Directory for scraped files.
        split_dir (Path): Directory for split files.
        clean_dir (Path): Directory for cleaned files.
        finalized_dir (Path): Directory for finalized output files.

    Example:
        >>> resolver = PathResolver(Path("/app"))
        >>> resolver.raw_file("document")
        PosixPath('/app/data/raw/document.txt')
    """
    def __init__(self, base_path: Path)->None:
        """Initialize PathResolver and define all managed subdirectories.

        Note:
            Directories are **not** created at initialization time; they are
            created lazily when a path-resolution method is first called.

        Args:
            base_path (Path): Root directory under which all data
                subdirectories will be created.

        Example:
            >>> resolver = PathResolver(Path("/app"))
            >>> resolver.data_path
            PosixPath('/app/data')
        """
        # Base directory for all application-generated files
        self.base_path = base_path
        self.data_path = base_path / "data"

        # Define raw and processed data directories
        self.raw_dir = self.data_path / "raw"
        self.scrap_dir = self.data_path / "scraped"
        self.split_dir = self.data_path / "splited"
        self.clean_dir = self.data_path / "cleaned"
        self.finalized_dir = self.data_path / "finalized"

    def _ensure_directories(self, path: Path) -> None:
        """Create a directory and all missing parents if they do not exist.

        This is a thin wrapper around :pymeth:`pathlib.Path.mkdir` with
        ``parents=True`` and ``exist_ok=True`` so callers do not need to
        handle ``FileExistsError``.

        Args:
            path (Path): Target directory to create.

        Example:
            >>> resolver._ensure_directories(Path("/tmp/new/nested/dir"))
            # /tmp/new/nested/dir is created if it did not exist
        """
        path.mkdir(parents=True, exist_ok=True)

    def finalized_directory(self) -> Path:
        """Return the finalized output directory, creating it if necessary.

        Returns:
            Path: Absolute path to ``<base_path>/data/finalized``.

        Example:
            >>> resolver.finalized_directory()
            PosixPath('/app/data/finalized')
        """
        self._ensure_directories(path=self.finalized_dir)
        return self.finalized_dir

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the full path for a single raw input file.

        Creates the raw directory if it does not already exist, then
        constructs a :class:`~pathlib.Path` by joining the directory with
        ``<name><suffix>``.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Full path to the raw file at
                ``<base_path>/data/raw/<name><suffix>``.

        Raises:
            ValueError: If ``name`` is an empty string.

        Example:
            >>> resolver.raw_file("document")
            PosixPath('/app/data/raw/document.txt')
            >>> resolver.raw_file("archive", suffix=".csv")
            PosixPath('/app/data/raw/archive.csv')
        """
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.raw_dir)
        
        raw_path = self.raw_dir / f"{name}{suffix}"
        
        return raw_path
    
    def scrap_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the full path for a single scraped file.

        Creates the scraped directory if it does not already exist, then
        constructs the target :class:`~pathlib.Path`.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Full path to the scraped file at
                ``<base_path>/data/scraped/<name><suffix>``.

        Raises:
            ValueError: If ``name`` is an empty string.

        Example:
            >>> resolver.scrap_file("page_01")
            PosixPath('/app/data/scraped/page_01.txt')
        """
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.scrap_dir)
        
        scrap_path = self.scrap_dir / f"{name}{suffix}"
        
        return scrap_path
    
    def split_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the full path for a single split file.

        Creates the split directory if it does not already exist, then
        constructs the target :class:`~pathlib.Path`.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Full path to the split file at
                ``<base_path>/data/splited/<name><suffix>``.

        Raises:
            ValueError: If ``name`` is an empty string.

        Example:
            >>> resolver.split_file("chunk_01")
            PosixPath('/app/data/splited/chunk_01.txt')
        """
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.split_dir )
        
        split_path = self.split_dir / f"{name}{suffix}"
        
        return split_path
    
    def clean_file(self, name: str, suffix: str = ".txt") -> Path:
        """Resolve the full path for a single cleaned file.

        Creates the cleaned directory if it does not already exist, then
        constructs the target :class:`~pathlib.Path`.

        Args:
            name (str): File stem (i.e. filename without extension).
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".txt"``.

        Returns:
            Path: Full path to the cleaned file at
                ``<base_path>/data/cleaned/<name><suffix>``.

        Raises:
            ValueError: If ``name`` is an empty string.

        Example:
            >>> resolver.clean_file("document_clean")
            PosixPath('/app/data/cleaned/document_clean.txt')
        """
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.clean_dir)
        
        clean_path = self.clean_dir / f"{name}{suffix}"
        
        return clean_path
    
    def finalized_file(
        self, 
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    ) -> Path:
        """Resolve the full path for a finalized output file.

        Constructs a nested path under the finalized directory using
        ``input_fname`` as an intermediate subdirectory, which keeps outputs
        grouped by their source input file.

        Args:
            name (str): File stem of the finalized file.
            input_fname (str): Name of the originating input file, used as a
                grouping subdirectory under ``finalized_dir``.
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".json"``.

        Returns:
            Path: Full path at
                ``<base_path>/data/finalized/<input_fname>/<name><suffix>``.

        Example:
            >>> resolver.finalized_file("result", "document")
            PosixPath('/app/data/finalized/document/result.json')
        """
        self._ensure_directories(path=self.finalized_dir)

        finalized_path = self.finalized_dir / input_fname / f"{name}{suffix}"

        return finalized_path
    
    def temp_finalized_file(
        self,
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    ) -> Path:
        """Resolve the full path for a temporary finalized file.

        Identical in structure to :pymeth:`finalized_file` but intended for
        intermediate or in-progress outputs that may be promoted or discarded
        before the pipeline completes.

        Args:
            name (str): File stem of the temporary finalized file.
            input_fname (str): Name of the originating input file, used as a
                grouping subdirectory under ``finalized_dir``.
            suffix (str, optional): File extension including the leading dot.
                Defaults to ``".json"``.

        Returns:
            Path: Full path at
                ``<base_path>/data/finalized/<input_fname>/<name><suffix>``.

        Example:
            >>> resolver.temp_finalized_file("result_tmp", "document")
            PosixPath('/app/data/finalized/document/result_tmp.json')
        """
        self._ensure_directories(path=self.finalized_dir)

        temp_finalized_path = self.finalized_dir / input_fname / f"{name}{suffix}"

        return temp_finalized_path