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
"""
import re
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW




DIRECTORY = BIBLE_TXT_NEW # BIBLE_TXT_PARTIAL
def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')


def is_standard_form(PTR:Chapter) -> bool:
    text = chapter_text(PTR)
    expected_total_verses = PTR.total_verses
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def has_missing_verses(PTR:Chapter) -> bool:
    """ I lack 100% certainty on this one, edge-case-wise. But keeping as an alternate iterating implementation """
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
            Chapters.mark(PTR)

    return Chapters

def identify_Chapters_missing_verses(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    """
    Missing Verses == LESS verses than expected and NOT a Psalms chapter
    
    A common problem for the Gospels, in default parsed form.

    **HOWEVER:** These Chapters have been temporarily deleted from the record, and will be dealt with later.
    """
    for PTR in Chapters.iterate():
        if has_missing_verses(PTR) and PTR.book != BIBLE.PSALMS:
            Chapters.mark(PTR)
        
    return Chapters

def identify_Standard_Form(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    for PTR in Chapters.iterate():
        if is_standard_form(PTR):
            Chapters.mark(PTR)

    return Chapters





"""
    .:: FOSSIL RECORD ::.

    Leftovers from some tests for iterate_verses(). Something in this form may be needed in the future.
"""
class Test2:
    """
    Runs tests on `iterate_verses()`
    """
    edge_cases:dict[Chapter, bool] = {
        Chapter(BIBLE.PSALMS,          42, translation='NET') : None,
        Chapter(BIBLE.FIRST_CHRONICLES, 3, translation='NRT') : None,
        # Chapter.From(850, translation='NRT'),
        # Chapter.From(12,  translation='NET'),
        # Chapter.From(411, translation='NIV'),
        # Chapter.From(411, translation='NET'),
        # Chapter.From(843, translation='NET'),
        # Chapter.From(87,  translation='NET')
    }

    def Run_Tests() -> bool:
        """
        **Returns:**
            `True` -> `iterate_verses()` being tested is trustworthy.
            `False` -> it is not.
        """
        return Test2.test_edge_cases()

    
    def test_edge_cases() -> bool:
        for edge_case in Test2.edge_cases.keys():
            VERSES = list(iterate_verses(edge_case))
            ACTUAL_VERSES = list(Edge_Case.get(edge_case).iterate_verses())

            if len(VERSES) != len(ACTUAL_VERSES):
                Test2.edge_cases[edge_case] = False
                continue

            for verse, actual_verse in zip(VERSES, ACTUAL_VERSES):
                if verse != actual_verse:
                    Test2.edge_cases[edge_case] = False

                if Test2.edge_cases[edge_case] == False:
                    break

            if Test2.edge_cases[edge_case] != False:
                Test2.edge_cases[edge_case] == True

        return all(Test2.edge_cases.values())