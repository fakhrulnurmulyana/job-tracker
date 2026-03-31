import logging

from typing import Protocol, List

logger = logging.getLogger(__name__)


class LinkSplitter(Protocol): 
    def split(
        self, 
        links:str
    )->List[str]:
        ...