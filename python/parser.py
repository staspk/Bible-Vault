
"""
Observation #1:
    The "Standard Form" has been identified, i.e: #3 (see: ./models/biblegateway/jeremiah-41-esv.txt)
        5996 chapters / 11890 total
        50.43%


Observations:
    All chapters have

"""
import re, random, subprocess
from typing import Generator
from definitions import BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY
from kozubenko.cls import instance_attributes
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE, Book, ChapterPtr, Iterate_Bible_Chapters


class BibleChapters:
    def __init__(self, *translations):
        self.set = set(range(1, 1190))
        for translation in translations:
            self.__dict__[translation] = set()

    def ratio(self) -> str:
        """ `{marked}/{total_chapters}` """
        marked = 0; total_chapters = 0
        for attr in instance_attributes(self, ['set']):
            marked_chapters_for_translation:set[int] = attr.value
            marked += len(marked_chapters_for_translation)
            total_chapters += 1189   # total_chapters <- standard protestant bible
        return f'{marked}/{total_chapters}'
    
    def next_random(self) -> Generator[ChapterPtr]:
        """
        **Returns:**
            A random chapter_index that has not been selected yet (1 - 1189).

        **How to Use:**
        ```python
        for PTR in BibleChapters().next_random():
        ```
        """
        while self.set.__len__() > 0:
            chapter:int = random.choice(tuple(self.set))
            self.set.remove(chapter)
            yield BIBLE.ChaptersMap(chapter)

    def mark(self, translation:str, chap_index:int):
        if translation not in self.__dict__:
            raise Exception(f'set must be instantiated in constructor. translation: {translation}')
        self.__dict__[translation].add(chap_index)

    
def identify_psalm_form():
    translations = ['KJV', 'NASB', 'RSV', 'NKJV', 'NRSV']

    Bible = BibleChapters()
    for PTR in Bible.next_random():
        if PTR.book.name == BIBLE.PSALMS.name:
            continue
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                left = text.split(str(PTR.chapter), 1)[0]
                if(left):
                    Print.yellow(f'{PTR.book} {PTR.chapter} [{translation}]')

def identify_standard_form(translations):
    """standard_form (#3)"""
    Bible = BibleChapters(*translations)
    for PTR in Bible.next_random():
        expected_total_verses = PTR.book.total_verses(PTR.chapter)
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions
                if lines.__len__() == expected_total_verses:
                    Bible.mark(translation, PTR.index)

    report = ""
    for attr in instance_attributes(Bible, ['set']):
        translation:str = attr.key
        marked_chapters:set[int] = attr.value
        report += f'{translation} = {str(marked_chapters)}\n'
    report += f'Standard Form: {Bible.ratio()}'

    File(PYTHON_TESTS_DIRECTORY, 'identify_standard_form()').save(report, encoding='UTF-8')
    Print.green(f'Standard Form: {Bible.ratio()}')

def identify_chapter(translation:str, book:Book, chapter:int):
    """standard_form (#3)"""
    file = File(BIBLE_TXT_NEW, translation, book.name, f'{chapter}.txt')
    text = file.contents(encoding='UTF-8')

    lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions

    EXPECTED_TOTAL_VERSES = book.total_verses(chapter)
    if lines.__len__() == EXPECTED_TOTAL_VERSES: Print.green(f'{translation}:{book}{chapter} standard_form')
    else:                                        Print.red(f'{translation}:{book}{chapter} NOT standard_form')
