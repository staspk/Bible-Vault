
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

    Many texts start with "1" instead of f"{chapter}". Decision needs to be made how to standardize.

Observations:
    - NKJV: DOES separate the second speaker in a verse into a separate line, see: ChapterPtr(BIBLE.SECOND_SAMUEL, 13, None, 'NKJV')
"""
from collections.abc import Callable
import re
from definitions import BIBLE_TXT_NEW
from kozubenko.os import File
from models.Bible import BIBLE, Book, ChapterPtr


def file(PTR:ChapterPtr): return File(BIBLE_TXT_NEW, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def text(PTR:ChapterPtr): return File(BIBLE_TXT_NEW, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def strip_title(text:str) -> str:
    """ **Returns:** `text` as is, if not `is_titled(text)` """
    if not is_titled(text):
        return text
    

    
def is_standard_form(PTR:ChapterPtr, text:str) -> bool:
    expected_total_verses = PTR.book.total_verses(PTR.chapter)
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def is_poetry_form(PTR:ChapterPtr, text:str) -> bool:
    """poetry_form (#2)"""

    pass

def is_titled(PTR:ChapterPtr, text:str) -> bool:
    start_index_1 = text.find(f'{PTR.chapter} ')
    start_index_2 = text.find(f'1 ')

    if start_index_1 == 0 or start_index_2 == 0:
        return False
    return True

def debug_chapter(translation:str, book:Book, chapter:int, identifying_func:Callable):
    ptr = ChapterPtr(book, chapter, None, translation)
    identifying_func(ptr, text(ptr))


def is_numbered_wrong(PTR:ChapterPtr, text:str) -> bool:
    start_index = text.find(f'1 ')

    if start_index == 0:
        return True
    return False

# def standardize_txts():
