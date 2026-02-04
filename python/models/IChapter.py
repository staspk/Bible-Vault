from dataclasses import dataclass
from models.Bible import Book


@dataclass(frozen=True)
class IChapter:
    translation:str
    book:Book
    chapter:int
