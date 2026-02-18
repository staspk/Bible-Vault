import time
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE, Chapter
from models.BibleChapterSets import BibleChapterSet, BibleChapterSets
from models.bible_chapter_sets.abnormal_verse_count import Chapters_abnormal_verse_count
from models.bible_chapter_sets.missing_chapters import MissingChapters
import definitions; from definitions import ALL_TRANSLATIONS, TEMP_DIR
from parser import ALL_CHAPTERS, chapter_File, chapter_text


BIBLE_TXT          = definitions.BIBLE_TXT_NEW      # the main set in python, currently standardized, ready to be consumed.
BIBLE_TXT_PARTIAL  = definitions.BIBLE_TXT_PARTIAL  # currently: Missing_Chapters from above
BIBLE_TXT_CURRENT  = definitions.BIBLE_TXT_CURRENT
BIBLE_TXT_POSTPONED = definitions.BIBLE_TXT_POSTPONED

def compare_changes(before:str, after:str):
    File(TEMP_DIR, 'pre.txt').save(before).open()
    time.sleep(.02)
    File(TEMP_DIR, 'post.txt').save(after).open()
    input()

def strip_title(PTR:Chapter, directory:str) -> tuple[str, str]:
    """
    NOTE: This `strip_title()` was intended to be used Post-Step1-Transformation, i.e: after `standardize_chapter_number_formatting()`
    
    **Returns:**
        `(title, rest)`
            `title == ""`, if no title in text
    """
    TEXT = chapter_text(PTR, directory)
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

def line_has_verse_num_AND_verse_text(line:str, minimum_verse_num:int, total_verses:int):
    """ helper function to: `standardize_verse_form_FOR_abnormal_verse_count()` """
    possible_verse_nums = range(minimum_verse_num, total_verses+3)  # +3 -> accounting for Chapters with: actual_total_verses > classic_total_verses (max distance == 2, supposedly)
    for verse_num in possible_verse_nums:
        if line.startswith(f'{verse_num} ') and len(line) > len(f'{verse_num} '):
            return True
    return False

def is_edge_case(chapter:Chapter) -> bool:
    """
    This function is necessary because verse iteration/transformation in STEP 2 assumes:
        next_verse_num > verse_num

    Currently, the only edge case found: RSV Exodus 22
    verse order:
        - 1
        - 4
        - 2
        - 3
        - 5
        - ...

    I standardized this chapter by hand. 
    """
    if chapter == Chapter(BIBLE.EXODUS, 22, translation='RSV'):
        return True
    return False

# --------------------------------------------------------------------------------------------------------------------------------
#       STEP #2
# --------------------------------------------------------------------------------------------------------------------------------
def standardize_verse_form(Chapters:BibleChapterSets = ALL_CHAPTERS(), only_report=False) -> tuple[BibleChapterSet, BibleChapterSet]:
    """
    STEP 2

    **PARAMETERS**:
        - `Chapters` - transformations will be done on: `Chapters.set`
        - `only_report` - if True: a theoretical run is done, without saving changes
    
    **RETURNS:**  
        `tuple[transformed, skipped]`  
        - `transformed` -> Chapters successfully transformed.
        - `skipped` -> Chapters that need a manual look/edit before `standardize_verse_form()` can transform text to new shape/formatting.

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

def standardize_verse_form_FOR_abnormal_verse_count(
    directory:str,
    Chapters:BibleChapterSets = Chapters_abnormal_verse_count.Chapters(),
    only_report=False
) -> tuple[BibleChapterSet, BibleChapterSet]:
    """
    STEP 2 - alternate implementation, necessary for Chapters that have:  
        - deviating *actual* total verses. Common in newer translations, which differ in source-texts used,
        but still report classic total verse counts for chapters.
        See: `./python/models/bible_chapter_sets/abnormal_verse_count.py`

    Guiding assumption/principle is that we do NOT know how many verses we will encounter during iteration, despite the BIBLE model claim

    **PARAMETERS**:
        - `directory` - `Chapters` residence
        - `Chapters` - transformations will be done on: `Chapters.set`
        - `only_report` - if True: a theoretical run is done without saving changes

    **RETURNS:**
    `tuple[transformed, skipped]`  
    - `transformed` -> Chapters successfully transformed.
    - `skipped` -> Chapters that raised Exception during transform operation.
    
    **SEE: `standardize_verse_form()` FOR BEFORE/AFTER EXAMPLE**
    """
    if not Test.text_starts_with_correct_versenum_after_strip_title(directory, Chapters):
        raise Exception('REQUIREMENT NOT MET: text_starts_with_correct_versenum_after_strip_title()')
    
    def is_verse_num_line(line:str, minimum_verse_num:int, total_verses:int) -> int|False:
        possible_verse_nums = range(minimum_verse_num, total_verses+3)  # +3 -> accounting for Chapters with: actual_total_verses > classic_total_verses (max distance == 2, supposedly)
        for verse_num in possible_verse_nums:
            if line.startswith(f'{verse_num} ') and len(line) > len(f'{verse_num} '):
                return verse_num
        return False
    
    transformed = BibleChapterSets(Chapters.set)
    skipped = BibleChapterSets(Chapters.set)
    
    for PTR in Chapters.iterate():
        # this implem wouldn't work because we assume: next_verse_num, is ALWAYS: next_verse_num > verse_num
        if is_edge_case(PTR) or not chapter_File(PTR, directory).exists():
            skipped.mark(PTR)
            continue
        try:
            title, text = strip_title(PTR, directory)
            new_text = ""

            verse_num = 1
            for line in text.splitlines():
                if line_has_verse_num_AND_verse_text(line, verse_num, PTR.total_verses):
                    verse_num, verse_text = line.split(" ", maxsplit=1)
                    new_text += f'{verse_num}\n'
                    new_text += f'{verse_text}\n'
                    verse_num += 1
                elif current_verse_num := is_verse_num_line():
                    new_text += f'{current_verse_num}\n'
                else:
                    new_text += f'{line}\n'
            
            if not only_report: chapter_File(PTR, directory).save(title+new_text)
            transformed.mark(PTR)
        except:
            skipped.mark(PTR)
        
    transformed.Save_Report('standardize_verse_form_FOR_abnormal_verse_count()_transformed')
    skipped.Save_Report('standardize_verse_form_FOR_abnormal_verse_count()_skipped')

    return (transformed.marked, skipped.marked)


# --------------------------------------------------------------------------------------------------------------------------------
#       STEP #1
# --------------------------------------------------------------------------------------------------------------------------------
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
    def text_starts_with_correct_versenum_after_strip_title(directory:str, CHAPTERS:BibleChapterSets=ALL_CHAPTERS()) -> bool:
        """
        A prerequisite test during `standardize_verse_form()`. Ensures `strip_title()` returns `text`  
        always starting with `"1 "`, i.e: the expected formatting Post-Step1-Transform
        """
        Chapters = BibleChapterSets(CHAPTERS.set)
        for PTR in Chapters.iterate():
            if not chapter_File(PTR, directory).exists():
                Chapters.mark(PTR)  # will not be transformed, so test not needed
                continue
            title, text = strip_title(PTR, directory)
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
