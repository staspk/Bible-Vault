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
from models.Bible import Chapter
from models.BibleChapterSets import BibleChapterSets
from models.bible_chapter_sets.abnormal_verse_count import abnormal_verse_count_Chapters


BIBLE_TXT          = definitions.BIBLE_TXT_NEW      # the main set in python, currently standardized, ready to be consumed.
BIBLE_TXT_PARTIAL  = definitions.BIBLE_TXT_PARTIAL  # currently: Missing_Chapters from above
BIBLE_TXT_CURRENT  = definitions.BIBLE_TXT_CURRENT
BIBLE_TXT_POSTPONED = definitions.BIBLE_TXT_POSTPONED

def ALL_CHAPTERS(): return BibleChapterSets.From(definitions.ALL_TRANSLATIONS).Mark(lambda Chapter:chapter_File(BIBLE_TXT, Chapter).exists()).Marked

def chapter_File(directory:str, PTR:Chapter): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt')
def chapter_text(directory:str, PTR:Chapter): return File(directory, PTR.translation, PTR.book.name, f'{PTR.chapter}.txt').contents(encoding='UTF-8')

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

    NOTE: Not sure what to do with: `title`, need to handle Eng/Rus Psalms Issue.
        Currently, not even saving it. Possibly could save to 0
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

    verse_num, start, end = find_verse_text(1, 0, len(TEXT))
    while end != -1:
        verse_num, start, end = find_verse_text(verse_num, start, end)

    verses[verse_num] = TEXT[start:len(TEXT) - 1]   # last verse

    return verses

def load_verses_FOR_abnormal_verse_count_Chapter(PTR:IChapter) -> dict[verse_num, verse_text]|None:
    """
    Intended to be used AFTER Standardization/Transform Steps.

    NOTE: Not sure what to do with: `title`, need to handle Eng/Rus Psalms Issue.
        Currently, not even saving it. Possibly could save to 0
    """
    return None

def Load_Verses(PTR:IChapter) -> dict[verse_num, verse_text]|None:
    """
    Intended to be used AFTER Standardization/Transform Steps.
    """
    if abnormal_verse_count_Chapters.includes(PTR):
        return load_verses_FOR_abnormal_verse_count_Chapter(PTR)
    return load_verses(PTR)

#---------------------------------------------------------------------
#      Quasi-Vestigial - but still useful!
#---------------------------------------------------------------------

def is_standard_form(directory:str, PTR:Chapter) -> bool:
    text = chapter_text(directory, PTR)
    expected_total_verses = PTR.total_verses
    lines = re.findall(r'.+', text)   # any single character (except newline), one or more repetitions
    if lines.__len__() == expected_total_verses:
        return True
    return False

def has_missing_verses(PTR:Chapter, directory:str) -> bool:
    """ I lack 100% certainty on this one, edge-case-wise. But keeping as an alternate iterating implementation """

    text = chapter_text(directory, PTR)
    start = 0; END = text.__len__()

    for verse in range(1, PTR.total_verses+1):
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
        if has_missing_verses(PTR, directory):
            Chapters.mark(PTR)
        
    return Chapters

def identify_Standard_Form(directory:str, Chapters:BibleChapterSets = ALL_CHAPTERS()) -> BibleChapterSets:
    for PTR in Chapters.iterate():
        if is_standard_form(directory, PTR):
            Chapters.mark(PTR)

    return Chapters
