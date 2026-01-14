import random
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from models.Bible import BIBLE, ChapterPtr


def Protestant_Set() -> set[int]:
    """ **Returns:** `set[chapter_index]` : {1-1189} """
    return set(range(1, BIBLE.TOTAL_CHAPTERS+1))

class BibleChapters:
    """ Iterates across one,default `set` {1-1189} """
    def __init__(self, translations:list):
        self.set = Protestant_Set()
        self.marked:dict[str,set] = {}
        for translation in translations:
            self.marked[translation] = set()

    def iterate(self) -> Generator[ChapterPtr]:
        """
        **Yields:**
            Pops a random "chapter_index" (1-1189) from `set`.

        **How to Use:**
        ```python
        for PTR in BibleChapters().iterate_Bible():
        ```
        """
        while self.set.__len__() > 0:
            chapter_index = random_pop(self.set)
            yield BIBLE.ChaptersMap(chapter_index)

    def next_marked(self) -> Generator[File]:
        TRANSLATIONS = list(self.marked.keys())
        marked = { translation:chapters.copy for translation,chapters in self.marked.items() }
        total = sum(len(set) for set in marked)
        while total > 0:
            translation = random.choice(TRANSLATIONS)
            set = self.marked[translation]
            chapter_index = random_pop(set)
            PTR = BIBLE.ChaptersMap(chapter_index)
            yield File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')

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

    def Save_Report(self):
        report = ""
        for translation,marked_chapters in self.marked:
            report += f'{translation} = {str(marked_chapters)}\n'
        report += f'Standard Form: {self.ratio()}'

        File(PYTHON_TESTS_DIRECTORY, 'identify_standard_form()').save(report, encoding='UTF-8')
        Print.yellow(f'Standard Form: {self.ratio()}')

class BibleChapters(BibleChapters):
    def __init__(self, sets:dict[str,set]):
        """ initialize via: `dict[translation,chapters]` """
        self.sets = sets
        self.marked:dict[str,set] = {}
        for translation in sets.keys():
            self.marked[translation] = set()

    def iterate(self) -> Generator[ChapterPtr]:
        """
        **Yields:**
            Pops a random "chapter_index" from `sets`.
        """
        sets = {key:value.copy() for key,value in self.sets.items() if len(value) > 0}
        left = sum(len(set) for set in sets.values())

        while left > 0:
            key = random.choice(tuple(sets.keys()))
            chapter_index = random_pop(sets[key])
            yield chapter_index

            left -= 1
            if sets[key].__len__() == 0:
                del sets[key]
