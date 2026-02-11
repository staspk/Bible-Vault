from typing import Iterator
from kozubenko.cls import class_attributes
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets, Protestant_Set


translation = str
chapter_index = int
BibleChapterSet = dict[translation, set[chapter_index]]

def Protestant_Set() -> set[int]: return set(range(1, BIBLE.TOTAL_CHAPTERS+1))

class IBibleChapterSet:
    """
    Classes subclassing are a dict container of `translation`->`set[chapter_index]`
    
    Used to load a set back in between runs. See example: `./python/models/bible_chapter_sets/missing_chapters.py`
    """

    @classmethod
    def chapters(cls) -> dict[translation, set[chapter_index]]:
        chapter_set:dict[translation, set[chapter_index]] = {}
        for key,value in class_attributes(cls):
            if isinstance(value, set):
                chapter_set[key] = value
        return chapter_set

    @classmethod
    def Chapters(cls) -> BibleChapterSets:
        return BibleChapterSets(cls.chapters())
    
    @classmethod
    def Inverse(cls) -> BibleChapterSets:
        """
        **Returns:** `cls.chapters()`, but each set is subtracted from a "full set", i.e: `Protestant_Set()`
        """
        chapter_set = cls.chapters()
        inverse = {}
        for translation in chapter_set.keys():
            inverse[translation] = Protestant_Set() - chapter_set[translation]
            
        return BibleChapterSets(inverse)
    
    @classmethod
    def iterate(cls) -> Iterator[tuple[Chapter, list[translation]]]:
        """
        **Intended:** To yield a form easily consumable by the parser.

        Technically, this may not belong here, being more in the spirit of `BibleChapterSets`
        """
        chapters:dict[chapter_index, list[translation]] = {}

        for translation,set in cls.chapters().items():
            while set.__len__() > 0:
                chapter_index = set.pop()
                if chapter_index in chapters: chapters[chapter_index].append(translation)
                else:                         chapters[chapter_index] = [translation]
        
        for chapter_index,translations in chapters.items():
            yield (Chapter.From(chapter_index), translations)
