"""
Intended to be used AFTER all Transform steps, on standardized Bible Chapter .txts:
    - strip_title()
    - load_verses()

----------------------------------------------------------------------------------

parser.py also holds leftovers used to test scrape results BEFORE/BETWEEN Transformation Steps.
    Much was destroyed due to poor methodology/unforeseen gaps. This is what remains...

----------------------------------------------------------------------------------

Below is the Analysis of Scraping 10 versions/translations of the Bible, before Transformation/Standardization Steps:
    ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

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
from models.IChapter import IChapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.abnormal_verse_count import abnormal_verse_count_Chapters


BIBLE_TXT          = definitions.BIBLE_TXT_NEW      # the main set in python, currently standardized, ready to be consumed.
BIBLE_TXT_PARTIAL  = definitions.BIBLE_TXT_PARTIAL  # currently: Missing_Chapters from above
BIBLE_TXT_CURRENT  = definitions.BIBLE_TXT_CURRENT
BIBLE_TXT_POSTPONED = definitions.BIBLE_TXT_POSTPONED

def ALL_CHAPTERS(): return BibleChapterSets.From(definitions.ALL_TRANSLATIONS).Mark(lambda Chapter:chapter_File(BIBLE_TXT, Chapter).exists()).Marked

def chapter_File(directory:str, PTR:IChapter): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(directory:str, PTR:IChapter): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

def open_Chapters(directory:str, Chapters:BibleChapterSets, step=50):
    """
    **PARAMETERS:**
        - `directory` - see: `parser.py` for the usual suspects
        - `Chapters` - `Chapters.set` are opened via Notepad++
    """
    i = 0
    for Chapter in Chapters.iterate():
        chapter = chapter_File(directory, Chapter)
        if chapter.exists():
            i += 1
            chapter.open()
            if i == 50:
                colored_input(f'Press Enter for {step} more...')
                i = 0
        else:
            Print.lite_red(f'open_Chapters(): {Chapter} does not exist!')

def move_Chapters(Chapters:BibleChapterSets, from_dir:str, to_dir:str):
    """ Moves: `Chapters.set` """
    for PTR in Chapters.iterate():
        chapter_File(from_dir, PTR).move(chapter_File(to_dir, PTR))


type title = str; type rest = str
type verse_num = int; type verse_text = str

def strip_title(PTR:IChapter) -> tuple[title, rest]:
    """
    Intended to be used AFTER Standardization/Transform Steps.

    `title == ""`, if no `title` in Chapter text
    """
    TEXT = chapter_text(BIBLE_TXT, PTR)
    lines = TEXT.splitlines(keepends=True)

    if lines[0] == "1\n": return ("", TEXT)

    # Every title <= 2 lines. To be safe, working backwards from line 5 to find first verse...
    i = 4
    while i > -1:
        if lines[i] == "1\n":
            title = "".join(lines[:i])
            rest  = "".join(lines[i:])
            return (title, rest)
        i -= 1
    
    raise Exception(f'strip_title(): Encountered text aberration. "1\n" not found! Chapter: {str(PTR)}')

def load_verses(PTR:IChapter) -> dict[verse_num, verse_text]|None:
    """
    Intended to be used AFTER Standardization/Transform Steps. Standard Method.

    NOTE: `title` is "lost" here. Solve Eng/Rus Psalms Issue, first. Possibly could save to 0.
    NOTE: `title` in Russian/Masoretic IS verse 1 
    """
    if not chapter_File(BIBLE_TXT, PTR).exists():
        return None

    verses = {}
    title, TEXT = strip_title(PTR)

    def find_verse_text(verse_num:int, start:int, end:int) -> tuple[int, int]:
        start = TEXT.find(f'{verse_num}\n', end) + len(f'{verse_num}\n')
        end   = TEXT.find(f'\n{verse_num+1}', start)
        if end != -1:
            verses[verse_num] = TEXT[start:end]
            verse_num += 1

        return verse_num, start, end

    verse_num, start, end = find_verse_text(1, 0, 0)
    while end != -1:
        verse_num, start, end = find_verse_text(verse_num, start, end)

    verses[verse_num] = TEXT[start:len(TEXT) - 1]   # last verse

    return verses

def load_verses_FOR_abnormal_verse_count_Chapter(PTR:IChapter) -> dict[verse_num, verse_text]|None:
    """
    Intended to be used AFTER Standardization/Transform Steps.

    Guiding Assumptions/Principle: 

    NOTE: `title` is "lost" here. Solve Eng/Rus Psalms Issue, first. Possibly could save to 0.
    NOTE: `title` in Russian/Masoretic IS verse 1 
    """
    UPPER_BOUND_DIVERGENCE = 3  # Eng/Rus & Critical-Text Variations < 3
    CLASSIC_CHAPTER_VERSE_COUNT = PTR.book.total_verses(PTR.chapter)   # aka: 
    MAX_POSSIBLE_ACTUAL_VERSE_COUNT = CLASSIC_CHAPTER_VERSE_COUNT + UPPER_BOUND_DIVERGENCE

    if not chapter_File(BIBLE_TXT, PTR).exists():
        return None

    verses = {}
    title, TEXT = strip_title(PTR)

    verse_num_positions = {1:0}   # verse_num -> position aka. We assume EVERY Chapter starts with verse_num == 1. So far, so true.
    start = 0 + len(f'{1}\n')

    for verse_num in range(MAX_POSSIBLE_ACTUAL_VERSE_COUNT, MAX_POSSIBLE_ACTUAL_VERSE_COUNT+UPPER_BOUND_DIVERGENCE, -1):
        position = TEXT.find(f'\n{verse_num}\n', start)
        if position != -1:
            verse_num_positions[verse_num] = position
            break

    if len(verse_num_positions.keys()) != 2:
        raise Exception("Assumption/Domain Breakdown: verse_num_positions MUST have a min/max at this point, aka: len()==2")
    
    VERSE_NUM_AT_END = list(verse_num_positions.keys())[1]   # we have NOT proven a higher int does not exist: 1 <-between-> VERSE_NUM_AT_END. Such a Variance not found in current 10 Bible versions, but potential possible future problem...
    start = list(verse_num_positions.values())[0]
    end   = list(verse_num_positions.values())[1]

    remaining = list(range(2, VERSE_NUM_AT_END))
    possible_verse_nums = list(range(2, VERSE_NUM_AT_END))
    for verse_num in possible_verse_nums:
        verse_num_string = f'\n{verse_num}\n'
        position = TEXT.find(verse_num_string, start, end)
        if position != -1:
            verse_num_positions[verse_num] = position
            
            remaining.remove(verse_num)
            start = position

    for verse_num,position in verse_num_positions.items():
        offset = f'{len(verse_num)}'



    if len(remaining) == 0:   # temporary check to make sure abnormal_verse_count_Chapters ACTUALLY HAVE abnormal verse count
        if not VERSE_NUM_AT_END > CLASSIC_CHAPTER_VERSE_COUNT:  # negates subset that above check can't pin down properly
            raise Exception(f"load_verses_FOR_abnormal_verse_count_Chapter(): This Chapter ain't an abnormal: {IChapter}")

    return None

def Load_Verses(PTR:IChapter) -> dict[verse_num, verse_text]|None:
    """
    Intended to be used AFTER Standardization/Transform Steps.

    NOTE: `title` is "lost" here. Solve Eng/Rus Psalms Issue, first. Possibly could save to 0.
    NOTE: `title` in Russian/Masoretic IS verse 1 
    """
    if abnormal_verse_count_Chapters.includes(PTR):
        return load_verses_FOR_abnormal_verse_count_Chapter(PTR)
    return load_verses(PTR)



# -----------------------------------------------------------------------------------------------------------------
#      Quasi-Vestigial - but still useful!
# -----------------------------------------------------------------------------------------------------------------
def is_standard_form(directory:str, PTR:IChapter) -> bool:
    text = chapter_text(directory, PTR)
    expected_total_verses = PTR.book.total_verses(PTR.chapter)
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def has_missing_verses(directory:str, PTR:IChapter) -> bool:
    """ I lack 100% certainty on this one, edge-case-wise. But keeping as an alternate iterating implementation """

    text = chapter_text(directory, PTR)
    start = 0; END = text.__len__()

    for verse in range(1, PTR.book.total_verses(PTR.chapter)+1):
        start = text[start:END].find(f'{verse} ')
        if start == -1:
            return True

    return False


def identify_missing_chapters(directory:str, Chapters:BibleChapterSets = BibleChapterSets.From(definitions.ALL_TRANSLATIONS)) -> BibleChapterSets:
    """
    Two main problem group Chapters were deleted from `./python/bible_txt` to facilitate movement forward:
        - chapters missing verses (a common problem in the Gospels)
        - chapter->total_verse mismatches between Eng/Rus
        - ???

    **RETURNS:**
        - `BibleChapterSets.marked` -> missing chapters found by parser.py
    """
    for PTR in Chapters.iterate():
        if not chapter_File(directory, PTR).exists():
            Chapters.mark(PTR)

    return Chapters

def identify_Chapters_missing_verses(directory:str, Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    """
    Missing Verses == LESS verses than expected and NOT a Psalms chapter
    
    A common problem for the Gospels, in default parsed form.

    **HOWEVER:** These Chapters have been temporarily deleted from the record, and will be dealt with later.
    """
    for PTR in Chapters.iterate():
        if has_missing_verses(directory, PTR):
            Chapters.mark(PTR)
        
    return Chapters

def identify_Standard_Form(directory:str, Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    for PTR in Chapters.iterate():
        if is_standard_form(directory, PTR):
            Chapters.mark(PTR)

    return Chapters
# -----------------------------------------------------------------------------------------------------------------



class Test:
    @staticmethod
    def load_verses_FOR_abnormal_verse_count_Chapter(PTR:IChapter):

        return False