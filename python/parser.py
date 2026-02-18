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
    
Oddities To Still Solve:
    " " aka: 6/MSP, John 15 NRT, 2 occurences. NOTE: NRT is riddled with these.
"""
import re, definitions
from kozubenko.os import File
from kozubenko.print import Print, colored_input
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters


BIBLE_TXT          = definitions.BIBLE_TXT_NEW      # the main set in python, currently standardized, ready to be consumed.
BIBLE_TXT_PARTIAL  = definitions.BIBLE_TXT_PARTIAL  # currently: Missing_Chapters from above
BIBLE_TXT_CURRENT  = definitions.BIBLE_TXT_CURRENT
BIBLE_TXT_POSTPONED = definitions.BIBLE_TXT_POSTPONED

def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(definitions.ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:Chapter, directory:str): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter, directory:str): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def move_Chapters(from_dir:str, to_dir:str, Chapters:BibleChapterSets):
    """ Moves: `Chapters.set` """
    for PTR in Chapters.iterate():
        chapter_File(PTR, from_dir).move(chapter_File(PTR, to_dir))

def open_Chapters(directory:str, Chapters:BibleChapterSets, step=50):
    """
    **PARAMETERS:**
        - `directory` - see: `parser.py` for the usual suspects
        - `Chapters` - `Chapters.set` are opened via Notepad++
    """
    i = 0
    for Chapter in Chapters.iterate():
        chapter = chapter_File(Chapter, directory)
        if chapter.exists():
            i += 1
            chapter.open()
            if i == 50:
                colored_input(f'Press Enter for {step} more...')
                i = 0
        else:
            Print.lite_red(f'open_Chapters(): {Chapter} does not exist!')



def is_standard_form(PTR:Chapter) -> bool:
    text = chapter_text(PTR)
    expected_total_verses = PTR.total_verses
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def has_missing_verses(PTR:Chapter, directory:str) -> bool:
    """ I lack 100% certainty on this one, edge-case-wise. But keeping as an alternate iterating implementation """

    text = chapter_text(PTR, directory)
    start = 0; END = text.__len__()

    for verse in range(1, PTR.total_verses+1):
        start = text[start:END].find(f'{verse} ')
        if start == -1:
            return True

    return False


def identify_missing_chapters(Chapters:BibleChapterSets = BibleChapterSets.From(definitions.ALL_TRANSLATIONS)) -> BibleChapterSets:
    """
    Two main problem group Chapters were deleted from `./python/bible_txt` to facilitate movement forward:
        - chapters missing verses (a common problem in the Gospels)
        - chapter->total_verse mismatches between Eng/Rus
        - ???

    **Returns:**
        - `BibleChapterSets.marked` -> missing chapters found by parser.py `chapter_File()`
    """
    for PTR in Chapters.iterate():
        if not chapter_File(PTR).exists():
            Chapters.mark(PTR)

    return Chapters

def identify_Chapters_missing_verses(directory:str, Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    """
    Missing Verses == LESS verses than expected and NOT a Psalms chapter
    
    A common problem for the Gospels, in default parsed form.

    **HOWEVER:** These Chapters have been temporarily deleted from the record, and will be dealt with later.
    """
    for PTR in Chapters.iterate():
        if has_missing_verses(PTR, directory):
            Chapters.mark(PTR)
        
    return Chapters

def identify_Standard_Form(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    for PTR in Chapters.iterate():
        if is_standard_form(PTR):
            Chapters.mark(PTR)

    return Chapters

