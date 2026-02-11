import time
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import Chapter
from models.BibleChapterSets import BibleChapterSet, BibleChapterSets
from models.bible_chapter_sets.missing_chapters import MissingChapters
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW, TEMP_DIR



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

    # Guaranteed that title exists, so long as title does not begin with "1 " (Never seen, though not proven)

    # Every title <= 2 lines. To be safe, working backwards from line 5 to find first verse...
    i = 4
    while i > -1:
        if lines[i][0:2] == "1 ":
            title = "".join(lines[:i])
            rest  = "".join(lines[i:])
            return (title, rest)
        i -= 1
    
    raise Exception(f'strip_title(): Encountered text aberration. "1 " not found! Chapter: {str(PTR)}')


def standardize_verse_form(Chapters:BibleChapterSets = ALL_CHAPTERS(), only_report=False) -> tuple[BibleChapterSet, BibleChapterSet]:
    """
    STEP 2
    
    **RETURNS:**  
        `tuple[transformed, skipped]`  
        - `transformed` -> Chapters successfully transformed.
        - `skipped` -> Chapters that need a manual look/edit before `standardize_verse_form()` can transform text to new shape/formatting.

    NOTES:
        - every line will begin begin at position 0

    **EXAMPLE:** Genesis 46 NKJV
    ```
    1 So Israel took his journey with all that he had, and came to Beersheba, and offered sacrifices to the God of his father Isaac.
    2 Then God spoke to Israel in the visions of the night, and said, “Jacob, Jacob!”
    And he said, “Here I am.”
    3 
    ```
    **BECOMES:**
    ```
    1
    So Israel took his journey with all that he had, and came to Beersheba, and offered sacrifices to the God of his father Isaac.
    2
    Then God spoke to Israel in the visions of the night, and said, “Jacob, Jacob!”
    And he said, “Here I am.”
    3
    ```
    """
    if not Test.text_starts_with_correct_versenum_after_strip_title(Chapters): raise Exception('REQUIREMENT NOT MET: text_starts_with_correct_versenum_after_strip_title()')

    transformed = BibleChapterSets(Chapters.set)
    skipped = BibleChapterSets(Chapters.set)

    for PTR in Chapters.iterate():
        title, text = strip_title(PTR)
        new_text = ""

        verse_num = 0
        for line in text.splitlines():
            if line.startswith(f'{verse_num+1} '):
                verse_num += 1

            if line.startswith(f'{verse_num} ') and len(line) > (len(str(verse_num)) + 1):
                verse_text = line.split(f'{verse_num} ')[1]
                new_text += f'{verse_num}\n{verse_text.strip()}\n'
                continue

            new_text += f'{line.replace("\n", "").strip()}\n'

        if not Test.ensure_new_text_has_correct_formatting(PTR, new_text):
            skipped.mark(PTR)
        else:
            if only_report is False:
                chapter_File(PTR).save(title+new_text)
            transformed.mark(PTR)

    transformed.Save_Report('standardize_verse_form()_transformed')
    skipped.Save_Report('standardize_verse_form()_skipped')

    return (transformed.marked, skipped.marked)

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
    def strip_title(PTR:Chapter, chapter_text:str) -> tuple[str, str]:
        """
        title == "", if no title

        **Returns:**
            - `(title, rest)`
        """
        lines = chapter_text.splitlines(keepends=True)

        if lines[0][0:len(f'{PTR.chapter} ')] == f'{PTR.chapter} ':
            return ("", "".join(lines))

        i = 4
        while i > -1:
            if lines[i][0:len(f'{PTR.chapter} ')] == f'{PTR.chapter} ':
                return (lines[0:i], "".join(lines[i:]))
            
            if lines[i][0:len(f'1 ')] == f'1 ':
                return (lines[0:i], "".join(lines[i:]))
            
            i -=1

        



    i = 1
    Chapters:BibleChapterSets = BibleChapterSets.From(ALL_TRANSLATIONS)
    for PTR in Chapters.iterate():
        (title, text) = strip_title(PTR.chapter, chapter_text(PTR))
        
        start_index = text.find(f'{PTR.chapter} ')
        if start_index == 0:
            text = "1" + text[len(str(PTR.chapter)):]

            chapter_File(PTR).save(f'{title}{text}', encoding='UTF-8')
            Chapters.mark(PTR)
            
    Print.yellow(Chapters.total_marked)
    Chapters.Save_Report('identify_chapters_standardized()', "Standardized Chapters")
    return Chapters


def Transform(chapters:BibleChapterSets):
    """
    **STEPS:**
        - `standardize_chapter_number_formatting()` NOTE: NEEDS FIX! SEE FUNCTION...
    """

    # standardize_chapter_number_formatting()


class Test:
    def text_starts_with_correct_versenum_after_strip_title(CHAPTERS:BibleChapterSets=ALL_CHAPTERS()) -> bool:
        """
        A prerequisite test during `standardize_verse_form()`. Ensures `strip_title()` returns `text`  
        always starting with `"1 "`, i.e: the expected formatting Post-Step1-Transform
        """
        Chapters = BibleChapterSets(CHAPTERS.set)
        for PTR in Chapters.iterate():
            title, text = strip_title(PTR)
            if text[0:2] == "1 ":
                Chapters.mark(PTR)

        return (Chapters.total == Chapters.total_marked)

    def ensure_new_text_has_correct_formatting(PTR:Chapter, new_text:str) -> bool:
        """
        Test used during `standardize_verse_form()` to ensure `new_text`:
            - has expected # of verses
            - every verse_num has correct formatting, i.e:
        ```
        "{verse_num}\n"
        ```
        """
        passed_test:bool = True 
        
        verse_num = 0
        for line in new_text.splitlines(keepends=True):
            if line.startswith(f'{verse_num+1}'):
                verse_num += 1
                
                if line != f"{verse_num}\n":
                    passed_test = False
                    break
        
        return (verse_num == PTR.total_verses and passed_test)
