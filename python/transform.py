import time
from parser import TEST_chapter_number_formatting, TEST_iterate_verses, iterate_verses
from kozubenko.os import Directory, File
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW, BIBLE_TXT_PARTIAL, TEMP_DIR



DIRECTORY = BIBLE_TXT_NEW # BIBLE_TXT_PARTIAL

def ALL_CHAPTERS() -> BibleChapterSets: return BibleChapterSets.Subtract(BibleChapterSets.From(ALL_TRANSLATIONS).set, MissingChapters.chapters())

def chapter_File(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(PTR:Chapter): return File(DIRECTORY, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def compare_changes(before:str, after:str):
    File(TEMP_DIR, 'pre.txt').save(before, None).open()
    time.sleep(.01)
    File(TEMP_DIR, 'post.txt').save(after, None).open()
    input()
    Directory(TEMP_DIR).delete()


# def standardize_verse_form(Chapters = ALL_CHAPTERS()) -> BibleChapterSets:
def standardize_verse_form(PTR:Chapter) -> BibleChapterSets:
    """
    STEP 2

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
    # if TEST_chapter_number_formatting(Chapters).total_marked != 0: raise Exception('REQUIREMENT NOT MET: TEST_chapter_number_formatting().total_marked == 0')
    # if TEST_iterate_verses(Chapters).total_marked != 0:            raise Exception('REQUIREMENT NOT MET: TEST_iterate_verses().total_marked == 0')

    # for PTR in Chapters.iterate():
    # i = 1
    # for verse in iterate_verses(Chapter(BIBLE.GENESIS, 46, translation='NKJV')):
    #     Print.yellow(verse)

    #     i += 1

    TEXT = chapter_text(PTR)
    new_text = ""

    i = 1
    for verse in iterate_verses(PTR):
        
        i += 1

    compare_changes(TEXT, new_text)


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
            Chapters.mark(PTR.translation, PTR.index)
            
    Print.yellow(Chapters.total_marked)
    Chapters.Save_Report('identify_chapters_standardized()', "Standardized Chapters")
    return Chapters

