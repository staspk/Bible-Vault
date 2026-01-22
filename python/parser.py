"""
"Standard Form" (#1) [see: ./models/biblegateway/#1-jeremiah-41-esv.txt]
    entire verse on one line
    6006/11890
    50.51%

"Poetry Form" (#2)   [see: ./models/biblegateway/#2-hosea-9-esv.txt]
    every verse made up of lines, ie: zero "Standard Form" verses


"Mixed Form" (#3)    [see: ./models/biblegateway/#3-genesis-49-esv.txt]
    

"Titled" Trait [see: ./models/biblegateway/psalms-42-net.txt]
    potential trait of #2-#3
    909/11890
    7.64%


Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences. NOTE: NRT is riddled with these.
    Joshua 12 - iffy formatting: "one"
    Chapter(BIBLE.JOHN, 5) -> only 3 verses were parsed for several translations...perhaps many more chapters are corrupted.

Observations:
    - NKJV: DOES separate the second speaker in a verse into a separate line, see: Chapter(BIBLE.SECOND_SAMUEL, 13, None, 'NKJV')

RESOLVED:
    11613/11890 Transformations: First verse in txts identified by "{book.chapter}" have all been standardized to "1", ie: "{verse}"
"""
import re
import time
from typing import Iterator
from definitions import BIBLE_TXT_NEW, BIBLE_TXT_PARTIAL
from collections.abc import Callable
from kozubenko.os import File
from kozubenko.print import ANSI, Print, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Book, Chapter
from models.BibleChapters import BibleChapterSets


DIRECTORY = BIBLE_TXT_NEW # BIBLE_TXT_PARTIAL
ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

def chapter_File(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def debug_chapter(translation:str, book:Book, chapter:int, identifying_func:Callable):
    ptr = Chapter(book, chapter, None, translation)
    identifying_func(ptr, chapter_text(ptr))

def visual_test(iterator:Callable[[], Iterator[Chapter]], files_per_iteration=50):
    """ **iterator:** `Chapters.iterate()` || `Chapters.iterate_marked()` """
    iteration = 1
    for PTR in iterator():
        # Print.green(f'{PTR.__str__()} -> SHOULD HAVE: ', new_line=False)
        # Print.red(PTR.book.total_verses(PTR.chapter))
        Subprocess.Notepad(chapter_File(PTR))
        time.sleep(.02)
        iteration += 1
        if iteration == files_per_iteration:
            colored_input(f'Press Enter to open another {files_per_iteration} chapters in Notepad++...', ANSI.YELLOW)
            iteration = 1


def strip_title(text:str) -> tuple[str, str]:
    """
    If no title in text: `title == ""`

    **Returns:** `(title, rest)`
    """
    start_index = text.find('1 ')
    if start_index == 0:   return ("", text)
    elif start_index != 0: return (text[0:start_index], text[start_index:])

    raise Exception('strip_title(): unexpected runtime path')

def is_standard_form(PTR:Chapter) -> bool:
    text = chapter_text(PTR)
    expected_total_verses = PTR.book.total_verses(PTR.chapter)
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def is_poetry_form(PTR:Chapter) -> bool:
    """poetry_form (#2)"""
    TOTAL_VERSES = PTR.book.total_verses(PTR.chapter)

    (title, text) = strip_title(chapter_text(PTR))
    HAS_TITLE = title != ""

    if HAS_TITLE:
        for verse in range(1, TOTAL_VERSES+1):
            start_index = text.find(f'\n{verse} \n')
            if start_index == -1:
                return False
        return True
    else:
        return False

def has_standard_line(PTR:Chapter) -> bool:
    TOTAL_VERSES = PTR.book.total_verses(PTR.chapter)
    (title, text) = strip_title(chapter_text(PTR))

    lines = re.findall(r'.+', text)

    lines = text.splitlines()
    verse = 1
    for line in lines:
        pass

def has_missing_verses(PTR:Chapter) -> bool:
    text = chapter_text(PTR)
    start = 0; END = text.__len__()

    TOTAL_VERSES = PTR.book.total_verses(PTR.chapter)
    for verse in range(1, TOTAL_VERSES+1):
        start = text[start:END].find(f'{verse} ')
        if start == -1:
            return True

    return False






""" 
Archived
"""
def standardize_chapter_number_formatting() -> BibleChapterSets:
    """
    **From:** `"{PTR.chapter} "`
    **To:** `"1 "`

    NOTE: strip_title() assumptions have CHANGED since using this function !!!
    """
    i = 1
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        TEXT = chapter_text(PTR)
        text = TEXT

        (title, text) = strip_title(PTR, text)
        
        start_index = text.find(f'{PTR.chapter} ')
        if start_index == 0:
            text = "1" + text[len(str(PTR.chapter)):]

            chapter_File(PTR).save(f'{title}{text}', encoding='UTF-8')
            Chapters.mark(PTR.translation, PTR.index)
            
    Print.yellow(Chapters.total_marked)
    Chapters.Save_Report('identify_chapters_standardized()', "Standardized Chapters")
    return Chapters