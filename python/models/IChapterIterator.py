from abc import ABC, abstractmethod
from typing import Iterator
from models.Bible import Chapter


class IChapterIterator(ABC):

    @abstractmethod
    def iterate(self) -> Iterator[Chapter]: pass

    @abstractmethod
    def iterate_marked(self) -> Iterator[Chapter]: pass