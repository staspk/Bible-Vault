
"""
"Standard Form" (#3) [see: ./models/biblegateway/jeremiah-41-esv.txt]
    5996 chapters / 11890 total
    50.43%

"Poetry Form" (#2) [see: ./models/biblegateway/hosea-9-esv.txt]



Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences

"""
import re, random
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, ChapterPtr


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


def identify_psalm_form():
    translations = ['KJV', 'NASB', 'RSV', 'NKJV', 'NRSV']

    Bible = BibleChapters()
    for PTR in Bible.iterate_Bible():
        if PTR.book.name == BIBLE.PSALMS.name:
            continue
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                left = text.split(str(PTR.chapter), 1)[0]
                if(left):
                    Print.yellow(f'{PTR.book} {PTR.chapter} [{translation}]')

def identify_standard_form(translations:list) -> BibleChapters:
    """standard_form (#3). Operation: ~3mins"""
    Chapters = BibleChapters(translations)
    for PTR in Chapters.iterate_Bible():
        expected_total_verses = PTR.book.total_verses(PTR.chapter)
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions
                if lines.__len__() == expected_total_verses:
                    Chapters.mark(translation, PTR.index)
    return Chapters

def identify_poetry_form(translations:list) -> BibleChapters:
    """poetry_form (#2)"""
    StandardChapters = identify_standard_form(translations)





