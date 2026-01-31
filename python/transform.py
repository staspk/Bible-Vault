import time
from typing import Iterator
from parser import TEST_chapter_number_formatting, TEST_iterate_verses
from kozubenko.os import Directory, File
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW, BIBLE_TXT_PARTIAL, TEMP_DIR
from tests.data.Test2_edge_cases import Edge_Case, IChapterIterator, NET_Psalms_42



DIRECTORY = BIBLE_TXT_NEW # BIBLE_TXT_PARTIAL

def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def compare_changes(before:str, after:str):
    File(TEMP_DIR, 'pre.txt').save(before).open()
    time.sleep(.02)
    File(TEMP_DIR, 'post.txt').save(after).open()
    input()

def strip_title(PTR:Chapter) -> tuple[str, str]:
    """
    NOTE: This `strip_title()` was intended to be used Post-Step1-Transformation, i.e: after `standardize_chapter_number_formatting()`
    
    **Returns:**
        `(title, rest)`
            `title == ""`, if no title in text
    """
    TEXT = chapter_text(PTR)
    lines = TEXT.splitlines(keepends=True)

    first_line = lines[0]
    if first_line[0:2] == "1 ": return ("", TEXT)

    # Guaranteed that title exists, so long as title does not begin with "1 " (I have never seen this, though not proven)

    # Every title <= 2 lines. To be safe, working backwards from line 5 to find first verse...
    i = 4
    while i > -1:
        if lines[i][0:2] == "1 ":
            title = "".join(lines[:i])
            rest  = "".join(lines[i:])
            return (title, rest)
        i -= 1
    
    raise Exception(f'strip_title(): Encountered text aberration. "1 " not found! Chapter: {str(PTR)}')

def standardize_verse_form(Chapters = ALL_CHAPTERS()) -> BibleChapterSets:
    """
    STEP 2

    **RETURNS:**
        `BibleChapterSets.marked` -> successfully transformed. NOTE: NOT CURRENTLY TRUE

    **EXAMPLE:** Genesis 46 NKJV
    ```
    1 So Israel took his journey with all that he had, and came to Beersheba, and offered sacrifices to the God of his father Isaac.
    2 Then God spoke to Israel in the visions of the night, and said, “Jacob, Jacob!”
    And he said, “Here I am.”
    ```
    **BECOMES:**
    ```
    1
    So Israel took his journey with all that he had, and came to Beersheba, and offered sacrifices to the God of his father Isaac.
    2
    Then God spoke to Israel in the visions of the night, and said, “Jacob, Jacob!”
    And he said, “Here I am.”
    ```
    """
    if TEST_chapter_number_formatting(Chapters).total_marked != 0: raise Exception('REQUIREMENT NOT MET: TEST_chapter_number_formatting().total_marked == 0')
    if TEST_iterate_verses(Chapters).total_marked != 0:            raise Exception('REQUIREMENT NOT MET: TEST_iterate_verses().total_marked == 0')

    for PTR in Chapters.iterate():
        title, text = strip_title(PTR)
        new_text = ""

        try:
            verse_num = 1
            for verse in iterate_verses(PTR):
                first_line, rest = verse.split('\n', maxsplit=1)

                if len(first_line) > 3:
                    first_line_text = first_line.split(f'{verse_num} ')[1]
                    new_text += f'{verse_num}\n{first_line_text}\n{rest}'
                else:
                    new_text += verse

                verse_num += 1

            # if TEXT != new_text:
            #     chapter_File(PTR).save(new_text)
            #     Chapters.mark(PTR)

        except:
            Chapters.mark(PTR)
            continue
    
    return Chapters


def standardize_chapter_number_formatting() -> BibleChapterSets:
    """
    STEP 1

    NOTE: strip_title() assumptions have CHANGED since using this to transform !!!  
    NOTE: this version did not account for chapter mismatches between Eng/Rus

    **From:** `"{PTR.chapter} "`  
    **To:** `"1 "`

    **Returns:**
        `marked` Chapters that were transformed.

    **EXAMPLE:** Genesis 3
    ```
    3 Now the serpent was more crafty than any other beast of the field that the Lord God had made.
    He said to the woman, “Did God actually say, ‘You shall not eat of any tree in the garden’?”
    2 And the woman said to the serpent, “We may eat of the fruit of the trees in the garden,
    ```
    **BECOMES:**
    ```
    1 Now the serpent was more crafty than any other beast of the field that the Lord God had made.
    He said to the woman, “Did God actually say, ‘You shall not eat of any tree in the garden’?”
    2 And the woman said to the serpent, “We may eat of the fruit of the trees in the garden,
    ```
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
            Chapters.mark(PTR)
            
    Print.yellow(Chapters.total_marked)
    Chapters.Save_Report('identify_chapters_standardized()', "Standardized Chapters")
    return Chapters


before_text = str
after_text = str
class Test:
    def standardize_verse_form(PTR:Chapter) -> tuple[before_text, after_text]:
        TEXT = chapter_text(PTR)
        new_text = ""

        verse_num = 1
        for verse in iterate_verses(PTR):
            first_line, rest = verse.split('\n', maxsplit=1)

            if len(first_line) > 3:
                first_line_text = first_line.split(f'{verse_num} ')[1]
                new_text += f'{verse_num}\n{first_line_text}\n{rest}'
            else:
                new_text += verse

            verse_num += 1

        return (TEXT, new_text)


class Transform:
    """
    STEP 1: 
    STEP 2: `standardize_verse_form()`
    """

    def standardize_verse_form(Chapters = ALL_CHAPTERS()) -> BibleChapterSets:
        """
        Manual Changes:
        """
        if TEST_chapter_number_formatting(Chapters).total_marked != 0: raise Exception('REQUIREMENT NOT MET: TEST_chapter_number_formatting().total_marked == 0')
        if TEST_iterate_verses(Chapters).total_marked != 0:            raise Exception('REQUIREMENT NOT MET: TEST_iterate_verses().total_marked == 0')


        results = standardize_verse_form(Chapters).Save_Report('transform_standardize_verse_form_')

class Test1:
    def chapter_number_formatting(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
        """
        **Returns:**
            `BibleChapterSets.marked` -> Chapter that after `strip_title()`, don't start with "1", i.e: the correct verse_number
        """
        for PTR in Chapters.iterate():
            if PTR.total_verses != len(list(iterate_verses(PTR))):
                Chapters.mark(PTR)

        return Chapters

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

    def iterate_verses(Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
        """
        **Returns:**:
            `BibleChapterSets.marked` -> Chapters that `iterate_verses()` yielded wrong # of verses
        """
        for PTR in Chapters.iterate():
            if PTR.total_verses != len(list(iterate_verses(PTR))):
                Chapters.mark(PTR)

        return Chapters
    

