from pathlib import Path
from typing import List, Protocol

class PathResolver(Protocol):
    """
    Contract for resolving filesystem paths used across the application.

    This protocol defines how different file categories (raw input,
    finalized output, and LLM-generated output) should be resolved
    into concrete `Path` objects.

    Implementations are responsible for handling directory structure,
    filename normalization, and path safety.
    """
    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        ...
    
    def scrap_file(self, name: str, suffix: str = ".txt") -> Path:
        ...
    
    def split_file(self, name: str, suffix: str = ".txt") -> Path:
        ...
    
    def clean_file(self, name: str, suffix: str = ".txt") -> Path:
        ...
    
    def finalized_file(
        self, 
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        ...
    
    def temp_finalized_file(
        self,
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        ...