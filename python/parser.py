
"""
"Standard Form" (#1) [see: ./models/biblegateway/#1-jeremiah-41-esv.txt]
    entire verse on one line
    5996/11890
    50.43%

"Poetry Form" (#2)   [see: ./models/biblegateway/#2-hosea-9-esv.txt]
    every verse made up of lines


"Mixed Form" (#3)    [see: ./models/biblegateway/#3-genesis-49-esv.txt]
    

"Titled Trait"  [see: ./models/biblegateway/psalms-42-net.txt]
    potential trait of #2-#3
    700/11890
    5.88%


Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences. NOTE: NRT is riddled with these

    Many texts start with "1" instead of f"{chapter}". Decision needs to be made how to standardize.
"""
import re
from collections.abc import Callable
from definitions import BIBLE_TXT_NEW
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE, ChapterPtr
from models.BibleChapters import BibleChapters
from models.text_forms.standard import StandardForm


def text(PTR:ChapterPtr): return File(BIBLE_TXT_NEW, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def identify_standard_form(translations:list) -> BibleChapters:
    """standard_form (#1). Operation: ~3mins"""
    Chapters = BibleChapters(translations)
    for PTR in Chapters.iterate():
        expected_total_verses = PTR.book.total_verses(PTR.chapter)
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions
                if lines.__len__() == expected_total_verses:
                    Chapters.mark(translation, PTR.index)
    return Chapters

# def is_standard_form(PTR:ChapterPtr, text:str) -> bool:
#     text =

def is_poetry_form(PTR:ChapterPtr, text:str) -> bool:
    """poetry_form (#2)"""
    pass

def is_titled(PTR:ChapterPtr, text:str) -> bool:
    array = text.split(f'{PTR.chapter} ')

    if len(array) == 1: return False
    if array[0].splitlines().__len__() > 0: return True
    return False
