import random
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter


def Protestant_Set() -> set[int]:
    """ **Returns:** `set[chapter_index]` : {1-1189} """
    return set(range(1, BIBLE.TOTAL_CHAPTERS+1))

class BibleChapters:
    """ Iterates across one,default `set` {1-1189} """
    @property
    def total_marked(self): return sum(len(set) for set in self.marked.values())

    def __init__(self, translations:list):
        self.set = Protestant_Set()
        self.marked:dict[str,set] = {}
        for translation in translations:
            self.marked[translation] = set()

    def iterate(self) -> Generator[Chapter]:
        """
        **Yields:**
            Pops a random "chapter_index" {1-1189} from `set`, yielding corresponding `Chapter` without `translation`.
        """
        set = self.set.copy()
        while set.__len__() > 0:
            chapter_index:int = random_pop(set)
            yield BIBLE.Chapter(chapter_index)

    def iterate_marked(self) -> Generator[Chapter]:
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
        if translation not in self.marked.keys():
            raise Exception(f'translation/set was not instantiated in constructor. translation: {translation}')
        self.marked[translation].add(chap_index)

    def ratio(self) -> str:
        """ `{marked}/{total_chapters}` """
        marked = 0; total_chapters = 0
        for chapters in self.marked.values():
            marked += len(chapters)
            total_chapters += BIBLE.TOTAL_CHAPTERS
        return f'{marked}/{total_chapters}'

    def Save_Report(self, file_name:str='identify_poetry_form()', form:str='Poetry Form'):
        report = ""
        for translation,marked_chapters in self.marked.items():
            report += f'{translation} = {str(marked_chapters)}\n'
        report += f'{form}: {self.ratio()}'

        File(PYTHON_TESTS_DIRECTORY, file_name).save(report, encoding='UTF-8')
        Print.yellow(f'{form}: {self.ratio()}')

class BibleChapterSets(BibleChapters):
    def __init__(self, sets:dict[str,set]):
        """ initialize via: `dict[translation,chapters]` """
        self.sets = sets
        self.marked:dict[str,set] = {}
        for translation in sets.keys():
            self.marked[translation] = set()

    def From(translations:list[str]) -> BibleChapterSets:
        """static constructor"""
        return BibleChapterSets({translation:Protestant_Set() for translation in translations})

    def iterate(self) -> Generator[Chapter]:
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
