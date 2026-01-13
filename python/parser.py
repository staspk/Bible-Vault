
"""
Observation #1:
    The "Standard Form" has been identified: #3 (see: ./models/biblegateway/jeremiah-41-esv.txt)
        5996 chapters / 11890 total
        50.43%



"""
import re, random, subprocess
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.os import File
from kozubenko.print import Print
from kozubenko.random import next_random_pop, random_pop
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Book, ChapterPtr, Iterate_Bible_Chapters


class BibleChapters:
    TOTAL_CHAPTERS = 1189  # aka: Protestant
    
    def __init__(self, translations:list):
        self.set = set(range(1, self.TOTAL_CHAPTERS+1))
        self.marked:dict[str,set] = {}
        for translation in translations:
            self.marked[translation] = set()

    def ratio(self) -> str:
        """ `{marked}/{total_chapters}` """
        marked = 0; total_chapters = 0
        for chapters in self.marked.values():
            marked += len(chapters)
            total_chapters += self.TOTAL_CHAPTERS
        return f'{marked}/{total_chapters}'
    
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
    """standard_form (#3)"""
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


def identify_chapter(translation:str, book:Book, chapter:int):
    """standard_form (#3)"""
    file = File(BIBLE_TXT_NEW, translation, book.name, f'{chapter}.txt')
    text = file.contents(encoding='UTF-8')

    lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions

    EXPECTED_TOTAL_VERSES = book.total_verses(chapter)
    if lines.__len__() == EXPECTED_TOTAL_VERSES: Print.green(f'{translation}:{book}{chapter} standard_form')
    else:                                        Print.red(f'{translation}:{book}{chapter} NOT standard_form')

