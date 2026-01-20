"""
"Standard Form" (#1) [see: ./models/biblegateway/#1-jeremiah-41-esv.txt]
    entire verse on one line
    5996/11890
    50.43%

"Poetry Form" (#2)   [see: ./models/biblegateway/#2-hosea-9-esv.txt]
    every verse made up of lines, ie: zero "Standard Form" verses


"Mixed Form" (#3)    [see: ./models/biblegateway/#3-genesis-49-esv.txt]
    

"Titled" Trait [see: ./models/biblegateway/psalms-42-net.txt]
    potential trait of #2-#3
    909/11890
    7.64%


Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences. NOTE: NRT is riddled with these.

Observations:
    - NKJV: DOES separate the second speaker in a verse into a separate line, see: ChapterPtr(BIBLE.SECOND_SAMUEL, 13, None, 'NKJV')

RESOLVED:
    11613/11890 Transformations: First verse in txts identified by "{book.chapter}" have all been standardized to "1", ie: "{verse}"
"""
import re
from definitions import BIBLE_TXT_NEW
from collections.abc import Callable
from kozubenko.os import File
from kozubenko.print import ANSI, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Book, ChapterPtr
from models.BibleChapters import BibleChapterSets


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

def chapter_file(PTR:ChapterPtr): return File(BIBLE_TXT_NEW, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:ChapterPtr): return File(BIBLE_TXT_NEW, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def debug_chapter(translation:str, book:Book, chapter:int, identifying_func:Callable):
    ptr = ChapterPtr(book, chapter, None, translation)
    identifying_func(ptr, chapter_text(ptr))

def visual_test(iterator:Callable, files_per_iteration=50):
    """ **iterator:** `Chapters.iterate()` || `Chapters.iterate_marked()` """
    iteration = 1
    for PTR in iterator():
        Subprocess.Notepad(chapter_file(PTR))
        iteration += 1
        if iteration == files_per_iteration:
            colored_input(f'Press Enter to open another {files_per_iteration} chapters in Notepad++...', ANSI.YELLOW)
            iteration = 1


def strip_title(PTR:ChapterPtr, text:str) -> tuple[str, str]:
    """
    Assumes: `is_titled(text) -> True`
    
    **Returns:** `(title, rest)`
    """
    start_index = text.find(f'{PTR.chapter} ')
    if start_index != -1:
        return (text[0:start_index], text[start_index:] )
    
    start_index = text.find('1 ')
    if start_index != -1:
        return (text[0:start_index], text[start_index:])

    raise Exception('strip_title(): is_titled(text) -> False. Illegal runtime path.')

def is_titled(PTR:ChapterPtr, text:str) -> bool:
    start_index_1 = text.find(f'{PTR.chapter} ')
    start_index_2 = text.find(f'1 ')

    if start_index_1 == 0 or start_index_2 == 0:
        return False
    return True

def is_standard_form(PTR:ChapterPtr, text:str) -> bool:
    expected_total_verses = PTR.book.total_verses(PTR.chapter)
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def is_poetry_form(PTR:ChapterPtr, text:str) -> bool:
    """poetry_form (#2)"""
    

def is_numbered_wrong(PTR:ChapterPtr, text:str) -> bool:
    start_index = text.find(f'1 ')
    if start_index == 0: return True
    return False









""" 
Archived
"""
def standardize_chapter_number_formatting():
    """
    **From:**  `f'1 '`  
    **To:** `f'{PTR.chapter} '`
    """
    i = 1
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        TEXT = chapter_text(PTR)
        text = TEXT

        if is_titled(PTR, text): (title, text) = strip_title(PTR, text)
        else: title = ""
        
        start_index = text.find(f'{PTR.chapter} ')
        if start_index == 0:
            text = "1" + text[len(str(PTR.chapter)):]

            chapter_file(PTR).save(f'{title}{text}', encoding='UTF-8')
            Chapters.mark(PTR.translation, PTR.index)
            
    Print.yellow(Chapters.total_marked)
    Chapters.Save_Report('identify_chapters_standardized()', "Standardized Chapters")