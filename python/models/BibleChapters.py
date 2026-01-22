import random
from typing import Iterator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter


def Protestant_Set() -> set[int]:
    """ **Returns:** `set[chapter_index]` : {1-1189} """
    return set(range(1, BIBLE.TOTAL_CHAPTERS+1))

class BibleChapters():
    """ Iterates across one,default `set[chapter_index:int]` {1-1189}"""
    @property
    def total_marked(self) -> int: return sum(len(set) for set in self.marked.values())

    def __init__(self):
        self.set = Protestant_Set()
        self.marked:dict[str,set[int]] = {}

    def iterate(self) -> Iterator[Chapter]:
        """
        **Yields:**
            Pops a random "chapter_index" {1-1189} from `set`, yielding corresponding `Chapter` without `translation`.
        """
        set = self.set.copy()
        while set.__len__() > 0:
            chapter_index:int = random_pop(set)
            yield BIBLE.Chapter(chapter_index)

    def iterate_marked(self) -> Iterator[Chapter]:
        marked = {key:value.copy() for key,value in self.marked.items() if len(value) > 0}
        left = sum(len(set) for set in marked.values())
        while left > 0:
            translation = random.choice(tuple(marked.keys()))
            chapter_index = random_pop(marked[translation])
            PTR:Chapter = BIBLE.Chapter(chapter_index)
            yield Chapter(PTR.book, PTR.chapter, PTR.index, translation)

            left -= 1
            if marked[translation].__len__() == 0:
                del marked[translation]

    def mark(self, translation:str, chap_index:int):
        if translation not in self.marked.keys(): self.marked[translation] = set([chap_index])
        else: self.marked[translation].add(chap_index)

    def ratio(self) -> str:
        """ `{marked}/{total_chapters}` """
        marked = 0; total_chapters = 0
        for chapters in self.marked.values():
            marked += len(chapters)
            total_chapters += BIBLE.TOTAL_CHAPTERS
        return f'{marked}/{total_chapters}'

    def Save_Report(self, test='Poetry Form'):
        report = ""
        for translation,marked_chapters in self.marked.items():
            report += f'{translation} = {str(marked_chapters)}\n'
        report += f'{test}: {self.ratio()}'

        File(PYTHON_TESTS_DIRECTORY, f'identify_{test.replace(" ", "_").lower()}').save(report, encoding='UTF-8')
        Print.yellow(f'{test}: {self.ratio()}')

class BibleChapterSets(BibleChapters):
    """
    `BibleChapterSets(sets)` -> Init with pre-existing `dict[translation,set[chapter_index:int]]`

    `BibleChapterSets.From(list[translation:str]]) -> Init a set {1-1189} for every `translation`
    """
    @property
    def total(self) -> int: return sum(len(set) for set in self.sets.values())
    
    def __init__(self, sets:dict[str,set]):
        """ initialize via: `dict[translation,set[chapter_index:int]]` """
        self.sets = sets
        self.marked:dict[str,set] = {}
        for translation in sets.keys():
            self.marked[translation] = set()

    def From(translations:list[str]) -> BibleChapterSets:
        """static constructor"""
        return BibleChapterSets({translation:Protestant_Set() for translation in translations})

    def iterate(self) -> Iterator[Chapter]:
        """
        **Yields:**
            Pops a random "chapter_index" from `sets`, yielding corresponding `Chapter` including `translation`.
        
        **How to Use:**
        ```python
        Chapters = BibleChapters(StandardForm.remaining_chapters())
        for PTR in Chapters.iterate():
        ```
        """
        sets = {key:value.copy() for key,value in self.sets.items() if len(value) > 0}
        left = sum(len(set) for set in sets.values())

        while left > 0:
            translation = random.choice(tuple(sets.keys()))
            chapter_index = random_pop(sets[translation])
            PTR:Chapter = BIBLE.Chapter(chapter_index)
            yield Chapter(PTR.book, PTR.chapter, PTR.index, translation)

            left -= 1
            if sets[translation].__len__() == 0:
                del sets[translation]

    def subtract(self, other:BibleChapterSets) -> BibleChapterSets:
        """ Assumes: no protection is needed against `other` having a value that `self` does not have """
        sets = {key:value.copy() for key,value in self.sets.items() if len(value) > 0}

        for translation,set in other.sets.items():
            sets[translation] = sets[translation] - set
        
        return BibleChapterSets(sets)