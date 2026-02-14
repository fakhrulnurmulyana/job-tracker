from abc import abstractmethod

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