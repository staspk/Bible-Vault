import random
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from models.Bible import BIBLE, ChapterPtr


def Protestant_Set() -> set[int]:
    """ **Returns:** `set[chapter_index]` : {1-1189} """
    return set(range(1, BibleChapters.TOTAL_CHAPTERS+1))

class BibleChapters:
    TOTAL_CHAPTERS = 1189  # aka: Protestant
    
    def __init__(self, translations:list):
        self.set = set(range(1, self.TOTAL_CHAPTERS+1))
        self.marked:dict[str,set] = {}
        for translation in translations:
            self.marked[translation] = set()

    def iterate_Bible(self) -> Generator[ChapterPtr]:
        """
        **Returns:**
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
            total_chapters += self.TOTAL_CHAPTERS
        return f'{marked}/{total_chapters}'

    def Save_Report(self):
        report = ""
        for translation,marked_chapters in self.marked:
            report += f'{translation} = {str(marked_chapters)}\n'
        report += f'Standard Form: {self.ratio()}'

        File(PYTHON_TESTS_DIRECTORY, 'identify_standard_form()').save(report, encoding='UTF-8')
        Print.yellow(f'Standard Form: {self.ratio()}')
