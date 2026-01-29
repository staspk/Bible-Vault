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

Certain translations skip certain verses. Pattern decided on (assume: verse 7):
7 [7]

Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences. NOTE: NRT is riddled with these.
    Joshua 12 - iffy formatting: "one"
    Chapter(BIBLE.JOHN, 5) -> only 3 verses were parsed for several translations...perhaps many more chapters are corrupted.
    TODO:
        - There are are strange space/tab after \n after certain chapters, NEED to see why they are caused, likely: TRANSFORM DATA

Observations:
    - NKJV: DOES separate the second speaker in a verse into a separate line, see: Chapter(BIBLE.SECOND_SAMUEL, 13, None, 'NKJV')

RESOLVED:
    11613/11890 Transformations: First verse in txts identified by "{book.chapter}" have all been standardized to "1", ie: "{verse}"
    TODO:
        Certain verses mix both the Standard/Lined format, increases parsing difficulty.
"""
import re, time
from typing import Iterator
from collections.abc import Callable
from kozubenko.os import File
from kozubenko.print import ANSI, Print, colored_input
from kozubenko.subprocess import Subprocess
from models.Bible import BIBLE, Book, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW, BIBLE_TXT_PARTIAL




DIRECTORY = BIBLE_TXT_NEW # BIBLE_TXT_PARTIAL
def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def iterate_verses(PTR:Chapter) -> Iterator[str]:
    TEXT = chapter_text(PTR); LENGTH = len(TEXT)
    verse = 1
    start = TEXT.find(f"{verse} ")
    end   = TEXT.find(f"{verse+1} ")
    while end != -1:
        yield TEXT[start:end]
        verse += 1
        start = TEXT.find(f"{verse} ", start)
        end   = TEXT.find(f"{verse+1} ", start)
    yield TEXT[start:LENGTH]

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

def find_skipped_verses() -> BibleChapterSets:
    """
    The syntax to mark such a verse, at least on the NIV, (assume: verse 7):
    
    **ORIGINAL:**
    ```
    [7] 
    ```
    **TRANSFORMED TO:**
    ```
    7
    [7]
    ```
    """
    Chapters:BibleChapterSets = ALL_CHAPTERS
    for PTR in Chapters.iterate():
        TEXT = chapter_text(PTR)

        for i in range(1, PTR.total_verses+1):
            start = TEXT.find(f'[{i}]')
            if start != -1:
                Chapters.mark(PTR.translation, PTR.index)
    Print.red(Chapters.total_marked)
    return BibleChapterSets(Chapters.marked)

def is_standard_form(PTR:Chapter) -> bool:
    text = chapter_text(PTR)
    expected_total_verses = PTR.book.total_verses(PTR.chapter)
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def is_poetry_form(PTR:Chapter) -> bool:
    """ TODO: DOES NOT WORK!"""
    TOTAL_VERSES = PTR.book.total_verses(PTR.chapter)

    (title, text) = strip_title(chapter_text(PTR))


def has_standard_line(PTR:Chapter) -> bool:
    """ TODO: DOES NOT WORK!"""
    TOTAL_VERSES = PTR.book.total_verses(PTR.chapter)
    (title, text) = strip_title(chapter_text(PTR))

    lines = re.findall(r'.+', text)

    lines = text.splitlines()
    verse = 1
    for line in lines:
        pass

def has_missing_verses(PTR:Chapter) -> bool:
    """ Logic Problem: false positives where chapter mismatches exist between Eng/Rus (Psalms) """
    text = chapter_text(PTR)
    start = 0; END = text.__len__()

    for verse in range(1, PTR.total_verses+1):
        start = text[start:END].find(f'{verse} ')
        if start == -1:
            return True

    return False




def identify_missing_chapters(Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)) -> BibleChapterSets:
    """
    Two main problem group Chapters were deleted from `./python/bible_txt` to facilitate movement forward:
        - chapters missing verses (a common problem in the Gospels)
        - chapter->total_verse mismatches between Eng/Rus
        - ???
    """
    for PTR in Chapters.iterate():
        if not chapter_File(PTR).exists():
            Chapters.mark(PTR.translation, PTR.index)

    return Chapters

def identify_Chapters_missing_verses(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    """
    Missing Verses == LESS verses than expected and NOT a Psalms chapter
    
    A common problem for the Gospels, in default parsed form.

    **HOWEVER:** These Chapters have been temporarily deleted from the record, and will be dealt with later.
    """
    for PTR in Chapters.iterate():
        if has_missing_verses(PTR) and PTR.book != BIBLE.PSALMS:
            Chapters.mark(PTR.translation, PTR.index)
        
    return Chapters


def identify_Standard_Form(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    for PTR in Chapters.iterate():
        if is_standard_form(PTR):
            Chapters.mark(PTR.translation, PTR.index)

    return Chapters


def TEST_iterate_verses(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    """ Failure == `iterate_verses()` yields wrong # of verses """
    for PTR in Chapters.iterate():
        if PTR.total_verses != len(list(iterate_verses(PTR))):
            Chapters.mark(PTR.translation, PTR.index)

    return Chapters


def identify_Chapters_with_Standard_Lined_verse() -> BibleChapterSets:
    """
    TODO: NOT COMPLETE
    Certain verses mix both the Standard/Lined format, increasing parsing difficulty.

    **EXAMPLE:**
    ```
    1 Paul and Timothy, servants of Christ Jesus,
    To all God’s holy people in Christ Jesus at Philippi, together with the overseers and deacons:
    2 Grace and peace to you from God our Father and the Lord Jesus Christ.
    ```
    """
    Chapters:BibleChapterSets = StandardForm.Inverse
    for PTR in Chapters.iterate():
        TEXT = chapter_text(PTR)
        for text in iterate_verses(PTR):
            pass
            Chapters.mark(PTR.translation, PTR.index)
